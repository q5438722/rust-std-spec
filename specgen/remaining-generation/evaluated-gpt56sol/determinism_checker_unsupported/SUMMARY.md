# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 109
- Add-spec decisions: 0
- Skip decisions: 109
- Static skips: 0
- Raw determinism reward: 0
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::borrow::Cow::to_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::boxed::Box::leak` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::BTreeMap::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::LinkedList::back_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::LinkedList::front_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::LinkedList::push_back_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::LinkedList::push_front_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::as_mut_slices` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::back_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::front_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::insert_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::make_contiguous` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::push_back_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::push_front_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_default` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_insert` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_insert_with` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_insert_with_key` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::OccupiedEntry::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::OccupiedEntry::into_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::VacantEntry::insert` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::rc::Rc::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::rc::Rc::make_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::string::String::as_mut_str` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::string::String::as_mut_vec` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::string::String::leak` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::sync::Arc::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::sync::Arc::make_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::IntoIter::as_mut_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::Vec::insert_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::Vec::leak` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::Vec::push_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::Vec::spare_capacity_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::array::IntoIter::as_mut_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::array::as_mut_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::array::each_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::array::from_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::Cell::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::LazyCell::force_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::LazyCell::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::OnceCell::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::RefCell::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::UnsafeCell::from_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::UnsafeCell::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::iter::Peekable::peek_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::mem::MaybeUninit::write` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::option::Option::as_deref_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::option::Option::as_pin_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::option::Option::get_or_insert_default` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::option::Option::get_or_insert_with` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::as_deref_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::as_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::get_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::get_unchecked_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::map_unchecked_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::static_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::ptr::NonNull::as_mut` | memory_pointer | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::ptr::as_mut` | memory_pointer | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::ptr::as_mut_unchecked` | memory_pointer | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::result::Result::as_deref_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::result::Result::as_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::ChunksExactMut::into_remainder` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::IterMut::into_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::RChunksExactMut::into_remainder` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::align_to_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::as_chunks_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::as_chunks_unchecked_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::as_flattened_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::as_mut_array` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::as_rchunks_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::assume_init_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::first_chunk_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::from_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::from_raw_parts_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::get_disjoint_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::get_disjoint_unchecked_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::get_unchecked_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::last_chunk_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::select_nth_unstable` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::select_nth_unstable_by` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::select_nth_unstable_by_key` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_at_mut_checked` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_at_mut_unchecked` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_first_chunk_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_first_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_last_chunk_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_last_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_off_first_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_off_last_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_off_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::write_clone_of_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::write_copy_of_slice` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::as_bytes_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::from_utf8_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::from_utf8_unchecked_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::get_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::get_unchecked_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::slice_mut_unchecked` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::split_at_mut` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::split_at_mut_checked` | data_structure | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::collections::HashMap::get_disjoint_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::collections::HashMap::get_disjoint_unchecked_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::collections::HashMap::get_mut` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::ffi::OsString::leak` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::Path::as_mut_os_str` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::PathBuf::as_mut_os_string` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::PathBuf::leak` | other | skip | 0 | 0 | classification:determinism_checker_unsupported |
