# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 181
- Add-spec decisions: 32
- Skip decisions: 149
- Static skips: 0
- Raw determinism reward: 29
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::alloc::alloc` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::alloc::alloc_zeroed` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::alloc::dealloc` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `alloc::alloc::realloc` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::as_mut_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::assume_init` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::downcast` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::from_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::into_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::ffi::CString::from_raw` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::ffi::CString::from_vec_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::ffi::CString::from_vec_with_nul_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::ffi::CString::into_raw` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::assume_init` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::decrement_strong_count` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `alloc::rc::Rc::from_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::increment_strong_count` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `alloc::rc::Rc::into_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::from_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::into_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::str::from_boxed_utf8_unchecked` | other | add_spec | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_not_proved:unknown |
| `alloc::string::String::from_raw_parts` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::string::String::from_utf8_unchecked` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::string::String::into_raw_parts` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::assume_init` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::decrement_strong_count` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `alloc::sync::Arc::from_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::increment_strong_count` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `alloc::sync::Arc::into_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::from_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::into_raw` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::vec::Vec::as_mut_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::vec::Vec::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::vec::Vec::from_raw_parts` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::vec::Vec::into_raw_parts` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::vec::Vec::set_len` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::alloc::Layout::from_size_align_unchecked` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::Cell::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::RefCell::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::RefCell::try_borrow_unguarded` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::UnsafeCell::get` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::UnsafeCell::raw_get` | data_structure | add_spec | 0 | 0 | checker_status:verus_error, classification:unsafe_or_representation_sensitive, trivial_equal_fn |
| `core::ffi::CStr::as_ptr` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ffi::CStr::from_bytes_with_nul_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ffi::CStr::from_ptr` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::hint::assert_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::intrinsics::copy` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::intrinsics::copy_nonoverlapping` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::intrinsics::transmute` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::intrinsics::write_bytes` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::mem::ManuallyDrop::drop` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::ManuallyDrop::take` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::as_mut_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::mem::MaybeUninit::assume_init_drop` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::assume_init_read` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::transmute_copy` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::uninitialized` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::zeroed` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::option::Option::copied` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::option::Option::unwrap_unchecked` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::into_inner_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::map_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::new_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::add` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::as_ptr` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::as_ref` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_add` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_offset_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_offset_from_unsigned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::copy_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::copy_from_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::copy_to` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::copy_to_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::drop_in_place` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::new` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::new_unchecked` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::offset_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::offset_from_unsigned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read_unaligned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read_volatile` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::replace` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::swap` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::write` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::write_bytes` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::write_unaligned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::NonNull::write_volatile` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::add` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::addr` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::addr_eq` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::align_offset` | memory_pointer | add_spec | 0 | 0 | classification:unsafe_or_representation_sensitive, contract_typecheck_failed |
| `core::ptr::as_array` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::as_mut_array` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::as_ref` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::as_ref_unchecked` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_add` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_offset_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_offset_from_unsigned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::cast` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive, trivial_equal_fn |
| `core::ptr::cast_const` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::cast_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::copy` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::copy_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::copy_from_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::copy_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::copy_to` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::copy_to_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::dangling` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::dangling_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::drop_in_place` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::eq` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::expose_provenance` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::from_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::from_ref` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::hash` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::is_aligned` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::is_empty` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::is_null` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::len` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::map_addr` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive, trivial_equal_fn |
| `core::ptr::offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::offset_from` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::offset_from_unsigned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::read` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::read_unaligned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::read_volatile` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::replace` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::slice_from_raw_parts` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::slice_from_raw_parts_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::swap` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::swap_nonoverlapping` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::with_addr` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::with_exposed_provenance` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::with_exposed_provenance_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::without_provenance` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::without_provenance_mut` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::ptr::wrapping_add` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_byte_add` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive, trivial_equal_fn |
| `core::ptr::wrapping_byte_offset` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_byte_sub` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_offset` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_sub` | memory_pointer | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::write` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::write_bytes` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::write_unaligned` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::ptr::write_volatile` | memory_pointer | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, no_modeled_observable_output |
| `core::result::Result::cloned` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::result::Result::copied` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::result::Result::unwrap_err_unchecked` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::result::Result::unwrap_unchecked` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::align_to` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::as_chunks_unchecked` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::as_mut_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::as_mut_ptr_range` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive, determinism_unsupported_contract_form |
| `core::slice::as_ptr_range` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::assume_init_drop` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::assume_init_ref` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::from_raw_parts` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::get_unchecked` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::split_at_unchecked` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::as_mut_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::as_ptr` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::from_utf8` | data_structure | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::get_unchecked` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::slice_unchecked` | data_structure | add_spec | 1 | 0 | classification:unsafe_or_representation_sensitive |
| `std::ffi::OsStr::from_encoded_bytes_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `std::ffi::OsString::from_encoded_bytes_unchecked` | other | skip | 0 | 0 | classification:unsafe_or_representation_sensitive |
