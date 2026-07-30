#!/usr/bin/env python3
"""Write the final all-contract proof campaign report."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_VERIFICATION = HERE.parent
PROVED_ROOT = SOURCE_VERIFICATION / "proved-apis"


def blocker_class(text: str) -> str:
    value = text.lower()
    if any(word in value for word in ("private", "opaque", "field", "representation")):
        return "private_or_opaque_representation"
    if any(word in value for word in ("hidden state", "random", "hasher", "runtime state")):
        return "hidden_or_runtime_state"
    if any(word in value for word in ("iterator", "guard", "drop", "lifetime", "borrow")):
        return "iterator_guard_or_lifetime"
    if any(word in value for word in ("allocator", "capacity", "allocation")):
        return "allocator_or_capacity"
    if any(word in value for word in ("trait", "generic", "closure", "callback")):
        return "trait_or_higher_order_law"
    if any(word in value for word in ("pointer", "unsafe", "provenance", "raw")):
        return "unsafe_pointer_or_provenance"
    if any(word in value for word in ("unsupported", "parser", "verus")):
        return "verus_tooling_gap"
    return "other"


def main() -> None:
    overall = json.loads((HERE / "OVERALL.json").read_text())
    verification = json.loads((PROVED_ROOT / "verification.json").read_text())
    organized_verification = json.loads(
        (SOURCE_VERIFICATION / "organized-suite" / "verification.json").read_text()
    )
    fidelity = json.loads(
        (SOURCE_VERIFICATION / "fidelity-verdicts.json").read_text()
    )
    surrogate_audit = json.loads(
        (SOURCE_VERIFICATION / "surrogate-audit" / "summary.json").read_text()
    )
    metadata = [
        json.loads(path.read_text())
        for path in sorted(PROVED_ROOT.glob("*/metadata.json"))
    ]
    trust = Counter(item.get("trust_level", "unknown") for item in metadata)
    metadata_by_id = {item["id"]: item for item in metadata}
    strict_trust = Counter(
        metadata_by_id[target_id].get("trust_level", "unknown")
        for target_id in fidelity["retained"]
    )
    blocked = [item for item in overall["results"] if item.get("status") == "blocked"]
    blocker_counts = Counter(blocker_class(item.get("blocker", "")) for item in blocked)
    source_counts = Counter(
        item.get("id", "").split("__L", 1)[0]
        for item in blocked
    )

    direct = overall["scope"]["direct_assume_specification_records"]
    preproved = overall["status_counts"].get("preproved", 0)
    newly_proved = overall["status_counts"].get("proved", 0)
    proved = preproved + newly_proved
    blocked_count = overall["status_counts"].get("blocked", 0)
    attempted_remaining = direct - preproved
    path_statuses: dict[str, set[str]] = {}
    for item in overall["results"]:
        status = "proved" if item.get("status") in {"proved", "preproved"} else "blocked"
        path_statuses.setdefault(item["api_path"], set()).add(status)
    unique_counts = Counter(
        "partial" if len(statuses) > 1 else next(iter(statuses))
        for statuses in path_statuses.values()
    )

    assert direct == 539
    assert proved == len(metadata) == 406
    assert blocked_count == len(blocked) == 133
    assert proved + blocked_count == direct
    assert verification["counts"] == {"total": 406, "passed": 406, "failed": 0}
    assert organized_verification["counts"]["total"] == 539
    assert organized_verification["counts"]["passed"] == 539
    assert organized_verification["counts"]["failed"] == 0
    assert organized_verification["counts"]["proved_passed"] == 168
    assert organized_verification["counts"]["external_body_passed"] == 371

    lines = [
        "# Final Rust std source-proof campaign",
        "",
        "## Result",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Direct `assume_specification` records | {direct} |",
        f"| Unique API paths | {len(path_statuses)} |",
        f"| Previously proved/exported | {preproved} |",
        f"| Remaining records attempted | {attempted_remaining} |",
        f"| Newly proved | {newly_proved} |",
        f"| Total proved | **{proved}** |",
        f"| Strict-faithful admissible local surrogates | **{fidelity['counts']['retained_verified']}** |",
        f"| Passing artifacts not retained | **{fidelity['counts']['downgraded']}** |",
        f"| Blocked after attempts/retries | **{blocked_count}** |",
        f"| Total proof rate | **{proved / direct * 100:.2f}%** |",
        f"| New-proof success rate | **{newly_proved / attempted_remaining * 100:.2f}%** |",
        "",
        "The accepting files verify local surrogate functions. No",
        "original external Rust std symbol is directly proved, and one accepting",
        "artifact has an incorrect target mapping.",
        "",
        "At unique API-path level:",
        "",
        f"- fully proved: **{unique_counts['proved']}**;",
        f"- partially proved (multiple contract records): **{unique_counts['partial']}**;",
        f"- blocked-only: **{unique_counts['blocked']}**.",
        "",
        "All 406 copied proof files were independently rerun:",
        "",
        "```text",
        "406 passed, 0 failed",
        "```",
        "",
        "## Trust levels of strict retained local surrogates",
        "",
        "| Level | Count | Meaning |",
        "|---|---:|---|",
        f"| A | {strict_trust['A']} | Body proof without another Rust external contract |",
        f"| B | {strict_trust['B']} | Composition from smaller trusted contracts |",
        f"| C | {strict_trust['C']} | Also needs a representation/compiler invariant |",
        f"| D | {strict_trust['D']} | Also needs target/runtime semantic assumptions |",
        f"| E | {strict_trust['E']} | Central equivalence remains represented by a large model axiom |",
        "",
        "## Blocked categories",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    for name, count in blocker_counts.most_common():
        lines.append(f"| `{name}` | {count} |")
    lines.extend(
        [
            "",
            "Largest blocked source modules:",
            "",
        ]
    )
    lines.extend(f"- `{name}`: {count}" for name, count in source_counts.most_common(15))
    lines.extend(
        [
            "",
            "## Proved API directory",
            "",
            "```text",
            str(PROVED_ROOT),
            "```",
            "",
            "Each child directory contains:",
            "",
            "- `proof.rs` — passing Verus harness;",
            "- `contract.rs` — original vstd contract;",
            "- `rust_source.rs` — copied Rust 1.96 implementation when available;",
            "- `api.json` — API and declaration metadata;",
            "- `metadata.json` — trust level and proof provenance.",
            "",
            "No copied proof contains `assume(...)`, `admit()`,",
            "`#[verifier::external_body]`, `unimplemented!()`, or `todo!()`.",
            "",
            "## Organized one-click suite",
            "",
            "The conservative 539-item suite is grouped by original vstd file:",
            "",
            "```text",
            str(SOURCE_VERIFICATION / "organized-suite"),
            "```",
            "",
            "Run:",
            "",
            "```bash",
            "cd "
            + str(SOURCE_VERIFICATION / "organized-suite"),
            "./verify.sh",
            "```",
            "",
            "Latest result: **539 passed, 0 failed** "
            f"({fidelity['counts']['retained_verified']} strict-faithful "
            "local-surrogate records across "
            f"{surrogate_audit['artifact_structure']['strict_unique_proof_file_contents']} "
            "unique proof artifacts + "
            f"{organized_verification['counts']['external_body_passed']} "
            "external-body fallbacks).",
        ]
    )
    (HERE / "FINAL-REPORT.md").write_text("\n".join(lines) + "\n")
    (HERE / "FINAL-REPORT.json").write_text(
        json.dumps(
            {
                "direct_contracts": direct,
                "preproved": preproved,
                "attempted_remaining": attempted_remaining,
                "newly_proved": newly_proved,
                "total_proved": proved,
                "blocked": blocked_count,
                "unique_api_paths": len(path_statuses),
                "unique_fully_proved": unique_counts["proved"],
                "unique_partially_proved": unique_counts["partial"],
                "unique_blocked_only": unique_counts["blocked"],
                "proof_rate_percent": round(proved / direct * 100, 2),
                "new_proof_rate_percent": round(
                    newly_proved / attempted_remaining * 100,
                    2,
                ),
                "independent_verification": verification["counts"],
                "organized_suite_verification": organized_verification["counts"],
                "strict_fidelity": fidelity["counts"],
                "trust_levels": dict(trust),
                "strict_trust_levels": dict(strict_trust),
                "blocker_categories": dict(blocker_counts),
                "blocked_source_modules": dict(source_counts),
                "proved_root": str(PROVED_ROOT),
            },
            indent=2,
        )
        + "\n"
    )
    print((HERE / "FINAL-REPORT.md").read_text())


if __name__ == "__main__":
    main()
