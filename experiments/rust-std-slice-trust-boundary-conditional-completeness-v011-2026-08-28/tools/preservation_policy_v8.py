#!/usr/bin/env python3
"""Fail-closed target-082 preservation successor from accepted v7."""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import preservation_policy_v3 as predecessor


OUT = common.OUT
POLICY_PATH = OUT / "preservation/path_policy_v8.json"
PARENT_POLICY_PATH = OUT / "preservation/path_policy_v7.json"
V6_PATH = OUT / "preservation/path_policy_v6.json"
V5_PATH = OUT / "preservation/path_policy_v5.json"
V9_PATH = OUT / "preservation/path_policy_v9.json"
REVIEW_PATH = (
    OUT / "review/REVIEW_ADDENDUM_TARGET_082_OPERATIONAL_V1.md"
)
ADDENDUM_JSON = (
    OUT / "crosswalk/target_082_operational_v1_addendum.json"
)
ADDENDUM_CSV = (
    OUT / "crosswalk/target_082_operational_v1_addendum.csv"
)

POLICY_ID = "slice-preservation-path-policy-v8"
PARENT_POLICY_ID = "slice-preservation-path-policy-v7"
TARGET_082_ADDITION = "target_082_operational_v1"
TARGET_082_TARGET = "core::slice::sort_unstable_by_key"
TARGET_082_REVIEW_ADDITION = "target_082_operational_v1_review"
V9_POLICY_ID = "slice-preservation-path-policy-v9"
ARCHIVE_ROOT = PurePosixPath("preservation/archive_v2")
FINAL_CAMPAIGN_BASELINE = (
    OUT / "evidence/final_campaign/preservation_baseline.json"
)
ARCHIVE_MAPPINGS = {
    (
        ".autors/"
        "rust-std-slice-trust-boundary-conditional-completeness-v011-"
        "2026-08-28/wiki/INDEX.md"
    ): (
        "target-081-v6-wiki-index@accepted-by-v7",
        ARCHIVE_ROOT / "wiki/INDEX.md",
    ),
    "tests/test_target_081_operational_artifacts_v1.py": (
        "target-081-v6-artifact-test@accepted-by-v7",
        ARCHIVE_ROOT
        / "tests/test_target_081_operational_artifacts_v1.py",
    ),
    "tools/preservation_policy_v3.py": (
        "target-081-v6-preservation-validator@accepted-by-v7",
        ARCHIVE_ROOT / "tools/preservation_policy_v3.py",
    ),
    "tools/run_target_081_operational_v1.py": (
        "target-081-v6-producer@accepted-by-v7",
        ARCHIVE_ROOT / "tools/run_target_081_operational_v1.py",
    ),
}
HISTORICAL_ARCHIVE_MAPPINGS = {
    "evidence/tool_versions/argus/command.txt": (
        "authority-argus-command@certified-final-campaign",
        ARCHIVE_ROOT / "evidence/tool_versions/argus/command.txt",
    ),
    "evidence/tool_versions/argus/record.json": (
        "authority-argus-record@certified-final-campaign",
        ARCHIVE_ROOT / "evidence/tool_versions/argus/record.json",
    ),
    "evidence/tool_versions/argus/status.txt": (
        "authority-argus-status@certified-final-campaign",
        ARCHIVE_ROOT / "evidence/tool_versions/argus/status.txt",
    ),
    "evidence/tool_versions/argus/stderr.txt": (
        "authority-argus-stderr@certified-final-campaign",
        ARCHIVE_ROOT / "evidence/tool_versions/argus/stderr.txt",
    ),
    "evidence/tool_versions/argus/stdout.txt": (
        "authority-argus-stdout@certified-final-campaign",
        ARCHIVE_ROOT / "evidence/tool_versions/argus/stdout.txt",
    ),
    "evidence/tool_versions/manifest.json": (
        "authority-tool-manifest@certified-final-campaign",
        ARCHIVE_ROOT / "evidence/tool_versions/manifest.json",
    ),
}

