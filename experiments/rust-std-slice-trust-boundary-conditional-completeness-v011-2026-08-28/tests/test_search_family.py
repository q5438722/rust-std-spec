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
import replay_target_028
import replay_target_030
import replay_target_065
import run_search_family_cluster
import search_family
import search_target_pipeline
import target_028
import target_030
import target_065
import target_pipeline


TARGETS = (
    (target_028, replay_target_028),
    (target_030, replay_target_030),
    (target_065, replay_target_065),
)


def delivered_crosswalk_rows() -> tuple[list[dict], list[dict]]:
    csv_rows = common.read_csv(
        ROOT / "crosswalk/target_to_proof_boundary.csv"
    )
    json_rows = copy.deepcopy(csv_rows)
    cluster_keys = set(run_search_family_cluster.CLUSTER_KEYS)
    for rows in (csv_rows, json_rows):
        for row in rows:
            key = (row["target"], row["input_order"])
            if key in search_target_pipeline.BASELINE_RESULTS:
                row.update(search_target_pipeline.BASELINE_RESULTS[key])
            elif key in cluster_keys:
                row.update(search_target_pipeline.INCOMPLETE)
            else:
                row.update(run_search_family_cluster.NOT_RUN)
    return csv_rows, json_rows


class SearchFamilyGuardTests(unittest.TestCase):
    def test_contract_hashes_are_exact(self) -> None:
        self.assertEqual(
            target_028.ACTIVE_CONTRACT_SHA256,
            "27d8e9d741e10e00091ad567844c0aca7d8bd48425cd705dfcf7173e0c973975",
        )
        self.assertEqual(
            target_030.ACTIVE_CONTRACT_SHA256,
            "613ffeb61ff37d877cf411db0ed8f76bcb2a93646330438d2a55cfb46e1a5ce5",
        )
        self.assertEqual(
            target_065.ACTIVE_CONTRACT_SHA256,
            "f28650f03f1c7e571f308b88c4dea8453057ce7b4b33946af0745ae5517fd695",
        )

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for module, _ in TARGETS:
            for purpose in module.PURPOSES:
                with self.subTest(target=module.TARGET, purpose=purpose):
                    text, metadata = module.obligation(purpose)
                    validate_obligation(text, metadata)
                    module.validate_target_obligation(text, metadata)

    def test_replaced_sites_are_excluded_not_relabeled(self) -> None:
        for module, _ in TARGETS:
            metadata = module.obligation(module.PRIMARY)[1]
            scope = metadata["boundary_scope"]
            replacements = metadata["source_backed_replacements"]
            with self.subTest(target=module.TARGET):
                self.assertEqual(
                    set(scope["excluded_retained_trust_site_ids"]),
                    set(module.EXCLUDED_RETAINED_TRUST_SITES),
                )
                self.assertEqual(len(replacements), 1)
                self.assertEqual(
                    set(replacements[0]["replaces_trust_site_ids"]),
                    set(module.EXCLUDED_RETAINED_TRUST_SITES),
                )
                admitted = set(scope["admitted_trust_site_ids"])
                excluded = set(scope["excluded_retained_trust_site_ids"])
                self.assertFalse(admitted & excluded)
                for field in metadata["boundary_fields"]:
                    self.assertTrue(set(field["trust_site_ids"]) <= admitted)
                    self.assertFalse(
                        set(field["trust_site_ids"]) & excluded
                    )

    def test_boundary_has_no_answer_or_trace_field(self) -> None:
        forbidden = ("answer", "selected", "result", "final", "trace")
        for module, _ in TARGETS:
            metadata = module.obligation(module.PRIMARY)[1]
            selectors = [item["selector"] for item in metadata["boundary_fields"]]
            with self.subTest(target=module.TARGET):
                for selector in selectors:
                    self.assertFalse(
                        any(token in selector for token in forbidden),
                        selector,
                    )

    def test_answer_bearing_delegation_is_rejected(self) -> None:
        text, metadata = target_028.obligation(target_028.PRIMARY)
        text = text.replace(
            "(declare-const x Input)",
            "(declare-fun OpaqueDelegate (Input Boundary) Output)\n"
            "(declare-const x Input)",
        )
        metadata = copy.deepcopy(metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "OpaqueDelegate",
                "role": "source_transition",
                "source_citations": ["core/src/slice/mod.rs:2922-2924"],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_opaque_result_bridge_is_rejected(self) -> None:
        text, metadata = target_030.obligation(target_030.PRIMARY)
        text = text.replace(
            "(declare-const x Input)",
            "(declare-fun OpaqueResultBridge (Output) Bool)\n"
            "(declare-const x Input)",
        ).replace(
            "(GeneratedBinarySearchByKeyResult x b y)",
            "(OpaqueResultBridge y)",
            1,
        )
        metadata = copy.deepcopy(metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "OpaqueResultBridge",
                "role": "source_transition",
                "source_citations": ["core/src/slice/mod.rs:3071-3077"],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_callback_state_loss_is_rejected(self) -> None:
        for module, equality in (
            (
                target_028,
                "(= (s_callback_state s) (CallbackStateAfterTwo x b))",
            ),
            (
                target_030,
                "(= (s_callback_state s) (CallbackStateAfterTwo x b))",
            ),
            (
                target_065,
                "(= (s_callback_state s) (CallbackStateAfterTwo x b))",
            ),
        ):
            text, metadata = module.obligation(module.PRIMARY)
            self.assertIn(equality, text)
            with self.subTest(target=module.TARGET):
                with self.assertRaises(GuardError):
                    module.validate_target_obligation(
                        text.replace(equality, "true", 1), metadata
                    )

    def test_ordering_or_partitioning_loss_is_rejected(self) -> None:
        mutations = (
            (
                target_028,
                "(=>\n         (SliceSortedByOrd x b)",
                "(=>\n         false",
            ),
            (
                target_030,
                "(=>\n         (ExtractedKeysOrdered b)",
                "(=>\n         false",
            ),
            (
                target_065,
                "(=> (PredicateProfilePartitioned b)",
                "(=> false",
            ),
        )
        for module, original, replacement in mutations:
            text, metadata = module.obligation(module.PRIMARY)
            self.assertIn(original, text)
            with self.subTest(target=module.TARGET):
                with self.assertRaises(GuardError):
                    module.validate_target_obligation(
                        text.replace(original, replacement, 1), metadata
                    )

    def test_upper_unsorted_lower_ordered_profiles_fail_closed(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        probes = (
            (
                target_028,
                """\
(assert (= x (mkInput 2 2 1 3 0)))
(assert (= b (mkBoundary 2 1 Less Less DZero DZero)))
(assert (= y1 (mkOutput true 0)))
(assert (= s1 (mkState 0)))
(assert (not (SliceSortedByOrd x b)))
(assert (ComparatorProfileOrdered b))
(assert (SourceBackedBinarySearchWrapper x b y1 s1))
(assert (not (ReviewedBinarySearchByLowerResult x b y1)))
(check-sat)
""",
            ),
            (
                target_030,
                """\
(assert (= x (mkInput 2 100 200 KLow 0)))
(assert
  (= b (mkBoundary 100 200 KHigh KMid Greater Greater DZero DZero)))
(assert (= y1 (mkOutput true 0)))
(assert (= s1 (mkState 0)))
(assert (not (ExtractedKeysOrdered b)))
(assert (ComparatorProfileOrdered b))
(assert (SourceBackedBinarySearchByKeyWrapper x b y1 s1))
(assert (not (ReviewedBinarySearchByLowerResult x b y1)))
(check-sat)
""",
            ),
        )
        for module, probe in probes:
            with self.subTest(target=module.TARGET):
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=search_family.model_text(
                        module.CONFIG, module.PRIMARY
                    )
                    + probe,
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, "unsat\n")
                self.assertEqual(process.stderr, "")

    def test_sortedness_and_partitioning_strengthening_is_rejected(self) -> None:
        text, metadata = target_028.obligation(target_028.PRIMARY)
        strengthened = text.replace(
            "(define-fun Requires_T ((x Input)) Bool\n  (LengthTwo x))",
            "(define-fun Requires_T ((x Input)) Bool\n"
            "  (and (LengthTwo x)\n"
            "       (<= (x_element0 x) (x_element1 x))))",
        )
        with self.assertRaises(GuardError):
            target_028.validate_target_obligation(strengthened, metadata)

        text, metadata = target_065.obligation(target_065.PRIMARY)
        strengthened = text.replace(
            "       (DeltaObservation (b_state_delta1 b))))",
            "       (DeltaObservation (b_state_delta1 b))\n"
            "       (PredicateProfilePartitioned b)))",
            1,
        )
        with self.assertRaises(GuardError):
            target_065.validate_target_obligation(strengthened, metadata)

    def test_output_laundering_is_rejected(self) -> None:
        text, metadata = target_065.obligation(target_065.PRIMARY)
        text = text.replace(
            "      (b_state_delta1 Delta)))))",
            "      (b_state_delta1 Delta)\n"
            "      (b_selected_index Int)))))",
        ).replace(
            "       (DeltaObservation (b_state_delta1 b))))",
            "       (DeltaObservation (b_state_delta1 b))\n"
            "       (>= (b_selected_index b) 0)))",
            1,
        ).replace(
            "       (GeneratedPartitionPointResult x b y)",
            "       (GeneratedPartitionPointResult x b y)\n"
            "       (= (y_index y) (b_selected_index b))",
            1,
        )
        metadata = copy.deepcopy(metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_selected_index",
                "role": "callback_result",
                "source_citations": ["core/src/slice/mod.rs:4854-4859"],
                "trust_site_ids": ["TS-065-D003"],
                "source_backed_replacement_ids": [],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_expected_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for module, _ in TARGETS:
            for purpose in module.PURPOSES:
                with self.subTest(target=module.TARGET, purpose=purpose):
                    text, metadata = module.obligation(purpose)
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

    def test_out_of_scope_row_mutation_is_rejected(self) -> None:
        csv_rows, json_rows = delivered_crosswalk_rows()
        other = next(
            row
            for row in csv_rows
            if (row["target"], row["input_order"])
            not in (
                set(search_target_pipeline.BASELINE_RESULTS)
                | set(run_search_family_cluster.CLUSTER_KEYS)
            )
        )
        other["exact_output_determinism_status"] = "conditional-complete"
        with self.assertRaises(ValueError):
            run_search_family_cluster.prepare_crosswalk_reset(
                csv_rows, json_rows
            )

    def test_verus_models_contain_no_external_body(self) -> None:
        for path in (
            ROOT / "proofs/028_core_slice_binary_search.rs",
            ROOT / "proofs/030_core_slice_binary_search_by_key.rs",
            ROOT / "proofs/065_core_slice_partition_point.rs",
        ):
            with self.subTest(model=path.name):
                self.assertNotIn("external_body", path.read_text())


class SearchFamilyReplayTests(unittest.TestCase):
    def test_fixed_witnesses_and_sanity_domains_replay(self) -> None:
        for module, replay in TARGETS:
            with self.subTest(target=module.TARGET):
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "witness.json"
                    path.write_text(
                        json.dumps(module.witness_payload(), sort_keys=True)
                        + "\n"
                    )
                    result = replay.replay(path)
                self.assertEqual(result["status"], "passed")
                self.assertTrue(
                    result[module.SANITY.replace("-", "_")][
                        "all_pairs_exactly_equal"
                        if module.CONFIG.kind == "partition"
                        else "all_pairs_equivalent"
                    ]
                )


class SearchFamilyCrosswalkTests(unittest.TestCase):
    def test_only_cluster_result_cells_are_reset(self) -> None:
        csv_rows, json_rows = delivered_crosswalk_rows()
        reset_csv, reset_json = (
            run_search_family_cluster.prepare_crosswalk_reset(
                csv_rows, json_rows
            )
        )
        self.assertEqual(reset_csv, reset_json)
        before = {
            (row["target"], row["input_order"]): row for row in csv_rows
        }
        after = {
            (row["target"], row["input_order"]): row for row in reset_csv
        }
        for key in before:
            changed = {
                field
                for field in before[key]
                if before[key][field] != after[key][field]
            }
            if key in set(run_search_family_cluster.CLUSTER_KEYS):
                self.assertEqual(
                    changed,
                    set(search_target_pipeline.INCOMPLETE),
                )
            else:
                self.assertFalse(changed)

    def test_single_target_update_rejects_out_of_scope_mutation(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = copy.deepcopy(csv_rows)
        for row in csv_rows:
            key = (row["target"], row["input_order"])
            if key in search_target_pipeline.BASELINE_RESULTS:
                row.update(search_target_pipeline.BASELINE_RESULTS[key])
            else:
                row.update(run_search_family_cluster.NOT_RUN)
        json_rows = copy.deepcopy(csv_rows)
        other = next(
            row
            for row in csv_rows
            if (row["target"], row["input_order"])
            not in search_target_pipeline.BASELINE_RESULTS
            and row["target"] != target_028.TARGET
        )
        other["completeness_modulo_reviewed_equivalence_status"] = (
            "conditional-complete"
        )
        with self.assertRaises(ValueError):
            target_pipeline.apply_crosswalk_result_update(
                csv_rows,
                json_rows,
                target=target_028.TARGET,
                input_order=target_028.INPUT_ORDER,
                statuses=search_target_pipeline.INCOMPLETE,
                preserved_results=search_target_pipeline.BASELINE_RESULTS,
            )


if __name__ == "__main__":
    unittest.main()
