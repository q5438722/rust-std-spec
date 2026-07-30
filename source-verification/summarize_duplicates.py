#!/usr/bin/env python3
"""Summarize why direct vstd contract records share canonical API paths."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "source-verification" / "duplicates"


def main() -> None:
    records = [
        record
        for record in json.loads((ROOT / "results" / "vstd_contracts.json").read_text())
        if record["mechanism"] == "assume_specification"
        and record["confidence"] == "high"
    ]
    by_path = defaultdict(list)
    for record in records:
        by_path[record["api_path"]].append(record)
    duplicates = {
        path: values for path, values in by_path.items() if len(values) > 1
    }
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for path, values in sorted(duplicates.items()):
        for record in values:
            rows.append(
                {
                    "api_path": path,
                    "record_count": len(values),
                    "raw_target": record["raw_target"],
                    "source_file": record["source_file"],
                    "source_line": record["source_line"],
                }
            )
    with (OUT / "records.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter({path: len(values) for path, values in duplicates.items()})
    payload = {
        "direct_contract_records": len(records),
        "unique_api_paths": len(by_path),
        "extra_records_after_path_deduplication": len(records) - len(by_path),
        "duplicated_api_paths": len(duplicates),
        "top_duplicates": counts.most_common(),
    }
    (OUT / "summary.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = [
        "# Duplicate direct-contract records",
        "",
        f"- Direct records: **{len(records)}**",
        f"- Canonical API paths: **{len(by_path)}**",
        f"- Extra records after path deduplication: **{len(records) - len(by_path)}**",
        f"- Paths with more than one record: **{len(duplicates)}**",
        "",
        "A duplicate path usually does not mean duplicated Rust code. Contract records",
        "retain concrete impl type, bounds, cfg variant, and source location, while",
        "canonical API paths intentionally collapse them.",
        "",
        "Largest examples:",
        "",
    ]
    lines.extend(f"- `{path}`: {count} records" for path, count in counts.most_common(15))
    (OUT / "SUMMARY.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
