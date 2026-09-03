# Independent Reviewer request: complete 62-target Slice campaign

**Status:** pending independent review

Review the additive
`crosswalk/conditional_obligation_crosswalk.{csv,json}`,
`evidence/final_campaign/results_dossier.{json,md}`, the target-029 boundary
manifest, and their live source evidence. Record the campaign-wide decision in
`review/FINAL_CAMPAIGN_REVIEW_ACCEPTANCE.md`; use `**VERDICT: ACCEPT**` only if
all 62 rows pass.

- Re-derive the 62 selected rows from the active 120-row generated Slice
  manifest/catalog intersection with `r0_z3=unknown`; reject Vec, exact-vstd,
  prior UNSAT, Array, Option, and String leakage.
- Confirm every row uniquely binds the active contract, generated declaration,
  Rust item/docs, frozen implementation-proof inputs, every retained trust
  site, the distinct new-obligation boundary, source citations, proof scope,
  equivalence, direct solver evidence, Verus evidence, replayable witness when
  applicable, and one accepting incremental review.
- Audit all six weakened equivalences (028-030 and 080-082), including their
  positive and negative witnesses. Audit missing-model rows 078-079 and reject
  any promotion of their bounded UNSAT diagnostics.
- Require direct clean UNSAT for each completeness cell and a fixed-input,
  fixed-boundary replayable SAT witness for each incompleteness cell. Recompute
  exact-output counts 48/12/2 and full-state counts 41/19/2 without coercion.
- Confirm the target-029 manifest distinguishes its retained implementation
  proof boundary from the four trust sites that back actual `Boundary_T`
  observations. It must exclude the selected index, returned Result, aggregate
  final state, branch choice, answer encodings, and traces.
- Confirm all 320 frozen inputs, every pre-existing evidence file, frozen
  authority ledger, and accepted incremental review match
  `evidence/final_campaign/preservation_baseline.json`.
- Run forced Python compilation, the complete nonzero unit suite,
  `tools/run_final_reconciliation.py`, and the complete
  `tools/run_acceptance.py` replay before deciding.
