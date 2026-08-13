# Recommended low-boundary B20 submission subset

## Selection objective

This subset selects 20 generated-contract B-disposition implementation proofs
with:

1. high confidence that the contract captures the source-visible return and
   mutation behavior;
2. actual Verus implementation-proof evidence;
3. no C mismatch;
4. dependency closure inside the subset where practical;
5. a small union of trusted/mechanical boundary contracts; and
6. an actual Verus result matching `verification results:: N verified, 0
   errors`, where `N > 0`.

Existing-vstd contracts are excluded. The subset also deliberately excludes
allocator growth, general raw-memory mutation, arbitrary `PartialEq`/`Pattern`,
stateful callbacks, unstable sorting/selection, and `MaybeUninit`.

## Selected targets

| # | Target | Input order | Verus result | Main boundary |
| ---: | --- | ---: | --- | --- |
| 1 | `core::slice::split_first` | 88 | 1 verified, 0 errors | Immutable slice-pattern mechanical desugaring |
| 2 | `core::slice::split_off_first` | 100 | 2 verified, 0 errors | Reviewed `split_first` proof and immutable pattern desugaring |
| 3 | `core::slice::split_last` | 94 | 1 verified, 0 errors | Immutable slice-pattern mechanical desugaring |
| 4 | `core::slice::split_off_last` | 102 | 2 verified, 0 errors | Reviewed `split_last` proof and immutable pattern desugaring |
| 5 | `core::slice::split_first_mut` | 91 | 1 verified, 0 errors | Mutable slice-pattern mechanical desugaring |
| 6 | `core::slice::split_last_mut` | 97 | 1 verified, 0 errors | Mutable slice-pattern mechanical desugaring |
| 7 | `core::slice::chunks_exact` | 34 | 2 verified, 0 errors | Verified private constructor, exact forward chunk partition, valid-index split boundary |
| 8 | `core::slice::rchunks_exact` | 67 | 2 verified, 0 errors | Verified private constructor, exact reverse chunk partition, valid-index split boundary |
| 9 | `core::slice::trim_ascii_start` | 116 | 6 verified, 0 errors | Source-backed ASCII whitespace helper and pattern lowering; choose uniqueness proved |
| 10 | `core::slice::trim_ascii_end` | 115 | 6 verified, 0 errors | Source-backed ASCII whitespace helper and pattern lowering; choose uniqueness proved |
| 11 | `core::slice::make_ascii_lowercase` | 63 | 8 verified, 0 errors | Per-byte Rust helper chain verified; only range-pattern lowering remains |
| 12 | `core::slice::make_ascii_uppercase` | 64 | 8 verified, 0 errors | Per-byte Rust helper chain verified; only range-pattern lowering remains |
| 13 | `core::slice::split_off_first_mut` | 101 | 1 verified, 0 errors | Reviewed `split_first_mut`, mutable pattern, and `mem::replace` lowering |
| 14 | `core::slice::split_off_last_mut` | 103 | 1 verified, 0 errors | Reviewed `split_last_mut`, mutable pattern, and `mem::replace` lowering |
| 15 | `core::slice::ChunksExact::remainder` | 1 | 1 verified, 0 errors | `ChunksExact` private representation invariant |
| 16 | `core::slice::ChunksExactMut::into_remainder` | 2 | 1 verified, 0 errors | `ChunksExactMut` private representation invariant |
| 17 | `core::slice::RChunksExact::remainder` | 6 | 1 verified, 0 errors | `RChunksExact` private representation invariant |
| 18 | `core::slice::RChunksExactMut::into_remainder` | 7 | 1 verified, 0 errors | `RChunksExactMut` private representation invariant |
| 19 | `core::slice::split_at_checked` | 84 | 1 verified, 0 errors | Reviewed `split_at_unchecked` contract and checked bound guard |
| 20 | `core::slice::split_at_mut_checked` | 85 | 1 verified, 0 errors | Reviewed `split_at_mut_unchecked` final-frame contract and checked bound guard |

All 20 rows are generated contracts.

## Implementations mechanically changed for Verus

Fourteen selected targets contain executable-body rewrites beyond receiver,
return-name, `const`, or proof-only annotation changes:

