# Slice specifications and source proofs

The source inventory contains 331 stable source-owned executable API
identities. Eighteen APIs have candidates and retained proof-track results: the six
original observers, the two slice-reference `Default` constructors, and
`core::slice::from_ref` / `core::slice::from_mut`, plus the two `[u8]`
in-place ASCII case conversions, `first_mut` / `last_mut`, and
`split_first_mut` / `split_last_mut`, plus the shared
`split_off_first` / `split_off_last`.
Four unchanged original source bodies, the two reviewed ASCII
source-derived bodies, eight individually approved slice-pattern conversions
and the separately permitted last split-off delegation
have successful implementation proofs on the selected upstream basis;
the other three remain blocked. The newly adopted last split-off input and
both split-off exports still require final independent review. All eight original
analysis inputs have actual deterministic specdet results, with the mutable
constructor using the proved observation adapter described below. That
adapter's redundancy repair has now passed engineering verification and
the second independent review. Both `Default` constructors are independently
reviewed in full `Seq<T>` value observation, not allocation-address determinism.

The singleton extension now also has a full initial-sequence/writeback
completeness check. Independent review confirmed the shared-value check,
the direct mutable extraction failure, and both array source failures.
The four-state mutable adaptation has completed independent review in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/63ed051184d5/round-0001.json`.
Both singleton source counts remain zero. This result is cited, not rerun,
in the ASCII work; the completed Default review is not reopened.

Both ASCII candidates now compare the entire final `Seq<u8>` for an arbitrary
initial sequence. Their actual analyses, reexecutions and exported comparisons
pass. Independent review approved six source-copy call rebindings, and the
repaired scalar and slice source proofs now compile and verify without new
assumptions. Six scalar dependencies are covered, not additional slice API
identities. Follow-up independent replay of the repaired source proofs and
result writeback remains pending.

The shared split-off candidates and their adopted current results are
described below. The remaining 313 identities have not been evaluated
in these bounded steps.
They are not exclusions from the campaign. Independent source/semantic checks and
dual-track reruns completed for the original inputs, within the scope
recorded below. They do not close the three remaining blocked source proofs or establish
any claim outside the stated value observation. **The slice module is not complete.**

[`coverage.tsv`](coverage.tsv) joins every canonical identity to its Rust
source/doc spans and selected-vstd coverage. The eighteen active rows additionally
name the predicate, unchanged value view, source proof inputs, available
generated completeness proofs, commands, queries, logs and issues. The
mutable row now names the generated four-state proof; its rejected direct
extraction remains separately recorded with no proof or original query.
[`apis.tsv`](apis.tsv)
retains the exact signatures, stability, owners and reexports; the ownership
and exclusion policy is in [`MODULE_MAP.md`](MODULE_MAP.md).
All Rust spans are relative to
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src`.

## Shared split-off endpoints after the permitted call rebinding

The new candidates in
[`split_off_post.rs`](../specs/slice/split_off_post.rs) observe the complete
original `Seq<T>`, the returned `Option<T>` value and the entire remaining
sequence in the reference slot at call return. Their exact public
declarations in [`split_off.rs`](../specs/slice/split_off.rs) are isolated from
the source proofs. Both selected-vstd bindings were absent. Neither candidate
adds an input, element trait bound or caller-final write environment.
The inner shared lifetime is independent of the short outer slot borrow;
public const invocation still requires `const_split_off_first_last`.

| API | Authoritative source | Current source proof | Actual complete comparison |
|---|---|---|---|
| `split_off_first` | `slice/mod.rs:4993-5015` | [Original receiver-lifted body](../proofs/correctness/slice/split_off_first.rs) compiled with `--no-cheating`: one target, no imported project proofs | [Direct declaration at line 15](../proofs/completeness/slice/inputs/split_off_first.rs); analyze and analyzed-directory reexecution each prove one goal, original UNSAT, eleven guards off |
| `split_off_last` | `slice/mod.rs:5043-5065` | [Adopted current body](../proofs/correctness/slice/split_off_last.rs) newly compiled with `--no-cheating`: one target, one shared split dependency and two existing consistency lemmas | [Direct declaration at line 15](../proofs/completeness/slice/inputs/split_off_last.rs); the same complete result and slot comparison passes both executions |

