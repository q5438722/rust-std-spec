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
import replay_target_052
import target_052


class Target052GuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text, self.metadata = target_052.obligation(target_052.PRIMARY)

    def assert_target_rejected(
        self,
        text: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        with self.assertRaises(GuardError):
            target_052.validate_target_obligation(
                text if text is not None else self.text,
                metadata if metadata is not None else self.metadata,
            )

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for purpose in target_052.PURPOSES:
            with self.subTest(purpose=purpose):
                text, metadata = target_052.obligation(purpose)
                validate_obligation(text, metadata)
                target_052.validate_target_obligation(text, metadata)

    def test_active_contract_identity_is_exact(self) -> None:
        self.assertEqual(
            target_052.ACTIVE_CONTRACT_SHA256,
            "98e2ff139533e1b36cd1ecef3a408b5045f5780bf76ff9a04f2b8f34879e368b",
        )
        self.assertIn(
            "requires slice_disjoint_indices_valid",
            target_052.ACTIVE_CONTRACT_TEXT,
        )
        self.assertIn(
            "ensures final(slice)@.len() == old(slice)@.len()",
            target_052.ACTIVE_CONTRACT_TEXT,
        )
        self.assertNotIn("ret.", target_052.ACTIVE_CONTRACT_TEXT)

    def test_answer_bearing_retained_sites_are_replaced_not_renamed(self) -> None:
        manifest = target_052.boundary_manifest()
        excluded = {
            item["trust_site_id"] for item in manifest["excluded_retained_sites"]
        }
        self.assertEqual(
            excluded, set(target_052.EXCLUDED_RETAINED_TRUST_SITES)
        )
        admitted = set(manifest["admitted_boundary_trust_site_ids"])
        self.assertTrue(excluded.isdisjoint(admitted))
        source = json.dumps(
            manifest["deterministic_source_semantics"], sort_keys=True
        )
        for required in (
            "usize Clone",
            "SliceIndex<usize>::get_unchecked_mut",
            "two-slot MaybeUninit write loop and assume_init",
            "preserves slot 0",
        ):
            self.assertIn(required, source)

    def test_boundary_excludes_outputs_state_and_trace(self) -> None:
        manifest = target_052.boundary_manifest()
        serialized = json.dumps(
            manifest["shared_boundary_observations"], sort_keys=True
        )
        for forbidden in (
            "returned borrow",
            "resulting state",
            "canonical answer",
            "initialization result",
            "execution trace",
        ):
            self.assertNotIn(forbidden, serialized)

    def test_output_bearing_boundary_is_rejected(self) -> None:
        text = self.text.replace(
            "      (b_frame_token Int)))))",
            "      (b_frame_token Int)\n"
            "      (b_selected_ref0 Int)))))",
        ).replace(
            "       (= (y_array_length y) (ReturnedArrayLength x))",
            "       (= (y_array_length y) (ReturnedArrayLength x))\n"
            "       (= (y_ref0_index y) (b_selected_ref0 b))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_selected_ref0",
                "role": "source_helper_observation",
                "source_citations": [target_052.TARGET_SOURCE_REFERENCE],
                "trust_site_ids": ["TS-052-D004", "TS-052-E001"],
            }
        )
        self.assert_target_rejected(text=text, metadata=metadata)

    def test_final_state_bearing_boundary_is_rejected(self) -> None:
        text = self.text.replace(
            "      (b_frame_token Int)))))",
            "      (b_frame_token Int)\n"
            "      (b_final_value0 Int)))))",
        ).replace(
            "       (= (s_length s) (PreservedSliceLength x))",
            "       (= (s_length s) (PreservedSliceLength x))\n"
            "       (= (s_value0 s) (b_final_value0 b))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_final_value0",
                "role": "source_helper_observation",
                "source_citations": [target_052.TARGET_SOURCE_REFERENCE],
                "trust_site_ids": ["TS-052-D004", "TS-052-E001"],
            }
        )
        self.assert_target_rejected(text=text, metadata=metadata)

    def test_opaque_validity_relation_is_rejected(self) -> None:
        original = """\
(define-fun IndicesValid ((x Input)) Bool
  (and (IndexInBounds x (x_index0 x))
       (IndexInBounds x (x_index1 x))
       (not (= (x_index0 x) (x_index1 x)))))"""
        self.assertIn(original, self.text)
        self.assert_target_rejected(
            text=self.text.replace(
                original,
                "(declare-fun IndicesValid (Input) Bool)",
            )
        )

    def test_canonical_answer_injection_is_rejected(self) -> None:
        text = self.text.replace(
            "       (ReturnedBorrowArrayWellFormed x y)\n",
            "       (ReturnedBorrowArrayWellFormed x y)\n"
            "       (CanonicalBorrowArrayConstructed x y)\n",
        )
        self.assert_target_rejected(text=text)

    def test_invalid_or_overlapping_returns_cannot_be_enabled(self) -> None:
        for original in (
            "(IndexInBounds x index)",
            "(not (= (y_ref0_index y) (y_ref1_index y)))",
        ):
            with self.subTest(original=original):
                self.assertIn(original, self.text)
                self.assert_target_rejected(
                    text=self.text.replace(original, "true", 1)
                )

    def test_source_clone_and_storage_mutations_are_rejected(self) -> None:
        mutations = {
            """\
(define-fun ClonedIndex0 ((x Input)) Int
  (x_index0 x))""": """\
(define-fun ClonedIndex0 ((x Input)) Int
  (x_index1 x))""",
            """\
(define-fun Slot0IndexAfterSecondWrite ((x Input)) Int
  (Slot0IndexAfterFirstWrite x))""": """\
(define-fun Slot0IndexAfterSecondWrite ((x Input)) Int
  (Slot1IndexAfterSecondWrite x))""",
            """\
(define-fun Slot1InitializedAfterSecondWrite ((x Input)) Bool
  (IndexInBounds x (ClonedIndex1 x)))""": """\
(define-fun Slot1InitializedAfterSecondWrite ((x Input)) Bool
  false)""",
            """\
(define-fun AssumeInitPermittedAfterFirstWrite ((x Input)) Bool
  (and (Slot0InitializedAfterFirstWrite x)
       (Slot1InitializedAfterFirstWrite x)))""": """\
(define-fun AssumeInitPermittedAfterFirstWrite ((x Input)) Bool
  (Slot0InitializedAfterFirstWrite x))""",
        }
        for original, replacement in mutations.items():
            with self.subTest(original=original.splitlines()[0]):
                self.assertIn(original, self.text)
                self.assert_target_rejected(
                    text=self.text.replace(original, replacement)
                )

    def test_required_solver_probes_are_present(self) -> None:
        self.assertEqual(
            set(target_052.PROBE_CASES),
            {
                "usize_clone_identity",
                "get_unchecked_mut_resolution",
                "complete_initialization_then_assume_init",
                "invalid_success_out_of_bounds_reference",
                "invalid_success_overlapping_references",
                "invalid_prior_slot_mutation",
                "invalid_partial_initialization",
                "invalid_premature_assume_init",
            },
        )

    def test_expected_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        texts = [
            (target_052.obligation(purpose)[0], "sat\n")
            for purpose in target_052.PURPOSES
        ] + [
            (target_052.fixed_witness_text(name), "sat\n")
            for name in target_052.WITNESS_CASES
        ] + [
            (
                target_052.probe_text(name),
                f"{target_052.PROBE_EXPECTED_RESULTS[name]}\n",
            )
            for name in target_052.PROBE_CASES
        ]
        for index, (text, expected) in enumerate(texts):
            with self.subTest(index=index):
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=text,
                    text=True,
                    capture_output=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertTrue(process.stdout.startswith(expected), process.stdout)
                self.assertEqual(process.stderr, "")


