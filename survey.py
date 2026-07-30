#!/usr/bin/env python3
"""Survey Rust standard-library APIs used by Nanvix and covered by Verus vstd."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Iterable

from tree_sitter import Language, Node, Parser
import tree_sitter_rust
import tree_sitter_verus


STANDARD_CRATES = ("core", "alloc", "std")
PATH_NODE_TYPES = {"scoped_identifier", "scoped_type_identifier"}
TYPE_KINDS = {"struct", "enum", "union", "primitive", "type_alias"}
TEST_PATH_PARTS = {"test", "tests", "benchmarks"}
PRIMITIVE_MODULES = {
    "array": "[T; N]",
    "char": "char",
    "f32": "f32",
    "f64": "f64",
    "ptr": "*const/*mut T",
    "slice": "[T]",
    "str": "str",
}
PRIMITIVE_NAMES = {
    "bool",
    "char",
    "f32",
    "f64",
    "i8",
    "i16",
    "i32",
    "i64",
    "i128",
    "isize",
    "str",
    "u8",
    "u16",
    "u32",
    "u64",
    "u128",
    "usize",
}
IGNORED_ROOT_PATHS = {
    ("alloc", "format"),
    ("std", "format"),
    ("std", "thread_local"),
}


@dataclass(frozen=True, order=True)
class ItemRef:
    crate: str
    item_id: str


@dataclass(frozen=True)
class ImportLeaf:
    path: tuple[str, ...]
    local_name: str | None
    is_glob: bool


@dataclass(frozen=True)
class UsageEvidence:
    module: str
    path: str
    file: str
    line: int
    syntax: str
    parser: str
    scope: str


@dataclass(frozen=True)
class ApiRecord:
    module: str
    display_path: str
    canonical_path: str
    origin_path: str
    kind: str
    declaration_id: str
    stability: str
    since: str
    is_const: bool
    is_unsafe: bool
    is_async: bool
    abi: str
    source_file: str
    source_line: int
    alias_approximate: bool


@dataclass(frozen=True)
class ContractRecord:
    api_path: str
    mechanism: str
    source_file: str
    source_line: int
    raw_target: str
    confidence: str


@dataclass(frozen=True)
class MacroDefinition:
    name: str
    params: tuple[str, ...]
    body: str
    source_file: str
    source_line: int


class RustdocCrate:
    def __init__(self, crate: str, path: Path) -> None:
        self.crate = crate
        self.data = json.loads(path.read_text())
        self.index: dict[str, dict[str, Any]] = self.data["index"]
        self.paths: dict[str, dict[str, Any]] = self.data["paths"]
        self.root_id = str(self.data["root"])
        self.local_crate_id = self.index[self.root_id]["crate_id"]

    def item(self, item_ref: ItemRef) -> dict[str, Any]:
        assert item_ref.crate == self.crate
        return self.index[item_ref.item_id]

    def kind(self, item_ref: ItemRef) -> str:
        return next(iter(self.item(item_ref)["inner"]))

    def local_path(self, item_id: str) -> tuple[str, ...] | None:
        entry = self.paths.get(item_id)
        if entry is None:
            return None
        return tuple(entry["path"])


class RustdocUniverse:
    """Public export graph and executable API inventory for core/alloc/std."""

    def __init__(self, rustdoc_dir: Path) -> None:
        self.docs = {
            crate: RustdocCrate(crate, rustdoc_dir / f"{crate}.json")
            for crate in STANDARD_CRATES
        }
        self.path_refs: dict[tuple[tuple[str, ...], str], ItemRef] = {}
        self.modules: dict[tuple[str, ...], set[ItemRef]] = {}
        self.exports: dict[tuple[str, ...], dict[str, set[ItemRef]]] = {}
        self.export_locations: dict[ItemRef, set[tuple[tuple[str, ...], str]]] = {}
        self.primitive_refs: dict[str, ItemRef] = {}
        self._expanded: set[tuple[tuple[str, ...], ItemRef]] = set()
        self._build_path_index()
        self._index_primitives()
        self._build_export_graph()
        self._index_export_locations()

    def _build_path_index(self) -> None:
        for crate, doc in self.docs.items():
            for item_id, entry in doc.paths.items():
                if item_id not in doc.index:
                    continue
                path = tuple(entry["path"])
                kind = entry["kind"]
                key = (path, kind)
                current = self.path_refs.get(key)
                candidate = ItemRef(crate, item_id)
                if current is None or path[0] == crate:
                    self.path_refs[key] = candidate

    def _index_primitives(self) -> None:
        for (path, kind), item_ref in self.path_refs.items():
            if kind == "primitive" and path and path[0] == "core":
                self.primitive_refs[path[-1]] = item_ref
                if path[-1] == "pointer":
                    self.primitive_refs["ptr"] = item_ref

    def resolve_ref(self, context_crate: str, item_id: int | str | None) -> ItemRef | None:
        if item_id is None:
            return None
        item_id = str(item_id)
        doc = self.docs[context_crate]
        if item_id in doc.index:
            return ItemRef(context_crate, item_id)
        entry = doc.paths.get(item_id)
        if entry is None:
            return None
        return self.path_refs.get((tuple(entry["path"]), entry["kind"]))

    def item(self, item_ref: ItemRef) -> dict[str, Any]:
        return self.docs[item_ref.crate].item(item_ref)

    def kind(self, item_ref: ItemRef) -> str:
        return self.docs[item_ref.crate].kind(item_ref)

    def public_path(self, item_ref: ItemRef) -> tuple[str, ...] | None:
        return self.docs[item_ref.crate].local_path(item_ref.item_id)

    @staticmethod
    def is_public(item: dict[str, Any]) -> bool:
        return item["visibility"] == "public"

    def _build_export_graph(self) -> None:
        for crate in STANDARD_CRATES:
            root = ItemRef(crate, self.docs[crate].root_id)
            self._walk_module((crate,), root)

    def _index_export_locations(self) -> None:
        for module_path, names in self.exports.items():
            for name, targets in names.items():
                for target in targets:
                    self.export_locations.setdefault(target, set()).add(
                        (module_path, name)
                    )

    def _add_export(
        self,
        module_path: tuple[str, ...],
        name: str,
        target: ItemRef,
    ) -> None:
        self.exports.setdefault(module_path, {}).setdefault(name, set()).add(target)

    def _walk_module(
        self,
        alias_path: tuple[str, ...],
        target: ItemRef,
        stack: tuple[ItemRef, ...] = (),
    ) -> None:
        self.modules.setdefault(alias_path, set()).add(target)
        if target in stack:
            return
        self._walk_module_contents(alias_path, target, stack + (target,))

    def _walk_module_contents(
        self,
        alias_path: tuple[str, ...],
        target: ItemRef,
        stack: tuple[ItemRef, ...],
    ) -> None:
        expansion_key = (alias_path, target)
        if expansion_key in self._expanded:
            return
        self._expanded.add(expansion_key)

        item = self.item(target)
        module = item["inner"].get("module")
        if module is None:
            return

        for child_id in module["items"]:
            child_ref = self.resolve_ref(target.crate, child_id)
            if child_ref is None:
                continue
            child = self.item(child_ref)
            child_kind = self.kind(child_ref)

            if child_kind == "use":
                if not self.is_public(child):
                    continue
                use = child["inner"]["use"]
                use_target = self.resolve_ref(child_ref.crate, use["id"])
                if use_target is None:
                    continue
                if use["is_glob"]:
                    if self.kind(use_target) == "module" and use_target not in stack:
                        self._walk_module_contents(
                            alias_path,
                            use_target,
                            stack + (use_target,),
                        )
                    continue
                name = use["name"]
                if name is None:
                    continue
                if self.kind(use_target) == "module":
                    self._walk_module(alias_path + (name,), use_target, stack)
                else:
                    self._add_export(alias_path, name, use_target)
                continue

            if not self.is_public(child):
                continue
            name = child["name"]
            if not name:
                continue
            if child_kind == "module":
                self._walk_module(alias_path + (name,), child_ref, stack)
            else:
                self._add_export(alias_path, name, child_ref)

    def resolve_usage(self, path: tuple[str, ...]) -> tuple[str, ...] | None:
        if len(path) < 2 or path[0] not in STANDARD_CRATES:
            return None
        for size in range(len(path), 0, -1):
            prefix = path[:size]
            if prefix not in self.modules:
                continue
            if size == len(path):
                return prefix
            if path[size] in self.exports.get(prefix, {}):
                if len(prefix) == 1:
                    targets = self.exports[prefix][path[size]]
                    preferred: list[tuple[str, ...]] = []
                    for target in targets:
                        for module_path, name in self.export_locations.get(
                            target, set()
                        ):
                            if (
                                name == path[size]
                                and len(module_path) > 1
                                and module_path[0] == path[0]
                                and "prelude" not in module_path
                            ):
                                preferred.append(module_path)
                    if preferred:
                        return sorted(preferred, key=lambda item: (len(item), item))[0]
                    for target in targets:
                        origin = self.public_path(target)
                        if (
                            origin is not None
                            and len(origin) > 2
                            and origin[:-1] in self.modules
                        ):
                            return origin[:-1]
                    return None
                return prefix
            if prefix + (path[size],) in self.modules:
                return prefix + (path[size],)
        return None

    def _origin_path(self, item_ref: ItemRef, fallback: tuple[str, ...]) -> str:
        path = self.public_path(item_ref)
        if path is None:
            path = fallback
        return "::".join(path)

    def preferred_export_path(
        self,
        item_ref: ItemRef,
        exported_name: str | None = None,
    ) -> tuple[str, ...] | None:
        candidates = []
        for module_path, name in self.export_locations.get(item_ref, set()):
            if exported_name is not None and name != exported_name:
                continue
            candidates.append(module_path + (name,))
        if candidates:
            return sorted(
                candidates,
                key=lambda path: (
                    "prelude" in path,
                    path[0] != item_ref.crate,
                    len(path),
                    path,
                ),
            )[0]
        path = self.public_path(item_ref)
        return path

    def resolve_symbol(
        self,
        name: str,
        aliases: dict[str, set[tuple[str, ...]]],
        glob_modules: set[tuple[str, ...]],
        expected_kinds: set[str] | None = None,
    ) -> tuple[str, ...] | None:
        alias_candidates = aliases.get(name, set())
        if alias_candidates:
            return sorted(alias_candidates, key=lambda path: (len(path), path))[0]

        candidates: list[tuple[tuple[str, ...], ItemRef]] = []
        for module_path in glob_modules:
            for target in self.exports.get(module_path, {}).get(name, set()):
                if expected_kinds is not None and self.kind(target) not in expected_kinds:
                    continue
                candidates.append((module_path + (name,), target))
        for target, locations in self.export_locations.items():
            if expected_kinds is not None and self.kind(target) not in expected_kinds:
                continue
            for module_path, exported_name in locations:
                if exported_name == name:
                    candidates.append((module_path + (name,), target))

        if not candidates:
            return None
        candidates.sort(
            key=lambda pair: (
                "prelude" in pair[0],
                pair[0][0] != pair[1].crate,
                len(pair[0]),
                pair[0],
            )
        )
        path, target = candidates[0]
        return self.preferred_export_path(target, name) or path


    @staticmethod
    def _stability(item: dict[str, Any]) -> tuple[str, str]:
        stability = item.get("stability")
        if not stability:
            return "unknown", ""
        return stability.get("level", "unknown"), stability.get("since") or ""

    @staticmethod
    def _function_header(item: dict[str, Any]) -> tuple[bool, bool, bool, str]:
        header = item["inner"]["function"]["header"]
        abi = header.get("abi", "")
        if isinstance(abi, dict):
            abi = abi.get("other", json.dumps(abi, sort_keys=True))
        return (
            bool(header.get("is_const")),
            bool(header.get("is_unsafe")),
            bool(header.get("is_async")),
            str(abi),
        )

    def _function_record(
        self,
        module_path: tuple[str, ...],
        display_path: tuple[str, ...],
        origin_owner: tuple[str, ...],
        function_ref: ItemRef,
        kind: str,
        alias_approximate: bool = False,
        canonical_owner: tuple[str, ...] | None = None,
    ) -> ApiRecord:
        item = self.item(function_ref)
        stability, since = self._stability(item)
        is_const, is_unsafe, is_async, abi = self._function_header(item)
        span = item.get("span") or {}
        begin = span.get("begin") or [0, 0]
        origin = origin_owner + (item["name"],)
        if kind == "free_function":
            canonical = self.preferred_export_path(function_ref) or origin
        else:
            canonical = (canonical_owner or origin_owner) + (item["name"],)
        return ApiRecord(
            module="::".join(module_path),
            display_path="::".join(display_path),
            canonical_path="::".join(canonical),
            origin_path=self._origin_path(function_ref, origin),
            kind=kind,
            declaration_id=f"{function_ref.crate}:{function_ref.item_id}",
            stability=stability,
            since=since,
            is_const=is_const,
            is_unsafe=is_unsafe,
            is_async=is_async,
            abi=abi,
            source_file=span.get("filename", ""),
            source_line=int(begin[0]),
            alias_approximate=alias_approximate,
        )

    def _inherent_methods(self, owner_ref: ItemRef) -> list[ItemRef]:
        item = self.item(owner_ref)
        kind = self.kind(owner_ref)
        body = item["inner"][kind]
        impl_ids = body.get("impls", []) if isinstance(body, dict) else []
        methods: list[ItemRef] = []
        for impl_id in impl_ids:
            impl_ref = self.resolve_ref(owner_ref.crate, impl_id)
            if impl_ref is None:
                continue
            impl = self.item(impl_ref)["inner"].get("impl")
            if impl is None or impl["trait"] is not None or impl.get("negative", False):
                continue
            for method_id in impl["items"]:
                method_ref = self.resolve_ref(impl_ref.crate, method_id)
                if method_ref is not None and self.kind(method_ref) == "function":
                    methods.append(method_ref)
        return methods

    @staticmethod
    def _resolved_type_id(type_data: Any) -> int | None:
        if not isinstance(type_data, dict):
            return None
        resolved = type_data.get("resolved_path")
        if resolved is not None:
            return resolved["id"]
        return None

    def _alias_methods(self, alias_ref: ItemRef) -> tuple[list[ItemRef], bool]:
        alias_item = self.item(alias_ref)
        alias_type = alias_item["inner"]["type_alias"]["type"]
        target_id = self._resolved_type_id(alias_type)
        target_ref = self.resolve_ref(alias_ref.crate, target_id)
        if target_ref is None or self.kind(target_ref) not in TYPE_KINDS - {"type_alias"}:
            return [], False

        target_item = self.item(target_ref)
        target_kind = self.kind(target_ref)
        impl_ids = target_item["inner"][target_kind].get("impls", [])
        exact: list[ItemRef] = []
        fallback: list[ItemRef] = []
        for impl_id in impl_ids:
            impl_ref = self.resolve_ref(target_ref.crate, impl_id)
            if impl_ref is None:
                continue
            impl = self.item(impl_ref)["inner"].get("impl")
            if impl is None or impl["trait"] is not None or impl.get("negative", False):
                continue
            destination = exact if impl["for"] == alias_type else fallback
            for method_id in impl["items"]:
                method_ref = self.resolve_ref(impl_ref.crate, method_id)
                if method_ref is not None and self.kind(method_ref) == "function":
                    destination.append(method_ref)
        if exact:
            return exact, False
        return fallback, bool(fallback)

    def module_apis(self, module_path: tuple[str, ...]) -> list[ApiRecord]:
        records: list[ApiRecord] = []
        seen: set[tuple[str, str, str]] = set()
        exports = self.exports.get(module_path, {})
        for exported_name, targets in sorted(exports.items()):
            for target in sorted(targets):
                kind = self.kind(target)
                item = self.item(target)
                target_origin = self.public_path(target) or module_path + (exported_name,)

                if kind == "function":
                    record = self._function_record(
                        module_path,
                        module_path + (exported_name,),
                        target_origin[:-1],
                        target,
                        "free_function",
                    )
                    key = (record.display_path, record.declaration_id, record.kind)
                    if key not in seen:
                        seen.add(key)
                        records.append(record)
                    continue

                if kind == "trait":
                    for method_id in item["inner"]["trait"]["items"]:
                        method_ref = self.resolve_ref(target.crate, method_id)
                        if method_ref is None or self.kind(method_ref) != "function":
                            continue
                        record = self._function_record(
                            module_path,
                            module_path + (exported_name, self.item(method_ref)["name"]),
                            target_origin,
                            method_ref,
                            "trait_method",
                            canonical_owner=self.preferred_export_path(
                                target, exported_name
                            )
                            or target_origin,
                        )
                        key = (record.display_path, record.declaration_id, record.kind)
                        if key not in seen:
                            seen.add(key)
                            records.append(record)
                    continue

                if kind in TYPE_KINDS:
                    approximate = False
                    if kind == "type_alias":
                        methods, approximate = self._alias_methods(target)
                    else:
                        methods = self._inherent_methods(target)
                    for method_ref in methods:
                        record = self._function_record(
                            module_path,
                            module_path + (exported_name, self.item(method_ref)["name"]),
                            target_origin,
                            method_ref,
                            "inherent_method",
                            approximate,
                            canonical_owner=self.preferred_export_path(
                                target, exported_name
                            )
                            or target_origin,
                        )
                        key = (record.display_path, record.declaration_id, record.kind)
                        if key not in seen:
                            seen.add(key)
                            records.append(record)

        primitive_name = module_path[-1]
        primitive_ref = self.primitive_refs.get(primitive_name)
        if primitive_ref is not None and primitive_name in PRIMITIVE_MODULES:
            primitive_origin = self.public_path(primitive_ref) or (
                "core",
                primitive_name,
            )
            owner = f"<{PRIMITIVE_MODULES[primitive_name]}>"
            for method_ref in self._inherent_methods(primitive_ref):
                record = self._function_record(
                    module_path,
                    module_path + (owner, self.item(method_ref)["name"]),
                    primitive_origin,
                    method_ref,
                    "primitive_method",
                    canonical_owner=("core", primitive_name),
                )
                key = (record.display_path, record.declaration_id, record.kind)
                if key not in seen:
                    seen.add(key)
                    records.append(record)
        return sorted(records, key=lambda row: (row.display_path, row.declaration_id))


def node_text(node: Node, source: bytes) -> str:
    return source[node.start_byte : node.end_byte].decode(errors="replace")


def path_segments(node: Node, source: bytes) -> tuple[str, ...]:
    if node.type in {
        "identifier",
        "type_identifier",
        "primitive_type",
        "self",
        "super",
        "crate",
    }:
        return (node_text(node, source).lstrip(":"),)
    if node.type in PATH_NODE_TYPES:
        path = node.child_by_field_name("path")
        name = node.child_by_field_name("name")
        segments: tuple[str, ...] = ()
        if path is not None:
            segments += path_segments(path, source)
        if name is not None:
            segments += path_segments(name, source)
        return tuple(part for part in segments if part)
    if node.type == "generic_type":
        type_node = node.child_by_field_name("type")
        return path_segments(type_node, source) if type_node is not None else ()
    text = node_text(node, source).strip().lstrip(":")
    return tuple(part for part in text.split("::") if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part))


def expand_use_node(
    node: Node,
    source: bytes,
    prefix: tuple[str, ...] = (),
) -> list[ImportLeaf]:
    if node.type == "use_list":
        leaves: list[ImportLeaf] = []
        for child in node.named_children:
            if child.type == "self":
                local = prefix[-1] if prefix else None
                leaves.append(ImportLeaf(prefix, local, False))
            else:
                leaves.extend(expand_use_node(child, source, prefix))
        return leaves

    if node.type == "scoped_use_list":
        path = node.child_by_field_name("path")
        use_list = node.child_by_field_name("list")
        base = prefix + (path_segments(path, source) if path is not None else ())
        return expand_use_node(use_list, source, base) if use_list is not None else []

    if node.type == "use_as_clause":
        path = node.child_by_field_name("path")
        alias = node.child_by_field_name("alias")
        full = prefix + (path_segments(path, source) if path is not None else ())
        local = node_text(alias, source) if alias is not None else (full[-1] if full else None)
        return [ImportLeaf(full, local, False)]

    if node.type == "use_wildcard":
        named = node.named_children
        base = prefix + (path_segments(named[0], source) if named else ())
        return [ImportLeaf(base, None, True)]

    segments = path_segments(node, source)
    full = prefix + segments
    return [ImportLeaf(full, full[-1] if full else None, False)]


def walk(node: Node) -> Iterable[Node]:
    yield node
    for child in node.named_children:
        yield from walk(child)


def has_ancestor(node: Node, node_type: str) -> bool:
    parent = node.parent
    while parent is not None:
        if parent.type == node_type:
            return True
        parent = parent.parent
    return False


def error_count(root: Node) -> int:
    return sum(node.type == "ERROR" for node in walk(root))


def source_scope(relative: Path) -> str:
    if any(part in TEST_PATH_PARTS for part in relative.parts):
        return "test_or_benchmark"
    return "production"


def canonicalize_path(
    path: tuple[str, ...],
    aliases: dict[str, set[tuple[str, ...]]],
) -> list[tuple[str, ...]]:
    if not path:
        return []
    first = path[0]
    if first in STANDARD_CRATES:
        return [path]
    candidates = aliases.get(first, set())
    return [candidate + path[1:] for candidate in sorted(candidates)]


def extract_alias_context(
    root: Node,
    source: bytes,
    universe: RustdocUniverse | None = None,
) -> tuple[dict[str, set[tuple[str, ...]]], set[tuple[str, ...]]]:
    aliases: dict[str, set[tuple[str, ...]]] = {}
    glob_modules: set[tuple[str, ...]] = set()
    for node in walk(root):
        if node.type == "extern_crate_declaration":
            name = node.child_by_field_name("name")
            alias = node.child_by_field_name("alias")
            if name is None:
                continue
            crate_name = node_text(name, source)
            if crate_name not in STANDARD_CRATES:
                continue
            local = node_text(alias, source) if alias is not None else crate_name
            aliases.setdefault(local, set()).add((crate_name,))
        elif node.type == "use_declaration":
            argument = node.child_by_field_name("argument")
            if argument is None:
                continue
            for leaf in expand_use_node(argument, source):
                if not leaf.path or leaf.path[0] not in STANDARD_CRATES:
                    continue
                if leaf.is_glob:
                    module = (
                        universe.resolve_usage(leaf.path)
                        if universe is not None
                        else leaf.path
                    )
                    if module is not None:
                        glob_modules.add(module)
                elif leaf.local_name:
                    aliases.setdefault(leaf.local_name, set()).add(leaf.path)
    return aliases, glob_modules


def strip_generic_arguments(text: str) -> str:
    output: list[str] = []
    depth = 0
    for char in text:
        if char == "<":
            depth += 1
            continue
        if char == ">" and depth:
            depth -= 1
            continue
        if depth == 0:
            output.append(char)
    return "".join(output).replace("::::", "::").rstrip(":")


def split_last_scope(text: str) -> tuple[str, str] | None:
    angle = square = paren = 0
    last = -1
    index = 0
    while index < len(text) - 1:
        char = text[index]
        if char == "<":
            angle += 1
        elif char == ">" and angle:
            angle -= 1
        elif char == "[":
            square += 1
        elif char == "]" and square:
            square -= 1
        elif char == "(":
            paren += 1
        elif char == ")" and paren:
            paren -= 1
        elif (
            char == ":"
            and text[index + 1] == ":"
            and angle == square == paren == 0
        ):
            last = index
            index += 1
        index += 1
    if last < 0:
        return None
    return text[:last], text[last + 2 :]


def strip_trailing_turbofish(text: str) -> str:
    text = text.rstrip()
    while text.endswith(">"):
        depth = 0
        opening = None
        for index in range(len(text) - 1, -1, -1):
            if text[index] == ">":
                depth += 1
            elif text[index] == "<":
                depth -= 1
                if depth == 0:
                    opening = index
                    break
        if opening is None or opening < 2 or text[opening - 2 : opening] != "::":
            break
        text = text[: opening - 2].rstrip()
    return text


def split_top_level_as(text: str) -> tuple[str, str] | None:
    angle = square = paren = 0
    index = 0
    while index <= len(text) - 4:
        char = text[index]
        if char == "<":
            angle += 1
        elif char == ">" and angle:
            angle -= 1
        elif char == "[":
            square += 1
        elif char == "]" and square:
            square -= 1
        elif char == "(":
            paren += 1
        elif char == ")" and paren:
            paren -= 1
        elif (
            text[index : index + 4] == " as "
            and angle == square == paren == 0
        ):
            return text[:index], text[index + 4 :]
        index += 1
    return None


def normalize_owner(
    owner: str,
    aliases: dict[str, set[tuple[str, ...]]],
    glob_modules: set[tuple[str, ...]],
    universe: RustdocUniverse,
    expected_kinds: set[str] | None = None,
) -> tuple[str, ...] | None:
    owner = owner.strip()
    owner = re.sub(r"^(?:&\s*(?:mut\s*)?)", "", owner)
    if owner.startswith("[") and owner.endswith("]"):
        return ("core", "array") if ";" in owner else ("core", "slice")
    if owner == "str":
        return ("core", "str")
    if owner in PRIMITIVE_NAMES:
        return ("core", owner)
    if owner == "()":
        return ("core", "tuple")

    plain = strip_generic_arguments(owner).strip().lstrip(":")
    parts = tuple(part for part in plain.split("::") if part)
    if not parts:
        return None
    if parts[0] in STANDARD_CRATES:
        return parts
    if parts[0] in aliases:
        base = sorted(aliases[parts[0]], key=lambda path: (len(path), path))[0]
        return base + parts[1:]
    if len(parts) == 1:
        return universe.resolve_symbol(
            parts[0],
            aliases,
            glob_modules,
            expected_kinds,
        )
    return None


def canonicalize_vstd_target(
    raw_target: str,
    aliases: dict[str, set[tuple[str, ...]]],
    glob_modules: set[tuple[str, ...]],
    universe: RustdocUniverse,
) -> str | None:
    raw = re.sub(r"\s+", " ", raw_target.strip())
    raw = strip_trailing_turbofish(raw)
    if "$" in raw:
        return None
    split = split_last_scope(raw)
    if split is None:
        return None
    owner, method = split
    method = strip_generic_arguments(method).strip()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", method):
        return None

    owner = owner.strip()
    if owner.startswith("<") and owner.endswith(">"):
        inner = owner[1:-1].strip()
        ufcs = split_top_level_as(inner)
        if ufcs is not None:
            _, trait = ufcs
            trait_path = normalize_owner(
                trait,
                aliases,
                glob_modules,
                universe,
                {"trait"},
            )
            if trait_path is None:
                return None
            return "::".join(trait_path + (method,))
        owner = inner

    owner_path = normalize_owner(
        owner,
        aliases,
        glob_modules,
        universe,
        TYPE_KINDS | {"module"},
    )
    if owner_path is None:
        return None
    return "::".join(owner_path + (method,))


def mask_comments_and_strings(text: str) -> str:
    chars = list(text)
    index = 0
    state = "code"
    while index < len(chars):
        if state == "code":
            if text.startswith("//", index):
                chars[index] = chars[index + 1] = " "
                index += 2
                state = "line_comment"
                continue
            if text.startswith("/*", index):
                chars[index] = chars[index + 1] = " "
                index += 2
                state = "block_comment"
                continue
            if chars[index] == '"':
                chars[index] = " "
                index += 1
                state = "string"
                continue
            if chars[index] == "'" and re.match(
                r"'(?:\\.|[^\\'])'",
                text[index : index + 4],
            ):
                chars[index] = " "
                index += 1
                state = "char"
                continue
        elif state == "line_comment":
            if chars[index] == "\n":
                state = "code"
            else:
                chars[index] = " "
            index += 1
            continue
        elif state == "block_comment":
            if text.startswith("*/", index):
                chars[index] = chars[index + 1] = " "
                index += 2
                state = "code"
            else:
                if chars[index] != "\n":
                    chars[index] = " "
                index += 1
            continue
        elif state in {"string", "char"}:
            if chars[index] == "\\":
                chars[index] = " "
                if index + 1 < len(chars):
                    chars[index + 1] = " "
                index += 2
                continue
            terminator = '"' if state == "string" else "'"
            if chars[index] == terminator:
                chars[index] = " "
                state = "code"
            elif chars[index] != "\n":
                chars[index] = " "
            index += 1
            continue
        index += 1
    return "".join(chars)


def find_matching(text: str, start: int, opening: str, closing: str) -> int | None:
    depth = 0
    for index in range(start, len(text)):
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return index
    return None


def extract_assume_targets(text: str) -> list[tuple[str, int]]:
    masked = mask_comments_and_strings(text)
    targets: list[tuple[str, int]] = []
    pattern = re.compile(r"\bassume_specification(?:\s*<[^;\[]*>)?\s*\[")
    for match in pattern.finditer(masked):
        start = masked.find("[", match.start())
        end = find_matching(masked, start, "[", "]")
        if end is None:
            continue
        line = text.count("\n", 0, start) + 1
        targets.append((text[start + 1 : end].strip(), line))
    return targets


def split_top_level_arguments(text: str) -> list[str]:
    arguments: list[str] = []
    angle = square = paren = brace = 0
    start = 0
    for index, char in enumerate(text):
        if char == "<":
            angle += 1
        elif char == ">" and angle:
            angle -= 1
        elif char == "[":
            square += 1
        elif char == "]" and square:
            square -= 1
        elif char == "(":
            paren += 1
        elif char == ")" and paren:
            paren -= 1
        elif char == "{":
            brace += 1
        elif char == "}" and brace:
            brace -= 1
        elif char == "," and angle == square == paren == brace == 0:
            arguments.append(text[start:index].strip())
            start = index + 1
    tail = text[start:].strip()
    if tail:
        arguments.append(tail)
    return arguments


def macro_calls_in_text(text: str) -> list[tuple[str, list[str]]]:
    masked = mask_comments_and_strings(text)
    calls: list[tuple[str, list[str]]] = []
    pattern = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*!\s*([\(\{\[])")
    for match in pattern.finditer(masked):
        opening = match.group(2)
        closing = {"(": ")", "{": "}", "[": "]"}[opening]
        start = match.end() - 1
        end = find_matching(masked, start, opening, closing)
        if end is None:
            continue
        calls.append(
            (
                match.group(1),
                split_top_level_arguments(text[start + 1 : end]),
            )
        )
    return calls


def extract_external_trait_contracts(
    text: str,
    relative: str,
    aliases: dict[str, set[tuple[str, ...]]],
    glob_modules: set[tuple[str, ...]],
    universe: RustdocUniverse,
) -> list[ContractRecord]:
    masked = mask_comments_and_strings(text)
    records: list[ContractRecord] = []
    marker = re.compile(r"#\s*\[\s*verifier::external_trait_specification\s*\]")
    for match in marker.finditer(masked):
        trait_match = re.search(
            r"\bpub\s+trait\s+[A-Za-z_][A-Za-z0-9_]*(?:\s*<[^{};]*>)?[^{]*\{",
            masked[match.end() :],
        )
        if trait_match is None:
            continue
        trait_start = match.end() + trait_match.start()
        brace = masked.find("{", trait_start)
        end = find_matching(masked, brace, "{", "}")
        if end is None:
            continue
        body = text[brace + 1 : end]
        target_match = re.search(
            r"\btype\s+ExternalTraitSpecificationFor\s*:\s*([^;]+);",
            body,
        )
        if target_match is None:
            continue
        trait_path = normalize_owner(
            target_match.group(1),
            aliases,
            glob_modules,
            universe,
            {"trait"},
        )
        if trait_path is None:
            continue

        visible = list(mask_comments_and_strings(body))
        depth = 0
        for index, char in enumerate(visible):
            if char == "{":
                depth += 1
                visible[index] = " "
            elif char == "}":
                visible[index] = " "
                depth = max(depth - 1, 0)
            elif depth:
                if char != "\n":
                    visible[index] = " "
        top_level = "".join(visible)
        fn_pattern = re.compile(
            r"\b(?:(spec|proof|exec)\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)"
        )
        for fn_match in fn_pattern.finditer(top_level):
            mode = fn_match.group(1)
            if mode in {"spec", "proof"}:
                continue
            method = fn_match.group(2)
            line = text.count("\n", 0, brace + 1 + fn_match.start()) + 1
            records.append(
                ContractRecord(
                    api_path="::".join(trait_path + (method,)),
                    mechanism="external_trait_specification",
                    source_file=relative,
                    source_line=line,
                    raw_target=target_match.group(1).strip() + "::" + method,
                    confidence="high",
                )
            )
    return records


def extract_vstd_contracts(
    vstd_root: Path,
    universe: RustdocUniverse,
) -> tuple[list[ContractRecord], dict[str, Any]]:
    parser = Parser(Language(tree_sitter_verus.language()))
    file_context: dict[
        str,
        tuple[
            str,
            dict[str, set[tuple[str, ...]]],
            set[tuple[str, ...]],
            Node,
            bytes,
        ],
    ] = {}
    macro_defs: dict[str, list[MacroDefinition]] = {}
    macro_calls: list[tuple[str, list[str], str, int]] = []
    records: list[ContractRecord] = []
    parse_error_files = 0
    lexical_assume_targets = 0
    lexical_non_template_targets = 0
    lexical_canonical_targets = 0
    lexical_unresolved_non_template: list[dict[str, Any]] = []

    for path in sorted(vstd_root.rglob("*.rs")):
        relative = str(path.relative_to(vstd_root))
        text = path.read_text(errors="replace")
        parse_text = re.sub(r"\bverus_!", "verus!", text)
        source = parse_text.encode()
        tree = parser.parse(source)
        if error_count(tree.root_node):
            parse_error_files += 1
        aliases, glob_modules = extract_alias_context(
            tree.root_node,
            source,
            universe,
        )
        file_context[relative] = (
            text,
            aliases,
            glob_modules,
            tree.root_node,
            source,
        )

        for raw_target, line in extract_assume_targets(text):
            lexical_assume_targets += 1
            if "$" not in raw_target:
                lexical_non_template_targets += 1
            canonical = canonicalize_vstd_target(
                raw_target,
                aliases,
                glob_modules,
                universe,
            )
            if canonical is not None:
                lexical_canonical_targets += 1
                records.append(
                    ContractRecord(
                        api_path=canonical,
                        mechanism="assume_specification",
                        source_file=relative,
                        source_line=line,
                        raw_target=raw_target,
                        confidence="high",
                    )
                )
            elif "$" not in raw_target:
                lexical_unresolved_non_template.append(
                    {
                        "source_file": relative,
                        "source_line": line,
                        "raw_target": raw_target,
                    }
                )

        for node in walk(tree.root_node):
            if node.type == "assume_specification_item":
                target = node.child_by_field_name("target")
                if target is None:
                    continue
                raw_target = node_text(target, source)
                canonical = canonicalize_vstd_target(
                    raw_target,
                    aliases,
                    glob_modules,
                    universe,
                )
                if canonical is not None:
                    records.append(
                        ContractRecord(
                            api_path=canonical,
                            mechanism="assume_specification",
                            source_file=relative,
                            source_line=node.start_point.row + 1,
                            raw_target=raw_target,
                            confidence="high",
                        )
                    )

            elif node.type == "macro_definition":
                name_node = node.child_by_field_name("name")
                if name_node is None:
                    continue
                name = node_text(name_node, source)
                for rule in node.named_children:
                    if rule.type != "macro_rule":
                        continue
                    left = rule.child_by_field_name("left")
                    right = rule.child_by_field_name("right")
                    if left is None or right is None:
                        continue
                    params = tuple(
                        dict.fromkeys(
                            re.findall(r"\$([A-Za-z_][A-Za-z0-9_]*)", node_text(left, source))
                        )
                    )
                    body = node_text(right, source)
                    if len(body) >= 2 and body[0] in "({[":
                        body = body[1:-1]
                    macro_defs.setdefault(name, []).append(
                        MacroDefinition(
                            name=name,
                            params=params,
                            body=body,
                            source_file=relative,
                            source_line=node.start_point.row + 1,
                        )
                    )

            elif node.type == "macro_invocation" and not has_ancestor(
                node, "macro_definition"
            ):
                name_node = node.child_by_field_name("macro")
                token_tree = next(
                    (
                        child
                        for child in node.named_children
                        if child.type == "token_tree"
                    ),
                    None,
                )
                if name_node is None or token_tree is None:
                    continue
                body = node_text(token_tree, source)
                if len(body) >= 2:
                    body = body[1:-1]
                macro_calls.append(
                    (
                        node_text(name_node, source),
                        split_top_level_arguments(body),
                        relative,
                        node.start_point.row + 1,
                    )
                )

        records.extend(
            extract_external_trait_contracts(
                text,
                relative,
                aliases,
                glob_modules,
                universe,
            )
        )

    macro_expansion_errors: list[dict[str, Any]] = []
    relevant_macros = {
        name
        for name, definitions in macro_defs.items()
        if any("assume_specification" in definition.body for definition in definitions)
    }
    changed = True
    while changed:
        changed = False
        for name, definitions in macro_defs.items():
            if name in relevant_macros:
                continue
            nested = {
                nested_name
                for definition in definitions
                for nested_name, _ in macro_calls_in_text(definition.body)
            }
            if nested & relevant_macros:
                relevant_macros.add(name)
                changed = True

    def expand_macro(
        name: str,
        args: list[str],
        call_file: str,
        call_line: int,
        stack: tuple[str, ...] = (),
    ) -> None:
        if len(stack) >= 12 or name in stack:
            return
        definitions = macro_defs.get(name, [])
        matched = False
        for definition in definitions:
            if len(definition.params) != len(args):
                continue
            matched = True
            rendered = definition.body
            for param, value in zip(definition.params, args):
                rendered = re.sub(rf"\${re.escape(param)}\b", value, rendered)
            context = file_context[definition.source_file]
            _, aliases, glob_modules, _, _ = context
            for raw_target, relative_line in extract_assume_targets(rendered):
                canonical = canonicalize_vstd_target(
                    raw_target,
                    aliases,
                    glob_modules,
                    universe,
                )
                if canonical is None:
                    continue
                records.append(
                    ContractRecord(
                        api_path=canonical,
                        mechanism=f"macro:{name}",
                        source_file=call_file,
                        source_line=call_line,
                        raw_target=raw_target,
                        confidence="macro_inferred",
                    )
                )
            for nested_name, nested_args in macro_calls_in_text(rendered):
                if nested_name == "verus":
                    continue
                expand_macro(
                    nested_name,
                    nested_args,
                    call_file,
                    call_line,
                    stack + (name,),
                )
        if definitions and not matched:
            macro_expansion_errors.append(
                {
                    "macro": name,
                    "argument_count": len(args),
                    "source_file": call_file,
                    "source_line": call_line,
                }
            )

    for name, args, source_file, source_line in macro_calls:
        if name in relevant_macros:
            expand_macro(name, args, source_file, source_line)

    unique = sorted(
        set(records),
        key=lambda row: (
            row.api_path,
            row.source_file,
            row.source_line,
            row.mechanism,
        ),
    )
    metadata = {
        "vstd_files": len(file_context),
        "parse_error_files": parse_error_files,
        "contract_records": len(unique),
        "unique_contract_paths": len({row.api_path for row in unique}),
        "lexical_assume_targets": lexical_assume_targets,
        "lexical_non_template_targets": lexical_non_template_targets,
        "lexical_canonical_targets": lexical_canonical_targets,
        "lexical_unresolved_non_template": lexical_unresolved_non_template,
        "mechanisms": {
            mechanism: sum(row.mechanism == mechanism for row in unique)
            for mechanism in sorted({row.mechanism for row in unique})
        },
        "macro_expansion_errors": macro_expansion_errors,
    }
    return unique, metadata


def api_match_keys(record: ApiRecord) -> set[str]:
    keys = {record.display_path, record.canonical_path, record.origin_path}
    normalized = set()
    for key in keys:
        normalized.add(re.sub(r"::<[^>]+>", "", key))
        normalized.add(
            key.replace("::<[T]>", "")
            .replace("::<[T; N]>", "")
            .replace("::<str>", "")
            .replace("::<char>", "")
            .replace("::<f32>", "")
            .replace("::<f64>", "")
        )
    return {key.replace("::::", "::") for key in keys | normalized}


def git_tracked_rust_files(repo: Path) -> list[Path]:
    output = subprocess.check_output(
        ["git", "-C", str(repo), "ls-files", "-z", "*.rs"],
    )
    return [repo / name.decode() for name in output.split(b"\0") if name]


def extract_nanvix_usage(
    nanvix_root: Path,
    universe: RustdocUniverse,
) -> tuple[list[UsageEvidence], dict[str, Any]]:
    rust_parser = Parser(Language(tree_sitter_rust.language()))
    verus_parser = Parser(Language(tree_sitter_verus.language()))
    evidences: set[UsageEvidence] = set()
    unresolved: list[dict[str, Any]] = []
    parser_counts = {"rust": 0, "verus": 0}
    parse_error_files = 0

    for path in git_tracked_rust_files(nanvix_root):
        source = path.read_bytes()
        relative = path.relative_to(nanvix_root)
        scope = source_scope(relative)
        verus_like = bool(
            re.search(
                rb"\bverus_?\s*!\s*\{|\b(?:spec|proof)\s+fn\b|\b(?:requires|ensures)\b",
                source,
            )
        )
        primary_name = "verus" if verus_like else "rust"
        primary = verus_parser if verus_like else rust_parser
        secondary_name = "rust" if verus_like else "verus"
        secondary = rust_parser if verus_like else verus_parser
        tree = primary.parse(source)
        primary_errors = error_count(tree.root_node)
        if primary_errors:
            alternate = secondary.parse(source)
            alternate_errors = error_count(alternate.root_node)
            if alternate_errors < primary_errors:
                tree = alternate
                primary_name = secondary_name
                primary_errors = alternate_errors
        parser_counts[primary_name] += 1
        if primary_errors:
            parse_error_files += 1

        aliases: dict[str, set[tuple[str, ...]]] = {}
        imports: list[tuple[ImportLeaf, int]] = []
        for node in walk(tree.root_node):
            if node.type == "extern_crate_declaration":
                name = node.child_by_field_name("name")
                alias = node.child_by_field_name("alias")
                if name is None:
                    continue
                crate_name = node_text(name, source)
                if crate_name not in STANDARD_CRATES:
                    continue
                local = node_text(alias, source) if alias is not None else crate_name
                aliases.setdefault(local, set()).add((crate_name,))
                imports.append((ImportLeaf((crate_name,), local, False), node.start_point.row + 1))
            elif node.type == "use_declaration":
                argument = node.child_by_field_name("argument")
                if argument is None:
                    continue
                for leaf in expand_use_node(argument, source):
                    imports.append((leaf, node.start_point.row + 1))
                    if leaf.local_name and leaf.path and leaf.path[0] in STANDARD_CRATES:
                        aliases.setdefault(leaf.local_name, set()).add(leaf.path)

        def add_path(
            raw_path: tuple[str, ...],
            line: int,
            syntax: str,
        ) -> None:
            if len(raw_path) < 2 or raw_path in IGNORED_ROOT_PATHS:
                return
            for canonical in canonicalize_path(raw_path, aliases):
                module = universe.resolve_usage(canonical)
                if module is None:
                    unresolved.append(
                        {
                            "path": "::".join(canonical),
                            "file": str(relative),
                            "line": line,
                            "syntax": syntax,
                            "parser": primary_name,
                            "scope": scope,
                        }
                    )
                    continue
                evidences.add(
                    UsageEvidence(
                        module="::".join(module),
                        path="::".join(canonical),
                        file=str(relative),
                        line=line,
                        syntax=syntax,
                        parser=primary_name,
                        scope=scope,
                    )
                )

        for leaf, line in imports:
            add_path(leaf.path, line, "glob_import" if leaf.is_glob else "import")

        for node in walk(tree.root_node):
            if node.type not in PATH_NODE_TYPES:
                continue
            if has_ancestor(node, "use_declaration") or has_ancestor(
                node, "extern_crate_declaration"
            ):
                continue
            if node.parent is not None and node.parent.type in PATH_NODE_TYPES:
                continue
            segments = path_segments(node, source)
            add_path(segments, node.start_point.row + 1, "qualified_path")

    metadata = {
        "rust_files": len(git_tracked_rust_files(nanvix_root)),
        "parser_counts": parser_counts,
        "parse_error_files": parse_error_files,
        "unresolved_evidence_count": len(unresolved),
        "unresolved": sorted(
            unresolved,
            key=lambda row: (row["path"], row["file"], row["line"]),
        ),
    }
    return sorted(
        evidences,
        key=lambda row: (row.module, row.file, row.line, row.path),
    ), metadata


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    metadata: dict[str, Any],
    summary: dict[str, Any],
    module_rows: list[dict[str, Any]],
) -> None:
    production = summary["production"]
    all_sources = summary["all_tracked_sources"]
    production_module_count = metadata["scope"]["production_modules"]
    all_module_count = metadata["scope"]["all_modules"]
    gaps = sorted(
        (
            row
            for row in module_rows
            if row["used_in_production"]
            and row["uncovered_stable_unique_api_paths"]
        ),
        key=lambda row: (
            row["uncovered_stable_unique_api_paths"],
            row["stable_unique_api_paths"],
        ),
        reverse=True,
    )

    lines = [
        "# Verus vstd coverage of Nanvix-used Rust std APIs",
        "",
        "This workspace measures the Rust `core`/`alloc`/`std` modules used by "
        "Nanvix and compares their public executable APIs with direct Rust API "
        "contracts in Verus vstd.",
        "",
        "## Main result",
        "",
        "| Scope | Used modules | Modules with exec APIs | Module-listed API paths | "
        "Deduplicated API paths | Covered by vstd | Uncovered | Coverage |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        f"| Production source | {production_module_count} | {production['modules']} | "
        f"{production['module_unique_display_paths']} | "
        f"{production['deduplicated_api_paths']} | "
        f"{production['covered_deduplicated_api_paths']} | "
        f"{production['uncovered_deduplicated_api_paths']} | "
        f"{production['deduplicated_path_coverage_percent']:.2f}% |",
        f"| Production, stable APIs only | {production_module_count} | "
        f"{production['modules']} | - | "
        f"{production['stable_deduplicated_api_paths']} | "
        f"{production['covered_stable_deduplicated_api_paths']} | "
        f"{production['uncovered_stable_deduplicated_api_paths']} | "
        f"{production['stable_deduplicated_path_coverage_percent']:.2f}% |",
        f"| All tracked source, including tests/benchmarks | {all_module_count} | "
        f"{all_sources['modules']} | {all_sources['module_unique_display_paths']} | "
        f"{all_sources['deduplicated_api_paths']} | "
        f"{all_sources['covered_deduplicated_api_paths']} | "
        f"{all_sources['uncovered_deduplicated_api_paths']} | "
        f"{all_sources['deduplicated_path_coverage_percent']:.2f}% |",
        "",
        "The production result is the primary number. The module-listed count "
        "retains public aliases such as both `core::mem` and `std::mem`; the "
        "deduplicated count collapses those aliases to one canonical Rust API.",
        "",
        "The only test/benchmark-only module is `core::arch::x86`, whose 6,144 "
        "intrinsic functions dominate the all-source total.",
        "",
        "## Source snapshots",
        "",
        "| Source | Commit | Branch/toolchain | Remote |",
        "|---|---|---|---|",
        f"| Nanvix | `{metadata['nanvix']['commit']}` | "
        f"`{metadata['nanvix']['branch']}` | `{metadata['nanvix']['remote']}` |",
        f"| rust-lang/rust | `{metadata['rust']['commit']}` | "
        f"`{metadata['rust_toolchain']}` | `{metadata['rust']['remote']}` |",
        f"| Verus vstd | `{metadata['verus']['commit']}` | "
        f"`{metadata['verus']['branch']}` | `{metadata['verus']['remote']}` |",
        "",
        "## Counting model",
        "",
        "- Nanvix usage is extracted from every Git-tracked `.rs` file. "
        "tree-sitter-rust parses ordinary Rust; tree-sitter-verus parses files "
        "containing Verus syntax.",
        "- A used module is the longest public `core`/`alloc`/`std` module prefix "
        "resolved through Rust public reexports and local aliases.",
        "- An exec API is a public free function, inherent method, primitive "
        "method, or trait method. Associated constants and macros are excluded.",
        "- Rust API enumeration comes from rustdoc JSON built from the pinned "
        "Rust sources, so macro-generated atomic, primitive, and architecture "
        "functions are included.",
        "- vstd coverage includes direct `assume_specification` contracts, "
        "external trait specifications, and statically expanded atomic, number, "
        "and default-value contract macros.",
        "- Coverage is path-level. Two covered production paths have multiple "
        "Rust declaration signatures: `Option::cloned` and "
        "`str::from_utf8_unchecked`.",
        "",
        "## Data quality",
        "",
        f"- Nanvix: {metadata['scope']['tracked_rust_files']} tracked Rust files, "
        f"{metadata['usage_parser']['parse_error_files']} parse-error files, and "
        f"{metadata['usage_parser']['unresolved_evidence_count']} unresolved path "
        "evidence. The only unresolved path is test-local `alloc::run`, which is "
        "not the Rust `alloc` crate.",
        f"- Parser selection: {metadata['usage_parser']['parser_counts']['rust']} "
        "files used tree-sitter-rust and "
        f"{metadata['usage_parser']['parser_counts']['verus']} used "
        "tree-sitter-verus.",
        f"- Verus vstd: {summary['vstd']['contract_records']} contract evidence "
        f"records and {summary['vstd']['unique_contract_paths']} unique Rust API "
        "paths.",
        f"- The lexical fallback canonicalized "
        f"{metadata['vstd_parser']['lexical_canonical_targets']} of "
        f"{metadata['vstd_parser']['lexical_non_template_targets']} non-template "
        "`assume_specification` targets.",
        "",
        "## Largest stable production gaps",
        "",
        "| Module | Stable API paths | Covered | Uncovered |",
        "|---|---:|---:|---:|",
    ]
    for row in gaps[:25]:
        lines.append(
            f"| `{row['module']}` | {row['stable_unique_api_paths']} | "
            f"{row['covered_stable_unique_api_paths']} | "
            f"{row['uncovered_stable_unique_api_paths']} |"
        )

    lines.extend(
        [
            "",
            "## Complete module list",
            "",
            "| Module | Scope | Source files | Exec APIs | Stable APIs | "
            "vstd covered | vstd uncovered (stable) |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in sorted(module_rows, key=lambda item: item["module"]):
        scope = "production" if row["used_in_production"] else "test/benchmark only"
        lines.append(
            f"| `{row['module']}` | {scope} | {row['source_file_count']} | "
            f"{row['unique_api_paths']} | "
            f"{row['stable_unique_api_paths']} | "
            f"{row['covered_unique_api_paths']} | "
            f"{row['uncovered_stable_unique_api_paths']} |"
        )

    lines.extend(
        [
            "",
            "## Important limitations",
            "",
            "- This is a source-wide cfg union, not one concrete Nanvix target "
            "build. Unix, Windows, kernel, user, and tool code are all included.",
            "- Module-complete counting intentionally includes APIs that Nanvix "
            "does not call directly. The experiment asks whether every API in a "
            "used module already has a vstd contract.",
            "- tree-sitter cannot resolve the receiver type of an arbitrary "
            "instance method call. Explicit imports, aliases, associated calls, "
            "and qualified paths still provide module evidence.",
            "- vstd operator/conversion repetition macros are not fully expanded; "
            "their public trait methods are already represented by external trait "
            "specifications, so this does not remove those API paths from coverage.",
            "- Type aliases that do not exactly match one rustdoc inherent impl "
            "are conservatively propagated and marked by "
            "`alias_approximate=true` in the detailed CSV.",
            "- Many uncovered APIs are I/O, OS, formatting, synchronization, or "
            "runtime effects. They should be semantically triaged before treating "
            "them as ordinary postcondition-generation targets.",
            "",
            "## Artifacts",
            "",
            "- `results/modules.csv`: complete module list and per-module coverage.",
            "- `results/complete_modules.csv`: concise module list using the report "
            "column order.",
            "- `results/usage_evidence.csv`: Nanvix source evidence for each module.",
            "- `results/rust_exec_apis.csv`: every module-listed Rust exec API.",
            "- `results/vstd_contracts.csv`: extracted vstd Rust API contracts.",
            "- `results/coverage.csv`: path-level API-to-contract match.",
            "- `results/uncovered_production_apis.csv`: deduplicated production gaps.",
            "- `results/uncovered_production_stable_apis.csv`: stable production "
            "gap list recommended for semantic triage.",
            "- `results/uncovered_all_apis.csv`: all-source gaps including tests.",
            "- `results/summary.json` and `results/metadata.json`: aggregate counts "
            "and exact source revisions.",
            "",
            "## Reproduce",
            "",
            "The source checkouts and rustdoc JSON already exist in this workspace. "
            "To rerun the analysis:",
            "",
            "```bash",
            "cd /home/chentianyu/nanvix-rust-std-spec-survey",
            "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python survey.py",
            "```",
            "",
            "The source snapshots were created with:",
            "",
            "```bash",
            "git clone git@github.com:nanvix/nanvix.git nanvix",
            "git -C nanvix checkout --detach "
            "bac7075214a385b0088145eb0738cc0c4f121feb",
            "git clone --filter=blob:none --no-checkout --depth 1 "
            "https://github.com/rust-lang/rust.git rust",
            "git -C rust fetch --depth 1 origin "
            "14cae681329a63c622a6e1fbe1d30f9374bc51d8",
            "git -C rust sparse-checkout init --cone",
            "git -C rust sparse-checkout set library",
            "git -C rust checkout --detach "
            "14cae681329a63c622a6e1fbe1d30f9374bc51d8",
            "git -C rust submodule update --init --depth 1 library/backtrace",
            "git clone --filter=blob:none --sparse "
            "https://github.com/verus-lang/verus.git verus",
            "git -C verus sparse-checkout set source/vstd",
            "git -C verus checkout --detach "
            "1beb0fad337b8f8a224cf8684162cb02d0c2fc01",
            "python -m venv --system-site-packages .venv",
            ".venv/bin/python -m pip install tree-sitter-rust",
            "```",
            "",
            "To regenerate the macro-expanded Rust API JSON:",
            "",
            "```bash",
            "cd rust/library",
            "for crate in core alloc std; do",
            "  CARGO_TARGET_DIR=../../rustdoc-target RUSTC_BOOTSTRAP=1 \\",
            "    cargo +nightly-2026-07-09 rustdoc -p \"$crate\" --lib -- \\",
            "    -Z unstable-options --output-format json",
            "done",
            "mkdir -p ../../rustdoc-json",
            "cp ../../rustdoc-target/doc/{core,alloc,std}.json ../../rustdoc-json/",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def write_main_results(
    path: Path,
    metadata: dict[str, Any],
    summary: dict[str, Any],
    module_rows: list[dict[str, Any]],
) -> None:
    production = summary["production"]
    all_sources = summary["all_tracked_sources"]
    lines = [
        "# Verus vstd coverage of Nanvix-used Rust std APIs",
        "",
        "## Main result",
        "",
        "| Scope | Used modules | Modules with exec APIs | Module-listed API paths | "
        "Deduplicated API paths | Covered by vstd | Uncovered | Coverage |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        f"| Production source | {metadata['scope']['production_modules']} | "
        f"{production['modules']} | {production['module_unique_display_paths']} | "
        f"{production['deduplicated_api_paths']} | "
        f"{production['covered_deduplicated_api_paths']} | "
        f"{production['uncovered_deduplicated_api_paths']} | "
        f"{production['deduplicated_path_coverage_percent']:.2f}% |",
        f"| Production, stable APIs only | "
        f"{metadata['scope']['production_modules']} | {production['modules']} | "
        f"- | {production['stable_deduplicated_api_paths']} | "
        f"{production['covered_stable_deduplicated_api_paths']} | "
        f"{production['uncovered_stable_deduplicated_api_paths']} | "
        f"{production['stable_deduplicated_path_coverage_percent']:.2f}% |",
        f"| All tracked source, including tests/benchmarks | "
        f"{metadata['scope']['all_modules']} | {all_sources['modules']} | "
        f"{all_sources['module_unique_display_paths']} | "
        f"{all_sources['deduplicated_api_paths']} | "
        f"{all_sources['covered_deduplicated_api_paths']} | "
        f"{all_sources['uncovered_deduplicated_api_paths']} | "
        f"{all_sources['deduplicated_path_coverage_percent']:.2f}% |",
        "",
        "## Complete module list",
        "",
        "| Module | Scope | Source files | Exec APIs | Stable APIs | "
        "vstd covered | vstd uncovered (stable) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in sorted(module_rows, key=lambda item: item["module"]):
        scope = "production" if row["used_in_production"] else "test/benchmark only"
        lines.append(
            f"| `{row['module']}` | {scope} | {row['source_file_count']} | "
            f"{row['unique_api_paths']} | {row['stable_unique_api_paths']} | "
            f"{row['covered_unique_api_paths']} | "
            f"{row['uncovered_stable_unique_api_paths']} |"
        )
    lines.append("")
    path.write_text("\n".join(lines))


def git_metadata(repo: Path) -> dict[str, str]:
    return {
        "path": str(repo),
        "commit": subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            text=True,
        ).strip(),
        "branch": subprocess.check_output(
            ["git", "-C", str(repo), "branch", "--show-current"],
            text=True,
        ).strip(),
        "remote": subprocess.check_output(
            ["git", "-C", str(repo), "remote", "get-url", "origin"],
            text=True,
        ).strip(),
    }


def run(args: argparse.Namespace) -> int:
    universe = RustdocUniverse(args.rustdoc_dir)
    evidence, usage_metadata = extract_nanvix_usage(args.nanvix_root, universe)
    contracts, vstd_metadata = extract_vstd_contracts(args.vstd_root, universe)
    production_modules = sorted(
        {row.module for row in evidence if row.scope == "production"}
    )
    all_modules = sorted({row.module for row in evidence})

    api_rows: list[ApiRecord] = []
    module_rows: list[dict[str, Any]] = []
    for module in all_modules:
        module_path = tuple(module.split("::"))
        records = universe.module_apis(module_path)
        api_rows.extend(records)
        module_evidence = [row for row in evidence if row.module == module]
        production_evidence = [
            row for row in module_evidence if row.scope == "production"
        ]
        module_rows.append(
            {
                "module": module,
                "used_in_production": bool(production_evidence),
                "evidence_count": len(module_evidence),
                "production_evidence_count": len(production_evidence),
                "source_file_count": len({row.file for row in module_evidence}),
                "production_source_file_count": len(
                    {row.file for row in production_evidence}
                ),
                "exec_declarations": len(records),
                "unique_api_paths": len({row.display_path for row in records}),
                "stable_unique_api_paths": len(
                    {
                        row.display_path
                        for row in records
                        if row.stability == "stable"
                    }
                ),
                "stable_declarations": sum(
                    row.stability == "stable" for row in records
                ),
                "unstable_declarations": sum(
                    row.stability == "unstable" for row in records
                ),
                "approximate_alias_declarations": sum(
                    row.alias_approximate for row in records
                ),
            }
        )

    contract_index: dict[str, list[ContractRecord]] = {}
    for contract in contracts:
        contract_index.setdefault(contract.api_path, []).append(contract)

    coverage_rows: list[dict[str, Any]] = []
    for record in api_rows:
        matches = {
            contract
            for key in api_match_keys(record)
            for contract in contract_index.get(key, [])
        }
        row = asdict(record)
        row.update(
            {
                "covered": bool(matches),
                "contract_mechanisms": ";".join(
                    sorted({contract.mechanism for contract in matches})
                ),
                "contract_evidence": ";".join(
                    sorted(
                        {
                            f"{contract.source_file}:{contract.source_line}"
                            for contract in matches
                        }
                    )
                ),
            }
        )
        coverage_rows.append(row)

    for module_row in module_rows:
        rows = [
            row for row in coverage_rows if row["module"] == module_row["module"]
        ]
        by_display: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            by_display.setdefault(row["display_path"], []).append(row)
        module_row.update(
            {
                "covered_declarations": sum(row["covered"] for row in rows),
                "uncovered_declarations": sum(not row["covered"] for row in rows),
                "covered_unique_api_paths": sum(
                    any(row["covered"] for row in group)
                    for group in by_display.values()
                ),
                "uncovered_unique_api_paths": sum(
                    not any(row["covered"] for row in group)
                    for group in by_display.values()
                ),
                "covered_stable_unique_api_paths": sum(
                    any(row["covered"] for row in group)
                    for group in by_display.values()
                    if any(row["stability"] == "stable" for row in group)
                ),
                "uncovered_stable_unique_api_paths": sum(
                    not any(row["covered"] for row in group)
                    for group in by_display.values()
                    if any(row["stability"] == "stable" for row in group)
                ),
            }
        )
        unique_total = module_row["unique_api_paths"]
        module_row["unique_path_coverage_percent"] = (
            round(
                100.0
                * module_row["covered_unique_api_paths"]
                / unique_total,
                2,
            )
            if unique_total
            else 0.0
        )
        stable_total = module_row["stable_unique_api_paths"]
        module_row["stable_unique_path_coverage_percent"] = (
            round(
                100.0
                * module_row["covered_stable_unique_api_paths"]
                / stable_total,
                2,
            )
            if stable_total
            else 0.0
        )

    production_module_set = set(production_modules)

    def scope_summary(include_all: bool) -> dict[str, Any]:
        rows = [
            row
            for row in coverage_rows
            if include_all or row["module"] in production_module_set
        ]
        canonical_groups: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            canonical_groups.setdefault(row["canonical_path"], []).append(row)
        covered_canonical = sum(
            any(row["covered"] for row in group)
            for group in canonical_groups.values()
        )
        stable_groups = {
            path: group
            for path, group in canonical_groups.items()
            if any(row["stability"] == "stable" for row in group)
        }
        covered_stable = sum(
            any(row["covered"] for row in group)
            for group in stable_groups.values()
        )
        return {
            "modules": len(
                {row["module"] for row in rows}
            ),
            "module_api_declarations": len(rows),
            "module_unique_display_paths": len(
                {row["display_path"] for row in rows}
            ),
            "deduplicated_declarations": len(
                {(row["canonical_path"], row["declaration_id"]) for row in rows}
            ),
            "deduplicated_api_paths": len(canonical_groups),
            "covered_deduplicated_api_paths": covered_canonical,
            "uncovered_deduplicated_api_paths": len(canonical_groups)
            - covered_canonical,
            "deduplicated_path_coverage_percent": (
                round(100.0 * covered_canonical / len(canonical_groups), 2)
                if canonical_groups
                else 0.0
            ),
            "stable_deduplicated_api_paths": len(stable_groups),
            "covered_stable_deduplicated_api_paths": covered_stable,
            "uncovered_stable_deduplicated_api_paths": len(stable_groups)
            - covered_stable,
            "stable_deduplicated_path_coverage_percent": (
                round(100.0 * covered_stable / len(stable_groups), 2)
                if stable_groups
                else 0.0
            ),
        }

    def uncovered_rows(
        include_all: bool,
        stable_only: bool = False,
    ) -> list[dict[str, Any]]:
        rows = [
            row
            for row in coverage_rows
            if include_all or row["module"] in production_module_set
        ]
        groups: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            groups.setdefault(row["canonical_path"], []).append(row)
        output = []
        for canonical_path, group in sorted(groups.items()):
            if any(row["covered"] for row in group):
                continue
            if stable_only and not any(
                row["stability"] == "stable" for row in group
            ):
                continue
            output.append(
                {
                    "canonical_path": canonical_path,
                    "representative_display_path": sorted(
                        {row["display_path"] for row in group}
                    )[0],
                    "modules": ";".join(sorted({row["module"] for row in group})),
                    "kinds": ";".join(sorted({row["kind"] for row in group})),
                    "stability": ";".join(
                        sorted({row["stability"] for row in group})
                    ),
                    "declaration_count": len(
                        {row["declaration_id"] for row in group}
                    ),
                    "source_locations": ";".join(
                        sorted(
                            {
                                f"{row['source_file']}:{row['source_line']}"
                                for row in group
                                if row["source_file"]
                            }
                        )
                    ),
                    "has_approximate_alias": any(
                        row["alias_approximate"] for row in group
                    ),
                }
            )
        return output

    summary = {
        "production": scope_summary(False),
        "all_tracked_sources": scope_summary(True),
        "vstd": {
            key: value
            for key, value in vstd_metadata.items()
            if key != "macro_expansion_errors"
        },
    }

    args.out_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        "nanvix": git_metadata(args.nanvix_root),
        "rust": git_metadata(args.rust_root),
        "verus": git_metadata(args.verus_root),
        "rust_toolchain": args.rust_toolchain,
        "scope": {
            "tracked_rust_files": usage_metadata["rust_files"],
            "production_modules": len(production_modules),
            "all_modules": len(all_modules),
            "production_exec_declarations": sum(
                row["exec_declarations"]
                for row in module_rows
                if row["used_in_production"]
            ),
            "all_exec_declarations": sum(
                row["exec_declarations"] for row in module_rows
            ),
        },
        "usage_parser": {
            key: value
            for key, value in usage_metadata.items()
            if key != "unresolved"
        },
        "vstd_parser": vstd_metadata,
    }
    (args.out_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    )
    (args.out_dir / "unresolved_usage.json").write_text(
        json.dumps(usage_metadata["unresolved"], indent=2, sort_keys=True) + "\n"
    )
    (args.out_dir / "usage_evidence.json").write_text(
        json.dumps([asdict(row) for row in evidence], indent=2, sort_keys=True)
        + "\n"
    )
    (args.out_dir / "rust_exec_apis.json").write_text(
        json.dumps([asdict(row) for row in api_rows], indent=2, sort_keys=True)
        + "\n"
    )
    (args.out_dir / "vstd_contracts.json").write_text(
        json.dumps([asdict(row) for row in contracts], indent=2, sort_keys=True)
        + "\n"
    )
    (args.out_dir / "coverage.json").write_text(
        json.dumps(coverage_rows, indent=2, sort_keys=True) + "\n"
    )
    (args.out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )

    write_csv(
        args.out_dir / "modules.csv",
        module_rows,
        list(module_rows[0]) if module_rows else ["module"],
    )
    complete_module_rows = [
        {
            "module": row["module"],
            "scope": (
                "production"
                if row["used_in_production"]
                else "test/benchmark only"
            ),
            "source_files": row["source_file_count"],
            "exec_apis": row["unique_api_paths"],
            "stable_apis": row["stable_unique_api_paths"],
            "vstd_covered": row["covered_unique_api_paths"],
            "vstd_uncovered_stable": row[
                "uncovered_stable_unique_api_paths"
            ],
        }
        for row in sorted(module_rows, key=lambda item: item["module"])
    ]
    write_csv(
        args.out_dir / "complete_modules.csv",
        complete_module_rows,
        list(complete_module_rows[0])
        if complete_module_rows
        else ["module"],
    )
    write_csv(
        args.out_dir / "usage_evidence.csv",
        [asdict(row) for row in evidence],
        list(asdict(evidence[0])) if evidence else ["module"],
    )
    write_csv(
        args.out_dir / "rust_exec_apis.csv",
        [asdict(row) for row in api_rows],
        list(asdict(api_rows[0])) if api_rows else ["module"],
    )
    write_csv(
        args.out_dir / "vstd_contracts.csv",
        [asdict(row) for row in contracts],
        list(asdict(contracts[0])) if contracts else ["api_path"],
    )
    write_csv(
        args.out_dir / "coverage.csv",
        coverage_rows,
        list(coverage_rows[0]) if coverage_rows else ["module"],
    )
    production_uncovered = uncovered_rows(False)
    production_stable_uncovered = uncovered_rows(False, stable_only=True)
    all_uncovered = uncovered_rows(True)
    write_csv(
        args.out_dir / "uncovered_production_apis.csv",
        production_uncovered,
        list(production_uncovered[0])
        if production_uncovered
        else ["canonical_path"],
    )
    write_csv(
        args.out_dir / "uncovered_production_stable_apis.csv",
        production_stable_uncovered,
        list(production_stable_uncovered[0])
        if production_stable_uncovered
        else ["canonical_path"],
    )
    write_csv(
        args.out_dir / "uncovered_all_apis.csv",
        all_uncovered,
        list(all_uncovered[0]) if all_uncovered else ["canonical_path"],
    )
    write_report(
        Path(__file__).resolve().parent / "README.md",
        metadata,
        summary,
        module_rows,
    )
    write_main_results(
        Path(__file__).resolve().parent / "MAIN-RESULTS.md",
        metadata,
        summary,
        module_rows,
    )
    print(
        f"wrote {len(all_modules)} modules, {len(api_rows)} exec declarations, "
        f"{len(contracts)} vstd contract records, and {len(evidence)} usage "
        f"evidence rows to {args.out_dir}"
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument("--nanvix-root", type=Path, default=workspace / "nanvix")
    parser.add_argument("--rust-root", type=Path, default=workspace / "rust")
    parser.add_argument("--verus-root", type=Path, default=workspace / "verus")
    parser.add_argument(
        "--rustdoc-dir", type=Path, default=workspace / "rustdoc-json"
    )
    parser.add_argument(
        "--vstd-root", type=Path, default=workspace / "verus" / "source" / "vstd"
    )
    parser.add_argument("--out-dir", type=Path, default=workspace / "results")
    parser.add_argument("--rust-toolchain", default="nightly-2026-07-09")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
