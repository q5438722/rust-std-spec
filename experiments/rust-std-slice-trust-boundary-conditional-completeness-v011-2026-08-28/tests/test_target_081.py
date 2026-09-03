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
import campaign_common as common
import replay_target_081
import run_target_081
import target_081
import target_pipeline


class Target081GuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text, self.metadata = target_081.obligation(target_081.PRIMARY)

    def assert_target_rejected(
        self,
        text: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        with self.assertRaises(GuardError):
            target_081.validate_target_obligation(
                text if text is not None else self.text,
                metadata if metadata is not None else self.metadata,
            )

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for purpose in target_081.PURPOSES:
            with self.subTest(purpose=purpose):
                text, metadata = target_081.obligation(purpose)
                validate_obligation(text, metadata)
                target_081.validate_target_obligation(text, metadata)

    def test_active_contract_identity_is_exact(self) -> None:
        self.assertEqual(
            target_081.ACTIVE_CONTRACT_SHA256,
            "420e250d3b0ae471b64eb3d6474588eaec8acfc7644b5c1dd4420e4c1b2c0597",
        )
        self.assertIn("slice_permutation", target_081.ACTIVE_CONTRACT_TEXT)
        self.assertIn("slice_sorted_by_cmp", target_081.ACTIVE_CONTRACT_TEXT)

    def test_omission_of_each_active_contract_conjunct_is_rejected(self) -> None:
        target_start = self.text.index("(define-fun TargetDefinition_T")
        for symbol in target_081.ACTIVE_CONJUNCT_SYMBOLS:
            with self.subTest(symbol=symbol):
                start = self.text.index(f"({symbol}", target_start)
                balance = 0
                end = start
                for end in range(start, len(self.text)):
                    if self.text[end] == "(":
                        balance += 1
                    elif self.text[end] == ")":
                        balance -= 1
                        if balance == 0:
                            break
                mutated = self.text[:start] + "true" + self.text[end + 1 :]
                self.assert_target_rejected(text=mutated)

    def test_opaque_whole_sort_relation_is_rejected(self) -> None:
        text = self.text.replace(
            "(declare-const x Input)",
            "(declare-fun WholeSort (Input Boundary Output State) Bool)\n"
            "(declare-const x Input)",
        )
        start = text.index("(define-fun TargetDefinition_T")
        end = text.index("(define-fun Spec_T", start)
        text = (
            text[:start]
            + """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (WholeSort x b y s))
"""
            + text[end:]
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "WholeSort",
                "role": "source_transition",
                "source_citations": [
                    "core/src/slice/sort/unstable/mod.rs:22-58"
                ],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_final_permutation_boundary_laundering_is_rejected(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"][3]["role"] = "final_permutation"
        with self.assertRaises(GuardError):
            validate_obligation(self.text, metadata)

    def test_complete_trace_boundary_is_rejected(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"][-1]["role"] = "full_execution_trace"
        with self.assertRaises(GuardError):
            validate_obligation(self.text, metadata)

    def test_multiset_free_equivalence_is_rejected(self) -> None:
        text = self.text.replace(
            "       (SameElementMultiset s1 s2)\n",
            "",
        )
        validate_obligation(text, self.metadata)
        self.assert_target_rejected(text=text)

    def test_total_order_precondition_cannot_be_injected_into_primary(self) -> None:
        original = "       (= (b_callback_state_delta b) 0))"
        replacement = (
            "       (= (b_callback_state_delta b) 0)\n"
            "       (TotalOrderProfile x b))"
        )
        self.assertIn(original, self.text)
        text = self.text.replace(original, replacement, 1)
        validate_obligation(text, self.metadata)
        self.assert_target_rejected(text=text)

    def test_boundary_manifest_excludes_answer_bearing_retained_sites(self) -> None:
        manifest = target_081.boundary_manifest()
        excluded = {
            item["trust_site_id"] for item in manifest["excluded_retained_sites"]
        }
        self.assertEqual(
            excluded, set(target_081.EXCLUDED_RETAINED_TRUST_SITES)
        )
        admitted = {
            trust_site
            for item in manifest["shared_boundary_observations"]
            for trust_site in item["trust_site_ids"]
        }
        self.assertEqual(admitted, {"TS-081-D004"})
        serialized = json.dumps(manifest["shared_boundary_observations"])
        for forbidden in ("final sequence", "permutation", "trace"):
            self.assertNotIn(forbidden, serialized)

    def test_expected_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        expected = {
            target_081.PRIMARY: "sat\n",
            target_081.TOTAL_ORDER_SANITY: "unsat\n",
            target_081.EXACT_FINAL_SLICE: "sat\n",
        }
        for purpose, solver_result in expected.items():
            with self.subTest(purpose=purpose):
                text, _ = target_081.obligation(purpose)
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

    def test_other_crosswalk_rows_cannot_be_mutated(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = copy.deepcopy(csv_rows)
        other = next(
            row
            for row in csv_rows
            if row["target"]
            not in {
                target_081.TARGET,
                *(target for target, _ in run_target_081.PRESERVED_RESULTS),
            }
        )
        other["exact_output_determinism_status"] = "conditional-complete"
        with self.assertRaises(ValueError):
            target_pipeline.apply_crosswalk_result_update(
                csv_rows,
                json_rows,
                target=target_081.TARGET,
                input_order=target_081.INPUT_ORDER,
                statuses=run_target_081.RESULT_STATUSES,
                preserved_results=run_target_081.PRESERVED_RESULTS,
            )


class Target081ReplayTests(unittest.TestCase):
    def test_independent_replay_accepts_both_counterexamples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "witness.json"
            path.write_text(
                json.dumps(target_081.witness_payload(), sort_keys=True) + "\n"
            )
            result = replay_target_081.replay(path)
        exact = result["exact_final_slice_counterexample"]
        general = result["general_non_total_counterexample"]
        self.assertTrue(exact["reviewed_equal_key_equivalent"])
        self.assertFalse(exact["exact_final_slice_equal"])
        self.assertFalse(general["boundary_is_total_order"])
        self.assertFalse(general["reviewed_equal_key_equivalent"])
        self.assertTrue(
            result["total_order_sanity"]["all_pairs_equal_key_equivalent"]
        )

    def test_foreign_identity_is_not_a_contract_witness(self) -> None:
        payload = target_081.witness_payload()
        payload["exact_final_slice_counterexample"]["execution2"][
            "final_slice"
        ][0] = 12
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "witness.json"
            path.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                replay_target_081.replay(path)


if __name__ == "__main__":
    unittest.main()
