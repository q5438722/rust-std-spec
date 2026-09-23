import json
import os
import re
import subprocess
import tomllib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.borrowed_scratch_config import write_config


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/alloc/src/vec/mod.rs")
RUSTC = ROOT / "toolchains/rustup/toolchains/1.98.1-x86_64-unknown-linux-gnu/bin/rustc"
VERUS = ROOT / "toolchains/verus-x86-linux/verus"
OUTPUT = Path(os.environ.get("BORROWED_TEST_OUTPUT", ROOT / "tests/output")).resolve()
BUILD = Path(os.environ.get("BORROWED_PROOF_BUILD", ROOT / "proofs/correctness/vec/build")).resolve()
COMPLETENESS = Path(os.environ.get(
    "BORROWED_COMPLETENESS_OUTPUT", ROOT / "proofs/completeness/vec")).resolve()
APIS = {
    "as_ref_vec": ("AsRef<Vec<T, A>>", "as_ref", "", "Vec<T, A>",
                   "result == vec,"),
    "as_ref_slice": ("AsRef<[T]>", "as_ref", "", "[T]", "result@ == vec@,"),
    "as_mut_vec": ("AsMut<Vec<T, A>>", "as_mut", "mut ", "Vec<T, A>",
                   "*result == *old(vec), *final(result) == *final(vec),"),
    "as_mut_slice": ("AsMut<[T]>", "as_mut", "mut ", "[T]",
                     "result@ == old(vec)@, final(result)@ == final(vec)@,"),
}


def compact(text):
    return re.sub(r"\s+", "", text)


def record_run(name, command):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / f"{name}.command.json").write_text(json.dumps(command, indent=2) + "\n")
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
    (OUTPUT / f"{name}.stdout").write_text(result.stdout)
    (OUTPUT / f"{name}.stderr").write_text(result.stderr)
    return result


def link_arguments():
    args = ["-L", f"dependency={BUILD}",
            "-L", f"dependency={ROOT / 'toolchains/verus-x86-linux'}",
            "-L", f"dependency={ROOT / 'toolchains/verus-x86-linux/deps'}"]
    for api in APIS:
        args += ["--extern", f"{api}={BUILD / ('lib' + api + '.rlib')}"]
    return args


