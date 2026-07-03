use plotive::{des, geom, style, text};
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyTuple};

use super::{extract_class_name, getattr_not_none};
use crate::py_annot::extract_annot;
use crate::py_legend::{extract_figure_legend, extract_plot_legend};
use crate::py_series::extract_series;
use crate::py_style::{extract_theme_color, extract_theme_fill, extract_theme_stroke};

fn extract_text_props(
    py_props: &Bound<'_, PyAny>,
) -> PyResult<text::TextProps<style::theme::Color>> {
    let mut props = text::TextProps::<style::theme::Color>::default();

    if let Some(py_family) = getattr_not_none(py_props, "family")? {
        let family = py_family.extract::<String>()?;
        props.family = Some(text::parse_font_families(&family).map_err(|e| {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Failed to parse font family string: {}",
                e
            ))
        })?);
    }

    if let Some(py_weight) = getattr_not_none(py_props, "weight")? {
        if let Ok(py_weight) = py_weight.extract::<u16>() {
            props.weight = Some(text::font::Weight(py_weight));
        } else if let Ok(py_weight) = py_weight.extract::<String>() {
            match py_weight.as_str() {
                "thin" => props.weight = Some(text::font::Weight::THIN),
                "extra-light" => props.weight = Some(text::font::Weight::EXTRA_LIGHT),
                "light" => props.weight = Some(text::font::Weight::LIGHT),
                "normal" => props.weight = Some(text::font::Weight::NORMAL),
                "medium" => props.weight = Some(text::font::Weight::MEDIUM),
                "semi-bold" => props.weight = Some(text::font::Weight::SEMIBOLD),
                "bold" => props.weight = Some(text::font::Weight::BOLD),
                "extra-bold" => props.weight = Some(text::font::Weight::EXTRA_BOLD),
                "black" => props.weight = Some(text::font::Weight::BLACK),
                _ => {
                    return Err(pyo3::exceptions::PyValueError::new_err(format!(
                        "Unknown text weight string: {}",
                        py_weight
                    )));
                }
            }
        } else {
            return Err(pyo3::exceptions::PyTypeError::new_err(
                "Text weight must be either an integer or a string.",
            ));
        }
    }
    if let Some(py_width) = getattr_not_none(py_props, "width")? {
        if let Ok(py_width) = py_width.extract::<f32>() {
            let width = py_width.clamp(1.0, 9.0).round() as i32;
            match width {
                1 => props.width = Some(text::font::Width::UltraCondensed),
                2 => props.width = Some(text::font::Width::ExtraCondensed),
                3 => props.width = Some(text::font::Width::Condensed),
                4 => props.width = Some(text::font::Width::SemiCondensed),
                5 => props.width = Some(text::font::Width::Normal),
                6 => props.width = Some(text::font::Width::SemiExpanded),
                7 => props.width = Some(text::font::Width::Expanded),
                8 => props.width = Some(text::font::Width::ExtraExpanded),
                9 => props.width = Some(text::font::Width::UltraExpanded),
                _ => unreachable!(),
            }
        } else if let Ok(py_width) = py_width.extract::<String>() {
            match py_width.as_str() {
                "ultra-condensed" => props.width = Some(text::font::Width::UltraCondensed),
                "extra-condensed" => props.width = Some(text::font::Width::ExtraCondensed),
                "condensed" => props.width = Some(text::font::Width::Condensed),
                "semi-condensed" => props.width = Some(text::font::Width::SemiCondensed),
                "normal" => props.width = Some(text::font::Width::Normal),
                "semi-expanded" => props.width = Some(text::font::Width::SemiExpanded),
                "expanded" => props.width = Some(text::font::Width::Expanded),
                "extra-expanded" => props.width = Some(text::font::Width::ExtraExpanded),
                "ultra-expanded" => props.width = Some(text::font::Width::UltraExpanded),
                _ => {
                    return Err(pyo3::exceptions::PyValueError::new_err(format!(
                        "Unknown text width string: {}",
                        py_width
                    )));
                }
            }
        } else {
            return Err(pyo3::exceptions::PyTypeError::new_err(
                "Text width must be either a float or a string.",
            ));
        }
    }

    if let Some(py_style) = getattr_not_none(py_props, "style")? {
        if let Ok(py_style) = py_style.extract::<String>() {
            match py_style.as_str() {
                "normal" => props.style = Some(text::font::Style::Normal),
                "italic" => props.style = Some(text::font::Style::Italic),
                "oblique" => props.style = Some(text::font::Style::Oblique),
                _ => {
                    return Err(pyo3::exceptions::PyValueError::new_err(format!(
                        "Unknown text style string: {}",
                        py_style
                    )));
                }
            }
        } else {
            return Err(pyo3::exceptions::PyTypeError::new_err(
                "Text style must be a string.",
            ));
        }
    }

    if let Some(py_color) = py_props.getattr_opt("color")? {
        if !py_color.is_none() {
            let color = extract_theme_fill(&py_color, style::theme::Col::Foreground.into())?;
            props.color = Some(Some(color));
        } else {
            props.color = Some(None);
        }
    }

    if let Some(py_outline) = py_props.getattr_opt("outline")? {
        if !py_outline.is_none() {
            let outline = extract_theme_stroke(&py_outline, style::theme::Col::Foreground.into())?;
            props.outline = Some(Some(outline));
        } else {
            props.outline = Some(None);
        }
    }

    if let Some(py_underline) = getattr_not_none(py_props, "underline")? {
        props.underline = Some(py_underline.extract()?);
    }

    if let Some(py_strikethrough) = getattr_not_none(py_props, "strikethrough")? {
        props.strikethrough = Some(py_strikethrough.extract()?);
    }

    Ok(props)
}

