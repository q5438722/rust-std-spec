#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import run_target_081_operational_v1 as runner
import target_081_operational_smt_v1 as smt
import target_081_operational_v1 as model


EVIDENCE = ROOT / "evidence/target_081_operational_v1"


class Target081OperationalArtifactsV1Tests(unittest.TestCase):
    def test_result_is_source_complete_additive_and_review_pending(self) -> None:
        result = json.loads((EVIDENCE / "result.json").read_text())
        self.assertEqual(
            result["status"], "engineer-complete-review-pending"
        )
        self.assertTrue(result["source_model_complete"])
        self.assertTrue(result["classification_eligible"])
        self.assertEqual(result["missing_source_phases"], [])
        self.assertEqual(result["unresolved_source_model_phases"], [])
        self.assertEqual(
            set(result["classification"].values()),
            {"conditional-complete"},
        )
        self.assertEqual(
            set(result["certified_baseline_classification"].values()),
            {"conditional-incomplete"},
        )
        self.assertFalse(
            result["certified_baseline_classification_mutated"]
        )
        self.assertEqual(
            result["independent_review"]["status"], "pending"
        )
        self.assertIsNone(result["independent_review"]["verdict"])

    def test_solver_evidence_has_required_sat_and_unsat_results(self) -> None:
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
            {
                name: record["solver"]["solver_result"]
                for name, record in result[
                    "retained_contract_classification_replays"
                ].items()
            },
            {
                "exact-output": "sat",
                "reviewed-equivalence": "sat",
                "total-order-sanity": "unsat",
            },
        )

    def test_source_closure_binds_all_trust_sites_and_no_missing_phase(self) -> None:
        manifest = runner.validate_source_bindings()
        self.assertGreaterEqual(len(manifest["bindings"]), 25)
        self.assertTrue(manifest["source_model_complete"])
        self.assertEqual(manifest["missing_source_phases"], [])
        self.assertEqual(
            manifest["trust_site_dispositions"],
            {
                "TS-081-D001": "context-only-generated-contract-vocabulary",
                "TS-081-D002": (
                    "replaced-by-source-ordering-to-less-adapter"
                ),
                "TS-081-D003": (
                    "replaced-by-accepted-private-source-transitions"
                ),
                "TS-081-D004": (
                    "admitted-total-callback-and-drop-observations"
                ),
                "TS-081-C001": "context-only-direct-call-identity",
                "TS-081-E001": (
                    "replaced-by-accepted-private-source-transitions"
                ),
            },
        )

    def test_boundary_excludes_answers_and_binds_drop_lifecycle(self) -> None:
        boundary = json.loads((EVIDENCE / "boundary_manifest.json").read_text())
        self.assertEqual(
            boundary["admitted_trust_site_ids"], ["TS-081-D004"]
        )
        self.assertTrue(boundary["boundary_narrower_than_target"])
        serialized = json.dumps(boundary["shared_boundary_observations"])
        self.assertIn("Ordering", serialized)
        self.assertIn("Drop", serialized)
        self.assertIn("observable element interior state", serialized)
        self.assertIn(
            "complete element interior-mutation state",
            boundary["externally_observable_state"],
        )
        for forbidden in (
            "selected output",
            "aggregate final state",
            "target execution trace",
        ):
            self.assertNotIn(
                forbidden, json.dumps(boundary["shared_boundary_observations"])
            )

    def test_verus_artifact_is_trusted_free_and_verified(self) -> None:
        source = (
            ROOT
            / "proofs/081_core_slice_sort_unstable_by_operational_v1.rs"
        ).read_text()
        for required in (
            "source_ordering_to_less_adapter",
            "comparator_observation",
            "adapter_evaluates_compare_exactly_once",
            "AcceptedTarget080PrivateTransition",
            "accepted_private_source_transition",
            "source_private_comparator_boundary",
            "observable_element_state",
            "normal_drop_panic_becomes_target_panic",
            "unwind_drop_panic_is_abort",
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
            "fixed_boundary_projection_is_deterministic",
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
        transition = result["verus"]["accepted_private_transition"]
        self.assertEqual(
            transition["model_id"],
            "target-080-operational-v1-rust-1.96-complete",
        )
        self.assertEqual(
            transition["arguments"],
            [
                "SourceInput",
                "SourceConfiguration",
                "source_private_comparator_boundary",
            ],
        )
        self.assertFalse(transition["terminal_result_supplied_as_input"])
        for key in ("source", "accepted_evidence", "accepting_review"):
            artifact = transition[key]
            path = ROOT / artifact["path"]
            self.assertEqual(path.stat().st_size, artifact["bytes"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                artifact["sha256"],
            )
        self.assertEqual(
            result["verus"]["expected_summary"],
            "verification results:: 11 verified, 0 errors",
        )

    def test_path_policy_v6_binds_v5_and_complete_package(self) -> None:
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
        self.assertIn(
            "tools/target_081_operational_v1.py", registered
        )
        self.assertIn(
            "evidence/target_081_operational_v1/result.json", registered
        )
        self.assertNotIn(
            "review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md",
            registered,
        )
        for record in lane["records"]:
            path = ROOT / record["path"]
            with self.subTest(path=record["path"]):
                self.assertEqual(path.stat().st_size, record["bytes"])
                self.assertEqual(
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                    record["sha256"],
                )
        self.assertEqual(
            policy["independent_review_lane"]["status"], "pending"
        )

    def test_preservation_and_additive_crosswalk_are_explicit(self) -> None:
        result = json.loads((EVIDENCE / "result.json").read_text())
        for record in result["preservation"]["protected_trees"].values():
            self.assertEqual(
                record["before_sha256"], record["after_sha256"]
            )
        for record in result["preservation"]["protected_files"].values():
            self.assertEqual(
                record["before_sha256"], record["after_sha256"]
            )
        addendum = json.loads(
            (
                ROOT
                / "crosswalk/target_081_operational_v1_addendum.json"
            ).read_text()
        )
        self.assertFalse(addendum["baseline_row_mutated"])
        self.assertFalse(addendum["target_080_mutated"])
        self.assertEqual(
            set(
                addendum[
                    "certified_baseline_classification"
                ].values()
            ),
            {"conditional-incomplete"},
        )


if __name__ == "__main__":
    unittest.main()
