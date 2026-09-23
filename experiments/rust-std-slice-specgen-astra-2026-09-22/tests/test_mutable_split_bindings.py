from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
APIS = ("split_first_mut", "split_last_mut")
PRESERVED = ROOT / "logs/mutable-splits/adoption-before"


def compact(text):
    return re.sub(r"\s+", "", text)


class MutableSplitBindings(unittest.TestCase):
    def test_only_the_missing_public_binding_is_added(self):
        declarations = "\n".join(
            path.read_text() for path in (ROOT / "specs").rglob("*.rs")
        )
        self.assertNotRegex(
            declarations, r"assume_specification<T>\s*\[\s*<\[T\]>::split_first_mut\s*\]",
        )
        self.assertEqual(len(re.findall(
            r"assume_specification<T>\s*\[\s*<\[T\]>::split_last_mut\s*\]", declarations,
        )), 1)
        binding = (ROOT / "specs/slice/mutable_splits.rs").read_text()
        self.assertIn("slice: &mut [T],", binding)
        self.assertIn("-> (result: Option<(&mut T, &mut [T])>)", binding)
        self.assertNotRegex(binding, r"\b(?:requires|Copy|Eq|Default|where)\b|'static")
        source = (ROOT / "proofs/correctness/slice/split_last_mut.rs").read_text()
        clause = source[source.index("    ensures\n"):source.index("\n{\n")]
        self.assertIn(clause.replace("contracts::", "post::"), binding)

    def test_pure_candidates_do_not_import_assumed_contracts(self):
        post = (ROOT / "specs/slice/mutable_splits_post.rs").read_text()
        self.assertEqual(post.count("pub open spec fn "), 2)
        self.assertNotRegex(
            post,
            r"\b(?:assume_specification|external_body|axiom|assume|admit|requires|mod|Copy|Eq|Default|where)\b|'static",
        )
        self.assertEqual(post.count("written_remainder.len() == remainder.len()"), 2)
        self.assertEqual(post.count("input_initial.len() == 0 && observations.1 =~= seq![]"), 2)
        self.assertIn("observations.1 =~= seq![written] + written_remainder", post)
        self.assertIn("observations.1 =~= written_remainder + seq![written]", post)
        self.assertNotIn("observations.1.len()", post)

    def test_current_sources_change_only_the_permitted_bodies(self):
        for api, body in (
            ("split_first_mut", "    if let [first, tail @ ..] = slice { Some((first, tail)) } else { None }"),
            ("split_last_mut", "    if let [init @ .., last] = slice { Some((last, init)) } else { None }"),
        ):
            with self.subTest(api=api):
                relative = f"proofs/correctness/slice/{api}.rs"
                original = (PRESERVED / relative).read_text()
                self.assertIn("\n{\n" + body + "\n}\n}\n", original)
                proposed = (ROOT / f"proofs/correctness/slice/proposals/{api}.rs").read_text()
                proposed_body = proposed.split("\n{\n", 1)[1].removesuffix("\n}\n}\n")
                self.assertEqual(
                    (ROOT / relative).read_text(), original.replace(body, proposed_body, 1),
                )
                clauses = []
                for directory in ("", "proposals/"):
                    source = (ROOT / f"proofs/correctness/slice/{directory}{api}.rs").read_text()
                    self.assertIn(
                        f"pub const fn {api}<T>(slice: &mut [T]) -> (result: Option<(&mut T, &mut [T])>)",
                        source,
                    )
                    self.assertNotRegex(
                        source,
                        r"\b(?:assume_specification|external_body|assume|admit|requires|Copy|Eq|Default|where)\b|'static",
                    )
                    self.assertNotRegex(source, rf"(?:\.|::){api}\s*(?:::<[^>]*>)?\(")
                    self.assertIn("specs/slice/mutable_splits_post.rs", source)
                    self.assertNotIn("specs/slice/mutable_splits.rs", source)
                    clauses.append(source[source.index("    ensures\n"):source.index("\n{\n")])
                self.assertEqual(clauses[0], clauses[1])
                for observation in (
                    "old(slice)@", "Some((*value, remainder@))",
                    "Some((*final(value), final(remainder)@))", "final(slice)@",
                ):
                    self.assertIn(observation, clauses[0])

    def test_proposals_use_the_existing_remainder_length_fact_only(self):
        for api, remainder in (("split_first_mut", "tail"), ("split_last_mut", "init")):
            with self.subTest(api=api):
                source = (ROOT / f"proofs/correctness/slice/proposals/{api}.rs").read_text()
                self.assertEqual(source.count("proof {"), 1)
                self.assertIn(f"vstd::slice::mut_ref_slice_len_eq(&{remainder});", source)
                self.assertNotIn("mutable_splits_state", source)

    def test_candidates_state_and_original_failures_are_preserved(self):
        unchanged = [
            "specs/mod.rs", "specs/slice/mod.rs", "specs/slice/mutable_splits.rs",
            "specs/slice/mutable_splits_post.rs", "specdet.toml",
            "proofs/completeness/slice/mutable_splits_state.rs",
            "tests/mutable_split_state.rs", "tests/mutable_split_contract_clients.rs",
        ]
        for api in APIS:
            unchanged.extend((
                f"proofs/correctness/slice/proposals/{api}.rs",
                f"proofs/completeness/slice/inputs/{api}.rs",
                f"proofs/completeness/slice/history/{api}_direct.rs",
                f"logs/mutable-splits-proposal/direct/{api}/analyze.json",
                f"logs/mutable-splits-proposal/correctness/initial/original/{api}/verus.log",
            ))
        for relative in unchanged:
            with self.subTest(path=relative):
                expected = (PRESERVED / relative).read_bytes()
                if relative == "specs/mod.rs":
                    expected += b'\n#[path = "slice/split_off.rs"]\npub mod slice_split_off;\n'
                self.assertEqual((ROOT / relative).read_bytes(), expected)

    def test_behavior_changes_only_the_current_implementation_label(self):
        original = (PRESERVED / "tests/mutable_split_proposal_behavior.rs").read_text()
        expected = original.replace(
            "// Isolated comparison only; no adoption or source-equivalence claim.",
            "// Compare authority patterns, adopted current proofs and public methods.",
            1,
        ).replace("SLICE_MUTABLE_SPLIT_PROPOSALS_SOURCE", "SLICE_MUTABLE_SPLITS_SOURCE").replace(
            "proposal::", "adopted::",
        )
        current = (ROOT / "tests/mutable_split_behavior.rs").read_text()
        self.assertEqual(current, expected)
        self.assertEqual(current.count("#[test]"), 19)
        self.assertFalse((ROOT / "tests/mutable_split_proposal_behavior.rs").exists())

    def test_first_correspondence_contains_the_exact_existing_vstd_clauses(self):
        upstream = (ROOT / "toolchain/upstream/source/vstd/std_specs/slice.rs").read_text()
        declaration = re.search(
            r"pub assume_specification<T> \[ <\[T\]>::split_first_mut \]"
            r".*?ensures\s+(.*?)\s+no_unwind", upstream, re.DOTALL,
        )
        self.assertIsNotNone(declaration)
        self.assertNotIn("<[T]>::split_last_mut", upstream)
        state = (ROOT / "proofs/completeness/slice/mutable_splits_state.rs").read_text()
        lemma = state[:state.index("pub proof fn last_candidate_correspondence")]
        for clause in declaration[1].strip().split(",\n"):
            self.assertIn(
                compact(clause.strip().replace("ret", "result")), compact(lemma),
            )
        self.assertIn("<==>", lemma)

    def test_analysis_inputs_do_not_presupply_either_observation(self):
        for api in APIS:
            with self.subTest(api=api):
                source = (ROOT / f"proofs/completeness/slice/inputs/{api}.rs").read_text()
                signature = (
                    f"pub fn {api}_observation<T>("
                    "input_initial: Ghost<Seq<T>>,"
                    "caller_final: Ghost<Option<(T, Seq<T>)>>,"
                    ") -> (result: Ghost<(Option<(T, Seq<T>)>, Seq<T>)>)"
                )
                self.assertIn(compact(signature), compact(source))
                self.assertEqual(source.count("    requires\n"), 1)
                self.assertIn("None => input_initial@.len() == 0,", source)
                self.assertIn("written_remainder.len() + 1 == input_initial@.len(),", source)
                self.assertIn(
                    f"state::post::{api}_post(input_initial@, caller_final@, result@),", source,
                )
                self.assertIn("state::all_caller_writes(input_initial@, caller_final@);", source)
                self.assertNotRegex(
                    source, r"\b(?:assume_specification|external_body|assume|admit|Copy|Eq|Default|where)\b|'static",
                )

    def test_direct_failures_remain_historical_not_active_targets(self):
        for api in APIS:
            with self.subTest(api=api):
                self.assertFalse((ROOT / f"proofs/completeness/slice/inputs/{api}_direct.rs").exists())
                history = (ROOT / f"proofs/completeness/slice/history/{api}_direct.rs").read_text()
                self.assertIn(f"pub assume_specification<T>[source::{api}::<T>]", history)
                self.assertIn("Option<(&mut T, &mut [T])>", history)
                self.assertIn(f"contracts::{api}_post(", history)

    def test_empty_witness_requires_no_element_and_non_copy_writes_are_unrestricted(self):
        regressions = (ROOT / "tests/mutable_split_state.rs").read_text()
        self.assertIn("pub proof fn empty_without_an_element<T>()", regressions)
        self.assertIn("state::all_caller_writes(Seq::<T>::empty(), None);", regressions)
        self.assertIn("state::all_caller_writes(initial, Some((element, remainder)));", regressions)
        state = (ROOT / "proofs/completeness/slice/mutable_splits_state.rs").read_text()
        self.assertEqual(state.count("None => (None, seq![]),"), 2)
        self.assertNotIn("unwrap_or", state)

    def test_aggregate_only_appends_the_new_binding_module(self):
        before = (ROOT / "logs/mutable-endpoints/adoption-before/specs/mod.rs").read_bytes()
        expected = before + b'\n#[path = "slice/mutable_splits.rs"]\npub mod slice_mutable_splits;\n'
        expected += b'\n#[path = "slice/split_off.rs"]\npub mod slice_split_off;\n'
        self.assertEqual((ROOT / "specs/mod.rs").read_bytes(), expected)


if __name__ == "__main__":
    unittest.main()
