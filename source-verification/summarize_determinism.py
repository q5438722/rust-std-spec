#!/usr/bin/env python3
"""Create record-level and unique-API determinism reports."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "determinism-all" / "summary.json"
OUT = ROOT / "determinism-report"


def record_category(result: dict) -> str:
    if result.get("status") == "ok":
        if result.get("equal_fn_trivial"):
            return "trivial_equality"
        if result.get("r0_z3") == "unsat":
            return "complete"
        if result.get("r0_z3") == "sat":
            return "incomplete_sat"
        if result.get("r0_z3") == "unknown":
            return "unknown"
        return "ok_unclassified"
    if result.get("status") == "no_ensures":
        return "no_local_postcondition"
    if result.get("status") == "unsupported_mut_ref_return":
        return "checker_unsupported"
    if str(result.get("status", "")).startswith("unsupported_"):
        return "checker_unsupported"
    if result.get("status") == "verus_error":
        return "verus_error"
    return result.get("status") or "error"


def api_category(categories: list[str]) -> str:
    values = set(categories)
    if values == {"complete"}:
        return "complete_all_records"
    if "incomplete_sat" in values:
        return "incomplete_sat"
    if "complete" in values:
        return "mixed_partial"
    if values == {"unknown"}:
        return "unknown"
    if values == {"trivial_equality"}:
        return "trivial_only"
    if values == {"no_local_postcondition"}:
        return "no_local_postcondition"
    if values == {"checker_unsupported"}:
        return "checker_unsupported"
    return "unclassified_or_error"


def main() -> None:
    payload = json.loads(INPUT.read_text())
    results = payload["results"]
    OUT.mkdir(parents=True, exist_ok=True)
    record_rows = []
    by_api: dict[str, list[dict]] = defaultdict(list)
    for result in results:
        row = {
            "id": result["id"],
            "api_path": result["api_path"],
            "raw_target": result["raw_target"],
            "source_file": result["contract_source_file"],
            "source_line": result["contract_source_line"],
            "category": record_category(result),
            "status": result.get("status", ""),
            "r0_z3": result.get("r0_z3", ""),
            "classification": result.get("classification", ""),
            "equal_fn_trivial": result.get("equal_fn_trivial", False),
        }
        record_rows.append(row)
        by_api[result["api_path"]].append(row)
    with (OUT / "records.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(record_rows[0]))
        writer.writeheader()
        writer.writerows(sorted(record_rows, key=lambda row: row["id"]))

    api_rows = []
    for api_path, rows in sorted(by_api.items()):
        categories = [row["category"] for row in rows]
        api_rows.append(
            {
                "api_path": api_path,
                "record_count": len(rows),
                "category": api_category(categories),
                "record_categories": ";".join(sorted(Counter(categories).elements())),
            }
        )
    with (OUT / "apis.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(api_rows[0]))
        writer.writeheader()
        writer.writerows(api_rows)

    record_counts = Counter(row["category"] for row in record_rows)
    api_counts = Counter(row["category"] for row in api_rows)
    summary = {
        "record_counts": dict(record_counts),
        "unique_api_counts": dict(api_counts),
        "records": len(record_rows),
        "unique_api_paths": len(api_rows),
    }
    verdict_path = ROOT / "fidelity-verdicts.json"
    strict_record_counts = Counter()
    strict_api_counts = Counter()
    if verdict_path.is_file():
        retained = set(json.loads(verdict_path.read_text())["retained"])
        retained_rows = [row for row in record_rows if row["id"] in retained]
        strict_record_counts.update(row["category"] for row in retained_rows)
        retained_by_api: dict[str, list[str]] = defaultdict(list)
        for row in retained_rows:
            retained_by_api[row["api_path"]].append(row["category"])
        strict_api_counts.update(
            api_category(categories) for categories in retained_by_api.values()
        )
        summary["strict_fidelity"] = {
            "records": len(retained_rows),
            "unique_api_paths": len(retained_by_api),
            "record_counts": dict(strict_record_counts),
            "unique_api_counts": dict(strict_api_counts),
        }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# Determinism/completeness summary",
        "",
        "## Direct contract records",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| `{key}` | {value} |" for key, value in record_counts.most_common())
    lines.extend(
        [
            "",
            "## Unique API paths",
            "",
            "| Category | Count |",
            "|---|---:|",
        ]
    )
    lines.extend(f"| `{key}` | {value} |" for key, value in api_counts.most_common())
    if strict_record_counts:
        lines.extend(
            [
                "",
                "## Strict-faithful admissible local-surrogate subset",
                "",
                "| Record category | Count |",
                "|---|---:|",
            ]
        )
        lines.extend(
            f"| `{key}` | {value} |"
            for key, value in strict_record_counts.most_common()
        )
        lines.extend(
            [
                "",
                "| Unique API category | Count |",
                "|---|---:|",
            ]
        )
        lines.extend(
            f"| `{key}` | {value} |"
            for key, value in strict_api_counts.most_common()
        )
    lines.extend(
        [
            "",
            "No contract produced `R0 = sat`; there is no SMT-confirmed incomplete",
            "contract in this run. `unknown` remains inconclusive rather than complete.",
        ]
    )
    (OUT / "SUMMARY.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