| Target | Executable change | Original implementation |
| --- | --- | --- |
| `split_first` | Slice pattern lowered to `split_at(1)` plus `head[0]` | `proof_harnesses/088_core_slice_split_first/original_implementation.rs` |
| `split_off_first` | `let-else`/method call lowered to a match over the reviewed local `split_first` | `proof_harnesses/100_core_slice_split_off_first/original_implementation.rs` |
| `split_last` | Slice pattern lowered to `split_at(len - 1)` plus `tail[0]` | `proof_harnesses/094_core_slice_split_last/original_implementation.rs` |
| `split_off_last` | `let-else`/method call lowered to a match over the reviewed local `split_last` | `proof_harnesses/102_core_slice_split_off_last/original_implementation.rs` |
| `split_first_mut` | Mutable slice pattern lowered to `split_at_mut(1)` plus `head[0]` | `proof_harnesses/091_core_slice_split_first_mut/original_implementation.rs` |
| `split_last_mut` | Mutable slice pattern lowered to `split_at_mut(len - 1)` plus `tail[0]` | `proof_harnesses/097_core_slice_split_last_mut/original_implementation.rs` |
| `chunks_exact` | Private constructor's valid `split_at_unchecked` lowered to reviewed `split_at` | `proof_harnesses/034_core_slice_chunks_exact/original_implementation.rs` |
| `rchunks_exact` | Private constructor's valid `split_at_unchecked` lowered to reviewed `split_at` | `proof_harnesses/067_core_slice_rchunks_exact/original_implementation.rs` |
| `trim_ascii_start` | `while let` slice pattern lowered to an explicit split-and-break loop | `proof_harnesses/116_core_slice_trim_ascii_start/original_implementation.rs` |
| `trim_ascii_end` | Reverse `while let` pattern lowered to an explicit split-and-break loop | `proof_harnesses/115_core_slice_trim_ascii_end/original_implementation.rs` |
| `make_ascii_lowercase` | Primitive method syntax expanded to a verified source-equivalent helper chain | `proof_harnesses/063_core_slice_make_ascii_lowercase/original_implementation.rs` |
| `make_ascii_uppercase` | Primitive method syntax expanded to a verified source-equivalent helper chain | `proof_harnesses/064_core_slice_make_ascii_uppercase/original_implementation.rs` |
| `split_off_first_mut` | `mem::replace` lowered to swap-with-empty; mutable pattern lowered | `proof_harnesses/101_core_slice_split_off_first_mut/original_implementation.rs` |
| `split_off_last_mut` | `mem::replace` lowered to swap-with-empty; mutable pattern lowered | `proof_harnesses/103_core_slice_split_off_last_mut/original_implementation.rs` |

Each file above is text-equivalent to the frozen `source_excerpt.rs` after
removing only the original source indentation and adding a two-line provenance
header.

The other six selected targets preserve their target executable statements:
the four exact-chunk remainder accessors, `split_at_checked`, and
`split_at_mut_checked`. Their harness differences are limited to signatures,
explicit receiver syntax, dependency contracts, model instantiation, and
ghost/proof annotations. Their original source remains in the adjacent
`source_excerpt.rs`.

## Boundary-contract union

After excluding the selected contracts' own specification vocabulary, the 20
proofs depend on 17 distinct boundary/mechanical interfaces:

1. immutable slice-pattern desugaring;
2. mutable slice-pattern desugaring;
3. `mem::replace` lowering for mutable slice-reference updates;
4. valid-index immutable slice split used by exact-chunk constructors;
5. exact-chunk constructor arithmetic and partition model;
6. `u8::is_ascii_whitespace`;
7. `trim_ascii_start` leading first/rest pattern lowering;
8. `trim_ascii_end` trailing rest/last pattern lowering;
9. `u8::is_ascii_uppercase` range-pattern desugaring;
10. `u8::is_ascii_lowercase` range-pattern desugaring;
11. `ChunksExact::invariant`;
12. `ChunksExactMut::chunks_exact_mut_private_invariant`;
13. `RChunksExact::invariant`;
14. `RChunksExactMut::rchunks_exact_mut_private_invariant`;
15. reviewed `core::slice::split_at_unchecked`;
16. reviewed `core::slice::split_at_mut_unchecked`; and
17. the source-checked guard `mid <= self.len()`.

There are 30 total boundary/model references across the 20 proofs. The two
replacement targets stay within the already selected exact-chunk
representation family and reuse the reviewed valid-index slice-split boundary.

