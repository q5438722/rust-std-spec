#!/usr/bin/env python3
"""Build the additive target-079 insert_tail/CopyOnDrop v3 package."""

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
import preservation_policy_v2
import target_079_insert_tail_refinement_v3 as model
import target_pipeline


ROOT = common.OUT
EVIDENCE = ROOT / "evidence/target_079_insert_tail_refinement_v3"
ACCEPTED_EVIDENCE = ROOT / "evidence/target_079_operational_v1"
POLICY_V3 = ROOT / "preservation/path_policy_v3.json"
EXPECTED_CLASSIFICATION = {
    "exact_output_determinism_status": "conditional-complete",
    "completeness_modulo_reviewed_equivalence_status": (
        "conditional-complete"
    ),
}
EXPECTED_VERUS_SUMMARY = "verification results:: 15 verified, 0 errors"

PROTECTED_TREES = {
    "target_078_operational_v1": (
        ROOT / "evidence/target_078_operational_v1"
    ),
    "target_078_adapter_refinement_v2": (
        ROOT / "evidence/target_078_adapter_refinement_v2"
    ),
    "target_078_insert_tail_refinement_v3": (
        ROOT / "evidence/target_078_insert_tail_refinement_v3"
    ),
    "target_079_operational_v1": ACCEPTED_EVIDENCE,
    "target_079_adapter_refinement_v2": (
        ROOT / "evidence/target_079_adapter_refinement_v2"
    ),
    "final_campaign": ROOT / "evidence/final_campaign",
    "frozen_authorities": ROOT / "provenance/frozen",
}
PROTECTED_FILES = {
    "target_079_operational_v1_proof": (
        ROOT
        / "proofs/079_core_slice_select_nth_unstable_by_key_operational_v1.rs"
    ),
    "target_079_adapter_refinement_v2_proof": (
        ROOT
        / "proofs/"
        "079_core_slice_select_nth_unstable_by_key_adapter_refinement_v2.rs"
    ),
    "target_079_adapter_refinement_v2_model": (
        ROOT / "tools/target_079_adapter_refinement_v2.py"
    ),
    "target_079_exact_smt_v1": ROOT / "tools/target_079_exact_smt_v1.py",
    "target_079_operational_smt_v1": (
        ROOT / "tools/target_079_operational_smt_v1.py"
    ),
    "target_079_operational_v1_review": (
        ROOT / "review/REVIEW_ADDENDUM_TARGET_079_OPERATIONAL_V1.md"
    ),
    "target_078_insert_tail_refinement_v3_proof": (
        ROOT
        / "proofs/"
        "078_core_slice_select_nth_unstable_by_insert_tail_refinement_v3.rs"
    ),
    "target_078_insert_tail_refinement_v3_model": (
        ROOT / "tools/target_078_insert_tail_refinement_v3.py"
    ),
    "path_policy_v1": ROOT / "preservation/path_policy_v1.json",
    "path_policy_v2": ROOT / "preservation/path_policy_v2.json",
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


def _validate_preservation_policy(
    *,
    require_registration: bool,
) -> str:
    if not POLICY_V3.is_file():
        preservation_policy_v2.validate_policy()
        if require_registration:
            raise RuntimeError("target-079 v3 preservation policy is missing")
        return "v2-parent"
    policy_v3 = importlib.import_module("preservation_policy_v3")
    if require_registration:
        policy_v3.validate_policy()
        return "v3"
    policy_v3.validate_parent_binding()
    return "v3-parent"


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
        raise RuntimeError("z3 is required for target-079 v3")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")

    _validate_preservation_policy(require_registration=False)
    protected_trees_before = {
        name: _tree_digest(path)
        for name, path in PROTECTED_TREES.items()
    }
    protected_files_before = {
        name: _file_digest(path)
        for name, path in PROTECTED_FILES.items()
    }

    proof_text = model.PROOF_PATH.read_text()
    proof_binding = model.validate_proof(proof_text)
    exact_binding = model.accepted_smt_binding()
    adapter_binding = model.accepted_adapter_binding()
    adapter_coverage = model.adapter_correspondence_coverage()
    insert_coverage = model.correspondence_coverage()
    accepted_result = json.loads(model.ACCEPTED_RESULT_PATH.read_text())
    if accepted_result.get("classification") != EXPECTED_CLASSIFICATION:
        raise RuntimeError("accepted target-079 classification changed")

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
        raise RuntimeError("target-079 v3 Verus model did not type-check")

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
        raise RuntimeError("target-079 v3 Verus verification failed")

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
            [
                str(common.VERUS),
                str(mutation_source),
                "--crate-type=lib",
                "--num-threads",
                "1",
            ],
        )
        verification_rejected = mutation_verification["exit_code"] != 0
        mutation_stdout = (
            ROOT / mutation_verification["stdout"]
        ).read_text()
        mutation_stderr = (
            ROOT / mutation_verification["stderr"]
        ).read_text()
        mutation_summary = re.search(
            r"verification results:: ([0-9]+) verified, ([0-9]+) errors",
            mutation_stdout,
        )
        if mutation_verification["exit_code"] == 124:
            raise RuntimeError(f"{kind}: mutation verification timed out")
        if kind in model.VERUS_INSENSITIVE_MUTATIONS:
            if (
                verification_rejected
                or mutation_stderr
                or EXPECTED_VERUS_SUMMARY not in mutation_stdout
            ):
                raise RuntimeError(
                    f"{kind}: expected correspondence-only sensitivity"
                )
        elif (
            not verification_rejected
            or not mutation_stderr
            or mutation_summary is None
            or int(mutation_summary.group(2)) <= 0
        ):
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
        mutations[kind] = {
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
                else "verus-insensitive-and-correspondence-sat"
            ),
            "insensitivity_reason": (
                model.VERUS_INSENSITIVITY_REASON
                if kind in model.VERUS_INSENSITIVE_MUTATIONS
                else None
            ),
        }

    rejected_count = sum(
        record["verification_rejected"] for record in mutations.values()
    )
    insensitive_count = len(mutations) - rejected_count
    if (
        rejected_count
        != len(model.MUTATION_KINDS)
        - len(model.VERUS_INSENSITIVE_MUTATIONS)
        or insensitive_count != len(model.VERUS_INSENSITIVE_MUTATIONS)
    ):
        raise RuntimeError("target-079 mutation sensitivity split changed")

    adapter_text = model.adapter_correspondence_query_text(proof_text)
    model.validate_adapter_correspondence_query(adapter_text)
    adapter_path = EVIDENCE / "adapter_correspondence.smt2"
    adapter_path.write_text(adapter_text)
    adapter_solver = _capture(
        EVIDENCE / "adapter_correspondence",
        [z3, "-smt2", str(adapter_path)],
    )
    _require_exact_solver_result(
        adapter_solver,
        "unsat",
        "adapter-correspondence",
    )

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

    expected_witness_details = {
        "no-shift": {
            "shift_count": 0,
            "panicked": False,
            "aborted": False,
        },
        "multi-shift": {
            "shift_count": 2,
            "panicked": False,
            "aborted": False,
        },
        "ordinary-panic-after-shift": {
            "shift_count_before_panic": 1,
            "panicked": True,
            "aborted": False,
            "retained_callback_state": 7,
            "active_gap_restored": True,
        },
        "abort-after-shift": {
            "shift_count_before_abort": 1,
            "panicked": True,
            "aborted": True,
            "cleanup_bypassed": True,
            "interrupted_sequence_preserved": True,
        },
    }
    witnesses: dict[str, Any] = {}
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
        for name, path in PROTECTED_FILES.items()
    }
    if protected_trees_after != protected_trees_before:
        raise RuntimeError("target-079 v3 mutated a protected tree")
    if protected_files_after != protected_files_before:
        raise RuntimeError("target-079 v3 mutated a protected file")

    result = {
        "schema_version": 1,
        "artifact_id": "target_079_insert_tail_refinement_v3",
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "status": "engineer-complete-review-pending",
        "classification": EXPECTED_CLASSIFICATION,
        "classification_changed": False,
        "classification_basis": (
            "accepted target-079 operational-v1 obligations replay "
            "unchanged; this package adds trusted-free adapter, "
            "insert_tail, and CopyOnDrop refinement"
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
        "mutation_summary": {
            "total": len(mutations),
            "verus_rejected_count": rejected_count,
            "verus_insensitive_count": insensitive_count,
            "verus_insensitive_mutations": sorted(
                model.VERUS_INSENSITIVE_MUTATIONS
            ),
            "verus_insensitivity_reason": (
                model.VERUS_INSENSITIVITY_REASON
            ),
        },
        "adapter_correspondence": {
            "query": _artifact(adapter_path),
            "solver": adapter_solver,
            "solver_result": "unsat",
            "derivation": "parsed-verus-expression-ast-to-smt",
            "compared_functions": adapter_coverage[
                "semantic_functions"
            ],
            "compared_fields": adapter_coverage["adapter_fields"],
            "comparison_count": adapter_coverage["comparison_count"],
            "accepted_smt": adapter_binding,
        },
        "insert_tail_correspondence": {
            "query": _artifact(correspondence_path),
            "solver": correspondence_solver,
            "solver_result": "unsat",
            "derivation": "parsed-verus-expression-ast-to-smt",
            "proof_rule": insert_coverage["proof_rule"],
            "valid_domains": insert_coverage["valid_domains"],
            "compared_functions": insert_coverage["semantic_functions"],
            "compared_state_fields": insert_coverage["state_fields"],
            "bound_boundary_fields": insert_coverage["boundary_fields"],
            "comparison_count": insert_coverage["comparison_count"],
            "accepted_smt": exact_binding,
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
            "insert_tail_refinement_v3_analogue_unchanged": True,
            "frozen_authorities_unchanged": True,
            "final_campaign_unchanged": True,
            "pipeline_state_unchanged": True,
        },
        "preservation_policy": {
            "required_version": "slice-preservation-path-policy-v3",
            "path_policy_v1_unchanged": True,
            "path_policy_v2_unchanged": True,
            "additive_registration": (
                "target_079_insert_tail_refinement_v3"
            ),
            "additive_review_registration": (
                "target_079_insert_tail_refinement_v3_review"
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

    print("target_079_insert_tail_refinement_v3=PASS")
    print("verus=15_verified_0_errors")
    print("adapter_correspondence=unsat")
    print("insert_tail_correspondence=unsat")
    print(f"witnesses={len(witnesses)}_sat_models")
    print(
        f"mutations={rejected_count}_verus_rejected_"
        f"{insensitive_count}_correspondence_only"
    )
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
            "usage: run_target_079_insert_tail_refinement_v3.py "
            "[--allow-unregistered-evidence]"
        )
