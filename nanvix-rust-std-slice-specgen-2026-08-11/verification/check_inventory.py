#!/usr/bin/env python3
"""Validate the core::slice inventory gate artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys


EXPECTED_EXISTING_VSTD = {
    "core::slice::copy_from_slice",
    "core::slice::copy_within",
    "core::slice::first",
    "core::slice::first_mut",
    "core::slice::get",
    "core::slice::is_empty",
    "core::slice::iter",
    "core::slice::last",
    "core::slice::last_mut",
    "core::slice::len",
    "core::slice::split_at",
    "core::slice::split_at_mut",
}

REQUIRED_COLUMNS = {
    "canonical_target",
    "display_path",
    "source_location",
    "kind",
    "signature",
    "generic_bounds",
    "safety",
    "stability",
    "existing_vstd_status",
    "existing_vstd_provenance",
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modules-csv", required=True, type=Path)
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--expect-total", required=True, type=int)
    parser.add_argument("--expect-existing-vstd", required=True, type=int)
    args = parser.parse_args()

    module_rows = read_csv(args.modules_csv)
    module_row = next((r for r in module_rows if r.get("module") == "core::slice"), None)
    if module_row is None:
        fail("core::slice row is missing from modules.csv")

    stable_unique = int(module_row["stable_unique_api_paths"])
    covered_stable = int(module_row["covered_stable_unique_api_paths"])
    uncovered_stable = int(module_row["uncovered_stable_unique_api_paths"])
    if stable_unique != args.expect_total:
        fail(f"modules.csv reports {stable_unique} stable unique paths, expected {args.expect_total}")
    if covered_stable != args.expect_existing_vstd:
        fail(
            f"modules.csv reports {covered_stable} covered stable unique paths, "
            f"expected {args.expect_existing_vstd}"
        )
    if uncovered_stable != args.expect_total - args.expect_existing_vstd:
        fail(f"modules.csv reports {uncovered_stable} uncovered stable paths")

    rows = read_csv(args.inventory)
    if not rows:
        fail("inventory is empty")
    missing_columns = REQUIRED_COLUMNS.difference(rows[0].keys())
    if missing_columns:
        fail(f"inventory missing columns: {sorted(missing_columns)}")
    if len(rows) != args.expect_total:
        fail(f"inventory has {len(rows)} rows, expected {args.expect_total}")

    targets = [r["canonical_target"] for r in rows]
    if len(set(targets)) != len(targets):
        duplicates = sorted({t for t in targets if targets.count(t) > 1})
        fail(f"duplicate canonical targets: {duplicates}")

    existing = {r["canonical_target"] for r in rows if r["existing_vstd_status"] == "existing-vstd"}
    if len(existing) != args.expect_existing_vstd:
        fail(f"inventory flags {len(existing)} existing-vstd rows, expected {args.expect_existing_vstd}")
    if existing != EXPECTED_EXISTING_VSTD:
        fail(
            "existing-vstd target set mismatch: "
            f"missing={sorted(EXPECTED_EXISTING_VSTD - existing)} "
            f"extra={sorted(existing - EXPECTED_EXISTING_VSTD)}"
        )

    for row in rows:
        target = row["canonical_target"]
        if row["stability"] != "stable":
            fail(f"{target} is not marked stable")
        if row.get("has_approximate_alias", "False") == "True":
            fail(f"{target} is marked as an approximate alias")
        for column in REQUIRED_COLUMNS:
            if not row.get(column, "").strip():
                fail(f"{target} has empty required column {column}")

    coverage_path = args.modules_csv.parent / "coverage.csv"
    if coverage_path.exists():
        coverage = read_csv(coverage_path)
        expected_rows = [
            r
            for r in coverage
            if r.get("module") == "core::slice" and r.get("stability") == "stable"
        ]
        expected_targets = {r["canonical_path"] for r in expected_rows}
        if len(expected_targets) != args.expect_total:
            fail(f"coverage.csv stable core::slice target count is {len(expected_targets)}")
        inventory_targets = set(targets)
        if inventory_targets != expected_targets:
            fail(
                "inventory target set differs from stable coverage set: "
                f"missing={sorted(expected_targets - inventory_targets)} "
                f"extra={sorted(inventory_targets - expected_targets)}"
            )
        unstable_targets = {
            r["canonical_path"]
            for r in coverage
            if r.get("module") == "core::slice" and r.get("stability") != "stable"
        }
        overlap = inventory_targets.intersection(unstable_targets)
        if overlap:
            fail(f"unstable targets were counted: {sorted(overlap)}")
        covered_targets = {
            r["canonical_path"]
            for r in expected_rows
            if r.get("covered") == "True"
        }
        if covered_targets != EXPECTED_EXISTING_VSTD:
            fail(
                "coverage.csv covered stable target set mismatch: "
                f"missing={sorted(EXPECTED_EXISTING_VSTD - covered_targets)} "
                f"extra={sorted(covered_targets - EXPECTED_EXISTING_VSTD)}"
            )

    json_path = args.inventory.with_suffix(".json")
    md_path = args.inventory.with_name("SLICE_EXEC_FN_INVENTORY.md")
    if not json_path.exists():
        fail(f"matching JSON inventory is missing: {json_path}")
    if not md_path.exists():
        fail(f"human-readable inventory is missing: {md_path}")

    with json_path.open() as f:
        payload = json.load(f)
    json_rows = payload.get("rows", [])
    json_targets = {r.get("canonical_target") for r in json_rows}
    if len(json_rows) != len(rows) or json_targets != set(targets):
        fail("JSON inventory rows do not match CSV inventory")
    summary = payload.get("summary", {})
    if summary.get("total_stable_unique_exec_apis") != args.expect_total:
        fail("JSON summary total does not match expected total")
    if summary.get("existing_vstd_specs") != args.expect_existing_vstd:
        fail("JSON summary existing-vstd count does not match expected count")

    print(
        "inventory ok: "
        f"{args.expect_total} stable unique core::slice exec APIs, "
        f"{args.expect_existing_vstd} existing-vstd, "
        f"{args.expect_total - args.expect_existing_vstd} pending"
    )


if __name__ == "__main__":
    main()
