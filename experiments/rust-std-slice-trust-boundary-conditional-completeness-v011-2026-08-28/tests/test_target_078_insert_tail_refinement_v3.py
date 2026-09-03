#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import target_078_insert_tail_refinement_v3 as model
import preservation_policy_v2 as policy_v2
import preservation_policy_v3 as policy_v3


EVIDENCE = ROOT / "evidence/target_078_insert_tail_refinement_v3"
RESULT = EVIDENCE / "result.json"


class Target078InsertTailRefinementModelTests(unittest.TestCase):
    def test_proof_is_constructive_trusted_free_and_nonempty(self) -> None:
        text = model.PROOF_PATH.read_text()
        binding = model.validate_proof(text)
        self.assertTrue(binding["trusted_free"])
        self.assertFalse(binding["precomputed_terminal_or_answer_input"])
        self.assertEqual(binding["proof_count"], 13)
        self.assertEqual(
            tuple(binding["proof_obligations"]),
            model.REQUIRED_PROOFS,
        )
        self.assertEqual(
            tuple(binding["semantic_bridge"]["functions"]),
            tuple(model.VERUS_SEMANTIC_SIGNATURES),
        )
        self.assertEqual(
            binding["semantic_bridge"]["derivation"],
            "parsed-verus-expression-ast-to-smt",
        )
        self.assertEqual(
            tuple(binding["fail_closed_guard_functions"]),
            model.PINNED_GUARD_FUNCTIONS,
        )
        self.assertEqual(
            binding["fail_closed_guard_sha256"],
            model.EXPECTED_GUARD_SHA256,
        )
        for forbidden in (
            "external_body",
            "assume(",
            "admit(",
            "ExactState",
            "ExactInsertTail",
            "selected_output",
            "final_state",
            "answer_encoding",
            "trace_input",
            "terminal_result",
        ):
            self.assertNotIn(forbidden, text)

    def test_verus_and_exact_state_fields_bind_one_for_one(self) -> None:
        proof = model.validate_proof()
        smt = model.accepted_smt_binding()
        self.assertEqual(
            proof["struct_fields"]["ComparatorBoundary"],
            smt["datatype_fields"]["Boundary"],
        )
        self.assertEqual(
            proof["struct_fields"]["InsertTailState"],
            smt["datatype_fields"]["ExactState"],
        )
        self.assertEqual(
            list(model.SMT_FIELD_BINDINGS["InsertTailState"]),
            ["e_sequence", "e_callback_state", "e_panicked"],
        )
        self.assertEqual(
            set(smt["definitions"]),
            {"ExactInsertTailLoop", "ExactInsertTail"},
        )

    def test_correspondence_is_ast_derived_and_full_valid_domain(self) -> None:
        text = model.correspondence_query_text()
        model.validate_correspondence_query(text)
        self.assertIn("mechanically translated", text)
        self.assertIn("(define-fun-rec RefinedInsertTailLoop ", text)
        self.assertIn("(define-fun RefinedInsertTail ", text)
        self.assertIn("(ExactInsertTailLoop", text)
        self.assertIn("(ExactInsertTail", text)
        for marker in (
            "(<= 0 loop_begin)",
            "(<= loop_begin loop_sift)",
            "(= loop_gap (+ loop_sift 1))",
            "(< loop_gap loop_sequence_len)",
            "(=> (> loop_sift loop_begin)",
            "(<= 0 entry_begin)",
            "(< entry_begin entry_tail)",
            "(< entry_tail entry_sequence_len)",
        ):
            self.assertIn(marker, text)
        for field in model.SMT_FIELD_BINDINGS["InsertTailState"]:
            self.assertIn(
                f"(not (= ({field} exact_loop_parent) "
                f"({field} refined_loop_parent)))",
                text,
            )
            self.assertIn(
                f"(not (= ({field} exact_entry_parent) "
                f"({field} refined_entry_parent)))",
                text,
            )
        coverage = model.correspondence_coverage()
        self.assertEqual(coverage["loop_result_comparison_count"], 3)
        self.assertEqual(coverage["entry_result_comparison_count"], 3)
        self.assertEqual(
            coverage["proof_rule"],
            "field-complete well-founded induction on sift - begin, "
            "followed by entry-point lifting",
        )

    def test_correspondence_replays_unsat_directly(self) -> None:
        z3 = shutil.which("z3")
        if z3 is None:
            raise unittest.SkipTest("z3 is unavailable")
        process = subprocess.run(
            [z3, "-in"],
            cwd=ROOT,
            input=model.correspondence_query_text(),
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stdout, "unsat\n")
        self.assertEqual(process.stderr, "")

    def test_required_source_mutations_are_distinct(self) -> None:
        source = model.PROOF_PATH.read_text()
        mutations = {
            kind: model.mutate_proof(kind, source)
            for kind in model.MUTATION_KINDS
        }
        self.assertEqual(
            set(mutations),
            {
                "operand-order",
                "lookup-state",
                "shift-source",
                "shift-destination",
                "gap-advancement",
                "normal-restoration",
                "base-restoration",
                "panic-restoration",
                "callback-next-state",
                "panic-propagation",
            },
        )
        self.assertEqual(len(set(mutations.values())), len(mutations))
        for mutated in mutations.values():
            self.assertNotEqual(mutated, source)

    def test_domain_and_preservation_guards_fail_closed(self) -> None:
        source = model.PROOF_PATH.read_text()
        mutations = (
            source.replace(
                "&& begin < tail",
                "&& begin >= tail",
                1,
            ),
            source.replace(
                "&& gap == sift + 1",
                "&& gap == sift",
                1,
            ),
            source.replace(
                "state.e_sequence.update(gap, temporary)",
                "state.e_sequence",
                1,
            ),
            source.replace(
                "boundary_panics(boundary, lookup_state, left, right)",
                "true",
                1,
            ),
        )
        for mutated in mutations:
            with self.subTest():
                self.assertNotEqual(mutated, source)
                with self.assertRaisesRegex(
                    ValueError, "source-sensitive fragment changed"
                ):
                    model.validate_proof(mutated)
        strengthened_to_vacuity = source.replace(
            "&& tail < state.e_sequence.len()\n}",
            "&& tail < state.e_sequence.len()\n"
            "        && false\n}",
            1,
        )
        with self.assertRaisesRegex(
            ValueError, "guard function body changed"
        ):
            model.validate_proof(strengthened_to_vacuity)

    def test_required_witness_queries_are_sat_with_models(self) -> None:
        z3 = shutil.which("z3")
        if z3 is None:
            raise unittest.SkipTest("z3 is unavailable")
        self.assertEqual(
            set(model.WITNESS_KINDS),
            {
                "no-shift",
                "multi-shift",
                "insert-at-begin",
                "panic-after-shift",
            },
        )
        for kind in model.WITNESS_KINDS:
            with self.subTest(kind=kind):
                query = model.witness_query_text(kind)
                model.validate_witness_query(kind, query)
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
                self.assertTrue(process.stdout.startswith("sat\n("))
                self.assertEqual(process.stderr, "")

    def test_boundary_excludes_results_answers_and_traces(self) -> None:
        manifest = model.boundary_manifest()
        self.assertTrue(manifest["narrower_than_target"])
        self.assertTrue(manifest["arbitrary_valid_range"])
        self.assertIn(
            "precomputed loop result or terminal result",
            manifest["excluded"],
        )
        self.assertIn("selected output or final state", manifest["excluded"])
        self.assertIn("answer encoding", manifest["excluded"])
        self.assertIn("execution trace", manifest["excluded"])
        self.assertIn(
            "panic-time guard restoration",
            manifest["source_derived_not_boundary"],
        )
        self.assertIn(
            "callback-state update before panic propagation",
            manifest["source_derived_not_boundary"],
        )

    def test_final_inventory_uses_mid_campaign_policy_validation(
        self,
    ) -> None:
        checks: list[bool] = []
        original = policy_v3.base._validate_operational_v2_inventory

        def validate_operational_inventory(
            payload: dict[str, object],
            *,
            root: Path,
            validate_all_records: bool = True,
        ) -> dict[str, list[dict[str, object]]]:
            checks.append(validate_all_records)
            return original(
                payload,
                root=root,
                validate_all_records=validate_all_records,
            )

        with mock.patch.object(
            policy_v3.base,
            "_validate_operational_v2_inventory",
            side_effect=validate_operational_inventory,
        ):
            groups = policy_v3.final_campaign_groups()

        self.assertEqual(checks, [False])
        self.assertEqual(
            set(groups),
            {
                "preexisting_evidence",
                "frozen_inputs",
                "authority_ledgers",
                "accepted_incremental_reviews",
            },
        )


