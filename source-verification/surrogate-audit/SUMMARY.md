# Source-surrogate and fidelity audit

The word `verified` below refers to the suite's pre-audit label.
Verus did not directly prove any original Rust std symbol: 405 accepting
artifacts verify mapped local `source_*` surrogate functions, while one
accepting artifact has a target-mapping failure.

## Conservative result

| Pre-audit suite label | Strict-faithful and admissible surrogate | Known mismatch/inadmissible | Source body unresolved | No passing artifact | Total |
|---|---:|---:|---:|---:|---:|
| Verified | 139 | 51 | 0 | 0 | 190 |
| Unverified / external body | 29 | 186 | 1 | 133 | 349 |
| **Overall** | **168** | **237** | **1** | **133** | **539** |

- Strict-faithful local-surrogate coverage: **168/539 (31.17%)**.
- Among Verus-accepting artifacts: **168/406 (41.38%)**.
- Within the pre-audit verified label: **139/190 (73.16%)**.
- Within all pre-audit unverified records: **29/349 (8.31%)**.
- Reclassified one-click suite: **168 local-surrogate proofs + 371 external-body fallbacks; 539 passed, 0 failed**.

The remaining 1 unresolved record is the declaration-only
`write_box_via_move` compiler intrinsic. `Tracked` and `Ghost` are known
absent/non-std targets, not unresolved Rust std implementations.

## What the proof object actually is

| Pre-audit suite label | Original std symbol | Mapped local surrogate | Wrong/ambiguous target | No passing artifact | Total |
|---|---:|---:|---:|---:|---:|
| Verified | 0 | 190 | 0 | 0 | 190 |
| Unverified / external body | 0 | 215 | 1 | 133 | 349 |

Thus no accepting artifact establishes the external-symbol contract by
machine-checked linkage; source fidelity is an audit judgment.

## Extra unrelated functions in per-record proof files

- Full shared preproved bundle copied per record: **91/539 (16.88%)**, representing **14** unique bundles.
- Any unrelated API surrogate present: **92/539 (17.07%)**.
- Pre-audit verified: **48/190 (25.26%)**.
- Pre-audit unverified: **54/349 (15.47%)**.

The extra unverified case outside the 101 shared bundles is the incorrect
TryFrom artifact that contains only the TryInto surrogate.

## First-pass mutually exclusive classification

| Classification | Pre-audit verified | Pre-audit unverified | Overall |
|---|---:|---:|---:|
| Exact executable body | 77 | 17 | 94 |
| Mechanical desugaring | 64 | 19 | 83 |
| Alternate implementation | 45 | 140 | 185 |
| Circular/target-axiom dominant issue | 2 | 38 | 40 |
| Source body unresolved | 2 | 1 | 3 |
| Ambiguous/wrong target mapping | 0 | 1 | 1 |
| No passing artifact | 0 | 133 | 133 |

Exact/mechanical totals are 177, but 9 artifacts are not admissible proofs. Known
examples include `CString::as_c_str`, which depends on a target-critical
representation axiom, and one `BTreeMap::contains_key` surrogate with
no target postcondition. The final conservative count is therefore 168.

Body fidelity and proof admissibility are separate dimensions in
`source-resolution-overrides.json`; the table above preserves the
older mutually exclusive first-pass category for other records.

## Exhaustive resolution of the former 104 unknown-source records

| Dimension | Category | Count |
|---|---|---:|
| Body fidelity | Exact | 37 |
| Body fidelity | Mechanical desugaring | 30 |
| Body fidelity | Alternate implementation | 34 |
| Body fidelity | No Rust body | 3 |
| Proof admissibility | Ordinary/acyclic | 72 |
| Proof admissibility | Target-critical axiom | 29 |
| Proof admissibility | Wrong/missing target | 2 |
| Proof admissibility | Unresolved intrinsic | 1 |

## Proof-artifact reuse in the retained set

- Strict-faithful records: **168**.
- Unique strict proof-file contents: **141**.
- Strict records copied from shared bundles: **33** across **6** bundles.

## Canonical API paths

- Paths with at least one strict-faithful admissible record: **129/447 (28.86%)**.
- Paths whose every direct record is strict-faithful and admissible: **115/447 (25.73%)**.

Per-record classifications and reasons are in `records.csv`; aggregate
machine-readable counts are in `summary.json`.
