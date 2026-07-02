use pyo3::{prelude::*, types::PyTuple};

use plotive::{des, style};

use crate::{py_des::extract_text, py_style::{extract_theme_color, extract_theme_marker, extract_theme_stroke}};

pub fn extract_annot(py_annot: &Bound<'_, PyAny>) -> PyResult<des::Annotation> {
    let cls_name = super::extract_class_name(py_annot)?;
    let mut annot = match cls_name.as_str() {
        "Line" => extract_line_annot(py_annot).map(des::Annotation::Line),
        "Arrow" => extract_arrow_annot(py_annot).map(des::Annotation::Arrow),
        "Marker" => extract_marker_annot(py_annot).map(des::Annotation::Marker),
        "Label" => extract_label_annot(py_annot).map(des::Annotation::Label),
        _ => Err(pyo3::exceptions::PyTypeError::new_err(format!(
            "Unsupported annotation type: {}",
            cls_name
        ))),
    }?;
    if let Some(py_x_axis) = super::getattr_not_none(py_annot, "x_axis")? {
        let x_axis = py_x_axis.extract::<String>()?;
        annot = annot.with_x_axis(x_axis.into());
    }
    if let Some(py_y_axis) = super::getattr_not_none(py_annot, "y_axis")? {
        let y_axis = py_y_axis.extract::<String>()?;
        annot = annot.with_y_axis(y_axis.into());
    }
    if let Some(py_zpos) = super::getattr_not_none(py_annot, "zpos")? {
        let zpos = py_zpos.extract::<&str>()?;
        match zpos {
            "below-series" => annot = annot.with_zpos(des::annot::ZPos::BelowSeries),
            "above-series" => annot = annot.with_zpos(des::annot::ZPos::AboveSeries),
            _ => {
                return Err(pyo3::exceptions::PyValueError::new_err(
                    "zpos must be either 'below-series' or 'above-series'.",
                ));
            }
        }
    }
    Ok(annot)
}

fn extract_line_annot(py_line: &Bound<'_, PyAny>) -> PyResult<des::annot::Line> {
    let mut annot = if let Some(py_y) = super::getattr_not_none(py_line, "horizontal")? {
        let y = py_y.extract::<f64>()?;
        des::annot::Line::horizontal(y)
    } else if let Some(py_x) = super::getattr_not_none(py_line, "vertical")? {
        let x = py_x.extract::<f64>()?;
        des::annot::Line::vertical(x)
    } else if let Some(py_slope) = super::getattr_not_none(py_line, "slope")? {
        let ((x, y), slope) = py_slope.extract::<((f64, f64), f32)>()?;
        des::annot::Line::slope(x, y, slope)
    } else if let Some(py_two_points) = super::getattr_not_none(py_line, "two_points")? {
        let ((x1, y1), (x2, y2)) = py_two_points.extract::<((f64, f64), (f64, f64))>()?;
        des::annot::Line::two_points(x1, y1, x2, y2)
    } else {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "Line annotation must have either 'horizontal', 'vertical', 'slope' or 'two_points' attribute.",
        ));
    };

    if let Some(py_stroke) = super::getattr_not_none(py_line, "stroke")? {
        let stroke = extract_theme_stroke(&py_stroke, style::theme::Col::Foreground.into())?;
        annot = annot.with_stroke(stroke);
    }

    Ok(annot)
}

fn extract_arrow_annot(py_annot: &Bound<'_, PyAny>) -> PyResult<des::annot::Arrow> {
    let x = py_annot.getattr("x")?.extract::<f64>()?;
    let y = py_annot.getattr("y")?.extract::<f64>()?;
    let dx = py_annot.getattr("dx")?.extract::<f32>()?;
    let dy = py_annot.getattr("dy")?.extract::<f32>()?;
    let mut annot = des::annot::Arrow::new(x, y, dx, dy);
    if let Some(py_head_size) = super::getattr_not_none(py_annot, "head_size")? {
        let head_size = py_head_size.extract::<f32>()?;
        annot = annot.with_head_size(head_size);
    }
    if let Some(py_stroke) = super::getattr_not_none(py_annot, "stroke")? {
        let stroke = extract_theme_stroke(&py_stroke, style::theme::Col::Foreground.into())?;
        annot = annot.with_stroke(stroke);
    }
    Ok(annot)
}

fn extract_marker_annot(py_annot: &Bound<'_, PyAny>) -> PyResult<des::annot::Marker> {
    let x = py_annot.getattr("x")?.extract::<f64>()?;
    let y = py_annot.getattr("y")?.extract::<f64>()?;
    let mut annot = des::annot::Marker::new(x, y);
    if let Some(py_marker) = super::getattr_not_none(py_annot, "marker")? {
        let marker = extract_theme_marker(&py_marker)?;
        annot = annot.with_marker(marker);
    }

    Ok(annot)
}

fn extract_label_annot(py_annot: &Bound<'_, PyAny>) -> PyResult<des::annot::Label> {
    let x = py_annot.getattr("x")?.extract::<f64>()?;
    let y = py_annot.getattr("y")?.extract::<f64>()?;
    let text = extract_text(&py_annot.getattr("text")?)?;
    let mut annot = des::annot::Label::new(text, x, y);
    if let Some(py_anchor) = super::getattr_not_none(py_annot, "anchor")? {
        let anchor = py_anchor.extract::<&str>()?;
        annot = match anchor {
            "top-left" => annot.with_anchor(des::annot::Anchor::TopLeft),
            "top-center" => annot.with_anchor(des::annot::Anchor::TopCenter),
            "top-right" => annot.with_anchor(des::annot::Anchor::TopRight),
            "center-left" => annot.with_anchor(des::annot::Anchor::CenterLeft),
            "center" => annot.with_anchor(des::annot::Anchor::Center),
            "center-right" => annot.with_anchor(des::annot::Anchor::CenterRight),
            "bottom-left" => annot.with_anchor(des::annot::Anchor::BottomLeft),
            "bottom-center" => annot.with_anchor(des::annot::Anchor::BottomCenter),
            "bottom-right" => annot.with_anchor(des::annot::Anchor::BottomRight),
            _ => {
                return Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "Unknown anchor string: {}",
                    anchor
                )));
            }
        };
    }
    if let Some(py_angle) = super::getattr_not_none(py_annot, "angle")? {
        let angle = py_angle.extract::<f32>()?;
        annot = annot.with_angle(angle);
    }
    if let Some(py_frame) = super::getattr_not_none(py_annot, "frame")? {
        let py_frame = py_frame.cast::<PyTuple>()?;
        if py_frame.len() != 2 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "Frame must be a tuple of (fill, stroke).",
            ));
        }
        let py_fill = py_frame.get_item(0)?;
        let py_stroke = py_frame.get_item(1)?;
        let fill = if py_fill.is_none() {
            None
        } else {
            Some(extract_theme_color(&py_fill, style::theme::Col::Background.into())?.into())
        };
        let stroke = if py_stroke.is_none() {
            None
        } else {
            Some(extract_theme_stroke(
                &py_stroke,
                style::theme::Col::Foreground.into(),
            )?)
        };
        annot = annot.with_frame(fill, stroke);
    }

    Ok(annot)
}
