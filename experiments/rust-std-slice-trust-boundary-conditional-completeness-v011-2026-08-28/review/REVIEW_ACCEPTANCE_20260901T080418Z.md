# Independent Reviewer decision: split-off pair

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T08:04:18Z

This decision covers only input orders 099 `core::slice::split_off` and 104
`core::slice::split_off_mut` against the independently accepted 47-target
baseline. It does not authorize a Manager stage transition.

## Semantic and boundary review

Both active declarations, the shared split-off vocabulary, canonical Rust
source and public docs, all source helpers used to derive slice identities,
all frozen implementation-proof artifacts, and all nine trust records were
checked by readable content. The mutable active declaration retains both its
initial returned-slice partition and its `final(ret.unwrap())` partition. The
corrected frozen harness remains negative provenance and is not substituted
into either obligation.

Range kind and index remain in shared input `x`. `Boundary_T` contains only
the initial slice address, allocation, provenance, parent-borrow identity,
element size, and element alignment. It contains no direction, split index,
overflow or bounds decision, derived region or borrow, returned value, final
state, answer encoding, or trace. All retained proof-boundary records are
replaced by source-defined transitions or retained only as call-closure
context; none is admitted as a boundary observation.

The target transitions derive StartInclusive-to-Back, End-to-Front,
EndInclusive checked addition and overflow-to-None, rejection exactly when
the resulting split index exceeds the receiver length, exact front and back
subranges, directional return and receiver reassignment, reference identity,
and unchanged None frames. The mutable transition additionally derives the
`mem::take` ownership transfer, temporary empty receiver, disjoint unique
borrows, returned/remaining identity, and ordered front-then-back final frame.
The one-past and nonempty zero-sized-type cases preserve logical region
identity even when addresses coincide.

Both theorem projections use one shared valid input and one shared boundary.
Exact-output equivalence compares every modeled option and returned-reference
field. Full equivalence additionally compares every helper, ownership,
region, borrow, receiver, and frame field.

## Independent execution

- Forced Python compilation completed without diagnostics, and all 16 focused
  tests passed.
- Both Verus models type-checked independently and each verified two
  obligations with zero errors; neither contains `external_body`.
- The bounded runner and local validator passed at 49 classified and 13
  `not-run` rows.
- Four retained theorem obligations replayed as clean UNSAT, 28 source
  instances replayed as SAT with models, and 20 semantic probes replayed as
  clean UNSAT. Both independent replay commands completed cleanly.
- A separate source-derived oracle covered all 28 target/case combinations,
  forced and falsified 2,380 output, state, and boundary expectations, and
  rejected 11 invalid input domains.
- The full acceptance driver passed all 38 commands. Its fresh unit-test
  capture reports 401 passing tests.
- Direct normalized-readable-content comparison preserved all 4,145 files in
  the 47 certified evidence trees and all 320 frozen-input files. Crosswalk
  and trust content remained unchanged during replay, and the classified set
  is exactly the accepted 47-target baseline plus rows 099 and 104.

