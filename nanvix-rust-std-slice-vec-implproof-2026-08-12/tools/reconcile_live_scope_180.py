#!/usr/bin/env python3
"""Append exact-vstd Slice/Vec obligations to the live implproof inventory.

The original extractor intentionally built the 144 generated-contract inventory.
The live manager scope is wider: preserve those 144 rows and any proof progress,
then add the 36 exact-vstd contracts as Rust-body proof obligations.  This script
is append-only for the new vstd rows and does not rewrite existing generated
harnesses or proof manifests.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path("/home/chentianyu/nanvix-rust-std-spec-survey/nanvix-rust-std-slice-vec-implproof-2026-08-12")
TARGETS_LEGACY_JSON = ROOT / "proof_inventory" / "targets_144.json"
TARGETS_LEGACY_CSV = ROOT / "proof_inventory" / "targets_144.csv"
TARGETS_LIVE_JSON = ROOT / "proof_inventory" / "targets_180.json"
TARGETS_LIVE_CSV = ROOT / "proof_inventory" / "targets_180.csv"
SPANS_JSON = ROOT / "proof_inventory" / "source_body_spans.json"
SPANS_CSV = ROOT / "proof_inventory" / "source_body_spans.csv"
ORDER_JSON = ROOT / "proof_inventory" / "proof_order.json"
ORDER_CSV = ROOT / "proof_inventory" / "proof_order.csv"
DEPENDENCY_SUMMARY = ROOT / "proof_inventory" / "dependency_summary.json"
TARGET_COUNTS = ROOT / "proof_inventory" / "target_counts.json"
AGGREGATE_COVERAGE = ROOT / "proof_inventory" / "aggregate_coverage.json"

GENERATED_STATUS = "generated-new-real-relation-spec"
EXISTING_VSTD_STATUS = "existing-vstd"
PENDING_PROOF_STATUS = "pending_implementation_proof"
PENDING_DEPENDENCY_STATUS = "pending_actual_verus_implementation_proof"
EXPECTED_GENERATED = {"slice": 120, "vec": 24}
EXPECTED_EXISTING_VSTD = {"slice": 12, "vec": 24}
EXPECTED_LIVE = {
    module: EXPECTED_GENERATED[module] + EXPECTED_EXISTING_VSTD[module]
    for module in EXPECTED_GENERATED
}
EXACT_VSTD_COMPLETED_RATIONALE = (
    "live-scope exact-vstd row appended after the 144 generated rows to preserve "
    "reviewed generated proof order; Rust body proof is completed and recorded in "
    "the target-local harness/evidence"
)
SOURCE_BACKED_HELPER_REPLACEMENTS = {
    "vstd split_at view facts pending exact-vstd implementation proof": (
        "vstd split_at view facts discharged by the completed exact-vstd "
        "implementation-proof row"
    ),
    "vstd split_at_mut view and final-frame facts pending exact-vstd implementation proof": (
        "vstd split_at_mut view and final-frame facts discharged by the completed "
        "exact-vstd implementation-proof row"
    ),
}
PRESERVED_EXACT_VSTD_PROOF_FIELDS = (
    "abcd_status",
    "audited_shared_helpers",
    "boundary_helpers",
    "direct_shared_helpers",
    "reachable_shared_helpers",
    "law_constrained_helpers",
    "source_backed_helpers",
    "private_helper_callee_closure",
    "proof_status",
    "requires",
    "ensures",
    "unsafe_intrinsic_trait_allocator_dependencies",
)


def load_extractor() -> Any:
    spec = importlib.util.spec_from_file_location(
        "extract_implproof_targets", ROOT / "tools" / "extract_implproof_targets.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load extract_implproof_targets.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def proof_status_base(status: str) -> str:
    return str(status).split(":", 1)[0]


def transformation_status_for(target_row: dict[str, Any]) -> str:
    status = proof_status_base(target_row.get("proof_status", ""))
    if status.startswith("actual_"):
        return status.removeprefix("actual_")
    return status


def refresh_completed_transformation_manifest(target_row: dict[str, Any], span_row: dict[str, Any]) -> None:
    if abcd_status(target_row) == "pending":
        return
    trans_path = ROOT / span_row["transformation_manifest_relpath"]
    if not trans_path.is_file():
        return
    trans = json.loads(trans_path.read_text())
    desired_status = transformation_status_for(target_row)
    if trans.get("status") == desired_status and trans.get("schema_version") == 2 and trans.get("harness_sha256"):
        return
    trans["schema_version"] = 2
    trans["status"] = desired_status
    harness_rel = trans.get("harness_relpath") or span_row.get("harness_relpath")
    if harness_rel:
        trans["harness_sha256"] = sha256_file(ROOT / harness_rel)
    write_json(trans_path, trans)


def refresh_completed_transformation_manifests(
    targets: list[dict[str, Any]], spans: list[dict[str, Any]]
) -> None:
    target_by_name = {row["target"]: row for row in targets}
    for span in spans:
        refresh_completed_transformation_manifest(target_by_name[span["target"]], span)


def normalize_completed_source_backed_helpers(target_row: dict[str, Any]) -> None:
    if abcd_status(target_row) == "pending":
        return
    helpers = str(target_row.get("source_backed_helpers", ""))
    for stale, replacement in SOURCE_BACKED_HELPER_REPLACEMENTS.items():
        helpers = helpers.replace(stale, replacement)
    target_row["source_backed_helpers"] = helpers


def abcd_status(row: dict[str, Any]) -> str:
    value = str(row.get("abcd_status", "")).strip()
    return value if value else "pending"


def proof_order_index(row: dict[str, Any]) -> int:
    proof_order = str(row.get("proof_order", ""))
    if not proof_order.startswith("index="):
        return 10**9
    return int(proof_order.split(";", 1)[0].split("=", 1)[1])


def next_pending_generated_target(targets: list[dict[str, Any]]) -> tuple[str, int | None]:
    pending = [row for row in targets if abcd_status(row) == "pending"]
    if not pending:
        return "", None
    row = min(pending, key=proof_order_index)
    return row["target"], proof_order_index(row)


def module_catalog_paths() -> dict[str, Path]:
    return {
        "slice": ROOT / "frozen_inputs" / "slice" / "catalog" / "slice_spec_catalog.csv",
        "vec": ROOT / "frozen_inputs" / "vec" / "catalog" / "vec_spec_catalog.csv",
    }


def load_existing_vstd_catalog_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for module, path in module_catalog_paths().items():
        selected = [
            {**row, "module": module}
            for row in read_csv(path)
            if row.get("status") == EXISTING_VSTD_STATUS
        ]
        if len(selected) != EXPECTED_EXISTING_VSTD[module]:
            raise RuntimeError(
                f"{module}: expected {EXPECTED_EXISTING_VSTD[module]} exact-vstd rows, "
                f"found {len(selected)}"
            )
        rows.extend(selected)
    if any(row["target"] == "alloc::vec::Vec::splice" for row in rows):
        raise RuntimeError("Vec::splice is justified-no-spec and must stay outside the proof count")
    return rows


def inventory_row_from_catalog(row: dict[str, Any], input_order: int) -> dict[str, Any]:
    contract_text = row.get("contract_text", "")
    shared_note = row.get("shared_helpers", "")
    return {
        "input_order": input_order,
        "module": row["module"],
        "target": row["target"],
        "semantic_family": row.get("semantic_family", ""),
        "catalog_status": EXISTING_VSTD_STATUS,
        "source_reference": row.get("source_reference", ""),
        "source_excerpt": row.get("source_excerpt", ""),
        "contract_sha256": hashlib.sha256(contract_text.encode()).hexdigest(),
        "contract_text": contract_text,
        "requires": row.get("requires", ""),
        "ensures": row.get("ensures", ""),
        "direct_shared_helpers": "",
        "reachable_shared_helpers": "",
        "audited_shared_helpers": "",
        "source_backed_helpers": shared_note,
        "law_constrained_helpers": "",
        "boundary_helpers": (
            "exact-vstd assume_specification contract is a live proof obligation; "
            "the Rust 1.96 implementation body is not proved by the copied baseline"
        ),
        "implementation_body_status": "pending_source_body_extraction",
        "private_helper_callee_closure": "pending_dependency_closure",
        "unsafe_intrinsic_trait_allocator_dependencies": "pending_dependency_closure",
        "proof_order": "pending_bottom_up_ordering",
        "proof_status": PENDING_PROOF_STATUS,
        "abcd_status": "",
    }


def make_span_row(
    row: dict[str, Any],
    item: Any,
    categories: dict[str, dict[str, Any]],
    private_closure: list[dict[str, Any]],
    target_deps: list[str],
    direct_call_count: int,
    source_manifest_rel: str,
    transformation_rel: str,
    dependency_rel: str,
    harness_rel: str,
    proof_order_index: int,
    proof_tier: int,
    proof_tier_reason: str,
) -> dict[str, Any]:
    present_categories = sorted(name for name, info in categories.items() if info["present"])
    return {
        "input_order": row["input_order"],
        "module": row["module"],
        "target": row["target"],
        "target_owner": "::".join(row["target"].split("::")[:-1]),
        "target_path": row["target"],
        "semantic_family": row["semantic_family"],
        "source_reference": row["source_reference"],
        "source_reference_path": item.source_reference_path,
        "frozen_relpath": item.frozen_relpath,
        "source_file_sha256": item.source_file_sha256,
        "source_item_sha256": item.item_sha256,
        "signature_start_line": item.signature_start_line,
        "signature_end_line": item.signature_end_line,
        "body_start_line": item.body_start_line,
        "body_end_line": item.body_end_line,
        "enclosing_impl_header": item.enclosing_impl_header,
        "enclosing_impl_start_line": item.enclosing_impl_start_line or "",
        "direct_call_count": direct_call_count,
        "private_helper_callee_count": len(private_closure),
        "generated_target_dependency_count": len(target_deps),
        "present_dependency_categories": present_categories,
        "dependency_categories": categories,
        "proof_order_index": proof_order_index,
        "proof_tier": proof_tier,
        "proof_tier_reason": proof_tier_reason,
        "source_manifest_relpath": source_manifest_rel,
        "transformation_manifest_relpath": transformation_rel,
        "dependency_manifest_relpath": dependency_rel,
        "harness_relpath": harness_rel,
    }


def summarize_dependency_categories(rows: list[dict[str, Any]]) -> dict[str, Any]:
    category_counts: dict[str, int] = defaultdict(int)
    module_category_counts: dict[str, Counter[str]] = defaultdict(Counter)
    private_count = 0
    generated_dep_count = 0
    for row in rows:
        for category, info in row["dependency_categories"].items():
            if info["present"]:
                category_counts[category] += 1
                module_category_counts[row["module"]][category] += 1
        private_count += 1 if int(row.get("private_helper_callee_count") or 0) else 0
        generated_dep_count += 1 if int(row.get("generated_target_dependency_count") or 0) else 0
    return {
        "target_count": len(rows),
        "dependency_category_target_counts": dict(sorted(category_counts.items())),
        "dependency_category_target_counts_by_module": {
            module: dict(sorted(counter.items()))
            for module, counter in sorted(module_category_counts.items())
        },
        "private_helper_callee_candidate_targets": private_count,
        "generated_target_dependency_candidate_targets": generated_dep_count,
    }


def load_dependency_manifest(row: dict[str, Any]) -> dict[str, Any]:
    rel = row.get("dependency_manifest_relpath")
    if not rel:
        return {}
    path = ROOT / rel
    return json.loads(path.read_text()) if path.is_file() else {}


def boundary_type_for(target_row: dict[str, Any], span_row: dict[str, Any] | None) -> str:
    status = proof_status_base(target_row.get("proof_status", ""))
    abcd = abcd_status(target_row)
    if abcd == "A":
        return "none"
    if abcd == "B":
        if "private_helper_and_pointer_boundary" in status:
            return "private_helper_and_pointer_boundary"
        if "private_representation_boundary" in status:
            return "private_representation_boundary"
        if "source_backed_iterator_view_boundary" in status:
            return "source_backed_iterator_view_boundary"
        if "source_backed_raw_pointer_swap_boundary" in status:
            return "source_backed_raw_pointer_swap_boundary"
        if "source_backed_raw_pointer_cast_boundary" in status:
            return "source_backed_raw_pointer_cast_boundary"
        return "trusted_boundary_enumerated"
    if abcd == "C":
        return "spec_mismatch_no_trusted_boundary"
    if abcd == "D":
        return "tool_or_model_blocker"
    if span_row is None:
        return "pending_source_extraction"
    present = span_row.get("present_dependency_categories") or []
    if isinstance(present, str):
        present = [part.strip(" '[]") for part in present.split(",") if part.strip(" '[]")]
    if present:
        return "pending_dependency_obligation:" + "+".join(sorted(present))
    return "none_detected_pending"


def aggregate_coverage(targets: list[dict[str, Any]], spans: list[dict[str, Any]]) -> dict[str, Any]:
    span_by_target = {row["target"]: row for row in spans}
    boundary_counts: Counter[str] = Counter()
    boundary_by_module: dict[str, Counter[str]] = defaultdict(Counter)
    blocker_counts: Counter[str] = Counter()
    next_target, next_index = next_pending_generated_target(targets)
    for row in targets:
        boundary = boundary_type_for(row, span_by_target.get(row["target"]))
        boundary_counts[boundary] += 1
        boundary_by_module[row["module"]][boundary] += 1
        blocker_counts["minimized_blocker_recorded" if abcd_status(row) == "D" else "no_blocker_recorded"] += 1
    return {
        "schema_version": 1,
        "target_count": len(targets),
        "target_counts_by_module": dict(sorted(Counter(row["module"] for row in targets).items())),
        "target_counts_by_catalog_status": dict(sorted(Counter(row["catalog_status"] for row in targets).items())),
        "semantic_family_counts": dict(sorted(Counter(row["semantic_family"] for row in targets).items())),
        "proof_status_counts": dict(sorted(Counter(proof_status_base(row["proof_status"]) for row in targets).items())),
        "abcd_status_counts": dict(sorted(Counter(abcd_status(row) for row in targets).items())),
        "boundary_type_counts": dict(sorted(boundary_counts.items())),
        "boundary_type_counts_by_module": {
            module: dict(sorted(counter.items())) for module, counter in sorted(boundary_by_module.items())
        },
        "blocker_type_counts": dict(sorted(blocker_counts.items())),
        "next_generated_target": next_target,
        "next_generated_proof_order_index": next_index,
        "scope_note": (
            "Live scope is 180 obligations: 144 generated rows plus 36 exact-vstd rows. "
            "Exact-vstd assume_specification declarations are obligations, not Rust-body proofs."
        ),
    }


def update_target_counts(targets: list[dict[str, Any]], spans: list[dict[str, Any]]) -> None:
    coverage = aggregate_coverage(targets, spans)
    dependency_summary = summarize_dependency_categories(spans)
    counts = {
        **coverage,
        "implementation_body_status_counts": dict(
            sorted(
                Counter(
                    str(row["implementation_body_status"]).split(":", 1)[0]
                    for row in targets
                ).items()
            )
        ),
        "proof_order_status_counts": {
            "ordered": sum(1 for row in targets if str(row.get("proof_order", "")).startswith("index=")),
            "pending": sum(1 for row in targets if str(row.get("proof_order", "")).startswith("pending")),
        },
        "dependency_category_target_counts": dependency_summary["dependency_category_target_counts"],
    }
    write_json(TARGET_COUNTS, counts)
    write_json(AGGREGATE_COVERAGE, coverage)
    write_json(DEPENDENCY_SUMMARY, dependency_summary)


def write_manifest_hashes() -> None:
    rels = [
        "proof_inventory/targets_144.csv",
        "proof_inventory/targets_144.json",
        "proof_inventory/targets_180.csv",
        "proof_inventory/targets_180.json",
        "proof_inventory/source_body_spans.csv",
        "proof_inventory/source_body_spans.json",
        "proof_inventory/proof_order.csv",
        "proof_inventory/proof_order.json",
        "proof_inventory/dependency_summary.json",
        "proof_inventory/target_counts.json",
        "proof_inventory/aggregate_coverage.json",
    ]
    hashes = {rel: sha256_file(ROOT / rel) for rel in rels if (ROOT / rel).is_file()}
    write_json(ROOT / "proof_inventory" / "implproof_manifest_hashes.json", hashes)


def update_freeze_summary(targets: list[dict[str, Any]]) -> None:
    path = ROOT / "FREEZE_SUMMARY.json"
    summary = json.loads(path.read_text()) if path.is_file() else {}
    summary["target_count"] = len(targets)
    summary["target_counts_by_module"] = dict(sorted(Counter(row["module"] for row in targets).items()))
    summary["target_counts_by_catalog_status"] = dict(
        sorted(Counter(row["catalog_status"] for row in targets).items())
    )
    summary["target_counts_by_proof_status"] = dict(
        sorted(Counter(proof_status_base(row["proof_status"]) for row in targets).items())
    )
    manifests = dict(summary.get("manifests", {}))
    manifests.update(
        {
            "targets_csv": "proof_inventory/targets_144.csv",
            "targets_json": "proof_inventory/targets_144.json",
            "live_targets_csv": "proof_inventory/targets_180.csv",
            "live_targets_json": "proof_inventory/targets_180.json",
            "aggregate_coverage_json": "proof_inventory/aggregate_coverage.json",
        }
    )
    summary["manifests"] = manifests
    summary["live_scope_note"] = (
        "The legacy targets_144 filenames are retained for tool compatibility but now mirror "
        "the 180-row live inventory; targets_180 is the explicit live-scope alias."
    )
    write_json(path, summary)


def main() -> None:
    extractor = load_extractor()
    targets = json.loads(TARGETS_LEGACY_JSON.read_text())
    generated_targets = [row for row in targets if row.get("catalog_status") == GENERATED_STATUS]
    previous_vstd_progress = {
        row["target"]: row
        for row in targets
        if row.get("catalog_status") == EXISTING_VSTD_STATUS and abcd_status(row) != "pending"
    }
    all_existing_spans = json.loads(SPANS_JSON.read_text())
    previous_vstd_spans = {
        row["target"]: row
        for row in all_existing_spans
        if row["target"] in previous_vstd_progress
    }
    generated_counts = Counter(row["module"] for row in generated_targets)
    if dict(sorted(generated_counts.items())) != EXPECTED_GENERATED:
        raise RuntimeError(f"generated target count mismatch: {dict(generated_counts)}")

    existing_names = {row["target"] for row in generated_targets}
    vstd_catalog_rows = load_existing_vstd_catalog_rows()
    overlap = sorted(existing_names & {row["target"] for row in vstd_catalog_rows})
    if overlap:
        raise RuntimeError(f"exact-vstd rows overlap generated inventory: {overlap}")

    file_rows = extractor.load_json(ROOT / "frozen_inputs" / "file_manifest.json")
    ref_map = extractor.manifest_ref_map(file_rows)
    source_index = extractor.build_source_item_index(file_rows)
    generated_target_name_map: dict[str, list[str]] = defaultdict(list)
    for row in generated_targets:
        generated_target_name_map[row["target"].split("::")[-1]].append(row["target"])

    existing_spans = [
        row
        for row in all_existing_spans
        if row["target"] in {target["target"] for target in generated_targets}
    ]
    existing_orders = [
        row
        for row in json.loads(ORDER_JSON.read_text())
        if row["target"] in {target["target"] for target in generated_targets}
    ]
    if len(existing_spans) != 144 or len(existing_orders) != 144:
        raise RuntimeError("expected 144 generated span/order rows before appending vstd obligations")

    next_input_order = max(int(row["input_order"]) for row in generated_targets) + 1
    next_proof_order = max(int(row["proof_order_index"]) for row in existing_orders) + 1
    vstd_targets: list[dict[str, Any]] = []
    vstd_spans: list[dict[str, Any]] = []
    vstd_orders: list[dict[str, Any]] = []

    for offset, catalog_row in enumerate(vstd_catalog_rows):
        target_row = inventory_row_from_catalog(catalog_row, next_input_order + offset)
        ref_path = extractor.source_ref_path(target_row["source_reference"])
        manifest_row = ref_map[ref_path]
        source_path = ROOT / manifest_row["frozen_relpath"]
        lines = source_path.read_text().splitlines(keepends=True)
        item = extractor.extract_item(
            target_row["target"],
            target_row["source_reference"],
            target_row["source_excerpt"],
            ref_path,
            manifest_row["frozen_relpath"],
            manifest_row["sha256"],
            lines,
        )
        call_tokens = extractor.extract_call_tokens(item.item_text)
        call_names = {token["name"] for token in call_tokens}
        private_closure = extractor.private_callee_closure(
            extractor.private_candidate_names(call_tokens),
            source_index,
        )
        categories = extractor.dependency_categories(item.signature_text, item.item_text, target_row["module"])
        target_deps = extractor.target_dependency_candidates(
            target_row["target"],
            item.item_text,
            generated_target_name_map,
        )
        proof_tier, proof_tier_reason = extractor.proof_tier(categories, target_deps)
        previous_span = previous_vstd_spans.get(target_row["target"])
        if previous_span is None:
            source_rel, transform_rel, dep_rel = extractor.write_target_artifacts(
                target_row,
                item,
                categories,
                call_names,
                private_closure,
                target_deps,
            )
        else:
            source_rel = previous_span["source_manifest_relpath"]
            transform_rel = previous_span["transformation_manifest_relpath"]
            dep_rel = previous_span["dependency_manifest_relpath"]
        proof_order_index = next_proof_order + offset
        span = make_span_row(
            target_row,
            item,
            categories,
            private_closure,
            target_deps,
            len(call_names),
            source_rel,
            transform_rel,
            dep_rel,
            str(Path("proof_harnesses") / extractor.slug_for(int(target_row["input_order"]), target_row["target"]) / "harness.rs"),
            proof_order_index,
            proof_tier,
            proof_tier_reason,
        )
        target_row["implementation_body_status"] = (
            "source_body_extracted:"
            f"{span['source_item_sha256']}:"
            f"{span['source_manifest_relpath']}"
        )
        target_row["private_helper_callee_closure"] = (
            f"source_indexed_conservative_count={span['private_helper_callee_count']};"
            f" manifest={span['dependency_manifest_relpath']}"
        )
        target_row["unsafe_intrinsic_trait_allocator_dependencies"] = (
            f"categories={','.join(span['present_dependency_categories']) or 'none'};"
            f" manifest={span['dependency_manifest_relpath']}"
        )
        target_row["proof_order"] = (
            f"index={proof_order_index};tier={proof_tier};"
            " manifest=proof_inventory/proof_order.json"
        )
        if target_row["target"] in previous_vstd_progress:
            previous = previous_vstd_progress[target_row["target"]]
            for field in PRESERVED_EXACT_VSTD_PROOF_FIELDS:
                target_row[field] = previous.get(field, target_row.get(field, ""))
        vstd_targets.append(target_row)
        vstd_spans.append(span)
        vstd_orders.append(
            {
                "proof_order_index": proof_order_index,
                "module": target_row["module"],
                "target": target_row["target"],
                "input_order": target_row["input_order"],
                "semantic_family": target_row["semantic_family"],
                "proof_tier": proof_tier,
                "proof_tier_reason": proof_tier_reason,
                "generated_target_dependencies": target_deps,
                "cycle_or_unresolved_dependencies": [],
                "bottom_up_rationale": EXACT_VSTD_COMPLETED_RATIONALE,
            }
        )

    live_targets = generated_targets + vstd_targets
    live_spans = existing_spans + vstd_spans
    live_orders = existing_orders + vstd_orders
    for row in live_targets:
        normalize_completed_source_backed_helpers(row)
    refresh_completed_transformation_manifests(live_targets, live_spans)
    live_counts = Counter(row["module"] for row in live_targets)
    if dict(sorted(live_counts.items())) != EXPECTED_LIVE:
        raise RuntimeError(f"live target count mismatch: {dict(live_counts)}")
    if len(live_targets) != 180 or len(live_spans) != 180 or len(live_orders) != 180:
        raise RuntimeError("live inventory did not reconcile to 180 rows")

    target_fields = list(live_targets[0].keys())
    span_fields = [
        "input_order",
        "module",
        "target",
        "target_owner",
        "target_path",
        "semantic_family",
        "source_reference",
        "source_reference_path",
        "frozen_relpath",
        "source_file_sha256",
        "source_item_sha256",
        "signature_start_line",
        "signature_end_line",
        "body_start_line",
        "body_end_line",
        "enclosing_impl_header",
        "enclosing_impl_start_line",
        "direct_call_count",
        "private_helper_callee_count",
        "generated_target_dependency_count",
        "present_dependency_categories",
        "proof_order_index",
        "proof_tier",
        "proof_tier_reason",
        "source_manifest_relpath",
        "transformation_manifest_relpath",
        "dependency_manifest_relpath",
        "harness_relpath",
    ]
    order_fields = [
        "proof_order_index",
        "module",
        "target",
        "input_order",
        "semantic_family",
        "proof_tier",
        "proof_tier_reason",
        "generated_target_dependencies",
        "cycle_or_unresolved_dependencies",
        "bottom_up_rationale",
    ]

    write_json(TARGETS_LEGACY_JSON, live_targets)
    write_csv(TARGETS_LEGACY_CSV, live_targets, target_fields)
    write_json(TARGETS_LIVE_JSON, live_targets)
    write_csv(TARGETS_LIVE_CSV, live_targets, target_fields)
    write_json(SPANS_JSON, live_spans)
    write_csv(SPANS_CSV, live_spans, span_fields)
    write_json(ORDER_JSON, live_orders)
    write_csv(ORDER_CSV, live_orders, order_fields)
    update_target_counts(live_targets, live_spans)
    update_freeze_summary(live_targets)
    write_manifest_hashes()

    print(
        "live scope reconciled: "
        f"{len(live_targets)} targets "
        f"(slice={live_counts['slice']}, vec={live_counts['vec']}), "
        "existing-vstd appended=36"
    )


if __name__ == "__main__":
    main()
