import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys
import unittest

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "inventory_source", PROJECT / "scripts/inventory_source.py"
)
SOURCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE)


class SourceInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = SOURCE.Inventory(SOURCE.DEFAULT_LIBRARY)
        cls.data = cls.inventory.build()
        cls.apis = cls.data["apis"]
        cls.excluded = cls.data["excluded_functions"]
        cls.functions = cls.apis + cls.excluded

    def one(self, method, owner="Vec<T, A>", trait=""):
        matches = [f for f in self.functions if f["method"] == method
                   and f["source_owner"] == owner and f["trait"] == trait]
        self.assertEqual(len(matches), 1, (method, owner, trait))
        return matches[0]

    def test_full_file_and_function_accounting(self):
        actual = {
            str(p.relative_to(SOURCE.DEFAULT_LIBRARY))
            for p in (SOURCE.DEFAULT_LIBRARY / "alloc/src/vec").rglob("*") if p.is_file()
        }
        self.assertEqual(actual, {f["path"] for f in self.data["source_files"]})
        self.assertEqual({Path(p).name for p in actual}, set(SOURCE.MODULE_ANALYSIS))
        expected = {
            (src.path, n.start_byte, n.end_byte)
            for src in self.inventory.sources.values()
            for n in SOURCE.walk(src.root) if n.type in SOURCE.FUNCTIONS
        }
        direct = [
            (f["source"]["path"], f["source"]["start_byte"], f["source"]["end_byte"])
            for f in self.functions if f["origin"]["kind"] == "source"
        ]
        self.assertEqual(len(direct), len(expected))
        self.assertEqual(set(direct), expected)
        self.assertTrue(all(not f["parse_errors"] for f in self.data["source_files"]))

    def test_no_duplicate_or_malformed_canonical_ids(self):
        ids = [f["canonical_id"] for f in self.apis]
        self.assertEqual(len(ids), len(set(ids)))
        candidate_ids = [f["inventory_id"] for f in self.functions]
        self.assertEqual(len(candidate_ids), len(set(candidate_ids)))
        self.assertFalse(any("core::core::" in i or "alloc::vec::vec::" in i for i in ids))
        self.assertTrue(all("alloc::" in i or i.startswith("<[") or i.startswith("<&[")
                            for i in ids))

    def test_both_asref_and_asmut_targets(self):
        for name in ("AsRef", "AsMut"):
            methods = [f for f in self.apis if f["source_owner"] == "Vec<T, A>"
                       and SOURCE.base_name(f["trait"]) == name]
            self.assertEqual({f["trait"] for f in methods},
                             {f"{name}<Vec<T, A>>", f"{name}<[T]>"})
            self.assertEqual(len(methods), 2)
        self.assertNotEqual(
            self.one("as_mut", trait="AsMut<Vec<T, A>>")["canonical_id"],
            self.one("as_mut", trait="AsMut<[T]>")["canonical_id"],
        )

    def test_allocator_and_const_bounds_not_collapsed(self):
        for method in ("push", "push_mut"):
            f = self.one(method)
            self.assertEqual(f["status"], "included")
            self.assertIn("A: [const] Allocator + [const] Destruct", f["impl_header"])
            self.assertTrue(f["owner_generic_parameter_attributes"])
            self.assertIn("const impl", f["impl_header"])
        self.assertEqual(self.one("new", "Vec<T>")["impl_generic_parameters"], "<T>")
        self.assertIn("A: Clone", self.one("split_off")["method_where_clause"])
        self.assertIn("T: Clone", self.one("resize")["impl_generic_parameters"])

    def test_const_stability_is_separate(self):
        f = self.one("with_capacity", "Vec<T>")
        self.assertEqual(f["status"], "included")
        self.assertTrue(any("rustc_const_unstable" in a["text"] for a in f["const_stability"]))
        f = self.one("default", "Vec<T>", "Default")
        self.assertEqual(f["status"], "included")
        self.assertIn("impl<T> const Default", f["impl_header"])

    def test_trait_declaration_overrides_stable_impl_gate(self):
        unstable = {
            "advance_by", "advance_back_by", "next_chunk", "__iterator_get_unchecked",
            "extend_one", "extend_reserve", "extend_one_unchecked",
        }
        records = [f for f in self.functions if f["method"] in unstable or
                   f["method"] == "is_empty" and f["trait"] == "ExactSizeIterator"]
        self.assertTrue(records)
        for f in records:
            self.assertEqual(f["status"], "excluded")
            self.assertEqual(f["exclusion_reason"], "unstable_api")
            self.assertTrue(any(g["role"] == "trait_member" and g["kind"] == "unstable"
                                for g in f["stability"]["gates"]))
        f = self.one("try_fold", "IntoIter<T, A>", "Iterator")
        self.assertEqual(f["status"], "included")
        self.assertIn("R: core::ops::Try<Output = B>", f["signature"])
        self.assertEqual(f["stability"]["effective_since"], "1.27.0")

    def test_cfg_inheritance_in_modules_impls_and_local_helpers(self):
        for f in self.functions:
            if f["source_module"] in {"cow", "splice", "is_zero"}:
                self.assertIn("not(no_global_oom_handling)", f["cfg"], f["inventory_id"])
        for method in ("push", "push_mut"):
            self.assertIn("not(no_global_oom_handling)", self.one(method)["cfg"])
        helper = next(f for f in self.excluded if "local in split_off" in f["canonical_id"])
        self.assertIn("not(no_global_oom_handling)", helper["cfg"])
        self.assertNotIn("not(no_global_oom_handling)", self.one("try_reserve")["cfg"])

    def test_partial_eq_macro_is_expanded_per_target(self):
        calls = [m for m in self.data["macro_sites"] if m["name"] == "__impl_slice_eq1"]
        entries = [f for f in self.apis if f["source_module"] == "partial_eq"]
        self.assertEqual(len(entries), 2 * len(calls))
        for call in calls:
            pair = [f for f in entries if f["source"] == call["source"]]
            self.assertEqual({f["method"] for f in pair}, {"eq", "ne"})
            self.assertTrue(all(f["origin"]["definition"]["path"].endswith("partial_eq.rs")
                                for f in pair))
        mixed = next(f for f in entries if f["source_owner"] == "Vec<T, A1>" and f["method"] == "eq")
        self.assertIn("A1: Allocator, A2: Allocator", mixed["impl_generic_parameters"])
        self.assertIn("T: PartialEq<U>", mixed["impl_where_clause"])
        borrowed_mut = next(f for f in entries if f["trait"] == "PartialEq<&mut [U]>"
                            and f["source_owner"] == "Vec<T, A>" and f["method"] == "eq")
        self.assertIn("other: &&mut [U]", borrowed_mut["signature"])
        self.assertTrue(any(f["source_owner"] == "&mut [T]" for f in entries))
        cows = [f for f in entries if f["source_owner"] == "Cow<'_, [T]>"]
        self.assertTrue(cows)
        self.assertTrue(all("T: Clone" in f["impl_where_clause"] for f in cows))

    def test_private_macro_recursion_is_accounted(self):
        tuple_entries = [f for f in self.excluded
                         if f["origin"].get("macro") == "impl_is_zero_tuples"]
        invocation = next(m for m in self.data["macro_sites"] if m["name"] == "impl_is_zero_tuples")
        self.assertEqual(len(tuple_entries), invocation["generated_impls"])
        self.assertEqual(
            sorted(len(SOURCE.split_commas(f["source_owner"][1:-1])) for f in tuple_entries),
            list(range(1, invocation["generated_impls"] + 1)),
        )
        self.assertTrue(all(f["exclusion_reason"] == "private_specialization_trait"
                            for f in tuple_entries))
        self.assertFalse(any(f["source_module"] == "is_zero" for f in self.apis))

    def test_derive_debug_signature_and_bounds(self):
        entries = [f for f in self.apis if f["origin"]["kind"] == "builtin_derive"]
        self.assertEqual(len(entries), 1)
        f = entries[0]
        self.assertEqual(f["canonical_id"],
                         "<alloc::vec::Splice<'a, I, A> as core::fmt::Debug>::fmt")
        self.assertIn("I: core::fmt::Debug + Iterator + 'a", f["impl_header"])
        self.assertIn("A: core::fmt::Debug + Allocator + 'a", f["impl_header"])
        self.assertIn("I::Item: core::fmt::Debug", f["impl_where_clause"])
        self.assertEqual(f["source"], f["origin"]["invocation"])
        self.assertEqual(f["stability"]["effective_since"], "1.21.0")

    def test_private_drop_guards_are_not_public_apis(self):
        private = {"in_place_drop", "set_len_on_drop"}
        self.assertFalse(any(f["source_module"] in private for f in self.apis))
        drops = [f for f in self.excluded if f["source_module"] in private and f["trait"] == "Drop"]
        self.assertEqual({SOURCE.base_name(f["source_owner"]) for f in drops},
                         {"InPlaceDrop", "InPlaceDstDataSrcBufDrop", "SetLenOnDrop"})
        self.assertTrue(all(f["exclusion_reason"] == "private_owner" for f in drops))

    def test_empty_impl_and_default_method_distinction(self):
        empty_eq = next(i for i in self.data["impls"] if i["trait"] == "Eq")
        self.assertFalse(empty_eq["methods"])
        inherited = self.data["inherited_trait_methods"]
        lengths = [f for f in inherited if f["trait"] == "core::iter::ExactSizeIterator"
                   and f["method"] == "len"]
        self.assertEqual(len(lengths), 3)
        self.assertTrue(all(f["source"]["path"].startswith("core/") for f in lengths))
        self.assertFalse(any(f["method"] == "len" and f["trait"] == "ExactSizeIterator"
                             for f in self.apis))
        self.assertTrue(any("IntoIter" in f["owner"] and f["method"] == "clone_from"
                            for f in inherited))
        self.assertTrue(any(f["reason"] == "reservation_impl_not_available"
                            for f in self.data["external_impl_boundaries"]))

    def test_hidden_public_and_foreign_owners_are_included(self):
        f = self.one("from_elem", "alloc::vec")
        self.assertEqual(f["status"], "included")
        self.assertTrue(any(a["text"] == "#[doc(hidden)]" for a in f["attributes"]))
        self.assertTrue(any(d["role"] == "caller_macro_not_own_docstring" for d in f["docs"]))
        self.assertTrue(any(f["source_owner"] == "Box<[T], A>" for f in self.apis))
        self.assertTrue(any(f["source_owner"] == "[T; N]" and f["method"] == "try_from"
                            for f in self.apis))
        self.assertTrue(any(f["source_owner"].startswith("Cow") and f["source_module"] == "cow"
                            for f in self.apis))
        self.assertTrue(any(f["trait"] == "From<Cow<'a, [T]>>"
                            and "[T]: ToOwned<Owned = Vec<T>>" in f["impl_where_clause"]
                            for f in self.apis))

    def test_receiver_and_lifetime_relations(self):
        f = self.one("into_iter", "&'a mut Vec<T, A>", "IntoIterator")
        self.assertEqual(f["receiver"]["kind"], "by_value")
        self.assertIn("'a", f["lifetime_relation"]["named_and_placeholder_lifetimes"])
        self.assertTrue(any("type Item = &'a mut T;" in a["text"] for a in f["associated_items"]))
        f = self.one("as_mut_slice")
        self.assertEqual(f["receiver"]["kind"], "mutable_borrow")
        self.assertTrue(f["receiver"]["reference_mutable"])
        self.assertFalse(f["receiver"]["binding_mutable"])
        f = self.one("leak")
        self.assertIn("A: 'a", f["method_where_clause"])
        self.assertIn("T:'a", f["lifetime_relation"]["relation"])
        self.assertNotIn("'static", f["signature"])
        self.assertIn("裸指针", self.one("as_ptr")["lifetime_relation"]["relation"])

    def test_source_and_doc_spans_round_trip(self):
        for f in self.functions:
            if f["origin"]["kind"] == "source":
                s = f["signature_source"]
                raw = self.inventory.sources[s["path"]].raw
                self.assertEqual(raw[s["start_byte"]:s["end_byte"]].decode().strip(), f["signature"])
        for key, doc in self.data["docstrings"].items():
            s = doc["source"]
            path = SOURCE.DEFAULT_LIBRARY / s["path"]
            raw = path.read_bytes()
            selected = raw[s["start_byte"]:s["end_byte"]].decode()
            self.assertEqual(SOURCE.loc(s), key)
            self.assertEqual(raw.count(b"\n", 0, s["start_byte"]) + 1, s["start_line"])
            self.assertTrue(all(line in selected for line in doc["text"].splitlines()))
        for f in self.apis:
            self.assertTrue(all(d["ref"] in self.data["docstrings"] for d in f["docs"]))

    def test_reexports_and_module_documentation(self):
        self.assertEqual({t["name"] for t in self.data["types"] if t["exported"]},
                         set(SOURCE.PUBLIC_TYPES))
        self.assertTrue(self.data["reexports"])
        self.assertTrue(all(f["origin"]["kind"] != "reexport" for f in self.apis))
        for name in ("mod.rs", "in_place_collect.rs"):
            f = next(f for f in self.data["source_files"] if f["path"].endswith("/" + name))
            self.assertTrue(f["module_docs"])
            self.assertIn(f["module_docs"][0]["ref"], self.data["docstrings"])

    def test_external_semantic_dependencies_are_not_owned_targets(self):
        paths = {d["path"] for d in self.data["dependency_sources"]}
        self.assertIn("alloc/src/raw_vec/mod.rs", paths)
        self.assertIn("core/src/alloc/mod.rs", paths)
        self.assertIn("core/src/slice/raw.rs", paths)
        self.assertTrue(all(f["source"]["path"].startswith("alloc/src/vec/") for f in self.apis))
        borrows = [d for d in self.data["external_impl_boundaries"]
                   if d["reason"] == "external_concrete_impl"]
        self.assertEqual(len(borrows), 2)
        self.assertTrue(all(d["source"]["path"] == "alloc/src/slice.rs" for d in borrows))

    def test_parser_distinguishes_comments_and_preserves_original_const_text(self):
        raw = b'''/// pub fn not_an_api() {}
#[cfg(not(no_global_oom_handling))]
const impl<T, A: [const] Allocator> Vec<T, A> {
    pub fn push(&mut self, t: T) {}
}
'''
        src = SOURCE.Source("<parser-shape-test>", raw)
        functions = [n for n in SOURCE.walk(src.root) if n.type in SOURCE.FUNCTIONS]
        self.assertEqual([src.field(n, "name") for n in functions], ["push"])
        impl = next(n for n in src.root.named_children if n.type == "impl_item")
        self.assertIn("const impl<T, A: [const] Allocator>", src.header(impl))
        self.assertFalse(src.errors)
        self.assertEqual(src.raw, raw)

    def test_unknown_item_macro_fails_closed(self):
        inventory = SOURCE.Inventory(SOURCE.DEFAULT_LIBRARY)
        path = "alloc/src/vec/cow.rs"
        original = inventory.sources[path].raw
        inventory.sources[path] = SOURCE.Source(path, original + b"\nunknown_api_macro! { x }\n")
        with self.assertRaises(AssertionError):
            inventory.build()

    def test_persisted_outputs_equal_fresh_extraction(self):
        for relative, content in SOURCE.generated_files(self.data).items():
            self.assertTrue((PROJECT / relative).read_text() == content, relative)

    def test_source_regeneration_preserves_vstd_section_and_detects_source_changes(self):
        source = SOURCE.render_markdown(self.data)
        section = (
            "<!-- BEGIN OFFICIAL VSTD COVERAGE -->\n"
            "independently generated coverage\n"
            "<!-- END OFFICIAL VSTD COVERAGE -->\n"
            "\nparent-tail\n"
        )
        original = "stale source\n\n" + section
        expected = source.rstrip("\n") + "\n\n" + section
        self.assertEqual(SOURCE.update_source_section(original, source), expected)
        self.assertNotEqual(original, expected)
        self.assertEqual(SOURCE.update_source_section(expected, source), expected)
        self.assertEqual(SOURCE.update_source_section("stale source\n", source), source)

    def test_source_regeneration_rejects_malformed_coverage_markers(self):
        begin = "<!-- BEGIN OFFICIAL VSTD COVERAGE -->"
        end = "<!-- END OFFICIAL VSTD COVERAGE -->"
        for original in (begin, end, begin + begin + end, begin + end + end, end + begin):
            with self.subTest(original=original), self.assertRaisesRegex(AssertionError, "coverage"):
                SOURCE.update_source_section(original, "fresh source\n")

    def test_builtin_debug_bounds_shape_with_available_compiler(self):
        env = dict(os.environ, RUSTC_BOOTSTRAP="1", TMPDIR=str(PROJECT / "inventory/source-tests"))
        completed = subprocess.run(
            ["rustc", "--crate-type=lib", "--crate-name=inventory_derive_probe",
             "-Zunpretty=expanded", str(PROJECT / "inventory/source-tests/derive_debug.rs")],
            cwd=PROJECT, env=env, text=True, capture_output=True, timeout=30, check=True,
        )
        expanded = SOURCE.Source("<derive-shape-probe>", completed.stdout.encode())
        impl = next(n for n in expanded.root.named_children
                    if n.type == "impl_item" and expanded.field(n, "type") == "Splice<'a, I, A>")
        header = SOURCE.compact(expanded.header(impl))
        for pattern in (r"I:\s*::core::fmt::Debug\s*\+\s*Iterator\s*\+\s*'a",
                        r"A:\s*::core::fmt::Debug\s*\+\s*Allocator\s*\+\s*'a",
                        r"where\s+I::Item:\s*::core::fmt::Debug"):
            self.assertRegex(header, pattern)


if __name__ == "__main__":
    unittest.main()
