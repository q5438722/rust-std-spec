# Slice Executable Function Inventory

Inventory gate for stable unique executable APIs under `core::slice`.

## Summary

- Authority: `/home/chentianyu/nanvix-rust-std-spec-survey/nanvix-rust-std-slice-specgen-2026-08-11/results/modules.csv` and `/home/chentianyu/nanvix-rust-std-spec-survey/nanvix-rust-std-slice-specgen-2026-08-11/results/coverage.csv` copied from the canonical survey results.
- Stable unique exec API rows counted: **132**.
- Existing vstd contracts explicitly flagged and integrated: **12**.
- Generated relation specs for previously uncovered stable APIs: **120**.
- Target-specific justified-no-spec rows: **0**.
- Excluded unstable declarations reported by `modules.csv`: **44**.
- Excluded approximate aliases reported by `modules.csv`: **0**.
- Private implementation helpers and non-executable spec helpers are not present in the executable API coverage source and are not counted.

## Existing vstd targets

- `core::slice::copy_from_slice`
- `core::slice::copy_within`
- `core::slice::first`
- `core::slice::first_mut`
- `core::slice::get`
- `core::slice::is_empty`
- `core::slice::iter`
- `core::slice::last`
- `core::slice::last_mut`
- `core::slice::len`
- `core::slice::split_at`
- `core::slice::split_at_mut`

## Inventory rows

