---
title: Conditional completeness theorem and boundary policy
description: Defines the two-execution theorem, admissible boundary observations, and equivalence defaults for the Slice experiment.
---

# Conditional completeness theorem and boundary policy

For one valid input `x` and one genuine dependency observation `b` shared by
both executions, target `T` is conditionally complete when:

```text
Requires_T(x)
and Boundary_T(x, b)
and Spec_T(x, b, y1, s1)
and Spec_T(x, b, y2, s2)
implies Equivalent_T(x, b, y1, s1, y2, s2).
```

The checker negates this implication with the same `x` and `b`. A completeness
claim requires a real `unsat` result. A SAT incompleteness claim requires a
replayable witness satisfying the active contract and fixed boundary; an
opaque relation's diagnostic SAT result is insufficient.

`Boundary_T` may fix only source-used user/external or hidden dependency
observations, such as callback transitions, iterator private state, input
memory/provenance, MaybeUninit initialization, or allocator outcomes. It may
not carry the selected output, aggregate final state, an equivalent answer, or
a complete target execution trace. `Spec_T` must invoke a defined,
source-backed target transition as an exact forwarding call rather than an
uninterpreted functionality relation or a semantically dead occurrence.

Principal returns, reference identities, and final-state observations use
exact equality by default. Binary search may compare distinct `Ok` indices
only when both identify matching duplicates. Unstable sort may disregard only
the order of identities within an equal-key class: exact identity
multiplicities over both results and the position-wise key sequence remain
equal. All other observations remain exact, and selection APIs remain exact
unless separately justified from Rust source and public docs.

## Semantic review invariants

Boundary narrowness is semantic, not syntactic. The public target lacking an
`external_body` attribute does not make its proof boundary narrower. A trusted
callee or proof lemma that supplies the target's complete result relation,
final permutation, aggregate final state, or equivalent postcondition is not
an admissible `Boundary_T` observation; it must be identified as non-narrow
and replaced by source-backed transition semantics before a conditional proof.

The normalized inventory captures the full retained contract and source links
for all 86 `external_body` sites, and all 14 former linkage gaps are resolved.
The fail-closed semantic audit enumerates every selected target/symbol pair and
binds its complete retained contract to a frozen input hash. It rejects 40
answer-bearing sites: 11 complete-target postconditions, 14 complete-branch
postconditions, 9 answer-equivalent results, and 6 opaque whole algorithms.
The remaining 46 sites are individually identified as lower pointer/layout,
raw-slice, subrange, derived-borrow, arithmetic, panic-edge, callback, or
element transitions. Added, removed, or changed sites invalidate the audit
rather than receiving an admissible default.

All 232 dependency-manifest records are likewise enumerated in disjoint,
frozen categories. Linked external-site dispositions propagate to dependency
records. Three dependencies are intrinsically inadmissible: the
answer-equivalent `SliceIndex::get_mut` delegation and the synthetic
null-provenance constructors for `as_mut_ptr` and `as_ptr`. The pointer
constructors ensure the complete public target postconditions rather than
modeling the canonical casts `self as *mut [T] as *mut T` and
`self as *const [T] as *const T`. The resulting target-level partition is 28
admissible boundaries that are narrower than their targets and 34
inadmissible boundaries that must be replaced by lower transition semantics
before a conditional-completeness obligation can be attempted.

Metadata labels and citations do not by themselves establish those semantics.
The checker must reject a declared scalar or relational whole-target oracle,
including a scalar UF over aggregate `Input` and `Boundary`; propagate
boundary-to-output dependencies through helper arguments, global constants,
and `let` bindings; and require `Spec_T` to forward exactly to the target
transition rather than place it in a tautology or other dead expression.

A weak equivalence must encode every observation that remains exact. In
particular, unstable-sort equivalence preserves exact element multiplicities
and the position-wise key sequence while ignoring only identity order within
an equal-key class. Its negative witness substitutes foreign identity 12 with
the same key and must reject it solely because the exact multiset changed.

The structural checker enforces this policy on parsed SMT syntax and
interprocedural dependency flow. It rejects whole-target relations and scalar
answer functions independently of symbol name or whether `Boundary` appears
in their signatures, requires exact metadata coverage for the declared
`Boundary` datatype, and requires every boundary field to be used
non-tautologically by both `Boundary_T` and the target transition. It also
normalizes affine integer addition, subtraction, and constant multiplication
after expanding `let` bindings and defined helpers. Direct, reversed,
`let`-mediated, helper-mediated, global-constant, and algebraically disguised
output laundering is rejected, including nominal input dependencies removed
by `x - x` or zero multiplication. Non-cancelling affine input dependencies
remain accepted. `Spec_T` definitions that omit or semantically discard the
target transition are also rejected.

## Checker soundness requirements

The theorem assertion cannot be reviewed in isolation. Every additional SMT
assertion must either be forbidden or be classified and checked as
source-backed semantics; an unchecked assertion can otherwise force `unsat`,
equate the two outputs, or inject an answer outside `Boundary_T` and `Spec_T`.
The six theorem variables must denote distinct, correctly sorted constants so
that the two executions cannot be collapsed through metadata aliases.

Exact equivalence also requires each principal-observation equality to occur
in a semantically live conjunct. Merely finding the equality syntactically is
insufficient when it is hidden under a branch such as `or true`. Reviewed weak
equivalence must preserve every observation not explicitly relaxed by the
source-backed policy.

The checker rejects extra assertions, dead exact-equality branches, aliased
execution variables, wrongly sorted theorem constants, and all global
constants outside the six typed theorem variables. An answer-bearing value
must therefore be represented by the shared, source/trust-audited `Boundary`
rather than by a fresh global scalar that collapses both executions.

The emitted reference obligation selects datatype-compatible logic `ALL`.
Acceptance executes that exact file with Z3 and requires exit status zero,
exact `unsat` stdout, and empty stderr. These checks remain part of the bounded
authority/design gate and do not classify any target result.

## Review constraints

Algebraic dependency normalization and semantic boundary adjudication are both
required. A clean `unsat` replay cannot repair an answer-bearing boundary, and
a syntactic input tag cannot rescue an expression whose input contribution
cancels. The retained `as_ptr` and `as_mut_ptr` helpers remain blockers until a
faithful source-backed slice-to-thin-pointer cast/provenance transition replaces
their synthetic null-provenance constructors.

## Independent review status

The bounded checker and pointer-audit repair was independently accepted on
2026-08-31 after a fresh ten-command acceptance run and additional cancellation
probes. The review confirmed the 28/34 boundary partition, the two pointer
blockers, and result-neutral `not-run` status for all 62 targets. This review
does not advance the Manager-owned stage or classify any target obligation.

The separately reviewed target-029 increment established
`core::slice::binary_search_by` as conditionally incomplete both for exact
output and modulo matching-index equivalence. Its certified evidence remains
immutable while later target runners execute.

## Target 079 key adapter lifecycle

For `select_nth_unstable_by_key`, `f(a).lt(&f(b))` evaluates the two `FnMut`
calls left-to-right and then invokes `PartialOrd::lt` on references to both
owned key temporaries. On normal completion, the right key is destroyed
before the left key. A second-key panic cleans up only the left key; an `lt`
panic cleans up right then left. Key destructors may have callback-visible
effects and may panic. A destructor panic during an existing unwind causes
immediate non-unwinding process termination, so abort must remain distinct
from an ordinary callback panic and must not trigger modeled outer guard
restoration.

The target-079 boundary may therefore contain total functional key, `lt`, and
source-justified hidden `Drop` result/state/panic observations. Which calls
occur, temporary liveness, destruction order, selection branches and
mutations, and all outputs/final state remain source-derived and may not be
placed in the shared boundary.

## Additive operational-v2 reconciliation

The operational-v2 crosswalk derives the independently certified 62-row
campaign without changing any certified row. It overlays only input orders
078 and 079 through their separately accepted operational-v1 addenda and
direct arbitrary-domain evidence. Both overlays require a clean UNSAT
exact-output obligation, a clean UNSAT exact reviewed-equivalence obligation,
a SAT nonvacuity replay, a source-complete classification-eligible result, and
clean Verus typecheck and verification captures.

The resulting effective counts are 50 conditional-complete, 12
conditional-incomplete, and zero missing for exact output; and 43
conditional-complete, 19 conditional-incomplete, and zero missing modulo
reviewed equivalence. The certified campaign, both accepted operational-v1
packages and addenda, all prior reviews, and `research/PIPELINE_STATE.json`
remain byte-locked.

Independent review accepted the operational-v2 reconciliation on 2026-09-01
and recorded the decision in
`review/REVIEW_OPERATIONAL_V2_RECONCILIATION_ACCEPTANCE.md`. Fresh review
forced Python compilation, passed all 13 focused reconciliation tests, ran
both target runners, directly replayed four classifying UNSAT obligations and
two SAT nonvacuity obligations, verified both trusted-free Verus models, and
passed all 553 unit tests and all 47 task-native acceptance commands. Direct
pre/post byte comparison found no membership or content change across the
protected certified campaign, accepted operational packages and addenda,
prior reviews, or Manager-owned state. This bounded acceptance does not
authorize a Manager-owned stage transition.

### Certified operational-v2 projection

The certification closure is additive. It leaves the accepted operational-v2
crosswalk, reconciliation manifest, JSON and Markdown dossiers, independent
review, prior accepted packages, frozen inputs, and
`research/PIPELINE_STATE.json` byte-identical. The certified projection binds
those reviewed bytes and carries a 62-row identity/classification projection;
it does not rewrite the pre-review status inside the accepted source package.

The certified status is valid only when the bounded review is one unambiguous
`ACCEPT` for operational-v2, reports overlays 078 and 079, and reports exact
counts 50/12/0 and reviewed-equivalence counts 43/19/0. Missing, malformed,
non-ACCEPT, wrong-scope, or count-inconsistent review text fails closed.
Artifact-byte drift, target/order/contract or row drift, count drift, any
pending status in the certified projection, and mutation of the inherited or
newly protected files also fail closed. Manager-owned stage transition remains
disabled.

The review grammar must also make the count-bearing acceptance summary
unambiguous. A 2026-09-01 L2 negative probe showed that validating only the
first match accepted an appended second summary with conflicting row and
classification counts. `_parse_accept_review` now enumerates canonical
count-bearing summaries and requires exactly one before validating its scope
and counts. Focused regression coverage rejects both an appended duplicate
canonical summary and an appended conflicting count-bearing summary.

Independent review on 2026-09-02 confirmed the repaired parser with a positive
control and both required negative probes. A clean five-command replay passed
Python compilation, 17 focused tests, 571 complete tests, the 62-row closure
with exact counts 50/12/0 and reviewed-equivalence counts 43/19/0, and all 49
task-native acceptance commands. Direct pre/post byte comparison found
identical membership and content for all 707 protected files, including
`research/PIPELINE_STATE.json`; independent row comparison found no
classification changes. This bounded parser certification does not authorize a
Manager-owned stage transition.

### Versioned path-level preservation

`preservation/path_policy_v1.json` is the shared preservation authority for
final-campaign validation, operational-v2 reconciliation and certification,
and the target-079 operational replay. It binds the accepted final-campaign
baseline and operational-v2 inventories without rewriting them. The 45
historical operational-v2 review paths are taken exactly from the accepted
reconciliation manifest; the separately certified operational-v2 review is
bound through the certified projection.

Post-certification exclusions are path-level registrations. Version 1 lists
all 142 target-078 adapter-refinement files with their individual byte
identities and the accepted target-079 adapter review. The target-078 scope
and the complete allowed review scope are closed sets: mutation, deletion,
substitution, duplicate or noncanonical paths, and unregistered files fail
validation. Target-079 computes its historical review digest over the explicit
45-path inventory; filename fragments and whole-directory exclusion digests
do not define membership.

