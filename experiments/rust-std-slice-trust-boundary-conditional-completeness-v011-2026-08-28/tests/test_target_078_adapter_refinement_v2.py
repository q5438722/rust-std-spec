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

import target_078_adapter_refinement_v2 as model


EVIDENCE = ROOT / "evidence/target_078_adapter_refinement_v2"
RESULT = EVIDENCE / "result.json"


class Target078AdapterRefinementModelTests(unittest.TestCase):
    def test_proof_is_constructive_trusted_free_and_nonempty(self) -> None:
        text = model.PROOF_PATH.read_text()
        binding = model.validate_proof(text)
        self.assertTrue(binding["trusted_free"])
        self.assertFalse(binding["precomputed_terminal_input"])
        self.assertEqual(
            binding["top_level_inputs"],
            [
                "boundary",
                "pre_call_callback_state",
                "left_identity",
                "right_identity",
            ],
        )
        self.assertEqual(
            tuple(binding["proof_obligations"]),
            model.REQUIRED_PROOFS,
        )
        self.assertEqual(binding["proof_count"], 11)
        self.assertEqual(
            tuple(binding["semantic_bridge"]["functions"]),
            tuple(model.VERUS_SEMANTIC_SIGNATURES),
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
            "ExactCallback",
            "ExactState",
            "selected_output",
            "final_state",
            "trace_input",
        ):
            self.assertNotIn(forbidden, text)

    def test_verus_and_smt_fields_bind_one_for_one(self) -> None:
        proof = model.validate_proof()
        smt = model.accepted_smt_binding()
        self.assertEqual(
            proof["struct_fields"]["ComparatorBoundary"],
            smt["datatype_fields"]["Boundary"],
        )
        self.assertEqual(
            proof["struct_fields"]["ComparatorAdapterFrame"],
            smt["datatype_fields"]["ComparatorAdapterFrame"],
        )
        self.assertEqual(proof["step_order"], list(model.STEP_ORDER))
        self.assertEqual(
            smt["exact_callback"]["compared_selectors"],
            ["e_callback_state", "e_panicked"],
        )

    def test_correspondence_is_ast_derived_and_field_complete(self) -> None:
        text = model.correspondence_query_text()
        model.validate_correspondence_query(text)
        self.assertIn("(ExactCallback", text)
        self.assertIn("(BoundaryOrdering", text)
        self.assertIn("(BoundaryNextState", text)
        self.assertIn("(BoundaryPanics", text)
        self.assertIn("(TargetAdapterIsLess", text)
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
        self.assertEqual(coverage["comparison_count"], 17)
        self.assertEqual(
            coverage["exact_callback_comparison_count"], 4
        )
        for field in model.SMT_FIELD_BINDINGS[
            "ComparatorAdapterFrame"
        ]:
            self.assertIn(
                f"(= ({field} accepted_frame) "
                f"({field} refined_frame))",
                text,
            )

    def test_each_mutation_changes_only_a_checked_function(self) -> None:
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

    def test_verus_valid_correspondence_mutations_are_sat(self) -> None:
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

    def test_boundary_excludes_target_answers_and_traces(self) -> None:
        manifest = model.boundary_manifest()
        self.assertTrue(manifest["narrower_than_target"])
        self.assertIn(
            "precomputed adapter transition or callback result",
            manifest["excluded"],
        )
        self.assertIn(
            "principal return or final selection state",
            manifest["excluded"],
        )
        self.assertIn(
            "callback-state update before panic propagation",
            manifest["source_derived_not_boundary"],
        )


class Target078AdapterRefinementArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not RESULT.is_file():
            raise AssertionError(
                "run tools/run_target_078_adapter_refinement_v2.py first"
            )
        cls.result = json.loads(RESULT.read_text())

    def test_verus_verified_nonzero_constructive_obligations(self) -> None:
        verus = self.result["verus"]
        self.assertEqual(verus["verified_obligations"], 11)
        self.assertTrue(verus["trusted_free"])
        self.assertFalse(verus["precomputed_terminal_or_answer_input"])
        self.assertEqual(verus["typecheck"]["exit_code"], 0)
        self.assertEqual(verus["verification"]["exit_code"], 0)
        self.assertEqual(
            verus["expected_summary"],
            "verification results:: 11 verified, 0 errors",
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
            list(
                model.SMT_FIELD_BINDINGS["ComparatorAdapterFrame"]
            ),
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

    def test_verus_valid_correspondence_mutations_are_rejected(self) -> None:
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
        for key in (
            "accepted_target_078_unchanged",
            "accepted_target_079_unchanged",
            "operational_v2_unchanged",
            "parser_repair_unchanged",
            "frozen_authorities_unchanged",
            "final_campaign_unchanged",
            "pipeline_state_unchanged",
        ):
            self.assertTrue(preservation[key])

    def test_classification_is_unchanged_and_review_pending(self) -> None:
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
