#!/usr/bin/env python3
"""Build and validate the additive 62-target final campaign crosswalk."""

from __future__ import annotations

import csv
import json
import re
import shlex
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import campaign_common as common
import preservation_policy_v3 as preservation_policy
import target_029


OUT = common.OUT
LEDGER_CSV = OUT / "crosswalk/target_to_proof_boundary.csv"
LEDGER_JSON = OUT / "crosswalk/target_to_proof_boundary.json"
TRUST_CSV = OUT / "crosswalk/trust_site_inventory.csv"
TRUST_JSON = OUT / "crosswalk/trust_site_inventory.json"
AGGREGATE_CSV = OUT / "crosswalk/conditional_obligation_crosswalk.csv"
AGGREGATE_JSON = OUT / "crosswalk/conditional_obligation_crosswalk.json"
OPERATIONAL_V2_CROSSWALKS = {
    OUT / "crosswalk/conditional_obligation_crosswalk_operational_v2.csv",
    OUT / "crosswalk/conditional_obligation_crosswalk_operational_v2.json",
}
TARGET_078_OPERATIONAL_EVIDENCE = (
    OUT / "evidence/target_078_operational_v1"
)
TARGET_078_OPERATIONAL_ADDENDA = {
    OUT / "crosswalk/target_078_operational_v1_addendum.csv",
    OUT / "crosswalk/target_078_operational_v1_addendum.json",
}
TARGET_079_OPERATIONAL_EVIDENCE = (
    OUT / "evidence/target_079_operational_v1"
)
TARGET_079_ADAPTER_REFINEMENT_V2_EVIDENCE = (
    OUT / "evidence/target_079_adapter_refinement_v2"
)
TARGET_078_ADAPTER_REFINEMENT_V2_EVIDENCE = (
    OUT / "evidence/target_078_adapter_refinement_v2"
)
TARGET_079_OPERATIONAL_ADDENDA = {
    OUT / "crosswalk/target_079_operational_v1_addendum.csv",
    OUT / "crosswalk/target_079_operational_v1_addendum.json",
}
FINAL_ROOT = OUT / "evidence/final_campaign"
TARGET_029_BOUNDARY = FINAL_ROOT / "target_029_boundary_manifest.json"
DOSSIER_JSON = FINAL_ROOT / "results_dossier.json"
DOSSIER_MD = FINAL_ROOT / "results_dossier.md"
PRESERVATION_BASELINE = FINAL_ROOT / "preservation_baseline.json"
RECONCILIATION_MANIFEST = FINAL_ROOT / "reconciliation_manifest.json"
FINAL_REVIEW_REQUEST = OUT / "review/FINAL_CAMPAIGN_REVIEW_REQUEST.md"
FINAL_REVIEW_ACCEPTANCE = OUT / "review/FINAL_CAMPAIGN_REVIEW_ACCEPTANCE.md"

EXACT_FIELD = "exact_output_determinism_status"
FULL_FIELD = "completeness_modulo_reviewed_equivalence_status"
ALLOWED_CLASSIFICATIONS = {
    "conditional-complete",
    "conditional-incomplete",
    "missing-source-backed-model",
}
EXPECTED_EXACT_COUNTS = Counter(
    {
        "conditional-complete": 48,
        "conditional-incomplete": 12,
        "missing-source-backed-model": 2,
    }
)
EXPECTED_FULL_COUNTS = Counter(
    {
        "conditional-complete": 41,
        "conditional-incomplete": 19,
        "missing-source-backed-model": 2,
    }
)
WEAK_EQUIVALENCE_ORDERS = {"28", "29", "30", "80", "81", "82"}
MISSING_MODEL_ORDERS = {"78", "79"}

REVIEW_GROUPS = {
    "review/REVIEW_ACCEPTANCE_20260831T110316Z.md": ("29",),
    "review/REVIEW_ACCEPTANCE_20260831T114621Z.md": ("13",),
    "review/REVIEW_ACCEPTANCE_20260831T122239Z.md": ("106",),
    "review/REVIEW_ACCEPTANCE_20260831T125401Z.md": ("81",),
    "review/REVIEW_ACCEPTANCE_20260831T133819Z.md": ("22",),
    "review/REVIEW_ACCEPTANCE_20260831T142401Z.md": ("120",),
    "review/REVIEW_ACCEPTANCE_20260831T150040Z.md": ("51",),
    "review/REVIEW_ACCEPTANCE_20260831T153731Z.md": ("52",),
    "review/REVIEW_ACCEPTANCE_20260831T173550Z.md": ("19", "20", "21"),
    "review/REVIEW_ACCEPTANCE_20260831T184122Z.md": ("28", "30", "65"),
    "review/REVIEW_ACCEPTANCE_20260831T192724Z.md": (
        "12",
        "14",
        "15",
        "23",
        "24",
    ),
    "review/REVIEW_ACCEPTANCE_20260831T205556Z.md": ("25", "26", "119"),
    "review/REVIEW_ACCEPTANCE_20260831T213648Z.md": ("80", "82"),
    "review/REVIEW_ACCEPTANCE_20260831T225709Z.md": ("77",),
    "review/REVIEW_ACCEPTANCE_20260901T014750Z.md": ("78", "79"),
    "review/REVIEW_ACCEPTANCE_20260901T024835Z.md": (
        "32",
        "36",
        "69",
        "74",
        "76",
        "93",
        "98",
    ),
    "review/REVIEW_ACCEPTANCE_20260901T034008Z.md": (
        "91",
        "97",
        "101",
        "103",
    ),
    "review/REVIEW_ACCEPTANCE_20260901T050359Z.md": ("37", "43"),
    "review/REVIEW_ACCEPTANCE_20260901T055412Z.md": ("35", "68"),
    "review/REVIEW_ACCEPTANCE_20260901T064245Z.md": ("62", "90", "96"),
    "review/REVIEW_ACCEPTANCE_20260901T072051Z.md": ("85", "86"),
    "review/REVIEW_ACCEPTANCE_20260901T080418Z.md": ("99", "104"),
    "review/REVIEW_ACCEPTANCE_20260901T102036Z.md": ("48", "49"),
    "review/REVIEW_ACCEPTANCE_20260901T111757Z.md": ("53", "54", "55"),
    "review/REVIEW_ACCEPTANCE_20260901T121316Z.md": ("39", "111"),
    "review/REVIEW_ACCEPTANCE_20260901T135004Z.md": (
        "17",
        "18",
        "46",
        "47",
    ),
    "review/REVIEW_ACCEPTANCE_20260901T145107Z.md": ("8", "9"),
}