Independent L2 review on 2026-09-02 accepted this preservation repair after
fresh Python compilation, all 10 focused policy tests, a separate same-size
file-mutation probe, 17 operational-v2 certification tests, all 625 repository
tests, and all 51 task-native acceptance commands passed. Target-078 replayed
with 11 verified obligations and zero errors; adapter correspondence and both
classification obligations were UNSAT, nonvacuity was SAT, and all semantic
and correspondence mutation probes retained their expected outcomes. A direct
pre/post content snapshot found identical membership and bytes for 8,155 files
across the evidence, frozen-authority, review, crosswalk, and Manager-owned
state scopes. This bounded acceptance does not authorize a Manager-owned stage
transition.

## Target 013: `core::slice::as_chunks_mut`

The target-013 checker binds active contract SHA
`669f8bbc7a27aa64da763386dccd397f1d7e81db22ef7b672e71a40b69ff5e7c`
and rejects retained two-conjunct SHA
`8c6cc8f88b4de3b1f2c2c1a25965e3744c851cf8ac05d251cc0effd85d0f590e`.
Its arbitrary-length source/range model expands all ten active partition,
initial length/subrange, final length, final-frame, and final-subrange
conjuncts. Reference identity is structural: allocation, parent borrow,
subrange, element width, and projection kind. The shared boundary merely
confirms the allocation and mutable-borrow identity already present in the
input; it carries no returned reference, chunk/remainder value, final state,
answer encoding, or trace.

The full exact-return/reference/final-state theorem is `sat`. A fixed
`N = 2`, length-3 replay gives both executions the same source-derived return
but different final contents; every active contract conjunct holds in each
execution. Thus completeness modulo the exact reviewed equivalence is
`conditional-incomplete`. The exact-output projection retains the complete
final contract existentially and is `unsat`, so exact output is
`conditional-complete`. The experiment-local source-shaped Verus instance for
that representative verifies with 8 verified and 0 errors, using only the
audited TS-013 lower transitions plus explicit immutable slice-length facts.

These target-013 classifications were independently accepted on 2026-08-31
after a fresh 12-command acceptance run, including 77 passing tests, clean
solver replays, and 8 verified Verus obligations with 0 errors. Target 029
remains unchanged and the other 60 selected rows remain `not-run`.

## Target 106: `core::slice::splitn_mut`

The target-106 constructor model follows the Rust source chain
`split_mut -> SplitMut::new -> SplitNMut::new`. It derives the returned
iterator's full source and remaining ranges, empty yielded prefix and
remainder, mutable allocation/borrow identity, stored predicate identity and
state, `finished=false`, zero callback calls, `count=n`, and `reverse=false`.
The slice and callback final-state observations remain unchanged.

Its shared boundary contains only the input allocation, mutable-borrow, and
predicate identities. It excludes the returned iterator or view, selected
ranges, predicate results, callback transitions, private iterator state, final
state, and traces. Thus the boundary is strictly narrower than the target.
The generated predicate-observation clause is retained only as its classical
totality formula; it does not introduce a constructor-time callback
observation.

The target-specific exact-output and full exact-state theorem negations both
return `unsat`, establishing
`conditional-complete` for exact-output determinism and
`conditional-complete` modulo the reviewed exact equivalence.

These target-106 classifications were independently accepted on 2026-08-31
after a fresh 13-command acceptance run. The run compiled the experiment,
executed 93 passing tests, replayed all three target pipelines and every solver
obligation, passed local validation, and verified the target-106 constructor
model with 5 verified obligations and 0 errors. Independent boundary probes
also covered empty and invalid domains, all 29 exact observations, constructor
defaults, identity mismatches, and theorem argument ordering. Targets 013 and
029 retain their accepted classifications, and the other 59 selected rows
remain `not-run`.

## Target 081: `core::slice::sort_unstable_by`

The bounded target-081 model uses three distinct element identities and expands
both active contract conjuncts: exact input/final multiplicity and all six
length-three comparator-sortedness observations. Its shared boundary contains
only the three input identities, a finite 3-by-3 comparator result table, and a
state-preserving callback transition delta. It excludes, rather than relabels,
the retained answer-bearing sites `TS-081-D002`, `TS-081-D003`, and
`TS-081-E001`; no final sequence, chosen permutation/order, pivot/swap decision,
answer encoding, or complete comparison trace enters the boundary.

Reviewed equivalence keeps unit return and callback final state exact, requires
exact identity multiplicities over both final sequences, and permits a
position-wise identity difference only when the shared comparator reports
`Equal` in both directions. The exact-final-slice obligation has an equal-key
reordering witness. The general obligation has a fixed-boundary non-total
comparator witness that reports each of two identities as `Less` than the
other, making both permutations contract-sorted but not comparator-equivalent.
A separate total-order restriction eliminates that witness and makes reviewed
equivalence unique. These are bounded active-contract results, not a recursive
verification of the private ipnsort implementation.

An independent Reviewer accepted this bounded increment on 2026-08-31 after a
fresh 14-command acceptance run. The run compiled the Python tools, executed
106 passing tests, replayed the three target obligations, passed local
validation, and verified the target model with 3 verified obligations and 0
errors. Independent content comparison preserved targets 013, 029, and 106
byte-for-byte; exhaustive enumeration of 13 total-order profiles and 66
contract-sorted result pairs confirmed the separate sanity result. Target 081
is `conditional-incomplete` in both result columns, and 58 rows remain
`not-run`.

## Target 022: `core::slice::as_ptr_range`

The target-specific model replaces the retained synthetic
null-provenance/length-address start pointer and answer-equivalent range-end
helper. Its boundary contains only the concrete input slice's allocation
identity and bounds, start address and provenance, element size and alignment,
and target-platform isize/address limits. It excludes both returned endpoints,
the range, final state, target truth, answer encodings, and execution traces.

The source transition expands `self as *const [T] as *const T` by retaining the
input allocation, address, and provenance. It expands
`start.add(self.len())` as mathematical `len * size_of::<T>()` byte arithmetic,
with isize-fit and no-wrap requirements. The start address is always non-null
and aligned; allocation provenance and an in-allocation range permitting the
one-past endpoint are required only for nonzero byte offsets. Both endpoints
and every modeled final-state observation are compared exactly.

The exact-output and full exact-state theorem negations both return `unsat`,
and the experiment-local Verus source-transition model verifies both
conclusions without `external_body`. SAT probes cover allocated empty/nonempty
cases and no-allocation/no-provenance dangling empty and nonempty-ZST cases.
UNSAT rejection probes cover a null slice address and nonzero offsets without
allocation or provenance.

These target-022 classifications were independently accepted on 2026-08-31
after a fresh 15-command acceptance run. The run compiled the experiment,
executed 123 passing tests, replayed both obligations and all eight domain
probes, passed local validation, and verified 2 Verus obligations with 0
errors. Targets 013, 029, 081, and 106 remained byte-identical, and 57 selected
rows remain `not-run`.

## Target 120: `core::slice::write_copy_of_slice`

The target-120 replacement excludes the mixed aggregate dependency
`TS-120-D004` and answer-equivalent storage-effect lemma `TS-120-E005`.
Its shared boundary contains only initial source storage, destination
`Uninitialized | Initialized(value)` cells, source/destination
memory-provenance and allocation facts, destination borrow identity, element
layout, platform limits, and a pre-existing outside-frame token. It contains
no resulting storage, returned reference, answer encoding, or trace.

The source transition follows Rust 1.96's same-layout transmute,
equal-length `copy_from_slice`, `copy_nonoverlapping`, and `assume_init_mut`
path. Raw copying is modeled pointwise by mapping the `Initialized`
constructor over every source value. An uninitialized destination cell has no
value projection, so the transition never reads an uninitialized value.
Destination identity and length, source storage and identity, returned
reference identity, layout/provenance, and the outside frame are all explicit.

Both exact-output and full exact-state theorem negations replay as clean
`unsat`. SAT probes cover empty, wholly uninitialized, mixed-initialization,
and fully initialized destinations. UNSAT probes reject unequal lengths,
no-op and partial copies, omitted initialization, wrong destination or return
identity, source mutation, and frame mutation. The experiment-local Verus
model proves the per-slot copy lemma and both determinism theorems without an
`external_body`.

An independent Reviewer accepted this increment on 2026-08-31 after a fresh
16-command acceptance run. Python compilation succeeded, 140 tests passed,
both theorem obligations and all 12 domain/rejection probes replayed with
their expected solver results, and Verus reported 3 verified obligations with
0 errors. Targets 013, 022, 029, 081, and 106 were preserved byte-for-byte,
and 56 selected rows remain `not-run`.

## Target 051: `core::slice::get_disjoint_mut`

The bounded target-051 model covers two `usize` indices into a length-three
non-ZST slice. It replaces retained answer-bearing sites `TS-051-D002`,
`TS-051-D004`, `TS-051-E001`, and `TS-051-E002` with the Rust 1.96 validation
loop and per-slot unchecked-borrow construction semantics. The validation
model checks each index in order and then overlap; the construction model
derives receiver allocation, address, provenance, parent borrow, and value for
each initialized result slot while preserving the first slot across the
second write.

`Spec_T` remains the active generated contract relation. It fixes the Result
tag from source-backed validity and enforces the Rust type invariant that an
`Ok` payload contains two well-formed, disjoint receiver borrows, but it does
not inject the implementation-selected error variant or exact borrow array.
The shared boundary contains only initial slice values, memory/provenance,
mutable-borrow identity, element layout/platform limits, and an outside-frame
token. It contains no validity bit, error kind, returned borrow, alias map,
resulting state, deterministic choice, or trace.

Both exact-output and full exact-state theorem negations are `sat`. One fixed
out-of-bounds input admits both error variants with the same unchanged final
state. One fixed valid-disjoint input admits the canonical `[0, 2]` borrow
array and a distinct well-formed `[1, 2]` borrow array with the same final
state. Thus both result columns are `conditional-incomplete` for this bounded
active-contract model.

An independent Reviewer accepted this increment on 2026-08-31 after the full
17-command acceptance run completed, 152 tests passed, both fixed witnesses
and all target-local probes replayed with their expected solver results, and
the source model verified 5 obligations with 0 errors. Direct content
comparisons bound the active contract and source inputs and found the other six
accepted target evidence trees unchanged. Exactly seven selected rows are now
classified and 55 remain `not-run`.

## Target 052: `core::slice::get_disjoint_unchecked_mut`

The bounded target-052 model fixes `N = 2`, `usize` indices `[0, 2]`, and a
length-three non-ZST receiver. It replaces answer-bearing retained sites
`TS-052-D004` and `TS-052-E001` with the Rust 1.96 transitions for identity
cloning of each `usize`, in-bounds `get_unchecked_mut` resolution, two
MaybeUninit slot writes, preservation of the first slot across the second
write, complete initialization, and `assume_init` only after both writes.

The shared boundary contains only initial receiver values, allocation,
address, provenance, mutable-borrow identity, element layout/platform limits,
and an outside-frame token. It excludes validity bits, returned references,
MaybeUninit results, alias maps, canonical answers, final state, and execution
traces. `Spec_T` is the active generated unsafe precondition and final-length
postcondition plus Rust return-array/reference well-formedness and
disjointness; it does not inject the source-canonical returned references or
the final state.

Both exact-output and full exact-state theorem negations are `sat`. Under the
same valid input and fixed boundary, one execution returns the canonical
well-formed disjoint array `[0, 2]` and the other returns the distinct
well-formed disjoint array `[1, 2]`; both retain the same final state and
satisfy the active contract. Thus both result columns are
`conditional-incomplete` for this bounded active-contract model.

## Slice pointer-cast cluster

For `as_mut_ptr` and `as_ptr`, the source-backed target transition is the
canonical slice-to-thin-pointer cast. It retains the input allocation, address,
and provenance. The synthetic retained constructors that use the slice length
as an address and null provenance are excluded rather than reclassified.
The valid-input domain requires the slice address to be non-null and aligned
to the element alignment, including for empty slices and zero-sized types.

