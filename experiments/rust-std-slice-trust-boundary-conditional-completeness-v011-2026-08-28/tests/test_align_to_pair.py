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

import align_to_pair as align
import align_to_pair_validation
import campaign_common as common
from checker_guards import GuardError
import run_align_to_pair as runner
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


def source_inputs(
    config: align.AlignTarget,
) -> tuple[str, str, str, str, str]:
    row = next(
        row
        for row in common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        if (row["target"], row["input_order"])
        == (config.target, config.input_order)
    )
    vocabulary_lines = Path(
        row["shared_vocabulary_path"]
    ).read_text().splitlines(keepends=True)
    vocabulary = "\n".join(
        "".join(vocabulary_lines[start - 1 : end])
        for start, end in align.VOCABULARY_RANGES
    )
    pointer_source_lines = (
        common.RUST_LIBRARY / align.PTR_SOURCE_PATH
    ).read_text().splitlines(keepends=True)
    pointer_docs_lines = (
        common.RUST_LIBRARY / align.PTR_DOCS_PATH
    ).read_text().splitlines(keepends=True)
    pointer_source = "".join(
        pointer_source_lines[
            align.PTR_SOURCE_RANGE[0] - 1 : align.PTR_SOURCE_RANGE[1]
        ]
    )
    pointer_docs = "".join(
        pointer_docs_lines[
            align.PTR_DOCS_RANGE[0] - 1 : align.PTR_DOCS_RANGE[1]
        ]
    )
    return (
        row["source_item_text"],
        row["public_docs_text"],
        vocabulary,
        pointer_source,
        pointer_docs,
    )


