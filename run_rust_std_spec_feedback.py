#!/usr/bin/env python3
"""Generate missing Rust std contracts and run Verus determinism feedback."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import logging
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback
from typing import Any


SPEC_DET_ROOT = Path("/home/chentianyu/intent_formalization/spec-determinism")
sys.path.insert(0, str(SPEC_DET_ROOT))

from spec_determinism.classify import classify_ok
from spec_determinism.codegen.equal_policy import EqualPolicy
from spec_determinism.codegen.gen_det import build_det_check_spec
from spec_determinism.extract.extractor import extract_spec
from spec_determinism.schema_search import enumerate_schemas, render_guarded_template
from spec_determinism.schema_search.search import build_schema_ctx, run_schema_search
from spec_determinism.view.registry import ViewRegistry


GENERATION_PROMPT = """\
You are proposing a trusted Verus contract for one Rust standard-library API
used by Nanvix but not currently covered by Verus vstd.

Target:
```json
{target_summary}
```

Rust 1.96 declaration metadata used by the current Verus toolchain:
```json
{verification_declaration}
```

Rust 1.96 source context:
```rust
{verification_source}
```

Nanvix's Rust 1.99 source context:
```rust
{nanvix_source}
```

Related existing vstd contracts:
```rust
{vstd_context}
```

Return JSON only:
{{
  "decision": "add_spec" | "skip",
  "contract_form": "assume_specification" | "external_trait_specification",
  "contract_code": "complete Verus declaration(s), without a verus! wrapper",
  "requires": ["Verus boolean expression", "..."],
  "ensures": ["Verus boolean expression", "..."],
  "feature_gates": ["allocator_api", "..."],
  "imports": ["core::...", "alloc::...", "vstd::..."],
  "useful": true | false,
  "rationale": "short explanation grounded in the supplied source",
  "risks": ["..."]
}}

Rules:
- Do not edit files.
- A Rust external contract is trusted: determinism does not establish soundness.
  Only state facts justified by the supplied Rust implementation or docs.
- Use the exact Rust 1.96 signature. For a non-unit return, bind the result by
  name so the ensures clauses can reference it.
- Preserve impl-level and method-level bounds exactly, including repeated bounds
  that `assume_specification` signature matching may require.
- Every mutable-reference parameter must use `old(x)` or `final(x)` in clauses;
  never write a bare `x@` for an `&mut` parameter.
- Use fully qualified Rust paths where practical.
- Do not add `cfg` or `cfg_attr` attributes; the runner validates the contract
  unconditionally.
- Use existing public vstd specification vocabulary. Do not invent access to
  private fields or hidden runtime state.
- Do not use `true`, `false`, `arbitrary()`, `assume`, `requires false`, or a
  postcondition that merely repeats a precondition.
- Distinguish semantic views from pointer/reference identity.
- If a useful relation only holds under an existing law such as
  `obeys_cmp::<T>()`, make that law a `requires` clause rather than leaving the
  other branch unconstrained behind an implication.
- For I/O, OS, formatting, synchronization, allocation, nondeterministic, or
  hidden-state APIs, choose skip unless a useful sound result relation is
  expressible without modeling hidden state.
- For trait methods, use external_trait_specification only if a complete,
  typecheckable declaration can be given; otherwise choose skip.
- If no useful non-vacuous contract is expressible, choose skip and leave
  contract_code/requires/ensures empty.
"""


FEEDBACK_PROMPT = """\
Revise a proposed trusted Verus contract after typechecking and determinism
feedback.

Target: {target}

Previous proposal:
```json
{candidate}
```

Checker result:
```json
{checker}
```

Semantic and anti-vacuity issues:
```json
{issues}
```

Rust 1.96 declaration/source:
```json
{verification_declaration}
```
```rust
{verification_source}
```

Return JSON only with the same schema as before.

