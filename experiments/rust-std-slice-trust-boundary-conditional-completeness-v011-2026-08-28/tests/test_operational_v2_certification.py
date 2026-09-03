#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import operational_v2_certification as certification
import run_target_079_operational_v1 as target_079_runner


class OperationalV2CertificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = certification.build_certified_projection()
        cls.review_text = certification.REVIEW_PATH.read_text()
        cls.v2_crosswalk = certification._load_json(
            certification.v2.V2_CROSSWALK_JSON,
            "test operational-v2 crosswalk",
        )

    def test_certified_projection_reports_accepted_62_row_counts(self) -> None:
        self.assertEqual(self.payload["status"], "certified")
        self.assertEqual(self.payload["row_count"], 62)
        self.assertEqual(
            self.payload["classification_counts"],
            certification.EXPECTED_COUNTS,
        )
        self.assertEqual(
            self.payload["independent_review"]["verdict"], "ACCEPT"
        )
        self.assertEqual(
            self.payload["independent_review"]["status"], "accepted"
        )

    def test_all_effective_rows_are_projected_without_reclassification(
        self,
    ) -> None:
        self.assertEqual(
            self.payload["rows"],
            certification._row_projection(self.v2_crosswalk),
        )
        self.assertEqual(
            certification._projection_digest(self.payload["rows"]),
            certification.EXPECTED_ROW_PROJECTION_SHA256,
        )

    def test_crosswalk_manifest_dossiers_and_review_are_bound(self) -> None:
        package = self.payload["accepted_operational_v2"]
        self.assertEqual(
            package["crosswalk"]["json"],
            certification.EXPECTED_V2_ARTIFACTS["crosswalk_json"],
        )
        self.assertEqual(
            package["crosswalk"]["csv"],
            certification.EXPECTED_V2_ARTIFACTS["crosswalk_csv"],
        )
        self.assertEqual(
            package["reconciliation_manifest"],
            certification.EXPECTED_V2_ARTIFACTS[
                "reconciliation_manifest"
            ],
        )
        self.assertEqual(
            package["dossiers"]["json"],
            certification.EXPECTED_V2_ARTIFACTS["results_dossier_json"],
        )
        self.assertEqual(
            package["dossiers"]["markdown"],
            certification.EXPECTED_V2_ARTIFACTS[
                "results_dossier_markdown"
            ],
        )
        self.assertEqual(
            self.payload["independent_review"]["artifact"],
            certification.EXPECTED_REVIEW_ARTIFACT,
        )

    def test_certified_projection_contains_no_pending_status(self) -> None:
        self.assertFalse(certification._contains_pending(self.payload))

    def test_missing_review_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing-review.md"
            with mock.patch.object(
                certification, "REVIEW_PATH", missing
            ):
                with self.assertRaises(
                    certification.OperationalV2CertificationError
                ):
                    certification.build_certified_projection()

    def test_malformed_review_is_rejected(self) -> None:
        malformed = self.review_text.replace(
            "**Timestamp:** 2026-09-01T22:41:27Z\n", ""
        )
        with self.assertRaises(
            certification.OperationalV2CertificationError
        ):
            certification._parse_accept_review(malformed)

    def test_non_accept_review_is_rejected(self) -> None:
        rejected = self.review_text.replace(
            "**VERDICT: ACCEPT**", "**VERDICT: REJECT**"
        )
        with self.assertRaises(
            certification.OperationalV2CertificationError
        ):
            certification._parse_accept_review(rejected)

    def test_wrong_scope_review_is_rejected(self) -> None:
        wrong_scope = self.review_text.replace(
            "additive operational-v2 reconciliation",
            "additive all-module reconciliation",
            1,
        )
        with self.assertRaises(
            certification.OperationalV2CertificationError
        ):
            certification._parse_accept_review(wrong_scope)

    def test_count_inconsistent_review_is_rejected(self) -> None:
        inconsistent = self.review_text.replace(
            "The reconciliation\nreports 62 rows",
            "The reconciliation\nreports 61 rows",
        )
        with self.assertRaises(
            certification.OperationalV2CertificationError
        ):
            certification._parse_accept_review(inconsistent)

    def test_duplicate_or_conflicting_count_summaries_are_rejected(
        self,
    ) -> None:
        accepted_summary = (
            "The reconciliation reports 62 rows, overlays `78,79`, exact "
            "counts `50/12/0`, reviewed-equivalence counts `43/19/0`, and "
            "zero missing classifications."
        )
        conflicting_summary = (
            "The reconciliation reports 61 rows, overlays `78,79`, exact "
            "counts `49/12/0`, reviewed-equivalence counts `42/19/0`, and "
            "zero missing classifications."
        )
        for label, extra_summary in (
            ("duplicate", accepted_summary),
            ("conflicting", conflicting_summary),
        ):
            with self.subTest(label=label):
                with self.assertRaisesRegex(
                    certification.OperationalV2CertificationError,
                    "expected exactly one count-bearing acceptance summary",
                ):
                    certification._parse_accept_review(
                        f"{self.review_text}\n\n{extra_summary}\n"
                    )

    def test_v2_identity_drift_is_rejected(self) -> None:
        corrupted = copy.deepcopy(self.v2_crosswalk)
        corrupted["campaign_version"] = "operational-v3"
        with self.assertRaises(
            certification.OperationalV2CertificationError
        ):
            certification._validate_candidate_crosswalk(corrupted)

    def test_v2_row_drift_is_rejected(self) -> None:
        corrupted = copy.deepcopy(self.v2_crosswalk)
        corrupted["rows"].pop()
        with self.assertRaises(
            certification.OperationalV2CertificationError
        ):
            certification._validate_candidate_crosswalk(corrupted)

    def test_v2_count_drift_is_rejected(self) -> None:
        corrupted = copy.deepcopy(self.v2_crosswalk)
        corrupted["classification_counts"][
            "exact_output_determinism"
        ]["conditional-complete"] = 49
        with self.assertRaises(
            certification.OperationalV2CertificationError
        ):
            certification._validate_candidate_crosswalk(corrupted)

    def test_v2_artifact_drift_is_rejected(self) -> None:
        corrupted = copy.deepcopy(
            certification.EXPECTED_V2_ARTIFACTS["crosswalk_json"]
        )
        corrupted["sha256"] = "0" * 64
        with self.assertRaises(
            certification.OperationalV2CertificationError
        ):
            certification._validate_expected_artifact(
                certification.v2.V2_CROSSWALK_JSON,
                corrupted,
                "test crosswalk",
            )

    def test_pending_certified_projection_is_rejected(self) -> None:
        corrupted = copy.deepcopy(self.payload)
        corrupted["independent_review"]["status"] = "pending"
        with self.assertRaises(
            certification.OperationalV2CertificationError
        ):
            certification._validate_certified_payload(corrupted)

    def test_protected_file_mutation_is_rejected(self) -> None:
        groups = copy.deepcopy(
            self.payload["protected_inputs"]["groups"]
        )
        groups["manager_owned_state"][0]["sha256"] = "0" * 64
        with self.assertRaises(
            certification.OperationalV2CertificationError
        ):
            certification._validate_protected_groups(groups)

    def test_target_079_replay_uses_frozen_pre_v2_review_set(self) -> None:
        self.assertEqual(
            target_079_runner.protected_tree_digest(
                "campaign_reviews", ROOT / "review"
            ),
            target_079_runner.EXPECTED_CAMPAIGN_REVIEWS_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
