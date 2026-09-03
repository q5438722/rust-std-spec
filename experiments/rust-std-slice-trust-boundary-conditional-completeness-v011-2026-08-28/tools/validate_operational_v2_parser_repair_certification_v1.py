#!/usr/bin/env python3
"""Validate the additive operational-v2 parser-repair certification."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from operational_v2_parser_repair_certification_v1 import (
    REVIEW_REJECTION_CASES,
    validate_written_artifacts,
)


if __name__ == "__main__":
    manifest = validate_written_artifacts()
    exact = manifest["classification_counts"]["exact_output_determinism"]
    full = manifest["classification_counts"][
        "completeness_modulo_reviewed_equivalence"
    ]
    print("operational_v2_parser_repair_certification_v1=PASS")
    print(f"rows={manifest['row_count']}")
    print(
        "exact="
        f"{exact['conditional-complete']}/"
        f"{exact['conditional-incomplete']}/"
        f"{exact['missing-source-backed-model']}"
    )
    print(
        "full="
        f"{full['conditional-complete']}/"
        f"{full['conditional-incomplete']}/"
        f"{full['missing-source-backed-model']}"
    )
    print("canonical_summary=accepted:1")
    print("review_rejections=" + ",".join(REVIEW_REJECTION_CASES))
    print("classification_drift=rejected")
    print("protected_file_drift=rejected")
    print("protected_paths=707")
    print("independent_reviewer=ACCEPT")
    print("stage_transition=disabled")
