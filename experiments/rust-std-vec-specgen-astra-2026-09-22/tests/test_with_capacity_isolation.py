import contextlib
import copy
import csv
import importlib.util
import io
import json
import os
from pathlib import Path
import py_compile
import re
import shutil
import subprocess
import sys
import time
import tomllib
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
BEFORE = ROOT / "tests/with-capacity/isolation/before"
OUTPUT = Path(os.environ.get(
    "CAPACITY_ISOLATION_OUTPUT", ROOT / "tests/with-capacity/isolation/regression",
)).resolve()
AGGREGATE = Path(os.environ.get(
    "CAPACITY_AGGREGATE_OUTPUT", ROOT / "proofs/correctness/vec/with-capacity/isolation/default",
)).resolve()
PROOF = Path(os.environ.get(
    "CAPACITY_PROOF_OUTPUT", ROOT / "proofs/correctness/vec/with-capacity/isolation/candidate",
)).resolve()
COMPLETENESS = Path(os.environ.get(
    "CAPACITY_COMPLETENESS_OUTPUT", ROOT / "proofs/completeness/vec/with-capacity/isolation/checker",
)).resolve()
REUSED = Path(os.environ.get(
    "CAPACITY_REUSED_OUTPUT", ROOT / "proofs/completeness/vec/reused-basic/isolation/checker",
)).resolve()
VERUS = ROOT / "toolchains/verus-x86-linux/verus"
BUILD_SCRIPT = ROOT / "proofs/correctness/vec/with-capacity/build.py"
CHECK_SCRIPT = ROOT / "proofs/completeness/vec/with-capacity/check.py"
API = "alloc::vec::Vec<T>::with_capacity"
TARGET = "vec/with_capacity.rs::vec::with_capacity::with_capacity"
GLOBAL_ERROR = "disallowed: constructor for an opaque datatype"


def read_json(path):
    return json.loads(path.read_text())


def run(output, name, arguments, timeout=115):
    command = [
        "bash", str(ROOT / "scripts/with_baseline.sh"),
        "env", f"TMPDIR={output / 'tmp'}", *map(str, arguments),
    ]
    with (output / f"{name}.command.json").open("x") as stream:
        stream.write(json.dumps(command, indent=2) + "\n")
    started = time.time_ns()
    with (output / f"{name}.stdout").open("x") as stdout, (
        output / f"{name}.stderr"
    ).open("x") as stderr:
        try:
            result = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr, timeout=timeout)
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
    return result


class WithCapacityIsolationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        OUTPUT.mkdir(parents=True, exist_ok=False)
        (OUTPUT / "tmp").mkdir()

    def test_entrypoints_and_unchanged_inputs(self):
        previous = (BEFORE / "specs/lib.rs").read_text()
        expected = previous.replace(
            "#![feature(allocator_api, const_heap, const_trait_impl)]",
            "#![feature(allocator_api)]",
        ).replace("    pub mod with_capacity;\n", "")
        self.assertEqual((ROOT / "specs/lib.rs").read_text(), expected)
        self.assertEqual((ROOT / "specs/with_capacity_candidate.rs").read_text(), (
            "#![feature(allocator_api, const_heap, const_trait_impl)]\n\n"
            "pub mod vec {\n    pub mod with_capacity;\n}\n"
        ))
        for source in (BEFORE / "specs").rglob("*.rs"):
            relative = source.relative_to(BEFORE / "specs")
            if relative != Path("lib.rs"):
                self.assertEqual((ROOT / "specs" / relative).read_bytes(), source.read_bytes())
        for current, saved in (
            ("proofs/correctness/vec/with_capacity.rs", "source-entry.rs"),
            ("proofs/correctness/vec/with-capacity/global_constructor.rs", "global_constructor.rs"),
            ("proofs/completeness/vec/reused-basic/check.py", "reused-basic-check.py"),
            ("review-criteria-temporary.txt", "review-criteria-temporary.txt"),
        ):
            self.assertEqual((ROOT / current).read_bytes(), (BEFORE / saved).read_bytes())
        baseline = ROOT / "proofs/correctness/vec/with-capacity/const-features"
        self.assertEqual((ROOT / "specs/vec/with_capacity.rs").read_bytes(),
                         (baseline / "sources/vec/with_capacity.rs").read_bytes())
        self.assertEqual(read_json(baseline / "aggregate.result.json")["returncode"], 1)
        self.assertIn(GLOBAL_ERROR, (baseline / "aggregate.stderr").read_text())
        previous_config = tomllib.loads((BEFORE / "specdet.toml").read_text())
        previous_config["targets"]["include"].remove("vec/with_capacity.rs")
        self.assertEqual(tomllib.loads((ROOT / "specdet.toml").read_text()), previous_config)

    def test_default_aggregate_compiles_all_three_source_obligations(self):
        AGGREGATE.mkdir(parents=True, exist_ok=False)
        (AGGREGATE / "tmp").mkdir()
        shutil.copytree(ROOT / "specs", AGGREGATE / "sources")
        library = AGGREGATE / "libvec_specs.rlib"
        result = run(AGGREGATE, "aggregate", [
            VERUS, ROOT / "specs/lib.rs", "--edition=2021", "--crate-type=lib",
            "--crate-name", "vec_specs", "--compile", "--num-threads=1",
            "--trace", "--log-all", "--log-dir", AGGREGATE / "logs", "-o", library,
        ])
        self.assertEqual(result.returncode, 0, (AGGREGATE / "aggregate.stderr").read_text())
        stdout = (AGGREGATE / "aggregate.stdout").read_text()
        self.assertIn("verification results:: 3 verified, 0 errors", stdout)
        air = (AGGREGATE / "logs/vec__reused_basic-final.air").read_text()
        self.assertEqual(re.findall(r"^;; Function-Def (\S+)$", air, re.MULTILINE), [
            f"vec_specs::vec::reused_basic::{name}" for name in ("default", "is_empty", "deref")
        ])
        self.assertEqual(air.count("\n(check-valid\n"), 3)
        transcript = (AGGREGATE / "logs/vec__reused_basic.smt_transcript").read_text().splitlines()
        self.assertEqual(transcript.count("(check-sat)"), 3)
        self.assertEqual(transcript.count("unsat"), 3)
        self.assertFalse(any(argument.startswith("--verify-") for argument in result.args))
        record = read_json(AGGREGATE / "aggregate.result.json")
        self.assertLessEqual(record["started_ns"], library.stat().st_mtime_ns)
        self.assertLessEqual(library.stat().st_mtime_ns, record["finished_ns"])
        self.assertGreater(library.stat().st_size, 0)

    def test_candidate_build_preserves_real_failure(self):
        result = run(OUTPUT, "candidate-build", [sys.executable, BUILD_SCRIPT, PROOF], 240)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Source verification/build failed: source, candidate",
                      (OUTPUT / "candidate-build.stderr").read_text())
        for name, entry, crate, module in (
            ("source", "proofs/correctness/vec/with_capacity.rs",
             "source_with_capacity", "with_capacity_source"),
            ("candidate", "specs/with_capacity_candidate.rs",
             "with_capacity_candidate", "vec::with_capacity"),
        ):
            with self.subTest(entry=name):
                record = read_json(PROOF / f"{name}.result.json")
                self.assertEqual(record["returncode"], 1)
                self.assertFalse(record["timed_out"])
                self.assertIn(GLOBAL_ERROR, (PROOF / f"{name}.stderr").read_text())
                self.assertIn("with_capacity_in(capacity, Global)",
                              (PROOF / f"{name}.stderr").read_text())
                self.assertFalse((PROOF / "build" / f"lib{crate}.rlib").exists())
                self.assertEqual((PROOF / f"{name}.source.rs").read_bytes(), (ROOT / entry).read_bytes())
                command = read_json(PROOF / f"{name}.command.json")
                self.assertIn(str(ROOT / entry), command)
                self.assertIn("--compile", command)
                self.assertEqual(command[-4:], [
                    "--verify-only-module", module, "--verify-function", "with_capacity",
                ])

    def test_candidate_checker_keeps_target_observation_and_failure(self):
        result = run(OUTPUT, "candidate-checker", [sys.executable, CHECK_SCRIPT, COMPLETENESS], 600)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Native checker failed: analyze=2, replay=2",
                      (OUTPUT / "candidate-checker.stderr").read_text())
        default = tomllib.loads((ROOT / "specdet.toml").read_text())
        expected = copy.deepcopy(default)
        settings = (
            (("project", "root"), str(ROOT / "specs")),
            (("adapters", "verus", "executable"), str(VERUS)),
            (("adapters", "verus", "environment", "TMPDIR"), str(COMPLETENESS / "tmp")),
            (("artifacts", "output_dir"), str(COMPLETENESS / "analysis-runs")),
            (("build", "entrypoint"), "with_capacity_candidate.rs"),
            (("targets", "include"), ["vec/with_capacity.rs"]),
        )
        changes = []
        for keys, value in settings:
            table = expected
            for key in keys[:-1]:
                table = table[key]
            changes.append({"setting": ".".join(keys), "before": table[keys[-1]], "after": value})
            table[keys[-1]] = value
        self.assertEqual(tomllib.loads((COMPLETENESS / "specdet.toml").read_text()), expected)
        self.assertEqual(read_json(COMPLETENESS / "config-changes.json"), changes)
        old = read_json(ROOT / "proofs/completeness/vec/with-capacity/const-features/analyze.json")
        old_revision = Path(old["results"][0]["proofs"][0]["artifact"]).parents[1] / "revisions/0"
        original_contract = read_json(old_revision / "contract.json")["payload"]["native"]
        original_plan = read_json(old_revision / "observation-plan.json")["payload"]
        original_obligation = read_json(old_revision / "obligation.json")["payload"]["native"]
        phases = {}
        for phase in ("analyze", "replay"):
            with self.subTest(phase=phase):
                data = read_json(COMPLETENESS / f"{phase}.json")
                phases[phase] = data
                self.assertEqual(read_json(COMPLETENESS / f"{phase}.result.json")["returncode"], 2)
                self.assertEqual(data["diagnostics"], [])
                self.assertEqual(data["discovery_coverage"], "source-visible")
                self.assertEqual([target["qualified_name"] for target in data["targets"]], [TARGET])
                self.assertEqual(len(data["results"]), 1)
                checked = data["results"][0]
                self.assertEqual(checked["target"]["qualified_name"], TARGET)
                self.assertEqual((checked["status"], checked["verdict"]), ("failed", "inconclusive"))
                self.assertIsNone(checked["baseline"])
                self.assertEqual(len(checked["proofs"]), 1)
                proof = checked["proofs"][0]
                self.assertEqual((proof["status"], proof["verified_goals"]), ("compile_error", 0))
                attempt = Path(proof["artifact"])
                revision = attempt.parents[1] / "revisions/0"
                contract = read_json(revision / "contract.json")["payload"]["native"]
                self.assertEqual(contract["function_spec"], original_contract["function_spec"])
                self.assertEqual(contract["source"].encode(), (ROOT / "specs/vec/with_capacity.rs").read_bytes())
                self.assertEqual(contract["overlays"], {})
                self.assertEqual(contract["accepted_semantics"], [])
                plan = read_json(revision / "observation-plan.json")["payload"]
                for key in ("policy", "analysis_kind", "ignored_dimensions"):
                    self.assertEqual(plan[key], original_plan[key])
                for key in ("comparisons", "equal_policy", "accepted_views", "source_bound_views"):
                    self.assertEqual(plan["native"][key], original_plan["native"][key])
                self.assertEqual(plan["native"]["comparisons"][0]["expression"], "(r1)@ =~= (r2)@")
                obligation = read_json(revision / "obligation.json")["payload"]["native"]
                self.assertEqual(obligation["source_function_spec"], original_contract["function_spec"])
                self.assertEqual(obligation["schemas"], original_obligation["schemas"])
                self.assertEqual(list(attempt.rglob("*.smt2")), [])
                self.assertEqual(Path(proof["native"]["entrypoint"]).name, "with_capacity_candidate.rs")
                self.assertEqual(len(proof["native"]["invocations"]), 1)
                process = proof["native"]["invocations"][0]["process"]
                self.assertEqual(process["returncode"], 1)
                self.assertFalse(process["timed_out"])
                self.assertIn(GLOBAL_ERROR, process["stderr"])
                self.assertIn("with_capacity_in(capacity, Global)", process["stderr"])
                self.assertEqual(Path(process["command"][1]).name, "with_capacity_candidate.rs")
                run_dir = Path(data["run_dir"])
                snapshot = read_json(run_dir / "snapshot.json")["payload"]
                self.assertEqual(set(snapshot["files"]), {
                    str(path.relative_to(ROOT / "specs")) for path in (ROOT / "specs").rglob("*.rs")
                })
                for relative in snapshot["files"]:
                    self.assertEqual((run_dir / "workspace" / relative).read_bytes(),
                                     (ROOT / "specs" / relative).read_bytes())
        self.assertNotEqual(phases["analyze"]["run_id"], phases["replay"]["run_id"])
        left, right = (phases[phase]["results"][0] for phase in ("analyze", "replay"))
        self.assertEqual(left["problem_id"], right["problem_id"])
        self.assertEqual(left["proofs"][0]["candidate_id"], right["proofs"][0]["candidate_id"])
        command = read_json(COMPLETENESS / "replay.command.json")
        self.assertIn("--reexecute", command)
        self.assertEqual(command[command.index("--run") + 1], phases["analyze"]["run_dir"])

    def test_checker_rejects_empty_targets_and_zero_goals(self):
        spec = importlib.util.spec_from_file_location("capacity_check", CHECK_SCRIPT)
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        real_run = checker.run
        for name, data, message in (
            ("empty-targets", {"targets": []}, "expected exactly the with_capacity target"),
            ("zero-goals", {
                "targets": [{"qualified_name": TARGET}], "counts": {"deterministic": 1},
                "results": [{"target": {"qualified_name": TARGET},
                             "proofs": [{"status": "verified", "verified_goals": 0}]}],
            }, "with_capacity has no successful proof obligation"),
        ):
            directory = OUTPUT / name
            data["run_dir"] = str(directory / "synthetic-negative-control")

            def negative_run(output, phase, arguments, timeout):
                if phase == "scratch-config":
                    return real_run(output, phase, arguments, timeout)
                return 0, data

            with self.subTest(case=name), patch.object(checker, "run", side_effect=negative_run), (
                patch.object(sys, "argv", [str(CHECK_SCRIPT), str(directory)])
            ), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(SystemExit, message):
                    checker.main()

    def test_confirmed_entries_reexecute_in_default_context(self):
        script = ROOT / "proofs/completeness/vec/reused-basic/check.py"
        result = run(OUTPUT, "reused-basic", [sys.executable, script, REUSED], 600)
        self.assertEqual(result.returncode, 0, (OUTPUT / "reused-basic.stderr").read_text())
        config = tomllib.loads((REUSED / "specdet.toml").read_text())
        self.assertEqual(config["build"]["entrypoint"], "lib.rs")
        self.assertEqual(config["targets"], tomllib.loads((ROOT / "specdet.toml").read_text())["targets"])
        names = ["default", "is_empty", "deref"]
        expected_targets = [f"vec/reused_basic.rs::vec::reused_basic::{name}" for name in names]
        phases = {}
        for phase in ("analyze", "replay"):
            data = read_json(REUSED / f"{phase}.json")
            phases[phase] = data
            self.assertEqual(read_json(REUSED / f"{phase}.result.json")["returncode"], 0)
            self.assertEqual([target["qualified_name"] for target in data["targets"]], expected_targets)
            self.assertEqual([result["target"]["qualified_name"] for result in data["results"]], expected_targets)
            self.assertEqual(data["counts"], {"deterministic": 3})
            for checked in data["results"]:
                self.assertEqual(checked["baseline"]["status"], "unsat")
                self.assertEqual(len(checked["proofs"]), 1)
                proof = checked["proofs"][0]
                self.assertEqual((proof["status"], proof["verified_goals"]), ("verified", 1))
                self.assertEqual(Path(proof["native"]["entrypoint"]).name, "lib.rs")
                self.assertEqual(len(proof["native"]["invocations"]), 1)
                process = proof["native"]["invocations"][0]["process"]
                self.assertEqual(process["returncode"], 0)
                self.assertFalse(process["timed_out"])
                self.assertIn("verification results:: 1 verified, 0 errors", process["stdout"])
                self.assertTrue(Path(checked["baseline"]["artifact"]).is_file())
        self.assertNotEqual(phases["analyze"]["run_id"], phases["replay"]["run_id"])
        command = read_json(REUSED / "replay.command.json")
        self.assertIn("--reexecute", command)
        self.assertEqual(command[command.index("--run") + 1], phases["analyze"]["run_dir"])

    def test_contract_clients_still_report_candidate_failure(self):
        result = run(OUTPUT, "clients", [
            VERUS, ROOT / "tests/with_capacity_clients.rs", "--edition=2021", "--crate-type=lib",
            "--crate-name", "capacity_clients", "--compile", "--num-threads=1", "--verify-root",
            "--log-all", "--log-dir", OUTPUT / "clients", "-o", OUTPUT / "libcapacity_clients.rlib",
        ])
        self.assertEqual(result.returncode, 1)
        self.assertIn(GLOBAL_ERROR, (OUTPUT / "clients.stderr").read_text())
        self.assertIn("with_capacity_in(capacity, Global)", (OUTPUT / "clients.stderr").read_text())
        self.assertFalse((OUTPUT / "libcapacity_clients.rlib").exists())

    def test_coverage_preserves_other_rows_and_seven_completions(self):
        with (BEFORE / "coverage.tsv").open() as stream:
            before = list(csv.DictReader(stream, delimiter="\t"))
        with (ROOT / "inventory/coverage.tsv").open() as stream:
            after = list(csv.DictReader(stream, delimiter="\t"))
        self.assertEqual(len(before), 138)
        self.assertEqual(len(after), 138)
        for left, right in zip(before, after):
            self.assertEqual(left["canonical_api"], right["canonical_api"])
            if right["canonical_api"] != API:
                self.assertEqual(left, right)
            else:
                self.assertTrue(right["correctness_result"].startswith("not_verified;"))
                self.assertTrue(right["completeness_result"].startswith("inconclusive;"))
                self.assertIn("0 verified goals", right["completeness_result"])
        completed = [
            row["canonical_api"] for row in after
            if row["correctness_result"].startswith("1 verified, 0 errors;")
            and row["completeness_result"].startswith("deterministic;")
            and "confirmed" in row["independent_review"]
        ]
        self.assertEqual(len(completed), 7)
        self.assertNotIn(API, completed)

    def test_modified_python_scripts_compile_to_private_output(self):
        for source in (BUILD_SCRIPT, CHECK_SCRIPT, ROOT / "tests/test_with_capacity.py"):
            py_compile.compile(str(source), cfile=str(OUTPUT / f"{source.stem}.pyc"), doraise=True)


if __name__ == "__main__":
    unittest.main()
