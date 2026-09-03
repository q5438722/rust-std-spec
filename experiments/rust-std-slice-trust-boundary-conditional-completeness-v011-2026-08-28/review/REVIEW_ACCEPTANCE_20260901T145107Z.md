# Independent Reviewer decision: `align_to` pair

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T14:51:07Z

This decision covers only input orders 008 `core::slice::align_to` and 009
`core::slice::align_to_mut` against the independently accepted 60-target
baseline. It does not authorize a Manager-owned stage transition.

## Readable semantic review

The Reviewer inspected both literal active declarations, generated align
vocabulary, Rust 1.96 implementations and public docs, the canonical
`align_to_offsets` and `ptr::align_offset` bodies and docs, both frozen
implementation-proof harnesses, all eight bound manifests, all 20 trust
records, both theorem projections per target, the mutable witness, the
target-local Verus models, and retained command/solver captures. Integrity
identifiers were not used as evidence; authority and preservation were judged
from readable content, fresh execution, and direct byte-content comparison.

The active contracts are preserved literally. Retained sites
`TS-008-D004`/`TS-008-E005`/`TS-008-E006` and
`TS-009-D004`/`TS-009-E003`/`TS-009-E004` remain classified as mixed or
inadmissible answer-bearing support. The new obligations exclude those sites
and replace them with defined source transitions rather than relabeling them
as boundary observations.

Every theorem uses one shared valid input `x` and one shared boundary
observation `b`. `Boundary_T` contains only initialized input bytes, Slice
length/address/allocation/provenance, T/U layout and platform limits, the
transmute-validity precondition, live exclusive root-borrow state, and the
outside frame. It contains no generated opaque relation, alignment offset,
branch choice, gcd result, partition, decoded middle value, returned
identity, final memory/view, target truth, answer encoding, or execution
trace.

The replacement follows canonical source order: Slice pointer extraction;
element-stride `ptr::align_offset` with wrapping address semantics and the
`usize::MAX` no-solution result; ZST and `offset > len` branches; gcd/ts/us
`align_to_offsets` arithmetic; exact prefix/middle/suffix ranges; pointer
casts and additions; raw-slice construction; byte-derived typed middle
interpretation; returned allocation, provenance, and root identity; disjoint
mutable regions; and one relational final byte frame decoded into the final
T/U views.

Exact-output equivalence compares all modeled branch, offset, value, length,
address, allocation, provenance, borrow-root, mutability, and disjointness
observations. Full-state equivalence additionally compares final bytes and
T/U views, the outside frame, and backing identity. No reviewed equivalence
is weakened.

The immutable target fixes both the complete output and final frame. The
mutable target fixes its returned partition but permits legal writes through
the returned mutable regions. Its concrete fixed-input/fixed-boundary witness
changes one valid in-range byte, changes the corresponding T and U values,
re-derives every final view, and preserves outside memory and backing
identity. It is therefore a source-backed incompleteness witness, not
diagnostic SAT from an opaque relation.

## Independent execution

- Forced Python compilation completed successfully, and all 11 focused tests
  passed.
- The full repository suite executed 466 tests and passed.
- Each trusted-free target-local Verus model type-checked and verified six
  items with zero errors.
- Direct Z3 replay returned clean UNSAT for target 008 exact output and full
  state and target 009 exact output. Target 009 full state and its concrete
  fixed witness returned SAT.
- Independent replay covered 20 SAT source instances and 43 UNSAT
  invalid-domain, wrong-transition, wrong-field, frame, and
  answer-laundering probes.
- A separate source-derived exhaustive probe checked 486,240 valid
  layout/address/length combinations, including empty, ZST, aligned,
  misaligned, equal/greater offsets, no-solution alignment, nontrivial gcd,
  byte reinterpretation, and nondefault provenance cases.
- The bounded runner, focused evidence validator, integrated authority
  validator, and complete 43-command acceptance driver passed.

## Preservation and decision

A direct byte-content comparison after the complete acceptance replay found
all 60 certified predecessor evidence trees and all 320 frozen input files
unchanged. Both crosswalk serializations remained identical to the delivered
ledger, and the row-reset guard limits this increment to the two result fields
on rows 008 and 009.

Target 008 is accepted as exact-output and full-state
`conditional-complete`. Target 009 is accepted as exact-output
`conditional-complete` and full-state `conditional-incomplete`. The selected
ledger contains exactly 62 classified rows and zero `not-run`. Stage
transition remains disabled.
