#!/usr/bin/env python3
"""Build and capture the complete additive target-080 operational package."""

from __future__ import annotations

import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import replay_target_080_operational_v1 as replay
import target_080_operational_smt_v1 as smt
import target_080_operational_v1 as model
import target_080_operational_witness_v1 as witnesses
import target_pipeline


ROOT = Path(__file__).resolve().parents[1]
RUST_LIBRARY = (ROOT / "../../rust-1.96/library").resolve()
BASELINE = ROOT / "evidence/targets/080_core_slice_sort_unstable"
FROZEN_IMPLPROOF = (
    ROOT / "provenance/frozen/implproof/080_core_slice_sort_unstable"
)
EVIDENCE_ROOT = ROOT / "evidence/target_080_operational_v1"
BOUND_INPUTS = EVIDENCE_ROOT / "bound_inputs"
SOURCE_BINDINGS = EVIDENCE_ROOT / "source_bindings.json"
INCREMENT_RESULT = EVIDENCE_ROOT / "increment_result.json"
RESULT = EVIDENCE_ROOT / "result.json"
BOUNDARY_MANIFEST = EVIDENCE_ROOT / "boundary_manifest.json"
WITNESS = EVIDENCE_ROOT / "witness.json"
SOURCE_PROOF = ROOT / "proofs/080_core_slice_sort_unstable_operational_v1.rs"
CROSSWALK_JSON = ROOT / "crosswalk/target_080_operational_v1_addendum.json"
CROSSWALK_CSV = ROOT / "crosswalk/target_080_operational_v1_addendum.csv"
REVIEW_ADDENDUM = (
    ROOT / "review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md"
)
REVIEW_POLICY_V5 = ROOT / "preservation/path_policy_v5.json"
PATH_POLICY_V4 = ROOT / "preservation/path_policy_v4.json"
PATH_POLICY_V3 = ROOT / "preservation/path_policy_v3.json"
EXPECTED_VERUS_SUMMARY = "verification results:: 5 verified, 0 errors"
BASELINE_CLASSIFICATION = {
    "exact_output_determinism_status": "conditional-incomplete",
    "completeness_modulo_reviewed_equivalence_status": (
        "conditional-complete"
    ),
}


def _binding(
    source: Path,
    destination_name: str,
    role: str,
    references: tuple[str, ...],
    anchors: tuple[str, ...],
    disposition: str,
) -> dict[str, Any]:
    return {
        "source": source,
        "destination": BOUND_INPUTS / destination_name,
        "role": role,
        "references": references,
        "semantic_anchors": anchors,
        "disposition": disposition,
    }


