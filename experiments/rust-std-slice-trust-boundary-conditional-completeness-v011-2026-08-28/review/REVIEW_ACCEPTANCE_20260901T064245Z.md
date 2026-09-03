# Independent Reviewer decision: mutable fixed-chunk edges

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T06:42:45Z

This decision covers only input orders 062
`core::slice::last_chunk_mut`, 090
`core::slice::split_first_chunk_mut`, and 096
`core::slice::split_last_chunk_mut` against the independently accepted
42-target baseline. It does not authorize a Manager stage transition.

## Semantic and boundary review

The active generated declarations, shared fixed-array vocabulary, public
source and docs, frozen implementation-proof harnesses and manifests,
canonical lower split/pointer sources, and all 22 trust records were checked
by readable content. The retained row-090 synthetic length-address,
null-provenance helper is not reused: the new model composes the canonical
mutable slice pointer cast, checked raw-parts split, pointer addition,
array-pointer cast, and mutable dereference transitions.

For all three targets, `N` is part of shared input `x`. The shared boundary
contains only initial slice address, allocation, provenance, unique
parent-borrow identity, and element size. It excludes branch results, checked
arithmetic and split indices, ranges, array views, tuple orientation, returned
references, derived borrows, output, final state, answer encodings, and
traces.

The source transitions select `Some` exactly when `N <= len`.
`last_chunk_mut` and `split_last_chunk_mut` derive `len - N`;
`split_first_chunk_mut` splits at `N`. Prefix/suffix regions, array-only,
array-first, and array-second orientations, structural reference identities,
unique-borrow partitions, and immediate final frames follow those source
steps. Disjointness is range-based and admits equal addresses for nonempty
zero-sized regions.

Both theorem projections use the same valid input and boundary in both
executions. The primary equivalence compares every modeled return,
reference-identity, and immediate final-state field exactly; the exact-output
projection omits only final-state fields.

## Independent execution

- Python compilation completed cleanly; all 14 focused tests and all 369
  repository tests passed.
- A separate source-derived probe fixed every output and state field for all
  21 required target/case combinations and rejected three invalid input
  domains.
- The retained solver evidence independently replayed six theorem
  obligations as UNSAT, 21 edge/ZST instances as SAT with models, and 30
  semantic negative probes as UNSAT.
- All three generated Verus models type-checked and verified two obligations
  with zero errors and contain no `external_body`.
- The bounded runner and local validator passed. A direct readable-content
  comparison preserved 3,487 files across all 42 previously certified target
  trees and all 320 frozen-input files.
- Both crosswalk formats remain content-equivalent. The ledger contains the
  certified 42-target baseline plus only rows 062, 090, and 096, for 45
  classified and 17 `not-run` rows.
- `python3 tools/run_acceptance.py` passed all 36 commands and retained clean
  zero statuses. Its full test capture reports 369 passing tests, and the
  Slice inventory remains 132 stable entries with 12 exact-vstd exclusions.

