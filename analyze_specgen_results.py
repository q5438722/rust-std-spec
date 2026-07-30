#!/usr/bin/env python3
"""Summarize Rust std contract-generation and determinism-feedback results."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
from typing import Any


def decision(round_record: dict[str, Any]) -> str:
    return (round_record.get("candidate") or {}).get(
        "decision",
        round_record.get("decision", ""),
    )


def typecheck_passed(round_record: dict[str, Any]) -> bool:
    typecheck = (round_record.get("checker") or {}).get("typecheck") or {}
    return typecheck.get("returncode") == 0


def det_summary(round_record: dict[str, Any]) -> dict[str, Any]:
    return (round_record.get("checker") or {}).get("determinism") or {}


def semantic_gate_issues(
    target: str,
    requires: list[str],
    ensures: list[str],
) -> list[str]:
    requires_text = "\n".join(requires)
    ensures_text = "\n".join(ensures)
    issues = []
    if target.startswith(
        ("alloc::collections::BTreeMap::", "alloc::collections::BTreeSet::")
    ):
        raw_ops = (".union(", ".union_prefer_right(", ".disjoint(")
        relation_tokens = (
            "deep_view",
            "contains_borrowed_key",
            "sets_borrowed_key_to_key",
            "maps_borrowed_key_to_value",
        )
        if (
            "@" in ensures_text
            and any(token in ensures_text for token in raw_ops)
            and not any(token in ensures_text for token in relation_tokens)
        ):
            issues.append("raw_btree_view_algebra")
    if (
        target.startswith(
            ("alloc::collections::BTreeMap::", "alloc::collections::BTreeSet::")
        )
        and any(
            token in requires_text
            for token in (
                "contains_borrowed_key(",
                "maps_borrowed_key_to_value(",
                "sets_borrowed_key_to_key(",
            )
        )
    ):
        issues.append("borrowed_key_domain_strengthening")
    if re.search(
        r"forall\|[^|]*(?:left|right)[^|]*\|.*==>.*left\s*==\s*right",
        requires_text,
        flags=re.DOTALL,
    ):
        issues.append("borrowed_key_uniqueness_precondition")
    if "strictly_cloned::<" in requires_text or "cloned::<" in requires_text:
        issues.append("clone_behavior_domain_strengthening")
    if target == "alloc::vec::Vec::dedup" and (
        "fold_left(" in ensures_text or "kept.last()" in ensures_text
    ):
        issues.append("dedup_pure_old_sequence_model")
    if target == "alloc::string::String::replace_range" and (
        "slice_range_start(" in requires_text + ensures_text
        or "slice_range_end(" in requires_text + ensures_text
    ):
        issues.append("generic_range_snapshot_mismatch")
    return sorted(set(issues))


def semantic_review_issues(target: str) -> list[str]:
    issues = []
    if target == "core::slice::binary_search":
        issues.append("public_api_allows_any_matching_index")
    if target in {
        "core::ops::RangeInclusive::start",
        "core::ops::RangeInclusive::end",
    }:
        issues.append("value_unspecified_after_exhaustion")
    if target == "std::collections::HashSet::replace":
        issues.append("hash_equivalence_class_view_requires_review")
    return issues


def analyze(payload: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    results = payload["results"]
    rows = []
    transitions = Counter()
    category_counts: dict[str, Counter] = {}
    for result in results:
        history = result.get("history") or []
        initial = history[0] if history else {}
        final = result.get("final") or {}
        initial_decision = decision(initial)
        final_decision = decision(final)
        if history:
            transitions[f"{initial_decision or 'none'}->{final_decision or 'none'}"] += 1
        category = result.get("category", "")
        category_counts.setdefault(category, Counter())[final_decision or "none"] += 1
        det = det_summary(final)
        candidate = final.get("candidate") or {}
        requires = candidate.get("requires") or []
        ensures = candidate.get("ensures") or []
        semantic_issues = semantic_gate_issues(
            result["target"],
            requires,
            ensures,
        )
        review_issues = semantic_review_issues(result["target"])
        guarded_reward = int(final.get("guarded_reward", 0))
        rows.append(
            {
                "target": result["target"],
                "category": category,
                "status": final.get("status", ""),
                "rounds": len(history),
                "initial_decision": initial_decision,
                "final_decision": final_decision,
                "contract_form": candidate.get("contract_form", ""),
                "typecheck_passed": typecheck_passed(final),
                "det_status": det.get("status", ""),
                "r0_z3": det.get("r0_z3", ""),
                "classification": det.get("classification", ""),
                "raw_det_reward": final.get("raw_det_reward", 0),
                "guarded_reward": guarded_reward,
                "semantic_guarded_reward": int(
                    guarded_reward == 1 and not semantic_issues
                ),
                "issues": ";".join(final.get("anti_vacuity_issues", final.get("issues", []))),
                "semantic_gate_issues": ";".join(semantic_issues),
                "semantic_review_issues": ";".join(review_issues),
                "requires": "; ".join(requires),
                "ensures": "; ".join(ensures),
                "contract_code": candidate.get("contract_code", ""),
                "rationale": candidate.get("rationale", ""),
            }
        )

    counts = {
        "targets": len(rows),
        "initial_add_spec": sum(row["initial_decision"] == "add_spec" for row in rows),
        "initial_skip": sum(row["initial_decision"] == "skip" for row in rows),
        "final_add_spec": sum(row["final_decision"] == "add_spec" for row in rows),
        "final_skip": sum(row["final_decision"] == "skip" for row in rows),
        "typecheck_passed": sum(row["typecheck_passed"] for row in rows),
        "det_unsat": sum(row["r0_z3"] == "unsat" for row in rows),
        "det_sat": sum(row["r0_z3"] == "sat" for row in rows),
        "det_unknown": sum(row["r0_z3"] == "unknown" for row in rows),
        "raw_reward": sum(int(row["raw_det_reward"]) for row in rows),
        "guarded_reward": sum(int(row["guarded_reward"]) for row in rows),
        "semantic_guarded_reward": sum(
            int(row["semantic_guarded_reward"]) for row in rows
        ),
        "llm_errors": sum(row["status"] == "llm_error" for row in rows),
        "static_skips": sum(row["status"] == "static_skip" for row in rows),
    }
    analysis = {
        "metadata": payload.get("metadata", {}),
        "counts": counts,
        "transitions": dict(sorted(transitions.items())),
        "categories": {
            category: dict(sorted(values.items()))
            for category, values in sorted(category_counts.items())
        },
        "issue_counts": dict(
            Counter(
                issue
                for row in rows
                for issue in row["issues"].split(";")
                if issue
            ).most_common()
        ),
        "semantic_gate_issue_counts": dict(
            Counter(
                issue
                for row in rows
                for issue in row["semantic_gate_issues"].split(";")
                if issue
            ).most_common()
        ),
        "semantic_review_issue_counts": dict(
            Counter(
                issue
                for row in rows
                for issue in row["semantic_review_issues"].split(";")
                if issue
            ).most_common()
        ),
    }
    return analysis, rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    analysis: dict[str, Any],
    rows: list[dict[str, Any]],
) -> None:
    counts = analysis["counts"]
    lines = [
        "# Rust std contract generation with determinism feedback",
        "",
        "## Aggregate result",
        "",
        "| Metric | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "External `assume_specification` declarations are trusted. A guarded "
            "determinism reward means only that the candidate typechecked, avoided "
            "the configured vacuity gates, and uniquely determined the modeled "
            "outputs. It does not prove the contract sound.",
            "",
            "## Feedback transitions",
            "",
            "| Transition | Count |",
            "|---|---:|",
        ]
    )
    for transition, count in analysis["transitions"].items():
        lines.append(f"| `{transition}` | {count} |")
    lines.extend(
        [
            "",
            "## Frequent issues",
            "",
            "| Issue | Count |",
            "|---|---:|",
        ]
    )
    for issue, count in list(analysis["issue_counts"].items())[:30]:
        lines.append(f"| `{issue}` | {count} |")
    successes = [row for row in rows if int(row["guarded_reward"]) == 1]
    semantic_successes = [
        row for row in rows if int(row["semantic_guarded_reward"]) == 1
    ]
    lines.extend(
        [
            "",
            "## Guarded-deterministic candidates",
            "",
            "| Target | Ensures |",
            "|---|---|",
        ]
    )
    for row in successes:
        lines.append(f"| `{row['target']}` | `{row['ensures']}` |")
    lines.extend(
        [
            "",
            "## Semantic-gated candidates",
            "",
            f"{len(semantic_successes)} of {len(successes)} guarded-deterministic "
            "candidates pass the pilot-derived semantic postprocessing gates.",
            "",
            "| Target | Ensures |",
            "|---|---|",
        ]
    )
    for row in semantic_successes:
        lines.append(f"| `{row['target']}` | `{row['ensures']}` |")
    lines.extend(
        [
            "",
            "## Per-target result",
            "",
            "| Target | Initial | Final | Typecheck | R0 | Guarded | Semantic | Issues |",
            "|---|---|---|---:|---|---:|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['target']}` | {row['initial_decision']} | "
            f"{row['final_decision']} | {int(row['typecheck_passed'])} | "
            f"{row['r0_z3']} | {row['guarded_reward']} | "
            f"{row['semantic_guarded_reward']} | "
            f"{';'.join(filter(None, [row['issues'], row['semantic_gate_issues'], row['semantic_review_issues']]))} |"
        )
    path.write_text("\n".join(lines).rstrip() + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_summary", type=Path, nargs="+")
    parser.add_argument("--out-dir", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payloads = [json.loads(path.read_text()) for path in args.batch_summary]
    by_target = {}
    for payload in payloads:
        for result in payload["results"]:
            by_target[result["target"]] = result
    payload = {
        "metadata": {
            "batches": [item.get("metadata", {}) for item in payloads],
            "batch_files": [str(path.resolve()) for path in args.batch_summary],
        },
        "results": list(by_target.values()),
    }
    out_dir = args.out_dir or args.batch_summary[0].parent
    out_dir.mkdir(parents=True, exist_ok=True)
    analysis, rows = analyze(payload)
    (out_dir / "analysis.json").write_text(
        json.dumps(analysis, indent=2, sort_keys=True) + "\n"
    )
    write_csv(out_dir / "final_candidates.csv", rows)
    write_report(out_dir / "ANALYSIS.md", analysis, rows)
    print(
        f"analyzed {analysis['counts']['targets']} targets; "
        f"guarded reward={analysis['counts']['guarded_reward']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
