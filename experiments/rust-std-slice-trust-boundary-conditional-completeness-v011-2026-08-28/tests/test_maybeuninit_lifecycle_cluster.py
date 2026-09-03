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
import replay_maybeuninit_lifecycle_cluster as replay_cluster
import run_maybeuninit_lifecycle_cluster as run_cluster
import target_025
import target_026
import target_119
import target_pipeline


MODULES = (target_026, target_119, target_025)


class MaybeUninitLifecycleGuardTests(unittest.TestCase):
    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for module in MODULES:
            for purpose in module.PURPOSES:
                with self.subTest(target=module.TARGET, purpose=purpose):
                    text, metadata = module.obligation(purpose)
                    validate_obligation(text, metadata)
                    module.validate_target_obligation(text, metadata)

    def test_active_contract_identities_and_conjuncts_are_exact(self) -> None:
        expected = {
            target_025.TARGET: (
                "ec9d059a1f66ae03009745a3d37edfc5306f2c23387856ea9aa3f52cfff09efe",
                ("maybe_uninit_drop_all", "final(slice)@.len()"),
            ),
            target_026.TARGET: (
                "8d0e90b87ee12383ef38b353ff71f43a4136f565d0ae0f63651ee295c06f649a",
                ("ret@ ==", "final(ret)@.len()", "maybe_uninit_all_initialized"),
            ),
            target_119.TARGET: (
                "0e3746ad6530835f74de584a989ea1c6126fdb297454de35509cbdb05fd8c54b",
                ("ret@ == src@", "maybe_uninit_written_from", "final(ret)@.len()"),
            ),
        }
        for module in MODULES:
            digest, clauses = expected[module.TARGET]
            self.assertEqual(module.ACTIVE_CONTRACT_SHA256, digest)
            for clause in clauses:
                self.assertIn(clause, module.ACTIVE_CONTRACT_TEXT)
            metadata = module.obligation_metadata(module.PRIMARY)
            self.assertEqual(
                set(metadata["contract_translation"]["active_conjuncts"]),
                set(module.ACTIVE_CONJUNCT_SYMBOLS),
            )

    def test_retained_answer_sites_are_excluded_not_relabelled(self) -> None:
        for module, expected in (
            (
                target_025,
                {"TS-025-D002", "TS-025-E001"},
            ),
            (
                target_026,
                {"TS-026-D002", "TS-026-E001"},
            ),
        ):
            metadata = module.obligation_metadata(module.PRIMARY)
            scope = metadata["boundary_scope"]
            self.assertEqual(
                set(scope["excluded_retained_trust_site_ids"]), expected
            )
            admitted = set(scope["admitted_trust_site_ids"])
            self.assertTrue(expected.isdisjoint(admitted))
            for field in metadata["boundary_fields"]:
                self.assertTrue(
                    expected.isdisjoint(field.get("trust_site_ids", []))
                )
            replaced = {
                site
                for replacement in metadata["source_backed_replacements"]
                for site in replacement["replaces_trust_site_ids"]
            }
            self.assertEqual(replaced, expected)

    def test_boundary_fields_do_not_launder_answers_or_final_state(self) -> None:
        forbidden = (
            "returned reference",
            "resulting storage",
            "aggregate final",
            "answer encoding",
            "complete target execution trace",
        )
        for module in MODULES:
            manifest = module.boundary_manifest()
            serialized_fields = json.dumps(
                manifest["shared_boundary_observations"], sort_keys=True
            ).lower()
            for phrase in forbidden:
                self.assertNotIn(phrase, serialized_fields)
            self.assertTrue(manifest["boundary_narrower_than_target"])

    def test_119_composes_026_and_retains_only_one_step_sites(self) -> None:
        metadata = target_119.obligation_metadata(target_119.PRIMARY)
        lower = metadata["source_transition_bindings"][
            "assume_init_mut_composition"
        ]
        self.assertEqual(lower["lower_target"], target_026.TARGET)
        self.assertEqual(
            lower["lower_active_contract_sha256"],
            target_026.ACTIVE_CONTRACT_SHA256,
        )
        self.assertEqual(
            set(lower["trust_site_ids"]), {"TS-119-D002", "TS-119-E003"}
        )
        restriction = metadata["source_transition_bindings"][
            "one_step_writes"
        ]["restriction"]
        self.assertIn("one Clone/write step", restriction)
        manifest = target_119.boundary_manifest()
        self.assertIn("only one", manifest["retained_site_restriction"])

    def test_source_order_count_and_panic_cleanup_probes_are_complete(self) -> None:
        required_025 = {
            "invalid_no_op_drop",
            "invalid_partial_drop",
            "invalid_duplicate_drop",
            "invalid_out_of_order_drop",
            "invalid_drop_count",
            "invalid_callback_order",
            "invalid_callback_state",
        }
        required_119 = {
            "invalid_no_op_write",
            "invalid_partial_write",
            "invalid_omitted_initialization",
            "invalid_duplicate_write",
            "invalid_out_of_order_write",
            "invalid_clone_count",
            "invalid_write_count",
            "invalid_clone_callback_order",
            "invalid_callback_state",
            "valid_clone_panic_at_0",
            "valid_clone_panic_at_1",
            "valid_clone_panic_at_2",
            "invalid_panic_partial_cleanup",
            "invalid_panic_duplicate_cleanup",
            "invalid_panic_out_of_order_cleanup",
            "invalid_panic_wrong_guard_count",
            "invalid_clone_after_panic",
        }
        self.assertTrue(required_025 <= set(target_025.PROBE_CASES))
        self.assertTrue(required_119 <= set(target_119.PROBE_CASES))
        for index in range(3):
            semantics = target_119.panic_probe_semantics(
                f"valid_clone_panic_at_{index}"
            )
            self.assertTrue(semantics["valid"])
            self.assertEqual(semantics["clone_call_count"], index + 1)
            self.assertEqual(semantics["write_count"], index)
            self.assertEqual(semantics["cleanup_drop_indices"], list(range(index)))
            self.assertEqual(
                semantics["final_storage"],
                ["Uninitialized", "Uninitialized", "Uninitialized"],
            )

    def test_ordering_and_panic_probes_mutate_reachable_source_paths(self) -> None:
        drop_text = target_025.obligation(target_025.PRIMARY)[0]
        self.assertIn("(DropSourceExecution_T x b)", drop_text)
        self.assertIn(
            "(DropIndexAtStep x step)",
            drop_text,
        )
        for name in (
            "invalid_duplicate_drop",
            "invalid_out_of_order_drop",
            "invalid_drop_count",
        ):
            probe = target_025.probe_text(name)
            assertion = probe.rsplit("(assert", 1)[1]
            self.assertIn("(Spec_T x b y1 s1)", assertion)
            self.assertNotIn("(DropIndexAtStep", assertion)
            self.assertNotIn("(DropOperationCount", assertion)

        write_text = target_119.obligation(target_119.PRIMARY)[0]
        self.assertIn("(CloneWriteSourceExecution_T x b)", write_text)
        self.assertIn("(WriteIndexAtStep x step)", write_text)
        for name in (
            "invalid_duplicate_write",
            "invalid_out_of_order_write",
            "invalid_clone_count",
            "invalid_write_count",
        ):
            probe = target_119.probe_text(name)
            assertion = probe.rsplit("(assert", 1)[1]
            self.assertIn("(Spec_T x b y1 s1)", assertion)
            self.assertNotIn("(WriteIndexAtStep", assertion)
            self.assertNotIn("(WriteOperationCount", assertion)

        for name in (
            "valid_clone_panic_at_0",
            "valid_clone_panic_at_1",
            "valid_clone_panic_at_2",
            "invalid_panic_partial_cleanup",
            "invalid_panic_duplicate_cleanup",
            "invalid_panic_out_of_order_cleanup",
            "invalid_panic_wrong_guard_count",
            "invalid_clone_after_panic",
        ):
            panic = target_119.PROBE_CASES[name]["panic_index"]
            probe = target_119.probe_text(name)
            assertion = probe.rsplit("(assert", 1)[1]
            self.assertIn(f"(PanicBoundary_T x b {panic})", assertion)
            self.assertIn(f"(PanicSpec_T x b {panic} p1)", assertion)
            self.assertIn(
                "(PanicTargetDefinition_T x b panic_index p)",
                probe,
            )
            self.assertNotIn("(define-fun CloneCalled", probe)
            self.assertNotIn("(define-fun FinalCell", probe)

    def test_required_empty_zst_invalid_mask_pointer_and_frame_probes_exist(
        self,
    ) -> None:
        for module in MODULES:
            names = set(module.PROBE_CASES)
            self.assertTrue(any("empty" in name for name in names))
            self.assertTrue(any("zst" in name for name in names))
            self.assertTrue(any("pointer" in name for name in names))
            self.assertTrue(any("frame" in name for name in names))
        self.assertIn("invalid_initialization_mask", target_025.PROBE_CASES)
        self.assertIn("invalid_initialization_mask", target_026.PROBE_CASES)
        self.assertIn("invalid_unequal_lengths", target_119.PROBE_CASES)

    def test_reviewed_models_fail_closed_on_semantic_mutations(self) -> None:
        mutations = (
            (
                target_025,
                "(define-fun DropFinalStorage\n"
                "  ((x Input) (b Boundary)) (Array Int Cell)\n"
                "  ((as const (Array Int Cell)) Uninitialized))",
                "(define-fun DropFinalStorage\n"
                "  ((x Input) (b Boundary)) (Array Int Cell)\n"
                "  (x_storage x))",
            ),
            (
                target_026,
                "(define-fun AssumeInitMutReturnBorrow ((x Input)) Int\n"
                "  (x_destination_borrow x))",
                "(define-fun AssumeInitMutReturnBorrow ((x Input)) Int\n"
                "  (+ (x_destination_borrow x) 1))",
            ),
            (
                target_119,
                "(define-fun WriteCloneFinalStorage\n"
                "  ((x Input)) (Array Int Cell)\n"
                "  ((_ map Initialized) (x_source_values x)))",
                "(define-fun WriteCloneFinalStorage\n"
                "  ((x Input)) (Array Int Cell)\n"
                "  (x_destination_storage x))",
            ),
            (
                target_119,
                "(define-fun AssumeInitMutReturnAllocation ((x Input)) Int\n"
                "  (x_destination_allocation x))",
                "(define-fun AssumeInitMutReturnAllocation ((x Input)) Int\n"
                "  (x_source_allocation x))",
            ),
        )
        for module, old, new in mutations:
            text, metadata = module.obligation(module.PRIMARY)
            self.assertIn(old, text)
            with self.subTest(target=module.TARGET, mutation=old.splitlines()[0]):
                with self.assertRaises(GuardError):
                    module.validate_target_obligation(
                        text.replace(old, new, 1), metadata
                    )

    def test_omitting_119_lower_composition_is_rejected(self) -> None:
        text, metadata = target_119.obligation(target_119.PRIMARY)
        required = (
            "       (= (s_return_values s) (AssumeInitMutReturnValues x))\n"
        )
        self.assertIn(required, text)
        with self.assertRaises(GuardError):
            target_119.validate_target_obligation(
                text.replace(required, "", 1), metadata
            )

    def test_excluded_site_reuse_and_final_boundary_field_are_rejected(
        self,
    ) -> None:
        text, metadata = target_026.obligation(target_026.PRIMARY)
        mutated = copy.deepcopy(metadata)
        mutated["boundary_fields"][0]["trust_site_ids"] = ["TS-026-E001"]
        with self.assertRaises(GuardError):
            validate_obligation(text, mutated)

        mutated = copy.deepcopy(metadata)
        mutated["boundary_fields"][0]["role"] = "aggregate_final_state"
        with self.assertRaises(GuardError):
            validate_obligation(text, mutated)

    def test_no_experiment_local_verus_model_has_external_body(self) -> None:
        for path in run_cluster.SOURCE_MODELS.values():
            self.assertTrue(path.is_file())
            self.assertNotIn("external_body", path.read_text())


