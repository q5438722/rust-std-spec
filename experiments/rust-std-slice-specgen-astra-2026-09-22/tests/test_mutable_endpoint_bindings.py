import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
APIS = ("first_mut", "last_mut")
PRESERVED = ROOT / "logs/mutable-endpoints/adoption-before"


def compact(text):
    return re.sub(r"\s+", "", text)


class MutableEndpointBindings(unittest.TestCase):
    def test_current_sources_change_only_the_exact_approved_bodies(self):
        saved_files = json.loads((PRESERVED / "files.json").read_text())
        for api, original_body, adopted_body in (
            (
                "first_mut",
                "    if let [first, ..] = slice { Some(first) } else { None }",
                "    if slice.len() == 0 { None } else { Some(&mut slice[0]) }",
            ),
            (
                "last_mut",
                "    if let [.., last] = slice { Some(last) } else { None }",
                "    if slice.len() == 0 {\n"
                "        None\n    } else {\n"
                "        let i = slice.len() - 1;\n"
                "        Some(&mut slice[i])\n    }",
            ),
        ):
            with self.subTest(api=api):
                relative = f"proofs/correctness/slice/{api}.rs"
                self.assertIn(relative, saved_files)
                original = (PRESERVED / relative).read_bytes()
                before = original_body.encode()
                self.assertEqual(original.count(before), 1)
                self.assertEqual(
                    (ROOT / relative).read_bytes(),
                    original.replace(before, adopted_body.encode(), 1),
                )

    def test_candidates_analysis_and_isolated_proposals_are_preserved_byte_for_byte(self):
        saved_files = json.loads((PRESERVED / "files.json").read_text())
        unchanged = [
            "specs/slice/mod.rs", "specs/slice/mutable_endpoints.rs",
            "proofs/completeness/slice/mutable_endpoints_state.rs",
            "tests/mutable_endpoint_state.rs",
        ]
        for api in APIS:
            unchanged.extend((
                f"proofs/correctness/slice/proposals/{api}.rs",
                f"proofs/completeness/slice/inputs/{api}.rs",
                f"proofs/completeness/slice/history/{api}_direct.rs",
                f"logs/mutable-endpoints-proposal/direct/{api}/analyze.json",
                f"logs/mutable-endpoints-proposal/correctness/original/{api}/verus.log",
            ))
        for relative in unchanged:
            with self.subTest(path=relative):
                self.assertIn(relative, saved_files)
                self.assertEqual(
                    (ROOT / relative).read_bytes(), (PRESERVED / relative).read_bytes(),
                )

    def test_native_behavior_only_relabels_the_adopted_implementation(self):
        original = (PRESERVED / "tests/mutable_endpoint_proposal_behavior.rs").read_text()
        expected = original.replace(
            "// Compare unchanged authority patterns, isolated proposals and public methods.",
            "// Compare authority patterns, adopted current proofs and public methods.",
            1,
        ).replace("proposal::", "adopted::")
        current = (ROOT / "tests/mutable_endpoint_behavior.rs").read_text()
        self.assertEqual(current, expected)
        self.assertEqual(current.count("#[test]"), 17)
        self.assertFalse((ROOT / "tests/mutable_endpoint_proposal_behavior.rs").exists())

    def test_pure_candidates_do_not_reregister_the_public_methods(self):
        candidate = (ROOT / "specs/slice/mutable_endpoints.rs").read_text()
        self.assertEqual(candidate.count("pub open spec fn "), 2)
        self.assertEqual(
            candidate.count("input_initial.len() == 0 && observations.1 =~= seq![]"), 2,
        )
        self.assertNotIn("observations.1 == seq![]", candidate)
        self.assertNotRegex(
            candidate, r"\b(?:assume_specification|external_body|axiom|assume|admit|requires)\b"
        )
        self.assertNotRegex(candidate, r"\b(?:Copy|Eq|Default|where)\b|'static")
        aggregate = (ROOT / "specs/mod.rs").read_text()
        self.assertEqual(
            aggregate.count(
                '#[path = "slice/mutable_endpoints.rs"]\npub mod slice_mutable_endpoints;'
            ),
            1,
        )

    def test_source_and_isolated_proposal_share_the_exact_candidate(self):
        for api in APIS:
            with self.subTest(api=api):
                clauses = []
                for directory in ("", "proposals/"):
                    source = (
                        ROOT / f"proofs/correctness/slice/{directory}{api}.rs"
                    ).read_text()
                    self.assertIn(
                        f"pub const fn {api}<T>(slice: &mut [T]) -> (result: Option<&mut T>)",
                        source,
                    )
                    self.assertNotRegex(
                        source, r"\b(?:assume_specification|external_body|assume|admit|requires)\b"
                    )
                    self.assertNotRegex(source, rf"(?:\.|::){api}\s*(?:::<[^>]*>)?\(")
                    start = source.index("    ensures\n")
                    end = source.index("\n{\n", start)
                    clauses.append(source[start:end])
                    self.assertIn("match result { None => None, Some(value) => Some(*value) }", source)
                    self.assertIn("match result { None => None, Some(value) => Some(*final(value)) }", source)
                    self.assertIn("final(slice)@", source)
                self.assertEqual(clauses[0], clauses[1])
                self.assertIn(f"contracts::{api}_post(", clauses[0])

    def test_state_equivalence_uses_the_existing_exact_upstream_clauses(self):
        state = (ROOT / "proofs/completeness/slice/mutable_endpoints_state.rs").read_text()
        upstream = (ROOT / "toolchain/upstream/source/vstd/std_specs/slice.rs").read_text()
        for api in APIS:
            with self.subTest(api=api):
                declaration = re.search(
                    rf"pub assume_specification<T> \[ <\[T\]>::{api} \]"
                    r".*?ensures\s+(.*?)\s+no_unwind",
                    upstream, re.DOTALL,
                )
                self.assertIsNotNone(declaration)
                empty, nonempty = declaration[1].strip().split(",\n")
                expected = [
                    clause.replace("res", "result")
                    for clause in (empty.strip(), nonempty.strip())
                ]
                lemma = re.search(
                    rf"pub proof fn {api.removesuffix('_mut')}_candidate_correspondence"
                    r"<T>.*?^\{\n\}",
                    state, re.MULTILINE | re.DOTALL,
                )
                self.assertIsNotNone(lemma)
                for clause in expected:
                    self.assertIn(compact(clause).replace(",)", ")"), compact(lemma[0]).replace(",)", ")"))
                self.assertIn("<==>", lemma[0])

    def test_analysis_inputs_do_not_presupply_the_final_slice(self):
        for api in APIS:
            with self.subTest(api=api):
                source = (ROOT / f"proofs/completeness/slice/inputs/{api}.rs").read_text()
                expected = (
                    f"pub fn {api}_observation<T>("
                    "input_initial: Ghost<Seq<T>>, caller_final: Ghost<Option<T>>,"
                    ") -> (result: Ghost<(Option<T>, Seq<T>)>)"
                )
                self.assertIn(compact(expected), compact(source))
                self.assertEqual(source.count("    requires\n"), 1)
                self.assertIn(
                    "caller_final@.is_none() <==> input_initial@.len() == 0,", source
                )
                self.assertIn(
                    f"state::post::{api}_post(input_initial@, caller_final@, result@),", source
                )
                self.assertIn("state::all_caller_writes(input_initial@, caller_final@);", source)
                self.assertNotRegex(
                    source, r"\b(?:assume_specification|external_body|assume|admit|Copy|Eq|Default|where)\b|'static"
                )
                historical = (
                    ROOT / f"proofs/completeness/slice/history/{api}_direct.rs"
                ).read_text()
                self.assertIn(f"pub assume_specification<T>[source::{api}::<T>]", historical)
                self.assertIn("Option<&mut T>", historical)

    def test_empty_environment_has_no_element_parameter(self):
        regressions = (ROOT / "tests/mutable_endpoint_state.rs").read_text()
        self.assertIn("pub proof fn empty_without_an_element<T>()", regressions)
        self.assertIn("state::all_caller_writes(Seq::<T>::empty(), None);", regressions)
        state = (ROOT / "proofs/completeness/slice/mutable_endpoints_state.rs").read_text()
        self.assertEqual(state.count("None => (None, seq![]),"), 2)
        self.assertNotIn("unwrap_or", state)


if __name__ == "__main__":
    unittest.main()
