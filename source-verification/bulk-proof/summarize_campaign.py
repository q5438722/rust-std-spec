#!/usr/bin/env python3
"""Aggregate preproved, generated-proof, and blocked contract campaign results."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_VERIFICATION = HERE.parent
PROVED_ROOT = SOURCE_VERIFICATION / "proved-apis"


def load(path: Path, default):
    return json.loads(path.read_text()) if path.is_file() else default


def main() -> None:
    manifest = load(HERE / "manifest.json", {"counts": {}, "targets": []})
    no_body = load(HERE / "runs" / "no-rust-body" / "summary.json", {"results": []})
    preproved = load(PROVED_ROOT / "preproved_manifest.json", {"targets": []})

    by_id = {}
    for target in preproved["targets"]:
        by_id[target["id"]] = {
            **target,
            "status": "preproved",
        }
    for result in no_body["results"]:
        by_id[result["id"]] = result
    rank = {
        "proved": 100,
        "preproved": 100,
        "blocked": 40,
        "blocked_no_rust_body": 30,
        "verus_error": 20,
        "llm_error": 10,
        "exception": 0,
    }
    for summary_path in sorted((HERE / "runs").glob("*/summary.json")):
        run = load(summary_path, {"results": []})
        for result in run.get("results", []):
            current = by_id.get(result["id"])
            if current is None or rank.get(result.get("status", ""), 0) >= rank.get(
                current.get("status", ""),
                0,
            ):
                by_id[result["id"]] = {
                    **result,
                    "selected_run": summary_path.parent.name,
                }

    proof_entries = []
    if PROVED_ROOT.is_dir():
        for metadata_path in sorted(PROVED_ROOT.glob("*/metadata.json")):
            proof_entries.append(json.loads(metadata_path.read_text()))
    status_counts = Counter(result.get("status", "unknown") for result in by_id.values())
    payload = {
        "scope": manifest.get("counts", {}),
        "status_counts": dict(status_counts),
        "proved_api_directories": len(proof_entries),
        "results": sorted(by_id.values(), key=lambda item: item["id"]),
    }
    (HERE / "OVERALL.json").write_text(json.dumps(payload, indent=2) + "\n")

    lines = [
        "# All-vstd source-proof campaign",
        "",
        f"- Direct `assume_specification` records: **{manifest.get('counts', {}).get('direct_assume_specification_records', 0)}**",
        f"- Preproved and exported: **{status_counts.get('preproved', 0)}**",
        f"- Newly proved by bulk run: **{status_counts.get('proved', 0)}**",
        f"- No Rust 1.96 body: **{status_counts.get('blocked_no_rust_body', 0)}**",
        f"- Other statuses: `{dict(status_counts)}`",
        f"- Per-API proof directories: **{len(proof_entries)}**",
        "",
        "Successful proofs are copied under:",
        "",
        "```text",
        str(PROVED_ROOT),
        "```",
    ]
    (HERE / "OVERALL.md").write_text("\n".join(lines) + "\n")

    PROVED_ROOT.mkdir(parents=True, exist_ok=True)
    (PROVED_ROOT / "manifest.json").write_text(
        json.dumps({"count": len(proof_entries), "proofs": proof_entries}, indent=2) + "\n"
    )
    (PROVED_ROOT / "README.md").write_text(
        "# Proved Rust std API contracts\n\n"
        "Each child directory represents one direct vstd `assume_specification` "
        "record with a passing Verus source-level proof harness:\n\n"
        "- `proof.rs`: passing Verus proof harness;\n"
        "- `contract.rs`: original vstd contract;\n"
        "- `rust_source.rs`: copied Rust 1.96 implementation when available;\n"
        "- `api.json`: API/declaration metadata;\n"
        "- `metadata.json`: proof provenance and trust classification.\n\n"
        f"Current directories: **{len(proof_entries)}**.\n"
    )
    print(json.dumps(payload["status_counts"], indent=2))
    print(f"proved directories: {len(proof_entries)}")


if __name__ == "__main__":
    main()
