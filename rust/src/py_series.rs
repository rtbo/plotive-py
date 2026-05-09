use plotive::des::series::BarsPosition;
use pyo3::prelude::*;

use plotive::{des, style};
use pyo3::types::{PyDateAccess, PyDateTime, PyList, PyTimeAccess};

use crate::py_style::{
    extract_series_color, extract_series_marker, extract_series_stroke, extract_stroke_pattern,
};
use crate::{extract_class_name, getattr_not_none};

fn datetime_conv(dt: &Bound<'_, PyDateTime>) -> PyResult<plotive::time::DateTime> {
    let comps = plotive::time::DateTimeComps {
        year: dt.get_year(),
        month: dt.get_month() as u32,
        day: dt.get_day() as u32,
        hour: dt.get_hour() as u32,
        minute: dt.get_minute() as u32,
        second: dt.get_second() as u32,
        micro: dt.get_microsecond(),
    };
    plotive::time::DateTime::try_from(comps).map_err(|err| {
        pyo3::exceptions::PyValueError::new_err(format!("Invalid datetime value: {err}"))
    })
}

fn extract_data_col(col: &Bound<'_, PyAny>) -> PyResult<des::DataCol> {
    if let Ok(src_ref) = col.extract::<String>() {
        Ok(des::DataCol::SrcRef(src_ref))
    } else if let Ok(values) = col.extract::<Vec<f64>>() {
        Ok(des::DataCol::Inline(values.into()))
    } else if let Ok(values) = col.extract::<Vec<String>>() {
        Ok(des::DataCol::Inline(values.into()))
    } else if let Ok(values) = col.cast::<PyList>() {
        if values.len() == 0 {
            // This case should be handled by the Vec<f64> branch
            return Err(pyo3::exceptions::PyValueError::new_err(
                "DataCol list cannot be empty.",
            ));
        }
        let item0 = values.get_item(0)?;
        if let Ok(dt0) = item0.cast::<PyDateTime>() {
            let mut res: Vec<plotive::time::DateTime> = Vec::with_capacity(values.len());
            res.push(datetime_conv(&dt0)?);
            for item in values.iter().skip(1) {
                let dt = item.cast::<PyDateTime>().map_err(|_| {
                    pyo3::exceptions::PyTypeError::new_err(
                        "DataCol datetime list must contain only datetime.datetime values.",
                    )
                })?;
                let date_time = datetime_conv(&dt)?;
                res.push(date_time);
            }
            Ok(des::DataCol::Inline(res.into()))
        } else {
            Err(pyo3::exceptions::PyTypeError::new_err(
                "Unsupported data type in list. DataCol list must contain either all floats, all strings, or all datetime.datetime values.",
            ))
        }
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "DataCol must be either a string (source reference) or a list of values.",
        ))
    }
}

fn extract_base(
    py_ser: &Bound<'_, PyAny>,
) -> PyResult<(
    Option<String>,
    Option<des::axis::Ref>,
    Option<des::axis::Ref>,
)> {
    let mut name = None;
    if let Some(py_name) = getattr_not_none(py_ser, "name")? {
        name = Some(py_name.extract()?);
    }

    let mut x_axis = None;
    if let Some(py_x_axis) = getattr_not_none(py_ser, "x_axis")? {
        // check if it is string or int
        if let Ok(id) = py_x_axis.extract::<String>() {
            x_axis = Some(des::axis::Ref::Id(id));
        } else if let Ok(idx) = py_x_axis.extract::<usize>() {
            x_axis = Some(des::axis::Ref::Idx(idx));
        } else {
            return Err(pyo3::exceptions::PyTypeError::new_err(
                "x_axis must be either a string (axis name) or an integer (axis index).",
            ));
        }
    }

    let mut y_axis = None;
    if let Some(py_y_axis) = getattr_not_none(py_ser, "y_axis")? {
        // check if it is string or int
        if let Ok(id) = py_y_axis.extract::<String>() {
            y_axis = Some(des::axis::Ref::Id(id));
        } else if let Ok(idx) = py_y_axis.extract::<usize>() {
            y_axis = Some(des::axis::Ref::Idx(idx));
        } else {
            return Err(pyo3::exceptions::PyTypeError::new_err(
                "x_axis must be either a string (axis name) or an integer (axis index).",
            ));
        }
    }

    Ok((name, x_axis, y_axis))
}

