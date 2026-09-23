import copy
import csv
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUST = Path("/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library")
VERUS = ROOT / "toolchains/verus-x86-linux"
RUSTC = ROOT / "toolchains/rustup/toolchains/1.98.1-x86_64-unknown-linux-gnu/bin/rustc"
PROOF = Path(os.environ.get(
    "CAPACITY_PROOF_OUTPUT", ROOT / "proofs/correctness/vec/with-capacity/isolation/candidate",
)).resolve()
COMPLETENESS = Path(os.environ.get(
    "CAPACITY_COMPLETENESS_OUTPUT", ROOT / "proofs/completeness/vec/with-capacity/isolation/checker",
)).resolve()
OUTPUT = Path(os.environ.get(
    "CAPACITY_TEST_OUTPUT", ROOT / "tests/with-capacity/isolation/api",
)).resolve()
BEFORE = ROOT / "tests/with-capacity/engineer"
API = "alloc::vec::Vec<T>::with_capacity"
TARGET = "vec/with_capacity.rs::vec::with_capacity::with_capacity"


def compact(text):
    return re.sub(r"\s+", "", text).replace(",)", ")")


def source_function(text):
    contract, body = compact(text).split("pubconstfnwith_capacity<T>", 1)[1].split("{", 1)
    return contract, body.split("}", 1)[0]


def read_json(path):
    return json.loads(path.read_text())


def run(name, arguments, bootstrap="1"):
    command = [
        "bash", str(ROOT / "scripts/with_baseline.sh"), "env",
        f"TMPDIR={OUTPUT / 'tmp'}", f"RUSTC_BOOTSTRAP={bootstrap}", *map(str, arguments),
    ]
    with (OUTPUT / f"{name}.command.json").open("x") as stream:
        stream.write(json.dumps(command, indent=2) + "\n")
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


class WithCapacityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        OUTPUT.mkdir(parents=True, exist_ok=False)
        (OUTPUT / "tmp").mkdir()
        shutil.copytree(ROOT / "specs", OUTPUT / "sources")
        cls.rust_links = [
            "--extern", f"vstd={VERUS / 'libvstd.rlib'}",
            "-L", f"dependency={VERUS}", "-L", f"dependency={VERUS / 'deps'}",
        ]
        cls.library = OUTPUT / "libsource_with_capacity.rlib"
        entry = ROOT / "proofs/correctness/vec/with_capacity.rs"
        shutil.copyfile(entry, OUTPUT / "source-entry.rs")
        result = run("native-source-build", [
            RUSTC, entry, "--edition=2021", "--crate-type=lib",
            "--crate-name", "source_with_capacity", *cls.rust_links, "-o", cls.library,
        ])
        if result.returncode != 0:
            raise AssertionError("Native source compilation failed:\n" + result.stderr)
        record = read_json(OUTPUT / "native-source-build.result.json")
        if not record["started_ns"] <= cls.library.stat().st_mtime_ns <= record["finished_ns"]:
            raise AssertionError("The native library was not produced by this compilation")
        cls.links = [*cls.rust_links, "--extern", f"source_with_capacity={cls.library}"]
        (OUTPUT / "linked-inputs.json").write_text(json.dumps({
            "compiler": str(RUSTC),
            "source_entry": str(entry),
            "library": str(cls.library),
            "build_record": str(OUTPUT / "native-source-build.result.json"),
            "formal_verification": False,
        }, indent=2) + "\n")

    def probe(self, name, source, bootstrap="1", extra=()):
        path = OUTPUT / f"{name}.rs"
        path.write_text(source)
        (OUTPUT / f"{name}.input.json").write_text(json.dumps({"source": source}, indent=2) + "\n")
        try:
            return run(name, [
                RUSTC, "--edition=2021", "--crate-type=lib", "--crate-name", "capacity_probe",
                "--emit=metadata", path, *self.links, *extra, "-o", OUTPUT / f"{name}.rmeta",
            ], bootstrap)
        finally:
            path.unlink()

    def test_official_contract_and_original_expression(self):
        candidate = (ROOT / "specs/vec/with_capacity.rs").read_text()
        official = (ROOT / "toolchains/upstream/source/vstd/std_specs/vec.rs").read_text()
        prefix = compact("pub assume_specification<T>[ Vec::<T>::with_capacity ]")
        contract = compact(official).split(prefix, 1)[1].split(";", 1)[0]
        signature, body = source_function(candidate)
        self.assertEqual(signature, contract)
        self.assertEqual(body, compact("Vec::<T>::with_capacity_in(capacity, Global)"))
        self.assertEqual(re.findall(r"pub\s+(?:const\s+)?fn\s+(\w+)", candidate), ["with_capacity"])
        self.assertNotRegex(candidate, r"\b(assume_specification|assume|admit|external_body|unsafe|requires)\b")
        self.assertTrue(candidate.startswith("#![cfg(not(no_global_oom_handling))]\n"))
        dependency = compact("""
            pub assume_specification<T, A: Allocator>[ Vec::<T, A>::with_capacity_in ]
            (capacity: usize, alloc: A) -> (v: Vec<T, A>)
                ensures v@ == Seq::<T>::empty(),;
        """)
        self.assertIn(dependency, compact(official))
        original = (RUST / "alloc/src/vec/mod.rs").read_text().splitlines()
        span = "\n".join(original[466:525])
        self.assertEqual(original[446], "impl<T> Vec<T> {")
        self.assertIn(compact("""
            pub const fn with_capacity(capacity: usize) -> Self {
                Self::with_capacity_in(capacity, Global)
            }
        """), compact(span))
        self.assertIn("#[cfg(not(no_global_oom_handling))]", span)
        self.assertIn('#[rustc_const_unstable(feature = "const_heap", issue = "79597")]', span)
        self.assertIn("at least the specified capacity", span)
        self.assertIn("more elements than", span)
        self.assertIn("`isize::MAX` _bytes_", span)
        self.assertIn("capacity will always be `usize::MAX`", span)
        (OUTPUT / "correspondence.json").write_text(json.dumps({
            "canonical_api": API,
            "rust_source": f"{RUST}/alloc/src/vec/mod.rs:447,467-525",
            "official_declaration": prefix + contract + ";",
            "source_signature": "pubconstfnwith_capacity<T>" + signature,
            "body": body,
            "official_dependency": dependency,
            "checker_target": TARGET,
            "normal_return_observation": "complete Vec sequence, not capacity or allocation",
        }, indent=2) + "\n")

    def test_source_and_candidate_verus_compilation(self):
        for name, crate, module in (
            ("source", "source_with_capacity", "with_capacity_source"),
            ("candidate", "with_capacity_candidate", "vec::with_capacity"),
        ):
            with self.subTest(entry=name):
                record = read_json(PROOF / f"{name}.result.json")
                command = read_json(PROOF / f"{name}.command.json")
                self.assertIn("--compile", command)
                self.assertEqual(command[-4:], [
                    "--verify-only-module", module, "--verify-function", "with_capacity",
                ])
                self.assertEqual(record["returncode"], 0, (PROOF / f"{name}.stderr").read_text())
                self.assertFalse(record["timed_out"])
                self.assertIn("verification results:: 1 verified, 0 errors",
                              (PROOF / f"{name}.stdout").read_text())
                library = PROOF / "build" / f"lib{crate}.rlib"
                self.assertLessEqual(record["started_ns"], library.stat().st_mtime_ns)
                self.assertLessEqual(library.stat().st_mtime_ns, record["finished_ns"])

    def test_lowered_source_calls_only_official_dependency(self):
        for relative in ("lib.rs", "with_capacity_candidate.rs", "vec/with_capacity.rs"):
            self.assertEqual((PROOF / "sources" / relative).read_bytes(),
                             (ROOT / "specs" / relative).read_bytes())
        for name, crate, module in (
            ("source", "source_with_capacity", "with_capacity_source"),
            ("candidate", "with_capacity_candidate", "vec::with_capacity"),
        ):
            entry = ROOT / (
                "proofs/correctness/vec/with_capacity.rs" if name == "source"
                else "specs/with_capacity_candidate.rs"
            )
            self.assertEqual((PROOF / f"{name}.source.rs").read_bytes(), entry.read_bytes())
            vir = (PROOF / name / "crate.vir").read_text()
            start = vir.index(f":name (Fun :path {crate}::{module}::with_capacity)")
            section = vir[start:vir.index(":extra_dependencies", start)]
            normalized = compact(section)
            self.assertIn(":require()", normalized)
            self.assertIn(":is_external_bodyfalse", normalized)
            parameters = normalized.split(":params(", 1)[1].split(":ret", 1)[0]
            self.assertEqual(parameters.count("(Param:name"), 1)
            self.assertIn('(VarIdent"capacity"', parameters)
            self.assertIn("(TypInt(IntRangeUSize))", parameters)
            bounds = normalized.split(":typ_bounds(", 1)[1].split(":params(", 1)[0]
            self.assertEqual(bounds.count("(GenericBound"), 1)
            self.assertIn("(SizednessSized)", bounds)
            body = re.split(r"\)\s+:body\s+\(@@", section, maxsplit=1)[1]
            calls = re.findall(r"\(Fun:path(alloc::vec::[^)]+)\)", compact(body))
            self.assertEqual(len(calls), 1)
            self.assertTrue(calls[0].endswith("::with_capacity_in"), calls)
            self.assertIn(compact('(> Ctor (Dt Path alloc::alloc::Global) "Global" () None)'), compact(body))
            self.assertIn(compact('(Place Local (VarIdent "capacity"'), compact(body))
            (OUTPUT / f"{name}.lowered-body.txt").write_text(body)

    def test_native_aggregate_compiles_current_sources(self):
        result = run("native-aggregate-build", [
            RUSTC, ROOT / "specs/lib.rs", "--edition=2021", "--crate-type=lib",
            "--crate-name", "native_vec_specs", *self.rust_links,
            "-o", OUTPUT / "libnative_vec_specs.rlib",
        ])
        self.assertEqual(result.returncode, 0, result.stderr)
        for path in (ROOT / "specs").rglob("*.rs"):
            self.assertEqual(path.read_bytes(), (OUTPUT / "sources" / path.relative_to(ROOT / "specs")).read_bytes())

    def test_native_behavior_with_fresh_library_and_executable(self):
        source = ROOT / "tests/with_capacity_behavior.rs"
        shutil.copyfile(source, OUTPUT / "native.source.rs")
        result = run("native-build", [
            RUSTC, "--edition=2021", "--test", source, *self.links, "-o", OUTPUT / "native-tests",
        ], bootstrap="0")
        self.assertEqual(result.returncode, 0, result.stderr)
        build = read_json(OUTPUT / "native-build.result.json")
        binary_time = (OUTPUT / "native-tests").stat().st_mtime_ns
        self.assertLessEqual(build["started_ns"], binary_time)
        self.assertLessEqual(binary_time, build["finished_ns"])
        result = run("native-tests", [OUTPUT / "native-tests", "--test-threads=1"], bootstrap="0")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("5 passed; 0 failed", result.stdout)
        execution = read_json(OUTPUT / "native-tests.result.json")
        self.assertGreaterEqual(execution["started_ns"], build["finished_ns"])

    def test_official_and_source_contract_clients(self):
        source = ROOT / "tests/with_capacity_clients.rs"
        shutil.copyfile(source, OUTPUT / "clients.source.rs")
        result = run("clients", [
            VERUS / "verus", source, "--edition=2021", "--crate-type=lib",
            "--crate-name", "capacity_clients", "--compile", "--num-threads=1",
            "--verify-root", "--log-all", "--log-dir", OUTPUT / "clients",
            "-o", OUTPUT / "libcapacity_clients.rlib",
        ])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("verification results:: 2 verified, 0 errors", result.stdout)

    def test_const_heap_enabled_on_actual_api_and_source(self):
        result = self.probe("const-heap-enabled", """
            #![feature(const_heap, const_trait_impl)]
            struct Zst;
            static EMPTY: Vec<u16> = Vec::with_capacity(0);
            static SOURCE_EMPTY: Vec<u16> = source_with_capacity::with_capacity(0);
            static ZST: Vec<Zst> = Vec::with_capacity(usize::MAX);
            static SOURCE_ZST: Vec<Zst> = source_with_capacity::with_capacity(usize::MAX);
            const _: () = assert!(EMPTY.len() == 0 && EMPTY.capacity() == 0);
            const _: () = assert!(SOURCE_EMPTY.len() == 0 && SOURCE_EMPTY.capacity() == 0);
            const _: () = assert!(ZST.len() == 0 && ZST.capacity() == usize::MAX);
            const _: () = assert!(SOURCE_ZST.len() == 0 && SOURCE_ZST.capacity() == usize::MAX);
            pub const fn arbitrary<T>(capacity: usize) -> Vec<T> {
                Vec::<T>::with_capacity(capacity)
            }
        """)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_actual_const_api_is_not_stable(self):
        result = self.probe("stable-const-rejected", """
            static EMPTY: Vec<u8> = Vec::with_capacity(0);
        """, bootstrap="0")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("const", result.stderr)
        self.assertIn("with_capacity", result.stderr)
        self.assertRegex(result.stderr, r"not yet stable as a const|cannot call conditionally-const")

    def test_source_body_requires_const_heap_to_compile(self):
        result = self.probe("source-const-feature-required", f"""
            #![feature(allocator_api, const_trait_impl)]
            #[path = "{ROOT / 'specs/vec/with_capacity.rs'}"]
            pub mod original;
        """)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("with_capacity_in", result.stderr)
        self.assertIn("const_heap", result.stderr)

    def test_disabled_global_oom_configuration_removes_entry(self):
        library = OUTPUT / "libsource_without_oom.rlib"
        result = run("cfg-disabled-build", [
            RUSTC, ROOT / "proofs/correctness/vec/with_capacity.rs",
            "--edition=2021", "--crate-type=lib", "--crate-name", "source_without_oom",
            "--cfg", "no_global_oom_handling", *self.rust_links, "-o", library,
        ])
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.probe("cfg-disabled-entry-rejected", """
            pub fn absent() -> Vec<u8> { source_without_oom::with_capacity(0) }
        """, extra=["--extern", f"source_without_oom={library}"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error[E0425]", result.stderr)
        self.assertIn("with_capacity", result.stderr)

    def test_exact_type_and_element_lifetime_rejections(self):
        for name, target in (("official", "Vec::<i32>::with_capacity"),
                             ("source", "source_with_capacity::with_capacity::<i32>")):
            for suffix, declaration in (
                ("capacity-type", f"fn f() {{ let _: fn(i32) -> Vec<i32> = {target}; }}"),
                ("return-type", f"fn f() {{ let _: fn(usize) -> [i32; 0] = {target}; }}"),
                ("allocator-type", f"""
                    #![feature(allocator_api)]
                    fn f() {{ let _: fn(usize) -> Vec<i32, std::alloc::System> = {target}; }}
                """),
            ):
                with self.subTest(api=name, probe=suffix):
                    result = self.probe(f"{name}-{suffix}", declaration)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(set(re.findall(r"^error\[(E\d+)\]", result.stderr, re.MULTILINE)),
                                     {"E0308"}, result.stderr)
            construct = "Vec::with_capacity" if name == "official" else "source_with_capacity::with_capacity"
            result = self.probe(f"{name}-element-escape", f"""
                fn f<'a>() -> Vec<&'a i32> {{
                    let local = 17;
                    let mut vec = {construct}(1);
                    vec.push(&local);
                    vec
                }}
            """)
            self.assertNotEqual(result.returncode, 0)
            self.assertRegex(result.stderr, r"error\[(E0515|E0597)\]")

    def test_minimal_global_constructor_diagnostic(self):
        source = ROOT / "proofs/correctness/vec/with-capacity/global_constructor.rs"
        shutil.copyfile(source, OUTPUT / "global-constructor.source.rs")
        result = run("global-constructor-verus", [
            VERUS / "verus", source, "--edition=2021", "--crate-type=lib",
            "--crate-name", "global_constructor", "--compile", "--num-threads=1",
            "--log-all", "--log-dir", OUTPUT / "global-constructor",
            "-o", OUTPUT / "libglobal_constructor.rlib",
        ])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("disallowed: constructor for an opaque datatype", result.stderr)
        self.assertIn("external_body", result.stderr)
        result = run("global-constructor-rustc", [
            RUSTC, source, "--edition=2021", "--crate-type=lib", "--crate-name", "native_global",
            *self.rust_links, "-o", OUTPUT / "libnative_global.rlib",
        ])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_checker_contract_observation_and_reexecution_records(self):
        phases = {}
        reports = {}
        candidate = (ROOT / "specs/vec/with_capacity.rs").read_text()
        expected_return = {
            "kind": "Seq", "name": "Vec<T>",
            "spec_view": {
                "kind": "Seq", "name": "Seq<T>",
                "type_args": [{"kind": "unknown", "name": "T"}],
            },
            "type_args": [{"kind": "unknown", "name": "T"}],
        }
        expected_spec = {
            "name": "with_capacity", "generics_decl": "<T>", "where_decl": "",
            "self_type": None, "trait_name": None, "type_defs": {},
            "params": [{
                "name": "capacity", "type": {"kind": "usize", "name": "usize"},
                "is_ref": False, "is_mut_ref": False, "is_self": False,
                "destructure_ctor": None,
            }],
            "return_type": expected_return, "result_binding": "v",
            "requires": [], "ensures": ["v@ == Seq::<T>::empty()"],
        }
        guards = [
            "g_capacity_eq", "g_capacity_rng", "g_r1_leneq", "g_r1_lenrng",
            "g_r2_leneq", "g_r2_lenrng", "g_neq_tuple",
        ]
        for phase in ("analyze", "replay"):
            data = read_json(COMPLETENESS / f"{phase}.json")
            phases[phase] = data
            self.assertEqual(data["discovery_coverage"], "source-visible")
            self.assertEqual(data["diagnostics"], [])
            self.assertEqual([target["qualified_name"] for target in data["targets"]], [TARGET])
            self.assertEqual(len(data["results"]), 1)
            result = data["results"][0]
            self.assertEqual(len(result["proofs"]), 1)
            proof = result["proofs"][0]
            attempt = Path(proof["artifact"])
            revision = attempt.parents[1] / "revisions/0"
            native = read_json(revision / "contract.json")["payload"]["native"]
            self.assertEqual(native["function_spec"], expected_spec)
            self.assertEqual(native["source"], candidate)
            self.assertEqual(native["overlays"], {})
            self.assertEqual(native["accepted_semantics"], [])
            plan = read_json(revision / "observation-plan.json")["payload"]
            self.assertEqual(plan["policy"], "verus-strict-v1")
            self.assertEqual(plan["analysis_kind"], "concrete_determinism")
            self.assertEqual(plan["ignored_dimensions"], ["return.representation_beyond_view"])
            comparison = {
                "dimension": "return", "expression": "(r1)@ =~= (r2)@",
                "type": expected_return, "view_prelude": [],
            }
            self.assertEqual(plan["native"]["comparisons"], [comparison])
            self.assertEqual(plan["native"]["accepted_views"], {})
            self.assertEqual(plan["native"]["source_bound_views"], {})
            self.assertEqual(plan["native"]["equal_policy"], {
                "compare_raw_pointers": True, "custom_body": None, "errs_equivalent": False,
                "ignore_fields": [], "opaque_ok": False, "opaque_types": [],
                "rationale": None, "source": "verus-strict-v1",
            })
            obligation = read_json(revision / "obligation.json")["payload"]["native"]
            self.assertEqual(obligation["source_function_spec"], expected_spec)
            self.assertEqual([schema["guard_name"] for schema in obligation["schemas"]], guards)
            harness = (attempt / "harness.rs").read_text()
            self.assertEqual(source_function(harness), source_function(candidate))
            self.assertIn(compact(comparison["expression"]), compact(harness))
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["verdict"], "inconclusive")
            self.assertIsNone(result["baseline"])
            self.assertEqual(proof["status"], "compile_error")
            self.assertEqual(proof["verified_goals"], 0)
            self.assertEqual(list(attempt.rglob("originalC.smt2")), [])
            self.assertEqual(len(proof["native"]["invocations"]), 1)
            invocation = proof["native"]["invocations"][0]
            process = invocation["process"]
            self.assertEqual(Path(proof["native"]["entrypoint"]).name, "with_capacity_candidate.rs")
            self.assertEqual(process["returncode"], 1)
            self.assertFalse(process["timed_out"])
            self.assertIn("disallowed: constructor for an opaque datatype", process["stderr"])
            self.assertEqual(process["command"][-4:], [
                "--verify-only-module", "vec::with_capacity",
                "--verify-function", invocation["function"],
            ])
            run_dir = Path(data["run_dir"])
            snapshot = read_json(run_dir / "snapshot.json")["payload"]
            self.assertEqual(set(snapshot["files"]), {
                "lib.rs", "with_capacity_candidate.rs", "vec/with_capacity.rs", "vec/reused_basic.rs",
                "vec/owned_conversions.rs", "vec/borrowed.rs",
                "cow/conversions.rs", "cow/observation.rs",
            })
            for relative in snapshot["files"]:
                self.assertEqual((run_dir / "workspace" / relative).read_bytes(),
                                 (ROOT / "specs" / relative).read_bytes())
            reports[phase] = {
                "function_spec": expected_spec, "comparison": comparison,
                "search_guard_schemas": guards, "query_generated": False,
                "proof_status": proof["status"], "verified_goals": proof["verified_goals"],
                "harness": str(attempt / "harness.rs"),
                "observation": str(revision / "observation-plan.json"),
                "source_compile_error": process["stderr"],
            }
        self.assertNotEqual(phases["analyze"]["run_id"], phases["replay"]["run_id"])
        left, right = (phases[phase]["results"][0] for phase in ("analyze", "replay"))
        self.assertEqual(left["target"], right["target"])
        self.assertEqual(left["problem_id"], right["problem_id"])
        self.assertEqual(left["proofs"][0]["candidate_id"], right["proofs"][0]["candidate_id"])
        replay_command = read_json(COMPLETENESS / "replay.command.json")
        self.assertIn("--reexecute", replay_command)
        self.assertEqual(replay_command[replay_command.index("--run") + 1], phases["analyze"]["run_dir"])
        (OUTPUT / "checker-correspondence.json").write_text(json.dumps(reports, indent=2) + "\n")

    def test_completeness_has_nonzero_successful_obligations(self):
        for phase in ("analyze", "replay"):
            with self.subTest(phase=phase):
                data = read_json(COMPLETENESS / f"{phase}.json")
                record = read_json(COMPLETENESS / f"{phase}.result.json")
                self.assertEqual(record["returncode"], 0, f"{phase}: {data['status']}")
                self.assertEqual(data["counts"], {"deterministic": 1})
                proof = data["results"][0]["proofs"][0]
                self.assertEqual(proof["status"], "verified")
                self.assertEqual(proof["verified_goals"], 1)

    def test_config_and_four_row_coverage_scope(self):
        previous = tomllib.loads((BEFORE / "specdet.before.toml").read_text())
        current = tomllib.loads((ROOT / "specdet.toml").read_text())
        self.assertEqual(current, previous)
        private = copy.deepcopy(current)
        private["project"]["root"] = str(ROOT / "specs")
        private["adapters"]["verus"]["executable"] = str(VERUS / "verus")
        private["adapters"]["verus"]["environment"]["TMPDIR"] = str(COMPLETENESS / "tmp")
        private["artifacts"]["output_dir"] = str(COMPLETENESS / "analysis-runs")
        private["build"]["entrypoint"] = "with_capacity_candidate.rs"
        private["targets"]["include"] = ["vec/with_capacity.rs"]
        self.assertEqual(tomllib.loads((COMPLETENESS / "specdet.toml").read_text()), private)
        previous_lib = (BEFORE / "lib.before.rs").read_text()
        self.assertEqual((ROOT / "specs/lib.rs").read_text(), previous_lib)
        with (BEFORE / "coverage-before.tsv").open() as stream:
            before = list(csv.DictReader(stream, delimiter="\t"))
        with (ROOT / "inventory/coverage.tsv").open() as stream:
            after = list(csv.DictReader(stream, delimiter="\t"))
        self.assertEqual(len(before), 138)
        self.assertEqual(len(after), 138)
        reviewed = {
            "<alloc::vec::Vec<T> as core::default::Default>::default",
            "alloc::vec::Vec<T, A>::is_empty",
            "<alloc::vec::Vec<T, A> as core::ops::Deref>::deref",
        }
        changes = {}
        for left, right in zip(before, after):
            self.assertEqual(left["canonical_api"], right["canonical_api"])
            fields = [key for key in left if left[key] != right[key]]
            if fields:
                name = right["canonical_api"]
                changes[name] = fields
                if name in reviewed:
                    self.assertEqual(fields, ["independent_review"])
                    self.assertIn("af05f6b80c5a", right["independent_review"])
                else:
                    self.assertEqual(name, API)
                    self.assertEqual(right["vstd_coverage"], "exact")
                    self.assertIn("pending", right["independent_review"])
                    self.assertTrue((ROOT / right["correctness_proof"]).is_file())
        self.assertEqual(set(changes), reviewed | {API})
        (OUTPUT / "coverage-changes.json").write_text(json.dumps(changes, indent=2) + "\n")


if __name__ == "__main__":
    unittest.main()
