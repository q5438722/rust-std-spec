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

import campaign_common as common
from checker_guards import GuardError, validate_obligation
import replay_slice_index_trio as replay
import run_slice_index_trio as runner
import slice_index_trio as trio
import slice_index_trio_validation as trio_validation
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
        timeout=30,
        check=False,
    )


def authority_row(config: trio.SliceIndexTarget) -> dict[str, str]:
    return next(
        row
        for row in common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        if (row["target"], row["input_order"])
        == (config.target, config.input_order)
    )


class SliceIndexTrioModelTests(unittest.TestCase):
    def test_active_contracts_and_eight_trust_records_are_exact(self) -> None:
        trust = common.read_csv(ROOT / "crosswalk/trust_site_inventory.csv")
        total = 0
        for config in trio.TARGETS:
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
                    row["active_contract_sha256"],
                    config.active_contract_sha256,
                )
                self.assertEqual(
                    row["active_contract_text"], config.active_contract_text
                )
                self.assertEqual(
                    row["generated_declaration_sha256"],
                    config.generated_declaration_sha256,
                )
                self.assertEqual(
                    row["source_item_sha256"], config.source_item_sha256
                )
                self.assertEqual(set(records), set(config.all_trust_site_ids))
                self.assertEqual(
                    {
                        record_id: trio.canonical_json_sha256(record)
                        for record_id, record in records.items()
                    },
                    config.trust_hashes,
                )
                self.assertTrue(
                    all(
                        records[record_id]["semantic_disposition"].startswith(
                            "inadmissible"
                        )
                        for record_id in config.excluded_trust_site_ids
                    )
                )
        self.assertEqual(total, 8)

    def test_all_25_sealed_rust_1_96_forms_are_unique_and_covered(self) -> None:
        expected_names = {
            "usize",
            "ops_index_range",
            "ops_range",
            "range_range",
            "ops_range_to",
            "ops_range_from",
            "range_range_from",
            "ops_range_full",
            "ops_range_inclusive",
            "range_range_inclusive",
            "ops_range_to_inclusive",
            "range_range_to_inclusive",
            "ops_bound_pair",
            "clamp_usize",
            "clamp_range_range",
            "clamp_ops_range",
            "clamp_range_range_inclusive",
            "clamp_ops_range_inclusive",
            "clamp_range_range_from",
            "clamp_ops_range_from",
            "clamp_ops_range_to",
            "clamp_range_range_to_inclusive",
            "clamp_ops_range_to_inclusive",
            "clamp_ops_range_full",
            "last",
        }
        self.assertEqual(
            {form.tag for form in trio.INDEX_FORMS}, set(range(25))
        )
        self.assertEqual(
            {form.name for form in trio.INDEX_FORMS}, expected_names
        )
        shared = trio.TARGETS[1]
        self.assertEqual(shared.input_order, "54")
        self.assertEqual(shared.covered_forms, trio.INDEX_FORMS)
        for mutable in (trio.TARGETS[0], trio.TARGETS[2]):
            self.assertEqual(
                [form.name for form in mutable.covered_forms], ["usize"]
            )

    def test_source_wrappers_vocabulary_and_impls_fail_closed(self) -> None:
        for config in trio.TARGETS:
            row = authority_row(config)
            vocabulary_lines = Path(
                row["shared_vocabulary_path"]
            ).read_text().splitlines(keepends=True)
            start, end = trio.SLICE_INDEX_VOCABULARY_RANGE
            inputs = (
                row["source_item_text"],
                row["public_docs_text"],
                "".join(vocabulary_lines[start - 1 : end]),
                (
                    common.RUST_LIBRARY / trio.SLICE_INDEX_SOURCE
                ).read_text(),
                (
                    common.RUST_LIBRARY / trio.INDEX_WRAPPER_SOURCE
                ).read_text(),
            )
            trio.validate_source_anchors(config, *inputs)
            mutations = (
                (
                    inputs[0].replace(
                        config.wrapper_fragment, "synthetic result", 1
                    ),
                    *inputs[1:],
                ),
                (
                    inputs[0],
                    inputs[1],
                    inputs[2].replace(
                        "pub uninterp spec fn slice_index_result",
                        "pub open spec fn slice_index_result",
                        1,
                    ),
                    inputs[3],
                    inputs[4],
                ),
                (
                    inputs[0],
                    inputs[1],
                    inputs[2],
                    inputs[3].replace(
                        trio.INDEX_FORMS[0].anchor,
                        "unsafe impl omitted",
                        1,
                    ),
                    inputs[4],
                ),
            )
            for index, mutation in enumerate(mutations):
                with self.subTest(target=config.target, mutation=index):
                    with self.assertRaises(GuardError):
                        trio.validate_source_anchors(config, *mutation)

    def test_literal_theorems_have_shared_input_and_boundary(self) -> None:
        expected_boundary = {
            selector for selector, _, _ in trio.BOUNDARY_FIELDS
        }
        for config in trio.TARGETS:
            for purpose in trio.PURPOSES:
                text, metadata = trio.obligation(config, purpose)
                with self.subTest(target=config.target, purpose=purpose):
                    validate_obligation(text, metadata)
                    trio.validate_target_obligation(config, text, metadata)
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
                    self.assertNotIn("(declare-fun", text)
                    self.assertNotIn("b_return", text)
                    self.assertNotIn("b_selected", text)
                    self.assertNotIn("b_final", text)
                    self.assertNotIn("b_trace", text)

    def test_mutable_specs_do_not_inject_the_canonical_reference(self) -> None:
        for config in (trio.TARGETS[0], trio.TARGETS[2]):
            text, metadata = trio.obligation(config, trio.PRIMARY)
            target = text[
                text.index("(define-fun TargetDefinition_T"):
                text.index("(define-fun Spec_T")
            ]
            self.assertNotIn("CanonicalSliceIndexResult", target)
            output_call = (
                f"({trio._output_transition_name(config)} x b y)"
            )
            mutated = text.replace(
                output_call,
                f"(and {output_call} (CanonicalSliceIndexResult x b y))",
                1,
            )
            with self.assertRaises(GuardError):
                trio.validate_target_obligation(config, mutated, metadata)

    def test_output_bearing_boundary_and_incomplete_coverage_are_rejected(
        self,
    ) -> None:
        config = trio.TARGETS[1]
        text, metadata = trio.obligation(config, trio.PRIMARY)
        changed = copy.deepcopy(metadata)
        changed["boundary_fields"][0]["role"] = "selected_output"
        with self.assertRaises(GuardError):
            validate_obligation(text, changed)
        changed = copy.deepcopy(metadata)
        changed["sealed_sliceindex_coverage"].pop()
        with self.assertRaises(GuardError):
            trio.validate_target_obligation(config, text, changed)

    def test_real_solver_results_are_decisive(self) -> None:
        for config in trio.TARGETS:
            for purpose in trio.PURPOSES:
                process = run_z3(trio.obligation_text(config, purpose))
                with self.subTest(target=config.target, purpose=purpose):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stderr, "")
                    self.assertEqual(
                        process.stdout,
                        config.expected_results[purpose] + "\n",
                    )

    def test_every_source_form_and_negative_probe_replays(self) -> None:
        for config in trio.TARGETS:
            for name in trio.source_cases(config):
                process = run_z3(trio.source_instance_text(config, name))
                with self.subTest(target=config.target, source=name):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertTrue(process.stdout.startswith("sat\n"))
                    self.assertIn("(NormalizedStart x)", process.stdout)
                    self.assertIn("(y_address y1)", process.stdout)
            for name in trio.negative_probe_names(config):
                process = run_z3(trio.negative_probe_text(config, name))
                with self.subTest(target=config.target, negative=name):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, "unsat\n")
                    self.assertEqual(process.stderr, "")

    def test_concrete_mutable_witnesses_replay_independently(self) -> None:
        for config in (trio.TARGETS[0], trio.TARGETS[2]):
            payload = trio.witness_payload(config)
            observed = replay.replay_witness(config, payload)
            self.assertEqual(observed, payload["expected"])
            self.assertTrue(
                observed["execution2_satisfies_active_contract"]
            )
            self.assertFalse(observed["source_result_is_execution2"])
            self.assertFalse(observed["exact_output_equal"])
            self.assertTrue(observed["exact_final_state_equal"])
            process = run_z3(trio.fixed_witness_text(config))
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertTrue(process.stdout.startswith("sat\n"))

    def test_verus_models_are_trusted_free_and_cover_the_claims(self) -> None:
        for config in trio.TARGETS:
            text = (ROOT / config.proof_filename).read_text()
            self.assertNotIn("external_body", text)
            self.assertEqual(text.count("pub proof fn"), 2)
        shared = (ROOT / trio.TARGETS[1].proof_filename).read_text()
        for name in (
            "Usize",
            "OpsIndexRange",
            "OpsBoundPair",
            "ClampUsize",
            "ClampOpsRangeFull",
            "Last",
        ):
            self.assertIn(name, shared)
        for config in (trio.TARGETS[0], trio.TARGETS[2]):
            text = (ROOT / config.proof_filename).read_text()
            self.assertIn(
                "active_contract_admits_distinct_usize_references", text
            )


