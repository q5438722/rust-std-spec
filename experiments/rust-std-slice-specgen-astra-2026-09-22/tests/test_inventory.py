"""Checks against the source tree, rather than a frozen API total."""

import hashlib
import io
import json
from pathlib import Path
import re
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_inventory import (  # noqa: E402
    API_COLUMNS, DEFAULT_CORE, Inventory, PENDING, SelectedVstd, Source,
    VSTD_CLASSES, VSTD_COMMIT, VSTD_RELEASE, VSTD_TREE_SHA256, children, decode,
    encode, impl_parts, lexical_mask, main, nearest, parse, read_tsv, stability,
    visibility,
)


class InventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = Inventory(DEFAULT_CORE).build()
        cls.apis = read_tsv(ROOT / "inventory/apis.tsv")
        cls.excluded = read_tsv(ROOT / "inventory/exclusions.tsv")
        cls.by_id = {r["canonical_id"]: r for r in cls.apis}
        cls.vstd_by_id = {r["canonical_id"]: r for r in cls.inventory.vstd.rows}

    def table(self, name):
        return read_tsv(ROOT / "inventory" / (name + ".tsv"))

    def test_regeneration_matches_persisted_inventory(self):
        self.assertEqual(self.apis, self.inventory.apis)
        self.assertEqual(self.excluded, self.inventory.exclusions)
        self.assertTrue(all(set(row) == set(API_COLUMNS) for row in self.apis))

    def test_primary_source_declarations_are_all_parsed(self):
        for path, source in self.inventory.sources.items():
            if not path.startswith("slice/") and path != "mem/maybe_uninit.rs":
                continue
            nodes = [n for n in self.inventory.nodes if n.source is source]
            macro_regions = [n for n in nodes if n.kind in {"macro", "macro_rules"}
                             or (n.kind == "macro_call" and not nearest(n, {"fn"}))]
            declarations = [
                m for m in re.finditer(r"\bfn\s+([A-Za-z_]\w*)\s*(?:<|\()", source.mask)
                if not any(n.start <= m.start() < n.end for n in macro_regions)
            ]
            parsed = [n for n in nodes if n.kind == "fn"]
            self.assertEqual(len(parsed), len(declarations), path)
            for declaration in declarations:
                self.assertEqual(
                    sum(n.start <= declaration.start() < n.head_end for n in parsed), 1,
                    (path, declaration[1]),
                )
        owned_functions = [n for n in self.inventory.owned_nodes if n.kind == "fn"]
        rows = [r for r in self.apis + self.excluded if r["kind"] != "derived-method"]
        self.assertEqual(len(rows), len(owned_functions))

    def test_six_observers_have_exact_source_signatures(self):
        names = ("len", "is_empty", "first", "split_first", "split_last", "last")
        for name in names:
            row = self.by_id[f"<[T]>::{name}"]
            declaration = next(n for n in self.inventory.owned_nodes if n.kind == "fn"
                               and n.name == name and n.source.path == "slice/mod.rs"
                               and nearest(n, {"impl"})
                               and impl_parts(nearest(n, {"impl"}))[1:3] == ("", "[T]"))
            self.assertEqual(row["signature"], declaration.header)
            self.assertEqual(row["impl_header"], "impl<T> [T]")
            self.assertEqual(row["receiver"], "&self")
            self.assertTrue(json.loads(row["doc_spans"]))
            self.assertTrue(row["const_stability"].startswith("stable:"))

    def test_unsafe_and_explicit_receiver_domains_are_not_rewritten(self):
        row = self.by_id["core::slice::from_raw_parts"]
        self.assertEqual(row["signature"],
                         "pub const unsafe fn from_raw_parts<'a, T>(data: *const T, len: usize) -> &'a [T]")
        self.assertEqual(row["unsafe_function"], "true")
        split_off = self.by_id["<[T]>::split_off_mut"]
        self.assertEqual(split_off["receiver"], "self: &mut &'a mut Self")
        self.assertIn("R: OneSidedRange<usize>", split_off["signature"])
        disjoint = self.by_id["<[T]>::get_disjoint_mut"]
        self.assertIn("I: GetDisjointMutIndex + SliceIndex<Self>", disjoint["signature"])
        self.assertNotIn("Copy", disjoint["signature"])
        self.assertEqual(disjoint["effective_stability"], "stable")

    def test_known_generic_constraints_are_exact(self):
        clone = self.by_id["<[T]>::clone_from_slice"]
        self.assertIn("T: [const] Clone + [const] Destruct", clone["signature"])
        search = self.by_id["<[T]>::binary_search_by"]
        self.assertIn("FnMut(&'a T) -> Ordering", search["signature"])
        index = self.by_id["<[T] as core::ops::Index<I>>::index"]
        self.assertEqual(index["self_type"], "[T]")
        self.assertIn("I: [const] SliceIndex<[T]>", index["impl_header"])
        self.assertIn("const_index", index["const_stability"])

    def test_macro_expansion_counts_come_from_templates_and_calls(self):
        records = self.table("macros")
        generated = [n for n in self.inventory.owned_nodes if n.kind == "fn" and n.source.invocation]
        for record in records:
            functions = [n for n in generated if n.source.invocation.span == record["invocation_span"]]
            self.assertEqual(len(functions), int(record["generated_functions"]))
            self.assertTrue(record["definition_span"])
            for node in functions:
                self.assertNotIn("$", node.header)
        template = self.inventory.sources["slice/iter/macros.rs"]
        iterator_definition = next(n for n in self.inventory.slice_nodes
                                   if n.kind == "macro_rules" and n.name == "iterator")
        template_count = len(re.findall(
            r"\bfn\s+\w+\s*(?:<|\()", template.mask[iterator_definition.head_end:iterator_definition.end]
        ))
        for record in (r for r in records if r["macro"] == "iterator"):
            extra_methods = len(re.findall(r"\bfn\s+\w+\s*(?:<|\()", lexical_mask(record["invocation"])[0]))
            self.assertEqual(int(record["generated_functions"]), template_count + extra_methods)
        self.assertEqual(
            {r["self_type"] for r in self.apis if r["name"] == "next" and r["signature_origin"] == "macro-token-substitution"},
            {"core::slice::Iter<'a, T>", "core::slice::IterMut<'a, T>",
             "core::slice::SplitN<'a, T, P>", "core::slice::SplitNMut<'a, T, P>",
             "core::slice::RSplitN<'a, T, P>", "core::slice::RSplitNMut<'a, T, P>"},
        )
        mutable_next = self.by_id["<core::slice::IterMut<'a, T> as core::iter::Iterator>::next"]
        self.assertIn("Option<&'a mut T>", mutable_next["signature"])
        self.assertIn("$elem", mutable_next["source_signature"])
        self.assertEqual(mutable_next["owner"], "core::slice::iter")

    def test_derived_interfaces_preserve_source_and_conditional_bounds(self):
        derived = [r for r in self.apis if r["kind"] == "derived-method"]
        for row in derived:
            self.assertEqual(row["signature_origin"], "trait-declaration-for-derive")
            self.assertIn("derive(", row["impl_header"])
            self.assertEqual(row["signature"], row["trait_signature"])
        windows = next(r for r in derived if r["name"] == "fmt" and "Windows<" in r["self_type"]
                       and "ArrayWindows" not in r["self_type"])
        self.assertEqual(json.loads(windows["derived_bounds"]), ["T: core::fmt::Debug"])
        self.assertTrue(any("EscapeAscii" in r["self_type"] and r["name"] == "clone" for r in derived))
        self.assertTrue(any("GetDisjointMutError" in r["self_type"] and r["name"] == "eq" for r in derived))

    def test_maybe_uninit_adjacent_slice_impl_is_complete(self):
        source = self.inventory.sources["mem/maybe_uninit.rs"]
        impl = next(n for n in self.inventory.nodes if n.source is source and n.kind == "impl"
                    and impl_parts(n)[1:3] == ("", "[MaybeUninit<T>]"))
        methods = children(self.inventory.nodes, impl)
        expected = {n.name for n in methods if visibility(n) == "pub" and stability(n).startswith("stable:")}
        actual = {r["name"] for r in self.apis if r["owner"] == "core::mem::maybe_uninit"}
        self.assertEqual(actual, expected)
        self.assertTrue({"write_copy_of_slice", "write_clone_of_slice", "assume_init_ref",
                         "assume_init_mut", "assume_init_drop"} <= actual)
        drop = self.by_id["<[core::mem::MaybeUninit<T>]>::assume_init_drop"]
        self.assertIn("T: [const] Destruct", drop["signature"])
        self.assertIn("const_drop_in_place", drop["const_stability"])
        excluded_names = {r["name"] for r in self.excluded if r["owner"] == "core::mem::maybe_uninit"}
        self.assertTrue({"as_bytes", "as_bytes_mut", "write_filled", "write_iter", "write_with"} <= excluded_names)
        adjacent = self.table("maybe_uninit_dependencies")
        self.assertTrue(any(r["name"] == "drop" and r["self_type"] == "Guard<'a, T>" for r in adjacent))
        specializations = [r for r in self.excluded if r["owner"] == "core::mem::maybe_uninit"
                           and r["name"] == "spec_fill"]
        self.assertTrue(specializations)
        self.assertTrue(all(r["trait"] == "core::mem::maybe_uninit::SpecFill<T>" for r in specializations))

    def test_slice_index_methods_and_replacement_ranges_are_not_lost(self):
        impls = [n for n in self.inventory.owned_nodes if n.kind == "impl"
                 and impl_parts(n)[1] == "SliceIndex<[T]>"]
        trait_methods = {n.name for n in children(self.inventory.nodes, self.inventory.traits["SliceIndex"])}
        for impl in impls:
            methods = [r for r in self.excluded if r["impl_span"] == impl.span]
            self.assertEqual({r["name"] for r in methods}, trait_methods)
            self.assertFalse(any(r["impl_span"] == impl.span for r in self.apis))
        replacement_names = {"Range", "RangeFrom", "RangeInclusive", "RangeToInclusive"}
        self.assertTrue({f"range::{name}<usize>" for name in replacement_names}
                        <= {impl_parts(impl)[2] for impl in impls})
        adjacent = self.table("range_dependencies")
        for name in replacement_names:
            typ = next(r for r in adjacent if r["owner"] == "core::range"
                       and r["kind"] == "struct" and r["name"] == name)
            self.assertTrue(typ["stability"].startswith("stable:"))
        wrapper_impls = [n for n in self.inventory.nodes if n.source.path == "index.rs"
                         and n.kind == "impl" and impl_parts(n)[1] == "SliceIndex<[T]>"]
        domains = self.table("index_domains")
        self.assertEqual(
            {r["source_span"] for r in domains if r["policy"].startswith("unstable-adjacent-wrapper")},
            {n.span for n in wrapper_impls},
        )
        self.assertTrue(all(r["impl_stability"].startswith("unstable:") for r in domains
                            if r["policy"].startswith("unstable-adjacent-wrapper")))

    def test_unstable_trait_members_do_not_inherit_stable_impl_status(self):
        for name in ("advance_by", "next_chunk", "__iterator_get_unchecked", "is_empty"):
            matches = [r for r in self.excluded if r["self_type"] == "core::slice::Iter<'a, T>"
                       or r["self_type"] == "core::slice::Iter<'_, T>"]
            matches = [r for r in matches if r["name"] == name]
            self.assertTrue(matches, name)
            self.assertTrue(all(r["effective_stability"] == "unstable" for r in matches))
        self.assertTrue(any(r["name"] == "try_fold" and r["effective_stability"] == "stable"
                            for r in self.apis))
        self.assertTrue(any(r["name"] == "sort" and r["owner"] == "core::slice::sort::stable"
                            and "slice_internals" in r["scope_reason"] for r in self.excluded))
        self.assertTrue(any(r["name"] == "choose_pivot"
                            and r["scope_reason"].startswith("public-in-private-module") for r in self.excluded))

    def test_unstable_receiver_type_gates_an_otherwise_stable_method(self):
        nodes = parse(Source("slice/mod.rs", '''
#[unstable(feature = "nightly_receiver", issue = "none")]
pub struct Nightly;
impl Nightly {
    #[stable(feature = "rust1", since = "1.0.0")]
    pub fn observe(&self) {}
}
'''))
        fake = object.__new__(Inventory)
        fake.nodes = fake.slice_nodes = fake.owned_nodes = nodes
        fake.types = {("core::slice", "Nightly"): next(n for n in nodes if n.kind == "struct")}
        fake.exports, fake.traits = {}, {}
        fake.local_types = {"Nightly": "core::slice::Nightly"}
        row = fake.row(next(n for n in nodes if n.kind == "fn"))
        self.assertEqual(row["effective_stability"], "unstable")
        self.assertTrue(row["scope_reason"].startswith("unstable-gate"))

    def test_defaults_blankets_and_adjacent_impls_have_separate_policy(self):
        rows = self.table("trait_surface")
        default_len = next(r for r in rows if r["policy"] == "external-trait-default-not-source-owned"
                           and r["trait"] == "ExactSizeIterator" and r["name"] == "len")
        applies = json.loads(default_len["applicability"])
        self.assertTrue(any("Chunks<" in a["impl"] for a in applies))
        self.assertFalse(any(r["self_type"] == "core::slice::Chunks<'_, T>"
                             and r["trait"] == "core::iter::ExactSizeIterator"
                             and r["name"] == "len" for r in self.apis))
        self.assertTrue(any(r["policy"] == "external-blanket-impl" and r["trait"] == "IntoIterator"
                            and " for I" in r["applicability"] for r in rows))
        self.assertTrue(any(r["policy"] == "adjacent-explicit-impl" and r["trait"] == "Error"
                            and "GetDisjointMutError" in r["applicability"] for r in rows))
        self.assertTrue(any(r["policy"] == "compiler-derived-internal-interface"
                            and r["name"] == "assert_fields_are_eq" for r in rows))

    def test_metadata_dependency_is_linked_to_actual_source(self):
        edges = [r for r in self.table("dependencies") if r["caller"] == "<[T]>::len"]
        edge = next(r for r in edges if r["call"] == "ptr::metadata")
        self.assertEqual(edge["resolution"], "source-path")
        target = next(n for n in self.inventory.nodes if n.source.path == "ptr/metadata.rs"
                      and n.kind == "fn" and n.name == "metadata")
        self.assertEqual(json.loads(edge["target_spans"]), [target.span])
        self.assertIn("ptr_metadata(ptr)", target.body)

    def test_identity_alias_and_coverage_invariants(self):
        rows = self.apis + self.excluded
        self.assertEqual(len(rows), len({r["canonical_id"] for r in rows}))
        self.assertTrue(all(r["scope_reason"] == "stable-public-source-owned" for r in self.apis))
        self.assertTrue(all(r["scope_reason"] != "stable-public-source-owned" for r in self.excluded))
        self.assertTrue(all(r["existing_vstd_coverage"] == PENDING for r in self.excluded))
        self.assertTrue(all(r["existing_vstd_coverage"] == self.vstd_by_id[r["canonical_id"]]["classification"]
                            for r in self.apis))
        self.assertTrue(all(r["effective_stability"] == "stable" for r in self.apis))
        self.assertEqual(sum(r["canonical_id"] == "core::slice::from_ref" for r in self.apis), 1)
        self.assertEqual(json.loads(self.by_id["core::slice::from_ref"]["aliases"]), ["core::slice::from_ref"])
        self.assertFalse(any("core::slice::raw::" in r["canonical_id"] for r in self.apis))

    def test_source_hashes_counts_and_encoding(self):
        for row in self.table("sources"):
            text = (DEFAULT_CORE / row["source"]).read_bytes()
            self.assertEqual(hashlib.sha256(text).hexdigest(), row["sha256"])
        for row in self.table("counts"):
            if row["dimension"] == "total":
                self.assertEqual(int(row["count"]), len(self.table(row["set"])), row["set"])
            elif row["set"] == "apis":
                self.assertEqual(int(row["count"]),
                                 sum(r[row["dimension"]] == row["key"] for r in self.apis))
        for value in ('\\n\t\n\r', "'a", '"quoted"\\t', '☃'):
            self.assertEqual(decode(encode(value)), value)

    def test_lexer_excludes_docs_strings_and_nested_comments(self):
        source = Source("slice/example.rs", '''
/// pub fn not_an_api() {}
#[stable(feature = "quoted_{text}", since = "1.0.0")]
pub const fn actual<'a>(x: &'a [u8]) -> &'a [u8] {
    let _ = r##"fn fake() { }"##;
    /* fn fake_two() {} /* nested */ */
    x
}
''')
        nodes = parse(source)
        self.assertEqual([n.name for n in nodes if n.kind == "fn"], ["actual"])
        method = next(n for n in nodes if n.kind == "fn")
        self.assertIn("'a", method.header)
        self.assertEqual(len(method.docs), 1)
        self.assertTrue(stability(method).startswith("stable:"))

    def test_selected_vstd_replay_matches_all_persisted_evidence(self):
        vstd = self.inventory.vstd
        self.assertEqual(self.table("vstd_coverage"), vstd.rows)
        self.assertEqual(self.table("vstd_sources"), vstd.manifest)
        self.assertEqual(self.table("vstd_scan"), vstd.scans)
        self.assertEqual(set(self.by_id), set(self.vstd_by_id))
        self.assertEqual({r["classification"] for r in vstd.rows}, VSTD_CLASSES)
        for row in vstd.rows:
            self.assertEqual(row["baseline"], VSTD_RELEASE + "@" + VSTD_COMMIT)
            self.assertEqual(row["source_tree_sha256"], VSTD_TREE_SHA256)
            self.assertEqual(row["rust_source_body_proof"], "not-established-by-vstd-mapping")
            self.assertTrue(row["limitations"])
            contracts = json.loads(row["contract_refs"])
            self.assertEqual(bool(contracts), row["classification"] != "missing")

    def test_selected_vstd_spans_resolve_to_the_pinned_source_bytes(self):
        vstd = self.inventory.vstd
        for entry in vstd.manifest:
            data = (vstd.root / entry["source"]).read_bytes()
            self.assertEqual(entry["sha256"], hashlib.sha256(data).hexdigest())
            self.assertEqual(int(entry["bytes"]), len(data))
            self.assertEqual(int(entry["lines"]), len(data.splitlines()))
        for row in vstd.rows:
            for column in ("contract_refs", "model_type_refs", "compiler_support_refs"):
                for ref in json.loads(row[column]):
                    path, first, last = re.fullmatch(r"(.+):(\d+)-(\d+)", ref["span"]).groups()
                    lines = vstd.sources[path].text.splitlines()
                    self.assertLessEqual(1, int(first), ref)
                    self.assertLessEqual(int(first), int(last), ref)
                    self.assertLessEqual(int(last), len(lines), ref)
                    fragment = "\n".join(lines[int(first) - 1:int(last)])
                    if "target" in ref:
                        self.assertIn(re.sub(r"\s+", "", ref["target"]),
                                      re.sub(r"\s+", "", fragment), ref)
                    else:
                        self.assertIn(re.sub(r"\s+", "", ref["declaration"]),
                                      re.sub(r"\s+", "", fragment), ref)

    def test_selected_vstd_missing_contracts_have_replayable_scan_evidence(self):
        vstd = self.inventory.vstd
        scans = {r["query_id"]: r for r in vstd.scans}
        for row in vstd.rows:
            queries = json.loads(row["scan_queries"])
            self.assertIn("name:" + self.by_id[row["canonical_id"]]["name"], queries)
            self.assertTrue(set(queries) <= scans.keys())
        for row in vstd.scans:
            matches = json.loads(row["matches"])
            self.assertEqual(int(row["matching_code_lines"]), sum(len(m["lines"]) for m in matches))
            expected = []
            for path, source in vstd.sources.items():
                lines = [i for i, line in enumerate(source.mask.splitlines(), 1)
                         if re.search(row["pattern"], line)]
                if lines:
                    expected.append({"source": path, "lines": lines})
            self.assertEqual(matches, expected, row["query_id"])
        for name in ("split_last", "size_hint", "from_raw_parts", "sort_unstable",
                     "clone_from_slice", "write_copy_of_slice"):
            self.assertEqual(scans["name:" + name]["matching_code_lines"], "0")
        self.assertEqual(scans["path:replacement-range"]["matching_code_lines"], "0")

    def test_six_observer_mapping_keeps_the_real_split_last_gap(self):
        for name in ("len", "is_empty", "first", "split_first", "last"):
            row = self.vstd_by_id[f"<[T]>::{name}"]
            self.assertEqual(row["classification"], "assumed-contract")
            self.assertTrue(any(ref.get("target") == f"<[T]>::{name}"
                                for ref in json.loads(row["contract_refs"])))
        self.assertEqual(self.vstd_by_id["<[T]>::split_last"]["classification"], "missing")
        length = self.vstd_by_id["<[T]>::len"]
        self.assertTrue(any("spec_slice_len" in ref["declaration"]
                            for ref in json.loads(length["compiler_support_refs"])))
        self.assertTrue(any("axiom_spec_len" in ref["declaration"]
                            for ref in json.loads(length["model_type_refs"])))

    def test_vstd_same_names_do_not_change_the_canonical_receiver(self):
        absent = (
            "<[T]>::as_ptr", "<[T]>::split_off", "<[T]>::contains", "<[u8]>::is_ascii",
            "<[core::mem::MaybeUninit<T>]>::assume_init_ref",
            "<[core::mem::MaybeUninit<T>]>::assume_init_mut",
            "<core::slice::Iter<'a, T>>::as_slice",
            "<core::slice::IterMut<'a, T>>::as_slice",
            "<core::slice::Iter<'_, T> as core::convert::AsRef<[T]>>::as_ref",
            "<core::slice::Iter<'a, T> as core::iter::Iterator>::last",
            "<core::slice::Iter<'a, T> as core::iter::Iterator>::nth",
        )
        for canonical in absent:
            row = self.vstd_by_id[canonical]
            self.assertEqual(row["classification"], "missing", canonical)
            self.assertEqual(json.loads(row["contract_refs"]), [])
        for row in self.inventory.vstd.rows:
            for ref in json.loads(row["contract_refs"]):
                self.assertFalse(ref["span"].startswith(("std_specs/vec.rs:", "std_specs/vecdeque.rs:",
                                                         "std_specs/array.rs:", "array.rs:")), row["canonical_id"])
        mutable = self.vstd_by_id["<&'a mut [T] as core::iter::IntoIterator>::into_iter"]
        self.assertEqual(mutable["classification"], "generic-trait-only")
        self.assertEqual(mutable["contract_extent"], "signature-only-no-postcondition")
        self.assertFalse(any("target" in r for r in json.loads(mutable["contract_refs"])))

    def test_vstd_generic_iterator_contracts_require_the_exact_receiver_model(self):
        for typ in ("Iter", "IterMut"):
            for method in ("next", "all", "any", "find"):
                row = self.vstd_by_id[f"<core::slice::{typ}<'a, T> as core::iter::Iterator>::{method}"]
                self.assertEqual(row["classification"], "generic-trait-conditional")
                refs = json.loads(row["model_type_refs"])
                self.assertTrue(any(r["declaration"] == f"pub struct Ex{typ}<" for r in refs))
                self.assertTrue(all(not r["span"].startswith("std_specs/vecdeque.rs:") for r in refs))
        windows = self.vstd_by_id["<core::slice::Windows<'a, T> as core::iter::Iterator>::next"]
        self.assertEqual(windows["classification"], "generic-trait-only")
        self.assertEqual(windows["receiver_model"], "no-selected-vstd-receiver-type-or-state-model-found")
        size_hint = self.vstd_by_id["<core::slice::Iter<'a, T> as core::iter::Iterator>::size_hint"]
        self.assertEqual(size_hint["classification"], "missing")
        self.assertTrue(json.loads(size_hint["model_type_refs"]))

    def test_vstd_index_contracts_retain_incomplete_rust196_index_domain(self):
        expected = {"usize", "Range<usize>", "RangeTo<usize>", "RangeFrom<usize>",
                    "RangeToInclusive<usize>", "RangeFull", "RangeInclusive<usize>"}
        for canonical in ("<[T]>::get", "<[T]>::get_mut", "<[T] as core::ops::Index<I>>::index",
                          "<[T] as core::ops::IndexMut<I>>::index_mut"):
            row = self.vstd_by_id[canonical]
            self.assertEqual(row["classification"], "assumed-partial-domain")
            declarations = [r["declaration"] for r in json.loads(row["model_type_refs"])]
            actual = {d.split(" for ", 1)[1] for d in declarations
                      if d.startswith("impl<T> super::super::slice::SliceIndexSpecImpl<[T]> for ")}
            self.assertEqual(actual, expected)
            self.assertIn("Bound pair", row["limitations"])
            self.assertIn("core::range", row["limitations"])
        self.assertEqual(self.vstd_by_id["<[T]>::copy_within"]["classification"], "assumed-partial-domain")
        for canonical in ("<[T]>::starts_with", "<[T]>::ends_with", "<[T] as core::cmp::PartialEq<[U]>>::eq"):
            self.assertEqual(self.vstd_by_id[canonical]["classification"], "assumed-conditional")
            self.assertIn("obeys_eq_spec()", self.vstd_by_id[canonical]["conditions"])

    def test_vstd_mapping_fails_closed_on_unreviewed_source_or_api_identity(self):
        with self.assertRaisesRegex(ValueError, "Selected vstd source tree differs"):
            SelectedVstd(ROOT / "inventory")
        with self.assertRaisesRegex(ValueError, "API identities differ"):
            self.inventory.vstd.build(self.apis[:-1])
        source = Source("statement.rs", "fn method() ensures { let x = 0; x == 0 },; fn other();")
        self.assertEqual(source.text[:SelectedVstd.statement_end(source, 0)],
                         "fn method() ensures { let x = 0; x == 0 },;")

    def test_vstd_only_cli_writes_only_mapping_and_the_api_column(self):
        with patch("generate_inventory.write_tsv") as write, \
                patch("generate_inventory.Inventory", side_effect=AssertionError("must not reread core")), \
                patch.object(sys, "argv", ["generate_inventory.py", "--vstd-only"]), \
                redirect_stdout(io.StringIO()):
            main()
        calls = {call.args[0].name: call.args[1] for call in write.call_args_list}
        self.assertEqual(set(calls), {"apis.tsv", "vstd_coverage.tsv", "vstd_sources.tsv", "vstd_scan.tsv"})
        self.assertEqual(calls["apis.tsv"], self.apis)
        self.assertEqual(calls["vstd_coverage.tsv"], self.inventory.vstd.rows)


if __name__ == "__main__":
    unittest.main()