class MaybeUninitLifecycleSolverTests(unittest.TestCase):
    def test_real_solver_results_and_all_probes(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        expected_obligations = replay_cluster.EXPECTED_THEOREM_RESULTS
        for module in MODULES:
            for purpose in module.PURPOSES:
                text, _ = module.obligation(purpose)
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=text,
                    text=True,
                    capture_output=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stderr, "")
                self.assertEqual(
                    process.stdout,
                    f"{expected_obligations[module.TARGET][purpose]}\n",
                )
            for name, expected in module.PROBE_EXPECTED_RESULTS.items():
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=module.probe_text(name),
                    text=True,
                    capture_output=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(
                    (process.returncode, process.stdout, process.stderr),
                    (0, f"{expected}\n", ""),
                    f"{module.TARGET}/{name}",
                )

    def test_target_026_fixed_countermodel_and_semantic_replay(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        process = subprocess.run(
            [str(z3), "-in", "-smt2"],
            input=target_026.fixed_model_text(),
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout.splitlines()[0], "sat")
        self.assertEqual(process.stderr, "")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "witness.json"
            path.write_text(
                json.dumps(target_026.witness_payload(), sort_keys=True) + "\n"
            )
            result = replay_cluster.replay_target_026_witness(path)
        self.assertEqual(result["status"], "passed")
        self.assertTrue(result["observed"]["exact_output_equal"])
        self.assertFalse(result["observed"]["full_exact_equivalent"])

    def test_classification_is_derived_from_solver_and_replay(self) -> None:
        self.assertEqual(
            run_cluster.derive_classification(
                "unsat", sat_witness_replayed=False
            ),
            "conditional-complete",
        )
        self.assertEqual(
            run_cluster.derive_classification(
                "sat", sat_witness_replayed=True
            ),
            "conditional-incomplete",
        )
        self.assertEqual(
            run_cluster.derive_classification(
                "unknown", sat_witness_replayed=False
            ),
            "solver-unknown",
        )
        with self.assertRaises(RuntimeError):
            run_cluster.derive_classification(
                "sat", sat_witness_replayed=False
            )

    def test_atomic_ledger_update_changes_only_three_rows(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        for rows in (csv_rows, json_rows):
            for row in rows:
                if row["target"] in {
                    target_025.TARGET,
                    target_026.TARGET,
                    target_119.TARGET,
                }:
                    for field in target_pipeline.RESULT_FIELDS:
                        row[field] = "not-run"
        preserved = copy.deepcopy(run_cluster.BASELINE_RESULTS)
        preserved.update(run_cluster.LATER_RESULTS)
        statuses = {
            target_025.TARGET: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
            },
            target_026.TARGET: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
            },
            target_119.TARGET: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
            },
        }
        for module in run_cluster.TARGET_MODULES:
            csv_rows, json_rows = target_pipeline.apply_crosswalk_result_update(
                csv_rows,
                json_rows,
                target=module.TARGET,
                input_order=module.INPUT_ORDER,
                statuses=statuses[module.TARGET],
                preserved_results=preserved,
            )
            preserved[(module.TARGET, module.INPUT_ORDER)] = statuses[
                module.TARGET
            ]
        classified = [
            row
            for row in csv_rows
            if any(
                row[field] != "not-run"
                for field in target_pipeline.RESULT_FIELDS
            )
        ]
        self.assertEqual(len(classified), 62)
        self.assertEqual(csv_rows, json_rows)

    def test_delivered_reset_supports_repeated_standalone_replay(self) -> None:
        delivered_csv = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        delivered_json = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        for rows in (delivered_csv, delivered_json):
            by_key = {
                (row["target"], row["input_order"]): row for row in rows
            }
            for key in run_cluster.CLUSTER_KEYS:
                by_key[key].update(run_cluster.DELIVERED_RESULTS[key])
        for _ in range(2):
            reset_csv, reset_json = run_cluster.prepare_crosswalk_reset(
                delivered_csv,
                delivered_json,
            )
            self.assertEqual(reset_csv, reset_json)
            before = {
                (row["target"], row["input_order"]): row
                for row in delivered_csv
            }
            after = {
                (row["target"], row["input_order"]): row
                for row in reset_csv
            }
            for key in before:
                changed = {
                    field
                    for field in before[key]
                    if before[key][field] != after[key][field]
                }
                if key in set(run_cluster.CLUSTER_KEYS):
                    self.assertEqual(
                        changed,
                        set(target_pipeline.RESULT_FIELDS),
                    )
                    self.assertEqual(
                        {
                            field: after[key][field]
                            for field in target_pipeline.RESULT_FIELDS
                        },
                        run_cluster.NOT_RUN,
                    )
                else:
                    self.assertFalse(changed)

            preserved = copy.deepcopy(run_cluster.BASELINE_RESULTS)
            preserved.update(run_cluster.LATER_RESULTS)
            for module in run_cluster.TARGET_MODULES:
                key = module.TARGET, module.INPUT_ORDER
                statuses = run_cluster.DELIVERED_RESULTS[key]
                reset_csv, reset_json = (
                    target_pipeline.apply_crosswalk_result_update(
                        reset_csv,
                        reset_json,
                        target=module.TARGET,
                        input_order=module.INPUT_ORDER,
                        statuses=statuses,
                        preserved_results=preserved,
                    )
                )
                preserved[key] = statuses
            self.assertEqual(reset_csv, delivered_csv)
            self.assertEqual(reset_json, delivered_json)
            delivered_csv, delivered_json = reset_csv, reset_json

    def test_reset_accepts_uniform_precluster_acceptance_state(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        for rows in (csv_rows, json_rows):
            by_key = {
                (row["target"], row["input_order"]): row for row in rows
            }
            for key in run_cluster.CLUSTER_KEYS:
                by_key[key].update(run_cluster.NOT_RUN)
        reset_csv, reset_json = run_cluster.prepare_crosswalk_reset(
            csv_rows,
            json_rows,
        )
        self.assertEqual(reset_csv, csv_rows)
        self.assertEqual(reset_json, json_rows)

    def test_delivered_reset_rejects_every_result_partition_mutation(self) -> None:
        original_csv = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        original_json = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        for rows in (original_csv, original_json):
            by_key = {
                (row["target"], row["input_order"]): row for row in rows
            }
            for key in run_cluster.CLUSTER_KEYS:
                by_key[key].update(run_cluster.DELIVERED_RESULTS[key])
        cases = (
            ("predecessor", next(iter(run_cluster.BASELINE_RESULTS))),
            ("cluster", run_cluster.CLUSTER_KEYS[0]),
            (
                "later",
                next(iter(run_cluster.LATER_RESULTS)),
            ),
        )
        for label, key in cases:
            csv_rows = copy.deepcopy(original_csv)
            json_rows = copy.deepcopy(original_json)
            for rows in (csv_rows, json_rows):
                row = next(
                    item
                    for item in rows
                    if (item["target"], item["input_order"]) == key
                )
                if label == "cluster":
                    row.update(run_cluster.NOT_RUN)
                else:
                    row["exact_output_determinism_status"] = (
                        "not-run"
                        if label == "predecessor"
                        else "solver-unknown"
                    )
            with self.subTest(partition=label), self.assertRaises(ValueError):
                run_cluster.prepare_crosswalk_reset(csv_rows, json_rows)


if __name__ == "__main__":
    unittest.main()
