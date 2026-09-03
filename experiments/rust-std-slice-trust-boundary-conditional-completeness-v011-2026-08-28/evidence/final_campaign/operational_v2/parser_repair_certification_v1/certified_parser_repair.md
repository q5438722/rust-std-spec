# Operational-v2 parser-repair certification v1

**Status:** `certified`

The additive validator accepts exactly one canonical count-bearing summary and rejects missing, duplicate, conflicting, wrong-scope, wrong-count, stale, and non-ACCEPT review evidence.

| Projection | Conditional complete | Conditional incomplete | Missing |
|---|---:|---:|---:|
| Exact output | 50 | 12 | 0 |
| Reviewed equivalence | 43 | 19 | 0 |

Certified rows: **62**.

Rejected review evidence: `missing`, `duplicate`, `conflicting`, `wrong-scope`, `wrong-count`, `stale`, `non-ACCEPT`.

Classification drift and protected-file drift are rejected. The unchanged certified projection and all 707 protected paths match their frozen identities.

**Independent Reviewer:** `ACCEPT` from `.review-scratch/operational-v2-certification-reviewer-round3` completed at `2026-09-02T00:30:23.021369Z`.

Manager-owned stage transition remains disabled.
