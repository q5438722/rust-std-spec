# Supervisor verdict — target-078-insert-tail-v3-full-acceptance-r5 [FAILED]

## Subagent Report: target-078-insert-tail-v3-full-acceptance-r5 [FAILED]

The run stayed healthy through all monitored checks and passed every acceptance stage until `44_final_reconciliation`, where I diagnosed a missing restored ledger artifact: `crosswalk/conditional_obligation_crosswalk.csv` is referenced by the certified final/operational-v2 manifests but is absent from the workspace.

**Key Metrics**
- Duration: `499s`
- Exit code: `1`
- Supervisor checks: `4`
- Last supervisor decision: `continue`
- Last health: `healthy`
- Acceptance stages passed before failure: compile, target 078 refinement, operational-v2 certification tests, unit tests, all target/cluster pipelines, local validator, target 078/079 operational-v1 checks
- Failed stage: `44_final_reconciliation`
- Reward/loss/KL/clipped ratio/steps/completion length: not applicable; this was an acceptance validation run, not a training run.

**Artifacts To Inspect**
- `.argus_subagents/target-078-insert-tail-v3-full-acceptance-r5_logs/stdout.log`
- `.argus_subagents/target-078-insert-tail-v3-full-acceptance-r5_logs/stderr.log`
- `.argus_subagents/target-078-insert-tail-v3-full-acceptance-r5.json`
- `.argus_subagents/target-078-insert-tail-v3-full-acceptance-r5_logs/supervisor.jsonl`
- `evidence/final_campaign/reconciliation_manifest.json`
- `evidence/final_campaign/operational_v2/reconciliation_manifest.json`
- Missing required artifact: `crosswalk/conditional_obligation_crosswalk.csv`

**Next Step**
Restore the exact certified ledger artifact `crosswalk/conditional_obligation_crosswalk.csv` with the digest expected by `evidence/final_campaign/reconciliation_manifest.json`, then rerun:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_final_reconciliation.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

There are no hyperparameter flags to change in this command. Do not rerun unchanged until the missing crosswalk artifact is restored or the preservation manifest is corrected to match the actual certified ledger contents.

Final health verdict: unusable | the runner trend was healthy, but the acceptance result is blocked by a deterministic missing-artifact preservation-policy failure, so this run cannot be accepted as-is.
