import contextlib
import csv
import io
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import collect_borrowed_results as collector


ROOT = Path(__file__).resolve().parents[1]
COLUMNS = [
    "canonical_api", "module", "source", "docstrings", "vstd_coverage", "vstd_specs",
    "views", "project_spec", "correctness_proof", "correctness_command", "correctness_result",
    "completeness_file", "completeness_command", "completeness_result", "native_query",
    "observation_plan", "reexecution", "issues", "independent_review", "notes",
]
ENSURES = {
    "as_ref_vec": ["result == vec"],
    "as_ref_slice": ["result@ == vec@"],
    "as_mut_vec": ["*result == *old(vec)", "*final(result) == *final(vec)"],
    "as_mut_slice": ["result@ == old(vec)@", "final(result)@ == final(vec)@"],
}
ENTRYPOINT = "#![feature(allocator_api)]\npub mod shared;\npub mod vec {\n    pub mod borrowed;\n}\n"
GUARDS = [
    "g_vec_leneq!", "g_vec_lenrng!", "g_r1_leneq!", "g_r1_lenrng!",
    "g_r2_leneq!", "g_r2_lenrng!", "g_neq_tuple!",
]


class CollectBorrowedResults(unittest.TestCase):
    """Exercise collection with synthetic evidence, without invoking proof tools."""

    def setUp(self):
        temporary = TemporaryDirectory(prefix="collector-fixture-", dir=ROOT / "tests")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.patch_root = patch.object(collector, "ROOT", self.root)
        self.patch_root.start()
        self.addCleanup(self.patch_root.stop)
        self.coverage = self.root / "inventory/coverage.tsv"
        self.canonical = {
            slug: f"<alloc::vec::Vec<T, A> as {trait}>::{target.rsplit('::', 1)[1]}"
            for trait, (slug, target, _) in collector.TARGETS.items()
        }
        source_apis = []
        vstd_apis = []
        rows = []
        for index, (trait, (slug, _, _)) in enumerate(collector.TARGETS.items(), 1):
            canonical = self.canonical[slug]
            source_apis.append({
                "canonical_id": canonical,
                "source": {"path": "alloc/src/vec/mod.rs", "start_line": index, "end_line": index},
                "docs": [{"ref": f"core/src/convert/mod.rs:{index}"}],
            })
            vstd_apis.append({
                "canonical_id": canonical, "source_module": "mod", "canonical_trait": trait,
                "direct_spec_refs": [], "compiler_hook_refs": [], "trait_contract_refs": [],
                "concrete_spec_impl_refs": [], "view_dependencies": [], "coverage_class": "indirect",
            })
            row = dict.fromkeys(COLUMNS, "")
            row.update(canonical_api=canonical, independent_review="not_requested")
            rows.append(row)
        for index in range(134):
            canonical = f"other::api_{index}"
            source_apis.append({"canonical_id": canonical})
            vstd_apis.append({
                "canonical_id": canonical, "source_module": "cow" if index < 4 else "drain",
                "canonical_trait": "core::convert::AsRef<[T]>",
            })
            row = {column: f"retained {index} {column}\twith\nwhitespace" for column in COLUMNS}
            row["canonical_api"] = canonical
            rows.insert(index, row)
        self.write_json("inventory/source_api.json", {
            "counts": {"stable_public_executable": 138}, "apis": source_apis,
        })
        self.write_json("inventory/vstd_coverage.json", {
            "apis": vstd_apis, "evidence": [], "views": [],
        })
        self.write_rows(rows)

    def write(self, path, text):
        path = self.root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def write_json(self, path, data):
        return self.write(path, json.dumps(data))

    def read_rows(self):
        with self.coverage.open(newline="") as stream:
            return list(csv.DictReader(stream, delimiter="\t"))

    def write_rows(self, rows):
        self.coverage.parent.mkdir(parents=True, exist_ok=True)
        with self.coverage.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    def make_evidence(self, name, *, extra=False, candidate="original", dependency="original",
                      baseline="original", entrypoint=ENTRYPOINT, build_args=None):
        directory = self.root / name
        correctness = directory / "correctness"
        completeness = directory / "completeness"
        ensures = {slug: list(clauses) for slug, clauses in ENSURES.items()}
        if candidate != "original":
            ensures["as_ref_vec"] = ["result@ == vec@"]
        declarations = []
        for slug, target, _ in collector.TARGETS.values():
            mutable = "mut " if slug.startswith("as_mut") else ""
            result_type = "Vec<T, A>" if slug.endswith("vec") else "[T]"
            clauses = "\n".join(f"        {clause}," for clause in ensures[slug])
            declarations.append(
                f"pub assume_specification<'a, T, A: Allocator>[\n    {target}\n"
                f"](vec: &'a {mutable}Vec<T, A>) -> (result: &'a {mutable}{result_type})\n"
                f"    ensures\n{clauses}\n;"
            )
            self.write(correctness / f"{slug}.log", "verification results:: 1 verified, 0 errors\n")
            self.write(correctness / f"build/lib{slug}.rlib", "fixture library")
            self.write(correctness / slug / "crate.vir",
                       f":name (Fun :path {slug}::{slug}) :is_external_body false ) :body (@ vec")
        code = "use std::alloc::Allocator;\nuse vstd::prelude::*;\nuse crate::shared::*;\n\n"
        code += "verus! {\n\n" + "\n\n".join(declarations) + "\n\n}\n"
        sources = {
            "lib.rs": entrypoint, "vec/borrowed.rs": code,
            "shared.rs": f"// fixture dependency {dependency}\n",
        }
        digests = {
            "lib.rs": entrypoint, "vec/borrowed.rs": candidate, "shared.rs": dependency,
        }
        if extra:
            sources["vec/cow.rs"] = "// independent Cow fixture\n"
            digests["vec/cow.rs"] = "cow"
        for file, text in sources.items():
            self.write(Path("specs") / file, text)
        for operation in ("analyze", "replay"):
            run = completeness / f"{operation}-run"
            for file, text in sources.items():
                self.write(run / "workspace" / file, text)
            self.write_json(run / "snapshot.json", {"payload": {"files": digests}})
            self.write_json(run / "toolchains.json", {
                "producer_version": "fixture-checker",
                "payload": {
                    "executable_digest": baseline, "rust_toolchain": "1.98.1",
                    "version": "fixture-verus", "z3_python": "4.12.5",
                },
            })
            self.write_json(run / "effective-config.json", {"payload": {
                "build": {"entrypoint": "lib.rs", "extra_args": build_args or []},
                "toolchain": {"extra_args": [], "environment": {"TMPDIR": str(run / "scratch")}},
                "observation_policy": "verus-strict-v1",
            }})
            results = []
            for line, (slug, target, observation) in enumerate(collector.TARGETS.values(), 1):
                target_data = {
                    "qualified_name": f"vec/borrowed.rs::vec::borrowed::{target}",
                    "file": "vec/borrowed.rs", "source_digest": candidate, "line": line,
                }
                result = {
                    "target": target_data, "status": "failed", "verdict": "not_evaluated",
                    "baseline": None, "proofs": [], "search": [],
                    "diagnostics": [{"code": "unsupported_mutable_return"}],
                }
                if observation is not None:
                    attempt = run / "targets" / slug / "attempts/000"
                    revisions = run / "targets" / slug / "revisions/0"
                    harness = self.write(attempt / "harness.rs", f"// fixture harness for {slug}\n")
                    query = self.write(
                        attempt / "query.smt2",
                        "(check-sat-assuming (" + " ".join(f"(not {g})" for g in GUARDS) + "))\n",
                    )
                    self.write_json(revisions / "contract.json", {"payload": {"native": {
                        "function_spec": {
                            "name": target, "generics_decl": "<'a, T, A: Allocator>", "requires": [],
                            "params": [{"name": "vec", "is_ref": True, "is_mut_ref": False,
                                        "type": {"name": "Vec<T, A>"}}],
                            "return_type": {"name": "&Vec<T, A>" if slug.endswith("vec") else "&[T]"},
                            "ensures": ensures[slug],
                        },
                    }}})
                    self.write_json(revisions / "observation-plan.json", {"payload": {
                        "policy": "verus-strict-v1", "native": {"comparisons": [
                            {"dimension": "return", "expression": observation},
                        ]},
                    }})
                    self.write_json(revisions / "obligation.json", {"payload": {
                        "trusted_translation": True,
                    }})
                    result.update(
                        status="completed", verdict="deterministic", diagnostics=[],
                        baseline={"status": "unsat", "constraints": [], "artifact": str(query)},
                        proofs=[{"status": "verified", "verified_goals": 1, "artifact": str(attempt),
                                 "native": {"harness": str(harness)}}],
                    )
                results.append(result)
            if extra:
                results.extend({
                    "target": {"qualified_name": f"vec/cow.rs::vec::cow::from_{index}"},
                    "status": "completed", "verdict": "deterministic",
                } for index in range(4))
            self.write_json(completeness / f"{operation}.json", {
                "run_dir": str(run), "results": results,
                "counts": {"deterministic": 6 if extra else 2, "not_evaluated": 2},
            })
        return correctness, completeness

    def collect(self, evidence):
        correctness, completeness = evidence
        with contextlib.redirect_stdout(io.StringIO()) as output:
            collector.main([
                "--correctness-dir", str(correctness), "--completeness-dir", str(completeness),
                "--coverage", str(self.coverage),
            ])
        return output.getvalue()

    def mark_reviewed(self):
        rows = self.read_rows()
        reviews = {
            canonical: ("confirmed dual-track" if slug.startswith("as_ref")
                        else "confirmed correctness; completeness remains blocked")
            for slug, canonical in self.canonical.items()
        }
        for row in rows:
            if row["canonical_api"] in reviews:
                row["independent_review"] = reviews[row["canonical_api"]]
        self.write_rows(rows)
        return reviews

    def borrowed_reviews(self):
        return {row["canonical_api"]: row["independent_review"] for row in self.read_rows()
                if row["canonical_api"] in self.canonical.values()}

    def test_inline_cow_registration_preserves_reviewed_borrowed_inputs(self):
        self.collect(self.make_evidence("reviewed"))
        reviews = self.mark_reviewed()
        expanded = ENTRYPOINT + (
            "\npub mod cow {\n"
            "    #![cfg(not(no_global_oom_handling))]\n"
            "    pub mod observation;\n"
            "    pub mod conversions;\n"
            "}\n"
        )
        self.collect(self.make_evidence("cow", extra=True, entrypoint=expanded))
        self.assertEqual(self.borrowed_reviews(), reviews)

    def test_extra_checker_targets_and_other_rows_are_preserved(self):
        before = self.read_rows()
        output = self.collect(self.make_evidence("expanded", extra=True))
        after = self.read_rows()
        self.assertIn("138 canonical APIs", output)
        self.assertIn("4 source bodies verified", output)
        self.assertEqual(len(after), 138)
        self.assertEqual([row["canonical_api"] for row in before],
                         [row["canonical_api"] for row in after])
        for old, new in zip(before, after):
            if old["canonical_api"] not in self.canonical.values():
                self.assertEqual(old, new)
        self.assertEqual(self.coverage.read_text().splitlines()[0], "\t".join(COLUMNS))

    def test_unchanged_reviews_survive_new_runs_and_cow_registration(self):
        self.collect(self.make_evidence("reviewed"))
        reviews = self.mark_reviewed()
        expanded = ENTRYPOINT.replace("    pub mod borrowed;", "    pub mod borrowed;\n    pub mod cow;")
        output = self.collect(self.make_evidence("expanded", extra=True, entrypoint=expanded))
        self.assertEqual(self.borrowed_reviews(), reviews)
        self.assertIn("4 independent review conclusions preserved", output)

    def test_unchanged_historical_runs_can_be_reused_after_adding_cow(self):
        evidence = self.make_evidence("reviewed")
        self.collect(evidence)
        reviews = self.mark_reviewed()
        self.write("specs/lib.rs", ENTRYPOINT.replace(
            "    pub mod borrowed;", "    pub mod borrowed;\n    pub mod cow;"))
        self.write("specs/vec/cow.rs", "// new independent module\n")
        self.collect(evidence)
        self.assertEqual(self.borrowed_reviews(), reviews)

    def test_changed_candidate_dependency_or_baseline_invalidates_reviews(self):
        for change in (
            {"candidate": "changed"}, {"dependency": "changed"}, {"baseline": "changed"},
            {"entrypoint": ENTRYPOINT.replace("allocator_api", "allocator_api, another_feature")},
            {"build_args": ["--cfg", "changed"]},
        ):
            with self.subTest(change=change):
                rows = self.read_rows()
                for row in rows:
                    if row["canonical_api"] in self.canonical.values():
                        row["independent_review"] = "pending"
                self.write_rows(rows)
                self.collect(self.make_evidence("reviewed"))
                self.mark_reviewed()
                self.collect(self.make_evidence("changed", **change))
                self.assertEqual(set(self.borrowed_reviews().values()), {"pending"})

    def test_changed_correctness_input_invalidates_only_its_review(self):
        self.collect(self.make_evidence("reviewed"))
        reviews = self.mark_reviewed()
        evidence = self.make_evidence("changed")
        vir = evidence[0] / "as_ref_vec/crate.vir"
        vir.write_text(vir.read_text() + " changed source proof")
        self.collect(evidence)
        reviews[self.canonical["as_ref_vec"]] = "pending"
        self.assertEqual(self.borrowed_reviews(), reviews)

    def test_missing_prior_evidence_fails_without_rewriting_coverage(self):
        old = self.make_evidence("reviewed")
        self.collect(old)
        self.mark_reviewed()
        before = self.coverage.read_bytes()
        (old[1] / "analyze-run/toolchains.json").unlink()
        with self.assertRaises(FileNotFoundError):
            self.collect(self.make_evidence("new"))
        self.assertEqual(self.coverage.read_bytes(), before)

    def test_missing_prior_dependency_snapshot_fails_explicitly(self):
        old = self.make_evidence("reviewed")
        self.collect(old)
        self.mark_reviewed()
        before = self.coverage.read_bytes()
        (old[1] / "analyze-run/workspace/shared.rs").unlink()
        with self.assertRaises(FileNotFoundError):
            self.collect(self.make_evidence("new"))
        self.assertEqual(self.coverage.read_bytes(), before)

    def test_missing_prior_entrypoint_identity_fails_explicitly(self):
        old = self.make_evidence("reviewed")
        self.collect(old)
        self.mark_reviewed()
        before = self.coverage.read_bytes()
        snapshot_path = old[1] / "analyze-run/snapshot.json"
        snapshot = json.loads(snapshot_path.read_text())
        del snapshot["payload"]["files"]["lib.rs"]
        self.write_json(snapshot_path, snapshot)
        with self.assertRaisesRegex(AssertionError, "Missing snapshot input: lib.rs"):
            self.collect(self.make_evidence("new"))
        self.assertEqual(self.coverage.read_bytes(), before)

    def test_missing_borrowed_result_is_not_hidden_by_extra_targets(self):
        evidence = self.make_evidence("expanded", extra=True)
        summary_path = evidence[1] / "analyze.json"
        summary = json.loads(summary_path.read_text())
        summary["results"].pop(0)
        self.write_json(summary_path, summary)
        before = self.coverage.read_bytes()
        with self.assertRaises(AssertionError):
            self.collect(evidence)
        self.assertEqual(self.coverage.read_bytes(), before)

    def test_changed_current_dependency_rejects_stale_results(self):
        evidence = self.make_evidence("reviewed")
        self.collect(evidence)
        self.mark_reviewed()
        before = self.coverage.read_bytes()
        self.write("specs/shared.rs", "// dependency changed after the proof\n")
        with self.assertRaisesRegex(AssertionError, "shared.rs"):
            self.collect(evidence)
        self.assertEqual(self.coverage.read_bytes(), before)

    def test_missing_coverage_is_not_reconstructed(self):
        evidence = self.make_evidence("new")
        self.coverage.unlink()
        with self.assertRaises(FileNotFoundError):
            self.collect(evidence)
        self.assertFalse(self.coverage.exists())

    def test_duplicate_coverage_identity_is_rejected(self):
        evidence = self.make_evidence("new")
        rows = self.read_rows()
        rows[0] = rows[1].copy()
        self.write_rows(rows)
        before = self.coverage.read_bytes()
        with self.assertRaises(AssertionError):
            self.collect(evidence)
        self.assertEqual(self.coverage.read_bytes(), before)

    def test_historical_artifacts_are_never_overwritten(self):
        evidence = self.make_evidence("new")
        artifact = self.write(evidence[1] / "as_ref_vec.rs", "// historical artifact\n")
        before = self.coverage.read_bytes()
        with self.assertRaisesRegex(FileExistsError, "historical evidence"):
            self.collect(evidence)
        self.assertEqual(artifact.read_text(), "// historical artifact\n")
        self.assertEqual(self.coverage.read_bytes(), before)
        self.assertFalse((evidence[1] / "as_ref_slice.rs").exists())


if __name__ == "__main__":
    unittest.main()
