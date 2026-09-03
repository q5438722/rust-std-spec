# Supervisor verdict — target-078-insert-tail-v3-ledger-recovery-r2 [FAILED]

## Subagent Report: target-078-insert-tail-v3-ledger-recovery-r2 [FAILED]

I resumed acceptance at `15_implproof_aggregate`; it passed `15_implproof_aggregate` and `44a_target_078_operational_v1`, then failed immediately in `44b_target_079_operational_v1` because the versioned preservation policy still references missing legacy artifact `crosswalk/conditional_obligation_crosswalk.csv` while computing the protected `campaign_reviews` digest.

**Key Metrics**

- Duration: 13s
- Exit code: 1
- Acceptance progress: 2/3 executed commands passed before failure
- Passing stages: `15_implproof_aggregate`, `44a_target_078_operational_v1`
- Failing stage: `44b_target_079_operational_v1`
- stderr root cause: `PreservationPolicyError: operational-v2 certified_campaign[0].path: path is missing or escapes the policy root`
- Reward/loss/steps/clipped_ratio/response length/KL: not applicable; this was an acceptance replay, not a training run.

**Artifacts To Inspect**

- `.argus_subagents/target-078-insert-tail-v3-ledger-recovery-r2_logs/stdout.log`
- `.argus_subagents/target-078-insert-tail-v3-ledger-recovery-r2_logs/stderr.log`
- `.argus_subagents/target-078-insert-tail-v3-ledger-recovery-r2.json`
- `logs/44b_target_079_operational_v1.stderr.txt`
- `logs/44b_target_079_operational_v1.status.txt`
- `tools/preservation_policy_v1.py`
- `tools/preservation_policy_v2.py`
- `crosswalk/`

**Next Step**

Do not rerun unchanged. Repair the preservation-policy inventory before relaunching acceptance: either restore/regenerate `crosswalk/conditional_obligation_crosswalk.csv`, or update the operational-v2 preservation payload/code path so `certified_campaign[0].path` points at the current existing crosswalk artifact set. The concrete fix path is `tools/preservation_policy_v2.py` / `tools/preservation_policy_v1.py`; after the inventory is repaired, rerun:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py --start-at 44b_target_079_operational_v1
```

Final health verdict: unusable | acceptance is blocked by a deterministic missing-artifact preservation-policy failure, not by a transient metric threshold or GPU health trend.
