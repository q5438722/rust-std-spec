# Specifications grouped by original Rust source file

This edition reorganizes the [original two-file collection](../README.md).
No API guarantee, generic domain, conditional guard or historical proof scope
is changed. The original `slice.rs` and `vec.rs` remain untouched.

| Contract file | Original Rust 1.96 implementation source | API declarations |
|---|---|---:|
| [`slice_mod.rs`](slice_mod.rs) | `core/src/slice/mod.rs` | 23 |
| [`slice_non_mod.rs`](slice_non_mod.rs) | Other slice files, including `iter.rs`, `iter/macros.rs`, `ascii.rs` | 39 |
| [`vec_mod.rs`](vec_mod.rs) | `alloc/src/vec/mod.rs` | 7 |
| [`vec_non_mod.rs`](vec_non_mod.rs) | Other vec files, including `partial_eq.rs`, `cow.rs`, `into_iter.rs` | 29 |
| Total | Same collected API set | 98 |

Classification follows the implementation/origin location in the canonical
inventory, not the `Self` type, the containing proof file or the trait's
declaration location. Thus the `&[T] != Vec<U,A>` implementation is in
`vec_non_mod.rs` because Rust defines it in `alloc/src/vec/partial_eq.rs`.
Trait implementations originating in root `mod.rs` remain in the `*_mod.rs`
group. Derived methods use the source location of the deriving type; they are
not reclassified according to the core trait declaration.

[`slice_shared.rs`](slice_shared.rs) contains shared value/state views and
external type registrations exactly once, with **zero API declarations**.
Both slice groups use it. Keep this file with the four contract files.
The `lib.rs` entry point loads all five modules; do not also import the
original two-file edition, which would duplicate API registrations.

Example crate layout:

```rust
#![feature(allocator_api)]

pub mod slice_shared;
pub mod slice_mod;
pub mod slice_non_mod;
pub mod vec_mod;
pub mod vec_non_mod;
```

[`api_index.tsv`](api_index.tsv) adds the exact source file/span and the new
location for every represented identity, including the 17 upstream-reused
entries that are not redeclared. [`source_mapping.json`](source_mapping.json)
records the original declaration locations/hashes and the source partition.

Reproduce and check in the existing pinned environment:

```sh
python3 -B scripts/split_by_source.py --check
python3 -B scripts/check_split.py
```

`validation.json` records declaration compatibility, the same 98 real-call
clients, concrete content/writeback examples and expected non-vacuity failures.
These are reorganization checks, not new std implementation proofs. The
original collection's selected-observation and conditional-equality scope
notes still apply.
