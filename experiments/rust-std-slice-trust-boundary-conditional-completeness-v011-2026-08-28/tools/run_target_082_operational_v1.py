#!/usr/bin/env python3
"""Build and capture the additive target-082 operational-v1 package."""

from __future__ import annotations

import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import preservation_policy_v8 as preservation
import target_082_operational_smt_v1 as smt
import target_082_operational_v1 as model
import target_082_operational_witness_v1 as witnesses
import target_pipeline


ROOT = Path(__file__).resolve().parents[1]
RUST_LIBRARY = (ROOT / "../../rust-1.96/library").resolve()
SPEC_ROOT = (
    ROOT / "../../nanvix-rust-std-slice-specgen-2026-08-11"
).resolve()
BASELINE = ROOT / "evidence/targets/082_core_slice_sort_unstable_by_key"
FROZEN_IMPLPROOF = (
    ROOT
    / "provenance/frozen/implproof/082_core_slice_sort_unstable_by_key"
)
TARGET_079_OPERATIONAL = ROOT / "evidence/target_079_operational_v1"
TARGET_080_OPERATIONAL = ROOT / "evidence/target_080_operational_v1"
TARGET_081_OPERATIONAL = ROOT / "evidence/target_081_operational_v1"
EVIDENCE_ROOT = ROOT / "evidence/target_082_operational_v1"
BOUND_INPUTS = EVIDENCE_ROOT / "bound_inputs"
SOURCE_BINDINGS = EVIDENCE_ROOT / "source_bindings.json"
BOUNDARY_MANIFEST = EVIDENCE_ROOT / "boundary_manifest.json"
WITNESS = EVIDENCE_ROOT / "witness.json"
RESULT = EVIDENCE_ROOT / "result.json"
INCREMENT_RESULT = EVIDENCE_ROOT / "increment_result.json"
SOURCE_PROOF = (
    ROOT
    / "proofs/082_core_slice_sort_unstable_by_key_operational_v1.rs"
)
CROSSWALK_JSON = ROOT / "crosswalk/target_082_operational_v1_addendum.json"
CROSSWALK_CSV = ROOT / "crosswalk/target_082_operational_v1_addendum.csv"
PATH_POLICY_V8 = ROOT / "preservation/path_policy_v8.json"
PATH_POLICY_V7 = ROOT / "preservation/path_policy_v7.json"
REVIEW_ADDENDUM = (
    ROOT / "review/REVIEW_ADDENDUM_TARGET_082_OPERATIONAL_V1.md"
)
REVIEW_POLICY_V9 = ROOT / "preservation/path_policy_v9.json"
WIKI_INDEX = (
    ROOT
    / ".autors/rust-std-slice-trust-boundary-conditional-completeness-v011-2026-08-28/wiki/INDEX.md"
)
WIKI_PAGE = (
    ROOT
    / ".autors/rust-std-slice-trust-boundary-conditional-completeness-v011-2026-08-28/wiki/pages/conditional-completeness/target-082-key-sort-operational-v1.md"
)
EXPECTED_VERUS_SUMMARY = "verification results:: 12 verified, 0 errors"
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
        BASELINE / "authority_bindings.json",
        "baseline_authority_bindings.json",
        "active-contract-source-doc-authority",
        ("evidence/targets/082_core_slice_sort_unstable_by_key",),
        (model.ACTIVE_CONTRACT_SHA256, '"input_order": "82"'),
        "bound-authority",
    ),
    _binding(
        BASELINE / "trust_site_bindings.json",
        "trust_site_bindings.json",
        "all-six-audited-trust-sites",
        ("evidence/targets/082_core_slice_sort_unstable_by_key",),
        ("TS-082-D002", "TS-082-D003", "TS-082-E001"),
        "bound-authority",
    ),
    _binding(
        BASELINE / "boundary_manifest.json",
        "baseline_boundary_manifest.json",
        "certified-target-boundary",
        ("evidence/targets/082_core_slice_sort_unstable_by_key",),
        ('"admitted_trust_site_ids"', "TS-082-D004"),
        "protected-baseline",
    ),
    _binding(
        BASELINE / "result.json",
        "certified_result.json",
        "certified-target-classifications",
        ("evidence/targets/082_core_slice_sort_unstable_by_key",),
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
        ("proof_harnesses/082_core_slice_sort_unstable_by_key/harness.rs",),
        ("pub fn sort_unstable_by_key", "#[verifier::external_body]"),
        "bound-legacy-proof",
    ),
    _binding(
        FROZEN_IMPLPROOF / "transformation_manifest.json",
        "transformation_manifest.json",
        "implementation-proof-transformation-manifest",
        ("proof_manifests/082_core_slice_sort_unstable_by_key",),
        (
            "verus_fnmut_key_ord_closure_lowering_boundary",
            "source_backed_private_helper_boundary",
        ),
        "bound-legacy-proof",
    ),
    _binding(
        FROZEN_IMPLPROOF / "dependency_assumption_manifest.json",
        "dependency_assumption_manifest.json",
        "implementation-proof-dependency-manifest",
        ("proof_manifests/082_core_slice_sort_unstable_by_key",),
        (
            "FnMut key extraction and Ord::lt observation",
            "sort::unstable::sort",
        ),
        "bound-legacy-proof",
    ),
    _binding(
        FROZEN_IMPLPROOF / "source_body.json",
        "source_body.json",
        "implementation-proof-source-body",
        ("proof_manifests/082_core_slice_sort_unstable_by_key",),
        (model.TARGET, "a1709e9e61a25"),
        "bound-legacy-proof",
    ),
    _binding(
        SPEC_ROOT / "specs/generated_slice_specs.rs",
        "generated_slice_specs.rs",
        "active-generated-contract-file",
        ("specs/generated_slice_specs.rs:1288-1297",),
        ("<[T]>::sort_unstable_by_key::<K, F>", "slice_sorted_by_key"),
        "bound-authority",
    ),
    _binding(
        SPEC_ROOT / "specs/slice_shared_vocabulary.rs",
        "slice_shared_vocabulary.rs",
        "active-key-contract-vocabulary",
        ("specs/slice_shared_vocabulary.rs",),
        ("fnmut_key_observed", "slice_sorted_by_key"),
        "bound-authority",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/mod.rs",
        "slice_mod.rs",
        "public-adapter-and-rustdoc",
        ("core/src/slice/mod.rs:3195-3246",),
        (
            "pub fn sort_unstable_by_key",
            "f(a).lt(&f(b))",
            "**without** preserving",
        ),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/cmp.rs",
        "cmp.rs",
        "ord-lt-and-ordering-semantics",
        ("core/src/cmp.rs",),
        ("pub enum Ordering", "pub const trait Ord"),
        "operationally-modeled",
    ),
    _binding(
        RUST_LIBRARY / "core/src/ops/drop.rs",
        "drop.rs",
        "owned-key-and-callback-destruction",
        ("core/src/ops/drop.rs",),
        ("pub const trait Drop", "reverse order"),
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
        "small-sort-and-copy-on-drop-restoration",
        ("core/src/slice/sort/shared/smallsort.rs",),
        ("struct CopyOnDrop", "fn small_sort_network"),
        "reused-accepted-source-transition",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/unstable/quicksort.rs",
        "quicksort.rs",
        "partition-and-gap-guard-restoration",
        ("core/src/slice/sort/unstable/quicksort.rs",),
        ("pub(crate) fn quicksort", "struct GapGuard"),
        "reused-accepted-source-transition",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/unstable/heapsort.rs",
        "heapsort.rs",
        "heapsort-and-sift-down",
        ("core/src/slice/sort/unstable/heapsort.rs",),
        ("pub(crate) fn heapsort", "unsafe fn sift_down"),
        "reused-accepted-source-transition",
    ),
    _binding(
        RUST_LIBRARY / "core/src/slice/sort/shared/pivot.rs",
        "pivot.rs",
        "pivot-selection",
        ("core/src/slice/sort/shared/pivot.rs",),
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
        "zst-and-sized-type-properties",
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
        "accepted-private-independent-transition",
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
        "independent-private-sort-review",
        ("preservation/path_policy_v5.json",),
        ("**VERDICT: ACCEPT**", "field-complete correspondence"),
        "protected-independent-review",
    ),
    _binding(
        ROOT / "tools/target_079_operational_v1.py",
        "accepted_target_079_operational_v1.py",
        "accepted-key-ord-drop-lifecycle",
        ("review/REVIEW_ADDENDUM_TARGET_079_OPERATIONAL_V1.md",),
        (
            "KeyOrdDropBoundary",
            "drop(right_owned_key)",
            "drop(left_owned_key)",
        ),
        "reused-accepted-lifecycle",
    ),
    _binding(
        TARGET_079_OPERATIONAL / "result.json",
        "accepted_target_079_result.json",
        "accepted-key-lifecycle-result",
        ("review/REVIEW_ADDENDUM_TARGET_079_OPERATIONAL_V1.md",),
        ("target-079-key-ord-drop-operational-v1", '"source_model_complete": true'),
        "protected-accepted-evidence",
    ),
    _binding(
        ROOT / "review/REVIEW_ADDENDUM_TARGET_079_OPERATIONAL_V1.md",
        "accepted_target_079_review.md",
        "independent-key-lifecycle-review",
        ("preservation/path_policy_v3.json",),
        ("**VERDICT: ACCEPT**", "right-key destruction"),
        "protected-independent-review",
    ),
    _binding(
        ROOT / "tools/target_081_operational_v1.py",
        "accepted_target_081_operational_v1.py",
        "accepted-interior-and-panic-before-result-treatment",
        ("review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md",),
        (
            "observable_element_state",
            "less_tested=not observation.panicked",
        ),
        "reused-accepted-state-treatment",
    ),
    _binding(
        TARGET_081_OPERATIONAL / "boundary_manifest.json",
        "accepted_target_081_boundary_manifest.json",
        "accepted-complete-observable-state-boundary",
        ("review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md",),
        (
            "complete element interior-mutation state",
            "drop panic during unwind is modeled as abort",
        ),
        "protected-accepted-evidence",
    ),
    _binding(
        ROOT / "review/REVIEW_ADDENDUM_TARGET_081_OPERATIONAL_V1.md",
        "accepted_target_081_review.md",
        "independent-interior-state-review",
        ("preservation/path_policy_v7.json",),
        ("**VERDICT: ACCEPT**", "less_tested"),
        "protected-independent-review",
    ),
    _binding(
        PATH_POLICY_V7,
        "path_policy_v7.json",
        "accepted-preservation-head",
        ("preservation/path_policy_v7.json",),
        (
            '"policy_id": "slice-preservation-path-policy-v7"',
            "target_081_operational_v1_review",
        ),
        "protected-preservation-head",
    ),
    _binding(
        ROOT / "research/probes/target_082_adapter_probe.rs",
        "target_082_adapter_probe.rs",
        "fresh-rust-process-probe-source",
        ("research/probes/target_082_adapter_probe.rs",),
        ("sort_unstable_by_key", "drop-key-{}", "drop-f"),
        "fresh-ground-truth",
    ),
    _binding(
        EVIDENCE_ROOT / "ground_truth/manifest.json",
        "ground_truth_manifest.json",
        "fresh-rust-process-probe-manifest",
        ("evidence/target_082_operational_v1/ground_truth",),
        ("1.96.0", "key-panic-f-drop-double-panic"),
        "fresh-ground-truth",
    ),
    _binding(
        EVIDENCE_ROOT / "ground_truth/probe.mir",
        "target_082_adapter_probe.mir",
        "fresh-rust-mir",
        ("evidence/target_082_operational_v1/ground_truth/probe.mir",),
        ("sort_unstable_by_key", "drop(_"),
        "fresh-ground-truth",
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
    records = []
    for binding in BINDINGS:
        source = binding["source"]
        destination = binding["destination"]
        if not source.is_file():
            raise RuntimeError(f"bound input is missing: {source}")
        shutil.copyfile(source, destination)
        text = destination.read_text(errors="replace")
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
        "source_model_complete": True,
        "classification_eligible": True,
        "covered_source_phases": list(model.COVERED_SOURCE_PHASES),
        "missing_source_phases": [],
        "bindings": records,
        "trust_site_dispositions": model.boundary_manifest()[
            "trust_site_dispositions"
        ],
        "accepted_models": {
            "private_sort": "target-080-operational-v1-rust-1.96-complete",
            "key_lifecycle": (
                "target-079-key-ord-drop-operational-v1-rust-1.96-complete"
            ),
            "observable_state": (
                "target-081-operational-v1-rust-1.96-complete"
            ),
            "classification_inherited": False,
        },
    }
    common.write_json(SOURCE_BINDINGS, manifest)
    return manifest