class AlignToPairTests(unittest.TestCase):
    def test_literal_contracts_and_all_twenty_trust_records_match(self) -> None:
        rows = {
            (row["target"], row["input_order"]): row
            for row in common.read_csv(
                ROOT / "crosswalk/target_to_proof_boundary.csv"
            )
        }
        trust = common.read_csv(ROOT / "crosswalk/trust_site_inventory.csv")
        total = 0
        for config in align.TARGETS:
            row = rows[(config.target, config.input_order)]
            records = {
                record["record_id"]: record
                for record in trust
                if (record["target"], record["input_order"])
                == (config.target, config.input_order)
            }
            total += len(records)
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
                self.assertEqual(
                    row["public_docs_sha256"],
                    config.public_docs_sha256,
                )
                self.assertEqual(set(records), set(config.all_trust_site_ids))
                self.assertEqual(
                    {
                        record_id: align.canonical_json_sha256(record)
                        for record_id, record in records.items()
                    },
                    config.trust_hashes,
                )
                self.assertEqual(
                    set(config.excluded_trust_site_ids),
                    set(row["inadmissible_trust_site_ids"].split(";")),
                )
        self.assertEqual(total, 20)

    def test_slice_pointer_and_align_offset_sources_fail_closed(self) -> None:
        for config in align.TARGETS:
            inputs = source_inputs(config)
            align.validate_source_anchors(config, *inputs)
            mutations = (
                (
                    inputs[0].replace(
                        "crate::ptr::align_offset(ptr, align_of::<U>())",
                        "opaque_offset(ptr)",
                        1,
                    ),
                    *inputs[1:],
                ),
                (
                    inputs[0],
                    inputs[1].replace("zero-sized", "sized", 1),
                    *inputs[2:],
                ),
                (
                    inputs[0],
                    inputs[1],
                    inputs[2].replace(
                        "slice_aligned_middle",
                        "slice_answer_oracle",
                    ),
                    *inputs[3:],
                ),
                (
                    *inputs[:3],
                    inputs[3].replace("Cannot be aligned at all", "opaque", 1),
                    inputs[4],
                ),
                (
                    *inputs[:4],
                    inputs[4].replace("number of `T` elements", "bytes", 1),
                ),
            )
            for index, mutation in enumerate(mutations):
                with self.subTest(target=config.target, mutation=index):
                    with self.assertRaises(GuardError):
                        align.validate_source_anchors(config, *mutation)

    def test_shared_boundary_is_genuine_and_every_field_is_exact(self) -> None:
        expected_boundary = {
            selector for selector, _, _ in align.BOUNDARY_FIELDS
        }
        for config in align.TARGETS:
            for purpose in align.PURPOSES:
                text, metadata = align.obligation(config, purpose)
                align.validate_target_obligation(config, text, metadata)
                with self.subTest(target=config.target, purpose=purpose):
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
                        expected_boundary,
                    )
                    self.assertTrue(
                        metadata["boundary_scope"]["narrower_than_target"]
                    )
                    for forbidden in (
                        "b_result",
                        "b_return",
                        "b_final",
                        "b_trace",
                        "b_alignment_offset",
                        "b_branch",
                        "b_middle_values",
                    ):
                        self.assertNotIn(forbidden, text)
                    for selector, _ in align.OUTPUT_FIELDS:
                        self.assertIn(
                            f"(= ({selector} y1) ({selector} y2))",
                            text,
                        )
                    if purpose == align.PRIMARY:
                        for selector, _ in align.STATE_FIELDS:
                            self.assertIn(
                                f"(= ({selector} s1) ({selector} s2))",
                                text,
                            )
                    replaced = {
                        site
                        for replacement in metadata[
                            "source_backed_replacements"
                        ]
                        for site in replacement["replaces_trust_site_ids"]
                    }
                    self.assertEqual(
                        replaced, set(config.excluded_trust_site_ids)
                    )

    def test_answer_laundering_and_wrong_boundary_fields_fail_closed(self) -> None:
        config = align.TARGETS[0]
        text, metadata = align.obligation(config, align.PRIMARY)
        mutations = (
            text.replace(
                "(b_outside_frame (Seq Int))",
                "(b_middle_values (Seq Int))",
                1,
            ),
            text.replace(
                "(MiddleValues x b)",
                "(seq.unit (b_usize_max b))",
                1,
            ),
            text.replace(
                "(BranchKind x)",
                "(b_root_borrow b)",
                1,
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(mutation=index):
                with self.assertRaises(GuardError):
                    align.validate_target_obligation(
                        config, mutation, copy.deepcopy(metadata)
                    )
        required = {
            "answer_laundered_branch",
            "answer_laundered_middle",
            "wrong_middle_decode",
            "wrong_pointer_cast",
            "wrong_final_frame",
        }
        for config in align.TARGETS:
            self.assertTrue(required <= set(align.negative_probe_names(config)))

    def test_direct_theorem_results_are_clean(self) -> None:
        for config in align.TARGETS:
            for purpose in align.PURPOSES:
                process = run_z3(align.obligation_text(config, purpose))
                with self.subTest(target=config.target, purpose=purpose):
                    self.assertEqual(process.returncode, 0)
                    self.assertEqual(process.stderr, "")
                    self.assertEqual(
                        process.stdout,
                        config.expected_solver_results[purpose] + "\n",
                    )

    def test_required_source_cases_are_sat_and_cover_all_edges(self) -> None:
        required = {
            "empty",
            "zst_source",
            "zst_destination",
            "already_aligned_byte_reinterpretation",
            "misaligned_finite_offset",
            "offset_equals_length",
            "offset_greater_than_length",
            "offset_usize_max",
            "nontrivial_size_gcd",
            "allocation_provenance",
        }
        for config in align.TARGETS:
            cases = align.source_cases(config)
            self.assertEqual(set(cases), required)
            self.assertEqual(
                align.evaluate_source(cases["offset_equals_length"])[
                    "branch"
                ],
                align.BRANCH_ALIGNED,
            )
            self.assertEqual(
                align.evaluate_source(cases["offset_greater_than_length"])[
                    "branch"
                ],
                align.BRANCH_OFFSET_FALLBACK,
            )
            self.assertEqual(
                align.evaluate_source(cases["offset_usize_max"])["offset"],
                cases["offset_usize_max"].usize_max,
            )
            gcd_result = align.evaluate_source(
                cases["nontrivial_size_gcd"]
            )
            self.assertEqual(gcd_result["middle_length"], 2)
            self.assertEqual(gcd_result["suffix_length"], 2)
            for name in cases:
                process = run_z3(align.source_instance_text(config, name))
                with self.subTest(target=config.target, case=name):
                    self.assertEqual(process.returncode, 0)
                    self.assertEqual(process.stderr, "")
                    self.assertTrue(process.stdout.startswith("sat\n"))
                    self.assertIn("(y_middle_values y1)", process.stdout)
                    self.assertIn("(s_final_source s1)", process.stdout)

    def test_invalid_inputs_and_every_wrong_transition_are_unsat(self) -> None:
        for config in align.TARGETS:
            for name in align.negative_probe_names(config):
                process = run_z3(align.negative_probe_text(config, name))
                with self.subTest(target=config.target, probe=name):
                    self.assertEqual(process.returncode, 0)
                    self.assertEqual(process.stderr, "")
                    self.assertEqual(process.stdout, "unsat\n")

    def test_mutable_witness_replays_same_input_and_boundary(self) -> None:
        config = next(config for config in align.TARGETS if config.mutable)
        payload = align.witness_payload(config)
        self.assertTrue(payload["shared_boundary"]["same_for_both_executions"])
        self.assertNotEqual(
            payload["execution1"]["final_bytes"],
            payload["execution2"]["final_bytes"],
        )
        self.assertTrue(
            payload["expected"][
                "both_executions_satisfy_every_active_conjunct"
            ]
        )
        process = run_z3(align.fixed_full_state_witness_text(config))
        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stderr, "")
        self.assertTrue(process.stdout.startswith("sat\n"))
        self.assertIn("(s_final_bytes s1)", process.stdout)
        self.assertIn("(s_final_bytes s2)", process.stdout)
        self.assertIn("false", process.stdout)

    def test_trusted_free_verus_models_typecheck_and_verify(self) -> None:
        self.assertTrue(common.VERUS.is_file())
        with tempfile.TemporaryDirectory() as directory:
            for config in align.TARGETS:
                text = align.verus_text(config)
                self.assertNotIn("external_body", text)
                self.assertNotIn("assume(", text)
                self.assertNotIn("admit(", text)
                path = Path(directory) / f"{config.artifact_id}.rs"
                path.write_text(text)
                typecheck = subprocess.run(
                    [
                        str(common.VERUS),
                        str(path),
                        "--crate-type=lib",
                        "--no-verify",
                    ],
                    text=True,
                    capture_output=True,
                    timeout=60,
                    check=False,
                )
                verification = subprocess.run(
                    [str(common.VERUS), str(path), "--crate-type=lib"],
                    text=True,
                    capture_output=True,
                    timeout=60,
                    check=False,
                )
                with self.subTest(target=config.target):
                    self.assertEqual(typecheck.returncode, 0, typecheck.stderr)
                    self.assertEqual(typecheck.stderr, "")
                    self.assertEqual(
                        verification.returncode, 0, verification.stderr
                    )
                    self.assertEqual(verification.stderr, "")
                    self.assertIn(
                        align.VERUS_EXPECTED_SUMMARY,
                        verification.stdout,
                    )

    def test_runner_reset_changes_only_rows_008_and_009(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        reset_csv, reset_json = runner.prepare_crosswalk_reset(
            csv_rows, json_rows
        )
        self.assertEqual(reset_csv, reset_json)
        for before, after in zip(csv_rows, reset_csv):
            changed = {
                field
                for field in before
                if before[field] != after[field]
            }
            key = (before["target"], before["input_order"])
            if key in set(align.TARGET_KEYS):
                self.assertTrue(changed <= set(target_pipeline.RESULT_FIELDS))
            else:
                self.assertFalse(changed)

    def test_final_ledger_and_dedicated_validator(self) -> None:
        evidence = all(
            (
                ROOT
                / "evidence/targets"
                / config.artifact_id
                / "result.json"
            ).is_file()
            for config in align.TARGETS
        )
        if not evidence:
            self.skipTest("align-to evidence has not been generated yet")
        errors: list[str] = []
        align_to_pair_validation.validate(errors)
        self.assertEqual(errors, [])
        rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        self.assertEqual(
            sum(
                any(
                    row[field] != "not-run"
                    for field in target_pipeline.RESULT_FIELDS
                )
                for row in rows
            ),
            62,
        )
        self.assertEqual(
            sum(
                all(
                    row[field] == "not-run"
                    for field in target_pipeline.RESULT_FIELDS
                )
                for row in rows
            ),
            0,
        )


if __name__ == "__main__":
    unittest.main()
