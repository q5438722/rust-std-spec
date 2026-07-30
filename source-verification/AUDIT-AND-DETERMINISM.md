# Proof fidelity and specification determinism

## Why direct contracts are duplicated

There are **539 direct contract records** but only **447 canonical API paths**:

- 92 records disappear after path-level deduplication;
- 33 API paths have more than one direct contract record.

This usually does not mean duplicated Rust implementation code. A record keeps
the concrete implementation type, generic bounds, cfg/source variant, and
source location, while the canonical path intentionally collapses them.

Examples:

- `Clone::clone`: 18 concrete implementations;
- `Default::default`: 16 concrete implementations;
- `PartialEq::eq`: 9 implementations;
- `RangeBounds::{start_bound,end_bound}`: 7 range types each;
- `BTreeMap::{get,contains_key,remove}`: separate borrowed-key/bound variants.

Detailed records are in `duplicates/records.csv`.

## Strict proof/source fidelity

The first bulk run produced 406 Verus-accepting artifacts. A second exhaustive
audit separated proof-object identity, source-body fidelity, proof
admissibility, and source-resolution quality.

No artifact directly proves an original Rust std symbol. Of the 406 accepting
artifacts, 405 map to local `source_*` surrogate functions and one has an
incorrect target mapping.

| Conservative result | Count |
|---|---:|
| Strict-faithful admissible local surrogates | **168** |
| Known mismatch, inadmissible proof, or wrong mapping | 237 |
| Source body unresolved | 1 |
| No passing artifact | 133 |
| **Total direct records** | **539** |

The sole unresolved record is the declaration-only
`write_box_via_move` compiler intrinsic.

Retained surrogate proof levels:

| Level | Count |
|---|---:|
| A | 54 |
| B | 112 |
| C | 2 |

The conservative organized suite verifies:

```text
539 passed, 0 failed
168 strict-faithful local-surrogate records (141 unique proof artifacts)
371 external-body fallbacks
```

Detailed verdicts:

- `surrogate-audit/SUMMARY.md`
- `surrogate-audit/records.csv`
- `fidelity-report/SUMMARY.md`
- `fidelity-verdicts.json`

## Determinism/completeness of all direct contracts

Record-level results for all 539 direct `assume_specification` declarations:

| Category | Count |
|---|---:|
| Complete, nontrivial (`R0 = unsat`) | **382** |
| Solver `unknown` | 120 |
| Trivial/opaque equality | 4 |
| No local postcondition | 16 |
| Checker unsupported after rerun | 17 |
| SMT-confirmed incomplete (`R0 = sat`) | **0** |

Thus **382 / 539 (70.87%)** are automatically established as complete under
the checker’s equality policy. `unknown` is inconclusive, not complete.

At unique API-path level:

| Category | Count |
|---|---:|
| Every direct contract record complete | **339** |
| Mixed complete/non-complete records | 3 |
| Unknown-only | 77 |
| Trivial-only | 2 |
| No-local-postcondition-only | 3 |
| Checker unsupported | 17 |
| Mixed no-postcondition/unknown | 6 |
| **Total unique API paths** | **447** |

For the 168 strict-faithful admissible local-surrogate records:

| Record category | Count |
|---|---:|
| Complete | **125** |
| Unknown | 20 |
| Trivial equality | 4 |
| No local postcondition | 14 |
| Checker unsupported after rerun | 5 |

So **125 / 168 (74.40%)** of the conservatively retained surrogate records are
also deterministically complete.

Detailed determinism artifacts:

- `determinism-report/SUMMARY.md`
- `determinism-report/records.csv`
- `determinism-report/apis.csv`
- `determinism-all/targets/`

## Paired determinism-feedback comparison

Both columns below use the same **2,121 generation targets**. The no-feedback
column is recovered from saved round-0 histories; the with-feedback column uses
the saved final result. Spec generation itself was not rerun for this report.
The final result also applies anti-vacuity and static suitability guards; it is
not a pure determinism-only refinement.

| Status | No feedback | With feedback |
|---|---:|---:|
| Complete | **150** | **225** |
| Solver `unknown` | 68 | 40 |
| Trivial equality | 19 | 3 |
| No specification or checker failure | 1,884 | 1,853 |
| SMT-confirmed incomplete (`sat`) | 0 | 0 |

| Completeness metric | No feedback | With feedback |
|---|---:|---:|
| Add-spec proposals | 462 | 280 |
| Checker-valid contracts | 237 | 268 |
| Complete contracts | 150 | 225 |
| Complete among checker-valid | **63.29%** | **83.96%** |

## Paired source-proof comparison

The 357 distinct checker-valid contract variants were all attempted against
their Rust 1.96 implementations. Of 201 Verus-passing artifacts, strict source
review retained 146 and rejected 55.

| Proof status | No feedback | With feedback |
|---|---:|---:|
| Strict-faithful admissible proof | **89** | **99** |
| Verus pass rejected by fidelity review | 36 | 24 |
| No passing proof | 112 | 79 |
| No checker-valid specification | 1,884 | 1,919 |
| Strict proof rate among checker-valid contracts | **37.55%** | **49.01%** |
| Strict proof rate among complete contracts | **42.67%** | **49.69%** |

## Why no specification was produced

| Reason | No feedback | With feedback |
|---|---:|---:|
| Runtime or hidden state | 463 | 456 |
| Missing vstd abstraction | 360 | 346 |
| Trait contract integration | 201 | 201 |
| Concurrency or hidden state | 175 | 179 |
| Unsafe/representation sensitive | 134 | 150 |
| Determinism checker unsupported | 110 | 124 |
| Iterator/adapter result model | 101 | 101 |
| Formatting effect | 68 | 67 |
| Toolchain unavailable | 70 | 70 |
| Representation or allocator state | 36 | 40 |
| Higher-order contract | 64 | 39 |
| Ownership/uninitialized model | 22 | 25 |
| Complex result/pattern model | 20 | 20 |
| Associated type/projection | 16 | 17 |
| No modeled observable output | 9 | 9 |
| Missing borrowed-key/ordering model | 0 | 4 |
| Missing pointer identity/provenance model | 30 | 3 |
| Non-functional Clone/Default semantics | 5 | 2 |

Full paired rows, transition matrices, reason descriptions, and proof outcomes:

- `feedback-comparison/SUMMARY.md`
- `feedback-comparison/records.csv`
- `feedback-comparison/summary.json`
