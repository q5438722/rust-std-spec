#!/usr/bin/env python3
"""Bind the existing source inventory to the pinned official vstd, without proofs."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[1]
VSTD = PROJECT / "toolchains/upstream/source/vstd"
COMMIT = "aef82eda71838deef4a8cd0260fda6c9504be9b9"
TAG = "release/0.2026.09.20.aef82ed"
BEGIN = "<!-- BEGIN OFFICIAL VSTD COVERAGE -->"
END = "<!-- END OFFICIAL VSTD COVERAGE -->"
CLASSES = ("exact", "partial", "trait_only", "indirect", "none")
IDENTITY_FIELDS = (
    "inventory_id", "canonical_id", "source_module", "source_owner",
    "canonical_owner", "trait", "canonical_trait", "method", "signature",
    "impl_header", "impl_generic_parameters", "impl_where_clause",
    "method_generic_parameters", "method_where_clause", "receiver",
    "lifetime_relation", "associated_items", "source", "signature_source",
    "docs", "cfg", "origin",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compact(text):
    return re.sub(r"\s+", " ", text).strip()


def tokens(text):
    return re.sub(r"\s+", "", text)


def mask_noncode(text):
    """Keep offsets/newlines; ignore nested comments and Rust string/char literals."""
    out = list(text)
    i = 0
    while i < len(text):
        end = None
        if text.startswith("//", i):
            end = text.find("\n", i)
            if end < 0:
                end = len(text)
        elif text.startswith("/*", i):
            depth, j = 1, i + 2
            while j < len(text) and depth:
                if text.startswith("/*", j):
                    depth += 1
                    j += 2
                elif text.startswith("*/", j):
                    depth -= 1
                    j += 2
                else:
                    j += 1
            require(depth == 0, "unterminated block comment")
            end = j
        else:
            raw = re.match(r'(?:br|cr|r)(#{0,255})"', text[i:])
            if raw and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] == "_")):
                closing = '"' + raw[1]
                at = text.find(closing, i + len(raw[0]))
                require(at >= 0, "unterminated raw string")
                end = at + len(closing)
            elif text[i] == '"':
                j = i + 1
                while j < len(text):
                    if text[j] == "\\":
                        j += 2
                    elif text[j] == '"':
                        end = j + 1
                        break
                    else:
                        j += 1
                require(end is not None, "unterminated string")
            elif text[i] == "'":
                char = re.match(r"'(?:\\(?:u\{[0-9a-fA-F_]+\}|x[0-9a-fA-F]{2}|.)|[^'\\\n])'", text[i:])
                if char:
                    end = i + len(char[0])
        if end is None:
            i += 1
        else:
            for j in range(i, end):
                if out[j] != "\n":
                    out[j] = " "
            i = end
    return "".join(out)


def balanced_end(code, start):
    pairs = {"(": ")", "[": "]", "{": "}"}
    require(code[start] in pairs, "balanced region must start with a delimiter")
    stack = [pairs[code[start]]]
    for i in range(start + 1, len(code)):
        c = code[i]
        if c in pairs:
            stack.append(pairs[c])
        elif c in ")]}":
            require(stack and stack.pop() == c, f"mismatched delimiter at {i}")
            if not stack:
                return i + 1
    raise ValueError("unterminated balanced region")


def generic_end(code, start):
    depth, i = 1, start + 1
    while i < len(code):
        c = code[i]
        if c in "([{":
            i = balanced_end(code, i)
            continue
        if c == "<":
            depth += 1
        elif c == ">" and code[i - 1] not in "-=":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unterminated generic parameters")


def semicolon_end(code, start):
    i = start
    while i < len(code):
        if code[i] in "([{":
            i = balanced_end(code, i)
        elif code[i] == ";":
            return i + 1
        else:
            i += 1
    raise ValueError("unterminated declaration")


def split_contract(text):
    code = mask_noncode(text)
    keys = ("requires", "ensures", "default_ensures", "returns",
            "opens_invariants", "no_unwind", "decreases")
    points = []
    i = 0
    while i < len(code):
        if code[i] in "([{":
            i = balanced_end(code, i)
            continue
        word = re.match(r"[A-Za-z_]\w*", code[i:])
        if word:
            if word[0] in keys and (i == 0 or code[i - 1] not in ".:"):
                points.append((i, i + len(word[0]), word[0]))
            i += len(word[0])
        else:
            i += 1
    signature_end = points[0][0] if points else len(text.rstrip().rstrip(";"))
    clauses = {}
    for n, (start, value, key) in enumerate(points):
        end = points[n + 1][0] if n + 1 < len(points) else len(text.rstrip().rstrip(";"))
        clauses[key] = text[value:end].strip()
    return text[:signature_end].strip(), clauses


class OfficialTree:
    def __init__(self, root=VSTD):
        self.root = root
        self.texts = {}
        self.code = {}
        self.files = []
        self.assumptions = []
        self.evidence = {}
        for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
            require(".git" not in path.relative_to(root).parts, "unexpected Git metadata in official tree")
            if not path.is_file():
                continue
            raw = path.read_bytes()
            relative = path.relative_to(root).as_posix()
            item = {"path": relative, "bytes": len(raw), "sha256": digest(raw)}
            if path.suffix == ".rs":
                text = raw.decode("utf-8")
                self.texts[relative] = text
                self.code[relative] = mask_noncode(text)
                item["lines"] = len(text.splitlines())
                item["assume_declarations_or_templates"] = 0
                item["active_external_fn_attributes"] = len(re.findall(
                    r"#\s*\[\s*verifier::external_fn_specification\s*\]", self.code[relative]))
            self.files.append(item)
        require(self.texts, "official vstd tree is missing")
        for item in self.files:
            path = item["path"]
            if path not in self.texts:
                continue
            text, code = self.texts[path], self.code[path]
            for match in re.finditer(r"\bassume_specification\b", code):
                start = match.start()
                prefix = re.search(r"\bpub\s+$", code[:start])
                if prefix:
                    start = prefix.start()
                i = match.end()
                while code[i].isspace():
                    i += 1
                generic = ""
                if code[i] == "<":
                    end = generic_end(code, i)
                    generic = text[i:end]
                    i = end
                    while code[i].isspace():
                        i += 1
                require(code[i] == "[", f"unrecognized assume specification at {path}:{start}")
                target_end = balanced_end(code, i)
                target = text[i + 1:target_end - 1].strip()
                end = semicolon_end(code, target_end)
                record = self.fragment(path, start, end)
                signature, clauses = split_contract(text[target_end:end])
                record.update(
                    kind="assume_specification",
                    literal_target=target,
                    literal_generics=generic,
                    literal_signature=signature,
                    literal_clauses=clauses,
                    macro_template="$" in code[start:end],
                )
                self.assumptions.append(record)
                item["assume_declarations_or_templates"] += 1

    def fragment(self, path, start, end):
        text = self.texts[path]
        literal = text[start:end]
        return {
            "source": {
                "path": f"toolchains/upstream/source/vstd/{path}",
                "start_line": text.count("\n", 0, start) + 1,
                "end_line": text.count("\n", 0, end - 1) + 1,
                "start_byte": len(text[:start].encode("utf-8")),
                "end_byte": len(text[:end].encode("utf-8")),
            },
            "literal": literal,
            "sha256": digest(literal.encode("utf-8")),
        }

    def add(self, name, record, **metadata):
        require(name not in self.evidence, f"duplicate evidence id {name}")
        self.evidence[name] = {"id": name, **record, **metadata}
        return name

    def assume(self, name, path, target, **metadata):
        matches = [r for r in self.assumptions
                   if r["source"]["path"].endswith("/" + path)
                   and tokens(r["literal_target"]) == tokens(target)]
        require(len(matches) == 1, f"expected one exact target {path}: {target}, got {len(matches)}")
        return self.add(name, matches[0], **metadata)

    def locate(self, path, needle, start=0, end=None):
        code = self.code[path]
        end = len(code) if end is None else end
        matches = [m.start() + start for m in re.finditer(re.escape(needle), code[start:end])]
        require(len(matches) == 1, f"expected unique active anchor in {path}: {needle!r}")
        return matches[0]

    def block(self, name, path, needle, kind, **metadata):
        start = self.locate(path, needle)
        opening = self.code[path].find("{", start)
        end = balanced_end(self.code[path], opening)
        return self.add(name, self.fragment(path, start, end), kind=kind,
                        literal_header=self.texts[path][start:opening].strip(), **metadata)

    def semi(self, name, path, needle, kind, **metadata):
        start = self.locate(path, needle)
        end = semicolon_end(self.code[path], start)
        return self.add(name, self.fragment(path, start, end), kind=kind, **metadata)

    def method(self, name, context, method):
        parent = self.evidence[context]
        path = parent["source"]["path"].removeprefix("toolchains/upstream/source/vstd/")
        text = self.texts[path]
        start = len(text.encode("utf-8")[:parent["source"]["start_byte"]].decode("utf-8"))
        end = start + len(parent["literal"])
        matches = list(re.finditer(r"\bfn\s+" + re.escape(method) + r"(?=[<(\s])",
                                   self.code[path][start:end]))
        require(len(matches) == 1, f"method is not unique: {context}::{method}")
        at = start + matches[0].start()
        finish = semicolon_end(self.code[path], at)
        fragment = self.fragment(path, at, finish)
        signature, clauses = split_contract(fragment["literal"])
        return self.add(name, fragment, kind="external_trait_method",
                        context_ref=context, literal_signature=signature,
                        literal_clauses=clauses)

    def symbol_occurrences(self, symbol):
        result = []
        for path, code in self.code.items():
            for match in re.finditer(r"\b" + re.escape(symbol) + r"\b", code):
                result.append({"path": path, "line": code.count("\n", 0, match.start()) + 1})
        return result


def load_source():
    path = PROJECT / "inventory/source_api.json"
    source = json.loads(path.read_text())
    tsv = list(csv.DictReader(io.StringIO((PROJECT / "inventory/source_api.tsv").read_text()), delimiter="\t"))
    included = [r for r in tsv if r["status"] == "included"]
    ids = [r["canonical_id"] for r in source["apis"]]
    require(len(ids) == len(set(ids)), "duplicate input canonical identity")
    require(Counter(ids) == Counter(r["canonical_id"] for r in included),
            "source JSON/TSV included identities differ")
    require(len(ids) == source["counts"]["stable_public_executable"], "input target count mismatch")
    require(len(source["excluded_functions"]) == source["counts"]["excluded_function_candidates"],
            "input exclusion accounting mismatch")
    require(len(tsv) == len(ids) + len(source["excluded_functions"]), "input candidate accounting mismatch")
    require(len(source["source_files"]) == source["counts"]["source_files"], "source file count mismatch")
    require(len(source["inherited_trait_methods"]) == source["counts"]["inherited_trait_default_instances"],
            "input default-method accounting mismatch")
    actual = Counter(r["source"]["path"].split("/")[-1] for r in source["apis"])
    for file in source["source_files"]:
        name = file["path"].split("/")[-1]
        require(actual[name] == source["counts"]["by_source_file"][name],
                f"source module accounting mismatch: {name}")
    return source


def api_id(owner, trait, method):
    return f"<{owner} as {trait}>::{method}" if trait else f"{owner}::{method}"


def collect_evidence(tree):
    vec = "std_specs/vec.rs"
    direct = {}
    for method in ("len", "reserve", "try_reserve", "push", "pop", "append",
                   "extend_from_slice", "swap_remove", "insert", "remove", "clear",
                   "as_slice", "as_mut_slice", "split_off", "truncate", "resize"):
        ref = tree.assume(f"vec.{method}", vec, f"Vec::<T, A>::{method}")
        direct[api_id("alloc::vec::Vec<T, A>", None, method)] = ref
    for method in ("new", "with_capacity"):
        ref = tree.assume(f"vec.{method}", vec, f"Vec::<T>::{method}")
        direct[api_id("alloc::vec::Vec<T>", None, method)] = ref
    for method in ("new_in", "with_capacity_in"):
        tree.assume(f"vec.{method}", vec, f"Vec::<T, A>::{method}",
                    source_scope="excluded unstable API, not a stable target")
    ref = tree.assume("vec.is_empty", vec, "<Vec<T, A>>::is_empty")
    direct["alloc::vec::Vec<T, A>::is_empty"] = ref
    aliases = [
        ("default", "<Vec<T> as core::default::Default>::default",
         "alloc::vec::Vec<T>", "core::default::Default", "default"),
        ("deref", "<Vec<T, A> as core::ops::Deref>::deref",
         "alloc::vec::Vec<T, A>", "core::ops::Deref", "deref"),
        ("deref_mut", "<Vec<T, A> as core::ops::DerefMut>::deref_mut",
         "alloc::vec::Vec<T, A>", "core::ops::DerefMut", "deref_mut"),
        ("clone", "<Vec<T, A> as Clone>::clone",
         "alloc::vec::Vec<T, A>", "core::clone::Clone", "clone"),
        ("index", "Vec::<T, A>::index",
         "alloc::vec::Vec<T, A>", "core::ops::Index<I>", "index"),
        ("eq", "<Vec<T, A1> as PartialEq<Vec<U, A2>>>::eq",
         "alloc::vec::Vec<T, A1>", "core::cmp::PartialEq<alloc::vec::Vec<U, A2>>", "eq"),
        ("into_iter", "Vec::<T, A>::into_iter",
         "alloc::vec::Vec<T, A>", "core::iter::IntoIterator", "into_iter"),
        ("ref_into_iter", "<&'a Vec<T, A> as core::iter::IntoIterator>::into_iter",
         "&'a alloc::vec::Vec<T, A>", "core::iter::IntoIterator", "into_iter"),
    ]
    for name, target, owner, trait, method in aliases:
        ref = tree.assume("vec." + name, vec, target)
        direct[api_id(owner, trait, method)] = ref
    direct["alloc::vec::from_elem"] = tree.assume("vec.from_elem", vec, "alloc::vec::from_elem")

    blocks = [
        ("vec.index_usize", vec, "pub fn vec_index<", "compiler_index_hook"),
        ("vec.index_mut_usize", vec, "pub fn vec_index_mut<", "compiler_index_hook"),
        ("vec.index_model", vec, "impl<T: Sized, I: SliceIndex<[T]>, A: Allocator>", "concrete_spec_impl"),
        ("vec.eq_model", vec, "impl<T: super::cmp::PartialEqSpec<U>, U, A1:", "concrete_spec_impl"),
        ("vec.iterator_model", vec, "impl <T, A: Allocator> super::iter::IteratorSpecImpl", "concrete_spec_impl"),
        ("vec.double_ended_model", vec, "impl <T, A: Allocator> super::iter::DoubleEndedIteratorSpecImpl", "concrete_spec_impl"),
        ("vec.from_iter_model", vec, "impl<T>  FromIteratorSpecImpl<T> for Vec<T>", "concrete_spec_impl"),
        ("vec.index_spec", vec, "impl<T, A: Allocator> VecAdditionalSpecFns<T>", "spec_impl"),
        ("vec.index_spec_trait", vec, "pub trait VecAdditionalSpecFns<T>", "spec_trait"),
        ("vec.len_axiom", vec, "pub broadcast proof fn axiom_spec_len<", "trusted_axiom"),
        ("vec.clone_trigger", vec, "pub open spec fn vec_clone_trigger<", "spec_helper"),
        ("vec.clone_deep", vec, "pub broadcast proof fn vec_clone_deep_view_proof<", "proof_helper"),
        ("vec.index_decreases", vec, "pub broadcast proof fn axiom_vec_index_decreases<", "trusted_axiom_global_only"),
        ("vec.eq_law", vec, "pub broadcast proof fn lemma_vec_obeys_eq_spec<", "proof_helper_global_only"),
        ("vec.view_eq_law", vec, "pub broadcast proof fn lemma_vec_obeys_view_eq<", "proof_helper_global_only"),
        ("vec.deep_eq_law", vec, "pub broadcast proof fn lemma_vec_obeys_deep_eq<", "proof_helper_global_only"),
        ("vec.axiom_group", vec, "pub broadcast group group_vec_axioms", "broadcast_group"),
        ("vec.view", "view.rs", "impl<T, A: core::alloc::Allocator> View for alloc::vec::Vec", "view_impl"),
        ("vec.deep_view", "view.rs", "impl<T: DeepView, A: core::alloc::Allocator> DeepView for alloc::vec::Vec", "view_impl"),
        ("vec.erased_view", "view.rs", "impl<T> View for alloc::vec::Vec<T>", "view_impl"),
        ("vec.erased_deep_view", "view.rs", "impl<T: DeepView> DeepView for alloc::vec::Vec<T>", "view_impl"),
        ("ref.view", "view.rs", "impl<A: View + ?Sized> View for &A", "view_impl"),
        ("box.view", "view.rs", "impl<A: View + ?Sized> View for alloc::boxed::Box<A>", "view_impl"),
        ("slice.view", "slice.rs", "impl<T> View for [T]", "view_impl"),
        ("slice.deep_view", "slice.rs", "impl<T: DeepView> DeepView for [T]", "view_impl"),
        ("slice.index_hook", "slice.rs", "pub exec fn slice_index_get<", "compiler_index_hook"),
        ("slice.to_vec_wrapper", "slice.rs", "pub exec fn slice_to_vec<", "vstd_wrapper_not_std_binding"),
        ("slice.index_model", "std_specs/slice.rs", "impl<T, I: SliceIndex<[T]>> super::core::IndexSpecImpl", "concrete_spec_impl"),
        ("slice.eq_model", "std_specs/slice.rs", "impl<T, U> super::cmp::PartialEqSpecImpl<[U]> for [T]", "concrete_spec_impl"),
        ("slice.iterator_model", "std_specs/slice.rs", "impl <'a, T: 'a> super::iter::IteratorSpecImpl", "concrete_spec_impl"),
        ("slice.iter_mut_model", "std_specs/slice.rs", "impl<'a, T: 'a> super::iter::IteratorSpecImpl for IterMut", "concrete_spec_impl"),
        ("slice.generic_in_bounds", "std_specs/slice.rs", "pub open spec fn generic_slice_in_bounds<", "spec_helper"),
        ("slice.generic_index_post", "std_specs/slice.rs", "pub open spec fn generic_slice_index_postcondition<", "spec_helper"),
        ("slice.generic_index_mut_post", "std_specs/slice.rs", "pub open spec fn generic_slice_index_mut_postcondition<", "spec_helper"),
        ("cow.slice_view", "std_specs/borrow.rs", "impl<'a, T: View + Clone> View for Cow<'a, [T]>", "view_impl"),
        ("cow.slice_deep_view", "std_specs/borrow.rs", "impl<'a, T: DeepView + Clone> DeepView for Cow<'a, [T]>", "view_impl"),
        ("array.view", "array.rs", "impl<T, const N: usize> View for [T; N]", "view_impl"),
        ("array.view_definition", "array.rs", "pub open spec fn array_view<", "spec_helper"),
        ("array.coercion", "array.rs", "pub fn array_as_slice<", "compiler_coercion_hook"),
        ("clone.strictly_cloned", "pervasive.rs", "pub open spec fn strictly_cloned<", "spec_helper"),
        ("clone.cloned", "pervasive.rs", "pub open spec fn cloned<", "spec_helper"),
        ("vec.extra_exec", "pervasive.rs", "impl<T> VecAdditionalExecFns<T> for alloc::vec::Vec<T>", "vstd_wrapper_not_std_binding"),
        ("iterator.ref_model", "std_specs/iter.rs", "impl <I> IteratorSpecImpl for &mut I", "blanket_spec_impl"),
        ("fmt.template", "std_specs/fmt.rs", "macro_rules! def_fmt_trait", "external_trait_macro_template"),
        ("range.bounds", "std_specs/range.rs", "pub trait ExRangeBounds<T: ?Sized>", "external_trait"),
        ("range.start", "std_specs/range.rs", "pub open spec fn slice_range_start<", "spec_helper"),
        ("range.end", "std_specs/range.rs", "pub open spec fn slice_range_end<", "spec_helper"),
        ("range.valid", "std_specs/range.rs", "pub open spec fn slice_range_valid<", "spec_helper"),
        ("range.inclusive_view_type", "std_specs/range.rs", "pub struct RangeInclusiveView<", "view_type"),
        ("range.inclusive_view", "std_specs/range.rs", "impl<Idx> View for RangeInclusive<Idx>", "view_impl"),
        ("range.inclusive_end", "std_specs/range.rs", "pub open spec fn spec_range_inclusive_end_bound<", "spec_helper"),
        ("string.byte_model", "string.rs", "impl StringSliceAdditionalSpecFns for str", "spec_impl"),
    ]
    for name, path, anchor, kind in blocks:
        tree.block(name, path, anchor, kind)
    for name, path, anchor, kind in [
        ("vec.type", vec, "pub struct ExVec<", "external_type"),
        ("vec.into_iter_type", vec, "pub struct ExIntoIter<", "external_type"),
        ("vec.try_reserve_error", vec, "pub struct ExTryReserveError", "external_type"),
        ("vec.len_spec", vec, "pub uninterp spec fn spec_vec_len<", "uninterpreted_spec"),
        ("vec.into_iter_elts", vec, "pub uninterp spec fn into_iter_elts<", "uninterpreted_spec"),
        ("vec.has_resolved", vec, "pub broadcast axiom fn axiom_vec_has_resolved<", "trusted_axiom_global_only"),
        ("vec.decreases_to_view", vec, "pub broadcast axiom fn axiom_vec_decreases_to_view<", "trusted_axiom_global_only"),
        ("slice.len_spec", "slice.rs", "pub uninterp spec fn spec_slice_len<", "uninterpreted_spec"),
        ("slice.len_axiom", "slice.rs", "pub broadcast axiom fn axiom_spec_len<", "trusted_axiom"),
        ("slice.into_iter_elts", "std_specs/slice.rs", "pub uninterp spec fn into_iter_elts<", "uninterpreted_spec"),
        ("slice.iter_type", "std_specs/slice.rs", "pub struct ExIter<", "external_type"),
        ("slice.iter_mut_type", "std_specs/slice.rs", "pub struct ExIterMut<", "external_type"),
        ("cow.type", "std_specs/borrow.rs", "pub struct ExCow<", "external_type"),
        ("slice.mutable_length", "slice.rs", "pub axiom fn mut_ref_slice_len_eq<", "trusted_axiom"),
        ("iterator.into_iter_remaining", "std_specs/iter.rs", "pub uninterp spec fn into_iter_remaining<", "uninterpreted_spec"),
        ("iterator.from_iter_axiom", "std_specs/iter.rs", "pub broadcast axiom fn axiom_from_iterator_ensures<", "trusted_axiom"),
        ("fmt.debug_expansion", "std_specs/fmt.rs", "def_fmt_trait!(core::fmt::Debug,", "macro_invocation"),
        ("vec.tracked_borrow", vec, "pub axiom fn tracked_borrow_slice<", "tracked_borrow_axiom"),
        ("vec.tracked_borrow_mut", vec, "pub axiom fn tracked_borrow_mut_slice<", "tracked_borrow_axiom"),
    ]:
        tree.semi(name, path, anchor, kind)

    trait_methods = {}
    traits = [
        ("clone", "std_specs/clone.rs", "pub trait ExClone", "core::clone::Clone", ["clone"]),
        ("default", "std_specs/default.rs", "pub trait ExDefault", "core::default::Default", ["default"]),
        ("deref", "std_specs/core.rs", "pub trait ExDeref:", "core::ops::Deref", ["deref"]),
        ("deref_mut", "std_specs/core.rs", "pub trait ExDerefMut:", "core::ops::DerefMut", ["deref_mut"]),
        ("index", "std_specs/core.rs", "pub trait ExIndex<", "core::ops::Index", ["index"]),
        ("index_mut", "std_specs/core.rs", "pub trait ExIndexMut<", "core::ops::IndexMut", ["index_mut"]),
        ("hash", "std_specs/core.rs", "pub trait ExHash:", "core::hash::Hash", []),
        ("fn_once", "std_specs/core.rs", "pub trait ExFnOnce<", "core::ops::FnOnce", []),
        ("fn_mut", "std_specs/core.rs", "pub trait ExFnMut<", "core::ops::FnMut", []),
        ("allocator", "std_specs/core.rs", "pub trait ExAllocator", "core::alloc::Allocator", []),
        ("partial_eq", "std_specs/cmp.rs", "pub trait ExPartialEq<", "core::cmp::PartialEq", ["eq", "ne"]),
        ("partial_ord", "std_specs/cmp.rs", "pub trait ExPartialOrd<", "core::cmp::PartialOrd", ["partial_cmp", "lt", "le", "gt", "ge"]),
        ("ord", "std_specs/cmp.rs", "pub trait ExOrd:", "core::cmp::Ord", ["cmp", "max", "min", "clamp"]),
        ("from", "std_specs/convert.rs", "pub trait ExFrom<", "core::convert::From", ["from"]),
        ("into", "std_specs/convert.rs", "pub trait ExInto<", "core::convert::Into", ["into"]),
        ("try_from", "std_specs/convert.rs", "pub trait ExTryFrom<", "core::convert::TryFrom", ["try_from"]),
        ("try_into", "std_specs/convert.rs", "pub trait ExTryInto<", "core::convert::TryInto", ["try_into"]),
        ("iterator", "std_specs/iter.rs", "pub trait ExIterator {", "core::iter::Iterator",
         ["next", "all", "any", "collect", "filter", "find", "map", "rev", "skip", "take", "zip"]),
        ("double_ended", "std_specs/iter.rs", "pub trait ExDoubleEndedIterator", "core::iter::DoubleEndedIterator", ["next_back"]),
        ("exact_size", "std_specs/iter.rs", "pub trait ExExactSizeIterator", "core::iter::ExactSizeIterator", ["len"]),
        ("into_iterator", "std_specs/iter.rs", "pub trait ExIntoIterator", "core::iter::IntoIterator", ["into_iter"]),
        ("from_iterator", "std_specs/iter.rs", "pub trait ExFromIterator<", "core::iter::FromIterator", ["from_iter"]),
        ("slice_index", "slice.rs", "pub trait ExSliceIndex<", "core::slice::SliceIndex", ["index", "index_mut", "get", "get_mut"]),
    ]
    for name, path, anchor, target, methods in traits:
        context = tree.block("trait." + name, path, anchor, "external_trait", canonical_trait=target)
        for method in methods:
            ref = tree.method("trait." + name + "." + method, context, method)
            trait_methods[(target, method)] = ref
    debug = tree.method("trait.debug.fmt", "fmt.template", "fmt")
    tree.evidence[debug]["instantiation_ref"] = "fmt.debug_expansion"
    tree.evidence[debug]["canonical_trait"] = "core::fmt::Debug"
    trait_methods[("core::fmt::Debug", "fmt")] = debug

    for name, target in [
        ("slice.index", "<[T] as Index<I>>::index"),
        ("slice.index_mut", "<[T] as IndexMut<I>>::index_mut"),
        ("slice.eq", "<[T] as PartialEq<[U]>>::eq"),
        ("slice.iter", "<[T]>::iter"),
        ("slice.iter_mut", "<[T]>::iter_mut"),
        ("slice.last_mut", "<[T]>::last_mut"),
        ("slice.ref_into_iter", "<&'a [T] as core::iter::IntoIterator>::into_iter"),
    ]:
        tree.assume(name, "std_specs/slice.rs", target)
    for index_type in ("usize", "Range<usize>", "RangeTo<usize>", "RangeFrom<usize>",
                       "RangeToInclusive<usize>", "RangeFull", "RangeInclusive<usize>"):
        slug = index_type.split("<", 1)[0].lower()
        tree.block("slice.index_model." + slug, "std_specs/slice.rs",
                   f"impl<T> super::super::slice::SliceIndexSpecImpl<[T]> for {index_type} ",
                   "concrete_spec_impl")
        for method in ("index", "index_mut"):
            tree.assume(f"slice.{slug}.{method}", "std_specs/slice.rs",
                        f"<{index_type} as SliceIndex<[T]>>::{method}")
    for range_type in ("Range", "RangeFrom", "RangeTo", "RangeFull", "RangeInclusive", "RangeToInclusive"):
        parameters = "<T: ?Sized>" if range_type == "RangeFull" else "<T>"
        owner = range_type if range_type == "RangeFull" else range_type + "<T>"
        tree.block("range.model." + range_type.lower(), "std_specs/range.rs",
                   f"impl{parameters} RangeBoundsSpecImpl<T> for {owner} ",
                   "concrete_spec_impl")
    for name, path, target in [
        ("box.into_vec", "std_specs/smart_ptrs.rs", "<[T]>::into_vec"),
        ("box.new", "std_specs/smart_ptrs.rs", "Box::<T>::new"),
        ("slice.len", "slice.rs", "<[T]>::len"),
        ("array.as_slice", "array.rs", "<[T; N]>::as_slice"),
        ("string.as_bytes", "string.rs", "str::as_bytes"),
        ("manually_drop.new", "std_specs/manually_drop.rs", "ManuallyDrop::<T>::new"),
        ("manually_drop.deref", "std_specs/manually_drop.rs", "<ManuallyDrop<T> as Deref>::deref"),
        ("convert.blanket_into", "std_specs/convert.rs", "<T as Into<U>>::into"),
        ("convert.blanket_try_into", "std_specs/convert.rs", "<T as TryInto<U>>::try_into"),
        ("convert.blanket_try_from", "std_specs/convert.rs", "<T as TryFrom<U>>::try_from"),
        ("iterator.blanket_into_iter", "std_specs/iter.rs", "<I as IntoIterator>::into_iter"),
        ("alloc.vec_literal_array", "std_specs/alloc.rs", "alloc::boxed::box_assume_init_into_vec_unsafe"),
        ("alloc.write_box", "std_specs/alloc.rs", "alloc::intrinsics::write_box_via_move"),
    ]:
        tree.assume(name, path, target)

    for name in ("vec.index_usize", "vec.index_mut_usize", "slice.index_hook"):
        record = tree.evidence[name]
        head = record["literal"].split("{", 1)[0]
        record["literal_signature"], record["literal_clauses"] = split_contract(head)
        record["binding_scope"] = "compiler indexing syntax redirection; not an assume_specification for explicit UFCS"
    supports = {
        "vec.len": ["vec.len_spec", "vec.len_axiom"],
        "slice.len": ["slice.len_spec", "slice.len_axiom"],
        "vec.index_spec": ["vec.index_spec_trait", "vec.view"],
        "vec.axiom_group": ["vec.len_axiom", "vec.index_decreases", "vec.clone_deep", "vec.has_resolved", "vec.decreases_to_view"],
        "vec.clone": ["clone.cloned", "vec.clone_trigger", "vec.clone_deep"],
        "vec.resize": ["clone.cloned"],
        "vec.extend_from_slice": ["clone.cloned"],
        "vec.from_elem": ["clone.cloned"],
        "clone.cloned": ["clone.strictly_cloned", "trait.clone.clone"],
        "vec.eq": ["trait.partial_eq.eq", "vec.eq_model", "vec.eq_law", "vec.view_eq_law", "vec.deep_eq_law"],
        "vec.eq_model": ["vec.len", "vec.index_spec", "trait.partial_eq"],
        "vec.into_iter": ["vec.into_iter_elts", "vec.iterator_model"],
        "vec.ref_into_iter": ["slice.into_iter_elts", "slice.iterator_model"],
        "vec.from_iter_model": ["trait.from_iterator.from_iter", "iterator.into_iter_remaining", "iterator.from_iter_axiom"],
        "vec.index": ["vec.index_model", "trait.index.index", "trait.slice_index.index"],
        "vec.index_mut_usize": ["vec.view", "vec.index_spec", "vec.len"],
        "vec.index_usize": ["vec.view", "vec.index_spec", "vec.len"],
        "slice.generic_in_bounds": ["range.valid", "range.start", "range.end"],
        "slice.generic_index_post": ["range.start", "range.end"],
        "slice.generic_index_mut_post": ["range.start", "range.end"],
        "range.inclusive_view": ["range.inclusive_view_type"],
        "range.model.rangeinclusive": ["range.inclusive_view", "range.inclusive_end"],
        "range.inclusive_end": ["range.inclusive_view"],
    }
    for slug in ("usize", "range", "rangeto", "rangefrom", "rangetoinclusive", "rangefull", "rangeinclusive"):
        model = "slice.index_model." + slug
        for method in ("index", "index_mut"):
            supports[f"slice.{slug}.{method}"] = [f"trait.slice_index.{method}", model]
        if slug != "usize":
            supports[model] = ["slice.generic_in_bounds", "slice.generic_index_post",
                               "slice.generic_index_mut_post", "range.model." + slug]
        supports["vec.index"].extend([model, f"slice.{slug}.index"])
    for ref, dependencies in supports.items():
        tree.evidence[ref]["support_refs"] = dependencies
    return direct, trait_methods


def view_inventory():
    return [
        {
            "id": "vec_sequence", "status": "official_opaque_view",
            "domain": "Vec<T, A>, T unrestricted, A: Allocator",
            "definition_refs": ["vec.type", "vec.view", "vec.deep_view", "vec.erased_view", "vec.erased_deep_view", "ref.view"],
            "relation_refs": ["vec.len_spec", "vec.len_axiom", "vec.index_spec", "vec.axiom_group"],
            "depends_on": [],
            "meaning": "View::V = Seq<T>; DeepView maps each element and separately requires T: DeepView. Ghost/allocator cfg has A; the non-ghost fallback is Global-only. The index-decreases, has_resolved and decreases-to-view axioms here explicitly use default-allocator Vec<T>, unlike the allocator-generic len axiom.",
            "source_bridge_required": "Relate the initialized prefix of buf/len to Seq, including ZST and length bounds. The opaque view does not expose capacity, allocation, addresses or allocator identity.",
        },
        {
            "id": "slice_sequence", "status": "official_opaque_view",
            "domain": "[T], T unrestricted",
            "definition_refs": ["slice.view", "slice.deep_view", "ref.view"],
            "relation_refs": ["slice.len", "slice.mutable_length", "vec.as_slice", "vec.as_mut_slice", "vec.deref", "vec.deref_mut", "vec.tracked_borrow", "vec.tracked_borrow_mut"],
            "depends_on": ["vec_sequence"],
            "meaning": "The Vec borrow constructors tie slice@ to the Vec sequence; mutable constructors give immediate equality and final(slice)@ == final(vec)@.",
            "source_bridge_required": "Preserve lawful writes and the initialized-region relation. Pointer metadata alone is not content; final is the borrow's final value, not evidence of Drop execution.",
        },
        {
            "id": "index_domain", "status": "official_trait_and_concrete_models",
            "domain": "I: SliceIndex<[T]>; mutable Vec content hook only for usize indexing syntax",
            "definition_refs": ["trait.index", "trait.index_mut", "trait.slice_index", "vec.index_model"],
            "relation_refs": ["vec.index", "vec.index_usize", "vec.index_mut_usize", "slice.index", "slice.index_mut", "range.bounds", "range.start", "range.end", "range.valid"],
            "depends_on": ["vec_sequence", "slice_sequence"],
            "meaning": "Vec index_req quantifies over slices with the same sequence; immutable index has an existential slice/call_ensures postcondition. usize plus six range SliceIndex models are explicit in std_specs/slice.rs.",
            "source_bridge_required": "Do not transfer the slice IndexMut postcondition through Vec's generic IndexMut without a source/delegation proof. The generic IndexMut trait only adds a precondition.",
        },
        {
            "id": "iterator_framework", "status": "official_generic_prophetic_contract",
            "domain": "Iterator / DoubleEndedIterator / ExactSizeIterator; no concrete representation implied",
            "definition_refs": ["trait.iterator", "trait.double_ended", "trait.exact_size", "iterator.ref_model"],
            "relation_refs": ["trait.iterator.next", "trait.double_ended.next_back", "trait.exact_size.len"],
            "depends_on": [],
            "meaning": "remaining is the prophetic sequence of future yielded items. Transition laws are guarded by obeys_prophetic_iter_laws; will_return_none and an optional decrease metric are separate observations.",
            "source_bridge_required": "Establish the concrete iterator's law predicate and its constructor/state relation. An arbitrary guarded framework is not a view of a source representation.",
        },
        {
            "id": "owned_iterator_state", "status": "official_state_relative_spec_functions_not_View",
            "domain": "IntoIter<T, A>, T unrestricted, A: Allocator",
            "definition_refs": ["vec.into_iter_type", "vec.into_iter_elts", "vec.iterator_model", "vec.double_ended_model", "trait.iterator", "trait.double_ended"],
            "relation_refs": ["vec.into_iter", "trait.iterator.next", "trait.double_ended.next_back", "iterator.ref_model"],
            "depends_on": ["vec_sequence", "iterator_framework"],
            "meaning": "remaining is prophetic; into_iter_elts(i) is an uninterpreted, non-prophetic observation of the iterator value/state i. peek/peek_back use that observation. obeys_prophetic_iter_laws is true for IntoIter; will_return_none and decrease remain uninterpreted.",
            "source_bridge_required": "Vec::into_iter establishes remaining(i0) == vec@ == into_iter_elts(i0) and decrease(i0) is Some. next/next_back change remaining, but give no equation for into_iter_elts(i1). Neither frozen-original contents nor elts(i1)==remaining(i1) is an invariant supplied by vstd. as_slice/as_mut_slice/Clone/Default need their own state connections.",
        },
        {
            "id": "borrowed_iterator_state", "status": "official_state_relative_spec_functions_not_View",
            "domain": "core::slice::Iter<'a,T> and IterMut<'a,T>",
            "definition_refs": ["slice.iter_type", "slice.into_iter_elts", "slice.iterator_model", "slice.iter_mut_type", "slice.iter_mut_model"],
            "relation_refs": ["vec.ref_into_iter", "slice.iter", "slice.ref_into_iter", "slice.iter_mut"],
            "depends_on": ["slice_sequence", "iterator_framework"],
            "meaning": "Iter remaining is Seq<&T>; constructor elts == remaining.unref(). IterMut remaining is Seq<&mut T>; slice::iter_mut relates each reference's initial/final value to the corresponding slice slot.",
            "source_bridge_required": "The shared Vec IntoIterator impl is directly assumed. &mut Vec IntoIterator is not: its source delegates through DerefMut to slice::iter_mut. Do not confuse that with the deref-visible method vec.iter_mut(), which is not a Vec-owned target.",
        },
        {
            "id": "collection_constructor", "status": "official_trait_specialization_with_opaque_input_observation",
            "domain": "FromIterator<T> for Vec<T> (Global, exactly as in the source); input I: IntoIterator<Item=T>",
            "definition_refs": ["trait.from_iterator", "vec.from_iter_model", "iterator.into_iter_remaining"],
            "relation_refs": ["trait.from_iterator.from_iter", "iterator.from_iter_axiom", "trait.iterator.collect"],
            "depends_on": ["vec_sequence", "iterator_framework"],
            "meaning": "from_iter ensures result@ == into_iter_remaining(input). The supplied axiom relates this UF to remaining only for inputs that are themselves Iterator + IteratorSpec; it is not in group_iter_axioms.",
            "source_bridge_required": "For arbitrary IntoIterator inputs, do not silently replace into_iter_remaining(input) by remaining(input.into_iter()) or Vec input contents. collect's conditional trait contract is a separate route. No allocator-general FromIterator impl is present in the source target.",
        },
        {
            "id": "clone_relation", "status": "official_weak_relational_model",
            "domain": "T: Clone, without Copy/Eq/DeepView/'static strengthening",
            "definition_refs": ["trait.clone", "clone.strictly_cloned", "clone.cloned"],
            "relation_refs": ["vec.clone", "vec.resize", "vec.extend_from_slice", "vec.from_elem"],
            "depends_on": ["vec_sequence"],
            "meaning": "cloned(a,b) = call_ensures(T::clone, (&a,), b) || a == b. Generic Clone::clone has no postcondition; element equality and Clone/callback side-effect traces are not supplied.",
            "source_bridge_required": "Preserve the reflexive weak relation and allocator.clone requirements; do not upgrade it to element equality or erase stateful Clone behavior.",
        },
        {
            "id": "comparison_relation", "status": "official_conditional_trait_model",
            "domain": "T: PartialEq<U>; Vec operands may have distinct A1/A2",
            "definition_refs": ["trait.partial_eq", "vec.eq_model", "slice.eq_model"],
            "relation_refs": ["vec.eq", "trait.partial_eq.eq", "trait.partial_eq.ne", "slice.eq", "vec.eq_law", "vec.view_eq_law", "vec.deep_eq_law"],
            "depends_on": ["vec_sequence", "slice_sequence"],
            "meaning": "Vec-to-Vec eq/ne use T::obeys_eq_spec and pointwise T::eq_spec. The explicit eq assume has no own ensures. Other Vec/Cow/slice/array pairings have only their generic trait contract, not this concrete model. The three law/view-equality proof helpers are Global-only and do not strengthen the A1/A2-generic method contracts.",
            "source_bridge_required": "Do not infer structural equality unconditionally, collapse allocators, or apply ne.default_ensures to the source's explicit ne implementations. Vec Ord/PartialOrd have no concrete comparison model here.",
        },
        {
            "id": "cow_slice_sequence", "status": "official_view_with_narrower_type_domain",
            "domain": "Cow<'a,[T]> View requires T: View + Clone; DeepView requires T: DeepView + Clone",
            "definition_refs": ["cow.type", "cow.slice_view", "cow.slice_deep_view"],
            "relation_refs": [],
            "depends_on": ["vec_sequence", "slice_sequence"],
            "meaning": "Both Borrowed and Owned branches map to the contained sequence; the sequence view alone forgets the variant. The enum type registration is not an API conversion specification.",
            "source_bridge_required": "Source Cow conversions require Clone / ToOwned, not T: View or DeepView. Preserve the full source type domain and variant/borrowing relation; do not add those extra bounds merely to use the official view.",
        },
        {
            "id": "array_box_string_adapters", "status": "official_indirect_dependencies",
            "domain": "arrays [T;N], Box<[T],A>::into_vec, str bytes",
            "definition_refs": ["array.view", "array.view_definition", "box.view", "string.byte_model"],
            "relation_refs": ["array.coercion", "array.as_slice", "box.into_vec", "box.new", "string.as_bytes"],
            "depends_on": ["vec_sequence", "slice_sequence"],
            "meaning": "Box into_vec has an A: Allocator signature; the literal View-for-Box impl in view.rs is default-allocator only, with borrowed/deref observations also available. str::as_bytes returns UTF-8 bytes, not char count.",
            "source_bridge_required": "These are different identities from Vec/Cow/Box From and array TryFrom. slice_to_vec<T:Copy> is a vstd wrapper, not a spec for source Clone-generic From<&[T]> or slice::to_vec.",
        },
        {
            "id": "drain_regions", "status": "missing_official_concrete_view",
            "domain": "Drain<'a,T,A> with source lifetime and allocator domain intact",
            "definition_refs": [], "relation_refs": ["trait.iterator.next", "trait.double_ended.next_back"],
            "depends_on": ["vec_sequence", "slice_sequence", "borrowed_iterator_state"],
            "meaning": "No active Drain name, external type, constructor spec or concrete iterator-law specialization in this official vstd.",
            "source_bridge_required": "Connect Vec::drain to head/remaining/tail and moved-out T values; track tail restoration by real Drop separately from borrow final. forget may skip cleanup. Generic guarded Iterator laws do not establish this connection.",
        },
        {
            "id": "extract_regions", "status": "missing_official_concrete_view",
            "domain": "ExtractIf<'a,T,F,A>, F: FnMut(&mut T)->bool",
            "definition_refs": [], "relation_refs": ["trait.iterator.next", "trait.fn_mut"],
            "depends_on": ["vec_sequence", "slice_sequence"],
            "meaning": "No active ExtractIf name, type/constructor spec or concrete iterator model.",
            "source_bridge_required": "Connect vec/idx/end/del/old_len/pred to retained, removed, unvisited and out-of-range regions; preserve mutable element/predicate state, order, panic and lazy Drop behavior.",
        },
        {
            "id": "splice_regions", "status": "missing_official_concrete_view",
            "domain": "Splice<'a,I,A>, I: Iterator",
            "definition_refs": [], "relation_refs": ["trait.iterator.next", "trait.double_ended.next_back"],
            "depends_on": ["drain_regions", "collection_constructor", "owned_iterator_state"],
            "meaning": "No active Splice name, type/constructor spec or concrete iterator model. ExactSizeIterator::len remains an inherited generic contract, not a new source-owned API.",
            "source_bridge_required": "Relate Drain regions and replace_with state at construction; replacement is consumed during Drop, including fill/move-tail/temporary-Vec paths. final does not prove Drop; forgotten Splice has weaker removal semantics.",
        },
        {
            "id": "allocation_and_callbacks", "status": "source_bridge_not_supplied_by_sequence_views",
            "domain": "allocator, RawVec, initialized/spare regions, raw pointers, callbacks and destructors",
            "definition_refs": ["trait.allocator", "trait.fn_once", "trait.fn_mut", "trait.hash"],
            "relation_refs": ["manually_drop.new", "manually_drop.deref"],
            "depends_on": ["vec_sequence"],
            "meaning": "Type-level trait registration and Seq abstractions are not capacity/layout/ownership/lifecycle or callback-state specifications.",
            "source_bridge_required": "Retain private source specialization/guards as proof dependencies. No API acceptance, new view axiom, synthetic lifecycle machine or source rewrite is performed by this inventory.",
        },
    ]


SUBMODULE_VIEWS = {
    "mod": ["vec_sequence", "slice_sequence", "index_domain", "owned_iterator_state",
            "borrowed_iterator_state", "collection_constructor", "clone_relation",
            "comparison_relation", "array_box_string_adapters", "drain_regions",
            "extract_regions", "splice_regions", "allocation_and_callbacks"],
    "into_iter": ["owned_iterator_state", "slice_sequence", "clone_relation", "allocation_and_callbacks"],
    "drain": ["drain_regions", "slice_sequence", "allocation_and_callbacks"],
    "extract_if": ["extract_regions", "allocation_and_callbacks"],
    "splice": ["splice_regions", "drain_regions", "collection_constructor", "allocation_and_callbacks"],
    "cow": ["cow_slice_sequence", "vec_sequence", "slice_sequence", "collection_constructor"],
    "partial_eq": ["comparison_relation", "cow_slice_sequence", "array_box_string_adapters"],
    "peek_mut": ["vec_sequence", "slice_sequence"],
    "spec_from_elem": ["vec_sequence", "clone_relation", "allocation_and_callbacks"],
    "is_zero": ["allocation_and_callbacks"],
    "spec_extend": ["vec_sequence", "owned_iterator_state", "clone_relation", "allocation_and_callbacks"],
    "spec_from_iter": ["collection_constructor", "owned_iterator_state", "allocation_and_callbacks"],
    "spec_from_iter_nested": ["collection_constructor", "owned_iterator_state", "allocation_and_callbacks"],
    "in_place_collect": ["collection_constructor", "owned_iterator_state", "allocation_and_callbacks"],
    "in_place_drop": ["owned_iterator_state", "allocation_and_callbacks"],
    "set_len_on_drop": ["vec_sequence", "clone_relation", "allocation_and_callbacks"],
}


def trait_base(trait):
    return trait.split("<", 1)[0] if trait else None


def framework_substitution(api):
    trait = api["canonical_trait"]
    substitution = {"Self": api["canonical_owner"]}
    base = trait_base(trait)
    parameters = {
        "core::cmp::PartialEq": "trait.Rhs",
        "core::cmp::PartialOrd": "trait.Rhs",
        "core::ops::Index": "trait.Idx",
        "core::ops::IndexMut": "trait.Idx",
        "core::convert::From": "trait.T",
        "core::convert::TryFrom": "trait.T",
        "core::iter::FromIterator": "trait.A",
    }
    if base in parameters:
        argument = trait[trait.index("<") + 1:-1] if "<" in trait else api["canonical_owner"]
        substitution[parameters[base]] = argument
    if base == "core::iter::FromIterator":
        require(api["method_generic_parameters"].startswith("<I:"), "unexpected source FromIterator method generic")
        substitution["method.T"] = "I"
    for item in api["associated_items"]:
        match = re.fullmatch(r"type\s+(\w+)\s*=\s*(.*);", compact(item["text"]))
        if match:
            substitution["Self::" + match[1]] = match[2]
    return substitution


def source_dependencies(api):
    """Only resolved collection/borrow/delegation edges, never method-name guesses."""
    module, method = api["source_module"], api["method"]
    calls = api["direct_calls"]
    result = []

    def edge(refs, relation, callees=()):
        result.append({
            "evidence_refs": list(refs),
            "source_relation": relation,
            "source": api["source"],
            "recorded_calls": [c for c in calls if c["callee_syntax"] in callees],
            "transfers_target_contract": False,
        })

    if module == "mod":
        resolved = {
            "self.len": "vec.len", "me.len": "vec.len", "other.len": "vec.len",
            "vec.len": "vec.len", "self.as_slice": "vec.as_slice",
            "other.as_slice": "vec.as_slice", "source.as_slice": "vec.as_slice",
            "self.as_mut_slice": "vec.as_mut_slice", "self.pop": "vec.pop",
            "self.truncate": "vec.truncate", "self.reserve": "vec.reserve",
            "Vec::new": "vec.new", "Vec::with_capacity_in": "vec.with_capacity_in",
            "Self::with_capacity_in": "vec.with_capacity_in",
            "ManuallyDrop::new": "manually_drop.new",
        }
        for syntax, ref in resolved.items():
            if any(c["callee_syntax"] == syntax for c in calls):
                edge([ref], "Resolved Vec/ManuallyDrop callee in the source body; not an external spec for the caller.", [syntax])
        if api["canonical_trait"] == "core::convert::AsRef<[T]>":
            edge(["vec.deref", "vec.as_slice"], "The source returns self and coerces &Vec to &[T] through Deref. AsRef is a different trait identity.")
        if api["canonical_trait"] == "core::convert::AsMut<[T]>":
            edge(["vec.deref_mut", "vec.as_mut_slice"], "The source returns self and coerces &mut Vec to &mut [T] through DerefMut. AsMut is a different trait identity.")
        if method == "into_iter" and api["canonical_owner"].startswith("&"):
            mutable = "mut " in api["canonical_owner"]
            edge(["vec.deref_mut" if mutable else "vec.deref",
                  "slice.iter_mut" if mutable else "slice.iter"],
                 "Deref-visible slice iterator constructor, not an interchangeable Vec IntoIterator binding.",
                 ["self.iter_mut" if mutable else "self.iter"])
        if method == "index":
            edge(["vec.deref", "slice.index", "trait.slice_index.index"],
                 "Index::index(&**self,index) delegates to slice indexing.", ["Index::index"])
        if method == "index_mut":
            edge(["vec.deref_mut", "slice.index_mut", "trait.slice_index.index_mut"],
                 "IndexMut::index_mut(&mut **self,index) requires a source bridge for general I.", ["IndexMut::index_mut"])
        if method == "pop_if":
            edge(["vec.deref_mut", "slice.last_mut", "vec.pop"],
                 "The predicate uses a mutable last-element borrow and conditionally calls Vec::pop.",
                 ["self.last_mut", "self.pop"])
        if method == "drain":
            edge(["slice.iter", "range.bounds"],
                 "The source constructs a slice iterator over the removed interval. RangeBounds models are not a spec for core::slice::range or Vec::drain.",
                 ["range_slice.iter", "slice::range"])
        if method == "splice":
            edge(["trait.into_iterator.into_iter"],
                 "replace_with.into_iter has only the generic IntoIterator declaration for arbitrary input; Vec::drain itself has no direct contract.",
                 ["replace_with.into_iter"])
        if method in ("extend", "from_iter"):
            edge(["trait.into_iterator.into_iter"],
                 "The input's IntoIterator conversion precedes private SpecExtend/SpecFromIter dispatch.",
                 ["iter.into_iter"])
        if method == "dedup":
            edge(["trait.partial_eq.eq"],
                 "The source predicate passed to dedup_by uses T::PartialEq; this does not specify dedup itself.")
        if method == "from":
            trait = api["canonical_trait"]
            if "From<alloc::boxed::Box<[T], A>>" in trait or "From<[T; N]>" in trait:
                refs = ["box.into_vec"]
                if "From<[T; N]>" in trait:
                    refs += ["box.new", "array.coercion"]
                edge(refs, "The source delegates to allocator-generic <[T]>::into_vec; Vec::From has a distinct identity.",
                     ["s.into_vec", "<[T]>::into_vec", "Box::new"])
            if "From<&[T; N]>" in trait:
                edge(["array.as_slice"], "Array-to-slice conversion is specified; the following Vec::From<&[T]> is not concretely specialized.",
                     ["s.as_slice"])
            if "From<&str>" in trait:
                edge(["string.as_bytes"], "UTF-8 slice conversion precedes Vec::From<&[u8]>; only the former has a concrete contract.", ["s.as_bytes"])
    elif module == "cow":
        if method == "from_iter":
            edge(["trait.from_iterator.from_iter", "vec.from_iter_model"],
                 "Cow::Owned wraps Vec::from_iter in the source; no Cow FromIteratorSpecImpl connects the result.",
                 ["FromIterator::from_iter"])
        if any(c["callee_syntax"] == "v.as_slice" for c in calls):
            edge(["vec.as_slice"], "The borrowed Cow constructor calls Vec::as_slice before choosing Cow::Borrowed.", ["v.as_slice"])
    elif module == "into_iter":
        if method in ("as_slice", "count"):
            edge(["trait.exact_size.len", "vec.iterator_model"],
                 "self.len is inherited ExactSizeIterator::len, not a source-owned IntoIter API; exact_len has no concrete IntoIter definition.",
                 ["self.len"])
        if method == "last":
            edge(["trait.double_ended.next_back", "vec.iterator_model"],
                 "The source's last calls the specified next_back; last has no method contract of its own.", ["self.next_back"])
        if method == "default":
            edge(["vec.new_in", "trait.default.default", "vec.into_iter"],
                 "The source constructs Vec::new_in(A::default()).into_iter(); generic Default::default itself has no ensures.",
                 ["super::Vec::new_in", "Default::default", "super::Vec::new_in(Default::default()).into_iter"])
        if method == "clone":
            edge(["vec.into_iter", "trait.clone.clone"],
                 "The source clones the allocator and builds a Vec from the remaining slice before into_iter; IntoIter::clone has no concrete content spec.",
                 ["self.as_slice().to_vec_in(self.alloc.deref().clone()).into_iter", "self.alloc.deref().clone"])
    elif module == "drain":
        if method in ("next", "next_back"):
            edge(["trait.iterator.next" if method == "next" else "trait.double_ended.next_back", "slice.iterator_model"],
                 "The inner slice iterator is specified, but ptr::read and the Drain/Vec partition correspondence are still unconnected.",
                 ["self.iter." + method])
        if method == "drop":
            edge(["vec.len", "vec.truncate"],
                 "Vec observers/truncate in the ZST cleanup path do not provide a Drain Drop/lifecycle contract.",
                 ["vec.len", "vec.truncate"])
    elif module == "splice" and method == "drop":
        edge(["trait.iterator.collect", "vec.from_iter_model", "vec.into_iter", "vec.len"],
             "The extra replacement path collects into Vec then into_iter; Splice's deferred replacement/Drain Drop relation remains absent.",
             ["self.replace_with.by_ref().collect::<Vec<I::Item>>",
              "self.replace_with.by_ref().collect::<Vec<I::Item>>().into_iter", "collected.len"])
    elif module == "partial_eq":
        edge(["slice.eq_model", "trait.partial_eq." + method, "slice.index"],
             "The macro's self[..] and other[..] compare slices; this is a delegation obligation, not a specialization for the original owner/Rhs pairing.")
    return result


def api_views(api):
    module = api["source_module"]
    method = api["method"]
    if module == "cow":
        return ["cow_slice_sequence", "vec_sequence", "slice_sequence"] + (
            ["collection_constructor"] if method == "from_iter" else [])
    if module == "into_iter":
        refs = ["owned_iterator_state"]
        if method in ("as_slice", "as_mut_slice", "as_ref", "clone", "fmt"):
            refs.append("slice_sequence")
        if method == "clone":
            refs.append("clone_relation")
        if method in ("fold", "try_fold", "default", "drop", "fmt"):
            refs.append("allocation_and_callbacks")
        return refs
    if module not in ("mod", "partial_eq"):
        return SUBMODULE_VIEWS[module]
    if module == "partial_eq":
        refs = ["comparison_relation", "slice_sequence"]
        if "Cow" in api["canonical_id"]:
            refs.append("cow_slice_sequence")
        if "Vec" in api["canonical_id"]:
            refs.append("vec_sequence")
        if "; N]" in api["canonical_id"]:
            refs.append("array_box_string_adapters")
        return refs
    refs = ["vec_sequence"]
    method, trait = api["method"], trait_base(api["canonical_trait"])
    if method in ("as_slice", "as_mut_slice", "deref", "deref_mut", "as_ref", "as_mut", "leak"):
        refs.append("slice_sequence")
    if method in ("index", "index_mut"):
        refs += ["slice_sequence", "index_domain"]
    if method == "into_iter":
        refs.append("borrowed_iterator_state" if api["canonical_owner"].startswith("&") else "owned_iterator_state")
    if method in ("from_iter", "extend"):
        refs.append("collection_constructor")
    if method in ("clone", "clone_from", "resize", "extend_from_slice", "extend_from_within", "from_elem"):
        refs.append("clone_relation")
    if method in ("eq", "ne", "partial_cmp", "cmp", "dedup", "dedup_by", "dedup_by_key"):
        refs.append("comparison_relation")
    if method in ("drain", "extract_if", "splice"):
        refs.append({"drain": "drain_regions", "extract_if": "extract_regions", "splice": "splice_regions"}[method])
    if trait in ("core::convert::From", "core::convert::TryFrom"):
        refs.append("array_box_string_adapters")
    if "Cow" in api["canonical_id"]:
        refs.append("cow_slice_sequence")
    if method in ("capacity", "reserve", "try_reserve", "reserve_exact", "try_reserve_exact",
                  "shrink_to_fit", "shrink_to", "with_capacity", "into_raw_parts", "from_raw_parts",
                  "as_ptr", "as_mut_ptr", "set_len", "spare_capacity_mut", "retain", "retain_mut",
                  "extract_if", "drop", "hash", "fmt", "resize_with", "into_flattened", "push_mut", "insert_mut"):
        refs.append("allocation_and_callbacks")
    return list(dict.fromkeys(refs))


def map_api(api, direct, trait_methods):
    row = {k: api[k] for k in IDENTITY_FIELDS}
    canonical, module, method = api["canonical_id"], api["source_module"], api["method"]
    trait = trait_base(api["canonical_trait"])
    framework = trait_methods.get((trait, method))
    direct_refs = [direct[canonical]] if canonical in direct else []
    specializations = []
    hooks = []
    notes = []
    if module == "partial_eq" and api["canonical_owner"] == "alloc::vec::Vec<T, A1>" and api["canonical_trait"] == "core::cmp::PartialEq<alloc::vec::Vec<U, A2>>":
        specializations.append("vec.eq_model")
        notes.append("Conditional T::obeys_eq_spec; preserve T:PartialEq<U> and independent A1/A2. The explicit eq assume adds no postcondition.")
    if module == "into_iter" and method in ("next", "next_back"):
        specializations.append("vec.iterator_model")
        if method == "next_back":
            specializations.append("vec.double_ended_model")
        notes.append("Concrete obeys_prophetic_iter_laws=true makes the generic remaining transition usable; no transition for into_iter_elts is supplied.")
    if canonical == "<alloc::vec::Vec<T> as core::iter::FromIterator<T>>::from_iter":
        specializations.append("vec.from_iter_model")
        notes.append("Global-only matches the source impl exactly. Result sequence equals opaque into_iter_remaining for arbitrary IntoIterator input; a separate axiom connects Iterator inputs to remaining.")
    if trait in ("core::ops::Index", "core::ops::IndexMut") and module == "mod":
        specializations.append("vec.index_model")
        hooks.append("vec.index_usize" if method == "index" else "vec.index_mut_usize")
        notes.append("Do not count the compiler hook as a second API or an external UFCS declaration.")
    dependencies = source_dependencies(api)
    if direct_refs:
        coverage = "exact"
        mechanism = "assume_specification"
    elif specializations and method in ("eq", "ne", "next", "next_back", "from_iter"):
        coverage = "exact"
        mechanism = "generic_trait_contract_with_concrete_spec_impl"
    elif hooks:
        coverage = "partial"
        mechanism = "usize_compiler_index_mut_hook_plus_generic_precondition"
    elif framework:
        coverage = "trait_only"
        mechanism = "generic_trait_method_without_concrete_spec_impl"
    elif dependencies:
        coverage = "indirect"
        mechanism = "other_identity_delegation_only"
    else:
        coverage = "none"
        mechanism = "no_method_contract_or_resolved_contract_delegation"

    domain_notes = []
    if coverage == "partial":
        domain_notes.append("Source I:SliceIndex<[T]> is not restricted to usize. Content/writeback is only supplied by the usize operator hook; general I and explicit IndexMut UFCS only have index_req, no ensures.")
    if method == "push" and module == "mod":
        domain_notes.append("Source const impl has A:[const] Allocator+[const] Destruct; official exec spec has A:Allocator. Runtime signature is retained; no const-evaluation coverage is claimed.")
    if "cow_slice_sequence" in api_views(api):
        domain_notes.append("Official Cow<[T]> View/DeepView adds T:View/DeepView beyond the source Clone/ToOwned domain; not imposed on this API row.")
    if coverage == "exact":
        domain_notes.append("Exact refers to the executable type/generic/lifetime signature binding, not value-domain completeness, panic semantics, or strength of the ensures.")
    if coverage == "trait_only":
        notes.append("A generic method declaration is present, but no official concrete content/observation model for this owner and trait arguments is established.")
    if method in ("default", "clone", "into_iter") and coverage == "trait_only":
        notes.append("This generic declaration has no ensures; source delegation must not be silently promoted to its contract.")
    if module == "partial_eq" and method == "ne":
        notes.append("default_ensures in ExPartialEq::ne describes the provided default, not this source-owned explicit implementation.")
    if method == "fmt":
        notes.append("Debug's macro-instantiated generic contract requires fmt_req and has no result/Formatter postcondition; derive(Debug) does not add one.")
    if method in ("from", "try_from") and framework:
        notes.append("obeys_from_spec/obeys_try_from_spec and the conversion model have no matching Vec/Cow/Box/array concrete specialization. Integer and Into/TryInto blanket specs are different bindings.")
    if method in ("partial_cmp", "cmp") and module == "mod":
        notes.append("Only the conditional PartialOrd/Ord framework; no Vec lexicographic concrete model.")
    if method in ("reserve", "try_reserve", "with_capacity") and module == "mod":
        notes.append("Only sequence contents/emptiness are constrained; no capacity/allocation relation. try_reserve does not constrain the Result variant or error.")
    if "clone_relation" in api_views(api):
        notes.append("cloned is a reflexive call_ensures relation, not unconditional equality or a callback-state trace.")
    if module in ("drain", "extract_if", "splice"):
        notes.append("No official concrete type/view/constructor relation for this iterator; generic guarded laws do not prove an obeys predicate or cleanup semantics.")
    if method in ("size_hint", "count", "last", "fold", "try_fold") and trait == "core::iter::Iterator":
        notes.append("ExIterator does not declare this method. Contracts for next/collect or inherited len are not contracts for this explicit source implementation.")
    if method == "hash":
        notes.append("ExHash only registers the trait type; it contains no hash method specification.")
    if method == "clone_from":
        notes.append("The only generic external_fn_specification for clone_from is inside a block comment; ExClone declares only clone.")
    if method in ("as_ref", "as_mut"):
        notes.append("No active AsRef/AsMut token or external trait/function contract in official vstd. Vec/slice target arguments remain distinct.")
    if method == "drop":
        notes.append("No Drop contract; borrow final cannot stand in for destructor execution.")

    exact_binding = None
    if coverage in ("exact", "partial"):
        exact_binding = {
            "canonical_owner": api["canonical_owner"],
            "canonical_trait": api["canonical_trait"],
            "method": method,
            "canonical_id": canonical,
            "domain_relation": "full_runtime_signature" if coverage == "exact" else "proper_subdomain_and_call_form",
        }
    row.update(
        coverage_class=coverage, mechanism=mechanism, canonical_binding=exact_binding,
        direct_spec_refs=direct_refs, trait_contract_refs=[framework] if framework else [],
        concrete_spec_impl_refs=specializations, compiler_hook_refs=hooks,
        indirect_dependencies=dependencies, view_dependencies=api_views(api),
        signature_domain={
            "relation": "full_runtime_signature" if coverage == "exact" else
                        "partial_runtime_signature_or_call_form" if coverage == "partial" else
                        "framework_only" if coverage == "trait_only" else "not_bound",
            "notes": domain_notes,
            "extra_bounds_added_by_inventory": [],
        },
        contract_limitations=notes,
        source_calls_input_ref={"path": "inventory/source_api.json", "canonical_id": canonical, "key": "direct_calls"},
        trait_instantiations=[{
            "contract_ref": framework, "self": api["canonical_owner"],
            "trait": api["canonical_trait"], "method": method,
            "generic_substitution": framework_substitution(api),
            "source_impl_generic_parameters": api["impl_generic_parameters"],
            "source_method_generic_parameters": api["method_generic_parameters"],
            "default_ensures_applies": False,
        }] if framework else [],
        source_correctness="not_assessed", specification_completeness="not_assessed",
        external_spec_policy=(
            "Do not duplicate the exact official assume_specification target." if direct_refs else
            "Use/preserve the existing trait specialization; do not add a duplicate target assumption." if coverage == "exact" else
            "No generic Vec IndexMut assumption exists; preserve the trait precondition and existing usize hook." if coverage == "partial" else
            "No exact target assumption found; any future spec must respect generic contracts and impls_cannot_extend_spec."
        ),
    )
    return row


def counts_by_class(rows):
    counts = Counter(r["coverage_class"] for r in rows)
    return {key: counts[key] for key in CLASSES}


def annotate_evidence(tree, direct):
    for canonical, ref in direct.items():
        tree.evidence[ref]["canonical_target"] = canonical
        tree.evidence[ref]["target_resolution"] = "source-owned UFCS identity; alloc/core aliases resolved, trait arguments retained"
    for record in tree.evidence.values():
        source = record["source"]
        path = source["path"].removeprefix("toolchains/upstream/source/vstd/")
        lines = tree.texts[path].splitlines(keepends=True)
        before = source["start_line"] - 2
        attrs = []
        while before >= 0 and lines[before].lstrip().startswith("#["):
            start = len("".join(lines[:before]))
            attrs.insert(0, tree.fragment(path, start, start + len(lines[before].rstrip("\n"))))
            before -= 1
        record["preceding_attribute_refs"] = attrs
    text = tree.texts["std_specs/clone.rs"]
    code = tree.code["std_specs/clone.rs"]
    inactive = []
    for n, match in enumerate(re.finditer(r"#\[verifier::external_fn_specification\]", text), 1):
        require(not code[match.start():match.end()].strip(), "unexpected active external_fn_specification")
        start = text.rfind("/*", 0, match.start())
        end = text.index("*/", match.end()) + 2
        name = f"clone.inactive_external_fn_{n}"
        tree.add(name, tree.fragment("std_specs/clone.rs", start, end), kind="commented_out_not_a_declaration")
        inactive.append(name)
    return inactive


def inherited_relations(source, trait_methods):
    rows = []
    for method in source["inherited_trait_methods"]:
        ref = trait_methods.get((trait_base(method["trait"]), method["method"]))
        models = []
        if method["owner"].startswith("alloc::vec::IntoIter") and ref:
            models.append("vec.iterator_model")
        rows.append({
            "canonical_id": method["canonical_id"], "owner": method["owner"],
            "trait": method["trait"], "method": method["method"],
            "source": method["source"], "impl_source": method["impl_source"],
            "stability": method["stability"], "included_in_api_count": False,
            "trait_contract_refs": [ref] if ref else [],
            "concrete_spec_impl_refs": models,
            "default_ensures_applies": bool(ref and method["provided"]),
            "note": "Read from input inherited_trait_methods; not re-enumerated or promoted to a module-owned implementation.",
        })
    return rows


def validate(data, source, tree):
    rows = data["apis"]
    require([r["canonical_id"] for r in rows] == [r["canonical_id"] for r in source["apis"]],
            "API order/identity differs from source input")
    for row, original in zip(rows, source["apis"]):
        require(all(row[k] == original[k] for k in IDENTITY_FIELDS), "source identity/domain changed")
        require(row["coverage_class"] in CLASSES, "unknown coverage class")
        require(not row["signature_domain"]["extra_bounds_added_by_inventory"], "added source-domain bounds")
        refs = row["direct_spec_refs"] + row["trait_contract_refs"] + row["concrete_spec_impl_refs"] + row["compiler_hook_refs"]
        for edge in row["indirect_dependencies"]:
            refs += edge["evidence_refs"]
        require(all(ref in tree.evidence for ref in refs), f"dangling API evidence: {row['canonical_id']}")
    claims = [ref for r in rows for ref in r["direct_spec_refs"]]
    require(len(claims) == len(set(claims)), "duplicate external specification claim")
    for row in rows:
        for ref in row["direct_spec_refs"]:
            require(tree.evidence[ref].get("canonical_target") == row["canonical_id"],
                    f"canonical target mismatch: {ref} -> {row['canonical_id']}")
        for instance in row["trait_instantiations"]:
            require(instance["self"] == row["canonical_owner"] and instance["trait"] == row["canonical_trait"],
                    "trait instantiation identity mismatch")
    claimed_spans = [tuple(tree.evidence[r]["source"].values()) for r in claims]
    require(len(claimed_spans) == len(set(claimed_spans)), "same declaration claimed under two evidence ids")
    for record in tree.evidence.values():
        require(all(ref in tree.evidence for ref in record.get("support_refs", [])),
                f"dangling supporting evidence: {record['id']}")
    vec_declarations = [r for r in tree.assumptions if r["source"]["path"].endswith("/std_specs/vec.rs")]
    accounted = claims + ["vec.new_in", "vec.with_capacity_in"]
    require(len(vec_declarations) == len(accounted), "unaccounted official Vec assumed specification")
    require({r["sha256"] for r in vec_declarations} == {tree.evidence[r]["sha256"] for r in accounted},
            "official Vec declaration identity accounting differs")
    available = set()
    for view in data["views"]:
        require(set(view["depends_on"]) <= available, "views must precede their dependencies' users")
        require(all(r in tree.evidence for r in view["definition_refs"] + view["relation_refs"]), "dangling view evidence")
        available.add(view["id"])
    require(all(set(row["view_dependencies"]) <= available for row in rows), "unknown per-API view")
    require(set(SUBMODULE_VIEWS) == {Path(f["path"]).stem for f in source["source_files"]},
            "source submodule map mismatch")
    require(sum(data["counts"]["by_coverage_class"].values()) == len(rows), "coverage partition mismatch")
    require(len(data["inherited_framework_relations"]) == len(source["inherited_trait_methods"]),
            "inherited instance accounting mismatch")
    for symbol in ("AsRef", "AsMut", "Drain", "ExtractIf", "Splice"):
        require(not tree.symbol_occurrences(symbol), f"new relevant official symbol requires mapping: {symbol}")


def build():
    source = load_source()
    tree = OfficialTree()
    direct, trait_methods = collect_evidence(tree)
    inactive = annotate_evidence(tree, direct)
    apis = [map_api(api, direct, trait_methods) for api in source["apis"]]
    source_ids = {a["canonical_id"] for a in source["apis"]}
    require(set(direct) <= source_ids, "unmatched direct binding identity")
    version_path = PROJECT / "toolchains/verus-x86-linux/version.json"
    version = json.loads(version_path.read_text())["verus"]
    require(version["commit"] == COMMIT, "binary commit does not match the required baseline")
    require(version["version"] == TAG.removeprefix("release/"), "binary tag/version mismatch")
    submodules = []
    for file in source["source_files"]:
        module = Path(file["path"]).stem
        selected = [a for a in apis if a["source_module"] == module]
        submodules.append({
            "source_module": module, "source_path": file["path"],
            "stable_api_count": len(selected), "by_coverage_class": counts_by_class(selected),
            "view_dependencies": SUBMODULE_VIEWS[module],
            "private_source_dependencies_are_not_public_targets": not bool(selected),
        })
    excluded_by_id = {r["canonical_id"]: r for r in source["excluded_functions"]}
    non_targets = []
    for method in ("new_in", "with_capacity_in"):
        canonical = f"alloc::vec::Vec<T, A>::{method}"
        require(canonical in excluded_by_id, f"missing source exclusion {canonical}")
        non_targets.append({
            "evidence_ref": "vec." + method, "canonical_id": canonical,
            "source": excluded_by_id[canonical]["source"],
            "reason": excluded_by_id[canonical]["exclusion_reason"],
            "included_in_api_count": False,
        })
    non_targets += [
        {"evidence_ref": "box.into_vec", "canonical_id": "<[T]>::into_vec",
         "reason": "alloc/src/slice.rs inherent method with Box<[T],A> receiver; not Vec::From<Box>.", "included_in_api_count": False},
        {"evidence_ref": "slice.to_vec_wrapper", "canonical_id": "vstd::slice::slice_to_vec<T: Copy>",
         "reason": "Global/Copy-restricted vstd wrapper, not Clone-generic std slice::to_vec or any Vec From identity.", "included_in_api_count": False},
        {"evidence_ref": "vec.extra_exec", "canonical_id": "vstd::pervasive::VecAdditionalExecFns::{set,set_and_swap}",
         "reason": "Custom Global-only trait methods; not std IndexMut specifications.", "included_in_api_count": False},
        {"evidence_ref": "alloc.vec_literal_array", "canonical_id": "alloc::boxed::box_assume_init_into_vec_unsafe",
         "reason": "Compiler/vec! array construction helper outside the 16 source-owned files; distinct from Vec::From<[T;N]> and from_elem.", "included_in_api_count": False},
        {"evidence_ref": "convert.blanket_try_from", "canonical_id": "<T as core::convert::TryFrom<U>>::try_from where U: Into<T>",
         "reason": "Infallible blanket conversion, not the source array TryFrom<Vec<T,A>> with Error=Vec<T,A>.", "included_in_api_count": False},
        {"evidence_ref": "iterator.blanket_into_iter", "canonical_id": "<I as core::iter::IntoIterator>::into_iter where I: Iterator",
         "reason": "Iterator identity blanket, not owned/shared/mutable Vec IntoIterator.", "included_in_api_count": False},
    ]
    data = {
        "schema_version": 1,
        "baseline": {
            "upstream_commit": COMMIT, "upstream_tag": TAG,
            "official_vstd_root": "toolchains/upstream/source/vstd",
            "binary_root": "toolchains/verus-x86-linux", "binary_version_record": version,
            "binary_version_record_sha256": digest(version_path.read_bytes()),
            "official_tree_sha256": digest("".join(f"{f['path']}\0{f['sha256']}\n" for f in tree.files).encode()),
            "provenance_boundary": "User-designated official pinned archive/binary. Asset SHA256 and extraction-byte fidelity checks belong to the parent; this inventory fingerprints the actual read-only tree and checks binary version metadata. No Git or old local vstd is consulted.",
            "source_inventory": [
                {"path": name, "sha256": digest((PROJECT / name).read_bytes())}
                for name in ("inventory/source_api.json", "inventory/source_api.tsv")
            ],
            "semantic_source_library": source["source_library"],
        },
        "scope": {
            "target": "Exactly source_api.json.apis, in the same order; no source inventory reconstruction.",
            "classes": {
                "exact": "Exact executable signature/type/lifetime domain, via an assumed spec or generic method + concrete spec impl. Weak/conditional/opaque clauses are preserved; this is NOT semantic completeness.",
                "partial": "Only a proper type domain or call form has a concrete contract; generic framework clauses may remain for the rest.",
                "trait_only": "The exact trait method has a generic declaration/guarded contract, but no matching concrete owner/trait-argument model. No-ensures declarations are included and identified.",
                "indirect": "No target method contract; only another collection/iterator/borrow/delegation identity has a relevant contract. Not API coverage.",
                "none": "No target method contract or resolved covered collection/delegation edge. Views/type registration/primitive arithmetic are not method coverage.",
            },
            "precedence": list(CLASSES),
            "signature_domain": "Rust executable generics, allocators, lifetimes and receiver/trait arguments retained; const execution and panic-domain completeness are not claimed. Value preconditions remain literal.",
            "dependencies": "Collection/view/constructor/delegation relations, not a whole-program call graph or primitive-operation survey. Original direct_calls remain referenced in source_api.json.",
            "trust": "Existing assumptions, external bodies and axioms are evidence of vstd coverage, never source implementation correctness or spec-determin-tool completeness.",
            "no_new_external_specs": True,
        },
        "input_accounting": source["counts"],
        "counts": {
            "apis": len(apis), "by_coverage_class": counts_by_class(apis),
            "by_submodule": {s["source_module"]: s["by_coverage_class"] for s in submodules},
            "direct_assume_target_claims": sum(bool(a["direct_spec_refs"]) for a in apis),
            "official_vec_assume_declarations": sum(a["source"]["path"].endswith("/std_specs/vec.rs") for a in tree.assumptions),
            "exact_trait_specialized_without_target_assume": sum(a["coverage_class"] == "exact" and not a["direct_spec_refs"] for a in apis),
            "unique_source_files": len(submodules),
            "inherited_instances_not_added": len(source["inherited_trait_methods"]),
        },
        "file_accounting": {
            "all_files": len(tree.files), "rust_files_scanned": len(tree.texts),
            "assume_declarations_or_macro_templates": len(tree.assumptions),
            "macro_templates_not_expanded_or_counted_as_vec_bindings": sum(a["macro_template"] for a in tree.assumptions),
            "active_external_fn_specification_attributes": sum(f.get("active_external_fn_attributes", 0) for f in tree.files),
            "inactive_external_fn_examples": inactive,
            "negative_active_symbol_searches": {s: tree.symbol_occurrences(s) for s in ("AsRef", "AsMut", "Drain", "ExtractIf", "Splice")},
            "vec_into_iter_symbol_files": sorted({r["path"] for s in ("Vec", "IntoIter") for r in tree.symbol_occurrences(s)}),
            "candidate_dispositions": {
                "std_specs/vec.rs": "Every assume is bound once: stable target or explicit unstable exclusion; also contains compiler hooks and concrete trait models.",
                "view.rs": "Vec/DeepView/Box/ref view definitions, not executable Vec API bindings.",
                "std_specs/iter.rs": "Generic and blanket iterator frameworks; no extra source targets.",
                "std_specs/slice.rs": "Only slice/iterator/index/comparison dependencies, never reclassified as Vec identities.",
                "slice.rs": "Slice views/indexing and Copy-only vstd wrapper, not Vec conversion specs.",
                "std_specs/smart_ptrs.rs": "Allocator-generic slice into_vec has Box receiver, not Vec::From<Box>.",
                "std_specs/alloc.rs": "Compiler vec-literal helpers outside source-owned scope.",
                "pervasive.rs": "cloned relation and custom Global-only VecAdditionalExecFns, not std targets.",
                "bytes.rs": "vstd byte-encoding wrappers return Vec; no std Vec target declaration.",
                "string.rs": "String/str declarations and custom byte Vec wrapper, only str::as_bytes relevant as a dependency.",
                "contrib/exec_spec/seq.rs": "Custom execution traits/wrappers using Vec, not std Vec API specifications.",
                "contrib/exec_spec/string.rs": "Custom execution traits and documentation, not std Vec API specifications.",
                "seq.rs": "Vec mention in documentation, no executable Vec target.",
            },
            "files": tree.files,
        },
        "views": view_inventory(),
        "evidence": list(tree.evidence.values()),
        "non_target_relations": non_targets,
        "inherited_framework_relations": inherited_relations(source, trait_methods),
        "submodules": submodules,
        "apis": apis,
        "checks": {
            "source_json_tsv_identity_bijection": True,
            "source_identity_and_domains_preserved": True,
            "all_source_files_accounted_including_zero_target_files": True,
            "official_vec_assume_partition_complete": True,
            "duplicate_external_spec_claims": 0,
            "evidence_is_literal_pinned_source_with_byte_and_line_spans": True,
            "view_dependency_order_checked": True,
            "replay": [
                "PYTHONDONTWRITEBYTECODE=1 python3 scripts/inventory_vstd.py --check",
                "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s inventory/vstd-tests -p 'test_*.py'",
                "PYTHONDONTWRITEBYTECODE=1 python3 inventory/vstd-tests/check_bindings.py",
            ],
            "binding_probe_artifact": "inventory/vstd-tests/binding_results.json",
            "binding_probes_are_not_source_or_completeness_proofs": True,
            "unchanged_source_tests_rerun": False,
        },
    }
    validate(data, source, tree)
    return data


def tsv_text(data):
    output = io.StringIO()
    columns = ["canonical_id", "source_module", "canonical_owner", "canonical_trait", "method",
               "signature", "impl_generic_parameters", "impl_where_clause",
               "method_generic_parameters", "method_where_clause", "source",
               "coverage_class", "mechanism", "direct_spec_refs", "trait_contract_refs",
               "concrete_spec_impl_refs", "compiler_hook_refs", "view_dependencies",
               "indirect_dependencies", "signature_domain", "contract_limitations"]
    writer = csv.DictWriter(output, fieldnames=columns, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for api in data["apis"]:
        row = {key: api[key] for key in columns}
        for key, value in row.items():
            if isinstance(value, (list, dict)):
                row[key] = json.dumps(value, ensure_ascii=False, sort_keys=True)
            elif isinstance(value, str):
                row[key] = compact(value)
        writer.writerow(row)
    return output.getvalue()


def markdown_section(data):
    evidence = {e["id"]: e for e in data["evidence"]}

    def location(ref):
        s = evidence[ref]["source"]
        return f"`{s['path']}:{s['start_line']}-{s['end_line']}`"

    text = [
        BEGIN, "", "## Official pinned vstd views and coverage relations", "",
        f"Baseline: `{TAG}` / `{COMMIT}`; only `toolchains/upstream/source/vstd` is scanned. "
        "Source identities and domains are taken unchanged from `source_api.json` / `.tsv`. "
        "This section is appended by `scripts/inventory_vstd.py`; the source-inventory section above is not rewritten.", "",
        "### Views first (definitions, limitations, constructor relations)", "",
    ]
    for view in data["views"]:
        refs = view["definition_refs"] or view["relation_refs"]
        text += [
            f"#### `{view['id']}`: {view['status']}", "",
            f"Domain: {view['domain']}.",
            f"{view['meaning']}",
            f"Required source/constructor relation: {view['source_bridge_required']}",
            "Definition references: " + ("; ".join(location(r) for r in refs) if refs else "none") + ".",
            "Constructor/relation references: " + ("; ".join(location(r) for r in view["relation_refs"]) if view["relation_refs"] else "none") + ".",
            "Depends on: " + (", ".join(f"`{d}`" for d in view["depends_on"]) or "none") + ".", "",
        ]
    text += [
        "### Coverage classes (not correctness/completeness acceptance)", "",
        "Exact counts signature bindings, including weak/conditional contracts; partial preserves the narrower call/type domain. "
        "Trait-only, indirect and none are not concrete API coverage. No API has been accepted by either proof track here.", "",
        "| Source module | APIs | exact | partial | trait_only | indirect | none |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for module in data["submodules"]:
        c = module["by_coverage_class"]
        text.append(f"| `{module['source_module']}.rs` | {module['stable_api_count']} | " +
                    " | ".join(str(c[k]) for k in CLASSES) + " |")
    c = data["counts"]["by_coverage_class"]
    text += [
        f"| **Total** | **{data['counts']['apis']}** | " + " | ".join(f"**{c[k]}**" for k in CLASSES) + " |", "",
        "### Exact identities that must not be merged", "",
        "| Canonical source identity | Classification | Official relation |",
        "|---|---|---|",
    ]
    for row in data["apis"]:
        if row["source_module"] == "mod" and row["method"] in ("as_ref", "as_mut"):
            refs = [ref for dep in row["indirect_dependencies"] for ref in dep["evidence_refs"]]
            text.append(f"| `{row['canonical_id']}` | `{row['coverage_class']}`; no own spec | " +
                        ("; ".join(location(r) for r in refs) if refs else "none (identity return is source behavior, not a vstd contract)") + " |")
    text += [
        "",
        f"Immutable generic `Index<I>`: {location('vec.index')}, with `IndexSpecImpl` "
        f"{location('vec.index_model')}; the `usize` hook {location('vec.index_usize')} is not another API. "
        f"Mutable `IndexMut<I>` has only the generic precondition {location('trait.index_mut.index_mut')}; "
        f"content/writeback is provided for `usize` operator syntax by {location('vec.index_mut_usize')}, not general I or explicit UFCS.", "",
        f"Do not strengthen `with_capacity`, `reserve`, or `try_reserve`: {location('vec.with_capacity')}, "
        f"{location('vec.reserve')}, {location('vec.try_reserve')} only constrain sequence contents/emptiness; "
        "`try_reserve` leaves the Result variant unconstrained. `cloned` is reflexive call_ensures, not equality.", "",
        f"All {data['file_accounting']['all_files']} official vstd files are fingerprinted; "
        f"{data['file_accounting']['rust_files_scanned']} Rust files are lexically scanned with nested comments/strings excluded. "
        f"{data['file_accounting']['assume_declarations_or_macro_templates']} active assume declarations/templates are scanned "
        "(not a macro-expanded API count). Active external_fn_specification attributes: "
        f"{data['file_accounting']['active_external_fn_specification_attributes']}. "
        "The commented clone_from examples are inactive. All "
        f"{data['counts']['official_vec_assume_declarations']} Vec-file assume declarations are reconciled: "
        f"{data['counts']['direct_assume_target_claims']} stable targets and the two excluded unstable constructors "
        "`new_in` / `with_capacity_in`; no duplicate external-spec claims.", "",
        f"The {data['input_accounting']['excluded_function_candidates']} excluded source candidates and "
        f"{data['input_accounting']['inherited_trait_default_instances']} inherited instances remain outside the "
        f"{data['counts']['apis']} source-owned rows. "
        "The inherited framework relations are copied/mapped from the existing input, not re-enumerated. "
        "Private spec_*/in_place_* modules still appear in the view dependency map with zero public targets.", "",
        "Full literal generics, target, signature, requires/ensures/default_ensures and byte/line ranges are in "
        f"`inventory/vstd_coverage.json` (`evidence`); the {data['counts']['apis']}-row TSV is `inventory/vstd_coverage.tsv`. "
        "Submodule-to-view relations and source constructor/delegation edges precede or accompany every API. "
        "Supplemental binary probes live only in `inventory/vstd-tests`; they are clients of existing assumptions, not implementation or determinism proofs.", "",
        "```sh",
        *data["checks"]["replay"],
        "```", "", END, "",
    ]
    return "\n".join(text)


def update_section(original, section):
    if BEGIN not in original:
        require(END not in original, "orphan coverage end marker")
        gap = "" if original.endswith("\n\n") else "\n" if original.endswith("\n") else "\n\n"
        return original + gap + section
    require(original.count(BEGIN) == original.count(END) == 1, "duplicate/unbalanced coverage markers")
    start, end = original.index(BEGIN), original.index(END) + len(END)
    return original[:start] + section.rstrip("\n") + original[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="regenerate in memory; fail on stale inventory or section")
    args = parser.parse_args()
    data = build()
    artifacts = {
        PROJECT / "inventory/vstd_coverage.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        PROJECT / "inventory/vstd_coverage.tsv": tsv_text(data),
    }
    docs = PROJECT / "inventory/submodules.md"
    artifacts[docs] = update_section(docs.read_text(), markdown_section(data))
    for path, content in artifacts.items():
        if args.check:
            require(path.is_file() and path.read_text() == content, f"stale or missing artifact: {path.relative_to(PROJECT)}")
        else:
            path.write_text(content)
    print(("CHECK PASS" if args.check else "WROTE") +
          f": {data['counts']['apis']} APIs; " +
          ", ".join(f"{k}={v}" for k, v in data["counts"]["by_coverage_class"].items()) +
          "; duplicate external claims=0")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
