# Conditional theorem and checker design

## Literal theorem

For each target `T`, the checker proves exactly:

```text
forall x, b, y1, s1, y2, s2.
  Requires_T(x)
  and Boundary_T(x, b)
  and Spec_T(x, b, y1, s1)
  and Spec_T(x, b, y2, s2)
  implies Equivalent_T(x, b, y1, s1, y2, s2)
```

The SMT obligation declares one `x` and one `b` and asserts the negation of
that implication. Both executions therefore share the same valid input and
the same genuine boundary observation. A completeness claim is admissible
only when the real solver returns `unsat`. The emitted template selects
datatype-compatible SMT logic `ALL`; acceptance executes that exact file with
Z3 and requires exit status zero, exact `unsat` stdout, and empty stderr.

`Spec_T` must call a defined, source-backed target transition. A declared
whole-target relation or functionality function is not a target definition.
`Boundary_T` may expose only source-used user/external or hidden dependency
observations. It may not contain a principal result, aggregate final state,
answer-equivalent encoding, final permutation, or complete execution trace.

## Observation equality

Exact equality of principal return, returned-reference identity, callback
state, and final-state observations is the default. Exact-output determinism
and completeness modulo reviewed equivalence are recorded separately.

The only pre-reviewed weak equivalences in this 62-row set are:

- Binary search (`binary_search`, `binary_search_by`, `binary_search_by_key`):
  two `Ok` indices may differ only when both identify matching duplicate
  elements; `Err` insertion indices remain exact. Citations:
  core/src/slice/mod.rs:2849-2917, core/src/slice/mod.rs:2925, core/src/slice/mod.rs:2926-2967, core/src/slice/mod.rs:2976, core/src/slice/mod.rs:3024-3063, core/src/slice/mod.rs:3077.
- Unstable sort (`sort_unstable`, `sort_unstable_by`,
  `sort_unstable_by_key`): element identities may differ only within equal-key
  classes; multiset, sorted key sequence, return, callback state, and all
  non-tie observations remain exact. Citations:
  core/src/slice/mod.rs:3079-3130, core/src/slice/mod.rs:3139, core/src/slice/mod.rs:3140-3185, core/src/slice/mod.rs:3194, core/src/slice/mod.rs:3195-3237, core/src/slice/mod.rs:3246.

For unstable sort, `Equivalent_T` therefore includes both exact element
multiplicity for every identity appearing in either result and position-wise
key equality. The positive witness swaps identities 10 and 11, which share a
key and preserve the multiset. The negative witness substitutes foreign
identity 12 with the same key; it preserves the key sequence but fails exact
multiset equality.

Each relation has a solver-replayed positive witness and a negative
discrimination witness under `evidence/equivalence/`. Selection APIs remain
exact; unstable-sort wording is not generalized to selection.

## Semantic boundary gate

The trust inventory records the full retained contract and a semantic
adjudication for every dependency, source-closure record, and `external_body`
site. A source citation is necessary but not sufficient: a helper that states a
complete target/branch postcondition or a definitionally answer-equivalent
result is marked inadmissible. All 86 external target/symbol pairs and all 232
dependency IDs are enumerated; hashes bind the audit to the complete retained
contracts and records. Any missing, added, or changed input fails closed.
Target-level admissibility and narrowness are derived from all dependency and
external-site dispositions, including intrinsic answer-equivalent dependencies,
rather than from whether the public target function itself has `external_body`.
The synthetic null-provenance constructors retained for `as_mut_ptr` and
`as_ptr` repeat those targets' complete generated postconditions and do not
model the canonical Rust slice-to-thin-pointer casts, so their dependency
records are intrinsically inadmissible and their boundaries are not narrower.

## Structural and data-flow guards

`tools/checker_guards.py` parses SMT S-expressions and enforces:

1. exactly one top-level assertion, which must be the negated theorem, a
   closed allowlist of non-query commands, and exactly one terminal,
   argument-free `check-sat`;
2. the literal shared-input/shared-boundary implication and argument order;
3. six distinct theorem constants declared at the exact `Input`, `Boundary`,
   `Output`, `State`, `Output`, and `State` sorts, with all global constants
   outside these six rejected rather than allowed to bypass source/trust
   auditing;
4. defined `Requires_T`, `Boundary_T`, `Spec_T`, `Equivalent_T`, and target
   transition symbols with role-exact signatures, and rejection of any
   definition that closes over theorem constants not passed as formals;
5. `Spec_T` as an exact forwarding call to the target transition, excluding
   short-circuited, self-equal, or otherwise semantically dead calls;
6. a complete, nonempty, selector-and-sort-derived principal-observation
   schema for every `Output` and `State` field, with exact metadata agreement;
7. every metadata-listed source transition as a proper defined helper that is
   meaningfully reachable and directly and conjunctively determines at least
   one principal observation in the forwarded target definition;
8. an allowlisted, cited role for every uninterpreted dependency;
9. rejection of whole-target functionality functions or relations independent
   of symbol name or signature, including scalar UFs that determine a principal
   observation and relations whose call-site arguments carry principal output;
10. an exact match between every declared `Boundary` datatype field and cited
   backing metadata; schema-v3 evidence requires every field's backing to be
   covered by the declared admitted trust sites or source-backed replacement
   identities, and an excluded retained trust-site ID cannot back a boundary
   field;
11. meaningful, non-tautological use of every boundary field by both
   `Boundary_T` and the target transition;
12. interprocedural data-flow through reachable helper definitions, formal
   arguments, `let` bindings, and global theorem constants, with affine
   arithmetic normalized before dependency labels are assigned;
13. rejection of direct, reversed, helper-mediated, or `let`-mediated equality
   between principal observations and boundary-only data, including nominal
   input dependencies eliminated by subtraction or zero multiplication;
14. semantically guaranteed exact equality for every declared principal
    observation, rejecting dead or merely optional equality branches, unless a
    cited weak-equivalence review names both constructive witnesses; and
15. datatype-compatible logic plus a required clean Z3 replay of the emitted
    theorem template with the exact `unsat` result.

The guards reject renamed answer/trace fields by semantic role, not spelling.
They also reject obligations that merely define the expected symbols but do
not use the target definition.

## Classification vocabulary for the solver campaign

- `conditional-complete`
- `conditional-incomplete`
- `boundary-insufficient`
- `missing-source-backed-model`
- `checker-unsupported`
- `solver-unknown`

`conditional-complete` requires replayed `unsat`. `conditional-incomplete`
requires a concrete replayable `sat` witness satisfying the active contract
under one fixed boundary. Diagnostic SAT from an opaque abstraction is never
an incompleteness witness. The remaining labels distinguish boundary,
source-model, checker, and solver limitations.

## Target 081 bounded replacement boundary

The target-specific `sort_unstable_by` model excludes retained sites
`TS-081-D002`, `TS-081-D003`, and `TS-081-E001`; it does not relabel their
complete permutation-and-sortedness postcondition as an admissible boundary.
For three distinct input identities, `Boundary_T` contains only those identities,
the finite 3-by-3 results of the user comparator, and a state-preserving callback
transition delta from `TS-081-D004`. It contains no final sequence, selected
permutation/order, answer encoding, pivot/swap decision, or comparator-call trace.

`TargetDefinition_T` expands the active `slice_permutation` and
`slice_sorted_by_cmp` conjuncts. Permutation compares exact multiplicities for
every identity occurring in either sequence; sortedness expands all six
`i <= j` observations for a length-three slice. Reviewed equivalence preserves
the unit return, callback final state, exact output multiset, and position-wise
comparator-equivalence classes.

Three obligations are reported separately: exact final-slice equality, general
reviewed equivalence without a total-order precondition, and a total-order sanity
restriction. The first two require replayable SAT witnesses; the sanity check
requires clean UNSAT. This bounded contract-completeness model does not claim to
be a recursive implementation proof of ipnsort.

## Target 022 source-backed pointer transition

The target-specific `as_ptr_range` model excludes retained sites
`TS-022-D003`, `TS-022-D004`, and `TS-022-E001`. The first synthesizes a
null-provenance pointer whose address is the slice length; the latter two
supply an answer-equivalent range endpoint. The replacement boundary contains
only pre-existing input allocation bounds, data-pointer address and provenance,
element size and alignment, and target-platform isize/address limits.

`TargetDefinition_T` interprets the generated
`slice_ptr_range_starts_at_slice` predicate from the Rust source. The
slice-to-thin-pointer cast retains the input allocation, address, and
provenance. The `ptr::add` transition computes `len * size_of::<T>()` over
mathematical integers, requires isize fit and no address wrap, and retains
provenance. A nonzero byte offset additionally requires allocation provenance
and an in-allocation range that permits the one-past endpoint; an empty
non-ZST slice or a ZST slice may instead use a non-null, aligned dangling
pointer. Both endpoints and all final-state observations use exact equality.

The exact-output and full exact-state theorem negations must both replay as
clean UNSAT. SAT probes cover allocated and dangling empty non-ZST slices,
nonempty non-ZST slices, and allocated and dangling nonempty ZST slices.
Negative UNSAT probes reject a null data pointer and nonzero offsets without
allocation or provenance. The target evidence freezes the exact canonical
`ptr::add` implementation and its included safety documentation.

## Target 120 source-backed MaybeUninit copy transition

The target-specific `write_copy_of_slice` model excludes retained sites
`TS-120-D004` and `TS-120-E005`. The former combines lower raw-pointer
operations with the latter's answer-equivalent aggregate storage-effect lemma;
neither aggregate record is admitted or renamed. The replacement boundary
contains only the initial source slice, destination
`Uninitialized | Initialized(value)` cells, source/destination memory and
provenance, destination borrow identity, element/platform layout, and the
pre-existing outside-frame token.

