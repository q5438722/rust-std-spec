# alloc::vec executable API inventory

Frozen authority: local copies of `/home/chentianyu/nanvix-rust-std-spec-survey/results/modules.csv` and `coverage.csv` in `results/`.

## Scope counts

- Stable unique executable APIs: 49
- Exact existing-vstd stable APIs: 24
- Stable uncovered APIs requiring a new executable declaration or justified no-spec record: 25
- Excluded unstable APIs: 28

`modules.csv` row confirms `stable_unique_api_paths=49`, `covered_stable_unique_api_paths=24`, and `uncovered_stable_unique_api_paths=25`. `coverage.csv` contributes the exact stable target set and the 28 unstable exclusions.

## Existing vstd exact-match subtraction

Each covered stable row was checked against a real copied vstd `assume_specification` target binding in `vstd-baseline/std_specs/{vec,capacity}.rs`, with source receiver/reference mutability, extra parameters, return shape, and required generic bounds compared to the copied Rust 1.96 source signature.

- `alloc::vec::Vec::append` -> `std_specs/vec.rs:154` (exact-existing-vstd)
- `alloc::vec::Vec::as_mut_slice` -> `std_specs/vec.rs:242` (exact-existing-vstd)
- `alloc::vec::Vec::as_slice` -> `std_specs/vec.rs:236` (exact-existing-vstd)
- `alloc::vec::Vec::capacity` -> `std_specs/capacity.rs:37` (exact-existing-vstd)
- `alloc::vec::Vec::clear` -> `std_specs/vec.rs:231` (exact-existing-vstd)
- `alloc::vec::Vec::extend_from_slice` -> `std_specs/vec.rs:163` (exact-existing-vstd)
- `alloc::vec::Vec::insert` -> `std_specs/vec.rs:203` (exact-existing-vstd)
- `alloc::vec::Vec::is_empty` -> `std_specs/vec.rs:214` (exact-existing-vstd)
- `alloc::vec::Vec::len` -> `std_specs/vec.rs:93` (exact-existing-vstd)
- `alloc::vec::Vec::new` -> `std_specs/vec.rs:100` (exact-existing-vstd)
- `alloc::vec::Vec::pop` -> `std_specs/vec.rs:146` (exact-existing-vstd)
- `alloc::vec::Vec::push` -> `std_specs/vec.rs:141` (exact-existing-vstd)
- `alloc::vec::Vec::remove` -> `std_specs/vec.rs:220` (exact-existing-vstd)
- `alloc::vec::Vec::reserve` -> `std_specs/vec.rs:125` (exact-existing-vstd)
- `alloc::vec::Vec::reserve_exact` -> `std_specs/capacity.rs:42` (exact-existing-vstd)
- `alloc::vec::Vec::resize` -> `std_specs/vec.rs:306` (exact-existing-vstd)
- `alloc::vec::Vec::shrink_to` -> `std_specs/capacity.rs:67` (exact-existing-vstd)
- `alloc::vec::Vec::shrink_to_fit` -> `std_specs/capacity.rs:60` (exact-existing-vstd)
- `alloc::vec::Vec::split_off` -> `std_specs/vec.rs:263` (exact-existing-vstd)
- `alloc::vec::Vec::swap_remove` -> `std_specs/vec.rs:192` (exact-existing-vstd)
- `alloc::vec::Vec::truncate` -> `std_specs/vec.rs:300` (exact-existing-vstd)
- `alloc::vec::Vec::try_reserve` -> `std_specs/vec.rs:133` (exact-existing-vstd)
- `alloc::vec::Vec::try_reserve_exact` -> `std_specs/capacity.rs:51` (exact-existing-vstd)
- `alloc::vec::Vec::with_capacity` -> `std_specs/vec.rs:115` (exact-existing-vstd)

## Uncovered stable rows

- `alloc::vec::Drain::as_slice` — vec-iterator-adaptor-state
- `alloc::vec::IntoIter::as_mut_slice` — vec-iterator-adaptor-state
- `alloc::vec::IntoIter::as_slice` — vec-iterator-adaptor-state
- `alloc::vec::Vec::as_mut_ptr` — vec-raw-parts-pointer-provenance
- `alloc::vec::Vec::as_ptr` — vec-raw-parts-pointer-provenance
- `alloc::vec::Vec::dedup` — vec-callback-trace-mutation
- `alloc::vec::Vec::dedup_by` — vec-callback-trace-mutation
- `alloc::vec::Vec::dedup_by_key` — vec-callback-trace-mutation
- `alloc::vec::Vec::drain` — vec-iterator-adaptor-state
- `alloc::vec::Vec::extend_from_within` — vec-sequence-mutation
- `alloc::vec::Vec::extract_if` — vec-iterator-adaptor-state
- `alloc::vec::Vec::from_raw_parts` — vec-raw-parts-pointer-provenance
- `alloc::vec::Vec::insert_mut` — vec-sequence-mutation
- `alloc::vec::Vec::into_boxed_slice` — vec-slice-boxed-slice-conversion
- `alloc::vec::Vec::into_flattened` — vec-sequence-mutation
- `alloc::vec::Vec::into_raw_parts` — vec-raw-parts-pointer-provenance
- `alloc::vec::Vec::leak` — vec-slice-boxed-slice-conversion
- `alloc::vec::Vec::pop_if` — vec-callback-trace-mutation
- `alloc::vec::Vec::push_mut` — vec-sequence-mutation
- `alloc::vec::Vec::resize_with` — vec-callback-trace-mutation
- `alloc::vec::Vec::retain` — vec-callback-trace-mutation
- `alloc::vec::Vec::retain_mut` — vec-callback-trace-mutation
- `alloc::vec::Vec::set_len` — vec-raw-parts-pointer-provenance
- `alloc::vec::Vec::spare_capacity_mut` — vec-spare-capacity-maybeuninit-storage
- `alloc::vec::Vec::splice` — vec-iterator-adaptor-state
