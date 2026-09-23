#!/usr/bin/env python3
"""Run real specdet controls after deleting each mutable observation constraint."""

import argparse
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
CHECKER = Path("/home/chentianyu/spec-determinism-tool/.venv/bin/specdet")
VERUS = ROOT / "toolchain/verus-x86-linux/verus"
INPUT = Path("proofs/completeness/slice/inputs/from_mut.rs")
CONFIG = Path("proofs/completeness/slice/singletons.toml")
INITIAL = "        state::post::singleton_post(input_initial@, result@.0),\n"
RETURNED = "        result@.1 == caller_final@[0],\n"


def run(command, cwd, directory, phase):
    (directory / f"{phase}-command.txt").write_text(
        f"cd {shlex.quote(str(cwd))} && " + shlex.join(map(str, command)) + "\n"
    )
    with (directory / f"{phase}.stdout").open("x") as stdout, (
        directory / f"{phase}.stderr"
    ).open("x") as stderr:
        result = subprocess.run(command, cwd=cwd, stdout=stdout, stderr=stderr)
    (directory / f"{phase}.exit-code.txt").write_text(f"{result.returncode}\n")
    return result.returncode


def check(output):
    output.mkdir(parents=True, exist_ok=False)
    original = (ROOT / INPUT).read_text()
    assert original.count(INITIAL) == original.count(RETURNED) == 1
    concrete = re.sub(
        r"\bT\b", "bool", original.replace("from_mut_observation<T>(", "from_mut_observation(")
    )
    results = {}
    for name, removed in (
        ("complete-bool", ""),
        ("missing-initial", INITIAL),
        ("missing-return", RETURNED),
    ):
        directory = output / name
        project = directory / "project"
        project.mkdir(parents=True)
        for relative in (
            CONFIG,
            Path("proofs/completeness/slice/from_mut_state.rs"),
            Path("proofs/completeness/slice/inputs/from_ref.rs"),
            Path("specs/slice/raw.rs"),
            Path("specs/slice/raw_post.rs"),
        ):
            destination = project / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)
        text = concrete.replace(removed, "") if removed else concrete
        (project / INPUT).write_text(text)
        compile_code = run(
            [
                VERUS, INPUT, "--crate-type", "lib", "--crate-name", "from_mut_control",
                "--compile", "--no-cheating", "--num-threads", "1",
                "-o", directory / "libfrom_mut_control.rlib",
            ],
            project, directory, "compile",
        )
        assert compile_code == 0, (name, "control does not compile")
        discover_code = run(
            [
                CHECKER, "discover", "--config", CONFIG, "--verus", VERUS,
                "--out", directory / "discovery", "--json",
            ],
            project, directory, "discover",
        )
        assert discover_code == 0, (name, "discovery failed")
        discovered = json.loads((directory / "discover.stdout").read_text())
        targets = [t for t in discovered["targets"] if t["name"] == "from_mut_observation"]
        assert len(targets) == 1 and targets[0]["kind"] == "function", targets
        target = targets[0]
        assert "pub fn from_mut_observation(" in text.splitlines()[target["line"] - 1]
        selector = f'{target["file"]}:{target["name"]}@{target["line"]}'
        code = run(
            [
                CHECKER, "analyze", "--config", CONFIG, "--verus", VERUS,
                "--target", selector, "--out", directory / "runs", "--json",
                "--counterexample-candidates", "64",
            ],
            project, directory, "analyze",
        )
        report = json.loads((directory / "analyze.stdout").read_text())
        assert len(report["results"]) == 1
        result = report["results"][0]
        assert len(result["proofs"]) >= 1, (name, "no generated comparison")
        comparison = result["proofs"][0]["native"]["det_spec"]["equal_fn_def"]
        assert "((r1)@.0 =~= (r2)@.0)" in comparison
        assert "((r1)@.1 == (r2)@.1)" in comparison
        witness = result["counterexample"]
        results[name] = {
            "exit_code": code,
            "verdict": result["verdict"],
            "baseline": result["baseline"]["status"],
            "proofs": [
                {"status": p["status"], "verified_goals": p["verified_goals"]}
                for p in result["proofs"]
            ],
            "diagnostics": [d["code"] for d in result["diagnostics"]],
            "run_dir": report["run_dir"],
            "counterexample": witness,
        }
        print(name + ": " + json.dumps(results[name]), flush=True)
    (output / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    check_results(results)


def check_results(results):
    assert results["complete-bool"]["exit_code"] == 0
    assert results["complete-bool"]["verdict"] == "deterministic"
    assert results["complete-bool"]["baseline"] == "unsat"
    assert results["complete-bool"]["proofs"] == [{"status": "verified", "verified_goals": 1}]
    for name in ("missing-initial", "missing-return"):
        assert results[name]["verdict"] == "nondeterministic", (name, results[name])
        witness = results[name]["counterexample"]
        assert witness["status"] == "verified" and witness["verified_goals"] == 1
        replay = json.loads(Path(witness["artifact"]).read_text())["payload"]
        assert replay["status"] == "verified" and replay["verifier"]["returncode"] == 0
        assert replay["verified_goals"] == 1
        assert replay["problem_id"] == witness["problem_id"]
        assert replay["bindings"] == witness["bindings"]
        bindings = witness["bindings"]
        initial = bindings["input_initial"]["value"]
        caller = bindings["caller_final"]["value"]["items"]
        left = bindings["r1"]["value"]["items"]
        right = bindings["r2"]["value"]["items"]
        assert len(caller) == 1
        if name == "missing-initial":
            assert left[1] == right[1] == caller[0]
            assert len(left[0]["items"]) == len(right[0]["items"]) == 1
            assert left[0]["items"] != right[0]["items"]
        else:
            assert left[0]["items"] == right[0]["items"] == [initial]
            assert left[1] != right[1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output-root", type=Path)
    mode.add_argument("--check-existing", type=Path)
    args = parser.parse_args()
    if args.check_existing is not None:
        check_results(json.loads((args.check_existing / "results.json").read_text()))
        print("Both omitted constraints have a verified constructive counterexample.")
    else:
        check(args.output_root.resolve())
