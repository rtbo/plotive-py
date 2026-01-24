use plotive::ColorU8;
use pyo3::prelude::*;

mod py_data;
mod py_des;
mod py_style;

fn getattr_not_none<'py>(
    obj: &Bound<'py, PyAny>,
    attr: &str,
) -> PyResult<Option<Bound<'py, PyAny>>> {
    let py_attr = obj.getattr_opt(attr)?;
    let Some(py_attr) = py_attr else {
        return Ok(None);
    };
    if py_attr.is_none() {
        Ok(None)
    } else {
        Ok(Some(py_attr))
    }
}

fn extract_class_name(obj: &Bound<'_, PyAny>) -> PyResult<String> {
    let class = obj.getattr("__class__")?;
    let name = class.getattr("__name__")?.str()?;
    Ok(name.to_str()?.to_owned())
}

fn extract_color(py_col: &Bound<'_, PyAny>) -> PyResult<ColorU8> {
    if let Ok(col) = py_col.extract::<&str>() {
        Ok(col.parse().map_err(|e| {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Failed to parse color string '{}': {}",
                col, e
            ))
        })?)
    } else if let Ok((r, g, b)) = py_col.extract::<(u8, u8, u8)>() {
        Ok(ColorU8::from_rgb(r, g, b))
    } else if let Ok((r, g, b, a)) = py_col.extract::<(u8, u8, u8, u8)>() {
        Ok(ColorU8::from_rgba(r, g, b, a))
    } else if let Ok((r, g, b, a)) = py_col.extract::<(u8, u8, u8, f32)>() {
        if a < 0.0 || a > 1.0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "Alpha value must be between 0.0 and 1.0.",
            ));
        }
        Ok(ColorU8::from_rgba(r, g, b, (a * 255.0) as u8))
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "Color must be a string.",
        ))
    }
}

#[pymodule]
#[pyo3(name = "_rs")]
mod plt_rs {
    use pyo3::prelude::*;

    use super::py_data;
    use super::py_des;
    use super::py_style;

    #[pyfunction]
    fn save_png(
        py_fig: &Bound<'_, PyAny>,
        path: &str,
        py_data_src: &Bound<'_, PyAny>,
        py_style: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        use plotive_pxl::SavePng;

        let fig = py_des::extract_figure(py_fig)?;
        let data_src = py_data::extract_data_source(py_data_src)?;
        let mut params: plotive_pxl::Params = Default::default();
        if !py_style.is_none() {
            let style = py_style::extract_style(py_style)?;
            params.style = style;
        }
        fig.save_png(path, &*data_src, params).map_err(|e| {
            pyo3::exceptions::PyIOError::new_err(format!("Failed to save PNG: {}", e))
        })?;

        Ok(())
    }

    #[pyfunction]
    fn save_svg(
        py_fig: &Bound<'_, PyAny>,
        path: &str,
        py_data_src: &Bound<'_, PyAny>,
        py_style: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        use plotive_svg::SaveSvg;

        let fig = py_des::extract_figure(py_fig)?;
        let data_src = py_data::extract_data_source(py_data_src)?;
        let mut params: plotive_svg::Params = Default::default();
        if !py_style.is_none() {
            let style = py_style::extract_style(py_style)?;
            params.style = style;
        }
        fig.save_svg(path, &*data_src, params).map_err(|e| {
            pyo3::exceptions::PyIOError::new_err(format!("Failed to save SVG: {}", e))
        })?;

        Ok(())
    }

    #[pyfunction]
    fn show(
        py_fig: &Bound<'_, PyAny>,
        py_data_src: &Bound<'_, PyAny>,
        py_style: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        use plotive_iced::Show;

        let fig = py_des::extract_figure(py_fig)?;
        // show requires 'static lifetime, so we need to copy the data source
        let data_src = py_data::extract_data_source(py_data_src)?.copy();
        let mut params: plotive_iced::show::Params = Default::default();
        if !py_style.is_none() {
            let style = py_style::extract_style(py_style)?;
            params.style = Some(style);
        }
        fig.show(data_src, params).map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to show figure: {}", e))
        })?;

        Ok(())
    }
}
