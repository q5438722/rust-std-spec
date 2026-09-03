#!/usr/bin/env python3
"""Build and capture additive target-079 operational-v1 evidence."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import preservation_policy_v3 as preservation_policy
import target_079_operational_smt_v1 as smt
import target_079_operational_v1 as model
import target_079_operational_witness_v1 as witnesses
import target_pipeline


EVIDENCE_ROOT = common.OUT / "evidence/target_079_operational_v1"
SOURCE_BINDINGS = EVIDENCE_ROOT / "source_bindings.json"
SOURCE_PROOF = (
    common.OUT
    / "proofs/079_core_slice_select_nth_unstable_by_key_operational_v1.rs"
)
BASELINE_078_ROOT = (
    common.OUT
    / "evidence/targets/078_core_slice_select_nth_unstable_by"
)
BASELINE_079_ROOT = (
    common.OUT
    / "evidence/targets/079_core_slice_select_nth_unstable_by_key"
)
ACCEPTED_078_ROOT = common.OUT / "evidence/target_078_operational_v1"
FROZEN_078_ROOT = (
    common.OUT
    / "provenance/frozen/implproof/078_core_slice_select_nth_unstable_by"
)
FROZEN_079_ROOT = (
    common.OUT
    / "provenance/frozen/implproof/079_core_slice_select_nth_unstable_by_key"
)
PIPELINE_STATE = common.OUT / "research/PIPELINE_STATE.json"
GROUND_TRUTH = common.OUT / "research/GROUND_TRUTH.md"
LEDGER_CSV = common.OUT / "crosswalk/target_to_proof_boundary.csv"
LEDGER_JSON = common.OUT / "crosswalk/target_to_proof_boundary.json"
ADDENDUM_CSV = (
    common.OUT / "crosswalk/target_079_operational_v1_addendum.csv"
)
ADDENDUM_JSON = (
    common.OUT / "crosswalk/target_079_operational_v1_addendum.json"
)
REVIEW_ADDENDUM = (
    common.OUT / "review/REVIEW_ADDENDUM_TARGET_079_OPERATIONAL_V1.md"
)

EXPECTED_STATUSES = {
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
EXPECTED_VERUS_SUMMARY = "verification results:: 7 verified, 0 errors"
EXPECTED_CAMPAIGN_REVIEWS_SHA256 = (
    "4aa3502700769d379be3caca4bcfb927c9fbd36db194ce883ae1136e26ca993f"
)


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


def protected_tree_digest(name: str, root: Path) -> str:
    if name == "campaign_reviews":
        try:
            return preservation_policy.historical_review_digest(root)
        except preservation_policy.PreservationPolicyError as exc:
            raise RuntimeError(
                f"versioned preservation policy failed: {exc}"
            ) from exc
    return tree_digest(root)


def file_digest(path: Path) -> str:
    if not path.is_file():
        raise RuntimeError(f"protected file is missing: {path}")
    return sha256(path.read_bytes()).hexdigest()


def _clean_generated_probe_artifacts() -> None:
    prefixes = (
        "probe_selection_",
        "mutation_selection_",
        "probe_adapter_",
        "mutation_adapter_",
    )
    for path in EVIDENCE_ROOT.iterdir():
        if not path.name.startswith(prefixes):
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


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


def _materialize_source_bindings() -> dict[str, Any]:
    bound = EVIDENCE_ROOT / "bound_inputs"
    bound.mkdir(parents=True, exist_ok=True)
    copies = {
        (
            BASELINE_079_ROOT / "bound_inputs/source_item.rs"
        ): bound / "source_item.rs",
        (
            ACCEPTED_078_ROOT / "bound_inputs/select.rs"
        ): bound / "select.rs",
        (
            ACCEPTED_078_ROOT / "bound_inputs/pivot.rs"
        ): bound / "pivot.rs",
        (
            ACCEPTED_078_ROOT / "bound_inputs/partition_entry.rs"
        ): bound / "partition_entry.rs",
        (
            ACCEPTED_078_ROOT / "bound_inputs/quicksort.rs"
        ): bound / "quicksort.rs",
        (
            ACCEPTED_078_ROOT / "bound_inputs/smallsort.rs"
        ): bound / "smallsort.rs",
        (
            ACCEPTED_078_ROOT / "bound_inputs/cfg_select.rs"
        ): bound / "cfg_select.rs",
        (
            ACCEPTED_078_ROOT / "bound_inputs/sized_type_properties.rs"
        ): bound / "sized_type_properties.rs",
        (
            BASELINE_079_ROOT / "bound_inputs/callback_vocabulary.rs"
        ): bound / "callback_vocabulary.rs",
        (
            common.OUT / "research/probes/target_079_adapter_probe.rs"
        ): bound / "adapter_probe.rs",
    }
    for source, destination in copies.items():
        if not source.is_file():
            raise RuntimeError(f"source-closure input is missing: {source}")
        shutil.copyfile(source, destination)

    authority = json.loads(
        (BASELINE_079_ROOT / "authority_bindings.json").read_text()
    )["bindings"]
    ground = json.loads(
        (EVIDENCE_ROOT / "ground_truth/manifest.json").read_text()
    )
    accepted_source = json.loads(
        (ACCEPTED_078_ROOT / "source_bindings.json").read_text()
    )
    covered = []
    roles = {
        "source_item.rs": "public-key-adapter",
        "select.rs": "selection-and-fallback",
        "pivot.rs": "pivot-selection",
        "partition_entry.rs": "partition-entry",
        "quicksort.rs": "partition-and-unwind",
        "smallsort.rs": "small-sort-and-unwind",
        "cfg_select.rs": "configuration-dispatch",
        "sized_type_properties.rs": "zst-dispatch",
        "callback_vocabulary.rs": "key-contract-vocabulary",
        "adapter_probe.rs": "adapter-lifetime-ground-truth",
    }
    for filename, role in roles.items():
        path = bound / filename
        covered.append(
            {
                "role": role,
                **target_pipeline.artifact_record(path),
            }
        )
    manifest = {
        "schema_version": 2,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "source_model_complete": True,
        "classification_eligible": True,
        "missing_source_phases": [],
        "active_contract": {
            "authority_path": (
                "evidence/targets/"
                "079_core_slice_select_nth_unstable_by_key/"
                "authority_bindings.json"
            ),
            "contract_sha256": authority["active_contract_sha256"],
            "contract_text": authority["active_contract_text"],
            "conjuncts": list(model.ACTIVE_CONJUNCTS),
        },
        "boundary": {
            "admitted_trust_site_ids": list(
                model.ADMITTED_TRUST_SITE_IDS
            ),
            "observations": model.boundary_manifest()[
                "shared_boundary_observations"
            ],
            "prohibited_observations": model.boundary_manifest()[
                "excluded_from_boundary"
            ],
        },
        "selection_reuse": {
            "accepted_model_id": accepted_source["model_id"],
            "accepted_source_model_complete": accepted_source[
                "source_model_complete"
            ],
            "accepted_result": target_pipeline.artifact_record(
                ACCEPTED_078_ROOT / "result.json"
            ),
            "python_engine": target_pipeline.artifact_record(
                common.OUT / "tools/target_078_operational_v1.py"
            ),
            "exact_smt_engine": target_pipeline.artifact_record(
                common.OUT / "tools/target_078_exact_smt_v1.py"
            ),
            "classification_inherited": False,
        },
        "adapter_ground_truth": {
            "toolchain": ground["toolchain"],
            "scenario_count": len(ground["scenarios"]),
            "manifest": target_pipeline.artifact_record(
                EVIDENCE_ROOT / "ground_truth/manifest.json"
            ),
            "mir": target_pipeline.artifact_record(
                EVIDENCE_ROOT / "ground_truth/probe.mir"
            ),
        },
        "covered_source": covered,
        "formal_source_transition": (
            "tools/target_079_operational_smt_v1.py::"
            "AdapterTransition + imported ExactRunState"
        ),
        "trust_site_dispositions": {
            "TS-079-D002": (
                "replaced-by-key-ord-drop-adapter-transition"
            ),
            "TS-079-D003": (
                "replaced-by-complete-imported-selection-source-model"
            ),
            "TS-079-E001": (
                "excluded-and-replaced-by-complete-source-model"
            ),
        },
    }
    common.write_json(SOURCE_BINDINGS, manifest)
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
        "accepted_target_078_mutated": False,
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
    *,
    obligations: dict[str, Any],
    nonvacuity: dict[str, Any],
    selection_probes: dict[str, Any],
    adapter_probes: dict[str, Any],
    selection_mutations: dict[str, Any],
    adapter_mutations: dict[str, Any],
    regressions: dict[str, Any],
    ground_manifest: dict[str, Any],
    replay_result: dict[str, Any],
    verification_stdout: str,
    negative_verus: dict[str, Any],
    review_text: str,
    require_review: bool,
) -> dict[str, str]:
    complete = (
        set(obligations) == set(smt.PURPOSES)
        and all(
            evidence["solver"]["solver_result"] == "unsat"
            for evidence in obligations.values()
        )
        and nonvacuity["solver"]["solver_result"] == "sat"
        and set(selection_probes) == set(smt.SELECTION_PROBE_KINDS)
        and set(smt.SELECTION_PHASE_COVERAGE)
        == set(model.selection.SOURCE_PHASES)
        and all(
            set(probes) <= set(selection_probes)
            for probes in smt.SELECTION_PHASE_COVERAGE.values()
        )
        and set(smt.PARTITION_KERNEL_PROBES.values())
        <= set(selection_probes)
        and all(
            evidence["solver"]["solver_result"] == "sat"
            for evidence in selection_probes.values()
        )
        and set(adapter_probes) == set(smt.ADAPTER_PROBE_KINDS)
        and all(
            evidence["solver"]["solver_result"] == "sat"
            for evidence in adapter_probes.values()
        )
        and set(selection_mutations)
        == set(smt.SELECTION_MUTATION_PROBES)
        and all(
            evidence["solver"]["solver_result"] == "unsat"
            for evidence in selection_mutations.values()
        )
        and set(adapter_mutations)
        == set(smt.ADAPTER_MUTATION_PROBES)
        and all(
            evidence["solver"]["solver_result"] == "unsat"
            for evidence in adapter_mutations.values()
        )
        and set(regressions)
        == {
            smt.LENGTH_17_CORRESPONDENCE,
            *smt.EXACT_CLEANUP_REGRESSIONS,
        }
        and all(
            evidence["solver"]["solver_result"] == "unsat"
            for evidence in regressions.values()
        )
        and len(ground_manifest["scenarios"]) == 10
        and (
            "ord-lt-panic-left-drop-panic"
            in ground_manifest["scenarios"]
        )
        and replay_result.get("status") == "passed"
        and EXPECTED_VERUS_SUMMARY in verification_stdout
        and negative_verus["exit_code"] != 0
        and (
            not require_review
            or (
                "**VERDICT: ACCEPT**" in review_text
                and model.TARGET in review_text
            )
        )
        and model.SOURCE_MODEL_COMPLETE
        and not model.MISSING_SOURCE_PHASES
    )
    if not complete:
        raise RuntimeError(
            "target-079 classification prerequisites are incomplete"
        )
    return dict(EXPECTED_STATUSES)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pre-review",
        action="store_true",
        help="run the complete engineer gate before independent acceptance",
    )
    args = parser.parse_args()
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for target-079 evidence")
    if not SOURCE_PROOF.is_file():
        raise RuntimeError(f"Verus proof is missing: {SOURCE_PROOF}")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if not args.pre_review and not REVIEW_ADDENDUM.is_file():
        raise RuntimeError(
            f"independent review addendum is missing: {REVIEW_ADDENDUM}"
        )
    review_text = (
        REVIEW_ADDENDUM.read_text()
        if REVIEW_ADDENDUM.is_file()
        else ""
    )

    csv_before, json_before = _load_ledger()
    baseline_row = _target_row(json_before, model.INPUT_ORDER)
    baseline = {
        field: baseline_row[field]
        for field in target_pipeline.RESULT_FIELDS
    }
    if baseline != BASELINE_STATUSES:
        raise RuntimeError(f"target-079 baseline changed: {baseline!r}")

    protected_trees = {
        "certified_target_078": BASELINE_078_ROOT,
        "baseline_target_079": BASELINE_079_ROOT,
        "accepted_target_078_operational_v1": ACCEPTED_078_ROOT,
        "frozen_target_078": FROZEN_078_ROOT,
        "frozen_target_079": FROZEN_079_ROOT,
        "campaign_reviews": common.OUT / "review",
    }
    protected_files = {
        "pipeline_state": PIPELINE_STATE,
        "ground_truth": GROUND_TRUTH,
        "ledger_csv": LEDGER_CSV,
        "ledger_json": LEDGER_JSON,
        "target_078_addendum_csv": (
            common.OUT / "crosswalk/target_078_operational_v1_addendum.csv"
        ),
        "target_078_addendum_json": (
            common.OUT / "crosswalk/target_078_operational_v1_addendum.json"
        ),
    }
    tree_before = {
        name: protected_tree_digest(name, path)
        for name, path in protected_trees.items()
    }
    if (
        tree_before["campaign_reviews"]
        != EXPECTED_CAMPAIGN_REVIEWS_SHA256
    ):
        raise RuntimeError("accepted pre-operational-v2 review set drifted")
    file_before = {
        name: file_digest(path) for name, path in protected_files.items()
    }

    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    _clean_generated_probe_artifacts()
    ground_replay = target_pipeline.capture_command(
        EVIDENCE_ROOT / "ground_truth_replay",
        [
            sys.executable,
            str(common.OUT / "tools/run_target_079_ground_truth.py"),
        ],
        cwd=common.OUT,
    )
    target_pipeline.require_clean_result(
        ground_replay,
        "captured target-079 adapter ground truth: 10 scenarios",
        label="ground-truth-replay",
    )
    ground_manifest = json.loads(
        (EVIDENCE_ROOT / "ground_truth/manifest.json").read_text()
    )
    for scenario, record in ground_manifest["scenarios"].items():
        expected_command = (
            "python3 tools/run_target_079_ground_truth.py "
            f"--check-scenario {scenario}"
        )
        if (
            record.get("replay_command") != expected_command
            or (
                EVIDENCE_ROOT
                / "ground_truth"
                / scenario
                / "command.txt"
            ).read_text()
            != expected_command + "\n"
        ):
            raise RuntimeError(f"{scenario}: replay command is not durable")

    source_manifest = _materialize_source_bindings()
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
    regression_texts = {
        smt.LENGTH_17_CORRESPONDENCE: (
            smt.length_17_correspondence_text()
        ),
        **{
            kind: smt.exact_cleanup_regression_text(kind)
            for kind in smt.EXACT_CLEANUP_REGRESSIONS
        },
    }
    for label, text in regression_texts.items():
        path = EVIDENCE_ROOT / f"regression_{label}.smt2"
        path.write_text(text)
        regressions[label] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _solver_capture(
                z3, f"regression_{label}", path, "unsat"
            ),
        }

    selection_probes: dict[str, Any] = {}
    for kind in smt.SELECTION_PROBE_KINDS:
        path = EVIDENCE_ROOT / f"probe_selection_{kind}.smt2"
        path.write_text(smt.selection_probe_text(kind))
        selection_probes[kind] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _solver_capture(
                z3, f"probe_selection_{kind}", path, "sat"
            ),
        }

    adapter_probes: dict[str, Any] = {}
    for kind in smt.ADAPTER_PROBE_KINDS:
        path = EVIDENCE_ROOT / f"probe_adapter_{kind}.smt2"
        path.write_text(smt.adapter_probe_text(kind))
        adapter_probes[kind] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _solver_capture(
                z3, f"probe_adapter_{kind}", path, "sat"
            ),
        }

    selection_mutations: dict[str, Any] = {}
    for kind in smt.SELECTION_MUTATION_PROBES:
        path = EVIDENCE_ROOT / f"mutation_selection_{kind}.smt2"
        path.write_text(smt.selection_mutation_probe_text(kind))
        selection_mutations[kind] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _solver_capture(
                z3, f"mutation_selection_{kind}", path, "unsat"
            ),
        }

    adapter_mutations: dict[str, Any] = {}
    for kind in smt.ADAPTER_MUTATION_PROBES:
        path = EVIDENCE_ROOT / f"mutation_adapter_{kind}.smt2"
        path.write_text(smt.adapter_mutation_probe_text(kind))
        adapter_mutations[kind] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _solver_capture(
                z3, f"mutation_adapter_{kind}", path, "unsat"
            ),
        }

    witness_path = EVIDENCE_ROOT / "witness.json"
    common.write_json(witness_path, witnesses.witness_payload())
    witness_replay = target_pipeline.capture_command(
        EVIDENCE_ROOT / "witness_replay",
        [
            sys.executable,
            str(
                common.OUT
                / "tools/replay_target_079_operational_v1.py"
            ),
            "--witness",
            str(witness_path),
        ],
        cwd=common.OUT,
    )
    replay_stdout = (common.OUT / witness_replay["stdout"]).read_text()
    replay_stderr = (common.OUT / witness_replay["stderr"]).read_text()
    if witness_replay["exit_code"] != 0 or replay_stderr:
        raise RuntimeError("target-079 witness replay failed")
    replay_result = json.loads(replay_stdout)
    if replay_result.get("status") != "passed":
        raise RuntimeError("target-079 witness did not pass")
    witness_replay["result"] = replay_result

    captured_proof = EVIDENCE_ROOT / "verus/selection_model.rs"
    captured_proof.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_PROOF, captured_proof)
    proof_text = captured_proof.read_text()
    for forbidden in ("external_body", "assume(", "admit(", "axiom"):
        if forbidden in proof_text:
            raise RuntimeError(
                f"target-079 Verus proof contains {forbidden!r}"
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
        raise RuntimeError("target-079 Verus proof did not type-check")
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
        raise RuntimeError("target-079 Verus proof did not verify")

    mutated_proof = (
        EVIDENCE_ROOT / "verus/sequence_projection_mutation.rs"
    )
    mutation_anchor = "sequence: source.state.sequence,"
    if proof_text.count(mutation_anchor) != 1:
        raise RuntimeError("Verus sequence projection anchor changed")
    mutated_proof.write_text(
        proof_text.replace(
            mutation_anchor, "sequence: Seq::empty(),", 1
        )
    )
    negative_verus = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/sequence_projection_mutation",
        [str(common.VERUS), str(mutated_proof), "--crate-type=lib"],
        cwd=common.OUT,
    )
    if negative_verus["exit_code"] == 0:
        raise RuntimeError("Verus sequence projection mutation verified")

    classification = _derive_classification(
        obligations=obligations,
        nonvacuity=nonvacuity,
        selection_probes=selection_probes,
        adapter_probes=adapter_probes,
        selection_mutations=selection_mutations,
        adapter_mutations=adapter_mutations,
        regressions=regressions,
        ground_manifest=ground_manifest,
        replay_result=replay_result,
        verification_stdout=verification_stdout,
        negative_verus=negative_verus,
        review_text=review_text,
        require_review=not args.pre_review,
    )
    addendum_json, addendum_csv = _write_crosswalk_addendum(
        classification
    )

    csv_after, json_after = _load_ledger()
    tree_after = {
        name: protected_tree_digest(name, path)
        for name, path in protected_trees.items()
    }
    file_after = {
        name: file_digest(path) for name, path in protected_files.items()
    }
    if csv_after != csv_before or json_after != json_before:
        raise RuntimeError("additive runner mutated certified crosswalk")
    if tree_after != tree_before:
        raise RuntimeError("additive runner mutated protected evidence")
    if file_after != file_before:
        raise RuntimeError("additive runner mutated protected files")

    result = {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "artifact_id": "target_079_operational_v1",
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "active_contract_text": source_manifest["active_contract"][
            "contract_text"
        ],
        "classification": classification,
        "classification_scope": (
            "additive target-079 operational-v1 crosswalk addendum; "
            "certified campaign state and target-078 remain byte-identical"
        ),
        "classification_basis": (
            "Both arbitrary-domain literal six-conjunct obligations are "
            "clean UNSAT under one total state-dependent key/Ord/Drop "
            "boundary. Distinct owned K identities drive reverse cleanup. "
            "The imported accepted ExactRunState composes normal return and "
            "ordinary unwind restoration, while a separate abort bit "
            "preserves interrupted state without CopyOnDrop or gap cleanup."
        ),
        "source_model_complete": True,
        "classification_eligible": True,
        "unresolved_source_model_phases": [],
        "source_bindings": target_pipeline.artifact_record(
            SOURCE_BINDINGS
        ),
        "boundary_manifest": target_pipeline.artifact_record(
            boundary_path
        ),
        "ground_truth": {
            "manifest": target_pipeline.artifact_record(
                EVIDENCE_ROOT / "ground_truth/manifest.json"
            ),
            "replay": ground_replay,
            "scenario_count": 10,
        },
        "obligations": obligations,
        "nonvacuity": nonvacuity,
        "semantic_force_probes": {
            "selection_phase_end_to_end": selection_probes,
            "adapter": adapter_probes,
        },
        "semantic_mutation_regressions": {
            "selection_phase_end_to_end": selection_mutations,
            "adapter": adapter_mutations,
        },
        "regressions": regressions,
        "witness": target_pipeline.artifact_record(witness_path),
        "witness_replay": witness_replay,
        "verus": {
            "source_model": target_pipeline.artifact_record(SOURCE_PROOF),
            "captured_model": target_pipeline.artifact_record(
                captured_proof
            ),
            "typecheck": typecheck,
            "verification": verification,
            "expected_summary": EXPECTED_VERUS_SUMMARY,
            "negative_sequence_projection_mutation": negative_verus,
            "trusted_free": True,
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
            "baseline_target_079_row_unchanged": True,
            "accepted_target_078_unchanged": True,
            "pipeline_state_unchanged": True,
            "campaign_reviews_unchanged": True,
        },
        "independent_review": (
            {
                "status": "accepted",
                "verdict": "ACCEPT",
                "addendum": target_pipeline.artifact_record(
                    REVIEW_ADDENDUM
                ),
            }
            if not args.pre_review
            else {
                "status": "pending",
                "verdict": None,
                "addendum": (
                    target_pipeline.artifact_record(REVIEW_ADDENDUM)
                    if REVIEW_ADDENDUM.is_file()
                    else None
                ),
            }
        ),
        "stage_transition": "disabled",
    }
    common.write_json(EVIDENCE_ROOT / "result.json", result)

    print("target_079_operational_v1=PASS")
    print("exact_principal_return=unsat")
    print("completeness_modulo_exact_equivalence=unsat")
    print(
        "selection_force_probes="
        f"{len(selection_probes)}_sat"
    )
    print(f"adapter_force_probes={len(adapter_probes)}_sat")
    print(
        "selection_mutations="
        f"{len(selection_mutations)}_unsat"
    )
    print(f"adapter_mutations={len(adapter_mutations)}_unsat")
    print("ground_truth=10_scenarios")
    print("witness_replay=passed")
    print("verus=7_verified_0_errors")
    print("baseline_target_079=preserved")
    print("accepted_target_078=preserved")
    print("pipeline_state=preserved")
    print("crosswalk=additive_only")
    print(
        "independent_review="
        + ("pending" if args.pre_review else "accepted")
    )


if __name__ == "__main__":
    main()
