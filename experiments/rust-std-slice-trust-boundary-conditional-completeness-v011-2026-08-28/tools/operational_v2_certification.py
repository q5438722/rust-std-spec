#!/usr/bin/env python3
"""Certify the independently accepted operational-v2 reconciliation."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import campaign_common as common
import operational_v2_reconciliation as v2


OUT = common.OUT
VERSION = "operational-v2"
KIND = "operational-v2-certified-projection"

REVIEW_PATH = (
    OUT / "review/REVIEW_OPERATIONAL_V2_RECONCILIATION_ACCEPTANCE.md"
)
CERTIFIED_ROOT = v2.V2_ROOT / "certified"
CERTIFIED_PROJECTION = CERTIFIED_ROOT / "certified_projection.json"
CERTIFIED_REPORT = CERTIFIED_ROOT / "certified_projection.md"
CERTIFICATION_MANIFEST = CERTIFIED_ROOT / "certification_manifest.json"

EXPECTED_COUNTS = {
    "exact_output_determinism": copy.deepcopy(v2.EXPECTED_V2_EXACT),
    "completeness_modulo_reviewed_equivalence": copy.deepcopy(
        v2.EXPECTED_V2_FULL
    ),
}
EXPECTED_SCOPE = {
    "module": "core::slice",
    "generated_slice_contracts": 120,
    "selected_r0_unknown": 62,
    "active_r0_unsat_excluded": 58,
    "exact_vstd_excluded": 12,
}
EXPECTED_ROW_PROJECTION_SHA256 = (
    "ef5bfdef97524ceb06c409e0277758136f4417294f94d24f5eb56c7152e55875"
)
EXPECTED_REVIEW_TIMESTAMP = "2026-09-01T22:41:27Z"

V2_PATHS = {
    "crosswalk_json": v2.V2_CROSSWALK_JSON,
    "crosswalk_csv": v2.V2_CROSSWALK_CSV,
    "reconciliation_manifest": v2.V2_MANIFEST,
    "results_dossier_json": v2.V2_DOSSIER_JSON,
    "results_dossier_markdown": v2.V2_DOSSIER_MD,
}
EXPECTED_V2_ARTIFACTS = {
    "crosswalk_json": {
        "path": "crosswalk/conditional_obligation_crosswalk_operational_v2.json",
        "sha256": (
            "e403de493f47b1d6ec5f9eb8d4932b9683b548070b7c5b80a16b31899d00b4bd"
        ),
        "bytes": 3209635,
    },
    "crosswalk_csv": {
        "path": "crosswalk/conditional_obligation_crosswalk_operational_v2.csv",
        "sha256": (
            "d8be49ebfa8e441d88c26a6f99784d74d04edbd8719a250a2feaf4e7ec5d85aa"
        ),
        "bytes": 22169,
    },
    "reconciliation_manifest": {
        "path": (
            "evidence/final_campaign/operational_v2/reconciliation_manifest.json"
        ),
        "sha256": (
            "e1aae7438ed00d02ba54f7525de278545d3472a6c4dcd989541cc5f572985518"
        ),
        "bytes": 162449,
    },
    "results_dossier_json": {
        "path": "evidence/final_campaign/operational_v2/results_dossier.json",
        "sha256": (
            "0b4e2fa51716b55aae7e01cc61e01e0c9c1dcb9853c20b909435d8ef42210033"
        ),
        "bytes": 19829,
    },
    "results_dossier_markdown": {
        "path": "evidence/final_campaign/operational_v2/results_dossier.md",
        "sha256": (
            "8d949d1fb282b2b5010d6212188519141f63f42bdfbac0074118769a7102b3b2"
        ),
        "bytes": 1875,
    },
}
EXPECTED_REVIEW_ARTIFACT = {
    "path": "review/REVIEW_OPERATIONAL_V2_RECONCILIATION_ACCEPTANCE.md",
    "sha256": (
        "499209677f1fde841309d1b0e42d46450f2510096bd3e5d339417078d2426319"
    ),
    "bytes": 3517,
}

BASE_PROTECTION_GROUPS = {
    "certified_campaign",
    "accepted_operational_v1_packages",
    "prior_reviews",
    "manager_owned_state",
}
PROTECTION_GROUPS = BASE_PROTECTION_GROUPS | {
    "accepted_operational_v2_package",
    "independent_operational_v2_review",
}


class OperationalV2CertificationError(ValueError):
    pass


def _display_path(path: Path) -> str:
    try:
        return common.relpath(path)
    except ValueError:
        return str(path)


def _load_json(path: Path, label: str) -> Any:
    try:
        with path.open() as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise OperationalV2CertificationError(
            f"{label}: missing file {_display_path(path)}"
        ) from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise OperationalV2CertificationError(
            f"{label}: malformed or unreadable JSON"
        ) from exc


def _read_text(path: Path, label: str) -> str:
    try:
        return path.read_text()
    except FileNotFoundError as exc:
        raise OperationalV2CertificationError(
            f"{label}: missing file {_display_path(path)}"
        ) from exc
    except (OSError, UnicodeError) as exc:
        raise OperationalV2CertificationError(
            f"{label}: malformed or unreadable text"
        ) from exc


def _artifact(path: Path) -> dict[str, Any]:
    return {
        "path": common.relpath(path),
        "sha256": common.sha256(path),
        "bytes": path.stat().st_size,
    }


def _validate_expected_artifact(
    path: Path, expected: Any, label: str
) -> dict[str, Any]:
    if not path.is_file():
        raise OperationalV2CertificationError(
            f"{label}: missing file {_display_path(path)}"
        )
    if (
        not isinstance(expected, dict)
        or set(expected) != {"path", "sha256", "bytes"}
        or expected["path"] != common.relpath(path)
        or expected["sha256"] != common.sha256(path)
        or expected["bytes"] != path.stat().st_size
    ):
        raise OperationalV2CertificationError(
            f"{label}: accepted artifact identity drifted"
        )
    return copy.deepcopy(expected)


def _parse_accept_review(text: Any) -> dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        raise OperationalV2CertificationError(
            "operational-v2 review: malformed review"
        )
    verdicts = re.findall(
        r"^\*\*VERDICT: ([A-Z]+)\*\*$", text, flags=re.MULTILINE
    )
    if verdicts != ["ACCEPT"]:
        raise OperationalV2CertificationError(
            "operational-v2 review: verdict is not one unambiguous ACCEPT"
        )
    if (
        text.count(
            "# Independent Reviewer decision: operational-v2 reconciliation"
        )
        != 1
    ):
        raise OperationalV2CertificationError(
            "operational-v2 review: wrong or ambiguous review scope"
        )
    timestamps = re.findall(
        r"^\*\*Timestamp:\*\* ([0-9]{4}-[0-9]{2}-[0-9]{2}"
        r"T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)$",
        text,
        flags=re.MULTILINE,
    )
    if len(timestamps) != 1:
        raise OperationalV2CertificationError(
            "operational-v2 review: missing or malformed timestamp"
        )
    try:
        parsed_timestamp = datetime.fromisoformat(
            timestamps[0].replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise OperationalV2CertificationError(
            "operational-v2 review: invalid timestamp"
        ) from exc
    if parsed_timestamp.utcoffset() is None:
        raise OperationalV2CertificationError(
            "operational-v2 review: timestamp is not timezone-qualified"
        )

    normalized = " ".join(text.split())
    scope_sentence = (
        "This decision covers only the additive operational-v2 "
        "reconciliation of the certified 62-row Slice campaign."
    )
    if scope_sentence not in normalized:
        raise OperationalV2CertificationError(
            "operational-v2 review: wrong or missing bounded scope"
        )
    summaries = list(
        re.finditer(
            r"The reconciliation reports ([0-9]+) rows, overlays "
            r"`([0-9,]+)`, exact counts `([0-9]+)/([0-9]+)/([0-9]+)`, "
            r"reviewed-equivalence counts `([0-9]+)/([0-9]+)/([0-9]+)`, "
            r"and zero missing classifications\.",
            normalized,
        )
    )
    if len(summaries) != 1:
        raise OperationalV2CertificationError(
            "operational-v2 review: expected exactly one count-bearing "
            "acceptance summary"
        )
    summary = summaries[0]
    row_count = int(summary.group(1))
    overlay_orders = summary.group(2).split(",")
    exact = {
        "conditional-complete": int(summary.group(3)),
        "conditional-incomplete": int(summary.group(4)),
        "missing-source-backed-model": int(summary.group(5)),
    }
    full = {
        "conditional-complete": int(summary.group(6)),
        "conditional-incomplete": int(summary.group(7)),
        "missing-source-backed-model": int(summary.group(8)),
    }
    if (
        row_count != 62
        or overlay_orders != ["78", "79"]
        or exact != EXPECTED_COUNTS["exact_output_determinism"]
        or full
        != EXPECTED_COUNTS[
            "completeness_modulo_reviewed_equivalence"
        ]
    ):
        raise OperationalV2CertificationError(
            "operational-v2 review: accepted scope or counts are inconsistent"
        )
    if (
        "The bounded operational-v2 objective and its independent Reviewer "
        "gate are satisfied." not in normalized
        or "Manager-owned stage transition remains disabled." not in normalized
    ):
        raise OperationalV2CertificationError(
            "operational-v2 review: acceptance or stage scope is incomplete"
        )
    return {
        "required": True,
        "status": "accepted",
        "verdict": "ACCEPT",
        "timestamp": timestamps[0],
        "scope": "additive-operational-v2-reconciliation",
        "row_count": row_count,
        "overlay_orders": overlay_orders,
        "classification_counts": copy.deepcopy(EXPECTED_COUNTS),
        "stage_transition": "disabled",
    }


def _load_accept_review() -> dict[str, Any]:
    artifact = _validate_expected_artifact(
        REVIEW_PATH,
        EXPECTED_REVIEW_ARTIFACT,
        "operational-v2 independent review",
    )
    review = _parse_accept_review(
        _read_text(REVIEW_PATH, "operational-v2 independent review")
    )
    review["artifact"] = artifact
    return review


def _row_projection(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "input_order": row["input_order"],
            "target": row["target"],
            "semantic_family": row["semantic_family"],
            "active_contract_sha256": row["active_contract_sha256"],
            "effective_classification": copy.deepcopy(
                row["effective_classification"]
            ),
            "classification_source_kind": row["classification_source"][
                "kind"
            ],
        }
        for row in payload["rows"]
    ]


def _projection_digest(rows: list[dict[str, Any]]) -> str:
    encoded = json.dumps(
        rows, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _counts(
    rows: list[dict[str, Any]], field: str
) -> dict[str, int]:
    observed = Counter(
        row["effective_classification"][field] for row in rows
    )
    return {
        name: observed[name]
        for name in v2.CLASSIFICATIONS
    }


def _validate_candidate_crosswalk(payload: Any) -> list[dict[str, Any]]:
    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != 2
        or payload.get("campaign_version") != VERSION
        or payload.get("status") != "ready-for-independent-review"
        or payload.get("independent_review")
        != {
            "required": True,
            "status": "pending",
            "stage_transition": "disabled",
        }
    ):
        raise OperationalV2CertificationError(
            "operational-v2 crosswalk identity or pre-review status drifted"
        )
    authority = payload.get("authority_scope")
    if not isinstance(authority, dict) or {
        key: authority.get(key)
        for key in (
            "generated_slice_contracts",
            "selected_r0_unknown",
            "active_r0_unsat_excluded",
            "exact_vstd_excluded",
        )
    } != {
        key: EXPECTED_SCOPE[key]
        for key in (
            "generated_slice_contracts",
            "selected_r0_unknown",
            "active_r0_unsat_excluded",
            "exact_vstd_excluded",
        )
    }:
        raise OperationalV2CertificationError(
            "operational-v2 authority scope drifted"
        )
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 62:
        raise OperationalV2CertificationError(
            "operational-v2 crosswalk must contain exactly 62 rows"
        )
    orders: list[str] = []
    targets: list[str] = []
    overlay_orders: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise OperationalV2CertificationError(
                "operational-v2 crosswalk contains a malformed row"
            )
        order = row.get("input_order")
        target = row.get("target")
        baseline = row.get("campaign_row")
        classification = row.get("effective_classification")
        source = row.get("classification_source")
        active_hash = row.get("active_contract_sha256")
        if (
            not isinstance(order, str)
            or not order.isdigit()
            or str(int(order)) != order
            or not isinstance(target, str)
            or not target.startswith("core::slice::")
            or not isinstance(row.get("semantic_family"), str)
            or re.fullmatch(r"[0-9a-f]{64}", str(active_hash)) is None
            or not isinstance(baseline, dict)
            or baseline.get("input_order") != order
            or baseline.get("target") != target
            or baseline.get("authority", {}).get(
                "active_contract_sha256"
            )
            != active_hash
            or not isinstance(classification, dict)
            or set(classification) != {v2.EXACT_FIELD, v2.FULL_FIELD}
            or any(
                value not in v2.CLASSIFICATIONS
                for value in classification.values()
            )
            or not isinstance(source, dict)
        ):
            raise OperationalV2CertificationError(
                f"operational-v2 row {order!r}: identity or classification drift"
            )
        if order in v2.OVERLAY_SPECS:
            overlay_orders.add(order)
            if (
                target != v2.OVERLAY_SPECS[order]["target"]
                or source.get("kind")
                != "accepted-operational-v1-overlay"
                or classification
                != {
                    v2.EXACT_FIELD: "conditional-complete",
                    v2.FULL_FIELD: "conditional-complete",
                }
            ):
                raise OperationalV2CertificationError(
                    f"operational-v2 row {order}: overlay identity drifted"
                )
        elif (
            source.get("kind") != "certified-baseline"
            or classification != baseline.get("classification")
        ):
            raise OperationalV2CertificationError(
                f"operational-v2 row {order}: baseline projection drifted"
            )
        orders.append(order)
        targets.append(target)
    if (
        len(set(orders)) != 62
        or len(set(targets)) != 62
        or orders != sorted(orders, key=int)
        or overlay_orders != set(v2.OVERLAY_SPECS)
        or payload.get("overlay_orders") != ["78", "79"]
    ):
        raise OperationalV2CertificationError(
            "operational-v2 row ordering, uniqueness, or overlay scope drifted"
        )
    projected = _row_projection(payload)
    if _projection_digest(projected) != EXPECTED_ROW_PROJECTION_SHA256:
        raise OperationalV2CertificationError(
            "operational-v2 certified row projection drifted"
        )
    observed_counts = {
        "exact_output_determinism": _counts(projected, v2.EXACT_FIELD),
        "completeness_modulo_reviewed_equivalence": _counts(
            projected, v2.FULL_FIELD
        ),
    }
    if (
        observed_counts != EXPECTED_COUNTS
        or payload.get("classification_counts") != EXPECTED_COUNTS
        or payload.get("missing_source_backed_model_orders") != []
    ):
        raise OperationalV2CertificationError(
            "operational-v2 row or recorded classification counts drifted"
        )
    return projected


def _validate_candidate_bundle() -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, list[dict[str, Any]]],
]:
    artifacts = {
        name: _validate_expected_artifact(
            V2_PATHS[name],
            EXPECTED_V2_ARTIFACTS[name],
            f"accepted operational-v2 {name}",
        )
        for name in V2_PATHS
    }
    try:
        v2.validate_written_artifacts()
    except (OSError, ValueError, v2.OperationalV2Error) as exc:
        raise OperationalV2CertificationError(
            "operational-v2 package failed its native validation"
        ) from exc

    crosswalk = _load_json(
        v2.V2_CROSSWALK_JSON, "operational-v2 crosswalk"
    )
    rows = _validate_candidate_crosswalk(crosswalk)
    dossier = _load_json(v2.V2_DOSSIER_JSON, "operational-v2 dossier")
    manifest = _load_json(v2.V2_MANIFEST, "operational-v2 manifest")
    expected_review_state = {
        "required": True,
        "status": "pending",
        "stage_transition": "disabled",
    }
    for label, payload in (("dossier", dossier), ("manifest", manifest)):
        if (
            not isinstance(payload, dict)
            or payload.get("schema_version") != 2
            or payload.get("campaign_version") != VERSION
            or payload.get("status") != "ready-for-independent-review"
            or payload.get("row_count") != 62
            or payload.get("classification_counts") != EXPECTED_COUNTS
            or payload.get("missing_source_backed_model_orders") != []
            or payload.get("independent_review") != expected_review_state
        ):
            raise OperationalV2CertificationError(
                f"operational-v2 {label} identity or counts drifted"
            )
    if dossier.get("crosswalk") != {
        "json": artifacts["crosswalk_json"],
        "csv": artifacts["crosswalk_csv"],
    }:
        raise OperationalV2CertificationError(
            "operational-v2 dossier crosswalk binding drifted"
        )
    if (
        manifest.get("overlay_orders") != ["78", "79"]
        or manifest.get("dossier_status")
        != "ready-for-independent-review"
        or manifest.get("artifacts")
        != {
            "operational_v2_crosswalk_json": artifacts["crosswalk_json"],
            "operational_v2_crosswalk_csv": artifacts["crosswalk_csv"],
            "results_dossier_json": artifacts["results_dossier_json"],
            "results_dossier_markdown": artifacts[
                "results_dossier_markdown"
            ],
        }
    ):
        raise OperationalV2CertificationError(
            "operational-v2 reconciliation manifest binding drifted"
        )
    groups = manifest.get("preservation", {}).get("groups")
    try:
        v2._validate_preservation_groups(groups)
    except (OSError, ValueError, v2.OperationalV2Error) as exc:
        raise OperationalV2CertificationError(
            "operational-v2 protected-input inventory drifted"
        ) from exc
    if v2._snapshot_preserved_files() != groups:
        raise OperationalV2CertificationError(
            "operational-v2 protected files changed"
        )
    return crosswalk, rows, artifacts, copy.deepcopy(groups)


def _validate_protected_groups(groups: Any) -> None:
    if not isinstance(groups, dict) or set(groups) != PROTECTION_GROUPS:
        raise OperationalV2CertificationError(
            "certification protected-file groups are malformed"
        )
    base = {name: groups[name] for name in BASE_PROTECTION_GROUPS}
    try:
        v2._validate_preservation_groups(base)
    except (OSError, ValueError, v2.OperationalV2Error) as exc:
        raise OperationalV2CertificationError(
            "certification inherited protected-file inventory drifted"
        ) from exc
    if v2._snapshot_preserved_files() != base:
        raise OperationalV2CertificationError(
            "certification inherited protected files changed"
        )
    expected_package = [
        EXPECTED_V2_ARTIFACTS[name] for name in V2_PATHS
    ]
    if groups["accepted_operational_v2_package"] != expected_package:
        raise OperationalV2CertificationError(
            "accepted operational-v2 protection inventory drifted"
        )
    if groups["independent_operational_v2_review"] != [
        EXPECTED_REVIEW_ARTIFACT
    ]:
        raise OperationalV2CertificationError(
            "operational-v2 review protection inventory drifted"
        )
    for name, records in groups.items():
        if not isinstance(records, list) or not records:
            raise OperationalV2CertificationError(
                f"certification protection group {name} is empty"
            )
        for index, record in enumerate(records):
            if not isinstance(record, dict) or set(record) != {
                "path",
                "sha256",
                "bytes",
            }:
                raise OperationalV2CertificationError(
                    f"certification protection {name}[{index}] is malformed"
                )
            try:
                path = v2._relative_file(
                    record["path"],
                    f"certification protection {name}[{index}]",
                )
            except (OSError, ValueError, v2.OperationalV2Error) as exc:
                raise OperationalV2CertificationError(
                    f"certification protection {name}[{index}] is missing"
                ) from exc
            _validate_expected_artifact(
                path,
                record,
                f"certification protection {name}[{index}]",
            )


def _protection_summary(
    groups: dict[str, list[dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    return {
        name: {
            "file_count": len(records),
            "inventory_sha256": hashlib.sha256(
                json.dumps(
                    records, sort_keys=True, separators=(",", ":")
                ).encode()
            ).hexdigest(),
        }
        for name, records in groups.items()
    }


def _contains_pending(value: Any) -> bool:
    if isinstance(value, str):
        return "pending" in value.lower()
    if isinstance(value, dict):
        return any(_contains_pending(child) for child in value.values())
    if isinstance(value, list):
        return any(_contains_pending(child) for child in value)
    return False


def _accepted_package(
    artifacts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    return {
        "crosswalk": {
            "json": copy.deepcopy(artifacts["crosswalk_json"]),
            "csv": copy.deepcopy(artifacts["crosswalk_csv"]),
        },
        "reconciliation_manifest": copy.deepcopy(
            artifacts["reconciliation_manifest"]
        ),
        "dossiers": {
            "json": copy.deepcopy(artifacts["results_dossier_json"]),
            "markdown": copy.deepcopy(
                artifacts["results_dossier_markdown"]
            ),
        },
    }


def _validate_certified_payload(payload: Any) -> None:
    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != 1
        or payload.get("kind") != KIND
        or payload.get("campaign_version") != VERSION
        or payload.get("status") != "certified"
    ):
        raise OperationalV2CertificationError(
            "certified operational-v2 projection is malformed"
        )
    if _contains_pending(payload):
        raise OperationalV2CertificationError(
            "certified operational-v2 projection contains pending status"
        )
    if payload.get("authority_scope") != EXPECTED_SCOPE:
        raise OperationalV2CertificationError(
            "certified operational-v2 scope drifted"
        )
    rows = payload.get("rows")
    if (
        not isinstance(rows, list)
        or len(rows) != 62
        or payload.get("row_count") != 62
        or _projection_digest(rows) != EXPECTED_ROW_PROJECTION_SHA256
        or payload.get("row_projection_sha256")
        != EXPECTED_ROW_PROJECTION_SHA256
    ):
        raise OperationalV2CertificationError(
            "certified operational-v2 rows or identities drifted"
        )
    observed_counts = {
        "exact_output_determinism": _counts(rows, v2.EXACT_FIELD),
        "completeness_modulo_reviewed_equivalence": _counts(
            rows, v2.FULL_FIELD
        ),
    }
    if (
        observed_counts != EXPECTED_COUNTS
        or payload.get("classification_counts") != EXPECTED_COUNTS
        or payload.get("missing_source_backed_model_orders") != []
        or payload.get("overlay_orders") != ["78", "79"]
    ):
        raise OperationalV2CertificationError(
            "certified operational-v2 classifications or counts drifted"
        )
    review = payload.get("independent_review")
    if (
        not isinstance(review, dict)
        or review.get("required") is not True
        or review.get("status") != "accepted"
        or review.get("verdict") != "ACCEPT"
        or review.get("timestamp") != EXPECTED_REVIEW_TIMESTAMP
        or review.get("scope")
        != "additive-operational-v2-reconciliation"
        or review.get("row_count") != 62
        or review.get("overlay_orders") != ["78", "79"]
        or review.get("classification_counts") != EXPECTED_COUNTS
        or review.get("stage_transition") != "disabled"
        or review.get("artifact") != EXPECTED_REVIEW_ARTIFACT
    ):
        raise OperationalV2CertificationError(
            "certified operational-v2 review binding drifted"
        )
    expected_artifacts = {
        name: copy.deepcopy(EXPECTED_V2_ARTIFACTS[name])
        for name in V2_PATHS
    }
    if payload.get("accepted_operational_v2") != _accepted_package(
        expected_artifacts
    ):
        raise OperationalV2CertificationError(
            "certified operational-v2 artifact binding drifted"
        )
    protection = payload.get("protected_inputs")
    if not isinstance(protection, dict) or protection.get("status") != "matched":
        raise OperationalV2CertificationError(
            "certified operational-v2 protection record is malformed"
        )
    groups = protection.get("groups")
    _validate_protected_groups(groups)
    if protection.get("summary") != _protection_summary(groups):
        raise OperationalV2CertificationError(
            "certified operational-v2 protection summary drifted"
        )


def build_certified_projection() -> dict[str, Any]:
    review = _load_accept_review()
    _, rows, artifacts, base_groups = _validate_candidate_bundle()
    groups = {
        **base_groups,
        "accepted_operational_v2_package": [
            copy.deepcopy(artifacts[name]) for name in V2_PATHS
        ],
        "independent_operational_v2_review": [
            copy.deepcopy(review["artifact"])
        ],
    }
    _validate_protected_groups(groups)
    payload = {
        "schema_version": 1,
        "kind": KIND,
        "campaign_version": VERSION,
        "status": "certified",
        "authority_scope": copy.deepcopy(EXPECTED_SCOPE),
        "row_count": 62,
        "overlay_orders": ["78", "79"],
        "classification_counts": copy.deepcopy(EXPECTED_COUNTS),
        "missing_source_backed_model_orders": [],
        "row_projection_sha256": EXPECTED_ROW_PROJECTION_SHA256,
        "accepted_operational_v2": _accepted_package(artifacts),
        "independent_review": review,
        "protected_inputs": {
            "status": "matched",
            "groups": groups,
            "summary": _protection_summary(groups),
        },
        "rows": rows,
    }
    _validate_certified_payload(payload)
    return payload


def _report(payload: dict[str, Any]) -> str:
    exact = payload["classification_counts"]["exact_output_determinism"]
    full = payload["classification_counts"][
        "completeness_modulo_reviewed_equivalence"
    ]
    review = payload["independent_review"]
    artifacts = payload["accepted_operational_v2"]
    lines = [
        "# Certified Slice operational-v2 projection",
        "",
        "**Status:** `certified`",
        "",
        (
            f"**Independent review:** `{review['verdict']}` at "
            f"`{review['timestamp']}`"
        ),
        "",
        (
            "This additive projection binds the accepted operational-v2 "
            "crosswalk, reconciliation manifest, JSON and Markdown dossiers, "
            "and independent review without rewriting those artifacts or "
            "advancing Manager-owned state."
        ),
        "",
        "| Projection | Conditional complete | Conditional incomplete | Missing |",
        "|---|---:|---:|---:|",
        (
            f"| Exact output | {exact['conditional-complete']} | "
            f"{exact['conditional-incomplete']} | "
            f"{exact['missing-source-backed-model']} |"
        ),
        (
            f"| Reviewed equivalence | {full['conditional-complete']} | "
            f"{full['conditional-incomplete']} | "
            f"{full['missing-source-backed-model']} |"
        ),
        "",
        f"Certified rows: **{payload['row_count']}**.",
        "",
        "| Bound artifact | SHA-256 |",
        "|---|---|",
        (
            f"| `{artifacts['crosswalk']['json']['path']}` | "
            f"`{artifacts['crosswalk']['json']['sha256']}` |"
        ),
        (
            f"| `{artifacts['crosswalk']['csv']['path']}` | "
            f"`{artifacts['crosswalk']['csv']['sha256']}` |"
        ),
        (
            f"| `{artifacts['reconciliation_manifest']['path']}` | "
            f"`{artifacts['reconciliation_manifest']['sha256']}` |"
        ),
        (
            f"| `{artifacts['dossiers']['json']['path']}` | "
            f"`{artifacts['dossiers']['json']['sha256']}` |"
        ),
        (
            f"| `{artifacts['dossiers']['markdown']['path']}` | "
            f"`{artifacts['dossiers']['markdown']['sha256']}` |"
        ),
        (
            f"| `{review['artifact']['path']}` | "
            f"`{review['artifact']['sha256']}` |"
        ),
        "",
        "Manager-owned stage transition remains disabled.",
        "",
    ]
    return "\n".join(lines)


def _manifest(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": "operational-v2-certification-manifest",
        "campaign_version": VERSION,
        "status": "certified",
        "row_count": payload["row_count"],
        "classification_counts": copy.deepcopy(
            payload["classification_counts"]
        ),
        "missing_source_backed_model_orders": [],
        "independent_review": copy.deepcopy(payload["independent_review"]),
        "artifacts": {
            "certified_projection_json": _artifact(CERTIFIED_PROJECTION),
            "certified_projection_markdown": _artifact(CERTIFIED_REPORT),
        },
        "protected_inputs": {
            "status": "matched",
            "summary": copy.deepcopy(
                payload["protected_inputs"]["summary"]
            ),
        },
        "stage_transition": "disabled",
    }


def write_artifacts() -> dict[str, Any]:
    before = build_certified_projection()
    protected_before = copy.deepcopy(before["protected_inputs"]["groups"])
    CERTIFIED_ROOT.mkdir(parents=True, exist_ok=True)
    common.write_json(CERTIFIED_PROJECTION, before)
    CERTIFIED_REPORT.write_text(_report(before))
    manifest = _manifest(before)
    common.write_json(CERTIFICATION_MANIFEST, manifest)
    if build_certified_projection()["protected_inputs"]["groups"] != (
        protected_before
    ):
        raise OperationalV2CertificationError(
            "certification writer mutated a protected file"
        )
    validate_written_artifacts()
    return manifest


def validate_written_artifacts() -> dict[str, Any]:
    expected = build_certified_projection()
    actual = _load_json(
        CERTIFIED_PROJECTION, "certified operational-v2 projection"
    )
    _validate_certified_payload(actual)
    if actual != expected:
        raise OperationalV2CertificationError(
            "certified operational-v2 projection is stale"
        )
    expected_report = _report(expected)
    if _read_text(
        CERTIFIED_REPORT, "certified operational-v2 report"
    ) != expected_report:
        raise OperationalV2CertificationError(
            "certified operational-v2 report is stale"
        )
    expected_manifest = _manifest(expected)
    actual_manifest = _load_json(
        CERTIFICATION_MANIFEST,
        "operational-v2 certification manifest",
    )
    if _contains_pending(actual_manifest):
        raise OperationalV2CertificationError(
            "operational-v2 certification manifest contains pending status"
        )
    if actual_manifest != expected_manifest:
        raise OperationalV2CertificationError(
            "operational-v2 certification manifest is stale"
        )
    for label, record in actual_manifest["artifacts"].items():
        path = OUT / record["path"]
        _validate_expected_artifact(path, record, label)
    return actual_manifest


def main() -> None:
    manifest = write_artifacts()
    exact = manifest["classification_counts"]["exact_output_determinism"]
    full = manifest["classification_counts"][
        "completeness_modulo_reviewed_equivalence"
    ]
    print("operational_v2_certification_closure=PASS")
    print("independent_review=ACCEPT")
    print("review_status=accepted")
    print(f"rows={manifest['row_count']}")
    print(
        "exact="
        f"{exact['conditional-complete']}/"
        f"{exact['conditional-incomplete']}/"
        f"{exact['missing-source-backed-model']}"
    )
    print(
        "full="
        f"{full['conditional-complete']}/"
        f"{full['conditional-incomplete']}/"
        f"{full['missing-source-backed-model']}"
    )
    print("stage_transition=disabled")


if __name__ == "__main__":
    main()
