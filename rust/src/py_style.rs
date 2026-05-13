use std::fmt;

use plotive::style;
use plotive::{Rgb8, Rgba8, color};

use pyo3::prelude::*;
use pyo3::types::PyList;

use super::getattr_not_none;

pub fn extract_color(py_col: &Bound<'_, PyAny>) -> PyResult<Rgba8> {
    if let Ok(col) = py_col.extract::<&str>() {
        Ok(col.parse().map_err(|e| {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Failed to parse color string '{}': {}",
                col, e
            ))
        })?)
    } else if let Ok((r, g, b, a)) = py_col.extract::<(f32, f32, f32, f32)>() {
        let rgb = color::SRgb::new(r, g, b).ok_or_else(|| {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Invalid color specification: {py_col}"
            ))
        })?;
        if a < 0.0 || a > 1.0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "Alpha value must be between 0.0 and 1.0.",
            ));
        }
        let rgb: Rgb8 = rgb.into();
        Ok(rgb.with_a((a / 255.0).round() as u8))
    } else if let Ok((r, g, b)) = py_col.extract::<(f32, f32, f32)>() {
        let rgb = color::SRgb::new(r, g, b).ok_or_else(|| {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Invalid color specification: {py_col}"
            ))
        })?;
        let rgb: Rgb8 = rgb.into();
        Ok(rgb.opaque())
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(format!(
            "Color must be a string (got {py_col:?})"
        )))
    }
}

pub fn extract_series_color(py_col: &Bound<'_, PyAny>) -> PyResult<style::series::Color> {
    if let Ok(col) = py_col.extract::<&str>() {
        if col == "auto" {
            return Ok(style::series::Color::Auto);
        }
        let colb = col.as_bytes();
        if colb.len() > 1 && colb[0] == b'C' && colb[1].is_ascii_digit() {
            let index_str = std::str::from_utf8(&colb[1..]).unwrap();
            let index = index_str.parse::<usize>().map_err(|e| {
                pyo3::exceptions::PyValueError::new_err(format!(
                    "Invalid color string '{}': {}",
                    col, e
                ))
            })?;
            return Ok(style::series::Color::Index(style::series::IndexColor(
                index,
            )));
        }
    }
    if let Ok(col) = py_col.extract::<usize>() {
        return Ok(style::series::Color::Index(style::series::IndexColor(col)));
    }
    let color = extract_color(py_col)?;
    Ok(color.into())
}

pub fn extract_theme_color(
    py_col: &Bound<'_, PyAny>,
    auto: style::theme::Color,
) -> PyResult<style::theme::Color> {
    if let Ok(col) = py_col.extract::<&str>() {
        match col {
            "auto" => return Ok(auto),
            "background" => return Ok(style::theme::Col::Background.into()),
            "foreground" => return Ok(style::theme::Col::Foreground.into()),
            "grid" => return Ok(style::theme::Col::Grid.into()),
            "legend-fill" => return Ok(style::theme::Col::LegendFill.into()),
            "legend-border" => return Ok(style::theme::Col::LegendBorder.into()),
            _ => {}
        }
    }
    let color = extract_color(py_col)?;
    Ok(color.into())
}

fn extract_fill<C: plotive::Color>(
    py_fill: &Bound<'_, PyAny>,
    color: C,
) -> PyResult<style::Fill<C>> {
    let opacity = getattr_not_none(py_fill, "opacity")?
        .map(|o| o.extract::<f32>())
        .transpose()?;

    Ok(style::Fill::Solid { color, opacity })
}

pub fn extract_theme_fill(
    py_fill: &Bound<'_, PyAny>,
    auto: style::theme::Color,
) -> PyResult<style::theme::Fill> {
    let py_color = py_fill.getattr("color")?;
    if py_color.is_none() {
        return Err(pyo3::exceptions::PyValueError::new_err(format!(
            "\"color\" attribute is required for fill.",
        )));
    }
    let color = extract_theme_color(&py_color, auto)?;
    extract_fill(py_fill, color)
}

pub fn extract_series_fill(py_fill: &Bound<'_, PyAny>) -> PyResult<style::series::Fill> {
    let py_color = py_fill.getattr("color")?;
    if py_color.is_none() {
        return Err(pyo3::exceptions::PyValueError::new_err(format!(
            "\"color\" attribute is required for fill.",
        )));
    }
    let color = extract_series_color(&py_color)?;
    extract_fill(py_fill, color)
}

