#!/usr/bin/env python3
"""Build and execute target 065 evidence."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import replay_target_065
import run_target_030
import search_target_pipeline
import target_030
import target_065


PRESERVED_RESULTS = {
    **run_target_030.PRESERVED_RESULTS,
    (target_030.TARGET, target_030.INPUT_ORDER): search_target_pipeline.INCOMPLETE,
}
PRESERVED_ARTIFACT_IDS = (
    *run_target_030.PRESERVED_ARTIFACT_IDS,
    target_030.ARTIFACT_ID,
)


def main() -> None:
    search_target_pipeline.run(
        target_065,
        replay_target_065,
        preserved_results=PRESERVED_RESULTS,
        preserved_artifact_ids=PRESERVED_ARTIFACT_IDS,
        expected_not_run=48,
        source_model=common.OUT / "proofs/065_core_slice_partition_point.rs",
    )


if __name__ == "__main__":
    main()
