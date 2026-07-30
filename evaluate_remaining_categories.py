#!/usr/bin/env python3
"""Evaluate batch-generated remaining contracts one classification at a time."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


DEFAULT_ORDER = [
    "retry_suitable_skip",
    "complex_result_or_pattern_model",
    "associated_type_or_projection",
    "higher_order_contract",
    "iterator_or_adapter_result",
    "needs_new_vstd_abstraction",
    "trait_contract_integration",
    "ownership_or_uninitialized_model",
    "representation_or_allocator",
    "unsafe_or_representation_sensitive",
    "no_modeled_observable_output",
    "determinism_checker_unsupported",
    "toolchain_unavailable",
    "formatting_effect",
    "concurrency_or_hidden_state",
    "runtime_or_hidden_state",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument(
        "--groups-dir",
        type=Path,
        default=workspace / "specgen" / "remaining-generation" / "groups",
    )
    parser.add_argument(
        "--seed-candidates",
        type=Path,
        default=workspace
        / "specgen"
        / "remaining-generation"
        / "firstpass-gpt56sol"
        / "seed-candidates.json",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=workspace
        / "specgen"
        / "remaining-generation"
        / "evaluated-gpt56sol",
    )
    parser.add_argument("--groups", nargs="*")
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--feedback-rounds", type=int, default=1)
    parser.add_argument("--llm-timeout", type=int, default=360)
    parser.add_argument("--llm-retries", type=int, default=1)
    parser.add_argument("--check-timeout", type=int, default=180)
    parser.add_argument("--rlimit", type=float, default=30)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--clean-verus-logs", action="store_true")
    return parser.parse_args()


def remove_verus_logs(root: Path) -> None:
    for path in root.rglob("verus_log"):
        if path.is_dir():
            shutil.rmtree(path)


def main() -> int:
    args = parse_args()
    workspace = Path(__file__).resolve().parent
    groups = args.groups or DEFAULT_ORDER
    args.out_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    for index, group in enumerate(groups, start=1):
        manifest = args.groups_dir / f"{group}.json"
        if not manifest.is_file():
            raise FileNotFoundError(manifest)
        group_out = args.out_dir / group
        command = [
            str(workspace / ".venv" / "bin" / "python"),
            str(workspace / "run_rust_std_spec_feedback.py"),
            "--manifest",
            str(manifest),
            "--seed-candidates",
            str(args.seed_candidates),
            "--out",
            str(group_out),
            "--jobs",
            str(args.jobs),
            "--feedback-rounds",
            str(args.feedback_rounds),
            "--model",
            "gpt-5.6-sol",
            "--llm-timeout",
            str(args.llm_timeout),
            "--llm-retries",
            str(args.llm_retries),
            "--check-timeout",
            str(args.check_timeout),
            "--rlimit",
            str(args.rlimit),
            "--include-non-suitable",
            "--include-unavailable",
        ]
        if args.resume:
            command.append("--resume")
        print(f"[{index}/{len(groups)}] evaluating {group}", flush=True)
        process = subprocess.run(command, cwd=workspace)
        if process.returncode != 0:
            return process.returncode
        summary = group_out / "batch_summary.json"
        summaries.append(summary)
        if args.clean_verus_logs:
            remove_verus_logs(group_out)

    combined = args.out_dir / "combined"
    command = [
        str(workspace / ".venv" / "bin" / "python"),
        str(workspace / "analyze_specgen_results.py"),
        *[str(path) for path in summaries],
        "--out-dir",
        str(combined),
    ]
    process = subprocess.run(command, cwd=workspace)
    if process.returncode != 0:
        return process.returncode
    metadata = {
        "groups": groups,
        "group_count": len(groups),
        "batch_summaries": [str(path.resolve()) for path in summaries],
    }
    (args.out_dir / "evaluation_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
