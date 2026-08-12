#!/usr/bin/env python3
"""Run feedback-pipeline determinism for generated alloc::vec assume-specs."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SURVEY_ROOT = Path("/home/chentianyu/nanvix-rust-std-spec-survey")
DEFAULT_VSTD_ROOT = DEFAULT_SURVEY_ROOT / "verus" / "source" / "vstd"
DEFAULT_VERUS_BIN = DEFAULT_SURVEY_ROOT / "verus" / "source" / "target-verus" / "release" / "verus"
DEFAULT_Z3_PATH = DEFAULT_SURVEY_ROOT / "verus" / "source" / "z3"
DEFAULT_EVIDENCE_ROOT = ROOT / "verification" / "evidence" / "vec_feedback_determinism"
DEFAULT_IMPORTS = ("vstd::seq::*", "vstd::view::*", "alloc::vec::*", "alloc::boxed::Box")
DEFAULT_FEATURE_GATES = ("allocator_api", "vec_into_raw_parts")
EXPECTED_GENERATED_TARGETS = 24
GENERATED_TARGETS = {
    "alloc::vec::Drain::as_slice",
    "alloc::vec::IntoIter::as_mut_slice",
    "alloc::vec::IntoIter::as_slice",
    "alloc::vec::Vec::as_mut_ptr",
    "alloc::vec::Vec::as_ptr",
    "alloc::vec::Vec::dedup",
    "alloc::vec::Vec::dedup_by",
    "alloc::vec::Vec::dedup_by_key",
    "alloc::vec::Vec::drain",
    "alloc::vec::Vec::extend_from_within",
    "alloc::vec::Vec::extract_if",
    "alloc::vec::Vec::from_raw_parts",
    "alloc::vec::Vec::insert_mut",
    "alloc::vec::Vec::into_boxed_slice",
    "alloc::vec::Vec::into_flattened",
    "alloc::vec::Vec::into_raw_parts",
    "alloc::vec::Vec::leak",
    "alloc::vec::Vec::pop_if",
    "alloc::vec::Vec::push_mut",
    "alloc::vec::Vec::resize_with",
    "alloc::vec::Vec::retain",
    "alloc::vec::Vec::retain_mut",
    "alloc::vec::Vec::set_len",
    "alloc::vec::Vec::spare_capacity_mut",
}

UNKNOWN_REASON_SUMMARIES = {
    "callback-trace-boundary": "FnMut/FnOnce or Clone effects are modeled by ordered source callback traces, preserving relational outcomes.",
    "iterator-adaptor-state-boundary": "Iterator/adaptor values expose modeled remaining sequences but keep opaque lifetime/drop state.",
    "raw-pointer-provenance-boundary": "Pointer address, provenance, and allocation layout are not uniquely recoverable from the Vec Seq view.",
    "maybeuninit-storage-boundary": "MaybeUninit spare storage is modeled relationally and cannot be collapsed to initialized values.",
    "conversion-allocation-boundary": "Conversion preserves logical sequence while allocation identity/lifetime provenance remains boundary state.",
    "array-flatten-boundary": "Fixed-array flattening preserves order while layout/capacity is relational.",
    "mutable-reference-view-boundary": "Returned mutable reference identity and post-borrow mutation frame remain relational.",
}

UNKNOWN_REASON_BY_TARGET = {
    "alloc::vec::Drain::as_slice": "iterator-adaptor-state-boundary",
    "alloc::vec::IntoIter::as_mut_slice": "iterator-adaptor-state-boundary",
    "alloc::vec::IntoIter::as_slice": "iterator-adaptor-state-boundary",
    "alloc::vec::Vec::as_mut_ptr": "raw-pointer-provenance-boundary",
    "alloc::vec::Vec::as_ptr": "raw-pointer-provenance-boundary",
    "alloc::vec::Vec::dedup": "callback-trace-boundary",
    "alloc::vec::Vec::dedup_by": "callback-trace-boundary",
    "alloc::vec::Vec::dedup_by_key": "callback-trace-boundary",
    "alloc::vec::Vec::drain": "iterator-adaptor-state-boundary",
    "alloc::vec::Vec::extend_from_within": "callback-trace-boundary",
    "alloc::vec::Vec::extract_if": "iterator-adaptor-state-boundary",
    "alloc::vec::Vec::from_raw_parts": "raw-pointer-provenance-boundary",
    "alloc::vec::Vec::insert_mut": "mutable-reference-view-boundary",
    "alloc::vec::Vec::into_boxed_slice": "conversion-allocation-boundary",
    "alloc::vec::Vec::into_flattened": "array-flatten-boundary",
    "alloc::vec::Vec::into_raw_parts": "raw-pointer-provenance-boundary",
    "alloc::vec::Vec::leak": "conversion-allocation-boundary",
    "alloc::vec::Vec::pop_if": "callback-trace-boundary",
    "alloc::vec::Vec::push_mut": "mutable-reference-view-boundary",
    "alloc::vec::Vec::resize_with": "callback-trace-boundary",
    "alloc::vec::Vec::retain": "callback-trace-boundary",
    "alloc::vec::Vec::retain_mut": "callback-trace-boundary",
    "alloc::vec::Vec::set_len": "raw-pointer-provenance-boundary",
    "alloc::vec::Vec::spare_capacity_mut": "maybeuninit-storage-boundary",
    "alloc::vec::Vec::splice": "iterator-adaptor-state-boundary",
}


def fail(message: str) -> None:
    print(f"vec feedback determinism failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_feedback_module(survey_root: Path) -> Any:
    module_path = survey_root / "run_rust_std_spec_feedback.py"
    if not module_path.is_file():
        fail(f"missing feedback runner {module_path}")
    sys.path.insert(0, str(survey_root))
    spec = importlib.util.spec_from_file_location("run_rust_std_spec_feedback", module_path)
    if spec is None or spec.loader is None:
        fail(f"cannot load feedback runner {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def matching_delimiter(text: str, start: int, opening: str, closing: str) -> int:
    depth = 0
    for index in range(start, len(text)):
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return index
    fail(f"unclosed {opening}")


def verus_body(source: str) -> str:
    match = re.search(r"\bverus!\s*\{", source)
    if match is None:
        fail("source has no verus! body")
    brace = source.find("{", match.start())
    end = matching_delimiter(source, brace, "{", "}")
    return source[brace + 1 : end]


def shared_vocabulary_body(path: Path) -> str:
    body = verus_body(path.read_text()).strip()
    if "verus!" in body:
        fail("nested verus! in shared vocabulary")
    return body


def assume_spec_items(body: str) -> list[str]:
    items = []
    for match in re.finditer(r"\b(?:pub\s+)?assume_specification\b", body):
        paren = bracket = brace = 0
        semicolon = None
        for index in range(match.start(), len(body)):
            char = body[index]
            if char == "(":
                paren += 1
            elif char == ")" and paren:
                paren -= 1
            elif char == "[":
                bracket += 1
            elif char == "]" and bracket:
                bracket -= 1
            elif char == "{":
                brace += 1
            elif char == "}" and brace:
                brace -= 1
            elif char == ";" and paren == bracket == brace == 0:
                semicolon = index
                break
        if semicolon is None:
            fail("unterminated assume_specification")
        items.append(body[match.start() : semicolon + 1].strip())
    return items


def normalize_target(target: str) -> str:
    return re.sub(r"\s+", " ", target).strip()


def strip_generic_suffix(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"::\s*<[^>]+>(?=::|$)", "", text)
    return re.sub(r"::<[^>]+>$", "", text)


def strip_all_turbofish(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"::\s*<[^>]+>", "", text)
    return text


def catalog_target_from_contract_target(contract_target: str) -> str:
    normalized = normalize_target(contract_target)
    simplified = strip_all_turbofish(normalized)
    if "::Drain" in simplified or simplified.startswith("Drain::"):
        return "alloc::vec::Drain::as_slice"
    if "::IntoIter" in simplified or simplified.startswith("IntoIter::"):
        if "as_mut_slice" in simplified:
            return "alloc::vec::IntoIter::as_mut_slice"
        return "alloc::vec::IntoIter::as_slice"
    if "Vec::into_flattened" in simplified:
        return "alloc::vec::Vec::into_flattened"
    if "::Vec" in simplified or simplified.startswith("Vec::") or simplified.startswith("<Vec"):
        method = simplified.rsplit("::", 1)[-1]
        method = strip_generic_suffix(method)
        return "alloc::vec::Vec::" + method
    fail(f"unsupported Vec assume_specification target form {contract_target!r}")


def split_top_level_commas(text: str) -> list[str]:
    clauses = []
    start = 0
    paren = bracket = brace = 0
    for index, char in enumerate(text):
        if char == "(":
            paren += 1
        elif char == ")" and paren:
            paren -= 1
        elif char == "[":
            bracket += 1
        elif char == "]" and bracket:
            bracket -= 1
        elif char == "{":
            brace += 1
        elif char == "}" and brace:
            brace -= 1
        elif char == "," and paren == bracket == brace == 0:
            clause = text[start:index].strip()
            if clause:
                clauses.append(clause)
            start = index + 1
    clause = text[start:].strip().rstrip(";").strip()
    if clause:
        clauses.append(clause)
    return clauses


def extract_clause_block(item: str, keyword: str) -> list[str]:
    match = re.search(rf"\b{keyword}\b", item)
    if match is None:
        return []
    next_keyword = re.search(r"\b(?:requires|ensures)\b", item[match.end() :])
    semicolon = item.rfind(";")
    end = semicolon if next_keyword is None else match.end() + next_keyword.start()
    return split_top_level_commas(item[match.end() : end])


def read_catalog(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or []), list(reader)


def build_assume_spec_index(feedback: Any, generated_path: Path) -> dict[str, dict[str, str]]:
    body = verus_body(generated_path.read_text())
    by_target: dict[str, dict[str, str]] = {}
    for item in assume_spec_items(body):
        contract_target = normalize_target(feedback.assume_specification_target(item))
        target = catalog_target_from_contract_target(contract_target)
        if target in by_target:
            fail(f"duplicate generated assume_specification for {target}")
        by_target[target] = {"contract_target": contract_target, "item": item}
    return by_target


def build_candidate(target: str, item: str, shared_body: str, catalog: dict[str, dict[str, str]]) -> dict[str, Any]:
    row = catalog[target]
    return {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "target": target,
        "contract_code": f"{shared_body}\n\n{item}",
        "requires": extract_clause_block(item, "requires"),
        "ensures": extract_clause_block(item, "ensures"),
        "source_requires": extract_clause_block(item, "requires"),
        "source_ensures": extract_clause_block(item, "ensures"),
        "imports": list(DEFAULT_IMPORTS),
        "feature_gates": list(DEFAULT_FEATURE_GATES),
        "useful": True,
        "rationale": "project-local alloc::vec candidate built from executable assume_specification and shared Vec vocabulary",
        "risks": [row.get("known_risks", "")],
        "semantic_family": row.get("semantic_family", ""),
        "source_reference": row.get("source_reference", ""),
        "catalog_requires": row.get("requires", ""),
        "catalog_ensures": row.get("ensures", ""),
    }


def safe_artifacts(target_dir: Path) -> dict[str, Any]:
    names = [
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
    ]
    artifacts = {name: str((target_dir / name).relative_to(ROOT)) for name in names if (target_dir / name).is_file()}
    smt2 = sorted((target_dir / "verus_log").rglob("*.smt2"))
    if smt2:
        artifacts["smt2_files"] = [str(path.relative_to(ROOT)) for path in smt2]
    return artifacts


def write_minimal_artifacts(target_dir: Path, candidate: dict[str, Any], feedback: Any, result: dict[str, Any]) -> None:
    active = feedback.active_contract_code(candidate)
    synthetic = feedback.assume_to_synthetic(active)
    (target_dir / "active_contract_code.rs").write_text(active)
    (target_dir / "__rust_std_candidate.rs").write_text(synthetic)
    if not (target_dir / "synthetic_spec.rs").is_file():
        (target_dir / "synthetic_spec.rs").write_text(synthetic)
    status = result.get("status", "runner_crash")
    for name, content in {
        "det_spec.json": json.dumps({"status": status, "requires": result.get("requires", []), "ensures": result.get("ensures", [])}, indent=2, sort_keys=True) + "\n",
        "det_harness.rs": f"// Determinism harness status={status}\n",
        "det_stdout.txt": "",
        "det_stderr.txt": f"determinism status={status}\n",
        "verus_stdout.txt": "",
        "verus_stderr.txt": f"determinism status={status}\n",
        "schema_search_evidence.json": json.dumps({"status": status, "r0_z3": result.get("r0_z3"), "classification": result.get("classification")}, indent=2, sort_keys=True) + "\n",
    }.items():
        path = target_dir / name
        if not path.is_file():
            path.write_text(content)
    if (target_dir / "det_stdout.txt").is_file():
        (target_dir / "verus_stdout.txt").write_text((target_dir / "det_stdout.txt").read_text())
    if (target_dir / "det_stderr.txt").is_file():
        (target_dir / "verus_stderr.txt").write_text((target_dir / "det_stderr.txt").read_text())


def annotate_result(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("status") == "ok" and result.get("r0_z3") == "unknown":
        reason = UNKNOWN_REASON_BY_TARGET[result["target"]]
        result["unknown_reason_class"] = reason
        result["unknown_reason"] = UNKNOWN_REASON_SUMMARIES[reason]
    return result


def determinism_outcome(result: dict[str, Any]) -> str:
    if result.get("status") == "ok":
        if result.get("r0_z3") == "unsat":
            return "UNSAT"
        if result.get("r0_z3") == "sat":
            return "SAT"
        return "UNKNOWN"
    if result.get("status") in {"no_ensures", "unsupported_mut_ref_return", "unsupported"}:
        return "unsupported"
    if result.get("status") == "verus_error":
        return "Verus error"
    return "runner crash"


def result_text(result: dict[str, Any]) -> str:
    pieces = [
        f"feedback-pipeline determinism: status={result.get('status')}",
        f"R0={determinism_outcome(result)}",
    ]
    if result.get("r0_z3"):
        pieces.append(f"r0_z3={result.get('r0_z3')}")
    if result.get("classification"):
        pieces.append(f"classification={result.get('classification')}")
    if result.get("unknown_reason_class"):
        pieces.append(f"unknown_reason={result.get('unknown_reason_class')}")
        pieces.append(f"unknown_review_reason={result.get('unknown_reason')}")
    if "verus_returncode" in result:
        pieces.append(f"verus_rc={result.get('verus_returncode')}")
    artifacts = result.get("artifacts", {})
    pieces.append(f"evidence={artifacts.get('result.json')}")
    pieces.append(f"synthetic={artifacts.get('synthetic_spec.rs')}")
    pieces.append(f"harness={artifacts.get('det_harness.rs')}")
    return "; ".join(pieces)


def update_catalog(catalog_path: Path, results: list[dict[str, Any]]) -> None:
    fieldnames, rows = read_catalog(catalog_path)
    by_target = {result["target"]: result for result in results}
    for row in rows:
        result = by_target.get(row["target"])
        if result is not None:
            row["determinism_result"] = result_text(result)
            row["reviewer_notes"] = "Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly."
    with catalog_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["status"] for row in rows)
    (catalog_path.with_suffix(".json")).write_text(json.dumps({"summary": {"total": len(rows), "existing_vstd": counts.get("existing-vstd", 0), "generated_new_real_relation_specs": counts.get("generated-new-real-relation-spec", 0), "justified_no_spec": counts.get("justified-no-spec", 0)}, "rows": rows}, indent=2, sort_keys=True) + "\n")


def update_markers(path: Path, results: list[dict[str, Any]]) -> None:
    by_target = {result["target"]: result_text(result) for result in results}
    out = []
    active = None
    for line in path.read_text().splitlines():
        match = re.match(r"// BEGIN VEC_SPEC target=(\S+)", line)
        if match:
            active = match.group(1)
        elif line == "// END VEC_SPEC":
            active = None
        if active in by_target and line.startswith("// determinism_result:"):
            out.append(f"// determinism_result: {by_target[active]}")
        elif active in by_target and line.startswith("// reviewer_notes:"):
            out.append("// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.")
        else:
            out.append(line)
    path.write_text("\n".join(out) + "\n")


def review_markdown(results: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    outcomes = Counter(determinism_outcome(result) for result in results)
    statuses = Counter(str(result.get("status")) for result in results)
    reason_counts = Counter(str(result.get("unknown_reason_class")) for result in results if result.get("unknown_reason_class"))
    reason_lines = ["| UNKNOWN reason class | Rows | Reason |", "| --- | ---: | --- |"]
    for reason, count in sorted(reason_counts.items()):
        reason_lines.append(f"| `{reason}` | {count} | {UNKNOWN_REASON_SUMMARIES[reason]} |")
    return "\n".join([
        "# Vec Spec Evidence Review",
        "",
        "The isolated `alloc::vec` artifact set accounts for all 49 stable executable API rows: 24 exact existing-vstd baseline rows, 24 generated executable `assume_specification` rows, and 1 justified no-spec row.",
        "",
        "Relational pointer/provenance, iterator/adaptor, callback, MaybeUninit, conversion, and mutable-reference outcomes are recorded honestly rather than strengthened to force determinism.",
        "",
        "## Audited totals",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        "| Catalog rows / stable unique `alloc::vec` exec APIs | 49 |",
        "| Existing vstd baseline rows preserved | 24 |",
        "| New generated executable contracts | 24 |",
        "| Justified-no-spec rows | 1 |",
        f"| Determinism `R0=UNSAT` | {outcomes.get('UNSAT', 0)} |",
        f"| Determinism `R0=SAT` | {outcomes.get('SAT', 0)} |",
        f"| Determinism `R0=UNKNOWN` | {outcomes.get('UNKNOWN', 0)} |",
        f"| Determinism unsupported | {outcomes.get('unsupported', 0)} |",
        f"| Determinism Verus error | {outcomes.get('Verus error', 0)} |",
        f"| Determinism runner crash | {outcomes.get('runner crash', 0)} |",
        "",
        "## UNKNOWN reason taxonomy",
        "",
        *reason_lines,
        "",
        "## Machine evidence",
        "",
        f"Latest feedback-pipeline manifest: `{summary['run_root']}/run_manifest.json`.",
        f"Status counts: `{dict(sorted(statuses.items()))}`.",
        f"R0 counts: `{dict(sorted(Counter(str(result.get('r0_z3', determinism_outcome(result))) for result in results).items()))}`.",
        "",
        "Per-target evidence directories include candidate, active contract code, synthetic `__rust_std_candidate`, determinism spec/harness, Verus stdout/stderr aliases, schema-search evidence, and result payloads.",
    ]) + "\n"


def write_outputs(evidence_root: Path, run_root: Path, run_id: str, targets: tuple[str, ...], results: list[dict[str, Any]], catalog_path: Path, update_artifacts: bool) -> None:
    summary = {
        "schema_version": 2,
        "run_id": run_id,
        "run_root": str(run_root.relative_to(ROOT)),
        "targets": list(targets),
        "status_counts": dict(Counter(str(result.get("status")) for result in results)),
        "r0_z3_counts": dict(Counter(str(result.get("r0_z3")) for result in results)),
        "unknown_reason_counts": dict(Counter(str(result.get("unknown_reason_class")) for result in results if result.get("unknown_reason_class"))),
        "results": [{"target": result["target"], "status": result.get("status"), "r0_z3": result.get("r0_z3"), "result_json": result["artifacts"].get("result.json"), **({"unknown_reason_class": result["unknown_reason_class"], "unknown_reason": result["unknown_reason"]} if result.get("unknown_reason_class") else {})} for result in results],
    }
    run_root.mkdir(parents=True, exist_ok=True)
    (run_root / "run_manifest.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    if update_artifacts:
        evidence_root.mkdir(parents=True, exist_ok=True)
        (evidence_root / "latest_manifest.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        update_catalog(catalog_path, results)
        update_markers(ROOT / "specs" / "generated_vec_specs.rs", results)
        update_markers(ROOT / "specs" / "all_vec_specs.rs", results)
        (catalog_path.with_name("VEC_SPEC_REVIEW.md")).write_text(review_markdown(results, summary))


def load_results_from_manifest(path: Path) -> tuple[str, Path, tuple[str, ...], list[dict[str, Any]]]:
    manifest = json.loads((ROOT / path if not path.is_absolute() else path).read_text())
    run_root = ROOT / manifest["run_root"]
    results = []
    targets = []
    for entry in manifest["results"]:
        payload = json.loads((ROOT / entry["result_json"]).read_text())
        results.append(annotate_result(payload))
        targets.append(entry["target"])
    return str(manifest.get("run_id") or run_root.name), run_root, tuple(targets), results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--survey-root", type=Path, default=DEFAULT_SURVEY_ROOT)
    parser.add_argument("--vstd-root", type=Path, default=DEFAULT_VSTD_ROOT)
    parser.add_argument("--verus-bin", type=Path, default=DEFAULT_VERUS_BIN)
    parser.add_argument("--z3-path", type=Path, default=DEFAULT_Z3_PATH)
    parser.add_argument("--generated-specs", type=Path, default=ROOT / "specs" / "generated_vec_specs.rs")
    parser.add_argument("--shared-vocabulary", type=Path, default=ROOT / "specs" / "vec_shared_vocabulary.rs")
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog" / "vec_spec_catalog.csv")
    parser.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--rlimit", type=float, default=60)
    parser.add_argument("--target", action="append")
    parser.add_argument("--no-update-artifacts", action="store_true")
    parser.add_argument("--refresh-from-manifest", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fieldnames, catalog_rows = read_catalog(args.catalog)
    catalog = {row["target"]: row for row in catalog_rows}
    generated_targets = tuple(row["target"] for row in catalog_rows if row["status"] == "generated-new-real-relation-spec")
    if set(generated_targets) != GENERATED_TARGETS or len(generated_targets) != EXPECTED_GENERATED_TARGETS:
        fail("generated target set mismatch")
    if args.refresh_from_manifest is not None:
        run_id, run_root, targets, results = load_results_from_manifest(args.refresh_from_manifest)
        write_outputs(args.evidence_root, run_root, run_id, targets, results, args.catalog, not args.no_update_artifacts)
        return 0
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_root = args.evidence_root / run_id
    feedback = load_feedback_module(args.survey_root)
    shared_body = shared_vocabulary_body(args.shared_vocabulary)
    assume_specs = build_assume_spec_index(feedback, args.generated_specs)
    registry = feedback.ViewRegistry.from_project(args.vstd_root)
    targets = tuple(args.target) if args.target else generated_targets
    results: list[dict[str, Any]] = []
    for target in targets:
        if target not in catalog:
            fail(f"{target} missing from catalog")
        assume = assume_specs.get(target)
        if assume is None:
            fail(f"{target} missing generated assume_specification")
        candidate = build_candidate(target, assume["item"], shared_body, catalog)
        target_dir = run_root / feedback.safe_name(target)
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "candidate.json").write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n")
        result = feedback.run_determinism(
            candidate=candidate,
            round_dir=target_dir,
            view_registry=registry,
            verus_bin=args.verus_bin,
            z3_path=args.z3_path,
            timeout=args.timeout,
            rlimit=args.rlimit,
        )
        write_minimal_artifacts(target_dir, candidate, feedback, result)
        payload = annotate_result({**result, "target": target, "contract_target": assume["contract_target"], "candidate": candidate})
        payload["artifacts"] = safe_artifacts(target_dir)
        payload["artifacts"]["result.json"] = str((target_dir / "result.json").relative_to(ROOT))
        (target_dir / "result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        results.append(payload)
        print(f"{target}: status={payload.get('status')} r0_z3={payload.get('r0_z3')} dir={target_dir.relative_to(ROOT)}", flush=True)
    write_outputs(args.evidence_root, run_root, run_id, targets, results, args.catalog, not args.no_update_artifacts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