class SliceIndexTrioScopeTests(unittest.TestCase):
    def test_baseline_and_delivered_ledger_scope_are_exact(self) -> None:
        self.assertEqual(len(runner.BASELINE_RESULTS), 51)
        self.assertEqual(len(runner.PRESERVED_ARTIFACT_IDS), 51)
        self.assertEqual(set(runner.CLUSTER_RESULTS), set(trio.TARGET_KEYS))
        rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        classified = sum(
            any(
                row[field] != "not-run"
                for field in target_pipeline.RESULT_FIELDS
            )
            for row in rows
        )
        self.assertEqual(classified, 62)
        self.assertEqual(len(rows) - classified, 0)

    def test_out_of_scope_ledger_edit_fails_closed(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = copy.deepcopy(csv_rows)
        other = next(
            row
            for row in csv_rows
            if (row["target"], row["input_order"])
            not in set(runner.BASELINE_RESULTS) | set(trio.TARGET_KEYS)
        )
        other["exact_output_determinism_status"] = "conditional-complete"
        matching = next(
            row
            for row in json_rows
            if (row["target"], row["input_order"])
            == (other["target"], other["input_order"])
        )
        matching["exact_output_determinism_status"] = "conditional-complete"
        with self.assertRaises(ValueError):
            runner.prepare_crosswalk_reset(csv_rows, json_rows)

    def test_retained_evidence_passes_the_dedicated_validator(self) -> None:
        errors: list[str] = []
        trio_validation.validate(errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
