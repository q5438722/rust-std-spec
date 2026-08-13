# Generated B16 submission subset

## Scope

This subset retains original B20 positions **1-15 and 17**. It contains only
generated contracts and deliberately excludes the two mutable-field invariant
cases and the two checked-split cases that transitively depend on
`from_raw_parts`.

The copied proof bundle is:

```text
submission_candidates/B16_LOW_BOUNDARY_SUBSET/proof_harnesses/
```

The submission-ready contracts and their minimal shared-helper closure are:

```text
submission_candidates/B16_LOW_BOUNDARY_SUBSET/specs/
```

Each copied target directory contains its complete original harness contents:
the executable `harness.rs`, frozen `source_excerpt.rs`, Verus evidence, helper
source excerpts, and `original_implementation.rs` where the implementation was
mechanically adapted.

## Selected targets

| New # | Original B20 # | Target | Verus result | Copied directory |
| ---: | ---: | --- | --- | --- |
| 1 | 1 | `core::slice::split_first` | 1 verified, 0 errors | `088_core_slice_split_first/` |
| 2 | 2 | `core::slice::split_off_first` | 2 verified, 0 errors | `100_core_slice_split_off_first/` |
| 3 | 3 | `core::slice::split_last` | 1 verified, 0 errors | `094_core_slice_split_last/` |
| 4 | 4 | `core::slice::split_off_last` | 2 verified, 0 errors | `102_core_slice_split_off_last/` |
| 5 | 5 | `core::slice::split_first_mut` | 1 verified, 0 errors | `091_core_slice_split_first_mut/` |
| 6 | 6 | `core::slice::split_last_mut` | 1 verified, 0 errors | `097_core_slice_split_last_mut/` |
| 7 | 7 | `core::slice::chunks_exact` | 2 verified, 0 errors | `034_core_slice_chunks_exact/` |
| 8 | 8 | `core::slice::rchunks_exact` | 2 verified, 0 errors | `067_core_slice_rchunks_exact/` |
| 9 | 9 | `core::slice::trim_ascii_start` | 6 verified, 0 errors | `116_core_slice_trim_ascii_start/` |
| 10 | 10 | `core::slice::trim_ascii_end` | 6 verified, 0 errors | `115_core_slice_trim_ascii_end/` |
| 11 | 11 | `core::slice::make_ascii_lowercase` | 8 verified, 0 errors | `063_core_slice_make_ascii_lowercase/` |
| 12 | 12 | `core::slice::make_ascii_uppercase` | 8 verified, 0 errors | `064_core_slice_make_ascii_uppercase/` |
| 13 | 13 | `core::slice::split_off_first_mut` | 1 verified, 0 errors | `101_core_slice_split_off_first_mut/` |
| 14 | 14 | `core::slice::split_off_last_mut` | 1 verified, 0 errors | `103_core_slice_split_off_last_mut/` |
| 15 | 15 | `core::slice::ChunksExact::remainder` | 1 verified, 0 errors | `001_core_slice_ChunksExact_remainder/` |
| 16 | 17 | `core::slice::RChunksExact::remainder` | 1 verified, 0 errors | `006_core_slice_RChunksExact_remainder/` |

## Verification properties

- All 16 rows are generated contracts with current B dispositions.
- Every copied target has an actual Verus result matching
  `verification results:: N verified, 0 errors`, with `N > 0`.
- None of the 16 copied `harness.rs` files contains
  `#[verifier::external_body]`.
- The copied bundle contains 16 target directories and 139 files.
- `specs/generated_slice_specs.rs` contains exactly 16 declarations selected
  from the active Slice specs, and `specs/slice_shared_vocabulary.rs` contains
  their 20 directly or transitively required helpers.
- The source-subset audit reports no missing, extra, or mismatched contracts or
  helpers.
- The merged specs entry point passes Verus `--no-verify` typechecking on the
  Rust 1.96 toolchain.

## Remaining boundary families

After excluding verified model/helper definitions and discharged preconditions,
the subset uses 10 distinct boundary or mechanical interfaces, referenced 22
times:

1. immutable slice-pattern desugaring;
2. mutable slice-pattern desugaring;
3. `mem::replace` swap-with-empty lowering;
4. `u8` ASCII range-pattern desugaring;
5. `u8::is_ascii_whitespace`;
6. trim-start first/rest pattern lowering;
7. trim-end rest/last pattern lowering;
8. reviewed valid-index `<[T]>::split_at`;
9. `ChunksExact::invariant`; and
10. `RChunksExact::invariant`.

The exact-chunk private constructors are included and verified in their
respective harnesses. The lowercase/uppercase byte helper chains and both
trim-index uniqueness lemmas are also verified rather than externalized.

## Excluded original B20 rows

| Original # | Target | Exclusion reason |
| ---: | --- | --- |
| 16 | `ChunksExactMut::into_remainder` | Moving an `&mut [T]` field out of an invariant-bearing struct currently needs a trusted private invariant lemma |
| 18 | `RChunksExactMut::into_remainder` | Same mutable-field/type-invariant limitation |
| 19 | `split_at_checked` | Reuses `split_at_unchecked`, whose lower-level proof still depends on raw-pointer/`from_raw_parts` semantics |
| 20 | `split_at_mut_checked` | Mutable unchecked split transitively depends on raw-pointer construction, aliasing, and final-frame boundaries |