fn extract_line_series(ser: &Bound<'_, PyAny>) -> PyResult<des::Series> {
    let x = ser.getattr("x")?;
    let y = ser.getattr("y")?;
    let x_data = extract_data_col(&x)?;
    let y_data = extract_data_col(&y)?;
    let mut line = des::series::Line::new(x_data, y_data);

    let (name, x_axis, y_axis) = extract_base(ser)?;
    if let Some(name) = name {
        line = line.with_name(name);
    }
    if let Some(x_axis) = x_axis {
        line = line.with_x_axis(x_axis);
    }
    if let Some(y_axis) = y_axis {
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
        line = line.with_stroke(stroke);
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

    Ok(des::Series::Line(line))
}

fn extract_scatter_series(ser: &Bound<'_, PyAny>) -> PyResult<des::Series> {
    let x = ser.getattr("x")?;
    let y = ser.getattr("y")?;
    let x_data = extract_data_col(&x)?;
    let y_data = extract_data_col(&y)?;
    let mut scatter = des::series::Scatter::new(x_data, y_data);

    let (name, x_axis, y_axis) = extract_base(ser)?;
    if let Some(name) = name {
        scatter = scatter.with_name(name);
    }
    if let Some(x_axis) = x_axis {
        scatter = scatter.with_x_axis(x_axis);
    }
    if let Some(y_axis) = y_axis {
        scatter = scatter.with_y_axis(y_axis);
    }

    if let Some(py_marker) = getattr_not_none(ser, "marker")? {
        scatter = scatter.with_marker(extract_series_marker(&py_marker)?);
    }
    Ok(des::Series::Scatter(scatter))
}

pub fn extract_histogram_series(ser: &Bound<'_, PyAny>) -> PyResult<des::Series> {
    let py_data = ser.getattr("data")?;
    let data = extract_data_col(&py_data)?;
    let mut hist = des::series::Histogram::new(data);

    let (name, x_axis, y_axis) = extract_base(ser)?;
    if let Some(name) = name {
        hist = hist.with_name(name);
    }
    if let Some(x_axis) = x_axis {
        hist = hist.with_x_axis(x_axis);
    }
    if let Some(y_axis) = y_axis {
        hist = hist.with_y_axis(y_axis);
    }

    if let Some(py_color) = getattr_not_none(ser, "fill")? {
        hist = hist.with_fill(extract_series_color(&py_color)?.into());
    }

    let py_width = ser.getattr("linewidth")?;
    let py_style = ser.getattr("linestyle")?;
    let py_color = ser.getattr("linecolor")?;
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
        hist = hist.with_outline(stroke);
    }

    if ser.getattr("bins").is_ok() {
        let bins = ser.getattr("bins")?.extract()?;
        hist = hist.with_bins(bins);
    }

    if ser.getattr("density").is_ok() {
        let density: bool = ser.getattr("density")?.extract()?;
        if density {
            hist = hist.with_density();
        }
    }

    Ok(des::Series::Histogram(hist))
}

pub fn extract_bars_series(ser: &Bound<'_, PyAny>) -> PyResult<des::Series> {
    let py_x = ser.getattr("x")?;
    let x_data = extract_data_col(&py_x)?;
    let py_y = ser.getattr("y")?;
    let y_data = extract_data_col(&py_y)?;
    let mut bars = des::series::Bars::new(x_data, y_data);

    let (name, x_axis, y_axis) = extract_base(ser)?;
    if let Some(name) = name {
        bars = bars.with_name(name);
    }
    if let Some(x_axis) = x_axis {
        bars = bars.with_x_axis(x_axis);
    }
    if let Some(y_axis) = y_axis {
        bars = bars.with_y_axis(y_axis);
    }

    if let Some(py_color) = getattr_not_none(ser, "fill")? {
        bars = bars.with_fill(extract_series_color(&py_color)?.into());
    }

    if let Some(py_outline) = getattr_not_none(ser, "outline")? {
        let stroke = extract_series_stroke(&py_outline)?;
        bars = bars.with_outline(stroke);
    }

    let mut offset: Option<f32> = None;
    let mut width: Option<f32> = None;
    if let Some(py_offset) = getattr_not_none(ser, "bars_offset")? {
        offset = Some(py_offset.extract()?);
    }
    if let Some(py_width) = getattr_not_none(ser, "bars_width")? {
        width = Some(py_width.extract()?);
    }
    match (offset, width) {
        (Some(offset), Some(width)) => {
            bars = bars.with_position(BarsPosition { offset, width });
        }
        (Some(offset), None) => {
            bars = bars.with_position(BarsPosition {
                offset,
                ..Default::default()
            });
        }
        (None, Some(width)) => {
            bars = bars.with_position(BarsPosition {
                width,
                ..Default::default()
            });
        }
        (None, None) => {}
    }

    Ok(bars.into())
}

pub fn extract_series(ser: &Bound<'_, PyAny>) -> PyResult<des::Series> {
    // check subtype of series
    let cls_name = extract_class_name(ser)?;
    let series = match cls_name.as_str() {
        "Line" => extract_line_series(ser)?,
        "Scatter" => extract_scatter_series(ser)?,
        "Histogram" => extract_histogram_series(ser)?,
        "Bars" => extract_bars_series(ser)?,
        _ => {
            return Err(pyo3::exceptions::PyTypeError::new_err(format!(
                "Unsupported series type: {}",
                cls_name
            )));
        }
    };

    Ok(series)
}
