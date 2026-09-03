#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import preservation_policy_v1 as parent
import preservation_policy_v2 as policy
import preservation_policy_v3 as additive_policy


class PreservationPolicyV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = policy._load_policy_payload()
        cls.validated = additive_policy.validate_predecessor_policy()

    def test_v1_is_bound_by_unchanged_byte_identity(self) -> None:
        record = self.validated["parent_policy"]
        self.assertEqual(record["path"], "preservation/path_policy_v1.json")
        self.assertEqual(
            record["sha256"], policy.EXPECTED_PARENT_POLICY_SHA256
        )
        self.assertEqual(
            record["bytes"], policy.EXPECTED_PARENT_POLICY_BYTES
        )
        self.assertEqual(
            hashlib.sha256(policy.PARENT_POLICY_PATH.read_bytes()).hexdigest(),
            policy.EXPECTED_PARENT_POLICY_SHA256,
        )
        self.assertEqual(
            self.validated["parent_policy_id"], parent.POLICY_ID
        )

    def test_only_v3_package_and_review_lane_are_added(self) -> None:
        additions = self.validated["registered_additions"]
        self.assertEqual(
            set(additions),
            {
                policy.TARGET_078_V3_ADDITION,
                policy.TARGET_078_V3_REVIEW_ADDITION,
            },
        )
        records = additions[policy.TARGET_078_V3_ADDITION]
        self.assertGreater(len(records), 0)
        config = self.payload["registered_post_v1_additions"][
            policy.TARGET_078_V3_ADDITION
        ]
        self.assertEqual(config["file_count"], len(records))
        self.assertEqual(
            config["scope_root"],
            "evidence/target_078_insert_tail_refinement_v3",
        )

    def test_review_lane_is_explicit_and_currently_pending(self) -> None:
        records = self.validated["registered_additions"][
            policy.TARGET_078_V3_REVIEW_ADDITION
        ]
        config = self.payload["registered_post_v1_additions"][
            policy.TARGET_078_V3_REVIEW_ADDITION
        ]
        self.assertEqual(config["file_count"], len(records))
        self.assertEqual(records, [])

    def test_v3_paths_are_unique_sorted_canonical_and_closed(self) -> None:
        records = self.validated["registered_additions"][
            policy.TARGET_078_V3_ADDITION
        ]
        paths = [record["path"] for record in records]
        self.assertEqual(paths, sorted(paths, key=lambda value: Path(value).parts))
        self.assertEqual(len(paths), len(set(paths)))
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in policy.TARGET_078_V3_EVIDENCE.rglob("*")
            if path.is_file()
        }
        self.assertEqual(actual, set(paths))
        for path in paths:
            self.assertFalse(Path(path).is_absolute())
            self.assertNotIn("..", Path(path).parts)
            self.assertEqual(Path(path).as_posix(), path)

    def test_registration_mutation_is_rejected(self) -> None:
        records = copy.deepcopy(
            self.validated["registered_additions"][
                policy.TARGET_078_V3_ADDITION
            ]
        )
        records[0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "byte identity changed"
        ):
            parent._validate_artifact_records(
                records,
                "mutated target-078 v3 registration",
                root=ROOT,
            )

    def test_producer_can_repair_a_stale_registered_scope(self) -> None:
        payload = copy.deepcopy(self.payload)
        records = payload["registered_post_v1_additions"][
            policy.TARGET_078_V3_ADDITION
        ]["records"]
        records[0]["sha256"] = "0" * 64
        binding = additive_policy.validate_parent_binding(
            validate_parent_addition=False,
            parent_payload=payload,
        )
        self.assertEqual(binding["policy_id"], additive_policy.POLICY_ID)
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "byte identity changed"
        ):
            policy._validate_v3_registration(payload)

    def test_additional_registration_is_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["registered_post_v1_additions"]["unregistered"] = {}
        with self.assertRaisesRegex(
            policy.PreservationPolicyError,
            "registration set is invalid",
        ):
            policy._validate_v3_registration(payload)

    def test_final_campaign_membership_uses_additive_exclusion(self) -> None:
        groups = additive_policy.final_campaign_groups()
        self.assertEqual(
            {name: len(records) for name, records in groups.items()},
            parent.EXPECTED_FINAL_COUNTS,
        )

    def test_review_inventory_is_inherited_unchanged(self) -> None:
        review_additions = self.validated["registered_additions"][
            policy.TARGET_078_V3_REVIEW_ADDITION
        ]
        successor_reviews = additive_policy.validate_policy()[
            "registered_additions"
        ][additive_policy.TARGET_079_V3_REVIEW_ADDITION]
        self.assertEqual(
            len(self.validated["allowed_reviews"]),
            47
            + len(review_additions)
            + len(successor_reviews)
            + len(
                additive_policy.validate_policy()[
                    "target_080_lifecycle"
                ]["review_records"]
            )
            + len(
                additive_policy.validate_policy()[
                    "target_081_lifecycle"
                ]["review_records"]
            ),
        )
        for record in [*review_additions, *successor_reviews]:
            self.assertIn(record, self.validated["allowed_reviews"])

    def test_review_consumers_use_the_additive_policy(self) -> None:
        for relative in (
            "tools/final_reconciliation.py",
            "tools/operational_v2_reconciliation.py",
            "tools/run_target_079_operational_v1.py",
            "tests/test_operational_v2_reconciliation.py",
        ):
            with self.subTest(relative=relative):
                text = (ROOT / relative).read_text()
                self.assertIn(
                    "import preservation_policy_v3 as preservation_policy",
                    text,
                )


if __name__ == "__main__":
    unittest.main()
