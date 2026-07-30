#!/usr/bin/env python3
"""Re-run every copied per-API proof independently."""

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


def verify(path: Path, verus: Path, z3: Path, timeout: int) -> dict:
    environment = os.environ.copy()
    environment["VERUS_Z3_PATH"] = str(z3)
    try:
        process = subprocess.run(
            [str(verus), str(path), "--rlimit", "180", "--multiple-errors", "40"],
            cwd=path.parent,
            env=environment,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "id": path.parent.name,
            "returncode": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
        }
    except subprocess.TimeoutExpired as error:
        return {
            "id": path.parent.name,
            "returncode": -1,
            "stdout": error.stdout or "",
            "stderr": (error.stderr or "") + f"\n[timeout after {timeout}s]",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--proved-root",
        type=Path,
        default=SOURCE_VERIFICATION / "proved-apis",
    )
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    verus = WORKSPACE / "verus" / "source" / "target-verus" / "release" / "verus"
    z3 = WORKSPACE / "verus" / "source" / "z3"
    paths = sorted(args.proved_root.glob("*/proof.rs"))
    results = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(verify, path, verus, z3, args.timeout): path
            for path in paths
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"[{len(results)}/{len(paths)}] {result['id']} rc={result['returncode']}",
                flush=True,
            )
    counts = {
        "total": len(results),
        "passed": sum(result["returncode"] == 0 for result in results),
        "failed": sum(result["returncode"] != 0 for result in results),
    }
    (args.proved_root / "verification.json").write_text(
        json.dumps({"counts": counts, "results": results}, indent=2) + "\n"
    )
    print(json.dumps(counts, indent=2))
    return 0 if counts["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
