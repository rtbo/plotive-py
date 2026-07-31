use plotive::{Rgb8, Rgba8, color, style};
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

pub fn extract_style(py_style: &Bound<'_, PyAny>) -> PyResult<plotive::Style> {
    if let Ok(py_str) = py_style.extract::<&str>() {
        return match py_str {
            "black_white" | "monochrome" | "black" | "bw" => Ok(plotive::Style::black_white()),
            "light" | "standard" => Ok(plotive::Style::light()),
            "dark" => Ok(plotive::Style::dark()),
            "okabe_ito" | "okabe" => Ok(plotive::Style::okabe_ito()),
            "tol_bright" | "tol" => Ok(plotive::Style::tol_bright()),
            "mocha" | "catppuccin-mocha" => Ok(plotive::Style::catppuccin_mocha()),
            "macchiato" | "catppuccin-macchiato" => Ok(plotive::Style::catppuccin_macchiato()),
            "frappe" | "catppuccin-frappe" => Ok(plotive::Style::catppuccin_frappe()),
            "latte" | "catppuccin-latte" => Ok(plotive::Style::catppuccin_latte()),
            "dracula" => Ok(plotive::Style::dracula()),
            "alucard" => Ok(plotive::Style::alucard()),
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
