#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import preservation_policy_v8 as policy


class PreservationPolicyV8Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(policy.POLICY_PATH.read_text())

    def test_v8_binds_exact_v7_and_declares_separate_v9_lane(self) -> None:
        validated = policy.validate_policy()
        self.assertEqual(
            self.payload["parent_policy"],
            policy._artifact(policy.PARENT_POLICY_PATH),
        )
        self.assertEqual(
            self.payload["independent_review_lane"],
            {
                "status": "pending",
                "expected_policy_id": policy.V9_POLICY_ID,
                "expected_policy_path": "preservation/path_policy_v9.json",
                "expected_verdict_path": (
                    "review/"
                    "REVIEW_ADDENDUM_TARGET_082_OPERATIONAL_V1.md"
                ),
            },
        )
        self.assertGreater(len(validated["registered_records"]), 50)

    def test_archive_mappings_are_exact_complete_and_project_local(
        self,
    ) -> None:
        resolved, mappings = policy._mapping_index(
            self.payload, root=ROOT
        )
        self.assertEqual(set(resolved), set(policy.ARCHIVE_MAPPINGS))
        self.assertEqual(len(mappings), len(policy.ARCHIVE_MAPPINGS))
        self.assertTrue(
            all(
                mapping["source"].startswith("project-local-archive:")
                for mapping in mappings
            )
        )
        historical, historical_mappings = (
            policy._historical_mapping_index(
                self.payload, root=ROOT
            )
        )
        self.assertEqual(
            set(historical),
            set(policy.HISTORICAL_ARCHIVE_MAPPINGS),
        )
        self.assertEqual(
            len(historical_mappings),
            len(policy.HISTORICAL_ARCHIVE_MAPPINGS),
        )

    def test_missing_duplicate_and_traversing_mappings_fail_closed(
        self,
    ) -> None:
        missing = copy.deepcopy(self.payload)
        missing["archive_resolution"]["record_version_mappings"].pop()
        with self.assertRaises(policy.PreservationPolicyError):
            policy._mapping_index(missing, root=ROOT)

        duplicate = copy.deepcopy(self.payload)
        duplicate["archive_resolution"]["record_version_mappings"].append(
            copy.deepcopy(
                duplicate["archive_resolution"][
                    "record_version_mappings"
                ][0]
            )
        )
        with self.assertRaises(policy.PreservationPolicyError):
            policy._mapping_index(duplicate, root=ROOT)

        traversal = copy.deepcopy(self.payload)
        traversal["archive_resolution"]["record_version_mappings"][0][
            "archive_record"
        ]["path"] = "preservation/archive_v2/../path_policy_v7.json"
        with self.assertRaises(policy.PreservationPolicyError):
            policy._mapping_index(traversal, root=ROOT)

        missing_historical = copy.deepcopy(self.payload)
        missing_historical["archive_resolution"][
            "historical_record_version_mappings"
        ].pop()
        with self.assertRaises(policy.PreservationPolicyError):
            policy._historical_mapping_index(
                missing_historical, root=ROOT
            )

    def test_target_082_lifecycle_is_pending_and_not_an_overlay(self) -> None:
        lifecycle = policy.target_082_lifecycle()
        self.assertEqual(lifecycle["status"], "review-pending")
        self.assertIsNone(lifecycle["policy_v9"])
        self.assertEqual(lifecycle["review_records"], [])
        self.assertFalse(lifecycle["selected_as_operational_v2_overlay"])
        self.assertEqual(
            {
                name: record["path"]
                for name, record in lifecycle[
                    "registered_addenda"
                ].items()
            },
            {
                "json": (
                    "crosswalk/"
                    "target_082_operational_v1_addendum.json"
                ),
                "csv": (
                    "crosswalk/"
                    "target_082_operational_v1_addendum.csv"
                ),
            },
        )


if __name__ == "__main__":
    unittest.main()
