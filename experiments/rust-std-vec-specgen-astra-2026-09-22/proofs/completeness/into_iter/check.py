import copy
import json
from pathlib import Path
import re
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
from scripts.borrowed_scratch_config import write_config
from test_with_capacity_isolation import run

SPECDET = "/home/chentianyu/spec-determinism-tool/.venv/bin/specdet"


def main():
    output = Path(sys.argv[1]).resolve()
    config = write_config(output)
    original = tomllib.loads(config.read_text())
    text = re.sub(
        r'^root = .+$',
        'root = ' + json.dumps(str(ROOT / "proofs/correctness/into_iter/isolated")),
        config.read_text(), count=1, flags=re.MULTILINE,
    )
    text = re.sub(
        r'^include = .+$', 'include = ["consumers.rs"]',
        text, count=1, flags=re.MULTILINE,
    )
    expected = copy.deepcopy(original)
    expected["project"]["root"] = str(ROOT / "proofs/correctness/into_iter/isolated")
    expected["targets"]["include"] = ["consumers.rs"]
    current = tomllib.loads(text)
    if current != expected:
        raise AssertionError("isolated input configuration differs beyond root and target selection")
    config.write_text(text)
    (output / "isolated-config-changes.json").write_text(json.dumps([
        {"setting": "project.root", "before": original["project"]["root"],
         "after": current["project"]["root"]},
        {"setting": "targets.include", "before": original["targets"]["include"],
         "after": current["targets"]["include"]},
    ], indent=2) + "\n")
    analyze_process = run(
        output, "analyze", [SPECDET, "analyze", "--config", str(config), "--json"],
        timeout=360,
    )
    analyze = json.loads((output / "analyze.stdout").read_text())
    (output / "analyze.json").write_text(json.dumps(analyze, indent=2) + "\n")
    replay_process = run(output, "replay", [
        SPECDET, "replay", "--run", analyze["run_dir"], "--reexecute",
        "--config", str(config),
        "--verus", str(ROOT / "toolchains/verus-x86-linux/verus"),
        "--out", str(output / "replay-runs"), "--json",
    ], timeout=360)
    replay = json.loads((output / "replay.stdout").read_text())
    (output / "replay.json").write_text(json.dumps(replay, indent=2) + "\n")
    passed = True
    targets = {
        f"consumers.rs::consumers::<IntoIter<T, A> as core::iter::Iterator>::{name}"
        for name in ("count", "last")
    }
    for name, process, summary in (
        ("analyze", analyze_process, analyze), ("replay", replay_process, replay),
    ):
        print(f"{name}: exit={process.returncode}, status={summary.get('status')}, "
              f"counts={summary.get('counts')}", flush=True)
        results = summary.get("results", [])
        actual = {result["target"]["qualified_name"] for result in results}
        print(f"{name}: targets={sorted(actual)}", flush=True)
        ok = (
            process.returncode == 0
            and summary.get("status") == "completed"
            and summary.get("exit_code") == 0
            and summary.get("diagnostics") == []
            and summary.get("discovery_coverage") == "source-visible"
            and actual == targets
            and {target["qualified_name"] for target in summary["targets"]} == targets
            and summary.get("counts") == {"deterministic": 2}
            and all(
                result.get("status") == "completed"
                and result.get("verdict") == "deterministic"
                and any(
                    proof.get("status") == "verified" and proof.get("verified_goals", 0) > 0
                    for proof in result.get("proofs", [])
                )
                for result in results
            )
        )
        passed = passed and ok
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