PreservationPolicyError = predecessor.PreservationPolicyError
base = predecessor.base


def _artifact(path: Path, *, root: Path = OUT) -> dict[str, Any]:
    if not path.is_file():
        raise PreservationPolicyError(f"missing preservation file: {path}")
    return {
        "path": path.relative_to(root).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": base._sha256(path),
    }


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise PreservationPolicyError(f"{label} is missing or invalid") from exc
    if not isinstance(payload, dict):
        raise PreservationPolicyError(f"{label} is not an object")
    return payload


def _canonical(path: str, label: str) -> PurePosixPath:
    if not isinstance(path, str):
        raise PreservationPolicyError(f"{label} path is not text")
    parsed = PurePosixPath(path)
    if (
        parsed.is_absolute()
        or not parsed.parts
        or any(part in {"", ".", ".."} for part in parsed.parts)
        or parsed.as_posix() != path
    ):
        raise PreservationPolicyError(f"{label} path is not canonical")
    return parsed


def _historical_records(*, root: Path) -> dict[str, dict[str, Any]]:
    baseline = _load_json(
        root / FINAL_CAMPAIGN_BASELINE.relative_to(OUT),
        "certified final-campaign preservation baseline",
    )
    groups = baseline.get("groups")
    records = (
        groups.get("preexisting_evidence")
        if isinstance(groups, dict)
        else None
    )
    if not isinstance(records, list):
        raise PreservationPolicyError(
            "certified final-campaign preexisting evidence is missing"
        )
    by_path = {
        record.get("path"): record
        for record in records
        if isinstance(record, dict)
    }
    if not set(HISTORICAL_ARCHIVE_MAPPINGS) <= set(by_path):
        raise PreservationPolicyError(
            "certified Argus authority records are incomplete"
        )
    return {
        path: copy.deepcopy(by_path[path])
        for path in HISTORICAL_ARCHIVE_MAPPINGS
    }


def materialize_historical_argus_archive(
    *, root: Path = OUT
) -> None:
    records = _historical_records(root=root)
    generated: dict[str, bytes] = {}
    for logical, (_, archive_rel) in HISTORICAL_ARCHIVE_MAPPINGS.items():
        archive = root / Path(*archive_rel.parts)
        record = records[logical]
        if (
            archive.is_file()
            and archive.stat().st_size == record["bytes"]
            and base._sha256(archive) == record["sha256"]
        ):
            continue
        live = root / Path(*PurePosixPath(logical).parts)
        if (
            live.is_file()
            and live.stat().st_size == record["bytes"]
            and base._sha256(live) == record["sha256"]
        ):
            archive.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(live, archive)
            continue
        if not generated:
            argus_python = (
                os.environ.get("ARGUS_SKILL_PYTHON") or "python3"
            )
            process = subprocess.run(
                [argus_python, "-m", "argus_skill", "--version"],
                cwd=root,
                capture_output=True,
                timeout=30,
                check=False,
            )
            if process.returncode != 0:
                raise PreservationPolicyError(
                    "noninteractive Argus archive capture failed"
                )
            generated = {
                "evidence/tool_versions/argus/stdout.txt": process.stdout,
                "evidence/tool_versions/argus/stderr.txt": process.stderr,
            }
        content = generated.get(logical)
        if content is None:
            raise PreservationPolicyError(
                f"cannot recover certified historical artifact: {logical}"
            )
        archive.parent.mkdir(parents=True, exist_ok=True)
        archive.write_bytes(content)
        if (
            archive.stat().st_size != record["bytes"]
            or base._sha256(archive) != record["sha256"]
        ):
            raise PreservationPolicyError(
                f"recovered historical artifact does not match: {logical}"
            )


