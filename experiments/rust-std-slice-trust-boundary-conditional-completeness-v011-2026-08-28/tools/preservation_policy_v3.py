#!/usr/bin/env python3
"""Compatibility entry point for the accepted v3-v7 preservation chain."""

from __future__ import annotations

from pathlib import Path


_ROOT = Path(__file__).resolve().parents[1]
_ARCHIVED = (
    _ROOT / "preservation/archive_v2/tools/preservation_policy_v3.py"
)
_MODULE_NAME = __name__
__name__ = "_preservation_policy_v3_accepted"
exec(compile(_ARCHIVED.read_bytes(), str(Path(__file__)), "exec"), globals())
__name__ = _MODULE_NAME

_accepted_validate_target_081_v6 = _validate_target_081_v6
_accepted_artifact_identity_path = base._artifact_identity_path


def _artifact_identity_path(
    record: dict[str, Any],
    live_path: Path,
    *,
    root: Path,
) -> Path:
    """Resolve authority capture drift only through path_policy_v8."""

    v8_path = root / "preservation/path_policy_v8.json"
    if v8_path.is_file():
        import preservation_policy_v8

        archived = preservation_policy_v8.historical_identity_path(
            record, live_path, root=root
        )
        if archived is not None:
            return archived
    return _accepted_artifact_identity_path(
        record, live_path, root=root
    )


base._artifact_identity_path = _artifact_identity_path


def _validate_target_081_v6(
    payload: dict[str, Any],
    v5_payload: dict[str, Any],
    *,
    root: Path,
) -> dict[str, Any]:
    """Resolve v6 live-path replacements only through path_policy_v8."""

    v8_path = root / "preservation/path_policy_v8.json"
    if not v8_path.is_file():
        return _accepted_validate_target_081_v6(
            payload, v5_payload, root=root
        )
    import preservation_policy_v8

    return preservation_policy_v8.validate_target_081_v6(
        payload, v5_payload, root=root
    )


def final_campaign_groups() -> dict[str, list[dict[str, Any]]]:
    """Keep v8 additions outside the already certified campaign groups."""

    import preservation_policy_v8

    validated = validate_policy_payload(
        _load_policy_payload(),
        validate_all_operational_records=False,
    )
    target_082 = preservation_policy_v8.target_082_lifecycle()
    chain = validated["parent_chain"]
    groups = chain["final_campaign_groups"]
    current = validated["registered_additions"][TARGET_079_V3_ADDITION]
    target_080 = validated["target_080_lifecycle"][
        "registered_records"
    ]
    target_081_state = validated["target_081_lifecycle"]
    target_081 = target_081_state["registered_records"]
    excluded = {
        (OUT / record["path"]).resolve()
        for record in (
            *chain["legacy_additions"][base.TARGET_078_ADDITION],
            *chain["parent_addition"],
            *current,
            *target_080,
            *target_081,
            *target_082["registered_records"],
        )
    }
    actual = base._actual_final_group_paths(excluded)
    actual["authority_ledgers"] -= {
        record["path"]
        for record in (
            *validated["target_080_lifecycle"][
                "registered_addenda"
            ].values(),
            *target_081_state["registered_addenda"].values(),
            *target_082["registered_addenda"].values(),
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


if __name__ == "__main__":
    main(sys.argv[1:])
