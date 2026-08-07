# Rust std specification-generation experiments

- `CLASSIFICATION.md`: classification of all 2,121 stable uncovered APIs.
- `SPECGEN-DETERMINISM-RESULTS-2026-07-22.md`: selected 133-target experiment.
- `ALL-2121-SPECGEN-RESULTS-2026-07-23.md`: complete 2,121-target experiment.
- `ALL-2121-SPECGEN-RESULTS-2026-08-06.md`: fresh source-backed rerun with
  127 accepted semantic candidates and a complete 1,994-row skip audit.
- `abstraction-final/`: final reclassification and the 20-target
  newly-unlocked generation batch.
- `abstraction-audits/`: module-level determinism audits for the experimental
  vstd additions, including the 2026-07-29 continuation.
- `all-2121-gpt56sol/`: final combined per-target results.
- `all-2121-gpt56sol-fresh-20260806-0453/`: canonical aggregate artifacts for
  the fresh 2026-08-06 rerun. Raw per-target `targets/` remain intentionally
  untracked.
- `remaining-generation/`: batched generation and checker artifacts for the
  remaining 2,018 APIs.
