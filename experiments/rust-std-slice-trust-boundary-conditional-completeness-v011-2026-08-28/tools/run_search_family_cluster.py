#!/usr/bin/env python3
"""Replay targets 028, 030, and 065 from the delivered crosswalk state."""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import run_target_028
import run_target_030
import run_target_065
import search_target_pipeline
import target_028
import target_030
import target_065
import target_pipeline


ORDERED_TARGETS = (
    (target_028, run_target_028),
    (target_030, run_target_030),
    (target_065, run_target_065),
)
CLUSTER_KEYS = tuple(
    (module.TARGET, module.INPUT_ORDER) for module, _ in ORDERED_TARGETS
)
NOT_RUN = {
    field: "not-run" for field in search_target_pipeline.INCOMPLETE
}


def _row_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("target", "")), str(row.get("input_order", ""))


def prepare_crosswalk_reset(
    csv_rows: list[dict[str, Any]],
    json_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if len(csv_rows) != 62 or len(json_rows) != 62:
        raise ValueError("crosswalk must contain exactly 62 rows in both formats")
    csv_by_key = {_row_key(row): row for row in csv_rows}
    json_by_key = {_row_key(row): row for row in json_rows}
    if (
        len(csv_by_key) != 62
        or set(csv_by_key) != set(json_by_key)
        or any(csv_by_key[key] != json_by_key[key] for key in csv_by_key)
    ):
        raise ValueError("crosswalk formats are duplicate, mismatched, or divergent")

    cluster_keys = set(CLUSTER_KEYS)
    for key, row in csv_by_key.items():
        actual = {
            field: str(row.get(field, ""))
            for field in search_target_pipeline.INCOMPLETE
        }
        if key in search_target_pipeline.BASELINE_RESULTS:
            if actual != search_target_pipeline.BASELINE_RESULTS[key]:
                raise ValueError(f"{key}: certified baseline result changed")
        elif key in cluster_keys:
            if actual != search_target_pipeline.INCOMPLETE:
                raise ValueError(f"{key}: delivered search result changed")
        elif actual != NOT_RUN:
            raise ValueError(f"{key}: out-of-scope result is classified")

    updated_csv = copy.deepcopy(csv_rows)
    updated_json = copy.deepcopy(json_rows)
    for rows in (updated_csv, updated_json):
        by_key = {_row_key(row): row for row in rows}
        for key in CLUSTER_KEYS:
            by_key[key].update(NOT_RUN)
    for before, after in zip(csv_rows, updated_csv):
        changed = {
            field
            for field in set(before) | set(after)
            if before.get(field) != after.get(field)
        }
        if changed - set(search_target_pipeline.INCOMPLETE):
            raise ValueError(f"{_row_key(before)}: reset changed a non-result field")
        if _row_key(before) not in cluster_keys and changed:
            raise ValueError(f"{_row_key(before)}: reset changed a non-cluster row")
    if updated_csv != updated_json:
        raise ValueError("crosswalk formats diverged during cluster reset")
    return updated_csv, updated_json


def _load_crosswalks() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    csv_path = common.OUT / "crosswalk/target_to_proof_boundary.csv"
    json_path = common.OUT / "crosswalk/target_to_proof_boundary.json"
    return common.read_csv(csv_path), json.loads(json_path.read_text())


def _cluster_results(rows: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    by_key = {_row_key(row): row for row in rows}
    return {
        module.ARTIFACT_ID: {
            field: str(by_key[(module.TARGET, module.INPUT_ORDER)][field])
            for field in search_target_pipeline.INCOMPLETE
        }
        for module, _ in ORDERED_TARGETS
    }


def main() -> None:
    csv_path = common.OUT / "crosswalk/target_to_proof_boundary.csv"
    json_path = common.OUT / "crosswalk/target_to_proof_boundary.json"
    before_csv, before_json = _load_crosswalks()
    reset_csv, reset_json = prepare_crosswalk_reset(before_csv, before_json)
    preserved_before = {
        artifact_id: search_target_pipeline.tree_digest(
            common.OUT / "evidence/targets" / artifact_id
        )
        for artifact_id in search_target_pipeline.BASELINE_ARTIFACT_IDS
    }
    cluster_roots = {
        module.ARTIFACT_ID: common.OUT / "evidence/targets" / module.ARTIFACT_ID
        for module, _ in ORDERED_TARGETS
    }
    (common.OUT / "logs").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".search-family-cluster-backup-",
        dir=common.OUT / "logs",
    ) as backup_directory:
        backup_root = Path(backup_directory)
        for artifact_id, root in cluster_roots.items():
            if not root.is_dir():
                raise ValueError(f"delivered target evidence is missing: {artifact_id}")
            shutil.copytree(root, backup_root / artifact_id)
        try:
            common.write_csv(csv_path, reset_csv, list(reset_csv[0]))
            common.write_json(json_path, reset_json)
            for module, runner in ORDERED_TARGETS:
                print(f"ordered_cluster_start={module.INPUT_ORDER}")
                runner.main()
            after_csv, after_json = _load_crosswalks()
            expected = copy.deepcopy(before_csv)
            by_key = {_row_key(row): row for row in expected}
            for key in CLUSTER_KEYS:
                by_key[key].update(search_target_pipeline.INCOMPLETE)
            if after_csv != expected or after_json != expected:
                raise RuntimeError(
                    "ordered search replay changed unexpected crosswalk cells"
                )
            preserved_after = {
                artifact_id: search_target_pipeline.tree_digest(
                    common.OUT / "evidence/targets" / artifact_id
                )
                for artifact_id in search_target_pipeline.BASELINE_ARTIFACT_IDS
            }
            if preserved_after != preserved_before:
                raise RuntimeError(
                    "ordered search replay mutated certified baseline evidence"
                )
        except BaseException:
            common.write_csv(csv_path, before_csv, list(before_csv[0]))
            common.write_json(json_path, before_json)
            for artifact_id, root in cluster_roots.items():
                if root.exists():
                    shutil.rmtree(root)
                shutil.copytree(backup_root / artifact_id, root)
            raise

    common.write_json(
        common.OUT / "logs/ordered_search_family_replay.json",
        {
            "schema_version": 1,
            "status": "passed",
            "ordered_artifact_ids": [
                module.ARTIFACT_ID for module, _ in ORDERED_TARGETS
            ],
            "initial_cluster_results": _cluster_results(before_csv),
            "final_cluster_results": _cluster_results(after_csv),
            "crosswalk": {
                "csv": target_pipeline.artifact_record(csv_path),
                "json": target_pipeline.artifact_record(json_path),
            },
            "preserved_certified_evidence": {
                artifact_id: {
                    "before_sha256": preserved_before[artifact_id],
                    "after_sha256": preserved_after[artifact_id],
                }
                for artifact_id in search_target_pipeline.BASELINE_ARTIFACT_IDS
            },
        },
    )
    print("ordered_search_family=PASS")
    print("order=028,030,065")
    print("classified=14 not_run=48")


if __name__ == "__main__":
    main()
