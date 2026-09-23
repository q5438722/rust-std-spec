---
title: Two mutable split observations
description: Complete initial element/remainder observations, independent final writes, fixed borrowed lengths and ordered whole-input reconstruction.
---

# Two mutable split observations

Rust 1.96 `slice/mod.rs:202-222,244-264` defines `split_first_mut` and
`split_last_mut` in the unconstrained `impl<T> [T]`. Each has one mutable
receiver, returns `Option<(&mut T, &mut [T])>` with both lifetimes bound to
that receiver, and is const-stable since 1.83.0. The last method returns
`(last, init)`, although whole-input reconstruction places `init` first.

The authoritative patterns borrow positions `0` and `[1,n)`, or `n-1`
and `[0,n-1)`, on exactly the nonempty branch. At length one the first
empty remainder begins one past the original element, whereas the last
empty remainder begins at its start. Element extents, not equality of
zero-sized addresses, distinguish these regions. The source, versioned
language rules and proposed split/index correspondence are documented in
[V-SLICE-PATTERN](../../../../../issues/V-SLICE-PATTERN.md#proposed-mutable-split-conversions).
The exact current source conversions have their own
[independent permission](../../../../../issues/V-SLICE-PATTERN.md#independent-mutable-split-permission-before-adoption);
neither the [shared splits](split-source-dependencies.md) nor the
[mutable endpoints](mutable-endpoint-observations.md) are its authority.

## A complete state relation

The pure predicates in
[`mutable_splits_post.rs`](../../../../../specs/slice/mutable_splits_post.rs)
take initial input `s: Seq<T>` and caller-final
`Option<(T, Seq<T>)>`. Their result observation contains initial
`Option<(T, Seq<T>)>` and the entire final input `Seq<T>`.

For nonempty input, the first initial pair is
`(s[0], s.subrange(1, s.len()))`; the last initial pair is
`(s[s.len()-1], s.subrange(0, s.len()-1))`. Neither full remainder is
determined by the endpoint alone. The final element and remainder are
independent caller choices, constrained only by the borrowed remainder's
unchanged length. Whole-input reconstruction is respectively
`seq![written_element] + written_remainder` and
`written_remainder + seq![written_element]`.

The caller Option tracks the original return variant, not a later assignment
to an Option variable. Its domain is:

```rust
match caller_final {
    None => s.len() == 0,
    Some((_, written_remainder)) => written_remainder.len() + 1 == s.len(),
}
```

The empty branch requires no inhabitant of `T`. Neither initial returned
contents nor the final owner is an environment input. The state lemmas in
[`mutable_splits_state.rs`](../../../../../proofs/completeness/slice/mutable_splits_state.rs)
derive that domain, prove every admissible independent caller write has a
satisfying result, and preserve all compared observations. Separate
regressions include independent mutations, initial remainder order, wrong
reconstruction order and a parameterless generic empty witness.

The cross-state remainder-length relation cannot be deleted merely because
the initial remainder equals a subrange. In the reference interface it follows
from borrowing; in the value representation the caller-final sequence is a
different input. Same-state remainder lengths and final-owner length follow
from the full sequence relations and are not separate candidate clauses.
The [temporary redundancy criterion](../../../../../review-criteria-temporary.txt)
distinguishes these cases.

## Existing trusted contracts and source isolation

The selected vstd already binds `split_first_mut` at
`toolchain/upstream/source/vstd/std_specs/slice.rs:554-564`. The first
correspondence lemma proves equivalence to those exact clauses, including
the initial full tail, its cross-state length and final reconstruction.
The selected vstd has no `split_last_mut` binding. Only the missing method
is declared in
[`mutable_splits.rs`](../../../../../specs/slice/mutable_splits.rs);
the source proofs import the pure file, not this declaration.

The upstream `split_at_mut` contract at `std_specs/slice.rs:526-535`
relates both initial subranges and the concatenation of both final regions.
Its `usize` mutable-index relation is at 17-35, with built-in lowering
correspondence in `vstd/slice.rs:177-197`. The existing
`mut_ref_slice_len_eq` at 218-221 preserves a mutable slice reference's length.
The current adopted sources invoke that fact for the returned remainder before
moving the reference. This does not freeze contents or add a trusted fact.
All these contracts remain dependencies, not new proofs of indexing,
metadata or `split_at_mut` itself.

The Rust 1.96 source chain is
`split_at_mut` at `slice/mod.rs:1986-1991`,
`split_at_mut_checked` at 2192-2200, and
`split_at_mut_unchecked` at 2092-2112. The guarded bound permits the latter
to construct two exclusive slices from the original mutable pointer,
with lengths `mid` and `n-mid`. Both proposed split positions stay within
that bound. These dependencies are const-callable on the required baseline.
The original patterns and isolated proposals remain historical inputs;
the independently permitted current source files contain only the exact
body replacement and that existing ghost call.

## The checker retains both complete returned regions

Specdet 0.3.0 rejects direct extraction of the nested mutable return.
The active value-state functions use
`Ghost<Seq<T>>`, `Ghost<Option<(T, Seq<T>)>>` and result
`Ghost<(Option<(T, Seq<T>)>, Seq<T>)>`. Their generated equality compares:

```text
initial Option variant
and, when Some, logical element equality and full remainder sequence equality
and full final-owner sequence equality
```

Only representation beyond the erased Ghost view is ignored. The original
queries for this shape have 19 guards: two initial-input length guards,
four caller Option/remainder guards, six per output, and output inequality.
All must be disabled for the original problem. The 13-guard mutable endpoint
shape does not cover these nested remainder observations.

The exact checker limitation, generated comparison, proof correspondence
and retained executions are in
[S-MUT-RETURN](../../../../../issues/S-MUT-RETURN.md#two-simultaneously-live-mutable-regions).
The current selectors are
`proofs/completeness/slice/inputs/split_first_mut.rs:split_first_mut_observation@7`
and the analogous `split_last_mut` selector at line 7. These are analysis
functions, not changes to either public API.

The [native comparison description](native-output-locations.md#adopted-mutable-split-comparisons)
covers actual simultaneous borrows, const calls, provenance-sensitive
nonzero-sized empty remainders, independent writes and compiler rejections.
Neither those tests nor the value-state determinism result supplies the
separate source correspondence or final review.

The selective exporter is
`scripts/export_completeness.py --mutable-splits [split_first_mut split_last_mut]`.
It validates every selected current source compile and the unchanged
state/adapter/checker files before updating any result. It requires one
source target, one actual generated comparison per analyze/reexecution,
the full nested equality and all 19 original guards off. Failed, UNKNOWN,
zero-goal, stale, incomplete-comparison or wrong reexecution inputs cannot
be exported. Existing unselected raw TSV records and proof files are
preserved, including during rejected invocations and partial selections.

The two exported files are copied from the real generated comparisons,
with only the relative state import relocated and provenance comments added.
Their nine compilation functions are one comparison, one adapter and
seven state lemmas, not nine source targets. The real CLI tests in
[`test_mutable_split_export_cli.py`](../../../../../tests/test_mutable_split_export_cli.py)
use `TMPDIR` for isolated roots and `MUTABLE_SPLIT_EXPORT_TEST_LOG_DIR` for
retained command results in review scratch. The default export retains
existing mutable split results without rewriting their observations.

For this exact nested observation shape, deleting an initial-element,
initial-remainder or final-owner clause yields independently compiled
unequal-output witnesses, but the selected checker's automated negative
search remains inconclusive in both generic and isolated `u8` instances.
The `u8` experiment removes the generic-type narrowing diagnostic without
resolving `UNKNOWN (incomplete quantifiers)`, so that earlier diagnostic
alone does not establish the cause. The complete controls still prove their
generated comparisons. Its concrete scalar search adds guards: all 121 are
disabled in each original `u8` query, whereas the generic main queries have
19. Both comparisons preserve the same complete observations. The scope and separate kinds of evidence are recorded
in [the omitted-observation controls](../../../../../issues/S-MUT-RETURN.md#omitted-observation-controls);
no UNKNOWN result supplies an API completion or a checker-certified witness.
