#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from checker_guards import GuardError, validate_obligation
import replay_target_029
import target_029


class Target029GuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text, self.metadata = target_029.obligation(target_029.PRIMARY)

    def assert_target_rejected(
        self,
        text: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        with self.assertRaises(GuardError):
            target_029.validate_target_obligation(
                text if text is not None else self.text,
                metadata if metadata is not None else self.metadata,
            )

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for purpose in target_029.PURPOSES:
            with self.subTest(purpose=purpose):
                text, metadata = target_029.obligation(purpose)
                validate_obligation(text, metadata)
                target_029.validate_target_obligation(text, metadata)

    def test_sortedness_strengthening_is_rejected(self) -> None:
        text = self.text.replace(
            "       (ComparatorObservation (b_cmp0 b))\n"
            "       (ComparatorObservation (b_cmp1 b))",
            "       (OrderedProfile x b)",
        )
        validate_obligation(text, self.metadata)
        self.assert_target_rejected(text=text)

    def test_blanket_unsorted_result_equivalence_is_rejected(self) -> None:
        original = """\
  (and (= (s_callback_state s1) (s_callback_state s2))
       (= (y_is_ok y1) (y_is_ok y2))
       (ite (y_is_ok y1)
            (and (EqualAt x b (y_index y1))
                 (EqualAt x b (y_index y2)))
            (= (y_index y1) (y_index y2)))))"""
        replacement = f"""\
  (or (not (OrderedProfile x b))
      {original.strip()})"""
        text = self.text.replace(original, replacement)
        validate_obligation(text, self.metadata)
        self.assert_target_rejected(text=text)

    def test_answer_bearing_callback_boundary_is_rejected(self) -> None:
        text = self.text.replace(
            "      (b_state_delta1 Int)))))",
            "      (b_state_delta1 Int)\n"
            "      (b_callback_answer Int)))))",
        ).replace(
            "       (= (b_state_delta1 b) 0)))",
            "       (= (b_state_delta1 b) 0)\n"
            "       (= (b_callback_answer b) 0)))",
        ).replace(
            "       (GeneratedBinarySearchByResult x b y)\n",
            "       (GeneratedBinarySearchByResult x b y)\n"
            "       (= (y_index y)\n"
            "          (+ (x_length x) (b_callback_answer b)))\n",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_callback_answer",
                "role": "callback_result",
                "source_citations": ["core/src/slice/mod.rs:2995,3014"],
                "trust_site_ids": ["TS-029-D003", "TS-029-E002"],
            }
        )
        validate_obligation(text, metadata)
        self.assert_target_rejected(text=text, metadata=metadata)

    def test_opaque_whole_target_relation_is_rejected(self) -> None:
        text = self.text.replace(
            "(declare-const x Input)",
            "(declare-fun WholeTarget (Input Boundary Output State) Bool)\n"
            "(declare-const x Input)",
        ).replace(
            "(and (ElementReadsMatch x b)\n"
            "       (GeneratedBinarySearchByResult x b y)\n"
            "       (= (s_callback_state s) (CallbackStateAfterTwo x b)))",
            "(WholeTarget x b y s)",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "WholeTarget",
                "role": "source_transition",
                "source_citations": ["core/src/slice/mod.rs:2970-3022"],
            }
        ]
        self.assert_target_rejected(text=text, metadata=metadata)

    def test_selected_execution_trace_boundary_is_rejected(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        delta0 = next(
            field
            for field in metadata["boundary_fields"]
            if field["selector"] == "b_state_delta0"
        )
        delta0["role"] = "implementation_trace"
        self.assert_target_rejected(metadata=metadata)

    def test_deterministic_implementation_choice_injection_is_rejected(
        self,
    ) -> None:
        text = self.text.replace(
            "(define-fun TargetDefinition_T",
            "(define-fun DeterministicChoice ((x Input) (b Boundary)) Int\n"
            "  (+ (- (x_length x) 2)\n"
            "     (ite (= (b_cmp1 b) Greater) 0 1)))\n"
            "(define-fun TargetDefinition_T",
        ).replace(
            "       (GeneratedBinarySearchByResult x b y)\n"
            "       (= (s_callback_state s) (CallbackStateAfterTwo x b)))",
            "       (GeneratedBinarySearchByResult x b y)\n"
            "       (= (y_index y) (DeterministicChoice x b))\n"
            "       (= (s_callback_state s) (CallbackStateAfterTwo x b)))",
        )
        validate_obligation(text, self.metadata)
        self.assert_target_rejected(text=text)

    def test_expected_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        expected = {
            target_029.PRIMARY: "sat\n",
            target_029.SORTED_SANITY: "unsat\n",
            target_029.EXACT_OUTPUT: "sat\n",
        }
        for purpose, solver_result in expected.items():
            with self.subTest(purpose=purpose):
                text, _ = target_029.obligation(purpose)
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=text,
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, solver_result)
                self.assertEqual(process.stderr, "")

    def test_boundary_manifest_separates_retained_and_obligation_sites(
        self,
    ) -> None:
        manifest = target_029.boundary_manifest()
        retained = manifest["retained_implementation_proof_boundary"]
        obligation = manifest["conditional_obligation_boundary"]
        self.assertEqual(
            set(manifest["all_audited_trust_site_ids"]),
            {
                "TS-029-D001",
                "TS-029-D002",
                "TS-029-D003",
                "TS-029-D004",
                "TS-029-D005",
                "TS-029-C001",
                "TS-029-E001",
                "TS-029-E002",
            },
        )
        self.assertEqual(
            set(obligation["used_boundary_trust_site_ids"]),
            {
                "TS-029-D002",
                "TS-029-D003",
                "TS-029-E001",
                "TS-029-E002",
            },
        )
        self.assertNotEqual(
            set(retained["executable_lower_boundary_trust_site_ids"]),
            set(obligation["used_boundary_trust_site_ids"]),
        )
        flattened = json.dumps(
            manifest["shared_boundary_observations"], sort_keys=True
        )
        for forbidden in ("selected index", "returned Result", "execution trace"):
            self.assertNotIn(forbidden, flattened)


class Target029ReplayTests(unittest.TestCase):
    def test_independent_replay_accepts_both_witnesses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "witness.json"
            path.write_text(
                json.dumps(target_029.witness_payload(), sort_keys=True) + "\n"
            )
            result = replay_target_029.replay(path)
        self.assertEqual(result["status"], "passed")
        self.assertFalse(
            result["general_counterexample"]["equivalent"]
        )
        self.assertTrue(
            result["sorted_domain_sanity"]["all_pairs_equivalent"]
        )
        self.assertTrue(
            result["exact_output_counterexample"][
                "matching_index_equivalent"
            ]
        )
        self.assertFalse(
            result["exact_output_counterexample"]["exactly_equal"]
        )


if __name__ == "__main__":
    unittest.main()
