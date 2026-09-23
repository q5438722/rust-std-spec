---
title: Endpoint source correspondence
description: The two permitted first/last proof-copy translations, their unchanged value observations, upstream trust boundary and selected checker scope.
---

# Endpoint source correspondence

Rust 1.96 `core/src/slice/mod.rs:140-157,266-283` specifies the first or last
shared element reference and `None` on an empty slice. The canonical bodies
use `[first, ..]` and `[.., last]`; the local source-proof copies may use only:

```rust
if slice.len() == 0 { None } else { Some(&slice[0]) }
if slice.len() == 0 { None } else { Some(&slice[slice.len() - 1]) }
```

For every legal slice length `n`, the original pattern condition is `n >= 1`.
The explicit empty condition is its complement, and the nonempty borrowed
places are exactly zero and `n - 1`. Those branches prove the new index bounds
and subtraction safety; the empty branch evaluates neither operation.
Both forms borrow from the same input with the same lifetime and preserve
stable const use. No element is moved, copied, compared or modified. This
includes non-Copy, non-static and zero-sized elements and legal empty slices
of uninhabited types. Zero-sized position correspondence follows from the
projections, not from addresses.

The unchanged `first_post` and `last_post` observe the Option variant and
complete element value using the selected `View for [T] = Seq<T>`. They do not
assert reference-address determinism. In a Some branch the nonempty condition
cannot be inferred from the element equality: an out-of-range spec sequence
index does not supply a bound. Both conditions are necessary.

The executable source proofs use the existing selected-vstd length contract
and `spec_slice_index`/`axiom_spec_slice_index` relationship. They discharge
their own bounds and arithmetic obligations but do not prove Rust's metadata
implementation or add a trusted assumption. This correspondence is limited
to the two endpoint bodies; it does not establish either split method or
general slice-pattern support.

The exact source mapping, language/MIR primary sources and trust boundary are
recorded in [V-SLICE-PATTERN](../../../../../issues/V-SLICE-PATTERN.md).
The candidates are in [specs/slice/mod.rs](../../../../../specs/slice/mod.rs).
The [native output description](native-output-locations.md#adopted-endpoint-comparisons)
identifies the separate authority/current/public comparison and its limits.

## The checker selector belongs to the analyzed run

On the installed specdet 0.3.0, `replay --run RUN --reexecute` restores the
analyzed run's effective selectors and reexecutes against its frozen workspace.
Passing `--config` instead loads that configuration over the workspace; it
does not automatically reapply a selector supplied only on the analyze CLI.
The implementation is `_restore_config` in
`/home/chentianyu/spec-determinism-tool/src/specdet/cli/main.py:199-239`.

For these unchanged declarations the selectors are
`proofs/completeness/slice/inputs/first.rs:first@13` and
`proofs/completeness/slice/inputs/last.rs:last@13`. Reexecution without a
configuration override preserves the one-endpoint scope. The effective
selector and actual returned target must agree; replaying an unrelated
declaration cannot substitute for the intended proof.

The source-only export mode `scripts/export_completeness.py --endpoints`
checks both executions, actual source/dependency contents, full Option/value
comparison and the original query with all seven search guards disabled.
It preserves the existing completeness files and cells and changes only
the selected source-result cells. It does not turn a successful checker
comparison into an implementation proof.

The focused CLI tests in `tests/test_endpoint_export_cli.py` honor `TMPDIR`
for their temporary project copies. With
`TMPDIR={scratch}/tmp` and
`ENDPOINT_EXPORT_TEST_LOG_DIR={scratch}/export-tests`, independent review can
exercise the real exporter without writing the reviewed workspace. The
temporary directory must exist before the test process starts.
