# Independent Reviewer decision: SliceIndex get trio

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T11:17:57Z

This decision covers only input orders 053 `core::slice::get_mut`, 054
`core::slice::get_unchecked`, and 055
`core::slice::get_unchecked_mut` against the independently accepted 51-target
baseline. It does not authorize a Manager stage transition.

## Readable semantic review

The Reviewer inspected all three active generated declarations, their public
Rust 1.96 wrappers and documentation, the opaque SliceIndex vocabulary, all
applicable implementations in `core/src/slice/index.rs` and
`core/src/index.rs`, the three frozen implementation-proof harnesses, all nine
frozen proof manifests, and all eight retained trust records.

The active contracts are reproduced without adding a source-selected return.
`TS-053-D002`, `TS-054-D001`, and `TS-055-D001` remain context-only
specification vocabulary. `TS-053-D001`, `TS-054-D002`, `TS-054-E001`,
`TS-055-D002`, and `TS-055-E001` remain inadmissible and are not admitted into
the theorem boundary. Defined source transitions replace those sites with
bounds normalization, pointer offset and provenance preservation,
dereference/reference well-formedness, root-borrow identity, and mutable or
immutable frames.

Every theorem uses one shared valid input `x` and one shared boundary `b`.
The boundary contains only initial bounded receiver memory, allocation and
address extent, provenance and root-borrow identity, alias permissions,
element layout and platform limits, and a pre-existing frame token. It
contains no option discriminant, returned reference, selected or normalized
index, raw-pointer result, final receiver memory, canonical answer, target
truth, or execution trace. Exact-output equivalence compares every modeled
return field; full equivalence additionally compares every modeled state
field.

For target 054, the source model contains no uninterpreted SMT function and
normalizes all 25 applicable sealed Rust 1.96 `SliceIndex<[T]>` forms:
`usize`, `IndexRange`, old and new range families, the bound pair, every
supported `Clamp` wrapper, and `Last`. A separate source-derived oracle checked
4,100 valid and invalid cases across empty and nonempty receivers, ZST and
non-ZST layout, exhausted inclusive ranges, bound-kind combinations, clamp
edges, and out-of-range inputs. Every normalized range, pointer address,
provenance, and returned value matched the canonical transitions.

For targets 053 and 055, the concrete `usize` index-zero witnesses are valid.
Under the same boundary and exact same unchanged final state, execution one
returns the well-formed element-zero reference at address 4096 with value 10,
while execution two returns the distinct well-formed element-one reference at
address 4100 with value 20. Both satisfy the literal active contract because
the mutable-frame relation constrains the index-zero frame but does not bind
the returned-reference identity. The canonical result is retained only as a
diagnostic transition and is not conjoined to `Spec_T`.

Six adversarial mutations were independently rejected: an opaque SMT
function, an output-bearing boundary field, incomplete target-054
implementation coverage, weakened equality, canonical-answer injection, and
an additional strengthened theorem precondition.

## Independent execution

- Forced Python compilation completed successfully.
- All 13 focused SliceIndex tests and all 431 repository tests passed.
- Each of the three trusted-free Verus models type-checked and verified with
  two verified obligations and zero errors.
- Direct Z3 replay covered six theorem files: both target-054 projections were
  UNSAT, while both projections for targets 053 and 055 were SAT.
- All 27 retained source instances replayed as SAT with model observations,
  all 12 semantic negative probes replayed as UNSAT, and both fixed-reference
  witnesses replayed as SAT.
- The bounded SliceIndex runner and integrated authority validator passed.
- The complete acceptance driver passed all 40 commands.

## Preservation and decision

A direct byte-content comparison, independent of retained digest metadata,
found all 4,903 files in the 51 certified evidence trees unchanged after the
fresh campaign and acceptance run. All 320 frozen input files were likewise
unchanged. The evidence directory contains exactly the 51 baseline trees plus
targets 053 through 055. The crosswalk and trust inventory were replay-stable,
and the 62-row selected ledger contains exactly 54 classified rows and 8
`not-run` rows.

Within the declared bounded model, targets 053 and 055 are accepted as
exact-output and full-state `conditional-incomplete`; target 054 is accepted
as exact-output and full-state `conditional-complete`. Stage transition
remains disabled.
