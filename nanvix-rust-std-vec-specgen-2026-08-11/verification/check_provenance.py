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

def main() -> None:
    manifest = read_csv(ROOT / "provenance" / "source_manifest.csv")
    for row in manifest:
        dest = ROOT / row["dest_path"]
        if not dest.is_file() or dest.is_symlink():
            fail(f"bad manifest destination {dest}")
        if sha256(dest) != row["sha256"]:
            fail(f"hash mismatch for {dest}")
    payload = read_json(ROOT / "provenance" / "source_manifest.json")
    if len(payload.get("files", [])) != len(manifest):
        fail("manifest JSON count mismatch")
    print(f"provenance ok: {len(manifest)} copied input files verified")

if __name__ == "__main__":
    main()
