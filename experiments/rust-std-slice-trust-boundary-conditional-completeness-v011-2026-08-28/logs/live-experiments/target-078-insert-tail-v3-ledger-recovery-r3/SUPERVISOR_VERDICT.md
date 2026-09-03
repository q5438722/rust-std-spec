# Supervisor verdict — target-078-insert-tail-v3-ledger-recovery-r3 [FAILED]

## Subagent Report: target-078-insert-tail-v3-ledger-recovery-r3 [FAILED]

I let the run continue because both live checks were healthy, but acceptance failed in `44_final_reconciliation` because preservation-policy validation references a missing certified-campaign artifact: `crosswalk/conditional_obligation_crosswalk.csv`.

**Key metrics:** duration `132s`, exit code `1`, supervisor checks `2`, last health `healthy`, target-079 operational step exit `0`, local validator exit `0`, final reconciliation exit `1`. No reward/loss/steps/clipped_ratio/KL/length metrics were emitted by this acceptance wrapper.

**Inspect:**
- `.argus_subagents/target-078-insert-tail-v3-ledger-recovery-r3_logs/stdout.log`
- `.argus_subagents/target-078-insert-tail-v3-ledger-recovery-r3_logs/stderr.log`
- `.argus_subagents/target-078-insert-tail-v3-ledger-recovery-r3.json`
- `.argus_subagents/target-078-insert-tail-v3-ledger-recovery-r3_logs/supervisor.jsonl`
- `preservation/path_policy_v1.json`
- `tools/preservation_policy_v1.py`
- `tools/final_reconciliation.py`

**Next step:** do not rerun unchanged. Restore or regenerate the missing certified artifact `crosswalk/conditional_obligation_crosswalk.csv` with the exact historical bytes expected by the preservation policy, or update the restoration/ledger-recovery code so `preservation/path_policy_v1.json` only binds paths actually restored in this workspace. After that, rerun the same command: `PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py --start-at 44b_target_079_operational_v1`.

Final health verdict: inconclusive | target-079 and local validation passed cleanly, but final reconciliation could not evaluate campaign health because the preserved artifact inventory is incomplete.