`as_mut_ptr_range` composes the source-backed `as_mut_ptr` transition with
mutable `ptr::add`. The add transition uses mathematical
`len * size_of::<T>()` byte arithmetic, requires isize fit and no address wrap,
and preserves allocation and provenance. A nonzero offset additionally
requires allocation provenance and a range that stays in allocation through
the one-past endpoint. A zero-byte offset supports empty slices and ZSTs,
including non-null aligned dangling pointers.

The shared boundary contains only initial memory and provenance, element and
platform layout, and mutable identity/frame observations where applicable. It
contains no returned pointer or range, endpoint, final state, target truth,
answer encoding, or execution trace. Pointer components and every modeled
final-state observation use exact equality.

### Independent review acceptance

The repaired cluster was independently accepted on 2026-08-31. Fresh
acceptance executed 22 commands and 182 tests, replayed all six exact-output
and full exact-state obligations as clean UNSAT, and obtained the expected 15
SAT domain probes and 24 UNSAT rejection guards. Each experiment-local Verus
model type-checked and reported `3 verified, 0 errors` without
`external_body`.

The accepted repair binds target-019 and target-021 boundary fields to
explicit canonical-source replacement identities instead of the excluded
synthetic sites. It also provides the self-contained ordered
019 -> 021 -> 020 cluster replay and rejects the concrete misaligned
address-1026/alignment-4 input in every model. Direct before/after byte
comparison preserved all eight previously certified evidence trees. The
crosswalk therefore records all three targets as `conditional-complete` in
both result columns, leaving 11 classified and 51 `not-run` rows. This bounded
acceptance does not authorize a Manager-owned stage transition.

## Search-wrapper cluster

The bounded length-two models for target 028 `binary_search`, target 030
`binary_search_by_key`, and target 065 `partition_point` replace their retained
answer-bearing delegations and result bridges with defined source-backed
wrapper transitions. Each model composes the accepted `binary_search_by`
relation with the wrapper-specific adapter: `Ord::cmp`, key extraction followed
by `Ord::cmp`, or predicate-to-Ordering conversion followed by
`unwrap_or_else(|i| i)`. Frozen provenance remains unchanged.

Their shared boundaries contain only source element reads, per-element
comparison/key/predicate observations, and callback state-transition deltas.
They contain no selected index, returned `Result`, aggregate callback final
state, answer encoding, or execution trace. `Requires_T` fixes only length two;
orderedness and partitioning occur solely in separate sanity obligations.

For targets 028 and 030, Result tags, Err indices, and callback final state are
exact under reviewed equivalence. Distinct Ok indices are equivalent only when
both identify matching duplicates. Their unrestricted obligations are SAT on
descending observations, ordered-domain sanity is UNSAT, and exact-output
determinism is SAT on duplicate matches. Target 065 keeps exact index and
callback-state equivalence: both general and exact-output obligations are SAT
on `[false, true]`, while partitioned-domain sanity is UNSAT.

All six SAT classifications have concrete fixed-boundary SMT models and
independent contract replays. The three experiment-local Verus models verify
with `3 verified, 0 errors` each and contain no `external_body`. The fresh
26-command acceptance run compiled the tools, passed 198 tests, replayed every
solver and Verus artifact, preserved all 11 previously certified evidence
trees by direct content comparison, and left 14 classified rows with 48
`not-run`.

Independent review found a source-composition conflict in targets 028 and 030.
Their canonical wrappers call `binary_search_by` unconditionally, but both the
SMT and Verus wrapper relations require the accepted lower relation only when
the upper slice/key sortedness predicate holds. Upper sortedness can be false
while the derived comparator profile is ordered. Concrete length-two probes
for both targets then satisfy `Spec_T` while violating the reviewed lower
relation. The fixed SAT witnesses use unordered lower profiles and therefore
remain plausible, but the target transitions are not yet faithful over their
full modeled domain. The candidate classifications remain uncertified pending
unconditional lower-relation composition, a regression for this branch, fresh
evidence generation, and independent re-review. No stage transition is
authorized.

## Strengthened chunk-contract cluster

Targets 014 `as_chunks_unchecked` and 015
`as_chunks_unchecked_mut` are the lower transitions for targets 012
`as_chunks`, 023 `as_rchunks`, and 024 `as_rchunks_mut`. All five models bind
the active strengthened contract rather than the retained weaker contract.
The unchecked transitions compose the accepted target-021 `as_ptr` or
target-019 `as_mut_ptr` cast semantics, preserve allocation/address/provenance
through the array-pointer cast, and apply explicit raw-slice domain and view
construction semantics. Target 015 excludes and replaces the answer-bearing
`TS-015-D006` and `TS-015-E002` contracts; neither is admitted into the new
boundary.

The upper transitions explicitly compute quotient and remainder and then
compose the appropriate unchecked lower transition. Target 012 uses front
chunks and a rear remainder. Targets 023 and 024 use a front remainder and
rear chunks. Their active-contract translations separately retain each
length, partition, initial subrange, mutable final-length, final-frame, and
final-subrange conjunct.

The shared boundary contains only initial allocation, address, provenance,
element layout, allocation extent, platform limits, borrow identity, and a
mutable frame identity where applicable. It excludes returned references,
front/rear ranges, final storage and views, answer encodings, and traces.
Real Z3 results are UNSAT for both obligations on immutable targets 012, 014,
and 023. Mutable targets 015 and 024 are UNSAT for exact-output determinism
and SAT for full exact output/state: fixed-input, fixed-boundary witnesses
independently replay every active conjunct while varying only legal final
contents reached through the returned mutable views.

The ordered 014 -> 015 -> 012 -> 023 -> 024 replay also covers positive empty
and ZST cases and rejects N=0, invalid lower divisibility, null or misaligned
pointers, changed provenance, isize overflow, and swapped front/rear
partitions. All five experiment-local Verus models type-check and verify with
zero errors and contain no `external_body`.

This five-target increment was independently accepted on 2026-08-31. The
Reviewer-owned acceptance run compiled the experiment, completed all 27
commands, and ran 214 passing tests. Direct Z3 replay confirmed UNSAT for all
five exact-output obligations and the three immutable full obligations, plus
SAT with concrete fixed-boundary replays for the two mutable full obligations.
An additional 205 adversarial checks covered conjunct and equality omission,
lower-transition removal, source-derived partition orientation, pointer
provenance, invalid domains, empty slices, and ZST slices. Direct recursive
content comparison preserved all 14 earlier certified evidence trees, leaving
19 classified and 43 `not-run` rows. This bounded acceptance does not authorize
a Manager-owned stage transition.

## MaybeUninit lifecycle cluster

Targets 026 `assume_init_mut`, 119 `write_clone_of_slice`, and 025
`assume_init_drop` form an ordered lifecycle cluster. Target 026 supplies a
layout-preserving mutable-slice cast that retains allocation, address,
provenance, unique-borrow identity, length, and initialized values. Target 119
composes this lower transition only after deriving the equal-length
source-ordered Clone/write loop. Target 025 independently expands its empty
check, raw slice cast, compiler drop glue, and element-wise Destruct
composition.

The target-025 and target-026 models exclude retained answer-bearing sites
`TS-025-D002`, `TS-025-E001`, `TS-026-D002`, and `TS-026-E001`; fresh
source-backed transition definitions replace them. Target 119 admits retained
Clone/write sites only for one lower element transition. Its aggregate write
order, write count, initialized storage, final callback state, and returned
reference are source-derived rather than trusted.

Lifecycle boundaries contain initial storage and initialization, memory
layout/address/provenance, mutable-borrow and frame identity, plus individual
Clone or Destruct results/outcomes/state transitions keyed by source index.
They do not contain a returned reference, aggregate resulting storage, a
standalone final callback state, operation order/count, an answer encoding, or
a full trace. Recursive SMT helper definitions compose arbitrary-length
per-call observations; the checker treats `define-fun-rec` definitions under
the same reachability, role, and principal-observation rules as ordinary
defined helpers.

Target 025 represents a dropped logical slot as `Uninitialized` with no
readable value payload. Its exact-output and full exact-state theorem
negations are UNSAT. Target 119's normal-return path similarly produces UNSAT
for both obligations because each successful Clone result must satisfy the
active written-from relation and target 026 preserves the derived initialized
storage identity. Panic probes at Clone indices 0, 1, and 2 derive the Guard
counter, successful prefix writes, and same-order Destruct cleanup; malformed
partial, duplicate, out-of-order, or post-panic operations are rejected.

Target 026's exact-output theorem is UNSAT, but its full exact-state theorem is
SAT. A fixed input and boundary return the same unique mutable reference and
the same initial values in both executions, while distinct in-range writes
through that reference produce different final storage and final returned
views. Both executions satisfy every active contract conjunct, so the result
is exact-output `conditional-complete` and full-exact
`conditional-incomplete`. Targets 025 and 119 are
`conditional-complete` for both reported obligations.

### Independent review status

Independent review accepted the repaired lifecycle cluster on 2026-08-31.
The delivered-state reset is target-local, the per-step index helpers and
panic paths are reachable from the classified relations, all 233 tests pass,
and all three Verus models verify with zero errors. The accepted result leaves
22 classified and 40 `not-run` rows.

## Targets 080 and 082: Ord-backed unstable-sort companions

Targets 080 `sort_unstable` and 082 `sort_unstable_by_key` use their active
contracts and do not inherit target 081's non-total comparator
classification. Both target signatures carry an `Ord` bound, Rust's public
docs define that bound as a total order, and the generated vocabulary supplies
reflexive, dual, total, and transitive Ord-observation laws.

The target-specific replacement boundaries admit only `TS-080-D003` for
extensional Ord observations and `TS-082-D004` for extensional key extraction
and key-Ord observations. They exclude `TS-080-D002`, `TS-080-E001`,
`TS-082-D002`, `TS-082-D003`, and `TS-082-E001`. No final sequence,
permutation, selected order, aggregate final state, pivot/swap choice, or
complete callback/target trace enters the boundary.

The completeness obligations quantify arbitrary nonnegative slice length,
identity multiplicities, and a valid observation position when nonempty; an
empty result has no position at which two sequences can differ. Exact
permutation and sortedness give an order-statistic interval for the class at
that position; total-order separation makes two different classes impossible.
Both general negated theorems are therefore UNSAT. Separate length-three UNSAT
obligations are sanity evidence only.

Exact final-slice determinism remains SAT for each target: two distinct
identities in one equal Ord/key class may swap while unit return, exact
identity multiplicities, callback final state, and all non-tie class
observations remain exact. Negative witnesses reject foreign identities,
unequal-class reorderings, and callback/key-state drift. The resulting
classifications are exact-output `conditional-incomplete` and
completeness modulo reviewed equal-class equivalence `conditional-complete`
for both targets.

Independent review accepted this bounded increment on 2026-08-31. Fresh
execution replayed both general obligations as UNSAT and both exact witnesses
as SAT, verified both Verus models with three verified obligations and zero
errors, ran 18 targeted and 251 full tests, and passed all 29 acceptance
commands. Direct byte comparison preserved all 22 previously certified
evidence trees and every frozen selection artifact for rows 077-079. The
accepted ledger has 24 classified and 38 `not-run` rows.

## Target 077: `select_nth_unstable`

Target 077 excludes retained answer-bearing dependency `TS-077-D002` and
opaque whole-algorithm body `TS-077-E001`; it does not relabel either as an
admissible boundary. `TS-077-D001` and `TS-077-C001` remain context-only.
Only the extensional `Ord` implementation and equivalence-class observations
from `TS-077-D003` enter `Boundary_T`. The boundary contains no pivot,
selected permutation, returned subslice, aggregate final state, answer
encoding, pivot/swap choice, or complete comparison/execution trace.

The accepted relation names valid-index, ZST, minimum/maximum scan, swap,
partition, recursive introselect/fallback, and final returned-subslice
transitions from core/src/slice/sort/select.rs:17-307 and the lower partition
operation at core/src/slice/sort/unstable/quicksort.rs:93-137. Identity
multiplicity is recursively counted from each modeled sequence. Input class,
less, equal, and greater counts are recursively derived from the initial
sequence and shared `Ord` class observation. Final identity and side-class
summaries are likewise derived from the concrete final sequence. The
introselect relation now carries strictly shrinking source windows through at
most 16 main-loop narrowings and a well-founded fallback path; small-window,
minimum, maximum, and pivot-hit terminals constrain the concrete final
sequence rather than selecting a fresh unconstrained branch tag.

