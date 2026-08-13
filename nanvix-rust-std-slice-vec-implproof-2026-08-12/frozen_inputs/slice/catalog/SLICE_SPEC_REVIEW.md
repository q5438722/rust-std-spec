# Slice Spec Evidence Review

## Independent audit result

The isolated `core::slice` artifact set accounts for all 132 stable executable API rows: 12 copied existing-vstd baseline rows and 120 generated executable Verus `assume_specification` attempts. The 120 generated rows now record Rust std feedback-pipeline determinism evidence generated from synthetic `__rust_std_candidate` exec specifications, not the old direct assume-specification harness path.

Relational or source-nondeterministic contracts are preserved as written; `SAT`/`UNKNOWN` outcomes are recorded honestly rather than strengthened away.

## Audited totals

| Metric | Count |
| --- | ---: |
| Catalog rows / stable unique `core::slice` exec APIs | 132 |
| Existing vstd baseline rows preserved | 12 |
| New generated contracts attempted | 120 |
| New generated contracts with Verus typecheck pass | 120 |
| New generated contracts with Verus typecheck fail | 0 |
| Determinism `R0=UNSAT` | 45 |
| Determinism `R0=SAT` | 0 |
| Determinism `R0=UNKNOWN` | 75 |
| Determinism unsupported | 0 |
| Determinism Verus error | 0 |
| Determinism runner crash | 0 |
| Remaining unconverted non-vstd rows | 0 |
| Justified-no-spec rows | 0 |
| Stale `Verus typecheck pending` catalog rows | 0 |

## Semantic-family outcomes

| Semantic family | Rows | UNSAT | SAT | UNKNOWN | unsupported | Verus error | runner crash |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ascii-byte-sequence | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| basic-observation-and-conversion | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| iterator-splitting-and-chunking | 59 | 18 | 0 | 41 | 0 | 0 | 0 |
| maybe-uninit-slice-storage | 5 | 1 | 0 | 4 | 0 | 0 | 0 |
| mutation-frame-and-permutation | 10 | 6 | 0 | 4 | 0 | 0 | 0 |
| raw-pointer-and-provenance | 14 | 1 | 0 | 13 | 0 | 0 | 0 |
| search-prefix-suffix-ordering | 13 | 9 | 0 | 4 | 0 | 0 | 0 |
| sorting-and-selection | 6 | 0 | 0 | 6 | 0 | 0 | 0 |
| views-and-fixed-subranges | 4 | 2 | 0 | 2 | 0 | 0 | 0 |

## UNKNOWN reason taxonomy

Every current `R0=UNKNOWN` generated row carries an `unknown_reason_class` in the manifest entry, result JSON, catalog/spec determinism text, and review table. These labels explain why the source-backed relational contract remains inconclusive without strengthening source-nondeterministic behavior.

| UNKNOWN reason class | Rows | Review reason |
| --- | ---: | --- |
| `clone-or-callback-effect-boundary` | 2 | Clone/FnMut effects are modeled by source-order observation relations, so the contract preserves effect nondeterminism instead of choosing outputs |
| `disjoint-mutable-alias-boundary` | 2 | disjoint mutable-reference arrays preserve source aliasing and post-state relations, but reference identity is not uniquely fixed by the contract |
| `duplicate-or-callback-search-boundary` | 4 | search result is source-backed but relational: duplicate matches, insertion points, or callback/predicate observations do not force a unique return |
| `iterator-or-subslice-state-boundary` | 41 | contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state |
| `maybeuninit-storage-boundary` | 4 | MaybeUninit initialization/storage state is modeled relationally through a raw-storage view and cannot be collapsed to one unique concrete value |
| `mutable-reference-view-boundary` | 3 | contract fixes the Seq view and old/final frame, but mutable reference identity and alias/lifetime state are not uniquely determined by that view |
| `raw-pointer-provenance-boundary` | 13 | pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view |
| `unstable-sort-or-selection-boundary` | 6 | unstable sort/select APIs guarantee ordering or partition plus permutation, not a unique permutation for equal keys or pivot-equivalent elements |

## UNKNOWN target classifications

