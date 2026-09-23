"""Check isolated u8 instances of complete and clause-deleted mutable split contracts."""

import argparse
import json
from pathlib import Path
import re
import shutil

from scripts.check_singleton_writeback import run


ROOT = Path(__file__).resolve().parents[1]
CHECKER = Path("/home/chentianyu/spec-determinism-tool/.venv/bin/specdet")
VERUS = ROOT / "toolchain/verus-x86-linux/verus"
POST = Path("specs/slice/mutable_splits_post.rs")
APIS = ("split_first_mut", "split_last_mut")


def witness(api, omitted):
    first = api == "split_first_mut"
    initial = "seq![10u8, 40, 30]"
    caller = "Some((7u8, seq![8u8, 9]))"
    element = "10u8" if first else "30u8"
    remainder = "seq![40u8, 30]" if first else "seq![10u8, 40]"
    returned = "seq![7u8, 8, 9]" if first else "seq![8u8, 9, 7]"
    left = f"(Some(({element}, {remainder})), {returned})"
    if omitted == "initial-element":
        right = f"(Some((99u8, {remainder})), {returned})"
    elif omitted == "initial-remainder":
        changed = "seq![30u8, 40]" if first else "seq![40u8, 10]"
        right = f"(Some(({element}, {changed})), {returned})"
    elif omitted == "final-owner":
        right = f"(Some(({element}, {remainder})), seq![90u8, 91, 92])"
    elif omitted == "empty-owner":
        initial, caller = "Seq::<u8>::empty()", "None"
        left = "(Option::<(u8, Seq<u8>)>::None, Seq::<u8>::empty())"
        right = "(Option::<(u8, Seq<u8>)>::None, seq![99u8])"
    else:
        raise ValueError(f"Unknown omitted observation: {omitted}")
    return f"""
pub proof fn omitted_observation_has_two_outputs()
    ensures
        post::{api}_post({initial}, {caller}, {left}),
        post::{api}_post({initial}, {caller}, {right}),
        {left} != {right},
{{
    assert(seq![10u8, 40, 30].subrange(1, 3) =~= seq![40u8, 30]);
    assert(seq![10u8, 40, 30].subrange(0, 2) =~= seq![10u8, 40]);
}}
"""


def check(output):
    output.mkdir(parents=True, exist_ok=False)
    original_post = (ROOT / POST).read_text()
    results = []
    for api in APIS:
        relative = Path(f"proofs/completeness/slice/inputs/{api}.rs")
        original_input = (ROOT / relative).read_text()
        state_import = '#[path = "../mutable_splits_state.rs"]\nmod state;'
        pure_import = '#[path = "../../../../specs/slice/mutable_splits_post.rs"]\nmod post;'
        proof_call = (
            "    proof {\n"
            "        state::all_caller_writes(input_initial@, caller_final@);\n"
            "    }\n"
        )
        if original_input.count(state_import) != 1 or original_input.count(proof_call) != 1:
            raise ValueError(f"Analysis adapter changed: {relative}")
        pure_input = original_input.replace(state_import, pure_import).replace(
            proof_call, "",
        ).replace("state::post::", "post::")
        pure_input = re.sub(
            r"\bT\b", "u8",
            pure_input.replace(f"{api}_observation<T>(", f"{api}_observation("),
        )
        first = api == "split_first_mut"
        index = "0" if first else "input_initial.len() - 1"
        subrange = "1, input_initial.len() as int" if first else "0, input_initial.len() - 1"
        final = "seq![written] + written_remainder" if first else "written_remainder + seq![written]"
        for omitted, removed in (
            ("complete", ""),
            ("initial-element", f"            &&& value == input_initial[{index}]\n"),
            ("initial-remainder", f"            &&& remainder == input_initial.subrange({subrange})\n"),
            ("final-owner", f"            &&& observations.1 =~= {final}\n"),
            ("empty-owner", " && observations.1 =~= seq![]"),
        ):
            directory = output / api / omitted
            project = directory / "project"
            project.mkdir(parents=True)
            for dependency in (Path("specdet.toml"), Path("specs/slice/mod.rs")):
                destination = project / dependency
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / dependency, destination)
            match = re.search(
                rf"pub open spec fn {api}_post<T>.*?(?=\npub open spec fn|\n\}}\n\Z)",
                original_post, re.DOTALL,
            )
            if match is None:
                raise ValueError(f"Pure candidate not found: {api}")
            clause = match[0]
            if removed:
                if clause.count(removed) != 1:
                    raise ValueError(f"Observation clause changed: {api}/{omitted}")
                clause = clause.replace(removed, "", 1)
            changed_post = original_post[:match.start()] + clause + original_post[match.end():]
            (project / POST).write_text(changed_post)
            text = pure_input
            if omitted != "complete":
                end = text.rindex("\n}")
                text = text[:end] + witness(api, omitted) + text[end:]
            (project / relative).parent.mkdir(parents=True, exist_ok=True)
            (project / relative).write_text(text)
            code = run(
                [
                    VERUS, relative, "--crate-type", "lib", "--crate-name", "mutable_split_control",
                    "--compile", "--no-cheating", "--num-threads", "1",
                    "-o", directory / "libmutable_split_control.rlib",
                ],
                project, directory, "compile",
            )
            count = 1 if omitted == "complete" else 2
            expected = f"verification results:: {count} verified, 0 errors"
            if code != 0 or expected not in (directory / "compile.stdout").read_text():
                raise RuntimeError(f"Control or constructive witness did not verify: {directory}")
            code = run(
                [
                    CHECKER, "discover", "--config", "specdet.toml", "--verus", VERUS,
                    "--out", directory / "discovery", "--json",
                ],
                project, directory, "discover",
            )
            if code != 0:
                raise RuntimeError(f"Control discovery failed: {directory}")
            discovery = json.loads((directory / "discover.stdout").read_text())
            targets = [t for t in discovery["targets"] if t["name"] == f"{api}_observation"]
            if len(targets) != 1 or targets[0]["kind"] != "function":
                raise RuntimeError(f"Expected one control observation: {targets}")
            target = targets[0]
            selector = f'{target["file"]}:{target["name"]}@{target["line"]}'
            code = run(
                [
                    CHECKER, "analyze", "--config", "specdet.toml", "--verus", VERUS,
                    "--target", selector, "--out", directory / "runs", "--json",
                ],
                project, directory, "analyze",
            )
            report = json.loads((directory / "analyze.stdout").read_text())
            if len(report["results"]) != 1:
                raise RuntimeError(f"Expected one analyzed control: {directory}")
            result = report["results"][0]
            entry = {
                "api": api, "element_type": "u8", "omitted": omitted, "exit_code": code,
                "verdict": result["verdict"],
                "baseline": result["baseline"]["status"] if result["baseline"] else None,
                "compiled_functions": count,
                "constructive_witness": str(project / relative) if omitted != "complete" else None,
                "run_dir": report["run_dir"],
                "counterexample": result["counterexample"],
                "diagnostics": result["diagnostics"],
            }
            results.append(entry)
            (output / "results.json").write_text(json.dumps(results, indent=2) + "\n")
            print(f'{api}/{omitted}: {entry["verdict"]}, baseline {entry["baseline"]}', flush=True)
    for result in results:
        expected = "deterministic" if result["omitted"] == "complete" else "nondeterministic"
        if result["verdict"] != expected:
            raise RuntimeError(
                f'{result["api"]}/{result["omitted"]}: expected {expected}, got {result["verdict"]}; '
                "the separate compiled witness does not change the checker result"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    check(args.output_root.resolve())
