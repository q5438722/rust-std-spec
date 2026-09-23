# Completeness-only declarations

The six original observer files bind each analysis declaration to a free-function copy with the
original `pub const fn` signature and executable expression. The only
translation is lifting the impl's type parameter and renaming its receiver,
as described in `specs/shared/SLICE_VIEW.md`. The Rust compiler checks that
each `assume_specification` has the same generic signature and reference
lifetimes as its named copy. The source functions are deliberately outside
`verus!`; they are not claimed as implementation proofs.

Each observer declaration's sole postcondition calls the exact public predicate from
`specs/slice/mod.rs` used by the corresponding correctness file. There is no
requires clause, added trait bound, alternate view or alternate observation.
Thus the binding is literal, not a separate handwritten approximation of
the candidate. No assumption in these files is imported by the correctness
files or the root specification aggregate.

`specdet.toml` configures the real checker and the same upstream release.
The generated checker comparison must be inspected to ensure that the
`Option` variant and every returned element/subslice value are retained.
The generated harnesses, queries and results remain under
`proofs/completeness/slice/runs/<api>/`; the per-API Rust files one directory
above this directory are compiled and verified exports of the generated harnesses.
Only their relative import of the unchanged predicate file may be relocated.

A deterministic result from these declarations is a completeness result
only. It cannot remove the source-body limitation recorded in `issues/`.

## Singleton state observations

`from_ref.rs` binds the unchanged shared candidate directly to the public
API. `from_mut.rs` is the sole current mutable analysis entry; the failed
direct declaration is preserved byte-for-byte in
`../history/from_mut_direct.rs` and in its original failed run snapshots.
`singletons.toml` discovers only the current shared declaration and mutable
observation function.

The mutable function's two `Ghost` inputs represent `*old(s)` and
`final(result)@`. Its `Ghost<(Seq<T>, T)>` output represents the entire
initial `result@` and the entire `*final(s)`, not preselected inputs.
`../from_mut_state.rs` proves correspondence with both unchanged candidate
clauses, the final-slice domain from existing borrow-length preservation,
existence for every lawful final sequence, and preservation of the complete
value comparison. Explicit `Ghost` carriers also keep native constructive
witnesses well-typed; they do not add observations or public API parameters.

The derived length-one environment domain permits arbitrary element
replacement. Within it, the final singleton clause is equivalent to
`result@.1 == caller_final@[0]`; the initial clause still constrains all of
`result@.0`. Both equality dimensions appear in the actual generated
comparison. The formal correspondence, native weakening controls, and
remaining source boundary are described in
[`S-MUT-RETURN`](../../../../issues/S-MUT-RETURN.md#complete-mutable-value-state-adaptation).
Neither this input nor its compiled export proves the array delegates.