## Boundary-to-helper mapping

| # | Boundary | Corresponding helper functions or operations |
| ---: | --- | --- |
| 1 | Immutable slice-pattern desugaring | `<[T]>::split_at`, immutable indexing of `head[0]`/`tail[0]` |
| 2 | Mutable slice-pattern desugaring | `<[T]>::split_at_mut`, mutable indexing of `head[0]`/`tail[0]` |
| 3 | `mem::replace` lowering | `core::mem::swap` with a local empty mutable slice |
| 4 | Exact-chunk valid split | reviewed `<[T]>::split_at`, replacing source `split_at_unchecked` only after the constructor proves the index is in range |
| 5 | Exact-chunk constructor | real `ChunksExact::new` / `RChunksExact::new`, `slice_chunk_partition`, `slice_iterator_view`, arithmetic `div_mod` lemmas |
| 6 | ASCII whitespace classification | `u8::is_ascii_whitespace`, harness helper `byte_is_ascii_whitespace`, spec helper `ascii_is_whitespace` |
| 7 | Trim-start model | `ascii_trim_start_boundary`, `ascii_trim_start_index`, `ascii_trim_start_result`, verified `lemma_ascii_trim_start_boundary_unique` and `lemma_ascii_trim_start_index_matches_boundary` |
| 8 | Trim-end model | `ascii_trim_end_boundary`, `ascii_trim_end_index`, `ascii_trim_end_result`, verified `lemma_ascii_trim_end_boundary_unique` and `lemma_ascii_trim_end_index_matches_boundary` |
| 9 | ASCII lowercase model | verified `byte_is_ascii_uppercase`, `byte_to_ascii_lowercase`, `byte_make_ascii_lowercase`, `ascii_lower_byte`, `ascii_lower_seq`; only `matches!(A..=Z)` is mechanically lowered |
| 10 | ASCII uppercase model | verified `byte_is_ascii_lowercase`, `byte_to_ascii_uppercase`, `byte_make_ascii_uppercase`, `ascii_upper_byte`, `ascii_upper_seq`; only `matches!(a..=z)` is mechanically lowered |
| 11 | `ChunksExact` representation | `slice_iterator_view::<&ChunksExact<'a, T>, T>`, `ChunksExact::invariant` |
| 12 | `ChunksExactMut` representation | `slice_iterator_view::<ChunksExactMut<'a, T>, T>`, `chunks_exact_mut_private_invariant` |
| 13 | `RChunksExact` representation | `slice_iterator_view::<&RChunksExact<'a, T>, T>`, `RChunksExact::invariant` |
| 14 | `RChunksExactMut` representation | `slice_iterator_view::<RChunksExactMut<'a, T>, T>`, `rchunks_exact_mut_private_invariant` |
| 15 | Immutable unchecked split dependency | reviewed `split_at_unchecked`, `split_point_in_range` |
| 16 | Mutable unchecked split dependency | reviewed `split_at_mut_unchecked`, `split_at_mut_unchecked_result`, `split_point_in_range` |
| 17 | Checked split branch guard | executable `slice.len()` and `mid <= len` comparison |

The concrete target-local definitions are in the selected
`proof_harnesses/NNN_TARGET/harness.rs` files. Shared spec helpers are frozen in
`frozen_inputs/slice/specs/slice_shared_vocabulary.rs`.

## Why each boundary is credible

These arguments explain why the boundary is source-backed and narrow. They do
not silently promote an unproved boundary to an A proof.

1. **Immutable slice-pattern desugaring:** for a nonempty slice,
   `split_at(1)` returns exactly the first singleton prefix and remaining tail;
   indexing `head[0]` therefore implements `[first, tail @ ..]`. For the last
   pattern, splitting at `len - 1` gives the exact prefix and singleton last
   suffix. The transformation changes syntax only, not control flow or data.

2. **Mutable slice-pattern desugaring:** `split_at_mut(1)` and
   `split_at_mut(len - 1)` produce disjoint mutable regions with the same
   first/tail or prefix/last decomposition. The selected contracts reconstruct
   `final(slice)@` from the final returned regions, so mutation effects are not
   discarded.

3. **`mem::replace` lowering:** swapping the receiver slot with a local empty
   mutable slice has the same state transition as
   `mem::replace(self, &mut [])`: the slot receives the empty value and the
   local variable receives the old slice reference. The subsequent assignment
   of the remainder back into the slot is preserved literally.