`TargetDefinition_T` expands the canonical same-layout transmute,
equal-length `copy_from_slice` branch, `copy_nonoverlapping`, and
`assume_init_mut` path. The raw copy is an array map of the `Initialized`
constructor over source values: each destination slot becomes initialized
with the corresponding source value, without projecting a value from an
uninitialized destination cell. The source, destination identity, returned
reference identity, layout/provenance, and outside frame are preserved
exactly.

The exact-output and full exact-state theorem negations must both replay as
clean UNSAT. SAT probes cover empty, wholly uninitialized, mixed-initialization,
and fully initialized destinations. UNSAT probes reject unequal lengths,
partial copies, omitted initialization, wrong returned identity, changed
source values, and changed frame state. The evidence freezes the canonical
transmute, copy-from-slice, copy-nonoverlapping, and assume-init-mut source
spans.

## Target 052 source-backed unchecked disjoint-borrow transition

The bounded target-specific `get_disjoint_unchecked_mut` model uses two
`usize` indices `[0, 2]` over a length-three non-ZST slice. It excludes the
answer-bearing retained sites `TS-052-D004` and `TS-052-E001` rather than
admitting their complete fill-and-return postcondition as a boundary.
`Boundary_T` contains only initial receiver values, memory/provenance and
mutable-borrow identity, element layout/platform limits, and an outside-frame
token. It contains no validity bit, returned reference, MaybeUninit result,
alias map, canonical answer, final state, or trace.

The source model expands `usize::clone` as identity,
`SliceIndex<usize>::get_unchecked_mut` as in-bounds receiver-element
resolution, and the two loop iterations as explicit MaybeUninit slot writes.
The second write preserves the initialized first slot, both slots must be
initialized before `assume_init`, and the canonical source result is `[0, 2]`.
These source facts are exercised by positive and negative probes, but the
canonical result is deliberately absent from `Spec_T`.

`Spec_T` remains the generated unsafe precondition and final-length
postcondition plus Rust return-type well-formedness and disjointness. Both
literal theorem negations are therefore SAT. A fixed-boundary witness returns
well-formed disjoint arrays `[0, 2]` and `[1, 2]` with the same exact final
state; both satisfy the active contract while exact output and full exact
equivalence fail.

## Targets 019 and 021 source-backed slice casts

The target-specific `as_mut_ptr` and `as_ptr` models exclude retained sites
`TS-019-D001` and `TS-021-D001`. Those sites synthesize a pointer whose address
is the slice length and whose provenance is null; changing their labels would
not make them faithful models of the canonical casts. The replacement
transitions interpret `self as *mut [T] as *mut T` and
`self as *const [T] as *const T` directly: allocation identity, data address,
and provenance are retained from the input slice.

Every boundary field is bound to an explicit canonical-source replacement
identity (`SRC-019-CANONICAL-SLICE-TO-MUT-PTR` or
`SRC-021-CANONICAL-SLICE-TO-CONST-PTR`), not to the excluded synthetic site.
The schema-v3 checker requires each field backing to be covered by the
declared admitted/source-backed set and rejects any intersection with excluded
retained trust sites. Although the initial address and provenance equal those
of the returned pointer, they are pre-existing observations of shared input
`x`; `TargetDefinition_T` derives the output from `x`, never from boundary
value `b`.

Their shared boundaries contain only initial allocation bounds, address,
provenance, element layout, platform limits, and, for the mutable target, the
initial mutable-borrow identity and outside-frame token. Returned pointers,
final state, target truth, answer encodings, and traces are excluded. Exact
output compares allocation, address, and provenance. Full equivalence also
compares every modeled input/final-state field, including mutable identity and
frame state for `as_mut_ptr`.

Both theorem negations for each target must replay as clean UNSAT. Independent
SAT probes cover allocated nonempty non-ZST, allocated empty non-ZST, dangling
zero-byte non-ZST, allocated ZST, and dangling ZST slices. UNSAT probes reject
null and misaligned pointers, address-equals-length/null-provenance synthesis
on a discriminating input, changed allocation or provenance, and mutable
final-state changes. The evidence freezes the active declaration, canonical
Rust item and docs, retained harness and all three manifests, and the exact
canonical cast source.

`tools/run_pointer_cast_cluster.py` is the self-contained replay entry point.
It validates the delivered 62-row state, resets only the six result cells for
019/021/020, executes the dependency order 019 -> 021 -> 020, proves that no
other crosswalk cell changed, and records byte preservation for all eight
accepted baseline evidence trees.

## Target 020 source-backed mutable pointer range

The `as_mut_ptr_range` model composes only the newly source-backed target-019
cast transition through `TS-020-D002`; it does not import target 019's returned
pointer as a boundary observation. It excludes retained synthetic cast
`TS-020-D003`, answer-bearing endpoint dependency `TS-020-D004`, and external
body `TS-020-E001` rather than relabeling any of them.

Schema-v3 metadata binds `TS-020-D003` to
`SRC-020-CANONICAL-SLICE-TO-MUT-PTR` and binds `TS-020-D004` plus
`TS-020-E001` to `SRC-020-CANONICAL-MUT-PTR-ADD`. The checker requires the
replacement records to cover the excluded set exactly; neither replacement is
eligible as boundary-field backing, whose only admitted retained identity is
the source-backed `TS-020-D002` dependency.

The range transition computes the end with mutable `ptr::add` using
mathematical `len * size_of::<T>()` arithmetic. The valid domain requires a
non-null aligned start, isize fit, no address wrap, and, for nonzero byte
offsets, allocation provenance and an in-allocation range through the allowed
one-past endpoint. Zero-byte additions cover empty slices and ZSTs, including
aligned dangling inputs. Allocation and provenance are retained at both
endpoints, and mutable identity, the outside frame, and all receiver state are
unchanged.

Its exact-output and full exact-state theorem negations must both replay as
clean UNSAT. In addition to the five positive domain probes used for the cast
targets, rejection probes cover missing allocation or provenance for nonzero
offsets, out-of-allocation offsets, isize and address overflow, wrong start or
end endpoints, synthetic address/length-null/provenance output, and mutable
final-state mutation. The target-local evidence freezes the mutable
`ptr::add` implementation and its included add safety documentation.

## Targets 028, 030, and 065 source-backed search wrappers

The bounded length-two models for `binary_search`, `binary_search_by_key`, and
`partition_point` exclude retained answer-bearing delegations and result
bridges rather than admitting or relabeling them. Target 028 replaces
`TS-028-D002`, `TS-028-D003`, `TS-028-D004`, `TS-028-E001`, and
`TS-028-E003`; target 030 replaces `TS-030-D005`, `TS-030-D006`,
`TS-030-E001`, and `TS-030-E002`; target 065 replaces `TS-065-D002` and
`TS-065-E001`.

Each `TargetDefinition_T` calls a defined source-backed wrapper relation.
Target 028 expands the `Ord::cmp` adapter and uses the accepted
`binary_search_by` lower relation only under the active contract's ordered
domain. Target 030 expands per-element key extraction, key-to-search-key
`Ord::cmp`, callback state transitions, and the same reviewed lower relation.
Target 065 expands predicate observations and the predicate-to-Ordering
conversion (`true` to `Less`, `false` to `Greater`), invokes the reviewed
lower relation, and maps either Result tag to its index through the source
`unwrap_or_else(|i| i)` identity.

The shared boundaries contain only source element reads, comparator/key or
predicate observations, and per-call callback state deltas. They exclude a
selected index, returned `Result`, aggregate final callback state,
answer-equivalent encoding, and selected or complete execution traces.
`Requires_T` fixes only the bounded length and never adds sortedness or
partitioning.

For targets 028 and 030, reviewed equivalence keeps Result tags, Err indices,
and callback final state exact; distinct Ok indices are equivalent only when
both select matching duplicates. Their unrestricted obligations are SAT for
descending profiles, their ordered-domain sanity obligations are UNSAT, and
their exact-output obligations are SAT for duplicate matches. Target 065 uses
exact index and callback-state equivalence: non-partitioned `[false, true]`
profiles produce SAT witnesses, while the partitioned-domain sanity obligation
is UNSAT. Every SAT result has a fixed-boundary SMT model and an independent
contract replay.

`tools/run_search_family_cluster.py` validates the delivered state, resets
only the six result cells for 028/030/065, reruns those targets in order, and
records byte preservation for all 11 independently certified evidence trees.
The three experiment-local Verus source-transition models contain no
`external_body` and must each verify with zero errors.

## Targets 012, 014, 015, 023, and 024 strengthened chunk contracts

The chunk contract-drift cluster binds the active generated contracts rather
than the weaker retained contracts. It runs target 014
`as_chunks_unchecked` and target 015 `as_chunks_unchecked_mut` first, then
composes those defined lower transitions into target 012 `as_chunks`, target
023 `as_rchunks`, and target 024 `as_rchunks_mut`.

Targets 014 and 015 compose the independently accepted target-021 `as_ptr`
and target-019 `as_mut_ptr` allocation/address/provenance casts. Their
array-pointer casts preserve those observations, and their raw-slice
constructors enforce non-null alignment, one-allocation initialized storage,
isize fit, and address no-wrap. For target 015, `TS-015-D006` and
`TS-015-E002` remain excluded: fresh pointer-cast, array-pointer-cast,
raw-slice-construction, shared-storage/alias, and final-view projection
definitions replace them rather than relabeling their complete postconditions.

The upper targets calculate quotient and remainder explicitly. Target 012
uses front chunks/rear remainder; targets 023 and 024 use front
remainder/rear chunks. Every active initial length and subrange conjunct is
named separately. Mutable targets additionally retain both final lengths,
the exact concatenation frame, and every final subrange conjunct.

