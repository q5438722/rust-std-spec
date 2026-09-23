"""Cow-only supplements; neither native tests nor contract clients prove source correctness.

Native std calls use Rust 1.98.1; Rust 1.96 source correspondence is token-checked separately.

Replay (from the project root, after the four proof crates and aggregate are built):
  bash scripts/with_baseline.sh env TMPDIR="$PWD/tests/cow-engineer/compiler-tmp" \
    COW_PROOF_BUILD=proofs/correctness/cow/cow-engineer/build \
    COW_TEST_OUTPUT=tests/cow-engineer \
    COW_COMPLETENESS_OUTPUT=proofs/completeness/cow/cow-engineer \
    python3 -m unittest discover -s tests -p 'test_cow_bindings.py' -v

Add ``-k CowStaticBindings`` to check source correspondence without any compiler.
Each compiler command is bounded to 120 seconds; longer orchestration belongs in
the Argus durable runner. No source proof or unchanged borrowed proof is rebuilt.
"""

import json
import os
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    "/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/alloc/src/vec/cow.rs"
)
RUSTC = ROOT / "toolchains/rustup/toolchains/1.98.1-x86_64-unknown-linux-gnu/bin/rustc"
VERUS = ROOT / "toolchains/verus-x86-linux/verus"
OFFICIAL = VERUS.parent
BUILD = Path(os.environ.get(
    "COW_PROOF_BUILD", ROOT / "proofs/correctness/cow/cow-engineer/build")).resolve()
OUTPUT = Path(os.environ.get("COW_TEST_OUTPUT", ROOT / "tests/cow-engineer")).resolve()
COMPLETENESS = Path(os.environ.get(
    "COW_COMPLETENESS_OUTPUT", ROOT / "proofs/completeness/cow/cow-engineer")).resolve()
OBSERVATION = ROOT / "specs/cow/observation.rs"
CONVERSIONS = ROOT / "specs/cow/conversions.rs"
APIS = {
    "from_slice": ("&'a [T]", "s", "<'a, T: Clone>", "Cow::Borrowed(s)", "Borrowed", (12, 14)),
    "from_array": ("&'a [T; N]", "s", "<'a, T: Clone, const N: usize>",
                   "Cow::Borrowed(s as &[_])", "Borrowed", (25, 27)),
    "from_vec": ("Vec<T>", "v", "<'a, T: Clone>", "Cow::Owned(v)", "Owned", (38, 40)),
    "from_vec_ref": ("&'a Vec<T>", "v", "<'a, T: Clone>",
                     "Cow::Borrowed(v.as_slice())", "Borrowed", (51, 53)),
}
LIFETIME_DIAGNOSTICS = {
    "E0515": "cannot return value referencing local variable",
    "E0597": "does not live long enough",
}
TOKEN = re.compile(
    r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|'
    r"'[A-Za-z_]\w*|[A-Za-z_]\w*|\d+|::|->|=>|==|!=|[^\s]",
    re.DOTALL,
)


def tokens(text):
    return [token for token in TOKEN.findall(text) if not token.startswith(("//", "/*"))]


def compact(text):
    return re.sub(r"\s+", "", text)


def record_run(directory, name, arguments):
    """Retain the actual baseline wrapper, private TMPDIR, output, and exit status."""
    directory = directory.resolve()
    directory.mkdir(parents=True, exist_ok=True)
    supplied_tmp = os.environ.get("TMPDIR")
    scratch = Path(supplied_tmp).resolve() if supplied_tmp else directory / "compiler-tmp"
    if scratch == ROOT / "toolchains/tmp":
        scratch = directory / "compiler-tmp"
    scratch.mkdir(parents=True, exist_ok=True)
    command = [
        "bash", "scripts/with_baseline.sh", "env", f"TMPDIR={scratch}",
        *map(str, arguments),
    ]
    prefix = directory / name
    prefix.with_suffix(".command.json").write_text(json.dumps(command, indent=2) + "\n")
    status = {"returncode": None, "timed_out": False}
    stdout = stderr = ""
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
        stdout, stderr = result.stdout, result.stderr
        status["returncode"] = result.returncode
        return result
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or ""
        stderr = error.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        status["timed_out"] = True
        raise AssertionError(f"{name} timed out; see {prefix}.result.json") from error
    except OSError as error:
        stderr = str(error)
        raise
    finally:
        prefix.with_suffix(".stdout").write_text(stdout)
        prefix.with_suffix(".stderr").write_text(stderr)
        prefix.with_suffix(".result.json").write_text(json.dumps(status, indent=2) + "\n")


