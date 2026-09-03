# Independent Reviewer decision: search-wrapper cluster

**VERDICT: ACCEPT**

**Timestamp:** 2026-08-31T18:41:22Z

This decision covers only input orders 028
`core::slice::binary_search`, 030 `core::slice::binary_search_by_key`, and
065 `core::slice::partition_point`. It does not authorize a stage transition.

## Prior finding

The blocker in `REVIEW_FINDINGS_20260831T181324Z.md` is resolved. Both the SMT
and Verus definitions for targets 028 and 030 now include the reviewed
`binary_search_by` lower relation as an unconditional wrapper conjunct.
Concrete upper-unsorted/lower-ordered probes for both wrappers are UNSAT when
the lower relation is negated.

## Boundary and theorem review

- Each target has separate completeness-modulo-reviewed-equivalence,
  exact-output, and ordered-domain or partitioned-domain sanity obligations.
  `Requires_T` fixes only the length-two experiment domain and adds no
  sortedness or partitioning.
- Target 028 fixes source reads, Ord outcomes, and callback-state deltas.
  Target 030 additionally fixes extracted keys. Target 065 fixes source reads,
  predicate outcomes, and callback-state deltas. No boundary contains an
  index, `Result`, aggregate final state, answer encoding, or execution trace.
- The retained answer-bearing delegation and result-bridge sites are excluded
  and replaced by defined wrapper transitions backed by the canonical wrapper
  bodies and the accepted target-029 lower relation. No excluded retained site
  backs a boundary field.
- Targets 028 and 030 compare result tags, Err indices, and callback final
  state exactly. Distinct Ok indices are equivalent only when both shared
  observations identify matches. Target 065 compares its index and callback
  final state exactly.
- Direct content comparison bound each active contract, formatted generated
  declaration, canonical Rust item and public docs, frozen harness,
  transformation manifest, dependency manifest, source-body manifest, and
  canonical lower source excerpt to the packaged evidence.

## Fresh verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

The driver completed all 26 commands and reported `acceptance=PASS`. Its
compile step completed with status zero and empty stdout/stderr. The unit suite
ran 199 tests and reported `OK`.

| Target | General | Sanity | Exact output | Fixed SAT replays | Verus |
|---|---|---|---|---|---|
| 028 | SAT | ordered-domain UNSAT | SAT | passed | 3 verified, 0 errors |
| 030 | SAT | ordered-domain UNSAT | SAT | passed | 3 verified, 0 errors |
| 065 | SAT | partitioned-domain UNSAT | SAT | passed | 3 verified, 0 errors |

All solver commands exited zero with empty stderr. The concrete replay for
each SAT classification uses one fixed input and boundary for both executions.
The target-028 and target-030 exact-output witnesses use two matching duplicate
Ok indices; their general witnesses use unordered profiles with inequivalent
Ok/Err tags. The target-065 witnesses use one non-partitioned predicate profile
with distinct exact indices. Exhaustive sanity replay covered 18 ordered
profiles and 27 valid result pairs for each search target, plus all three
partitioned Boolean profiles for target 065.

All three experiment-local Verus models separately type-checked with
`--no-verify`, then verified with `3 verified, 0 errors`; stderr was empty and
no model contains `external_body`.

Independent boundary probes also established:

- ordered 028 and 030 profiles admit the exact Err insertion index and reject
  a wrong Err index;
- the all-true target-065 profile admits index 2 and rejects index 1;
- all three wrappers reject a wrong callback final state and an invalid
  length-one input;
- matching duplicate Ok indices satisfy reviewed equivalence, while distinct
  Err indices do not.

The fail-closed suite covers answer-bearing delegation, opaque result bridges,
callback-state loss, ordering/partitioning loss, sortedness/partitioning
strengthening, output laundering, the previously missing lower-transition
branches, and out-of-scope ledger mutation.

## Scope and preservation

The CSV and JSON crosswalks agree on 62 unique rows. Exactly 14 targets are
classified and 48 remain `not-run`; rows 028, 030, and 065 contain the six
requested `conditional-incomplete` result cells. A direct recursive content
comparison around the fresh acceptance run found no change in any of the 11
previously certified evidence trees.

**No stage transition is authorized by this review.**