The reviewed selection equivalence is justified by the public docs at
core/src/slice/mod.rs:3461-3513. It preserves returned range identities and
lengths, exact whole-input identity multiplicities, pivot rank and `Ord`
class, left/right class multiplicities, allocation and mutable-borrow
identity, and final length. It relaxes only ordering within the two documented
unsorted sides and pivot identity among equal-class elements.

The fixed-input/fixed-boundary exact witness is a concrete active-contract
witness for non-deterministic exact output. The repaired arbitrary-length
obligation returns real `unsat`. Fixed-input/fixed-boundary regressions make
both the foreign-identity sequence with stale input multiplicity and the
partition-crossing sequence with stale expected side-class counts `unsat`; a
same-input/shared-boundary rank-summary uniqueness probe is also `unsat`. A
small-sort reachability probe changes from `unsat` to `sat` only when the
recursive/fallback transition is removed, showing that the source-path
relation has semantic force.

Independent review accepted this bounded increment on 2026-08-31. Fresh
execution compiled the Python tools, ran 17 targeted and 268 full tests,
verified five Verus obligations with zero errors, and passed all 30 acceptance
commands. Independent contract replay and 16,739 exhaustively enumerated
finite class domains through length five confirmed the positive and negative
equivalence cases. Direct content comparison preserved all 24 certified
evidence trees, every frozen selection input for rows 077-079, and every
non-result crosswalk field. Target 077 is exact-output
`conditional-incomplete` and completeness modulo reviewed selection
equivalence `conditional-complete`; the ledger has 25 classified and 37
`not-run` rows.

## Targets 078-079: callback-driven selection

Targets 078 `select_nth_unstable_by` and 079
`select_nth_unstable_by_key` exclude retained closure adapters D002,
whole-selection dependencies D003, and opaque external bodies E001.
Their D001 specification vocabulary and C001 source closure remain
context-only. Only D004 supplies genuine callback observations.

The shared boundary contains callback identity, initial callback-visible
state, and functional source-step observations over arguments, result, next
state, and panic. It excludes a realized invocation trace or count, pivot, permutation,
returned range, final callback state, final slice, and every answer encoding.
Target 078 models each adapter invocation as exactly one `compare(a,b)` call
followed by equality with `Ordering::Less`; it does not assume comparator
totality. Target 079 models `f(a)`, then `f(b)`, then `Ord::lt`, threading the
intermediate states and permitting different keys on different invocations.

The current obligations keep all six generated contract conjuncts explicit
and retain exact returned-reference, final-slice, allocation/borrow, panic,
and callback-state equivalence for both targets. They are deliberately
bounded to a non-ZST length-four, index-one execution and are not presented as
arbitrary-length target proofs.

The bounded transition follows canonical
`insertion_sort_shift_left(v, 1, is_less)`: it executes tails one, two, and
three, derives every comparison argument/result from `insert_tail`, threads
each intermediate callback state, and rotates the mutable sequence at the
source-derived insertion position. The frozen helper excerpt now includes
the loop advance and the `CopyOnDrop` definition/`Drop` implementation.
Source-coupled panic probes use those same adapter and rotation definitions,
including an unchanged slice on the first comparison and gap-guard
restoration after a later comparison prefix; a paired negative regression
rejects the unrestored slice.

The two bounded theorem negations are `unsat`, while explicit nonvacuity and
source-required all-equal length-four executions are `sat`. Permanent
regressions reject one- and two-adapter all-equal executions and accept the
canonical three-adapter execution. Descending and mixed inputs additionally
exercise the shift loop; two more tail-three cases cover the remaining
rotations. Each rejects any final sequence or callback state other than the
source-derived result.

The bounded obligation models the callback closure adapter associated with
D002. D003 and E001 remain excluded and unresolved because no operational
relation derives arbitrary-length `choose_pivot`, lower partition mutation
and callbacks, ancestor-pivot handling, introselect narrowing, the 16-step
median-of-medians fallback, or their panic/unwind behavior. A realized
schedule remains forbidden in `Boundary_T`, but it must be derived internally
before either completeness theorem can classify the full target. Both result
columns are therefore `missing-source-backed-model`, not
`boundary-insufficient`. Target 079 additionally leaves temporary key `Drop`
order, callback-visible state, and panic unmodeled.

### Independent review status

The round-two `boundary-insufficient` candidate was independently rejected on
2026-09-01 because its arbitrary-length trace was disconnected and its full
acceptance run failed. The accepted replacement removes those general source
claims, extends both Verus files to five bounded length-four all-equal
schedule obligations, and repairs the downstream preservation fixtures.

Independent review accepted the evidence-backed
`missing-source-backed-model` classification on 2026-09-01. Fresh execution
compiled the tools, passed 19 targeted and 287 full tests, verified both Verus
files with five verified obligations and zero errors, replayed the solver
campaign, and passed all 31 acceptance commands. Independent SAT probes
confirmed that the comparator need not be total and that key extraction may
vary by callback state. Direct pre/post content comparison preserved all 25
certified evidence trees, all three frozen selection inputs, every non-result
crosswalk field, and every out-of-scope row. The accepted ledger has 27
classified and 35 `not-run` rows.

This acceptance certifies the missing-model diagnosis, not full-target
conditional completeness or incompleteness. The bounded UNSAT results remain
source-faithfulness regressions only. Stage transition remains disabled.

## Mutable iterator constructor cluster

Input orders 032 `chunk_by_mut`, 036 `chunks_mut`, 069 `rchunks_mut`, 074
`rsplit_mut`, 076 `rsplitn_mut`, 093 `split_inclusive_mut`, and 098
`split_mut` use arbitrary-valid-length source constructor transitions.
`chunk_by_mut` stores its mutable slice and adjacent predicate without calling
the predicate. The chunk constructors preserve the input raw-slice address,
length, allocation, provenance, mutable-borrow marker, and element size while
storing a positive chunk size and the source direction. The predicate-split
constructors preserve the mutable slice and callable state, perform zero
constructor-time callback calls, and derive their exact reverse, inclusive,
count, and finished defaults from the canonical private constructors.

The boundary contains only input address/allocation/provenance/borrow/layout
and callable identity. Returned views and private iterator fields, callback
results, immediate final state, answer encodings, and traces are excluded.
Every output and final-state observation uses exact equality. Both theorem
projections are UNSAT for all seven targets; empty, nonempty, and nonempty-ZST
source instances are SAT, and all seven target-local Verus models verify
without `external_body`.

Frozen trust record `TS-076-C003` remains unchanged at its retained
`iter.rs:1223-1225` citation. A derived experiment-local reconciliation binds
the same `RSplitNMut::new` body in the assigned canonical Rust 1.96 tree at
`iter.rs:1289-1293`; no frozen provenance was rewritten.

The delivered candidate records both columns as `conditional-complete` for
all seven rows, preserves the 27 certified evidence trees and seven frozen
input trees, and leaves a 34-classified/28-not-run ledger.

### Independent review status

The first independent review on 2026-09-01 required changes. Fresh execution
compiled the Python tools, ran 17 targeted and 304 full tests, verified all
seven Verus files with two verified obligations and zero errors each,
replayed 14 UNSAT theorems and 21 SAT source instances, and passed all 32
acceptance commands. Readable content comparison also preserved the 27
predecessor evidence trees and seven frozen input trees.

The second independent review accepted the repaired cluster on 2026-09-01.
Permanent canonical-source guards now reject wrong `finished=false` defaults,
the wrong `RSplitNMut` count, and wrong nested reverse-constructor order even
when the generic theorem checker still accepts the mutated SMT. The
`rsplit_mut` and `rsplitn_mut` Verus models now represent their nested
`SplitMut`, `RSplitMut`, and `GenericSplitN` storage and prove explicit
nested-to-flat projections. The local result summary now reports 34
classified and 28 `not-run` rows.

Fresh accepted execution compiled the Python tools, ran 21 focused and 308
full tests, replayed 14 UNSAT theorem obligations and 21 SAT source instances,
and type-checked and verified every Verus model without `external_body`.
All 32 acceptance commands passed. The independent acceptance is retained in
`review/REVIEW_ACCEPTANCE_20260901T024835Z.md`; stage transition remains
disabled.

## Mutable edge extraction

Input orders 091 `split_first_mut`, 097 `split_last_mut`, 101
`split_off_first_mut`, and 103 `split_off_last_mut` use arbitrary-length
source transitions. Direct edge extraction follows the canonical
empty/nonempty slice-pattern split. The split-off wrappers follow three
ordered operations: replace the receiver with the source-created empty
literal, split the held original slice at the first or last element, and
assign the remainder back to the receiver.

The shared boundary contains only initial address, allocation, provenance,
mutable-borrow identity, and element layout. Wrapper boundaries additionally
contain the pre-result empty-literal identity consumed by `mem::replace`.
That identity is a lower source observation, not a final receiver or answer:
the explicit replacement and assignment transitions propagate it only on the
empty path. Result tags, selected indices and ranges, returned references,
final receiver/storage, answer encodings, and traces are excluded.

Reference identity is structural over address, allocation, provenance,
parent borrow, element range, element layout, and projection kind. First/tail
and init/last disjointness is range-based; selected and remainder references
may have equal addresses for a zero-sized element while remaining disjoint.
Full equivalence compares every principal return/reference identity,
receiver slot, backing sequence, and immediate mutable frame exactly.
Exact-output determinism projects only the principal return observations.

The source models produce UNSAT for both theorem projections on all four
targets. Their retained nonvacuity set includes empty, singleton, and longer
slices for both zero-sized and non-zero-sized element layouts. Independent
review accepted the four classifications on 2026-09-01 after Python
compilation, 15 focused and 323 full tests, four clean Verus proofs, 62
source-derived positive/negative probes, replay of eight UNSAT obligations and
24 SAT source instances, and direct semantic-content preservation checks.
The accepted ledger contains 38 classified and 24 `not-run` rows; stage
transition remains disabled.

## Targets 037 and 043 clone-effect semantics

Input orders 037 `clone_from_slice` and 043 `fill` are the only remaining
members of the `clone-or-callback-effect-boundary` reason class. Their
classification increment was independently accepted on 2026-09-01 against
the 38-classified/24-not-run baseline. Their retained boundaries are
admissible only for individual
source-used `Clone` results, callback-visible state transitions, panic
outcomes, and lower per-element write observations. Aggregate destination
storage, final callback state, operation order or count, and a complete
execution trace remain forbidden boundary observations.

The active generated vocabulary defines `slice_cloned_from(source, dest)` by
equal lengths and `cloned::<T>(source[i], dest[i])` at every index. The frozen
target-037 implementation-proof harness instead declares its local helper as
`dest == source`. That equality is not the active contract relation and
cannot be reused as the target obligation's semantics. The source-backed
model must retain relation-valued per-call clone results and derive the
destination sequence, callback order, state chain, and panic prefix from the
canonical `CloneFromSpec` transition.

Canonical Rust 1.96 gives `clone_from_slice` both the default ordered
`clone_from` loop and the `TrivialClone` nonoverlapping-copy specialization.
It gives `fill` the default split-last clone loop, a `TrivialClone`
`ptr::read` loop, `u8`/`i8` `write_bytes` implementations, and integer
fast-path-or-loop implementations. Specialization selection is fixed by the
input type and is not a free hidden dependency observation. The Miri
configuration is a platform input, while the integer specialization's
`is_val_statically_known(value)` result is a genuine hidden intrinsic
observation that may be fixed by `Boundary_T`; neither may carry the resulting
slice.

