use std::sync::Arc;

use numpy::PyArrayMethods;
use plotive::data;
use plotive::time::DateTime;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};

pub fn extract_data_source<'py>(obj: &Bound<'py, PyAny>) -> PyResult<Arc<dyn data::Source + 'py>> {
    if obj.is_none() {
        Ok(Arc::new(()))
    } else if obj.is_instance_of::<pyo3::types::PyDict>() {
        let dict = obj.cast::<PyDict>()?;
        let ds = extract_dict_data_source(dict.clone())?;
        Ok(Arc::new(ds))
    } else if obj.is_instance_of::<PyList>() {
        let list = obj.cast::<PyList>()?;
        let ds = extract_list_data_source(list.clone())?;
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
    Time(Vec<Option<DateTime>>),
    Str(Vec<Option<String>>),
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

struct NumpyTimeIter<'a> {
    data: &'a [Option<DateTime>],
    index: usize,
}

impl Iterator for NumpyTimeIter<'_> {
    type Item = Option<DateTime>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.index < self.data.len() {
            let value = self.data[self.index];
            self.index += 1;
            Some(value)
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
            NumpyColumn::Time(col) => col.len(),
            NumpyColumn::Str(col) => col.len(),
        }
    }

    fn len_some(&self) -> usize {
        match self {
            NumpyColumn::F64(col) => col.as_array().iter().filter(|v| v.is_finite()).count(),
            NumpyColumn::F32(col) => col.as_array().iter().filter(|v| v.is_finite()).count(),
            NumpyColumn::I64(col) => col.as_array().len(),
            NumpyColumn::Time(col) => col.iter().filter(|v| v.is_some()).count(),
            NumpyColumn::Str(col) => col.iter().filter(|v| v.is_some()).count(),
        }
    }

    fn f64(&self) -> Option<&dyn data::F64Column> {
        match self {
            NumpyColumn::F64(_) => Some(self),
            NumpyColumn::F32(_) => Some(self),
            NumpyColumn::I64(_) => Some(self),
            NumpyColumn::Time(_) => Some(self),
            NumpyColumn::Str(_) => None,
        }
    }

    fn i64(&self) -> Option<&dyn data::I64Column> {
        match self {
            NumpyColumn::I64(_) => Some(self),
            _ => None,
        }
    }

    fn str(&self) -> Option<&dyn data::StrColumn> {
        match self {
            NumpyColumn::Str(_) => Some(self),
            _ => None,
        }
    }

    fn time(&self) -> Option<&dyn data::TimeColumn> {
        match self {
            NumpyColumn::Time(_) => Some(self),
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
            NumpyColumn::Time(col) => col.len(),
            NumpyColumn::Str(_) => 0,
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
            NumpyColumn::Time(col) => {
                Box::new(col.iter().copied().map(|v| v.map(|dt| dt.timestamp())))
            }
            _ => Box::new(std::iter::empty()),
        }
    }
}

impl data::TimeColumn for NumpyColumn<'_> {
    fn len(&self) -> usize {
        match self {
            NumpyColumn::Time(col) => col.len(),
            _ => 0,
        }
    }

    fn time_iter(&self) -> Box<dyn Iterator<Item = Option<DateTime>> + '_> {
        match self {
            NumpyColumn::Time(col) => Box::new(NumpyTimeIter {
                data: col.as_slice(),
                index: 0,
            }),
            _ => Box::new(std::iter::empty()),
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

impl data::StrColumn for NumpyColumn<'_> {
    fn len(&self) -> usize {
        match self {
            NumpyColumn::Str(col) => col.len(),
            _ => 0,
        }
    }

    fn str_iter(&self) -> Box<dyn Iterator<Item = Option<&str>> + '_> {
        match self {
            NumpyColumn::Str(col) => Box::new(col.iter().map(|s| s.as_deref())),
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
            "Column '{}' could not be converted to a supported array/list type (numeric or string).",
            name
        )));
    }
    Ok(NumpyDataSource { names, columns })
}

fn extract_list_data_source<'py>(list: Bound<'py, PyList>) -> PyResult<NumpyDataSource<'py>> {
    let np = list.py().import("numpy")?;
    let float64_dtype = np.getattr("float64")?;
    let col = list.as_any();

    if let Some(array) = extract_column(col) {
        return Ok(NumpyDataSource {
            names: vec!["value".to_string()],
            columns: vec![array],
        });
    }
    if let Some(array) = convert_column(col, &np, &float64_dtype) {
        return Ok(NumpyDataSource {
            names: vec!["value".to_string()],
            columns: vec![array],
        });
    }

    Err(pyo3::exceptions::PyTypeError::new_err(
        "List data source could not be converted to a supported array/list type (numeric or string).",
    ))
}

