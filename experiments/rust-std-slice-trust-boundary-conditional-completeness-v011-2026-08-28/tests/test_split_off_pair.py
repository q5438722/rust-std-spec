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
import run_split_off_pair as runner
import split_off_pair as split
import target_pipeline
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


def source_inputs(
    config: split.SplitOffTarget,
) -> tuple[str, str, dict[str, str]]:
    row = next(
        row
        for row in common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        if (row["target"], row["input_order"])
        == (config.target, config.input_order)
    )
    vocabulary_lines = Path(row["shared_vocabulary_path"]).read_text().splitlines(
        keepends=True
    )
    vocabulary = "\n".join(
        "".join(vocabulary_lines[start - 1 : end])
        for start, end in split.VOCABULARY_RANGES
    )
    source_lines = Path(row["source_path"]).read_text().splitlines(
        keepends=True
    )
    helpers = {
        source.name: "".join(source_lines[source.start - 1 : source.end])
        for source in config.helper_sources
    }
    return row["source_item_text"], vocabulary, helpers


def run_z3(text: str) -> subprocess.CompletedProcess[str]:
    z3 = shutil.which("z3")
    if not z3:
        raise AssertionError("z3 is unavailable")
    return subprocess.run(
        [z3, "-in", "-smt2"],
        input=text,
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )


class SplitOffPairTests(unittest.TestCase):
    def test_active_contracts_and_all_nine_trust_records_match_authority(
        self,
    ) -> None:
        rows = {
            (row["target"], row["input_order"]): row
            for row in common.read_csv(
                ROOT / "crosswalk/target_to_proof_boundary.csv"
            )
        }
        trust = common.read_csv(ROOT / "crosswalk/trust_site_inventory.csv")
        total = 0
        for config in split.TARGETS:
            row = rows[(config.target, config.input_order)]
            records = {
                item["record_id"]: item
                for item in trust
                if (item["target"], item["input_order"])
                == (config.target, config.input_order)
            }
            total += len(records)
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
                    config.generated_declaration_sha256,
                    row["generated_declaration_sha256"],
                )
                self.assertEqual(
                    config.source_item_sha256,
                    row["source_item_sha256"],
                )
                self.assertEqual(set(records), set(config.all_trust_site_ids))
                self.assertEqual(
                    {
                        record_id: split.canonical_json_sha256(record)
                        for record_id, record in records.items()
                    },
                    config.trust_hashes,
                )
        self.assertEqual(total, 9)

    def test_mutable_active_contract_is_not_replaced_by_retained_correction(
        self,
    ) -> None:
        config = next(config for config in split.TARGETS if config.mutable)
        row = next(
            row
            for row in common.read_csv(
                ROOT / "crosswalk/target_to_proof_boundary.csv"
            )
            if (row["target"], row["input_order"])
            == (config.target, config.input_order)
        )
        harness = (ROOT / row["frozen_harness_path"]).read_text()
        transformation = (
            ROOT / row["frozen_transformation_manifest_path"]
        ).read_text()
        text, metadata = split.obligation(config, split.PRIMARY)
        self.assertIn("final(ret.unwrap())@", config.active_contract_text)
        self.assertNotIn("final(ret.unwrap())@", harness)
        self.assertIn(
            "Removed only the generated `final(ret.unwrap())@` partition clause",
            transformation,
        )
        self.assertIn(
            "(define-fun ActiveFinalReturnPartitionConjunct",
            text,
        )
        self.assertIn(
            "ActiveFinalReturnPartitionConjunct",
            metadata["active_contract_conjuncts"],
        )
        self.assertIn("TS-104-D004", config.excluded_trust_site_ids)

    def test_target_vocabulary_and_canonical_helpers_fail_closed(self) -> None:
        for config in split.TARGETS:
            source, vocabulary, helpers = source_inputs(config)
            split.validate_source_anchors(config, source, vocabulary, helpers)
            changed = source.replace(config.source_fragments[0], "source drift")
            with self.subTest(target=config.target, mutation="target"):
                with self.assertRaises(GuardError):
                    split.validate_source_anchors(
                        config,
                        changed,
                        vocabulary,
                        helpers,
                    )
            helper = config.helper_sources[0]
            changed_helpers = dict(helpers)
            changed_helpers[helper.name] = helpers[helper.name].replace(
                helper.fragments[0],
                "helper drift",
                1,
            )
            with self.subTest(target=config.target, mutation="helper"):
                with self.assertRaises(GuardError):
                    split.validate_source_anchors(
                        config,
                        source,
                        vocabulary,
                        changed_helpers,
                    )
            synthetic = dict(helpers)
            synthetic[helper.name] += "\nexternal_body\n"
            with self.subTest(target=config.target, mutation="synthetic"):
                with self.assertRaises(GuardError):
                    split.validate_source_anchors(
                        config,
                        source,
                        vocabulary,
                        synthetic,
                    )

    def test_literal_shared_input_shared_boundary_theorems_are_valid(
        self,
    ) -> None:
        expected = {
            "b_input_address",
            "b_input_allocation",
            "b_input_provenance",
            "b_parent_borrow",
            "b_element_size",
            "b_element_alignment",
        }
        for config in split.TARGETS:
            for purpose in split.PURPOSES:
                text, metadata = split.obligation(config, purpose)
                with self.subTest(target=config.target, purpose=purpose):
                    validate_obligation(text, metadata)
                    split.validate_target_obligation(config, text, metadata)
                    self.assertIn(
                        """(and (Requires_T x)
           (Boundary_T x b)
           (Spec_T x b y1 s1)
           (Spec_T x b y2 s2))""",
                        text,
                    )
                    self.assertEqual(
                        {
                            field["selector"]
                            for field in metadata["boundary_fields"]
                        },
                        expected,
                    )
                    self.assertTrue(
                        metadata["boundary_scope"]["narrower_than_target"]
                    )
                    self.assertNotIn("b_range_kind", text)
                    self.assertNotIn("b_range_index", text)

    def test_source_transitions_and_active_conjuncts_are_live(self) -> None:
        for config in split.TARGETS:
            for purpose in split.PURPOSES:
                text, metadata = split.obligation(config, purpose)
                transitions = (
                    split.OUTPUT_SOURCE_TRANSITIONS
                    if purpose == split.EXACT_OUTPUT
                    else split.SOURCE_TRANSITIONS
                )
                for symbol in transitions:
                    with self.subTest(
                        target=config.target,
                        purpose=purpose,
                        transition=symbol,
                    ):
                        self.assertIn(f"(define-fun {symbol}", text)
                        with self.assertRaises(GuardError):
                            split.validate_target_obligation(
                                config,
                                omit_call(text, symbol),
                                metadata,
                            )
            text, metadata = split.obligation(config, split.PRIMARY)
            for symbol in config.active_conjuncts:
                with self.subTest(target=config.target, conjunct=symbol):
                    self.assertIn(f"(define-fun {symbol}", text)
                    with self.assertRaises(GuardError):
                        split.validate_target_obligation(
                            config,
                            omit_call(text, symbol),
                            metadata,
                        )

    def test_source_semantic_mutations_fail_closed(self) -> None:
        for config in split.TARGETS:
            text, metadata = split.obligation(config, split.PRIMARY)
            mutations = {
                "direction-reversal": text.replace(
                    "(ite (= (x_range_kind x) 0) 1 0)",
                    "(ite (= (x_range_kind x) 0) 0 1)",
                    1,
                ),
                "wrapping-addition": text.replace(
                    "(= (s_split_index s)\n"
                    "       (ite (s_helper_has_split s)",
                    "(= (s_split_index s)\n"
                    "       (ite true",
                    1,
                ),
                "bounds-comparison": text.replace(
                    "(<= (s_split_index s) (x_length x))",
                    "(< (s_split_index s) (x_length x))",
                    1,
                ),
                "off-by-one-split": text.replace(
                    "(x_range_index x))\n            (- 1)))",
                    "(+ (x_range_index x) 1))\n            (- 1)))",
                    1,
                ),
                "swapped-branches": text.replace(
                    "(ite (= (s_direction s) 0)",
                    "(ite (= (s_direction s) 1)",
                    1,
                ),
                "mutated-none-frame": text.replace(
                    "(= (s_receiver_values s) (x_source x))))",
                    f"(= (s_receiver_values s) {split.EMPTY_SEQ})))",
                    1,
                ),
                "lost-identity": text.replace(
                    "(= (s_back_allocation s) (x_allocation x))",
                    "(= (s_back_allocation s) 0)",
                    1,
                ),
                "lost-disjointness": text.replace(
                    "(<= (+ (s_front_start s) (s_front_length s))",
                    "(> (+ (s_front_start s) (s_front_length s))",
                    1,
                ),
                "reversed-frame": text.replace(
                    "(seq.++ (s_front_values s) (s_back_values s))",
                    "(seq.++ (s_back_values s) (s_front_values s))",
                    1,
                ),
            }
            for name, changed in mutations.items():
                with self.subTest(target=config.target, mutation=name):
                    self.assertNotEqual(changed, text)
                    with self.assertRaises(GuardError):
                        split.validate_target_obligation(
                            config,
                            changed,
                            metadata,
                        )

    def test_active_final_clause_removal_fails_closed(self) -> None:
        config = next(config for config in split.TARGETS if config.mutable)
        text, metadata = split.obligation(config, split.PRIMARY)
        changed = omit_call(text, "ActiveFinalReturnPartitionConjunct")
        changed_metadata = copy.deepcopy(metadata)
        changed_metadata["active_contract_conjuncts"].remove(
            "ActiveFinalReturnPartitionConjunct"
        )
        with self.assertRaises(GuardError):
            split.validate_target_obligation(
                config,
                changed,
                changed_metadata,
            )

    def test_every_principal_output_and_state_equality_is_required(self) -> None:
        for config in split.TARGETS:
            for purpose in split.PURPOSES:
                text, metadata = split.obligation(config, purpose)
                fields = list(split.OUTPUT_FIELDS)
                if purpose == split.PRIMARY:
                    fields.extend(split.STATE_FIELDS)
                for selector, _ in fields:
                    left = "y1" if selector.startswith("y_") else "s1"
                    right = "y2" if selector.startswith("y_") else "s2"
                    equality = f"(= ({selector} {left}) ({selector} {right}))"
                    with self.subTest(
                        target=config.target,
                        purpose=purpose,
                        selector=selector,
                    ):
                        self.assertIn(equality, text)
                        with self.assertRaises(GuardError):
                            split.validate_target_obligation(
                                config,
                                text.replace(equality, "true", 1),
                                metadata,
                            )

    def test_answer_bearing_and_laundered_boundaries_fail_closed(self) -> None:
        config = split.TARGETS[0]
        text, metadata = split.obligation(config, split.EXACT_OUTPUT)
        expanded = text.replace(
            "      (b_element_alignment Int))))",
            "      (b_element_alignment Int)\n"
            "      (b_split_answer Int))))",
            1,
        )
        answer_bearing = expanded.replace(
            "       (= (b_element_alignment b) (x_element_alignment x))))",
            "       (= (b_element_alignment b) (x_element_alignment x))\n"
            "       (= (b_split_answer b) (x_range_index x))))",
            1,
        )
        answer_metadata = copy.deepcopy(metadata)
        answer_metadata["boundary_fields"].append(
            {
                "selector": "b_split_answer",
                "role": "selected_output",
                "meaning": "laundered split answer",
                "source_citations": list(config.source_citations),
                "trust_site_ids": [],
                "source_backed_replacement_ids": list(config.replacement_ids),
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(answer_bearing, answer_metadata)

        laundered = answer_bearing.replace(
            "(= (y_return_allocation y) (x_allocation x))",
            "(= (y_return_allocation y)\n"
            "   (+ (b_split_answer b)\n"
            "      (- (x_range_index x) (x_range_index x))))",
            1,
        )
        self.assertNotEqual(laundered, answer_bearing)
        laundering_metadata = copy.deepcopy(answer_metadata)
        laundering_metadata["boundary_fields"][-1]["role"] = "input_memory"
        with self.assertRaises(GuardError):
            validate_obligation(laundered, laundering_metadata)

    def test_mismatched_shared_input_and_boundary_fail_closed(self) -> None:
        config = split.TARGETS[0]
        text, metadata = split.obligation(config, split.PRIMARY)
        mismatched_input = text.replace(
            "(declare-const b Boundary)",
            "(declare-const x2 Input)\n(declare-const b Boundary)",
            1,
        ).replace(
            "(Spec_T x b y2 s2)",
            "(Spec_T x2 b y2 s2)",
            1,
        )
        with self.assertRaises(GuardError):
            split.validate_target_obligation(
                config,
                mismatched_input,
                metadata,
            )
        mismatched_boundary = text.replace(
            "(declare-const y1 Output)",
            "(declare-const b2 Boundary)\n(declare-const y1 Output)",
            1,
        ).replace(
            "(Spec_T x b y2 s2)",
            "(Spec_T x b2 y2 s2)",
            1,
        )
        with self.assertRaises(GuardError):
            split.validate_target_obligation(
                config,
                mismatched_boundary,
                metadata,
            )

    def test_required_source_cases_are_sat_with_models(self) -> None:
        self.assertEqual(len(split.SOURCE_CASES), 14)
        for config in split.TARGETS:
            for name, case in split.SOURCE_CASES.items():
                process = run_z3(split.source_instance_text(config, case))
                with self.subTest(target=config.target, case=name):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertTrue(process.stdout.startswith("sat\n"))
                    self.assertIn("(x_range_kind x)", process.stdout)
                    self.assertIn("(x_range_index x)", process.stdout)
                    self.assertIn("(s_split_index s1)", process.stdout)
                    self.assertEqual(process.stderr, "")

    def test_semantic_negative_probes_are_unsat(self) -> None:
        self.assertEqual(len(split.NEGATIVE_PROBES), 10)
        for config in split.TARGETS:
            for name in split.NEGATIVE_PROBES:
                process = run_z3(split.negative_probe_text(config, name))
                with self.subTest(target=config.target, probe=name):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, "unsat\n")
                    self.assertEqual(process.stderr, "")

    def test_both_theorem_projections_are_unsat(self) -> None:
        for config in split.TARGETS:
            for purpose in split.PURPOSES:
                process = run_z3(split.obligation_text(config, purpose))
                with self.subTest(target=config.target, purpose=purpose):
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
            not in set(runner.BASELINE_RESULTS) | set(split.TARGET_KEYS)
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

    def test_generated_verus_models_are_target_specific_and_trusted_free(
        self,
    ) -> None:
        for config in split.TARGETS:
            text = split.verus_text(config)
            function = config.function_name
            with self.subTest(target=config.target):
                self.assertNotIn("external_body", text)
                self.assertIn("helper_split_index", text)
                self.assertIn("front_region", text)
                self.assertIn("back_region", text)
                self.assertIn("source_output", text)
                self.assertIn("source_state", text)
                self.assertIn(f"conditional_complete_{function}", text)
                self.assertIn(
                    f"conditional_complete_exact_output_{function}",
                    text,
                )
                if config.mutable:
                    self.assertIn(
                        "state.returned_final.values",
                        text,
                    )

    def test_local_result_summary_reports_56_classified_6_not_run(
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
        for order in ("099", "104"):
            self.assertIn(f"{order}_conditional-complete", summary)
        self.assertTrue(summary.endswith(",0_not-run"))
        self.assertEqual(
            authority_validator.target_result_count_summary(rows),
            "target_result_counts=62_classified,0_not-run",
        )


if __name__ == "__main__":
    unittest.main()
