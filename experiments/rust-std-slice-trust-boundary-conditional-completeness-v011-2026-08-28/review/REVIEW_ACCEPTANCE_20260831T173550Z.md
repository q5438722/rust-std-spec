# Independent Reviewer decision: pointer-cast cluster

**VERDICT: ACCEPT**

**Timestamp:** 2026-08-31T17:35:50Z

## Scope

Input orders 019 `core::slice::as_mut_ptr`, 021 `core::slice::as_ptr`, and
020 `core::slice::as_mut_ptr_range`, in dependency order 019 → 021 → 020.

## Alignment fix assessment

The prior blocker identified that all three `valid_input` specs omitted the
alignment conjunct `input.address % input.element_alignment == 0`, allowing
an otherwise-valid witness with address=1026 and element_alignment=4 (since
1026 mod 4 = 2 ≠ 0).

**Fix confirmed in all three models:**

- `proofs/019_core_slice_as_mut_ptr.rs`: `valid_input` includes
  `&& input.address % input.element_alignment == 0` and the
  `rejects_misaligned_regression_input` proof theorem with
  address=1026, alignment=4 ensuring `!valid_input(input)`.
- `proofs/021_core_slice_as_ptr.rs`: identical fix.
- `proofs/020_core_slice_as_mut_ptr_range.rs`: identical fix.

All three captured models (`evidence/targets/*/verus/source_transition_model.rs`)
are byte-identical to their respective source proofs. No `external_body`
annotations present. Evidence result.json SHA-256 bindings match actual file
hashes for both source and captured models.

Python regression test `test_verus_models_reject_misaligned_regression_input`
in `tests/test_pointer_cast_cluster.py` explicitly asserts the presence of
the alignment conjunct, the regression theorem, and the 1026/4 witness in
all three models. The full 182-test unit suite passes.

## Fresh direct Z3 results

**Obligations (6/6 UNSAT):**

| Target | Obligation | Result |
|--------|-----------|--------|
| 019 | full_exact (completeness) | unsat |
| 019 | exact_output (determinism) | unsat |
| 021 | full_exact (completeness) | unsat |
| 021 | exact_output (determinism) | unsat |
| 020 | full_exact (completeness) | unsat |
| 020 | exact_output (determinism) | unsat |

**Probes (39 total: 15 SAT, 24 UNSAT):**

- 019: 5 SAT (allocated empty/nonempty non-ZST, allocated/dangling ZST,
  dangling empty non-ZST) + 6 UNSAT (null, misaligned, address-len
  synthesis, changed allocation/provenance, mutable state change)
- 021: 5 SAT + 5 UNSAT (null, misaligned, address-len synthesis, changed
  allocation/provenance)
- 020: 5 SAT + 13 UNSAT (null, misaligned, address-len synthesis, changed
  allocation/provenance, mutable state change, address overflow, isize
  exceeded, nonzero offset without allocation/provenance/past-allocation,
  wrong start/end endpoints)

All three `invalid_misaligned_pointer` probes: UNSAT — Z3 confirms
address=1026/alignment=4 is rejected by `valid_input`.

SMT obligations include `(= (mod (x_address x) (x_element_alignment x)) 0)`
in the valid-input definition.

## Fresh direct Verus results

| Model | Result |
|-------|--------|
| 019_core_slice_as_mut_ptr.rs | verification results:: 3 verified, 0 errors |
| 021_core_slice_as_ptr.rs | verification results:: 3 verified, 0 errors |
| 020_core_slice_as_mut_ptr_range.rs | verification results:: 3 verified, 0 errors |

Zero errors, no stderr output, no `external_body`.

## Acceptance capture validation

- `logs/acceptance_manifest.json`: 22 commands, all exit code 0, status=passed.
- Unit test suite: 182 tests, all OK.
- Verus captured verification stdout matches `verification results:: 3 verified,
  0 errors` for all three targets.

## Active contract SHA-256 hashes

- 019: `840c4efc8976016ca0b1c8728d1cabb13529c6e83939e8ca3cbc31232ba6a14a` ✓
- 021: `52c2a91bc8c7e49cd77d4429bb2b2a6e50a788211f2abca511f4df650f1a5edc` ✓
- 020: `0d55922a668ea2e52e07ca14a1146f6ff2d0c9a9d68d9369ff4171f9a6d574c1` ✓

## Preservation and count checks

- **Ordered replay:** `logs/ordered_pointer_cast_cluster_replay.json` reports
  artifact order [019, 021, 020], status=passed.
- **Baseline evidence:** All 8 preserved trees (013, 022, 029, 051, 052, 081,
  106, 120) have before_sha256 == after_sha256 (byte-identical).
- **Crosswalk:** 62 total rows, 11 classified, 51 not-run.
  CSV and JSON both have 62 rows.
- **Result.json:** All three targets classified as conditional-complete for both
  exact-output-determinism and completeness-modulo-reviewed-equivalence.

## Boundary struct inspection

All three Boundary structs contain only permitted initial observations:
allocation, address, provenance, element_size, element_alignment,
allocation_base, allocation_bytes, isize_max, address_space_limit (plus
mutable_identity and frame_token for 019/020). No returned pointers, ranges,
endpoints, final state, target truth, answer encodings, or traces are present.

## Local validator

`tools/validate_authority_design.py` returns `validation=PASS` with
62 unique core_slice targets, 28 admissible + 34 inadmissible boundaries,
6 drift controls, and the expected target results including 51 not-run.

## Stage transition

**No stage transition is authorized by this review.** This decision covers
only the independent verification of the bounded pointer-cast cluster
alignment fix and evidence regeneration.
