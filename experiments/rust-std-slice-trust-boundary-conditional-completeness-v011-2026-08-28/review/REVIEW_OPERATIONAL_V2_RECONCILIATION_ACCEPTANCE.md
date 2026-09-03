# Independent Reviewer decision: operational-v2 reconciliation

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T22:41:27Z

This decision covers only the additive operational-v2 reconciliation of the
certified 62-row Slice campaign. It does not alter either accepted
operational-v1 package, reopen their source-model classifications, or
authorize a Manager-owned stage transition.

## Findings

| Check | Decision |
|---|---|
| Additive scope | Accepted. All 62 certified campaign rows are embedded exactly. Only input orders 078 and 079 change effective classification, and they map to `core::slice::select_nth_unstable_by` and `core::slice::select_nth_unstable_by_key`. Every other effective classification remains identical to the certified baseline. |
| Overlay authority | Accepted. The two overlays are the complete discovered operational-v1 addendum set. Their JSON and CSV identities agree with the certified target, order, and active contract; both source packages have independent `ACCEPT` reviews. Duplicate, missing, unsupported, target/order/contract-mismatched, or non-accepted overlays fail closed. |
| Direct evidence | Accepted. Independent Z3 replay returned UNSAT for each target's exact-output and reviewed-equivalence obligation and SAT for each nonvacuity obligation. The trusted-free Verus models type-checked and verified with `5 verified, 0 errors` for target 078 and `7 verified, 0 errors` for target 079. |
| Effective counts | Accepted. Independent recomputation gives exact-output counts `50/12/0` and reviewed-equivalence counts `43/19/0` for conditional-complete, conditional-incomplete, and missing-source-backed-model respectively. The JSON and CSV crosswalks contain the same 62 ordered target identities, and the reconciliation manifest and both dossier projections report the same counts. |
| Fail-closed behavior | Accepted. The 13 focused tests exercised scope drift, duplicate and unsupported overlays, target/order/contract mismatches, non-ACCEPT reviews, missing clean UNSAT evidence, absent SAT nonvacuity, stale counts, and preserved-artifact mutation. All negative cases were rejected. |
| Preservation | Accepted. The certified preservation fixture matched before execution. A Reviewer-owned direct byte snapshot then compared 701 unique protected paths before and after all target, solver, Verus, unit, reconciliation, and acceptance runs. Membership had no missing or extra path and no file changed. This covers 650 accepted operational-package records, nine certified-campaign records, 45 prior-review records, and the Manager-owned state record, with four paths shared between groups. |

## Fresh Reviewer execution

The Reviewer forced Python compilation, ran all 13 focused operational-v2
tests, ran the dedicated reconciliation and both operational-v1 target
runners, directly replayed the six retained SMT obligations, and directly
ran both typecheck and verification commands for each Verus model. The
complete unit suite ran 553 tests and reported `OK`.

The complete task-native driver then reported:

```text
acceptance=PASS
commands=47
```

Its embedded complete suite again ran 553 tests and reported `OK`; both target
runners and the operational-v2 reconciliation passed. The reconciliation
reports 62 rows, overlays `78,79`, exact counts `50/12/0`, reviewed-equivalence
counts `43/19/0`, and zero missing classifications.

The bounded operational-v2 objective and its independent Reviewer gate are
satisfied. Manager-owned stage transition remains disabled.
