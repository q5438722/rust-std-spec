#!/usr/bin/env python3
"""Add the original contract and Rust implementation beside every copied proof."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_VERIFICATION = HERE.parent
PROVED_ROOT = SOURCE_VERIFICATION / "proved-apis"


def selected_declaration(target: dict) -> dict:
    declarations = target.get("verification_declarations") or []
    for declaration in declarations:
        if declaration.get("has_body"):
            return declaration
    return declarations[0] if declarations else {}


def main() -> None:
    manifest = json.loads((HERE / "manifest.json").read_text())
    targets = {target["id"]: target for target in manifest["targets"]}
    count = 0
    for proof_dir in sorted(path for path in PROVED_ROOT.iterdir() if path.is_dir()):
        target = targets.get(proof_dir.name)
        if target is None:
            continue
        declaration = selected_declaration(target)
        (proof_dir / "contract.rs").write_text(target.get("contract_code", "").rstrip() + "\n")
        (proof_dir / "rust_source.rs").write_text(
            declaration.get("source_text", "").rstrip() + "\n"
        )
        (proof_dir / "api.json").write_text(
            json.dumps(
                {
                    "id": target["id"],
                    "api_path": target["api_path"],
                    "normalized_api_path": target["normalized_api_path"],
                    "raw_target": target["raw_target"],
                    "contract_source_file": target["contract_source_file"],
                    "contract_source_line": target["contract_source_line"],
                    "rust_declaration": declaration,
                },
                indent=2,
            )
            + "\n"
        )
        count += 1
    print(f"materialized {count} proved API directories")


if __name__ == "__main__":
    main()
