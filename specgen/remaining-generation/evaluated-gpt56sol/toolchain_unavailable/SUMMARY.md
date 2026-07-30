# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 70
- Add-spec decisions: 0
- Skip decisions: 70
- Static skips: 0
- Raw determinism reward: 0
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::boxed::BoxedArrayIntoIter::as_mut_slice` | data_structure | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
| `alloc::boxed::BoxedArrayIntoIter::as_slice` | data_structure | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
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
| `core::io::Result::map_err` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
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
| `std::path::PathBuf::into_string` | other | skip | 0 | 0 | classification:toolchain_unavailable, no_modeled_observable_output, not_in_verus_rust_1_96 |
