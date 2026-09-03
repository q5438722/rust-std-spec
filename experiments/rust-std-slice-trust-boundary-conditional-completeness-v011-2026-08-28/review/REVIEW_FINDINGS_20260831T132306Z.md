# Independent Reviewer decision: target 022

**VERDICT: CHANGES REQUESTED**

This decision covers only input order 22, `core::slice::as_ptr_range`. It does
not alter the accepted decisions for targets 013, 029, 081, or 106 and does not
authorize a Manager stage transition.

## Fresh verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

All 15 commands completed successfully. Python compilation was clean, 121
tests ran and reported `OK`, and local validation passed. A focused target-022
run executed 15 tests successfully.

Direct Z3 replay returned `unsat` for both the full exact-equivalence and
exact-output obligations and `sat` for the retained empty non-ZST, nonempty
non-ZST, and nonempty ZST probes. Direct Verus type-checking succeeded, and
verification reported 2 verified obligations and 0 errors with no
`external_body` in the target-specific model.

Content comparisons confirmed that the target-local generated declaration,
slice item, implementation-proof artifacts, and canonical `ptr::add`
implementation and documentation match their bound sources. A target-022
pipeline rerun left all 145 files under the accepted target-013, target-029,
target-081, and target-106 evidence trees byte-for-byte unchanged. The
crosswalk formats agree, contain 62 rows, classify only those four targets and
target 022, and leave exactly 57 rows `not-run`.

## Blocking finding

### R1: `Requires_T` does not model the valid zero-byte pointer domain

`tools/target_022.py:275-277` and
`proofs/022_core_slice_as_ptr_range.rs:62-65` require positive allocation and
provenance identities for every slice, but permit address zero. This conflicts
with the bound Rust semantics:

- `canonical_ptr_add_safety.md:17-19` imposes the allocation/in-bounds
  requirement only when the computed byte offset is nonzero.
- `provenance/frozen/rust-1.96/library/core/src/slice/raw.rs:20-24` requires a
  non-null aligned data pointer even for empty and ZST slices and explicitly
  permits `NonNull::dangling()` for zero-length slices.
- Canonical `core/src/ptr/non_null.rs:129-131` constructs that dangling pointer
  without provenance.

Independent SMT probes against the emitted model produced:

```text
null_address_nonempty_non_zst: sat
dangling_empty_non_zst: unsat
dangling_nonempty_zst: unsat
```

The first case should be outside `Requires_T`; the latter two are valid
zero-byte source cases and should be inside it. Consequently, the clean UNSAT
results establish determinism only for a narrowed, partly invalid domain and
do not yet establish the requested target-wide conditional completeness.

Repair the input and pointer model so address non-nullness is explicit and
allocation/provenance plus in-allocation constraints are conditional on a
nonzero byte offset. Exercise the zero-byte branch with no-provenance dangling
empty and nonempty-ZST probes, and add rejection probes for a null data address
and a nonzero offset without an allocation. Mirror the corrected domain in
the Verus model and regenerated metadata/evidence.

The persistent regression suite also does not directly exercise mutation of
the four prior accepted result rows: `tests/test_target_022.py:191-211`
deliberately selects a row outside `PRESERVED_RESULTS`. The implementation
does reject all four mutations in an independent probe, but that behavior
needs a target-022 regression test to satisfy the stated negative-test gate.

