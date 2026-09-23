# Slice values on the selected upstream baseline

The existing `View for [T]` in
`toolchain/upstream/source/vstd/slice.rs:13-17` maps a borrowed slice to `Seq<T>`.
No new view, answer-selecting observer, element trait bound, or axiom is added.
All six predicates in `specs/slice/mod.rs` observe that same ordered sequence.
They have no input preconditions. `Option` variants, element values, tuple
order, and the entire returned subslice sequence are observed.
`split_last` places the last element first and the initial subslice second.

The selected release is `0.2026.09.20.aef82ed`, not the Rust 1.96 semantic
source. Its slice view is an existing upstream uninterpreted view with
existing correspondence axioms: `axiom_spec_len` at `slice.rs:77-80`,
`axiom_spec_slice_index` at `slice.rs:190-193`,
`axiom_slice_ext_equal` at `slice.rs:170-174`, and the existing array/slice
coercion and indexing support. This is the upstream trusted basis, not a new
proof that Rust 1.96 `ptr::metadata` satisfies the length predicate.

The Rust implementation chain is
`core/src/slice/mod.rs:116-118` ->
`core/src/ptr/metadata.rs:101-103` ->
`core/src/intrinsics/mod.rs:2951-2958` (`UnOp::PtrMetadata`).
The metadata docs at `ptr/metadata.rs:12-27` distinguish a data address from
metadata and specify a slice's metadata as its element count.
The other four reference-returning bodies use slice patterns, not indexing
or the upstream assumed `first`/`split_first` contracts.
The correctness files must establish those actual operations' connection to
the existing value view; a direct call to the target method cannot do so.

The proof copies lift `impl<T> [T]` methods into free functions only because
another crate cannot declare inherent methods on the primitive slice type.
The impl type parameter becomes the function type parameter and the bound
receiver identifier `self` becomes `slice: &[T]`. All six remain `pub const fn`,
with unconstrained `T`, unchanged elided reference lifetimes and return types,
and the original executable expressions. Source attributes concerning library
stability, lang-item registration, inlining and documentation are recorded in
the inventory rather than redeclared by the proof crate. This naming/binding
translation does not replace metadata access or desugar a slice pattern.

`scalar_domain` and `empty_results` in the aggregate are contract consistency
lemmas, not implementation proofs. Native Rust 1.96 probes in
`tests/readonly_behavior.rs` independently exercise the exact source copies;
they likewise do not close the Verus correctness track.

## Empty-reference Default observations

Both zero-argument slice-reference `Default` constructors use this same
`Seq<T>` view. `specs/slice/default_post.rs` requires the full view to equal
`Seq::<T>::empty()` extensionally; it introduces no new observer or element
bound. The source proof bodies remain exactly `&[]` and `&mut []`.

For the mutable constructor's analysis-only shared reborrow,
`proofs/completeness/slice/inputs/default_mut.rs` retains
`result@ == old(value)@` in `observe`. Predicate preservation follows from
full view equality by substitution, so the additional equivalence of
`default_post` on those views was redundant and has been removed.
This does not change the selected full-value observation or remove a
cross-state or final writeback obligation. The constructor has no input
slice or caller-owned region requiring writeback.

Independent review justified the original observation transfer and proved
the redundancy implication (one goal, zero errors); a temporary reduced
adapter compiled with four functions verified and zero errors. The revised
real input has since compiled with four functions verified and zero errors;
its actual analyze and reexecution each checked one determinism goal with an
UNSAT original query. The second independent review completed this revision
for both Default constructors in the full-sequence observation scope:
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/8b6d043ccde7/round-0002.json`.
Direct mutable-return checker extraction
is still unsupported; the shared reborrow is an analysis encoding, not a
replacement implementation. See [S-MUT-RETURN](../../issues/S-MUT-RETURN.md)
for the retained original evidence and separate revision paths.
