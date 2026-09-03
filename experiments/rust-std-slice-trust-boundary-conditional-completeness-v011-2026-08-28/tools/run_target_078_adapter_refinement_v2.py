#!/usr/bin/env python3
"""Build the additive target-078 constructive adapter proof package."""

from __future__ import annotations

import json
import re
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import target_078_adapter_refinement_v2 as model
import target_pipeline


ROOT = common.OUT
EVIDENCE = ROOT / "evidence/target_078_adapter_refinement_v2"
ACCEPTED_EVIDENCE = ROOT / "evidence/target_078_operational_v1"
EXPECTED_CLASSIFICATION = {
    "exact_output_determinism_status": "conditional-complete",
    "completeness_modulo_reviewed_equivalence_status": (
        "conditional-complete"
    ),
}
EXPECTED_VERUS_SUMMARY = "verification results:: 11 verified, 0 errors"

PROTECTED_TREES = {
    "target_078_operational_v1": ACCEPTED_EVIDENCE,
    "target_079_operational_v1": (
        ROOT / "evidence/target_079_operational_v1"
    ),
    "target_079_adapter_refinement_v2": (
        ROOT / "evidence/target_079_adapter_refinement_v2"
    ),
    "final_campaign": ROOT / "evidence/final_campaign",
    "parser_repair_certification": (
        ROOT
        / "evidence/final_campaign/operational_v2/"
        "parser_repair_certification_v1"
    ),
    "frozen_authorities": ROOT / "provenance/frozen",
}
EXPECTED_PROTECTED_TREE_DIGESTS = {
    "target_078_operational_v1": (
        "657161a66944847919b917b9f41c99d34f4b2b6d13d35eac853d491ce9ac777d"
    ),
    "target_079_operational_v1": (
        "51340b8bae25814b07866d110a5734d6dae7b68d82e142407f5a31f9f330de8e"
    ),
    "target_079_adapter_refinement_v2": (
        "e899d86f6b95b34c745b8d26508c88a485bcc4ad4a0f58dd0f0fb8c46f7fae9f"
    ),
    "final_campaign": (
        "c67f30407b2a58f4cdf2c3fbbb8cea064e4a48dd28b10a1e94de0d164588a360"
    ),
    "parser_repair_certification": (
        "de295a7e76427cb879963229bbe5f72de721b457a392d6f20a664b2159783911"
    ),
    "frozen_authorities": (
        "0d5d65e518cf382183e5fa472de96a513214d1f3e5233233f221145d7e15e142"
    ),
}
PROTECTED_FILES = {
    "target_078_operational_v1_proof": (
        ROOT
        / "proofs/078_core_slice_select_nth_unstable_by_operational_v1.rs"
    ),
    "target_078_operational_v1_model": (
        ROOT / "tools/target_078_operational_v1.py"
    ),
    "target_078_operational_v1_smt": (
        ROOT / "tools/target_078_operational_smt_v1.py"
    ),
    "target_078_exact_smt_v1": (
        ROOT / "tools/target_078_exact_smt_v1.py"
    ),
    "target_078_operational_v1_runner": (
        ROOT / "tools/run_target_078_operational_v1.py"
    ),
    "target_078_operational_v1_review": (
        ROOT / "review/REVIEW_ADDENDUM_TARGET_078_OPERATIONAL_V1.md"
    ),
    "target_079_adapter_refinement_v2_proof": (
        ROOT
        / "proofs/"
        "079_core_slice_select_nth_unstable_by_key_adapter_refinement_v2.rs"
    ),
    "target_079_adapter_refinement_v2_model": (
        ROOT / "tools/target_079_adapter_refinement_v2.py"
    ),
    "target_079_adapter_refinement_v2_runner": (
        ROOT / "tools/run_target_079_adapter_refinement_v2.py"
    ),
    "target_079_adapter_refinement_v2_review": (
        ROOT / "review/REVIEW_ADDENDUM_TARGET_079_ADAPTER_REFINEMENT_V2.md"
    ),
    "parser_repair_acceptance": (
        ROOT / "review/REVIEW_OPERATIONAL_V2_RECONCILIATION_ACCEPTANCE.md"
    ),
    "pipeline_state": ROOT / "research/PIPELINE_STATE.json",
}
EXPECTED_PROTECTED_FILE_DIGESTS = {
    "target_078_operational_v1_proof": (
        "cf85499e95d1d783ceaf09b6e27a1855e79ba6a040ad76f4759070494c5765e5"
    ),
    "target_078_operational_v1_model": (
        "3686e3e5da098f0660327d64da95a06981a6683fae5907e90046806d5433e6ef"
    ),
    "target_078_operational_v1_smt": (
        "ce89442a40a956e2130f2313a130303228417be54e631a8211910623437ae475"
    ),
    "target_078_exact_smt_v1": (
        "ea6a2e02e75e902b0c8632e0938d1833224ca8fa45ade7697fc9672de1e49fd1"
    ),
    "target_078_operational_v1_runner": (
        "c00b3d00d49ada82f01ff4cebad07123776a836a323de0e377246086d6c7bcfc"
    ),
    "target_078_operational_v1_review": (
        "4838f13fd4258f6f285877ad4f063f8f6b6816620eeec11c6b7c07a21ff7e703"
    ),
    "target_079_adapter_refinement_v2_proof": (
        "850ce906c62eb9a2f57ba7f154e34d4005e81c32608242ac72746f56ed9db022"
    ),
    "target_079_adapter_refinement_v2_model": (
        "f8560b9ee5bf760ee037c102fdbadf525719aff71928a47cbbd0eeb93ff7a442"
    ),
    "target_079_adapter_refinement_v2_runner": (
        "4d1cfe6f202f34d2f932aaa19d1fa116ff6bcc53a85ce68c51ff8730587e628d"
    ),
    "target_079_adapter_refinement_v2_review": (
        "cdbbc53ca4a9230354b36b663cd7c1e7dc3274c6a982bee3fa9c067f06b175b3"
    ),
    "parser_repair_acceptance": (
        "499209677f1fde841309d1b0e42d46450f2510096bd3e5d339417078d2426319"
    ),
    "pipeline_state": (
        "9c38f65e9db80ac5a02dfd8aff19d28f2a14c4608e61dae306268ad7442e9732"
    ),
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


def _require_exact_solver_result(
    record: dict[str, Any],
    expected: str,
    label: str,
) -> None:
    stdout = (ROOT / record["stdout"]).read_text()
    stderr = (ROOT / record["stderr"]).read_text()
    if (
        record["exit_code"] != 0
        or stdout != expected + "\n"
        or stderr != ""
    ):
        raise RuntimeError(
            f"{label}: expected clean {expected}, got "
            f"exit={record['exit_code']} stdout={stdout!r} "
            f"stderr={stderr!r}"
        )
    record["expected_solver_result"] = expected
    record["solver_result"] = expected


def _reset_generated_subtree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def _artifact(path: Path) -> dict[str, Any]:
    return target_pipeline.artifact_record(path)


def main() -> None:
    z3 = shutil.which("z3")
    if z3 is None:
        raise RuntimeError("z3 is required for target-078 v2")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")

    protected_trees_before = {
        name: _tree_digest(path)
        for name, path in PROTECTED_TREES.items()
    }
    protected_files_before = {
        name: _file_digest(path)
        for name, path in PROTECTED_FILES.items()
    }
    if protected_trees_before != EXPECTED_PROTECTED_TREE_DIGESTS:
        raise RuntimeError("protected certification tree baseline changed")
    if protected_files_before != EXPECTED_PROTECTED_FILE_DIGESTS:
        raise RuntimeError("protected certification file baseline changed")

    proof_text = model.PROOF_PATH.read_text()
    proof_binding = model.validate_proof(proof_text)
    smt_binding = model.accepted_smt_binding()
    coverage = model.correspondence_coverage()
    accepted_result = json.loads(model.ACCEPTED_RESULT_PATH.read_text())
    if accepted_result.get("classification") != EXPECTED_CLASSIFICATION:
        raise RuntimeError("accepted target-078 classification changed")

    EVIDENCE.mkdir(parents=True, exist_ok=True)
    verus_root = EVIDENCE / "verus"
    mutation_root = EVIDENCE / "mutations"
    correspondence_mutation_root = (
        EVIDENCE / "correspondence_mutations"
    )
    replay_root = EVIDENCE / "classification_replay"
    _reset_generated_subtree(verus_root)
    _reset_generated_subtree(mutation_root)
    _reset_generated_subtree(correspondence_mutation_root)
    _reset_generated_subtree(replay_root)

    captured_proof = verus_root / "adapter_model.rs"
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
        raise RuntimeError("target-078 v2 Verus model did not type-check")

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
        raise RuntimeError("target-078 v2 Verus verification failed")

    mutations: dict[str, Any] = {}
    for kind in model.MUTATION_KINDS:
        mutation_dir = mutation_root / kind
        mutation_dir.mkdir()
        mutation_source = mutation_dir / "adapter_model.rs"
        mutation_source.write_text(model.mutate_proof(kind, proof_text))
        mutation_typecheck = _capture(
            mutation_dir / "typecheck",
            [
                str(common.VERUS),
                str(mutation_source),
                "--crate-type=lib",
                "--no-verify",
            ],
        )
        mutation_verification = _capture(
            mutation_dir / "verification",
            [str(common.VERUS), str(mutation_source), "--crate-type=lib"],
        )
        if mutation_typecheck["exit_code"] != 0:
            raise RuntimeError(f"{kind}: mutation did not type-check")
        if mutation_verification["exit_code"] == 0:
            raise RuntimeError(f"{kind}: mutation unexpectedly verified")
        mutations[kind] = {
            "source": _artifact(mutation_source),
            "typecheck": mutation_typecheck,
            "verification": mutation_verification,
            "typecheck_passed": True,
            "verification_rejected": True,
        }

    correspondence_text = model.correspondence_query_text(proof_text)
    model.validate_correspondence_query(correspondence_text)
    correspondence_path = EVIDENCE / "adapter_correspondence.smt2"
    correspondence_path.write_text(correspondence_text)
    correspondence_solver = _capture(
        EVIDENCE / "adapter_correspondence",
        [z3, "-smt2", str(correspondence_path)],
    )
    _require_exact_solver_result(
        correspondence_solver,
        "unsat",
        "adapter-correspondence",
    )

    correspondence_mutations: dict[str, Any] = {}
    for kind in model.CORRESPONDENCE_MUTATION_KINDS:
        mutation_dir = correspondence_mutation_root / kind
        mutation_dir.mkdir()
        mutation_source = mutation_dir / "adapter_model.rs"
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
        mutation_verification = _capture(
            mutation_dir / "verification",
            [str(common.VERUS), str(mutation_source), "--crate-type=lib"],
        )
        mutation_stdout = (
            ROOT / mutation_verification["stdout"]
        ).read_text()
        mutation_stderr = (
            ROOT / mutation_verification["stderr"]
        ).read_text()
        if mutation_typecheck["exit_code"] != 0:
            raise RuntimeError(f"{kind}: mutation did not type-check")
        if (
            mutation_verification["exit_code"] != 0
            or mutation_stderr
            or EXPECTED_VERUS_SUMMARY not in mutation_stdout
        ):
            raise RuntimeError(
                f"{kind}: correspondence-only mutation did not verify"
            )

        mutation_query_text = model.correspondence_query_text(mutated_text)
        model.validate_correspondence_query(mutation_query_text)
        mutation_query = mutation_dir / "adapter_correspondence.smt2"
        mutation_query.write_text(mutation_query_text)
        mutation_solver = _capture(
            mutation_dir / "adapter_correspondence",
            [z3, "-smt2", str(mutation_query)],
        )
        _require_exact_solver_result(
            mutation_solver,
            "sat",
            f"{kind}-adapter-correspondence",
        )
        correspondence_mutations[kind] = {
            "source": _artifact(mutation_source),
            "typecheck": mutation_typecheck,
            "verification": mutation_verification,
            "query": _artifact(mutation_query),
            "solver": mutation_solver,
            "typecheck_passed": True,
            "verification_passed": True,
            "correspondence_result": "sat",
            "correspondence_rejected": True,
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
        raise RuntimeError("target-078 v2 mutated a protected tree")
    if protected_files_after != protected_files_before:
        raise RuntimeError("target-078 v2 mutated a protected file")

    result = {
        "schema_version": 1,
        "artifact_id": "target_078_adapter_refinement_v2",
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "status": "engineer-complete-review-pending",
        "classification": EXPECTED_CLASSIFICATION,
        "classification_changed": False,
        "classification_basis": (
            "replay of accepted operational-v1 exact-output and full-state "
            "obligations; this package adds a constructive adapter proof"
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
        "correspondence_mutation_matrix": correspondence_mutations,
        "adapter_correspondence": {
            "query": _artifact(correspondence_path),
            "solver": correspondence_solver,
            "compared_fields": list(
                model.SMT_FIELD_BINDINGS["ComparatorAdapterFrame"]
            ),
            "compared_functions": list(
                coverage["semantic_functions"]
            ),
            "comparison_count": coverage["comparison_count"],
            "exact_callback_selectors": [
                "e_callback_state",
                "e_panicked",
            ],
            "derivation": "parsed-verus-expression-ast-to-smt",
            "accepted_smt": smt_binding,
            "verus_binding": proof_binding,
        },
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
            "operational_v2_unchanged": True,
            "parser_repair_unchanged": True,
            "frozen_authorities_unchanged": True,
            "final_campaign_unchanged": True,
            "pipeline_state_unchanged": True,
        },
        "independent_review": {
            "required": True,
            "status": "pending",
            "verdict": None,
        },
        "stage_transition": "disabled",
    }
    common.write_json(EVIDENCE / "result.json", result)

    print("target_078_adapter_refinement_v2=PASS")
    print("verus=11_verified_0_errors")
    print("adapter_correspondence=unsat")
    print("exact_output_replay=unsat")
    print("full_state_replay=unsat")
    print("nonvacuity_replay=sat")
    print(f"mutations={len(mutations)}_rejected")
    print(
        "correspondence_mutations="
        f"{len(correspondence_mutations)}_sat"
    )
    print("protected_artifacts=preserved")
    print("classification=unchanged")
    print("independent_review=pending")


if __name__ == "__main__":
    main()
