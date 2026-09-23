import csv
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src")
SPANS = {"make_ascii_uppercase": (173, 181), "make_ascii_lowercase": (195, 203)}


def compact(text):
    return re.sub(r"\s+", "", re.sub(r"//[^\n]*", "", text))


class AsciiContracts(unittest.TestCase):
    def test_reviewed_slice_calls_preserve_execution_and_const_signatures(self):
        lines = (SOURCE / "slice/ascii.rs").read_text().splitlines()
        for api, (start, end) in SPANS.items():
            with self.subTest(api=api):
                original = lines[start - 1:end]
                self.assertEqual(original[0].strip(), f"pub const fn {api}(&mut self) {{")
                proof = (ROOT / f"proofs/correctness/slice/{api}.rs").read_text()
                self.assertIn(f"pub const fn {api}(slice: &mut [u8])", proof)
                body = re.search(r"^\{\n(.*?)^\}", proof, re.MULTILINE | re.DOTALL)[1]
                body = re.sub(
                    r"(while i < slice\.len\(\))\n.*?^    \{",
                    r"\1 {", body, flags=re.MULTILINE | re.DOTALL,
                )
                body = re.sub(
                    r"^    proof \{\n.*?^    \}\n", "", body,
                    flags=re.MULTILINE | re.DOTALL,
                )
                expected = re.sub(r"\bself\b", "slice", "\n".join(original[1:-1]))
                original_call = f"byte.{api}();"
                rebound_call = f"u8_ascii::{api}(byte);"
                self.assertEqual(expected.count(original_call), 1)
                self.assertEqual(body.count(rebound_call), 1)
                expected = expected.replace(original_call, rebound_call)
                self.assertEqual(compact(body), compact(expected))
                self.assertNotRegex(
                    proof, r"\b(?:requires|assume_specification|external_body|admit|assume)\b",
                )
                self.assertIn('#[path = "../../../specs/slice/ascii_post.rs"]', proof)
                self.assertIn('#[path = "../num/u8_ascii.rs"]\nmod u8_ascii;', proof)

    def test_reviewed_scalar_calls_preserve_operations_and_const_signatures(self):
        lines = (SOURCE / "num/mod.rs").read_text().splitlines()
        groups = {
            "u8_ascii_classify.rs": {
                "is_ascii_uppercase": (812, 814), "is_ascii_lowercase": (846, 848),
            },
            "u8_ascii.rs": {
                "to_ascii_uppercase": (639, 642), "to_ascii_lowercase": (664, 667),
                "make_ascii_uppercase": (716, 718), "make_ascii_lowercase": (742, 744),
            },
        }
        replacements = {
            "to_ascii_uppercase": (
                "byte.is_ascii_lowercase()", "classify::is_ascii_lowercase(byte)",
            ),
            "to_ascii_lowercase": (
                "byte.is_ascii_uppercase()", "classify::is_ascii_uppercase(byte)",
            ),
            "make_ascii_uppercase": ("byte.to_ascii_uppercase()", "to_ascii_uppercase(byte)"),
            "make_ascii_lowercase": ("byte.to_ascii_lowercase()", "to_ascii_lowercase(byte)"),
        }
        for filename, methods in groups.items():
            proof = (ROOT / "proofs/correctness/num" / filename).read_text()
            self.assertNotRegex(
                proof, r"\b(?:requires|assume_specification|external_body|admit|assume)\b",
            )
            for api, (start, end) in methods.items():
                with self.subTest(api=api):
                    body = re.search(
                        rf"pub const fn {api}\(.*?^\{{\n(.*?)^\}}",
                        proof, re.MULTILINE | re.DOTALL,
                    )[1]
                    body = re.sub(
                        r"^    proof \{\n.*?^    \}\n", "", body,
                        flags=re.MULTILINE | re.DOTALL,
                    )
                    expected = re.sub(r"\bself\b", "byte", "\n".join(lines[start:end - 1]))
                    if api in replacements:
                        original_call, rebound_call = replacements[api]
                        self.assertEqual(expected.count(original_call), 1)
                        self.assertEqual(body.count(rebound_call), 1)
                        expected = expected.replace(original_call, rebound_call)
                    self.assertEqual(compact(body), compact(expected))
                    receiver = "&mut u8" if api.startswith("make_") else "&u8"
                    result = "" if api.startswith("make_") else (
                        " -> (result: bool)" if api.startswith("is_") else " -> (result: u8)"
                    )
                    self.assertIn(f"pub const fn {api}(byte: {receiver}){result}\n", proof)
        self.assertIn(
            lines[538].strip(), (ROOT / "proofs/correctness/num/u8_ascii.rs").read_text(),
        )
        self.assertIn(
            '#[path = "u8_ascii_classify.rs"]\nmod classify;',
            (ROOT / "proofs/correctness/num/u8_ascii.rs").read_text(),
        )

    def test_real_bindings_observe_only_complete_final_sequences(self):
        binding = (ROOT / "specs/slice/ascii.rs").read_text()
        self.assertEqual(binding.count("pub assume_specification"), 2)
        self.assertNotIn("requires", binding)
        self.assertIn(
            '#[path = "slice/ascii.rs"]\npub mod slice_ascii;',
            (ROOT / "specs/mod.rs").read_text(),
        )
        for api in SPANS:
            case = api.removeprefix("make_ascii_")
            expected = (
                f"pub assume_specification[<[u8]>::{api}](slice:&mut[u8])"
                f"ensures post::{case}_post(old(slice)@,final(slice)@),;"
            )
            self.assertIn(compact(expected), compact(binding))
            proof = (ROOT / f"proofs/correctness/slice/{api}.rs").read_text()
            self.assertIn(
                f"ensurescontracts::{case}_post(old(slice)@,final(slice)@),", compact(proof),
            )
        predicates = (ROOT / "specs/slice/ascii_post.rs").read_text()
        self.assertIn("if b'a' <= byte <= b'z' { (byte - 32) as u8 } else { byte }", predicates)
        self.assertIn("if b'A' <= byte <= b'Z' { (byte + 32) as u8 } else { byte }", predicates)
        for case in ("uppercase", "lowercase"):
            self.assertIn(
                f"result =~= initial.map_values(|byte: u8| {case}_byte(byte))", predicates,
            )
        self.assertNotRegex(predicates, r"\b(?:requires|assume|admit|uninterp|external_body)\b")

    def test_analysis_never_takes_the_final_sequence_as_input(self):
        for api in SPANS:
            case = api.removeprefix("make_ascii_")
            adapter = (ROOT / f"proofs/completeness/slice/inputs/{api}.rs").read_text()
            signature = (
                f"pub fn {api}_observation(initial: Ghost<Seq<u8>>) "
                "-> (result: Ghost<Seq<u8>>)"
            )
            self.assertIn(signature, adapter)
            self.assertIn(f"state::post::{case}_post(initial@, result@)", adapter)
            self.assertNotRegex(
                adapter, r"\b(?:requires|assume_specification|external_body|admit|assume)\b",
            )
        state = (ROOT / "proofs/completeness/slice/ascii_state.rs").read_text()
        self.assertIn("candidate_correspondence(slice: &mut [u8])", state)
        self.assertIn("lawful_outputs(initial: Seq<u8>)", state)
        self.assertIn("(left =~= right) <==> (left@ =~= right@)", state)
        self.assertNotRegex(state, r"\b(?:requires|assume_specification|external_body|admit|assume)\b")

    def test_inventory_keeps_exact_source_docs_and_stable_const_domain(self):
        with (ROOT / "inventory/apis.tsv").open() as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        self.assertEqual(len(rows), 331)
        for api, (start, end) in SPANS.items():
            row = next(row for row in rows if row["canonical_id"] == f"<[u8]>::{api}")
            self.assertEqual(row["signature"], f"pub const fn {api}(&mut self)")
            self.assertEqual(row["source_span"], f"slice/ascii.rs:{start}-{end}")
            self.assertEqual(
                json.loads(row["doc_spans"]),
                [f"slice/ascii.rs:{line}-{line}" for line in range(start - 12, start - 3)],
            )
            self.assertEqual(row["stable_since"], "1.23.0")
            self.assertTrue(row["const_stability"].startswith("stable:"))
            self.assertIn('since = "1.84.0"', row["const_stability"])


if __name__ == "__main__":
    unittest.main()
