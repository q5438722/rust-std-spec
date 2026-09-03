# Independent Reviewer addendum: target 079 operational v1

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T21:25:30Z

This decision covers only the additive operational-v1 evidence for input order
079, `core::slice::select_nth_unstable_by_key`. It does not alter the
certified campaign result, the accepted target-078 package, or Manager-owned
state.

## Source-model review

The repaired target-079 composition structurally parses every imported
`mkExactState` constructor instead of matching pretty-printed fragments. All
14 constructors derive abort from their source state, and all seven active
CopyOnDrop or gap-restoration stores preserve the interrupted sequence when
that source state has aborted. Ordinary panic still performs the accepted
target-078 restoration. The former dead cleanup wrappers are absent.

The adapter transition follows the Rust 1.96 MIR and ten replayable process
probes: `f(left)`, `f(right)`, `PartialOrd::lt`, right-key destruction, then
left-key destruction. It distinguishes the two owned key identities and
covers normal return, every panic prefix, destructor panic during normal
destruction, unwind cleanup, and immediate abort when a destructor panics
during an existing unwind. The accepted target-078 selection interpreter is
reused only as source-backed semantics; no target-078 classification is
inherited.

The shared boundary contains total functional key, `Ord::lt`, Drop, and
callback-state observations. It excludes realized calls, destruction
schedules, pivots, mutations, returned ranges, selected answers, final state,
and traces. The theorem is intentionally narrower than unrestricted public
Rust execution: classification requires every runtime key result to project
to the state-independent contract key and the reviewed Ordering relation to
be a total order. Under that explicit condition, the boundary remains
strictly below the target and does not encode its answer.

## Obligation and sensitivity review

Both arbitrary-valid-length obligations share one valid input, configuration,
and boundary. They bind the exact active six-conjunct contract through the
source-backed target transition. The first rejects unequal principal returns;
the second rejects unequal principal returns or any unequal final/interrupted
state field. A concrete non-ZST execution asserts both `TargetDefinition_T`
and `Spec_T`, and the ZST force case does the same.

Seventeen target-079 selection force probes cover ZST, extrema, insertion and
CopyOnDrop, recursive pivot selection, every partition kernel, ancestor-pivot
handling, both narrowing directions, the sixteen-step fallback,
median-of-ninthers, and return projection. Their 17 paired mutations are
UNSAT. Nine adapter force probes are SAT and nine paired source-transition
mutations are UNSAT. Dedicated regressions distinguish ordinary restoration
from abort bypass for both CopyOnDrop and partition gap guards.

## Independent execution

Fresh reviewer execution compiled the Python sources, replayed all ten Rust
ground-truth scenarios, passed 18 lifecycle/composition tests and 15
formal/artifact tests, and ran the additive target runner. Direct Z3 replay
returned clean UNSAT for principal-return determinism and full-state
conditional completeness and SAT for the nonvacuity witness. The trusted-free
Verus artifact type-checked and reported `7 verified, 0 errors`. All 540
repository unit tests passed.

The reviewer-owned replay gate captured all 12 required commands. The final
target runner passed with independent review accepted, and all 46 acceptance
commands passed. Those gates also confirmed that the certified target-078
package, target-079 baseline, frozen authorities, campaign ledgers and
reviews, and `research/PIPELINE_STATE.json` remained unchanged while only the
additive target-079 package was regenerated.
