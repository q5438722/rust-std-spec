# Independent Reviewer request: target 080 operational v1

**Status:** pending independent review

Review only input order 080, `core::slice::sort_unstable`, and the additive
model `target-080-operational-v1-rust-1.96-complete`. Do not inherit the stale
rejection in `review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md`, select
target 080 as an operational-v2 overlay, change either certified target-080
classification, or invoke a stage-transition writer.

Replace that addendum with one fresh, target-specific decision containing
exactly one marker in this form:

```text
**VERDICT: ACCEPT**
```

or:

```text
**VERDICT: REJECT**
```

An acceptance must be evidence-backed. A rejection must state actionable
findings and leave `preservation/path_policy_v5.json` absent.

## Decisive fresh run

From the experiment root, run the complete driver from command 1, without
`--start-at`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

Require exit 0 and a newly written `logs/acceptance_manifest.json` with
`status == "passed"`, exactly 54 command records, every command successful,
successful `01_compileall`, and at least 721 executed passing repository
tests. Directly inspect `logs/44g_target_080_operational_v1.*`; it must report
28 passing witness replays, 26 SAT source-force probes, 15 SAT semantic
mutations, two UNSAT correspondence obligations, and Verus 5 verified with
zero errors. Do not accept retained captures in place of the fresh run.

## Source fidelity and schedule

- Bind the active generated contract by its literal declaration and readable
  provenance. Inspect the public rustdoc, `Ord` vocabulary and laws, public
  adapter, implementation-proof harness and manifests, audited trust records,
  and every Rust 1.96 source item listed in
  `evidence/target_080_operational_v1/source_bindings.json`.
- Compare the bound source copies directly to canonical Rust 1.96 without
  inspecting, quoting, or adjudicating opaque integrity identifiers. Inspect
  the entry/dispatch, existing-run detection, small sorts and `CopyOnDrop`,
  pivot selection, all partition variants and guards, quicksort recursion,
  heapsort and `sift_down`, ZST/trivial returns, configuration dispatch, and
  panic/unwind restoration.
- Directly inspect `tools/target_080_operational_v1.py`,
  `tools/target_080_source_interpreter_v1.py`,
  `tools/target_080_operational_witness_v1.py`, and
  `tools/target_080_operational_smt_v1.py`. Confirm the realized comparison,
  swap, write, pivot, partition, recursion, and restoration schedule is
  derived from the source transitions and retained input sequence. The SMT
  execution must start from that input and the boundary initial state, not a
  terminal record or expected output. The independent reference interpreter
  must remain separate from the SMT transition encoding.

## Boundary admissibility

- Inspect `evidence/target_080_operational_v1/boundary_manifest.json` and all
  five readable target-080 trust records. `TS-080-D002` and `TS-080-E001`
  must be replaced by source-backed transitions; only `TS-080-D003` may
  remain admitted.
- `Boundary_T` may expose only total per-call `Ord::lt`, callback next-state,
  and callback panic observations indexed by callback state and compared
  element identities. Classification-eligible executions must make the
  implementation comparison exactly one state-independent contract total
  preorder; state-indexed symbolic relations are diagnostic only.
- Reject any boundary containing the realized callback schedule, pivot or
  partition choice, swap choice, selected output, final sequence or
  permutation, aggregate final state, target trace, or precomputed terminal
  state. Confirm the callback boundary is genuine, source-used, and narrower
  than the target.

## Correspondence, solver, witnesses, and Verus

- Regenerate and directly replay
  `evidence/target_080_operational_v1/obligation.smt2` and
  `exact_output_obligation.smt2`. Require clean UNSAT for the field-complete
  operational-correspondence and exact-output/terminal-state obligations.
  The compared result must include the full sequence, callback state, panic,
  abort, terminal status, unit return, and helper return index where
  applicable, under the same input and the same boundary arrays.
- Require SAT nonvacuity, all 26 source-force probes SAT, and all 15
  source-semantic mutations SAT. Inspect the metadata and generated formulas,
  not only their result summaries.
- Replay all 28 retained witnesses with
  `tools/replay_target_080_operational_v1.py`. Confirm field-complete equality,
  source-derived callback schedules and phase sequences, permutation
  retention, normal and panic paths, duplicate classes, configuration
  dispatch, small-sort specializations, partition variants, restoration
  guards, recursion, and heapsort.
- Directly type-check and verify
  `proofs/080_core_slice_sort_unstable_operational_v1.rs`. Require a
  trusted-free proof with 5 verified and 0 errors, no `assume`, `admit`,
  `external_body`, or precomputed terminal state, and confirm the retained
  sequence-projection mutation is rejected.

## Preservation and verdict closure

- Confirm the 280 paths registered by `preservation/path_policy_v4.json`
  retain their current content using direct observations and the fail-closed
  validator, without treating opaque identifier values as review evidence.
  Preserve policies v1-v4, every v4-registered package byte, accepted
  target-078/079 packages, certified target-080 classifications, and
  `research/PIPELINE_STATE.json`.
- Confirm target 080 remains an additive operational-v1 correspondence
  result only: exact-output `conditional-incomplete` and completeness modulo
  reviewed equal-key permutation `conditional-complete` stay unchanged.
- For an acceptance, create `preservation/path_policy_v5.json` as the exact
  one-review successor: schema version 1, policy id
  `slice-preservation-path-policy-v5`, parent id
  `slice-preservation-path-policy-v4`, an exact byte/hash/size record for the
  current v4 file, and `registered_post_v4_additions` containing only
  `target_080_operational_v1_review` with one exact record for the accepted
  addendum. `tools/preservation_policy_v3.py::target_080_lifecycle` must then
  report `review-accepted` while
  `selected_as_operational_v2_overlay` remains false.
- Change only lifecycle integration that is necessary for the accepted state,
  then rerun the complete acceptance driver from command 1 and require the
  same passing gates. Do not edit the accepted addendum after v5 hashes it.
