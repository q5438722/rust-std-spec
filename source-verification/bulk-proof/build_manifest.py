#!/usr/bin/env python3
"""Build the all-vstd assume_specification source-proof campaign manifest."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import re
import sys
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_verus


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(HERE.parent))

from analyze_remaining import verified_new_stable_targets
from prepare_specgen_manifest import RustdocIndex
from survey import RustdocUniverse


VSTD_ROOT = WORKSPACE / "verus" / "source" / "vstd"
RUST_ROOT = WORKSPACE / "rust-1.96"
RUSTDOC_DIR = WORKSPACE / "rustdoc-json-1.96"


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", value).strip("_")


def normalize_api_path(path: str) -> str:
    return (
        path.replace(
            "alloc::collections::vec_deque::VecDeque::",
            "alloc::collections::VecDeque::",
        )
        .replace("core::fmt::Result::", "core::result::Result::")
    )


def walk(node):
    yield node
    for child in node.named_children:
        yield from walk(child)


def contract_nodes(path: Path) -> list[tuple[int, str, str]]:
    source = path.read_bytes()
    tree = Parser(Language(tree_sitter_verus.language())).parse(source)
    output = []
    for node in walk(tree.root_node):
        if node.type != "assume_specification_item":
            continue
        target = node.child_by_field_name("target")
        target_text = (
            source[target.start_byte : target.end_byte].decode(errors="replace")
            if target is not None
            else ""
        )
        output.append(
            (
                node.start_point.row + 1,
                source[node.start_byte : node.end_byte].decode(errors="replace"),
                target_text,
            )
        )
    return output


def contract_code(
    record: dict[str, Any],
    cache: dict[str, list[tuple[int, str, str]]],
) -> str:
    source_file = record["source_file"]
    if source_file not in cache:
        cache[source_file] = contract_nodes(VSTD_ROOT / source_file)
    nodes = cache[source_file]
    wanted = re.sub(r"\s+", "", record["raw_target"])
    target_matches = [
        code
        for _, code, target in nodes
        if re.sub(r"\s+", "", target) == wanted
    ]
    if len(target_matches) == 1:
        return target_matches[0]
    exact = [code for line, code, _ in nodes if line == int(record["source_line"])]
    if exact:
        return exact[0]
    text = (VSTD_ROOT / source_file).read_text(errors="replace")
    compact_chars = []
    compact_to_source = []
    for index, char in enumerate(text):
        if not char.isspace():
            compact_chars.append(char)
            compact_to_source.append(index)
    compact_text = "".join(compact_chars)
    search_at = 0
    while True:
        position = compact_text.find(wanted, search_at)
        if position < 0:
            break
        original = compact_to_source[position]
        assume = text.rfind("assume_specification", max(0, original - 4000), original + 1)
        if assume >= 0:
            start = text.rfind("\n", 0, assume) + 1
            if text[start:assume].strip() == "pub":
                pass
            elif text[max(0, assume - 4) : assume] == "pub ":
                start = assume - 4
            depth = 0
            for end in range(assume, len(text)):
                char = text[end]
                if char in "([{":
                    depth += 1
                elif char in ")]}":
                    depth = max(0, depth - 1)
                elif char == ";" and depth == 0:
                    candidate = text[start : end + 1].strip()
                    if wanted in re.sub(r"\s+", "", candidate):
                        return candidate
                    break
        search_at = position + 1
    if not nodes:
        return ""
    line, code, _ = min(
        nodes,
        key=lambda item: abs(item[0] - int(record["source_line"])),
    )
    return code if abs(line - int(record["source_line"])) <= 4 else ""


def span_text(span: dict[str, Any] | None) -> str:
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


def module_context(source_file: str) -> str:
    path = VSTD_ROOT / source_file
    if not path.is_file():
        return ""
    lines = path.read_text(errors="replace").splitlines()
    return "\n".join(f"{index + 1:>5}: {line}" for index, line in enumerate(lines[:80]))


def vstd_import(source_file: str) -> str:
    path = Path(source_file)
    module = "::".join(path.with_suffix("").parts)
    return f"vstd::{module}::*"


def function_name(raw_target: str) -> str:
    compact = re.sub(r"\s+", "", raw_target)
    match = re.search(r"::([A-Za-z_][A-Za-z0-9_]*)\s*(?:::<[^]]*>)?$", compact)
    return match.group(1) if match else compact.rsplit("::", 1)[-1]


def build_rust_api_index() -> tuple[dict[str, list[Any]], RustdocIndex]:
    universe = RustdocUniverse(RUSTDOC_DIR)
    by_path: dict[str, dict[str, Any]] = defaultdict(dict)
    for module in universe.modules:
        try:
            apis = universe.module_apis(module)
        except Exception:
            continue
        for api in apis:
            by_path[api.canonical_path][api.declaration_id] = api
    return {path: list(values.values()) for path, values in by_path.items()}, RustdocIndex(
        RUSTDOC_DIR
    )


def declaration_payload(
    declaration_id: str,
    rustdoc: RustdocIndex,
) -> dict[str, Any]:
    payload = rustdoc.declaration(declaration_id, RUST_ROOT, 20)
    payload["source_text"] = span_text(payload.get("span"))
    payload["has_body"] = "{" in payload["source_text"] and "}" in payload["source_text"]
    return payload


def preproved(record: dict[str, Any]) -> bool:
    if normalize_api_path(record["api_path"]) in verified_new_stable_targets():
        return True
    compact = re.sub(r"\s+", "", record["raw_target"])
    special = (
        "Result::<T,E>::branch",
        "Option::<T>::branch",
        "Option::<T>::from_residual",
        "Result::<T,F>::from_residual",
        "<VecDeque<T>ascore::default::Default>::default",
        "Vec::<T>::with_capacity",
        "VecDeque::<T>::with_capacity",
    )
    return any(value in compact for value in special)


def main() -> None:
    contracts = json.loads((WORKSPACE / "results" / "vstd_contracts.json").read_text())
    direct = [
        record
        for record in contracts
        if record["mechanism"] == "assume_specification"
        and record["confidence"] == "high"
    ]
    api_index, rustdoc = build_rust_api_index()
    contract_cache: dict[str, list[tuple[int, str, str]]] = {}
    targets = []
    for index, record in enumerate(
        sorted(direct, key=lambda item: (item["source_file"], item["source_line"], item["raw_target"]))
    ):
        normalized = normalize_api_path(record["api_path"])
        candidates = api_index.get(normalized, [])
        declarations = [
            declaration_payload(candidate.declaration_id, rustdoc)
            for candidate in candidates
        ]
        declarations.sort(
            key=lambda item: (
                not item["has_body"],
                item.get("visibility") != "public",
                item["declaration_id"],
            )
        )
        target_id = (
            f"{safe_name(record['source_file'])}__L{record['source_line']}__"
            f"{safe_name(record['raw_target'])}"
        )
        targets.append(
            {
                "id": target_id,
                "ordinal": index,
                "api_path": record["api_path"],
                "normalized_api_path": normalized,
                "raw_target": record["raw_target"],
                "function_name": function_name(record["raw_target"]),
                "contract_source_file": record["source_file"],
                "contract_source_line": record["source_line"],
                "contract_code": contract_code(record, contract_cache),
                "contract_module_context": module_context(record["source_file"]),
                "suggested_vstd_import": vstd_import(record["source_file"]),
                "preproved": preproved(record),
                "verification_declarations": declarations,
                "has_rust_1_96_body": any(item["has_body"] for item in declarations),
            }
        )

    counts = {
        "direct_assume_specification_records": len(targets),
        "preproved": sum(target["preproved"] for target in targets),
        "pending": sum(not target["preproved"] for target in targets),
        "pending_with_rust_1_96_body": sum(
            not target["preproved"] and target["has_rust_1_96_body"] for target in targets
        ),
        "pending_without_rust_1_96_body": sum(
            not target["preproved"] and not target["has_rust_1_96_body"] for target in targets
        ),
    }
    payload = {
        "metadata": {
            "vstd_root": str(VSTD_ROOT),
            "rust_root": str(RUST_ROOT),
            "rustdoc_dir": str(RUSTDOC_DIR),
        },
        "counts": counts,
        "targets": targets,
    }
    HERE.mkdir(parents=True, exist_ok=True)
    (HERE / "manifest.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
