#!/usr/bin/env python3
"""Build the additive target-078 insert_tail/CopyOnDrop v3 package."""

from __future__ import annotations

import importlib
import json
import re
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import preservation_policy_v1
import preservation_policy_v3 as preservation_policy
import target_078_insert_tail_refinement_v3 as model
import target_pipeline


ROOT = common.OUT
EVIDENCE = ROOT / "evidence/target_078_insert_tail_refinement_v3"
ACCEPTED_EVIDENCE = ROOT / "evidence/target_078_operational_v1"
POLICY_V2 = ROOT / "preservation/path_policy_v2.json"
POLICY_V3 = ROOT / "preservation/path_policy_v3.json"
EXPECTED_CLASSIFICATION = {
    "exact_output_determinism_status": "conditional-complete",
    "completeness_modulo_reviewed_equivalence_status": (
        "conditional-complete"
    ),
}
EXPECTED_VERUS_SUMMARY = "verification results:: 14 verified, 0 errors"

PROTECTED_TREES = {
    "target_078_operational_v1": ACCEPTED_EVIDENCE,
    "target_078_adapter_refinement_v2": (
        ROOT / "evidence/target_078_adapter_refinement_v2"
    ),
    "target_079_operational_v1": (
        ROOT / "evidence/target_079_operational_v1"
    ),
    "target_079_adapter_refinement_v2": (
        ROOT / "evidence/target_079_adapter_refinement_v2"
    ),
    "final_campaign": ROOT / "evidence/final_campaign",
    "frozen_authorities": ROOT / "provenance/frozen",
}
PROTECTED_FILES = {
    "target_078_operational_v1_proof": (
        ROOT
        / "proofs/078_core_slice_select_nth_unstable_by_operational_v1.rs"
    ),
    "target_078_adapter_refinement_v2_proof": (
        ROOT
        / "proofs/"
        "078_core_slice_select_nth_unstable_by_adapter_refinement_v2.rs"
    ),
    "target_078_exact_smt_v1": (
        ROOT / "tools/target_078_exact_smt_v1.py"
    ),
    "target_078_operational_smt_v1": (
        ROOT / "tools/target_078_operational_smt_v1.py"
    ),
    "target_078_operational_v1_review": (
        ROOT / "review/REVIEW_ADDENDUM_TARGET_078_OPERATIONAL_V1.md"
    ),
    "path_policy_v1": ROOT / "preservation/path_policy_v1.json",
    "pipeline_state": ROOT / "research/PIPELINE_STATE.json",
}


def _tree_digest(root: Path) -> str:
    if not root.is_dir():
        raise RuntimeError(f"protected tree is missing: {root}")
    digest = sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _file_digest(path: Path) -> str:
    if not path.is_file():
        raise RuntimeError(f"protected file is missing: {path}")
    return sha256(path.read_bytes()).hexdigest()


def _protected_file_set() -> dict[str, Path]:
    return dict(PROTECTED_FILES)


def _validate_preservation_policy(
    *,
    require_registration: bool,
) -> str:
    if POLICY_V3.is_file():
        if require_registration:
            preservation_policy.validate_policy()
            return "v2"
        preservation_policy.validate_parent_binding(
            validate_parent_addition=False
        )
        return "v2-parent"
    if not POLICY_V2.is_file():
        preservation_policy_v1.validate_policy()
        if require_registration:
            raise RuntimeError("target-078 v3 preservation policy is missing")
        return "v1-parent"
    policy_v2 = importlib.import_module("preservation_policy_v2")
    if require_registration:
        policy_v2.validate_policy()
        return "v2"
    policy_v2.validate_parent_binding()
    return "v2-parent"


def _capture(
    destination: Path,
    argv: list[str],
    *,
    timeout: int = 300,
) -> dict[str, Any]:
    return target_pipeline.capture_command(
        destination,
        argv,
        cwd=ROOT,
        timeout=timeout,
    )


def _artifact(path: Path) -> dict[str, Any]:
    return target_pipeline.artifact_record(path)


