# Independent Reviewer findings: mutable view construction

**VERDICT: CHANGES REQUIRED**

**Timestamp:** 2026-09-01T13:00:48Z

This decision covers only input orders 017
`core::slice::as_flattened_mut`, 018 `core::slice::as_mut_array`, 046
`core::slice::first_chunk_mut`, and 047 `core::slice::from_mut`. It does not
authorize a Manager stage transition.

## Blocking finding: full-state relations are overconstrained

The exact-output source transitions are supported by the four literal active
contracts and the canonical Rust bodies. The full-state transitions are not.
`ImmediateFinalFrameTransition` fixes both the receiver and returned mutable
view to their initial values. That is stronger than the active `final(...)`
clauses and removes the legal writes made through each returned `&mut`.

The contracts require relational frames, not unchanged returned contents:

- `as_flattened_mut` requires the flattened final receiver to equal
  `final(ret)`.
- `as_mut_array` requires the final receiver to equal the final returned
  array.
- `first_chunk_mut` requires the final receiver to be the final returned
  prefix followed by the unchanged old suffix.
- `from_mut` requires the singleton final returned slice to contain the final
  input value.

The canonical docs demonstrate mutation through `as_flattened_mut` and
`first_chunk_mut`; the other two signatures return the same exclusive mutable
borrow capability. This is also the established campaign treatment for
mutable returned views in the chunk and raw-slice models: fixed input and
boundary do not fix legal final in-range writes.

An independent Z3 probe retained each target's generated output transitions,
literal active-contract transition, one shared valid input, and one shared
boundary. It replaced only the unchanged-content restriction with the
contract's borrow-lifetime frame and fixed two concrete legal final states:
the original integer values and a state with the first returned element
changed to `99`. All four probes returned `SAT` while exact equality of full
state failed:

| Input order | Fixed source case | Distinct legal final state |
|---|---|---|
| 017 | non-ZST `len=3`, `N=2` | flattened first element changed |
| 018 | `len=N=3` | returned array first element changed |
| 046 | `len=3`, `N=2` | returned prefix first element changed; suffix fixed |
| 047 | non-ZST singleton | returned/input element changed |

The current eight `UNSAT` theorem results therefore prove a strengthened
immediate-state model, not full-state conditional completeness of the active
contracts.

## Confirmed portions

Readable inspection confirmed the four active declarations, canonical target
and helper source, public docs, frozen harnesses and manifests, all 34 trust
records, project-local `array::from_mut` excerpt, and boundary schema. The
eight retained answer-bearing sites remain inadmissible and are replaced
rather than relabeled. `Boundary_T` contains no returned result, branch,
final-state value, answer encoding, or execution trace.

Fresh Python compilation succeeded. All 12 focused tests and all 454
repository tests passed. The four trusted-free Verus models type-checked and
verified two obligations with zero errors, and direct replay reproduced 8
current theorem `UNSAT` results, 22 source-instance `SAT` results, and 82
negative-probe `UNSAT` results. Those checks expose no build regression, but
their expected full-state result encodes the same overconstraint.

## Required repair

Keep exact output/range/reference identity deterministic and retain its direct
`UNSAT` proof. For the full-state projection, leave final values reached
through the returned mutable borrow free while enforcing exact lengths,
receiver/return reconstruction, unchanged suffix or outside frame, backing
identity, exclusivity, and provenance. Retain one concrete same-input,
same-boundary `SAT` witness per target and classify all four full-state rows
as `conditional-incomplete`. Update the generated evidence, tests, checker
design, wiki result, and validators, then rerun the bounded and complete
acceptance commands.