4. **Exact-chunk valid split:** both constructors compute the split index from
   `len % chunk_size`, prove that it is within the source slice, and then split
   at that exact index. Replacing the source's unsafe unchecked split with the
   reviewed safe `split_at` contract changes no valid-input result and avoids
   trusting arbitrary pointer arithmetic.

5. **Exact-chunk constructors:** the real private constructor bodies are
   included in the harness. They compute the remainder, execute the split, and
   construct the iterator fields directly. Verus proves the modulo arithmetic,
   exact source decomposition, remainder bound, divisible chunk region, chunk
   size, and forward/reverse direction.

6. **`u8::is_ascii_whitespace`:** Rust defines this predicate by the fixed byte
   set `09, 0A, 0B, 0C, 0D, 20`. The open `ascii_is_whitespace` definition lists
   exactly those six values, making the helper correspondence finite and
   directly inspectable.

7. **Trim-start helpers:** `ascii_trim_start_boundary` states that every byte
   before the selected index is whitespace and the selected byte, when one
   exists, is not. This uniquely identifies the first non-whitespace boundary.
   The implementation loop repeatedly removes one leading whitespace byte, so
   its exit condition establishes exactly this predicate. The former external
   choose/index bridge has been removed: Verus now proves boundary uniqueness
   by contradiction and then proves that `choose` returns the loop-computed
   index.

8. **Trim-end helpers:** the end predicate analogously requires all bytes from
   the selected index onward to be whitespace and the preceding byte, when one
   exists, to be non-whitespace. The implementation repeatedly removes the
   trailing whitespace byte and therefore establishes this exact boundary. The
   former external choose/index bridge has been removed: Verus now proves
   boundary uniqueness and that `choose` returns the loop-computed end index.

9. **ASCII lowercase helpers:** the full Rust helper chain is now verified in
   the harness: uppercase classification, the exact OR-mask expression, and
   the in-place assignment. A bit-vector proof establishes that setting bit
   `0x20` on `A..=Z` equals the arithmetic `+ 0x20` model and that OR with zero
   leaves all other bytes unchanged. Only the unsupported Rust range-pattern
   syntax is lowered to equivalent comparisons.

10. **ASCII uppercase helpers:** the full Rust helper chain is now verified in
    the harness: lowercase classification, the exact XOR-mask expression, and
    the in-place assignment. A bit-vector proof establishes that toggling bit
    `0x20` on `a..=z` equals the arithmetic `- 0x20` model and that XOR with
    zero leaves all other bytes unchanged. Only the unsupported Rust
    range-pattern syntax is lowered to equivalent comparisons.

11. **`ChunksExact::invariant`:** the constructor computes the remainder from
    `slice.len() % chunk_size`; therefore `remainder.len() < chunk_size` for a
    positive chunk size. `remainder()` then returns the private `rem` field
    directly. The model is consequently tied to extracted private fields rather
    than an arbitrary result function.

12. **`ChunksExactMut` private invariant:** the same modulo construction
    establishes the remainder bound. A trusted lemma is currently needed
    because Verus rejects moving a mutable-reference field out of a datatype
    carrying a user-defined invariant, not because the Rust source leaves the
    remainder unspecified.

13. **`RChunksExact::invariant`:** reverse exact chunks use the same
    `len % chunk_size` arithmetic, with the remainder placed at the opposite
    end. The accessor still returns the private remainder field directly, so the
    representation relation is exact.

14. **`RChunksExactMut` private invariant:** this is the mutable reverse analogue
    of item 13. Its trusted lemma covers the same Verus field-move limitation and
    the same source-derived strict remainder-length bound.

15. **`split_at_unchecked`:** the reviewed callee contract fixes both returned
    views exactly to `source[0..mid]` and `source[mid..len]`. The checked wrapper
    invokes it only after proving `mid <= len`; the wrapper adds no further
    pointer arithmetic or implementation choice.

16. **`split_at_mut_unchecked`:** the reviewed mutable callee fixes the initial
    left/right views and requires the final source to equal
    `final(left) + final(right)`. This captures both the split and all
    write-through effects needed by `split_at_mut_checked`.

