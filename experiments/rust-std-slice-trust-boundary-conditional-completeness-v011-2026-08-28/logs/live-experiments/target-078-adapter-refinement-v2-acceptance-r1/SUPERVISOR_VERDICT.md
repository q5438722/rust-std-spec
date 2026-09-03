# Supervisor verdict — target-078-adapter-refinement-v2-acceptance-r1 [FAILED]

## Subagent Report: target-078-adapter-refinement-v2-acceptance-r1 [FAILED]

The acceptance campaign failed immediately because `01b_operational_v2_certification_tests` hit `OperationalV2Error: operational-v2 preservation lock mismatch`, meaning the recorded operational-v2 preservation lock no longer matches the current preserved artifacts on disk.

**Key Metrics**
- Exit code: `1`
- Duration: `1s`
- Acceptance status: `FAIL`
- Last completed command: `01_compileall`, exit `0`
- Failing command: `01b_operational_v2_certification_tests`, exit `1`
- Tests run: `0`
- Failure phase: `setUpClass`, before certification tests executed
- RL/GPU metrics: not applicable; this was a deterministic acceptance script, not a training run.

**Artifacts To Inspect**
- `.argus_subagents/target-078-adapter-refinement-v2-acceptance-r1.json`
- `.argus_subagents/target-078-adapter-refinement-v2-acceptance-r1_logs/stdout.log`
- `.argus_subagents/target-078-adapter-refinement-v2-acceptance-r1_logs/stderr.log`
- `logs/acceptance_manifest.json`
- `logs/01b_operational_v2_certification_tests.stderr.txt`
- `logs/01b_operational_v2_certification_tests.status.txt`
- `crosswalk/conditional_obligation_crosswalk_operational_v2.json`
- `evidence/final_campaign/preservation_baseline.json`

**Concrete Next Step**
Do not rerun unchanged. Regenerate or repair the operational-v2 preservation lock so `crosswalk/conditional_obligation_crosswalk_operational_v2.json` records the current preserved artifact set, including the additive target-078/079 operational-v1 and adapter-refinement-v2 artifacts now present under `evidence/target_078_operational_v1`, `evidence/target_079_operational_v1`, related `crosswalk/target_078_*`, `crosswalk/target_079_*`, and `review/REVIEW_ADDENDUM_*` files. The specific code path is `tools/operational_v2_reconciliation.py`: update the preservation snapshot by rerunning the operational-v2 reconciliation writer, e.g. `PYTHONDONTWRITEBYTECODE=1 python3 tools/run_operational_v2_reconciliation.py`, then rerun `PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py`.

Final health verdict: unusable | the run produced no acceptance signal beyond compileall; the first certification setup failed on stale preservation metadata.
