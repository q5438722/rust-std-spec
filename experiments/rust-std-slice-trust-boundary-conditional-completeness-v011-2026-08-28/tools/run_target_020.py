#!/usr/bin/env python3
"""Build and execute target 020 evidence after targets 019 and 021."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import pointer_target_pipeline
import replay_target_020
import target_019
import target_020
import target_021


PRESERVED_RESULTS = {
    **pointer_target_pipeline.BASELINE_RESULTS,
    (target_019.TARGET, target_019.INPUT_ORDER): pointer_target_pipeline.COMPLETE,
    (target_021.TARGET, target_021.INPUT_ORDER): pointer_target_pipeline.COMPLETE,
}
PRESERVED_ARTIFACT_IDS = (
    *pointer_target_pipeline.BASELINE_ARTIFACT_IDS,
    target_019.ARTIFACT_ID,
    target_021.ARTIFACT_ID,
)


def main() -> None:
    pointer_target_pipeline.run(
        target_020,
        replay_target_020,
        preserved_results=PRESERVED_RESULTS,
        preserved_artifact_ids=PRESERVED_ARTIFACT_IDS,
        expected_not_run=51,
        source_model=common.OUT / "proofs/020_core_slice_as_mut_ptr_range.rs",
    )


if __name__ == "__main__":
    main()