CSV_FIELDS = [
    "input_order",
    "target",
    "semantic_family",
    "active_contract_sha256",
    "generated_declaration_path",
    "source_reference",
    "public_docs_reference",
    "harness_path",
    "transformation_manifest_path",
    "dependency_manifest_path",
    "retained_implementation_proof_boundary_assumption",
    "retained_implementation_proof_trust_site_ids",
    "conditional_boundary_manifest_path",
    "conditional_boundary_manifest_sha256",
    "conditional_boundary_observations_json",
    "conditional_boundary_trust_site_ids",
    "conditional_boundary_exclusions_json",
    "conditional_boundary_replacements_json",
    "source_citations_json",
    "proof_scope_json",
    "equivalence_kind",
    "equivalence_policy",
    "equivalence_source_citation",
    "equivalence_positive_witness",
    "equivalence_negative_witness",
    EXACT_FIELD,
    FULL_FIELD,
    "exact_obligation_path",
    "exact_solver_result",
    "full_obligation_path",
    "full_solver_result",
    "witness_evidence_json",
    "verus_evidence_json",
    "accepting_incremental_review_path",
    "accepting_incremental_review_sha256",
    "accepting_incremental_review_verdict",
]


class ReconciliationError(ValueError):
    pass


def _load_json(path: Path) -> Any:
    with path.open() as handle:
        return json.load(handle)


def _artifact(path: Path) -> dict[str, Any]:
    return {
        "path": common.relpath(path),
        "sha256": common.sha256(path),
        "bytes": path.stat().st_size,
    }


