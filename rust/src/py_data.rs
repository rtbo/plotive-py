use std::sync::Arc;

use numpy::PyArrayMethods;
use plotive::data;
use pyo3::{prelude::*, types::PyDict};

pub fn extract_data_source<'py>(obj: &Bound<'py, PyAny>) -> PyResult<Arc<dyn data::Source + 'py>> {
    if obj.is_none() {
        Ok(Arc::new(()))
    } else if obj.is_instance_of::<pyo3::types::PyDict>() {
        let dict = obj.cast::<PyDict>()?;
        let ds = extract_dict_data_source(dict.clone())?;
        Ok(Arc::new(ds))
    } else if is_pandas_dataframe(obj)? {
        let ds = extract_pandas_data_source(obj.clone())?;
        Ok(Arc::new(ds))
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "Data source could not be extracted.",
        ))
    }
}

fn is_pandas_dataframe(obj: &Bound<'_, PyAny>) -> PyResult<bool> {
    if let Ok(module) = obj.py().import("pandas") {
        let df_class = module.getattr("DataFrame")?;
        Ok(obj.is_instance(&df_class)?)
    } else {
        Ok(false)
    }
}

fn is_numpy_array_f64<'py>(
    obj: &Bound<'py, PyAny>,
) -> Option<numpy::borrow::PyReadonlyArray1<'py, f64>> {
    if let Ok(py_array) = obj.cast::<numpy::PyArray1<f64>>() {
        Some(py_array.readonly())
    } else {
        None
    }
}

fn is_numpy_array_f32<'py>(
    obj: &Bound<'py, PyAny>,
) -> Option<numpy::borrow::PyReadonlyArray1<'py, f32>> {
    if let Ok(py_array) = obj.cast::<numpy::PyArray1<f32>>() {
        Some(py_array.readonly())
    } else {
        None
    }
}

fn is_numpy_array_i64<'py>(
    obj: &Bound<'py, PyAny>,
) -> Option<numpy::borrow::PyReadonlyArray1<'py, i64>> {
    if let Ok(py_array) = obj.cast::<numpy::PyArray1<i64>>() {
        Some(py_array.readonly())
    } else {
        None
    }
}

#[derive(Debug)]
enum NumpyColumn<'py> {
    F64(numpy::borrow::PyReadonlyArray1<'py, f64>),
    F32(numpy::borrow::PyReadonlyArray1<'py, f32>),
    I64(numpy::borrow::PyReadonlyArray1<'py, i64>),
}

struct NumpyF64Iter<'py> {
    array: numpy::borrow::PyReadonlyArray1<'py, f64>,
    index: usize,
}

impl<'py> Iterator for NumpyF64Iter<'py> {
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

struct NumpyF32Iter<'py> {
    array: numpy::borrow::PyReadonlyArray1<'py, f32>,
    index: usize,
}

impl<'py> Iterator for NumpyF32Iter<'py> {
    type Item = Option<f64>;

    fn next(&mut self) -> Option<Self::Item> {
        let array = self.array.as_array();
        if self.index < array.len() {
            let value = array[self.index];
            self.index += 1;
            Some(if value.is_finite() {
                Some(value as f64)
            } else {
                None
            })
        } else {
            None
        }
    }
}

struct NumpyI64toF64Iter<'py> {
    array: numpy::borrow::PyReadonlyArray1<'py, i64>,
    index: usize,
}

impl<'py> Iterator for NumpyI64toF64Iter<'py> {
    type Item = Option<f64>;

    fn next(&mut self) -> Option<Self::Item> {
        let array = self.array.as_array();
        if self.index < array.len() {
            let value = array[self.index] as f64;
            self.index += 1;
            Some(Some(value))
        } else {
            None
        }
    }
}

struct NumpyI64Iter<'py> {
    array: numpy::borrow::PyReadonlyArray1<'py, i64>,
    index: usize,
}

impl<'py> Iterator for NumpyI64Iter<'py> {
    type Item = Option<i64>;

    fn next(&mut self) -> Option<Self::Item> {
        let array = self.array.as_array();
        if self.index < array.len() {
            let value = array[self.index];
            self.index += 1;
            Some(Some(value))
        } else {
            None
        }
    }
}

impl data::Column for NumpyColumn<'_> {
    fn len(&self) -> usize {
        match self {
            NumpyColumn::F64(col) => col.len().unwrap_or(0),
            NumpyColumn::F32(col) => col.len().unwrap_or(0),
            NumpyColumn::I64(col) => col.len().unwrap_or(0),
        }
    }

    fn len_some(&self) -> usize {
        match self {
            NumpyColumn::F64(col) => col.as_array().iter().filter(|v| v.is_finite()).count(),
            NumpyColumn::F32(col) => col.as_array().iter().filter(|v| v.is_finite()).count(),
            NumpyColumn::I64(col) => col.as_array().len(),
        }
    }

    fn f64(&self) -> Option<&dyn data::F64Column> {
        match self {
            NumpyColumn::F64(_) => Some(self),
            NumpyColumn::F32(_) => Some(self),
            NumpyColumn::I64(_) => Some(self),
        }
    }

    fn i64(&self) -> Option<&dyn data::I64Column> {
        match self {
            NumpyColumn::I64(_) => Some(self),
            _ => None,
        }
    }
}

