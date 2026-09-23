#!/usr/bin/env python3
"""Extract the source-owned alloc::vec surface; never read generated specs or vstd."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import io
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "inventory/source-tests/parser"))
from tree_sitter import Language, Parser
import tree_sitter_rust

DEFAULT_LIBRARY = Path(
    "/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library"
)
PARSER = Parser(Language(tree_sitter_rust.language()))
FUNCTIONS = {"function_item", "function_signature_item"}
COMMENTS = {"line_comment", "block_comment"}
DECLARATIONS = {
    "function_item", "function_signature_item", "impl_item", "trait_item",
    "struct_item", "enum_item", "union_item", "type_item", "associated_type",
    "const_item", "static_item", "mod_item", "use_declaration", "macro_definition",
    "extern_crate_declaration", "foreign_mod_item",
}
TRAIT_FILES = {
    **{n: "core/src/cmp.rs" for n in ("PartialEq", "Eq", "PartialOrd", "Ord")},
    "Clone": "core/src/clone.rs",
    "Hash": "core/src/hash/mod.rs",
    "Debug": "core/src/fmt/mod.rs",
    "Default": "core/src/default.rs",
    **{n: "core/src/convert/mod.rs" for n in ("AsRef", "AsMut", "From", "TryFrom")},
    **{n: "core/src/ops/deref.rs" for n in ("Deref", "DerefMut", "DerefPure")},
    **{n: "core/src/ops/index.rs" for n in ("Index", "IndexMut")},
    "Drop": "core/src/ops/drop.rs",
    "Iterator": "core/src/iter/traits/iterator.rs",
    "DoubleEndedIterator": "core/src/iter/traits/double_ended.rs",
    "ExactSizeIterator": "core/src/iter/traits/exact_size.rs",
    **{n: "core/src/iter/traits/collect.rs"
       for n in ("IntoIterator", "FromIterator", "Extend")},
    **{n: "core/src/iter/traits/marker.rs"
       for n in ("FusedIterator", "TrustedFused", "TrustedLen", "InPlaceIterable")},
    "SourceIter": "core/src/iter/adapters/mod.rs",
    "TrustedRandomAccessNoCoerce": "core/src/iter/adapters/zip.rs",
}
TRAIT_PATHS = {
    **{n: f"core::cmp::{n}" for n in ("PartialEq", "Eq", "PartialOrd", "Ord")},
    "Clone": "core::clone::Clone", "Hash": "core::hash::Hash",
    "Debug": "core::fmt::Debug", "Default": "core::default::Default",
    **{n: f"core::convert::{n}"
       for n in ("AsRef", "AsMut", "From", "TryFrom", "Into", "TryInto")},
    **{n: f"core::ops::{n}"
       for n in ("Deref", "DerefMut", "DerefPure", "Index", "IndexMut", "Drop")},
    **{n: f"core::iter::{n}" for n in TRAIT_FILES if "/iter/" in TRAIT_FILES[n]},
    "Send": "core::marker::Send", "Sync": "core::marker::Sync",
    "UnwindSafe": "core::panic::UnwindSafe",
}
PUBLIC_TYPES = ("Vec", "IntoIter", "Drain", "Splice", "ExtractIf", "PeekMut")
ALIASES = {
    **TRAIT_PATHS,
    **{n: f"alloc::vec::{n}" for n in PUBLIC_TYPES},
    "Box": "alloc::boxed::Box", "Cow": "alloc::borrow::Cow",
    "Allocator": "core::alloc::Allocator", "Global": "alloc::alloc::Global",
    "MaybeUninit": "core::mem::MaybeUninit", "NonNull": "core::ptr::NonNull",
    "Range": "core::ops::Range", "RangeBounds": "core::ops::RangeBounds",
}

# Each row describes actual source/delegation dependencies, not a work schedule.
MODULE_ANALYSIS = {
    "mod.rs": {
        "role": "Vec 表示、固有方法、转换/借用/顺序/散列/析构；含稳定 doc(hidden) 自由函数 from_elem。",
        "depends_on": ["RawVec", "Allocator", "core::slice", "alloc::slice", "into_iter",
                       "drain", "splice", "extract_if", "spec_from_elem", "spec_extend",
                       "spec_from_iter", "set_len_on_drop"],
        "views": ["vec_contents", "allocation_layout", "borrow_writeback", "callback_state"],
        "obligations": "Seq 对应已初始化前缀；len<=capacity、ZST/isize 限界；spare 与已初始化区不重叠；原始指针内容/有效期不能仅由地址推得；Clone/FnMut/Drop 不得增加 Copy/Eq/'static 假设。",
    },
    "into_iter.rs": {
        "role": "拥有分配的双端移出迭代器；显式消费者、Clone/Default/Drop；私有回收接口与不稳定优化 trait。",
        "depends_on": ["Vec::into_iter", "RawVec", "core::slice", "in_place_collect"],
        "views": ["owned_remaining", "allocation_layout", "borrow_writeback", "callback_state"],
        "obligations": "构造后 remaining 随 next/next_back/fold/try_fold 更新；ZST end 用字节距离编码长度；as_mut_slice 写回剩余区域；Clone 保留 allocator.clone；Drop 释放剩余元素及原分配。",
    },
    "drain.rs": {
        "role": "带源 Vec 独占借用的区间移出迭代器；析构移动尾部；keep_rest/allocator 不稳定。",
        "depends_on": ["Vec::drain", "core::slice::Iter", "Vec::set_len", "Vec::truncate"],
        "views": ["drain_regions", "borrow_writeback", "allocation_layout"],
        "obligations": "head、remaining、已移出区、tail 分区；返回 T 为移出值不是 &mut T；尾部复原依赖真实 Drop，不能将 borrow final 等同于析构；forget 可泄漏范围外元素。",
    },
    "splice.rs": {
        "role": "Drain 包装与延迟替换；显式 next/next_back/size_hint/Drop，另有内建 derive(Debug)::fmt。",
        "depends_on": ["drain", "Vec::extend", "Vec::from_iter", "RawVec::reserve"],
        "views": ["drain_regions", "replacement_iterator", "callback_state"],
        "obligations": "replace_with 仅在 Drop 中消费；fill/move_tail 为私有 Drain 方法；不足/恰好/过量及临时 Vec 分支都须保留；泄漏时移除数量未规定。ExactSizeIterator::len 来自默认实现。",
    },
    "extract_if.rs": {
        "role": "闭包决定移出项的惰性迭代器；new 私有、allocator 不稳定；Iterator/Drop/Debug 稳定。",
        "depends_on": ["Vec::extract_if", "slice::range", "Vec::set_len"],
        "views": ["extract_regions", "callback_state", "borrow_writeback"],
        "obligations": "vec/idx/end/del/old_len/pred 与保留前缀、未扫描区和范围外尾部对应；谓词可修改 T/自身状态且按顺序执行；未消费元素在 Drop 中保留；panic 项不被移出。",
    },
    "cow.rs": {
        "role": "源码归属于 vec 的 Cow<[T]> 转换与 FromIterator；即使 owner 不是 Vec 也计入。",
        "depends_on": ["alloc::borrow::Cow", "Vec::as_slice", "Vec::from_iter"],
        "views": ["cow_variant_contents", "vec_contents", "borrow_writeback"],
        "obligations": "Borrowed/Owned 变体及 'a 输入输出关系必须保留；From<Vec> 移动不克隆，From<&Vec>/切片/数组引用不分配。",
    },
    "partial_eq.rs": {
        "role": "__impl_slice_eq1 宏的每次调用展开 eq/ne；双 allocator、异元素类型、反向切片及 Cow 左侧均保留。",
        "depends_on": ["core::cmp::PartialEq", "core::slice", "alloc::borrow::Cow"],
        "views": ["vec_contents", "cow_variant_contents", "element_comparison"],
        "obligations": "T: PartialEq<U> 不是 Eq；不能把两个 allocator 合一；源码注释中未启用的宏调用不产生 impl。每个实际 impl 的 eq 与 ne 都是本模块显式实现。",
    },
    "peek_mut.rs": {
        "role": "整个公开 PeekMut surface 属 vec_peek_mut 不稳定功能；new 私有；保留排除清单。",
        "depends_on": ["Vec::peek_mut", "Vec::pop", "slice::get_unchecked"],
        "views": ["borrow_writeback"],
        "obligations": "独占借用最后元素及非空构造关系；当前稳定目标中排除，不声称已覆盖。",
    },
    "spec_from_elem.rs": {
        "role": "私有 SpecFromElem：Clone 通用路径、IsZero、i8/u8/() 专门路径。",
        "depends_on": ["is_zero", "Vec::extend_with", "RawVec::with_capacity_zeroed_in"],
        "views": ["vec_contents", "allocation_layout", "callback_state"],
        "obligations": "from_elem/vec![e;n] 的委托依赖；Clone 次数/副作用与末项移动不可凭纯值模型抹去；零初始化须有表示关系。",
    },
    "is_zero.rs": {
        "role": "私有 unsafe IsZero 及标量、元组、Option 宏展开；全部逐项排除为私有专门化。",
        "depends_on": ["core::mem", "SpecFromElem"],
        "views": ["zero_representation"],
        "obligations": "全零有效表示不是普遍零值定理；Option 布局/niche、ZST 与数组长度分支按源码适用；指针不实现 IsZero（provenance 注释）。",
    },
    "spec_extend.rs": {
        "role": "私有 SpecExtend：一般迭代器、TrustedLen、IntoIter 移入、借用 Clone、TrivialClone 切片。",
        "depends_on": ["Vec::extend_desugared", "Vec::extend_trusted", "Vec::append_elements", "into_iter"],
        "views": ["vec_contents", "owned_remaining", "callback_state"],
        "obligations": "各专门化共享元素顺序目标但适用界限不同；借用 Clone 与移动 T 分开；IntoIter 转移后必须不再析构已移入元素。",
    },
    "spec_from_iter.rs": {
        "role": "私有 SpecFromIter 分派；IntoIter 未推进/足够剩余时复用分配，否则 SpecExtend。",
        "depends_on": ["spec_from_iter_nested", "spec_extend", "in_place_collect", "into_iter"],
        "views": ["vec_contents", "owned_remaining", "allocation_layout"],
        "obligations": "分配复用不是稳定容量等式；一般路径与专门路径的顺序/所有权对应必须都证明。",
    },
    "spec_from_iter_nested.rs": {
        "role": "私有嵌套分派，解决 Iterator 与 TrustedLen 重叠。",
        "depends_on": ["spec_extend", "RawVec::MIN_NON_ZERO_CAP", "Vec::with_capacity"],
        "views": ["vec_contents", "callback_state", "allocation_layout"],
        "obligations": "空迭代器、预取首元素、size_hint、精确上界和超 usize::MAX 的 panic 分支分开。",
    },
    "in_place_collect.rs": {
        "role": "私有 InPlaceCollect/SpecInPlaceCollect/AsVecIntoIter 与原地收集；模块长文为不变量来源。",
        "depends_on": ["into_iter", "in_place_drop", "spec_from_iter_nested", "SourceIter", "InPlaceIterable", "Allocator::shrink"],
        "views": ["in_place_regions", "owned_remaining", "allocation_layout", "callback_state"],
        "obligations": "读取源/写入目标同分配；消费释放字节不少于写入字节；布局匹配或 shrink；未读区不可被覆盖；异常析构及 TrustedRandomAccessNoCoerce 的 NonDrop 前提不可省略。",
    },
    "in_place_drop.rs": {
        "role": "两个私有 Drop guard，分别销毁已写目标区与原源布局分配。",
        "depends_on": ["RawVec", "in_place_collect", "into_iter"],
        "views": ["in_place_regions", "allocation_layout"],
        "obligations": "用 Src 布局释放分配、以 Dest 类型析构前缀；需与原地收集状态一致，不新增抽象生命周期事件系统。",
    },
    "set_len_on_drop.rs": {
        "role": "私有长度提交 guard；源码以局部长度避免别名分析开销。",
        "depends_on": ["Vec::extend_with", "Vec::extend_trusted"],
        "views": ["initialized_prefix"],
        "obligations": "只有实际已初始化的前缀可提交到 len；Clone/迭代 panic 时 guard 仍提交正确长度。",
    },
}


def walk(node):
    yield node
    for child in node.named_children:
        yield from walk(child)


def compact(text):
    return re.sub(r"\s+", " ", text).strip()


def base_name(text):
    return text.split("<", 1)[0].strip().split("::")[-1]


def preceding(node):
    nodes = []
    prev = node.prev_named_sibling
    while prev is not None and prev.type in COMMENTS | {"attribute_item"}:
        nodes.append(prev)
        prev = prev.prev_named_sibling
    return list(reversed(nodes))


class Source:
    def __init__(self, path, raw, strict=True):
        self.path = path
        self.raw = raw
        self.adjustments = []
        normalized = bytearray(raw)
        initial = PARSER.parse(raw)
        protected = [
            (n.start_byte, n.end_byte) for n in walk(initial.root_node)
            if n.type in COMMENTS | {"string_literal", "raw_string_literal", "char_literal"}
        ]

        def replace(start, end, replacement, reason):
            assert end - start == len(replacement)
            if any(a <= start < b for a, b in protected):
                return
            normalized[start:end] = replacement
            self.adjustments.append({
                "source": self.span_bytes(start, end),
                "original": raw[start:end].decode(),
                "parser_only": replacement.decode(),
                "reason": reason,
            })

        for m in re.finditer(rb"\[const\]", raw):
            replace(m.start(), m.end(), b" " * len(m.group()), "grammar 未支持的条件 const bound；原始签名不变")
        for m in re.finditer(rb"\bconst\b(?=\s+(?:(?:unsafe\s+)?trait|impl)\b)", raw):
            replace(m.start(), m.end(), b" " * 5, "grammar 未支持的 const trait/impl 修饰；运行时稳定性独立")
        for m in re.finditer(
            rb"\bconst\b(?=\s+[A-Za-z_:][A-Za-z_0-9:]*(?:<|\s+for\b))", raw
        ):
            replace(m.start(), m.end(), b" " * 5, "grammar 未支持的 const trait impl 修饰")
        if path == "alloc/src/vec/into_iter.rs":
            m = re.search(rb"(?m)^macro non_null \{.*?^\}", raw, re.S)
            assert m, "non_null 源码形状改变，须重新检查 declarative-macro 映射"
            replace(m.start(), m.start() + 14, b"macro_rules! x", "macro 2.0 表达式宏，仅以等长 macro_rules 形状解析")
            for sep in re.finditer(rb"\}\},", m.group()):
                at = m.start() + sep.end() - 1
                replace(at, at + 1, b";", "macro 2.0 arm 分隔符，仅 parser 形状兼容")
        assert len(normalized) == len(raw)
        assert normalized.count(b"\n") == raw.count(b"\n")
        self.tree = PARSER.parse(bytes(normalized))
        self.root = self.tree.root_node
        self.errors = [
            self.span(n) for n in walk(self.root) if n.type == "ERROR" or n.is_missing
        ]
        if strict:
            assert not self.errors, (path, self.errors)

    def text(self, node):
        return self.raw[node.start_byte:node.end_byte].decode() if node else ""

    def start(self, node):
        start = node.start_byte
        if node.type == "impl_item" and self.raw[max(0, start - 6):start] == b"const ":
            start -= 6
        return start

    def span_bytes(self, start, end):
        return {
            "path": self.path,
            "start_line": self.raw.count(b"\n", 0, start) + 1,
            "end_line": self.raw.count(b"\n", 0, max(start, end - 1)) + 1,
            "start_byte": start,
            "end_byte": end,
        }

    def span(self, node):
        return self.span_bytes(self.start(node), node.end_byte)

    def attrs(self, node):
        return [
            {"text": self.text(n), "source": self.span(n)}
            for n in preceding(node) if n.type == "attribute_item"
        ]

    def header(self, node):
        body = node.child_by_field_name("body")
        end = body.start_byte if body else node.end_byte
        return self.raw[self.start(node):end].decode().strip()

    def field(self, node, name):
        return self.text(node.child_by_field_name(name))

    def macro_name(self, node):
        if self.text(node).startswith("macro non_null"):
            return "non_null"
        return self.field(node, "name") or self.field(node, "macro")


def attr_kind(attr):
    m = re.match(r"#\!?\[\s*([:\w]+)", attr["text"])
    assert m, attr
    return m.group(1)


def attr_value(attrs, names):
    return [a for a in attrs if attr_kind(a) in names]


def availability(attrs):
    relevant = attr_value(attrs, {"stable", "unstable"})
    assert len(relevant) <= 1, relevant
    if not relevant:
        return None
    a = relevant[0]
    return {
        "kind": attr_kind(a),
        **dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', a["text"])),
        "source": a["source"],
    }


def cfgs(attrs):
    return [
        a["text"][a["text"].find("(") + 1:a["text"].rfind(")")]
        for a in attrs if attr_kind(a) == "cfg"
    ]


def unique(items):
    return list(dict.fromkeys(items))


def loc(span):
    return f'{span["path"]}:{span["start_line"]}-{span["end_line"]}'


def split_commas(text):
    result, start, depth = [], 0, 0
    for i, char in enumerate(text):
        if char in "<([{":
            depth += 1
        elif char in ">)]}":
            depth -= 1
        elif char == "," and depth == 0:
            result.append(text[start:i].strip())
            start = i + 1
    assert depth == 0, text
    if text[start:].strip():
        result.append(text[start:].strip())
    return result


class Inventory:
    def __init__(self, library):
        self.library = library
        paths = sorted((library / "alloc/src/vec").rglob("*"))
        assert all(p.is_file() and p.suffix == ".rs" for p in paths), paths
        self.sources = {
            str(p.relative_to(library)): Source(str(p.relative_to(library)), p.read_bytes())
            for p in paths
        }
        assert {Path(p).name for p in self.sources} == set(MODULE_ANALYSIS), (
            "新增/删除的源文件必须补充实质依赖分析", sorted(self.sources)
        )
        self.external = {}
        self.docs = {}
        self.types = []
        self.external_types = []
        self.impls = []
        self.functions = []
        self.non_executable = []
        self.inherited = []
        self.macros = []
        self.reexports = []
        self.traits = {}
        self.local_traits = {}
        self.aliases = dict(ALIASES)
        self.accounted_functions = set()
        self.module_cfg = {"mod.rs": []}
        root = self.sources["alloc/src/vec/mod.rs"]
        for n in root.root.named_children:
            if n.type == "mod_item":
                name = root.field(n, "name")
                self.module_cfg[name + ".rs"] = cfgs(root.attrs(n))
        assert set(self.module_cfg) == {Path(p).name for p in self.sources}
        self.module_stability = availability([
            {"text": root.text(n), "source": root.span(n)}
            for n in root.root.named_children if n.type == "inner_attribute_item"
        ])
        assert self.module_stability and self.module_stability["kind"] == "stable"

    def external_source(self, path):
        if path not in self.external:
            self.external[path] = Source(path, (self.library / path).read_bytes(), strict=False)
        return self.external[path]

    def doc_refs(self, src, node, role):
        docs = [
            n for n in preceding(node)
            if n.type in COMMENTS and (
                src.text(n).startswith("///") and not src.text(n).startswith("////")
                or src.text(n).startswith("/**") and not src.text(n).startswith("/***")
            )
        ]
        if not docs:
            return []
        span = src.span_bytes(docs[0].start_byte, docs[-1].end_byte)
        key = loc(span)
        text = "\n".join(src.text(n).rstrip("\n") for n in docs)
        self.docs[key] = {"source": span, "text": text}
        return [{"role": role, "ref": key}]

    def qualify(self, text, bound_names=()):
        text = compact(text)
        text = re.sub(r"(?<![\w:])(?:ops|fmt|slice)::", lambda m: "core::" + m.group(), text)
        text = re.sub(r"\b(?:super|self)::(?=" + "|".join(PUBLIC_TYPES) + r"\b)", "", text)
        return re.sub(
            r"(?<![\w:])[A-Za-z_]\w*",
            lambda m: self.aliases.get(m.group(), m.group())
            if m.group() not in bound_names else m.group(),
            text,
        )

    def generic_names(self, src, node):
        params = node.child_by_field_name("type_parameters")
        if not params:
            return []
        return [
            src.field(n, "name") for n in params.named_children
            if n.type in {"type_parameter", "const_parameter", "lifetime_parameter"}
        ]

    def describe_trait(self, name, src, node):
        assert not node.has_error, (src.path, name, src.span(node))
        attrs = src.attrs(node)
        methods = {}
        for m in node.child_by_field_name("body").named_children:
            if m.type in FUNCTIONS:
                method_attrs = src.attrs(m)
                methods[src.field(m, "name")] = {
                    "signature": src.header(m),
                    "source": src.span(m),
                    "attributes": method_attrs,
                    "stability": availability(method_attrs) or availability(attrs),
                    "provided": m.type == "function_item",
                    "docs": self.doc_refs(src, m, "trait_member"),
                }
        return {
            "name": name, "path": self.aliases[name],
            "signature": src.header(node), "source": src.span(node),
            "attributes": attrs, "stability": availability(attrs),
            "docs": self.doc_refs(src, node, "trait"),
            "methods": methods,
        }

    def scan_types_and_traits(self):
        for src in self.sources.values():
            for n in walk(src.root):
                if n.type not in {"struct_item", "enum_item", "union_item", "trait_item"}:
                    continue
                name = src.field(n, "name")
                attrs = src.attrs(n)
                parent_function = next(
                    (p for p in self.ancestors(n) if p.type in FUNCTIONS), None
                )
                public = any(src.text(c) == "pub" for c in n.named_children
                             if c.type == "visibility_modifier")
                exported = public and name in PUBLIC_TYPES and not parent_function
                path = "alloc::vec" if src.path.endswith("/mod.rs") else (
                    "alloc::vec::" + Path(src.path).stem
                )
                canonical = f"alloc::vec::{name}" if exported else f"{path}::{name}"
                if not parent_function:
                    self.aliases[name] = canonical
                item = {
                    "name": name, "canonical": canonical,
                    "source": src.span(n), "signature": src.header(n),
                    "visibility": next(
                        (src.text(c) for c in n.named_children if c.type == "visibility_modifier"),
                        "private",
                    ),
                    "exported": exported, "local_to_function": bool(parent_function),
                    "attributes": attrs, "stability": availability(attrs),
                    "cfg": self.module_cfg[Path(src.path).name] + cfgs(attrs),
                    "docs": self.doc_refs(src, n, "type"),
                    "generic_parameter_attributes": [
                        {"text": src.text(c), "source": src.span(c)}
                        for p in n.named_children if p.type == "type_parameters"
                        for c in walk(p) if c.type == "attribute_item"
                    ],
                    "fields": [
                        {"name": src.field(f, "name"), "type": src.field(f, "type"),
                         "source": src.span(f)}
                        for b in n.named_children if b.type == "field_declaration_list"
                        for f in b.named_children if f.type == "field_declaration"
                    ],
                }
                self.types.append(item)
                if n.type == "trait_item" and not parent_function:
                    self.local_traits[name] = (src, n)
        for name, path in (("Box", "alloc/src/boxed.rs"), ("Cow", "alloc/src/borrow.rs")):
            src = self.external_source(path)
            n = next(n for n in src.root.named_children
                     if n.type in {"struct_item", "enum_item"} and src.field(n, "name") == name)
            assert not n.has_error
            self.external_types.append({
                "name": name, "canonical": ALIASES[name], "source": src.span(n),
                "signature": src.header(n), "stability": availability(src.attrs(n)),
                "docs": self.doc_refs(src, n, "external_owner_type"),
                "generic_parameter_attributes": [
                    {"text": src.text(c), "source": src.span(c)}
                    for p in n.named_children if p.type == "type_parameters"
                    for c in walk(p) if c.type == "attribute_item"
                ],
            })
        for name, (src, node) in self.local_traits.items():
            self.traits[name] = self.describe_trait(name, src, node)
        for name, path in TRAIT_FILES.items():
            src = self.external_source(path)
            nodes = [n for n in src.root.named_children
                     if n.type == "trait_item" and src.field(n, "name") == name]
            assert len(nodes) == 1, (name, path, len(nodes))
            self.traits[name] = self.describe_trait(name, src, nodes[0])

    @staticmethod
    def ancestors(node):
        node = node.parent
        while node is not None:
            yield node
            node = node.parent

    def nearest_function(self, node):
        return next((p for p in self.ancestors(node) if p.type in FUNCTIONS), None)

    def ancestor_cfg(self, src, node):
        return [
            cfg for p in self.ancestors(node)
            if p.type in FUNCTIONS | {"impl_item", "mod_item", "trait_item"}
            for cfg in cfgs(src.attrs(p))
        ]

    def private_owner(self, owner):
        owner = re.sub(r"^&\s*(?:'\w+\s+)?(?:mut\s+)?", "", owner)
        name = base_name(owner)
        return any(t["name"] == name and not t["exported"] for t in self.types)

    def type_item(self, owner):
        for name in PUBLIC_TYPES:
            if re.search(r"(?<!\w)" + name + r"\s*<", owner):
                return next(t for t in self.types if t["name"] == name and t["exported"])
        owner = re.sub(r"^&\s*(?:'\w+\s+)?(?:mut\s+)?", "", owner)
        return next((t for t in self.external_types if t["name"] == base_name(owner)), None)

    def impl_record(self, src, node, origin=None):
        attrs = src.attrs(node)
        type_text = src.field(node, "type")
        trait_text = src.field(node, "trait")
        names = self.generic_names(src, node)
        body = node.child_by_field_name("body")
        where = next((src.text(n) for n in node.named_children if n.type == "where_clause"), "")
        local = self.nearest_function(node)
        source = origin["invocation"] if origin else src.span(node)
        record = {
            "id": f"{loc(source)}::{compact(src.header(node))}",
            "source": source, "header": src.header(node), "owner": type_text,
            "canonical_owner": self.qualify(type_text, names),
            "trait": trait_text, "canonical_trait": self.qualify(trait_text, names),
            "generic_parameters": src.field(node, "type_parameters"),
            "where_clause": where, "attributes": attrs,
            "stability": availability(attrs),
            "cfg": unique(self.module_cfg[Path(source["path"]).name]
                          + self.ancestor_cfg(src, node) + cfgs(attrs)),
            "docs": [] if origin else self.doc_refs(src, node, "impl"),
            "associated_items": [
                {"kind": n.type, "text": src.text(n),
                 "source": source if origin else src.span(n)}
                for n in body.named_children if n.type in {"type_item", "const_item"}
            ],
            "methods": [],
            "local_to_function": src.field(local, "name") if local else None,
            "origin": origin or {"kind": "source"},
        }
        if origin:
            record["attributes"] = origin.get("inherited_attributes", []) + attrs
            record["cfg"] = unique(record["cfg"] + cfgs(origin.get("inherited_attributes", [])))
            for a in record["attributes"]:
                if a["source"]["path"].startswith("<"):
                    a["source"] = origin["invocation"]
            record["stability"] = availability(record["attributes"])
        self.impls.append(record)
        for m in body.named_children:
            if m.type in FUNCTIONS:
                rec = self.function_record(src, m, record, origin)
                record["methods"].append(rec["inventory_id"])
        if not record["methods"]:
            self.non_executable.append({
                "kind": "impl_without_executable_body",
                "source": source, "impl": record["id"],
                "reason": "空 impl / 仅关联类型或常量，不是可执行方法；默认 trait 方法另列。",
            })
        return record

    def lifetime_info(self, src, node, impl):
        params = node.child_by_field_name("parameters")
        ret = node.child_by_field_name("return_type")
        self_node = next((n for n in params.named_children if n.type == "self_parameter"), None)
        receiver_text = src.text(self_node) if self_node else ""
        if not self_node:
            kind = "none"
        elif "&" in receiver_text:
            kind = "mutable_borrow" if "mut" in receiver_text else "shared_borrow"
        else:
            kind = "by_value"
        receiver = {
            "kind": kind, "source": receiver_text,
            "binding_mutable": receiver_text.startswith("mut "),
            "reference_mutable": kind == "mutable_borrow",
            "owner_type": impl["owner"] if impl else None,
        }
        inputs = []
        for param in params.named_children:
            if param.type == "parameter":
                inputs.append({
                    "pattern": src.field(param, "pattern"),
                    "type": src.field(param, "type"),
                })
        return_text = src.text(ret)
        lifetimes = unique(re.findall(
            r"'(?:[A-Za-z_]\w*)",
            (impl["header"] if impl else "") + " " + src.header(node),
        ))
        if ret and ret.type == "pointer_type":
            relation = "裸指针无签名编码的 outlives 关系；有效期、aliasing 与内容按自身 safety/doc 约束。"
        elif kind in {"shared_borrow", "mutable_borrow"} and (
            "&" in return_text or "'_" in return_text
        ):
            relation = "返回类型的省略引用生命周期/'_ 绑定本次 receiver 借用；不是直接放宽到类型内部 'a；显式同名生命周期仍按签名。"
        elif lifetimes:
            relation = "显式同名生命周期按 impl/方法/参数/返回类型及关联类型保持；匿名 '_ 独立推断，不改为 'static。"
        else:
            relation = "无额外命名借用生命周期关系；泛型内可能含借用，不添加 Copy/Eq/'static。"
        if src.field(node, "name") == "leak" and impl and base_name(impl["owner"]) == "Vec":
            relation = "消耗 Vec；调用者选择返回 'a；显式 A:'a，&'a mut [T] 的良构要求 T:'a；不得强制 'static，底层分配泄漏。"
        return receiver, {
            "named_and_placeholder_lifetimes": lifetimes,
            "inputs": inputs, "return_type": return_text or "()",
            "relation": relation,
            "associated_items": impl["associated_items"] if impl else [],
        }

    def function_record(self, src, node, impl=None, origin=None):
        name = src.field(node, "name")
        attrs = src.attrs(node)
        source = origin["invocation"] if origin else src.span(node)
        if origin:
            for a in attrs:
                a["source"] = source
        parent_function = self.nearest_function(node)
        enclosing_trait = next((p for p in self.ancestors(node) if p.type == "trait_item"), None)
        source_module = "alloc::vec" if source["path"].endswith("/mod.rs") else (
            "alloc::vec::" + Path(source["path"]).stem
        )
        owner = impl["owner"] if impl else (
            src.field(enclosing_trait, "name") if enclosing_trait else source_module
        )
        trait = impl["trait"] if impl else ""
        names = self.generic_names(src, node)
        if impl:
            names += re.findall(r"(?<!\w)([A-Z]\w*)\s*[:,>]", impl["generic_parameters"])
        canonical_owner = impl["canonical_owner"] if impl else (
            self.aliases.get(owner, f"{source_module}::{owner}") if enclosing_trait else source_module
        )
        canonical = (
            f'<{canonical_owner} as {impl["canonical_trait"]}>::{name}'
            if trait else f"{canonical_owner}::{name}"
        )
        if parent_function:
            canonical += f' [local in {src.field(parent_function, "name")}]'
        trait_name = base_name(trait)
        trait_def = self.traits.get(trait_name)
        member = trait_def["methods"].get(name) if trait_def else None
        if trait and trait_name not in self.local_traits and not parent_function:
            assert trait_def is not None and member is not None, (trait, name, source)
        type_def = self.type_item(owner)
        own = availability(attrs)
        inherited = impl["stability"] if impl else None
        declared = own or inherited or (type_def["stability"] if type_def else None) or self.module_stability
        gates = [
            {"role": role, **a} for role, a in (
                ("method", own), ("impl", inherited),
                ("owner_type", type_def["stability"] if type_def else None),
                ("trait_member", member["stability"] if member else None),
                ("trait", trait_def["stability"] if trait_def else None),
            ) if a
        ]
        unstable = [g for g in gates if g["kind"] == "unstable"]
        visible = any(src.text(n) == "pub" for n in node.named_children
                      if n.type == "visibility_modifier") or bool(trait)
        local_owner = impl and impl["local_to_function"]
        private_trait = trait_name in self.local_traits
        if parent_function or local_owner:
            status, reason = "excluded", "local_helper"
        elif node.type == "function_signature_item" and not origin:
            status, reason = "excluded", "trait_declaration_not_implementation"
        elif private_trait:
            status, reason = "excluded", "private_specialization_trait"
        elif impl and self.private_owner(owner):
            status, reason = "excluded", "private_owner"
        elif not visible:
            status, reason = "excluded", "non_public_function"
        elif unstable:
            status, reason = "excluded", "unstable_api"
        else:
            assert declared and declared["kind"] == "stable", (canonical, declared)
            status, reason = "included", None
        docs = [] if origin else self.doc_refs(src, node, "method")
        if impl:
            docs += impl["docs"]
        if member:
            docs += member["docs"]
            docs += trait_def["docs"]
        receiver, lifetimes = self.lifetime_info(src, node, impl)
        where = next((src.text(n) for n in node.named_children if n.type == "where_clause"), "")
        inventory_id = canonical if status == "included" else f"{canonical} @ {loc(source)}"
        if origin and status != "included":
            inventory_id += " " + compact(impl["header"])
        const_attrs = attr_value(attrs + (impl["attributes"] if impl else []),
                                 {"rustc_const_stable", "rustc_const_unstable"})
        record = {
            "inventory_id": inventory_id, "canonical_id": canonical,
            "status": status, "exclusion_reason": reason,
            "source_module": Path(source["path"]).stem,
            "source_owner": owner, "canonical_owner": canonical_owner,
            "trait": trait, "canonical_trait": impl["canonical_trait"] if impl else "",
            "method": name, "signature": src.header(node),
            "impl_header": impl["header"] if impl else None,
            "impl_generic_parameters": impl["generic_parameters"] if impl else "",
            "impl_where_clause": impl["where_clause"] if impl else "",
            "trait_declaration_context": src.header(enclosing_trait) if enclosing_trait else None,
            "enclosing_function": {
                "source": src.span(parent_function), "signature": src.header(parent_function),
            } if parent_function else None,
            "method_generic_parameters": src.field(node, "type_parameters"),
            "method_where_clause": where, "receiver": receiver,
            "lifetime_relation": lifetimes,
            "associated_items": impl["associated_items"] if impl else [],
            "source": source,
            "signature_source": source if origin else src.span_bytes(
                node.start_byte, node.child_by_field_name("body").start_byte
                if node.child_by_field_name("body") else node.end_byte
            ),
            "docs": docs,
            "documentation_note": (
                "无该方法自身 docstring；trait/impl 文档适用（若 refs 非空），行为仍须读 body。"
                if not any(d["role"] == "method" for d in docs) else None
            ),
            "cfg": unique((impl["cfg"] if impl else self.module_cfg[Path(source["path"]).name])
                          + self.ancestor_cfg(src, node) + cfgs(attrs)),
            "attributes": attrs,
            "stability": {"effective": "unstable" if unstable else declared["kind"],
                          "effective_since": None if unstable else max(
                              [g.get("since", "0.0.0") for g in gates if g["kind"] == "stable"]
                              + [declared.get("since", "0.0.0")],
                              key=lambda v: tuple(int(x) for x in v.split(".")),
                          ),
                          "declared_or_inherited": declared, "gates": gates},
            "const_stability": const_attrs,
            "owner_generic_parameter_attributes": type_def["generic_parameter_attributes"] if type_def else [],
            "owner_definition": type_def["source"] if type_def else None,
            "owner_docs": type_def["docs"] if type_def else [],
            "origin": origin or {"kind": "source"},
            "direct_calls": [],
            "existing_vstd_coverage": "unassessed_official_baseline_pending",
        }
        body = node.child_by_field_name("body")
        if body:
            for call in walk(body):
                if call.type == "call_expression" and self.nearest_function(call) == node:
                    record["direct_calls"].append({
                        "callee_syntax": src.field(call, "function"),
                        "source": source if origin else src.span(call),
                    })
        if name == "from_elem" and not impl and source["path"] == "alloc/src/vec/mod.rs":
            caller = self.external_source("alloc/src/macros.rs")
            vec_macro = next(n for n in caller.root.named_children
                             if n.type == "macro_definition" and caller.macro_name(n) == "vec")
            record["docs"] += self.doc_refs(caller, vec_macro, "caller_macro_not_own_docstring")
            record["documentation_note"] = "自身没有 docstring；关联 vec![elem;n] 的真实调用者宏文档，不能将宏名称另算 vec 内 API。"
        self.functions.append(record)
        if not origin:
            self.accounted_functions.add((src.path, node.start_byte, node.end_byte))
        return record

    def expand_impl(self, text, origin):
        generated = Source("<macro-expansion>", text.encode())
        impls = [n for n in generated.root.named_children if n.type == "impl_item"]
        assert len(impls) == 1, text
        return self.impl_record(generated, impls[0], origin)

    def expand_item_macro(self, src, node, definitions):
        name = src.macro_name(node)
        definition = definitions[name]
        rule = next(n for n in definition.named_children if n.type == "macro_rule")
        template_node = rule.child_by_field_name("right")
        assert template_node is not None, (name, str(rule))
        template = src.text(template_node)[1:-1]
        args_node = next(n for n in node.named_children if n.type == "token_tree")
        args = src.text(args_node)[1:-1].strip()
        origin = {
            "kind": "macro_expansion", "macro": name,
            "invocation": src.span(node), "definition": src.span(definition),
            "template": src.span(template_node),
            "inherited_attributes": src.attrs(node),
        }
        expansions = []
        if name == "__impl_slice_eq1":
            assert args.startswith("[")
            end = args.index("]")
            variables = args[1:end].strip()
            rest = args[end + 1:].strip()
            lhs, rhs_and_where, stability = split_commas(rest)
            rhs, sep, bounds = rhs_and_where.partition(" where ")
            assert stability.startswith("#[") and stability.endswith("]")
            optional = bounds.strip() if sep else ""
            expanded = template.replace("$($vars)*", variables)
            expanded = expanded.replace("$($ty: $bound)?", optional)
            expanded = expanded.replace("$stability", stability[2:-1])
            expanded = expanded.replace("$rhs", rhs).replace("$lhs", lhs)
            expansions.append(expanded)
        elif name == "impl_is_zero":
            at = args.index(",")
            t, expr = args[:at].strip(), args[at + 1:].strip()
            expansions.append(template.replace("$is_zero", expr).replace("$t", t))
        elif name == "impl_is_zero_tuples":
            rules = [n for n in definition.named_children if n.type == "macro_rule"]
            assert len(rules) == 2
            template_node = rules[1].child_by_field_name("right")
            template = src.text(template_node)[1:-1]
            origin["template"] = src.span(template_node)
            variables = split_commas(args)
            for i in range(len(variables)):
                first, rest = variables[i], variables[i + 1:]
                expanded = template.replace("impl_is_zero_tuples!($($rest),*);", "")
                expanded = expanded.replace("$($rest: IsZero,)*", "".join(f"{v}: IsZero," for v in rest))
                expanded = expanded.replace("$($rest,)*", "".join(f"{v}," for v in rest))
                expanded = expanded.replace("$( && $rest.is_zero() )*", "".join(f" && {v}.is_zero()" for v in rest))
                expanded = expanded.replace("$first_arg", first)
                expansions.append(expanded)
        elif name in {
            "impl_is_zero_option_of_nonzero_int",
            "impl_is_zero_option_of_int", "impl_is_zero_option_of_bool",
        }:
            begin, end = template.index("$(") + 2, template.rindex(")+")
            repeated = template[begin:end]
            args_without_comments = re.sub(r"//[^\n]*", "", args)
            expansions.extend(repeated.replace("$t", t) for t in split_commas(args_without_comments))
        else:
            raise AssertionError(("未分类的 item macro", name, src.span(node)))
        for expanded in expansions:
            assert "$" not in expanded, (name, expanded)
            self.expand_impl(expanded, origin)
        return len(expansions)

    def expand_debug(self, src, node):
        name = src.field(node, "name")
        attrs = src.attrs(node)
        derives = attr_value(attrs, {"derive"})
        if not derives:
            return
        assert name == "Splice" and len(derives) == 1 and derives[0]["text"] == "#[derive(Debug)]"
        assert compact(src.field(node, "type_parameters")) == (
            "< 'a, I: Iterator + 'a, #[unstable(feature = \"allocator_api\", issue = \"32838\")] A: Allocator + 'a = Global, >"
        )
        origin = {
            "kind": "builtin_derive", "macro": "Debug",
            "invocation": derives[0]["source"], "type_source": src.span(node),
            "inherited_attributes": attr_value(attrs, {"stable", "unstable", "cfg"}),
            "note": "仅展开 canonical impl/header/method；非手写替代 body。I/A 的 Debug bound 与 I::Item 投影 bound 保留；独立 derive 形状测试见 source-tests。",
        }
        text = """impl<'a, I: core::fmt::Debug + Iterator + 'a,
            A: core::fmt::Debug + Allocator + 'a> core::fmt::Debug for Splice<'a, I, A>
            where I::Item: core::fmt::Debug {
                fn fmt(&self, f: &mut core::fmt::Formatter) -> core::fmt::Result;
            }"""
        self.expand_impl(text, origin)

    def scan_items(self):
        for src in self.sources.values():
            definitions = {src.macro_name(n): n for n in src.root.named_children
                           if n.type == "macro_definition"}
            all_nodes = list(walk(src.root))
            for n in all_nodes:
                if n.type == "impl_item":
                    self.impl_record(src, n)
                elif n.type in FUNCTIONS:
                    parent = n.parent
                    if parent and parent.type == "declaration_list" and parent.parent.type == "impl_item":
                        continue
                    self.function_record(src, n)
                elif n.type == "struct_item":
                    self.expand_debug(src, n)
                elif n.type == "use_declaration":
                    if any(c.type == "visibility_modifier" for c in n.named_children):
                        self.reexports.append({
                            "source": src.span(n), "text": src.text(n),
                            "attributes": src.attrs(n), "cfg": cfgs(src.attrs(n)),
                            "reason": "绑定/镜像，不新增 executable API；所有者采用实际定义/impl 所在文件。",
                        })
                elif n.type == "macro_invocation":
                    item = n.parent.type in {"source_file", "declaration_list"} or (
                        n.parent.type == "expression_statement" and n.parent.parent.type == "source_file"
                    )
                    macro = {
                        "name": src.macro_name(n), "source": src.span(n),
                        "context": "item" if item else "body_expression",
                        "generated_impls": 0,
                    }
                    if item:
                        assert macro["name"] in definitions, macro
                        macro["generated_impls"] = self.expand_item_macro(src, n, definitions)
                    else:
                        macro["reason"] = "表达式/检查宏，不另计 public executable 方法。"
                    self.macros.append(macro)
            for n in all_nodes:
                if n.type in {"type_item", "associated_type", "const_item", "static_item",
                              "mod_item", "macro_definition", "trait_item", "struct_item"}:
                    self.non_executable.append({
                        "kind": n.type, "source": src.span(n),
                        "reason": "类型/关联项/模块/宏定义不是独立可执行方法；函数与宏展开另列。",
                    })
            for n in src.root.named_children:
                assert n.type in DECLARATIONS | COMMENTS | {
                    "attribute_item", "inner_attribute_item", "expression_statement",
                    "macro_invocation",
                }, (src.path, n.type, src.span(n))
        self.add_inherited()

    def add_inherited(self):
        for impl in self.impls:
            trait_name = base_name(impl["trait"])
            if not impl["trait"] or trait_name in self.local_traits or impl["local_to_function"]:
                continue
            trait = self.traits.get(trait_name)
            if not trait:
                assert not impl["methods"], impl
                continue
            own_names = {
                f["method"] for f in self.functions if f["inventory_id"] in impl["methods"]
            }
            for name, member in trait["methods"].items():
                if name not in own_names:
                    assert member["provided"], (impl["id"], name)
                    self.inherited.append({
                        "canonical_id": f'<{impl["canonical_owner"]} as {impl["canonical_trait"]}>::{name}',
                        "owner": impl["canonical_owner"], "trait": impl["canonical_trait"],
                        "impl_source": impl["source"], "impl_header": impl["header"],
                        "cfg": impl["cfg"], "method": name, **member,
                        "status": "excluded", "reason": "external_trait_default_not_module_implementation",
                    })

    def external_boundaries(self):
        selections = {
            "core/src/convert/mod.rs": lambda owner, trait: (
                (owner == "T" and base_name(trait) in {"Into", "TryInto", "TryFrom", "From"})
                or (owner in {"&T", "&mut T"} and base_name(trait) in {"AsRef", "AsMut"})
            ),
            "core/src/borrow.rs": lambda owner, trait: owner in {"T", "&T", "&mut T"},
            "alloc/src/borrow.rs": lambda owner, trait: owner == "T" and trait == "ToOwned",
            "core/src/iter/traits/collect.rs": lambda owner, trait: owner == "I" and trait == "IntoIterator",
            "core/src/iter/traits/iterator.rs": lambda owner, trait: owner == "&mut I" and trait == "Iterator",
            "core/src/iter/traits/double_ended.rs": lambda owner, trait: owner == "&'a mut I" and trait == "DoubleEndedIterator",
            "core/src/iter/traits/exact_size.rs": lambda owner, trait: owner == "&mut I" and trait == "ExactSizeIterator",
            "core/src/any.rs": lambda owner, trait: owner == "T" and trait == "Any",
            "alloc/src/slice.rs": lambda owner, trait: owner == "Vec<T, A>" and base_name(trait) in {"Borrow", "BorrowMut"},
        }
        result = []
        for path, select in selections.items():
            src = self.external_source(path)
            for n in src.root.named_children:
                if n.type != "impl_item":
                    continue
                owner, trait = src.field(n, "type"), src.field(n, "trait")
                if not select(owner, trait):
                    continue
                assert not n.has_error, (path, src.span(n))
                attrs = src.attrs(n)
                reservation = bool(attr_value(attrs, {"rustc_reservation_impl"}))
                result.append({
                    "source": src.span(n), "header": src.header(n),
                    "attributes": attrs, "docs": self.doc_refs(src, n, "external_impl"),
                    "methods": [
                        {"name": src.field(m, "name"), "signature": src.header(m),
                         "source": src.span(m), "docs": self.doc_refs(src, m, "external_method")}
                        for m in n.child_by_field_name("body").named_children if m.type in FUNCTIONS
                    ],
                    "reason": (
                        "reservation_impl_not_available" if reservation else
                        "external_concrete_impl" if path == "alloc/src/slice.rs" else
                        "external_blanket_impl_family"
                    ),
                    "status": "excluded",
                })
        return result

    def dependency_sources(self):
        targets = {
            "alloc/src/raw_vec/mod.rs": {
                "types": {"RawVec", "RawVecInner"},
                "functions": {
                    "new", "new_in", "with_capacity_in", "try_with_capacity_in",
                    "with_capacity_zeroed_in", "into_box", "from_raw_parts_in",
                    "from_nonnull_in", "ptr", "non_null", "capacity", "allocator",
                    "reserve", "try_reserve", "reserve_exact", "try_reserve_exact",
                    "grow_one", "shrink_to_fit", "try_shrink_to_fit", "drop",
                },
                "owner": "RawVec",
                "relation": "Vec/IntoIter 的分配、capacity、指针与释放表示；RawVec 不析构 T。",
            },
            "alloc/src/slice.rs": {
                "types": {"SpecCloneIntoVec"},
                "functions": {"to_vec", "to_vec_in", "into_vec", "clone_into"},
                "relation": "Vec Clone/From 借用数据/Box 转移的委托及 Clone/TrivialClone 专门化。",
            },
            "core/src/slice/raw.rs": {
                "functions": {"from_raw_parts", "from_raw_parts_mut"},
                "relation": "原始指针到借用内容：单分配、对齐、初始化、长度界与共享/独占访问要求。",
            },
            "core/src/slice/index.rs": {
                "functions": {"range", "into_slice_range"},
                "relation": "drain/extract_if/extend_from_within 的 RangeBounds 正规化与 panic 边界。",
            },
            "alloc/src/borrow.rs": {
                "types": {"Cow"}, "functions": {"into_owned", "deref"},
                "owner": "Cow",
                "relation": "Cow 变体与 Borrowed/Owned 内容及借用/移动关系。",
            },
            "alloc/src/boxed.rs": {
                "types": {"Box"}, "functions": {"into_raw_with_allocator"},
                "relation": "Box<[T],A> 与 Vec<T,A> 的同分配所有权转换及 allocator 泛型。",
            },
            "core/src/alloc/mod.rs": {
                "types": {"Allocator"},
                "functions": {"allocate", "allocate_zeroed", "deallocate", "grow", "grow_zeroed", "shrink"},
                "trait_only": "Allocator",
                "relation": "RawVec 与原地收集的 fitting layout、分配失败、grow/shrink 安全前提。",
            },
            "core/src/slice/cmp.rs": {
                "functions": {"eq", "partial_cmp", "cmp"}, "owner": "[T]",
                "relation": "Vec/切片/Cow 比较委托；异元素 PartialEq 与字典序观察，不改为 Eq。",
            },
            "core/src/hash/mod.rs": {
                "functions": {"hash"}, "owner": "[T]",
                "relation": "Vec::hash 委托到对应切片的 Hash；保留 Hasher 状态和调用协议。",
            },
            "core/src/fmt/mod.rs": {
                "functions": {"fmt"}, "owner": "[T]",
                "relation": "Vec::fmt 的切片格式化委托；Formatter 状态/错误不是纯字符串假设。",
            },
        }
        result = []
        for path, select in targets.items():
            src = self.external_source(path)
            selected = []
            for n in walk(src.root):
                name = src.field(n, "name")
                is_type = n.type in {"struct_item", "enum_item", "trait_item"}
                is_function = n.type in FUNCTIONS
                if is_type and name in select.get("types", set()):
                    pass
                elif is_function and name in select["functions"]:
                    impl = next((p for p in self.ancestors(n) if p.type == "impl_item"), None)
                    trait = next((p for p in self.ancestors(n) if p.type == "trait_item"), None)
                    owner = src.field(impl, "type") if impl else ""
                    if "owner" in select and base_name(owner) != select["owner"]:
                        continue
                    if "trait_only" in select and (
                        not trait or src.field(trait, "name") != select["trait_only"]
                    ):
                        continue
                else:
                    continue
                assert not n.has_error, (path, name, src.span(n))
                impl = next((p for p in self.ancestors(n) if p.type == "impl_item"), None)
                selected.append({
                    "kind": n.type, "name": name, "source": src.span(n),
                    "signature": src.header(n),
                    "impl_header": src.header(impl) if impl else None,
                    "attributes": src.attrs(n),
                    "docs": self.doc_refs(src, n, "dependency"),
                })
            assert selected, (path, select)
            result.append({
                "path": path, "relation": select["relation"], "items": selected,
                "scope": "仅链接所需源码依赖，不纳入 vec 公共 executable 数，也不是相邻模块覆盖声明。",
            })
        return result

    def verify(self):
        expected = {
            (src.path, n.start_byte, n.end_byte)
            for src in self.sources.values() for n in walk(src.root) if n.type in FUNCTIONS
        }
        assert expected == self.accounted_functions, (
            "函数 AST 分区不完整", expected - self.accounted_functions,
            self.accounted_functions - expected,
        )
        ids = [f["inventory_id"] for f in self.functions]
        assert len(ids) == len(set(ids)), [x for x, n in Counter(ids).items() if n > 1]
        stable = [f for f in self.functions if f["status"] == "included"]
        canonical = [f["canonical_id"] for f in stable]
        assert len(canonical) == len(set(canonical))
        for f in stable:
            assert f["stability"]["effective"] == "stable", f["canonical_id"]
            assert f["source"]["path"] in self.sources
            assert f["method"] in f["signature"]
            for d in f["docs"]:
                assert d["ref"] in self.docs
        assert len([f for f in stable if f["source_module"] == "partial_eq"]) == (
            2 * len([m for m in self.macros if m["name"] == "__impl_slice_eq1"])
        )
        for name in ("AsRef", "AsMut"):
            targets = [f["trait"] for f in stable if f["source_owner"] == "Vec<T, A>"
                       and base_name(f["trait"]) == name]
            assert set(targets) == {f"{name}<Vec<T, A>>", f"{name}<[T]>"}, targets
        for f in self.functions:
            if f["method"] in {"advance_by", "advance_back_by", "next_chunk",
                               "__iterator_get_unchecked", "extend_one", "extend_reserve",
                               "extend_one_unchecked"} or (
                f["method"] == "is_empty" and f["trait"] == "ExactSizeIterator"
            ):
                assert f["status"] == "excluded" and f["exclusion_reason"] == "unstable_api", f
        push = next(f for f in stable if f["method"] == "push")
        assert "A: [const] Allocator + [const] Destruct" in push["impl_header"]
        assert push["source_owner"] == "Vec<T, A>"
        assert any(f["method"] == "from_elem" and not f["trait"] for f in stable)
        assert any(f["origin"]["kind"] == "builtin_derive" for f in stable)
        assert any(f["method"] == "try_fold" for f in stable)
        assert all(f["source_module"] != "peek_mut" for f in stable)
        assert all(f["source_module"] not in {
            "in_place_drop", "set_len_on_drop", "spec_from_elem", "spec_from_iter",
            "spec_from_iter_nested", "spec_extend", "in_place_collect", "is_zero",
        } for f in stable)
        assert all("core::core::" not in f["canonical_id"] for f in self.functions)
        assert all(i["reason"] == "external_trait_default_not_module_implementation"
                   for i in self.inherited)

    def build(self):
        self.scan_types_and_traits()
        self.scan_items()
        external_boundaries = self.external_boundaries()
        dependencies = self.dependency_sources()
        self.verify()
        self.functions.sort(key=lambda f: (
            f["source"]["path"], f["source"]["start_byte"], f["inventory_id"]
        ))
        included = [f for f in self.functions if f["status"] == "included"]
        excluded = [f for f in self.functions if f["status"] == "excluded"]
        files = []
        for path, src in sorted(self.sources.items()):
            declarations = [n for n in walk(src.root) if n.type in DECLARATIONS]
            file_functions = [f for f in self.functions if f["source"]["path"] == path]
            inner_docs = [n for n in src.root.named_children if n.type in COMMENTS
                          and src.text(n).startswith("//!")]
            module_docs = []
            if inner_docs:
                span = src.span_bytes(inner_docs[0].start_byte, inner_docs[-1].end_byte)
                key = loc(span)
                self.docs[key] = {
                    "source": span,
                    "text": "\n".join(src.text(n).rstrip("\n") for n in inner_docs),
                }
                module_docs = [{"role": "module", "ref": key}]
            files.append({
                "path": path, "lines": len(src.raw.splitlines()), "bytes": len(src.raw),
                "module_cfg": self.module_cfg[Path(path).name],
                "module_docs": module_docs,
                "ast_declarations": dict(sorted(Counter(n.type for n in declarations).items())),
                "declaration_spans": [{"kind": n.type, "source": src.span(n)} for n in declarations],
                "included_executable": sum(f["status"] == "included" for f in file_functions),
                "excluded_function_candidates": sum(f["status"] == "excluded" for f in file_functions),
                "parse_errors": src.errors, "parser_only_adjustments": src.adjustments,
                "analysis": MODULE_ANALYSIS[Path(path).name],
            })
        return {
            "source_library": str(self.library),
            "scope": {
                "definition": "alloc/src/vec 全部文件中实际定义的稳定 public executable 方法/自由函数；包含宏/derive 生成项及外部 owner 的本模块 impl。",
                "cfg_policy": "保留所有源码 cfg 条件，不按当前机器裁剪；not(no_global_oom_handling) 条件项仍在清单。",
                "stability_policy": "runtime API 与 const 稳定性分开；impl 属性继承、trait 成员门控都检查；allocator 泛型及其属性保留，不替换为 Global。",
                "excluded_policy": "不稳定、私有专门化、局部 helper、trait 声明、非 executable 项、默认/blanket/模块外 impl 分列；doc(hidden) 本身不排除稳定公开函数。",
                "canonical_policy": "带完整 owner 与 trait 实参的 UFCS 身份；源码泛型名称保留。reexport/std 镜像不另计；Drop 是生命周期执行入口，计入而不声称可以显式调用。",
                "vstd": "未读取或借用旧 vstd/spec/proof/count；existing-vstd coverage 留待父任务对官方固定基线比对。",
                "proof_baseline": "release/0.2026.09.20.aef82ed / Rust 1.98.1（父任务负责）；本清单不是任何 API 的证明通过记录。",
            },
            "counts": {
                "source_files": len(files),
                "stable_public_executable": len(included),
                "source_function_candidates_including_macro_derive": len(self.functions),
                "excluded_function_candidates": len(excluded),
                "excluded_by_reason": dict(sorted(Counter(f["exclusion_reason"] for f in excluded).items())),
                "inherited_trait_default_instances": len(self.inherited),
                "external_impl_families_or_boundaries": len(external_boundaries),
                "by_source_file": {
                    Path(f["path"]).name: f["included_executable"] for f in files
                },
            },
            "source_files": files,
            "apis": included, "excluded_functions": excluded,
            "types": self.types, "external_owner_types": self.external_types,
            "impls": self.impls,
            "non_executable_items": self.non_executable,
            "reexports": self.reexports, "macro_sites": self.macros,
            "inherited_trait_methods": self.inherited,
            "external_impl_boundaries": external_boundaries,
            "dependency_sources": dependencies,
            "trait_declarations": self.traits,
            "docstrings": dict(sorted(self.docs.items())),
            "checks": [
                "vec 全文件集合 == mod.rs 模块声明集合 == 实质依赖分析集合",
                "vec AST 零 ERROR/缺失节点；等长 parser-only 兼容保持原始字节/行号",
                "每个原始 function_item/function_signature_item 恰好分类一次（含嵌套 helper）",
                "所有 item macro 必须识别并展开；公开 PartialEq 每调用恰好 eq/ne 两项",
                "canonical stable API 与候选 inventory_id 均无重复",
                "AsRef/AsMut 两个目标、allocator/const bound、doc(hidden) from_elem、derive(Debug) 保留",
                "稳定 impl 中不稳定 trait 成员排除；try_fold 不因 Try bound 而排除",
            ],
        }


def render_tsv(data):
    output = io.StringIO()
    fields = [
        "status", "canonical_id", "source_owner", "trait", "method", "impl_generic_parameters",
        "impl_where_clause", "signature", "receiver", "lifetime_relation", "stability",
        "const_stability", "cfg", "source", "docs", "exclusion_reason", "origin",
    ]
    writer = csv.DictWriter(output, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for f in sorted(data["apis"] + data["excluded_functions"], key=lambda f: (
        f["source"]["path"], f["source"]["start_byte"], f["inventory_id"]
    )):
        row = {k: f.get(k, "") for k in fields}
        row["source"] = loc(f["source"])
        row["docs"] = "; ".join(d["role"] + "=" + d["ref"] for d in f["docs"])
        row["receiver"] = json.dumps(f["receiver"], ensure_ascii=False, sort_keys=True)
        row["lifetime_relation"] = json.dumps(f["lifetime_relation"], ensure_ascii=False, sort_keys=True)
        row["stability"] = json.dumps(f["stability"], ensure_ascii=False, sort_keys=True)
        row["const_stability"] = "; ".join(a["text"] for a in f["const_stability"])
        row["cfg"] = " && ".join(f["cfg"])
        row["origin"] = f["origin"]["kind"]
        writer.writerow({k: compact(str(v)) if v is not None else "" for k, v in row.items()})
    return output.getvalue()


def render_markdown(data):
    counts = data["counts"]
    lines = [
        "# alloc::vec 源码清单与依赖图", "",
        "## 边界与复跑", "",
        f"- 权威语义输入：`{data['source_library']}/alloc/src/vec`；仅为必要的 trait 文档、稳定性和委托边界读取相邻 alloc/core。",
        "- JSON 是完整记录；TSV 是本模块函数候选表，必须筛选 `status=included`，不能把排除行当作目标。",
        "- 清单由 Rust AST 生成，不用 `pub fn` 正则计数。原源码、字节位置、generic/bounds、receiver、生命周期、cfg、docstring 与稳定性属性保留。",
        "- parser 所需 grammar 缺失已经由实际 import 失败确认，再仅局部安装 `tree-sitter-rust==0.24.0`；宿主 `tree-sitter==0.25.2`。依赖固定在 `inventory/source-tests/requirements.txt`。",
        "- grammar 不支持的 `const impl`、条件 `[const]`、`macro non_null` 仅在内存解析副本做等长替换；JSON 逐项记录，不改源文件或可执行证明副本。",
        "- 核心 trait 只使用无错误的指定 AST 节点；相邻 core 文件中无关内建 derive-macro stub 不纳入 vec 的文件计数。",
        "- 未评估任何 existing-vstd coverage。官方证明基线由父任务提供：`release/0.2026.09.20.aef82ed` / Rust `1.98.1`。这里没有正确性/完整性证明通过声明。",
        "",
        "```sh",
        "PYTHONDONTWRITEBYTECODE=1 python scripts/inventory_source.py",
        "PYTHONDONTWRITEBYTECODE=1 python scripts/inventory_source.py --check",
        "PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s inventory/source-tests -p 'test_*.py'",
        "```", "",
        f"共 **{counts['source_files']} 个 vec 源文件，{counts['stable_public_executable']} 个源码所有的稳定公开 executable 条目**；"
        f"另有 {counts['excluded_function_candidates']} 个排除函数候选，"
        f"{counts['inherited_trait_default_instances']} 个 trait 默认方法实例单列。",
        "",
        "## 每个源文件（没有零目标文件被隐藏）", "",
        "| 文件 | 稳定 executable | 排除函数候选 | 实际职责 |",
        "|---|---:|---:|---|",
    ]
    for f in data["source_files"]:
        lines.append(
            f"| `{Path(f['path']).name}` | {f['included_executable']} | "
            f"{f['excluded_function_candidates']} | {f['analysis']['role']} |"
        )
    lines += ["", "## 类型、表示与必须先连接的观察", ""]
    type_notes = {
        "Vec": "buf: RawVec<T,A> + len；Seq 只描述初始化前缀，capacity/layout/allocator 与 spare 独立。省略 A 的源码 impl 维持默认分配器，显式 A 的 impl 绝不收窄。",
        "IntoIter": "buf/cap/alloc 持有原分配，ptr/end 表示 remaining；ZST 用 end 字节差；构造/消费者/借用必须共享状态关系。",
        "Drain": "tail_start/tail_len/iter/vec；与源 Vec 的 head/removed/tail 分区连接，析构复原不能由 final 自动假设。",
        "Splice": "drain + replace_with；复用 Drain 视图并附替换迭代器状态；Debug derive 的 I:Debug、A:Debug、I::Item:Debug 均保留。",
        "ExtractIf": "vec/idx/end/del/old_len/pred；已保留区、空洞、未检查区、范围外尾部及可变闭包状态一起连接。",
        "PeekMut": "vec 的末项独占借用包装；类型/方法当前均不稳定，只有表示分析，不列为稳定目标。",
    }
    for name, note in type_notes.items():
        item = next(t for t in data["types"] if t["name"] == name and t["exported"])
        lines.append(f"- **`{item['signature']}`**（`{loc(item['source'])}`）：{note}")
    lines += [
        "- **Cow/Box/切片/数组 owner**：本目录内的转换与比较也计入；Cow 保留 Borrowed/Owned 变体和借用寿命；Box 转换保留分配所有权；元素类型/allocator 不合并。",
        "- **共享观察不是已有 view 声明**：`vec_contents`、`owned_remaining`、`drain_regions`、`extract_regions` 等是所需关系的名字，不是已实现或已证明的幽灵状态；父任务须对固定 vstd 先比对再决定复用。",
        "- **借用**：返回 `&[T]`/`&mut [T]` 与本次 receiver 借用关联；可变引用需要初始内容、最终写回和未借用区 frame，不能禁止合法写入。`leak<'a>` 保留 A:'a 与返回类型隐含 T:'a，不加 `'static`。",
        "- **回调**：FnMut/FnOnce、Clone、PartialEq、Hasher、Formatter 与 Drop 的可观察状态/异常行为不能隐藏成选答案的纯函数。",
        "",
        "## 实际委托与表示依赖（并非证明完成顺序）", "",
        "```text",
        "Vec 基本表示 ── RawVec / Allocator / pointer + 已初始化前缀",
        "  ├─ as_slice/as_mut_slice ── Deref/DerefMut ── slice indexing/hash/order/debug",
        "  ├─ into_iter ── IntoIter remaining ── next/next_back/fold/try_fold/Drop",
        "  ├─ drain ── Drain 区域 ── Splice（Drop 时消费 replace_with）",
        "  ├─ extract_if ── ExtractIf 区域 + FnMut 状态（惰性 next，Drop 保留未扫描区）",
        "  ├─ from_elem ── SpecFromElem ── IsZero 或 extend_with ── SetLenOnDrop",
        "  ├─ extend/extend_from_slice ── SpecExtend ── 一般/TrustedLen/IntoIter/借用专门化",
        "  ├─ extend_from_within ── 私有 ExtendFromWithinSpec（Clone / TrivialClone）",
        "  └─ FromIterator ── SpecFromIter",
        "         ├─ SpecFromIterNested ── Iterator / TrustedLen ── SpecExtend",
        "         ├─ IntoIter 分配复用 ── fallback SpecExtend",
        "         └─ InPlaceCollect ── 布局条件 / SourceIter / InPlaceIterable",
        "                ├─ SpecInPlaceCollect + InPlaceDrop",
        "                └─ IntoIter 剩余析构 + InPlaceDstDataSrcBufDrop + shrink",
        "Cow 转换 ── Vec/as_slice/FromIterator；PartialEq 宏 ── 两侧 slice 比较",
        "```", "",
        "具体调用语法和调用点保存在每个条目的 `direct_calls`；这是完整的直接 call-expression 记录，不冒充已类型解析的动态调用图。"
        "操作符、deref coercion、隐式析构和内建 derive 的依赖还必须结合下列语义关系。",
        "",
    ]
    for f in data["source_files"]:
        a = f["analysis"]
        lines += [
            f"### `{Path(f['path']).name}`",
            f"- 委托/表示依赖：{', '.join('`' + x + '`' for x in a['depends_on'])}。",
            f"- 观察关系：{', '.join('`' + x + '`' for x in a['views'])}。",
            f"- 源码对应义务：{a['obligations']}", "",
        ]
    lines += ["## 已定位的相邻语义依赖（不新增目标数）", ""]
    for d in data["dependency_sources"]:
        links = ", ".join(
            f"`{i['name']}` L{i['source']['start_line']}-{i['source']['end_line']}"
            for i in d["items"]
        )
        lines += [
            f"- `{d['path']}`：{d['relation']}",
            f"  - AST 定位：{links}；完整签名、bounds、文档位置见 JSON `dependency_sources`。",
        ]
    lines.append("")
    lines += [
        "## 不可混淆的计数与排除决定", "",
        "- `<Vec<T,A> as AsRef<Vec<T,A>>>::as_ref` 与 `<Vec<T,A> as AsRef<[T]>>::as_ref` 是两个身份；AsMut 同理。owner、trait 实参、impl 泛型和方法泛型均独立保存。",
        "- 稳定 impl 中的 `Iterator::{advance_by,next_chunk,__iterator_get_unchecked}`、`DoubleEndedIterator::advance_back_by`、`ExactSizeIterator::is_empty`、`Extend::{extend_one,extend_reserve,extend_one_unchecked}` 由 trait 声明确定为不稳定；不可仅继承 impl 的 stable 标签。",
        "- 相反 `Vec::push/push_mut` 的 `[const] Allocator + [const] Destruct`，以及稳定 `try_fold` 的 Try bound 不导致删除该稳定运行时 API。const 稳定性单独列出。",
        "- `from_elem` 虽 `doc(hidden)` 仍是 stable public executable，自身没有 docstring；它是目录外 `alloc/src/macros.rs` 的 `vec![elem;n]` 委托入口。宏本身不是本目录新 API。",
        "- `partial_eq.rs` 的所有实际宏调用（包括无 Vec owner 的 Cow/切片配对）展开；注释里的候选调用不计。私有 IsZero 宏也展开到排除行，元组递归不是按一行一个 impl 猜数。",
        "- Splice 的 `derive(Debug)` 是稳定 executable fmt 条目，不可遗漏；清单只展开签名/必要 bounds，未凭空写一个用于证明的替代 body。",
        "- `Eq`、`Send`、`Sync`、`FusedIterator`、`UnwindSafe` 等空 impl，及仅有关联常量的优化 trait impl，不是 executable 方法。Splice 的空 ExactSizeIterator impl 仍使默认 len 可用，另列 inherited_methods。",
        "- `Iterator` 等 trait 未覆盖的默认方法按每个本地 impl 机械枚举，但实现源在 core，不加到本模块实现数。supertrait 方法沿原 trait 身份处理，不按多个 trait 重复镜像。",
        "- `Into/From<T>/TryInto/TryFrom`、Borrow/BorrowMut、ToOwned、Any、Iterator->IntoIterator 与引用转发 blanket 用源声明族表示；不存在无限展开所有泛型实例的假计数。`From<!>` reservation impl 明确不可用。",
        "- Vec 的 `Borrow<[T]>` / `BorrowMut<[T]>` 实现在相邻 alloc/slice.rs；只记模块外边界。deref 可见的 slice API、目录外集合转换/std trait impl 和 std::vec 重导出均非本目录所定义；没有产生 Slice campaign 输出。",
        "- 私有 spec_*、in_place_*、SetLenOnDrop 与局部 Drop/panic guard 是源正确性依赖，不作为独立 public 目标，也不因排除而声称其证明可跳过。",
        "",
        "## 机械检查", "",
    ]
    lines += ["- " + c + "。" for c in data["checks"]]
    lines += [
        "- `--check` 重新从源码提取，逐字比较 JSON/TSV/源码段落；保留的 vstd 段落由 `scripts/inventory_vstd.py --check` 独立检查，不使用旧清单来构造新清单。",
        "- source-tests 覆盖宏配对、反向 owner、双 allocator、稳定性继承、默认与空 impl、文档位置、cfg、泛型/生命周期及变更后重放。",
        "- 这些检查只验证清单/源码抽取，既不是 Verus 源实现证明，也不是 spec-determin-tool 完整性检查。",
        "",
    ]
    return "\n".join(lines)


def update_source_section(original, source):
    begin = "<!-- BEGIN OFFICIAL VSTD COVERAGE -->"
    end = "<!-- END OFFICIAL VSTD COVERAGE -->"
    if begin not in original:
        assert end not in original, "orphan coverage end marker"
        return source
    assert original.count(begin) == original.count(end) == 1, "malformed coverage markers"
    start = original.index(begin)
    assert original.index(end) > start, "reversed coverage markers"
    return source.rstrip("\n") + "\n\n" + original[start:]


def generated_files(data):
    document = PROJECT / "inventory/submodules.md"
    original = document.read_text() if document.exists() else ""
    return {
        "inventory/source_api.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        "inventory/source_api.tsv": render_tsv(data),
        "inventory/submodules.md": update_source_section(original, render_markdown(data)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-library", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = Inventory(args.source_library).build()
    for relative, text in generated_files(data).items():
        path = PROJECT / relative
        if args.check:
            assert path.read_text() == text, f"{relative} 与 fresh source extraction 不一致"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    print(json.dumps({"result": "source extraction checks passed", **data["counts"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