def historical_mapping_records(
    *, root: Path = OUT
) -> list[dict[str, Any]]:
    records = _historical_records(root=root)
    mappings = []
    for logical, (version_id, archive_rel) in sorted(
        HISTORICAL_ARCHIVE_MAPPINGS.items()
    ):
        archive = root / Path(*archive_rel.parts)
        archive_record = _artifact(archive, root=root)
        logical_record = records[logical]
        if (
            archive_record["bytes"] != logical_record["bytes"]
            or archive_record["sha256"] != logical_record["sha256"]
        ):
            raise PreservationPolicyError(
                f"historical archive does not preserve {logical}"
            )
        mappings.append(
            {
                "version_id": version_id,
                "logical_record": logical_record,
                "archive_record": archive_record,
                "source": (
                    "project-local-archive:certified-final-campaign/"
                    f"{logical}"
                ),
            }
        )
    return mappings


def _validate_record(
    record: dict[str, Any],
    path: Path,
    label: str,
) -> None:
    if not isinstance(record, dict) or set(record) != {
        "path",
        "bytes",
        "sha256",
    }:
        raise PreservationPolicyError(f"{label} record is malformed")
    _canonical(record["path"], label)
    if not path.is_file():
        raise PreservationPolicyError(f"{label} file is missing")
    if (
        isinstance(record["bytes"], bool)
        or not isinstance(record["bytes"], int)
        or record["bytes"] < 0
        or path.stat().st_size != record["bytes"]
        or base._sha256(path) != record["sha256"]
    ):
        raise PreservationPolicyError(f"{label} byte identity changed")


def _v8_payload(*, root: Path) -> dict[str, Any]:
    return _load_json(
        root / POLICY_PATH.relative_to(OUT), "target-082 path-policy-v8"
    )


def _mapping_index(
    payload: dict[str, Any],
    *,
    root: Path,
) -> tuple[dict[str, Path], list[dict[str, Any]]]:
    config = payload.get("archive_resolution")
    if (
        not isinstance(config, dict)
        or set(config)
        != {
            "schema_version",
            "archive_root",
            "record_version_mappings",
            "historical_record_version_mappings",
        }
        or config.get("schema_version") != 1
        or config.get("archive_root") != ARCHIVE_ROOT.as_posix()
    ):
        raise PreservationPolicyError(
            "target-082 archive configuration is invalid"
        )
    mappings = config["record_version_mappings"]
    if not isinstance(mappings, list):
        raise PreservationPolicyError(
            "target-082 archive mappings are not a list"
        )
    v6 = _load_json(
        root / V6_PATH.relative_to(OUT), "target-081 path-policy-v6"
    )
    records = v6.get("registered_post_v5_additions", {}).get(
        predecessor.TARGET_081_ADDITION, {}
    ).get("records")
    if not isinstance(records, list):
        raise PreservationPolicyError("target-081 v6 records are missing")
    by_path = {
        record.get("path"): record
        for record in records
        if isinstance(record, dict)
    }

    resolved: dict[str, Path] = {}
    version_ids: set[str] = set()
    archive_paths: set[str] = set()
    for index, mapping in enumerate(mappings):
        label = f"target-082 archive mapping[{index}]"
        if not isinstance(mapping, dict) or set(mapping) != {
            "version_id",
            "logical_record",
            "archive_record",
            "source",
        }:
            raise PreservationPolicyError(f"{label} is malformed")
        logical = mapping["logical_record"]
        if not isinstance(logical, dict):
            raise PreservationPolicyError(f"{label} logical record is invalid")
        logical_path = logical.get("path")
        expected = ARCHIVE_MAPPINGS.get(logical_path)
        archive_record = mapping["archive_record"]
        if (
            expected is None
            or mapping["version_id"] != expected[0]
            or mapping["version_id"] in version_ids
            or by_path.get(logical_path) != logical
            or not isinstance(mapping["source"], str)
            or not mapping["source"].startswith("project-local-archive:")
            or not isinstance(archive_record, dict)
            or archive_record.get("path") != expected[1].as_posix()
            or archive_record.get("path") in archive_paths
        ):
            raise PreservationPolicyError(f"{label} is invalid")
        archive_rel = _canonical(archive_record["path"], label)
        if not archive_rel.is_relative_to(ARCHIVE_ROOT):
            raise PreservationPolicyError(
                f"{label} escapes the target-082 archive root"
            )
        archive_path = root / Path(*archive_rel.parts)
        _validate_record(archive_record, archive_path, label)
        if (
            archive_record["bytes"] != logical["bytes"]
            or archive_record["sha256"] != logical["sha256"]
        ):
            raise PreservationPolicyError(
                f"{label} does not materialize its logical record"
            )
        resolved[logical_path] = archive_path.resolve()
        version_ids.add(mapping["version_id"])
        archive_paths.add(archive_record["path"])

    if set(resolved) != set(ARCHIVE_MAPPINGS):
        raise PreservationPolicyError(
            "target-082 archive mappings are incomplete"
        )
    return resolved, copy.deepcopy(mappings)


