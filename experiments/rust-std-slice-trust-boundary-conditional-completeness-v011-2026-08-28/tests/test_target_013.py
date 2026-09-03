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
import replay_target_013
import target_013
import target_029
import target_pipeline


class Target013GuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text, self.metadata = target_013.obligation(target_013.PRIMARY)

    def assert_target_rejected(
        self,
        text: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        with self.assertRaises(GuardError):
            target_013.validate_target_obligation(
                text if text is not None else self.text,
                metadata if metadata is not None else self.metadata,
            )

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for purpose in target_013.PURPOSES:
            with self.subTest(purpose=purpose):
                text, metadata = target_013.obligation(purpose)
                validate_obligation(text, metadata)
                target_013.validate_target_obligation(text, metadata)

    def test_retained_two_conjunct_contract_is_rejected(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["active_contract_sha256"] = target_013.RETAINED_CONTRACT_SHA256
        metadata["active_contract_text"] = target_013.RETAINED_CONTRACT_TEXT
        self.assert_target_rejected(metadata=metadata)

    def test_omission_of_each_strengthened_conjunct_is_rejected(self) -> None:
        def omit_target_call(text: str, symbol: str) -> str:
            target_start = text.index("(define-fun TargetDefinition_T")
            start = text.index(f"({symbol}", target_start)
            balance = 0
            for end in range(start, len(text)):
                if text[end] == "(":
                    balance += 1
                elif text[end] == ")":
                    balance -= 1
                    if balance == 0:
                        return text[:start] + "true" + text[end + 1 :]
            self.fail(f"unterminated target call for {symbol}")

        retained = {
            "ActivePartitionConjunct",
            "ActiveFinalFrameConjunct",
        }
        for symbol in target_013.ACTIVE_CONJUNCT_SYMBOLS:
            if symbol in retained:
                continue
            with self.subTest(symbol=symbol):
                mutated = omit_target_call(self.text, symbol)
                validate_obligation(mutated, self.metadata)
                self.assert_target_rejected(text=mutated)

    def test_output_laundering_is_rejected(self) -> None:
        text = self.text.replace(
            "      (b_input_borrow Int)))))",
            "      (b_input_borrow Int)\n"
            "      (b_selected_chunks_ref Int)))))",
        ).replace(
            "       (InputIdentityObserved x b)))",
            "       (InputIdentityObserved x b)\n"
            "       (>= (b_selected_chunks_ref b) 0)))",
        ).replace(
            "       (= (y_chunks_len y) (AsChunksUncheckedMutLength x))",
            "       (= (y_chunks_len y) (AsChunksUncheckedMutLength x))\n"
            "       (= (y_chunks_len y)\n"
            "          (+ (b_selected_chunks_ref b)\n"
            "             (- (x_length x) (x_length x))))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_selected_chunks_ref",
                "role": "source_helper_observation",
                "source_citations": ["core/src/slice/mod.rs:1557-1561"],
                "trust_site_ids": ["TS-013-E002", "TS-013-E003"],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_final_state_laundering_is_rejected(self) -> None:
        text = self.text.replace(
            "      (b_input_borrow Int)))))",
            "      (b_input_borrow Int)\n"
            "      (b_selected_final_value Int)))))",
        ).replace(
            "       (InputIdentityObserved x b)))",
            "       (InputIdentityObserved x b)\n"
            "       (>= (b_selected_final_value b) 0)))",
        ).replace(
            "       (ActiveFinalChunksLengthConjunct",
            "       (= (s_final_sequence s)\n"
            "          (+ (b_selected_final_value b)\n"
            "             (- (x_length x) (x_length x))))\n"
            "       (ActiveFinalChunksLengthConjunct",
            1,
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_selected_final_value",
                "role": "source_helper_observation",
                "source_citations": ["core/src/slice/mod.rs:1557-1561"],
                "trust_site_ids": ["TS-013-E002", "TS-013-E003"],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_opaque_whole_target_relation_is_rejected(self) -> None:
        text = self.text.replace(
            "(declare-const x Input)",
            "(declare-fun WholeTarget (Input Boundary Output State) Bool)\n"
            "(declare-const x Input)",
        )
        start = text.index("(define-fun TargetDefinition_T")
        end = text.index("(define-fun Spec_T", start)
        replacement = """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (WholeTarget x b y s))
"""
        text = text[:start] + replacement + text[end:]
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "WholeTarget",
                "role": "source_transition",
                "source_citations": ["core/src/slice/mod.rs:1552-1562"],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_selected_trace_boundary_is_rejected(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"][0]["role"] = "implementation_trace"
        with self.assertRaises(GuardError):
            validate_obligation(self.text, metadata)

    def test_weakened_final_state_equality_is_rejected(self) -> None:
        equality = (
            "(= (s_final_sequence s1) (s_final_sequence s2))"
        )
        self.assertIn(equality, self.text)
        with self.assertRaises(GuardError):
            validate_obligation(self.text.replace(equality, "true"), self.metadata)

    def test_expected_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        expected = {
            target_013.PRIMARY: "sat\n",
            target_013.EXACT_OUTPUT: "unsat\n",
        }
        for purpose, solver_result in expected.items():
            with self.subTest(purpose=purpose):
                text, _ = target_013.obligation(purpose)
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


class Target013ReplayTests(unittest.TestCase):
    def test_independent_replay_checks_every_active_conjunct(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "witness.json"
            path.write_text(
                json.dumps(target_013.witness_payload(), sort_keys=True) + "\n"
            )
            result = replay_target_013.replay(path)
        self.assertEqual(result["status"], "passed")
        for checks in result["active_conjuncts"].values():
            self.assertEqual(set(checks), {
                "partition",
                "initial_chunks_length",
                "initial_remainder_length",
                "initial_chunk_subranges",
                "initial_remainder_subrange",
                "final_chunks_length",
                "final_remainder_length",
                "final_frame",
                "final_chunk_subranges",
                "final_remainder_subrange",
            })
            self.assertTrue(all(checks.values()))
        self.assertTrue(result["observed"]["exact_output_equal"])
        self.assertFalse(result["observed"]["full_exact_equivalent"])


class TargetPipelineScopeTests(unittest.TestCase):
    def test_target_013_update_preserves_029_and_all_other_rows(self) -> None:
        rows = [
            {
                "target": f"target-{index}",
                "input_order": str(index),
                "exact_output_determinism_status": "not-run",
                "completeness_modulo_reviewed_equivalence_status": "not-run",
            }
            for index in range(62)
        ]
        rows[13]["target"] = target_013.TARGET
        rows[13]["input_order"] = target_013.INPUT_ORDER
        rows[29]["target"] = target_029.TARGET
        rows[29]["input_order"] = target_029.INPUT_ORDER
        rows[29].update(
            {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
        )
        before = copy.deepcopy(rows)
        updated_csv, updated_json = target_pipeline.apply_crosswalk_result_update(
            rows,
            copy.deepcopy(rows),
            target=target_013.TARGET,
            input_order=target_013.INPUT_ORDER,
            statuses={
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            },
            preserved_results={
                (target_029.TARGET, target_029.INPUT_ORDER): {
                    "exact_output_determinism_status": "conditional-incomplete",
                    "completeness_modulo_reviewed_equivalence_status": (
                        "conditional-incomplete"
                    ),
                }
            },
        )
        self.assertEqual(updated_csv, updated_json)
        for index, (old, new) in enumerate(zip(before, updated_csv)):
            if index == 13:
                self.assertEqual(
                    new["exact_output_determinism_status"],
                    "conditional-complete",
                )
            else:
                self.assertEqual(new, old)

    def test_target_013_update_rejects_mutated_029_or_other_row(self) -> None:
        base = [
            {
                "target": f"target-{index}",
                "input_order": str(index),
                "exact_output_determinism_status": "not-run",
                "completeness_modulo_reviewed_equivalence_status": "not-run",
            }
            for index in range(62)
        ]
        base[13].update(
            {"target": target_013.TARGET, "input_order": target_013.INPUT_ORDER}
        )
        base[29].update(
            {
                "target": target_029.TARGET,
                "input_order": target_029.INPUT_ORDER,
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
        )
        preserved = {
            (target_029.TARGET, target_029.INPUT_ORDER): {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
        }
        statuses = {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-incomplete"
            ),
        }
        for index in (29, 7):
            with self.subTest(index=index):
                rows = copy.deepcopy(base)
                rows[index]["exact_output_determinism_status"] = "solver-unknown"
                with self.assertRaises(ValueError):
                    target_pipeline.apply_crosswalk_result_update(
                        rows,
                        copy.deepcopy(rows),
                        target=target_013.TARGET,
                        input_order=target_013.INPUT_ORDER,
                        statuses=statuses,
                        preserved_results=preserved,
                    )


if __name__ == "__main__":
    unittest.main()
