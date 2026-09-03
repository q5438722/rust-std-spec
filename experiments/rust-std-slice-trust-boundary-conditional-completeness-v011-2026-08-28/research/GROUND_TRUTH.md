# Active Slice UNKNOWN ground truth

This package freezes and joins the active working-tree authorities. No target
count or target list is used as selection authority.

## Scope derivation

- active feedback run: `all-20260815T0127Z-ascii-whitespace-vtab-repair`
- active feedback rows: 120
- generated catalog rows: 120
- active `r0_z3=unknown` generated rows selected: 62
- active `r0_z3=unsat` generated rows excluded: 58
- exact-vstd catalog rows excluded: 12
- catalog rows in total: 132
- selected namespaces: `core::slice` only
- Vec, Array, Option, String, old UNSAT rows, exact-vstd rows, and every
  non-Slice family are absent from the selected set.

The active feedback target set equals the 120 generated catalog targets. Every
selected implementation-proof row has `module=slice` and `abcd_status=B`.

## Selected reason classes

- `clone-or-callback-effect-boundary`: 2
- `disjoint-mutable-alias-boundary`: 2
- `duplicate-or-callback-search-boundary`: 4
- `iterator-or-subslice-state-boundary`: 24
- `maybeuninit-storage-boundary`: 4
- `mutable-reference-view-boundary`: 7
- `raw-pointer-provenance-boundary`: 13
- `unstable-sort-or-selection-boundary`: 6

## Active-over-retained contract reconciliation

The active catalog and executable generated declaration control. Exactly six
selected retained proof contracts differ:

- `core::slice::as_chunks`: active `9d7c778009f44f0fd043dfc0e22215c99b3c90dde9ed5434c911087402bbe05f`, retained `3b57534adcd1c2d3cf18052a45f2e11ea9dfc2889dcef6ab4586a35bc8501ef9`
- `core::slice::as_chunks_mut`: active `669f8bbc7a27aa64da763386dccd397f1d7e81db22ef7b672e71a40b69ff5e7c`, retained `8c6cc8f88b4de3b1f2c2c1a25965e3744c851cf8ac05d251cc0effd85d0f590e`
- `core::slice::as_chunks_unchecked`: active `a2a5116af11a32d4169f8b90ce1a319e948a4705e36b8a2c171f6a8191655b66`, retained `0d342b93267baa83df2dd43ffee6dcc76c257cf313c3f7d6a0c76f7bd309eab1`
- `core::slice::as_chunks_unchecked_mut`: active `c7cdf29658c01698013e14c2ab14e93699f855167a15eb4e3d697742a7d40c9a`, retained `7cd825e6f6de9150b8a4e29d505fd432ddcb44e1add7c2053c43317a3dcacb0f`
- `core::slice::as_rchunks`: active `1b3b024fdbd8f22771d68cefc3082062544ac60b7d7ac07fda1c14cab04ab3ca`, retained `e2267d28d210517821bbafb80115b79374ff4925b5096b1b27fb466f399a2cec`
- `core::slice::as_rchunks_mut`: active `f7f4347b6b668b99b56a86daa936797fae5b45f6ffc22dbacc872c1be89b2dde`, retained `2eb4482ca836049f0db386dc97308eeb2e7376ffde6abdd110f3691e11c6cf69`

No retained contract is substituted for an active contract.

## Binding and trust-site inventory

- crosswalk rows: 62
- dependency-manifest records expanded: 232
- harnesses containing `external_body`: 43
- `external_body` sites enumerated: 86
- private-helper closure records expanded: 91
- frozen read-only input files: 320

Every row binds the active contract/declaration, canonical Rust item and
preceding public docs, implementation harness, three proof manifests, all
dependency records, private helper closure, and every harness `external_body`.

## Semantic trust-site adjudication

- trust-site records adjudicated: 409
- `external_body` contracts captured in full and source-linked: 86
- previously unlinked `external_body` sites resolved: 14
- exhaustively audited `external_body` sites: 86
- inadmissible complete/answer-equivalent `external_body` sites: 40
- intrinsically answer-equivalent dependency records: 3
- targets with admissible, narrower current boundaries: 28
- targets blocked by an answer-bearing boundary: 34

