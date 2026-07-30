#!/usr/bin/env python3
"""Verify all organized proof and external-body files."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
SOURCE_VERIFICATION = HERE.parent
WORKSPACE = SOURCE_VERIFICATION.parent
DEFAULT_SUITE = SOURCE_VERIFICATION / "organized-suite"


def run(path: Path, kind: str, verus: Path, z3: Path, timeout: int) -> dict:
    environment = os.environ.copy()
    environment["VERUS_Z3_PATH"] = str(z3)
    try:
        process = subprocess.run(
            [str(verus), str(path), "--rlimit", "240", "--multiple-errors", "60"],
            cwd=path.parent,
            env=environment,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "path": str(path),
            "kind": kind,
            "returncode": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
        }
    except subprocess.TimeoutExpired as error:
        return {
            "path": str(path),
            "kind": kind,
            "returncode": -1,
            "stdout": error.stdout or "",
            "stderr": (error.stderr or "") + f"\n[timeout after {timeout}s]",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--jobs", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--only", choices=["proved", "external_body"])
    args = parser.parse_args()

    manifest = json.loads((args.suite / "manifest.json").read_text())
    files = []
    for group in manifest["groups"]:
        if args.only in {None, "proved"}:
            files.extend(
                (args.suite / item["path"], "proved")
                for item in group["proved"]
            )
        if args.only in {None, "external_body"}:
            files.extend(
                (args.suite / item["path"], "external_body")
                for item in group["external_body"]
            )
    verus = WORKSPACE / "verus" / "source" / "target-verus" / "release" / "verus"
    z3 = WORKSPACE / "verus" / "source" / "z3"
    results = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(run, path, kind, verus, z3, args.timeout): (path, kind)
            for path, kind in files
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"[{len(results)}/{len(files)}] {result['kind']} "
                f"{Path(result['path']).parent.name} rc={result['returncode']}",
                flush=True,
            )
    counts = {
        "total": len(results),
        "passed": sum(item["returncode"] == 0 for item in results),
        "failed": sum(item["returncode"] != 0 for item in results),
        "proved_passed": sum(
            item["kind"] == "proved" and item["returncode"] == 0
            for item in results
        ),
        "external_body_passed": sum(
            item["kind"] == "external_body" and item["returncode"] == 0
            for item in results
        ),
    }
    (args.suite / "verification.json").write_text(
        json.dumps({"counts": counts, "results": results}, indent=2) + "\n"
    )
    print(json.dumps(counts, indent=2))
    return 0 if counts["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