def link_arguments():
    args = [
        "-L", f"dependency={BUILD}",
        "-L", f"dependency={OFFICIAL}",
        "-L", f"dependency={OFFICIAL / 'deps'}",
        "--extern", f"vstd={OFFICIAL / 'libvstd.rlib'}",
        "--extern", f"vec_specs={BUILD / 'libvec_specs.rlib'}",
    ]
    for api in APIS:
        args += ["--extern", f"{api}={BUILD / ('lib' + api + '.rlib')}"]
    return args


class CowStaticBindings(unittest.TestCase):
    def assert_tokens_present_once(self, expected, actual):
        needle, haystack = tokens(expected), tokens(actual)
        occurrences = sum(
            haystack[index:index + len(needle)] == needle
            for index in range(len(haystack) - len(needle) + 1)
        )
        self.assertEqual(occurrences, 1, expected)

    def test_canonical_signatures_bodies_and_exact_contract_bindings(self):
        source = SOURCE.read_text()
        specs = CONVERSIONS.read_text()
        declarations = re.findall(r"pub\s+assume_specification.*?\n\s*;", specs, re.DOTALL)
        self.assertEqual(len(declarations), 4)
        self.assertNotIn("requires", tokens(specs))
        for api, (input_type, param, generics, body, variant, span) in APIS.items():
            with self.subTest(api=api):
                signature = f"({param}: {input_type}) -> Cow<'a, [T]>"
                canonical = (
                    f"impl{generics} From<{input_type}> for Cow<'a, [T]> {{"
                    f"fn from{signature} {{ {body} }} }}"
                )
                self.assert_tokens_present_once(canonical, source)
                source_body = "\n".join(source.splitlines()[span[0] - 1:span[1]])
                self.assertEqual(tokens(source_body), tokens(f"fn from{signature} {{ {body} }}"))
                binding = f"<Cow<'a, [T]> as From<{input_type}>>::from"
                params = f"({param}: {input_type}) -> (result: Cow<'a, [T]>)"
                postcondition = (
                    f"ensures CowObservation::view(&result) == CowContents::{variant}({param}@),"
                )
                matches = [declaration for declaration in declarations
                           if compact(binding) in compact(declaration)]
                self.assertEqual(len(matches), 1)
                declaration = matches[0]
                expected = f"pub assume_specification{generics}[{binding}]{params}"
                self.assertEqual(tokens(declaration), tokens(f"{expected} {postcondition};"))
                proof = (ROOT / f"proofs/correctness/cow/{api}.rs").read_text()
                self.assert_tokens_present_once(
                    f"pub fn {api}{generics}{params} {postcondition} {{ {body} }}", proof)
                proof_tokens = tokens(proof)
                self.assertEqual(proof_tokens.count("fn"), 1)
                self.assertEqual(proof_tokens.count("mod"), 1)
                self.assertEqual(
                    re.findall(r"\buse\s+([^;]+);", proof),
                    ["std::borrow::Cow", "vstd::prelude::*", "observation::{CowContents, CowObservation}"],
                )
                self.assert_tokens_present_once(
                    '#[path = "../../../specs/cow/observation.rs"] pub mod observation;', proof)
                for forbidden in (
                    "requires", "assume", "assume_specification", "admit", "external_body",
                    "external", "axiom", "unimplemented", "todo", "loop", "include",
                ):
                    self.assertNotIn(forbidden, proof_tokens)

    def test_observer_is_transparent_and_universal_for_clone(self):
        observation = OBSERVATION.read_text()
        self.assert_tokens_present_once(
            "pub enum CowContents<T> { Borrowed(Seq<T>), Owned(Seq<T>), }", observation)
        self.assert_tokens_present_once(
            "pub trait CowObservation<T> { spec fn view(&self) -> CowContents<T>; }", observation)
        self.assert_tokens_present_once(
            """impl<'a, T: Clone> CowObservation<T> for Cow<'a, [T]> {
                open spec fn view(&self) -> CowContents<T> {
                    match self {
                        Cow::Borrowed(s) => CowContents::Borrowed(s@),
                        Cow::Owned(v) => CowContents::Owned(v@),
                    }
                }
            }""", observation)
        for forbidden in ("assume", "assume_specification", "admit", "external_body", "requires"):
            self.assertNotIn(forbidden, tokens(observation))

    def test_original_cfg_and_default_allocator_are_retained(self):
        self.assert_tokens_present_once(
            "#[cfg(not(no_global_oom_handling))] mod cow;", SOURCE.with_name("mod.rs").read_text())
        self.assert_tokens_present_once(
            "pub mod cow { #![cfg(not(no_global_oom_handling))] pub mod observation; pub mod conversions; }",
            (ROOT / "specs/lib.rs").read_text(),
        )
        for path in [OBSERVATION, CONVERSIONS, *(
            ROOT / f"proofs/correctness/cow/{api}.rs" for api in APIS
        )]:
            with self.subTest(file=path):
                self.assert_tokens_present_once("#![cfg(not(no_global_oom_handling))]", path.read_text())
                self.assertNotIn("Allocator", tokens(path.read_text()))

    def test_clients_add_no_bounds_or_local_contract_assumptions(self):
        client = (ROOT / "tests/cow_clients.rs").read_text()
        for forbidden in ("where", "requires", "assume_specification", "assume", "admit", "external_body"):
            self.assertNotIn(forbidden, tokens(client))
        self.assert_tokens_present_once('#[path = "../specs/lib.rs"] mod aggregate;', client)
        for input_type, param, _, _, _, _ in APIS.values():
            self.assert_tokens_present_once(
                f"<Cow<'a, [T]> as From<{input_type}>>::from({param})", client)


