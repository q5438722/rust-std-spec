# Completeness-only declarations

These files bind each analysis declaration to a free-function copy with the
original `pub const fn` signature and executable expression. The only
translation is lifting the impl's type parameter and renaming its receiver,
as described in `specs/shared/SLICE_VIEW.md`. The Rust compiler checks that
each `assume_specification` has the same generic signature and reference
lifetimes as its named copy. The source functions are deliberately outside
`verus!`; they are not claimed as implementation proofs.

Each declaration's sole postcondition calls the exact public predicate from
`specs/slice/mod.rs` used by the corresponding correctness file. There is no
requires clause, added trait bound, alternate view or alternate observation.
Thus the binding is literal, not a separate handwritten approximation of
the candidate. No assumption in these files is imported by the correctness
files or the root specification aggregate.

`specdet.toml` configures the real checker and the same upstream release.
The generated checker comparison must be inspected to ensure that the
`Option` variant and every returned element/subslice value are retained.
The generated harnesses, queries and results will remain under
`proofs/completeness/slice/runs/<api>/`; the per-API Rust files one directory
above this directory will be replayable exports of the generated harnesses.
Only their relative import of the unchanged predicate file may be relocated.

A deterministic result from these declarations is a completeness result
only. It cannot remove the source-body limitation recorded in `issues/`.
