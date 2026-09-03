# Independent Reviewer findings: raw slice addressed-memory repair

**VERDICT: CHANGES REQUIRED**

**Timestamp:** 2026-09-01T09:56:57Z

This review covers only input orders 048 `core::slice::from_raw_parts` and
049 `core::slice::from_raw_parts_mut` against the independently accepted
49-target baseline. It does not authorize a Manager stage transition.

## Verified observations

The SMT input no longer contains a logical result array. Both target
transitions construct a finite returned sequence pointwise from shared
address-indexed boundary memory using the pointer address, element size,
length, initialization, allocation bounds, provenance, ZST equal-address
semantics, and an empty one-past base case that performs no memory read. The
trusted-free Verus models mirror that relation with boundary maps and contain
no `external_body`.

`TS-048-D001` and `TS-049-D001` remain context-only. The four answer-bearing
records `TS-048-D002`/`TS-048-E001` and
`TS-049-D002`/`TS-049-E001` remain explicitly inadmissible and are absent from
`Boundary_T`.

Fresh Reviewer execution produced the following results:

- Forced Python compilation completed cleanly, all 17 focused tests passed,
  and all 418 repository tests passed.
- Thirty-six independent source-derived SAT/UNSAT probes confirmed the live
  base domains, exact return-field mapping, the element at address 4096,
  every returned address in the representative interior range, invalid
  initialization/allocation/provenance/one-past cases, ZST no-stride
  semantics, and empty one-past non-dereference.
- The bounded runner passed at 51 classified and 11 `not-run`. Three theorem
  projections replayed as UNSAT, the mutable full-state projection replayed
  as SAT, 14 source instances replayed as SAT with models, and 54 negative
  probes replayed as UNSAT.
- The fixed mutable witness uses one shared input and boundary, returns
  `[10, 20, 30]` in both executions, and varies only the unconstrained final
  in-range memory.
- Both Verus models type-checked and each verified two obligations with zero
  errors. The complete acceptance driver passed all 39 commands, including
  local validation.
- Direct content comparison around both the bounded runner and complete
  acceptance preserved all 4,475 files in the 49 accepted evidence trees and
  all 320 frozen-input files. The exact 51-directory set was accepted and a
  foreign directory was rejected.

## Blocking finding

### F1: Generated review and checker-design artifacts retain the obsolete 44-probe count

`tools/raw_slice_pair.py` now defines 27 negative probes per target, and both
generated result trees contain and replay all 54 probes. The Wiki correctly
reports 54. However:

- `tools/build_authority_design.py:1618-1620` still generates
  `research/CONDITIONAL_THEOREM_CHECKER_DESIGN.md` with “forty-four UNSAT
  negative probes”.
- `tools/build_authority_design.py:2488-2490` still generates
  `review/REVIEW_REQUEST.md` with “44 negative probes”.
- `tools/validate_authority_design.py:5036` and
  `tools/validate_authority_design.py:5063` require those obsolete phrases,
  so `tools/run_acceptance.py` passes while enforcing a false audit fact.

The generated independent-review checklist therefore omits the ten new
pointwise, one-past, and ZST regressions introduced by this repair. Update both
generator strings and both validator expectations to 54, regenerate the
checker design and review request, and rerun the focused and complete
acceptance commands before requesting another independent review.

Rows 048 and 049 remain candidate classifications.
