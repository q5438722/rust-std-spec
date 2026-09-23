# Source ownership: `core::slice`

Authority: `/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src`.
The 23 files below, the adjacent slice inherent impl in `mem/maybe_uninit.rs`,
and the actual adjacent definitions listed in `sources.tsv` are the evidence.
No earlier campaign inventory, specification, proof, or verifier installation is
an input. `sources.tsv` pins the bytes read, not a claimed upstream commit.

## Real module graph

```text
slice/mod.rs                         primitive slice inherent impls; error; helpers
├── ascii.rs                         [u8]; EscapeAscii; ASCII implementation
├── cmp.rs                           slice comparison impls and specializations
├── index.rs [pub(crate)]             Index/IndexMut; SliceIndex; sealing; range checks
├── iter.rs                          public iterator types and their impls
│   └── iter/macros.rs                iterator!, forward_iterator!, pointer/ZST helpers
├── raw.rs                           reference/raw-pointer constructors
├── rotate.rs                        private pointer rotation algorithms
├── specialize.rs                    private SpecFill specializations
├── memchr.rs [pub, unstable, hidden] byte-search helpers
└── sort/mod.rs [pub, unstable, hidden]
    ├── stable/mod.rs [pub]           sort; BufGuard; scratch allocation abstraction
    │   ├── drift.rs [pub(crate)]     driftsort
    │   ├── merge.rs [pub(crate)]     merge and unwind guard
    │   ├── quicksort.rs [pub(crate)] stable quicksort/partition
    │   └── tiny.rs [pub(crate)]      size-optimized mergesort
    ├── unstable/mod.rs [pub]         unstable sort / partial sort entrypoints
    │   ├── heapsort.rs               heapsort fallback
    │   └── quicksort.rs              ipnsort/partition and gap guards
    ├── select.rs [pub(crate)]        selection; median-of-medians fallback
    └── shared/mod.rs [pub(crate)]    existing runs; FreezeMarker
        ├── pivot.rs [pub(crate)]     pivot selection
        └── smallsort.rs [pub(crate)] specialization, insertion/network/merge sorts
```

`stable/{drift,quicksort}` versus `stable/tiny` are configuration-dependent:
`optimize_for_size` / 16-bit targets select the small implementation.
ASCII has separately retained scalar/SWAR, x86-64 SSE2, and loongarch64 LSX
implementations. These are source alternatives, not extra public APIs.

## Type, impl and export ownership

* `mod.rs`: `impl<T> [T]`, `impl<T, const N: usize> [[T; N]]`,
  the unstable alignment method on `[MaybeUninit<T>]`, and unstable `[f32]`/
  `[f64]` sorting; `Default` for shared/mutable slice references;
  `GetDisjointMutError` and its Display/derived interfaces.
* `ascii.rs`: `[u8]` methods and `EscapeAscii`, reexported at `core::slice`.
  Its `EscapeByte` callable is private even though macro-generated.
* `iter.rs`: 24 exported iterator types: `Iter`, `IterMut`, `Windows`,
  `ArrayWindows`, `Chunks{,Mut}`, `ChunksExact{,Mut}`, `RChunks{,Mut}`,
  `RChunksExact{,Mut}`, `Split{,Mut}`, `SplitInclusive{,Mut}`, `RSplit{,Mut}`,
  `SplitN{,Mut}`, `RSplitN{,Mut}`, `ChunkBy{,Mut}`.
  Their public inherent methods, explicit Iterator/DoubleEndedIterator/
  ExactSizeIterator overrides, formatting, cloning, AsRef and Default impls
  belong here. `IntoIterator` for `&[T]` and `&mut [T]` also belongs here.
  Private constructors, `SplitIter`, and `GenericSplitN` are dependencies.
* `cmp.rs`: `PartialEq`, `PartialOrd`, `Ord` executable slice impls.
  `Eq` has no source-written method here. `SlicePartialEq`, `SlicePartialOrd`,
  `SliceChain`, `SliceOrd`, `SliceContains`, and their specialized implementations
  remain private dependencies, not additional public comparisons.
