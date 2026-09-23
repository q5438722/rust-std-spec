from __future__ import annotations

from collections import Counter
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
M = runpy.run_path(str(ROOT / "scripts/inventory_vstd.py"))


class CoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "inventory/vstd_coverage.json").read_text())
        cls.source = M["load_source"]()
        cls.tree = M["OfficialTree"]()
        cls.direct, cls.traits = M["collect_evidence"](cls.tree)
        M["annotate_evidence"](cls.tree, cls.direct)
        cls.apis = {a["canonical_id"]: a for a in cls.data["apis"]}
        cls.evidence = {e["id"]: e for e in cls.data["evidence"]}

    def test_full_138_row_identity_bijection(self):
        self.assertEqual(len(self.apis), 138)
        self.assertEqual([a["canonical_id"] for a in self.data["apis"]],
                         [a["canonical_id"] for a in self.source["apis"]])
        for current, original in zip(self.data["apis"], self.source["apis"]):
            for field in M["IDENTITY_FIELDS"]:
                self.assertEqual(current[field], original[field], (current["canonical_id"], field))

    def test_tsv_has_exactly_one_row_per_source_api(self):
        rows = list(csv.DictReader(io.StringIO((ROOT / "inventory/vstd_coverage.tsv").read_text()), delimiter="\t"))
        self.assertEqual(len(rows), 138)
        self.assertEqual(Counter(r["canonical_id"] for r in rows), Counter(self.apis.keys()))
        self.assertEqual([r["coverage_class"] for r in rows],
                         [r["coverage_class"] for r in self.data["apis"]])

    def test_all_16_modules_and_exclusions_accounted(self):
        self.assertEqual(len(self.data["submodules"]), 16)
        self.assertEqual(self.data["input_accounting"], self.source["counts"])
        self.assertEqual(self.data["input_accounting"]["excluded_function_candidates"], 164)
        self.assertEqual(sum(s["stable_api_count"] for s in self.data["submodules"]), 138)
        for s in self.data["submodules"]:
            expected = Counter(a["coverage_class"] for a in self.data["apis"] if a["source_module"] == s["source_module"])
            self.assertEqual(s["stable_api_count"], sum(expected.values()))
            self.assertEqual(s["by_coverage_class"], {k: expected[k] for k in M["CLASSES"]})

    def test_class_partition_and_direct_claims(self):
        self.assertEqual(self.data["counts"]["by_coverage_class"],
                         {"exact": 32, "partial": 1, "trait_only": 52, "indirect": 22, "none": 31})
        self.assertEqual(self.data["counts"]["direct_assume_target_claims"], 28)
        self.assertEqual(self.data["counts"]["exact_trait_specialized_without_target_assume"], 4)
        claims = [ref for a in self.data["apis"] for ref in a["direct_spec_refs"]]
        self.assertEqual(len(claims), len(set(claims)))
        self.assertEqual(self.data["checks"]["duplicate_external_spec_claims"], 0)

    def test_every_evidence_span_matches_official_bytes(self):
        for evidence in self.data["evidence"]:
            for fragment in [evidence] + evidence.get("preceding_attribute_refs", []):
                span = fragment["source"]
                self.assertTrue(span["path"].startswith("toolchains/upstream/source/vstd/"))
                raw = (ROOT / span["path"]).read_bytes()
                selected = raw[span["start_byte"]:span["end_byte"]]
                self.assertEqual(selected.decode(), fragment["literal"], evidence["id"])
                self.assertEqual(hashlib.sha256(selected).hexdigest(), fragment["sha256"])
                self.assertEqual(raw[:span["start_byte"]].count(b"\n") + 1, span["start_line"])
                self.assertEqual(raw[:span["end_byte"] - 1].count(b"\n") + 1, span["end_line"])

    def test_all_official_files_fingerprinted(self):
        manifest = self.data["file_accounting"]
        root = ROOT / "toolchains/upstream/source/vstd"
        actual = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
        self.assertEqual(actual, [f["path"] for f in manifest["files"]])
        self.assertEqual(manifest["all_files"], 133)
        self.assertEqual(manifest["rust_files_scanned"], 130)
        for f in manifest["files"]:
            raw = (root / f["path"]).read_bytes()
            self.assertEqual(len(raw), f["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), f["sha256"])

    def test_source_inputs_not_modified(self):
        for record in self.data["baseline"]["source_inventory"]:
            self.assertEqual(hashlib.sha256((ROOT / record["path"]).read_bytes()).hexdigest(), record["sha256"])

    def test_every_vec_assumption_is_accounted_once(self):
        assumptions = [a for a in self.tree.assumptions if a["source"]["path"].endswith("/std_specs/vec.rs")]
        self.assertEqual(len(assumptions), 30)
        refs = list(self.direct.values()) + ["vec.new_in", "vec.with_capacity_in"]
        self.assertEqual(Counter(a["sha256"] for a in assumptions),
                         Counter(self.evidence[r]["sha256"] for r in refs))

    def test_four_conversion_targets_are_distinct_and_uncovered(self):
        rows = [a for a in self.data["apis"] if a["source_module"] == "mod" and a["method"] in ("as_ref", "as_mut")]
        self.assertEqual(len(rows), 4)
        self.assertEqual(len({r["canonical_trait"] for r in rows}), 4)
        for row in rows:
            self.assertFalse(row["direct_spec_refs"])
            self.assertFalse(row["trait_contract_refs"])
            self.assertFalse(row["compiler_hook_refs"])
            target_slice = "<[T]>" in row["canonical_trait"]
            self.assertEqual(row["coverage_class"], "indirect" if target_slice else "none")
            refs = [r for d in row["indirect_dependencies"] for r in d["evidence_refs"]]
            self.assertEqual(bool(refs), target_slice)
        for name in ("AsRef", "AsMut"):
            self.assertEqual(self.tree.symbol_occurrences(name), [])

    def test_index_and_index_mut_domains_not_conflated(self):
        index = self.apis["<alloc::vec::Vec<T, A> as core::ops::Index<I>>::index"]
        mutable = self.apis["<alloc::vec::Vec<T, A> as core::ops::IndexMut<I>>::index_mut"]
        self.assertEqual(index["coverage_class"], "exact")
        self.assertEqual(mutable["coverage_class"], "partial")
        self.assertIn("I: SliceIndex<[T]>", self.evidence["vec.index"]["literal_generics"])
        self.assertEqual(mutable["direct_spec_refs"], [])
        self.assertEqual(mutable["compiler_hook_refs"], ["vec.index_mut_usize"])
        self.assertNotIn("ensures", self.evidence["trait.index_mut.index_mut"]["literal_clauses"])
        hook = self.evidence["vec.index_mut_usize"]
        self.assertIn("i: usize", hook["literal_signature"])
        self.assertIn("final(vec)@ == old(vec)@.update", hook["literal_clauses"]["ensures"])
        self.assertIn("explicit IndexMut UFCS", " ".join(mutable["signature_domain"]["notes"]))

    def test_allocator_parameters_preserved(self):
        for row in self.data["apis"]:
            if not row["direct_spec_refs"]:
                continue
            evidence = self.evidence[row["direct_spec_refs"][0]]
            for allocator in ("A", "A1", "A2"):
                if allocator + ":" in row["impl_generic_parameters"]:
                    self.assertIn(allocator + ":", evidence["literal_generics"], row["canonical_id"])
            self.assertNotIn("Copy", evidence["literal_generics"])
        default = self.apis["<alloc::vec::Vec<T> as core::default::Default>::default"]
        self.assertEqual(default["canonical_owner"], "alloc::vec::Vec<T>")
        self.assertEqual(default["coverage_class"], "exact")

    def test_trait_specializations_apply_to_exact_identities(self):
        specialized = [a for a in self.data["apis"] if a["coverage_class"] == "exact" and not a["direct_spec_refs"]]
        self.assertEqual({(a["source_module"], a["method"]) for a in specialized},
                         {("into_iter", "next"), ("into_iter", "next_back"), ("mod", "from_iter"), ("partial_eq", "ne")})
        for row in specialized:
            self.assertTrue(row["trait_contract_refs"])
            self.assertTrue(row["concrete_spec_impl_refs"])
        comparisons = [a for a in self.data["apis"] if a["source_module"] == "partial_eq"]
        self.assertEqual(sum(a["coverage_class"] == "trait_only" for a in comparisons), 22)
        for row in comparisons:
            self.assertFalse(row["trait_instantiations"][0]["default_ensures_applies"])

    def test_weak_contracts_are_literal_and_not_upgraded(self):
        reserve = self.evidence["vec.try_reserve"]["literal_clauses"]
        self.assertEqual(reserve, {"ensures": "final(vec)@ == old(vec)@,"})
        capacity = self.evidence["vec.with_capacity"]["literal_clauses"]["ensures"]
        self.assertEqual(capacity, "v@ == Seq::<T>::empty(),")
        self.assertEqual(self.evidence["vec.eq"]["literal_clauses"], {})
        for ref in ("trait.clone.clone", "trait.default.default", "trait.into_iterator.into_iter"):
            self.assertEqual(self.evidence[ref]["literal_clauses"], {})
        self.assertIn("strictly_cloned(a, b) || a == b", self.evidence["clone.cloned"]["literal"])

    def test_builtin_index_models_and_global_only_helpers_are_explicit(self):
        refs = self.evidence["vec.index"]["support_refs"]
        for slug in ("usize", "range", "rangeto", "rangefrom", "rangetoinclusive", "rangefull", "rangeinclusive"):
            self.assertIn("slice.index_model." + slug, refs)
            self.assertIn("slice." + slug + ".index", refs)
        self.assertIn("final_slice == old_slice", self.evidence["slice.generic_index_mut_post"]["literal"])
        for ref in ("vec.index_decreases", "vec.has_resolved", "vec.decreases_to_view",
                    "vec.eq_law", "vec.view_eq_law", "vec.deep_eq_law"):
            self.assertIn("global_only", self.evidence[ref]["kind"])
            self.assertNotIn("A: Allocator", self.evidence[ref]["literal"])

    def test_missing_methods_are_not_inherited_from_unrelated_contracts(self):
        for row in self.data["apis"]:
            if row["source_module"] == "into_iter" and row["method"] in ("count", "last", "size_hint", "fold", "try_fold"):
                self.assertEqual(row["trait_contract_refs"], [])
                self.assertEqual(row["direct_spec_refs"], [])
        hash_row = self.apis["<alloc::vec::Vec<T, A> as core::hash::Hash>::hash"]
        self.assertEqual(hash_row["coverage_class"], "none")
        self.assertNotIn("fn hash", self.evidence["trait.hash"]["literal"])

    def test_missing_iterator_views_and_conditional_frameworks(self):
        for symbol in ("Drain", "ExtractIf", "Splice"):
            self.assertEqual(self.tree.symbol_occurrences(symbol), [])
        for module in ("drain", "extract_if", "splice"):
            rows = [a for a in self.data["apis"] if a["source_module"] == module]
            self.assertFalse(any(a["coverage_class"] in ("exact", "partial") for a in rows))
        views = {v["id"]: v for v in self.data["views"]}
        self.assertIn("into_iter_elts(i1)", views["owned_iterator_state"]["source_bridge_required"])
        self.assertIn("Neither frozen-original contents nor elts(i1)==remaining(i1) is an invariant supplied by vstd.",
                      views["owned_iterator_state"]["source_bridge_required"])
        self.assertIn("T: View + Clone", views["cow_slice_sequence"]["domain"])

    def test_327_inherited_instances_stay_outside_target_count(self):
        rows = self.data["inherited_framework_relations"]
        self.assertEqual(len(rows), 327)
        self.assertEqual([r["canonical_id"] for r in rows],
                         [r["canonical_id"] for r in self.source["inherited_trait_methods"]])
        self.assertTrue(all(not r["included_in_api_count"] for r in rows))
        self.assertTrue(any(r["method"] == "len" and r["trait_contract_refs"] == ["trait.exact_size.len"] for r in rows))

    def test_external_fn_comments_do_not_count(self):
        self.assertEqual(self.data["file_accounting"]["active_external_fn_specification_attributes"], 0)
        self.assertEqual(len(self.data["file_accounting"]["inactive_external_fn_examples"]), 2)
        for ref in self.data["file_accounting"]["inactive_external_fn_examples"]:
            self.assertTrue(self.evidence[ref]["literal"].startswith("/*"))
        self.assertNotIn(("core::clone::Clone", "clone_from"), self.traits)

    def test_view_order_and_all_references(self):
        M["validate"](self.data, self.source, self.tree)
        seen = set()
        for view in self.data["views"]:
            self.assertLessEqual(set(view["depends_on"]), seen)
            seen.add(view["id"])
        for module in self.data["submodules"]:
            self.assertLessEqual(set(module["view_dependencies"]), seen)

    def test_duplicate_external_claim_is_rejected(self):
        data = copy.deepcopy(self.data)
        rows = {r["canonical_id"]: r for r in data["apis"]}
        rows["alloc::vec::Vec<T>::with_capacity"]["direct_spec_refs"] = ["vec.new"]
        with self.assertRaisesRegex(ValueError, "duplicate external"):
            M["validate"](data, self.source, self.tree)

    def test_changed_source_identity_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["apis"][0]["canonical_trait"] = "core::convert::AsRef<[T]>"
        with self.assertRaisesRegex(ValueError, "identity/domain changed"):
            M["validate"](data, self.source, self.tree)

    def test_swapped_external_bindings_are_rejected(self):
        data = copy.deepcopy(self.data)
        rows = {r["canonical_id"]: r for r in data["apis"]}
        rows["alloc::vec::Vec<T>::new"]["direct_spec_refs"] = ["vec.with_capacity"]
        rows["alloc::vec::Vec<T>::with_capacity"]["direct_spec_refs"] = ["vec.new"]
        with self.assertRaisesRegex(ValueError, "canonical target mismatch"):
            M["validate"](data, self.source, self.tree)

    def test_trait_generic_names_and_associated_types_are_resolved(self):
        row = self.apis["<alloc::vec::Vec<T> as core::iter::FromIterator<T>>::from_iter"]
        self.assertEqual(row["trait_instantiations"][0]["generic_substitution"],
                         {"Self": "alloc::vec::Vec<T>", "trait.A": "T", "method.T": "I"})
        row = self.apis["<alloc::vec::IntoIter<T, A> as core::iter::Iterator>::next"]
        self.assertEqual(row["trait_instantiations"][0]["generic_substitution"]["Self::Item"], "T")

    def test_append_section_preserves_source_and_other_sections(self):
        for prefix in ("source\n", "source\n\n", "source\n\n\n", "source"):
            new = M["update_section"](prefix, M["BEGIN"] + "\nours\n" + M["END"] + "\n")
            self.assertTrue(new.startswith(prefix))
            replaced = M["update_section"](new + "\nparent-tail\n", M["BEGIN"] + "\nnew\n" + M["END"] + "\n")
            self.assertTrue(replaced.startswith(prefix))
            self.assertTrue(replaced.endswith("\nparent-tail\n"))
            self.assertEqual(replaced.count(M["BEGIN"]), 1)

    def test_binary_probe_artifact_is_current(self):
        result = json.loads((HERE / "binding_results.json").read_text())
        self.assertEqual(result["fixture_sha256"], hashlib.sha256((HERE / "binding_probes.rs").read_bytes()).hexdigest())
        self.assertTrue(result["all_matched"])
        self.assertEqual(result["cases"], 15)
        self.assertEqual(result["positive_cases"], 6)
        self.assertEqual(result["negative_controls"], 9)
        self.assertTrue(all(r["actual_exit"] == r["expected_exit"] for r in result["results"]))


class ScannerTests(unittest.TestCase):
    def test_comments_literals_and_lifetimes(self):
        text = """// assume_specification [fake];
/* outer /* #[verifier::external_fn_specification] */ comment */
const S: &str = r##"assume_specification [fake];"##;
const C: char = '\\u{3bb}';
pub assume_specification<'a, T: Trait<[u8; 2]>>[ <Thing<T> as Trait<&'a [u8;2]>>::f ](
    a: &'a [u8; 2],
) -> (r: bool)
    ensures { let x = 1; r == (x == 1) },
;
"""
        masked = M["mask_noncode"](text)
        self.assertEqual(masked.count("assume_specification"), 1)
        self.assertIn("'a", masked)
        with tempfile.TemporaryDirectory(prefix="scanner-", dir=HERE) as directory:
            path = Path(directory) / "fixture.rs"
            path.write_text(text)
            tree = M["OfficialTree"](Path(directory))
            self.assertEqual(len(tree.assumptions), 1)
            declaration = tree.assumptions[0]
            self.assertEqual(declaration["literal_generics"], "<'a, T: Trait<[u8; 2]>>")
            self.assertEqual(declaration["literal_target"], "<Thing<T> as Trait<&'a [u8;2]>>::f")
            self.assertEqual(declaration["literal_clauses"]["ensures"], "{ let x = 1; r == (x == 1) },")

    def test_invalid_or_new_shapes_fail_explicitly(self):
        with self.assertRaisesRegex(ValueError, "unterminated block"):
            M["mask_noncode"]("/* broken")
        with self.assertRaisesRegex(ValueError, "mismatched delimiter"):
            M["balanced_end"]("([)]", 0)
        with tempfile.TemporaryDirectory(prefix="scanner-", dir=HERE) as directory:
            (Path(directory) / "fixture.rs").write_text("pub assume_specification broken;")
            with self.assertRaisesRegex(ValueError, "unrecognized assume"):
                M["OfficialTree"](Path(directory))


if __name__ == "__main__":
    unittest.main()
