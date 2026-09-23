import json
from pathlib import Path
import subprocess
import sys
import time
import tomllib


ROOT = Path(__file__).resolve().parents[4]
CHECKER = Path("/home/chentianyu/spec-determinism-tool/.venv/bin/specdet")
VERUS = ROOT / "toolchains/verus-x86-linux/verus"
TARGET = "vec/with_capacity.rs::vec::with_capacity::with_capacity"


def run(output, name, arguments, timeout):
    command = [
        "bash", str(ROOT / "scripts/with_baseline.sh"),
        "env", f"TMPDIR={output / 'tmp'}", *map(str, arguments),
    ]
    (output / f"{name}.command.json").write_text(json.dumps(command, indent=2) + "\n")
    started = time.time_ns()
    suffix = "stdout" if name == "scratch-config" else "json"
    with (output / f"{name}.{suffix}").open("w") as stdout, (
        output / f"{name}.stderr"
    ).open("w") as stderr:
        try:
            result = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr, timeout=timeout)
        except subprocess.TimeoutExpired:
            (output / f"{name}.result.json").write_text(json.dumps({
                "returncode": None, "timed_out": True,
                "started_ns": started, "finished_ns": time.time_ns(),
            }, indent=2) + "\n")
            raise
    (output / f"{name}.result.json").write_text(json.dumps({
        "returncode": result.returncode, "timed_out": False,
        "started_ns": started, "finished_ns": time.time_ns(),
    }, indent=2) + "\n")
    if suffix == "json":
        return result.returncode, json.loads((output / f"{name}.json").read_text())
    result.check_returncode()


def main():
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=False)
    run(output, "scratch-config", [
        sys.executable, ROOT / "scripts/borrowed_scratch_config.py", output,
    ], 115)
    config_path = output / "specdet.toml"
    text = config_path.read_text()
    expected = tomllib.loads(text)
    for table, key, value in (
        (expected["build"], "entrypoint", "with_capacity_candidate.rs"),
        (expected["targets"], "include", ["vec/with_capacity.rs"]),
    ):
        original = f"{key} = {json.dumps(table[key])}"
        if text.count(original) != 1:
            raise ValueError(f"Expected one original {key} assignment in scratch config")
        table[key] = value
        text = text.replace(original, f"{key} = {json.dumps(value)}", 1)
    if tomllib.loads(text) != expected:
        raise ValueError("Candidate configuration changed more than entrypoint and target selection")
    config_path.write_text(text)
    default = tomllib.loads((ROOT / "specdet.toml").read_text())
    changes = []
    for keys in (
        ("project", "root"),
        ("adapters", "verus", "executable"),
        ("adapters", "verus", "environment", "TMPDIR"),
        ("artifacts", "output_dir"),
        ("build", "entrypoint"),
        ("targets", "include"),
    ):
        before, after = default, expected
        for key in keys:
            before, after = before[key], after[key]
        changes.append({"setting": ".".join(keys), "before": before, "after": after})
    (output / "config-changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    analysis_code, analysis = run(output, "analyze", [
        CHECKER, "analyze", "--config", config_path,
        "--target", "vec/with_capacity.rs", "--json",
    ], 240)
    replay_code, replay = run(output, "replay", [
        CHECKER, "replay", "--run", analysis["run_dir"], "--reexecute",
        "--verus", VERUS, "--out", output / "replay-runs", "--json",
    ], 240)
    print(f"Native analyze and replay outputs: {output}")
    if analysis_code != 0 or replay_code != 0:
        raise SystemExit(f"Native checker failed: analyze={analysis_code}, replay={replay_code}")
    for phase, data in (("analyze", analysis), ("replay", replay)):
        if [target["qualified_name"] for target in data["targets"]] != [TARGET]:
            raise SystemExit(f"{phase}: expected exactly the with_capacity target")
        if data["counts"] != {"deterministic": 1} or len(data["results"]) != 1:
            raise SystemExit(f"{phase}: with_capacity completeness was not proved")
        result = data["results"][0]
        if result["target"]["qualified_name"] != TARGET or len(result["proofs"]) != 1:
            raise SystemExit(f"{phase}: expected one with_capacity proof")
        proof = result["proofs"][0]
        if proof["status"] != "verified" or proof["verified_goals"] != 1:
            raise SystemExit(f"{phase}: with_capacity has no successful proof obligation")


if __name__ == "__main__":
    main()
