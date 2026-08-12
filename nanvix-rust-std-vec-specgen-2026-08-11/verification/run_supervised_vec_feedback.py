#!/usr/bin/env python3
"""Supervised wrapper for the alloc::vec feedback determinism refresh."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import selectors
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json_atomic(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    tmp.replace(path)


def append_event(run_dir: Path, event: dict[str, object]) -> None:
    event = {"timestamp": now(), **event}
    path = run_dir / "progress.jsonl"
    with path.open("a") as stream:
        stream.write(json.dumps(event, sort_keys=True) + "\n")
        stream.flush()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--rlimit", type=float, default=60)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir
    run_dir.mkdir(parents=True, exist_ok=True)
    stop_path = run_dir / "STOP"
    command = [
        sys.executable,
        "verification/run_vec_assume_spec_feedback_determinism.py",
        "--run-id",
        args.run_id,
        "--timeout",
        str(args.timeout),
        "--rlimit",
        str(args.rlimit),
    ]
    manifest = {
        "schema_version": 1,
        "objective": "Run feedback-pipeline determinism for the 24 executable alloc::vec generated contracts.",
        "command": command,
        "cwd": str(ROOT),
        "run_id": args.run_id,
        "expected_targets": 24,
        "evidence_manifest": "verification/evidence/vec_feedback_determinism/latest_manifest.json",
    }
    write_json_atomic(run_dir / "manifest.json", manifest)
    status = {
        "state": "running",
        "started_at": now(),
        "current_item": "",
        "targets_done": 0,
        "expected_targets": 24,
        "return_code": None,
    }
    write_json_atomic(run_dir / "status.json", status)
    append_event(run_dir, {"event": "run_started", "run_id": args.run_id})

    stdout_log = (run_dir / "stdout.log").open("w")
    stderr_log = (run_dir / "stderr.log").open("w")
    selector = selectors.DefaultSelector()
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
    )
    assert process.stdout is not None
    assert process.stderr is not None
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    last_status = time.monotonic()
    try:
        while selector.get_map():
            if stop_path.exists() and process.poll() is None:
                append_event(run_dir, {"event": "stop_requested"})
                process.terminate()
            for key, _ in selector.select(timeout=0.5):
                line = key.fileobj.readline()
                if line == "":
                    selector.unregister(key.fileobj)
                    continue
                if key.data == "stdout":
                    stdout_log.write(line)
                    stdout_log.flush()
                    if ": status=" in line and " dir=" in line:
                        target = line.split(": status=", 1)[0]
                        status["current_item"] = target
                        status["targets_done"] = int(status["targets_done"]) + 1
                        append_event(
                            run_dir,
                            {"event": "trial_done", "target": target, "line": line.strip()},
                        )
                        write_json_atomic(run_dir / "status.json", status)
                else:
                    stderr_log.write(line)
                    stderr_log.flush()
            if time.monotonic() - last_status > 30:
                status["heartbeat_at"] = now()
                write_json_atomic(run_dir / "status.json", status)
                append_event(run_dir, {"event": "heartbeat", "targets_done": status["targets_done"]})
                last_status = time.monotonic()
        return_code = process.wait()
    finally:
        stdout_log.close()
        stderr_log.close()

    status["return_code"] = return_code
    status["finished_at"] = now()
    status["state"] = "done" if return_code == 0 else "failed"
    write_json_atomic(run_dir / "status.json", status)
    append_event(
        run_dir,
        {
            "event": "run_completed" if return_code == 0 else "run_failed",
            "return_code": return_code,
            "targets_done": status["targets_done"],
        },
    )
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
