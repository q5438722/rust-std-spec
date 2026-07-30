#!/usr/bin/env python3
"""Classify stable uncovered Rust APIs before launching spec generation."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
from typing import Any


REPRESENTATION_METHODS = {
    "allocator",
    "as_mut_ptr",
    "as_non_null",
    "as_ptr",
    "capacity",
    "const_make_global",
    "dangling_ptr",
    "from_parts",
    "from_parts_in",
    "from_raw",
    "from_raw_parts",
    "from_raw_parts_in",
    "into_parts",
    "into_parts_with_alloc",
    "into_raw",
    "into_raw_parts",
    "into_raw_parts_with_alloc",
    "leak",
    "new_in",
    "reserve",
    "reserve_exact",
    "shrink_to",
    "shrink_to_fit",
    "set_len",
    "spare_capacity_mut",
    "try_with_capacity",
    "try_with_capacity_in",
    "try_reserve",
    "try_reserve_exact",
    "hasher",
    "with_hasher",
    "with_capacity_and_hasher",
    "with_capacity",
    "with_capacity_in",
}

COMPLEX_ITERATOR_METHODS = {
    "array_windows",
    "bytes",
    "char_indices",
    "chunks",
    "chunks_exact",
    "chunks_exact_mut",
    "chunks_mut",
    "difference",
    "drain",
    "encode_utf16",
    "entry",
    "escape_ascii",
    "escape_debug",
    "escape_default",
    "escape_unicode",
    "extract_if",
    "intersection",
    "into_keys",
    "into_values",
    "iter",
    "iter_mut",
    "lines",
    "lines_any",
    "match_indices",
    "matches",
    "range",
    "range_mut",
    "rchunks",
    "rchunks_exact",
    "rchunks_exact_mut",
    "rchunks_mut",
    "retain",
    "retain_mut",
    "split",
    "split_ascii_whitespace",
    "split_inclusive",
    "split_terminator",
    "split_whitespace",
    "splitn",
    "splice",
    "symmetric_difference",
    "union",
    "utf8_chunks",
    "values_mut",
    "windows",
}

OWNERSHIP_MODEL_PREFIXES = (
    "alloc::boxed::Box::",
    "alloc::rc::Rc::",
    "alloc::sync::Arc::",
    "core::mem::MaybeUninit::",
)

COMPLEX_RESULT_METHODS = {
    "first_entry",
    "get_disjoint_mut",
    "into_boxed_str",
    "last_entry",
    "select_nth_unstable",
    "sort_unstable",
}

FALLIBLE_STRING_CONSTRUCTORS = {
    "from_utf16",
    "from_utf16_lossy",
    "from_utf16be",
    "from_utf16be_lossy",
    "from_utf16le",
    "from_utf16le_lossy",
    "from_utf8",
    "from_utf8_lossy",
}

STR_PATTERN_METHODS = {
    "contains",
    "find",
    "split_once",
    "starts_with",
    "strip_prefix",
    "strip_suffix",
    "trim_left_matches",
    "trim_start_matches",
}


def json_contains(value: Any, predicate) -> bool:
    if isinstance(value, dict):
        return any(
            predicate(key, item) or json_contains(item, predicate)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return any(json_contains(item, predicate) for item in value)
    return predicate("", value)


def signature_flags(target: dict[str, Any]) -> dict[str, bool]:
    declarations = target.get("verification_declarations") or []
    payload = [
        {
            "signature": declaration.get("signature"),
            "generics": declaration.get("generics"),
            "owner": declaration.get("owner"),
        }
        for declaration in declarations
    ]
    has_closure = json_contains(
        payload,
        lambda key, value: (
            isinstance(value, str)
            and re.search(r"\bFn(?:Mut|Once)?\b", value) is not None
        ),
    )
    has_raw_pointer = json_contains(
        payload,
        lambda key, value: key == "raw_pointer",
    )
    has_qualified_projection = json_contains(
        payload,
        lambda key, value: key == "qualified_path",
    )
    has_unsafe = any(
        declaration.get("header", {}).get("is_unsafe")
        for declaration in declarations
    )
    has_mutable_output_state = any(
        declaration.get("observability", {}).get("mutable_inputs")
        for declaration in declarations
    )
    has_observable_output = any(
        declaration.get("observability", {}).get("has_modeled_output")
        for declaration in declarations
    )
    returns_reference = any(
        declaration.get("observability", {}).get("return_is_reference")
        for declaration in declarations
    )
    returns_mutable_reference = any(
        declaration.get("observability", {}).get(
            "return_reference_is_mutable"
        )
        for declaration in declarations
    )
    return_is_raw_pointer = any(
        declaration.get("observability", {}).get("return_is_raw_pointer")
        for declaration in declarations
    )
    return {
        "has_closure": has_closure,
        "has_raw_pointer": has_raw_pointer,
        "has_qualified_projection": has_qualified_projection,
        "has_unsafe": has_unsafe,
        "has_mutable_output_state": has_mutable_output_state,
        "has_observable_output": has_observable_output,
        "returns_reference": returns_reference,
        "returns_mutable_reference": returns_mutable_reference,
        "return_is_raw_pointer": return_is_raw_pointer,
    }


def owner_prefix(target: str) -> str:
    return target.rsplit("::", 1)[0]


def classify(
    target: dict[str, Any],
    contracts: list[dict[str, Any]],
) -> tuple[str, list[str], dict[str, bool], int]:
    path = target["target"]
    owner = owner_prefix(path)
    method = path.rsplit("::", 1)[-1]
    flags = signature_flags(target)
    related_contracts = sum(
        contract["api_path"].startswith(owner + "::")
        for contract in contracts
    )
    reasons: list[str] = []

    if not target.get("available_in_verus_rust_1_96"):
        return "toolchain_unavailable", ["not_in_verus_rust_1_96"], flags, 0

    if "trait_method" in target.get("kinds", []):
        return (
            "trait_contract_integration",
            ["requires_external_trait_specification_edit"],
            flags,
            related_contracts,
        )

    category = target["category"]
    if category == "io_os_runtime":
        return (
            "runtime_or_hidden_state",
            ["external_or_hidden_runtime_state"],
            flags,
            related_contracts,
        )
    if category == "formatting":
        return (
            "formatting_effect",
            ["formatting_state_not_modeled"],
            flags,
            related_contracts,
        )
    if category == "atomic":
        return (
            "concurrency_or_hidden_state",
            ["atomic_state_not_exposed_by_ordinary_view"],
            flags,
            related_contracts,
        )

    if flags["returns_mutable_reference"]:
        return (
            "determinism_checker_unsupported",
            ["mutable_reference_return_not_supported"],
            flags,
            related_contracts,
        )

    if flags["has_unsafe"] or flags["has_raw_pointer"]:
        reasons.append("unsafe_or_raw_pointer_signature")
    if flags["return_is_raw_pointer"]:
        reasons.append("raw_pointer_result")
    if len(target.get("verification_declarations") or []) > 1:
        reasons.append("multiple_rust_declarations_share_path")
    if reasons:
        return "unsafe_or_representation_sensitive", reasons, flags, related_contracts

    if path.startswith(OWNERSHIP_MODEL_PREFIXES):
        return (
            "ownership_or_uninitialized_model",
            ["requires_linear_ownership_or_initialization_model"],
            flags,
            related_contracts,
        )

    if method in REPRESENTATION_METHODS or method == "fn_addr_eq":
        return (
            "representation_or_allocator",
            ["representation_or_allocator_state_not_in_public_view"],
            flags,
            related_contracts,
        )

    if method in COMPLEX_ITERATOR_METHODS or path.startswith("core::iter::"):
        return (
            "iterator_or_adapter_result",
            ["iterator_or_adapter_semantics_require_prophetic_model"],
            flags,
            related_contracts,
        )

    if (
        method in COMPLEX_RESULT_METHODS
        or (
            path.startswith("alloc::string::String::")
            and method in FALLIBLE_STRING_CONSTRUCTORS
        )
        or (
            path.startswith("core::option::Option::")
            and method in {"as_pin_mut", "as_pin_ref"}
        )
        or (
            path.startswith("core::str::")
            and method in STR_PATTERN_METHODS
        )
    ):
        return (
            "complex_result_or_pattern_model",
            ["result_type_or_pattern_semantics_need_additional_model"],
            flags,
            related_contracts,
        )

    if not flags["has_observable_output"]:
        return (
            "no_modeled_observable_output",
            ["unit_result_without_mutable_output_state"],
            flags,
            related_contracts,
        )

    if flags["has_closure"]:
        return (
            "higher_order_contract",
            ["closure_call_ensures_or_prophetic_model_required"],
            flags,
            related_contracts,
        )

    if flags["has_qualified_projection"]:
        return (
            "associated_type_or_projection",
            ["associated_type_signature_requires_manual_integration"],
            flags,
            related_contracts,
        )

    if related_contracts == 0:
        return (
            "needs_new_vstd_abstraction",
            ["no_existing_contract_for_owner_or_module"],
            flags,
            related_contracts,
        )

    if flags["returns_reference"]:
        reasons.append("must_compare_semantic_view_not_reference_identity")

    return "suitable_now", reasons, flags, related_contracts


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    rows: list[dict[str, Any]],
    suitable: list[dict[str, Any]],
) -> None:
    counts = Counter(row["classification"] for row in rows)
    category_counts = Counter(row["category"] for row in suitable)
    owner_counts = Counter(row["owner"] for row in suitable)
    lines = [
        "# Classification of 2,121 stable uncovered Rust APIs",
        "",
        "## Summary",
        "",
        "| Classification | Count |",
        "|---|---:|",
    ]
    for name, count in counts.most_common():
        lines.append(f"| `{name}` | {count} |")
    lines.extend(
        [
            "",
            f"First-run generation targets: **{len(suitable)}**.",
            "",
            "## Suitable-now targets by category",
            "",
            "| Category | Count |",
            "|---|---:|",
        ]
    )
    for name, count in category_counts.most_common():
        lines.append(f"| `{name}` | {count} |")
    lines.extend(
        [
            "",
            "## Largest suitable owner groups",
            "",
            "| Owner/module | Count |",
            "|---|---:|",
        ]
    )
    for owner, count in owner_counts.most_common(40):
        lines.append(f"| `{owner}` | {count} |")
    lines.extend(
        [
            "",
            "## First-run target list",
            "",
            "| Target | Category | Notes |",
            "|---|---|---|",
        ]
    )
    for row in suitable:
        lines.append(
            f"| `{row['target']}` | {row['category']} | "
            f"{row['classification_reasons']} |"
        )
    path.write_text("\n".join(lines).rstrip() + "\n")


def pilot_bucket(target: dict[str, Any]) -> str:
    flags = target["signature_flags"]
    if flags["returns_reference"] and flags["has_mutable_output_state"]:
        return "reference_and_mutation"
    if flags["returns_reference"]:
        return "reference_output"
    if flags["has_mutable_output_state"]:
        return "mutable_post_state"
    return "value_output"


def select_pilot(
    suitable: list[dict[str, Any]],
    size: int,
) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = {}
    for target in suitable:
        buckets.setdefault(pilot_bucket(target), []).append(target)
    selected: list[dict[str, Any]] = []
    quota = max(1, (size + len(buckets) - 1) // len(buckets))
    for bucket in sorted(buckets):
        choices = sorted(
            buckets[bucket],
            key=lambda target: (
                target["target"].rsplit("::", 1)[0],
                target["target"],
            ),
        )
        seen_owners: set[str] = set()
        bucket_selected: list[dict[str, Any]] = []
        for target in choices:
            owner = target["target"].rsplit("::", 1)[0]
            if owner in seen_owners:
                continue
            seen_owners.add(owner)
            bucket_selected.append(target)
            if len(bucket_selected) >= quota:
                break
        if len(bucket_selected) < quota:
            selected_targets = {item["target"] for item in bucket_selected}
            for target in choices:
                if target["target"] in selected_targets:
                    continue
                bucket_selected.append(target)
                if len(bucket_selected) >= quota:
                    break
        selected.extend(bucket_selected)
    if len(selected) < size:
        selected_paths = {target["target"] for target in selected}
        for target in sorted(suitable, key=lambda item: item["target"]):
            if target["target"] in selected_paths:
                continue
            selected.append(target)
            if len(selected) >= size:
                break
    return selected[:size]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument(
        "--manifest",
        type=Path,
        default=workspace / "specgen" / "stable-uncovered-manifest.json",
    )
    parser.add_argument(
        "--contracts",
        type=Path,
        default=workspace / "results" / "vstd_contracts.json",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=workspace / "specgen",
    )
    parser.add_argument("--pilot-size", type=int, default=32)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = json.loads(args.manifest.read_text())
    contracts = json.loads(args.contracts.read_text())
    classified_targets = []
    csv_rows = []
    for target in manifest["targets"]:
        name, reasons, flags, related_contracts = classify(target, contracts)
        enriched = dict(target)
        enriched.update(
            {
                "classification": name,
                "classification_reasons": reasons,
                "signature_flags": flags,
                "related_vstd_contract_count": related_contracts,
            }
        )
        classified_targets.append(enriched)
        csv_rows.append(
            {
                "target": target["target"],
                "classification": name,
                "category": target["category"],
                "owner": owner_prefix(target["target"]),
                "kinds": ";".join(target["kinds"]),
                "classification_reasons": ";".join(reasons),
                "related_vstd_contract_count": related_contracts,
                "returns_reference": flags["returns_reference"],
                "returns_mutable_reference": flags["returns_mutable_reference"],
                "has_mutable_output_state": flags["has_mutable_output_state"],
                "has_closure": flags["has_closure"],
                "has_unsafe": flags["has_unsafe"],
                "has_raw_pointer": flags["has_raw_pointer"],
            }
        )

    suitable = [
        target
        for target in classified_targets
        if target["classification"] == "suitable_now"
    ]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "target_count": len(classified_targets),
            "suitable_count": len(suitable),
            "classification_counts": dict(
                sorted(Counter(
                    target["classification"] for target in classified_targets
                ).items())
            ),
        },
        "targets": classified_targets,
    }
    (args.out_dir / "classified-manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    suitable_payload = {
        "metadata": {
            "target_count": len(suitable),
            "source_target_count": len(classified_targets),
            "selection": "classification == suitable_now",
        },
        "targets": suitable,
    }
    (args.out_dir / "suitable-manifest.json").write_text(
        json.dumps(suitable_payload, indent=2, sort_keys=True) + "\n"
    )
    pilot = select_pilot(suitable, args.pilot_size)
    (args.out_dir / "suitable-pilot-manifest.json").write_text(
        json.dumps(
            {
                "metadata": {
                    "target_count": len(pilot),
                    "source_suitable_count": len(suitable),
                    "selection": "signature-shape and owner-stratified",
                    "bucket_counts": dict(
                        Counter(pilot_bucket(target) for target in pilot)
                    ),
                },
                "targets": pilot,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    pilot_paths = {target["target"] for target in pilot}
    remaining = [
        target for target in suitable if target["target"] not in pilot_paths
    ]
    (args.out_dir / "suitable-remaining-manifest.json").write_text(
        json.dumps(
            {
                "metadata": {
                    "target_count": len(remaining),
                    "source_suitable_count": len(suitable),
                    "excluded_pilot_count": len(pilot),
                    "selection": "suitable targets not in suitable-pilot-manifest",
                },
                "targets": remaining,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    write_csv(args.out_dir / "classification.csv", csv_rows)
    write_report(
        args.out_dir / "CLASSIFICATION.md",
        csv_rows,
        [
            {
                **row,
                "classification_reasons": row["classification_reasons"] or "-",
            }
            for row in csv_rows
            if row["classification"] == "suitable_now"
        ],
    )
    print(
        f"classified {len(classified_targets)} targets; "
        f"{len(suitable)} are suitable for the first run"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
