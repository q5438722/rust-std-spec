#!/usr/bin/env python3
"""Validate the versioned, path-level preservation policy."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

import campaign_common as common


OUT = common.OUT
POLICY_PATH = OUT / "preservation/path_policy_v1.json"

FINAL_ROOT = OUT / "evidence/final_campaign"
FINAL_BASELINE = FINAL_ROOT / "preservation_baseline.json"
OPERATIONAL_V2_MANIFEST = (
    FINAL_ROOT / "operational_v2/reconciliation_manifest.json"
)
OPERATIONAL_V2_CERTIFIED_PROJECTION = (
    FINAL_ROOT / "operational_v2/certified/certified_projection.json"
)
REVIEW_ROOT = OUT / "review"
LIVE_REVIEW_REQUEST = OUT / "review/REVIEW_REQUEST.md"
OPERATIONAL_V2_REVIEW_REQUEST_ARCHIVE = (
    OUT / "preservation/review_request_operational_v2_frozen.md"
)
OPERATIONAL_V2_REVIEW_REQUEST_RECORD = {
    "path": "review/REVIEW_REQUEST.md",
    "sha256": "e1905d3a69c4f42af694f9483490b9a3a7d688aa9e9175e8bd93bc79474d425c",
    "bytes": 3347,
}

TARGET_078_OPERATIONAL_EVIDENCE = (
    OUT / "evidence/target_078_operational_v1"
)
TARGET_079_OPERATIONAL_EVIDENCE = (
    OUT / "evidence/target_079_operational_v1"
)
TARGET_079_ADAPTER_EVIDENCE = (
    OUT / "evidence/target_079_adapter_refinement_v2"
)

AGGREGATE_CROSSWALKS = {
    OUT / "crosswalk/conditional_obligation_crosswalk.csv",
    OUT / "crosswalk/conditional_obligation_crosswalk.json",
    OUT / "crosswalk/conditional_obligation_crosswalk_operational_v2.csv",
    OUT / "crosswalk/conditional_obligation_crosswalk_operational_v2.json",
}
OPERATIONAL_ADDENDA = {
    OUT / "crosswalk/target_078_operational_v1_addendum.csv",
    OUT / "crosswalk/target_078_operational_v1_addendum.json",
    OUT / "crosswalk/target_079_operational_v1_addendum.csv",
    OUT / "crosswalk/target_079_operational_v1_addendum.json",
}

POLICY_ID = "slice-preservation-path-policy-v1"
TARGET_078_ADDITION = "target_078_adapter_refinement_v2"
TARGET_079_REVIEW_ADDITION = "target_079_adapter_review"

EXPECTED_FINAL_COUNTS = {
    "preexisting_evidence": 6844,
    "frozen_inputs": 320,
    "authority_ledgers": 9,
    "accepted_incremental_reviews": 29,
}
EXPECTED_OPERATIONAL_V2_COUNTS = {
    "certified_campaign": 9,
    "accepted_operational_v1_packages": 650,
    "prior_reviews": 45,
    "manager_owned_state": 1,
}


class PreservationPolicyError(ValueError):
    pass


def _load_json(path: Path, label: str) -> Any:
    if not path.is_file():
        raise PreservationPolicyError(f"{label}: missing file {path}")
    with path.open() as handle:
        return json.load(handle)


def _canonical_relative(value: Any, label: str) -> PurePosixPath:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or value.endswith("/")
    ):
        raise PreservationPolicyError(
            f"{label}: expected a canonical relative POSIX path"
        )
    pure = PurePosixPath(value)
    if (
        pure.is_absolute()
        or pure.as_posix() != value
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        raise PreservationPolicyError(f"{label}: path is not canonical")
    return pure


def _resolve_path(
    value: Any,
    label: str,
    *,
    root: Path,
    file: bool,
) -> Path:
    pure = _canonical_relative(value, label)
    resolved_root = root.resolve()
    lexical = resolved_root.joinpath(*pure.parts)
    try:
        resolved = lexical.resolve(strict=True)
        resolved.relative_to(resolved_root)
    except (FileNotFoundError, ValueError) as exc:
        raise PreservationPolicyError(
            f"{label}: path is missing or escapes the policy root"
        ) from exc
    if resolved != lexical:
        raise PreservationPolicyError(
            f"{label}: symlink substitution is not permitted"
        )
    if file and not resolved.is_file():
        raise PreservationPolicyError(f"{label}: expected a regular file")
    if not file and not resolved.is_dir():
        raise PreservationPolicyError(f"{label}: expected a directory")
    return resolved


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _artifact_identity_path(
    record: dict[str, Any],
    live_path: Path,
    *,
    root: Path,
) -> Path:
    if (
        root.resolve() == OUT.resolve()
        and record == OPERATIONAL_V2_REVIEW_REQUEST_RECORD
    ):
        return _resolve_path(
            OPERATIONAL_V2_REVIEW_REQUEST_ARCHIVE.relative_to(OUT).as_posix(),
            "operational-v2 archived review request",
            root=root,
            file=True,
        )
    return live_path


def _validate_artifact_records(
    records: Any,
    label: str,
    *,
    root: Path = OUT,
    expected_count: int | None = None,
) -> list[Path]:
    if not isinstance(records, list):
        raise PreservationPolicyError(f"{label}: records must be a list")
    if expected_count is not None and len(records) != expected_count:
        raise PreservationPolicyError(
            f"{label}: expected {expected_count} records, got {len(records)}"
        )

    paths: list[str] = []
    resolved: list[Path] = []
    for index, record in enumerate(records):
        item_label = f"{label}[{index}]"
        if not isinstance(record, dict) or set(record) != {
            "path",
            "sha256",
            "bytes",
        }:
            raise PreservationPolicyError(
                f"{item_label}: malformed artifact record"
            )
        path = _resolve_path(
            record["path"], f"{item_label}.path", root=root, file=True
        )
        identity_path = _artifact_identity_path(record, path, root=root)
        expected_hash = record["sha256"]
        expected_bytes = record["bytes"]
        if (
            not isinstance(expected_hash, str)
            or len(expected_hash) != 64
            or any(character not in "0123456789abcdef" for character in expected_hash)
            or isinstance(expected_bytes, bool)
            or not isinstance(expected_bytes, int)
            or expected_bytes < 0
        ):
            raise PreservationPolicyError(
                f"{item_label}: malformed hash or byte count"
            )
        if (
            identity_path.stat().st_size != expected_bytes
            or _sha256(identity_path) != expected_hash
        ):
            raise PreservationPolicyError(
                f"{item_label}: artifact byte identity changed"
            )
        paths.append(record["path"])
        resolved.append(path)

    if len(paths) != len(set(paths)):
        raise PreservationPolicyError(f"{label}: duplicate path")
    if paths != sorted(paths, key=lambda value: PurePosixPath(value).parts):
        raise PreservationPolicyError(f"{label}: paths are not sorted")
    return resolved


def _inventory_sha256(records: list[dict[str, Any]]) -> str:
    return hashlib.sha256(
        json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _validate_exact_scope(
    scope_root: Any,
    records: list[dict[str, Any]],
    label: str,
    *,
    root: Path = OUT,
) -> None:
    directory = _resolve_path(
        scope_root, f"{label}.scope_root", root=root, file=False
    )
    actual = {
        path.relative_to(root.resolve()).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
    }
    expected = {record["path"] for record in records}
    if actual != expected:
        missing = sorted(expected - actual)
        added = sorted(actual - expected)
        raise PreservationPolicyError(
            f"{label}: scope membership changed; "
            f"missing={missing[:3]!r} added={added[:3]!r}"
        )


def _load_policy_payload() -> dict[str, Any]:
    payload = _load_json(POLICY_PATH, "preservation policy")
    expected_keys = {
        "schema_version",
        "policy_id",
        "policy",
        "review_scope_root",
        "historical_inventories",
        "registered_post_certification_additions",
    }
    if (
        not isinstance(payload, dict)
        or set(payload) != expected_keys
        or payload.get("schema_version") != 1
        or payload.get("policy_id") != POLICY_ID
    ):
        raise PreservationPolicyError("preservation policy identity is invalid")
    if payload.get("review_scope_root") != "review":
        raise PreservationPolicyError("review scope root is invalid")
    return payload


def _validate_source_artifact(
    config: Any,
    label: str,
    expected_path: Path,
    *,
    root: Path,
    extra_keys: set[str],
) -> Path:
    if not isinstance(config, dict) or set(config) != {"artifact", *extra_keys}:
        raise PreservationPolicyError(f"{label}: malformed inventory binding")
    paths = _validate_artifact_records(
        [config["artifact"]], f"{label}.artifact", root=root, expected_count=1
    )
    expected = root.resolve() / expected_path.relative_to(OUT)
    if paths[0] != expected:
        raise PreservationPolicyError(f"{label}: unexpected inventory path")
    return paths[0]


def _reject_cross_group_duplicates(
    groups: dict[str, list[dict[str, Any]]], label: str
) -> None:
    owners: dict[str, str] = {}
    for group, records in groups.items():
        for record in records:
            path = record["path"]
            if path in owners:
                raise PreservationPolicyError(
                    f"{label}: {path} occurs in both {owners[path]} and {group}"
                )
            owners[path] = group


def _validate_final_inventory(
    payload: dict[str, Any], *, root: Path
) -> dict[str, list[dict[str, Any]]]:
    inventories = payload["historical_inventories"]
    if not isinstance(inventories, dict) or set(inventories) != {
        "final_campaign",
        "operational_v2",
        "operational_v2_certification",
    }:
        raise PreservationPolicyError("historical inventory set is invalid")
    config = inventories["final_campaign"]
    path = _validate_source_artifact(
        config,
        "final campaign inventory",
        FINAL_BASELINE,
        root=root,
        extra_keys={"group_counts"},
    )
    if config["group_counts"] != EXPECTED_FINAL_COUNTS:
        raise PreservationPolicyError("final campaign count policy drifted")
    baseline = _load_json(path, "final campaign inventory")
    groups = baseline.get("groups") if isinstance(baseline, dict) else None
    if (
        baseline.get("schema_version") != 1
        or not isinstance(groups, dict)
        or set(groups) != set(EXPECTED_FINAL_COUNTS)
        or {name: len(records) for name, records in groups.items()}
        != EXPECTED_FINAL_COUNTS
    ):
        raise PreservationPolicyError(
            "final campaign historical inventory is malformed"
        )
    for group, expected_count in EXPECTED_FINAL_COUNTS.items():
        _validate_artifact_records(
            groups[group],
            f"final campaign {group}",
            root=root,
            expected_count=expected_count,
        )
    _reject_cross_group_duplicates(groups, "final campaign inventory")
    return groups


def _validate_operational_v2_inventory(
    payload: dict[str, Any],
    *,
    root: Path,
    validate_all_records: bool = True,
) -> dict[str, list[dict[str, Any]]]:
    config = payload["historical_inventories"]["operational_v2"]
    path = _validate_source_artifact(
        config,
        "operational-v2 inventory",
        OPERATIONAL_V2_MANIFEST,
        root=root,
        extra_keys={"group_counts", "prior_review_inventory_sha256"},
    )
    if config["group_counts"] != EXPECTED_OPERATIONAL_V2_COUNTS:
        raise PreservationPolicyError("operational-v2 count policy drifted")
    manifest = _load_json(path, "operational-v2 inventory")
    preservation = (
        manifest.get("preservation") if isinstance(manifest, dict) else None
    )
    groups = (
        preservation.get("groups")
        if isinstance(preservation, dict)
        else None
    )
    if (
        manifest.get("schema_version") != 2
        or not isinstance(groups, dict)
        or set(groups) != set(EXPECTED_OPERATIONAL_V2_COUNTS)
        or {name: len(records) for name, records in groups.items()}
        != EXPECTED_OPERATIONAL_V2_COUNTS
    ):
        raise PreservationPolicyError(
            "operational-v2 historical inventory is malformed"
        )
    groups_to_validate = (
        EXPECTED_OPERATIONAL_V2_COUNTS
        if validate_all_records
        else {"prior_reviews": EXPECTED_OPERATIONAL_V2_COUNTS["prior_reviews"]}
    )
    for group, expected_count in groups_to_validate.items():
        _validate_artifact_records(
            groups[group],
            f"operational-v2 {group}",
            root=root,
            expected_count=expected_count,
        )
    prior_reviews = groups["prior_reviews"]
    if (
        config["prior_review_inventory_sha256"]
        != _inventory_sha256(prior_reviews)
    ):
        raise PreservationPolicyError(
            "operational-v2 prior-review inventory digest changed"
        )
    return groups


def _validate_certification_inventory(
    payload: dict[str, Any], *, root: Path
) -> list[dict[str, Any]]:
    config = payload["historical_inventories"][
        "operational_v2_certification"
    ]
    path = _validate_source_artifact(
        config,
        "operational-v2 certification inventory",
        OPERATIONAL_V2_CERTIFIED_PROJECTION,
        root=root,
        extra_keys={"review_records"},
    )
    reviews = config["review_records"]
    _validate_artifact_records(
        reviews,
        "operational-v2 certification reviews",
        root=root,
        expected_count=1,
    )
    projection = _load_json(path, "operational-v2 certified projection")
    protected = (
        projection.get("protected_inputs", {}).get("groups", {})
        if isinstance(projection, dict)
        else {}
    )
    if (
        projection.get("schema_version") != 1
        or projection.get("status") != "certified"
        or protected.get("independent_operational_v2_review") != reviews
        or projection.get("independent_review", {}).get("artifact")
        != reviews[0]
    ):
        raise PreservationPolicyError(
            "operational-v2 certification review binding changed"
        )
    return reviews


def _validate_registered_additions(
    payload: dict[str, Any], *, root: Path
) -> dict[str, list[dict[str, Any]]]:
    additions = payload["registered_post_certification_additions"]
    if not isinstance(additions, dict) or set(additions) != {
        TARGET_078_ADDITION,
        TARGET_079_REVIEW_ADDITION,
    }:
        raise PreservationPolicyError(
            "registered post-certification addition set is invalid"
        )

    target_078 = additions[TARGET_078_ADDITION]
    if not isinstance(target_078, dict) or set(target_078) != {
        "scope_root",
        "file_count",
        "records",
    }:
        raise PreservationPolicyError(
            "target-078 addition registration is malformed"
        )
    if target_078["file_count"] != 142:
        raise PreservationPolicyError(
            "target-078 addition count policy drifted"
        )
    _validate_artifact_records(
        target_078["records"],
        "target-078 registered addition",
        root=root,
        expected_count=142,
    )
    _validate_exact_scope(
        target_078["scope_root"],
        target_078["records"],
        "target-078 registered addition",
        root=root,
    )

    target_079 = additions[TARGET_079_REVIEW_ADDITION]
    if not isinstance(target_079, dict) or set(target_079) != {
        "file_count",
        "records",
    }:
        raise PreservationPolicyError(
            "target-079 review registration is malformed"
        )
    if target_079["file_count"] != 1:
        raise PreservationPolicyError(
            "target-079 review count policy drifted"
        )
    _validate_artifact_records(
        target_079["records"],
        "target-079 registered review",
        root=root,
        expected_count=1,
    )
    return {
        TARGET_078_ADDITION: target_078["records"],
        TARGET_079_REVIEW_ADDITION: target_079["records"],
    }


def _validate_review_membership(
    historical: list[dict[str, Any]],
    certification: list[dict[str, Any]],
    registered: list[dict[str, Any]],
    *,
    root: Path,
) -> list[dict[str, Any]]:
    records = sorted(
        [*historical, *certification, *registered],
        key=lambda record: record["path"],
    )
    paths = [record["path"] for record in records]
    if len(paths) != len(set(paths)):
        raise PreservationPolicyError(
            "allowed review inventory contains duplicate paths"
        )
    review_root = _resolve_path(
        "review", "review scope root", root=root, file=False
    )
    actual = {
        path.relative_to(root.resolve()).as_posix()
        for path in review_root.rglob("*")
        if path.is_file()
    }
    if actual != set(paths):
        missing = sorted(set(paths) - actual)
        added = sorted(actual - set(paths))
        raise PreservationPolicyError(
            "review scope membership changed; "
            f"missing={missing[:3]!r} added={added[:3]!r}"
        )
    return records


def validate_policy_payload(
    payload: dict[str, Any], *, root: Path = OUT
) -> dict[str, Any]:
    final_groups = _validate_final_inventory(payload, root=root)
    operational_groups = _validate_operational_v2_inventory(
        payload, root=root
    )
    certification_reviews = _validate_certification_inventory(
        payload, root=root
    )
    additions = _validate_registered_additions(payload, root=root)
    reviews = _validate_review_membership(
        operational_groups["prior_reviews"],
        certification_reviews,
        additions[TARGET_079_REVIEW_ADDITION],
        root=root,
    )
    return {
        "final_campaign_groups": copy.deepcopy(final_groups),
        "operational_v2_groups": copy.deepcopy(operational_groups),
        "registered_additions": copy.deepcopy(additions),
        "allowed_reviews": copy.deepcopy(reviews),
    }


def validate_policy() -> dict[str, Any]:
    return validate_policy_payload(_load_policy_payload())


def _validated_review_inventory(
    payload: dict[str, Any], *, root: Path
) -> dict[str, list[dict[str, Any]]]:
    operational_groups = _validate_operational_v2_inventory(
        payload,
        root=root,
        validate_all_records=False,
    )
    certification_reviews = _validate_certification_inventory(
        payload, root=root
    )
    additions = _validate_registered_additions(payload, root=root)
    allowed = _validate_review_membership(
        operational_groups["prior_reviews"],
        certification_reviews,
        additions[TARGET_079_REVIEW_ADDITION],
        root=root,
    )
    return {
        "historical": copy.deepcopy(operational_groups["prior_reviews"]),
        "allowed": copy.deepcopy(allowed),
    }


def _actual_final_group_paths(
    target_078_registered: set[Path],
) -> dict[str, set[str]]:
    excluded_crosswalk = {
        *(path.resolve() for path in AGGREGATE_CROSSWALKS),
        *(path.resolve() for path in OPERATIONAL_ADDENDA),
    }
    groups: dict[str, list[Path]] = {
        "preexisting_evidence": [
            path
            for path in (OUT / "evidence").rglob("*")
            if (
                path.is_file()
                and FINAL_ROOT not in path.parents
                and TARGET_078_OPERATIONAL_EVIDENCE not in path.parents
                and TARGET_079_OPERATIONAL_EVIDENCE not in path.parents
                and TARGET_079_ADAPTER_EVIDENCE not in path.parents
                and path.resolve() not in target_078_registered
            )
        ],
        "frozen_inputs": [
            path
            for path in (OUT / "provenance/frozen").rglob("*")
            if path.is_file()
        ],
        "authority_ledgers": [
            path
            for path in (OUT / "crosswalk").glob("*")
            if path.is_file() and path.resolve() not in excluded_crosswalk
        ],
        "accepted_incremental_reviews": list(
            (OUT / "review").glob("REVIEW_ACCEPTANCE_*.md")
        ),
    }
    return {
        name: {common.relpath(path) for path in paths}
        for name, paths in groups.items()
    }


def final_campaign_groups() -> dict[str, list[dict[str, Any]]]:
    payload = _load_policy_payload()
    groups = _validate_final_inventory(payload, root=OUT)
    additions = _validate_registered_additions(payload, root=OUT)
    _validated_review_inventory(payload, root=OUT)
    registered = {
        (OUT / record["path"]).resolve()
        for record in additions[TARGET_078_ADDITION]
    }
    actual = _actual_final_group_paths(registered)
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
    return _validated_review_inventory(_load_policy_payload(), root=OUT)


def historical_review_paths() -> list[Path]:
    return [
        OUT / record["path"] for record in review_inventory()["historical"]
    ]


def historical_review_digest(root: Path = REVIEW_ROOT) -> str:
    expected_root = REVIEW_ROOT.resolve()
    if root.resolve() != expected_root:
        raise PreservationPolicyError(
            "historical review digest root is not the registered review scope"
        )
    records = review_inventory()["historical"]
    digest = hashlib.sha256()
    for record in records:
        path = OUT / record["path"]
        identity_path = _artifact_identity_path(
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
    payload = _load_policy_payload()
    _validate_registered_additions(payload, root=OUT)
