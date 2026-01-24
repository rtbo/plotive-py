use std::sync::Arc;

use numpy::PyArrayMethods;
use plotive::data;
use pyo3::prelude::*;

mod py_des;

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

fn is_pandas_dataframe(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    let module = obj.py().import("pandas")?;
    let df_class = module.getattr("DataFrame")?;
    Ok(obj.is_instance(&df_class)?)
}

#[derive(Debug)]
enum PandasColumn<'py> {
    F64(numpy::borrow::PyReadonlyArray1<'py, f64>),
}

struct PandasF64Iter<'py> {
    array: numpy::borrow::PyReadonlyArray1<'py, f64>,
    index: usize,
}

impl<'py> Iterator for PandasF64Iter<'py> {
    type Item = Option<f64>;

    fn next(&mut self) -> Option<Self::Item> {
        let array = self.array.as_array();
        if self.index < array.len() {
            let value = array[self.index];
            self.index += 1;
            Some(if value.is_finite() { Some(value) } else { None })
        } else {
            None
        }
    }
}

impl data::Column for PandasColumn<'_> {
    fn len(&self) -> usize {
        match self {
            PandasColumn::F64(col) => col.len().unwrap_or(0),
        }
    }

    fn len_some(&self) -> usize {
        match self {
            PandasColumn::F64(col) => col.as_array().iter().filter(|v| v.is_finite()).count(),
        }
    }

    fn f64(&self) -> Option<&dyn data::F64Column> {
        match self {
            PandasColumn::F64(_) => Some(self),
        }
    }
}

impl data::F64Column for PandasColumn<'_> {
    fn len(&self) -> usize {
        match self {
            PandasColumn::F64(col) => col.len().unwrap_or(0),
        }
    }

    fn f64_iter(&self) -> Box<dyn Iterator<Item = Option<f64>> + '_> {
        match self {
            PandasColumn::F64(col) => Box::new(PandasF64Iter {
                array: col.clone(),
                index: 0,
            }),
        }
    }
}

#[derive(Debug)]
struct PandasDataSource<'py> {
    names: Vec<String>,
    columns: Vec<PandasColumn<'py>>,
}

impl<'py> PandasDataSource<'py> {
    fn new(df: Bound<'py, PyAny>) -> PyResult<Self> {
        let np = df.py().import("numpy")?;
        let float64_dtype = np.getattr("float64")?;

        let names: Vec<String> = df.getattr("columns")?.extract()?;
        let mut columns = Vec::with_capacity(names.len());
        for name in &names {
            let col = df.get_item(name)?;
            // Convert to float64 explicitly using astype
            let data = col.call_method1("astype", (float64_dtype.clone(),))?;
            let values = data.getattr("values")?;
            let array = values.cast::<numpy::PyArray1<f64>>()?;
            columns.push(PandasColumn::F64(array.readonly()));
        }
        Ok(Self { names, columns })
    }
}

impl<'py> data::Source for PandasDataSource<'py> {
    fn names(&self) -> Vec<&str> {
        self.names.iter().map(|s| s.as_str()).collect()
    }

    fn column(&self, name: &str) -> Option<&dyn data::Column> {
        let index = self.names.iter().position(|n| n == name)?;
        self.columns.get(index).map(|c| c as &dyn data::Column)
    }
}

fn extract_data_source<'py>(obj: &Bound<'py, PyAny>) -> PyResult<Arc<dyn data::Source + 'py>> {
    if obj.is_none() {
        Ok(Arc::new(()))
    } else if is_pandas_dataframe(obj)? {
        let ds = PandasDataSource::new(obj.clone())?;
        Ok(Arc::new(ds))
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "Data source must be a pandas DataFrame.",
        ))
    }
}

#[pymodule]
#[pyo3(name = "_rs")]
mod plt_rs {
    use pyo3::prelude::*;

    use super::py_des;

    #[pyfunction]
    fn save_png(
        py_fig: &Bound<'_, PyAny>,
        path: &str,
        py_data_src: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        use plotive_pxl::SavePng;

        let fig = py_des::extract_figure(py_fig)?;
        let data_src = super::extract_data_source(py_data_src)?;
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
        let data_src = super::extract_data_source(py_data_src)?;
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
        let data_src = super::extract_data_source(py_data_src)?.copy();
        fig.show(data_src, Default::default()).map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to show figure: {}", e))
        })?;

        Ok(())
    }
}
