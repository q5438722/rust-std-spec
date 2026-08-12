#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TOTAL = 49
EXPECTED_EXISTING = 24
EXPECTED_GENERATED = 24
EXPECTED_JUSTIFIED = 1
CATALOG_COLUMNS = {'status', 'source_excerpt', 'source_reference', 'determinism_result', 'generic_bounds_result', 'reviewer_notes', 'target', 'known_risks', 'requires', 'semantic_family', 'contract_text', 'ensures', 'typecheck_result', 'strength', 'target_binding_result', 'signature_shape_result', 'shared_helpers'}
EXISTING = {'alloc::vec::Vec::shrink_to', 'alloc::vec::Vec::as_mut_slice', 'alloc::vec::Vec::reserve_exact', 'alloc::vec::Vec::truncate', 'alloc::vec::Vec::swap_remove', 'alloc::vec::Vec::resize', 'alloc::vec::Vec::append', 'alloc::vec::Vec::push', 'alloc::vec::Vec::try_reserve_exact', 'alloc::vec::Vec::capacity', 'alloc::vec::Vec::split_off', 'alloc::vec::Vec::reserve', 'alloc::vec::Vec::with_capacity', 'alloc::vec::Vec::shrink_to_fit', 'alloc::vec::Vec::pop', 'alloc::vec::Vec::extend_from_slice', 'alloc::vec::Vec::is_empty', 'alloc::vec::Vec::remove', 'alloc::vec::Vec::len', 'alloc::vec::Vec::try_reserve', 'alloc::vec::Vec::new', 'alloc::vec::Vec::as_slice', 'alloc::vec::Vec::clear', 'alloc::vec::Vec::insert'}
GENERATED = {'alloc::vec::IntoIter::as_slice', 'alloc::vec::Vec::extract_if', 'alloc::vec::Vec::from_raw_parts', 'alloc::vec::Vec::resize_with', 'alloc::vec::Vec::leak', 'alloc::vec::Vec::retain_mut', 'alloc::vec::IntoIter::as_mut_slice', 'alloc::vec::Vec::into_boxed_slice', 'alloc::vec::Vec::extend_from_within', 'alloc::vec::Vec::set_len', 'alloc::vec::Vec::dedup_by', 'alloc::vec::Vec::into_raw_parts', 'alloc::vec::Vec::dedup', 'alloc::vec::Vec::drain', 'alloc::vec::Vec::as_mut_ptr', 'alloc::vec::Vec::spare_capacity_mut', 'alloc::vec::Vec::push_mut', 'alloc::vec::Vec::dedup_by_key', 'alloc::vec::Drain::as_slice', 'alloc::vec::Vec::as_ptr', 'alloc::vec::Vec::retain', 'alloc::vec::Vec::into_flattened', 'alloc::vec::Vec::pop_if', 'alloc::vec::Vec::insert_mut'}
NO_SPEC = {'alloc::vec::Vec::splice'}
SHARED_HELPER_CLASS = {'spec_vec_len': 'law-constrained', 'CapacitySpec::spec_capacity': 'irreducible-boundary', 'vec_start_ptr': 'irreducible-boundary', 'vec_start_mut_ptr': 'irreducible-boundary', 'vec_raw_parts_domain': 'irreducible-boundary', 'vec_raw_parts_initialized_seq': 'irreducible-boundary', 'vec_raw_parts_round_trip': 'irreducible-boundary', 'vec_raw_parts_storage_ptr': 'irreducible-boundary', 'vec_set_len_domain': 'irreducible-boundary', 'vec_set_len_result': 'irreducible-boundary', 'vec_spare_capacity_relation': 'irreducible-boundary', 'vec_drain_remaining': 'law-constrained', 'vec_drain_created': 'law-constrained', 'vec_into_iter_remaining': 'law-constrained', 'vec_into_iter_remaining_mut': 'law-constrained', 'vec_extract_if_created': 'law-constrained', 'vec_range_bounds_valid': 'law-constrained', 'vec_range_start': 'law-constrained', 'vec_range_end': 'law-constrained', 'vec_extend_from_within_result': 'source-backed', 'flatten_array_vec': 'source-backed', 'array_value_view': 'law-constrained', 'boxed_slice_view': 'irreducible-boundary', 'boxed_slice_capacity': 'irreducible-boundary', 'vec_dedup_partial_eq_result': 'law-constrained', 'vec_dedup_by_result': 'law-constrained', 'vec_dedup_by_key_result': 'law-constrained', 'vec_pop_if_result': 'law-constrained', 'vec_resize_with_result': 'law-constrained', 'vec_retain_result': 'law-constrained', 'vec_retain_mut_result': 'law-constrained'}
REQUIRED_FEEDBACK_ARTIFACTS = (
    "candidate.json",
    "active_contract_code.rs",
    "synthetic_spec.rs",
    "__rust_std_candidate.rs",
    "det_spec.json",
    "det_harness.rs",
    "det_stdout.txt",
    "det_stderr.txt",
    "verus_stdout.txt",
    "verus_stderr.txt",
    "schema_search_evidence.json",
    "result.json",
)

def fail(message: str) -> None:
    print(f"{Path(__file__).name} failed: {message}", file=sys.stderr)
    raise SystemExit(1)

def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing CSV {path}")
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        fail(f"{path} is empty")
    return rows

def read_json(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing JSON {path}")
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        fail(f"{path} must contain a JSON object")
    return payload

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def catalog_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "catalog" / "vec_spec_catalog.csv")

def inventory_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "inventory" / "vec_exec_fn_inventory.csv")