class BorrowedConversions(unittest.TestCase):
    def test_scratch_config_preserves_analysis(self):
        original = (ROOT / "specdet.toml").read_text()
        expected = tomllib.loads(original)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=OUTPUT) as temporary:
            directory = Path(temporary)
            config = write_config(directory)
            expected["project"]["root"] = str(ROOT / "specs")
            expected["adapters"]["verus"]["executable"] = str(VERUS)
            expected["adapters"]["verus"]["environment"]["TMPDIR"] = str(directory / "tmp")
            expected["artifacts"]["output_dir"] = str(directory / "analysis-runs")
            self.assertEqual(tomllib.loads(config.read_text()), expected)
            self.assertEqual((ROOT / "specdet.toml").read_text(), original)
            with self.assertRaises(FileExistsError):
                write_config(directory)

    def test_source_body_and_exact_contract_binding(self):
        original = compact(SOURCE.read_text())
        specs = compact((ROOT / "specs/vec/borrowed.rs").read_text())
        self.assertEqual(specs.count("pubassume_specification"), 4)
        for api, (trait, method, mutable, result_type, ensures) in APIS.items():
            with self.subTest(api=api):
                source_impl = (
                    f"impl<T, A: Allocator> {trait} for Vec<T, A> {{"
                    f"fn {method}(&{mutable}self) -> &{mutable}{result_type} {{ self }} }}"
                )
                self.assertEqual(original.count(compact(source_impl)), 1)
                params = f"(vec: &'a {mutable}Vec<T, A>) -> (result: &'a {mutable}{result_type})"
                declaration = (
                    f"pub assume_specification<'a, T, A: Allocator>"
                    f"[<Vec<T, A> as {trait}>::{method}]{params} ensures {ensures};"
                )
                self.assertEqual(specs.count(compact(declaration)), 1)
                proof = compact((ROOT / f"proofs/correctness/vec/{api}.rs").read_text())
                expected = f"pub fn {api}<'a, T, A: Allocator>{params} ensures {ensures} {{ vec }}"
                self.assertEqual(proof.count(compact(expected)), 1)
                self.assertNotRegex(proof, r"assume|admit|external_body|requires|loop")
                self.assertEqual(proof.count("pubfn"), 1)

    def test_native_behavior(self):
        binary = OUTPUT / "borrowed_behavior"
        command = [str(RUSTC), "--edition=2021", "--test", "tests/borrowed_behavior.rs",
                   "-o", str(binary), *link_arguments()]
        compiled = record_run("native-build", command)
        self.assertEqual(compiled.returncode, 0, compiled.stdout + compiled.stderr)
        executed = record_run("native-tests", [str(binary)])
        self.assertEqual(executed.returncode, 0, executed.stdout + executed.stderr)
        self.assertIn("5 passed; 0 failed", executed.stdout)

    def test_writeback_composition(self):
        log_dir = OUTPUT / "writeback-verus"
        log_dir.mkdir(parents=True, exist_ok=True)
        result = record_run("writeback", [
            str(VERUS), "tests/borrowed_clients.rs", "--edition=2021", "--crate-type=lib",
            "--num-threads=1", "--log-all", "--log-dir", str(log_dir),
        ])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("6 verified, 0 errors", result.stdout)

    def test_published_completeness_files(self):
        directory = COMPLETENESS
        analysis = json.loads((directory / "analyze.json").read_text())
        for api, (trait, method, mutable, result_type, ensures) in APIS.items():
            target = f"vec/borrowed.rs::vec::borrowed::<Vec<T, A> as {trait}>::{method}"
            matches = [result for result in analysis["results"]
                       if result["target"]["qualified_name"] == target]
            with self.subTest(api=api):
                self.assertEqual(len(matches), 1)
                result = matches[0]
                published = directory / f"{api}.rs"
                if not mutable:
                    self.assertEqual(published.read_bytes(),
                                     Path(result["proofs"][0]["native"]["harness"]).read_bytes())
                    self.assertEqual((directory / f"{api}.smt2").read_bytes(),
                                     Path(result["baseline"]["artifact"]).read_bytes())
                else:
                    params = f"(vec: &'a mut Vec<T, A>) -> (result: &'a mut {result_type})"
                    declaration = (
                        f"pub assume_specification<'a, T, A: Allocator>"
                        f"[<Vec<T, A> as {trait}>::{method}]{params} ensures {ensures};"
                    )
                    self.assertIn(compact(declaration), compact(published.read_text()))
                    self.assertEqual(result["verdict"], "not_evaluated")
                    self.assertIsNone(result["baseline"])
                    self.assertEqual(result["proofs"], [])
                    self.assertEqual(result["diagnostics"][0]["code"],
                                     "unsupported_mutable_return")

    def test_receiver_lifetime_cannot_escape(self):
        for api, (_, _, mutable, result_type, _) in APIS.items():
            result_type = result_type.replace("T", "String").replace(", A", "")
            text = (
                "#![feature(allocator_api)]\n"
                f"fn escape<'a>() -> &'a {mutable}{result_type} {{\n"
                f"    let {mutable}vec = Vec::<String>::new();\n"
                f"    {api}::{api}(&{mutable}vec)\n"
                "}\nfn main() {}\n"
            )
            with self.subTest(api=api):
                self.check_rejection(f"lifetime-{api}", text, "E0515")

    def test_vector_and_slice_return_types_are_not_interchangeable(self):
        for api, (_, _, mutable, result_type, _) in APIS.items():
            wrong_type = "[String]" if result_type.startswith("Vec") else "Vec<String>"
            text = (
                "#![feature(allocator_api)]\n"
                "fn main() {\n"
                f"    let _: for<'a> fn(&'a {mutable}Vec<String>) -> &'a {mutable}{wrong_type}"
                f" = {api}::{api}::<String, std::alloc::Global>;\n"
                "}\n"
            )
            with self.subTest(api=api):
                self.check_rejection(f"return-type-{api}", text, "E0308")

    def check_rejection(self, name, text, diagnostic):
        OUTPUT.mkdir(parents=True, exist_ok=True)
        source = OUTPUT / f"{name}.rs"
        source.write_text(text)
        result = record_run(name, [
            str(RUSTC), "--edition=2021", "--crate-name", "borrowed_negative",
            str(source), "-o", str(OUTPUT / name), *link_arguments(),
        ])
        source.unlink()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(diagnostic, result.stderr, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
