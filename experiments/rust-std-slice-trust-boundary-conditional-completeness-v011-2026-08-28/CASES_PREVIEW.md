# Representative conditional-completeness cases

This is an operator-facing preview of three already executed `core::slice`
cases from different semantic families. It does not classify any additional
target or mark the 62-target campaign complete. Paths below are relative to
this experiment root.

| Input order | Exact API | Family | Solver result | Classification |
|---|---|---|---|---|
| 029 | `<[T]>::binary_search_by::<F>(&[T], F) -> Result<usize, usize>` | callback/search | `sat` for both theorem negations | exact output: `conditional-incomplete`; reviewed equivalence: `conditional-incomplete` |
| 106 | `<[T]>::splitn_mut::<F>(&mut [T], usize, F) -> SplitNMut<'_, T, F>` | iterator/subslice | `unsat` for both theorem negations | exact output: `conditional-complete`; reviewed equivalence: `conditional-complete` |
| 078 | `<[T]>::select_nth_unstable_by::<F>(&mut [T], usize, F) -> (&mut [T], &mut T, &mut [T])` | callback/selection | bounded length-four theorem negation: `unsat`; nonvacuity: `sat` | exact output: `missing-source-backed-model`; reviewed equivalence: `missing-source-backed-model` |

## 029 `core::slice::binary_search_by`

**Contract binding.** Input order 029 binds active contract SHA-256
`bbea7d2146da8d9116c68e9603460103ed4f7322c785180266a17b23b06c0f6b`
and Rust 1.96 source/docs at `core/src/slice/mod.rs:2926-3022`.

**Fixed boundary.** Both executions share the input sequence/element-read
observations, each source-call comparator argument and `Ordering` result, and
the comparator's pre/post state transition, call count, and panic observation.
The boundary does not contain a selected index, insertion point, returned
`Result`, aggregate final state, or selected execution trace.

**Equivalence.** Result tags and callback final state are exact. `Err` indices
are exact. Distinct `Ok` indices are equivalent only when both indices identify
elements observed as `Equal`, matching the duplicate-key allowance in
`core/src/slice/mod.rs:2926-2967`.

**Result and classification.** The reviewed-equivalence and exact-output
theorem negations both returned `sat`. The fixed length-two
`[Greater, Less]` boundary admits contract-valid `Ok(0)` and `Err(0)`
executions with the same callback final state, so they are not matching-index
equivalent. Independent replay confirms both executions satisfy the active
contract. Therefore both result columns are `conditional-incomplete`.

**Trust caveat.** This is incompleteness of the active relational contract,
not nondeterminism of one concrete Rust execution. The witness is intentionally
outside the sorted comparator domain because the active contract does not
require sortedness; the retained sorted-domain sanity obligation is `unsat`.
Element reads and `FnMut` observations remain audited lower, source-backed
transitions rather than an oracle for the returned result.

**Replay evidence.**

- Result index and hashes: `evidence/targets/029_core_slice_binary_search_by/result.json`
- Reviewed-equivalence SMT and capture:
  `evidence/targets/029_core_slice_binary_search_by/obligation.smt2`,
  `evidence/targets/029_core_slice_binary_search_by/obligation/command.txt`,
  `evidence/targets/029_core_slice_binary_search_by/obligation/stdout.txt`,
  `evidence/targets/029_core_slice_binary_search_by/obligation/stderr.txt`,
  `evidence/targets/029_core_slice_binary_search_by/obligation/status.txt`
- Exact-output SMT and capture:
  `evidence/targets/029_core_slice_binary_search_by/exact_output_obligation.smt2`,
  `evidence/targets/029_core_slice_binary_search_by/exact_output_obligation/command.txt`,
  `evidence/targets/029_core_slice_binary_search_by/exact_output_obligation/stdout.txt`,
  `evidence/targets/029_core_slice_binary_search_by/exact_output_obligation/stderr.txt`,
  `evidence/targets/029_core_slice_binary_search_by/exact_output_obligation/status.txt`
- Fixed model and independent replay:
  `evidence/targets/029_core_slice_binary_search_by/counterexample_model.smt2`,
  `evidence/targets/029_core_slice_binary_search_by/counterexample_model/stdout.txt`,
  `evidence/targets/029_core_slice_binary_search_by/witness.json`,
  `evidence/targets/029_core_slice_binary_search_by/witness_replay/command.txt`,
  `evidence/targets/029_core_slice_binary_search_by/witness_replay/stdout.txt`,
  `evidence/targets/029_core_slice_binary_search_by/witness_replay/status.txt`
- Independent decision: `review/REVIEW_ACCEPTANCE_20260831T110316Z.md`

## 106 `core::slice::splitn_mut`

**Contract binding.** Input order 106 binds active contract SHA-256
`8fb38da00d00aea693a93e948863b8ab7bf6d6d2e6e4662345ad50d9a923d3db`
and the Rust 1.96 constructor chain
`split_mut -> SplitMut::new -> SplitNMut::new` at
`core/src/slice/mod.rs:2423-2447` and the cited iterator constructors.

**Fixed boundary.** Both executions share only the input allocation identity,
input mutable-borrow identity, and predicate identity. Construction invokes
the predicate zero times. The returned iterator/view, all projected ranges,
predicate results or transitions, private iterator fields, final state,
answer encodings, and traces are excluded.

**Equivalence.** Exact equality covers every principal return and reference
identity, all returned private iterator observations, stored predicate
identity/state, `finished`, `count`, direction, callback count, final mutable
slice, and final callback state. No observation is weakened.

