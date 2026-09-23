"""Source correspondence, fresh builds, native behavior, and generic completeness."""

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
SOURCE = ROOT / "specs/vec/index.rs"
PROOF = Path(os.environ.get(
    "INDEX_PROOF_OUTPUT", ROOT / "proofs/correctness/vec/generic-index/caller-preserved-source"
)).resolve()
AGGREGATE = Path(os.environ.get(
    "INDEX_AGGREGATE_OUTPUT", ROOT / "proofs/correctness/vec/generic-index/caller-preserved-aggregate"
)).resolve()
COMPLETENESS = Path(os.environ.get(
    "INDEX_COMPLETENESS_OUTPUT", ROOT / "proofs/completeness/vec/generic-index/caller-preserved"
)).resolve()
OUTPUT = Path(os.environ.get("INDEX_TEST_OUTPUT", ROOT / "tests/vec-index/engineer")).resolve()
VERUS = ROOT / "toolchains/verus-x86-linux/verus"
RUSTC = ROOT / "toolchains/rustup/toolchains/1.98.1-x86_64-unknown-linux-gnu/bin/rustc"
OFFICIAL = ROOT / "toolchains/upstream/source/vstd"
RUST_SOURCE = Path(json.loads((ROOT / "inventory/source_api.json").read_text())["source_library"])
API = "<alloc::vec::Vec<T, A> as core::ops::Index<I>>::index"
TARGET = "vec/index.rs::vec::index::index_source"


def read_json(path):
    return json.loads(path.read_text())


def compact(text):
    return re.sub(r"\s+", "", text)


class VecIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        OUTPUT.mkdir(parents=True, exist_ok=False)
        (OUTPUT / "tmp").mkdir()
        cls.links = [
            "-L", f"dependency={PROOF}", "-L", f"dependency={AGGREGATE}",
            "-L", f"dependency={ROOT / 'toolchains/verus-x86-linux'}",
            "-L", f"dependency={ROOT / 'toolchains/verus-x86-linux/deps'}",
            "--extern", f"vec_index_source={PROOF / 'libvec_index_source.rlib'}",
            "--extern", f"vec_specs={AGGREGATE / 'libvec_specs.rlib'}",
        ]

    def run_command(self, name, arguments):
        command = [
            "bash", str(ROOT / "scripts/with_baseline.sh"),
            "env", f"TMPDIR={OUTPUT / 'tmp'}",
        ] + [str(argument) for argument in arguments]
        (OUTPUT / f"{name}.command.json").write_text(json.dumps(command, indent=2) + "\n")
        started = time.time_ns()
        try:
            result = subprocess.run(
                command, cwd=ROOT, capture_output=True, text=True, timeout=115
            )
        except subprocess.TimeoutExpired as error:
            for suffix, value in (("stdout", error.stdout), ("stderr", error.stderr)):
                if isinstance(value, bytes):
                    value = value.decode(errors="replace")
                (OUTPUT / f"{name}.{suffix}").write_text(value or "")
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

    def assert_fresh_build(self, directory, crate, count, entry):
        record = read_json(directory / "build.result.json")
        self.assertEqual(record["returncode"], 0)
        self.assertFalse(record["timed_out"])
        library = directory / f"lib{crate}.rlib"
        self.assertLessEqual(record["started_ns"], library.stat().st_mtime_ns)
        self.assertLessEqual(library.stat().st_mtime_ns, record["finished_ns"])
        self.assertEqual((directory / "candidate.rs").read_bytes(), SOURCE.read_bytes())
        self.assertEqual((directory / "entry.rs").read_bytes(), entry.read_bytes())
        command = read_json(directory / "build.command.json")
        self.assertIn("--compile", command)
        self.assertIn("--num-threads=1", command)
        self.assertIn(str(entry), command)
        self.assertFalse(any(arg.startswith("--verify-") for arg in command))
        self.assertIn(
            f"verification results:: {count} verified, 0 errors",
            (directory / "build.stdout").read_text(),
        )

    def test_source_signature_and_inherited_contract(self):
        original = (RUST_SOURCE / "alloc/src/vec/mod.rs").read_text()
        self.assertIn(
            "impl<T, I: SliceIndex<[T]>, A: Allocator> Index<I> for Vec<T, A> {\n"
            "    type Output = I::Output;\n\n"
            "    #[inline]\n"
            "    fn index(&self, index: I) -> &Self::Output {\n"
            "        Index::index(&**self, index)\n"
            "    }\n}",
            original,
        )
        candidate = compact(SOURCE.read_text())
        self.assertIn("#[inline]#[track_caller]pubfnindex_source", candidate)
        trait = compact((RUST_SOURCE / "core/src/ops/index.rs").read_text())
        self.assertIn(
            "#[track_caller]fnindex(&self,index:Idx)->&Self::Output;", trait
        )
        self.assertIn(
            "pubfnindex_source<T,I:SliceIndex<[T]>,A:Allocator>"
            "(vec:&Vec<T,A>,index:I,)->(r:&<Vec<T,A>asIndex<I>>::Output)",
            candidate,
        )
        self.assertIn("requiresvec.index_req(&index),ensures", candidate)
        self.assertIn(
            "exists|s:&[T]|#[trigger]s@==vec@"
            "&&call_ensures(<IasSliceIndex<[T]>>::index,(index,s),r),",
            candidate,
        )
        self.assertTrue(candidate.endswith("{Index::index(&**vec,index)}}"))
        for forbidden in ("assume_specification", "external_body", "admit(", "assume(", "'static"):
            self.assertNotIn(forbidden, candidate)
        core = compact((OFFICIAL / "std_specs/core.rs").read_text())
        vec = compact((OFFICIAL / "std_specs/vec.rs").read_text())
        slices = compact((OFFICIAL / "std_specs/slice.rs").read_text())
        self.assertIn("requiresself.index_req(&index)", core)
        self.assertIn(
            "forall|s:&[T]|#[trigger]s@==self@==>index.in_bounds(s)", vec
        )
        self.assertIn(
            "exists|s:&[T]|#[trigger]s@==vec@"
            "&&call_ensures(<IasSliceIndex<[T]>>::index,(i,s),r)", vec
        )
        self.assertIn("openspecfnindex_req(&self,index:&I)->bool{index.in_bounds(self)}", slices)
        self.assertIn(
            "call_ensures(<IasSliceIndex<[T]>>::index,(index,slice),output)", slices
        )

    def test_fresh_source_and_aggregate_builds(self):
        self.assert_fresh_build(
            PROOF, "vec_index_source", 1, ROOT / "proofs/correctness/vec/index.rs"
        )
        self.assert_fresh_build(AGGREGATE, "vec_specs", 4, ROOT / "specs/lib.rs")
        before = ROOT / "tests/vec-index/before"
        expected = (before / "lib.rs").read_text().replace(
            "#![feature(allocator_api)]", "#![feature(allocator_api, slice_index_methods)]"
        ).replace("    pub mod borrowed;\n", "    pub mod borrowed;\n    pub mod index;\n")
        self.assertEqual((ROOT / "specs/lib.rs").read_text(), expected)
        config = tomllib.loads((ROOT / "specdet.toml").read_text())
        old_config = tomllib.loads((before / "specdet.toml").read_text())
        old_config["targets"]["include"].append("vec/index.rs")
        self.assertEqual(config, old_config)
        self.assertNotIn("with_capacity", expected)
        self.assertNotIn("into_iter", expected)

    def test_source_obligation_uses_deref_and_slice_index(self):
        vir = (PROOF / "logs/crate.vir").read_text()
        function = vir.split(
            ":name (Fun :path vec_index_source::vec_index::index_source)", 1
        )[1].split(":extra_dependencies", 1)[0]
        body = function.split(") :body (@@", 1)[1]
        calls = re.findall(r":resolved \(Fun :path ([^\s)]+)\)", body)
        self.assertEqual(calls, [
            "core::slice::index::impl&%0::index", "alloc::vec::impl&%9::deref"
        ])
        self.assertIn(':trait_path core::slice::index::SliceIndex :name', function)
        self.assertIn('"Output"', function)
        air = (PROOF / "logs/vec_index-final.air").read_text().split(
            ";; Function-Def vec_index_source::vec_index::index_source", 1
        )[1]
        self.assertEqual(air.count("(check-valid"), 1)
        self.assertIn("ens%alloc!vec.impl&%9.deref.", air)
        self.assertIn("ens%core!slice.index.impl&%0.index.", air)
        self.assertNotIn("ens%alloc!vec.impl&%14.index.", air)
        self.assertNotIn("ens%vec_index_source!vec_index.index_source.", air)
        self.assertEqual((PROOF / "logs/vec_index.smt2").read_text().count("(check-sat)"), 1)
        self.assertEqual(
            re.findall(r"^unsat$", (PROOF / "logs/vec_index.smt_transcript").read_text(), re.M),
            ["unsat"],
        )

    def test_original_index_families(self):
        sources = "\n".join(
            (RUST_SOURCE / path).read_text()
            for path in ("core/src/slice/index.rs", "core/src/index.rs")
        )
        implementations = set(re.findall(
            r"unsafe impl<T> (?:const )?SliceIndex<\[T\]> for ([^\n{]+) \{", sources
        ))
        ranges = {
            "ops::Range<usize>", "range::Range<usize>", "ops::RangeTo<usize>",
            "ops::RangeFrom<usize>", "range::RangeFrom<usize>", "ops::RangeFull",
            "ops::RangeInclusive<usize>", "range::RangeInclusive<usize>",
            "ops::RangeToInclusive<usize>", "range::RangeToInclusive<usize>",
        }
        public = {"usize", "Last", "(ops::Bound<usize>, ops::Bound<usize>)"}
        public.update(ranges)
        public.update(f"Clamp<{kind}>" for kind in ranges | {"usize"})
        self.assertEqual(len(public), 24)
        self.assertEqual(implementations, public | {"ops::IndexRange"})
        private = (RUST_SOURCE / "core/src/ops/index_range.rs").read_text()
        self.assertIn("pub(crate) struct IndexRange", private)

    def test_native_source_and_standard_behavior(self):
        executable = OUTPUT / "native-tests"
        compiled = self.run_command("native-compile", [
            RUSTC, "--edition=2021", "--test", ROOT / "tests/vec_index_behavior.rs",
            *self.links, "-o", executable,
        ])
        self.assertEqual(compiled.returncode, 0, compiled.stderr)
        record = read_json(OUTPUT / "native-compile.result.json")
        self.assertLessEqual(record["started_ns"], executable.stat().st_mtime_ns)
        self.assertLessEqual(executable.stat().st_mtime_ns, record["finished_ns"])
        result = self.run_command("native-run", [executable, "--test-threads=1"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("8 passed; 0 failed", result.stdout)

    def test_generic_and_complete_content_clients(self):
        logs = OUTPUT / "clients"
        logs.mkdir()
        library = OUTPUT / "libvec_index_clients.rlib"
        result = self.run_command("clients", [
            VERUS, ROOT / "tests/vec_index_clients.rs", "--edition=2021",
            "--crate-type=lib", "--crate-name", "vec_index_clients", "--compile",
            "--num-threads=1", "--verify-root", "--log-all", "--log-dir", logs,
            "-o", library,
        ])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("verification results:: 8 verified, 0 errors", result.stdout)
        record = read_json(OUTPUT / "clients.result.json")
        self.assertLessEqual(record["started_ns"], library.stat().st_mtime_ns)
        self.assertLessEqual(library.stat().st_mtime_ns, record["finished_ns"])

    def test_exact_return_and_receiver_lifetime_rejections(self):
        cases = {
            "element_as_slice": ("E0308", "pub fn bad(v: &Vec<String>) -> &[String] { CALL(v, 0usize) }"),
            "slice_as_element": ("E0308", "pub fn bad(v: &Vec<String>) -> &String { CALL(v, 0..1) }"),
            "mutable_return": ("E0308", "pub fn bad(v: &Vec<String>) -> &mut String { CALL(v, 0usize) }"),
            "owned_return": ("E0308", "pub fn bad(v: &Vec<String>) -> String { CALL(v, 0usize) }"),
            "element_escape": ("E0515", "pub fn bad<'a>() -> &'a String { let v = vec![String::from(\"x\")]; CALL(&v, 0usize) }"),
            "slice_escape": ("E0515", "pub fn bad<'a>() -> &'a [String] { let v = vec![String::from(\"x\")]; CALL(&v, 0..1) }"),
            "element_mutation": ("E0502", "pub fn bad() -> usize { let mut v = vec![String::from(\"x\")]; let r = CALL(&v, 0usize); v.clear(); r.len() }"),
            "slice_mutation": ("E0502", "pub fn bad() -> usize { let mut v = vec![String::from(\"x\")]; let r = CALL(&v, 0..1); v.clear(); r.len() }"),
        }
        for origin, call in (
            ("source", "vec_index_source::index_source"),
            ("aggregate", "vec_specs::vec::index::index_source"),
            ("standard", "std::ops::Index::index"),
        ):
            for case, (expected, body) in cases.items():
                with self.subTest(origin=origin, case=case):
                    name = f"probe-{origin}-{case}"
                    source = OUTPUT / f"{name}.rs"
                    text = body.replace("CALL", call) + "\n"
                    source.write_text(text)
                    (OUTPUT / f"{name}.input.json").write_text(json.dumps({
                        "source": text, "expected_error": expected,
                    }, indent=2) + "\n")
                    try:
                        result = self.run_command(name, [
                            RUSTC, "--edition=2021", "--crate-type=lib",
                            "--crate-name", "index_probe", "--emit=metadata", source,
                            *self.links, "-o", OUTPUT / f"{name}.rmeta",
                        ])
                    finally:
                        source.unlink()
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(set(re.findall(r"^error\[(E\d+)\]", result.stderr, re.M)), {expected})
                    self.assertFalse(source.exists())

    def test_checker_inputs_and_selected_reexecution(self):
        reports = [read_json(COMPLETENESS / f"{name}.stdout") for name in ("analyze", "replay-selected")]
        self.assertNotEqual(reports[0]["run_id"], reports[1]["run_id"])
        current = SOURCE.read_text()
        for report in reports:
            self.assertEqual([target["qualified_name"] for target in report["targets"]], [TARGET])
            self.assertEqual(len(report["results"]), 1)
            run = Path(report["run_dir"])
            effective = read_json(run / "effective-config.json")["payload"]
            self.assertEqual(effective["selectors"], ["vec/index.rs"])
            self.assertEqual(effective["observation_policy"], "verus-strict-v1")
            self.assertEqual((run / "workspace/vec/index.rs").read_text(), current)
            contracts = list((run / "targets").glob("*/revisions/0/contract.json"))
            self.assertEqual(len(contracts), 1)
            native = read_json(contracts[0])["payload"]["native"]
            self.assertEqual(native["source"], current)
            spec = native["function_spec"]
            self.assertEqual(spec["generics_decl"], "<T, I: SliceIndex<[T]>, A: Allocator>")
            self.assertEqual(spec["where_decl"], "")
            self.assertEqual(spec["params"][0]["name"], "vec")
            self.assertEqual(spec["params"][0]["type"]["name"], "Vec<T, A>")
            self.assertTrue(spec["params"][0]["is_ref"])
            self.assertEqual(spec["params"][1]["name"], "index")
            self.assertEqual(spec["params"][1]["type"]["name"], "I")
            self.assertFalse(spec["params"][1]["is_ref"])
            self.assertEqual(spec["return_type"]["name"], "&<Vec<T, A> as Index<I>>::Output")
            self.assertEqual(spec["requires"], ["vec.index_req(&index)"])
            self.assertEqual([compact(clause) for clause in spec["ensures"]], [
                "exists|s:&[T]|#[trigger]s@==vec@"
                "&&call_ensures(<IasSliceIndex<[T]>>::index,(index,s),r)"
            ])
            self.assertEqual(native["overlays"], {})
            self.assertEqual(native["transformations"], [])
            self.assertEqual(native["accepted_semantics"], [])
            for dependency in native["type_sources"]:
                self.assertEqual(
                    dependency["source"], (ROOT / "specs" / dependency["file"]).read_text()
                )
        command = read_json(COMPLETENESS / "replay-selected.command.json")
        self.assertIn("--reexecute", command)
        self.assertNotIn("--config", command)
        self.assertEqual(command[command.index("--run") + 1], reports[0]["run_dir"])

    def test_full_generic_completeness(self):
        for name in ("analyze", "replay-selected"):
            with self.subTest(phase=name):
                result = read_json(COMPLETENESS / f"{name}.result.json")
                report = read_json(COMPLETENESS / f"{name}.stdout")
                self.assertEqual(result["returncode"], 0, report["results"][0]["diagnostics"])
                self.assertEqual(report["counts"], {"deterministic": 1})
                proofs = report["results"][0]["proofs"]
                self.assertTrue(proofs, "No completeness proof was generated")
                for proof in proofs:
                    self.assertEqual(proof["status"], "verified")
                    self.assertGreater(proof["verified_goals"], 0)
                    self.assertTrue(Path(proof["native"]["harness"]).is_file())
                    for invocation in proof["native"]["invocations"]:
                        self.assertEqual(invocation["process"]["returncode"], 0)
                        self.assertFalse(invocation["process"]["timed_out"])
                self.assertEqual(report["results"][0]["baseline"]["status"], "unsat")
                self.assertTrue(Path(report["results"][0]["baseline"]["artifact"]).is_file())

    def test_only_index_coverage_changes(self):
        def rows(path):
            with path.open(newline="") as file:
                data = list(csv.DictReader(file, delimiter="\t"))
            self.assertEqual(len(data), 138)
            return {row["canonical_api"]: row for row in data}

        before = rows(ROOT / "tests/vec-index/before/coverage.tsv")
        after = rows(ROOT / "inventory/coverage.tsv")
        self.assertEqual(before.keys(), after.keys())
        self.assertNotEqual(before[API], after[API])
        del before[API]
        del after[API]
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
