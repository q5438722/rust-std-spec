"""Compile the current source entry or aggregate into a new output directory."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[4]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--entry", choices=("source", "aggregate"), default="source")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "tmp").mkdir()
    (output / "logs").mkdir()
    entry = ROOT / (
        "proofs/correctness/vec/index.rs" if args.entry == "source" else "specs/lib.rs"
    )
    crate = "vec_index_source" if args.entry == "source" else "vec_specs"
    library = output / f"lib{crate}.rlib"
    shutil.copyfile(ROOT / "specs/vec/index.rs", output / "candidate.rs")
    shutil.copyfile(entry, output / "entry.rs")
    command = [
        "bash", str(ROOT / "scripts/with_baseline.sh"),
        "env", f"TMPDIR={output / 'tmp'}",
        str(ROOT / "toolchains/verus-x86-linux/verus"), str(entry),
        "--edition=2021", "--crate-type=lib", "--crate-name", crate,
        "--compile", "--num-threads=1", "--trace", "--log-all",
        "--log-dir", str(output / "logs"), "-o", str(library),
    ]
    (output / "build.command.json").write_text(json.dumps(command, indent=2) + "\n")
    started = time.time_ns()
    try:
        result = subprocess.run(
            command, cwd=ROOT, text=True, capture_output=True, timeout=115
        )
    except subprocess.TimeoutExpired as error:
        for name, value in (("stdout", error.stdout), ("stderr", error.stderr)):
            if isinstance(value, bytes):
                value = value.decode(errors="replace")
            (output / f"build.{name}").write_text(value or "")
        (output / "build.result.json").write_text(json.dumps({
            "returncode": None, "timed_out": True,
            "started_ns": started, "finished_ns": time.time_ns(),
        }, indent=2) + "\n")
        raise
    finished = time.time_ns()
    (output / "build.stdout").write_text(result.stdout)
    (output / "build.stderr").write_text(result.stderr)
    (output / "build.result.json").write_text(json.dumps({
        "returncode": result.returncode, "timed_out": False,
        "started_ns": started, "finished_ns": finished,
    }, indent=2) + "\n")
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    result.check_returncode()
    expected = 1 if args.entry == "source" else 4
    assert f"verification results:: {expected} verified, 0 errors" in result.stdout
    assert started <= library.stat().st_mtime_ns <= finished
    print(f"Fresh library: {library}")


if __name__ == "__main__":
    main()
