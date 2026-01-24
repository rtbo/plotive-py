use pyo3::prelude::*;

mod py_des;
mod py_data;

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

#[pymodule]
#[pyo3(name = "_rs")]
mod plt_rs {
    use pyo3::prelude::*;

    use super::py_des;
    use super::py_data;

    #[pyfunction]
    fn save_png(
        py_fig: &Bound<'_, PyAny>,
        path: &str,
        py_data_src: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        use plotive_pxl::SavePng;

        let fig = py_des::extract_figure(py_fig)?;
        let data_src = py_data::extract_data_source(py_data_src)?;
        fig.save_png(path, &*data_src, Default::default())
            .map_err(|e| {
                pyo3::exceptions::PyIOError::new_err(format!("Failed to save PNG: {}", e))
            })?;

        Ok(())
    }

    #[pyfunction]
    fn save_svg(
        py_fig: &Bound<'_, PyAny>,
        path: &str,
        py_data_src: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        use plotive_svg::SaveSvg;

        let fig = py_des::extract_figure(py_fig)?;
        let data_src = py_data::extract_data_source(py_data_src)?;
        fig.save_svg(path, &*data_src, Default::default())
            .map_err(|e| {
                pyo3::exceptions::PyIOError::new_err(format!("Failed to save SVG: {}", e))
            })?;

        Ok(())
    }

    #[pyfunction]
    fn show(py_fig: &Bound<'_, PyAny>, py_data_src: &Bound<'_, PyAny>) -> PyResult<()> {
        use plotive_iced::Show;

        let fig = py_des::extract_figure(py_fig)?;
        // show requires 'static lifetime, so we need to copy the data source
        let data_src = py_data::extract_data_source(py_data_src)?.copy();
        fig.show(data_src, Default::default()).map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to show figure: {}", e))
        })?;

        Ok(())
    }
}
