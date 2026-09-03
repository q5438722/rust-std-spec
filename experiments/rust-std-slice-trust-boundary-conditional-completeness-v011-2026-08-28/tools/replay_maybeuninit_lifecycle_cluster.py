#!/usr/bin/env python3
"""Independently replay the three-target MaybeUninit lifecycle evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import target_025
import target_026
import target_119


TARGET_MODULES = (target_026, target_119, target_025)
OBLIGATION_STEMS = {
    target_025.PRIMARY: "obligation",
    target_025.EXACT_OUTPUT: "exact_output_obligation",
}
EXPECTED_THEOREM_RESULTS = {
    target_025.TARGET: {
        target_025.PRIMARY: "unsat",
        target_025.EXACT_OUTPUT: "unsat",
    },
    target_026.TARGET: {
        target_026.PRIMARY: "sat",
        target_026.EXACT_OUTPUT: "unsat",
    },
    target_119.TARGET: {
        target_119.PRIMARY: "unsat",
        target_119.EXACT_OUTPUT: "unsat",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_z3(path: Path, z3: str, expected: str) -> dict[str, Any]:
    process = subprocess.run(
        [z3, "-smt2", str(path)],
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    first_line = process.stdout.splitlines()[0] if process.stdout else ""
    if (
        process.returncode != 0
        or first_line != expected
        or process.stderr != ""
    ):
        raise ValueError(
            f"{path}: expected clean {expected}, got "
            f"rc={process.returncode}, stdout={process.stdout!r}, "
            f"stderr={process.stderr!r}"
        )
    return {
        "solver_result": first_line,
        "stdout_sha256": hashlib.sha256(process.stdout.encode()).hexdigest(),
        "stderr_empty": True,
    }


def replay_target_026_witness(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    witness = json.loads(raw)
    if (
        witness.get("target") != target_026.TARGET
        or witness.get("input_order") != target_026.INPUT_ORDER
        or witness.get("active_contract_sha256")
        != target_026.ACTIVE_CONTRACT_SHA256
    ):
        raise ValueError("target-026 witness identity or contract hash changed")

    input_record = witness["input"]
    boundary = witness["boundary"]
    initial_values = [slot["value"] for slot in input_record["slice"]]
    all_initial = all(slot["initialized"] for slot in input_record["slice"])
    same_boundary = (
        boundary["initial_storage"] == initial_values
        and all(
            boundary[field] == input_record[field]
            for field in (
                "allocation",
                "address",
                "provenance",
                "borrow",
                "element_size",
                "element_alignment",
                "frame_token",
            )
        )
    )

    checks: list[dict[str, bool]] = []
    for execution in (witness["execution1"], witness["execution2"]):
        returned = execution["return"]
        final_storage = execution["final_storage"]
        final_return = execution["final_return_values"]
        checks.append(
            {
                "requires_all_initialized": all_initial,
                "initial_relation_well_formed": (
                    len(initial_values) == len(input_record["slice"])
                ),
                "final_relation_well_formed": (
                    len(final_storage) == len(initial_values)
                ),
                "final_slice_length_preserved": (
                    len(final_storage) == len(initial_values)
                ),
                "return_equals_initial_values": (
                    returned["values"] == initial_values
                ),
                "return_length_preserved": (
                    len(returned["values"]) == len(initial_values)
                ),
                "final_return_length_matches_slice": (
                    len(final_return) == len(final_storage)
                ),
                "final_all_initialized": all(
                    isinstance(value, int) for value in final_storage
                ),
                "final_storage_equals_return": (
                    final_storage == final_return
                ),
                "return_identity_preserved": all(
                    returned[field] == input_record[field]
                    for field in (
                        "allocation",
                        "address",
                        "provenance",
                        "borrow",
                    )
                ),
            }
        )

    first = witness["execution1"]
    second = witness["execution2"]
    output_equal = first["return"] == second["return"]
    final_equal = (
        first["final_storage"] == second["final_storage"]
        and first["final_return_values"] == second["final_return_values"]
    )
    observed = {
        "same_valid_input": all_initial,
        "same_boundary": same_boundary,
        "execution1_satisfies_every_active_conjunct": all(checks[0].values()),
        "execution2_satisfies_every_active_conjunct": all(checks[1].values()),
        "exact_output_equal": output_equal,
        "exact_final_state_equal": final_equal,
        "full_exact_equivalent": output_equal and final_equal,
    }
    if observed != witness["expected"]:
        raise ValueError(f"target-026 witness replay mismatch: {observed!r}")
    return {
        "status": "passed",
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "active_conjuncts": {
            "execution1": checks[0],
            "execution2": checks[1],
        },
        "observed": observed,
    }


def semantic_sat_probe(module: Any, name: str) -> dict[str, Any]:
    case = module.PROBE_CASES[name]
    if case["expected"] != "sat":
        raise ValueError(f"{name}: semantic replay requested for non-SAT probe")
    if module is target_025:
        length = int(case["length"])
        chain = all(
            case["destruct_before"][index]
            == (
                case["destruct_initial_state"]
                if index == 0
                else case["destruct_after"][index - 1]
            )
            and index in case["completed"]
            for index in range(length)
        )
        return {
            "valid": (
                length >= 0
                and case["address"] > 0
                and case["element_alignment"] > 0
                and chain
            ),
            "drop_indices": list(range(length)),
            "final_initialization": [False] * length,
        }
    if module is target_026:
        length = int(case["length"])
        initialized = set(case["initialized"])
        initialized -= set(case["uninitialized"])
        return {
            "valid": (
                length >= 0
                and all(index in initialized for index in range(length))
                and case["address"] > 0
                and case["element_alignment"] > 0
            ),
            "return_identity": [
                case["allocation"],
                case["address"],
                case["provenance"],
                case["borrow"],
            ],
            "final_mutation": case.get("final_values"),
        }
    if case["kind"].startswith("panic_lifecycle"):
        return target_119.panic_probe_semantics(name)
    length = int(case["destination_length"])
    chain = all(
        case["clone_before"][index]
        == (
            case["clone_initial_state"]
            if index == 0
            else case["clone_after"][index - 1]
        )
        and index in case["completed"]
        for index in range(length)
    )
    return {
        "valid": (
            length == case["source_length"]
            and case["clone_result"] == case["source_values"]
            and chain
        ),
        "clone_indices": list(range(length)),
        "write_indices": list(range(length)),
        "final_values": [
            case["source_values"][index] for index in range(length)
        ],
    }


def replay(root: Path, z3: str) -> dict[str, Any]:
    targets: dict[str, Any] = {}
    for module in TARGET_MODULES:
        evidence_root = root / module.ARTIFACT_ID
        obligations: dict[str, Any] = {}
        for purpose, stem in OBLIGATION_STEMS.items():
            smt_path = evidence_root / f"{stem}.smt2"
            metadata_path = evidence_root / f"{stem}.metadata.json"
            if not smt_path.is_file() or not metadata_path.is_file():
                raise ValueError(f"{module.TARGET}: retained obligation is missing")
            text = smt_path.read_text()
            metadata = json.loads(metadata_path.read_text())
            module.validate_target_obligation(text, metadata)
            expected = EXPECTED_THEOREM_RESULTS[module.TARGET][purpose]
            solver = run_z3(smt_path, z3, expected)
            obligations[purpose] = {
                **solver,
                "smt_sha256": sha256(smt_path),
                "metadata_sha256": sha256(metadata_path),
            }

        probes: dict[str, Any] = {}
        for name, case in module.PROBE_CASES.items():
            path = evidence_root / "probes" / f"{name}.smt2"
            if not path.is_file():
                raise ValueError(f"{module.TARGET}/{name}: probe is missing")
            if path.read_text() != module.probe_text(name):
                raise ValueError(f"{module.TARGET}/{name}: probe text changed")
            expected = module.PROBE_EXPECTED_RESULTS[name]
            solver = run_z3(path, z3, expected)
            record: dict[str, Any] = {
                **solver,
                "kind": case["kind"],
                "smt_sha256": sha256(path),
            }
            if expected == "sat":
                semantic = semantic_sat_probe(module, name)
                if not semantic["valid"]:
                    raise ValueError(
                        f"{module.TARGET}/{name}: SAT probe is not semantically valid"
                    )
                record["semantic_replay"] = semantic
            probes[name] = record

        target_record: dict[str, Any] = {
            "target": module.TARGET,
            "input_order": module.INPUT_ORDER,
            "active_contract_sha256": module.ACTIVE_CONTRACT_SHA256,
            "obligations": obligations,
            "satisfiability_probes": probes,
        }
        if module is target_026:
            fixed_model = evidence_root / "counterexample_model.smt2"
            if fixed_model.read_text() != target_026.fixed_model_text():
                raise ValueError("target-026 fixed countermodel text changed")
            target_record["fixed_countermodel"] = {
                **run_z3(fixed_model, z3, "sat"),
                "smt_sha256": sha256(fixed_model),
            }
            target_record["witness"] = replay_target_026_witness(
                evidence_root / "witness.json"
            )
        targets[module.TARGET] = target_record

    return {
        "status": "passed",
        "targets": targets,
        "replayed_sat_witnesses": sum(
            record["solver_result"] == "sat"
            for target in targets.values()
            for record in (
                list(target["obligations"].values())
                + list(target["satisfiability_probes"].values())
            )
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--z3", required=True)
    args = parser.parse_args()
    print(json.dumps(replay(args.evidence_root, args.z3), sort_keys=True))


if __name__ == "__main__":
    main()
