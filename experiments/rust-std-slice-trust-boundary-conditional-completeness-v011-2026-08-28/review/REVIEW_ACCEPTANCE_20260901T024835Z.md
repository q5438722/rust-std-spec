# Independent Reviewer decision: mutable iterator constructors

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T02:48:35Z

This decision covers only input orders 032 `core::slice::chunk_by_mut`, 036
`core::slice::chunks_mut`, 069 `core::slice::rchunks_mut`, 074
`core::slice::rsplit_mut`, 076 `core::slice::rsplitn_mut`, 093
`core::slice::split_inclusive_mut`, and 098 `core::slice::split_mut`. It does
not authorize a Manager stage transition.

## Prior findings

The Reviewer independently confirmed that the round-1 findings are repaired:

- Canonical-source anchors now fail closed for the `SplitMut`
  `finished=false` default, `RSplitNMut` count, and reverse-constructor order.
  The permanent tests demonstrate that the corresponding source-wrong SMT
  mutations remain structurally valid to the generic checker but are rejected
  by the target-specific reviewed-model guard.
- The target-074 Verus model represents
  `SplitMutStorage -> RSplitMutStorage`; target 076 represents
  `SplitMutStorage -> RSplitMutStorage -> GenericSplitNStorage ->
  RSplitNMutStorage`. Their explicit projection proofs derive the flat
  iterator fields, including `finished=false`, `reverse=true`, and `count=n`.
- The local validator lists all seven new classifications and derives
  `target_result_counts=34_classified,28_not-run`. A permanent regression test
  covers the detailed and aggregate summaries.

## Independent evidence review

The seven active contract hashes match the authority crosswalk. The retained
public/private source, frozen inputs, trust records, narrow boundaries,
literal shared-input/shared-boundary theorems, and exact return/final-state
equalities satisfy the review request. The Reviewer confirmed 14 clean UNSAT
obligations, 21 SAT source instances, seven clean Verus models without
`external_body`, preservation of all 27 certified evidence trees and all
seven frozen trees, the `TS-076-C003` citation reconciliation, unchanged
out-of-scope ledger cells, and disabled stage transition.

Fresh retained execution reports 21 focused tests and 308 full tests passing.
The supervised acceptance run recorded in
`.argus_subagents/constructor-acceptance-r2.json` completed with exit code
zero; `logs/acceptance_manifest.json` contains 32 successful commands.
