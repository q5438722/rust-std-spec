#!/usr/bin/env python3
"""Build typed spec-generation targets for stable Rust APIs missing vstd contracts."""

from __future__ import annotations

import argparse
from collections import defaultdict
import csv
import json
from pathlib import Path
from typing import Any

from survey import RustdocUniverse


CRATES = ("core", "alloc", "std")
PURE_PREFIXES = (
    "alloc::borrow::",
    "alloc::boxed::",
    "alloc::collections::",
    "alloc::rc::",
    "alloc::string::",
    "alloc::sync::",
    "alloc::vec::",
    "core::array::",
    "core::cell::",
    "core::cmp::",
    "core::convert::",
    "core::iter::",
    "core::mem::",
    "core::option::",
    "core::result::",
    "core::slice::",
    "core::str::",
)
RUNTIME_PREFIXES = (
    "std::env::",
    "std::fs::",
    "std::io::",
    "std::net::",
    "std::os::",
    "std::process::",
    "std::sync::",
    "std::thread::",
    "std::time::",
)


def resolved_id(type_data: Any) -> int | None:
    if not isinstance(type_data, dict):
        return None
    resolved = type_data.get("resolved_path")
    return resolved["id"] if resolved is not None else None


def contains_type_kind(value: Any, kind: str) -> bool:
    if isinstance(value, dict):
        if kind in value:
            return True
        return any(contains_type_kind(item, kind) for item in value.values())
    if isinstance(value, list):
        return any(contains_type_kind(item, kind) for item in value)
    return False


def source_context(rust_root: Path, span: dict[str, Any] | None, radius: int) -> str:
    if not span:
        return ""
    filename = span.get("filename")
    begin = span.get("begin")
    if not filename or not begin:
        return ""
    path = rust_root / "library" / filename
    if not path.is_file():
        return ""
    lines = path.read_text(errors="replace").splitlines()
    line = int(begin[0])
    start = max(1, line - radius)
    end = min(len(lines), line + radius)
    return "\n".join(
        f"{number:>6}: {lines[number - 1]}"
        for number in range(start, end + 1)
    )


class RustdocIndex:
    def __init__(self, rustdoc_dir: Path) -> None:
        self.docs = {
            crate: json.loads((rustdoc_dir / f"{crate}.json").read_text())
            for crate in CRATES
        }
        self.parents: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        self._index_parents()

    def item(self, declaration_id: str) -> tuple[str, str, dict[str, Any]]:
        crate, item_id = declaration_id.split(":", 1)
        return crate, item_id, self.docs[crate]["index"][item_id]

    def path(self, crate: str, item_id: int | str) -> list[str] | None:
        entry = self.docs[crate]["paths"].get(str(item_id))
        return entry["path"] if entry is not None else None

    def _index_parents(self) -> None:
        for crate, data in self.docs.items():
            index = data["index"]
            for parent_id, item in index.items():
                trait = item["inner"].get("trait")
                if trait is not None:
                    for child_id in trait["items"]:
                        self.parents[(crate, str(child_id))].append(
                            {
                                "kind": "trait",
                                "parent_id": parent_id,
                                "parent_name": item["name"],
                                "parent_path": self.path(crate, parent_id),
                            }
                        )
                impl = item["inner"].get("impl")
                if impl is not None:
                    for child_id in impl["items"]:
                        self.parents[(crate, str(child_id))].append(
                            {
                                "kind": "impl",
                                "parent_id": parent_id,
                                "trait": impl["trait"],
                                "for": impl["for"],
                                "generics": impl["generics"],
                            }
                        )

    def declaration(
        self,
        declaration_id: str,
        rust_root: Path,
        context_radius: int,
    ) -> dict[str, Any]:
        crate, item_id, item = self.item(declaration_id)
        function = item["inner"]["function"]
        parents = self.parents.get((crate, item_id), [])
        owner = None
        for parent in parents:
            if parent["kind"] == "trait":
                owner = {
                    "kind": "trait",
                    "item_id": f"{crate}:{parent['parent_id']}",
                    "name": parent["parent_name"],
                    "path": parent["parent_path"],
                }
                break
            impl_for_id = resolved_id(parent["for"])
            owner = {
                "kind": "trait_impl" if parent["trait"] is not None else "inherent_impl",
                "impl_id": f"{crate}:{parent['parent_id']}",
                "for": parent["for"],
                "trait": parent["trait"],
                "generics": parent["generics"],
                "resolved_owner_id": (
                    f"{crate}:{impl_for_id}" if impl_for_id is not None else None
                ),
                "resolved_owner_path": (
                    self.path(crate, impl_for_id)
                    if impl_for_id is not None
                    else None
                ),
            }
            if parent["trait"] is None:
                break

        signature = function["sig"]
        return_type = signature["output"]
        mutable_inputs = [
            name
            for name, type_data in signature["inputs"]
            if contains_type_kind(type_data, "borrowed_ref")
            and any(
                value is True
                for value in find_values(type_data, "is_mutable")
            )
        ]
        return_is_unit = return_type is None or (
            isinstance(return_type, dict) and return_type.get("tuple") == []
        )
        return_is_reference = contains_type_kind(return_type, "borrowed_ref")
        return_reference_is_mutable = return_is_reference and any(
            value is True
            for value in find_values(return_type, "is_mutable")
        )
        return_is_raw_pointer = contains_type_kind(return_type, "raw_pointer")
        span = item.get("span")
        return {
            "declaration_id": declaration_id,
            "name": item["name"],
            "visibility": item["visibility"],
            "stability": item.get("stability"),
            "deprecation": item.get("deprecation"),
            "attrs": item.get("attrs", []),
            "span": span,
            "header": function["header"],
            "signature": signature,
            "generics": function["generics"],
            "owner": owner,
            "observability": {
                "return_is_unit": return_is_unit,
                "return_is_reference": return_is_reference,
                "return_reference_is_mutable": return_reference_is_mutable,
                "return_is_raw_pointer": return_is_raw_pointer,
                "mutable_inputs": mutable_inputs,
                "has_modeled_output": not return_is_unit or bool(mutable_inputs),
            },
            "source_context": source_context(rust_root, span, context_radius),
        }