fn extract_stroke_pattern(pattern: &Bound<'_, PyAny>) -> PyResult<style::LinePattern> {
    if let Ok(s) = pattern.extract::<String>() {
        match s.as_str() {
            "solid" => return Ok(style::LinePattern::Solid),
            "dashed" => return Ok(style::Dash::default().into()),
            "dotted" => return Ok(style::LinePattern::Dot),
            _ => {
                return Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "Unknown line pattern string: {}",
                    s
                )));
            }
        }
    }
    let pattern_vec: Vec<f32> = pattern.extract()?;
    Ok(style::Dash(pattern_vec).into())
}

fn extract_stroke<C: plotive::Color>(
    py_stroke: &Bound<'_, PyAny>,
    color: C,
) -> PyResult<style::Stroke<C>> {
    let width = if let Some(w) = getattr_not_none(py_stroke, "width")? {
        w.extract::<f32>()?
    } else {
        1.0
    };
    let pattern = if let Some(p) = getattr_not_none(py_stroke, "pattern")? {
        extract_stroke_pattern(&p)?
    } else {
        style::LinePattern::Solid
    };
    let opacity = if let Some(o) = getattr_not_none(py_stroke, "opacity")? {
        Some(o.extract::<f32>()?)
    } else {
        None
    };
    Ok(style::Stroke {
        color,
        width,
        pattern,
        opacity,
    })
}

pub fn extract_theme_stroke(
    py_stroke: &Bound<'_, PyAny>,
    auto_col: style::theme::Color,
) -> PyResult<style::theme::Stroke> {
    let py_color = py_stroke.getattr("color")?;
    if py_color.is_none() {
        return Err(pyo3::exceptions::PyValueError::new_err(format!(
            "\"color\" attribute is required for stroke.",
        )));
    }
    let color = extract_theme_color(&py_color, auto_col)?;
    extract_stroke(py_stroke, color)
}

pub fn extract_series_stroke(py_stroke: &Bound<'_, PyAny>) -> PyResult<style::series::Stroke> {
    let py_color = py_stroke.getattr("color")?;
    if py_color.is_none() {
        return Err(pyo3::exceptions::PyValueError::new_err(format!(
            "\"color\" attribute is required for stroke.",
        )));
    }
    let color = extract_series_color(&py_color)?;
    extract_stroke(py_stroke, color)
}

pub fn extract_marker<C>(
    py_marker: &Bound<'_, PyAny>,
    fill: Option<style::Fill<C>>,
    stroke: Option<style::Stroke<C>>,
) -> PyResult<style::Marker<C>>
where
    C: plotive::Color + fmt::Debug,
{
    let shape = getattr_not_none(py_marker, "shape")?
        .map(|s| {
            let s_str = s.extract::<&str>()?;
            match s_str {
                "circle" => Ok(style::MarkerShape::Circle),
                "square" => Ok(style::MarkerShape::Square),
                "diamond" => Ok(style::MarkerShape::Diamond),
                "cross" => Ok(style::MarkerShape::Cross),
                "plus" => Ok(style::MarkerShape::Plus),
                "triangle-up" => Ok(style::MarkerShape::TriangleUp),
                "triangle-down" => Ok(style::MarkerShape::TriangleDown),
                "triangle-left" => Ok(style::MarkerShape::TriangleLeft),
                "triangle-right" => Ok(style::MarkerShape::TriangleRight),
                _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
                    "Unknown marker shape: {}",
                    s_str
                ))),
            }
        })
        .transpose()?
        .unwrap_or_default();

    let size = getattr_not_none(py_marker, "size")?
        .map(|s| s.extract::<f32>())
        .transpose()?
        .map(style::MarkerSize)
        .unwrap_or_default();

    Ok(style::Marker {
        shape,
        size,
        fill,
        stroke,
    })
}

pub fn extract_theme_marker(py_marker: &Bound<'_, PyAny>) -> PyResult<style::theme::Marker> {
    let fill = super::getattr_not_none(py_marker, "fill")?
        .map(|py_fill| extract_theme_fill(&py_fill, style::theme::Col::Foreground.into()))
        .transpose()?;
    let stroke = super::getattr_not_none(py_marker, "stroke")?
        .map(|py_stroke| extract_theme_stroke(&py_stroke, style::theme::Col::Foreground.into()))
        .transpose()?;
    extract_marker(py_marker, fill, stroke)
}

pub fn extract_series_marker(py_marker: &Bound<'_, PyAny>) -> PyResult<style::series::Marker> {
    let fill = super::getattr_not_none(py_marker, "fill")?
        .map(|py_fill| extract_series_fill(&py_fill))
        .transpose()?;
    let stroke = super::getattr_not_none(py_marker, "stroke")?
        .map(|py_stroke| extract_series_stroke(&py_stroke))
        .transpose()?;
    extract_marker(py_marker, fill, stroke)
}

