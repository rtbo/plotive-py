use plotive::geom;
use pyo3::prelude::*;

pub fn extract_padding(py_padding: &Bound<'_, PyAny>) -> PyResult<geom::Padding> {
    if let Ok(pad) = py_padding.extract::<f32>() {
        Ok(geom::Padding::Even(pad))
    } else if let Ok((hor, ver)) = py_padding.extract::<(f32, f32)>() {
        Ok(geom::Padding::Center { ver, hor })
    } else if let Ok((top, right, bottom, left)) = py_padding.extract::<(f32, f32, f32, f32)>() {
        Ok(geom::Padding::Custom {
            top,
            right,
            bottom,
            left,
        })
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "Padding must be a float, a tuple of two floats, or a tuple of four floats.",
        ))
    }
}
