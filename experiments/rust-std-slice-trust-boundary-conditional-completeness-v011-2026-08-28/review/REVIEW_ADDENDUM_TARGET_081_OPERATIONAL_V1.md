# Independent Reviewer addendum: target 081 operational v1

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-02T19:36:13Z

This decision covers only the additive operational-v1 package for input order
081, `core::slice::sort_unstable_by`, under model
`target-081-operational-v1-rust-1.96-complete`. It does not change either
certified target-081 public-contract classification, select target 081 as an
operational-v2 overlay, or authorize a Manager-owned stage transition.

## Source fidelity and boundary

Direct content comparison matched all 26 bound inputs to their declared
origins, including the active generated contract, canonical Rust 1.96 source
and rustdoc, implementation-proof artifacts, accepted target-080 private-sort
transition, and its independent acceptance. The public implementation at
`core/src/slice/mod.rs:3188-3193` evaluates `compare(a, b)` once and tests
`Ordering::Less` only after that evaluation returns. Both operational adapters
therefore expose a latent `Less` diagnostic on a panicking callback while
setting `less_tested` and `is_less` false, propagating callback and observable
element-interior state before unwind.

The admitted boundary is limited to total per-call callback observations:
exact `Ordering`, callback next state, observable element-interior next state,
and panic, plus the corresponding callback-destruction observations indexed
by unwind mode. The comparison schedule, pivots, partitions, swaps, writes,
output sequence, aggregate final state, and execution trace are derived by the
source transition and are not boundary inputs. The boundary is consequently
strictly narrower than the target. Callback destruction after normal return,
destruction during comparator unwind, normal destruction panic, and
double-panic abort remain distinct.

## Correspondence, witnesses, and proof

All 31 paired witnesses replay field-for-field against the separate public
adapter and accepted independent private-sort interpreter. They preserve exact
sequence multiplicities and cover normal, panic, and abort terminals; single
callback evaluation; callback and observable interior-state transitions;
equal-key classes; non-total comparators; trivial and ZST returns; insertion,
small-sort, partition, recursion, restoration, and heapsort paths.

Direct Z3 replay is UNSAT for accepted-private source correspondence,
Ordering-to-`Less` adapter correspondence, and fixed-boundary operational
determinism. Nonvacuity and all ten branch-force probes are SAT. All nine
source-semantic mutations are SAT, including duplicate callback evaluation,
testing equality as less, discarded callback/interior/panic effects, skipped
destruction, ignored destruction panic, and collapsed double panic. The
trusted-free Verus composition contains no `assume`, `admit`,
`external_body`, axiom, or precomputed terminal result and reports 11 verified
with 0 errors.

## Retained classifications and preservation

The retained exact-output and reviewed-equivalence obligations replay SAT,
while the total-order sanity restriction replays UNSAT. The concrete retained
witnesses independently satisfy the active permutation and sortedness
contract: equal-key reordering disproves exact output, and a fixed non-total
comparator permits contract-valid outputs outside reviewed equal-key
equivalence. This agrees with Rust's documentation that equal elements may be
reordered and that output is unspecified for a non-total comparator. Both
certified public-contract classifications therefore remain
`conditional-incomplete`; the additive source-operational determinism and
field-complete correspondence results are `conditional-complete`.

The archive validator resolves the accepted target-080 version through five
explicit mappings, rejects missing, altered, traversing, duplicate, or
unmapped archive content, and keeps target 081 outside the operational-v2
overlay set. A pre/post direct comparison found no change or deletion among
all 204 files in the reviewed v6 package, policies v1-v6, and protected
Manager state.

The Reviewer ran `PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py`
from command 1. All 55 commands succeeded, including Python compilation,
target-081 solver and Verus replay, operational-v2 reconciliation, 17
certification tests, 754 complete repository tests, and the final local
validator. This acceptance is valid only when registered as the sole review
record in the exact v6 successor `preservation/path_policy_v7.json`.
