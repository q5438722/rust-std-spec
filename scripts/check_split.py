#!/usr/bin/env python3
"""Check the source-file partition without changing the original collection."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT.parent
TOOLS = ORIGINAL.parent.parent / "toolchains/2026-10-12"


def main():
    pin = json.loads((TOOLS / "manifest.json").read_text())
    verifier = str(Path(pin["verifier"]).resolve())
    env = os.environ.copy()
    env.update({
        "RUSTUP_HOME": "/home/chentianyu/.rustup",
        "RUSTUP_TOOLCHAIN": "1.98.1",
        "VERUS_Z3_PATH": str(Path(pin["z3"]).resolve()),
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    directory = ROOT / "work/validation"
    directory.mkdir(parents=True, exist_ok=True)
    (ROOT / "work/build").mkdir(exist_ok=True)
    report = {"started_at_utc": datetime.now(timezone.utc).isoformat(), "checks": []}

    def run(name, command, goals=None, errors=0, expected_rc=0):
        completed = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
        (directory / f"{name}.stdout").write_text(completed.stdout)
        (directory / f"{name}.stderr").write_text(completed.stderr)
        match = re.search(r"verification results:: (\d+) verified, (\d+) errors?", completed.stdout + completed.stderr)
        good = completed.returncode == expected_rc
        if goals is not None:
            good = good and match is not None and (int(match[1]), int(match[2])) == (goals, errors)
        report["checks"].append({
            "name": name, "command": command, "returncode": completed.returncode,
            "verified_goals": int(match[1]) if match else None,
            "verification_errors": int(match[2]) if match else None,
            "expected_result_met": bool(good),
        })
        report["status"] = "in_progress" if good else "failed"
        (ROOT / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
        print(name + (": OK" if good else ": FAILED"), flush=True)
        if not good:
            print((completed.stdout + completed.stderr)[-12000:])
            raise SystemExit(1)

    run("partition", [sys.executable, "-B", "scripts/split_by_source.py", "--check"])
    formatter = shutil.which("verusfmt")
    if formatter is None:
        raise RuntimeError("verusfmt is required")
    names = ["lib.rs", "slice_shared.rs", "slice_mod.rs", "slice_non_mod.rs", "vec_mod.rs", "vec_non_mod.rs"]
    run("format", [formatter, "--check", "--edition", "2021", *names,
                   "checks/api_clients.rs", "checks/examples.rs", "checks/reject_vacuity.rs"])
    common = ["--crate-type=lib", "--edition=2021", "--triggers-mode", "silent", "--num-threads=1"]
    run("declarations", [verifier, "lib.rs", *common, "--compile", "--out-dir", "work/build"], goals=0)
    run("api_clients", [verifier, "checks/api_clients.rs", *common, "--compile", "--out-dir", "work/build"], goals=98)
    run("examples", [verifier, "checks/examples.rs", *common, "--compile", "--out-dir", "work/build"], goals=10)
    run("reject_vacuity", [verifier, "checks/reject_vacuity.rs", *common, "--multiple-errors", "20"],
        goals=0, errors=10, expected_rc=1)
    original = json.loads((ORIGINAL / "manifest.json").read_text())
    for name, metadata in original["files"].items():
        assert hashlib.sha256((ORIGINAL / name).read_bytes()).hexdigest() == metadata["sha256"], name
    report["status"] = "passed"
    report["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    report["original_collection_unchanged"] = True
    report["output_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in [*names, "api_index.tsv", "source_mapping.json"]
    }
    (ROOT / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "original_collection_unchanged": True}))


if __name__ == "__main__":
    main()
