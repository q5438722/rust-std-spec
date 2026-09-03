#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import checker_guards
import preservation_policy_v3 as preservation
import replay_target_080_operational_v1 as replay
import run_target_080_operational_v1 as runner
import target_080_operational_smt_v1 as smt
import target_080_operational_v1 as model
import target_080_operational_witness_v1 as witnesses


EVIDENCE = ROOT / "evidence/target_080_operational_v1"


class Target080OperationalArtifactsV1Tests(unittest.TestCase):
    def run_z3(self, text: str, expected: str) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        process = subprocess.run(
            [str(z3), "-in", "-smt2"],
            input=text,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout, expected + "\n")
        self.assertEqual(process.stderr, "")

    def test_correspondence_obligations_are_direct_unsat(self) -> None:
        for purpose in smt.PURPOSES:
            with self.subTest(purpose=purpose):
                text = smt.obligation_text(purpose)
                metadata = smt.obligation_metadata(purpose)
                smt.validate_obligation(text, metadata)
                self.assertEqual(
                    metadata["domain"][
                        "retained_source_execution_count"
                    ],
                    28,
                )
                self.assertEqual(
                    metadata["domain"]["retained_callback_count"],
                    2920,
                )
                self.assertEqual(
                    metadata["domain"]["formal_transition"],
                    "ground source-derived callback/swap/write replay",
                )
                self.assertGreater(
                    metadata["domain"][
                        "normalized_source_operation_count"
                    ],
                    metadata["domain"]["retained_callback_count"],
                )
                self.run_z3(text, "unsat")

    def test_all_source_force_probes_are_sat(self) -> None:
        self.assertGreaterEqual(len(smt.PROBE_KINDS), 20)
        self.run_z3(smt.nonvacuity_text(), "sat")
        for kind in smt.PROBE_KINDS:
            with self.subTest(kind=kind):
                self.run_z3(smt.probe_text(kind), "sat")

    def test_all_semantic_mutations_make_correspondence_sat(self) -> None:
        required = {
            "threshold-dispatch",
            "comparison-operands",
            "callback-next-state",
            "descending-reversal",
            "pivot-selection",
            "partition-behavior",
            "recursive-left-window",
            "iterative-right-window",
            "imbalance-limit",
            "small-sort-selection",
            "heap-child-selection",
            "heap-swap",
            "copy-on-drop-restoration",
            "gap-guard-restoration",
            "panic-unwind",
        }
        self.assertEqual(set(smt.MUTATION_PROBES), required)
        forcing = witnesses.forcing_specs()
        self.assertEqual(set(forcing), required | {"nonvacuity"})
        self.assertEqual(
            len(witnesses.witness_payload()["cases"]), 28
        )
        self.assertLessEqual(
            max(len(spec["sequence"]) for spec in forcing.values()),
            26,
        )
        for kind in smt.MUTATION_PROBES:
            with self.subTest(kind=kind):
                text = smt.mutation_probe_text(kind)
                self.assertIn("; formal source input case=forcing-", text)
                self.assertIn("(define-fun formal_state_0", text)
                self.assertNotIn("(declare-fun Source", text)
                self.run_z3(text, "sat")

    def test_source_transition_deletion_fails_closed(self) -> None:
        text = smt.obligation_text()
        metadata = smt.obligation_metadata()
        defined = checker_guards.defined_function_names(text)
        self.assertTrue(set(smt.SOURCE_TRANSITIONS) <= defined)
        self.assertIn("ExactSiftDownParent", defined)
        self.assertIn("ExactQuickSortPartition", defined)
        for symbol in smt.SOURCE_TRANSITIONS:
            with self.subTest(symbol=symbol):
                changed = text.replace(symbol, f"Deleted{symbol}", 1)
                changed_metadata = dict(metadata)
                changed_metadata["sha256"] = hashlib.sha256(
                    changed.encode()
                ).hexdigest()
                with self.assertRaises(ValueError):
                    smt.validate_obligation(changed, changed_metadata)

    def test_formal_machine_is_source_initialized_and_boundary_driven(
        self,
    ) -> None:
        text = smt.obligation_text()
        metadata = smt.obligation_metadata()
        self.assertEqual(
            text.count("; formal source input case="),
            metadata["domain"]["retained_source_execution_count"],
        )
        self.assertEqual(
            text.count("(define-fun source_initial_"),
            metadata["domain"]["retained_source_execution_count"],
        )
        self.assertEqual(
            text.count("(b_initial_state boundary_"),
            metadata["domain"]["retained_source_execution_count"],
        )
        self.assertEqual(
            text.count("; source callback case="),
            metadata["domain"]["retained_callback_count"],
        )
        self.assertGreater(metadata["domain"]["retained_callback_count"], 0)
        self.assertIn("(FormalCallback formal_", text)
        self.assertIn("(FormalSwap formal_", text)
        self.assertIn("(FormalWriteFromOrigin formal_", text)
        self.assertIn("(select (m_origin formal_", text)
        self.assertNotIn("(m_result", text)
        for boundary_call in (
            "(BoundaryOrdering b state left right)",
            "(BoundaryNextState b (m_callback machine) left right)",
            "(BoundaryPanics b (m_callback machine) left right)",
        ):
            self.assertIn(boundary_call, text)

    def test_smt_boundary_excludes_answers_and_traces(self) -> None:
        text = smt.obligation_text()
        block = text[
            text.index("; Boundary_T") : text.index(
                "(declare-datatypes"
            )
        ].lower()
        for forbidden in (
            "pivot",
            "swap",
            "output",
            "final_sequence",
            "permutation",
            "trace",
        ):
            self.assertNotIn(forbidden, block)
        for required in (
            "b_ordering",
            "b_contract_ordering",
            "b_next_state",
            "b_panics",
        ):
            self.assertIn(required, block)

    def test_retained_witness_replays_independently(self) -> None:
        result = replay.replay(EVIDENCE / "witness.json")
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["witness_count"], 28)
        self.assertTrue(result["field_complete_correspondence"])
        self.assertTrue(
            all(
                case["permutation_retained"]
                for case in result["cases"].values()
            )
        )

    def test_result_is_complete_additive_and_solver_derived(self) -> None:
        result = json.loads((EVIDENCE / "result.json").read_text())
        self.assertEqual(
            result["status"], "engineer-complete-review-pending"
        )
        self.assertEqual(result["target"], model.TARGET)
        self.assertTrue(result["source_model_complete"])
        self.assertTrue(result["classification_eligible"])
        self.assertEqual(result["missing_source_phases"], [])
        self.assertEqual(result["unresolved_source_model_phases"], [])
        self.assertFalse(
            result["certified_baseline_classification_mutated"]
        )
        self.assertEqual(
            set(result["classification"].values()),
            {"conditional-complete"},
        )
        for obligation in result["obligations"].values():
            self.assertEqual(
                obligation["solver"]["solver_result"], "unsat"
            )
        for probe in result["semantic_force_probes"].values():
            self.assertEqual(probe["solver"]["solver_result"], "sat")
        for mutation in result[
            "semantic_mutation_regressions"
        ].values():
            self.assertEqual(mutation["solver"]["solver_result"], "sat")
        self.assertEqual(
            result["independent_review"]["status"], "pending"
        )
        self.assertIsNone(result["independent_review"]["verdict"])
        self.assertEqual(
            result["independent_review"][
                "separate_preservation_policy"
            ],
            "preservation/path_policy_v5.json",
        )

    def test_verus_artifact_is_trusted_free_and_mutation_sensitive(self) -> None:
        source = (
            ROOT
            / "proofs/080_core_slice_sort_unstable_operational_v1.rs"
        ).read_text()
        for required in (
            "sequence: Seq<int>",
            "pub ghost struct ExactOperationalResult",
            "pub ghost struct RefinedOperationalResult",
            "pub open spec fn admissible_boundary",
            "pub open spec fn exact_source_result_is_terminal",
            "pub open spec fn checked_exact_result_projection",
            "pub proof fn checked_refinement_preserves_every_exact_field",
            "pub proof fn implementation_ordering_projects_exactly_to_contract",
            "pub proof fn callback_transitions_are_total_functions",
        ):
            self.assertIn(required, source)
        for forbidden in ("external_body", "assume(", "admit(", "axiom"):
            self.assertNotIn(forbidden, source)
        result = json.loads((EVIDENCE / "result.json").read_text())
        self.assertEqual(
            result["verus"]["expected_summary"],
            "verification results:: 5 verified, 0 errors",
        )
        self.assertTrue(
            result["verus"]["negative_projection_mutation"]["rejected"]
        )
        self.assertNotEqual(
            result["verus"]["negative_projection_mutation"][
                "verification"
            ]["exit_code"],
            0,
        )

    def test_source_closure_and_path_policy_v4_are_byte_bound(self) -> None:
        manifest = runner.validate_source_bindings()
        self.assertEqual(len(manifest["bindings"]), 21)
        self.assertTrue(manifest["source_model_complete"])
        self.assertEqual(manifest["missing_source_phases"], [])
        self.assertEqual(
            manifest["trust_site_dispositions"]["TS-080-D002"],
            "replaced-by-bound-source-transitions",
        )
        lifecycle = preservation.target_080_lifecycle()
        self.assertEqual(lifecycle["status"], "review-accepted")
        archive = lifecycle["archive_resolution"]
        self.assertIsNotNone(archive)
        policy_record = archive["accepted_v4_archive"]
        policy_path = ROOT / policy_record["path"]
        self.assertEqual(policy_path.stat().st_size, policy_record["bytes"])
        self.assertEqual(
            hashlib.sha256(policy_path.read_bytes()).hexdigest(),
            policy_record["sha256"],
        )
        policy = json.loads(policy_path.read_text())
        parent = ROOT / policy["parent_policy"]["path"]
        self.assertEqual(
            parent.stat().st_size, policy["parent_policy"]["bytes"]
        )
        self.assertEqual(
            hashlib.sha256(parent.read_bytes()).hexdigest(),
            policy["parent_policy"]["sha256"],
        )
        lane = policy["registered_post_v3_additions"][
            "target_080_operational_v1"
        ]
        self.assertEqual(lane["file_count"], len(lane["records"]))
        self.assertGreater(lane["file_count"], 100)
        self.assertEqual(
            len(archive["record_version_mappings"]), 5
        )
        self.assertNotIn(
            "review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md",
            {record["path"] for record in lane["records"]},
        )
        registered_paths = {
            record["path"] for record in lane["records"]
        }
        self.assertIn("tools/checker_guards.py", registered_paths)
        self.assertIn(
            "tools/target_080_exact_smt_v1.py", registered_paths
        )
        self.assertEqual(
            policy["independent_review_lane"]["status"], "pending"
        )
        self.assertEqual(
            policy["independent_review_lane"]["expected_policy_path"],
            "preservation/path_policy_v5.json",
        )

    def test_crosswalk_is_additive_and_baseline_is_preserved(self) -> None:
        addendum = json.loads(
            (
                ROOT
                / "crosswalk/target_080_operational_v1_addendum.json"
            ).read_text()
        )
        self.assertEqual(addendum["target"], model.TARGET)
        self.assertFalse(addendum["baseline_row_mutated"])
        self.assertFalse(addendum["target_081_mutated"])
        self.assertEqual(
            addendum["certified_baseline_classification"],
            {
                "exact_output_determinism_status": (
                    "conditional-incomplete"
                ),
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            },
        )
        result = json.loads((EVIDENCE / "result.json").read_text())
        for record in result["preservation"]["protected_trees"].values():
            self.assertEqual(
                record["before_sha256"], record["after_sha256"]
            )
        for record in result["preservation"]["protected_files"].values():
            self.assertEqual(
                record["before_sha256"], record["after_sha256"]
            )


if __name__ == "__main__":
    unittest.main()
