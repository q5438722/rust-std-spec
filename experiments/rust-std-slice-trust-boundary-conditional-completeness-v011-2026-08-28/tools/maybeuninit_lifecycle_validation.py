#!/usr/bin/env python3
"""Fail-closed validation for the 025/026/119 MaybeUninit increment."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import campaign_common as common
import align_to_pair as align_pair
import clone_effect_cluster as clone_cluster
import exact_mutable_iterator_partitions as exact_partitions
import mutable_edge_extraction as edge
import mutable_fixed_chunk_edges as fixed_chunks
import mutable_iterator_constructors as constructors
import split_at_mut_primitives as split_primitives
import split_off_pair as split_off
import raw_slice_pair as raw_slice
import slice_index_trio as slice_trio
import address_observer_pair as address_pair
import mutable_view_construction_cluster as mutable_views
import replay_maybeuninit_lifecycle_cluster as replay_cluster
import run_maybeuninit_lifecycle_cluster as runner
import target_025
import target_026
import target_119
import target_pipeline


MODULES = (target_026, target_119, target_025)
EXPECTED_RESULTS = {
    target_025.TARGET: {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    target_026.TARGET: {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    target_119.TARGET: {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def check_artifact(
    errors: list[str],
    record: dict[str, Any],
    *,
    label: str,
) -> Path | None:
    try:
        path = common.OUT / record["path"]
        expected = record["sha256"]
        expected_bytes = record["bytes"]
    except (KeyError, TypeError):
        errors.append(f"{label}: malformed artifact record")
        return None
    if (
        not path.is_file()
        or common.sha256(path) != expected
        or path.stat().st_size != expected_bytes
    ):
        errors.append(f"{label}: artifact is missing or hash/size changed")
        return None
    return path


def check_command(
    errors: list[str],
    record: dict[str, Any],
    *,
    expected_first_line: str | None,
    label: str,
) -> None:
    try:
        stdout = common.OUT / record["stdout"]
        stderr = common.OUT / record["stderr"]
        status = common.OUT / record["status"]
        command = common.OUT / record["command"]
    except (KeyError, TypeError):
        errors.append(f"{label}: malformed command record")
        return
    if (
        not command.is_file()
        or not stdout.is_file()
        or not stderr.is_file()
        or not status.is_file()
        or status.read_text() != "0\n"
        or stderr.read_text() != ""
        or record.get("exit_code") != 0
    ):
        errors.append(f"{label}: command capture is not clean")
        return
    if expected_first_line is not None:
        first = stdout.read_text().splitlines()
        if not first or first[0] != expected_first_line:
            errors.append(
                f"{label}: expected {expected_first_line}, got "
                f"{first[0] if first else '<empty>'}"
            )


def validate_target(errors: list[str], module: Any) -> None:
    root = common.OUT / "evidence/targets" / module.ARTIFACT_ID
    try:
        result = load_json(root / "result.json")
        authority = load_json(root / "authority_bindings.json")
        boundary = load_json(root / "boundary_manifest.json")
        bound = load_json(root / "bound_inputs_manifest.json")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{module.TARGET}: evidence is unreadable: {exc}")
        return
    if (
        result.get("target") != module.TARGET
        or result.get("input_order") != module.INPUT_ORDER
        or result.get("active_contract_sha256")
        != module.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != module.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != EXPECTED_RESULTS[module.TARGET]
    ):
        errors.append(f"{module.TARGET}: result identity/classification changed")
    bindings = authority.get("bindings", {})
    if (
        bindings.get("active_contract_sha256")
        != module.ACTIVE_CONTRACT_SHA256
        or bindings.get("active_contract_text") != module.ACTIVE_CONTRACT_TEXT
        or set(bindings.get("all_trust_site_ids", "").split(";"))
        != set(module.ALL_AUDITED_TRUST_SITES)
    ):
        errors.append(f"{module.TARGET}: authority binding changed")
    if (
        boundary != module.boundary_manifest()
        or not boundary.get("boundary_narrower_than_target")
    ):
        errors.append(f"{module.TARGET}: boundary manifest changed")
    artifacts = bound.get("artifacts", {})
    required_bound = {
        "active_contract.txt",
        "generated_declaration.rs",
        "target_source_item.rs",
        "target_public_docs.md",
        "implproof_harness.rs",
        "transformation_manifest.json",
        "dependency_assumption_manifest.json",
        "source_body.json",
        "trust_site_inventory.json",
    }
    if not required_bound <= set(artifacts):
        errors.append(f"{module.TARGET}: bound input package is incomplete")
    for name, record in artifacts.items():
        check_artifact(errors, record, label=f"{module.TARGET}/{name}")

    for purpose, stem in replay_cluster.OBLIGATION_STEMS.items():
        try:
            text = (root / f"{stem}.smt2").read_text()
            metadata = load_json(root / f"{stem}.metadata.json")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{module.TARGET}/{purpose}: unreadable: {exc}")
            continue
        try:
            module.validate_target_obligation(text, metadata)
        except ValueError as exc:
            errors.append(f"{module.TARGET}/{purpose}: {exc}")
        expected = replay_cluster.EXPECTED_THEOREM_RESULTS[module.TARGET][purpose]
        check_command(
            errors,
            result["obligations"][purpose]["solver"],
            expected_first_line=expected,
            label=f"{module.TARGET}/{purpose}",
        )

    for name, expected in module.PROBE_EXPECTED_RESULTS.items():
        if (root / "probes" / f"{name}.smt2").read_text() != module.probe_text(name):
            errors.append(f"{module.TARGET}/{name}: probe text changed")
        check_command(
            errors,
            result["satisfiability_probes"][name]["solver"],
            expected_first_line=expected,
            label=f"{module.TARGET}/{name}",
        )

    model_path = check_artifact(
        errors,
        result["verus"]["captured_model"],
        label=f"{module.TARGET}/Verus model",
    )
    if model_path is not None and "external_body" in model_path.read_text():
        errors.append(f"{module.TARGET}: Verus model contains external_body")
    check_command(
        errors,
        result["verus"]["typecheck"],
        expected_first_line=None,
        label=f"{module.TARGET}/Verus typecheck",
    )
    check_command(
        errors,
        result["verus"]["verification"],
        expected_first_line="verification results:: "
        + (
            "3 verified, 0 errors"
            if module is target_119
            else "2 verified, 0 errors"
        ),
        label=f"{module.TARGET}/Verus verification",
    )
    if module is target_026:
        witness = result.get("witness", {})
        if witness.get("semantic_replay", {}).get("status") != "passed":
            errors.append("target-026 concrete SAT witness was not replayed")
        check_command(
            errors,
            result["counterexample_model"]["solver"],
            expected_first_line="sat",
            label="target-026/fixed countermodel",
        )


def validate(errors: list[str]) -> None:
    for module in MODULES:
        validate_target(errors, module)

    try:
        manifest = load_json(
            common.OUT / "evidence/maybeuninit_lifecycle_cluster/manifest.json"
        )
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"MaybeUninit cluster manifest is unreadable: {exc}")
        return
    if (
        manifest.get("execution_order")
        != [target_026.TARGET, target_119.TARGET, target_025.TARGET]
        or manifest.get("classified_rows") != 22
        or manifest.get("not_run_rows") != 40
        or manifest.get("stage_transition") != "not-authorized"
        or manifest.get("independent_solver_and_witness_replay", {})
        .get("result", {})
        .get("status")
        != "passed"
    ):
        errors.append("MaybeUninit cluster manifest is malformed")
    preservation = manifest.get("preserved_certified_evidence", {})
    if set(preservation) != set(runner.PRESERVED_ARTIFACT_IDS):
        errors.append("MaybeUninit cluster does not cover all 19 preserved trees")
    for artifact_id, hashes in preservation.items():
        root = common.OUT / "evidence/targets" / artifact_id
        actual = runner.tree_digest(root)
        if (
            hashes.get("before_sha256") != hashes.get("after_sha256")
            or hashes.get("after_sha256") != actual
        ):
            errors.append(f"MaybeUninit cluster mutated {artifact_id}")

    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    expected = dict(runner.BASELINE_RESULTS)
    expected.update(
        {
            (module.TARGET, module.INPUT_ORDER): EXPECTED_RESULTS[module.TARGET]
            for module in MODULES
        }
    )
    expected.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in split_primitives.TARGET_KEYS
        }
    )
    expected.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in split_off.TARGET_KEYS
        }
    )
    expected.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in clone_cluster.TARGET_KEYS
        }
    )
    expected.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in edge.TARGET_KEYS
        }
    )
    expected.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in constructors.TARGET_KEYS
        }
    )
    expected.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in exact_partitions.TARGET_KEYS
        }
    )
    expected.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in fixed_chunks.TARGET_KEYS
        }
    )
    expected.update(
        {
            ("core::slice::sort_unstable", "80"): {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
            },
            ("core::slice::sort_unstable_by_key", "82"): {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
            },
            ("core::slice::select_nth_unstable", "77"): {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
            },
            ("core::slice::select_nth_unstable_by", "78"): {
                "exact_output_determinism_status": "missing-source-backed-model",
                "completeness_modulo_reviewed_equivalence_status": "missing-source-backed-model",
            },
            ("core::slice::select_nth_unstable_by_key", "79"): {
                "exact_output_determinism_status": "missing-source-backed-model",
                "completeness_modulo_reviewed_equivalence_status": "missing-source-backed-model",
            },
        }
    )
    expected.update(
        {
            (config.target, config.input_order): config.expected_classification
            for config in raw_slice.TARGETS
        }
    )
    expected.update(
        {
            (config.target, config.input_order): config.expected_classification
            for config in slice_trio.TARGETS
        }
    )
    expected.update(
        {
            (config.target, config.input_order): config.expected_classification
            for config in address_pair.TARGETS
        }
    )
    expected.update(
        {
            (config.target, config.input_order): config.expected_classification
            for config in mutable_views.TARGETS
        }
    )
    expected.update(
        {
            (config.target, config.input_order): config.expected_classification
            for config in align_pair.TARGETS
        }
    )
    for row in rows:
        key = row["target"], row["input_order"]
        actual = {
            field: row[field] for field in target_pipeline.RESULT_FIELDS
        }
        wanted = expected.get(
            key, {field: "not-run" for field in target_pipeline.RESULT_FIELDS}
        )
        if actual != wanted:
            errors.append(f"{key}: result differs from 25-target ledger")
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows
    )
    if len(expected) != 62 or not_run != 0:
        errors.append("delivered ledger did not finish at 62/0")
