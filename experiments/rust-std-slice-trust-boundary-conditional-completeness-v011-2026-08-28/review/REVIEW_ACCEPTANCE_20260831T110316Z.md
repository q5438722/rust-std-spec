# Independent Reviewer decision: target 029

**VERDICT: ACCEPT**

This acceptance covers only input order 29,
`core::slice::binary_search_by`. It does not classify the other 61 selected
targets and does not authorize a stage transition.

## Fresh verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

The command reported `acceptance=PASS` for all 11 command records. Python
compilation exited successfully, the unit suite ran 65 tests and reported
`OK`, the local validator reported `validation=PASS`, and the frozen Verus
harness reported `verification results:: 9 verified, 0 errors`.

The target captures recorded clean zero-exit runs with empty stderr:

| Obligation or replay | Result |
|---|---|
| General completeness modulo reviewed equivalence | `sat` |
| Fixed nonmonotone counterexample | `sat` |
| Sorted-domain sanity | `unsat` |
| Exact-output duplicate obligation | `sat` |
| Fixed duplicate witness | `sat` |
| Independent witness replay | `passed` |

## Review findings

| Check | Decision |
|---|---|
| Contract fidelity | Accepted. `Requires_T` restricts the counterexample search to length two but adds no sortedness. `Spec_T` preserves unconditional result bounds and the generated ordered-implies-`Ok`/`Err` relation rather than injecting the implementation's deterministic choice. |
| Boundary adequacy | Accepted. The shared boundary consists of element-read values, per-element comparator observations, and callback transition deltas backed by the frozen source and proof inventory. Hint behavior is modeled as deterministic source semantics. No selected index, returned `Result`, aggregate final state, answer-equivalent field, or selected execution trace occurs in the boundary. |
| Reviewed equivalence | Accepted. Result tags and callback final state remain exact; `Err` indices remain exact; distinct `Ok` indices are equivalent only when both identify `Equal` observations, as permitted by the public duplicate-match documentation. |
| General witness | Accepted. Under one fixed `[Greater, Less]` profile and state-preserving callback boundary, both `Ok(0)` and `Err(0)` satisfy the active relation because the profile is unordered, while their different tags violate reviewed equivalence. |
| Sorted and duplicate checks | Accepted. Exhaustive independent replay covered all six ordered length-two comparator profiles and found every valid result pair equivalent modulo matching index. The `[Equal, Equal]` witness admits distinct `Ok(0)` and `Ok(1)` results, which are exactly unequal but matching-index-equivalent. |
| Negative and boundary probes | Accepted. The six required regressions reject sortedness strengthening, blanket unsorted equivalence, answer-bearing callback data, an opaque whole-target relation, a selected trace, and deterministic implementation-choice injection. Additional SMT probes rejected wrong length, mismatched element reads, an out-of-bounds `Ok` index, and an inconsistent callback state; a zero-valued duplicate case remained satisfiable. |
| Scope and preservation | Accepted. Exactly target 029 has both result fields set to `conditional-incomplete`; the other 61 rows remain `not-run`, only the target-029 evidence directory is present, the pipeline state remains delivery/software/staged, and no recent writes appeared in the assigned read-only inputs. |

