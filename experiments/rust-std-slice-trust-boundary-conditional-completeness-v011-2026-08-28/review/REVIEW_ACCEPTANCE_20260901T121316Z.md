# Independent Reviewer decision: address-derived slice observers

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T12:13:16Z

This decision covers only input orders 039 `core::slice::element_offset` and
111 `core::slice::subslice_range` against the independently accepted
54-target baseline. It does not authorize a Manager stage transition.

## Readable semantic review

The Reviewer inspected both literal active generated declarations, their
opaque generated vocabulary, the Rust 1.96 implementations and public docs,
both frozen implementation-proof harnesses, the source-body, transformation,
dependency, and bound-input manifests for both targets, all 27 trust records,
the generated SMT obligations, the target-local Verus models, and the retained
solver captures.

The active contracts remain the original normal-return implications through
`slice_element_offset_option_result` and
`slice_subslice_range_option_result`. The replacement does not declare the
opaque vocabulary to Z3 and does not conjoin a source-selected return outside
those implications. Instead, defined transitions implement the source order:
ZST panic, slice pointer extraction, `ptr::from_ref` for target 039, exposed
addresses, machine-usize wrapping subtraction, element-size alignment,
division, wrapping end addition for target 111, exact bounds decisions, and
algebraic `None`/`Some` construction.

The retained complete-branch bridges remain inadmissible:
`TS-039-D006`, `TS-039-E003`, `TS-039-E004`, `TS-039-E005`,
`TS-111-D006`, `TS-111-E002`, `TS-111-E003`, and `TS-111-E004`.
They are excluded and replaced by the defined source transition rather than
renamed or admitted. The remaining sites are either context-only provenance
records or lower pointer/layout/panic observations. No uninterpreted
functionality relation, result bridge, output-bearing boundary field, final
state, branch truth, computed offset/range, answer encoding, or target trace
enters `Boundary_T`.

Both theorem projections use one shared valid `x` and one shared `b`.
`Requires_T` adds only nonnegative integer-representation conditions;
reference, allocation, provenance, liveness, layout, and machine-width
validity are checked from genuine initial observations in `Boundary_T`.
Offsets, ranges, branch results, and outputs are computed afterward. Exact
output equivalence compares the complete panic/`None`/`Some` algebraic return.
Full-state equivalence additionally compares the unchanged memory identity;
no observation is weakened.

The source cases cover same-allocation starts and interiors, distinct
allocations, stride misalignment, pointer-before-receiver wrapping, exact end,
later out-of-bounds pointers, machine-width limits, invalid reference
representations, and ZST panic behavior. Target 111's documented empty-slice
false positives use distinct zero-length allocations at the receiver's
numeric start and end and deterministically produce `Some(0..0)` and
`Some(4..4)`. Independent adjacent nonzero-allocation probes produced the same
exact ranges and rejected `None`. Quantifier-free canonical-return checks
also rejected any valid boundary with no modeled target result, and a valid
in-domain wrapping range end was impossible under the reference-span limits.

## Independent execution

- Forced Python compilation of `tools` and `tests` completed successfully.
- All 11 focused address-observer tests and all 442 repository tests passed.
- Both target-local Verus files type-checked, then verified two obligations
  with zero errors and no `external_body`.
- Direct final Z3 replay produced four clean theorem `unsat` results, 22
  source-instance `sat` results with models, and 46 invalid or
  wrong-transition `unsat` results.
- The bounded runner and integrated authority validator passed.
- The complete acceptance driver passed all 41 commands with 132 stable Slice
  inventory rows and 12 exact-vstd rows excluded from the generated campaign.

## Preservation and decision

A direct byte-content comparison, independent of retained identifier metadata,
found all 5,236 files in the 54 certified evidence trees unchanged after the
fresh bounded and complete acceptance runs. All 320 frozen input files were
also unchanged, and both crosswalk serializations were stable.

Within the declared bounded model, targets 039 and 111 are accepted as
exact-output and full-state `conditional-complete`. The selected ledger now
contains exactly 56 classified rows and 6 `not-run` rows. Stage transition
remains disabled.
