# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 32
- Add-spec decisions: 24
- Skip decisions: 8
- Static skips: 0
- Raw determinism reward: 24
- Guarded reward: 24
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::collections::BTreeMap::append` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::first_key_value` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::get_key_value` | data_structure | skip | 0 | 0 |  |
| `alloc::collections::BTreeMap::last_key_value` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::pop_first` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::pop_last` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::remove_entry` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::append` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::first` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::is_disjoint` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::as_bytes` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::clear` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::into_bytes` | data_structure | add_spec | 1 | 1 |  |
| `alloc::vec::Vec::dedup` | data_structure | add_spec | 1 | 1 |  |
| `alloc::vec::Vec::into_boxed_slice` | data_structure | add_spec | 1 | 1 |  |
| `core::array::each_ref` | data_structure | add_spec | 1 | 1 |  |
| `core::array::repeat` | data_structure | add_spec | 1 | 1 |  |
| `core::cmp::max` | data_structure | add_spec | 1 | 1 |  |
| `core::convert::identity` | data_structure | add_spec | 1 | 1 |  |
| `core::hint::black_box` | other | add_spec | 1 | 1 |  |
| `core::mem::discriminant` | data_structure | skip | 0 | 0 |  |
| `core::mem::replace` | data_structure | add_spec | 1 | 1 |  |
| `core::ops::RangeInclusive::end` | other | add_spec | 1 | 1 |  |
| `core::option::Option::replace` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::as_array` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::clone_from_slice` | data_structure | skip | 0 | 0 |  |
| `core::slice::split_off` | data_structure | skip | 0 | 0 |  |
| `core::slice::split_off_first` | data_structure | skip | 0 | 0 |  |
| `core::slice::split_off_last` | data_structure | skip | 0 | 0 |  |
| `core::str::make_ascii_lowercase` | data_structure | skip | 0 | 0 |  |
| `core::str::split_at_checked` | data_structure | add_spec | 1 | 1 |  |
| `std::collections::HashMap::get_key_value` | other | skip | 0 | 0 |  |
