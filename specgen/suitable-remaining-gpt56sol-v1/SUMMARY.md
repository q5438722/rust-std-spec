# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 101
- Add-spec decisions: 79
- Skip decisions: 22
- Static skips: 0
- Raw determinism reward: 79
- Guarded reward: 79
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::collections::BTreeMap::split_off` | data_structure | skip | 0 | 0 |  |
| `alloc::collections::BTreeSet::is_subset` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::is_superset` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::last` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::pop_first` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::pop_last` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::replace` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::split_off` | data_structure | skip | 0 | 0 |  |
| `alloc::collections::BTreeSet::take` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::extend_from_within` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::insert` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::insert_str` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::is_empty` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::len` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::pop` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::push` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::push_str` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::remove` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::replace_range` | data_structure | skip | 0 | 0 |  |
| `alloc::string::String::split_off` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::truncate` | data_structure | add_spec | 1 | 1 |  |
| `alloc::vec::Vec::extend_from_within` | data_structure | skip | 0 | 0 |  |
| `alloc::vec::Vec::into_flattened` | data_structure | add_spec | 1 | 1 |  |
| `core::array::from_ref` | data_structure | add_spec | 1 | 1 |  |
| `core::cmp::min` | data_structure | add_spec | 1 | 1 |  |
| `core::hint::select_unpredictable` | other | add_spec | 1 | 1 |  |
| `core::mem::min_align_of` | data_structure | add_spec | 1 | 1 |  |
| `core::mem::min_align_of_val` | data_structure | add_spec | 1 | 1 |  |
| `core::mem::needs_drop` | data_structure | skip | 0 | 0 |  |
| `core::mem::take` | data_structure | skip | 0 | 0 |  |
| `core::ops::Range::is_empty` | other | add_spec | 1 | 1 |  |
| `core::ops::RangeInclusive::into_inner` | other | add_spec | 1 | 1 |  |
| `core::ops::RangeInclusive::is_empty` | other | add_spec | 1 | 1 |  |
| `core::ops::RangeInclusive::start` | other | add_spec | 1 | 1 |  |
| `core::option::Option::and` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::flatten` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::or` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::transpose` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::unzip` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::xor` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::zip` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::and` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::expect_err` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::flatten` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::or` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::transpose` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::unwrap_or` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::unwrap_or_default` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::as_chunks` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::as_flattened` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::as_rchunks` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::binary_search` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::contains` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::element_offset` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::ends_with` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::eq_ignore_ascii_case` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::fill` | data_structure | skip | 0 | 0 |  |
| `core::slice::first_chunk` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::from_ref` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::is_ascii` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::is_sorted` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::last_chunk` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::make_ascii_lowercase` | data_structure | skip | 0 | 0 |  |
| `core::slice::make_ascii_uppercase` | data_structure | skip | 0 | 0 |  |
| `core::slice::reverse` | data_structure | skip | 0 | 0 |  |
| `core::slice::rotate_left` | data_structure | skip | 0 | 0 |  |
| `core::slice::rotate_right` | data_structure | skip | 0 | 0 |  |
| `core::slice::split_at_checked` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_first` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_first_chunk` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_last` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_last_chunk` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::starts_with` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::strip_circumfix` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::strip_prefix` | data_structure | skip | 0 | 0 |  |
| `core::slice::strip_suffix` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::subslice_range` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::swap` | data_structure | skip | 0 | 0 |  |
| `core::slice::swap_with_slice` | data_structure | skip | 0 | 0 |  |
| `core::slice::trim_ascii` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::trim_ascii_end` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::trim_ascii_start` | data_structure | add_spec | 1 | 1 |  |
| `core::str::ceil_char_boundary` | data_structure | add_spec | 1 | 1 |  |
| `core::str::eq_ignore_ascii_case` | data_structure | add_spec | 1 | 1 |  |
| `core::str::floor_char_boundary` | data_structure | add_spec | 1 | 1 |  |
| `core::str::make_ascii_uppercase` | data_structure | skip | 0 | 0 |  |
| `core::str::substr_range` | data_structure | skip | 0 | 0 |  |
| `core::str::trim` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_ascii` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_ascii_end` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_ascii_start` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_end` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_left` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_right` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_start` | data_structure | add_spec | 1 | 1 |  |
| `std::collections::HashMap::remove_entry` | other | add_spec | 1 | 1 |  |
| `std::collections::HashSet::is_disjoint` | other | add_spec | 1 | 1 |  |
| `std::collections::HashSet::is_subset` | other | add_spec | 1 | 1 |  |
| `std::collections::HashSet::is_superset` | other | add_spec | 1 | 1 |  |
| `std::collections::HashSet::replace` | other | add_spec | 1 | 1 |  |
| `std::collections::HashSet::take` | other | add_spec | 1 | 1 |  |
