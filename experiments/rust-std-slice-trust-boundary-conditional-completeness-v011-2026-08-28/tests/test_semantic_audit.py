from __future__ import annotations

import hashlib
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import campaign_common as common


class SemanticAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scope = common.derive_scope()
        cls.dependency_payload: list[dict] = []
        cls.external_payload: list[dict] = []
        cls.external_sites: dict[tuple[str, str], dict] = {}
        cls.dependency_ids: set[str] = set()
        for manifest_row in cls.scope["selected_manifest_rows"]:
            target = manifest_row["target"]
            order = int(cls.scope["proof_by_target"][target]["input_order"])
            paths = common.proof_paths(target, order)
            dependency = json.loads(paths["dependency"].read_text())
            for index, item in enumerate(
                dependency.get("assumptions_and_boundaries", []), start=1
            ):
                record_id = f"TS-{order:03d}-D{index:03d}"
                cls.dependency_ids.add(record_id)
                cls.dependency_payload.append(
                    {"record_id": record_id, "target": target, "record": item}
                )
            for index, item in enumerate(
                common.external_body_sites(paths["harness"]), start=1
            ):
                record_id = f"TS-{order:03d}-E{index:03d}"
                cls.external_sites[(target, item["symbol"])] = item
                cls.external_payload.append(
                    {
                        "record_id": record_id,
                        "target": target,
                        "symbol": item["symbol"],
                        "contract_text": item["contract_text"],
                    }
                )

    @staticmethod
    def digest(payload: list[dict]) -> str:
        encoded = json.dumps(
            payload, sort_keys=True, separators=(",", ":")
        ).encode()
        return hashlib.sha256(encoded).hexdigest()

    def test_external_audit_is_exhaustive_and_frozen(self) -> None:
        self.assertEqual(
            set(self.external_sites), set(common.EXTERNAL_SITE_SEMANTIC_AUDIT)
        )
        self.assertEqual(len(self.external_sites), 86)
        self.assertEqual(
            self.digest(self.external_payload),
            common.EXTERNAL_AUDIT_INPUT_SHA256,
        )
        self.assertEqual(
            Counter(common.EXTERNAL_SITE_SEMANTIC_AUDIT.values()),
            Counter(
                {
                    "complete-target-postcondition": 11,
                    "complete-branch-postcondition": 14,
                    "answer-equivalent-result": 9,
                    "opaque-whole-algorithm": 6,
                    "pointer-layout-provenance-transition": 14,
                    "intermediate-raw-slice-constructor": 5,
                    "intermediate-subrange-split": 3,
                    "derived-borrow-source-callee": 10,
                    "arithmetic-or-offset-fact": 4,
                    "panic-edge": 3,
                    "callback-or-element-effect": 7,
                }
            ),
        )

    def test_measured_answer_bearing_sites_are_rejected(self) -> None:
        expected = {
            (
                "core::slice::from_raw_parts",
                "rust_1_96_from_raw_parts_ub_checked_raw_slice",
            ): "complete-target-postcondition",
            (
                "core::slice::from_raw_parts_mut",
                "rust_1_96_from_raw_parts_mut_ub_checked_raw_slice",
            ): "complete-target-postcondition",
            (
                "core::slice::get_unchecked",
                "rust_1_96_sliceindex_get_unchecked_ref",
            ): "complete-target-postcondition",
            (
                "core::slice::get_unchecked_mut",
                "rust_1_96_sliceindex_get_unchecked_mut_ref",
            ): "complete-target-postcondition",
            (
                "core::slice::assume_init_mut",
                "rust_1_96_assume_init_mut_raw_cast",
            ): "complete-target-postcondition",
            (
                "core::slice::element_offset",
                "rust_1_96_element_offset_some_bridge",
            ): "complete-branch-postcondition",
            (
                "core::slice::subslice_range",
                "rust_1_96_subslice_range_some_bridge",
            ): "complete-branch-postcondition",
        }
        for key, category in expected.items():
            self.assertEqual(
                common.EXTERNAL_SITE_SEMANTIC_AUDIT[key], category, key
            )
        self.assertEqual(
            common.EXTERNAL_SITE_SEMANTIC_AUDIT[
                ("core::slice::as_chunks", "from_raw_parts")
            ],
            "intermediate-raw-slice-constructor",
        )

    def test_dependency_audit_is_exhaustive_and_rejects_answer_equivalents(
        self,
    ) -> None:
        category_sets = (
            set(common.DEPENDENCY_CONTEXT_ONLY_RECORD_IDS),
            set(common.DEPENDENCY_ADMISSIBLE_RECORD_IDS),
            set(common.DEPENDENCY_INTRINSIC_INADMISSIBLE),
        )
        self.assertEqual(sum(map(len, category_sets)), 232)
        self.assertEqual(len(set().union(*category_sets)), 232)
        self.assertEqual(set().union(*category_sets), self.dependency_ids)
        self.assertEqual(
            self.digest(self.dependency_payload),
            common.DEPENDENCY_AUDIT_INPUT_SHA256,
        )
        self.assertEqual(
            set(common.DEPENDENCY_INTRINSIC_INADMISSIBLE),
            {"TS-019-D001", "TS-021-D001", "TS-053-D001"},
        )

    def test_audit_rederives_twenty_eight_admissible_targets(self) -> None:
        inadmissible_categories = {
            category
            for category, policy in common.EXTERNAL_SEMANTIC_CATEGORY_POLICY.items()
            if policy["semantic_disposition"].startswith("inadmissible-")
        }
        inadmissible_targets = {
            target
            for (target, _), category in common.EXTERNAL_SITE_SEMANTIC_AUDIT.items()
            if category in inadmissible_categories
        }
        intrinsic_targets = {
            row["target"]
            for row in self.dependency_payload
            if row["record_id"] in common.DEPENDENCY_INTRINSIC_INADMISSIBLE
        }
        self.assertEqual(
            intrinsic_targets,
            {
                "core::slice::as_mut_ptr",
                "core::slice::as_ptr",
                "core::slice::get_mut",
            },
        )
        inadmissible_targets.update(intrinsic_targets)
        self.assertEqual(len(inadmissible_targets), 34)
        self.assertEqual(
            len(self.scope["selected_targets"]) - len(inadmissible_targets), 28
        )

    def test_contract_capture_keeps_match_and_struct_literal_braces(self) -> None:
        bridge = self.external_sites[
            (
                "core::slice::binary_search",
                "rust_1_96_binary_search_ord_result_bridge",
            )
        ]["contract_text"]
        self.assertIn("match result {", bridge)
        self.assertIn("slice_binary_search_result(seq, value, result)", bridge)
        range_bridge = self.external_sites[
            (
                "core::slice::subslice_range",
                "rust_1_96_subslice_range_some_bridge",
            )
        ]["contract_text"]
        self.assertIn("Some(Range { start, end })", range_bridge)


if __name__ == "__main__":
    unittest.main()
