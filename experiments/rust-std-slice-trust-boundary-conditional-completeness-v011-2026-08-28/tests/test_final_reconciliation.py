#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import final_reconciliation as final
import target_029


class FinalReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        final.FINAL_ROOT.mkdir(parents=True, exist_ok=True)
        final.common.write_json(
            final.TARGET_029_BOUNDARY, target_029.boundary_manifest()
        )
        cls.payload = final.build_campaign()

    def test_scope_and_counts_are_recomputed(self) -> None:
        self.assertEqual(len(self.payload["rows"]), 62)
        self.assertEqual(
            Counter(
                row["classification"][final.EXACT_FIELD]
                for row in self.payload["rows"]
            ),
            final.EXPECTED_EXACT_COUNTS,
        )
        self.assertEqual(
            Counter(
                row["classification"][final.FULL_FIELD]
                for row in self.payload["rows"]
            ),
            final.EXPECTED_FULL_COUNTS,
        )

    def test_every_row_has_one_boundary_result_and_accepting_review(self) -> None:
        for row in self.payload["rows"]:
            with self.subTest(order=row["input_order"]):
                self.assertTrue(
                    row["conditional_obligation_boundary"][
                        "shared_observations"
                    ]
                )
                self.assertEqual(
                    row["accepting_incremental_review"]["verdict"], "ACCEPT"
                )
                self.assertTrue(row["verus_evidence"]["verification_captures"])
                self.assertTrue(row["result_manifest"]["sha256"])
                review_text = (
                    ROOT
                    / row["accepting_incremental_review"]["path"]
                ).read_text()
                self.assertIn(row["target"], review_text)

    def test_target_evidence_has_no_missing_or_orphan_directories(self) -> None:
        expected = {
            final.common.target_artifact_id(
                row["target"], int(row["input_order"])
            )
            for row in self.payload["rows"]
        }
        actual = {
            path.name
            for path in (ROOT / "evidence/targets").iterdir()
            if path.is_dir()
        }
        self.assertEqual(actual, expected)

    def test_operational_addenda_are_outside_preservation_baseline(
        self,
    ) -> None:
        for evidence in (
            final.TARGET_078_OPERATIONAL_EVIDENCE,
            final.TARGET_079_OPERATIONAL_EVIDENCE,
            final.TARGET_079_ADAPTER_REFINEMENT_V2_EVIDENCE,
            final.TARGET_078_ADAPTER_REFINEMENT_V2_EVIDENCE,
        ):
            self.assertTrue((evidence / "result.json").is_file())
        for path in (
            *final.TARGET_078_OPERATIONAL_ADDENDA,
            *final.TARGET_079_OPERATIONAL_ADDENDA,
        ):
            self.assertTrue(path.is_file())

        baseline = final._load_json(final.PRESERVATION_BASELINE)
        snapshot = final._snapshot_preserved_files()
        self.assertEqual(snapshot, baseline["groups"])

    def test_only_six_rows_weaken_equivalence(self) -> None:
        weakened = {
            row["input_order"]
            for row in self.payload["rows"]
            if row["equivalence"]["weakened"]
        }
        self.assertEqual(weakened, final.WEAK_EQUIVALENCE_ORDERS)
        for row in self.payload["rows"]:
            if row["input_order"] not in weakened:
                continue
            with self.subTest(order=row["input_order"]):
                self.assertTrue(row["equivalence"]["source_citation"])
                self.assertTrue(row["equivalence"]["positive_witness"])
                self.assertTrue(row["equivalence"]["negative_witness"])

    def test_missing_models_do_not_promote_bounded_unsat(self) -> None:
        rows = {
            row["input_order"]: row
            for row in self.payload["rows"]
            if row["input_order"] in final.MISSING_MODEL_ORDERS
        }
        self.assertEqual(set(rows), final.MISSING_MODEL_ORDERS)
        for row in rows.values():
            with self.subTest(order=row["input_order"]):
                exact = row["solver_evidence"]["exact_output"]
                full = row["solver_evidence"]["full_state"]
                self.assertFalse(exact["classification_evidence"])
                self.assertFalse(full["classification_evidence"])
                self.assertTrue(full["diagnostic_only"])
                self.assertEqual(
                    row["classification"][final.FULL_FIELD],
                    "missing-source-backed-model",
                )

    def test_complete_requires_direct_unsat(self) -> None:
        row = next(
            item
            for item in self.payload["rows"]
            if item["classification"][final.EXACT_FIELD]
            == "conditional-complete"
        )
        result = final._load_json(
            ROOT / row["result_manifest"]["path"]
        )
        obligation = final._obligation_entry(result, "exact")
        self.assertIsNotNone(obligation)
        assert obligation is not None
        _, evidence = obligation
        corrupted = copy.deepcopy(result)
        corrupted["obligations"][obligation[0]]["solver"][
            "solver_result"
        ] = "sat"
        with self.assertRaises(final.ReconciliationError):
            final._validate_direct_obligation(
                corrupted,
                projection="exact",
                classification="conditional-complete",
                missing_model=False,
            )
        self.assertEqual(evidence["solver"]["solver_result"], "unsat")

    def test_incomplete_requires_fixed_sat_witness(self) -> None:
        result = final._load_json(
            ROOT
            / "evidence/targets/029_core_slice_binary_search_by/result.json"
        )
        corrupted = {
            key: value
            for key, value in result.items()
            if "witness" not in key and "counterexample" not in key
        }
        with self.assertRaises(final.ReconciliationError):
            final._validate_incomplete_witness(corrupted, "exact")


if __name__ == "__main__":
    unittest.main()
