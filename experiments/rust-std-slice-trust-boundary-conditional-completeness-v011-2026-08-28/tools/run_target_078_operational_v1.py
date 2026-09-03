#!/usr/bin/env python3
"""Build and capture additive target-078 operational evidence."""

from __future__ import annotations

import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import replay_target_078_operational_v1
import target_078_operational_smt_v1 as smt
import target_078_operational_v1 as model
import target_078_operational_witness_v1 as witnesses
import target_pipeline


EVIDENCE_ROOT = common.OUT / "evidence/target_078_operational_v1"
SOURCE_BINDINGS = EVIDENCE_ROOT / "source_bindings.json"
SOURCE_PROOF = (
    common.OUT
    / "proofs/078_core_slice_select_nth_unstable_by_operational_v1.rs"
)
CERTIFIED_TARGET_ROOT = (
    common.OUT
    / "evidence/targets/078_core_slice_select_nth_unstable_by"
)
TARGET_079_ROOT = (
    common.OUT
    / "evidence/targets/079_core_slice_select_nth_unstable_by_key"
)
FROZEN_078_ROOT = (
    common.OUT
    / "provenance/frozen/implproof/078_core_slice_select_nth_unstable_by"
)
FROZEN_079_ROOT = (
    common.OUT
    / "provenance/frozen/implproof/079_core_slice_select_nth_unstable_by_key"
)
PIPELINE_STATE = common.OUT / "research/PIPELINE_STATE.json"
LEDGER_CSV = common.OUT / "crosswalk/target_to_proof_boundary.csv"
LEDGER_JSON = common.OUT / "crosswalk/target_to_proof_boundary.json"
ADDENDUM_CSV = (
    common.OUT / "crosswalk/target_078_operational_v1_addendum.csv"
)
ADDENDUM_JSON = (
    common.OUT / "crosswalk/target_078_operational_v1_addendum.json"
)
REVIEW_ADDENDUM = (
    common.OUT / "review/REVIEW_ADDENDUM_TARGET_078_OPERATIONAL_V1.md"
)

EXPECTED_RESULT_STATUSES = {
    "exact_output_determinism_status": "conditional-complete",
    "completeness_modulo_reviewed_equivalence_status": (
        "conditional-complete"
    ),
}
BASELINE_STATUSES = {
    "exact_output_determinism_status": "missing-source-backed-model",
    "completeness_modulo_reviewed_equivalence_status": (
        "missing-source-backed-model"
    ),
}
EXPECTED_VERUS_SUMMARY = "verification results:: 5 verified, 0 errors"


def tree_digest(root: Path) -> str:
    if not root.is_dir():
        raise RuntimeError(f"protected tree is missing: {root}")
    digest = sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def file_digest(path: Path) -> str:
    if not path.is_file():
        raise RuntimeError(f"protected file is missing: {path}")
    return sha256(path.read_bytes()).hexdigest()


def _load_ledger() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    csv_rows = common.read_csv(LEDGER_CSV)
    json_rows = json.loads(LEDGER_JSON.read_text())
    if csv_rows != json_rows or len(csv_rows) != 62:
        raise RuntimeError("certified crosswalk projections diverged")
    return csv_rows, json_rows


def _target_row(
    rows: list[dict[str, Any]], order: str
) -> dict[str, Any]:
    matches = [row for row in rows if row["input_order"] == order]
    if len(matches) != 1:
        raise RuntimeError(f"crosswalk does not contain one order {order}")
    return matches[0]


