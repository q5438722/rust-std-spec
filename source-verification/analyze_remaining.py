#!/usr/bin/env python3
"""Classify newly covered stable APIs that lack a source-verification harness."""

from __future__ import annotations

from collections import defaultdict
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def add(targets: set[str], owner: str, names: list[str]) -> None:
    targets.update(f"{owner}::{name}" for name in names)


def verified_new_stable_targets() -> set[str]:
    targets: set[str] = set()
    add(
        targets,
        "core::cmp::Ordering",
        ["is_eq", "is_ne", "is_lt", "is_gt", "is_le", "is_ge", "reverse", "then"],
    )
    add(
        targets,
        "core::ops::ControlFlow",
        ["is_break", "is_continue", "break_value", "continue_value", "break_ok", "continue_ok"],
    )
    add(
        targets,
        "alloc::collections::VecDeque",
        ["swap_remove_front", "swap_remove_back", "is_empty", "front", "back"],
    )
    add(targets, "alloc::collections::BinaryHeap", ["is_empty", "with_capacity"])
    add(targets, "alloc::collections::LinkedList", ["is_empty"])
    add(targets, "alloc::string::String", ["with_capacity"])
    add(
        targets,
        "core::net::Ipv4Addr",
        [
            "is_loopback",
            "is_unspecified",
            "is_private",
            "is_link_local",
            "is_multicast",
            "is_documentation",
            "is_broadcast",
            "to_ipv6_compatible",
            "to_ipv6_mapped",
        ],
    )
    add(
        targets,
        "core::net::Ipv6Addr",
        [
            "to_ipv4_mapped",
            "is_unspecified",
            "is_loopback",
            "is_multicast",
            "is_unique_local",
            "is_unicast_link_local",
            "to_canonical",
        ],
    )
    add(
        targets,
        "core::net::IpAddr",
        ["is_ipv4", "is_ipv6", "is_unspecified", "is_loopback", "is_multicast", "to_canonical"],
    )
    add(
        targets,
        "core::net::SocketAddr",
        ["new", "ip", "port", "is_ipv4", "is_ipv6", "set_port", "set_ip"],
    )
    add(targets, "core::ffi::CStr", ["count_bytes", "is_empty"])
    add(targets, "alloc::ffi::CString", ["as_bytes", "as_bytes_with_nul"])
    add(
        targets,
        "core::alloc::Layout",
        ["align_to", "pad_to_align", "repeat_packed", "extend_packed", "extend", "repeat", "array"],
    )
    add(
        targets,
        "core::time::Duration",
        [
            "from_secs",
            "from_millis",
            "from_micros",
            "from_nanos",
            "from_nanos_u128",
            "from_hours",
            "from_mins",
            "as_millis",
            "as_micros",
            "as_nanos",
            "is_zero",
            "checked_add",
            "checked_sub",
            "checked_mul",
            "checked_div",
            "saturating_add",
            "saturating_sub",
            "saturating_mul",
            "abs_diff",
            "from_secs_f32",
            "from_secs_f64",
            "try_from_secs_f32",
            "try_from_secs_f64",
            "as_secs_f32",
            "as_secs_f64",
            "mul_f32",
            "mul_f64",
            "div_f32",
            "div_f64",
            "div_duration_f32",
            "div_duration_f64",
        ],
    )
    return targets


def coverage(name: str) -> dict[str, bool]:
    result: dict[str, bool] = {}
    with (ROOT / "results" / name).open() as stream:
        for row in csv.DictReader(stream):
            if row["stability"] != "stable":
                continue
            path = row["canonical_path"]
            result[path] = result.get(path, False) or row["covered"] == "True"
    return result


