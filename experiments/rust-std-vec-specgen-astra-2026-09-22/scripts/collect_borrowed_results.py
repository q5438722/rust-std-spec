"""Update borrowed evidence in an existing coverage TSV, leaving other rows intact.

For a separate output, copy the coverage TSV first and pass it with --coverage.
Reviewed rows must retain their original completeness directory (analyze.json and
its saved run) and correctness logs so their input identities can be compared.
"""

import argparse
import csv
import io
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPLETENESS = ROOT / "proofs/completeness/vec"
SPECDET = "/home/chentianyu/spec-determinism-tool/.venv/bin/specdet"
TARGETS = {
    "core::convert::AsRef<alloc::vec::Vec<T, A>>":
        ("as_ref_vec", "<Vec<T, A> as AsRef<Vec<T, A>>>::as_ref", "(r1)@ =~= (r2)@"),
    "core::convert::AsRef<[T]>":
        ("as_ref_slice", "<Vec<T, A> as AsRef<[T]>>::as_ref", "r1 =~= r2"),
    "core::convert::AsMut<alloc::vec::Vec<T, A>>":
        ("as_mut_vec", "<Vec<T, A> as AsMut<Vec<T, A>>>::as_mut", None),
    "core::convert::AsMut<[T]>":
        ("as_mut_slice", "<Vec<T, A> as AsMut<[T]>>::as_mut", None),
}
INVENTORY_COLUMNS = (
    "module", "source", "docstrings", "vstd_coverage", "vstd_specs", "views",
)


def read_json(path):
    return json.loads(path.read_text())


def relative(path):
    path = Path(path).resolve()
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def source_ref(source):
    return f"{source['path']}:{source['start_line']}-{source['end_line']}"


def result_for(summary, target):
    matches = [result for result in summary["results"]
               if result["target"]["qualified_name"] == f"vec/borrowed.rs::vec::borrowed::{target}"]
    assert len(matches) == 1, target
    return matches[0]


def compact(text):
    return re.sub(r"\s+", "", text)


def entrypoint_context(text):
    # Registering a sibling module does not change the borrowed contracts.
    registrations = r"(?:\s*#!?\[[^\n]*\]|\s*pub mod (?!borrowed\b)\w+;|\s+)*"
    text = re.sub(r"(?m)^pub mod (?!vec\b)\w+\s*\{" + registrations + r"\}\s*\n?", "", text)
    return re.sub(r"(?m)^[ \t]*pub mod (?!borrowed\b)\w+;[ \t]*\n?", "", text).strip()


def run_inputs(summary):
    directory = ROOT / summary["run_dir"]
    snapshot = read_json(directory / "snapshot.json")["payload"]["files"]
    for file in ("lib.rs", "vec/borrowed.rs"):
        assert file in snapshot, f"Missing snapshot input: {file}"
    toolchains = read_json(directory / "toolchains.json")
    config = read_json(directory / "effective-config.json")["payload"]
    toolchain = config["toolchain"]
    identity = toolchains["payload"]
    return {
        "files": snapshot,
        "workspace": directory / "workspace",
        "baseline": (
            toolchains["producer_version"],
            {key: identity[key] for key in (
                "executable_digest", "rust_toolchain", "version", "z3_python",
            )},
            config["build"],
            toolchain["extra_args"],
            {key: value for key, value in toolchain["environment"].items() if key != "TMPDIR"},
            config["observation_policy"],
        ),
    }


def unchanged_inputs(previous, current):
    if previous["baseline"] != current["baseline"]:
        return False
    for file, digest in previous["files"].items():
        if file not in current["files"]:
            return False
        before = (previous["workspace"] / file).read_bytes()
        after = (current["workspace"] / file).read_bytes()
        if file == "lib.rs":
            if entrypoint_context(before.decode()) != entrypoint_context(after.decode()):
                return False
        elif digest != current["files"][file] or before != after:
            return False
    return True


