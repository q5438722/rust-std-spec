# Supervisor verdict — target-081-v2-command1-acceptance-r1 [FAILED]

## Subagent Report: target-081-v2-command1-acceptance-r1 [FAILED]

I let the run continue because it stayed healthy, but command-1 acceptance failed at `44_final_reconciliation` when the preservation policy rejected new authority-ledger members: `crosswalk/target_081_operational_v1_addendum.csv` and `.json`.

**Key Metrics**
- Duration: 508.3s
- Exit code: 1
- Supervisor checks: 3
- Health trend: healthy at 60.0s, 194.3s, and 446.7s
- Acceptance commands before failure: all completed with `exit_code=0`
- Unit test gate: `Ran 725 tests in 581.504s`, `OK`
- Failure point: `44_final_reconciliation`
- ML metrics: not applicable here; this was an acceptance/reconciliation run, not a training run, so no reward/loss/KL/clipped_ratio signal exists.

**Artifacts To Inspect**
- `.argus_subagents/target-081-v2-command1-acceptance-r1_logs/stdout.log`
- `.argus_subagents/target-081-v2-command1-acceptance-r1_logs/stderr.log`
- `.argus_subagents/target-081-v2-command1-acceptance-r1.json`
- `.argus_subagents/target-081-v2-command1-acceptance-r1_logs/supervisor.jsonl`
- `logs/44_final_reconciliation.stderr.txt`
- `logs/44_final_reconciliation.status.txt`
- `logs/44_final_reconciliation.command.txt`

**Next Step**
Do not rerun unchanged. Update the preservation policy/baseline to intentionally admit the two new archive-backed target-081 v2 authority ledgers: add `crosswalk/target_081_operational_v1_addendum.csv` and `crosswalk/target_081_operational_v1_addendum.json` to the expected `authority_ledgers` membership in `tools/preservation_policy_v3.py` or its versioned baseline source, then rerun `PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py`.

Final health verdict: usable | The run produced usable signal: tests met the 725 minimum and all substantive acceptance stages passed; the only failure is a reconciliation allowlist/baseline mismatch for newly added target-081 ledger artifacts.
