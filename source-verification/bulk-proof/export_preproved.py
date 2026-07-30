#!/usr/bin/env python3
"""Copy the existing source-verification harnesses into proved-apis per target."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil


HERE = Path(__file__).resolve().parent
SOURCE_VERIFICATION = HERE.parent
PROVED_ROOT = SOURCE_VERIFICATION / "proved-apis"


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value)


def harness(target: dict) -> str:
    path = target["normalized_api_path"]
    raw = compact(target["raw_target"])
    if path.startswith("core::cmp::Ordering::") or path.startswith("core::ops::ControlFlow::"):
        return "pure_control_flow.rs"
    if "branch" in raw:
        return "pure_control_flow.rs"
    if "from_residual" in raw:
        return "residual.rs"
    if "VecDeque" in raw:
        if "swap_remove_" in raw:
            return "vecdeque.rs"
        if "with_capacity" in raw:
            return "capacity_composed.rs"
        return "collections.rs"
    if path.startswith("alloc::collections::BinaryHeap::"):
        return "capacity_composed.rs" if path.endswith("with_capacity") else "collections.rs"
    if path.startswith("alloc::collections::LinkedList::"):
        return "collections.rs"
    if path in {"alloc::string::String::with_capacity", "alloc::vec::Vec::with_capacity"}:
        return "capacity_composed.rs"
    if path.startswith(("core::net::IpAddr::", "core::net::Ipv6Addr::to_canonical")):
        return "net_enums.rs"
    if path.startswith("core::net::SocketAddr::"):
        return "socket_addr.rs"
    if path.startswith(("core::net::Ipv4Addr::", "core::net::Ipv6Addr::")):
        return "net.rs"
    if path.startswith(("core::ffi::CStr::", "alloc::ffi::CString::")):
        return "ffi.rs"
    if path.startswith("core::alloc::Layout::"):
        return "layout.rs"
    if path.startswith("core::time::Duration::"):
        name = path.rsplit("::", 1)[-1]
        if name in {"from_secs_f32", "from_secs_f64"}:
            return "duration_from_secs.rs"
        if name in {"try_from_secs_f32", "try_from_secs_f64"}:
            return "duration_try_from.rs"
        if name in {
            "as_secs_f32",
            "as_secs_f64",
            "mul_f32",
            "mul_f64",
            "div_f32",
            "div_f64",
            "div_duration_f32",
            "div_duration_f64",
        }:
            return "duration_float.rs"
        return "duration_integer.rs"
    raise ValueError(f"no preproved harness mapping for {target['id']} {path} {raw}")


TRUST_LEVEL = {
    "pure_control_flow.rs": "A",
    "residual.rs": "C",
    "vecdeque.rs": "B",
    "collections.rs": "B",
    "capacity_composed.rs": "B",
    "net.rs": "B",
    "net_enums.rs": "B",
    "socket_addr.rs": "B",
    "ffi.rs": "B",
    "layout.rs": "C",
    "duration_integer.rs": "C",
    "duration_from_secs.rs": "B",
    "duration_try_from.rs": "E",
    "duration_float.rs": "D",
}


def main() -> None:
    manifest = json.loads((HERE / "manifest.json").read_text())
    targets = [target for target in manifest["targets"] if target["preproved"]]
    PROVED_ROOT.mkdir(parents=True, exist_ok=True)
    exported = []
    for target in targets:
        harness_name = harness(target)
        source = SOURCE_VERIFICATION / harness_name
        destination = PROVED_ROOT / target["id"]
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination / "proof.rs")
        metadata = {
            "id": target["id"],
            "api_path": target["api_path"],
            "raw_target": target["raw_target"],
            "contract_source_file": target["contract_source_file"],
            "contract_source_line": target["contract_source_line"],
            "preproved": True,
            "proof_bundle": harness_name,
            "trust_level": TRUST_LEVEL[harness_name],
        }
        (destination / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        exported.append(metadata)
    (PROVED_ROOT / "preproved_manifest.json").write_text(
        json.dumps({"count": len(exported), "targets": exported}, indent=2) + "\n"
    )
    print(f"exported {len(exported)} preproved contract records")


if __name__ == "__main__":
    main()
