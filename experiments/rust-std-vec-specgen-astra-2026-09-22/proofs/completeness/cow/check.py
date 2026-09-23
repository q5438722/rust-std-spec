"""Run the real Cow analysis and a fresh native replay using a scratch config."""

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SPECDET = "/home/chentianyu/spec-determinism-tool/.venv/bin/specdet"


def run(directory, name, arguments):
    command = [
        "bash", str(ROOT / "scripts/with_baseline.sh"),
        "env", f"TMPDIR={directory / 'tmp'}", SPECDET, *map(str, arguments),
    ]
    with (directory / f"{name}.command.json").open("x") as stream:
        json.dump(command, stream, indent=2)
        stream.write("\n")
    with (directory / f"{name}.json").open("x") as stdout, (
        directory / f"{name}.stderr"
    ).open("x") as stderr:
        result = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr)
    (directory / f"{name}.exit-code").write_text(f"{result.returncode}\n")
    data = json.loads((directory / f"{name}.json").read_text())
    print(f"{name}: exit {result.returncode}; {data.get('counts', {})}", flush=True)
    for target in data["results"]:
        print(target["target"]["qualified_name"], target["verdict"],
              [diagnostic["code"] for diagnostic in target["diagnostics"]], flush=True)
    if result.returncode not in (0, 2):
        raise RuntimeError(f"{name} failed: see {directory / (name + '.stderr')}")
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    directory = args.directory.resolve()
    config = directory / "specdet.toml"
    if not config.is_file():
        raise FileNotFoundError(f"Create a transparent private-output configuration first: {config}")
    analysis = run(directory, "analyze", [
        "analyze", "--config", config, "--target", "cow/conversions.rs", "--json",
    ])
    replay = run(directory, "replay", [
        "replay", "--run", analysis["run_dir"], "--reexecute",
        "--verus", ROOT / "toolchains/verus-x86-linux/verus",
        "--out", directory / "replay-runs", "--json",
    ])
    if analysis["run_dir"] == replay["run_dir"]:
        raise AssertionError("Replay must execute in a new native run directory")
    initial_targets = {result["target"]["qualified_name"] for result in analysis["results"]}
    replay_targets = {result["target"]["qualified_name"] for result in replay["results"]}
    if len(initial_targets) != 4 or initial_targets != replay_targets:
        raise AssertionError("Analysis and replay must select the same four Cow declarations")
    if any(result["verdict"] != "deterministic" for data in (analysis, replay)
           for result in data["results"]):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
