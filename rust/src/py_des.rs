use plotive::{des, geom, style};
use pyo3::prelude::*;
use pyo3::types::PyList;

use crate::{py_annot::extract_annot, py_style::{extract_series_color, extract_stroke_pattern, extract_theme_color, extract_theme_stroke}};

use super::{extract_class_name, getattr_not_none};

fn extract_padding(py_padding: &Bound<'_, PyAny>) -> PyResult<geom::Padding> {
    if let Ok(pad) = py_padding.extract::<f32>() {
        Ok(geom::Padding::Even(pad))
    } else if let Ok((h, v)) = py_padding.extract::<(f32, f32)>() {
        Ok(geom::Padding::Center { v, h })
    } else if let Ok((t, r, b, l)) = py_padding.extract::<(f32, f32, f32, f32)>() {
        Ok(geom::Padding::Custom { t, r, b, l })
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "Padding must be a float, a tuple of two floats, or a tuple of four floats.",
        ))
    }
}

fn extract_data_col(col: &Bound<'_, PyAny>) -> PyResult<des::DataCol> {
    if let Ok(src_ref) = col.extract::<String>() {
        Ok(des::DataCol::SrcRef(src_ref))
    } else if let Ok(values) = col.extract::<Vec<f64>>() {
        Ok(des::DataCol::Inline(values.into()))
    } else if let Ok(values) = col.extract::<Vec<String>>() {
        Ok(des::DataCol::Inline(values.into()))
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "DataCol must be either a string (source reference) or a list of values.",
        ))
    }
}

fn extract_axis_ref(rf: &Bound<'_, PyAny>) -> PyResult<des::axis::Ref> {
    if let Ok(src_ref) = rf.extract::<String>() {
        Ok(des::axis::Ref::Id(src_ref))
    } else if let Ok(idx) = rf.extract::<usize>() {
        Ok(des::axis::Ref::Idx(idx))
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "Axis reference must be either a string (axis id or title) or an integer (axis index).",
        ))
    }
}

fn extract_series(ser: &Bound<'_, PyAny>) -> PyResult<des::Series> {
    // check subtype of series
    let cls_name = extract_class_name(ser)?;
    let series = match cls_name.as_str() {
        "Line" => {
            let x = ser.getattr("x")?;
            let y = ser.getattr("y")?;
            let x_data = extract_data_col(&x)?;
            let y_data = extract_data_col(&y)?;

            let mut line = des::series::Line::new(x_data, y_data);
            if let Some(name) = getattr_not_none(ser, "name")? {
                let name_str: String = name.extract()?;
                line = line.with_name(name_str);
            }
            if let Some(py_x_axis) = getattr_not_none(ser, "x_axis")? {
                let x_axis = extract_axis_ref(&py_x_axis)?;
                line = line.with_x_axis(x_axis);
            }
            if let Some(py_y_axis) = getattr_not_none(ser, "y_axis")? {
                let y_axis = extract_axis_ref(&py_y_axis)?;
                line = line.with_y_axis(y_axis);
            }
            let py_width = ser.getattr("linewidth")?;
            let py_style = ser.getattr("linestyle")?;
            let py_color = ser.getattr("color")?;
            if !py_width.is_none() || !py_style.is_none() || !py_color.is_none() {
                let mut stroke = style::series::Stroke::default();
                if !py_width.is_none() {
                    stroke.width = py_width.extract()?;
                }
                if !py_style.is_none() {
                    stroke.pattern = extract_stroke_pattern(&py_style)?;
                }
                if !py_color.is_none() {
                    stroke.color = extract_series_color(&py_color)?;
                }
                line = line.with_line(stroke);
            }

            if let Some(py_interp) = getattr_not_none(ser, "interpolation")? {
                let interp_str: &str = py_interp.extract()?;
                let interp = match interp_str {
                    "linear" => des::series::Interpolation::Linear,
                    "step-early" => des::series::Interpolation::StepEarly,
                    "step-middle" => des::series::Interpolation::StepMiddle,
                    "step-late" | "step" => des::series::Interpolation::StepLate,
                    "cubic" | "spline" => des::series::Interpolation::Spline,
                    _ => {
                        return Err(pyo3::exceptions::PyValueError::new_err(format!(
                            "Unknown interpolation method: {}",
                            interp_str
                        )));
                    }
                };
                line = line.with_interpolation(interp);
            }

            des::Series::Line(line)
        }
        _ => {
            return Err(pyo3::exceptions::PyTypeError::new_err(format!(
                "Unsupported series type: {}",
                cls_name
            )));
        }
    };

    Ok(series)
}

