# Independent Reviewer decision: complete 62-target Slice campaign

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T15:28:54Z

This campaign-wide decision covers exactly the 62 active generated
`core::slice` targets whose active pre-upgrade result is `r0_z3=unknown`. It
accepts the additive conditional-obligation crosswalk and final results
dossier for this bounded mission. It does not classify excluded rows or
authorize a Manager-owned project-stage transition.

## Campaign-wide findings

| Check | Decision |
|---|---|
| Authority and scope | Accepted. An independent manifest/catalog join yields 120 generated Slice contracts split into 62 UNKNOWN and 58 UNSAT rows, plus 12 exact-vstd rows outside the generated set. The aggregate contains 62 unique targets, all `core::slice`, all with implementation-proof status B, and no Vec, Array, Option, String, exact-vstd, or prior-UNSAT leakage. |
| Active contracts and inputs | Accepted. Every aggregate row carries the exact active catalog contract text and binds the generated declaration, canonical Rust item and public docs, frozen harness, source-body record, transformation manifest, and dependency manifest. The active catalog controls the six chunk-contract drifts: `as_chunks`, `as_chunks_mut`, `as_chunks_unchecked`, `as_chunks_unchecked_mut`, `as_rchunks`, and `as_rchunks_mut`. |
| Crosswalk and trust sites | Accepted. The JSON and CSV projections contain one row per selected target and retain all 409 audited trust records. Each row separates the retained implementation-proof boundary from the new obligation boundary and joins shared observations, exclusions, source-backed replacements or transitions, source citations, proof scope, solver/Verus evidence, classification, and exactly one accepting target review. Missing or orphan target evidence, duplicate or orphan review mappings, trust-inventory divergence, and result/classification mismatches fail closed. |
| Target 029 boundary | Accepted. The deterministic manifest distinguishes the six executable lower sites retained by the implementation proof from the four sites that back actual `Boundary_T` observations. Only element reads and per-call comparator/state observations enter the shared boundary. Hint and loop support are source transitions or context, while the selected index, returned `Result`, aggregate final state, branch choice, answer encodings, and traces remain excluded. |
| Equivalence policy | Accepted. Exact principal return and final-state equality remains the default. Only rows 028-030 use matching-index equivalence and only rows 080-082 use equal-key unstable-sort reordering. Canonical Rust docs support both relaxations. The retained positive witnesses admit distinct matching indices or equal-key reorderings; the negative witnesses reject nonmatches, foreign identities, unequal classes, and callback/key-state drift. |
| Direct classification evidence | Accepted. Recomputed exact-output counts are 48 conditional-complete, 12 conditional-incomplete, and 2 missing-source-backed-model; full-state/reviewed-equivalence counts are 41, 19, and 2. Every completeness cell has a direct clean UNSAT obligation. Every incompleteness cell has a direct SAT obligation and a fixed-input, fixed-boundary SAT replay checked by its accepting incremental review. |
| Missing models | Accepted. Rows 078 and 079 use exact equivalence and remain `missing-source-backed-model` for both projections. Their length-four small-sort obligations are explicitly diagnostic-only. The unmodeled arbitrary-length pivot, partition, narrowing, fallback, mutation, callback/panic behavior, and target-079 temporary-key drop behavior prevent promotion of bounded UNSAT to a target classification. |
| Preservation | Accepted. Direct recursive byte comparison across the fresh run found no change in the 6,844 pre-existing evidence files, 320 frozen inputs, nine frozen authority-ledger artifacts, or any prior review file. The only campaign additions are the reviewed target-029/final aggregate artifacts and this decision. The assigned read-only inputs and `research/PIPELINE_STATE.json` were not written. |

## Fresh Reviewer execution

The Reviewer ran the complete task-native acceptance driver:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

It reported `acceptance=PASS` for all 44 commands. Forced Python compilation
completed successfully, and the complete unit suite ran 474 tests in 49.649
seconds and reported `OK`. The final reconciliation reported 62 rows with
exact counts `48/12/2` and full-state counts `41/19/2`.

An independent freshness audit found 1,164 distinct retained target capture
records rewritten by this run: 985 Z3 invocations, 123 Verus invocations, and
56 Python witness replays. Every capture exited successfully with empty
stderr. The Z3 captures comprised 587 UNSAT and 398 SAT results across
classifying obligations and guarded probes; 62 Verus verification runs
reported zero errors, with the remaining Verus captures serving as clean
type-checks.

The campaign therefore satisfies the bounded objective and its independent
Reviewer gate.
