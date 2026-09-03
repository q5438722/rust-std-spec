#!/usr/bin/env python3
from __future__ import annotations

import copy
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from checker_guards import GuardError, example_obligation, validate_obligation


class CheckerGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text, self.metadata = example_obligation()

    def assert_rejected(
        self, text: str | None = None, metadata: dict | None = None
    ) -> None:
        with self.assertRaises(GuardError):
            validate_obligation(
                text if text is not None else self.text,
                metadata if metadata is not None else self.metadata,
            )

    def laundering_obligation(
        self, expression: str, helper_definition: str = ""
    ) -> str:
        text = self.text
        if helper_definition:
            text = text.replace(
                "(define-fun TargetDefinition_T",
                f"{helper_definition}(define-fun TargetDefinition_T",
            )
        return text.replace(
            "(and (= (y_value y) (CallbackStep x b))\n"
            "       (= (s_value s) (x_value x)))",
            f"(and (= (y_value y) {expression})\n"
            "       (= (s_value s) (CallbackStep x b)))",
        )

    def test_reference_obligation_is_accepted(self) -> None:
        validate_obligation(self.text, self.metadata)

    def test_reference_obligation_executes_cleanly_with_z3(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        process = subprocess.run(
            [str(z3), "-in", "-smt2"],
            input=self.text,
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout, "unsat\n")
        self.assertEqual(process.stderr, "")

    def test_datatype_incompatible_logic_is_rejected(self) -> None:
        text = self.text.replace(
            "(set-logic ALL)",
            "(set-logic QF_LIA)",
        )
        self.assert_rejected(text=text)

    def test_fresh_global_answer_constant_is_rejected(self) -> None:
        text = self.text.replace(
            "(declare-const b Boundary)",
            "(declare-const b Boundary)\n(declare-const forged_answer Int)",
        ).replace(
            "(and (= (y_value y) (CallbackStep x b))\n"
            "       (= (s_value s) (x_value x)))",
            "(and (= (y_value y) forged_answer)\n"
            "       (= (s_value s) (CallbackStep x b)))",
        )
        self.assert_rejected(text=text)

    def test_requires_cannot_capture_principal_constants(self) -> None:
        text = self.text.replace(
            "(define-fun Requires_T ((x Input)) Bool true)",
            "(define-fun Requires_T ((x Input)) Bool\n"
            "  (and (= (y_value y1) (y_value y2))\n"
            "       (= (s_value s1) (s_value s2))))",
        )
        self.assert_rejected(text=text)

    def test_required_definition_signature_is_checked(self) -> None:
        text = self.text.replace(
            "(define-fun Requires_T ((x Input)) Bool true)",
            "(define-fun Requires_T ((x Boundary)) Bool true)",
        )
        self.assert_rejected(text=text)

    def test_additional_false_assertion_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            "(assert false)\n(check-sat)",
        )
        self.assert_rejected(text=text)

    def test_additional_principal_equality_assertion_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            "(assert (= (y_value y1) (y_value y2)))\n(check-sat)",
        )
        self.assert_rejected(text=text)

    def test_check_sat_assuming_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            "(check-sat-assuming (false))",
        )
        self.assert_rejected(text=text)

    def test_output_echo_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            '(echo "unsat")\n(check-sat)',
        )
        self.assert_rejected(text=text)

    def test_renamed_functionality_function_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            "(declare-fun ChosenValue (Input Boundary) Output)\n(check-sat)",
        )
        self.assert_rejected(text=text)

    def test_renamed_functionality_relation_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            "(declare-fun HoldsNow (Input Boundary Output State) Bool)\n"
            "(check-sat)",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "HoldsNow",
                "role": "source_transition",
                "source_citations": ["fake.rs:1"],
            }
        ]
        self.assert_rejected(text=text, metadata=metadata)

    def test_scalar_whole_target_function_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            "(declare-fun ComputeAnswer (Input Boundary) Int)\n(check-sat)",
        ).replace(
            "(CallbackStep x b)",
            "(ComputeAnswer x b)",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "ComputeAnswer",
                "role": "source_transition",
                "source_citations": ["fake.rs:1"],
            }
        ]
        self.assert_rejected(text=text, metadata=metadata)

    def test_whole_target_relation_without_boundary_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            "(declare-fun WholeResult (Input Output State) Bool)\n(check-sat)",
        ).replace(
            "(and (= (y_value y) (CallbackStep x b))\n"
            "       (= (s_value s) (x_value x)))",
            "(WholeResult x y s)",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "WholeResult",
                "role": "source_transition",
                "source_citations": ["fake.rs:1"],
            }
        ]
        self.assert_rejected(text=text, metadata=metadata)

    def test_scalar_whole_target_without_boundary_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            "(declare-fun ComputeValue (Input) Int)\n(check-sat)",
        ).replace(
            "(CallbackStep x b)",
            "(ComputeValue x)",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "ComputeValue",
                "role": "source_transition",
                "source_citations": ["fake.rs:1"],
            }
        ]
        self.assert_rejected(text=text, metadata=metadata)

    def test_primitive_signature_answer_function_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            "(declare-fun ComputeValue (Int) Int)\n(check-sat)",
        ).replace(
            "(CallbackStep x b)",
            "(ComputeValue (x_value x))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "ComputeValue",
                "role": "source_transition",
                "source_citations": ["fake.rs:1"],
            }
        ]
        self.assert_rejected(text=text, metadata=metadata)

    def test_primitive_signature_whole_relation_is_rejected(self) -> None:
        text = self.text.replace(
            "(check-sat)",
            "(declare-fun WholeResult (Int Int Int) Bool)\n(check-sat)",
        ).replace(
            "(and (= (y_value y) (CallbackStep x b))\n"
            "       (= (s_value s) (x_value x)))",
            "(WholeResult (x_value x) (y_value y) (s_value s))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "WholeResult",
                "role": "source_transition",
                "source_citations": ["fake.rs:1"],
            }
        ]
        self.assert_rejected(text=text, metadata=metadata)

    def test_direct_boundary_output_laundering_is_rejected(self) -> None:
        text = self.text.replace(
            "(= (y_value y) (CallbackStep x b))",
            "(= (y_value y) (b_callback_value b))",
        )
        self.assert_rejected(text=text)

    def test_reversed_boundary_output_laundering_is_rejected(self) -> None:
        text = self.text.replace(
            "(= (y_value y) (CallbackStep x b))",
            "(= (b_callback_value b) (y_value y))",
        )
        self.assert_rejected(text=text)

    def test_let_mediated_boundary_output_laundering_is_rejected(self) -> None:
        text = self.text.replace(
            "(= (y_value y) (CallbackStep x b))",
            "(= (y_value y) "
            "(let ((hidden (b_callback_value b))) hidden))",
        )
        self.assert_rejected(text=text)

    def test_direct_subtraction_cancellation_is_rejected(self) -> None:
        text = self.laundering_obligation(
            "(+ (b_callback_value b) "
            "(- (x_value x) (x_value x)))"
        )
        self.assert_rejected(text=text)

    def test_direct_zero_multiplication_cancellation_is_rejected(self) -> None:
        text = self.laundering_obligation(
            "(+ (b_callback_value b) (* 0 (x_value x)))"
        )
        self.assert_rejected(text=text)

    def test_let_mediated_subtraction_cancellation_is_rejected(self) -> None:
        text = self.laundering_obligation(
            "(let ((left (x_value x)) (right (x_value x))) "
            "(+ (b_callback_value b) (- left right)))"
        )
        self.assert_rejected(text=text)

    def test_let_mediated_zero_multiplication_cancellation_is_rejected(
        self,
    ) -> None:
        text = self.laundering_obligation(
            "(let ((zero (- 2 2))) "
            "(+ (b_callback_value b) (* zero (x_value x))))"
        )
        self.assert_rejected(text=text)

    def test_helper_mediated_subtraction_cancellation_is_rejected(self) -> None:
        text = self.laundering_obligation(
            "(+ (b_callback_value b) (CancelInput (x_value x)))",
            "(define-fun CancelInput ((value Int)) Int (- value value))\n",
        )
        self.assert_rejected(text=text)

    def test_helper_mediated_zero_multiplication_cancellation_is_rejected(
        self,
    ) -> None:
        text = self.laundering_obligation(
            "(+ (b_callback_value b) (ScaleInput 0 (x_value x)))",
            "(define-fun ScaleInput ((factor Int) (value Int)) Int "
            "(* factor value))\n",
        )
        self.assert_rejected(text=text)

    def test_non_cancelling_affine_input_dependency_is_accepted(self) -> None:
        text = self.laundering_obligation(
            "(+ (b_callback_value b) (* 2 (x_value x)))"
        )
        validate_obligation(text, self.metadata)

    def test_reachable_global_helper_laundering_is_rejected(self) -> None:
        text = self.text.replace(
            "(define-fun TargetDefinition_T",
            "(define-fun HiddenBoundary () Int\n"
            "  (b_callback_value b))\n"
            "(define-fun TargetDefinition_T",
        ).replace(
            "(CallbackStep x b)",
            "HiddenBoundary",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["source_transition_definitions"].append("HiddenBoundary")
        self.assert_rejected(text=text, metadata=metadata)

    def test_renamed_answer_field_role_is_rejected(self) -> None:
        text = self.text.replace("b_callback_value", "b_winner")
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"][0].update(
            {"selector": "b_winner", "role": "selected_output"}
        )
        self.assert_rejected(text=text, metadata=metadata)

    def test_renamed_trace_field_role_is_rejected(self) -> None:
        text = self.text.replace("b_callback_value", "b_steps")
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"][0].update(
            {"selector": "b_steps", "role": "implementation_trace"}
        )
        self.assert_rejected(text=text, metadata=metadata)

    def test_unused_boundary_field_is_rejected(self) -> None:
        text = self.text.replace(
            "(b_callback_value Int)",
            "(b_callback_value Int) (b_extra Int)",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_extra",
                "role": "source_helper_observation",
                "source_citations": ["source.rs:20"],
                "trust_site_ids": ["TS-EXTRA"],
            }
        )
        self.assert_rejected(text=text, metadata=metadata)

    def test_boundary_field_without_metadata_is_rejected(self) -> None:
        text = self.text.replace(
            "(b_callback_value Int)",
            "(b_callback_value Int) (b_unlisted Int)",
        )
        self.assert_rejected(text=text)

    def test_tautological_boundary_field_use_is_rejected(self) -> None:
        text = self.text.replace(
            "(b_callback_value Int)",
            "(b_callback_value Int) (b_extra Int)",
        ).replace(
            "(>= (b_callback_value b) 0)",
            "(and (>= (b_callback_value b) 0) (= (b_extra b) (b_extra b)))",
        ).replace(
            "(= (s_value s) (x_value x))",
            "(and (= (s_value s) (x_value x)) (= (b_extra b) (b_extra b)))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_extra",
                "role": "source_helper_observation",
                "source_citations": ["source.rs:20"],
                "trust_site_ids": ["TS-EXTRA"],
            }
        )
        self.assert_rejected(text=text, metadata=metadata)

    def test_spec_without_target_definition_is_rejected(self) -> None:
        text = self.text.replace(
            "(TargetDefinition_T x b y s))\n"
            "(define-fun Equivalent_T",
            "true)\n(define-fun Equivalent_T",
        )
        self.assert_rejected(text=text)

    def test_semantically_dead_target_call_is_rejected(self) -> None:
        text = self.text.replace(
            "(TargetDefinition_T x b y s))\n"
            "(define-fun Equivalent_T",
            "(or true (TargetDefinition_T x b y s)))\n"
            "(define-fun Equivalent_T",
        )
        self.assert_rejected(text=text)

    def test_nonshared_boundary_in_theorem_is_rejected(self) -> None:
        text = self.text.replace(
            "(declare-const y1 Output)",
            "(declare-const b2 Boundary)\n(declare-const y1 Output)",
        ).replace(
            "(Spec_T x b y2 s2)",
            "(Spec_T x b2 y2 s2)",
        )
        self.assert_rejected(text=text)

    def test_exact_equivalence_cannot_omit_state(self) -> None:
        text = self.text.replace(
            "(and (= (y_value y1) (y_value y2))\n"
            "       (= (s_value s1) (s_value s2))))",
            "(= (y_value y1) (y_value y2)))",
        )
        self.assert_rejected(text=text)

    def test_empty_principal_observation_schema_is_rejected(self) -> None:
        text = self.text.replace(
            "(and (= (y_value y1) (y_value y2))\n"
            "       (= (s_value s1) (s_value s2))))",
            "true)",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["principal_observations"] = []
        self.assert_rejected(text=text, metadata=metadata)

    def test_partial_principal_observation_schema_is_rejected(self) -> None:
        text = self.text.replace(
            "(and (= (y_value y1) (y_value y2))\n"
            "       (= (s_value s1) (s_value s2))))",
            "(= (y_value y1) (y_value y2)))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["principal_observations"] = metadata[
            "principal_observations"
        ][:1]
        self.assert_rejected(text=text, metadata=metadata)

    def test_duplicate_principal_observation_schema_is_rejected(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["principal_observations"].append(
            copy.deepcopy(metadata["principal_observations"][0])
        )
        self.assert_rejected(metadata=metadata)

    def test_substituted_principal_observation_schema_is_rejected(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["principal_observations"][1]["selector"] = "other_state"
        self.assert_rejected(metadata=metadata)

    def test_wrong_principal_observation_sort_is_rejected(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["principal_observations"][0]["sort"] = "Bool"
        self.assert_rejected(metadata=metadata)

    def test_dead_exact_equivalence_equality_is_rejected(self) -> None:
        text = self.text.replace(
            "(= (s_value s1) (s_value s2))",
            "(or true (= (s_value s1) (s_value s2)))",
        )
        self.assert_rejected(text=text)

    def test_unreachable_source_transition_is_rejected(self) -> None:
        text = self.text.replace(
            "(and (= (y_value y) (CallbackStep x b))\n"
            "       (= (s_value s) (x_value x)))",
            "(and (= (y_value y) (x_value x))\n"
            "       (= (s_value s) (+ (x_value x) (b_callback_value b))))",
        )
        self.assert_rejected(text=text)

    def test_cancelling_source_transition_is_rejected(self) -> None:
        text = self.text.replace(
            "(and (= (y_value y) (CallbackStep x b))\n"
            "       (= (s_value s) (x_value x)))",
            "(and (= (y_value y)\n"
            "          (+ (x_value x)\n"
            "             (- (CallbackStep x b) (CallbackStep x b))))\n"
            "       (= (s_value s) (+ (x_value x) (b_callback_value b))))",
        )
        self.assert_rejected(text=text)

    def test_empty_source_transition_metadata_is_rejected(self) -> None:
        metadata = copy.deepcopy(self.metadata)
        metadata["source_transition_definitions"] = []
        self.assert_rejected(metadata=metadata)

    def test_aliased_execution_variables_are_rejected(self) -> None:
        text = self.text.replace("y2", "y1").replace("s2", "s1")
        metadata = copy.deepcopy(self.metadata)
        metadata["theorem_variables"]["output2"] = "y1"
        metadata["theorem_variables"]["state2"] = "s1"
        self.assert_rejected(text=text, metadata=metadata)

    def test_wrong_theorem_variable_sort_is_rejected(self) -> None:
        text = self.text.replace(
            "(declare-const y2 Output)",
            "(declare-const y2 State)",
        )
        self.assert_rejected(text=text)


if __name__ == "__main__":
    unittest.main()
