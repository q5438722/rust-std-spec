# Independent Reviewer decision: clone-effect transitions

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T05:03:59Z

This decision covers only input orders 037
`core::slice::clone_from_slice` and 043 `core::slice::fill` against the
independently accepted 38-target baseline. It does not authorize a Manager
stage transition.

## Semantic and boundary review

Both active declarations, the relation-valued `cloned<T>` vocabulary, public
docs, canonical Rust 1.96 items and private helper bodies, frozen
implementation-proof inputs, and all 22 trust records were checked by readable
content. Target 037 follows the increasing-index default `clone_from` loop and
the type-selected `TrivialClone` nonoverlapping copy; both unequal-length paths
panic before any callback or write. Target 043 follows the empty/nonempty
split-last default loop, per-element Clone transitions, final-slot move,
`TrivialClone` reads, primitive `write_bytes` paths, and integer
fast-path-or-loop selection.

The shared boundaries contain initial storage, identity, provenance, layout,
source or fill inputs, individual Clone arguments/results/outcomes/state
transitions, Miri as platform input, and target 043's
`is_val_statically_known` observation. They exclude aggregate destination
results, final callback state, operation order/count, selected paths, answer
encodings, and traces. Clone results remain relation-valued, while callback
order, state chaining, write effects, dispatch, final storage, and final state
are derived. Exact equivalence compares every principal return and immediate
final-state observation.

Target 043's integer intrinsic count matches Rust's left-to-right
short-circuit control flow: static-known uniform is 2; static-known
nonuniform, dynamic loop, Miri-short loop, and Miri-long uniform are 1; and
Miri-long nonuniform is 0. The former selected-path-only formula disagrees
with exactly the first four cases. The shared SMT transition, compact and
zero-callback witnesses, generated Verus model, and generated checker design
all carry the repaired rule. The validator still requires the exact
`is_val_statically_known` identifier.

## Independent execution

- `python3 -m compileall -q tools tests` completed cleanly, followed by all 17
  focused clone-effect tests passing.
- `python3 tools/run_clone_effect_cluster.py` replayed four normal, two
  panic-prefix, and one mismatch theorem obligations as UNSAT; 27 source, six
  panic-prefix, and two mismatch witnesses as SAT with retained models; and
  ten negative probes as UNSAT.
- Both generated Verus files type-checked and verified with one verified proof
  and zero errors each; neither contains `external_body`.
- `python3 tools/run_acceptance.py` passed all 34 commands. The full suite ran
  340 passing tests, and `22_local_validator` reported `validation=PASS`.
- A direct before/after readable-content comparison, excluding opaque
  integrity fields, found 2,945 files across all 38 certified evidence trees
  and 320 frozen-input files unchanged. The ledger contains exactly 40
  classified rows and 22 `not-run` rows, with only 037 and 043 added to the
  accepted baseline.
