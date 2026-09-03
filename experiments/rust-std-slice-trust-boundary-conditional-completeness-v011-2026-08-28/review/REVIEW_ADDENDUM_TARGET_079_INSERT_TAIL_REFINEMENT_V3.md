# Independent Reviewer addendum: target 079 insert-tail refinement v3

**VERDICT: ACCEPT**

**Date:** 2026-09-02

This decision covers only the additive trusted-free `insert_tail` and
`CopyOnDrop` refinement for input order 079,
`core::slice::select_nth_unstable_by_key`. It does not replace the accepted
operational-v1 or adapter-v2 packages, change either accepted classification,
or authorize a Manager-owned stage transition. The Engineer-generated
`result.json` remains review-pending by design; this addendum is the
independent verdict.

## Source and boundary review

The frozen Rust 1.96 source first invokes the adapter on the tail and its
predecessor. Only a normal Less result creates the gap. Each loop iteration
copies `sift` into the current gap, moves the guard destination to `sift`, and
either restores the temporary, invokes the next adapter comparison, or
continues with the decremented `sift`. Ordinary unwind runs `CopyOnDrop`;
double-panic abort bypasses that cleanup.

The Verus kernel follows that order over arbitrary
`0 <= begin < tail < sequence.len()` inputs. Every adapter frame is constructed
from the accepted `KeyOrdDropBoundary`, the current callback state, and the
current left and right source identities. Key, `Ord::lt`, and Drop
result/state/panic observations are the only trusted boundary data. Adapter
frames, invocation schedules, Less decisions, gap positions, outputs, final
states, answer encodings, and traces are not inputs, so the boundary remains
strictly narrower than the target.

The initial panic and abort branches precede gap creation. After a shift,
ordinary panic retains the callback state and restores the active gap, while
abort retains the callback state and exact interrupted sequence without
running the cleanup write. Length and outside-range framing hold on every
path; identity multiplicity holds after every normal or ordinary-panic
restoration.

## Verus and SMT correspondence review

The Verus artifact contains no `assume`, `admit`, `external_body`, axiom, or
precomputed terminal result. Fresh verification reports
`15 verified, 0 errors`.

The bridge parses the Verus expression AST rather than accepting a translated
result. It mechanically binds the locally composed adapter to the accepted
`AdapterTransition`, then compares all four state fields against retained
`ExactInsertTailLoop` and `ExactInsertTail` over the arbitrary valid recursive
and entry domains. Both correspondence queries replay UNSAT.

Ten mutations cover adapter operands, callback-state lookup, Less gating,
shift source and destination, gap advancement, callback-state propagation,
panic restoration, abort discrimination, and cleanup bypass. Every mutation
makes correspondence SAT; eight also fail deterministic Verus verification.
The two definition-consistent adapter/Less mutations are correctly
correspondence-only. Independent negative probes additionally reject wrong
return type, argument order, missing abort field, abort-default laundering,
an invalid entry relation, and an invalid loop-gap relation.

The no-shift, multi-shift, ordinary-panic-after-shift, and abort-after-shift
witnesses all replay SAT with models. Their expected sequence, callback,
panic, and abort observations are independently fixed by the frozen source and
retained exact semantics.

## Independent execution

Fresh Reviewer execution produced these results:

- Python compilation passed.
- Verus type-check passed; verification reported
  `15 verified, 0 errors`.
- Nineteen direct Z3 replays passed: both correspondences and both retained
  classifications were UNSAT, retained nonvacuity and all four witnesses were
  SAT, and all ten mutation correspondences were SAT.
- The 16 target-specific tests and 11 v3 preservation-policy tests passed.
- The package runner passed with all required mutations and witnesses.
- All 681 repository tests and all 53 task-native acceptance commands passed.

The accepted exact-output and full-state classifications remain
`conditional-complete`, protected prior packages remain unchanged, and stage
transition remains disabled.