The integer condition evaluates
`(cfg!(miri) && self.len() > 32) || is_val_statically_known(value)`
left-to-right. The static-known intrinsic is skipped only on the Miri
long-slice branch; every other integer branch calls it once. A static-known
uniform-byte fast path then calls `write_bytes` as a second intrinsic. The
source-backed model therefore records totals of 2 for static-known uniform;
1 for static-known nonuniform, dynamic loop, Miri-short loop, and Miri-long
uniform; and 0 for Miri-long nonuniform. Its independent fail-closed probe
requires all six totals and shows that the former selected-path-only formula
fails the first four rows.

The shared SMT transition, compact and zero-callback witnesses, and Verus
model use this control flow. Every reachable path has explicit source-backed
transition semantics. Independent execution compiled the Python tools, passed
17 focused and 340 full tests, verified both Verus models without
`external_body`, replayed four normal, two panic-prefix, and one mismatch
theorems as UNSAT, replayed 27 source, six panic-prefix, and two mismatch
witnesses as SAT, and rejected ten negative probes as UNSAT. The accepted
ledger contains 40 classified and 22 `not-run` rows; stage transition remains
disabled.

## Exact mutable chunk partitions

For `chunks_exact_mut` and `rchunks_exact_mut`, the admissible shared boundary
contains only the initial slice address, allocation, provenance, unique parent
borrow, and element layout. The chunk size is part of the shared input, not the
boundary. The modulo remainder, split index, returned ranges, raw iterator
region, remainder reference, private constructor fields, direction, output,
and immediate final state must all be derived.

Both constructors require a positive chunk size and compute
`rem = len % chunk_size`. The forward constructor splits at `len - rem`, stores
the divisible prefix in raw `v`, and retains the suffix as the unique
remainder. The reverse constructor splits at `rem`, retains the prefix as the
remainder, and stores the divisible suffix in raw `v`. Consequently the
forward partition composes as yielded-prefix, remaining, remainder; the reverse
partition composes as remainder, remaining, yielded-prefix. The yielded prefix
is empty at construction.

Allocation, provenance, element layout, and parent-borrow identity are
preserved for both derived regions. Region disjointness is defined by element
ranges rather than data-address inequality: two nonempty regions of a
zero-sized type may have the same address while remaining disjoint. Exact
equivalence compares every source/range, raw-pointer, reference/borrow,
modulo/split, direction, private-state, and immediate final-state observation.
An exact-output projection omits only the final-state fields.

The retained nonvacuity set covers empty, unit-chunk, shorter-than-chunk,
divisible, nondivisible, and ZST equal-address inputs. Permanent guards reject
zero chunk size, incorrect modulo or split index, swapped remainder placement,
wrong concatenation order, provenance or borrow loss, incorrect ZST address
reasoning, omitted active-contract conjuncts, weakened equality,
answer-bearing or laundered boundary fields, mismatched boundaries, and
out-of-scope ledger updates.

An independent Reviewer accepted this bounded increment on 2026-09-01 after
fresh Python compilation, 15 focused and 355 full tests, direct field and
composition-order probes, and the complete 35-command acceptance driver. Four
theorem obligations replayed as UNSAT, 12 required source instances replayed
as SAT with models, and 16 negative probes replayed as UNSAT. Both Verus models
verified three obligations with zero errors and no `external_body`. A
readable-content comparison preserved 3,267 files in the 40 previously
certified evidence trees and all 320 frozen inputs. The accepted ledger now
contains 42 classified and 20 `not-run` rows; stage transition remains
disabled.

## Mutable fixed-chunk edge semantics

For `last_chunk_mut`, `split_first_chunk_mut`, and `split_last_chunk_mut`, the
admissible shared boundary contains only the initial non-null slice address,
allocation, provenance, unique parent-borrow identity, and element size. The
const-generic `N` is part of the shared input `x`, not a hidden observation.
The branch result, subtraction and split indices, prefix and suffix ranges,
array view, tuple orientation, returned references, derived borrows, output,
final state, answer encodings, and traces must be derived.

The `Some` branch is taken exactly when `N <= len`. `last_chunk_mut` and
`split_last_chunk_mut` use checked subtraction to derive `index = len - N`;
`split_first_chunk_mut` uses the checked split at `N`. The canonical mutable
raw-parts transition constructs `[0,index)` and `[index,len)`, and preserves
allocation, provenance, layout, and parent borrow for both regions. The
selected prefix or suffix then flows through the canonical slice
`as_mut_ptr`, raw-pointer `cast_array`, and mutable dereference transitions.
In particular, the retained row-090 helper that uses the slice length as an
address and null provenance is not a usable transition and must be replaced,
not trusted or relabeled.

Reference identity is structural over address, allocation, provenance, parent
borrow, element range, layout, and projection. Tuple orientation is
array-only for `last_chunk_mut`, array-first for `split_first_chunk_mut`, and
array-second for `split_last_chunk_mut`. Array conversion is permitted only
after the selected region length is shown equal to `N`. Prefix/suffix
disjointness is range-based, so nonempty zero-sized regions may have equal
addresses. The immediate final frame preserves both regions and composes them
in their original order.

Exact equivalence compares every principal return and reference-identity field
and every modeled immediate final-state observation. The exact-output
projection omits only final-state fields. The required nonvacuity cases are
empty `N=0`, empty positive `N`, `N=0` on nonempty input, `N > len`, `N = len`,
strict interior splits, and nonempty ZST equal-address regions. Permanent
guards reject wrong branches, subtraction or split indices, swapped ranges or
tuple order, unchecked array length, synthetic/null provenance, allocation or
borrow loss, address-based ZST disjointness, missing final-frame composition,
omitted contract conjuncts, weakened equality, answer-bearing or laundered
boundaries, mismatched boundaries, and out-of-scope ledger changes.

An independent Reviewer accepted this three-row increment on 2026-09-01 after
fresh Python compilation, 14 focused and 369 full tests, a source-derived
field probe over all 21 required target/case combinations, and the complete
36-command acceptance driver. Six theorem obligations replayed as UNSAT, 21
edge and ZST instances replayed as SAT with retained models, and 30 semantic
negative probes replayed as UNSAT. All three trusted-free Verus models
verified two obligations with zero errors.

A readable-content comparison preserved 3,487 files in the 42 previously
certified evidence trees and all 320 frozen inputs. The accepted ledger now
contains 45 classified and 17 `not-run` rows; stage transition remains
disabled.

## Mutable split-at primitives

For `split_at_mut_checked` and `split_at_mut_unchecked`, `mid` is part of
shared input `x`. The admissible shared boundary contains only the initial
non-null slice address, allocation identity, pointer provenance, unique
parent-borrow identity, element size, and element alignment. It excludes the
checked branch, unchecked-domain decision, pointer-add result, tail
subtraction, derived regions and borrows, principal output, immediate final
state, answer encodings, and traces.

The checked transition selects `Some` exactly when `mid <= len` and otherwise
returns `None` without changing the parent frame. The unchecked transition is
defined only under `mid <= len`. The successful source path casts the slice to
its thin mutable pointer while preserving address, allocation, provenance,
borrow, and layout; derives `ptr.add(mid)` and `len - mid`; constructs raw
mutable regions `[0,mid)` and `[mid,len)`; and returns unique structural
references to those regions in left-then-right order.

Reference identity includes values, logical range, address, allocation,
provenance, parent borrow, element layout, side projection, and uniqueness.
The right pointer may be one-past-end when `mid = len`. Disjointness is based
on element ranges rather than unequal addresses, so nonempty ZST left and
right regions may have the same address. The immediate frame preserves the
two regions and composes them in their original order.

Retained sites `TS-085-D002`, `TS-085-E002`, `TS-086-D005`, and
`TS-086-E002` remain identified as answer-bearing blockers; they are replaced
by the canonical transitions above rather than relabeled or admitted into
`Boundary_T`. The retained length-as-address, null-provenance mutable pointer
constructor is likewise prohibited.

Exact equivalence compares every modeled return and structural
reference-identity field. Full conditional completeness additionally compares
every pointer, region, borrow, and immediate final-state field. Nonvacuity
must cover `mid = 0`, `mid = len`, strict interior splits, checked
`mid > len`, rejection of invalid unchecked inputs, one-past-end pointers,
and nonempty ZST equal-address regions. Permanent guards reject branch
inversion, off-by-one split or subtraction, swapped regions,
pointer/allocation/provenance/borrow loss, address-only disjointness, missing
or reversed final frames, omitted contract conjuncts, weakened equality,
answer laundering, boundary mismatch, and out-of-scope ledger edits.

An independent Reviewer accepted this two-row increment on 2026-09-01 after
fresh Python compilation, 16 focused and 385 full tests, and a separate
source-derived probe over all 11 required cases and all 781 modeled
output/state field expectations. Four theorem obligations replayed as UNSAT,
11 source instances as SAT with retained models, and 23 semantic/domain probes
as UNSAT. Both trusted-free Verus models verified two obligations with zero
errors.

A direct readable-content comparison preserved 3,882 files across the 45
previously certified evidence trees and all 320 frozen inputs. The accepted
ledger now contains 47 classified and 15 `not-run` rows; stage transition
remains disabled.

## Split-off pair

For `split_off` and `split_off_mut`, one-sided range kind and index belong to
shared input `x`. `Boundary_T` contains only the initial slice address,
allocation, provenance, parent-borrow identity, element size, and element
alignment. It excludes direction, split index, checked-add and bounds
decisions, returned/remaining regions, derived borrows, output, final state,
answer encodings, and traces.

The source transition maps StartInclusive to Back, End to Front, and
EndInclusive to Front after checked addition; `usize::MAX` overflows to
`None`. A split index greater than the receiver length returns `None` with an
unchanged receiver. Successful paths derive exact front and back subranges,
directional receiver reassignment and return, reference identity, one-past
behavior, and range-based ZST identity. The mutable path additionally derives
`mem::take` ownership transfer, the temporary empty receiver, disjoint unique
borrows, and ordered front-then-back frame composition.

The active mutable contract is used without correction: both the initial
returned-slice partition and `final(ret.unwrap())` partition are live. The
frozen corrected harness remains provenance only and cannot substitute its
deleted final-return clause. Exact-output equivalence compares all principal
option and returned-reference fields; full equivalence also compares every
modeled helper, ownership, region, borrow, receiver, and frame observation.

Four theorem obligations replay as UNSAT. Twenty-eight source cases are SAT
with retained models, covering empty, zero, interior, len, out-of-bounds,
EndInclusive-len, `usize::MAX`, one-past, and nonempty ZST behavior. Twenty
semantic probes are UNSAT. Permanent guards reject direction reversal,
wrapping addition, altered bounds, off-by-one splits, swapped branches,
mutated None frames, identity or borrow loss, removal of the active
final-return clause, reversed frames, weakened equality, answer laundering,
mismatched shared inputs or boundaries, and out-of-scope ledger edits.

The bounded runner preserves the 47-target accepted baseline and all 320
frozen inputs, changes only rows 099 and 104, and records 49 classified and 13
`not-run` rows. Independent review accepted this bounded pair after a fresh
38-command acceptance run, 401 tests, direct replay of all four theorem
obligations, and a separate source-derived oracle over every modeled output,
state, and boundary field. Stage transition remains disabled.

## Raw slice constructors

For `from_raw_parts` and `from_raw_parts_mut`, the pointer, length, and
mutability are shared input `x`. `Boundary_T` contains only genuine initial
address-indexed memory, initialization, allocation bounds, provenance,
single-allocation identity, alias permissions, element layout, platform
limits, and the root borrow/frame. It excludes returned references or
sequences, raw fat-pointer results, final storage, answer encodings, target
truth, and traces.

`TS-048-D001` and `TS-049-D001` remain context-only raw-domain vocabulary.
The answer-bearing `TS-048-D002`/`TS-048-E001` and
`TS-049-D002`/`TS-049-E001` remain inadmissible. They are replaced, not
relabeled, by explicit source transitions for the UB precondition, raw
fat-pointer construction, and reference dereference. Those transitions derive
the returned length, allocation, address, provenance, root borrow, mutability,
and finite element sequence directly from pointer-reachable initial memory.
Shared input `x` contains no logical memory/result array. Boundary memory uses
initialized/uninitialized cells keyed by concrete addresses.

