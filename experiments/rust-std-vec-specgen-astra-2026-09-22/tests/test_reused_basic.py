import copy
import csv
import json
import os
from pathlib import Path
import re
import subprocess
import time
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUST = Path("/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library")
VERUS = ROOT / "toolchains/verus-x86-linux"
RUSTC = ROOT / "toolchains/rustup/toolchains/1.98.1-x86_64-unknown-linux-gnu/bin/rustc"
PROOF = Path(os.environ.get(
    "REUSED_PROOF_OUTPUT", ROOT / "proofs/correctness/vec/reused-basic/source",
)).resolve()
COMPLETENESS = Path(os.environ.get(
    "REUSED_COMPLETENESS_OUTPUT", ROOT / "proofs/completeness/vec/reused-basic/engineer",
)).resolve()
OUTPUT = Path(os.environ.get("REUSED_TEST_OUTPUT", ROOT / "tests/reused-basic/engineer")).resolve()
CASES = {
    "default": {
        "generics": "<T>", "target": "<Vec<T> as core::default::Default>::default",
        "return": "Vec<T>", "binding": "v", "params": [],
        "ensures": "v@ == Seq::<T>::empty()", "body": "Vec::new()",
        "lines": (4256, 4264), "dependency": "new",
        "comparison": "(r1)@ =~= (r2)@",
        "guards": ["g_r1_leneq", "g_r1_lenrng", "g_r2_leneq", "g_r2_lenrng", "g_neq_tuple"],
    },
    "is_empty": {
        "generics": "<T, A: Allocator>", "target": "<Vec<T, A>>::is_empty",
        "return": "bool", "binding": "res", "params": ["v"],
        "ensures": "res <==> v@.len() == 0", "body": "v.len() == 0",
        "lines": (3033, 3049), "dependency": "len",
        "comparison": "r1 == r2",
        "guards": [
            "g_v_leneq", "g_v_lenrng", "g_r1_is_true", "g_r1_is_false",
            "g_r2_is_true", "g_r2_is_false", "g_neq_tuple",
        ],
    },
    "deref": {
        "generics": "<T, A: Allocator>", "target": "<Vec<T, A> as core::ops::Deref>::deref",
        "return": "&[T]", "binding": "slice", "params": ["vec"],
        "ensures": "slice@ == vec@", "body": "vec.as_slice()",
        "lines": (3749, 3756), "dependency": "as_slice",
        "comparison": "r1 =~= r2",
        "guards": [
            "g_vec_leneq", "g_vec_lenrng", "g_r1_leneq", "g_r1_lenrng",
            "g_r2_leneq", "g_r2_lenrng", "g_neq_tuple",
        ],
    },
}


def compact(text):
    return re.sub(r"\s+", "", text).replace(",)", ")")


def source_function(text, name):
    const = "const" if name == "is_empty" else ""
    prefix = compact(f"pub {const} fn {name}{CASES[name]['generics']}")
    contract, body = compact(text).split(prefix, 1)[1].split("{", 1)
    return prefix, contract, body.split("}", 1)[0]


def read_json(path):
    return json.loads(path.read_text())


def run(name, arguments, bootstrap="1"):
    command = [
        "bash", str(ROOT / "scripts/with_baseline.sh"), "env",
        f"TMPDIR={OUTPUT / 'tmp'}", f"RUSTC_BOOTSTRAP={bootstrap}", *map(str, arguments),
    ]
    (OUTPUT / f"{name}.command.json").write_text(json.dumps(command, indent=2) + "\n")
    started = time.time_ns()
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=115)
    except subprocess.TimeoutExpired as error:
        (OUTPUT / f"{name}.stdout").write_bytes(error.stdout or b"")
        (OUTPUT / f"{name}.stderr").write_bytes(error.stderr or b"")
        (OUTPUT / f"{name}.result.json").write_text(json.dumps({
            "returncode": None, "timed_out": True,
            "started_ns": started, "finished_ns": time.time_ns(),
        }, indent=2) + "\n")
        raise
    (OUTPUT / f"{name}.stdout").write_text(result.stdout)
    (OUTPUT / f"{name}.stderr").write_text(result.stderr)
    (OUTPUT / f"{name}.result.json").write_text(json.dumps({
        "returncode": result.returncode, "timed_out": False,
        "started_ns": started, "finished_ns": time.time_ns(),
    }, indent=2) + "\n")
    return result


class ReusedBasicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        OUTPUT.mkdir(parents=True, exist_ok=False)
        (OUTPUT / "tmp").mkdir()
        cls.links = [
            "-L", f"dependency={PROOF / 'build'}",
            "-L", f"dependency={VERUS}", "-L", f"dependency={VERUS / 'deps'}",
        ]
        inputs = {}
        for name in CASES:
            library = PROOF / "build" / f"libreused_{name}.rlib"
            record = read_json(PROOF / f"{name}.result.json")
            if record["returncode"] != 0 or record["timed_out"]:
                raise AssertionError(f"Current source build failed: {name}")
            if not record["started_ns"] <= library.stat().st_mtime_ns <= record["finished_ns"]:
                raise AssertionError(f"Library was not produced by the recorded build: {library}")
            cls.links += ["--extern", f"reused_{name}={library}"]
            inputs[name] = {
                "library": str(library), "mtime_ns": library.stat().st_mtime_ns,
                "build_record": str(PROOF / f"{name}.result.json"),
            }
        if (PROOF / "reused_basic.source.rs").read_bytes() != (
            ROOT / "specs/vec/reused_basic.rs"
        ).read_bytes():
            raise AssertionError("The recorded source build is not the current candidate")
        (OUTPUT / "linked-inputs.json").write_text(json.dumps(inputs, indent=2) + "\n")

    def probe(self, name, source, bootstrap="1"):
        path = OUTPUT / f"{name}.rs"
        path.write_text(source)
        (OUTPUT / f"{name}.input.json").write_text(json.dumps({"source": source}, indent=2) + "\n")
        try:
            return run(name, [
                RUSTC, "--edition=2021", "--crate-type=lib", "--crate-name", "reused_probe",
                "--emit=metadata", path, *self.links, "-o", OUTPUT / f"{name}.rmeta",
            ], bootstrap)
        finally:
            path.unlink()

    def test_official_source_and_trait_correspondence(self):
        official = (ROOT / "toolchains/upstream/source/vstd/std_specs/vec.rs").read_text()
        candidate = (ROOT / "specs/vec/reused_basic.rs").read_text()
        original = (RUST / "alloc/src/vec/mod.rs").read_text().splitlines()
        self.assertEqual(re.findall(r"pub\s+(?:const\s+)?fn\s+(\w+)", candidate), list(CASES))
        self.assertNotRegex(candidate, r"\b(assume_specification|assume|admit|external_body|unsafe)\b")
        report = {}
        for name, case in CASES.items():
            with self.subTest(api=name):
                prefix = compact(f"pub assume_specification{case['generics']}[{case['target']}]")
                contract = compact(official).split(prefix, 1)[1].split(";", 1)[0]
                source_prefix, source_contract, body = source_function(candidate, name)
                self.assertEqual(source_contract, contract)
                self.assertEqual(body, compact(case["body"]))
                lo, hi = case["lines"]
                span = "\n".join(original[lo - 1:hi])
                method = re.search(rf"(fn {name}\([^{{]+)\{{([^}}]+)\}}", span)
                self.assertIsNotNone(method)
                receiver = {"default": "self", "is_empty": "v", "deref": "vec"}[name]
                self.assertEqual(compact(re.sub(r"\bself\b", receiver, method[2])), body)
                if name == "default":
                    self.assertIn("impl<T> const Default for Vec<T>", span)
                    self.assertIn('feature = "const_default"', span)
                    self.assertEqual(compact(method[0]), "fndefault()->Vec<T>{Vec::new()}")
                elif name == "is_empty":
                    self.assertIn("pub const fn is_empty(&self) -> bool", span)
                    self.assertIn('since = "1.87.0"', span)
                else:
                    self.assertIn("impl<T, A: Allocator> ops::Deref for Vec<T, A>", span)
                    self.assertIn("type Target = [T];", span)
                    self.assertIn("fn deref(&self) -> &[T]", span)
                report[name] = {
                    "canonical_binding": case["target"],
                    "rust_source": f"{RUST}/alloc/src/vec/mod.rs:{lo}-{hi}",
                    "official_declaration": prefix + contract + ";",
                    "source_entry": source_prefix + source_contract,
                    "body": body,
                    "checker_target": f"vec/reused_basic.rs::vec::reused_basic::{name}",
                    "receiver_substitution": receiver if name != "default" else None,
                }
        traits = ROOT / "toolchains/upstream/source/vstd/std_specs"
        self.assertIn(compact("""
            pub trait ExDefault: Sized {
                type ExternalTraitSpecificationFor: core::default::Default;
                fn default() -> (r: Self);
            }
        """), compact((traits / "default.rs").read_text()))
        self.assertIn(compact("""
            pub trait ExDeref: PointeeSized {
                type ExternalTraitSpecificationFor: core::ops::Deref;
                type Target: ?Sized;
                fn deref(&self) -> &Self::Target;
            }
        """), compact((traits / "core.rs").read_text()))
        self.assertIn("pub const trait Default: Sized", (RUST / "core/src/default.rs").read_text())
        self.assertIn("fn default() -> Self;", (RUST / "core/src/default.rs").read_text())
        deref_trait = (RUST / "core/src/ops/deref.rs").read_text()
        self.assertIn("type Target: ?Sized;", deref_trait)
        self.assertIn("fn deref(&self) -> &Self::Target;", deref_trait)
        (OUTPUT / "correspondence.json").write_text(json.dumps(report, indent=2) + "\n")

    def test_current_nonzero_source_builds_and_lowered_calls(self):
        for name in (*CASES, "aggregate"):
            with self.subTest(api=name):
                record = read_json(PROOF / f"{name}.result.json")
                command = read_json(PROOF / f"{name}.command.json")
                self.assertEqual(record["returncode"], 0)
                self.assertFalse(record["timed_out"])
                self.assertIn("--compile", command)
                self.assertIn(str(VERUS / "verus"), command)
                expected = 3 if name == "aggregate" else 1
                self.assertIn(
                    f"verification results:: {expected} verified, 0 errors",
                    (PROOF / f"{name}.stdout").read_text(),
                )
                entry = ROOT / ("specs/lib.rs" if name == "aggregate" else f"proofs/correctness/vec/{name}.rs")
                self.assertEqual((PROOF / f"{name}.source.rs").read_bytes(), entry.read_bytes())
                if name == "aggregate":
                    continue
                self.assertEqual(command[-4:], ["--verify-only-module", "reused_basic", "--verify-function", name])
                self.assertIn('../../../specs/vec/reused_basic.rs', entry.read_text())
                vir = (PROOF / name / "crate.vir").read_text()
                start = vir.index(f":name (Fun :path reused_{name}::reused_basic::{name})")
                section = vir[start:vir.index(":extra_dependencies", start)]
                self.assertIn(":require ()", section)
                self.assertIn(":is_external_body false", section)
                body = re.split(r"\)\s+:body\s+\(@@", section, maxsplit=1)[1]
                calls = re.findall(r"\(Fun :path (alloc::vec::[^\s)]+)\)", body)
                self.assertEqual(len(calls), 1)
                self.assertTrue(calls[0].endswith("::" + CASES[name]["dependency"]), calls)
                self.assertNotRegex(body, r"core::(?:default::Default|ops::Deref)::|::is_empty\b")
                (OUTPUT / f"{name}.lowered-body.txt").write_text(body)

    def test_native_behavior_uses_newly_compiled_libraries(self):
        source = ROOT / "tests/reused_basic_behavior.rs"
        (OUTPUT / "native.source.rs").write_bytes(source.read_bytes())
        build = run("native-build", [
            RUSTC, "--edition=2021", "--test", source, *self.links, "-o", OUTPUT / "native-tests",
        ])
        self.assertEqual(build.returncode, 0, build.stderr)
        result = run("native-tests", [OUTPUT / "native-tests", "--test-threads=1"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("7 passed; 0 failed", result.stdout)

    def test_official_bindings_and_source_clients(self):
        source = ROOT / "tests/reused_basic_clients.rs"
        (OUTPUT / "clients.source.rs").write_bytes(source.read_bytes())
        result = run("clients", [
            VERUS / "verus", source, "--edition=2021", "--crate-type=lib",
            "--crate-name", "reused_clients", "--compile", "--num-threads=1",
            "--verify-root", "--log-all", "--log-dir", OUTPUT / "clients",
            "-o", OUTPUT / "libreused_clients.rlib",
        ])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("verification results:: 6 verified, 0 errors", result.stdout)

    def test_stable_const_is_empty(self):
        result = self.probe("stable-is-empty", """
            static EMPTY: Vec<i32> = Vec::new();
            const SOURCE: bool = reused_is_empty::is_empty(&EMPTY);
            const OFFICIAL: bool = Vec::is_empty(&EMPTY);
            const _: () = assert!(SOURCE && OFFICIAL);
            pub const fn arbitrary<T>(v: &Vec<T>) -> bool {
                reused_is_empty::is_empty(v) == Vec::is_empty(v)
            }
        """, bootstrap="0")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unstable_const_default(self):
        result = self.probe("unstable-default-enabled", """
            #![feature(const_default, const_trait_impl)]
            struct NotDefault;
            static EMPTY: Vec<NotDefault> = <Vec<NotDefault> as Default>::default();
            const _: () = assert!(EMPTY.is_empty());
        """)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_stable_const_default_is_rejected(self):
        result = self.probe("stable-default-rejected", """
            static EMPTY: Vec<i32> = <Vec<i32> as Default>::default();
        """, bootstrap="0")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error[E0658]", result.stderr)
        self.assertIn("Default", result.stderr)
        self.assertIn("const", result.stderr)
        self.assertRegex(result.stderr, r"cannot call conditionally-const|not yet stable as a const")

    def test_source_default_is_runtime_only(self):
        result = self.probe("source-default-runtime-only", """
            static EMPTY: Vec<i32> = reused_default::default();
        """, bootstrap="0")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error[E0015]", result.stderr)
        self.assertIn("non-const", result.stderr)

    def test_type_and_borrow_rejections(self):
        for kind in ("source", "official"):
            default = "reused_default::default()" if kind == "source" else "Default::default()"
            empty = "reused_is_empty::is_empty(v)" if kind == "source" else "Vec::is_empty(v)"
            deref = "reused_deref::deref" if kind == "source" else "<Vec<i32> as std::ops::Deref>::deref"
            cases = {
                "default-type": (f"fn f() -> [i32; 0] {{ let v: Vec<i32> = {default}; v }}", {"E0308"}),
                "empty-type": (f"fn f(v: &Vec<i32>) -> usize {{ {empty} }}", {"E0308"}),
                "deref-type": (f"fn f(v: &Vec<i32>) -> &Vec<i32> {{ {deref}(v) }}", {"E0308"}),
                "deref-mut": (f"fn f(v: &Vec<i32>) -> &mut [i32] {{ {deref}(v) }}", {"E0308"}),
                "deref-escape": (f"fn f<'a>() -> &'a [i32] {{ let v = vec![1]; {deref}(&v) }}", {"E0515"}),
                "deref-live-borrow": (
                    f"fn f() {{ let mut v = vec![1]; let s = {deref}(&v); v.push(2); let _ = s[0]; }}",
                    {"E0502"},
                ),
                "default-element-escape": (
                    f"fn f<'a>() -> Vec<&'a i32> {{ let x = 1; let mut v: Vec<&i32> = {default}; v.push(&x); v }}",
                    {"E0515", "E0597"},
                ),
            }
            for name, (source, expected) in cases.items():
                with self.subTest(kind=kind, probe=name):
                    result = self.probe(f"{kind}-{name}", source)
                    self.assertNotEqual(result.returncode, 0)
                    codes = set(re.findall(r"^error\[(E\d+)\]", result.stderr, re.MULTILINE))
                    self.assertTrue(codes, result.stderr)
                    self.assertTrue(codes <= expected, result.stderr)
                    self.assertFalse((OUTPUT / f"{kind}-{name}.rs").exists())

    def test_config_and_coverage_scope(self):
        before = ROOT / "proofs/correctness/vec/reused-basic"
        original = tomllib.loads((before / "specdet.before.toml").read_text())
        current = tomllib.loads((ROOT / "specdet.toml").read_text())
        original["targets"]["include"].append("vec/reused_basic.rs")
        self.assertEqual(current, original)
        expected = copy.deepcopy(current)
        expected["project"]["root"] = str(ROOT / "specs")
        expected["adapters"]["verus"]["executable"] = str(VERUS / "verus")
        expected["adapters"]["verus"]["environment"]["TMPDIR"] = str(COMPLETENESS / "tmp")
        expected["artifacts"]["output_dir"] = str(COMPLETENESS / "analysis-runs")
        self.assertEqual(tomllib.loads((COMPLETENESS / "specdet.toml").read_text()), expected)
        prior_lib = (before / "lib.before.rs").read_text()
        self.assertEqual(
            (ROOT / "specs/lib.rs").read_text(),
            prior_lib.replace("    pub mod owned_conversions;\n", "    pub mod owned_conversions;\n    pub mod reused_basic;\n"),
        )
        with (before / "coverage-before.tsv").open() as stream:
            old = list(csv.DictReader(stream, delimiter="\t"))
        with (ROOT / "inventory/coverage.tsv").open() as stream:
            new = list(csv.DictReader(stream, delimiter="\t"))
        self.assertEqual(len(old), 138)
        self.assertEqual(len(new), 138)
        expected_changes = {
            "<alloc::vec::Vec<T> as core::default::Default>::default",
            "alloc::vec::Vec<T, A>::is_empty",
            "<alloc::vec::Vec<T, A> as core::ops::Deref>::deref",
            "<alloc::vec::Vec<T> as core::convert::From<[T; N]>>::from",
            "<alloc::vec::Vec<T, A> as core::convert::From<alloc::boxed::Box<[T], A>>>::from",
        }
        changed = {}
        for left, right in zip(old, new):
            self.assertEqual(left["canonical_api"], right["canonical_api"])
            fields = [key for key in left if left[key] != right[key]]
            if fields:
                changed[right["canonical_api"]] = fields
                if "core::convert::From" in right["canonical_api"]:
                    self.assertEqual(fields, ["independent_review"])
                    self.assertIn("db4ff3669ca5", right["independent_review"])
                else:
                    self.assertEqual(right["vstd_coverage"], "exact")
                    self.assertIn("pending", right["independent_review"])
                    for key in ("correctness_proof", "correctness_command", "completeness_file", "completeness_command", "native_query", "observation_plan"):
                        self.assertTrue((ROOT / right[key]).is_file(), (key, right[key]))
        self.assertEqual(set(changed), expected_changes)
        (OUTPUT / "coverage-changes.json").write_text(json.dumps(changed, indent=2) + "\n")

    def test_native_checker_contracts_full_observations_and_reexecution(self):
        candidate = (ROOT / "specs/vec/reused_basic.rs").read_text()
        results = {}
        reports = {}
        snapshots = []
        for phase in ("analyze", "replay"):
            outcome = read_json(COMPLETENESS / f"{phase}.result.json")
            self.assertEqual(outcome["returncode"], 0)
            self.assertFalse(outcome["timed_out"])
            data = read_json(COMPLETENESS / f"{phase}.json")
            results[phase] = data
            self.assertEqual(data["status"], "completed")
            self.assertEqual(data["exit_code"], 0)
            self.assertEqual(data["diagnostics"], [])
            self.assertEqual(data["discovery_coverage"], "source-visible")
            self.assertEqual(data["counts"], {"deterministic": 3})
            names = {f"vec/reused_basic.rs::vec::reused_basic::{name}" for name in CASES}
            self.assertEqual({target["qualified_name"] for target in data["targets"]}, names)
            self.assertEqual(len(data["results"]), 3)
            run_dir = Path(data["run_dir"])
            snapshot = read_json(run_dir / "snapshot.json")["payload"]
            snapshots.append(snapshot)
            self.assertEqual(set(snapshot["files"]), {
                "lib.rs", "vec/borrowed.rs", "vec/owned_conversions.rs",
                "vec/reused_basic.rs", "cow/observation.rs", "cow/conversions.rs",
            })
            for relative in snapshot["files"]:
                self.assertEqual((run_dir / "workspace" / relative).read_bytes(), (ROOT / "specs" / relative).read_bytes())
            for result in data["results"]:
                name = result["target"]["name"]
                case = CASES[name]
                with self.subTest(phase=phase, api=name):
                    self.assertEqual(result["verdict"], "deterministic")
                    self.assertEqual(result["status"], "completed")
                    self.assertEqual(result["baseline"]["status"], "unsat")
                    self.assertEqual(result["baseline"]["constraints"], [])
                    self.assertIsNone(result["search"])
                    self.assertEqual(result["analysis_kind"], "concrete_determinism")
                    self.assertEqual(len(result["proofs"]), 1)
                    proof = result["proofs"][0]
                    self.assertEqual(proof["status"], "verified")
                    self.assertEqual(proof["verified_goals"], 1)
                    attempt = Path(proof["artifact"])
                    revision = attempt.parents[1] / "revisions/0"
                    native = read_json(revision / "contract.json")["payload"]["native"]
                    spec = native["function_spec"]
                    self.assertEqual(spec["generics_decl"], case["generics"])
                    self.assertEqual(spec["where_decl"], "")
                    self.assertIsNone(spec["trait_name"])
                    self.assertIsNone(spec["self_type"])
                    self.assertEqual(spec["type_defs"], {})
                    self.assertEqual(spec["requires"], [])
                    self.assertEqual(spec["ensures"], [case["ensures"]])
                    self.assertEqual(spec["result_binding"], case["binding"])
                    self.assertEqual(spec["return_type"]["name"], case["return"])
                    self.assertEqual([param["name"] for param in spec["params"]], case["params"])
                    for param in spec["params"]:
                        self.assertTrue(param["is_ref"])
                        self.assertFalse(param["is_mut_ref"])
                        self.assertFalse(param["is_self"])
                        self.assertIsNone(param["destructure_ctor"])
                        self.assertEqual(param["type"]["name"], "Vec<T, A>")
                        self.assertEqual([typ["name"] for typ in param["type"]["type_args"]], ["T", "A"])
                    self.assertEqual(source_function(native["source"], name), source_function(candidate, name))
                    plan = read_json(revision / "observation-plan.json")["payload"]
                    self.assertEqual(plan["policy"], "verus-strict-v1")
                    self.assertEqual(plan["analysis_kind"], "concrete_determinism")
                    self.assertEqual(plan["ignored_dimensions"], ["return.representation_beyond_view"] if name == "default" else [])
                    observations = plan["native"]
                    self.assertEqual(len(observations["comparisons"]), 1)
                    comparison = observations["comparisons"][0]
                    self.assertEqual(comparison["dimension"], "return")
                    self.assertEqual(comparison["expression"], case["comparison"])
                    self.assertEqual(comparison["view_prelude"], [])
                    self.assertEqual(comparison["type"]["name"], case["return"])
                    self.assertEqual(comparison["type"]["kind"], "bool" if name == "is_empty" else "Seq")
                    self.assertEqual(observations["accepted_views"], {})
                    self.assertEqual(observations["source_bound_views"], {})
                    self.assertEqual(observations["diagnostics"], [])
                    self.assertEqual(observations["equal_policy"], {
                        "compare_raw_pointers": True, "custom_body": None, "errs_equivalent": False,
                        "ignore_fields": [], "opaque_ok": False, "opaque_types": [],
                        "rationale": None, "source": "verus-strict-v1",
                    })
                    obligation = read_json(revision / "obligation.json")["payload"]["native"]
                    self.assertEqual(obligation["source_function_spec"], spec)
                    self.assertEqual([schema["guard_name"] for schema in obligation["schemas"]], case["guards"])
                    query = Path(result["baseline"]["artifact"]).read_text()
                    expected_query = "(check-sat-assuming (" + " ".join(f"(not {guard}!)" for guard in case["guards"]) + "))"
                    queries = re.findall(r"^\(check-sat-assuming.*$", query, re.MULTILINE)
                    self.assertEqual(list(map(compact, queries)), [compact(expected_query)])
                    self.assertEqual(set(re.findall(r"\bg_[A-Za-z0-9_]+!", query)), {guard + "!" for guard in case["guards"]})
                    harness = (attempt / "harness.rs").read_text()
                    self.assertEqual(source_function(harness, name), source_function(candidate, name))
                    self.assertIn(compact(case["comparison"]), compact(harness))
                    self.assertEqual(len(proof["native"]["invocations"]), 1)
                    invocation = proof["native"]["invocations"][0]
                    self.assertEqual(invocation["role"], "determinism")
                    self.assertEqual(invocation["module"], "vec::reused_basic")
                    self.assertEqual(invocation["status"], "verified")
                    self.assertEqual(invocation["verified_goals"], 1)
                    process = invocation["process"]
                    self.assertEqual(process["returncode"], 0)
                    self.assertFalse(process["timed_out"])
                    self.assertIn("verification results:: 1 verified, 0 errors", process["stdout"])
                    self.assertEqual(
                        process["command"][-4:],
                        ["--verify-only-module", "vec::reused_basic", "--verify-function", invocation["function"]],
                    )
                    self.assertTrue(invocation["function"].startswith("__specdet_"))
                    self.assertEqual((Path(invocation["artifact"]) / "stdout.txt").read_text(), process["stdout"])
                    reports[f"{phase}/{name}"] = {
                        "function_spec": spec, "comparison": comparison,
                        "query_assumptions": expected_query, "verified_goals": proof["verified_goals"],
                        "harness": str(attempt / "harness.rs"), "query": result["baseline"]["artifact"],
                    }
        self.assertNotEqual(results["analyze"]["run_id"], results["replay"]["run_id"])
        self.assertEqual(snapshots[0]["files"], snapshots[1]["files"])
        self.assertEqual(snapshots[0]["snapshot_digest"], snapshots[1]["snapshot_digest"])
        for left, right in zip(results["analyze"]["results"], results["replay"]["results"]):
            self.assertEqual(left["target"], right["target"])
            self.assertEqual(left["problem_id"], right["problem_id"])
            self.assertEqual(left["proofs"][0]["candidate_id"], right["proofs"][0]["candidate_id"])
        command = read_json(COMPLETENESS / "replay.command.json")
        self.assertIn("--reexecute", command)
        self.assertEqual(command[command.index("--run") + 1], results["analyze"]["run_dir"])
        (OUTPUT / "checker-correspondence.json").write_text(json.dumps(reports, indent=2) + "\n")


if __name__ == "__main__":
    unittest.main()
