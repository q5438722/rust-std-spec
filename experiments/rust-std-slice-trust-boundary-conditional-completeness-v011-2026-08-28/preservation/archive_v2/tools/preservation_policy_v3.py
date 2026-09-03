#!/usr/bin/env python3
"""Validate the additive target-079 v3 preservation policy successor."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import preservation_policy_v2 as parent


OUT = common.OUT
POLICY_PATH = OUT / "preservation/path_policy_v3.json"
PARENT_POLICY_PATH = OUT / "preservation/path_policy_v2.json"
TARGET_079_V3_EVIDENCE = (
    OUT / "evidence/target_079_insert_tail_refinement_v3"
)
REVIEW_ROOT = OUT / "review"

POLICY_ID = "slice-preservation-path-policy-v3"
PARENT_POLICY_ID = parent.POLICY_ID
TARGET_079_V3_ADDITION = "target_079_insert_tail_refinement_v3"
TARGET_079_V3_REVIEW_ADDITION = (
    "target_079_insert_tail_refinement_v3_review"
)
TARGET_080_POLICY_V4_PATH = OUT / "preservation/path_policy_v4.json"
TARGET_080_POLICY_V5_PATH = OUT / "preservation/path_policy_v5.json"
TARGET_081_POLICY_V6_PATH = OUT / "preservation/path_policy_v6.json"
TARGET_081_POLICY_V7_PATH = OUT / "preservation/path_policy_v7.json"
TARGET_080_REVIEW_PATH = (
    OUT / "review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md"
)
TARGET_081_REVIEW_PATH = (
    OUT / "review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md"
)
TARGET_080_ADDENDUM_JSON = (
    OUT / "crosswalk/target_080_operational_v1_addendum.json"
)
TARGET_080_ADDENDUM_CSV = (
    OUT / "crosswalk/target_080_operational_v1_addendum.csv"
)
TARGET_081_ADDENDUM_JSON = (
    OUT / "crosswalk/target_081_operational_v1_addendum.json"
)
TARGET_081_ADDENDUM_CSV = (
    OUT / "crosswalk/target_081_operational_v1_addendum.csv"
)
TARGET_080_POLICY_V4_ID = "slice-preservation-path-policy-v4"
TARGET_080_POLICY_V5_ID = "slice-preservation-path-policy-v5"
TARGET_081_POLICY_V6_ID = "slice-preservation-path-policy-v6"
TARGET_081_POLICY_V7_ID = "slice-preservation-path-policy-v7"
TARGET_080_ADDITION = "target_080_operational_v1"
TARGET_080_REVIEW_ADDITION = "target_080_operational_v1_review"
TARGET_081_ADDITION = "target_081_operational_v1"
TARGET_081_REVIEW_ADDITION = "target_081_operational_v1_review"
TARGET_080_TARGET = "core::slice::sort_unstable"
TARGET_081_TARGET = "core::slice::sort_unstable_by"
TARGET_080_V4_VERSION_ID = (
    "slice-preservation-path-policy-v4@accepted-by-v5"
)
TARGET_080_V4_ARCHIVE_ROOT = PurePosixPath("preservation/archive_v1")
TARGET_080_V4_ARCHIVE_PATH = (
    TARGET_080_V4_ARCHIVE_ROOT / "path_policy_v4.json"
)
TARGET_080_V4_RECORD_ARCHIVES = {
    (
        ".autors/"
        "rust-std-slice-trust-boundary-conditional-completeness-v011-"
        "2026-08-28/wiki/INDEX.md"
    ): (
        "target-080-v4-wiki-index@accepted-by-v5",
        TARGET_080_V4_ARCHIVE_ROOT / "wiki/INDEX.md",
    ),
    (
        ".autors/"
        "rust-std-slice-trust-boundary-conditional-completeness-v011-"
        "2026-08-28/wiki/pages/conditional-completeness/"
        "theorem-and-boundary-policy.md"
    ): (
        "target-080-v4-wiki-page@accepted-by-v5",
        TARGET_080_V4_ARCHIVE_ROOT
        / "wiki/theorem-and-boundary-policy.md",
    ),
    "tools/run_acceptance.py": (
        "target-080-v4-acceptance-runner@accepted-by-v5",
        TARGET_080_V4_ARCHIVE_ROOT / "run_acceptance.py",
    ),
    "tools/run_target_080_operational_v1.py": (
        "target-080-v4-producer@accepted-by-v5",
        TARGET_080_V4_ARCHIVE_ROOT
        / "run_target_080_operational_v1.py",
    ),
    "tests/test_target_080_operational_artifacts_v1.py": (
        "target-080-v4-artifact-test@accepted-by-v5",
        TARGET_080_V4_ARCHIVE_ROOT
        / "test_target_080_operational_artifacts_v1.py",
    ),
}
EXPECTED_PARENT_POLICY_SHA256 = (
    "df04b6d0b5388e0620d07623e365c9d538f9b41c762f98ef898cc3cdd1ca7cfe"
)
EXPECTED_PARENT_POLICY_BYTES = 48840
PreservationPolicyError = parent.PreservationPolicyError
base = parent.parent


def _artifact(path: Path, *, root: Path = OUT) -> dict[str, Any]:
    if not path.is_file():
        raise PreservationPolicyError(
            f"cannot register missing preservation artifact: {path}"
        )
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": base._sha256(path),
        "bytes": path.stat().st_size,
    }


def _registration_records(
    *,
    root: Path = OUT,
    evidence: Path = TARGET_079_V3_EVIDENCE,
) -> list[dict[str, Any]]:
    if not evidence.is_dir():
        raise PreservationPolicyError(
            f"target-079 v3 evidence is missing: {evidence}"
        )
    return [
        _artifact(path, root=root)
        for path in sorted(
            (item for item in evidence.rglob("*") if item.is_file()),
            key=lambda item: item.relative_to(root).parts,
        )
    ]


def _review_registration_records() -> list[dict[str, Any]]:
    return [
        _artifact(path)
        for path in sorted(
            REVIEW_ROOT.glob(
                "*TARGET_079_INSERT_TAIL_REFINEMENT_V3*.md"
            ),
            key=lambda item: item.relative_to(OUT).parts,
        )
    ]


def build_policy_payload() -> dict[str, Any]:
    records = _registration_records()
    review_records = _review_registration_records()
    return {
        "schema_version": 1,
        "policy_id": POLICY_ID,
        "parent_policy_id": PARENT_POLICY_ID,
        "parent_policy": _artifact(PARENT_POLICY_PATH),
        "policy": (
            "path_policy_v2 remains authoritative and byte-identical. "
            "This successor adds the closed target-079 insert_tail and "
            "CopyOnDrop refinement v3 evidence scope and an explicit lane "
            "for its independent review artifacts."
        ),
        "registered_post_v2_additions": {
            TARGET_079_V3_ADDITION: {
                "scope_root": TARGET_079_V3_EVIDENCE.relative_to(
                    OUT
                ).as_posix(),
                "file_count": len(records),
                "records": records,
            },
            TARGET_079_V3_REVIEW_ADDITION: {
                "file_count": len(review_records),
                "records": review_records,
            },
        },
    }


def write_policy() -> None:
    common.write_json(POLICY_PATH, build_policy_payload())


def _load_policy_payload() -> dict[str, Any]:
    try:
        with POLICY_PATH.open() as handle:
            payload = json.load(handle)
    except FileNotFoundError as exc:
        raise PreservationPolicyError(
            f"additive preservation policy is missing: {POLICY_PATH}"
        ) from exc
    expected_keys = {
        "schema_version",
        "policy_id",
        "parent_policy_id",
        "parent_policy",
        "policy",
        "registered_post_v2_additions",
    }
    if (
        not isinstance(payload, dict)
        or set(payload) != expected_keys
        or payload.get("schema_version") != 1
        or payload.get("policy_id") != POLICY_ID
        or payload.get("parent_policy_id") != PARENT_POLICY_ID
    ):
        raise PreservationPolicyError(
            "additive preservation policy identity is invalid"
        )
    return payload


def _registered_additions(payload: dict[str, Any]) -> dict[str, Any]:
    additions = payload["registered_post_v2_additions"]
    if not isinstance(additions, dict) or set(additions) != {
        TARGET_079_V3_ADDITION,
        TARGET_079_V3_REVIEW_ADDITION,
    }:
        raise PreservationPolicyError(
            "additive preservation registration set is invalid"
        )
    return additions


def _validate_v3_registration(
    payload: dict[str, Any],
    *,
    root: Path = OUT,
) -> list[dict[str, Any]]:
    config = _registered_additions(payload)[TARGET_079_V3_ADDITION]
    if not isinstance(config, dict) or set(config) != {
        "scope_root",
        "file_count",
        "records",
    }:
        raise PreservationPolicyError(
            "target-079 v3 registration is malformed"
        )
    records = config["records"]
    count = config["file_count"]
    if (
        isinstance(count, bool)
        or not isinstance(count, int)
        or count <= 0
        or not isinstance(records, list)
        or count != len(records)
    ):
        raise PreservationPolicyError(
            "target-079 v3 registration count is invalid"
        )
    base._validate_artifact_records(
        records,
        "target-079 v3 registered addition",
        root=root,
        expected_count=count,
    )
    base._validate_exact_scope(
        config["scope_root"],
        records,
        "target-079 v3 registered addition",
        root=root,
    )
    expected_scope = TARGET_079_V3_EVIDENCE.relative_to(OUT).as_posix()
    if config["scope_root"] != expected_scope:
        raise PreservationPolicyError(
            "target-079 v3 registration scope changed"
        )
    return records


def _validate_review_registration(
    payload: dict[str, Any],
    *,
    root: Path = OUT,
) -> list[dict[str, Any]]:
    config = _registered_additions(payload)[
        TARGET_079_V3_REVIEW_ADDITION
    ]
    if not isinstance(config, dict) or set(config) != {
        "file_count",
        "records",
    }:
        raise PreservationPolicyError(
            "target-079 v3 review registration is malformed"
        )
    records = config["records"]
    count = config["file_count"]
    if (
        isinstance(count, bool)
        or not isinstance(count, int)
        or count < 0
        or not isinstance(records, list)
        or count != len(records)
    ):
        raise PreservationPolicyError(
            "target-079 v3 review registration count is invalid"
        )
    base._validate_artifact_records(
        records,
        "target-079 v3 registered reviews",
        root=root,
        expected_count=count,
    )
    for record in records:
        path = Path(record["path"])
        if (
            path.parent.as_posix() != "review"
            or "TARGET_079_INSERT_TAIL_REFINEMENT_V3" not in path.name
            or path.suffix != ".md"
        ):
            raise PreservationPolicyError(
                "target-079 v3 review path is outside its additive lane"
            )
    return records


def _load_target_080_policy(path: Path, label: str) -> dict[str, Any]:
    try:
        with path.open() as handle:
            payload = json.load(handle)
    except FileNotFoundError as exc:
        raise PreservationPolicyError(f"{label} is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PreservationPolicyError(f"{label} is not valid JSON") from exc
    if not isinstance(payload, dict):
        raise PreservationPolicyError(f"{label} must be a JSON object")
    return payload


def _canonical_relative_path(value: Any, label: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value:
        raise PreservationPolicyError(f"{label} is not a canonical path")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or ".." in path.parts
        or path.as_posix() != value
    ):
        raise PreservationPolicyError(f"{label} is not a canonical path")
    return path


def _validate_record_shape(
    record: Any, label: str
) -> PurePosixPath:
    if not isinstance(record, dict) or set(record) != {
        "path",
        "sha256",
        "bytes",
    }:
        raise PreservationPolicyError(f"{label} is malformed")
    path = _canonical_relative_path(record["path"], f"{label}.path")
    digest = record["sha256"]
    size = record["bytes"]
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
        or isinstance(size, bool)
        or not isinstance(size, int)
        or size < 0
    ):
        raise PreservationPolicyError(
            f"{label} has a malformed hash or byte count"
        )
    return path


def _resolved_record_path(
    record: dict[str, Any],
    label: str,
    *,
    root: Path,
    require_file: bool = True,
) -> Path:
    relative = _validate_record_shape(record, label)
    root_resolved = root.resolve()
    path = (root / Path(*relative.parts)).resolve()
    try:
        path.relative_to(root_resolved)
    except ValueError as exc:
        raise PreservationPolicyError(
            f"{label}.path escapes the campaign root"
        ) from exc
    if require_file and not path.is_file():
        raise PreservationPolicyError(f"{label} is missing")
    return path


def _record_matches_path(record: dict[str, Any], path: Path) -> bool:
    return (
        path.is_file()
        and path.stat().st_size == record["bytes"]
        and base._sha256(path) == record["sha256"]
    )


def _resolved_archive_root(
    archive_root: PurePosixPath,
    *,
    root: Path,
) -> Path:
    root_resolved = root.resolve()
    archive = (root / Path(*archive_root.parts)).resolve()
    try:
        archive.relative_to(root_resolved)
    except ValueError as exc:
        raise PreservationPolicyError(
            "historical archive root escapes the campaign root"
        ) from exc
    return archive


def _validate_archive_artifact(
    record: Any,
    label: str,
    *,
    root: Path,
    archive_root: PurePosixPath,
) -> Path:
    relative = _validate_record_shape(record, label)
    prefix = archive_root.parts
    if (
        len(relative.parts) <= len(prefix)
        or relative.parts[: len(prefix)] != prefix
    ):
        raise PreservationPolicyError(
            f"{label}.path is outside the archive root"
        )
    archive = _resolved_archive_root(archive_root, root=root)
    path = _resolved_record_path(record, label, root=root)
    try:
        path.relative_to(archive)
    except ValueError as exc:
        raise PreservationPolicyError(
            f"{label}.path resolves outside the archive root"
        ) from exc
    if not _record_matches_path(record, path):
        raise PreservationPolicyError(
            f"{label}: archive byte identity changed"
        )
    return path


def _validate_archive_membership(
    archive_root: PurePosixPath,
    expected_paths: set[str],
    *,
    root: Path,
) -> None:
    archive = _resolved_archive_root(archive_root, root=root)
    if not archive.is_dir():
        raise PreservationPolicyError("historical archive root is missing")
    actual_paths = set()
    for path in archive.rglob("*"):
        resolved = path.resolve()
        try:
            resolved.relative_to(archive)
        except ValueError as exc:
            raise PreservationPolicyError(
                "historical archive member resolves outside the archive root"
            ) from exc
        if path.is_file():
            actual_paths.add(
                path.relative_to(root.resolve()).as_posix()
            )
    if actual_paths != expected_paths:
        missing = sorted(expected_paths - actual_paths)
        unmapped = sorted(actual_paths - expected_paths)
        raise PreservationPolicyError(
            "historical archive membership changed; "
            f"missing={missing[:3]!r} unmapped={unmapped[:3]!r}"
        )


def _validate_target_081_v6_header(
    payload: dict[str, Any],
    v5_payload: dict[str, Any],
    *,
    root: Path,
) -> list[dict[str, Any]]:
    expected_keys = {
        "schema_version",
        "policy_id",
        "parent_policy_id",
        "parent_policy",
        "policy",
        "archive_resolution",
        "registered_post_v5_additions",
        "independent_review_lane",
    }
    if (
        set(payload) != expected_keys
        or payload.get("schema_version") != 2
        or payload.get("policy_id") != TARGET_081_POLICY_V6_ID
        or payload.get("parent_policy_id") != TARGET_080_POLICY_V5_ID
    ):
        raise PreservationPolicyError(
            "target-081 path-policy-v6 identity is invalid"
        )
    parent_record = payload["parent_policy"]
    expected_parent = _artifact(
        root / TARGET_080_POLICY_V5_PATH.relative_to(OUT), root=root
    )
    base._validate_artifact_records(
        [parent_record],
        "target-081 path-policy-v6 parent",
        root=root,
        expected_count=1,
    )
    if parent_record != expected_parent:
        raise PreservationPolicyError(
            "target-081 path-policy-v6 does not byte-bind path_policy_v5"
        )

    additions = payload["registered_post_v5_additions"]
    if not isinstance(additions, dict) or set(additions) != {
        TARGET_081_ADDITION
    }:
        raise PreservationPolicyError(
            "target-081 path-policy-v6 registration set is invalid"
        )
    config = additions[TARGET_081_ADDITION]
    if not isinstance(config, dict) or set(config) != {
        "file_count",
        "records",
    }:
        raise PreservationPolicyError(
            "target-081 path-policy-v6 registration is malformed"
        )
    count = config["file_count"]
    records = config["records"]
    if (
        isinstance(count, bool)
        or not isinstance(count, int)
        or count <= 0
        or not isinstance(records, list)
        or count != len(records)
    ):
        raise PreservationPolicyError(
            "target-081 path-policy-v6 registration count is invalid"
        )
    base._validate_artifact_records(
        records,
        "target-081 path-policy-v6 registered addition",
        root=root,
        expected_count=count,
    )
    forbidden = {
        "preservation/path_policy_v6.json",
        "preservation/path_policy_v7.json",
        "review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md",
    }
    if forbidden & {record["path"] for record in records}:
        raise PreservationPolicyError(
            "target-081 Engineer lane includes reviewer-owned artifacts"
        )
    lane = payload["independent_review_lane"]
    if lane != {
        "status": "pending",
        "expected_policy_id": TARGET_081_POLICY_V7_ID,
        "expected_policy_path": "preservation/path_policy_v7.json",
        "expected_verdict_path": (
            "review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md"
        ),
    }:
        raise PreservationPolicyError(
            "target-081 independent-review lane is invalid"
        )
    return records


def _validate_archive_resolution(
    payload: dict[str, Any],
    v5_payload: dict[str, Any],
    *,
    root: Path,
) -> dict[str, Any]:
    config = payload.get("archive_resolution")
    expected_keys = {
        "schema_version",
        "archive_root",
        "template_record",
        "accepted_policy_version",
        "record_version_mappings",
    }
    if (
        not isinstance(config, dict)
        or set(config) != expected_keys
        or config.get("schema_version") != 1
        or config.get("archive_root")
        != TARGET_080_V4_ARCHIVE_ROOT.as_posix()
    ):
        raise PreservationPolicyError(
            "target-081 historical archive configuration is invalid"
        )
    archive_root = _canonical_relative_path(
        config["archive_root"], "historical archive root"
    )

    template_record = config["template_record"]
    template_path = _resolved_record_path(
        template_record, "historical v4 reconstruction template", root=root
    )
    if (
        template_record["path"]
        != TARGET_080_POLICY_V4_PATH.relative_to(OUT).as_posix()
        or not _record_matches_path(template_record, template_path)
    ):
        raise PreservationPolicyError(
            "historical v4 reconstruction template changed"
        )

    accepted = config["accepted_policy_version"]
    if not isinstance(accepted, dict) or set(accepted) != {
        "version_id",
        "logical_record",
        "archive_record",
        "source",
    }:
        raise PreservationPolicyError(
            "accepted v4 policy version mapping is malformed"
        )
    if (
        accepted["version_id"] != TARGET_080_V4_VERSION_ID
        or accepted["logical_record"] != v5_payload["parent_policy"]
        or not isinstance(accepted["source"], str)
        or not accepted["source"]
    ):
        raise PreservationPolicyError(
            "accepted v4 policy version mapping is invalid"
        )
    accepted_archive = accepted["archive_record"]
    if (
        not isinstance(accepted_archive, dict)
        or accepted_archive.get("path")
        != TARGET_080_V4_ARCHIVE_PATH.as_posix()
    ):
        raise PreservationPolicyError(
            "accepted v4 archive path mapping is invalid"
        )
    accepted_path = _validate_archive_artifact(
        accepted_archive,
        "accepted v4 archive",
        root=root,
        archive_root=archive_root,
    )
    if (
        accepted_path.stat().st_size
        != accepted["logical_record"]["bytes"]
        or base._sha256(accepted_path)
        != accepted["logical_record"]["sha256"]
    ):
        raise PreservationPolicyError(
            "accepted v4 archive does not satisfy path_policy_v5"
        )
    accepted_payload = _load_target_080_policy(
        accepted_path, "accepted archived path-policy-v4"
    )
    accepted_records = accepted_payload.get(
        "registered_post_v3_additions", {}
    ).get(TARGET_080_ADDITION, {}).get("records")
    if not isinstance(accepted_records, list):
        raise PreservationPolicyError(
            "accepted archived path-policy-v4 records are missing"
        )
    accepted_by_path = {
        record.get("path"): record
        for record in accepted_records
        if isinstance(record, dict)
    }

    mappings = config["record_version_mappings"]
    if not isinstance(mappings, list):
        raise PreservationPolicyError(
            "historical record version mappings must be a list"
        )
    mapped_by_path: dict[str, dict[str, Any]] = {}
    archive_paths = {accepted_archive["path"]}
    version_ids: set[str] = set()
    for index, mapping in enumerate(mappings):
        label = f"historical record version mapping[{index}]"
        if not isinstance(mapping, dict) or set(mapping) != {
            "version_id",
            "logical_record",
            "archive_record",
            "source",
        }:
            raise PreservationPolicyError(f"{label} is malformed")
        logical = mapping["logical_record"]
        logical_path = _validate_record_shape(
            logical, f"{label}.logical_record"
        ).as_posix()
        expected = TARGET_080_V4_RECORD_ARCHIVES.get(logical_path)
        archive_record = mapping["archive_record"]
        if (
            expected is None
            or mapping["version_id"] != expected[0]
            or not isinstance(archive_record, dict)
            or archive_record.get("path")
            != expected[1].as_posix()
            or accepted_by_path.get(logical_path) != logical
            or not isinstance(mapping["source"], str)
            or not mapping["source"]
        ):
            raise PreservationPolicyError(f"{label} is invalid")
        if (
            logical_path in mapped_by_path
            or mapping["version_id"] in version_ids
            or archive_record["path"] in archive_paths
        ):
            raise PreservationPolicyError(
                "historical archive mappings conflict"
            )
        archive_path = _validate_archive_artifact(
            archive_record,
            f"{label}.archive_record",
            root=root,
            archive_root=archive_root,
        )
        if (
            archive_path.stat().st_size != logical["bytes"]
            or base._sha256(archive_path) != logical["sha256"]
        ):
            raise PreservationPolicyError(
                f"{label} does not materialize its logical record"
            )
        mapped_by_path[logical_path] = {
            **mapping,
            "archive_path": archive_path,
        }
        version_ids.add(mapping["version_id"])
        archive_paths.add(archive_record["path"])
    if set(mapped_by_path) != set(TARGET_080_V4_RECORD_ARCHIVES):
        raise PreservationPolicyError(
            "historical v4 records are missing explicit version mappings"
        )
    _validate_archive_membership(
        archive_root, archive_paths, root=root
    )

    template_payload = _load_target_080_policy(
        template_path, "historical v4 reconstruction template"
    )
    template_records = template_payload.get(
        "registered_post_v3_additions", {}
    ).get(TARGET_080_ADDITION, {}).get("records")
    if not isinstance(template_records, list):
        raise PreservationPolicyError(
            "historical v4 reconstruction template records are missing"
        )
    template_by_path = {
        record.get("path"): record
        for record in template_records
        if isinstance(record, dict)
    }
    for logical_path, mapping in mapped_by_path.items():
        if logical_path not in template_by_path:
            raise PreservationPolicyError(
                "historical v4 reconstruction mapping is unmapped"
            )
        template_by_path[logical_path].clear()
        template_by_path[logical_path].update(
            copy.deepcopy(mapping["logical_record"])
        )
    reconstructed = (
        json.dumps(template_payload, indent=2, sort_keys=True) + "\n"
    ).encode()
    if reconstructed != accepted_path.read_bytes():
        raise PreservationPolicyError(
            "accepted v4 archive is not the declared deterministic "
            "reconstruction"
        )

    def resolve_record(record: dict[str, Any]) -> Path:
        logical_path = _validate_record_shape(
            record, "accepted v4 registered record"
        ).as_posix()
        mapping = mapped_by_path.get(logical_path)
        if mapping is not None:
            if mapping["logical_record"] != record:
                raise PreservationPolicyError(
                    "historical archive mapping conflicts with v4 record"
                )
            return mapping["archive_path"]
        return base._validate_artifact_records(
            [record],
            "accepted v4 live registered record",
            root=root,
            expected_count=1,
        )[0]

    validated_v4 = _validate_target_080_v4(
        accepted_payload,
        root=root,
        record_resolver=resolve_record,
        policy_record=accepted["logical_record"],
    )
    return {
        "accepted_v4_record": copy.deepcopy(accepted["logical_record"]),
        "accepted_v4_archive": copy.deepcopy(accepted_archive),
        "record_version_mappings": copy.deepcopy(mappings),
        "validated_v4": validated_v4,
        "archive_paths": copy.deepcopy(archive_paths),
    }


def _validate_target_081_v6(
    payload: dict[str, Any],
    v5_payload: dict[str, Any],
    *,
    root: Path,
) -> dict[str, Any]:
    records = _validate_target_081_v6_header(
        payload, v5_payload, root=root
    )
    archive = _validate_archive_resolution(
        payload, v5_payload, root=root
    )
    records_by_path = {record["path"]: record for record in records}
    for archive_path in archive["archive_paths"]:
        if archive_path not in records_by_path:
            raise PreservationPolicyError(
                "target-081 path-policy-v6 does not register its archive"
            )
    addendum_paths = {
        "json": TARGET_081_ADDENDUM_JSON.relative_to(OUT).as_posix(),
        "csv": TARGET_081_ADDENDUM_CSV.relative_to(OUT).as_posix(),
    }
    if not set(addendum_paths.values()) <= set(records_by_path):
        raise PreservationPolicyError(
            "target-081 path-policy-v6 does not register both addenda"
        )
    lane = payload["independent_review_lane"]
    addendum = _load_target_080_policy(
        root / addendum_paths["json"], "target-081 crosswalk addendum"
    )
    review = addendum.get("independent_review")
    if (
        addendum.get("schema_version") != 1
        or addendum.get("input_order") != "81"
        or addendum.get("target") != TARGET_081_TARGET
        or not isinstance(review, dict)
        or review.get("required") is not True
        or review.get("status") != "pending"
        or review.get("verdict") is not None
        or review.get("expected_path") != lane["expected_verdict_path"]
        or review.get("expected_successor_policy")
        != lane["expected_policy_path"]
    ):
        raise PreservationPolicyError(
            "target-081 crosswalk does not retain the pending v6/v7 lifecycle"
        )
    return {
        "registered_records": copy.deepcopy(records),
        "addenda": {
            name: copy.deepcopy(records_by_path[path])
            for name, path in addendum_paths.items()
        },
        **archive,
    }


def _target_080_review_verdict(path: Path) -> str:
    text = path.read_text()
    verdicts = re.findall(
        r"^\*\*VERDICT: (ACCEPT|REJECT)\*\*\s*$",
        text,
        flags=re.MULTILINE,
    )
    if len(verdicts) != 1 or TARGET_080_TARGET not in text:
        raise PreservationPolicyError(
            "target-080 review verdict is malformed or targets another item"
        )
    return verdicts[0]


def _target_081_review_verdict(path: Path) -> str:
    text = path.read_text()
    verdicts = re.findall(
        r"^\*\*VERDICT: (ACCEPT|REJECT)\*\*\s*$",
        text,
        flags=re.MULTILINE,
    )
    if len(verdicts) != 1 or TARGET_081_TARGET not in text:
        raise PreservationPolicyError(
            "target-081 review verdict is malformed or targets another item"
        )
    return verdicts[0]


def _validate_target_080_v4(
    payload: dict[str, Any],
    *,
    root: Path,
    record_resolver: Callable[[dict[str, Any]], Path] | None = None,
    policy_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    expected_keys = {
        "schema_version",
        "policy_id",
        "parent_policy_id",
        "parent_policy",
        "policy",
        "registered_post_v3_additions",
        "independent_review_lane",
    }
    if (
        set(payload) != expected_keys
        or payload.get("schema_version") != 1
        or payload.get("policy_id") != TARGET_080_POLICY_V4_ID
        or payload.get("parent_policy_id") != POLICY_ID
    ):
        raise PreservationPolicyError(
            "target-080 path-policy-v4 identity is invalid"
        )

    parent_record = payload["parent_policy"]
    resolved_parent = base._validate_artifact_records(
        [parent_record],
        "target-080 path-policy-v4 parent",
        root=root,
        expected_count=1,
    )
    expected_parent = root / "preservation/path_policy_v3.json"
    if (
        parent_record["path"] != "preservation/path_policy_v3.json"
        or resolved_parent[0] != expected_parent.resolve()
    ):
        raise PreservationPolicyError(
            "target-080 path-policy-v4 does not bind path_policy_v3"
        )

    additions = payload["registered_post_v3_additions"]
    if not isinstance(additions, dict) or set(additions) != {
        TARGET_080_ADDITION
    }:
        raise PreservationPolicyError(
            "target-080 path-policy-v4 registration set is invalid"
        )
    config = additions[TARGET_080_ADDITION]
    if not isinstance(config, dict) or set(config) != {
        "file_count",
        "records",
    }:
        raise PreservationPolicyError(
            "target-080 path-policy-v4 registration is malformed"
        )
    count = config["file_count"]
    records = config["records"]
    if (
        isinstance(count, bool)
        or not isinstance(count, int)
        or count <= 0
        or not isinstance(records, list)
        or count != len(records)
    ):
        raise PreservationPolicyError(
            "target-080 path-policy-v4 registration count is invalid"
        )
    if record_resolver is None:
        base._validate_artifact_records(
            records,
            "target-080 path-policy-v4 registered addition",
            root=root,
            expected_count=count,
        )
    else:
        for record in records:
            record_resolver(record)
    paths = [record["path"] for record in records]
    if paths != sorted(paths, key=lambda value: Path(value).parts):
        raise PreservationPolicyError(
            "target-080 path-policy-v4 records are not sorted"
        )

    addendum_paths = {
        "json": TARGET_080_ADDENDUM_JSON.relative_to(OUT).as_posix(),
        "csv": TARGET_080_ADDENDUM_CSV.relative_to(OUT).as_posix(),
    }
    records_by_path = {record["path"]: record for record in records}
    if not set(addendum_paths.values()) <= set(records_by_path):
        raise PreservationPolicyError(
            "target-080 path-policy-v4 does not register both addenda"
        )
    forbidden = {
        "preservation/path_policy_v4.json",
        "preservation/path_policy_v5.json",
        "review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md",
    }
    if forbidden & set(records_by_path):
        raise PreservationPolicyError(
            "target-080 Engineer lane includes reviewer-owned artifacts"
        )

    lane = payload["independent_review_lane"]
    if lane != {
        "status": "pending",
        "expected_policy_id": TARGET_080_POLICY_V5_ID,
        "expected_policy_path": "preservation/path_policy_v5.json",
        "expected_verdict_path": (
            "review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md"
        ),
    }:
        raise PreservationPolicyError(
            "target-080 independent-review lane is invalid"
        )

    addendum = _load_target_080_policy(
        root / addendum_paths["json"], "target-080 crosswalk addendum"
    )
    review = addendum.get("independent_review")
    if (
        addendum.get("schema_version") != 1
        or addendum.get("input_order") != "80"
        or addendum.get("target") != TARGET_080_TARGET
        or not isinstance(review, dict)
        or review.get("required") is not True
        or review.get("status") != "pending"
        or review.get("verdict") is not None
        or review.get("expected_path") != lane["expected_verdict_path"]
        or review.get("separate_preservation_policy")
        != lane["expected_policy_path"]
    ):
        raise PreservationPolicyError(
            "target-080 crosswalk does not retain the pending v4/v5 lifecycle"
        )

    if policy_record is None:
        policy_record = _artifact(
            root / TARGET_080_POLICY_V4_PATH.relative_to(OUT),
            root=root,
        )
        base._validate_artifact_records(
            [policy_record],
            "target-080 path-policy-v4",
            root=root,
            expected_count=1,
        )
    else:
        _validate_record_shape(
            policy_record, "target-080 path-policy-v4 logical record"
        )
    return {
        "policy_record": policy_record,
        "registered_records": copy.deepcopy(records),
        "addenda": {
            name: copy.deepcopy(records_by_path[path])
            for name, path in addendum_paths.items()
        },
    }


def _validate_target_080_v5(
    payload: dict[str, Any],
    *,
    root: Path,
    expected_parent: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    expected_keys = {
        "schema_version",
        "policy_id",
        "parent_policy_id",
        "parent_policy",
        "policy",
        "registered_post_v4_additions",
    }
    if (
        set(payload) != expected_keys
        or payload.get("schema_version") != 1
        or payload.get("policy_id") != TARGET_080_POLICY_V5_ID
        or payload.get("parent_policy_id") != TARGET_080_POLICY_V4_ID
    ):
        raise PreservationPolicyError(
            "target-080 path-policy-v5 identity is invalid"
        )

    parent_record = payload["parent_policy"]
    if expected_parent is None:
        expected_parent = _artifact(
            root / "preservation/path_policy_v4.json", root=root
        )
        base._validate_artifact_records(
            [parent_record],
            "target-080 path-policy-v5 parent",
            root=root,
            expected_count=1,
        )
    if parent_record != expected_parent:
        raise PreservationPolicyError(
            "target-080 path-policy-v5 does not byte-bind path_policy_v4"
        )

    additions = payload["registered_post_v4_additions"]
    if not isinstance(additions, dict) or set(additions) != {
        TARGET_080_REVIEW_ADDITION
    }:
        raise PreservationPolicyError(
            "target-080 path-policy-v5 registration set is invalid"
        )
    config = additions[TARGET_080_REVIEW_ADDITION]
    if not isinstance(config, dict) or set(config) != {
        "file_count",
        "records",
    }:
        raise PreservationPolicyError(
            "target-080 path-policy-v5 review registration is malformed"
        )
    count = config["file_count"]
    records = config["records"]
    if (
        isinstance(count, bool)
        or not isinstance(count, int)
        or count != 1
        or not isinstance(records, list)
    ):
        raise PreservationPolicyError(
            "target-080 path-policy-v5 must register one review"
        )
    base._validate_artifact_records(
        records,
        "target-080 path-policy-v5 registered review",
        root=root,
        expected_count=1,
    )
    if records[0]["path"] != (
        "review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md"
    ):
        raise PreservationPolicyError(
            "target-080 path-policy-v5 review path is outside its lane"
        )
    if _target_080_review_verdict(root / records[0]["path"]) != "ACCEPT":
        raise PreservationPolicyError(
            "target-080 path-policy-v5 does not bind an accepting verdict"
        )
    return records


def _validate_target_081_v7(
    payload: dict[str, Any],
    *,
    root: Path,
    expected_parent: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    expected_keys = {
        "schema_version",
        "policy_id",
        "parent_policy_id",
        "parent_policy",
        "policy",
        "registered_post_v6_additions",
    }
    if (
        set(payload) != expected_keys
        or payload.get("schema_version") != 1
        or payload.get("policy_id") != TARGET_081_POLICY_V7_ID
        or payload.get("parent_policy_id") != TARGET_081_POLICY_V6_ID
    ):
        raise PreservationPolicyError(
            "target-081 path-policy-v7 identity is invalid"
        )

    parent_record = payload["parent_policy"]
    resolved_parent = base._validate_artifact_records(
        [parent_record],
        "target-081 path-policy-v7 parent",
        root=root,
        expected_count=1,
    )
    v6_path = root / TARGET_081_POLICY_V6_PATH.relative_to(OUT)
    if expected_parent is None:
        expected_parent = _artifact(v6_path, root=root)
    if (
        resolved_parent[0] != v6_path.resolve()
        or parent_record != expected_parent
    ):
        raise PreservationPolicyError(
            "target-081 path-policy-v7 does not byte-bind path_policy_v6"
        )

    additions = payload["registered_post_v6_additions"]
    if not isinstance(additions, dict) or set(additions) != {
        TARGET_081_REVIEW_ADDITION
    }:
        raise PreservationPolicyError(
            "target-081 path-policy-v7 registration set is invalid"
        )
    config = additions[TARGET_081_REVIEW_ADDITION]
    if not isinstance(config, dict) or set(config) != {
        "file_count",
        "records",
    }:
        raise PreservationPolicyError(
            "target-081 path-policy-v7 review registration is malformed"
        )
    count = config["file_count"]
    records = config["records"]
    if (
        isinstance(count, bool)
        or not isinstance(count, int)
        or count != 1
        or not isinstance(records, list)
        or len(records) != 1
    ):
        raise PreservationPolicyError(
            "target-081 path-policy-v7 must register one review"
        )
    base._validate_artifact_records(
        records,
        "target-081 path-policy-v7 registered review",
        root=root,
        expected_count=1,
    )
    expected_review_path = TARGET_081_REVIEW_PATH.relative_to(OUT).as_posix()
    if records[0]["path"] != expected_review_path:
        raise PreservationPolicyError(
            "target-081 path-policy-v7 review path is outside its lane"
        )
    if _target_081_review_verdict(root / records[0]["path"]) != "ACCEPT":
        raise PreservationPolicyError(
            "target-081 path-policy-v7 does not bind an accepting verdict"
        )
    return copy.deepcopy(records)


def target_080_lifecycle(*, root: Path = OUT) -> dict[str, Any]:
    if root.resolve() != OUT.resolve():
        raise PreservationPolicyError(
            "target-080 lifecycle must validate against the campaign root"
        )
    v5_path = root / TARGET_080_POLICY_V5_PATH.relative_to(OUT)
    review_path = root / TARGET_080_REVIEW_PATH.relative_to(OUT)
    if v5_path.exists():
        if not v5_path.is_file():
            raise PreservationPolicyError(
                "target-080 path-policy-v5 is not a regular file"
            )
        v5_payload = _load_target_080_policy(
            v5_path, "target-080 path-policy-v5"
        )
        v6_path = root / TARGET_081_POLICY_V6_PATH.relative_to(OUT)
        v6_payload = _load_target_080_policy(
            v6_path, "target-081 path-policy-v6"
        )
        archive = _validate_target_081_v6(
            v6_payload, v5_payload, root=root
        )
        v4 = archive["validated_v4"]
        reviews = _validate_target_080_v5(
            v5_payload,
            root=root,
            expected_parent=archive["accepted_v4_record"],
        )
        status = "review-accepted"
        v5_record: dict[str, Any] | None = _artifact(v5_path, root=root)
        base._validate_artifact_records(
            [v5_record],
            "target-080 path-policy-v5",
            root=root,
            expected_count=1,
        )
    else:
        reviews = []
        if review_path.exists():
            if not review_path.is_file():
                raise PreservationPolicyError(
                    "target-080 review path is not a regular file"
                )
            if _target_080_review_verdict(review_path) == "ACCEPT":
                raise PreservationPolicyError(
                    "target-080 acceptance is not registered by path_policy_v5"
                )
            reviews = [_artifact(review_path, root=root)]
            base._validate_artifact_records(
                reviews,
                "target-080 pending review",
                root=root,
                expected_count=1,
            )
        v4_path = root / TARGET_080_POLICY_V4_PATH.relative_to(OUT)
        v4 = _validate_target_080_v4(
            _load_target_080_policy(
                v4_path, "target-080 path-policy-v4"
            ),
            root=root,
        )
        archive = None
        status = "review-pending"
        v5_record = None
    return {
        "status": status,
        "policy_v4": v4["policy_record"],
        "policy_v5": v5_record,
        "registered_records": v4["registered_records"],
        "registered_addenda": v4["addenda"],
        "review_records": copy.deepcopy(reviews),
        "archive_resolution": (
            None
            if archive is None
            else {
                "accepted_v4_archive": copy.deepcopy(
                    archive["accepted_v4_archive"]
                ),
                "record_version_mappings": copy.deepcopy(
                    archive["record_version_mappings"]
                ),
            }
        ),
        "selected_as_operational_v2_overlay": False,
    }


def target_081_lifecycle(*, root: Path = OUT) -> dict[str, Any]:
    v5_path = root / TARGET_080_POLICY_V5_PATH.relative_to(OUT)
    v6_path = root / TARGET_081_POLICY_V6_PATH.relative_to(OUT)
    v7_path = root / TARGET_081_POLICY_V7_PATH.relative_to(OUT)
    review_path = root / TARGET_081_REVIEW_PATH.relative_to(OUT)
    v5_payload = _load_target_080_policy(
        v5_path, "target-080 path-policy-v5"
    )
    v6_payload = _load_target_080_policy(
        v6_path, "target-081 path-policy-v6"
    )
    validated_v6 = _validate_target_081_v6(
        v6_payload, v5_payload, root=root
    )
    _validate_target_080_v5(
        v5_payload,
        root=root,
        expected_parent=validated_v6["accepted_v4_record"],
    )
    v6_record = _artifact(v6_path, root=root)
    base._validate_artifact_records(
        [v6_record],
        "target-081 path-policy-v6",
        root=root,
        expected_count=1,
    )

    if v7_path.exists():
        if not v7_path.is_file():
            raise PreservationPolicyError(
                "target-081 path-policy-v7 is not a regular file"
            )
        v7_payload = _load_target_080_policy(
            v7_path, "target-081 path-policy-v7"
        )
        reviews = _validate_target_081_v7(
            v7_payload,
            root=root,
            expected_parent=v6_record,
        )
        status = "review-accepted"
        v7_record: dict[str, Any] | None = _artifact(v7_path, root=root)
        base._validate_artifact_records(
            [v7_record],
            "target-081 path-policy-v7",
            root=root,
            expected_count=1,
        )
    else:
        reviews = []
        if review_path.exists():
            if not review_path.is_file():
                raise PreservationPolicyError(
                    "target-081 review path is not a regular file"
                )
            if _target_081_review_verdict(review_path) == "ACCEPT":
                raise PreservationPolicyError(
                    "target-081 acceptance is not registered by path_policy_v7"
                )
            reviews = [_artifact(review_path, root=root)]
            base._validate_artifact_records(
                reviews,
                "target-081 pending review",
                root=root,
                expected_count=1,
            )
        status = "review-pending"
        v7_record = None
    return {
        "status": status,
        "policy_v6": v6_record,
        "policy_v7": v7_record,
        "registered_records": copy.deepcopy(
            validated_v6["registered_records"]
        ),
        "registered_addenda": copy.deepcopy(validated_v6["addenda"]),
        "review_records": copy.deepcopy(reviews),
        "archive_resolution": {
            "accepted_v4_archive": copy.deepcopy(
                validated_v6["accepted_v4_archive"]
            ),
            "record_version_mappings": copy.deepcopy(
                validated_v6["record_version_mappings"]
            ),
        },
        "selected_as_operational_v2_overlay": False,
    }


def _validate_parent_chain(
    current_reviews: list[dict[str, Any]],
    *,
    target_080_reviews: list[dict[str, Any]],
    target_081_reviews: list[dict[str, Any]],
    validate_all_operational_records: bool,
    validate_parent_addition: bool = True,
    parent_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if parent_payload is None:
        parent_payload = parent._load_policy_payload()
    parent_parent = parent_payload["parent_policy"]
    resolved = base._validate_artifact_records(
        [parent_parent],
        "path-policy-v2 parent preservation policy",
        root=OUT,
        expected_count=1,
    )
    if (
        resolved[0] != parent.PARENT_POLICY_PATH.resolve()
        or parent_parent["sha256"]
        != parent.EXPECTED_PARENT_POLICY_SHA256
        or parent_parent["bytes"] != parent.EXPECTED_PARENT_POLICY_BYTES
    ):
        raise PreservationPolicyError(
            "path_policy_v2 no longer binds immutable path_policy_v1"
        )

    parent_addition = (
        parent._validate_v3_registration(parent_payload)
        if validate_parent_addition
        else []
    )
    parent_reviews = parent._validate_review_registration(parent_payload)
    legacy_payload = base._load_policy_payload()
    final_groups = base._validate_final_inventory(
        legacy_payload, root=OUT
    )
    operational_groups = base._validate_operational_v2_inventory(
        legacy_payload,
        root=OUT,
        validate_all_records=validate_all_operational_records,
    )
    certification_reviews = base._validate_certification_inventory(
        legacy_payload, root=OUT
    )
    legacy_additions = base._validate_registered_additions(
        legacy_payload, root=OUT
    )
    allowed_reviews = base._validate_review_membership(
        operational_groups["prior_reviews"],
        certification_reviews,
        [
            *legacy_additions[base.TARGET_079_REVIEW_ADDITION],
            *parent_reviews,
            *current_reviews,
            *target_080_reviews,
            *target_081_reviews,
        ],
        root=OUT,
    )
    return {
        "final_campaign_groups": copy.deepcopy(final_groups),
        "operational_v2_groups": copy.deepcopy(operational_groups),
        "legacy_additions": copy.deepcopy(legacy_additions),
        "parent_addition": copy.deepcopy(parent_addition),
        "parent_reviews": copy.deepcopy(parent_reviews),
        "historical_reviews": copy.deepcopy(
            operational_groups["prior_reviews"]
        ),
        "allowed_reviews": copy.deepcopy(allowed_reviews),
    }


def validate_parent_binding(
    payload: dict[str, Any] | None = None,
    *,
    root: Path = OUT,
    validate_all_operational_records: bool = True,
    validate_parent_addition: bool = True,
    parent_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if payload is None:
        payload = _load_policy_payload()
    if root.resolve() != OUT.resolve():
        raise PreservationPolicyError(
            "additive policy must validate against the campaign root"
        )
    parent_record = payload["parent_policy"]
    resolved = base._validate_artifact_records(
        [parent_record],
        "parent preservation policy",
        root=root,
        expected_count=1,
    )
    if resolved[0] != PARENT_POLICY_PATH.resolve():
        raise PreservationPolicyError(
            "additive policy does not bind path_policy_v2.json"
        )
    if (
        parent_record["sha256"] != EXPECTED_PARENT_POLICY_SHA256
        or parent_record["bytes"] != EXPECTED_PARENT_POLICY_BYTES
    ):
        raise PreservationPolicyError(
            "path_policy_v2.json immutable identity changed"
        )
    current_reviews = _validate_review_registration(payload, root=root)
    target_080 = target_080_lifecycle(root=root)
    target_081 = target_081_lifecycle(root=root)
    chain = _validate_parent_chain(
        current_reviews,
        target_080_reviews=target_080["review_records"],
        target_081_reviews=target_081["review_records"],
        validate_all_operational_records=(
            validate_all_operational_records
        ),
        validate_parent_addition=validate_parent_addition,
        parent_payload=parent_payload,
    )
    return {
        "policy_id": POLICY_ID,
        "parent_policy_id": PARENT_POLICY_ID,
        "parent_policy": copy.deepcopy(parent_record),
        "parent_chain": chain,
        "review_additions": copy.deepcopy(current_reviews),
        "target_080_lifecycle": copy.deepcopy(target_080),
        "target_081_lifecycle": copy.deepcopy(target_081),
    }


def validate_predecessor_policy(
    *,
    require_registration: bool = True,
    parent_payload: dict[str, Any] | None = None,
    validate_all_operational_records: bool = True,
) -> dict[str, Any]:
    if parent_payload is None:
        parent_payload = parent._load_policy_payload()
    binding = validate_parent_binding(
        validate_all_operational_records=(
            validate_all_operational_records
        ),
        validate_parent_addition=require_registration,
        parent_payload=parent_payload,
    )
    chain = binding["parent_chain"]
    return {
        "policy_id": parent.POLICY_ID,
        "parent_policy_id": parent.PARENT_POLICY_ID,
        "parent_policy": copy.deepcopy(parent_payload["parent_policy"]),
        "legacy": {
            "final_campaign_groups": copy.deepcopy(
                chain["final_campaign_groups"]
            ),
            "operational_v2_groups": copy.deepcopy(
                chain["operational_v2_groups"]
            ),
            "registered_additions": copy.deepcopy(
                chain["legacy_additions"]
            ),
            "allowed_reviews": copy.deepcopy(chain["allowed_reviews"]),
        },
        "registered_additions": {
            parent.TARGET_078_V3_ADDITION: copy.deepcopy(
                chain["parent_addition"]
            ),
            parent.TARGET_078_V3_REVIEW_ADDITION: copy.deepcopy(
                chain["parent_reviews"]
            ),
        },
        "allowed_reviews": copy.deepcopy(chain["allowed_reviews"]),
        "target_080_lifecycle": copy.deepcopy(
            binding["target_080_lifecycle"]
        ),
        "target_081_lifecycle": copy.deepcopy(
            binding["target_081_lifecycle"]
        ),
    }


def validate_policy_payload(
    payload: dict[str, Any],
    *,
    root: Path = OUT,
    validate_all_operational_records: bool = True,
) -> dict[str, Any]:
    binding = validate_parent_binding(
        payload,
        root=root,
        validate_all_operational_records=(
            validate_all_operational_records
        ),
    )
    additions = _validate_v3_registration(payload, root=root)
    return {
        "policy_id": POLICY_ID,
        "parent_policy_id": PARENT_POLICY_ID,
        "parent_policy": binding["parent_policy"],
        "parent_chain": binding["parent_chain"],
        "legacy": {
            "final_campaign_groups": copy.deepcopy(
                binding["parent_chain"]["final_campaign_groups"]
            ),
            "operational_v2_groups": copy.deepcopy(
                binding["parent_chain"]["operational_v2_groups"]
            ),
            "registered_additions": copy.deepcopy(
                binding["parent_chain"]["legacy_additions"]
            ),
            "allowed_reviews": copy.deepcopy(
                binding["parent_chain"]["allowed_reviews"]
            ),
        },
        "registered_additions": {
            TARGET_079_V3_ADDITION: copy.deepcopy(additions),
            TARGET_079_V3_REVIEW_ADDITION: copy.deepcopy(
                binding["review_additions"]
            ),
        },
        "allowed_reviews": copy.deepcopy(
            binding["parent_chain"]["allowed_reviews"]
        ),
        "target_080_lifecycle": copy.deepcopy(
            binding["target_080_lifecycle"]
        ),
        "target_081_lifecycle": copy.deepcopy(
            binding["target_081_lifecycle"]
        ),
    }


def validate_policy() -> dict[str, Any]:
    return validate_policy_payload(_load_policy_payload())


def final_campaign_groups() -> dict[str, list[dict[str, Any]]]:
    validated = validate_policy_payload(
        _load_policy_payload(),
        validate_all_operational_records=False,
    )
    chain = validated["parent_chain"]
    groups = chain["final_campaign_groups"]
    current = validated["registered_additions"][TARGET_079_V3_ADDITION]
    target_080 = validated["target_080_lifecycle"][
        "registered_records"
    ]
    target_081_lifecycle_state = validated["target_081_lifecycle"]
    target_081 = target_081_lifecycle_state["registered_records"]
    excluded = {
        (OUT / record["path"]).resolve()
        for record in (
            *chain["legacy_additions"][base.TARGET_078_ADDITION],
            *chain["parent_addition"],
            *current,
            *target_080,
            *target_081,
        )
    }
    actual = base._actual_final_group_paths(excluded)
    actual["authority_ledgers"] -= {
        record["path"]
        for record in (
            *validated["target_080_lifecycle"][
                "registered_addenda"
            ].values(),
            *target_081_lifecycle_state["registered_addenda"].values(),
        )
        if PurePosixPath(record["path"]).parent
        == PurePosixPath("crosswalk")
    }
    actual["accepted_incremental_reviews"] -= {
        record["path"]
        for record in (
            *chain["parent_reviews"],
            *validated["registered_additions"][
                TARGET_079_V3_REVIEW_ADDITION
            ],
        )
    }
    for group, records in groups.items():
        expected = {record["path"] for record in records}
        if actual[group] != expected:
            missing = sorted(expected - actual[group])
            added = sorted(actual[group] - expected)
            raise PreservationPolicyError(
                f"final campaign {group} membership changed; "
                f"missing={missing[:3]!r} added={added[:3]!r}"
            )
    return groups


def review_inventory() -> dict[str, list[dict[str, Any]]]:
    validated = validate_policy_payload(
        _load_policy_payload(),
        validate_all_operational_records=False,
    )
    return {
        "historical": copy.deepcopy(
            validated["parent_chain"]["historical_reviews"]
        ),
        "allowed": copy.deepcopy(validated["allowed_reviews"]),
    }


def historical_review_paths() -> list[Path]:
    return [
        OUT / record["path"] for record in review_inventory()["historical"]
    ]


def historical_review_digest(root: Path = REVIEW_ROOT) -> str:
    if root.resolve() != REVIEW_ROOT.resolve():
        raise PreservationPolicyError(
            "historical review digest root is not the registered review scope"
        )
    digest = hashlib.sha256()
    for record in review_inventory()["historical"]:
        path = OUT / record["path"]
        identity_path = base._artifact_identity_path(
            record, path, root=OUT
        )
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(identity_path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def validate_review_universe() -> None:
    review_inventory()


def validate_post_certification_additions() -> None:
    validate_policy()


def main(argv: list[str]) -> None:
    if argv == ["--write"]:
        write_policy()
        print(f"preservation_policy_written={common.relpath(POLICY_PATH)}")
        return
    if argv:
        raise SystemExit("usage: preservation_policy_v3.py [--write]")
    validated = validate_policy()
    count = len(validated["registered_additions"][TARGET_079_V3_ADDITION])
    reviews = len(
        validated["registered_additions"][
            TARGET_079_V3_REVIEW_ADDITION
        ]
    )
    print("preservation_policy_v3=PASS")
    print(f"target_079_v3_files={count}")
    print(f"target_079_v3_reviews={reviews}")


if __name__ == "__main__":
    main(sys.argv[1:])