`Boundary_T` contains only initial allocation, address, provenance, element
layout, allocation extent, platform limits, borrow identity, and (for mutable
targets) frame identity. Returned references, front/rear ranges, final
storage, final views, answer encodings, and traces are excluded. The two
immutable targets and target 012 are conditional-complete for exact output
and full exact equivalence. Targets 015 and 024 are exact-output
conditional-complete but full-exact conditional-incomplete because their
active contracts permit distinct writes through the returned mutable views;
each SAT result has an independent fixed-input/fixed-boundary replay.

`tools/run_chunk_contract_drift_cluster.py` replays the targets in dependency
order, exercises empty and ZST inputs plus rejection of N=0, invalid
divisibility, null/misaligned/changed-provenance pointers, overflow, and
swapped partitions, and preserves all 14 previously certified evidence trees.
All five experiment-local Verus transition models have zero
`external_body` sites and must type-check and verify with zero errors.

## Targets 025, 026, and 119 source-backed MaybeUninit lifecycle transitions

The lifecycle cluster evaluates `assume_init_drop`, `assume_init_mut`, and
`write_clone_of_slice` against active contract SHAs
`ec9d059a1f66ae03009745a3d37edfc5306f2c23387856ea9aa3f52cfff09efe`,
`8d0e90b87ee12383ef38b353ff71f43a4136f565d0ae0f63651ee295c06f649a`,
and
`0e3746ad6530835f74de584a989ea1c6126fdb297454de35509cbdb05fd8c54b`.
Target 026 is modeled first as a layout-preserving raw mutable-slice cast;
target 119 composes that exact lower transition after its source-ordered
Clone/write loop. Target 025 separately expands the nonempty branch, raw
slice cast, slice drop glue, and one Destruct transition per element.

Retained answer-bearing sites `TS-025-D002` and `TS-025-E001`, plus
`TS-026-D002` and `TS-026-E001`, remain excluded and receive fresh
source-backed replacements. Target 119's retained Clone/write sites contribute
only one lower Clone/write observation at a time. `Boundary_T` contains only
initial storage and initialization, memory/layout/provenance/borrow/frame
identity, and individual Clone or Destruct observations. It excludes returned
references, resulting storage, aggregate final callback state, source-derived
operation order/count, answer encodings, and full traces.

All six literal theorem obligations use exact principal-return/final-state
equality. Targets 025 and 119 are conditional-complete for exact output and
full exact equivalence. Target 026 is exact-output conditional-complete but
full-exact conditional-incomplete: a fixed-input, fixed-boundary replay keeps
the same returned reference and initial values while two legal writes through
the returned mutable slice produce different final storage. Panic probes at
Clone positions 0, 1, and 2 derive Guard counts and initialized-prefix cleanup.
Additional fail-closed probes reject no-op, partial, duplicate, or out-of-order
writes/drops, wrong callback order/count/state, invalid initialization,
unequal lengths, pointer/layout/provenance faults, wrong identities, frame
mutation, omitted lower composition, and answer laundering.

`tools/run_maybeuninit_lifecycle_cluster.py` executes targets in order
026 -> 119 -> 025, retains every solver and Verus command/output/status,
independently replays all SAT evidence, preserves all 19 certified evidence
trees, changes only the two result fields for the three bounded rows, and
finishes with 22 classified and 40 `not-run` rows. All three experiment-local
Verus models contain no `external_body` and must type-check and verify with
zero errors.

## Targets 080 and 082 Ord-backed unstable-sort companions

Target 080 `sort_unstable` and target 082 `sort_unstable_by_key` bind active
contract SHAs
`877e37bea31dc31a92b85282f1d2f633c20aeb5391a5f1f02821cbfa0a09dd4b`
and
`019252db65344fd8830ffbbd90d127355a93541c6fbfab3fde3e6b3abe16e8ae`.
Their active contracts retain exact input/final identity multiplicities and
Ord- or extracted-key-sortedness. Rust's public docs permit equal elements to
reorder, while the `Ord` bounds and generated observation vocabulary supply
reflexive, dual, total, and transitive ordering laws.

The replacement boundaries admit only `TS-080-D003` for extensional
`Ord::lt` observations and `TS-082-D004` for extensional key extraction and
key `Ord::lt` observations. Answer-bearing sites `TS-080-D002` and
`TS-080-E001`, plus `TS-082-D002`, `TS-082-D003`, and `TS-082-E001`, remain
excluded. The boundary contains no final slice, chosen permutation, aggregate
final state, pivot/swap choice, answer encoding, comparison/key call trace, or
complete execution trace.

Each completeness obligation covers an arbitrary nonnegative slice length,
arbitrary identity multiplicities, and an arbitrary valid observation
position when nonempty; the empty case has no position at which the final
sequences can differ. It uses the order-statistic consequence of exact
permutation and sortedness: the shared input's count below/through the
observed Ord class brackets the same position in both executions. Total-order
separation makes different classes impossible at that position. The resulting
real solver result is UNSAT for completeness modulo reviewed
equal-Ord/equal-key equivalence. This is the classification proof; the
separate length-three UNSAT obligations are sanity evidence only.

Exact final-slice determinism is SAT for both targets. Concrete fixed-input,
fixed-boundary witnesses swap two distinct identities in one equal Ord/key
class while retaining unit return, exact identity multiplicities, callback
final state, and every non-tie class. Target-specific negative witnesses
reject foreign identities, unequal-class reordering, and callback/key-state
drift. Both experiment-local Verus models contain no `external_body` and prove
the arbitrary-length order-statistic contradiction plus the positive and
negative witness facts.

`tools/run_unstable_sort_companions.py` records every SMT and Verus command,
stdout, stderr, status, and replay model; preserves all 22 certified evidence
trees byte-for-byte; changes only rows 080 and 082; and finishes with 24
classified and 38 `not-run` rows.

## Target 077 source-backed selection method

Target 077 `select_nth_unstable` binds active contract SHA
`e570c36bf97546100d3408a95ea9c5f821ba0aed6ebe0e63ef6358d7d713fdaf`,
the exact generated declaration, Rust item and public docs, all four frozen
implementation-proof inputs, the private selection source, the lower
partition source, the `Ord` docs, the generated selection vocabulary, and all
five `TS-077` trust records.

`TS-077-D002` and `TS-077-E001` remain excluded; only `TS-077-D003` is
admitted for genuine
extensional `Ord` observations. `TS-077-D001` and `TS-077-C001` remain
context-only. The experiment-local replacement explicitly models the
source-reachable bounds, zero-sized-type, minimum/maximum, swap, partition,
recursive-loop/fallback, and final returned-subslice transitions. No pivot,
selected permutation, final state, answer encoding, or complete trace enters
`Boundary_T`.

The arbitrary-length shared-input/shared-boundary theorem is UNSAT modulo a
selection equivalence cited to core/src/slice/mod.rs:3461-3513 and
core/src/slice/sort/select.rs:17-307. It preserves returned range identities
and lengths, whole-input identity multiplicities, pivot rank and `Ord` class,
side-class multiplicities, allocation and mutable-borrow identity, and final
length. It relaxes only documented unsorted side ordering and equal-class
pivot identity. A fixed-input exact theorem and replayable model are SAT:
both executions satisfy every active contract conjunct while ordering the two
sides differently. Positive side-reordering and equal-pivot witnesses, plus
negative foreign-identity, wrong-rank/class, partition-crossing,
malformed-range, and state-drift witnesses, are solver- and semantically
replayed.

`tools/run_target_077.py` retains exact SMT/Verus commands, stdout, stderr,
status, and models; verifies a five-obligation target-local Verus model with
zero errors and no `external_body`; preserves all 24 certified evidence trees
and all frozen selection inputs; changes only row 077's two result fields;
leaves rows 078 and 079 `not-run`; and finishes with 25 classified and 37
`not-run` rows.

## Targets 078-079 bounded callback model and source-model gap

Targets 078 `select_nth_unstable_by` and 079
`select_nth_unstable_by_key` bind active contract SHAs
`8d197563a2e9735beef3c52ff46ea5d3dd44da47b48e3b199654cf3c667490d7`
and
`9366859a88badc5f8d8cdfb15fbc544ef81edb756429e14a887b1ce6c73e3e95`.
Each evidence tree binds its exact generated declaration, canonical source
item and public docs, frozen harness and three manifests, private introselect
and lower partition source, callback vocabulary, and all six trust records.

`TS-078-D001`/`TS-079-D001` and `TS-078-C001`/`TS-079-C001` remain
context-only. Only `TS-078-D004` and `TS-079-D004` back genuine callback
observations. The bounded obligations model the closure adapters represented
by `TS-078-D002`/`TS-079-D002`. The answer-bearing whole-selection
dependencies `TS-078-D003`/`TS-079-D003` and external bodies
`TS-078-E001`/`TS-079-E001` remain excluded and unresolved; they are not
relabeled or claimed as source-replaced.

The shared boundary contains callback identity, initial callback-visible
state, and source-step relations over arguments, result, next state, and
panic. It contains no realized invocation trace or count, pivot, selected
permutation, returned range, final callback state, final slice, or answer
encoding. Target 078 executes exactly one `compare(a,b)` step followed by
equality with `Ordering::Less` at each adapter invocation and assumes no
comparator totality. Target 079 executes `f(a)`, then `f(b)`, then
`Ord::lt`, threading all intermediate states without assuming a pure or
stable key extractor.

The source-backed portion is deliberately bounded to a non-ZST length-four,
index-one insertion-sort execution. It derives tails one, two, and three from
the canonical loop advance, threads every callback/key/`Ord::lt` state, and
models each intermediate rotation. Panic reachability uses the same adapter
definitions and the frozen `CopyOnDrop` guard semantics, so a first comparison
panic leaves the slice unchanged and a later panic restores the moved element
at the current gap. All six active contract conjuncts, callback-visible final
state, exact returned references, final slice, allocation/borrow identity,
and panic status remain explicit.