For each logical index `i`, the finite dereference transition reads the
initialized boundary cell at `data + i * size_of::<T>()`. Zero-sized elements
reuse `data` for every logical index. Recursion stops at `len`, so a zero-length
slice, including an allocated one-past pointer, performs no boundary-memory
read. Returned and immutable-final memory are finite sequences rather than
whole backing arrays; mutable final contents remain arbitrary at the fixed
slice length because the active contract has no final-memory conjunct.

The valid domain includes allocated nonempty slices; allocated and non-null
aligned dangling empty slices; allocated and dangling nonempty ZST slices
whose end address equals the start; initialized elements; a single allocation;
shared no-mutation or mutable exclusive aliasing; `len * size_of::<T>()`
fitting `isize`; non-wrapping address arithmetic; and permitted one-past
endpoints. Null or misaligned pointers remain invalid for empty and ZST
inputs. Nonzero spans require allocation and provenance and must remain within
one allocation. Uninitialized elements, alias violations, multiplication or
address overflow, incorrect return/reference identity, boundary mismatch,
helper-mediated answer laundering, weakened equality, and out-of-scope ledger
edits fail closed.

Exact equivalence compares every principal return/reference field. Full
equivalence additionally compares every modeled state field. The immutable
constructor has deterministic initial output and unchanged state, so both
theorem negations are UNSAT. The mutable constructor has deterministic initial
output, so its exact-output theorem negation is UNSAT, but its active contract
contains no final returned-memory clause. Its full-state theorem is therefore
SAT: a separately replayed fixed-input/fixed-boundary witness holds both
executions to every active conjunct and identical initial returns while
varying only final in-range memory. No final-frame clause is invented.

The bounded runner retains four theorem obligations, 14 SAT source instances
with models, 54 UNSAT negative probes, the fixed mutable SAT witness and model,
independent solver replay, and two trusted-free Verus models. It preserves the
49-target accepted baseline and all 320 frozen inputs by readable content,
changes only rows 048 and 049, and records 51 classified and 11 `not-run`
rows. Stage transition remains disabled.

The 2026-09-01 changes-required finding was repaired by updating the generator,
validator, generated checker design, and Reviewer request to the measured total
of 54 negative probes. Independent UNSAT probes reject a first element
different from the cell at address 4096, any mismatching interior element, a
nonempty slice starting at one-past, missing initialization, allocation or
provenance, nonzero byte stride for a ZST, and an empty one-past view that
materializes an element.

Independent review at 2026-09-01T10:20:36Z accepted targets 048 and 049 after
fresh Python compilation, 17 focused tests, the complete 418-test suite, two
trusted-free Verus models with two verified obligations and zero errors each,
three UNSAT theorem projections, the mutable full-state SAT result and fixed
witness, 14 SAT source instances, 54 UNSAT negative probes, the 51/11 bounded
runner, local validation, and the 39-command acceptance driver. Direct
readable-content comparison preserved all 49 accepted evidence trees and all
320 frozen inputs. Target 048 is conditional-complete for exact output and
full state; target 049 is exact-output conditional-complete and full-state
conditional-incomplete. Stage transition remains disabled.

## SliceIndex get trio

Targets 053 `get_mut`, 054 `get_unchecked`, and 055 `get_unchecked_mut`
replace their retained answer-equivalent or answer-bearing SliceIndex helpers
with defined bounds, pointer/provenance, dereference, returned-reference,
borrow-identity, and frame transitions. Retained contract vocabulary remains
context-only, and no retained whole-target helper is admitted into
`Boundary_T`.

The shared boundary contains only initial bounded slice memory,
allocation/address extent, provenance and root-borrow identity, alias
permissions, element layout and platform limits, and an outside-frame token.
It excludes returned references, option results, normalized indices, raw
pointer results, final memory, canonical answers, target truth, and traces.

Target 054 expands every applicable sealed Rust 1.96 `SliceIndex<[T]>`
implementation: `usize`, `IndexRange`, old and new range families, the bound
pair, all supported `Clamp` wrappers, and `Last`. Its two bounded theorem
negations are UNSAT. All 25 source instances are SAT with retained
observations, and an independent 4,100-case source oracle covers valid and
invalid bounds, ZST address behavior, exhausted inclusive ranges, bound-pair
variants, and clamp edges.

Targets 053 and 055 use a concrete valid `usize` instantiation. Their active
mutable-frame contracts do not bind returned-reference identity, so the
canonical element-zero reference and a distinct well-formed element-one
reference satisfy the same contract under one shared boundary and exact same
final state. Both exact-output and full-state classifications are therefore
`conditional-incomplete`; target 054 is `conditional-complete` for both
projections within the declared bounded model.

Independent review accepted the trio on 2026-09-01 after forced Python
compilation, 13 focused and 431 complete tests, three trusted-free Verus
models, direct replay of six theorem obligations, 27 SAT source models, 12
UNSAT negative probes, two SAT fixed witnesses, the bounded runner, integrated
validation, and the 40-command acceptance driver. Direct byte-content
comparison preserved all 4,903 files in the 51 certified evidence trees and
all 320 frozen inputs. The ledger contains 54 classified and 8 `not-run` rows;
stage transition remains disabled.

## Address-derived slice observers

For `element_offset` and `subslice_range`, target lengths and initial memory
identity are shared input. `Boundary_T` contains only initial exposed
addresses, allocation identities and extents, provenance, liveness, element
layout, and machine usize/isize limits. It excludes computed offsets or
ranges, branch truth, panic/option outputs, final state, answer encodings, and
traces.

The active generated normal-return implications remain unchanged. Their
opaque pointer-domain predicates are interpreted by defined Rust 1.96
transitions for slice pointer extraction, `ptr::from_ref` where applicable,
address observation, machine-usize wrapping subtraction, element-stride
alignment, division, wrapping range-end addition, exact bounds decisions, and
algebraic option construction. The documented ZST panic is a separate
algebraic outcome reached before address division. No uninterpreted solver
function or source-selected answer conjunct is used.

Retained sites `TS-039-D006`, `TS-039-E003`, `TS-039-E004`,
`TS-039-E005`, `TS-111-D006`, `TS-111-E002`, `TS-111-E003`, and
`TS-111-E004` remain inadmissible and are replaced rather than relabeled.
Every other retained site is bound and dispositioned explicitly. Exact-output
equivalence compares the entire panic/None/Some return. Full equivalence also
compares the unchanged memory identity.

The source domain includes same-allocation interiors and endpoints, distinct
allocations, element-stride misalignment, pointer-before-receiver wrapping,
machine-width limits, valid dangling ZST references, and invalid null,
misaligned, dead, overlapping, wrapping, or oversized reference
representations. The two documented empty-subslice false positives at a
separate allocation's numerically equal start or end address are modeled
positively. They do not weaken equivalence: one fixed boundary still computes
one exact range.

The bounded campaign changes only rows 039 and 111, preserves all 54
previously certified evidence trees and all 320 frozen inputs, and requires
four UNSAT theorem projections before recording both targets as
`conditional-complete` for exact output and full state. The resulting ledger
has 56 classified and 6 `not-run` rows.

Independent review accepted this increment on 2026-09-01 after readable
inspection of both contracts, source items, docs, harnesses, proof manifests,
all 27 trust records, theorem boundaries, equivalence projections, and
empty-subslice witnesses. Fresh execution passed 11 focused tests, all 442
repository tests, both trusted-free Verus checks, four UNSAT theorem replays,
22 SAT source-model replays, 46 UNSAT negative probes, the bounded runner, the
integrated validator, and all 41 acceptance commands. A direct byte-content
comparison preserved all 54 certified evidence trees and 320 frozen inputs.
This acceptance does not transition the Manager-owned stage.

## `align_to` source semantics

For `align_to` and `align_to_mut`, the shared boundary is the initial
address-indexed byte memory and initialization, Slice length/address/
allocation/provenance, T/U layout and ZST facts, platform limits, the unsafe
transmute-validity precondition, root-borrow state, alias permission, and
outside frame. It never contains `slice_align_to_domain`,
`slice_aligned_middle`, an offset or branch answer, returned partitions,
decoded middle values, final memory, or a trace.

The source interpretation follows Rust 1.96 through Slice pointer extraction,
`ptr::align_offset` including element stride, wrapping addresses and
`usize::MAX`, ZST/offset fallback, gcd-based `align_to_offsets`, exact split
ranges, pointer casts/addition, raw-slice construction, and byte-derived typed
middle values. Returned references preserve allocation, provenance, and root
identity; mutable ranges are disjoint. A relational final byte frame decodes
the final receiver and all three returned views, while legal mutable writes
remain free.

The answer-bearing sites `TS-008-D004`/`TS-008-E005`/`TS-008-E006` and
`TS-009-D004`/`TS-009-E003`/`TS-009-E004` remain excluded and are replaced,
not relabeled. Exact output and full state are both conditional-complete for
`align_to`. `align_to_mut` is exact-output conditional-complete and full-state
conditional-incomplete: its fixed same-input/same-boundary witness changes an
in-range byte and re-derives every final T/U view while preserving the
outside frame and backing identity. The bounded evidence leaves all 62
selected targets classified and zero `not-run`.

Independent review accepted the `align_to` pair on 2026-09-01 after readable
inspection of the literal contracts, canonical source/docs, frozen proof
inputs, all 20 trust records, theorem boundaries, exact equivalence, and the
mutable witness. Fresh execution passed 11 focused tests, all 466 repository
tests, both six-item trusted-free Verus proofs, direct Z3 replay, the bounded
runner, the integrated validator, and all 43 acceptance commands. An
independent source-derived probe covered 486,240 valid
layout/address/length combinations, and direct byte comparison preserved all
60 predecessor evidence trees and 320 frozen files. The review did not invoke
a Manager-owned stage transition.

## Final obligation crosswalk and results dossier

The additive `crosswalk/conditional_obligation_crosswalk.{csv,json}` joins
each of the 62 active UNKNOWN targets to the exact active authority,
implementation-proof inputs and complete retained trust inventory, the
separate boundary used by the conditional obligation, source citations,
proof scope, equivalence, direct solver evidence, replayable SAT evidence
when required, Verus evidence, classification, and the accepting incremental
review. The original `target_to_proof_boundary` authority ledger remains
unchanged.

Target 029 now has a deterministic source-backed manifest at
`evidence/final_campaign/target_029_boundary_manifest.json`. It explicitly
distinguishes the six executable lower sites retained by the implementation
proof from the four lower sites that back actual `Boundary_T` observations.
Only source element reads and per-call comparator results/state transitions
enter `b`; hint/loop support remains outside the boundary, as do the selected
index, returned `Result`, aggregate final state, branch choice, answer
encodings, and traces.

The reconciled exact-output counts are 48 conditional-complete, 12
conditional-incomplete, and 2 missing-source-backed-model. The full-state or
reviewed-equivalence counts are 41, 19, and 2 respectively. The only weakened
equivalences are matching-index equivalence for rows 028-030 and equal-key
reordering equivalence for rows 080-082. Rows 078-079 remain
missing-source-backed-model: their bounded UNSAT results are retained as
diagnostics and are explicitly ineligible as classification evidence.

`evidence/final_campaign/preservation_baseline.json` byte-locks every
pre-existing evidence file, all 320 frozen inputs, the frozen authority
ledger, and all accepted incremental reviews. The final campaign-wide
independent review accepted all 62 rows on 2026-09-01 and is recorded in
`review/FINAL_CAMPAIGN_REVIEW_ACCEPTANCE.md`. The fresh 44-command acceptance
run compiled the Python sources, ran all 474 tests, replayed all 1,164 retained
target captures, and reproduced the exact-output `48/12/2` and full-state
`41/19/2` counts. Direct recursive comparison preserved all 6,844
pre-existing evidence files, 320 frozen inputs, nine authority-ledger
artifacts, and the accepted incremental reviews.

## Mutable view construction

