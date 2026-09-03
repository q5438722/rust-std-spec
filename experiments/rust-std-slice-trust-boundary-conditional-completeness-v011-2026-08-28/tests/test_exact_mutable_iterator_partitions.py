#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import campaign_common as common
from checker_guards import GuardError, validate_obligation
import exact_mutable_iterator_partitions as partitions
import run_exact_mutable_iterator_partitions as runner
import validate_authority_design as authority_validator


def omit_call(text: str, symbol: str) -> str:
    target_start = text.index("(define-fun TargetDefinition_T")
    start = text.index(f"({symbol}", target_start)
    balance = 0
    for end in range(start, len(text)):
        if text[end] == "(":
            balance += 1
        elif text[end] == ")":
            balance -= 1
            if balance == 0:
                return text[:start] + "true" + text[end + 1 :]
    raise AssertionError(f"unterminated call to {symbol}")


def source_anchor_inputs(
    config: partitions.ExactPartitionTarget,
) -> tuple[str, str]:
    row = next(
        row
        for row in common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        if (row["target"], row["input_order"])
        == (config.target, config.input_order)
    )
    canonical = (
        common.RUST_LIBRARY / partitions.CANONICAL_ITER_PATH
    ).read_text().splitlines(keepends=True)
    private = "".join(
        canonical[
            config.private_source_start - 1 : config.private_source_end
        ]
    )
    return row["source_item_text"], private