17. **`mid <= len` guard:** this is not an assumed helper result. It is the
    executable condition in the Rust target body. The verified true branch
    discharges the unchecked split precondition, while the false branch returns
    `None` and, for the mutable case, leaves the slice unchanged.

## Two remaining foundational proof gaps

### Raw slice construction and provenance

`split_at_unchecked` ultimately constructs its two returned slices using:

```rust
from_raw_parts(ptr, mid)
from_raw_parts(ptr.add(mid), len - mid)
```

Proving `from_raw_parts` requires a memory model showing that the raw pointer is
properly aligned, live, carries the correct provenance, and denotes at least
the requested number of initialized `T` elements. The current Verus setup
cannot derive these allocation and permission facts from an arbitrary
`*const T`, so raw slice construction remains an explicit unsafe boundary.

This boundary is transitive for selected targets that reuse slice splitting:

- `chunks_exact`;
- `rchunks_exact`;
- `split_at_checked`; and
- `split_at_mut_checked`.

The relevant lower-level evidence is under
`proof_harnesses/087_core_slice_split_at_unchecked/` and
`proof_harnesses/086_core_slice_split_at_mut_unchecked/`. Inlining those
helpers would remove one modular `external_body`, but would not eliminate the
underlying raw-pointer/`from_raw_parts` trust.

### Moving mutable-reference fields across type invariants

`ChunksExactMut` and `RChunksExactMut` store their remainder as an
`&mut [T]`. Their consuming remainder accessors return that field directly:

```rust
pub fn into_remainder(self) -> &'a mut [T] {
    self.rem
}
```

Unlike `&[T]`, an `&mut [T]` is not `Copy`; returning it moves the unique
reference out of the consumed struct. Verus currently does not support moving
a mutable-reference field out of a datatype carrying a user-defined type
invariant. Consequently the proofs use the narrowly scoped trusted lemmas:

- `ChunksExactMut::chunks_exact_mut_private_invariant`; and
- `RChunksExactMut::rchunks_exact_mut_private_invariant`.

These lemmas state only that `remainder.len() < chunk_size`, a fact established
by the constructor's `len % chunk_size` computation. Removing this boundary
would require verifying the constructor with a formal type invariant and
lowering the field move to a swap/take-with-empty operation that preserves the
invariant before returning the original remainder.

These two foundational gaps are why the affected targets remain B rather than
A even though their public target bodies have successful Verus results.

## Confidence rationale

- The head/tail family is dependency-closed inside this subset:
  `split_off_first` reuses the selected `split_first` proof, while
  `split_off_last` reuses the selected `split_last` proof. The mutable split
  functions have explicit final-frame equations and do not use the invalid
  `final(slice)@ == old(slice)@` iterator frame found in the C targets.
- `chunks_exact` and `rchunks_exact` include and verify the real private
  constructor bodies. They share the same exact-chunk representation model as
  the four selected remainder accessors, so their helper dependencies close
  within one reviewed family.
- The four ASCII contracts use byte-level definitions directly aligned with
  Rust's ASCII source semantics. They avoid generic Unicode, locale, Pattern,
  and callback behavior.
- The four exact-chunk remainder accessors preserve direct private-field data
  flow and expose the exact remaining slice; their boundaries are narrowly
  scoped representation invariants rather than arbitrary return models.
- `split_at_checked` and `split_at_mut_checked` execute the source bound guard
  and reuse already reviewed unchecked-split contracts. Their `None`/`Some`
  result relations are fully determined by `mid <= len`.

## Artifact layout

For input order `NNN` and target slug `TARGET`, use:

```text
proof_harnesses/NNN_TARGET/harness.rs
proof_harnesses/NNN_TARGET/source_excerpt.rs
proof_harnesses/NNN_TARGET/evidence/verus_stdout.txt
proof_harnesses/NNN_TARGET/evidence/verus_stderr.txt
proof_harnesses/NNN_TARGET/evidence/verus_exit_code.txt  # when present
proof_manifests/NNN_TARGET/source_body.json
proof_manifests/NNN_TARGET/transformation_manifest.json
proof_manifests/NNN_TARGET/dependency_assumption_manifest.json
```

The authoritative aggregate rows are in
`proof_inventory/targets_180.{json,csv}`.

The selection gate parses `verus_stdout.txt` directly and requires
`verification results:: N verified, 0 errors` with `N > 0`; it does not infer
verification success from typecheck output or B status alone.
