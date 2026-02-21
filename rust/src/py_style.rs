use plotive::ColorU8;
use plotive::style;

use pyo3::prelude::*;
use pyo3::types::PyList;

use super::{getattr_not_none, extract_color};

pub fn extract_style(py_style: &Bound<'_, PyAny>) -> PyResult<plotive::Style> {
    if let Ok(py_str) = py_style.extract::<&str>() {
        return match py_str {
            "black_white" | "monochrome" | "black" => Ok(plotive::Style::black_white()),
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

    let get_color_attr = |attr: &str| -> PyResult<ColorU8> {
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
    let legend_fill = get_color_attr("legend_fill")?;
    let legend_border = get_color_attr("legend_border")?;

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

pub fn extract_stroke_pattern(pattern: &Bound<'_, PyAny>) -> PyResult<style::LinePattern> {
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

pub fn extract_series_color(py_col: &Bound<'_, PyAny>) -> PyResult<style::series::Color> {
    if let Ok(col) = py_col.extract::<&str>() {
        if col == "auto" {
            return Ok(style::series::Color::Auto);
        }
    }
    let color = super::extract_color(py_col)?;
    Ok(color.into())
}

pub fn extract_theme_color(py_col: &Bound<'_, PyAny>) -> PyResult<style::theme::Color> {
    if let Ok(col) = py_col.extract::<&str>() {
        match col {
            "background" => return Ok(style::theme::Col::Background.into()),
            "foreground" => return Ok(style::theme::Col::Foreground.into()),
            "grid" => return Ok(style::theme::Col::Grid.into()),
            "legend-fill" => return Ok(style::theme::Col::LegendFill.into()),
            "legend-border" => return Ok(style::theme::Col::LegendBorder.into()),
            _ => {}
        }
    }
    let color = super::extract_color(py_col)?;
    Ok(color.into())
}

pub fn extract_theme_stroke(py_stroke: &Bound<'_, PyAny>) -> PyResult<style::theme::Stroke> {
    let py_color = py_stroke.getattr("color")?;
    if py_color.is_none() {
        return Err(pyo3::exceptions::PyValueError::new_err(format!(
            "\"color\" attribute is required for stroke.",
        )));
    }
    let color = extract_theme_color(&py_color)?;
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
    Ok(style::theme::Stroke {
        color,
        width,
        pattern,
        opacity,
    })
}