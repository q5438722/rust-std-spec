import json
import os
import re
import subprocess
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/alloc/src/vec/mod.rs")
CORRECTNESS = ROOT / "proofs/correctness/vec/owned-conversions"
BUILD = Path(os.environ.get("OWNED_PROOF_BUILD", CORRECTNESS / "build")).resolve()
OUTPUT = Path(os.environ.get("OWNED_TEST_OUTPUT", ROOT / "tests/owned-conversions/engineer")).resolve()
COMPLETENESS = Path(os.environ.get(
    "OWNED_COMPLETENESS_OUTPUT", ROOT / "proofs/completeness/vec/owned-conversions/verus-module",
)).resolve()
VERUS = ROOT / "toolchains/verus-x86-linux"
RUSTC = ROOT / "toolchains/rustup/toolchains/1.98.1-x86_64-unknown-linux-gnu/bin/rustc"
TARGETS = {
    "from_array": {
        "binding": "<Vec<T> as From<[T; N]>>::from",
        "module": "array::",
        "generics": "<T, const N: usize>",
        "input": "[T; N]",
        "output": "Vec<T>",
        "body": "<[T]>::into_vec(Box::new(s))",
        "span": (4364, 4375),
        "impl": "impl<T, const N: usize> From<[T; N]> for Vec<T>",
    },
    "from_boxed_slice": {
        "binding": "<Vec<T, A> as From<Box<[T], A>>>::from",
        "module": "",
        "generics": "<T, A: Allocator>",
        "input": "Box<[T], A>",
        "output": "Vec<T, A>",
        "body": "s.into_vec()",
        "span": (4403, 4416),
        "impl": "impl<T, A: Allocator> From<Box<[T], A>> for Vec<T, A>",
    },
}


def tokens(text):
    text = re.sub(r"//[^\n]*|/\*.*?\*/", "", text, flags=re.DOTALL)
    return re.findall(r"[A-Za-z_]\w*|\d+|::|->|==|=>|!=|[^\s]", text)


def compact(text):
    return re.sub(r"\s+", "", text)


def read_json(path):
    return json.loads(path.read_text())


def declaration(target):
    return (
        f"pub assume_specification{target['generics']}[{target['binding']}]"
        f"(s: {target['input']}) -> (result: {target['output']}) "
        "ensures result@ == s@,;"
    )


def record_run(directory, name, arguments):
    command = [
        "bash", str(ROOT / "scripts/with_baseline.sh"),
        "env", f"TMPDIR={directory / 'compiler-tmp'}", *map(str, arguments),
    ]
    (directory / f"{name}.command.json").write_text(json.dumps(command, indent=2) + "\n")
    stdout = stderr = ""
    returncode = None
    timed_out = False
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=115)
        stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
        return result
    except subprocess.TimeoutExpired as error:
        timed_out = True
        stdout = error.stdout or ""
        stderr = error.stderr or ""
        raise
    finally:
        for suffix, text in (("stdout", stdout), ("stderr", stderr)):
            if isinstance(text, bytes):
                text = text.decode("utf-8", errors="replace")
            (directory / f"{name}.{suffix}").write_text(text)
        (directory / f"{name}.result.json").write_text(json.dumps({
            "returncode": returncode, "timed_out": timed_out,
        }, indent=2) + "\n")


