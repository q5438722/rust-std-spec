# Slice/Vec implementation-proof trust-boundary audit

Date: 2026-08-13

## Scope

This audit covers the 180 implementation-proof obligations in
`proof_inventory/targets_180.json`:

| Module | Proof targets | Existing-vstd contracts | Generated contracts |
| --- | ---: | ---: | ---: |
| `core::slice` | 132 | 12 | 120 |
| `alloc::vec` | 48 | 24 | 24 |
| **Total** | **180** | **36** | **144** |

`Vec::splice` is not part of the 180-target proof inventory because it has no
selected contract.

## Two different meanings of "no trust boundary"

Two counts are useful and must not be conflated:

1. **No additional implementation/dependency boundary:** the executable target
   body is proved without a target-local `external_body`, assumed dependency
   implementation, manually trusted private invariant, or mechanically reviewed
   source-to-Verus lowering. Under this campaign-specific definition, **2 of
   180** targets are boundary-free.
2. **End-to-end trust-free:** the result does not rely on Verus/rustc, Z3, vstd
   axioms and external type models, the selected API contract, or any manually
   reviewed source adaptation. Under this foundational definition, **0 of 180**
   targets are trust-free.

Unless explicitly stated otherwise, this document uses the first,
implementation-boundary definition.

## Headline result

| Metric | Slice | Vec | Total |
| --- | ---: | ---: | ---: |
| Proof targets | 132 | 48 | 180 |
| No target-level `external_body` | 132 | 48 | 180 |
| No `external_body` anywhere in the harness | 47 | 2 | 49 |
| No additional implementation/dependency boundary | 1 | 1 | 2 |
| At least one additional boundary | 131 | 47 | 178 |
| Harness contains helper/model/dependency `external_body` | 85 | 46 | 131 |
| Boundary-dependent without a literal `external_body` | 46 | 1 | 47 |

The 131 harnesses containing `external_body` have 392 occurrences: 219 in
Slice harnesses and 173 in Vec harnesses. This is a syntactic count, not a count
of distinct semantic assumptions. A harness may contain several external type,
model, dependency, or primitive-operation declarations for one conceptual
boundary.

The important distinction is:

- **Target body:** all 180 target functions remain executable in their proof
  harnesses; none is accepted by marking the target itself `external_body`.
- **Helper/dependency body:** 131 harnesses externalize at least one lower-level
  operation or model.
- **Reviewed lowering without `external_body`:** 47 additional harnesses have
  no literal `external_body` but still rely on a reviewed equivalence,
  representation invariant, iterator model, or previously reviewed dependency.

## The two implementation-boundary-free targets

| Target | Contract origin | Executable body | Evidence |
| --- | --- | --- | --- |
| `core::slice::is_empty` | Existing vstd | `slice.len() == 0` | `proof_harnesses/150_core_slice_is_empty/` |
| `alloc::vec::Vec::is_empty` | Existing vstd | `self.len() == 0`, with the Vec length/view relation proved locally | `proof_harnesses/164_alloc_vec_Vec_is_empty/` |

Both manifests use
`proof_status = actual_verus_verified_no_trusted_boundary`. Their target bodies
and required length/view facts are verified directly, and neither harness
contains `#[verifier::external_body]`.

By contract origin:

| Contract origin | Targets | Boundary-free | Boundary-dependent |
| --- | ---: | ---: | ---: |
| Slice existing-vstd | 12 | 1 | 11 |
| Slice generated | 120 | 0 | 120 |
| Vec existing-vstd | 24 | 1 | 23 |
| Vec generated | 24 | 0 | 24 |
| **Existing-vstd total** | **36** | **2** | **34** |
| **Generated total** | **144** | **0** | **144** |

The existing-vstd contract is still part of the specification-layer trust
surface. "Boundary-free" here means that no additional implementation
boundary is needed to prove the executable body against that contract.

## Why `ABCD = B` does not mean the boundary-free count is zero

`proof_inventory/aggregate_coverage.json` reports `B = 180`. That field is a
conservative campaign disposition covering contract provenance, model
instantiation, source adaptation, and dependency review. It is not the precise
counter for target-level implementation boundaries.

The finer `proof_status` field distinguishes the two
`actual_verus_verified_no_trusted_boundary` targets. The aggregate
`boundary_type_for` function in `tools/reconcile_live_scope_180.py` only emits
`none` for an A row; every unrecognized B status is placed in the
`trusted_boundary_enumerated` catch-all. Consequently, the two boundary-free
implementation proofs are also present in that catch-all. Use `proof_status`
and the target dependency manifests for the implementation-boundary count.

