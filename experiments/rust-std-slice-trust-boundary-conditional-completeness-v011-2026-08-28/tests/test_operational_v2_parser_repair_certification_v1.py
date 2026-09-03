#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import operational_v2_parser_repair_certification_v1 as repair


class OperationalV2ParserRepairCertificationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = repair.build_certification()
        cls.canonical = repair.certification.REVIEW_PATH.read_text(
            encoding="utf-8"
        )

    def test_reports_certified_62_row_counts(self) -> None:
        self.assertEqual(self.payload["status"], "certified")
        self.assertEqual(self.payload["row_count"], 62)
        self.assertEqual(
            self.payload["classification_counts"],
            repair.EXPECTED_COUNTS,
        )

    def test_accepts_one_canonical_summary(self) -> None:
        parsed = repair._validate_repaired_review_text(self.canonical)
        self.assertEqual(parsed, repair.EXPECTED_PARSED_REVIEW)
        self.assertEqual(
            self.payload["semantic_validation"]["canonical_summary"][
                "count"
            ],
            1,
        )

    def test_rejects_missing_review_evidence(self) -> None:
        self._assert_review_rejected("missing")

    def test_rejects_duplicate_review_summary(self) -> None:
        self._assert_review_rejected("duplicate")

    def test_rejects_conflicting_review_summary(self) -> None:
        self._assert_review_rejected("conflicting")

    def test_rejects_wrong_scope_review(self) -> None:
        self._assert_review_rejected("wrong-scope")

    def test_rejects_wrong_count_review(self) -> None:
        self._assert_review_rejected("wrong-count")

    def test_rejects_stale_review(self) -> None:
        self._assert_review_rejected("stale")

    def test_rejects_non_accept_review(self) -> None:
        self._assert_review_rejected("non-ACCEPT")

    def _assert_review_rejected(self, label: str) -> None:
        candidate = repair.review_negative_candidates(self.canonical)[label]
        with self.assertRaises(repair.ParserRepairCertificationError):
            repair._validate_repaired_review_text(candidate)

    def test_binds_repair_implementation_and_regressions(self) -> None:
        self.assertEqual(
            self.payload["parser_repair"]["implementation"],
            repair.EXPECTED_REPAIR_IMPLEMENTATION,
        )
        self.assertEqual(
            self.payload["parser_repair"]["regression_tests"],
            repair.EXPECTED_REGRESSION_TESTS,
        )

    def test_binds_unchanged_existing_certification(self) -> None:
        existing = self.payload["existing_certified_projection"]
        self.assertEqual(existing["artifacts"], repair.EXPECTED_EXISTING_CERTIFICATION)
        self.assertEqual(existing["row_count"], 62)
        self.assertEqual(
            existing["classification_counts"], repair.EXPECTED_COUNTS
        )

    def test_binds_707_protected_paths(self) -> None:
        self.assertEqual(
            self.payload["preservation"]["protected_file_count"], 707
        )
        self.assertEqual(
            self.payload["preservation"]["protected_inventory_sha256"],
            repair.EXPECTED_PROTECTED_INVENTORY_SHA256,
        )

    def test_binds_fresh_independent_reviewer_accept(self) -> None:
        reviewer = self.payload["independent_reviewer"]
        self.assertEqual(reviewer["verdict"], "ACCEPT")
        self.assertEqual(reviewer["status"], "accepted")
        self.assertEqual(
            reviewer["completed_at"], repair.REVIEWER_COMPLETED_AT
        )
        self.assertEqual(
            reviewer["evidence_inventory"]["file_count"], 33
        )

    def test_rejects_stale_reviewer_completion(self) -> None:
        manifest = repair._load_json(
            repair.REVIEWER_ROOT / "manifest.json", "test manifest"
        )
        status = repair._load_json(
            repair.REVIEWER_ROOT / "status.json", "test status"
        )
        summary = repair._load_json(
            repair.REVIEWER_ROOT / "summary.json", "test summary"
        )
        classification = repair._load_json(
            repair.REVIEWER_ROOT / "classification-comparison.json",
            "test classification",
        )
        direct = repair._load_json(
            repair.REVIEWER_ROOT / "direct-byte-comparison.json",
            "test direct comparison",
        )
        status["updated_at"] = "2026-09-01T00:30:23.026808Z"
        with self.assertRaises(repair.ParserRepairCertificationError):
            repair._validate_reviewer_documents(
                manifest, status, summary, classification, direct
            )

    def test_rejects_certification_classification_drift(self) -> None:
        corrupted = copy.deepcopy(self.payload)
        corrupted["classification_counts"][
            "exact_output_determinism"
        ]["conditional-complete"] = 49
        with self.assertRaises(repair.ParserRepairCertificationError):
            repair._validate_certification_payload(corrupted)

    def test_rejects_certification_protection_drift(self) -> None:
        corrupted = copy.deepcopy(self.payload)
        corrupted["preservation"]["protected_inventory_sha256"] = "0" * 64
        with self.assertRaises(repair.ParserRepairCertificationError):
            repair._validate_certification_payload(corrupted)

    def test_written_artifacts_are_current(self) -> None:
        manifest = repair.validate_written_artifacts()
        self.assertEqual(manifest["status"], "certified")
        self.assertEqual(
            manifest["independent_reviewer"]["verdict"], "ACCEPT"
        )


if __name__ == "__main__":
    unittest.main()
