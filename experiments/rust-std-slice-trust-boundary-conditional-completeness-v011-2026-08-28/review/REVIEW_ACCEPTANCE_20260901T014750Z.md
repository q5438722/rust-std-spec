# Independent Reviewer decision: targets 078-079

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T01:47:50Z

This decision covers only input orders 078
`core::slice::select_nth_unstable_by` and 079
`core::slice::select_nth_unstable_by_key`. It accepts
`missing-source-backed-model` for both result columns; it does not claim either
full target conditionally complete or conditionally incomplete and does not
authorize a Manager stage transition.

## Authority, trust, and boundary review

Readable-content inspection binds each active declaration, canonical source
item and public docs, frozen implementation-proof harness and manifests,
private selection/partition/small-sort source, callback vocabulary, and all
six trust records. D001 and C001 remain context-only. Only D004 supplies
genuine callback observations. D002 is replaced only for the bounded
small-sort path; D003 and E001 remain excluded and explicitly unresolved.

The shared boundary contains callback identity, initial callback-visible
state, and functional relations over source-call arguments, results, next
state, and panic. It contains no realized call trace or count, pivot,
permutation, returned range, final callback state, final slice, selected
answer, or equivalent encoding. Target 078 performs exactly one
`compare(a,b)` call followed by equality with `Ordering::Less` and imposes no
comparator-totality premise. Target 079 evaluates `f(a)`, then `f(b)`, then
`Ord::lt`, threads every intermediate state, and permits the key for one
identity to vary between invocations.

Exact equality remains the reviewed equivalence for every returned reference
and length, pivot identity, entire final slice, allocation/borrow identity,
panic status, and callback-visible final state. No weaker selection
equivalence is used.

## Source model and classification

The emitted SMT is deliberately restricted to a valid non-ZST length-four,
index-one execution. It follows the canonical
`insertion_sort_shift_left(v, 1, is_less)` path through tails one, two, and
three. `InsertTailNormal` derives comparison arguments, callback states, and
each mutable rotation from the source. The panic relation follows the same
steps and restores the moved element through the `CopyOnDrop` gap guard.
Normal return constructs the exact left, pivot, and right references.

The two bounded theorem negations are UNSAT. SAT nonvacuity and canonical
source executions show that the theorem is not vacuous. UNSAT regressions
reject one- or two-adapter all-equal schedules, wrong descending/mixed/tail
rotations, and an unrestored post-shift panic state; the corresponding
source-valid executions and restored panic state are SAT. The retained
positive and negative witnesses replay against an independent insertion-sort
implementation.

The emitted obligations contain none of the former disconnected aggregate
introselect, partition, narrowing, fallback, or callback-trace relations.
There is still no source-backed operational model for arbitrary-length pivot
selection, lower-partition mutation and callbacks, ancestor-pivot handling,
shrinking introselect windows, the 16-step fallback, or their panic/unwind
semantics. Target 079 additionally lacks temporary-key drop transitions.
Those concrete omissions support `missing-source-backed-model` for both exact
output and completeness modulo reviewed equivalence. The bounded UNSAT
results are regression evidence only and are not promoted into full-target
classifications.

## Fresh Reviewer execution

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m compileall -q tools tests
PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s tests \
    -p 'test_selection_callback_cluster.py' -v
../../verus/source/target-verus/release/verus \
  proofs/078_core_slice_select_nth_unstable_by.rs \
  --crate-type=lib --no-verify
../../verus/source/target-verus/release/verus \
  proofs/078_core_slice_select_nth_unstable_by.rs --crate-type=lib
../../verus/source/target-verus/release/verus \
  proofs/079_core_slice_select_nth_unstable_by_key.rs \
  --crate-type=lib --no-verify
../../verus/source/target-verus/release/verus \
  proofs/079_core_slice_select_nth_unstable_by_key.rs --crate-type=lib
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_selection_callback_cluster.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_authority_design.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

Python compilation succeeded. The targeted suite ran 19 tests and the full
suite ran 287 tests; both reported `OK`. Each Verus file type-checked and
reported `verification results:: 5 verified, 0 errors`. The cluster runner and
local validator passed, and the acceptance driver passed all 31 commands.

Two additional in-memory SMT probes, with expected behavior derived from the
canonical source rather than the generated witnesses, were SAT: one retained
a source-valid execution while violating comparator totality on an unused
pair, and one retained a source-valid all-equal execution with keys that vary
by callback state. These probes confirm the intended callback boundary and
left-to-right key evaluation.

A separate in-memory pre/post snapshot compared file paths and bytes directly
while rerunning the cluster writer. It preserved all 25 certified evidence
trees and all three frozen selection input trees. Every non-result crosswalk
field and every out-of-scope crosswalk row was unchanged. The final ledger has
27 classified and 35 `not-run` rows.
