# B16 submission specifications

This directory follows the layout of the module-first `core::slice` specs:

- `slice_shared_vocabulary.rs`: the transitive spec-helper closure used by the
  selected contracts;
- `generated_slice_specs.rs`: the 16 generated `assume_specification`
  declarations;
- `existing_vstd_slice_specs.rs`: intentionally empty because this submission
  subset excludes existing-vstd contracts; and
- `all_slice_specs.rs`: the merged submission entry point.

The corresponding implementation proofs and Verus evidence are in
`../proof_harnesses/`.

The 16 declarations are:

1. `<[T]>::split_first`
2. `<[T]>::split_off_first`
3. `<[T]>::split_last`
4. `<[T]>::split_off_last`
5. `<[T]>::split_first_mut`
6. `<[T]>::split_last_mut`
7. `<[T]>::chunks_exact`
8. `<[T]>::rchunks_exact`
9. `<[u8]>::trim_ascii_start`
10. `<[u8]>::trim_ascii_end`
11. `<[u8]>::make_ascii_lowercase`
12. `<[u8]>::make_ascii_uppercase`
13. `<[T]>::split_off_first_mut`
14. `<[T]>::split_off_last_mut`
15. `core::slice::ChunksExact::remainder`
16. `core::slice::RChunksExact::remainder`

The contract text and helper definitions were selected from the active
module-first Slice artifacts:

- `nanvix-rust-std-slice-specgen-2026-08-11/specs/generated_slice_specs.rs`
- `nanvix-rust-std-slice-specgen-2026-08-11/specs/slice_shared_vocabulary.rs`

`ExChunksExact` and `ExRChunksExact` retain Verus external type
specifications. These model Rust standard-library iterator types; they are not
external bodies for any of the 16 target implementations.
