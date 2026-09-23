# specdet does not directly model mutable-reference returns

This is a checker limitation on specdet 0.3.0, not a Rust or Verus
implementation defect. Independent review justified the original full-value
observation transfer; direct extraction remains unsupported. The revised
adapter has now passed engineering verification and follow-up independent
review in full `Seq<T>` value observation, not allocation-address determinism.
No checker, verifier, vstd or canonical Rust change is proposed or authorized;
no external issue has been filed.

The affected API is `<&mut [T] as core::default::Default>::default`, defined
at Rust 1.96 `core/src/slice/mod.rs:5644-5646` and documented at line 5643.
Its original `&mut []` body already verifies and compiles with one target
function and no imported proof functions:
[`default_mut.rs`](../proofs/correctness/slice/default_mut.rs),
[`command`](../logs/defaults/correctness/default_mut/command.txt),
[`output`](../logs/defaults/correctness/default_mut/verus.log).
The baseline is official Verus `0.2026.09.20.aef82ed`, matching vstd,
and host Rust `1.98.1`, as recorded in `toolchain/BASELINE.md`.

## Two simultaneously live mutable regions

The same actual specdet 0.3.0 extraction limit has now been reproduced for
`split_first_mut` and `split_last_mut`, whose exact return type is
`Option<(&mut T, &mut [T])>`. The direct declarations were discovered at line
13 of their input files and analyzed with their project-relative selectors.
Both exited with code 2, `unsupported_mutable_return`, no baseline query and
no proof goal. The command/report directories are
[`logs/mutable-splits-proposal/direct/`](../logs/mutable-splits-proposal/direct/);
the exact inputs now reside in
`proofs/completeness/slice/history/{split_first_mut,split_last_mut}_direct.rs`.
Their frozen analyzed copies and failures remain unchanged. Moving them out
of active discovery does not turn either failure into a successful check.

The candidates in
[`mutable_splits_post.rs`](../specs/slice/mutable_splits_post.rs) retain
four distinct states: the entire initial input, the returned initial element
and complete remainder, the caller's final element and complete remainder,
and the entire final input. The caller-final pair is optional so that an
empty input needs no inhabitant of `T`. Its Option tracks the original return
variant, not a later reassignment of a caller-local Option variable.

The active analysis functions take only `Ghost<Seq<T>>` and
`Ghost<Option<(T, Seq<T>)>>` as inputs. They return
`Ghost<(Option<(T, Seq<T>)>, Seq<T>)>` containing the initial returned pair
and the final owner. The admissible caller domain is:

```rust
match caller_final {
    None => input_initial.len() == 0,
    Some((_, written_remainder)) =>
        written_remainder.len() + 1 == input_initial.len(),
}
```

No element value, remainder contents or final owner is supplied as an answer
in those premises. `caller_domain` derives this domain from the candidate;
`all_caller_writes` proves a satisfying output for every independent choice
of final element and same-length remainder. The latter length follows from
the initial subrange and the existing borrow-length fact invoked by each
isolated source proof. The remaining state lemmas prove full reconstruction,
full comparison preservation, exact equivalence to the existing first
contract, and the corresponding last contract. All seven state functions
compile with `--no-cheating` in
[`value-state/initial/state/`](../logs/mutable-splits-proposal/value-state/initial/state/).
Each of the two compiled adapters has one additional function.

Actual discovery identifies:

```text
proofs/completeness/slice/inputs/split_first_mut.rs:split_first_mut_observation@7
proofs/completeness/slice/inputs/split_last_mut.rs:split_last_mut_observation@7
```

Both analyze commands and their `replay --run ... --reexecute` commands,
without a configuration override, pass with one selected deterministic
result and one verified generated goal each. All four original queries are
UNSAT and disable exactly 19 guards. The comparison is:

```rust
((r1@.0 is Some) == (r2@.0 is Some))
    && ((r1@.0 is Some) ==>
        (r1@.0->Some_0.0 == r2@.0->Some_0.0
         && r1@.0->Some_0.1 =~= r2@.0->Some_0.1))
    && r1@.1 =~= r2@.1
```

Only the erased Ghost carrier representation is excluded. No Option variant,
tuple component, initial remainder position or final input position is
excluded. The generated sources, original queries and complete reports are
under [`completeness/`](../logs/mutable-splits-proposal/completeness/).
The current adapter, pure predicates, state lemmas, configured type source
and configuration match both frozen workspaces and native comparison
dependencies byte-for-byte. Each analyzed/reexecuted generated source pair
is identical. Separate `--compile` invocations of the two generated files
check nine functions each: one comparison, one adapter and seven state
lemmas. This is not an exported success for an adopted source implementation.

