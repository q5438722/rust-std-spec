#!/usr/bin/env python3
"""Validate the additive target-078 v3 preservation policy successor."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import preservation_policy_v1 as parent


OUT = common.OUT
POLICY_PATH = OUT / "preservation/path_policy_v2.json"
PARENT_POLICY_PATH = OUT / "preservation/path_policy_v1.json"
TARGET_078_V3_EVIDENCE = (
    OUT / "evidence/target_078_insert_tail_refinement_v3"
)
REVIEW_ROOT = OUT / "review"

POLICY_ID = "slice-preservation-path-policy-v2"
PARENT_POLICY_ID = parent.POLICY_ID
TARGET_078_V3_ADDITION = "target_078_insert_tail_refinement_v3"
TARGET_078_V3_REVIEW_ADDITION = (
    "target_078_insert_tail_refinement_v3_review"
)
EXPECTED_PARENT_POLICY_SHA256 = (
    "6f625f9808170c354ef5a6d5a68142989538dedb6677ac95264a2e7ffc0c4619"
)
EXPECTED_PARENT_POLICY_BYTES = 37965
PreservationPolicyError = parent.PreservationPolicyError


def _artifact(path: Path, *, root: Path = OUT) -> dict[str, Any]:
    if not path.is_file():
        raise PreservationPolicyError(
            f"cannot register missing preservation artifact: {path}"
        )
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": parent._sha256(path),
        "bytes": path.stat().st_size,
    }


def _registration_records(
    *,
    root: Path = OUT,
    evidence: Path = TARGET_078_V3_EVIDENCE,
) -> list[dict[str, Any]]:
    if not evidence.is_dir():
        raise PreservationPolicyError(
            f"target-078 v3 evidence is missing: {evidence}"
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
                "*TARGET_078_INSERT_TAIL_REFINEMENT_V3*.md"
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
            "path_policy_v1 remains authoritative and byte-identical. "
            "This successor adds the closed target-078 insert_tail "
            "refinement v3 evidence scope and an explicit lane for its "
            "independent review artifacts."
        ),
        "registered_post_v1_additions": {
            TARGET_078_V3_ADDITION: {
                "scope_root": TARGET_078_V3_EVIDENCE.relative_to(
                    OUT
                ).as_posix(),
                "file_count": len(records),
                "records": records,
            },
            TARGET_078_V3_REVIEW_ADDITION: {
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
        "registered_post_v1_additions",
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
    additions = payload["registered_post_v1_additions"]
    if not isinstance(additions, dict) or set(additions) != {
        TARGET_078_V3_ADDITION,
        TARGET_078_V3_REVIEW_ADDITION,
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
    additions = _registered_additions(payload)
    config = additions[TARGET_078_V3_ADDITION]
    if not isinstance(config, dict) or set(config) != {
        "scope_root",
        "file_count",
        "records",
    }:
        raise PreservationPolicyError(
            "target-078 v3 registration is malformed"
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
            "target-078 v3 registration count is invalid"
        )
    parent._validate_artifact_records(
        records,
        "target-078 v3 registered addition",
        root=root,
        expected_count=count,
    )
    parent._validate_exact_scope(
        config["scope_root"],
        records,
        "target-078 v3 registered addition",
        root=root,
    )
    expected_scope = TARGET_078_V3_EVIDENCE.relative_to(OUT).as_posix()
    if config["scope_root"] != expected_scope:
        raise PreservationPolicyError(
            "target-078 v3 registration scope changed"
        )
    return records


def _validate_review_registration(
    payload: dict[str, Any],
    *,
    root: Path = OUT,
) -> list[dict[str, Any]]:
    additions = _registered_additions(payload)
    config = additions[TARGET_078_V3_REVIEW_ADDITION]
    if not isinstance(config, dict) or set(config) != {
        "file_count",
        "records",
    }:
        raise PreservationPolicyError(
            "target-078 v3 review registration is malformed"
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
            "target-078 v3 review registration count is invalid"
        )
    parent._validate_artifact_records(
        records,
        "target-078 v3 registered reviews",
        root=root,
        expected_count=count,
    )
    for record in records:
        path = Path(record["path"])
        if (
            path.parent.as_posix() != "review"
            or "TARGET_078_INSERT_TAIL_REFINEMENT_V3" not in path.name
            or path.suffix != ".md"
        ):
            raise PreservationPolicyError(
                "target-078 v3 review path is outside its additive lane"
            )
    return records


def _validate_legacy_policy(
    extra_reviews: list[dict[str, Any]],
    *,
    validate_all_operational_records: bool = True,
) -> dict[str, Any]:
    payload = parent._load_policy_payload()
    final_groups = parent._validate_final_inventory(payload, root=OUT)
    operational_groups = parent._validate_operational_v2_inventory(
        payload,
        root=OUT,
        validate_all_records=validate_all_operational_records,
    )
    certification_reviews = parent._validate_certification_inventory(
        payload, root=OUT
    )
    additions = parent._validate_registered_additions(payload, root=OUT)
    allowed_reviews = parent._validate_review_membership(
        operational_groups["prior_reviews"],
        certification_reviews,
        [
            *additions[parent.TARGET_079_REVIEW_ADDITION],
            *extra_reviews,
        ],
        root=OUT,
    )
    return {
        "final_campaign_groups": copy.deepcopy(final_groups),
        "operational_v2_groups": copy.deepcopy(operational_groups),
        "registered_additions": copy.deepcopy(additions),
        "allowed_reviews": copy.deepcopy(allowed_reviews),
    }


def validate_parent_binding(
    payload: dict[str, Any] | None = None,
    *,
    root: Path = OUT,
    validate_all_operational_records: bool = True,
) -> dict[str, Any]:
    if payload is None:
        payload = _load_policy_payload()
    if root.resolve() != OUT.resolve():
        raise PreservationPolicyError(
            "additive policy must validate against the campaign root"
        )
    parent_record = payload["parent_policy"]
    resolved = parent._validate_artifact_records(
        [parent_record],
        "parent preservation policy",
        root=root,
        expected_count=1,
    )
    if resolved[0] != PARENT_POLICY_PATH.resolve():
        raise PreservationPolicyError(
            "additive policy does not bind path_policy_v1.json"
        )
    if (
        parent_record["sha256"] != EXPECTED_PARENT_POLICY_SHA256
        or parent_record["bytes"] != EXPECTED_PARENT_POLICY_BYTES
    ):
        raise PreservationPolicyError(
            "path_policy_v1.json immutable identity changed"
        )
    review_additions = _validate_review_registration(payload, root=root)
    legacy = _validate_legacy_policy(
        review_additions,
        validate_all_operational_records=(
            validate_all_operational_records
        ),
    )
    return {
        "policy_id": POLICY_ID,
        "parent_policy_id": PARENT_POLICY_ID,
        "parent_policy": copy.deepcopy(parent_record),
        "legacy": copy.deepcopy(legacy),
        "review_additions": copy.deepcopy(review_additions),
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
        "legacy": binding["legacy"],
        "registered_additions": {
            TARGET_078_V3_ADDITION: copy.deepcopy(additions),
            TARGET_078_V3_REVIEW_ADDITION: copy.deepcopy(
                binding["review_additions"]
            ),
        },
        "allowed_reviews": copy.deepcopy(
            binding["legacy"]["allowed_reviews"]
        ),
    }


def validate_policy() -> dict[str, Any]:
    return validate_policy_payload(_load_policy_payload())


def final_campaign_groups() -> dict[str, list[dict[str, Any]]]:
    validated = validate_policy_payload(
        _load_policy_payload(),
        validate_all_operational_records=False,
    )
    groups = validated["legacy"]["final_campaign_groups"]
    legacy_additions = validated["legacy"]["registered_additions"]
    current = validated["registered_additions"][TARGET_078_V3_ADDITION]
    excluded = {
        (OUT / record["path"]).resolve()
        for record in (
            *legacy_additions[parent.TARGET_078_ADDITION],
            *current,
        )
    }
    actual = parent._actual_final_group_paths(excluded)
    actual["accepted_incremental_reviews"] -= {
        record["path"]
        for record in validated["registered_additions"][
            TARGET_078_V3_REVIEW_ADDITION
        ]
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


def _validated_review_inventory() -> dict[str, list[dict[str, Any]]]:
    payload = _load_policy_payload()
    parent_record = payload["parent_policy"]
    resolved = parent._validate_artifact_records(
        [parent_record],
        "parent preservation policy",
        root=OUT,
        expected_count=1,
    )
    if (
        resolved[0] != PARENT_POLICY_PATH.resolve()
        or parent_record["sha256"] != EXPECTED_PARENT_POLICY_SHA256
        or parent_record["bytes"] != EXPECTED_PARENT_POLICY_BYTES
    ):
        raise PreservationPolicyError(
            "path_policy_v1.json immutable identity changed"
        )
    extra_reviews = _validate_review_registration(payload, root=OUT)
    parent_payload = parent._load_policy_payload()
    operational_groups = parent._validate_operational_v2_inventory(
        parent_payload,
        root=OUT,
        validate_all_records=False,
    )
    certification_reviews = parent._validate_certification_inventory(
        parent_payload, root=OUT
    )
    additions = parent._validate_registered_additions(
        parent_payload, root=OUT
    )
    allowed = parent._validate_review_membership(
        operational_groups["prior_reviews"],
        certification_reviews,
        [
            *additions[parent.TARGET_079_REVIEW_ADDITION],
            *extra_reviews,
        ],
        root=OUT,
    )
    return {
        "historical": copy.deepcopy(
            operational_groups["prior_reviews"]
        ),
        "allowed": copy.deepcopy(allowed),
    }


def review_inventory() -> dict[str, list[dict[str, Any]]]:
    return _validated_review_inventory()


def historical_review_paths() -> list[Path]:
    return [
        OUT / record["path"] for record in review_inventory()["historical"]
    ]


def historical_review_digest(root: Path = parent.REVIEW_ROOT) -> str:
    if root.resolve() != REVIEW_ROOT.resolve():
        raise PreservationPolicyError(
            "historical review digest root is not the registered review scope"
        )
    digest = hashlib.sha256()
    for record in review_inventory()["historical"]:
        path = OUT / record["path"]
        identity_path = parent._artifact_identity_path(
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
        raise SystemExit("usage: preservation_policy_v2.py [--write]")
    validated = validate_policy()
    count = len(validated["registered_additions"][TARGET_078_V3_ADDITION])
    reviews = len(
        validated["registered_additions"][
            TARGET_078_V3_REVIEW_ADDITION
        ]
    )
    print("preservation_policy_v2=PASS")
    print(f"target_078_v3_files={count}")
    print(f"target_078_v3_reviews={reviews}")


if __name__ == "__main__":
    main(sys.argv[1:])
