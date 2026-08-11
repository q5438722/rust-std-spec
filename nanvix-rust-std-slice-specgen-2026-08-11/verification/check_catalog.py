#!/usr/bin/env python3
"""Validate the core::slice spec catalog against the locked inventory."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


REQUIRED_COLUMNS = {
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

BOOTSTRAP_VERUS_TARGETS = {
    "core::slice::contains",
    "core::slice::ends_with",
    "core::slice::starts_with",
}

MUTATION_VERUS_TARGETS = {
    "core::slice::binary_search",
    "core::slice::binary_search_by",
    "core::slice::binary_search_by_key",
    "core::slice::clone_from_slice",
    "core::slice::contains",
    "core::slice::ends_with",
    "core::slice::fill",
    "core::slice::fill_with",
    "core::slice::partition_point",
    "core::slice::reverse",
    "core::slice::rotate_left",
    "core::slice::rotate_right",
    "core::slice::starts_with",
    "core::slice::swap",
    "core::slice::swap_with_slice",
}

REMAINING_VERUS_TARGETS = {
    "core::slice::align_to",
    "core::slice::align_to_mut",
    "core::slice::as_flattened",
    "core::slice::as_flattened_mut",
    "core::slice::as_mut_ptr",
    "core::slice::as_mut_ptr_range",
    "core::slice::as_ptr",
    "core::slice::as_ptr_range",
    "core::slice::assume_init_drop",
    "core::slice::assume_init_mut",
    "core::slice::assume_init_ref",
    "core::slice::element_offset",
    "core::slice::eq_ignore_ascii_case",
    "core::slice::escape_ascii",
    "core::slice::from_mut",
    "core::slice::from_raw_parts",
    "core::slice::from_raw_parts_mut",
    "core::slice::from_ref",
    "core::slice::get_disjoint_mut",
    "core::slice::get_disjoint_unchecked_mut",
    "core::slice::get_mut",
    "core::slice::get_unchecked",
    "core::slice::get_unchecked_mut",
    "core::slice::is_ascii",
    "core::slice::is_sorted",
    "core::slice::is_sorted_by",
    "core::slice::is_sorted_by_key",
    "core::slice::make_ascii_lowercase",
    "core::slice::make_ascii_uppercase",
    "core::slice::select_nth_unstable",
    "core::slice::select_nth_unstable_by",
    "core::slice::select_nth_unstable_by_key",
    "core::slice::sort_unstable",
    "core::slice::sort_unstable_by",
    "core::slice::sort_unstable_by_key",
    "core::slice::strip_circumfix",
    "core::slice::strip_prefix",
    "core::slice::strip_suffix",
    "core::slice::subslice_range",
    "core::slice::trim_ascii",
    "core::slice::trim_ascii_end",
    "core::slice::trim_ascii_start",
    "core::slice::write_clone_of_slice",
    "core::slice::write_copy_of_slice",
}

BOOTSTRAP_VERUS_EVIDENCE = Path("verification/evidence/slice_observation_bootstrap.verus.json")
BOOTSTRAP_VERUS_HARNESS = "verification/harnesses/slice_observation_bootstrap.rs"
BOOTSTRAP_VERUS_STDOUT = "verification/evidence/slice_observation_bootstrap.verus.stdout"
BOOTSTRAP_VERUS_STDERR = "verification/evidence/slice_observation_bootstrap.verus.stderr"
MUTATION_VERUS_EVIDENCE = Path("verification/evidence/slice_observation_mutation_batch.verus.json")
MUTATION_VERUS_HARNESS = "verification/harnesses/slice_observation_mutation_batch.rs"
MUTATION_VERUS_STDOUT = "verification/evidence/slice_observation_mutation_batch.verus.stdout"
MUTATION_VERUS_STDERR = "verification/evidence/slice_observation_mutation_batch.verus.stderr"
REMAINING_VERUS_EVIDENCE = Path("verification/evidence/slice_remaining_families_batch.verus.json")
REMAINING_VERUS_HARNESS = "verification/harnesses/slice_remaining_families_batch.rs"
REMAINING_VERUS_STDOUT = "verification/evidence/slice_remaining_families_batch.verus.stdout"
REMAINING_VERUS_STDERR = "verification/evidence/slice_remaining_families_batch.verus.stderr"
FEEDBACK_DETERMINISM_MANIFEST = Path(
    "verification/evidence/slice_feedback_determinism/latest_manifest.json"
)
STALE_DIRECT_DETERMINISM_FRAGMENTS = (
    "0 exec ensures targets",
    "verusage runner",
    "assume_specification harness",
)
STALE_KNOWN_RISKS_PHRASES = (
    "determinism checker unsupported for " + "assume_specification-only harness",
    "determinism checker is unsupported for " + "assume-specification-only harnesses",
)
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


def fail(message: str) -> None:
    print(f"catalog check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing file {path}")
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        fail(f"{path} is empty")
    return rows


def records_bootstrap_verus_typecheck(row: dict[str, str], root: Path) -> bool:
    if row["target"] not in BOOTSTRAP_VERUS_TARGETS:
        return False

    evidence_path = root / BOOTSTRAP_VERUS_EVIDENCE
    if not evidence_path.is_file():
        fail(f"{row['target']} records Verus typecheck evidence but {evidence_path} is missing")
    evidence = json.loads(evidence_path.read_text())
    if evidence.get("return_code") != 0:
        fail(f"{row['target']} records Verus typecheck evidence but {evidence_path} return_code is not 0")
    if evidence.get("harness_path") != BOOTSTRAP_VERUS_HARNESS:
        fail(f"{row['target']} records Verus typecheck evidence with wrong harness in {evidence_path}")
    if evidence.get("stdout_path") != BOOTSTRAP_VERUS_STDOUT:
        fail(f"{row['target']} records Verus typecheck evidence with wrong stdout path in {evidence_path}")
    if evidence.get("stderr_path") != BOOTSTRAP_VERUS_STDERR:
        fail(f"{row['target']} records Verus typecheck evidence with wrong stderr path in {evidence_path}")

    result = row["typecheck_result"]
    required_fragments = (
        "verus-typecheck: pass",
        "rc=0",
        f"command={evidence.get('command')}",
        f"harness={BOOTSTRAP_VERUS_HARNESS}",
        f"stdout={BOOTSTRAP_VERUS_STDOUT}",
        f"stderr={BOOTSTRAP_VERUS_STDERR}",
    )
    return all(fragment in result for fragment in required_fragments)


def records_mutation_verus_typecheck(row: dict[str, str], root: Path) -> bool:
    if row["target"] not in MUTATION_VERUS_TARGETS:
        return False

    evidence_path = root / MUTATION_VERUS_EVIDENCE
    if not evidence_path.is_file():
        fail(f"{row['target']} records Verus typecheck evidence but {evidence_path} is missing")
    evidence = json.loads(evidence_path.read_text())
    if evidence.get("return_code") != 0:
        fail(f"{row['target']} records Verus typecheck evidence but {evidence_path} return_code is not 0")
    if evidence.get("harness_path") != MUTATION_VERUS_HARNESS:
        fail(f"{row['target']} records Verus typecheck evidence with wrong harness in {evidence_path}")
    if evidence.get("stdout_path") != MUTATION_VERUS_STDOUT:
        fail(f"{row['target']} records Verus typecheck evidence with wrong stdout path in {evidence_path}")
    if evidence.get("stderr_path") != MUTATION_VERUS_STDERR:
        fail(f"{row['target']} records Verus typecheck evidence with wrong stderr path in {evidence_path}")

    result = row["typecheck_result"]
    required_fragments = (
        "verus-typecheck: pass",
        "rc=0",
        f"command={evidence.get('command')}",
        f"harness={MUTATION_VERUS_HARNESS}",
        f"stdout={MUTATION_VERUS_STDOUT}",
        f"stderr={MUTATION_VERUS_STDERR}",
    )
    return all(fragment in result for fragment in required_fragments)


def records_remaining_verus_typecheck(row: dict[str, str], root: Path) -> bool:
    if row["target"] not in REMAINING_VERUS_TARGETS:
        return False

    evidence_path = root / REMAINING_VERUS_EVIDENCE
    if not evidence_path.is_file():
        fail(f"{row['target']} records Verus typecheck evidence but {evidence_path} is missing")
    evidence = json.loads(evidence_path.read_text())
    if evidence.get("return_code") != 0:
        fail(f"{row['target']} records Verus typecheck evidence but {evidence_path} return_code is not 0")
    if evidence.get("harness_path") != REMAINING_VERUS_HARNESS:
        fail(f"{row['target']} records Verus typecheck evidence with wrong harness in {evidence_path}")
    if evidence.get("stdout_path") != REMAINING_VERUS_STDOUT:
        fail(f"{row['target']} records Verus typecheck evidence with wrong stdout path in {evidence_path}")
    if evidence.get("stderr_path") != REMAINING_VERUS_STDERR:
        fail(f"{row['target']} records Verus typecheck evidence with wrong stderr path in {evidence_path}")

    result = row["typecheck_result"]
    required_fragments = (
        "verus-typecheck: pass",
        "rc=0",
        f"command={evidence.get('command')}",
        f"harness={REMAINING_VERUS_HARNESS}",
        f"stdout={REMAINING_VERUS_STDOUT}",
        f"stderr={REMAINING_VERUS_STDERR}",
    )
    return all(fragment in result for fragment in required_fragments)


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


def validate_unknown_reason(
    *,
    target: str,
    entry: dict[str, object],
    result: dict[str, object],
    determinism_text: str,
) -> None:
    is_unknown = result.get("status") == "ok" and result.get("r0_z3") == "unknown"
    if not is_unknown:
        if entry.get("unknown_reason_class") or result.get("unknown_reason_class"):
            fail(f"{target} is not R0=UNKNOWN but records an UNKNOWN reason class")
        return
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
    if f"unknown_reason={reason_class}" not in determinism_text:
        fail(f"{target} catalog determinism_result does not record UNKNOWN reason class")


def validate_feedback_artifact(root: Path, result: dict[str, object]) -> None:
    target = str(result.get("target"))
    artifacts = result.get("artifacts")
    if not isinstance(artifacts, dict):
        fail(f"{target} feedback result has no artifacts map")
    for name in REQUIRED_FEEDBACK_ARTIFACTS:
        rel = artifacts.get(name)
        if not isinstance(rel, str) or not (root / rel).is_file():
            fail(f"{target} feedback result is missing artifact {name}")
    if "r0_z3" in result:
        rel = artifacts.get("schema_search_evidence.json")
        if not isinstance(rel, str) or not (root / rel).is_file():
            fail(f"{target} feedback result has r0_z3 but no schema-search evidence")
        smt2_files = artifacts.get("smt2_files")
        if not isinstance(smt2_files, list) or not smt2_files:
            fail(f"{target} feedback result has r0_z3 but no SMT evidence")
        for rel_smt in smt2_files:
            if not isinstance(rel_smt, str) or not (root / rel_smt).is_file():
                fail(f"{target} feedback result references missing SMT evidence")


def validate_feedback_determinism(root: Path, catalog: list[dict[str, str]]) -> None:
    generated = [
        row for row in catalog if row["status"] == "generated-new-real-relation-spec"
    ]
    manifest_path = root / FEEDBACK_DETERMINISM_MANIFEST
    if not manifest_path.is_file():
        fail(f"missing feedback determinism manifest {manifest_path}")
    manifest = json.loads(manifest_path.read_text())
    result_entries = manifest.get("results", [])
    if len(result_entries) != len(generated):
        fail(
            f"feedback manifest has {len(result_entries)} results, expected {len(generated)}"
        )
    manifest_targets = {entry.get("target") for entry in result_entries}
    generated_targets = {row["target"] for row in generated}
    if manifest_targets != generated_targets:
        fail(
            "feedback manifest targets differ from generated catalog targets: "
            f"missing={sorted(generated_targets - manifest_targets)} "
            f"extra={sorted(manifest_targets - generated_targets)}"
        )

    results: dict[str, dict[str, object]] = {}
    entries_by_target: dict[str, dict[str, object]] = {}
    for entry in result_entries:
        if not isinstance(entry, dict):
            fail("feedback manifest contains a non-object result entry")
        rel = entry.get("result_json")
        target = entry.get("target")
        if not isinstance(rel, str) or not (root / rel).is_file():
            fail(f"{target} manifest entry has missing result_json")
        payload = json.loads((root / rel).read_text())
        if payload.get("target") != target:
            fail(f"{target} manifest/result target mismatch")
        validate_feedback_artifact(root, payload)
        results[str(target)] = payload
        entries_by_target[str(target)] = entry

    for row in generated:
        text = row["determinism_result"]
        target = row["target"]
        if any(fragment in text for fragment in STALE_DIRECT_DETERMINISM_FRAGMENTS):
            fail(f"{target} still records stale direct assume-spec determinism evidence")
        result = results[target]
        result_json = result["artifacts"]["result.json"]  # checked above
        if result_json not in text:
            fail(f"{target} determinism_result does not reference its feedback result JSON")
        outcome = feedback_outcome(result)
        if f"R0={outcome}" not in text:
            fail(f"{target} determinism_result does not record outcome {outcome}")
        if result.get("status") == "ok" and f"r0_z3={result.get('r0_z3')}" not in text:
            fail(f"{target} determinism_result does not record r0_z3")
        validate_unknown_reason(
            target=target,
            entry=entries_by_target[target],
            result=result,
            determinism_text=text,
        )


def validate_generated_known_risks(rows: list[dict[str, str]], source: str) -> None:
    for row in rows:
        if row.get("status") != "generated-new-real-relation-spec":
            continue
        known_risks = str(row.get("known_risks", ""))
        stale_phrase = next(
            (phrase for phrase in STALE_KNOWN_RISKS_PHRASES if phrase in known_risks),
            None,
        )
        if stale_phrase is not None:
            fail(f"{row.get('target', '<unknown>')} {source} known_risks still records stale determinism unsupported wording")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate slice spec catalog artifacts.")
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--expect-total", required=True, type=int)
    parser.add_argument("--expect-existing-vstd", required=True, type=int)
    args = parser.parse_args()

    inventory = read_csv(args.inventory)
    catalog = read_csv(args.catalog)
    root = args.catalog.resolve().parents[1]

    if len(inventory) != args.expect_total:
        fail(f"inventory has {len(inventory)} rows, expected {args.expect_total}")
    if len(catalog) != args.expect_total:
        fail(f"catalog has {len(catalog)} rows, expected {args.expect_total}")

    missing = REQUIRED_COLUMNS.difference(catalog[0].keys())
    if missing:
        fail(f"catalog missing columns: {sorted(missing)}")

    inventory_targets = {row["canonical_target"] for row in inventory}
    catalog_targets = [row["target"] for row in catalog]
    if len(set(catalog_targets)) != len(catalog_targets):
        duplicates = sorted({target for target in catalog_targets if catalog_targets.count(target) > 1})
        fail(f"duplicate catalog targets: {duplicates}")
    if set(catalog_targets) != inventory_targets:
        fail(
            "catalog target set differs from inventory: "
            f"missing={sorted(inventory_targets - set(catalog_targets))} "
            f"extra={sorted(set(catalog_targets) - inventory_targets)}"
        )

    existing_rows = {row["target"] for row in catalog if row["status"] == "existing-vstd"}
    if len(existing_rows) != args.expect_existing_vstd:
        fail(f"catalog has {len(existing_rows)} existing-vstd rows, expected {args.expect_existing_vstd}")
    if existing_rows != EXISTING_VSTD:
        fail(
            "existing-vstd catalog set mismatch: "
            f"missing={sorted(EXISTING_VSTD - existing_rows)} "
            f"extra={sorted(existing_rows - EXISTING_VSTD)}"
        )

    for row in catalog:
        target = row["target"]
        for column in REQUIRED_COLUMNS:
            if not row.get(column, "").strip():
                fail(f"{target} has empty required column {column}")
        if row["status"] not in {"existing-vstd", "generated-new-real-relation-spec", "justified-no-spec"}:
            fail(f"{target} has unexpected status {row['status']}")
        if row["status"] == "generated-new-real-relation-spec":
            records_static_shape_check = "static-contract-shape-check" in row["typecheck_result"]
            if (
                not records_static_shape_check
                and not records_bootstrap_verus_typecheck(row, root)
                and not records_mutation_verus_typecheck(row, root)
                and not records_remaining_verus_typecheck(row, root)
            ):
                fail(f"{target} records neither static contract-shape nor known Verus typecheck evidence")
        if row["status"] == "justified-no-spec":
            required_words = ("strongest weak spec", "missing", "prerequisite", "operator")
            text = " ".join(row[column] for column in REQUIRED_COLUMNS).lower()
            absent = [word for word in required_words if word not in text]
            if absent:
                fail(f"{target} no-spec justification is incomplete; missing words {absent}")

    validate_generated_known_risks(catalog, "CSV catalog")
    validate_feedback_determinism(root, catalog)

    json_path = args.catalog.with_suffix(".json")
    review_path = args.catalog.with_name("SLICE_SPEC_REVIEW.md")
    if not json_path.is_file():
        fail(f"missing JSON catalog {json_path}")
    if not review_path.is_file():
        fail(f"missing review document {review_path}")
    payload = json.loads(json_path.read_text())
    json_rows = payload.get("rows", [])
    if len(json_rows) != len(catalog) or {row.get("target") for row in json_rows} != set(catalog_targets):
        fail("JSON catalog rows do not match CSV catalog")
    validate_generated_known_risks(json_rows, "JSON catalog")
    summary = payload.get("summary", {})
    if summary.get("total") != args.expect_total:
        fail("JSON summary total does not match expected total")
    if summary.get("existing_vstd") != args.expect_existing_vstd:
        fail("JSON summary existing-vstd count does not match expected count")
    if summary.get("generated_new_real_relation_specs") + summary.get("justified_no_spec", 0) != (
        args.expect_total - args.expect_existing_vstd
    ):
        fail("JSON generated/justified count does not cover non-vstd rows")

    print(
        "catalog ok: "
        f"{args.expect_total} rows, "
        f"{args.expect_existing_vstd} existing-vstd, "
        f"{args.expect_total - args.expect_existing_vstd} generated/justified"
    )


if __name__ == "__main__":
    main()
