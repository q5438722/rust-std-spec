---
title: Split remainder source dependencies
description: The two permitted split conversions, Rust 1.96 remainder origins and const dependencies, and complete tuple observations.
---

# Split remainder source dependencies

The canonical Rust 1.96 file is
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src/slice/mod.rs`.
Its `split_first` at 182-200 and `split_last` at 224-242 have shared receivers,
unconstrained `T`, const signatures and the exact result `Option<(&T, &[T])>`.
Both returned lifetimes are tied to the input. The last method returns
`(last, init)`, not `(init, last)`.

For a legal slice of length `n`, the one-element/rest patterns match exactly
when `n >= 1`. On that branch the first result borrows input element zero and
range `[1, n)`; the last result borrows input element `n - 1` and range
`[0, n - 1)`. At length one, the first empty remainder begins at the input's
one-past position and the last begins at its start. Zero-sized elements do not
make these element ranges interchangeable merely because addresses coincide.

The versioned Rust MIR definition of `ConstantIndex` and `Subslice` is retained
in
[`.argus/sources/d30066527f26d75ae5d1fd58.txt:1225-1267`](../../../../../.argus/sources/d30066527f26d75ae5d1fd58.txt).
For slices, the latter projects `[from, n - to)`, with `from_end = true`.
The [versioned pattern rules](../../../../../.argus/sources/74d2d8be6f6312a91e3caccc.txt)
establish the nonempty condition and shared reference bindings; the
[lifetime-elision rules](../../../../../.argus/sources/3710179701fb89b97071de07.txt)
bind both returned references to the input.

## Shared `split_at` is a Rust 1.96 const dependency

`split_at` is documented at 1913-1945 and implemented at 1952-1957. For
`mid <= n` its two ordered ranges are `[0, mid)` and `[mid, n)`; otherwise it
panics. It is const-stable since 1.71.0, which supports the required 1.96
baseline but does not imply const compatibility with 1.56-1.70.

The body delegates to `split_at_checked` at 2153-2161, which guards
`mid <= self.len()` before calling `split_at_unchecked` at 2038-2054.
The unchecked body derives `ptr` from that same slice and constructs
`(from_raw_parts(ptr, mid), from_raw_parts(ptr.add(mid), len - mid))`.
Its source spells the safe subtraction as `unchecked_sub(len, mid)`.
The safe caller's bound justifies it. Both delegates are const-callable in
Rust 1.96.

This source trace identifies remainder origin as well as sequence contents.
`as_ptr` at 694-728 derives the pointer from the input; `ptr/docs/add.md`
specifies element-unit offsets; `slice/raw.rs:6-40,124-140` gives the validity,
extent and shared-lifetime rules. For a legal input and `0 <= mid <= n`,
the subranges remain in the original extent. For zero-sized `T`, the byte
offset is zero but slice length metadata still records the element extent.

## The selected Verus boundary is a value contract

The selected unmodified vstd provides the following dependencies:

| Declaration | Meaning and limit |
|---|---|
| `vstd/slice.rs:13-17` | `View for [T]` is `Seq<T>` |
| `vstd/slice.rs:71-87` | Existing length specification and its sequence-length relation; not a proof of Rust pointer metadata |
| `vstd/slice.rs:186-193` | Built-in shared indexing relates an in-range borrowed value to the sequence element |
| `vstd/std_specs/slice.rs:516-523` | Existing `split_at` specification requires the split bound and returns the full left and right sequence subranges with `no_unwind` |

These paths are relative to
[`toolchain/upstream/source/`](../../../../../toolchain/upstream/source/).
The `split_at` declaration does not prove the implementation of `split_at`
and does not state pointer-origin equality. Borrowed-place correspondence
therefore also needs the canonical source and language projections; a proof
of equal output sequences or a native address comparison alone is insufficient.

The existing split candidates in
[`specs/slice/mod.rs`](../../../../../specs/slice/mod.rs) observe the Option
variant, complete endpoint value and entire ordered remainder. The selected
`Seq::subrange` has a recommended in-range domain
(`vstd/seq.rs:1088-1104`); its length and indexing lemmas require that domain
(`1702-1709,1738-1747`). Equality to a spec subrange does not establish those
bounds by itself.

The only permitted current split proof-copy bodies are:

```rust
if slice.len() == 0 {
    None
} else {
    Some((&slice[0], slice.split_at(1).1))
}
```

```rust
if slice.len() == 0 {
    None
} else {
    let i = slice.len() - 1;
    Some((&slice[i], slice.split_at(i).0))
}
```

Their exact difference, source correspondence and limited permission are
recorded in [V-SLICE-PATTERN](../../../../../issues/V-SLICE-PATTERN.md#independent-split-permission-before-adoption).
They leave the candidate and public signature unchanged and are distinct from the
[endpoint conversions](endpoint-source-correspondence.md).
The [native output description](native-output-locations.md#adopted-split-comparisons)
defines which authoritative and current source inputs are compared.

## Complete tuple observations introduce four additional search guards

On the selected specdet 0.3.0, each unchanged split declaration generates a
comparison of the Option variant, logical element value at tuple position 0
and extensional slice equality at position 1:

```rust
((r1 is Some) == (r2 is Some))
    && ((r1 is Some) ==>
        ((r1->Some_0.0 == r2->Some_0.0) && (r1->Some_0.1 =~= r2->Some_0.1)))
```

The existing `axiom_slice_ext_equal` at `vstd/slice.rs:170-174` relates that
slice equality to the length and every corresponding element. It observes
the full ordered remainder, not only a length or pointer address.

The original queries have eleven search guards: `g_slice_leneq`,
`g_slice_lenrng`, both `g_r1_is_{Some,None}` and `g_r2_is_{Some,None}`,
`g_r1__Some_0_1_leneq`, `g_r1__Some_0_1_lenrng`,
`g_r2__Some_0_1_leneq`, `g_r2__Some_0_1_lenrng`, and `g_neq_tuple`.
An unrestricted original query disables all eleven. The seven-guard endpoint
shape cannot be assumed for tuple returns containing slices.
The actual generated inputs and queries are under
[`logs/splits/completeness/`](../../../../../logs/splits/completeness/).

Discovery distinguishes the original function at line 6 from the contract
declaration at line 13 by `kind`. The selectors for these unchanged declarations
are `proofs/completeness/slice/inputs/split_first.rs:split_first@13` and
`proofs/completeness/slice/inputs/split_last.rs:split_last@13`.
Reexecution preserves the analyzed selection without a configuration override,
as described for [the checker selector](endpoint-source-correspondence.md#the-checker-selector-belongs-to-the-analyzed-run).

`scripts/export_completeness.py --splits [split_first split_last]` validates
current compiled source results, both actual checker executions, their input
contents, full comparisons and all disabled guards before updating only the
selected source-result cells. It preserves existing completeness cells/files
and unselected raw TSV records. The same checked source results are used by
the default exporter rather than restoring the historical syntax failures.
