#!/usr/bin/env python3
"""Build the additive operational-v2 reconciliation of the certified campaign."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import re
import shlex
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import campaign_common as common
import final_reconciliation as certified
import preservation_policy_v3 as preservation_policy
import preservation_policy_v8 as preservation_policy_v8


OUT = common.OUT
VERSION = "operational-v2"

BASELINE_CROSSWALK_JSON = certified.AGGREGATE_JSON
BASELINE_CROSSWALK_CSV = certified.AGGREGATE_CSV
BASELINE_MANIFEST = certified.RECONCILIATION_MANIFEST
BASELINE_DOSSIER = certified.DOSSIER_JSON
BASELINE_DOSSIER_MD = certified.DOSSIER_MD
BASELINE_PRESERVATION = certified.PRESERVATION_BASELINE
BASELINE_REVIEW = certified.FINAL_REVIEW_ACCEPTANCE
BASELINE_REVIEW_REQUEST = certified.FINAL_REVIEW_REQUEST
HISTORICAL_REVIEW_REQUEST = "review/REVIEW_REQUEST.md"
HISTORICAL_REVIEW_REQUEST_ARCHIVE = (
    OUT / "preservation/review_request_operational_v2_frozen.md"
)

V2_CROSSWALK_JSON = (
    OUT / "crosswalk/conditional_obligation_crosswalk_operational_v2.json"
)
V2_CROSSWALK_CSV = (
    OUT / "crosswalk/conditional_obligation_crosswalk_operational_v2.csv"
)
V2_ROOT = certified.FINAL_ROOT / "operational_v2"
V2_DOSSIER_JSON = V2_ROOT / "results_dossier.json"
V2_DOSSIER_MD = V2_ROOT / "results_dossier.md"
V2_MANIFEST = V2_ROOT / "reconciliation_manifest.json"
PIPELINE_STATE = OUT / "research/PIPELINE_STATE.json"

EXACT_FIELD = certified.EXACT_FIELD
FULL_FIELD = certified.FULL_FIELD
CLASSIFICATIONS = (
    "conditional-complete",
    "conditional-incomplete",
    "missing-source-backed-model",
)
EXPECTED_BASELINE_EXACT = {
    "conditional-complete": 48,
    "conditional-incomplete": 12,
    "missing-source-backed-model": 2,
}
EXPECTED_BASELINE_FULL = {
    "conditional-complete": 41,
    "conditional-incomplete": 19,
    "missing-source-backed-model": 2,
}
EXPECTED_V2_EXACT = {
    "conditional-complete": 50,
    "conditional-incomplete": 12,
    "missing-source-backed-model": 0,
}
EXPECTED_V2_FULL = {
    "conditional-complete": 43,
    "conditional-incomplete": 19,
    "missing-source-backed-model": 0,
}
OVERLAY_SPECS = {
    "78": {
        "target": "core::slice::select_nth_unstable_by",
        "json": OUT / "crosswalk/target_078_operational_v1_addendum.json",
        "csv": OUT / "crosswalk/target_078_operational_v1_addendum.csv",
    },
    "79": {
        "target": "core::slice::select_nth_unstable_by_key",
        "json": OUT / "crosswalk/target_079_operational_v1_addendum.json",
        "csv": OUT / "crosswalk/target_079_operational_v1_addendum.csv",
    },
}

CSV_FIELDS = [
    "input_order",
    "target",
    "semantic_family",
    "active_contract_sha256",
    "baseline_exact_output_determinism_status",
    "effective_exact_output_determinism_status",
    "baseline_completeness_modulo_reviewed_equivalence_status",
    "effective_completeness_modulo_reviewed_equivalence_status",
    "classification_source_kind",
    "model_id",
    "addendum_path",
    "result_manifest_path",
    "accepting_review_path",
    "exact_obligation_path",
    "full_obligation_path",
    "nonvacuity_path",
]


class OperationalV2Error(ValueError):
    pass


class _HistoricalArtifactPath(type(Path())):
    """Keep a legacy logical path while reading its frozen archive."""

    __slots__ = ("_archive_path",)

    def __new__(
        cls, logical_path: Path, archive_path: Path
    ) -> "_HistoricalArtifactPath":
        return super().__new__(cls, logical_path)

    def __init__(self, logical_path: Path, archive_path: Path) -> None:
        super().__init__(logical_path)
        self._archive_path = archive_path

    def open(self, *args: Any, **kwargs: Any):
        return self._archive_path.open(*args, **kwargs)

    def stat(self, *, follow_symlinks: bool = True):
        return self._archive_path.stat(follow_symlinks=follow_symlinks)

    def resolve(self, strict: bool = False) -> Path:
        return Path(str(self)).resolve(strict=strict)


def _load_json(path: Path) -> Any:
    with path.open() as handle:
        return json.load(handle)


def _artifact(path: Path) -> dict[str, Any]:
    return {
        "path": common.relpath(path),
        "sha256": common.sha256(path),
        "bytes": path.stat().st_size,
    }


def _canonical_order(value: Any, label: str) -> str:
    if isinstance(value, bool):
        raise OperationalV2Error(f"{label}: boolean is not an input order")
    try:
        order = str(int(str(value)))
    except (TypeError, ValueError) as exc:
        raise OperationalV2Error(f"{label}: invalid input order {value!r}") from exc
    if int(order) <= 0:
        raise OperationalV2Error(f"{label}: input order must be positive")
    return order


def _relative_file(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise OperationalV2Error(f"{label}: expected a relative artifact path")
    path = (OUT / value).resolve()
    try:
        path.relative_to(OUT.resolve())
    except ValueError as exc:
        raise OperationalV2Error(f"{label}: path escapes experiment root") from exc
    if not path.is_file():
        raise OperationalV2Error(f"{label}: missing file {value}")
    if common.relpath(path) != value:
        raise OperationalV2Error(f"{label}: path is not canonical")
    if (
        value == HISTORICAL_REVIEW_REQUEST
        and label.startswith("certification protection prior_reviews[")
    ):
        if not HISTORICAL_REVIEW_REQUEST_ARCHIVE.is_file():
            raise OperationalV2Error(
                f"{label}: frozen historical review request is missing"
            )
        return _HistoricalArtifactPath(
            path, HISTORICAL_REVIEW_REQUEST_ARCHIVE
        )
    return path


def _validate_artifact(
    record: Any,
    label: str,
    *,
    expected_path: Path | None = None,
) -> Path:
    if not isinstance(record, dict) or not {
        "path",
        "sha256",
        "bytes",
    } <= set(record):
        raise OperationalV2Error(f"{label}: malformed artifact record")
    path = _relative_file(record["path"], label)
    if expected_path is not None and path != expected_path.resolve():
        raise OperationalV2Error(f"{label}: unexpected artifact path")
    identity_path = (
        preservation_policy_v8.historical_identity_path(
            record, path, root=OUT
        )
        or path
    )
    if (
        record["sha256"] != common.sha256(identity_path)
        or record["bytes"] != identity_path.stat().st_size
    ):
        raise OperationalV2Error(f"{label}: artifact hash or size mismatch")
    return path


def _require_accept_review(text: str, target: str | None, label: str) -> None:
    if not re.search(r"^\*\*VERDICT: ACCEPT\*\*$", text, re.MULTILINE):
        raise OperationalV2Error(f"{label}: independent review is not ACCEPT")
    if target is not None and target not in text:
        raise OperationalV2Error(f"{label}: review does not name {target}")


def _counts(rows: Iterable[dict[str, Any]], field: str) -> dict[str, int]:
    observed = Counter(row["effective_classification"][field] for row in rows)
    return {name: observed[name] for name in CLASSIFICATIONS}


def _validate_recorded_preservation() -> dict[str, Any]:
    payload = _load_json(BASELINE_PRESERVATION)
    groups = payload.get("groups")
    if payload.get("schema_version") != 1 or not isinstance(groups, dict):
        raise OperationalV2Error("certified preservation baseline is malformed")
    expected_counts = {
        "preexisting_evidence": 6844,
        "frozen_inputs": 320,
        "authority_ledgers": 9,
        "accepted_incremental_reviews": 29,
    }
    if {name: len(records) for name, records in groups.items()} != expected_counts:
        raise OperationalV2Error("certified preservation group counts drifted")
    for group, records in groups.items():
        seen: set[str] = set()
        for index, record in enumerate(records):
            _validate_artifact(record, f"baseline preservation {group}[{index}]")
            path = record["path"]
            if path in seen:
                raise OperationalV2Error(
                    f"baseline preservation {group}: duplicate path {path}"
                )
            seen.add(path)
    frozen_now = {
        common.relpath(path)
        for path in (OUT / "provenance/frozen").rglob("*")
        if path.is_file()
    }
    frozen_recorded = {
        record["path"] for record in groups["frozen_inputs"]
    }
    if frozen_now != frozen_recorded:
        raise OperationalV2Error("frozen input tree membership drifted")
    return {
        "baseline": _artifact(BASELINE_PRESERVATION),
        "counts": expected_counts,
        "status": "matched",
    }


def _validate_baseline_scope(payload: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise OperationalV2Error("certified campaign crosswalk is malformed")
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 62:
        raise OperationalV2Error("certified campaign must contain 62 rows")
    authority = payload.get("authority_scope")
    if not isinstance(authority, dict) or {
        "generated_slice_contracts": authority.get("generated_slice_contracts"),
        "selected_r0_unknown": authority.get("selected_r0_unknown"),
        "active_r0_unsat_excluded": authority.get("active_r0_unsat_excluded"),
        "exact_vstd_excluded": authority.get("exact_vstd_excluded"),
    } != {
        "generated_slice_contracts": 120,
        "selected_r0_unknown": 62,
        "active_r0_unsat_excluded": 58,
        "exact_vstd_excluded": 12,
    }:
        raise OperationalV2Error("certified campaign authority scope drifted")
    by_order: dict[str, dict[str, Any]] = {}
    targets: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise OperationalV2Error("certified campaign row is malformed")
        order = _canonical_order(row.get("input_order"), "baseline row")
        target = row.get("target")
        if (
            order in by_order
            or not isinstance(target, str)
            or not target.startswith("core::slice::")
            or target in targets
        ):
            raise OperationalV2Error(
                "certified campaign has duplicate or out-of-scope rows"
            )
        classification = row.get("classification")
        if (
            not isinstance(classification, dict)
            or classification.get(EXACT_FIELD) not in CLASSIFICATIONS
            or classification.get(FULL_FIELD) not in CLASSIFICATIONS
        ):
            raise OperationalV2Error(
                f"baseline row {order}: invalid classification"
            )
        authority_row = row.get("authority")
        if (
            not isinstance(authority_row, dict)
            or authority_row.get("active_r0_z3") != "unknown"
            or not authority_row.get("active_contract_sha256")
            or not authority_row.get("active_contract_text")
        ):
            raise OperationalV2Error(
                f"baseline row {order}: invalid authority binding"
            )
        by_order[order] = row
        targets.add(target)
    exact = Counter(row["classification"][EXACT_FIELD] for row in rows)
    full = Counter(row["classification"][FULL_FIELD] for row in rows)
    if dict(exact) != EXPECTED_BASELINE_EXACT:
        raise OperationalV2Error("certified exact-output counts drifted")
    if dict(full) != EXPECTED_BASELINE_FULL:
        raise OperationalV2Error("certified reviewed-equivalence counts drifted")
    if set(payload.get("missing_source_backed_model_orders", [])) != {"78", "79"}:
        raise OperationalV2Error("certified missing-model set drifted")
    for order, spec in OVERLAY_SPECS.items():
        row = by_order.get(order)
        if row is None or row["target"] != spec["target"]:
            raise OperationalV2Error(
                f"certified row {order}: target identity drifted"
            )
        if row["classification"] != {
            EXACT_FIELD: "missing-source-backed-model",
            FULL_FIELD: "missing-source-backed-model",
        }:
            raise OperationalV2Error(
                f"certified row {order}: no longer an overlay candidate"
            )
    return by_order


def _load_certified_campaign() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = _load_json(BASELINE_MANIFEST)
    dossier = _load_json(BASELINE_DOSSIER)
    if (
        manifest.get("schema_version") != 1
        or manifest.get("status") != "passed"
        or manifest.get("campaign_wide_review") != "accepted"
        or manifest.get("row_count") != 62
    ):
        raise OperationalV2Error("certified reconciliation manifest drifted")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        raise OperationalV2Error("certified reconciliation artifacts are missing")
    _validate_artifact(
        artifacts.get("conditional_obligation_crosswalk_json"),
        "certified JSON crosswalk",
        expected_path=BASELINE_CROSSWALK_JSON,
    )
    _validate_artifact(
        artifacts.get("conditional_obligation_crosswalk_csv"),
        "certified CSV crosswalk",
        expected_path=BASELINE_CROSSWALK_CSV,
    )
    _validate_artifact(
        artifacts.get("results_dossier_json"),
        "certified results dossier",
        expected_path=BASELINE_DOSSIER,
    )
    _validate_artifact(
        artifacts.get("results_dossier_markdown"),
        "certified Markdown dossier",
        expected_path=BASELINE_DOSSIER_MD,
    )
    baseline = _load_json(BASELINE_CROSSWALK_JSON)
    by_order = _validate_baseline_scope(baseline)
    if (
        dossier.get("classification_counts")
        != baseline.get("classification_counts")
        or manifest.get("classification_counts")
        != baseline.get("classification_counts")
    ):
        raise OperationalV2Error("certified campaign count records diverge")
    review = baseline.get("campaign_wide_review", {}).get("acceptance")
    review_path = _validate_artifact(
        review, "certified campaign review", expected_path=BASELINE_REVIEW
    )
    _require_accept_review(
        review_path.read_text(), None, "certified campaign review"
    )
    preservation = _validate_recorded_preservation()
    return baseline, {
        "crosswalk_json": _artifact(BASELINE_CROSSWALK_JSON),
        "crosswalk_csv": _artifact(BASELINE_CROSSWALK_CSV),
        "reconciliation_manifest": _artifact(BASELINE_MANIFEST),
        "results_dossier": _artifact(BASELINE_DOSSIER),
        "campaign_review": _artifact(BASELINE_REVIEW),
        "preservation": preservation,
        "rows_by_order": by_order,
    }


def _read_single_csv(path: Path, label: str) -> dict[str, str]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise OperationalV2Error(f"{label}: expected exactly one CSV row")
    return rows[0]


def _validate_addendum_identity(
    addendum: Any,
    csv_row: dict[str, str],
    baseline_row: dict[str, Any],
    order: str,
) -> None:
    spec = OVERLAY_SPECS[order]
    authority = baseline_row["authority"]
    expected_classification = {
        EXACT_FIELD: "conditional-complete",
        FULL_FIELD: "conditional-complete",
    }
    if (
        not isinstance(addendum, dict)
        or addendum.get("schema_version") != 1
        or _canonical_order(addendum.get("input_order"), "addendum") != order
        or addendum.get("target") != spec["target"]
        or addendum.get("active_contract_sha256")
        != authority["active_contract_sha256"]
        or addendum.get("baseline_classification")
        != baseline_row["classification"]
        or addendum.get("additive_classification")
        != expected_classification
        or addendum.get("equivalence_kind")
        != "exact-principal-return-and-final-state"
        or addendum.get("baseline_row_mutated") is not False
        or addendum.get("manager_stage_mutated") is not False
    ):
        raise OperationalV2Error(
            f"overlay {order}: target/order/contract/classification mismatch"
        )
    evidence_root = addendum.get("evidence_root")
    review = addendum.get("independent_review")
    if not isinstance(evidence_root, str) or not isinstance(review, str):
        raise OperationalV2Error(f"overlay {order}: evidence paths are malformed")
    expected_csv = {
        "input_order": order,
        "target": spec["target"],
        "model_id": addendum["model_id"],
        "active_contract_sha256": authority["active_contract_sha256"],
        "baseline_exact_output_determinism_status": (
            baseline_row["classification"][EXACT_FIELD]
        ),
        "baseline_completeness_modulo_reviewed_equivalence_status": (
            baseline_row["classification"][FULL_FIELD]
        ),
        "additive_exact_output_determinism_status": (
            expected_classification[EXACT_FIELD]
        ),
        "additive_completeness_modulo_reviewed_equivalence_status": (
            expected_classification[FULL_FIELD]
        ),
        "equivalence_kind": addendum["equivalence_kind"],
        "evidence_root": evidence_root,
        "independent_review": review,
    }
    if csv_row != expected_csv:
        raise OperationalV2Error(f"overlay {order}: JSON and CSV diverge")


def _validate_capture(
    capture: Any,
    label: str,
    *,
    expected_solver_result: str | None = None,
    expected_input: Path | None = None,
) -> dict[str, Any]:
    required = {
        "argv",
        "command",
        "stdout",
        "stderr",
        "status",
        "exit_code",
    }
    if not isinstance(capture, dict) or not required <= set(capture):
        raise OperationalV2Error(f"{label}: incomplete command capture")
    argv = capture["argv"]
    if (
        not isinstance(argv, list)
        or not argv
        or not all(isinstance(arg, str) and arg for arg in argv)
    ):
        raise OperationalV2Error(f"{label}: malformed argv")
    command = _relative_file(capture["command"], f"{label} command")
    stdout = _relative_file(capture["stdout"], f"{label} stdout")
    stderr = _relative_file(capture["stderr"], f"{label} stderr")
    status = _relative_file(capture["status"], f"{label} status")
    if (
        capture["exit_code"] != 0
        or status.read_text() != "0\n"
        or stderr.read_text() != ""
        or command.read_text() != shlex.join(argv) + "\n"
    ):
        raise OperationalV2Error(f"{label}: command did not complete cleanly")
    if expected_input is not None:
        resolved_args = {
            Path(arg).resolve()
            for arg in argv[1:]
            if not arg.startswith("-")
        }
        if expected_input.resolve() not in resolved_args:
            raise OperationalV2Error(
                f"{label}: capture did not execute the retained artifact"
            )
    if expected_solver_result is not None:
        if (
            Path(argv[0]).name != "z3"
            or capture.get("expected_solver_result") != expected_solver_result
            or capture.get("solver_result") != expected_solver_result
            or stdout.read_text() != expected_solver_result + "\n"
        ):
            raise OperationalV2Error(
                f"{label}: expected direct clean {expected_solver_result.upper()}"
            )
    return copy.deepcopy(capture)


def _validate_obligation(
    result: dict[str, Any],
    projection: str,
    identity: dict[str, str],
) -> dict[str, Any]:
    prefix = "exact-" if projection == "exact" else "completeness-modulo-"
    obligations = result.get("obligations")
    if not isinstance(obligations, dict):
        raise OperationalV2Error("operational result obligations are malformed")
    matches = [
        (name, evidence)
        for name, evidence in obligations.items()
        if name.startswith(prefix)
    ]
    if len(matches) != 1:
        raise OperationalV2Error(
            f"overlay {identity['input_order']} {projection}: "
            "requires exactly one direct obligation"
        )
    name, evidence = matches[0]
    if not isinstance(evidence, dict):
        raise OperationalV2Error(f"{name}: malformed obligation evidence")
    metadata_path = _validate_artifact(
        evidence.get("metadata"), f"{name} metadata"
    )
    smt_path = _validate_artifact(evidence.get("smt"), f"{name} SMT")
    metadata = _load_json(metadata_path)
    if (
        _canonical_order(metadata.get("input_order"), name)
        != identity["input_order"]
        or metadata.get("target") != identity["target"]
        or metadata.get("active_contract_sha256")
        != identity["active_contract_sha256"]
        or metadata.get("model_id") != identity["model_id"]
        or metadata.get("classification_eligible") is not True
        or metadata.get("expected_solver_result") != "unsat"
        or not metadata.get("executable_source_model")
    ):
        raise OperationalV2Error(f"{name}: direct obligation metadata mismatch")
    capture = _validate_capture(
        evidence.get("solver"),
        f"{name} solver",
        expected_solver_result="unsat",
        expected_input=smt_path,
    )
    return {
        "purpose": name,
        "metadata": _artifact(metadata_path),
        "smt": _artifact(smt_path),
        "solver": capture,
    }


def _validate_nonvacuity(result: dict[str, Any], order: str) -> dict[str, Any]:
    nonvacuity = result.get("nonvacuity")
    if not isinstance(nonvacuity, dict):
        raise OperationalV2Error(f"overlay {order}: nonvacuity evidence is missing")
    smt_path = _validate_artifact(
        nonvacuity.get("smt"), f"overlay {order} nonvacuity SMT"
    )
    capture = _validate_capture(
        nonvacuity.get("solver"),
        f"overlay {order} nonvacuity solver",
        expected_solver_result="sat",
        expected_input=smt_path,
    )
    return {"smt": _artifact(smt_path), "solver": capture}


def _validate_verus(result: dict[str, Any], order: str) -> dict[str, Any]:
    verus = result.get("verus")
    if not isinstance(verus, dict):
        raise OperationalV2Error(f"overlay {order}: Verus evidence is missing")
    source_path = _validate_artifact(
        verus.get("source_model"), f"overlay {order} Verus source"
    )
    captured_path = _validate_artifact(
        verus.get("captured_model"), f"overlay {order} captured Verus source"
    )
    if (
        common.sha256(source_path) != common.sha256(captured_path)
        or "external_body" in source_path.read_text()
    ):
        raise OperationalV2Error(
            f"overlay {order}: Verus source is not the retained trusted-free model"
        )
    typecheck = _validate_capture(
        verus.get("typecheck"),
        f"overlay {order} Verus typecheck",
        expected_input=captured_path,
    )
    verification = _validate_capture(
        verus.get("verification"),
        f"overlay {order} Verus verification",
        expected_input=captured_path,
    )
    if (
        Path(typecheck["argv"][0]).name != "verus"
        or "--no-verify" not in typecheck["argv"]
        or Path(verification["argv"][0]).name != "verus"
        or "--no-verify" in verification["argv"]
    ):
        raise OperationalV2Error(f"overlay {order}: Verus command mismatch")
    expected = verus.get("expected_summary")
    verification_stdout = _relative_file(
        verification["stdout"], f"overlay {order} Verus verification stdout"
    ).read_text()
    if not isinstance(expected, str) or expected not in verification_stdout:
        raise OperationalV2Error(
            f"overlay {order}: Verus verification summary mismatch"
        )
    return {
        "source_model": _artifact(source_path),
        "captured_model": _artifact(captured_path),
        "expected_summary": expected,
        "typecheck": typecheck,
        "verification": verification,
    }


def _validate_operational_result(
    result: Any,
    result_path: Path,
    addendum: dict[str, Any],
    baseline_row: dict[str, Any],
    order: str,
) -> dict[str, Any]:
    if not isinstance(result, dict):
        raise OperationalV2Error(f"overlay {order}: result is malformed")
    authority = baseline_row["authority"]
    identity = {
        "input_order": order,
        "target": baseline_row["target"],
        "active_contract_sha256": authority["active_contract_sha256"],
        "model_id": addendum["model_id"],
    }
    expected_classification = {
        EXACT_FIELD: "conditional-complete",
        FULL_FIELD: "conditional-complete",
    }
    if (
        result.get("schema_version") != 1
        or _canonical_order(result.get("input_order"), "operational result")
        != order
        or result.get("target") != identity["target"]
        or result.get("active_contract_sha256")
        != identity["active_contract_sha256"]
        or result.get("active_contract_text") != authority["active_contract_text"]
        or result.get("model_id") != identity["model_id"]
        or result.get("classification") != expected_classification
        or result.get("classification_eligible") is not True
        or result.get("source_model_complete") is not True
        or result.get("unresolved_source_model_phases") != []
        or result.get("stage_transition") != "disabled"
    ):
        raise OperationalV2Error(
            f"overlay {order}: operational result identity or eligibility mismatch"
        )
    if set(result.get("obligations", {})) != {
        name
        for name in result.get("obligations", {})
        if name.startswith("exact-") or name.startswith("completeness-modulo-")
    } or len(result["obligations"]) != 2:
        raise OperationalV2Error(
            f"overlay {order}: duplicate or unsupported classifying obligation"
        )
    try:
        certified._validate_artifacts(result, f"overlay {order} result")
    except certified.ReconciliationError as exc:
        raise OperationalV2Error(str(exc)) from exc
    addendum_links = result.get("crosswalk_addendum")
    if (
        not isinstance(addendum_links, dict)
        or addendum_links.get("certified_ledger_mutated") is not False
    ):
        raise OperationalV2Error(
            f"overlay {order}: certified-ledger preservation flag is invalid"
        )
    spec = OVERLAY_SPECS[order]
    _validate_artifact(
        addendum_links.get("json"),
        f"overlay {order} JSON addendum link",
        expected_path=spec["json"],
    )
    _validate_artifact(
        addendum_links.get("csv"),
        f"overlay {order} CSV addendum link",
        expected_path=spec["csv"],
    )
    review = result.get("independent_review")
    if (
        not isinstance(review, dict)
        or review.get("status") != "accepted"
        or review.get("verdict") != "ACCEPT"
    ):
        raise OperationalV2Error(f"overlay {order}: review result is not ACCEPT")
    review_path = _validate_artifact(
        review.get("addendum"),
        f"overlay {order} review artifact",
        expected_path=OUT / addendum["independent_review"],
    )
    _require_accept_review(
        review_path.read_text(), identity["target"], f"overlay {order} review"
    )
    preservation = result.get("preservation")
    if not isinstance(preservation, dict):
        raise OperationalV2Error(
            f"overlay {order}: preservation evidence is missing"
        )
    for key, value in preservation.items():
        if key.endswith("_unchanged") and value is not True:
            raise OperationalV2Error(
                f"overlay {order}: preservation flag {key} is not true"
            )
        if key.endswith("_mutated") and value is not False:
            raise OperationalV2Error(
                f"overlay {order}: preservation flag {key} is not false"
            )
    exact = _validate_obligation(result, "exact", identity)
    full = _validate_obligation(result, "full", identity)
    nonvacuity = _validate_nonvacuity(result, order)
    verus = _validate_verus(result, order)
    return {
        "kind": "accepted-operational-v1-overlay",
        "model_id": identity["model_id"],
        "equivalence_kind": addendum["equivalence_kind"],
        "addendum": {
            "json": _artifact(spec["json"]),
            "csv": _artifact(spec["csv"]),
        },
        "result_manifest": _artifact(result_path),
        "accepting_review": _artifact(review_path),
        "classification_basis": result.get("classification_basis"),
        "direct_evidence": {
            "exact_output": exact,
            "reviewed_equivalence": full,
            "nonvacuity": nonvacuity,
        },
        "verus": verus,
    }


def _discover_overlay_paths() -> tuple[Path, ...]:
    lifecycles = (
        preservation_policy.target_080_lifecycle(),
        preservation_policy.target_081_lifecycle(),
        preservation_policy_v8.target_082_lifecycle(),
    )
    expected_json = {
        spec["json"].resolve() for spec in OVERLAY_SPECS.values()
    }
    expected_csv = {
        spec["csv"].resolve() for spec in OVERLAY_SPECS.values()
    }
    registered_json = {
        (
            OUT / lifecycle["registered_addenda"]["json"]["path"]
        ).resolve()
        for lifecycle in lifecycles
    }
    registered_csv = {
        (
            OUT / lifecycle["registered_addenda"]["csv"]["path"]
        ).resolve()
        for lifecycle in lifecycles
    }
    actual_json = {
        path.resolve()
        for path in (OUT / "crosswalk").glob(
            "target_*_operational_v1_addendum.json"
        )
    }
    actual_csv = {
        path.resolve()
        for path in (OUT / "crosswalk").glob(
            "target_*_operational_v1_addendum.csv"
        )
    }
    if (
        any(
            lifecycle["selected_as_operational_v2_overlay"] is not False
            for lifecycle in lifecycles
        )
        or len(registered_json) != len(lifecycles)
        or len(registered_csv) != len(lifecycles)
        or actual_json != expected_json | registered_json
        or actual_csv != expected_csv | registered_csv
    ):
        raise OperationalV2Error(
            "operational-v1 overlay discovery found missing or unsupported addenda"
        )
    return tuple(sorted(expected_json))


def _load_overlays(
    baseline_by_order: dict[str, dict[str, Any]],
    paths: Iterable[Path] | None = None,
) -> dict[str, dict[str, Any]]:
    selected = tuple(paths) if paths is not None else _discover_overlay_paths()
    resolved = [path.resolve() for path in selected]
    if len(resolved) != len(set(resolved)):
        raise OperationalV2Error("duplicate operational-v1 overlay path")
    expected_paths = {
        spec["json"].resolve(): order
        for order, spec in OVERLAY_SPECS.items()
    }
    if set(resolved) != set(expected_paths):
        raise OperationalV2Error("missing or unsupported operational-v1 overlay")
    overlays: dict[str, dict[str, Any]] = {}
    for path in sorted(resolved):
        order = expected_paths[path]
        spec = OVERLAY_SPECS[order]
        addendum = _load_json(path)
        csv_row = _read_single_csv(spec["csv"], f"overlay {order}")
        baseline_row = baseline_by_order[order]
        _validate_addendum_identity(
            addendum, csv_row, baseline_row, order
        )
        result_path = _relative_file(
            f"{addendum['evidence_root']}/result.json",
            f"overlay {order} result",
        )
        result = _load_json(result_path)
        source = _validate_operational_result(
            result, result_path, addendum, baseline_row, order
        )
        overlays[order] = {
            "classification": copy.deepcopy(
                addendum["additive_classification"]
            ),
            "source": source,
        }
    if set(overlays) != set(OVERLAY_SPECS):
        raise OperationalV2Error("operational-v1 overlay set is incomplete")
    return overlays


def _validate_effective_payload(payload: Any) -> None:
    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != 2
        or payload.get("campaign_version") != VERSION
    ):
        raise OperationalV2Error("operational-v2 crosswalk is malformed")
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 62:
        raise OperationalV2Error("operational-v2 crosswalk must contain 62 rows")
    orders = [_canonical_order(row.get("input_order"), "v2 row") for row in rows]
    targets = [row.get("target") for row in rows]
    if len(set(orders)) != 62 or len(set(targets)) != 62:
        raise OperationalV2Error("operational-v2 rows are not one-to-one")
    overlay_orders = {
        row["input_order"]
        for row in rows
        if row.get("classification_source", {}).get("kind")
        == "accepted-operational-v1-overlay"
    }
    if overlay_orders != set(OVERLAY_SPECS):
        raise OperationalV2Error("operational-v2 overlay scope drifted")
    for row in rows:
        baseline = row.get("campaign_row")
        if (
            not isinstance(baseline, dict)
            or baseline.get("input_order") != row["input_order"]
            or baseline.get("target") != row["target"]
            or baseline.get("authority", {}).get("active_contract_sha256")
            != row.get("active_contract_sha256")
        ):
            raise OperationalV2Error(
                f"v2 row {row.get('input_order')}: baseline binding mismatch"
            )
        if row["input_order"] in OVERLAY_SPECS:
            expected = {
                EXACT_FIELD: "conditional-complete",
                FULL_FIELD: "conditional-complete",
            }
        else:
            expected = baseline["classification"]
            if row.get("classification_source", {}).get("kind") != (
                "certified-baseline"
            ):
                raise OperationalV2Error(
                    f"v2 row {row['input_order']}: unsupported overlay"
                )
        if row.get("effective_classification") != expected:
            raise OperationalV2Error(
                f"v2 row {row['input_order']}: effective classification mismatch"
            )
    exact = _counts(rows, EXACT_FIELD)
    full = _counts(rows, FULL_FIELD)
    if exact != EXPECTED_V2_EXACT or full != EXPECTED_V2_FULL:
        raise OperationalV2Error(
            f"operational-v2 classification count mismatch: "
            f"exact={exact}, full={full}"
        )
    if payload.get("classification_counts") != {
        "exact_output_determinism": exact,
        "completeness_modulo_reviewed_equivalence": full,
    }:
        raise OperationalV2Error("operational-v2 recorded counts are stale")
    if payload.get("missing_source_backed_model_orders") != []:
        raise OperationalV2Error("operational-v2 still records missing models")


def build_crosswalk(
    overlay_paths: Iterable[Path] | None = None,
) -> dict[str, Any]:
    baseline, certification = _load_certified_campaign()
    baseline_by_order = certification.pop("rows_by_order")
    overlays = _load_overlays(baseline_by_order, overlay_paths)
    rows: list[dict[str, Any]] = []
    for baseline_row in baseline["rows"]:
        order = baseline_row["input_order"]
        if order in overlays:
            classification = overlays[order]["classification"]
            source = overlays[order]["source"]
        else:
            classification = copy.deepcopy(baseline_row["classification"])
            source = {
                "kind": "certified-baseline",
                "result_manifest": copy.deepcopy(
                    baseline_row["result_manifest"]
                ),
                "accepting_review": copy.deepcopy(
                    baseline_row["accepting_incremental_review"]
                ),
            }
        rows.append(
            {
                "input_order": order,
                "target": baseline_row["target"],
                "semantic_family": baseline_row["semantic_family"],
                "active_contract_sha256": baseline_row["authority"][
                    "active_contract_sha256"
                ],
                "campaign_row": copy.deepcopy(baseline_row),
                "effective_classification": copy.deepcopy(classification),
                "classification_source": copy.deepcopy(source),
            }
        )
    payload = {
        "schema_version": 2,
        "campaign_version": VERSION,
        "status": "ready-for-independent-review",
        "authority_scope": copy.deepcopy(baseline["authority_scope"]),
        "theorem": copy.deepcopy(baseline["theorem"]),
        "weakened_equivalence_orders": copy.deepcopy(
            baseline["weakened_equivalence_orders"]
        ),
        "derived_from": certification,
        "overlay_orders": sorted(OVERLAY_SPECS, key=int),
        "classification_counts": {
            "exact_output_determinism": _counts(rows, EXACT_FIELD),
            "completeness_modulo_reviewed_equivalence": _counts(
                rows, FULL_FIELD
            ),
        },
        "missing_source_backed_model_orders": [],
        "independent_review": {
            "required": True,
            "status": "pending",
            "stage_transition": "disabled",
        },
        "rows": rows,
    }
    _validate_effective_payload(payload)
    return payload


def _csv_rows(payload: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in payload["rows"]:
        baseline = row["campaign_row"]
        source = row["classification_source"]
        evidence = source.get("direct_evidence", {})
        rows.append(
            {
                "input_order": row["input_order"],
                "target": row["target"],
                "semantic_family": row["semantic_family"],
                "active_contract_sha256": row["active_contract_sha256"],
                "baseline_exact_output_determinism_status": (
                    baseline["classification"][EXACT_FIELD]
                ),
                "effective_exact_output_determinism_status": (
                    row["effective_classification"][EXACT_FIELD]
                ),
                "baseline_completeness_modulo_reviewed_equivalence_status": (
                    baseline["classification"][FULL_FIELD]
                ),
                "effective_completeness_modulo_reviewed_equivalence_status": (
                    row["effective_classification"][FULL_FIELD]
                ),
                "classification_source_kind": source["kind"],
                "model_id": source.get("model_id", ""),
                "addendum_path": source.get("addendum", {})
                .get("json", {})
                .get("path", ""),
                "result_manifest_path": source["result_manifest"]["path"],
                "accepting_review_path": source.get(
                    "accepting_review", {}
                ).get("path", ""),
                "exact_obligation_path": evidence.get(
                    "exact_output", {}
                ).get("smt", {}).get("path", ""),
                "full_obligation_path": evidence.get(
                    "reviewed_equivalence", {}
                ).get("smt", {}).get("path", ""),
                "nonvacuity_path": evidence.get("nonvacuity", {})
                .get("smt", {})
                .get("path", ""),
            }
        )
    return rows


def _walk_artifacts(value: Any) -> Iterable[Path]:
    if isinstance(value, dict):
        if {"path", "sha256", "bytes"} <= set(value):
            yield _relative_file(value["path"], "accepted package artifact")
        for child in value.values():
            yield from _walk_artifacts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_artifacts(child)


def _snapshot_preserved_files() -> dict[str, list[dict[str, Any]]]:
    try:
        review_inventory = preservation_policy.review_inventory()
    except preservation_policy.PreservationPolicyError as exc:
        raise OperationalV2Error(
            f"versioned preservation policy failed: {exc}"
        ) from exc
    certified_paths = {
        BASELINE_CROSSWALK_JSON,
        BASELINE_CROSSWALK_CSV,
        BASELINE_MANIFEST,
        BASELINE_DOSSIER,
        BASELINE_DOSSIER_MD,
        BASELINE_PRESERVATION,
        BASELINE_REVIEW,
        BASELINE_REVIEW_REQUEST,
        *(
            path
            for path in certified.FINAL_ROOT.rglob("*")
            if path.is_file() and V2_ROOT not in path.parents
        ),
    }
    accepted_paths: set[Path] = set()
    for spec in OVERLAY_SPECS.values():
        accepted_paths.update({spec["json"], spec["csv"]})
        addendum = _load_json(spec["json"])
        result_path = OUT / addendum["evidence_root"] / "result.json"
        result = _load_json(result_path)
        accepted_paths.update(_walk_artifacts(result))
        accepted_paths.update(
            path
            for path in result_path.parent.rglob("*")
            if path.is_file()
        )
        accepted_paths.add(OUT / addendum["independent_review"])
    return {
        "certified_campaign": [
            _artifact(path) for path in sorted(certified_paths)
        ],
        "accepted_operational_v1_packages": [
            _artifact(path) for path in sorted(accepted_paths)
        ],
        "prior_reviews": copy.deepcopy(review_inventory["historical"]),
        "manager_owned_state": [_artifact(PIPELINE_STATE)],
    }


def _validate_preservation_groups(groups: Any) -> None:
    expected_names = {
        "certified_campaign",
        "accepted_operational_v1_packages",
        "prior_reviews",
        "manager_owned_state",
    }
    if not isinstance(groups, dict) or set(groups) != expected_names:
        raise OperationalV2Error("operational-v2 preservation groups are malformed")
    try:
        historical_reviews = preservation_policy.review_inventory()[
            "historical"
        ]
    except preservation_policy.PreservationPolicyError as exc:
        raise OperationalV2Error(
            f"versioned preservation policy failed: {exc}"
        ) from exc
    if groups["prior_reviews"] != historical_reviews:
        raise OperationalV2Error(
            "prior reviews differ from the versioned historical inventory"
        )
    for group, records in groups.items():
        if not isinstance(records, list) or not records:
            raise OperationalV2Error(f"preservation group {group} is empty")
        paths: set[str] = set()
        for index, record in enumerate(records):
            if group != "prior_reviews":
                _validate_artifact(record, f"preservation {group}[{index}]")
            if record["path"] in paths:
                raise OperationalV2Error(
                    f"preservation group {group} has duplicate paths"
                )
            paths.add(record["path"])
    manager = groups["manager_owned_state"]
    if len(manager) != 1 or manager[0]["path"] != common.relpath(PIPELINE_STATE):
        raise OperationalV2Error("Manager-owned state lock is incomplete")


def _preservation_summary(
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


def _dossier_payload(
    payload: dict[str, Any],
    preservation: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    overlay_rows = [
        row for row in payload["rows"] if row["input_order"] in OVERLAY_SPECS
    ]
    return {
        "schema_version": 2,
        "campaign_version": VERSION,
        "status": "ready-for-independent-review",
        "row_count": len(payload["rows"]),
        "classification_counts": copy.deepcopy(
            payload["classification_counts"]
        ),
        "missing_source_backed_model_orders": [],
        "derived_from": copy.deepcopy(payload["derived_from"]),
        "overlays": [
            {
                "input_order": row["input_order"],
                "target": row["target"],
                "active_contract_sha256": row["active_contract_sha256"],
                "classification": copy.deepcopy(
                    row["effective_classification"]
                ),
                "source": copy.deepcopy(row["classification_source"]),
            }
            for row in overlay_rows
        ],
        "crosswalk": {
            "json": _artifact(V2_CROSSWALK_JSON),
            "csv": _artifact(V2_CROSSWALK_CSV),
        },
        "preservation": {
            "status": "matched",
            "groups": _preservation_summary(preservation),
        },
        "independent_review": copy.deepcopy(payload["independent_review"]),
    }


def _dossier_markdown(
    payload: dict[str, Any],
    preservation: dict[str, list[dict[str, Any]]],
) -> str:
    exact = payload["classification_counts"]["exact_output_determinism"]
    full = payload["classification_counts"][
        "completeness_modulo_reviewed_equivalence"
    ]
    lines = [
        "# Slice operational-v2 reconciliation results",
        "",
        "**Status:** `ready-for-independent-review`",
        "",
        "This additive reconciliation derives the certified 62-row campaign "
        "and overlays only the independently accepted operational-v1 results "
        "for input orders 078 and 079. The certified campaign rows remain "
        "embedded without modification.",
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
        "| Order | Target | Effective exact | Effective reviewed equivalence | Evidence | Review |",
        "|---:|---|---|---|---|---|",
    ]
    for row in payload["rows"]:
        if row["input_order"] not in OVERLAY_SPECS:
            continue
        source = row["classification_source"]
        lines.append(
            f"| {int(row['input_order']):03d} | `{row['target']}` | "
            f"`{row['effective_classification'][EXACT_FIELD]}` | "
            f"`{row['effective_classification'][FULL_FIELD]}` | "
            f"`{source['result_manifest']['path']}` | "
            f"`{source['accepting_review']['path']}` |"
        )
    lines.extend(
        [
            "",
            "Both overlays retain one direct arbitrary-domain exact-output "
            "UNSAT obligation, one direct arbitrary-domain reviewed-equivalence "
            "UNSAT obligation, one SAT nonvacuity replay, and clean Verus "
            "typecheck and verification captures.",
            "",
            "| Preserved group | Files | Inventory SHA-256 |",
            "|---|---:|---|",
        ]
    )
    summaries = _preservation_summary(preservation)
    for name in sorted(summaries):
        summary = summaries[name]
        lines.append(
            f"| `{name}` | {summary['file_count']} | "
            f"`{summary['inventory_sha256']}` |"
        )
    lines.extend(
        [
            "",
            "A new independent campaign-level review is still required. This "
            "reconciliation does not alter `research/PIPELINE_STATE.json` or "
            "authorize a stage transition.",
            "",
        ]
    )
    return "\n".join(lines)


def _manifest_payload(
    payload: dict[str, Any],
    dossier: dict[str, Any],
    preservation: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "campaign_version": VERSION,
        "status": "ready-for-independent-review",
        "row_count": len(payload["rows"]),
        "overlay_orders": sorted(OVERLAY_SPECS, key=int),
        "classification_counts": copy.deepcopy(
            payload["classification_counts"]
        ),
        "missing_source_backed_model_orders": [],
        "independent_review": copy.deepcopy(payload["independent_review"]),
        "preservation": {
            "status": "matched",
            "certified_baseline": copy.deepcopy(
                payload["derived_from"]["preservation"]
            ),
            "groups": copy.deepcopy(preservation),
            "summary": _preservation_summary(preservation),
        },
        "artifacts": {
            "operational_v2_crosswalk_json": _artifact(V2_CROSSWALK_JSON),
            "operational_v2_crosswalk_csv": _artifact(V2_CROSSWALK_CSV),
            "results_dossier_json": _artifact(V2_DOSSIER_JSON),
            "results_dossier_markdown": _artifact(V2_DOSSIER_MD),
        },
        "dossier_status": dossier["status"],
    }


def write_artifacts() -> dict[str, Any]:
    preservation_before = _snapshot_preserved_files()
    _validate_preservation_groups(preservation_before)
    if V2_MANIFEST.is_file():
        prior = _load_json(V2_MANIFEST).get("preservation", {}).get("groups")
        if prior != preservation_before:
            raise OperationalV2Error(
                "preserved artifacts changed since operational-v2 was emitted"
            )
    payload = build_crosswalk()
    V2_ROOT.mkdir(parents=True, exist_ok=True)
    common.write_json(V2_CROSSWALK_JSON, payload)
    common.write_csv(V2_CROSSWALK_CSV, _csv_rows(payload), CSV_FIELDS)
    dossier = _dossier_payload(payload, preservation_before)
    common.write_json(V2_DOSSIER_JSON, dossier)
    V2_DOSSIER_MD.write_text(
        _dossier_markdown(payload, preservation_before)
    )
    manifest = _manifest_payload(payload, dossier, preservation_before)
    common.write_json(V2_MANIFEST, manifest)
    if _snapshot_preserved_files() != preservation_before:
        raise OperationalV2Error(
            "operational-v2 writer mutated a preserved artifact"
        )
    validate_written_artifacts()
    return manifest


def validate_written_artifacts() -> None:
    manifest = _load_json(V2_MANIFEST)
    preservation = manifest.get("preservation", {}).get("groups")
    _validate_preservation_groups(preservation)
    if _snapshot_preserved_files() != preservation:
        raise OperationalV2Error("operational-v2 preservation lock mismatch")
    rebuilt = build_crosswalk()
    if _load_json(V2_CROSSWALK_JSON) != rebuilt:
        raise OperationalV2Error("operational-v2 JSON crosswalk is stale")
    if common.read_csv(V2_CROSSWALK_CSV) != _csv_rows(rebuilt):
        raise OperationalV2Error("operational-v2 CSV crosswalk is stale")
    dossier = _dossier_payload(rebuilt, preservation)
    if _load_json(V2_DOSSIER_JSON) != dossier:
        raise OperationalV2Error("operational-v2 JSON dossier is stale")
    if V2_DOSSIER_MD.read_text() != _dossier_markdown(
        rebuilt, preservation
    ):
        raise OperationalV2Error("operational-v2 Markdown dossier is stale")
    expected_manifest = _manifest_payload(rebuilt, dossier, preservation)
    if manifest != expected_manifest:
        raise OperationalV2Error("operational-v2 reconciliation manifest is stale")
    for name, artifact in manifest["artifacts"].items():
        _validate_artifact(artifact, f"operational-v2 output {name}")


def main() -> None:
    manifest = write_artifacts()
    exact = manifest["classification_counts"]["exact_output_determinism"]
    full = manifest["classification_counts"][
        "completeness_modulo_reviewed_equivalence"
    ]
    print("operational_v2_reconciliation=PASS")
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
    print("overlays=78,79")
    print("independent_review=pending")


if __name__ == "__main__":
    main()
