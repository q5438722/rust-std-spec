#!/usr/bin/env python3
"""Extract source-backed implementation-proof inputs for Slice/Vec targets.

The extractor is intentionally mechanical: it reads only frozen inputs, records
exact source spans and hashes, and emits target-local manifests without claiming
any Verus implementation proof.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path("/home/chentianyu/nanvix-rust-std-spec-survey/nanvix-rust-std-slice-vec-implproof-2026-08-12")
TARGETS_JSON = ROOT / "proof_inventory" / "targets_144.json"
TARGETS_CSV = ROOT / "proof_inventory" / "targets_144.csv"
FILE_MANIFEST = ROOT / "frozen_inputs" / "file_manifest.json"
SPANS_JSON = ROOT / "proof_inventory" / "source_body_spans.json"
SPANS_CSV = ROOT / "proof_inventory" / "source_body_spans.csv"
ORDER_JSON = ROOT / "proof_inventory" / "proof_order.json"
ORDER_CSV = ROOT / "proof_inventory" / "proof_order.csv"
DEPENDENCY_SUMMARY = ROOT / "proof_inventory" / "dependency_summary.json"
TARGET_COUNTS = ROOT / "proof_inventory" / "target_counts.json"
MANIFEST_ROOT = ROOT / "proof_manifests"
HARNESS_ROOT = ROOT / "proof_harnesses"

CONTROL_WORDS = {
    "if",
    "else",
    "for",
    "while",
    "loop",
    "match",
    "return",
    "let",
    "where",
    "Some",
    "None",
    "Ok",
    "Err",
    "Self",
    "unsafe",
    "const",
    "move",
    "async",
}

BOUNDARY_PATTERNS = {
    "unsafe": [
        r"\bunsafe\s*\{",
        r"\bunsafe\s+fn\b",
        r"assert_unsafe_precondition!",
    ],
    "intrinsic": [
        r"\bintrinsics::",
        r"\bcore::intrinsics::",
        r"\bub_checks::",
        r"\bassert_unsafe_precondition!",
        r"\bunchecked_",
    ],
    "trait_or_callback": [
        r"\bFn(?:Once|Mut)?\b",
        r"\bOrd\b",
        r"\bPartialEq\b",
        r"\bClone\b",
        r"\bCopy\b",
        r"\bIterator\b",
        r"\bRangeBounds\b",
        r"\bDestruct\b",
        r"\.clone\s*\(",
        r"\.lt\s*\(",
    ],
    "allocator": [
        r"\bAllocator\b",
        r"\bRawVec\b",
        r"\bGlobal\b",
        r"\balloc",
        r"\bcapacity\s*\(",
        r"\bgrow",
        r"\breserve",
        r"\bshrink",
        r"\btry_reserve",
        r"\bbuf\b",
    ],
    "raw_pointer_or_provenance": [
        r"\bptr::",
        r"\bNonNull\b",
        r"\bas_ptr\s*\(",
        r"\bas_mut_ptr\s*\(",
        r"\bfrom_raw_parts",
        r"\bslice_from_raw_parts",
        r"\.add\s*\(",
        r"\.sub\s*\(",
        r"\.cast\s*\(",
        r"\.read\s*\(",
        r"\.write\s*\(",
        r"\bcopy_nonoverlapping\b",
        r"\bdrop_in_place\b",
        r"\bset_len\b",
    ],
    "maybe_uninit": [
        r"\bMaybeUninit\b",
        r"\bassume_init",
        r"\bspare_capacity",
    ],
    "panic_or_bounds": [
        r"\bassert(?:_eq|_ne)?!",
        r"\bpanic!",
        r"\bunwrap\s*\(",
        r"\bexpect\s*\(",
        r"\bindex\s*>=",
    ],
}


@dataclass(frozen=True)
class ExtractedItem:
    source_reference_path: str
    frozen_relpath: str
    source_file_sha256: str
    fn_name: str
    signature_start_line: int
    signature_end_line: int
    body_start_line: int
    body_end_line: int
    item_text: str
    item_sha256: str
    signature_text: str
    enclosing_impl_header: str
    enclosing_impl_start_line: int | None


class ScanState:
    def __init__(self) -> None:
        self.block_comment_depth = 0
        self.in_string = False
        self.string_escape = False
        self.raw_hashes: int | None = None

    def copy(self) -> "ScanState":
        other = ScanState()
        other.block_comment_depth = self.block_comment_depth
        other.in_string = self.in_string
        other.string_escape = self.string_escape
        other.raw_hashes = self.raw_hashes
        return other


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def slug_for(order: int, target: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", target).strip("_")
    return f"{order:03d}_{slug}"


def rust_brace_counts(line: str, state: ScanState) -> tuple[int, int]:
    opens = 0
    closes = 0
    i = 0
    while i < len(line):
        ch = line[i]
        nxt = line[i + 1] if i + 1 < len(line) else ""

        if state.block_comment_depth:
            if ch == "/" and nxt == "*":
                state.block_comment_depth += 1
                i += 2
                continue
            if ch == "*" and nxt == "/":
                state.block_comment_depth -= 1
                i += 2
                continue
            i += 1
            continue

        if state.raw_hashes is not None:
            if ch == '"':
                hashes = 0
                j = i + 1
                while j < len(line) and line[j] == "#":
                    hashes += 1
                    j += 1
                if hashes == state.raw_hashes:
                    state.raw_hashes = None
                    i = j
                    continue
            i += 1
            continue

        if state.in_string:
            if state.string_escape:
                state.string_escape = False
            elif ch == "\\":
                state.string_escape = True
            elif ch == '"':
                state.in_string = False
            i += 1
            continue

        if ch == "/" and nxt == "/":
            break
        if ch == "/" and nxt == "*":
            state.block_comment_depth += 1
            i += 2
            continue
        if ch == "r":
            j = i + 1
            hashes = 0
            while j < len(line) and line[j] == "#":
                hashes += 1
                j += 1
            if j < len(line) and line[j] == '"':
                state.raw_hashes = hashes
                i = j + 1
                continue
        if ch == '"':
            state.in_string = True
            i += 1
            continue
        if ch == "{":
            opens += 1
        elif ch == "}":
            closes += 1
        i += 1
    return opens, closes


def code_without_line_comment(line: str) -> str:
    state = ScanState()
    result: list[str] = []
    i = 0
    while i < len(line):
        ch = line[i]
        nxt = line[i + 1] if i + 1 < len(line) else ""
        if state.in_string:
            result.append(ch)
            if state.string_escape:
                state.string_escape = False
            elif ch == "\\":
                state.string_escape = True
            elif ch == '"':
                state.in_string = False
            i += 1
            continue
        if ch == "/" and nxt == "/":
            break
        if ch == '"':
            state.in_string = True
        result.append(ch)
        i += 1
    return "".join(result)


def find_function_line(lines: list[str], target: str, source_reference: str, source_excerpt: str) -> int:
    fn_name = target.split("::")[-1]
    _, line_text = source_reference.rsplit(":", 1)
    reference_index = max(0, int(line_text) - 1)
    fn_pattern = re.compile(rf"\bfn\s+{re.escape(fn_name)}\b")
    candidates: list[int] = []
    lo = max(0, reference_index - 80)
    hi = min(len(lines), reference_index + 120)
    for idx in range(lo, hi):
        if fn_pattern.search(code_without_line_comment(lines[idx])):
            candidates.append(idx)
    if not candidates:
        for idx, line in enumerate(lines):
            if fn_pattern.search(code_without_line_comment(line)):
                candidates.append(idx)
    if not candidates and source_excerpt:
        first_excerpt_line = source_excerpt.splitlines()[0].strip()
        for idx, line in enumerate(lines):
            if first_excerpt_line and first_excerpt_line in line:
                candidates.append(idx)
    if not candidates:
        raise RuntimeError(f"could not locate function line for {target} near {source_reference}")
    return min(candidates, key=lambda idx: abs(idx - reference_index))


def find_enclosing_impl(lines: list[str], function_index: int) -> tuple[str, int | None]:
    depth = 0
    state = ScanState()
    stack: list[tuple[int, int, str]] = []
    pending_impl: tuple[int, str] | None = None
    impl_start = re.compile(r"^\s*(?:unsafe\s+)?impl\b")
    for idx, line in enumerate(lines[: function_index + 1]):
        stripped = code_without_line_comment(line).strip()
        if impl_start.search(stripped):
            pending_impl = (idx + 1, stripped)
        opens, closes = rust_brace_counts(line, state)
        if pending_impl and opens:
            stack.append((depth + opens - closes, pending_impl[0], pending_impl[1]))
            pending_impl = None
        depth += opens - closes
        while stack and depth < stack[-1][0]:
            stack.pop()
    if stack:
        _, start_line, header = stack[-1]
        return header, start_line
    return "", None


def extract_item(
    target: str,
    source_reference: str,
    source_excerpt: str,
    source_reference_path: str,
    frozen_relpath: str,
    source_file_sha256: str,
    lines: list[str],
    function_index: int | None = None,
) -> ExtractedItem:
    fn_name = target.split("::")[-1]
    start = function_index
    if start is None:
        start = find_function_line(lines, target, source_reference, source_excerpt)
    depth = 0
    body_started = False
    body_start = start
    body_end = start
    state = ScanState()
    for idx in range(start, len(lines)):
        opens, closes = rust_brace_counts(lines[idx], state)
        if not body_started and opens:
            body_started = True
            body_start = idx
        if body_started:
            depth += opens - closes
            if depth == 0:
                body_end = idx
                break
    if not body_started:
        raise RuntimeError(f"could not find body opening brace for {target} at {source_reference}")
    if depth != 0:
        raise RuntimeError(f"unterminated body for {target} at {source_reference}")

    item_lines = lines[start : body_end + 1]
    item_text = "".join(item_lines)
    signature_text = "".join(lines[start : body_start + 1])
    impl_header, impl_line = find_enclosing_impl(lines, start)
    return ExtractedItem(
        source_reference_path=source_reference_path,
        frozen_relpath=frozen_relpath,
        source_file_sha256=source_file_sha256,
        fn_name=fn_name,
        signature_start_line=start + 1,
        signature_end_line=body_start + 1,
        body_start_line=body_start + 1,
        body_end_line=body_end + 1,
        item_text=item_text,
        item_sha256=sha256_text(item_text),
        signature_text=signature_text,
        enclosing_impl_header=impl_header,
        enclosing_impl_start_line=impl_line,
    )


def source_ref_path(source_reference: str) -> str:
    return source_reference.split(":", 1)[0]


def manifest_ref_map(file_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    mapping: dict[str, dict[str, Any]] = {}
    for row in file_rows:
        ref = row.get("rust_source_reference", "")
        if row.get("category") == "rust-1.96-source-body" and ref:
            mapping[ref] = row
    return mapping


def extract_call_tokens(text: str) -> list[dict[str, str]]:
    code = "\n".join(code_without_line_comment(line) for line in text.splitlines())
    tokens: list[dict[str, str]] = []
    occupied: list[range] = []

    def mark(start: int, end: int) -> None:
        occupied.append(range(start, end))

    def is_occupied(start: int, end: int) -> bool:
        return any(start in item or end - 1 in item for item in occupied if end > start)

    for match in re.finditer(
        r"\b(?P<receiver>self|Self)\s*(?P<sep>\.|::)\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*(?:::<[^>\n]+>)?\s*\(",
        code,
    ):
        tokens.append(
            {
                "kind": "self_method" if match.group("sep") == "." else "self_associated",
                "name": match.group("name"),
                "receiver": match.group("receiver"),
                "path": f"{match.group('receiver')}{match.group('sep')}{match.group('name')}",
            }
        )
        mark(match.start(), match.end())

    for match in re.finditer(r"\.\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*(?:::<[^>\n]+>)?\s*\(", code):
        if is_occupied(match.start(), match.end()):
            continue
        tokens.append({"kind": "method", "name": match.group("name"), "path": f".{match.group('name')}"})
        mark(match.start(), match.end())

    for match in re.finditer(
        r"\b(?P<path>[A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z_][A-Za-z0-9_]*)+)\s*(?:::<[^>\n]+>)?\s*\(",
        code,
    ):
        if is_occupied(match.start(), match.end()):
            continue
        path = match.group("path")
        tokens.append({"kind": "path", "name": path.split("::")[-1], "path": path})
        mark(match.start(), match.end())

    for match in re.finditer(r"\b([A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z_][A-Za-z0-9_]*)*)!", code):
        tokens.append({"kind": "macro", "name": match.group(1).split("::")[-1] + "!", "path": match.group(1)})
        mark(match.start(), match.end())

    for match in re.finditer(r"(?<!fn\s)\b([A-Za-z_][A-Za-z0-9_]*)\s*(?:::<[^>\n]+>)?\s*\(", code):
        if is_occupied(match.start(), match.end()):
            continue
        prefix = code[max(0, match.start() - 2) : match.start()]
        if "." in prefix or ":" in prefix:
            continue
        name = match.group(1)
        if name not in CONTROL_WORDS:
            tokens.append({"kind": "simple", "name": name, "path": name})
            mark(match.start(), match.end())
    return tokens


def extract_call_names(text: str) -> set[str]:
    names: set[str] = set()
    for token in extract_call_tokens(text):
        names.add(token["name"])
    return names


def private_candidate_names(tokens: list[dict[str, str]]) -> set[str]:
    return {
        token["name"]
        for token in tokens
        if token["kind"] in {"simple", "self_method", "self_associated"}
        and not token["name"].endswith("!")
    }


def dependency_categories(signature_text: str, item_text: str, module: str) -> dict[str, dict[str, Any]]:
    text = signature_text + "\n" + item_text
    categories: dict[str, dict[str, Any]] = {}
    for name, patterns in BOUNDARY_PATTERNS.items():
        matches: list[str] = []
        for pattern in patterns:
            if re.search(pattern, text):
                matches.append(pattern)
        if module == "vec" and name == "allocator" and re.search(r"\bVec\b|\bbuf\b|\bcapacity\b", text):
            matches.append("vec_storage_context")
        categories[name] = {
            "present": bool(matches),
            "matched_patterns": sorted(set(matches)),
        }
    return categories


def build_source_item_index(
    file_rows: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    fn_line = re.compile(r"\bfn\s+([A-Za-z_][A-Za-z0-9_]*)\b")
    for row in file_rows:
        if row.get("category") != "rust-1.96-source-body" or not row.get("rust_source_reference"):
            continue
        path = ROOT / row["frozen_relpath"]
        lines = path.read_text().splitlines(keepends=True)
        for idx, line in enumerate(lines):
            match = fn_line.search(code_without_line_comment(line))
            if not match:
                continue
            name = match.group(1)
            synthetic_target = f"{row['rust_source_reference']}::{name}"
            try:
                item = extract_item(
                    synthetic_target,
                    f"{row['rust_source_reference']}:{idx + 1}",
                    line.strip(),
                    row["rust_source_reference"],
                    row["frozen_relpath"],
                    row["sha256"],
                    lines,
                    function_index=idx,
                )
            except RuntimeError:
                continue
            public = bool(re.search(r"\bpub\b", item.signature_text))
            index[name].append(
                {
                    "name": name,
                    "source_reference_path": row["rust_source_reference"],
                    "frozen_relpath": row["frozen_relpath"],
                    "signature_start_line": item.signature_start_line,
                    "body_end_line": item.body_end_line,
                    "item_sha256": item.item_sha256,
                    "public": public,
                    "item_text": item.item_text,
                }
            )
    return index


def private_callee_closure(candidate_names: set[str], source_index: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, int]] = set()
    queue: deque[str] = deque(sorted(name for name in candidate_names if not name.endswith("!")))
    closure: list[dict[str, Any]] = []
    while queue and len(closure) < 300:
        name = queue.popleft()
        for entry in source_index.get(name, []):
            if entry["public"]:
                continue
            key = (entry["name"], entry["frozen_relpath"], int(entry["signature_start_line"]))
            if key in seen:
                continue
            seen.add(key)
            closure_entry = {k: v for k, v in entry.items() if k != "item_text"}
            closure.append(closure_entry)
            child_tokens = extract_call_tokens(entry["item_text"])
            for child in private_candidate_names(child_tokens):
                if child not in seen and not child.endswith("!"):
                    queue.append(child)
    return closure


def target_dependency_candidates(
    current_target: str,
    item_text: str,
    target_name_map: dict[str, list[str]],
) -> list[str]:
    deps: set[str] = set()
    current_owner = "::".join(current_target.split("::")[:-1])
    for token in extract_call_tokens(item_text):
        name = token["name"]
        if token["kind"] in {"self_method", "self_associated"}:
            for target in target_name_map.get(name, []):
                if target != current_target and "::".join(target.split("::")[:-1]) == current_owner:
                    deps.add(target)
        elif token["kind"] == "path":
            path = token["path"]
            for target in target_name_map.get(name, []):
                target_owner = "::".join(target.split("::")[:-1])
                if target != current_target and (
                    path == target_owner
                    or path.endswith(target_owner)
                    or path.endswith(target_owner.replace("alloc::vec::", "Vec::"))
                ):
                    deps.add(target)
        elif token["kind"] == "simple":
            for target in target_name_map.get(name, []):
                target_owner = "::".join(target.split("::")[:-1])
                if target != current_target and target_owner == current_owner:
                    deps.add(target)
    return sorted(deps)


def proof_tier(categories: dict[str, dict[str, Any]], target_deps: list[str]) -> tuple[int, str]:
    if target_deps:
        return 2, "depends on other generated targets"
    if categories["allocator"]["present"] or categories["raw_pointer_or_provenance"]["present"]:
        return 1, "no generated-target callees; allocator/raw-pointer boundary required"
    if categories["unsafe"]["present"] or categories["intrinsic"]["present"] or categories["maybe_uninit"]["present"]:
        return 1, "no generated-target callees; unsafe/intrinsic/MaybeUninit boundary required"
    if categories["trait_or_callback"]["present"]:
        return 1, "no generated-target callees; trait/callback behavior required"
    return 0, "no generated-target callees or detected hard boundary"


def bottom_up_order(
    targets: list[dict[str, Any]],
    dependency_by_target: dict[str, list[str]],
    tier_by_target: dict[str, tuple[int, str]],
) -> list[dict[str, Any]]:
    target_by_name = {row["target"]: row for row in targets}
    remaining_deps = {target: set(deps) for target, deps in dependency_by_target.items()}
    reverse: dict[str, set[str]] = defaultdict(set)
    for target, deps in remaining_deps.items():
        for dep in deps:
            if dep in target_by_name:
                reverse[dep].add(target)

    def sort_key(target: str) -> tuple[int, int, int, str]:
        row = target_by_name[target]
        tier, _ = tier_by_target[target]
        return (tier, len(remaining_deps[target]), int(row["input_order"]), target)

    ready = sorted([target for target, deps in remaining_deps.items() if not deps], key=sort_key)
    emitted: list[str] = []
    while ready:
        target = ready.pop(0)
        if target in emitted:
            continue
        emitted.append(target)
        for dependent in sorted(reverse.get(target, set()), key=sort_key):
            remaining_deps[dependent].discard(target)
            if not remaining_deps[dependent] and dependent not in emitted and dependent not in ready:
                ready.append(dependent)
        ready.sort(key=sort_key)

    cycle_members = sorted([target for target in target_by_name if target not in emitted], key=sort_key)
    emitted.extend(cycle_members)
    order_entries: list[dict[str, Any]] = []
    for index, target in enumerate(emitted, start=1):
        row = target_by_name[target]
        tier, reason = tier_by_target[target]
        unresolved = sorted(remaining_deps[target])
        order_entries.append(
            {
                "proof_order_index": index,
                "module": row["module"],
                "target": target,
                "input_order": row["input_order"],
                "semantic_family": row["semantic_family"],
                "proof_tier": tier,
                "proof_tier_reason": reason,
                "generated_target_dependencies": dependency_by_target[target],
                "cycle_or_unresolved_dependencies": unresolved,
                "bottom_up_rationale": (
                    "all generated-target dependencies ordered earlier"
                    if not unresolved
                    else "cycle/ambiguous generated-target dependency remains; keep dependency manifest as proof obligation"
                ),
            }
        )
    return order_entries


def assumption_entries(categories: dict[str, dict[str, Any]], shared_helpers: list[str]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    if shared_helpers:
        entries.append(
            {
                "kind": "shared_model_helper",
                "name": ",".join(shared_helpers),
                "status": "existing_generated_contract_vocabulary_assumption_until_body_proved",
                "rationale": "Generated contract uses audited shared helper vocabulary; this manifest does not assume the target postcondition.",
            }
        )
    for name, info in categories.items():
        if not info["present"]:
            continue
        entries.append(
            {
                "kind": name,
                "name": name,
                "status": "dependency_obligation_or_minimal_boundary_candidate",
                "rationale": "Detected directly from the Rust 1.96 source body/signature and must be discharged by recursive proof, reviewed contract, or named minimal trusted boundary.",
            }
        )
    return entries


def harness_text(row: dict[str, Any], item: ExtractedItem, dependency_manifest_rel: str) -> str:
    contract = row["contract_text"].replace("*/", "* /")
    body = item.item_text
    return f"""#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Auto-generated implementation-proof harness seed.
