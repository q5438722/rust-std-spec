from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
APIS = ("split_off_first", "split_off_last")
AGGREGATE_APPEND = b'\n#[path = "slice/split_off.rs"]\npub mod slice_split_off;\n'


def compact(text):
    return re.sub(r"\s+", "", text)


class SplitOffBindings(unittest.TestCase):
    def test_both_public_bindings_are_missing_from_the_selected_vstd(self):
        upstream = "\n".join(
            path.read_text() for path in (ROOT / "toolchain/upstream/source/vstd").rglob("*.rs")
        )
        declarations = "\n".join(path.read_text() for path in (ROOT / "specs").rglob("*.rs"))
        for api in APIS:
            with self.subTest(api=api):
                self.assertNotRegex(upstream, rf"\b{api}\b")
                self.assertEqual(len(re.findall(
                    rf"assume_specification<'a,\s*T>\s*\[\s*<\[T\]>::{api}\s*\]",
                    declarations,
                )), 1)
        self.assertIn("<[T]>::split_first", upstream)
        self.assertNotRegex(upstream, r"<\[T\]>::split_last\b")

    def test_source_public_binding_and_checker_use_the_same_complete_candidate(self):
        bindings = (ROOT / "specs/slice/split_off.rs").read_text()
        for api in APIS:
            with self.subTest(api=api):
                source = (ROOT / f"proofs/correctness/slice/{api}.rs").read_text()
                analysis = (ROOT / f"proofs/completeness/slice/inputs/{api}.rs").read_text()
                clause = source[source.index("    ensures\n"):source.index("\n{\n")]
                self.assertIn(compact(clause), compact(analysis))
                self.assertIn(compact(clause.replace("contracts::", "post::")), compact(bindings))
                for observation in ("(*old(slice))@", "Some(*value)", "(*final(slice))@"):
                    self.assertIn(observation, clause)
                self.assertNotIn("final(value)", clause)
                self.assertNotIn("caller_final", source + analysis + bindings)
                self.assertIn(
                    f"pub const fn {api}<'a, T>(slice: &mut &'a [T]) -> (result: Option<&'a T>)",
                    source,
                )
                self.assertNotRegex(
                    re.sub(r"//[^\n]*", "", source + analysis + bindings),
                    r"\b(?:requires|Copy|Eq|Default|where)\b|'static",
                )

    def test_pure_candidates_keep_variant_value_and_the_whole_ordered_remainder(self):
        post = (ROOT / "specs/slice/split_off_post.rs").read_text()
        self.assertEqual(post.count("pub open spec fn "), 2)
        self.assertEqual(
            post.count("None => input_initial.len() == 0 && observations.1 =~= input_initial"), 2,
        )
        self.assertEqual(post.count("&&& input_initial.len() > 0"), 2)
        self.assertIn("&&& value == input_initial[0]", post)
        self.assertIn("&&& value == input_initial[input_initial.len() - 1]", post)
        self.assertIn("observations.1 =~= input_initial.subrange(1, input_initial.len() as int)", post)
        self.assertIn("observations.1 =~= input_initial.subrange(0, input_initial.len() - 1)", post)
        self.assertNotIn("observations.1.len()", post)
        self.assertNotRegex(
            post,
            r"\b(?:assume_specification|external_body|axiom|assume|admit|requires|mod|Copy|Eq|Default|where)\b|'static",
        )

    def test_formal_sources_do_not_call_or_assume_the_target(self):
        for api, endpoint in (("split_off_first", "first"), ("split_off_last", "last")):
            with self.subTest(api=api):
                source = (ROOT / f"proofs/correctness/slice/{api}.rs").read_text()
                self.assertNotRegex(source, r"\b(?:assume_specification|external_body|assume|admit)\b")
                self.assertNotRegex(source, rf"(?:\.|::){api}\s*\(")
                self.assertIn("specs/slice/split_off_post.rs", source)
                self.assertNotIn("specs/slice/split_off.rs", source)
                call = (
                    "slice.split_first()" if endpoint == "first"
                    else "split_dependency::split_last(*slice)"
                )
                self.assertIn(
                    f"let Some(({endpoint}, rem)) = {call} else {{ return None }};\n"
                    f"    *slice = rem;\n    Some({endpoint})",
                    source,
                )

    def test_last_adopts_only_the_independently_permitted_call(self):
        before = ROOT / "logs/split-off-endpoints/adoption-before"
        relative = "proofs/correctness/slice/split_off_last.rs"
        original = (before / relative).read_text()
        expected = original.replace(
            '#[path = "../../../specs/slice/split_off_post.rs"]',
            '#[path = "../../../../specs/slice/split_off_post.rs"]',
        ).replace(
            "mod contracts;\n", 'mod contracts;\n#[path = "../split_last.rs"]\nmod split_dependency;\n', 1,
        ).replace(
            "// Rust 1.96 core/src/slice/mod.rs:5043-5065; body:5061-5064.",
            "// Isolated proposal for Rust 1.96 slice/mod.rs:5043-5065; not adopted.",
        ).replace("slice.split_last()", "split_dependency::split_last(*slice)", 1)
        proposal = (ROOT / "proofs/correctness/slice/proposals/split_off_last.rs").read_text()
        self.assertEqual(proposal, expected)
        self.assertFalse((ROOT / "proofs/correctness/slice/proposals/split_off_first.rs").exists())
        self.assertNotIn("split_dependency", original)
        adopted = original.replace(
            "mod contracts;\n", 'mod contracts;\n#[path = "split_last.rs"]\nmod split_dependency;\n', 1,
        ).replace("slice.split_last()", "split_dependency::split_last(*slice)", 1)
        self.assertEqual((ROOT / relative).read_text(), adopted)
        for relative in (
            "proofs/correctness/slice/split_off_first.rs",
            "proofs/correctness/slice/split_last.rs",
            "specs/slice/split_off_post.rs", "specs/slice/split_off.rs",
            "proofs/completeness/slice/split_off_state.rs",
            "proofs/completeness/slice/inputs/split_off_first.rs",
            "proofs/completeness/slice/inputs/split_off_last.rs",
        ):
            self.assertEqual((ROOT / relative).read_bytes(), (before / relative).read_bytes())

    def test_state_proofs_cover_totality_and_the_direct_reference_comparison(self):
        state = (ROOT / "proofs/completeness/slice/split_off_state.rs").read_text()
        self.assertEqual(state.count("pub proof fn "), 6)
        self.assertIn("pub proof fn all_initial_states<T>(input_initial: Seq<T>)", state)
        totality = state[state.index("pub proof fn all_initial_states"):state.index("pub proof fn first_reconstruction")]
        self.assertNotIn("requires", totality)
        self.assertEqual(totality.count("(None, input_initial)"), 2)
        self.assertIn("left->Some_0 == right->Some_0", state)
        self.assertIn("left_remaining =~= right_remaining", state)
        self.assertIn("left_remaining@", state)
        self.assertNotIn("caller_final", state)
        self.assertNotRegex(state, r"\b(?:assume_specification|external_body|assume|admit)\b")

    def test_clients_can_consume_again_reassign_and_drop_the_outer_slot(self):
        clients = (ROOT / "tests/split_off_contract_clients.rs").read_text()
        for name in (
            "consecutive_first", "consecutive_last", "alternating_and_exhaustion",
            "first_slot_can_be_reassigned", "last_slot_can_be_reassigned",
            "first_outlives_the_local_slot", "last_outlives_the_local_slot",
        ):
            self.assertIn(f"pub fn {name}", clients)
        self.assertEqual(clients.count("remaining = unrelated;"), 2)
        self.assertNotIn("final(remaining)", clients)

    def test_aggregate_preserves_the_previous_modules_exactly(self):
        previous = (ROOT / "logs/mutable-splits/adoption-before/specs/mod.rs").read_bytes()
        self.assertEqual((ROOT / "specs/mod.rs").read_bytes(), previous + AGGREGATE_APPEND)


if __name__ == "__main__":
    unittest.main()