Every dependency record, source-closure record, and external body carries a
semantic role, disposition, target-postcondition coverage judgment, rationale,
and source citation. The audit enumerates every dependency ID and external
target/symbol pair and is bound to the complete retained inputs by SHA-256; a
new, removed, or changed trust input fails generation instead of becoming
admissible by default. Context-only vocabulary and source-closure records are
not counted as executable boundary observations. `TS-019-D001` and
`TS-021-D001` are intrinsically inadmissible: their synthetic null-provenance
pointer constructors ensure the complete public `as_mut_ptr` and `as_ptr`
postconditions instead of modeling the canonical Rust casts
`self as *mut [T] as *mut T` and `self as *const [T] as *const T`.

The following target boundaries are explicitly inadmissible until their
complete or answer-equivalent helpers are replaced by lower source
transitions:

- `core::slice::align_to`
- `core::slice::align_to_mut`
- `core::slice::as_chunks_unchecked_mut`
- `core::slice::as_flattened_mut`
- `core::slice::as_mut_array`
- `core::slice::as_mut_ptr`
- `core::slice::as_mut_ptr_range`
- `core::slice::as_ptr`
- `core::slice::as_ptr_range`
- `core::slice::assume_init_drop`
- `core::slice::assume_init_mut`
- `core::slice::binary_search`
- `core::slice::binary_search_by_key`
- `core::slice::element_offset`
- `core::slice::first_chunk_mut`
- `core::slice::from_mut`
- `core::slice::from_raw_parts`
- `core::slice::from_raw_parts_mut`
- `core::slice::get_disjoint_mut`
- `core::slice::get_disjoint_unchecked_mut`
- `core::slice::get_mut`
- `core::slice::get_unchecked`
- `core::slice::get_unchecked_mut`
- `core::slice::partition_point`
- `core::slice::select_nth_unstable`
- `core::slice::select_nth_unstable_by`
- `core::slice::select_nth_unstable_by_key`
- `core::slice::sort_unstable`
- `core::slice::sort_unstable_by`
- `core::slice::sort_unstable_by_key`
- `core::slice::split_at_mut_checked`
- `core::slice::split_at_mut_unchecked`
- `core::slice::subslice_range`
- `core::slice::write_copy_of_slice`

Disposition totals:

- `admissible-source-backed-lower-boundary`: 46
- `admissible-source-backed-support`: 144
- `context-only-source-closure`: 91
- `context-only-specification-vocabulary`: 46
- `inadmissible-answer-bearing-support`: 34
- `inadmissible-answer-equivalent-dependency`: 3
- `inadmissible-answer-equivalent-result`: 9
- `inadmissible-complete-branch-postcondition`: 14
- `inadmissible-complete-target-postcondition`: 11
- `inadmissible-opaque-whole-algorithm`: 6
- `mixed-support-includes-answer-bearing-site`: 5

## Authority-stage result neutrality

The authority/design builder does not classify targets: it initializes both
result fields to `not-run`. A separately validated per-target evidence runner
may update only the rows in its explicitly bounded scope.

## Source-backed pointer-cast cluster

The target-local replacements for input orders 019, 021, and 020 bind active
contract hashes
`840c4efc8976016ca0b1c8728d1cabb13529c6e83939e8ca3cbc31232ba6a14a`,
`52c2a91bc8c7e49cd77d4429bb2b2a6e50a788211f2abca511f4df650f1a5edc`,
and
`0d55922a668ea2e52e07ca14a1146f6ff2d0c9a9d68d9369ff4171f9a6d574c1`.
They replace, rather than relabel, synthetic or answer-bearing sites
`TS-019-D001`, `TS-021-D001`, `TS-020-D003`, `TS-020-D004`, and
`TS-020-E001`. `TS-020-D002` is used only as a dependency edge to the
source-backed target-019 cast transition.

The canonical slice casts retain allocation, address, and provenance. Mutable
`ptr::add` computes mathematical `len * size_of::<T>()` with non-null,
alignment, isize-fit, no-wrap, allocation, provenance, one-past, empty-slice,
and ZST conditions. Boundaries contain only initial memory, provenance,
layout, platform, mutable-identity, and frame observations. Outputs and all
modeled final-state observations use exact equality.