* `index.rs`: stable `Index`/`IndexMut` overrides; the stable, sealed
  `SliceIndex` trait is reexported. Its **six callable methods remain unstable**,
  including in stable impls. They are retained as dispatch dependencies, not
  falsely counted as stable directly callable methods.
* `raw.rs`: stable reexports `from_ref`, `from_mut`, `from_raw_parts`,
  `from_raw_parts_mut`; unstable pointer-range constructors are retained as
  exclusions. A reexport never creates another executable identity.
* `mem/maybe_uninit.rs`: the adjacent `impl<T> [MaybeUninit<T>]` contributes
  five stable methods: `write_copy_of_slice`, `write_clone_of_slice`,
  `assume_init_drop`, `assume_init_ref`, `assume_init_mut`.
  Its unstable fill/byte-view methods are excluded explicitly. Scalar/array
  `MaybeUninit` methods and initialization/unwind guards remain adjacent
  dependencies, not extra slice-owned APIs.

`SlicePattern` and `GetDisjointMutIndex` are unstable traits despite their use
in stable slice signatures. That does **not** make `strip_prefix`, `strip_suffix`,
or `get_disjoint_mut` unstable. Conversely, a stable impl attribute does not
stabilize an unstable trait method or an unstable receiver type.
`BufGuard` and public functions behind the unstable `sort` module inherit that
gate. Public helpers inside private modules have no independently reachable
public binding.

### Range/indexing domains

The slice-owned `SliceIndex<[T]>` impls cover 12 public stable input families:
`usize`; legacy `ops::{Range,RangeTo,RangeFrom,RangeFull,RangeInclusive,
RangeToInclusive}`; a pair of `ops::Bound<usize>`; and the **distinct**
`core::range::{Range,RangeFrom,RangeInclusive,RangeToInclusive}` types.
There is also the private `ops::IndexRange` implementation.
All six methods of every implementation are retained in `exclusions.tsv`;
the public wrappers still require their semantics.

The replacement inclusive range stabilized in 1.95, the other three in 1.96.
`range.rs` contains their exact fields, bounds, and conversions; `range/iter.rs`
owns their iterators, not `slice/iter.rs`. `range/legacy.rs` is an unstable
reexport route to the already-stable legacy `ops` types, not a new type identity.
New inclusive types use `last`; legacy inclusive ranges also carry exhaustion
state. The actual conversion bodies, not an assumed field renaming, are the
indexing dependency.

`GetDisjointMutIndex` has five source impls: `usize`, legacy and replacement
`Range<usize>` / `RangeInclusive<usize>`. Bounds pairs, open-ended ranges, and
all other `SliceIndex` implementers are not silently added to this domain.
Adjacent `core::index::{Clamp,Last}` wrappers are unstable and outside the stable
surface; sealing declarations alone do not establish stable indexing support.

## Count and scope policy

`apis.tsv` contains **331 stable public source-owned executable identities**:

| Owning source module | Identities |
|---|---:|
| `slice/mod.rs` | 111 |
| `slice/iter.rs` (including emitted macro methods) | 185 |
| `slice/ascii.rs` | 17 |
| `slice/cmp.rs` | 7 |
| `slice/index.rs` | 2 |
| `slice/raw.rs` | 4 |
| adjacent slice impl in `mem/maybe_uninit.rs` | 5 |

By interface kind: 125 inherent methods, 188 explicit/emitted trait methods,
14 derived required-method interfaces, and four free functions. Derive rows
quote the actual trait declaration signature and derive input/type, **not an
invented compiler-expanded impl or body**. Lifetime, type and method bounds,
`[const]`, unsafe and explicit receivers remain in the exact source headers.
`counts.tsv` is the generated reconciliation for the source inventory tables.
Selected-vstd evidence is reconciled separately below.

The complete owned-candidate partition is **726 declarations/interfaces**:
622 directly spelled function declarations, 87 item-macro-emitted functions,
and 17 derive-required interfaces. These partition into the 331 stable APIs
and **395 exclusions/dependencies**, including 29 non-executable trait method
declarations. The stable set itself comprises 274 directly spelled functions,
43 macro-emitted functions, and 14 derived interfaces. Ten actual item-macro
invocations are replayed; marker-only expansions contribute no functions.
The source manifest contains 23 slice files and 37 inspected adjacent files.
`trait_surface.tsv` separately records 97 default-method groups, 61 conditional
blanket rules, six adjacent explicit impls, and one unstable derive-only
interface. These numbers are not added to the source-owned API denominator.

