"""Analyze only the two owned conversions and reexecute their native checks."""

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
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
    if result.returncode not in (0, 2):
        raise RuntimeError(f"{name} failed: see {directory / (name + '.stderr')}")
    data = json.loads((directory / f"{name}.json").read_text())
    print(f"{name}: exit {result.returncode}; {data['counts']}", flush=True)
    for target in data["results"]:
        print(target["target"]["qualified_name"], target["verdict"],
              [diagnostic["code"] for diagnostic in target["diagnostics"]], flush=True)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory.resolve()
    config = directory / "specdet.toml"
    if not config.is_file():
        raise FileNotFoundError(f"Create a private-output configuration first: {config}")
    analysis = run(directory, "analyze", [
        "analyze", "--config", config, "--target", "vec/owned_conversions.rs", "--json",
    ])
    replay = run(directory, "replay", [
        "replay", "--run", analysis["run_dir"], "--reexecute",
        "--verus", ROOT / "toolchains/verus-x86-linux/verus",
        "--out", directory / "replay-runs", "--json",
    ])
    if analysis["run_dir"] == replay["run_dir"]:
        raise AssertionError("Replay must reexecute in a different native run directory")
    targets = {
        "vec/owned_conversions.rs::vec::owned_conversions::array::<Vec<T> as From<[T; N]>>::from",
        "vec/owned_conversions.rs::vec::owned_conversions::<Vec<T, A> as From<Box<[T], A>>>::from",
    }
    for data in (analysis, replay):
        actual = {result["target"]["qualified_name"] for result in data["results"]}
        if actual != targets or len(data["results"]) != 2:
            raise AssertionError(f"Only the two owned bindings may be selected: {actual}")
    if any(result["verdict"] != "deterministic" for data in (analysis, replay)
           for result in data["results"]):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