Do not optimize merely for `R0 = unsat`. The declaration must first typecheck,
remain source-justified, use an observable semantic output, and avoid false or
redundant domains. Choose skip when the API cannot receive a useful ordinary
contract in existing vstd vocabulary.
"""


def safe_name(path: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", path).strip("_")


def call_copilot(
    *,
    prompt: str,
    model: str,
    copilot_bin: str,
    timeout: int,
    cwd: Path,
    retries: int,
) -> str:
    command = [
        copilot_bin,
        "--model",
        model,
        "-s",
        "--no-auto-update",
        "--allow-all-tools",
        "--allow-all-paths",
        "-p",
        prompt,
    ]
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            process = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if process.returncode == 0:
                return process.stdout
            last_error = RuntimeError(
                process.stderr.strip()
                or f"copilot exited {process.returncode}"
            )
        except subprocess.TimeoutExpired as error:
            last_error = error
        if attempt < retries:
            time.sleep(2)
    assert last_error is not None
    raise last_error


def parse_json_response(text: str) -> dict[str, Any]:
    blocks = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL)
    candidates = list(reversed(blocks)) + [text]
    decoder = json.JSONDecoder()
    for candidate in candidates:
        candidate = candidate.strip()
        try:
            value = json.loads(candidate)
            if isinstance(value, dict):
                return value
        except json.JSONDecodeError:
            pass
        for match in re.finditer(r"\{", candidate):
            try:
                value, _ = decoder.raw_decode(candidate[match.start() :])
                if isinstance(value, dict):
                    return value
            except json.JSONDecodeError:
                continue
    raise ValueError("Copilot response did not contain valid JSON")


def strip_code_fences(text: str) -> str:
    text = text.strip()
    match = re.fullmatch(r"```(?:rust)?\s*(.*?)```", text, flags=re.DOTALL)
    return match.group(1).strip() if match else text


def sanitize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    result = dict(candidate)
    result["decision"] = str(result.get("decision", "")).strip()
    result["contract_form"] = str(result.get("contract_form", "")).strip()
    result["contract_code"] = strip_code_fences(
        str(result.get("contract_code", ""))
    )
    for key in ("requires", "ensures", "feature_gates", "imports", "risks"):
        value = result.get(key) or []
        if not isinstance(value, list):
            value = [value]
        result[key] = [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]
    return result


def common_prefix_length(left: str, right: str) -> int:
    left_parts = left.split("::")
    right_parts = right.split("::")
    count = 0
    for lhs, rhs in zip(left_parts, right_parts):
        if lhs != rhs:
            break
        count += 1
    return count


def related_vstd_context(
    target: str,
    contracts: list[dict[str, Any]],
    vstd_root: Path,
) -> str:
    scored = sorted(
        contracts,
        key=lambda row: (
            common_prefix_length(target, row["api_path"]),
            row["api_path"] == target,
        ),
        reverse=True,
    )
    blocks: list[str] = []
    seen: set[tuple[str, int]] = set()
    for row in scored:
        score = common_prefix_length(target, row["api_path"])
        if score < 2:
            break
        key = (row["source_file"], int(row["source_line"]))
        if key in seen:
            continue
        seen.add(key)
        path = vstd_root / row["source_file"]
        if not path.is_file():
            continue
        lines = path.read_text(errors="replace").splitlines()
        line = key[1]
        start = max(1, line - 10)
        end = min(len(lines), line + 18)
        block = [
            f"// {row['api_path']} — {row['source_file']}:{line}",
            *[
                f"{number:>6}: {lines[number - 1]}"
                for number in range(start, end + 1)
            ],
        ]
        blocks.append("\n".join(block))
        if len(blocks) >= 4:
            break
    return "\n\n".join(blocks) if blocks else "// No closely related vstd contract."


def target_summary(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "target": entry["target"],
        "category": entry["category"],
        "kinds": entry["kinds"],
        "modules": entry["modules"],
        "semantic_risks": entry["semantic_risks"],
        "classification": entry.get("classification"),
        "classification_reasons": entry.get("classification_reasons", []),
        "recommended_contract_form": entry["recommended_contract_form"],
        "available_in_verus_rust_1_96": entry["available_in_verus_rust_1_96"],
        "declaration_count": entry["declaration_count"],
        "verification_declaration_count": entry["verification_declaration_count"],
    }


def selected_declaration(entry: dict[str, Any], verification: bool) -> dict[str, Any]:
    key = "verification_declarations" if verification else "declarations"
    declarations = entry.get(key) or []
    return declarations[0] if declarations else {}


def prompt_for(
    entry: dict[str, Any],
    contracts: list[dict[str, Any]],
    vstd_root: Path,
) -> str:
    verification = selected_declaration(entry, True)
    nanvix = selected_declaration(entry, False)
    return GENERATION_PROMPT.format(
        target_summary=json.dumps(target_summary(entry), indent=2),
        verification_declaration=json.dumps(
            {
                key: value
                for key, value in verification.items()
                if key != "source_context"
            },
            indent=2,
        ),
        verification_source=verification.get("source_context", ""),
        nanvix_source=nanvix.get("source_context", ""),
        vstd_context=related_vstd_context(entry["target"], contracts, vstd_root),
    )


def feature_attributes(candidate: dict[str, Any]) -> str:
    features = []
    for feature in candidate.get("feature_gates") or []:
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", feature):
            features.append(feature)
    return "".join(f"#![feature({feature})]\n" for feature in sorted(set(features)))


def import_lines(candidate: dict[str, Any]) -> str:
    imports = []
    for path in candidate.get("imports") or []:
        path = path.removeprefix("use ").removesuffix(";").strip()
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_:*{} ,<>]*", path):
            imports.append(path)
    return "".join(f"use {path};\n" for path in sorted(set(imports)))


def build_contract_harness(candidate: dict[str, Any]) -> str:
    code = active_contract_code(candidate)
    return (
        "#![allow(unused_imports, dead_code)]\n"
        f"{feature_attributes(candidate)}"
        "extern crate alloc;\n"
        "use vstd::prelude::*;\n"
        f"{import_lines(candidate)}\n"
        "verus! {\n"
        f"{code}\n"
        "}\n\n"
        "fn main() {}\n"
    )


def active_contract_code(candidate: dict[str, Any]) -> str:
    code = candidate["contract_code"].strip()
    code = re.sub(
        r"(?m)^[ \t]*#\s*\[(?:cfg|cfg_attr)\b[^\n]*\][ \t]*\n?",
        "",
        code,
    )
    return code.strip()


def run_verus(
    *,
    verus_bin: Path,
    z3_path: Path,
    file_path: Path,
    timeout: int,
    rlimit: float,
    log_dir: Path | None = None,
    verify_function: str | None = None,
) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["RUSTC_BOOTSTRAP"] = "1"
    environment["VERUS_Z3_PATH"] = str(z3_path)
    rust_lib = (
        Path.home()
        / ".rustup"
        / "toolchains"
        / "1.96.0-x86_64-unknown-linux-gnu"
        / "lib"
    )
    environment["LD_LIBRARY_PATH"] = (
        str(rust_lib) + ":" + environment.get("LD_LIBRARY_PATH", "")
    )
    command = [str(verus_bin), str(file_path), "--rlimit", str(rlimit)]
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        command += ["--log-all", "--log-dir", str(log_dir)]
    if verify_function is not None:
        command += ["--verify-root", "--verify-function", verify_function]
    started = time.monotonic()
    try:
        process = subprocess.run(
            command,
            env=environment,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "returncode": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "duration_ms": int((time.monotonic() - started) * 1000),
            "command": command,
        }
    except subprocess.TimeoutExpired as error:
        return {
            "returncode": -1,
            "stdout": error.stdout or "",
            "stderr": (error.stderr or "") + f"\n[timeout after {timeout}s]",
            "duration_ms": int((time.monotonic() - started) * 1000),
            "command": command,
        }


def matching_delimiter(text: str, start: int, opening: str, closing: str) -> int:
    depth = 0
    for index in range(start, len(text)):
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            if closing == ">" and index > 0 and text[index - 1] == "-":
                continue
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"unclosed {opening}")


def assume_to_synthetic(contract_code: str) -> str:
    match = re.search(r"\bassume_specification\b", contract_code)
    if match is None:
        raise ValueError("contract_code has no assume_specification")
    cursor = match.end()
    while cursor < len(contract_code) and contract_code[cursor].isspace():
        cursor += 1
    generics = ""
    if cursor < len(contract_code) and contract_code[cursor] == "<":
        end = matching_delimiter(contract_code, cursor, "<", ">")
        generics = contract_code[cursor : end + 1]
        cursor = end + 1
    while cursor < len(contract_code) and contract_code[cursor].isspace():
        cursor += 1
    if cursor >= len(contract_code) or contract_code[cursor] != "[":
        raise ValueError("assume_specification target bracket not found")
    target_end = matching_delimiter(contract_code, cursor, "[", "]")
    rest_start = target_end + 1

    paren = bracket = brace = 0
    semicolon = None
    for index in range(rest_start, len(contract_code)):
        char = contract_code[index]
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
        raise ValueError("assume_specification terminator not found")
    rest = contract_code[rest_start:semicolon].strip()
    return (
        f"pub exec fn __rust_std_candidate{generics}{rest}\n"
        "    { loop { } }\n"
    )


def equal_fn_is_trivial(equal_fn_def: str) -> bool:
    match = re.search(
        r"->\s*bool\s*\{(?P<body>.*)\}\s*$",
        equal_fn_def,
        flags=re.DOTALL,
    )
    if not match:
        return False
    body = re.sub(r"/\*.*?\*/", "", match.group("body"), flags=re.DOTALL)
    body = re.sub(r"//.*", "", body)
    body = re.sub(r"[\s()]", "", body)
    return body == "true"


def build_det_harness(
    candidate: dict[str, Any],
    det_spec: Any,
    schemas: list[Any],
) -> str:
    body = det_spec.equal_fn_def + "\n\n" + render_guarded_template(
        det_spec,
        schemas,
    )
    for spec_name in det_spec.opened_closed_specs:
        body = re.sub(
            rf"^[ \t]*reveal\((?:[A-Za-z_][A-Za-z0-9_]*::)*"
            rf"{re.escape(spec_name)}\);[ \t]*\n?",
            "",
            body,
            flags=re.MULTILINE,
        )
    return (
        "#![allow(unused_imports, dead_code)]\n"
        f"{feature_attributes(candidate)}"
        "extern crate alloc;\n"
        "use vstd::prelude::*;\n"
        f"{import_lines(candidate)}\n"
        "verus! {\n"
        f"{body}\n"
        "}\n\n"
        "fn main() {}\n"
    )


def run_determinism(
    *,
    candidate: dict[str, Any],
    round_dir: Path,
    view_registry: ViewRegistry,
    verus_bin: Path,
    z3_path: Path,
    timeout: int,
    rlimit: float,
) -> dict[str, Any]:
    result: dict[str, Any] = {"status": "runner_crash"}
    try:
        synthetic_fn = assume_to_synthetic(active_contract_code(candidate))
        synthetic_source = (
            "#![allow(unused_imports)]\n"
            f"{feature_attributes(candidate)}"
            "extern crate alloc;\n"
            "use vstd::prelude::*;\n"
            f"{import_lines(candidate)}\n"
            "verus! {\n"
            f"{synthetic_fn}"
            "}\n"
        )
        (round_dir / "synthetic_spec.rs").write_text(synthetic_source)
        spec = extract_spec(
            synthetic_source,
            "__rust_std_candidate",
            type_sources=[synthetic_source],
        )
        result["requires"] = list(spec.requires)
        result["ensures"] = list(spec.ensures)
        if not spec.ensures:
            result["status"] = "no_ensures"
            return result
        if spec.return_type.name.strip().startswith("&mut "):
            result["status"] = "unsupported_mut_ref_return"
            return result

        det_spec = build_det_check_spec(
            spec,
            source=synthetic_source,
            equal_policy=EqualPolicy(
                compare_raw_pointers=False,
                source="rust_std_specgen",
            ),
            view_registry=view_registry,
        )
        schemas = enumerate_schemas(det_spec)
        harness = build_det_harness(candidate, det_spec, schemas)
        harness_path = round_dir / "det_harness.rs"
        harness_path.write_text(harness)
        (round_dir / "det_spec.json").write_text(det_spec.to_json())
        result["det_function"] = det_spec.check_fn_name
        result["equal_fn_trivial"] = equal_fn_is_trivial(det_spec.equal_fn_def)
        result["n_schemas"] = len(schemas)

        log_dir = round_dir / "verus_log"
        raw = run_verus(
            verus_bin=verus_bin,
            z3_path=z3_path,
            file_path=harness_path,
            timeout=timeout,
            rlimit=rlimit,
            log_dir=log_dir,
            verify_function=det_spec.check_fn_name,
        )
        result["verus_returncode"] = raw["returncode"]
        result["verus_ms"] = raw["duration_ms"]
        (round_dir / "det_stdout.txt").write_text(raw["stdout"])
        (round_dir / "det_stderr.txt").write_text(raw["stderr"])
        if raw["returncode"] != 0:
            stderr = raw["stderr"]
            expected = (
                "postcondition not satisfied" in stderr
                or "assertion failed" in stderr.lower()
            )
            if not expected and "error:" in stderr:
                result["status"] = "verus_error"
                result["stderr_tail"] = stderr[-4000:]
                return result

        smt2_candidates = sorted(
            log_dir.rglob("*.smt2"),
            key=lambda path: path.stat().st_size,
        )
        if not smt2_candidates:
            result["status"] = "no_smt2"
            return result
        smt2 = smt2_candidates[-1]
        schema_ctx = build_schema_ctx(
            smt2,
            det_spec.check_fn_name,
            schemas,
            safe_name(det_spec.check_fn_name),
        )
        witness = run_schema_search(det_spec, schema_ctx)
        result["r0_z3"] = witness.r0_z3
        result["n_rounds"] = len(witness.trace or [])
        result["assumes"] = [
            assume.expression for assume in (witness.assumes or [])
        ]
        result["status"] = "ok"
        result["permitted"] = False
        raw_classification = classify_ok(result)
        result["classification"] = (
            "invalid_equal_fn_trivial"
            if result["equal_fn_trivial"]
            else raw_classification
        )
        return result
    except Exception as error:
        result["error"] = (
            f"{type(error).__name__}: {error}\n"
            f"{traceback.format_exc()[-4000:]}"
        )
        return result


def normalize_expr(expression: str) -> str:
    normalized = re.sub(r"\s+", "", expression).strip("()")
    return re.sub(r",(?=\))", "", normalized)


def anti_vacuity_issues(
    entry: dict[str, Any],
    candidate: dict[str, Any],
    typecheck: dict[str, Any] | None,
    checker: dict[str, Any] | None,
) -> list[str]:
    issues: list[str] = []
    if entry.get("classification") not in {None, "suitable_now"}:
        issues.append(f"classification:{entry.get('classification')}")
    ensures = [
        expression
        for expression in candidate.get("ensures") or []
        if expression.strip()
    ]
    requires = [
        expression
        for expression in candidate.get("requires") or []
        if expression.strip()
    ]
    normalized_ensures = {normalize_expr(expression) for expression in ensures}
    normalized_requires = {normalize_expr(expression) for expression in requires}
    if candidate.get("decision") == "add_spec":
        if not candidate.get("contract_code"):
            issues.append("missing_contract_code")
        if not ensures:
            issues.append("no_candidate_postcondition")
        if normalized_ensures & {"true", "false"}:
            issues.append("constant_postcondition")
        if "false" in normalized_requires:
            issues.append("false_precondition")
        if normalized_ensures and normalized_ensures <= normalized_requires:
            issues.append("postcondition_implied_by_requires")
    if not entry.get("available_in_verus_rust_1_96"):
        issues.append("not_in_verus_rust_1_96")
    if not any(
        declaration["observability"]["has_modeled_output"]
        for declaration in entry.get("verification_declarations") or []
    ):
        issues.append("no_modeled_observable_output")
    if typecheck is not None and typecheck.get("returncode") != 0:
        issues.append("contract_typecheck_failed")
    if candidate.get("contract_form") != "assume_specification":
        issues.append("determinism_unsupported_contract_form")
    if checker is not None:
        checker_requires = {
            normalize_expr(expression)
            for expression in checker.get("requires", [])
        }
        checker_ensures = {
            normalize_expr(expression)
            for expression in checker.get("ensures", [])
        }
        if (
            checker_requires != normalized_requires
            or checker_ensures != normalized_ensures
        ):
            issues.append("structured_contract_mismatch")
        if checker.get("status") != "ok":
            issues.append(f"checker_status:{checker.get('status')}")
        elif checker.get("r0_z3") != "unsat":
            issues.append(f"determinism_not_proved:{checker.get('r0_z3')}")
        if checker.get("equal_fn_trivial"):
            issues.append("trivial_equal_fn")
    return sorted(set(issues))


def checker_summary(
    typecheck: dict[str, Any] | None,
    checker: dict[str, Any] | None,
) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    if typecheck is not None:
        summary["typecheck"] = {
            "returncode": typecheck.get("returncode"),
            "duration_ms": typecheck.get("duration_ms"),
            "stderr_tail": (typecheck.get("stderr") or "")[-4000:],
        }
    if checker is not None:
        keys = (
            "status",
            "r0_z3",
            "classification",
            "requires",
            "ensures",
            "equal_fn_trivial",
            "stderr_tail",
            "error",
        )
        summary["determinism"] = {
            key: checker[key]
            for key in keys
            if key in checker
        }
    return summary or {"status": "not_run"}


def run_one(
    *,
    entry: dict[str, Any],
    contracts: list[dict[str, Any]],
    vstd_root: Path,
    out_root: Path,
    view_registry: ViewRegistry,
    verus_bin: Path,
    z3_path: Path,
    model: str,
    copilot_bin: str,
    llm_timeout: int,
    llm_retries: int,
    check_timeout: int,
    rlimit: float,
    feedback_rounds: int,
    seed_candidate: dict[str, Any] | None,
    include_non_suitable: bool,
    include_unavailable: bool,
) -> dict[str, Any]:
    target_dir = out_root / "targets" / safe_name(entry["target"])
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "target.json").write_text(
        json.dumps(entry, indent=2, sort_keys=True) + "\n"
    )

    if (
        not entry.get("available_in_verus_rust_1_96")
        and not include_unavailable
    ):
        result = {
            "target": entry["target"],
            "category": entry["category"],
            "history": [],
            "final": {
                "status": "static_skip",
                "decision": "skip",
                "issues": ["not_in_verus_rust_1_96"],
            },
        }
        (target_dir / "summary.json").write_text(
            json.dumps(result, indent=2) + "\n"
        )
        return result
    if (
        entry.get("classification") not in {None, "suitable_now"}
        and not include_non_suitable
    ):
        result = {
            "target": entry["target"],
            "category": entry["category"],
            "history": [],
            "final": {
                "status": "static_skip",
                "decision": "skip",
                "issues": [f"classification:{entry.get('classification')}"],
            },
        }
        (target_dir / "summary.json").write_text(
            json.dumps(result, indent=2) + "\n"
        )
        return result

    prompt = prompt_for(entry, contracts, vstd_root)
    history = []
    verification = selected_declaration(entry, True)
    for round_index in range(feedback_rounds + 1):
        round_dir = target_dir / f"round_{round_index:02d}"
        round_dir.mkdir(exist_ok=True)
        (round_dir / "prompt.md").write_text(prompt)
        if round_index == 0 and seed_candidate is not None:
            llm_ms = 0
            candidate = sanitize_candidate(seed_candidate)
            (round_dir / "candidate.json").write_text(
                json.dumps(candidate, indent=2) + "\n"
            )
            (round_dir / "response.txt").write_text(
                "[seeded from batch first-pass generation]\n"
            )
        else:
            started = time.monotonic()
            try:
                response = call_copilot(
                    prompt=prompt,
                    model=model,
                    copilot_bin=copilot_bin,
                    timeout=llm_timeout,
                    cwd=round_dir,
                    retries=llm_retries,
                )
                llm_ms = int((time.monotonic() - started) * 1000)
                (round_dir / "response.txt").write_text(response)
                candidate = sanitize_candidate(parse_json_response(response))
                (round_dir / "candidate.json").write_text(
                    json.dumps(candidate, indent=2) + "\n"
                )
            except Exception as error:
                record = {
                    "round": round_index,
                    "status": "llm_error",
                    "error": f"{type(error).__name__}: {error}",
                }
                history.append(record)
                break

        typecheck = None
        checker = None
        if (
            candidate.get("decision") == "add_spec"
            and candidate.get("contract_code")
            and entry.get("available_in_verus_rust_1_96")
        ):
            contract_harness = build_contract_harness(candidate)
            contract_path = round_dir / "contract_harness.rs"
            contract_path.write_text(contract_harness)
            typecheck = run_verus(
                verus_bin=verus_bin,
                z3_path=z3_path,
                file_path=contract_path,
                timeout=check_timeout,
                rlimit=rlimit,
            )
            (round_dir / "typecheck_stdout.txt").write_text(typecheck["stdout"])
            (round_dir / "typecheck_stderr.txt").write_text(typecheck["stderr"])
            if (
                typecheck["returncode"] == 0
                and candidate.get("contract_form") == "assume_specification"
            ):
                checker = run_determinism(
                    candidate=candidate,
                    round_dir=round_dir,
                    view_registry=view_registry,
                    verus_bin=verus_bin,
                    z3_path=z3_path,
                    timeout=check_timeout,
                    rlimit=rlimit,
                )

        issues = anti_vacuity_issues(entry, candidate, typecheck, checker)
        raw_reward = int(
            checker is not None
            and checker.get("status") == "ok"
            and checker.get("r0_z3") == "unsat"
        )
        guarded_reward = int(
            raw_reward == 1
            and typecheck is not None
            and typecheck.get("returncode") == 0
            and not issues
        )
        record = {
            "round": round_index,
            "llm_ms": llm_ms,
            "candidate": candidate,
            "checker": checker_summary(typecheck, checker),
            "anti_vacuity_issues": issues,
            "raw_det_reward": raw_reward,
            "guarded_reward": guarded_reward,
            "soundness_status": "unverified_trusted_external_contract",
            "apply_upstream": False,
        }
        history.append(record)
        (round_dir / "round_result.json").write_text(
            json.dumps(record, indent=2) + "\n"
        )
        if (
            candidate.get("decision") == "skip"
            or guarded_reward == 1
            or round_index >= feedback_rounds
        ):
            break
        prompt = FEEDBACK_PROMPT.format(
            target=entry["target"],
            candidate=json.dumps(candidate, indent=2),
            checker=json.dumps(checker_summary(typecheck, checker), indent=2),
            issues=json.dumps(issues, indent=2),
            verification_declaration=json.dumps(
                {
                    key: value
                    for key, value in verification.items()
                    if key != "source_context"
                },
                indent=2,
            ),
            verification_source=verification.get("source_context", ""),
        )

    final = history[-1] if history else {"status": "no_round"}
    result = {
        "target": entry["target"],
        "category": entry["category"],
        "history": history,
        "final": final,
    }
    (target_dir / "summary.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    return result


def write_batch_summary(
    out_dir: Path,
    results: list[dict[str, Any]],
    metadata: dict[str, Any],
) -> None:
    finals = []
    for result in results:
        final = result.get("final") or {}
        candidate = final.get("candidate") or {}
        finals.append(
            {
                "target": result["target"],
                "category": result.get("category", ""),
                "status": final.get("status", ""),
                "decision": candidate.get("decision", final.get("decision", "")),
                "contract_form": candidate.get("contract_form", ""),
                "useful_claim": candidate.get("useful"),
                "raw_det_reward": final.get("raw_det_reward", 0),
                "guarded_reward": final.get("guarded_reward", 0),
                "issues": final.get("anti_vacuity_issues", final.get("issues", [])),
                "soundness_status": final.get("soundness_status", ""),
            }
        )
    counts = {
        "targets": len(results),
        "add_spec": sum(item["decision"] == "add_spec" for item in finals),
        "skip": sum(item["decision"] == "skip" for item in finals),
        "raw_reward": sum(item["raw_det_reward"] for item in finals),
        "guarded_reward": sum(item["guarded_reward"] for item in finals),
        "static_skip": sum(item["status"] == "static_skip" for item in finals),
        "llm_errors": sum(item["status"] == "llm_error" for item in finals),
    }
    payload = {
        "metadata": metadata,
        "counts": counts,
        "results": results,
        "final_candidates": finals,
    }
    (out_dir / "batch_summary.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )
    lines = [
        "# Rust std missing-contract generation with determinism feedback",
        "",
        f"- Model: `{metadata['model']}`",
        f"- Targets: {counts['targets']}",
        f"- Add-spec decisions: {counts['add_spec']}",
        f"- Skip decisions: {counts['skip']}",
        f"- Static skips: {counts['static_skip']}",
        f"- Raw determinism reward: {counts['raw_reward']}",
        f"- Guarded reward: {counts['guarded_reward']}",
        f"- LLM errors: {counts['llm_errors']}",
        "- Soundness: external contracts remain unverified; no candidate is "
        "automatically eligible for upstream application.",
        "",
        "| Target | Category | Decision | Raw | Guarded | Issues |",
        "|---|---|---|---:|---:|---|",
    ]
    for item in sorted(finals, key=lambda value: value["target"]):
        lines.append(
            f"| `{item['target']}` | {item['category']} | {item['decision']} | "
            f"{item['raw_det_reward']} | {item['guarded_reward']} | "
            f"{', '.join(item['issues'])} |"
        )
    (out_dir / "SUMMARY.md").write_text("\n".join(lines).rstrip() + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument(
        "--manifest",
        type=Path,
        default=workspace / "specgen" / "pilot-manifest.json",
    )
    parser.add_argument(
        "--contracts",
        type=Path,
        default=workspace / "results" / "vstd_contracts.json",
    )
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
    parser.add_argument(
        "--out",
        type=Path,
        default=workspace / "specgen" / "pilot-gpt56sol",
    )
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--copilot-bin", default="copilot")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--include-non-suitable", action="store_true")
    parser.add_argument("--include-unavailable", action="store_true")
    parser.add_argument("--seed-candidates", type=Path)
    parser.add_argument("--feedback-rounds", type=int, default=2)
    parser.add_argument("--llm-timeout", type=int, default=420)
    parser.add_argument("--llm-retries", type=int, default=1)
    parser.add_argument("--check-timeout", type=int, default=240)
    parser.add_argument("--rlimit", type=float, default=60)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_payload = json.loads(args.manifest.read_text())
    entries = manifest_payload.get("targets", manifest_payload)
    if args.limit is not None:
        entries = entries[: args.limit]
    contracts = json.loads(args.contracts.read_text())
    seed_candidates = (
        json.loads(args.seed_candidates.read_text())
        if args.seed_candidates is not None
        else {}
    )
    args.out.mkdir(parents=True, exist_ok=True)
    logging.getLogger("spec_determinism").setLevel(logging.ERROR)
    view_registry = ViewRegistry.from_project(args.vstd_root)
    verus_version = subprocess.check_output(
        [str(args.verus_bin), "--version"],
        text=True,
    ).strip()
    metadata = {
        "model": args.model,
        "manifest": str(args.manifest.resolve()),
        "vstd_root": str(args.vstd_root.resolve()),
        "verus_bin": str(args.verus_bin.resolve()),
        "verus_version": verus_version,
        "feedback_rounds": args.feedback_rounds,
        "contract_soundness": "unverified_trusted_external_contract",
        "seed_candidates": (
            str(args.seed_candidates.resolve())
            if args.seed_candidates is not None
            else None
        ),
        "include_non_suitable": args.include_non_suitable,
        "include_unavailable": args.include_unavailable,
    }
    results = []
    pending_entries = []
    for entry in entries:
        summary_path = (
            args.out
            / "targets"
            / safe_name(entry["target"])
            / "summary.json"
        )
        if args.resume and summary_path.is_file():
            saved = json.loads(summary_path.read_text())
            final = saved.get("final") or {}
            if final.get("status") not in {"llm_error", "exception", "no_round"}:
                results.append(saved)
                continue
        pending_entries.append(entry)
    if results:
        print(f"resumed {len(results)} completed targets", flush=True)
        write_batch_summary(args.out, results, metadata)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(
                run_one,
                entry=entry,
                contracts=contracts,
                vstd_root=args.vstd_root,
                out_root=args.out,
                view_registry=view_registry,
                verus_bin=args.verus_bin,
                z3_path=args.z3_path,
                model=args.model,
                copilot_bin=args.copilot_bin,
                llm_timeout=args.llm_timeout,
                llm_retries=args.llm_retries,
                check_timeout=args.check_timeout,
                rlimit=args.rlimit,
                feedback_rounds=args.feedback_rounds,
                seed_candidate=seed_candidates.get(entry["target"]),
                include_non_suitable=args.include_non_suitable,
                include_unavailable=args.include_unavailable,
            ): entry
            for entry in pending_entries
        }
        for index, future in enumerate(as_completed(futures), start=1):
            entry = futures[future]
            try:
                result = future.result()
            except Exception as error:
                result = {
                    "target": entry["target"],
                    "category": entry["category"],
                    "history": [],
                    "final": {
                        "status": "exception",
                        "error": f"{type(error).__name__}: {error}",
                    },
                }
            results.append(result)
            final = result.get("final") or {}
            candidate = final.get("candidate") or {}
            print(
                f"[{len(results)}/{len(entries)}] {entry['target']} "
                f"decision={candidate.get('decision', final.get('decision'))} "
                f"raw={final.get('raw_det_reward', 0)} "
                f"guarded={final.get('guarded_reward', 0)}",
                flush=True,
            )
            write_batch_summary(args.out, results, metadata)
    write_batch_summary(args.out, results, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
