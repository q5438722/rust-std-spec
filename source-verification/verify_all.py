#!/usr/bin/env python3
"""Run all source-level Verus contract derivations and summarize the trust boundary."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
VERUS = WORKSPACE / "verus" / "source" / "target-verus" / "release" / "verus"
Z3 = WORKSPACE / "verus" / "source" / "z3"

CASES = [
    {
        "file": "pure_control_flow.rs",
        "contracts": 16,
        "level": "A",
        "basis": "Copied enum matches; no lower external contract is needed.",
    },
    {
        "file": "residual.rs",
        "contracts": 2,
        "level": "C",
        "basis": (
            "Copied FromResidual bodies using FromSpec plus one trusted axiom that "
            "core::convert::Infallible is uninhabited."
        ),
    },
    {
        "file": "vecdeque.rs",
        "contracts": 2,
        "level": "B",
        "basis": "Copied control flow, using trusted len/swap/pop_front/pop_back contracts.",
    },
    {
        "file": "collections.rs",
        "contracts": 6,
        "level": "B",
        "basis": "Copied one-line compositions using trusted len/get/new contracts.",
    },
    {
        "file": "capacity_composed.rs",
        "contracts": 4,
        "level": "B",
        "basis": (
            "Source-equivalent constructor compositions using trusted new/reserve and "
            "capacity contracts."
        ),
    },
    {
        "file": "net.rs",
        "contracts": 15,
        "level": "B",
        "basis": "Copied/desugared address operations using trusted octets/constructor contracts.",
    },
    {
        "file": "net_enums.rs",
        "contracts": 7,
        "level": "B",
        "basis": (
            "Copied IpAddr enum matches using the structural enum View and lower IPv4/IPv6 "
            "contracts."
        ),
    },
    {
        "file": "socket_addr.rs",
        "contracts": 7,
        "level": "B",
        "basis": (
            "Copied SocketAddr enum matches using the structural enum View and lower "
            "SocketAddrV4/V6 contracts."
        ),
    },
    {
        "file": "ffi.rs",
        "contracts": 4,
        "level": "B",
        "basis": "Copied public compositions using trusted CStr/CString view-producing methods.",
    },
    {
        "file": "layout.rs",
        "contracts": 7,
        "level": "C",
        "basis": (
            "Public-API copies plus trusted Layout view validity and two rounding lemmas; "
            "private Alignment internals are inaccessible downstream."
        ),
    },
    {
        "file": "duration_integer.rs",
        "contracts": 19,
        "level": "C",
        "basis": (
            "Integer/public-API copies plus the trusted invariant "
            "duration@ <= Duration::MAX."
        ),
    },
    {
        "file": "duration_from_secs.rs",
        "contracts": 2,
        "level": "B",
        "basis": (
            "Copied panic wrappers using the lower try_from_secs_f32/f64 contracts; "
            "the error branch is proved unreachable from the validity precondition."
        ),
    },
    {
        "file": "duration_try_from.rs",
        "contracts": 2,
        "level": "E",
        "basis": (
            "Source-faithful f32/f64 control flow, but the complete rounding/overflow "
            "equivalence remains in two trusted arithmetic-model axioms; the private error "
            "representation is only modeled by a local mirror."
        ),
    },
    {
        "file": "duration_float.rs",
        "contracts": 8,
        "level": "D",
        "basis": (
            "Copied float bodies under duration_float_ieee_semantics() and explicit "
            "RFC 3514 bridges from relational executable float specs to IEEE spec operators."
        ),
    },
]


def target_cfg(path: Path) -> list[str]:
    environment = os.environ.copy()
    environment["RUSTC_BOOTSTRAP"] = "1"
    process = subprocess.run(
        [
            "rustc",
            "+1.96.0",
            "-Zunstable-options",
            "--target",
            str(path),
            "--print",
            "cfg",
        ],
        env=environment,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        return [f"probe_error={process.stderr.strip()}"]
    return sorted(line for line in process.stdout.splitlines() if "target_feature" in line)


def main() -> int:
    environment = os.environ.copy()
    environment["VERUS_Z3_PATH"] = str(Z3)
    results = []
    for case in CASES:
        path = ROOT / case["file"]
        process = subprocess.run(
            [str(VERUS), str(path), "--rlimit", "600", "--multiple-errors", "80"],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )
        output = process.stdout + process.stderr
        match = re.search(r"verification results:: (\d+) verified, (\d+) errors", output)
        result = {
            **case,
            "returncode": process.returncode,
            "verified_functions": int(match.group(1)) if match else None,
            "errors": int(match.group(2)) if match else None,
            "output": output,
        }
        results.append(result)
        status = "ok" if process.returncode == 0 else "failed"
        print(
            f"{case['file']}: {status}, "
            f"verified={result['verified_functions']}, errors={result['errors']}",
            flush=True,
        )

    user_target = WORKSPACE / "nanvix" / "build" / "targets" / "x86-user.json"
    kernel_target = WORKSPACE / "nanvix" / "build" / "targets" / "x86-kernel.json"
    target_assessment = {
        "x86_user_cfg": target_cfg(user_target),
        "x86_kernel_cfg": target_cfg(kernel_target),
        "x86_user_ieee_predicate": "not_established_no_sse2_cfg",
        "x86_kernel_ieee_predicate": "not_established_softfloat_requires_separate_audit",
    }
    payload = {
        "contracts_with_source_derivations": sum(case["contracts"] for case in CASES),
        "contracts_without_duration_float_target_axiom": sum(
            case["contracts"] for case in CASES if case["level"] != "D"
        ),
        "contracts_conditional_on_float_target_axiom": sum(
            case["contracts"] for case in CASES if case["level"] == "D"
        ),
        "all_passed": all(result["returncode"] == 0 for result in results),
        "target_assessment": target_assessment,
        "results": results,
    }
    (ROOT / "summary.json").write_text(json.dumps(payload, indent=2) + "\n")

    lines = [
        "# Source-level verification of generated Rust std contracts",
        "",
        f"- Derived contracts: **{payload['contracts_with_source_derivations']}**",
        "- Without `duration_float_ieee_semantics()`: "
        f"**{payload['contracts_without_duration_float_target_axiom']}**",
        "- Conditional on the float target axiom: "
        f"**{payload['contracts_conditional_on_float_target_axiom']}**",
        f"- All harnesses passed: **{payload['all_passed']}**",
        "",
        "| Harness | Contracts | Level | Verus result | Trusted basis |",
        "|---|---:|---|---|---|",
    ]
    for result in results:
        verification = (
            f"{result['verified_functions']} verified, {result['errors']} errors"
            if result["verified_functions"] is not None
            else f"exit {result['returncode']}"
        )
        lines.append(
            f"| `{result['file']}` | {result['contracts']} | {result['level']} | "
            f"{verification} | {result['basis']} |"
        )
    lines.extend(
        [
            "",
            "## Levels",
            "",
            "- **A:** copied body proves the contract without another Rust external contract.",
            "- **B:** copied body is verified compositionally from smaller trusted std contracts.",
            "- **C:** additionally depends on a trusted representation/type invariant.",
            "- **D:** additionally depends on an explicit target-semantics axiom.",
            "- **E:** source control flow is copied, but the central numerical/error",
            "  equivalence is still captured by a large trusted model axiom.",
            "",
            "A successful harness removes trust from the target contract only relative to its",
            "listed lower-level assumptions. It does not prove the Rust compiler or private",
            "standard-library representation itself.",
            "",
            "## Nanvix floating-point target assessment",
            "",
            f"- `x86-user.json`: `{target_assessment['x86_user_cfg']}`",
            "  `duration_float_ieee_semantics()` is not established because SSE2 is not",
            "  enabled in the effective cfg; RFC 3514 documents finite-result excess-",
            "  precision deviations on 32-bit x86 without SSE2.",
            f"- `x86-kernel.json`: `{target_assessment['x86_kernel_cfg']}`",
            "  the target requests soft-float, but the compiler-builtins path still needs",
            "  a separate conformance audit before the predicate can be assumed.",
        ]
    )
    (ROOT / "SUMMARY.md").write_text("\n".join(lines) + "\n")
    return 0 if payload["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
