#!/usr/bin/env python3
"""Reusable evidence capture and crosswalk updates for target obligations."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Any

import campaign_common as common


RESULT_FIELDS = (
    "exact_output_determinism_status",
    "completeness_modulo_reviewed_equivalence_status",
)


def _row_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("target", "")), str(row.get("input_order", ""))


def apply_crosswalk_result_update(
    csv_rows: list[dict[str, Any]],
    json_rows: list[dict[str, Any]],
    *,
    target: str,
    input_order: str,
    statuses: dict[str, str],
    preserved_results: dict[tuple[str, str], dict[str, str]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return a fail-closed result-only update for one target."""
    if set(statuses) != set(RESULT_FIELDS):
        raise ValueError("target result update must set exactly both result fields")
    preserved = preserved_results or {}
    for key, values in preserved.items():
        if set(values) != set(RESULT_FIELDS):
            raise ValueError(f"{key}: preserved result must set both result fields")

    if len(csv_rows) != 62 or len(json_rows) != 62:
        raise ValueError("crosswalk must contain exactly 62 rows in both formats")
    csv_by_key = {_row_key(row): row for row in csv_rows}
    json_by_key = {_row_key(row): row for row in json_rows}
    if len(csv_by_key) != 62 or set(csv_by_key) != set(json_by_key):
        raise ValueError("crosswalk formats have duplicate or mismatched row identities")
    for key in csv_by_key:
        if csv_by_key[key] != json_by_key[key]:
            raise ValueError(f"{key}: CSV and JSON crosswalk rows differ before update")

    selected_key = (target, input_order)
    if selected_key not in csv_by_key:
        raise ValueError(f"crosswalk does not contain exactly one {target} row")
    if selected_key in preserved:
        raise ValueError("target row cannot also be a preserved row")

    for key, values in preserved.items():
        if key not in csv_by_key:
            raise ValueError(f"{key}: preserved result row is missing")
        actual = {
            field: str(csv_by_key[key].get(field, ""))
            for field in RESULT_FIELDS
        }
        if actual != values:
            raise ValueError(f"{key}: preserved result fields changed")

    for key, row in csv_by_key.items():
        actual = {field: str(row.get(field, "")) for field in RESULT_FIELDS}
        if key == selected_key:
            allowed = (
                {field: "not-run" for field in RESULT_FIELDS},
                statuses,
            )
            if actual not in allowed:
                raise ValueError(f"{target}: target result fields have unexpected state")
        elif key in preserved:
            continue
        elif actual != {field: "not-run" for field in RESULT_FIELDS}:
            raise ValueError(f"{key}: refusing to alter an out-of-scope result")

    updated_csv = [dict(row) for row in csv_rows]
    updated_json = [dict(row) for row in json_rows]
    for rows in (updated_csv, updated_json):
        match = next(row for row in rows if _row_key(row) == selected_key)
        match.update(statuses)

    for before, after in zip(csv_rows, updated_csv):
        changed = {
            key for key in set(before) | set(after) if before.get(key) != after.get(key)
        }
        if _row_key(before) == selected_key:
            if not changed <= set(RESULT_FIELDS):
                raise ValueError("target update changed non-result crosswalk fields")
        elif changed:
            raise ValueError(f"{_row_key(before)}: non-target row was mutated")
    if updated_csv != updated_json:
        raise ValueError("crosswalk formats diverged after result update")
    return updated_csv, updated_json


def capture_command(
    evidence_dir: Path,
    argv: list[str],
    *,
    cwd: Path,
    timeout: int = 110,
) -> dict[str, Any]:
    evidence_dir.mkdir(parents=True, exist_ok=True)
    command_path = evidence_dir / "command.txt"
    stdout_path = evidence_dir / "stdout.txt"
    stderr_path = evidence_dir / "stderr.txt"
    status_path = evidence_dir / "status.txt"
    command_path.write_text(shlex.join(argv) + "\n")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        process = subprocess.run(
            argv,
            cwd=cwd,
            env=environment,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        stdout = process.stdout
        stderr = process.stderr
        return_code = process.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = (exc.stderr or "") + "\ncommand timed out\n"
        return_code = 124
    stdout_path.write_text(stdout)
    stderr_path.write_text(stderr)
    status_path.write_text(f"{return_code}\n")
    return {
        "argv": argv,
        "command": common.relpath(command_path),
        "stdout": common.relpath(stdout_path),
        "stderr": common.relpath(stderr_path),
        "status": common.relpath(status_path),
        "exit_code": return_code,
    }


def first_output_line(record: dict[str, Any]) -> str:
    lines = (common.OUT / record["stdout"]).read_text().splitlines()
    return lines[0] if lines else ""


def require_clean_result(
    record: dict[str, Any],
    expected_first_line: str,
    *,
    label: str,
) -> None:
    stderr = (common.OUT / record["stderr"]).read_text()
    result = first_output_line(record)
    if record["exit_code"] != 0:
        raise RuntimeError(f"{label}: command exited {record['exit_code']}")
    if stderr:
        raise RuntimeError(f"{label}: command emitted stderr: {stderr.strip()}")
    if result != expected_first_line:
        raise RuntimeError(
            f"{label}: expected {expected_first_line}, received {result or '<empty>'}"
        )


def artifact_record(path: Path) -> dict[str, Any]:
    return {
        "path": common.relpath(path),
        "sha256": common.sha256(path),
        "bytes": path.stat().st_size,
    }


def update_crosswalk_result(
    *,
    target: str,
    input_order: str,
    statuses: dict[str, str],
    preserved_results: dict[tuple[str, str], dict[str, str]] | None = None,
) -> None:
    json_path = common.OUT / "crosswalk/target_to_proof_boundary.json"
    csv_path = common.OUT / "crosswalk/target_to_proof_boundary.csv"
    csv_rows = common.read_csv(csv_path)
    with json_path.open() as handle:
        json_rows = json.load(handle)
    updated_csv, updated_json = apply_crosswalk_result_update(
        csv_rows,
        json_rows,
        target=target,
        input_order=input_order,
        statuses=statuses,
        preserved_results=preserved_results,
    )
    common.write_csv(csv_path, updated_csv, list(updated_csv[0]))
    common.write_json(json_path, updated_json)
