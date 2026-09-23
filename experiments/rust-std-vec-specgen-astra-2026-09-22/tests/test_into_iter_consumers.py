import csv
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tomllib
import unittest

from test_with_capacity_isolation import run


ROOT = Path(__file__).resolve().parents[1]
VERUS_DIR = ROOT / "toolchains/verus-x86-linux"
VERUS = VERUS_DIR / "verus"
RUSTC = ROOT / "toolchains/rustup/toolchains/1.98.1-x86_64-unknown-linux-gnu/bin/rustc"
PROOFS = ROOT / "proofs/correctness/into_iter"
OUTPUT = Path(os.environ.get(
    "INTO_ITER_OUTPUT_DIR", ROOT / "tests/into-iter-consumers/engineer",
)).resolve()
CHECKER = Path(os.environ.get(
    "INTO_ITER_COMPLETENESS_DIR", OUTPUT / "completeness",
)).resolve()
TARGETS = {
    f"consumers.rs::consumers::<IntoIter<T, A> as core::iter::Iterator>::{name}"
    for name in ("count", "last")
}


def read_json(path):
    return json.loads(path.read_text())


class IntoIterConsumers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        OUTPUT.mkdir(parents=True, exist_ok=False)
        (OUTPUT / "tmp").mkdir()
        cls.records = {}
        for name in ("bindings", "count", "last"):
            variable = f"INTO_ITER_{name.upper()}_RECORD"
            if variable in os.environ:
                cls.records[name] = Path(os.environ[variable]).resolve()
            else:
                cls.records[name] = OUTPUT / "correctness" / name
                run(OUTPUT, f"build-{name}", [
                    sys.executable, str(PROOFS / "build.py"),
                    str(cls.records[name]), name,
                ])
        cls.count_library = cls.records["count"] / "build/libinto_iter_count.rlib"
        cls.native_library = OUTPUT / "libinto_iter_last_native.rlib"
        cls.links = [
            "-L", f"dependency={VERUS_DIR}",
            "-L", f"dependency={VERUS_DIR / 'deps'}",
            "--extern", f"into_iter_count={cls.count_library}",
            "--extern", f"into_iter_last_native={cls.native_library}",
        ]
        shutil.copyfile(PROOFS / "source_last.rs", OUTPUT / "native-last.source.rs")
        cls.native_build = run(OUTPUT, "native-last", [
            str(RUSTC), str(PROOFS / "last.rs"), "--edition=2021", "--crate-type=lib",
            "--crate-name", "into_iter_last_native",
            "--extern", f"vstd={VERUS_DIR / 'libvstd.rlib'}",
            "-L", f"dependency={VERUS_DIR}", "-L", f"dependency={VERUS_DIR / 'deps'}",
            "-o", str(cls.native_library),
        ])
        (OUTPUT / "native-scope.json").write_text(json.dumps({
            "count": {"compiler": "Verus --compile", "library": str(cls.count_library),
                      "record": str(cls.records["count"])},
            "last": {"compiler": "rustc only; supplemental original-body execution",
                     "library": str(cls.native_library),
                     "not_a_Verus_source_proof": True},
        }, indent=2) + "\n")
        if "INTO_ITER_COMPLETENESS_DIR" not in os.environ:
            run(OUTPUT, "completeness", [
                sys.executable, str(ROOT / "proofs/completeness/into_iter/check.py"),
                str(CHECKER),
            ], timeout=780)

    def successful_source(self, name):
        record = self.records[name]
        receipt = read_json(record / f"{name}.result.json")
        self.assertEqual(receipt["returncode"], 0, (record / f"{name}.stderr").read_text())
        self.assertFalse(receipt["timed_out"])
        expected = 0 if name == "bindings" else 1
        self.assertIn(
            f"verification results:: {expected} verified, 0 errors",
            (record / f"{name}.stdout").read_text(),
        )
        library = record / "build" / f"libinto_iter_{name}.rlib"
        self.assertTrue(receipt["started_ns"] <= library.stat().st_mtime_ns <= receipt["finished_ns"])
        return record

    def test_count_source(self):
        record = self.successful_source("count")
        self.assertEqual((record / "source.rs").read_bytes(), (PROOFS / "source.rs").read_bytes())
        self.assertEqual((record / "count.source.rs").read_bytes(), (PROOFS / "count.rs").read_bytes())
        vir = (record / "count/crate.vir").read_text()
        section = vir.split(":name (Fun :path into_iter_count::source::impl&%0::count)", 1)[1]
        section = section.split("\n(group_id", 1)[0]
        body = section.split(":is_external_body false", 1)[1].split(" :body ", 1)[1]
        self.assertIn("ExactSizeIterator::len", body)
        self.assertNotRegex(body, r"\(Fun :path [^)]*::count\)")
        self.assertIn(':typ_params (\n   "T"\n   "A"', section)
        self.assertIn(":require ()", section)

    def test_last_source(self):
        record = self.successful_source("last")
        self.assertEqual(
            (record / "source_last.rs").read_bytes(), (PROOFS / "source_last.rs").read_bytes(),
        )

    def test_real_standard_library_bindings(self):
        record = self.successful_source("bindings")
        self.assertEqual(
            (record / "consumers.source.rs").read_bytes(),
            (PROOFS / "isolated/consumers.rs").read_bytes(),
        )

    def test_source_signatures_and_contracts(self):
        binding = (PROOFS / "isolated/consumers.rs").read_text()
        self.assertEqual(binding.count("pub assume_specification<T, A: Allocator>["), 2)
        self.assertNotIn("requires", binding)
        self.assertNotIn("into_iter_elts", binding)
        self.assertNotIn("external_trait_extension", binding)
        methods = (PROOFS / "isolated/iterator_methods.rs").read_text()
        self.assertEqual(re.findall(r"\bfn\s+(\w+)", methods), ["count", "last"])
        self.assertNotIn("external_trait_extension", methods)
        self.assertNotRegex(methods, r"\b(requires|ensures)\b")
        self.assertIn("result == IteratorSpec::remaining(&iter).len()", binding)
        self.assertIn("Some(IteratorSpec::remaining(&iter).last())", binding)
        for name, file, signature, expression in (
            ("count", "source.rs", "fn count(self) -> usize", "self.len()"),
            ("last", "source_last.rs", "fn last(mut self) -> Option<T>", "self.next_back()"),
        ):
            source = (PROOFS / file).read_text()
            self.assertIn("impl<T, A: Allocator> Iterator for IntoIter<T, A>", source)
            self.assertIn("type Item = T;", source)
            self.assertIn(signature, source)
            self.assertIn(expression, source)
            self.assertNotIn("assume_specification", source)
            self.assertNotIn("external_body", source)
            self.assertNotIn("no_unwind", source)
            self.assertNotRegex(source, r"\b(Clone|Copy|View|Eq|Default)\b")

    def test_generic_remaining_clients(self):
        source = ROOT / "tests/into_iter_consumers_clients.rs"
        shutil.copyfile(source, OUTPUT / "clients.source.rs")
        result = run(OUTPUT, "clients", [
            str(VERUS), str(source), "--edition=2021", "--crate-type=lib",
            "--crate-name", "into_iter_consumers_clients", "--compile", "--verify-root",
            "--num-threads=1", "--log-all", "--log-dir", str(OUTPUT / "clients"),
            "-o", str(OUTPUT / "libinto_iter_consumers_clients.rlib"),
        ])
        self.assertEqual(result.returncode, 0, (OUTPUT / "clients.stderr").read_text())
        self.assertIn("8 verified, 0 errors", (OUTPUT / "clients.stdout").read_text())

    def test_original_body_runtime_supplement(self):
        self.assertEqual(self.native_build.returncode, 0, (OUTPUT / "native-last.stderr").read_text())
        source = ROOT / "tests/into_iter_consumers.rs"
        shutil.copyfile(source, OUTPUT / "runtime.source.rs")
        binary = OUTPUT / "original-body-runtime"
        result = run(OUTPUT, "runtime-build", [
            str(RUSTC), str(source), "--edition=2021", "--test", *self.links,
            "-o", str(binary),
        ])
        self.assertEqual(result.returncode, 0, (OUTPUT / "runtime-build.stderr").read_text())
        result = run(OUTPUT, "runtime", [str(binary), "--test-threads=1"])
        self.assertEqual(result.returncode, 0, (OUTPUT / "runtime.stdout").read_text())
        self.assertIn("6 passed; 0 failed", (OUTPUT / "runtime.stdout").read_text())

    def test_move_result_and_lifetime_rejections(self):
        self.assertEqual(self.native_build.returncode, 0, (OUTPUT / "native-last.stderr").read_text())
        prelude = (
            "#![feature(allocator_api)]\n"
            "extern crate into_iter_count;\nextern crate into_iter_last_native;\n"
            "use std::vec::IntoIter;\n"
        )
        calls = {
            "count-std": "<IntoIter<i32> as Iterator>::count",
            "count-source": "<IntoIter<i32> as into_iter_count::source::Iterator>::count",
            "last-std": "<IntoIter<i32> as Iterator>::last",
            "last-source": "<IntoIter<i32> as into_iter_last_native::source::Iterator>::last",
        }
        cases = []
        for name, call in calls.items():
            cases.append((
                f"reuse-{name}",
                f"fn main() {{ let i = vec![1].into_iter(); let _ = {call}(i); let _ = i.len(); }}",
                {"E0382"},
            ))
            wrong = "Option<i32>" if name.startswith("count") else "usize"
            cases.append((
                f"return-{name}",
                f"fn main() {{ let _: {wrong} = {call}(vec![1].into_iter()); }}",
                {"E0308"},
            ))
        for name, call in (
            ("std", "<IntoIter<&i32> as Iterator>::last"),
            ("source", "<IntoIter<&i32> as into_iter_last_native::source::Iterator>::last"),
        ):
            cases.append((
                f"lifetime-{name}",
                f"fn escaped<'a>() -> Option<&'a i32> {{ let x = 1; {call}(vec![&x].into_iter()) }}"
                "\nfn main() {}",
                {"E0515", "E0597"},
            ))
        for name, body, expected in cases:
            with self.subTest(name=name):
                source = OUTPUT / f"{name}.rs"
                source.write_text(prelude + body)
                (OUTPUT / f"{name}.input.json").write_text(json.dumps({
                    "source": source.read_text(), "expected_errors": sorted(expected),
                }, indent=2) + "\n")
                try:
                    result = run(OUTPUT, name, [
                        str(RUSTC), str(source), "--crate-name", name.replace("-", "_"),
                        "--edition=2021", "--emit=metadata", *self.links,
                        "-o", str(OUTPUT / f"{name}.rmeta"),
                    ])
                finally:
                    source.unlink()
                errors = set(re.findall(r"error\[(E\d+)\]", (OUTPUT / f"{name}.stderr").read_text()))
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(errors and errors <= expected, errors)

    def test_native_analyze_and_reexecute(self):
        for name in ("analyze", "replay"):
            with self.subTest(name=name):
                summary = read_json(CHECKER / f"{name}.json")
                receipt = read_json(CHECKER / f"{name}.result.json")
                self.assertEqual(
                    {target["qualified_name"] for target in summary["targets"]}, TARGETS,
                )
                self.assertEqual(receipt["returncode"], 0, summary["counts"])
                self.assertEqual(summary["counts"], {"deterministic": 2})
                self.assertEqual(len(summary["results"]), 2)
                for result in summary["results"]:
                    self.assertEqual(result["baseline"]["status"], "unsat")
                    self.assertEqual(result["baseline"]["constraints"], [])
                    self.assertIsNone(result["search"])
                    self.assertTrue(any(
                        proof["status"] == "verified" and proof["verified_goals"] > 0
                        for proof in result["proofs"]
                    ))
        replay_command = read_json(CHECKER / "replay.command.json")
        self.assertIn("--reexecute", replay_command)
        self.assertIn(read_json(CHECKER / "analyze.json")["run_dir"], replay_command)

    def test_preserved_checker_inputs_and_full_observations(self):
        source = (PROOFS / "isolated/consumers.rs").read_text()
        contracts = re.findall(r"\bensures\s*(.*?)\n;", source, flags=re.DOTALL)
        normalize = lambda text: re.sub(r"\s+", "", text).rstrip(",")
        comparisons = {
            "count": "r1 == r2",
            "last": "((r1 is Some) == (r2 is Some)) && "
                    "((r1 is Some) ==> (r1->Some_0 == r2->Some_0))",
        }
        snapshots = []
        for phase in ("analyze", "replay"):
            summary = read_json(CHECKER / f"{phase}.json")
            self.assertEqual(
                {target["qualified_name"] for target in summary["targets"]}, TARGETS,
            )
            run_dir = Path(summary["run_dir"])
            snapshot = read_json(run_dir / "snapshot.json")["payload"]
            snapshots.append(snapshot["files"])
            self.assertEqual(set(snapshot["files"]), {"consumers.rs", "iterator_methods.rs", "lib.rs"})
            for file in snapshot["files"]:
                self.assertEqual(
                    (run_dir / "workspace" / file).read_bytes(),
                    (PROOFS / "isolated" / file).read_bytes(),
                )
            for result in summary["results"]:
                name = result["target"]["name"]
                revision = Path(result["proofs"][0]["artifact"]).parents[1] / "revisions/0"
                native = read_json(revision / "contract.json")["payload"]["native"]
                spec = native["function_spec"]
                plan = read_json(revision / "observation-plan.json")["payload"]
                obligation = read_json(revision / "obligation.json")["payload"]["native"]
                self.assertEqual(native["source"], source)
                self.assertEqual(native["overlays"], {})
                self.assertEqual(native["accepted_semantics"], [])
                self.assertEqual(spec["generics_decl"], "<T, A: Allocator>")
                self.assertEqual(spec["where_decl"], "")
                self.assertEqual(spec["requires"], [])
                self.assertEqual(spec["result_binding"], "result")
                self.assertEqual(spec["type_defs"], {})
                self.assertEqual(spec["name"], f"<IntoIter<T, A> as core::iter::Iterator>::{name}")
                self.assertEqual(len(spec["params"]), 1)
                parameter = spec["params"][0]
                self.assertEqual(parameter["name"], "iter")
                self.assertEqual(parameter["type"]["name"], "IntoIter<T, A>")
                self.assertFalse(parameter["is_ref"])
                self.assertFalse(parameter["is_mut_ref"])
                self.assertEqual(spec["return_type"]["name"], "usize" if name == "count" else "Option<T>")
                self.assertEqual(len(spec["ensures"]), 1)
                self.assertEqual(
                    normalize(spec["ensures"][0]),
                    normalize(contracts[0 if name == "count" else 1]),
                )
                self.assertEqual(obligation["source_function_spec"], spec)
                self.assertEqual(plan["policy"], "verus-strict-v1")
                self.assertEqual(plan["ignored_dimensions"], [])
                self.assertEqual(plan["native"]["diagnostics"], [])
                self.assertEqual(plan["native"]["accepted_views"], {})
                comparison, = plan["native"]["comparisons"]
                self.assertEqual(comparison["dimension"], "return")
                self.assertEqual(comparison["expression"], comparisons[name])
                policy = plan["native"]["equal_policy"]
                self.assertEqual(policy["ignore_fields"], [])
                self.assertFalse(policy["opaque_ok"])
                self.assertIsNone(policy["custom_body"])
        self.assertEqual(snapshots[0], snapshots[1])
        expected = tomllib.loads((ROOT / "tests/into-iter-consumers/before/specdet.toml").read_text())
        expected["project"]["root"] = str(PROOFS / "isolated")
        expected["targets"]["include"] = ["consumers.rs"]
        expected["adapters"]["verus"]["executable"] = str(VERUS)
        expected["adapters"]["verus"]["environment"]["TMPDIR"] = str(CHECKER / "tmp")
        expected["artifacts"]["output_dir"] = str(CHECKER / "analysis-runs")
        self.assertEqual(tomllib.loads((CHECKER / "specdet.toml").read_text()), expected)

    def test_default_inputs_and_unrelated_coverage_preserved(self):
        before = ROOT / "tests/into-iter-consumers/before"
        self.assertEqual((before / "lib.rs").read_bytes(), (ROOT / "specs/lib.rs").read_bytes())
        self.assertEqual((before / "specdet.toml").read_bytes(), (ROOT / "specdet.toml").read_bytes())
        with (before / "coverage.tsv").open() as f:
            old = list(csv.DictReader(f, delimiter="\t"))
        with (ROOT / "inventory/coverage.tsv").open() as f:
            current = list(csv.DictReader(f, delimiter="\t"))
        self.assertEqual(len(old), 138)
        self.assertEqual(len(current), 138)
        changed = {
            "<alloc::vec::IntoIter<T, A> as core::iter::Iterator>::count",
            "<alloc::vec::IntoIter<T, A> as core::iter::Iterator>::last",
        }
        self.assertEqual(
            [row for row in old if row["canonical_api"] not in changed],
            [row for row in current if row["canonical_api"] not in changed],
        )


if __name__ == "__main__":
    unittest.main()