## Boundary layers

### 1. Specification and model layer

All 180 targets are checked against a selected contract:

- 36 exact existing-vstd contracts;
- 144 generated `assume_specification` contracts.

Client verification trusts these declarations as API contracts. The
implementation campaign provides evidence that an executable Rust 1.96 body,
or an auditable mechanical adaptation of it, satisfies the contract. The
current artifacts do not replace the standard-library binary or mechanically
link the proof harness function to rustc's compiled standard-library item.

Shared views such as `slice_iterator_view`, Vec logical sequence views,
raw-domain predicates, callback observation traces, and mutable final-frame
relations are also part of this layer. Open definitions and lemmas proved in
the same harness are not additional implementation boundaries; uninterpreted
or externally constrained models are.

### 2. Literal Verus external bodies

`#[verifier::external_body]` is used for lower-level operations that Verus
cannot currently prove directly, including:

- raw pointer construction, arithmetic, reads, writes, copies, swaps, and
  dereferences;
- allocation and `RawVec` capacity/storage transitions;
- private iterator or container representation bridges;
- trait, callback, and comparison observations;
- intrinsics, layout queries, panic paths, and selected unsafe preconditions;
- `MaybeUninit`, drop, transmute, and initialization-state operations.

The target function itself is never externalized. The external declaration is
kept narrow, source-backed, and recorded in the corresponding
`dependency_assumption_manifest.json`.

### 3. Reviewed dependency contracts

Some target bodies call another Slice/Vec function whose contract or earlier B
proof is reused rather than inlined and re-proved. Examples include:

- `split_off_first` reusing `split_first`;
- `split_off_last_mut` reusing `split_last_mut`;
- checked split functions reusing unchecked split contracts;
- Vec methods reusing `as_ptr`, `as_mut_ptr`, `push_mut`, `insert_mut`,
  `truncate`, or other storage-changing operations.

These dependencies are transitive trust boundaries until the complete call
chain is connected without assumed intermediate contracts.

### 4. Mechanical source-to-Verus lowerings

A harness can contain no `external_body` and still be B because unsupported
Rust syntax or borrowing behavior was mechanically lowered:

- immutable and mutable slice patterns;
- `u8` range patterns used by ASCII classification;
- `mem::replace` or `mem::take` expressed as an equivalent swap;
- `FnMut`/`FnOnce` closure calls represented by observation functions;
- panic/unreachable branches represented by reviewed preconditions;
- unchecked valid-index operations replaced with reviewed safe splits.

These are human-review boundaries: the Verus proof establishes the lowered
program, while equivalence to the frozen Rust source is justified by a
transformation manifest and adjacent `original_implementation.rs` where
applicable.

### 5. Private representation and iterator-state boundaries

Iterator and container methods frequently expose behavior determined by
private fields. Residual boundaries include:

- `ChunksExact`, `RChunksExact`, mutable exact-chunk, `Iter`, `IterMut`,
  splitting, and window iterator state;
- source, remaining, yielded-prefix, remainder, chunk-size, and direction
  relations;
- private representation invariants such as
  `remainder.len() < chunk_size`;
- Vec buffer pointer, initialized length, capacity, allocator, and
  ownership/lifetime state.

Immutable exact-chunk remainder access is easier because `&[T]` is copyable and
the type invariant can be used directly. Moving an `&mut [T]` field out of an
invariant-bearing datatype remains a Verus limitation for
`ChunksExactMut::into_remainder` and
`RChunksExactMut::into_remainder`.

### 6. Raw memory, provenance, and allocator boundaries

These are the largest foundational gaps. Full proofs would need a common model
for:

- pointer validity, alignment, liveness, and initialization;
- allocation identity and provenance;
- aliasing and exclusive mutable permissions;
- pointer arithmetic and one-allocation bounds;
- ownership transfer through `from_raw_parts`, `ManuallyDrop`, raw Vec parts,
  and boxed-slice conversion;
- allocator growth, reserve, shrink, capacity, and initialized-prefix
  preservation.

This is why `from_raw_parts` and many Vec storage operations cannot currently
be reduced to ordinary Seq reasoning alone.

### 7. Trait, callback, and specialization boundaries

Search, sorting, selection, deduplication, retention, and iterator predicates
call arbitrary user code or typeclass operations. Their boundaries record:

- `PartialEq`, `PartialOrd`, `Ord`, `Clone`, and indexing behavior;
- `FnMut`, `FnOnce`, key extraction, comparator, and predicate observations;
- callback order and mutable callback effects;
- specialization such as slice contains/fill/clone paths;
- unstable sorting/selection helper behavior.

