#!/usr/bin/env python3
"""Generate and verify source-level proofs for all remaining vstd contracts."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from typing import Any


HERE = Path(__file__).resolve().parent
SOURCE_VERIFICATION = HERE.parent
WORKSPACE = SOURCE_VERIFICATION.parent
sys.path.insert(0, str(WORKSPACE))

from run_rust_std_spec_feedback import parse_json_response, run_verus, strip_code_fences


GENERATION_PROMPT = """\
Copy or source-faithfully desugar one Rust 1.96 standard-library implementation
into an ordinary Verus function and prove the supplied vstd contract.

Target metadata:
```json
{metadata}
```

Current vstd contract:
```rust
{contract}
```

Rust 1.96 implementation:
```rust
{rust_source}
```

Fidelity retry context:
```text
{retry_context}
```

The contract's vstd module context:
```rust
{module_context}
```

Return JSON only:
{{
  "decision": "proved" | "blocked",
  "proof_file": "complete standalone Verus .rs file, or empty when blocked",
  "trust_level": "A" | "B" | "C" | "D" | "E",
  "trusted_assumptions": ["..."],
  "rationale": "short explanation",
  "blocker": "empty when proved"
}}

Requirements:
- The file must contain an ordinary exec `source_...` function with the target
  postcondition and a copied/source-faithful body. Add proof annotations.
- Never call the exact target function from the source function; that would
  circularly use the contract being proved. Calls to smaller std APIs are okay.
- Preserve the implementation's control flow. Desugar unsupported syntax such
  as slice patterns when needed.
- Use `vstd::prelude::*` and the suggested vstd module import. Add exact feature
  attributes and Rust imports required by the signature.
- Do not use `assume`, `admit`, `external_body`, or an empty proof body to hide
  an obligation. Explicit `axiom fn` declarations are allowed only for a real
  representation/compiler/target fact unavailable downstream; list each one.
- A/B/C/D/E mean the same as source-verification/SUMMARY.md.
- Include `fn main() {{}}`.
- If private representation makes a meaningful source proof impossible, return
  blocked instead of restating the target contract as an axiom.
- If the supplied Rust body is empty, use repository tools to locate the exact
  Rust 1.96 implementation, macro expansion, or trait default before deciding
  that no body is available.
"""


FEEDBACK_PROMPT = """\
Repair this source-level Verus proof.

Target: {target}

Previous response:
```json
{candidate}
```

Verus output:
```text
{diagnostic}
```

