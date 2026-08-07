# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Manifest targets: 2121
- Targets: 2121
- Missing targets: 0
- Add-spec decisions: 127
- Skip decisions: 1994
- Static skips: 0
- Raw determinism reward: 127
- Guarded reward: 127
- LLM errors: 0
- Exceptions: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::alloc::alloc` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::alloc::alloc_zeroed` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::alloc::dealloc` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `alloc::alloc::handle_alloc_error` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::alloc::realloc` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::borrow::Cow::into_owned` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `alloc::borrow::Cow::to_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, cow_to_mut_payload_reference_model_missing |
| `alloc::borrow::ToOwned::clone_into` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `alloc::borrow::ToOwned::to_owned` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `alloc::boxed::Box::as_mut_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::assume_init` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::downcast` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::from_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::into_pin` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::boxed::Box::into_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::boxed::Box::leak` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::boxed::Box::new_uninit_slice` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::boxed::Box::new_zeroed` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::boxed::Box::new_zeroed_slice` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::boxed::Box::pin` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::boxed::Box::write` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::boxed::BoxedArrayIntoIter::as_mut_slice` | data_structure | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `alloc::boxed::BoxedArrayIntoIter::as_slice` | data_structure | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `alloc::collections::BTreeMap::append` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::entry` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::extract_if` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::first_entry` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::first_key_value` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::get_key_value` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::get_mut` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::into_keys` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::into_values` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::last_entry` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::last_key_value` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::pop_first` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::pop_last` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeMap::range` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::range_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::remove_entry` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::split_off` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::values_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::append` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::difference` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::extract_if` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::first` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::intersection` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::BTreeSet::is_disjoint` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::is_subset` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::is_superset` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::last` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::pop_first` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::pop_last` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::range` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::replace` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::BTreeSet::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::BTreeSet::split_off` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BTreeSet::symmetric_difference` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::BTreeSet::take` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BTreeSet::union` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BinaryHeap::append` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::as_slice` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::clear` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::drain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::BinaryHeap::into_sorted_vec` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::into_vec` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::is_empty` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::iter` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::BinaryHeap::len` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::new` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::peek` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::peek_mut` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BinaryHeap::pop` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::push` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::reserve` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::BinaryHeap::shrink_to` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::shrink_to_fit` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::try_reserve` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::try_reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::with_capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::append` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::back` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::back_mut` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::LinkedList::clear` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::contains` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::extract_if` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::front` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::front_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::LinkedList::is_empty` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::iter` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::len` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::new` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::pop_back` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::pop_front` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::push_back` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::push_back_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::LinkedList::push_front` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::push_front_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::LinkedList::split_off` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::as_mut_slices` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, implementation_dependent_split_point |
| `alloc::collections::VecDeque::as_slices` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::back` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::back_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::binary_search` | data_structure | add_spec | 1 | 1 |  |
| `alloc::collections::VecDeque::binary_search_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract, higher_order_closure_comparator_underdetermined |
| `alloc::collections::VecDeque::binary_search_by_key` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::contains` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::drain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::front` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::front_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::get` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::insert_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::is_empty` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::make_contiguous` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::partition_point` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::pop_back_if` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::pop_front_if` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::push_back_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::push_front_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::range` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::range_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::resize_with` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::retain_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::rotate_left` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::rotate_right` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::shrink_to` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::shrink_to_fit` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::swap` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::swap_remove_back` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::swap_remove_front` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::try_reserve` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::try_reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::collections::btree_map::Entry::and_modify` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `alloc::collections::btree_map::Entry::insert_entry` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::Entry::key` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `alloc::collections::btree_map::Entry::or_default` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_insert` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::btree_map::Entry::or_insert_with` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_insert_with_key` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::OccupiedEntry::get` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::OccupiedEntry::insert` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::into_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::OccupiedEntry::key` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `alloc::collections::btree_map::OccupiedEntry::remove` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::remove_entry` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `alloc::collections::btree_map::VacantEntry::insert` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::collections::btree_map::VacantEntry::insert_entry` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::VacantEntry::into_key` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::VacantEntry::key` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::as_bytes` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::as_bytes_with_nul` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::as_c_str` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::from_raw` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::ffi::CString::from_vec_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::ffi::CString::from_vec_with_nul` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::from_vec_with_nul_unchecked` | other | add_spec | 1 | 1 |  |
| `alloc::ffi::CString::into_boxed_c_str` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::into_bytes` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::into_bytes_with_nul` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::into_raw` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::ffi::CString::into_string` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::new` | other | skip | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::ffi::FromVecWithNulError::as_bytes` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::FromVecWithNulError::into_bytes` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::IntoStringError::into_cstring` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::IntoStringError::utf8_error` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::NulError::into_vec` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::NulError::nul_position` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::fmt::format` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `alloc::rc::Rc::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::rc::Rc::assume_init` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::decrement_strong_count` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `alloc::rc::Rc::downcast` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::rc::Rc::downgrade` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::from_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::rc::Rc::increment_strong_count` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `alloc::rc::Rc::into_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::make_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::rc::Rc::new_cyclic` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_uninit` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_uninit_slice` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::rc::Rc::new_zeroed` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_zeroed_slice` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::rc::Rc::pin` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::rc::Rc::ptr_eq` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::strong_count` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::rc::Rc::unwrap_or_clone` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::rc::Rc::weak_count` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Weak::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::from_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::into_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::new` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::ptr_eq` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::strong_count` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::upgrade` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::weak_count` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::str::from_boxed_utf8_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::string::Drain::as_str` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::string::FromUtf8Error::as_bytes` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::string::FromUtf8Error::into_bytes` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::string::FromUtf8Error::utf8_error` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::string::String::as_bytes` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::as_mut_str` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::string::String::as_mut_vec` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::string::String::capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::string::String::clear` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::drain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::string::String::extend_from_within` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::string::String::from_raw_parts` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::string::String::from_utf16` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::string::String::from_utf16_lossy` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::string::String::from_utf16be` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::string::String::from_utf16be_lossy` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::string::String::from_utf16le` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::string::String::from_utf16le_lossy` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::string::String::from_utf8` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::string::String::from_utf8_lossy` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::string::String::from_utf8_unchecked` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::insert` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::insert_str` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::into_boxed_str` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `alloc::string::String::into_bytes` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::into_raw_parts` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::string::String::is_empty` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::leak` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::string::String::len` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::pop` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::push` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::push_str` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::remove` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::replace_range` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::reserve` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::string::String::reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::string::String::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::string::String::shrink_to` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::string::String::shrink_to_fit` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::string::String::split_off` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::truncate` | data_structure | add_spec | 1 | 1 |  |
| `alloc::string::String::try_reserve` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::string::String::try_reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::string::String::with_capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::sync::Arc::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::assume_init` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::sync::Arc::decrement_strong_count` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `alloc::sync::Arc::downcast` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::downgrade` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::from_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::sync::Arc::increment_strong_count` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `alloc::sync::Arc::into_inner` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::sync::Arc::into_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::make_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::sync::Arc::new_cyclic` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::sync::Arc::new_uninit` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::new_uninit_slice` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::sync::Arc::new_zeroed` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::new_zeroed_slice` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::sync::Arc::pin` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::sync::Arc::ptr_eq` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::strong_count` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::sync::Arc::try_unwrap` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::unwrap_or_clone` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::sync::Arc::weak_count` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Weak::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::from_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::into_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::new` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::ptr_eq` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::strong_count` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::upgrade` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::weak_count` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::vec::Drain::as_slice` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `alloc::vec::IntoIter::as_mut_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::IntoIter::as_slice` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::vec::Vec::as_mut_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::vec::Vec::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::vec::Vec::capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::vec::Vec::dedup` | data_structure | add_spec | 1 | 1 |  |
| `alloc::vec::Vec::dedup_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `alloc::vec::Vec::dedup_by_key` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `alloc::vec::Vec::drain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::vec::Vec::extend_from_within` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::vec::Vec::extract_if` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::from_raw_parts` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::vec::Vec::insert_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::vec::Vec::into_boxed_slice` | data_structure | add_spec | 1 | 1 |  |
| `alloc::vec::Vec::into_flattened` | data_structure | add_spec | 1 | 1 |  |
| `alloc::vec::Vec::into_raw_parts` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::vec::Vec::leak` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::vec::Vec::pop_if` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `alloc::vec::Vec::push_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::vec::Vec::reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::vec::Vec::resize_with` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `alloc::vec::Vec::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::vec::Vec::retain_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `alloc::vec::Vec::set_len` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `alloc::vec::Vec::shrink_to` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::vec::Vec::shrink_to_fit` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `alloc::vec::Vec::spare_capacity_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `alloc::vec::Vec::splice` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::try_reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, duplicate_vstd_assume_specification |
| `core::alloc::GlobalAlloc::alloc` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::alloc::GlobalAlloc::alloc_zeroed` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::alloc::GlobalAlloc::dealloc` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form, no_modeled_observable_output |
| `core::alloc::GlobalAlloc::realloc` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::alloc::Layout::align` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::align_to` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::array` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::dangling_ptr` | memory_pointer | skip | 0 | 0 | classification:representation_or_allocator |
| `core::alloc::Layout::extend` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::extend_packed` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::for_value` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::from_size_align` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::from_size_align_unchecked` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, duplicate_vstd_assume_specification |
| `core::alloc::Layout::new` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::pad_to_align` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::repeat` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::repeat_packed` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::size` | memory_pointer | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::array::IntoIter::as_mut_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::array::IntoIter::as_slice` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `core::array::IntoIter::new` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::array::as_mut_slice` | data_structure | add_spec | 1 | 1 |  |
| `core::array::each_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::array::each_ref` | data_structure | add_spec | 1 | 1 |  |
| `core::array::from_fn` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::array::from_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::array::from_ref` | data_structure | add_spec | 1 | 1 |  |
| `core::array::map` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::array::repeat` | data_structure | skip | 0 | 0 | clone_semantics_unmodeled |
| `core::borrow::Borrow::borrow` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::borrow::BorrowMut::borrow_mut` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::cell::Cell::as_array_of_cells` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::cell::Cell::as_slice_of_cells` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::from_mut` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::get` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::Cell::into_inner` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::new` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::replace` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::set` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::cell::Cell::swap` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::cell::Cell::take` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::update` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::cell::LazyCell::force` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::LazyCell::force_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::LazyCell::get` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::LazyCell::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::LazyCell::new` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::OnceCell::get` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::OnceCell::get_or_init` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::OnceCell::into_inner` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::new` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::set` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::take` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Ref::clone` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Ref::filter_map` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::cell::Ref::map` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::map_split` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefCell::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::cell::RefCell::borrow` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::borrow_mut` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::RefCell::into_inner` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::new` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::replace` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::replace_with` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefCell::swap` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::cell::RefCell::take` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::try_borrow` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::try_borrow_mut` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::try_borrow_unguarded` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::RefMut::filter_map` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::map` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::map_split` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::UnsafeCell::from_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::UnsafeCell::get` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::cell::UnsafeCell::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::UnsafeCell::into_inner` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::UnsafeCell::new` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::UnsafeCell::raw_get` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::clone::Clone::clone_from` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::cmp::Ordering::is_eq` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::is_ge` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::is_gt` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::is_le` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::is_lt` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::is_ne` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::reverse` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::then` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::then_with` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::cmp::max` | data_structure | add_spec | 1 | 1 |  |
| `core::cmp::max_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::cmp::max_by_key` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::cmp::min` | data_structure | add_spec | 1 | 1 |  |
| `core::cmp::min_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::cmp::min_by_key` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::convert::AsMut::as_mut` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::convert::AsRef::as_ref` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::convert::identity` | data_structure | add_spec | 1 | 1 |  |
| `core::error::Error::cause` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::error::Error::description` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::error::Error::source` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ffi::CStr::as_ptr` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ffi::CStr::count_bytes` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::from_bytes_until_nul` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::from_bytes_with_nul` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::from_bytes_with_nul_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ffi::CStr::from_ptr` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ffi::CStr::is_empty` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::to_bytes` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::to_bytes_with_nul` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::to_str` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::fmt::Arguments::as_str` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Binary::fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::Debug::fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::DebugList::entries` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugList::entry` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugList::finish` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugList::finish_non_exhaustive` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::entries` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::entry` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::finish` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::finish_non_exhaustive` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::key` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::value` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::entries` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::entry` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::finish` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::finish_non_exhaustive` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugStruct::field` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugStruct::finish` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugStruct::finish_non_exhaustive` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugTuple::field` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugTuple::finish` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugTuple::finish_non_exhaustive` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Display::fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::Formatter::align` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::alternate` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_list` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_map` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_set` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_struct` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_tuple` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::fill` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::flags` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Formatter::pad` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::pad_integral` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::precision` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::sign_aware_zero_pad` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::sign_minus` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::sign_plus` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::width` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::write_fmt` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::write_str` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::LowerExp::fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::LowerHex::fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::NumBuffer::new` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Octal::fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::Pointer::fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::Result::and` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::and_then` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_deref` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::as_deref_mut` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::as_mut` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_ref` | formatting | skip | 0 | 0 | classification:formatting_effect, duplicate_vstd_assume_specification |
| `core::fmt::Result::cloned` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::copied` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::err` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::expect` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::expect_err` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::flatten` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::inspect` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::inspect_err` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::is_err` | formatting | skip | 0 | 0 | classification:formatting_effect, duplicate_vstd_assume_specification |
| `core::fmt::Result::is_err_and` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::is_ok` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::is_ok_and` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::iter` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::iter_mut` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::map` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::map_err` | formatting | skip | 0 | 0 | classification:formatting_effect, duplicate_vstd_assume_specification |
| `core::fmt::Result::map_or` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::map_or_default` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map_or_else` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::ok` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::or` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::or_else` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::transpose` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_err` | formatting | skip | 0 | 0 | classification:formatting_effect, duplicate_vstd_assume_specification |
| `core::fmt::Result::unwrap_err_unchecked` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_or` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::unwrap_or_default` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_or_else` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::unwrap_unchecked` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::UpperExp::fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::UpperHex::fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::Write::write_char` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::Write::write_fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::Write::write_str` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::fmt::from_fn` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::write` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::future::Future::poll` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::future::IntoFuture::into_future` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::future::Ready::into_inner` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::future::pending` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::future::poll_fn` | other | skip | 0 | 0 | classification:higher_order_contract |
| `core::future::ready` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::hint::assert_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form, no_modeled_observable_output |
| `core::hint::black_box` | other | add_spec | 1 | 1 |  |
| `core::hint::cold_path` | other | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::hint::select_unpredictable` | other | add_spec | 1 | 1 |  |
| `core::hint::spin_loop` | other | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::intrinsics::copy` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::intrinsics::copy_nonoverlapping` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::intrinsics::transmute` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::intrinsics::write_bytes` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::io::Chain::get_mut` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Chain::get_ref` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Chain::into_inner` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Cursor::get_mut` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Cursor::get_ref` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Cursor::into_inner` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Cursor::new` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Cursor::position` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Cursor::set_position` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Error::get_mut` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Error::get_ref` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Error::kind` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Error::raw_os_error` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::IoSlice::advance` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::IoSlice::advance_slices` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::IoSlice::new` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::IoSliceMut::advance` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::IoSliceMut::advance_slices` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::IoSliceMut::new` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::and` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::and_then` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::as_deref` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::as_deref_mut` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::as_mut` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::as_ref` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::cloned` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::copied` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::err` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::expect` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::expect_err` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::flatten` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::inspect` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::inspect_err` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::is_err` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::is_err_and` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::is_ok` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::is_ok_and` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::iter` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::iter_mut` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::map` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::map_err` | other | skip | 0 | 0 | classification:toolchain_unavailable, determinism_unsupported_contract_form, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::map_or` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::map_or_default` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::map_or_else` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::ok` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::or` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::or_else` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::transpose` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::unwrap` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_err` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_err_unchecked` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_or` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_or_default` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_or_else` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_unchecked` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Seek::rewind` | trait_method | skip | 0 | 0 | classification:toolchain_unavailable, determinism_unsupported_contract_form, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Seek::seek` | trait_method | skip | 0 | 0 | classification:toolchain_unavailable, determinism_unsupported_contract_form, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Seek::seek_relative` | trait_method | skip | 0 | 0 | classification:toolchain_unavailable, determinism_unsupported_contract_form, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Seek::stream_position` | trait_method | skip | 0 | 0 | classification:toolchain_unavailable, determinism_unsupported_contract_form, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Take::get_mut` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Take::get_ref` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Take::into_inner` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Take::limit` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::Take::set_limit` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::empty` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::repeat` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::io::sink` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `core::iter::DoubleEndedIterator::nth_back` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::DoubleEndedIterator::rfind` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::DoubleEndedIterator::rfold` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, duplicate_vstd_assume_specification |
| `core::iter::DoubleEndedIterator::try_rfold` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::ExactSizeIterator::len` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Extend::extend` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::by_ref` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::chain` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::cloned` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::cmp` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::copied` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::count` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::cycle` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::enumerate` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::eq` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::filter` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::filter_map` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::find_map` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::flat_map` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::flatten` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::fold` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::for_each` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form, no_modeled_observable_output |
| `core::iter::Iterator::fuse` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::ge` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::gt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::inspect` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::is_sorted` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::is_sorted_by` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::is_sorted_by_key` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::last` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::le` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::lt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::map` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::map_while` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::max` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::max_by` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::max_by_key` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::min` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::min_by` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::min_by_key` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::ne` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::nth` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::partial_cmp` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::partition` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::peekable` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::position` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::product` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::reduce` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::rposition` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::scan` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::size_hint` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::skip` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::skip_while` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::step_by` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::sum` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::take` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::take_while` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::try_fold` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::try_for_each` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::unzip` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Iterator::zip` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Peekable::next_if` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::next_if_eq` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, peekable_next_if_closure_observation_underdetermined |
| `core::iter::Peekable::next_if_map` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::iter::Peekable::next_if_map_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, peekable_next_if_map_mut_closure_observation_underdetermined |
| `core::iter::Peekable::peek` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::peek_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::iter::Product::product` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::Sum::sum` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::iter::chain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::iter::empty` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::from_fn` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::once` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::iter::once_with` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::repeat` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::repeat_n` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::iter::repeat_with` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::successors` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::iter::zip` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::mem::ManuallyDrop::drop` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::ManuallyDrop::take` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::as_mut_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::assume_init_drop` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::mem::MaybeUninit::assume_init_read` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::mem::MaybeUninit::write` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::mem::MaybeUninit::zeroed` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `core::mem::discriminant` | data_structure | skip | 0 | 0 | compiler_intrinsic_discriminant_model_gap |
| `core::mem::drop` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::mem::forget` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, determinism_unsupported_contract_form, no_modeled_observable_output |
| `core::mem::min_align_of` | data_structure | add_spec | 1 | 1 |  |
| `core::mem::min_align_of_val` | data_structure | add_spec | 1 | 1 |  |
| `core::mem::needs_drop` | data_structure | skip | 0 | 0 | compiler_intrinsic_type_property_model_gap |
| `core::mem::replace` | data_structure | add_spec | 1 | 1 |  |
| `core::mem::take` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::mem::transmute_copy` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::uninitialized` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::zeroed` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::net::IpAddr::is_ipv4` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::IpAddr::is_ipv6` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::IpAddr::is_loopback` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::IpAddr::is_multicast` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::IpAddr::is_unspecified` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::IpAddr::to_canonical` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::from_bits` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::from_octets` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_broadcast` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_documentation` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_link_local` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_loopback` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_multicast` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_private` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_unspecified` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::new` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::octets` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::to_bits` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::to_ipv6_compatible` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::to_ipv6_mapped` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::from_bits` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::from_octets` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::from_segments` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::is_loopback` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::is_multicast` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::is_unicast_link_local` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::is_unique_local` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::is_unspecified` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::new` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::octets` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::segments` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::to_bits` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::to_canonical` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::to_ipv4` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::to_ipv4_mapped` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::ip` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::is_ipv4` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::is_ipv6` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::new` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::port` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::set_ip` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::set_port` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV4::ip` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV4::new` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV4::port` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV4::set_ip` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV4::set_port` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::flowinfo` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::ip` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::new` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::port` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::scope_id` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::set_flowinfo` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::set_ip` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::set_port` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::set_scope_id` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::AddAssign::add_assign` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::BitAnd::bitand` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::BitAndAssign::bitand_assign` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::BitOr::bitor` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::BitOrAssign::bitor_assign` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::BitXor::bitxor` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::BitXorAssign::bitxor_assign` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::Bound::as_ref` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `core::ops::Bound::cloned` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `core::ops::Bound::map` | other | skip | 0 | 0 | classification:higher_order_contract, higher_order_closure_result_underdetermined |
| `core::ops::ControlFlow::break_ok` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::break_value` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::continue_ok` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::continue_value` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::is_break` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::is_continue` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::map_break` | other | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::ops::ControlFlow::map_continue` | other | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::ops::DivAssign::div_assign` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::Drop::drop` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::IndexMut::index_mut` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::MulAssign::mul_assign` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::Not::not` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::Range::is_empty` | other | add_spec | 1 | 1 |  |
| `core::ops::RangeBounds::contains` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::RangeFrom::contains` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ops::RangeInclusive::end` | other | skip | 0 | 0 | value_unspecified_after_exhaustion |
| `core::ops::RangeInclusive::into_inner` | other | add_spec | 1 | 1 |  |
| `core::ops::RangeInclusive::is_empty` | other | add_spec | 1 | 1 |  |
| `core::ops::RangeInclusive::start` | other | skip | 0 | 0 | value_unspecified_after_exhaustion |
| `core::ops::RangeTo::contains` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `core::ops::RangeToInclusive::contains` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `core::ops::Rem::rem` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::RemAssign::rem_assign` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::Shl::shl` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::ShlAssign::shl_assign` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::Shr::shr` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::ShrAssign::shr_assign` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::ops::SubAssign::sub_assign` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::option::Option::and` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::as_deref` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection, determinism_unsupported_contract_form |
| `core::option::Option::as_deref_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::option::Option::as_pin_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::option::Option::as_pin_ref` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `core::option::Option::copied` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::option::Option::filter` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::option::Option::flatten` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::get_or_insert_default` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::option::Option::get_or_insert_with` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::option::Option::inspect` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::option::Option::is_none_or` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::is_some_and` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::option::Option::iter` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::option::Option::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::option::Option::map_or` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::option::Option::map_or_default` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::option::Option::map_or_else` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::or` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::or_else` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::option::Option::replace` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::take_if` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::transpose` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::unwrap_unchecked` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::option::Option::unzip` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::xor` | data_structure | add_spec | 1 | 1 |  |
| `core::option::Option::zip` | data_structure | add_spec | 1 | 1 |  |
| `core::panic::Location::caller` | other | skip | 0 | 0 | call_site_intrinsic_hidden_state |
| `core::panic::Location::column` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::panic::Location::file` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::panic::Location::file_as_c_str` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::panic::Location::line` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::panic::PanicInfo::location` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, panic_location_abstraction_missing |
| `core::panic::PanicInfo::message` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::PanicInfo::payload` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::PanicMessage::as_str` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `core::pin::Pin::as_deref_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::as_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::as_ref` | other | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::pin::Pin::get_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::get_ref` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::get_unchecked_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::into_inner` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::into_inner_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::into_ref` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::map_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::map_unchecked_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::new` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::new_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::set` | other | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::pin::Pin::static_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::static_ref` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::add` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::addr` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::align_offset` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::as_mut` | memory_pointer | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::ptr::NonNull::as_ptr` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, missing_nonnull_pointer_view |
| `core::ptr::NonNull::as_ref` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_add` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::NonNull::byte_offset_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_offset_from_unsigned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::cast` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::copy_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::copy_from_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::copy_to` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::copy_to_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::dangling` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::drop_in_place` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::expose_provenance` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::from_mut` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `core::ptr::NonNull::from_ref` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::is_aligned` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::is_empty` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::len` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::map_addr` | memory_pointer | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::ptr::NonNull::new` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::NonNull::new_unchecked` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::NonNull::offset_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::offset_from_unsigned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read_unaligned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read_volatile` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::replace` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::slice_from_raw_parts` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::swap` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::with_addr` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::with_exposed_provenance` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::without_provenance` | memory_pointer | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::write` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::write_bytes` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::write_unaligned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::write_volatile` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::add` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::addr` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, duplicate_vstd_assume_specification |
| `core::ptr::addr_eq` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::align_offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::as_array` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::as_mut` | memory_pointer | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::ptr::as_mut_array` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, raw_pointer_representation_contract |
| `core::ptr::as_mut_unchecked` | memory_pointer | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::ptr::as_ref` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::as_ref_unchecked` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::byte_add` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_offset_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::byte_offset_from_unsigned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::byte_sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::cast` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::cast_const` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::cast_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::copy` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::copy_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::copy_from_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::copy_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::copy_to` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::copy_to_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::dangling` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::dangling_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::drop_in_place` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::eq` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::expose_provenance` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::fn_addr_eq` | memory_pointer | skip | 0 | 0 | classification:representation_or_allocator |
| `core::ptr::from_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::from_ref` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::hash` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::is_aligned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::is_empty` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::is_null` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::len` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::map_addr` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::offset_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::offset_from_unsigned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::read` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::read_unaligned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::read_volatile` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::replace` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::slice_from_raw_parts` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::slice_from_raw_parts_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::swap` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::swap_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::with_addr` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::with_exposed_provenance` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::with_exposed_provenance_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::without_provenance` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::without_provenance_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_add` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::wrapping_byte_add` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_byte_offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::wrapping_byte_sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::wrapping_offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::write` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::write_bytes` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::write_unaligned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::write_volatile` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::result::Result::and` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::and_then` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::as_deref` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection, determinism_unsupported_contract_form |
| `core::result::Result::as_deref_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, deref_mut_result_payload_model_missing |
| `core::result::Result::as_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::result::Result::cloned` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::result::Result::copied` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::result::Result::expect_err` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::flatten` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::inspect` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::inspect_err` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::is_err_and` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::is_ok_and` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::iter` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::result::Result::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::result::Result::map_or` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::map_or_default` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::map_or_else` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::or` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::or_else` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::transpose` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::unwrap_err_unchecked` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::result::Result::unwrap_or` | data_structure | add_spec | 1 | 1 |  |
| `core::result::Result::unwrap_or_default` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::result::Result::unwrap_or_else` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::unwrap_unchecked` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::ChunksExact::remainder` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::slice::ChunksExactMut::into_remainder` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::Iter::as_slice` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `core::slice::IterMut::as_slice` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::slice::IterMut::into_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::RChunksExact::remainder` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::slice::RChunksExactMut::into_remainder` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::align_to` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::align_to_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::slice::array_windows` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::as_array` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::as_chunks` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::as_chunks_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::as_chunks_unchecked` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::as_chunks_unchecked_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::slice::as_flattened` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::as_flattened_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::slice::as_mut_array` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::as_mut_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::as_mut_ptr_range` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::as_ptr_range` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::as_rchunks` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::as_rchunks_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::assume_init_drop` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::assume_init_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::slice::assume_init_ref` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::binary_search` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::binary_search_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract, higher_order_closure_comparator_underdetermined |
| `core::slice::binary_search_by_key` | data_structure | skip | 0 | 0 | classification:higher_order_contract, higher_order_closure_key_extraction_underdetermined |
| `core::slice::chunk_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::chunk_by_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::chunks` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::slice::chunks_exact` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::chunks_exact_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::slice::chunks_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::clone_from_slice` | data_structure | skip | 0 | 0 | clone_semantics_unmodeled |
| `core::slice::contains` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::element_offset` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::ends_with` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::eq_ignore_ascii_case` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::escape_ascii` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::fill` | data_structure | skip | 0 | 0 | clone_semantics_unmodeled |
| `core::slice::fill_with` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::first_chunk` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::first_chunk_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::from_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::from_raw_parts` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::from_raw_parts_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::slice::from_ref` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::get_disjoint_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::slice::get_disjoint_unchecked_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::slice::get_unchecked` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::get_unchecked_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::is_ascii` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::is_sorted` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::is_sorted_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::slice::is_sorted_by_key` | data_structure | skip | 0 | 0 | classification:higher_order_contract, higher_order_closure_key_extraction_underdetermined |
| `core::slice::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::last_chunk` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::last_chunk_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::make_ascii_lowercase` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::make_ascii_uppercase` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::partition_point` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::slice::rchunks` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::slice::rchunks_exact` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks_exact_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::reverse` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::rotate_left` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::rotate_right` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::rsplit` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplit_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplitn` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplitn_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::select_nth_unstable` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, permitted_partition_order_underdetermined |
| `core::slice::select_nth_unstable_by` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, permitted_partition_order_underdetermined |
| `core::slice::select_nth_unstable_by_key` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, permitted_partition_order_underdetermined |
| `core::slice::sort_unstable` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `core::slice::sort_unstable_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::sort_unstable_by_key` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::split` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::split_at_checked` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_at_mut_checked` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_at_mut_unchecked` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_at_unchecked` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::split_first` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_first_chunk` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_first_chunk_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_first_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_inclusive` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::split_inclusive_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::split_last` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_last_chunk` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_last_chunk_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_last_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::slice::split_off` | data_structure | skip | 0 | 0 | one_sided_range_split_point_underdetermined, direction_choice_not_modeled |
| `core::slice::split_off_first` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_off_first_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_off_last` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::split_off_last_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::split_off_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::slice::splitn` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::splitn_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::starts_with` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::strip_circumfix` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::strip_prefix` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::strip_suffix` | data_structure | skip | 0 | 0 | generic_slice_pattern_model_gap |
| `core::slice::subslice_range` | data_structure | skip | 0 | 0 | pointer_address_or_provenance_model_gap |
| `core::slice::swap` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::swap_with_slice` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::trim_ascii` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::trim_ascii_end` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::trim_ascii_start` | data_structure | add_spec | 1 | 1 |  |
| `core::slice::utf8_chunks` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::windows` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::write_clone_of_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::slice::write_copy_of_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::str::CharIndices::as_str` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::CharIndices::offset` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::Chars::as_str` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `core::str::FromStr::from_str` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `core::str::Utf8Chunk::invalid` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `core::str::Utf8Chunk::valid` | data_structure | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::Utf8Error::error_len` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::str::Utf8Error::valid_up_to` | data_structure | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::str::as_bytes_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::str::as_mut_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::str::bytes` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::str::ceil_char_boundary` | data_structure | add_spec | 1 | 1 |  |
| `core::str::char_indices` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::contains` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::encode_utf16` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::ends_with` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::eq_ignore_ascii_case` | data_structure | add_spec | 1 | 1 |  |
| `core::str::escape_debug` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::escape_default` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::escape_unicode` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::find` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::floor_char_boundary` | data_structure | add_spec | 1 | 1 |  |
| `core::str::from_utf8` | data_structure | add_spec | 1 | 1 |  |
| `core::str::from_utf8_mut` | data_structure | add_spec | 1 | 1 |  |
| `core::str::from_utf8_unchecked_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported, determinism_unsupported_contract_form |
| `core::str::get` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::get_unchecked` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::get_unchecked_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::lines` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::lines_any` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::make_ascii_lowercase` | data_structure | add_spec | 1 | 1 |  |
| `core::str::make_ascii_uppercase` | data_structure | add_spec | 1 | 1 |  |
| `core::str::match_indices` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::matches` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::parse` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rfind` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection, generic_pattern_reverse_search_underdetermined |
| `core::str::rmatch_indices` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rmatches` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplit` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplit_once` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection, generic_pattern_reverse_search_underdetermined |
| `core::str::rsplit_terminator` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplitn` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::slice_mut_unchecked` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::slice_unchecked` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::str::split` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_ascii_whitespace` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_at_checked` | data_structure | add_spec | 1 | 1 |  |
| `core::str::split_at_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::split_at_mut_checked` | data_structure | add_spec | 1 | 1 |  |
| `core::str::split_inclusive` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_once` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `core::str::split_terminator` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_whitespace` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::splitn` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::starts_with` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::strip_circumfix` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection, determinism_unsupported_contract_form |
| `core::str::strip_prefix` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::strip_suffix` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `core::str::substr_range` | data_structure | skip | 0 | 0 | determinism_unsupported_contract_form |
| `core::str::trim` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_ascii` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_ascii_end` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_ascii_start` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_end` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_end_matches` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection, determinism_unsupported_contract_form |
| `core::str::trim_left` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_left_matches` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, determinism_unsupported_contract_form |
| `core::str::trim_matches` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection, determinism_unsupported_contract_form |
| `core::str::trim_right` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_right_matches` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection, generic_pattern_suffix_trim_underdetermined |
| `core::str::trim_start` | data_structure | add_spec | 1 | 1 |  |
| `core::str::trim_start_matches` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model, generic_pattern_prefix_trim_underdetermined |
| `core::sync::atomic::Atomic::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::compare_exchange` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::compare_exchange_weak` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_add` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_and` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_byte_add` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_byte_sub` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_max` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_min` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_nand` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_not` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_or` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_ptr_add` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_ptr_sub` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_sub` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_xor` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::Atomic::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::Atomic::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::Atomic::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::load` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::new` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::store` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, no_modeled_observable_output |
| `core::sync::atomic::Atomic::swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::fetch_not` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicBool::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI16::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI16::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI16::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI32::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI64::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI64::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI8::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI8::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicPtr::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::compare_exchange` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::compare_exchange_weak` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicPtr::fetch_and` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_byte_add` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_byte_sub` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_or` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_ptr_add` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_ptr_sub` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_xor` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicPtr::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicPtr::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::load` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::new` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::store` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, no_modeled_observable_output |
| `core::sync::atomic::AtomicPtr::swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU16::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU16::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU16::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU32::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU32::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU64::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU8::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU8::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicUsize::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicUsize::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicUsize::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::compiler_fence` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, no_modeled_observable_output |
| `core::sync::atomic::fence` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, no_modeled_observable_output |
| `core::sync::atomic::spin_loop_hint` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, no_modeled_observable_output |
| `core::time::Duration::abs_diff` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_micros` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_millis` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_nanos` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_secs` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_secs_f32` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_secs_f64` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::checked_add` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::checked_div` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::checked_mul` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::checked_sub` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::div_duration_f32` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::div_duration_f64` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::div_f32` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::div_f64` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_hours` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_micros` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_millis` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_mins` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_nanos` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_nanos_u128` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_secs` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_secs_f32` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_secs_f64` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::is_zero` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::mul_f32` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::mul_f64` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::new` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::saturating_add` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::saturating_mul` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::saturating_sub` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::subsec_micros` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::subsec_millis` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::subsec_nanos` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::try_from_secs_f32` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::try_from_secs_f64` | other | skip | 0 | 0 | duplicate_vstd_assume_specification |
| `std::collections::HashMap::capacity` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashMap::drain` | other | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `std::collections::HashMap::extract_if` | other | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `std::collections::HashMap::get_disjoint_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported, hashmap_get_disjoint_mut_reference_array_model_missing |
| `std::collections::HashMap::get_disjoint_unchecked_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::collections::HashMap::get_key_value` | other | skip | 0 | 0 | determinism_unsupported_contract_form |
| `std::collections::HashMap::get_mut` | other | add_spec | 1 | 1 |  |
| `std::collections::HashMap::hasher` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashMap::into_keys` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::into_values` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::iter_mut` | other | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `std::collections::HashMap::remove_entry` | other | add_spec | 1 | 1 |  |
| `std::collections::HashMap::retain` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::shrink_to` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashMap::shrink_to_fit` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashMap::try_reserve` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashMap::values_mut` | other | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `std::collections::HashMap::with_capacity_and_hasher` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashMap::with_hasher` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashSet::capacity` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashSet::difference` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::drain` | other | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `std::collections::HashSet::extract_if` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::hasher` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashSet::intersection` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::is_disjoint` | other | add_spec | 1 | 1 |  |
| `std::collections::HashSet::is_subset` | other | add_spec | 1 | 1 |  |
| `std::collections::HashSet::is_superset` | other | add_spec | 1 | 1 |  |
| `std::collections::HashSet::replace` | other | add_spec | 1 | 1 |  |
| `std::collections::HashSet::retain` | other | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `std::collections::HashSet::shrink_to` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashSet::shrink_to_fit` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashSet::symmetric_difference` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::take` | other | skip | 0 | 0 | determinism_unsupported_contract_form |
| `std::collections::HashSet::try_reserve` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashSet::union` | other | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `std::collections::HashSet::with_capacity_and_hasher` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashSet::with_hasher` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::env::args` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::args_os` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::current_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::current_exe` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::home_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::join_paths` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::remove_var` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::env::set_current_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::set_var` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::env::split_paths` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::temp_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::var` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::var_os` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::vars` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::vars_os` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::ffi::OsStr::as_encoded_bytes` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::display` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::eq_ignore_ascii_case` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::from_encoded_bytes_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `std::ffi::OsStr::into_os_string` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::is_ascii` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::is_empty` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::len` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::make_ascii_lowercase` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::make_ascii_uppercase` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::new` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::to_ascii_lowercase` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::to_ascii_uppercase` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::to_os_string` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::to_str` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::to_string_lossy` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::as_os_str` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::capacity` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::clear` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::from_encoded_bytes_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `std::ffi::OsString::into_boxed_os_str` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::into_encoded_bytes` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::into_string` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::leak` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::ffi::OsString::new` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::push` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::reserve` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::reserve_exact` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::shrink_to` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::shrink_to_fit` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::try_reserve` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::try_reserve_exact` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::with_capacity` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::fs::DirBuilder::create` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirBuilder::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirBuilder::recursive` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::file_name` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::file_type` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::metadata` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::path` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::create` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::create_new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::lock_shared` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::metadata` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::open` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::options` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_len` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_modified` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_permissions` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_times` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::sync_all` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::sync_data` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::try_lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::try_lock_shared` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::unlock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileTimes::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileTimes::set_accessed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileTimes::set_modified` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileType::is_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileType::is_file` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileType::is_symlink` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::accessed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::created` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::file_type` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::is_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::is_file` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::is_symlink` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::len` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::modified` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::permissions` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::append` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::create` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::create_new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::open` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::read` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::truncate` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::write` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Permissions::readonly` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Permissions::set_readonly` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::canonicalize` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::copy` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::create_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::create_dir_all` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::exists` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::hard_link` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::metadata` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read_link` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read_to_string` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::remove_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::remove_dir_all` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::remove_file` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::rename` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::set_permissions` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::soft_link` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::symlink_metadata` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::write` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufRead::consume` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::BufRead::fill_buf` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::BufRead::lines` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::BufRead::read_line` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::BufRead::read_until` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::BufRead::skip_until` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::BufRead::split` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::BufReader::buffer` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::capacity` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::get_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::seek_relative` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::with_capacity` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::buffer` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::capacity` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::get_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::into_parts` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::with_capacity` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::into_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::into_parts` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IsTerminal::is_terminal` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::LineWriter::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::get_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::with_capacity` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::PipeReader::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::PipeWriter::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Read::by_ref` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Read::bytes` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Read::chain` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Read::read` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Read::read_exact` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Read::read_to_end` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Read::read_to_string` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Read::read_vectored` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Read::take` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Stderr::lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::lines` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::read_line` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdout::lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Write::by_ref` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Write::flush` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Write::write` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Write::write_all` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Write::write_fmt` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::Write::write_vectored` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::io::WriterPanicked::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::copy` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::pipe` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::read_to_string` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::stderr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::stdin` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::stdout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::accept` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::bind` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::incoming` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::only_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::set_only_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::set_ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::connect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::connect_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::net::TcpStream::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::nodelay` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::peek` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::net::TcpStream::peer_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_nodelay` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::shutdown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::ToSocketAddrs::to_socket_addrs` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::net::UdpSocket::bind` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::broadcast` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::connect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::join_multicast_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::join_multicast_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::leave_multicast_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::leave_multicast_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::multicast_loop_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::multicast_loop_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::multicast_ttl_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::peek` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::net::UdpSocket::peek_from` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::peer_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::recv` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::recv_from` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::send` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::send_to` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_broadcast` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_multicast_loop_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_multicast_loop_v6` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_multicast_ttl_v4` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::ttl` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::AsFd::as_fd` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::fd::AsRawFd::as_raw_fd` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::fd::BorrowedFd::borrow_raw` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::BorrowedFd::try_clone_to_owned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::FromRawFd::from_raw_fd` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::fd::IntoRawFd::into_raw_fd` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::fd::OwnedFd::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::ffi::OsStrExt::as_bytes` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::ffi::OsStrExt::from_bytes` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::ffi::OsStringExt::from_vec` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::ffi::OsStringExt::into_vec` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::DirBuilderExt::mode` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::DirEntryExt::ino` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::FileExt::read_at` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::FileExt::read_exact_at` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::FileExt::write_all_at` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::FileExt::write_at` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::FileTypeExt::is_block_device` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::FileTypeExt::is_char_device` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::FileTypeExt::is_fifo` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::FileTypeExt::is_socket` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::atime` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::atime_nsec` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::blksize` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::blocks` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::ctime` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::ctime_nsec` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::dev` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::gid` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::ino` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::mode` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::mtime` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::mtime_nsec` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::nlink` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::rdev` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::size` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::uid` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::OpenOptionsExt::custom_flags` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::OpenOptionsExt::mode` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::PermissionsExt::from_mode` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::PermissionsExt::mode` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::PermissionsExt::set_mode` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::unix::fs::chown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::chroot` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::fchown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::lchown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::symlink` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::SocketAddr::as_pathname` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::SocketAddr::from_pathname` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::SocketAddr::is_unnamed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::bind` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::bind_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::connect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::connect_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::pair` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::peer_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::recv` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::recv_from` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::send` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::os::unix::net::UnixDatagram::send_to` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::send_to_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::os::unix::net::UnixDatagram::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::set_read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::set_write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::os::unix::net::UnixDatagram::shutdown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::unbound` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::accept` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::bind` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::bind_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::incoming` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::connect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::connect_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::local_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::pair` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::peer_addr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::set_nonblocking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::set_read_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::set_write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::shutdown` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::take_error` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::write_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::ffi::OsStrExt::encode_wide` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::ffi::OsStringExt::from_wide` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::FileExt::seek_read` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::FileExt::seek_write` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::FileTimesExt::set_created` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::FileTypeExt::is_symlink_dir` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::FileTypeExt::is_symlink_file` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::MetadataExt::creation_time` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::MetadataExt::file_attributes` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::MetadataExt::file_size` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::MetadataExt::last_access_time` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::MetadataExt::last_write_time` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::OpenOptionsExt::access_mode` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::OpenOptionsExt::attributes` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::OpenOptionsExt::custom_flags` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::OpenOptionsExt::security_qos_flags` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::OpenOptionsExt::share_mode` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::fs::symlink_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::fs::symlink_file` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::AsHandle::as_handle` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::io::AsRawHandle::as_raw_handle` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::io::AsRawSocket::as_raw_socket` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::io::AsSocket::as_socket` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::io::BorrowedHandle::borrow_raw` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedHandle::try_clone_to_owned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedSocket::borrow_raw` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedSocket::try_clone_to_owned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::FromRawHandle::from_raw_handle` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::io::FromRawSocket::from_raw_socket` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::io::HandleOrInvalid::from_raw_handle` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::HandleOrNull::from_raw_handle` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::IntoRawHandle::into_raw_handle` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::io::IntoRawSocket::into_raw_socket` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::os::windows::io::OwnedHandle::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::OwnedSocket::try_clone` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::panic::PanicHookInfo::location` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, panic_location_abstraction_missing |
| `std::panic::PanicHookInfo::payload` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicHookInfo::payload_as_str` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicInfo::location` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, panic_location_abstraction_missing |
| `std::panic::PanicInfo::payload` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicInfo::payload_as_str` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::catch_unwind` | other | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `std::panic::panic_any` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::resume_unwind` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `std::panic::set_hook` | other | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `std::panic::take_hook` | other | skip | 0 | 0 | classification:higher_order_contract |
| `std::path::Component::as_os_str` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Components::as_path` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Iter::as_path` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::ancestors` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::as_mut_os_str` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::Path::as_os_str` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::canonicalize` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::components` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::display` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::ends_with` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::exists` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::extension` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::file_name` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::file_prefix` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::file_stem` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::has_root` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::into_path_buf` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_absolute` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_dir` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_empty` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `std::path::Path::is_file` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_relative` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_symlink` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::iter` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::path::Path::join` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::metadata` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::new` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::parent` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::read_dir` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::read_link` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::starts_with` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::strip_prefix` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::symlink_metadata` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::to_path_buf` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::to_str` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::to_string_lossy` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::try_exists` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::with_added_extension` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::with_extension` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::with_file_name` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::add_extension` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::as_mut_os_string` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::PathBuf::as_path` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::capacity` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::clear` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::into_boxed_path` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::into_os_string` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::into_string` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `std::path::PathBuf::leak` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::PathBuf::new` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::pop` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `std::path::PathBuf::push` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::reserve` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::reserve_exact` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::set_extension` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `std::path::PathBuf::set_file_name` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::shrink_to` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::shrink_to_fit` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::try_reserve` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::try_reserve_exact` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::with_capacity` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::Prefix::is_verbatim` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PrefixComponent::as_os_str` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PrefixComponent::kind` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::absolute` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::is_separator` | other | skip | 0 | 0 | classification:needs_new_vstd_abstraction, determinism_unsupported_contract_form |
| `std::process::Child::id` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::kill` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::try_wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::process::Child::wait_with_output` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::arg` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::args` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::current_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::process::Command::env` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::env_clear` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::env_remove` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::envs` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::process::Command::get_args` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::get_current_dir` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::get_envs` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::get_program` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::output` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::spawn` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::status` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::stderr` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::stdin` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::stdout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::ExitStatus::code` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::ExitStatus::success` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Stdio::inherit` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Stdio::null` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Stdio::piped` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Termination::report` | trait_method | skip | 0 | 0 | classification:trait_contract_integration, determinism_unsupported_contract_form |
| `std::process::abort` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::exit` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::id` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Barrier::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Barrier::wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::BarrierWaitResult::is_leader` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::notify_all` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Condvar::notify_one` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Condvar::wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_timeout_ms` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_timeout_while` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_while` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::force` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::force_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::get` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::and_then` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::as_deref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::as_deref_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::as_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::as_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::cloned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::copied` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, duplicate_vstd_assume_specification |
| `std::sync::LockResult::expect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::expect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::flatten` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::inspect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::inspect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, duplicate_vstd_assume_specification |
| `std::sync::LockResult::is_err_and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, duplicate_vstd_assume_specification |
| `std::sync::LockResult::is_ok_and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::iter` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::iter_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::map_or_default` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, duplicate_vstd_assume_specification |
| `std::sync::LockResult::or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::transpose` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::unwrap_err_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::unwrap_or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_or_default` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::Mutex::clear_poison` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Mutex::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::is_poisoned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::try_lock` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Once::call_once` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Once::call_once_force` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Once::is_completed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Once::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Once::wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::Once::wait_force` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::OnceLock::get` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::get_or_init` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::set` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::OnceLock::take` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::wait` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceState::is_poisoned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::get_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::clear_poison` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::sync::RwLock::get_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::into_inner` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::is_poisoned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::read` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::try_read` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::try_write` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::write` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLockWriteGuard::downgrade` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::and_then` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::as_deref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::as_deref_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::as_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::as_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::cloned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::copied` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::expect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::expect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::flatten` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::inspect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::inspect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::is_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::is_err_and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::is_ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::is_ok_and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::iter` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::iter_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::map_or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map_or_default` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map_or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, duplicate_vstd_assume_specification |
| `std::sync::TryLockResult::or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::transpose` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::unwrap` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::unwrap_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_err_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_or_default` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::WaitTimeoutResult::timed_out` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::iter` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::recv` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::recv_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::try_iter` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::try_recv` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Sender::send` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::sync::mpsc::SyncSender::send` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::SyncSender::try_send` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::channel` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::sync_channel` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::name` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::new` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::spawn` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::spawn_scoped` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::spawn_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::stack_size` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::JoinHandle::is_finished` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::JoinHandle::join` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::JoinHandle::thread` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::get` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::replace` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::set` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::LocalKey::take` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::try_with` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::update` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::LocalKey::with` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::with_borrow` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::with_borrow_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::and_then` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::as_deref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::as_deref_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::as_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::as_ref` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::cloned` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::copied` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, duplicate_vstd_assume_specification |
| `std::thread::Result::expect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::expect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::flatten` | io_os_runtime | add_spec | 1 | 1 |  |
| `std::thread::Result::inspect` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::inspect_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::is_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, duplicate_vstd_assume_specification |
| `std::thread::Result::is_err_and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::is_ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, duplicate_vstd_assume_specification |
| `std::thread::Result::is_ok_and` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::iter` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::iter_mut` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::map_or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_or_default` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::ok` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, duplicate_vstd_assume_specification |
| `std::thread::Result::or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::transpose` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::unwrap` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::unwrap_err` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, duplicate_vstd_assume_specification |
| `std::thread::Result::unwrap_err_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::unwrap_or` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::unwrap_or_default` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::unwrap_or_else` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Result::unwrap_unchecked` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::Scope::spawn` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::is_finished` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::join` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::thread` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::id` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::name` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::unpark` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::available_parallelism` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::thread::current` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::panicking` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::park` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::park_timeout` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::park_timeout_ms` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::scope` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::sleep` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::sleep_ms` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::thread::spawn` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::yield_now` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, no_modeled_observable_output |
| `std::time::Instant::checked_add` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::checked_duration_since` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::checked_sub` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::duration_since` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::elapsed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::now` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::saturating_duration_since` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::checked_add` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::checked_sub` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state, determinism_unsupported_contract_form |
| `std::time::SystemTime::duration_since` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::elapsed` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::now` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTimeError::duration` | io_os_runtime | skip | 0 | 0 | classification:runtime_or_hidden_state |
