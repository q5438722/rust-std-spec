#!/usr/bin/env python3
"""Supplemental official-contract clients; not source or completeness proofs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "binding_probes.rs"
CASES = [
    ("positive", 0, "5 verified, 0 errors", "Generic len, Index<I>, range indexing, usize mutable syntax and Box<[T],A>::into_vec."),
    ("next", 0, "1 verified, 0 errors", "IntoIter<T,A> generic next + concrete IteratorSpecImpl."),
    ("next_back", 0, "1 verified, 0 errors", "IntoIter<T,A> generic next_back + concrete law predicate."),
    ("from_iter", 0, "1 verified, 0 errors", "Full I:IntoIterator input domain; literal opaque into_iter_remaining relation."),
    ("eq", 0, "1 verified, 0 errors", "T:PartialEq<U> and distinct generic A1/A2; literal conditional equality model."),
    ("ne", 0, "1 verified, 0 errors", "Explicit Vec/Vec ne uses generic trait + concrete model without its own assume declaration."),
    ("as_ref_vec", 1, "is not supported", "No exact <Vec<T,A> as AsRef<Vec<T,A>>>::as_ref binding."),
    ("as_ref_slice", 1, "is not supported", "No exact <Vec<T,A> as AsRef<[T]>>::as_ref binding."),
    ("as_mut_vec", 1, "is not supported", "No exact <Vec<T,A> as AsMut<Vec<T,A>>>::as_mut binding."),
    ("as_mut_slice", 1, "is not supported", "No exact <Vec<T,A> as AsMut<[T]>>::as_mut binding."),
    ("index_mut_range", 1, "postcondition not satisfied", "General IndexMut range content/frame is not supplied."),
    ("index_mut_usize_ufcs", 1, "postcondition not satisfied", "Even usize UFCS lacks the mutable-index syntax hook's postcondition."),
    ("into_iter_elts_after_next", 1, "postcondition not satisfied", "Constructor-only elts/remaining equality is not propagated across next."),
    ("from_iter_vec_contents", 1, "postcondition not satisfied", "into_iter_remaining(Vec) is not tied to the Vec sequence by the Iterator-only axiom."),
    ("try_reserve_variant", 1, "postcondition not satisfied", "Existing try_reserve only frames contents; no success-variant guarantee, even for zero."),
]


def main():
    env = os.environ.copy()
    env.update({
        "RUSTUP_HOME": str(ROOT / "toolchains/rustup"),
        "CARGO_HOME": str(ROOT / "toolchains/cargo"),
        "RUSTUP_TOOLCHAIN": "1.98.1-x86_64-unknown-linux-gnu",
        "RUSTC_BOOTSTRAP": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    deadline = time.monotonic() + 110
    results = []
    executable = ROOT / "toolchains/verus-x86-linux/verus"
    with tempfile.TemporaryDirectory(prefix="binding-tmp-", dir=HERE) as temp:
        env["TMPDIR"] = temp
        version = subprocess.run([str(executable), "--version"], cwd=ROOT, env=env,
                                 text=True, capture_output=True, timeout=10, check=True)
        if "0.2026.09.20.aef82ed" not in version.stdout:
            raise RuntimeError("unexpected official binary version")
        for name, expected_exit, diagnostic, purpose in CASES:
            command = [str(executable), "--crate-type=lib", "--out-dir", temp,
                       "--cfg", "probe_" + name, str(FIXTURE)]
            remaining = deadline - time.monotonic()
            if remaining <= 1:
                raise TimeoutError("110-second command budget exhausted; rerun via the Argus durable runner")
            process = subprocess.run(command, cwd=ROOT, env=env, text=True,
                                     capture_output=True, timeout=min(18, remaining))
            output = process.stdout + process.stderr
            matched = process.returncode == expected_exit and diagnostic in output
            results.append({
                "probe": name, "purpose": purpose,
                "command": ["toolchains/verus-x86-linux/verus", "--crate-type=lib",
                            "--out-dir", "<temporary directory under inventory/vstd-tests>",
                            "--cfg", "probe_" + name, "inventory/vstd-tests/binding_probes.rs"],
                "expected_exit": expected_exit, "actual_exit": process.returncode,
                "expected_diagnostic": diagnostic, "matched_expectation": matched,
                "stdout": process.stdout, "stderr": process.stderr,
                "interpretation": "official-contract client verified" if expected_exit == 0 else
                                  "expected unsupported binding or unproved strengthening; not a Rust-source counterexample",
            })
    record = {
        "purpose": __doc__,
        "fixture_sha256": hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
        "binary_version_stdout": version.stdout,
        "environment": {k: v.replace(str(ROOT) + "/", "") for k, v in env.items()
                        if k in ("RUSTUP_HOME", "CARGO_HOME", "RUSTUP_TOOLCHAIN", "RUSTC_BOOTSTRAP")},
        "all_matched": all(r["matched_expectation"] for r in results),
        "cases": len(results), "positive_cases": sum(r["expected_exit"] == 0 for r in results),
        "negative_controls": sum(r["expected_exit"] != 0 for r in results),
        "results": results,
    }
    (HERE / "binding_results.json").write_text(json.dumps(record, indent=2) + "\n")
    failed = [r["probe"] for r in results if not r["matched_expectation"]]
    if failed:
        print("BINDING CHECK FAILED: " + ", ".join(failed), file=sys.stderr)
        return 1
    print(f"BINDING CHECK PASS: {record['cases']} cases "
          f"({record['positive_cases']} positive groups; {record['negative_controls']} expected-negative controls)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
