#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import time
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_DIR = Path(__file__).resolve().parent
STOP_PATH = RUN_DIR / "STOP"
PYTHON = "/home/chentianyu/miniconda3/bin/python3"
COMMANDS = [
    (
        "01_compileall",
        [PYTHON, "-m", "compileall", "-f", "-q", "tools", "tests"],
    ),
    (
        "02_focused_tests",
        [
            PYTHON,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_operational_v2_certification.py",
            "-v",
        ],
    ),
    (
        "03_complete_tests",
        [PYTHON, "-m", "unittest", "discover", "-s", "tests", "-v"],
    ),
    (
        "04_closure",
        [PYTHON, "tools/run_operational_v2_certification_closure.py"],
    ),
    (
        "05_task_native_acceptance",
        [PYTHON, "tools/run_acceptance.py"],
    ),
]
RECOVERY_COMMANDS = [
    (
        "01_target_079_operational_v1",
        [PYTHON, "tools/run_target_079_operational_v1.py"],
        600,
    ),
    (
        "02_local_validator",
        [PYTHON, "tools/validate_authority_design.py"],
        110,
    ),
    (
        "03_final_reconciliation",
        [PYTHON, "tools/run_final_reconciliation.py"],
        110,
    ),
    (
        "04_operational_v2_reconciliation",
        [PYTHON, "tools/run_operational_v2_reconciliation.py"],
        110,
    ),
    (
        "05_operational_v2_certification_closure",
        [PYTHON, "tools/run_operational_v2_certification_closure.py"],
        110,
    ),
]