BINDINGS = (
    _binding(
        BASELINE / "bound_inputs/source_item.rs",
        "source_item.rs",
        "public-target-adapter",
        ("core/src/slice/mod.rs:3133-3138",),
        ("pub fn sort_unstable", "sort::unstable::sort(self, &mut T::lt)"),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/unstable/mod.rs",
        "unstable_mod.rs",
        "unstable-sort-entry-and-ipnsort-dispatch",
        ("core/src/slice/sort/unstable/mod.rs:1-148",),
        (
            "if T::IS_ZST",
            "MAX_LEN_ALWAYS_INSERTION_SORT: usize = 20",
            "let (run_len, was_reversed) = find_existing_run",
            "let limit = 2 * (len | 1).ilog2()",
        ),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/shared/mod.rs",
        "shared_mod.rs",
        "existing-run-detection",
        ("core/src/slice/sort/shared/mod.rs:16-53",),
        (
            "pub(crate) fn find_existing_run",
            "let strictly_descending = is_less",
            "(run_len, strictly_descending)",
        ),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/shared/smallsort.rs",
        "smallsort.rs",
        "insertion-and-type-specialized-small-sorts",
        ("core/src/slice/sort/shared/smallsort.rs:15-867",),
        (
            "pub(crate) trait UnstableSmallSortTypeImpl",
            "unsafe fn insert_tail",
            "pub fn insertion_sort_shift_left",
            "fn small_sort_network",
        ),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/unstable/quicksort.rs",
        "quicksort.rs",
        "quicksort-partition-and-guards",
        ("core/src/slice/sort/unstable/quicksort.rs:1-393",),
        (
            "pub(crate) fn quicksort",
            "pub(crate) fn partition",
            "struct GapGuard",
            "struct GapGuardRaw",
        ),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/unstable/heapsort.rs",
        "heapsort.rs",
        "heapsort-and-sift-down",
        ("core/src/slice/sort/unstable/heapsort.rs:1-75",),
        ("pub(crate) fn heapsort", "unsafe fn sift_down"),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/shared/pivot.rs",
        "pivot.rs",
        "pivot-selection",
        ("core/src/slice/sort/shared/pivot.rs:1-94",),
        ("pub fn choose_pivot", "unsafe fn median3_rec", "fn median3"),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/macros/mod.rs",
        "cfg_select.rs",
        "cfg-select-semantics",
        ("core/src/macros/mod.rs:231-236",),
        ("pub macro cfg_select", "compiler built-in"),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/mem/mod.rs",
        "sized_type_properties.rs",
        "sized-type-properties",
        ("core/src/mem/mod.rs:1271-1324",),
        ("pub trait SizedTypeProperties", "const IS_ZST: bool"),
        "operationally-modeled",
    ),
    _binding(
        BASELINE / "bound_inputs/generated_declaration.rs",
        "generated_declaration.rs",
        "active-generated-contract",
        ("specs/generated_slice_specs.rs:1269-1275",),
        ("pub assume_specification", "<[T]>::sort_unstable"),
        "bound-authority",
    ),
    _binding(
        BASELINE / "bound_inputs/public_docs.md",
        "public_docs.md",
        "public-rustdoc",
        ("core/src/slice/mod.rs:3079-3130",),
        (
            "preserving the initial order of equal elements",
            "All original elements will remain in the slice",
        ),
        "bound-authority",
    ),
    _binding(
        BASELINE / "bound_inputs/ord_observation_vocabulary.rs",
        "ord_observation_vocabulary.rs",
        "generated-ord-vocabulary",
        ("specs/slice_shared_vocabulary.rs:330-379",),
        ("ord_cmp_observed", "axiom_ord_leq_observed_transitive"),
        "bound-authority",
    ),
    _binding(
        BASELINE / "bound_inputs/ord_totality_docs.rs",
        "ord_totality_docs.rs",
        "ord-totality-rustdoc",
        ("core/src/cmp.rs:733-761",),
        ("total order", "Ord"),
        "bound-authority",
    ),
    _binding(
        BASELINE / "authority_bindings.json",
        "baseline_authority_bindings.json",
        "certified-authority-bindings",
        ("evidence/targets/080_core_slice_sort_unstable",),
        (model.ACTIVE_CONTRACT_SHA256, '"input_order": "80"'),
        "bound-authority",
    ),
    _binding(
        BASELINE / "boundary_manifest.json",
        "baseline_boundary_manifest.json",
        "certified-boundary-manifest",
        ("evidence/targets/080_core_slice_sort_unstable",),
        ("TS-080-D002", "TS-080-D003", "TS-080-E001"),
        "bound-authority",
    ),
    _binding(
        BASELINE / "trust_site_bindings.json",
        "trust_site_bindings.json",
        "audited-trust-site-records",
        ("evidence/targets/080_core_slice_sort_unstable",),
        ("TS-080-D002", "TS-080-D003", "TS-080-E001"),
        "bound-authority",
    ),
    _binding(
        BASELINE / "result.json",
        "certified_result.json",
        "certified-target-classifications",
        ("evidence/targets/080_core_slice_sort_unstable",),
        (
            '"exact_output_determinism_status": "conditional-incomplete"',
            '"completeness_modulo_reviewed_equivalence_status": "conditional-complete"',
        ),
        "protected-baseline",
    ),
    _binding(
        FROZEN_IMPLPROOF / "harness.rs",
        "implproof_harness.rs",
        "implementation-proof-harness",
        ("proof_harnesses/080_core_slice_sort_unstable/harness.rs",),
        ("pub fn sort_unstable", "#[verifier::external_body]"),
        "bound-legacy-proof",
    ),
    _binding(
        FROZEN_IMPLPROOF / "transformation_manifest.json",
        "transformation_manifest.json",
        "implementation-proof-transformation-manifest",
        ("proof_manifests/080_core_slice_sort_unstable",),
        ("source_backed_private_helper_boundary", "ord_lt_callback"),
        "bound-legacy-proof",
    ),
    _binding(
        FROZEN_IMPLPROOF / "dependency_assumption_manifest.json",
        "dependency_assumption_manifest.json",
        "implementation-proof-dependency-manifest",
        ("proof_manifests/080_core_slice_sort_unstable",),
        ("sort::unstable::sort", "Ord::lt observation"),
        "bound-legacy-proof",
    ),
    _binding(
        FROZEN_IMPLPROOF / "source_body.json",
        "source_body.json",
        "implementation-proof-source-body-manifest",
        ("proof_manifests/080_core_slice_sort_unstable",),
        (
            model.TARGET,
            "5154b661dcc16f24263c4b635e0888ffc4be3015e2838c800eab883b6f352be6",
        ),
        "bound-legacy-proof",
    ),
)