For `as_flattened_mut`, `as_mut_array`, `first_chunk_mut`, and `from_mut`,
the shared input contains the receiver values, slice or container length,
`N` where applicable, and the initial hidden representation. `Boundary_T`
contains only initial and outside-frame memory, address, allocation extent,
provenance, live exclusive root-borrow identity, element layout, and
usize/isize platform limits. It excludes multiplication results, overflow or
option branches, returned values, ranges, pointer or borrow identities,
array/slice projections, final state, answer encodings, and execution traces.

The source transition computes `as_flattened_mut`'s checked ZST
multiplication and overflow panic separately from its valid non-ZST unchecked
multiplication. Normal construction then preserves mutable pointer address,
allocation, provenance, and root-borrow identity through the source cast and
raw-slice construction. `as_mut_array` uses the exact `len == N` branch;
`first_chunk_mut` uses the exact `N <= len` branch and returns `[0,N)`.
Both derive the mutable array reference from the canonical `as_mut_ptr` and
`cast_array` steps. `from_mut` derives a singleton mutable array reference
from canonical `core::array::from_mut` and then applies the array-to-slice
unsizing coercion, preserving the singleton range and borrow identity.

`BorrowLifetimeFinalFrameTransition` preserves the outside-memory region and
backing identity while leaving successful returned contents free at the exact
returned length. On a successful prefix return, the receiver is the returned
prefix followed by the untouched old suffix; whole-view returns reconstruct
the same complete backing range from the returned view. Panic and `None`
branches create no returned borrow and preserve the input. Zero-length and
ZST references retain their structural
address/allocation/provenance/root-borrow identity even when byte ranges or
addresses alone cannot distinguish them.

This relational frame repairs the first independent review finding. It does
not fix successful returned mutable views to their initial values. The active
`final(...)` clauses relate the receiver to the returned view while permitting
legal writes through the returned `&mut`, matching the campaign's accepted
chunk and raw-slice policy.

Retained sites `TS-017-D006`/`TS-017-E004`,
`TS-018-D004`/`TS-018-E002`, `TS-046-D004`/`TS-046-E002`, and
`TS-047-D001`/`TS-047-E001` remain inadmissible complete-result or
complete-branch support. Defined source transitions replace them; they are
not relabeled as boundary observations. Target 047's canonical Rust 1.96
`core/src/array/mod.rs:174-177` excerpt is retained as project-local evidence
outside the frozen authority tree.

Exact-output equivalence compares the complete panic/option tag, values,
range, address, allocation, provenance, root-borrow, layout, projection, and
uniqueness. Its four direct theorem replays are UNSAT.
Full-state equivalence additionally compares receiver and returned-view final
contents, so all four contract-faithful obligations are SAT. Each target
retains a replayable same-input/same-boundary witness whose executions have
the same exact initial output and backing identity but distinct first returned
elements. Witnesses preserve exact final lengths, receiver/return
reconstruction, target-046's old suffix, outside memory, and backing
provenance.

The ledger therefore classifies all four targets exact-output
`conditional-complete` and full-state `conditional-incomplete`, with 60
classified rows and 2 `not-run` rows. The bounded runner also retains all 22
SAT source instances, 82 UNSAT semantic/domain probes, four trusted-free Verus
models, all 56 certified predecessor evidence trees, and all 320 frozen
inputs.

Independent review accepted this bounded increment on 2026-09-01 after
readable inspection of all four contracts, source items, docs, canonical
helpers, frozen harnesses and manifests, all 34 trust records, generated
obligations, and concrete witnesses. Fresh execution passed forced Python
compilation, 13 focused tests, all 455 repository tests, all four
trusted-free Verus checks, direct replay of four exact-output UNSAT
obligations, four full-state SAT obligations, four fixed-witness SAT
instances, 22 source SAT instances, and 82 negative-probe UNSAT instances.
A separate 17-case source-derived mapping probe accepted every correct
output/default/frame mapping and rejected every wrong-field alternative. The
bounded runner, both validators, and all 42 acceptance commands passed.
Direct byte-content comparison preserved the complete target-evidence tree,
including all 56 certified predecessor trees, and all 320 frozen inputs.
This acceptance does not transition the Manager-owned stage.

## Target 078 operational-model increment

The additive `target_078_operational_v1` Python interpreter now covers the
full reachable Rust selection algorithm for arbitrary valid lengths and
indices: bounds, ZST, min/max scans, insertion sort and CopyOnDrop restoration,
recursive pivot selection, all partition kernels, ancestor-pivot handling,
strictly shrinking windows, the sixteen-step fallback, ninther helpers,
callback panic prefixes, and returned subslices. Adversarial source review
found the reachable algorithmic translation faithful.

The later accepted repair replaces the former compact classification machine
with a fuel-free `ExactRunState` big-step transition. It preserves exact
callback and mutation order for insertion, extrema, recursive pivot selection,
all partition kernels and their guards, narrowing, fallback, panic
propagation, and return projection. The descending length-17 cyclic regression
now compares that formal transition directly with the Python interpreter over
the complete final slice, callback state, panic status, and principal return.

Classification boundaries are total over all callback states and identity
pairs, and their separate state-independent contract Ordering projection is
required to satisfy the reviewed order laws. The trusted-free Verus artifact
is a checked projection of every exact terminal result field rather than a
compressed source interpreter. The additive target-078 exact-output and
full-state classifications are `conditional-complete`; the independent
target-078 review addendum accepted this increment without changing the
certified campaign row or Manager-owned stage.

## Target 079 operational-model increment

The target-079 Rust 1.96 source, MIR, and behavioral probes establish the
adapter order `f(left)`, `f(right)`, `PartialOrd::lt`, right-key destruction,
then left-key destruction. They also establish all ordinary panic prefixes,
callback-visible destructor effects, and immediate process termination when a
key destructor panics during an existing unwind. The shared boundary may
therefore expose total key, `lt`, and hidden Drop observations, but not their
realized schedule or any selection answer, mutation, final state, or trace.

The accepted repair structurally parses all 14 imported `ExactState`
constructors and derives abort from each constructor's source state. Seven
active CopyOnDrop or gap-restoration stores now restore on ordinary panic but
preserve the interrupted sequence on abort. The target-079 adapter separately
models both owned key identities, reverse destruction, every normal and panic
prefix, unwind cleanup, destructor panic, and double-panic termination while
reusing the target-078 selection engine only as read-only source semantics.

The classification boundary is explicitly narrower than unrestricted public
Rust execution: runtime key results must project to one state-independent
contract key function, and the reviewed contract Ordering must be total. That
condition is admissible because it fixes only genuine key, `Ord::lt`, Drop,
and callback-state observations. It still excludes realized calls, temporary
or drop schedules, selection control, mutations, return projections, final
state, and traces.

Seventeen target-specific selection force probes and 17 paired mutations cover
ZST and extrema dispatch, insertion and CopyOnDrop, recursive pivot selection,
all partition kernels, ancestor handling, both narrowing directions, the
sixteen-step fallback, median-of-ninthers, and return projection. Nine adapter
force probes and nine adapter mutations cover the source lifecycle. Direct Z3
replay is UNSAT for both exact principal-return determinism and exact
principal-return/final-state completeness; normal non-ZST and ZST
`TargetDefinition_T`/`Spec_T` witnesses are SAT. The trusted-free Verus
projection verifies seven obligations.

The independent target-079 addendum accepts this additive
`conditional-complete` result after 18 lifecycle/composition tests, 15
formal/artifact tests, all 540 repository unit tests, and all 46 acceptance
commands passed. The certified campaign row, accepted target-078 package,
frozen authorities, campaign ledgers and reviews, and Manager-owned pipeline
state remain unchanged.

### Constructive adapter refinement

The additive target-079 adapter refinement constructs its terminal frame in
Verus from exactly four inputs: the accepted shared `KeyOrdDropBoundary`, the
current callback-visible state, and the left and right source identities. It
does not accept an exact result, terminal frame, lifecycle schedule, or trace.
Its five source transitions are composed in the fixed order `f(left)`,
`f(right)`, `Ord::lt`, `drop(right)`, and `drop(left)`. Owned-key creation
state, operand slot, source identity, temporary liveness, callback-state
threading, panic origin, cleanup order, and abort are all derived by those
transitions.

The Verus branch proofs cover normal execution, first- and second-key panic
prefixes, `Ord::lt` unwind, normal and unwind destructor panic, reverse
cleanup, and double-panic abort. The correspondence bridge parses the
expression AST of all 27 Verus semantic functions and mechanically emits an
independent `Refined*` SMT definition for each one. Nested Verus boundary-map
indices are encoded through the accepted `KeyCall`, `OrdCall`, `DropCall`, and
`PairKey` keys, and struct literals are emitted in the accepted constructor
field order. The query compares every scalar helper result plus every
`OwnedKey` and `AdapterFrame` selector at every constructor/helper boundary,
for 113 explicit comparisons.

Three correspondence-only regressions remain valid trusted-free Verus models:
storing the left owned key in `adapter_drop_right.af_right_owned`, changing the
initial right-owned slot default, and reading key results from the next-state
boundary field. Each mutation makes the derived correspondence query SAT,
while the unmodified query is UNSAT. The bridge therefore detects changes to
constructor defaults, helper field selection, and frame-field propagation
that the branch lemmas alone need not reject. This refinement does not widen
`Boundary_T` or change the separately accepted exact-output and full-state
classification.

Independent L2 review accepted the constructive refinement on 2026-09-02.
Fresh execution type-checked the Verus model and verified all 13 obligations,
replayed the 113-comparison correspondence query as UNSAT, rejected all six
semantic mutations, and replayed all three Verus-valid correspondence
mutations as SAT. The 13 focused tests, all 601 repository tests, and all 50
task-native acceptance commands passed. Direct before/after byte comparisons
also preserved the protected operational-v1, operational-v2, parser-repair,
and Manager-owned artifacts. The Engineer-generated result intentionally
retains its review-pending marker; the external decision is recorded in
`review/REVIEW_ADDENDUM_TARGET_079_ADAPTER_REFINEMENT_V2.md`.

### Target-078 constructive comparator adapter refinement

The additive target-078 adapter refinement constructs the source expression
`compare(a, b) == Ordering::Less` from exactly the accepted
`ComparatorBoundary`, the pre-call callback-visible state, and ordered left
and right source identities. The model looks up Ordering, next state, and
panic using the same pre-call state and operand order. It retains the derived
next state on both normal and panic paths, propagates panic only after that
update, and exposes the Less boolean only when the callback returns normally.
The boundary therefore remains narrower than the public selection target: no
call schedule, adapter result, selected output, final state, selection trace,
or target execution is an input.

The trusted-free Verus artifact proves ordered operand lookup, callback-state
threading on both paths, panic propagation, normal Less/equal/greater results,
normal-return gating, panic suppression of the boolean, and target entry from
the boundary's initial state. Its bridge parses the expression ASTs of all
five semantic helpers and emits distinct `Refined*` SMT definitions. For an
arbitrary accepted `ExactState`, boundary, and operands, 17 explicit
comparisons cover all nine `ComparatorAdapterFrame` fields, the four accepted
boundary/adapter helpers, the `e_callback_state` and `e_panicked` selectors of
`ExactCallback`, the normal Less result, and panic suppression.

Fresh Engineer execution verified 11 Verus obligations and replayed the
field-complete correspondence as UNSAT. Six paired source-semantic mutations
for operand reversal, pre-state lookup, next state, panic propagation,
normal-path gating, and Less encoding all type-check but fail verification.
Four Verus-valid field/selector/index mutations make the correspondence query
SAT. Retained exact-output and full-state obligations remain UNSAT and the
nonvacuity obligation remains SAT, so this additive package does not change
the accepted target-078 classifications. Its immutable result metadata retains
the package-local review-pending marker; the later independent acceptance is
recorded in the versioned path-level preservation section above. Stage
transition remains disabled.