def find_values(value: Any, key: str) -> list[Any]:
    output: list[Any] = []
    if isinstance(value, dict):
        if key in value:
            output.append(value[key])
        for item in value.values():
            output.extend(find_values(item, key))
    elif isinstance(value, list):
        for item in value:
            output.extend(find_values(item, key))
    return output


def category(path: str, kinds: set[str]) -> str:
    if "trait_method" in kinds:
        return "trait_method"
    if path.startswith("core::sync::atomic::"):
        return "atomic"
    if path.startswith(("core::ptr::", "core::alloc::", "alloc::alloc::")):
        return "memory_pointer"
    if path.startswith(("core::fmt::", "alloc::fmt::", "std::fmt::")):
        return "formatting"
    if path.startswith(RUNTIME_PREFIXES):
        return "io_os_runtime"
    if path.startswith(PURE_PREFIXES):
        return "data_structure"
    return "other"


def semantic_risks(path: str, declarations: list[dict[str, Any]]) -> list[str]:
    risks: list[str] = []
    if path.startswith(RUNTIME_PREFIXES):
        risks.append("external_or_hidden_runtime_state")
    if path.startswith(("core::sync::atomic::", "std::sync::")):
        risks.append("concurrency_or_hidden_state")
    if path.startswith(("core::ptr::", "core::alloc::", "alloc::alloc::")):
        risks.append("unsafe_or_ownership_sensitive")
    if path.startswith(("core::fmt::", "alloc::fmt::", "std::fmt::")):
        risks.append("formatting_effect")
    if any(item["observability"]["return_is_unit"] for item in declarations):
        risks.append("unit_return_variant")
    if any(item["observability"]["return_is_reference"] for item in declarations):
        risks.append("reference_identity_vs_view")
    if any(item["observability"]["return_is_raw_pointer"] for item in declarations):
        risks.append("raw_pointer_equality")
    if len(declarations) > 1:
        risks.append("multiple_rust_declarations_share_path")
    return risks


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    uncovered = list(csv.DictReader(args.uncovered_csv.open()))
    coverage = list(csv.DictReader(args.coverage_csv.open()))
    target_paths = {row["canonical_path"] for row in uncovered}
    by_path: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in coverage:
        if (
            row["canonical_path"] in target_paths
            and row["covered"] == "False"
            and row["stability"] == "stable"
        ):
            by_path[row["canonical_path"]].append(row)

    rustdoc = RustdocIndex(args.rustdoc_dir)
    verus_rustdoc = RustdocIndex(args.verus_rustdoc_dir)
    verus_universe = RustdocUniverse(args.verus_rustdoc_dir)
    used_modules = sorted(
        {
            row["module"]
            for rows in by_path.values()
            for row in rows
        }
    )
    verus_apis: dict[str, list[Any]] = defaultdict(list)
    for module in used_modules:
        module_path = tuple(module.split("::"))
        if module_path not in verus_universe.modules:
            continue
        for api in verus_universe.module_apis(module_path):
            verus_apis[api.canonical_path].append(api)

    targets = []
    for uncovered_row in uncovered:
        path = uncovered_row["canonical_path"]
        rows = by_path[path]
        declaration_ids = sorted({row["declaration_id"] for row in rows})
        declarations = [
            rustdoc.declaration(item_id, args.rust_root, args.context_radius)
            for item_id in declaration_ids
        ]
        verification_api_rows = verus_apis.get(path, [])
        verification_declaration_ids = sorted(
            {row.declaration_id for row in verification_api_rows}
        )
        verification_declarations = [
            verus_rustdoc.declaration(
                item_id,
                args.verus_rust_root,
                args.context_radius,
            )
            for item_id in verification_declaration_ids
        ]
        kinds = {kind for row in rows for kind in row["kind"].split(";")}
        target_category = category(path, kinds)
        risks = semantic_risks(path, declarations)
        if not verification_declarations:
            risks.append("not_in_verus_rust_1_96")
        targets.append(
            {
                "target": path,
                "category": target_category,
                "kinds": sorted(kinds),
                "modules": sorted({row["module"] for row in rows}),
                "display_paths": sorted({row["display_path"] for row in rows}),
                "origin_paths": sorted({row["origin_path"] for row in rows}),
                "declaration_count": len(declarations),
                "declarations": declarations,
                "verification_declaration_count": len(verification_declarations),
                "verification_declarations": verification_declarations,
                "available_in_verus_rust_1_96": bool(verification_declarations),
                "semantic_risks": risks,
                "static_reward_eligible": not any(
                    risk
                    in {
                        "external_or_hidden_runtime_state",
                        "formatting_effect",
                        "not_in_verus_rust_1_96",
                        "unit_return_variant",
                    }
                    for risk in risks
                ),
                "recommended_contract_form": (
                    "external_trait_specification"
                    if "trait_method" in kinds
                    else "assume_specification"
                ),
            }
        )

    counts = defaultdict(int)
    for target in targets:
        counts[target["category"]] += 1
    return {
        "metadata": {
            "target_count": len(targets),
            "source": str(args.uncovered_csv),
            "context_radius": args.context_radius,
            "category_counts": dict(sorted(counts.items())),
            "reward_eligible_count": sum(
                target["static_reward_eligible"] for target in targets
            ),
            "available_in_verus_rust_1_96": sum(
                target["available_in_verus_rust_1_96"] for target in targets
            ),
            "unavailable_in_verus_rust_1_96": sum(
                not target["available_in_verus_rust_1_96"] for target in targets
            ),
        },
        "targets": targets,
    }


