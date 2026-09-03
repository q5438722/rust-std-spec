#!/usr/bin/env python3
"""Build and capture the additive target-081 operational-v1 package."""

from __future__ import annotations

import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import preservation_policy_v3 as preservation
import target_081_operational_smt_v1 as smt
import target_081_operational_v1 as model
import target_081_operational_witness_v1 as witnesses
import target_pipeline


ROOT = Path(__file__).resolve().parents[1]
RUST_LIBRARY = (ROOT / "../../rust-1.96/library").resolve()
SPEC_ROOT = (
    ROOT / "../../nanvix-rust-std-slice-specgen-2026-08-11"
).resolve()
BASELINE = ROOT / "evidence/targets/081_core_slice_sort_unstable_by"
FROZEN_IMPLPROOF = (
    ROOT / "provenance/frozen/implproof/081_core_slice_sort_unstable_by"
)
TARGET_080_BASELINE = ROOT / "evidence/targets/080_core_slice_sort_unstable"
TARGET_080_OPERATIONAL = ROOT / "evidence/target_080_operational_v1"
EVIDENCE_ROOT = ROOT / "evidence/target_081_operational_v1"
BOUND_INPUTS = EVIDENCE_ROOT / "bound_inputs"
SOURCE_BINDINGS = EVIDENCE_ROOT / "source_bindings.json"
BOUNDARY_MANIFEST = EVIDENCE_ROOT / "boundary_manifest.json"
WITNESS = EVIDENCE_ROOT / "witness.json"
RESULT = EVIDENCE_ROOT / "result.json"
INCREMENT_RESULT = EVIDENCE_ROOT / "increment_result.json"
SOURCE_PROOF = (
    ROOT / "proofs/081_core_slice_sort_unstable_by_operational_v1.rs"
)
CROSSWALK_JSON = ROOT / "crosswalk/target_081_operational_v1_addendum.json"
CROSSWALK_CSV = ROOT / "crosswalk/target_081_operational_v1_addendum.csv"
PATH_POLICY_V5 = ROOT / "preservation/path_policy_v5.json"
PATH_POLICY_V6 = ROOT / "preservation/path_policy_v6.json"
PATH_POLICY_V4 = ROOT / "preservation/path_policy_v4.json"
WIKI_INDEX = (
    ROOT
    / ".autors/rust-std-slice-trust-boundary-conditional-completeness-v011-2026-08-28/wiki/INDEX.md"
)
WIKI_PAGE = (
    ROOT
    / ".autors/rust-std-slice-trust-boundary-conditional-completeness-v011-2026-08-28/wiki/pages/conditional-completeness/theorem-and-boundary-policy.md"
)
REVIEW_ADDENDUM = (
    ROOT / "review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md"
)
REVIEW_POLICY_V7 = ROOT / "preservation/path_policy_v7.json"
EXPECTED_VERUS_SUMMARY = "verification results:: 11 verified, 0 errors"
BASELINE_CLASSIFICATION = {
    "exact_output_determinism_status": "conditional-incomplete",
    "completeness_modulo_reviewed_equivalence_status": (
        "conditional-incomplete"
    ),
}
ARCHIVE_SOURCE_REFERENCES = {
    (
        ".autors/"
        "rust-std-slice-trust-boundary-conditional-completeness-v011-"
        "2026-08-28/wiki/INDEX.md"
    ): (
        "project-local-rewind-snapshot:"
        "e6d3e710-46ff-4840-a025-52af9b02d8f0"
    ),
    (
        ".autors/"
        "rust-std-slice-trust-boundary-conditional-completeness-v011-"
        "2026-08-28/wiki/pages/conditional-completeness/"
        "theorem-and-boundary-policy.md"
    ): (
        "project-local-rewind-snapshot:"
        "22e83f53-f3b3-4f1d-814c-335c8ceef332"
    ),
    "tools/run_acceptance.py": (
        "project-local-rewind-snapshot:"
        "d80c5504-42e1-47e9-9aae-2c11e4850f87"
    ),
    "tools/run_target_080_operational_v1.py": (
        "task-start-live-v4-bound-file"
    ),
    "tests/test_target_080_operational_artifacts_v1.py": (
        "task-start-live-v4-bound-file"
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
        BASELINE / "authority_bindings.json",
        "baseline_authority_bindings.json",
        "active-contract-source-doc-authority",
        ("evidence/targets/081_core_slice_sort_unstable_by",),
        (model.ACTIVE_CONTRACT_SHA256, '"input_order": "81"'),
        "bound-authority",
    ),
    _binding(
        BASELINE / "boundary_manifest.json",
        "baseline_boundary_manifest.json",
        "certified-target-boundary",
        ("evidence/targets/081_core_slice_sort_unstable_by",),
        ("TS-081-D002", "TS-081-D003", "TS-081-E001"),
        "protected-baseline",
    ),
    _binding(
        BASELINE / "result.json",
        "certified_result.json",
        "certified-target-classifications",
        ("evidence/targets/081_core_slice_sort_unstable_by",),
        (
            '"exact_output_determinism_status": "conditional-incomplete"',
            '"completeness_modulo_reviewed_equivalence_status": "conditional-incomplete"',
        ),
        "protected-baseline",
    ),
    _binding(
        FROZEN_IMPLPROOF / "harness.rs",
        "implproof_harness.rs",
        "implementation-proof-harness",
        ("proof_harnesses/081_core_slice_sort_unstable_by/harness.rs",),
        ("pub fn sort_unstable_by", "#[verifier::external_body]"),
        "bound-legacy-proof",
    ),
    _binding(
        FROZEN_IMPLPROOF / "transformation_manifest.json",
        "transformation_manifest.json",
        "implementation-proof-transformation-manifest",
        ("proof_manifests/081_core_slice_sort_unstable_by",),
        (
            "fnmut_comparator_closure_lowering_boundary",
            "source_backed_private_helper_boundary",
        ),
        "bound-legacy-proof",
    ),
    _binding(
        FROZEN_IMPLPROOF / "dependency_assumption_manifest.json",
        "dependency_assumption_manifest.json",
        "all-audited-trust-sites",
        ("proof_manifests/081_core_slice_sort_unstable_by",),
        (
            "shared_contract_vocabulary",
            "sort::unstable::sort",
            "compare FnMut Ordering observation",
        ),
        "bound-legacy-proof",
    ),
    _binding(
        FROZEN_IMPLPROOF / "source_body.json",
        "source_body.json",
        "implementation-proof-source-body",
        ("proof_manifests/081_core_slice_sort_unstable_by",),
        (model.TARGET, "92008bd2d8e"),
        "bound-legacy-proof",
    ),
    _binding(
        SPEC_ROOT / "specs/generated_slice_specs.rs",
        "generated_slice_specs.rs",
        "active-generated-contract-file",
        ("specs/generated_slice_specs.rs",),
        ("<[T]>::sort_unstable_by::<F>", "slice_sorted_by_cmp"),
        "bound-authority",
    ),
    _binding(
        SPEC_ROOT / "specs/slice_shared_vocabulary.rs",
        "slice_shared_vocabulary.rs",
        "active-comparator-observation-vocabulary",
        ("specs/slice_shared_vocabulary.rs",),
        ("comparator_observation", "slice_sorted_by_cmp"),
        "bound-authority",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/mod.rs",
        "slice_mod.rs",
        "public-adapter-and-rustdoc",
        ("core/src/slice/mod.rs:3140-3193",),
        (
            "pub fn sort_unstable_by",
            "compare(a, b) == Ordering::Less",
            "possible modifications via interior",
        ),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/cmp.rs",
        "cmp.rs",
        "ordering-layout-and-copy-semantics",
        ("core/src/cmp.rs:396-414",),
        ("pub enum Ordering", "Less = -1", "Greater = 1"),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/ops/drop.rs",
        "drop.rs",
        "callback-destruction-semantics",
        ("core/src/ops/drop.rs:1-220",),
        (
            "When a value is no longer needed",
            "local variables are dropped in reverse order",
            "pub const trait Drop",
        ),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/unstable/mod.rs",
        "unstable_mod.rs",
        "private-sort-entry-and-ipnsort",
        ("core/src/slice/sort/unstable/mod.rs:1-148",),
        ("if T::IS_ZST", "MAX_LEN_ALWAYS_INSERTION_SORT"),
        "reused-accepted-source-transition",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/shared/mod.rs",
        "shared_mod.rs",
        "existing-run-detection",
        ("core/src/slice/sort/shared/mod.rs:16-53",),
        ("pub(crate) fn find_existing_run", "strictly_descending"),
        "reused-accepted-source-transition",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/shared/smallsort.rs",
        "smallsort.rs",
        "small-sort-and-restoration",
        ("core/src/slice/sort/shared/smallsort.rs:15-867",),
        ("struct CopyOnDrop", "fn small_sort_network"),
        "reused-accepted-source-transition",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/unstable/quicksort.rs",
        "quicksort.rs",
        "quicksort-partition-and-restoration",
        ("core/src/slice/sort/unstable/quicksort.rs:1-393",),
        ("pub(crate) fn quicksort", "struct GapGuard"),
        "reused-accepted-source-transition",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/unstable/heapsort.rs",
        "heapsort.rs",
        "heapsort-and-sift-down",
        ("core/src/slice/sort/unstable/heapsort.rs:1-75",),
        ("pub(crate) fn heapsort", "unsafe fn sift_down"),
        "reused-accepted-source-transition",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/shared/pivot.rs",
        "pivot.rs",
        "pivot-selection",
        ("core/src/slice/sort/shared/pivot.rs:1-94",),
        ("pub fn choose_pivot", "unsafe fn median3_rec"),
        "reused-accepted-source-transition",
    ),
    _binding(
        RUST_LIBRARY / "core/src/macros/mod.rs",
        "cfg_select.rs",
        "configuration-selection",
        ("core/src/macros/mod.rs:231-236",),
        ("pub macro cfg_select", "compiler built-in"),
        "reused-accepted-source-transition",
    ),
    _binding(
        RUST_LIBRARY / "core/src/mem/mod.rs",
        "sized_type_properties.rs",
        "sized-type-properties",
        ("core/src/mem/mod.rs:1271-1324",),
        ("pub trait SizedTypeProperties", "const IS_ZST"),
        "reused-accepted-source-transition",
    ),
    _binding(
        ROOT / "tools/target_080_operational_v1.py",
        "accepted_target_080_operational_v1.py",
        "accepted-private-primary-transition",
        ("review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md",),
        ("SOURCE_MODEL_COMPLETE = True", "def execute("),
        "reused-accepted-implementation",
    ),
    _binding(
        ROOT / "tools/target_080_source_interpreter_v1.py",
        "accepted_target_080_source_interpreter_v1.py",
        "accepted-private-independent-interpreter",
        ("review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md",),
        ("Independent Rust 1.96 source interpreter", "def execute("),
        "reused-accepted-implementation",
    ),
    _binding(
        ROOT / "tools/target_080_exact_smt_v1.py",
        "accepted_target_080_exact_smt_v1.py",
        "accepted-private-smt-transition",
        ("evidence/target_080_operational_v1/obligation.smt2",),
        ("ExactSort", "TargetAdapterIsLess"),
        "reused-accepted-formal-transition",
    ),
    _binding(
        TARGET_080_OPERATIONAL / "result.json",
        "accepted_target_080_result.json",
        "accepted-private-operational-result",
        ("review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md",),
        (
            '"source_model_complete": true',
            '"field_complete_correspondence": "conditional-complete"',
        ),
        "protected-accepted-evidence",
    ),
    _binding(
        ROOT / "review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md",
        "accepted_target_080_review.md",
        "independent-private-model-review",
        ("preservation/path_policy_v5.json",),
        ("**VERDICT: ACCEPT**", "field-complete correspondence"),
        "protected-independent-review",
    ),
    _binding(
        PATH_POLICY_V5,
        "path_policy_v5.json",
        "accepted-preservation-head",
        ("preservation/path_policy_v5.json",),
        (
            '"policy_id": "slice-preservation-path-policy-v5"',
            "target_080_operational_v1_review",
        ),
        "protected-preservation-head",
    ),
)


