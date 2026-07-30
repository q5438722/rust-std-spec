#!/usr/bin/env python3
"""Summarize saved round-0 spec-generation results without rerunning them."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPECGEN = ROOT / "specgen"
OUT = ROOT / "source-verification" / "pre-feedback"


def batch_files() -> list[Path]:
    selected = [
        SPECGEN / "suitable-pilot-gpt56sol-v2" / "batch_summary.json",
        SPECGEN / "suitable-remaining-gpt56sol-v1" / "batch_summary.json",
    ]
    evaluated = sorted(
        (SPECGEN / "remaining-generation" / "evaluated-gpt56sol").glob(
            "*/batch_summary.json"
        )
    )
    return selected + evaluated


def category(result: dict) -> str:
    history = result.get("history") or []
    record = next(
        (item for item in history if item.get("round") == 0),
        history[0] if history else {},
    )
    candidate = record.get("candidate") or {}
    if candidate.get("decision") != "add_spec":
        return "skip_no_spec"
    checker = record.get("checker") or {}
    typecheck = checker.get("typecheck") or {}
    determinism = checker.get("determinism") or {}
    if typecheck and typecheck.get("returncode") != 0:
        return "typecheck_or_checker_failure"
    if determinism.get("status") == "ok":
        if determinism.get("equal_fn_trivial"):
            return "trivial_equality"
        if determinism.get("r0_z3") == "unsat":
            return "complete"
        if determinism.get("r0_z3") == "unknown":
            return "unknown"
        if determinism.get("r0_z3") == "sat":
            return "incomplete_sat"
    return "typecheck_or_checker_failure"


def main() -> None:
    # The selected 133-target run happened first. The remaining run reprocessed
    # 30 selected-run skips; keep the earliest round-0 result for each target.
    targets = {}
    sources = {}
    for path in batch_files():
        payload = json.loads(path.read_text())
        for result in payload["results"]:
            if result["target"] not in targets:
                targets[result["target"]] = result
                sources[result["target"]] = str(path)
    assert len(targets) == 2121
    counts = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    rows = []
    for target, result in sorted(targets.items()):
        value = category(result)
        counts[value] += 1
        if len(examples[value]) < 10:
            examples[value].append(target)
        rows.append(
            {
                "target": target,
                "category": value,
                "source_batch": sources[target],
            }
        )
    assert sum(counts.values()) == 2121
    assert counts == {
        "skip_no_spec": 1659,
        "complete": 150,
        "typecheck_or_checker_failure": 225,
        "unknown": 68,
        "trivial_equality": 19,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    payload = {
        "method": (
            "Saved earliest round-0 result per target. No model or checker was rerun."
        ),
        "counts": dict(counts),
        "targets": rows,
    }
    (OUT / "summary.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = [
        "# Original results before determinism feedback",
        "",
        "Recovered from saved round-0 histories; no rerun was performed.",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| `{key}` | {value} |" for key, value in counts.most_common())
    (OUT / "SUMMARY.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(payload["counts"], indent=2))


if __name__ == "__main__":
    main()
