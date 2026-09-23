#!/usr/bin/env python3
"""Source-owned slice inventory for the supplied Rust tree; Python stdlib only.

This is a declaration reader, not a Rust type checker. It keeps exact source
signatures, attribute gates and macro provenance. Calls which require Rust type
resolution are explicitly labelled, never guessed to be resolved dependencies.
"""

from __future__ import annotations

import argparse
import bisect
from collections import Counter, defaultdict
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import re


DEFAULT_CORE = Path(
    "/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src"
)
ROOT = Path(__file__).resolve().parents[1]
PENDING = "awaiting-selected-baseline"
SELECTED_VSTD = ROOT / "toolchain/upstream/source/vstd"
VSTD_RELEASE = "0.2026.09.20.aef82ed"
VSTD_COMMIT = "aef82eda71838deef4a8cd0260fda6c9504be9b9"
VSTD_TREE_SHA256 = "742b8567a2c9b143b7d0a40ce13c59823a712a583871b7b59c0be1d5a4891922"
VSTD_API_IDS_SHA256 = "8ed95acbf2bb938cbf4f8a9ff30d5979609f96d53173a92e3f1f4c6a7e42897d"


def compact(text):
    return re.sub(r"\s+", " ", text).strip()


def encode(text):
    return str(text).replace("\\", "\\\\").replace("\t", "\\t").replace(
        "\r", "\\r"
    ).replace("\n", "\\n")


def decode(text):
    return re.sub(r"\\([\\trn])", lambda m: {
        "\\": "\\", "t": "\t", "r": "\r", "n": "\n"
    }[m[1]], text)


def write_tsv(path, rows, columns):
    text = "\t".join(columns) + "\n"
    text += "".join(
        "\t".join(encode(row.get(key, "")) for key in columns) + "\n"
        for row in rows
    )
    path.write_text(text, encoding="utf-8")