An earlier L2 replay had confirmed the package-local proof but exposed an
integration-policy conflict: the final-campaign selector absorbed the 142 new
target-078 files, while operational-v2 absorbed the later target-079 adapter
review. That failed run was not a semantic counterexample. The shared
versioned policy above now resolves both selectors through exact registered
paths and closes the bounded acceptance gap.

### Target-078 insert-tail and CopyOnDrop refinement

The additive insert-tail refinement starts from the accepted
`ComparatorBoundary`, an arbitrary pre-call identity sequence and callback
state, and valid `begin < tail` indices. Its state has exactly the three
source-observable fields retained by `ExactState`: the identity sequence,
callback state, and panic flag. It does not accept a terminal result, final
state, selected value, answer encoding, call schedule, or execution trace.

The refinement follows the Rust 1.96 source order. It first compares the
temporary tail identity with `tail - 1`. A normal non-Less result leaves the
sequence unchanged. A Less result repeatedly copies `sift` into the current
gap, moves the gap to `sift`, and compares the temporary with `sift - 1`.
Normal termination restores the temporary into the gap. A callback panic
commits the callback's next state before propagating panic, and the active
CopyOnDrop guard restores the temporary into the current gap. The recursive
domain invariant is `0 <= begin <= sift`, `gap == sift + 1`, and
`gap < sequence.len()`.

The trusted-free Verus artifact proves the exact no-shift, initial-panic,
normal-restoration, panic-restoration, and recursive shift/gap transitions. A
structural induction additionally proves unchanged sequence length, equality
of identity multisets after guard restoration, equality at every index outside
the inclusive affected range, and retention of a boundary-observed callback
next state on every propagated panic. These properties hold for arbitrary
valid ranges rather than a bounded trace fixture.

The AST-derived bridge compares all three retained `ExactState` fields over
the arbitrary valid loop and entry domains. Correspondence with both
`ExactInsertTailLoop` and `ExactInsertTail` is UNSAT. Ten paired mutations
cover operand order, lookup state, shift source and destination, gap
advancement, base/normal/panic restoration, callback next state, and panic
propagation; each fails Verus verification and makes correspondence SAT. Four
SAT witnesses retain no-shift, multi-shift, insertion-at-begin, and
panic-after-shift paths.

Independent L2 review accepted this refinement after Verus reported
`14 verified, 0 errors`, the complete repository suite passed 654 tests, and
all 52 task-native acceptance commands passed. The additive
`path_policy_v2.json` binds the 196-file evidence scope and its separate review
lane while leaving `path_policy_v1.json`, prior classifications, frozen
authorities, accepted evidence, and Manager-owned state unchanged.

### Target-079 abort-aware insert-tail composition

The additive target-079 insert-tail kernel locally reproduces the accepted
`KeyOrdDropBoundary` lifecycle and composes its derived `adapter_transition`
with the Rust 1.96 `insert_tail` and `CopyOnDrop` control flow. Manual review
finds the primitive boundary fields and lifecycle chain consistent with the
accepted v2 artifact, but a retained mechanical binding is still required to
make that dependency fail closed against drift. Each comparison derives its
adapter invocation from only the current callback state and the current left
and right source identities. The resulting adapter frame is internal; the
model does not accept an adapter frame, invocation schedule, output, terminal
state, answer encoding, or execution trace.

The composed state adds the abort flag retained by target 079's
`ExactState`. Adapter termination `0` continues with the derived Less result,
termination `1` commits the adapter callback state and performs ordinary
active-gap restoration, and termination `2` commits the callback state but
bypasses `CopyOnDrop`, preserving the exact interrupted sequence after the
most recent shift. An adapter panic or abort during the initial comparison
occurs before gap creation and therefore leaves the sequence unchanged.

The arbitrary loop domain is `0 <= begin <= sift`, `gap == sift + 1`, and
`gap < sequence.len()`. The trusted-free kernel establishes exact no-shift,
multi-shift step, normal restoration, ordinary-panic restoration, and
abort-bypass equations. It also establishes length and outside-range framing
on every path and identity multiplicity whenever execution does not abort.

Independent L2 review accepted the composition on 2026-09-02. Fresh execution
verified 15 Verus obligations, replayed the adapter and arbitrary-domain
insertion correspondences as UNSAT, replayed four required path witnesses as
SAT, and made all ten source-semantic mutations correspondence-SAT; eight of
those mutations also failed Verus verification. The 16 target-specific tests,
11 additive-policy tests, 681-test repository suite, package runner, and
53-command task-native acceptance campaign passed. The accepted exact-output
and full-state classifications are unchanged, the independent decision is
registered through the `path_policy_v3` review lane, and stage transition
remains disabled.

## Operational-v2 parser-repair certification

The versioned additive certification at
`evidence/final_campaign/operational_v2/parser_repair_certification_v1`
binds the operational-v2 certified projection without replacing or rewriting
it. The accepted projection remains exactly 62 `core::slice` rows, with
exact-output counts `50/12/0` and reviewed-equivalence counts `43/19/0`.

The certification treats a review as canonical only when the repaired parser
finds exactly one count-bearing acceptance summary and the complete parsed
scope, timestamp, row count, overlay set, classifications, verdict, and stage
policy match the accepted operational-v2 review. Missing, duplicate,
conflicting, wrong-scope, wrong-count, stale, and non-`ACCEPT` evidence all
fail closed. Classification mutation and protected-file mutation are separate
mandatory negative probes.

The layer hash-binds the repaired parser implementation and its duplicate and
conflicting-summary regression test, the three unchanged certified-projection
artifacts, and the complete repository-local independent Reviewer evidence
inventory. Certification requires the Reviewer's build, focused regression
tests, complete nonzero suite, existing closure, and task-native acceptance to
have succeeded with no missing, extra, or changed member among the 707
protected paths. These paths include the reconciliation inputs,
classifications, frozen review tree, and Manager-owned pipeline state. The
new certification subtree is outside those frozen selectors and does not
authorize a stage transition.

## Target 080 operational-v1 source-closure work

The additive target-080 operational model binds the active generated
`sort_unstable` contract, public docs, `Ord` laws, public adapter, legacy
implementation-proof harness and manifests, all five audited trust records,
and the Rust 1.96 unstable-sort source closure. Its shared input contains
type and compilation properties; its boundary contains only total per-call
`Ord::lt` result, callback next-state, and panic functions. Realized calls,
pivots, partitions, swaps, schedules, outputs, final permutations, aggregate
state, and traces remain excluded.

The completed boundary provides total functions for every callback state and
identity pair. It includes arbitrary ordered duplicate classes, identity and
all-equal orders, affine callback-state transitions, and state/key panic
predicates. Classification-admissible instances require every implementation
`Ord::lt` observation to equal a separate state-independent contract order;
state-indexed operational fixtures remain explicitly nonclassifying.

The primary model and a separately structured source interpreter implement
both configuration-selected heapsort entries and `sift_down`, top-level
insertion, existing-run reversal, unstable small-sort algorithms, recursive
pivot selection, all three partition kernels and both guards, duplicate-heavy
ancestor partitioning, recursive-left and iterative-right quicksort, limit
fallback, and normal or panic unwind. The direct partition harness now returns
zero for an empty slice, the reference interpreter derives ZST and
configuration dispatch from shared configuration fields, and retained cases
cover sort8, sort9, `presorted_len = 1`, and scratch insertion-unwind paths.
The trusted-free Verus projection currently type-checks and verifies five
obligations.

The operational correspondence keeps all 28 retained executions initialized
from their source sequences and boundary initial states, then applies
source-derived primitive callback, swap, and origin-backed write transitions.
Both correspondence projections and all 26 force probes use this ground
normal form. The SMT definition inventory expands every signature in
`define-funs-rec`, including non-first members, before checking the required
transition set. Deleting any singular or mutually recursive source transition
therefore fails closed.

Nonvacuity and all 15 semantic mutations use small instances evaluated by
both independent source interpreters. Most replay the exact recursive
transition directly. The threshold and imbalance mutations use a
source-faithful reduction: a mutated dispatch predicate selects the exact
first callback transition, and a source-derived boundary panic makes that
transition terminal. The reduced side still starts from the source input and
consumes `Boundary_T`; it does not import an output, final state, aggregate
relation, or execution trace.

The Engineer runner always records
`engineer-complete-review-pending`. Preservation policy v4 registers the
Engineer model, parser, proof, queries, captures, and generated evidence, but
does not register or interpret a review addendum. An independent verdict is a
separate successor-policy lane, expected at path policy v5. The certified
target-080 classifications and Manager-owned stage remain separate and
unchanged.

`review/REVIEW_REQUEST.md` is a live lifecycle input and is not regenerated
or deleted by the authority builder. The operational-v2 request formerly at
that path remains byte-preserved in
`preservation/review_request_operational_v2_frozen.md`; only its exact
3,347-byte historical record is resolved to that archive for identity and
historical-review digests. The current target-080 request is validated
separately for target, source, boundary, solver, witness, Verus, and
path-policy-v5 review gates. No other historical artifact record receives
this treatment.

Independent review accepted the target-080 operational-v1 package on
2026-09-02 after direct source, schedule, boundary, correspondence, witness,
and Verus inspection. The final command-1 acceptance run passed all 54
commands, Python compilation, 725 repository tests, 28 source-initialized
witness replays, both UNSAT correspondence obligations, SAT nonvacuity, all
26 SAT force probes, all 15 SAT semantic mutations, and the trusted-free
five-obligation Verus proof.

The accepted campaign order must respect two regeneration layers.
Target 079's adapter producer runs first, followed by target 078's adapter
producer with four-CPU affinity so its byte-bound Verus rejection diagnostics
retain their registered emission order. `build_authority_design.py` then
resets the generated `crosswalk/` tree, after which the target and cluster
producers reconstruct the protected authority ledgers. Target 080 regenerates
its v4 registration and deleted addenda before target 079 consumes them.
Final-campaign reconciliation, operational-v2 reconciliation, and
certification closure then recreate the other crosswalk projections deleted
by the builder. Only after that closure do the target-078 and target-079 v3
refinement runners and the complete tests consume the fully reconstructed
policy chain.

Path policy v5 registers exactly
`review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md` as the one-review
successor to v4. The target lifecycle is `review-accepted`, while the
operational-v2 projection still excludes target 080 and retains its certified
exact-output `conditional-incomplete` and reviewed-equivalence
`conditional-complete` classifications. Direct pre/post comparison found no
change or deletion among the 832 files protected by policies v1-v4 and
Manager-owned state. This acceptance does not authorize a stage transition.

## Target 081 comparator-panic and archive-backed preservation semantics

The target-081 public adapter evaluates `compare(a, b)` exactly once before it
tests whether the returned ordering is `Ordering::Less`. Callback scalar state
and complete observable interior state transition during that evaluation even
when it panics. On panic, `less_tested` and `is_less` are both false; a latent
`Less` value may remain in the diagnostic event but cannot become the private
sorter's Boolean comparator result. Callback destruction, unwind, a panic from
normal destruction, and abort from a second panic remain separate observable
effects.

Path policy v6 is the archive-backed successor to the byte-identical v1-v5
chain. Its accepted-v4 policy version is materialized under
`preservation/archive_v1/` and must exactly satisfy the parent record carried
by v5. The archived policy is a deterministic reconstruction from the live v4
template plus explicit historical record versions. Those mappings name the
wiki index, this wiki page, the command-1 acceptance runner, the target-080
producer, and the target-080 artifact regression. No digest search or
best-effort archive discovery is permitted.

The resolver uses an archive only when the corresponding logical record has a
named version mapping. Every other accepted-v4 record must still match its
live path exactly. Missing or changed archive bytes, non-canonical or
traversing paths, duplicate logical/version/archive identities, absent
mappings, and files present under the archive root without a mapping are
errors. Once v5 exists, the target-080 producer returns the preserved live-v4
record without rewriting v4 from mutable acceptance or wiki files.

Target-081 evidence remains an additive operational result. Its two certified
public-contract classifications stay `conditional-incomplete`; independent
acceptance belongs only in a v7 successor that byte-binds the reviewed v6
package and verdict.