def _materialize_bound_inputs() -> None:
    root = EVIDENCE_ROOT / "bound_inputs"
    root.mkdir(parents=True, exist_ok=True)
    copies = {
        (
            CERTIFIED_TARGET_ROOT / "bound_inputs/source_item.rs"
        ): root / "source_item.rs",
        (
            CERTIFIED_TARGET_ROOT / "bound_inputs/select.rs"
        ): root / "select.rs",
        (
            common.RUST_LIBRARY / "core/src/slice/sort/shared/pivot.rs"
        ): root / "pivot.rs",
        (
            CERTIFIED_TARGET_ROOT / "bound_inputs/partition.rs"
        ): root / "partition_entry.rs",
        (
            common.RUST_LIBRARY
            / "core/src/slice/sort/unstable/quicksort.rs"
        ): root / "quicksort.rs",
        (
            CERTIFIED_TARGET_ROOT / "bound_inputs/smallsort.rs"
        ): root / "smallsort.rs",
        (
            common.RUST_LIBRARY / "core/src/macros/mod.rs"
        ): root / "cfg_select.rs",
        (
            common.RUST_LIBRARY / "core/src/mem/mod.rs"
        ): root / "sized_type_properties.rs",
        (
            CERTIFIED_TARGET_ROOT
            / "bound_inputs/callback_vocabulary.rs"
        ): root / "callback_vocabulary.rs",
    }
    for source, destination in copies.items():
        if not source.is_file():
            raise RuntimeError(f"source-closure input is missing: {source}")
        shutil.copyfile(source, destination)


def _validate_source_bindings() -> dict[str, Any]:
    manifest = json.loads(SOURCE_BINDINGS.read_text())
    if (
        manifest.get("model_id") != model.MODEL_ID
        or manifest.get("model_version") != model.MODEL_VERSION
        or not manifest.get("source_model_complete")
        or not manifest.get("classification_eligible")
        or manifest.get("missing_source_phases") != []
    ):
        raise RuntimeError("source-binding manifest is not complete")
    for binding in manifest.get("covered_source", []):
        path = common.OUT / binding["path"]
        if not path.is_file():
            raise RuntimeError(f"bound source is missing: {path}")
        text = path.read_text()
        for anchor in binding.get("semantic_anchors", []):
            if anchor not in text:
                raise RuntimeError(
                    f"{binding['role']}: source anchor is missing: {anchor}"
                )
    if len(manifest.get("covered_source", [])) != 9:
        raise RuntimeError("source closure must contain nine readable bindings")
    return manifest


def _solver_capture(
    z3: str, label: str, path: Path, expected: str
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        EVIDENCE_ROOT / label,
        [z3, "-smt2", str(path)],
        cwd=common.OUT,
    )
    target_pipeline.require_clean_result(record, expected, label=label)
    record.update(
        {
            "solver_result": target_pipeline.first_output_line(record),
            "expected_solver_result": expected,
        }
    )
    return record


