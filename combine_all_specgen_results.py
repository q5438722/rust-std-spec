#!/usr/bin/env python3
"""Combine the suitable run and remaining run into one 2,121-target result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import analyze_specgen_results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument(
        "--suitable",
        type=Path,
        nargs="+",
        default=[
            workspace
            / "specgen"
            / "suitable-pilot-gpt56sol-v2"
            / "batch_summary.json",
            workspace
            / "specgen"
            / "suitable-remaining-gpt56sol-v1"
            / "batch_summary.json",
        ],
    )
    parser.add_argument(
        "--remaining-dir",
        type=Path,
        default=workspace
        / "specgen"
        / "remaining-generation"
        / "evaluated-gpt56sol",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=workspace / "specgen" / "all-2121-gpt56sol",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payloads = [json.loads(path.read_text()) for path in args.suitable]
    remaining_paths = sorted(
        args.remaining_dir.glob("*/batch_summary.json")
    )
    payloads.extend(json.loads(path.read_text()) for path in remaining_paths)
    by_target = {}
    for payload in payloads:
        for result in payload["results"]:
            by_target[result["target"]] = result
    if len(by_target) != 2121:
        raise ValueError(f"expected 2121 unique targets, got {len(by_target)}")
    combined = {
        "metadata": {
            "model": "gpt-5.6-sol",
            "target_count": len(by_target),
            "source_batches": [
                str(path.resolve())
                for path in [*args.suitable, *remaining_paths]
            ],
            "selection": (
                "remaining-run results override the 30 suitable-run skips; "
                "the original 103 suitable add-spec results are retained"
            ),
        },
        "results": list(by_target.values()),
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary = args.out_dir / "batch_summary.json"
    summary.write_text(json.dumps(combined, indent=2) + "\n")
    analysis, rows = analyze_specgen_results.analyze(combined)
    (args.out_dir / "analysis.json").write_text(
        json.dumps(analysis, indent=2, sort_keys=True) + "\n"
    )
    analyze_specgen_results.write_csv(args.out_dir / "final_candidates.csv", rows)
    analyze_specgen_results.write_report(
        args.out_dir / "ANALYSIS.md",
        analysis,
        rows,
    )
    print(
        f"combined {len(by_target)} targets; "
        f"final add={analysis['counts']['final_add_spec']} "
        f"skip={analysis['counts']['final_skip']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
