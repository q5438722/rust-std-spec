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
import replay_unstable_sort_companions as replay
import run_unstable_sort_companions as runner
import target_080
import target_082


MODULES = (target_080, target_082)


class UnstableSortCompanionGuardTests(unittest.TestCase):
    def test_all_target_obligations_are_checker_valid(self) -> None:
        for module in MODULES:
            for purpose in module.PURPOSES:
                with self.subTest(target=module.TARGET, purpose=purpose):
                    text, metadata = module.obligation(purpose)
                    validate_obligation(text, metadata)
                    module.validate_target_obligation(text, metadata)

    def test_active_contract_hashes_and_conjuncts_are_exact(self) -> None:
        expected = {
            target_080.TARGET: (
                "877e37bea31dc31a92b85282f1d2f633c20aeb5391a5f1f02821cbfa0a09dd4b",
                "slice_sorted_by_ord",
            ),
            target_082.TARGET: (
                "019252db65344fd8830ffbbd90d127355a93541c6fbfab3fde3e6b3abe16e8ae",
                "slice_sorted_by_key",
            ),
        }
        for module in MODULES:
            digest, sortedness = expected[module.TARGET]
            self.assertEqual(module.ACTIVE_CONTRACT_SHA256, digest)
            self.assertIn("slice_permutation", module.ACTIVE_CONTRACT_TEXT)
            self.assertIn(sortedness, module.ACTIVE_CONTRACT_TEXT)
            self.assertIn("core::cmp::Ord", module.ACTIVE_CONTRACT_TEXT)

    def test_primary_theorems_are_unbounded_and_exact_witnesses_are_bounded(
        self,
    ) -> None:
        for module in MODULES:
            primary = module.obligation_metadata(module.PRIMARY)
            exact = module.obligation_metadata(module.EXACT_FINAL_SLICE)
            self.assertFalse(primary["domain"]["bounded"])
            self.assertEqual(
                primary["domain"]["slice_length"],
                "arbitrary nonnegative integer",
            )
            self.assertEqual(
                primary["domain"]["position"],
                "arbitrary valid index when nonempty",
            )
            self.assertTrue(exact["domain"]["bounded"])
            self.assertEqual(exact["domain"]["classification_use"], "exact SAT witness")

    def test_omitting_either_active_conjunct_is_rejected(self) -> None:
        for module in MODULES:
            for purpose in module.PURPOSES:
                text, metadata = module.obligation(purpose)
                start = text.index("(define-fun TargetDefinition_T")
                for symbol in metadata["active_contract_conjuncts"]:
                    with self.subTest(
                        target=module.TARGET,
                        purpose=purpose,
                        symbol=symbol,
                    ):
                        call = text.index(f"({symbol}", start)
                        balance = 0
                        end = call
                        for end in range(call, len(text)):
                            if text[end] == "(":
                                balance += 1
                            elif text[end] == ")":
                                balance -= 1
                                if balance == 0:
                                    break
                        mutated = text[:call] + "true" + text[end + 1 :]
                        with self.assertRaises(GuardError):
                            module.validate_target_obligation(mutated, metadata)

    def test_opaque_whole_sort_relations_are_rejected(self) -> None:
        text, metadata = target_080.obligation(target_080.PRIMARY)
        mutated = text.replace(
            "(declare-const x Input)",
            "(declare-fun WholeSort (Input Boundary Output State) Bool)\n"
            "(declare-const x Input)",
        )
        start = mutated.index("(define-fun TargetDefinition_T")
        end = mutated.index("(define-fun Spec_T", start)
        mutated = (
            mutated[:start]
            + """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (WholeSort x b y s))
"""
            + mutated[end:]
        )
        changed = copy.deepcopy(metadata)
        changed["declared_functions"] = [
            {
                "symbol": "WholeSort",
                "role": "source_transition",
                "source_citations": [
                    "core/src/slice/sort/unstable/mod.rs:22-58"
                ],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(mutated, changed)

    def test_answer_and_trace_boundary_roles_are_rejected(self) -> None:
        text, metadata = target_082.obligation(target_082.PRIMARY)
        for role in ("final_permutation", "full_execution_trace"):
            with self.subTest(role=role):
                changed = copy.deepcopy(metadata)
                changed["boundary_fields"][0]["role"] = role
                with self.assertRaises(GuardError):
                    validate_obligation(text, changed)

    def test_only_genuine_lower_sites_are_admitted(self) -> None:
        expected = {
            target_080.TARGET: (
                {"TS-080-D003"},
                {"TS-080-D002", "TS-080-E001"},
            ),
            target_082.TARGET: (
                {"TS-082-D004"},
                {"TS-082-D002", "TS-082-D003", "TS-082-E001"},
            ),
        }
        for module in MODULES:
            admitted, excluded = expected[module.TARGET]
            manifest = module.boundary_manifest()
            self.assertEqual(
                set(manifest["admitted_trust_site_ids"]), admitted
            )
            self.assertEqual(
                {
                    item["trust_site_id"]
                    for item in manifest["excluded_retained_sites"]
                },
                excluded,
            )
            observed = json.dumps(
                manifest["shared_boundary_observations"]
            ).lower()
            for forbidden in (
                "final sequence",
                "permutation",
                "selected ordering",
                "trace",
            ):
                self.assertNotIn(forbidden, observed)

    def test_ord_totality_is_bound_to_each_active_type_constraint(self) -> None:
        for module, expected_bound in (
            (target_080, "T: core::cmp::Ord"),
            (target_082, "K: core::cmp::Ord"),
        ):
            metadata = module.obligation_metadata(module.PRIMARY)
            self.assertEqual(
                metadata["ord_totality_basis"]["type_bound"], expected_bound
            )
            self.assertTrue(
                metadata["ord_totality_basis"]["not_inherited_from_target_081"]
            )
            changed = copy.deepcopy(metadata)
            changed["ord_totality_basis"]["type_bound"] = "unconstrained comparator"
            with self.assertRaises(GuardError):
                module.validate_target_obligation(
                    module.obligation_text(module.PRIMARY), changed
                )

    def test_solver_results_match_classification_evidence(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        expected = {
            target_080.PRIMARY: "unsat\n",
            target_080.BOUNDED_SANITY: "unsat\n",
            target_080.EXACT_FINAL_SLICE: "sat\n",
        }
        for module in MODULES:
            for purpose, result in expected.items():
                with self.subTest(target=module.TARGET, purpose=purpose):
                    process = subprocess.run(
                        [str(z3), "-in", "-smt2"],
                        input=module.obligation_text(purpose),
                        text=True,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, result)
                    self.assertEqual(process.stderr, "")

    def test_fixed_models_and_equivalence_probes_are_sat(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for module in MODULES:
            cases = (
                module.fixed_exact_model_text(),
                module.equivalence_probe_text(positive=True),
                module.equivalence_probe_text(positive=False),
            )
            for index, text in enumerate(cases):
                with self.subTest(target=module.TARGET, case=index):
                    process = subprocess.run(
                        [str(z3), "-in", "-smt2"],
                        input=text,
                        text=True,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertTrue(process.stdout.startswith("sat\n"))
                    self.assertEqual(process.stderr, "")

    def test_witness_replay_preserves_exact_observations(self) -> None:
        for module in MODULES:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "witness.json"
                path.write_text(
                    json.dumps(module.witness_payload(), sort_keys=True) + "\n"
                )
                result = replay.replay(path)
            exact = result["exact_final_slice_counterexample"]
            self.assertTrue(exact["execution1_satisfies_active_contract"])
            self.assertTrue(exact["execution2_satisfies_active_contract"])
            self.assertTrue(exact["identity_multiplicities_equal"])
            self.assertTrue(exact["callback_final_state_equal"])
            self.assertTrue(exact["reviewed_equal_class_equivalent"])
            self.assertFalse(exact["exact_final_slice_equal"])

    def test_foreign_unequal_class_and_callback_drift_are_rejected(self) -> None:
        for module in MODULES:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "witness.json"
                path.write_text(json.dumps(module.witness_payload()))
                result = replay.replay(path)
            negatives = result["negative_equivalence_witnesses"]
            self.assertTrue(negatives["foreign_identity_negative_witness"])
            self.assertTrue(negatives["unequal_class_negative_witness"])
            self.assertTrue(negatives["callback_state_drift_negative_witness"])
            self.assertTrue(
                negatives["callback_state_drift_rejected_by_contract"]
            )

    def test_key_extraction_drift_is_not_a_fixed_boundary_witness(self) -> None:
        payload = target_082.witness_payload()
        payload["exact_final_slice_counterexample"]["boundary"][
            "key_by_identity"
        ].pop("11")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "witness.json"
            path.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                replay.replay(path)

    def test_exact_multiset_cannot_be_removed_from_weak_equivalence(self) -> None:
        for module in MODULES:
            text, metadata = module.obligation(module.BOUNDED_SANITY)
            mutated = text.replace(
                "    (SameElementMultiset s1 s2)\n",
                "",
            )
            validate_obligation(mutated, metadata)
            with self.assertRaises(GuardError):
                module.validate_target_obligation(mutated, metadata)

    def test_unit_callback_and_non_tie_observations_remain_exact(self) -> None:
        replacements = (
            ("    (= (y_return_unit y1) (y_return_unit y2))\n", ""),
            ("    (= (s_callback_state s1) (s_callback_state s2))\n", ""),
            (
                "    (= (ObservedClass b (s_final2 s1))\n"
                "       (ObservedClass b (s_final2 s2))))",
                "    true)",
            ),
        )
        for module in MODULES:
            text, metadata = module.obligation(module.BOUNDED_SANITY)
            for original, replacement in replacements:
                with self.subTest(target=module.TARGET, removed=original[:30]):
                    self.assertIn(original, text)
                    mutated = text.replace(original, replacement, 1)
                    with self.assertRaises(GuardError):
                        module.validate_target_obligation(mutated, metadata)

    def test_cluster_scope_is_exact_and_baseline_has_22_trees(self) -> None:
        self.assertEqual(
            set(runner.CLUSTER_KEYS),
            {
                (target_080.TARGET, target_080.INPUT_ORDER),
                (target_082.TARGET, target_082.INPUT_ORDER),
            },
        )
        self.assertEqual(len(runner.BASELINE_RESULTS), 22)
        self.assertEqual(len(runner.PRESERVED_ARTIFACT_IDS), 22)
        self.assertTrue(
            all(
                not artifact.startswith(("077_", "078_", "079_"))
                for artifact in runner.PRESERVED_ARTIFACT_IDS
            )
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
        matching_json = next(
            row
            for row in json_rows
            if (row["target"], row["input_order"])
            == (other["target"], other["input_order"])
        )
        matching_json["exact_output_determinism_status"] = "conditional-complete"
        with self.assertRaises(ValueError):
            runner.prepare_crosswalk_reset(csv_rows, json_rows)

    def test_experiment_local_verus_models_have_no_external_body(self) -> None:
        for module in MODULES:
            text = (ROOT / module.CONFIG.proof_filename).read_text()
            self.assertNotIn("external_body", text)
            self.assertIn(
                "arbitrary_length_order_statistic_classes_are_unique", text
            )


if __name__ == "__main__":
    unittest.main()
