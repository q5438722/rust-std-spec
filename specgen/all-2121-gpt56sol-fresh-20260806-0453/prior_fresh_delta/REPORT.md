# Prior vs Fresh Rust Std Specgen Delta

Generated at UTC `2026-08-07T06:20:48Z`.

This audit compares the prior full run against the canonical fresh run by target name and final decision. It records explicit target lists and row deltas; it does not use checksum evidence.

## Target Set and Fresh Verifier

| Measure | Value |
| --- | ---: |
| prior final-candidate rows | 2121 |
| fresh final-candidate rows | 2121 |
| common targets | 2121 |
| missing in fresh | 0 |
| extra in fresh | 0 |
| fresh verifier missing targets | 0 |
| fresh verifier extra targets | 0 |
| fresh verifier duplicate result targets | 0 |
| fresh verifier accepted semantic candidates | 127 |
| fresh verifier final add_spec rows | 127 |
| fresh verifier final skip rows | 1994 |
| fresh verifier empty skip rationales | 0 |

## Decision Delta

| Measure | Value |
| --- | ---: |
| changed final decisions | 147 |
| prior add_spec -> fresh skip | 117 |
| prior skip -> fresh add_spec | 30 |
| changed fresh skip rows missing rationale | 0 |

The changed-row CSVs include prior and fresh category, gate, issue, requires, ensures, rationale, source-fidelity, and contract-text fields so the decision changes are inspectable without relying on opaque summaries.

## Artifacts

- `REPORT.md`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/prior_fresh_delta/REPORT.md`
- `decision_changes.csv`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/prior_fresh_delta/decision_changes.csv`
- `newly_accepted_prior_skip_fresh_add.csv`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/prior_fresh_delta/newly_accepted_prior_skip_fresh_add.csv`
- `prior_add_spec_now_fresh_skip.csv`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/prior_fresh_delta/prior_add_spec_now_fresh_skip.csv`
- `summary.json`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/prior_fresh_delta/summary.json`
- `target_set_audit.json`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/prior_fresh_delta/target_set_audit.json`
