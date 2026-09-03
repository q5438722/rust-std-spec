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
import replay_target_051
import target_051


class Target051GuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text, self.metadata = target_051.obligation(target_051.PRIMARY)

    def assert_target_rejected(
        self,
        text: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        with self.assertRaises(GuardError):
            target_051.validate_target_obligation(
                text if text is not None else self.text,
                metadata if metadata is not None else self.metadata,
            )

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for purpose in target_051.PURPOSES:
            with self.subTest(purpose=purpose):
                text, metadata = target_051.obligation(purpose)
                validate_obligation(text, metadata)
                target_051.validate_target_obligation(text, metadata)

    def test_active_contract_identity_is_exact(self) -> None:
        self.assertEqual(
            target_051.ACTIVE_CONTRACT_SHA256,
            "65402a0e5a620790d6f1413ab49efa952f05d939b14bf1066e92da32f7cd548a",
        )
        for clause in (
            "ret.is_ok() ==> slice_disjoint_indices_valid",
            "final(slice)@.len() == old(slice)@.len()",
            "ret.is_err() ==> !slice_disjoint_indices_valid",
            "final(slice)@ == old(slice)@",
        ):
            self.assertIn(clause, target_051.ACTIVE_CONTRACT_TEXT)

    def test_answer_bearing_retained_sites_are_replaced_not_renamed(self) -> None:
        manifest = target_051.boundary_manifest()
        excluded = {
            item["trust_site_id"] for item in manifest["excluded_retained_sites"]
        }
        self.assertEqual(
            excluded, set(target_051.EXCLUDED_RETAINED_TRUST_SITES)
        )
        admitted = set(manifest["admitted_boundary_trust_site_ids"])
        self.assertTrue(excluded.isdisjoint(admitted))
        serialized = json.dumps(
            manifest["shared_boundary_observations"], sort_keys=True
        )
        for forbidden in (
            "validity bit",
            "error kind",
            "returned borrow",
            "alias map",
            "resulting state",
            "execution trace",
        ):
            self.assertNotIn(forbidden, serialized)

    def test_answer_bearing_boundary_is_rejected(self) -> None:
        text = self.text.replace(
            "      (b_frame_token Int)))))",
            "      (b_frame_token Int)\n"
            "      (b_selected_error ErrorKind)))))",
        ).replace(
            "       (= (b_frame_token b) (x_frame_token x))))",
            "       (= (b_frame_token b) (x_frame_token x))\n"
            "       (= (b_selected_error b) (y_error_kind y))))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_selected_error",
                "role": "source_helper_observation",
                "source_citations": [target_051.VALIDATION_LOOP_REFERENCE],
                "trust_site_ids": ["TS-051-D002", "TS-051-E001"],
            }
        )
        self.assert_target_rejected(text=text, metadata=metadata)

    def test_opaque_validity_relation_is_rejected(self) -> None:
        original = """\
(define-fun ValidationLoopIsValid ((x Input)) Bool
  (= (ValidationLoopError x) NoError))"""
        replacement = "(declare-fun ValidationLoopIsValid (Input) Bool)"
        text = self.text.replace(original, replacement)
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "ValidationLoopIsValid",
                "role": "source_transition",
                "source_citations": [target_051.VALIDATION_LOOP_REFERENCE],
            }
        ]
        self.assert_target_rejected(text=text, metadata=metadata)

    def test_deterministic_error_choice_injection_is_rejected(self) -> None:
        text = self.text.replace(
            "       (ResultEncodingWellFormed x y)\n",
            "       (ResultEncodingWellFormed x y)\n"
            "       (= (y_error_kind y) (ValidationLoopError x))\n",
        )
        self.assert_target_rejected(text=text)

    def test_deterministic_borrow_choice_injection_is_rejected(self) -> None:
        text = self.text.replace(
            "       (ResultEncodingWellFormed x y)\n",
            "       (ResultEncodingWellFormed x y)\n"
            "       (=> (y_is_ok y) (CanonicalBorrowArrayConstructed x y))\n",
        )
        self.assert_target_rejected(text=text)

    def test_invalid_or_overlapping_success_acceptance_is_rejected(self) -> None:
        mutations = (
            "(IndexInBounds x index)",
            "(not (= (y_ref0_index y) (y_ref1_index y)))",
        )
        replacements = ("true", "true")
        for original, replacement in zip(mutations, replacements, strict=True):
            with self.subTest(original=original):
                self.assertIn(original, self.text)
                self.assert_target_rejected(
                    text=self.text.replace(original, replacement, 1)
                )

    def test_prior_result_mutation_is_rejected(self) -> None:
        original = """\
(define-fun CanonicalSlot0AfterSecondWrite ((x Input)) Int
  (CanonicalSlot0AfterFirstWrite x))"""
        replacement = """\
(define-fun CanonicalSlot0AfterSecondWrite ((x Input)) Int
  (x_index1 x))"""
        self.assertIn(original, self.text)
        self.assert_target_rejected(text=self.text.replace(original, replacement))

    def test_required_solver_probes_are_present(self) -> None:
        self.assertEqual(
            set(target_051.PROBE_CASES),
            {
                "validation_loop_out_of_bounds",
                "validation_loop_overlap",
                "canonical_disjoint_construction",
                "invalid_success_out_of_bounds_reference",
                "invalid_success_overlapping_references",
                "invalid_prior_result_mutation",
            },
        )

    def test_expected_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        texts = [
            (target_051.obligation(purpose)[0], "sat\n")
            for purpose in target_051.PURPOSES
        ] + [
            (target_051.fixed_witness_text(name), "sat\n")
            for name in target_051.WITNESS_CASES
        ] + [
            (
                target_051.probe_text(name),
                f"{target_051.PROBE_EXPECTED_RESULTS[name]}\n",
            )
            for name in target_051.PROBE_CASES
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
                self.assertTrue(
                    process.stdout.startswith(expected),
                    process.stdout,
                )
                self.assertEqual(process.stderr, "")


class Target051ReplayTests(unittest.TestCase):
    def test_independent_replay_checks_both_witnesses(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "witnesses").mkdir()
            (root / "probes").mkdir()
            for purpose, stem in replay_target_051.OBLIGATIONS.items():
                text, metadata = target_051.obligation(purpose)
                (root / f"{stem}.smt2").write_text(text)
                (root / f"{stem}.metadata.json").write_text(
                    json.dumps(metadata, indent=2, sort_keys=True) + "\n"
                )
            for name in target_051.WITNESS_CASES:
                (root / "witnesses" / f"{name}.smt2").write_text(
                    target_051.fixed_witness_text(name)
                )
            for name in target_051.PROBE_CASES:
                (root / "probes" / f"{name}.smt2").write_text(
                    target_051.probe_text(name)
                )
            (root / "witness.json").write_text(
                json.dumps(
                    target_051.witness_payload(),
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            )
            result = replay_target_051.replay(root, str(z3))
        self.assertEqual(result["status"], "passed")
        self.assertFalse(
            result["out_of_bounds_error_variants"]["exact_equivalent"]
        )
        self.assertFalse(
            result["valid_disjoint_distinct_borrows"]["exact_equivalent"]
        )
        self.assertTrue(
            result["valid_disjoint_distinct_borrows"][
                "execution2_borrows_well_formed_and_disjoint"
            ]
        )


if __name__ == "__main__":
    unittest.main()
