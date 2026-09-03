#!/usr/bin/env python3
"""Run the accepted target-081 artifact tests with v8 archive resolution."""

from __future__ import annotations

from pathlib import Path


_ROOT = Path(__file__).resolve().parents[1]
_ARCHIVED = (
    _ROOT
    / "preservation/archive_v2/tests/"
    "test_target_081_operational_artifacts_v1.py"
)
_MODULE_NAME = __name__
__name__ = "_test_target_081_operational_artifacts_v1_accepted"
exec(compile(_ARCHIVED.read_bytes(), str(Path(__file__)), "exec"), globals())
__name__ = _MODULE_NAME


def _test_path_policy_v6_with_archive_resolution(self) -> None:
    import preservation_policy_v8

    policy = json.loads(
        (ROOT / "preservation/path_policy_v6.json").read_text()
    )
    self.assertEqual(
        policy["parent_policy_id"],
        "slice-preservation-path-policy-v5",
    )
    parent = ROOT / policy["parent_policy"]["path"]
    self.assertEqual(parent.stat().st_size, policy["parent_policy"]["bytes"])
    self.assertEqual(
        hashlib.sha256(parent.read_bytes()).hexdigest(),
        policy["parent_policy"]["sha256"],
    )
    lane = policy["registered_post_v5_additions"][
        "target_081_operational_v1"
    ]
    self.assertEqual(lane["file_count"], len(lane["records"]))
    self.assertGreater(lane["file_count"], 60)
    registered = {record["path"] for record in lane["records"]}
    self.assertIn("tools/target_081_operational_v1.py", registered)
    self.assertIn(
        "evidence/target_081_operational_v1/result.json", registered
    )
    self.assertNotIn(
        "review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md",
        registered,
    )
    v5 = json.loads(
        (ROOT / "preservation/path_policy_v5.json").read_text()
    )
    validated = preservation_policy_v8.validate_target_081_v6(
        policy, v5, root=ROOT
    )
    resolutions = validated["registered_record_resolutions"]
    for record in lane["records"]:
        path = Path(resolutions[record["path"]])
        with self.subTest(path=record["path"]):
            self.assertEqual(path.stat().st_size, record["bytes"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                record["sha256"],
            )
    self.assertEqual(policy["independent_review_lane"]["status"], "pending")


Target081OperationalArtifactsV1Tests.test_path_policy_v6_binds_v5_and_complete_package = (
    _test_path_policy_v6_with_archive_resolution
)


if __name__ == "__main__":
    unittest.main()
