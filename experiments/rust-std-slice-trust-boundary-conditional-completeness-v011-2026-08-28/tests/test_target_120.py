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
import campaign_common as common
import replay_target_120
import run_target_120
import target_120
import target_pipeline


class Target120GuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text, self.metadata = target_120.obligation(target_120.PRIMARY)

    def assert_target_rejected(
        self,
        text: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        with self.assertRaises(GuardError):
            target_120.validate_target_obligation(
                text if text is not None else self.text,
                metadata if metadata is not None else self.metadata,
            )

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for purpose in target_120.PURPOSES:
            with self.subTest(purpose=purpose):
                text, metadata = target_120.obligation(purpose)
                validate_obligation(text, metadata)
                target_120.validate_target_obligation(text, metadata)

    def test_active_contract_identity_is_exact(self) -> None:
        self.assertEqual(
            target_120.ACTIVE_CONTRACT_SHA256,
            "09f266d66c804f7e0f5f296f4050ba156240da188db824b5f5f6efc0a0145e69",
        )
        for clause in (
            "ret@ == src@",
            "maybe_uninit_written_from",
            "maybe_uninit_all_initialized",
            "final(ret)@.len() == src@.len()",
        ):
            self.assertIn(clause, target_120.ACTIVE_CONTRACT_TEXT)

    def test_answer_equivalent_retained_sites_are_replaced_not_renamed(self) -> None:
        manifest = target_120.boundary_manifest()
        excluded = {
            item["trust_site_id"] for item in manifest["excluded_retained_sites"]
        }
        self.assertEqual(
            excluded, set(target_120.EXCLUDED_RETAINED_TRUST_SITES)
        )
        admitted = set(manifest["admitted_boundary_trust_site_ids"])
        self.assertTrue(excluded.isdisjoint(admitted))
        serialized_boundary = json.dumps(
            manifest["shared_boundary_observations"], sort_keys=True
        )
        for forbidden in (
            "resulting",
            "returned reference",
            "aggregate final",
            "execution trace",
            "storage-effect",
        ):
            self.assertNotIn(forbidden, serialized_boundary)

    def test_aggregate_final_storage_boundary_is_rejected(self) -> None:
        mutated = self.text.replace(
            "      (b_frame_token Int)))))",
            "      (b_frame_token Int)\n"
            "      (b_final_storage (Array Int Int))))))",
        ).replace(
            "       (= (b_frame_token b) (x_frame_token x))",
            "       (= (b_frame_token b) (x_frame_token x))\n"
            "       (= (b_final_storage b) (b_final_storage b))",
            1,
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_final_storage",
                "role": "aggregate_final_state",
                "source_citations": [target_120.COPY_NONOVERLAPPING_REFERENCE],
                "trust_site_ids": ["TS-120-E005"],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(mutated, metadata)

    def test_uninitialized_destination_value_read_is_rejected(self) -> None:
        original = """\
(define-fun FinalDestinationStorage ((x Input)) (Array Int Cell)
  ((_ map Initialized) (SameLayoutTransmuteValues x)))"""
        mutated = """\
(define-fun FinalDestinationStorage ((x Input)) (Array Int Cell)
  (store
    ((_ map Initialized) (SameLayoutTransmuteValues x))
    0
    (Initialized
      (initialized_value (select (x_destination_storage x) 0)))))"""
        self.assertIn(original, self.text)
        self.assert_target_rejected(text=self.text.replace(original, mutated))

    def test_no_op_copy_is_rejected(self) -> None:
        self.assert_target_rejected(
            text=self.text.replace(
                "(define-fun FinalDestinationStorage ((x Input)) (Array Int Cell)\n"
                "  ((_ map Initialized) (SameLayoutTransmuteValues x)))",
                "(define-fun FinalDestinationStorage ((x Input)) (Array Int Cell)\n"
                "  (x_destination_storage x))",
                1,
            )
        )

    def test_partial_copy_is_rejected(self) -> None:
        self.assert_target_rejected(
            text=self.text.replace(
                "(define-fun FinalDestinationStorage ((x Input)) (Array Int Cell)\n"
                "  ((_ map Initialized) (SameLayoutTransmuteValues x)))",
                "(define-fun FinalDestinationStorage ((x Input)) (Array Int Cell)\n"
                "  (store ((_ map Initialized) (SameLayoutTransmuteValues x))\n"
                "         0 (select (x_destination_storage x) 0)))",
                1,
            )
        )

    def test_omitted_initialization_update_is_rejected(self) -> None:
        self.assert_target_rejected(
            text=self.text.replace(
                "((_ map Initialized) (SameLayoutTransmuteValues x))",
                "((as const (Array Int Cell)) Uninitialized)",
                1,
            )
        )

    def test_omitted_value_update_is_rejected(self) -> None:
        self.assert_target_rejected(
            text=self.text.replace(
                "((_ map Initialized) (SameLayoutTransmuteValues x))",
                "((as const (Array Int Cell)) (Initialized 0))",
                1,
            )
        )

    def test_unequal_length_admission_is_rejected(self) -> None:
        equality = "(= (x_destination_length x) (x_source_length x))"
        self.assertGreaterEqual(self.text.count(equality), 2)
        self.assert_target_rejected(
            text=self.text.replace(equality, "true", 1)
        )

    def test_wrong_destination_or_return_identity_is_rejected(self) -> None:
        mutations = (
            (
                "(define-fun FinalDestinationAllocation ((x Input)) Int\n"
                "  (x_destination_allocation x))",
                "(define-fun FinalDestinationAllocation ((x Input)) Int\n"
                "  (x_source_allocation x))",
            ),
            (
                "(define-fun AssumeInitReturnBorrow ((x Input)) Int\n"
                "  (FinalDestinationBorrow x))",
                "(define-fun AssumeInitReturnBorrow ((x Input)) Int\n"
                "  (+ (FinalDestinationBorrow x) 1))",
            ),
        )
        for old, new in mutations:
            with self.subTest(old=old.splitlines()[0]):
                self.assertIn(old, self.text)
                self.assert_target_rejected(text=self.text.replace(old, new))

    def test_source_or_frame_mutation_is_rejected(self) -> None:
        mutations = (
            (
                "(define-fun PreservedSourceValues ((x Input)) (Array Int Int)\n"
                "  (CanonicalSourceValues x))",
                "(define-fun PreservedSourceValues ((x Input)) (Array Int Int)\n"
                "  ((as const (Array Int Int)) 0))",
            ),
            (
                "(define-fun PreservedFrameToken ((x Input)) Int\n"
                "  (x_frame_token x))",
                "(define-fun PreservedFrameToken ((x Input)) Int\n"
                "  (+ (x_frame_token x) 1))",
            ),
        )
        for old, new in mutations:
            with self.subTest(old=old.splitlines()[0]):
                self.assertIn(old, self.text)
                self.assert_target_rejected(text=self.text.replace(old, new))

    def test_required_domain_probes_are_present(self) -> None:
        self.assertTrue(
            {
                "valid_empty",
                "valid_wholly_uninitialized",
                "valid_mixed_initialization",
                "valid_fully_initialized",
                "invalid_unequal_lengths",
                "invalid_no_op_copy",
                "invalid_partial_copy",
                "invalid_omitted_initialization",
                "invalid_wrong_destination_identity",
                "invalid_wrong_return_identity",
                "invalid_changed_source",
                "invalid_changed_frame",
            }
            <= set(target_120.PROBE_CASES)
        )

    def test_expected_solver_results_and_domain_probes(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        texts = [
            (target_120.obligation(purpose)[0], "unsat\n")
            for purpose in target_120.PURPOSES
        ] + [
            (
                target_120.probe_text(name),
                f"{target_120.PROBE_EXPECTED_RESULTS[name]}\n",
            )
            for name in target_120.PROBE_CASES
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
                self.assertEqual(process.stdout, expected)
                self.assertEqual(process.stderr, "")

    def test_each_accepted_crosswalk_row_cannot_be_mutated(self) -> None:
        base_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        for row in base_rows:
            if row["target"] in {
                "core::slice::get_disjoint_mut",
                "core::slice::get_disjoint_unchecked_mut",
            }:
                for field in target_pipeline.RESULT_FIELDS:
                    row[field] = "not-run"
        for key in run_target_120.PRESERVED_RESULTS:
            for field in target_pipeline.RESULT_FIELDS:
                with self.subTest(key=key, field=field):
                    csv_rows = copy.deepcopy(base_rows)
                    json_rows = copy.deepcopy(base_rows)
                    for rows in (csv_rows, json_rows):
                        row = next(
                            candidate
                            for candidate in rows
                            if (candidate["target"], candidate["input_order"]) == key
                        )
                        row[field] = "solver-unknown"
                    with self.assertRaisesRegex(
                        ValueError, "preserved result fields changed"
                    ):
                        target_pipeline.apply_crosswalk_result_update(
                            csv_rows,
                            json_rows,
                            target=target_120.TARGET,
                            input_order=target_120.INPUT_ORDER,
                            statuses=run_target_120.RESULT_STATUSES,
                            preserved_results=run_target_120.PRESERVED_RESULTS,
                        )

    def test_unclassified_crosswalk_row_cannot_be_mutated(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        other = next(
            row
            for row in csv_rows
            if row["target"]
            not in {
                target_120.TARGET,
                *(target for target, _ in run_target_120.PRESERVED_RESULTS),
            }
        )
        other["completeness_modulo_reviewed_equivalence_status"] = (
            "conditional-complete"
        )
        with self.assertRaises(ValueError):
            target_pipeline.apply_crosswalk_result_update(
                csv_rows,
                copy.deepcopy(csv_rows),
                target=target_120.TARGET,
                input_order=target_120.INPUT_ORDER,
                statuses=run_target_120.RESULT_STATUSES,
                preserved_results=run_target_120.PRESERVED_RESULTS,
            )


class Target120ReplayTests(unittest.TestCase):
    def test_independent_replay_checks_obligations_and_probes(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "probes").mkdir()
            for purpose, stem in replay_target_120.OBLIGATIONS.items():
                text, metadata = target_120.obligation(purpose)
                (root / f"{stem}.smt2").write_text(text)
                (root / f"{stem}.metadata.json").write_text(
                    json.dumps(metadata, indent=2, sort_keys=True) + "\n"
                )
            for name in target_120.PROBE_CASES:
                (root / "probes" / f"{name}.smt2").write_text(
                    target_120.probe_text(name)
                )
            result = replay_target_120.replay(root, str(z3))
        self.assertEqual(result["status"], "passed")
        self.assertEqual(set(result["obligations"]), set(target_120.PURPOSES))
        self.assertEqual(
            set(result["satisfiability_probes"]), set(target_120.PROBE_CASES)
        )


if __name__ == "__main__":
    unittest.main()