The denominator is ownership, not everything discoverable by method lookup:

* Trait defaults are separately enumerated in `trait_surface.tsv`, with their
  real declaration/body spans and the source impls which do not override them.
  This includes iterator adapters/reducers, default ExactSizeIterator `len`,
  Clone `clone_from`, PartialEq `ne`, and Ord defaults. They do not become new
  slice-owned bodies merely because an impl can use them.
* Actual adjacent blanket rules are recorded conditionally with their exact
  impl bounds. Generic conversions, borrowing, Any and blanket IntoIterator
  are not multiplied across every type or monomorphization. Downstream
  extension traits, alloc/std additions, auto-trait facts, marker impls,
  associated types/constants, fields, and unit variants are not executable
  source-owned functions.
* Adjacent explicit impls such as Hash/Debug/AsRef/AsMut for slices and Error
  for `GetDisjointMutError` have their external ownership recorded. No stable
  slice definition is discarded for difficulty, mutation, unsafe operations,
  callback behavior, sorting, pointer provenance, or initialization.
* Private/specialized/unstable definitions stay in `exclusions.tsv`, with
  reasons. Source cfg alternatives stay distinct there. Empty/negative impls,
  sealing, reexports and public types remain in `ownership.tsv`.

TSV cells use reversible `\\`, `\t`, `\r`, `\n` escaping; list cells contain
JSON after unescaping. Spans are inclusive source line spans relative to the
authority above. Macro rows retain both template and invocation provenance.
The extractor substitutes the actual item-macro templates, not grep counts.

## Actual dependencies and foundations

* `len` calls `ptr::metadata`, whose body calls the `ptr_metadata` intrinsic.
  The other five initial read-only observers use `len` or slice patterns.
  **Inspect the selected vstd's slice value view, metadata correspondence and
  borrowing facts before claiming any existing coverage.** Metadata alone
  cannot establish returned element contents.
* `raw::{from_ref,from_mut}` delegate to `array::{from_ref,from_mut}`.
  Raw constructors use `ptr::slice_from_raw_parts{,_mut}` and UB checks;
  provenance, lifetime, alignment, initialized contents and allocation extent
  are foundations, not consequences of a length-only view.
* Generic get/index methods dispatch through the exact SliceIndex impls.
  Replacement ranges delegate to legacy conversions/indexing. Pointer-offset
  helpers use intrinsics; bounds-pair normalization checks overflow and range
  endpoints. `IndexRange`'s `start <= end` invariant is private.
* Iterator constructors establish NonNull pointer/end-or-length invariants;
  ZST state differs from non-ZST pointer arithmetic. Split/chunk iterators
  delegate to slice splitting; mutable variants require disjointness and
  writeback. `EscapeAscii` delegates to FlatMap and ASCII escape iterators.
* Comparisons/contains dispatch through private specialization; bytewise paths
  use `compare_bytes`/memchr. Clone/fill have ordinary Clone, TrivialClone and
  integer-byte-fill branches. They are not replaced by unconditional Copy.
* Sorting/selection depend on partition, pivot, smallsort, heapsort, scratch
  and unwind/drop guards. Rotation selects private pointer algorithms.
  Stable sorting machinery is an unstable public core implementation dependency,
  not an extra stable `core::slice::sort` API.
* MaybeUninit copy/clone initialization delegates to copy/transmute/write and
  a prefix-initialization guard; unwind cleanup calls slice `assume_init_drop`.

`dependencies.tsv` preserves actual source callsites. Exact source-path targets
are linked; receiver/trait/callback ambiguities are explicitly tagged, not
presented as a compiler-resolved call graph. Builtin derives likewise have no
materialized compiler body in this core source tree. These boundaries do not
change the stable interface denominator or constitute implementation proofs.

## Bottom-up dependency order

After establishing the slice-value/metadata foundation, begin with these six
read-only observers, in order:
**`len` → `is_empty` → `first` → `split_first` → `split_last` → `last`.**
They require no iterator constructor relation; this explains beginning with
observers rather than constructors.

