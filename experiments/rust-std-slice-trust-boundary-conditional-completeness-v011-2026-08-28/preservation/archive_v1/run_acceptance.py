#!/usr/bin/env python3
"""Run and capture the fresh build/test/read-only acceptance commands."""

from __future__ import annotations

import csv
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common


OUT = common.OUT
LOGS = OUT / "logs"
THEOREM_SOLVER_STEM = "04_theorem_template_z3"
UNIT_TEST_STEMS = {
    "01b_operational_v2_certification_tests",
    "02_unit_tests",
}
HEARTBEAT_SECONDS = 20
TARGET_078_ADAPTER_CPU_LIST = "0-3"


def _timeout_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value


def command_timeout(stem: str) -> int:
    if stem in {
        "02_unit_tests",
        "21_pointer_cast_cluster_replay",
        "28_maybeuninit_lifecycle_cluster",
    }:
        return 900
    if stem in {
        "44b_target_079_operational_v1",
        "44c_target_079_adapter_refinement_v2",
        "44d_target_078_adapter_refinement_v2",
        "44e_target_078_insert_tail_refinement_v3",
        "44f_target_079_insert_tail_refinement_v3",
        "44g_target_080_operational_v1",
    }:
        return 600
    return 110


def unittest_count(stdout: str, stderr: str) -> int | None:
    matches = re.findall(r"^Ran ([0-9]+) tests? in ", stdout + stderr, re.MULTILINE)
    if len(matches) != 1:
        return None
    return int(matches[0])


def target_078_adapter_command(python: str) -> list[str]:
    taskset = shutil.which("taskset")
    if taskset is None:
        raise RuntimeError(
            "taskset is required for reproducible target-078 diagnostics"
        )
    return [
        taskset,
        "-c",
        TARGET_078_ADAPTER_CPU_LIST,
        python,
        "tools/run_target_078_adapter_refinement_v2.py",
    ]


