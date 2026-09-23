---
title: Optional mutable endpoint observations
description: Complete first_mut and last_mut value observations, optional caller writes, exact vstd correspondence and the separate source-conversion boundary.
---

# Optional mutable endpoint observations

Rust 1.96 `slice/mod.rs:159-180,285-306` defines the first and last mutable
element borrows. Both methods are unconstrained in `T`, tie the returned
`Option<&mut T>` to the input lifetime, and are const-stable since 1.83.0.
The selected vstd already registers their exact public contracts at
`std_specs/slice.rs:498-513`; the project must not register them again.

The pure candidate in
[`specs/slice/mutable_endpoints.rs`](../../../../../specs/slice/mutable_endpoints.rs)
observes the initial input `Seq<T>`, the initial return variant and full
element value, the caller's final borrowed value, and the entire input
returned after the borrow. For a nonempty initial sequence `s`, position
`i` is zero or `s.len() - 1`, and the complete relation is:

```text
initial return = Some(s[i])
final input = s.update(i, written)
```

The nonempty condition remains explicit: a spec index alone does not imply
its bounds. The update already determines final length and every unborrowed
position. Those consequences need no additional candidate postconditions.
Initial and caller-final element values are independent; equality between
them would wrongly prohibit writes permitted by the documentation.

## The optional caller value is an input, not the final owner

The active checker entries in
[`inputs/first_mut.rs`](../../../../../proofs/completeness/slice/inputs/first_mut.rs)
and [`inputs/last_mut.rs`](../../../../../proofs/completeness/slice/inputs/last_mut.rs)
take `Ghost<Seq<T>>` for the initial slice and `Ghost<Option<T>>` for the
caller's final borrowed element. Their compared result is
`Ghost<(Option<T>, Seq<T>)>`: the initial returned observation and the whole
final input. The latter is never supplied as an input or assumed frame.

The caller Option retains the method's original return variant, not the
later state of a caller-local Option variable. Its `None` branch corresponds
exactly to empty input. It supplies no `T` in that branch, so empty slices
do not acquire an inhabitation requirement. Every `Some(written)` is allowed
on a nonempty initial sequence.

[`mutable_endpoints_state.rs`](../../../../../proofs/completeness/slice/mutable_endpoints_state.rs)
proves this shape from the candidate, equivalence to the unchanged vstd
contracts, and a satisfying output for every such caller choice. It also
derives complete frame/length properties and equates the full value
comparison with Option variant/element equality and sequence extensional
equality. A parameterless generic empty witness and changed-value
regressions are in
[`tests/mutable_endpoint_state.rs`](../../../../../tests/mutable_endpoint_state.rs).

The installed checker rejects direct `Option<&mut T>` extraction. Its
value-state comparisons retain the Option variant, entire initial element
and entire final sequence. For these entries the original query has 13
search guards, all disabled: input length, caller Option shape, both
outputs' Option/sequence shapes, and output inequality. The only excluded
representation is the erased `Ghost` carrier. This does not exclude either
tuple component or any element. The exact limit, generated comparisons and
input correspondence are recorded in
[S-MUT-RETURN](../../../../../issues/S-MUT-RETURN.md#optional-mutable-endpoint-observations).

The selective `scripts/export_completeness.py --mutable-endpoints` command
validates the current compiled source copies and both retained checker runs
before writing either selected API. It compares current predicates/state
inputs with frozen and native copies, requires the exact full comparison
and 13 disabled guards, and copies the generated checker source with only
its relative state import relocated. Unselected raw TSV rows and existing
proofs are preserved. A failed, zero-target, stale, UNKNOWN or incomplete
writeback result is rejected without writing selected outputs.
The real CLI tests are in
[`test_mutable_endpoint_export_cli.py`](../../../../../tests/test_mutable_endpoint_export_cli.py);
their temporary project roots honor `TMPDIR`, and
`MUTABLE_ENDPOINT_EXPORT_TEST_LOG_DIR` can place retained command/results
under review scratch. Input-only `Ghost` values are not public API changes.

## Source correspondence is a separate obligation

The existing `usize` mutable-index contract at
`std_specs/slice.rs:17-35` relates both the initial pointee and the complete
final slice update. Verus's built-in mutable slice indexing uses its existing
`spec_slice_index` and `spec_slice_update` view relationships. These are
upstream trust dependencies, not project proofs of Rust metadata or indexing.

The authoritative bodies use mutable slice patterns. Their independently
permitted length/index translations and the exclusive-place/lifetime argument are
confined to
[V-SLICE-PATTERN](../../../../../issues/V-SLICE-PATTERN.md#proposed-mutable-endpoint-conversions).
Permission covers only the two exact current proof-body replacements, not
canonical Rust or other APIs. The source proofs import only the pure candidate and never call
or assume the target method. The existing
[shared endpoint permission](endpoint-source-correspondence.md) does not
extend to mutable borrowing.

The [native output description](native-output-locations.md#adopted-mutable-endpoint-comparisons)
identifies the separate authority/current/public comparison. Real writes,
whole-slice frames, const compilation and lifetime/conflict rejections
complement, rather than replace, source correspondence and completeness.
