#!/usr/bin/env python3
"""Re-run typechecking and determinism on final generated contracts."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import run_rust_std_spec_feedback as runner
from spec_determinism.view.registry import ViewRegistry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument("batch_summary", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--vstd-root",
        type=Path,
        default=workspace / "verus" / "source" / "vstd",
    )
    parser.add_argument(
        "--verus-bin",
        type=Path,
        default=workspace
        / "verus"
        / "source"
        / "target-verus"
        / "release"
        / "verus",
    )
    parser.add_argument(
        "--z3-path",
        type=Path,
        default=workspace / "verus" / "source" / "z3",
    )
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--rlimit", type=float, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = json.loads(args.batch_summary.read_text())
    manifest_payload = json.loads(args.manifest.read_text())
    entries = {
        entry["target"]: entry
        for entry in manifest_payload.get("targets", manifest_payload)
    }
    logging.getLogger("spec_determinism").setLevel(logging.ERROR)
    registry = ViewRegistry.from_project(args.vstd_root)
    changed = 0
    for result in payload["results"]:
        final = result.get("final") or {}
        candidate = final.get("candidate") or {}
        recovered_from_history = False
        if not candidate:
            for record in reversed(result.get("history") or []):
                prior = record.get("candidate") or {}
                if prior.get("decision") == "add_spec" and prior.get(
                    "contract_code"
                ):
                    final = dict(record)
                    candidate = prior
                    recovered_from_history = True
                    break
        if candidate.get("decision") != "add_spec" or not candidate.get(
            "contract_code"
        ):
            continue
        entry = entries[result["target"]]
        target_dir = (
            args.batch_summary.parent
            / "targets"
            / runner.safe_name(result["target"])
        )
        recheck_dir = target_dir / "recheck_final"
        recheck_dir.mkdir(parents=True, exist_ok=True)
        contract_path = recheck_dir / "contract_harness.rs"
        contract_path.write_text(runner.build_contract_harness(candidate))
        typecheck = runner.run_verus(
            verus_bin=args.verus_bin,
            z3_path=args.z3_path,
            file_path=contract_path,
            timeout=args.timeout,
            rlimit=args.rlimit,
        )
        (recheck_dir / "typecheck_stdout.txt").write_text(typecheck["stdout"])
        (recheck_dir / "typecheck_stderr.txt").write_text(typecheck["stderr"])
        checker = None
        if (
            typecheck["returncode"] == 0
            and candidate.get("contract_form") == "assume_specification"
        ):
            checker = runner.run_determinism(
                candidate=candidate,
                round_dir=recheck_dir,
                view_registry=registry,
                verus_bin=args.verus_bin,
                z3_path=args.z3_path,
                timeout=args.timeout,
                rlimit=args.rlimit,
            )
        issues = runner.anti_vacuity_issues(
            entry,
            candidate,
            typecheck,
            checker,
        )
        raw_reward = int(
            checker is not None
            and checker.get("status") == "ok"
            and checker.get("r0_z3") == "unsat"
        )
        guarded_reward = int(
            raw_reward == 1
            and typecheck["returncode"] == 0
            and not issues
        )
        final.update(
            {
                "checker": runner.checker_summary(typecheck, checker),
                "anti_vacuity_issues": issues,
                "raw_det_reward": raw_reward,
                "guarded_reward": guarded_reward,
                "soundness_status": "unverified_trusted_external_contract",
                "apply_upstream": False,
                "rechecked": True,
            }
        )
        if result.get("history"):
            if recovered_from_history:
                result["history"].append(final)
            else:
                result["history"][-1] = final
        result["final"] = final
        (target_dir / "summary.json").write_text(
            json.dumps(result, indent=2) + "\n"
        )
        changed += 1

    runner.write_batch_summary(
        args.batch_summary.parent,
        payload["results"],
        payload["metadata"],
    )
    print(f"rechecked {changed} add-spec candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
