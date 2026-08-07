#!/usr/bin/env python3
"""Regenerate the canonical prior-vs-fresh final-decision delta audit."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


DEFAULT_PRIOR_ROOT = Path(
    "/home/chentianyu/nanvix-rust-std-spec-survey/specgen/all-2121-gpt56sol"
)
DEFAULT_FRESH_ROOT = Path(
    "/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06"
    "/specgen/all-2121-gpt56sol-fresh-20260806-0453"
)

EXPECTED_DECISION_CHANGES = 147
EXPECTED_PRIOR_ADD_FRESH_SKIP = 117
EXPECTED_PRIOR_SKIP_FRESH_ADD = 30
EXPECTED_FRESH_ACCEPTED = 127
EXPECTED_FRESH_SKIP = 1994

DELTA_FIELDS = [
    "target",
    "transition",
    "prior_category",
    "fresh_category",
    "prior_status",
    "fresh_status",
    "prior_rounds",
    "fresh_rounds",
    "prior_initial_decision",
    "fresh_initial_decision",
    "prior_final_decision",
    "fresh_final_decision",
    "prior_contract_form",
    "fresh_contract_form",
    "prior_typecheck_passed",
    "fresh_typecheck_passed",
    "prior_det_status",
    "fresh_det_status",
    "prior_r0_z3",
    "fresh_r0_z3",
    "prior_classification",
    "fresh_classification",
    "prior_raw_det_reward",
    "fresh_raw_det_reward",
    "prior_guarded_reward",
    "fresh_guarded_reward",
    "prior_semantic_guarded_reward",
    "fresh_semantic_guarded_reward",
    "prior_issues",
    "fresh_issues",
    "prior_semantic_gate_issues",
    "fresh_semantic_gate_issues",
    "prior_semantic_review_issues",
    "fresh_semantic_review_issues",
    "prior_requires",
    "fresh_requires",
    "prior_ensures",
    "fresh_ensures",
    "prior_rationale",
    "fresh_rationale",
    "prior_requires_source_fidelity_classification",
    "fresh_requires_source_fidelity_classification",
    "prior_requires_source_fidelity_rationale",
    "fresh_requires_source_fidelity_rationale",
    "prior_requires_source_reference",
    "fresh_requires_source_reference",
    "prior_requires_source_excerpt",
    "fresh_requires_source_excerpt",
    "prior_contract_code",
    "fresh_contract_code",
]

ROW_FIELDS = [
    "category",
    "status",
    "rounds",
    "initial_decision",
    "final_decision",
    "contract_form",
    "typecheck_passed",
    "det_status",
    "r0_z3",
    "classification",
    "raw_det_reward",
    "guarded_reward",
    "semantic_guarded_reward",
    "issues",
    "semantic_gate_issues",
    "semantic_review_issues",
    "requires",
    "ensures",
    "rationale",
    "requires_source_fidelity_classification",
    "requires_source_fidelity_rationale",
    "requires_source_reference",
    "requires_source_excerpt",
    "contract_code",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prior-root",
        type=Path,
        default=DEFAULT_PRIOR_ROOT,
        help="Prior specgen output root with final_candidates.csv.",
    )
    parser.add_argument(
        "--fresh-root",
        type=Path,
        default=DEFAULT_FRESH_ROOT,
        help="Fresh canonical specgen output root with final_candidates.csv.",
    )
    parser.add_argument(
        "--final-verification",
        type=Path,
        help="Fresh final_verification.json; defaults to FRESH_ROOT/final_verification.json.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        help="Output directory; defaults to FRESH_ROOT/prior_fresh_delta.",
    )
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def rows_by_target(rows: list[dict[str, str]], path: Path) -> dict[str, dict[str, str]]:
    by_target: dict[str, dict[str, str]] = {}
    duplicates: list[str] = []
    for row in rows:
        target = row.get("target", "")
        if target in by_target:
            duplicates.append(target)
        by_target[target] = row
    if duplicates:
        joined = ", ".join(sorted(set(duplicates))[:10])
        raise ValueError(f"{path} has duplicate target rows: {joined}")
    return by_target


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def count_decisions(rows: list[dict[str, str]]) -> dict[str, int]:
    return dict(sorted(Counter(row.get("final_decision", "") for row in rows).items()))


def delta_row(target: str, prior: dict[str, str], fresh: dict[str, str]) -> dict[str, str]:
    row: dict[str, str] = {
        "target": target,
        "transition": (
            f"{prior.get('final_decision', '')}->{fresh.get('final_decision', '')}"
        ),
    }
    for field in ROW_FIELDS:
        row[f"prior_{field}"] = prior.get(field, "")
        row[f"fresh_{field}"] = fresh.get(field, "")
    return row


def verifier_counts(path: Path, final_verification: dict[str, Any]) -> dict[str, Any]:
    final_decision_counts = final_verification.get("final_decision_counts", {})
    candidate_counts = final_verification.get("candidate_decision_counts", {})
    skip_rationale = final_verification.get("skip_rationale", {})
    return {
        "path": str(path.resolve()),
        "manifest_targets": final_verification.get("manifest_targets"),
        "result_rows": final_verification.get("result_rows"),
        "final_candidates": final_verification.get("final_candidates"),
        "accepted_semantic_candidates": candidate_counts.get(
            "accepted_semantic_candidates"
        ),
        "final_add_spec": final_decision_counts.get("add_spec"),
        "final_skip": final_decision_counts.get("skip"),
        "missing_target_count": final_verification.get("missing_target_count"),
        "extra_target_count": final_verification.get("extra_target_count"),
        "duplicate_result_count": final_verification.get("duplicate_result_count"),
        "empty_skip_rationale_rows": skip_rationale.get("empty_skip_rationale_rows"),
        "all_skip_rows_have_rationale": skip_rationale.get(
            "empty_skip_rationale_rows"
        )
        == 0,
    }


def build_report(summary: dict[str, Any], artifacts: dict[str, str]) -> str:
    target_set = summary["target_set"]
    verifier = summary["fresh_verifier_counts"]
    delta = summary["decision_delta"]
    lines = [
        "# Prior vs Fresh Rust Std Specgen Delta",
        "",
        f"Generated at UTC `{summary['generated_at_utc']}`.",
        "",
        "This audit compares the prior full run against the canonical fresh run "
        "by target name and final decision. It records explicit target lists and "
        "row deltas; it does not use checksum evidence.",
        "",
        "## Target Set and Fresh Verifier",
        "",
        "| Measure | Value |",
        "| --- | ---: |",
        f"| prior final-candidate rows | {summary['prior']['rows']} |",
        f"| fresh final-candidate rows | {summary['fresh']['rows']} |",
        f"| common targets | {target_set['common_count']} |",
        f"| missing in fresh | {target_set['missing_in_fresh_count']} |",
        f"| extra in fresh | {target_set['extra_in_fresh_count']} |",
        f"| fresh verifier missing targets | {verifier['missing_target_count']} |",
        f"| fresh verifier extra targets | {verifier['extra_target_count']} |",
        f"| fresh verifier duplicate result targets | {verifier['duplicate_result_count']} |",
        f"| fresh verifier accepted semantic candidates | {verifier['accepted_semantic_candidates']} |",
        f"| fresh verifier final add_spec rows | {verifier['final_add_spec']} |",
        f"| fresh verifier final skip rows | {verifier['final_skip']} |",
        f"| fresh verifier empty skip rationales | {verifier['empty_skip_rationale_rows']} |",
        "",
        "## Decision Delta",
        "",
        "| Measure | Value |",
        "| --- | ---: |",
        f"| changed final decisions | {delta['changed_count']} |",
        f"| prior add_spec -> fresh skip | {delta['prior_add_fresh_skip_count']} |",
        f"| prior skip -> fresh add_spec | {delta['prior_skip_fresh_add_count']} |",
        "| changed fresh skip rows missing rationale | "
        f"{delta['changed_fresh_skip_missing_rationale_count']} |",
        "",
        "The changed-row CSVs include prior and fresh category, gate, issue, "
        "requires, ensures, rationale, source-fidelity, and contract-text fields "
        "so the decision changes are inspectable without relying on opaque summaries.",
        "",
        "## Artifacts",
        "",
    ]
    for name, artifact_path in artifacts.items():
        lines.append(f"- `{name}`: `{artifact_path}`")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    prior_root = args.prior_root.expanduser().resolve()
    fresh_root = args.fresh_root.expanduser().resolve()
    prior_csv = prior_root / "final_candidates.csv"
    fresh_csv = fresh_root / "final_candidates.csv"
    final_verification_path = (
        args.final_verification.expanduser().resolve()
        if args.final_verification
        else fresh_root / "final_verification.json"
    )
    out_dir = (
        args.out_dir.expanduser().resolve()
        if args.out_dir
        else fresh_root / "prior_fresh_delta"
    )

    prior_rows = read_rows(prior_csv)
    fresh_rows = read_rows(fresh_csv)
    prior_by_target = rows_by_target(prior_rows, prior_csv)
    fresh_by_target = rows_by_target(fresh_rows, fresh_csv)
    prior_targets = set(prior_by_target)
    fresh_targets = set(fresh_by_target)
    common_targets = sorted(prior_targets & fresh_targets)
    missing_in_fresh = sorted(prior_targets - fresh_targets)
    extra_in_fresh = sorted(fresh_targets - prior_targets)
    changed_rows = [
        delta_row(target, prior_by_target[target], fresh_by_target[target])
        for target in common_targets
        if prior_by_target[target].get("final_decision", "")
        != fresh_by_target[target].get("final_decision", "")
    ]
    prior_add_fresh_skip = [
        row for row in changed_rows if row["transition"] == "add_spec->skip"
    ]
    prior_skip_fresh_add = [
        row for row in changed_rows if row["transition"] == "skip->add_spec"
    ]
    missing_rationale = [
        row["target"]
        for row in changed_rows
        if row["fresh_final_decision"] == "skip"
        and not str(row.get("fresh_rationale", "")).strip()
    ]

    final_verification = json.loads(final_verification_path.read_text())
    fresh_verifier_counts = verifier_counts(
        final_verification_path, final_verification
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "REPORT.md": str((out_dir / "REPORT.md").resolve()),
        "decision_changes.csv": str((out_dir / "decision_changes.csv").resolve()),
        "newly_accepted_prior_skip_fresh_add.csv": str(
            (out_dir / "newly_accepted_prior_skip_fresh_add.csv").resolve()
        ),
        "prior_add_spec_now_fresh_skip.csv": str(
            (out_dir / "prior_add_spec_now_fresh_skip.csv").resolve()
        ),
        "summary.json": str((out_dir / "summary.json").resolve()),
        "target_set_audit.json": str((out_dir / "target_set_audit.json").resolve()),
    }
    target_set = {
        "common_count": len(common_targets),
        "common_targets": common_targets,
        "extra_in_fresh": extra_in_fresh,
        "extra_in_fresh_count": len(extra_in_fresh),
        "fresh_path": str(fresh_csv.resolve()),
        "fresh_target_count": len(fresh_targets),
        "missing_in_fresh": missing_in_fresh,
        "missing_in_fresh_count": len(missing_in_fresh),
        "prior_path": str(prior_csv.resolve()),
        "prior_target_count": len(prior_targets),
        "target_sets_equal": prior_targets == fresh_targets,
    }
    transition_counts = Counter(row["transition"] for row in changed_rows)
    decision_delta = {
        "changed_count": len(changed_rows),
        "changed_fresh_skip_missing_rationale_count": len(missing_rationale),
        "changed_fresh_skip_missing_rationale_targets": missing_rationale,
        "prior_add_fresh_skip_count": len(prior_add_fresh_skip),
        "prior_skip_fresh_add_count": len(prior_skip_fresh_add),
        "transition_counts": dict(sorted(transition_counts.items())),
    }
    acceptance_checks = {
        "target_sets_equal": target_set["target_sets_equal"],
        "target_sets_have_2121_rows_each": (
            len(prior_rows) == 2121 and len(fresh_rows) == 2121
        ),
        f"decision_changes_total_{EXPECTED_DECISION_CHANGES}": len(changed_rows)
        == EXPECTED_DECISION_CHANGES,
        f"prior_add_fresh_skip_total_{EXPECTED_PRIOR_ADD_FRESH_SKIP}": len(
            prior_add_fresh_skip
        )
        == EXPECTED_PRIOR_ADD_FRESH_SKIP,
        f"prior_skip_fresh_add_total_{EXPECTED_PRIOR_SKIP_FRESH_ADD}": len(
            prior_skip_fresh_add
        )
        == EXPECTED_PRIOR_SKIP_FRESH_ADD,
        "changed_fresh_skip_rationales_non_empty": not missing_rationale,
        f"fresh_verifier_{EXPECTED_FRESH_ACCEPTED}_accepted_{EXPECTED_FRESH_SKIP}_skips": (
            fresh_verifier_counts["accepted_semantic_candidates"]
            == EXPECTED_FRESH_ACCEPTED
            and fresh_verifier_counts["final_add_spec"] == EXPECTED_FRESH_ACCEPTED
            and fresh_verifier_counts["final_skip"] == EXPECTED_FRESH_SKIP
        ),
        "fresh_verifier_zero_missing_extra_duplicates": (
            fresh_verifier_counts["missing_target_count"] == 0
            and fresh_verifier_counts["extra_target_count"] == 0
            and fresh_verifier_counts["duplicate_result_count"] == 0
        ),
    }
    summary = {
        "schema_version": 1,
        "generated_at_utc": utc_now(),
        "prior": {
            "root": str(prior_root),
            "final_candidates_csv": str(prior_csv),
            "rows": len(prior_rows),
            "unique_targets": len(prior_targets),
            "final_decision_counts": count_decisions(prior_rows),
        },
        "fresh": {
            "root": str(fresh_root),
            "final_candidates_csv": str(fresh_csv),
            "rows": len(fresh_rows),
            "unique_targets": len(fresh_targets),
            "final_decision_counts": count_decisions(fresh_rows),
        },
        "target_set": {
            key: value for key, value in target_set.items() if not key.endswith("_targets")
        },
        "decision_delta": decision_delta,
        "fresh_verifier_counts": fresh_verifier_counts,
        "acceptance_checks": acceptance_checks,
        "acceptance_passed": all(acceptance_checks.values()),
        "artifacts": artifacts,
    }

    write_csv(out_dir / "decision_changes.csv", changed_rows, DELTA_FIELDS)
    write_csv(
        out_dir / "newly_accepted_prior_skip_fresh_add.csv",
        prior_skip_fresh_add,
        DELTA_FIELDS,
    )
    write_csv(
        out_dir / "prior_add_spec_now_fresh_skip.csv",
        prior_add_fresh_skip,
        DELTA_FIELDS,
    )
    (out_dir / "target_set_audit.json").write_text(
        json.dumps(target_set, indent=2, sort_keys=True) + "\n"
    )
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    (out_dir / "REPORT.md").write_text(build_report(summary, artifacts))

    print(
        f"wrote {len(changed_rows)} decision changes; "
        f"add_spec->skip={len(prior_add_fresh_skip)} "
        f"skip->add_spec={len(prior_skip_fresh_add)}"
    )
    return 0 if summary["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
