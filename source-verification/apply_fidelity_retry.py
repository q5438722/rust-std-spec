#!/usr/bin/env python3
"""Apply independently audited strict fidelity retry proofs."""

from __future__ import annotations

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
RETRY = ROOT / "fidelity-retry"
RETRY_PROVED = RETRY / "proved-apis"
MAIN_PROVED = ROOT / "proved-apis"


def main() -> None:
    audit = json.loads((RETRY / "audit.json").read_text())
    accepted = [
        record
        for record in audit["records"]
        if record["strict_verdict"] == "strict_faithful_admissible"
    ]
    backup_root = RETRY / "pre-retry-proofs"
    overrides = []
    for record in accepted:
        target_id = record["id"]
        source = RETRY_PROVED / target_id
        destination = MAIN_PROVED / target_id
        assert (source / "proof.rs").is_file(), target_id
        backup = backup_root / target_id
        backup.mkdir(parents=True, exist_ok=True)
        for filename in ("proof.rs", "metadata.json"):
            current = destination / filename
            if current.is_file() and not (backup / filename).exists():
                shutil.copy2(current, backup / filename)
            replacement = source / filename
            if replacement.is_file():
                shutil.copy2(replacement, destination / filename)
        metadata_path = destination / "metadata.json"
        metadata = json.loads(metadata_path.read_text())
        metadata["fidelity_retry"] = {
            "accepted": True,
            "audit_reason": record["reason"],
            "source_run": str(source),
        }
        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")
        overrides.append(
            {
                "id": target_id,
                "body_fidelity": record["body_fidelity"],
                "proof_admissibility": record["proof_admissibility"],
                "reason": record["reason"],
                "resolved_source_path": record.get("resolved_source_path", ""),
                "resolved_source_lines": record.get("resolved_source_lines", ""),
            }
        )

    (RETRY / "accepted-overrides.json").write_text(
        json.dumps(
            {
                "count": len(overrides),
                "records": sorted(overrides, key=lambda record: record["id"]),
            },
            indent=2,
        )
        + "\n"
    )
    print(json.dumps({"accepted": len(overrides)}, indent=2))


if __name__ == "__main__":
    main()