fn extract_axis_range(py_range: &Bound<'_, PyAny>) -> PyResult<des::axis::Range> {
    let (min, max): (Option<f64>, Option<f64>) = py_range.extract()?;
    Ok(des::axis::Range(min, max))
}

fn extract_axis_scale(py_scale: &Bound<'_, PyAny>) -> PyResult<des::axis::Scale> {
    let cls_name = extract_class_name(py_scale)?;
    match cls_name.as_str() {
        "AutoScale" => Ok(des::axis::Scale::Auto),
        "LinScale" => Ok(des::axis::Scale::Linear(extract_axis_range(
            &py_scale.getattr("range")?,
        )?)),
        "LogScale" => Ok(des::axis::LogScale::new(
            py_scale.getattr("base")?.extract()?,
            extract_axis_range(&py_scale.getattr("range")?)?,
        )
        .into()),
        "SharedScale" => Ok(des::axis::Scale::Shared(extract_axis_ref(
            &py_scale.getattr("ref")?,
        )?)),
        _ => Err(pyo3::exceptions::PyTypeError::new_err(format!(
            "Unsupported scale type: {}",
            cls_name
        ))),
    }
}

fn extract_ticks_locator(py_locator: &Bound<'_, PyAny>) -> PyResult<des::axis::ticks::Locator> {
    let cls_name = extract_class_name(py_locator)?;
    match cls_name.as_str() {
        "AutoTicksLocator" => Ok(des::axis::ticks::Locator::Auto),
        "MaxNTicksLocator" => Ok(des::axis::ticks::MaxNLocator {
            bins: py_locator.getattr("bins")?.extract()?,
            steps: py_locator.getattr("steps")?.extract()?,
        }
        .into()),
        "PiMultipleTicksLocator" => Ok(des::axis::ticks::PiMultipleLocator {
            bins: py_locator.getattr("bins")?.extract()?,
        }
        .into()),
        "LogTicksLocator" => Ok(des::axis::ticks::LogLocator {
            base: py_locator.getattr("base")?.extract()?,
        }
        .into()),
        "DateTimeTicksLocator" => {
            let unit = py_locator.getattr("unit")?.extract::<String>()?;
            let period = py_locator.getattr("period")?.extract::<u32>()?;
            match unit.as_str() {
                "seconds" => Ok(des::axis::ticks::DateTimeLocator::Seconds(period).into()),
                "minutes" => Ok(des::axis::ticks::DateTimeLocator::Minutes(period).into()),
                "hours" => Ok(des::axis::ticks::DateTimeLocator::Hours(period).into()),
                "days" => Ok(des::axis::ticks::DateTimeLocator::Days(period).into()),
                "weeks" => Ok(des::axis::ticks::DateTimeLocator::Weeks(period).into()),
                "months" => Ok(des::axis::ticks::DateTimeLocator::Months(period).into()),
                "years" => Ok(des::axis::ticks::DateTimeLocator::Years(period).into()),
                _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "Unknown DateTimeTicksLocator unit: {}",
                    unit
                ))),
            }
        }
        "TimeDeltaTicksLocator" => {
            let unit = py_locator.getattr("unit")?.extract::<String>()?;
            let period = py_locator.getattr("period")?.extract::<u32>()?;
            match unit.as_str() {
                "seconds" => Ok(des::axis::ticks::TimeDeltaLocator::Seconds(period).into()),
                "minutes" => Ok(des::axis::ticks::TimeDeltaLocator::Minutes(period).into()),
                "hours" => Ok(des::axis::ticks::TimeDeltaLocator::Hours(period).into()),
                "days" => Ok(des::axis::ticks::TimeDeltaLocator::Days(period).into()),
                _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "Unknown TimeDeltaTicksLocator unit: {}",
                    unit
                ))),
            }
        }
        _ => Err(pyo3::exceptions::PyTypeError::new_err(format!(
            "Unsupported ticks locator type: {}",
            cls_name
        ))),
    }
}

