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
import raw_slice_pair as raw
import run_raw_slice_pair as runner
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


def source_inputs(
    config: raw.RawSliceTarget,
) -> tuple[str, str, str]:
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
        for start, end in raw.VOCABULARY_RANGES
    )
    return row["source_item_text"], row["public_docs_text"], vocabulary


class RawSlicePairTests(unittest.TestCase):
    def test_active_contracts_and_all_six_trust_records_match_authority(
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
        for config in raw.TARGETS:
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
                        record_id: raw.canonical_json_sha256(record)
                        for record_id, record in records.items()
                    },
                    config.trust_hashes,
                )
                self.assertEqual(
                    records[config.context_only_trust_site_ids[0]][
                        "semantic_disposition"
                    ],
                    "context-only-specification-vocabulary",
                )
                self.assertTrue(
                    all(
                        records[site]["semantic_disposition"].startswith(
                            "inadmissible"
                        )
                        for site in config.excluded_trust_site_ids
                    )
                )
        self.assertEqual(total, 6)

    def test_source_docs_and_raw_vocabulary_fail_closed(self) -> None:
        for config in raw.TARGETS:
            source, docs, vocabulary = source_inputs(config)
            raw.validate_source_anchors(config, source, docs, vocabulary)
            mutations = (
                (
                    source.replace(
                        config.source_fragments[-1],
                        "synthetic raw result",
                        1,
                    ),
                    docs,
                    vocabulary,
                ),
                (
                    source,
                    docs.replace(config.docs_fragments[0], "multiple allocations"),
                    vocabulary,
                ),
                (
                    source,
                    docs,
                    vocabulary.replace(
                        "pub ghost struct SliceRawDomain",
                        "pub ghost struct AnswerDomain",
                    ),
                ),
                (
                    source + "\nexternal_body\n",
                    docs,
                    vocabulary,
                ),
            )
            for index, mutation in enumerate(mutations):
                with self.subTest(target=config.target, mutation=index):
                    with self.assertRaises(GuardError):
                        raw.validate_source_anchors(config, *mutation)

    def test_literal_shared_x_shared_boundary_and_allowed_fields(self) -> None:
        expected = {selector for selector, _, _ in raw.BOUNDARY_FIELDS}
        for config in raw.TARGETS:
            for purpose in raw.PURPOSES:
                text, metadata = raw.obligation(config, purpose)
                with self.subTest(target=config.target, purpose=purpose):
                    validate_obligation(text, metadata)
                    raw.validate_target_obligation(config, text, metadata)
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
                    self.assertNotIn("b_return", text)
                    self.assertNotIn("b_final", text)
                    self.assertNotIn("b_output", text)
                    self.assertNotIn("b_trace", text)
                    self.assertNotIn("b_length", text)
                    self.assertNotIn("x_memory", text)
                    self.assertNotIn("x_initialized", text)
                    self.assertIn(
                        "(ReferenceDereferenceTransition x b y)",
                        text,
                    )

    def test_every_principal_field_has_exact_equality(self) -> None:
        for config in raw.TARGETS:
            for purpose in raw.PURPOSES:
                text, metadata = raw.obligation(config, purpose)
                expected = {
                    selector for selector, _ in raw.OUTPUT_FIELDS
                }
                if purpose == raw.PRIMARY:
                    expected |= {
                        selector for selector, _ in raw.STATE_FIELDS
                    }
                self.assertEqual(
                    {
                        item["selector"]
                        for item in metadata["principal_observations"]
                    },
                    expected,
                )
                for selector, _ in raw.OUTPUT_FIELDS:
                    self.assertIn(
                        f"(= ({selector} y1) ({selector} y2))",
                        text,
                    )
                if purpose == raw.PRIMARY:
                    for selector, _ in raw.STATE_FIELDS:
                        self.assertIn(
                            f"(= ({selector} s1) ({selector} s2))",
                            text,
                        )

    def test_obligations_have_the_expected_real_solver_results(self) -> None:
        for config in raw.TARGETS:
            for purpose in raw.PURPOSES:
                text, _ = raw.obligation(config, purpose)
                process = run_z3(text)
                with self.subTest(target=config.target, purpose=purpose):
                    self.assertEqual(process.returncode, 0)
                    self.assertEqual(process.stderr, "")
                    self.assertEqual(
                        process.stdout,
                        config.expected_results[purpose] + "\n",
                    )

    def test_all_allocated_empty_zst_and_one_past_cases_are_live(self) -> None:
        required = {
            "allocated_nonempty",
            "allocated_empty",
            "dangling_empty",
            "allocated_nonempty_zst",
            "dangling_nonempty_zst",
            "permitted_one_past_endpoint",
            "allocated_empty_at_one_past",
        }
        for config in raw.TARGETS:
            cases = raw.source_cases(config)
            self.assertEqual(set(cases), required)
            for name in cases:
                process = run_z3(raw.source_instance_text(config, name))
                with self.subTest(target=config.target, case=name):
                    self.assertEqual(process.returncode, 0)
                    self.assertEqual(process.stderr, "")
                    self.assertTrue(process.stdout.startswith("sat\n"))
                    self.assertIn("(y_return_address y1)", process.stdout)
                    self.assertIn("(s_final_memory s1)", process.stdout)

    def test_invalid_domains_and_wrong_results_are_unsat(self) -> None:
        for config in raw.TARGETS:
            for name in raw.NEGATIVE_PROBES:
                process = run_z3(raw.negative_probe_text(config, name))
                with self.subTest(target=config.target, probe=name):
                    self.assertEqual(process.returncode, 0)
                    self.assertEqual(process.stderr, "")
                    self.assertEqual(process.stdout, "unsat\n")

    def test_addressed_view_and_zst_one_past_rules_are_independently_unsat(
        self,
    ) -> None:
        regressions = {
            "wrong_first_addressed_element",
            "wrong_interior_addressed_element",
            "nonempty_starts_at_one_past",
            "uninitialized_element",
            "nonzero_without_allocation",
            "nonzero_without_provenance",
            "zst_nonzero_stride",
            "empty_one_past_dereference",
        }
        self.assertTrue(regressions <= set(raw.NEGATIVE_PROBES))
        for config in raw.TARGETS:
            text, _ = raw.obligation(config, raw.EXACT_OUTPUT)
            self.assertIn(
                "(select (b_memory b) (ElementAddress x i))",
                text,
            )
            self.assertIn(
                "(+ (x_address x) (* i (x_element_size x)))",
                text,
            )
            self.assertNotIn(
                "(= (y_return_memory y) (x_memory x))",
                text,
            )
            self.assertEqual(
                raw.base_case(config)["memory"],
                {4096: 10, 4100: 20, 4104: 30},
            )
            for name in sorted(regressions):
                with self.subTest(target=config.target, regression=name):
                    process = run_z3(raw.negative_probe_text(config, name))
                    self.assertEqual(process.returncode, 0)
                    self.assertEqual(process.stderr, "")
                    self.assertEqual(process.stdout, "unsat\n")

    def test_state_frame_probe_distinguishes_immutable_memory_from_mutable_aliases(
        self,
    ) -> None:
        immutable = next(config for config in raw.TARGETS if not config.mutable)
        mutable = next(config for config in raw.TARGETS if config.mutable)
        immutable_probe = raw.negative_probe_text(
            immutable, "state_frame_semantics"
        )
        mutable_probe = raw.negative_probe_text(
            mutable, "state_frame_semantics"
        )
        self.assertIn("(= (s_final_memory s1)", immutable_probe)
        self.assertNotIn(
            "(= (s_final_memory s1)", mutable_probe.rsplit("(assert", 1)[1]
        )
        self.assertIn("(= (s_final_alias_writers s1) 1)", mutable_probe)
        self.assertEqual(run_z3(immutable_probe).stdout, "unsat\n")
        self.assertEqual(run_z3(mutable_probe).stdout, "unsat\n")

    def test_mutable_fixed_witness_satisfies_both_specs(self) -> None:
        config = next(config for config in raw.TARGETS if config.mutable)
        process = run_z3(raw.fixed_witness_text(config))
        payload = raw.witness_payload(config)
        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stderr, "")
        self.assertTrue(process.stdout.startswith("sat\n"))
        self.assertIn("(Equivalent_T x b y1 s1 y2 s2) false", process.stdout)
        self.assertTrue(
            payload["expected"][
                "both_executions_satisfy_every_active_conjunct"
            ]
        )
        self.assertTrue(payload["expected"]["exact_output_equal"])
        self.assertFalse(payload["expected"]["full_state_equal"])
        self.assertEqual(
            config.expected_classification[
                "completeness_modulo_reviewed_equivalence_status"
            ],
            "conditional-incomplete",
        )

    def test_no_mutable_final_frame_is_invented(self) -> None:
        config = next(config for config in raw.TARGETS if config.mutable)
        text, metadata = raw.obligation(config, raw.PRIMARY)
        self.assertNotIn(
            "(= (s_final_memory s) (FiniteReturnedView x b 0))",
            text[text.index("(define-fun MutableExclusiveIdentityFrame") :],
        )
        self.assertIn(
            "states no final returned-memory clause",
            metadata["domain"]["mutable_final_state"],
        )
        self.assertNotIn("final(ret)", config.active_contract_text)

    def test_helper_boundary_equality_and_theorem_mutations_fail_closed(
        self,
    ) -> None:
        mutations = (
            ("(UbCheckTransition x b)", "true"),
            ("(RawFatPointerConstruction x y)", "true"),
            ("(ReferenceDereferenceTransition x b y)", "true"),
            ("(ActiveReturnLengthConjunct x y)", "true"),
            ("(ActiveSliceStartPointerConjunct x y)", "true"),
            (
                "(= (b_input_address b) (x_address x))",
                "(= (b_input_address b) 1)",
            ),
            ("(Spec_T x b y2 s2)", "(Spec_T x b y1 s2)"),
            (
                "(= (y_return_address y1) (y_return_address y2))",
                "true",
            ),
        )
        for config in raw.TARGETS:
            text, metadata = raw.obligation(config, raw.PRIMARY)
            for old, new in mutations:
                changed = text.replace(old, new, 1)
                self.assertNotEqual(changed, text)
                with self.subTest(target=config.target, mutation=old):
                    with self.assertRaises(GuardError):
                        raw.validate_target_obligation(
                            config,
                            changed,
                            metadata,
                        )

    def test_answer_laundering_and_trust_relabeling_fail_closed(self) -> None:
        for config in raw.TARGETS:
            text, metadata = raw.obligation(config, raw.PRIMARY)
            changed = copy.deepcopy(metadata)
            changed["boundary_fields"][0]["role"] = "selected_output"
            with self.assertRaises(GuardError):
                validate_obligation(text, changed)

            changed = copy.deepcopy(metadata)
            changed["boundary_scope"]["admitted_trust_site_ids"] = [
                config.excluded_trust_site_ids[0]
            ]
            changed["boundary_scope"]["excluded_retained_trust_site_ids"] = [
                config.excluded_trust_site_ids[1]
            ]
            with self.assertRaises(GuardError):
                validate_obligation(text, changed)

            changed = copy.deepcopy(metadata)
            changed["source_backed_replacements"][0][
                "replaces_trust_site_ids"
            ] = [config.excluded_trust_site_ids[0]]
            with self.assertRaises(GuardError):
                validate_obligation(text, changed)

    def test_verus_models_are_trusted_free_and_target_specific(self) -> None:
        for config in raw.TARGETS:
            text = raw.verus_text(config)
            with self.subTest(target=config.target):
                self.assertNotIn("external_body", text)
                self.assertNotIn("assume_specification", text)
                self.assertIn("pub open spec fn valid_input", text)
                self.assertIn("pub open spec fn source_output", text)
                self.assertIn("pub open spec fn returned_view", text)
                self.assertIn("pub memory: Map<int, int>", text)
                self.assertIn(
                    "boundary.memory[element_address(input, i)]",
                    text,
                )
                self.assertNotIn("input.memory", text)
                self.assertNotIn("input.initialized", text)
                self.assertIn(
                    f"conditional_complete_exact_output_{config.function_name}",
                    text,
                )
                if config.mutable:
                    self.assertIn(
                        "mutable_distinct_final_memory_witness",
                        text,
                    )
                    self.assertIn("first: Seq<int>", text)
                    self.assertIn(
                        "first.len() == input.length",
                        text,
                    )
                else:
                    self.assertIn(
                        "conditional_complete_from_raw_parts",
                        text,
                    )

    def test_exact_bounded_evidence_directory_set_rejects_foreign_name(
        self,
    ) -> None:
        expected = authority_validator.bounded_target_artifact_ids()
        self.assertEqual(len(expected), 62)
        self.assertEqual(
            {config.artifact_id for config in raw.TARGETS}
            & expected,
            {config.artifact_id for config in raw.TARGETS},
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for artifact_id in expected:
                (root / artifact_id).mkdir()
            errors: list[str] = []
            authority_validator.validate_bounded_target_evidence_directories(
                root,
                errors,
            )
            self.assertEqual(errors, [])

            (root / "foreign_target").mkdir()
            authority_validator.validate_bounded_target_evidence_directories(
                root,
                errors,
            )
            self.assertEqual(
                errors,
                ["target evidence exists outside the bounded target scope"],
            )

    def test_runner_reset_and_delivery_touch_only_rows_048_049(self) -> None:
        csv_rows, json_rows = runner._load_crosswalks()
        for rows in (csv_rows, json_rows):
            for row in rows:
                if row["input_order"] in {
                    "17",
                    "18",
                    "39",
                    "46",
                    "47",
                    "53",
                    "54",
                    "55",
                    "111",
                }:
                    row.update(
                        {
                            field: "not-run"
                            for field in target_pipeline.RESULT_FIELDS
                        }
                    )
        reset_csv, reset_json = runner.prepare_crosswalk_reset(
            csv_rows, json_rows
        )
        self.assertEqual(reset_csv, reset_json)
        changed = []
        for before, after in zip(csv_rows, reset_csv):
            fields = {
                field
                for field in set(before) | set(after)
                if before.get(field) != after.get(field)
            }
            if fields:
                changed.append((before["input_order"], fields))
        self.assertEqual(
            {order for order, _ in changed},
            {"48", "49"},
        )
        self.assertTrue(
            all(
                fields <= set(target_pipeline.RESULT_FIELDS)
                for _, fields in changed
            )
        )

    def test_retained_evidence_reports_56_classified_6_not_run(self) -> None:
        rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        classified = sum(
            any(row[field] != "not-run" for field in target_pipeline.RESULT_FIELDS)
            for row in rows
        )
        not_run = sum(
            all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
            for row in rows
        )
        self.assertEqual((classified, not_run), (62, 0))
        manifest = json.loads(
            (ROOT / "evidence/raw_slice_pair_cluster/manifest.json").read_text()
        )
        self.assertEqual(manifest["classified_rows"], 51)
        self.assertEqual(manifest["not_run_rows"], 11)
        self.assertEqual(
            len(manifest["preserved_certified_evidence"]),
            49,
        )
        self.assertEqual(
            manifest["preserved_frozen_inputs"]["root"]["file_count"],
            320,
        )


if __name__ == "__main__":
    unittest.main()
