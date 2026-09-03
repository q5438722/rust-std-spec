#!/usr/bin/env python3
"""Certify the operational-v2 exactly-one-summary parser repair."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import campaign_common as common
import operational_v2_certification as certification


ROOT = common.OUT
VERSION = "operational-v2-parser-repair-certification-v1"
KIND = "operational-v2-parser-repair-certification"
CERTIFICATION_ROOT = (
    ROOT
    / "evidence/final_campaign/operational_v2"
    / "parser_repair_certification_v1"
)
CERTIFIED_REPAIR = CERTIFICATION_ROOT / "certified_parser_repair.json"
CERTIFIED_REPORT = CERTIFICATION_ROOT / "certified_parser_repair.md"
CERTIFICATION_MANIFEST = CERTIFICATION_ROOT / "certification_manifest.json"

REPAIR_IMPLEMENTATION = ROOT / "tools/operational_v2_certification.py"
REGRESSION_TESTS = ROOT / "tests/test_operational_v2_certification.py"
REVIEWER_ROOT = (
    ROOT
    / ".review-scratch"
    / "operational-v2-certification-reviewer-round3"
)

EXPECTED_COUNTS = {
    "exact_output_determinism": {
        "conditional-complete": 50,
        "conditional-incomplete": 12,
        "missing-source-backed-model": 0,
    },
    "completeness_modulo_reviewed_equivalence": {
        "conditional-complete": 43,
        "conditional-incomplete": 19,
        "missing-source-backed-model": 0,
    },
}
EXPECTED_REPAIR_IMPLEMENTATION = {
    "path": "tools/operational_v2_certification.py",
    "sha256": (
        "fedea6cc8eae66b23b9ed93446a1a2d16cacafd068787d20ceb674e0f527b5e8"
    ),
    "bytes": 33855,
}
EXPECTED_REGRESSION_TESTS = {
    "path": "tests/test_operational_v2_certification.py",
    "sha256": (
        "2169caaadb02e24883b7abebde0f32c8fc463cd1ec402833b4c13d37447ec26a"
    ),
    "bytes": 8575,
}
EXPECTED_EXISTING_CERTIFICATION = {
    "certified_projection_json": {
        "path": (
            "evidence/final_campaign/operational_v2/certified/"
            "certified_projection.json"
        ),
        "sha256": (
            "92c5d9a4c5e7baf7c8745abc5a339a6ff5d1c5238070bfd831be5ee5999f681f"
        ),
        "bytes": 195924,
    },
    "certified_projection_markdown": {
        "path": (
            "evidence/final_campaign/operational_v2/certified/"
            "certified_projection.md"
        ),
        "sha256": (
            "5de6fdca10a0c93fff7a9a83b245cf69e561dbcc53a195c93bc00c996ee8b461"
        ),
        "bytes": 1443,
    },
    "certification_manifest": {
        "path": (
            "evidence/final_campaign/operational_v2/certified/"
            "certification_manifest.json"
        ),
        "sha256": (
            "91eaa80c3975fe202efc1abae608d90499eb30009234227034a73c4375918649"
        ),
        "bytes": 3047,
    },
}
EXPECTED_PROTECTED_FILE_COUNT = 707
EXPECTED_PROTECTED_INVENTORY_SHA256 = (
    "f8f2695005085532dc8e5eb34964a22af5f09c054be1c861b6c89e6ba7f1a07b"
)

REVIEWER_TASK_ID = "operational-v2-certification-summary-r3"
REVIEWER_STARTED_AT = "2026-09-02T00:19:39.486861Z"
REVIEWER_COMPLETED_AT = "2026-09-02T00:30:23.021369Z"
REVIEWER_STATUS_AT = "2026-09-02T00:30:23.026808Z"
EXPECTED_REVIEWER_FILE_COUNT = 33
EXPECTED_REVIEWER_INVENTORY_SHA256 = (
    "9ce3eecad132e1eea0d8171a3c0d67dea6025e425ba295cfbe0df4212a15c471"
)
EXPECTED_REVIEWER_PRIMARY = {
    "manifest": {
        "path": (
            ".review-scratch/operational-v2-certification-reviewer-round3/"
            "manifest.json"
        ),
        "sha256": (
            "9eac3f3e82b9d2de84c0a2c0a8300f133d6f46df9c1eedd44075b0aefd795fba"
        ),
        "bytes": 1411,
    },
    "summary": {
        "path": (
            ".review-scratch/operational-v2-certification-reviewer-round3/"
            "summary.json"
        ),
        "sha256": (
            "6019a2b3fd1cf9bfd056b5d8bdbf9b00eaa79fbdc0b7f92813a08dbe7ab2e169"
        ),
        "bytes": 879,
    },
    "status": {
        "path": (
            ".review-scratch/operational-v2-certification-reviewer-round3/"
            "status.json"
        ),
        "sha256": (
            "2e466faa10d114ed13d4ff7d315eb15a92db426b924374e1dd8c1462ee4459fd"
        ),
        "bytes": 1097,
    },
}
REVIEW_COMMANDS = [
    "01_compileall",
    "02_focused_tests",
    "03_complete_tests",
    "04_closure",
    "05_task_native_acceptance",
]
REVIEW_TEST_COUNTS = [None, 17, 571, None, None]
REVIEW_REJECTION_CASES = [
    "missing",
    "duplicate",
    "conflicting",
    "wrong-scope",
    "wrong-count",
    "stale",
    "non-ACCEPT",
]
EXPECTED_PARSED_REVIEW = {
    "required": True,
    "status": "accepted",
    "verdict": "ACCEPT",
    "timestamp": certification.EXPECTED_REVIEW_TIMESTAMP,
    "scope": "additive-operational-v2-reconciliation",
    "row_count": 62,
    "overlay_orders": ["78", "79"],
    "classification_counts": copy.deepcopy(EXPECTED_COUNTS),
    "stage_transition": "disabled",
}


class ParserRepairCertificationError(ValueError):
    pass


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ParserRepairCertificationError(
            f"missing artifact {_display_path(path)}"
        )
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": _sha256(path),
        "bytes": path.stat().st_size,
    }


def _validate_expected_artifact(
    path: Path, expected: dict[str, Any], label: str
) -> dict[str, Any]:
    actual = _artifact(path)
    if actual != expected:
        raise ParserRepairCertificationError(f"{label} identity drifted")
    return copy.deepcopy(actual)


def _load_json(path: Path, label: str) -> Any:
    try:
        with path.open(encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError as exc:
        raise ParserRepairCertificationError(
            f"{label} is missing: {_display_path(path)}"
        ) from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ParserRepairCertificationError(
            f"{label} is malformed or unreadable"
        ) from exc


def _read_text(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ParserRepairCertificationError(
            f"{label} is missing: {_display_path(path)}"
        ) from exc
    except (OSError, UnicodeError) as exc:
        raise ParserRepairCertificationError(
            f"{label} is malformed or unreadable"
        ) from exc


def _inventory(root: Path) -> list[dict[str, Any]]:
    if not root.is_dir():
        raise ParserRepairCertificationError(
            f"reviewer evidence root is missing: {_display_path(root)}"
        )
    entries = sorted(root.rglob("*"))
    if any(path.is_symlink() for path in entries):
        raise ParserRepairCertificationError(
            "reviewer evidence inventory contains a symbolic link"
        )
    records = [_artifact(path) for path in entries if path.is_file()]
    if not records:
        raise ParserRepairCertificationError(
            "reviewer evidence inventory is empty"
        )
    return records


def _inventory_digest(records: list[dict[str, Any]]) -> str:
    encoded = json.dumps(
        records, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _parse_utc(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ParserRepairCertificationError(
            f"{label} is not an RFC3339 UTC timestamp"
        )
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ParserRepairCertificationError(
            f"{label} is not an RFC3339 UTC timestamp"
        ) from exc
    if parsed.tzinfo != UTC:
        raise ParserRepairCertificationError(f"{label} is not UTC")
    return parsed


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ParserRepairCertificationError(
            f"canonical review does not have one {label} field"
        )
    return text.replace(old, new, 1)


def review_negative_candidates(
    canonical_text: str,
) -> dict[str, str | None]:
    accepted_summary = (
        "The reconciliation reports 62 rows, overlays `78,79`, exact "
        "counts `50/12/0`, reviewed-equivalence counts `43/19/0`, and "
        "zero missing classifications."
    )
    conflicting_summary = (
        "The reconciliation reports 61 rows, overlays `78,79`, exact "
        "counts `49/12/0`, reviewed-equivalence counts `42/19/0`, and "
        "zero missing classifications."
    )
    return {
        "missing": None,
        "duplicate": f"{canonical_text}\n\n{accepted_summary}\n",
        "conflicting": f"{canonical_text}\n\n{conflicting_summary}\n",
        "wrong-scope": _replace_once(
            canonical_text,
            "additive operational-v2 reconciliation",
            "additive all-module reconciliation",
            "scope",
        ),
        "wrong-count": _replace_once(
            canonical_text,
            "reports 62 rows",
            "reports 61 rows",
            "count",
        ),
        "stale": _replace_once(
            canonical_text,
            certification.EXPECTED_REVIEW_TIMESTAMP,
            "2026-08-31T22:41:27Z",
            "timestamp",
        ),
        "non-ACCEPT": _replace_once(
            canonical_text,
            "**VERDICT: ACCEPT**",
            "**VERDICT: REJECT**",
            "verdict",
        ),
    }


def _validate_repaired_review_text(text: Any) -> dict[str, Any]:
    try:
        parsed = certification._parse_accept_review(text)
    except certification.OperationalV2CertificationError as exc:
        raise ParserRepairCertificationError(
            "review evidence was rejected"
        ) from exc
    if parsed != EXPECTED_PARSED_REVIEW:
        raise ParserRepairCertificationError(
            "review evidence is stale or semantically inconsistent"
        )
    return parsed


def _semantic_review_validation() -> dict[str, Any]:
    canonical = _read_text(
        certification.REVIEW_PATH, "canonical operational-v2 review"
    )
    parsed = _validate_repaired_review_text(canonical)
    candidates = review_negative_candidates(canonical)
    if list(candidates) != REVIEW_REJECTION_CASES:
        raise ParserRepairCertificationError(
            "review rejection case inventory drifted"
        )
    rejected: dict[str, str] = {}
    for label, candidate in candidates.items():
        try:
            _validate_repaired_review_text(candidate)
        except ParserRepairCertificationError:
            rejected[label] = "rejected"
        else:
            raise ParserRepairCertificationError(
                f"{label} review evidence was unexpectedly accepted"
            )
    return {
        "canonical_summary": {
            "status": "accepted",
            "count": 1,
            "row_count": parsed["row_count"],
            "classification_counts": copy.deepcopy(
                parsed["classification_counts"]
            ),
        },
        "rejected_review_evidence": rejected,
    }


def _flatten_protected_groups(
    groups: Any,
) -> list[dict[str, Any]]:
    if not isinstance(groups, dict):
        raise ParserRepairCertificationError(
            "existing protected-file groups are malformed"
        )
    unique: dict[str, dict[str, Any]] = {}
    for records in groups.values():
        if not isinstance(records, list):
            raise ParserRepairCertificationError(
                "existing protected-file group is malformed"
            )
        for record in records:
            if not isinstance(record, dict) or set(record) != {
                "path",
                "sha256",
                "bytes",
            }:
                raise ParserRepairCertificationError(
                    "existing protected-file record is malformed"
                )
            prior = unique.setdefault(record["path"], record)
            if prior != record:
                raise ParserRepairCertificationError(
                    "duplicate protected-file identities conflict"
                )
    flattened = [copy.deepcopy(unique[path]) for path in sorted(unique)]
    if (
        len(flattened) != EXPECTED_PROTECTED_FILE_COUNT
        or _inventory_digest(flattened)
        != EXPECTED_PROTECTED_INVENTORY_SHA256
    ):
        raise ParserRepairCertificationError(
            "existing 707-file protection inventory drifted"
        )
    return flattened


def _validate_existing_certification() -> tuple[
    dict[str, Any], dict[str, Any], list[dict[str, Any]]
]:
    paths = {
        "certified_projection_json": certification.CERTIFIED_PROJECTION,
        "certified_projection_markdown": certification.CERTIFIED_REPORT,
        "certification_manifest": certification.CERTIFICATION_MANIFEST,
    }
    artifacts = {
        name: _validate_expected_artifact(
            paths[name],
            EXPECTED_EXISTING_CERTIFICATION[name],
            f"existing {name}",
        )
        for name in paths
    }
    try:
        certification.validate_written_artifacts()
    except (
        OSError,
        ValueError,
        certification.OperationalV2CertificationError,
    ) as exc:
        raise ParserRepairCertificationError(
            "existing operational-v2 certification failed native validation"
        ) from exc
    projection = _load_json(
        certification.CERTIFIED_PROJECTION,
        "existing certified operational-v2 projection",
    )
    if (
        projection.get("row_count") != 62
        or projection.get("classification_counts") != EXPECTED_COUNTS
        or projection.get("row_projection_sha256")
        != certification.EXPECTED_ROW_PROJECTION_SHA256
    ):
        raise ParserRepairCertificationError(
            "existing certified projection classifications drifted"
        )
    protected = _flatten_protected_groups(
        projection.get("protected_inputs", {}).get("groups")
    )
    binding = {
        "status": "validated",
        "campaign_version": "operational-v2",
        "row_count": 62,
        "classification_counts": copy.deepcopy(EXPECTED_COUNTS),
        "row_projection_sha256": (
            certification.EXPECTED_ROW_PROJECTION_SHA256
        ),
        "artifacts": artifacts,
        "protected_inputs": {
            "status": "matched",
            "file_count": len(protected),
            "inventory_sha256": _inventory_digest(protected),
        },
    }
    return binding, projection, protected


def _expect_classification_drift_rejected(
    projection: dict[str, Any],
) -> None:
    corrupted = copy.deepcopy(projection)
    corrupted["rows"][0]["effective_classification"][
        certification.v2.EXACT_FIELD
    ] = "conditional-incomplete"
    try:
        certification._validate_certified_payload(corrupted)
    except certification.OperationalV2CertificationError:
        return
    raise ParserRepairCertificationError(
        "classification drift was unexpectedly accepted"
    )


def _expect_protected_drift_rejected(projection: dict[str, Any]) -> None:
    groups = copy.deepcopy(projection["protected_inputs"]["groups"])
    groups["manager_owned_state"][0]["sha256"] = "0" * 64
    try:
        certification._validate_protected_groups(groups)
    except certification.OperationalV2CertificationError:
        return
    raise ParserRepairCertificationError(
        "protected-file drift was unexpectedly accepted"
    )


def _unittest_count(text: str, label: str) -> int:
    matches = re.findall(
        r"^Ran ([0-9]+) tests? in ", text, flags=re.MULTILINE
    )
    if len(matches) != 1:
        raise ParserRepairCertificationError(
            f"{label} does not report exactly one unittest count"
        )
    return int(matches[0])


def _validate_review_command_results(summary: Any) -> None:
    if (
        not isinstance(summary, dict)
        or set(summary)
        != {
            "acceptance",
            "acceptance_commands",
            "commands",
            "protected_changed",
            "protected_extra",
            "protected_file_count",
            "protected_missing",
            "status",
        }
        or summary["acceptance"] != "PASS"
        or summary["acceptance_commands"] != 49
        or summary["protected_file_count"] != EXPECTED_PROTECTED_FILE_COUNT
        or summary["protected_changed"] != []
        or summary["protected_extra"] != []
        or summary["protected_missing"] != []
        or summary["status"] != "PASS"
    ):
        raise ParserRepairCertificationError(
            "fresh reviewer summary is not an accepted preservation replay"
        )
    results = summary["commands"]
    if not isinstance(results, list) or len(results) != len(REVIEW_COMMANDS):
        raise ParserRepairCertificationError(
            "fresh reviewer command results are incomplete"
        )
    for result, name, test_count in zip(
        results, REVIEW_COMMANDS, REVIEW_TEST_COUNTS, strict=True
    ):
        elapsed = result.get("elapsed_seconds")
        if (
            not isinstance(result, dict)
            or set(result)
            != {"elapsed_seconds", "name", "status", "test_count"}
            or result["name"] != name
            or result["status"] != 0
            or result["test_count"] != test_count
            or isinstance(elapsed, bool)
            or not isinstance(elapsed, (int, float))
            or elapsed <= 0
        ):
            raise ParserRepairCertificationError(
                f"fresh reviewer result {name} is malformed or unsuccessful"
            )


def _validate_reviewer_documents(
    manifest: Any,
    status: Any,
    summary: Any,
    classification: Any,
    direct_bytes: Any,
) -> None:
    expected_manifest_counts = {
        "focused_test_count": 17,
        "complete_test_count": 571,
        "acceptance_commands": 49,
        "protected_file_count": EXPECTED_PROTECTED_FILE_COUNT,
    }
    if (
        not isinstance(manifest, dict)
        or manifest.get("schema_version") != 1
        or manifest.get("task_id") != REVIEWER_TASK_ID
        or manifest.get("cwd") != str(ROOT)
        or manifest.get("expected") != expected_manifest_counts
        or "one unambiguous count-bearing review summary"
        not in manifest.get("objective", "")
    ):
        raise ParserRepairCertificationError(
            "fresh reviewer manifest scope or expectations drifted"
        )
    commands = manifest.get("commands")
    if (
        not isinstance(commands, list)
        or [record.get("name") for record in commands] != REVIEW_COMMANDS
        or any(
            not isinstance(record.get("command"), str)
            or not record["command"].startswith(
                "PYTHONDONTWRITEBYTECODE=1 "
            )
            for record in commands
        )
    ):
        raise ParserRepairCertificationError(
            "fresh reviewer command manifest is malformed"
        )
    _validate_review_command_results(summary)
    if (
        not isinstance(status, dict)
        or status.get("state") != "completed"
        or status.get("completed_commands") != len(REVIEW_COMMANDS)
        or status.get("total_commands") != len(REVIEW_COMMANDS)
        or status.get("updated_at") != REVIEWER_STATUS_AT
        or status.get("summary") != summary
    ):
        raise ParserRepairCertificationError(
            "fresh reviewer completion status is stale or incomplete"
        )
    expected_classification = {
        "classification_changed_rows": [],
        **copy.deepcopy(EXPECTED_COUNTS),
        "row_count": 62,
        "row_membership_extra": [],
        "row_membership_missing": [],
        "status": "PASS",
    }
    if classification != expected_classification:
        raise ParserRepairCertificationError(
            "fresh reviewer classification comparison drifted"
        )
    expected_direct = {
        "byte_changed": [],
        "comparison": "direct byte equality against pre-replay copies",
        "filesystem_missing": [],
        "membership_extra": [],
        "membership_missing": [],
        "protected_file_count": EXPECTED_PROTECTED_FILE_COUNT,
        "status": "PASS",
    }
    if direct_bytes != expected_direct:
        raise ParserRepairCertificationError(
            "fresh reviewer direct-byte comparison drifted"
        )


def _validate_reviewer_logs(summary: dict[str, Any]) -> None:
    for name in REVIEW_COMMANDS:
        if _read_text(
            REVIEWER_ROOT / name / "status.txt",
            f"fresh reviewer {name} status",
        ) != "0\n":
            raise ParserRepairCertificationError(
                f"fresh reviewer {name} did not exit successfully"
            )
    expected_closure = "\n".join(
        [
            "operational_v2_certification_closure=PASS",
            "independent_review=ACCEPT",
            "review_status=accepted",
            "rows=62",
            "exact=50/12/0",
            "full=43/19/0",
            "stage_transition=disabled",
            "",
        ]
    )
    if _read_text(
        REVIEWER_ROOT / "04_closure/stdout.txt",
        "fresh reviewer certification closure stdout",
    ) != expected_closure:
        raise ParserRepairCertificationError(
            "fresh reviewer certification closure output drifted"
        )
    expected_acceptance = "\n".join(
        [
            "acceptance=PASS",
            "commands=49",
            "slice_inventory_total=132 existing_vstd=12",
            "",
        ]
    )
    if _read_text(
        REVIEWER_ROOT / "05_task_native_acceptance/stdout.txt",
        "fresh reviewer acceptance stdout",
    ) != expected_acceptance:
        raise ParserRepairCertificationError(
            "fresh reviewer task-native acceptance output drifted"
        )
    focused = _read_text(
        REVIEWER_ROOT / "02_focused_tests/stderr.txt",
        "fresh reviewer focused-test stderr",
    )
    complete = _read_text(
        REVIEWER_ROOT / "03_complete_tests/stderr.txt",
        "fresh reviewer complete-test stderr",
    )
    regression_name = (
        "test_duplicate_or_conflicting_count_summaries_are_rejected"
    )
    if regression_name not in focused or regression_name not in complete:
        raise ParserRepairCertificationError(
            "fresh reviewer did not execute the parser regression"
        )
    if (
        _unittest_count(focused, "fresh focused tests") != 17
        or _unittest_count(complete, "fresh complete tests") != 571
        or not focused.rstrip().endswith("OK")
        or not complete.rstrip().endswith("OK")
    ):
        raise ParserRepairCertificationError(
            "fresh reviewer test counts or outcomes drifted"
        )
    if summary["commands"][1]["test_count"] != 17:
        raise ParserRepairCertificationError(
            "fresh reviewer focused-test summary is inconsistent"
        )


def _validate_reviewer_progress(summary: dict[str, Any]) -> None:
    progress_text = _read_text(
        REVIEWER_ROOT / "progress.jsonl", "fresh reviewer progress"
    )
    try:
        records = [
            json.loads(line)
            for line in progress_text.splitlines()
            if line.strip()
        ]
    except json.JSONDecodeError as exc:
        raise ParserRepairCertificationError(
            "fresh reviewer progress is malformed"
        ) from exc
    expected_events = ["run_started"]
    for _name in REVIEW_COMMANDS:
        expected_events.extend(["command_started", "command_completed"])
    expected_events.append("run_completed")
    if [record.get("event") for record in records] != expected_events:
        raise ParserRepairCertificationError(
            "fresh reviewer progress event sequence drifted"
        )
    started = [
        record.get("command_name")
        for record in records
        if record.get("event") == "command_started"
    ]
    completed = [
        record.get("name")
        for record in records
        if record.get("event") == "command_completed"
    ]
    if (
        records[0].get("task_id") != REVIEWER_TASK_ID
        or records[0].get("timestamp") != REVIEWER_STARTED_AT
        or started != REVIEW_COMMANDS
        or completed != REVIEW_COMMANDS
        or records[-1].get("timestamp") != REVIEWER_COMPLETED_AT
        or records[-1].get("summary") != summary
    ):
        raise ParserRepairCertificationError(
            "fresh reviewer progress scope or terminal result drifted"
        )
    timestamps = [
        _parse_utc(record.get("timestamp"), "fresh reviewer event timestamp")
        for record in records
    ]
    if timestamps != sorted(timestamps) or _parse_utc(
        REVIEWER_STATUS_AT, "fresh reviewer status timestamp"
    ) < timestamps[-1]:
        raise ParserRepairCertificationError(
            "fresh reviewer timestamps are inconsistent"
        )


def _validate_reviewer_bundle(
    protected: list[dict[str, Any]],
) -> dict[str, Any]:
    inventory = _inventory(REVIEWER_ROOT)
    if (
        len(inventory) != EXPECTED_REVIEWER_FILE_COUNT
        or _inventory_digest(inventory)
        != EXPECTED_REVIEWER_INVENTORY_SHA256
    ):
        raise ParserRepairCertificationError(
            "fresh reviewer evidence inventory drifted"
        )
    by_path = {record["path"]: record for record in inventory}
    for label, expected in EXPECTED_REVIEWER_PRIMARY.items():
        if by_path.get(expected["path"]) != expected:
            raise ParserRepairCertificationError(
                f"fresh reviewer {label} identity drifted"
            )
    manifest = _load_json(
        REVIEWER_ROOT / "manifest.json", "fresh reviewer manifest"
    )
    status = _load_json(
        REVIEWER_ROOT / "status.json", "fresh reviewer status"
    )
    summary = _load_json(
        REVIEWER_ROOT / "summary.json", "fresh reviewer summary"
    )
    classification = _load_json(
        REVIEWER_ROOT / "classification-comparison.json",
        "fresh reviewer classification comparison",
    )
    direct_bytes = _load_json(
        REVIEWER_ROOT / "direct-byte-comparison.json",
        "fresh reviewer direct-byte comparison",
    )
    _validate_reviewer_documents(
        manifest, status, summary, classification, direct_bytes
    )
    _validate_reviewer_logs(summary)
    _validate_reviewer_progress(summary)
    protected_paths = _load_json(
        REVIEWER_ROOT / "protected-paths.json",
        "fresh reviewer protected-path inventory",
    )
    expected_paths = [record["path"] for record in protected]
    if protected_paths != expected_paths:
        raise ParserRepairCertificationError(
            "fresh reviewer protected-path inventory drifted"
        )
    return {
        "required": True,
        "status": "accepted",
        "verdict": "ACCEPT",
        "scope": VERSION,
        "task_id": REVIEWER_TASK_ID,
        "started_at": REVIEWER_STARTED_AT,
        "completed_at": REVIEWER_COMPLETED_AT,
        "source_root": REVIEWER_ROOT.relative_to(ROOT).as_posix(),
        "replay": {
            "commands": len(REVIEW_COMMANDS),
            "focused_tests": 17,
            "complete_tests": 571,
            "task_native_acceptance_commands": 49,
            "row_count": 62,
            "classification_counts": copy.deepcopy(EXPECTED_COUNTS),
        },
        "preservation": {
            "status": "matched",
            "protected_file_count": EXPECTED_PROTECTED_FILE_COUNT,
            "changed": [],
            "missing": [],
            "extra": [],
        },
        "evidence_inventory": {
            "file_count": len(inventory),
            "inventory_sha256": _inventory_digest(inventory),
            "primary_artifacts": copy.deepcopy(EXPECTED_REVIEWER_PRIMARY),
            "files": inventory,
        },
    }


def _contains_pending(value: Any) -> bool:
    if isinstance(value, str):
        return "pending" in value.lower()
    if isinstance(value, dict):
        return any(_contains_pending(child) for child in value.values())
    if isinstance(value, list):
        return any(_contains_pending(child) for child in value)
    return False


def _validate_certification_payload(payload: Any) -> None:
    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != 1
        or payload.get("kind") != KIND
        or payload.get("certification_version") != VERSION
        or payload.get("status") != "certified"
        or payload.get("campaign_version") != "operational-v2"
        or payload.get("row_count") != 62
        or payload.get("classification_counts") != EXPECTED_COUNTS
        or payload.get("stage_transition") != "disabled"
    ):
        raise ParserRepairCertificationError(
            "parser-repair certification identity or counts drifted"
        )
    if _contains_pending(payload):
        raise ParserRepairCertificationError(
            "parser-repair certification contains pending status"
        )
    repair = payload.get("parser_repair")
    if repair != {
        "status": "validated",
        "parser": (
            "operational_v2_certification._parse_accept_review"
        ),
        "implementation": EXPECTED_REPAIR_IMPLEMENTATION,
        "regression_tests": EXPECTED_REGRESSION_TESTS,
    }:
        raise ParserRepairCertificationError(
            "parser repair implementation or regression binding drifted"
        )
    semantic = payload.get("semantic_validation")
    if (
        not isinstance(semantic, dict)
        or semantic.get("canonical_summary")
        != {
            "status": "accepted",
            "count": 1,
            "row_count": 62,
            "classification_counts": EXPECTED_COUNTS,
        }
        or semantic.get("rejected_review_evidence")
        != {label: "rejected" for label in REVIEW_REJECTION_CASES}
        or semantic.get("classification_drift") != "rejected"
        or semantic.get("protected_file_drift") != "rejected"
    ):
        raise ParserRepairCertificationError(
            "parser-repair semantic validation drifted"
        )
    existing = payload.get("existing_certified_projection")
    if (
        not isinstance(existing, dict)
        or existing.get("status") != "validated"
        or existing.get("row_count") != 62
        or existing.get("classification_counts") != EXPECTED_COUNTS
        or existing.get("artifacts") != EXPECTED_EXISTING_CERTIFICATION
        or existing.get("protected_inputs")
        != {
            "status": "matched",
            "file_count": EXPECTED_PROTECTED_FILE_COUNT,
            "inventory_sha256": EXPECTED_PROTECTED_INVENTORY_SHA256,
        }
    ):
        raise ParserRepairCertificationError(
            "existing certified projection binding drifted"
        )
    reviewer = payload.get("independent_reviewer")
    inventory = (
        reviewer.get("evidence_inventory")
        if isinstance(reviewer, dict)
        else None
    )
    files = inventory.get("files") if isinstance(inventory, dict) else None
    if (
        not isinstance(reviewer, dict)
        or reviewer.get("required") is not True
        or reviewer.get("status") != "accepted"
        or reviewer.get("verdict") != "ACCEPT"
        or reviewer.get("scope") != VERSION
        or reviewer.get("task_id") != REVIEWER_TASK_ID
        or reviewer.get("completed_at") != REVIEWER_COMPLETED_AT
        or not isinstance(files, list)
        or len(files) != EXPECTED_REVIEWER_FILE_COUNT
        or _inventory_digest(files)
        != EXPECTED_REVIEWER_INVENTORY_SHA256
        or inventory.get("primary_artifacts")
        != EXPECTED_REVIEWER_PRIMARY
    ):
        raise ParserRepairCertificationError(
            "fresh independent Reviewer ACCEPT binding drifted"
        )
    if payload.get("preservation") != {
        "status": "matched",
        "protected_file_count": EXPECTED_PROTECTED_FILE_COUNT,
        "protected_inventory_sha256": (
            EXPECTED_PROTECTED_INVENTORY_SHA256
        ),
        "existing_certification_artifacts": copy.deepcopy(
            EXPECTED_EXISTING_CERTIFICATION
        ),
    }:
        raise ParserRepairCertificationError(
            "parser-repair preservation binding drifted"
        )


def build_certification() -> dict[str, Any]:
    implementation = _validate_expected_artifact(
        REPAIR_IMPLEMENTATION,
        EXPECTED_REPAIR_IMPLEMENTATION,
        "repaired parser implementation",
    )
    regression_tests = _validate_expected_artifact(
        REGRESSION_TESTS,
        EXPECTED_REGRESSION_TESTS,
        "parser regression tests",
    )
    existing, projection, protected = _validate_existing_certification()
    semantic = _semantic_review_validation()
    _expect_classification_drift_rejected(projection)
    _expect_protected_drift_rejected(projection)
    semantic.update(
        {
            "classification_drift": "rejected",
            "protected_file_drift": "rejected",
        }
    )
    reviewer = _validate_reviewer_bundle(protected)
    payload = {
        "schema_version": 1,
        "kind": KIND,
        "certification_version": VERSION,
        "campaign_version": "operational-v2",
        "status": "certified",
        "row_count": 62,
        "classification_counts": copy.deepcopy(EXPECTED_COUNTS),
        "parser_repair": {
            "status": "validated",
            "parser": (
                "operational_v2_certification._parse_accept_review"
            ),
            "implementation": implementation,
            "regression_tests": regression_tests,
        },
        "semantic_validation": semantic,
        "existing_certified_projection": existing,
        "independent_reviewer": reviewer,
        "preservation": {
            "status": "matched",
            "protected_file_count": len(protected),
            "protected_inventory_sha256": _inventory_digest(protected),
            "existing_certification_artifacts": copy.deepcopy(
                existing["artifacts"]
            ),
        },
        "stage_transition": "disabled",
    }
    _validate_certification_payload(payload)
    return payload


def _report(payload: dict[str, Any]) -> str:
    exact = payload["classification_counts"]["exact_output_determinism"]
    full = payload["classification_counts"][
        "completeness_modulo_reviewed_equivalence"
    ]
    rejections = payload["semantic_validation"][
        "rejected_review_evidence"
    ]
    lines = [
        "# Operational-v2 parser-repair certification v1",
        "",
        "**Status:** `certified`",
        "",
        (
            "The additive validator accepts exactly one canonical "
            "count-bearing summary and rejects missing, duplicate, "
            "conflicting, wrong-scope, wrong-count, stale, and non-ACCEPT "
            "review evidence."
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
        (
            "Rejected review evidence: "
            + ", ".join(f"`{name}`" for name in rejections)
            + "."
        ),
        "",
        (
            "Classification drift and protected-file drift are rejected. "
            "The unchanged certified projection and all 707 protected paths "
            "match their frozen identities."
        ),
        "",
        (
            "**Independent Reviewer:** `ACCEPT` from "
            f"`{payload['independent_reviewer']['source_root']}` completed "
            f"at `{payload['independent_reviewer']['completed_at']}`."
        ),
        "",
        "Manager-owned stage transition remains disabled.",
        "",
    ]
    return "\n".join(lines)


def _manifest(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": (
            "operational-v2-parser-repair-certification-manifest"
        ),
        "certification_version": VERSION,
        "campaign_version": "operational-v2",
        "status": "certified",
        "row_count": 62,
        "classification_counts": copy.deepcopy(EXPECTED_COUNTS),
        "semantic_validation": copy.deepcopy(
            payload["semantic_validation"]
        ),
        "independent_reviewer": {
            "status": "accepted",
            "verdict": "ACCEPT",
            "task_id": REVIEWER_TASK_ID,
            "completed_at": REVIEWER_COMPLETED_AT,
            "evidence_inventory_sha256": (
                EXPECTED_REVIEWER_INVENTORY_SHA256
            ),
        },
        "preservation": copy.deepcopy(payload["preservation"]),
        "artifacts": {
            "certified_parser_repair_json": _artifact(CERTIFIED_REPAIR),
            "certified_parser_repair_markdown": _artifact(
                CERTIFIED_REPORT
            ),
        },
        "stage_transition": "disabled",
    }


def write_artifacts() -> dict[str, Any]:
    before = build_certification()
    protected_before = copy.deepcopy(before["preservation"])
    CERTIFICATION_ROOT.mkdir(parents=True, exist_ok=True)
    common.write_json(CERTIFIED_REPAIR, before)
    CERTIFIED_REPORT.write_text(_report(before), encoding="utf-8")
    manifest = _manifest(before)
    common.write_json(CERTIFICATION_MANIFEST, manifest)
    after = build_certification()
    if after["preservation"] != protected_before:
        raise ParserRepairCertificationError(
            "parser-repair writer mutated a protected input"
        )
    validate_written_artifacts()
    return manifest


def validate_written_artifacts() -> dict[str, Any]:
    expected = build_certification()
    actual = _load_json(
        CERTIFIED_REPAIR, "certified parser-repair projection"
    )
    _validate_certification_payload(actual)
    if actual != expected:
        raise ParserRepairCertificationError(
            "certified parser-repair projection is stale"
        )
    if _read_text(
        CERTIFIED_REPORT, "certified parser-repair report"
    ) != _report(expected):
        raise ParserRepairCertificationError(
            "certified parser-repair report is stale"
        )
    expected_manifest = _manifest(expected)
    actual_manifest = _load_json(
        CERTIFICATION_MANIFEST, "parser-repair certification manifest"
    )
    if actual_manifest != expected_manifest:
        raise ParserRepairCertificationError(
            "parser-repair certification manifest is stale"
        )
    for label, record in actual_manifest["artifacts"].items():
        _validate_expected_artifact(
            ROOT / record["path"], record, label
        )
    return actual_manifest


def main() -> None:
    manifest = write_artifacts()
    exact = manifest["classification_counts"]["exact_output_determinism"]
    full = manifest["classification_counts"][
        "completeness_modulo_reviewed_equivalence"
    ]
    print("operational_v2_parser_repair_certification_v1=PASS")
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
    print("canonical_summary=accepted:1")
    print(
        "review_rejections="
        + ",".join(REVIEW_REJECTION_CASES)
    )
    print("classification_drift=rejected")
    print("protected_file_drift=rejected")
    print("protected_paths=707")
    print("independent_reviewer=ACCEPT")
    print("stage_transition=disabled")


if __name__ == "__main__":
    main()
