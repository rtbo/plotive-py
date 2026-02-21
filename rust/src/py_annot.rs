use pyo3::{prelude::*, types::PyTuple};

use plotive::des;

use crate::py_style::{extract_theme_color, extract_theme_stroke};

pub fn extract_annot(py_annot: &Bound<'_, PyAny>) -> PyResult<des::Annotation> {
    let cls_name = super::extract_class_name(py_annot)?;
    let mut annot = match cls_name.as_str() {
        "Line" => extract_line_annot(py_annot).map(des::Annotation::Line),
        "Arrow" => extract_arrow_annot(py_annot).map(des::Annotation::Arrow),
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
                ))
            }
        }
    }
    Ok(annot)
}

fn extract_line_annot(py_line: &Bound<'_, PyAny>) -> PyResult<des::annot::Line> {
    let mut line = if let Some(py_y) = super::getattr_not_none(py_line, "horizontal")? {
        let y = py_y.extract::<f64>()?;
        des::annot::Line::horizontal(y)
    } else if let Some(py_x) = super::getattr_not_none(py_line, "vertical")? {
        let x = py_x.extract::<f64>()?;
        des::annot::Line::vertical(x)
    } else if let Some(py_slope) = super::getattr_not_none(py_line, "slope")? {
        let ((x,  y), slope) = py_slope.extract::<((f64, f64), f32)>()?;
        des::annot::Line::slope(x, y, slope)
    } else if let Some(py_two_points) = super::getattr_not_none(py_line, "two_points")? {
        let ((x1, y1), (x2, y2)) = py_two_points.extract::<((f64, f64), (f64, f64))>()?;
        des::annot::Line::two_points(x1, y1, x2, y2)
    } else {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "Line annotation must have either 'horizontal', 'vertical', 'slope' or 'two_points' attribute.",
        ))
    };

    if let Some(py_stroke) = super::getattr_not_none(py_line, "stroke")? {
        let stroke = extract_theme_stroke(&py_stroke)?;
        line = line.with_line(stroke);
    }

    Ok(line)
}

fn extract_arrow_annot(py_annot: &Bound<'_, PyAny>) -> PyResult<des::annot::Arrow> {
    let x = py_annot.getattr("x")?.extract::<f64>()?;
    let y = py_annot.getattr("y")?.extract::<f64>()?;
    let dx = py_annot.getattr("dx")?.extract::<f32>()?;
    let dy = py_annot.getattr("dy")?.extract::<f32  >()?;
    let mut arrow = des::annot::Arrow::new(x, y, dx, dy);
    if let Some(py_head_size) = super::getattr_not_none(py_annot, "head_size")? {
        let head_size = py_head_size.extract::<f32>()?;
        arrow = arrow.with_head_size(head_size);
    }
    if let Some(py_stroke) = super::getattr_not_none(py_annot, "stroke")? {
        let stroke = extract_theme_stroke(&py_stroke)?;
        arrow = arrow.with_line(stroke);
    }
    Ok(arrow)
}

fn extract_label_annot(py_annot: &Bound<'_, PyAny>) -> PyResult<des::annot::Label> {
    let x = py_annot.getattr("x")?.extract::<f64>()?;
    let y = py_annot.getattr("y")?.extract::<f64>()?;
    let text = py_annot.getattr("text")?.extract::<String>()?;
    let mut label = des::annot::Label::new(text, x, y);
    if let Some(py_anchor) = super::getattr_not_none(py_annot, "anchor")? {
        let anchor = py_anchor.extract::<&str>()?;
        label = match anchor {
            "top-left" => label.with_anchor(des::annot::Anchor::TopLeft),
            "top-center" => label.with_anchor(des::annot::Anchor::TopCenter),
            "top-right" => label.with_anchor(des::annot::Anchor::TopRight),
            "center-left" => label.with_anchor(des::annot::Anchor::CenterLeft),
            "center" => label.with_anchor(des::annot::Anchor::Center),
            "center-right" => label.with_anchor(des::annot::Anchor::CenterRight),
            "bottom-left" => label.with_anchor(des::annot::Anchor::BottomLeft),
            "bottom-center" => label.with_anchor(des::annot::Anchor::BottomCenter),
            "bottom-right" => label.with_anchor(des::annot::Anchor::BottomRight),
            _ => {
                return Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "Unknown anchor string: {}",
                    anchor
                )));
            }
        };
    }
    if let Some(py_color) = super::getattr_not_none(py_annot, "color")? {
        let color = extract_theme_color(&py_color)?;
        label = label.with_color(color);
    }
    if let Some(py_angle) = super::getattr_not_none(py_annot, "angle")? {
        let angle = py_angle.extract::<f32>()?;
        label = label.with_angle(angle);
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
            Some(extract_theme_color(&py_fill)?.into())
        };
        let stroke = if py_stroke.is_none() {
            None
        } else {
            Some(extract_theme_stroke(&py_stroke)?)
        };
        label = label.with_frame(fill, stroke);
    }

    Ok(label)
}