def reviewed_inputs_unchanged(previous, updated, target, current, initial_result):
    directory = (ROOT / previous["completeness_file"]).parent
    summary = read_json(directory / "analyze.json")
    result = result_for(summary, target)
    inputs = run_inputs(summary)
    file = result["target"]["file"]
    assert inputs["files"][file] == result["target"]["source_digest"], file
    previous_log = ROOT / previous["correctness_result"].rsplit("; ", 1)[1]
    current_log = ROOT / updated["correctness_result"].rsplit("; ", 1)[1]
    previous_vir = (previous_log.with_suffix("") / "crate.vir").read_bytes()
    current_vir = (current_log.with_suffix("") / "crate.vir").read_bytes()
    return (
        result["target"]["source_digest"] == initial_result["target"]["source_digest"]
        and unchanged_inputs(inputs, current)
        and previous_vir == current_vir
        and all(previous[column] == updated[column] for column in INVENTORY_COLUMNS)
        and previous["completeness_result"] == updated["completeness_result"]
    )


def check_readonly(result, expected_observation, declaration):
    assert result["status"] == "completed" and result["verdict"] == "deterministic"
    assert result["baseline"]["status"] == "unsat"
    assert result["baseline"]["constraints"] == []
    proofs = result["proofs"]
    assert len(proofs) == 1 and proofs[0]["status"] == "verified"
    assert proofs[0]["verified_goals"] > 0
    proof = proofs[0]
    revisions = Path(proof["artifact"]).parents[1] / "revisions/0"
    contract = read_json(revisions / "contract.json")["payload"]["native"]["function_spec"]
    assert compact(contract["generics_decl"]) == "<'a,T,A:Allocator>"
    assert contract["requires"] == []
    assert len(contract["params"]) == 1
    param = contract["params"][0]
    assert param["name"] == "vec" and param["is_ref"] and not param["is_mut_ref"]
    assert compact(param["type"]["name"]) == "Vec<T,A>"
    expected_return = "&Vec<T,A>" if "AsRef<Vec" in contract["name"] else "&[T]"
    assert compact(contract["return_type"]["name"]) == expected_return
    clauses = declaration.split("ensures", 1)[1].rsplit(";", 1)[0]
    assert compact(",".join(contract["ensures"]) + ",") == compact(clauses)
    observation = read_json(revisions / "observation-plan.json")["payload"]
    assert observation["policy"] == "verus-strict-v1"
    comparisons = observation["native"]["comparisons"]
    assert len(comparisons) == 1
    assert comparisons[0]["dimension"] == "return"
    assert comparisons[0]["expression"] == expected_observation
    obligation = read_json(revisions / "obligation.json")["payload"]
    assert obligation["trusted_translation"] is True
    query = Path(result["baseline"]["artifact"]).read_text()
    guards = [
        "g_vec_leneq!", "g_vec_lenrng!", "g_r1_leneq!", "g_r1_lenrng!",
        "g_r2_leneq!", "g_r2_lenrng!", "g_neq_tuple!",
    ]
    query_command = "(check-sat-assuming (" + " ".join(f"(not {guard})" for guard in guards) + "))"
    assert query.count("(check-sat") == 1
    assert query.rstrip().endswith(query_command)
    assert not result["search"]
    return proof, revisions


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--correctness-dir", type=Path, default=ROOT / "proofs/correctness/vec")
    parser.add_argument("--completeness-dir", type=Path, default=COMPLETENESS)
    parser.add_argument("--coverage", type=Path, default=ROOT / "inventory/coverage.tsv",
                        help="Existing coverage TSV to update in place; copy it first for a separate output")
    args = parser.parse_args(argv)
    correctness_dir = args.correctness_dir.resolve()
    completeness_dir = args.completeness_dir.resolve()
    inventory = read_json(ROOT / "inventory/source_api.json")
    vstd = read_json(ROOT / "inventory/vstd_coverage.json")
    baseline = read_json(completeness_dir / "analyze.json")
    replay = read_json(completeness_dir / "replay.json")
    assert baseline["run_dir"] != replay["run_dir"]
    inputs = run_inputs(baseline)
    replay_inputs = run_inputs(replay)
    assert inputs["files"] == replay_inputs["files"], "Analysis and replay snapshots differ"
    assert inputs["baseline"] == replay_inputs["baseline"], "Analysis and replay baselines differ"
    for run in (inputs, replay_inputs):
        for file in run["files"]:
            saved = (run["workspace"] / file).read_bytes()
            current = (ROOT / "specs" / file).read_bytes()
            if file == "lib.rs":
                assert entrypoint_context(saved.decode()) == entrypoint_context(current.decode()), file
            else:
                assert saved == current, file
    code = (ROOT / "specs/vec/borrowed.rs").read_text()
    declarations = re.findall(r"pub assume_specification.*?\n;", code, re.DOTALL)
    assert len(declarations) == len(TARGETS)
    original = {api["canonical_id"]: api for api in inventory["apis"]}
    covered = {api["canonical_id"]: api for api in vstd["apis"]}
    assert original.keys() == covered.keys()
    assert len(original) == len(inventory["apis"]) == len(vstd["apis"])
    with args.coverage.open(newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        columns = reader.fieldnames
        rows = list(reader)
    assert len(rows) == len(original) == inventory["counts"]["stable_public_executable"]
    assert {row["canonical_api"] for row in rows} == original.keys()
    evidence = {item["id"]: item for item in vstd["evidence"]}
    views = {item["id"]: item for item in vstd["views"]}
    selected = 0
    retained_reviews = 0
    artifacts = []
    for row in rows:
        canonical = row["canonical_api"]
        api = covered[canonical]
        if api["source_module"] != "mod" or api["canonical_trait"] not in TARGETS:
            continue
        previous = row.copy()
        source_api = original[canonical]
        references = [*api["direct_spec_refs"], *api["compiler_hook_refs"],
                      *api["trait_contract_refs"], *api["concrete_spec_impl_refs"]]
        view_refs = []
        for name in api["view_dependencies"]:
            view = views[name]
            view_refs.extend(source_ref(evidence[ref]["source"]) for ref in view["definition_refs"])
            if not view["definition_refs"]:
                view_refs.append(f"inventory/vstd_coverage.json:views.{name} ({view['status']})")
        row.update({
            "module": api["source_module"],
            "source": source_ref(source_api["source"]),
            "docstrings": "; ".join(doc["ref"] for doc in source_api["docs"]),
            "vstd_coverage": api["coverage_class"],
            "vstd_specs": "; ".join(dict.fromkeys(source_ref(evidence[ref]["source"]) for ref in references)),
            "views": "; ".join(dict.fromkeys(view_refs)),
        })
        selected += 1
        slug, target, observation = TARGETS[api["canonical_trait"]]
        initial_result = result_for(baseline, target)
        replay_result = result_for(replay, target)
        for result, run in ((initial_result, inputs), (replay_result, replay_inputs)):
            assert result["target"]["source_digest"] == run["files"]["vec/borrowed.rs"]
        matches = [declaration for declaration in declarations if f"\n    {target}\n" in declaration]
        assert len(matches) == 1
        declaration = matches[0]
        correctness = relative(correctness_dir / slug)
        assert "verification results:: 1 verified, 0 errors" in (ROOT / f"{correctness}.log").read_text()
        build = relative(correctness_dir / f"build/lib{slug}.rlib")
        assert (ROOT / build).is_file()
        vir = (ROOT / correctness / "crate.vir").read_text()
        own_body = vir.split(f":name (Fun :path {slug}::{slug})", 1)[1]
        assert ":is_external_body false" in own_body
        assert ") :body (@" in own_body
        assert "core::convert::AsRef::as_ref" not in own_body
        assert "core::convert::AsMut::as_mut" not in own_body
        row.update({
            "project_spec": f"specs/vec/borrowed.rs:{initial_result['target']['line']}",
            "correctness_proof": f"proofs/correctness/vec/{slug}.rs",
            "correctness_command":
                f"bash scripts/with_baseline.sh env TMPDIR={relative(completeness_dir / 'tmp')} "
                f"toolchains/verus-x86-linux/verus proofs/correctness/vec/{slug}.rs "
                f"--edition=2021 --crate-type=lib --crate-name {slug} --compile --num-threads=1 "
                f"--trace --log-all --log-dir {correctness} "
                f"-o {build}",
            "correctness_result": f"1 verified, 0 errors; {correctness}.log",
            "completeness_file": relative(completeness_dir / f"{slug}.rs"),
            "completeness_command":
                f"bash scripts/with_baseline.sh env TMPDIR={relative(completeness_dir / 'tmp')} "
                f"{SPECDET} analyze --config {relative(completeness_dir / 'specdet.toml')} --json",
            "reexecution":
                f"bash scripts/with_baseline.sh env TMPDIR={relative(completeness_dir / 'tmp')} "
                f"{SPECDET} replay --run {relative(baseline['run_dir'])} "
                f"--reexecute --config {relative(completeness_dir / 'specdet.toml')} "
                f"--verus toolchains/verus-x86-linux/verus "
                f"--out {relative(completeness_dir / 'replay-runs')} --json",
            "issues": "issues/source-body-embedding.md",
            "independent_review": "pending",
        })
        if observation is not None:
            proof, revisions = check_readonly(initial_result, observation, declaration)
            check_readonly(replay_result, observation, declaration)
            artifacts.append((ROOT / row["completeness_file"], Path(proof["native"]["harness"]).read_bytes()))
            artifacts.append((completeness_dir / f"{slug}.smt2",
                              Path(initial_result["baseline"]["artifact"]).read_bytes()))
            row["completeness_result"] = "deterministic; baseline=unsat; verified_goals=1; fresh replay=unsat"
            row["native_query"] = relative(completeness_dir / f"{slug}.smt2")
            row["observation_plan"] = relative(revisions / "observation-plan.json")
        else:
            for result in (initial_result, replay_result):
                assert result["status"] == "failed" and result["verdict"] == "not_evaluated"
                assert result["baseline"] is None and result["proofs"] == []
                assert [d["code"] for d in result["diagnostics"]] == ["unsupported_mutable_return"]
            input_copy = (
                "#![feature(allocator_api)]\n\n"
                "use std::alloc::Allocator;\nuse vstd::prelude::*;\n\n"
                "// Exact input declaration; specdet stops before proof/query generation.\n"
                "verus! {\n\n" + declaration + "\n\n}\n"
            )
            artifacts.append((ROOT / row["completeness_file"], input_copy.encode()))
            row["completeness_result"] = "not_evaluated; unsupported_mutable_return; fresh replay=same"
            row["native_query"] = "not_generated: extraction rejected mutable return"
            row["observation_plan"] = "not_generated"
            row["issues"] += "; issues/specdet-mutable-return.md"
        if previous["independent_review"] not in ("", "pending", "not_requested"):
            if reviewed_inputs_unchanged(previous, row, target, inputs, initial_result):
                row["independent_review"] = previous["independent_review"]
                retained_reviews += 1
    assert selected == len(TARGETS)
    text = io.StringIO()
    writer = csv.DictWriter(text, fieldnames=columns, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    for path, content in artifacts:
        if path.exists() and path.read_bytes() != content:
            raise FileExistsError(f"Refusing to overwrite historical evidence: {path}")
    for path, content in artifacts:
        if not path.exists():
            path.write_bytes(content)
    args.coverage.write_text(text.getvalue())
    readonly = sum(observation is not None for _, _, observation in TARGETS.values())
    print(f"{len(rows)} canonical APIs; {selected} source bodies verified; "
          f"{readonly} current dual-track results; {selected - readonly} mutable completeness failures retained; "
          f"{retained_reviews} independent review conclusions preserved.")
    print(f"Analysis: {relative(baseline['run_dir'])}")
    print(f"Fresh replay: {relative(replay['run_dir'])}")


if __name__ == "__main__":
    main()