def validate_source_bindings() -> dict[str, Any]:
    manifest = json.loads(SOURCE_BINDINGS.read_text())
    if (
        manifest["target"] != model.TARGET
        or manifest["active_contract_sha256"]
        != model.ACTIVE_CONTRACT_SHA256
        or not manifest["source_model_complete"]
        or manifest["missing_source_phases"]
        or len(manifest["bindings"]) != len(BINDINGS)
    ):
        raise RuntimeError("target-082 source binding identity changed")
    by_role = {record["role"]: record for record in manifest["bindings"]}
    if len(by_role) != len(BINDINGS):
        raise RuntimeError("target-082 source binding roles are duplicated")
    for binding in BINDINGS:
        source = binding["source"]
        destination = binding["destination"]
        record = by_role[binding["role"]]
        if (
            source.read_bytes() != destination.read_bytes()
            or _digest(destination) != record["sha256"]
            or _digest(source) != record["origin_sha256"]
        ):
            raise RuntimeError(
                f"target-082 bound source changed: {destination}"
            )
    expected_sites = {
        "TS-082-D001",
        "TS-082-D002",
        "TS-082-D003",
        "TS-082-D004",
        "TS-082-C001",
        "TS-082-E001",
    }
    if (
        set(manifest["trust_site_dispositions"]) != expected_sites
        or set(model.REPLACED_TRUST_SITE_IDS)
        != {"TS-082-D002", "TS-082-D003", "TS-082-E001"}
    ):
        raise RuntimeError("target-082 trust-site closure changed")
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
        "equal-key-exact-output-counterexample": (
            BASELINE / "exact_final_slice_obligation.smt2",
            "sat",
        ),
        "reviewed-equivalence-total-order-projection": (
            BASELINE / "obligation.smt2",
            "unsat",
        ),
    }
    records = {}
    for label, (path, expected) in cases.items():
        before = _digest(path)
        solver = _solver_capture(
            z3, f"retained_{label}", path, expected
        )
        if _digest(path) != before:
            raise RuntimeError(f"retained target-082 SMT mutated: {path}")
        records[label] = {
            "smt": _artifact(path),
            "before_sha256": before,
            "after_sha256": _digest(path),
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
        "equivalence_kind": (
            "exact-terminal-output-and-full-state-operational; "
            "retained-equal-key-reordering-public-equivalence"
        ),
        "baseline_row_mutated": False,
        "certified_projection_mutated": False,
        "operational_v2_overlay_selected": False,
        "manager_stage_mutated": False,
        "evidence_root": _relpath(EVIDENCE_ROOT),
        "independent_review": {
            "required": True,
            "status": "pending",
            "verdict": None,
            "expected_path": _relpath(REVIEW_ADDENDUM),
            "expected_successor_policy": _relpath(REVIEW_POLICY_V9),
        },
    }
    common.write_json(CROSSWALK_JSON, addendum)
    row = {
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
        "source_operational_determinism": operational[
            "source_operational_determinism"
        ],
        "field_complete_source_correspondence": operational[
            "field_complete_source_correspondence"
        ],
        "baseline_row_mutated": "false",
        "certified_projection_mutated": "false",
        "operational_v2_overlay_selected": "false",
        "evidence_root": _relpath(EVIDENCE_ROOT),
    }
    common.write_csv(CROSSWALK_CSV, [row], list(row))
    return {
        "json": _artifact(CROSSWALK_JSON),
        "csv": _artifact(CROSSWALK_CSV),
        "certified_ledger_mutated": False,
    }


