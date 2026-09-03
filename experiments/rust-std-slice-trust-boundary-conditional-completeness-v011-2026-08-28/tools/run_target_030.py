#!/usr/bin/env python3
"""Build and execute target 030 evidence."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import replay_target_030
import run_target_028
import search_target_pipeline
import target_028
import target_030


PRESERVED_RESULTS = {
    **search_target_pipeline.BASELINE_RESULTS,
    (target_028.TARGET, target_028.INPUT_ORDER): search_target_pipeline.INCOMPLETE,
}
PRESERVED_ARTIFACT_IDS = (
    *search_target_pipeline.BASELINE_ARTIFACT_IDS,
    target_028.ARTIFACT_ID,
)


def main() -> None:
    search_target_pipeline.run(
        target_030,
        replay_target_030,
        preserved_results=PRESERVED_RESULTS,
        preserved_artifact_ids=PRESERVED_ARTIFACT_IDS,
        expected_not_run=49,
        source_model=common.OUT / "proofs/030_core_slice_binary_search_by_key.rs",
    )


if __name__ == "__main__":
    main()