The new source correspondence received
[separate independent permission](V-SLICE-PATTERN.md#independent-mutable-split-permission-before-adoption);
the [current adopted results](V-SLICE-PATTERN.md#adopted-mutable-split-source-results)
and their new exported comparisons still require final independent review.
Direct extraction failures and original source-pattern failures remain
recorded. The temporary redundancy criterion retains the cross-state length
relation while omitting derived same-state remainder and owner lengths;
it does not identify independent initial and final contents with each other.

### Omitted-observation controls

The isolated generic controls in
[`observation-controls/`](../logs/mutable-splits-proposal/observation-controls/)
remove, one at a time, the initial element, entire initial remainder,
nonempty final owner or empty final owner clause. Their adapters import
only the changed pure predicate, not the state lemmas for the complete
contract. Both complete controls still prove one deterministic result.
Each omitted-clause file also contains an explicit pair of unequal outputs
for the same legal `u8` initial/caller state. Actual
`--compile --no-cheating` checks verify the adapter and that concrete
existence proof: two functions, zero errors in each of eight cases.

The automated generic searches do **not** certify those counterexamples.
All eight return `inconclusive`, with original baseline
`UNKNOWN (incomplete quantifiers)` and diagnostics that narrowing is not
supported for `TypeKind.UNKNOWN:T`. Their generated determinism goals are
unproved, not successful zero-goal checks. The strict control command exits
with code 1 rather than converting these results into success. Its command,
inputs, complete reports, compiled concrete witnesses and runner snapshot
remain available in the same directory and in
`.argus_subagents/slice-mutable-splits-observation-controls.json`.

The concrete witness proofs demonstrate nonuniqueness of each weakened
relation; they are distinct from the unresolved automated search. None of
these weakened inputs is active in the project configuration or used for an
API export. The complete generic predicates, source proposals and successful
main analyze/reexecute runs remain unchanged.

The subsequent isolated `u8` experiment is retained in
[`observation-controls-u8/`](../logs/mutable-splits-proposal/observation-controls-u8/).
Only the analysis functions' generic element type was instantiated; the
project's actual generic candidates and adapters were not changed. Both
complete `u8` controls again prove one generated comparison with original
query UNSAT. All eight deleted-clause searches still return `inconclusive`,
with `UNKNOWN (incomplete quantifiers)`, an unproved generated goal and no
checker-certified counterexample. The earlier `TypeKind.UNKNOWN:T`
narrowing diagnostics are absent. Concretizing the element type therefore
did not resolve this search limitation; the earlier generic diagnostic is
not sufficient to identify its cause.

All ten concrete control predicates match exactly the complete candidate or
the intended single-clause deletion, including their generated worktree
copies. Their comparisons still observe the Option, tuple positions,
complete initial element/remainder and entire final input. The `u8`
queries introduce scalar equality/range search guards in addition to the
generic shape guards: each original query declares 121 guards and disables
all 121, rather than the main generic analyses' 19. No finite search range
was turned into a restriction of the original problem.

Each current weakened `u8` input actually compiled with
`--crate-type lib --compile --no-cheating --num-threads 1`, verifying the
adapter and its explicit unequal-output witness, and produced a nonempty
library. The two complete controls compiled one function each. These are
18 compiled functions in total, including eight separate witness proofs,
not 18 successful checker comparisons. For example, the initial-remainder
witness preserves the element and final owner while reversing the two
initial remainder values; the empty-owner witness compares empty and
nonempty final sequences for the same empty input and `None` caller state.
The latter needs no input element to represent the actual empty call.
Both forms are available in
[`split_first_mut/initial-remainder/project/proofs/completeness/slice/inputs/split_first_mut.rs`](../logs/mutable-splits-proposal/observation-controls-u8/split_first_mut/initial-remainder/project/proofs/completeness/slice/inputs/split_first_mut.rs)
and
[`split_last_mut/empty-owner/project/proofs/completeness/slice/inputs/split_last_mut.rs`](../logs/mutable-splits-proposal/observation-controls-u8/split_last_mut/empty-owner/project/proofs/completeness/slice/inputs/split_last_mut.rs).

The durable command completed with exit code 1, as required by its strict
refusal to treat inconclusive search as a verified counterexample:
`.argus_subagents/slice-mutable-splits-u8-controls.json`.
Its inputs, compiler outputs, commands and ten checker reports have been
inspected; it is no longer running and is not being relaunched. Neither
the original nor concrete-type failure is overwritten or counted toward
API completion. These supplementary negative searches remain unresolved;
they neither prevent recording the separately granted source-conversion
permission nor replace final independent review of the adopted files.

## Reproduction

The unchanged public binding and candidate are retained in
[`default_mut_direct.rs`](../proofs/completeness/slice/inputs/default_mut_direct.rs).
The actual command was:

```sh
/home/chentianyu/spec-determinism-tool/.venv/bin/specdet analyze \
  --config specdet.toml \
  --target proofs/completeness/slice/inputs/default_mut_direct.rs \
  --out proofs/completeness/slice/runs/defaults/default_mut_direct --json
```

It exits with code 2 during extraction, before any completeness obligation:

```text
unsupported_mutable_return:
Mutable-reference return values are not modeled by this backend
```

The complete report is
[`analyze.json`](../logs/defaults/completeness/default_mut_direct/analyze.json).
The matching checker source is
`/home/chentianyu/spec-determinism-tool/src/specdet/adapters/verus/backend.py:790-792`.
The expected direct analysis would compare both complete returned slice
values; instead, this return type is rejected. A deterministic result for
the shared-reference API does not close this failure.

## Full-value analysis-only reborrow and redundancy repair

The candidate in `specs/slice/default_post.rs` observes the entire `Seq<T>`,
not an allocation address or a new observer. The real API retains its
zero-argument mutable-reference binding in `specs/slice/default.rs`.

For this zero-input constructor, a separate analysis function
calls the independently proved source copy and reborrows its result as
`&[T]`. Its postcondition remains exactly `default_post(result)`. Its
`observe` function retains `result@ == old(value)@` for an arbitrary mutable
slice. Predicate preservation follows from full view equality by substitution:
`default_post` only states extensional equality to `Seq::<T>::empty()`.
At Reviewer's request, the redundant second postcondition
`contracts::default_post(result) <==> contracts::default_post(old(value))`
has been removed. No cross-state or final writeback obligation was removed;
the full initial-view relation and the original `&mut []` body remain intact.
`full_value_comparison` proves that the checker's shared-slice extensional
comparison is equivalent to equality of the two full sequence views.

This analyzes a superset of the possible returned value observations,
without restricting inputs or selecting an answer in an assumption.
Lifetime and exclusive-borrow permissions remain Rust/Verus type-checking
obligations on the real API and its original implementation. The selected
observation is the complete initial returned value; there is no input
slice, unreturned region or caller-owned writeback to omit.

The adapter is
[`proofs/completeness/slice/inputs/default_mut.rs`](../proofs/completeness/slice/inputs/default_mut.rs).
Before the redundancy repair, it compiled and verified with `--no-cheating`,
without importing the new assumed public binding: four functions passed,
consisting of the original constructor and the three observation/transfer
functions. That historical command, full output and queries are in
[`logs/defaults/adapter/`](../logs/defaults/adapter/).

For that original adapter, the actual checker analyzed and reexecuted the candidate with its
unchanged `verus-observable-v1` policy. Both runs proved one generated goal
and reported deterministic with original query UNSAT. The exact complete
comparison is `(r1 =~= r2)`; all five native search guards are disabled in
the original query. No custom equivalence or observation filter is used.
The original and reexecuted harnesses are byte-identical.
The reports and actual commands are in
[`logs/defaults/completeness/default_mut/`](../logs/defaults/completeness/default_mut/),
with native queries and replay reports under
`proofs/completeness/slice/runs/defaults/default_mut/`.

Reviewer independently proved that full view equality entails the removed
clause (one goal, zero errors) and compiled a temporary reduced adapter
(four functions, zero errors). The completed independent source/semantic
checks and dual-track reruns for the original inputs are recorded in the
[review account](../inventory/COVERAGE.md#independent-review-and-redundancy-repair).
Those first-round results justified the repair, but did not certify new runs
of the revised real input. Engineering verification and follow-up independent
review were still pending at that handoff; this is historical, not the current
status.

The revised real target is `default_mut_observation@24`; retained commands
with `default_mut_observation@25` refer to the original adapter and must
keep their historical line number. The reduced adapter compiled with
`--no-cheating`, verifying four functions with zero errors; its output is
`logs/defaults-redundancy/adapter/verus.log`.
Actual analyze and replay `--reexecute` both returned deterministic with
original query UNSAT, one verified goal and exit code 0. Their reports are
`logs/defaults-redundancy/completeness/default_mut/selected/{analyze,replay}.json`,
with new run trees under
`proofs/completeness/slice/runs/defaults-redundancy/default_mut/`.
The current exported proof remains `proofs/completeness/slice/default_mut.rs`.
The first, absolute-path selection failed before proof with `target_not_found`;
`logs/defaults-redundancy/completeness/default_mut/analyze.json` retains that
failure. The adjacent `discover.json` supplies the project-relative selector
`proofs/completeness/slice/inputs/default_mut.rs:default_mut_observation@24`
used by the successful analysis. Original results in `logs/defaults/`
and the old run trees remain historical evidence; independent results on
unchanged inputs may be retained.

The dedicated configuration
[`defaults.toml`](../proofs/completeness/slice/defaults.toml) retains the
same verifier, host Rust and observation policy, but includes the
correctness file needed by this adapter in its frozen source tree. The
first adapter analysis used the root configuration, which excludes all
correctness files, and failed to compile its missing import. That setup
failure remains at
`logs/defaults/completeness/default_mut-missing-snapshot-source/`; it is
not evidence of a verifier or checker semantic defect.

This is an analysis encoding, not a replacement implementation or an
implementation proof.
The original `&mut []` source proof and the failed direct analysis remain
separate and visible. The original observation transfer was independently
justified. The reduced adapter now passes its affected engineering checks and
has completed follow-up independent review.

## Completed second independent review (current)

The authoritative record is
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/8b6d043ccde7/round-0002.json`
(`round: 2`, `review.status: done`). Reviewer independently verified the revised
real adapter with `--compile --no-cheating` (four functions, zero errors),
the current export with `--compile` (five functions, zero errors), and two
focused mutable tests. Actual analyze of
`proofs/completeness/slice/inputs/default_mut.rs:default_mut_observation@24`
and replay `--reexecute` each passed one deterministic goal with original
query UNSAT. The generated comparison still covers the full returned slice,
with no added input premise and all search guards disabled; the analyzed
source, predicate and configuration match the current files.

Together with the first round, this completes independent review of both
`Default` constructors in full `Seq<T>` value observation, not allocation
addresses. The direct extraction failure and this issue remain open as a
checker limitation. All historical failures and proof results remain retained;
unchanged native and six-observer checks were not rerun in round 2.
Neither `len` nor the four slice-pattern APIs gain source proofs from this
review, and the full slice module remains incomplete.

## Singleton borrows with caller-owned state

`core::slice::from_mut` is also affected. Its Rust 1.96 signature and body
are at `slice/raw.rs:211-213`, with documentation at line 207. Unlike the
zero-argument Default constructor, it borrows a caller-owned `T` and must
return the caller's final element after arbitrary lawful writes through
the returned mutable slice.

The historical direct
[`analysis input`](../proofs/completeness/slice/history/from_mut_direct.rs)
preserves `s: &mut T`, `result: &mut [T]`, implicit `Sized` and the
input-tied lifetime. Its two postconditions use the full sequence:
the initial result equals `seq![*old(s)]`, and the final returned slice
equals `seq![*final(s)]`. There is no added input restriction.

The original discovery reported
`proofs/completeness/slice/inputs/from_mut.rs:from_mut@8`.
Both analyze with
[`singletons.toml`](../proofs/completeness/slice/singletons.toml) and
`replay --reexecute` return exit code 2 with:

```text
unsupported_mutable_return
Mutable-reference return values are not modeled by this backend
```

The exact commands, full reports and errors are retained under
[`logs/singletons/completeness/from_mut/`](../logs/singletons/completeness/from_mut/).
Neither execution generated a determinism proof, comparison or original
query. There was no exported `proofs/completeness/slice/from_mut.rs` at
that point. The direct declaration has since been moved, byte-for-byte,
outside the active input directory; the original paths and line numbers
remain in the historical commands and frozen source copies.

Independent review in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/d67769d288a6/round-0001.json`
repeated both direct commands, confirmed zero generated goals and no original
query, and matched the rejection to the installed checker's
`src/specdet/adapters/verus/backend.py:488-495`. The same review independently
replayed the shared singleton with one goal and original query UNSAT, and
confirmed that its initial and mutable final clauses are not redundant.
It did not establish either array source bridge.

The Default adapter is not reused as an answer to this problem. Its shared
reborrow only observes the initial returned contents; it does not carry a
singleton input's final return relation. A mutable singleton adaptation must
justify both states and arbitrary lawful caller writes.
The generic writeback client in
[`singleton_contract_clients.rs`](../tests/singleton_contract_clients.rs)
verifies against the candidate binding, but is neither that adaptation
proof nor a source proof.

The actual array delegate is independently blocked by
[the reference-conversion limitation](V-METADATA.md#singleton-array-delegation-on-the-same-baseline).
No missing dependency contract, caller-write restriction or tool change
was introduced. The completed Default review and all its earlier records
remain unchanged.

## Complete mutable value-state adaptation

The public candidate and both original execution expressions remain unchanged.
The current analysis-only entry is
[`inputs/from_mut.rs`](../proofs/completeness/slice/inputs/from_mut.rs),
`from_mut_observation@9`. Its two `Ghost` inputs carry values, not additional
arguments to `core::slice::from_mut`. The correspondence is:

| Observation | Original candidate state | Analysis position |
|---|---|---|
| Input at the call | `*old(s)` | `input_initial@ : T` |
| Returned slice at construction | `result@` | output tuple field 0, the entire `Seq<T>` |
| Caller-selected final slice | `final(result)@` | `caller_final@ : Seq<T>` |
| Input returned after the borrow | `*final(s)` | output tuple field 1, the entire `T` |

[`from_mut_state.rs`](../proofs/completeness/slice/from_mut_state.rs)
defines `from_mut_post` as precisely the two original `singleton_post`
relations. `candidate_correspondence` proves that identity using the existing
mutable-reference states. Its returned reference is a lemma parameter, so
`old(result)@` denotes the constructor's initial returned slice there.
`caller_domain` derives final length one from the initial singleton relation
and the existing `vstd::slice::mut_ref_slice_len_eq`; no return-value assumption
or new trusted observation is introduced. `all_caller_writes` supplies a
satisfying pair for every initial `T` and every final length-one `Seq<T>`.
In particular it imposes neither equality with the initial element nor any
`Copy`, `Eq`, `Default`, or lifetime bound.

On that derived environment domain, `observation_correspondence` proves
that the second original singleton relation is equivalent to equality of
the full returned `T` with `caller_final[0]`. The first relation still
constrains the entire initial sequence. The current checker postconditions
are just those two nonredundant statements. The singleton length is not
repeated as an output postcondition. `full_value_comparison` connects the
initial slice-value comparison to full sequence equality while retaining
the full input return value.

All five state lemmas compiled with `--compile --no-cheating`:
[`state-correspondence`](../logs/singleton-writeback/state-correspondence/).
The current adapter compiled with the same flags, checking one adapter
function plus those five imported lemmas:
[`adapter-ghost-inputs`](../logs/singleton-writeback/adapter-ghost-inputs/).
Neither compilation imports an assumed array constructor contract or
claims a source implementation proof.

Actual discovery, analyze, and `replay --reexecute` use the unchanged
`singletons.toml` and the project-relative target at line 9. Analyze and
reexecution each verify one generated goal, with original query UNSAT and
no diagnostics. The comparison is exactly
`((r1@.0 =~= r2@.0) && (r1@.1 == r2@.1))`. All seven original-query search
guards are disabled. The input, state file, original predicate, public
binding, and configuration match both frozen source copies. The only
excluded representation is the `Ghost` carrier beyond its value, not
either tuple field or any element. Commands and reports are in
[`completeness/from_mut-ghost-inputs`](../logs/singleton-writeback/completeness/from_mut-ghost-inputs/).
The exported [`from_mut.rs`](../proofs/completeness/slice/from_mut.rs)
compiles with one generated goal, one adapter function, and five imported
state lemmas. Export moves only the relative state import.

The first two-sequence analysis restatement compiled but its synthetic
goal was unproved and its baseline query was UNKNOWN; it is retained at
[`completeness/from_mut`](../logs/singleton-writeback/completeness/from_mut/).
The equivalent indexed restatement then passed at
[`completeness/from_mut-index`](../logs/singleton-writeback/completeness/from_mut-index/).
That intermediate input destructured its `Ghost` parameters. In the
weakening controls, the checker's witness generator consequently emitted
an executable `Seq` local and failed mode checking. Those unsuccessful
controls remain under [`weakening`](../logs/singleton-writeback/weakening/).
The current input keeps the same values in explicit `Ghost` carriers, so
the native witness generator retains their mode. No checker code changed.

The current controls in
[`weakening-ghost-inputs`](../logs/singleton-writeback/weakening-ghost-inputs/)
specialize only scratch inputs to `bool`. The complete relation passes one
goal with original query UNSAT. Removing the initial-content clause yields
two length-one sequences, `[false]` and `[true]`, with the same returned
input value. Removing the return clause yields the same initial sequence
`[false]` with different returned input values. Both results are
`nondeterministic` with a checker-generated, source-verified constructive
counterexample and one verified witness goal. Their original SMT queries
are UNKNOWN; those queries are not counted as counterexamples or successful
completeness proofs. The actual constructive proofs, not failed syntax or
zero goals, establish each missing observation.

The regression driver initially misread a certificate file path as a
directory after all three analyses had finished. Its reader was corrected
and the retained certificates were validated without rerunning unchanged
analyses; `validation.exit-code.txt` is zero. The driver is
[`scripts/check_singleton_writeback.py`](../scripts/check_singleton_writeback.py).
The separate generic, non-Copy/non-static, changed-value, zero-sized, and
clause-independence proofs are
[`tests/from_mut_state.rs`](../tests/from_mut_state.rs), with five regression
functions plus five imported lemmas verified and compiled.

The four-state completeness adaptation has now completed independent review,
recorded in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/63ed051184d5/round-0001.json`.
That review confirms the state correspondence, arbitrary lawful caller writes,
full initial-sequence/input-writeback comparison, both real checker executions,
constructive weakening checks and selective exports. This is a reference to
the completed review, not a replay during the ASCII work.
Direct mutable extraction remains unsupported. Both singleton APIs still have
zero source implementation proofs because the independently confirmed array
conversion failure is unchanged. The completed Default review is not reopened.

## Optional mutable endpoint observations

Actual discovery of the initial `first_mut` and `last_mut` declarations
reported line 13 in each corresponding `inputs/` file. Each actual analysis
returned `unsupported_mutable_return`, no generated proof and no original
query. Their exact declarations are now preserved, without alteration, in
[`history/first_mut_direct.rs`](../proofs/completeness/slice/history/first_mut_direct.rs)
and [`history/last_mut_direct.rs`](../proofs/completeness/slice/history/last_mut_direct.rs).
Commands, reports and frozen inputs remain in
[`logs/mutable-endpoints-proposal/direct/`](../logs/mutable-endpoints-proposal/direct/).
This is an observed limit for these two `Option<&mut T>` returns, not an
inference solely from the earlier singleton result.

The pure candidate file is
[`specs/slice/mutable_endpoints.rs`](../specs/slice/mutable_endpoints.rs).
It does not reregister the existing public vstd bindings at
`toolchain/upstream/source/vstd/std_specs/slice.rs:498-513`. Its representation
separates four observations:

| Meaning | Source expression | Value-state position |
|---|---|---|
| Initial input contents | `old(slice)@` | input `input_initial: Seq<T>` |
| Initial return variant and element | `None` or `Some(*result.unwrap())` | output tuple field 0, `Option<T>` |
| Caller-selected final borrowed element | Same return variant, with `*final(result.unwrap())` in `Some` | input `caller_final: Option<T>` |
| Entire input after the borrow | `final(slice)@` | output tuple field 1, `Seq<T>` |

The optional caller value preserves the original return branch; it does not
model reassignment of the caller's local Option variable. On empty input it
is `None`, and neither input nor output requires an inhabitant of `T`.
On nonempty input it is `Some(written)` for an arbitrary legal final element.
The original slice's final sequence is never an analysis input.

The seven lemmas in
[`mutable_endpoints_state.rs`](../proofs/completeness/slice/mutable_endpoints_state.rs)
compiled with `--crate-type lib --compile --no-cheating --num-threads 1`.
Two prove equivalence to the exact existing first/last vstd postconditions,
without calling either target. `caller_domain` derives the optional shape;
`all_caller_writes` constructs both outputs for every such caller choice.
The two frame lemmas derive full length, selected writeback and every
unborrowed position from `Seq::update`, rather than assuming a frame.
`value_state_comparison` equates the complete tuple value relation with
Option-variant/element equality and full sequence equality. Logs are in
[`value-state/state/`](../logs/mutable-endpoints-proposal/value-state/state/).

The current active entries are only
[`inputs/first_mut.rs`](../proofs/completeness/slice/inputs/first_mut.rs) and
[`inputs/last_mut.rs`](../proofs/completeness/slice/inputs/last_mut.rs), each
with its `*_observation` function at actual discovered line 8. Each compiled
with the same no-cheating flags: **one adapter and seven imported lemmas**.
The derived shape condition is confined to this analysis environment, not
added to either public API or source proof. No element bounds, frozen
writes or final-owner values are introduced.

Actual analyze and `replay --run ANALYZED_RUN --reexecute`, with no
configuration override, each returned one selected target, one verified
comparison goal and original query UNSAT for each API. The generated
comparison includes all three required parts:

```text
((r1@.0 is Some) == (r2@.0 is Some))
&& ((r1@.0 is Some) ==> r1@.0->Some_0 == r2@.0->Some_0)
&& (r1@.1 =~= r2@.1)
```

All **13 search guards** are disabled: two initial-sequence-length guards,
two caller-Option guards, four guards for each output's Option and sequence,
and the output-inequality guard. The current adapter, candidate, state
lemmas, original slice predicate module and configuration are byte-identical
to both frozen inputs; dependencies also match the native proof worktrees.
Reexecution preserved the generated comparison and original query exactly.
The excluded `return.representation_beyond_view` is the erased `Ghost`
carrier, not an Option component or slice element. Commands and reports are
under [`completeness/`](../logs/mutable-endpoints-proposal/completeness/);
[`comparison-check.json`](../logs/mutable-endpoints-proposal/completeness/comparison-check.json)
records the inspected paths and guard set.

The checker's feasibility fields say `not_run`; they are not represented
as successful checks. Constructive `all_caller_writes` and the separately
compiled
[`tests/mutable_endpoint_state.rs`](../tests/mutable_endpoint_state.rs)
provide lawful witnesses instead. Its **eight regression functions and
seven imported lemmas** pass, including documented changed contents,
wrong variant and initial-value rejection, unborrowed-position/length
rejection, non-Copy/non-static values, zero-sized values and a parameterless
generic empty witness. The successful run is
[`regressions-length-triggers/`](../logs/mutable-endpoints-proposal/value-state/regressions-length-triggers/).
The first regression input tried to declare an empty Rust enum, which this
Verus frontend rejected with `datatype must have at least one non-recursive
variant`; the diagnostic remains in `value-state/regressions/`. The final
empty proof quantifies over `T` without constructing it; real uninhabited
Rust slices are separately exercised by the native suite. A later length
rejection proof needed explicit update-length assertions to instantiate
the existing sequence rule; these are proof steps, not extra candidate
clauses. All earlier failures remain available.

The temporary redundancy check finds no removable semantic clause. The
nonempty bounds justify sequence indexing, the initial returned observation
and the final caller write describe different values, and the full final
sequence is independent of both inputs. Length and frame are consequences
of the update relation and are not repeated as candidate postconditions.
Five new Python binding tests also pass in
[`python-bindings.log`](../logs/mutable-endpoints-proposal/python-bindings.log).

These completeness results do not authorize either executable pattern
replacement. That separate independent permission was subsequently granted,
and only then were the two exact body replacements adopted. Their new
current-source compilations, native comparisons, actual selective export
and preservation checks are described in
[V-SLICE-PATTERN](V-SLICE-PATTERN.md#adopted-mutable-source-results).
The original rejected source bodies and direct-return analysis inputs remain
preserved. Final independent review of the adopted files is still required.

Neither active value-state input nor its candidate/dependencies changed on
adoption, so the existing independently reviewed analyze/reexecution results
were retained instead of rerun. The exporter checks their current/frozen
contents, complete comparisons, 13 disabled guards and actual target
results before copying the real generated sources to
[`first_mut.rs`](../proofs/completeness/slice/first_mut.rs) and
[`last_mut.rs`](../proofs/completeness/slice/last_mut.rs), relocating only the
state import. Those new files each compiled nine obligations: one generated
comparison, one adapter and the seven imported state lemmas. These counts
are distinct from each endpoint's single adopted source-proof target.