class ExactMutableIteratorPartitionTests(unittest.TestCase):
    def test_active_contracts_and_trust_sets_match_live_authority(self) -> None:
        rows = {
            (row["target"], row["input_order"]): row
            for row in common.read_csv(
                ROOT / "crosswalk/target_to_proof_boundary.csv"
            )
        }
        for config in partitions.TARGETS:
            row = rows[(config.target, config.input_order)]
            with self.subTest(target=config.target):
                self.assertEqual(
                    config.active_contract_sha256,
                    row["active_contract_sha256"],
                )
                self.assertEqual(
                    config.active_contract_text,
                    row["active_contract_text"],
                )
                self.assertEqual(
                    set(config.all_trust_site_ids),
                    set(row["all_trust_site_ids"].split(";")),
                )
                self.assertEqual(row["boundary_admissibility"], "admissible")
                self.assertEqual(row["boundary_narrower_than_target"], "yes")

    def test_source_transitions_remain_anchored_to_canonical_bodies(self) -> None:
        for config in partitions.TARGETS:
            public, private = source_anchor_inputs(config)
            with self.subTest(target=config.target):
                partitions.validate_source_anchors(
                    config,
                    public,
                    private,
                )
                for fragment in config.private_fragments:
                    changed = private.replace(fragment, "source drift", 1)
                    self.assertNotEqual(changed, private)
                    with self.assertRaises(GuardError):
                        partitions.validate_source_anchors(
                            config,
                            public,
                            changed,
                        )

    def test_literal_shared_input_shared_boundary_theorems_are_valid(
        self,
    ) -> None:
        for config in partitions.TARGETS:
            for purpose in partitions.PURPOSES:
                text, metadata = partitions.obligation(config, purpose)
                with self.subTest(target=config.target, purpose=purpose):
                    validate_obligation(text, metadata)
                    partitions.validate_target_obligation(
                        config,
                        text,
                        metadata,
                    )
                    self.assertIn("(Spec_T x b y1 s1)", text)
                    self.assertIn("(Spec_T x b y2 s2)", text)
                    self.assertIn(
                        "(Equivalent_T x b y1 s1 y2 s2)",
                        text,
                    )

    def test_boundary_contains_only_initial_identity_and_layout(self) -> None:
        expected = {
            "b_input_address",
            "b_input_allocation",
            "b_input_provenance",
            "b_input_borrow",
            "b_element_size",
        }
        forbidden = (
            "split",
            "remainder",
            "remaining",
            "returned",
            "result",
            "final",
            "direction",
            "chunk",
            "trace",
        )
        for config in partitions.TARGETS:
            metadata = partitions.obligation_metadata(
                config,
                partitions.PRIMARY,
            )
            selectors = {
                item["selector"] for item in metadata["boundary_fields"]
            }
            manifest = partitions.boundary_manifest(config)
            with self.subTest(target=config.target):
                self.assertEqual(selectors, expected)
                self.assertTrue(
                    metadata["boundary_scope"]["narrower_than_target"]
                )
                self.assertTrue(manifest["boundary_narrower_than_target"])
                self.assertFalse(
                    any(
                        token in selector
                        for selector in selectors
                        for token in forbidden
                    )
                )

    def test_every_source_transition_and_contract_conjunct_is_live(
        self,
    ) -> None:
        for config in partitions.TARGETS:
            text, metadata = partitions.obligation(
                config,
                partitions.PRIMARY,
            )
            target = text[text.index("(define-fun TargetDefinition_T") :]
            for transition in config.source_transitions:
                with self.subTest(target=config.target, transition=transition):
                    self.assertIn(f"(define-fun {transition}", text)
                    self.assertIn(f"({transition}", target)
                    with self.assertRaises(GuardError):
                        partitions.validate_target_obligation(
                            config,
                            omit_call(text, transition),
                            metadata,
                        )
            for conjunct in config.active_conjuncts:
                with self.subTest(target=config.target, conjunct=conjunct):
                    self.assertIn(f"(define-fun {conjunct}", text)
                    self.assertIn(f"({conjunct}", target)
                    with self.assertRaises(GuardError):
                        partitions.validate_target_obligation(
                            config,
                            omit_call(text, conjunct),
                            metadata,
                        )

    def test_remainder_split_orientation_and_identity_mutations_fail_closed(
        self,
    ) -> None:
        for config in partitions.TARGETS:
            text, metadata = partitions.obligation(
                config,
                partitions.PRIMARY,
            )
            wrong_split = (
                "(= (y_split_index y) (- (x_length x) (y_mod_remainder y)))"
                if config.reverse
                else "(= (y_split_index y) (y_mod_remainder y))"
            )
            right_split = (
                "(= (y_split_index y) (y_mod_remainder y))"
                if config.reverse
                else "(= (y_split_index y) (- (x_length x) (y_mod_remainder y)))"
            )
            right_remainder_start = (
                "(= (y_remainder_start y) (x_source_start x))"
                if config.reverse
                else "(= (y_remainder_start y)\n"
                "          (+ (x_source_start x) (y_remaining_length y)))"
            )
            wrong_remainder_start = (
                "(= (y_remainder_start y)\n"
                "          (+ (x_source_start x) (y_remaining_length y)))"
                if config.reverse
                else "(= (y_remainder_start y) (x_source_start x))"
            )
            mutations = {
                "zero-domain": text.replace(
                    "(> (x_chunk_size x) 0)",
                    "(>= (x_chunk_size x) 0)",
                    1,
                ),
                "incorrect-modulo": text.replace(
                    "(= (y_mod_remainder y) (mod (x_length x) (x_chunk_size x)))",
                    "(= (y_mod_remainder y) (+ 1 (mod (x_length x) (x_chunk_size x))))",
                    1,
                ),
                "incorrect-split": text.replace(
                    right_split,
                    wrong_split,
                    1,
                ),
                "swapped-remainder": text.replace(
                    right_remainder_start,
                    wrong_remainder_start,
                    1,
                ),
                "wrong-concatenation": text.replace(
                    "(= (+ (y_remaining_length y) (y_remainder_length y))\n"
                    "          (x_length x))",
                    "(= (+ (y_remaining_length y) (y_remainder_length y))\n"
                    "          (+ (x_length x) 1))",
                    1,
                ),
                "provenance-loss": text.replace(
                    "(= (y_raw_v_provenance y) (y_remaining_provenance y))",
                    "(= (y_raw_v_provenance y) (x_allocation x))",
                    1,
                ),
                "borrow-loss": text.replace(
                    "(= (y_remainder_parent_borrow y) (x_borrow x))",
                    "(= (y_remainder_parent_borrow y) (+ (x_borrow x) 1))",
                    1,
                ),
            }
            for name, changed in mutations.items():
                with self.subTest(target=config.target, mutation=name):
                    self.assertNotEqual(changed, text)
                    with self.assertRaises(GuardError):
                        partitions.validate_target_obligation(
                            config,
                            changed,
                            metadata,
                        )

    def test_all_principal_equalities_are_exact_and_required(self) -> None:
        for config in partitions.TARGETS:
            text, metadata = partitions.obligation(
                config,
                partitions.PRIMARY,
            )
            selectors = partitions.OUTPUT_FIELDS + partitions.STATE_FIELDS
            for selector, _ in selectors:
                left = "y1" if selector.startswith("y_") else "s1"
                right = "y2" if selector.startswith("y_") else "s2"
                equality = f"(= ({selector} {left}) ({selector} {right}))"
                with self.subTest(target=config.target, selector=selector):
                    self.assertIn(equality, text)
                    with self.assertRaises(GuardError):
                        partitions.validate_target_obligation(
                            config,
                            text.replace(equality, "true", 1),
                            metadata,
                        )

    def test_answer_bearing_and_laundered_boundaries_fail_closed(self) -> None:
        config = partitions.TARGETS[0]
        text, metadata = partitions.obligation(
            config,
            partitions.PRIMARY,
        )
        expanded = text.replace(
            "      (b_element_size Int))))",
            "      (b_element_size Int)\n"
            "      (b_split_answer Int))))",
            1,
        )
        answer_bearing = expanded.replace(
            "       (InputIdentityObserved x b)))",
            "       (InputIdentityObserved x b)\n"
            "       (= (b_split_answer b) (y_split_index y)))",
            1,
        )
        answer_metadata = copy.deepcopy(metadata)
        answer_metadata["boundary_fields"].append(
            {
                "selector": "b_split_answer",
                "role": "selected_output",
                "source_citations": [config.private_source_reference],
                "trust_site_ids": list(config.boundary_trust_site_ids),
            }
        )
        with self.assertRaises(GuardError):
            partitions.validate_target_obligation(
                config,
                answer_bearing,
                answer_metadata,
            )

        laundered = expanded.replace(
            "(= (y_split_index y) (- (x_length x) (y_mod_remainder y)))",
            "(= (y_split_index y) "
            "(+ (b_split_answer b) (- (x_length x) (x_length x))))",
            1,
        )
        laundered_metadata = copy.deepcopy(metadata)
        laundered_metadata["boundary_fields"].append(
            {
                "selector": "b_split_answer",
                "role": "input_memory",
                "source_citations": [config.private_source_reference],
                "trust_site_ids": list(config.boundary_trust_site_ids),
            }
        )
        with self.assertRaises(GuardError):
            partitions.validate_target_obligation(
                config,
                laundered,
                laundered_metadata,
            )

    def test_mismatched_second_boundary_fails_closed(self) -> None:
        config = partitions.TARGETS[0]
        text, metadata = partitions.obligation(
            config,
            partitions.PRIMARY,
        )
        changed = text.replace(
            "(declare-const y1 Output)",
            "(declare-const b2 Boundary)\n(declare-const y1 Output)",
            1,
        ).replace(
            "(Spec_T x b y2 s2)",
            "(Spec_T x b2 y2 s2)",
            1,
        )
        with self.assertRaises(GuardError):
            partitions.validate_target_obligation(
                config,
                changed,
                metadata,
            )

    def test_required_source_cases_are_sat_with_replay_values(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        self.assertEqual(
            set(partitions.SOURCE_CASES),
            {
                "empty",
                "unit_chunk",
                "shorter_than_chunk",
                "divisible",
                "nondivisible",
                "zst_equal_address_disjoint",
            },
        )
        for config in partitions.TARGETS:
            for name, case in partitions.SOURCE_CASES.items():
                with self.subTest(target=config.target, case=name):
                    process = subprocess.run(
                        [str(z3), "-in", "-smt2"],
                        input=partitions.source_instance_text(config, case),
                        text=True,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertTrue(process.stdout.startswith("sat\n"))
                    self.assertIn("(x_length x)", process.stdout)
                    self.assertIn("(y_split_index y1)", process.stdout)
                    self.assertEqual(process.stderr, "")

    def test_semantic_negative_probes_are_unsat(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for config in partitions.TARGETS:
            for name in partitions.NEGATIVE_PROBES:
                with self.subTest(target=config.target, probe=name):
                    process = subprocess.run(
                        [str(z3), "-in", "-smt2"],
                        input=partitions.negative_probe_text(config, name),
                        text=True,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, "unsat\n")
                    self.assertEqual(process.stderr, "")

    def test_both_literal_theorem_projections_are_unsat(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for config in partitions.TARGETS:
            for purpose in partitions.PURPOSES:
                with self.subTest(target=config.target, purpose=purpose):
                    process = subprocess.run(
                        [str(z3), "-in", "-smt2"],
                        input=partitions.obligation_text(config, purpose),
                        text=True,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, "unsat\n")
                    self.assertEqual(process.stderr, "")

    def test_out_of_scope_ledger_mutation_is_rejected(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        other_key = next(
            (row["target"], row["input_order"])
            for row in csv_rows
            if (row["target"], row["input_order"])
            not in set(runner.BASELINE_RESULTS)
            | set(partitions.TARGET_KEYS)
        )
        for rows in (csv_rows, json_rows):
            row = next(
                item
                for item in rows
                if (item["target"], item["input_order"]) == other_key
            )
            row.update(runner.COMPLETE)
        with self.assertRaises(ValueError):
            runner.prepare_crosswalk_reset(csv_rows, json_rows)

    def test_generated_verus_is_target_specific_and_trusted_free(self) -> None:
        for config in partitions.TARGETS:
            text = partitions.verus_text(config)
            function = config.target.rsplit("::", 1)[-1]
            with self.subTest(target=config.target):
                self.assertNotIn("external_body", text)
                self.assertIn(f"{function}_constructor", text)
                self.assertIn(f"conditional_complete_{function}", text)
                self.assertIn(
                    f"conditional_complete_exact_output_{function}",
                    text,
                )
                self.assertIn("make_region", text)
                self.assertIn("modulo_remainder", text)
                self.assertIn("split_index", text)
                self.assertIn("parent_borrow", text)

    def test_local_validator_reports_56_classified_and_6_not_run(
        self,
    ) -> None:
        rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        self.assertEqual(
            authority_validator.target_result_counts(rows),
            (62, 0),
        )
        self.assertEqual(
            len(authority_validator.TARGET_RESULT_LABELS),
            62,
        )
        summary = authority_validator.target_results_summary(rows)
        self.assertIn("035_conditional-complete", summary)
        self.assertIn("068_conditional-complete", summary)
        self.assertTrue(summary.endswith(",0_not-run"))
        self.assertEqual(
            authority_validator.target_result_count_summary(rows),
            "target_result_counts=62_classified,0_not-run",
        )


if __name__ == "__main__":
    unittest.main()