def _historical_mapping_index(
    payload: dict[str, Any],
    *,
    root: Path,
) -> tuple[dict[str, Path], list[dict[str, Any]]]:
    config = payload.get("archive_resolution")
    mappings = (
        config.get("historical_record_version_mappings")
        if isinstance(config, dict)
        else None
    )
    if not isinstance(mappings, list):
        raise PreservationPolicyError(
            "historical archive mappings are not a list"
        )
    records = _historical_records(root=root)
    resolved: dict[str, Path] = {}
    version_ids: set[str] = set()
    archive_paths: set[str] = set()
    for index, mapping in enumerate(mappings):
        label = f"historical authority archive mapping[{index}]"
        if not isinstance(mapping, dict) or set(mapping) != {
            "version_id",
            "logical_record",
            "archive_record",
            "source",
        }:
            raise PreservationPolicyError(f"{label} is malformed")
        logical = mapping["logical_record"]
        logical_path = (
            logical.get("path") if isinstance(logical, dict) else None
        )
        expected = HISTORICAL_ARCHIVE_MAPPINGS.get(logical_path)
        archive_record = mapping["archive_record"]
        if (
            expected is None
            or mapping["version_id"] != expected[0]
            or mapping["version_id"] in version_ids
            or records.get(logical_path) != logical
            or not isinstance(mapping["source"], str)
            or not mapping["source"].startswith(
                "project-local-archive:"
            )
            or not isinstance(archive_record, dict)
            or archive_record.get("path") != expected[1].as_posix()
            or archive_record.get("path") in archive_paths
        ):
            raise PreservationPolicyError(f"{label} is invalid")
        archive_rel = _canonical(archive_record["path"], label)
        if not archive_rel.is_relative_to(ARCHIVE_ROOT):
            raise PreservationPolicyError(
                f"{label} escapes the target-082 archive root"
            )
        archive_path = root / Path(*archive_rel.parts)
        _validate_record(archive_record, archive_path, label)
        if (
            archive_record["bytes"] != logical["bytes"]
            or archive_record["sha256"] != logical["sha256"]
        ):
            raise PreservationPolicyError(
                f"{label} does not materialize its logical record"
            )
        resolved[logical_path] = archive_path.resolve()
        version_ids.add(mapping["version_id"])
        archive_paths.add(archive_record["path"])
    if set(resolved) != set(HISTORICAL_ARCHIVE_MAPPINGS):
        raise PreservationPolicyError(
            "historical authority archive mappings are incomplete"
        )
    return resolved, copy.deepcopy(mappings)


def _validate_archive_membership(
    *,
    root: Path,
    mappings: tuple[list[dict[str, Any]], ...],
) -> None:
    expected = {
        mapping["archive_record"]["path"]
        for group in mappings
        for mapping in group
    }
    archive_root = root / Path(*ARCHIVE_ROOT.parts)
    actual = {
        path.relative_to(root).as_posix()
        for path in archive_root.rglob("*")
        if path.is_file()
    }
    if actual != expected:
        raise PreservationPolicyError(
            "target-082 archive has unmapped or missing content"
        )