def _timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: Any) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def _append_progress(event: str, **details: Any) -> None:
    record = {"event": event, "timestamp": _timestamp(), **details}
    with (RUN_DIR / "progress.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def _write_status(state: str, **details: Any) -> None:
    _write_json(
        RUN_DIR / "status.json",
        {"state": state, "updated_at": _timestamp(), **details},
    )


def _display_command(arguments: list[str]) -> str:
    return f"PYTHONDONTWRITEBYTECODE=1 {shlex.join(arguments)}"


def _protected_map(groups: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    protected: dict[str, Any] = {}
    for records in groups.values():
        for record in records:
            protected[record["path"]] = {
                "bytes": record["bytes"],
                "sha256": record["sha256"],
            }
    return protected


def _stop_process(process: subprocess.Popen[bytes]) -> None:
    os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()


def _run_command(
    index: int, name: str, arguments: list[str]
) -> dict[str, Any]:
    command_dir = RUN_DIR / name
    command_dir.mkdir()
    display = _display_command(arguments)
    (command_dir / "command.txt").write_text(display + "\n")
    _append_progress(
        "command_started",
        command_index=index,
        command_name=name,
        command=display,
    )
    _write_status(
        "running",
        command_index=index,
        command_name=name,
        completed_commands=index - 1,
        total_commands=len(COMMANDS),
    )
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.monotonic()
    with (
        (command_dir / "stdout.txt").open("wb") as stdout,
        (command_dir / "stderr.txt").open("wb") as stderr,
    ):
        process = subprocess.Popen(
            arguments,
            cwd=ROOT,
            env=environment,
            stdout=stdout,
            stderr=stderr,
            start_new_session=True,
        )
        while process.poll() is None:
            if STOP_PATH.exists():
                _stop_process(process)
                raise InterruptedError(
                    f"STOP requested while running {name}"
                )
            time.sleep(1)
    elapsed = time.monotonic() - started
    status = process.returncode
    (command_dir / "status.txt").write_text(f"{status}\n")
    (command_dir / "elapsed_seconds.txt").write_text(f"{elapsed:.6f}\n")
    test_count = None
    if name in {"02_focused_tests", "03_complete_tests"}:
        stderr_text = (command_dir / "stderr.txt").read_text(
            encoding="utf-8", errors="replace"
        )
        match = re.search(r"^Ran ([0-9]+) tests? in ", stderr_text, re.MULTILINE)
        if match is not None:
            test_count = int(match.group(1))
    result = {
        "elapsed_seconds": elapsed,
        "name": name,
        "status": status,
        "test_count": test_count,
    }
    _append_progress("command_completed", **result)
    return result


def _manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "task_id": "operational-v2-certification-summary-r3",
        "objective": (
            "Replay the five-command operational-v2 certification validation "
            "chain after enforcing one unambiguous count-bearing review summary."
        ),
        "cwd": str(ROOT),
        "commands": [
            {"name": name, "command": _display_command(arguments)}
            for name, arguments in COMMANDS
        ],
        "expected": {
            "focused_test_count": 17,
            "complete_test_count": 571,
            "acceptance_commands": 49,
            "protected_file_count": 707,
        },
    }


def _completed_results() -> list[dict[str, Any]]:
    completed: dict[str, list[dict[str, Any]]] = {}
    with (RUN_DIR / "progress.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            if record.get("event") == "command_completed":
                completed.setdefault(record["name"], []).append(
                    {
                        "elapsed_seconds": record["elapsed_seconds"],
                        "name": record["name"],
                        "status": record["status"],
                        "test_count": record["test_count"],
                    }
                )

    results = []
    for name, _arguments in COMMANDS[:4]:
        matches = completed.get(name, [])
        if len(matches) != 1:
            raise RuntimeError(
                f"resume requires exactly one completed result for {name}"
            )
        result = matches[0]
        command_status = int(
            (RUN_DIR / name / "status.txt").read_text().strip()
        )
        if result["status"] != 0 or command_status != 0:
            raise RuntimeError(f"resume requires a successful {name}")
        results.append(result)

    if results[1]["test_count"] != 17:
        raise RuntimeError("resume requires 17 focused tests")
    if results[2]["test_count"] != 571:
        raise RuntimeError("resume requires 571 complete tests")

    expected_closure = [
        "operational_v2_certification_closure=PASS",
        "independent_review=ACCEPT",
        "review_status=accepted",
        "rows=62",
        "exact=50/12/0",
        "full=43/19/0",
        "stage_transition=disabled",
    ]
    closure_output = (
        RUN_DIR / "04_closure" / "stdout.txt"
    ).read_text().splitlines()
    if closure_output != expected_closure:
        raise RuntimeError("resume requires the accepted closure output")
    return results


def _acceptance_markers() -> tuple[str | None, int | None]:
    stdout_path = RUN_DIR / "05_task_native_acceptance" / "stdout.txt"
    if not stdout_path.is_file():
        return None, None
    stdout = stdout_path.read_text(encoding="utf-8", errors="replace")
    acceptance_matches = re.findall(
        r"^acceptance=([A-Z]+)$", stdout, flags=re.MULTILINE
    )
    command_matches = re.findall(
        r"^commands=([0-9]+)$", stdout, flags=re.MULTILINE
    )
    acceptance = (
        acceptance_matches[0] if len(acceptance_matches) == 1 else None
    )
    command_count = (
        int(command_matches[0]) if len(command_matches) == 1 else None
    )
    return acceptance, command_count


def _finalize(
    results: list[dict[str, Any]], protected_before: dict[str, Any]
) -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    import operational_v2_certification as certification

    protected_after = _protected_map(
        certification.build_certified_projection()["protected_inputs"]["groups"]
    )
    protected_missing = sorted(protected_before.keys() - protected_after.keys())
    protected_extra = sorted(protected_after.keys() - protected_before.keys())
    protected_changed = sorted(
        path
        for path in protected_before.keys() & protected_after.keys()
        if protected_before[path] != protected_after[path]
    )
    acceptance, acceptance_commands = _acceptance_markers()
    passed = (
        len(results) == len(COMMANDS)
        and all(result["status"] == 0 for result in results)
        and results[1]["test_count"] == 17
        and results[2]["test_count"] == 571
        and acceptance == "PASS"
        and acceptance_commands == 49
        and len(protected_before) == 707
        and not protected_missing
        and not protected_extra
        and not protected_changed
    )
    summary = {
        "acceptance": acceptance,
        "acceptance_commands": acceptance_commands,
        "commands": results,
        "protected_changed": protected_changed,
        "protected_extra": protected_extra,
        "protected_file_count": len(protected_before),
        "protected_missing": protected_missing,
        "status": "PASS" if passed else "FAIL",
    }
    _write_json(RUN_DIR / "summary.json", summary)
    if not passed:
        _append_progress("run_failed", summary=summary)
        _write_status(
            "failed",
            completed_commands=len(results),
            total_commands=len(COMMANDS),
            summary=summary,
        )
        return 1
    _append_progress("run_completed", summary=summary)
    _write_status(
        "completed",
        completed_commands=len(results),
        total_commands=len(COMMANDS),
        summary=summary,
    )
    return 0


def _protected_snapshot() -> dict[str, Any]:
    sys.path.insert(0, str(ROOT / "tools"))
    import operational_v2_certification as certification

    return _protected_map(
        copy.deepcopy(
            certification.build_certified_projection()[
                "protected_inputs"
            ]["groups"]
        )
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _protected_baseline() -> dict[str, Any]:
    projection_path = (
        ROOT
        / "evidence/final_campaign/operational_v2/certified"
        / "certified_projection.json"
    )
    manifest_path = projection_path.with_name("certification_manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = manifest["artifacts"]["certified_projection_json"]
    if (
        expected["path"]
        != "evidence/final_campaign/operational_v2/certified/"
        "certified_projection.json"
        or projection_path.stat().st_size != expected["bytes"]
        or _sha256(projection_path) != expected["sha256"]
    ):
        raise RuntimeError(
            "certified protected-input baseline identity has drifted"
        )
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    protected = _protected_map(projection["protected_inputs"]["groups"])
    if len(protected) != 707:
        raise RuntimeError(
            "certified protected-input baseline must contain 707 files"
        )
    return protected


def _protected_drift(
    baseline: dict[str, Any]
) -> tuple[list[str], list[str]]:
    missing = []
    changed = []
    for relative, expected in baseline.items():
        path = ROOT / relative
        if not path.is_file():
            missing.append(relative)
        elif (
            path.stat().st_size != expected["bytes"]
            or _sha256(path) != expected["sha256"]
        ):
            changed.append(relative)
    return sorted(missing), sorted(changed)


def _run_recovery_command(
    index: int, name: str, arguments: list[str], timeout: int
) -> None:
    recovery_root = RUN_DIR / "command_05_recovery"
    recovery_root.mkdir(exist_ok=True)
    command_dir = recovery_root / name
    command_dir.mkdir()
    display = _display_command(arguments)
    (command_dir / "command.txt").write_text(display + "\n")
    _append_progress(
        "recovery_command_started",
        recovery_command_index=index,
        recovery_command_name=name,
        command=display,
    )
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.monotonic()
    timed_out = False
    with (
        (command_dir / "stdout.txt").open("wb") as stdout,
        (command_dir / "stderr.txt").open("wb") as stderr,
    ):
        process = subprocess.Popen(
            arguments,
            cwd=ROOT,
            env=environment,
            stdout=stdout,
            stderr=stderr,
            start_new_session=True,
        )
        while process.poll() is None:
            if time.monotonic() - started >= timeout:
                _stop_process(process)
                timed_out = True
                break
            time.sleep(1)
    elapsed = time.monotonic() - started
    status = 124 if timed_out else process.returncode
    (command_dir / "status.txt").write_text(f"{status}\n")
    (command_dir / "elapsed_seconds.txt").write_text(f"{elapsed:.6f}\n")
    _append_progress(
        "recovery_command_completed",
        elapsed_seconds=elapsed,
        name=name,
        status=status,
    )
    if status != 0:
        raise RuntimeError(
            f"command-five recovery failed in {name} with status {status}"
        )


def main() -> int:
    manifest = _manifest()
    _write_json(RUN_DIR / "manifest.json", manifest)
    _append_progress("run_started", task_id=manifest["task_id"])
    _write_status(
        "running",
        command_index=0,
        completed_commands=0,
        total_commands=len(COMMANDS),
    )

    protected_before = _protected_snapshot()
    results = []
    for index, (name, arguments) in enumerate(COMMANDS, start=1):
        if STOP_PATH.exists():
            raise InterruptedError(f"STOP requested before running {name}")
        result = _run_command(index, name, arguments)
        results.append(result)
        if result["status"] != 0:
            break
    return _finalize(results, protected_before)


def resume_command_5() -> int:
    manifest = _manifest()
    if json.loads((RUN_DIR / "manifest.json").read_text()) != manifest:
        raise RuntimeError("resume manifest does not match this validation chain")
    status = json.loads((RUN_DIR / "status.json").read_text())
    if (
        status.get("state") != "cancelled"
        or status.get("reason")
        != "STOP requested while running 05_task_native_acceptance"
    ):
        raise RuntimeError("resume requires the command-five cancellation state")

    results = _completed_results()
    protected_before = _protected_snapshot()
    if len(protected_before) != 707:
        raise RuntimeError("resume requires exactly 707 protected files")

    cancelled_dir = RUN_DIR / "05_task_native_acceptance_cancelled"
    command_dir = RUN_DIR / "05_task_native_acceptance"
    if cancelled_dir.exists():
        raise RuntimeError("cancelled command-five archive already exists")
    os.replace(command_dir, cancelled_dir)
    STOP_PATH.unlink()
    _append_progress(
        "run_resumed",
        command_index=5,
        command_name="05_task_native_acceptance",
        completed_commands=4,
    )
    name, arguments = COMMANDS[4]
    results.append(_run_command(5, name, arguments))
    return _finalize(results, protected_before)


def recover_and_resume_command_5() -> int:
    manifest = _manifest()
    if json.loads((RUN_DIR / "manifest.json").read_text()) != manifest:
        raise RuntimeError("resume manifest does not match this validation chain")
    status = json.loads((RUN_DIR / "status.json").read_text())
    expected_error = (
        "OperationalV2CertificationError('accepted operational-v2 "
        "crosswalk_json: missing file "
        "crosswalk/conditional_obligation_crosswalk_operational_v2.json')"
    )
    if status.get("state") != "failed" or status.get("error") != expected_error:
        raise RuntimeError(
            "recovery requires the observed missing-crosswalk precondition "
            "failure"
        )

    results = _completed_results()
    protected_before = _protected_baseline()
    missing_before, changed_before = _protected_drift(protected_before)
    if not missing_before or changed_before:
        raise RuntimeError(
            "recovery requires missing but no byte-changed protected files"
        )

    stop_archive = RUN_DIR / "STOP.cancelled"
    if stop_archive.exists() or not STOP_PATH.is_file():
        raise RuntimeError("recovery requires the consumed STOP marker")
    os.replace(STOP_PATH, stop_archive)
    _append_progress(
        "command_05_recovery_started",
        missing_protected_files=len(missing_before),
        changed_protected_files=len(changed_before),
    )
    _write_status(
        "recovering",
        command_index=5,
        command_name="05_task_native_acceptance",
        completed_commands=4,
        missing_protected_files=len(missing_before),
        total_commands=len(COMMANDS),
    )
    for index, (name, arguments, timeout) in enumerate(
        RECOVERY_COMMANDS, start=1
    ):
        _run_recovery_command(index, name, arguments, timeout)

    restored = _protected_snapshot()
    if restored != protected_before:
        missing_after, changed_after = _protected_drift(protected_before)
        raise RuntimeError(
            "command-five recovery did not restore the certified protected "
            f"baseline: missing={len(missing_after)} "
            f"changed={len(changed_after)}"
        )
    _append_progress(
        "command_05_recovery_completed",
        protected_file_count=len(restored),
        protected_missing=[],
        protected_changed=[],
    )

    cancelled_dir = RUN_DIR / "05_task_native_acceptance_cancelled"
    command_dir = RUN_DIR / "05_task_native_acceptance"
    if cancelled_dir.exists():
        raise RuntimeError("cancelled command-five archive already exists")
    os.replace(command_dir, cancelled_dir)
    _append_progress(
        "run_resumed",
        command_index=5,
        command_name="05_task_native_acceptance",
        completed_commands=4,
    )
    name, arguments = COMMANDS[4]
    results.append(_run_command(5, name, arguments))
    return _finalize(results, protected_before)


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["--resume-command-5"]:
            raise SystemExit(resume_command_5())
        if sys.argv[1:] == ["--recover-and-resume-command-5"]:
            raise SystemExit(recover_and_resume_command_5())
        if sys.argv[1:]:
            raise SystemExit(
                "usage: run_validation_chain.py "
                "[--resume-command-5|--recover-and-resume-command-5]"
            )
        raise SystemExit(main())
    except InterruptedError as error:
        _append_progress("run_cancelled", reason=str(error))
        _write_status("cancelled", reason=str(error))
        raise SystemExit(130) from error
    except Exception as error:
        traceback.print_exc()
        _append_progress("run_failed", error=repr(error))
        _write_status("failed", error=repr(error))
        raise
