use plotive::{des, geom, style};
use pyo3::prelude::*;

use crate::getattr_not_none;
use crate::py_geom::extract_padding;
use crate::py_style::{extract_theme_fill, extract_theme_stroke};

fn extract_legend<P: Default>(py_legend: &Bound<'_, PyAny>, pos: P) -> PyResult<des::Legend<P>> {
    let mut legend = des::Legend::new(pos);
    if let Some(py_columns) = getattr_not_none(py_legend, "columns")? {
        legend = legend.with_columns(py_columns.extract()?);
    }
    if let Some(py_padding) = getattr_not_none(py_legend, "padding")? {
        let padding = extract_padding(&py_padding)?;
        legend = legend.with_padding(padding);
    }
    let fill = getattr_not_none(py_legend, "fill")?
        .map(|f| extract_theme_fill(&f, style::theme::Col::LegendFill.into()))
        .transpose()?;
    legend = legend.with_fill(fill);

    let border = getattr_not_none(py_legend, "border")?
        .map(|b| extract_theme_stroke(&b, style::theme::Col::LegendBorder.into()))
        .transpose()?;
    legend = legend.with_border(border);

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

pub fn extract_plot_legend(py_legend: &Bound<'_, PyAny>) -> PyResult<des::PlotLegend> {
    let mut pos = des::plot::LegendPos::default();
    if let Some(py_pos) = getattr_not_none(py_legend, "pos")? {
        let pos_str: String = py_pos.extract()?;
        pos = match pos_str.as_str() {
            "auto" => des::plot::LegendPos::default(),
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

pub fn extract_figure_legend(py_legend: &Bound<'_, PyAny>) -> PyResult<des::FigLegend> {
    let mut pos = des::figure::LegendPos::default();
    if let Some(py_pos) = getattr_not_none(py_legend, "pos")? {
        let pos_str: String = py_pos.extract()?;
        pos = match pos_str.as_str() {
            "auto" => des::figure::LegendPos::default(),
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
