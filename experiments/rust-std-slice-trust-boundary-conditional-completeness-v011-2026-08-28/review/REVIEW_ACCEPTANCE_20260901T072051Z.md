# Independent Reviewer decision: mutable split-at primitives

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T07:20:51Z

This decision covers only input orders 085
`core::slice::split_at_mut_checked` and 086
`core::slice::split_at_mut_unchecked` against the independently accepted
45-target baseline. It does not authorize a Manager stage transition.

## Semantic and boundary review

The active declarations, shared `split_point_in_range` vocabulary, target
source and public docs, lower pointer/raw-slice/intrinsic sources, frozen
implementation-proof artifacts, and all 18 trust records were checked by
readable content. The four retained answer-bearing sites remain blocked. The
new obligations replace them with defined source transitions rather than
admitting or relabeling them.

`mid` remains part of shared input `x`. The shared boundary contains only the
initial slice address, allocation, provenance, parent-borrow identity, element
size, and element alignment. It contains no branch result, unsafe-domain
decision, pointer result, subtraction result, region, returned reference,
derived borrow, final state, answer encoding, or trace.

The checked path selects `Some` exactly for `mid <= len`; the unchecked path is
restricted to that same valid domain. Both models derive the canonical
slice-to-thin mutable pointer cast, `ptr.add(mid)`, `len - mid`, raw regions
`[0,mid)` and `[mid,len)`, structural left/right reference identities, unique
derived borrows, and immediate left-then-right frame composition. The retained
length-as-address/null-provenance helper is not used. The `mid = len` model
retains the one-past-end pointer, and nonempty zero-sized regions use logical
range disjointness while permitting equal addresses.

Both theorem projections use one shared valid input and one shared boundary
for the two executions. Exact-output equivalence compares every modeled
return and reference-identity field. Full equivalence additionally compares
every pointer, region, borrow, and immediate final-state field.

## Independent execution

- `python3 -m compileall -q -f tools tests` completed with no diagnostics.
- All 16 focused tests passed. A separate source-derived probe covered all 11
  required source cases, falsified all 781 modeled output/state field
  expectations at once per case, checked each boundary field, and rejected
  the invalid unchecked domain.
- The four retained theorem obligations replayed as UNSAT, 11 source cases
  replayed as SAT with models, and 23 semantic/domain probes replayed as
  UNSAT.
- Both generated Verus files type-checked and verified two obligations with
  zero errors and contain no `external_body`.
- The bounded runner and local validator passed at 47 classified and 15
  `not-run` rows. Only rows 085 and 086 extend the accepted baseline.
- `python3 tools/run_acceptance.py` passed all 37 commands. Its full test
  capture reports 385 passing tests.
- A direct recursive content comparison preserved 3,882 files across all 45
  previously certified evidence trees and all 320 frozen-input files. The two
  crosswalk formats remained content-equivalent and unchanged during review.

