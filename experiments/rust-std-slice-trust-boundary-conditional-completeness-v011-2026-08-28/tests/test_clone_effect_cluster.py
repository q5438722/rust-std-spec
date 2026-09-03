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
import clone_effect_cluster as cluster
import exact_mutable_iterator_partitions as exact_partitions
import mutable_fixed_chunk_edges as fixed_chunks
import run_clone_effect_cluster as runner
import split_at_mut_primitives as split_primitives
import split_off_pair as split_off
import raw_slice_pair as raw_slice
import slice_index_trio as slice_trio
import address_observer_pair as address_pair
import mutable_view_construction_cluster as mutable_views
import target_pipeline


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


def definition_span(text: str, symbol: str) -> tuple[int, int]:
    markers = (f"(define-fun {symbol}", f"(define-fun-rec {symbol}")
    start = next(text.index(marker) for marker in markers if marker in text)
    balance = 0
    for end in range(start, len(text)):
        if text[end] == "(":
            balance += 1
        elif text[end] == ")":
            balance -= 1
            if balance == 0:
                return start, end + 1
    raise AssertionError(f"unterminated definition {symbol}")


class CloneEffectClusterTests(unittest.TestCase):
    def test_active_contracts_hashes_and_trust_partitions_match(self) -> None:
        rows = {
            (row["target"], row["input_order"]): row
            for row in common.read_csv(
                ROOT / "crosswalk/target_to_proof_boundary.csv"
            )
        }
        trust_rows = common.read_csv(
            ROOT / "crosswalk/trust_site_inventory.csv"
        )
        for config in cluster.TARGETS:
            row = rows[(config.target, config.input_order)]
            records = {
                record["record_id"]: record
                for record in trust_rows
                if (record["target"], record["input_order"])
                == (config.target, config.input_order)
            }
            with self.subTest(target=config.target):
                self.assertEqual(
                    row["active_contract_sha256"],
                    config.active_contract_sha256,
                )
                self.assertEqual(
                    row["active_contract_text"],
                    config.active_contract_text,
                )
                self.assertEqual(
                    row["generated_declaration_sha256"],
                    config.generated_declaration_sha256,
                )
                self.assertEqual(
                    row["source_item_sha256"],
                    config.source_item_sha256,
                )
                self.assertEqual(set(records), set(config.all_trust_site_ids))
                self.assertTrue(
                    all(
                        records[record_id]["target_postcondition_coverage"]
                        == "partial-or-lower-level"
                        for record_id in config.admitted_trust_site_ids
                    )
                )
                self.assertTrue(
                    all(
                        records[record_id]["semantic_disposition"].startswith(
                            "context-only-"
                        )
                        for record_id in config.context_only_trust_site_ids
                    )
                )

    def test_all_public_helper_specialization_and_vocabulary_anchors(self) -> None:
        rows = {
            (row["target"], row["input_order"]): row
            for row in common.read_csv(
                ROOT / "crosswalk/target_to_proof_boundary.csv"
            )
        }
        vocabulary_lines = (
            ROOT
            / "provenance/frozen/specgen/specs/slice_shared_vocabulary.rs"
        ).read_text().splitlines(keepends=True)
        vocabulary = "".join(
            vocabulary_lines[
                cluster.VOCABULARY_RANGE[0] - 1 :
                cluster.VOCABULARY_RANGE[1]
            ]
        )
        slice_source = common.RUST_LIBRARY / cluster.CANONICAL_SLICE_PATH
        slice_lines = slice_source.read_text().splitlines(keepends=True)
        clone_helper = "".join(slice_lines[5555:5628])
        fill_helper = (
            common.RUST_LIBRARY / cluster.SPECIALIZE_PATH
        ).read_text()
        for config in cluster.TARGETS:
            source_item = rows[(config.target, config.input_order)][
                "source_item_text"
            ]
            helper = fill_helper if config.is_fill else clone_helper
            cluster.validate_source_anchors(
                config,
                source_item,
                helper,
                vocabulary,
            )
            with self.subTest(target=config.target):
                with self.assertRaises(GuardError):
                    cluster.validate_source_anchors(
                        config,
                        source_item,
                        helper.replace(
                            (
                                "crate::intrinsics::is_val_statically_known(value)"
                                if config.is_fill
                                else "self[idx].clone_from(&src[idx]);"
                            ),
                            "removed_source_transition",
                            1,
                        ),
                        vocabulary,
                    )
                with self.assertRaises(GuardError):
                    cluster.validate_source_anchors(
                        config,
                        source_item,
                        helper,
                        vocabulary.replace("cloned::<T>", "source == dest"),
                    )

    def test_literal_shared_input_boundary_theorems_are_guarded(self) -> None:
        literal = """(and (Requires_T x)
           (Boundary_T x b)
           (Spec_T x b y1 s1)
           (Spec_T x b y2 s2))"""
        for config in cluster.TARGETS:
            for purpose in cluster.PURPOSES:
                text, metadata = cluster.obligation(config, purpose)
                with self.subTest(target=config.target, purpose=purpose):
                    self.assertIn(literal, text)
                    validate_obligation(text, metadata)
                    cluster.validate_target_obligation(
                        config,
                        text,
                        metadata,
                    )

    def test_normal_and_panic_theorems_are_clean_unsat(self) -> None:
        for config in cluster.TARGETS:
            texts = [
                cluster.obligation_text(config, purpose)
                for purpose in cluster.PURPOSES
            ]
            texts.append(cluster.panic_obligation_text(config))
            if not config.is_fill:
                texts.append(cluster.mismatch_obligation_text(config))
            for index, text in enumerate(texts):
                process = run_z3(text)
                with self.subTest(target=config.target, obligation=index):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, "unsat\n")
                    self.assertEqual(process.stderr, "")

    def test_every_source_path_has_a_replayable_sat_model(self) -> None:
        expected_fill_paths = {
            cluster.PATH_FILL_DEFAULT,
            cluster.PATH_FILL_TRIVIAL_READ,
            cluster.PATH_FILL_U8_BYTES,
            cluster.PATH_FILL_I8_BYTES,
            cluster.PATH_FILL_INTEGER_BYTES,
            cluster.PATH_FILL_INTEGER_LOOP,
        }
        observed_fill_paths: set[int] = set()
        for config in cluster.TARGETS:
            cases = cluster.SOURCE_CASES[config.artifact_id]
            for case in cases:
                observed_fill_paths.add(
                    case.expected_path if config.is_fill else -1
                )
                process = run_z3(cluster.source_instance_text(config, case))
                with self.subTest(target=config.target, case=case.name):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertTrue(process.stdout.startswith("sat\n("))
                    self.assertEqual(process.stderr, "")
        observed_fill_paths.discard(-1)
        self.assertEqual(observed_fill_paths, expected_fill_paths)

    def test_generic_clone_results_are_relational_not_equality(self) -> None:
        for config in cluster.TARGETS:
            case = next(
                item
                for item in cluster.SOURCE_CASES[config.artifact_id]
                if item.relation_valued and item.length > 0
            )
            text = cluster.source_instance_text(config, case)
            process = run_z3(text)
            self.assertEqual(process.stdout.splitlines()[0], "sat")
            mutated = cluster._replace_definition(
                text,
                "ResultValueAt",
                """(define-fun ResultValueAt
  ((x Input) (b Boundary) (index Int)) Int
  (SourceValueAt x index))""",
            ).replace("(get-model)\n", "")
            process = run_z3(mutated)
            with self.subTest(target=config.target):
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, "unsat\n")
                self.assertEqual(process.stderr, "")

    def test_callback_order_count_and_state_chain_fail_closed(self) -> None:
        for config in cluster.TARGETS:
            text, metadata = cluster.obligation(config, cluster.PRIMARY)
            mutations = [
                text.replace(
                    "(define-fun CloneIndexAtStep ((x Input) (step Int)) Int\n"
                    "  step)",
                    "(define-fun CloneIndexAtStep ((x Input) (step Int)) Int\n"
                    "  (- (CallbackOperationCount x) step 1))",
                    1,
                ),
                text.replace(
                    "(s_clone_call_count s) (CallbackOperationCount x)",
                    "(s_clone_call_count s) (- (CallbackOperationCount x) 1)",
                    1,
                ),
                text.replace(
                    "(CloneIndexAtStep x (- step 1))",
                    "(CloneIndexAtStep x step)",
                    1,
                ),
            ]
            for index, mutated in enumerate(mutations):
                with self.subTest(target=config.target, mutation=index):
                    with self.assertRaises(GuardError):
                        cluster.validate_target_obligation(
                            config,
                            mutated,
                            metadata,
                        )
            for name in ("wrong_callback_count", "broken_state_chain"):
                process = run_z3(cluster.negative_probe_text(config, name))
                self.assertEqual(process.stdout, "unsat\n")

    def test_every_reachable_bounded_panic_prefix_is_sat(self) -> None:
        for config in cluster.TARGETS:
            for index in range(3):
                process = run_z3(
                    cluster.panic_probe_text(config, index)
                )
                with self.subTest(target=config.target, panic=index):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertTrue(process.stdout.startswith("sat\n("))
                    self.assertEqual(process.stderr, "")
            text = cluster.panic_obligation_text(config)
            mutated = text.replace(
                "(< index (CallbackOperationCount x))",
                "(< (+ index 1) (CallbackOperationCount x))",
                1,
            )
            with self.assertRaises(GuardError):
                cluster.validate_panic_obligation(config, mutated)

    def test_clone_from_slice_mismatch_panics_before_effects(self) -> None:
        config = cluster.TARGET_037
        for trivial in (False, True):
            process = run_z3(
                cluster.mismatch_probe_text(config, trivial=trivial)
            )
            with self.subTest(trivial=trivial):
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertTrue(process.stdout.startswith("sat\n("))
                self.assertEqual(process.stderr, "")

    def test_fill_final_move_and_specialization_dispatch_fail_closed(self) -> None:
        config = cluster.TARGET_043
        for name in (
            "wrong_final_slot",
            "wrong_specialization_path",
            "callback_on_specialized_path",
        ):
            process = run_z3(cluster.negative_probe_text(config, name))
            with self.subTest(probe=name):
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, "unsat\n")
                self.assertEqual(process.stderr, "")
        text, metadata = cluster.obligation(config, cluster.PRIMARY)
        free_dispatch = text.replace(
            "(SelectedSpecializationPath x b)",
            "(b_destination_address b)",
            1,
        )
        with self.assertRaises(GuardError):
            cluster.validate_target_obligation(
                config,
                free_dispatch,
                metadata,
            )

    def test_hidden_intrinsic_and_answer_laundering_are_rejected(self) -> None:
        config = cluster.TARGET_043
        text, metadata = cluster.obligation(config, cluster.PRIMARY)
        anchor = "      (b_static_known Bool))))"
        self.assertIn(anchor, text)
        for selector, role in (
            ("b_selected_path_answer", "selected_output"),
            ("b_final_values_answer", "aggregate_final_state"),
        ):
            mutated = text.replace(
                anchor,
                f"      (b_static_known Bool)\n"
                f"      ({selector} Int))))",
                1,
            )
            mutated_metadata = copy.deepcopy(metadata)
            mutated_metadata["boundary_fields"].append(
                {
                    "selector": selector,
                    "role": role,
                    "meaning": "laundered answer",
                    "source_citations": [config.helper_reference],
                    "trust_site_ids": list(
                        config.admitted_trust_site_ids
                    ),
                    "source_backed_replacement_ids": [],
                }
            )
            with self.subTest(selector=selector):
                with self.assertRaises(GuardError):
                    validate_obligation(mutated, mutated_metadata)

    def test_fill_intrinsic_short_circuit_truth_table_fails_closed(self) -> None:
        config = cluster.TARGET_043
        expected = {
            "integer_static_uniform_bytes": 2,
            "integer_static_nonuniform_loop": 1,
            "integer_dynamic_loop": 1,
            "integer_miri_short_loop": 1,
            "integer_miri_long_uniform_bytes": 1,
            "integer_miri_long_nonuniform_loop": 0,
        }
        formerly_undercounted = {
            "integer_static_uniform_bytes",
            "integer_static_nonuniform_loop",
            "integer_dynamic_loop",
            "integer_miri_short_loop",
        }
        cases = {
            case.name: case
            for case in cluster.SOURCE_CASES[config.artifact_id]
        }
        target_model = cluster._model_text(
            config,
            cluster.PRIMARY,
            include_theorem=False,
        )
        selected_start, selected_end = definition_span(
            target_model,
            "SelectedSpecializationPath",
        )
        intrinsic_start, intrinsic_end = definition_span(
            target_model,
            "IntrinsicCallCount",
        )
        probe_prelude = f"""\
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_destination_length Int)
      (x_type_kind Int)
      (x_miri Bool)
      (x_value_uniform_bytes Bool)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_static_known Bool)))))
(declare-const x Input)
(declare-const b Boundary)
{target_model[selected_start:selected_end]}
{target_model[intrinsic_start:intrinsic_end]}
"""
        old_path_only_definition = f"""\
(define-fun IntrinsicCallCount ((x Input) (b Boundary)) Int
  (ite
    (= (SelectedSpecializationPath x b)
       {cluster.PATH_FILL_INTEGER_BYTES})
    1
    0))"""
        for name, expected_count in expected.items():
            case = cases[name]
            assertions = [
                f"(assert (= (x_destination_length x) {case.length}))",
                f"(assert (= (x_type_kind x) {case.type_kind}))",
                f"(assert (= (x_miri x) {str(case.miri).lower()}))",
                (
                    "(assert (= (x_value_uniform_bytes x) "
                    f"{str(case.uniform_bytes).lower()}))"
                ),
                (
                    "(assert (= (b_static_known b) "
                    f"{str(case.static_known).lower()}))"
                ),
                f"(assert (= (IntrinsicCallCount x b) {expected_count}))",
                "(check-sat)",
            ]
            probe = probe_prelude + "\n".join(assertions) + "\n"
            with self.subTest(case=name, formula="source_order"):
                self.assertEqual(
                    cluster.expected_intrinsic_call_count(config, case),
                    expected_count,
                )
                process = run_z3(probe)
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, "sat\n")
                self.assertEqual(process.stderr, "")

            old_probe = cluster._replace_definition(
                probe,
                "IntrinsicCallCount",
                old_path_only_definition,
            )
            with self.subTest(case=name, formula="former_path_only"):
                process = run_z3(old_probe)
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(
                    process.stdout,
                    "unsat\n" if name in formerly_undercounted else "sat\n",
                )
                self.assertEqual(process.stderr, "")

    def test_active_relations_cannot_be_dead(self) -> None:
        for config in cluster.TARGETS:
            text, metadata = cluster.obligation(config, cluster.PRIMARY)
            call = f"({config.active_conjuncts[1]} x b y)"
            self.assertIn(call, text)
            with self.subTest(target=config.target):
                with self.assertRaises(GuardError):
                    cluster.validate_target_obligation(
                        config,
                        text.replace(call, "true", 1),
                        metadata,
                    )

    def test_boundary_excludes_aggregate_answers_counts_and_paths(self) -> None:
        forbidden = (
            "final_values",
            "final_state",
            "write_count",
            "call_count",
            "selected_path",
            "trace",
        )
        for config in cluster.TARGETS:
            metadata = cluster.obligation_metadata(
                config,
                cluster.PRIMARY,
            )
            selectors = [
                item["selector"] for item in metadata["boundary_fields"]
            ]
            with self.subTest(target=config.target):
                self.assertTrue(
                    metadata["boundary_scope"]["narrower_than_target"]
                )
                self.assertTrue(
                    all(
                        not any(token in selector for token in forbidden)
                        for selector in selectors
                    )
                )
                if config.is_fill:
                    self.assertIn("b_static_known", selectors)
                    self.assertNotIn("b_miri_path", selectors)

    def test_out_of_scope_ledger_edit_is_rejected(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        other = next(
            (row["target"], row["input_order"])
            for row in csv_rows
            if (row["target"], row["input_order"])
            not in set(runner.BASELINE_RESULTS) | set(cluster.TARGET_KEYS)
        )
        for rows in (csv_rows, json_rows):
            row = next(
                item
                for item in rows
                if (item["target"], item["input_order"]) == other
            )
            row.update(runner.COMPLETE)
        with self.assertRaises(ValueError):
            runner.prepare_crosswalk_reset(csv_rows, json_rows)

    def test_generated_verus_models_are_target_specific_and_trusted_free(
        self,
    ) -> None:
        for config in cluster.TARGETS:
            text = cluster.verus_text(config)
            with self.subTest(target=config.target):
                self.assertNotIn("external_body", text)
                self.assertIn(
                    f"conditional_complete_{config.function_name}",
                    text,
                )
                self.assertIn("cloned_relation_at", text)
                self.assertIn("callback_chain", text)
                self.assertIn("panic_prefix", text)
                self.assertIn("selected_path", text)
                if config.is_fill:
                    self.assertIn("final_slot_moved", text)
                    self.assertIn("static_known", text)

    def test_reset_accepts_only_uniform_cluster_state(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        for rows in (csv_rows, json_rows):
            by_key = {
                (row["target"], row["input_order"]): row for row in rows
            }
            for key in (
                *exact_partitions.TARGET_KEYS,
                *fixed_chunks.TARGET_KEYS,
                *split_primitives.TARGET_KEYS,
                *split_off.TARGET_KEYS,
                *raw_slice.TARGET_KEYS,
                *slice_trio.TARGET_KEYS,
                *address_pair.TARGET_KEYS,
                *mutable_views.TARGET_KEYS,
            ):
                by_key[key].update(runner.NOT_RUN)
        reset_csv, reset_json = runner.prepare_crosswalk_reset(
            csv_rows,
            json_rows,
        )
        self.assertEqual(reset_csv, reset_json)
        selected = {
            (row["target"], row["input_order"]): {
                field: row[field]
                for field in target_pipeline.RESULT_FIELDS
            }
            for row in reset_csv
            if (row["target"], row["input_order"])
            in set(cluster.TARGET_KEYS)
        }
        self.assertEqual(
            selected,
            {key: runner.NOT_RUN for key in cluster.TARGET_KEYS},
        )


if __name__ == "__main__":
    unittest.main()
