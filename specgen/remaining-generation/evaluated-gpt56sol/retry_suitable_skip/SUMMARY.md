# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 30
- Add-spec decisions: 1
- Skip decisions: 29
- Static skips: 0
- Raw determinism reward: 1
- Guarded reward: 1
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::collections::BTreeMap::get_key_value` | data_structure | skip | 0 | 0 |  |
| `alloc::collections::BTreeMap::split_off` | data_structure | skip | 0 | 0 |  |
| `alloc::collections::BTreeSet::split_off` | data_structure | skip | 0 | 0 |  |
| `alloc::string::String::replace_range` | data_structure | add_spec | 1 | 1 |  |
| `alloc::vec::Vec::extend_from_within` | data_structure | skip | 0 | 0 |  |
| `core::mem::discriminant` | data_structure | skip | 0 | 0 |  |
| `core::mem::needs_drop` | data_structure | skip | 0 | 0 |  |
| `core::mem::take` | data_structure | skip | 0 | 0 |  |
| `core::result::Result::unwrap_or_default` | data_structure | skip | 0 | 0 |  |
| `core::slice::clone_from_slice` | data_structure | skip | 0 | 0 |  |
| `core::slice::element_offset` | data_structure | skip | 0 | 0 |  |
| `core::slice::fill` | data_structure | skip | 0 | 0 |  |
| `core::slice::make_ascii_lowercase` | data_structure | skip | 0 | 0 |  |
| `core::slice::make_ascii_uppercase` | data_structure | skip | 0 | 0 |  |
| `core::slice::reverse` | data_structure | skip | 0 | 0 |  |
| `core::slice::rotate_left` | data_structure | skip | 0 | 0 |  |
| `core::slice::rotate_right` | data_structure | skip | 0 | 0 |  |
| `core::slice::split_off` | data_structure | skip | 0 | 0 |  |
| `core::slice::split_off_first` | data_structure | skip | 0 | 0 |  |
| `core::slice::split_off_last` | data_structure | skip | 0 | 0 |  |
| `core::slice::strip_circumfix` | data_structure | skip | 0 | 0 |  |
| `core::slice::strip_prefix` | data_structure | skip | 0 | 0 |  |
| `core::slice::strip_suffix` | data_structure | skip | 0 | 0 |  |
| `core::slice::subslice_range` | data_structure | skip | 0 | 0 |  |
| `core::slice::swap` | data_structure | skip | 0 | 0 |  |
| `core::slice::swap_with_slice` | data_structure | skip | 0 | 0 |  |
| `core::str::make_ascii_lowercase` | data_structure | skip | 0 | 0 |  |
| `core::str::make_ascii_uppercase` | data_structure | skip | 0 | 0 |  |
| `core::str::substr_range` | data_structure | skip | 0 | 0 |  |
| `std::collections::HashMap::get_key_value` | other | skip | 0 | 0 |  |
