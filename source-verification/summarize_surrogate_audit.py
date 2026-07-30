#!/usr/bin/env python3
"""Summarize source-surrogate and implementation-fidelity audit results."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "surrogate-audit"
PROVED = ROOT / "proved-apis"

STRICT_BODY_FIDELITY = {"exact_body", "mechanical_desugaring"}

# These bodies are source-faithful, but the accepting artifact still does not
# constitute an admissible proof of the target contract.
ADMISSIBILITY_OVERRIDES = {
    "std_specs__ffi.rs__L237__CString__as_c_str": {
        "admissibility": "target_equivalent_axiom",
        "reason": (
            "The copied body is exact, but axiom_cstring_view_valid supplies an "
            "unsourced representation invariant needed for the target postcondition."
        ),
    },
    "std_specs__btree.rs__L461__BTreeMap__Key__Value__A__contains_key__Q": {
        "admissibility": "missing_target_postcondition",
        "reason": (
            "The copied body is exact, but source_btree_map_contains_key has no "
            "target ensures clause, so the accepting function does not prove the contract."
        ),
    },
}


def load(path: Path):
    return json.loads(path.read_text())


def percent(count: int, total: int) -> float:
    return round(100.0 * count / total, 2) if total else 0.0


def pre_audit_label(record: dict) -> str:
    return "verified" if record.get("current_status") == "verified" else "unverified"


def main() -> None:
    preproved = load(REPORT / "preproved-records.json")["records"]
    generated = load(REPORT / "generated-records.json")["records"]
    audited = {record["id"]: record for record in preproved + generated}
    resolution_path = REPORT / "source-resolution-overrides.json"
    resolution_payload = load(resolution_path) if resolution_path.is_file() else {}
    resolutions = (
        {
            record["id"]: record
            for record in resolution_payload.get("records", [])
        }
        if resolution_payload
        else {}
    )
    retry_path = ROOT / "fidelity-retry" / "accepted-overrides.json"
    retry_payload = load(retry_path) if retry_path.is_file() else {}
    retry_overrides = {
        record["id"]: record for record in retry_payload.get("records", [])
    }

    manifest = load(ROOT / "bulk-proof" / "manifest.json")["targets"]
    overall = {
        record["id"]: record
        for record in load(ROOT / "bulk-proof" / "OVERALL.json")["results"]
    }
    organized_verification_path = ROOT / "organized-suite" / "verification.json"
    organized_verification = (
        load(organized_verification_path)["counts"]
        if organized_verification_path.is_file()
        else {}
    )

    assert len(manifest) == 539
    assert len(audited) == 406
    assert set(audited).issubset(overall)

    rows = []
    for target in manifest:
        target_id = target["id"]
        audit = audited.get(target_id)
        if audit is None:
            assert overall[target_id]["status"] == "blocked"
            rows.append(
                {
                    "id": target_id,
                    "api_path": target["api_path"],
                    "raw_target": target["raw_target"],
                    "pre_audit_label": "unverified",
                    "campaign_status": "blocked",
                    "proof_object": "no_passing_artifact",
                    "body_fidelity": "",
                    "proof_admissibility": "",
                    "strict_verdict": "no_passing_artifact",
                    "proof_bundle": "",
                    "contains_unrelated_target": False,
                    "trust_level": "",
                    "resolved_source_path": "",
                    "resolved_source_lines": "",
                    "reason": overall[target_id].get("blocker", ""),
                }
            )
            continue

        resolution = retry_overrides.get(target_id) or resolutions.get(target_id)
        fidelity = (
            resolution["body_fidelity"] if resolution is not None else audit["fidelity"]
        )
        resolved_admissibility = (
            resolution["proof_admissibility"] if resolution is not None else None
        )
        base_reason = resolution["reason"] if resolution is not None else audit["reason"]
        override = ADMISSIBILITY_OVERRIDES.get(target_id)
        if override is not None:
            admissibility = override["admissibility"]
            verdict = "known_mismatch_or_inadmissible"
            reason = f"{base_reason} {override['reason']}".strip()
        elif resolved_admissibility in {
            "peer_cycle",
            "target_equivalent_axiom",
            "wrong_or_missing_target",
        }:
            admissibility = resolved_admissibility
            verdict = "known_mismatch_or_inadmissible"
            reason = base_reason
        elif fidelity == "source_unavailable":
            admissibility = resolved_admissibility or "unresolved"
            verdict = "source_unresolved"
            reason = base_reason
        elif fidelity in STRICT_BODY_FIDELITY and resolved_admissibility in {
            None,
            "ordinary_acyclic",
        }:
            admissibility = resolved_admissibility or "ordinary_acyclic"
            verdict = "strict_faithful_admissible"
            reason = base_reason
        else:
            admissibility = (
                resolved_admissibility
                or (
                    fidelity
                    if fidelity in {"circular_or_target_axiom", "ambiguous_mapping"}
                    else "not_admissible_under_strict_policy"
                )
            )
            verdict = "known_mismatch_or_inadmissible"
            reason = base_reason

        proof_object = audit["proof_object"]
        if proof_object == "no_target_proof/ambiguous":
            proof_object = "target_mapping_failure"

        rows.append(
            {
                "id": target_id,
                "api_path": target["api_path"],
                "raw_target": target["raw_target"],
                "pre_audit_label": pre_audit_label(audit),
                "campaign_status": overall[target_id]["status"],
                "proof_object": proof_object,
                "body_fidelity": fidelity,
                "proof_admissibility": admissibility,
                "strict_verdict": verdict,
                "proof_bundle": (
                    "" if target_id in retry_overrides else audit.get("proof_bundle", "")
                ),
                "contains_unrelated_target": bool(
                    audit.get("unrelated_target_count", 0)
                    and target_id not in retry_overrides
                ),
                "trust_level": audit.get("trust_level", ""),
                "resolved_source_path": (
                    resolution.get("resolved_source_path", "")
                    if resolution is not None
                    else ""
                ),
                "resolved_source_lines": (
                    resolution.get("resolved_source_lines", "")
                    if resolution is not None
                    else ""
                ),
                "reason": reason,
            }
        )

    assert len(rows) == 539

    fieldnames = list(rows[0])
    with (REPORT / "records.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    labels = ("verified", "unverified")
    verdicts = (
        "strict_faithful_admissible",
        "known_mismatch_or_inadmissible",
        "source_unresolved",
        "no_passing_artifact",
    )
    verdict_matrix = {
        label: Counter(
            row["strict_verdict"] for row in rows if row["pre_audit_label"] == label
        )
        for label in labels
    }
    verdict_totals = Counter(row["strict_verdict"] for row in rows)

    body_categories = (
        "exact_body",
        "mechanical_desugaring",
        "alternate_implementation",
        "circular_or_target_axiom",
        "source_unavailable",
        "ambiguous_mapping",
        "",
    )
    body_matrix = {
        label: Counter(
            row["body_fidelity"] for row in rows if row["pre_audit_label"] == label
        )
        for label in labels
    }

    object_matrix = {
        label: Counter(
            row["proof_object"] for row in rows if row["pre_audit_label"] == label
        )
        for label in labels
    }

    paths: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        paths[row["api_path"]].append(row["strict_verdict"])
    path_summary = {
        "total": len(paths),
        "with_any_strict_faithful_record": sum(
            "strict_faithful_admissible" in values for values in paths.values()
        ),
        "with_all_records_strict_faithful": sum(
            all(value == "strict_faithful_admissible" for value in values)
            for values in paths.values()
        ),
        "with_any_known_mismatch": sum(
            "known_mismatch_or_inadmissible" in values for values in paths.values()
        ),
        "with_any_source_unresolved": sum(
            "source_unresolved" in values for values in paths.values()
        ),
        "with_all_records_no_passing_artifact": sum(
            all(value == "no_passing_artifact" for value in values)
            for values in paths.values()
        ),
    }

    proof_hashes = Counter()
    for target_id in audited:
        proof = PROVED / target_id / "proof.rs"
        proof_hashes[hashlib.sha256(proof.read_bytes()).hexdigest()] += 1

    strict_ids = {
        row["id"]
        for row in rows
        if row["strict_verdict"] == "strict_faithful_admissible"
    }
    strict_proof_hashes = {
        hashlib.sha256((PROVED / target_id / "proof.rs").read_bytes()).hexdigest()
        for target_id in strict_ids
    }
    strict_bundle_records = sum(
        row["id"] in strict_ids and bool(row["proof_bundle"]) for row in rows
    )
    strict_bundles = {
        row["proof_bundle"]
        for row in rows
        if row["id"] in strict_ids and row["proof_bundle"]
    }

    shared_bundle_records = sum(bool(row["proof_bundle"]) for row in rows)
    unrelated_target_records = sum(row["contains_unrelated_target"] for row in rows)
    summary = {
        "scope": {
            "direct_contract_records": len(rows),
            "canonical_api_paths": len(paths),
            "verus_accepting_artifacts": len(audited),
            "blocked_without_passing_artifact": len(rows) - len(audited),
            "pre_audit_verified_label": sum(
                row["pre_audit_label"] == "verified" for row in rows
            ),
            "pre_audit_unverified_label": sum(
                row["pre_audit_label"] == "unverified" for row in rows
            ),
        },
        "strict_verdict_totals": dict(verdict_totals),
        "strict_verdict_by_pre_audit_label": {
            label: dict(verdict_matrix[label]) for label in labels
        },
        "passing_body_fidelity_by_pre_audit_label": {
            label: {
                category or "no_passing_artifact": body_matrix[label][category]
                for category in body_categories
                if body_matrix[label][category]
            }
            for label in labels
        },
        "proof_object_by_pre_audit_label": {
            label: dict(object_matrix[label]) for label in labels
        },
        "artifact_structure": {
            "unique_proof_file_contents": len(proof_hashes),
            "shared_preproved_bundle_records": shared_bundle_records,
            "shared_preproved_bundle_count": len(
                {row["proof_bundle"] for row in rows if row["proof_bundle"]}
            ),
            "records_containing_unrelated_target_function": unrelated_target_records,
            "strict_record_count": len(strict_ids),
            "strict_unique_proof_file_contents": len(strict_proof_hashes),
            "strict_shared_bundle_records": strict_bundle_records,
            "strict_shared_bundle_count": len(strict_bundles),
        },
        "canonical_path_summary": path_summary,
        "admissibility_overrides": ADMISSIBILITY_OVERRIDES,
        "resolved_source_overrides": len(resolutions),
        "resolved_source_summary": resolution_payload.get("summary", {}),
        "accepted_fidelity_retries": len(retry_overrides),
        "reclassified_suite_verification": organized_verification,
    }
    (REPORT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    verified_total = summary["scope"]["pre_audit_verified_label"]
    unverified_total = summary["scope"]["pre_audit_unverified_label"]
    passing_total = summary["scope"]["verus_accepting_artifacts"]
    strict_total = verdict_totals["strict_faithful_admissible"]
    unresolved_total = verdict_totals["source_unresolved"]
    faithful_body_total = sum(
        row["body_fidelity"] in STRICT_BODY_FIDELITY for row in rows
    )
    faithful_body_rejected = sum(
        row["body_fidelity"] in STRICT_BODY_FIDELITY
        and row["strict_verdict"] != "strict_faithful_admissible"
        for row in rows
    )
    resolution_summary = resolution_payload.get("summary", {})
    resolution_body = resolution_summary.get("body_fidelity", {})
    resolution_admissibility = resolution_summary.get("proof_admissibility", {})

    lines = [
        "# Source-surrogate and fidelity audit",
        "",
        "The word `verified` below refers to the suite's pre-audit label.",
        "Verus did not directly prove any original Rust std symbol: 405 accepting",
        "artifacts verify mapped local `source_*` surrogate functions, while one",
        "accepting artifact has a target-mapping failure.",
        "",
        "## Conservative result",
        "",
        "| Pre-audit suite label | Strict-faithful and admissible surrogate | Known mismatch/inadmissible | Source body unresolved | No passing artifact | Total |",
        "|---|---:|---:|---:|---:|---:|",
        (
            f"| Verified | {verdict_matrix['verified']['strict_faithful_admissible']} "
            f"| {verdict_matrix['verified']['known_mismatch_or_inadmissible']} "
            f"| {verdict_matrix['verified']['source_unresolved']} "
            f"| {verdict_matrix['verified']['no_passing_artifact']} | {verified_total} |"
        ),
        (
            f"| Unverified / external body | "
            f"{verdict_matrix['unverified']['strict_faithful_admissible']} "
            f"| {verdict_matrix['unverified']['known_mismatch_or_inadmissible']} "
            f"| {verdict_matrix['unverified']['source_unresolved']} "
            f"| {verdict_matrix['unverified']['no_passing_artifact']} | {unverified_total} |"
        ),
        (
            f"| **Overall** | **{strict_total}** "
            f"| **{verdict_totals['known_mismatch_or_inadmissible']}** "
            f"| **{verdict_totals['source_unresolved']}** "
            f"| **{verdict_totals['no_passing_artifact']}** | **{len(rows)}** |"
        ),
        "",
        f"- Strict-faithful local-surrogate coverage: **{strict_total}/{len(rows)} "
        f"({percent(strict_total, len(rows)):.2f}%)**.",
        f"- Among Verus-accepting artifacts: **{strict_total}/{passing_total} "
        f"({percent(strict_total, passing_total):.2f}%)**.",
        f"- Within the pre-audit verified label: "
        f"**{verdict_matrix['verified']['strict_faithful_admissible']}/{verified_total} "
        f"({percent(verdict_matrix['verified']['strict_faithful_admissible'], verified_total):.2f}%)**.",
        f"- Within all pre-audit unverified records: "
        f"**{verdict_matrix['unverified']['strict_faithful_admissible']}/{unverified_total} "
        f"({percent(verdict_matrix['unverified']['strict_faithful_admissible'], unverified_total):.2f}%)**.",
        (
            "- Reclassified one-click suite: "
            f"**{organized_verification.get('proved_passed', 'pending')} "
            "local-surrogate proofs + "
            f"{organized_verification.get('external_body_passed', 'pending')} "
            "external-body fallbacks; "
            f"{organized_verification.get('passed', 'pending')} passed, "
            f"{organized_verification.get('failed', 'pending')} failed**."
        ),
        "",
        f"The remaining {unresolved_total} unresolved record is the declaration-only",
        "`write_box_via_move` compiler intrinsic. `Tracked` and `Ghost` are known",
        "absent/non-std targets, not unresolved Rust std implementations.",
        "",
        "## What the proof object actually is",
        "",
        "| Pre-audit suite label | Original std symbol | Mapped local surrogate | Wrong/ambiguous target | No passing artifact | Total |",
        "|---|---:|---:|---:|---:|---:|",
        (
            f"| Verified | 0 | {object_matrix['verified']['local_surrogate']} "
            f"| {object_matrix['verified']['target_mapping_failure']} "
            f"| {object_matrix['verified']['no_passing_artifact']} | {verified_total} |"
        ),
        (
            f"| Unverified / external body | 0 "
            f"| {object_matrix['unverified']['local_surrogate']} "
            f"| {object_matrix['unverified']['target_mapping_failure']} "
            f"| {object_matrix['unverified']['no_passing_artifact']} | {unverified_total} |"
        ),
        "",
        "Thus no accepting artifact establishes the external-symbol contract by",
        "machine-checked linkage; source fidelity is an audit judgment.",
        "",
        "## Extra unrelated functions in per-record proof files",
        "",
        f"- Full shared preproved bundle copied per record: **{shared_bundle_records}/{len(rows)} "
        f"({percent(shared_bundle_records, len(rows)):.2f}%)**, representing "
        f"**{summary['artifact_structure']['shared_preproved_bundle_count']}** unique bundles.",
        f"- Any unrelated API surrogate present: **{unrelated_target_records}/{len(rows)} "
        f"({percent(unrelated_target_records, len(rows)):.2f}%)**.",
        f"- Pre-audit verified: **48/{verified_total} ({percent(48, verified_total):.2f}%)**.",
        f"- Pre-audit unverified: **54/{unverified_total} ({percent(54, unverified_total):.2f}%)**.",
        "",
        "The extra unverified case outside the 101 shared bundles is the incorrect",
        "TryFrom artifact that contains only the TryInto surrogate.",
        "",
        "## First-pass mutually exclusive classification",
        "",
        "| Classification | Pre-audit verified | Pre-audit unverified | Overall |",
        "|---|---:|---:|---:|",
    ]
    display_categories = (
        ("exact_body", "Exact executable body"),
        ("mechanical_desugaring", "Mechanical desugaring"),
        ("alternate_implementation", "Alternate implementation"),
        ("circular_or_target_axiom", "Circular/target-axiom dominant issue"),
        ("source_unavailable", "Source body unresolved"),
        ("ambiguous_mapping", "Ambiguous/wrong target mapping"),
        ("", "No passing artifact"),
    )
    for category, label in display_categories:
        verified = body_matrix["verified"][category]
        unverified = body_matrix["unverified"][category]
        lines.append(f"| {label} | {verified} | {unverified} | {verified + unverified} |")
    lines.extend(
        [
            "",
            f"Exact/mechanical totals are {faithful_body_total}, but "
            f"{faithful_body_rejected} artifacts are not admissible proofs. Known",
            "examples include `CString::as_c_str`, which depends on a target-critical",
            "representation axiom, and one `BTreeMap::contains_key` surrogate with",
            f"no target postcondition. The final conservative count is therefore {strict_total}.",
            "",
            "Body fidelity and proof admissibility are separate dimensions in",
            "`source-resolution-overrides.json`; the table above preserves the",
            "older mutually exclusive first-pass category for other records.",
            "",
            "## Exhaustive resolution of the former 104 unknown-source records",
            "",
            "| Dimension | Category | Count |",
            "|---|---|---:|",
            f"| Body fidelity | Exact | {resolution_body.get('exact_body', 0)} |",
            f"| Body fidelity | Mechanical desugaring | {resolution_body.get('mechanical_desugaring', 0)} |",
            f"| Body fidelity | Alternate implementation | {resolution_body.get('alternate_implementation', 0)} |",
            f"| Body fidelity | No Rust body | {resolution_body.get('source_unavailable', 0)} |",
            f"| Proof admissibility | Ordinary/acyclic | {resolution_admissibility.get('ordinary_acyclic', 0)} |",
            f"| Proof admissibility | Target-critical axiom | {resolution_admissibility.get('target_equivalent_axiom', 0)} |",
            f"| Proof admissibility | Wrong/missing target | {resolution_admissibility.get('wrong_or_missing_target', 0)} |",
            f"| Proof admissibility | Unresolved intrinsic | {resolution_admissibility.get('unresolved', 0)} |",
            "",
            "## Proof-artifact reuse in the retained set",
            "",
            f"- Strict-faithful records: **{len(strict_ids)}**.",
            f"- Unique strict proof-file contents: **{len(strict_proof_hashes)}**.",
            f"- Strict records copied from shared bundles: **{strict_bundle_records}** "
            f"across **{len(strict_bundles)}** bundles.",
            "",
            "## Canonical API paths",
            "",
            f"- Paths with at least one strict-faithful admissible record: "
            f"**{path_summary['with_any_strict_faithful_record']}/{len(paths)} "
            f"({percent(path_summary['with_any_strict_faithful_record'], len(paths)):.2f}%)**.",
            f"- Paths whose every direct record is strict-faithful and admissible: "
            f"**{path_summary['with_all_records_strict_faithful']}/{len(paths)} "
            f"({percent(path_summary['with_all_records_strict_faithful'], len(paths)):.2f}%)**.",
            "",
            "Per-record classifications and reasons are in `records.csv`; aggregate",
            "machine-readable counts are in `summary.json`.",
        ]
    )
    (REPORT / "SUMMARY.md").write_text("\n".join(lines) + "\n")

    print(json.dumps(summary["scope"], indent=2))
    print(json.dumps(summary["strict_verdict_totals"], indent=2))


if __name__ == "__main__":
    main()