The two bounded theorem negations are UNSAT and have SAT nonvacuity/source
executions. Permanent regressions reject one- and two-adapter all-equal
length-four traces while admitting the source-required three adapters; they
also reject wrong descending, mixed, and both tail-three insertion results,
exercising every length-four rotation and the shift loop's off-by-one
behavior. A SAT/UNSAT pair pins gap-guard restoration after a later panic.
Source-coupled SAT probes cover the comparator panic and each first-key,
second-key, and `Ord::lt` panic prefix.

No operational relation derives arbitrary-length `choose_pivot`, lower
partition mutation and callbacks, ancestor-pivot handling, introselect
narrowing, the 16-step median-of-medians fallback, or their panic prefixes.
Target 079 also does not model temporary key `Drop` order, callback-visible
state, or panic.
Putting a realized schedule in `Boundary_T` remains forbidden, but absence of
an internal source execution is a model gap rather than a boundary result.
Both result columns for both targets are therefore
`missing-source-backed-model`, not `boundary-insufficient`.

`tools/run_selection_callback_cluster.py` retains exact solver and Verus
commands, stdout, stderr, status, and models; verifies two five-obligation
all-equal length-four Verus schedule models with zero errors and no
`external_body`;
preserves all 25 certified evidence trees and every frozen selection input;
changes only rows 078-079's result fields; and finishes with 27 classified
and 35 `not-run` rows.

### Target 078 arbitrary-range `insert_tail`/`CopyOnDrop` refinement

The additive target-078 v3 package isolates the Rust 1.96 `insert_tail`
helper and its one-element `CopyOnDrop` guard. Its only semantic inputs are
the accepted comparator boundary, a pre-call sequence and callback state,
valid `begin` and `tail` indices, and the identities already present in that
sequence. It accepts no terminal result, selected output, final state, answer
encoding, or callback trace. The first callback precedes the tail move; each
later callback uses the current pre-call callback state; normal and panic
stops restore the temporary at the current gap; and panic propagation retains
the callback next state.

`proofs/078_core_slice_select_nth_unstable_by_insert_tail_refinement_v3.rs`
constructively proves no-shift, initial-comparison panic, repeated shifts,
normal and panic restoration, insertion at `begin`, callback-state retention,
sequence length, identity multiplicity, and the frame outside the affected
range. Verus reports 14 verified obligations and no errors without
`external_body`, assumptions, admits, or axioms.

The parsed Verus expression AST is translated to SMT and compared field by
field with retained `ExactInsertTailLoop` and `ExactInsertTail`. The arbitrary
loop step guards its induction hypothesis with `sift > begin`, discharges the
`sift == begin` base directly, and then lifts the loop result to the source
entry. The correspondence replays UNSAT. The SMT array encoding is total; the
fresh sequence-length symbols express the in-range side condition but are not
selectors of `ExactState`, so the correspondence proves the transition for
all arrays at valid indices. Ten source mutations cover operand order, lookup
state, shift source and destination, gap advancement, normal/base/panic
restoration, callback next state, and panic propagation. Every mutation is
rejected by Verus and independently makes correspondence SAT.

Retained SAT models exercise no shift, a two-shift normal stop, insertion at
`begin`, and panic after a shift. `path_policy_v2.json` registers the closed v3
evidence scope while binding unchanged `path_policy_v1.json`; it also owns
the additive lane for the pending v3 review. The canonical review artifact is
`review/REVIEW_ADDENDUM_TARGET_078_INSERT_TAIL_REFINEMENT_V3.md`, and v2
admits only direct `review/*TARGET_078_INSERT_TAIL_REFINEMENT_V3*.md` files.
`tools/run_acceptance.py` runs the v3 producer before policy consumers. If an
intentional tool-output change requires resealing, run
`python3 tools/run_target_078_insert_tail_refinement_v3.py
--allow-unregistered-evidence`, then
`python3 tools/preservation_policy_v2.py --write`, and finally rerun the
package.
The accepted classifications and stage remain unchanged; independent review
is pending.

## Targets 032, 036, 069, 074, 076, 093, and 098 mutable iterator constructors

The constructor cluster binds the exact active declarations, canonical public
wrappers/docs, frozen implementation-proof harnesses and all three manifests,
shared iterator vocabulary, canonical private constructor bodies, and every
trust record for `chunk_by_mut`, `chunks_mut`, `rchunks_mut`, `rsplit_mut`,
`rsplitn_mut`, `split_inclusive_mut`, and `split_mut`. The frozen
`TS-076-C003` record and its `core/src/slice/iter.rs:1223-1225` citation remain
unchanged. Experiment-local derived evidence reconciles that stale location to
the assigned canonical `RSplitNMut::new` at
`core/src/slice/iter.rs:1289-1293`.

Every obligation uses an arbitrary nonnegative slice length and element size,
so empty, nonempty, and ZST inputs stay in scope. The `chunks_mut` and
`rchunks_mut` transitions require a positive chunk size and preserve raw
address, allocation, provenance, fat-pointer length, mutable-borrow marker,
and element layout; they differ only in source-backed direction. In
particular, the modeled identity is the raw address, allocation, provenance,
and mutable-borrow identity. `chunk_by_mut` stores the complete mutable slice
and adjacent predicate. `split_mut` stores the slice and predicate with
`finished=false`; `rsplit_mut` nests that transition and sets reverse
direction; `rsplitn_mut` additionally follows `RSplitNMut::new` and stores
`count=n`; `split_inclusive_mut` sets inclusive direction and
`finished=slice.is_empty()`. All callback-bearing constructors perform zero
constructor-time callback calls.

`Boundary_T` contains only the input address, allocation, provenance,
mutable-borrow and element-layout observations, plus callable identity where
applicable. It contains no iterator result/private state, selected range,
callback result, final state, direction/default, answer encoding, or trace.
Every view, raw pointer, predicate state, direction, count, inclusive/finished
default, and immediate final-state observation is derived by defined
source-backed transitions and compared with exact equality.

For each target, both the exact-output and full exact-state shared-input,
shared-boundary theorem negations are clean UNSAT. Three retained SAT source
instances per target cover empty non-ZST, nonempty non-ZST, and nonempty ZST
inputs. The seven generated target-local Verus models type-check and verify
with zero errors and no `external_body`. Therefore all seven targets are
`conditional-complete` in both result columns.

`tools/run_mutable_iterator_constructors.py` retains all 14 theorem files,
21 source-instance files, exact solver/Verus commands and captures, and
independent solver replays. Its atomic run preserves all 27 certified evidence
trees, all seven frozen input trees, and every non-result crosswalk field,
changes only the fourteen result cells for the selected rows, and finishes
with 34 classified and 28 `not-run` rows. Independent review remains pending;
the runner does not invoke a stage transition.

## Targets 091, 097, 101, and 103 mutable edge extraction

The mutable-edge cluster binds the active declarations, shared split-off
vocabulary, canonical source items and public docs, frozen implementation
harnesses, all three proof manifests, and all eight trust records for
`split_first_mut`, `split_last_mut`, `split_off_first_mut`, and
`split_off_last_mut`. The direct targets encode the exact empty/nonempty
slice-pattern branches. The split-off wrappers encode the ordered
`mem::replace(self, &mut [])`, first/last split, receiver reassignment, and
return transitions rather than trusting a whole-target relation.

`Boundary_T` fixes only the input address, allocation, provenance,
mutable-borrow identity, and element size. For the wrappers it additionally
fixes the identity of the pre-result empty-slice literal consumed by
`mem::replace`; that lower source observation is propagated through explicit
replace, split, and assignment states and is not a final receiver or answer
encoding. Result tags, selected indices/ranges, returned references, final
receiver/storage, and traces remain excluded. The boundary is therefore
narrower than each target.

All selected indices, structural mutable-reference identities, first/tail or
init/last ranges, receiver slots, and immediate backing storage are
source-derived. Range disjointness is index-based, so ZST references may share
an address while retaining disjoint ranges. Exact equality covers every
principal return/reference field and, for the full theorem, every receiver
and immediate final-frame field.

Both theorem negations are clean UNSAT for each target. Six SAT source
instances per target cover empty, singleton, and longer slices for both ZST
and non-ZST layouts. Four target-specific Verus models encode the pattern or
ordered wrapper transitions and verify without `external_body`.
`tools/run_mutable_edge_extraction.py` retains exact solver and Verus
commands/captures, independent replay, all 34 certified evidence trees, and
the complete frozen-input tree. It changes only the eight selected result
cells and finishes with 38 classified and 24 `not-run` rows. Independent
review remains pending and stage transition is disabled.

## Targets 037 and 043 clone-effect transitions

The clone-effect cluster binds active contracts
`a0fab9b11562f51ba66aa30d496a750f79f0e0b691e4d3e75051a847547033f5`
and
`7772c35bc8a2e714a53e79384d43b99e96daae6650124087e508e2542ceb3f38`,
the generated declarations, relation-valued `cloned<T>` vocabulary, public
source/docs, private helper and specialization bodies, frozen implementation
harnesses/manifests, and all 22 audited trust records.

`Boundary_T` admits initial storage/identity/layout plus individual Clone
arguments, relation-valued results, outcomes, and callback state transitions.
For target 043, Miri remains platform input and
`is_val_statically_known` on `value` is the sole hidden intrinsic observation.
Aggregate destination storage, final callback state, operation order/count,
selected specialization, answer encodings, and traces remain excluded.

