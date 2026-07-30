#!/usr/bin/env python3
"""Write final strict implementation-fidelity reports."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROVED = ROOT / "proved-apis"


def main() -> None:
    verdicts = json.loads((ROOT / "fidelity-verdicts.json").read_text())
    organized = json.loads((ROOT / "organized-suite" / "verification.json").read_text())
    manifest = json.loads((ROOT / "bulk-proof" / "manifest.json").read_text())
    targets = {target["id"]: target for target in manifest["targets"]}
    retained = set(verdicts["retained"])
    downgraded = set(verdicts["downgraded"])
    trust = Counter()
    rows = []
    for target_id in sorted(retained | downgraded):
        target = targets[target_id]
        metadata = json.loads((PROVED / target_id / "metadata.json").read_text())
        verdict = "retained" if target_id in retained else "downgraded"
        if verdict == "retained":
            trust[metadata.get("trust_level", "unknown")] += 1
        rows.append(
            {
                "id": target_id,
                "api_path": target["api_path"],
                "raw_target": target["raw_target"],
                "source_file": target["contract_source_file"],
                "source_line": target["contract_source_line"],
                "verdict": verdict,
                "trust_level": metadata.get("trust_level", ""),
            }
        )
    out = ROOT / "fidelity-report"
    out.mkdir(exist_ok=True)
    with (out / "verdicts.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    group_downgrades = Counter(
        targets[target_id]["contract_source_file"] for target_id in downgraded
    )
    summary = {
        "original_passing_harnesses": len(rows),
        "retained_strict_faithful_surrogates": len(retained),
        "not_retained": len(downgraded),
        "retained_trust_levels": dict(trust),
        "not_retained_by_source_file": dict(group_downgrades),
        "organized_suite_verification": organized["counts"],
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# Strict proof/source fidelity audit",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Mechanically passing proof harnesses before audit | {len(rows)} |",
        f"| Retained strict-faithful admissible local surrogates | **{len(retained)}** |",
        f"| Passing artifacts not retained | **{len(downgraded)}** |",
        "",
        "No original Rust std symbol is directly proved. The conservative policy",
        "retains only local `source_*` surrogates whose executable bodies are exact",
        "copies or mechanical desugarings and whose proof artifacts are admissible.",
        "Alternate algorithms, target-critical axioms, wrong mappings, unresolved",
        "source bodies, and blocked records use external-body fallback.",
        "",
        "## Retained trust levels",
        "",
        "| Level | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| {key} | {value} |" for key, value in trust.most_common())
    lines.extend(
        [
            "",
            "## Largest not-retained groups",
            "",
        ]
    )
    lines.extend(
        f"- `{source}`: {count}"
        for source, count in group_downgrades.most_common(20)
    )
    lines.extend(
        [
            "",
            "## Strict organized suite",
            "",
            f"- Strict-faithful local-surrogate proofs: **{organized['counts']['proved_passed']}**",
            f"- External-body fallbacks: **{organized['counts']['external_body_passed']}**",
            f"- Full run: **{organized['counts']['passed']} passed, "
            f"{organized['counts']['failed']} failed**",
        ]
    )
    (out / "SUMMARY.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