| Target | Semantic family | UNKNOWN reason class |
| --- | --- | --- |
| `core::slice::align_to` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::align_to_mut` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::array_windows` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::as_chunks` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::as_chunks_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::as_chunks_unchecked` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::as_chunks_unchecked_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::as_flattened_mut` | views-and-fixed-subranges | `mutable-reference-view-boundary` |
| `core::slice::as_mut_array` | views-and-fixed-subranges | `mutable-reference-view-boundary` |
| `core::slice::as_mut_ptr` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::as_mut_ptr_range` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::as_ptr` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::as_ptr_range` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::as_rchunks` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::as_rchunks_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::assume_init_drop` | maybe-uninit-slice-storage | `maybeuninit-storage-boundary` |
| `core::slice::assume_init_mut` | maybe-uninit-slice-storage | `maybeuninit-storage-boundary` |
| `core::slice::binary_search` | search-prefix-suffix-ordering | `duplicate-or-callback-search-boundary` |
| `core::slice::binary_search_by` | search-prefix-suffix-ordering | `duplicate-or-callback-search-boundary` |
| `core::slice::binary_search_by_key` | search-prefix-suffix-ordering | `duplicate-or-callback-search-boundary` |
| `core::slice::chunk_by` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::chunk_by_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::chunks` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::chunks_exact` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::chunks_exact_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::chunks_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::clone_from_slice` | mutation-frame-and-permutation | `clone-or-callback-effect-boundary` |
| `core::slice::element_offset` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::fill` | mutation-frame-and-permutation | `clone-or-callback-effect-boundary` |
| `core::slice::first_chunk_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::from_mut` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::from_raw_parts` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::from_raw_parts_mut` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::get_disjoint_mut` | mutation-frame-and-permutation | `disjoint-mutable-alias-boundary` |
| `core::slice::get_disjoint_unchecked_mut` | mutation-frame-and-permutation | `disjoint-mutable-alias-boundary` |
| `core::slice::get_mut` | basic-observation-and-conversion | `mutable-reference-view-boundary` |
| `core::slice::get_unchecked` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::get_unchecked_mut` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::last_chunk_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::partition_point` | search-prefix-suffix-ordering | `duplicate-or-callback-search-boundary` |
| `core::slice::rchunks` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::rchunks_exact` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::rchunks_exact_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::rchunks_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::rsplit` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::rsplit_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::rsplitn` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::rsplitn_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::select_nth_unstable` | sorting-and-selection | `unstable-sort-or-selection-boundary` |
| `core::slice::select_nth_unstable_by` | sorting-and-selection | `unstable-sort-or-selection-boundary` |
| `core::slice::select_nth_unstable_by_key` | sorting-and-selection | `unstable-sort-or-selection-boundary` |
| `core::slice::sort_unstable` | sorting-and-selection | `unstable-sort-or-selection-boundary` |
| `core::slice::sort_unstable_by` | sorting-and-selection | `unstable-sort-or-selection-boundary` |
| `core::slice::sort_unstable_by_key` | sorting-and-selection | `unstable-sort-or-selection-boundary` |
| `core::slice::split` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_at_mut_checked` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_at_mut_unchecked` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_first_chunk_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_first_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_inclusive` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_inclusive_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_last_chunk_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_last_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_off` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_off_first_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_off_last_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::split_off_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::splitn` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::splitn_mut` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::subslice_range` | raw-pointer-and-provenance | `raw-pointer-provenance-boundary` |
| `core::slice::utf8_chunks` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::windows` | iterator-splitting-and-chunking | `iterator-or-subslice-state-boundary` |
| `core::slice::write_clone_of_slice` | maybe-uninit-slice-storage | `maybeuninit-storage-boundary` |
| `core::slice::write_copy_of_slice` | maybe-uninit-slice-storage | `maybeuninit-storage-boundary` |

## Machine evidence audited

Latest feedback-pipeline manifest: `verification/evidence/slice_feedback_determinism/all-20260811T1415Z-select-nth-result-shape/run_manifest.json`.
Per-target evidence directories live under `verification/evidence/slice_feedback_determinism/all-20260811T1415Z-select-nth-result-shape` and include `synthetic_spec.rs`, `det_spec.json`, `det_harness.rs`, Verus stdout/stderr aliases, schema-search evidence when `r0_z3` is produced, `candidate.json`, and complete `result.json` payloads.

Status counts: `{'ok': 120}`.
R0 counts: `{'unknown': 75, 'unsat': 45}`.

The generated catalog rows reference feedback-pipeline result JSONs and no generated catalog determinism row relies on legacy direct assume-specification evidence.

## Shared vocabulary audit

`verification/check_contracts.py` audits the 41 shared vocabulary helpers that were originally uninterpreted and rejects any unaudited `pub uninterp spec fn` added to `specs/slice_shared_vocabulary.rs`. The enforced classification is: 10 source-backed helpers, 7 law-constrained observation/state abstractions, and 24 irreducible boundary abstractions.

The source-backed replacements are `slice_multiplicity`, `array_ref_view`, `array_mut_ref_view`, `array_value_view`, `flatten_array_chunks`, `ascii_lower_byte`, `ascii_upper_byte`, `ascii_trim_start_index`, `ascii_trim_end_index`, and `ascii_escape_seq`. `slice_multiplicity` is tied to `Seq::to_multiset().count`, fixed-array/chunk flattening is tied to Verus array views, ASCII case/trim helpers are tied to the byte ranges and leading/trailing whitespace searches used by `core/src/slice/ascii.rs`, `core::slice::trim_ascii` now uses the source-body composition relation `ascii_trim_source_body_result`, and `ascii_escape_seq` models the Rust 1.96 `escape_default` byte cases plus slice `escape_ascii` flat-map behavior.

The focused no-update feedback smoke `verification/evidence/slice_feedback_determinism/ascii-escape-source-backed-smoke-20260811T1235Z` ran `core::slice::escape_ascii` with the source-backed escape helper and reached `status=ok`, `r0_z3=unsat`.

The law-constrained helpers are `partial_eq_observed`, `zero_arg_fnmut_outputs`, `ord_cmp_observed`, `partial_ord_leq_observed`, `comparator_ordering_observed`, `comparator_observation`, and `slice_iterator_view`. The shared vocabulary now includes broadcast axiom laws for PartialEq symmetry/transitivity, zero-arg FnMut output length, Ord duality/totality/transitivity and equality correspondence, PartialOrd equality/antisymmetry/transitivity, comparator observation domain plus Ordering-return/reflexive/dual/total-preorder laws, and iterator/chunk well-formedness/partition structure.

`slice_pattern_view`, the arbitrary FnMut callback observations (`fnmut_ordering_observed`, `fnmut_key_observed`, `fnmut_predicate_observed`, `fnmut_adjacent_predicate_observed`, `fnmut_adjacent_bool_outputs`, and `fnmut_adjacent_key_outputs`), raw-pointer/provenance helpers, SliceIndex/GetDisjointMutIndex helpers, and the active MaybeUninit sequence relation helper remain classified as irreducible boundary abstractions because their source semantics depend on callback traces, pointer provenance, layout, initialization state, or trait-associated behavior that is not recoverable from a pure `Seq` slice view. The `is_sorted_by` and `is_sorted_by_key` contracts now consume these source-order adjacent call traces instead of all-pairs/extensional callback or key observations.
