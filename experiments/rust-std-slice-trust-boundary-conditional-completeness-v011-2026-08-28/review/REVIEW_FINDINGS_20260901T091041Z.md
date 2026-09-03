# Independent Reviewer findings: raw slice constructors

**VERDICT: CHANGES REQUIRED**

This review covers only input orders 048 `core::slice::from_raw_parts` and
049 `core::slice::from_raw_parts_mut` against the independently accepted
49-target baseline. It does not authorize a Manager stage transition.

## Verified observations

Readable-content inspection bound both active generated declarations, the
shared raw-domain vocabulary, canonical Rust source and public safety docs,
both frozen harnesses, all six frozen manifests, and all six trust records.
`TS-048-D001` and `TS-049-D001` remain context-only. The four answer-bearing
records remain explicitly inadmissible and are not admitted into `Boundary_T`.

Fresh Reviewer execution compiled the Python sources and passed all 15 focused
tests and all 416 repository tests. The bounded runner and raw-pair validator
reported 51 classified and 11 `not-run`. Both Verus models type-checked and
reported `2 verified, 0 errors` with no `external_body`. The retained solver
captures replayed target 048's full-state and exact-output obligations as
UNSAT, target 049's exact-output obligation as UNSAT, and target 049's
full-state obligation and fixed witness as SAT.

A direct path-and-byte comparison around an idempotent bounded rerun preserved
all 4,475 files in the 49 certified evidence trees and all 320 frozen-input
files. Both crosswalk representations were unchanged by that rerun.

## Blocking findings

### F1: Returned memory is copied from a logical answer array, not read pointwise from the pointer address

`tools/raw_slice_pair.py:245-266` places `x_memory` in the shared input and
`b_memory` in the boundary. `_boundary_equalities` equates them at line 419,
but `ReferenceDereferenceTransition` at lines 558-561 takes only `x` and `y`
and sets the complete `y_return_memory` array equal to `x_memory`. It never
uses the pointer address, element size, or `b_memory`. The active-return
translation repeats the same whole-array equality at line 569. The Verus
model likewise defines `source_output(input).memory` from `input.memory` and
requires `output.memory == input.memory` at lines 1562-1618.

This conflicts with the declared "address-indexed memory" boundary and the
objective's requirement to derive each returned element pointwise from
pointer-reachable memory. A source-derived Reviewer probe fixed the existing
valid non-ZST case at address 4096 and asserted that returned element zero
differs from boundary memory at address 4096. Z3 returned SAT: the returned
element was 10 while the boundary cell at the pointer address was 0. In the
generated case, values 10, 20, and 30 are stored at logical indices 0, 1, and
2 rather than at reachable addresses.

If the array is genuinely address-indexed, the dereference transition is
wrong. If it is instead a precomputed slice view, it is an answer-equivalent
sequence carried in `x` and duplicated into `b`, which the mission excludes.
In either interpretation, the clean theorem results do not establish the
requested conditional completeness.

Represent initial storage and initialization as genuine boundary memory, and
derive the finite returned view pointwise using the pointer address, element
size, length, provenance/allocation, and ZST rules. The target transition must
consume that boundary relation rather than copy a complete return sequence
from `x`. Mirror the same relation in Verus. Add a regression requiring the
Reviewer probe above, plus interior-element and one-past/ZST variants, to be
UNSAT.

### F2: The complete acceptance driver fails its final bounded-scope check

Fresh `python3 tools/run_acceptance.py` completed its compilation, 416-test
suite, all target runners, the raw-pair runner, and all read-only authority
checks successfully, then failed command `22_local_validator` with:

```text
validation=FAIL
ERROR target evidence exists outside the bounded target scope
```

`tools/validate_authority_design.py:1470-1527` builds the exact allowed target
evidence-directory list but stops after `split_off_pair.TARGETS`; it omits
`raw_slice_pair.TARGETS`. The same validator imports and invokes raw-pair
validation elsewhere, so the generated 048 and 049 evidence directories are
incorrectly rejected as out of scope.

Include both raw-pair artifact IDs in that exact directory set and add a
regression that rejects a foreign directory while accepting precisely the
51 classified target directories. Rerun the full acceptance driver to a clean
PASS after repairing F1.

The two candidate result rows are not independently accepted.
