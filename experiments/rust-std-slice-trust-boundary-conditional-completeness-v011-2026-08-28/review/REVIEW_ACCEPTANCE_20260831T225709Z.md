# Independent Reviewer decision: target 077

**VERDICT: ACCEPT**

**Timestamp:** 2026-08-31T22:57:09Z

This decision covers only input order 077
`core::slice::select_nth_unstable`. It does not classify targets 078-079 or
authorize a Manager stage transition.

## Authority, trust, and boundary review

- Direct readable-content comparisons bind the active contract and generated
  declaration, canonical Rust item and public docs, generated selection
  vocabulary, frozen implementation-proof harness, transformation manifest,
  dependency manifest, and source-body record.
- All five `TS-077` records are present. `TS-077-D002` and `TS-077-E001`
  remain excluded, `TS-077-D001` and `TS-077-C001` remain context-only, and
  only `TS-077-D003` backs the shared `Ord` implementation and extensional
  class observations.
- `Boundary_T` contains no pivot, selected permutation, returned subslice,
  final state, answer encoding, swap/pivot choice, or execution trace. It is
  narrower than the target.
- The source-backed replacement covers valid bounds, ZST behavior,
  minimum/maximum scans, swap/permutation preservation, partitioning,
  strictly shrinking introselect windows, the 16-step fallback edge, and
  final returned ranges. The experiment-local Verus model contains no
  `external_body`.

## Theorem, equivalence, and witnesses

The primary SMT obligation uses one arbitrary positive-length input and one
shared `Ord` boundary for both executions. Input identity/class/rank summaries
are recursively derived from the physical initial sequence. Final identity
and side-class summaries are recursively derived from each physical final
sequence. Both active-contract instances are conjoined before negating the
reviewed equivalence.

The reviewed relation preserves returned range identities and lengths, exact
whole-input identity multiplicity, pivot rank and `Ord` class, left/right
class multiplicities, allocation identity, mutable-borrow identity, and final
length. It relaxes only the documented ordering freedom in the two unsorted
sides and pivot identity among equal-class elements, as permitted by
`core/src/slice/mod.rs:3461-3513`.

Direct Z3 replay returned `unsat` for the general reviewed-equivalence
obligation. The fixed-input, fixed-boundary exact-output obligation returned
`sat`; both executions satisfy the active contract and reviewed relation
while their final sequences differ. Positive side-reordering and equal-pivot
witnesses replayed, and the foreign-identity, wrong-rank/class,
partition-crossing, malformed-range, and state-drift candidates were rejected.
The stale-summary foreign-identity and partition-crossing regressions, plus
same-input rank-summary uniqueness and small-sort reachability regressions,
all returned `unsat`.

An independent contract implementation checked the concrete witnesses and
domain edges without importing the target runner. Exhaustive enumeration of
16,739 finite total-order-class domains through length five found no pair of
contract-satisfying results outside the reviewed equivalence, while retaining
exact-output and equal-pivot non-uniqueness.

Replacing each source-transition call individually with `true` left the
general theorem `unsat`: the active generated contract and sequence-derived
summaries already entail the reviewed relation, so the completeness result
does not depend on an over-constraining source path. Separately, deleting the
recursive/fallback transition makes the dedicated small-sort reachability
probe `sat`, confirming that the source relation is semantically live.

## Fresh Reviewer execution

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m compileall -q tools tests
PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s tests -p test_target_077.py -v
../../verus/source/target-verus/release/verus \
  proofs/077_core_slice_select_nth_unstable.rs --crate-type=lib --no-verify
../../verus/source/target-verus/release/verus \
  proofs/077_core_slice_select_nth_unstable.rs --crate-type=lib
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_target_077.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_authority_design.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

Compilation and Verus type-checking completed successfully. The targeted suite
ran 17 tests and the full suite ran 268 tests; both reported `OK`. Verus
reported `verification results:: 5 verified, 0 errors`. The target runner and
local validator reported `PASS`, and the acceptance driver passed all 30
commands.

Direct before/after content comparison preserved all 24 certified evidence
trees, every frozen input for targets 077-079, and every non-result crosswalk
field. Only target 077 has the new result pair; targets 078-079 remain
`not-run`. The selected ledger has 25 classified and 37 `not-run` rows.

Target 077 is accepted as exact-output `conditional-incomplete` and
completeness modulo reviewed selection equivalence `conditional-complete`.
No stage transition is authorized by this review.
