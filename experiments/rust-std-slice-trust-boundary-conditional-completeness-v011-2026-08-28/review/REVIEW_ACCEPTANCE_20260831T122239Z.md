# Independent Reviewer decision: target 106

**VERDICT: ACCEPT**

This acceptance covers only input order 106,
`core::slice::splitn_mut`. It preserves the accepted target-013 and target-029
classifications, leaves 59 selected targets unclassified, and does not
authorize a stage transition.

## Fresh verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

The command reported `acceptance=PASS` for all 13 command records. Python
compilation completed successfully, 93 tests ran and reported `OK`, local
validation reported `validation=PASS`, and the target-106 Verus constructor
harness reported `verification results:: 5 verified, 0 errors`.

The freshly regenerated target captures had zero exit status and empty stderr:

| Obligation or replay | Result |
|---|---|
| Full exact-output-and-state theorem | `unsat` |
| Exact-output theorem | `unsat` |
| Independent solver replay | `passed` |
| Verus type-check | passed |
| Verus verification | 5 verified, 0 errors |

## Review findings

| Check | Decision |
|---|---|
| Contract fidelity | Accepted. Direct comparison with the active generated declaration and shared vocabulary confirmed all ten initial iterator-view conjuncts: well-formedness, source, remaining range, empty yielded prefix, empty remainder, forward direction, limit, nonnegative limit, forward composition, and predicate totality. The predicate clause is classical totality and does not observe the callback during construction. |
| Source model | Accepted. Canonical Rust source confirms `splitn_mut` calls `split_mut` and then `SplitNMut::new`; `split_mut` calls `SplitMut::new`; those constructors store the mutable slice and predicate unchanged, initialize `finished=false`, and store `count=n`. The SMT and Verus models derive these fields rather than importing an opaque target or iterator-view relation. |
| Boundary adequacy | Accepted. `Boundary_T` contains only the input allocation, mutable-borrow, and predicate identities shared by both executions. It excludes the returned iterator/view, selected ranges, callback results or transitions, private state, final state, answer-equivalent encodings, and traces, so it is narrower than the target. |
| Exact equivalence | Accepted. The full theorem compares all 21 return/private iterator observations and all 8 final-state observations exactly, including ranges, reference identity, predicate identity/state, `finished`, `count`, direction, callback count, mutable final slice, and final callback state. The exact-output theorem retains exact equality for all 21 output observations. |
| Solver evidence | Accepted. Both retained target obligations and an independent replay returned exact `unsat` with empty stderr. No SAT classification, opaque diagnostic relation, selected output, or weakened equivalence is used. |
| Verus evidence | Accepted. The experiment-local constructor model follows the source bodies, exposes no target-body `external_body`, and verifies the constructor transition and exact two-execution theorem. |
| Negative and boundary probes | Accepted. The 93-test suite rejects omission of each active conjunct, opaque whole-target and iterator-view relations, returned-view or selected-range laundering, constructor-time predicate observations, weakened exact equality, wrong `n`, incorrect flags, nonempty initial yielded/remainder state, identity mismatches, and out-of-scope row mutation. Independent probes additionally checked every exact equality, theorem argument ordering, valid empty input, invalid negative domains, boundary mismatch, and 12 contradictory constructor observations. |
| Scope and preservation | Accepted. CSV and JSON contain the same 62 selected rows. Targets 013 and 029 retain their accepted classifications, target 106 alone receives this increment's two `conditional-complete` results, and exactly 59 rows remain `not-run`. |