class OwnedStaticBindings(unittest.TestCase):
    def test_original_bodies_and_generic_domains(self):
        source = SOURCE.read_text().splitlines()
        for name, target in TARGETS.items():
            with self.subTest(name=name):
                start, end = target["span"]
                returned = "Self" if name == "from_boxed_slice" else target["output"]
                original = (
                    f"{target['impl']} {{ fn from(s: {target['input']}) -> {returned} "
                    f"{{ {target['body']} }} }}"
                )
                self.assertEqual(tokens("\n".join(source[start - 1:end])), tokens(original))
                prefix = (
                    "#![cfg(not(no_global_oom_handling))]"
                    if name == "from_array" else
                    "#![feature(allocator_api)] use std::alloc::Allocator;"
                )
                proof = (
                    f"{prefix} use vstd::prelude::*; verus! {{ "
                    f"pub fn {name}{target['generics']}(s: {target['input']}) "
                    f"-> (result: {target['output']}) ensures result@ == s@, "
                    f"{{ {target['body']} }} }}"
                )
                self.assertEqual(
                    tokens((ROOT / f"proofs/correctness/vec/{name}.rs").read_text()),
                    tokens(proof),
                )
        self.assertEqual(source[4361].strip(), "#[cfg(not(no_global_oom_handling))]")
        self.assertIn("moves `s`'s items", "\n".join(source[4364:4371]))
        self.assertIn("existing heap allocation", "\n".join(source[4403:4412]))

    def test_exact_contracts_and_cfg_scope(self):
        expected = (
            "use std::alloc::Allocator; use vstd::prelude::*; verus! {"
            "pub mod array { #![cfg(not(no_global_oom_handling))]"
            "use vstd::prelude::*;"
            + declaration(TARGETS["from_array"]) + "}"
            + declaration(TARGETS["from_boxed_slice"]) + "}"
        )
        self.assertEqual(
            tokens((ROOT / "specs/vec/owned_conversions.rs").read_text()), tokens(expected),
        )

    def test_aggregate_and_checker_registration(self):
        aggregate = (ROOT / "specs/lib.rs").read_text()
        for name in ("borrowed", "owned_conversions", "observation", "conversions"):
            self.assertIn(f"pub mod {name};", aggregate)
        self.assertIn("pub mod cow", aggregate)
        config = (ROOT / "specdet.toml").read_text()
        for path in ("vec/borrowed.rs", "cow/conversions.rs", "vec/owned_conversions.rs"):
            self.assertIn(f'"{path}"', config)


class OwnedCompileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        OUTPUT.mkdir(parents=True, exist_ok=False)
        (OUTPUT / "compiler-tmp").mkdir()
        cls.links = [
            "-L", f"dependency={BUILD}",
            "-L", f"dependency={VERUS}",
            "-L", f"dependency={VERUS / 'deps'}",
        ]
        inputs = []
        for name in TARGETS:
            library = BUILD / f"libowned_{name}.rlib"
            source = ROOT / f"proofs/correctness/vec/{name}.rs"
            if not library.is_file() or library.stat().st_mtime_ns < source.stat().st_mtime_ns:
                raise AssertionError(f"Compile the current source body first: {library}")
            cls.links.extend(["--extern", f"owned_{name}={library}"])
            inputs.append({
                "source": str(source), "source_mtime_ns": source.stat().st_mtime_ns,
                "library": str(library), "library_mtime_ns": library.stat().st_mtime_ns,
            })
        (OUTPUT / "linked-inputs.json").write_text(json.dumps(inputs, indent=2) + "\n")

    def test_native_behavior(self):
        result = record_run(OUTPUT, "native-build", [
            RUSTC, "--edition=2021", "--test", ROOT / "tests/owned_conversions.rs",
            *self.links, "-o", OUTPUT / "native-tests",
        ])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        result = record_run(OUTPUT, "native-tests", [OUTPUT / "native-tests", "--test-threads=1"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("7 passed; 0 failed", result.stdout)

    def test_generic_contract_clients(self):
        for name, cfg, count in (
            ("clients", [], 6),
            ("clients-no-global-oom", ["--cfg", "no_global_oom_handling"], 3),
        ):
            with self.subTest(name=name):
                result = record_run(OUTPUT, name, [
                    VERUS / "verus", ROOT / "tests/owned_conversion_clients.rs",
                    "--edition=2021", "--crate-type=lib", "--crate-name", "owned_conversion_clients",
                    "--compile", "--num-threads=1", "--log-all",
                    "--log-dir", OUTPUT / name, "-o", OUTPUT / f"{name}.rlib", *cfg,
                ])
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertRegex(result.stdout, rf"verification results:: {count} verified, 0 errors")

    def reject(self, name, source, diagnostics, message):
        path = OUTPUT / f"{name}.rs"
        (OUTPUT / f"{name}.input.json").write_text(json.dumps({
            "source": source, "expected_diagnostics": diagnostics,
        }, indent=2) + "\n")
        path.write_text(source)
        try:
            result = record_run(OUTPUT, name, [
                RUSTC, "--edition=2021", "--crate-type=lib", "--crate-name", "owned_negative",
                "--emit=metadata", path,
                *self.links, "-o", OUTPUT / f"{name}.rmeta",
            ])
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            errors = re.findall(r"^error\[(E\d+)\]", result.stderr, re.MULTILINE)
            self.assertTrue(errors, result.stdout + result.stderr)
            self.assertTrue(set(errors).issubset(diagnostics), result.stderr)
            self.assertIn(message, result.stderr)
        finally:
            path.unlink()

    def test_move_reuse_is_rejected(self):
        for name in TARGETS:
            for implementation in ("source", "std"):
                with self.subTest(name=name, implementation=implementation):
                    if name == "from_array":
                        input = "let input = [Token];"
                        call = "owned_from_array::from_array(input)"
                        standard = "<Vec<Token> as From<[Token; 1]>>::from(input)"
                    else:
                        input = "let input: Box<[Token]> = Box::new([Token]);"
                        call = "owned_from_boxed_slice::from_boxed_slice(input)"
                        standard = "<Vec<Token> as From<Box<[Token]>>>::from(input)"
                    expression = call if implementation == "source" else standard
                    self.reject(
                        f"move-{name}-{implementation}",
                        f"struct Token; fn rejected() {{ {input} let _result = {expression}; "
                        "let _reused = input; }\n",
                        ["E0382"], "moved value",
                    )

    def test_borrowed_elements_cannot_escape(self):
        for name in TARGETS:
            for implementation in ("source", "std"):
                with self.subTest(name=name, implementation=implementation):
                    if name == "from_array":
                        input = "let input = [&local];"
                        call = "owned_from_array::from_array(input)"
                        standard = "<Vec<&i32> as From<[&i32; 1]>>::from(input)"
                    else:
                        input = "let input: Box<[&i32]> = Box::new([&local]);"
                        call = "owned_from_boxed_slice::from_boxed_slice(input)"
                        standard = "<Vec<&i32> as From<Box<[&i32]>>>::from(input)"
                    expression = call if implementation == "source" else standard
                    self.reject(
                        f"lifetime-{name}-{implementation}",
                        f"fn rejected<'a>() -> Vec<&'a i32> {{ let local = 9; {input} "
                        f"{expression} }}\n",
                        ["E0515", "E0597"], "local",
                    )


class OwnedCompletenessTests(unittest.TestCase):
    def test_private_config_preserves_analysis(self):
        expected = tomllib.loads((ROOT / "specdet.toml").read_text())
        expected["project"]["root"] = str(ROOT / "specs")
        expected["adapters"]["verus"]["executable"] = str(VERUS / "verus")
        expected["adapters"]["verus"]["environment"]["TMPDIR"] = str(COMPLETENESS / "tmp")
        expected["artifacts"]["output_dir"] = str(COMPLETENESS / "analysis-runs")
        self.assertEqual(tomllib.loads((COMPLETENESS / "specdet.toml").read_text()), expected)

    def test_current_native_analysis_and_reexecution(self):
        runs = [read_json(COMPLETENESS / f"{name}.json") for name in ("analyze", "replay")]
        self.assertNotEqual(runs[0]["run_dir"], runs[1]["run_dir"])
        qualified = {
            compact("vec/owned_conversions.rs::vec::owned_conversions::"
                    + target["module"] + target["binding"]): name
            for name, target in TARGETS.items()
        }
        for summary in runs:
            with self.subTest(run=summary["run_dir"]):
                self.assertEqual(summary["discovery_coverage"], "source-visible")
                self.assertEqual(summary["diagnostics"], [])
                self.assertEqual(len(summary["results"]), 2)
                self.assertEqual(
                    {compact(result["target"]["qualified_name"]) for result in summary["results"]},
                    set(qualified),
                )
                run = ROOT / summary["run_dir"]
                snapshot = read_json(run / "snapshot.json")["payload"]["files"]
                for file in snapshot:
                    self.assertEqual((run / "workspace" / file).read_bytes(),
                                     (ROOT / "specs" / file).read_bytes(), file)
                for result in summary["results"]:
                    name = qualified[compact(result["target"]["qualified_name"])]
                    target = TARGETS[name]
                    with self.subTest(target=name):
                        self.assertEqual(result["target"]["source_digest"],
                                         snapshot["vec/owned_conversions.rs"])
                        self.assertEqual(result["status"], "completed")
                        self.assertEqual(result["verdict"], "deterministic")
                        self.assertEqual(result["baseline"]["status"], "unsat")
                        self.assertEqual(result["baseline"]["constraints"], [])
                        self.assertIsNone(result["search"])
                        self.assertEqual(len(result["proofs"]), 1)
                        proof = result["proofs"][0]
                        self.assertEqual(proof["status"], "verified")
                        self.assertGreater(proof["verified_goals"], 0)
                        revision = Path(proof["artifact"]).parents[1] / "revisions/0"
                        contract = read_json(revision / "contract.json")["payload"]["native"]["function_spec"]
                        self.assertEqual(compact(contract["generics_decl"]), compact(target["generics"]))
                        self.assertEqual(contract["requires"], [])
                        self.assertEqual([compact(clause) for clause in contract["ensures"]], ["result@==s@"])
                        self.assertEqual(len(contract["params"]), 1)
                        param = contract["params"][0]
                        self.assertEqual(param["name"], "s")
                        self.assertFalse(param["is_ref"])
                        self.assertFalse(param["is_mut_ref"])
                        self.assertEqual(compact(param["type"]["name"]), compact(target["input"]))
                        self.assertEqual(compact(contract["return_type"]["name"]), compact(target["output"]))
                        observation = read_json(revision / "observation-plan.json")["payload"]
                        self.assertEqual(observation["policy"], "verus-strict-v1")
                        comparisons = observation["native"]["comparisons"]
                        self.assertEqual(len(comparisons), 1)
                        self.assertEqual(comparisons[0]["dimension"], "return")
                        self.assertEqual(comparisons[0]["expression"], "(r1)@ =~= (r2)@")
                        obligation = read_json(revision / "obligation.json")["payload"]
                        self.assertIs(obligation["trusted_translation"], True)
                        policy = proof["native"]["det_spec"]["equal_policy"]
                        self.assertIsNone(policy["custom_body"])
                        self.assertFalse(policy["opaque_ok"])
                        self.assertEqual(policy["ignore_fields"], [])
                        query = Path(result["baseline"]["artifact"]).read_text()
                        guards = re.findall(r"\(declare-fun (g_[^\s()]+) \(\) Bool\)", query)
                        expected_guards = (
                            ["g_s_leneq!", "g_s_lenrng!"] if name == "from_array" else []
                        ) + [
                            "g_r1_leneq!", "g_r1_lenrng!", "g_r2_leneq!",
                            "g_r2_lenrng!", "g_neq_tuple!",
                        ]
                        self.assertCountEqual(guards, expected_guards)
                        self.assertEqual(query.count("(check-sat"), 1)
                        final = query.strip().splitlines()[-1]
                        self.assertEqual(
                            final, "(check-sat-assuming ("
                            + " ".join(f"(not {guard})" for guard in expected_guards) + "))",
                        )
                        self.assertEqual(len(proof["native"]["invocations"]), 1)
                        for invocation in proof["native"]["invocations"]:
                            self.assertEqual(invocation["process"]["returncode"], 0)
                            self.assertFalse(invocation["process"]["timed_out"])
                            self.assertGreater(invocation["verified_goals"], 0)


if __name__ == "__main__":
    unittest.main()