**Result and classification.** The full exact-state theorem negation and the
exact-output theorem negation each returned exact `unsat` with exit status
zero and empty stderr. The source constructor chain determines the complete
initial lazy-iterator state from the shared input and narrower identity
boundary. Both result columns are therefore `conditional-complete`.

**Trust caveat.** The result covers construction of `SplitNMut`; it does not
claim that later iterator consumption is callback-free. Completeness is
conditional on the shared input allocation, borrow, and predicate identities,
but no target output or private-state answer is fixed by the boundary.

**Replay evidence.**

- Result and boundary records:
  `evidence/targets/106_core_slice_splitn_mut/result.json`,
  `evidence/targets/106_core_slice_splitn_mut/boundary_manifest.json`
- Full exact-state SMT and capture:
  `evidence/targets/106_core_slice_splitn_mut/obligation.smt2`,
  `evidence/targets/106_core_slice_splitn_mut/obligation/command.txt`,
  `evidence/targets/106_core_slice_splitn_mut/obligation/stdout.txt`,
  `evidence/targets/106_core_slice_splitn_mut/obligation/stderr.txt`,
  `evidence/targets/106_core_slice_splitn_mut/obligation/status.txt`
- Exact-output SMT and capture:
  `evidence/targets/106_core_slice_splitn_mut/exact_output_obligation.smt2`,
  `evidence/targets/106_core_slice_splitn_mut/exact_output_obligation/command.txt`,
  `evidence/targets/106_core_slice_splitn_mut/exact_output_obligation/stdout.txt`,
  `evidence/targets/106_core_slice_splitn_mut/exact_output_obligation/stderr.txt`,
  `evidence/targets/106_core_slice_splitn_mut/exact_output_obligation/status.txt`
- Independent replay:
  `evidence/targets/106_core_slice_splitn_mut/solver_replay/command.txt`,
  `evidence/targets/106_core_slice_splitn_mut/solver_replay/stdout.txt`,
  `evidence/targets/106_core_slice_splitn_mut/solver_replay/status.txt`
- Independent decision: `review/REVIEW_ACCEPTANCE_20260831T122239Z.md`

## 078 `core::slice::select_nth_unstable_by`

**Contract binding.** Input order 078 binds active contract SHA-256
`8d197563a2e9735beef3c52ff46ea5d3dd44da47b48e3b199654cf3c667490d7`
and Rust 1.96 source/docs at `core/src/slice/mod.rs:3523-3590` plus private
selection source at `core/src/slice/sort/select.rs:17-307`.

**Fixed boundary.** Both executions share callback identity, initial
callback-visible state, and source-call relations for comparator arguments and
`Ordering` results, unique next callback state, and panic. The boundary
contains no realized call trace/count, pivot, permutation, returned range,
final callback state, final slice, selected answer, or equivalent encoding.

**Equivalence.** Exact equality is required for all returned references and
lengths, pivot identity, the entire final slice, allocation/borrow identity,
panic status, and callback-visible final state. Selection receives no
equal-key reordering relaxation.

**Result and classification.** The retained valid non-ZST length-four,
index-one insertion-sort theorem negation returned `unsat`; a separate
nonvacuity obligation returned `sat`. These are regression results for that
source path only. They are not a full-target UNSAT proof. Both result columns
remain `missing-source-backed-model`.

**Trust caveat.** The bounded model covers the literal three-tail insertion
path, callback state threading, rotations, and gap-guard-restored panic
prefixes. It does not model arbitrary-length `choose_pivot`, lower-partition
mutation/callback schedules, introselect narrowing and ancestor-pivot
handling, the 16-step fallback, or their panic/unwind behavior. Retained
answer-bearing sites `TS-078-D003` and `TS-078-E001` are excluded and remain
unresolved; their bounded `unsat` result is not laundered into a conditional
completeness classification.

**Replay evidence.**

- Result and boundary records:
  `evidence/targets/078_core_slice_select_nth_unstable_by/result.json`,
  `evidence/targets/078_core_slice_select_nth_unstable_by/boundary_manifest.json`
- Bounded theorem SMT and capture:
  `evidence/targets/078_core_slice_select_nth_unstable_by/obligation.smt2`,
  `evidence/targets/078_core_slice_select_nth_unstable_by/obligation/command.txt`,
  `evidence/targets/078_core_slice_select_nth_unstable_by/obligation/stdout.txt`,
  `evidence/targets/078_core_slice_select_nth_unstable_by/obligation/stderr.txt`,
  `evidence/targets/078_core_slice_select_nth_unstable_by/obligation/status.txt`
- Nonvacuity and canonical source execution:
  `evidence/targets/078_core_slice_select_nth_unstable_by/bounded_nonvacuity.smt2`,
  `evidence/targets/078_core_slice_select_nth_unstable_by/bounded_nonvacuity/stdout.txt`,
  `evidence/targets/078_core_slice_select_nth_unstable_by/length_four_source_execution.smt2`,
  `evidence/targets/078_core_slice_select_nth_unstable_by/length_four_source_execution/stdout.txt`
- Independent decision: `review/REVIEW_ACCEPTANCE_20260901T014750Z.md`

The latest independent campaign checkpoint,
`review/REVIEW_ACCEPTANCE_20260901T034008Z.md`, records 38 classified rows and
24 `not-run` rows. This preview leaves that ledger and every retained evidence
tree unchanged.
