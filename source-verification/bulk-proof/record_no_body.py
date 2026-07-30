#!/usr/bin/env python3
"""Record pending contracts that have no Rust 1.96 executable body."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "runs" / "no-rust-body"


def main() -> None:
    manifest = json.loads((HERE / "manifest.json").read_text())
    targets = [
        target
        for target in manifest["targets"]
        if not target["preproved"] and not target["has_rust_1_96_body"]
    ]
    results = []
    for target in targets:
        target_dir = OUT / "targets" / target["id"]
        target_dir.mkdir(parents=True, exist_ok=True)
        result = {
            "id": target["id"],
            "api_path": target["api_path"],
            "raw_target": target["raw_target"],
            "status": "blocked_no_rust_body",
            "decision": "blocked",
            "blocker": (
                "Rust 1.96 rustdoc exposes no executable body. The declaration is "
                "trait-only, macro/compiler-generated, or otherwise unavailable for "
                "downstream source copying."
            ),
        }
        (target_dir / "target.json").write_text(json.dumps(target, indent=2) + "\n")
        (target_dir / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
        results.append(result)
    OUT.mkdir(parents=True, exist_ok=True)
    payload = {
        "counts": {"blocked_no_rust_body": len(results)},
        "results": results,
    }
    (OUT / "summary.json").write_text(json.dumps(payload, indent=2) + "\n")
    (OUT / "SUMMARY.md").write_text(
        "# Contracts without a Rust 1.96 executable body\n\n"
        f"- Count: **{len(results)}**\n\n"
        + "\n".join(f"- `{result['api_path']}` — `{result['raw_target']}`" for result in results)
        + "\n"
    )
    print(f"recorded {len(results)} no-body targets")


if __name__ == "__main__":
    main()
