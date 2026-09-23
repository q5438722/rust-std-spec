---
title: Singleton borrow contracts and the source boundary
description: A complete four-state value relation supports mutable singleton completeness without supplying the missing element-reference to array-reference source proof.
---

# Singleton borrow contracts and the source boundary

Rust 1.96 `slice/raw.rs:198,203-205` and `207,211-213` define `from_ref` and
`from_mut`. Both take one reference to an implicitly `Sized` unconstrained
`T`, return an input-lifetime slice of length one without copying, and retain
stable const callability. The array delegates and their documentation are
at `array/mod.rs:163-169,171-177` in the authoritative source tree recorded
in [toolchain/BASELINE.md](../../../../../toolchain/BASELINE.md).

The candidate in [specs/slice/raw.rs](../../../../../specs/slice/raw.rs) uses
the existing slice view and
[singleton_post](../../../../../specs/slice/raw_post.rs):

```rust
elements =~= seq![value]
```

Shared conversion relates the full result to `*s`. Mutable conversion has
two independent state relations: its initial result equals `seq![*old(s)]`,
and its final returned slice equals `seq![*final(s)]`. The latter does not
freeze caller writes. Neither relation asserts allocation-address determinism.
Length and element-zero clauses would be redundant with a full singleton
sequence; the initial and final clauses are not redundant with each other.

## The existing array relations stop short of the constructor

The selected upstream vstd defines its array view at `array.rs:11-21`.
Shared unsizing relates array and slice views at lines 90-95 and 115-121;
mutable unsizing preserves initial and final views at lines 175-183.
These declarations model array-to-slice conversion, not conversion from
an element reference to a singleton array reference.

On unmodified Verus `0.2026.09.20.aef82ed`, both original array bodies are
rejected at `s as *const T` / `s as *mut T` before source verification.
The contract-free
[minimal reproduction](../../../../../issues/repros/singleton_reference_casts.rs)
has the same diagnostic. The
[exact source proof copies](../../../../../proofs/correctness/array/singleton.rs),
[commands and output](../../../../../logs/singletons/correctness/array/), and
[isolated conversion output](../../../../../logs/singletons/reference-cast-repro/)
bound this observation to the selected baseline and these conversions.
No conclusion about later raw-pointer operations follows from a frontend
rejection before those operations are reached.

No array constructor contract has been assumed to fill the missing step.
The public bindings remain candidates, not completed source proofs; the
current boundary is recorded in
[V-METADATA](../../../../../issues/V-METADATA.md#singleton-array-delegation-on-the-same-baseline).

## Mutable observations need both states

The installed specdet 0.3.0 can generate and replay the shared singleton's
full slice-value comparison. Direct mutable-reference return extraction
remains unsupported, as recorded in
[S-MUT-RETURN](../../../../../issues/S-MUT-RETURN.md#singleton-borrows-with-caller-owned-state).

The [Default observation](default-slice-observation.md) does not supply the
singleton adaptation: observing a shared reborrow at construction does not
describe a caller-owned element after subsequent mutable writes.

The complete relation in
[from_mut_state.rs](../../../../../proofs/completeness/slice/from_mut_state.rs)
uses four separate value observations:

| Meaning | Candidate expression | Relation parameter |
|---|---|---|
| Input initial value | `*old(s)` | `input_initial : T` |
| Initial returned slice | `result@` | `observations.0 : Seq<T>` |
| Caller-selected final slice | `final(result)@` | `caller_final : Seq<T>` |
| Input returned after the borrow | `*final(s)` | `observations.1 : T` |

Its definition is exactly
`singleton_post(input_initial, observations.0) &&
singleton_post(observations.1, caller_final)`.
The first and third rows are the checker inputs; the second and fourth are
the outputs to be compared. In particular the initial returned sequence
and input writeback value are not assumed equal between the two outcomes.

The original initial clause and the existing
`vstd::slice::mut_ref_slice_len_eq` imply `caller_final.len() == 1`.
On this environment domain the second relation is equivalent to
`observations.1 == caller_final[0]`. This is a proved restatement, not a
new precondition on the public constructor. Every length-one final sequence
has a satisfying pair `(seq![input_initial], caller_final[0])`, for arbitrary
`T` and independent initial/final contents. No element trait or lifetime
restriction is needed.

The current
[analysis entry](../../../../../proofs/completeness/slice/inputs/from_mut.rs)
uses explicit `Ghost` carriers for these values. The generated
[comparison](../../../../../proofs/completeness/slice/from_mut.rs) checks
extensional equality of the entire initial sequence and logical equality
of the entire returned `T`. It does not compare allocation addresses.
The original mutable declaration is retained only as a
[historical reproduction](../../../../../proofs/completeness/slice/history/from_mut_direct.rs);
there is one current mutable entry.

The formal correspondence includes full slice-view equality, environment
coverage, and lawful witnesses. The
[state regressions](../../../../../tests/from_mut_state.rs) cover changed
contents, non-Copy/non-static elements, and zero-sized elements.
[Native checker controls](../../../../../logs/singleton-writeback/weakening-ghost-inputs/results.json)
separately omit each constraint and carry constructive witnesses for the
corresponding lost observation. The source implementation and its array
delegates are not imported into this completeness proof. Their source
boundary above therefore remains unchanged.

[Native source checks](native-output-locations.md#singleton-source-checks)
cover addresses, non-Copy and non-static elements, zero-sized elements,
stable const calls and legal writeback. They complement, rather than
replace, the two formal proof requirements.