Target 037 derives the default increasing-index `CloneFromSpec` loop and the
type-selected `TrivialClone` nonoverlapping-copy path. Both unequal-length
paths panic before a callback or write. Target 043 derives the empty/nonempty
default split-last loop, every Clone transition, and the move of fill's
original value into the final slot. It also derives the `TrivialClone`
`ptr::read` loop, `u8`/`i8` `write_bytes`, and every integer
Miri/static-known/uniform-byte fast-path-or-loop branch. Specialization is
fixed by input type rather than admitted as a free observation.

The integer intrinsic count follows Rust's left-to-right short-circuit
control flow. `is_val_statically_known` is called once unless the Miri
long-slice condition succeeds first; `write_bytes` adds one call on a
uniform-byte fast path. The resulting totals are 2 for static-known uniform,
1 for static-known nonuniform, dynamic loop, Miri-short loop, and Miri-long
uniform, and 0 for Miri-long nonuniform. A fail-closed probe also confirms
that the former selected-path-only count is inconsistent with the first four
rows.

Generic Clone results may differ from their source values while satisfying
the active relation. The source fold derives callback order/count, state
chaining, write order/count, intrinsic and assignment counts, final storage,
and final callback state. Arbitrary panic-prefix obligations include all
completed calls plus the failing element's unwind-visible partial value.

Four normal theorem negations, two arbitrary panic-prefix theorem negations,
and one unequal-length theorem negation are clean UNSAT. Twenty-seven
source-path, six bounded panic-prefix, and two mismatch witnesses are SAT with
retained models; ten negative probes are UNSAT. Both target-local Verus models
verify with zero errors and no `external_body`.
`tools/run_clone_effect_cluster.py` preserves all 38 certified evidence trees
and the complete frozen-input tree, changes only rows 037 and 043, and finishes
with 40 classified and 22 `not-run` rows. Independent review remains pending
and stage transition is disabled.

## Targets 035 and 068 exact mutable iterator partitions

Targets 035 `core::slice::chunks_exact_mut` and 068
`core::slice::rchunks_exact_mut` bind active contract SHAs
`c4e09211e598b511902feb1f0fd0207e386dd8e7077da17462c9ba20c1944c68`
and
`64f0260c2044e5b2b440a7c66eb354d3685862070f8ad8979838a571fbe47afe`.
Each tree retains the generated declaration and shared iterator vocabulary,
canonical public item/docs and private constructor body, frozen implementation
harness and three manifests, and all six audited trust records.

Both source transitions require a nonzero chunk size and derive
`len % chunk_size`. The forward constructor splits at `len - rem`, stores the
divisible prefix in raw `v`, and stores the suffix remainder as the unique
reference. The reverse constructor splits at `rem`, stores the divisible suffix
in raw `v`, and stores the prefix remainder. This fixes the opposite
concatenation orientations, empty yielded prefix, direction, chunk size,
private modulo/split state, and immediate unchanged backing state.
Thus the reviewed arithmetic names are the forward split at `len - rem` and
the reverse split at `rem`.

`Boundary_T` contains only the initial address, allocation, provenance,
mutable-borrow identity, and element layout. Remainder arithmetic, split index,
partition ranges and orientation, returned/private iterator state, raw-v and
remainder identities, direction, outputs, final state, and traces are derived
rather than fixed. Allocation and provenance are preserved for both regions;
parent borrow identity is preserved structurally. Disjointness is range-based
so zero-sized nonempty regions may have equal addresses. This is the reviewed
range-based ZST disjointness rule.

Both literal shared-input/shared-boundary theorem negations are UNSAT per
target under exact equality for every iterator, region/reference identity,
private-state, and immediate final-state observation. Twelve SAT source
instances cover empty, unit-chunk, shorter-than-chunk, divisible,
nondivisible, and ZST equal-address cases. Sixteen UNSAT negative probes reject
zero chunk size, incorrect modulo/split/orientation/concatenation, provenance
or borrow loss, and unequal ZST-derived addresses. Checker regressions reject
omitted contract conjuncts, weakened equality, answer-bearing or laundered
boundaries, mismatched boundaries, and out-of-scope ledger mutation.

`tools/run_exact_mutable_iterator_partitions.py` retains exact SMT, metadata,
solver commands/stdout/stderr/status, SAT replay models, independent replay,
and two target-specific Verus files that type-check and verify with zero errors
and no `external_body`. Its atomic run preserves all 40 certified evidence
trees and all 320 frozen inputs by readable content, changes only rows 035 and
068's result fields, and finishes with 42 classified and 20 `not-run` rows.
Independent review remains required and stage transition is disabled.

## Targets 062, 090, and 096 mutable fixed-chunk edges

Input orders 062 `core::slice::last_chunk_mut`, 090
`core::slice::split_first_chunk_mut`, and 096
`core::slice::split_last_chunk_mut` bind active contract SHAs
`32a4497f959b05a42448f7ea2a070f4e3635c1b46d5c08628772d7601f9f9e57`,
`eb599a67a0f7b786e404c9b3f97181b56e9b01bb82f3cc21822b93d2d46ab950`,
and
`0c9131cd588a99217fc333ad32e54ac62deaf95cfc245fffb3523ba683296ce5`.
Each evidence tree binds its exact generated declaration, shared fixed-array
vocabulary, canonical public item/docs and lower split/pointer helpers, frozen
implementation harness and three manifests, and its complete share of the 22
audited trust records.

`Boundary_T` contains only the initial non-null slice address, allocation,
provenance, unique parent-borrow identity, and element size. `N` is part of
the shared input `x`. Branch results, subtraction and split indices, ranges,
array views, tuple orientation, returned references, derived borrows, output,
final state, answer encodings, and traces are excluded.

The source transition returns `None` exactly when `N > len`. The last and
split-last targets derive `index = len - N` through checked subtraction; the
split-first target derives the checked split at `N`. The canonical mutable
raw-parts split constructs `[0,index)` and `[index,len)`, preserving
allocation, provenance, layout, and parent borrow. The selected region then
flows through the canonical slice `as_mut_ptr` cast, `cast_array`, and mutable
dereference transitions. This replaces row 090's retained
null-provenance/length-address pointer model rather than trusting it. Array
length is checked before conversion, and tuple orientation is array-only,
array-first, and array-second respectively.

Reference identity is structural over address, allocation, provenance, parent
borrow, element range, layout, and projection. Prefix/suffix disjointness is
range-based, so nonempty ZST regions may have equal addresses. The immediate
final frame preserves both regions and composes them in canonical order.
Exact equivalence compares every principal return/reference identity and every
modeled final-state observation; the exact-output projection omits only state.

Six theorem obligations are clean UNSAT. Twenty-one SAT source instances with
retained models cover empty `N=0`, empty positive `N`, `N=0` on nonempty input,
`N > len`, `N = len`, strict interior splits, and nonempty ZST equal-address
regions. Thirty UNSAT semantic probes reject wrong branching/arithmetic,
swapped ranges or tuple order, unchecked array length, synthetic provenance,
allocation or borrow loss, address-based ZST disjointness, and missing final
frame composition. Structural guards additionally reject omitted contract
conjuncts, weakened equality, answer-bearing or laundered boundaries,
mismatched boundaries, and out-of-scope ledger edits.

`tools/run_mutable_fixed_chunk_edges.py` retains exact commands, SMT, metadata,
stdout, stderr, statuses, SAT models, independent replay, and three
target-specific trusted-free Verus models. Its atomic run preserves all 42
certified evidence trees and all 320 frozen inputs by readable content, changes
only the two result fields on rows 062, 090, and 096, and finishes with 45
classified and 17 `not-run` rows. Independent review remains required and
stage transition is disabled.

## Targets 085 and 086 source-backed mutable split primitives

Input orders 085 `core::slice::split_at_mut_checked` and 086
`core::slice::split_at_mut_unchecked` bind active contract SHAs
`f545d70fd2f00566e6847d457980a532ef48cdc82fe2e12eba1be9ccff4aebd6`
and
`dfe96dd890e058e02f390e85bdfce250a48823c9e43c15ad599961b2f28f2da9`.
Each target tree retains the exact generated declaration, shared
`split_point_in_range` vocabulary, canonical public item and docs, lower
`as_mut_ptr`, `ptr::add`, `unchecked_sub`, and `from_raw_parts_mut` source and
safety text, all four frozen implementation-proof artifacts, and its complete
share of the 18 audited trust records.

The source model replaces, rather than relabels, answer-bearing records
`TS-085-D002`, `TS-085-E002`, `TS-086-D005`, and `TS-086-E002`. The checked
target derives `Some` exactly when `mid <= len` and preserves the parent frame
on `mid > len`. The unchecked target admits only the generated and documented
`mid <= len` domain. Both then derive the canonical slice-to-thin mutable
pointer cast, `ptr.add(mid)`, `unchecked_sub(len, mid)`, raw slices
`[0,mid)` and `[mid,len)`, structural mutable-reference identities, unique
derived borrows, and immediate left-then-right final-frame composition.

`mid` belongs to shared input `x`. `Boundary_T` contains only the initial
non-null address, allocation, provenance, unique parent-borrow identity,
element size, and element alignment. It contains no branch result, domain
decision, pointer-add result, subtraction, region, borrow, output, final
state, answer encoding, or trace. The former synthetic length-as-address and
null-provenance pointer construction is rejected. Reference identity is exact
over values, logical range, address, allocation, provenance, parent borrow,
layout, side projection, and uniqueness. Range-based disjointness admits
nonempty ZST equal-address regions.

