#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from checker_guards import GuardError, validate_obligation
import replay_target_077
import run_target_077
import target_077
import target_pipeline


class Target077GuardTests(unittest.TestCase):
    def test_both_literal_theorems_pass_the_structural_checker(self) -> None:
        for purpose in target_077.PURPOSES:
            with self.subTest(purpose=purpose):
                text, metadata = target_077.obligation(purpose)
                validate_obligation(text, metadata)
                target_077.validate_target_obligation(text, metadata)

    def test_active_contract_identity_and_all_six_conjuncts_are_bound(self) -> None:
        self.assertEqual(
            target_077.ACTIVE_CONTRACT_SHA256,
            "e570c36bf97546100d3408a95ea9c5f821ba0aed6ebe0e63ef6358d7d713fdaf",
        )
        for fragment in (
            "final(slice)@ == final(ret.0)@ + seq![*final(ret.1)]",
            "final(ret.0)@.len() == index",
            "*final(ret.1) == final(slice)@[index as int]",
            "final(ret.2)@.len() ==",
            "slice_permutation",
            "slice_select_partition_ord",
        ):
            self.assertIn(fragment, target_077.ACTIVE_CONTRACT_TEXT)
        metadata = target_077.obligation_metadata(target_077.PRIMARY)
        self.assertEqual(
            tuple(metadata["active_contract_conjuncts"]),
            target_077.ACTIVE_CONJUNCTS,
        )

    def test_primary_is_general_and_exact_sat_case_is_fixed(self) -> None:
        primary = target_077.obligation_metadata(target_077.PRIMARY)["domain"]
        exact = target_077.obligation_metadata(
            target_077.EXACT_OUTPUT
        )["domain"]
        self.assertFalse(primary["bounded"])
        self.assertEqual(primary["slice_length"], "arbitrary positive integer")
        self.assertEqual(primary["index"], "arbitrary integer in [0, length)")
        self.assertTrue(exact["bounded"])
        self.assertEqual(exact["classification_use"], "fixed-input exact SAT witness")

    def test_only_ts_077_d003_backs_the_boundary(self) -> None:
        metadata = target_077.obligation_metadata(target_077.PRIMARY)
        scope = metadata["boundary_scope"]
        self.assertEqual(
            set(scope["admitted_trust_site_ids"]), {"TS-077-D003"}
        )
        self.assertEqual(
            set(scope["excluded_retained_trust_site_ids"]),
            {"TS-077-D002", "TS-077-E001"},
        )
        self.assertEqual(
            set(scope["context_only_trust_site_ids"]),
            {"TS-077-D001", "TS-077-C001"},
        )
        for field in metadata["boundary_fields"]:
            self.assertEqual(set(field["trust_site_ids"]), {"TS-077-D003"})
            self.assertEqual(field["source_backed_replacement_ids"], [])

    def test_boundary_has_no_answer_or_trace_observation(self) -> None:
        manifest = target_077.boundary_manifest()
        observed = json.dumps(
            manifest["shared_boundary_observations"]
        ).lower()
        for forbidden in (
            "final sequence",
            "permutation",
            "selected output",
            "returned subslice",
            "pivot identity",
            "pivot class",
            "trace",
        ):
            self.assertNotIn(forbidden, observed)
        self.assertEqual(
            set(manifest["source_backed_replacement"]["replaces_trust_site_ids"]),
            {"TS-077-D002", "TS-077-E001"},
        )

    def test_all_required_source_transitions_are_reachable(self) -> None:
        text, metadata = target_077.obligation(target_077.PRIMARY)
        for symbol in target_077.SOURCE_TRANSITIONS:
            self.assertIn(f"(define-fun {symbol}", text)
            self.assertIn(f"({symbol} ", text[text.index("(define-fun TargetDefinition_T"):])
        self.assertEqual(
            set(metadata["source_transition_definitions"]),
            set(target_077.SOURCE_TRANSITIONS),
        )
        required = {
            "BoundsTransition",
            "ZstTransition",
            "MinMaxScanTransition",
            "SwapPermutationTransition",
            "PartitionTransition",
            "RecursiveLoopOrFallbackTransition",
            "FinalReturnedSubsliceTransition",
        }
        replacement = metadata["source_backed_replacements"][0]
        self.assertEqual(set(replacement["symbols"]), required)

    def test_all_summaries_are_derived_from_sequences_and_ord(self) -> None:
        text = target_077.obligation_text(target_077.PRIMARY)
        for fragment in (
            "(IdentityCountThrough sequence length identity)",
            "(ClassCountThrough sequence classes length class)",
            "(LessCountThrough sequence classes length class)",
            "(GreaterCountThrough sequence classes length class)",
            "(= (x_identity_multiplicity x)",
            "(InputIdentityMultiplicity x)",
            "(= (x_class_multiplicity x)",
            "(InputClassMultiplicity x b)",
            "(= (x_less_count x)",
            "(InputLessCounts x b)",
            "(= (s_final_identity_multiplicity s)",
            "(FinalIdentityMultiplicity x s)",
            "(= (s_left_class_multiplicity s)",
            "(FinalLeftClassMultiplicity x b s)",
            "(= (s_right_class_multiplicity s)",
            "(FinalRightClassMultiplicity x b s)",
        ):
            self.assertIn(fragment, text)

    def test_source_transition_or_active_conjunct_deletion_fails_closed(self) -> None:
        text, metadata = target_077.obligation(target_077.PRIMARY)
        target_start = text.index("(define-fun TargetDefinition_T")

        def remove_call(source: str, symbol: str) -> str:
            start = source.index(f"({symbol}", target_start)
            balance = 0
            for end in range(start, len(source)):
                if source[end] == "(":
                    balance += 1
                elif source[end] == ")":
                    balance -= 1
                    if balance == 0:
                        return source[:start] + "true" + source[end + 1 :]
            self.fail(f"unterminated call for {symbol}")

        for symbol in (*target_077.SOURCE_TRANSITIONS, *target_077.ACTIVE_CONJUNCTS):
            with self.subTest(symbol=symbol):
                with self.assertRaises(GuardError):
                    target_077.validate_target_obligation(
                        remove_call(text, symbol), metadata
                    )

    def test_opaque_whole_selection_relation_is_rejected(self) -> None:
        text, metadata = target_077.obligation(target_077.PRIMARY)
        mutated = text.replace(
            "(declare-const x Input)",
            "(declare-fun WholeSelection (Input Boundary Output State) Bool)\n"
            "(declare-const x Input)",
        )
        start = mutated.index("(define-fun TargetDefinition_T")
        end = mutated.index("(define-fun Spec_T", start)
        mutated = (
            mutated[:start]
            + """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (WholeSelection x b y s))
"""
            + mutated[end:]
        )
        changed = copy.deepcopy(metadata)
        changed["declared_functions"] = [
            {
                "symbol": "WholeSelection",
                "role": "source_transition",
                "source_citations": [target_077.SELECT_SOURCE],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(mutated, changed)

    def test_answer_bearing_boundary_roles_and_excluded_backing_are_rejected(
        self,
    ) -> None:
        text, metadata = target_077.obligation(target_077.PRIMARY)
        for role in ("selected_output", "final_permutation", "pivot_trace"):
            with self.subTest(role=role):
                changed = copy.deepcopy(metadata)
                changed["boundary_fields"][1]["role"] = role
                with self.assertRaises(GuardError):
                    validate_obligation(text, changed)
        changed = copy.deepcopy(metadata)
        changed["boundary_fields"][1]["trust_site_ids"] = ["TS-077-D002"]
        with self.assertRaises(GuardError):
            validate_obligation(text, changed)

    def test_solver_results_and_all_sat_models_replay(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for purpose, expected in (
            (target_077.PRIMARY, "unsat\n"),
            (target_077.EXACT_OUTPUT, "sat\n"),
        ):
            with self.subTest(purpose=purpose):
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=target_077.obligation_text(purpose),
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, expected)
                self.assertEqual(process.stderr, "")
        fixed = subprocess.run(
            [str(z3), "-in", "-smt2"],
            input=target_077.fixed_exact_model_text(),
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(fixed.returncode, 0, fixed.stderr)
        self.assertTrue(fixed.stdout.startswith("sat\n"))
        for kind in target_077.PROBE_KINDS:
            with self.subTest(kind=kind):
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=target_077.witness_probe_text(kind),
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertTrue(process.stdout.startswith("sat\n"))
                self.assertEqual(process.stderr, "")
        for kind in target_077.SEMANTIC_REGRESSION_KINDS:
            with self.subTest(semantic_regression=kind):
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=target_077.semantic_regression_probe_text(kind),
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, "unsat\n")
                self.assertEqual(process.stderr, "")

    def test_recursive_source_path_has_semantic_force(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        text = target_077.semantic_regression_probe_text(
            "small_sort_source_reachability"
        )
        call = "    (RecursiveLoopOrFallbackTransition x b y s)\n"
        self.assertEqual(text.count(call), 1)
        process = subprocess.run(
            [str(z3), "-in", "-smt2"],
            input=text.replace(call, "    true\n", 1),
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout, "sat\n")
        self.assertEqual(process.stderr, "")


class Target077WitnessTests(unittest.TestCase):
    def test_positive_and_negative_witnesses_replay(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "witness.json"
            path.write_text(
                json.dumps(target_077.witness_payload(), sort_keys=True) + "\n"
            )
            result = replay_target_077.replay(path)
        self.assertEqual(result["status"], "passed")
        side = result["exact_side_reordering_counterexample"]["observed"]
        self.assertTrue(side["execution1_satisfies_active_contract"])
        self.assertTrue(side["execution2_satisfies_active_contract"])
        self.assertFalse(side["exact_equivalent"])
        self.assertTrue(side["reviewed_selection_equivalent"])
        equal = result["equal_pivot_positive_witness"]["observed"]
        self.assertFalse(equal["pivot_identity_equal"])
        self.assertTrue(equal["pivot_class_equal"])
        self.assertTrue(equal["reviewed_selection_equivalent"])
        self.assertEqual(
            set(result["negative_witnesses"]),
            {
                "foreign_identity",
                "wrong_rank_class",
                "partition_crossing",
                "malformed_range",
                "state_drift",
            },
        )
        for observed in result["negative_witnesses"].values():
            self.assertTrue(observed["baseline_satisfies_active_contract"])
            self.assertFalse(observed["candidate_satisfies_active_contract"])
            self.assertFalse(observed["reviewed_selection_equivalent"])

    def test_boundary_drift_is_not_a_fixed_boundary_witness(self) -> None:
        payload = target_077.witness_payload()
        payload["boundary"]["class_by_identity"].pop("20")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "witness.json"
            path.write_text(json.dumps(payload))
            with self.assertRaises((KeyError, ValueError)):
                replay_target_077.replay(path)


class Target077ScopeTests(unittest.TestCase):
    def test_certified_baseline_and_frozen_selection_scope_are_exact(self) -> None:
        self.assertEqual(len(run_target_077.BASELINE_RESULTS), 24)
        self.assertEqual(len(run_target_077.PRESERVED_ARTIFACT_IDS), 24)
        self.assertEqual(
            set(run_target_077.FROZEN_SELECTION_DIRS),
            {
                "077_core_slice_select_nth_unstable",
                "078_core_slice_select_nth_unstable_by",
                "079_core_slice_select_nth_unstable_by_key",
            },
        )

    def test_result_only_update_preserves_24_rows_and_78_79(self) -> None:
        rows = [
            {
                "target": f"target-{index}",
                "input_order": str(index),
                "exact_output_determinism_status": "not-run",
                "completeness_modulo_reviewed_equivalence_status": "not-run",
            }
            for index in range(62)
        ]
        preserved: dict[tuple[str, str], dict[str, str]] = {}
        for index, (key, status) in enumerate(
            run_target_077.BASELINE_RESULTS.items()
        ):
            rows[index]["target"], rows[index]["input_order"] = key
            rows[index].update(status)
            preserved[key] = status
        selected_index = 24
        rows[selected_index]["target"] = target_077.TARGET
        rows[selected_index]["input_order"] = target_077.INPUT_ORDER
        before = copy.deepcopy(rows)
        updated_csv, updated_json = target_pipeline.apply_crosswalk_result_update(
            rows,
            copy.deepcopy(rows),
            target=target_077.TARGET,
            input_order=target_077.INPUT_ORDER,
            statuses=run_target_077.RESULT_STATUSES,
            preserved_results=preserved,
        )
        self.assertEqual(updated_csv, updated_json)
        for index, (old, new) in enumerate(zip(before, updated_csv)):
            if index == selected_index:
                changed = {
                    key
                    for key in new
                    if old.get(key) != new.get(key)
                }
                self.assertEqual(
                    changed, set(target_pipeline.RESULT_FIELDS)
                )
            else:
                self.assertEqual(new, old)

    def test_verus_model_has_no_trusted_body(self) -> None:
        text = (
            ROOT / "proofs/077_core_slice_select_nth_unstable.rs"
        ).read_text()
        self.assertNotIn("external_body", text)
        for symbol in (
            "source_branch",
            "zst_transition",
            "min_max_transition",
            "swap_transition",
            "partition_transition",
            "recursive_or_fallback_transition",
            "final_subslice_transition",
        ):
            self.assertIn(symbol, text)


if __name__ == "__main__":
    unittest.main()
