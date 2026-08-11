#!/usr/bin/env python3
"""Run the final integrity pass and record machine-check evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


EXPECTED_TOTAL = 132
EXPECTED_EXISTING_VSTD = 12
MODULES_CSV = Path("/home/chentianyu/nanvix-rust-std-spec-survey/results/modules.csv")
EXISTING_VSTD = {
    "core::slice::copy_from_slice",
    "core::slice::copy_within",
    "core::slice::first",
    "core::slice::first_mut",
    "core::slice::get",
    "core::slice::is_empty",
    "core::slice::iter",
    "core::slice::last",
    "core::slice::last_mut",
    "core::slice::len",
    "core::slice::split_at",
    "core::slice::split_at_mut",
}
REQUIRED_ARTIFACTS = (
    "inventory/SLICE_EXEC_FN_INVENTORY.md",
    "inventory/slice_exec_fn_inventory.csv",
    "inventory/slice_exec_fn_inventory.json",
    "specs/existing_vstd_slice_specs.rs",
    "specs/generated_slice_specs.rs",
    "specs/all_slice_specs.rs",
    "catalog/slice_spec_catalog.csv",
    "catalog/slice_spec_catalog.json",
    "catalog/SLICE_SPEC_REVIEW.md",
    "provenance/source_manifest.csv",
    "provenance/source_manifest.json",
    "verification/shared_helper_target_usage_audit.csv",
    "verification/shared_helper_target_usage_audit.json",
    "verification/check_inventory.py",
    "verification/check_catalog.py",
    "verification/check_provenance.py",
    "verification/check_contracts.py",
    "verification/check_artifact_integrity.py",
)
EVIDENCE_JSON = Path("verification/artifact_integrity_evidence.json")
EVIDENCE_CSV = Path("verification/artifact_integrity_evidence.csv")
EVIDENCE_MD = Path("verification/ARTIFACT_INTEGRITY_EVIDENCE.md")
ACTIVE_FEEDBACK_DETERMINISM_RUN = (
    "verification/evidence/slice_feedback_determinism/"
    "all-20260811T1142Z-comparator-ordering-refresh"
)
FEEDBACK_DETERMINISM_MANIFEST = Path("verification/evidence/slice_feedback_determinism/latest_manifest.json")
ACTIVE_FEEDBACK_DETERMINISM_MANIFEST = Path(ACTIVE_FEEDBACK_DETERMINISM_RUN) / "run_manifest.json"
STALE_DETERMINISM_REFS = (
    "all-20260811T1030Z-adjacent-fnmut",
    "all-20260811T1100Z-iterator-chunk-state-refresh",
)
ACTIVE_DETERMINISM_REF_ARTIFACTS = (
    "catalog/slice_spec_catalog.csv",
    "catalog/slice_spec_catalog.json",
    "catalog/SLICE_SPEC_REVIEW.md",
    "specs/generated_slice_specs.rs",
    "specs/all_slice_specs.rs",
)
EXPECTED_FEEDBACK_STATUS_COUNTS = {"ok": EXPECTED_TOTAL - EXPECTED_EXISTING_VSTD}
EXPECTED_FEEDBACK_R0_Z3_COUNTS = {"unknown": 75, "unsat": 45}
UNKNOWN_REASON_CLASSES = {
    "clone-or-callback-effect-boundary",
    "disjoint-mutable-alias-boundary",
    "duplicate-or-callback-search-boundary",
    "iterator-or-subslice-state-boundary",
    "maybeuninit-storage-boundary",
    "mutable-reference-view-boundary",
    "raw-pointer-provenance-boundary",
    "unstable-sort-or-selection-boundary",
}
REQUIRED_FEEDBACK_ARTIFACTS = (
    "synthetic_spec.rs",
    "det_spec.json",
    "det_harness.rs",
    "det_stdout.txt",
    "det_stderr.txt",
    "verus_stdout.txt",
    "verus_stderr.txt",
    "candidate.json",
    "result.json",
)
REQUIRED_CATALOG_COLUMNS = {
    "target",
    "semantic_family",
    "status",
    "contract_text",
    "requires",
    "ensures",
    "shared_helpers",
    "source_reference",
    "source_excerpt",
    "strength",
    "known_risks",
    "typecheck_result",
    "determinism_result",
    "target_binding_result",
    "signature_shape_result",
    "generic_bounds_result",
    "reviewer_notes",
}
REQUIRED_SPEC_MARKER_FIELDS = {
    "status",
    "family",
    "source",
    "signature",
    "requires",
    "ensures",
    "shared_helpers",
    "typecheck_result",
    "determinism_result",
    "target_binding_result",
    "signature_shape_result",
    "generic_bounds_result",
    "reviewer_notes",
    "contract_text",
}
RELATIONAL_TOKENS = (
    "@",
    "Seq",
    "subrange",
    "update",
    "old(",
    "final(",
    "permutation",
    "sorted",
    "partition",
    "prefix",
    "suffix",
    "pointer",
    "provenance",
    "len",
    "range",
    "remainder",
    "ascii",
    "utf8",
    "initialized",
    "drop",
)
BANNED_CONTRACT_FRAGMENTS = (
    "ensures true",
    "requires false",
    "arbitrary()",
    "fresh_uninterp",
    "fresh uninterp",
    "unconstrained result",
    "result == fresh",
)


def fail(message: str) -> None:
    print(f"artifact integrity failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing CSV {path}")
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        fail(f"{path} is empty")
    return rows


def read_json(path: Path) -> dict[str, object]:
    if not path.is_file():
        fail(f"missing JSON {path}")
    with path.open() as stream:
        payload = json.load(stream)
    if not isinstance(payload, dict):
        fail(f"{path} must contain a JSON object")
    return payload


def parse_spec_blocks(text: str) -> dict[str, dict[str, str]]:
    pattern = re.compile(
        r"// BEGIN SLICE_SPEC target=(?P<target>\S+)\n(?P<body>.*?)// END SLICE_SPEC",
        re.DOTALL,
    )
    blocks: dict[str, dict[str, str]] = {}
    for match in pattern.finditer(text):
        target = match.group("target")
        if target in blocks:
            fail(f"duplicate spec block for {target}")
        fields: dict[str, str] = {}
        for line in match.group("body").splitlines():
            if not line.startswith("// ") or ": " not in line:
                continue
            key, value = line[3:].split(": ", 1)
            fields[key.strip()] = value.strip()
        blocks[target] = fields
    return blocks


def run_check(root: Path, args: list[str]) -> dict[str, object]:
    command = [sys.executable, *args]
    completed = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        fail(
            "check command failed: "
            + " ".join(command)
            + f"\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return {
        "command": " ".join(command),
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def ensure_required_artifacts(root: Path) -> None:
    for rel in REQUIRED_ARTIFACTS:
        path = root / rel
        if not path.is_file():
            fail(f"missing required artifact {rel}")
    if not (root / "rust-core-slice").is_dir():
        fail("missing rust-core-slice source copy")
    if not (root / "vstd-baseline").is_dir():
        fail("missing vstd-baseline source copy")
    other_module_dirs = [
        path.name
        for path in root.iterdir()
        if path.is_dir() and path.name.startswith("rust-core-") and path.name != "rust-core-slice"
    ]
    if other_module_dirs:
        fail(f"unexpected additional Rust module copies: {sorted(other_module_dirs)}")


def validate_payloads(root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, dict[str, str]]]:
    inventory_path = root / "inventory" / "slice_exec_fn_inventory.csv"
    catalog_path = root / "catalog" / "slice_spec_catalog.csv"
    specs_path = root / "specs" / "all_slice_specs.rs"
    inventory = read_csv(inventory_path)
    catalog = read_csv(catalog_path)
    blocks = parse_spec_blocks(specs_path.read_text())

    if len(inventory) != EXPECTED_TOTAL:
        fail(f"inventory has {len(inventory)} rows, expected {EXPECTED_TOTAL}")
    if len(catalog) != EXPECTED_TOTAL:
        fail(f"catalog has {len(catalog)} rows, expected {EXPECTED_TOTAL}")
    if len(blocks) != EXPECTED_TOTAL:
        fail(f"specs have {len(blocks)} marked blocks, expected {EXPECTED_TOTAL}")
    missing_columns = REQUIRED_CATALOG_COLUMNS.difference(catalog[0].keys())
    if missing_columns:
        fail(f"catalog missing required columns {sorted(missing_columns)}")

    inventory_by_target = {row["canonical_target"]: row for row in inventory}
    catalog_by_target = {row["target"]: row for row in catalog}
    if len(inventory_by_target) != EXPECTED_TOTAL:
        fail("inventory targets are not unique")
    if len(catalog_by_target) != EXPECTED_TOTAL:
        fail("catalog targets are not unique")
    if set(inventory_by_target) != set(catalog_by_target):
        fail("inventory and catalog target sets differ")
    if set(blocks) != set(inventory_by_target):
        fail("spec block target set differs from inventory")

    existing_catalog = {row["target"] for row in catalog if row["status"] == "existing-vstd"}
    if existing_catalog != EXISTING_VSTD:
        fail(
            "existing-vstd catalog set mismatch: "
            f"missing={sorted(EXISTING_VSTD - existing_catalog)} "
            f"extra={sorted(existing_catalog - EXISTING_VSTD)}"
        )
    generated_count = sum(1 for row in catalog if row["status"] == "generated-new-real-relation-spec")
    justified_count = sum(1 for row in catalog if row["status"] == "justified-no-spec")
    if generated_count + justified_count != EXPECTED_TOTAL - EXPECTED_EXISTING_VSTD:
        fail("generated and justified catalog rows do not cover the 120 non-vstd APIs")

    inventory_json = read_json(root / "inventory" / "slice_exec_fn_inventory.json")
    catalog_json = read_json(root / "catalog" / "slice_spec_catalog.json")
    helper_usage_json = read_json(root / "verification" / "shared_helper_target_usage_audit.json")
    if inventory_json.get("summary", {}).get("total_stable_unique_exec_apis") != EXPECTED_TOTAL:
        fail("inventory JSON summary total is not 132")
    if catalog_json.get("summary", {}).get("total") != EXPECTED_TOTAL:
        fail("catalog JSON summary total is not 132")
    if catalog_json.get("summary", {}).get("generated_new_real_relation_specs") != generated_count:
        fail("catalog JSON generated count differs from CSV")
    if catalog_json.get("summary", {}).get("justified_no_spec", 0) != justified_count:
        fail("catalog JSON justified-no-spec count differs from CSV")
    helper_usage_summary = helper_usage_json.get("summary", {})
    if not isinstance(helper_usage_summary, dict):
        fail("shared helper target usage audit summary is missing")
    if helper_usage_summary.get("generated_targets") != EXPECTED_TOTAL - EXPECTED_EXISTING_VSTD:
        fail("shared helper target usage audit generated target count is not 120")
    if helper_usage_summary.get("audited_helpers_declared") != 41:
        fail("shared helper target usage audit does not cover the 41 audited helpers")

    for target, block in blocks.items():
        missing = REQUIRED_SPEC_MARKER_FIELDS.difference(block)
        if missing:
            fail(f"{target} spec marker missing fields {sorted(missing)}")
        catalog_row = catalog_by_target[target]
        inventory_row = inventory_by_target[target]
        if block["status"] != catalog_row["status"]:
            fail(f"{target} status differs between spec block and catalog")
        if block["family"] != catalog_row["semantic_family"]:
            fail(f"{target} semantic family differs between spec block and catalog")
        if block["signature"] != inventory_row["signature"]:
            fail(f"{target} signature differs between spec block and inventory")
        if block["generic_bounds_result"] != inventory_row["generic_bounds"]:
            fail(f"{target} generic bounds differ between spec block and inventory")

    return inventory, catalog, blocks


def validate_recorded_evidence(
    inventory: list[dict[str, str]],
    catalog: list[dict[str, str]],
    blocks: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    inventory_by_target = {row["canonical_target"]: row for row in inventory}
    per_target: list[dict[str, str]] = []
    for row in catalog:
        target = row["target"]
        inventory_row = inventory_by_target[target]
        block = blocks[target]
        for column in REQUIRED_CATALOG_COLUMNS:
            if not row.get(column, "").strip():
                fail(f"{target} has empty catalog evidence column {column}")
        contract_lower = " ".join(
            [row["requires"], row["ensures"], row["contract_text"], block["requires"], block["ensures"], block["contract_text"]]
        ).lower()
        for fragment in BANNED_CONTRACT_FRAGMENTS:
            if fragment in contract_lower:
                fail(f"{target} contains banned/vacuous contract fragment {fragment!r}")
        if row["source_reference"] != inventory_row["source_location"]:
            fail(f"{target} source reference differs from inventory source location")
        if row["generic_bounds_result"] != inventory_row["generic_bounds"]:
            fail(f"{target} generic-bounds evidence differs from inventory")
        if "signature" not in row["signature_shape_result"].lower():
            fail(f"{target} signature-shape evidence does not mention the signature")
        if row["status"] == "generated-new-real-relation-spec":
            if not row["target_binding_result"].startswith(f"target {target} bound from inventory declaration "):
                fail(f"{target} target-binding evidence is not tied to the inventory declaration")
            if not any(token.lower() in contract_lower for token in RELATIONAL_TOKENS):
                fail(f"{target} generated contract lacks a shared-model relation token")
            anti_vacuity_result = "passed: generated relation uses shared Seq/View vocabulary and no banned vacuity fragment"
            coverage_result = "covered: generated-new-real-relation-spec"
        elif row["status"] == "existing-vstd":
            if target not in EXISTING_VSTD:
                fail(f"{target} is unexpectedly marked existing-vstd")
            if target not in row["target_binding_result"] or "vstd" not in row["target_binding_result"].lower():
                fail(f"{target} existing-vstd target-binding evidence does not name the vstd binding")
            anti_vacuity_result = "passed: exact existing vstd relation retained and no banned vacuity fragment"
            coverage_result = "covered: existing-vstd"
        elif row["status"] == "justified-no-spec":
            needed = ("strongest weak spec", "missing", "prerequisite", "operator")
            absent = [word for word in needed if word not in contract_lower]
            if absent:
                fail(f"{target} no-spec justification is incomplete: missing {absent}")
            anti_vacuity_result = "passed: no-spec justification avoids vacuous contract"
            coverage_result = "covered: justified-no-spec"
        else:
            fail(f"{target} has unexpected catalog status {row['status']}")

        per_target.append(
            {
                "target": target,
                "status": row["status"],
                "semantic_family": row["semantic_family"],
                "contract_coverage_result": coverage_result,
                "typecheck_result": row["typecheck_result"],
                "determinism_result": row["determinism_result"],
                "target_binding_result": row["target_binding_result"],
                "signature_shape_result": row["signature_shape_result"],
                "generic_bounds_result": row["generic_bounds_result"],
                "anti_vacuity_result": anti_vacuity_result,
                "source_fidelity_result": "passed: source reference, signature, and generic bounds match inventory",
            }
        )
    return per_target


def count_by(rows: list[dict[str, str]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = row[key]
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def feedback_outcome(result: dict[str, object]) -> str:
    status = str(result.get("status", "runner_crash"))
    r0_z3 = result.get("r0_z3")
    if status == "ok":
        if r0_z3 == "unsat":
            return "UNSAT"
        if r0_z3 == "sat":
            return "SAT"
        if r0_z3 == "unknown":
            return "UNKNOWN"
        fail(f"{result.get('target')} has status=ok without a recognized r0_z3")
    if status in {"no_ensures", "unsupported_mut_ref_return"}:
        return "unsupported"
    if status == "verus_error":
        return "Verus error"
    return "runner crash"


def sorted_counter(values: object) -> dict[str, int]:
    if not isinstance(values, list):
        fail("feedback manifest results must be a list")
    return dict(sorted(Counter(str(value) for value in values).items()))


def validate_unknown_reason_fields(
    *,
    target: str,
    entry: dict[str, object],
    result: dict[str, object],
) -> str | None:
    is_unknown = result.get("status") == "ok" and result.get("r0_z3") == "unknown"
    if not is_unknown:
        if entry.get("unknown_reason_class") or result.get("unknown_reason_class"):
            fail(f"{target} is not R0=UNKNOWN but records an UNKNOWN reason class")
        return None
    reason_class = result.get("unknown_reason_class")
    reason = result.get("unknown_reason")
    if not isinstance(reason_class, str) or reason_class not in UNKNOWN_REASON_CLASSES:
        fail(f"{target} R0=UNKNOWN result has missing or unknown reason class")
    if not isinstance(reason, str) or not reason.strip():
        fail(f"{target} R0=UNKNOWN result has empty review reason")
    if entry.get("unknown_reason_class") != reason_class:
        fail(f"{target} manifest UNKNOWN reason class differs from result JSON")
    if entry.get("unknown_reason") != reason:
        fail(f"{target} manifest UNKNOWN reason text differs from result JSON")
    return reason_class


def validate_no_stale_active_refs(root: Path, extra_files: tuple[str, ...] = ()) -> None:
    for rel in (*ACTIVE_DETERMINISM_REF_ARTIFACTS, *extra_files):
        path = root / rel
        if not path.is_file():
            fail(f"missing active determinism reference artifact {rel}")
        text = path.read_text()
        stale_refs = [ref for ref in STALE_DETERMINISM_REFS if ref in text]
        if stale_refs:
            fail(f"{rel} contains stale determinism refs {stale_refs}")


def validate_feedback_artifact(root: Path, result: dict[str, object]) -> None:
    target = str(result.get("target"))
    artifacts = result.get("artifacts")
    if not isinstance(artifacts, dict):
        fail(f"{target} feedback result has no artifacts map")
    for name in REQUIRED_FEEDBACK_ARTIFACTS:
        rel = artifacts.get(name)
        if not isinstance(rel, str) or not rel.startswith(ACTIVE_FEEDBACK_DETERMINISM_RUN + "/"):
            fail(f"{target} feedback artifact {name} does not reference the active feedback run")
        if not (root / rel).is_file():
            fail(f"{target} feedback result is missing artifact {name}")
    if "r0_z3" in result:
        rel = artifacts.get("schema_search_evidence.json")
        if not isinstance(rel, str) or not rel.startswith(ACTIVE_FEEDBACK_DETERMINISM_RUN + "/"):
            fail(f"{target} feedback result has r0_z3 but no active-run schema-search evidence")
        if not (root / rel).is_file():
            fail(f"{target} feedback result has r0_z3 but missing schema-search evidence")
        smt2_files = artifacts.get("smt2_files")
        if not isinstance(smt2_files, list) or not smt2_files:
            fail(f"{target} feedback result has r0_z3 but no SMT evidence")
        for rel_smt in smt2_files:
            if not isinstance(rel_smt, str) or not rel_smt.startswith(ACTIVE_FEEDBACK_DETERMINISM_RUN + "/"):
                fail(f"{target} feedback SMT evidence does not reference the active feedback run")
            if not (root / rel_smt).is_file():
                fail(f"{target} feedback result references missing SMT evidence")


def validate_active_feedback_determinism(
    root: Path,
    catalog: list[dict[str, str]],
    blocks: dict[str, dict[str, str]],
) -> dict[str, object]:
    validate_no_stale_active_refs(root)
    latest_path = root / FEEDBACK_DETERMINISM_MANIFEST
    active_path = root / ACTIVE_FEEDBACK_DETERMINISM_MANIFEST
    if not latest_path.is_file():
        fail(f"missing feedback determinism manifest {latest_path}")
    if not active_path.is_file():
        fail(f"missing active feedback determinism manifest {active_path}")

    latest_manifest = read_json(latest_path)
    active_manifest = read_json(active_path)
    if latest_manifest != active_manifest:
        fail("latest feedback determinism manifest is not the active feedback determinism run")

    generated = [
        row for row in catalog if row["status"] == "generated-new-real-relation-spec"
    ]
    entries = latest_manifest.get("results")
    if not isinstance(entries, list):
        fail("feedback determinism manifest results must be a list")
    if len(entries) != EXPECTED_TOTAL - EXPECTED_EXISTING_VSTD:
        fail(f"feedback manifest has {len(entries)} results, expected 120")

    generated_targets = {row["target"] for row in generated}
    manifest_targets = {entry.get("target") for entry in entries if isinstance(entry, dict)}
    if manifest_targets != generated_targets:
        fail(
            "feedback manifest target set differs from generated catalog targets: "
            f"missing={sorted(generated_targets - manifest_targets)} "
            f"extra={sorted(manifest_targets - generated_targets)}"
        )

    status_counts = sorted_counter([entry.get("status") for entry in entries if isinstance(entry, dict)])
    r0_z3_counts = sorted_counter([entry.get("r0_z3") for entry in entries if isinstance(entry, dict)])
    if status_counts != EXPECTED_FEEDBACK_STATUS_COUNTS:
        fail(f"feedback manifest status counts {status_counts} differ from expected {EXPECTED_FEEDBACK_STATUS_COUNTS}")
    if r0_z3_counts != EXPECTED_FEEDBACK_R0_Z3_COUNTS:
        fail(f"feedback manifest r0_z3 counts {r0_z3_counts} differ from expected {EXPECTED_FEEDBACK_R0_Z3_COUNTS}")
    manifest_r0_counts = latest_manifest.get("r0_z3_counts")
    if manifest_r0_counts != EXPECTED_FEEDBACK_R0_Z3_COUNTS:
        fail(f"feedback manifest summary r0_z3_counts {manifest_r0_counts} differ from expected {EXPECTED_FEEDBACK_R0_Z3_COUNTS}")

    results: dict[str, dict[str, object]] = {}
    entries_by_target: dict[str, dict[str, object]] = {}
    unknown_reason_by_target: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            fail("feedback manifest contains a non-object result entry")
        target = str(entry.get("target"))
        rel = entry.get("result_json")
        if not isinstance(rel, str) or not rel.startswith(ACTIVE_FEEDBACK_DETERMINISM_RUN + "/"):
            fail(f"{target} manifest result_json does not reference the active feedback run")
        result_path = root / rel
        if not result_path.is_file():
            fail(f"{target} manifest entry has missing result_json")
        payload = read_json(result_path)
        if payload.get("target") != target:
            fail(f"{target} feedback result target mismatch")
        if payload.get("status") != entry.get("status"):
            fail(f"{target} feedback result status differs from manifest entry")
        if payload.get("r0_z3") != entry.get("r0_z3"):
            fail(f"{target} feedback result r0_z3 differs from manifest entry")
        validate_feedback_artifact(root, payload)
        reason_class = validate_unknown_reason_fields(
            target=target,
            entry=entry,
            result=payload,
        )
        if reason_class is not None:
            unknown_reason_by_target[target] = reason_class
        results[target] = payload
        entries_by_target[target] = entry

    unknown_reason_counts = dict(sorted(Counter(unknown_reason_by_target.values()).items()))
    manifest_unknown_reason_counts = latest_manifest.get("unknown_reason_counts")
    if manifest_unknown_reason_counts != unknown_reason_counts:
        fail(
            "feedback manifest unknown_reason_counts "
            f"{manifest_unknown_reason_counts} differ from computed {unknown_reason_counts}"
        )

    for row in generated:
        target = row["target"]
        result = results[target]
        determinism_texts = (row["determinism_result"], blocks[target]["determinism_result"])
        for text in determinism_texts:
            if ACTIVE_FEEDBACK_DETERMINISM_RUN not in text:
                fail(f"{target} determinism_result does not reference the active feedback run")
            if result["artifacts"]["result.json"] not in text:
                fail(f"{target} determinism_result does not reference its active feedback result JSON")
            if f"R0={feedback_outcome(result)}" not in text:
                fail(f"{target} determinism_result does not record feedback outcome")
            if f"r0_z3={result.get('r0_z3')}" not in text:
                fail(f"{target} determinism_result does not record r0_z3")
            reason_class = unknown_reason_by_target.get(target)
            if reason_class is not None and f"unknown_reason={reason_class}" not in text:
                fail(f"{target} determinism_result does not record UNKNOWN reason class")

    review_text = (root / "catalog" / "SLICE_SPEC_REVIEW.md").read_text()
    if "## UNKNOWN reason taxonomy" not in review_text:
        fail("review summary is missing UNKNOWN reason taxonomy section")
    for target, reason_class in unknown_reason_by_target.items():
        if target not in review_text:
            fail(f"{target} R0=UNKNOWN reason classification is missing from review summary")
        if reason_class not in review_text:
            fail(f"{target} UNKNOWN reason class is missing from review summary")

    return {
        "active_run": ACTIVE_FEEDBACK_DETERMINISM_RUN,
        "latest_manifest": str(FEEDBACK_DETERMINISM_MANIFEST),
        "run_manifest": str(ACTIVE_FEEDBACK_DETERMINISM_MANIFEST),
        "generated_targets": len(generated),
        "status_counts": status_counts,
        "r0_z3_counts": r0_z3_counts,
        "unknown_reason_counts": unknown_reason_counts,
    }


def artifact_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in REQUIRED_ARTIFACTS:
        hashes[rel] = sha256(root / rel)
    return hashes


def write_evidence(root: Path, evidence: dict[str, object], per_target: list[dict[str, str]]) -> None:
    json_path = root / EVIDENCE_JSON
    csv_path = root / EVIDENCE_CSV
    md_path = root / EVIDENCE_MD

    json_text = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if not json_path.exists() or json_path.read_text() != json_text:
        json_path.write_text(json_text)

    fieldnames = [
        "target",
        "status",
        "semantic_family",
        "contract_coverage_result",
        "typecheck_result",
        "determinism_result",
        "target_binding_result",
        "signature_shape_result",
        "generic_bounds_result",
        "anti_vacuity_result",
        "source_fidelity_result",
    ]
    rows: list[str] = []
    from io import StringIO

    stream = StringIO()
    writer = csv.DictWriter(stream, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(per_target)
    csv_text = stream.getvalue()
    if not csv_path.exists() or csv_path.read_text() != csv_text:
        csv_path.write_text(csv_text)

    summary = evidence["summary"]
    feedback = evidence["feedback_determinism"]
    md_text = "\n".join(
        [
            "# Artifact Integrity Evidence",
            "",
            f"- total stable unique exec APIs: {summary['total_targets']}",
            f"- existing vstd specs: {summary['existing_vstd']}",
            f"- generated relation specs: {summary['generated_new_real_relation_specs']}",
            f"- justified no-spec rows: {summary['justified_no_spec']}",
            f"- active feedback determinism run: `{feedback['active_run']}`",
            f"- feedback manifest status counts: {feedback['status_counts']}",
            f"- feedback R0/Z3 split: {feedback['r0_z3_counts']}",
            f"- feedback UNKNOWN reason split: {feedback['unknown_reason_counts']}",
            "- recorded evidence: provenance, contract coverage, determinism, target binding, signature shape, generic bounds, anti-vacuity, and source fidelity",
            "",
        ]
    )
    if not md_path.exists() or md_path.read_text() != md_text:
        md_path.write_text(md_text)

    for path in (json_path, csv_path, md_path):
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"failed to write evidence file {path.relative_to(root)}")
    validate_no_stale_active_refs(root, (str(EVIDENCE_JSON), str(EVIDENCE_CSV), str(EVIDENCE_MD)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and record final core::slice artifact integrity evidence.")
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        fail(f"missing experiment root {root}")
    if not MODULES_CSV.is_file():
        fail(f"missing module authority CSV {MODULES_CSV}")

    ensure_required_artifacts(root)
    checks = [
        run_check(
            root,
            [
                "verification/check_inventory.py",
                "--modules-csv",
                str(MODULES_CSV),
                "--inventory",
                "inventory/slice_exec_fn_inventory.csv",
                "--expect-total",
                str(EXPECTED_TOTAL),
                "--expect-existing-vstd",
                str(EXPECTED_EXISTING_VSTD),
            ],
        ),
        run_check(
            root,
            [
                "verification/check_catalog.py",
                "--inventory",
                "inventory/slice_exec_fn_inventory.csv",
                "--catalog",
                "catalog/slice_spec_catalog.csv",
                "--expect-total",
                str(EXPECTED_TOTAL),
                "--expect-existing-vstd",
                str(EXPECTED_EXISTING_VSTD),
            ],
        ),
        run_check(
            root,
            [
                "verification/check_provenance.py",
                "--root",
                ".",
                "--rust-copy",
                "rust-core-slice",
                "--vstd-copy",
                "vstd-baseline",
            ],
        ),
        run_check(
            root,
            [
                "verification/check_contracts.py",
                "--specs",
                "specs/all_slice_specs.rs",
                "--catalog",
                "catalog/slice_spec_catalog.csv",
            ],
        ),
    ]
    inventory, catalog, blocks = validate_payloads(root)
    per_target = validate_recorded_evidence(inventory, catalog, blocks)
    feedback_summary = validate_active_feedback_determinism(root, catalog, blocks)
    status_counts = count_by(catalog, "status")
    summary = {
        "total_targets": len(catalog),
        "existing_vstd": status_counts.get("existing-vstd", 0),
        "generated_new_real_relation_specs": status_counts.get("generated-new-real-relation-spec", 0),
        "justified_no_spec": status_counts.get("justified-no-spec", 0),
        "spec_blocks": len(blocks),
        "inventory_targets": len(inventory),
        "anti_vacuity": "passed",
        "source_fidelity": "passed",
        "no_additional_rust_module_started": "passed",
    }
    if summary["total_targets"] != EXPECTED_TOTAL or summary["existing_vstd"] != EXPECTED_EXISTING_VSTD:
        fail(f"unexpected summary counts: {summary}")

    evidence: dict[str, object] = {
        "schema_version": 1,
        "root": str(root),
        "module_authority_csv": str(MODULES_CSV),
        "summary": summary,
        "shared_helper_target_usage_audit": read_json(
            root / "verification" / "shared_helper_target_usage_audit.json"
        ).get("summary", {}),
        "status_distribution": status_counts,
        "determinism_distribution": count_by(catalog, "determinism_result"),
        "typecheck_distribution": count_by(catalog, "typecheck_result"),
        "semantic_family_distribution": count_by(catalog, "semantic_family"),
        "check_commands": checks,
        "feedback_determinism": feedback_summary,
        "artifact_hashes": artifact_hashes(root),
        "per_target_evidence": per_target,
        "evidence_files": [str(EVIDENCE_JSON), str(EVIDENCE_CSV), str(EVIDENCE_MD)],
    }
    write_evidence(root, evidence, per_target)
    print(
        "artifact integrity ok: "
        f"{EXPECTED_TOTAL} targets; "
        f"{EXPECTED_EXISTING_VSTD} existing-vstd; "
        f"{EXPECTED_TOTAL - EXPECTED_EXISTING_VSTD} generated/justified; "
        "evidence recorded in verification/artifact_integrity_evidence.*"
    )


if __name__ == "__main__":
    main()
