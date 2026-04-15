use pyo3::prelude::*;

use plotive::{des, style};

use crate::py_style::{extract_series_color, extract_series_marker, extract_stroke_pattern};
use crate::{extract_class_name, getattr_not_none};

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

fn extract_line_series(ser: &Bound<'_, PyAny>) -> PyResult<des::Series> {
    let x = ser.getattr("x")?;
    let y = ser.getattr("y")?;
    let x_data = extract_data_col(&x)?;
    let y_data = extract_data_col(&y)?;
    let mut line = des::series::Line::new(x_data, y_data);
    if let Some(name) = getattr_not_none(ser, "name")? {
        let name_str: String = name.extract()?;
        line = line.with_name(name_str);
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

    Ok(des::Series::Line(line))
}

fn extract_scatter_series(ser: &Bound<'_, PyAny>) -> PyResult<des::Series> {
    let x = ser.getattr("x")?;
    let y = ser.getattr("y")?;
    let x_data = extract_data_col(&x)?;
    let y_data = extract_data_col(&y)?;
    let mut scatter = des::series::Scatter::new(x_data, y_data);
    if let Some(name) = getattr_not_none(ser, "name")? {
        let name_str: String = name.extract()?;
        scatter = scatter.with_name(name_str);
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
    if let Some(name) = getattr_not_none(ser, "name")? {
        let name_str: String = name.extract()?;
        hist = hist.with_name(name_str);
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
        hist = hist.with_line(stroke);
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

pub fn extract_series(ser: &Bound<'_, PyAny>) -> PyResult<des::Series> {
    // check subtype of series
    let cls_name = extract_class_name(ser)?;
    let series = match cls_name.as_str() {
        "Line" => extract_line_series(ser)?,
        "Scatter" => extract_scatter_series(ser)?,
        "Histogram" => extract_histogram_series(ser)?,
        _ => {
            return Err(pyo3::exceptions::PyTypeError::new_err(format!(
                "Unsupported series type: {}",
                cls_name
            )));
        }
    };

    Ok(series)
}