| # | Canonical target | Source | Existing vstd | Semantic family | Final status |
|---:|---|---|---|---|---|
| 1 | `core::slice::ChunksExact::remainder` | `core/src/slice/iter.rs:1876` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 2 | `core::slice::ChunksExactMut::into_remainder` | `core/src/slice/iter.rs:2039` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 3 | `core::slice::Iter::as_slice` | `core/src/slice/iter.rs:135` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 4 | `core::slice::IterMut::as_slice` | `core/src/slice/iter.rs:311` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 5 | `core::slice::IterMut::into_slice` | `core/src/slice/iter.rs:274` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 6 | `core::slice::RChunksExact::remainder` | `core/src/slice/iter.rs:2686` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 7 | `core::slice::RChunksExactMut::into_remainder` | `core/src/slice/iter.rs:2855` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 8 | `core::slice::align_to` | `core/src/slice/mod.rs:4506` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 9 | `core::slice::align_to_mut` | `core/src/slice/mod.rs:4571` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 10 | `core::slice::array_windows` | `core/src/slice/mod.rs:1649` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 11 | `core::slice::as_array` | `core/src/slice/mod.rs:853` | uncovered | views-and-fixed-subranges | generated-new-real-relation-spec-static-revalidated |
| 12 | `core::slice::as_chunks` | `core/src/slice/mod.rs:1399` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 13 | `core::slice::as_chunks_mut` | `core/src/slice/mod.rs:1555` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 14 | `core::slice::as_chunks_unchecked` | `core/src/slice/mod.rs:1341` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 15 | `core::slice::as_chunks_unchecked_mut` | `core/src/slice/mod.rs:1501` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 16 | `core::slice::as_flattened` | `core/src/slice/mod.rs:5451` | uncovered | views-and-fixed-subranges | generated-new-real-relation-spec-static-revalidated |
| 17 | `core::slice::as_flattened_mut` | `core/src/slice/mod.rs:5493` | uncovered | views-and-fixed-subranges | generated-new-real-relation-spec-static-revalidated |
| 18 | `core::slice::as_mut_array` | `core/src/slice/mod.rs:872` | uncovered | views-and-fixed-subranges | generated-new-real-relation-spec-static-revalidated |
| 19 | `core::slice::as_mut_ptr` | `core/src/slice/mod.rs:760` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 20 | `core::slice::as_mut_ptr_range` | `core/src/slice/mod.rs:839` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 21 | `core::slice::as_ptr` | `core/src/slice/mod.rs:728` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 22 | `core::slice::as_ptr_range` | `core/src/slice/mod.rs:796` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 23 | `core::slice::as_rchunks` | `core/src/slice/mod.rs:1446` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 24 | `core::slice::as_rchunks_mut` | `core/src/slice/mod.rs:1608` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 25 | `core::slice::assume_init_drop` | `core/src/mem/maybe_uninit.rs:1487` | uncovered | maybe-uninit-slice-storage | generated-new-real-relation-spec-static-revalidated |
| 26 | `core::slice::assume_init_mut` | `core/src/mem/maybe_uninit.rs:1528` | uncovered | maybe-uninit-slice-storage | generated-new-real-relation-spec-static-revalidated |
| 27 | `core::slice::assume_init_ref` | `core/src/mem/maybe_uninit.rs:1509` | uncovered | maybe-uninit-slice-storage | generated-new-real-relation-spec-static-revalidated |
| 28 | `core::slice::binary_search` | `core/src/slice/mod.rs:2925` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 29 | `core::slice::binary_search_by` | `core/src/slice/mod.rs:2976` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 30 | `core::slice::binary_search_by_key` | `core/src/slice/mod.rs:3077` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 31 | `core::slice::chunk_by` | `core/src/slice/mod.rs:1867` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 32 | `core::slice::chunk_by_mut` | `core/src/slice/mod.rs:1909` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 33 | `core::slice::chunks` | `core/src/slice/mod.rs:1158` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 34 | `core::slice::chunks_exact` | `core/src/slice/mod.rs:1245` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 35 | `core::slice::chunks_exact_mut` | `core/src/slice/mod.rs:1293` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 36 | `core::slice::chunks_mut` | `core/src/slice/mod.rs:1202` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 37 | `core::slice::clone_from_slice` | `core/src/slice/mod.rs:4260` | uncovered | mutation-frame-and-permutation | generated-new-real-relation-spec-static-revalidated |
| 38 | `core::slice::contains` | `core/src/slice/mod.rs:2594` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 39 | `core::slice::copy_from_slice` | `core/src/slice/mod.rs:4326` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 40 | `core::slice::copy_within` | `core/src/slice/mod.rs:4361` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 41 | `core::slice::element_offset` | `core/src/slice/mod.rs:5267` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 42 | `core::slice::ends_with` | `core/src/slice/mod.rs:2655` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 43 | `core::slice::eq_ignore_ascii_case` | `core/src/slice/ascii.rs:60` | uncovered | ascii-byte-sequence | generated-new-real-relation-spec-static-revalidated |
| 44 | `core::slice::escape_ascii` | `core/src/slice/ascii.rs:218` | uncovered | ascii-byte-sequence | generated-new-real-relation-spec-static-revalidated |
| 45 | `core::slice::fill` | `core/src/slice/mod.rs:4172` | uncovered | mutation-frame-and-permutation | generated-new-real-relation-spec-static-revalidated |
| 46 | `core::slice::fill_with` | `core/src/slice/mod.rs:4196` | uncovered | mutation-frame-and-permutation | generated-new-real-relation-spec-static-revalidated |
| 47 | `core::slice::first` | `core/src/slice/mod.rs:155` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 48 | `core::slice::first_chunk` | `core/src/slice/mod.rs:327` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 49 | `core::slice::first_chunk_mut` | `core/src/slice/mod.rs:357` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 50 | `core::slice::first_mut` | `core/src/slice/mod.rs:178` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 51 | `core::slice::from_mut` | `core/src/slice/raw.rs:211` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 52 | `core::slice::from_raw_parts` | `core/src/slice/raw.rs:124` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 53 | `core::slice::from_raw_parts_mut` | `core/src/slice/raw.rs:179` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 54 | `core::slice::from_ref` | `core/src/slice/raw.rs:203` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 55 | `core::slice::get` | `core/src/slice/mod.rs:572` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 56 | `core::slice::get_disjoint_mut` | `core/src/slice/mod.rs:5216` | uncovered | mutation-frame-and-permutation | generated-new-real-relation-spec-static-revalidated |
| 57 | `core::slice::get_disjoint_unchecked_mut` | `core/src/slice/mod.rs:5149` | uncovered | mutation-frame-and-permutation | generated-new-real-relation-spec-static-revalidated |
| 58 | `core::slice::get_mut` | `core/src/slice/mod.rs:600` | uncovered | basic-observation-and-conversion | generated-new-real-relation-spec-static-revalidated |
| 59 | `core::slice::get_unchecked` | `core/src/slice/mod.rs:640` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 60 | `core::slice::get_unchecked_mut` | `core/src/slice/mod.rs:686` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 61 | `core::slice::is_ascii` | `core/src/slice/ascii.rs:18` | uncovered | ascii-byte-sequence | generated-new-real-relation-spec-static-revalidated |
| 62 | `core::slice::is_empty` | `core/src/slice/mod.rs:136` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 63 | `core::slice::is_sorted` | `core/src/slice/mod.rs:4735` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 64 | `core::slice::is_sorted_by` | `core/src/slice/mod.rs:4778` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 65 | `core::slice::is_sorted_by_key` | `core/src/slice/mod.rs:4802` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 66 | `core::slice::iter` | `core/src/slice/mod.rs:1043` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 67 | `core::slice::iter_mut` | `core/src/slice/mod.rs:1063` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 68 | `core::slice::last` | `core/src/slice/mod.rs:281` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 69 | `core::slice::last_chunk` | `core/src/slice/mod.rs:509` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 70 | `core::slice::last_chunk_mut` | `core/src/slice/mod.rs:539` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 71 | `core::slice::last_mut` | `core/src/slice/mod.rs:304` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 72 | `core::slice::len` | `core/src/slice/mod.rs:116` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 73 | `core::slice::make_ascii_lowercase` | `core/src/slice/ascii.rs:195` | uncovered | ascii-byte-sequence | generated-new-real-relation-spec-static-revalidated |
| 74 | `core::slice::make_ascii_uppercase` | `core/src/slice/ascii.rs:173` | uncovered | ascii-byte-sequence | generated-new-real-relation-spec-static-revalidated |
| 75 | `core::slice::partition_point` | `core/src/slice/mod.rs:4861` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 76 | `core::slice::rchunks` | `core/src/slice/mod.rs:1689` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 77 | `core::slice::rchunks_exact` | `core/src/slice/mod.rs:1778` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 78 | `core::slice::rchunks_exact_mut` | `core/src/slice/mod.rs:1827` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 79 | `core::slice::rchunks_mut` | `core/src/slice/mod.rs:1733` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 80 | `core::slice::reverse` | `core/src/slice/mod.rs:981` | uncovered | mutation-frame-and-permutation | generated-new-real-relation-spec-static-revalidated |
| 81 | `core::slice::rotate_left` | `core/src/slice/mod.rs:3890` | uncovered | mutation-frame-and-permutation | generated-new-real-relation-spec-static-revalidated |
| 82 | `core::slice::rotate_right` | `core/src/slice/mod.rs:3936` | uncovered | mutation-frame-and-permutation | generated-new-real-relation-spec-static-revalidated |
| 83 | `core::slice::rsplit` | `core/src/slice/mod.rs:2365` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 84 | `core::slice::rsplit_mut` | `core/src/slice/mod.rs:2391` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 85 | `core::slice::rsplitn` | `core/src/slice/mod.rs:2474` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 86 | `core::slice::rsplitn_mut` | `core/src/slice/mod.rs:2501` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 87 | `core::slice::select_nth_unstable` | `core/src/slice/mod.rs:3522` | uncovered | sorting-and-selection | generated-new-real-relation-spec-static-revalidated |
| 88 | `core::slice::select_nth_unstable_by` | `core/src/slice/mod.rs:3587` | uncovered | sorting-and-selection | generated-new-real-relation-spec-static-revalidated |
| 89 | `core::slice::select_nth_unstable_by_key` | `core/src/slice/mod.rs:3654` | uncovered | sorting-and-selection | generated-new-real-relation-spec-static-revalidated |
| 90 | `core::slice::sort_unstable` | `core/src/slice/mod.rs:3139` | uncovered | sorting-and-selection | generated-new-real-relation-spec-static-revalidated |
| 91 | `core::slice::sort_unstable_by` | `core/src/slice/mod.rs:3194` | uncovered | sorting-and-selection | generated-new-real-relation-spec-static-revalidated |
| 92 | `core::slice::sort_unstable_by_key` | `core/src/slice/mod.rs:3246` | uncovered | sorting-and-selection | generated-new-real-relation-spec-static-revalidated |
| 93 | `core::slice::split` | `core/src/slice/mod.rs:2247` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 94 | `core::slice::split_at` | `core/src/slice/mod.rs:1955` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 95 | `core::slice::split_at_checked` | `core/src/slice/mod.rs:2156` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 96 | `core::slice::split_at_mut` | `core/src/slice/mod.rs:1989` | existing-vstd | existing-vstd-baseline | existing-vstd-contract-integrated-and-static-revalidated |
| 97 | `core::slice::split_at_mut_checked` | `core/src/slice/mod.rs:2195` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 98 | `core::slice::split_at_mut_unchecked` | `core/src/slice/mod.rs:2095` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 99 | `core::slice::split_at_unchecked` | `core/src/slice/mod.rs:2041` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 100 | `core::slice::split_first` | `core/src/slice/mod.rs:198` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 101 | `core::slice::split_first_chunk` | `core/src/slice/mod.rs:387` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 102 | `core::slice::split_first_chunk_mut` | `core/src/slice/mod.rs:417` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 103 | `core::slice::split_first_mut` | `core/src/slice/mod.rs:220` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 104 | `core::slice::split_inclusive` | `core/src/slice/mod.rs:2305` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 105 | `core::slice::split_inclusive_mut` | `core/src/slice/mod.rs:2329` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 106 | `core::slice::split_last` | `core/src/slice/mod.rs:240` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 107 | `core::slice::split_last_chunk` | `core/src/slice/mod.rs:447` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 108 | `core::slice::split_last_chunk_mut` | `core/src/slice/mod.rs:478` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 109 | `core::slice::split_last_mut` | `core/src/slice/mod.rs:262` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 110 | `core::slice::split_mut` | `core/src/slice/mod.rs:2269` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 111 | `core::slice::split_off` | `core/src/slice/mod.rs:4913` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 112 | `core::slice::split_off_first` | `core/src/slice/mod.rs:5017` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 113 | `core::slice::split_off_first_mut` | `core/src/slice/mod.rs:5042` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 114 | `core::slice::split_off_last` | `core/src/slice/mod.rs:5067` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 115 | `core::slice::split_off_last_mut` | `core/src/slice/mod.rs:5092` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 116 | `core::slice::split_off_mut` | `core/src/slice/mod.rs:4979` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 117 | `core::slice::splitn` | `core/src/slice/mod.rs:2419` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 118 | `core::slice::splitn_mut` | `core/src/slice/mod.rs:2445` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 119 | `core::slice::starts_with` | `core/src/slice/mod.rs:2624` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 120 | `core::slice::strip_circumfix` | `core/src/slice/mod.rs:2763` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 121 | `core::slice::strip_prefix` | `core/src/slice/mod.rs:2687` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 122 | `core::slice::strip_suffix` | `core/src/slice/mod.rs:2723` | uncovered | search-prefix-suffix-ordering | generated-new-real-relation-spec-static-revalidated |
| 123 | `core::slice::subslice_range` | `core/src/slice/mod.rs:5321` | uncovered | raw-pointer-and-provenance | generated-new-real-relation-spec-static-revalidated |
| 124 | `core::slice::swap` | `core/src/slice/mod.rs:908` | uncovered | mutation-frame-and-permutation | generated-new-real-relation-spec-static-revalidated |
| 125 | `core::slice::swap_with_slice` | `core/src/slice/mod.rs:4429` | uncovered | mutation-frame-and-permutation | generated-new-real-relation-spec-static-revalidated |
| 126 | `core::slice::trim_ascii` | `core/src/slice/ascii.rs:308` | uncovered | ascii-byte-sequence | generated-new-real-relation-spec-static-revalidated |
| 127 | `core::slice::trim_ascii_end` | `core/src/slice/ascii.rs:274` | uncovered | ascii-byte-sequence | generated-new-real-relation-spec-static-revalidated |
| 128 | `core::slice::trim_ascii_start` | `core/src/slice/ascii.rs:241` | uncovered | ascii-byte-sequence | generated-new-real-relation-spec-static-revalidated |
| 129 | `core::slice::utf8_chunks` | `core/src/str/lossy.rs:45` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 130 | `core::slice::windows` | `core/src/slice/mod.rs:1118` | uncovered | iterator-splitting-and-chunking | generated-new-real-relation-spec-static-revalidated |
| 131 | `core::slice::write_clone_of_slice` | `core/src/mem/maybe_uninit.rs:1223` | uncovered | maybe-uninit-slice-storage | generated-new-real-relation-spec-static-revalidated |
| 132 | `core::slice::write_copy_of_slice` | `core/src/mem/maybe_uninit.rs:1163` | uncovered | maybe-uninit-slice-storage | generated-new-real-relation-spec-static-revalidated |