// Target: {row['target']}
// Source: {item.source_reference_path}:{item.signature_start_line}-{item.body_end_line}
// Source item sha256: {item.item_sha256}
// Dependency manifest: {dependency_manifest_rel}
//
// Status: real Rust 1.96 body extracted verbatim; Verus syntax adaptation and
// verification are intentionally pending. This file must not be counted as an
// implementation proof until a future manifest records mechanical adaptations
// and an actual Verus command succeeds without assuming the target body.

use vstd::prelude::*;

const CONTRACT_UNDER_TEST: &str = r###"{contract}"###;

const REAL_RUST_1_96_BODY: &str = r###"{body}"###;

verus! {{
    proof fn real_body_extraction_recorded() ensures true {{
    }}
}}
"""


def write_target_artifacts(
    row: dict[str, Any],
    item: ExtractedItem,
    categories: dict[str, dict[str, Any]],
    call_names: set[str],
    private_closure: list[dict[str, Any]],
    target_deps: list[str],
) -> tuple[str, str, str]:
    slug = slug_for(int(row["input_order"]), row["target"])
    manifest_dir = MANIFEST_ROOT / slug
    harness_dir = HARNESS_ROOT / slug
    manifest_dir.mkdir(parents=True, exist_ok=True)
    harness_dir.mkdir(parents=True, exist_ok=True)

    source_excerpt_path = harness_dir / "source_excerpt.rs"
    source_excerpt_path.write_text(item.item_text)

    shared_helpers = sorted(
        {
            helper.strip()
            for field in ["direct_shared_helpers", "reachable_shared_helpers", "audited_shared_helpers"]
            for helper in str(row.get(field, "")).split(",")
            if helper.strip()
        }
    )
    dependency_manifest = {
        "schema_version": 1,
        "target": row["target"],
        "module": row["module"],
        "source_item_sha256": item.item_sha256,
        "source_file_sha256": item.source_file_sha256,
        "direct_call_names": sorted(call_names),
        "private_helper_callee_closure": private_closure,
        "generated_target_dependency_candidates": target_deps,
        "unsafe_intrinsic_trait_allocator_dependencies": categories,
        "assumptions_and_boundaries": assumption_entries(categories, shared_helpers),
        "proof_status": "pending_actual_verus_implementation_proof",
        "notes": "Callee closure is source-indexed and conservative for Rust method dispatch; every listed item is source-backed by frozen line/hash metadata.",
    }
    dep_path = manifest_dir / "dependency_assumption_manifest.json"
    write_json(dep_path, dependency_manifest)

    transformation_manifest = {
        "schema_version": 1,
        "target": row["target"],
        "source_reference_path": item.source_reference_path,
        "frozen_relpath": item.frozen_relpath,
        "source_span": {
            "signature_start_line": item.signature_start_line,
            "signature_end_line": item.signature_end_line,
            "body_start_line": item.body_start_line,
            "body_end_line": item.body_end_line,
            "item_sha256": item.item_sha256,
        },
        "harness_relpath": (harness_dir / "harness.rs").relative_to(ROOT).as_posix(),
        "source_excerpt_relpath": source_excerpt_path.relative_to(ROOT).as_posix(),
        "transformations": [],
        "status": "seed_verbatim_body_recorded_for_verus_syntax_adaptation",
        "semantic_replacement": False,
    }
    trans_path = manifest_dir / "transformation_manifest.json"
    write_json(trans_path, transformation_manifest)

    source_manifest = {
        "schema_version": 1,
        "target": row["target"],
        "target_owner": "::".join(row["target"].split("::")[:-1]),
        "target_path": row["target"],
        "source_reference": row["source_reference"],
        "source_reference_path": item.source_reference_path,
        "frozen_relpath": item.frozen_relpath,
        "source_file_sha256": item.source_file_sha256,
        "source_item_sha256": item.item_sha256,
        "signature_text": item.signature_text,
        "enclosing_impl_header": item.enclosing_impl_header,
        "enclosing_impl_start_line": item.enclosing_impl_start_line,
        "span": {
            "signature_start_line": item.signature_start_line,
            "signature_end_line": item.signature_end_line,
            "body_start_line": item.body_start_line,
            "body_end_line": item.body_end_line,
        },
    }
    source_path = manifest_dir / "source_body.json"
    write_json(source_path, source_manifest)

    dep_rel = dep_path.relative_to(ROOT).as_posix()
    (harness_dir / "harness.rs").write_text(harness_text(row, item, dep_rel))

    return (
        source_path.relative_to(ROOT).as_posix(),
        trans_path.relative_to(ROOT).as_posix(),
        dep_rel,
    )


def summarize_dependency_categories(rows: list[dict[str, Any]]) -> dict[str, Any]:
    category_counts: dict[str, int] = defaultdict(int)
    module_category_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        for category, info in row["dependency_categories"].items():
            if info["present"]:
                category_counts[category] += 1
                module_category_counts[row["module"]][category] += 1
    return {
        "target_count": len(rows),
        "dependency_category_target_counts": dict(sorted(category_counts.items())),
        "dependency_category_target_counts_by_module": {
            module: dict(sorted(counter.items()))
            for module, counter in sorted(module_category_counts.items())
        },
        "private_helper_callee_candidate_targets": sum(1 for row in rows if row["private_helper_callee_count"]),
        "generated_target_dependency_candidate_targets": sum(1 for row in rows if row["generated_target_dependency_count"]),
    }


def update_target_inventory(
    targets: list[dict[str, Any]],
    span_rows: list[dict[str, Any]],
    order_rows: list[dict[str, Any]],
) -> None:
    span_by_target = {row["target"]: row for row in span_rows}
    order_by_target = {row["target"]: row for row in order_rows}
    for row in targets:
        span = span_by_target[row["target"]]
        order = order_by_target[row["target"]]
        row["implementation_body_status"] = (
            "source_body_extracted:"
            f"{span['source_item_sha256']}:"
            f"{span['source_manifest_relpath']}"
        )
        row["private_helper_callee_closure"] = (
            f"source_indexed_conservative_count={span['private_helper_callee_count']};"
            f" manifest={span['dependency_manifest_relpath']}"
        )
        row["unsafe_intrinsic_trait_allocator_dependencies"] = (
            f"categories={','.join(span['present_dependency_categories']) or 'none'};"
            f" manifest={span['dependency_manifest_relpath']}"
        )
        row["proof_order"] = (
            f"index={order['proof_order_index']};tier={order['proof_tier']};"
            f" manifest=proof_inventory/proof_order.json"
        )
    fieldnames = list(targets[0].keys())
    write_json(TARGETS_JSON, targets)
    write_csv(TARGETS_CSV, targets, fieldnames)


def update_target_counts(targets: list[dict[str, Any]], span_rows: list[dict[str, Any]]) -> None:
    base = load_json(TARGET_COUNTS) if TARGET_COUNTS.is_file() else {}
    base["implementation_body_status_counts"] = dict(Counter(row["implementation_body_status"].split(":", 1)[0] for row in targets))
    base["proof_order_status_counts"] = {
        "ordered": sum(1 for row in targets if str(row.get("proof_order", "")).startswith("index=")),
        "pending": sum(1 for row in targets if str(row.get("proof_order", "")).startswith("pending")),
    }
    base["dependency_category_target_counts"] = summarize_dependency_categories(span_rows)[
        "dependency_category_target_counts"
    ]
    write_json(TARGET_COUNTS, base)


def extract_all(refresh: bool) -> None:
    targets = load_json(TARGETS_JSON)
    file_rows = load_json(FILE_MANIFEST)
    ref_map = manifest_ref_map(file_rows)
    target_ref_paths = {source_ref_path(row["source_reference"]) for row in targets}
    missing = sorted(target_ref_paths - set(ref_map))
    if missing:
        raise RuntimeError(f"target source references not frozen: {missing}")

    if refresh:
        for path in [MANIFEST_ROOT, HARNESS_ROOT]:
            if path.exists():
                shutil.rmtree(path)

    source_index = build_source_item_index(file_rows)
    target_name_map: dict[str, list[str]] = defaultdict(list)
    for row in targets:
        target_name_map[row["target"].split("::")[-1]].append(row["target"])

    span_rows: list[dict[str, Any]] = []
    dependency_by_target: dict[str, list[str]] = {}
    tier_by_target: dict[str, tuple[int, str]] = {}
    extracted_by_target: dict[str, ExtractedItem] = {}
    row_by_target = {row["target"]: row for row in targets}

    for row in targets:
        ref_path = source_ref_path(row["source_reference"])
        manifest_row = ref_map[ref_path]
        source_path = ROOT / manifest_row["frozen_relpath"]
        lines = source_path.read_text().splitlines(keepends=True)
        item = extract_item(
            row["target"],
            row["source_reference"],
            row["source_excerpt"],
            ref_path,
            manifest_row["frozen_relpath"],
            manifest_row["sha256"],
            lines,
        )
        extracted_by_target[row["target"]] = item
        call_tokens = extract_call_tokens(item.item_text)
        call_names = {token["name"] for token in call_tokens}
        private_closure = private_callee_closure(private_candidate_names(call_tokens), source_index)
        categories = dependency_categories(item.signature_text, item.item_text, row["module"])
        target_deps = target_dependency_candidates(row["target"], item.item_text, target_name_map)
        dependency_by_target[row["target"]] = target_deps
        tier_by_target[row["target"]] = proof_tier(categories, target_deps)
        source_manifest_rel, transformation_rel, dependency_rel = write_target_artifacts(
            row,
            item,
            categories,
            call_names,
            private_closure,
            target_deps,
        )
        present_categories = sorted(name for name, info in categories.items() if info["present"])
        span_rows.append(
            {
                "input_order": row["input_order"],
                "module": row["module"],
                "target": row["target"],
                "target_owner": "::".join(row["target"].split("::")[:-1]),
                "target_path": row["target"],
                "semantic_family": row["semantic_family"],
                "source_reference": row["source_reference"],
                "source_reference_path": ref_path,
                "frozen_relpath": item.frozen_relpath,
                "source_file_sha256": item.source_file_sha256,
                "source_item_sha256": item.item_sha256,
                "signature_start_line": item.signature_start_line,
                "signature_end_line": item.signature_end_line,
                "body_start_line": item.body_start_line,
                "body_end_line": item.body_end_line,
                "enclosing_impl_header": item.enclosing_impl_header,
                "enclosing_impl_start_line": item.enclosing_impl_start_line or "",
                "direct_call_count": len(call_names),
                "private_helper_callee_count": len(private_closure),
                "generated_target_dependency_count": len(target_deps),
                "present_dependency_categories": present_categories,
                "dependency_categories": categories,
                "source_manifest_relpath": source_manifest_rel,
                "transformation_manifest_relpath": transformation_rel,
                "dependency_manifest_relpath": dependency_rel,
                "harness_relpath": str(Path("proof_harnesses") / slug_for(int(row["input_order"]), row["target"]) / "harness.rs"),
            }
        )

    order_rows = bottom_up_order(targets, dependency_by_target, tier_by_target)
    order_by_target = {row["target"]: row for row in order_rows}
    for span in span_rows:
        order = order_by_target[span["target"]]
        span["proof_order_index"] = order["proof_order_index"]
        span["proof_tier"] = order["proof_tier"]
        span["proof_tier_reason"] = order["proof_tier_reason"]

    span_fields = [
        "input_order",
        "module",
        "target",
        "target_owner",
        "target_path",
        "semantic_family",
        "source_reference",
        "source_reference_path",
        "frozen_relpath",
        "source_file_sha256",
        "source_item_sha256",
        "signature_start_line",
        "signature_end_line",
        "body_start_line",
        "body_end_line",
        "enclosing_impl_header",
        "enclosing_impl_start_line",
        "direct_call_count",
        "private_helper_callee_count",
        "generated_target_dependency_count",
        "present_dependency_categories",
        "proof_order_index",
        "proof_tier",
        "proof_tier_reason",
        "source_manifest_relpath",
        "transformation_manifest_relpath",
        "dependency_manifest_relpath",
        "harness_relpath",
    ]
    write_json(SPANS_JSON, span_rows)
    write_csv(SPANS_CSV, span_rows, span_fields)
    order_fields = [
        "proof_order_index",
        "module",
        "target",
        "input_order",
        "semantic_family",
        "proof_tier",
        "proof_tier_reason",
        "generated_target_dependencies",
        "cycle_or_unresolved_dependencies",
        "bottom_up_rationale",
    ]
    write_json(ORDER_JSON, order_rows)
    write_csv(ORDER_CSV, order_rows, order_fields)
    write_json(DEPENDENCY_SUMMARY, summarize_dependency_categories(span_rows))
    update_target_inventory(targets, span_rows, order_rows)
    update_target_counts(targets, span_rows)
    write_manifest_hashes()


def write_manifest_hashes() -> None:
    paths = [
        "proof_inventory/targets_144.csv",
        "proof_inventory/targets_144.json",
        "proof_inventory/source_body_spans.csv",
        "proof_inventory/source_body_spans.json",
        "proof_inventory/proof_order.csv",
        "proof_inventory/proof_order.json",
        "proof_inventory/dependency_summary.json",
        "proof_inventory/target_counts.json",
    ]
    hashes = {}
    for rel in paths:
        path = ROOT / rel
        if path.is_file():
            hashes[rel] = sha256_file(path)
    write_json(ROOT / "proof_inventory" / "implproof_manifest_hashes.json", hashes)


def check_artifacts() -> None:
    targets = load_json(TARGETS_JSON)
    spans = load_json(SPANS_JSON)
    orders = load_json(ORDER_JSON)
    expected_count = len(targets)
    if expected_count not in {144, 180} or len(spans) != expected_count or len(orders) != expected_count:
        raise RuntimeError(
            f"expected {expected_count} targets/spans/orders, got {len(targets)}/{len(spans)}/{len(orders)}"
        )
    target_names = {row["target"] for row in targets}
    if {row["target"] for row in spans} != target_names:
        raise RuntimeError("source_body_spans target set mismatch")
    if {row["target"] for row in orders} != target_names:
        raise RuntimeError("proof_order target set mismatch")
    indices = [int(row["proof_order_index"]) for row in orders]
    if sorted(indices) != list(range(1, expected_count + 1)):
        raise RuntimeError(f"proof order indices are not a 1..{expected_count} permutation")
    order_index = {row["target"]: int(row["proof_order_index"]) for row in orders}
    for order in orders:
        for dep in order["generated_target_dependencies"]:
            if dep in order_index and not order["cycle_or_unresolved_dependencies"]:
                if order_index[dep] >= int(order["proof_order_index"]):
                    raise RuntimeError(f"dependency ordered after dependent: {dep} -> {order['target']}")
    for span in spans:
        frozen_path = ROOT / span["frozen_relpath"]
        lines = frozen_path.read_text().splitlines(keepends=True)
        item_text = "".join(lines[int(span["signature_start_line"]) - 1 : int(span["body_end_line"])])
        if sha256_text(item_text) != span["source_item_sha256"]:
            raise RuntimeError(f"source item hash mismatch for {span['target']}")
        for rel_field in [
            "source_manifest_relpath",
            "transformation_manifest_relpath",
            "dependency_manifest_relpath",
            "harness_relpath",
        ]:
            if not (ROOT / span[rel_field]).is_file():
                raise FileNotFoundError(f"{span['target']}: missing {rel_field} {span[rel_field]}")
        trans = load_json(ROOT / span["transformation_manifest_relpath"])
        if trans.get("semantic_replacement") is not False:
            raise RuntimeError(f"{span['target']}: transformation manifest is not semantic-replacement-free")
        dep = load_json(ROOT / span["dependency_manifest_relpath"])
        target = next(row for row in targets if row["target"] == span["target"])
        target_status = str(target.get("proof_status", "")).split(":", 1)[0]
        dependency_status = str(dep.get("proof_status", "")).split(":", 1)[0]
        abcd_status = target.get("abcd_status", "")
        if abcd_status:
            if abcd_status not in {"A", "B", "C", "D"}:
                raise RuntimeError(f"{span['target']}: invalid A/B/C/D status {abcd_status!r}")
            if dependency_status != target_status:
                raise RuntimeError(f"{span['target']}: dependency manifest proof status disagrees with inventory")
        elif dep.get("proof_status") != "pending_actual_verus_implementation_proof":
            raise RuntimeError(f"{span['target']}: pending dependency manifest proof status is dishonest")
    pending_source = [row["target"] for row in targets if str(row.get("implementation_body_status", "")).startswith("pending")]
    if pending_source:
        raise RuntimeError(f"targets still pending source extraction: {pending_source[:5]}")
    print(
        "implproof extraction ok: "
        f"{len(spans)} source bodies, {len(orders)} proof-order rows, "
        f"{sum(1 for row in spans if row['private_helper_callee_count'])} targets with private helper candidates"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="replace generated extraction/manifests")
    parser.add_argument("--check", action="store_true", help="check generated extraction/manifests")
    args = parser.parse_args()
    if args.check:
        check_artifacts()
    else:
        extract_all(refresh=args.refresh)
        check_artifacts()


if __name__ == "__main__":
    main()