def _relpath(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


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


def materialize_bound_inputs() -> dict[str, Any]:
    BOUND_INPUTS.mkdir(parents=True, exist_ok=True)
    for binding in BINDINGS:
        source = binding["source"]
        destination = binding["destination"]
        if not source.is_file():
            raise RuntimeError(f"bound input is missing: {source}")
        shutil.copyfile(source, destination)
    records = []
    for binding in BINDINGS:
        source = binding["source"]
        destination = binding["destination"]
        text = destination.read_text()
        for anchor in binding["semantic_anchors"]:
            if anchor not in text:
                raise RuntimeError(
                    f"{binding['role']}: source anchor is missing: {anchor}"
                )
        records.append(
            {
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
        )
    manifest = {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "source_model_complete": model.SOURCE_MODEL_COMPLETE,
        "classification_eligible": model.CLASSIFICATION_ELIGIBLE,
        "covered_source_phases": list(model.COVERED_SOURCE_PHASES),
        "missing_source_phases": [],
        "bindings": records,
        "trust_site_dispositions": model.boundary_manifest()[
            "trust_site_dispositions"
        ],
        "accepted_private_model": {
            "model_id": "target-080-operational-v1-rust-1.96-complete",
            "review_verdict": "ACCEPT",
            "preservation_head": "preservation/path_policy_v5.json",
            "verus_transition_type": (
                "AcceptedTarget080PrivateTransition"
            ),
            "verus_transition_application": (
                "accepted_private_source_transition(source input, source "
                "configuration, exact Ordering-to-Less boundary)"
            ),
            "raw_terminal_result_input": False,
        },
    }
    common.write_json(SOURCE_BINDINGS, manifest)
    return manifest


def validate_source_bindings() -> dict[str, Any]:
    manifest = json.loads(SOURCE_BINDINGS.read_text())
    if manifest["target"] != model.TARGET:
        raise RuntimeError("source bindings target drifted")
    if manifest["active_contract_sha256"] != model.ACTIVE_CONTRACT_SHA256:
        raise RuntimeError("active contract binding drifted")
    if not manifest["source_model_complete"]:
        raise RuntimeError("source model is not complete")
    if manifest["missing_source_phases"]:
        raise RuntimeError("source model retains missing phases")
    if len(manifest["bindings"]) != len(BINDINGS):
        raise RuntimeError("source closure binding count drifted")
    by_role = {record["role"]: record for record in manifest["bindings"]}
    if len(by_role) != len(BINDINGS):
        raise RuntimeError("source closure roles are not unique")
    for binding in BINDINGS:
        source = binding["source"]
        destination = binding["destination"]
        record = by_role[binding["role"]]
        if destination.read_bytes() != source.read_bytes():
            raise RuntimeError(f"bound source no longer matches: {destination}")
        if _digest(destination) != record["sha256"]:
            raise RuntimeError(f"bound source hash drifted: {destination}")
    return manifest


def _solver_capture(
    z3: str, label: str, path: Path, expected: str
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        EVIDENCE_ROOT / label,
        [z3, "-smt2", str(path)],
        cwd=ROOT,
        timeout=120,
    )
    target_pipeline.require_clean_result(record, expected, label=label)
    record.update(
        {
            "solver_result": target_pipeline.first_output_line(record),
            "expected_solver_result": expected,
        }
    )
    return record


def _write_obligation(
    z3: str, stem: str, purpose: str
) -> dict[str, Any]:
    text = smt.obligation_text(purpose)
    metadata = smt.obligation_metadata(purpose)
    smt.validate_obligation(text, metadata)
    path = EVIDENCE_ROOT / f"{stem}.smt2"
    metadata_path = EVIDENCE_ROOT / f"{stem}.metadata.json"
    path.write_text(text)
    common.write_json(metadata_path, metadata)
    return {
        "smt": _artifact(path),
        "metadata": _artifact(metadata_path),
        "solver": _solver_capture(z3, stem, path, "unsat"),
    }


def _replay_retained_classifications(z3: str) -> dict[str, Any]:
    cases = {
        "exact-output": (
            BASELINE / "exact_final_slice_obligation.smt2",
            "sat",
        ),
        "reviewed-equivalence": (BASELINE / "obligation.smt2", "sat"),
        "total-order-sanity": (
            BASELINE / "total_order_sanity.smt2",
            "unsat",
        ),
    }
    records = {}
    for label, (path, expected) in cases.items():
        before = _digest(path)
        solver = _solver_capture(
            z3, f"retained_{label}", path, expected
        )
        after = _digest(path)
        if before != after:
            raise RuntimeError(f"retained target-081 SMT mutated: {path}")
        records[label] = {
            "smt": _artifact(path),
            "before_sha256": before,
            "after_sha256": after,
            "solver": solver,
        }
    return records


def _write_crosswalk_addendum() -> dict[str, Any]:
    operational = {
        "source_operational_determinism": "conditional-complete",
        "field_complete_source_correspondence": "conditional-complete",
    }
    addendum = {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "certified_baseline_classification": BASELINE_CLASSIFICATION,
        "additive_operational_classification": operational,
        "baseline_row_mutated": False,
        "target_080_mutated": False,
        "manager_stage_mutated": False,
        "evidence_root": _relpath(EVIDENCE_ROOT),
        "independent_review": {
            "required": True,
            "status": "pending",
            "verdict": None,
            "expected_path": _relpath(REVIEW_ADDENDUM),
            "expected_successor_policy": _relpath(REVIEW_POLICY_V7),
        },
    }
    common.write_json(CROSSWALK_JSON, addendum)
    row = {
        "input_order": model.INPUT_ORDER,
        "target": model.TARGET,
        "model_id": model.MODEL_ID,
        "baseline_exact_output_determinism_status": BASELINE_CLASSIFICATION[
            "exact_output_determinism_status"
        ],
        "baseline_completeness_modulo_reviewed_equivalence_status": (
            BASELINE_CLASSIFICATION[
                "completeness_modulo_reviewed_equivalence_status"
            ]
        ),
        "source_operational_determinism": operational[
            "source_operational_determinism"
        ],
        "field_complete_source_correspondence": operational[
            "field_complete_source_correspondence"
        ],
        "baseline_row_mutated": "false",
        "target_080_mutated": "false",
        "evidence_root": _relpath(EVIDENCE_ROOT),
    }
    common.write_csv(CROSSWALK_CSV, [row], list(row))
    return {
        "json": _artifact(CROSSWALK_JSON),
        "csv": _artifact(CROSSWALK_CSV),
        "certified_ledger_mutated": False,
    }


def _write_path_policy_v6() -> dict[str, Any]:
    if not PATH_POLICY_V5.is_file():
        raise RuntimeError("path_policy_v5 is missing")
    if not PATH_POLICY_V4.is_file():
        raise RuntimeError("path_policy_v4 reconstruction template is missing")
    archived_v4 = (
        ROOT / Path(*preservation.TARGET_080_V4_ARCHIVE_PATH.parts)
    )
    if not archived_v4.is_file():
        raise RuntimeError("accepted path_policy_v4 archive is missing")
    static_paths = {
        ROOT / "tools/target_081_operational_v1.py",
        ROOT / "tools/target_081_source_interpreter_v1.py",
        ROOT / "tools/target_081_operational_witness_v1.py",
        ROOT / "tools/target_081_operational_smt_v1.py",
        ROOT / "tools/replay_target_081_operational_v1.py",
        ROOT / "tools/run_target_081_operational_v1.py",
        ROOT / "tests/test_target_081_operational_v1.py",
        ROOT / "tests/test_target_081_operational_artifacts_v1.py",
        ROOT / "tests/test_preservation_archive_v1.py",
        ROOT / "tests/test_target_080_operational_artifacts_v1.py",
        ROOT / "tools/preservation_policy_v3.py",
        ROOT / "tools/run_target_080_operational_v1.py",
        SOURCE_PROOF,
        CROSSWALK_JSON,
        CROSSWALK_CSV,
        WIKI_INDEX,
        WIKI_PAGE,
        archived_v4,
        *{
            ROOT / Path(*archive_path.parts)
            for _, archive_path in (
                preservation.TARGET_080_V4_RECORD_ARCHIVES.values()
            )
        },
    }
    evidence_paths = {
        path for path in EVIDENCE_ROOT.rglob("*") if path.is_file()
    }
    records = []
    for path in sorted(static_paths | evidence_paths):
        if not path.is_file():
            raise RuntimeError(f"path_policy_v6 input is missing: {path}")
        records.append(
            {
                "path": _relpath(path),
                "bytes": path.stat().st_size,
                "sha256": _digest(path),
            }
        )
    v5_payload = json.loads(PATH_POLICY_V5.read_text())
    accepted_v4_payload = json.loads(archived_v4.read_text())
    accepted_records = {
        record["path"]: record
        for record in accepted_v4_payload[
            "registered_post_v3_additions"
        ]["target_080_operational_v1"]["records"]
    }
    version_mappings = []
    for logical_path, (
        version_id,
        archive_path,
    ) in sorted(
        preservation.TARGET_080_V4_RECORD_ARCHIVES.items(),
        key=lambda item: Path(item[0]).parts,
    ):
        logical_record = accepted_records.get(logical_path)
        if logical_record is None:
            raise RuntimeError(
                f"accepted path_policy_v4 lacks {logical_path}"
            )
        archive_record = _artifact(
            ROOT / Path(*archive_path.parts)
        )
        if (
            archive_record["bytes"] != logical_record["bytes"]
            or archive_record["sha256"] != logical_record["sha256"]
        ):
            raise RuntimeError(
                f"historical archive does not materialize {logical_path}"
            )
        version_mappings.append(
            {
                "version_id": version_id,
                "logical_record": logical_record,
                "archive_record": archive_record,
                "source": ARCHIVE_SOURCE_REFERENCES[logical_path],
            }
        )
    archived_v4_record = _artifact(archived_v4)
    if (
        archived_v4_record["bytes"]
        != v5_payload["parent_policy"]["bytes"]
        or archived_v4_record["sha256"]
        != v5_payload["parent_policy"]["sha256"]
    ):
        raise RuntimeError(
            "accepted path_policy_v4 archive does not satisfy path_policy_v5"
        )
    policy = {
        "schema_version": 2,
        "policy_id": "slice-preservation-path-policy-v6",
        "parent_policy_id": "slice-preservation-path-policy-v5",
        "parent_policy": {
            "path": _relpath(PATH_POLICY_V5),
            "bytes": PATH_POLICY_V5.stat().st_size,
            "sha256": _digest(PATH_POLICY_V5),
        },
        "policy": (
            "path_policy_v5 remains authoritative and byte-identical. "
            "This archive-backed additive successor resolves accepted "
            "historical records only through explicit version mappings and "
            "registers the target-081 operational-v1 Engineer package. "
            "Independent acceptance must be recorded by path_policy_v7 "
            "without rewriting policies v1-v6."
        ),
        "archive_resolution": {
            "schema_version": 1,
            "archive_root": (
                preservation.TARGET_080_V4_ARCHIVE_ROOT.as_posix()
            ),
            "template_record": _artifact(PATH_POLICY_V4),
            "accepted_policy_version": {
                "version_id": preservation.TARGET_080_V4_VERSION_ID,
                "logical_record": v5_payload["parent_policy"],
                "archive_record": archived_v4_record,
                "source": (
                    "deterministic reconstruction from template_record "
                    "and record_version_mappings"
                ),
            },
            "record_version_mappings": version_mappings,
        },
        "registered_post_v5_additions": {
            "target_081_operational_v1": {
                "file_count": len(records),
                "records": records,
            }
        },
        "independent_review_lane": {
            "status": "pending",
            "expected_policy_id": "slice-preservation-path-policy-v7",
            "expected_policy_path": _relpath(REVIEW_POLICY_V7),
            "expected_verdict_path": _relpath(REVIEW_ADDENDUM),
        },
    }
    preservation._validate_target_081_v6(
        policy, v5_payload, root=ROOT
    )
    common.write_json(PATH_POLICY_V6, policy)
    return _artifact(PATH_POLICY_V6)


def main() -> int:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for target-081 operational evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if not SOURCE_PROOF.is_file():
        raise RuntimeError(f"Verus source proof is missing: {SOURCE_PROOF}")

    protected_trees = {
        "certified_target_081": BASELINE,
        "frozen_target_081": FROZEN_IMPLPROOF,
        "accepted_target_080": TARGET_080_OPERATIONAL,
        "certified_target_080": TARGET_080_BASELINE,
    }
    protected_files = {
        "ledger_csv": ROOT / "crosswalk/target_to_proof_boundary.csv",
        "ledger_json": ROOT / "crosswalk/target_to_proof_boundary.json",
        "pipeline_state": ROOT / "research/PIPELINE_STATE.json",
        **{
            f"path_policy_v{version}": (
                ROOT / f"preservation/path_policy_v{version}.json"
            )
            for version in range(1, 6)
        },
        "target_080_review": (
            ROOT / "review/REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md"
        ),
        "certified_target_081_proof": (
            ROOT / "proofs/081_core_slice_sort_unstable_by.rs"
        ),
    }
    tree_before = {
        name: _tree_digest(path) for name, path in protected_trees.items()
    }
    file_before = {
        name: _digest(path) for name, path in protected_files.items()
    }

    if EVIDENCE_ROOT.exists():
        shutil.rmtree(EVIDENCE_ROOT)
    EVIDENCE_ROOT.mkdir(parents=True)
    manifest = materialize_bound_inputs()
    validate_source_bindings()
    common.write_json(BOUNDARY_MANIFEST, model.boundary_manifest())

    payload = witnesses.witness_payload()
    common.write_json(WITNESS, payload)
    witness_capture = target_pipeline.capture_command(
        EVIDENCE_ROOT / "witness_replay",
        [
            sys.executable,
            str(ROOT / "tools/replay_target_081_operational_v1.py"),
            "--witness",
            str(WITNESS),
        ],
        cwd=ROOT,
        timeout=120,
    )
    witness_stdout = (ROOT / witness_capture["stdout"]).read_text()
    witness_stderr = (ROOT / witness_capture["stderr"]).read_text()
    if witness_capture["exit_code"] != 0 or witness_stderr:
        raise RuntimeError("target-081 witness replay failed")
    witness_result = json.loads(witness_stdout)
    if witness_result.get("status") != "passed":
        raise RuntimeError("target-081 witnesses did not pass")
    witness_capture["result"] = witness_result

    obligations = {
        smt.PRIVATE_SOURCE: _write_obligation(
            z3, "private_source_correspondence", smt.PRIVATE_SOURCE
        ),
        smt.ADAPTER_SOURCE: _write_obligation(
            z3, "adapter_source_correspondence", smt.ADAPTER_SOURCE
        ),
        smt.FIXED_BOUNDARY: _write_obligation(
            z3, "fixed_boundary_operational_determinism", smt.FIXED_BOUNDARY
        ),
    }

    nonvacuity_path = EVIDENCE_ROOT / "nonvacuity.smt2"
    nonvacuity_path.write_text(smt.nonvacuity_text())
    nonvacuity = {
        "smt": _artifact(nonvacuity_path),
        "solver": _solver_capture(
            z3, "nonvacuity", nonvacuity_path, "sat"
        ),
    }
    probes = {}
    for kind in smt.PROBE_KINDS:
        path = EVIDENCE_ROOT / f"probe_{kind}.smt2"
        path.write_text(smt.probe_text(kind))
        probes[kind] = {
            "smt": _artifact(path),
            "solver": _solver_capture(
                z3, f"probe_{kind}", path, "sat"
            ),
        }
    mutations = {}
    for kind in smt.MUTATION_KINDS:
        path = EVIDENCE_ROOT / f"mutation_{kind}.smt2"
        path.write_text(smt.mutation_text(kind))
        mutations[kind] = {
            "smt": _artifact(path),
            "solver": _solver_capture(
                z3, f"mutation_{kind}", path, "sat"
            ),
        }
    retained = _replay_retained_classifications(z3)

    captured_proof = EVIDENCE_ROOT / "verus/adapter_model.rs"
    captured_proof.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_PROOF, captured_proof)
    proof_text = captured_proof.read_text()
    for forbidden in ("external_body", "assume(", "admit(", "axiom"):
        if forbidden in proof_text:
            raise RuntimeError(
                f"trusted-free target-081 proof contains {forbidden!r}"
            )
    for required in (
        "AcceptedTarget080PrivateTransition",
        "accepted_private_source_transition",
        "source_private_comparator_boundary",
        "source_public_sort",
        "first.apply == second.apply",
        "observable_element_state",
    ):
        if required not in proof_text:
            raise RuntimeError(
                "target-081 Verus proof lacks accepted private-transition "
                f"connection: {required}"
            )
    if "fixed_boundary_projection_is_deterministic" in proof_text:
        raise RuntimeError(
            "target-081 Verus proof retains the abstract projection shortcut"
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
        timeout=120,
    )
    if (
        typecheck["exit_code"] != 0
        or (ROOT / typecheck["stderr"]).read_text()
    ):
        raise RuntimeError("target-081 Verus proof did not type-check")
    verification = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/verification",
        [str(common.VERUS), str(captured_proof), "--crate-type=lib"],
        cwd=ROOT,
        timeout=120,
    )
    verification_stdout = (ROOT / verification["stdout"]).read_text()
    if (
        verification["exit_code"] != 0
        or (ROOT / verification["stderr"]).read_text()
        or EXPECTED_VERUS_SUMMARY not in verification_stdout
    ):
        raise RuntimeError("target-081 Verus proof did not verify")

    tree_after = {
        name: _tree_digest(path) for name, path in protected_trees.items()
    }
    file_after = {
        name: _digest(path) for name, path in protected_files.items()
    }
    if tree_before != tree_after or file_before != file_after:
        raise RuntimeError("target-081 runner mutated protected evidence")

    crosswalk = _write_crosswalk_addendum()
    result = {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "artifact_id": "target_081_operational_v1",
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "status": "engineer-complete-review-pending",
        "source_model_complete": model.SOURCE_MODEL_COMPLETE,
        "classification_eligible": model.CLASSIFICATION_ELIGIBLE,
        "covered_source_phases": list(model.COVERED_SOURCE_PHASES),
        "missing_source_phases": [],
        "unresolved_source_model_phases": [],
        "classification": {
            "source_operational_determinism": "conditional-complete",
            "field_complete_source_correspondence": "conditional-complete",
        },
        "classification_scope": (
            "additive source-operational result only; both certified "
            "target-081 public-contract classifications are preserved"
        ),
        "certified_baseline_classification": BASELINE_CLASSIFICATION,
        "certified_baseline_classification_mutated": False,
        "source_bindings": _artifact(SOURCE_BINDINGS),
        "boundary_manifest": _artifact(BOUNDARY_MANIFEST),
        "trust_site_dispositions": manifest["trust_site_dispositions"],
        "independent_interpreter": {
            "path": "tools/target_081_source_interpreter_v1.py",
            "case_count": payload["case_count"],
            "field_complete_correspondence": True,
            "single_callback_evaluation": True,
            "observable_interior_state_correspondence": True,
        },
        "witness": _artifact(WITNESS),
        "witness_replay": witness_capture,
        "obligations": obligations,
        "nonvacuity": nonvacuity,
        "branch_force_probes": probes,
        "semantic_mutation_regressions": mutations,
        "retained_contract_classification_replays": retained,
        "verus": {
            "source": _artifact(SOURCE_PROOF),
            "captured": _artifact(captured_proof),
            "expected_summary": EXPECTED_VERUS_SUMMARY,
            "typecheck": typecheck,
            "verification": verification,
            "trusted_free": True,
            "accepted_private_transition_applied": True,
            "raw_private_terminal_result_parameter": False,
            "composition_proof": (
                "fixed_boundary_accepted_transition_is_deterministic"
            ),
            "accepted_private_transition": {
                "model_id": (
                    "target-080-operational-v1-rust-1.96-complete"
                ),
                "source": _artifact(
                    ROOT / "tools/target_080_operational_v1.py"
                ),
                "accepted_evidence": _artifact(
                    TARGET_080_OPERATIONAL / "result.json"
                ),
                "accepting_review": _artifact(
                    ROOT
                    / "review/"
                    "REVIEW_ADDENDUM_TARGET_080_OPERATIONAL_V1.md"
                ),
                "arguments": [
                    "SourceInput",
                    "SourceConfiguration",
                    "source_private_comparator_boundary",
                ],
                "terminal_result_supplied_as_input": False,
            },
        },
        "crosswalk_addendum": crosswalk,
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
            "target_080_unchanged": True,
            "target_081_baseline_unchanged": True,
            "manager_state_unchanged": True,
        },
        "independent_review": {
            "required": True,
            "status": "pending",
            "verdict": None,
            "expected_addendum": _relpath(REVIEW_ADDENDUM),
            "engineer_policy": _relpath(PATH_POLICY_V6),
            "expected_review_policy": _relpath(REVIEW_POLICY_V7),
        },
    }
    common.write_json(RESULT, result)
    common.write_json(
        INCREMENT_RESULT,
        {
            "schema_version": 1,
            "target": model.TARGET,
            "input_order": model.INPUT_ORDER,
            "status": result["status"],
            "classification": result["classification"],
            "certified_baseline_classification": BASELINE_CLASSIFICATION,
            "source_model_complete": True,
            "missing_source_phases": [],
            "witness_count": payload["case_count"],
            "branch_force_probe_count": len(probes),
            "semantic_mutation_count": len(mutations),
            "independent_review": result["independent_review"],
        },
    )
    path_policy = _write_path_policy_v6()
    print(
        json.dumps(
            {
                "status": result["status"],
                "target": model.TARGET,
                "witness_count": payload["case_count"],
                "obligations": {
                    purpose: item["solver"]["solver_result"]
                    for purpose, item in obligations.items()
                },
                "nonvacuity": nonvacuity["solver"]["solver_result"],
                "branch_force_probes": len(probes),
                "semantic_mutations": len(mutations),
                "retained_classifications": {
                    name: item["solver"]["solver_result"]
                    for name, item in retained.items()
                },
                "verus": EXPECTED_VERUS_SUMMARY,
                "path_policy_v6": path_policy,
                "independent_review": "pending",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
