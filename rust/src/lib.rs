use pyo3::prelude::*;
use pythonize::depythonize;

mod py_data;
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

fn extract_figure(obj: &Bound<'_, PyAny>) -> PyResult<plotive::des::Figure> {
    let fig: plotive::des::Figure = depythonize(obj)?;
    Ok(fig)
}

#[derive(Debug, Default)]
struct Params {
    style: Option<plotive::Style>,
    fontdb: Option<plotive::text::fontdb::Database>,
}

fn extract_fontdb(py_fonts: &Bound<'_, PyAny>) -> PyResult<plotive::text::fontdb::Database> {
    let mut fontdb = plotive::text::bundled_font_db();

    let fonts: Vec<Vec<u8>> = if let Ok(py_list) = py_fonts.cast::<pyo3::types::PyList>() {
        py_list
            .iter()
            .map(|item| item.extract::<Vec<u8>>())
            .collect::<Result<Vec<_>, _>>()?
    } else if let Ok(py_bytes) = py_fonts.extract::<&[u8]>() {
        vec![py_bytes.to_vec()]
    } else {
        return Err(pyo3::exceptions::PyTypeError::new_err(
            "params.fontdb must be a list of bytes or a single bytes object",
        ));
    };

    for bytes in fonts.into_iter() {
        use woff2_patched::decode::{convert_woff2_to_ttf, is_woff2};

        let bytes = if is_woff2(&bytes) {
            let mut bytes = bytes.as_slice();
            convert_woff2_to_ttf(&mut bytes).map_err(|err| {
                pyo3::exceptions::PyRuntimeError::new_err(format!(
                    "Error while converting WOFF font file: {}",
                    err
                ))
            })?
        } else {
            bytes
        };

        fontdb.load_font_data(bytes);
    }

    Ok(fontdb)
}
fn extract_params(py_params: &Bound<'_, PyAny>) -> PyResult<Params> {
    if py_params.is_none() {
        return Ok(Params::default());
    }

    // get class plotive.Params and check if py_params is an instance of it
    let pv_params_class = py_params.py().import("plotive")?.getattr("Params")?;
    if py_params.is_instance(&pv_params_class)? {
        // extract style attribute
        let style = getattr_not_none(py_params, "style")?
            .map(|py_style| py_style::extract_style(&py_style))
            .transpose()?;

        let fontdb = getattr_not_none(py_params, "fonts")?
            .map(|py_fontdb| extract_fontdb(&py_fontdb))
            .transpose()?;

        Ok(Params { style, fontdb })
    } else {
        py_style::extract_style(py_params)
            .map(|style| Params {
                style: Some(style),
                fontdb: None,
            })
            .map_err(|_| {
                pyo3::exceptions::PyTypeError::new_err(
                    "Expected an instance of plotive.Params or a style object",
                )
            })
    }
}

#[pymodule]
#[pyo3(name = "_rs")]
mod plt_rs {

    use std::sync::Arc;

    use plotive_pxl::PxlRender;
    use pyo3::prelude::*;

    use super::{py_data, py_style};

    #[pyfunction]
    fn parse_color(py_col: &Bound<'_, PyAny>) -> PyResult<(f32, f32, f32, f32)> {
        let col = py_style::extract_color(py_col)?;
        Ok((
            col.r() as f32 / 255.0,
            col.g() as f32 / 255.0,
            col.b() as f32 / 255.0,
            col.a() as f32 / 255.0,
        ))
    }

    #[pyfunction]
    fn render_pxl(
        py_fig: &Bound<'_, PyAny>,
        py_data_src: &Bound<'_, PyAny>,
        py_params: &Bound<'_, PyAny>,
    ) -> PyResult<(Vec<u8>, u32, u32)> {
        let fig = super::extract_figure(py_fig)?;
        let data_src = py_data::extract_data_source(py_data_src)?;

        let params = if !py_params.is_none() {
            super::extract_params(py_params)?
        } else {
            super::Params::default()
        };
        let params = plotive_pxl::Params {
            style: params.style.unwrap_or_default(),
            fontdb: params.fontdb.as_ref(),
            ..Default::default()
        };

        let pixmap = fig.to_pixmap(&*data_src, params).map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to render figure: {}", e))
        })?;

        let width = pixmap.width();
        let height = pixmap.height();
        let bytes = pixmap.take();

        Ok((bytes, width, height))
    }

    #[pyfunction]
    fn save_png(
        py_fig: &Bound<'_, PyAny>,
        path: &str,
        py_data_src: &Bound<'_, PyAny>,
        py_params: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        use plotive_pxl::PxlRender;

        let fig = super::extract_figure(py_fig)?;
        let data_src = py_data::extract_data_source(py_data_src)?;

        let params = if !py_params.is_none() {
            super::extract_params(py_params)?
        } else {
            super::Params::default()
        };
        let params = plotive_pxl::Params {
            style: params.style.unwrap_or_default(),
            fontdb: params.fontdb.as_ref(),
            ..Default::default()
        };

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
        py_params: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        use plotive_svg::SaveSvg;

        let fig = super::extract_figure(py_fig)?;
        let data_src = py_data::extract_data_source(py_data_src)?;

        let params = if !py_params.is_none() {
            super::extract_params(py_params)?
        } else {
            super::Params::default()
        };
        let params = plotive_svg::Params {
            style: params.style.unwrap_or_default(),
            fontdb: params.fontdb.as_ref(),
            ..Default::default()
        };

        fig.save_svg(path, &*data_src, params).map_err(|e| {
            pyo3::exceptions::PyIOError::new_err(format!("Failed to save SVG: {}", e))
        })?;

        Ok(())
    }

    #[pyfunction]
    fn show(
        py_fig: &Bound<'_, PyAny>,
        py_data_src: &Bound<'_, PyAny>,
        py_params: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        use plotive_iced::Show;

        let fig = super::extract_figure(py_fig)?;
        // show requires 'static lifetime, so we need to copy the data source
        let data_src = py_data::extract_data_source(py_data_src)?.copy();

        let params = if !py_params.is_none() {
            super::extract_params(py_params)?
        } else {
            super::Params::default()
        };
        let params = plotive_iced::show::Params {
            style: params.style,
            fontdb: params.fontdb.map(Arc::new),
            ..Default::default()
        };

        fig.show(data_src, params).map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to show figure: {}", e))
        })?;

        Ok(())
    }

    #[pyfunction]
    fn to_json(py_fig: &Bound<'_, PyAny>) -> PyResult<String> {
        let fig = super::extract_figure(py_fig)?;
        let json = serde_json::to_string_pretty(&fig).map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!(
                "Failed to convert figure to JSON: {}",
                e
            ))
        })?;
        Ok(json)
    }
}