class Target078InsertTailRefinementArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not RESULT.is_file():
            raise AssertionError(
                "run tools/run_target_078_insert_tail_refinement_v3.py first"
            )
        cls.result = json.loads(RESULT.read_text())

    def test_verus_verified_nonzero_trusted_free_obligations(self) -> None:
        verus = self.result["verus"]
        self.assertEqual(verus["verified_obligations"], 14)
        self.assertTrue(verus["trusted_free"])
        self.assertFalse(verus["precomputed_terminal_or_answer_input"])
        self.assertEqual(verus["typecheck"]["exit_code"], 0)
        self.assertEqual(verus["verification"]["exit_code"], 0)
        self.assertEqual(
            verus["expected_summary"],
            "verification results:: 14 verified, 0 errors",
        )

    def test_every_required_mutation_is_sensitive(self) -> None:
        mutations = self.result["mutation_matrix"]
        self.assertEqual(set(mutations), set(model.MUTATION_KINDS))
        for kind, record in mutations.items():
            with self.subTest(kind=kind):
                self.assertTrue(record["typecheck_passed"])
                self.assertEqual(record["typecheck"]["exit_code"], 0)
                self.assertEqual(
                    record["sensitivity_result"],
                    "verus-rejected-and-correspondence-sat",
                )
                self.assertTrue(record["verification_rejected"])
                self.assertNotEqual(
                    record["verification"]["exit_code"], 0
                )
                self.assertEqual(record["correspondence_result"], "sat")
                self.assertEqual(record["solver"]["solver_result"], "sat")

    def test_correspondence_is_unsat_and_field_complete(self) -> None:
        correspondence = self.result["insert_tail_correspondence"]
        self.assertEqual(correspondence["solver_result"], "unsat")
        self.assertEqual(
            correspondence["solver"]["solver_result"], "unsat"
        )
        self.assertEqual(
            correspondence["derivation"],
            "parsed-verus-expression-ast-to-smt",
        )
        self.assertEqual(
            correspondence["compared_state_fields"],
            list(model.SMT_FIELD_BINDINGS["InsertTailState"]),
        )
        self.assertEqual(
            correspondence["bound_boundary_fields"],
            list(model.SMT_FIELD_BINDINGS["ComparatorBoundary"]),
        )
        self.assertEqual(
            correspondence["valid_domains"],
            model.correspondence_coverage()["valid_domains"],
        )

    def test_all_nonvacuity_witnesses_retain_sat_models(self) -> None:
        witnesses = self.result["nonvacuity_witnesses"]
        self.assertEqual(set(witnesses), set(model.WITNESS_KINDS))
        self.assertEqual(witnesses["no-shift"]["shift_count"], 0)
        self.assertEqual(witnesses["multi-shift"]["shift_count"], 2)
        at_begin = witnesses["insert-at-begin"]
        self.assertEqual(at_begin["shift_count"], 2)
        self.assertTrue(at_begin["reached_begin"])
        panic = witnesses["panic-after-shift"]
        self.assertEqual(panic["shift_count_before_panic"], 1)
        self.assertTrue(panic["panicked"])
        self.assertEqual(panic["retained_callback_state"], 7)
        for kind, record in witnesses.items():
            with self.subTest(kind=kind):
                self.assertEqual(record["solver_result"], "sat")
                self.assertEqual(
                    record["solver"]["solver_result"], "sat"
                )
                model_path = ROOT / record["model"]["path"]
                self.assertTrue(model_path.read_text().startswith("("))
                self.assertGreater(record["model"]["bytes"], 0)

    def test_solver_artifacts_replay_directly(self) -> None:
        z3 = shutil.which("z3")
        if z3 is None:
            raise unittest.SkipTest("z3 is unavailable")
        cases = {
            EVIDENCE / "insert_tail_correspondence.smt2": "unsat",
            EVIDENCE / "classification_replay/exact_output.smt2": "unsat",
            EVIDENCE / "classification_replay/full_state.smt2": "unsat",
            EVIDENCE / "classification_replay/nonvacuity.smt2": "sat",
        }
        cases.update(
            {
                EVIDENCE / "witnesses" / kind / "witness.smt2": "sat"
                for kind in model.WITNESS_KINDS
            }
        )
        cases.update(
            {
                EVIDENCE
                / "mutations"
                / kind
                / "correspondence.smt2": "sat"
                for kind in model.MUTATION_KINDS
            }
        )
        for path, expected in cases.items():
            with self.subTest(path=path):
                process = subprocess.run(
                    [z3, "-smt2", str(path)],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=30,
                )
                self.assertEqual(process.returncode, 0)
                self.assertEqual(
                    process.stdout.splitlines()[0], expected
                )
                self.assertEqual(process.stderr, "")

    def test_classification_replays_are_byte_identical(self) -> None:
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

    def test_protected_artifacts_remain_byte_identical(self) -> None:
        preservation = self.result["preservation"]
        for family in ("protected_trees", "protected_files"):
            for record in preservation[family].values():
                self.assertEqual(
                    record["before_sha256"], record["after_sha256"]
                )
        for key in (
            "accepted_target_078_unchanged",
            "accepted_target_079_unchanged",
            "adapter_refinement_v2_unchanged",
            "operational_v2_unchanged",
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
            self.result["preservation_policy"],
            {
                "required_version": "slice-preservation-path-policy-v2",
                "path_policy_v1_unchanged": True,
                "additive_registration": (
                    "target_078_insert_tail_refinement_v3"
                ),
                "additive_review_registration": (
                    "target_078_insert_tail_refinement_v3_review"
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