def write_pilot(manifest: dict[str, Any], path: Path, per_category: int) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for target in manifest["targets"]:
        grouped[target["category"]].append(target)
    pilot = []
    for name in sorted(grouped):
        choices = sorted(
            grouped[name],
            key=lambda target: (
                not target["static_reward_eligible"],
                len(target["semantic_risks"]),
                target["target"],
            ),
        )
        pilot.extend(choices[:per_category])
    path.write_text(
        json.dumps(
            {
                "metadata": {
                    "target_count": len(pilot),
                    "per_category": per_category,
                    "categories": sorted(grouped),
                },
                "targets": pilot,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument(
        "--uncovered-csv",
        type=Path,
        default=workspace / "results" / "uncovered_production_stable_apis.csv",
    )
    parser.add_argument(
        "--coverage-csv",
        type=Path,
        default=workspace / "results" / "coverage.csv",
    )
    parser.add_argument(
        "--rustdoc-dir",
        type=Path,
        default=workspace / "rustdoc-json",
    )
    parser.add_argument("--rust-root", type=Path, default=workspace / "rust")
    parser.add_argument(
        "--verus-rustdoc-dir",
        type=Path,
        default=workspace / "rustdoc-json-1.96",
    )
    parser.add_argument(
        "--verus-rust-root",
        type=Path,
        default=workspace / "rust-1.96",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=workspace / "specgen" / "stable-uncovered-manifest.json",
    )
    parser.add_argument(
        "--pilot-out",
        type=Path,
        default=workspace / "specgen" / "pilot-manifest.json",
    )
    parser.add_argument("--context-radius", type=int, default=45)
    parser.add_argument("--pilot-per-category", type=int, default=6)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_manifest(args)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    write_pilot(manifest, args.pilot_out, args.pilot_per_category)
    print(
        f"wrote {manifest['metadata']['target_count']} targets to {args.out} "
        f"and pilot to {args.pilot_out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
