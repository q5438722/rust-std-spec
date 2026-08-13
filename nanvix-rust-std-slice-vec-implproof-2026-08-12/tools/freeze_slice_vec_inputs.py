#!/usr/bin/env python3
"""Freeze Slice/Vec inputs for implementation-proof work.

This script copies only from the completed isolated Slice/Vec module workspaces
into the implementation-proof workspace and records hashes for every frozen
file. It does not edit the canonical Rust/vstd/source checkouts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TARGET_ROOT = Path("/home/chentianyu/nanvix-rust-std-spec-survey/nanvix-rust-std-slice-vec-implproof-2026-08-12")
DEPENDENCY_LATEST = Path("/home/chentianyu/.argus-skill/projects/s-8d9b336f/handoffs/180cfdc34b6c/latest.json")
DEPENDENCY_CHECKPOINT = Path("/home/chentianyu/.argus-skill/projects/s-8d9b336f/handoffs/180cfdc34b6c/CHECKPOINT.md")
RUST_196_LIBRARY = Path("/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library")


MODULES = {
    "slice": {
        "source_root": Path("/home/chentianyu/nanvix-rust-std-spec-survey/nanvix-rust-std-slice-specgen-2026-08-11"),
        "generated_count": 120,
        "source_dirs": ["rust-core-slice", "vstd-baseline"],
        "extra_source_files": [
            {
                "source_workspace": RUST_196_LIBRARY,
                "source_relpath": "core/src/mem/maybe_uninit.rs",
                "frozen_relpath": "rust-core-adjacent/mem/maybe_uninit.rs",
                "rust_source_reference": "core/src/mem/maybe_uninit.rs",
            },
            {
                "source_workspace": RUST_196_LIBRARY,
                "source_relpath": "core/src/str/lossy.rs",
                "frozen_relpath": "rust-core-adjacent/str/lossy.rs",
                "rust_source_reference": "core/src/str/lossy.rs",
            },
        ],
        "file_globs": [
            "catalog/*",
            "inventory/*",
            "provenance/*",
            "results/modules.csv",
            "results/coverage.csv",
            "specs/*.rs",
            "verification/shared_helper_target_usage_audit.*",
            "verification/artifact_integrity_evidence.*",
        ],
        "catalog": "catalog/slice_spec_catalog.csv",
        "helper_audit": "verification/shared_helper_target_usage_audit.csv",
    },
    "vec": {
        "source_root": Path("/home/chentianyu/nanvix-rust-std-spec-survey/nanvix-rust-std-vec-specgen-2026-08-11"),
        "generated_count": 24,
        "source_dirs": ["rust-alloc-vec", "rust-alloc-adjacent", "vstd-baseline"],
        "extra_source_files": [],
        "file_globs": [
            "catalog/*",
            "inventory/*",
            "provenance/*",
            "results/modules.csv",
            "results/coverage.csv",
            "specs/*.rs",
            "verification/shared_helper_target_usage_audit.*",
            "verification/artifact_integrity_evidence.*",
        ],
        "catalog": "catalog/vec_spec_catalog.csv",
        "helper_audit": "verification/shared_helper_target_usage_audit.csv",
    },
}


GENERATED_STATUS = "generated-new-real-relation-spec"
EXISTING_VSTD_STATUS = "existing-vstd"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def iter_selected_files(module: str, config: dict[str, Any]) -> list[Path]:
    source_root = config["source_root"]
    selected: set[Path] = set()

    for rel_dir in config["source_dirs"]:
        directory = source_root / rel_dir
        if not directory.is_dir():
            raise FileNotFoundError(f"{module}: missing source directory {directory}")
        for path in directory.rglob("*"):
            if path.is_file():
                selected.add(path)

    for pattern in config["file_globs"]:
        matches = [path for path in source_root.glob(pattern) if path.is_file()]
        if not matches:
            raise FileNotFoundError(f"{module}: no files matched {pattern}")
        selected.update(matches)

    return sorted(selected, key=lambda path: path.relative_to(source_root).as_posix())


def copy_inputs(refresh: bool) -> list[dict[str, Any]]:
    frozen_root = TARGET_ROOT / "frozen_inputs"
    manifest_path = frozen_root / "file_manifest.json"
    if manifest_path.exists() and not refresh:
        raise FileExistsError(f"{manifest_path} already exists; pass --refresh to rebuild")

    rows: list[dict[str, Any]] = []
    for module, config in MODULES.items():
        source_root = config["source_root"]
        module_root = frozen_root / module
        if refresh and module_root.exists():
            shutil.rmtree(module_root)
        module_root.mkdir(parents=True, exist_ok=True)

        for source_path in iter_selected_files(module, config):
            rel = source_path.relative_to(source_root)
            frozen_path = module_root / rel
            frozen_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, frozen_path)
            source_hash = sha256_file(source_path)
            frozen_hash = sha256_file(frozen_path)
            if source_hash != frozen_hash:
                raise RuntimeError(f"hash mismatch after copy: {source_path} -> {frozen_path}")
            rows.append(
                {
                    "module": module,
                    "category": classify_relpath(rel),
                    "source_workspace": str(source_root),
                    "source_relpath": rel.as_posix(),
                    "frozen_relpath": frozen_path.relative_to(TARGET_ROOT).as_posix(),
                    "rust_source_reference": rust_source_reference(module, rel),
                    "sha256": frozen_hash,
                    "bytes": frozen_path.stat().st_size,
                }
            )

        for extra in config.get("extra_source_files", []):
            source_workspace = Path(extra["source_workspace"])
            source_relpath = Path(extra["source_relpath"])
            source_path = source_workspace / source_relpath
            if not source_path.is_file():
                raise FileNotFoundError(f"{module}: missing extra source file {source_path}")
            frozen_path = module_root / extra["frozen_relpath"]
            frozen_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, frozen_path)
            source_hash = sha256_file(source_path)
            frozen_hash = sha256_file(frozen_path)
            if source_hash != frozen_hash:
                raise RuntimeError(f"hash mismatch after copy: {source_path} -> {frozen_path}")
            rows.append(
                {
                    "module": module,
                    "category": "rust-1.96-source-body",
                    "source_workspace": str(source_workspace),
                    "source_relpath": source_relpath.as_posix(),
                    "frozen_relpath": frozen_path.relative_to(TARGET_ROOT).as_posix(),
                    "rust_source_reference": extra["rust_source_reference"],
                    "sha256": frozen_hash,
                    "bytes": frozen_path.stat().st_size,
                }
            )

    rows.sort(key=lambda row: (row["module"], row["source_relpath"]))
    return rows


def classify_relpath(rel: Path) -> str:
    parts = rel.parts
    if not parts:
        return "unknown"
    if parts[0].startswith("rust-"):
        return "rust-1.96-source-body"
    if parts[0] == "vstd-baseline":
        return "vstd-definition"
    if parts[0] == "specs":
        return "contract-or-vocabulary"
    if parts[0] == "catalog":
        return "catalog"
    if parts[0] == "inventory":
        return "module-inventory"
    if parts[0] == "provenance":
        return "source-provenance"
    if parts[0] == "results":
        return "canonical-survey-snapshot"
    if parts[0] == "verification":
        return "verification-audit"
    return parts[0]


def rust_source_reference(module: str, rel: Path) -> str:
    parts = rel.parts
    if module == "slice" and parts[:1] == ("rust-core-slice",):
        return Path("core/src/slice", *parts[1:]).as_posix()
    if module == "vec" and parts[:2] == ("rust-alloc-vec", "vec"):
        return Path("alloc/src/vec", *parts[2:]).as_posix()
    if module == "vec" and parts[:1] == ("rust-alloc-adjacent",):
        return Path("alloc/src", *parts[1:]).as_posix()
    return ""


def build_target_inventory() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    order = 0
    for module, config in MODULES.items():
        source_root = config["source_root"]
        catalog_rows = read_csv(source_root / config["catalog"])
        helper_rows = {
            row["target"]: row
            for row in read_csv(source_root / config["helper_audit"])
        }
        generated_rows = [row for row in catalog_rows if row.get("status") == GENERATED_STATUS]
        expected = int(config["generated_count"])
        if len(generated_rows) != expected:
            raise RuntimeError(f"{module}: expected {expected} generated rows, found {len(generated_rows)}")

        for row in generated_rows:
            order += 1
            target = row["target"]
            helper = helper_rows.get(target, {})
            rows.append(
                {
                    "input_order": order,
                    "module": module,
                    "target": target,
                    "semantic_family": row.get("semantic_family", ""),
                    "catalog_status": row.get("status", ""),
                    "source_reference": row.get("source_reference", ""),
                    "source_excerpt": row.get("source_excerpt", ""),
                    "contract_sha256": hashlib.sha256(row.get("contract_text", "").encode()).hexdigest(),
                    "contract_text": row.get("contract_text", ""),
                    "requires": row.get("requires", ""),
                    "ensures": row.get("ensures", ""),
                    "direct_shared_helpers": helper.get("direct_shared_helpers", ""),
                    "reachable_shared_helpers": helper.get("reachable_shared_helpers", ""),
                    "audited_shared_helpers": helper.get("audited_shared_helpers", ""),
                    "source_backed_helpers": helper.get("source-backed", ""),
                    "law_constrained_helpers": helper.get("law-constrained", ""),
                    "boundary_helpers": helper.get("irreducible-boundary-abstraction", ""),
                    "implementation_body_status": "pending_source_body_extraction",
                    "private_helper_callee_closure": "pending_dependency_closure",
                    "unsafe_intrinsic_trait_allocator_dependencies": "pending_dependency_closure",
                    "proof_order": "pending_bottom_up_ordering",
                    "proof_status": "pending_implementation_proof",
                    "abcd_status": "",
                }
            )

    expected_total = sum(int(config["generated_count"]) for config in MODULES.values())
    if len(rows) != expected_total:
        raise RuntimeError(f"expected {expected_total} total generated rows, found {len(rows)}")
    return rows


def dependency_status() -> dict[str, Any]:
    latest = json.loads(DEPENDENCY_LATEST.read_text())
    status = {
        "latest_path": str(DEPENDENCY_LATEST),
        "latest_sha256": sha256_file(DEPENDENCY_LATEST),
        "checkpoint_path": str(DEPENDENCY_CHECKPOINT),
        "checkpoint_sha256": sha256_file(DEPENDENCY_CHECKPOINT),
    }
    if latest.get("kind") == "handoff_ref":
        handoff_path = Path(latest["handoff"]["path"])
        handoff = json.loads(handoff_path.read_text())
        status.update(
            {
                "kind": latest.get("kind"),
                "review_handoff_path": str(handoff_path),
                "review_handoff_sha256": sha256_file(handoff_path),
                "review_status": handoff.get("review", {}).get("status", ""),
                "review_reason": handoff.get("review", {}).get("reason", ""),
            }
        )
    else:
        status.update({"kind": latest.get("kind"), "review_status": ""})
    if status.get("review_status") != "done":
        raise RuntimeError(f"dependency 180cfdc34b6c is not accepted: {status}")
    return status


def write_freeze(refresh: bool) -> None:
    TARGET_ROOT.mkdir(parents=True, exist_ok=True)
    (TARGET_ROOT / "proof_inventory").mkdir(parents=True, exist_ok=True)
    (TARGET_ROOT / "frozen_inputs").mkdir(parents=True, exist_ok=True)

    file_rows = copy_inputs(refresh)
    file_fields = [
        "module",
        "category",
        "source_workspace",
        "source_relpath",
        "frozen_relpath",
        "rust_source_reference",
        "sha256",
        "bytes",
    ]
    write_csv(TARGET_ROOT / "frozen_inputs" / "file_manifest.csv", file_rows, file_fields)
    write_json(TARGET_ROOT / "frozen_inputs" / "file_manifest.json", file_rows)

    target_rows = build_target_inventory()
    target_fields = [
        "input_order",
        "module",
        "target",
        "semantic_family",
        "catalog_status",
        "source_reference",
        "source_excerpt",
        "contract_sha256",
        "contract_text",
        "requires",
        "ensures",
        "direct_shared_helpers",
        "reachable_shared_helpers",
        "audited_shared_helpers",
        "source_backed_helpers",
        "law_constrained_helpers",
        "boundary_helpers",
        "implementation_body_status",
        "private_helper_callee_closure",
        "unsafe_intrinsic_trait_allocator_dependencies",
        "proof_order",
        "proof_status",
        "abcd_status",
    ]
    write_csv(TARGET_ROOT / "proof_inventory" / "targets_144.csv", target_rows, target_fields)
    write_json(TARGET_ROOT / "proof_inventory" / "targets_144.json", target_rows)

    target_counts = Counter(row["module"] for row in target_rows)
    category_counts = Counter(row["category"] for row in file_rows)
    module_file_counts = Counter(row["module"] for row in file_rows)
    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(TARGET_ROOT),
        "dependency": dependency_status(),
        "frozen_file_count": len(file_rows),
        "frozen_file_counts_by_module": dict(sorted(module_file_counts.items())),
        "frozen_file_counts_by_category": dict(sorted(category_counts.items())),
        "target_count": len(target_rows),
        "target_counts_by_module": dict(sorted(target_counts.items())),
        "target_counts_by_proof_status": dict(Counter(row["proof_status"] for row in target_rows)),
        "manifests": {
            "file_manifest_csv": "frozen_inputs/file_manifest.csv",
            "file_manifest_json": "frozen_inputs/file_manifest.json",
            "targets_csv": "proof_inventory/targets_144.csv",
            "targets_json": "proof_inventory/targets_144.json",
        },
    }
    write_json(TARGET_ROOT / "proof_inventory" / "target_counts.json", {
        "target_count": len(target_rows),
        "target_counts_by_module": dict(sorted(target_counts.items())),
        "semantic_family_counts": dict(sorted(Counter(row["semantic_family"] for row in target_rows).items())),
        "proof_status_counts": dict(Counter(row["proof_status"] for row in target_rows)),
    })
    write_json(TARGET_ROOT / "FREEZE_SUMMARY.json", summary)

    manifest_hashes = {
        "frozen_inputs/file_manifest.csv": sha256_file(TARGET_ROOT / "frozen_inputs" / "file_manifest.csv"),
        "frozen_inputs/file_manifest.json": sha256_file(TARGET_ROOT / "frozen_inputs" / "file_manifest.json"),
        "proof_inventory/targets_144.csv": sha256_file(TARGET_ROOT / "proof_inventory" / "targets_144.csv"),
        "proof_inventory/targets_144.json": sha256_file(TARGET_ROOT / "proof_inventory" / "targets_144.json"),
        "proof_inventory/target_counts.json": sha256_file(TARGET_ROOT / "proof_inventory" / "target_counts.json"),
        "FREEZE_SUMMARY.json": sha256_file(TARGET_ROOT / "FREEZE_SUMMARY.json"),
    }
    write_json(TARGET_ROOT / "frozen_inputs" / "manifest_hashes.json", manifest_hashes)


def check_freeze() -> None:
    file_manifest_path = TARGET_ROOT / "frozen_inputs" / "file_manifest.json"
    targets_path = TARGET_ROOT / "proof_inventory" / "targets_144.json"
    summary_path = TARGET_ROOT / "FREEZE_SUMMARY.json"
    for path in [file_manifest_path, targets_path, summary_path]:
        if not path.is_file():
            raise FileNotFoundError(path)

    file_rows = json.loads(file_manifest_path.read_text())
    for row in file_rows:
        frozen_path = TARGET_ROOT / row["frozen_relpath"]
        if not frozen_path.is_file():
            raise FileNotFoundError(frozen_path)
        actual_hash = sha256_file(frozen_path)
        actual_bytes = frozen_path.stat().st_size
        if actual_hash != row["sha256"] or actual_bytes != int(row["bytes"]):
            raise RuntimeError(f"frozen hash/size mismatch for {frozen_path}")
        source_path = Path(row["source_workspace"]) / row["source_relpath"]
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        if sha256_file(source_path) != row["sha256"]:
            raise RuntimeError(f"source no longer matches frozen hash for {source_path}")

    target_rows = json.loads(targets_path.read_text())
    counts = Counter(row["module"] for row in target_rows)
    if sum(counts.values()) == sum(int(config["generated_count"]) for config in MODULES.values()):
        expected = {module: int(config["generated_count"]) for module, config in MODULES.items()}
        allowed_catalog_statuses = {GENERATED_STATUS}
    else:
        expected = {"slice": 132, "vec": 48}
        allowed_catalog_statuses = {GENERATED_STATUS, EXISTING_VSTD_STATUS}
    if dict(counts) != expected:
        raise RuntimeError(f"target count mismatch: expected {expected}, got {dict(counts)}")
    if any(row.get("catalog_status") not in allowed_catalog_statuses for row in target_rows):
        raise RuntimeError("unexpected catalog_status found in target inventory")
    for row in target_rows:
        abcd = row.get("abcd_status", "")
        proof_status = str(row.get("proof_status", "")).split(":", 1)[0]
        if abcd:
            if abcd not in {"A", "B", "C", "D"}:
                raise RuntimeError(f"{row['target']}: invalid A/B/C/D status {abcd!r}")
        elif proof_status != "pending_implementation_proof":
            raise RuntimeError(f"{row['target']}: unexpected pending proof_status {proof_status!r}")

    source_refs = {
        row.get("rust_source_reference", "")
        for row in file_rows
        if row.get("category") == "rust-1.96-source-body" and row.get("rust_source_reference")
    }
    target_ref_paths = {
        row["source_reference"].split(":", 1)[0]
        for row in target_rows
        if row.get("source_reference")
    }
    missing = sorted(target_ref_paths - source_refs)
    if missing:
        raise RuntimeError(f"target source references not frozen: {missing}")

    dependency_status()
    print(
        "freeze ok: "
        f"{len(file_rows)} files, "
        f"{sum(counts.values())} targets, "
        f"module_counts={dict(sorted(counts.items()))}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="replace generated freeze artifacts inside this workspace")
    parser.add_argument("--check", action="store_true", help="validate an existing freeze instead of creating one")
    args = parser.parse_args()

    if args.check:
        check_freeze()
    else:
        write_freeze(refresh=args.refresh)
        check_freeze()


if __name__ == "__main__":
    main()