Both literal shared-input/shared-boundary theorem projections are clean UNSAT
for each target. Eleven SAT source instances retain models for `mid = 0`,
`mid = len`, strict interior splits, the checked `mid > len` branch,
one-past-end right pointers, and nonempty ZST equal-address regions. The
unchecked out-of-domain instance is rejected and replayed as UNSAT.
Twenty-three UNSAT semantic probes reject branch inversion, off-by-one split
or subtraction, swapped regions, pointer/allocation/provenance/borrow loss,
address-only disjointness, missing or reversed final frames, and the invalid
unchecked domain. Structural guards additionally reject omitted active
contract conjuncts, weakened equality, answer-bearing or laundered
boundaries, mismatched boundaries, and out-of-scope ledger changes.

`tools/run_split_at_mut_primitives.py` retains exact commands, SMT, metadata,
stdout, stderr, status, SAT models, independent replay, and two target-specific
Verus models with no trusted bodies. Its atomic run preserves the 45-target
baseline and all 320 frozen inputs by readable content, changes only rows 085
and 086's two result fields, and finishes with 47 classified and 15 `not-run`
rows. Independent review remains required and stage transition is disabled.

## Targets 099 and 104 source-backed split-off pair

Input orders 099 `core::slice::split_off` and 104
`core::slice::split_off_mut` bind active contract SHAs
`980c0fc48d42c16666be982fb8949777aea4c339d73a52ba80f62fded2ae7085`
and
`74829510395c909f4449ed0dd06a0ac44332151e2a9d1feba392c5728e616e99`.
Each target tree retains the exact declaration, split-off vocabulary, public
source/docs, canonical one-sided-range and split helpers, all four frozen
implementation-proof artifacts, and its share of all nine audited trust
records (`TS-099-D001` through `TS-099-C001` and `TS-104-D001` through
`TS-104-C001`) by readable content.

Range kind and index remain in shared input `x`. The shared boundary contains
only initial address, allocation, provenance, parent-borrow identity, element
size, and element alignment. Direction, split index, overflow/bounds results,
front/back or returned/remaining regions, derived borrows, output, final
state, answer encodings, and traces are excluded.

The source transition derives StartInclusive-to-Back, End-to-Front, and
EndInclusive checked addition with overflow-to-None. It rejects
`split_index > len` without changing the receiver, constructs exact
`[0,split_index)` and `[split_index,len)` regions, and applies the canonical
directional return/reassignment. The mutable model additionally derives
`mem::take` ownership transfer, the temporary empty receiver, disjoint unique
split borrows, and ordered front-then-back frame composition. One-past and ZST
equal-address behavior retain logical range and projection identity.

The mutable active declaration is evaluated literally. Both its initial
returned-slice partition and active final-return partition clause remain live.
The frozen harness and transformation manifest are retained as negative
provenance for the corrected contract, but their deletion of
`final(ret.unwrap())@` is never substituted into the obligation.

Exact-output equivalence compares every principal option/reference-identity
field. Full equivalence additionally compares every helper, ownership,
region, borrow, receiver, and ordered final-frame observation. Four theorem
negations are clean UNSAT. Twenty-eight SAT source instances with retained
models cover empty, zero, interior, len, out-of-bounds, EndInclusive-len,
`usize::MAX`, one-past, and nonempty ZST cases. Twenty UNSAT semantic probes
reject direction reversal, wrapping addition, altered bounds, off-by-one
splits, swapped branches, changed None frames, identity/borrow loss, reversed
frames, and final-return drift. Structural guards reject removal of the
active final-return clause, weakened equality, answer laundering, mismatched
shared inputs/boundaries, and out-of-scope ledger edits.

`tools/run_split_off_pair.py` retains exact SMT/Verus commands, stdout,
stderr, statuses, SAT models, and independent replay. Both target-specific
Verus models contain no trusted bodies. The atomic run preserves all 47
certified evidence trees and all 320 frozen inputs by readable content,
changes only rows 099 and 104's result fields, and finishes with 49 classified
and 13 `not-run` rows. Independent review remains required and stage
transition is disabled.

## Targets 048 and 049 source-backed raw slice constructors

Input orders 048 `core::slice::from_raw_parts` and 049
`core::slice::from_raw_parts_mut` bind active contract SHAs
`73ec9d9cba07629dcf152cde202578a52cea87134075f0568244d747a3183769`
and
`47e90942a15f2cdb0e6584968eedeeb627353ed37da324f1af080c3917f0dc40`.
Each target tree retains its generated declaration, the shared raw-domain
vocabulary, canonical source item and public safety documentation, all four
frozen implementation-proof artifacts, and its three audited trust records
by readable content. `TS-048-D001` and `TS-049-D001` remain context-only
vocabulary. Answer-bearing `TS-048-D002`/`TS-048-E001` and
`TS-049-D002`/`TS-049-E001` remain inadmissible and are replaced rather than
relabeled.

The literal theorem uses one shared input `x` and one shared boundary `b`.
`Boundary_T` contains only genuine initial address-indexed memory,
allocation/provenance and one-allocation facts, initialization, alias
permissions, element layout, platform limits, and root borrow/frame
observations. It excludes returned references or sequences, raw fat-pointer
results, final storage, answers, and traces. Explicit source transitions
model the UB precondition, raw fat-pointer construction, and reference
dereference. They derive initial memory, length, allocation, address,
provenance, borrow, and mutability pointwise from pointer-reachable memory.

The domain includes allocated nonempty slices; allocated and non-null aligned
dangling empty slices; allocated and dangling nonempty ZST slices whose
endpoints equal their starts; initialized values; one-allocation bounds;
shared no-mutation and mutable exclusivity; isize multiplication fit;
address no-wrap; and permitted one-past endpoints. Negative probes reject
null or misaligned empty/ZST pointers, missing allocation/provenance for
nonzero spans, multi-allocation and out-of-allocation spans, uninitialized
elements, alias violations, overflow, wrong return/reference fields, state
identity drift, and boundary mismatch. Exact-AST tests reject removed helper
transitions, answer laundering, weakened equality, mismatched theorem
variables, invented mutable final frames, and out-of-scope ledger edits.

Target 048's exact-output and full-state theorem negations are clean UNSAT.
Target 049's exact-output theorem negation is clean UNSAT. Its full-state
theorem is SAT because the active contract has no final returned-memory
clause; an independently replayed fixed-input/fixed-boundary witness fixes
identical initial returns while varying only final in-range memory. This
classifies target 048 conditional-complete for both projections and target
049 exact-output conditional-complete/full-state conditional-incomplete
without inventing a final-frame assumption.

`tools/run_raw_slice_pair.py` retains all four theorem obligations, fourteen
SAT source instances with models, fifty-four UNSAT negative probes, the fixed
SAT incompleteness witness and model, exact commands/stdout/stderr/statuses,
independent replay, and two trusted-free Verus models. Its atomic run
preserves all 49 certified evidence trees and all 320 frozen inputs by
readable content, changes only rows 048 and 049's result fields, and finishes
with 51 classified and 11 `not-run` rows. Independent review remains
required and stage transition is disabled.

## Targets 053 through 055 explicit SliceIndex transitions

Input orders 053 `core::slice::get_mut`, 054
`core::slice::get_unchecked`, and 055
`core::slice::get_unchecked_mut` bind active contract SHAs
`87a9796fc553d16e3e75cfe5ea9196e6482c5088d278a2f10112c31107e74f9c`,
`71eedef5ee0aa574329fe132e65757563db0764095f5cc5dbdf2911acc0b4aad`,
and
`ec6f48bf7b072e49afdad4bacb69dc2288ec2047621c339df4614e01b612903f`.
Each target tree retains its generated declaration, opaque SliceIndex
vocabulary, canonical public wrapper and documentation, the complete Rust
1.96 `slice/index.rs` and `index.rs` implementation sources, all four frozen
implementation-proof artifacts, and all eight audited trust records by
readable content.

`TS-053-D002`, `TS-054-D001`, and `TS-055-D001` remain context-only
specification vocabulary. Answer-equivalent `TS-053-D001`, answer-bearing
`TS-054-D002` and `TS-055-D002`, and complete-target external sites
`TS-054-E001` and `TS-055-E001` remain inadmissible. They are replaced rather
than relabeled by explicit bounds decisions, pointer offset and raw-pointer
construction, allocation/address/provenance preservation, reference
dereference and well-formedness, root-borrow identity, and mutable or
immutable frame transitions. No SMT obligation declares an opaque function.

All obligations use one shared valid input `x` and one shared boundary `b`.
`Boundary_T` contains only initial receiver memory, allocation/address/
provenance, root-borrow identity, one-allocation facts, alias permissions,
element layout and platform limits, and a pre-existing outside-memory frame
token. It excludes returned references and option discriminants, normalized
or selected indices, raw pointer results, final receiver memory, canonical
answers, target truth, and traces.

Target 054 faithfully expands `slice_index_result` through all 25 applicable
sealed Rust 1.96 `SliceIndex<[T]>` forms: `usize`, `IndexRange`, both old and
new range families, the bound pair, all supported `Clamp` wrappers, and
`Last`. Its exact-output and full-state theorem negations are clean UNSAT, and
each form has a retained SAT source instance with its normalized start, end,
reference kind, address, and provenance. The source-selected result is not
placed in the boundary.

Targets 053 and 055 use the concrete valid `usize` index zero over the same
length-three non-ZST slice. Their active mutable-frame contracts do not bind
returned-reference identity. For each target, both the canonical element-zero
reference and a distinct well-formed element-one reference satisfy the active
contract under the same boundary and exact same final state. Both exact-output
and full-state theorem negations, plus both fixed reference witnesses, replay
SAT. The canonical source result is retained as a diagnostic transition but
is deliberately not conjoined to `Spec_T`.

`tools/run_slice_index_trio.py` retains six theorem obligations, 27 SAT source
instances with models, twelve UNSAT negative probes, two concrete SAT
reference witnesses, exact commands/stdout/stderr/statuses, independent
replay, and three trusted-free Verus models. Its atomic run preserves all 51
certified evidence trees and all 320 frozen inputs byte-for-byte, changes only
rows 053 through 055's result fields, and finishes with 54 classified and 8
`not-run` rows. Independent review remains required and stage transition is
disabled.