Then: array/raw/pointer foundations and indexing domains → checked/unchecked
subslice and chunk operations → mutable splitting/writeback → iterator
constructors plus state correspondence → iterator consumers and formatting →
comparison/search and specialization → clone/copy/fill and initialization →
disjoint indexing, rotation, sorting/selection and alignment.
Constructor-dependent iterator correspondence is established with the
constructor, not assumed to prove it. Shared helpers and mutually dependent
mutable operations retain their common obligations.

## Selected-vstd declaration mapping

All **331 stable API rows** now have a receiver-aware
`existing_vstd_coverage` classification, joined by `canonical_id` to
`vstd_coverage.tsv`. The source-owned denominator and the source/signature,
macro, derive, exclusion, and trait-surface inventories are unchanged.
The 395 excluded/dependency rows retain their previous pending cells: this
bounded mapping does not classify them or add trait defaults/blankets to the
stable denominator.

Baseline: pristine release **`0.2026.09.20.aef82ed`**, matching upstream commit
**`aef82eda71838deef4a8cd0260fda6c9504be9b9`**. All vstd spans below and in the
mapping are inclusive, relative to **`toolchain/upstream/source/vstd`**, not to
the Rust 1.96 semantic source root. Neither tree nor the verifier was modified.
The mappings refer to Verus specification/ghost mode; the `std_specs` module is
gated by `verus_keep_ghost` at `vstd.rs:96-97`.

| Classification | API rows | Meaning, not a proof result |
|---|---:|---|
| `assumed-contract` | 15 | Exact canonical API has an assumed value/content contract, with its stated preconditions and observations |
| `assumed-conditional` | 3 | Exact binding, but element-equality law gates the content result |
| `assumed-partial-domain` | 5 | Exact generic binding, with concrete index/range models for only part of the Rust 1.96 domain |
| `generic-trait-conditional` | 12 | Actual trait member plus the exact `slice::Iter`/`IterMut` type/state model; trait-law and callback conditions remain |
| `generic-trait-only` | 95 | Generic trait declaration is present, but no adequate concrete receiver contract/model is established |
| `missing` | 201 | Whole-vstd scan found no applicable method contract for this canonical receiver/trait |
| **Total** | **331** | |

The 95 generic-only rows comprise **18 signature-only**, **28 formatting
precondition-only**, and **49 law-gated members without a concrete receiver
model**. They are **not content coverage**. Likewise, a missing method may
still have an existing type/view. Compiler diagnostic hooks are a separate
`compiler_support_refs` field, not additional covered APIs: the mapping links
them for slice `len`, `Index::index`, and `IndexMut::index_mut`.
No compiler-only method coverage is inferred from same-name helpers.

### Important receiver and domain distinctions

* Five of the initial six observers have exact assumed bindings:
  `len` (`slice.rs:82-86`), `is_empty` (`slice.rs:92-96`), `first`
  (`std_specs/slice.rs:484-489`), `split_first`
  (`std_specs/slice.rs:547-552`), and `last`
  (`std_specs/slice.rs:491-496`). **`split_last` is missing**; its name has
  zero code-token hits across the selected vstd tree.
* The slice `View` is uninterpreted (`slice.rs:13-17`); the length link is an
  axiom (`slice.rs:77-80`). The `spec_slice_len` diagnostic item
  (`slice.rs:72-73`) is compiler support, not a proof connecting the current
  Rust `ptr::metadata` body or its pointer representation to slice contents.
* `get`, `get_mut`, and the two slice-owned indexing overrides have generic
  dispatch contracts. Concrete `SliceIndexSpecImpl<[T]>` models cover
  **seven** inputs: `usize` and the six legacy `core::ops` range types.
  The Rust source has **12** public stable index families. There is no
  concrete `[T]` model for the bounds pair or the four distinct replacement
  `core::range` types. A bounds-pair `SliceIndex<str>` model is a different
  receiver; a `RangeBoundsSpecImpl` is not a `SliceIndexSpecImpl`.
