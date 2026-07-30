#!/usr/bin/env python3
"""Run the determinism checker for all direct vstd assume_specification records."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import logging
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(ROOT / "bulk-proof"))

from organize_suite import FEATURES, original_imports
import run_rust_std_spec_feedback as feedback
from run_rust_std_spec_feedback import active_contract_code
from spec_determinism.view.registry import ViewRegistry


ORIGINAL_ASSUME_TO_SYNTHETIC = feedback.assume_to_synthetic


def rewrite_returns(source: str) -> str:
    match = re.search(r"\breturns\b", source)
    if match is None:
        return source
    start = match.end()
    paren = bracket = brace = angle = 0
    comma = None
    for index in range(start, len(source)):
        char = source[index]
        if char == "(":
            paren += 1
        elif char == ")":
            paren -= 1
        elif char == "[":
            bracket += 1
        elif char == "]":
            bracket -= 1
        elif char == "{":
            brace += 1
        elif char == "}":
            brace -= 1
        elif char == "<":
            angle += 1
        elif char == ">" and angle:
            angle -= 1
        elif char == "," and paren == bracket == brace == angle == 0:
            comma = index
            break
    if comma is None:
        return source
    expression = source[start:comma].strip()
    header = source[: match.start()]
    named = re.search(r"->\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*:", header)
    if named:
        result_name = named.group(1)
    else:
        arrow = header.rfind("->")
        if arrow < 0:
            return source
        return_start = arrow + 2
        return_end = len(header)
        for keyword in ("\n    requires", "\n    ensures", "\n    where", "\n    opens_invariants", "\n    no_unwind"):
            position = header.find(keyword, return_start)
            if position >= 0:
                return_end = min(return_end, position)
        return_type = header[return_start:return_end].strip()
        result_name = "result"
        header = (
            header[:return_start]
            + f" (result: {return_type})"
            + header[return_end:]
        )
    return (
        header
        + f"ensures\n        {result_name} == ({expression}),"
        + source[comma + 1 :]
    )


def assume_to_synthetic_with_returns(contract_code: str) -> str:
    return rewrite_returns(ORIGINAL_ASSUME_TO_SYNTHETIC(contract_code))


feedback.assume_to_synthetic = assume_to_synthetic_with_returns
run_determinism = feedback.run_determinism


def imports_for(target: dict) -> list[str]:
    text = original_imports(target["contract_source_file"])
    imports = re.findall(r"(?m)^use\s+(.+);$", text)
    imports.append(target["suggested_vstd_import"])
    return list(dict.fromkeys(imports))


def run_one(
    target: dict,
    *,
    out: Path,
    registry: ViewRegistry,
    verus_bin: Path,
    z3_path: Path,
    timeout: int,
    rlimit: float,
) -> dict:
    target_dir = out / "targets" / target["id"]
    target_dir.mkdir(parents=True, exist_ok=True)
    candidate = {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": active_contract_code({"contract_code": target["contract_code"]}),
        "requires": [],
        "ensures": [],
        "feature_gates": FEATURES,
        "imports": imports_for(target),
        "useful": True,
        "rationale": "all-vstd determinism audit",
        "risks": [],
    }
    result = run_determinism(
        candidate=candidate,
        round_dir=target_dir,
        view_registry=registry,
        verus_bin=verus_bin,
        z3_path=z3_path,
        timeout=timeout,
        rlimit=rlimit,
    )
    result.update(
        {
            "id": target["id"],
            "api_path": target["api_path"],
            "raw_target": target["raw_target"],
            "contract_source_file": target["contract_source_file"],
            "contract_source_line": target["contract_source_line"],
        }
    )
    (target_dir / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def write_summary(out: Path, results: list[dict]) -> None:
    status = Counter(result.get("status", "") for result in results)
    r0 = Counter(result.get("r0_z3", "") for result in results)
    classification = Counter(result.get("classification", "") for result in results)
    complete = [
        result
        for result in results
        if result.get("status") == "ok"
        and result.get("r0_z3") == "unsat"
        and not result.get("equal_fn_trivial")
    ]
    trivial = [
        result
        for result in results
        if result.get("status") == "ok" and result.get("equal_fn_trivial")
    ]
    payload = {
        "counts": {
            "targets": len(results),
            "status": dict(status),
            "r0_z3": dict(r0),
            "classification": dict(classification),
            "complete_nontrivial": len(complete),
            "trivial_equality": len(trivial),
        },
        "results": sorted(results, key=lambda item: item["id"]),
    }
    (out / "summary.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = [
        "# Determinism of all direct vstd contracts",
        "",
        f"- Targets processed: **{len(results)}**",
        f"- Complete, nontrivial (`R0=unsat`): **{len(complete)}**",
        f"- Trivial equality: **{len(trivial)}**",
        f"- Status counts: `{dict(status)}`",
        f"- R0 counts: `{dict(r0)}`",
        "",
        "| Target | Status | R0 | Classification | Trivial equal |",
        "|---|---|---|---|---|",
    ]
    for result in sorted(results, key=lambda item: item["id"]):
        lines.append(
            f"| `{result['api_path']}` | {result.get('status', '')} | "
            f"{result.get('r0_z3', '')} | {result.get('classification', '')} | "
            f"{result.get('equal_fn_trivial', False)} |"
        )
    (out / "SUMMARY.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "bulk-proof" / "manifest.json",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "determinism-all",
    )
    parser.add_argument("--jobs", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--rlimit", type=float, default=60)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--only-returns", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    targets = manifest["targets"]
    if args.only_returns:
        targets = [target for target in targets if re.search(r"\breturns\b", target["contract_code"])]
    if args.limit is not None:
        targets = targets[: args.limit]
    args.out.mkdir(parents=True, exist_ok=True)
    logging.getLogger("spec_determinism").setLevel(logging.ERROR)
    vstd_root = WORKSPACE / "verus" / "source" / "vstd"
    registry = ViewRegistry.from_project(vstd_root)
    verus_bin = WORKSPACE / "verus" / "source" / "target-verus" / "release" / "verus"
    z3_path = WORKSPACE / "verus" / "source" / "z3"
    results = []
    pending = []
    for target in targets:
        summary_path = args.out / "targets" / target["id"] / "summary.json"
        if args.resume and summary_path.is_file():
            results.append(json.loads(summary_path.read_text()))
        else:
            pending.append(target)
    write_summary(args.out, results)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(
                run_one,
                target,
                out=args.out,
                registry=registry,
                verus_bin=verus_bin,
                z3_path=z3_path,
                timeout=args.timeout,
                rlimit=args.rlimit,
            ): target
            for target in pending
        }
        for future in as_completed(futures):
            target = futures[future]
            try:
                result = future.result()
            except Exception as error:
                result = {
                    "id": target["id"],
                    "api_path": target["api_path"],
                    "raw_target": target["raw_target"],
                    "status": "exception",
                    "error": f"{type(error).__name__}: {error}",
                }
            results.append(result)
            print(
                f"[{len(results)}/{len(targets)}] {target['api_path']} "
                f"status={result.get('status')} r0={result.get('r0_z3')}",
                flush=True,
            )
            write_summary(args.out, results)
    write_summary(args.out, results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