def _write_crosswalk_addendum(
    baseline_row: dict[str, Any],
    classification: dict[str, str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    row = {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "baseline_crosswalk_path": common.relpath(LEDGER_JSON),
        "baseline_classification": BASELINE_STATUSES,
        "additive_classification": classification,
        "equivalence_kind": "exact-principal-return-and-final-state",
        "evidence_root": common.relpath(EVIDENCE_ROOT),
        "independent_review": common.relpath(REVIEW_ADDENDUM),
        "baseline_row_mutated": False,
        "target_079_mutated": False,
        "manager_stage_mutated": False,
    }
    common.write_json(ADDENDUM_JSON, row)
    csv_row = {
        "input_order": model.INPUT_ORDER,
        "target": model.TARGET,
        "model_id": model.MODEL_ID,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "baseline_exact_output_determinism_status": (
            BASELINE_STATUSES["exact_output_determinism_status"]
        ),
        "baseline_completeness_modulo_reviewed_equivalence_status": (
            BASELINE_STATUSES[
                "completeness_modulo_reviewed_equivalence_status"
            ]
        ),
        "additive_exact_output_determinism_status": (
            classification["exact_output_determinism_status"]
        ),
        "additive_completeness_modulo_reviewed_equivalence_status": (
            classification[
                "completeness_modulo_reviewed_equivalence_status"
            ]
        ),
        "equivalence_kind": "exact-principal-return-and-final-state",
        "evidence_root": common.relpath(EVIDENCE_ROOT),
        "independent_review": common.relpath(REVIEW_ADDENDUM),
    }
    common.write_csv(ADDENDUM_CSV, [csv_row], list(csv_row))
    return (
        target_pipeline.artifact_record(ADDENDUM_JSON),
        target_pipeline.artifact_record(ADDENDUM_CSV),
    )


def _derive_classification(
    obligations: dict[str, Any],
    regressions: dict[str, Any],
    probes: dict[str, Any],
    mutations: dict[str, Any],
    replay_result: dict[str, Any],
    verification_stdout: str,
    review_text: str,
) -> dict[str, str]:
    if (
        set(obligations) != set(smt.PURPOSES)
        or any(
            evidence["solver"].get("solver_result") != "unsat"
            for evidence in obligations.values()
        )
        or set(regressions)
        != {
            "immutable_boundary_divergence",
            "source_swap_mutation",
            smt.LENGTH_17_CORRESPONDENCE,
        }
        or any(
            evidence["solver"].get("solver_result") != "unsat"
            for evidence in regressions.values()
        )
        or set(probes) != set(smt.PROBE_KINDS)
        or any(
            evidence["solver"].get("solver_result") != "sat"
            for evidence in probes.values()
        )
        or set(mutations) != set(smt.MUTATION_PROBES)
        or any(
            evidence["solver"].get("solver_result") != "unsat"
            for evidence in mutations.values()
        )
        or replay_result.get("status") != "passed"
        or EXPECTED_VERUS_SUMMARY not in verification_stdout
        or "**VERDICT: ACCEPT**" not in review_text
        or model.TARGET not in review_text
        or not model.SOURCE_MODEL_COMPLETE
        or model.MISSING_SOURCE_PHASES
    ):
        raise RuntimeError(
            "target-078 classification prerequisites are incomplete"
        )
    return dict(EXPECTED_RESULT_STATUSES)


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for target-078 operational evidence")
    if not SOURCE_PROOF.is_file():
        raise RuntimeError(f"parameterized Verus proof is missing: {SOURCE_PROOF}")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    _materialize_bound_inputs()
    source_manifest = _validate_source_bindings()

    csv_rows_before, json_rows_before = _load_ledger()
    target_row = _target_row(json_rows_before, model.INPUT_ORDER)
    target_079_row = _target_row(json_rows_before, "79")
    actual_baseline = {
        field: target_row[field] for field in target_pipeline.RESULT_FIELDS
    }
    if actual_baseline != BASELINE_STATUSES:
        raise RuntimeError(
            f"certified target-078 baseline changed: {actual_baseline!r}"
        )
    target_079_before = dict(target_079_row)

    protected_trees = {
        "certified_target_078": CERTIFIED_TARGET_ROOT,
        "target_079": TARGET_079_ROOT,
        "frozen_target_078": FROZEN_078_ROOT,
        "frozen_target_079": FROZEN_079_ROOT,
    }
    protected_files = {
        "pipeline_state": PIPELINE_STATE,
        "ledger_csv": LEDGER_CSV,
        "ledger_json": LEDGER_JSON,
        "certified_target_078_proof": (
            common.OUT / "proofs/078_core_slice_select_nth_unstable_by.rs"
        ),
        "target_079_proof": (
            common.OUT
            / "proofs/079_core_slice_select_nth_unstable_by_key.rs"
        ),
    }
    tree_before = {
        name: tree_digest(path) for name, path in protected_trees.items()
    }
    file_before = {
        name: file_digest(path) for name, path in protected_files.items()
    }

    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    boundary_path = EVIDENCE_ROOT / "boundary_manifest.json"
    common.write_json(boundary_path, model.boundary_manifest())

    obligations: dict[str, Any] = {}
    for filename, purpose in (
        ("exact_output_obligation", smt.EXACT),
        ("obligation", smt.FULL),
    ):
        text = smt.obligation_text(purpose)
        metadata = smt.obligation_metadata(purpose)
        smt.validate_obligation(text, metadata)
        smt_path = EVIDENCE_ROOT / f"{filename}.smt2"
        metadata_path = EVIDENCE_ROOT / f"{filename}.metadata.json"
        smt_path.write_text(text)
        common.write_json(metadata_path, metadata)
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": _solver_capture(
                z3, filename, smt_path, "unsat"
            ),
        }

    nonvacuity_path = EVIDENCE_ROOT / "nonvacuity.smt2"
    nonvacuity_path.write_text(smt.nonvacuity_text())
    nonvacuity = {
        "smt": target_pipeline.artifact_record(nonvacuity_path),
        "solver": _solver_capture(
            z3, "nonvacuity", nonvacuity_path, "sat"
        ),
    }

    regressions: dict[str, Any] = {}
    for label, text in (
        ("immutable_boundary_divergence", smt.immutable_replay_text()),
        ("source_swap_mutation", smt.swap_regression_text()),
        (
            smt.LENGTH_17_CORRESPONDENCE,
            smt.length_17_correspondence_text(),
        ),
    ):
        path = EVIDENCE_ROOT / f"{label}.smt2"
        path.write_text(text)
        regressions[label] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _solver_capture(z3, label, path, "unsat"),
        }

    probes: dict[str, Any] = {}
    for kind in smt.PROBE_KINDS:
        path = EVIDENCE_ROOT / f"probe_{kind}.smt2"
        path.write_text(smt.probe_text(kind))
        probes[kind] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _solver_capture(
                z3, f"probe_{kind}", path, "sat"
            ),
        }

    semantic_mutations: dict[str, Any] = {}
    for kind in smt.MUTATION_PROBES:
        path = EVIDENCE_ROOT / f"mutation_{kind}.smt2"
        path.write_text(smt.mutation_probe_text(kind))
        semantic_mutations[kind] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _solver_capture(
                z3, f"mutation_{kind}", path, "unsat"
            ),
        }

    witness_path = EVIDENCE_ROOT / "witness.json"
    common.write_json(witness_path, witnesses.witness_payload())
    witness_replay = target_pipeline.capture_command(
        EVIDENCE_ROOT / "witness_replay",
        [
            sys.executable,
            str(common.OUT / "tools/replay_target_078_operational_v1.py"),
            "--witness",
            str(witness_path),
        ],
        cwd=common.OUT,
    )
    replay_stdout = (common.OUT / witness_replay["stdout"]).read_text()
    replay_stderr = (common.OUT / witness_replay["stderr"]).read_text()
    if witness_replay["exit_code"] != 0 or replay_stderr:
        raise RuntimeError("target-078 operational witness replay failed")
    replay_result = json.loads(replay_stdout)
    if replay_result.get("status") != "passed":
        raise RuntimeError("target-078 operational witness did not pass")
    witness_replay["result"] = replay_result

    captured_proof = EVIDENCE_ROOT / "verus/selection_model.rs"
    captured_proof.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_PROOF, captured_proof)
    proof_text = captured_proof.read_text()
    for forbidden in ("external_body", "assume(", "admit(", "axiom"):
        if forbidden in proof_text:
            raise RuntimeError(
                f"parameterized Verus proof contains {forbidden!r}"
            )
    typecheck = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/typecheck",
        [
            str(common.VERUS),
            str(captured_proof),
            "--crate-type=lib",
            "--no-verify",
        ],
        cwd=common.OUT,
    )
    if (
        typecheck["exit_code"] != 0
        or (common.OUT / typecheck["stderr"]).read_text()
    ):
        raise RuntimeError("target-078 operational Verus proof did not type-check")
    verification = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/verification",
        [str(common.VERUS), str(captured_proof), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (
        common.OUT / verification["stdout"]
    ).read_text()
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or EXPECTED_VERUS_SUMMARY not in verification_stdout
    ):
        raise RuntimeError("target-078 operational Verus proof did not verify")

    if not REVIEW_ADDENDUM.is_file():
        raise RuntimeError("target-078 independent review addendum is missing")
    review_text = REVIEW_ADDENDUM.read_text()
    classification = _derive_classification(
        obligations,
        regressions,
        probes,
        semantic_mutations,
        replay_result,
        verification_stdout,
        review_text,
    )
    addendum_json, addendum_csv = _write_crosswalk_addendum(
        target_row, classification
    )

    csv_rows_after, json_rows_after = _load_ledger()
    if (
        csv_rows_after != csv_rows_before
        or json_rows_after != json_rows_before
        or _target_row(json_rows_after, "79") != target_079_before
    ):
        raise RuntimeError("additive runner mutated the certified crosswalk")
    tree_after = {
        name: tree_digest(path) for name, path in protected_trees.items()
    }
    file_after = {
        name: file_digest(path) for name, path in protected_files.items()
    }
    if tree_after != tree_before:
        raise RuntimeError("additive runner mutated protected evidence")
    if file_after != file_before:
        raise RuntimeError("additive runner mutated protected files")

    result = {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "artifact_id": "target_078_operational_v1",
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "active_contract_text": source_manifest["active_contract"][
            "contract_text"
        ],
        "classification": classification,
        "classification_scope": (
            "additive target-078 operational-v1 crosswalk addendum; the "
            "certified campaign ledger remains byte-identical"
        ),
        "classification_basis": (
            "Both arbitrary-domain exact projections are direct clean UNSAT "
            "under one total immutable callback relation and completed "
            "executions. ExactRunState is a source-structured big-step "
            "translation of every Rust 1.96 helper and preserves callback "
            "state, panic restoration, exact sequence mutations, returned "
            "references, and terminal status. The independently executable "
            "Python interpreter supplies the source oracle for the permanent "
            "length-17 correspondence regression. The trusted-free Verus "
            "artifact proves the terminal-only, lossless projection of every "
            "retained exact result field."
        ),
        "source_model_complete": True,
        "classification_eligible": True,
        "unresolved_source_model_phases": [],
        "source_bindings": target_pipeline.artifact_record(SOURCE_BINDINGS),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "obligations": obligations,
        "nonvacuity": nonvacuity,
        "semantic_force_probes": probes,
        "semantic_mutation_regressions": semantic_mutations,
        "regressions": regressions,
        "witness": target_pipeline.artifact_record(witness_path),
        "witness_replay": witness_replay,
        "verus": {
            "source_model": target_pipeline.artifact_record(SOURCE_PROOF),
            "captured_model": target_pipeline.artifact_record(captured_proof),
            "typecheck": typecheck,
            "verification": verification,
            "expected_summary": EXPECTED_VERUS_SUMMARY,
            "parameterization": (
                "arbitrary Seq<int> length/index, total immutable callback "
                "maps, both build configurations, and fuel-free terminal "
                "exact results"
            ),
            "evidence_scope": (
                "Trusted-free terminal control lemmas and a lossless checked "
                "projection for every exact return/final-state field; the "
                "source-exact classification transition is ExactRunState."
            ),
        },
        "crosswalk_addendum": {
            "json": addendum_json,
            "csv": addendum_csv,
            "certified_ledger_mutated": False,
        },
        "trust_site_dispositions": source_manifest[
            "trust_site_dispositions"
        ],
        "preservation": {
            "protected_trees": {
                name: {
                    "before_sha256": tree_before[name],
                    "after_sha256": tree_after[name],
                }
                for name in tree_before
            },
            "protected_files": {
                name: {
                    "before_sha256": file_before[name],
                    "after_sha256": file_after[name],
                }
                for name in file_before
            },
            "target_079_row_unchanged": True,
            "pipeline_state_unchanged": True,
        },
        "independent_review": {
            "status": "accepted",
            "verdict": "ACCEPT",
            "addendum": target_pipeline.artifact_record(REVIEW_ADDENDUM),
        },
        "stage_transition": "disabled",
    }
    common.write_json(EVIDENCE_ROOT / "result.json", result)

    print("target_078_operational_v1=PASS")
    print("exact_output_and_final_state=unsat")
    print("completeness_modulo_exact_equivalence=unsat")
    print(f"semantic_force_probes={len(probes)}_sat")
    print(f"semantic_mutations={len(semantic_mutations)}_unsat")
    print("witness_replay=passed")
    print("verus=5_verified_0_errors")
    print("certified_target_078=preserved")
    print("target_079=preserved")
    print("pipeline_state=preserved")
    print("crosswalk=additive_only")


if __name__ == "__main__":
    main()