* `copy_within` links its content/frame helper and the exact
  `RangeBoundsSpecImpl` declarations for legacy ranges, bounds pairs, and
  their supported reference-bound forms. It is partial for arbitrary lawful
  user `RangeBounds` implementations and the replacement ranges: a generic
  spec-bound function is not by itself correspondence to the executable
  bound methods. Bounds/destination preconditions exclude panicking calls.
* Slice equality, `starts_with`, and `ends_with` retain the
  `PartialEqSpec::obeys_eq_spec()` gate, rather than imposing `Eq`/`Copy` or
  assuming all user comparisons have a deterministic, stateless model.
  The generic ordering-trait declarations do not supply slice lexicographic
  models, and their `default_ensures` do not prove source-written overrides.
* `slice::Iter` and `slice::IterMut` have exact external type declarations and
  prophetic state interfaces in `std_specs/slice.rs`. Their `next`,
  `next_back`, `len`, `all`, `any`, and `find` map to the actual members of
  `ExIterator`, `ExDoubleEndedIterator`, and `ExExactSizeIterator`; unrelated
  `VecDeque::Iter`, map/set iterators, or vector `IntoIter` are not substituted.
  No explicit per-invocation `FnMut` state trace or callback/drop-effect model
  is supplied by the linked generic consumer clauses. No concrete iterator
  pointer/ZST correspondence or separate frontend import/call test is claimed.
* Shared-slice `IntoIterator::into_iter` has an exact constructor binding;
  **mutable-slice `IntoIterator::into_iter` does not**. Its generic
  `ExIntoIterator` declaration is signature-only. The `I: Iterator` blanket
  identity contract does not apply to `&mut [T]`; the separately specified
  `<[T]>::iter_mut` is not the same canonical entry point.
* Array/Vec/Option `as_slice`, scalar `MaybeUninit::assume_init_{ref,mut}`,
  string ASCII operations, vector `split_off`, `core::mem::swap`, and
  `Seq`/resource proof helpers are explicitly not promoted to coverage of
  same-name slice APIs. All five adjacent `[MaybeUninit<T>]` APIs and all
  source-owned `[u8]` methods remain missing method contracts.

### Evidence and replay

* `vstd_coverage.tsv`: **331 rows**, with exact assumption/trait-member
  bindings, type/model/helper declarations and spans, compiler hooks,
  conditions, missing observations, and scan-query links. Every row explicitly
  says a Rust source-body proof is **not established by this mapping**.
* `vstd_sources.tsv`: the **130 Rust files / 1,924,657 bytes** actually scanned,
  with individual SHA-256 hashes, sizes, and line counts. The sorted
  `source + "\t" + sha256 + "\n"` records hash to
  `742b8567a2c9b143b7d0a40ce13c59823a712a583871b7b59c0be1d5a4891922`.
* `vstd_scan.tsv`: **186 replayed queries** for method tokens, receiver types,
  index/range models, and replacement-range paths. Comments/string literals
  are blanked without changing line offsets. Every matching code line and
  same-name `assume_specification` target candidate is retained; zero matches
  are explicit. Hits, including macro-template hits, are inspection evidence,
  **not** automatic receiver resolution or coverage.
* The audited mapping fails closed if the vstd Rust-file tree digest or the
  stable canonical API identity set changes. No previous campaign labels,
  specifications, or proofs are inputs. A new baseline needs a new inspection,
  not silently regenerated negative labels.

Bounded mapping replay, without rereading or rewriting the Rust ownership
inventory, writes only `apis.tsv` and the three `vstd_*.tsv` tables:

```sh
python3 -B scripts/generate_inventory.py --vstd-only
```

Full regeneration also preserves/recomputes this selected-baseline mapping:

```sh
python3 -B scripts/generate_inventory.py
python3 -B -m unittest discover -s tests -p 'test_inventory.py'
```

The inventory tests check persisted regeneration, exact spans and baseline
bytes, replayed absence evidence, receiver false positives, partial indexing
domains, generic-trait distinctions, and the bounded CLI's write set.
**25 tests passed**. These are inventory/replay tests, not correctness,
completeness, runtime behavior, or Verus frontend capability tests. An upstream
vstd assumption is never a current Rust 1.96 source-body correctness proof.
