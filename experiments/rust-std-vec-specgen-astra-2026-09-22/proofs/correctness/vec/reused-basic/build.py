import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[4]
VERUS = ROOT / "toolchains/verus-x86-linux/verus"
APIS = ("default", "is_empty", "deref")


def main():
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "build").mkdir()
    (output / "tmp").mkdir()
    source = ROOT / "specs/vec/reused_basic.rs"
    shutil.copyfile(source, output / "reused_basic.source.rs")
    entries = [(name, ROOT / f"proofs/correctness/vec/{name}.rs") for name in APIS]
    entries.append(("aggregate", ROOT / "specs/lib.rs"))
    for name, entry in entries:
        shutil.copyfile(entry, output / f"{name}.source.rs")
        crate = "vec_specs" if name == "aggregate" else f"reused_{name}"
        command = [
            "bash", str(ROOT / "scripts/with_baseline.sh"),
            "env", f"TMPDIR={output / 'tmp'}", str(VERUS), str(entry),
            "--edition=2021", "--crate-type=lib", "--crate-name", crate,
            "--compile", "--num-threads=1", "--trace", "--log-all",
            "--log-dir", str(output / name),
            "-o", str(output / "build" / f"lib{crate}.rlib"),
        ]
        if name in APIS:
            command += ["--verify-only-module", "reused_basic", "--verify-function", name]
        (output / f"{name}.command.json").write_text(json.dumps(command, indent=2) + "\n")
        started = time.time_ns()
        with (output / f"{name}.stdout").open("w") as stdout, (
            output / f"{name}.stderr"
        ).open("w") as stderr:
            try:
                result = subprocess.run(
                    command, cwd=ROOT, stdout=stdout, stderr=stderr, timeout=115,
                )
            except subprocess.TimeoutExpired:
                (output / f"{name}.result.json").write_text(json.dumps({
                    "returncode": None, "timed_out": True, "started_ns": started,
                    "finished_ns": time.time_ns(),
                }, indent=2) + "\n")
                raise
        (output / f"{name}.result.json").write_text(json.dumps({
            "returncode": result.returncode, "timed_out": False,
            "started_ns": started, "finished_ns": time.time_ns(),
        }, indent=2) + "\n")
        result.check_returncode()
        text = (output / f"{name}.stdout").read_text()
        expected = 3 if name == "aggregate" else 1
        if f"verification results:: {expected} verified, 0 errors" not in text:
            raise AssertionError(f"{name}: expected {expected} nonzero source obligations\n{text}")
        print(f"{name}: {expected} verified; compiled {crate}", flush=True)


if __name__ == "__main__":
    main()