pub fn extract_text(py_text: &Bound<'_, PyAny>) -> PyResult<des::Text> {
    if let Ok(text) = py_text.extract::<String>() {
        Ok(des::Text::Plain(text))
    } else if let Ok(fmt) = py_text.extract::<Vec<String>>() {
        Ok(des::Text::Rich(fmt.join("\n")))
    } else if let Ok(py_text) = py_text.cast::<PyTuple>() {
        let fmt = py_text.get_item(0)?.extract::<String>()?;
        let py_classes = py_text.get_item(1)?;
        let py_classes = py_classes.cast::<PyDict>()?;
        let mut classes = Vec::new();
        for (py_key, py_class) in py_classes {
            let key = py_key.extract::<String>()?;
            let class = extract_text_props(&py_class)?;
            classes.push((key, class));
        }
        Ok(des::Text::RichWithClasses { fmt, classes })
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "Text must be a string or a RichText object.",
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

fn extract_axis_range(py_range: &Bound<'_, PyAny>) -> PyResult<des::axis::Range> {
    let (min, max): (Option<f64>, Option<f64>) = py_range.extract()?;
    Ok(des::axis::Range(min, max))
}

pub fn extract_axis_scale(py_scale: &Bound<'_, PyAny>) -> PyResult<des::axis::Scale> {
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

pub fn extract_ticks_locator(py_locator: &Bound<'_, PyAny>) -> PyResult<des::axis::ticks::Locator> {
    let cls_name = extract_class_name(py_locator)?;
    match cls_name.as_str() {
        "AutoTicksLocator" => Ok(des::axis::ticks::Locator::Auto),
        "ListTicksLocator" => {
            Ok(des::axis::ticks::ListLocator(py_locator.getattr("ticks")?.extract()?).into())
        }
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
    if let Some(py_lbl_props) = getattr_not_none(py_ticks, "label_props")? {
        let lbl_props = extract_text_props(&py_lbl_props)?;
        ticks = ticks.with_label_props(lbl_props);
    }
    if let Some(py_color) = getattr_not_none(py_ticks, "color")? {
        let color = extract_theme_color(&py_color, style::theme::Col::Foreground.into())?;
        ticks = ticks.with_color(color);
    }
    Ok(ticks)
}

fn extract_axis(py_axis: &Bound<'_, PyAny>) -> PyResult<des::Axis> {
    let mut axis = des::Axis::new().with_scale(extract_axis_scale(&py_axis.getattr("scale")?)?);

    if let Some(py_title) = getattr_not_none(py_axis, "title")? {
        let title = extract_text(&py_title)?;
        axis = axis.with_title(title);
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
        let stroke = extract_theme_stroke(&py_grid, style::theme::Col::Grid.into())?;
        axis = axis.with_grid(stroke.into());
    }

    if let Some(py_minor_ticks) = getattr_not_none(py_axis, "minor_ticks")? {
        let locator = extract_ticks_locator(&py_minor_ticks)?;
        let minor_ticks = des::axis::MinorTicks::new().with_locator(locator);
        axis = axis.with_minor_ticks(minor_ticks);
    }

    if let Some(py_minor_grid) = getattr_not_none(py_axis, "minor_grid")? {
        let stroke = extract_theme_stroke(&py_minor_grid, style::theme::Col::Grid.into())?;
        axis = axis.with_minor_grid(stroke.into());
    }

    Ok(axis)
}

fn extract_colorbar(py_cbar: &Bound<'_, PyAny>) -> PyResult<des::ColorBar> {
    let pos = getattr_not_none(py_cbar, "pos")?
        .map(|py_pos| {
            let pos_str: String = py_pos.extract()?;
            match pos_str.as_str() {
                "auto" => Ok(des::colorbar::Pos::default()),
                "top" => Ok(des::colorbar::Pos::Top),
                "right" => Ok(des::colorbar::Pos::Right),
                "bottom" => Ok(des::colorbar::Pos::Bottom),
                "left" => Ok(des::colorbar::Pos::Left),
                _ => {
                    return Err(pyo3::exceptions::PyValueError::new_err(format!(
                        "Unknown colorbar position string: {}",
                        pos_str
                    )));
                }
            }
        })
        .transpose()?
        .unwrap_or_default();

    let mut cbar = des::ColorBar::new(pos);

    if let Some(py_width) = getattr_not_none(py_cbar, "width")? {
        cbar = cbar.with_width(py_width.extract()?);
    }

    if let Some(py_title) = getattr_not_none(py_cbar, "title")? {
        let title = extract_text(&py_title)?;
        cbar = cbar.with_title(title);
    }

    if let Some(py_border) = getattr_not_none(py_cbar, "border")? {
        let border = extract_theme_stroke(&py_border, style::theme::Col::Foreground.into())?;
        cbar = cbar.with_border(border.into());
    }

    if let Some(py_locator) = getattr_not_none(py_cbar, "ticks")? {
        let locator = extract_ticks_locator(&py_locator)?;
        cbar = cbar.with_ticks_locator(locator);
    }

    if let Some(py_margin) = getattr_not_none(py_cbar, "margin")? {
        cbar = cbar.with_margin(py_margin.extract()?);
    }

    Ok(cbar)
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

    if let Some(py_cbar) = getattr_not_none(py_plot, "colorbar")? {
        let cbar = extract_colorbar(&py_cbar)?;
        plot = plot.with_colorbar(cbar);
    }

    let py_title = py_plot.getattr("title")?;
    if !py_title.is_none() {
        let title = extract_text(&py_title)?;
        plot = plot.with_title(title);
    }

    if let Some(py_fill) = getattr_not_none(py_plot, "fill")? {
        let fill = extract_theme_fill(&py_fill, style::theme::Col::Background.into())?;
        plot = plot.with_fill(fill.into());
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

    let fill = py_fig
        .getattr_opt("fill")?
        .map(|f| extract_theme_fill(&f, style::theme::Col::Background.into()))
        .transpose()?;

    let mut fig = des::Figure::new(plots).with_fill(fill);

    if let Some(py_size) = getattr_not_none(py_fig, "size")? {
        let size = py_size.extract::<(f32, f32)>()?;
        fig = fig.with_size(geom::Size::new(size.0, size.1));
    }

    if let Some(py_title) = getattr_not_none(py_fig, "title")? {
        let title = extract_text(&py_title)?;
        fig = fig.with_title(title);
    }

    if let Some(py_legend) = getattr_not_none(py_fig, "legend")? {
        let legend = extract_figure_legend(&py_legend)?;
        fig = fig.with_legend(legend);
    }
    Ok(fig)
}
