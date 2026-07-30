#!/usr/bin/env python3
"""Write paired determinism-feedback, provability, and no-spec reason tables."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import glob
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPECGEN = ROOT / "specgen"
SOURCE_VERIFICATION = ROOT / "source-verification"
OUT = SOURCE_VERIFICATION / "feedback-comparison"

STATUS_ORDER = (
    "complete",
    "unknown",
    "trivial_equality",
    "incomplete_sat",
    "typecheck_or_checker_failure",
    "skip_no_spec",
)
PRIMARY_STATUS_ORDER = (
    "complete",
    "unknown",
    "trivial_equality",
    "incomplete_sat",
    "no_spec_or_checker_failure",
)

REASON_DESCRIPTIONS = {
    "runtime_or_hidden_state": "Result depends on OS/runtime/process state not exposed by a stable pure view.",
    "needs_new_vstd_abstraction": "Required semantic vocabulary or owner/module model is absent from vstd.",
    "trait_contract_integration": "Requires editing or composing an external trait specification.",
    "concurrency_or_hidden_state": "Atomic/concurrent state is not represented by an ordinary deterministic view.",
    "unsafe_or_representation_sensitive": "Raw pointer, provenance, unsafe, or representation-sensitive behavior.",
    "determinism_checker_unsupported": "Current checker cannot encode the exact output or mutable post-state.",
    "iterator_or_adapter_result": "Iterator/guard/adapter result needs a prophetic or state-transition model.",
    "formatting_effect": "Formatting state and emitted effects are not modeled.",
    "toolchain_unavailable": "API is unavailable in the Verus Rust 1.96 toolchain.",
    "representation_or_allocator": "Allocator or private representation state is absent from the public view.",
    "higher_order_contract": "Closure/callback semantics require call-ensures or a higher-order model.",
    "ownership_or_uninitialized_model": "Linear ownership, initialization, or MaybeUninit state is not modeled.",
    "complex_result_or_pattern_model": "Result discriminant/pattern semantics need an additional model.",
    "associated_type_or_projection": "Associated-type/projection signature requires manual integration.",
    "no_modeled_observable_output": "No return value or mutable output is represented by the checker.",
    "needs_borrowed_key_or_ordering_model": "Borrow<Q> functionality or cross-type ordering is missing.",
    "needs_pointer_identity_or_provenance_model": "Semantic views erase location, identity, address, or provenance.",
    "needs_functional_trait_semantics": "Clone/Default is only relational and does not uniquely determine output.",
}


def batch_files() -> list[Path]:
    return [
        SPECGEN / "suitable-pilot-gpt56sol-v2" / "batch_summary.json",
        SPECGEN / "suitable-remaining-gpt56sol-v1" / "batch_summary.json",
        *sorted(
            Path(path)
            for path in glob.glob(
                str(
                    SPECGEN
                    / "remaining-generation"
                    / "evaluated-gpt56sol"
                    / "*"
                    / "batch_summary.json"
                )
            )
        ),
    ]


def status(record: dict) -> str:
    candidate = record.get("candidate") or {}
    if candidate.get("decision") != "add_spec":
        return "skip_no_spec"
    checker = record.get("checker") or {}
    typecheck = checker.get("typecheck") or {}
    determinism = checker.get("determinism") or {}
    if typecheck and typecheck.get("returncode") != 0:
        return "typecheck_or_checker_failure"
    if determinism.get("status") == "ok":
        if determinism.get("equal_fn_trivial"):
            return "trivial_equality"
        return {
            "unsat": "complete",
            "unknown": "unknown",
            "sat": "incomplete_sat",
        }.get(determinism.get("r0_z3"), "typecheck_or_checker_failure")
    return "typecheck_or_checker_failure"


def records_by_phase() -> tuple[dict[str, dict[str, dict]], dict[str, dict]]:
    occurrences: dict[str, list[tuple[dict, dict]]] = defaultdict(list)
    for path in batch_files():
        payload = json.loads(path.read_text())
        for result in payload["results"]:
            history = result.get("history") or []
            round_zero = next(
                (item for item in history if item.get("round") == 0),
                history[0] if history else {},
            )
            final = result.get("final") or (history[-1] if history else {})
            occurrences[result["target"]].append((round_zero, final))
    assert len(occurrences) == 2121
    return (
        {
            "no_feedback": {
                target: values[0][0] for target, values in occurrences.items()
            },
            "with_feedback": {
                target: values[-1][1] for target, values in occurrences.items()
            },
        },
        {target: values[-1][1] for target, values in occurrences.items()},
    )


def suitable_skip_reason(record: dict) -> str:
    candidate = record.get("candidate") or {}
    text = " ".join(
        [
            str(candidate.get("rationale", "")),
            " ".join(str(value) for value in candidate.get("risks") or []),
        ]
    ).lower()
    if any(
        value in text
        for value in (
            "unsized",
            "post-state",
            "post state",
            "nested_reference",
            "nested reference",
        )
    ):
        return "determinism_checker_unsupported"
    if "borrowed" in text or "borrow<" in text:
        return "needs_borrowed_key_or_ordering_model"
    if "clone" in text or "default" in text:
        return "needs_functional_trait_semantics"
    if any(
        value in text
        for value in (
            "pointer",
            "provenance",
            "reference-identity",
            "reference identity",
            "location",
        )
    ):
        return "needs_pointer_identity_or_provenance_model"
    return "needs_new_vstd_abstraction"


def load_proof_outcomes() -> tuple[dict[str, str], dict]:
    phase_path = SOURCE_VERIFICATION / "feedback-proof" / "phase-status.json"
    run_path = (
        SOURCE_VERIFICATION
        / "feedback-proof"
        / "runs"
        / "full-gpt56sol"
        / "summary.json"
    )
    audit_path = SOURCE_VERIFICATION / "feedback-proof" / "fidelity.csv"
    if not phase_path.is_file() or not run_path.is_file():
        return {}, {"status": "pending"}
    run = json.loads(run_path.read_text())
    run_by_id = {result["id"]: result for result in run["results"]}
    strict_by_id = {}
    if audit_path.is_file():
        with audit_path.open() as stream:
            strict_by_id = {
                row["variant_id"]: row["strict_verdict"]
                for row in csv.DictReader(stream)
            }
    outcomes = {}
    for variant_id, result in run_by_id.items():
        if result.get("status") != "proved":
            outcomes[variant_id] = "not_proved"
        elif strict_by_id:
            outcomes[variant_id] = strict_by_id.get(
                variant_id, "proved_fidelity_unreviewed"
            )
        else:
            outcomes[variant_id] = "proved_fidelity_unreviewed"
    return outcomes, {
        "status": "complete" if strict_by_id else "fidelity_review_pending",
        "variants": len(run_by_id),
    }


def percent(count: int, total: int) -> str:
    return f"{100.0 * count / total:.2f}%" if total else "0.00%"


def main() -> None:
    phases, final_records = records_by_phase()
    classifications = {
        row["target"]: row
        for row in csv.DictReader((SPECGEN / "classification.csv").open())
    }
    proof_phase = json.loads(
        (
            SOURCE_VERIFICATION / "feedback-proof" / "phase-status.json"
        ).read_text()
    )
    proof_variant_by_phase_target = {
        (row["phase"], row["target"]): row["variant_id"]
        for row in proof_phase["rows"]
    }
    proof_outcomes, proof_metadata = load_proof_outcomes()

    rows = []
    status_counts = {"no_feedback": Counter(), "with_feedback": Counter()}
    transition = Counter()
    no_spec_reasons = {
        "no_feedback": Counter(),
        "with_feedback": Counter(),
    }
    proof_counts = {"no_feedback": Counter(), "with_feedback": Counter()}
    proof_by_completeness = {
        "no_feedback": defaultdict(Counter),
        "with_feedback": defaultdict(Counter),
    }

    for target in sorted(phases["no_feedback"]):
        no_status = status(phases["no_feedback"][target])
        with_status = status(phases["with_feedback"][target])
        status_counts["no_feedback"][no_status] += 1
        status_counts["with_feedback"][with_status] += 1
        transition[(no_status, with_status)] += 1

        reasons = {}
        proof_statuses = {}
        for phase, phase_status in (
            ("no_feedback", no_status),
            ("with_feedback", with_status),
        ):
            adjusted_no_spec = phase_status in {
                "skip_no_spec",
                "typecheck_or_checker_failure",
            } and not (
                phase == "with_feedback"
                and no_status == "complete"
                and with_status == "skip_no_spec"
            )
            if adjusted_no_spec:
                initial = classifications[target]["classification"]
                reason = (
                    suitable_skip_reason(phases[phase][target])
                    if initial == "suitable_now"
                    else initial
                )
                no_spec_reasons[phase][reason] += 1
                reasons[phase] = reason
            else:
                reasons[phase] = ""

            variant_id = proof_variant_by_phase_target.get((phase, target), "")
            if not variant_id:
                proof_status = "no_valid_spec"
            else:
                proof_status = proof_outcomes.get(
                    variant_id, "proof_campaign_pending"
                )
            proof_counts[phase][proof_status] += 1
            if phase_status == "complete":
                completeness = "complete"
            elif phase_status in {
                "unknown",
                "trivial_equality",
                "incomplete_sat",
            }:
                completeness = "checker_valid_noncomplete"
            else:
                completeness = "invalid_or_no_spec"
            proof_by_completeness[phase][completeness][proof_status] += 1
            proof_statuses[phase] = proof_status

        rows.append(
            {
                "target": target,
                "no_feedback_status": no_status,
                "with_feedback_status": with_status,
                "no_feedback_complete": no_status == "complete",
                "with_feedback_complete": with_status == "complete",
                "no_feedback_proof_status": proof_statuses["no_feedback"],
                "with_feedback_proof_status": proof_statuses["with_feedback"],
                "no_feedback_no_spec_reason": reasons["no_feedback"],
                "with_feedback_no_spec_reason": reasons["with_feedback"],
                "initial_classification": classifications[target]["classification"],
            }
        )

    assert len(rows) == 2121
    for phase in ("no_feedback", "with_feedback"):
        assert sum(status_counts[phase].values()) == 2121
        assert sum(proof_counts[phase].values()) == 2121

    pure_feedback_counts = Counter(status_counts["with_feedback"])
    filtered_complete = transition[("complete", "skip_no_spec")]
    pure_feedback_counts["complete"] += filtered_complete
    pure_feedback_counts["skip_no_spec"] -= filtered_complete
    assert filtered_complete == 66
    assert sum(pure_feedback_counts.values()) == 2121
    merged_status_counts = {
        "no_feedback": Counter(status_counts["no_feedback"]),
        "with_feedback": Counter(pure_feedback_counts),
    }
    for counts in merged_status_counts.values():
        counts["no_spec_or_checker_failure"] = (
            counts["skip_no_spec"] + counts["typecheck_or_checker_failure"]
        )
    assert sum(no_spec_reasons["no_feedback"].values()) == (
        merged_status_counts["no_feedback"]["no_spec_or_checker_failure"]
    )
    assert sum(no_spec_reasons["with_feedback"].values()) == (
        merged_status_counts["with_feedback"]["no_spec_or_checker_failure"]
    )
    OUT.mkdir(exist_ok=True)
    with (OUT / "records.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "method": {
            "no_feedback": (
                "Earliest saved round-0 record for each target; no rerun."
            ),
            "with_feedback": (
                "Final saved record from the latest evaluation occurrence for "
                "each target; no spec-generation rerun."
            ),
        },
        "status_counts": {
            phase: dict(counts) for phase, counts in status_counts.items()
        },
        "pure_determinism_with_feedback_counts": dict(pure_feedback_counts),
        "primary_merged_status_counts": {
            phase: {
                value: counts[value] for value in PRIMARY_STATUS_ORDER
            }
            for phase, counts in merged_status_counts.items()
        },
        "transition_counts": {
            f"{before} -> {after}": count
            for (before, after), count in transition.items()
        },
        "proof_counts": {
            phase: dict(counts) for phase, counts in proof_counts.items()
        },
        "proof_by_completeness": {
            phase: {
                completeness: dict(counts)
                for completeness, counts in values.items()
            }
            for phase, values in proof_by_completeness.items()
        },
        "proof_metadata": proof_metadata,
        "no_spec_reason_counts": {
            phase: dict(counts) for phase, counts in no_spec_reasons.items()
        },
        "no_spec_reason_descriptions": REASON_DESCRIPTIONS,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# Determinism-feedback comparison",
        "",
        "Both columns use the same **2,121 targets**. The no-feedback column is",
        "recovered from saved round-0 histories. The primary with-feedback table",
        "counts every contract that reached `R0 = unsat` before later suitability",
        "filtering. Spec generation was not rerun.",
        "",
        "The final column is **not pure SMT determinism feedback**. Its guarded",
        "reward also requires zero anti-vacuity issues and a `suitable_now` static",
        "classification. Contracts can therefore be changed to `skip` even when",
        "their round-0 R0 result was `unsat`, if they model only a framing fact,",
        "depend on hidden representation, or need an unavailable abstraction.",
        "",
        "## Pure determinism-feedback status table",
        "",
        "This primary table keeps the 66 contracts with round-0 `R0 = unsat` in",
        "`complete`, even though the later suitability/anti-vacuity filter changed",
        "their saved final decision to `skip`.",
        "",
        "| Status | No feedback | With feedback | Delta |",
        "|---|---:|---:|---:|",
    ]
    for value in PRIMARY_STATUS_ORDER:
        before = merged_status_counts["no_feedback"][value]
        after = merged_status_counts["with_feedback"][value]
        lines.append(f"| `{value}` | {before} | {after} | {after - before:+d} |")

    lines.extend(
        [
            "",
            "## Completeness summary",
            "",
            "| Metric | No feedback | With feedback |",
            "|---|---:|---:|",
        ]
    )
    for label, values in (
        (
            "Add-spec proposals",
            (
                2121 - status_counts["no_feedback"]["skip_no_spec"],
                2121 - pure_feedback_counts["skip_no_spec"],
            ),
        ),
        (
            "Checker-valid contracts",
            (
                sum(
                    status_counts["no_feedback"][value]
                    for value in (
                        "complete",
                        "unknown",
                        "trivial_equality",
                        "incomplete_sat",
                    )
                ),
                sum(
                    pure_feedback_counts[value]
                    for value in (
                        "complete",
                        "unknown",
                        "trivial_equality",
                        "incomplete_sat",
                    )
                ),
            ),
        ),
        (
            "Complete contracts",
            (
                status_counts["no_feedback"]["complete"],
                pure_feedback_counts["complete"],
            ),
        ),
        (
            "Not complete / no spec",
            (
                2121 - status_counts["no_feedback"]["complete"],
                2121 - pure_feedback_counts["complete"],
            ),
        ),
    ):
        lines.append(
            f"| {label} | {values[0]} ({percent(values[0], 2121)}) "
            f"| {values[1]} ({percent(values[1], 2121)}) |"
        )
    valid_before = sum(
        status_counts["no_feedback"][value]
        for value in ("complete", "unknown", "trivial_equality", "incomplete_sat")
    )
    valid_after = sum(
        pure_feedback_counts[value]
        for value in ("complete", "unknown", "trivial_equality", "incomplete_sat")
    )
    lines.append(
        f"| Complete among checker-valid | "
        f"{status_counts['no_feedback']['complete']}/{valid_before} "
        f"({percent(status_counts['no_feedback']['complete'], valid_before)}) "
        f"| {pure_feedback_counts['complete']}/{valid_after} "
        f"({percent(pure_feedback_counts['complete'], valid_after)}) |"
    )

    lines.extend(
        [
            "",
            "## Raw saved-final transitions",
            "",
            "The transition table below shows the literal saved final decisions",
            "before moving the 66 suitability-filtered complete contracts back into",
            "the pure determinism `complete` count.",
            "",
            "| No-feedback status | With-feedback status | Targets |",
            "|---|---|---:|",
        ]
    )
    for (before, after), count in transition.most_common():
        lines.append(f"| `{before}` | `{after}` | {count} |")

    newly_skipped = sum(
        count
        for (before, after), count in transition.items()
        if before != "skip_no_spec" and after == "skip_no_spec"
    )
    recovered_skips = sum(
        count
        for (before, after), count in transition.items()
        if before == "skip_no_spec" and after != "skip_no_spec"
    )
    lines.extend(
        [
            "",
            "### Why the no-spec count increased",
            "",
            f"- Newly changed to skip: **{newly_skipped}**.",
            f"- Previously skipped but recovered: **{recovered_skips}**.",
            f"- Net increase: **{newly_skipped - recovered_skips}**.",
            "",
            "| Round-0 status of newly skipped target | Count |",
            "|---|---:|",
        ]
    )
    for value in (
        "typecheck_or_checker_failure",
        "complete",
        "unknown",
        "trivial_equality",
    ):
        lines.append(
            f"| `{value}` | {transition[(value, 'skip_no_spec')]} |"
        )

    lines.extend(
        [
            "",
            "## Source-proof status for saved final contracts",
            "",
            f"Proof campaign state: `{proof_metadata['status']}`.",
            "",
            "| Proof status | No feedback | With feedback |",
            "|---|---:|---:|",
        ]
    )
    all_proof_statuses = sorted(
        set(proof_counts["no_feedback"]) | set(proof_counts["with_feedback"])
    )
    for value in all_proof_statuses:
        lines.append(
            f"| `{value}` | {proof_counts['no_feedback'][value]} "
            f"| {proof_counts['with_feedback'][value]} |"
        )

    valid_proof_before = 2121 - proof_counts["no_feedback"]["no_valid_spec"]
    valid_proof_after = 2121 - proof_counts["with_feedback"]["no_valid_spec"]
    strict_before = proof_counts["no_feedback"]["strict_faithful_admissible"]
    strict_after = proof_counts["with_feedback"]["strict_faithful_admissible"]
    complete_strict_before = proof_by_completeness["no_feedback"]["complete"][
        "strict_faithful_admissible"
    ]
    complete_strict_after = proof_by_completeness["with_feedback"]["complete"][
        "strict_faithful_admissible"
    ]
    lines.extend(
        [
            "",
            "### Provability summary",
            "",
            "| Metric | No feedback | With feedback |",
            "|---|---:|---:|",
            f"| Checker-valid contracts attempted | {valid_proof_before} | {valid_proof_after} |",
            (
                "| Verus pass before fidelity rejection | "
                f"{strict_before + proof_counts['no_feedback']['known_mismatch_or_inadmissible']} "
                f"| {strict_after + proof_counts['with_feedback']['known_mismatch_or_inadmissible']} |"
            ),
            f"| Strict-faithful admissible proofs | **{strict_before}** | **{strict_after}** |",
            (
                "| Strict proof rate among checker-valid | "
                f"{strict_before}/{valid_proof_before} ({percent(strict_before, valid_proof_before)}) "
                f"| {strict_after}/{valid_proof_after} ({percent(strict_after, valid_proof_after)}) |"
            ),
            (
                "| Strict proof rate among complete contracts | "
                f"{complete_strict_before}/{status_counts['no_feedback']['complete']} "
                f"({percent(complete_strict_before, status_counts['no_feedback']['complete'])}) "
                f"| {complete_strict_after}/{status_counts['with_feedback']['complete']} "
                f"({percent(complete_strict_after, status_counts['with_feedback']['complete'])}) |"
            ),
        ]
    )

    lines.extend(
        [
            "",
            "## Completeness crossed with proof status",
            "",
            "| Feedback phase | Completeness group | Proof status | Targets |",
            "|---|---|---|---:|",
        ]
    )
    for phase in ("no_feedback", "with_feedback"):
        for completeness in (
            "complete",
            "checker_valid_noncomplete",
            "invalid_or_no_spec",
        ):
            for proof_status, count in sorted(
                proof_by_completeness[phase][completeness].items()
            ):
                lines.append(
                    f"| `{phase}` | `{completeness}` | `{proof_status}` | {count} |"
                )

    lines.extend(
        [
            "",
            "## Why no specification was produced",
            "",
            "| Reason | Meaning | No feedback | With feedback | With-feedback share |",
            "|---|---|---:|---:|---:|",
        ]
    )
    all_reasons = sorted(
        set(no_spec_reasons["no_feedback"]) | set(no_spec_reasons["with_feedback"]),
        key=lambda value: (
            -no_spec_reasons["with_feedback"][value],
            value,
        ),
    )
    for value in all_reasons:
        lines.append(
            f"| `{value}` | {REASON_DESCRIPTIONS[value]} "
            f"| {no_spec_reasons['no_feedback'][value]} "
            f"| {no_spec_reasons['with_feedback'][value]} "
            f"| {percent(no_spec_reasons['with_feedback'][value], merged_status_counts['with_feedback']['no_spec_or_checker_failure'])} |"
        )
    lines.extend(
        [
            "",
            "Detailed paired rows are in `records.csv`; machine-readable totals",
            "and the full transition matrix are in `summary.json`.",
        ]
    )
    (OUT / "SUMMARY.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary["status_counts"], indent=2))
    print(json.dumps(summary["no_spec_reason_counts"], indent=2))


if __name__ == "__main__":
    main()
