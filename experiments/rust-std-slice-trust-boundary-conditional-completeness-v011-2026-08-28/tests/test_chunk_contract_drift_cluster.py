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
import chunk_contract_drift_cluster as cluster
import replay_chunk_contract_drift
import run_chunk_contract_drift_cluster as runner


class ChunkContractDriftGuardTests(unittest.TestCase):
    def test_exact_active_contract_hashes_and_drift_are_bound(self) -> None:
        expected = {
            "12": "9d7c778009f44f0fd043dfc0e22215c99b3c90dde9ed5434c911087402bbe05f",
            "14": "a2a5116af11a32d4169f8b90ce1a319e948a4705e36b8a2c171f6a8191655b66",
            "15": "c7cdf29658c01698013e14c2ab14e93699f855167a15eb4e3d697742a7d40c9a",
            "23": "1b3b024fdbd8f22771d68cefc3082062544ac60b7d7ac07fda1c14cab04ab3ca",
            "24": "f7f4347b6b668b99b56a86daa936797fae5b45f6ffc22dbacc872c1be89b2dde",
        }
        self.assertEqual(
            {item.input_order: item.active_contract_sha256 for item in cluster.ORDERED_TARGETS},
            {order: expected[order] for order in ("14", "15", "12", "23", "24")},
        )
        for config in cluster.ORDERED_TARGETS:
            row = cluster.authority_row(config.input_order)
            with self.subTest(target=config.target):
                self.assertEqual(
                    common.sha256_text(row["active_contract_text"]),
                    expected[config.input_order],
                )
                self.assertNotEqual(
                    row["active_contract_text"], row["retained_contract_text"]
                )
                self.assertEqual(row["contract_drift"], "yes")

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for config in cluster.ORDERED_TARGETS:
            for purpose in cluster.PURPOSES:
                with self.subTest(target=config.target, purpose=purpose):
                    text, metadata = cluster.obligation(config, purpose)
                    validate_obligation(text, metadata)
                    cluster.validate_target_obligation(config, text, metadata)

    def test_retained_contract_substitution_is_rejected(self) -> None:
        for config in cluster.ORDERED_TARGETS:
            text, metadata = cluster.obligation(config, cluster.PRIMARY)
            row = cluster.authority_row(config.input_order)
            metadata = copy.deepcopy(metadata)
            metadata["active_contract_sha256"] = config.retained_contract_sha256
            metadata["active_contract_text"] = row["retained_contract_text"]
            with self.subTest(target=config.target):
                with self.assertRaises(GuardError):
                    cluster.validate_target_obligation(config, text, metadata)

    def test_omission_of_every_active_conjunct_is_rejected(self) -> None:
        for config in cluster.ORDERED_TARGETS:
            for purpose in cluster.PURPOSES:
                text, metadata = cluster.obligation(config, purpose)
                target_start = text.index("(define-fun TargetDefinition_T")
                target_end = text.index("(define-fun Spec_T", target_start)
                target_text = text[target_start:target_end]
                for symbol in cluster._active_conjunct_symbols(config):
                    if (
                        purpose == cluster.EXACT_OUTPUT
                        and symbol.startswith("ActiveFinal")
                    ):
                        self.assertIn(symbol, text)
                        continue
                    marker = f"({symbol} "
                    self.assertIn(marker, target_text)
                    mutated = (
                        text[:target_start]
                        + target_text.replace(marker, "(and ", 1)
                        + text[target_end:]
                    )
                    with self.subTest(
                        target=config.target,
                        purpose=purpose,
                        symbol=symbol,
                    ):
                        with self.assertRaises(GuardError):
                            cluster.validate_target_obligation(
                                config, mutated, metadata
                            )

    def test_lower_transition_composition_is_mandatory(self) -> None:
        for config in (
            cluster.TARGET_012,
            cluster.TARGET_023,
            cluster.TARGET_024,
        ):
            text, metadata = cluster.obligation(config, cluster.PRIMARY)
            symbol = (
                "LowerAsChunksUncheckedMutTransition"
                if config.mutable
                else "LowerAsChunksUncheckedTransition"
            )
            call = f"({symbol} x y"
            self.assertIn(call, text)
            with self.subTest(target=config.target):
                with self.assertRaises(GuardError):
                    cluster.validate_target_obligation(
                        config, text.replace(call, "(and", 1), metadata
                    )

    def test_target_015_answer_bearing_sites_are_replaced_not_reused(self) -> None:
        _, metadata = cluster.obligation(cluster.TARGET_015, cluster.PRIMARY)
        scope = metadata["boundary_scope"]
        excluded = set(scope["excluded_retained_trust_site_ids"])
        admitted = set(scope["admitted_trust_site_ids"])
        replacements = metadata["source_backed_replacements"]
        replaced = {
            site
            for replacement in replacements
            for site in replacement["replaces_trust_site_ids"]
        }
        self.assertTrue({"TS-015-D006", "TS-015-E002"} <= excluded)
        self.assertTrue({"TS-015-D006", "TS-015-E002"} <= replaced)
        self.assertFalse({"TS-015-D006", "TS-015-E002"} & admitted)
        symbols = {
            symbol
            for replacement in replacements
            for symbol in replacement["symbols"]
        }
        self.assertTrue(
            {
                "PointerCastProjection",
                "ArrayPointerCastProjection",
                "RawSliceConstructionProjection",
                "SharedStorageAliasProjection",
                "LowerAsChunksUncheckedMutTransition",
            }
            <= symbols
        )

    def test_boundaries_contain_only_initial_observations(self) -> None:
        forbidden = (
            "output",
            "return",
            "result",
            "range",
            "chunks",
            "remainder",
            "final",
            "answer",
            "trace",
        )
        for config in cluster.ORDERED_TARGETS:
            _, metadata = cluster.obligation(config, cluster.PRIMARY)
            for field in metadata["boundary_fields"]:
                with self.subTest(target=config.target, field=field["selector"]):
                    self.assertFalse(
                        any(token in field["selector"] for token in forbidden)
                    )

    def test_output_and_final_state_laundering_are_rejected(self) -> None:
        config = cluster.TARGET_015
        text, metadata = cluster.obligation(config, cluster.PRIMARY)
        text = text.replace(
            "      (b_frame_token Int)))))",
            "      (b_frame_token Int)\n"
            "      (b_selected_output Int)\n"
            "      (b_final_storage Int)))))",
        ).replace(
            "(define-fun Boundary_T ((x Input) (b Boundary)) Bool\n"
            "  (and (InputMemoryLayoutObserved x b)",
            "(define-fun Boundary_T ((x Input) (b Boundary)) Bool\n"
            "  (and (= (b_selected_output b) (x_length x))\n"
            "       (= (b_final_storage b) (x_sequence x))\n"
            "       (InputMemoryLayoutObserved x b)",
        ).replace(
            "(and (InputMemoryLayoutObserved x b)\n"
            "       (PointerCastProjection x y)",
            "(and (InputMemoryLayoutObserved x b)\n"
            "       (= (y_chunks_len y) (b_selected_output b))\n"
            "       (= (s_final_sequence s) (b_final_storage b))\n"
            "       (PointerCastProjection x y)",
            1,
        )
        metadata = copy.deepcopy(metadata)
        metadata["boundary_fields"].extend(
            (
                {
                    "selector": "b_selected_output",
                    "role": "source_helper_observation",
                    "source_citations": ["core/src/slice/mod.rs:1498-1509"],
                    "trust_site_ids": ["TS-015-D003"],
                    "source_backed_replacement_ids": [],
                },
                {
                    "selector": "b_final_storage",
                    "role": "source_helper_observation",
                    "source_citations": ["core/src/slice/raw.rs:143-196"],
                    "trust_site_ids": ["TS-015-D003"],
                    "source_backed_replacement_ids": [],
                },
            )
        )
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_opaque_whole_target_helper_is_rejected(self) -> None:
        config = cluster.TARGET_014
        text, metadata = cluster.obligation(config, cluster.PRIMARY)
        text = text.replace(
            "(declare-const x Input)",
            "(declare-fun WholeTarget (Input Boundary) Output)\n"
            "(declare-const x Input)",
        )
        metadata = copy.deepcopy(metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "WholeTarget",
                "role": "source_transition",
                "source_citations": ["core/src/slice/mod.rs:1338-1349"],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_all_domain_and_transition_probes_have_expected_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        required = {
            "valid_nonempty",
            "valid_empty",
            "valid_zst",
            "invalid_n_zero",
            "invalid_null_pointer",
            "invalid_misaligned_pointer",
            "invalid_isize_overflow",
            "invalid_uninitialized_storage",
            "invalid_multiple_allocation_span",
            "changed_output_provenance",
            "invalid_lower_divisibility",
        }
        for config in cluster.ORDERED_TARGETS:
            cases = cluster.probe_cases(config)
            self.assertTrue(required <= set(cases))
            if config.has_remainder:
                self.assertIn("swapped_front_rear", cases)
            if config.mutable:
                self.assertIn("invalid_nonwritable_storage", cases)
                self.assertIn("invalid_alias_exclusivity", cases)
            for name, case in cases.items():
                with self.subTest(target=config.target, probe=name):
                    process = subprocess.run(
                        [str(z3), "-in", "-smt2"],
                        input=cluster.probe_text(config, name),
                        text=True,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(
                        process.stdout.splitlines()[0], case["expected"]
                    )
                    self.assertEqual(process.stderr, "")

    def test_theorem_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for config in cluster.ORDERED_TARGETS:
            for purpose in cluster.PURPOSES:
                text, metadata = cluster.obligation(config, purpose)
                with self.subTest(target=config.target, purpose=purpose):
                    process = subprocess.run(
                        [str(z3), "-in", "-smt2"],
                        input=text,
                        text=True,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(
                        process.stdout,
                        metadata["expected_solver_result"] + "\n",
                    )
                    self.assertEqual(process.stderr, "")

    def test_verus_models_have_no_external_body(self) -> None:
        for config in cluster.ORDERED_TARGETS:
            path = ROOT / "proofs" / f"{config.artifact_id}.rs"
            with self.subTest(model=path.name):
                self.assertTrue(path.is_file())
                self.assertNotIn("external_body", path.read_text())

    def test_out_of_scope_result_mutation_is_rejected(self) -> None:
        rows = common.read_csv(ROOT / "crosswalk/target_to_proof_boundary.csv")
        for row in rows:
            key = (row["target"], row["input_order"])
            if key in runner.BASELINE_RESULTS:
                row.update(runner.BASELINE_RESULTS[key])
            elif key in set(runner.CLUSTER_KEYS):
                config = next(
                    item
                    for item in cluster.ORDERED_TARGETS
                    if (item.target, item.input_order) == key
                )
                row.update(config.expected_results)
            else:
                row.update(runner.NOT_RUN)
        json_rows = copy.deepcopy(rows)
        other = next(
            row
            for row in rows
            if (row["target"], row["input_order"])
            not in set(runner.BASELINE_RESULTS) | set(runner.CLUSTER_KEYS)
        )
        other["exact_output_determinism_status"] = "solver-unknown"
        with self.assertRaises(ValueError):
            runner.prepare_crosswalk_reset(rows, json_rows)


class ChunkContractDriftReplayTests(unittest.TestCase):
    def test_mutable_fixed_witnesses_replay_every_active_conjunct(self) -> None:
        for config in (cluster.TARGET_015, cluster.TARGET_024):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "witness.json"
                path.write_text(
                    json.dumps(cluster.witness_payload(config), sort_keys=True)
                    + "\n"
                )
                result = replay_chunk_contract_drift.replay(path)
            with self.subTest(target=config.target):
                self.assertEqual(result["status"], "passed")
                expected = set(cluster._active_conjunct_symbols(config))
                for checks in result["active_conjuncts"].values():
                    self.assertEqual(set(checks), expected)
                    self.assertTrue(all(checks.values()))
                self.assertTrue(result["observed"]["exact_output_equal"])
                self.assertFalse(
                    result["observed"]["full_exact_equivalent"]
                )

    def test_fixed_smt_countermodels_are_sat(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for config in (cluster.TARGET_015, cluster.TARGET_024):
            with self.subTest(target=config.target):
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=cluster.fixed_model_text(config),
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertTrue(process.stdout.startswith("sat\n"))
                self.assertEqual(process.stderr, "")


if __name__ == "__main__":
    unittest.main()