def _require_exact_solver_result(
    record: dict[str, Any],
    expected: str,
    label: str,
    *,
    model_required: bool = False,
) -> str:
    stdout = (ROOT / record["stdout"]).read_text()
    stderr = (ROOT / record["stderr"]).read_text()
    first_line, separator, remainder = stdout.partition("\n")
    if (
        record["exit_code"] != 0
        or first_line != expected
        or not separator
        or stderr
        or (model_required and not remainder.strip())
        or (not model_required and remainder)
    ):
        raise RuntimeError(
            f"{label}: expected clean {expected}, got "
            f"exit={record['exit_code']} stdout={stdout!r} "
            f"stderr={stderr!r}"
        )
    record["expected_solver_result"] = expected
    record["solver_result"] = expected
    return remainder


def _reset_evidence() -> None:
    if EVIDENCE.exists():
        shutil.rmtree(EVIDENCE)
    EVIDENCE.mkdir(parents=True)


def main(*, allow_unregistered_evidence: bool = False) -> None:
    z3 = shutil.which("z3")
    if z3 is None:
        raise RuntimeError("z3 is required for target-078 v3")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")

    _validate_preservation_policy(require_registration=False)
    protected_files = _protected_file_set()
    protected_trees_before = {
        name: _tree_digest(path)
        for name, path in PROTECTED_TREES.items()
    }
    protected_files_before = {
        name: _file_digest(path)
        for name, path in protected_files.items()
    }

    proof_text = model.PROOF_PATH.read_text()
    proof_binding = model.validate_proof(proof_text)
    smt_binding = model.accepted_smt_binding()
    coverage = model.correspondence_coverage()
    accepted_result = json.loads(model.ACCEPTED_RESULT_PATH.read_text())
    if accepted_result.get("classification") != EXPECTED_CLASSIFICATION:
        raise RuntimeError("accepted target-078 classification changed")

    _reset_evidence()
    verus_root = EVIDENCE / "verus"
    mutation_root = EVIDENCE / "mutations"
    witness_root = EVIDENCE / "witnesses"
    replay_root = EVIDENCE / "classification_replay"

    captured_proof = verus_root / "insert_tail_model.rs"
    captured_proof.parent.mkdir(parents=True)
    shutil.copyfile(model.PROOF_PATH, captured_proof)
    typecheck = _capture(
        verus_root / "typecheck",
        [
            str(common.VERUS),
            str(captured_proof),
            "--crate-type=lib",
            "--no-verify",
        ],
    )
    if (
        typecheck["exit_code"] != 0
        or (ROOT / typecheck["stderr"]).read_text()
    ):
        raise RuntimeError("target-078 v3 Verus model did not type-check")

    verification = _capture(
        verus_root / "verification",
        [str(common.VERUS), str(captured_proof), "--crate-type=lib"],
    )
    verification_stdout = (ROOT / verification["stdout"]).read_text()
    verification_stderr = (ROOT / verification["stderr"]).read_text()
    match = re.search(
        r"verification results:: ([0-9]+) verified, ([0-9]+) errors",
        verification_stdout,
    )
    if (
        verification["exit_code"] != 0
        or verification_stderr
        or match is None
        or int(match.group(1)) <= 0
        or int(match.group(2)) != 0
        or EXPECTED_VERUS_SUMMARY not in verification_stdout
    ):
        raise RuntimeError("target-078 v3 Verus verification failed")

    mutations: dict[str, Any] = {}
    for kind in model.MUTATION_KINDS:
        mutation_dir = mutation_root / kind
        mutation_dir.mkdir(parents=True)
        mutation_source = mutation_dir / "insert_tail_model.rs"
        mutated_text = model.mutate_proof(kind, proof_text)
        mutation_source.write_text(mutated_text)
        mutation_typecheck = _capture(
            mutation_dir / "typecheck",
            [
                str(common.VERUS),
                str(mutation_source),
                "--crate-type=lib",
                "--no-verify",
            ],
        )
        if (
            mutation_typecheck["exit_code"] != 0
            or (ROOT / mutation_typecheck["stderr"]).read_text()
        ):
            raise RuntimeError(f"{kind}: mutation did not type-check")
        mutation_verification = _capture(
            mutation_dir / "verification",
            [str(common.VERUS), str(mutation_source), "--crate-type=lib"],
        )
        verification_rejected = mutation_verification["exit_code"] != 0
        if not verification_rejected:
            raise RuntimeError(
                f"{kind}: mutation unexpectedly passed Verus verification"
            )
        query_text = model.correspondence_query_text(mutated_text)
        model.validate_correspondence_query(query_text)
        query_path = mutation_dir / "correspondence.smt2"
        query_path.write_text(query_text)
        solver = _capture(
            mutation_dir / "correspondence",
            [z3, "-smt2", str(query_path)],
        )
        _require_exact_solver_result(
            solver, "sat", f"{kind}-correspondence"
        )
        record: dict[str, Any] = {
            "source": _artifact(mutation_source),
            "typecheck": mutation_typecheck,
            "verification": mutation_verification,
            "query": _artifact(query_path),
            "solver": solver,
            "typecheck_passed": True,
            "verification_rejected": verification_rejected,
            "correspondence_result": "sat",
            "sensitivity_result": (
                "verus-rejected-and-correspondence-sat"
                if verification_rejected
                else "correspondence-sat"
            ),
        }
        mutations[kind] = record

    correspondence_text = model.correspondence_query_text(proof_text)
    model.validate_correspondence_query(correspondence_text)
    correspondence_path = EVIDENCE / "insert_tail_correspondence.smt2"
    correspondence_path.write_text(correspondence_text)
    correspondence_solver = _capture(
        EVIDENCE / "insert_tail_correspondence",
        [z3, "-smt2", str(correspondence_path)],
    )
    _require_exact_solver_result(
        correspondence_solver,
        "unsat",
        "insert-tail-correspondence",
    )

    witnesses: dict[str, Any] = {}
    expected_witness_details = {
        "no-shift": {
            "shift_count": 0,
            "panicked": False,
        },
        "multi-shift": {
            "shift_count": 2,
            "panicked": False,
        },
        "insert-at-begin": {
            "shift_count": 2,
            "reached_begin": True,
            "panicked": False,
        },
        "panic-after-shift": {
            "shift_count_before_panic": 1,
            "panicked": True,
            "retained_callback_state": 7,
        },
    }
    for kind in model.WITNESS_KINDS:
        witness_dir = witness_root / kind
        witness_dir.mkdir(parents=True)
        query_text = model.witness_query_text(kind, proof_text)
        model.validate_witness_query(kind, query_text)
        query_path = witness_dir / "witness.smt2"
        query_path.write_text(query_text)
        solver = _capture(
            witness_dir / "solver",
            [z3, "-smt2", str(query_path)],
        )
        model_text = _require_exact_solver_result(
            solver,
            "sat",
            f"{kind}-witness",
            model_required=True,
        )
        model_path = witness_dir / "model.txt"
        model_path.write_text(model_text)
        witnesses[kind] = {
            "query": _artifact(query_path),
            "solver": solver,
            "model": _artifact(model_path),
            "solver_result": "sat",
            **expected_witness_details[kind],
        }

    classification_inputs = {
        "exact_output": (
            ACCEPTED_EVIDENCE / "exact_output_obligation.smt2",
            "unsat",
        ),
        "full_state": (
            ACCEPTED_EVIDENCE / "obligation.smt2",
            "unsat",
        ),
        "nonvacuity": (
            ACCEPTED_EVIDENCE / "nonvacuity.smt2",
            "sat",
        ),
    }
    classification_replay: dict[str, Any] = {}
    for name, (source, expected) in classification_inputs.items():
        copied = replay_root / f"{name}.smt2"
        copied.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, copied)
        if _file_digest(copied) != _file_digest(source):
            raise RuntimeError(f"{name}: retained SMT copy changed")
        solver = _capture(
            replay_root / name,
            [z3, "-smt2", str(copied)],
        )
        _require_exact_solver_result(solver, expected, name)
        classification_replay[name] = {
            "accepted_source": _artifact(source),
            "retained_copy": _artifact(copied),
            "solver": solver,
        }

    binding_path = EVIDENCE / "correspondence_manifest.json"
    common.write_json(binding_path, model.binding_manifest())
    boundary_path = EVIDENCE / "boundary_manifest.json"
    common.write_json(boundary_path, model.boundary_manifest())

    protected_trees_after = {
        name: _tree_digest(path)
        for name, path in PROTECTED_TREES.items()
    }
    protected_files_after = {
        name: _file_digest(path)
        for name, path in protected_files.items()
    }
    if protected_trees_after != protected_trees_before:
        raise RuntimeError("target-078 v3 mutated a protected tree")
    if protected_files_after != protected_files_before:
        raise RuntimeError("target-078 v3 mutated a protected file")

    result = {
        "schema_version": 1,
        "artifact_id": "target_078_insert_tail_refinement_v3",
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "status": "engineer-complete-review-pending",
        "classification": EXPECTED_CLASSIFICATION,
        "classification_changed": False,
        "classification_basis": (
            "accepted operational-v1 obligations replay unchanged; this "
            "package adds trusted-free insert_tail/CopyOnDrop refinement"
        ),
        "verus": {
            "source": _artifact(model.PROOF_PATH),
            "captured_source": _artifact(captured_proof),
            "typecheck": typecheck,
            "verification": verification,
            "verified_obligations": int(match.group(1)),
            "expected_summary": EXPECTED_VERUS_SUMMARY,
            "trusted_free": True,
            "precomputed_terminal_or_answer_input": False,
        },
        "mutation_matrix": mutations,
        "insert_tail_correspondence": {
            "query": _artifact(correspondence_path),
            "solver": correspondence_solver,
            "solver_result": "unsat",
            "derivation": "parsed-verus-expression-ast-to-smt",
            "proof_rule": coverage["proof_rule"],
            "valid_domains": coverage["valid_domains"],
            "compared_functions": coverage["semantic_functions"],
            "compared_state_fields": coverage["state_fields"],
            "bound_boundary_fields": coverage["boundary_fields"],
            "comparison_count": coverage["comparison_count"],
            "accepted_smt": smt_binding,
            "verus_binding": proof_binding,
        },
        "nonvacuity_witnesses": witnesses,
        "classification_replay": classification_replay,
        "correspondence_manifest": _artifact(binding_path),
        "boundary_manifest": _artifact(boundary_path),
        "preservation": {
            "protected_trees": {
                name: {
                    "before_sha256": protected_trees_before[name],
                    "after_sha256": protected_trees_after[name],
                }
                for name in protected_trees_before
            },
            "protected_files": {
                name: {
                    "before_sha256": protected_files_before[name],
                    "after_sha256": protected_files_after[name],
                }
                for name in protected_files_before
            },
            "accepted_target_078_unchanged": True,
            "accepted_target_079_unchanged": True,
            "adapter_refinement_v2_unchanged": True,
            "operational_v2_unchanged": True,
            "frozen_authorities_unchanged": True,
            "final_campaign_unchanged": True,
            "pipeline_state_unchanged": True,
        },
        "preservation_policy": {
            "required_version": "slice-preservation-path-policy-v2",
            "path_policy_v1_unchanged": True,
            "additive_registration": (
                "target_078_insert_tail_refinement_v3"
            ),
            "additive_review_registration": (
                "target_078_insert_tail_refinement_v3_review"
            ),
        },
        "independent_review": {
            "required": True,
            "status": "pending",
            "verdict": None,
        },
        "stage_transition": "disabled",
    }
    common.write_json(EVIDENCE / "result.json", result)

    if allow_unregistered_evidence:
        policy_version_after = "registration-deferred"
    else:
        policy_version_after = _validate_preservation_policy(
            require_registration=True
        )

    print("target_078_insert_tail_refinement_v3=PASS")
    print("verus=14_verified_0_errors")
    print("insert_tail_correspondence=unsat")
    print(f"witnesses={len(witnesses)}_sat_models")
    print(f"mutations={len(mutations)}_sensitive")
    print("exact_output_replay=unsat")
    print("full_state_replay=unsat")
    print("nonvacuity_replay=sat")
    print("protected_artifacts=preserved")
    print("classification=unchanged")
    print(f"preservation_policy={policy_version_after}")
    print("independent_review=pending")


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if arguments == ["--allow-unregistered-evidence"]:
        main(allow_unregistered_evidence=True)
    elif not arguments:
        main()
    else:
        raise SystemExit(
            "usage: run_target_078_insert_tail_refinement_v3.py "
            "[--allow-unregistered-evidence]"
        )