Return JSON only with the same schema. Preserve the Rust implementation logic,
do not call the exact target method, and do not hide the failed obligation with
`assume`, `admit`, `external_body`, or a target-contract axiom. Choose blocked
if the proof fundamentally requires private representation unavailable here.
"""


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", value).strip("_")


def call_copilot(
    prompt: str,
    model: str,
    copilot_bin: str,
    cwd: Path,
    timeout: int,
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
            last_error = RuntimeError(process.stderr.strip() or f"copilot exit {process.returncode}")
        except subprocess.TimeoutExpired as error:
            last_error = error
        if attempt < retries:
            time.sleep(2)
    assert last_error is not None
    raise last_error


def sanitize(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result["decision"] = str(result.get("decision", "")).strip()
    result["proof_file"] = strip_code_fences(str(result.get("proof_file", "")))
    result["trust_level"] = str(result.get("trust_level", "")).strip()
    assumptions = result.get("trusted_assumptions") or []
    if not isinstance(assumptions, list):
        assumptions = [assumptions]
    result["trusted_assumptions"] = [str(item).strip() for item in assumptions if str(item).strip()]
    result["rationale"] = str(result.get("rationale", "")).strip()
    result["blocker"] = str(result.get("blocker", "")).strip()
    return result


def selected_declaration(target: dict[str, Any]) -> dict[str, Any]:
    declarations = target.get("verification_declarations") or []
    for declaration in declarations:
        if declaration.get("has_body"):
            return declaration
    return declarations[0] if declarations else {}


def target_metadata(target: dict[str, Any]) -> dict[str, Any]:
    declaration = selected_declaration(target)
    return {
        "id": target["id"],
        "api_path": target["api_path"],
        "normalized_api_path": target["normalized_api_path"],
        "raw_target": target["raw_target"],
        "contract_source": (
            f"{target['contract_source_file']}:{target['contract_source_line']}"
        ),
        "suggested_vstd_import": target["suggested_vstd_import"],
        "rust_declaration": {
            key: value
            for key, value in declaration.items()
            if key not in {"source_context", "source_text"}
        },
    }


def circular_target_use(target: dict[str, Any], proof: str) -> bool:
    raw = re.sub(r"\s+", "", target["raw_target"])
    api_path = re.sub(r"\s+", "", target["normalized_api_path"])
    source_functions = re.findall(
        r"\b(?:pub\s+)?fn\s+(source_[A-Za-z0-9_]+)[^{]*\{(.*?)\n\}",
        proof,
        flags=re.DOTALL,
    )
    for _, body in source_functions:
        compact = re.sub(r"\s+", "", body)
        if raw and raw in compact:
            return True
        if api_path and api_path in compact:
            return True
    return False


def proof_policy_error(proof: str) -> str | None:
    if not re.search(r"\b(?:pub\s+)?fn\s+source_[A-Za-z0-9_]+\s*[<(]", proof):
        return "Proof file has no ordinary source_ exec function."
    forbidden = {
        r"\bassume\s*\(": "assume(...) is forbidden",
        r"\badmit\s*\(": "admit() is forbidden",
        r"external_body": "external_body is forbidden",
        r"\bunimplemented!\s*\(": "unimplemented!() is forbidden",
        r"\btodo!\s*\(": "todo!() is forbidden",
    }
    for pattern, message in forbidden.items():
        if re.search(pattern, proof):
            return message
    return None


def run_one(
    target: dict[str, Any],
    *,
    run_root: Path,
    proved_root: Path,
    model: str,
    copilot_bin: str,
    llm_timeout: int,
    llm_retries: int,
    feedback_rounds: int,
    check_timeout: int,
    rlimit: float,
    verus_bin: Path,
    z3_path: Path,
    attempt_no_body: bool,
) -> dict[str, Any]:
    target_dir = run_root / "targets" / target["id"]
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "target.json").write_text(json.dumps(target, indent=2) + "\n")
    declaration = selected_declaration(target)
    if not declaration.get("has_body") and not attempt_no_body:
        result = {
            "id": target["id"],
            "api_path": target["api_path"],
            "status": "blocked_no_rust_body",
            "decision": "blocked",
            "blocker": "Rust 1.96 rustdoc has no executable body for this declaration.",
            "history": [],
        }
        (target_dir / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
        return result

    prompt = GENERATION_PROMPT.format(
        metadata=json.dumps(target_metadata(target), indent=2),
        contract=target["contract_code"],
        rust_source=declaration.get("source_text", ""),
        retry_context=target.get(
            "fidelity_retry_context",
            "No additional fidelity-retry constraints.",
        ),
        module_context=target["contract_module_context"],
    )
    history = []
    for round_index in range(feedback_rounds + 1):
        round_dir = target_dir / f"round_{round_index:02d}"
        round_dir.mkdir(exist_ok=True)
        (round_dir / "prompt.md").write_text(prompt)
        try:
            response = call_copilot(
                prompt,
                model,
                copilot_bin,
                round_dir,
                llm_timeout,
                llm_retries,
            )
            (round_dir / "response.txt").write_text(response)
            candidate = sanitize(parse_json_response(response))
            (round_dir / "candidate.json").write_text(json.dumps(candidate, indent=2) + "\n")
        except Exception as error:
            history.append(
                {
                    "round": round_index,
                    "status": "llm_error",
                    "error": f"{type(error).__name__}: {error}",
                }
            )
            break

        if candidate["decision"] != "proved" or not candidate["proof_file"]:
            history.append(
                {
                    "round": round_index,
                    "status": "blocked",
                    "candidate": candidate,
                }
            )
            break
        proof_path = round_dir / "proof.rs"
        proof_path.write_text(candidate["proof_file"])
        policy_error = proof_policy_error(candidate["proof_file"])
        if policy_error is not None:
            diagnostic = f"Static proof policy rejected the candidate: {policy_error}."
            check = {"returncode": 2, "stderr": diagnostic, "stdout": ""}
        elif circular_target_use(target, candidate["proof_file"]):
            diagnostic = "Static check rejected a circular call to the exact target method."
            check = {"returncode": 2, "stderr": diagnostic, "stdout": ""}
        else:
            check = run_verus(
                verus_bin=verus_bin,
                z3_path=z3_path,
                file_path=proof_path,
                timeout=check_timeout,
                rlimit=rlimit,
            )
            (round_dir / "verus_stdout.txt").write_text(check["stdout"])
            (round_dir / "verus_stderr.txt").write_text(check["stderr"])
        record = {
            "round": round_index,
            "status": "proved" if check["returncode"] == 0 else "verus_error",
            "candidate": candidate,
            "verus_returncode": check["returncode"],
            "diagnostic": (check.get("stderr") or "")[-8000:],
        }
        history.append(record)
        (round_dir / "round_result.json").write_text(json.dumps(record, indent=2) + "\n")
        if check["returncode"] == 0:
            proved_dir = proved_root / target["id"]
            proved_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(proof_path, proved_dir / "proof.rs")
            (proved_dir / "metadata.json").write_text(
                json.dumps(
                    {
                        "id": target["id"],
                        "api_path": target["api_path"],
                        "raw_target": target["raw_target"],
                        "contract_source_file": target["contract_source_file"],
                        "contract_source_line": target["contract_source_line"],
                        "rust_declaration": declaration,
                        "trust_level": candidate["trust_level"],
                        "trusted_assumptions": candidate["trusted_assumptions"],
                        "rationale": candidate["rationale"],
                        "run_target_dir": str(target_dir),
                    },
                    indent=2,
                )
                + "\n"
            )
            break
        if round_index >= feedback_rounds:
            break
        prompt = FEEDBACK_PROMPT.format(
            target=target["api_path"],
            candidate=json.dumps(candidate, indent=2),
            diagnostic=(check.get("stderr") or check.get("stdout") or "")[-10000:],
        )

    final = history[-1] if history else {"status": "no_round"}
    result = {
        "id": target["id"],
        "api_path": target["api_path"],
        "status": final.get("status"),
        "decision": (final.get("candidate") or {}).get("decision", "blocked"),
        "trust_level": (final.get("candidate") or {}).get("trust_level", ""),
        "trusted_assumptions": (final.get("candidate") or {}).get("trusted_assumptions", []),
        "blocker": (final.get("candidate") or {}).get("blocker", final.get("error", "")),
        "history": history,
    }
    (target_dir / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def write_summary(out: Path, results: list[dict[str, Any]], metadata: dict[str, Any]) -> None:
    counts: dict[str, int] = {}
    for result in results:
        counts[result.get("status") or "unknown"] = counts.get(result.get("status") or "unknown", 0) + 1
    payload = {"metadata": metadata, "counts": counts, "results": results}
    (out / "summary.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = [
        "# Bulk source-proof campaign",
        "",
        f"- Attempted: {len(results)}",
        f"- Counts: `{counts}`",
        "",
        "| Target | Status | Trust | Blocker |",
        "|---|---|---|---|",
    ]
    for result in sorted(results, key=lambda item: item["id"]):
        blocker = str(result.get("blocker", "")).replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| `{result['api_path']}` | {result.get('status', '')} | "
            f"{result.get('trust_level', '')} | {blocker[:240]} |"
        )
    (out / "SUMMARY.md").write_text("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=HERE / "manifest.json")
    parser.add_argument("--out", type=Path, default=HERE / "runs" / "gpt56sol")
    parser.add_argument(
        "--proved-root",
        type=Path,
        default=SOURCE_VERIFICATION / "proved-apis",
    )
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--copilot-bin", default="copilot")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--include-no-body", action="store_true")
    parser.add_argument("--attempt-no-body", action="store_true")
    parser.add_argument("--only-no-body", action="store_true")
    parser.add_argument("--select-from-summary", type=Path)
    parser.add_argument(
        "--select-status",
        default="blocked,verus_error,llm_error,exception",
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retry-blocked", action="store_true")
    parser.add_argument("--feedback-rounds", type=int, default=2)
    parser.add_argument("--llm-timeout", type=int, default=600)
    parser.add_argument("--llm-retries", type=int, default=2)
    parser.add_argument("--check-timeout", type=int, default=300)
    parser.add_argument("--rlimit", type=float, default=120)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = json.loads(args.manifest.read_text())
    targets = [
        target
        for target in manifest["targets"]
        if not target["preproved"]
        and (args.include_no_body or args.attempt_no_body or target["has_rust_1_96_body"])
        and (not args.only_no_body or not target["has_rust_1_96_body"])
    ]
    if args.select_from_summary is not None:
        selected_payload = json.loads(args.select_from_summary.read_text())
        selected_statuses = {
            value.strip() for value in args.select_status.split(",") if value.strip()
        }
        selected_ids = {
            result["id"]
            for result in selected_payload.get("results", [])
            if result.get("status") in selected_statuses
        }
        targets = [target for target in targets if target["id"] in selected_ids]
    targets = targets[args.offset :]
    if args.limit is not None:
        targets = targets[: args.limit]
    args.out.mkdir(parents=True, exist_ok=True)
    args.proved_root.mkdir(parents=True, exist_ok=True)
    verus_bin = WORKSPACE / "verus" / "source" / "target-verus" / "release" / "verus"
    z3_path = WORKSPACE / "verus" / "source" / "z3"
    metadata = {
        "model": args.model,
        "manifest": str(args.manifest.resolve()),
        "proved_root": str(args.proved_root.resolve()),
        "feedback_rounds": args.feedback_rounds,
    }
    results = []
    pending = []
    for target in targets:
        summary_path = args.out / "targets" / target["id"] / "summary.json"
        if args.resume and summary_path.is_file():
            saved = json.loads(summary_path.read_text())
            retry_statuses = {"llm_error", "verus_error", "no_round", "exception"}
            if args.retry_blocked:
                retry_statuses |= {"blocked", "blocked_no_rust_body"}
            if saved.get("status") not in retry_statuses:
                results.append(saved)
                continue
        pending.append(target)
    write_summary(args.out, results, metadata)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(
                run_one,
                target,
                run_root=args.out,
                proved_root=args.proved_root,
                model=args.model,
                copilot_bin=args.copilot_bin,
                llm_timeout=args.llm_timeout,
                llm_retries=args.llm_retries,
                feedback_rounds=args.feedback_rounds,
                check_timeout=args.check_timeout,
                rlimit=args.rlimit,
                verus_bin=verus_bin,
                z3_path=z3_path,
                attempt_no_body=args.attempt_no_body,
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
                    "status": "exception",
                    "decision": "blocked",
                    "blocker": f"{type(error).__name__}: {error}",
                    "history": [],
                }
            results.append(result)
            print(
                f"[{len(results)}/{len(targets)}] {target['api_path']} "
                f"status={result.get('status')} trust={result.get('trust_level', '')}",
                flush=True,
            )
            write_summary(args.out, results, metadata)
    write_summary(args.out, results, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
