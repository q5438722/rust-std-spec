# Slice trust-boundary conditional-completeness results

**Campaign-wide review:** `accepted`

The active authority contains 120 generated Slice contracts. This dossier covers exactly the 62 active `r0_z3=unknown` rows; the 58 active UNSAT rows and 12 exact-vstd rows are excluded.

The retained implementation-proof boundary and the boundary used by each new two-execution obligation are separate columns in the additive crosswalk. No retained whole-target helper is silently promoted into `Boundary_T`.

| Projection | Conditional complete | Conditional incomplete | Missing source-backed model |
|---|---:|---:|---:|
| Exact output | 48 | 12 | 2 |
| Full state / reviewed equivalence | 41 | 19 | 2 |

The only weakened-equivalence rows are 028-030 matching-index search and 080-082 equal-key unstable sort. Rows 078-079 remain `missing-source-backed-model`; their bounded UNSAT obligations are diagnostic only and are not completeness proofs.

| Order | Target | Exact output | Full state / reviewed equivalence | Boundary | Incremental review |
|---:|---|---|---|---|---|
| 008 | `core::slice::align_to` | `conditional-complete` | `conditional-complete` | `evidence/targets/008_core_slice_align_to/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T145107Z.md` |
| 009 | `core::slice::align_to_mut` | `conditional-complete` | `conditional-incomplete` | `evidence/targets/009_core_slice_align_to_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T145107Z.md` |
| 012 | `core::slice::as_chunks` | `conditional-complete` | `conditional-complete` | `evidence/targets/012_core_slice_as_chunks/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T192724Z.md` |
| 013 | `core::slice::as_chunks_mut` | `conditional-complete` | `conditional-incomplete` | `evidence/targets/013_core_slice_as_chunks_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T114621Z.md` |
| 014 | `core::slice::as_chunks_unchecked` | `conditional-complete` | `conditional-complete` | `evidence/targets/014_core_slice_as_chunks_unchecked/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T192724Z.md` |
| 015 | `core::slice::as_chunks_unchecked_mut` | `conditional-complete` | `conditional-incomplete` | `evidence/targets/015_core_slice_as_chunks_unchecked_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T192724Z.md` |
| 017 | `core::slice::as_flattened_mut` | `conditional-complete` | `conditional-incomplete` | `evidence/targets/017_core_slice_as_flattened_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T135004Z.md` |
| 018 | `core::slice::as_mut_array` | `conditional-complete` | `conditional-incomplete` | `evidence/targets/018_core_slice_as_mut_array/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T135004Z.md` |
| 019 | `core::slice::as_mut_ptr` | `conditional-complete` | `conditional-complete` | `evidence/targets/019_core_slice_as_mut_ptr/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T173550Z.md` |
| 020 | `core::slice::as_mut_ptr_range` | `conditional-complete` | `conditional-complete` | `evidence/targets/020_core_slice_as_mut_ptr_range/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T173550Z.md` |
| 021 | `core::slice::as_ptr` | `conditional-complete` | `conditional-complete` | `evidence/targets/021_core_slice_as_ptr/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T173550Z.md` |
| 022 | `core::slice::as_ptr_range` | `conditional-complete` | `conditional-complete` | `evidence/targets/022_core_slice_as_ptr_range/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T133819Z.md` |
| 023 | `core::slice::as_rchunks` | `conditional-complete` | `conditional-complete` | `evidence/targets/023_core_slice_as_rchunks/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T192724Z.md` |
| 024 | `core::slice::as_rchunks_mut` | `conditional-complete` | `conditional-incomplete` | `evidence/targets/024_core_slice_as_rchunks_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T192724Z.md` |
| 025 | `core::slice::assume_init_drop` | `conditional-complete` | `conditional-complete` | `evidence/targets/025_core_slice_assume_init_drop/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T205556Z.md` |
| 026 | `core::slice::assume_init_mut` | `conditional-complete` | `conditional-incomplete` | `evidence/targets/026_core_slice_assume_init_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T205556Z.md` |
| 028 | `core::slice::binary_search` | `conditional-incomplete` | `conditional-incomplete` | `evidence/targets/028_core_slice_binary_search/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T184122Z.md` |
| 029 | `core::slice::binary_search_by` | `conditional-incomplete` | `conditional-incomplete` | `evidence/final_campaign/target_029_boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T110316Z.md` |
| 030 | `core::slice::binary_search_by_key` | `conditional-incomplete` | `conditional-incomplete` | `evidence/targets/030_core_slice_binary_search_by_key/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T184122Z.md` |
| 032 | `core::slice::chunk_by_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/032_core_slice_chunk_by_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T024835Z.md` |
| 035 | `core::slice::chunks_exact_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/035_core_slice_chunks_exact_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T055412Z.md` |
| 036 | `core::slice::chunks_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/036_core_slice_chunks_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T024835Z.md` |
| 037 | `core::slice::clone_from_slice` | `conditional-complete` | `conditional-complete` | `evidence/targets/037_core_slice_clone_from_slice/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T050359Z.md` |
| 039 | `core::slice::element_offset` | `conditional-complete` | `conditional-complete` | `evidence/targets/039_core_slice_element_offset/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T121316Z.md` |
| 043 | `core::slice::fill` | `conditional-complete` | `conditional-complete` | `evidence/targets/043_core_slice_fill/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T050359Z.md` |
| 046 | `core::slice::first_chunk_mut` | `conditional-complete` | `conditional-incomplete` | `evidence/targets/046_core_slice_first_chunk_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T135004Z.md` |
| 047 | `core::slice::from_mut` | `conditional-complete` | `conditional-incomplete` | `evidence/targets/047_core_slice_from_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T135004Z.md` |
| 048 | `core::slice::from_raw_parts` | `conditional-complete` | `conditional-complete` | `evidence/targets/048_core_slice_from_raw_parts/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T102036Z.md` |
| 049 | `core::slice::from_raw_parts_mut` | `conditional-complete` | `conditional-incomplete` | `evidence/targets/049_core_slice_from_raw_parts_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T102036Z.md` |
| 051 | `core::slice::get_disjoint_mut` | `conditional-incomplete` | `conditional-incomplete` | `evidence/targets/051_core_slice_get_disjoint_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T150040Z.md` |
| 052 | `core::slice::get_disjoint_unchecked_mut` | `conditional-incomplete` | `conditional-incomplete` | `evidence/targets/052_core_slice_get_disjoint_unchecked_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T153731Z.md` |
| 053 | `core::slice::get_mut` | `conditional-incomplete` | `conditional-incomplete` | `evidence/targets/053_core_slice_get_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T111757Z.md` |
| 054 | `core::slice::get_unchecked` | `conditional-complete` | `conditional-complete` | `evidence/targets/054_core_slice_get_unchecked/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T111757Z.md` |
| 055 | `core::slice::get_unchecked_mut` | `conditional-incomplete` | `conditional-incomplete` | `evidence/targets/055_core_slice_get_unchecked_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T111757Z.md` |
| 062 | `core::slice::last_chunk_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/062_core_slice_last_chunk_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T064245Z.md` |
| 065 | `core::slice::partition_point` | `conditional-incomplete` | `conditional-incomplete` | `evidence/targets/065_core_slice_partition_point/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T184122Z.md` |
| 068 | `core::slice::rchunks_exact_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/068_core_slice_rchunks_exact_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T055412Z.md` |
| 069 | `core::slice::rchunks_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/069_core_slice_rchunks_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T024835Z.md` |
| 074 | `core::slice::rsplit_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/074_core_slice_rsplit_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T024835Z.md` |
| 076 | `core::slice::rsplitn_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/076_core_slice_rsplitn_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T024835Z.md` |
| 077 | `core::slice::select_nth_unstable` | `conditional-incomplete` | `conditional-complete` | `evidence/targets/077_core_slice_select_nth_unstable/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T225709Z.md` |
| 078 | `core::slice::select_nth_unstable_by` | `missing-source-backed-model` | `missing-source-backed-model` | `evidence/targets/078_core_slice_select_nth_unstable_by/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T014750Z.md` |
| 079 | `core::slice::select_nth_unstable_by_key` | `missing-source-backed-model` | `missing-source-backed-model` | `evidence/targets/079_core_slice_select_nth_unstable_by_key/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T014750Z.md` |
| 080 | `core::slice::sort_unstable` | `conditional-incomplete` | `conditional-complete` | `evidence/targets/080_core_slice_sort_unstable/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T213648Z.md` |
| 081 | `core::slice::sort_unstable_by` | `conditional-incomplete` | `conditional-incomplete` | `evidence/targets/081_core_slice_sort_unstable_by/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T125401Z.md` |
| 082 | `core::slice::sort_unstable_by_key` | `conditional-incomplete` | `conditional-complete` | `evidence/targets/082_core_slice_sort_unstable_by_key/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T213648Z.md` |
| 085 | `core::slice::split_at_mut_checked` | `conditional-complete` | `conditional-complete` | `evidence/targets/085_core_slice_split_at_mut_checked/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T072051Z.md` |
| 086 | `core::slice::split_at_mut_unchecked` | `conditional-complete` | `conditional-complete` | `evidence/targets/086_core_slice_split_at_mut_unchecked/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T072051Z.md` |
| 090 | `core::slice::split_first_chunk_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/090_core_slice_split_first_chunk_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T064245Z.md` |
| 091 | `core::slice::split_first_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/091_core_slice_split_first_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T034008Z.md` |
| 093 | `core::slice::split_inclusive_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/093_core_slice_split_inclusive_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T024835Z.md` |
| 096 | `core::slice::split_last_chunk_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/096_core_slice_split_last_chunk_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T064245Z.md` |
| 097 | `core::slice::split_last_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/097_core_slice_split_last_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T034008Z.md` |
| 098 | `core::slice::split_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/098_core_slice_split_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T024835Z.md` |
| 099 | `core::slice::split_off` | `conditional-complete` | `conditional-complete` | `evidence/targets/099_core_slice_split_off/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T080418Z.md` |
| 101 | `core::slice::split_off_first_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/101_core_slice_split_off_first_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T034008Z.md` |
| 103 | `core::slice::split_off_last_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/103_core_slice_split_off_last_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T034008Z.md` |
| 104 | `core::slice::split_off_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/104_core_slice_split_off_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T080418Z.md` |
| 106 | `core::slice::splitn_mut` | `conditional-complete` | `conditional-complete` | `evidence/targets/106_core_slice_splitn_mut/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T122239Z.md` |
| 111 | `core::slice::subslice_range` | `conditional-complete` | `conditional-complete` | `evidence/targets/111_core_slice_subslice_range/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260901T121316Z.md` |
| 119 | `core::slice::write_clone_of_slice` | `conditional-complete` | `conditional-complete` | `evidence/targets/119_core_slice_write_clone_of_slice/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T205556Z.md` |
| 120 | `core::slice::write_copy_of_slice` | `conditional-complete` | `conditional-complete` | `evidence/targets/120_core_slice_write_copy_of_slice/boundary_manifest.json` | `review/REVIEW_ACCEPTANCE_20260831T142401Z.md` |

A classification of `conditional-complete` is backed by the row's direct UNSAT theorem capture. A classification of `conditional-incomplete` is backed by a fixed-input, fixed-boundary SAT model retained in the row's witness index.
