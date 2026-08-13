#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path


EXPECTED_CONTRACTS = [
    "<[T]>::split_first",
    "<[T]>::split_off_first",
    "<[T]>::split_last",
    "<[T]>::split_off_last",
    "<[T]>::split_first_mut",
    "<[T]>::split_last_mut",
    "<[T]>::chunks_exact",
    "<[T]>::rchunks_exact",
    "<[u8]>::trim_ascii_start",
    "<[u8]>::trim_ascii_end",
    "<[u8]>::make_ascii_lowercase",
    "<[u8]>::make_ascii_uppercase",
    "<[T]>::split_off_first_mut",
    "<[T]>::split_off_last_mut",
    "core::slice::ChunksExact::<'a,T>::remainder",
    "core::slice::RChunksExact::<'a,T>::remainder",
]

HELPERS = [
    "SliceIteratorView",
    "slice_iterator_view",
    "slice_iterator_well_formed",
    "axiom_slice_iterator_view_well_formed",
    "slice_chunk_partition",
    "slice_split_off_first_result",
    "slice_split_off_last_result",
    "ascii_is_uppercase",
    "ascii_is_lowercase",
    "ascii_lower_byte",
    "ascii_upper_byte",
    "ascii_is_whitespace",
    "ascii_lower_seq",
    "ascii_upper_seq",
    "ascii_trim_start_boundary",
    "ascii_trim_end_boundary",
    "ascii_trim_start_index",
    "ascii_trim_end_index",
    "ascii_trim_start_result",
    "ascii_trim_end_result",
]


def canonical(text: str) -> str:
    return re.sub(r"\s+", "", text)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contracts(path: Path) -> dict[str, str]:
    text = path.read_text()
    blocks = re.findall(
        r"^pub assume_specification.*?^\s*;\s*$",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    result = {}
    for block in blocks:
        match = re.search(r"\[\s*(.*?)\s*\]\s*\(", block, flags=re.DOTALL)
        if not match:
            raise RuntimeError(f"cannot identify contract in {path}: {block[:80]}")
        key = canonical(match.group(1))
        if key in result:
            raise RuntimeError(f"duplicate contract key {key} in {path}")
        result[key] = canonical(block)
    return result


def helper_item(path: Path, name: str) -> str:
    text = path.read_text()
    match = re.search(
        rf"^pub\s+(?:ghost\s+struct|uninterp\s+spec\s+fn|open\s+spec\s+fn|"
        rf"broadcast\s+axiom\s+fn)\s+{re.escape(name)}\b",
        text,
        flags=re.MULTILINE,
    )
    if not match:
        raise RuntimeError(f"cannot find helper {name} in {path}")

    start = match.start()
    brace = text.find("{", match.end())
    semicolon = text.find(";", match.end())
    if semicolon != -1 and (brace == -1 or semicolon < brace):
        return canonical(text[start : semicolon + 1])

    depth = 0
    for index in range(brace, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return canonical(text[start : index + 1])
    raise RuntimeError(f"unterminated helper {name} in {path}")


def main() -> int:
    bundle_root = Path(__file__).resolve().parents[1]
    repository_root = Path(__file__).resolve().parents[4]
    active_root = (
        repository_root
        / "nanvix-rust-std-slice-specgen-2026-08-11"
        / "specs"
    )
    subset_root = bundle_root / "specs"

    active_contracts_path = active_root / "generated_slice_specs.rs"
    subset_contracts_path = subset_root / "generated_slice_specs.rs"
    active_helpers_path = active_root / "slice_shared_vocabulary.rs"
    subset_helpers_path = subset_root / "slice_shared_vocabulary.rs"

    expected = [canonical(key) for key in EXPECTED_CONTRACTS]
    active_contracts = contracts(active_contracts_path)
    subset_contracts = contracts(subset_contracts_path)
    missing = sorted(set(expected) - set(subset_contracts))
    extra = sorted(set(subset_contracts) - set(expected))
    contract_mismatches = sorted(
        key
        for key in expected
        if key in subset_contracts and active_contracts.get(key) != subset_contracts[key]
    )
    helper_mismatches = sorted(
        name
        for name in HELPERS
        if helper_item(active_helpers_path, name)
        != helper_item(subset_helpers_path, name)
    )

    subset_helpers = subset_helpers_path.read_text()
    external_types_ok = all(
        re.search(
            rf"#\[verifier::external_type_specification\]\s*"
            rf"#\[verifier::external_body\]\s*"
            rf"#\[verifier::reject_recursive_types\(T\)\]\s*"
            rf"pub struct {name}\b",
            subset_helpers,
        )
        for name in ("ExChunksExact", "ExRChunksExact")
    )
    passed = not (
        missing
        or extra
        or contract_mismatches
        or helper_mismatches
        or not external_types_ok
    )

    print(
        json.dumps(
            {
                "result": "pass" if passed else "fail",
                "comparison": "whitespace-normalized exact item comparison",
                "active_generated_specs": str(active_contracts_path),
                "active_generated_specs_sha256": sha256(active_contracts_path),
                "active_shared_vocabulary": str(active_helpers_path),
                "active_shared_vocabulary_sha256": sha256(active_helpers_path),
                "selected_contract_count": len(subset_contracts),
                "selected_helper_count": len(HELPERS),
                "missing_contracts": missing,
                "extra_contracts": extra,
                "contract_mismatches": contract_mismatches,
                "helper_mismatches": helper_mismatches,
                "external_type_specs_present": external_types_ok,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
