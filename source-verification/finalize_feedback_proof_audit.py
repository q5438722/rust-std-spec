#!/usr/bin/env python3
"""Combine feedback proof campaign results with strict fidelity review."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CAMPAIGN = ROOT / "feedback-proof"


def main() -> None:
    run = json.loads(
        (CAMPAIGN / "runs" / "full-gpt56sol" / "summary.json").read_text()
    )
    audit = json.loads((CAMPAIGN / "audit-passing.json").read_text())
    audited = {record["variant_id"]: record for record in audit["records"]}
    rows = []
    proved = {
        result["id"]
        for result in run["results"]
        if result.get("status") == "proved"
    }
    assert set(audited) == proved
    for result in run["results"]:
        variant_id = result["id"]
        if result.get("status") == "proved":
            review = audited[variant_id]
            verdict = review["strict_verdict"]
            reason = review["reason"]
        else:
            verdict = "not_proved"
            reason = result.get("blocker", "")
        rows.append(
            {
                "variant_id": variant_id,
                "api_path": result["api_path"],
                "campaign_status": result.get("status", ""),
                "strict_verdict": verdict,
                "reason": reason,
            }
        )
    assert len(rows) == 357
    with (CAMPAIGN / "fidelity.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts = {}
    for row in rows:
        counts[row["strict_verdict"]] = counts.get(row["strict_verdict"], 0) + 1
    (CAMPAIGN / "fidelity-summary.json").write_text(
        json.dumps({"counts": counts}, indent=2) + "\n"
    )
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
