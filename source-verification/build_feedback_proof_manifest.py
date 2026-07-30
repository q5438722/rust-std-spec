#!/usr/bin/env python3
"""Build paired no-feedback/with-feedback source-proof variants."""

from __future__ import annotations

from collections import defaultdict
import glob
import hashlib
import json
from pathlib import Path
import re

from tree_sitter import Language, Parser
import tree_sitter_verus


ROOT = Path(__file__).resolve().parent.parent
SOURCE_VERIFICATION = ROOT / "source-verification"
SPECGEN = ROOT / "specgen"
RUST_ROOT = ROOT / "rust-1.96"
OUT = SOURCE_VERIFICATION / "feedback-proof"
PARSER = Parser(Language(tree_sitter_verus.language()))
VALID_CATEGORIES = {"complete", "unknown", "trivial_equality", "incomplete_sat"}


def batch_files() -> list[Path]:
    return [
        SPECGEN / "suitable-pilot-gpt56sol-v2" / "batch_summary.json",
        SPECGEN / "suitable-remaining-gpt56sol-v1" / "batch_summary.json",
        *sorted(
            Path(path)
            for path in glob.glob(
                str(
                    SPECGEN
                    / "remaining-generation"
                    / "evaluated-gpt56sol"
                    / "*"
                    / "batch_summary.json"
                )
            )
        ),
    ]


def record_category(record: dict) -> str:
    candidate = record.get("candidate") or {}
    if candidate.get("decision") != "add_spec":
        return "skip_no_spec"
    checker = record.get("checker") or {}
    typecheck = checker.get("typecheck") or {}
    determinism = checker.get("determinism") or {}
    if typecheck and typecheck.get("returncode") != 0:
        return "typecheck_or_checker_failure"
    if determinism.get("status") == "ok":
        if determinism.get("equal_fn_trivial"):
            return "trivial_equality"
        return {
            "unsat": "complete",
            "unknown": "unknown",
            "sat": "incomplete_sat",
        }.get(determinism.get("r0_z3"), "typecheck_or_checker_failure")
    return "typecheck_or_checker_failure"


def phase_records() -> dict[str, dict[str, dict]]:
    occurrences: dict[str, list[tuple[dict, dict]]] = defaultdict(list)
    for path in batch_files():
        payload = json.loads(path.read_text())
        for result in payload["results"]:
            history = result.get("history") or []
            round_zero = next(
                (item for item in history if item.get("round") == 0),
                history[0] if history else {},
            )
            final = result.get("final") or (history[-1] if history else {})
            occurrences[result["target"]].append((round_zero, final))
    assert len(occurrences) == 2121
    return {
        "no_feedback": {
            target: values[0][0] for target, values in occurrences.items()
        },
        "with_feedback": {
            target: values[-1][1] for target, values in occurrences.items()
        },
    }


def source_text(span: dict | None) -> str:
    if not span:
        return ""
    filename = span.get("filename")
    begin = span.get("begin")
    end = span.get("end")
    if not filename or not begin or not end:
        return ""
    path = RUST_ROOT / "library" / filename
    if not path.is_file():
        return ""
    lines = path.read_text(errors="replace").splitlines(keepends=True)
    start_line, start_col = int(begin[0]) - 1, int(begin[1]) - 1
    end_line, end_col = int(end[0]) - 1, int(end[1]) - 1
    if start_line == end_line:
        return lines[start_line][start_col:end_col]
    return (
        lines[start_line][start_col:]
        + "".join(lines[start_line + 1 : end_line])
        + lines[end_line][:end_col]
    )


def target_text(contract: str, fallback: str) -> str:
    source = contract.encode()
    tree = PARSER.parse(source)
    stack = [tree.root_node]
    while stack:
        node = stack.pop()
        if node.type == "assume_specification_item":
            target = node.child_by_field_name("target")
            if target is not None:
                return source[target.start_byte : target.end_byte].decode(
                    errors="replace"
                )
        stack.extend(reversed(node.named_children))
    return fallback


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", value).strip("_")


def main() -> None:
    phases = phase_records()
    stable = json.loads((SPECGEN / "stable-uncovered-manifest.json").read_text())
    stable_by_target = {target["target"]: target for target in stable["targets"]}

    variants: dict[tuple[str, str], dict] = {}
    phase_rows = []
    for phase, records in phases.items():
        for api_path, record in sorted(records.items()):
            category = record_category(record)
            candidate = record.get("candidate") or {}
            contract = candidate.get("contract_code", "")
            phase_row = {
                "phase": phase,
                "target": api_path,
                "category": category,
                "variant_id": "",
            }
            if category in VALID_CATEGORIES:
                assert contract
                key = (api_path, re.sub(r"\s+", "", contract))
                if key not in variants:
                    digest = hashlib.sha256(contract.encode()).hexdigest()[:12]
                    variant_id = f"{safe_name(api_path)}__{digest}"
                    source_target = stable_by_target[api_path]
                    declarations = []
                    for declaration in source_target["verification_declarations"]:
                        item = dict(declaration)
                        item["source_text"] = source_text(item.get("span"))
                        item["has_body"] = (
                            "{" in item["source_text"] and "}" in item["source_text"]
                        )
                        declarations.append(item)
                    declarations.sort(
                        key=lambda item: (
                            not item["has_body"],
                            item.get("visibility") != "public",
                            item["declaration_id"],
                        )
                    )
                    imports = candidate.get("imports") or []
                    context = "\n".join(f"use {value};" for value in imports)
                    variants[key] = {
                        "id": variant_id,
                        "ordinal": len(variants),
                        "api_path": api_path,
                        "normalized_api_path": api_path,
                        "raw_target": target_text(contract, api_path),
                        "function_name": api_path.rsplit("::", 1)[-1],
                        "contract_source_file": f"specgen/{phase}",
                        "contract_source_line": 0,
                        "contract_code": contract,
                        "contract_module_context": context,
                        "suggested_vstd_import": "vstd::prelude::*",
                        "preproved": False,
                        "verification_declarations": declarations,
                        "has_rust_1_96_body": any(
                            item["has_body"] for item in declarations
                        ),
                        "fidelity_retry_context": (
                            "This artifact is used for a determinism-feedback "
                            "provability comparison. Copy the exact Rust executable "
                            "operations/control flow or a mechanical desugaring. Do "
                            "not declare new axioms, replace private operations with "
                            "public alternatives, or use an equivalent algorithm. "
                            "Return blocked if the exact implementation is unavailable."
                        ),
                        "feedback_variants": [],
                    }
                variants[key]["feedback_variants"].append(
                    {"phase": phase, "category": category}
                )
                phase_row["variant_id"] = variants[key]["id"]
            phase_rows.append(phase_row)

    targets = list(variants.values())
    assert len(targets) == 357, len(targets)
    assert len(phase_rows) == 4242
    payload = {
        "metadata": {
            "purpose": (
                "Source-proof comparison for valid contracts before and after "
                "determinism feedback."
            )
        },
        "counts": {
            "unique_contract_variants": len(targets),
            "no_feedback_valid_contracts": sum(
                row["phase"] == "no_feedback" and bool(row["variant_id"])
                for row in phase_rows
            ),
            "with_feedback_valid_contracts": sum(
                row["phase"] == "with_feedback" and bool(row["variant_id"])
                for row in phase_rows
            ),
        },
        "targets": targets,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(payload, indent=2) + "\n")
    (OUT / "phase-status.json").write_text(
        json.dumps({"rows": phase_rows}, indent=2) + "\n"
    )
    print(json.dumps(payload["counts"], indent=2))


if __name__ == "__main__":
    main()