fn extract_pandas_data_source<'py>(df: Bound<'py, PyAny>) -> PyResult<NumpyDataSource<'py>> {
    let pd = df.py().import("pandas")?;
    let np = df.py().import("numpy")?;
    let float64_dtype = np.getattr("float64")?;

    let mut names: Vec<String> = Vec::new();
    let mut columns: Vec<NumpyColumn<'py>> = Vec::new();

    // Include named index as a regular column (e.g. Date index).
    let index = df.getattr("index")?;
    let index_name: Option<String> = index.getattr("name")?.extract()?;
    if let Some(index_name) = index_name.filter(|s| !s.is_empty()) {
        let mut has_conflict = false;
        for col_name in df.getattr("columns")?.try_iter()? {
            let col_name = col_name?.extract::<String>()?;
            if col_name == index_name {
                has_conflict = true;
                break;
            }
        }
        if !has_conflict {
            if let Some(array) = extract_supported_pandas_column(&index, &pd, &np, &float64_dtype)? {
                names.push(index_name);
                columns.push(array);
            } else {
                return Err(pyo3::exceptions::PyTypeError::new_err(
                    "Pandas index could not be converted to a supported data column.",
                ));
            }
        }
    }

    for name in df.getattr("columns")?.try_iter()? {
        let name = name?.extract::<String>()?;
        let col = df.get_item(&name)?;
        if let Some(array) = extract_supported_pandas_column(&col, &pd, &np, &float64_dtype)? {
            names.push(name);
            columns.push(array);
            continue;
        }
        return Err(pyo3::exceptions::PyTypeError::new_err(format!(
            "Column '{}' could not be converted to a supported data column.",
            name
        )));
    }
    Ok(NumpyDataSource { names, columns })
}

fn extract_supported_pandas_column<'py>(
    col: &Bound<'py, PyAny>,
    pd: &Bound<'py, PyAny>,
    np: &Bound<'py, PyAny>,
    float64_dtype: &Bound<'py, PyAny>,
) -> PyResult<Option<NumpyColumn<'py>>> {
    if let Some(array) = extract_column(col) {
        return Ok(Some(array));
    }
    if let Some(array) = convert_pandas_time_column(col, pd)? {
        return Ok(Some(array));
    }
    if let Some(array) = convert_column(col, np, float64_dtype) {
        return Ok(Some(array));
    }
    Ok(None)
}

fn convert_pandas_time_column<'py>(
    col: &Bound<'py, PyAny>,
    pd: &Bound<'py, PyAny>,
) -> PyResult<Option<NumpyColumn<'py>>> {
    let api_types = pd.getattr("api")?.getattr("types")?;
    let dtype = col.getattr("dtype")?;

    let is_numeric_dtype = api_types
        .call_method1("is_numeric_dtype", (dtype.clone(),))?
        .is_truthy()?;
    if is_numeric_dtype {
        return Ok(None);
    }

    let to_datetime = pd.getattr("to_datetime")?;
    let kwargs = PyDict::new(col.py());
    kwargs.set_item("errors", "coerce")?;
    kwargs.set_item("utc", true)?;
    let converted = to_datetime.call((col,), Some(&kwargs))?;

    let source_not_null = col
        .call_method0("notna")?
        .call_method0("sum")?
        .extract::<usize>()?;
    let parsed_not_null = converted
        .call_method0("notna")?
        .call_method0("sum")?
        .extract::<usize>()?;

    if source_not_null > 0 && parsed_not_null == 0 {
        return Ok(None);
    }

    // Normalize to microseconds explicitly for cross-platform consistency
    // before converting datetime values to integer epoch units.
    let kwargs = PyDict::new(col.py());
    kwargs.set_item("dtype", "datetime64[us]")?;
    let us_array = converted.call_method("to_numpy", (), Some(&kwargs))?;
    let us_values = us_array.call_method1("astype", ("int64",))?;
    let values = if let Ok(array) = us_values.cast::<numpy::PyArray1<i64>>() {
        array.readonly().as_array().to_vec()
    } else {
        us_values.extract::<Vec<i64>>()?
    };

    const NAT_I64: i64 = i64::MIN;
    let mut out = Vec::with_capacity(values.len());
    for value_us in values {
        if value_us == NAT_I64 {
            out.push(None);
            continue;
        }
        let ts = value_us as f64 / 1_000_000.0;
        out.push(DateTime::from_timestamp(ts));
    }

    Ok(Some(NumpyColumn::Time(out)))
}

fn extract_column<'py>(col: &Bound<'py, PyAny>) -> Option<NumpyColumn<'py>> {
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
    if let Ok(list) = col.extract::<Vec<Option<String>>>() {
        return Some(NumpyColumn::Str(list));
    }
    if let Ok(list) = col.extract::<Vec<String>>() {
        return Some(NumpyColumn::Str(list.into_iter().map(Some).collect()));
    }
    if let Ok(list_obj) = col.call_method0("tolist") {
        if let Ok(list) = list_obj.extract::<Vec<Option<String>>>() {
            return Some(NumpyColumn::Str(list));
        }
        if let Ok(list) = list_obj.extract::<Vec<String>>() {
            return Some(NumpyColumn::Str(list.into_iter().map(Some).collect()));
        }
    }

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
