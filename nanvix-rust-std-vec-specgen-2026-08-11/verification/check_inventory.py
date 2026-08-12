#!/usr/bin/env python3
"""Validate the isolated alloc::vec inventory/provenance bootstrap."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

EXPECTED_EXISTING_VSTD = {
    "alloc::vec::Vec::append",
    "alloc::vec::Vec::as_mut_slice",
    "alloc::vec::Vec::as_slice",
    "alloc::vec::Vec::capacity",
    "alloc::vec::Vec::clear",
    "alloc::vec::Vec::extend_from_slice",
    "alloc::vec::Vec::insert",
    "alloc::vec::Vec::is_empty",
    "alloc::vec::Vec::len",
    "alloc::vec::Vec::new",
    "alloc::vec::Vec::pop",
    "alloc::vec::Vec::push",
    "alloc::vec::Vec::remove",
    "alloc::vec::Vec::reserve",
    "alloc::vec::Vec::reserve_exact",
    "alloc::vec::Vec::resize",
    "alloc::vec::Vec::shrink_to",
    "alloc::vec::Vec::shrink_to_fit",
    "alloc::vec::Vec::split_off",
    "alloc::vec::Vec::swap_remove",
    "alloc::vec::Vec::truncate",
    "alloc::vec::Vec::try_reserve",
    "alloc::vec::Vec::try_reserve_exact",
    "alloc::vec::Vec::with_capacity",
}

REQUIRED_INVENTORY_COLUMNS = {
    "canonical_target",
    "display_path",
    "source_location",
    "copied_source_path",
    "kind",
    "signature",
    "generic_bounds",
    "safety",
    "stability",
    "existing_vstd_status",
    "existing_vstd_provenance",
    "existing_vstd_exact_match_status",
    "planned_spec_status",
    "semantic_family",
    "source_observable_inputs",
    "source_observable_outputs",
    "source_observable_mutations",
    "required_shared_model_helper",
    "decisive_validation_command",
    "final_contract_or_justified_no_spec_status",
}


def fail(message: str) -> None:
    print(f"inventory check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modules-csv", required=True, type=Path)
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--expect-total", required=True, type=int)
    parser.add_argument("--expect-existing-vstd", required=True, type=int)
    parser.add_argument("--expect-unstable", required=True, type=int)
    args = parser.parse_args()

    root = args.inventory.resolve().parents[1]
    if root.is_symlink():
        fail(f"workspace root is a symlink: {root}")

    modules = read_csv(args.modules_csv)
    module_row = next((r for r in modules if r.get("module") == "alloc::vec"), None)
    if module_row is None:
        fail("alloc::vec row is missing from modules.csv")
    stable_unique = int(module_row["stable_unique_api_paths"])
    covered_stable = int(module_row["covered_stable_unique_api_paths"])
    uncovered_stable = int(module_row["uncovered_stable_unique_api_paths"])
    unstable_decls = int(module_row["unstable_declarations"])
    if stable_unique != args.expect_total:
        fail(f"modules.csv stable count {stable_unique}, expected {args.expect_total}")
    if covered_stable != args.expect_existing_vstd:
        fail(f"modules.csv covered stable count {covered_stable}, expected {args.expect_existing_vstd}")
    if uncovered_stable != args.expect_total - args.expect_existing_vstd:
        fail(f"modules.csv uncovered stable count {uncovered_stable}")
    if unstable_decls != args.expect_unstable:
        fail(f"modules.csv unstable count {unstable_decls}, expected {args.expect_unstable}")

    coverage_path = args.modules_csv.parent / "coverage.csv"
    coverage = read_csv(coverage_path)
    stable_rows = [r for r in coverage if r.get("module") == "alloc::vec" and r.get("stability") == "stable"]
    unstable_rows = [r for r in coverage if r.get("module") == "alloc::vec" and r.get("stability") != "stable"]
    covered_targets = {r["canonical_path"] for r in stable_rows if r.get("covered") == "True"}
    if len(stable_rows) != args.expect_total:
        fail(f"coverage.csv stable row count {len(stable_rows)}, expected {args.expect_total}")
    if len(unstable_rows) != args.expect_unstable:
        fail(f"coverage.csv unstable row count {len(unstable_rows)}, expected {args.expect_unstable}")
    if covered_targets != EXPECTED_EXISTING_VSTD:
        fail(
            "covered stable target set mismatch: "
            f"missing={sorted(EXPECTED_EXISTING_VSTD - covered_targets)} "
            f"extra={sorted(covered_targets - EXPECTED_EXISTING_VSTD)}"
        )

    inventory = read_csv(args.inventory)
    if len(inventory) != args.expect_total:
        fail(f"inventory has {len(inventory)} rows, expected {args.expect_total}")
    missing_columns = REQUIRED_INVENTORY_COLUMNS.difference(inventory[0].keys())
    if missing_columns:
        fail(f"inventory missing columns: {sorted(missing_columns)}")
    targets = [r["canonical_target"] for r in inventory]
    if len(targets) != len(set(targets)):
        fail("inventory contains duplicate canonical targets")
    if set(targets) != {r["canonical_path"] for r in stable_rows}:
        fail("inventory target set differs from stable coverage set")
    for row in inventory:
        target = row["canonical_target"]
        if row["stability"] != "stable":
            fail(f"{target} is not marked stable")
        if row.get("has_approximate_alias") == "True":
            fail(f"{target} is marked approximate alias")
        for column in REQUIRED_INVENTORY_COLUMNS:
            if not row.get(column, "").strip():
                fail(f"{target} has empty required column {column}")
        copied = root / row["copied_source_path"]
        if not copied.exists() or copied.is_symlink():
            fail(f"{target} copied source missing or symlink: {copied}")

    existing = {r["canonical_target"] for r in inventory if r["existing_vstd_status"] == "existing-vstd"}
    if existing != EXPECTED_EXISTING_VSTD:
        fail(
            "inventory existing-vstd target set mismatch: "
            f"missing={sorted(EXPECTED_EXISTING_VSTD - existing)} "
            f"extra={sorted(existing - EXPECTED_EXISTING_VSTD)}"
        )
    exact = {r["canonical_target"] for r in inventory if r["existing_vstd_exact_match_status"] == "exact-existing-vstd"}
    if exact != EXPECTED_EXISTING_VSTD:
        fail("inventory exact-vstd set does not match expected covered set")

    audit_path = root / "inventory/vec_existing_vstd_exact_match_audit.csv"
    audit = read_csv(audit_path)
    if len(audit) != args.expect_existing_vstd:
        fail(f"vstd exact audit has {len(audit)} rows, expected {args.expect_existing_vstd}")
    audit_targets = {r["canonical_target"] for r in audit}
    if audit_targets != EXPECTED_EXISTING_VSTD:
        fail("vstd exact audit target set mismatch")
    for row in audit:
        if row.get("exact_match_status") != "exact-existing-vstd":
            fail(f"{row['canonical_target']} audit status is {row.get('exact_match_status')}")
        for column in ["target_binding_status", "receiver_shape_status", "parameter_shape_status", "return_shape_status", "generic_bounds_status"]:
            if row.get(column) != "ok":
                fail(f"{row['canonical_target']} audit column {column} is {row.get(column)}")
        vstd_path = root / row["vstd_copied_path"]
        if not vstd_path.exists() or "assume_specification" not in row.get("vstd_declaration", ""):
            fail(f"{row['canonical_target']} has invalid vstd declaration provenance")

    unstable_path = root / "inventory/vec_unstable_exclusions.csv"
    unstable = read_csv(unstable_path)
    if len(unstable) != args.expect_unstable:
        fail(f"unstable exclusions have {len(unstable)} rows, expected {args.expect_unstable}")
    if {r["canonical_target"] for r in unstable} != {r["canonical_path"] for r in unstable_rows}:
        fail("unstable exclusions target set mismatch")

    json_path = args.inventory.with_suffix(".json")
    md_path = args.inventory.with_name("VEC_EXEC_FN_INVENTORY.md")
    for path in [json_path, md_path, root / "inventory/vec_existing_vstd_exact_match_audit.json", root / "inventory/vec_unstable_exclusions.json"]:
        if not path.exists():
            fail(f"required inventory artifact missing: {path}")
    payload = json.loads(json_path.read_text())
    summary = payload.get("summary", {})
    if summary.get("total_stable_unique_exec_apis") != args.expect_total:
        fail("JSON summary total mismatch")
    if summary.get("existing_vstd_specs") != args.expect_existing_vstd:
        fail("JSON summary existing-vstd mismatch")
    if summary.get("excluded_unstable_exec_apis") != args.expect_unstable:
        fail("JSON summary unstable mismatch")

    manifest_path = root / "provenance/source_manifest.csv"
    manifest_json_path = root / "provenance/source_manifest.json"
    manifest = read_csv(manifest_path)
    if not manifest:
        fail("source manifest is empty")
    components = {r["component"] for r in manifest}
    required_components = {"rust-alloc-vec", "rust-alloc-adjacent", "vstd-baseline", "survey-results"}
    if not required_components.issubset(components):
        fail(f"source manifest components missing: {sorted(required_components - components)}")
    vec_files = [r for r in manifest if r["component"] == "rust-alloc-vec"]
    if len(vec_files) != 16:
        fail(f"rust-alloc-vec manifest has {len(vec_files)} files, expected complete 16-file vec source copy")
    for row in manifest:
        dest = root / row["dest_path"]
        if not dest.exists() or dest.is_symlink():
            fail(f"manifest destination missing or symlink: {dest}")
        if sha256(dest) != row["sha256"]:
            fail(f"manifest hash mismatch for {dest}")
    manifest_payload = json.loads(manifest_json_path.read_text())
    if len(manifest_payload.get("files", [])) != len(manifest):
        fail("manifest JSON file count mismatch")

    print(
        "inventory ok: "
        f"{args.expect_total} stable unique alloc::vec APIs, "
        f"{args.expect_existing_vstd} exact existing-vstd, "
        f"{args.expect_total - args.expect_existing_vstd} uncovered, "
        f"{args.expect_unstable} unstable excluded; provenance hashes verified"
    )


if __name__ == "__main__":
    main()
