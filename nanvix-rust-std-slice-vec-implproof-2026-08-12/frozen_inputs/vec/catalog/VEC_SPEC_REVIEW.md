# Vec Spec Evidence Review

The isolated `alloc::vec` artifact set accounts for all 49 stable executable API rows: 24 exact existing-vstd baseline rows, 24 generated executable `assume_specification` rows, and 1 justified no-spec row.

Relational pointer/provenance, iterator/adaptor, callback, MaybeUninit, conversion, and mutable-reference outcomes are recorded honestly rather than strengthened to force determinism.

## Audited totals

| Metric | Count |
| --- | ---: |
| Catalog rows / stable unique `alloc::vec` exec APIs | 49 |
| Existing vstd baseline rows preserved | 24 |
| New generated executable contracts | 24 |
| Justified-no-spec rows | 1 |
| Determinism `R0=UNSAT` | 4 |
| Determinism `R0=SAT` | 0 |
| Determinism `R0=UNKNOWN` | 15 |
| Determinism unsupported | 5 |
| Determinism Verus error | 0 |
| Determinism runner crash | 0 |

## UNKNOWN reason taxonomy

| UNKNOWN reason class | Rows | Reason |
| --- | ---: | --- |
| `callback-trace-boundary` | 8 | FnMut/FnOnce or Clone effects are modeled by ordered source callback traces, preserving relational outcomes. |
| `conversion-allocation-boundary` | 1 | Conversion preserves logical sequence while allocation identity/lifetime provenance remains boundary state. |
| `iterator-adaptor-state-boundary` | 2 | Iterator/adaptor values expose modeled remaining sequences but keep opaque lifetime/drop state. |
| `raw-pointer-provenance-boundary` | 4 | Pointer address, provenance, and allocation layout are not uniquely recoverable from the Vec Seq view. |

## Machine evidence

Latest feedback-pipeline manifest: `verification/evidence/vec_feedback_determinism/merged-all-20260811T1519Z/run_manifest.json`.
Status counts: `{'ok': 19, 'unsupported_mut_ref_return': 5}`.
R0 counts: `{'unknown': 15, 'unsat': 4, 'unsupported': 5}`.

Per-target evidence directories include candidate, active contract code, synthetic `__rust_std_candidate`, determinism spec/harness, Verus stdout/stderr aliases, schema-search evidence, and result payloads.
