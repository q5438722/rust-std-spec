#!/usr/bin/env python3
"""Build and execute target 028 evidence."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import replay_target_028
import search_target_pipeline
import target_028


PRESERVED_RESULTS = search_target_pipeline.BASELINE_RESULTS
PRESERVED_ARTIFACT_IDS = search_target_pipeline.BASELINE_ARTIFACT_IDS


def main() -> None:
    search_target_pipeline.run(
        target_028,
        replay_target_028,
        preserved_results=PRESERVED_RESULTS,
        preserved_artifact_ids=PRESERVED_ARTIFACT_IDS,
        expected_not_run=50,
        source_model=common.OUT / "proofs/028_core_slice_binary_search.rs",
    )


if __name__ == "__main__":
    main()
