# Independent Reviewer decision: target 013

**VERDICT: ACCEPT**

This acceptance covers only input order 13,
`core::slice::as_chunks_mut`. It preserves the accepted input-order-29
baseline, leaves 60 selected targets unclassified, and does not authorize a
stage transition.

## Fresh verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

The command reported `acceptance=PASS` for all 12 command records. Python
compilation completed successfully, 77 tests ran and reported `OK`, local
validation reported `validation=PASS`, and the experiment-local Verus harness
reported `verification results:: 8 verified, 0 errors`.

The retained target captures had clean zero-exit runs with empty stderr:

| Obligation or replay | Result |
|---|---|
| Full exact-output-and-state theorem | `sat` |
| Fixed `N=2`, length-3 counterexample | `sat` |
| Exact-output theorem | `unsat` |
| Independent witness replay | `passed` |

## Review findings

| Check | Decision |
|---|---|
| Contract fidelity | Accepted. Direct comparison with the active generated declaration confirmed partition, both initial lengths, both initial subrange properties, both final lengths, the final frame, and both final subrange properties. The retained two-conjunct contract is not used. |
| Source model | Accepted. The arbitrary-length model follows the nonzero assertion, rounded-down length, unchecked mutable split, and unchecked mutable chunk conversion. Output ranges and reference identities are derived structurally from the shared input rather than supplied as opaque functionality. |
| Boundary adequacy | Accepted. `Boundary_T` contains only the input allocation and mutable-borrow identities. Returned references, chunks, remainder, aggregate final state, answer encodings, and traces are absent, so the boundary is narrower than the target. |
| Equivalence | Accepted. The full theorem compares every principal return field, both structural reference identities, and every final-state field exactly. The separate exact-output theorem projects only final state while retaining all final contract conjuncts existentially. |
| Full-state witness | Accepted. One fixed positive chunk size, length-three input, and shared boundary admits identical source-derived outputs but two distinct concrete final slices. Independent replay checked all ten active conjuncts for both executions and rejected full exact equivalence. |
| Exact-output proof | Accepted. The clean real-solver `unsat` result covers arbitrary nonnegative modeled lengths and positive chunk sizes; it is not restricted to the concrete witness. |
| Verus evidence | Accepted. The experiment-local harness proves the strengthened representative contract for `N=2`, length 3 while retaining and disclosing the three audited lower-transition external bodies. Frozen provenance was not edited. |
| Negative and boundary probes | Accepted. Tests reject retained-contract substitution, each strengthened-conjunct omission, output/final-state laundering, opaque whole-target relations, selected traces, weakened final equality, and out-of-scope row mutation. Reviewer probes additionally covered empty input, remainder-only and even partitions, zero chunk size, negative modeled length, mismatched boundary identity, theorem argument order, reference equality, and final-conjunct retention. |
| Scope and preservation | Accepted. CSV and JSON contain the same 62 selected rows: target 013 has the new split classification, target 029 retains its certified classification, and exactly 60 rows remain `not-run`. The target-013 writer is confined to its evidence root and a result-only crosswalk update; non-target row changes fail closed. |