def _relpath(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _record(binding: dict[str, Any]) -> dict[str, Any]:
    destination = binding["destination"]
    source = binding["source"]
    return {
        "role": binding["role"],
        "path": _relpath(destination),
        "origin_path": _relpath(source),
        "references": list(binding["references"]),
        "semantic_anchors": list(binding["semantic_anchors"]),
        "disposition": binding["disposition"],
        "bytes": destination.stat().st_size,
        "sha256": _digest(destination),
        "origin_sha256": _digest(source),
    }


def materialize_bound_inputs() -> dict[str, Any]:
    BOUND_INPUTS.mkdir(parents=True, exist_ok=True)
    for binding in BINDINGS:
        source = binding["source"]
        destination = binding["destination"]
        if not source.is_file():
            raise RuntimeError(f"bound input is missing: {source}")
        shutil.copyfile(source, destination)

    records = [_record(binding) for binding in BINDINGS]
    manifest = {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "source_model_complete": model.SOURCE_MODEL_COMPLETE,
        "classification_eligible": model.CLASSIFICATION_ELIGIBLE,
        "covered_source_phases": list(model.COVERED_SOURCE_PHASES),
        "missing_source_phases": list(model.MISSING_SOURCE_PHASES),
        "bindings": records,
        "boundary": model.boundary_manifest(),
        "target_078_kernel_correspondence": list(
            model.TARGET_078_KERNEL_CORRESPONDENCE
        ),
        "trust_site_dispositions": {
            "TS-080-D002": "replaced-by-bound-source-transitions",
            "TS-080-D003": "admitted-total-per-call-Ord-observations",
            "TS-080-E001": "replaced-by-bound-source-transitions",
        },
        "classification_publication": (
            "additive-operational-v1-only-certified-baseline-preserved"
        ),
    }
    SOURCE_BINDINGS.parent.mkdir(parents=True, exist_ok=True)
    SOURCE_BINDINGS.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    return manifest


def validate_source_bindings() -> dict[str, Any]:
    manifest = json.loads(SOURCE_BINDINGS.read_text())
    if manifest["target"] != model.TARGET:
        raise RuntimeError("source bindings target drifted")
    if manifest["active_contract_sha256"] != model.ACTIVE_CONTRACT_SHA256:
        raise RuntimeError("active contract binding drifted")
    if (
        not manifest["source_model_complete"]
        or not manifest["classification_eligible"]
    ):
        raise RuntimeError("complete source model flags are missing")
    if manifest["missing_source_phases"] != []:
        raise RuntimeError("source model still has missing phases")
    if len(manifest["bindings"]) != len(BINDINGS):
        raise RuntimeError("bound source closure is incomplete")

    by_role = {record["role"]: record for record in manifest["bindings"]}
    if len(by_role) != len(BINDINGS):
        raise RuntimeError("bound source roles must be unique")
    for binding in BINDINGS:
        record = by_role[binding["role"]]
        source = binding["source"]
        destination = binding["destination"]
        if not destination.is_file():
            raise RuntimeError(f"frozen input is missing: {destination}")
        if _digest(destination) != record["sha256"]:
            raise RuntimeError(f"frozen input hash drifted: {destination}")
        if destination.read_bytes() != source.read_bytes():
            raise RuntimeError(
                f"frozen input no longer matches its origin: {destination}"
            )
        text = destination.read_text()
        for anchor in binding["semantic_anchors"]:
            if anchor not in text:
                raise RuntimeError(
                    f"{binding['role']}: source anchor is missing: {anchor}"
                )
    return manifest


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


def _artifact(path: Path) -> dict[str, Any]:
    return target_pipeline.artifact_record(path)


def _solver_capture(
    z3: str, label: str, path: Path, expected: str
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        EVIDENCE_ROOT / label,
        [z3, "-smt2", str(path)],
        cwd=ROOT,
        timeout=30,
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
) -> dict[str, Any]:
    addendum = {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "certified_baseline_classification": BASELINE_CLASSIFICATION,
        "additive_operational_classification": classification,
        "evidence_root": _relpath(EVIDENCE_ROOT),
        "independent_review": {
            "required": True,
            "status": "pending",
            "verdict": None,
            "expected_path": _relpath(REVIEW_ADDENDUM),
            "separate_preservation_policy": _relpath(REVIEW_POLICY_V5),
        },
        "baseline_row_mutated": False,
        "target_081_mutated": False,
        "manager_stage_mutated": False,
    }
    common.write_json(CROSSWALK_JSON, addendum)
    csv_row = {
        "input_order": model.INPUT_ORDER,
        "target": model.TARGET,
        "model_id": model.MODEL_ID,
        "baseline_exact_output_determinism_status": (
            BASELINE_CLASSIFICATION["exact_output_determinism_status"]
        ),
        "baseline_completeness_modulo_reviewed_equivalence_status": (
            BASELINE_CLASSIFICATION[
                "completeness_modulo_reviewed_equivalence_status"
            ]
        ),
        "operational_exact_output_and_terminal_state": classification[
            "exact_output_and_terminal_state"
        ],
        "operational_field_complete_correspondence": classification[
            "field_complete_correspondence"
        ],
        "baseline_row_mutated": "false",
        "evidence_root": _relpath(EVIDENCE_ROOT),
    }
    common.write_csv(CROSSWALK_CSV, [csv_row], list(csv_row))
    return {
        "json": _artifact(CROSSWALK_JSON),
        "csv": _artifact(CROSSWALK_CSV),
        "certified_ledger_mutated": False,
    }


def _write_path_policy_v4() -> dict[str, Any]:
    if REVIEW_POLICY_V5.is_file():
        return _artifact(PATH_POLICY_V4)
    if not PATH_POLICY_V3.is_file():
        raise RuntimeError("path_policy_v3 is missing")
    static_paths = {
        ROOT / "tools/target_080_operational_v1.py",
        ROOT / "tools/target_080_source_interpreter_v1.py",
        ROOT / "tools/target_080_operational_witness_v1.py",
        ROOT / "tools/target_080_exact_smt_v1.py",
        ROOT / "tools/target_080_operational_smt_v1.py",
        ROOT / "tools/checker_guards.py",
        ROOT / "tools/replay_target_080_operational_v1.py",
        ROOT / "tools/run_target_080_operational_v1.py",
        ROOT / "tools/run_acceptance.py",
        ROOT / "tests/test_target_080_operational_v1.py",
        ROOT / "tests/test_target_080_operational_artifacts_v1.py",
        SOURCE_PROOF,
        CROSSWALK_JSON,
        CROSSWALK_CSV,
        (
            ROOT
            / ".autors/rust-std-slice-trust-boundary-conditional-completeness-v011-2026-08-28/wiki/INDEX.md"
        ),
        (
            ROOT
            / ".autors/rust-std-slice-trust-boundary-conditional-completeness-v011-2026-08-28/wiki/pages/conditional-completeness/theorem-and-boundary-policy.md"
        ),
    }
    evidence_paths = {
        path
        for path in EVIDENCE_ROOT.rglob("*")
        if path.is_file()
        and "independent_review_gate" not in path.parts
    }
    records = []
    for path in sorted(static_paths | evidence_paths):
        if not path.is_file():
            raise RuntimeError(f"path_policy_v4 input is missing: {path}")
        records.append(
            {
                "path": _relpath(path),
                "bytes": path.stat().st_size,
                "sha256": _digest(path),
            }
        )
    policy = {
        "schema_version": 1,
        "policy_id": "slice-preservation-path-policy-v4",
        "parent_policy_id": "slice-preservation-path-policy-v3",
        "parent_policy": {
            "path": _relpath(PATH_POLICY_V3),
            "bytes": PATH_POLICY_V3.stat().st_size,
            "sha256": _digest(PATH_POLICY_V3),
        },
        "policy": (
            "path_policy_v3 remains authoritative and byte-identical. "
            "This additive successor registers the complete target-080 "
            "operational-v1 Engineer source, proof, correspondence, mutation, "
            "and generated evidence paths. A later independent verdict must "
            "be registered by a separate successor policy."
        ),
        "registered_post_v3_additions": {
            "target_080_operational_v1": {
                "file_count": len(records),
                "records": records,
            }
        },
        "independent_review_lane": {
            "status": "pending",
            "expected_policy_id": "slice-preservation-path-policy-v5",
            "expected_policy_path": _relpath(REVIEW_POLICY_V5),
            "expected_verdict_path": _relpath(REVIEW_ADDENDUM),
        },
    }
    common.write_json(PATH_POLICY_V4, policy)
    return _artifact(PATH_POLICY_V4)


def main() -> int:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for target-080 operational evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if not SOURCE_PROOF.is_file():
        raise RuntimeError(f"Verus source proof is missing: {SOURCE_PROOF}")

    protected_trees = {
        "certified_target_080": BASELINE,
        "frozen_target_080": FROZEN_IMPLPROOF,
    }
    protected_files = {
        "ledger_csv": ROOT / "crosswalk/target_to_proof_boundary.csv",
        "ledger_json": ROOT / "crosswalk/target_to_proof_boundary.json",
        "pipeline_state": ROOT / "research/PIPELINE_STATE.json",
        "path_policy_v1": ROOT / "preservation/path_policy_v1.json",
        "path_policy_v2": ROOT / "preservation/path_policy_v2.json",
        "path_policy_v3": PATH_POLICY_V3,
        "certified_target_080_proof": (
            ROOT / "proofs/080_core_slice_sort_unstable.rs"
        ),
    }
    tree_before = {
        name: _tree_digest(path) for name, path in protected_trees.items()
    }
    file_before = {
        name: _digest(path) for name, path in protected_files.items()
    }

    manifest = materialize_bound_inputs()
    validate_source_bindings()
    common.write_json(BOUNDARY_MANIFEST, model.boundary_manifest())

    payload = witnesses.witness_payload()
    common.write_json(WITNESS, payload)
    witness_capture = target_pipeline.capture_command(
        EVIDENCE_ROOT / "witness_replay",
        [
            sys.executable,
            str(ROOT / "tools/replay_target_080_operational_v1.py"),
            "--witness",
            str(WITNESS),
        ],
        cwd=ROOT,
        timeout=60,
    )
    witness_stdout = (ROOT / witness_capture["stdout"]).read_text()
    witness_stderr = (ROOT / witness_capture["stderr"]).read_text()
    if witness_capture["exit_code"] != 0 or witness_stderr:
        raise RuntimeError("target-080 witness replay failed")
    witness_result = json.loads(witness_stdout)
    if witness_result.get("status") != "passed":
        raise RuntimeError("target-080 witnesses did not pass")
    witness_capture["result"] = witness_result

    obligations: dict[str, Any] = {}
    for stem, purpose in (
        ("exact_output_obligation", smt.EXACT),
        ("obligation", smt.FULL),
    ):
        text = smt.obligation_text(purpose)
        metadata = smt.obligation_metadata(purpose)
        smt.validate_obligation(text, metadata)
        smt_path = EVIDENCE_ROOT / f"{stem}.smt2"
        metadata_path = EVIDENCE_ROOT / f"{stem}.metadata.json"
        smt_path.write_text(text)
        common.write_json(metadata_path, metadata)
        obligations[purpose] = {
            "smt": _artifact(smt_path),
            "metadata": _artifact(metadata_path),
            "solver": _solver_capture(z3, stem, smt_path, "unsat"),
        }

    nonvacuity_path = EVIDENCE_ROOT / "nonvacuity.smt2"
    nonvacuity_path.write_text(smt.nonvacuity_text())
    nonvacuity = {
        "smt": _artifact(nonvacuity_path),
        "solver": _solver_capture(
            z3, "nonvacuity", nonvacuity_path, "sat"
        ),
    }

    probes: dict[str, Any] = {}
    for kind in smt.PROBE_KINDS:
        path = EVIDENCE_ROOT / f"probe_{kind}.smt2"
        path.write_text(smt.probe_text(kind))
        probes[kind] = {
            "smt": _artifact(path),
            "solver": _solver_capture(
                z3, f"probe_{kind}", path, "sat"
            ),
        }

    mutations: dict[str, Any] = {}
    for kind in smt.MUTATION_PROBES:
        path = EVIDENCE_ROOT / f"mutation_{kind}.smt2"
        path.write_text(smt.mutation_probe_text(kind))
        mutations[kind] = {
            "smt": _artifact(path),
            "solver": _solver_capture(
                z3, f"mutation_{kind}", path, "sat"
            ),
        }

    captured_proof = EVIDENCE_ROOT / "verus/sort_model.rs"
    captured_proof.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_PROOF, captured_proof)
    proof_text = captured_proof.read_text()
    for forbidden in ("external_body", "assume(", "admit(", "axiom"):
        if forbidden in proof_text:
            raise RuntimeError(
                f"trusted-free Verus proof contains {forbidden!r}"
            )
    typecheck = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/typecheck",
        [
            str(common.VERUS),
            str(captured_proof),
            "--crate-type=lib",
            "--no-verify",
        ],
        cwd=ROOT,
        timeout=60,
    )
    if (
        typecheck["exit_code"] != 0
        or (ROOT / typecheck["stderr"]).read_text()
    ):
        raise RuntimeError("target-080 Verus proof did not type-check")
    verification = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/verification",
        [str(common.VERUS), str(captured_proof), "--crate-type=lib"],
        cwd=ROOT,
        timeout=60,
    )
    verification_stdout = (ROOT / verification["stdout"]).read_text()
    if (
        verification["exit_code"] != 0
        or (ROOT / verification["stderr"]).read_text()
        or EXPECTED_VERUS_SUMMARY not in verification_stdout
    ):
        raise RuntimeError("target-080 Verus proof did not verify")

    mutation_source = EVIDENCE_ROOT / "verus/sequence_projection_mutation.rs"
    anchor = "sequence: source.state.sequence,"
    if proof_text.count(anchor) != 1:
        raise RuntimeError("Verus sequence projection anchor drifted")
    mutation_source.write_text(
        proof_text.replace(anchor, "sequence: Seq::empty(),", 1)
    )
    proof_mutation = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/sequence_projection_mutation",
        [str(common.VERUS), str(mutation_source), "--crate-type=lib"],
        cwd=ROOT,
        timeout=60,
    )
    mutation_stdout = (ROOT / proof_mutation["stdout"]).read_text()
    if (
        proof_mutation["exit_code"] == 0
        or "verification results" not in mutation_stdout
        or "0 errors" in mutation_stdout
    ):
        raise RuntimeError("Verus projection mutation was not rejected")

    tree_after = {
        name: _tree_digest(path) for name, path in protected_trees.items()
    }
    file_after = {
        name: _digest(path) for name, path in protected_files.items()
    }
    if tree_after != tree_before or file_after != file_before:
        raise RuntimeError("additive target-080 runner mutated protected state")

    classification = {
        "exact_output_and_terminal_state": "conditional-complete",
        "field_complete_correspondence": "conditional-complete",
    }
    if (
        any(
            item["solver"]["solver_result"] != "unsat"
            for item in obligations.values()
        )
        or nonvacuity["solver"]["solver_result"] != "sat"
        or any(
            item["solver"]["solver_result"] != "sat"
            for item in probes.values()
        )
        or any(
            item["solver"]["solver_result"] != "sat"
            for item in mutations.values()
        )
        or witness_result["status"] != "passed"
        or EXPECTED_VERUS_SUMMARY not in verification_stdout
        or not model.SOURCE_MODEL_COMPLETE
        or model.MISSING_SOURCE_PHASES
    ):
        raise RuntimeError("classification prerequisites are incomplete")

    crosswalk = _write_crosswalk_addendum(classification)
    result = {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "artifact_id": "target_080_operational_v1",
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "status": "engineer-complete-review-pending",
        "classification": classification,
        "classification_scope": (
            "additive operational-v1 finding only; certified target-080 "
            "classifications remain byte-identical"
        ),
        "certified_baseline_classification": BASELINE_CLASSIFICATION,
        "certified_baseline_classification_mutated": False,
        "source_model_complete": True,
        "classification_eligible": True,
        "covered_source_phases": list(model.COVERED_SOURCE_PHASES),
        "missing_source_phases": [],
        "unresolved_source_model_phases": [],
        "source_bindings": _artifact(SOURCE_BINDINGS),
        "boundary_manifest": _artifact(BOUNDARY_MANIFEST),
        "obligations": obligations,
        "nonvacuity": nonvacuity,
        "semantic_force_probes": probes,
        "semantic_mutation_regressions": mutations,
        "witness": _artifact(WITNESS),
        "witness_replay": witness_capture,
        "independent_interpreter": {
            "path": "tools/target_080_source_interpreter_v1.py",
            "field_complete_correspondence": True,
            "case_count": witness_result["witness_count"],
        },
        "verus": {
            "source_model": _artifact(SOURCE_PROOF),
            "captured_model": _artifact(captured_proof),
            "typecheck": typecheck,
            "verification": verification,
            "expected_summary": EXPECTED_VERUS_SUMMARY,
            "negative_projection_mutation": {
                "source": _artifact(mutation_source),
                "verification": proof_mutation,
                "rejected": True,
            },
            "trusted_free": True,
        },
        "crosswalk_addendum": crosswalk,
        "trust_site_dispositions": manifest["trust_site_dispositions"],
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
            "certified_target_080_unchanged": True,
            "pipeline_state_unchanged": True,
        },
        "independent_review": {
            "required": True,
            "status": "pending",
            "verdict": None,
            "expected_addendum": _relpath(REVIEW_ADDENDUM),
            "separate_preservation_policy": _relpath(REVIEW_POLICY_V5),
        },
        "path_policy_v4": "preservation/path_policy_v4.json",
        "stage_transition": "disabled",
    }
    common.write_json(RESULT, result)
    common.write_json(INCREMENT_RESULT, result)
    path_policy = _write_path_policy_v4()

    print("target_080_operational_v1=PASS")
    print("source_model_complete=true")
    print("missing_source_phases=0")
    print(f"witnesses={witness_result['witness_count']}_passed")
    print(f"source_force_probes={len(probes)}_sat")
    print(f"semantic_mutations={len(mutations)}_sat")
    print("correspondence_obligations=2_unsat")
    print("verus=5_verified_0_errors")
    print("verus_projection_mutation=rejected")
    print("certified_target_080=preserved")
    print("independent_review=pending")
    print(f"path_policy_v4_sha256={path_policy['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
