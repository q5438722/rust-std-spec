# Independent Reviewer decision: exact mutable iterator partitions

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T05:54:12Z

This decision covers only input orders 035
`core::slice::chunks_exact_mut` and 068
`core::slice::rchunks_exact_mut` against the independently accepted 40-target
baseline. It does not authorize a Manager stage transition.

## Semantic and boundary review

The active generated contracts, shared iterator vocabulary, public source and
docs, private constructors, implementation-proof harnesses and manifests, and
all 12 trust records were checked by readable content. The forward constructor
derives `rem = len % chunk_size`, splits at `len - rem`, stores the divisible
prefix in raw `v`, and retains the suffix remainder. The reverse constructor
derives the same remainder, splits at `rem`, retains the prefix remainder, and
stores the divisible suffix in raw `v`.

The shared boundary contains only initial slice address, allocation,
provenance, unique parent-borrow identity, and element layout. It excludes
remainder arithmetic, split index, partition ranges and orientation, returned
or private iterator state, raw and reference identities, direction, output,
final state, answer encodings, and traces. Those observations are derived by
the source-backed transitions. Region disjointness is range-based, so
nonempty zero-sized regions may have equal addresses.

The primary equivalence compares all 34 iterator/output observations and all
10 immediate final-state observations exactly. The exact-output projection
omits only those 10 final-state fields. Both targets therefore support
`conditional-complete` for exact-output determinism and for completeness
modulo the reviewed exact equivalence.

## Independent execution

- Python compilation completed cleanly; all 15 focused exact-partition tests
  and all 355 repository tests passed.
- An independent source-derived probe falsified all 44 principal fields for
  each of the 12 required source cases and rejected a true composition-order
  swap for both targets.
- The bounded runner replayed four theorem obligations as UNSAT, 12 source
  instances as SAT with retained models, and 16 negative probes as UNSAT.
  Every target tree retains 19 command/stdout/stderr/status capture groups.
- Both generated Verus files type-checked and independently verified three
  obligations with zero errors; neither contains `external_body`.
- A before/after readable-content comparison preserved 3,267 files across all
  40 certified evidence trees and all 320 frozen-input files. The CSV and JSON
  crosswalks remain content-equivalent with 42 classified and 20 `not-run`
  rows.
- `python3 tools/run_acceptance.py` passed all 35 commands. The local validator
  confirmed 120 generated contracts, exactly 62 selected UNKNOWN rows, 58
  excluded prior-UNSAT rows, 12 excluded exact-vstd rows, and the 42/20 result
  ledger.