## Targets 039 and 111 source-backed address observers

Input orders 039 `core::slice::element_offset` and 111
`core::slice::subslice_range` retain active contract hashes
`6cb1971fc22b193456b858636b8e9d6ed1874cc9b7b9352f94eea2cf2a66960b`
and
`efa221cefc2e3ffa897082292c658fd9163e1e151be34c08189360d0b01729bb`.
The generated declarations, Rust 1.96 source and public docs, frozen
implementation-proof harnesses, all proof manifests, and all 27 audited trust
records are bound by hash and readable content.

The retained answer-bearing sites `TS-039-D006`, `TS-039-E003`,
`TS-039-E004`, `TS-039-E005`, `TS-111-D006`, `TS-111-E002`,
`TS-111-E003`, and `TS-111-E004` remain inadmissible. They are replaced,
not relabeled, by defined transitions for receiver pointer extraction,
`ptr::from_ref` or subslice pointer extraction, exposed addresses,
machine-usize wrapping subtraction, element-stride alignment, offset
division, wrapping range-end addition, exact bounds decisions, the documented
ZST panic, and algebraic `None`/`Some` construction. The generated
normal-return implications remain literal; no canonical answer is conjoined
outside them and no SMT function is uninterpreted.

The shared input contains only target lengths and initial memory identity.
`Boundary_T` contains only initial addresses, allocation identities and
extents, provenance, liveness, element size/alignment, and usize/isize
platform limits. It excludes computed offsets/ranges, branch truth, panic or
option outputs, final state, answer encodings, and traces. `Requires_T` adds
no semantic target precondition: it only states nonnegative integer encodings
for Rust lengths and the initial-memory token. Rust reference validity,
including non-null alignment and non-wrapping live spans, is checked in the
shared boundary.

Both equivalence projections use exact algebraic return equality. The full
projection additionally uses exact equality for the unchanged memory token.
The required source cases cover same-allocation starts/interiors, distinct
allocations, element-stride misalignment, pointer-before-receiver wrapping,
exact-end and later out-of-bounds pointers, machine-usize limits, invalid
pointer/reference conditions, and ZST panic behavior. Target 111 additionally
retains positive models for the two documented distinct-allocation empty
subslice false positives at receiver start and end; those address collisions
remain deterministic under one fixed boundary.

`tools/run_address_observer_pair.py` retains four clean UNSAT theorem
obligations, 22 SAT source instances with models, 46 UNSAT semantic/domain
probes, direct independent Z3 replay, and two trusted-free Verus models. Its
atomic preservation gate covers all 54 certified evidence trees and all 320
frozen inputs, changes only rows 039 and 111's two result fields, and requires
the ledger to finish with 56 classified and 6 `not-run` rows. Independent
review remains required and stage transition is disabled.

## Targets 017, 018, 046, and 047 source-backed mutable view construction

Input orders 017 `core::slice::as_flattened_mut`, 018
`core::slice::as_mut_array`, 046 `core::slice::first_chunk_mut`, and 047
`core::slice::from_mut` retain their literal active generated declarations.
Their Rust 1.96 source and docs, frozen implementation-proof harnesses and
manifests, and all 34 trust records are hash-bound and retained by readable
content.

The answer-bearing pairs `TS-017-D006`/`TS-017-E004`,
`TS-018-D004`/`TS-018-E002`, `TS-046-D004`/`TS-046-E002`, and
`TS-047-D001`/`TS-047-E001` remain inadmissible. They are replaced rather
than relabeled by defined source transitions for checked multiplication
overflow and valid unchecked multiplication, mutable pointer extraction,
pointer casts, raw-slice or mutable array-reference construction, exact
returned ranges and root-borrow identities, singleton array-to-slice
unsizing, and borrow-lifetime final frames. Successful returned contents
remain free at their exact length while receiver/return reconstruction,
unchanged prefix suffix, outside memory, and backing
address/allocation/provenance/root-borrow identity remain enforced. Target
047 additionally binds a project-local exact excerpt of canonical Rust 1.96
`core/src/array/mod.rs:174-177`; the frozen authority tree is unchanged.

Every theorem uses one shared valid `x` and one shared `b`. `Boundary_T`
contains only initial and outside-frame memory, address, allocation extent,
provenance, live exclusive root-borrow identity, element layout, and
usize/isize platform limits. It excludes the length product, overflow and
option branches, returned values, range, pointer/borrow identity, projection,
final state, answer encodings, and execution traces. `Requires_T` contains
only integer encodings and target input-shape facts.

The active old-view and final-frame clauses are checked literally after the
source transition. Exact-output equivalence compares the complete panic or
option outcome and exact reference identity/range. Full-state equivalence
also compares the borrow-lifetime input, returned-view, outside-memory, and
backing identity frames. No equivalence observation is weakened. Legal writes
through the returned exclusive borrow therefore make the full-state theorem
SAT even though exact output remains deterministic.

The retained cases cover empty and nonempty receivers, ZST and non-ZST
elements, `N = 0`, `N < len`, `N = len`, `N > len`, checked multiplication
overflow, valid unchecked multiplication, and singleton unsizing. Negative
probes reject null, misaligned, out-of-allocation, provenance-free,
nonexclusive, dead-borrow, wrong-branch, wrong-range, wrong-identity,
wrong-frame, and answer-laundering alternatives.

`tools/run_mutable_view_construction_cluster.py` retains four clean UNSAT
exact-output obligations, four SAT full-state obligations, one replayable
fixed-input/fixed-boundary SAT witness per target, 22 SAT source instances
with models, 82 UNSAT semantic/domain probes, independent direct Z3 replay,
and four trusted-free Verus models. Exact output is
`conditional-complete`; full state is `conditional-incomplete` for all four
targets. Its atomic preservation gate covers all 56 certified evidence trees
and all 320 frozen inputs, changes only the four assigned rows' two result
fields, and requires the ledger to finish with 60 classified and 2 `not-run`
rows. Independent review remains required and stage transition is disabled.

## Targets 008 and 009 source-backed `align_to` transitions

For `align_to` and `align_to_mut`, `Boundary_T` contains only initialized
address-indexed input bytes, input Slice length and representation,
allocation bounds and provenance, T/U size/alignment/ZST facts, usize/isize
limits, the public unsafe transmute-validity precondition, root-borrow
identity/liveness/alias permission, and outside-frame memory. It excludes
`slice_align_to_domain`, `slice_aligned_middle`, the alignment offset, branch
choice, gcd result, returned partitions or identities, decoded U values,
final bytes or views, target truth, and traces.

The model replaces `TS-008-D004`/`TS-008-E005`/`TS-008-E006` and
`TS-009-D004`/`TS-009-E003`/`TS-009-E004`; none is relabeled. Defined
transitions follow canonical Rust 1.96 source order: Slice thin-pointer
extraction; `ptr::align_offset`'s element-stride search, wrapping address
semantics, ZST case, and `usize::MAX` no-solution result; the target ZST and
`offset > len` branches; gcd/ts/us `align_to_offsets` arithmetic; prefix,
middle, and suffix ranges; pointer casts/addition; raw-slice construction;
finite typed decoding of the middle from the same initial bytes; returned
allocation/provenance/root-borrow identity; disjoint mutable regions; and a
single relational final byte frame decoded back into every final T/U view.
The literal active result and mutable-final conjuncts are checked explicitly;
the opaque generated vocabulary is not declared to the solver.

Exact equivalence compares every branch, offset, value, length, address,
allocation, provenance, borrow identity, mutability, and disjointness field.
Full equivalence additionally compares final bytes, source/prefix/middle/
suffix views, outside frame, and backing identity. Both target-008 theorem
negations and target 009's exact-output negation are clean UNSAT. Target 009's
full-state negation is SAT, with a retained same-input/same-boundary witness
that changes one byte through the returned mutable partition while preserving
all active clauses and relational frames.

Twenty SAT source instances cover empty, source/destination ZST, already
aligned byte reinterpretation, finite misalignment, offset equal to length,
offset greater than length, `usize::MAX`, nontrivial size gcd, and nondefault
allocation/provenance. Forty-three UNSAT probes reject invalid memory,
alignment, allocation, provenance, transmute/borrow/alias state, wrong
offset/branch/arithmetic/ranges/identity/decoding/final frames, boundary
mismatch, and answer laundering. Two trusted-free Verus models each verify
six source-transition obligations. The bounded runner preserves all 60
certified target trees and 320 frozen files, changes only the two result cells
on rows 008 and 009, and leaves 62 classified and zero `not-run`.
The retained campaign entry point is `tools/run_align_to_pair.py`.

## Evidence layout

- `crosswalk/target_to_proof_boundary.{csv,json}`: one row per selected target
- `crosswalk/trust_site_inventory.{csv,json}`: normalized dependency and
  external-body sites
- `crosswalk/contract_drift_reconciliation.{csv,json}`: six active drifts
- `provenance/`: working-tree hashes and frozen bytes
- `evidence/tool_versions/`: exact command/stdout/stderr/status captures
- `evidence/equivalence/`: SMT, solver captures, models, and witness manifest
- `evidence/targets/029_core_slice_binary_search_by/`: checker-validated
  target obligation, sorted-domain sanity proof, exact-output witness, concrete
  model, independent replay, and fresh frozen-harness Verus capture
- `evidence/targets/013_core_slice_as_chunks_mut/`: checker-validated full
  exact-state and exact-output obligations, fixed-boundary final-state witness,
  independent replay, and fresh strengthened-contract Verus capture
