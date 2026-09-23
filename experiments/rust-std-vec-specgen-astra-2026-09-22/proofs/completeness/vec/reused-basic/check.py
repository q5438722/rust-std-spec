import json
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[4]
CHECKER = Path("/home/chentianyu/spec-determinism-tool/.venv/bin/specdet")
VERUS = ROOT / "toolchains/verus-x86-linux/verus"


def run(output, name, arguments, timeout):
    command = [
        "bash", str(ROOT / "scripts/with_baseline.sh"),
        "env", f"TMPDIR={output / 'tmp'}", *map(str, arguments),
    ]
    started = time.time_ns()
    if name == "scratch-config":
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
        output.mkdir(parents=True, exist_ok=True)
        (output / f"{name}.stdout").write_text(result.stdout)
        (output / f"{name}.stderr").write_text(result.stderr)
    else:
        with (output / f"{name}.json").open("w") as stdout, (
            output / f"{name}.stderr"
        ).open("w") as stderr:
            try:
                result = subprocess.run(
                    command, cwd=ROOT, stdout=stdout, stderr=stderr, timeout=timeout,
                )
            except subprocess.TimeoutExpired:
                (output / f"{name}.command.json").write_text(json.dumps(command, indent=2) + "\n")
                (output / f"{name}.result.json").write_text(json.dumps({
                    "returncode": None, "timed_out": True, "started_ns": started,
                    "finished_ns": time.time_ns(),
                }, indent=2) + "\n")
                raise
    (output / f"{name}.command.json").write_text(json.dumps(command, indent=2) + "\n")
    (output / f"{name}.result.json").write_text(json.dumps({
        "returncode": result.returncode, "timed_out": False,
        "started_ns": started, "finished_ns": time.time_ns(),
    }, indent=2) + "\n")
    result.check_returncode()
    if name != "scratch-config":
        json.loads((output / f"{name}.json").read_text())


def main():
    output = Path(sys.argv[1]).resolve()
    if output.exists():
        raise FileExistsError(output)
    run(output, "scratch-config", [
        sys.executable, ROOT / "scripts/borrowed_scratch_config.py", output,
    ], 115)
    (output / "tmp").mkdir(exist_ok=True)
    run(output, "analyze", [
        CHECKER, "analyze", "--config", output / "specdet.toml",
        "--target", "vec/reused_basic.rs", "--json",
    ], 240)
    runs = list((output / "analysis-runs").iterdir())
    if len(runs) != 1 or not runs[0].is_dir():
        raise AssertionError(f"Expected one native analysis run, found {runs}")
    run(output, "replay", [
        CHECKER, "replay", "--run", runs[0], "--reexecute",
        "--verus", VERUS, "--out", output / "replay-runs", "--json",
    ], 240)
    print(f"Native analyze and replay outputs: {output}")


if __name__ == "__main__":
    main()
