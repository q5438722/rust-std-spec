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
import replay_target_106
import target_013
import target_029
import target_106
import target_pipeline


class Target106GuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text, self.metadata = target_106.obligation(target_106.PRIMARY)

    def assert_target_rejected(
        self,
        text: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        with self.assertRaises(GuardError):
            target_106.validate_target_obligation(
                text if text is not None else self.text,
                metadata if metadata is not None else self.metadata,
            )

    @staticmethod
    def add_boundary_field(
        text: str,
        declaration: str,
        boundary_clause: str,
        target_clause: str,
    ) -> str:
        text = text.replace(
            "      (b_predicate_identity Int)))))",
            "      (b_predicate_identity Int)\n"
            f"      {declaration})))))",
        )
        text = text.replace(
            "       (InputIdentityObserved x b)))",
            "       (InputIdentityObserved x b)\n"
            f"       {boundary_clause}))",
            1,
        )
        text = text.replace(
            "  (and (InputIdentityObserved x b)",
            "  (and (InputIdentityObserved x b)\n"
            f"       {target_clause}",
            1,
        )
        return text

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for purpose in target_106.PURPOSES:
            with self.subTest(purpose=purpose):
                text, metadata = target_106.obligation(purpose)
                validate_obligation(text, metadata)
                target_106.validate_target_obligation(text, metadata)

    def test_active_contract_identity_is_exact(self) -> None:
        self.assertEqual(
            target_106.ACTIVE_CONTRACT_SHA256,
            "8fb38da00d00aea693a93e948863b8ab7bf6d6d2e6e4662345ad50d9a923d3db",
        )
        self.assertIn("slice_predicate_split_view", target_106.ACTIVE_CONTRACT_TEXT)
        self.assertIn("pred, false, false, n as int", target_106.ACTIVE_CONTRACT_TEXT)

    def test_omission_of_each_active_contract_conjunct_is_rejected(self) -> None:
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

        for symbol in target_106.ACTIVE_CONJUNCT_SYMBOLS:
            with self.subTest(symbol=symbol):
                mutated = omit_target_call(self.text, symbol)
                validate_obligation(mutated, self.metadata)
                self.assert_target_rejected(text=mutated)

    def test_opaque_whole_target_relation_is_rejected(self) -> None:
        text = self.text.replace(
            "(declare-const x Input)",
            "(declare-fun WholeTarget (Input Boundary Output State) Bool)\n"
            "(declare-const x Input)",
        )
        start = text.index("(define-fun TargetDefinition_T")
        end = text.index("(define-fun Spec_T", start)
        text = (
            text[:start]
            + """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (WholeTarget x b y s))
"""
            + text[end:]
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "WholeTarget",
                "role": "source_transition",
                "source_citations": ["core/src/slice/mod.rs:2442-2447"],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_opaque_iterator_view_relation_is_rejected(self) -> None:
        text = self.text.replace(
            "(declare-const x Input)",
            "(declare-fun IteratorViewOracle (Input Boundary Output) Bool)\n"
            "(declare-const x Input)",
        ).replace(
            "  (and (InputIdentityObserved x b)",
            "  (and (IteratorViewOracle x b y)\n"
            "       (InputIdentityObserved x b)",
            1,
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "IteratorViewOracle",
                "role": "source_transition",
                "source_citations": ["core/src/slice/iter.rs:678-690,1241-1252"],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_returned_iterator_laundering_is_rejected(self) -> None:
        text = self.add_boundary_field(
            self.text,
            "(b_returned_count Int)",
            "(>= (b_returned_count b) 0)",
            "(= (y_count y) (b_returned_count b))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_returned_count",
                "role": "selected_output",
                "source_citations": ["core/src/slice/iter.rs:1241-1252"],
                "trust_site_ids": ["TS-106-D004"],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_selected_range_or_trace_boundary_is_rejected(self) -> None:
        text = self.add_boundary_field(
            self.text,
            "(b_selected_remaining_start Int)",
            "(>= (b_selected_remaining_start b) 0)",
            "(= (y_remaining_start y) (b_selected_remaining_start b))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_selected_remaining_start",
                "role": "implementation_trace",
                "source_citations": ["core/src/slice/iter.rs:678-690"],
                "trust_site_ids": ["TS-106-D001"],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_constructor_time_predicate_observation_is_rejected(self) -> None:
        text = self.add_boundary_field(
            self.text,
            "(b_predicate_result Bool)",
            "(or (b_predicate_result b) (not (b_predicate_result b)))",
            "(= (b_predicate_result b) (b_predicate_result b))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_predicate_result",
                "role": "callback_result",
                "source_citations": ["core/src/slice/iter.rs:678-690"],
                "trust_site_ids": ["TS-106-D003"],
            }
        )
        self.assert_target_rejected(text=text, metadata=metadata)

    def test_boundary_has_no_callback_result_or_returned_view(self) -> None:
        boundary = target_106.boundary_manifest()
        self.assertEqual(boundary["constructor_callback_invocations"], 0)
        self.assertEqual(
            [entry["field"] for entry in boundary["shared_boundary_observations"]],
            [
                "b_input_allocation",
                "b_input_borrow",
                "b_predicate_identity",
            ],
        )
        self.assertNotIn("PredicateObserved", self.text)
        self.assertNotIn("b_callback", self.text)

    def test_weakened_exact_equivalence_is_rejected(self) -> None:
        for equality in (
            "(= (y_borrow y1) (y_borrow y2))",
            "(= (y_predicate_state y1) (y_predicate_state y2))",
            "(= (y_finished y1) (y_finished y2))",
            "(= (s_final_slice_sequence s1) (s_final_slice_sequence s2))",
            "(= (s_callback_state s1) (s_callback_state s2))",
        ):
            with self.subTest(equality=equality):
                self.assertIn(equality, self.text)
                self.assert_target_rejected(text=self.text.replace(equality, "true"))

    def test_wrong_n_finished_reverse_and_nonempty_initial_state_are_rejected(
        self,
    ) -> None:
        mutations = {
            "wrong n": self.text.replace(
                "(define-fun SplitNMutNewCount ((x Input)) Int\n  (x_n x))",
                "(define-fun SplitNMutNewCount ((x Input)) Int\n  (+ (x_n x) 1))",
            ),
            "finished true": self.text.replace(
                "(define-fun SplitMutNewFinished ((x Input)) Bool\n  false)",
                "(define-fun SplitMutNewFinished ((x Input)) Bool\n  true)",
            ),
            "reverse true": self.text.replace(
                "(define-fun SplitNMutNewReverse ((x Input)) Bool\n  false)",
                "(define-fun SplitNMutNewReverse ((x Input)) Bool\n  true)",
            ),
            "yielded nonempty": self.text.replace(
                "(= (y_yielded_length y) 0)",
                "(= (y_yielded_length y) 1)",
                1,
            ),
            "remainder nonempty": self.text.replace(
                "(= (y_remainder_length y) 0)",
                "(= (y_remainder_length y) 1)",
                1,
            ),
        }
        for name, mutated in mutations.items():
            with self.subTest(name=name):
                self.assertNotEqual(mutated, self.text)
                self.assert_target_rejected(text=mutated)

    def test_mismatched_borrow_allocation_or_predicate_identity_is_rejected(
        self,
    ) -> None:
        mutations = {
            "allocation": self.text.replace(
                "(= (b_input_allocation b) (x_allocation x))",
                "(= (b_input_allocation b) (x_borrow x))",
            ),
            "borrow": self.text.replace(
                "(= (b_input_borrow b) (x_borrow x))",
                "(= (b_input_borrow b) (x_allocation x))",
            ),
            "predicate": self.text.replace(
                "(= (b_predicate_identity b) (x_predicate_identity x))",
                "(= (b_predicate_identity b) (x_predicate_state x))",
            ),
        }
        for name, mutated in mutations.items():
            with self.subTest(name=name):
                self.assertNotEqual(mutated, self.text)
                self.assert_target_rejected(text=mutated)

    def test_expected_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for purpose in target_106.PURPOSES:
            with self.subTest(purpose=purpose):
                text, _ = target_106.obligation(purpose)
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


class Target106ReplayTests(unittest.TestCase):
    def test_independent_replay_checks_both_obligations(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for purpose, stem in replay_target_106.OBLIGATIONS.items():
                text, metadata = target_106.obligation(purpose)
                (root / f"{stem}.smt2").write_text(text)
                (root / f"{stem}.metadata.json").write_text(
                    json.dumps(metadata, indent=2, sort_keys=True) + "\n"
                )
            result = replay_target_106.replay(root, str(z3))
        self.assertEqual(result["status"], "passed")
        self.assertEqual(set(result["obligations"]), set(target_106.PURPOSES))
        self.assertTrue(
            all(
                record["solver_result"] == "unsat"
                for record in result["obligations"].values()
            )
        )


class Target106PipelineScopeTests(unittest.TestCase):
    def make_rows(self) -> list[dict[str, str]]:
        rows = [
            {
                "target": f"target-{index}",
                "input_order": str(index),
                "exact_output_determinism_status": "not-run",
                "completeness_modulo_reviewed_equivalence_status": "not-run",
            }
            for index in range(62)
        ]
        rows[0].update(
            {"target": target_013.TARGET, "input_order": target_013.INPUT_ORDER}
        )
        rows[1].update(
            {"target": target_029.TARGET, "input_order": target_029.INPUT_ORDER}
        )
        rows[2].update(
            {"target": target_106.TARGET, "input_order": target_106.INPUT_ORDER}
        )
        rows[0].update(
            {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
        )
        rows[1].update(
            {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
        )
        return rows

    @staticmethod
    def preserved_results() -> dict[tuple[str, str], dict[str, str]]:
        return {
            (target_013.TARGET, target_013.INPUT_ORDER): {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            },
            (target_029.TARGET, target_029.INPUT_ORDER): {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            },
        }

    def test_update_preserves_013_029_and_all_other_rows(self) -> None:
        rows = self.make_rows()
        before = copy.deepcopy(rows)
        updated_csv, updated_json = target_pipeline.apply_crosswalk_result_update(
            rows,
            copy.deepcopy(rows),
            target=target_106.TARGET,
            input_order=target_106.INPUT_ORDER,
            statuses={
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            },
            preserved_results=self.preserved_results(),
        )
        self.assertEqual(updated_csv, updated_json)
        for old, new in zip(before, updated_csv):
            if new["target"] == target_106.TARGET:
                self.assertEqual(
                    new["completeness_modulo_reviewed_equivalence_status"],
                    "conditional-complete",
                )
            else:
                self.assertEqual(new, old)

    def test_update_rejects_mutated_013_029_or_unrelated_row(self) -> None:
        for index in (0, 1, 7):
            with self.subTest(index=index):
                rows = self.make_rows()
                rows[index]["exact_output_determinism_status"] = "solver-unknown"
                with self.assertRaises(ValueError):
                    target_pipeline.apply_crosswalk_result_update(
                        rows,
                        copy.deepcopy(rows),
                        target=target_106.TARGET,
                        input_order=target_106.INPUT_ORDER,
                        statuses={
                            "exact_output_determinism_status": (
                                "conditional-complete"
                            ),
                            "completeness_modulo_reviewed_equivalence_status": (
                                "conditional-complete"
                            ),
                        },
                        preserved_results=self.preserved_results(),
                    )


if __name__ == "__main__":
    unittest.main()
