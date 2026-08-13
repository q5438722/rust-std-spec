#!/usr/bin/env python3
"""Post-proof aggregate checker for the live 180-row Slice/Vec campaign."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path("/home/chentianyu/nanvix-rust-std-spec-survey/nanvix-rust-std-slice-vec-implproof-2026-08-12")
TARGETS_JSON = ROOT / "proof_inventory" / "targets_180.json"
TARGETS_LEGACY_JSON = ROOT / "proof_inventory" / "targets_144.json"
SPANS_JSON = ROOT / "proof_inventory" / "source_body_spans.json"
ORDER_JSON = ROOT / "proof_inventory" / "proof_order.json"
COUNTS_JSON = ROOT / "proof_inventory" / "target_counts.json"
AGGREGATE_JSON = ROOT / "proof_inventory" / "aggregate_coverage.json"
ACTIVE_CERTIFICATION_JSON = ROOT / "proof_inventory" / "active_aggregate_certification.json"
ACTIVE_CERTIFICATION_ID = "20260813T1315Z"
ACTIVE_CERTIFICATION_RELPATH = (
    "proof_inventory/final_aggregate_certification_20260813T1315Z.json"
)
HISTORICAL_CERTIFICATION_RELPATHS = [
    "proof_inventory/final_aggregate_certification_20260813T1137Z.json",
    "proof_inventory/final_aggregate_certification_20260813T1214Z.json",
]

EXPECTED_MODULE_COUNTS = {"slice": 132, "vec": 48}
EXPECTED_CATALOG_STATUS_COUNTS = {
    "existing-vstd": 36,
    "generated-new-real-relation-spec": 144,
}
EXPECTED_CERTIFICATION_SUMMARY = {
    "checker_counts": {
        "unknown": 94,
        "unsat": 50,
    },
    "classification_missing_artifact_count": 0,
    "generated_incompleteness_rows": 144,
    "implproof_abcd_status_counts": {
        "B": 180,
    },
    "implproof_c_target_count": 0,
    "implproof_exact_vstd": 36,
    "implproof_generated_new_real_relation_spec": 144,
    "implproof_pending": 0,
    "semantic_spec_mismatch_targets": [],
    "unsupported_mut_ref_return_targets": [],
}
REQUIRED_B_TARGETS = {
    "core::slice::ChunksExact::remainder",
    "core::slice::ChunksExactMut::into_remainder",
    "core::slice::Iter::as_slice",
    "core::slice::IterMut::as_slice",
    "core::slice::RChunksExact::remainder",
    "core::slice::RChunksExactMut::into_remainder",
}
ALLOWED_ABCD = {"", "A", "B", "C", "D"}
PENDING_DEP_STATUS = "pending_actual_verus_implementation_proof"
STALE_NON_PENDING_MARKERS = (
    "Rust body remains pending",
    "pending_verus_syntax_adaptation",
    "pending exact-vstd implementation proof",
    "pending_source_body_extraction",
    "pending_dependency_closure",
    "pending_bottom_up_ordering",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def proof_status_base(status: str) -> str:
    return str(status).split(":", 1)[0]


def abcd_status(row: dict[str, Any]) -> str:
    status = str(row.get("abcd_status", "")).strip()
    return status if status else "pending"


def next_pending_generated_target(targets: list[dict[str, Any]]) -> tuple[str, int | None]:
    pending = [row for row in targets if abcd_status(row) == "pending"]
    if not pending:
        return "", None
    row = min(pending, key=parse_order_index)
    return row["target"], parse_order_index(row)


def parse_order_index(row: dict[str, Any]) -> int:
    proof_order = str(row.get("proof_order", ""))
    if not proof_order.startswith("index="):
        raise RuntimeError(f"{row['target']}: missing proof_order index")
    return int(proof_order.split(";", 1)[0].split("=", 1)[1])


def assert_no_stale_pending_marker(target: str, label: str, value: Any) -> None:
    text = json.dumps(value, sort_keys=True) if not isinstance(value, str) else value
    for marker in STALE_NON_PENDING_MARKERS:
        if marker in text:
            raise RuntimeError(f"{target}: stale pending marker in {label}: {marker!r}")


def assert_counts(name: str, actual: Counter[str], expected: dict[str, int]) -> None:
    actual_dict = dict(sorted(actual.items()))
    if actual_dict != expected:
        raise RuntimeError(f"{name} mismatch: expected {expected}, got {actual_dict}")


def assert_equal(name: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        raise RuntimeError(f"{name} mismatch: expected {expected!r}, got {actual!r}")


def check_target_sets(targets: list[dict[str, Any]], spans: list[dict[str, Any]], orders: list[dict[str, Any]]) -> None:
    if len(targets) != 180 or len(spans) != 180 or len(orders) != 180:
        raise RuntimeError(f"expected 180 targets/spans/orders, got {len(targets)}/{len(spans)}/{len(orders)}")
    target_names = {row["target"] for row in targets}
    if len(target_names) != 180:
        raise RuntimeError("target names are not unique")
    if {row["target"] for row in spans} != target_names:
        raise RuntimeError("source_body_spans target set mismatch")
    if {row["target"] for row in orders} != target_names:
        raise RuntimeError("proof_order target set mismatch")
    assert_counts("module counts", Counter(row["module"] for row in targets), EXPECTED_MODULE_COUNTS)
    assert_counts(
        "catalog status counts",
        Counter(row["catalog_status"] for row in targets),
        EXPECTED_CATALOG_STATUS_COUNTS,
    )
    if "alloc::vec::Vec::splice" in target_names:
        raise RuntimeError("Vec::splice must remain outside the 180 proof count")
    order_indices = [int(row["proof_order_index"]) for row in orders]
    if sorted(order_indices) != list(range(1, 181)):
        raise RuntimeError("proof order indices are not a 1..180 permutation")
    target_order_indices = [parse_order_index(row) for row in targets]
    if sorted(target_order_indices) != list(range(1, 181)):
        raise RuntimeError("target proof_order fields are not a 1..180 permutation")
    order_by_target = {row["target"]: int(row["proof_order_index"]) for row in orders}
    for row in targets:
        if order_by_target[row["target"]] != parse_order_index(row):
            raise RuntimeError(f"{row['target']}: target proof_order disagrees with proof_order.json")
    if order_by_target.get("core::slice::array_windows") != 7:
        raise RuntimeError("core::slice::array_windows must remain proof-order index 7")


def check_source_hashes(spans: list[dict[str, Any]]) -> None:
    for span in spans:
        frozen_path = ROOT / span["frozen_relpath"]
        lines = frozen_path.read_text().splitlines(keepends=True)
        item_text = "".join(lines[int(span["signature_start_line"]) - 1 : int(span["body_end_line"])])
        if sha256_text(item_text) != span["source_item_sha256"]:
            raise RuntimeError(f"{span['target']}: source item hash mismatch")
        for rel_field in [
            "source_manifest_relpath",
            "transformation_manifest_relpath",
            "dependency_manifest_relpath",
            "harness_relpath",
        ]:
            if not (ROOT / span[rel_field]).is_file():
                raise FileNotFoundError(f"{span['target']}: missing {rel_field} {span[rel_field]}")


def check_manifests(targets: list[dict[str, Any]], spans: list[dict[str, Any]]) -> None:
    target_by_name = {row["target"]: row for row in targets}
    order_by_target = {row["target"]: row for row in load_json(ORDER_JSON)}
    for span in spans:
        target = span["target"]
        target_row = target_by_name[target]
        abcd = str(target_row.get("abcd_status", "")).strip()
        if abcd not in ALLOWED_ABCD:
            raise RuntimeError(f"{target}: invalid A/B/C/D status {abcd!r}")
        trans = load_json(ROOT / span["transformation_manifest_relpath"])
        if trans.get("semantic_replacement") is not False:
            raise RuntimeError(f"{target}: transformation manifest is not semantic-replacement-free")
        dep = load_json(ROOT / span["dependency_manifest_relpath"])
        dep_status = proof_status_base(dep.get("proof_status", ""))
        target_status = proof_status_base(target_row.get("proof_status", ""))
        if abcd == "":
            if dep_status != PENDING_DEP_STATUS or target_status != "pending_implementation_proof":
                raise RuntimeError(f"{target}: pending row has non-pending proof status")
            continue
        assert_no_stale_pending_marker(target, "inventory source_backed_helpers", target_row.get("source_backed_helpers", ""))
        assert_no_stale_pending_marker(target, "inventory proof_order", target_row.get("proof_order", ""))
        assert_no_stale_pending_marker(target, "proof_order row", order_by_target[target])
        assert_no_stale_pending_marker(target, "transformation manifest", trans)
        if dep_status != target_status:
            raise RuntimeError(f"{target}: dependency manifest proof status disagrees with inventory")
        if abcd in {"A", "B"}:
            evidence = dep.get("proof_evidence", {})
            stdout_rel = evidence.get("stdout_relpath", "")
            if not stdout_rel:
                raise RuntimeError(f"{target}: verified status lacks stdout evidence")
            stdout = (ROOT / stdout_rel).read_text()
            if "verification results::" not in stdout or "0 errors" not in stdout:
                raise RuntimeError(f"{target}: stdout evidence is not a successful Verus result")
            harness_text = (ROOT / span["harness_relpath"]).read_text()
            if "--no-verify" in harness_text or "assume_specification" in harness_text:
                raise RuntimeError(f"{target}: verified harness contains proof-by-assumption marker")


def check_aggregate_counts(targets: list[dict[str, Any]]) -> None:
    counts = load_json(COUNTS_JSON)
    coverage = load_json(AGGREGATE_JSON)
    status_counts = Counter(proof_status_base(row["proof_status"]) for row in targets)
    abcd_counts = Counter(abcd_status(row) for row in targets)
    expected_abcd = dict(sorted(abcd_counts.items()))
    next_target, next_index = next_pending_generated_target(targets)
    for doc_name, doc in [("target_counts", counts), ("aggregate_coverage", coverage)]:
        if doc.get("target_count") != 180:
            raise RuntimeError(f"{doc_name}: target_count is not 180")
        if doc.get("target_counts_by_module") != EXPECTED_MODULE_COUNTS:
            raise RuntimeError(f"{doc_name}: module counts mismatch")
        if doc.get("target_counts_by_catalog_status") != EXPECTED_CATALOG_STATUS_COUNTS:
            raise RuntimeError(f"{doc_name}: catalog status counts mismatch")
        if doc.get("abcd_status_counts") != expected_abcd:
            raise RuntimeError(f"{doc_name}: A/B/C/D counts mismatch")
        if doc.get("proof_status_counts") != dict(sorted(status_counts.items())):
            raise RuntimeError(f"{doc_name}: proof status counts mismatch")
        if doc.get("next_generated_target") != next_target:
            raise RuntimeError(f"{doc_name}: next generated target mismatch")
        if doc.get("next_generated_proof_order_index") != next_index:
            raise RuntimeError(f"{doc_name}: next generated proof-order index mismatch")


def check_legacy_alias() -> None:
    live = load_json(TARGETS_JSON)
    legacy = load_json(TARGETS_LEGACY_JSON)
    if live != legacy:
        raise RuntimeError("targets_144 legacy file and targets_180 live alias disagree")


def check_active_certification_pointer(targets: list[dict[str, Any]]) -> None:
    pointer = load_json(ACTIVE_CERTIFICATION_JSON)
    assert_equal("active pointer status", pointer.get("status"), "active")
    assert_equal(
        "active pointer certification id",
        pointer.get("active_certification_id"),
        ACTIVE_CERTIFICATION_ID,
    )
    assert_equal(
        "active pointer certification relpath",
        pointer.get("active_certification_relpath"),
        ACTIVE_CERTIFICATION_RELPATH,
    )
    assert_equal(
        "active pointer historical certifications",
        pointer.get("historical_certification_relpaths"),
        HISTORICAL_CERTIFICATION_RELPATHS,
    )

    for relpath in [ACTIVE_CERTIFICATION_RELPATH, *HISTORICAL_CERTIFICATION_RELPATHS]:
        if not (ROOT / relpath).is_file():
            raise FileNotFoundError(f"missing certification artifact {relpath}")

    certification = load_json(ROOT / ACTIVE_CERTIFICATION_RELPATH)
    assert_equal("active certification status", certification.get("status"), "pass")
    assert_equal("active certification root", certification.get("root"), str(ROOT))
    if certification.get("supersedes", {}).get("artifact") not in HISTORICAL_CERTIFICATION_RELPATHS:
        raise RuntimeError("active certification does not supersede preserved historical evidence")

    summary = certification.get("certification_summary", {})
    pointer_expected = pointer.get("expected_acceptance", {})
    assert_equal("active pointer expected_acceptance", pointer_expected, EXPECTED_CERTIFICATION_SUMMARY)
    for key, expected_value in EXPECTED_CERTIFICATION_SUMMARY.items():
        assert_equal(f"active certification summary {key}", summary.get(key), expected_value)

    abcd_counts = dict(sorted(Counter(abcd_status(row) for row in targets).items()))
    assert_equal("active certification summary current A/B/C/D count", summary.get("implproof_abcd_status_counts"), abcd_counts)
    assert_equal("active certification summary current pending count", summary.get("implproof_pending"), abcd_counts.get("pending", 0))

    measured = certification.get("measured", {})
    for source_name, source_doc in [
        ("target_counts", load_json(COUNTS_JSON)),
        ("aggregate_coverage", load_json(AGGREGATE_JSON)),
    ]:
        measured_doc = measured.get(source_name, {})
        for key in [
            "target_count",
            "target_counts_by_module",
            "target_counts_by_catalog_status",
            "abcd_status_counts",
            "next_generated_target",
            "next_generated_proof_order_index",
        ]:
            assert_equal(
                f"active certification measured {source_name}.{key}",
                measured_doc.get(key),
                source_doc.get(key),
            )

    native_checks = certification.get("native_checks", [])
    if not native_checks:
        raise RuntimeError("active certification has no native check records")
    for check in native_checks:
        assert_equal("active certification native check status", check.get("status"), "pass")


def main() -> None:
    check_legacy_alias()
    targets = load_json(TARGETS_JSON)
    spans = load_json(SPANS_JSON)
    orders = load_json(ORDER_JSON)
    check_target_sets(targets, spans, orders)
    b_targets = {row["target"] for row in targets if row.get("abcd_status") == "B"}
    missing_required_b = sorted(REQUIRED_B_TARGETS - b_targets)
    if missing_required_b:
        raise RuntimeError(f"missing required reviewed B targets: {missing_required_b}")
    check_source_hashes(spans)
    check_manifests(targets, spans)
    check_aggregate_counts(targets)
    check_active_certification_pointer(targets)
    abcd_counts = Counter(abcd_status(row) for row in targets)
    next_target, next_index = next_pending_generated_target(targets)
    print(
        "aggregate ok: "
        f"180 targets, B={abcd_counts.get('B', 0)}, "
        f"pending={abcd_counts.get('pending', 0)}, exact-vstd=36, "
        f"next={next_target}#{next_index}, "
        f"active_certification={ACTIVE_CERTIFICATION_ID}"
    )


if __name__ == "__main__":
    main()
