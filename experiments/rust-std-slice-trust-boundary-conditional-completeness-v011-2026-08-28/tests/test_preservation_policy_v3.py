#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import preservation_policy_v2 as parent
import preservation_policy_v3 as policy


class PreservationPolicyV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = policy._load_policy_payload()
        cls.validated = policy.validate_policy()

    def test_v2_is_bound_by_unchanged_byte_identity(self) -> None:
        record = self.validated["parent_policy"]
        self.assertEqual(record["path"], "preservation/path_policy_v2.json")
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

    def test_only_target_079_v3_and_review_lane_are_added(self) -> None:
        additions = self.validated["registered_additions"]
        self.assertEqual(
            set(additions),
            {
                policy.TARGET_079_V3_ADDITION,
                policy.TARGET_079_V3_REVIEW_ADDITION,
            },
        )
        records = additions[policy.TARGET_079_V3_ADDITION]
        self.assertGreater(len(records), 0)
        config = self.payload["registered_post_v2_additions"][
            policy.TARGET_079_V3_ADDITION
        ]
        self.assertEqual(config["file_count"], len(records))
        self.assertEqual(
            config["scope_root"],
            "evidence/target_079_insert_tail_refinement_v3",
        )

    def test_review_lane_registers_independent_acceptance(self) -> None:
        records = self.validated["registered_additions"][
            policy.TARGET_079_V3_REVIEW_ADDITION
        ]
        config = self.payload["registered_post_v2_additions"][
            policy.TARGET_079_V3_REVIEW_ADDITION
        ]
        self.assertEqual(config["file_count"], len(records))
        self.assertEqual(len(records), 1)
        self.assertEqual(
            records[0]["path"],
            "review/"
            "REVIEW_ADDENDUM_TARGET_079_INSERT_TAIL_REFINEMENT_V3.md",
        )

    def test_v3_paths_are_unique_sorted_canonical_and_closed(self) -> None:
        records = self.validated["registered_additions"][
            policy.TARGET_079_V3_ADDITION
        ]
        paths = [record["path"] for record in records]
        self.assertEqual(
            paths, sorted(paths, key=lambda value: Path(value).parts)
        )
        self.assertEqual(len(paths), len(set(paths)))
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in policy.TARGET_079_V3_EVIDENCE.rglob("*")
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
                policy.TARGET_079_V3_ADDITION
            ]
        )
        records[0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "byte identity changed"
        ):
            policy.base._validate_artifact_records(
                records,
                "mutated target-079 v3 registration",
                root=ROOT,
            )

    def test_producer_can_repair_a_stale_registered_scope(self) -> None:
        payload = copy.deepcopy(self.payload)
        records = payload["registered_post_v2_additions"][
            policy.TARGET_079_V3_ADDITION
        ]["records"]
        records[0]["sha256"] = "0" * 64
        binding = policy.validate_parent_binding(payload)
        self.assertEqual(binding["policy_id"], policy.POLICY_ID)
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "byte identity changed"
        ):
            policy._validate_v3_registration(payload)

    def test_additional_registration_is_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["registered_post_v2_additions"]["unregistered"] = {}
        with self.assertRaisesRegex(
            policy.PreservationPolicyError,
            "registration set is invalid",
        ):
            policy._validate_v3_registration(payload)

    def test_final_campaign_membership_uses_additive_exclusion(self) -> None:
        groups = policy.final_campaign_groups()
        self.assertEqual(
            {name: len(records) for name, records in groups.items()},
            policy.base.EXPECTED_FINAL_COUNTS,
        )

    def test_review_inventory_is_inherited_unchanged(self) -> None:
        chain = self.validated["parent_chain"]
        reviews = self.validated["registered_additions"][
            policy.TARGET_079_V3_REVIEW_ADDITION
        ]
        target_080_reviews = self.validated[
            "target_080_lifecycle"
        ]["review_records"]
        target_081_reviews = self.validated[
            "target_081_lifecycle"
        ]["review_records"]
        self.assertEqual(
            len(self.validated["allowed_reviews"]),
            47
            + len(chain["parent_reviews"])
            + len(reviews)
            + len(target_080_reviews)
            + len(target_081_reviews),
        )
        for record in [
            *reviews,
            *target_080_reviews,
            *target_081_reviews,
        ]:
            self.assertIn(record, self.validated["allowed_reviews"])

    def test_target_080_v4_lane_closes_only_through_v5(self) -> None:
        v4 = policy._load_target_080_policy(
            policy.TARGET_080_POLICY_V4_PATH,
            "target-080 path-policy-v4",
        )
        self.assertEqual(
            v4["independent_review_lane"]["status"], "pending"
        )
        lifecycle = self.validated["target_080_lifecycle"]
        self.assertEqual(lifecycle["status"], "review-accepted")
        self.assertIsNotNone(lifecycle["policy_v5"])
        self.assertFalse(
            lifecycle["selected_as_operational_v2_overlay"]
        )
        self.assertEqual(
            set(lifecycle["registered_addenda"]),
            {"json", "csv"},
        )
        self.assertEqual(
            [record["path"] for record in lifecycle["review_records"]],
            [
                "review/"
                "REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md"
            ],
        )

    def test_target_080_v4_rejects_a_different_review_lane(self) -> None:
        payload = copy.deepcopy(
            policy._load_target_080_policy(
                policy.TARGET_080_POLICY_V4_PATH,
                "target-080 path-policy-v4",
            )
        )
        payload["independent_review_lane"]["expected_verdict_path"] = (
            "review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md"
        )
        with self.assertRaisesRegex(
            policy.PreservationPolicyError,
            "independent-review lane is invalid",
        ):
            policy._validate_target_080_v4(
                payload,
                root=ROOT,
                record_resolver=lambda record: ROOT / record["path"],
                policy_record=policy._artifact(
                    policy.TARGET_080_POLICY_V4_PATH
                ),
            )

    def test_target_080_acceptance_requires_v5_registration(self) -> None:
        absent_v5 = ROOT / "preservation/path_policy_v5.absent-test.json"
        self.assertFalse(absent_v5.exists())
        with (
            mock.patch.object(
                policy, "TARGET_080_POLICY_V5_PATH", absent_v5
            ),
            mock.patch.object(
                policy,
                "_target_080_review_verdict",
                return_value="ACCEPT",
            ),
        ):
            with self.assertRaisesRegex(
                policy.PreservationPolicyError,
                "acceptance is not registered by path_policy_v5",
            ):
                policy.target_080_lifecycle()

    def test_target_080_v5_binds_one_exact_accepting_review(self) -> None:
        review_record = policy._artifact(policy.TARGET_080_REVIEW_PATH)
        payload = {
            "schema_version": 1,
            "policy_id": policy.TARGET_080_POLICY_V5_ID,
            "parent_policy_id": policy.TARGET_080_POLICY_V4_ID,
            "parent_policy": policy._artifact(
                policy.TARGET_080_POLICY_V4_PATH
            ),
            "policy": "register the independent target-080 verdict",
            "registered_post_v4_additions": {
                policy.TARGET_080_REVIEW_ADDITION: {
                    "file_count": 1,
                    "records": [review_record],
                }
            },
        }
        with mock.patch.object(
            policy,
            "_target_080_review_verdict",
            return_value="ACCEPT",
        ):
            self.assertEqual(
                policy._validate_target_080_v5(payload, root=ROOT),
                [review_record],
            )

    def test_historical_digest_uses_mid_campaign_validation(self) -> None:
        checks: list[bool] = []
        original = policy.base._validate_operational_v2_inventory

        def validate_operational_inventory(
            payload: dict[str, object],
            *,
            root: Path,
            validate_all_records: bool = True,
        ) -> dict[str, list[dict[str, object]]]:
            checks.append(validate_all_records)
            return original(
                payload,
                root=root,
                validate_all_records=validate_all_records,
            )

        with mock.patch.object(
            policy.base,
            "_validate_operational_v2_inventory",
            side_effect=validate_operational_inventory,
        ):
            digest = policy.historical_review_digest()

        self.assertEqual(checks, [False])
        self.assertEqual(len(digest), 64)

    def test_review_consumers_use_the_additive_policy(self) -> None:
        for relative in (
            "tools/final_reconciliation.py",
            "tools/operational_v2_reconciliation.py",
            "tools/run_target_078_insert_tail_refinement_v3.py",
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
