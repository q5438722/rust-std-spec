#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import target_079_adapter_refinement_v2 as model


EVIDENCE = ROOT / "evidence/target_079_adapter_refinement_v2"
RESULT = EVIDENCE / "result.json"


class Target079AdapterRefinementModelTests(unittest.TestCase):
    def test_proof_is_constructive_trusted_free_and_nonempty(self) -> None:
        text = model.PROOF_PATH.read_text()
        binding = model.validate_proof(text)
        self.assertTrue(binding["trusted_free"])
        self.assertFalse(binding["precomputed_terminal_input"])
        self.assertEqual(
            binding["top_level_inputs"],
            [
                "boundary",
                "state",
                "left_identity",
                "right_identity",
            ],
        )
        self.assertEqual(
            binding["proof_obligations"].keys(),
            set(model.REQUIRED_PROOFS),
        )
        self.assertEqual(binding["proof_count"], 13)
        self.assertEqual(
            list(binding["semantic_bridge"]["functions"]),
            list(model.VERUS_SEMANTIC_SIGNATURES),
        )
        self.assertEqual(
            binding["semantic_bridge"]["derivation"],
            "parsed-verus-expression-ast-to-smt",
        )
        for forbidden in (
            "external_body",
            "assume(",
            "admit(",
            "axiom",
            "ExactOperationalResult",
        ):
            self.assertNotIn(forbidden, text)

    def test_verus_and_smt_constructor_fields_bind_one_for_one(
        self,
    ) -> None:
        proof = model.validate_proof()
        smt = model.accepted_smt_binding()
        self.assertEqual(
            proof["struct_fields"]["OwnedKey"],
            smt["datatype_fields"]["OwnedKey"],
        )
        self.assertEqual(
            proof["struct_fields"]["AdapterFrame"],
            smt["datatype_fields"]["AdapterFrame"],
        )
        self.assertEqual(
            proof["struct_fields"]["KeyOrdDropBoundary"],
            smt["datatype_fields"]["Boundary"],
        )
        self.assertEqual(
            [
                field["field"]
                for field in proof["struct_field_types"][
                    "KeyOrdDropBoundary"
                ]
            ],
            [
                field["field"]
                for field in smt["datatype_sorts"]["Boundary"]
            ],
        )
        self.assertEqual(proof["step_order"], list(model.STEP_ORDER))
        self.assertEqual(smt["step_order"], list(model.STEP_ORDER))
        for verus, smt_name in model.SMT_FUNCTION_BINDINGS.items():
            self.assertEqual(
                proof["functions"][verus]["smt_function"],
                smt_name,
            )
            self.assertEqual(
                smt["definitions"][smt_name]["verus_function"],
                verus,
            )

    def test_correspondence_covers_every_helper_and_field(self) -> None:
        text = model.correspondence_query_text()
        model.validate_correspondence_query(text)
        self.assertIn("(AdapterTransition", text)
        self.assertIn("(RefinedAdapterTransition", text)
        self.assertIn(
            "mechanically translated from\n"
            "; the parsed Verus expression AST",
            text,
        )
        for refined in model.REFINED_FUNCTION_NAMES.values():
            self.assertEqual(
                text.count(f"(define-fun {refined} "),
                1,
            )
        coverage = model.correspondence_coverage()
        self.assertEqual(
            coverage["comparison_count"],
            113,
        )
        for field in model.SMT_FIELD_BINDINGS["AdapterFrame"]:
            self.assertIn(
                f"(= ({field} accepted_frame) "
                f"({field} refined_frame))",
                text,
            )

    def test_each_mutation_changes_only_its_checked_semantic(self) -> None:
        source = model.PROOF_PATH.read_text()
        mutations = {
            kind: model.mutate_proof(kind, source)
            for kind in (
                *model.MUTATION_KINDS,
                *model.CORRESPONDENCE_MUTATION_KINDS,
            )
        }
        self.assertEqual(
            set(mutations),
            {
                *model.MUTATION_KINDS,
                *model.CORRESPONDENCE_MUTATION_KINDS,
            },
        )
        self.assertEqual(len(set(mutations.values())), len(mutations))
        for mutated in mutations.values():
            self.assertNotEqual(mutated, source)

    def test_verus_valid_field_mutations_make_correspondence_sat(
        self,
    ) -> None:
        z3 = shutil.which("z3")
        if z3 is None:
            raise unittest.SkipTest("z3 is unavailable")
        source = model.PROOF_PATH.read_text()
        for kind in model.CORRESPONDENCE_MUTATION_KINDS:
            with self.subTest(kind=kind):
                query = model.correspondence_query_text(
                    model.mutate_proof(kind, source)
                )
                model.validate_correspondence_query(query)
                process = subprocess.run(
                    [z3, "-in"],
                    cwd=ROOT,
                    input=query,
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=30,
                )
                self.assertEqual(process.returncode, 0)
                self.assertEqual(process.stdout, "sat\n")
                self.assertEqual(process.stderr, "")

    def test_boundary_excludes_lifecycle_and_target_answers(self) -> None:
        manifest = model.boundary_manifest()
        self.assertTrue(manifest["narrower_than_target"])
        self.assertIn(
            "precomputed adapter result or lifecycle trace",
            manifest["excluded"],
        )
        self.assertIn(
            "principal return or final selection state",
            manifest["excluded"],
        )
        self.assertIn(
            "five-step evaluation and cleanup order",
            manifest["source_derived_not_boundary"],
        )


