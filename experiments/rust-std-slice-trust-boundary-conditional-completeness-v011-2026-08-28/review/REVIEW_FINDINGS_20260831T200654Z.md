# Independent Reviewer findings: MaybeUninit lifecycle cluster

**VERDICT: CHANGES REQUIRED**

This review covers only input orders 025 `core::slice::assume_init_drop`, 026
`core::slice::assume_init_mut`, and 119
`core::slice::write_clone_of_slice`. It does not authorize a Manager stage
transition.

## Fresh verification

The readable authority content, canonical Rust excerpts, frozen harnesses,
transformation manifests, dependency manifests, and source-body records were
directly compared with the three bound evidence packages. The CSV and JSON
ledgers agree on 62 rows, with 22 classified and 40 `not-run`.

The Reviewer ran the target tests, direct solver and witness replays, all three
Verus models, and the full acceptance driver. The target suite ran 15 tests and
reported `OK`. Direct Z3 replay returned:

| Target | Full exact equivalence | Exact output |
|---|---|---|
| 025 `assume_init_drop` | `unsat` | `unsat` |
| 026 `assume_init_mut` | `sat` | `unsat` |
| 119 `write_clone_of_slice` | `unsat` | `unsat` |

The target-026 fixed model was SAT. An independent content-level replay found
the same valid input and boundary, equal returned mutable-slice identity and
initial values, and unequal final initialized storage in the two executions;
every active contract conjunct checked by the replay held.

All three Verus models separately type-checked. Verification reported
`2 verified, 0 errors`, `2 verified, 0 errors`, and
`3 verified, 0 errors` for targets 025, 026, and 119 respectively, with no
`external_body`.

`PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py` passed all 28
commands. Python compilation succeeded, 229 tests ran and reported `OK`, and
the local validator passed. A direct recursive content comparison around the
acceptance run found no changes in the captured evidence trees or crosswalks.
These successful checks do not cover the two findings below.

## Blocking findings

### 1. The required standalone cluster replay fails from the delivered state

Running:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_maybeuninit_lifecycle_cluster.py
```

from the delivered 22-classified/40-`not-run` ledger fails in
`update_ledgers_atomically` with:

```text
ValueError: ('core::slice::assume_init_drop', '25'): refusing to alter an out-of-scope result
```

`tools/run_maybeuninit_lifecycle_cluster.py:619-650` starts applying the three
updates without first normalizing those three result rows. While updating the
first target, the other already delivered cluster rows are therefore treated
as out of scope. The full acceptance driver passes only because its authority
builder and predecessor pipelines reconstruct the ledger before invoking the
cluster.

Add a fail-closed delivered-state reset analogous to
`tools/run_pointer_cast_cluster.py:43-94`: validate the complete 22-target
delivered state, reset only both result cells for 025, 026, and 119, run the
ordered cluster, and verify that every other cell and evidence tree is
unchanged. Add tests for a successful repeated standalone replay and rejection
of any altered predecessor, cluster, or unrelated result.

### 2. The write/drop ordering and panic guards are not connected to the classified transition

The production obligations define `DropIndexAtStep` and `WriteIndexAtStep` at
`tools/target_025.py:260` and `tools/target_119.py:402`, but neither symbol is
called by its `TargetDefinition_T`. In the emitted production obligations each
symbol occurs only in its own definition. Reversing either index function in a
Reviewer-owned mutation left the corresponding full theorem result `unsat`.

The duplicate/out-of-order probes at `tools/target_025.py:830-832` and
`tools/target_119.py:1268-1270` obtain UNSAT by contradicting those isolated
identity definitions rather than by falsifying a reachable per-step source
composition. The target-119 clone-panic probes generated at
`tools/target_119.py:1146-1221` likewise invoke neither `Boundary_T` nor
`Spec_T`; their expected order, counts, final cells, and Destruct state are
embedded in both helper definitions and assertions.

The recursive Clone and Destruct chains do constrain callback-state chaining,
so this finding does not invalidate the captured solver outputs by itself.
It does mean that the required fail-closed evidence for write/drop order and
panic cleanup has not yet exercised the classified source transition.

Make the per-step index, write/drop storage transition, operation count, and
panic cleanup semantics reachable from a reviewed target or panic-path
definition. Negative probes must mutate that reachable composition and fail
because source order, initialized-prefix cleanup, or callback state is wrong,
not merely because an otherwise unused identity helper contradicts itself.
Then regenerate the three evidence trees and rerun the independent gate.

**No stage transition is authorized by this review.**