def _write_path_policy_v8() -> dict[str, Any]:
    preservation.materialize_historical_argus_archive(root=ROOT)
    v7 = json.loads(PATH_POLICY_V7.read_text())
    v6 = json.loads(
        (ROOT / "preservation/path_policy_v6.json").read_text()
    )
    v6_records = {
        record["path"]: record
        for record in v6["registered_post_v5_additions"][
            "target_081_operational_v1"
        ]["records"]
    }
    mappings = []
    for logical, (version_id, archive_rel) in sorted(
        preservation.ARCHIVE_MAPPINGS.items()
    ):
        if logical not in v6_records:
            raise RuntimeError(f"path_policy_v6 lacks {logical}")
        archive = ROOT / Path(*archive_rel.parts)
        archive_record = _artifact(archive)
        logical_record = v6_records[logical]
        if (
            archive_record["bytes"] != logical_record["bytes"]
            or archive_record["sha256"] != logical_record["sha256"]
        ):
            raise RuntimeError(
                f"target-082 archive does not preserve {logical}"
            )
        mappings.append(
            {
                "version_id": version_id,
                "logical_record": logical_record,
                "archive_record": archive_record,
                "source": f"project-local-archive:accepted-v7/{logical}",
            }
        )

    static_paths = {
        ROOT / "tools/target_082_operational_v1.py",
        ROOT / "tools/target_082_source_interpreter_v1.py",
        ROOT / "tools/target_082_operational_witness_v1.py",
        ROOT / "tools/target_082_operational_smt_v1.py",
        ROOT / "tools/replay_target_082_operational_v1.py",
        ROOT / "tools/run_target_082_ground_truth.py",
        ROOT / "tools/run_target_082_operational_v1.py",
        ROOT / "tools/preservation_policy_v8.py",
        ROOT / "tools/preservation_policy_v3.py",
        ROOT / "tools/run_target_081_operational_v1.py",
        ROOT / "tools/operational_v2_reconciliation.py",
        ROOT / "tools/run_acceptance.py",
        ROOT / "tools/build_authority_design.py",
        ROOT / "tests/test_target_082_operational_v1.py",
        ROOT / "tests/test_target_082_operational_artifacts_v1.py",
        ROOT / "tests/test_preservation_policy_v8.py",
        ROOT / "tests/test_acceptance_timeout.py",
        ROOT / "tests/test_target_081_operational_artifacts_v1.py",
        ROOT / "tests/test_operational_v2_reconciliation.py",
        ROOT / "research/probes/target_082_adapter_probe.rs",
        SOURCE_PROOF,
        CROSSWALK_JSON,
        CROSSWALK_CSV,
        WIKI_INDEX,
        WIKI_PAGE,
        *{
            ROOT / Path(*archive.parts)
            for _, archive in preservation.ARCHIVE_MAPPINGS.values()
        },
        *{
            ROOT / Path(*archive.parts)
            for _, archive in (
                preservation.HISTORICAL_ARCHIVE_MAPPINGS.values()
            )
        },
    }
    evidence_paths = {
        path for path in EVIDENCE_ROOT.rglob("*") if path.is_file()
    }
    records = []
    for path in sorted(static_paths | evidence_paths):
        if not path.is_file():
            raise RuntimeError(f"path_policy_v8 input is missing: {path}")
        records.append(_artifact(path))
    payload = {
        "schema_version": 1,
        "policy_id": preservation.POLICY_ID,
        "parent_policy_id": preservation.PARENT_POLICY_ID,
        "parent_policy": _artifact(PATH_POLICY_V7),
        "policy": (
            "path_policy_v7 remains authoritative and byte-identical. "
            "This fail-closed successor registers the target-082 "
            "operational-v1 Engineer package and resolves every changed "
            "v6-bound live path only through an explicit project-local "
            "archive mapping. Independent acceptance belongs only in v9."
        ),
        "archive_resolution": {
            "schema_version": 1,
            "archive_root": preservation.ARCHIVE_ROOT.as_posix(),
            "record_version_mappings": mappings,
            "historical_record_version_mappings": (
                preservation.historical_mapping_records(root=ROOT)
            ),
        },
        "registered_post_v7_additions": {
            preservation.TARGET_082_ADDITION: {
                "file_count": len(records),
                "records": records,
            }
        },
        "independent_review_lane": {
            "status": "pending",
            "expected_policy_id": preservation.V9_POLICY_ID,
            "expected_policy_path": "preservation/path_policy_v9.json",
            "expected_verdict_path": (
                "review/REVIEW_ADDENDUM_TARGET_082_OPERATIONAL_V1.md"
            ),
        },
    }
    common.write_json(PATH_POLICY_V8, payload)
    preservation.validate_policy(root=ROOT)
    if v7 != json.loads(PATH_POLICY_V7.read_text()):
        raise RuntimeError("path_policy_v7 changed while writing v8")
    return _artifact(PATH_POLICY_V8)