Independent review separately permitted the last delegated call to use the
unchanged, previously proved local shared `split_last`. The exact import
and call difference is now adopted; no first rebinding was needed.
The [permission and source argument](../issues/V-ASCII-CALL-BINDING.md#independent-split-off-permission-before-adoption)
do not authorize other conversions. The isolated proposal and original
external-binding failure remain in their historical files.

The selected checker directly generates independent post-call slot
observations, so no replacement adapter was introduced. The six
[`state lemmas`](../proofs/completeness/slice/split_off_state.rs) prove
totality, source/analysis value correspondence, ordered reconstruction and
full comparison equivalence. Five state regressions and seven public
composition/lifetime clients also compile. The two actual generated
comparisons compile separately with one goal apiece. The new aggregate
compiles with its two existing consistency lemmas; those are not split-off
source targets.

Current proof and checker commands, source snapshots and results are under
[`logs/split-off-endpoints/`](../logs/split-off-endpoints/);
isolated-proposal results are under
[`logs/split-off-endpoints-proposal/`](../logs/split-off-endpoints-proposal/).
The active native group is `split-off-endpoints`, reading the actual formal
files rather than the isolated proposal. It newly compiled Rust 1.96
metadata/MIR, linked and passed 20 runtime tests and 110 exact compiler
rejections through the restricted read-only command actions. The old
proposal execution route was replaced, while its files and failures remain.

`scripts/export_completeness.py --split-off-endpoints [split_off_first split_off_last]`
validates all selected current proofs and actual analyze/reexecute contents
before writing. It rejects failed, UNKNOWN, zero-goal, stale or incomplete
remaining observations without partially exporting another selection.
Both new [first](../proofs/completeness/slice/split_off_first.rs) and
[last](../proofs/completeness/slice/split_off_last.rs) exports compile with
one generated comparison each, using ordinary `--compile`; they are not
source implementation functions.

Five affected Python files compile, and 47 native-runner/binding/export
test methods pass, including 137 real export CLI invocations.
The actual export changed only these two coverage rows: 329 unselected raw
records, header/order and 21 previous top-level proof/state files remain
unchanged, as recorded in
[`export/preservation.json`](../logs/split-off-endpoints/export/preservation.json).
The first source, state and actual analyses were unchanged and independently
checked before adoption, so they were not rerun. Final independent review
now concerns the adopted last source and integration changes.

## Adopted mutable splits with two independently writable regions

The separate mutable split permission is recorded before adoption in
[V-SLICE-PATTERN](../issues/V-SLICE-PATTERN.md#independent-mutable-split-permission-before-adoption).
It covers exactly the two split/index bodies and their existing borrow-length
ghost blocks, not canonical Rust, vstd, metadata, indexing or other APIs.
Each formal file preserves its const signature, unrestricted `T`, mutable
receiver, result tuple order and pure candidate, with no target call or
local assumed target declaration.

| API | Authority and pure candidate | Current source result | Complete observation |
|---|---|---|---|
| `split_first_mut` | docs `slice/mod.rs:202-215`, body `220-222`; `mutable_splits_post.rs::split_first_mut_post` | [Current proof](../proofs/correctness/slice/split_first_mut.rs), newly compiled with `--no-cheating`: one source target, zero imported proof functions | [`split_first_mut_observation@7`](../proofs/completeness/slice/inputs/split_first_mut.rs), retaining the initial `(first, tail)` and entire final `seq![written_first] + written_tail` |
| `split_last_mut` | docs `slice/mod.rs:244-257`, body `262-264`; `mutable_splits_post.rs::split_last_mut_post` | [Current proof](../proofs/correctness/slice/split_last_mut.rs), newly compiled with `--no-cheating`: one source target, zero imported proof functions | [`split_last_mut_observation@7`](../proofs/completeness/slice/inputs/split_last_mut.rs), retaining initial `(last, init)` and entire final `written_init + seq![written_last]` |

The existing vstd `split_first_mut` binding is reused, not registered again.
Only the missing `split_last_mut` declaration is added in
[`specs/slice/mutable_splits.rs`](../specs/slice/mutable_splits.rs), separately
from the source proofs. The checker inputs are the initial `Seq<T>` and
caller-final `Option<(T, Seq<T>)>`; neither initial output nor final owner
is supplied in advance. The empty case needs no `T`; every independently
chosen final element and same-length remainder is covered by the proved
state relation. Cross-state remainder length is retained, while derived
initial-remainder and final-owner length clauses are not duplicated.

The unchanged seven state lemmas, adapters, aggregate, and actual
analyze/reexecute pairs were independently checked before source adoption.
Each main query remains one verified full comparison, original UNSAT and
all 19 search guards off. The current selective exporter checks content
against both frozen runs rather than pretending these are new executions.
Its two newly written comparison files each received an actual `--compile`
run: one generated comparison, one adapter and seven state lemmas, nine
functions and zero errors. Fresh current-source and exported results are
under [`logs/mutable-splits/`](../logs/mutable-splits/).

The native route now reads the adopted current files through
`scripts/check_native.py --group mutable-splits --output-root DIR`.
It replaces the isolated proposal route and has newly compiled Rust 1.96
metadata/runtime/const MIR, linked and passed 19 runtime tests plus 216
exact compiler rejections. Current extraction and binding tests passed
33 methods. The new real export tests passed 16 methods, including selection,
failure/staleness/UNKNOWN/zero-goal rejection, full observations, independent
writeback and preservation of every unselected file.

The actual export changed only these two rows and added their two
top-level comparison files. The other 329 raw rows, header/order and all
18 previous top-level completeness files are unchanged; historical failures
and isolated proposals remain in place. See
[`preservation.json`](../logs/mutable-splits/preservation.json).
The eight supplementary generic and `u8` negative searches still return
UNKNOWN; separately compiled concrete witnesses do not change those results.
They are retained, not rerun or counted as API successes. Final independent
review of the adopted files and export remains required.

## Adopted mutable endpoint source and complete return observations

The two additional candidates are in
[`specs/slice/mutable_endpoints.rs`](../specs/slice/mutable_endpoints.rs).
They reuse the existing `Seq<T>` view and public vstd bindings, preserve
unconstrained `T` and arbitrary legal caller writes, and observe both the
initial `Option<T>` and the whole returned input sequence.

| API | Authority and candidate | Adopted current source | Actual state analysis |
|---|---|---|---|
| `first_mut` | docs `slice/mod.rs:159-173`, body `178-180`; `first_mut_post` | [Current proof](../proofs/correctness/slice/first_mut.rs) uses only the independently permitted empty/indexed mutable borrow; newly compiled and verified one target, zero imported proof functions | [`first_mut_observation@8`](../proofs/completeness/slice/inputs/first_mut.rs): unchanged independently reviewed analyze and reexecution each pass one goal, original query UNSAT |
| `last_mut` | docs `slice/mod.rs:285-299`, body `304-306`; `last_mut_post` | [Current proof](../proofs/correctness/slice/last_mut.rs) uses only the independently permitted empty branch and computed final index; newly compiled and verified one target, zero imported proof functions | [`last_mut_observation@8`](../proofs/completeness/slice/inputs/last_mut.rs): unchanged independently reviewed analyze and reexecution each pass one goal, original query UNSAT |

The seven common state lemmas establish exact vstd correspondence, optional
caller shape, all legal writes, complete frames and the full comparison.
The separate adapters each compile with one adapter and those seven imported
lemmas. Source goals import only the pure candidate, not those lemmas or
assumed target declarations. The aggregate still checks two consistency
lemmas; none of these imported obligations is another API implementation.
Commands and actual outputs are retained in
[`logs/mutable-endpoints/`](../logs/mutable-endpoints/) for the adopted
source/native/export runs, and
[`logs/mutable-endpoints-proposal/`](../logs/mutable-endpoints-proposal/)
for the unchanged candidate/state/checker runs.
Direct mutable extraction failures and the original failed source runs
are retained separately from the successful isolated runs.

The two exact source conversions received their own independent permission
before adoption, as recorded in
[V-SLICE-PATTERN](../issues/V-SLICE-PATTERN.md#independent-mutable-permission-before-adoption).
The optional observation argument and actual comparisons are recorded in
[S-MUT-RETURN](../issues/S-MUT-RETURN.md#optional-mutable-endpoint-observations).
The real `--mutable-endpoints` export updates only those two coverage rows
and adds two actual generated checker files, each compiled with one comparison,
one adapter and seven imported lemmas. All 329 unselected rows and 15 prior
completeness Rust files remain byte-identical. The 170 mutable CLI cases
check selection, preservation and rejection of failed, zero, stale or
incomplete-writeback evidence. The adopted native comparison actually passed
17 runtime tests and 96 expected rejections with Rust 1.96.
Final independent review of the adopted files and export is still required.
This work does not close the metadata or singleton source gaps, or the module.

## Retained original results and current revision status

| API | Rust 1.96 implementation proof | Actual specdet result | Local issue |
|---|---|---|---|
| `len` | Rejected before source-body verification: reference-to-pointer coercion; isolated raw metadata call also unsupported | `deterministic`, original query UNSAT, one checked goal | [V-METADATA](../issues/V-METADATA.md) |
| `is_empty` | Verified and compiled: one target function, plus two imported consistency lemmas | `deterministic`, original query UNSAT, one checked goal | Uses the existing upstream `len` contract; its Rust 1.96 dependency proof remains blocked |
| `first` | Approved length/index conversion compiled and verified: one target plus two imported consistency lemmas | Fresh analyze and reexecution: `deterministic`, original query UNSAT, one checked goal each | [V-SLICE-PATTERN](../issues/V-SLICE-PATTERN.md#adopted-current-source-results); final independent review pending |
| `split_first` | Approved length/index/split_at conversion compiled and verified: one target plus two imported consistency lemmas | Fresh analyze and reexecution: `deterministic`, original query UNSAT, one checked goal each; all eleven search guards off | [V-SLICE-PATTERN](../issues/V-SLICE-PATTERN.md#adopted-split-source-results); final independent split review pending |
| `split_last` | Approved length/index/split_at conversion compiled and verified: one target plus two imported consistency lemmas | Fresh analyze and reexecution: `deterministic`, original query UNSAT, one checked goal each; all eleven search guards off | [V-SLICE-PATTERN](../issues/V-SLICE-PATTERN.md#adopted-split-source-results); final independent split review pending |
| `last` | Approved length/index conversion compiled and verified: one target plus two imported consistency lemmas | Fresh analyze and reexecution: `deterministic`, original query UNSAT, one checked goal each | [V-SLICE-PATTERN](../issues/V-SLICE-PATTERN.md#adopted-current-source-results); final independent review pending |
| `<&[T] as Default>::default` | Original `&[]` verified and compiled: one target function, no imported proof functions | `deterministic` in analyze and reexecution; one checked goal each | None |
| `<&mut [T] as Default>::default` | Original `&mut []` verified and compiled: one target function, no imported proof functions | Original and reduced adapters: `deterministic` in analyze and reexecution, one checked goal each | [S-MUT-RETURN](../issues/S-MUT-RETURN.md), direct extraction unsupported; revised adapter independently reviewed in full `Seq<T>` value observation |
| `core::slice::from_ref` | Array delegate rejected at reference-to-pointer cast; zero target and zero dependency functions verified | Analyze and reexecution UNSAT, one generated goal each; relocated proof compiled; independently reproduced | [V-METADATA](../issues/V-METADATA.md#singleton-array-delegation-on-the-same-baseline); source limitation independently reproduced |
| `core::slice::from_mut` | Array delegate rejected at reference-to-pointer cast; zero target and zero dependency functions verified | Complete state adaptation independently reviewed; analyze and reexecution UNSAT, one generated goal each; exported proof compiled | [V-METADATA](../issues/V-METADATA.md#singleton-array-delegation-on-the-same-baseline), [S-MUT-RETURN](../issues/S-MUT-RETURN.md#complete-mutable-value-state-adaptation); direct mutable extraction still unsupported |
| `<[u8]>::make_ascii_uppercase` | Reviewed call rebinding verified and compiled: one target and six scalar source functions; 13 obligations including auxiliary checks | Analyze and reexecution UNSAT for the full final sequence; one generated comparison goal for this API; exported proof compiled | [V-ASCII-CALL-BINDING](../issues/V-ASCII-CALL-BINDING.md); repaired source proof independent replay pending |
| `<[u8]>::make_ascii_lowercase` | Reviewed call rebinding verified and compiled: one target and six scalar source functions; 13 obligations including auxiliary checks | Analyze and reexecution UNSAT for the full final sequence; one generated comparison goal for this API; exported proof compiled | [V-ASCII-CALL-BINDING](../issues/V-ASCII-CALL-BINDING.md); repaired source proof independent replay pending |

The successful `is_empty` query is retained in
`logs/foundation/correctness/is_empty/queries/root.smt2`.
Its body is the original `slice.len() == 0`, not a call to `is_empty`
under its candidate contract. The five original failure diagnostics remain
present. The two original endpoint proof inputs were preserved in
`logs/endpoints/adoption-before/` before adopting their independently approved
desugaring. Original split proof inputs are separately preserved in
`logs/splits/adoption-before/`; `len` and `is_empty` remain unchanged.
No new assumption, external body, nonterminating implementation or verifier
change closes a source proof.

The unchanged `is_empty` source proof was compiled again for this constructor
integration with `--no-cheating`: one target function and two imported
consistency lemmas passed. That integration's command, queries and output are in
[`logs/defaults/correctness/is_empty/`](../logs/defaults/correctness/is_empty/).
This establishes only `slice.len() == 0` against the already trusted vstd
length contract. It does not establish Rust 1.96 `ptr::metadata`, close
`len`, or remove [V-METADATA](../issues/V-METADATA.md).

## Adopted first/last source correspondence

Independent review permitted only the exact two conversions in
[V-SLICE-PATTERN](../issues/V-SLICE-PATTERN.md#independent-permission-before-adoption).
The current first proof returns `None` for zero length and otherwise
`Some(&slice[0])`; the last uses the same empty branch and otherwise
`Some(&slice[slice.len() - 1])`. The permission covers shared borrowing at the
same element position, all legal lengths, stable const behavior and
unreachable indexing/subtraction failures, without changing the candidates,
signatures, authoritative Rust or either split method.

The current source compilations in `logs/endpoints/correctness/{first,last}/`
each checked one target plus two imported consistency lemmas, with
`--compile --no-cheating --num-threads 1`, zero errors and nonempty compiled
libraries. The aggregate in `correctness/aggregate_current/` compiled and
verified its two consistency lemmas using the existing specification-binding
workflow. It does not use `--no-cheating`, which correctly rejects its
pre-existing `assume_specification` declarations; the source proofs do.
Both the earlier rejected aggregate flag combination and invalid crate-name
invocation remain under `logs/endpoints/correctness/`.

Only the two actual selectors
`proofs/completeness/slice/inputs/first.rs:first@13` and
`proofs/completeness/slice/inputs/last.rs:last@13` were analyzed and reexecuted.
Each of the four invocations in `logs/endpoints/completeness/{first,last}/`
selected one endpoint, verified one full variant/element-value comparison,
and reported original-query UNSAT with all seven search guards off.
Input, contract, configuration and actual native-worktree bytes match;
the replay preserves the same harness and query. These results do not claim
allocation-address determinism or prove the upstream metadata implementation.

The current-source native group, `check_native.py --group endpoints`,
passed 14 runtime cases and 60 diagnostic-checked invalid programs against
the authority, adopted proofs and public calls. It preserves `--output-root`
and retains the compiled source and MIR. Its records are in
`logs/endpoints/adopted-native-root/logs/endpoints/native/`.
The independent pre-adoption review could not link runtime tests because
its sandbox lacked `cc`; it did not independently execute those runtime
cases. That limitation remains distinct from the reviewed all-input
correspondence and independently checked isolated Verus/MIR evidence.

The real `export_completeness.py --endpoints` invocation changed only
four source-result fields in each of the two coverage rows. The other
329 rows, all completeness cells, all 14 exported completeness files and
the five historical failure logs remained byte-identical, as recorded in
`logs/endpoints/export-current/results.json`. Fresh checker results are linked
above rather than replacing the old completeness records. Export validation
rejects failed/zero/partial proofs and stale inputs; 11 tests exercised
117 real CLI cases. Source-binding/native-runner Python tests and the revised
post-export coverage assertion also passed. The final independent review of
these adopted files and this export is still required.

## Candidate and checker binding

The separately authorized split conversions are now the current source-proof
bodies. Their source and aggregate compilations are in
`logs/splits/correctness/`; discovery and the two one-target
analyze/reexecution pairs are in `logs/splits/completeness/`. Full ordered
remainder equality is included, not only the element and return variant.
The eleven actual search guards, including four remainder-length guards,
are all off. The existing `split_at` contract remains a named trusted
dependency, not a source proof of that method.

`scripts/check_native.py --group splits` reads the adopted files and passed
15 runtime tests and 120 diagnostic-checked rejections. Its 32 runner/binding
tests, 25 shared-export tests with 254 recorded real CLI cases and one revised
coverage assertion passed. The real `--splits` export changed only four
source-result cells in each split row; the other 329 rows, all 14
completeness files and five historical failure logs remained byte-identical.
Exact commands and results are linked from
[the issue](../issues/V-SLICE-PATTERN.md#adopted-split-source-results).
These are engineering executions and still need final independent review;
the pre-adoption independent linker failure is retained separately.

`specs/slice/mod.rs` defines six candidate predicates, rather than redeclaring
or replacing the five existing vstd method contracts. The sixth method,
`split_last`, has no selected-vstd contract. The nonempty root
`specs/mod.rs` compiles and verifies two consistency lemmas; those two
lemmas are not implementation proofs. The aggregate also imports the real
`Default` bindings from `specs/slice/default.rs` and the singleton bindings
from `specs/slice/raw.rs`, together with the two ASCII mutation bindings in
`specs/slice/ascii.rs`. The original
six-predicate file and the selected value-view definition remain unchanged.

The view is the selected upstream `View for [T] = Seq<T>`, documented in
`specs/shared/SLICE_VIEW.md`. There are no target preconditions or additional
`Copy`, `Eq` or `'static` bounds. The predicates constrain length/boolean
answers, `Option` variants, element values and the complete ordered remainder.
The `split_last` pair is `(last, init)`.

For the original six observers, the analysis declarations in
`proofs/completeness/slice/inputs/` have the
same generic types, const source functions and reference lifetimes as the
source copies. Every declaration calls the identical predicate used by its
correctness input, with no added premise. Their contract-preserving binding
is checked by the Rust compiler and the source/signature/predicate comparisons
in `tests/test_contract_bindings.py`. Their `assume_specification` declarations
are confined to completeness analysis and never imported by the correctness
files or specification aggregate.

The real checker uses `verus-observable-v1` without customization. Inspection
of the generated comparisons confirmed scalar equality; matching `Option`
variants and element values for `first`/`last`; and matching variants, first
tuple fields and **extensional equality of the full returned slices** for
the splitting methods. This is value-view completeness, not an additional
claim about reference allocation addresses. The Engineer's retained native
behavior probes separately check the actual references with pointer equality.

The native checker generates guarded search assumptions. In each retained
`query/originalC.smt2`, the final `check-sat-assuming` disables every search
guard, including `g_neq_tuple`. The reported UNSAT results therefore concern
the original problem, not a narrowed search case. The source predicates are
unchanged between the two tracks. No nondeterministic, inconclusive or
unevaluated result is counted as deterministic.

`scripts/export_completeness.py` checks the current predicate, adapter and
configuration bytes against each frozen checker snapshot, then exports the
native harness to `proofs/completeness/slice/<api>.rs`. Its only source change
is relocating the unchanged predicate import, or the mutable singleton's
proved state-module import. Native originals, query files, solver reports and process commands
remain under `proofs/completeness/slice/runs/<api>/`.
All six relocated harnesses were actually compiled and verified: each checks
one generated determinism function and two imported consistency lemmas.
Their replay logs are under `logs/foundation/exported/<api>/`.

## Singleton reference constructors

The authoritative source is Rust 1.96 `slice/raw.rs:198,203-205` for
`from_ref` and `slice/raw.rs:207,211-213` for `from_mut`. The corresponding
array documentation and bodies are `array/mod.rs:163-169,171-177`.
Both slice copies remain `pub const fn`, take exactly one reference to an
implicitly `Sized` unconstrained `T`, preserve the input-tied elided lifetime,
and execute only `array::from_ref(s)` or `array::from_mut(s)`.
Stable const calls are supported since Rust 1.63 and 1.83 respectively.

[`raw.rs`](../specs/slice/raw.rs) uses
[`singleton_post`](../specs/slice/raw_post.rs), defined by
`elements =~= seq![value]`. The shared result is the full singleton sequence
of `*s`. The mutable contract relates the initial result to `*old(s)` and
the final returned slice to `*final(s)`. The latter is an independent
cross-state return relation, not a requirement to preserve the initial value.
No separate length or element clause is retained: the singleton sequence
already implies both. No element bounds, preconditions or address-determinism
claim are introduced.

The two source proof inputs,
[`from_ref.rs`](../proofs/correctness/slice/from_ref.rs) and
[`from_mut.rs`](../proofs/correctness/slice/from_mut.rs), resolve `array` to
[`array/singleton.rs`](../proofs/correctness/array/singleton.rs). That file
retains both original unsafe pointer-cast expressions and adds only their
candidate postconditions. There is no assumed contract for either array
delegate. The existing vstd array/slice coercion relations are the intended
second step; they do not establish the first step from `&T` to `&[T; 1]`.

Actual `--compile --no-cheating` runs of the array file and both API files
reject both casts before verification. Each API file contains one target and
two imported dependency functions, but **zero of either kind were verified**.
The array-only run likewise verified zero of its two functions. Commands,
exit codes, full output and verifier logs are under
[`logs/singletons/correctness/`](../logs/singletons/correctness/).
The contract-free
[`reference-cast reproduction`](../issues/repros/singleton_reference_casts.rs)
fails at the same two conversions, independently of the candidate predicates.
Its output is under
[`reference-cast-repro/`](../logs/singletons/reference-cast-repro/).
No executable rewrite, verifier change or new dependency assumption was made.

The aggregate compiled with `--compile`: two existing consistency lemmas,
zero errors, not two singleton source proofs. Its successful command is in
[`aggregate-bindings/`](../logs/singletons/aggregate-bindings/).
The earlier command in `aggregate/` incorrectly also requested
`--no-cheating`, which rejects the aggregate's specification declarations;
that invocation is retained and is not evidence against an executable body.

The original discovery selected
`proofs/completeness/slice/inputs/from_ref.rs:from_ref@8` and
`proofs/completeness/slice/inputs/from_mut.rs:from_mut@8` using
[`singletons.toml`](../proofs/completeness/slice/singletons.toml).
The shared analyze and `replay --reexecute` each proved one original
determinism goal with UNSAT. Their comparison uses the same unconstrained
input `s` and complete returned slice values, with only the two candidate
postconditions as premises and all original-query search guards disabled.
[`from_ref.rs`](../proofs/completeness/slice/from_ref.rs) is the actual
generated proof with only its predicate import relocated; it compiled with
one generated goal and no imported proof functions. Reports and commands
are under
[`completeness/from_ref/`](../logs/singletons/completeness/from_ref/) and
[`export-selections/`](../logs/singletons/export-selections/).

The original direct mutable analyze and reexecution both return the diagnostic
`unsupported_mutable_return`, with exit code 2 and no proof or query.
Those complete reports are under
[`completeness/from_mut/`](../logs/singletons/completeness/from_mut/).
The original input is now retained byte-for-byte at
[`history/from_mut_direct.rs`](../proofs/completeness/slice/history/from_mut_direct.rs),
outside current target selection. No Default-style shared reborrow is
substituted: it would omit the caller-owned input's final return relation.
The current full-state adaptation is described below.

The supplemental
[`contract clients`](../tests/singleton_contract_clients.rs) compile against
the candidate public bindings. The shared-content client verified one
function; the final generic arbitrary-replacement client verified one
function, after explicitly observing sequence index zero in ghost code.
The current writeback result is in
[`contracts-writeback-index/`](../logs/singletons/contracts-writeback-index/);
earlier failed client attempts remain in `contracts/` and
`contracts-writeback/`. These are clients of assumed target contracts,
not proofs of the source or of the array delegates.

Rust 1.96 compiled and executed 16 native tests and correctly rejected 66
negative programs through `scripts/check_native.py --group singleton`.
Both the real public APIs and source copies are exercised, including exact
types, one-argument calls, const evaluation, non-Copy/non-static elements,
zero-sized elements, pointer correspondence, lawful writes and borrow
rejections. The independent output root is
[`native-singleton-20260922-111038/`](../native-singleton-20260922-111038/);
all generated probes were removed, while commands and diagnostics remain.
Eleven native-runner Python tests, six source/binding tests and six export
tests passed. `--singletons` exports only available real proofs, and its
individual API selectors preserve all unrelated coverage rows and exports.
The original eight exports and completed Default review were not changed
or reexecuted.

### Independent singleton review

The record
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/d67769d288a6/round-0001.json`
independently confirmed the source/docstring and signature correspondence,
the shared full-sequence determinism result, and the two distinct tool
limitations. Reviewer reproduced the array and both slice compilation
failures with zero verified source functions, and matched the contract-free
casts to `AutoBorrow::RawPtr` in `rust_to_vir_expr.rs:1688-1693`.
Shared analyze and reexecution each verified one goal with original query
UNSAT; direct mutable analyze and reexecution each stopped before any goal.
The temporary redundancy check found the two mutable states independent.

That review also compiled four Python files, ran 22 related tests and five
real export selections, and confirmed unchanged nonselected files. Its
native Rust run stopped at missing `cc` before behavior tests; the earlier
16 behavior and 66 rejection results are not independent native reruns.
This completeness-only work does not repeat the unchanged source failures,
native suite, six observers, or completed Default review.

### Complete mutable singleton state relation

The current entry
[`inputs/from_mut.rs`](../proofs/completeness/slice/inputs/from_mut.rs)
keeps the input's initial value and the caller's final slice contents as
separate environment values in `Ghost` carriers. Its output is
`Ghost<(Seq<T>, T)>`: the entire initial returned sequence and the entire
input value returned after the borrow. Neither output is an input premise.
The public signature, original execution expressions, and both clauses in
`specs/slice/raw.rs` remain unchanged.

[`from_mut_state.rs`](../proofs/completeness/slice/from_mut_state.rs)
proves the exact original two-state relation, derives the length-one final
environment from existing borrowed-slice length preservation, covers every
such caller sequence without relating it to the initial element, and proves
the indexed final-value restatement and complete value comparison. The
analysis requires only this derived environment domain, not an additional
public API precondition. No new trusted function, array assumption, trait
bound, or lifetime restriction is introduced.

Actual discovery selected
`proofs/completeness/slice/inputs/from_mut.rs:from_mut_observation@9`.
Analyze and `replay --reexecute` each verify one generated goal with
original query UNSAT and no diagnostics. The exact generated comparison is
`((r1@.0 =~= r2@.0) && (r1@.1 == r2@.1))`; all seven search guards are off.
The current input, state file, predicate, public binding, and configuration
match both frozen source copies. The reports are
[`completeness/from_mut-ghost-inputs/`](../logs/singleton-writeback/completeness/from_mut-ghost-inputs/).
The original direct failure, the first relational UNKNOWN, and the
intermediate indexed representation remain historical; none is counted as
the current successful check.

The actual verification counts for this bounded implementation are:

| File or execution | Relevant functions verified | Imported project proof functions |
|---|---:|---:|
| `from_mut_state.rs`, `--compile --no-cheating` | 5 correspondence/domain/value lemmas | 0 |
| Current mutable input, `--compile --no-cheating` | 1 analysis function | 5 state lemmas |
| `tests/from_mut_state.rs`, `--compile --no-cheating` | 5 regression proofs | 5 state lemmas |
| Actual analyze / actual reexecution | 1 generated determinism goal each | 0 selected |
| Exported `from_mut.rs`, `--compile` | 1 generated goal and 1 analysis function | 5 state lemmas |
| `specs/mod.rs`, `--compile` | 0 singleton source functions | 2 existing consistency lemmas |
| Both singleton source APIs | 0, unchanged independently confirmed frontend failure | 0 |

The formal regressions include changed initial/final contents, arbitrary
generic and non-Copy/non-static values, and zero-sized elements.
[`scripts/check_singleton_writeback.py`](../scripts/check_singleton_writeback.py)
also runs the real checker on scratch `bool` instances, with the same full
tuple observation. The complete instance is deterministic (one goal,
UNSAT). Removing the initial clause produces `[false]` versus `[true]`
with the same input return; removing the return clause produces the same
`[false]` sequence with return values `false` versus `true`.
Each is a conclusive native `nondeterministic` result supported by one
verified constructive witness. Their SMT baselines are UNKNOWN, not
counterexamples; the separately verified witness proofs establish the
loss of the respective observation. See
[`weakening-ghost-inputs/results.json`](../logs/singleton-writeback/weakening-ghost-inputs/results.json)
and the linked native certificates.

The driver initially treated each certificate filename as a directory
after the actual checker runs completed. The corrected reader passes
`--check-existing` on those same results and three focused unit tests;
unchanged analyses were not repeated. Older controls with destructured
`Ghost` inputs failed witness mode checking and remain historical.
These details and the complete observation mapping are in
[S-MUT-RETURN](../issues/S-MUT-RETURN.md#complete-mutable-value-state-adaptation).

Six modified/new Python files have been compiled without bytecode output.
The 35 related binding/export tests and three counterexample-reader tests
pass. The former include 15 real scratch CLI cases: mutable-only, default
dual selection, explicit selections, invalid selections, and stale
dependencies. The actual mutable-only export changes only its coverage row
and proof; all 330 other rows and all other proof files remain byte-identical.
Commands and outputs are in
[`export-selections-ghost-inputs/`](../logs/singleton-writeback/export-selections-ghost-inputs/)
and [`weakening-ghost-inputs/`](../logs/singleton-writeback/weakening-ghost-inputs/).
Scratch output can be redirected with `TMPDIR` and
`SINGLETON_EXPORT_TEST_LOG_DIR` for the CLI tests, or `--output-root` for the
real checker controls, including under a read-only review mount.

The mutable completeness work has now completed independent review under
`review-criteria-temporary.txt`. The authoritative record is
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/63ed051184d5/round-0001.json`.
Reviewer confirmed all five state lemmas, the analysis function, the current
generated comparison, analyze/reexecution, both constructive weakening
controls and selective exports. The temporary redundancy check found the
initial and returned-state relations independent. This paragraph records
that completed review without repeating it. The coverage review column
remains pending for the full singleton APIs because neither source bridge
has been proved. Neither this adaptation nor the aggregate's consistency
lemmas complete either API or the slice module.

## In-place ASCII case conversion

Rust 1.96 documents uppercase conversion at `slice/ascii.rs:161-169` and
lowercase conversion at `183-191`; their original bodies are `173-181` and
`195-203`. Both are `pub const fn make_ascii_*case(&mut self)`, take no
additional arguments, and return unit. They are stable since 1.23 and callable
in stable const contexts since 1.84. The proof copies lift
`self` to `slice: &mut [u8]`, add ghost annotations, and apply the independently
reviewed scalar-call rebindings. The loop, indexed reborrow, scalar algorithm,
increment and unit-returning const signatures are unchanged.

[`ascii.rs`](../specs/slice/ascii.rs) binds the actual public APIs.
[`ascii_post.rs`](../specs/slice/ascii_post.rs) uses the existing sequence view:

```rust
uppercase_post(initial, result) =
    result =~= initial.map_values(|byte: u8| uppercase_byte(byte))
lowercase_post(initial, result) =
    result =~= initial.map_values(|byte: u8| lowercase_byte(byte))
```

The upper mapping subtracts 32 only for `b'a'..=b'z'`; the lower mapping adds
32 only for `b'A'..=b'Z'`. All other bytes are unchanged, including 0, 255 and
every non-ASCII byte. There is no input precondition, ASCII/UTF-8 restriction
or nonempty requirement. The single full-sequence equality already fixes
length, order and each unchanged byte, so no redundant length or per-index
clause is added. Each actual binding instantiates it with
`old(slice)@` and `final(slice)@`, not with the unit return.

The exact scalar source chain and observed missing method bindings are in
[V-ASCII-CALL-BINDING](../issues/V-ASCII-CALL-BINDING.md). The original
`is_ascii_uppercase` and `is_ascii_lowercase` classification bodies each
verify without assumptions. Their corresponding `u8` methods are distinct
external functions: the original conversions and mutations were rejected at
those external calls before verification. The retained contract-free reproduction
rejects the same six calls. A separate indexed-reborrow/assignment proof
verifies the complete sequence-update relation on the existing upstream
indexing basis. It does not prove Rust 1.96 indexing or length internals,
close [V-METADATA](../issues/V-METADATA.md), or by itself prove either casing
loop. Independent review approved exactly six calls to the corresponding
local source bodies. With those rebindings and four ghost bit-vector
assertions, both casing loops now verify with their original invariants.
No missing scalar contract is assumed.

The actual counts for the current ASCII proofs are:

| File or execution | Verified obligations | Scope |
|---|---:|---|
| `proofs/correctness/num/u8_ascii_classify.rs`, `--compile --no-cheating` | 2 | Scalar source dependencies; no imported proof functions or lemmas |
| `proofs/correctness/num/u8_ascii.rs`, same flags | 11 | Six scalar source bodies, one constant and four bit-vector assertions |
| Each `proofs/correctness/slice/make_ascii_*case.rs`, same flags | 13 | One slice body, six scalar bodies, one loop, one constant and four bit-vector assertions |
| `issues/repros/ascii_mutable_index.rs`, same flags | 1 | Indexed write and full complement preservation, not an API source proof |
| `proofs/completeness/slice/ascii_state.rs`, same flags | 3 | State correspondence, lawful outputs and complete value comparison |
| Each ASCII analysis input, same flags | 4 | 1 observation function plus the 3 state lemmas |
| Each actual analyze | 1 | Generated comparison for the selected API; original query UNSAT |
| Each retained config-backed `replay --reexecute` | 2 | Both configured ASCII targets, one comparison each; both original queries UNSAT |
| Each exported comparison, `--compile` | 5 | 1 generated goal, 1 observation function and 3 state lemmas |
| `specs/mod.rs`, `--compile` | 2 | Existing consistency lemmas only; zero new API source proofs |

Commands, exit codes, compiled libraries, source snapshots and verifier output
for the repaired proofs are retained under
[`logs/ascii-case/rebinding/`](../logs/ascii-case/rebinding/).
The original external-call failures and the first rebound scalar run's two
bitwise postcondition failures remain separate. The six scalar functions
are dependency proofs, not new entries in the 331-API denominator.

### Complete mutable-state observation

[`ascii_state.rs`](../proofs/completeness/slice/ascii_state.rs) proves the
candidate's `old`/`final` relation is exactly the full pointwise sequence map.
It gives lawful length-preserving outputs for every initial `Seq<u8>`,
without restricting bytes or requiring an unchanged final state, and connects
slice-value equality to complete view equality. These are observation lemmas,
not implementations of the public methods.

The analysis functions take only `Ghost<Seq<u8>>` for the initial sequence
and return `Ghost<Seq<u8>>` for the entire final sequence. The final sequence
is not an input or a shared premise. The public API retains its mutable
receiver and unit return. No allocation-address claim or extra observation
of unrelated memory is introduced; the native subslice checks below exercise
the frame outside the borrowed range.

Real discovery in
[`discover.json`](../logs/ascii-case/completeness/discover.json) found exactly
the two project-relative targets:
`proofs/completeness/slice/inputs/make_ascii_uppercase.rs:make_ascii_uppercase_observation@9`
and
`proofs/completeness/slice/inputs/make_ascii_lowercase.rs:make_ascii_lowercase_observation@9`.
Each analyze proves one comparison. Passing the explicit two-target
configuration to replay selected both targets in each retained reexecution;
each therefore proves two comparisons, rather than one. Both relevant
reexecuted comparisons match their analyzed originals byte-for-byte. No
additional replay was run to change that presentation.

The native comparison is `((r1)@ =~= (r2)@)` over full sequences.
Its only premises are the same mapping predicate for the same initial
sequence and the two independently quantified final sequences. Each original
SMT query disables **all 55 search guards**, including every byte-search guard
and `g_neq_tuple`; no bounded case is substituted for the original problem.
The checker's feasibility analysis is not run; the separately verified
`lawful_outputs` and observation functions provide witnesses instead.
The current input, state file, predicate, public binding and configuration
match the frozen checker sources for analyze and replay.

[`export_completeness.py`](../scripts/export_completeness.py) adds
`--ascii-case`, with optional selection of either API. It verifies the exact
target, complete comparison, original premises, disabled search guards and
current source bytes before exporting. Only the relative state-module import
is changed in
[`make_ascii_uppercase.rs`](../proofs/completeness/slice/make_ascii_uppercase.rs)
and
[`make_ascii_lowercase.rs`](../proofs/completeness/slice/make_ascii_lowercase.rs).
The actual export changed just these two proof files and the two selected
coverage rows; all **329 unselected rows** and all unselected proof files
remained byte-identical, as recorded in
[`export/isolation.json`](../logs/ascii-case/export/isolation.json).
Neither singleton coverage row was rewritten.

The current exporter additionally requires a successful compiled source run
with all 13 obligations and checks the slice body, both scalar modules and
predicate against the successful run's saved source bytes. The new export
records one source target per API, not the previous zero. It changes only the
two ASCII coverage rows and leaves all 329 other rows and all 14 completeness
proof/state files byte-identical:
[`rebinding/export/isolation.json`](../logs/ascii-case/rebinding/export/isolation.json).
The old ASCII rows and all original proof logs remain available.

### Independent review and source repair

The independent review in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/d52fae2975c8/round-0001.json`
confirmed the source spans, concrete `u8` callees, const signatures, receiver
coercions, evaluation order and nonescaping indexed reborrows. It approved
only the six substitutions listed in V-ASCII-CALL-BINDING, not an algorithm
or input-domain change. The revised source-correspondence tests compare each
body after exactly those substitutions, rather than dropping the comparison.

That review independently analyzed both unchanged line-9 targets: exit 0,
one complete-sequence comparison each, original query UNSAT and all 55 search
guards disabled. It also compiled the aggregate and exported comparisons and
verified the three state lemmas. Those unchanged results are reused here;
the specification, state helpers, analysis inputs and configuration were not
edited. The temporary redundancy review found no clause to delete: the one
full-sequence relation includes the required cross-state writeback.
The repaired source proofs now supply successful engineering results for the
previously missing correctness dimension. Their independent replay remains
pending.

### Native and Python checks

The original `scripts/check_native.py --group ascii-case --output-root .` compiled
and ran **17 Rust 1.96 tests** and rejected **16 invalid programs**.
Both exact source copies and actual public calls are exercised. The tests
cover every single-byte input, empty and mixed ordered slices, letter
boundaries and adjacent punctuation, 0 and 255, every non-ASCII value,
idempotence, alternating conversions, and local slice mutation with unchanged
prefix/suffix. Expected values use the numeric ASCII intervals and offsets,
not calls to the tested functions. Exact `fn(&mut [u8]) -> ()` types and
stable const calls compile without `RUSTC_BOOTSTRAP`; shared receivers,
wrong element types, wrong returns and extra arguments are rejected.
Zero tests and linking failures cannot count as behavior success.
Commands, copied source spans and diagnostics remain in
[`native/`](../logs/ascii-case/native/); this run's temporary probes and
binaries were removed.

Across the focused runs, **38 Python unittest cases** passed, including the
new native group, source/binding checks, real selective exports, and affected
existing group/export behavior. The actual CLI cases check that stale source
snapshots, unit-only comparisons, extra premises and active search guards
cannot be exported, and that invalid selectors leave coverage and proofs
unchanged. One initial test incorrectly expected JSON-escaped quotes in the
CSV const-stability cell. Only that assertion was corrected and rerun; the
initial failure remains in
[`python-checks/first/`](../logs/ascii-case/python-checks/first/), with its
correction in
[`python-checks/const-stability/`](../logs/ascii-case/python-checks/const-stability/).
No completed Default or singleton source proof was rerun.

After the approved rebinding, ten affected Python tests passed: five
source/specification comparisons and five export tests covering 25 real CLI
cases. These retain selection isolation, reject failed/empty/partial source
runs and stale source dependencies, and preserve the original failure logs.
Their commands and outputs are in
[`rebinding/python-tests/`](../logs/ascii-case/rebinding/python-tests/).
The independent review's native run stopped at missing `cc` during linking;
it did not run the 17 behavior cases or the 16 rejection cases. Those older
native results are not presented as new results, and unchanged native inputs
were not rerun for this source-proof-only repair.

Both proof dimensions now have successful results for the unchanged
full-sequence candidates, with the newly repaired source proofs awaiting
independent replay. `review-criteria-temporary.txt` continues to apply;
neither API nor the slice module is declared independently complete here.

## The two default constructors

The real public bindings are
`<&'a [T] as core::default::Default>::default()` and
`<&'a mut [T] as core::default::Default>::default()`. Both take no arguments.
The source signatures are `fn default() -> Self`, with unconstrained `T`
and the reference lifetime belonging to `Self`. The shared implementation
is stable since 1.0.0, the mutable one since 1.5.0; their const-trait calls
remain unstable under `const_default` in Rust 1.96. No new `Copy`, `Default`
or `'static` element constraint, const-call promise, or precondition is
introduced.

The source/docstring correspondence is:

| Canonical API | Rust 1.96 source / docstring | Source proof |
|---|---|---|
| `<&[T] as core::default::Default>::default` | `slice/mod.rs:5635-5637` / `5634`: "Creates an empty slice." | [`default_shared.rs`](../proofs/correctness/slice/default_shared.rs) |
| `<&mut [T] as core::default::Default>::default` | `slice/mod.rs:5644-5646` / `5643`: "Creates a mutable empty slice." | [`default_mut.rs`](../proofs/correctness/slice/default_mut.rs) |

The proof copies lift the external trait methods into free functions,
substitute the corresponding reference type for `Self`, and make the
impl's elided lifetime explicit. Another crate cannot redeclare these std
impls. These are binding-only translations: the executable bodies are
still exactly `&[]` and `&mut []`. No const trait implementation is
advertised as a stable const function.

[`default_post.rs`](../specs/slice/default_post.rs) requires the entire
existing value view to equal `Seq::<T>::empty()` extensionally. Both the
public bindings and both proof tracks use that same predicate. There is
no new view or trusted observer. Each implementation proof imports only
this pure predicate, never the declaration that assumes its own answer.
The selected upstream array view and array-to-slice coercions connect the
zero-element array literals to the existing slice view: see `array_view`,
`array_as_slice`, and `ref_mut_array_unsizing_coercion` in
`toolchain/upstream/source/vstd/array.rs`, and `View for [T]` in
`toolchain/upstream/source/vstd/slice.rs`.

The shared proof's initial equality-automation attempts remain in
`logs/defaults/correctness/default_shared-unassisted/` and
`default_shared-len-trigger/`. The final candidate uses Verus's sequence
extensional equality operator `=~=`, not a weaker length-only observation.
No executable expression changed in that repair; both tracks were then
run on the current predicate.

### The mutable-return analysis

Direct specdet analysis of the actual mutable declaration fails before
generating a goal; the input, exact diagnostic and report remain linked
from [S-MUT-RETURN](../issues/S-MUT-RETURN.md). This direct failure is not
counted as a completeness success.

The separate
[`inputs/default_mut.rs`](../proofs/completeness/slice/inputs/default_mut.rs)
contains the analysis adapter. Its revised `observe` retains
`result@ == old(value)@`: the shared reborrow has the identical full
sequence view of an arbitrary mutable slice. **Predicate preservation
follows from full view equality** by substitution, because `default_post`
only requires extensional equality to `Seq::<T>::empty()`. The redundant
explicit predicate-equivalence postcondition has been removed; no
cross-state or final writeback obligation has been removed.
`full_value_comparison` proves that the checker's `(left =~= right)` is
equivalent to extensional equality of their full sequence views.
`default_mut_observation` reborrows the result of the independently proved
original constructor. Before this repair, the adapter compiled with
`--no-cheating` and checked four functions: the original constructor, the
general reborrow, the comparison lemma, and the observation wrapper.
The retained `logs/defaults/adapter/` result is for that original adapter,
not the revised real input; the latter's completed verification and
independent review are recorded below.

There are no API inputs to restrict, and the checker quantifies over
arbitrary shared slice observations satisfying the same predicate, a
superset of the possible mutable-return observations. It cannot discard
an element, ordering difference or length difference. The real API still
returns `&mut [T]`; lifetime and exclusive-reference validity are checked
on that real binding and the original mutable source proof. The selected
observation is the initial complete returned value, not allocation
addresses. There is no caller-owned input slice or unreturned region
requiring a writeback relation.

[`defaults.toml`](../proofs/completeness/slice/defaults.toml) keeps the same
unmodified Verus/vstd, host toolchain, observation policy and disabled
assistance as the root configuration. Its snapshot includes the adapter's
source-proof dependency; the root configuration excludes correctness
files. The first missing-dependency run is retained at
`logs/defaults/completeness/default_mut-missing-snapshot-source/` and is
not a checker semantic result. The root configuration was not changed.

For **each original** constructor analysis input, actual `specdet analyze` and
`specdet replay --reexecute` passed with one generated goal and original
query UNSAT. The generated comparison is `(r1 =~= r2)` over the complete
returned slices. The original native queries disable all five search
guards, including `g_neq_tuple`; there is no custom comparison or extra
premise. The replayed harness bytes match the originals.
The checker does not independently test feasibility. Here the two
precondition-free source proofs construct legal outputs for arbitrary
element types; they are also the nonvacuity witnesses, rather than
assuming the candidate or relying on the checker result.

Both original native harnesses were exported to
[`default_shared.rs`](../proofs/completeness/slice/default_shared.rs) and
[`default_mut.rs`](../proofs/completeness/slice/default_mut.rs), with only
relative imports relocated. In that round, the shared export compiled with
one generated goal; the mutable export compiled with one generated goal plus the four
adapter/source functions. Native originals, queries, comparison definitions
and reexecution reports remain under
`proofs/completeness/slice/runs/defaults/`. Exact analyze and replay
commands and their JSON reports are joined in `coverage.tsv` and retained
under `logs/defaults/completeness/`. The current mutable export keeps the
same path; the old verification result does not certify its revised bytes.
The second independent review below verifies the current export.

### Independent review and redundancy repair

The previously blocked independent source/semantic checks and dual-track
reruns completed. Reviewer confirmed the exact zero-argument signatures,
lifetimes and `&[]` / `&mut []` bodies at Rust 1.96
`slice/mod.rs:5631-5647`; each source proof compiled and verified one target.
The `is_empty` proof verified three functions (one target and two imported
lemmas), conditional on existing vstd `len`, not a metadata proof.
Aggregate, default-client and foundation-witness checks verified 2, 10 and
7 functions respectively. Each of the eight original candidates had an
actual deterministic `specdet analyze` result with one goal and original
query UNSAT. The comparisons retained variants, elements and full ordered
slices, with every search guard disabled.

Reviewer justified the mutable observation transfer; direct mutable-return
extraction remains unsupported. The independent checks also reproduced the
pointer-conversion and metadata-call limitations and all four slice-pattern
translation rejections. Those five source proofs remained incomplete then; no Rust
std implementation or documentation defect was found. This describes that
original review; the later endpoint conversions and current results are
recorded above. The persisted review
account is `review.next_action` in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/8b6d043ccde7/round-0001.json`.

Reviewer requested removing only `observe`'s redundant predicate-equivalence
postcondition. Reviewer independently proved the implication from full view
equality (one goal, zero errors) and compiled a temporary reduced adapter
(four functions, zero errors). The real adapter now has that clause removed;
the original `&mut []` body and predicate remain unchanged. Those first-round
independent checks alone did not constitute completed reruns of the revised
real input: its engineering verification and follow-up independent review
were still pending at that handoff.

The revised real target is
`proofs/completeness/slice/inputs/default_mut.rs:default_mut_observation@24`.
Historical commands using `default_mut_observation@25` retain that original
line number. The reduced adapter compiled with `--no-cheating` and verified
four functions with zero errors:
`logs/defaults-redundancy/adapter/verus.log`.
New actual analyze and replay `--reexecute` runs both returned
`deterministic`, original query UNSAT, one checked goal and exit code 0:
`logs/defaults-redundancy/completeness/default_mut/selected/{analyze,replay}.json`.
Their run trees are under
`proofs/completeness/slice/runs/defaults-redundancy/default_mut/`.

An earlier absolute-path selector reached no proof and returned
`target_not_found`; its report remains at
`logs/defaults-redundancy/completeness/default_mut/analyze.json`.
The adjacent `discover.json` records the project-relative file and line 24
used by the successful command. This selection error did not require another
adapter compilation or a contract change.

The current export remains `proofs/completeness/slice/default_mut.rs`.
The single-API command
`python -B scripts/export_completeness.py --defaults default_mut`
updated that export and its coverage entry; the other 330 coverage rows and
seven exported proofs remained unchanged. Two focused mutable-analysis tests
passed, including the current snapshot, generated comparison, disabled search
guards, reexecution, and relocated export checks. The export and test commands
and outputs are retained under `logs/defaults-redundancy/`.
At the close of those engineering checks, the revised mutable adapter still
awaited follow-up independent review; that historical state is superseded
by the completed second round below.
Independent results on unchanged inputs and all old failures, logs and runs
remain retained.

#### Completed second independent review (current)

The authoritative second-round record is
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/8b6d043ccde7/round-0002.json`
(`round: 2`, `review.status: done`). Combined with the first round's source
correspondence and dual-track reruns, it completes independent review for
**both `Default` constructors in full `Seq<T>` value observation**, not
allocation-address determinism. Both constructor rows in `coverage.tsv`
now record `independent_review=done`; their source results remain
`verified` (one target each) and completeness results remain `deterministic`
(one checked goal each).

Reviewer independently compiled and verified the revised real adapter with
`--compile --no-cheating`: four functions, zero errors. The current exported
proof passed `--compile`: five functions, zero errors. Actual analyze of
`proofs/completeness/slice/inputs/default_mut.rs:default_mut_observation@24`
and replay `--reexecute` each verified one deterministic goal with original
query UNSAT. Reviewer confirmed full returned-slice comparison, no added
input premise, all search guards disabled, and snapshots matching the
current source, predicate and configuration.

Two focused mutable tests passed. Reviewer also checked the single-API
export CLI, preservation of the other 330 coverage rows and seven proofs,
the two-constructor default selection, and rejection of invalid names.
Unchanged native behavior tests and the six foundation analyses were not
rerun in round 2. Direct mutable-return extraction remains unsupported;
`len` and the four slice-pattern APIs still lack source proofs. No old
failure, issue, source proof or completeness proof is superseded as
historical evidence, and the full slice module remains incomplete.

### Retained original compilation and behavior checks

All commands below ran during the original constructor integration, before
the redundancy repair:

```sh
python3 -B scripts/export_completeness.py --defaults
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 -B scripts/check_native.py
```

That Python suite passed **37 tests**. Exporting constructor results
preserves the other 329 coverage rows, including all six original results.
The native script preserves the foundation logs, writes this round's
output only under `logs/defaults/native/` and `target/defaults/native/`,
and removes only its generated probe sources and binaries.

The Engineer's Rust 1.96 run passed the seven original observer tests and four lifetime
rejections, plus **seven constructor behavior tests** and **eight rejected
signature/const-call probes**. Constructor tests compile without
`RUSTC_BOOTSTRAP`: zero arguments, exact shared/mutable function return
types, empty values, non-Copy/non-Default and non-static elements, legal
reference lifetimes, non-Copy zero-sized elements, uninhabited elements,
and simultaneous mutable empty borrows. The temporary negative probes
reject extra arguments with E0061, incorrect result types/mutability with
E0308, and both unstable const-trait calls with E0658. Their expectations
come from the original signatures, bodies and stability attributes.
The older observer probes alone still need `RUSTC_BOOTSTRAP=1` for their
standalone copy of core's internal pointer-metadata call.

Reviewer's native runtime rerun stopped because `cc` was missing, before
behavior tests ran. The fourteen successful Rust behavior tests above are
the Engineer's retained results, not independently reproduced runtime results.

The original aggregate compiled successfully; its two obligations are still
the original consistency lemmas. The new public `assume_specification`
bindings are intentionally compiled without `--no-cheating`, unlike the
independent implementation and adapter proofs.
[`tests/default_contract_clients.rs`](../tests/default_contract_clients.rs)
also compiles: five client/witness functions, the original `is_empty`
source function, and four imported instances of the two consistency lemmas.
It checks real fully qualified and type-inferred `Default` calls, both
constructors composed with the proved `is_empty` body, and rejection of a
nonempty slice by the predicate. These ten obligations are supplementary,
not constructor implementation proofs. An initial ill-scoped client
lifetime annotation and its compiler diagnostic remain in
`logs/defaults/clients-lifetime-check/`; the repaired clients infer legal
local lifetimes without adding element trait bounds.

Exact Verus commands and full outputs are in `logs/defaults/aggregate/`,
`correctness/<api>/`, `adapter/`, `clients/`, and `exported/<api>/`, each
with a `command.txt` and `verus.log`. The constructor source proofs each
checked one target function and no imported proof functions. Independent
review subsequently checked those source correspondences, the original
mutable observation transfer, the bounded `is_empty` result and the two
pre-existing limitation reports, as recorded above. Follow-up review of the
revised real mutable adapter is now complete under the second-round record.

## Retained checks for the original observers

The earlier foundation results and their original logs remain available.
The commands run for that six-observer step were:

```sh
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 -B scripts/check_native.py
toolchain/verus-x86-linux/verus tests/readonly_contract_witnesses.rs \
  --crate-type lib --crate-name readonly_contract_witnesses --compile \
  --no-cheating --num-threads 1 --log-all \
  --log-dir logs/foundation/witnesses/verified-queries \
  -o target/foundation/libreadonly_contract_witnesses.rlib
python3 -B scripts/export_completeness.py
```

That Python suite passed **29 tests**: 25 inventory/vstd-mapping tests and four
binding tests. Native Rust **1.96.0** passed **seven behavior tests** and
rejected exactly **four invalid lifetime escapes** with E0515. These cover
empty, singleton, ordered multi-element, zero-sized, non-Copy and non-static
elements, all six const evaluations and exact returned types. The native
command enables `ptr_metadata` with `RUSTC_BOOTSTRAP=1` only because the
standalone copy calls a core-internal unstable operation; it does not change
the canonical source or the Verus baseline. Derived temporary probe source
and binaries were removed by the script.

The Verus witness file compiled and verified **five lawful-input cases plus
the two imported lemmas**, with zero errors. Its positive and negative
assertions rule out empty-only, wrong-constant, wrong-element and
wrong-remainder candidates on those cases. The first witness attempt lacked
sequence extensionality proof steps; its failure is retained in
`logs/foundation/witnesses/verus.log`, and the repaired ghost-only proof is
recorded in `logs/foundation/witnesses/verified.log`. No candidate or view
changed during that repair. These witnesses and native probes do not replace
the missing source proofs.

For a source replay, use the literal per-API command in `coverage.tsv`.
For a checker replay, use its recorded `specdet analyze` command. A relocated
native harness can also be compiled and checked, substituting an API name:

```sh
toolchain/verus-x86-linux/verus proofs/completeness/slice/split_last.rs \
  --crate-type lib --crate-name complete_split_last --compile \
  --num-threads 1 --log-all \
  --log-dir logs/foundation/exported/split_last/queries \
  -o target/foundation/libcomplete_split_last.rlib
```

The unresolved original-observer source work remains metadata and the two
split patterns. The constructor results do not close those APIs; the separate
first/last conversion above covers neither metadata nor a split method.
Independent review of the original inputs and of the revised mutable adapter
is complete within the stated value observation, as recorded above.
No canonical-source or trusted-baseline change has been adopted,
and no external issue has been posted.
