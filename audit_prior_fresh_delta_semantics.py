#!/usr/bin/env python3
"""Audit semantic adequacy of prior-vs-fresh final-decision changes."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

import audit_final_skip_rationales


CANONICAL_FRESH_ROOT = Path(
    "/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06"
    "/specgen/all-2121-gpt56sol-fresh-20260806-0453"
)

EXPECTED_DECISION_CHANGES = 147
EXPECTED_PRIOR_ADD_FRESH_SKIP = 117
EXPECTED_PRIOR_SKIP_FRESH_ADD = 30
EXPECTED_FRESH_ACCEPTED = 127
EXPECTED_FRESH_SKIP = 1994

AUDIT_FIELDS = [
    "target",
    "transition",
    "fresh_category",
    "fresh_final_decision",
    "rationale_taxonomy",
    "taxonomy_source_fields",
    "taxonomy_source_backed",
    "adequacy_verdict",
    "adequacy_notes",
    "unjustified_change",
    "change_direction",
    "fresh_issues_combined",
    "fresh_rationale",
    "fresh_requires",
    "fresh_requires_source_fidelity_classification",
    "fresh_requires_source_reference",
    "fresh_requires_source_excerpt",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fresh-root",
        type=Path,
        default=CANONICAL_FRESH_ROOT,
        help="Canonical fresh specgen output root.",
    )
    parser.add_argument(
        "--decision-changes",
        type=Path,
        help="Override path to prior_fresh_delta/decision_changes.csv.",
    )
    parser.add_argument(
        "--final-verification",
        type=Path,
        help="Override path to final_verification.json.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        help="Directory for semantic audit artifacts; defaults to prior_fresh_delta.",
    )
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def bool_value(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def int_value(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def split_tags(*values: str) -> list[str]:
    tags: list[str] = []
    seen: set[str] = set()
    for value in values:
        for tag in str(value or "").split(";"):
            tag = tag.strip()
            if tag and tag not in seen:
                seen.add(tag)
                tags.append(tag)
    return tags


def one_line(value: str, limit: int = 500) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def fresh_tags(row: dict[str, str]) -> list[str]:
    return split_tags(
        row.get("fresh_issues", ""),
        row.get("fresh_semantic_gate_issues", ""),
        row.get("fresh_semantic_review_issues", ""),
    )


def classify_downgrade(row: dict[str, str], tags: set[str]) -> tuple[str, str]:
    rationale = str(row.get("fresh_rationale") or "").lower()
    if "duplicate_vstd_assume_specification" in tags:
        return (
            "duplicate_existing_vstd_spec",
            "fresh issue tags identify an existing trusted vstd "
            "assume_specification for the exact API target",
        )
    if (
        "classification:higher_order_contract" in tags
        or any(tag.startswith("higher_order_closure_") for tag in tags)
    ):
        return (
            "higher_order_behavior_unmodeled",
            "fresh issue tags identify higher-order closure or predicate behavior "
            "that the public model cannot observe completely",
        )
    if (
        "classification:unsafe_or_representation_sensitive" in tags
        or "raw_pointer_representation_contract" in tags
    ):
        return (
            "unsafe_or_representation_sensitive",
            "fresh issue tags identify unsafe representation, provenance, or raw "
            "pointer behavior that would be trusted as an axiom",
        )
    if "classification:runtime_or_hidden_state" in tags:
        return (
            "runtime_or_hidden_state",
            "fresh issue tags identify OS, runtime, synchronization, or hidden "
            "state effects outside the public vstd model",
        )
    if "classification:ownership_or_uninitialized_model" in tags:
        return (
            "ownership_or_uninitialized_model_gap",
            "fresh issue tags identify ownership or MaybeUninit state that is not "
            "modeled by available public views",
        )
    if "classification:representation_or_allocator" in tags:
        return (
            "representation_or_allocator_model_gap",
            "fresh issue tags identify allocator capacity or container "
            "representation facts rather than stable semantic outputs",
        )
    if "value_unspecified_after_exhaustion" in tags:
        return (
            "source_unspecified_after_exhaustion",
            "fresh issue tags identify APIs whose post-exhaustion value is "
            "intentionally unspecified",
        )
    if "classification:associated_type_or_projection" in tags:
        return (
            "associated_type_or_projection_gap",
            "fresh issue tags identify generic associated-type or projection "
            "results without an available public relation",
        )
    if "classification:formatting_effect" in tags:
        return (
            "formatting_effect_unmodeled",
            "fresh issue tags identify formatter side effects rather than a pure "
            "modeled result relation",
        )
    if "classification:trait_contract_integration" in tags:
        return (
            "trait_contract_integration_gap",
            "fresh issue tags identify trait-method semantics that would require "
            "integration with trait-level contracts",
        )
    if "classification:needs_new_vstd_abstraction" in tags:
        return (
            "needs_new_vstd_abstraction",
            "fresh issue tags identify a source fact that needs new shared vstd "
            "vocabulary before it can be expressed non-vacuously",
        )
    if "classification:complex_result_or_pattern_model" in tags:
        return (
            "complex_result_or_pattern_model_gap",
            "fresh issue tags identify string or pattern result semantics that "
            "lack a complete public model",
        )
    if "public_api_allows_any_matching_index" in tags:
        return (
            "public_api_allows_multiple_results",
            "fresh issue tags identify an API that may return any matching index, "
            "so the prior singleton result relation was too strong",
        )
    if "clone" in rationale or "cloning" in rationale:
        return (
            "clone_semantics_unmodeled",
            "fresh rationale identifies Clone behavior with no public equality or "
            "view-preservation guarantee for arbitrary T",
        )
    if "borrowed-key" in rationale or "borrowed key" in rationale:
        return (
            "borrowed_key_model_underdetermined",
            "fresh rationale identifies borrowed-key lookup semantics that cannot "
            "select a unique stored key with existing predicates",
        )
    if "determinism_unsupported_contract_form" in tags:
        return (
            "determinism_unsupported_contract_form",
            "fresh determinism feedback rejected the modeled contract form and no "
            "more specific issue tag was emitted",
        )
    return ("unclassified", "no normalized fresh issue tag was available")


def classify_upgrade(row: dict[str, str]) -> tuple[str, str]:
    target = row["target"]
    requires = str(row.get("fresh_requires") or "").strip()
    requires_class = str(
        row.get("fresh_requires_source_fidelity_classification") or ""
    ).strip()
    if requires and requires_class == "source_justified":
        return (
            "accepted_source_justified_precondition",
            "fresh accepted contract has a non-empty requires clause with "
            "source-fidelity reference and excerpt",
        )
    if target.startswith("core::slice::") or target.startswith("core::array::"):
        return (
            "accepted_slice_array_view_contract",
            "fresh accepted contract exposes source-documented slice or array view "
            "semantics without extra preconditions",
        )
    if target.startswith("core::str::"):
        return (
            "accepted_string_view_contract",
            "fresh accepted contract exposes source-documented string byte or UTF-8 "
            "semantics without extra preconditions",
        )
    if target == "std::thread::Result::flatten":
        return (
            "accepted_enum_result_forwarding_contract",
            "fresh accepted contract is a pure source-level forwarding relation "
            "over nested Result values",
        )
    return (
        "accepted_collection_lookup_or_conversion_contract",
        "fresh accepted contract exposes stable collection lookup or conversion "
        "semantics with no semantic-gate issues",
    )


def source_evidence_fields(
    row: dict[str, str],
    tags: list[str],
    *,
    manifest_source_context: bool,
) -> list[str]:
    fields: list[str] = []
    if tags:
        fields.append("fresh_issue_tags")
    if str(row.get("fresh_rationale") or "").strip():
        fields.append("fresh_rationale")
    if str(row.get("fresh_requires_source_reference") or "").strip():
        fields.append("fresh_requires_source_reference")
    if str(row.get("fresh_requires_source_excerpt") or "").strip():
        fields.append("fresh_requires_source_excerpt")
    if str(row.get("fresh_requires_source_fidelity_rationale") or "").strip():
        fields.append("fresh_requires_source_fidelity_rationale")
    if manifest_source_context:
        fields.append("manifest_source_context")
    return fields


def audit_row(
    row: dict[str, str],
    manifest_entries: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    transition = row["transition"]
    tags = fresh_tags(row)
    normalized_tags = audit_final_skip_rationales.recognized_issue_tags(tags)
    tag_set = set(tags)
    if transition == "add_spec->skip":
        taxonomy, taxonomy_reason = classify_downgrade(row, tag_set)
        direction = "downgrade"
    elif transition == "skip->add_spec":
        taxonomy, taxonomy_reason = classify_upgrade(row)
        direction = "upgrade"
    else:
        taxonomy = "unclassified"
        taxonomy_reason = f"unsupported transition {transition!r}"
        direction = "other"

    manifest_source_context = audit_final_skip_rationales.manifest_has_source_evidence(
        manifest_entries,
        row["target"],
    )
    evidence_fields = source_evidence_fields(
        row,
        normalized_tags,
        manifest_source_context=manifest_source_context,
    )
    problems: list[str] = []

    if taxonomy == "unclassified":
        problems.append(taxonomy_reason)

    if transition == "add_spec->skip":
        if row.get("fresh_final_decision") != "skip":
            problems.append("fresh final decision is not skip")
        if not str(row.get("fresh_rationale") or "").strip():
            problems.append("fresh skip rationale is empty")
        if (
            str(row.get("fresh_requires_source_fidelity_classification") or "").strip()
            != "not_applicable"
        ):
            problems.append("fresh skip has unexpected requires source-fidelity class")
        source_backed = (
            bool(normalized_tags)
            and manifest_source_context
            and taxonomy != "unclassified"
        )
        if not source_backed:
            problems.append("downgrade taxonomy is not source-backed")
        verdict = (
            "adequate_source_backed_skip"
            if not problems
            else "unjustified_downgrade"
        )
    elif transition == "skip->add_spec":
        requires = str(row.get("fresh_requires") or "").strip()
        requires_class = str(
            row.get("fresh_requires_source_fidelity_classification") or ""
        ).strip()
        requires_reference = str(
            row.get("fresh_requires_source_reference") or ""
        ).strip()
        requires_excerpt = str(row.get("fresh_requires_source_excerpt") or "").strip()
        if row.get("fresh_final_decision") != "add_spec":
            problems.append("fresh final decision is not add_spec")
        if not bool_value(row.get("fresh_typecheck_passed", "")):
            problems.append("fresh accepted row did not typecheck")
        if int_value(row.get("fresh_guarded_reward")) != 1:
            problems.append("fresh accepted row is not guarded deterministic")
        if int_value(row.get("fresh_semantic_guarded_reward")) != 1:
            problems.append("fresh accepted row failed semantic reward")
        if tags:
            problems.append("fresh accepted row has issue tags")
        if requires:
            if requires_class != "source_justified":
                problems.append("non-empty fresh requires is not source-justified")
            if not requires_reference:
                problems.append("non-empty fresh requires lacks source reference")
            if not requires_excerpt:
                problems.append("non-empty fresh requires lacks source excerpt")
        elif requires_class not in {"not_applicable", ""}:
            problems.append("empty fresh requires has unexpected source-fidelity class")
        source_backed = (
            manifest_source_context
            and taxonomy != "unclassified"
            and (
                not requires
                or (
                    requires_class == "source_justified"
                    and bool(requires_reference)
                    and bool(requires_excerpt)
                )
            )
        )
        if not source_backed:
            problems.append("upgrade taxonomy is not source-backed")
        verdict = (
            "adequate_source_backed_add_spec"
            if not problems
            else "unjustified_upgrade"
        )
    else:
        source_backed = False
        verdict = "unsupported_transition"
        problems.append("unsupported transition")

    return {
        "target": row["target"],
        "transition": transition,
        "fresh_category": row.get("fresh_category", ""),
        "fresh_final_decision": row.get("fresh_final_decision", ""),
        "rationale_taxonomy": taxonomy,
        "taxonomy_source_fields": ";".join(evidence_fields),
        "taxonomy_source_backed": str(source_backed).lower(),
        "adequacy_verdict": verdict,
        "adequacy_notes": taxonomy_reason
        if not problems
        else "; ".join([taxonomy_reason, *problems]),
        "unjustified_change": str(bool(problems)).lower(),
        "change_direction": direction,
        "fresh_issues_combined": ";".join(tags),
        "fresh_rationale": one_line(row.get("fresh_rationale", ""), 1200),
        "fresh_requires": row.get("fresh_requires", ""),
        "fresh_requires_source_fidelity_classification": row.get(
            "fresh_requires_source_fidelity_classification", ""
        ),
        "fresh_requires_source_reference": row.get(
            "fresh_requires_source_reference", ""
        ),
        "fresh_requires_source_excerpt": one_line(
            row.get("fresh_requires_source_excerpt", ""), 1200
        ),
    }


def verification_checks(final_verification: dict[str, Any]) -> dict[str, bool]:
    final_decisions = final_verification.get("final_decision_counts", {})
    candidate_counts = final_verification.get("candidate_decision_counts", {})
    skip_rationale = final_verification.get("skip_rationale", {})
    return {
        "final_verification_2121_targets": (
            final_verification.get("manifest_targets") == 2121
            and final_verification.get("result_rows") == 2121
            and final_verification.get("final_candidates") == 2121
        ),
        f"final_verification_{EXPECTED_FRESH_ACCEPTED}_accepted": (
            candidate_counts.get("accepted_semantic_candidates")
            == EXPECTED_FRESH_ACCEPTED
            and final_decisions.get("add_spec") == EXPECTED_FRESH_ACCEPTED
        ),
        f"final_verification_{EXPECTED_FRESH_SKIP}_skips": final_decisions.get("skip")
        == EXPECTED_FRESH_SKIP,
        "final_verification_zero_missing_extra_duplicates": (
            final_verification.get("missing_target_count") == 0
            and final_verification.get("extra_target_count") == 0
            and final_verification.get("duplicate_result_count") == 0
        ),
        "final_verification_skip_rationales_non_empty": (
            skip_rationale.get("empty_skip_rationale_rows") == 0
        ),
    }


def build_summary(
    decision_changes_path: Path,
    final_verification_path: Path,
    audit_rows: list[dict[str, Any]],
    final_verification: dict[str, Any],
) -> dict[str, Any]:
    transition_counts = Counter(row["transition"] for row in audit_rows)
    taxonomy_counts = Counter(row["rationale_taxonomy"] for row in audit_rows)
    adequacy_counts = Counter(row["adequacy_verdict"] for row in audit_rows)
    unclassified = [
        row["target"]
        for row in audit_rows
        if row["rationale_taxonomy"] == "unclassified"
    ]
    unjustified = [
        row["target"] for row in audit_rows if row["unjustified_change"] == "true"
    ]
    downgrades = [
        row for row in audit_rows if row["transition"] == "add_spec->skip"
    ]
    upgrades = [row for row in audit_rows if row["transition"] == "skip->add_spec"]
    checks = {
        f"decision_change_rows_{EXPECTED_DECISION_CHANGES}": (
            len(audit_rows) == EXPECTED_DECISION_CHANGES
        ),
        f"classified_rows_{EXPECTED_DECISION_CHANGES}": (
            len(audit_rows) == EXPECTED_DECISION_CHANGES
        )
        and not unclassified,
        "unclassified_rows_zero": not unclassified,
        f"add_spec_to_skip_rows_{EXPECTED_PRIOR_ADD_FRESH_SKIP}": len(downgrades)
        == EXPECTED_PRIOR_ADD_FRESH_SKIP,
        "add_spec_to_skip_all_have_fresh_rationale": all(
            str(row["fresh_rationale"]).strip() for row in downgrades
        ),
        "add_spec_to_skip_all_source_backed_verdicts": all(
            row["taxonomy_source_backed"] == "true"
            and row["adequacy_verdict"] == "adequate_source_backed_skip"
            for row in downgrades
        ),
        f"skip_to_add_spec_rows_{EXPECTED_PRIOR_SKIP_FRESH_ADD}": len(upgrades)
        == EXPECTED_PRIOR_SKIP_FRESH_ADD,
        "skip_to_add_spec_all_remain_accepted": all(
            row["adequacy_verdict"] == "adequate_source_backed_add_spec"
            for row in upgrades
        ),
        "skip_to_add_spec_issues_empty": all(
            not row["fresh_issues_combined"] for row in upgrades
        ),
        "skip_to_add_spec_requires_source_justified_where_present": all(
            (
                not str(row["fresh_requires"]).strip()
                and row["fresh_requires_source_fidelity_classification"]
                in {"not_applicable", ""}
            )
            or (
                bool(str(row["fresh_requires"]).strip())
                and row["fresh_requires_source_fidelity_classification"]
                == "source_justified"
                and bool(str(row["fresh_requires_source_reference"]).strip())
                and bool(str(row["fresh_requires_source_excerpt"]).strip())
            )
            for row in upgrades
        ),
        "unjustified_downgrade_rows_zero": not any(
            row["unjustified_change"] == "true"
            for row in downgrades
        ),
        "unjustified_upgrade_rows_zero": not any(
            row["unjustified_change"] == "true"
            for row in upgrades
        ),
        "unjustified_change_rows_zero": not unjustified,
    }
    checks.update(verification_checks(final_verification))
    return {
        "schema_version": 1,
        "generated_at_utc": utc_now(),
        "inputs": {
            "decision_changes_csv": str(decision_changes_path.resolve()),
            "final_verification_json": str(final_verification_path.resolve()),
        },
        "counts": {
            "rows": len(audit_rows),
            "transition_counts": dict(sorted(transition_counts.items())),
            "taxonomy_counts": dict(sorted(taxonomy_counts.items())),
            "adequacy_counts": dict(sorted(adequacy_counts.items())),
            "unclassified_rows": len(unclassified),
            "unjustified_change_rows": len(unjustified),
            "unjustified_downgrade_rows": sum(
                row["unjustified_change"] == "true"
                for row in downgrades
            ),
            "unjustified_upgrade_rows": sum(
                row["unjustified_change"] == "true" for row in upgrades
            ),
        },
        "unclassified_targets": unclassified,
        "unjustified_change_targets": unjustified,
        "acceptance_checks": checks,
        "acceptance_passed": all(checks.values()),
    }


def write_report(path: Path, summary: dict[str, Any], artifacts: dict[str, str]) -> None:
    counts = summary["counts"]
    checks = summary["acceptance_checks"]
    lines = [
        "# Prior vs Fresh Semantic Taxonomy Audit",
        "",
        f"Generated at UTC `{summary['generated_at_utc']}`.",
        "",
        "This reproducible audit classifies every row in "
        "`prior_fresh_delta/decision_changes.csv` using fresh issue tags, "
        "fresh final-candidate rationales, and requires source-fidelity "
        "references/excerpts where a fresh accepted contract has preconditions.",
        "",
        "## Counts",
        "",
        "| Measure | Value |",
        "| --- | ---: |",
        f"| changed rows | {counts['rows']} |",
        f"| unclassified rows | {counts['unclassified_rows']} |",
        f"| unjustified change rows | {counts['unjustified_change_rows']} |",
        f"| unjustified downgrades | {counts['unjustified_downgrade_rows']} |",
        f"| unjustified upgrades | {counts['unjustified_upgrade_rows']} |",
        "",
        "## Transition Counts",
        "",
        "| Transition | Rows |",
        "| --- | ---: |",
    ]
    for key, value in counts["transition_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Taxonomy Counts", "", "| Taxonomy | Rows |", "| --- | ---: |"])
    for key, value in counts["taxonomy_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Acceptance Checks",
            "",
            "| Check | Passed |",
            "| --- | --- |",
        ]
    )
    for key, value in checks.items():
        lines.append(f"| `{key}` | `{str(value).lower()}` |")
    lines.extend(["", "## Artifacts", ""])
    for name, artifact_path in artifacts.items():
        lines.append(f"- `{name}`: `{artifact_path}`")
    path.write_text("\n".join(lines).rstrip() + "\n")


def main() -> int:
    args = parse_args()
    fresh_root = args.fresh_root.expanduser().resolve()
    delta_dir = fresh_root / "prior_fresh_delta"
    decision_changes_path = (
        args.decision_changes.expanduser().resolve()
        if args.decision_changes
        else delta_dir / "decision_changes.csv"
    )
    final_verification_path = (
        args.final_verification.expanduser().resolve()
        if args.final_verification
        else fresh_root / "final_verification.json"
    )
    out_dir = (
        args.out_dir.expanduser().resolve() if args.out_dir else delta_dir.resolve()
    )

    source_rows = read_csv(decision_changes_path)
    manifest_entries = audit_final_skip_rationales.load_manifest_entries(
        fresh_root,
        None,
    )
    audit_rows = [audit_row(row, manifest_entries) for row in source_rows]
    final_verification = json.loads(final_verification_path.read_text())
    summary = build_summary(
        decision_changes_path,
        final_verification_path,
        audit_rows,
        final_verification,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "semantic_taxonomy_audit.csv"
    summary_path = out_dir / "semantic_taxonomy_summary.json"
    report_path = out_dir / "SEMANTIC_TAXONOMY_AUDIT.md"
    artifacts = {
        "semantic_taxonomy_audit.csv": str(csv_path.resolve()),
        "semantic_taxonomy_summary.json": str(summary_path.resolve()),
        "SEMANTIC_TAXONOMY_AUDIT.md": str(report_path.resolve()),
    }
    summary["artifacts"] = artifacts

    write_csv(csv_path, audit_rows, AUDIT_FIELDS)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_report(report_path, summary, artifacts)

    counts = summary["counts"]
    print(
        f"audited {counts['rows']} rows; "
        f"unclassified={counts['unclassified_rows']} "
        f"unjustified={counts['unjustified_change_rows']}"
    )
    return 0 if summary["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
