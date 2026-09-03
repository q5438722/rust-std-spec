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
import mutable_view_construction_cluster as cluster
import mutable_view_construction_validation as cluster_validation
import run_mutable_view_construction_cluster as runner
import target_pipeline
import validate_authority_design as authority_validator


def run_z3(text: str) -> subprocess.CompletedProcess[str]:
    z3 = shutil.which("z3")
    if not z3:
        raise AssertionError("z3 is unavailable")
    return subprocess.run(
        [z3, "-in", "-smt2"],
        input=text,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


def authority_row(
    config: cluster.MutableViewTarget,
) -> dict[str, str]:
    return next(
        row
        for row in common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        if (row["target"], row["input_order"])
        == (config.target, config.input_order)
    )


def source_inputs(
    config: cluster.MutableViewTarget,
) -> tuple[str, str, str, dict[str, str]]:
    row = authority_row(config)
    vocabulary_lines = Path(
        row["shared_vocabulary_path"]
    ).read_text().splitlines(keepends=True)
    vocabulary = "\n".join(
        "".join(vocabulary_lines[start - 1 : end])
        for start, end in cluster.VOCABULARY_RANGES
    )
    helpers = {}
    for source in config.helper_sources:
        lines = (
            common.RUST_LIBRARY / source.path
        ).read_text().splitlines(keepends=True)
        helpers[source.name] = "".join(
            lines[source.start - 1 : source.end]
        )
    return (
        row["source_item_text"],
        row["public_docs_text"],
        vocabulary,
        helpers,
    )


class MutableViewConstructionTests(unittest.TestCase):
    def test_all_authority_and_trust_bindings_are_literal(self) -> None:
        trust = common.read_csv(ROOT / "crosswalk/trust_site_inventory.csv")
        total = 0
        for config in cluster.TARGETS:
            row = authority_row(config)
            records = {
                item["record_id"]: item
                for item in trust
                if (item["target"], item["input_order"])
                == (config.target, config.input_order)
            }
            total += len(records)
            with self.subTest(target=config.target):
                self.assertEqual(
                    row["active_contract_text"],
                    config.active_contract_text,
                )
                self.assertEqual(
                    row["active_contract_sha256"],
                    config.active_contract_sha256,
                )
                self.assertEqual(
                    row["generated_declaration_sha256"],
                    config.generated_declaration_sha256,
                )
                self.assertEqual(
                    row["source_item_sha256"],
                    config.source_item_sha256,
                )
                self.assertEqual(
                    row["public_docs_sha256"],
                    config.public_docs_sha256,
                )
                self.assertEqual(set(records), set(config.all_trust_site_ids))
                self.assertEqual(
                    {
                        record_id: cluster.canonical_json_sha256(record)
                        for record_id, record in records.items()
                    },
                    config.trust_hashes,
                )
                self.assertTrue(
                    all(
                        records[record_id][
                            "semantic_disposition"
                        ].startswith("inadmissible")
                        for record_id in config.excluded_trust_site_ids
                    )
                )
        self.assertEqual(total, 34)

    def test_source_docs_vocabulary_and_helpers_fail_closed(self) -> None:
        for config in cluster.TARGETS:
            inputs = source_inputs(config)
            cluster.validate_source_anchors(config, *inputs)
            source, docs, vocabulary, helpers = inputs
            source_mutation = source.replace(
                config.source_fragments[-1],
                "synthetic source result",
                1,
            )
            with self.subTest(target=config.target, mutation="source"):
                with self.assertRaises(GuardError):
                    cluster.validate_source_anchors(
                        config,
                        source_mutation,
                        docs,
                        vocabulary,
                        helpers,
                    )
            docs_mutation = docs.replace(
                config.docs_fragments[-1],
                "synthetic docs",
                1,
            )
            with self.subTest(target=config.target, mutation="docs"):
                with self.assertRaises(GuardError):
                    cluster.validate_source_anchors(
                        config,
                        source,
                        docs_mutation,
                        vocabulary,
                        helpers,
                    )
            if config.vocabulary_fragments:
                changed = vocabulary.replace(
                    config.vocabulary_fragments[-1],
                    "synthetic vocabulary",
                    1,
                )
                with self.subTest(
                    target=config.target, mutation="vocabulary"
                ):
                    with self.assertRaises(GuardError):
                        cluster.validate_source_anchors(
                            config,
                            source,
                            docs,
                            changed,
                            helpers,
                        )
            helper = config.helper_sources[0]
            changed_helpers = dict(helpers)
            changed_helpers[helper.name] = changed_helpers[
                helper.name
            ].replace(helper.fragments[-1], "synthetic helper", 1)
            with self.subTest(target=config.target, mutation="helper"):
                with self.assertRaises(GuardError):
                    cluster.validate_source_anchors(
                        config,
                        source,
                        docs,
                        vocabulary,
                        changed_helpers,
                    )

    def test_array_from_mut_excerpt_is_project_local_and_exact(self) -> None:
        config = cluster.TARGET_BY_ARTIFACT[
            "047_core_slice_from_mut"
        ]
        helpers = source_inputs(config)[-1]
        excerpt = helpers["array_from_mut"]
        self.assertEqual(
            common.sha256_text(excerpt),
            cluster.ARRAY_FROM_MUT_EXCERPT_SHA256,
        )
        local = (
            ROOT
            / "evidence/mutable_view_construction_cluster/source_excerpts"
            / "core_array_from_mut_174_177.rs"
        )
        self.assertEqual(local.read_text(), excerpt)
        self.assertFalse(
            str(local).startswith(str(ROOT / "provenance/frozen"))
        )

    def test_literal_theorems_use_one_shared_genuine_boundary(self) -> None:
        expected_boundary = {
            selector for selector, _, _ in cluster.BOUNDARY_FIELDS
        }
        for config in cluster.TARGETS:
            for purpose in cluster.PURPOSES:
                text, metadata = cluster.obligation(config, purpose)
                with self.subTest(target=config.target, purpose=purpose):
                    validate_obligation(text, metadata)
                    cluster.validate_target_obligation(
                        config, text, metadata
                    )
                    self.assertIn(
                        """(and (Requires_T x)
           (Boundary_T x b)
           (Spec_T x b y1 s1)
           (Spec_T x b y2 s2))""",
                        text,
                    )
                    self.assertEqual(
                        {
                            item["selector"]
                            for item in metadata["boundary_fields"]
                        },
                        expected_boundary,
                    )
                    self.assertTrue(
                        metadata["boundary_scope"]["narrower_than_target"]
                    )
                    for token in (
                        "b_output",
                        "b_result",
                        "b_return",
                        "b_final",
                        "b_trace",
                        "b_product",
                        "b_branch",
                    ):
                        self.assertNotIn(token, text)

    def test_source_transitions_and_exact_equalities_are_live(self) -> None:
        for config in cluster.TARGETS:
            for purpose in cluster.PURPOSES:
                text, metadata = cluster.obligation(config, purpose)
                for symbol in metadata["source_transition_definitions"]:
                    with self.subTest(
                        target=config.target,
                        purpose=purpose,
                        symbol=symbol,
                    ):
                        self.assertIn(f"(define-fun {symbol}", text)
                for observation in metadata["principal_observations"]:
                    selector = observation["selector"]
                    left = (
                        "y1"
                        if observation["left"] == "output1"
                        else "s1"
                    )
                    right = (
                        "y2"
                        if observation["right"] == "output2"
                        else "s2"
                    )
                    equality = (
                        f"(= ({selector} {left}) ({selector} {right}))"
                    )
                    self.assertIn(equality, text)
                    with self.assertRaises(GuardError):
                        cluster.validate_target_obligation(
                            config,
                            text.replace(equality, "true", 1),
                            metadata,
                        )

    def test_answer_bearing_and_laundered_boundaries_fail_closed(self) -> None:
        config = cluster.TARGETS[0]
        text, metadata = cluster.obligation(config, cluster.PRIMARY)
        changed_metadata = copy.deepcopy(metadata)
        changed_metadata["boundary_fields"][0]["role"] = "selected_output"
        with self.assertRaises(GuardError):
            validate_obligation(text, changed_metadata)

        boundary_tail = "      (b_outside_frame (Seq Int))))"
        self.assertIn(boundary_tail, text)
        expanded = text.replace(
            boundary_tail,
            "      (b_outside_frame (Seq Int))\n"
            "      (b_selected_length Int))))",
            1,
        )
        observed_tail = (
            "       (= (b_outside_frame b) (x_outside_frame x))))"
        )
        self.assertIn(observed_tail, expanded)
        expanded = expanded.replace(
            observed_tail,
            "       (= (b_outside_frame b) (x_outside_frame x))\n"
            "       (= (b_selected_length b) (x_n x))))",
            1,
        )
        target_head = (
            "(define-fun TargetDefinition_T\n"
            "  ((x Input) (b Boundary) (y Output) (s State)) Bool\n"
            "  (and "
        )
        self.assertIn(target_head, expanded)
        laundered = expanded.replace(
            target_head,
            target_head
            + "(= (y_length y)\n"
            "          (+ (b_selected_length b) (- (x_n x) (x_n x))))\n"
            "       ",
            1,
        )
        laundering_metadata = copy.deepcopy(metadata)
        laundering_metadata["boundary_fields"].append(
            {
                "selector": "b_selected_length",
                "role": "input_memory",
                "source_citations": list(config.source_citations),
                "trust_site_ids": list(config.admitted_trust_site_ids),
                "source_backed_replacement_ids": [config.replacement_id],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(laundered, laundering_metadata)

    def test_required_source_cases_are_sat_with_models(self) -> None:
        expected_names = {
            "17": {
                "empty_n0",
                "empty_n_positive",
                "nonempty_n0",
                "nonzst_valid_unchecked_mul",
                "zst_valid_checked_mul",
                "zst_checked_mul_overflow",
            },
            "18": {
                "empty_n0",
                "empty_n_positive",
                "nonempty_n0",
                "n_less_than_length",
                "n_equal_length",
                "n_greater_than_length",
                "zst_n_equal_length",
            },
            "46": {
                "empty_n0",
                "empty_n_positive",
                "nonempty_n0",
                "n_less_than_length",
                "n_equal_length",
                "n_greater_than_length",
                "zst_n_less_than_length",
            },
            "47": {"singleton_nonzst", "singleton_zst"},
        }
        for config in cluster.TARGETS:
            cases = cluster.source_cases(config)
            self.assertEqual(set(cases), expected_names[config.input_order])
            for name, case in cases.items():
                process = run_z3(
                    cluster.source_instance_text(config, name)
                )
                with self.subTest(target=config.target, case=name):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stderr, "")
                    self.assertTrue(process.stdout.startswith("sat\n"))
                    self.assertIn("(y_length y1)", process.stdout)
                    outcome = cluster.evaluate_source(config, case)
                    if name == "zst_checked_mul_overflow":
                        self.assertEqual(outcome["kind"], "panic")
                    if name == "nonzst_valid_unchecked_mul":
                        self.assertEqual(outcome["length"], 6)

    def test_all_invalid_and_wrong_transition_probes_are_unsat(self) -> None:
        for config in cluster.TARGETS:
            for name in cluster.negative_probe_names(config):
                process = run_z3(
                    cluster.negative_probe_text(config, name)
                )
                with self.subTest(target=config.target, probe=name):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stderr, "")
                    self.assertEqual(process.stdout, "unsat\n")

    def test_exact_output_theorems_are_direct_unsat(self) -> None:
        for config in cluster.TARGETS:
            process = run_z3(
                cluster.obligation_text(config, cluster.EXACT_OUTPUT)
            )
            with self.subTest(target=config.target):
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stderr, "")
                self.assertEqual(process.stdout, "unsat\n")

    def test_full_state_theorems_and_fixed_witnesses_are_sat(self) -> None:
        for config in cluster.TARGETS:
            theorem = run_z3(
                cluster.obligation_text(config, cluster.PRIMARY)
            )
            witness = run_z3(
                cluster.fixed_full_state_witness_text(config)
            )
            payload = cluster.witness_payload(config)
            with self.subTest(target=config.target):
                self.assertEqual(theorem.returncode, 0, theorem.stderr)
                self.assertEqual(theorem.stderr, "")
                self.assertEqual(theorem.stdout, "sat\n")
                self.assertEqual(witness.returncode, 0, witness.stderr)
                self.assertEqual(witness.stderr, "")
                self.assertTrue(witness.stdout.startswith("sat\n"))
                self.assertIn("(s_return_final s1)", witness.stdout)
                self.assertIn("(s_return_final s2)", witness.stdout)
                self.assertIn(
                    "(Equivalent_T x b y1 s1 y2 s2)",
                    witness.stdout,
                )
                self.assertIn("false", witness.stdout)
                self.assertTrue(
                    payload["shared_boundary"][
                        "same_for_both_executions"
                    ]
                )
                self.assertTrue(
                    payload["expected"][
                        "both_executions_satisfy_every_active_conjunct"
                    ]
                )
                self.assertFalse(
                    payload["expected"]["full_state_equal"]
                )

    def test_trusted_free_verus_models_are_target_specific(self) -> None:
        for config in cluster.TARGETS:
            text = cluster.verus_text(config)
            with self.subTest(target=config.target):
                self.assertNotIn("external_body", text)
                self.assertIn("checked_length_multiplication", text)
                self.assertIn("mutable_pointer_extraction", text)
                self.assertIn("pointer_cast", text)
                self.assertIn("raw_slice_or_array_reference", text)
                self.assertIn("singleton_array_unsize", text)
                self.assertIn("borrow_lifetime_final_frame", text)
                self.assertIn("borrow_lifetime_state", text)
                self.assertIn(
                    f"exact_output_conditional_complete_{config.function_name}",
                    text,
                )
                self.assertIn(
                    f"full_state_conditional_incomplete_{config.function_name}",
                    text,
                )

    def test_runner_reset_changes_only_the_four_assigned_rows(self) -> None:
        csv_rows, json_rows = runner._load_crosswalks()
        reset_csv, reset_json = runner.prepare_crosswalk_reset(
            csv_rows, json_rows
        )
        self.assertEqual(reset_csv, reset_json)
        before = {
            (row["target"], row["input_order"]): row for row in csv_rows
        }
        after = {
            (row["target"], row["input_order"]): row for row in reset_csv
        }
        for key in before:
            changed = {
                field
                for field in before[key]
                if before[key][field] != after[key][field]
            }
            if key in set(cluster.TARGET_KEYS):
                self.assertLessEqual(
                    changed, set(target_pipeline.RESULT_FIELDS)
                )
            else:
                self.assertFalse(changed)

    def test_final_ledger_and_dedicated_validator(self) -> None:
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
        errors: list[str] = []
        cluster_validation.validate(errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
