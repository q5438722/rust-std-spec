#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import preservation_policy_v8 as policy
import run_target_082_operational_v1 as runner
import target_082_operational_smt_v1 as smt


EVIDENCE = ROOT / "evidence/target_082_operational_v1"


class Target082OperationalArtifactsV1Tests(unittest.TestCase):
    def test_result_is_additive_complete_and_review_pending(self) -> None:
        result = json.loads((EVIDENCE / "result.json").read_text())
        self.assertEqual(
            result["status"], "engineer-complete-review-pending"
        )
        self.assertTrue(result["source_model_complete"])
        self.assertTrue(result["classification_eligible"])
        self.assertEqual(result["missing_source_phases"], [])
        self.assertEqual(
            set(result["classification"].values()),
            {"conditional-complete"},
        )
        self.assertEqual(
            result["certified_baseline_classification"],
            runner.BASELINE_CLASSIFICATION,
        )
        self.assertFalse(
            result["certified_baseline_classification_mutated"]
        )
        self.assertEqual(
            result["independent_review"]["status"], "pending"
        )
        self.assertIsNone(result["independent_review"]["verdict"])

    def test_source_bindings_cover_authority_models_and_all_trust_sites(
        self,
    ) -> None:
        manifest = runner.validate_source_bindings()
        self.assertGreaterEqual(len(manifest["bindings"]), 35)
        self.assertEqual(manifest["missing_source_phases"], [])
        self.assertEqual(
            set(manifest["trust_site_dispositions"]),
            {
                "TS-082-D001",
                "TS-082-D002",
                "TS-082-D003",
                "TS-082-D004",
                "TS-082-C001",
                "TS-082-E001",
            },
        )
        roles = {record["role"] for record in manifest["bindings"]}
        for required in (
            "active-contract-source-doc-authority",
            "implementation-proof-harness",
            "implementation-proof-transformation-manifest",
            "implementation-proof-dependency-manifest",
            "accepted-private-primary-transition",
            "accepted-private-independent-transition",
            "accepted-key-ord-drop-lifecycle",
            "accepted-interior-and-panic-before-result-treatment",
            "fresh-rust-mir",
        ):
            self.assertIn(required, roles)

    def test_ground_truth_is_fresh_rust_196_mir_and_process_evidence(
        self,
    ) -> None:
        result = json.loads((EVIDENCE / "result.json").read_text())
        ground = result["ground_truth"]
        self.assertEqual(ground["scenario_count"], 14)
        self.assertIn("rustc 1.96.0", ground["toolchain"])
        manifest = json.loads(
            (EVIDENCE / "ground_truth/manifest.json").read_text()
        )
        self.assertIn(
            "ord-lt-panic-right-drop-double-panic",
            manifest["scenarios"],
        )
        self.assertIn(
            "key-panic-f-drop-double-panic",
            manifest["scenarios"],
        )
        mir = (EVIDENCE / "ground_truth/probe.mir").read_text()
        self.assertIn("sort_unstable_by_key", mir)
        self.assertIn("drop(_", mir)

    def test_solver_evidence_has_exact_required_results(self) -> None:
        result = json.loads((EVIDENCE / "result.json").read_text())
        self.assertEqual(
            {
                purpose: record["solver"]["solver_result"]
                for purpose, record in result["obligations"].items()
            },
            {purpose: "unsat" for purpose in smt.PURPOSES},
        )
        self.assertEqual(result["nonvacuity"]["solver"]["solver_result"], "sat")
        self.assertEqual(
            set(result["branch_force_probes"]), set(smt.PROBE_KINDS)
        )
        self.assertTrue(
            all(
                record["solver"]["solver_result"] == "sat"
                for record in result["branch_force_probes"].values()
            )
        )
        self.assertEqual(
            set(result["semantic_mutation_regressions"]),
            set(smt.MUTATION_KINDS),
        )
        self.assertTrue(
            all(
                record["solver"]["solver_result"] == "sat"
                for record in result[
                    "semantic_mutation_regressions"
                ].values()
            )
        )
        self.assertEqual(
            set(result["correspondence_mutation_regressions"]),
            set(smt.CORRESPONDENCE_MUTATION_KINDS),
        )
        self.assertTrue(
            all(
                record["mutated_side"] == "source-only"
                and record["solver"]["solver_result"] == "sat"
                for record in result[
                    "correspondence_mutation_regressions"
                ].values()
            )
        )
        composition = result[
            "abort_preserving_composition_regressions"
        ]
        self.assertEqual(
            {
                name: record["solver"]["solver_result"]
                for name, record in composition.items()
            },
            smt.COMPOSITION_REGRESSION_EXPECTATIONS,
        )
        retained = result["retained_contract_classification_replays"]
        self.assertEqual(
            retained["equal-key-exact-output-counterexample"]["solver"][
                "solver_result"
            ],
            "sat",
        )
        self.assertEqual(
            retained[
                "reviewed-equivalence-total-order-projection"
            ]["solver"]["solver_result"],
            "unsat",
        )

    def test_verus_model_is_trusted_free_and_verified(self) -> None:
        source = runner.SOURCE_PROOF.read_text()
        for required in (
            "source_key_ord_drop_adapter",
            "cleanup_two_owned_keys",
            "AcceptedTarget080PrivateTransition",
            "accepted_private_source_transition",
            "fixed_boundary_accepted_transition_is_deterministic",
            "first.apply == second.apply",
        ):
            self.assertIn(required, source)
        for forbidden in (
            "external_body",
            "assume(",
            "admit(",
            "axiom",
            "precomputed_terminal",
        ):
            self.assertNotIn(forbidden, source)
        result = json.loads((EVIDENCE / "result.json").read_text())
        self.assertTrue(result["verus"]["trusted_free"])
        self.assertTrue(
            result["verus"]["accepted_private_transition_applied"]
        )
        self.assertFalse(
            result["verus"]["raw_private_terminal_result_parameter"]
        )
        self.assertEqual(
            result["verus"]["expected_summary"],
            "verification results:: 12 verified, 0 errors",
        )

    def test_v8_registers_package_and_archival_replacements(self) -> None:
        validated = policy.validate_policy()
        records = {
            record["path"]: record
            for record in validated["registered_records"]
        }
        self.assertIn(
            "evidence/target_082_operational_v1/result.json", records
        )
        self.assertIn(
            "tools/target_082_operational_v1.py", records
        )
        self.assertIn(
            "crosswalk/target_082_operational_v1_addendum.json",
            records,
        )
        self.assertEqual(
            set(
                validated["validated_v6"][
                    "v8_record_version_mappings"
                ][index]["logical_record"]["path"]
                for index in range(
                    len(
                        validated["validated_v6"][
                            "v8_record_version_mappings"
                        ]
                    )
                )
            ),
            set(policy.ARCHIVE_MAPPINGS),
        )
        for record in records.values():
            path = ROOT / record["path"]
            self.assertEqual(path.stat().st_size, record["bytes"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                record["sha256"],
            )

    def test_certified_projection_and_prior_policies_are_unchanged(
        self,
    ) -> None:
        result = json.loads((EVIDENCE / "result.json").read_text())
        preservation = result["preservation"]
        self.assertTrue(
            preservation["certified_projection_62_rows_unchanged"]
        )
        self.assertTrue(
            preservation["operational_v2_overlay_counts_unchanged"]
        )
        self.assertTrue(
            preservation["policies_v1_through_v7_unchanged"]
        )
        for records in (
            preservation["protected_trees"],
            preservation["protected_files"],
        ):
            self.assertTrue(
                all(
                    record["before_sha256"]
                    == record["after_sha256"]
                    for record in records.values()
                )
            )


if __name__ == "__main__":
    unittest.main()
