import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[4]
VERUS = ROOT / "toolchains/verus-x86-linux/verus"


def main():
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "build").mkdir()
    (output / "tmp").mkdir()
    shutil.copytree(ROOT / "specs", output / "sources")
    entries = (
        ("source", ROOT / "proofs/correctness/vec/with_capacity.rs",
         "source_with_capacity", "with_capacity_source"),
        ("candidate", ROOT / "specs/with_capacity_candidate.rs",
         "with_capacity_candidate", "vec::with_capacity"),
    )
    failures = []
    for name, entry, crate, module in entries:
        shutil.copyfile(entry, output / f"{name}.source.rs")
        command = [
            "bash", str(ROOT / "scripts/with_baseline.sh"),
            "env", f"TMPDIR={output / 'tmp'}", str(VERUS), str(entry),
            "--edition=2021", "--crate-type=lib", "--crate-name", crate,
            "--compile", "--num-threads=1", "--trace", "--log-all",
            "--log-dir", str(output / name),
            "-o", str(output / "build" / f"lib{crate}.rlib"),
            "--verify-only-module", module, "--verify-function", "with_capacity",
        ]
        (output / f"{name}.command.json").write_text(json.dumps(command, indent=2) + "\n")
        started = time.time_ns()
        with (output / f"{name}.stdout").open("w") as stdout, (
            output / f"{name}.stderr"
        ).open("w") as stderr:
            try:
                result = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr, timeout=115)
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
        text = (output / f"{name}.stdout").read_text()
        if result.returncode != 0 or "verification results:: 1 verified, 0 errors" not in text:
            failures.append(name)
            print(f"{name}: source verification/build failed; see {output / name}", flush=True)
        else:
            print(f"{name}: 1 verified; compiled {crate}", flush=True)
    if failures:
        raise SystemExit(f"Source verification/build failed: {', '.join(failures)}")


if __name__ == "__main__":
    main()
