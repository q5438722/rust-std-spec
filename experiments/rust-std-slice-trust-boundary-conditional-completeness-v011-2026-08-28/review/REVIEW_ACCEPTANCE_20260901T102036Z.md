# Independent Reviewer decision: raw-slice addressed-memory pair

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T10:20:36Z

This decision covers only input orders 048 `core::slice::from_raw_parts` and
049 `core::slice::from_raw_parts_mut` against the independently accepted
49-target baseline. It does not authorize a Manager stage transition.

## Semantic and boundary review

Both generated declarations, the shared raw-domain vocabulary, the canonical
Rust source items and public safety documentation, all four frozen
implementation-proof artifacts per target, and all six trust records were
checked by readable content.

`TS-048-D001` and `TS-049-D001` remain context-only specification vocabulary.
`TS-048-D002`/`TS-048-E001` and `TS-049-D002`/`TS-049-E001` remain
inadmissible answer-bearing or complete-target support. None is admitted into
`Boundary_T`; each excluded pair is replaced by explicit source transitions
for the UB precondition, raw fat-pointer construction, and reference
dereference.

The retained implementation-proof boundary is therefore not relabeled as the
conditional proof boundary. The replacement boundary is narrower than the
public target and contains only initial address-indexed memory and
initialization, allocation and provenance, one-allocation facts, alias
permissions, element layout and platform limits, and root borrow/frame
observations. It contains no returned reference or sequence, raw fat-pointer
result, final storage, answer encoding, target truth, or execution trace.

Both theorem projections use one shared input `x` and one shared boundary `b`.
The source model constructs each returned element from the initialized cell at
`data + index * size_of::<T>()`; zero-sized elements reuse `data`, and an empty
one-past slice performs no memory read. It preserves immutable memory and
reference identity. For the mutable constructor it preserves identity,
exclusivity, and the outside frame without inventing a final-memory clause
that the active contract does not contain.

The reviewed domain covers allocated nonempty slices, allocated and dangling
empty slices, allocated and dangling nonempty ZST slices with equal endpoint
addresses, initialized values, one-allocation bounds, immutable no-mutation
aliasing, mutable exclusivity, `isize` multiplication fit, address no-wrap,
and permitted one-past endpoints. Negative obligations reject null and
misaligned empty/ZST pointers, missing allocation or provenance for nonzero
spans, multi-allocation and out-of-allocation spans, uninitialized elements,
alias violations, overflow, incorrect pointwise memory or return fields,
state-identity drift, boundary mismatch, answer laundering, weakened
equality, invented mutable final frames, and out-of-scope ledger edits.

Exact-output equivalence compares every modeled return/reference field.
Full-state equivalence additionally compares every modeled state field.

## Independent execution

- Forced Python compilation completed for the seven raw-slice implementation,
  validator, test, and authority-design files.
- All 17 focused raw-slice tests passed. The complete repository suite ran 418
  tests and passed.
- Both trusted-free Verus models type-checked independently. Each verified two
  obligations with zero errors and contains no `external_body`.
- Target 048's full-state and exact-output theorem projections replayed as
  UNSAT. Target 049's exact-output projection replayed as UNSAT, while its
  full-state projection replayed as SAT.
- All 14 retained source instances replayed as SAT with models, and all 54
  retained negative probes replayed as exact UNSAT.
- The fixed-input/fixed-boundary mutable witness replayed as SAT. Both
  executions return the same initial sequence `[10, 20, 30]`; their final
  in-range memories are `[101, 202, 303]` and `[404, 505, 606]`, and full-state
  equivalence is false. The difference is confined to final memory omitted by
  the active contract.
- The bounded runner and local raw-slice validator passed at 51 classified
  rows and 11 `not-run` rows. The complete acceptance driver passed all 39
  commands.

## Preservation and decision

A direct byte-for-byte comparison before and after the fresh acceptance run
preserved all 4,475 files in the 49 accepted evidence trees and all 320 frozen
input files. The live evidence directory set is exactly the 49-target baseline
plus targets 048 and 049. The 62-row ledger contains exactly 51 classified and
11 `not-run` rows, with 048 and 049 as the only additions to the accepted
baseline.

Target 048 is accepted as conditional-complete for exact output and full
state. Target 049 is accepted as exact-output conditional-complete and
full-state conditional-incomplete. Stage transition remains disabled.
