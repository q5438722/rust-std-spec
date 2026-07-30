#!/usr/bin/env python3
"""Prepare the 2,018 Rust APIs not generated in the first suitable run."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument(
        "--classified",
        type=Path,
        default=workspace / "specgen" / "classified-manifest.json",
    )
    parser.add_argument(
        "--first-run-results",
        type=Path,
        default=workspace
        / "specgen"
        / "suitable-combined-gpt56sol"
        / "final_candidates.csv",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=workspace / "specgen" / "remaining-generation",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    classified = json.loads(args.classified.read_text())["targets"]
    first_run = {
        row["target"]: row
        for row in csv.DictReader(args.first_run_results.open())
    }
    remaining = []
    for target in classified:
        classification = target["classification"]
        if classification != "suitable_now":
            enriched = dict(target)
            enriched["generation_group"] = classification
            remaining.append(enriched)
            continue
        result = first_run[target["target"]]
        if result["final_decision"] == "skip":
            enriched = dict(target)
            enriched["generation_group"] = "retry_suitable_skip"
            enriched["previous_skip_rationale"] = result["rationale"]
            remaining.append(enriched)

    remaining.sort(key=lambda item: (item["generation_group"], item["target"]))
    groups = Counter(target["generation_group"] for target in remaining)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "target_count": len(remaining),
            "group_counts": dict(sorted(groups.items())),
            "source_classified_count": len(classified),
            "already_generated_count": len(classified) - len(remaining),
        },
        "targets": remaining,
    }
    (args.out_dir / "all-remaining-manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    groups_dir = args.out_dir / "groups"
    groups_dir.mkdir(exist_ok=True)
    for group in sorted(groups):
        targets = [
            target for target in remaining if target["generation_group"] == group
        ]
        (groups_dir / f"{group}.json").write_text(
            json.dumps(
                {
                    "metadata": {
                        "group": group,
                        "target_count": len(targets),
                    },
                    "targets": targets,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
    lines = [
        "# Remaining Rust std generation batches",
        "",
        "| Group | Count |",
        "|---|---:|",
    ]
    for group, count in sorted(groups.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{group}` | {count} |")
    lines.extend(
        [
            "",
            f"Total remaining targets: **{len(remaining)}**.",
            "",
        ]
    )
    (args.out_dir / "README.md").write_text("\n".join(lines))
    print(
        f"prepared {len(remaining)} remaining targets across {len(groups)} groups"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
