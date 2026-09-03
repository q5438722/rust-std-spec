#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import operational_v2_reconciliation as v2
import preservation_policy_v3 as preservation_policy
import preservation_policy_v8 as preservation_policy_v8


class OperationalV2ReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = v2.build_crosswalk()
        cls.baseline = v2._load_json(v2.BASELINE_CROSSWALK_JSON)
        cls.baseline_by_order = v2._validate_baseline_scope(cls.baseline)

    def test_scope_and_effective_counts(self) -> None:
        self.assertEqual(len(self.payload["rows"]), 62)
        self.assertEqual(self.payload["overlay_orders"], ["78", "79"])
        self.assertEqual(
            self.payload["classification_counts"][
                "exact_output_determinism"
            ],
            v2.EXPECTED_V2_EXACT,
        )
        self.assertEqual(
            self.payload["classification_counts"][
                "completeness_modulo_reviewed_equivalence"
            ],
            v2.EXPECTED_V2_FULL,
        )
        self.assertEqual(
            self.payload["missing_source_backed_model_orders"], []
        )

    def test_certified_rows_are_embedded_without_mutation(self) -> None:
        baseline = {
            row["input_order"]: row for row in self.baseline["rows"]
        }
        for row in self.payload["rows"]:
            with self.subTest(order=row["input_order"]):
                self.assertEqual(
                    row["campaign_row"], baseline[row["input_order"]]
                )
                if row["input_order"] in v2.OVERLAY_SPECS:
                    self.assertNotEqual(
                        row["effective_classification"],
                        row["campaign_row"]["classification"],
                    )
                else:
                    self.assertEqual(
                        row["effective_classification"],
                        row["campaign_row"]["classification"],
                    )

    def test_only_accepted_overlays_supply_direct_evidence(self) -> None:
        overlaid = {
            row["input_order"]: row
            for row in self.payload["rows"]
            if row["classification_source"]["kind"]
            == "accepted-operational-v1-overlay"
        }
        self.assertEqual(set(overlaid), {"78", "79"})
        for order, row in overlaid.items():
            with self.subTest(order=order):
                source = row["classification_source"]
                self.assertEqual(
                    source["direct_evidence"]["exact_output"]["solver"][
                        "solver_result"
                    ],
                    "unsat",
                )
                self.assertEqual(
                    source["direct_evidence"]["reviewed_equivalence"][
                        "solver"
                    ]["solver_result"],
                    "unsat",
                )
                self.assertEqual(
                    source["direct_evidence"]["nonvacuity"]["solver"][
                        "solver_result"
                    ],
                    "sat",
                )
                self.assertIn(
                    "verified, 0 errors",
                    source["verus"]["expected_summary"],
                )

    def test_scope_drift_is_rejected(self) -> None:
        corrupted = copy.deepcopy(self.baseline)
        corrupted["rows"].pop()
        with self.assertRaises(v2.OperationalV2Error):
            v2._validate_baseline_scope(corrupted)

    def test_duplicate_overlay_is_rejected(self) -> None:
        path = v2.OVERLAY_SPECS["78"]["json"]
        with self.assertRaises(v2.OperationalV2Error):
            v2._load_overlays(
                self.baseline_by_order, paths=[path, path]
            )

    def test_registered_addenda_are_not_selected_as_overlays(
        self,
    ) -> None:
        lifecycles = (
            preservation_policy.target_080_lifecycle(),
            preservation_policy.target_081_lifecycle(),
            preservation_policy_v8.target_082_lifecycle(),
        )
        selected = set(v2._discover_overlay_paths())
        self.assertEqual(
            selected,
            {
                spec["json"].resolve()
                for spec in v2.OVERLAY_SPECS.values()
            },
        )
        for lifecycle in lifecycles:
            with self.subTest(policy=lifecycle["status"]):
                self.assertNotIn(
                    (
                        ROOT
                        / lifecycle["registered_addenda"]["json"]["path"]
                    ).resolve(),
                    selected,
                )
                self.assertFalse(
                    lifecycle["selected_as_operational_v2_overlay"]
                )

    def test_unregistered_discovered_overlay_is_rejected(self) -> None:
        original_glob = Path.glob

        def glob_with_unregistered(
            path: Path, pattern: str, *args, **kwargs
        ):
            yield from original_glob(path, pattern, *args, **kwargs)
            if path == ROOT / "crosswalk" and pattern.endswith(
                (".json", ".csv")
            ):
                suffix = "json" if pattern.endswith(".json") else "csv"
                yield path / (
                    f"target_083_operational_v1_addendum.{suffix}"
                )

        with mock.patch.object(Path, "glob", glob_with_unregistered):
            with self.assertRaisesRegex(
                v2.OperationalV2Error,
                "missing or unsupported addenda",
            ):
                v2._discover_overlay_paths()

    def test_missing_registered_target_080_addendum_is_rejected(
        self,
    ) -> None:
        original_glob = Path.glob

        def glob_without_target_080(
            path: Path, pattern: str, *args, **kwargs
        ):
            yield from (
                item
                for item in original_glob(
                    path, pattern, *args, **kwargs
                )
                if (
                    path != ROOT / "crosswalk"
                    or "target_080_operational_v1_addendum"
                    not in item.name
                )
            )

        with mock.patch.object(Path, "glob", glob_without_target_080):
            with self.assertRaisesRegex(
                v2.OperationalV2Error,
                "missing or unsupported addenda",
            ):
                v2._discover_overlay_paths()

    def test_missing_registered_target_081_addendum_is_rejected(
        self,
    ) -> None:
        original_glob = Path.glob

        def glob_without_target_081(
            path: Path, pattern: str, *args, **kwargs
        ):
            yield from (
                item
                for item in original_glob(
                    path, pattern, *args, **kwargs
                )
                if (
                    path != ROOT / "crosswalk"
                    or "target_081_operational_v1_addendum"
                    not in item.name
                )
            )

        with mock.patch.object(Path, "glob", glob_without_target_081):
            with self.assertRaisesRegex(
                v2.OperationalV2Error,
                "missing or unsupported addenda",
            ):
                v2._discover_overlay_paths()

    def test_unsupported_overlay_order_is_rejected(self) -> None:
        addendum = v2._load_json(v2.OVERLAY_SPECS["78"]["json"])
        csv_row = v2._read_single_csv(
            v2.OVERLAY_SPECS["78"]["csv"], "test overlay"
        )
        addendum["input_order"] = "80"
        with self.assertRaises(v2.OperationalV2Error):
            v2._validate_addendum_identity(
                addendum, csv_row, self.baseline_by_order["78"], "78"
            )

    def test_target_and_contract_mismatch_are_rejected(self) -> None:
        addendum = v2._load_json(v2.OVERLAY_SPECS["79"]["json"])
        csv_row = v2._read_single_csv(
            v2.OVERLAY_SPECS["79"]["csv"], "test overlay"
        )
        for field, value in (
            ("target", "core::slice::select_nth_unstable"),
            ("active_contract_sha256", "0" * 64),
        ):
            with self.subTest(field=field):
                corrupted = copy.deepcopy(addendum)
                corrupted[field] = value
                with self.assertRaises(v2.OperationalV2Error):
                    v2._validate_addendum_identity(
                        corrupted,
                        csv_row,
                        self.baseline_by_order["79"],
                        "79",
                    )

    def test_non_accept_review_is_rejected(self) -> None:
        with self.assertRaises(v2.OperationalV2Error):
            v2._require_accept_review(
                "**VERDICT: REJECT**\n",
                v2.OVERLAY_SPECS["78"]["target"],
                "test review",
            )

    def test_missing_direct_unsat_is_rejected(self) -> None:
        order = "78"
        addendum = v2._load_json(v2.OVERLAY_SPECS[order]["json"])
        result = v2._load_json(
            ROOT / addendum["evidence_root"] / "result.json"
        )
        obligation = next(
            value
            for key, value in result["obligations"].items()
            if key.startswith("exact-")
        )
        obligation["solver"]["solver_result"] = "sat"
        identity = {
            "input_order": order,
            "target": addendum["target"],
            "active_contract_sha256": addendum[
                "active_contract_sha256"
            ],
            "model_id": addendum["model_id"],
        }
        with self.assertRaises(v2.OperationalV2Error):
            v2._validate_obligation(result, "exact", identity)

    def test_absent_sat_nonvacuity_is_rejected(self) -> None:
        order = "79"
        addendum = v2._load_json(v2.OVERLAY_SPECS[order]["json"])
        result = v2._load_json(
            ROOT / addendum["evidence_root"] / "result.json"
        )
        result["nonvacuity"]["solver"]["solver_result"] = "unknown"
        with self.assertRaises(v2.OperationalV2Error):
            v2._validate_nonvacuity(result, order)

    def test_stale_counts_are_rejected(self) -> None:
        corrupted = copy.deepcopy(self.payload)
        corrupted["classification_counts"][
            "exact_output_determinism"
        ]["conditional-complete"] = 49
        with self.assertRaises(v2.OperationalV2Error):
            v2._validate_effective_payload(corrupted)

    def test_preserved_artifact_mutation_is_rejected(self) -> None:
        groups = v2._snapshot_preserved_files()
        corrupted = copy.deepcopy(groups)
        corrupted["manager_owned_state"][0]["sha256"] = "0" * 64
        with self.assertRaises(v2.OperationalV2Error):
            v2._validate_preservation_groups(corrupted)

    def test_certified_preservation_snapshot_still_matches(self) -> None:
        baseline = v2._load_json(v2.BASELINE_PRESERVATION)
        self.assertEqual(
            v2.certified._snapshot_preserved_files(), baseline["groups"]
        )

    def test_prior_reviews_come_from_exact_historical_inventory(self) -> None:
        manifest = v2._load_json(v2.V2_MANIFEST)
        expected = manifest["preservation"]["groups"]["prior_reviews"]
        self.assertEqual(
            preservation_policy.review_inventory()["historical"],
            expected,
        )

    def test_snapshot_uses_frozen_historical_review_inventory(self) -> None:
        self.assertEqual(
            v2._snapshot_preserved_files()["prior_reviews"],
            preservation_policy.review_inventory()["historical"],
        )

    def test_legacy_certification_reads_frozen_request_at_logical_path(
        self,
    ) -> None:
        path = v2._relative_file(
            v2.HISTORICAL_REVIEW_REQUEST,
            "certification protection prior_reviews[44]",
        )
        self.assertEqual(
            v2.common.relpath(path), v2.HISTORICAL_REVIEW_REQUEST
        )
        self.assertEqual(
            path.read_bytes(),
            v2.HISTORICAL_REVIEW_REQUEST_ARCHIVE.read_bytes(),
        )
        self.assertNotEqual(
            path.read_bytes(),
            (ROOT / v2.HISTORICAL_REVIEW_REQUEST).read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
