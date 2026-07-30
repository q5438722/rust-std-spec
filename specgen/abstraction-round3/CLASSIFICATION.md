# Classification of 2,121 stable uncovered Rust APIs

## Summary

| Classification | Count |
|---|---:|
| `runtime_or_hidden_state` | 495 |
| `trait_contract_integration` | 201 |
| `needs_new_vstd_abstraction` | 191 |
| `unsafe_or_representation_sensitive` | 180 |
| `concurrency_or_hidden_state` | 179 |
| `suitable_now` | 164 |
| `determinism_checker_unsupported` | 109 |
| `iterator_or_adapter_result` | 101 |
| `formatting_effect` | 79 |
| `higher_order_contract` | 71 |
| `toolchain_unavailable` | 70 |
| `representation_or_allocator` | 59 |
| `ownership_or_uninitialized_model` | 33 |
| `complex_result_or_pattern_model` | 21 |
| `associated_type_or_projection` | 19 |
| `no_modeled_observable_output` | 9 |

First-run generation targets: **164**.

## Suitable-now targets by category

| Category | Count |
|---|---:|
| `data_structure` | 121 |
| `other` | 39 |
| `memory_pointer` | 4 |

## Largest suitable owner groups

| Owner/module | Count |
|---|---:|
| `core::slice` | 39 |
| `alloc::string::String` | 15 |
| `core::str` | 15 |
| `core::time::Duration` | 12 |
| `alloc::collections::BTreeSet` | 11 |
| `alloc::collections::BTreeMap` | 8 |
| `core::net::Ipv6Addr` | 8 |
| `core::option::Option` | 8 |
| `core::result::Result` | 7 |
| `core::mem` | 6 |
| `std::collections::HashSet` | 5 |
| `alloc::vec::Vec` | 4 |
| `core::alloc::Layout` | 4 |
| `core::ops::RangeInclusive` | 4 |
| `core::array` | 3 |
| `core::cmp` | 2 |
| `core::hint` | 2 |
| `core::net::Ipv4Addr` | 2 |
| `std::collections::HashMap` | 2 |
| `alloc::collections::BinaryHeap` | 1 |
| `alloc::collections::LinkedList` | 1 |
| `alloc::ffi::CString` | 1 |
| `core::convert` | 1 |
| `core::net::IpAddr` | 1 |
| `core::net::SocketAddr` | 1 |
| `core::ops::Range` | 1 |

## First-run target list

