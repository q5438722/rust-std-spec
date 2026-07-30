#!/usr/bin/env python3
"""Run determinism checks for assume_specification declarations in one vstd module."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import logging
from pathlib import Path
import re
import sys

from tree_sitter import Language, Parser
import tree_sitter_verus

from run_rust_std_spec_feedback import (
    active_contract_code,
    run_determinism,
    safe_name,
)


SPEC_DET_ROOT = Path("/home/chentianyu/intent_formalization/spec-determinism")
sys.path.insert(0, str(SPEC_DET_ROOT))

from spec_determinism.extract.extractor import extract_spec
from spec_determinism.view.registry import ViewRegistry


def walk(node):
    yield node
    for child in node.named_children:
        yield from walk(child)


def target_text(node, source: bytes) -> str:
    target = node.child_by_field_name("target")
    return (
        source[target.start_byte : target.end_byte].decode(errors="replace")
        if target is not None
        else "unknown"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument("module_file", type=Path)
    parser.add_argument("--imports", action="append", default=[])
    parser.add_argument("--feature", action="append", default=[])
    parser.add_argument(
        "--vstd-root",
        type=Path,
        default=workspace / "verus" / "source" / "vstd",
    )
    parser.add_argument(
        "--verus-bin",
        type=Path,
        default=workspace
        / "verus"
        / "source"
        / "target-verus"
        / "release"
        / "verus",
    )
    parser.add_argument(
        "--z3-path",
        type=Path,
        default=workspace / "verus" / "source" / "z3",
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--rlimit", type=float, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.module_file.read_bytes()
    tree = Parser(Language(tree_sitter_verus.language())).parse(source)
    contracts = [
        node for node in walk(tree.root_node) if node.type == "assume_specification_item"
    ]
    if not contracts:
        raise ValueError(f"no assume_specification declarations in {args.module_file}")
    logging.getLogger("spec_determinism").setLevel(logging.ERROR)
    registry = ViewRegistry.from_project(args.vstd_root)
    args.out.mkdir(parents=True, exist_ok=True)
    results = []
    imports = [
        *args.imports,
        "vstd::prelude::*",
    ]
    for index, node in enumerate(contracts, start=1):
        code = source[node.start_byte : node.end_byte].decode(errors="replace")
        target = target_text(node, source)
        candidate = {
            "decision": "add_spec",
            "contract_form": "assume_specification",
            "contract_code": active_contract_code({"contract_code": code}),
            "requires": [],
            "ensures": [],
            "feature_gates": args.feature,
            "imports": imports,
            "useful": True,
            "rationale": "hand-written experimental vstd contract",
            "risks": [],
        }
        target_dir = args.out / safe_name(target)
        target_dir.mkdir(parents=True, exist_ok=True)
        result = run_determinism(
            candidate=candidate,
            round_dir=target_dir,
            view_registry=registry,
            verus_bin=args.verus_bin,
            z3_path=args.z3_path,
            timeout=args.timeout,
            rlimit=args.rlimit,
        )
        result["target"] = target
        result["source_line"] = node.start_point.row + 1
        results.append(result)
        print(
            f"[{index}/{len(contracts)}] {target} "
            f"status={result.get('status')} r0={result.get('r0_z3')}",
            flush=True,
        )

    counts = {
        "targets": len(results),
        "status": dict(Counter(result.get("status", "") for result in results)),
        "r0_z3": dict(Counter(result.get("r0_z3", "") for result in results)),
        "classification": dict(
            Counter(result.get("classification", "") for result in results)
        ),
    }
    payload = {
        "metadata": {
            "module_file": str(args.module_file.resolve()),
            "imports": imports,
        },
        "counts": counts,
        "results": results,
    }
    (args.out / "summary.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )
    lines = [
        f"# Determinism audit: {args.module_file.name}",
        "",
        f"- Targets: {counts['targets']}",
        f"- R0 results: `{counts['r0_z3']}`",
        "",
        "| Target | Status | R0 | Classification |",
        "|---|---|---|---|",
    ]
    for result in results:
        lines.append(
            f"| `{result['target']}` | {result.get('status', '')} | "
            f"{result.get('r0_z3', '')} | {result.get('classification', '')} |"
        )
    (args.out / "SUMMARY.md").write_text("\n".join(lines).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