fn extract_ticks_formatter(
    py_formatter: &Bound<'_, PyAny>,
) -> PyResult<des::axis::ticks::Formatter> {
    let cls_name = extract_class_name(py_formatter)?;
    match cls_name.as_str() {
        "AutoTicksFormatter" => Ok(des::axis::ticks::Formatter::Auto),
        "SharedAutoTicksFormatter" => Ok(des::axis::ticks::Formatter::SharedAuto),
        "DecimalTicksFormatter" => Ok(des::axis::ticks::Formatter::Prec(
            py_formatter.getattr("precision")?.extract()?,
        )),
        "PercentTicksFormatter" => Ok(des::axis::ticks::PercentFormatter {
            decimal_places: py_formatter.getattr("decimals")?.extract()?,
        }
        .into()),
        "DateTimeTicksFormatter" => {
            let fmt: Option<String> = py_formatter
                .getattr_opt("fmt")?
                .map(|f| f.extract())
                .transpose()?;
            let formatter = fmt
                .map(|f| des::axis::ticks::DateTimeFormatter::Custom(f))
                .unwrap_or_else(|| des::axis::ticks::DateTimeFormatter::Auto);
            Ok(formatter.into())
        }
        "TimeDeltaTicksFormatter" => {
            let fmt: Option<String> = py_formatter
                .getattr_opt("fmt")?
                .map(|f| f.extract())
                .transpose()?;
            let formatter = fmt
                .map(|f| des::axis::ticks::TimeDeltaFormatter::Custom(f))
                .unwrap_or_else(|| des::axis::ticks::TimeDeltaFormatter::Auto);
            Ok(formatter.into())
        }
        _ => Err(pyo3::exceptions::PyTypeError::new_err(format!(
            "Unsupported ticks formatter type: {}",
            cls_name
        ))),
    }
}

fn extract_axis_ticks(py_ticks: &Bound<'_, PyAny>) -> PyResult<des::axis::Ticks> {
    let mut ticks = des::axis::Ticks::default();
    if let Ok(py_locator) = py_ticks.getattr("locator") {
        let locator = extract_ticks_locator(&py_locator)?;
        ticks = ticks.with_locator(locator);
    }
    if let Ok(py_formatter) = py_ticks.getattr("formatter") {
        let formatter = extract_ticks_formatter(&py_formatter)?;
        ticks = ticks.with_formatter(Some(formatter));
    } else {
        ticks = ticks.with_formatter(None);
    }
    Ok(ticks)
}

fn extract_axis(py_axis: &Bound<'_, PyAny>) -> PyResult<des::Axis> {
    let mut axis = des::Axis::new().with_scale(extract_axis_scale(&py_axis.getattr("scale")?)?);

    if let Some(py_title) = getattr_not_none(py_axis, "title")? {
        let title: String = py_title.extract()?;
        axis = axis.with_title(title.into());
    }

    if let Some(py_id) = getattr_not_none(py_axis, "id")? {
        let id: String = py_id.extract()?;
        axis = axis.with_id(id);
    }

    if let Some(py_opposite_side) = getattr_not_none(py_axis, "opposite_side")? {
        let opposite_side: bool = py_opposite_side.extract()?;
        if opposite_side {
            axis = axis.with_opposite_side();
        }
    }

    if let Some(py_ticks) = getattr_not_none(py_axis, "ticks")? {
        let ticks = extract_axis_ticks(&py_ticks)?;
        axis = axis.with_ticks(ticks);
    }

    if let Some(py_grid) = getattr_not_none(py_axis, "grid")? {
        let stroke = extract_theme_stroke(&py_grid)?;
        axis = axis.with_grid(stroke.into());
    }

    if let Some(py_minor_ticks) = getattr_not_none(py_axis, "minor_ticks")? {
        let locator = extract_ticks_locator(&py_minor_ticks)?;
        let minor_ticks = des::axis::MinorTicks::new().with_locator(locator);
        axis = axis.with_minor_ticks(minor_ticks);
    }

    if let Some(py_minor_grid) = getattr_not_none(py_axis, "minor_grid")? {
        let stroke = extract_theme_stroke(&py_minor_grid)?;
        axis = axis.with_minor_grid(stroke.into());
    }

    Ok(axis)
}