def historical_identity_path(
    record: dict[str, Any],
    live_path: Path,
    *,
    root: Path,
) -> Path | None:
    try:
        logical = live_path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None
    if logical not in HISTORICAL_ARCHIVE_MAPPINGS:
        return None
    payload = _v8_payload(root=root)
    resolved, _ = _historical_mapping_index(payload, root=root)
    expected = _historical_records(root=root)[logical]
    return resolved[logical] if record == expected else None


def validate_target_081_v6(
    payload: dict[str, Any],
    v5_payload: dict[str, Any],
    *,
    root: Path,
) -> dict[str, Any]:
    """Validate v6 while resolving only v8-declared historical records."""

    v8 = _v8_payload(root=root)
    mapped, mappings = _mapping_index(v8, root=root)
    if (
        set(payload)
        != {
            "schema_version",
            "policy_id",
            "parent_policy_id",
            "parent_policy",
            "policy",
            "archive_resolution",
            "registered_post_v5_additions",
            "independent_review_lane",
        }
        or payload.get("schema_version") != 2
        or payload.get("policy_id")
        != predecessor.TARGET_081_POLICY_V6_ID
        or payload.get("parent_policy_id")
        != predecessor.TARGET_080_POLICY_V5_ID
    ):
        raise PreservationPolicyError("target-081 v6 identity is invalid")
    parent = payload["parent_policy"]
    expected_parent = _artifact(
        root / V5_PATH.relative_to(OUT), root=root
    )
    _validate_record(
        parent,
        root / Path(*_canonical(parent["path"], "v6 parent").parts),
        "target-081 v6 parent",
    )
    if parent != expected_parent:
        raise PreservationPolicyError(
            "target-081 v6 does not byte-bind path_policy_v5"
        )
    additions = payload["registered_post_v5_additions"]
    if not isinstance(additions, dict) or set(additions) != {
        predecessor.TARGET_081_ADDITION
    }:
        raise PreservationPolicyError("target-081 v6 addition set changed")
    config = additions[predecessor.TARGET_081_ADDITION]
    if not isinstance(config, dict) or set(config) != {
        "file_count",
        "records",
    }:
        raise PreservationPolicyError("target-081 v6 addition is malformed")
    records = config["records"]
    if (
        not isinstance(records, list)
        or isinstance(config["file_count"], bool)
        or config["file_count"] != len(records)
        or not records
    ):
        raise PreservationPolicyError("target-081 v6 count is invalid")
    resolutions: dict[str, str] = {}
    seen: set[str] = set()
    for index, record in enumerate(records):
        logical = _canonical(
            record.get("path"), f"target-081 v6 record[{index}]"
        ).as_posix()
        if logical in seen:
            raise PreservationPolicyError("target-081 v6 path is duplicated")
        seen.add(logical)
        path = mapped.get(logical, (root / logical).resolve())
        _validate_record(record, path, f"target-081 v6 record[{index}]")
        resolutions[logical] = str(path)

    archive = predecessor._validate_archive_resolution(
        payload, v5_payload, root=root
    )
    addendum_paths = {
        "json": predecessor.TARGET_081_ADDENDUM_JSON.relative_to(
            OUT
        ).as_posix(),
        "csv": predecessor.TARGET_081_ADDENDUM_CSV.relative_to(
            OUT
        ).as_posix(),
    }
    records_by_path = {record["path"]: record for record in records}
    if not set(addendum_paths.values()) <= set(records_by_path):
        raise PreservationPolicyError("target-081 v6 addenda are missing")
    lane = payload["independent_review_lane"]
    addendum = _load_json(
        root / addendum_paths["json"], "target-081 crosswalk addendum"
    )
    review = addendum.get("independent_review")
    if (
        lane
        != {
            "status": "pending",
            "expected_policy_id": predecessor.TARGET_081_POLICY_V7_ID,
            "expected_policy_path": "preservation/path_policy_v7.json",
            "expected_verdict_path": (
                "review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md"
            ),
        }
        or not isinstance(review, dict)
        or review.get("status") != "pending"
        or review.get("verdict") is not None
    ):
        raise PreservationPolicyError("target-081 v6 lifecycle changed")
    return {
        "registered_records": copy.deepcopy(records),
        "registered_record_resolutions": resolutions,
        "addenda": {
            name: copy.deepcopy(records_by_path[path])
            for name, path in addendum_paths.items()
        },
        "v8_record_version_mappings": mappings,
        **archive,
    }


