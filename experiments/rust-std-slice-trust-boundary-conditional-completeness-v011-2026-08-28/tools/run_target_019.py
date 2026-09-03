#!/usr/bin/env python3
"""Build and execute target 019 evidence."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import pointer_target_pipeline
import replay_target_019
import target_019


PRESERVED_RESULTS = pointer_target_pipeline.BASELINE_RESULTS
PRESERVED_ARTIFACT_IDS = pointer_target_pipeline.BASELINE_ARTIFACT_IDS


def main() -> None:
    pointer_target_pipeline.run(
        target_019,
        replay_target_019,
        preserved_results=PRESERVED_RESULTS,
        preserved_artifact_ids=PRESERVED_ARTIFACT_IDS,
        expected_not_run=53,
        source_model=common.OUT / "proofs/019_core_slice_as_mut_ptr.rs",
    )


if __name__ == "__main__":
    main()
