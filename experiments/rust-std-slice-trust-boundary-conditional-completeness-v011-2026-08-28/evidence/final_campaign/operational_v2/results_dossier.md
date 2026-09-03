# Slice operational-v2 reconciliation results

**Status:** `ready-for-independent-review`

This additive reconciliation derives the certified 62-row campaign and overlays only the independently accepted operational-v1 results for input orders 078 and 079. The certified campaign rows remain embedded without modification.

| Projection | Conditional complete | Conditional incomplete | Missing |
|---|---:|---:|---:|
| Exact output | 50 | 12 | 0 |
| Reviewed equivalence | 43 | 19 | 0 |

| Order | Target | Effective exact | Effective reviewed equivalence | Evidence | Review |
|---:|---|---|---|---|---|
| 078 | `core::slice::select_nth_unstable_by` | `conditional-complete` | `conditional-complete` | `evidence/target_078_operational_v1/result.json` | `review/REVIEW_ADDENDUM_TARGET_078_OPERATIONAL_V1.md` |
| 079 | `core::slice::select_nth_unstable_by_key` | `conditional-complete` | `conditional-complete` | `evidence/target_079_operational_v1/result.json` | `review/REVIEW_ADDENDUM_TARGET_079_OPERATIONAL_V1.md` |

Both overlays retain one direct arbitrary-domain exact-output UNSAT obligation, one direct arbitrary-domain reviewed-equivalence UNSAT obligation, one SAT nonvacuity replay, and clean Verus typecheck and verification captures.

| Preserved group | Files | Inventory SHA-256 |
|---|---:|---|
| `accepted_operational_v1_packages` | 650 | `e27b9e79fc4df47a61665b6f82ee2d4b4a93389085c6ed0531940f25d0574691` |
| `certified_campaign` | 9 | `a52ab003b291ca3dcf6f9d4c291e6c4249e88559ab02cc27f789d07c02d27392` |
| `manager_owned_state` | 1 | `120b226aee5c883997986e92beb08ffce4ce41423be6cb2e648eac8a443555ce` |
| `prior_reviews` | 45 | `cbb996cc65588ce013b5cb91aee00854921cbf260460e3586baab15b712fc214` |

A new independent campaign-level review is still required. This reconciliation does not alter `research/PIPELINE_STATE.json` or authorize a stage transition.