impl data::F64Column for NumpyColumn<'_> {
    fn len(&self) -> usize {
        match self {
            NumpyColumn::F64(col) => col.len().unwrap_or(0),
            NumpyColumn::F32(col) => col.len().unwrap_or(0),
            NumpyColumn::I64(col) => col.len().unwrap_or(0),
        }
    }

    fn f64_iter(&self) -> Box<dyn Iterator<Item = Option<f64>> + '_> {
        match self {
            NumpyColumn::F64(col) => Box::new(NumpyF64Iter {
                array: col.clone(),
                index: 0,
            }),
            NumpyColumn::F32(col) => Box::new(NumpyF32Iter {
                array: col.clone(),
                index: 0,
            }),
            NumpyColumn::I64(col) => Box::new(NumpyI64toF64Iter {
                array: col.clone(),
                index: 0,
            }),
        }
    }
}

impl data::I64Column for NumpyColumn<'_> {
    fn len(&self) -> usize {
        match self {
            NumpyColumn::I64(col) => col.len().unwrap_or(0),
            _ => 0,
        }
    }

    fn i64_iter(&self) -> Box<dyn Iterator<Item = Option<i64>> + '_> {
        match self {
            NumpyColumn::I64(col) => Box::new(NumpyI64Iter {
                array: col.clone(),
                index: 0,
            }),
            _ => Box::new(std::iter::empty()),
        }
    }
}

#[derive(Debug)]
struct NumpyDataSource<'py> {
    names: Vec<String>,
    columns: Vec<NumpyColumn<'py>>,
}

impl<'py> data::Source for NumpyDataSource<'py> {
    fn names(&self) -> Vec<&str> {
        self.names.iter().map(|s| s.as_str()).collect()
    }

    fn column(&self, name: &str) -> Option<&dyn data::Column> {
        let index = self.names.iter().position(|n| n == name)?;
        self.columns.get(index).map(|c| c as &dyn data::Column)
    }
}

fn extract_dict_data_source<'py>(dict: Bound<'py, PyDict>) -> PyResult<NumpyDataSource<'py>> {
    let np = dict.py().import("numpy")?;
    let float64_dtype = np.getattr("float64")?;

    let names: Vec<String> = dict.keys().extract()?;
    let mut columns = Vec::with_capacity(names.len());
    for name in &names {
        let col = dict.get_item(name)?.unwrap();
        if let Some(array) = extract_column(&col) {
            columns.push(array);
            continue;
        }
        if let Some(array) = convert_column(&col, &np, &float64_dtype) {
            columns.push(array);
            continue;
        }
        return Err(pyo3::exceptions::PyTypeError::new_err(format!(
            "Column '{}' could not be converted to a numeric array.",
            name
        )));
    }
    Ok(NumpyDataSource { names, columns })
}

fn extract_pandas_data_source<'py>(df: Bound<'py, PyAny>) -> PyResult<NumpyDataSource<'py>> {
    let np = df.py().import("numpy")?;
    let float64_dtype = np.getattr("float64")?;

    let names: Vec<String> = df.getattr("columns")?.extract()?;
    let mut columns = Vec::with_capacity(names.len());
    for name in &names {
        let col = df.get_item(name)?;
        if let Some(array) = extract_column(&col) {
            columns.push(array);
            continue;
        }
        if let Some(array) = convert_column(&col, &np, &float64_dtype) {
            columns.push(array);
            continue;
        }
        return Err(pyo3::exceptions::PyTypeError::new_err(format!(
            "Column '{}' could not be converted to a numeric array.",
            name
        )));
    }
    Ok(NumpyDataSource { names, columns })
}

fn extract_column<'py>(
    col: &Bound<'py, PyAny>,
) -> Option<NumpyColumn<'py>> {
    if let Some(array) = is_numpy_array_f64(col) {
        Some(NumpyColumn::F64(array))
    } else if let Some(array) = is_numpy_array_f32(col) {
        Some(NumpyColumn::F32(array))
    } else if let Some(array) = is_numpy_array_i64(col) {
        Some(NumpyColumn::I64(array))
    } else {
        None
    }
}

fn convert_column<'py>(
    col: &Bound<'py, PyAny>,
    np: &Bound<'py, PyAny>,
    float64_dtype: &Bound<'py, PyAny>,
) -> Option<NumpyColumn<'py>> {
    if let Ok(data) = col.call_method1("astype", (float64_dtype.clone(),)) {
        if let Ok(values) = data.getattr("values") {
            if let Ok(array) = values.cast::<numpy::PyArray1<f64>>() {
                return Some(NumpyColumn::F64(array.readonly()));
            }
        }
    }
    if let Ok(list) = col.extract::<Vec<f64>>() {
        if let Ok(array) = np.call_method1("array", (list,)) {
            if let Ok(array) = array.cast::<numpy::PyArray1<f64>>() {
                return Some(NumpyColumn::F64(array.readonly()));
            }
        }
    }
    None
}
