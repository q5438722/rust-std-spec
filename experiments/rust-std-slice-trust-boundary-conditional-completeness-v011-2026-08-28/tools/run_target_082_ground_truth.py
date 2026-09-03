#!/usr/bin/env python3
"""Compile and capture Rust 1.96 target-082 lifecycle behavior."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/probes/target_082_adapter_probe.rs"
OUT = ROOT / "evidence/target_082_operational_v1/ground_truth"
TOOLCHAIN = "1.96.0-x86_64-unknown-linux-gnu"
SCENARIOS: dict[str, int | str] = {
    "normal": 0,
    "trivial": 0,
    "zst": 0,
    "duplicate-equal-keys": 0,
    "interior-mutation": 0,
    "left-key-panic": 101,
    "right-key-panic": 101,
    "ord-lt-panic": 101,
    "right-drop-panic": 101,
    "left-drop-panic": 101,
    "ord-lt-panic-right-drop-double-panic": "abort",
    "right-left-drop-double-panic": "abort",
    "f-drop-panic": 101,
    "key-panic-f-drop-double-panic": "abort",
}
ORDERED_EVENTS = {
    "normal": (
        "event=key-left",
        "event=key-right",
        "event=ord-lt",
        "event=drop-key-right",
        "event=drop-key-left",
        "event=drop-f",
        "event=target-return",
    ),
    "right-key-panic": (
        "event=key-left",
        "event=key-right",
        "event=drop-key-left",
        "event=drop-f",
    ),
    "ord-lt-panic": (
        "event=key-left",
        "event=key-right",
        "event=ord-lt",
        "event=drop-key-right",
        "event=drop-key-left",
        "event=drop-f",
    ),
    "right-drop-panic": (
        "event=key-left",
        "event=key-right",
        "event=ord-lt",
        "event=drop-key-right",
        "event=drop-key-left",
        "event=drop-f",
    ),
    "ord-lt-panic-right-drop-double-panic": (
        "event=key-left",
        "event=key-right",
        "event=ord-lt",
        "event=drop-key-right",
    ),
    "right-left-drop-double-panic": (
        "event=key-left",
        "event=key-right",
        "event=ord-lt",
        "event=drop-key-right",
        "event=drop-key-left",
    ),
    "key-panic-f-drop-double-panic": (
        "event=key-left",
        "event=drop-f",
    ),
}


def _run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )


def _validate_scenario(
    scenario: str,
    expected: int | str,
    process: subprocess.CompletedProcess[str],
) -> None:
    if expected == "abort":
        if process.returncode in (0, 101):
            raise RuntimeError(
                f"{scenario}: expected abort, got {process.returncode}"
            )
    elif process.returncode != expected:
        raise RuntimeError(
            f"{scenario}: expected {expected}, got {process.returncode}"
        )
    position = -1
    for token in ORDERED_EVENTS.get(scenario, ()):
        next_position = process.stderr.find(token, position + 1)
        if next_position < 0:
            raise RuntimeError(
                f"{scenario}: missing ordered event {token!r}"
            )
        position = next_position


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-scenario", choices=tuple(SCENARIOS))
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.check_scenario is None:
        OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory)
        executable = temporary / "target_082_adapter_probe"
        mir = temporary / "target_082_adapter_probe.mir"
        compile_argv = [
            "rustup",
            "run",
            TOOLCHAIN,
            "rustc",
            "--edition=2021",
            "-C",
            "panic=unwind",
            str(SOURCE),
            "-o",
            str(executable),
        ]
        compiled = _run(compile_argv)
        if compiled.returncode != 0:
            raise RuntimeError(compiled.stderr)
        if args.check_scenario is not None:
            scenario = args.check_scenario
            process = _run([str(executable), scenario])
            _validate_scenario(scenario, SCENARIOS[scenario], process)
            print(
                f"scenario={scenario} exit_code={process.returncode} "
                "status=passed"
            )
            return

        emitted = _run(
            [
                "rustup",
                "run",
                TOOLCHAIN,
                "rustc",
                "--edition=2021",
                "-C",
                "panic=unwind",
                "--emit=mir",
                str(SOURCE),
                "-o",
                str(mir),
            ]
        )
        if emitted.returncode != 0:
            raise RuntimeError(emitted.stderr)
        (OUT / "probe.mir").write_text(mir.read_text())

        captures: dict[str, dict[str, object]] = {}
        for scenario, expected in SCENARIOS.items():
            process = _run([str(executable), scenario])
            _validate_scenario(scenario, expected, process)
            scenario_root = OUT / scenario
            scenario_root.mkdir(parents=True, exist_ok=True)
            replay_command = (
                "python3 tools/run_target_082_ground_truth.py "
                f"--check-scenario {scenario}"
            )
            (scenario_root / "command.txt").write_text(
                replay_command + "\n"
            )
            (scenario_root / "stdout.txt").write_text(process.stdout)
            (scenario_root / "stderr.txt").write_text(process.stderr)
            (scenario_root / "status.txt").write_text(
                f"{process.returncode}\n"
            )
            captures[scenario] = {
                "expected": expected,
                "exit_code": process.returncode,
                "ordered_events": list(ORDERED_EVENTS.get(scenario, ())),
                "stderr": (
                    "evidence/target_082_operational_v1/ground_truth/"
                    f"{scenario}/stderr.txt"
                ),
                "replay_command": replay_command,
            }

    version = _run(["rustup", "run", TOOLCHAIN, "rustc", "--version"])
    if version.returncode != 0:
        raise RuntimeError(version.stderr)
    manifest = {
        "schema_version": 1,
        "target": "core::slice::sort_unstable_by_key",
        "input_order": "82",
        "toolchain": version.stdout.strip(),
        "source": "research/probes/target_082_adapter_probe.rs",
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "mir": (
            "evidence/target_082_operational_v1/ground_truth/probe.mir"
        ),
        "replay_all_command": "python3 tools/run_target_082_ground_truth.py",
        "scenarios": captures,
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(
        "captured target-082 key-sort ground truth: "
        f"{len(captures)} scenarios"
    )


if __name__ == "__main__":
    main()
