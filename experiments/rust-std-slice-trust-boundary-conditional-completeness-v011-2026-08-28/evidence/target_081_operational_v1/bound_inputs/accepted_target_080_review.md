# Independent Reviewer addendum: target 080 operational v1

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-02T16:20:13Z

This decision covers only the additive operational-v1 package for input order
080, `core::slice::sort_unstable`, under model
`target-080-operational-v1-rust-1.96-complete`. It does not change either
certified target-080 classification, select target 080 as an operational-v2
overlay, or authorize a Manager-owned stage transition.

## Source fidelity and boundary

Direct content comparison matched every bound input to its declared origin.
The generated contract requires permutation and sorting by the observed `Ord`
relation. Rust 1.96 rustdoc explicitly permits equal elements to be reordered,
so exact public-contract output remains `conditional-incomplete` while
completeness modulo reviewed equal-`Ord` permutation remains
`conditional-complete`.

The primary model follows the canonical public adapter, ZST and trivial
returns, configuration heapsort dispatch, insertion sort, existing-run
detection and reversal, specialized small sorts, `CopyOnDrop`, recursive pivot
selection, all three partition kernels, both gap guards, recursive-left and
iterative-right quicksort, imbalance fallback, and panic restoration. The
separate reference interpreter reconstructs those transitions without
importing the target-080 model.

The only admitted trust site is the source-used `Ord::lt` callback. Its
boundary supplies total per-call ordering, next-state, and panic observations
indexed by callback state and compared element identities. Classification
requires the implementation ordering at every state to equal one
state-independent contract total preorder. State-indexed symbolic orderings
remain diagnostic only. The boundary contains no realized schedule, pivot,
partition or swap choice, output, final state, permutation, execution trace,
or precomputed terminal state, and is strictly narrower than the target. The
prior whole-sort postcondition and opaque external body are replaced by
source-backed transitions.

## Correspondence, witnesses, and proof

Both generated obligations start from each retained source sequence and the
boundary initial state. They replay source-derived callback, swap, and
origin-backed write transitions and compare against the independent
interpreter. The full result comparison includes sequence, callback state,
panic, abort, terminal status, unit return, and helper return index. Direct Z3
replay is UNSAT for both field-complete correspondence and exact
output/terminal-state correspondence. Nonvacuity is SAT; all 26 source-force
probes and all 15 source-semantic mutations are SAT.

All 28 retained witnesses replay with field-complete equality and identical
callback schedules. They cover normal and panic paths, duplicate order
classes, existing runs, configuration dispatch, all small-sort
specializations, all partition variants, restoration guards, recursion, and
heapsort. The trusted-free Verus projection contains no `assume`, `admit`,
`external_body`, or precomputed terminal result and reports 5 verified with 0
errors. Removing the sequence projection is rejected.

## Independent execution and preservation

The Reviewer ran `PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py`
from command 1. All 54 commands succeeded, including compileall, 17 focused
operational-v2 certification tests, 725 complete repository tests, the
target-080 runner, and the final authority validator. The target runner
reported 28 witness replays, 26 SAT force probes, 15 SAT semantic mutations,
two UNSAT correspondence obligations, and Verus 5 verified with 0 errors.

A direct pre/post content comparison found no change or deletion among 832
files named by preservation policies v1-v4 and the protected Manager state.
The live target-specific review brief is separate from the frozen historical
operational-v2 request; legacy reconciliation and certification consume the
versioned historical inventory without reopening the live brief. This
acceptance is valid only when registered by the exact one-review
`preservation/path_policy_v5.json` successor.
