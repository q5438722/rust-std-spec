#!/usr/bin/env python3
"""Build a strict retry manifest for alternate-implementation proof artifacts."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "fidelity-retry"


def source_excerpt(path_value: str, lines_value: str) -> str:
    if not path_value or not lines_value:
        return ""
    path = Path(path_value)
    if not path.is_file():
        return ""
    match = re.search(r"(\d+)(?:-(\d+))?", str(lines_value))
    if match is None:
        return ""
    start = int(match.group(1))
    end = int(match.group(2) or start)
    lines = path.read_text(errors="replace").splitlines()
    start = max(1, start)
    end = min(len(lines), end)
    return "\n".join(
        f"{index:>6}: {lines[index - 1]}" for index in range(start, end + 1)
    )


def main() -> None:
    manifest = json.loads((ROOT / "bulk-proof" / "manifest.json").read_text())
    targets = {target["id"]: target for target in manifest["targets"]}
    with (ROOT / "surrogate-audit" / "records.csv").open() as stream:
        audit_rows = list(csv.DictReader(stream))

    selected = []
    for row in audit_rows:
        if (
            row["strict_verdict"] != "known_mismatch_or_inadmissible"
            or row["body_fidelity"] != "alternate_implementation"
        ):
            continue
        target = copy.deepcopy(targets[row["id"]])
        target["preproved"] = False
        excerpt = source_excerpt(
            row.get("resolved_source_path", ""),
            row.get("resolved_source_lines", ""),
        )
        context = [
            "This is a strict implementation-fidelity retry.",
            f"Previous audit rejection: {row['reason']}",
            f"Previous proof artifact: {ROOT / 'proved-apis' / row['id'] / 'proof.rs'}",
            "",
            "Mandatory retry rules:",
            "- Keep the Rust executable operations and control flow unchanged.",
            "- Do not replace private fields or internal helpers with public APIs.",
            "- Do not substitute an extensionally equivalent algorithm.",
            "- Do not declare any new axiom or target-equivalent representation bridge.",
            "- Calls to already specified, genuinely smaller operations are allowed.",
            "- Copy additional internal helper bodies mechanically when practical.",
            "- If downstream visibility or Verus support prevents the exact body, return blocked.",
        ]
        if row.get("resolved_source_path"):
            context.extend(
                [
                    "",
                    "Resolved Rust source:",
                    f"{row['resolved_source_path']}:{row['resolved_source_lines']}",
                    excerpt,
                ]
            )
        target["fidelity_retry_context"] = "\n".join(context)
        target["fidelity_retry"] = {
            "previous_body_fidelity": row["body_fidelity"],
            "previous_admissibility": row["proof_admissibility"],
            "audit_reason": row["reason"],
            "resolved_source_path": row.get("resolved_source_path", ""),
            "resolved_source_lines": row.get("resolved_source_lines", ""),
        }
        selected.append(target)

    assert len(selected) == 204, len(selected)
    payload = {
        "metadata": {
            "purpose": (
                "Retry every alternate-implementation artifact with exact Rust "
                "operations/control flow and no new axioms."
            ),
            "source_manifest": str(ROOT / "bulk-proof" / "manifest.json"),
        },
        "counts": {
            "targets": len(selected),
            "with_resolved_source_excerpt": sum(
                bool(target["fidelity_retry"]["resolved_source_path"])
                for target in selected
            ),
        },
        "targets": selected,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload["counts"], indent=2))


if __name__ == "__main__":
    main()
