# Independent Reviewer findings: targets 078-079

**VERDICT: CHANGES REQUIRED**

This review covers only input orders 078
`core::slice::select_nth_unstable_by` and 079
`core::slice::select_nth_unstable_by_key`. It does not authorize a Manager
stage transition.

## Fresh verification

Readable-content inspection bound both generated declarations, canonical Rust
items and public docs, frozen harnesses and manifests, private `select.rs` and
partition source, callback vocabulary, and all six trust records per target.
`D001` and `C001` remain context-only, only `D004` is admitted, and
`D002`, `D003`, and `E001` remain excluded. The current candidate ledger has
27 classified rows and 35 `not-run` rows.

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
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_authority_design.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

Compilation succeeded. The targeted suite ran 17 tests and the full suite ran
285 tests; both reported `OK`. Each Verus file reported
`verification results:: 8 verified, 0 errors`. The cluster runner and local
validator reported `PASS`, and the acceptance driver passed all 31 commands.
These mechanical checks do not detect the semantic findings below.

## Blocking findings

### F1: The SAT witnesses expose a non-functional boundary, not conditional incompleteness

For target 078, `tools/selection_callback_targets.py:89-167` puts two
next-state deltas in `Boundary` and defines one `CompareStep` to accept either
delta for the same callback state and arguments. For target 079, `KeyStep` and
`OrdLtStep` at lines 210-257 are arbitrary relations that can likewise contain
multiple next states for the same invocation. The fixed relations constructed
at lines 1782-1884 deliberately admit both outcomes.

Both reported counterexamples keep the input, selected slice, returned
references, callback arguments, and callback result fixed. They differ only
because that one shared relation permits two next states for the identical
source invocation. This means the boundary does not determine the missing
callback observation. It is evidence for `boundary-insufficient`, not a
fixed-observation witness for `conditional-incomplete`.

The Reviewer added functionality constraints to the two temporary fixed
obligations: identical callback state and arguments must determine the same
result, next state, and panic outcome. Z3 returned `unsat` for both targets.
The temporary probes were removed. Thus neither retained SAT counterexample
survives when the shared boundary actually fixes the callback transition it
claims to observe.

### F2: `Spec_T` accepts callback traces that the frozen source cannot execute

`InteriorCallbackTraceNormal` at
`tools/selection_callback_targets.py:901-927` chooses an arbitrary positive
call count and arbitrary input identities. It is not connected to the pivot
choices, swaps, partition steps, intermediate sequences, or narrowing windows.
`MainNarrowingSteps`, `PartitionTransition`, and
`RecursiveLoopOrFallbackTransition` at lines 1024-1180 constrain only the
single final sequence and do not consume the callback trace.

The concrete interior branch for a non-ZST length-three slice and index one
enters `insertion_sort_shift_left(v, 1, is_less)`. The canonical helper at
`core/src/slice/sort/shared/smallsort.rs:580-604` visits tail positions one
and two, and `insert_tail` at lines 542-576 performs at least one callback at
each position. An all-equal length-three input therefore performs exactly two
adapter invocations.

The Reviewer fixed a functional, non-panicking callback relation and asked
each delivered `Spec_T` for that same all-equal length-three execution with
only one adapter invocation represented in the final callback state. Z3
returned `sat` for both 078 and 079. The temporary probes were removed. This
is a source-impossible execution admitted by the production obligation, so
the claimed arbitrary-length introselect/callback model is not source-backed.
The standalone panic probes are similarly not connected to `Spec_T`;
`PanicPrefixTransition` at lines 955-963 only asserts the normal,
non-panicking path.

### F3: The Verus files do not verify either target transition or theorem

`proofs/078_core_slice_select_nth_unstable_by.rs` and
`proofs/079_core_slice_select_nth_unstable_by_key.rs` prove eight local facts
about a branch number, pair swap, integer window shrinkage, the literal value
16, and returned-length arithmetic. They contain no `Requires_T`,
`Boundary_T`, `Spec_T`, `Equivalent_T`, six-conjunct active contract, mutable
slice execution, partition transition, or two-execution theorem.

The corresponding test at
`tests/test_selection_callback_cluster.py:346-351` checks only that the files
lack the text `external_body` and contain two function names. The source and
contract mutation test at lines 157-180 rejects any text that differs from
the same generator; it does not establish semantic reachability. Consequently
the eight verified obligations are not Verus evidence for the requested
target-local models.

Replace the non-functional callback relation with observations that fix each
source transition, or classify the target as `boundary-insufficient` if doing
so would require a forbidden realized trace. Couple an internal existential
execution to every callback, sequence mutation, partition, narrowing, fallback,
panic prefix, and final subslice step, including the small-sort path. Add
regressions for both functionality-constrained fixed witnesses and both
length-three one-adapter probes. Make each Verus file verify the target-local
transition and two-execution property rather than disconnected arithmetic
lemmas. Then regenerate only 078-079, rerun the complete acceptance campaign,
and request independent review again.

The current 078-079 result cells are candidate values and are not independently
accepted. **No stage transition is authorized by this review.**
