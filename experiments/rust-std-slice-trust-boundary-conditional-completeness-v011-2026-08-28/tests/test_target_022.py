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
import replay_target_022
import run_target_022
import target_022
import target_pipeline


class Target022GuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text, self.metadata = target_022.obligation(target_022.PRIMARY)

    def assert_target_rejected(
        self,
        text: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        with self.assertRaises(GuardError):
            target_022.validate_target_obligation(
                text if text is not None else self.text,
                metadata if metadata is not None else self.metadata,
            )

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for purpose in target_022.PURPOSES:
            with self.subTest(purpose=purpose):
                text, metadata = target_022.obligation(purpose)
                validate_obligation(text, metadata)
                target_022.validate_target_obligation(text, metadata)

    def test_active_contract_identity_is_exact(self) -> None:
        self.assertEqual(
            target_022.ACTIVE_CONTRACT_SHA256,
            "2bb2f31be87ccb793fb77b630b4b57ca59c5d534fd90d38b858122dee6212434",
        )
        self.assertIn("slice_ptr_range_starts_at_slice", target_022.ACTIVE_CONTRACT_TEXT)

    def test_null_provenance_synthesis_is_rejected(self) -> None:
        mutated = self.text.replace(
            "(define-fun SliceCastProvenance ((x Input)) Int\n"
            "  (x_provenance x))",
            "(define-fun SliceCastProvenance ((x Input)) Int\n  0)",
        )
        self.assert_target_rejected(text=mutated)

    def test_address_equals_length_substitution_is_rejected(self) -> None:
        mutated = self.text.replace(
            "(define-fun SliceCastAddress ((x Input)) Int\n  (x_address x))",
            "(define-fun SliceCastAddress ((x Input)) Int\n  (x_length x))",
        )
        self.assert_target_rejected(text=mutated)

    def test_endpoint_bearing_boundary_is_rejected(self) -> None:
        mutated = self.text.replace(
            "      (b_address_space_limit Int)))))",
            "      (b_address_space_limit Int)\n"
            "      (b_returned_end_address Int)))))",
        ).replace(
            "       (= (b_address_space_limit b) (x_address_space_limit x))))",
            "       (= (b_address_space_limit b) (x_address_space_limit x))\n"
            "       (= (b_returned_end_address b) (b_returned_end_address b))))",
            1,
        ).replace(
            "       (InputMemoryLayoutObserved x b)))",
            "       (InputMemoryLayoutObserved x b)\n"
            "       (= (b_returned_end_address b) (b_returned_end_address b))))",
            1,
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_returned_end_address",
                "role": "selected_output",
                "source_citations": [target_022.CANONICAL_PTR_ADD_REFERENCE],
                "trust_site_ids": ["TS-022-D004"],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(mutated, metadata)

    def test_provenance_change_is_rejected(self) -> None:
        mutated = self.text.replace(
            "(define-fun PtrAddEndProvenance ((x Input)) Int\n"
            "  (SliceCastProvenance x))",
            "(define-fun PtrAddEndProvenance ((x Input)) Int\n"
            "  (+ (SliceCastProvenance x) 1))",
        )
        self.assert_target_rejected(text=mutated)

    def test_wrong_byte_offset_is_rejected(self) -> None:
        mutated = self.text.replace(
            "(+ (SliceCastAddress x) (* (x_length x) (x_element_size x)))",
            "(+ (SliceCastAddress x) (x_length x))",
            1,
        )
        self.assert_target_rejected(text=mutated)

    def test_missing_no_wrap_constraint_is_rejected(self) -> None:
        clause = """\
       (<= (+ (x_address x)
              (* (x_length x) (x_element_size x)))
           (x_address_space_limit x))"""
        self.assertIn(clause, self.text)
        self.assert_target_rejected(text=self.text.replace(clause, "       true", 1))

    def test_missing_allocation_constraint_is_rejected(self) -> None:
        clause = """\
                (<= (+ (x_address x)
                       (* (x_length x) (x_element_size x)))
                    (+ (x_allocation_base x)
                       (x_allocation_bytes x))))"""
        self.assertIn(clause, self.text)
        self.assert_target_rejected(text=self.text.replace(clause, "       true", 1))

    def test_non_null_and_conditional_allocation_domain_is_required(self) -> None:
        self.assertIn("(> (x_address x) 0)", self.text)
        conditional = """\
       (or (= (* (x_length x) (x_element_size x)) 0)
           (and (> (x_allocation x) 0)
                (> (x_provenance x) 0)"""
        self.assertIn(conditional, self.text)
        self.assert_target_rejected(
            text=self.text.replace("(> (x_address x) 0)", "(>= (x_address x) 0)", 1)
        )
        self.assert_target_rejected(
            text=self.text.replace(conditional, "       true", 1)
        )

    def test_opaque_pointer_add_relation_is_rejected(self) -> None:
        mutated = self.text.replace(
            "(declare-const x Input)",
            "(declare-fun OpaquePointerAdd (Input) Int)\n"
            "(declare-const x Input)",
        ).replace(
            "(define-fun PtrAddEndAddress ((x Input)) Int\n"
            "  (+ (SliceCastAddress x) (* (x_length x) (x_element_size x))))",
            "(define-fun PtrAddEndAddress ((x Input)) Int\n"
            "  (OpaquePointerAdd x))",
        )
        metadata = copy.deepcopy(self.metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "OpaquePointerAdd",
                "role": "source_transition",
                "source_citations": [target_022.CANONICAL_PTR_ADD_REFERENCE],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(mutated, metadata)

    def test_omitted_endpoint_equality_is_rejected(self) -> None:
        equality = "(= (y_end_provenance y1) (y_end_provenance y2))"
        self.assertIn(equality, self.text)
        self.assert_target_rejected(text=self.text.replace(equality, "true", 1))

    def test_boundary_manifest_excludes_replaced_helpers(self) -> None:
        manifest = target_022.boundary_manifest()
        excluded = {
            item["trust_site_id"] for item in manifest["excluded_retained_sites"]
        }
        self.assertEqual(excluded, set(target_022.EXCLUDED_RETAINED_TRUST_SITES))
        serialized = json.dumps(manifest["shared_boundary_observations"])
        for forbidden in ("returned", "endpoint", "range", "trace"):
            self.assertNotIn(forbidden, serialized)

    def test_expected_solver_results_and_domain_probes(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        texts = [
            (target_022.obligation(purpose)[0], "unsat\n")
            for purpose in target_022.PURPOSES
        ] + [
            (
                target_022.probe_text(name),
                f"{target_022.PROBE_EXPECTED_RESULTS[name]}\n",
            )
            for name in target_022.PROBE_CASES
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
        for key in run_target_022.PRESERVED_RESULTS:
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
                            target=target_022.TARGET,
                            input_order=target_022.INPUT_ORDER,
                            statuses=run_target_022.RESULT_STATUSES,
                            preserved_results=run_target_022.PRESERVED_RESULTS,
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
                target_022.TARGET,
                *(target for target, _ in run_target_022.PRESERVED_RESULTS),
            }
        )
        other["exact_output_determinism_status"] = "conditional-complete"
        json_rows = copy.deepcopy(csv_rows)
        with self.assertRaises(ValueError):
            target_pipeline.apply_crosswalk_result_update(
                csv_rows,
                json_rows,
                target=target_022.TARGET,
                input_order=target_022.INPUT_ORDER,
                statuses=run_target_022.RESULT_STATUSES,
                preserved_results=run_target_022.PRESERVED_RESULTS,
            )


class Target022ReplayTests(unittest.TestCase):
    def test_independent_replay_checks_obligations_and_probes(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "probes").mkdir()
            for purpose, stem in replay_target_022.OBLIGATIONS.items():
                text, metadata = target_022.obligation(purpose)
                (root / f"{stem}.smt2").write_text(text)
                (root / f"{stem}.metadata.json").write_text(
                    json.dumps(metadata, indent=2, sort_keys=True) + "\n"
                )
            for name in target_022.PROBE_CASES:
                (root / "probes" / f"{name}.smt2").write_text(
                    target_022.probe_text(name)
                )
            result = replay_target_022.replay(root, str(z3))
        self.assertEqual(result["status"], "passed")
        self.assertEqual(set(result["obligations"]), set(target_022.PURPOSES))
        self.assertEqual(
            set(result["satisfiability_probes"]), set(target_022.PROBE_CASES)
        )


if __name__ == "__main__":
    unittest.main()
