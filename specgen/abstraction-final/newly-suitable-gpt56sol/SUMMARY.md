# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 20
- Add-spec decisions: 10
- Skip decisions: 10
- Static skips: 0
- Raw determinism reward: 10
- Guarded reward: 10
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::collections::BinaryHeap::peek_mut` | data_structure | skip | 0 | 0 |  |
| `alloc::collections::VecDeque::binary_search` | data_structure | skip | 0 | 0 |  |
| `alloc::collections::VecDeque::swap_remove_back` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::VecDeque::swap_remove_front` | data_structure | add_spec | 1 | 1 |  |
| `alloc::ffi::CString::new` | other | skip | 0 | 0 |  |
| `core::alloc::Layout::extend` | memory_pointer | add_spec | 1 | 1 |  |
| `core::alloc::Layout::extend_packed` | memory_pointer | add_spec | 1 | 1 |  |
| `core::alloc::Layout::repeat` | memory_pointer | add_spec | 1 | 1 |  |
| `core::alloc::Layout::repeat_packed` | memory_pointer | add_spec | 1 | 1 |  |
| `core::panic::Location::caller` | other | skip | 0 | 0 |  |
| `core::panic::Location::file_as_c_str` | other | add_spec | 1 | 1 |  |
| `core::time::Duration::as_secs_f32` | other | add_spec | 1 | 1 |  |
| `core::time::Duration::as_secs_f64` | other | add_spec | 1 | 1 |  |
| `core::time::Duration::div_duration_f32` | other | skip | 0 | 0 |  |
| `core::time::Duration::div_duration_f64` | other | skip | 0 | 0 |  |
| `core::time::Duration::div_f32` | other | skip | 0 | 0 |  |
| `core::time::Duration::div_f64` | other | add_spec | 1 | 1 |  |
| `core::time::Duration::mul_f32` | other | skip | 0 | 0 |  |
| `core::time::Duration::try_from_secs_f32` | other | skip | 0 | 0 |  |
| `core::time::Duration::try_from_secs_f64` | other | skip | 0 | 0 |  |