class Target052ReplayTests(unittest.TestCase):
    def test_independent_replay_checks_fixed_witness(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "witnesses").mkdir()
            (root / "probes").mkdir()
            for purpose, stem in replay_target_052.OBLIGATIONS.items():
                text, metadata = target_052.obligation(purpose)
                (root / f"{stem}.smt2").write_text(text)
                (root / f"{stem}.metadata.json").write_text(
                    json.dumps(metadata, indent=2, sort_keys=True) + "\n"
                )
            for name in target_052.WITNESS_CASES:
                (root / "witnesses" / f"{name}.smt2").write_text(
                    target_052.fixed_witness_text(name)
                )
            for name in target_052.PROBE_CASES:
                (root / "probes" / f"{name}.smt2").write_text(
                    target_052.probe_text(name)
                )
            (root / "witness.json").write_text(
                json.dumps(
                    target_052.witness_payload(),
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            )
            result = replay_target_052.replay(root, str(z3))
        witness = result["valid_disjoint_distinct_borrows"]
        self.assertEqual(result["status"], "passed")
        self.assertTrue(witness["source_transition_is_complete"])
        self.assertTrue(witness["execution1_satisfies_contract"])
        self.assertTrue(witness["execution2_satisfies_contract"])
        self.assertFalse(witness["exact_output_equal"])
        self.assertTrue(witness["exact_final_state_equal"])
        self.assertFalse(witness["exact_equivalent"])


if __name__ == "__main__":
    unittest.main()