fn extract_legend<P: Default>(py_legend: &Bound<'_, PyAny>, pos: P) -> PyResult<des::Legend<P>> {
    let mut legend = des::Legend::new(pos);
    if let Some(py_columns) = getattr_not_none(py_legend, "columns")? {
        legend = legend.with_columns(py_columns.extract()?);
    }
    if let Some(py_padding) = getattr_not_none(py_legend, "padding")? {
        let padding = extract_padding(&py_padding)?;
        legend = legend.with_padding(padding);
    }
    if let Some(py_fill) = py_legend.getattr_opt("fill")? {
        if py_fill.is_none() {
            legend = legend.with_fill(None);
        } else {
            let fill = extract_theme_color(&py_fill)?;
            legend = legend.with_fill(Some(fill.into()));
        }
    }
    if let Some(py_spacing) = getattr_not_none(py_legend, "spacing")? {
        if let Ok(spacing) = py_spacing.extract::<f32>() {
            legend = legend.with_spacing(geom::Size::new(spacing, spacing));
        } else if let Ok((h, v)) = py_spacing.extract::<(f32, f32)>() {
            legend = legend.with_spacing(geom::Size::new(h, v));
        } else {
            return Err(pyo3::exceptions::PyTypeError::new_err(
                "Legend spacing must be a float or a tuple of two floats.",
            ));
        }
    }
    if let Some(py_margin) = getattr_not_none(py_legend, "margin")? {
        let margin = py_margin.extract::<f32>()?;
        legend = legend.with_margin(margin);
    }
    Ok(legend)
}

fn extract_plot_legend(py_legend: &Bound<'_, PyAny>) -> PyResult<des::PlotLegend> {
    let mut pos = des::plot::LegendPos::default();
    if let Some(py_pos) = getattr_not_none(py_legend, "pos")? {
        let pos_str: String = py_pos.extract()?;
        pos = match pos_str.as_str() {
            "out-top" => des::plot::LegendPos::OutTop,
            "out-right" => des::plot::LegendPos::OutRight,
            "out-bottom" => des::plot::LegendPos::OutBottom,
            "out-left" => des::plot::LegendPos::OutLeft,
            "in-top" => des::plot::LegendPos::InTop,
            "in-top-right" => des::plot::LegendPos::InTopRight,
            "in-right" => des::plot::LegendPos::InRight,
            "in-bottom-right" => des::plot::LegendPos::InBottomRight,
            "in-bottom" => des::plot::LegendPos::InBottom,
            "in-bottom-left" => des::plot::LegendPos::InBottomLeft,
            "in-left" => des::plot::LegendPos::InLeft,
            "in-top-left" => des::plot::LegendPos::InTopLeft,
            _ => {
                return Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "Unknown legend position string: {}",
                    pos_str
                )));
            }
        }
    }
    Ok(extract_legend(py_legend, pos)?)
}

fn extract_figure_legend(py_legend: &Bound<'_, PyAny>) -> PyResult<des::FigLegend> {
    let mut pos = des::figure::LegendPos::default();
    if let Some(py_pos) = getattr_not_none(py_legend, "pos")? {
        let pos_str: String = py_pos.extract()?;
        pos = match pos_str.as_str() {
            "top" => des::figure::LegendPos::Top,
            "right" => des::figure::LegendPos::Right,
            "bottom" => des::figure::LegendPos::Bottom,
            "left" => des::figure::LegendPos::Left,
            _ => {
                return Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "Unknown legend position string: {}",
                    pos_str
                )));
            }
        };
    }
    Ok(extract_legend(py_legend, pos)?)
}

fn extract_plot(py_plot: &Bound<'_, PyAny>) -> PyResult<des::Plot> {
    let py_series = py_plot.getattr("series")?;
    let py_series = py_series.cast::<PyList>()?;
    let mut series = Vec::with_capacity(py_series.len());

    for ser in py_series.iter() {
        let ser = extract_series(&ser)?;
        series.push(ser);
    }
    let mut plot = des::Plot::new(series);

    if let Some(py_legend) = getattr_not_none(py_plot, "legend")? {
        let legend = extract_plot_legend(&py_legend)?;
        plot = plot.with_legend(legend);
    }

    let py_title = py_plot.getattr("title")?;
    if !py_title.is_none() {
        let title: String = py_title.extract()?;
        plot = plot.with_title(title.into());
    }

    let py_x_axes = py_plot.getattr("x_axes")?;
    let py_x_axes = py_x_axes.cast::<PyList>()?;
    for py_x_axis in py_x_axes.iter() {
        let x_axis = extract_axis(&py_x_axis)?;
        plot = plot.with_x_axis(x_axis);
    }

    let py_y_axes = py_plot.getattr("y_axes")?;
    let py_y_axes = py_y_axes.cast::<PyList>()?;
    for py_y_axis in py_y_axes.iter() {
        let y_axis = extract_axis(&py_y_axis)?;
        plot = plot.with_y_axis(y_axis);
    }

    let py_annots = py_plot.getattr("annotations")?;
    let py_annots = py_annots.cast::<PyList>()?;
    for py_annot in py_annots.iter() {
        let annot = extract_annot(&py_annot)?;
        plot = plot.with_annotation(annot);
    }

    Ok(plot)
}