def capture(
    stem: str,
    argv: list[str],
    *,
    cwd: Path,
    timeout: int = 110,
) -> dict[str, Any]:
    LOGS.mkdir(parents=True, exist_ok=True)
    command = LOGS / f"{stem}.command.txt"
    stdout = LOGS / f"{stem}.stdout.txt"
    stderr = LOGS / f"{stem}.stderr.txt"
    status = LOGS / f"{stem}.status.txt"
    command.write_text(shlex.join(argv) + "\n")
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    print(f"acceptance_command_start={stem}", flush=True)
    process = subprocess.Popen(
        argv,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    started_at = time.monotonic()
    while True:
        elapsed = time.monotonic() - started_at
        remaining = timeout - elapsed
        if remaining <= 0:
            process.kill()
            out, err = process.communicate()
            out = _timeout_text(out)
            err = _timeout_text(err)
            if err and not err.endswith("\n"):
                err += "\n"
            err += "command timed out\n"
            return_code = 124
            break
        try:
            out, err = process.communicate(
                timeout=min(HEARTBEAT_SECONDS, remaining)
            )
            return_code = process.returncode
            break
        except subprocess.TimeoutExpired:
            print(
                f"acceptance_command_heartbeat={stem} "
                f"elapsed_seconds={int(time.monotonic() - started_at)}",
                flush=True,
            )
    out = _timeout_text(out)
    err = _timeout_text(err)
    stdout.write_text(out)
    stderr.write_text(err)
    status.write_text(f"{return_code}\n")
    print(
        f"acceptance_command_done={stem} exit_code={return_code}",
        flush=True,
    )
    return {
        "stem": stem,
        "argv": argv,
        "cwd": str(cwd),
        "command": common.relpath(command),
        "stdout": common.relpath(stdout),
        "stderr": common.relpath(stderr),
        "status": common.relpath(status),
        "exit_code": return_code,
    }


def inventory_expectations() -> tuple[int, int]:
    path = common.SPECGEN / "inventory/slice_exec_fn_inventory.csv"
    with path.open(newline="") as handle:
        stable = [
            row for row in csv.DictReader(handle) if row["stability"] == "stable"
        ]
    return (
        len(stable),
        sum(row["existing_vstd_status"] == "existing-vstd" for row in stable),
    )


def clean_bytecode() -> None:
    for path in (OUT / "tools/__pycache__", OUT / "tests/__pycache__"):
        if path.exists():
            shutil.rmtree(path)


def main(*, start_at: str | None = None) -> None:
    python = sys.executable
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required to replay the theorem template")
    total, existing = inventory_expectations()
    commands = [
        (
            "01_compileall",
            [python, "-m", "compileall", "-f", "-q", "tools", "tests"],
            OUT,
        ),
        (
            "44c_target_079_adapter_refinement_v2",
            [python, "tools/run_target_079_adapter_refinement_v2.py"],
            OUT,
        ),
        (
            "44d_target_078_adapter_refinement_v2",
            target_078_adapter_command(python),
            OUT,
        ),
        (
            "03_builder",
            [python, "tools/build_authority_design.py"],
            OUT,
        ),
        (
            THEOREM_SOLVER_STEM,
            [
                z3,
                "-smt2",
                str(OUT / "crosswalk/conditional_theorem_template.smt2"),
            ],
            OUT,
        ),
        (
            "05_target_029_pipeline",
            [python, "tools/run_target_029.py"],
            OUT,
        ),
        (
            "06_target_013_pipeline",
            [python, "tools/run_target_013.py"],
            OUT,
        ),
        (
            "07_target_106_pipeline",
            [python, "tools/run_target_106.py"],
            OUT,
        ),
        (
            "08_target_081_pipeline",
            [python, "tools/run_target_081.py"],
            OUT,
        ),
        (
            "09_target_022_pipeline",
            [python, "tools/run_target_022.py"],
            OUT,
        ),
        (
            "10_target_120_pipeline",
            [python, "tools/run_target_120.py"],
            OUT,
        ),
        (
            "16_target_051_pipeline",
            [python, "tools/run_target_051.py"],
            OUT,
        ),
        (
            "17_target_052_pipeline",
            [python, "tools/run_target_052.py"],
            OUT,
        ),
        (
            "18_target_019_pipeline",
            [python, "tools/run_target_019.py"],
            OUT,
        ),
        (
            "19_target_021_pipeline",
            [python, "tools/run_target_021.py"],
            OUT,
        ),
        (
            "20_target_020_pipeline",
            [python, "tools/run_target_020.py"],
            OUT,
        ),
        (
            "21_pointer_cast_cluster_replay",
            [python, "tools/run_pointer_cast_cluster.py"],
            OUT,
        ),
        (
            "23_target_028_pipeline",
            [python, "tools/run_target_028.py"],
            OUT,
        ),
        (
            "24_target_030_pipeline",
            [python, "tools/run_target_030.py"],
            OUT,
        ),
        (
            "25_target_065_pipeline",
            [python, "tools/run_target_065.py"],
            OUT,
        ),
        (
            "26_search_family_cluster_replay",
            [python, "tools/run_search_family_cluster.py"],
            OUT,
        ),
        (
            "27_chunk_contract_drift_cluster_replay",
            [python, "tools/run_chunk_contract_drift_cluster.py"],
            OUT,
        ),
        (
            "28_maybeuninit_lifecycle_cluster",
            [python, "tools/run_maybeuninit_lifecycle_cluster.py"],
            OUT,
        ),
        (
            "29_unstable_sort_companions",
            [python, "tools/run_unstable_sort_companions.py"],
            OUT,
        ),
        (
            "30_target_077_pipeline",
            [python, "tools/run_target_077.py"],
            OUT,
        ),
        (
            "31_selection_callback_cluster",
            [python, "tools/run_selection_callback_cluster.py"],
            OUT,
        ),
        (
            "32_mutable_iterator_constructor_cluster",
            [python, "tools/run_mutable_iterator_constructors.py"],
            OUT,
        ),
        (
            "33_mutable_edge_extraction_cluster",
            [python, "tools/run_mutable_edge_extraction.py"],
            OUT,
        ),
        (
            "34_clone_effect_cluster",
            [python, "tools/run_clone_effect_cluster.py"],
            OUT,
        ),
        (
            "35_exact_mutable_iterator_partition_cluster",
            [python, "tools/run_exact_mutable_iterator_partitions.py"],
            OUT,
        ),
        (
            "36_mutable_fixed_chunk_edge_cluster",
            [python, "tools/run_mutable_fixed_chunk_edges.py"],
            OUT,
        ),
        (
            "37_split_at_mut_primitive_cluster",
            [python, "tools/run_split_at_mut_primitives.py"],
            OUT,
        ),
        (
            "38_split_off_pair_cluster",
            [python, "tools/run_split_off_pair.py"],
            OUT,
        ),
        (
            "39_raw_slice_pair_cluster",
            [python, "tools/run_raw_slice_pair.py"],
            OUT,
        ),
        (
            "40_slice_index_trio",
            [python, "tools/run_slice_index_trio.py"],
            OUT,
        ),
        (
            "41_address_observer_pair",
            [python, "tools/run_address_observer_pair.py"],
            OUT,
        ),
        (
            "42_mutable_view_construction_cluster",
            [python, "tools/run_mutable_view_construction_cluster.py"],
            OUT,
        ),
        (
            "43_align_to_pair",
            [python, "tools/run_align_to_pair.py"],
            OUT,
        ),
        (
            "11_slice_inventory",
            [
                python,
                "verification/check_inventory.py",
                "--modules-csv",
                "results/modules.csv",
                "--inventory",
                "inventory/slice_exec_fn_inventory.csv",
                "--expect-total",
                str(total),
                "--expect-existing-vstd",
                str(existing),
            ],
            common.SPECGEN,
        ),
        (
            "12_slice_catalog",
            [
                python,
                "verification/check_catalog.py",
                "--inventory",
                "inventory/slice_exec_fn_inventory.csv",
                "--catalog",
                "catalog/slice_spec_catalog.csv",
                "--expect-total",
                str(total),
                "--expect-existing-vstd",
                str(existing),
            ],
            common.SPECGEN,
        ),
        (
            "13_slice_contracts",
            [
                python,
                "verification/check_contracts.py",
                "--specs",
                "specs/all_slice_specs.rs",
                "--inventory",
                "inventory/slice_exec_fn_inventory.csv",
                "--catalog",
                "catalog/slice_spec_catalog.csv",
            ],
            common.SPECGEN,
        ),
        (
            "14_slice_provenance",
            [
                python,
                "verification/check_provenance.py",
                "--root",
                ".",
                "--rust-copy",
                "rust-core-slice",
                "--vstd-copy",
                "vstd-baseline",
            ],
            common.SPECGEN,
        ),
        (
            "15_implproof_aggregate",
            [
                python,
                str(common.IMPLPROOF / "tools/check_implproof_aggregate.py"),
            ],
            common.SURVEY,
        ),
        (
            "44a_target_078_operational_v1",
            [python, "tools/run_target_078_operational_v1.py"],
            OUT,
        ),
        (
            "44g_target_080_operational_v1",
            [python, "tools/run_target_080_operational_v1.py"],
            OUT,
        ),
        (
            "44b_target_079_operational_v1",
            [python, "tools/run_target_079_operational_v1.py"],
            OUT,
        ),
        (
            "44_final_reconciliation",
            [python, "tools/run_final_reconciliation.py"],
            OUT,
        ),
        (
            "45_operational_v2_reconciliation",
            [python, "tools/run_operational_v2_reconciliation.py"],
            OUT,
        ),
        (
            "46_operational_v2_certification_closure",
            [python, "tools/run_operational_v2_certification_closure.py"],
            OUT,
        ),
        (
            "44e_target_078_insert_tail_refinement_v3",
            [python, "tools/run_target_078_insert_tail_refinement_v3.py"],
            OUT,
        ),
        (
            "44f_target_079_insert_tail_refinement_v3",
            [python, "tools/run_target_079_insert_tail_refinement_v3.py"],
            OUT,
        ),
        (
            "01b_operational_v2_certification_tests",
            [
                python,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_operational_v2_certification.py",
                "-v",
            ],
            OUT,
        ),
        (
            "02_unit_tests",
            [python, "-m", "unittest", "discover", "-s", "tests", "-v"],
            OUT,
        ),
        (
            "22_local_validator",
            [python, "tools/validate_authority_design.py"],
            OUT,
        ),
    ]

    records: list[dict[str, Any]] = []
    started = start_at is None
    try:
        for stem, argv, cwd in commands:
            if not started:
                if stem != start_at:
                    continue
                started = True
            record = capture(
                stem,
                argv,
                cwd=cwd,
                timeout=command_timeout(stem),
            )
            if stem == THEOREM_SOLVER_STEM:
                solver_stdout = (
                    LOGS / f"{THEOREM_SOLVER_STEM}.stdout.txt"
                ).read_text()
                solver_stderr = (
                    LOGS / f"{THEOREM_SOLVER_STEM}.stderr.txt"
                ).read_text()
                record.update(
                    {
                        "expected_solver_result": "unsat",
                        "stdout_exact_match": solver_stdout == "unsat\n",
                        "stderr_empty": solver_stderr == "",
                    }
                )
            if stem in UNIT_TEST_STEMS:
                tests_run = unittest_count(
                    (LOGS / f"{stem}.stdout.txt").read_text(),
                    (LOGS / f"{stem}.stderr.txt").read_text(),
                )
                record.update(
                    {
                        "tests_run": tests_run,
                        "tests_nonzero": (
                            tests_run is not None and tests_run > 0
                        ),
                    }
                )
            records.append(record)
            if (
                record["exit_code"] != 0
                or record.get("stdout_exact_match") is False
                or record.get("stderr_empty") is False
                or record.get("tests_nonzero") is False
            ):
                common.write_json(
                    LOGS / "acceptance_manifest.json",
                    {"status": "failed", "commands": records},
                )
                print(f"acceptance=FAIL command={stem}")
                raise SystemExit(record["exit_code"] or 1)
        if not started:
            raise RuntimeError(f"unknown acceptance start stem: {start_at}")
    finally:
        clean_bytecode()

    common.write_json(
        LOGS / "acceptance_manifest.json",
        {"status": "passed", "commands": records},
    )
    print("acceptance=PASS")
    print(f"commands={len(records)}")
    print(f"slice_inventory_total={total} existing_vstd={existing}")


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if not arguments:
        main()
    elif len(arguments) == 2 and arguments[0] == "--start-at":
        main(start_at=arguments[1])
    else:
        raise SystemExit("usage: run_acceptance.py [--start-at STEM]")