def read_tsv(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    columns = lines[0].split("\t")
    return [dict(zip(columns, map(decode, line.split("\t")))) for line in lines[1:]]


def json_text(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def lexical_mask(text):
    """Blank comments/literals without changing offsets, retaining doc spans."""
    chars = list(text)
    docs = []
    pos = 0
    while pos < len(text):
        end = pos
        doc = False
        if text.startswith("//", pos):
            end = text.find("\n", pos)
            if end == -1:
                end = len(text)
            doc = text.startswith("///", pos) and not text.startswith("////", pos)
        elif text.startswith("/*", pos):
            depth, end = 1, pos + 2
            doc = text.startswith("/**", pos) and not text.startswith("/***", pos)
            while depth:
                if end >= len(text):
                    raise ValueError("Unterminated block comment")
                if text.startswith("/*", end):
                    depth += 1
                    end += 2
                elif text.startswith("*/", end):
                    depth -= 1
                    end += 2
                else:
                    end += 1
        else:
            raw = re.match(r'(?:br|cr|r)(#{0,255})"', text[pos:])
            if raw and (pos == 0 or not (text[pos - 1].isalnum() or text[pos - 1] == "_")):
                close = '"' + raw[1]
                at = text.find(close, pos + raw.end())
                if at < 0:
                    raise ValueError("Unterminated raw string")
                end = at + len(close)
            elif text[pos] == '"':
                end = pos + 1
                while end < len(text):
                    if text[end] == "\\":
                        end += 2
                    elif text[end] == '"':
                        end += 1
                        break
                    else:
                        end += 1
            elif text[pos] == "'":
                char = re.match(r"'(?:\\(?:u\{[0-9A-Fa-f_]+\}|x[0-9A-Fa-f]{2}|.)|[^'\\\n])'", text[pos:])
                if char:
                    end = pos + char.end()
        if end > pos:
            if doc:
                docs.append((pos, end))
            for i in range(pos, end):
                if chars[i] not in "\r\n":
                    chars[i] = " "
            pos = end
        else:
            pos += 1
    return "".join(chars), docs


@dataclass(eq=False)
class Source:
    path: str
    text: str
    mapping: list | None = None
    invocation: "Node | None" = None
    macro_name: str = ""
    mask: str = field(init=False)
    docs: list = field(init=False)
    pairs: dict = field(init=False)
    lines: list = field(init=False)

    def __post_init__(self):
        self.mask, self.docs = lexical_mask(self.text)
        self.lines = [0] + [m.end() for m in re.finditer("\n", self.text)]
        self.pairs = {}
        stack = []
        for i, char in enumerate(self.mask):
            if char in "([{":
                stack.append((char, i))
            elif char in ")]}":
                if not stack or stack[-1][0] != {")": "(", "]": "[", "}": "{"}[char]:
                    raise ValueError(f"{self.path}: unbalanced delimiter at {i}")
                _, start = stack.pop()
                self.pairs[start] = i
                self.pairs[i] = start
        if stack:
            raise ValueError(f"{self.path}: unclosed delimiter")

    def origin(self, offset):
        if self.mapping is None:
            return self, offset
        source, position = self.mapping[min(offset, len(self.mapping) - 1)]
        return source.origin(position)

    def span(self, start, end):
        source, first = self.origin(start)
        last_source, last = self.origin(max(start, end - 1))
        if last_source is not source:
            return source.span(first, first + 1) + ";" + last_source.span(last, last + 1)
        return f"{source.path}:{bisect.bisect_right(source.lines, first)}-{bisect.bisect_right(source.lines, last)}"

    def original(self, start, end):
        source, first = self.origin(start)
        last_source, last = self.origin(max(start, end - 1))
        return source.text[first:last + 1] if source is last_source else ""


@dataclass(eq=False)
class Node:
    source: Source
    kind: str
    name: str
    start: int
    head_end: int
    end: int
    attrs: list
    docs: list
    parent: "Node | None" = None
    module: str = ""

    @property
    def header(self):
        return self.source.text[self.start:self.head_end].rstrip()

    @property
    def body(self):
        return self.source.text[self.head_end:self.end]

    @property
    def span(self):
        return self.source.span(self.start, self.end)

    @property
    def attributes(self):
        return [self.source.text[a:b] for a, b in self.attrs]

    @property
    def doc_spans(self):
        return [self.source.span(a, b) for a, b in self.docs]


ITEM = re.compile(
    r"(?m)^[ \t]*(?P<header>(?:(?:pub(?:\([^\n)]*\))?|unsafe|const|default|async|extern|safe|auto)[ \t]+)*"
    r"(?P<kind>fn|impl|trait|struct|enum|union|mod|use|macro_rules|macro)\b)"
)
INVOCATION = re.compile(r"(?m)^[ \t]*(?P<name>[A-Za-z_]\w*)!\s*(?P<open>[({[])")


def attributes_before(source, start):
    position = start
    attrs = []
    while True:
        previous = len(source.mask[:position].rstrip()) - 1
        if previous < 0 or source.mask[previous] != "]":
            break
        opening = source.pairs[previous]
        if opening == 0 or source.mask[opening - 1] != "#":
            break
        attrs.append((opening - 1, previous + 1))
        position = opening - 1
    boundary = len(source.mask[:position].rstrip())
    docs = [(a, b) for a, b in source.docs if boundary <= a and b <= start]
    docs.extend((a, b) for a, b in attrs if re.match(r"#\[\s*doc\b", source.text[a:b]))
    return sorted(attrs), sorted(docs)


def header_end(source, start, kind):
    pos = start
    while pos < len(source.mask):
        char = source.mask[pos]
        if char in "([":
            pos = source.pairs[pos] + 1
        elif char == "{":
            if kind == "use":
                pos = source.pairs[pos] + 1
            else:
                return pos, source.pairs[pos] + 1
        elif char == ";":
            return pos, pos + 1
        else:
            pos += 1
    raise ValueError(f"{source.path}: unterminated {kind} at {start}")


def parse(source):
    nodes, macros = [], []
    for match in ITEM.finditer(source.mask):
        start, kind = match.start("header"), match["kind"]
        if any(a <= start < b for a, b in macros):
            continue
        if kind == "fn":
            name_match = re.match(r"\s+([A-Za-z_]\w*)\s*(?:<|\()", source.mask[match.end():])
            if not name_match:
                continue
            name = name_match[1]
        elif kind in {"impl", "use"}:
            name = ""
        else:
            name_match = re.match(r"[!\s]*([A-Za-z_]\w*)", source.mask[match.end():])
            if not name_match:
                continue
            name = name_match[1]
        end_head, end = header_end(source, start, kind)
        attrs, docs = attributes_before(source, start)
        node = Node(source, kind, name, start, end_head, end, attrs, docs)
        nodes.append(node)
        if kind in {"macro_rules", "macro"}:
            macros.append((start, end))
    for match in INVOCATION.finditer(source.mask):
        start = match.start("name")
        if any(a <= start < b for a, b in macros):
            continue
        opening = match.start("open")
        attrs, docs = attributes_before(source, start)
        nodes.append(Node(source, "macro_call", match["name"], start, opening,
                          source.pairs[opening] + 1, attrs, docs))
    containers = [n for n in nodes if n.kind in {
        "impl", "trait", "mod", "fn", "macro_call", "struct", "enum", "union"
    } and source.mask[n.head_end] == "{"]
    for node in nodes:
        parents = [p for p in containers if p.head_end < node.start < p.end]
        node.parent = min(parents, key=lambda p: p.end - p.start, default=None)
        path = source.path.removesuffix(".rs").replace("/", "::")
        if path.endswith("::mod"):
            path = path[:-5]
        node.module = source.invocation.module if source.invocation else (
            "core" if path == "lib" else "core::" + path
        )
        parent = node.parent
        scopes = []
        while parent:
            if parent.kind == "mod":
                scopes.append(parent.name)
            parent = parent.parent
        if scopes:
            node.module += "::" + "::".join(reversed(scopes))
    return sorted(
        (n for n in nodes if not (
            nearest(n, {"macro_call"}) and not nearest(n, {"fn"})
        )), key=lambda n: n.start,
    )


def angle_end(text, start):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "<":
            depth += 1
        elif text[i] == ">" and (i == 0 or text[i - 1] != "-"):
            depth -= 1
            if depth == 0:
                return i + 1
    raise ValueError(f"Unbalanced generic parameters: {text[start:]}")


def split_top(text, delimiter=","):
    parts, start, pos = [], 0, 0
    mask, _ = lexical_mask(text)
    while pos < len(mask):
        if mask[pos] == "<":
            pos = angle_end(mask, pos)
        elif mask[pos] in "([{":
            opening, closing = mask[pos], {"(": ")", "[": "]", "{": "}"}[mask[pos]]
            depth = 1
            pos += 1
            while depth and pos < len(mask):
                depth += (mask[pos] == opening) - (mask[pos] == closing)
                pos += 1
        elif mask.startswith(delimiter, pos):
            parts.append(text[start:pos].strip())
            pos += len(delimiter)
            start = pos
        else:
            pos += 1
    parts.append(text[start:].strip())
    return parts


def impl_parts(node):
    text = compact(re.sub(r"^.*?\bimpl\s*", "", node.header, count=1))
    generics = ""
    if text.startswith("<"):
        end = angle_end(text, 0)
        generics, text = text[:end], text[end:].strip()
    where = split_top(text, " where")
    text, bounds = where[0], " where".join(where[1:])
    const = text.startswith("const ")
    text = text.removeprefix("const ")
    pieces = split_top(text, " for ")
    if len(pieces) == 2:
        trait, self_type = pieces
    else:
        trait, self_type = "", text
    return generics, trait, self_type, bounds, const


def stability(node, const=False):
    if not node:
        return ""
    pattern = r"#\[\s*rustc_const_(stable|unstable)\b" if const else r"#\[\s*(stable|unstable)\b"
    for attr in node.attributes:
        match = re.match(pattern, attr)
        if match:
            return match[1] + ":" + compact(attr)
    return ""


def visibility(node):
    match = re.match(r"pub(?:\([^)]*\))?", node.header)
    return match[0] if match else "private"


def children(nodes, parent, kind="fn"):
    return [n for n in nodes if n.parent is parent and n.kind == kind]


def nearest(node, kinds):
    parent = node.parent
    while parent and parent.kind not in kinds:
        parent = parent.parent
    return parent


def expansion_source(template, start, end, replacements, invocation, macro_name):
    text = template.text[start:end]
    mapping = [(template, i) for i in range(start, end)]
    patterns = [
        r"\$\(\s*\$mut_\s*\)\?", r"\$\(\s*\$extra\s*\)\*",
        r"\$\(\s*\$p\s*\)\*", r"\$\(\s*#\[\$attr\]\s*\)\*",
        r"\$\(\s*<\$\(\s*\$lifetime\s*\),\+>\s*\)\?",
        r"\$\(\s*\$ArgTy,\s*\)\*", r"\$\(\s*\$arg,\s*\)\*",
    ]
    patterns.extend(re.escape("$" + key) + r"\b" for key in replacements)
    regex = re.compile("|".join(patterns))
    chunks, origins, previous = [], [], 0
    for match in regex.finditer(text):
        chunks.append(text[previous:match.start()])
        origins.extend(mapping[previous:match.start()])
        key = re.search(r"\$(\w+)", match[0])[1]
        replacement, replacement_source, replacement_offset = replacements[key]
        chunks.append(replacement)
        if replacement_source:
            origins.extend((replacement_source, replacement_offset + i) for i in range(len(replacement)))
        else:
            origins.extend([mapping[match.start()]] * len(replacement))
        previous = match.end()
    chunks.append(text[previous:])
    origins.extend(mapping[previous:])
    return Source(template.path, "".join(chunks), origins, invocation, macro_name)


def expand_macros(nodes):
    definitions = {n.name: n for n in nodes if n.kind in {"macro_rules", "macro"}}
    expanded, records = [], []
    for call in [n for n in nodes if n.kind == "macro_call" and n.parent is None]:
        name = call.name
        if name not in {"iterator", "forward_iterator", "impl_slice_contains", "spec_fill_int",
                        "always_applicable_ord", "impl_fn_for_zst"}:
            raise ValueError(f"Unreviewed item macro: {call.span}: {name}")
        definition = definitions[name]
        source = definition.source
        arrow = source.mask.find("=>", definition.head_end, definition.end)
        opening = source.mask.find("{", arrow, definition.end)
        start, end = opening + 1, source.pairs[opening]
        args = call.source.text[call.head_end + 1:call.end - 1].strip()
        replacement_sets = []
        if name == "iterator":
            parts = split_top(args)
            match = re.fullmatch(r"struct\s+(\w+)\s*->\s*(.*)", parts[0])
            if not match or len(parts) != 7:
                raise ValueError(f"Unexpected iterator! shape: {call.span}")
            extra_start = call.source.text.find(parts[6], call.head_end, call.end) + 1
            replacement_sets = [{
                "name": (match[1], None, 0), "ptr": (match[2], None, 0),
                "elem": (parts[1], None, 0), "raw_mut": (parts[2], None, 0),
                "mut_": ("mut" if re.search(r"\bmut\b", lexical_mask(parts[3])[0]) else "", None, 0),
                "into_ref": (parts[4], None, 0), "array_ref": (parts[5], None, 0),
                "extra": (parts[6][1:-1], call.source, extra_start),
            }]
        elif name == "forward_iterator":
            first, item = split_top(args)
            iterator, element = first.split(":")
            replacement_sets = [{"name": (iterator.strip(), None, 0),
                                 "elem": (element.strip(), None, 0),
                                 "iter_of": (item, None, 0)}]
        elif name == "impl_fn_for_zst":
            repeat = source.mask.find("$(", start, end)
            start, end = repeat + 2, source.pairs[repeat + 1]
            match = re.fullmatch(
                r"\s*(?P<attrs>(?:#\[[^\]]+\]\s*)*)struct\s+(?P<name>\w+)\s+impl\s+Fn\s*=\s*"
                r"\|(?P<arg>\w+)\s*:\s*(?P<argty>[^|]+)\|\s*->\s*(?P<ret>[^{]+)"
                r"(?P<body>\{.*\})\s*;\s*", args, flags=re.S,
            )
            if not match:
                raise ValueError(f"Unexpected impl_fn_for_zst! shape: {call.span}")
            args_start = call.source.text.find(args, call.head_end, call.end)
            replacement_sets = [{
                "Name": (match["name"], None, 0),
                "attr": (match["attrs"], call.source, args_start + match.start("attrs")),
                "lifetime": ("", None, 0), "arg": (match["arg"] + ",", None, 0),
                "ArgTy": (match["argty"].strip() + ",", None, 0),
                "ReturnTy": (match["ret"].strip(), None, 0),
                "body": (match["body"], call.source, args_start + match.start("body")),
            }]
        elif name == "always_applicable_ord":
            repeat = source.mask.find("$(", start, end)
            start, end = repeat + 2, source.pairs[repeat + 1]
            for arg in split_top(args):
                if not arg:
                    continue
                match = re.fullmatch(r"\[([^]]*)\]\s*(.+)", arg, re.S)
                if not match:
                    raise ValueError(f"Unexpected marker macro argument: {arg}")
                replacement_sets.append({"p": (match[1], None, 0), "t": (match[2], None, 0)})
        else:
            repeat = source.mask.find("$(", start, end)
            opening = repeat + 1
            start, end = opening + 1, source.pairs[opening]
            key = "t" if name == "impl_slice_contains" else "type"
            types = split_top(args) if name == "impl_slice_contains" else args.split()
            replacement_sets = [{key: (typ, None, 0)} for typ in types]
        count = 0
        for replacements in replacement_sets:
            unit = expansion_source(source, start, end, replacements, call, name)
            generated = parse(unit)
            if re.search(r"\$(?:\w+|\()", unit.mask):
                raise ValueError(f"Unexpanded metavariable: {call.span}")
            expanded.extend(generated)
            count += sum(n.kind == "fn" for n in generated)
        records.append({"macro": name, "invocation_span": call.span,
                        "definition_span": definition.span, "policy": "token-substitution",
                        "generated_functions": str(count),
                        "invocation": call.source.text[call.start:call.end]})
    return expanded, records


TRAIT_FILES = {
    "Iterator": "iter/traits/iterator.rs",
    "IntoIterator": "iter/traits/collect.rs",
    "DoubleEndedIterator": "iter/traits/double_ended.rs",
    "ExactSizeIterator": "iter/traits/exact_size.rs",
    "FusedIterator": "iter/traits/marker.rs",
    "TrustedLen": "iter/traits/marker.rs",
    "TrustedRandomAccess": "iter/adapters/zip.rs",
    "TrustedRandomAccessNoCoerce": "iter/adapters/zip.rs",
    "UncheckedIterator": "iter/traits/unchecked_iterator.rs",
    "Clone": "clone.rs", "TrivialClone": "clone.rs",
    "Debug": "fmt/mod.rs", "Display": "fmt/mod.rs",
    "PartialEq": "cmp.rs", "Eq": "cmp.rs", "Ord": "cmp.rs", "PartialOrd": "cmp.rs",
    "Index": "ops/index.rs", "IndexMut": "ops/index.rs",
    "Default": "default.rs", "Drop": "ops/drop.rs",
    "AsRef": "convert/mod.rs", "AsMut": "convert/mod.rs", "From": "convert/mod.rs",
    "Into": "convert/mod.rs", "TryFrom": "convert/mod.rs", "TryInto": "convert/mod.rs",
    "Borrow": "borrow.rs", "BorrowMut": "borrow.rs", "Any": "any.rs",
    "Send": "marker.rs", "Sync": "marker.rs", "Copy": "marker.rs",
    "Hash": "hash/mod.rs", "Error": "error.rs",
    "RangeBounds": "ops/range.rs", "OneSidedRange": "ops/range.rs",
    "IntoBounds": "ops/range.rs",
    "Fn": "ops/function.rs", "FnMut": "ops/function.rs", "FnOnce": "ops/function.rs",
}


def base_name(type_text):
    text = type_text.strip().removeprefix("!")
    return text.split("<", 1)[0].split("::")[-1].strip()


def flatten_use(text):
    text = re.sub(r"^(?:pub(?:\([^)]*\))?\s+)?use\s+", "", text).rstrip(";").strip()
    if "{" not in text:
        return [text]
    before, group = text.split("{", 1)
    return [before + part.strip() for part in split_top(group.rsplit("}", 1)[0])]


def public_exports(nodes):
    exports = defaultdict(list)
    for node in nodes:
        if node.source.path == "slice/mod.rs" and node.kind == "use" and visibility(node) == "pub":
            for binding in flatten_use(node.header):
                if " as " in binding:
                    source_binding, alias = binding.split(" as ")
                else:
                    source_binding, alias = binding, binding.split("::")[-1]
                exports[source_binding].append(("core::slice::" + alias, node))
    return exports


def type_parameters(node):
    after = node.header.split(node.name, 1)[1].lstrip()
    if not after.startswith("<"):
        return ""
    return after[:angle_end(after, 0)]


def type_application(node):
    generic = type_parameters(node)
    if not generic:
        return node.name
    args = [re.sub(r"^const\s+", "", p).split(":", 1)[0].strip()
            for p in split_top(generic[1:-1])]
    return node.name + "<" + ", ".join(args) + ">"


def qualified_type(text, node, local_types):
    text = re.sub(r"\bcrate::", "core::", text)
    text = re.sub(r"(?<![\w:])ops::", "core::ops::", text)
    text = re.sub(r"(?<![\w:])range::", "core::range::", text)
    text = re.sub(r"(?<![\w:])MaybeUninit\b", "core::mem::MaybeUninit", text)
    if node.source.path == "slice/mod.rs":
        text = re.sub(r"(?<![\w:])(RangeInclusive|Range)\b", r"core::ops::\1", text)
    if node.source.path == "range.rs":
        text = re.sub(r"(?<![\w:])(RangeToInclusive|RangeInclusive|RangeFrom|Range)\b", r"core::range::\1", text)
    local_types = dict(local_types)
    if node.kind in {"struct", "enum", "union", "trait"} and visibility(node) != "pub":
        local_types[node.name] = node.module + "::" + node.name
    for name, owner in sorted(local_types.items(), key=lambda p: -len(p[0])):
        if name in {"Range", "RangeInclusive", "RangeToInclusive", "RangeFrom"}:
            continue
        text = re.sub(r"(?<![\w:])" + re.escape(name) + r"\b", owner, text)
    return compact(text)


def trait_path(name):
    base = base_name(name)
    if base not in TRAIT_FILES:
        return name
    path = TRAIT_FILES[base]
    module = "iter" if path.startswith("iter/") else path.split("/")[0].removesuffix(".rs")
    prefix = name.split("<", 1)[0]
    return name.replace(prefix, f"core::{module}::{base}", 1)


API_COLUMNS = [
    "canonical_id", "owner", "kind", "name", "self_type", "trait", "impl_header",
    "type_header", "trait_header", "trait_signature", "derived_bounds",
    "signature", "receiver", "source_span", "signature_span", "doc_spans",
    "impl_span", "impl_doc_spans", "type_span", "trait_item_span", "signature_origin",
    "source_signature", "macro_invocation", "aliases", "reexport_spans",
    "item_stability", "impl_stability", "type_stability", "trait_stability",
    "effective_stability", "stable_since", "const_stability", "stability_evidence",
    "attributes", "attribute_evidence", "unsafe_function", "unsafe_impl", "cfg",
    "delegated_calls", "scope_reason", "existing_vstd_coverage",
]


class Inventory:
    def __init__(self, core, vstd=SELECTED_VSTD):
        self.core = Path(core)
        self.vstd_path = Path(vstd)
        self.sources, self.nodes = {}, []
        for file in sorted((self.core / "slice").rglob("*.rs")):
            self.load(file.relative_to(self.core).as_posix())
        self.slice_nodes = list(self.nodes)
        for path in sorted(set(TRAIT_FILES.values()) | {
            "mem/maybe_uninit.rs", "range.rs", "range/iter.rs", "range/legacy.rs",
            "ptr/metadata.rs", "ptr/mod.rs", "ptr/const_ptr.rs", "ptr/mut_ptr.rs",
            "ptr/non_null.rs", "array/mod.rs", "internal_macros.rs",
            "ops/index_range.rs", "intrinsics/mod.rs", "ub_checks.rs", "lib.rs", "index.rs",
        }):
            self.load(path)
        self.exports = public_exports(self.slice_nodes)
        generated, self.macros = expand_macros(self.slice_nodes + [
            n for n in self.nodes if n.source.path == "internal_macros.rs" and n.kind == "macro_rules"
        ])
        self.nodes.extend(generated)
        self.owned_nodes = self.slice_nodes + generated + [
            n for n in self.nodes if n.source.path == "mem/maybe_uninit.rs"
            and ((n.kind == "impl" and impl_parts(n)[2] == "[MaybeUninit<T>]")
                 or (nearest(n, {"impl"}) is not None
                     and impl_parts(nearest(n, {"impl"}))[2] == "[MaybeUninit<T>]"))
        ]
        self.types = {}
        for node in self.owned_nodes:
            if node.kind in {"struct", "enum", "union", "trait"}:
                self.types[(node.module, node.name)] = node
        self.local_types = {}
        for node in self.owned_nodes:
            if node.kind in {"struct", "enum", "union", "trait"}:
                exports = self.exported(node)
                self.local_types[node.name] = exports[0][0] if exports else node.module + "::" + node.name
        self.traits = {}
        for node in self.nodes:
            if node.kind == "trait" and (node.name not in self.traits or node in self.owned_nodes):
                self.traits[node.name] = node
        self.apis, self.exclusions, self.ownership, self.defaults = [], [], [], []
        self.all_rows, self.node_rows, self.dependencies = [], [], []

    def load(self, path):
        if path not in self.sources:
            source = Source(path, (self.core / path).read_text(encoding="utf-8"))
            self.sources[path] = source
            self.nodes.extend(parse(source))

    def exported(self, node):
        if visibility(node) != "pub":
            return []
        if node.module == "core::slice":
            return [(node.module + "::" + node.name, node)]
        if node.module in {"core::range", "core::index"}:
            return [(node.module + "::" + node.name, node)]
        if node.module == "core::range::iter" and node.kind == "struct":
            exports = [n for n in self.nodes if n.kind == "use" and n.module == "core::range"
                       and visibility(n) == "pub" and "iter::" + node.name in flatten_use(n.header)]
            return [("core::range::" + node.name, export) for export in exports]
        binding = node.module.removeprefix("core::slice::") + "::" + node.name
        if binding in self.exports:
            return self.exports[binding]
        path = "core::slice"
        for component in node.module.removeprefix("core::slice::").split("::"):
            declaration = next((n for n in self.slice_nodes if n.kind == "mod"
                                and n.module == path and n.name == component), None)
            if not declaration or visibility(declaration) != "pub":
                return []
            path += "::" + component
        return [(node.module + "::" + node.name, node)]

    def find_trait(self, trait, node):
        name = base_name(trait)
        local = next((n for n in self.nodes if n.kind == "trait"
                      and n.name == name and n.module == node.module), None)
        return local or self.traits.get(name)

    def module_declarations(self, node):
        return [n for n in self.nodes if n.kind == "mod"
                and (node.module == n.module + "::" + n.name
                     or node.module.startswith(n.module + "::" + n.name + "::"))]

    def type_node(self, self_type, node):
        name = base_name(self_type)
        same = self.types.get((node.module, name))
        if same:
            return same
        candidates = [t for (_, n), t in self.types.items() if n == name and self.exported(t)]
        return candidates[0] if len(candidates) == 1 else None

    def row(self, node, derive=None):
        impl = nearest(node, {"impl"})
        trait_container = nearest(node, {"trait"})
        local = nearest(node, {"fn"})
        generics, trait, self_type, bounds, const_impl = impl_parts(impl) if impl else ("", "", "", "", False)
        type_node = self.type_node(self_type, node) if impl else None
        trait_node = self.find_trait(trait, node) if trait else trait_container
        trait_method = next((n for n in self.nodes if n.parent is trait_node and n.kind == "fn"
                             and n.name == node.name), None)
        if derive:
            type_node, trait_node = derive
            trait = trait_node.name
            self_type = type_application(type_node)
            trait_method = node
        qself = qualified_type(self_type, type_node or node, self.local_types)
        trait_identity = trait_path(trait)
        if trait and trait_node and base_name(trait) not in TRAIT_FILES:
            exports = self.exported(trait_node)
            trait_identity = (exports[0][0] if exports else trait_node.module + "::" + trait_node.name)
            trait_identity += trait[len(trait.split("<", 1)[0]):]
        qtrait = qualified_type(trait_identity, node, self.local_types)
        if trait_container and not impl and not derive:
            canonical = self.local_types.get(trait_container.name, trait_container.module + "::" + trait_container.name) + "::" + node.name
        elif trait:
            canonical = f"<{qself} as {qtrait}>::{node.name}"
        elif impl:
            canonical = f"<{qself}>::{node.name}"
        else:
            export = self.exported(node)
            canonical = (export[0][0] if export else node.module + "::" + node.name)
        if local:
            canonical += f"@local:{node.span}"
        owning = type_node if derive else node
        item_gate = "" if derive else stability(node)
        impl_gate = stability(type_node if derive else impl)
        type_gate = stability(type_node)
        trait_gate = stability(trait_node)
        method_gate = stability(trait_method)
        modules = self.module_declarations(node)
        ancestor_gates = [stability(module) for module in modules]
        for _, export_node in self.exported(type_node or node):
            ancestor_gates.append(stability(export_node))
        gates = [item_gate, impl_gate, type_gate, trait_gate, method_gate] + ancestor_gates
        unstable = [g for g in gates if g.startswith("unstable:")]
        effective = "unstable" if unstable else ("stable" if any(g.startswith("stable:") for g in gates) else "unannotated")
        runtime_gate = next((g for g in gates if g), "")
        if unstable:
            runtime_gate = unstable[0]
        self_private = bool(type_node and not self.exported(type_node))
        trait_private = bool(trait_node and visibility(trait_node) != "pub")
        if trait_node and trait_node.source.path.startswith("slice/") and not self.exported(trait_node):
            trait_private = True
        if self_type == "ops::IndexRange":
            self_private = True
        if local:
            reason = "local-helper: not a public binding"
        elif trait_container and not derive:
            reason = "trait-declaration: no independent implementation identity"
        elif self_private:
            reason = "private-self-type: no public name or return-type reachability"
        elif trait_private:
            reason = "private-trait: implementation dependency, not public API"
        elif impl and not trait and visibility(node) != "pub":
            reason = "non-public-inherent-method: implementation dependency"
        elif not impl and not derive and not self.exported(node):
            if visibility(node) == "pub":
                reason = "public-in-private-module: no stable public reexport"
            else:
                reason = "non-public-free-function: implementation dependency"
        elif effective == "unstable":
            reason = "unstable-gate: " + runtime_gate
        elif effective != "stable":
            reason = "no-stable-public-gate"
        else:
            reason = "stable-public-source-owned"
        if derive and not self_private and effective == "stable":
            reason = "stable-public-source-owned"
        const_syntax = bool(re.search(r"\bconst\s+(?:unsafe\s+)?fn\b", node.header)) or const_impl
        const_gates = [stability(node, True), stability(impl, True),
                       stability(trait_method, True), stability(trait_node, True)]
        const_gate = next((g for g in const_gates if g), "")
        const_status = const_gate if const_syntax else "not-const"
        if const_syntax and not const_gate:
            const_status = "unstable-implicit" if effective == "unstable" else "unannotated-const"
        match = re.search(r"\bfn\s+\w+", node.source.mask[node.start:node.head_end])
        after_name = node.start + match.end()
        if node.source.mask[after_name:after_name + 1] == "<":
            after_name = angle_end(node.source.mask, after_name)
        opening = node.source.mask.find("(", after_name, node.head_end)
        parameters = node.source.text[opening + 1:node.source.pairs[opening]] if opening >= 0 else ""
        first_param = split_top(parameters)[0]
        receiver = first_param if re.search(r"\bself\b", first_param) else "(associated; no self)"
        calls = call_sites(node) if not derive and node.source.mask[node.head_end] == "{" else []
        row = {
            "canonical_id": canonical, "owner": owning.module,
            "kind": "derived-method" if derive else (
                "trait-declaration" if trait_container else (
                    "trait-method" if trait else ("inherent-method" if impl else "free-function")
                )
            ),
            "name": node.name, "self_type": qself, "trait": qtrait,
            "impl_header": (json_text(type_node.attributes) + "\n" + type_node.header) if derive else (impl.header if impl else (trait_container.header if trait_container else "")),
            "type_header": type_node.header if type_node else "",
            "trait_header": trait_node.header if trait_node else "",
            "trait_signature": trait_method.header if trait_method else "",
            "derived_bounds": json_text([
                re.sub(r"^const\s+", "", parameter).split(":", 1)[0].strip()
                + ": " + trait_path(trait)
                for parameter in split_top(type_parameters(type_node)[1:-1])
                if parameter and not parameter.startswith(("'", "const "))
            ]) if derive else "",
            "signature": node.header, "receiver": receiver,
            "source_span": owning.span,
            "signature_span": node.source.span(node.start, node.head_end),
            "doc_spans": json_text(node.doc_spans or (trait_method.doc_spans if trait_method else [])),
            "impl_span": type_node.span if derive else (impl.span if impl else ""),
            "impl_doc_spans": json_text((type_node if derive else impl).doc_spans if (derive or impl) else []),
            "type_span": type_node.span if type_node else "",
            "trait_item_span": trait_method.span if trait_method else "",
            "signature_origin": "trait-declaration-for-derive" if derive else ("macro-token-substitution" if node.source.mapping else "source"),
            "source_signature": node.source.original(node.start, node.head_end).rstrip(),
            "macro_invocation": node.source.invocation.span if node.source.invocation else ("derive@" + type_node.span if derive else ""),
            "aliases": json_text([path for path, _ in self.exported(type_node or node)]),
            "reexport_spans": json_text([export.span for _, export in self.exported(type_node or node)]),
            "item_stability": item_gate, "impl_stability": impl_gate,
            "type_stability": type_gate, "trait_stability": method_gate or trait_gate,
            "effective_stability": effective,
            "stable_since": max(
                [match[1] for gate in gates if gate.startswith("stable:")
                 for match in re.finditer(r'\bsince\s*=\s*"([^"]+)"', gate)],
                key=lambda version: tuple(int(x) for x in version.split(".") if x.isdigit()),
                default="",
            ) if effective == "stable" else "",
            "const_stability": const_status,
            "stability_evidence": json_text([g for g in gates if g]),
            "attributes": json_text(node.attributes),
            "attribute_evidence": json_text([
                {"role": role, "source_span": item.span, "attributes": item.attributes}
                for role, item in [("method", node), ("impl", impl), ("type", type_node),
                                   ("trait", trait_node), ("trait-method", trait_method)]
                + [("module", module) for module in modules]
                if item
            ]),
            "unsafe_function": str(bool(re.search(r"\bunsafe\s+fn\b", node.header))).lower(),
            "unsafe_impl": str(bool(impl and impl.header.startswith("unsafe "))).lower(),
            "cfg": json_text([a for n in [node, impl, type_node] + modules if n for a in n.attributes
                             if re.match(r"#\[cfg(?:_attr)?\b", a)]),
            "delegated_calls": json_text(calls),
            "scope_reason": reason, "existing_vstd_coverage": PENDING,
        }
        return row

    def build(self):
        for node in self.owned_nodes:
            if node.kind == "fn":
                row = self.row(node)
                self.all_rows.append(row)
                self.node_rows.append((node, row))
            elif node.kind in {"impl", "trait", "struct", "enum", "union", "use", "mod"}:
                self.ownership.append(self.owner_row(node))
        for node in self.owned_nodes:
            if node.kind not in {"struct", "enum", "union"}:
                continue
            for attr in node.attributes:
                match = re.match(r"#\[\s*derive(?:_const)?\(([^)]*)\)\s*\]", attr)
                if not match:
                    continue
                for trait_name in split_top(match[1]):
                    trait = self.traits.get(trait_name)
                    if not trait:
                        raise ValueError(f"Unreviewed derive {trait_name}: {node.span}")
                    for method in children(self.nodes, trait):
                        if method.source.mask[method.head_end] == ";":
                            self.all_rows.append(self.row(method, (node, trait)))
        identities = Counter(r["canonical_id"] for r in self.all_rows)
        for row in self.all_rows:
            if identities[row["canonical_id"]] > 1:
                discriminator = compact(row["impl_header"]) or row["cfg"]
                row["canonical_id"] += " @ " + discriminator
            (self.apis if row["scope_reason"] == "stable-public-source-owned" else self.exclusions).append(row)
        for rows in (self.apis, self.exclusions):
            rows.sort(key=lambda r: r["canonical_id"])
            if len({r["canonical_id"] for r in rows}) != len(rows):
                duplicate = [key for key, count in Counter(r["canonical_id"] for r in rows).items() if count > 1]
                raise ValueError(f"Duplicate canonical identities: {duplicate}")
        self.build_defaults()
        self.build_dependencies()
        self.vstd = SelectedVstd(self.vstd_path).build(self.apis)
        return self

    def build_dependencies(self):
        imports, symbols = defaultdict(dict), defaultdict(list)
        for node in self.nodes:
            if node.kind == "use" and not nearest(node, {"fn"}):
                for binding in flatten_use(node.header):
                    target, _, alias = binding.partition(" as ")
                    alias = alias or target.rsplit("::", 1)[-1]
                    if target.startswith("crate::"):
                        target = "core::" + target[7:]
                    elif target.startswith("self::"):
                        target = node.module + target[4:]
                    elif target.startswith("super::"):
                        target = node.module.rsplit("::", 1)[0] + target[5:]
                    elif not target.startswith("core::"):
                        target = node.module + "::" + target
                    imports[node.module][alias] = target
            if node.kind == "fn" and not nearest(node, {"impl", "trait", "fn"}):
                symbols[node.module + "::" + node.name].append(node)
        for module, bindings in imports.items():
            for alias, target in bindings.items():
                if target in symbols:
                    symbols[module + "::" + alias] = symbols[target]
        macros = defaultdict(list)
        for node in self.nodes:
            if node.kind in {"macro", "macro_rules"}:
                macros[node.name].append(node)
        for node, row in self.node_rows:
            for call in json.loads(row["delegated_calls"]):
                spelling = call["call"]
                targets, resolution = [], "requires-Rust-type-or-callable-resolution"
                if spelling.endswith("!"):
                    targets = macros.get(spelling[:-1], [])
                    resolution = "macro-definition" if len(targets) == 1 else "macro-or-builtin"
                elif "." not in spelling:
                    first, separator, rest = spelling.partition("::")
                    if first in imports[node.module]:
                        path = imports[node.module][first] + (separator + rest if separator else "")
                    elif first == "crate":
                        path = "core::" + rest
                    elif first == "core":
                        path = spelling
                    elif first == "super":
                        path = node.module.rsplit("::", 1)[0] + "::" + rest
                    else:
                        path = node.module + "::" + spelling
                    targets = symbols.get(path, [])
                    if targets:
                        resolution = "source-path" if len(targets) == 1 else "cfg-alternative-source-path"
                elif re.fullmatch(r"self\.\w+", spelling):
                    method = spelling.split(".")[1]
                    impl = nearest(node, {"impl"})
                    if impl:
                        own_type = impl_parts(impl)[2]
                        targets = [candidate for candidate, _ in self.node_rows
                                   if candidate.name == method
                                   and nearest(candidate, {"impl"})
                                   and impl_parts(nearest(candidate, {"impl"}))[2] == own_type]
                        resolution = "same-self-type-candidates" if targets else resolution
                if row["self_type"] == "[T]" and row["name"] in {
                    "get", "get_mut", "get_unchecked", "get_unchecked_mut"
                } and spelling == "index." + row["name"]:
                    targets = children(self.nodes, self.traits["SliceIndex"])
                    targets = [target for target in targets if target.name == row["name"]]
                    resolution = "generic-SliceIndex-dispatch"
                self.dependencies.append({
                    "caller": row["canonical_id"], "call": spelling, "call_span": call["span"],
                    "resolution": resolution, "target_spans": json_text(sorted({t.span for t in targets})),
                    "target_signatures": json_text([t.header for t in targets]),
                })

    def owner_row(self, node):
        impl = node if node.kind == "impl" else nearest(node, {"impl"})
        generic, trait, self_type, bounds, const = impl_parts(impl) if impl else ("", "", "", "", False)
        return {
            "owner": node.module, "kind": node.kind, "name": node.name,
            "source_span": node.span, "doc_spans": json_text(node.doc_spans),
            "header": node.header, "attributes": json_text(node.attributes),
            "stability": stability(node), "const_stability": stability(node, True),
            "impl_header": impl.header if impl else "", "impl_stability": stability(impl),
            "impl_const_stability": stability(impl, True),
            "visibility": visibility(node), "self_type": self_type, "trait": trait,
            "generics": generic, "where_bounds": bounds,
            "public_paths": json_text([path for path, _ in self.exported(node)]),
            "macro_invocation": node.source.invocation.span if node.source.invocation else "",
        }

    def build_defaults(self):
        groups = defaultdict(list)
        adjacent_impls = [n for n in self.nodes if n.kind == "impl" and n not in self.owned_nodes
                          and n.source.path in set(TRAIT_FILES.values())
                          and impl_parts(n)[2] in {"[T]", "crate::slice::GetDisjointMutError"}]
        for impl in [n for n in self.owned_nodes if n.kind == "impl"] + adjacent_impls:
            _, trait_name, self_type, _, _ = impl_parts(impl)
            trait = self.find_trait(trait_name, impl)
            if not trait or not trait_name:
                continue
            overrides = {n.name for n in children(self.nodes, impl)}
            for method in children(self.nodes, trait):
                if method.name not in overrides and method.source.mask[method.head_end] == "{":
                    groups[method].append({"impl": impl.header, "span": impl.span})
        for type_node in [n for n in self.owned_nodes if n.kind in {"struct", "enum", "union"}]:
            for attr in type_node.attributes:
                match = re.match(r"#\[\s*derive(?:_const)?\(([^)]*)\)\s*\]", attr)
                if match:
                    for name in split_top(match[1]):
                        trait = self.traits[name]
                        for method in children(self.nodes, trait):
                            if method.source.mask[method.head_end] == "{" and method.name != "assert_fields_are_eq":
                                groups[method].append({"derive": attr, "type": type_node.header, "span": type_node.span})
                            elif method.name == "assert_fields_are_eq":
                                self.defaults.append({
                                    "policy": "compiler-derived-internal-interface",
                                    "trait": name, "name": method.name,
                                    "signature": method.header, "source_span": method.span,
                                    "doc_spans": json_text(method.doc_spans),
                                    "stability": stability(method),
                                    "applicability": json_text({"derive": attr, "type": type_node.header, "span": type_node.span}),
                                    "reason": "Core documents this unstable derive-only interface; compiler-generated body is not materialized here.",
                                })
        for method, applies in groups.items():
            self.defaults.append({
                "policy": "external-trait-default-not-source-owned",
                "trait": method.parent.name, "name": method.name,
                "signature": method.header, "source_span": method.span,
                "doc_spans": json_text(method.doc_spans),
                "stability": stability(method) or stability(method.parent),
                "applicability": json_text(applies),
                "reason": "Body is owned by the trait definition; no per-slice copy is counted.",
            })
        for impl in [n for n in self.nodes if n.kind == "impl" and n not in self.owned_nodes]:
            _, trait_name, self_type, _, _ = impl_parts(impl)
            if impl.source.path not in set(TRAIT_FILES.values()):
                continue
            is_blanket = re.fullmatch(r"(?:&(?:'\w+\s+)?(?:mut\s+)?)?[A-Z]", self_type) is not None
            slice_facing = self_type in {"[T]", "crate::slice::GetDisjointMutError"}
            if not trait_name or not (is_blanket or slice_facing):
                continue
            methods = children(self.nodes, impl)
            self.defaults.append({
                "policy": "external-blanket-impl" if is_blanket else "adjacent-explicit-impl",
                "trait": trait_name, "name": ",".join(n.name for n in methods),
                "signature": json_text([n.header for n in methods]),
                "source_span": impl.span, "doc_spans": json_text(impl.doc_spans),
                "stability": stability(impl), "applicability": impl.header,
                "reason": "Conditional on the exact impl bounds; owned outside slice, not counted as a slice-owned body.",
            })
        self.defaults.sort(key=lambda r: (r["policy"], r["trait"], r["name"], r["source_span"]))

    def write(self, output):
        output.mkdir(parents=True, exist_ok=True)
        write_tsv(output / "apis.tsv", self.apis, API_COLUMNS)
        write_tsv(output / "exclusions.tsv", self.exclusions, API_COLUMNS)
        write_tsv(output / "ownership.tsv", self.ownership, [
            "owner", "kind", "name", "source_span", "doc_spans", "header", "attributes",
            "stability", "const_stability", "visibility", "self_type", "trait",
            "generics", "where_bounds", "public_paths", "macro_invocation",
        ])
        write_tsv(output / "trait_surface.tsv", self.defaults, [
            "policy", "trait", "name", "signature", "source_span", "doc_spans",
            "stability", "applicability", "reason",
        ])
        write_tsv(output / "macros.tsv", self.macros, [
            "macro", "invocation_span", "definition_span", "policy",
            "generated_functions", "invocation",
        ])
        adjacent = [self.owner_row(n) for n in self.nodes if n.source.path in {
            "range.rs", "range/iter.rs", "range/legacy.rs", "ops/range.rs", "ops/index_range.rs", "index.rs"
        } and n.kind in {"struct", "enum", "trait", "impl", "use", "fn", "macro", "macro_rules", "macro_call"}]
        write_tsv(output / "range_dependencies.tsv", adjacent, [
            "owner", "kind", "name", "source_span", "doc_spans", "header", "attributes",
            "stability", "const_stability", "visibility", "self_type", "trait",
            "impl_header", "impl_stability", "impl_const_stability",
            "generics", "where_bounds", "public_paths", "macro_invocation",
        ])
        maybe_uninit = [self.owner_row(n) for n in self.nodes
                        if n.source.path == "mem/maybe_uninit.rs" and n.kind in {
                            "struct", "union", "impl", "trait", "fn"
                        }]
        write_tsv(output / "maybe_uninit_dependencies.tsv", maybe_uninit, [
            "owner", "kind", "name", "source_span", "doc_spans", "header", "attributes",
            "stability", "const_stability", "visibility", "self_type", "trait",
            "impl_header", "impl_stability", "impl_const_stability",
            "generics", "where_bounds",
        ])
        write_tsv(output / "dependencies.tsv", self.dependencies, [
            "caller", "call", "call_span", "resolution", "target_spans", "target_signatures",
        ])
        index_domains = []
        for impl in [n for n in self.nodes if n.kind == "impl" and n.source.path in {
            "slice/index.rs", "slice/mod.rs", "index.rs"
        }]:
            _, trait, self_type, _, _ = impl_parts(impl)
            if base_name(trait) not in {"SliceIndex", "GetDisjointMutIndex", "SlicePattern"}:
                continue
            trait_node = self.find_trait(trait, impl)
            members = children(self.nodes, impl)
            if impl.source.path == "index.rs":
                policy = "unstable-adjacent-wrapper; not a stable index domain"
            elif self_type == "ops::IndexRange":
                policy = "private-index-invariant dependency"
            else:
                policy = "stable-wrapper dispatch domain; helper methods are not stable public APIs"
            index_domains.append({
                "trait": trait, "self_type": self_type, "impl_header": impl.header,
                "source_span": impl.span, "impl_stability": stability(impl),
                "const_stability": stability(impl, True), "policy": policy,
                "methods": json_text([{"name": m.name, "signature": m.header, "span": m.span}
                                      for m in members]),
                "trait_method_gates": json_text([
                    {"name": m.name, "gate": stability(m) or stability(trait_node)}
                    for m in children(self.nodes, trait_node)
                ]),
            })
        write_tsv(output / "index_domains.tsv", index_domains, [
            "trait", "self_type", "impl_header", "source_span", "impl_stability",
            "const_stability", "policy", "methods", "trait_method_gates",
        ])
        manifest = [{
            "source": path, "sha256": hashlib.sha256(source.text.encode()).hexdigest(),
            "lines": str(len(source.text.splitlines())),
            "role": "slice-owned" if path.startswith("slice/") else "adjacent-source",
        } for path, source in sorted(self.sources.items())]
        write_tsv(output / "sources.tsv", manifest, ["source", "sha256", "lines", "role"])
        counts = [{"set": "apis", "dimension": "owner", "key": key, "count": count}
                  for key, count in sorted(Counter(r["owner"] for r in self.apis).items())]
        counts += [{"set": "apis", "dimension": "kind", "key": key, "count": count}
                   for key, count in sorted(Counter(r["kind"] for r in self.apis).items())]
        counts += [{"set": "apis", "dimension": "signature_origin", "key": key, "count": count}
                   for key, count in sorted(Counter(r["signature_origin"] for r in self.apis).items())]
        counts += [{"set": "exclusions", "dimension": "reason", "key": key, "count": count}
                   for key, count in sorted(Counter(r["scope_reason"].split(":")[0] for r in self.exclusions).items())]
        counts += [{"set": "all-owned-candidates", "dimension": "signature_origin", "key": key, "count": count}
                   for key, count in sorted(Counter(r["signature_origin"] for r in self.all_rows).items())]
        counts += [{"set": "trait_surface", "dimension": "policy", "key": key, "count": count}
                   for key, count in sorted(Counter(r["policy"] for r in self.defaults).items())]
        counts += [{"set": "sources", "dimension": "role", "key": key, "count": count}
                   for key, count in sorted(Counter(r["role"] for r in manifest).items())]
        counts += [{"set": name, "dimension": "total", "key": "rows", "count": len(rows)}
                   for name, rows in [("apis", self.apis), ("exclusions", self.exclusions),
                                      ("ownership", self.ownership), ("trait_surface", self.defaults),
                                      ("macros", self.macros), ("range_dependencies", adjacent),
                                      ("maybe_uninit_dependencies", maybe_uninit),
                                      ("dependencies", self.dependencies),
                                      ("index_domains", index_domains),
                                      ("sources", manifest)]]
        write_tsv(output / "counts.tsv", counts, ["set", "dimension", "key", "count"])
        self.vstd.write(output)


def call_sites(node):
    mask = node.source.mask[node.head_end:node.end]
    calls = []
    pattern = re.compile(r"(?P<call>(?:[A-Za-z_]\w*::)*[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*(?:(?P<macro>!)\s*(?=[({[])|(?=::\s*<|\())")
    skip = {"if", "while", "for", "match", "loop", "fn", "unsafe", "return", "Some", "Ok", "Err",
            "const"}
    for match in pattern.finditer(mask):
        text = match["call"]
        if text in skip:
            continue
        if re.search(r"\bfn\s+$", mask[:match.start()]):
            continue
        kind = "macro" if match["macro"] else ("receiver-call-requires-type-resolution" if "." in text else
                                             "source-path-or-callable")
        calls.append({"call": text + ("!" if match["macro"] else ""), "kind": kind,
                      "span": node.source.span(node.head_end + match.start(),
                                               node.head_end + match.end())})
    return calls


VSTD_COVERAGE_COLUMNS = [
    "canonical_id", "classification", "contract_extent", "contract_refs",
    "model_type_refs", "compiler_support_refs", "receiver_model", "conditions",
    "limitations", "scan_queries", "baseline", "source_tree_sha256",
    "rust_source_body_proof",
]
VSTD_SOURCE_COLUMNS = ["source", "sha256", "bytes", "lines"]
VSTD_SCAN_COLUMNS = [
    "query_id", "pattern", "matching_code_lines", "matches",
    "assume_specification_candidates",
]
VSTD_CLASSES = {
    "assumed-contract", "assumed-conditional", "assumed-partial-domain",
    "generic-trait-conditional", "generic-trait-only", "missing",
}


class SelectedVstd:
    """Audited receiver-aware mapping, with a replayable whole-vstd lexical scan.

    Token hits are evidence to inspect, never coverage. The fixed tree and API
    identity digests make the negative decisions fail closed on either drift.
    This deliberately does not parse or claim to verify external Rust bodies.
    """

    def __init__(self, root=SELECTED_VSTD):
        self.root = Path(root)
        self.sources, self.manifest = {}, []
        for path in sorted(self.root.rglob("*.rs")):
            data = path.read_bytes()
            name = path.relative_to(self.root).as_posix()
            self.sources[name] = Source(name, data.decode("utf-8"))
            self.manifest.append({
                "source": name, "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": str(len(data)), "lines": str(len(data.splitlines())),
            })
        digest_input = "".join(r["source"] + "\t" + r["sha256"] + "\n"
                               for r in self.manifest)
        self.tree_sha256 = hashlib.sha256(digest_input.encode()).hexdigest()
        if self.tree_sha256 != VSTD_TREE_SHA256:
            raise ValueError("Selected vstd source tree differs from the audited "
                             f"{VSTD_RELEASE} baseline: {self.tree_sha256}")
        self.assumptions = []
        for source in self.sources.values():
            for match in re.finditer(r"\bassume_specification\b", source.mask):
                pos, angles = match.end(), 0
                while pos < len(source.mask):
                    char = source.mask[pos]
                    if char == "[" and angles == 0:
                        break
                    if char in "([{":
                        pos = source.pairs[pos] + 1
                        continue
                    if char == "<":
                        angles += 1
                    elif char == ">" and source.mask[pos - 1] != "-":
                        angles -= 1
                    pos += 1
                if pos == len(source.mask):
                    raise ValueError(f"Unparsed vstd assumption: {source.path}")
                target_end = source.pairs[pos]
                target = compact(source.text[pos + 1:target_end])
                end = self.statement_end(source, target_end + 1)
                start = source.mask.rfind("\n", 0, match.start()) + 1
                start += len(source.mask[start:match.start()]) - len(
                    source.mask[start:match.start()].lstrip())
                attrs, _ = attributes_before(source, start)
                if attrs:
                    start = attrs[0][0]
                self.assumptions.append({
                    "span": source.span(start, end),
                    "declaration": "assume_specification[" + target + "]",
                    "target": target,
                })
        self.rows, self.scans = [], []
        self.queries = {}

    @staticmethod
    def statement_end(source, start):
        pos = start
        while pos < len(source.mask):
            char = source.mask[pos]
            if char in "([{":
                pos = source.pairs[pos] + 1
            elif char == ";":
                return pos + 1
            else:
                pos += 1
        raise ValueError(f"Unterminated vstd declaration: {source.path}:{start}")

    def ref(self, path, needle, kind="block", scope=None):
        source = self.sources[path]
        lower, upper = 0, len(source.mask)
        if scope:
            begin = source.mask.index(scope)
            opening = source.mask.index("{", begin)
            lower, upper = opening + 1, source.pairs[opening]
        pattern = re.escape(needle).replace(r"\ ", r"\s+")
        matches = list(re.finditer(pattern, source.mask[lower:upper]))
        if len(matches) != 1:
            raise ValueError(f"Expected one audited declaration: {path}: {needle}")
        start = lower + matches[0].start()
        if kind == "block":
            opening = source.mask.index("{", lower + matches[0].end())
            end = source.pairs[opening] + 1
        else:
            end = self.statement_end(source, lower + matches[0].end())
        attrs, _ = attributes_before(source, start)
        if attrs:
            start = attrs[0][0]
        return {"span": source.span(start, end), "declaration": compact(needle)}

    def assumption(self, target, path=None):
        key = re.sub(r"\s+", "", target)
        candidates = [
            r for r in self.assumptions
            if re.sub(r"\s+", "", r["target"]) == key
            and (path is None or r["span"].startswith(path + ":"))
        ]
        if len(candidates) != 1:
            raise ValueError(f"Expected one audited vstd binding: {target}")
        return candidates[0]

    def query(self, key, pattern):
        if key in self.queries and self.queries[key] != pattern:
            raise ValueError(f"Inconsistent vstd scan query: {key}")
        self.queries[key] = pattern
        return key

    def type_refs(self, api):
        typ = api["self_type"]
        refs, queries = [], []
        receiver_model = "no-selected-vstd-receiver-type-or-state-model-found"
        if typ.startswith(("[", "&")) or not typ:
            refs.append(self.ref("slice.rs", "impl<T> View for [T]"))
            receiver_model = "primitive-slice-Seq-view; not an API body or pointer correspondence"
            queries.append(self.query("type:slice", r"\[\s*(?:T|U|u8)\s*\]"))
        if typ.startswith("[["):
            refs.append(self.ref("array.rs", "impl<T, const N: usize> View for [T; N]"))
        if "MaybeUninit" in typ:
            refs += [
                self.ref("std_specs/maybe_uninit.rs", "pub struct ExMaybeUninit", "statement"),
                self.ref("std_specs/maybe_uninit.rs",
                         "impl<T> MaybeUninitAdditionalSpecFns<T> for MaybeUninit<T>"),
            ]
            queries.append(self.query("type:MaybeUninit", r"\bMaybeUninit\b"))
        found = re.match(r"core::slice::(\w+)", typ)
        if found:
            name = found[1]
            queries.append(self.query("type:" + name, r"\b" + name + r"\b"))
            if name in {"Iter", "IterMut"}:
                refs.append(self.ref("std_specs/slice.rs", "pub struct Ex" + name + "<",
                                     "statement"))
                header = ("impl <'a, T: 'a>" if name == "Iter" else "impl<'a, T: 'a>")
                refs.append(self.ref("std_specs/slice.rs", header
                                     + " super::iter::IteratorSpecImpl for "
                                     + name + "<'a, T>"))
                receiver_model = "opaque-external-type; prophetic-IteratorSpecImpl"
        return refs, queries, receiver_model

    def index_refs(self, method):
        refs = [
            self.ref("slice.rs", "pub trait ExSliceIndex"),
            self.ref("slice.rs", "fn " + method + "(", "statement",
                     scope="pub trait ExSliceIndex"),
        ]
        for index in ("usize", "Range<usize>", "RangeTo<usize>", "RangeFrom<usize>",
                      "RangeToInclusive<usize>", "RangeFull", "RangeInclusive<usize>"):
            refs.append(self.ref("std_specs/slice.rs",
                                 "impl<T> super::super::slice::SliceIndexSpecImpl<[T]> for "
                                 + index))
            refs.append(self.assumption(f"<{index} as SliceIndex<[T]>>::{method}",
                                        "std_specs/slice.rs"))
        for helper in ("generic_slice_in_bounds", "generic_slice_index_postcondition",
                       "generic_slice_index_mut_postcondition"):
            refs.append(self.ref("std_specs/slice.rs", "pub open spec fn " + helper + "<"))
        refs += self.range_refs()
        return refs

    def range_refs(self):
        refs = [self.ref("std_specs/range.rs", "pub trait ExRangeBounds")]
        for header in (
            "impl<T> RangeBoundsSpecImpl<T> for Range<T>",
            "impl<T: ?Sized> RangeBoundsSpecImpl<T> for RangeFull",
            "impl<T> RangeBoundsSpecImpl<T> for RangeFrom<T>",
            "impl<T> RangeBoundsSpecImpl<T> for RangeTo<T>",
            "impl<T> RangeBoundsSpecImpl<T> for RangeInclusive<T>",
            "impl<T> RangeBoundsSpecImpl<T> for RangeToInclusive<T>",
            "impl<T> RangeBoundsSpecImpl<T> for (Bound<T>, Bound<T>)",
            "impl<'a, T: ?Sized + 'a> RangeBoundsSpecImpl<T> for (Bound<&'a T>, Bound<&'a T>)",
            "impl<T> RangeBoundsSpecImpl<T> for RangeFrom<&T>",
            "impl<T> RangeBoundsSpecImpl<T> for RangeTo<&T>",
            "impl<T> RangeBoundsSpecImpl<T> for Range<&T>",
            "impl<T> RangeBoundsSpecImpl<T> for RangeInclusive<&T>",
            "impl<T> RangeBoundsSpecImpl<T> for RangeToInclusive<&T>",
        ):
            refs.append(self.ref("std_specs/range.rs", header))
        for helper in ("slice_range_start", "slice_range_end", "slice_range_valid"):
            refs.append(self.ref("std_specs/range.rs", "pub open spec fn " + helper + "<"))
        refs += [
            self.ref("std_specs/range.rs", "pub struct ExRangeInclusive", "statement"),
            self.ref("std_specs/range.rs", "pub struct RangeInclusiveView"),
            self.ref("std_specs/range.rs", "impl<Idx> View for RangeInclusive<Idx>"),
            self.ref("std_specs/range.rs", "pub open spec fn spec_range_inclusive_end_bound"),
        ]
        return refs

    def map_api(self, api):
        canonical, name, trait = api["canonical_id"], api["name"], api["trait"]
        models, queries, receiver_model = self.type_refs(api)
        queries.insert(0, self.query("name:" + name, r"\b" + name + r"\b"))
        contracts, compiler = [], []
        classification, extent = "missing", "no-applicable-method-contract"
        conditions = "Exact canonical receiver and trait, not method-name equality."
        limitations = ("No applicable API contract found in the pinned whole-vstd scan. "
                       "Any linked type/view alone does not specify this method.")
        direct_names = {
            "len", "is_empty", "first", "last", "first_mut", "last_mut", "split_at",
            "split_at_mut", "split_at_checked", "split_first", "split_first_mut",
            "copy_from_slice", "copy_within", "starts_with", "ends_with",
            "get", "get_mut", "iter", "iter_mut",
        }
        direct = None
        if api["self_type"] == "[T]" and not trait and name in direct_names:
            target = f"<[T]>::{name}"
            if name in {"get", "get_mut"}:
                target += "::<I>"
            elif name == "copy_within":
                target += "::<R>"
            direct = self.assumption(target, "slice.rs" if name in {"len", "is_empty"}
                                     else "std_specs/slice.rs")
        elif canonical == "<[T] as core::cmp::PartialEq<[U]>>::eq":
            direct = self.assumption("<[T] as PartialEq<[U]>>::eq", "std_specs/slice.rs")
        elif canonical == "<&'a [T] as core::iter::IntoIterator>::into_iter":
            direct = self.assumption("<&'a [T] as core::iter::IntoIterator>::into_iter",
                                     "std_specs/slice.rs")
        elif canonical in {"<[T] as core::ops::Index<I>>::index",
                           "<[T] as core::ops::IndexMut<I>>::index_mut"}:
            index_trait = "Index" if name == "index" else "IndexMut"
            direct = self.assumption(f"<[T] as {index_trait}<I>>::{name}",
                                     "std_specs/slice.rs")

        if direct:
            contracts.append(direct)
            classification, extent = "assumed-contract", "returned-values-and-slice-contents"
            conditions = "The declaration is assumed by vstd, not a verified Rust source body."
            limitations = "No Rust 1.96 source-body correctness or completeness proof is implied."
            if name == "len":
                extent = "length"
                compiler.append(self.ref("slice.rs", "pub uninterp spec fn spec_slice_len",
                                         "statement"))
                models.append(self.ref("slice.rs", "pub broadcast axiom fn axiom_spec_len",
                                       "statement"))
            elif name == "is_empty":
                extent = "emptiness"
                models.append(self.ref("slice.rs", "pub open spec fn spec_slice_is_empty"))
            if name in {"split_at", "split_at_mut", "copy_from_slice"}:
                extent = "nonpanicking-domain-contents"
                conditions += (" Requires mid <= len." if name.startswith("split_at")
                               else " Requires equal lengths and the original T: Copy bound.")
                limitations += " Panicking executions are outside the vstd precondition."
            if name in {"first_mut", "last_mut", "split_at_mut", "split_first_mut", "iter_mut"}:
                extent += "-and-final-writeback"
                models.append(self.ref("slice.rs", "pub axiom fn mut_ref_slice_len_eq",
                                       "statement"))
            if name in {"iter", "into_iter", "iter_mut"}:
                iterator = "IterMut" if name == "iter_mut" else "Iter"
                refs, _, _ = self.type_refs({"self_type": f"core::slice::{iterator}<'a, T>"})
                models += refs
                extent = "constructor-to-remaining-sequence" + (
                    "-and-final-writeback" if iterator == "IterMut" else "")
                if iterator == "Iter":
                    models.append(self.ref("std_specs/slice.rs",
                                           "pub uninterp spec fn into_iter_elts", "statement"))
                limitations += " Iterator pointer/ZST representation correspondence is not proved here."
            if name in {"eq", "starts_with", "ends_with"}:
                classification = "assumed-conditional"
                extent = "contents-conditional-on-element-equality-law"
                contracts.append(self.ref("std_specs/cmp.rs", "fn eq(", "statement",
                                          scope="pub trait ExPartialEq"))
                models.append(self.ref("std_specs/cmp.rs", "pub trait ExPartialEq"))
                if name == "eq":
                    models.append(self.ref("std_specs/slice.rs",
                                           "impl<T, U> super::cmp::PartialEqSpecImpl<[U]> for [T]"))
                else:
                    models.append(self.ref("std_specs/slice.rs",
                                           "pub open spec fn spec_slice_" + name + "<"))
                conditions += " Content result is gated by element PartialEqSpec::obeys_eq_spec()."
                limitations += " Arbitrary lawful/stateful PartialEq implementations are not unconditionally modeled."
            if name in {"get", "get_mut", "index", "index_mut"}:
                classification, extent = "assumed-partial-domain", "SliceIndex-dispatch-with-seven-concrete-models"
                models += self.index_refs(name)
                conditions += (" Concrete [T] index models: usize and legacy core::ops::{Range, "
                               "RangeTo, RangeFrom, RangeToInclusive, RangeFull, RangeInclusive}.")
                limitations += (" No [T] SliceIndexSpecImpl for a Bound pair or the four "
                                "core::range replacement types; a str Bound-pair impl is not applicable. "
                                "Generic call_ensures dispatch is not a concrete model of every lawful I.")
                queries += [
                    self.query("model:SliceIndexSpecImpl", r"\bSliceIndexSpecImpl\b"),
                    self.query("path:replacement-range", r"\b(?:core|std)::range::"),
                ]
                if name.startswith("index"):
                    models.append(self.ref("std_specs/slice.rs",
                                           "impl<T, I: SliceIndex<[T]>> super::core::IndexSpecImpl<I> for [T]"))
                    contracts.append(self.ref("std_specs/core.rs", "pub trait ExIndex"
                                              + ("Mut" if name == "index_mut" else "") + "<"))
                    helpers = (("pub uninterp spec fn spec_slice_update", "pub broadcast axiom fn axiom_spec_slice_update")
                               if name == "index_mut" else
                               ("pub uninterp spec fn spec_slice_index", "pub broadcast axiom fn axiom_spec_slice_index"))
                    compiler.append(self.ref("slice.rs", helpers[0], "statement"))
                    models.append(self.ref("slice.rs", helpers[1], "statement"))
                    if name == "index":
                        compiler.append(self.ref("slice.rs", "pub exec fn slice_index_get"))
                    limitations += " Linked diagnostic hooks concern scalar indexing, not all generic I."
            if name == "copy_within":
                classification, extent = "assumed-partial-domain", "nonpanicking-range-model-content-and-frame"
                models += self.range_refs()
                models.append(self.ref("std_specs/slice.rs", "pub open spec fn copy_within_result"))
                conditions += (" Original T: Copy; normalized source bounds and destination extent "
                               "must be valid. RangeBoundsSpec models legacy ranges, Bound pairs and "
                               "the explicitly linked reference-bound specializations.")
                limitations += (" No replacement core::range model or general proof relating an "
                                "arbitrary user's RangeBounds methods to its spec-bound functions. "
                                "Panicking executions are outside the precondition.")
                queries += [
                    self.query("model:RangeBoundsSpecImpl", r"\bRangeBoundsSpecImpl\b"),
                    self.query("path:replacement-range", r"\b(?:core|std)::range::"),
                ]
        else:
            generic = None
            if trait == "core::iter::Iterator" and name in {"next", "all", "any", "find"}:
                generic = ("std_specs/iter.rs", "ExIterator")
            elif trait == "core::iter::DoubleEndedIterator" and name == "next_back":
                generic = ("std_specs/iter.rs", "ExDoubleEndedIterator")
            elif trait == "core::iter::ExactSizeIterator" and name == "len":
                generic = ("std_specs/iter.rs", "ExExactSizeIterator")
            elif trait == "core::iter::IntoIterator":
                generic = ("std_specs/iter.rs", "ExIntoIterator")
            elif trait == "core::clone::Clone":
                generic = ("std_specs/clone.rs", "ExClone")
            elif trait == "core::default::Default":
                generic = ("std_specs/default.rs", "ExDefault")
            elif trait == "core::cmp::PartialEq":
                generic = ("std_specs/cmp.rs", "ExPartialEq")
            elif trait in {"core::cmp::PartialOrd", "core::cmp::Ord"}:
                generic = ("std_specs/cmp.rs", "Ex" + trait.rsplit("::", 1)[1])
            if generic:
                path, declaration = generic
                scope = "pub trait " + declaration
                contracts += [self.ref(path, scope),
                              self.ref(path, "fn " + name + ("<" if name in {"all", "any", "find"} else "("),
                                       "statement", scope=scope)]
                classification, extent = "generic-trait-only", "law-gated-without-receiver-model"
                conditions = "External trait binding only; not a concrete method-body contract for this receiver."
                limitations = ("No receiver-specific law/model supplied for this API. "
                               "Trait default_ensures are not a proof of source-written overrides.")
                if trait in {"core::clone::Clone", "core::default::Default", "core::iter::IntoIterator"}:
                    extent = "signature-only-no-postcondition"
                    limitations = "The generic trait member supplies no value/content postcondition for this receiver."
                if trait == "core::clone::Clone":
                    models += [self.ref("pervasive.rs", "pub open spec fn strictly_cloned"),
                               self.ref("pervasive.rs", "pub open spec fn cloned")]
                    limitations += " cloned delegates to Clone call_ensures (or identity); no iterator clone-state relation is supplied."
                if trait == "core::iter::IntoIterator":
                    limitations += (" The I: Iterator blanket into_iter contract does not apply to "
                                    "&mut [T]; <[T]>::iter_mut is a distinct entry point.")
                if trait.startswith("core::iter::") and re.match(r"core::slice::Iter(?:Mut)?<", api["self_type"]):
                    classification = "generic-trait-conditional"
                    extent = "prophetic-state-transition" if name != "len" else "remaining-length"
                    conditions = ("ExIter/ExIterMut and IteratorSpecImpl exist for this exact receiver. "
                                  "Generic method ensures depend on obeys_prophetic_iter_laws; "
                                  "constructor contracts relate remaining to slice contents.")
                    limitations = ("Generic trusted trait contract, not a source-body proof or a "
                                   "separately tested frontend import/call. No concrete pointer/ZST invariant.")
                    if name in {"all", "any", "find"}:
                        extent = "law-and-callback-conditional"
                        conditions += " Requires callback preconditions and uses call_ensures on observed results."
                        limitations += " No explicit per-invocation FnMut state trace or callback/drop effects are specified."
                    if name == "len":
                        limitations += " exact_len is an abstract trait observation, not a concrete slice-iterator field model."
            if trait in {"core::fmt::Debug", "core::fmt::Display"}:
                short = trait.rsplit("::", 1)[1]
                classification, extent = "generic-trait-only", "precondition-only-no-formatting-postcondition"
                contracts = [
                    self.ref("std_specs/fmt.rs", "macro_rules! def_fmt_trait"),
                    self.ref("std_specs/fmt.rs", "fn fmt(", "statement"),
                    self.ref("std_specs/fmt.rs", f"def_fmt_trait!(core::fmt::{short},", "statement"),
                ]
                conditions = "Macro-instantiated external trait member requires self.fmt_req(f)."
                limitations = ("No output text, formatter state, or receiver-specific fmt_req model "
                               "is supplied; compiler formatting machinery is not formatting correctness.")

        if classification == "missing":
            false_friends = {
                "as_slice": "Array, Vec and Option as_slice bindings are not slice::Iter/IterMut::as_slice.",
                "as_ref": "Seq::as_ref and Option/Result/SharedReference helpers are not Iter/IterMut as AsRef<[T]>.",
                "as_ptr": "SharedReference::as_ptr is not <[T]>::as_ptr.",
                "assume_init_ref": "Scalar MaybeUninit::assume_init_ref is not [MaybeUninit<T>]::assume_init_ref.",
                "assume_init_mut": "Scalar MaybeUninit::assume_init_mut is not [MaybeUninit<T>]::assume_init_mut.",
                "is_ascii": "str::is_ascii/String helpers are not [u8]::is_ascii.",
                "split_off": "Vec/VecDeque split_off has a different receiver and signature.",
                "contains": "Set and range contains contracts are not [T]::contains.",
                "nth": "A chars().nth call inside a string helper is not an iterator nth contract.",
                "reverse": "Seq::reverse is a model operation, not [T]::reverse.",
                "swap": "core::mem::swap and atomic swap are not <[T]>::swap.",
                "last": "A slice observer or Seq::last is not Iterator::last.",
                "count": "Multiset/token count and helper callsites are not Iterator::count.",
                "fold": "Set/ISet spec folds are not Iterator::fold.",
                "split": "Resource/token proof splitting is not a slice split iterator constructor.",
                "split_mut": "Resource-map permission splitting is not <[T]>::split_mut.",
                "position": "A map cursor position field is not Iterator::position.",
            }
            if name in false_friends:
                limitations += " " + false_friends[name]
        return {
            "canonical_id": canonical, "classification": classification, "contract_extent": extent,
            "contract_refs": json_text(contracts), "model_type_refs": json_text(models),
            "compiler_support_refs": json_text(compiler), "receiver_model": receiver_model,
            "conditions": conditions, "limitations": limitations,
            "scan_queries": json_text(queries),
            "baseline": VSTD_RELEASE + "@" + VSTD_COMMIT,
            "source_tree_sha256": self.tree_sha256, "rust_source_body_proof": "not-established-by-vstd-mapping",
        }

    def build(self, apis):
        identity_input = "".join(r["canonical_id"] + "\n"
                                 for r in sorted(apis, key=lambda r: r["canonical_id"]))
        if hashlib.sha256(identity_input.encode()).hexdigest() != VSTD_API_IDS_SHA256:
            raise ValueError("Source-owned API identities differ from the audited vstd mapping domain")
        self.rows = [self.map_api(api) for api in apis]
        for api, row in zip(apis, self.rows):
            api["existing_vstd_coverage"] = row["classification"]
        for key, pattern in sorted(self.queries.items()):
            matches = []
            for path, source in self.sources.items():
                lines = sorted({bisect.bisect_right(source.lines, m.start())
                                for m in re.finditer(pattern, source.mask)})
                if lines:
                    matches.append({"source": path, "lines": lines})
            candidates = []
            if key.startswith("name:"):
                name = key.removeprefix("name:")
                candidates = [r for r in self.assumptions
                              if re.search(r"::" + re.escape(name) + r"\s*(?:::\s*<.*>)?$", r["target"])]
            self.scans.append({
                "query_id": key, "pattern": pattern,
                "matching_code_lines": str(sum(len(m["lines"]) for m in matches)),
                "matches": json_text(matches), "assume_specification_candidates": json_text(candidates),
            })
        return self

    def write(self, output):
        write_tsv(output / "vstd_coverage.tsv", self.rows, VSTD_COVERAGE_COLUMNS)
        write_tsv(output / "vstd_sources.tsv", self.manifest, VSTD_SOURCE_COLUMNS)
        write_tsv(output / "vstd_scan.tsv", self.scans, VSTD_SCAN_COLUMNS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core-src", type=Path, default=DEFAULT_CORE)
    parser.add_argument("--output", type=Path, default=ROOT / "inventory")
    parser.add_argument("--vstd-src", type=Path, default=SELECTED_VSTD,
                        help="Exact selected upstream vstd source tree (hash checked)")
    parser.add_argument("--vstd-only", action="store_true",
                        help="Fill/replay selected-vstd mapping without rereading Rust ownership")
    args = parser.parse_args()
    if args.vstd_only:
        apis = read_tsv(args.output / "apis.tsv")
        vstd = SelectedVstd(args.vstd_src).build(apis)
        write_tsv(args.output / "apis.tsv", apis, API_COLUMNS)
        vstd.write(args.output)
        print(f"selected vstd {VSTD_RELEASE}: {dict(sorted(Counter(r['classification'] for r in vstd.rows).items()))}")
        return
    inventory = Inventory(args.core_src, args.vstd_src).build()
    inventory.write(args.output)
    print(f"stable source-owned APIs: {len(inventory.apis)}; excluded/dependency declarations: "
          f"{len(inventory.exclusions)}; selected vstd: {VSTD_RELEASE}")


if __name__ == "__main__":
    main()
