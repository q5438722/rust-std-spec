# Independent Reviewer decision: target 081

**VERDICT: ACCEPT**

This acceptance covers only input order 81,
`core::slice::sort_unstable_by`. It preserves the independently accepted
target-013, target-029, target-106, and authority/design baselines, leaves 58
selected targets unclassified, and does not authorize a stage transition.

## Fresh verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

The command reported `acceptance=PASS` for all 14 command records. Python
compilation completed successfully, 106 tests ran and reported `OK`, local
validation reported `validation=PASS`, and the target-081 Verus model reported
`verification results:: 3 verified, 0 errors`.

The Reviewer also replayed the five target/equivalence SMT files directly.
The general reviewed-equivalence and exact-final-slice obligations returned
`sat`, the total-order sanity obligation returned `unsat`, and both standalone
equal-key equivalence witnesses returned `sat`. An independently implemented
witness checker confirmed both executions satisfy the active contract,
preserve exact multiplicities and callback final state, and have the required
equivalence polarity. Exhaustive enumeration covered 13 total-order profiles
and 66 pairs of contract-sorted results without finding a reviewed-equivalence
counterexample.

## Review findings

| Check | Decision |
|---|---|
| Contract fidelity | Accepted. Direct textual comparison with the frozen generated declaration confirmed the two active postconditions: input/final permutation and comparator-observed sortedness. The SMT expands exact multiplicities and all six `i <= j` comparisons for its declared length-three domain; `Spec_T` is an exact call to that target definition rather than an opaque whole-sort relation. |
| Source and documentation | Accepted. The frozen Rust item forwards the comparator through `compare(a, b) == Ordering::Less` to the private unstable sorter. Its public documentation explicitly permits reordering equal elements and states that a non-total comparator can leave the normally returned order unspecified. |
| Boundary adequacy | Accepted. The shared boundary contains only the three input identities, the finite comparator result table, and a state-preserving callback transition. It contains no final sequence, chosen permutation, selected ordering, answer encoding, pivot/swap decisions, or complete trace. The answer-bearing retained sites `TS-081-D002`, `TS-081-D003`, and `TS-081-E001` are excluded rather than relabeled; only callback site `TS-081-D004` supplies admitted observations. |
| Exact-output witness | Accepted. One total comparator places two distinct identities in the same equal-key class. Both permutations satisfy the contract and share callback final state; they are reviewed-equivalent but have different exact final slices. |
| General witness | Accepted. One fixed non-total comparator reports each of two identities as `Less` than the other. Both permutations satisfy exact multiplicity and comparator-sortedness under the same boundary, but their position-wise identities are not comparator-equivalent. |
| Reviewed equivalence | Accepted. Unit return and callback final state remain exact. The relation requires exact identity multiplicities in both directions and bidirectional comparator equality at every position. The positive equal-key reorder is admitted, while the foreign same-key identity witness is rejected by the multiset requirement. |
| Total-order sanity | Accepted. The separate total-order restriction is absent from the primary theorem and makes its negated reviewed-equivalence theorem `unsat`. Independent exhaustive enumeration confirms the result for the complete three-identity domain. |
| Verus evidence | Accepted. The experiment-local model defines permutation, comparator-sortedness, equality classes, callback state, and both concrete SAT witnesses without an `external_body`; it freshly type-checks and verifies with 3 verified obligations and 0 errors. |
| Negative probes | Accepted. The fresh suite rejects opaque whole-sort relations, answer-bearing permutation and trace boundaries, omission of either active conjunct, removal of multiset equality, foreign identities, injection of a total-order precondition into the primary theorem, and mutation of any non-target crosswalk row. |
| Scope and preservation | Accepted. CSV and JSON contain the same 62 selected `core::slice` UNKNOWN rows. Target 081 alone has this increment's two `conditional-incomplete` results, targets 013, 029, and 106 retain their certified results and exact file contents across a target-081 rerun, and exactly 58 rows remain `not-run`. |