- `evidence/targets/106_core_slice_splitn_mut/`: checker-validated
  source-constructor exact-state and exact-output obligations, independent
  solver replay, and fresh constructor-model Verus capture
- `evidence/targets/032_core_slice_chunk_by_mut/` and the corresponding
  036/069/074/076/093/098 target trees: arbitrary-length source-constructor
  exact-state and exact-output obligations, empty/nonempty/ZST source
  instances, complete authority/trust/source bindings, target-local Verus
  models, and independent solver replays
- `evidence/mutable_iterator_constructor_cluster/`: 27-tree and seven-frozen-
  input preservation manifest plus the final 34/28 ledger transition
- `evidence/targets/037_core_slice_clone_from_slice/` and
  `evidence/targets/043_core_slice_fill/`: relation-valued normal and panic
  obligations, every specialization witness, retained SAT models, exact
  source/trust bindings, independent replay, and trusted-free Verus models
- `evidence/clone_effect_cluster/`: 38-tree and complete frozen-input
  preservation manifest plus the final 40/22 ledger transition
- `evidence/targets/035_core_slice_chunks_exact_mut/` and
  `evidence/targets/068_core_slice_rchunks_exact_mut/`: arbitrary-length exact
  partition theorems, six source instances with retained models and eight
  negative probes per target, complete source/trust bindings, independent
  replay, and trusted-free Verus models
- `evidence/exact_mutable_iterator_partition_cluster/`: 40-tree and
  320-frozen-input preservation manifest plus the final 42/20 ledger transition
- `evidence/targets/062_core_slice_last_chunk_mut/`,
  `evidence/targets/090_core_slice_split_first_chunk_mut/`, and
  `evidence/targets/096_core_slice_split_last_chunk_mut/`: exact fixed-chunk
  source theorems, required edge/ZST models, negative probes, complete
  source/trust bindings, independent replay, and trusted-free Verus models
- `evidence/mutable_fixed_chunk_edge_cluster/`: 42-tree and 320-frozen-input
  preservation manifest plus the final 45/17 ledger transition
- `evidence/targets/085_core_slice_split_at_mut_checked/` and
  `evidence/targets/086_core_slice_split_at_mut_unchecked/`: exact mutable
  split theorems, checked/unchecked domain instances, one-past-end and ZST
  models, semantic negative probes, complete source/trust bindings,
  independent replay, and trusted-free Verus models
- `evidence/split_at_mut_primitive_cluster/`: 45-tree and 320-frozen-input
  preservation manifest plus the final 47/15 ledger transition
- `evidence/targets/099_core_slice_split_off/` and
  `evidence/targets/104_core_slice_split_off_mut/`: exact directional
  split-off obligations, active mutable dual-partition audit, edge/ZST source
  models, semantic probes, complete source/trust bindings, independent
  replay, and trusted-free Verus models
- `evidence/split_off_pair_cluster/`: 47-tree and 320-frozen-input
  preservation manifest plus the final 49/13 ledger transition
- `evidence/targets/048_core_slice_from_raw_parts/` and
  `evidence/targets/049_core_slice_from_raw_parts_mut/`: raw-domain UB-check,
  fat-pointer construction, reference-dereference, exact-output/full-state
  obligations, empty/ZST/one-past models, semantic probes, fixed mutable
  incompleteness witness, complete source/trust bindings, independent replay,
  and trusted-free Verus models
- `evidence/raw_slice_pair_cluster/`: 49-tree and 320-frozen-input
  preservation manifest plus the final 51/11 ledger transition
- `evidence/targets/053_core_slice_get_mut/`,
  `evidence/targets/054_core_slice_get_unchecked/`, and
  `evidence/targets/055_core_slice_get_unchecked_mut/`: explicit SliceIndex
  bounds, pointer/provenance, dereference, returned-reference, borrow, and
  frame obligations; exhaustive 25-form target-054 normalization; concrete
  target-053/055 alternative-reference witnesses; semantic probes; complete
  source/trust bindings; independent replay; and trusted-free Verus models
- `evidence/slice_index_trio/`: 51-tree and 320-frozen-input preservation
  manifest plus the final 54/8 ledger transition
- `evidence/targets/039_core_slice_element_offset/` and
  `evidence/targets/111_core_slice_subslice_range/`: exact active contracts,
  canonical source/docs, all frozen proof inputs and trust records, explicit
  address/arithmetic/Option transitions, exact-output/full-state obligations,
  edge and false-positive source models, semantic probes, independent replay,
  and trusted-free Verus models
- `evidence/address_observer_pair/`: 54-tree and 320-frozen-input preservation
  manifest plus the bounded 56/6 ledger transition
- `evidence/targets/017_core_slice_as_flattened_mut/`,
  `evidence/targets/018_core_slice_as_mut_array/`,
  `evidence/targets/046_core_slice_first_chunk_mut/`, and
  `evidence/targets/047_core_slice_from_mut/`: literal active contracts,
  canonical target/helper source, frozen proof inputs, all trust records,
  explicit length/overflow, pointer, cast, raw-slice/array-reference, range,
  borrow, singleton-unsizing, and frame transitions; exact-output/full-state
  obligations; source models; semantic probes; independent replay; and
  trusted-free Verus models
- `evidence/mutable_view_construction_cluster/`: 56-tree and 320-frozen-input
  preservation manifest, project-local canonical `array::from_mut` excerpt,
  and the bounded 60/2 ledger transition
- `evidence/targets/008_core_slice_align_to/` and
  `evidence/targets/009_core_slice_align_to_mut/`: literal active contracts,
  canonical Slice and `ptr::align_offset` source/docs, all frozen proof inputs
  and 20 trust records, exact-output/full-state obligations, edge and
  wrong-transition probes, the mutable fixed witness, independent replay,
  and trusted-free Verus models
- `evidence/align_to_pair_cluster/`: 60-tree and 320-frozen-input preservation
  manifest plus the final 62/0 ledger transition
- `evidence/targets/081_core_slice_sort_unstable_by/`: checker-validated
  exact-final-slice and reviewed equal-key SAT obligations, total-order
  sanity proof, fixed-boundary witness replays, and a fresh Verus model capture
- `evidence/targets/080_core_slice_sort_unstable/` and
  `evidence/targets/082_core_slice_sort_unstable_by_key/`: general
  arbitrary-length reviewed-equivalence UNSAT proofs, bounded exact-output SAT
  witnesses, positive/negative equal-class probes, complete trust-site and
  source bindings, independent replay, and clean experiment-local Verus models
- `evidence/targets/077_core_slice_select_nth_unstable/`: arbitrary-length
  reviewed-selection UNSAT proof, fixed exact-output SAT model, seven
  positive/negative witness probes, all authority/trust/source bindings,
  independent replay, 24-tree preservation evidence, and a clean target-local
  Verus model
- `evidence/targets/078_core_slice_select_nth_unstable_by/` and
  `evidence/targets/079_core_slice_select_nth_unstable_by_key/`: arbitrary-
  length exact and reviewed SAT obligations, fixed source-replayed callback
  state countermodels, callback panic-prefix probes, complete authority/trust/
  source bindings, and clean target-local Verus models
- `evidence/selection_callback_cluster/`: two-target result, 25-tree
  preservation, and frozen-input preservation manifest
- `evidence/unstable_sort_companions/`: two-target result and preservation
  manifest for the 22-tree certified baseline
- `evidence/targets/022_core_slice_as_ptr_range/`: checker-validated exact
  endpoint/state obligations, five valid-domain SAT probes, three invalid-domain
  UNSAT probes, canonical `ptr::add` source/docs, independent replay, and a
  fresh Verus model capture
- `evidence/targets/120_core_slice_write_copy_of_slice/`: checker-validated
  exact output/state obligations, source-backed per-slot MaybeUninit copy
  semantics, twelve domain/rejection probes, canonical source bindings,
  independent replay, and a fresh Verus model capture
- `evidence/targets/052_core_slice_get_disjoint_unchecked_mut/`:
  checker-validated exact-output and full-state SAT obligations, a fixed
  `[0,2]` versus `[1,2]` witness, source-backed two-slot MaybeUninit probes,
  canonical source bindings, independent replay, and a fresh Verus model
  capture
- `evidence/targets/019_core_slice_as_mut_ptr/` and
  `evidence/targets/021_core_slice_as_ptr/`: checker-validated exact pointer
  and full exact-state obligations, canonical cast bindings, five valid-domain
  probes, rejection probes, independent replay, and Verus models
- `evidence/targets/020_core_slice_as_mut_ptr_range/`: checker-validated exact
  endpoint and full exact-state obligations, a hash-bound dependency on the
  target-019 source transition, canonical mutable `ptr::add` source and safety
  docs, domain/rejection probes, independent replay, and a Verus model
- `evidence/targets/028_core_slice_binary_search/`,
  `evidence/targets/030_core_slice_binary_search_by_key/`, and
  `evidence/targets/065_core_slice_partition_point/`: separate general,
  ordered/partitioned sanity, and exact-output obligations; fixed SAT models;
  contract witness replay; frozen wrapper/lower-source bindings; and
  experiment-local Verus source-transition models
- `evidence/targets/025_core_slice_assume_init_drop/`,
  `evidence/targets/026_core_slice_assume_init_mut/`, and
  `evidence/targets/119_core_slice_write_clone_of_slice/`: exact active input
  bindings, target-specific full/exact obligations, storage/lifecycle probes,
  target-026 fixed SAT countermodel and contract replay, canonical drop/Clone/
  Guard/cast source, independent cluster replay, and clean Verus models
- `logs/04_theorem_template_z3.*`: required clean replay of the emitted theorem
- per-target solver evidence retains immutable SMT/Verus input, exact command,
  stdout, stderr, exit status, solver status, and SAT model/replay records