def validate_policy(*, root: Path = OUT) -> dict[str, Any]:
    payload = _v8_payload(root=root)
    if (
        set(payload)
        != {
            "schema_version",
            "policy_id",
            "parent_policy_id",
            "parent_policy",
            "policy",
            "archive_resolution",
            "registered_post_v7_additions",
            "independent_review_lane",
        }
        or payload.get("schema_version") != 1
        or payload.get("policy_id") != POLICY_ID
        or payload.get("parent_policy_id") != PARENT_POLICY_ID
    ):
        raise PreservationPolicyError("target-082 v8 identity is invalid")
    parent = payload["parent_policy"]
    parent_path = root / PARENT_POLICY_PATH.relative_to(OUT)
    _validate_record(parent, parent_path, "target-082 v8 parent")
    if parent != _artifact(parent_path, root=root):
        raise PreservationPolicyError(
            "target-082 v8 does not byte-bind path_policy_v7"
        )

    v5 = _load_json(root / V5_PATH.relative_to(OUT), "path-policy-v5")
    v6_path = root / V6_PATH.relative_to(OUT)
    v6 = _load_json(v6_path, "path-policy-v6")
    validated_v6 = validate_target_081_v6(v6, v5, root=root)
    _, v6_mappings = _mapping_index(payload, root=root)
    historical_resolved, historical_mappings = (
        _historical_mapping_index(payload, root=root)
    )
    _validate_archive_membership(
        root=root,
        mappings=(v6_mappings, historical_mappings),
    )
    v6_record = _artifact(v6_path, root=root)
    v7 = _load_json(parent_path, "path-policy-v7")
    predecessor._validate_target_081_v7(
        v7, root=root, expected_parent=v6_record
    )

    additions = payload["registered_post_v7_additions"]
    if not isinstance(additions, dict) or set(additions) != {
        TARGET_082_ADDITION
    }:
        raise PreservationPolicyError("target-082 v8 addition set changed")
    config = additions[TARGET_082_ADDITION]
    if not isinstance(config, dict) or set(config) != {
        "file_count",
        "records",
    }:
        raise PreservationPolicyError("target-082 v8 addition is malformed")
    records = config["records"]
    if (
        not isinstance(records, list)
        or isinstance(config["file_count"], bool)
        or config["file_count"] != len(records)
        or not records
    ):
        raise PreservationPolicyError("target-082 v8 count is invalid")
    forbidden = {
        "preservation/path_policy_v8.json",
        "preservation/path_policy_v9.json",
        REVIEW_PATH.relative_to(OUT).as_posix(),
    }
    records_by_path: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        logical = _canonical(
            record.get("path"), f"target-082 v8 record[{index}]"
        ).as_posix()
        if logical in records_by_path or logical in forbidden:
            raise PreservationPolicyError(
                "target-082 v8 path is duplicate or reviewer-owned"
            )
        path = root / Path(*PurePosixPath(logical).parts)
        _validate_record(record, path, f"target-082 v8 record[{index}]")
        records_by_path[logical] = copy.deepcopy(record)
    required = {
        ADDENDUM_JSON.relative_to(OUT).as_posix(),
        ADDENDUM_CSV.relative_to(OUT).as_posix(),
        "evidence/target_082_operational_v1/result.json",
        "tools/target_082_operational_v1.py",
        "tools/run_target_082_operational_v1.py",
        "proofs/082_core_slice_sort_unstable_by_key_operational_v1.rs",
        *{
            archive.as_posix()
            for _, archive in ARCHIVE_MAPPINGS.values()
        },
    }
    if not required <= set(records_by_path):
        raise PreservationPolicyError(
            "target-082 v8 package registration is incomplete"
        )
    addendum = _load_json(ADDENDUM_JSON, "target-082 addendum")
    review = addendum.get("independent_review")
    lane = payload["independent_review_lane"]
    if (
        addendum.get("target") != TARGET_082_TARGET
        or addendum.get("input_order") != "82"
        or not isinstance(review, dict)
        or review.get("required") is not True
        or review.get("status") != "pending"
        or review.get("verdict") is not None
        or lane
        != {
            "status": "pending",
            "expected_policy_id": V9_POLICY_ID,
            "expected_policy_path": "preservation/path_policy_v9.json",
            "expected_verdict_path": (
                "review/REVIEW_ADDENDUM_TARGET_082_OPERATIONAL_V1.md"
            ),
        }
    ):
        raise PreservationPolicyError(
            "target-082 v8/v9 review lifecycle is invalid"
        )
    return {
        "policy": copy.deepcopy(payload),
        "registered_records": list(records_by_path.values()),
        "registered_addenda": {
            "json": records_by_path[
                ADDENDUM_JSON.relative_to(OUT).as_posix()
            ],
            "csv": records_by_path[
                ADDENDUM_CSV.relative_to(OUT).as_posix()
            ],
        },
        "validated_v6": validated_v6,
        "historical_archive": {
            "resolved_paths": {
                path: resolved.relative_to(root.resolve()).as_posix()
                for path, resolved in historical_resolved.items()
            },
            "record_version_mappings": historical_mappings,
        },
    }