def _split_site_ids(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _walk(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, (*path, str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, (*path, str(index)))


def _trust_ids(value: Any) -> list[str]:
    found: set[str] = set()
    for _, item in _walk(value):
        if isinstance(item, str):
            found.update(re.findall(r"TS-\d{3}-[A-Z]\d{3}", item))
    return sorted(found)


def _source_citations(row: dict[str, str], manifest: dict[str, Any]) -> list[str]:
    citations = {
        row["source_reference"],
        row["public_docs_reference"],
        row["equivalence_source_citation"],
    }
    for _, item in _walk(manifest):
        if isinstance(item, str) and (
            "core/src/" in item or "library/core/src/" in item
        ):
            citations.add(item)
    return sorted(item for item in citations if item)


def _manifest_fields(
    manifest: dict[str, Any], needles: tuple[str, ...]
) -> dict[str, Any]:
    return {
        key: value
        for key, value in manifest.items()
        if any(needle in key for needle in needles)
    }


def _capture_summaries(value: Any) -> list[dict[str, Any]]:
    captures: list[dict[str, Any]] = []
    for json_path, item in _walk(value):
        if not isinstance(item, dict):
            continue
        required = {"argv", "command", "stdout", "stderr", "status", "exit_code"}
        if not required <= set(item):
            continue
        summary = {
            "json_path": ".".join(json_path),
            "argv": item["argv"],
            "command": item["command"],
            "stdout": item["stdout"],
            "stderr": item["stderr"],
            "status": item["status"],
            "exit_code": item["exit_code"],
        }
        for key in ("solver_result", "expected_solver_result"):
            if key in item:
                summary[key] = item[key]
        captures.append(summary)
    return captures


def _artifact_summaries(value: Any) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for json_path, item in _walk(value):
        if (
            isinstance(item, dict)
            and {"path", "sha256", "bytes"} <= set(item)
        ):
            artifacts.append(
                {
                    "json_path": ".".join(json_path),
                    "path": item["path"],
                    "sha256": item["sha256"],
                    "bytes": item["bytes"],
                }
            )
    return artifacts


def _validate_relative_path(value: str, label: str) -> Path:
    path = (OUT / value).resolve()
    try:
        path.relative_to(OUT.resolve())
    except ValueError as exc:
        raise ReconciliationError(f"{label}: path escapes experiment root") from exc
    if not path.is_file():
        raise ReconciliationError(f"{label}: missing file {value}")
    return path


def _validate_artifacts(value: Any, label: str) -> None:
    for json_path, item in _walk(value):
        if not (
            isinstance(item, dict)
            and {"path", "sha256", "bytes"} <= set(item)
        ):
            continue
        suffix = ".".join(json_path)
        path = _validate_relative_path(str(item["path"]), f"{label}.{suffix}")
        if (
            item["sha256"] != common.sha256(path)
            or item["bytes"] != path.stat().st_size
        ):
            raise ReconciliationError(
                f"{label}.{suffix}: artifact hash or size mismatch"
            )


def _validate_captures(value: Any, label: str) -> None:
    for json_path, item in _walk(value):
        if not isinstance(item, dict):
            continue
        required = {"argv", "command", "stdout", "stderr", "status", "exit_code"}
        if not required <= set(item):
            continue
        suffix = ".".join(json_path)
        paths = {
            key: _validate_relative_path(
                str(item[key]), f"{label}.{suffix}.{key}"
            )
            for key in ("command", "stdout", "stderr", "status")
        }
        argv = item["argv"]
        if (
            not isinstance(argv, list)
            or not all(isinstance(arg, str) for arg in argv)
            or paths["command"].read_text() != shlex.join(argv) + "\n"
            or item["exit_code"] != 0
            or paths["status"].read_text() != "0\n"
            or paths["stderr"].read_text() != ""
        ):
            raise ReconciliationError(f"{label}.{suffix}: invalid command capture")
        if "solver_result" in item:
            result = str(item["solver_result"])
            first = paths["stdout"].read_text().splitlines()
            if (
                not first
                or first[0] != result
                or (
                    "expected_solver_result" in item
                    and item["expected_solver_result"] != result
                )
            ):
                raise ReconciliationError(
                    f"{label}.{suffix}: solver capture/result mismatch"
                )


def _obligation_entry(
    result: dict[str, Any], projection: str
) -> tuple[str, dict[str, Any]] | None:
    obligations = result.get("obligations")
    if not isinstance(obligations, dict):
        raise ReconciliationError("result obligations must be an object")
    if projection == "exact":
        matches = [
            (key, value)
            for key, value in obligations.items()
            if key.startswith("exact-")
        ]
    else:
        matches = [
            (key, value)
            for key, value in obligations.items()
            if key.startswith("completeness-modulo-")
        ]
    if len(matches) > 1:
        raise ReconciliationError(
            f"{projection}: duplicate classification obligations"
        )
    if not matches:
        return None
    key, value = matches[0]
    if not isinstance(value, dict):
        raise ReconciliationError(f"{key}: obligation evidence must be an object")
    return key, value


def _validate_direct_obligation(
    result: dict[str, Any],
    *,
    projection: str,
    classification: str,
    missing_model: bool,
) -> dict[str, Any]:
    entry = _obligation_entry(result, projection)
    if missing_model:
        if projection == "exact" and entry is not None:
            raise ReconciliationError(
                "missing-source-backed-model exact projection must not carry "
                "a classifying bounded obligation"
            )
        if projection == "full":
            if entry is None:
                raise ReconciliationError(
                    "missing-source-backed-model row lacks bounded diagnostic"
                )
            key, evidence = entry
            solver = evidence.get("solver")
            if not isinstance(solver, dict) or solver.get("solver_result") != "unsat":
                raise ReconciliationError(
                    "missing-source-backed-model diagnostic must retain bounded UNSAT"
                )
            return {
                "purpose": key,
                "classification_evidence": False,
                "diagnostic_only": True,
                "smt": evidence.get("smt"),
                "solver": _capture_summaries(evidence),
            }
        return {
            "purpose": None,
            "classification_evidence": False,
            "diagnostic_only": True,
            "reason": "arbitrary-length source transition is not modeled",
        }

    if entry is None:
        raise ReconciliationError(f"{projection}: classifying obligation is missing")
    key, evidence = entry
    solver = evidence.get("solver")
    if not isinstance(solver, dict):
        raise ReconciliationError(f"{key}: direct solver evidence is missing")
    expected = {
        "conditional-complete": "unsat",
        "conditional-incomplete": "sat",
    }[classification]
    if solver.get("solver_result") != expected:
        raise ReconciliationError(
            f"{key}: {classification} requires direct {expected.upper()}"
        )
    smt = evidence.get("smt")
    if not isinstance(smt, dict):
        raise ReconciliationError(f"{key}: generated SMT artifact is missing")
    return {
        "purpose": key,
        "classification_evidence": True,
        "diagnostic_only": False,
        "smt": smt,
        "metadata": evidence.get("metadata"),
        "solver": _capture_summaries(evidence),
    }


def _witness_candidates(
    result: dict[str, Any], projection: str
) -> dict[str, Any]:
    common_keys = {
        "fixed_witnesses",
        "fixed_reference_witness",
        "fixed_sat_replays",
    }
    selected: dict[str, Any] = {}
    for key, value in result.items():
        if key in common_keys:
            selected[key] = value
        elif projection == "exact" and "exact" in key and "witness" in key:
            selected[key] = value
        elif projection == "full" and (
            key == "fixed_sat_replay"
            or "counterexample" in key
            or ("full" in key and "witness" in key)
        ):
            selected[key] = value
    return selected


def _validate_incomplete_witness(
    result: dict[str, Any], projection: str
) -> dict[str, Any]:
    selected = _witness_candidates(result, projection)
    sat_captures = [
        capture
        for capture in _capture_summaries(selected)
        if capture.get("solver_result") == "sat"
    ]
    smt_artifacts = [
        artifact
        for artifact in _artifact_summaries(selected)
        if str(artifact["path"]).endswith(".smt2")
    ]
    if not sat_captures or not smt_artifacts:
        raise ReconciliationError(
            f"{projection}: conditional-incomplete lacks fixed-boundary SAT evidence"
        )
    return {
        "projection": projection,
        "top_level_keys": sorted(selected),
        "sat_solver_captures": sat_captures,
        "fixed_model_artifacts": smt_artifacts,
    }


def _validate_verus(result: dict[str, Any]) -> dict[str, Any]:
    verus = result.get("verus")
    if not isinstance(verus, dict):
        raise ReconciliationError("result lacks Verus evidence")
    expected = verus.get("expected_summary")
    if expected is not None and (not isinstance(expected, str) or not expected):
        raise ReconciliationError("Verus expected summary is malformed")
    verified: list[dict[str, Any]] = []
    observed_summaries: set[str] = set()
    for capture in _capture_summaries(verus):
        argv = capture["argv"]
        if "--no-verify" in argv or not argv:
            continue
        if Path(argv[0]).name != "verus":
            continue
        stdout = _validate_relative_path(
            capture["stdout"], "Verus verification stdout"
        ).read_text()
        matches = re.findall(
            r"verification results:: \d+ verified, 0 errors", stdout
        )
        if not matches:
            continue
        observed_summaries.update(matches)
        if expected is None or expected in matches:
            verified.append(capture)
    if not verified:
        raise ReconciliationError("no clean Verus verification capture matches summary")
    if len(observed_summaries) != 1:
        raise ReconciliationError("Verus verification summaries are ambiguous")
    observed = next(iter(observed_summaries))
    if expected is not None and expected != observed:
        raise ReconciliationError("Verus expected and observed summaries differ")
    return {
        "expected_summary": expected or observed,
        "verification_captures": verified,
        "artifacts": _artifact_summaries(verus),
    }


def _review_map(
    expected_targets_by_order: dict[str, str],
) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for relative, orders in REVIEW_GROUPS.items():
        path = OUT / relative
        if not path.is_file():
            raise ReconciliationError(f"incremental review is missing: {relative}")
        text = path.read_text()
        if "**VERDICT: ACCEPT**" not in text:
            raise ReconciliationError(f"incremental review did not ACCEPT: {relative}")
        for order in orders:
            if order in mapped:
                raise ReconciliationError(
                    f"input order {order} has duplicate incremental reviews"
                )
            target = expected_targets_by_order.get(order)
            if target is None:
                raise ReconciliationError(
                    f"incremental review maps orphan input order {order}"
                )
            if target not in text:
                raise ReconciliationError(
                    f"incremental review does not name {order} {target}: {relative}"
                )
            mapped[order] = {
                **_artifact(path),
                "verdict": "ACCEPT",
            }
    expected_orders = set(expected_targets_by_order)
    if set(mapped) != expected_orders:
        missing = sorted(expected_orders - set(mapped), key=int)
        orphaned = sorted(set(mapped) - expected_orders, key=int)
        raise ReconciliationError(
            f"incremental review map mismatch: missing={missing}, orphaned={orphaned}"
        )
    return mapped


def _trust_rows() -> list[dict[str, str]]:
    csv_rows = common.read_csv(TRUST_CSV)
    json_rows = _load_json(TRUST_JSON)
    if not isinstance(json_rows, list) or csv_rows != json_rows:
        raise ReconciliationError("trust-site CSV and JSON inventories diverge")
    ids = [row["record_id"] for row in csv_rows]
    if len(ids) != len(set(ids)):
        raise ReconciliationError("trust-site inventory contains duplicate IDs")
    return csv_rows


def _normalized_trust_record(row: dict[str, str]) -> dict[str, str]:
    fields = (
        "record_id",
        "record_type",
        "kind",
        "name",
        "status",
        "rationale",
        "source_lines",
        "source_sha256",
        "harness_path",
        "attribute_line",
        "declaration_line",
        "signature",
        "contract_sha256",
        "matching_dependency_record_ids",
        "semantic_role",
        "semantic_disposition",
        "target_postcondition_coverage",
        "adjudication_rationale",
        "adjudication_source_citations",
        "semantic_audit_category",
        "semantic_audit_version",
    )
    return {field: row[field] for field in fields if row.get(field)}


def _boundary_path(order: str, artifact_id: str) -> Path:
    if order == target_029.INPUT_ORDER:
        return TARGET_029_BOUNDARY
    return OUT / "evidence/targets" / artifact_id / "boundary_manifest.json"


def _authority_binding(row: dict[str, str]) -> dict[str, str]:
    fields = (
        "active_run_id",
        "active_r0_z3",
        "active_unknown_reason_class",
        "catalog_status",
        "abcd_status",
        "active_contract_text",
        "active_contract_sha256",
        "generated_declaration_path",
        "generated_declaration_start_line",
        "generated_declaration_end_line",
        "generated_declaration_sha256",
        "shared_vocabulary_path",
        "shared_vocabulary_sha256",
        "source_reference",
        "source_path",
        "source_file_sha256",
        "source_item_start_line",
        "source_item_end_line",
        "source_item_sha256",
        "public_docs_reference",
        "public_docs_start_line",
        "public_docs_end_line",
        "public_docs_sha256",
        "harness_path",
        "harness_sha256",
        "source_body_manifest_path",
        "source_body_manifest_sha256",
        "transformation_manifest_path",
        "transformation_manifest_sha256",
        "dependency_manifest_path",
        "dependency_manifest_sha256",
    )
    return {field: row[field] for field in fields}


def _campaign_review() -> dict[str, Any]:
    if not FINAL_REVIEW_ACCEPTANCE.is_file():
        return {
            "status": "pending-independent-review",
            "request": _artifact(FINAL_REVIEW_REQUEST),
            "acceptance": None,
        }
    text = FINAL_REVIEW_ACCEPTANCE.read_text()
    if "**VERDICT: ACCEPT**" not in text:
        raise ReconciliationError("campaign-wide review file is not ACCEPT")
    if "62" not in text:
        raise ReconciliationError("campaign-wide ACCEPT does not cover 62 rows")
    return {
        "status": "accepted",
        "request": _artifact(FINAL_REVIEW_REQUEST),
        "acceptance": _artifact(FINAL_REVIEW_ACCEPTANCE),
    }


def build_campaign() -> dict[str, Any]:
    scope = common.derive_scope()
    manifest_counts = Counter(
        row["r0_z3"] for row in scope["manifest_rows"]
    )
    if (
        len(scope["generated_targets"]) != 120
        or manifest_counts != Counter({"unknown": 62, "unsat": 58})
        or len(scope["exact_vstd_targets"]) != 12
    ):
        raise ReconciliationError(
            "active authority does not cross-check as 120 generated, "
            "62 UNKNOWN, 58 UNSAT, and 12 exact-vstd"
        )

    csv_rows = common.read_csv(LEDGER_CSV)
    json_rows = _load_json(LEDGER_JSON)
    if not isinstance(json_rows, list) or csv_rows != json_rows:
        raise ReconciliationError("frozen authority ledger formats diverge")
    keys = [(row["target"], row["input_order"]) for row in csv_rows]
    if len(keys) != 62 or len(set(keys)) != 62:
        raise ReconciliationError("authority ledger must have 62 unique rows")
    selected_targets = set(scope["selected_targets"])
    if {row["target"] for row in csv_rows} != selected_targets:
        raise ReconciliationError("authority ledger target set differs from active UNKNOWN set")
    if any(
        row["module"] != "slice"
        or row["active_r0_z3"] != "unknown"
        or row["catalog_status"] != common.GENERATED_STATUS
        for row in csv_rows
    ):
        raise ReconciliationError("authority ledger leaks non-Slice or non-UNKNOWN rows")

    expected_targets_by_order = {
        row["input_order"]: row["target"] for row in csv_rows
    }
    expected_artifact_ids = {
        common.target_artifact_id(row["target"], int(row["input_order"]))
        for row in csv_rows
    }
    actual_artifact_ids = {
        path.name
        for path in (OUT / "evidence/targets").iterdir()
        if path.is_dir()
    }
    if actual_artifact_ids != expected_artifact_ids:
        missing = sorted(expected_artifact_ids - actual_artifact_ids)
        orphaned = sorted(actual_artifact_ids - expected_artifact_ids)
        raise ReconciliationError(
            f"target evidence directory mismatch: missing={missing}, "
            f"orphaned={orphaned}"
        )
    reviews = _review_map(expected_targets_by_order)
    trust_rows = _trust_rows()
    trust_by_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    for trust in trust_rows:
        trust_by_target[trust["target"]].append(trust)
    if set(trust_by_target) != selected_targets:
        raise ReconciliationError("trust inventory has missing or orphaned targets")

    exact_counts = Counter(row[EXACT_FIELD] for row in csv_rows)
    full_counts = Counter(row[FULL_FIELD] for row in csv_rows)
    if (
        set(exact_counts) - ALLOWED_CLASSIFICATIONS
        or set(full_counts) - ALLOWED_CLASSIFICATIONS
        or exact_counts != EXPECTED_EXACT_COUNTS
        or full_counts != EXPECTED_FULL_COUNTS
    ):
        raise ReconciliationError(
            f"classification count mismatch: exact={dict(exact_counts)}, "
            f"full={dict(full_counts)}"
        )

    aggregate_rows: list[dict[str, Any]] = []
    retained_capture_count = 0
    for row in sorted(csv_rows, key=lambda item: int(item["input_order"])):
        target = row["target"]
        order = row["input_order"]
        artifact_id = common.target_artifact_id(target, int(order))
        root = OUT / "evidence/targets" / artifact_id
        result_path = root / "result.json"
        if not result_path.is_file():
            raise ReconciliationError(f"{order} {target}: result.json is missing")
        result = _load_json(result_path)
        updated_fields = result.get("updated_crosswalk_fields")
        if (
            result.get("target") != target
            or str(int(str(result.get("input_order")))) != order
            or result.get("active_contract_sha256") != row["active_contract_sha256"]
            or result.get("active_contract_text") != row["active_contract_text"]
            or result.get("artifact_id") != artifact_id
            or result.get("classification")
            != {
                EXACT_FIELD: row[EXACT_FIELD],
                FULL_FIELD: row[FULL_FIELD],
            }
            or not isinstance(updated_fields, list)
            or len(updated_fields) != 2
            or set(updated_fields) != {EXACT_FIELD, FULL_FIELD}
        ):
            raise ReconciliationError(f"{order} {target}: result/ledger mismatch")
        _validate_artifacts(result, f"{order} result")
        _validate_captures(result, f"{order} result")
        retained_capture_count += len(_capture_summaries(result))

        boundary_path = _boundary_path(order, artifact_id)
        if not boundary_path.is_file():
            raise ReconciliationError(
                f"{order} {target}: conditional boundary manifest is missing"
            )
        boundary = _load_json(boundary_path)
        if (
            boundary.get("target") != target
            or str(int(str(boundary.get("input_order")))) != order
            or (
                "active_contract_sha256" in boundary
                and boundary["active_contract_sha256"]
                != row["active_contract_sha256"]
            )
            or not isinstance(boundary.get("shared_boundary_observations"), list)
            or not boundary["shared_boundary_observations"]
        ):
            raise ReconciliationError(f"{order} {target}: boundary manifest mismatch")
        narrower = boundary.get(
            "boundary_narrower_than_target",
            boundary.get("model_boundary_narrower_than_target"),
        )
        if narrower is not True:
            raise ReconciliationError(f"{order} {target}: boundary is not narrower")

        expected_site_ids = _split_site_ids(row["all_trust_site_ids"])
        actual_trust_rows = trust_by_target[target]
        actual_site_ids = [trust["record_id"] for trust in actual_trust_rows]
        if sorted(expected_site_ids) != sorted(actual_site_ids):
            raise ReconciliationError(
                f"{order} {target}: trust inventory/ledger site mismatch"
            )
        manifest_site_ids = _trust_ids(boundary)
        if sorted(expected_site_ids) != manifest_site_ids:
            raise ReconciliationError(
                f"{order} {target}: boundary manifest trust-site coverage mismatch"
            )

        missing_model = order in MISSING_MODEL_ORDERS
        if missing_model != (
            row[EXACT_FIELD] == "missing-source-backed-model"
            and row[FULL_FIELD] == "missing-source-backed-model"
        ):
            raise ReconciliationError(
                f"{order} {target}: missing-model set/classification mismatch"
            )
        exact_evidence = _validate_direct_obligation(
            result,
            projection="exact",
            classification=row[EXACT_FIELD],
            missing_model=missing_model,
        )
        full_evidence = _validate_direct_obligation(
            result,
            projection="full",
            classification=row[FULL_FIELD],
            missing_model=missing_model,
        )
        if missing_model:
            unresolved = result.get("unresolved_source_model_phases")
            if not isinstance(unresolved, list) or not unresolved:
                raise ReconciliationError(
                    f"{order} {target}: unresolved source phases are missing"
                )

        witnesses: list[dict[str, Any]] = []
        for projection, field in (("exact", EXACT_FIELD), ("full", FULL_FIELD)):
            if row[field] == "conditional-incomplete":
                witnesses.append(_validate_incomplete_witness(result, projection))
        verus = _validate_verus(result)

        weak = order in WEAK_EQUIVALENCE_ORDERS
        if weak:
            expected_kind = (
                "matching-index-equivalence"
                if order in {"28", "29", "30"}
                else "equal-key-reordering-equivalence"
            )
            if (
                row["equivalence_kind"] != expected_kind
                or not row["equivalence_source_citation"]
                or not row["equivalence_positive_witness"]
                or not row["equivalence_negative_witness"]
            ):
                raise ReconciliationError(
                    f"{order} {target}: weakened equivalence audit is incomplete"
                )
            for key in (
                "equivalence_positive_witness",
                "equivalence_negative_witness",
            ):
                _validate_relative_path(row[key], f"{order} {key}")
        elif row["equivalence_kind"] != "exact-principal-return-and-final-state":
            raise ReconciliationError(
                f"{order} {target}: unreviewed weakened equivalence"
            )

        observations = boundary["shared_boundary_observations"]
        conditional_site_ids = _trust_ids(observations)
        exclusions = _manifest_fields(
            boundary,
            (
                "excluded",
                "forbidden",
                "inactive",
                "missing_source",
                "classification_limit",
            ),
        )
        replacements = _manifest_fields(
            boundary,
            (
                "replacement",
                "transition",
                "source_backed",
                "deterministic_source",
                "canonical_source",
            ),
        )
        proof_scope = {
            "bounded_domain": result.get(
                "bounded_domain", boundary.get("bounded_domain")
            ),
            "obligation_purposes": sorted(result["obligations"]),
            "classification_basis": result.get("classification_basis"),
            "manifest_proof_scope": boundary.get("proof_scope"),
            "general_proof_scope": boundary.get("general_proof_scope"),
            "unresolved_source_model_phases": result.get(
                "unresolved_source_model_phases", []
            ),
        }
        exact_path = (
            exact_evidence["smt"].get("path")
            if isinstance(exact_evidence.get("smt"), dict)
            else ""
        )
        full_path = (
            full_evidence["smt"].get("path")
            if isinstance(full_evidence.get("smt"), dict)
            else ""
        )
        review = reviews[order]
        aggregate_rows.append(
            {
                "input_order": order,
                "target": target,
                "semantic_family": row["semantic_family"],
                "authority": _authority_binding(row),
                "retained_implementation_proof_boundary": {
                    "proof_boundary_assumption": row["proof_boundary_assumption"],
                    "boundary_model_requirement": row["boundary_model_requirement"],
                    "boundary_admissibility": row["boundary_admissibility"],
                    "boundary_narrower_than_target": row[
                        "boundary_narrower_than_target"
                    ],
                    "all_trust_site_ids": expected_site_ids,
                    "trust_sites": [
                        _normalized_trust_record(item)
                        for item in actual_trust_rows
                    ],
                },
                "conditional_obligation_boundary": {
                    "manifest": _artifact(boundary_path),
                    "shared_observations": observations,
                    "observation_trust_site_ids": conditional_site_ids,
                    "admitted_and_context_fields": _manifest_fields(
                        boundary,
                        (
                            "admitted",
                            "context",
                            "boundary_backing",
                            "source_support",
                        ),
                    ),
                    "excluded_fields": exclusions,
                    "source_backed_replacement_and_transition_fields": replacements,
                    "boundary_narrower_than_target": True,
                },
                "source_citations": _source_citations(row, boundary),
                "proof_scope": proof_scope,
                "equivalence": {
                    "kind": row["equivalence_kind"],
                    "policy": row["equivalence_policy"],
                    "source_citation": row["equivalence_source_citation"],
                    "positive_witness": row["equivalence_positive_witness"],
                    "negative_witness": row["equivalence_negative_witness"],
                    "weakened": weak,
                },
                "classification": {
                    EXACT_FIELD: row[EXACT_FIELD],
                    FULL_FIELD: row[FULL_FIELD],
                },
                "solver_evidence": {
                    "exact_output": exact_evidence,
                    "full_state": full_evidence,
                    "all_retained_captures": _capture_summaries(result),
                },
                "replayable_witnesses": witnesses,
                "verus_evidence": verus,
                "result_manifest": _artifact(result_path),
                "accepting_incremental_review": review,
                "_csv": {
                    "generated_declaration_path": row[
                        "generated_declaration_path"
                    ],
                    "source_reference": row["source_reference"],
                    "public_docs_reference": row["public_docs_reference"],
                    "harness_path": row["harness_path"],
                    "transformation_manifest_path": row[
                        "transformation_manifest_path"
                    ],
                    "dependency_manifest_path": row["dependency_manifest_path"],
                    "exact_obligation_path": exact_path,
                    "exact_solver_result": (
                        "diagnostic-only"
                        if missing_model
                        else (
                            "unsat"
                            if row[EXACT_FIELD] == "conditional-complete"
                            else "sat"
                        )
                    ),
                    "full_obligation_path": full_path,
                    "full_solver_result": (
                        "diagnostic-only-unsat"
                        if missing_model
                        else (
                            "unsat"
                            if row[FULL_FIELD] == "conditional-complete"
                            else "sat"
                        )
                    ),
                },
            }
        )

    return {
        "schema_version": 1,
        "theorem": (
            "For the same valid input x and boundary observation b in both "
            "executions, Requires_T(x) and Boundary_T(x,b) and "
            "Spec_T(x,b,y1,s1) and Spec_T(x,b,y2,s2) imply "
            "Equivalent_T(x,b,y1,s1,y2,s2)."
        ),
        "authority_scope": {
            "active_run_id": scope["active_run_id"],
            "generated_slice_contracts": len(scope["generated_targets"]),
            "selected_r0_unknown": len(scope["selected_targets"]),
            "active_r0_unsat_excluded": manifest_counts["unsat"],
            "exact_vstd_excluded": len(scope["exact_vstd_targets"]),
            "authority_ledger": {
                "csv": _artifact(LEDGER_CSV),
                "json": _artifact(LEDGER_JSON),
            },
            "trust_inventory": {
                "csv": _artifact(TRUST_CSV),
                "json": _artifact(TRUST_JSON),
                "record_count": len(trust_rows),
            },
        },
        "classification_counts": {
            "exact_output_determinism": dict(sorted(exact_counts.items())),
            "completeness_modulo_reviewed_equivalence": dict(
                sorted(full_counts.items())
            ),
        },
        "weakened_equivalence_orders": sorted(
            WEAK_EQUIVALENCE_ORDERS, key=int
        ),
        "missing_source_backed_model_orders": sorted(
            MISSING_MODEL_ORDERS, key=int
        ),
        "retained_command_capture_count": retained_capture_count,
        "campaign_wide_review": _campaign_review(),
        "rows": aggregate_rows,
    }


def _csv_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in payload["rows"]:
        boundary = item["conditional_obligation_boundary"]
        equivalence = item["equivalence"]
        review = item["accepting_incremental_review"]
        csv_extra = item["_csv"]
        row = {
            "input_order": item["input_order"],
            "target": item["target"],
            "semantic_family": item["semantic_family"],
            "active_contract_sha256": item["authority"][
                "active_contract_sha256"
            ],
            "generated_declaration_path": csv_extra[
                "generated_declaration_path"
            ],
            "source_reference": csv_extra["source_reference"],
            "public_docs_reference": csv_extra["public_docs_reference"],
            "harness_path": csv_extra["harness_path"],
            "transformation_manifest_path": csv_extra[
                "transformation_manifest_path"
            ],
            "dependency_manifest_path": csv_extra["dependency_manifest_path"],
            "retained_implementation_proof_boundary_assumption": item[
                "retained_implementation_proof_boundary"
            ]["proof_boundary_assumption"],
            "retained_implementation_proof_trust_site_ids": ";".join(
                item["retained_implementation_proof_boundary"][
                    "all_trust_site_ids"
                ]
            ),
            "conditional_boundary_manifest_path": boundary["manifest"]["path"],
            "conditional_boundary_manifest_sha256": boundary["manifest"][
                "sha256"
            ],
            "conditional_boundary_observations_json": common.json_compact(
                boundary["shared_observations"]
            ),
            "conditional_boundary_trust_site_ids": ";".join(
                boundary["observation_trust_site_ids"]
            ),
            "conditional_boundary_exclusions_json": common.json_compact(
                boundary["excluded_fields"]
            ),
            "conditional_boundary_replacements_json": common.json_compact(
                boundary["source_backed_replacement_and_transition_fields"]
            ),
            "source_citations_json": common.json_compact(
                item["source_citations"]
            ),
            "proof_scope_json": common.json_compact(item["proof_scope"]),
            "equivalence_kind": equivalence["kind"],
            "equivalence_policy": equivalence["policy"],
            "equivalence_source_citation": equivalence["source_citation"],
            "equivalence_positive_witness": equivalence["positive_witness"],
            "equivalence_negative_witness": equivalence["negative_witness"],
            EXACT_FIELD: item["classification"][EXACT_FIELD],
            FULL_FIELD: item["classification"][FULL_FIELD],
            "exact_obligation_path": csv_extra["exact_obligation_path"],
            "exact_solver_result": csv_extra["exact_solver_result"],
            "full_obligation_path": csv_extra["full_obligation_path"],
            "full_solver_result": csv_extra["full_solver_result"],
            "witness_evidence_json": common.json_compact(
                item["replayable_witnesses"]
            ),
            "verus_evidence_json": common.json_compact(
                item["verus_evidence"]
            ),
            "accepting_incremental_review_path": review["path"],
            "accepting_incremental_review_sha256": review["sha256"],
            "accepting_incremental_review_verdict": review["verdict"],
        }
        rows.append(row)
    return rows


def _public_payload(payload: dict[str, Any]) -> dict[str, Any]:
    result = json.loads(json.dumps(payload))
    for row in result["rows"]:
        row.pop("_csv", None)
    return result


def _dossier_markdown(payload: dict[str, Any]) -> str:
    exact = payload["classification_counts"]["exact_output_determinism"]
    full = payload["classification_counts"][
        "completeness_modulo_reviewed_equivalence"
    ]
    review = payload["campaign_wide_review"]["status"]
    lines = [
        "# Slice trust-boundary conditional-completeness results",
        "",
        f"**Campaign-wide review:** `{review}`",
        "",
        "The active authority contains 120 generated Slice contracts. This "
        "dossier covers exactly the 62 active `r0_z3=unknown` rows; the 58 "
        "active UNSAT rows and 12 exact-vstd rows are excluded.",
        "",
        "The retained implementation-proof boundary and the boundary used by "
        "each new two-execution obligation are separate columns in the "
        "additive crosswalk. No retained whole-target helper is silently "
        "promoted into `Boundary_T`.",
        "",
        "| Projection | Conditional complete | Conditional incomplete | Missing source-backed model |",
        "|---|---:|---:|---:|",
        (
            f"| Exact output | {exact['conditional-complete']} | "
            f"{exact['conditional-incomplete']} | "
            f"{exact['missing-source-backed-model']} |"
        ),
        (
            f"| Full state / reviewed equivalence | "
            f"{full['conditional-complete']} | "
            f"{full['conditional-incomplete']} | "
            f"{full['missing-source-backed-model']} |"
        ),
        "",
        "The only weakened-equivalence rows are 028-030 matching-index search "
        "and 080-082 equal-key unstable sort. Rows 078-079 remain "
        "`missing-source-backed-model`; their bounded UNSAT obligations are "
        "diagnostic only and are not completeness proofs.",
        "",
        "| Order | Target | Exact output | Full state / reviewed equivalence | Boundary | Incremental review |",
        "|---:|---|---|---|---|---|",
    ]
    for row in payload["rows"]:
        boundary = row["conditional_obligation_boundary"]["manifest"]["path"]
        accepted = row["accepting_incremental_review"]["path"]
        lines.append(
            f"| {int(row['input_order']):03d} | `{row['target']}` | "
            f"`{row['classification'][EXACT_FIELD]}` | "
            f"`{row['classification'][FULL_FIELD]}` | "
            f"`{boundary}` | `{accepted}` |"
        )
    lines.extend(
        [
            "",
            "A classification of `conditional-complete` is backed by the "
            "row's direct UNSAT theorem capture. A classification of "
            "`conditional-incomplete` is backed by a fixed-input, "
            "fixed-boundary SAT model retained in the row's witness index.",
            "",
        ]
    )
    return "\n".join(lines)


def _snapshot_preserved_files() -> dict[str, list[dict[str, Any]]]:
    try:
        return preservation_policy.final_campaign_groups()
    except preservation_policy.PreservationPolicyError as exc:
        raise ReconciliationError(
            f"versioned preservation policy failed: {exc}"
        ) from exc


def ensure_preservation_baseline() -> dict[str, Any]:
    snapshot = _snapshot_preserved_files()
    if len(snapshot["frozen_inputs"]) != 320:
        raise ReconciliationError(
            "frozen input tree does not contain exactly 320 files"
        )
    provenance = _load_json(OUT / "provenance/input_provenance.json")
    if not isinstance(provenance, list) or len(provenance) != 320:
        raise ReconciliationError(
            "input provenance ledger does not contain exactly 320 rows"
        )
    for record in provenance:
        path = _validate_relative_path(
            record["frozen_path"], "input provenance frozen path"
        )
        if (
            common.sha256(path) != record["sha256"]
            or path.stat().st_size != record["bytes"]
        ):
            raise ReconciliationError(
                f"frozen input changed: {record['frozen_path']}"
            )
    payload = {
        "schema_version": 1,
        "policy": (
            "Every pre-existing evidence file, frozen input, authority-ledger "
            "file, and accepted incremental review is byte-locked. Only files "
            "under evidence/final_campaign and the additive conditional "
            "crosswalk serializations are outside this baseline."
        ),
        "groups": snapshot,
    }
    if not PRESERVATION_BASELINE.is_file():
        raise ReconciliationError("preservation baseline is missing")
    if _load_json(PRESERVATION_BASELINE) != payload:
        raise ReconciliationError("preservation baseline mismatch")
    return {
        "baseline": _artifact(PRESERVATION_BASELINE),
        "counts": {key: len(value) for key, value in snapshot.items()},
        "status": "matched",
    }


def write_artifacts() -> dict[str, Any]:
    FINAL_ROOT.mkdir(parents=True, exist_ok=True)
    common.write_json(TARGET_029_BOUNDARY, target_029.boundary_manifest())
    preservation = ensure_preservation_baseline()
    payload = build_campaign()
    public = _public_payload(payload)
    common.write_json(AGGREGATE_JSON, public)
    common.write_csv(AGGREGATE_CSV, _csv_rows(payload), CSV_FIELDS)
    dossier = {
        "schema_version": 1,
        "campaign_wide_review": payload["campaign_wide_review"],
        "authority_scope": payload["authority_scope"],
        "classification_counts": payload["classification_counts"],
        "weakened_equivalence_orders": payload["weakened_equivalence_orders"],
        "missing_source_backed_model_orders": payload[
            "missing_source_backed_model_orders"
        ],
        "retained_command_capture_count": payload[
            "retained_command_capture_count"
        ],
        "preservation": preservation,
        "crosswalk": {
            "csv": _artifact(AGGREGATE_CSV),
            "json": _artifact(AGGREGATE_JSON),
        },
    }
    common.write_json(DOSSIER_JSON, dossier)
    DOSSIER_MD.write_text(_dossier_markdown(payload))
    manifest = {
        "schema_version": 1,
        "status": "passed",
        "row_count": len(payload["rows"]),
        "classification_counts": payload["classification_counts"],
        "campaign_wide_review": payload["campaign_wide_review"]["status"],
        "preservation": preservation,
        "artifacts": {
            "target_029_boundary_manifest": _artifact(TARGET_029_BOUNDARY),
            "conditional_obligation_crosswalk_csv": _artifact(AGGREGATE_CSV),
            "conditional_obligation_crosswalk_json": _artifact(AGGREGATE_JSON),
            "results_dossier_json": _artifact(DOSSIER_JSON),
            "results_dossier_markdown": _artifact(DOSSIER_MD),
        },
    }
    common.write_json(RECONCILIATION_MANIFEST, manifest)
    validate_written_artifacts()
    return manifest


def validate_written_artifacts() -> None:
    if _load_json(TARGET_029_BOUNDARY) != target_029.boundary_manifest():
        raise ReconciliationError("target 029 boundary manifest is not deterministic")
    rebuilt = build_campaign()
    if _load_json(AGGREGATE_JSON) != _public_payload(rebuilt):
        raise ReconciliationError("aggregate JSON differs from live reconciliation")
    if common.read_csv(AGGREGATE_CSV) != _csv_rows(rebuilt):
        raise ReconciliationError("aggregate CSV differs from live reconciliation")
    dossier = _load_json(DOSSIER_JSON)
    if dossier.get("classification_counts") != rebuilt["classification_counts"]:
        raise ReconciliationError("results dossier count mismatch")
    if dossier.get("campaign_wide_review") != rebuilt["campaign_wide_review"]:
        raise ReconciliationError("results dossier review mapping mismatch")
    if DOSSIER_MD.read_text() != _dossier_markdown(rebuilt):
        raise ReconciliationError("results dossier Markdown is stale")


def main() -> None:
    manifest = write_artifacts()
    counts = manifest["classification_counts"]
    exact = counts["exact_output_determinism"]
    full = counts["completeness_modulo_reviewed_equivalence"]
    print("final_reconciliation=PASS")
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
    print(f"campaign_review={manifest['campaign_wide_review']}")


if __name__ == "__main__":
    main()