def parse_markers(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text()
    pattern = re.compile(r"// BEGIN VEC_SPEC target=(?P<target>\S+)\n(?P<body>.*?)// END VEC_SPEC", re.DOTALL)
    blocks: dict[str, dict[str, str]] = {}
    for match in pattern.finditer(text):
        target = match.group("target")
        fields: dict[str, str] = {}
        for line in match.group("body").splitlines():
            if line.startswith("// ") and ": " in line:
                key, value = line[3:].split(": ", 1)
                fields[key.strip()] = value.strip()
        blocks[target] = fields
    return blocks

def generated_manifest(required: bool = True) -> dict | None:
    path = ROOT / "verification" / "evidence" / "vec_feedback_determinism" / "latest_manifest.json"
    if not path.is_file():
        if required:
            fail(f"missing feedback manifest {path}")
        return None
    return read_json(path)

REQUIRED_ARTIFACTS = (
    "inventory/VEC_EXEC_FN_INVENTORY.md",
    "inventory/vec_exec_fn_inventory.csv",
    "inventory/vec_exec_fn_inventory.json",
    "inventory/vec_existing_vstd_exact_match_audit.csv",
    "inventory/vec_existing_vstd_exact_match_audit.json",
    "inventory/vec_unstable_exclusions.csv",
    "inventory/vec_unstable_exclusions.json",
    "specs/vec_shared_vocabulary.rs",
    "specs/existing_vstd_vec_specs.rs",
    "specs/generated_vec_specs.rs",
    "specs/all_vec_specs.rs",
    "catalog/vec_spec_catalog.csv",
    "catalog/vec_spec_catalog.json",
    "catalog/VEC_SPEC_REVIEW.md",
    "catalog/vec_old_30_subset_comparison.csv",
    "catalog/vec_old_30_subset_comparison.json",
    "catalog/vec_justified_no_spec_records.csv",
    "catalog/vec_justified_no_spec_records.json",
    "provenance/source_manifest.csv",
    "provenance/source_manifest.json",
    "verification/shared_helper_target_usage_audit.csv",
    "verification/shared_helper_target_usage_audit.json",
    "verification/harnesses/vec_all_contracts_batch.rs",
    "verification/evidence/vec_all_contracts_batch.verus.json",
    "verification/check_inventory.py",
    "verification/check_provenance.py",
    "verification/check_catalog.py",
    "verification/check_contracts.py",
    "verification/check_artifact_integrity.py",
    "verification/run_vec_assume_spec_feedback_determinism.py",
)

def run_check(args: list[str]) -> dict:
    completed = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        fail("check failed: " + " ".join(args) + "\nstdout:\n" + completed.stdout + "\nstderr:\n" + completed.stderr)
    return {"command": " ".join([sys.executable, *args]), "stdout": completed.stdout.strip(), "stderr": completed.stderr.strip(), "exit_code": completed.returncode}

def main() -> None:
    for rel in REQUIRED_ARTIFACTS:
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing required artifact {rel}")
    if not (ROOT / "rust-alloc-vec").is_dir() or not (ROOT / "vstd-baseline").is_dir():
        fail("missing copied source or vstd baseline directories")
    manifest = generated_manifest(required=True)
    run_root = ROOT / str(manifest.get("run_root", ""))
    if not run_root.is_dir():
        fail("manifest run_root missing")
    entries = manifest.get("results")
    if not isinstance(entries, list) or len(entries) != EXPECTED_GENERATED:
        fail("determinism result entry count mismatch")
    for entry in entries:
        target = entry.get("target")
        if target not in GENERATED:
            fail(f"unexpected determinism target {target}")
        result_rel = entry.get("result_json")
        if not isinstance(result_rel, str):
            fail(f"{target} missing result_json")
        target_dir = (ROOT / result_rel).parent
        for name in REQUIRED_FEEDBACK_ARTIFACTS:
            if not (target_dir / name).is_file():
                fail(f"{target} missing feedback artifact {name}")
        payload = read_json(ROOT / result_rel)
        if payload.get("target") != target:
            fail(f"{target} result target mismatch")
        if payload.get("status") not in {"ok", "unsupported", "verus_error", "runner_crash", "no_ensures", "unsupported_mut_ref_return"}:
            fail(f"{target} has unknown feedback status {payload.get('status')}")
    checks = {
        "inventory": run_check(["verification/check_inventory.py", "--modules-csv", "results/modules.csv", "--inventory", "inventory/vec_exec_fn_inventory.csv", "--expect-total", "49", "--expect-existing-vstd", "24", "--expect-unstable", "28"]),
        "provenance": run_check(["verification/check_provenance.py"]),
        "catalog": run_check(["verification/check_catalog.py"]),
        "contracts": run_check(["verification/check_contracts.py"]),
    }
    evidence = {
        "schema_version": 1,
        "required_artifacts": list(REQUIRED_ARTIFACTS),
        "determinism_manifest": "verification/evidence/vec_feedback_determinism/latest_manifest.json",
        "determinism_status_counts": manifest.get("status_counts"),
        "determinism_r0_z3_counts": manifest.get("r0_z3_counts"),
        "checks": checks,
    }
    write_path = ROOT / "verification" / "artifact_integrity_evidence.json"
    write_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    rows = [{"gate": key, "exit_code": str(value["exit_code"]), "stdout": value["stdout"]} for key, value in checks.items()]
    with (ROOT / "verification" / "artifact_integrity_evidence.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["gate", "exit_code", "stdout"])
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "verification" / "ARTIFACT_INTEGRITY_EVIDENCE.md").write_text("# Vec Artifact Integrity Evidence\n\nAll Vec module-first gates passed.\n")
    print("artifact integrity ok: required artifacts, feedback evidence, and nested gates passed")

if __name__ == "__main__":
    main()