def _review_verdict(path: Path) -> str:
    text = path.read_text()
    verdicts = re.findall(
        r"^\*\*VERDICT: (ACCEPT|REJECT)\*\*\s*$",
        text,
        flags=re.MULTILINE,
    )
    if len(verdicts) != 1 or TARGET_082_TARGET not in text:
        raise PreservationPolicyError("target-082 review is malformed")
    return verdicts[0]


def target_082_lifecycle(*, root: Path = OUT) -> dict[str, Any]:
    validated = validate_policy(root=root)
    policy_record = _artifact(
        root / POLICY_PATH.relative_to(OUT), root=root
    )
    if (root / V9_PATH.relative_to(OUT)).exists():
        raise PreservationPolicyError(
            "path_policy_v9 exists but has no independent-review validator"
        )
    review_path = root / REVIEW_PATH.relative_to(OUT)
    reviews: list[dict[str, Any]] = []
    if review_path.exists():
        if not review_path.is_file():
            raise PreservationPolicyError(
                "target-082 review path is not a regular file"
            )
        if _review_verdict(review_path) == "ACCEPT":
            raise PreservationPolicyError(
                "target-082 acceptance is not registered by path_policy_v9"
            )
        reviews = [_artifact(review_path, root=root)]
    return {
        "status": "review-pending",
        "policy_v8": policy_record,
        "policy_v9": None,
        "registered_records": copy.deepcopy(
            validated["registered_records"]
        ),
        "registered_addenda": copy.deepcopy(
            validated["registered_addenda"]
        ),
        "review_records": reviews,
        "selected_as_operational_v2_overlay": False,
    }


def main() -> None:
    if len(sys.argv) != 1:
        raise SystemExit("usage: preservation_policy_v8.py")
    validated = validate_policy()
    print("preservation_policy_v8=PASS")
    print(f"target_082_files={len(validated['registered_records'])}")
    print("target_082_review=pending")


if __name__ == "__main__":
    main()
