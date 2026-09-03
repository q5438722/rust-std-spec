#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import preservation_policy_v1 as policy
import preservation_policy_v3 as additive_policy
import build_authority_design as authority_builder


def artifact(path: Path, root: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
    }


class PreservationPolicyV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.additive = additive_policy.validate_policy()
        cls.validated = cls.additive["legacy"]

    def test_exact_historical_and_registered_membership(self) -> None:
        self.assertEqual(
            {
                name: len(records)
                for name, records in self.validated[
                    "final_campaign_groups"
                ].items()
            },
            policy.EXPECTED_FINAL_COUNTS,
        )
        self.assertEqual(
            {
                name: len(records)
                for name, records in self.validated[
                    "operational_v2_groups"
                ].items()
            },
            policy.EXPECTED_OPERATIONAL_V2_COUNTS,
        )
        self.assertEqual(
            len(
                self.validated["registered_additions"][
                    policy.TARGET_078_ADDITION
                ]
            ),
            142,
        )
        self.assertEqual(
            len(
                self.validated["registered_additions"][
                    policy.TARGET_079_REVIEW_ADDITION
                ]
            ),
            1,
        )
        self.assertEqual(
            len(self.validated["allowed_reviews"]),
            47
            + len(
                self.additive["parent_chain"]["parent_reviews"]
            )
            + len(
                self.additive["registered_additions"][
                    additive_policy.TARGET_079_V3_REVIEW_ADDITION
                ]
            )
            + len(
                self.additive["target_080_lifecycle"][
                    "review_records"
                ]
            )
            + len(
                self.additive["target_081_lifecycle"][
                    "review_records"
                ]
            ),
        )

    def test_registered_paths_are_unique_sorted_and_canonical(self) -> None:
        for name, records in self.validated[
            "registered_additions"
        ].items():
            with self.subTest(name=name):
                paths = [record["path"] for record in records]
                self.assertEqual(
                    paths,
                    sorted(
                        paths,
                        key=lambda value: Path(value).parts,
                    ),
                )
                self.assertEqual(len(paths), len(set(paths)))
                for path in paths:
                    self.assertEqual(Path(path).as_posix(), path)
                    self.assertNotIn("..", Path(path).parts)
                    self.assertFalse(Path(path).is_absolute())

    def test_final_and_operational_sources_are_bound_by_byte_identity(self) -> None:
        payload = policy._load_policy_payload()
        inventories = payload["historical_inventories"]
        self.assertEqual(
            inventories["final_campaign"]["artifact"]["sha256"],
            hashlib.sha256(policy.FINAL_BASELINE.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            inventories["operational_v2"]["artifact"]["sha256"],
            hashlib.sha256(
                policy.OPERATIONAL_V2_MANIFEST.read_bytes()
            ).hexdigest(),
        )

    def test_live_request_uses_frozen_historical_identity(self) -> None:
        records = self.validated["operational_v2_groups"]["prior_reviews"]
        record = next(
            item
            for item in records
            if item["path"] == "review/REVIEW_REQUEST.md"
        )
        self.assertEqual(
            record, policy.OPERATIONAL_V2_REVIEW_REQUEST_RECORD
        )
        self.assertEqual(
            artifact(
                policy.OPERATIONAL_V2_REVIEW_REQUEST_ARCHIVE, ROOT
            )["sha256"],
            record["sha256"],
        )
        self.assertNotEqual(
            hashlib.sha256(policy.LIVE_REVIEW_REQUEST.read_bytes()).hexdigest(),
            record["sha256"],
        )
        policy._validate_artifact_records(
            [record],
            "operational-v2 archived review request",
            root=ROOT,
            expected_count=1,
        )

    def test_authority_reset_preserves_live_review_request(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request = root / "review/REVIEW_REQUEST.md"
            request.parent.mkdir(parents=True)
            request.write_text("live target-specific request\n")
            generated = root / "crosswalk"
            generated.mkdir()
            (generated / "generated.txt").write_text("generated\n")
            with mock.patch.object(authority_builder, "OUT", root):
                authority_builder.reset_generated_paths()
            self.assertEqual(
                request.read_text(), "live target-specific request\n"
            )
            self.assertFalse(generated.exists())

    def _temporary_scope(
        self,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path, list[dict[str, object]]]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        scope = root / "evidence/registered"
        scope.mkdir(parents=True)
        first = scope / "first.txt"
        second = scope / "second.txt"
        first.write_text("first\n")
        second.write_text("second\n")
        records = [artifact(first, root), artifact(second, root)]
        return temporary, root, records

    def test_mutation_is_rejected(self) -> None:
        temporary, root, records = self._temporary_scope()
        self.addCleanup(temporary.cleanup)
        corrupted = copy.deepcopy(records)
        corrupted[0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "byte identity changed"
        ):
            policy._validate_artifact_records(corrupted, "test", root=root)

    def test_deletion_is_rejected(self) -> None:
        temporary, root, records = self._temporary_scope()
        self.addCleanup(temporary.cleanup)
        (root / records[0]["path"]).unlink()
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "missing"
        ):
            policy._validate_artifact_records(records, "test", root=root)

    def test_substitution_is_rejected(self) -> None:
        temporary, root, records = self._temporary_scope()
        self.addCleanup(temporary.cleanup)
        substituted = copy.deepcopy(records)
        substituted[0]["path"] = substituted[1]["path"]
        with self.assertRaises(policy.PreservationPolicyError):
            policy._validate_artifact_records(
                substituted, "test", root=root
            )

    def test_duplicate_entry_is_rejected(self) -> None:
        temporary, root, records = self._temporary_scope()
        self.addCleanup(temporary.cleanup)
        duplicated = [*records, copy.deepcopy(records[-1])]
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "duplicate path"
        ):
            policy._validate_artifact_records(
                duplicated, "test", root=root
            )

    def test_noncanonical_path_is_rejected(self) -> None:
        temporary, root, records = self._temporary_scope()
        self.addCleanup(temporary.cleanup)
        noncanonical = copy.deepcopy(records)
        noncanonical[0]["path"] = (
            "evidence/registered/../registered/first.txt"
        )
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "not canonical"
        ):
            policy._validate_artifact_records(
                noncanonical, "test", root=root
            )

    def test_unregistered_evidence_addition_is_rejected(self) -> None:
        temporary, root, records = self._temporary_scope()
        self.addCleanup(temporary.cleanup)
        (root / "evidence/registered/unregistered.txt").write_text("new\n")
        with self.assertRaisesRegex(
            policy.PreservationPolicyError, "scope membership changed"
        ):
            policy._validate_exact_scope(
                "evidence/registered", records, "test", root=root
            )

    def test_unregistered_review_addition_is_rejected(self) -> None:
        temporary, root, records = self._temporary_scope()
        self.addCleanup(temporary.cleanup)
        review = root / "review"
        review.mkdir()
        allowed = review / "accepted.md"
        allowed.write_text("accepted\n")
        allowed_record = artifact(allowed, root)
        (review / "unregistered.md").write_text("new\n")
        with self.assertRaisesRegex(
            policy.PreservationPolicyError,
            "review scope membership changed",
        ):
            policy._validate_review_membership(
                [allowed_record], [], [], root=root
            )


if __name__ == "__main__":
    unittest.main()
