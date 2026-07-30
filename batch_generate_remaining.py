#!/usr/bin/env python3
"""Batch first-pass generation for the 2,018 remaining Rust std APIs."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
import subprocess
import time
from typing import Any


PROMPT = """\
For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
{targets}
```

Return JSON only:
{{
  "candidates": [
    {{
      "target": "exact target string",
      "decision": "add_spec" | "skip",
      "contract_form": "assume_specification" | "external_trait_specification",
      "contract_code": "complete Verus declaration(s), without verus! wrapper",
      "requires": ["..."],
      "ensures": ["..."],
      "feature_gates": ["..."],
      "imports": ["..."],
      "useful": true | false,
      "rationale": "short source-grounded explanation",
      "risks": ["..."]
    }}
  ]
}}

Rules:
- Return exactly one candidate for every target, in the same order.
- Do not edit files.
- External contracts are trusted; do not invent private fields, hidden state, or
  stronger behavior than the supplied signature/source supports.
- Respect each target's classification and reasons. A `skip` decision is the
  expected result for runtime effects, hidden state, formatting, concurrency,
  unavailable toolchain APIs, unsupported mutable-reference returns, and APIs
  that need a missing abstraction.
- Use `add_spec` only when a concrete useful relation can be written in existing
  public vstd vocabulary.
- For `add_spec`, use the exact Rust 1.96 signature metadata. Bind non-unit
  results by name. Use `old(x)`/`final(x)` for mutable references.
- Do not add cfg/cfg_attr attributes.
- Do not use `true`, `false`, `arbitrary()`, `assume`, `requires false`, or
  source-unjustified preconditions to force determinism.
- Prefer `skip` over a deterministic but semantically unsupported contract.
"""


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
    raise ValueError("response did not contain a JSON object")


def compact_source(context: str, radius: int = 16) -> str:
    lines = context.splitlines()
    if len(lines) <= radius * 2 + 1:
        return context
    center = len(lines) // 2
    return "\n".join(lines[center - radius : center + radius + 1])


def compact_target(target: dict[str, Any]) -> dict[str, Any]:
    verification = (target.get("verification_declarations") or [{}])[0]
    nanvix = (target.get("declarations") or [{}])[0]
    return {
        "target": target["target"],
        "generation_group": target["generation_group"],
        "classification": target["classification"],
        "classification_reasons": target.get("classification_reasons", []),
        "category": target["category"],
        "kinds": target["kinds"],
        "semantic_risks": target.get("semantic_risks", []),
        "available_in_verus_rust_1_96": target[
            "available_in_verus_rust_1_96"
        ],
        "recommended_contract_form": target["recommended_contract_form"],
        "verification_signature": {
            key: value
            for key, value in verification.items()
            if key
            in {
                "name",
                "header",
                "signature",
                "generics",
                "owner",
                "observability",
            }
        },
        "verification_source": compact_source(
            verification.get("source_context", "")
        ),
        "nanvix_source": compact_source(nanvix.get("source_context", ""), 10),
        "previous_skip_rationale": target.get("previous_skip_rationale", ""),
    }


def sanitize(candidate: dict[str, Any]) -> dict[str, Any]:
    result = dict(candidate)
    result["target"] = str(result.get("target", "")).strip()
    result["decision"] = str(result.get("decision", "")).strip()
    result["contract_form"] = str(result.get("contract_form", "")).strip()
    code = str(result.get("contract_code", "")).strip()
    match = re.fullmatch(r"```(?:rust)?\s*(.*?)```", code, flags=re.DOTALL)
    result["contract_code"] = match.group(1).strip() if match else code
    for key in ("requires", "ensures", "feature_gates", "imports", "risks"):
        value = result.get(key) or []
        if not isinstance(value, list):
            value = [value]
        result[key] = [
            str(item).strip() for item in value if str(item).strip()
        ]
    return result


def call_copilot(
    *,
    prompt: str,
    model: str,
    copilot_bin: str,
    timeout: int,
    retries: int,
    cwd: Path,
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


def build_batches(
    targets: list[dict[str, Any]],
    batch_size: int,
) -> list[list[dict[str, Any]]]:
    batches = []
    current_group = None
    current = []
    for target in targets:
        group = target["generation_group"]
        if current and (group != current_group or len(current) >= batch_size):
            batches.append(current)
            current = []
        current_group = group
        current.append(target)
    if current:
        batches.append(current)
    return batches


def run_batch(
    *,
    index: int,
    targets: list[dict[str, Any]],
    out_dir: Path,
    model: str,
    copilot_bin: str,
    timeout: int,
    retries: int,
    resume: bool,
) -> dict[str, Any]:
    batch_dir = out_dir / "batches" / f"batch_{index:04d}"
    batch_dir.mkdir(parents=True, exist_ok=True)
    result_path = batch_dir / "result.json"
    if resume and result_path.is_file():
        return json.loads(result_path.read_text())

    target_payload = [compact_target(target) for target in targets]
    prompt = PROMPT.format(targets=json.dumps(target_payload, indent=2))
    (batch_dir / "prompt.md").write_text(prompt)
    started = time.monotonic()
    response = call_copilot(
        prompt=prompt,
        model=model,
        copilot_bin=copilot_bin,
        timeout=timeout,
        retries=retries,
        cwd=batch_dir,
    )
    duration_ms = int((time.monotonic() - started) * 1000)
    (batch_dir / "response.txt").write_text(response)
    parsed = parse_json_response(response)
    raw_candidates = parsed.get("candidates")
    if not isinstance(raw_candidates, list):
        raise ValueError("response JSON has no candidates array")
    candidates = [sanitize(candidate) for candidate in raw_candidates]
    expected = [target["target"] for target in targets]
    actual = [candidate["target"] for candidate in candidates]
    if actual != expected:
        raise ValueError(
            f"target mismatch: expected {expected!r}, received {actual!r}"
        )
    result = {
        "batch": index,
        "group": targets[0]["generation_group"],
        "duration_ms": duration_ms,
        "targets": expected,
        "candidates": candidates,
    }
    result_path.write_text(json.dumps(result, indent=2) + "\n")
    return result


def write_summary(
    out_dir: Path,
    results: list[dict[str, Any]],
    metadata: dict[str, Any],
) -> None:
    candidates = [
        candidate
        for result in sorted(results, key=lambda item: item["batch"])
        for candidate in result["candidates"]
    ]
    counts = Counter(candidate["decision"] for candidate in candidates)
    group_counts: dict[str, Counter] = {}
    for result in results:
        counter = group_counts.setdefault(result["group"], Counter())
        counter.update(candidate["decision"] for candidate in result["candidates"])
    payload = {
        "metadata": metadata,
        "counts": dict(sorted(counts.items())),
        "group_counts": {
            group: dict(sorted(counter.items()))
            for group, counter in sorted(group_counts.items())
        },
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    (out_dir / "firstpass_summary.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )
    (out_dir / "seed-candidates.json").write_text(
        json.dumps(
            {
                candidate["target"]: candidate
                for candidate in candidates
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    lines = [
        "# Remaining API batch-generation first pass",
        "",
        f"- Candidates: {len(candidates)}",
        f"- Add spec: {counts['add_spec']}",
        f"- Skip: {counts['skip']}",
        "",
        "| Group | Add spec | Skip |",
        "|---|---:|---:|",
    ]
    for group, counter in sorted(group_counts.items()):
        lines.append(
            f"| `{group}` | {counter['add_spec']} | {counter['skip']} |"
        )
    (out_dir / "SUMMARY.md").write_text("\n".join(lines).rstrip() + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument(
        "--manifest",
        type=Path,
        default=workspace
        / "specgen"
        / "remaining-generation"
        / "all-remaining-manifest.json",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=workspace
        / "specgen"
        / "remaining-generation"
        / "firstpass-gpt56sol",
    )
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--copilot-bin", default="copilot")
    parser.add_argument("--batch-size", type=int, default=6)
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--limit-batches", type=int)
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = json.loads(args.manifest.read_text())
    targets = manifest["targets"]
    batches = build_batches(targets, args.batch_size)
    if args.limit_batches is not None:
        batches = batches[: args.limit_batches]
    args.out.mkdir(parents=True, exist_ok=True)
    metadata = {
        "model": args.model,
        "manifest": str(args.manifest.resolve()),
        "batch_size": args.batch_size,
        "batch_count": len(batches),
        "target_count": sum(len(batch) for batch in batches),
    }
    results = []
    failures = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(
                run_batch,
                index=index,
                targets=batch,
                out_dir=args.out,
                model=args.model,
                copilot_bin=args.copilot_bin,
                timeout=args.timeout,
                retries=args.retries,
                resume=args.resume,
            ): index
            for index, batch in enumerate(batches)
        }
        for completed, future in enumerate(as_completed(futures), start=1):
            index = futures[future]
            try:
                result = future.result()
            except Exception as error:
                failures.append(
                    {
                        "batch": index,
                        "error": f"{type(error).__name__}: {error}",
                    }
                )
                print(
                    f"[{completed}/{len(batches)}] batch={index} ERROR "
                    f"{type(error).__name__}: {error}",
                    flush=True,
                )
                continue
            results.append(result)
            counts = Counter(
                candidate["decision"] for candidate in result["candidates"]
            )
            print(
                f"[{completed}/{len(batches)}] batch={index} "
                f"group={result['group']} add={counts['add_spec']} "
                f"skip={counts['skip']}",
                flush=True,
            )
            write_summary(args.out, results, metadata)
    write_summary(args.out, results, metadata)
    (args.out / "failures.json").write_text(
        json.dumps(failures, indent=2) + "\n"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
