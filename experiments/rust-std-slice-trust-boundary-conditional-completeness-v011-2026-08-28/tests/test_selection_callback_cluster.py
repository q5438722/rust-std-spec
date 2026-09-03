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
import replay_selection_callback_cluster as replay
import run_selection_callback_cluster as runner
import target_078
import target_079
import target_pipeline


MODULES = (target_078, target_079)


class SelectionCallbackGuardTests(unittest.TestCase):
    def test_all_literal_theorems_pass_the_checker(self) -> None:
        for module in MODULES:
            for purpose in module.PURPOSES:
                with self.subTest(target=module.TARGET, purpose=purpose):
                    text, metadata = module.obligation(purpose)
                    validate_obligation(text, metadata)
                    module.validate_target_obligation(text, metadata)

    def test_active_contract_hashes_and_six_conjuncts_are_exact(self) -> None:
        expected = {
            target_078.TARGET: (
                "8d197563a2e9735beef3c52ff46ea5d3dd44da47b48e3b199654cf3c667490d7",
                "slice_select_partition_cmp",
            ),
            target_079.TARGET: (
                "9366859a88badc5f8d8cdfb15fbc544ef81edb756429e14a887b1ce6c73e3e95",
                "slice_select_partition_key",
            ),
        }
        for module in MODULES:
            digest, partition = expected[module.TARGET]
            self.assertEqual(module.ACTIVE_CONTRACT_SHA256, digest)
            for fragment in (
                "final(slice)@ == final(ret.0)@",
                "final(ret.0)@.len() == index",
                "*final(ret.1) == final(slice)@[index as int]",
                "final(ret.2)@.len() ==",
                "slice_permutation",
                partition,
            ):
                self.assertIn(fragment, module.ACTIVE_CONTRACT_TEXT)
            metadata = module.obligation_metadata(module.PRIMARY)
            self.assertEqual(
                tuple(metadata["active_contract_conjuncts"]),
                module.ACTIVE_CONJUNCTS,
            )

    def test_only_d004_is_admitted_and_opaque_sites_are_replaced(self) -> None:
        for module in MODULES:
            metadata = module.obligation_metadata(module.PRIMARY)
            scope = metadata["boundary_scope"]
            self.assertEqual(
                set(scope["admitted_trust_site_ids"]),
                set(module.ADMITTED_TRUST_SITES),
            )
            self.assertEqual(
                set(scope["excluded_retained_trust_site_ids"]),
                set(module.EXCLUDED_RETAINED_TRUST_SITES),
            )
            self.assertEqual(
                set(scope["context_only_trust_site_ids"]),
                set(module.CONTEXT_ONLY_TRUST_SITES),
            )
            replacement = metadata["source_backed_replacements"][0]
            self.assertEqual(
                set(replacement["replaces_trust_site_ids"]),
                {
                    trust_site
                    for trust_site in module.EXCLUDED_RETAINED_TRUST_SITES
                    if trust_site.endswith("D002")
                },
            )
            self.assertEqual(
                set(metadata["unresolved_source_model_trust_site_ids"]),
                {
                    trust_site
                    for trust_site in module.EXCLUDED_RETAINED_TRUST_SITES
                    if not trust_site.endswith("D002")
                },
            )
            for field in metadata["boundary_fields"]:
                self.assertEqual(
                    set(field["trust_site_ids"]),
                    set(module.ADMITTED_TRUST_SITES),
                )

    def test_boundary_contains_relations_but_no_realized_trace_or_answer(
        self,
    ) -> None:
        for module in MODULES:
            manifest = module.boundary_manifest()
            observed = json.dumps(
                manifest["shared_boundary_observations"]
            ).lower()
            self.assertIn("state", observed)
            for forbidden in (
                "final slice",
                "final callback state",
                "returned range",
                "pivot",
                "permutation",
                "invocation count",
                "realized invocation trace",
            ):
                self.assertNotIn(forbidden, observed)

    def test_callback_boundary_is_functional(self) -> None:
        compare = target_078.obligation_text(target_078.PRIMARY)
        self.assertIn("(define-fun CallbackTransitionFunctional", compare)
        self.assertIn("b_compare_next_state_relation", compare)
        self.assertNotIn("b_compare_next_delta_low", compare)
        self.assertNotIn("b_compare_next_delta_high", compare)
        key = target_079.obligation_text(target_079.PRIMARY)
        self.assertIn("(define-fun CallbackTransitionFunctional", key)
        for selector in (
            "b_key_result_relation",
            "b_key_next_state_relation",
            "b_key_panic_relation",
            "b_ord_lt_result_relation",
            "b_ord_lt_next_state_relation",
            "b_ord_lt_panic_relation",
        ):
            self.assertIn(selector, key)
        self.assertNotIn("b_key_step_relation", key)
        self.assertNotIn("b_ord_lt_step_relation", key)

    def test_comparator_adapter_is_one_call_then_exact_less(self) -> None:
        text = target_078.obligation_text(target_078.PRIMARY)
        start = text.index("(define-fun AdapterNormal")
        end = text.index("(define-fun AdapterPanic", start)
        adapter = text[start:end]
        self.assertEqual(adapter.count("(CompareStep"), 1)
        self.assertIn("(= is_less (= ordering -1))", adapter)
        self.assertNotIn("total", text.lower())

    def test_key_adapter_threads_left_then_right_then_ord(self) -> None:
        text = target_079.obligation_text(target_079.PRIMARY)
        start = text.index("(define-fun AdapterNormal")
        end = text.index("(define-fun AdapterPanic", start)
        adapter = text[start:end]
        first = adapter.index("(KeyStep")
        second = adapter.index("(KeyStep", first + 1)
        ordered = adapter.index("(OrdLtStep", second + 1)
        self.assertLess(first, second)
        self.assertLess(second, ordered)
        self.assertIn("after_left", adapter)
        self.assertIn("after_right", adapter)
        self.assertNotIn("(= left_key right_key)", adapter)

    def test_bounded_source_transitions_and_model_gap_are_explicit(
        self,
    ) -> None:
        for module in MODULES:
            text, metadata = module.obligation(module.PRIMARY)
            target_start = text.index("(define-fun TargetDefinition_T")
            for symbol in module.SOURCE_TRANSITIONS:
                with self.subTest(target=module.TARGET, symbol=symbol):
                    self.assertIn(f"(define-fun {symbol}", text)
                    self.assertIn(
                        f"({symbol} ", text[target_start:]
                    )
            self.assertEqual(
                set(metadata["source_transition_definitions"]),
                set(module.SOURCE_TRANSITIONS),
            )
            self.assertTrue(metadata["domain"]["bounded"])
            self.assertEqual(
                metadata["domain"]["slice_length"],
                "exactly four",
            )
            self.assertFalse(metadata["domain"]["source_model_complete"])
            self.assertEqual(
                metadata["model_status"],
                "missing-source-backed-model",
            )
            for rejected in (
                "InteriorCallbackTraceNormal",
                "MainNarrowingSteps",
                "FallbackReachable",
                "PartitionTransition",
                "RecursiveLoopOrFallbackTransition",
                "ReviewedFinalSequenceEquivalent",
                "AdapterNormalFast",
                "FastContractLeq",
            ):
                self.assertNotIn(rejected, text)

    def test_incomplete_model_metadata_fails_closed(self) -> None:
        text, metadata = target_078.obligation(target_078.PRIMARY)
        metadata = copy.deepcopy(metadata)
        metadata["unresolved_source_model_trust_site_ids"] = []
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_mutating_source_or_contract_calls_fails_closed(self) -> None:
        for module in MODULES:
            text, metadata = module.obligation(module.PRIMARY)
            target_start = text.index("(define-fun TargetDefinition_T")
            for symbol in (
                *module.SOURCE_TRANSITIONS,
                *module.ACTIVE_CONJUNCTS,
            ):
                with self.subTest(target=module.TARGET, symbol=symbol):
                    call = text.index(f"({symbol}", target_start)
                    balance = 0
                    for end in range(call, len(text)):
                        if text[end] == "(":
                            balance += 1
                        elif text[end] == ")":
                            balance -= 1
                            if balance == 0:
                                break
                    mutated = text[:call] + "true" + text[end + 1 :]
                    with self.assertRaises(GuardError):
                        if symbol in module.SOURCE_TRANSITIONS:
                            validate_obligation(mutated, metadata)
                        else:
                            module.validate_target_obligation(
                                mutated, metadata
                            )

    def test_adapter_order_mutations_fail_closed(self) -> None:
        text, metadata = target_078.obligation(target_078.PRIMARY)
        changed = text.replace(
            "(= is_less (= ordering -1))",
            "(= is_less (<= ordering 0))",
            1,
        )
        with self.assertRaises(GuardError):
            target_078.validate_target_obligation(changed, metadata)
        text, metadata = target_079.obligation(target_079.PRIMARY)
        changed = text.replace(
            "        state\n        left\n        left_key\n        after_left",
            "        state\n        right\n        left_key\n        after_left",
            1,
        )
        with self.assertRaises(GuardError):
            target_079.validate_target_obligation(changed, metadata)

    def test_bounded_theorems_and_source_schedule_regressions(
        self,
    ) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for module in MODULES:
            for purpose in module.PURPOSES:
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=module.obligation_text(purpose),
                    text=True,
                    capture_output=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, "unsat\n")
                self.assertEqual(process.stderr, "")
            nonvacuity = subprocess.run(
                [str(z3), "-in", "-smt2"],
                input=module.nonvacuity_text(),
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(
                nonvacuity.returncode, 0, nonvacuity.stderr
            )
            self.assertEqual(nonvacuity.stdout, "sat\n")
            self.assertEqual(nonvacuity.stderr, "")
            wrong_schedule = subprocess.run(
                [str(z3), "-in", "-smt2"],
                input=module.length_four_wrong_schedule_text(),
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(
                wrong_schedule.returncode, 0, wrong_schedule.stderr
            )
            self.assertEqual(wrong_schedule.stdout, "unsat\n")
            self.assertEqual(wrong_schedule.stderr, "")
            source_execution = subprocess.run(
                [str(z3), "-in", "-smt2"],
                input=module.length_four_source_execution_text(),
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(
                source_execution.returncode, 0, source_execution.stderr
            )
            self.assertEqual(source_execution.stdout, "sat\n")
            self.assertEqual(source_execution.stderr, "")
            for case in (
                "descending",
                "mixed",
                "tail-three-middle",
                "tail-three-front",
            ):
                mutation = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=module.small_sort_regression_text(case),
                    text=True,
                    capture_output=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(
                    mutation.returncode, 0, mutation.stderr
                )
                self.assertEqual(mutation.stdout, "unsat\n")
                self.assertEqual(mutation.stderr, "")
            mixed = subprocess.run(
                [str(z3), "-in", "-smt2"],
                input=module.mixed_source_execution_text(),
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(mixed.returncode, 0, mixed.stderr)
            self.assertEqual(mixed.stdout, "sat\n")
            self.assertEqual(mixed.stderr, "")

    def test_all_panic_prefixes_are_solver_reachable(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        self.assertEqual(target_078.panic_probe_kinds(), ("compare",))
        self.assertEqual(
            target_079.panic_probe_kinds(),
            ("first-key", "second-key", "ord-lt"),
        )
        for module in MODULES:
            for kind in module.panic_probe_kinds():
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=module.panic_probe_text(kind),
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertTrue(process.stdout.startswith("sat\n"))
                self.assertEqual(process.stderr, "")
            restored = subprocess.run(
                [str(z3), "-in", "-smt2"],
                input=module.panic_after_shift_text(restored=True),
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(restored.returncode, 0, restored.stderr)
            self.assertEqual(restored.stdout, "sat\n")
            self.assertEqual(restored.stderr, "")
            unrestored = subprocess.run(
                [str(z3), "-in", "-smt2"],
                input=module.panic_after_shift_text(restored=False),
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(unrestored.returncode, 0, unrestored.stderr)
            self.assertEqual(unrestored.stdout, "unsat\n")
            self.assertEqual(unrestored.stderr, "")


class SelectionCallbackWitnessTests(unittest.TestCase):
    def test_functional_boundary_rejects_callback_state_drift(self) -> None:
        for module in MODULES:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "witness.json"
                path.write_text(json.dumps(module.witness_payload()))
                result = replay.replay(path)
            observed = result["functional_boundary_diagnostic"]["observed"]
            self.assertTrue(observed["execution1_is_source_reachable"])
            self.assertFalse(observed["execution2_is_source_reachable"])
            self.assertTrue(observed["execution1_satisfies_active_contract"])
            self.assertTrue(observed["execution2_satisfies_active_contract"])
            self.assertFalse(observed["exact_equivalent"])
            self.assertFalse(observed["reviewed_selection_equivalent"])
            self.assertEqual(
                observed["only_difference"],
                "callback-visible-final-state",
            )

    def test_source_and_negative_witnesses_replay(self) -> None:
        for module in MODULES:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "witness.json"
                path.write_text(json.dumps(module.witness_payload()))
                result = replay.replay(path)
            source = result["bounded_source_execution_witness"]
            self.assertEqual(source["sequence"], [10, 20, 30, 40])
            self.assertEqual(
                source["callback_state"],
                4 if module is target_078 else 12,
            )
            negatives = result["negative_witnesses"]
            self.assertFalse(
                negatives["foreign_identity"][
                    "candidate_satisfies_active_contract"
                ]
            )
            self.assertFalse(
                negatives["malformed_returned_range"][
                    "candidate_satisfies_active_contract"
                ]
            )
            self.assertFalse(
                negatives["callback_final_state_drift"][
                    "reviewed_selection_equivalent"
                ]
            )

    def test_boundary_relation_drift_breaks_replay(self) -> None:
        payload = target_079.witness_payload()
        payload["boundary"]["source_step_relation"][
            "evaluation_order"
        ] = ["f(right)", "f(left)", "Ord::lt"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "witness.json"
            path.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                replay.replay(path)


class SelectionCallbackScopeTests(unittest.TestCase):
    def test_cluster_scope_and_certified_baseline_are_exact(self) -> None:
        self.assertEqual(
            set(runner.CLUSTER_KEYS),
            {
                (target_078.TARGET, target_078.INPUT_ORDER),
                (target_079.TARGET, target_079.INPUT_ORDER),
            },
        )
        self.assertEqual(len(runner.BASELINE_RESULTS), 25)
        self.assertEqual(len(runner.PRESERVED_ARTIFACT_IDS), 25)
        self.assertEqual(
            set(runner.FROZEN_SELECTION_DIRS),
            {
                "077_core_slice_select_nth_unstable",
                "078_core_slice_select_nth_unstable_by",
                "079_core_slice_select_nth_unstable_by_key",
            },
        )

    def test_out_of_scope_ledger_edits_fail_closed(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = copy.deepcopy(csv_rows)
        other = next(
            row
            for row in csv_rows
            if (row["target"], row["input_order"])
            not in set(runner.BASELINE_RESULTS) | set(runner.CLUSTER_KEYS)
        )
        other["exact_output_determinism_status"] = "conditional-complete"
        matching = next(
            row
            for row in json_rows
            if (row["target"], row["input_order"])
            == (other["target"], other["input_order"])
        )
        matching["exact_output_determinism_status"] = "conditional-complete"
        with self.assertRaises(ValueError):
            runner.prepare_crosswalk_reset(csv_rows, json_rows)

    def test_verus_models_have_no_trusted_body(self) -> None:
        for module in MODULES:
            text = (ROOT / module.CONFIG.proof_filename).read_text()
            self.assertNotIn("external_body", text)
            requires = text[
                text.index("pub open spec fn requires_t"):
                text.index("pub open spec fn boundary_t")
            ]
            boundary = text[
                text.index("pub open spec fn boundary_t"):
                text.index("pub open spec fn", text.index(
                    "pub open spec fn boundary_t"
                ) + 1)
            ]
            small_sort = text[
                text.index(
                    "pub open spec fn small_sort_mutable_slice_transition"
                ):
                text.index("pub open spec fn partition_transition")
            ]
            self.assertIn("input.initial.e0 == input.initial.e1", requires)
            self.assertNotIn("input.initial.e0 == input.initial.e1", boundary)
            self.assertIn("state.callback_state,", small_sort)
            self.assertNotIn("&& state.callback_state", small_sort)
            for symbol in (
                "requires_t",
                "boundary_t",
                "spec_t",
                "equivalent_t",
                "target_transition_implies_active_contract",
                "shared_boundary_two_execution_theorem",
                "length_four_one_or_two_adapters_is_impossible",
            ):
                self.assertIn(symbol, text)


if __name__ == "__main__":
    unittest.main()