def category(target: str, original_classification: str) -> str:
    if original_classification == "representation_or_allocator":
        return "allocator_capacity_state"
    if target.startswith(
        (
            "alloc::collections::BinaryHeap::",
            "alloc::collections::LinkedList::",
            "alloc::collections::VecDeque::",
        )
    ):
        return "collection_private_internals"
    if target.startswith(
        (
            "alloc::ffi::",
            "alloc::string::FromUtf8Error::",
            "core::ffi::CStr::",
            "core::str::Utf8Error::",
        )
    ):
        return "ffi_private_buffers_and_errors"
    if target.startswith(
        (
            "core::net::Ipv4Addr::",
            "core::net::Ipv6Addr::",
            "core::net::SocketAddrV4::",
            "core::net::SocketAddrV6::",
        )
    ):
        return "network_leaf_representation"
    if target.startswith("core::alloc::Layout::"):
        return "layout_root_primitives"
    if target.startswith("core::panic::Location::"):
        return "compiler_location_state"
    if target.startswith("core::time::Duration::"):
        return "duration_root_representation"
    raise ValueError(f"unclassified target: {target}")


DESCRIPTIONS = {
    "collection_private_internals": (
        "Private Vec/node/ring-buffer fields, unsafe pointer algorithms, or guard/reference "
        "semantics are hidden by the public collection View."
    ),
    "allocator_capacity_state": (
        "Capacity and reserve behavior depends on RawVec/allocator state; success and final "
        "capacity are intentionally not uniquely determined by abstract contents."
    ),
    "ffi_private_buffers_and_errors": (
        "Raw slices, ownership transfer, NUL/UTF-8 scans, and private error payloads require "
        "memory/provenance and representation models not available to a downstream proof."
    ),
    "network_leaf_representation": (
        "Leaf address structs keep octets/ports private; constructors, accessors, endian "
        "conversions, and setters are the trusted roots beneath the verified enum dispatch."
    ),
    "layout_root_primitives": (
        "These are the trusted roots for private Alignment and compiler size/align intrinsics; "
        "derived Layout methods were verified from them."
    ),
    "compiler_location_state": (
        "Location fields and the trailing-NUL filename allocation are compiler-created private "
        "state, including raw-pointer reconstruction in file_as_c_str."
    ),
    "duration_root_representation": (
        "The private secs/Nanoseconds fields are the trusted representation roots beneath the "
        "verified Duration arithmetic and conversion methods."
    ),
}


def main() -> None:
    before = coverage("coverage-before-abstractions.csv")
    current = coverage("coverage.csv")
    newly_covered = {
        path for path, is_covered in current.items() if is_covered and not before.get(path, False)
    }
    verified = verified_new_stable_targets()
    verified &= newly_covered
    remaining = sorted(newly_covered - verified)

    classifications: dict[str, str] = {}
    with (ROOT / "specgen" / "classification.csv").open() as stream:
        for row in csv.DictReader(stream):
            classifications[row["target"]] = row["classification"]

    groups: dict[str, list[str]] = defaultdict(list)
    for target in remaining:
        groups[category(target, classifications.get(target, ""))].append(target)

    payload = {
        "newly_covered_stable": len(newly_covered),
        "source_verified": len(verified),
        "remaining": len(remaining),
        "groups": {
            key: {
                "count": len(values),
                "description": DESCRIPTIONS[key],
                "targets": values,
            }
            for key, values in groups.items()
        },
    }
    (Path(__file__).resolve().parent / "remaining_new_stable.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )

    lines = [
        "# Why 117 newly specified stable APIs lack source verification",
        "",
        f"- Newly covered stable APIs: **{len(newly_covered)}**",
        f"- Source-verified intersection: **{len(verified)}**",
        f"- Remaining: **{len(remaining)}**",
        "",
        "| Blocker | Count | Explanation |",
        "|---|---:|---|",
    ]
    for key, values in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        lines.append(f"| `{key}` | {len(values)} | {DESCRIPTIONS[key]} |")
    for key, values in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        lines.extend(["", f"## {key} ({len(values)})", ""])
        lines.extend(f"- `{target}`" for target in values)
    (Path(__file__).resolve().parent / "REMAINING.md").write_text(
        "\n".join(lines) + "\n"
    )

    assert len(newly_covered) == 211
    assert len(verified) == 94
    assert len(remaining) == 117
    assert sum(len(values) for values in groups.values()) == 117


if __name__ == "__main__":
    main()