class CowBindingClients(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = OUTPUT / "bindings"
        cls.output.mkdir(parents=True, exist_ok=False)
        cls().require_fresh_build()

    def require_fresh_build(self):
        inputs = {}
        for api in [*APIS, "vec_specs"]:
            library = BUILD / f"lib{api}.rlib"
            self.assertTrue(library.is_file(), f"Build {library} before running Cow native tests")
            sources = [OBSERVATION]
            if api == "vec_specs":
                sources += [CONVERSIONS, ROOT / "specs/lib.rs", ROOT / "specs/vec/borrowed.rs"]
            else:
                sources += [ROOT / f"proofs/correctness/cow/{api}.rs"]
            self.assertGreaterEqual(
                library.stat().st_mtime_ns, max(path.stat().st_mtime_ns for path in sources),
                f"{library} predates its source; rebuild this Cow crate, not borrowed proofs",
            )
            inputs[api] = {
                "library": str(library),
                "built_at_ns": library.stat().st_mtime_ns,
                "sources": [str(path) for path in sources],
            }
        (self.output / "linked-inputs.json").write_text(json.dumps(inputs, indent=2) + "\n")

    def test_native_behavior_and_full_domain_signatures(self):
        binary = self.output / "cow_behavior"
        compiled = record_run(self.output, "native-build", [
            RUSTC, "--edition=2021", "--test", "tests/cow_behavior.rs",
            "-o", binary, *link_arguments(),
        ])
        self.assertEqual(compiled.returncode, 0, compiled.stdout + compiled.stderr)
        executed = record_run(self.output, "native-tests", [binary])
        self.assertEqual(executed.returncode, 0, executed.stdout + executed.stderr)
        self.assertIn("6 passed; 0 failed", executed.stdout)

    def test_observer_and_original_from_contract_clients_in_aggregate(self):
        logs = self.output / "client-verus"
        logs.mkdir()
        result = record_run(self.output, "clients", [
            VERUS, "tests/cow_clients.rs", "--edition=2021", "--crate-type=lib",
            "--num-threads=1", "--log-all", "--log-dir", logs,
        ])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        verified = re.search(r"verification results:: (\d+) verified, 0 errors", result.stdout)
        self.assertIsNotNone(verified, result.stdout + result.stderr)
        self.assertGreaterEqual(int(verified.group(1)), 7)

    def check_rust_rejection(self, name, text, diagnostics):
        source = self.output / f"{name}.rs"
        source.write_text(text)
        # Preserve the probe input with its command even though only temporary .rs files are removed.
        (self.output / f"{name}.input.json").write_text(json.dumps({"source": text}, indent=2) + "\n")
        try:
            result = record_run(self.output, name, [
                RUSTC, "--edition=2021", "--crate-name", "cow_negative",
                source, "-o", self.output / name, *link_arguments(),
            ])
        finally:
            source.unlink()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        codes = re.findall(r"^error\[(E\d+)\]", result.stderr, re.MULTILINE)
        self.assertTrue(codes, result.stdout + result.stderr)
        self.assertTrue(set(codes).issubset(diagnostics), result.stdout + result.stderr)
        for code in codes:
            self.assertIn(diagnostics[code], result.stderr, result.stdout + result.stderr)

    def test_borrowed_lifetimes_cannot_escape_for_std_and_source_copies(self):
        for api, input_type, declaration, argument in [
            ("from_slice", "&'a [String]", 'let values = vec![String::from("local")];', "&values[..]"),
            ("from_array", "&'a [String; 1]", 'let values = [String::from("local")];', "&values"),
            ("from_vec_ref", "&'a Vec<String>", 'let values = vec![String::from("local")];', "&values"),
        ]:
            for binding in ("std", "copy"):
                callee = (
                    f"<Cow<'a, [String]> as From<{input_type}>>::from"
                    if binding == "std" else f"{api}::{api}"
                )
                with self.subTest(api=api, binding=binding):
                    self.check_rust_rejection(
                        f"lifetime-{api}-{binding}",
                        "use std::borrow::Cow;\n"
                        f"fn escape<'a>() -> Cow<'a, [String]> {{\n"
                        f"    {declaration}\n    {callee}({argument})\n}}\nfn main() {{}}\n",
                        LIFETIME_DIAGNOSTICS,
                    )

    def test_owned_cow_cannot_extend_element_lifetimes(self):
        for binding, callee in [
            ("std", "<Cow<'a, [&'a str]> as From<Vec<&'a str>>>::from"),
            ("copy", "from_vec::from_vec"),
        ]:
            with self.subTest(binding=binding):
                self.check_rust_rejection(
                    f"element-lifetime-from-vec-{binding}",
                    "use std::borrow::Cow;\n"
                    "fn escape<'a>() -> Cow<'a, [&'a str]> {\n"
                    '    let text = String::from("local");\n'
                    "    let values = vec![text.as_str()];\n"
                    f"    {callee}(values)\n}}\nfn main() {{}}\n",
                    LIFETIME_DIAGNOSTICS,
                )

    def test_moved_vec_cannot_be_reused_for_std_and_source_copy(self):
        for binding, callee in [
            ("std", "<Cow<'_, [String]> as From<Vec<String>>>::from"),
            ("copy", "from_vec::from_vec"),
        ]:
            with self.subTest(binding=binding):
                self.check_rust_rejection(
                    f"moved-vec-{binding}",
                    "use std::borrow::Cow;\nfn main() {\n"
                    '    let values = vec![String::from("moved")];\n'
                    f"    let result: Cow<'_, [String]> = {callee}(values);\n"
                    "    let _ = values.len();\n    drop(result);\n}\n",
                    {"E0382": "borrow of moved value"},
                )

    def test_published_completeness_artifacts_match_current_cow_candidate(self):
        analysis = json.loads((COMPLETENESS / "analyze.json").read_text())
        workspace = Path(analysis["run_dir"]) / "workspace"
        snapshot = json.loads((workspace.parent / "snapshot.json").read_text())["payload"]["files"]
        for relative in ("cow/observation.rs", "cow/conversions.rs"):
            self.assertEqual((workspace / relative).read_bytes(), (ROOT / "specs" / relative).read_bytes())
        for api, (input_type, _, _, _, _, _) in APIS.items():
            binding = compact(f"<Cow<'a, [T]> as From<{input_type}>>::from")
            matches = [
                result for result in analysis["results"]
                if result["target"]["file"] == "cow/conversions.rs"
                and compact(result["target"]["qualified_name"]).endswith("::" + binding)
            ]
            with self.subTest(api=api):
                self.assertEqual(len(matches), 1)
                result = matches[0]
                self.assertEqual(result["target"]["source_digest"], snapshot["cow/conversions.rs"])
                self.assertEqual(result["status"], "completed")
                self.assertEqual(result["verdict"], "deterministic")
                self.assertEqual(result["baseline"]["status"], "unsat")
                self.assertEqual(result["baseline"]["constraints"], [])
                self.assertEqual(len(result["proofs"]), 1)
                proof = result["proofs"][0]
                self.assertEqual(proof["status"], "verified")
                self.assertGreater(proof["verified_goals"], 0)
                self.assertEqual(
                    (COMPLETENESS / f"{api}.rs").read_bytes(),
                    Path(proof["native"]["harness"]).read_bytes(),
                )
                self.assertEqual(
                    (COMPLETENESS / f"{api}.smt2").read_bytes(),
                    Path(result["baseline"]["artifact"]).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
