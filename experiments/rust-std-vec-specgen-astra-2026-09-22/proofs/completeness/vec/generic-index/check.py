"""Analyze and reexecute only the current generic Vec Index contract."""

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import tomllib


ROOT = Path(__file__).resolve().parents[4]
VERUS = ROOT / "toolchains/verus-x86-linux/verus"
SPECDET = Path("/home/chentianyu/spec-determinism-tool/.venv/bin/specdet")
TARGET = "vec/index.rs::vec::index::index_source"


def run(output, name, command):
    (output / f"{name}.command.json").write_text(json.dumps(command, indent=2) + "\n")
    started = time.time_ns()
    try:
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, timeout=600
        )
    except subprocess.TimeoutExpired as error:
        for suffix, value in (("stdout", error.stdout), ("stderr", error.stderr)):
            if isinstance(value, bytes):
                value = value.decode(errors="replace")
            (output / f"{name}.{suffix}").write_text(value or "")
        (output / f"{name}.result.json").write_text(json.dumps({
            "returncode": None, "timed_out": True,
            "started_ns": started, "finished_ns": time.time_ns(),
        }, indent=2) + "\n")
        raise
    (output / f"{name}.stdout").write_text(result.stdout)
    (output / f"{name}.stderr").write_text(result.stderr)
    (output / f"{name}.result.json").write_text(json.dumps({
        "returncode": result.returncode, "timed_out": False,
        "started_ns": started, "finished_ns": time.time_ns(),
    }, indent=2) + "\n")
    print(f"{name}: exit {result.returncode}", flush=True)
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "tmp").mkdir()
    prefix = [
        "bash", str(ROOT / "scripts/with_baseline.sh"),
        "env", f"TMPDIR={output / 'tmp'}",
    ]
    setup = run(output, "scratch-config", prefix + [
        sys.executable, str(ROOT / "scripts/borrowed_scratch_config.py"), str(output),
    ])
    setup.check_returncode()
    config = output / "specdet.toml"
    original = tomllib.loads((ROOT / "specdet.toml").read_text())
    adjusted = tomllib.loads(config.read_text())
    original["project"]["root"] = str(ROOT / "specs")
    original["adapters"]["verus"]["executable"] = str(VERUS)
    original["adapters"]["verus"]["environment"]["TMPDIR"] = str(output / "tmp")
    original["artifacts"]["output_dir"] = str(output / "analysis-runs")
    assert adjusted == original, "Scratch configuration changed more than output paths"
    analyze = run(output, "analyze", prefix + [
        str(SPECDET), "analyze", "--config", str(config),
        "--target", "vec/index.rs", "--json",
    ])
    analysis = json.loads(analyze.stdout)
    replay = run(output, "replay-selected", prefix + [
        str(SPECDET), "replay", "--run", analysis["run_dir"], "--reexecute",
        "--verus", str(VERUS), "--out", str(output / "selected-replay-runs"), "--json",
    ])
    replayed = json.loads(replay.stdout)
    failed = False
    for name, process, report in (
        ("analyze", analyze, analysis), ("replay-selected", replay, replayed)
    ):
        assert [target["qualified_name"] for target in report["targets"]] == [
            TARGET
        ], f"{name}: the checker selected an unrelated target"
        assert [result["target"]["qualified_name"] for result in report["results"]] == [
            TARGET
        ], f"{name}: expected exactly one result for the selected target"
        result = report["results"][0]
        proofs = result["proofs"]
        verified = bool(proofs) and all(
            proof["status"] == "verified" and proof["verified_goals"] > 0
            for proof in proofs
        )
        if process.returncode != 0 or report["counts"] != {"deterministic": 1} or not verified:
            failed = True
            print(
                f"{name}: completeness not proved for {TARGET} "
                f"(exit {process.returncode}, counts={report['counts']})",
                file=sys.stderr,
            )
            for diagnostic in report["diagnostics"] + result["diagnostics"]:
                print(
                    f"{name}: {diagnostic['stage']}/{diagnostic['code']}: "
                    f"{diagnostic['message']}",
                    file=sys.stderr,
                )
            if not verified:
                print(
                    f"{name}: expected a nonempty proof set with every proof verified "
                    "and every verified_goals count greater than zero",
                    file=sys.stderr,
                )
            print(f"{name}: saved report: {output / f'{name}.stdout'}", file=sys.stderr)
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
