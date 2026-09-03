#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import preservation_policy_v3 as policy
import run_target_080_operational_v1 as target_080


PROTECTED_POLICY_SHA256 = {
    "path_policy_v1.json": (
        "6f625f9808170c354ef5a6d5a68142989538dedb6677ac95264a2e7ffc0c4619"
    ),
    "path_policy_v2.json": (
        "df04b6d0b5388e0620d07623e365c9d538f9b41c762f98ef898cc3cdd1ca7cfe"
    ),
    "path_policy_v3.json": (
        "2717af5821625cdce4065de3e6f499efa6660a8be701e651298092ad1e4e9624"
    ),
    "path_policy_v4.json": (
        "d7cfd30f5204d621628d2289d8a76ea5074b974e6adfe74bb356fbd986e62bc7"
    ),
    "path_policy_v5.json": (
        "613243010af9581dc0a15b55004bc807be260fdb3dcb4ed14524633839a02451"
    ),
}


class PreservationArchiveV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.v5 = json.loads(
            (ROOT / "preservation/path_policy_v5.json").read_text()
        )
        cls.v6 = json.loads(
            (ROOT / "preservation/path_policy_v6.json").read_text()
        )

    def test_policies_v1_through_v5_retain_task_start_bytes(self) -> None:
        for name, expected in PROTECTED_POLICY_SHA256.items():
            with self.subTest(policy=name):
                path = ROOT / "preservation" / name
                self.assertEqual(
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                    expected,
                )

    def test_v5_accepted_v4_and_record_versions_are_materialized(self) -> None:
        validated = policy._validate_target_081_v6(
            self.v6, self.v5, root=ROOT
        )
        self.assertEqual(
            validated["accepted_v4_record"], self.v5["parent_policy"]
        )
        self.assertEqual(
            len(validated["record_version_mappings"]), 5
        )
        lifecycle = policy.target_080_lifecycle()
        self.assertEqual(lifecycle["status"], "review-accepted")
        self.assertIsNotNone(lifecycle["archive_resolution"])
        self.assertEqual(
            lifecycle["policy_v4"], self.v5["parent_policy"]
        )

    def test_target_081_lifecycle_validates_v6_addenda(self) -> None:
        lifecycle = policy.target_081_lifecycle()
        self.assertIn(
            lifecycle["status"], {"review-pending", "review-accepted"}
        )
        self.assertEqual(
            lifecycle["policy_v6"],
            policy._artifact(policy.TARGET_081_POLICY_V6_PATH),
        )
        self.assertEqual(
            {
                name: record["path"]
                for name, record in lifecycle[
                    "registered_addenda"
                ].items()
            },
            {
                "json": (
                    "crosswalk/target_081_operational_v1_addendum.json"
                ),
                "csv": (
                    "crosswalk/target_081_operational_v1_addendum.csv"
                ),
            },
        )
        self.assertFalse(
            lifecycle["selected_as_operational_v2_overlay"]
        )

    def test_target_081_v7_binds_exact_v6_and_one_accept(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            v6_path = root / "preservation/path_policy_v6.json"
            review_path = (
                root
                / "review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md"
            )
            v6_path.parent.mkdir(parents=True)
            review_path.parent.mkdir(parents=True)
            v6_path.write_text('{"policy_id": "test-v6"}\n')
            review_path.write_text(
                "# Independent target-081 review\n\n"
                "**VERDICT: ACCEPT**\n\n"
                "Target: core::slice::sort_unstable_by\n"
            )
            review_record = policy._artifact(review_path, root=root)
            payload = {
                "schema_version": 1,
                "policy_id": policy.TARGET_081_POLICY_V7_ID,
                "parent_policy_id": policy.TARGET_081_POLICY_V6_ID,
                "parent_policy": policy._artifact(v6_path, root=root),
                "policy": "register the independent target-081 verdict",
                "registered_post_v6_additions": {
                    policy.TARGET_081_REVIEW_ADDITION: {
                        "file_count": 1,
                        "records": [review_record],
                    }
                },
            }
            self.assertEqual(
                policy._validate_target_081_v7(payload, root=root),
                [review_record],
            )

            wrong_parent = copy.deepcopy(payload)
            wrong_parent["parent_policy"]["sha256"] = "0" * 64
            with self.assertRaisesRegex(
                policy.PreservationPolicyError, "byte identity changed"
            ):
                policy._validate_target_081_v7(
                    wrong_parent, root=root
                )

            duplicate_review = copy.deepcopy(payload)
            registration = duplicate_review[
                "registered_post_v6_additions"
            ][policy.TARGET_081_REVIEW_ADDITION]
            registration["file_count"] = 2
            registration["records"].append(copy.deepcopy(review_record))
            with self.assertRaisesRegex(
                policy.PreservationPolicyError, "register one review"
            ):
                policy._validate_target_081_v7(
                    duplicate_review, root=root
                )

            review_path.write_text(
                "# Independent target-081 review\n\n"
                "**VERDICT: REJECT**\n\n"
                "Target: core::slice::sort_unstable_by\n"
            )
            rejected = copy.deepcopy(payload)
            rejected_record = policy._artifact(review_path, root=root)
            rejected["registered_post_v6_additions"][
                policy.TARGET_081_REVIEW_ADDITION
            ]["records"] = [rejected_record]
            with self.assertRaisesRegex(
                policy.PreservationPolicyError, "accepting verdict"
            ):
                policy._validate_target_081_v7(rejected, root=root)

    def test_target_081_lifecycle_requires_v7_for_acceptance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            preservation = root / "preservation"
            review = root / "review"
            preservation.mkdir()
            review.mkdir()
            v5_path = preservation / "path_policy_v5.json"
            v6_path = preservation / "path_policy_v6.json"
            v7_path = preservation / "path_policy_v7.json"
            review_path = (
                review / "REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md"
            )
            v5_path.write_text("{}\n")
            v6_path.write_text("{}\n")
            review_path.write_text(
                "# Independent target-081 review\n\n"
                "**VERDICT: ACCEPT**\n\n"
                "Target: core::slice::sort_unstable_by\n"
            )
            v7_payload = {
                "schema_version": 1,
                "policy_id": policy.TARGET_081_POLICY_V7_ID,
                "parent_policy_id": policy.TARGET_081_POLICY_V6_ID,
                "parent_policy": policy._artifact(v6_path, root=root),
                "policy": "register the independent target-081 verdict",
                "registered_post_v6_additions": {
                    policy.TARGET_081_REVIEW_ADDITION: {
                        "file_count": 1,
                        "records": [
                            policy._artifact(review_path, root=root)
                        ],
                    }
                },
            }
            v7_path.write_text(
                json.dumps(v7_payload, indent=2, sort_keys=True) + "\n"
            )
            validated_v6 = {
                "registered_records": [],
                "addenda": {
                    "json": {
                        "path": (
                            "crosswalk/"
                            "target_081_operational_v1_addendum.json"
                        ),
                        "bytes": 1,
                        "sha256": "0" * 64,
                    },
                    "csv": {
                        "path": (
                            "crosswalk/"
                            "target_081_operational_v1_addendum.csv"
                        ),
                        "bytes": 1,
                        "sha256": "0" * 64,
                    },
                },
                "accepted_v4_record": {},
                "accepted_v4_archive": {},
                "record_version_mappings": [],
            }
            with (
                mock.patch.object(
                    policy,
                    "_validate_target_081_v6",
                    return_value=validated_v6,
                ),
                mock.patch.object(
                    policy,
                    "_validate_target_080_v5",
                    return_value=[],
                ),
            ):
                lifecycle = policy.target_081_lifecycle(root=root)
                self.assertEqual(
                    lifecycle["status"], "review-accepted"
                )
                self.assertEqual(
                    lifecycle["review_records"],
                    [
                        policy._artifact(review_path, root=root)
                    ],
                )
                v7_path.unlink()
                with self.assertRaisesRegex(
                    policy.PreservationPolicyError,
                    "acceptance is not registered by path_policy_v7",
                ):
                    policy.target_081_lifecycle(root=root)

    def test_target_080_producer_cannot_rebuild_accepted_v4(self) -> None:
        before = target_080.PATH_POLICY_V4.read_bytes()
        with mock.patch.object(
            target_080.common, "write_json"
        ) as write_json:
            artifact = target_080._write_path_policy_v4()
        write_json.assert_not_called()
        self.assertEqual(target_080.PATH_POLICY_V4.read_bytes(), before)
        self.assertEqual(
            artifact["sha256"], hashlib.sha256(before).hexdigest()
        )

    def test_missing_and_tampered_archive_bytes_are_rejected(self) -> None:
        missing = {
            "path": "preservation/archive_v1/missing.json",
            "bytes": 1,
            "sha256": "0" * 64,
        }
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "missing"
        ):
            policy._validate_archive_artifact(
                missing,
                "missing archive",
                root=ROOT,
                archive_root=policy.TARGET_080_V4_ARCHIVE_ROOT,
            )

        tampered = copy.deepcopy(
            self.v6["archive_resolution"][
                "accepted_policy_version"
            ]["archive_record"]
        )
        tampered["sha256"] = "0" * 64
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "byte identity changed"
        ):
            policy._validate_archive_artifact(
                tampered,
                "tampered archive",
                root=ROOT,
                archive_root=policy.TARGET_080_V4_ARCHIVE_ROOT,
            )

    def test_traversal_conflicts_and_missing_mappings_are_rejected(self) -> None:
        traversal = {
            "path": "preservation/archive_v1/../path_policy_v4.json",
            "bytes": 0,
            "sha256": "0" * 64,
        }
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "canonical"
        ):
            policy._validate_archive_artifact(
                traversal,
                "traversing archive",
                root=ROOT,
                archive_root=policy.TARGET_080_V4_ARCHIVE_ROOT,
            )

        conflicting = copy.deepcopy(self.v6)
        conflicting["archive_resolution"][
            "record_version_mappings"
        ].append(
            copy.deepcopy(
                conflicting["archive_resolution"][
                    "record_version_mappings"
                ][0]
            )
        )
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "conflict"
        ):
            policy._validate_archive_resolution(
                conflicting, self.v5, root=ROOT
            )

        unmapped = copy.deepcopy(self.v6)
        unmapped["archive_resolution"][
            "record_version_mappings"
        ].pop()
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "explicit version mappings"
        ):
            policy._validate_archive_resolution(
                unmapped, self.v5, root=ROOT
            )

    def test_unmapped_archive_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "preservation/archive_v1"
            archive.mkdir(parents=True)
            (archive / "mapped").write_text("mapped")
            (archive / "extra").write_text("extra")
            with self.assertRaisesRegex(
                policy.PreservationPolicyError, "unmapped"
            ):
                policy._validate_archive_membership(
                    PurePosixPath("preservation/archive_v1"),
                    {"preservation/archive_v1/mapped"},
                    root=root,
                )

    def test_symlink_escape_is_rejected_for_artifact_and_membership(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "preservation/archive_v1"
            archive.mkdir(parents=True)
            outside = root / "outside"
            outside.write_text("mapped")
            (archive / "mapped").symlink_to(outside)
            record = {
                "path": "preservation/archive_v1/mapped",
                "bytes": outside.stat().st_size,
                "sha256": hashlib.sha256(
                    outside.read_bytes()
                ).hexdigest(),
            }

            with self.assertRaisesRegex(
                policy.PreservationPolicyError,
                "resolves outside the archive root",
            ):
                policy._validate_archive_artifact(
                    record,
                    "escaping archive",
                    root=root,
                    archive_root=PurePosixPath(
                        "preservation/archive_v1"
                    ),
                )
            with self.assertRaisesRegex(
                policy.PreservationPolicyError,
                "member resolves outside the archive root",
            ):
                policy._validate_archive_membership(
                    PurePosixPath("preservation/archive_v1"),
                    {"preservation/archive_v1/mapped"},
                    root=root,
                )


if __name__ == "__main__":
    unittest.main()
