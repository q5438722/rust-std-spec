# Independent Reviewer findings: targets 078-079, round 2

**VERDICT: CHANGES REQUIRED**

This review covers only input orders 078
`core::slice::select_nth_unstable_by` and 079
`core::slice::select_nth_unstable_by_key`. It does not authorize a Manager
stage transition.

## Authority, trust, and boundary observations

Readable inspection found both active declarations, target source items and
public docs, frozen implementation-proof inputs, private selection and
partition source, callback vocabulary, and six trust records per target.
`D001` and `C001` remain context-only, only `D004` is admitted, and
`D002`, `D003`, and `E001` remain excluded. The new callback observations are
functional arrays over state and arguments. Target 078's adapter makes one
`compare(a, b)` observation followed by exact comparison with
`Ordering::Less`; target 079 threads `f(a)`, `f(b)`, and `Ord::lt` in that
order. No selected output, final slice, final callback state, realized trace,
or call count was found in `Boundary_T`.

Those repairs address the first round's non-functional callback relation, but
they do not make the arbitrary-length target transition source-backed.

## Fresh execution

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
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_authority_design.py
```

Python compilation succeeded. The targeted suite ran 18 tests and reported
`OK`. Each Verus file type-checked and reported
`verification results:: 4 verified, 0 errors`. The target runner reported its
candidate 27 classified / 35 `not-run` ledger.

The full suite ran 286 tests and failed with three errors in
`test_maybeuninit_lifecycle_cluster.py`. All three reject the newly populated
078 result as a changed preserved/later result. Consequently
`tools/run_acceptance.py` failed at `02_unit_tests`, and local validation
failed because that required acceptance log is unsuccessful.

## Blocking findings

### F1: The arbitrary-length callback transition contradicts the cited source

For every interior non-ZST slice other than length three,
`InteriorCallbackTraceNormal` in
`tools/selection_callback_targets.py:1048-1111` supplies the callback schedule.
Its special length-four branch admits either one or two adapter calls. Its
generic branch admits any positive call count and any pair of identities from
the input. Neither branch is coupled to pivot selection, intermediate
sequences, swaps, partition operations, narrowing windows, or fallback
execution.

The frozen `select.rs` takes every interior slice of length at most 16 through
`insertion_sort_shift_left(v, 1, is_less)`. The canonical helper initializes
`tail` at offset one, calls `insert_tail` once per loop iteration, and advances
`tail` by one until the one-past-end pointer. For an all-equal length-four
slice, each `insert_tail` makes one false adapter call and returns, so the
source executes exactly three adapters. The frozen small-sort excerpt stops
immediately before the canonical `tail = tail.add(1)` statement, so its bound
range is also insufficient to justify the claimed loop schedule.

An independent in-memory probe fixed that source case in each delivered
`Spec_T` and invoked `z3 -in -smt2`. Expected states were derived from the
canonical loop and target source adapters, not from the generated
obligations:

| Target | Final callback state | Source meaning | Z3 |
|---|---:|---|---|
| 078 | 1 | one adapter, impossible | `sat` |
| 078 | 2 | two adapters, impossible | `sat` |
| 078 | 3 | three adapters, required | `unsat` |
| 079 | 3 | one key adapter, impossible | `sat` |
| 079 | 6 | two key adapters, impossible | `sat` |
| 079 | 9 | three key adapters, required | `unsat` |

The delivered model therefore accepts both source-impossible executions used
by the boundary-gap diagnostic and excludes the real source execution.

### F2: Missing source semantics are misclassified as an insufficient boundary

`PartitionTransition` and `MainNarrowingSteps` at
`tools/selection_callback_targets.py:1204-1379` constrain the one aggregate
final sequence. They do not derive pivot choices, intermediate mutations,
partition callback calls, or the state threaded through those calls.
`PanicPrefixTransition` at lines 1142-1151 only excludes a panicked returned
state; the separate `PanicPrefixReachable` predicate is not called by
`TargetDefinition_T`.

With a fixed functional callback observation and a deterministic source
program, the realized schedule must be derived internally by the source
transition. It must not be placed in `Boundary_T`, but its omission does not
show that the genuine callback boundary is insufficient. Under the accepted
classification policy this is a `missing-source-backed-model` condition until
the source execution is expressed. The four general SAT results and two
length-four diagnostics are artifacts of the omitted transition and cannot
support `boundary-insufficient`.

### F3: The Verus obligations are bounded examples, not target-local general models

Both files fix `index == 1`, exactly three equal identities, a non-panicking
equal comparison, and an unchanged final triple. Their shared-boundary theorem
therefore verifies only the repaired length-three example. They do not model
arbitrary lengths, min/max paths, ZSTs, pivot selection, partition mutations,
shrinking windows, fallback, or panic prefixes. Function names matching the
requested theorem do not make these fixed examples evidence for the general
target transition.

The corresponding tests check symbol occurrence and exact equality with the
same generator. They do not fail closed when a semantically incorrect
source schedule is generated, as the length-four probe demonstrates.

### F4: Required full tests and acceptance do not pass

The three stale preservation failures in
`tests/test_maybeuninit_lifecycle_cluster.py:413-547` are reachable from the
required full suite. This is a hard delivery failure independently of the
semantic findings.

Replace the arbitrary callback trace with source-coupled transitions for
small-sort and introselect execution, including intermediate arrays and
callback states, partition/pivot calls, narrowing, fallback, and panic
prefixes. Add the length-four three-adapter case as a permanent fail-closed
regression and expand the bound small-sort excerpt through the loop advance.
If the general transition cannot be expressed in this mission, use
`missing-source-backed-model` rather than `boundary-insufficient`. Extend the
Verus models beyond the fixed length-three example, repair the downstream
preservation fixtures, regenerate only 078-079, and rerun the full acceptance
campaign before requesting another independent review.

The candidate 078-079 result cells are not independently accepted.

