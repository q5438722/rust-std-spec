# B16 spec/helper index

| Targets | Required helper functions |
| --- | --- |
| `split_first`, `split_first_mut`, `split_last`, `split_last_mut` | Built-in `Seq`, `subrange`, `old`, and `final` vocabulary |
| `split_off_first`, `split_off_first_mut` | `slice_split_off_first_result` |
| `split_off_last`, `split_off_last_mut` | `slice_split_off_last_result` |
| `chunks_exact`, `ChunksExact::remainder` | `SliceIteratorView`, `slice_iterator_view`, `slice_iterator_well_formed`, `slice_chunk_partition` |
| `rchunks_exact`, `RChunksExact::remainder` | `SliceIteratorView`, `slice_iterator_view`, `slice_iterator_well_formed`, `slice_chunk_partition` |
| `trim_ascii_start` | `ascii_is_whitespace`, `ascii_trim_start_boundary`, `ascii_trim_start_index`, `ascii_trim_start_result` |
| `trim_ascii_end` | `ascii_is_whitespace`, `ascii_trim_end_boundary`, `ascii_trim_end_index`, `ascii_trim_end_result` |
| `make_ascii_lowercase` | `ascii_is_uppercase`, `ascii_lower_byte`, `ascii_lower_seq` |
| `make_ascii_uppercase` | `ascii_is_lowercase`, `ascii_upper_byte`, `ascii_upper_seq` |