pub fn extract_style(py_style: &Bound<'_, PyAny>) -> PyResult<plotive::Style> {
    if let Ok(py_str) = py_style.extract::<&str>() {
        return match py_str {
            "black_white" | "monochrome" | "black" | "bw" => Ok(plotive::Style::black_white()),
            "light" => Ok(plotive::Style::light()),
            "dark" => Ok(plotive::Style::dark()),
            "okabe_ito" | "okabe" => Ok(plotive::Style::okabe_ito()),
            "tol_bright" | "tol" => Ok(plotive::Style::tol_bright()),
            "mocha" | "catppuccin-mocha" => Ok(plotive::Style::catppuccin_mocha()),
            "macchiato" | "catppuccin-macchiato" => Ok(plotive::Style::catppuccin_macchiato()),
            "frappe" | "catppuccin-frappe" => Ok(plotive::Style::catppuccin_frappe()),
            "latte" | "catppuccin-latte" => Ok(plotive::Style::catppuccin_latte()),
            _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
                "Unknown name for plotive's style: {}",
                py_str
            ))),
        };
    }
    let Some(theme) = getattr_not_none(py_style, "theme")? else {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "Style object must have a theme attribute",
        ));
    };
    let Some(palette) = getattr_not_none(py_style, "palette")? else {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "Style object must have a palette attribute",
        ));
    };
    let theme = extract_theme(&theme)?;
    let palette = extract_palette(&palette)?;
    Ok(plotive::Style::new(theme, palette))
}

fn extract_theme(py_theme: &Bound<'_, PyAny>) -> PyResult<style::theme::Theme> {
    if let Ok(py_str) = py_theme.extract::<&str>() {
        return match py_str {
            "light" => Ok(style::theme::Theme::Light),
            "dark" => Ok(style::theme::Theme::Dark),
            "mocha" | "catppuccin-mocha" => Ok(style::theme::Theme::CatppuccinMocha),
            "macchiato" | "catppuccin-macchiato" => Ok(style::theme::Theme::CatppuccinMacchiato),
            "frappe" | "catppuccin-frappe" => Ok(style::theme::Theme::CatppuccinFrappe),
            "latte" | "catppuccin-latte" => Ok(style::theme::Theme::CatppuccinLatte),
            _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
                "Unknown theme name: {}",
                py_str
            ))),
        };
    }

    let get_color_attr = |attr: &str| -> PyResult<Rgba8> {
        if let Some(py_str) = getattr_not_none(py_theme, attr)? {
            Ok(extract_color(&py_str)?)
        } else {
            Err(pyo3::exceptions::PyValueError::new_err(format!(
                "Theme object must have a '{}' color",
                attr
            )))
        }
    };

    let background = get_color_attr("background")?;
    let foreground = get_color_attr("foreground")?;
    let grid = get_color_attr("grid")?;
    let legend_fill = get_color_attr("legend-fill")?;
    let legend_border = get_color_attr("legend-border")?;

    Ok(style::theme::Theme::Custom(style::theme::ThemePalette {
        background,
        foreground,
        grid,
        legend_fill,
        legend_border,
    }))
}

fn extract_palette(py_palette: &Bound<'_, PyAny>) -> PyResult<style::series::Palette> {
    if let Ok(py_str) = py_palette.extract::<&str>() {
        return match py_str {
            "black" => Ok(style::series::Palette::Black),
            "standard" | "default" => Ok(style::series::Palette::Standard),
            "pastel" => Ok(style::series::Palette::Pastel),
            "tol_bright" | "tol" => Ok(style::series::Palette::TolBright),
            "okabe_ito" | "okabe" => Ok(style::series::Palette::OkabeIto),
            "mocha" | "catppuccin-mocha" => Ok(style::series::Palette::CatppuccinMocha),
            "macchiato" | "catppuccin-macchiato" => Ok(style::series::Palette::CatppuccinMacchiato),
            "frappe" | "catppuccin-frappe" => Ok(style::series::Palette::CatppuccinFrappe),
            "latte" | "catppuccin-latte" => Ok(style::series::Palette::CatppuccinLatte),
            _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
                "Unknown palette name: {}",
                py_str
            ))),
        };
    }
    if let Ok(py_list) = py_palette.cast::<PyList>() {
        let mut colors = Vec::with_capacity(py_list.len());
        for item in py_list.iter() {
            let color = extract_color(&item)?;
            colors.push(color);
        }
        return Ok(style::series::Palette::Custom(colors));
    }
    Err(pyo3::exceptions::PyTypeError::new_err(
        "Palette must be a string or a list of colors.",
    ))
}