The contracts describe observable result and mutation relations without
claiming a proof of arbitrary callback implementations.

### 8. Intrinsic, panic, drop, and `MaybeUninit` boundaries

Additional low-level boundaries include:

- `copy_nonoverlapping`, overlapping copy, rotate, swap, transmute, metadata,
  and optimization intrinsics;
- checked unsafe preconditions and unreachable panic branches;
- `drop_in_place`, panic guards, length commits, and leak amplification;
- initialized/uninitialized storage transitions and `assume_init` operations.

These require memory-state and unwind/frame semantics beyond the current
target-local sequence models.

## Conservative source-dependency incidence

`proof_inventory/target_counts.json` records a conservative scan of the frozen
Rust bodies. The categories overlap: one target can appear in several rows,
and presence in source does not mean every occurrence remains an undischarged
trust boundary.

| Source dependency category | Slice targets | Vec targets | Total targets |
| --- | ---: | ---: | ---: |
| `unsafe` | 46 | 23 | 69 |
| Raw pointer or provenance | 38 | 23 | 61 |
| Trait or callback | 39 | 10 | 49 |
| Panic or bounds | 25 | 5 | 30 |
| Allocator | 0 | 27 | 27 |
| Intrinsic | 10 | 5 | 15 |
| `MaybeUninit` | 6 | 2 | 8 |

These counts are useful for prioritization, not for summing a total number of
trusted assumptions.

## B16 low-boundary subset

The submission subset in
`submission_candidates/B16_LOW_BOUNDARY_SUBSET/` contains 16 generated
contracts and 16 implementation harnesses.

- All 16 harnesses contain no `#[verifier::external_body]`.
- None of the 16 is implementation-boundary-free.
- The subset uses 10 distinct reviewed boundary/mechanical interface families,
  referenced 22 times.
- Its remaining boundaries are slice-pattern lowering, mutable slice-pattern
  lowering, swap-with-empty lowering, ASCII range/pattern lowering,
  `u8::is_ascii_whitespace`, reviewed valid-index split behavior, and immutable
  exact-chunk representation invariants.

Therefore B16 is a **low-boundary** subset, not a boundary-free subset.

## Boundaries removed during this campaign

The following former shortcuts are no longer trusted boundaries:

- `lemma_ascii_trim_start_index_matches_boundary`;
- `lemma_ascii_trim_end_index_matches_boundary`;
- `byte_make_ascii_lowercase`;
- `byte_make_ascii_uppercase`.

The trim lemmas now prove boundary uniqueness and the `choose` witness
directly. The ASCII case helpers now prove byte classification, bit-mask
behavior, arithmetic equivalence, and in-place mutation in Verus. The
lowercase and uppercase mask/arithmetic bridges use bit-vector proofs.

The exact-chunk constructor harnesses also verify constructor arithmetic and
partition facts; the remaining boundary is the reviewed valid-index split and,
for remainder accessors, the private iterator representation relation.

## Priority order for reducing the remaining trust surface

1. Build a reusable pointer/provenance/permission model for raw slices and Vec
   storage.
2. Connect `RawVec` allocation, growth, shrink, and initialized-prefix
   invariants.
3. Add Verus support or reusable proofs for moving mutable-reference fields
   from invariant-bearing datatypes.
4. Replace iterator-view assumptions with constructor-to-method invariant
   proofs across complete iterator families.
5. Connect trait/callback observation models to executable closure semantics.
6. Eliminate mechanical pattern and closure lowerings through frontend support
   or formally proved desugaring lemmas.
7. Model `MaybeUninit`, drop, panic guards, and unwind-sensitive final frames.

## Audit sources

- `proof_inventory/targets_180.json`
- `proof_inventory/aggregate_coverage.json`
- `proof_inventory/target_counts.json`
- `proof_inventory/source_body_spans.json`
- `proof_manifests/*/dependency_assumption_manifest.json`
- `proof_manifests/*/transformation_manifest.json`
- `proof_harnesses/*/harness.rs`
- `submission_candidates/B16_LOW_BOUNDARY_SUBSET.md`
- `submission_candidates/B20_LOW_BOUNDARY_SUBSET.md`

The aggregate gate remains:

```text
180 targets, B=180, pending=0, exact-vstd=36
```

That gate establishes complete campaign coverage. The finer distinction in
this document establishes that 2 targets need no additional implementation
boundary, while 178 retain at least one explicit trusted or mechanically
reviewed dependency.
