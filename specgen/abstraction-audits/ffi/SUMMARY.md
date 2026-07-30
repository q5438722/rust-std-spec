# Determinism audit: ffi.rs

- Targets: 15
- R0 results: `{'unsat': 14, 'unknown': 1}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `CStr::count_bytes` | ok | unsat | complete |
| `CStr::is_empty` | ok | unsat | complete |
| `CStr::to_bytes` | ok | unsat | complete |
| `CStr::to_bytes_with_nul` | ok | unsat | complete |
| `CStr::from_bytes_with_nul` | ok | unsat | complete |
| `CStr::from_bytes_until_nul` | ok | unsat | complete |
| `CStr::to_str` | ok | unsat | complete |
| `CString::as_bytes` | ok | unsat | complete |
| `CString::as_bytes_with_nul` | ok | unsat | complete |
| `CString::as_c_str` | ok | unknown | ok_inconclusive |
| `CString::into_bytes` | ok | unsat | complete |
| `CString::into_bytes_with_nul` | ok | unsat | complete |
| `CString::into_boxed_c_str` | ok | unsat | complete |
| `CString::from_vec_with_nul` | ok | unsat | complete |
| `CString::into_string` | ok | unsat | complete |
