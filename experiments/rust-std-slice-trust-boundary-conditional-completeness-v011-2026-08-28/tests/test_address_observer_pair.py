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

import address_observer_pair as pair
import campaign_common as common
from checker_guards import GuardError, validate_obligation
import run_address_observer_pair as runner
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


def authority_row(config: pair.AddressObserverTarget) -> dict[str, str]:
    return next(
        row
        for row in common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        if (row["target"], row["input_order"])
        == (config.target, config.input_order)
    )


class AddressObserverPairTests(unittest.TestCase):
    def test_active_contracts_manifests_and_all_trust_sites_are_exact(
        self,
    ) -> None:
        trust = common.read_csv(ROOT / "crosswalk/trust_site_inventory.csv")
        total = 0
        for config in pair.TARGETS:
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
                self.assertEqual(
                    row["harness_sha256"],
                    config.harness_sha256,
                )
                self.assertEqual(
                    row["source_body_manifest_sha256"],
                    config.source_body_manifest_sha256,
                )
                self.assertEqual(
                    row["transformation_manifest_sha256"],
                    config.transformation_manifest_sha256,
                )
                self.assertEqual(
                    row["dependency_manifest_sha256"],
                    config.dependency_manifest_sha256,
                )
                self.assertEqual(set(records), set(config.all_trust_site_ids))
                self.assertEqual(
                    {
                        record_id: pair.canonical_json_sha256(record)
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
        self.assertEqual(total, 27)

    def test_source_docs_and_opaque_vocabulary_fail_closed(self) -> None:
        for config in pair.TARGETS:
            row = authority_row(config)
            vocabulary_lines = Path(
                row["shared_vocabulary_path"]
            ).read_text().splitlines(keepends=True)
            vocabulary = "\n".join(
                "".join(vocabulary_lines[start - 1 : end])
                for start, end in pair.VOCABULARY_RANGES
            )
            inputs = (
                row["source_item_text"],
                row["public_docs_text"],
                vocabulary,
            )
            pair.validate_source_anchors(config, *inputs)
            mutations = (
                (
                    inputs[0].replace(
                        config.source_fragments[-1],
                        "synthetic source result",
                        1,
                    ),
                    inputs[1],
                    inputs[2],
                ),
                (
                    inputs[0],
                    inputs[1].replace(
                        config.docs_fragments[-1],
                        "No panic.",
                        1,
                    ),
                    inputs[2],
                ),
                (
                    inputs[0],
                    inputs[1],
                    inputs[2].replace("pub uninterp spec fn", "pub spec fn"),
                ),
            )
            for index, mutation in enumerate(mutations):
                with self.subTest(target=config.target, mutation=index):
                    with self.assertRaises(GuardError):
                        pair.validate_source_anchors(config, *mutation)

    def test_literal_theorems_use_only_shared_genuine_boundary_data(
        self,
    ) -> None:
        expected_boundary = {
            selector for selector, _, _ in pair.BOUNDARY_FIELDS
        }
        for config in pair.TARGETS:
            for purpose in pair.PURPOSES:
                text, metadata = pair.obligation(config, purpose)
                with self.subTest(target=config.target, purpose=purpose):
                    validate_obligation(text, metadata)
                    pair.validate_target_obligation(config, text, metadata)
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
                    self.assertNotIn("(declare-fun", text)
                    for token in (
                        "b_computed",
                        "b_offset",
                        "b_range",
                        "b_branch",
                        "b_output",
                        "b_result",
                        "b_final",
                        "b_trace",
                    ):
                        self.assertNotIn(token, text)
                    requires = text[
                        text.index("(define-fun Requires_T"):
                        text.index("(define-fun Boundary_T")
                    ]
                    self.assertNotIn("b_element_size", requires)
                    self.assertNotIn("b_receiver_alive", requires)

    def test_exact_equivalence_covers_every_projected_field(self) -> None:
        for config in pair.TARGETS:
            exact_text, exact_metadata = pair.obligation(
                config, pair.EXACT_OUTPUT
            )
            full_text, full_metadata = pair.obligation(config, pair.PRIMARY)
            self.assertEqual(
                [item["selector"] for item in exact_metadata[
                    "principal_observations"
                ]],
                ["y_return"],
            )
            self.assertEqual(
                [item["selector"] for item in full_metadata[
                    "principal_observations"
                ]],
                ["y_return", "s_final_memory_token"],
            )
            self.assertIn(
                "(= (y_return y1) (y_return y2))",
                exact_text,
            )
            self.assertIn(
                "(= (y_return y1) (y_return y2))",
                full_text,
            )
            self.assertIn(
                "(= (s_final_memory_token s1) (s_final_memory_token s2))",
                full_text,
            )

    def test_both_real_theorem_obligations_are_unsat(self) -> None:
        for config in pair.TARGETS:
            for purpose in pair.PURPOSES:
                process = run_z3(pair.obligation_text(config, purpose))
                with self.subTest(target=config.target, purpose=purpose):
                    self.assertEqual(process.returncode, 0)
                    self.assertEqual(process.stderr, "")
                    self.assertEqual(process.stdout, "unsat\n")

    def test_source_cases_cover_required_address_and_panic_edges(self) -> None:
        expected = {
            "39": {
                "same_allocation_start": ("some", 0, None),
                "same_allocation_interior": ("some", 2, None),
                "distinct_allocation": ("none", None, None),
                "element_stride_misalignment": ("none", None, None),
                "pointer_before_receiver_wrapping": ("none", None, None),
                "exact_end": ("none", None, None),
                "out_of_bounds_after_end": ("none", None, None),
                "usize_wrapping_limit": ("none", None, None),
                "zst_panic": ("panic", None, None),
            },
            "111": {
                "same_allocation_full": ("some", 0, 4),
                "same_allocation_interior": ("some", 1, 3),
                "same_allocation_empty_start": ("some", 0, 0),
                "same_allocation_empty_end": ("some", 4, 4),
                "distinct_allocation_nonempty": ("none", None, None),
                "element_stride_misalignment": ("none", None, None),
                "pointer_before_receiver_wrapping": ("none", None, None),
                "exact_end_nonempty": ("none", None, None),
                "out_of_bounds_after_end": ("none", None, None),
                "separate_empty_false_positive_start": ("some", 0, 0),
                "separate_empty_false_positive_end": ("some", 4, 4),
                "usize_limit_valid_no_wrap": ("some", 68, 100),
                "zst_panic": ("panic", None, None),
            },
        }
        for config in pair.TARGETS:
            cases = pair.source_cases(config)
            self.assertEqual(set(cases), set(expected[config.input_order]))
            for name, case in cases.items():
                outcome = pair.evaluate_source(config, case)
                observed = (
                    outcome["kind"],
                    outcome["start"],
                    outcome["end"],
                )
                with self.subTest(target=config.target, case=name):
                    self.assertEqual(
                        observed,
                        expected[config.input_order][name],
                    )
                    process = run_z3(
                        pair.source_instance_text(config, name)
                    )
                    self.assertEqual(process.returncode, 0)
                    self.assertEqual(process.stderr, "")
                    self.assertTrue(process.stdout.startswith("sat\n"))
                    self.assertIn("(y_return y1)", process.stdout)

    def test_every_invalid_or_wrong_transition_probe_is_unsat(self) -> None:
        for config in pair.TARGETS:
            names = pair.negative_probe_names(config)
            self.assertEqual(len(names), 22 if config.kind == "element" else 24)
            for name in names:
                process = run_z3(pair.negative_probe_text(config, name))
                with self.subTest(target=config.target, probe=name):
                    self.assertEqual(process.returncode, 0)
                    self.assertEqual(process.stderr, "")
                    self.assertEqual(process.stdout, "unsat\n")

    def test_empty_subslice_false_positives_are_distinct_and_deterministic(
        self,
    ) -> None:
        config = pair.TARGETS[1]
        assessment = pair.false_positive_assessment(config)
        self.assertEqual(len(assessment["witnesses"]), 2)
        self.assertTrue(
            all(
                item["allocations_distinct"]
                and item["subslice_length"] == 0
                and item["source_outcome"]["kind"] == "some"
                for item in assessment["witnesses"]
            )
        )
        self.assertEqual(assessment["exact_output_effect"], "none; both executions return the same range")

    def test_answer_injection_weakened_equality_and_preconditions_fail_closed(
        self,
    ) -> None:
        config = pair.TARGETS[0]
        text, metadata = pair.obligation(config, pair.PRIMARY)
        mutations = (
            text.replace(
                "(AddressObserverContractTransition x b y s)",
                "(and (AddressObserverContractTransition x b y s) "
                "(= (y_return y) ElementNone))",
                1,
            ),
            text.replace(
                "(= (y_return y1) (y_return y2))",
                "true",
                1,
            ),
            text.replace(
                "(>= (x_receiver_length x) 0)",
                "(and (>= (x_receiver_length x) 0) "
                "(> (x_receiver_length x) 0))",
                1,
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(mutation=index):
                with self.assertRaises(GuardError):
                    pair.validate_target_obligation(
                        config,
                        mutation,
                        metadata,
                    )
        changed = copy.deepcopy(metadata)
        changed["boundary_fields"][0]["role"] = "selected_output"
        with self.assertRaises(GuardError):
            validate_obligation(text, changed)

    def test_reset_and_result_update_touch_only_rows_039_and_111(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        reset_csv, reset_json = runner.prepare_crosswalk_reset(
            csv_rows,
            json_rows,
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
            if key in set(pair.TARGET_KEYS):
                self.assertLessEqual(
                    changed,
                    set(target_pipeline.RESULT_FIELDS),
                )
            else:
                self.assertFalse(changed)

    def test_trusted_free_verus_models_are_source_specific(self) -> None:
        for config in pair.TARGETS:
            text = pair.verus_text(config)
            self.assertNotIn("external_body", text)
            self.assertIn("source_output", text)
            self.assertIn("% modulus", text)
            self.assertIn("exact_output_conditional_complete", text)
            self.assertIn("full_state_conditional_complete", text)


if __name__ == "__main__":
    unittest.main()