| Target | Category | Notes |
|---|---|---|
| `alloc::collections::BTreeMap::append` | data_structure | - |
| `alloc::collections::BTreeMap::first_key_value` | data_structure | must_compare_semantic_view_not_reference_identity |
| `alloc::collections::BTreeMap::get_key_value` | data_structure | must_compare_semantic_view_not_reference_identity |
| `alloc::collections::BTreeMap::last_key_value` | data_structure | must_compare_semantic_view_not_reference_identity |
| `alloc::collections::BTreeMap::pop_first` | data_structure | - |
| `alloc::collections::BTreeMap::pop_last` | data_structure | - |
| `alloc::collections::BTreeMap::remove_entry` | data_structure | - |
| `alloc::collections::BTreeMap::split_off` | data_structure | - |
| `alloc::collections::BTreeSet::append` | data_structure | - |
| `alloc::collections::BTreeSet::first` | data_structure | must_compare_semantic_view_not_reference_identity |
| `alloc::collections::BTreeSet::is_disjoint` | data_structure | - |
| `alloc::collections::BTreeSet::is_subset` | data_structure | - |
| `alloc::collections::BTreeSet::is_superset` | data_structure | - |
| `alloc::collections::BTreeSet::last` | data_structure | must_compare_semantic_view_not_reference_identity |
| `alloc::collections::BTreeSet::pop_first` | data_structure | - |
| `alloc::collections::BTreeSet::pop_last` | data_structure | - |
| `alloc::collections::BTreeSet::replace` | data_structure | - |
| `alloc::collections::BTreeSet::split_off` | data_structure | - |
| `alloc::collections::BTreeSet::take` | data_structure | - |
| `alloc::collections::BinaryHeap::peek_mut` | data_structure | - |
| `alloc::collections::LinkedList::contains` | data_structure | - |
| `alloc::ffi::CString::new` | other | - |
| `alloc::string::String::as_bytes` | data_structure | must_compare_semantic_view_not_reference_identity |
| `alloc::string::String::clear` | data_structure | - |
| `alloc::string::String::extend_from_within` | data_structure | - |
| `alloc::string::String::insert` | data_structure | - |
| `alloc::string::String::insert_str` | data_structure | - |
| `alloc::string::String::into_bytes` | data_structure | - |
| `alloc::string::String::is_empty` | data_structure | - |
| `alloc::string::String::len` | data_structure | - |
| `alloc::string::String::pop` | data_structure | - |
| `alloc::string::String::push` | data_structure | - |
| `alloc::string::String::push_str` | data_structure | - |
| `alloc::string::String::remove` | data_structure | - |
| `alloc::string::String::replace_range` | data_structure | - |
| `alloc::string::String::split_off` | data_structure | - |
| `alloc::string::String::truncate` | data_structure | - |
| `alloc::vec::Vec::dedup` | data_structure | - |
| `alloc::vec::Vec::extend_from_within` | data_structure | - |
| `alloc::vec::Vec::into_boxed_slice` | data_structure | - |
| `alloc::vec::Vec::into_flattened` | data_structure | - |
| `core::alloc::Layout::extend` | memory_pointer | - |
| `core::alloc::Layout::extend_packed` | memory_pointer | - |
| `core::alloc::Layout::repeat` | memory_pointer | - |
| `core::alloc::Layout::repeat_packed` | memory_pointer | - |
| `core::array::each_ref` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::array::from_ref` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::array::repeat` | data_structure | - |
| `core::cmp::max` | data_structure | - |
| `core::cmp::min` | data_structure | - |
| `core::convert::identity` | data_structure | - |
| `core::hint::black_box` | other | - |
| `core::hint::select_unpredictable` | other | - |
| `core::mem::discriminant` | data_structure | - |
| `core::mem::min_align_of` | data_structure | - |
| `core::mem::min_align_of_val` | data_structure | - |
| `core::mem::needs_drop` | data_structure | - |
| `core::mem::replace` | data_structure | - |
| `core::mem::take` | data_structure | - |
| `core::net::IpAddr::to_canonical` | other | - |
| `core::net::Ipv4Addr::from_bits` | other | - |
| `core::net::Ipv4Addr::to_bits` | other | - |
| `core::net::Ipv6Addr::from_bits` | other | - |
| `core::net::Ipv6Addr::from_segments` | other | - |
| `core::net::Ipv6Addr::new` | other | - |
| `core::net::Ipv6Addr::segments` | other | - |
| `core::net::Ipv6Addr::to_bits` | other | - |
| `core::net::Ipv6Addr::to_canonical` | other | - |
| `core::net::Ipv6Addr::to_ipv4` | other | - |
| `core::net::Ipv6Addr::to_ipv4_mapped` | other | - |
| `core::net::SocketAddr::set_ip` | other | - |
| `core::ops::Range::is_empty` | other | - |
| `core::ops::RangeInclusive::end` | other | must_compare_semantic_view_not_reference_identity |
| `core::ops::RangeInclusive::into_inner` | other | - |
| `core::ops::RangeInclusive::is_empty` | other | - |
| `core::ops::RangeInclusive::start` | other | must_compare_semantic_view_not_reference_identity |
| `core::option::Option::and` | data_structure | - |
| `core::option::Option::flatten` | data_structure | - |
| `core::option::Option::or` | data_structure | - |
| `core::option::Option::replace` | data_structure | - |
| `core::option::Option::transpose` | data_structure | - |
| `core::option::Option::unzip` | data_structure | - |
| `core::option::Option::xor` | data_structure | - |
| `core::option::Option::zip` | data_structure | - |
| `core::result::Result::and` | data_structure | - |
| `core::result::Result::expect_err` | data_structure | - |
| `core::result::Result::flatten` | data_structure | - |
| `core::result::Result::or` | data_structure | - |
| `core::result::Result::transpose` | data_structure | - |
| `core::result::Result::unwrap_or` | data_structure | - |
| `core::result::Result::unwrap_or_default` | data_structure | - |
| `core::slice::as_array` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::as_chunks` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::as_flattened` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::as_rchunks` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::binary_search` | data_structure | - |
| `core::slice::clone_from_slice` | data_structure | - |
| `core::slice::contains` | data_structure | - |
| `core::slice::element_offset` | data_structure | - |
| `core::slice::ends_with` | data_structure | - |
| `core::slice::eq_ignore_ascii_case` | data_structure | - |
| `core::slice::fill` | data_structure | - |
| `core::slice::first_chunk` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::from_ref` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::is_ascii` | data_structure | - |
| `core::slice::is_sorted` | data_structure | - |
| `core::slice::last_chunk` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::make_ascii_lowercase` | data_structure | - |
| `core::slice::make_ascii_uppercase` | data_structure | - |
| `core::slice::reverse` | data_structure | - |
| `core::slice::rotate_left` | data_structure | - |
| `core::slice::rotate_right` | data_structure | - |
| `core::slice::split_at_checked` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::split_first` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::split_first_chunk` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::split_last` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::split_last_chunk` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::split_off` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::split_off_first` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::split_off_last` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::starts_with` | data_structure | - |
| `core::slice::strip_circumfix` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::strip_prefix` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::strip_suffix` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::subslice_range` | data_structure | - |
| `core::slice::swap` | data_structure | - |
| `core::slice::swap_with_slice` | data_structure | - |
| `core::slice::trim_ascii` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::trim_ascii_end` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::slice::trim_ascii_start` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::str::ceil_char_boundary` | data_structure | - |
| `core::str::eq_ignore_ascii_case` | data_structure | - |
| `core::str::floor_char_boundary` | data_structure | - |
| `core::str::make_ascii_lowercase` | data_structure | - |
| `core::str::make_ascii_uppercase` | data_structure | - |
| `core::str::split_at_checked` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::str::substr_range` | data_structure | - |
| `core::str::trim` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::str::trim_ascii` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::str::trim_ascii_end` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::str::trim_ascii_start` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::str::trim_end` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::str::trim_left` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::str::trim_right` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::str::trim_start` | data_structure | must_compare_semantic_view_not_reference_identity |
| `core::time::Duration::as_secs_f32` | other | - |
| `core::time::Duration::as_secs_f64` | other | - |
| `core::time::Duration::div_duration_f32` | other | - |
| `core::time::Duration::div_duration_f64` | other | - |
| `core::time::Duration::div_f32` | other | - |
| `core::time::Duration::div_f64` | other | - |
| `core::time::Duration::from_secs_f32` | other | - |
| `core::time::Duration::from_secs_f64` | other | - |
| `core::time::Duration::mul_f32` | other | - |
| `core::time::Duration::mul_f64` | other | - |
| `core::time::Duration::try_from_secs_f32` | other | - |
| `core::time::Duration::try_from_secs_f64` | other | - |
| `std::collections::HashMap::get_key_value` | other | must_compare_semantic_view_not_reference_identity |
| `std::collections::HashMap::remove_entry` | other | - |
| `std::collections::HashSet::is_disjoint` | other | - |
| `std::collections::HashSet::is_subset` | other | - |
| `std::collections::HashSet::is_superset` | other | - |
| `std::collections::HashSet::replace` | other | - |
| `std::collections::HashSet::take` | other | - |
