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
import mutable_fixed_chunk_edges as fixed
import run_mutable_fixed_chunk_edges as runner
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


def canonical_path(
    source: fixed.CanonicalSource,
    row: dict[str, str],
) -> Path:
    if source.path == fixed.SLICE_SOURCE_PATH:
        return Path(row["source_path"])
    return common.RUST_LIBRARY / source.path


def source_inputs(
    config: fixed.FixedChunkTarget,
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
        for start, end in fixed.VOCABULARY_RANGES
    )
    helpers = {}
    for source in config.helper_sources:
        lines = canonical_path(source, row).read_text().splitlines(
            keepends=True
        )
        helpers[source.name] = "".join(lines[source.start - 1 : source.end])
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


class MutableFixedChunkEdgeTests(unittest.TestCase):
    def test_active_contracts_and_all_22_trust_records_match_authority(
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
        for config in fixed.TARGETS:
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
                replaced = {
                    site
                    for replacement in config.source_backed_replacements
                    for site in replacement.replaces_trust_site_ids
                }
                self.assertEqual(replaced, set(config.excluded_trust_site_ids))
        self.assertEqual(total, 22)

    def test_target_vocabulary_and_canonical_helpers_fail_closed(self) -> None:
        for config in fixed.TARGETS:
            source, vocabulary, helpers = source_inputs(config)
            fixed.validate_source_anchors(
                config,
                source,
                vocabulary,
                helpers,
            )
            with self.subTest(target=config.target, mutation="target"):
                changed = source.replace(config.source_fragments[0], "source drift")
                self.assertNotEqual(changed, source)
                with self.assertRaises(GuardError):
                    fixed.validate_source_anchors(
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
                    fixed.validate_source_anchors(
                        config,
                        source,
                        vocabulary,
                        changed_helpers,
                    )
            synthetic = dict(helpers)
            synthetic[helper.name] += "\nProvenance::null()\n"
            with self.subTest(target=config.target, mutation="synthetic"):
                with self.assertRaises(GuardError):
                    fixed.validate_source_anchors(
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
        }
        for config in fixed.TARGETS:
            for purpose in fixed.PURPOSES:
                text, metadata = fixed.obligation(config, purpose)
                with self.subTest(target=config.target, purpose=purpose):
                    validate_obligation(text, metadata)
                    fixed.validate_target_obligation(config, text, metadata)
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
                    self.assertNotIn("b_n", text)

    def test_source_transitions_and_contract_conjuncts_are_live(self) -> None:
        for config in fixed.TARGETS:
            text, metadata = fixed.obligation(config, fixed.PRIMARY)
            for symbol in fixed.SOURCE_TRANSITIONS:
                with self.subTest(target=config.target, transition=symbol):
                    self.assertIn(f"(define-fun {symbol}", text)
                    with self.assertRaises(GuardError):
                        fixed.validate_target_obligation(
                            config,
                            omit_call(text, symbol),
                            metadata,
                        )
            for symbol in config.active_conjuncts:
                with self.subTest(target=config.target, conjunct=symbol):
                    self.assertIn(f"(define-fun {symbol}", text)
                    with self.assertRaises(GuardError):
                        fixed.validate_target_obligation(
                            config,
                            omit_call(text, symbol),
                            metadata,
                        )

    def test_branch_split_cast_tuple_provenance_borrow_and_frame_fail_closed(
        self,
    ) -> None:
        for config in fixed.TARGETS:
            text, metadata = fixed.obligation(config, fixed.PRIMARY)
            split = (
                "(x_n x)"
                if config.kind == "split_first"
                else "(- (x_length x) (x_n x))"
            )
            mutations = {
                "branch": text.replace(
                    "(= (y_is_some y) (<= (x_n x) (x_length x)))",
                    "(= (y_is_some y) (> (x_n x) (x_length x)))",
                    1,
                ),
                "checked-index": text.replace(
                    f"(ite (<= (x_n x) (x_length x)) {split} (- 1))",
                    "(ite (<= (x_n x) (x_length x)) 0 (- 1))",
                    1,
                ),
                "split-range": text.replace(
                    f"(= (s_prefix_length s) {split})",
                    "(= (s_prefix_length s) (x_length x))",
                    1,
                ),
                "tuple-order": text.replace(
                    f"(ite (<= (x_n x) (x_length x)) "
                    f"{config.tuple_array_position} (- 1))",
                    "(ite (<= (x_n x) (x_length x)) 9 (- 1))",
                    1,
                ),
                "unchecked-array-length": text.replace(
                    "(= (y_array_length y) (x_n x))",
                    "(= (y_array_length y) (+ (x_n x) 1))",
                    1,
                ),
                "synthetic-provenance": text.replace(
                    "(= (y_array_provenance y) (x_provenance x))",
                    "(= (y_array_provenance y) 0)",
                    1,
                ),
                "allocation-loss": text.replace(
                    "(= (y_array_allocation y) (x_allocation x))",
                    "(= (y_array_allocation y) 0)",
                    1,
                ),
                "borrow-loss": text.replace(
                    "(= (y_array_parent_borrow y) (x_parent_borrow x))",
                    "(= (y_array_parent_borrow y) 0)",
                    1,
                ),
                "address-disjoint-zst": text.replace(
                    "(<= (+ (s_prefix_start s) (s_prefix_length s))\n"
                    "              (s_suffix_start s))",
                    "(distinct (s_prefix_address s) (s_suffix_address s))",
                    1,
                ),
                "final-frame": text.replace(
                    "(= (s_composed_final s) (x_source x))",
                    f"(= (s_composed_final s) {fixed.EMPTY_SEQ})",
                    1,
                ),
            }
            for name, changed in mutations.items():
                with self.subTest(target=config.target, mutation=name):
                    self.assertNotEqual(changed, text)
                    with self.assertRaises(GuardError):
                        fixed.validate_target_obligation(
                            config,
                            changed,
                            metadata,
                        )

    def test_every_principal_output_and_state_equality_is_required(self) -> None:
        for config in fixed.TARGETS:
            for purpose in fixed.PURPOSES:
                text, metadata = fixed.obligation(config, purpose)
                fields = list(fixed.OUTPUT_FIELDS)
                if purpose == fixed.PRIMARY:
                    fields.extend(fixed.STATE_FIELDS)
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
                            fixed.validate_target_obligation(
                                config,
                                text.replace(equality, "true", 1),
                                metadata,
                            )

    def test_answer_bearing_and_laundered_boundaries_fail_closed(self) -> None:
        config = next(item for item in fixed.TARGETS if item.kind == "split_first")
        text, metadata = fixed.obligation(config, fixed.PRIMARY)
        expanded = text.replace(
            "      (b_element_size Int))))",
            "      (b_element_size Int)\n"
            "      (b_split_answer Int))))",
            1,
        )
        answer_bearing = expanded.replace(
            "       (= (b_element_size b) (x_element_size x))))",
            "       (= (b_element_size b) (x_element_size x))\n"
            "       (= (b_split_answer b) (x_n x))))",
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
            "(ite (<= (x_n x) (x_length x)) (x_n x) (- 1))",
            "(ite (<= (x_n x) (x_length x)) "
            "(+ (b_split_answer b) (- (x_length x) (x_length x))) (- 1))",
            1,
        )
        laundering_metadata = copy.deepcopy(answer_metadata)
        laundering_metadata["boundary_fields"][-1]["role"] = "input_memory"
        with self.assertRaises(GuardError):
            validate_obligation(laundered, laundering_metadata)

    def test_mismatched_second_boundary_fails_closed(self) -> None:
        config = fixed.TARGETS[0]
        text, metadata = fixed.obligation(config, fixed.PRIMARY)
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
            fixed.validate_target_obligation(config, changed, metadata)

    def test_required_source_cases_are_sat_with_models(self) -> None:
        self.assertEqual(
            set(fixed.SOURCE_CASES),
            {
                "empty_n0",
                "empty_n_positive",
                "nonempty_n0",
                "n_greater_than_length",
                "n_equal_length",
                "strict_interior",
                "zst_equal_addresses",
            },
        )
        for config in fixed.TARGETS:
            for name, case in fixed.SOURCE_CASES.items():
                process = run_z3(fixed.source_instance_text(config, case))
                with self.subTest(target=config.target, case=name):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertTrue(process.stdout.startswith("sat\n"))
                    self.assertIn("(x_n x)", process.stdout)
                    self.assertIn("(y_split_index y1)", process.stdout)
                    self.assertEqual(process.stderr, "")

    def test_semantic_negative_probes_are_unsat(self) -> None:
        for config in fixed.TARGETS:
            for name in fixed.NEGATIVE_PROBES:
                process = run_z3(fixed.negative_probe_text(config, name))
                with self.subTest(target=config.target, probe=name):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, "unsat\n")
                    self.assertEqual(process.stderr, "")

    def test_both_literal_theorem_projections_are_unsat(self) -> None:
        for config in fixed.TARGETS:
            for purpose in fixed.PURPOSES:
                process = run_z3(fixed.obligation_text(config, purpose))
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
            not in set(runner.BASELINE_RESULTS) | set(fixed.TARGET_KEYS)
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
        for config in fixed.TARGETS:
            text = fixed.verus_text(config)
            function = config.function_name
            with self.subTest(target=config.target):
                self.assertNotIn("external_body", text)
                self.assertIn("raw_parts_split", text)
                self.assertIn("as_mut_ptr_transition", text)
                self.assertIn("cast_array_transition", text)
                self.assertIn("dereference_array_transition", text)
                self.assertIn(f"conditional_complete_{function}", text)
                self.assertIn(
                    f"conditional_complete_exact_output_{function}",
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
        for order in ("062", "090", "096"):
            self.assertIn(f"{order}_conditional-complete", summary)
        self.assertTrue(summary.endswith(",0_not-run"))
        self.assertEqual(
            authority_validator.target_result_count_summary(rows),
            "target_result_counts=62_classified,0_not-run",
        )


if __name__ == "__main__":
    unittest.main()
