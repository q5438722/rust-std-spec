#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
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
import pointer_cast_cluster
import pointer_target_pipeline
import replay_target_019
import replay_target_020
import replay_target_021
import run_pointer_cast_cluster
import target_019
import target_020
import target_021


TARGETS = (
    (target_019, replay_target_019),
    (target_021, replay_target_021),
    (target_020, replay_target_020),
)


def delivered_crosswalk_rows() -> tuple[list[dict], list[dict]]:
    csv_rows = common.read_csv(
        ROOT / "crosswalk/target_to_proof_boundary.csv"
    )
    json_rows = json.loads(
        (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
    )
    cluster_keys = set(run_pointer_cast_cluster.CLUSTER_KEYS)
    for rows in (csv_rows, json_rows):
        for row in rows:
            key = (row["target"], row["input_order"])
            if key in pointer_target_pipeline.BASELINE_RESULTS:
                row.update(pointer_target_pipeline.BASELINE_RESULTS[key])
            elif key in cluster_keys:
                row.update(pointer_target_pipeline.COMPLETE)
            else:
                row.update(run_pointer_cast_cluster.NOT_RUN)
    return csv_rows, json_rows


class PointerCastClusterTests(unittest.TestCase):
    def test_verus_models_reject_misaligned_regression_input(self) -> None:
        model_paths = (
            ROOT / "proofs/019_core_slice_as_mut_ptr.rs",
            ROOT / "proofs/021_core_slice_as_ptr.rs",
            ROOT / "proofs/020_core_slice_as_mut_ptr_range.rs",
        )
        for path in model_paths:
            text = path.read_text()
            with self.subTest(model=path.name):
                self.assertEqual(
                    text.count(
                        "&& input.address % input.element_alignment == 0"
                    ),
                    1,
                )
                self.assertIn(
                    "pub proof fn rejects_misaligned_regression_input("
                    "input: SliceInput)",
                    text,
                )
                self.assertIn("input.address == 1026,", text)
                self.assertIn("input.element_alignment == 4,", text)
                self.assertIn("!valid_input(input),", text)

    def test_contract_hashes_and_dependency_order_are_exact(self) -> None:
        self.assertEqual(
            target_019.ACTIVE_CONTRACT_SHA256,
            "840c4efc8976016ca0b1c8728d1cabb13529c6e83939e8ca3cbc31232ba6a14a",
        )
        self.assertEqual(
            target_021.ACTIVE_CONTRACT_SHA256,
            "52c2a91bc8c7e49cd77d4429bb2b2a6e50a788211f2abca511f4df650f1a5edc",
        )
        self.assertEqual(
            target_020.ACTIVE_CONTRACT_SHA256,
            "0d55922a668ea2e52e07ca14a1146f6ff2d0c9a9d68d9369ff4171f9a6d574c1",
        )
        self.assertEqual(
            target_020.CONFIG.source_dependency,
            (
                "TS-020-D002",
                target_019.TARGET,
                target_019.ARTIFACT_ID,
            ),
        )

    def test_reviewed_obligations_are_checker_valid(self) -> None:
        for module, _ in TARGETS:
            for purpose in module.PURPOSES:
                with self.subTest(target=module.TARGET, purpose=purpose):
                    text, metadata = module.obligation(purpose)
                    validate_obligation(text, metadata)
                    module.validate_target_obligation(text, metadata)

    def test_replaced_sites_are_not_admitted_as_boundaries(self) -> None:
        expected = {
            target_019.TARGET: {"TS-019-D001"},
            target_021.TARGET: {"TS-021-D001"},
            target_020.TARGET: {
                "TS-020-D003",
                "TS-020-D004",
                "TS-020-E001",
            },
        }
        for module, _ in TARGETS:
            with self.subTest(target=module.TARGET):
                manifest = module.boundary_manifest()
                self.assertEqual(manifest["schema_version"], 2)
                excluded = {
                    item["trust_site_id"]
                    for item in manifest["excluded_retained_sites"]
                }
                admitted = set(manifest["admitted_boundary_trust_site_ids"])
                self.assertEqual(excluded, expected[module.TARGET])
                self.assertTrue(excluded.isdisjoint(admitted))

    def test_boundary_backing_is_declared_and_excludes_replaced_sites(self) -> None:
        expected_replacements = {
            target_019.TARGET: {"SRC-019-CANONICAL-SLICE-TO-MUT-PTR"},
            target_021.TARGET: {"SRC-021-CANONICAL-SLICE-TO-CONST-PTR"},
            target_020.TARGET: set(),
        }
        expected_declared_replacements = {
            target_019.TARGET: {"SRC-019-CANONICAL-SLICE-TO-MUT-PTR"},
            target_021.TARGET: {"SRC-021-CANONICAL-SLICE-TO-CONST-PTR"},
            target_020.TARGET: {
                "SRC-020-CANONICAL-SLICE-TO-MUT-PTR",
                "SRC-020-CANONICAL-MUT-PTR-ADD",
            },
        }
        for module, _ in TARGETS:
            metadata = module.obligation(module.PRIMARY)[1]
            scope = metadata["boundary_scope"]
            admitted = set(scope["admitted_trust_site_ids"])
            excluded = set(scope["excluded_retained_trust_site_ids"])
            context_only = set(scope["context_only_trust_site_ids"])
            audited = set(scope["all_audited_trust_site_ids"])
            replacements = set(scope["source_backed_replacement_ids"])
            with self.subTest(target=module.TARGET):
                self.assertEqual(
                    replacements,
                    expected_replacements[module.TARGET],
                )
                self.assertEqual(
                    {
                        replacement["replacement_id"]
                        for replacement in metadata[
                            "source_backed_replacements"
                        ]
                    },
                    expected_declared_replacements[module.TARGET],
                )
                self.assertEqual(
                    {
                        trust_site_id
                        for replacement in metadata[
                            "source_backed_replacements"
                        ]
                        for trust_site_id in replacement[
                            "replaces_trust_site_ids"
                        ]
                    },
                    excluded,
                )
                self.assertEqual(admitted | excluded | context_only, audited)
                self.assertFalse(admitted & excluded)
                self.assertFalse(admitted & context_only)
                self.assertFalse(excluded & context_only)
                for field in metadata["boundary_fields"]:
                    trust_sites = set(field["trust_site_ids"])
                    replacement_ids = set(
                        field["source_backed_replacement_ids"]
                    )
                    self.assertTrue(trust_sites.isdisjoint(excluded))
                    self.assertTrue(trust_sites <= admitted)
                    self.assertTrue(replacement_ids <= replacements)
                    self.assertTrue(trust_sites or replacement_ids)

    def test_excluded_or_undeclared_boundary_backing_is_rejected(self) -> None:
        text, metadata = target_019.obligation(target_019.PRIMARY)
        excluded = copy.deepcopy(metadata)
        excluded["boundary_fields"][0]["trust_site_ids"] = ["TS-019-D001"]
        with self.assertRaises(GuardError):
            validate_obligation(text, excluded)

        undeclared = copy.deepcopy(metadata)
        undeclared["boundary_fields"][0]["source_backed_replacement_ids"] = [
            "SRC-019-UNDECLARED"
        ]
        with self.assertRaises(GuardError):
            validate_obligation(text, undeclared)

        relabeled = copy.deepcopy(metadata)
        relabeled_id = "TS-019-D001"
        relabeled["boundary_scope"]["source_backed_replacement_ids"] = [
            relabeled_id
        ]
        relabeled["source_backed_replacements"][0][
            "replacement_id"
        ] = relabeled_id
        for field in relabeled["boundary_fields"]:
            field["source_backed_replacement_ids"] = [relabeled_id]
        with self.assertRaises(GuardError):
            validate_obligation(text, relabeled)

        unbacked = copy.deepcopy(metadata)
        unbacked["boundary_fields"][0]["source_backed_replacement_ids"] = []
        with self.assertRaises(GuardError):
            validate_obligation(text, unbacked)

        text, metadata = target_020.obligation(target_020.PRIMARY)
        excluded_020 = copy.deepcopy(metadata)
        excluded_020["boundary_fields"][0]["trust_site_ids"] = [
            "TS-020-D003"
        ]
        with self.assertRaises(GuardError):
            validate_obligation(text, excluded_020)

        relabeled_020 = copy.deepcopy(metadata)
        relabeled_020["boundary_scope"]["excluded_retained_trust_site_ids"].remove(
            "TS-020-D003"
        )
        relabeled_020["boundary_scope"]["admitted_trust_site_ids"].append(
            "TS-020-D003"
        )
        relabeled_020["source_backed_replacements"] = [
            replacement
            for replacement in relabeled_020["source_backed_replacements"]
            if "TS-020-D003" not in replacement["replaces_trust_site_ids"]
        ]
        for field in relabeled_020["boundary_fields"]:
            field["trust_site_ids"] = ["TS-020-D003"]
        with self.assertRaises(GuardError):
            target_020.validate_target_obligation(text, relabeled_020)

        fabricated = copy.deepcopy(metadata)
        fabricated["boundary_scope"]["admitted_trust_site_ids"].append(
            "TS-999-FABRICATED"
        )
        for field in fabricated["boundary_fields"]:
            field["trust_site_ids"] = ["TS-999-FABRICATED"]
        with self.assertRaises(GuardError):
            validate_obligation(text, fabricated)

    def test_ordered_cluster_reset_changes_only_cluster_result_cells(self) -> None:
        csv_rows, json_rows = delivered_crosswalk_rows()
        reset_csv, reset_json = run_pointer_cast_cluster.prepare_crosswalk_reset(
            csv_rows,
            json_rows,
        )
        self.assertEqual(reset_csv, reset_json)
        cluster_keys = set(run_pointer_cast_cluster.CLUSTER_KEYS)
        for before, after in zip(csv_rows, reset_csv):
            key = (before["target"], before["input_order"])
            changed = {
                field
                for field in before
                if before[field] != after[field]
            }
            if key in cluster_keys:
                self.assertTrue(
                    changed
                    <= {
                        "exact_output_determinism_status",
                        "completeness_modulo_reviewed_equivalence_status",
                    }
                )
                self.assertEqual(
                    {
                        field: after[field]
                        for field in run_pointer_cast_cluster.NOT_RUN
                    },
                    run_pointer_cast_cluster.NOT_RUN,
                )
            else:
                self.assertFalse(changed)

    def test_ordered_cluster_reset_requires_delivered_state(self) -> None:
        csv_rows, json_rows = delivered_crosswalk_rows()
        for rows in (csv_rows, json_rows):
            row = next(
                item
                for item in rows
                if item["target"] == target_019.TARGET
                and item["input_order"] == target_019.INPUT_ORDER
            )
            row.update(run_pointer_cast_cluster.NOT_RUN)
        with self.assertRaises(ValueError):
            run_pointer_cast_cluster.prepare_crosswalk_reset(
                csv_rows,
                json_rows,
            )

    def test_boundary_contains_no_answer_or_final_state(self) -> None:
        for module, _ in TARGETS:
            shared = json.dumps(
                module.boundary_manifest()["shared_boundary_observations"],
                sort_keys=True,
            )
            with self.subTest(target=module.TARGET):
                for forbidden in (
                    "returned pointer",
                    "endpoint",
                    "final state",
                    "answer",
                    "trace",
                ):
                    self.assertNotIn(forbidden, shared)

    def test_canonical_source_hashes_match(self) -> None:
        for module, _ in TARGETS:
            for binding in module.CANONICAL_SOURCE_BINDINGS:
                path = common.RUST_LIBRARY / binding.path
                excerpt = "".join(
                    path.read_text().splitlines(keepends=True)[
                        binding.start - 1 : binding.end
                    ]
                ).encode()
                with self.subTest(target=module.TARGET, source=binding.name):
                    self.assertEqual(common.sha256(path), binding.file_sha256)
                    self.assertEqual(
                        hashlib.sha256(excerpt).hexdigest(),
                        binding.excerpt_sha256,
                    )

    def test_synthetic_pointer_mutations_are_rejected(self) -> None:
        for module in (target_019, target_021, target_020):
            text, metadata = module.obligation(module.PRIMARY)
            mutations = (
                text.replace(
                    "(define-fun SliceCastAddress ((x Input)) Int\n"
                    "  (x_address x))",
                    "(define-fun SliceCastAddress ((x Input)) Int\n"
                    "  (x_length x))",
                ),
                text.replace(
                    "(define-fun SliceCastProvenance ((x Input)) Int\n"
                    "  (x_provenance x))",
                    "(define-fun SliceCastProvenance ((x Input)) Int\n  0)",
                ),
            )
            for mutated in mutations:
                with self.subTest(target=module.TARGET):
                    with self.assertRaises(GuardError):
                        module.validate_target_obligation(mutated, metadata)

    def test_range_offset_mutations_are_rejected(self) -> None:
        text, metadata = target_020.obligation(target_020.PRIMARY)
        mutations = (
            text.replace(
                "(+ (SliceCastAddress x) (* (x_length x) (x_element_size x)))",
                "(+ (SliceCastAddress x) (x_length x))",
                1,
            ),
            text.replace(
                "(define-fun PtrAddEndAllocation ((x Input)) Int\n"
                "  (SliceCastAllocation x))",
                "(define-fun PtrAddEndAllocation ((x Input)) Int\n  0)",
            ),
            text.replace(
                "(define-fun PtrAddEndProvenance ((x Input)) Int\n"
                "  (SliceCastProvenance x))",
                "(define-fun PtrAddEndProvenance ((x Input)) Int\n  0)",
            ),
        )
        for mutated in mutations:
            with self.assertRaises(GuardError):
                target_020.validate_target_obligation(mutated, metadata)

    def test_exact_equivalence_covers_every_state_field(self) -> None:
        for module in (target_019, target_020):
            text, metadata = module.obligation(module.PRIMARY)
            equality = (
                "(= (s_final_mutable_identity s1) "
                "(s_final_mutable_identity s2))"
            )
            self.assertIn(equality, text)
            with self.subTest(target=module.TARGET):
                with self.assertRaises(GuardError):
                    module.validate_target_obligation(
                        text.replace(equality, "true", 1),
                        metadata,
                    )

    def test_probe_matrix_has_required_cases(self) -> None:
        common_names = {
            "allocated_nonempty_non_zst",
            "allocated_empty_non_zst",
            "dangling_empty_non_zst",
            "allocated_nonempty_zst",
            "dangling_nonempty_zst",
            "invalid_null_pointer",
            "invalid_misaligned_pointer",
            "invalid_address_len_null_provenance_synthesis",
            "invalid_changed_output_allocation",
            "invalid_changed_output_provenance",
        }
        for module, _ in TARGETS:
            with self.subTest(target=module.TARGET):
                self.assertTrue(common_names <= set(module.PROBE_CASES))
        self.assertTrue(
            {
                "invalid_nonzero_offset_without_allocation",
                "invalid_nonzero_offset_without_provenance",
                "invalid_nonzero_offset_past_allocation",
                "invalid_offset_exceeds_isize",
                "invalid_address_overflow",
                "invalid_wrong_start_endpoint",
                "invalid_wrong_end_endpoint",
                "invalid_mutable_final_state_change",
            }
            <= set(target_020.PROBE_CASES)
        )

    def test_all_obligations_and_probes_have_expected_solver_results(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for module, _ in TARGETS:
            texts = [
                (module.obligation(purpose)[0], "unsat")
                for purpose in module.PURPOSES
            ] + [
                (module.probe_text(name), case["expected_solver_result"])
                for name, case in module.PROBE_CASES.items()
            ]
            for index, (text, expected) in enumerate(texts):
                with self.subTest(target=module.TARGET, index=index):
                    process = subprocess.run(
                        [str(z3), "-in", "-smt2"],
                        input=text,
                        text=True,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(
                        process.stdout.splitlines()[0],
                        expected,
                    )
                    self.assertEqual(process.stderr, "")
                    if expected == "sat":
                        self.assertGreater(len(process.stdout.splitlines()), 1)

    def test_independent_replay_checks_every_retained_input(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for module, replay_module in TARGETS:
            with self.subTest(target=module.TARGET):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    (root / "probes").mkdir()
                    for purpose, stem in (
                        (module.PRIMARY, "obligation"),
                        (module.EXACT_OUTPUT, "exact_output_obligation"),
                    ):
                        text, metadata = module.obligation(purpose)
                        (root / f"{stem}.smt2").write_text(text)
                        (root / f"{stem}.metadata.json").write_text(
                            json.dumps(metadata, indent=2, sort_keys=True) + "\n"
                        )
                    for name in module.PROBE_CASES:
                        (root / "probes" / f"{name}.smt2").write_text(
                            module.probe_text(name)
                        )
                    result = replay_module.replay(root, str(z3))
                self.assertEqual(result["status"], "passed")
                self.assertEqual(
                    set(result["obligations"]),
                    set(module.PURPOSES),
                )
                self.assertEqual(
                    set(result["satisfiability_and_rejection_probes"]),
                    set(module.PROBE_CASES),
                )

    def test_answer_bearing_boundary_metadata_is_rejected(self) -> None:
        text, metadata = target_020.obligation(target_020.PRIMARY)
        mutated = text.replace(
            "      (b_frame_token Int)))))",
            "      (b_frame_token Int)\n"
            "      (b_returned_end_address Int)))))",
        ).replace(
            "       (= (b_frame_token b) (x_frame_token x))))",
            "       (= (b_frame_token b) (x_frame_token x))\n"
            "       (= (b_returned_end_address b) "
            "(b_returned_end_address b))))",
            1,
        ).replace(
            "       (InputMemoryLayoutObserved x b)))",
            "       (InputMemoryLayoutObserved x b)\n"
            "       (= (b_returned_end_address b) "
            "(b_returned_end_address b))))",
            1,
        )
        changed = copy.deepcopy(metadata)
        changed["boundary_fields"].append(
            {
                "selector": "b_returned_end_address",
                "role": "selected_output",
                "source_citations": [
                    pointer_cast_cluster.MUT_PTR_ADD.reference
                ],
                "trust_site_ids": ["TS-020-D004"],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(mutated, changed)


if __name__ == "__main__":
    unittest.main()
