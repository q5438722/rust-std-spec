#!/usr/bin/env python3
"""Summarize strict retries for previously alternate implementations."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RETRY = ROOT / "fidelity-retry"


def blocker_category(text: str) -> str:
    value = text.lower()
    if any(word in value for word in ("private", "inaccessible", "visibility")):
        return "private_or_internal_operation_inaccessible"
    if any(
        word in value
        for word in (
            "circular",
            "exact target",
            "same target",
            "target `",
            "lowers",
        )
    ):
        return "exact_operation_is_target_or_circular"
    if any(
        word in value
        for word in (
            "intrinsic",
            "compiler",
            "unsupported",
            "not support",
            "cannot represent",
            "cannot encode",
        )
    ):
        return "verus_or_compiler_operation_unavailable"
    if any(
        word in value
        for word in (
            "contract",
            "specification",
            "postcondition",
            "view",
            "model",
        )
    ):
        return "missing_lower_contract_or_model_bridge"
    if any(word in value for word in ("panic", "unwind", "unsafe precondition")):
        return "panic_or_unsafe_behavior_not_supported"
    return "other_strict_fidelity_blocker"


def main() -> None:
    run = json.loads(
        (RETRY / "runs" / "full-gpt56sol" / "summary.json").read_text()
    )
    audit_path = RETRY / "audit.json"
    audit = json.loads(audit_path.read_text()) if audit_path.is_file() else None
    accepted = []
    rejected = []
    if audit is not None:
        for record in audit["records"]:
            if record["strict_verdict"] == "strict_faithful_admissible":
                accepted.append(record)
            else:
                rejected.append(record)

    blocked = [
        result for result in run["results"] if result.get("status") != "proved"
    ]
    blocker_counts = Counter(
        blocker_category(result.get("blocker", "")) for result in blocked
    )
    summary = {
        "attempted": len(run["results"]),
        "verus_passed": sum(
            result.get("status") == "proved" for result in run["results"]
        ),
        "blocked": len(blocked),
        "fidelity_review": (
            {
                "accepted": len(accepted),
                "rejected": len(rejected),
            }
            if audit is not None
            else {"status": "pending"}
        ),
        "blocker_categories": dict(blocker_counts),
    }
    (RETRY / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# Strict implementation-fidelity retry",
        "",
        "| Result | Count |",
        "|---|---:|",
        f"| Previously alternate-implementation records retried | {len(run['results'])} |",
        f"| Verus-passing retry artifacts | {summary['verus_passed']} |",
        f"| Blocked under exact-body policy | {len(blocked)} |",
    ]
    if audit is not None:
        lines.extend(
            [
                f"| Accepted after independent fidelity review | **{len(accepted)}** |",
                f"| Passing retry artifacts rejected by review | {len(rejected)} |",
            ]
        )
    else:
        lines.append("| Fidelity review | pending |")
    lines.extend(
        [
            "",
            "## Blocker categories",
            "",
            "| Category | Count |",
            "|---|---:|",
        ]
    )
    lines.extend(
        f"| `{category}` | {count} |"
        for category, count in blocker_counts.most_common()
    )
    if accepted:
        lines.extend(["", "## Newly accepted records", ""])
        lines.extend(
            f"- `{record['id']}` — {record['reason']}" for record in accepted
        )
    (RETRY / "SUMMARY.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
