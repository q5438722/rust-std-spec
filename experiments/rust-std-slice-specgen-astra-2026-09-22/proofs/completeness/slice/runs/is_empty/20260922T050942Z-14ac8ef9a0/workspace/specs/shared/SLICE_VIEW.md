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
`axiom_spec_slice_index` at `slice.rs:192-196`, and the existing array/slice
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
