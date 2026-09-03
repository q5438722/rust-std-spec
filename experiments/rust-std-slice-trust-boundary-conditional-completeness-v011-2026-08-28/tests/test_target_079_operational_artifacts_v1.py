#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import replay_target_079_operational_v1 as replay
import target_078_exact_smt_v1 as accepted_exact
import target_079_exact_smt_v1 as exact
import target_079_operational_smt_v1 as smt
import target_079_operational_v1 as model


EVIDENCE = ROOT / "evidence/target_079_operational_v1"
RESULT = EVIDENCE / "result.json"


def run_z3(text: str) -> tuple[int, str, str]:
    z3 = shutil.which("z3")
    if z3 is None:
        raise unittest.SkipTest("z3 is unavailable")
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "query.smt2"
        path.write_text(text)
        process = subprocess.run(
            [z3, "-smt2", str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
    return process.returncode, process.stdout, process.stderr


class Target079OperationalFormalTests(unittest.TestCase):
    def test_exact_state_is_imported_then_only_abort_extended(self) -> None:
        accepted = accepted_exact.definitions_text()
        adapted = exact.definitions_text()
        self.assertEqual(
            exact.ACCEPTED_DEFINITIONS_SHA256,
            __import__("hashlib").sha256(accepted.encode()).hexdigest(),
        )
        self.assertIn("(define-fun ExactRunState", adapted)
        self.assertIn("(e_aborted Bool)", adapted)
        self.assertIn("(BoundaryAborts b", adapted)
        self.assertEqual(
            adapted.count("(ite (e_aborted"),
            exact.ACTIVE_CLEANUP_GUARD_COUNT,
        )
        self.assertEqual(
            adapted.count("(mkExactState") - 1,
            exact.EXACT_STATE_CONSTRUCTOR_COUNT,
        )
        self.assertNotIn("AbortAwareCopyOnDrop", smt.obligation_text())
        self.assertNotIn("AbortAwareGapGuard", smt.obligation_text())

    def test_both_obligations_are_literal_six_conjunct_queries(
        self,
    ) -> None:
        for purpose in smt.PURPOSES:
            with self.subTest(purpose=purpose):
                text = smt.obligation_text(purpose)
                metadata = smt.obligation_metadata(purpose)
                smt.validate_obligation(text, metadata)
                self.assertEqual(metadata["literal_conjunct_count"], 6)
                self.assertEqual(
                    tuple(metadata["active_contract_conjuncts"]),
                    model.ACTIVE_CONJUNCTS,
                )
                self.assertEqual(
                    text.count("(assert (TargetDefinition_T x b c"),
                    2,
                )
        exact_text = smt.obligation_text(smt.EXACT)
        full_text = smt.obligation_text(smt.FULL)
        self.assertNotEqual(exact_text, full_text)
        self.assertIn(
            "(assert (not (ExactPrincipalReturn y1 y2)))",
            exact_text,
        )
        self.assertIn(
            "(assert (not (ExactPrincipalReturnAndFinalState "
            "y1 s1 y2 s2)))",
            full_text,
        )

    def test_boundary_has_total_key_ord_drop_maps_and_owned_identity(
        self,
    ) -> None:
        text = smt.obligation_text()
        for selector in (
            "b_key_result",
            "b_key_next_state",
            "b_key_panics",
            "b_ord_lt_result",
            "b_ord_lt_next_state",
            "b_ord_lt_panics",
            "b_drop_next_state",
            "b_drop_panics",
        ):
            self.assertIn(selector, text)
        for selector in (
            "owned_creation_state",
            "owned_slot",
            "owned_source_identity",
            "owned_key_identity",
        ):
            self.assertIn(selector, text)
        self.assertNotIn("b_realized_calls", text)
        self.assertNotIn("b_drop_schedule", text)

    def test_direct_obligations_and_nonvacuity(self) -> None:
        for purpose in smt.PURPOSES:
            with self.subTest(purpose=purpose):
                code, stdout, stderr = run_z3(
                    smt.obligation_text(purpose)
                )
                self.assertEqual(code, 0)
                self.assertEqual(stdout, "unsat\n")
                self.assertEqual(stderr, "")
        nonvacuity = smt.nonvacuity_text()
        self.assertIn(
            "(assert (TargetDefinition_T x normal_b c y s))",
            nonvacuity,
        )
        self.assertIn("(assert (Spec_T x normal_b y s))", nonvacuity)
        self.assertIn("(mkInput\n    4\n    1", nonvacuity)
        self.assertIn("    false))", nonvacuity)
        code, stdout, stderr = run_z3(nonvacuity)
        self.assertEqual((code, stdout, stderr), (0, "sat\n", ""))

    def test_selection_force_and_mutation_probes_are_target_specific(
        self,
    ) -> None:
        self.assertEqual(
            set(smt.SELECTION_PHASE_COVERAGE),
            set(model.selection.SOURCE_PHASES),
        )
        self.assertEqual(
            set(smt.PARTITION_KERNEL_PROBES.values())
            <= set(smt.SELECTION_PROBE_KINDS),
            True,
        )
        for kind in smt.SELECTION_PROBE_KINDS:
            with self.subTest(force_probe=kind):
                text = smt.selection_probe_text(kind)
                self.assertIn(
                    f"; Target: {model.TARGET}",
                    text,
                )
                self.assertIn(
                    f"Target-079 selection force probe: {kind}",
                    text,
                )
                self.assertIn("AdapterTransition", text)
                self.assertIn("(e_aborted Bool)", text)
                self.assertNotIn(
                    "read-only reuse of accepted target-078 selection probe",
                    text,
                )
                code, stdout, stderr = run_z3(text)
                self.assertEqual(
                    (code, stdout, stderr), (0, "sat\n", "")
                )
            with self.subTest(selection_mutation=kind):
                mutation = smt.selection_mutation_probe_text(kind)
                self.assertIn(
                    f"Target-079 selection mutation probe: {kind}",
                    mutation,
                )
                code, stdout, stderr = run_z3(mutation)
                self.assertEqual(
                    (code, stdout, stderr), (0, "unsat\n", "")
                )

    def test_adapter_force_and_mutation_probes(self) -> None:
        for kind in smt.ADAPTER_PROBE_KINDS:
            with self.subTest(probe=kind):
                code, stdout, stderr = run_z3(
                    smt.adapter_probe_text(kind)
                )
                self.assertEqual((code, stdout, stderr), (0, "sat\n", ""))
        for kind in smt.ADAPTER_MUTATION_PROBES:
            with self.subTest(mutation=kind):
                code, stdout, stderr = run_z3(
                    smt.adapter_mutation_probe_text(kind)
                )
                self.assertEqual(
                    (code, stdout, stderr), (0, "unsat\n", "")
                )

    def test_exact_cleanup_and_source_correspondence_regressions(
        self,
    ) -> None:
        queries = {
            smt.LENGTH_17_CORRESPONDENCE: (
                smt.length_17_correspondence_text()
            ),
            **{
                kind: smt.exact_cleanup_regression_text(kind)
                for kind in smt.EXACT_CLEANUP_REGRESSIONS
            },
        }
        for name, text in queries.items():
            with self.subTest(regression=name):
                code, stdout, stderr = run_z3(text)
                self.assertEqual(
                    (code, stdout, stderr), (0, "unsat\n", "")
                )


class Target079OperationalArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not RESULT.is_file():
            raise AssertionError(
                "run tools/run_target_079_operational_v1.py first"
            )
        cls.result = json.loads(RESULT.read_text())

    def test_result_is_additive_conditional_complete(self) -> None:
        self.assertEqual(
            self.result["classification"],
            {
                "exact_output_determinism_status": (
                    "conditional-complete"
                ),
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            },
        )
        self.assertTrue(self.result["source_model_complete"])
        self.assertEqual(
            self.result["unresolved_source_model_phases"], []
        )
        self.assertEqual(self.result["stage_transition"], "disabled")

    def test_retained_solver_outputs_are_exact(self) -> None:
        for evidence in self.result["obligations"].values():
            self.assertEqual(
                evidence["solver"]["solver_result"], "unsat"
            )
        self.assertEqual(
            self.result["nonvacuity"]["solver"]["solver_result"],
            "sat",
        )
        for family in self.result["semantic_force_probes"].values():
            self.assertTrue(family)
            self.assertTrue(
                all(
                    record["solver"]["solver_result"] == "sat"
                    for record in family.values()
                )
            )
        for family in self.result[
            "semantic_mutation_regressions"
        ].values():
            self.assertTrue(family)
            self.assertTrue(
                all(
                    record["solver"]["solver_result"] == "unsat"
                    for record in family.values()
                )
            )

    def test_probe_evidence_contains_only_current_target_matrix(
        self,
    ) -> None:
        families = {
            "probe_selection_": smt.SELECTION_PROBE_KINDS,
            "mutation_selection_": smt.SELECTION_MUTATION_PROBES,
            "probe_adapter_": smt.ADAPTER_PROBE_KINDS,
            "mutation_adapter_": smt.ADAPTER_MUTATION_PROBES,
        }
        for prefix, kinds in families.items():
            with self.subTest(prefix=prefix):
                expected = {
                    name
                    for kind in kinds
                    for name in (
                        f"{prefix}{kind}",
                        f"{prefix}{kind}.smt2",
                    )
                }
                actual = {
                    path.name
                    for path in EVIDENCE.iterdir()
                    if path.name.startswith(prefix)
                }
                self.assertEqual(actual, expected)

    def test_ground_truth_has_ten_durable_replays(self) -> None:
        manifest = json.loads(
            (EVIDENCE / "ground_truth/manifest.json").read_text()
        )
        self.assertEqual(len(manifest["scenarios"]), 10)
        self.assertIn(
            "ord-lt-panic-left-drop-panic",
            manifest["scenarios"],
        )
        for scenario, record in manifest["scenarios"].items():
            command = (
                "python3 tools/run_target_079_ground_truth.py "
                f"--check-scenario {scenario}"
            )
            self.assertEqual(record["replay_command"], command)
            self.assertEqual(
                (
                    EVIDENCE
                    / "ground_truth"
                    / scenario
                    / "command.txt"
                ).read_text(),
                command + "\n",
            )

    def test_witness_replays_independently(self) -> None:
        result = replay.replay(EVIDENCE / "witness.json")
        self.assertEqual(result["status"], "passed")
        self.assertTrue(result["ordinary_panic_restored"])
        self.assertTrue(result["abort_retained_interrupted_state"])
        self.assertTrue(result["missing_cleanup_path_replayed"])

    def test_verus_is_trusted_free_and_field_sensitive(self) -> None:
        proof = (EVIDENCE / "verus/selection_model.rs").read_text()
        for forbidden in ("external_body", "assume(", "admit(", "axiom"):
            self.assertNotIn(forbidden, proof)
        self.assertEqual(
            self.result["verus"]["expected_summary"],
            "verification results:: 7 verified, 0 errors",
        )
        self.assertEqual(
            self.result["verus"]["verification"]["exit_code"], 0
        )
        self.assertNotEqual(
            self.result["verus"][
                "negative_sequence_projection_mutation"
            ]["exit_code"],
            0,
        )

    def test_crosswalk_is_additive_and_baseline_is_unchanged(self) -> None:
        addendum = json.loads(
            (
                ROOT
                / "crosswalk/target_079_operational_v1_addendum.json"
            ).read_text()
        )
        self.assertFalse(addendum["baseline_row_mutated"])
        self.assertEqual(
            addendum["additive_classification"],
            self.result["classification"],
        )
        baseline_rows = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        row = next(
            item for item in baseline_rows if item["input_order"] == "79"
        )
        self.assertEqual(
            row["exact_output_determinism_status"],
            "missing-source-backed-model",
        )
        self.assertEqual(
            row[
                "completeness_modulo_reviewed_equivalence_status"
            ],
            "missing-source-backed-model",
        )

    def test_every_protected_digest_is_preserved(self) -> None:
        preservation = self.result["preservation"]
        for family in ("protected_trees", "protected_files"):
            for record in preservation[family].values():
                self.assertEqual(
                    record["before_sha256"], record["after_sha256"]
                )
        self.assertTrue(
            preservation["accepted_target_078_unchanged"]
        )
        self.assertTrue(preservation["pipeline_state_unchanged"])


if __name__ == "__main__":
    unittest.main()