def main() -> int:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for target-082 evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if not SOURCE_PROOF.is_file():
        raise RuntimeError(f"Verus proof is missing: {SOURCE_PROOF}")

    protected_trees = {
        "certified_target_082": BASELINE,
        "frozen_target_082": FROZEN_IMPLPROOF,
        "accepted_target_079": TARGET_079_OPERATIONAL,
        "accepted_target_080": TARGET_080_OPERATIONAL,
        "accepted_target_081": TARGET_081_OPERATIONAL,
        "operational_v2_certification": (
            ROOT / "evidence/final_campaign/operational_v2"
        ),
        "review_tree": ROOT / "review",
    }
    protected_files = {
        "ledger_csv": ROOT / "crosswalk/target_to_proof_boundary.csv",
        "ledger_json": ROOT / "crosswalk/target_to_proof_boundary.json",
        "pipeline_state": ROOT / "research/PIPELINE_STATE.json",
        **{
            f"path_policy_v{version}": (
                ROOT / f"preservation/path_policy_v{version}.json"
            )
            for version in range(1, 8)
        },
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
    ground_replay = target_pipeline.capture_command(
        EVIDENCE_ROOT / "ground_truth_replay",
        [sys.executable, str(ROOT / "tools/run_target_082_ground_truth.py")],
        cwd=ROOT,
        timeout=120,
    )
    target_pipeline.require_clean_result(
        ground_replay,
        "captured target-082 key-sort ground truth: 14 scenarios",
        label="target-082-ground-truth",
    )
    ground_manifest = json.loads(
        (EVIDENCE_ROOT / "ground_truth/manifest.json").read_text()
    )
    if (
        len(ground_manifest["scenarios"]) != 14
        or "1.96.0" not in ground_manifest["toolchain"]
    ):
        raise RuntimeError("target-082 Rust ground truth is incomplete")

    manifest = materialize_bound_inputs()
    validate_source_bindings()
    common.write_json(BOUNDARY_MANIFEST, model.boundary_manifest())

    payload = witnesses.witness_payload()
    common.write_json(WITNESS, payload)
    witness_capture = target_pipeline.capture_command(
        EVIDENCE_ROOT / "witness_replay",
        [
            sys.executable,
            str(ROOT / "tools/replay_target_082_operational_v1.py"),
            "--witness",
            str(WITNESS),
        ],
        cwd=ROOT,
        timeout=120,
    )
    witness_stdout = (ROOT / witness_capture["stdout"]).read_text()
    if (
        witness_capture["exit_code"] != 0
        or (ROOT / witness_capture["stderr"]).read_text()
    ):
        raise RuntimeError("target-082 witness replay failed")
    witness_result = json.loads(witness_stdout)
    if witness_result.get("status") != "passed":
        raise RuntimeError("target-082 witnesses did not pass")
    witness_capture["result"] = witness_result

    obligations = {
        smt.PRIVATE_SOURCE: _write_obligation(
            z3, "private_source_correspondence", smt.PRIVATE_SOURCE
        ),
        smt.ADAPTER_SOURCE: _write_obligation(
            z3, "adapter_source_correspondence", smt.ADAPTER_SOURCE
        ),
        smt.FIXED_BOUNDARY: _write_obligation(
            z3,
            "fixed_boundary_exact_terminal_output_full_state",
            smt.FIXED_BOUNDARY,
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
    composition_regressions = {}
    for kind, expected in smt.COMPOSITION_REGRESSION_EXPECTATIONS.items():
        stem = f"composition_{kind}"
        path = EVIDENCE_ROOT / f"{stem}.smt2"
        path.write_text(smt.composition_regression_text(kind))
        composition_regressions[kind] = {
            "smt": _artifact(path),
            "solver": _solver_capture(z3, stem, path, expected),
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
    correspondence_mutations = {}
    for kind in smt.CORRESPONDENCE_MUTATION_KINDS:
        stem = f"correspondence_mutation_{kind}"
        path = EVIDENCE_ROOT / f"{stem}.smt2"
        path.write_text(smt.correspondence_mutation_text(kind))
        correspondence_mutations[kind] = {
            "mutated_side": "source-only",
            "smt": _artifact(path),
            "solver": _solver_capture(z3, stem, path, "sat"),
        }
    retained = _replay_retained_classifications(z3)

    captured_proof = EVIDENCE_ROOT / "verus/key_sort_model.rs"
    captured_proof.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_PROOF, captured_proof)
    proof_text = captured_proof.read_text()
    for forbidden in (
        "external_body",
        "assume(",
        "admit(",
        "axiom",
        "precomputed_terminal",
    ):
        if forbidden in proof_text:
            raise RuntimeError(
                f"trusted-free target-082 proof contains {forbidden!r}"
            )
    for required in (
        "source_key_ord_drop_adapter",
        "AcceptedTarget080PrivateTransition",
        "accepted_private_source_transition",
        "fixed_boundary_accepted_transition_is_deterministic",
        "first.apply == second.apply",
        "observable_element_state",
    ):
        if required not in proof_text:
            raise RuntimeError(
                f"target-082 Verus proof lacks {required}"
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
        raise RuntimeError("target-082 Verus proof did not type-check")
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
        raise RuntimeError("target-082 Verus proof did not verify")

    tree_after = {
        name: _tree_digest(path) for name, path in protected_trees.items()
    }
    file_after = {
        name: _digest(path) for name, path in protected_files.items()
    }
    if tree_before != tree_after or file_before != file_after:
        raise RuntimeError("target-082 runner mutated protected evidence")

    crosswalk = _write_crosswalk_addendum()
    result = {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "artifact_id": "target_082_operational_v1",
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "status": "engineer-complete-review-pending",
        "source_model_complete": True,
        "classification_eligible": True,
        "covered_source_phases": list(model.COVERED_SOURCE_PHASES),
        "missing_source_phases": [],
        "unresolved_source_model_phases": [],
        "classification": {
            "source_operational_determinism": "conditional-complete",
            "field_complete_source_correspondence": "conditional-complete",
        },
        "classification_scope": (
            "additive source-operational result only; certified target-082 "
            "exact-output and reviewed-equivalence classifications remain "
            "unchanged"
        ),
        "certified_baseline_classification": BASELINE_CLASSIFICATION,
        "certified_baseline_classification_mutated": False,
        "source_bindings": _artifact(SOURCE_BINDINGS),
        "boundary_manifest": _artifact(BOUNDARY_MANIFEST),
        "trust_site_dispositions": manifest["trust_site_dispositions"],
        "ground_truth": {
            "manifest": _artifact(
                EVIDENCE_ROOT / "ground_truth/manifest.json"
            ),
            "mir": _artifact(EVIDENCE_ROOT / "ground_truth/probe.mir"),
            "scenario_count": len(ground_manifest["scenarios"]),
            "toolchain": ground_manifest["toolchain"],
            "capture": ground_replay,
        },
        "independent_interpreter": {
            "path": "tools/target_082_source_interpreter_v1.py",
            "case_count": payload["case_count"],
            "field_complete_correspondence": True,
            "normal_panic_abort_correspondence": True,
            "full_observable_state_correspondence": True,
        },
        "witness": _artifact(WITNESS),
        "witness_replay": witness_capture,
        "obligations": obligations,
        "nonvacuity": nonvacuity,
        "branch_force_probes": probes,
        "abort_preserving_composition_regressions": (
            composition_regressions
        ),
        "semantic_mutation_regressions": mutations,
        "correspondence_mutation_regressions": (
            correspondence_mutations
        ),
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
                    "SourceAdapterBinding",
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
            "certified_projection_62_rows_unchanged": True,
            "operational_v2_overlay_counts_unchanged": True,
            "policies_v1_through_v7_unchanged": True,
            "manager_state_unchanged": True,
        },
        "independent_review": {
            "required": True,
            "status": "pending",
            "verdict": None,
            "expected_addendum": _relpath(REVIEW_ADDENDUM),
            "engineer_policy": _relpath(PATH_POLICY_V8),
            "expected_review_policy": _relpath(REVIEW_POLICY_V9),
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
            "witness_count": payload["case_count"],
            "ground_truth_scenario_count": len(
                ground_manifest["scenarios"]
            ),
            "branch_force_probe_count": len(probes),
            "composition_regression_count": len(
                composition_regressions
            ),
            "semantic_mutation_count": (
                len(mutations) + len(correspondence_mutations)
            ),
            "correspondence_mutation_count": len(
                correspondence_mutations
            ),
            "independent_review": result["independent_review"],
        },
    )
    policy = _write_path_policy_v8()
    print(
        json.dumps(
            {
                "status": result["status"],
                "target": model.TARGET,
                "witness_count": payload["case_count"],
                "ground_truth_scenarios": len(
                    ground_manifest["scenarios"]
                ),
                "obligations": {
                    purpose: item["solver"]["solver_result"]
                    for purpose, item in obligations.items()
                },
                "nonvacuity": nonvacuity["solver"]["solver_result"],
                "branch_force_probes": len(probes),
                "composition_regressions": {
                    name: item["solver"]["solver_result"]
                    for name, item in composition_regressions.items()
                },
                "semantic_mutations": (
                    len(mutations) + len(correspondence_mutations)
                ),
                "correspondence_mutations": len(
                    correspondence_mutations
                ),
                "retained_classifications": {
                    name: item["solver"]["solver_result"]
                    for name, item in retained.items()
                },
                "verus": EXPECTED_VERUS_SUMMARY,
                "path_policy_v8": policy,
                "independent_review": "pending",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