fn extract_row_col(subplot: &Bound<'_, PyAny>) -> PyResult<(u32, u32)> {
    if let Ok(tuple) = subplot.extract::<(u32, u32)>() {
        return Ok(tuple);
    } else if let Ok(list) = subplot.cast::<PyList>() {
        if list.len() == 2 {
            return Ok((list.get_item(0)?.extract()?, list.get_item(1)?.extract()?));
        }
    }
    Err(pyo3::exceptions::PyTypeError::new_err(
        "Subplot must be a tuple or list of two integers (rows, cols).",
    ))
}

fn extract_plots(
    py_plots: &Bound<'_, PyAny>,
    subplots: Option<(u32, u32)>,
    space: Option<f32>,
) -> PyResult<des::figure::Plots> {
    let py_plots = py_plots.cast::<PyList>()?;
    if py_plots.len() == 1 {
        let py_plot = py_plots.get_item(0)?;
        let plot = extract_plot(&py_plot)?;
        return Ok(plot.into());
    }

    if py_plots.len() == 0 {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "At least one plot must be provided.",
        ));
    }

    let mut plots = Vec::with_capacity(py_plots.len());
    let mut max_sp: Option<(u32, u32)> = None;

    for py_plot in py_plots.iter() {
        let plot = extract_plot(&py_plot)?;
        let subplot = getattr_not_none(&py_plot, "subplot")?
            .map(|sp| extract_row_col(&sp))
            .transpose()?;
        match (subplot, &mut max_sp) {
            (None, None) => (),
            (Some(sp), Some(subplots)) => {
                subplots.0 = sp.0.max(subplots.0);
                subplots.1 = sp.1.max(subplots.1);
            }
            (Some(sp), None) => max_sp = Some(sp),
            (None, Some(..)) => (),
        }
        plots.push((subplot, plot));
    }

    let subplots = match (subplots, max_sp) {
        (Some(subplots), Some(max_sp)) => {
            if subplots.0 < max_sp.0 || subplots.1 < max_sp.1 {
                return Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "Provided subplot grid {:?} is smaller than required grid {:?} for the plots.",
                    subplots, max_sp
                )));
            }
            subplots
        }
        (Some(subplots), None) => subplots,
        (None, Some(max_sp)) => max_sp,
        (None, None) => (py_plots.len() as u32, 1),
    };

    let (rows, cols) = subplots;
    let mut subplots = des::Subplots::new(rows, cols);
    // python has rows and cols starting at 1,
    // but des has rows and cols starting at 0
    let mut row = 0;
    let mut col = 0;
    for (sp, plot) in plots {
        let (r, c) = match sp {
            Some((r, c)) => (r - 1, c - 1),
            None => (row, col),
        };
        subplots = subplots.with_plot((r, c), plot);
        row += 1;
        if row >= rows {
            row = 0;
            col += 1;
        }
    }

    if let Some(space) = space {
        subplots = subplots.with_space(space);
    }

    Ok(subplots.into())
}

pub fn extract_figure(py_fig: &Bound<'_, PyAny>) -> PyResult<des::Figure> {
    let space = if let Ok(space) = py_fig.getattr("space") {
        Some(space.extract::<f32>()?)
    } else {
        None
    };
    let subplots = if let Ok(subplots) = py_fig.getattr("subplots") {
        Some(extract_row_col(&subplots)?)
    } else {
        None
    };
    let py_plots = py_fig.getattr("plots")?;
    let plots = extract_plots(&py_plots, subplots, space)?;

    let py_fill = py_fig.getattr_opt("fill")?;
    let fill = py_fill
        .map(|f| extract_theme_color(&f))
        .transpose()?
        .and_then(|c| {
            style::theme::Fill::Solid {
                color: c,
                opacity: None,
            }
            .into()
        });

    let mut fig = des::Figure::new(plots).with_fill(fill);

    if let Some(py_title) = getattr_not_none(py_fig, "title")? {
        let title_fmt: String = py_title.extract()?;
        let title = plotive_text::parse_rich_text(&title_fmt).map_err(|e| {
            pyo3::exceptions::PyValueError::new_err(format!("Failed to parse plot title: {}", e))
        })?;
        fig = fig.with_title(title.into());
    }

    if let Some(py_legend) = getattr_not_none(py_fig, "legend")? {
        let legend = extract_figure_legend(&py_legend)?;
        fig = fig.with_legend(legend);
    }
    Ok(fig)
}
