# Determinism audit: ffi.rs

- Targets: 26
- R0 results: `{'unsat': 25, 'unknown': 1}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `CStr::count_bytes` | ok | unsat | complete |
| `CStr::is_empty` | ok | unsat | complete |
| `CStr::to_bytes` | ok | unsat | complete |
| `CStr::to_bytes_with_nul` | ok | unsat | complete |
| `CStr::from_bytes_with_nul` | ok | unsat | complete |
| `CStr::from_bytes_until_nul` | ok | unsat | complete |
| `CStr::to_str` | ok | unsat | complete |
| `core::str::Utf8Error::valid_up_to` | ok | unsat | complete |
| `core::str::Utf8Error::error_len` | ok | unsat | complete |
| `CString::as_bytes` | ok | unsat | complete |
| `CString::as_bytes_with_nul` | ok | unsat | complete |
| `CString::as_c_str` | ok | unknown | ok_inconclusive |
| `CString::into_bytes` | ok | unsat | complete |
| `CString::into_bytes_with_nul` | ok | unsat | complete |
| `CString::into_boxed_c_str` | ok | unsat | complete |
| `CString::from_vec_with_nul` | ok | unsat | complete |
| `CString::into_string` | ok | unsat | complete |
| `FromUtf8Error::as_bytes` | ok | unsat | complete |
| `FromUtf8Error::into_bytes` | ok | unsat | complete |
| `FromUtf8Error::utf8_error` | ok | unsat | complete |
| `alloc::ffi::NulError::nul_position` | ok | unsat | complete |
| `alloc::ffi::NulError::into_vec` | ok | unsat | complete |
| `alloc::ffi::FromVecWithNulError::as_bytes` | ok | unsat | complete |
| `alloc::ffi::FromVecWithNulError::into_bytes` | ok | unsat | complete |
| `alloc::ffi::IntoStringError::into_cstring` | ok | unsat | complete |
| `alloc::ffi::IntoStringError::utf8_error` | ok | unsat | complete |
