#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import replay_target_078_operational_v1 as replay
import target_078_operational_smt_v1 as smt
import target_078_operational_v1 as model


EVIDENCE = ROOT / "evidence/target_078_operational_v1"


class Target078OperationalArtifactsV1Tests(unittest.TestCase):
    def test_both_arbitrary_domain_obligations_are_direct_unsat(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for purpose in smt.PURPOSES:
            with self.subTest(purpose=purpose):
                text = smt.obligation_text(purpose)
                metadata = smt.obligation_metadata(purpose)
                smt.validate_obligation(text, metadata)
                self.assertFalse(metadata["domain"]["bounded"])
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=text,
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, "unsat\n")
                self.assertEqual(process.stderr, "")

    def test_nonvacuity_probes_and_regressions_have_expected_results(
        self,
    ) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        cases = [
            ("nonvacuity", smt.nonvacuity_text(), "sat\n"),
            (
                "immutable-replay",
                smt.immutable_replay_text(),
                "unsat\n",
            ),
            ("swap-regression", smt.swap_regression_text(), "unsat\n"),
            (
                "length-17-correspondence",
                smt.length_17_correspondence_text(),
                "unsat\n",
            ),
        ]
        cases.extend(
            (kind, smt.probe_text(kind), "sat\n")
            for kind in smt.PROBE_KINDS
        )
        for name, text, expected in cases:
            with self.subTest(name=name):
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=text,
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, expected)
                self.assertEqual(process.stderr, "")

    def test_source_transition_deletion_fails_closed(self) -> None:
        text = smt.obligation_text(smt.EXACT)
        metadata = smt.obligation_metadata(smt.EXACT)
        for symbol in smt.SOURCE_TRANSITIONS:
            with self.subTest(symbol=symbol):
                changed = text.replace(
                    symbol, f"Deleted{symbol}", 1
                )
                with self.assertRaises(ValueError):
                    smt.validate_obligation(changed, metadata)

    def test_source_semantic_mutations_change_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for kind in smt.MUTATION_PROBES:
            with self.subTest(kind=kind):
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=smt.mutation_probe_text(kind),
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, "unsat\n")
                self.assertEqual(process.stderr, "")

    def test_callback_boundary_contains_no_answer_or_trace(self) -> None:
        text = smt.obligation_text()
        start = text.index("(declare-datatypes ((Boundary 0))")
        end = text.index("(declare-datatypes ((Reference 0))")
        block = text[start:end].lower()
        for forbidden in (
            "pivot",
            "permutation",
            "returned",
            "final_sequence",
            "final_callback",
            "trace",
        ):
            self.assertNotIn(forbidden, block)
        self.assertIn("b_ordering", block)
        self.assertIn("b_contract_ordering", block)
        self.assertIn("b_next_state", block)
        self.assertIn("b_panics", block)
        self.assertIn("(m_terminal run)", text)
        self.assertIn("(define-fun ExactRunState", text)
        self.assertNotIn("(define-fun-rec RunSource", text)
        self.assertNotIn("(define-fun ExecutionFuel", text)

    def test_concrete_witness_replays_independently(self) -> None:
        result = replay.replay(EVIDENCE / "witness.json")
        self.assertEqual(result["status"], "passed")
        self.assertTrue(
            result["normal_determinism"]["observed"][
                "exact_principal_return_and_final_state"
            ]
        )
        self.assertEqual(
            result["frozen_prior_falsifier"]["final_sequence"],
            [1, 2, 3],
        )
        self.assertTrue(
            result["frozen_prior_falsifier"][
                "relation_is_total_and_trace_independent"
            ]
        )
        self.assertEqual(result["fallback"]["choose_pivot_count"], 16)
        self.assertEqual(len(result["partition_configurations"]), 5)
        self.assertTrue(
            all(
                not equivalent
                for equivalent in result["negative_witnesses"].values()
            )
        )

    def test_result_packages_complete_additive_classification(self) -> None:
        result = json.loads((EVIDENCE / "result.json").read_text())
        self.assertEqual(result["target"], model.TARGET)
        self.assertEqual(result["model_id"], model.MODEL_ID)
        self.assertTrue(result["source_model_complete"])
        self.assertTrue(result["classification_eligible"])
        self.assertEqual(result["unresolved_source_model_phases"], [])
        self.assertEqual(
            set(result["classification"].values()),
            {"conditional-complete"},
        )
        self.assertEqual(
            set(result["obligations"]), set(smt.PURPOSES)
        )
        for evidence in result["obligations"].values():
            self.assertEqual(
                evidence["solver"]["solver_result"], "unsat"
            )
        self.assertEqual(
            len(result["semantic_force_probes"]), len(smt.PROBE_KINDS)
        )
        for evidence in result["semantic_force_probes"].values():
            self.assertEqual(evidence["solver"]["solver_result"], "sat")
        self.assertEqual(
            len(result["semantic_mutation_regressions"]),
            len(smt.MUTATION_PROBES),
        )
        for evidence in result["semantic_mutation_regressions"].values():
            self.assertEqual(evidence["solver"]["solver_result"], "unsat")
        self.assertEqual(
            result["verus"]["expected_summary"],
            "verification results:: 5 verified, 0 errors",
        )

    def test_verus_proof_is_parameterized_and_trusted_free(self) -> None:
        path = (
            ROOT
            / "proofs/078_core_slice_select_nth_unstable_by_operational_v1.rs"
        )
        text = path.read_text()
        for required in (
            "sequence: Seq<int>",
            "contract_ordering: Map<int, Map<int, int>>",
            "ordering: Map<int, Map<int, Map<int, int>>>",
            "pub ghost struct ExactOperationalResult",
            "pub ghost struct RefinedOperationalResult",
            "pub open spec fn admissible_boundary",
            "pub open spec fn exact_source_result_is_terminal",
            "pub open spec fn checked_exact_result_projection",
            "pub proof fn checked_refinement_preserves_every_exact_field",
            "pub proof fn implementation_ordering_projects_exactly_to_contract",
            "pub proof fn callback_transitions_are_total_functions",
        ):
            self.assertIn(required, text)
        for forbidden in ("external_body", "assume(", "admit(", "axiom"):
            self.assertNotIn(forbidden, text)
        self.assertNotIn("run_source", text)
        self.assertNotIn("fuel", text)

    def test_verus_rejects_a_dropped_exact_projection_field(self) -> None:
        verus = ROOT / "../../verus/source/target-verus/release/verus"
        self.assertTrue(verus.is_file())
        source = (
            ROOT
            / "proofs/078_core_slice_select_nth_unstable_by_operational_v1.rs"
        ).read_text()
        anchor = "sequence: source.state.sequence,"
        self.assertEqual(source.count(anchor), 1)
        mutated = source.replace(
            anchor, "sequence: Seq::empty(),", 1
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mutated.rs"
            path.write_text(mutated)
            process = subprocess.run(
                [str(verus), str(path), "--crate-type=lib"],
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("verification results", process.stdout)
        self.assertNotIn("0 errors", process.stdout)

    def test_crosswalk_and_protected_state_remain_additive_only(self) -> None:
        addendum = json.loads(
            (
                ROOT
                / "crosswalk/target_078_operational_v1_addendum.json"
            ).read_text()
        )
        self.assertEqual(addendum["target"], model.TARGET)
        self.assertFalse(addendum["baseline_row_mutated"])
        self.assertFalse(addendum["target_079_mutated"])
        self.assertFalse(addendum["manager_stage_mutated"])

        ledger = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        by_order = {row["input_order"]: row for row in ledger}
        for order in ("78", "79"):
            with self.subTest(order=order):
                self.assertEqual(
                    by_order[order]["exact_output_determinism_status"],
                    "missing-source-backed-model",
                )
                self.assertEqual(
                    by_order[order][
                        "completeness_modulo_reviewed_equivalence_status"
                    ],
                    "missing-source-backed-model",
                )

        result = json.loads((EVIDENCE / "result.json").read_text())
        preservation = result["preservation"]
        for record in preservation["protected_trees"].values():
            self.assertEqual(
                record["before_sha256"], record["after_sha256"]
            )
        for record in preservation["protected_files"].values():
            self.assertEqual(
                record["before_sha256"], record["after_sha256"]
            )
        self.assertTrue(preservation["target_079_row_unchanged"])
        self.assertTrue(preservation["pipeline_state_unchanged"])


if __name__ == "__main__":
    unittest.main()
