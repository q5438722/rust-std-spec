# Independent Reviewer addendum: target 079 adapter refinement v2

**VERDICT: ACCEPT**

**Date:** 2026-09-02

This decision covers only the additive constructive adapter-refinement package
for input order 079, `core::slice::select_nth_unstable_by_key`. It does not
alter operational-v1, operational-v2, parser-repair, campaign, or
Manager-owned stage artifacts. The Engineer-generated `result.json` remains
review-pending by design; this addendum is the independent verdict.

## Source and boundary review

The canonical Rust 1.96 item delegates to `partition_at_index` with the
adapter `f(a).lt(&f(b))`. The accepted operational-v1 source model establishes
the corresponding order `f(left)`, `f(right)`, `Ord::lt`, `drop(right)`, then
`drop(left)`, including unwind cleanup and abort when a destructor panics
during an existing unwind.

The new Verus transition takes only the shared `KeyOrdDropBoundary`, current
callback state, left source identity, and right source identity. Its boundary
maps expose total key, `Ord::lt`, and Drop result/state/panic observations.
Evaluation order, owned-key slots and identities, liveness, panic origin,
termination, terminal callback state, selection behavior, outputs, final
state, and traces remain source-derived. The boundary is therefore strictly
narrower than the target and contains no answer-bearing lifecycle input.

## Verus and SMT correspondence review

The Verus artifact contains no `assume`, `admit`, `external_body`, axiom, or
precomputed terminal result. Thirteen proof obligations cover construction,
owned-key identity, callback-state threading, normal execution, both key-panic
prefixes, reverse cleanup after `Ord::lt` panic, normal and unwind destructor
panics, and double-panic abort.

The bridge parses the expression ASTs and exact signatures of all 27 open-spec
semantic helpers. It translates boundary-map indices through the accepted
call-key datatypes, emits distinct `Refined*` functions, and compares every
scalar result and every `OwnedKey` or `AdapterFrame` selector. The single
symbolic counterexample query contains 113 comparisons and replays UNSAT.
Wrong return types, reordered or extra transition arguments, a missing
constructor field, and a field-type mismatch are rejected. Constraints for a
negative callback state, equal source identities, a negative abstract slot,
and both first-key panic values remain UNSAT. Three Verus-valid default,
boundary-selector, and propagated-field mutations replay SAT.

All six paired semantic mutations type-check and then fail Verus verification
on postconditions: step order, ownership slot, next state, panic propagation,
cleanup order, and panic/abort distinction.

## Independent execution

Fresh Reviewer execution produced these results:

- Python compilation passed.
- Verus type-check passed; verification reported `13 verified, 0 errors`.
- The package runner replayed adapter correspondence, exact output, and full
  state as UNSAT; nonvacuity replayed SAT.
- All six semantic mutations were rejected, and all three correspondence
  mutations replayed SAT.
- The 13 focused tests and all 601 repository tests passed.
- `tools/run_acceptance.py` passed all 50 commands.
- Direct before/after byte comparisons found no changes in the two protected
  certification trees or seven protected files.

The accepted exact-output and full-state classifications remain
`conditional-complete`, and stage transition remains disabled.