class Target079AdapterRefinementArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not RESULT.is_file():
            raise AssertionError(
                "run tools/run_target_079_adapter_refinement_v2.py first"
            )
        cls.result = json.loads(RESULT.read_text())

    def test_verus_verified_nonzero_constructive_obligations(self) -> None:
        verus = self.result["verus"]
        self.assertEqual(verus["verified_obligations"], 13)
        self.assertTrue(verus["trusted_free"])
        self.assertFalse(verus["precomputed_terminal_lifecycle_input"])
        self.assertEqual(verus["typecheck"]["exit_code"], 0)
        self.assertEqual(verus["verification"]["exit_code"], 0)
        self.assertEqual(
            verus["expected_summary"],
            "verification results:: 13 verified, 0 errors",
        )

    def test_all_paired_mutations_typecheck_then_fail_verification(
        self,
    ) -> None:
        mutations = self.result["mutation_matrix"]
        self.assertEqual(set(mutations), set(model.MUTATION_KINDS))
        for kind, record in mutations.items():
            with self.subTest(kind=kind):
                self.assertTrue(record["typecheck_passed"])
                self.assertTrue(record["verification_rejected"])
                self.assertEqual(record["typecheck"]["exit_code"], 0)
                self.assertNotEqual(
                    record["verification"]["exit_code"], 0
                )

    def test_correspondence_and_classification_replays_are_exact(self) -> None:
        correspondence = self.result["adapter_correspondence"]
        self.assertEqual(
            correspondence["solver"]["solver_result"], "unsat"
        )
        self.assertEqual(
            correspondence["compared_fields"],
            list(model.SMT_FIELD_BINDINGS["AdapterFrame"]),
        )
        self.assertEqual(
            correspondence["compared_functions"],
            list(model.VERUS_SEMANTIC_SIGNATURES),
        )
        self.assertEqual(
            correspondence["derivation"],
            "parsed-verus-expression-ast-to-smt",
        )
        self.assertEqual(
            correspondence["comparison_count"],
            model.correspondence_coverage()["comparison_count"],
        )
        expected = {
            "exact_output": "unsat",
            "full_state": "unsat",
            "nonvacuity": "sat",
        }
        for name, solver_result in expected.items():
            with self.subTest(name=name):
                replay = self.result["classification_replay"][name]
                self.assertEqual(
                    replay["solver"]["solver_result"], solver_result
                )
                self.assertEqual(
                    replay["accepted_source"]["sha256"],
                    replay["retained_copy"]["sha256"],
                )

    def test_verus_valid_correspondence_mutations_are_sat(self) -> None:
        mutations = self.result["correspondence_mutation_matrix"]
        self.assertEqual(
            set(mutations),
            set(model.CORRESPONDENCE_MUTATION_KINDS),
        )
        for kind, record in mutations.items():
            with self.subTest(kind=kind):
                self.assertTrue(record["typecheck_passed"])
                self.assertTrue(record["verification_passed"])
                self.assertTrue(record["correspondence_rejected"])
                self.assertEqual(record["typecheck"]["exit_code"], 0)
                self.assertEqual(record["verification"]["exit_code"], 0)
                self.assertEqual(
                    record["solver"]["solver_result"], "sat"
                )

    def test_solver_artifacts_replay_directly(self) -> None:
        z3 = shutil.which("z3")
        if z3 is None:
            raise unittest.SkipTest("z3 is unavailable")
        cases = {
            EVIDENCE / "adapter_correspondence.smt2": "unsat\n",
            EVIDENCE / "classification_replay/exact_output.smt2": (
                "unsat\n"
            ),
            EVIDENCE / "classification_replay/full_state.smt2": (
                "unsat\n"
            ),
            EVIDENCE / "classification_replay/nonvacuity.smt2": "sat\n",
        }
        cases.update(
            {
                EVIDENCE
                / "correspondence_mutations"
                / kind
                / "adapter_correspondence.smt2": "sat\n"
                for kind in model.CORRESPONDENCE_MUTATION_KINDS
            }
        )
        for path, expected in cases.items():
            with self.subTest(path=path.name):
                process = subprocess.run(
                    [z3, "-smt2", str(path)],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=30,
                )
                self.assertEqual(process.returncode, 0)
                self.assertEqual(process.stdout, expected)
                self.assertEqual(process.stderr, "")

    def test_protected_certifications_remain_byte_identical(self) -> None:
        preservation = self.result["preservation"]
        for family in ("protected_trees", "protected_files"):
            for record in preservation[family].values():
                self.assertEqual(
                    record["before_sha256"], record["after_sha256"]
                )
        self.assertTrue(preservation["operational_v1_unchanged"])
        self.assertTrue(preservation["operational_v2_unchanged"])
        self.assertTrue(preservation["parser_repair_unchanged"])
        self.assertTrue(preservation["pipeline_state_unchanged"])

    def test_classification_is_explicitly_unchanged_and_review_pending(
        self,
    ) -> None:
        self.assertFalse(self.result["classification_changed"])
        self.assertEqual(
            self.result["classification"],
            {
                "exact_output_determinism_status": (
                    "conditional-complete"
                ),
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            },
        )
        self.assertEqual(
            self.result["independent_review"],
            {"required": True, "status": "pending", "verdict": None},
        )
        self.assertEqual(self.result["stage_transition"], "disabled")


if __name__ == "__main__":
    unittest.main()
