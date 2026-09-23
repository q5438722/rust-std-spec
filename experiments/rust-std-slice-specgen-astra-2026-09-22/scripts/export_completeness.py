"""Export checked evidence, preserving unselected API records and proofs."""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import shlex


ROOT = Path(__file__).resolve().parents[1]
APIS = ("len", "is_empty", "first", "split_first", "split_last", "last")
CHECKER = "/home/chentianyu/spec-determinism-tool/.venv/bin/specdet"
VERUS = "toolchain/verus-x86-linux/verus"
ENDPOINTS = ("first", "last")
SPLITS = ("split_first", "split_last")
PATTERNS = (*ENDPOINTS, *SPLITS)
PATTERN_IDS = {f"<[T]>::{api}" for api in PATTERNS}
PATTERN_SOURCE_FIELDS = (
    "correctness_proof", "correctness_command", "correctness_log",
    "correctness_result", "correctness_target_functions",
)
MUTABLE_ENDPOINTS = ("first_mut", "last_mut")
MUTABLE_CHECKER_LOGS = "logs/mutable-endpoints-proposal/completeness"
MUTABLE_STATE = "proofs/completeness/slice/mutable_endpoints_state.rs"
MUTABLE_POST = "specs/slice/mutable_endpoints.rs"
MUTABLE_DEPENDENCIES = (MUTABLE_STATE, MUTABLE_POST, "specs/slice/mod.rs", "specdet.toml")
MUTABLE_SPLITS = ("split_first_mut", "split_last_mut")
MUTABLE_SPLIT_CHECKER_LOGS = "logs/mutable-splits-proposal/completeness"
MUTABLE_SPLIT_STATE = "proofs/completeness/slice/mutable_splits_state.rs"
MUTABLE_SPLIT_POST = "specs/slice/mutable_splits_post.rs"
MUTABLE_SPLIT_BINDING = "specs/slice/mutable_splits.rs"
MUTABLE_SPLIT_DEPENDENCIES = (
    MUTABLE_SPLIT_STATE, MUTABLE_SPLIT_POST, "specs/slice/mod.rs", "specdet.toml",
)
MUTABLE_SPLIT_BEFORE = "logs/mutable-splits/adoption-before"
MUTABLE_SPLIT_STATE_LOGS = "logs/mutable-splits-proposal/value-state/initial"
MUTABLE_SPLIT_STATE_FUNCTIONS = (
    "first_candidate_correspondence", "last_candidate_correspondence", "caller_domain",
    "all_caller_writes", "first_full_return", "last_full_return", "value_state_comparison",
)
SPLIT_OFF_ENDPOINTS = ("split_off_first", "split_off_last")
SPLIT_OFF_POST = "specs/slice/split_off_post.rs"
SPLIT_OFF_BINDING = "specs/slice/split_off.rs"
SPLIT_OFF_STATE = "proofs/completeness/slice/split_off_state.rs"
SPLIT_OFF_BEFORE = "logs/split-off-endpoints/adoption-before"
SPLIT_OFF_CHECKER_LOGS = "logs/split-off-endpoints/direct"
SPLIT_OFF_DEPENDENCIES = (SPLIT_OFF_POST, "specs/slice/mod.rs", "specdet.toml")
SPLIT_OFF_SOURCE_LOGS = {
    "split_off_first": "logs/split-off-endpoints/return-state/split_off_first",
    "split_off_last": "logs/split-off-endpoints/correctness/split_off_last",
}
SPLIT_OFF_STATE_FUNCTIONS = (
    "first_candidate_correspondence", "last_candidate_correspondence", "all_initial_states",
    "first_reconstruction", "last_reconstruction", "complete_comparison",
)
DEFAULT_CHECKER_LOGS = {
    "default_shared": "logs/defaults/completeness/default_shared",
    "default_mut": "logs/defaults-redundancy/completeness/default_mut/selected",
}
SINGLETON_CHECKER_LOGS = {
    "from_ref": "logs/singletons/completeness/from_ref",
    "from_mut": "logs/singleton-writeback/completeness/from_mut-ghost-inputs",
}
ASCII_CHECKER_LOGS = {
    "make_ascii_uppercase": "logs/ascii-case/completeness/make_ascii_uppercase",
    "make_ascii_lowercase": "logs/ascii-case/completeness/make_ascii_lowercase",
}
ASCII_CORRECTNESS_LOGS = {
    "make_ascii_uppercase": "logs/ascii-case/rebinding/uppercase-initial",
    "make_ascii_lowercase": "logs/ascii-case/rebinding/lowercase-initial",
}
ASCII_CORRECTNESS_DEPENDENCIES = (
    "proofs/correctness/num/u8_ascii.rs",
    "proofs/correctness/num/u8_ascii_classify.rs",
    "specs/slice/ascii_post.rs",
)


def relative(path):
    return str(Path(path).relative_to(ROOT))


def checked_pattern_execution(logs, phase, command):
    receipt = json.loads((logs / f"{phase}-execution.json").read_text())
    recorded = (logs / f"{phase}-command.txt").read_text().strip()
    if (
        receipt["command"] != command or receipt["cwd"] != str(ROOT)
        or receipt["RUSTUP_HOME"] != "/home/chentianyu/.rustup"
        or receipt["returncode"] != 0 or receipt.get("error")
        or shlex.split(recorded) != ["RUSTUP_HOME=/home/chentianyu/.rustup", *command]
        or int((logs / f"{phase}.exit-code.txt").read_text()) != 0
        or (logs / f"{phase}.stderr").read_text().strip()
    ):
        raise ValueError(f"Unsuccessful or unexpected pattern execution: {logs}/{phase}")
    return recorded


def checked_pattern_run(api, phase, analyzed_run=None):
    group = "splits" if api in SPLITS else "endpoints"
    logs = ROOT / f"logs/{group}/completeness/{api}"
    report_path = logs / f"{phase}.json"
    report = json.loads(report_path.read_text())
    if (
        phase not in ("analyze", "replay")
        or report["schema_version"] != 1 or len(report["results"]) != 1
        or report["status"] != "completed" or report["exit_code"] != 0
        or report["diagnostics"] or report["counts"] != {"deterministic": 1}
        or (logs / f"{phase}.stdout").read_bytes() != report_path.read_bytes()
    ):
        raise ValueError(f"Unexpected pattern checker report: {report_path}")
    result = report["results"][0]
    source = f"proofs/completeness/slice/inputs/{api}.rs"
    selector = f"{source}:{api}@13"
    target = result["target"]
    expected_target = {
        "language": "verus", "file": source, "name": api, "line": 13,
        "qualified_name": f"{source}::source::{api}::<T>",
        "kind": "contract_declaration", "module": "",
        "source_digest": hashlib.sha256((ROOT / source).read_bytes()).hexdigest(),
    }
    if (
        target != expected_target or report["targets"] != [target]
        or f"pub assume_specification<T>[source::{api}::<T>]" not in
        (ROOT / source).read_text().splitlines()[12]
    ):
        raise ValueError(f"Unexpected pattern target or stale input: {report_path}")
    expected_diagnostics = [{
        "stage": "extract", "code": "contract_declaration",
        "message": (
            "This analysis concerns the declared contract, not a proof "
            "that an implementation satisfies it"
        ),
        "severity": "info", "details": {},
    }]
    if (
        result["status"] != "completed" or result["verdict"] != "deterministic"
        or result["baseline"] is None or result["baseline"]["status"] != "unsat"
        or result["baseline"]["role"] != "baseline" or result["baseline"]["constraints"]
        or result["baseline"]["reason"] or result["diagnostics"] != expected_diagnostics
        or len(result["proofs"]) != 1 or result["search"] is not None
        or result["analysis_kind"] != "concrete_determinism"
        or result["assistance"]["accepted_proposals"]
    ):
        raise ValueError(f"No successful original pattern completeness result: {report_path}")
    run = Path(report["run_dir"])
    output = logs / ("runs" if phase == "analyze" else "replays")
    if (
        run.parent != output or run.name != report["run_id"]
        or result["run_id"] != report["run_id"]
        or (phase == "replay" and (analyzed_run is None or run == analyzed_run))
    ):
        raise ValueError(f"Unexpected pattern run identity: {report_path}")
    command = (
        [CHECKER, "analyze", "--config", "specdet.toml", "--verus", str(ROOT / VERUS),
         "--target", selector, "--out", str(output), "--json"]
        if phase == "analyze" else
        [CHECKER, "replay", "--run", str(analyzed_run), "--reexecute",
         "--verus", str(ROOT / VERUS), "--out", str(output), "--json"]
    )
    checked_pattern_execution(logs, phase, command)
    manifest = json.loads((run / "manifest.json").read_text())["payload"]
    if manifest != {
        "run_id": report["run_id"], "status": "completed", "exit_code": 0,
        "parent_run": "" if phase == "analyze" else str(analyzed_run),
    }:
        raise ValueError(f"Pattern replay does not reexecute its analyzed run: {report_path}")
    config = json.loads((run / "effective-config.json").read_text())["payload"]
    project_root = ROOT if phase == "analyze" else Path(analyzed_run) / "workspace"
    if (
        config["selectors"] != [selector] or config["project_root"] != str(project_root)
        or config["output_dir"] != str(output) or config["language"] != "verus"
        or config["type_sources"] != ["specs/slice/mod.rs"]
        or config["build"]["adapter"] != "verus.single_file"
        or config["build"]["extra_args"] != ["--crate-type", "lib"]
        or config["toolchain"]["executable"] != str(ROOT / VERUS)
        or config["toolchain"]["extra_args"] != ["--num-threads", "1"]
        or config["toolchain"]["environment"] or not config["offline"]
        or config["assistance"] != {"mode": "off"}
        or config["analysis_kind"] != "concrete_determinism"
        or config["observation_policy"] != "verus-observable-v1"
    ):
        raise ValueError(f"Unexpected effective pattern selectors or configuration: {report_path}")
    snapshot = run / "workspace"
    snapshot_record = json.loads((run / "snapshot.json").read_text())["payload"]
    for path in (source, "specs/slice/mod.rs", "specdet.toml"):
        current = (ROOT / path).read_bytes()
        if (
            (snapshot / path).read_bytes() != current
            or snapshot_record["files"][path] != hashlib.sha256(current).hexdigest()
        ):
            raise ValueError(f"Current input differs from the checked snapshot: {path}")
    proof = result["proofs"][0]
    native = proof["native"]
    if (
        proof["status"] != "verified" or proof["verified_goals"] != 1
        or proof["diagnostics"] or native["baseline"] is not True
    ):
        raise ValueError(f"Expected one verified pattern baseline goal: {report_path}")
    comparison = native["det_spec"]
    policy = comparison["equal_policy"]
    return_type = "Option<(&T, &[T])>" if api in SPLITS else "Option<&T>"
    payload_equal = (
        "((r1->Some_0.0 == r2->Some_0.0) && (r1->Some_0.1 =~= r2->Some_0.1))"
        if api in SPLITS else "(r1->Some_0 == r2->Some_0)"
    )
    expected_equal = (
        "// Generated equal-fn for determinism check.\n"
        "// Policy: errs_equivalent=True, opaque_ok=False\n"
        f"spec fn {comparison['equal_fn_name']}<T>(r1: {return_type}, r2: {return_type}) -> bool {{\n"
        "    (((r1 is Some) == (r2 is Some)) && "
        f"((r1 is Some) ==> {payload_equal}))\n}}"
    )
    if (
        comparison["equal_arg_pairs"] != [{"lhs": "r1", "rhs": "r2"}]
        or comparison["equal_fn_def"] != expected_equal
        or comparison["equal_fn_name"] != native["fn_det"] + "_equal"
        or comparison["check_fn_name"] != native["fn_det"]
        or comparison["generics_decl"] != "<T>" or comparison["where_decl"]
        or policy["source"] != "verus-observable-v1" or policy["custom_body"] is not None
        or policy["ignore_fields"] or policy["opaque_ok"] or policy["opaque_types"]
        or policy["compare_raw_pointers"] or result["coverage"]["ignored_dimensions"]
    ):
        raise ValueError(f"The Option variant or complete ordered return value is not compared: {report_path}")
    parameters = f"slice: &[T], r1: {return_type}, r2: {return_type}"
    expected_template = (
        f"proof fn {native['fn_det']}<T>({parameters})\n"
        "    ensures\n"
        "        ({\n"
        f"            &&& (contracts::{api}_post(slice, r1))\n"
        f"            &&& (contracts::{api}_post(slice, r2))\n"
        f"        }}) ==> {comparison['equal_fn_name']}::<T>(r1, r2),\n"
        "{\n{ASSUMES}}"
    )
    if comparison["det_check_template"] != expected_template:
        raise ValueError(f"Unexpected premises in the pattern determinism obligation: {report_path}")
    guards = ["g_slice_leneq", "g_slice_lenrng"]
    guard_parameters = (
        "g_slice_leneq: bool, k_slice_leneq: nat, g_slice_lenrng: bool, "
        "k_slice_lenrng_lo: nat, k_slice_lenrng_hi: nat, "
    )
    assumptions = (
        "    if g_slice_leneq { assume(slice.len() == k_slice_leneq); }\n"
        "    if g_slice_lenrng { assume(slice.len() >= k_slice_lenrng_lo "
        "&& slice.len() <= k_slice_lenrng_hi); }\n"
    )
    for value in ("r1", "r2"):
        guards.append(f"g_{value}_is_Some")
        guard_parameters += f"g_{value}_is_Some: bool, "
        assumptions += f"    if g_{value}_is_Some {{ assume({value} is Some); }}\n"
        if api in SPLITS:
            remainder = f"{value}__Some_0_1"
            guards.extend((f"g_{remainder}_leneq", f"g_{remainder}_lenrng"))
            guard_parameters += (
                f"g_{remainder}_leneq: bool, k_{remainder}_leneq: nat, "
                f"g_{remainder}_lenrng: bool, k_{remainder}_lenrng_lo: nat, "
                f"k_{remainder}_lenrng_hi: nat, "
            )
            assumptions += (
                f"    if g_{remainder}_leneq {{ assume({value} is Some); "
                f"assume({value}->Some_0.1.len() == k_{remainder}_leneq); }}\n"
                f"    if g_{remainder}_lenrng {{ assume({value} is Some); "
                f"assume({value}->Some_0.1.len() >= k_{remainder}_lenrng_lo "
                f"&& {value}->Some_0.1.len() <= k_{remainder}_lenrng_hi); }}\n"
            )
        guards.append(f"g_{value}_is_None")
        guard_parameters += f"g_{value}_is_None: bool, "
        assumptions += f"    if g_{value}_is_None {{ assume({value} is None); }}\n"
    guards.append("g_neq_tuple")
    guard_parameters += "g_neq_tuple: bool, "
    assumptions += f"    if g_neq_tuple {{ assume(!{comparison['equal_fn_name']}::<T>(r1, r2)); }}\n"
    guarded = expected_template.replace(
        f"({parameters})", f"({guard_parameters}{parameters})", 1,
    ).replace("{ASSUMES}", assumptions)
    input_text = (ROOT / source).read_text()
    harness = Path(native["harness"])
    attempt = Path(proof["artifact"])
    worktree = attempt / "worktree"
    entrypoint = str(worktree / source)
    query = Path(result["baseline"]["artifact"])
    if (
        not attempt.is_relative_to(run / "targets")
        or harness != attempt / "harness.rs" or query != attempt / "query/originalC.smt2"
        or native["worktree"] != str(worktree) or native["source"] != entrypoint
        or native["entrypoint"] != entrypoint or native["crate_entrypoint"] != entrypoint
        or native["logs"] != str(attempt / "verifier/logs")
        or native["module"] or native["crate"] != api
        or not input_text.endswith(";\n}\n")
        or harness.read_text() != input_text[:-2] + f"\n{expected_equal}\n\n{guarded}\n\n}}\n"
        or harness.read_bytes() != Path(entrypoint).read_bytes()
        or hashlib.sha256(harness.read_bytes()).hexdigest() != native["harness_digest"]
    ):
        raise ValueError(f"Unexpected actual pattern native harness: {report_path}")
    for path in ("specs/slice/mod.rs", "specdet.toml"):
        if (worktree / path).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Current input differs from the native worktree: {path}")
    query_text = query.read_text()
    checks = [line.strip() for line in query_text.splitlines() if line.lstrip().startswith("(check-sat")]
    declarations = re.findall(r"^\(declare-fun (g_\S+)! \(\) Bool\)$", query_text, re.MULTILINE)
    expected_check = "(check-sat-assuming (" + " ".join(f"(not {guard}!)" for guard in guards) + "))"
    if checks != [expected_check] or sorted(declarations) != sorted(guards):
        raise ValueError(f"The original query did not disable every search guard: {query}")
    invocations = native["invocations"]
    if len(invocations) != 1:
        raise ValueError(f"Expected one pattern verifier invocation: {report_path}")
    invocation = invocations[0]
    process = invocation["process"]
    if (
        invocation["function"] != native["fn_det"] or invocation["module"]
        or invocation["role"] != "determinism" or invocation["status"] != "verified"
        or invocation["verified_goals"] != 1 or process["returncode"] != 0
        or process["timed_out"]
        or process["command"] != [
            str(ROOT / VERUS), entrypoint, "--crate-type", "lib", "--log-all",
            "--log-dir", native["logs"], "--num-threads", "1",
            "--verify-root", "--verify-function", native["fn_det"],
        ]
        or process["stdout"].strip() !=
        "verification results:: 1 verified, 0 errors (partial verification with `--verify-*`)"
        or process["stderr"].strip() != "note: verifying root module (selected functions)"
    ):
        raise ValueError(f"Unexpected pattern verifier invocation: {report_path}")
    return report, result, native


def checked_pattern_source(api):
    """Return source-only cells after checking the compiled proof and both native runs."""
    if api not in PATTERNS:
        raise ValueError("Select first, last, split_first or split_last")
    group = "splits" if api in SPLITS else "endpoints"
    logs = ROOT / f"logs/{group}/correctness/{api}"
    source = f"proofs/correctness/slice/{api}.rs"
    output = logs / f"libslice_{api}.rlib"
    command = checked_pattern_execution(logs, "verus", [
        str(ROOT / VERUS), source, "--crate-type", "lib", "--crate-name", f"slice_{api}",
        "--compile", "--no-cheating", "--num-threads", "1", "--log-all",
        "--log-dir", str(logs / "queries"), "-o", str(output),
    ])
    if (
        (logs / "verus.stdout").read_text().strip() != "verification results:: 3 verified, 0 errors"
        or output.stat().st_size == 0
    ):
        raise ValueError(f"No successful compiled pattern source proof for {api}")
    for path in (source, "specs/slice/mod.rs"):
        if (logs / "inputs" / path).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Current source differs from the checked source proof: {path}")
    for module, functions in (
        ("root", [f"slice_{api}::{api}"]),
        ("contracts", [f"slice_{api}::contracts::{name}" for name in ("scalar_domain", "empty_results")]),
    ):
        query = (logs / "queries" / f"{module}.smt2").read_text()
        transcript = (logs / "queries" / f"{module}.smt_transcript").read_text()
        if (
            re.findall(r"^;; Function-Def (.+)$", query, re.MULTILINE) != functions
            or len(re.findall(r"^\s*\(check-sat\)\s*$", query, re.MULTILINE)) != len(functions)
            or len(re.findall(r"^\(check-sat\)$", transcript, re.MULTILINE)) != len(functions)
            or re.findall(r"^(?:unsat|sat|unknown)$", transcript, re.MULTILINE) != ["unsat"] * len(functions)
        ):
            raise ValueError(f"Missing successful pattern target or consistency queries: {api}/{module}")
    analyzed, result, native = checked_pattern_run(api, "analyze")
    _, replay_result, replay_native = checked_pattern_run(api, "replay", Path(analyzed["run_dir"]))
    if (
        Path(native["harness"]).read_bytes() != Path(replay_native["harness"]).read_bytes()
        or Path(result["baseline"]["artifact"]).read_bytes() !=
        Path(replay_result["baseline"]["artifact"]).read_bytes()
    ):
        raise ValueError(f"Pattern replay changed the native harness or original query: {api}")
    correspondence = (
        "reviewed pattern-to-length/index/split_at conversion; trusts upstream slice length/index/"
        "split_at contracts and Seq view, not metadata or split_at implementation verification; "
        if api in SPLITS else
        "reviewed pattern-to-length/index conversion; trusts upstream slice length/index "
        "contracts and Seq view, not metadata implementation verification; "
    )
    return {
        "correctness_proof": source,
        "correctness_command": command,
        "correctness_log": relative(logs / "verus.stdout"),
        "correctness_result": (
            "verified and compiled with --no-cheating; 1 target + 2 imported consistency lemmas; "
            + correspondence + "final implementation review pending"
        ),
        "correctness_target_functions": "1",
    }


def pattern_coverage():
    coverage = ROOT / "inventory/coverage.tsv"
    text = coverage.read_bytes().decode()
    stream = io.StringIO(text, newline="")
    reader = csv.reader(stream, delimiter="\t", strict=True)
    fields = next(reader)
    end = stream.tell()
    records = [text[:end]]
    rows = {}
    if (
        len(set(fields)) != len(fields)
        or not {*PATTERN_SOURCE_FIELDS, "canonical_id", "issues", "independent_review"} <= set(fields)
    ):
        raise ValueError("Invalid existing pattern coverage columns")
    for values in reader:
        start, end = end, stream.tell()
        if len(values) != len(fields):
            raise ValueError("Invalid existing pattern coverage row")
        row = dict(zip(fields, values))
        if not row["canonical_id"] or row["canonical_id"] in rows:
            raise ValueError("Duplicate or missing canonical identity in existing coverage")
        rows[row["canonical_id"]] = row
        records.append(text[start:end])
    with (ROOT / "inventory/apis.tsv").open() as source:
        identities = [row["canonical_id"] for row in csv.DictReader(source, delimiter="\t")]
    if (
        not all(identities) or len(set(identities)) != len(identities)
        or set(identities) != rows.keys()
    ):
        raise ValueError("Existing coverage and source inventory identities differ")
    return fields, rows, records


def pattern_evidence(apis):
    if not apis or len(set(apis)) != len(apis) or not set(apis) <= set(PATTERNS):
        raise ValueError("Select distinct APIs from first, last, split_first and split_last")
    _, rows, _ = pattern_coverage()
    evidence = {}
    for api in apis:
        identity = f"<[T]>::{api}"
        if identity not in rows:
            raise ValueError(f"Missing pattern source identity: {identity}")
        row = rows[identity]
        if (
            "issues/V-SLICE-PATTERN.md" not in row["issues"].split(";")
            or row["independent_review"] != "pending"
        ):
            raise ValueError(f"Pattern source issue and pending final review must be retained: {api}")
        evidence[identity] = {
            key: value for key, value in row.items()
            if key not in ("canonical_id", "source_span", "doc_spans", "existing_vstd_coverage")
        }
        evidence[identity].update(checked_pattern_source(api))
    return evidence


def updated_coverage(evidence, update_fields):
    fields, rows, records = pattern_coverage()
    if not evidence.keys() <= rows.keys() or not set(update_fields) <= set(fields):
        raise ValueError("Unknown selected coverage identity or field")
    for index, (identity, row) in enumerate(rows.items(), start=1):
        if identity not in evidence:
            continue
        if any(
            row[key] != value for key, value in evidence[identity].items()
            if key not in update_fields
        ):
            raise ValueError("Existing coverage changed during validation")
        # Retain the raw TSV cells, including unrelated quoting and line endings.
        cells = list(re.finditer(r'(?:^|\t)("(?:[^"]|"")*"|[^\t\r\n]*)', records[index]))
        if len(cells) != len(fields):
            raise ValueError("Cannot preserve existing pattern coverage cells")
        for field_index in reversed(range(len(fields))):
            field = fields[field_index]
            if field not in update_fields:
                continue
            encoded = io.StringIO(newline="")
            csv.writer(encoded, delimiter="\t", lineterminator="\n").writerow([evidence[identity][field]])
            start, end = cells[field_index].span(1)
            records[index] = records[index][:start] + encoded.getvalue()[:-1] + records[index][end:]
    return "".join(records).encode(), len(rows)


def export_pattern_sources(evidence):
    contents, count = updated_coverage(evidence, PATTERN_SOURCE_FIELDS)
    (ROOT / "inventory/coverage.tsv").write_bytes(contents)
    label = "split" if evidence.keys() <= {f"<[T]>::{api}" for api in SPLITS} else "endpoint"
    print(
        f"Updated {len(evidence)} checked {label} source results; preserved all native "
        f"completeness harnesses; indexed {count} stable source-owned APIs."
    )


def checked_mutable_source(api):
    source = f"proofs/correctness/slice/{api}.rs"
    logs = ROOT / f"logs/mutable-endpoints/correctness/{api}"
    output = logs / f"libslice_{api}.rlib"
    command = checked_pattern_execution(logs, "verus", [
        str(ROOT / VERUS), source, "--crate-type", "lib", "--crate-name", f"slice_{api}",
        "--compile", "--no-cheating", "--num-threads", "1", "--log-all",
        "--log-dir", str(logs / "queries"), "-o", str(output),
    ])
    if (
        (logs / "verus.stdout").read_text().strip() != "verification results:: 1 verified, 0 errors"
        or output.stat().st_size == 0
    ):
        raise ValueError(f"No successful compiled mutable source target: {api}")
    for path in (source, MUTABLE_POST):
        if (logs / "inputs" / path).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Current mutable source differs from its compiled input: {path}")
    original = (ROOT / "logs/mutable-endpoints/adoption-before" / source).read_text()
    before, after = (
        (
            "    if let [first, ..] = slice { Some(first) } else { None }",
            "    if slice.len() == 0 { None } else { Some(&mut slice[0]) }",
        ) if api == "first_mut" else (
            "    if let [.., last] = slice { Some(last) } else { None }",
            "    if slice.len() == 0 {\n        None\n    } else {\n"
            "        let i = slice.len() - 1;\n        Some(&mut slice[i])\n    }",
        )
    )
    if original.count(before) != 1 or (ROOT / source).read_text() != original.replace(before, after, 1):
        raise ValueError(f"Mutable source is not the exact permitted body replacement: {api}")
    query = (logs / "queries/root.smt2").read_text()
    transcript = (logs / "queries/root.smt_transcript").read_text()
    if (
        re.findall(r"^;; Function-Def (.+)$", query, re.MULTILINE) != [f"slice_{api}::{api}"]
        or len(re.findall(r"^\s*\(check-sat\)\s*$", query, re.MULTILINE)) != 1
        or len(re.findall(r"^\(check-sat\)$", transcript, re.MULTILINE)) != 1
        or re.findall(r"^(?:unsat|sat|unknown)$", transcript, re.MULTILINE) != ["unsat"]
        or ";; Function-Def " in (logs / "queries/contracts.smt2").read_text()
    ):
        raise ValueError(f"Missing successful mutable source query: {api}")
    return {
        "correctness_proof": source,
        "correctness_command": command,
        "correctness_log": relative(logs / "verus.stdout"),
        "correctness_result": (
            "verified and compiled with --no-cheating; 1 target + 0 imported proof functions; "
            "independently permitted mutable pattern-to-length/index conversion; "
            "trusts upstream slice length/index-update contracts and Seq view, "
            "not metadata or indexing implementation verification; final implementation review pending"
        ),
        "correctness_target_functions": "1",
    }


def checked_mutable_run(api, phase, analyzed_run=None):
    split = api in MUTABLE_SPLITS
    logs = ROOT / (MUTABLE_SPLIT_CHECKER_LOGS if split else MUTABLE_CHECKER_LOGS) / api
    dependencies = MUTABLE_SPLIT_DEPENDENCIES if split else MUTABLE_DEPENDENCIES
    line = 7 if split else 8
    report_path = logs / f"{phase}.json"
    report = json.loads(report_path.read_text())
    source = f"proofs/completeness/slice/inputs/{api}.rs"
    name = f"{api}_observation"
    selector = f"{source}:{name}@{line}"
    if (
        report["schema_version"] != 1 or report["status"] != "completed"
        or report["exit_code"] != 0 or report["counts"] != {"deterministic": 1}
        or report["diagnostics"] or len(report["results"]) != 1
    ):
        raise ValueError(f"No successful mutable checker run: {report_path}")
    result = report["results"][0]
    target = result["target"]
    if (
        report["targets"] != [target] or target["file"] != source
        or target["name"] != name or target["line"] != line or target["kind"] != "function"
        or target["language"] != "verus" or target["module"]
        or target["qualified_name"] != f"{source}::{name}"
        or (ROOT / source).read_text().splitlines()[line - 1] != f"pub fn {name}<T>("
        or result["status"] != "completed" or result["verdict"] != "deterministic"
        or result["diagnostics"] or len(result["proofs"]) != 1
        or result["baseline"] is None or result["baseline"]["status"] != "unsat"
        or result["baseline"]["role"] != "baseline" or result["baseline"]["constraints"]
        or result["baseline"]["reason"] or result["search"] is not None
        or result["analysis_kind"] != "concrete_determinism"
        or result["assistance"]["accepted_proposals"]
    ):
        raise ValueError(f"Unexpected mutable target or original result: {report_path}")
    run = Path(report["run_dir"])
    output = logs / phase
    if (
        phase not in ("analyze", "replay") or run.parent != output
        or run.name != report["run_id"] or result["run_id"] != report["run_id"]
        or (phase == "replay" and (analyzed_run is None or run == analyzed_run))
    ):
        raise ValueError(f"Unexpected mutable run identity: {report_path}")
    output_argument = str(output) if split else relative(output)
    command = (
        [CHECKER, "analyze", "--config", "specdet.toml", "--target", selector,
         "--out", output_argument, "--json"] if phase == "analyze" else
        [CHECKER, "replay", "--run", str(analyzed_run), "--reexecute",
         "--out", output_argument, "--json"]
    )
    receipt = json.loads((logs / f"{phase}-command.json").read_text())
    if receipt != {"command": command, "returncode": 0} or (logs / f"{phase}.stderr").read_text().strip():
        raise ValueError(f"Unexpected mutable checker command: {report_path}")
    manifest = json.loads((run / "manifest.json").read_text())["payload"]
    if manifest != {
        "run_id": report["run_id"], "status": "completed", "exit_code": 0,
        "parent_run": "" if phase == "analyze" else str(analyzed_run),
    }:
        raise ValueError(f"Mutable replay did not reexecute its analyzed run: {report_path}")
    config = json.loads((run / "effective-config.json").read_text())["payload"]
    if (
        config["selectors"] != [selector]
        or config["project_root"] != str(ROOT if phase == "analyze" else analyzed_run / "workspace")
        or config["output_dir"] != str(output) or config["language"] != "verus"
        or config["type_sources"] != ["specs/slice/mod.rs"]
        or config["build"]["adapter"] != "verus.single_file"
        or config["build"]["extra_args"] != ["--crate-type", "lib"]
        or config["toolchain"]["executable"] != str(ROOT / VERUS)
        or config["toolchain"]["rust_toolchain"] != "1.98.1-x86_64-unknown-linux-gnu"
        or config["toolchain"]["extra_args"] != ["--num-threads", "1"]
        or config["toolchain"]["environment"] or not config["offline"]
        or config["assistance"] != {"mode": "off"}
        or config["analysis_kind"] != "concrete_determinism"
        or config["observation_policy"] != "verus-observable-v1"
    ):
        raise ValueError(f"Unexpected mutable checker configuration: {report_path}")
    proof = result["proofs"][0]
    native = proof["native"]
    if (
        proof["status"] != "verified" or proof["verified_goals"] != 1
        or proof["diagnostics"] or native["baseline"] is not True
    ):
        raise ValueError(f"Expected one verified mutable comparison goal: {report_path}")
    for path in (source, *dependencies):
        if (run / "workspace" / path).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Current mutable input differs from its frozen input: {path}")
        if path != source and (
            Path(native["worktree"]) / path
        ).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Mutable native dependency is stale: {path}")
    comparison = native["det_spec"]
    function = native["fn_det"]
    equal = function + "_equal"
    element = "(T, Seq<T>)" if split else "T"
    output_type = f"Ghost<(Option<{element}>, Seq<T>)>"
    payload_equal = (
        "(((r1)@.0->Some_0.0 == (r2)@.0->Some_0.0) && "
        "((r1)@.0->Some_0.1 =~= (r2)@.0->Some_0.1))"
        if split else "((r1)@.0->Some_0 == (r2)@.0->Some_0)"
    )
    expected_equal = (
        "// Generated equal-fn for determinism check.\n"
        "// Policy: errs_equivalent=True, opaque_ok=False\n"
        f"spec fn {equal}<T>(r1: {output_type}, r2: {output_type}) -> bool {{\n"
        "    (((((r1)@.0 is Some) == ((r2)@.0 is Some)) && "
        f"(((r1)@.0 is Some) ==> {payload_equal})) "
        "&& ((r1)@.1 =~= (r2)@.1))\n}"
    )
    parameters = (
        f"input_initial: Ghost<Seq<T>>, caller_final: Ghost<Option<{element}>>, "
        f"r1: {output_type}, r2: {output_type}"
    )
    precondition = (
        "match caller_final@ {\n"
        "            None => input_initial@.len() == 0,\n"
        "            Some((_, written_remainder)) =>\n"
        "                written_remainder.len() + 1 == input_initial@.len(),\n"
        "        }" if split else "caller_final@.is_none() <==> input_initial@.len() == 0"
    )
    expected_template = (
        f"proof fn {function}<T>({parameters})\n"
        f"    requires ({precondition}),\n"
        "    ensures\n        ({\n"
        f"            &&& (state::post::{api}_post(input_initial@, caller_final@, r1@))\n"
        f"            &&& (state::post::{api}_post(input_initial@, caller_final@, r2@))\n"
        f"        }}) ==> {equal}::<T>(r1, r2),\n{{\n{{ASSUMES}}}}"
    )
    policy = comparison["equal_policy"]
    if (
        comparison["equal_fn_def"] != expected_equal
        or comparison["det_check_template"] != expected_template
        or comparison["equal_fn_name"] != equal or comparison["check_fn_name"] != function
        or comparison["equal_arg_pairs"] != [{"lhs": "r1", "rhs": "r2"}]
        or comparison["function"] != name or comparison["generics_decl"] != "<T>"
        or comparison["where_decl"] or comparison["opened_closed_specs"]
        or policy["source"] != "verus-observable-v1" or policy["custom_body"] is not None
        or policy["ignore_fields"] or policy["opaque_ok"] or policy["opaque_types"]
        or policy["compare_raw_pointers"] or policy["errs_equivalent"] is not True
        or result["coverage"]["ignored_dimensions"] != ["return.representation_beyond_view"]
    ):
        raise ValueError(f"Missing full mutable Option, ordered payload or final-sequence comparison: {report_path}")
    guards, guard_parameters, assumptions = [], "", ""
    for stem, expression, kind in (
        ("_input_initial__", "(input_initial)@", "seq"),
        ("_caller_final__", "(caller_final)@", "option"),
        ("_r1___0", "(r1)@.0", "option"), ("_r1___1", "(r1)@.1", "seq"),
        ("_r2___0", "(r2)@.0", "option"), ("_r2___1", "(r2)@.1", "seq"),
    ):
        if kind == "option":
            for variant in ("Some", "None"):
                guard = f"g_{stem}_is_{variant}"
                guards.append(guard)
                guard_parameters += f"{guard}: bool, "
                assumptions += f"    if {guard} {{ assume({expression} is {variant}); }}\n"
                if split and variant == "Some":
                    remainder = f"{stem}__Some_0_1"
                    guards.extend((f"g_{remainder}_leneq", f"g_{remainder}_lenrng"))
                    guard_parameters += (
                        f"g_{remainder}_leneq: bool, k_{remainder}_leneq: nat, "
                        f"g_{remainder}_lenrng: bool, k_{remainder}_lenrng_lo: nat, "
                        f"k_{remainder}_lenrng_hi: nat, "
                    )
                    assumptions += (
                        f"    if g_{remainder}_leneq {{ assume({expression} is Some); "
                        f"assume({expression}->Some_0.1.len() == k_{remainder}_leneq); }}\n"
                        f"    if g_{remainder}_lenrng {{ assume({expression} is Some); "
                        f"assume({expression}->Some_0.1.len() >= k_{remainder}_lenrng_lo "
                        f"&& {expression}->Some_0.1.len() <= k_{remainder}_lenrng_hi); }}\n"
                    )
        else:
            guards.extend((f"g_{stem}_leneq", f"g_{stem}_lenrng"))
            guard_parameters += (
                f"g_{stem}_leneq: bool, k_{stem}_leneq: nat, g_{stem}_lenrng: bool, "
                f"k_{stem}_lenrng_lo: nat, k_{stem}_lenrng_hi: nat, "
            )
            assumptions += (
                f"    if g_{stem}_leneq {{ assume({expression}.len() == k_{stem}_leneq); }}\n"
                f"    if g_{stem}_lenrng {{ assume({expression}.len() >= k_{stem}_lenrng_lo "
                f"&& {expression}.len() <= k_{stem}_lenrng_hi); }}\n"
            )
    guards.append("g_neq_tuple")
    guard_parameters += "g_neq_tuple: bool, "
    assumptions += f"    if g_neq_tuple {{ assume(!{equal}::<T>(r1, r2)); }}\n"
    guarded = expected_template.replace(
        f"({parameters})", f"({guard_parameters}{parameters})", 1,
    ).replace("{ASSUMES}", assumptions)
    attempt = Path(proof["artifact"])
    harness = Path(native["harness"])
    worktree = attempt / "worktree"
    entrypoint = str(worktree / source)
    input_text = (ROOT / source).read_text()
    expected_harness = input_text[:-2] + f"{expected_equal}\n\n{guarded}\n\n\n}}\n"
    query = Path(result["baseline"]["artifact"])
    if (
        not attempt.is_relative_to(run / "targets") or harness != attempt / "harness.rs"
        or native["worktree"] != str(worktree) or native["source"] != entrypoint
        or native["entrypoint"] != entrypoint or native["crate_entrypoint"] != entrypoint
        or native["logs"] != str(attempt / "verifier/logs") or native["module"]
        or native["crate"] != api or not input_text.endswith("\n}\n")
        or harness.read_text() != expected_harness
        or harness.read_bytes() != Path(entrypoint).read_bytes()
        or query != attempt / "query/originalC.smt2"
    ):
        raise ValueError(f"Unexpected actual mutable comparison source: {report_path}")
    query_text = query.read_text()
    checks = [line.strip() for line in query_text.splitlines() if line.lstrip().startswith("(check-sat")]
    declarations = re.findall(r"^\(declare-fun (g_\S+)! \(\) Bool\)$", query_text, re.MULTILINE)
    expected_check = "(check-sat-assuming (" + " ".join(f"(not {guard}!)" for guard in guards) + "))"
    if checks != [expected_check] or sorted(declarations) != sorted(guards):
        raise ValueError(f"The mutable original query did not disable all {len(guards)} search guards: {query}")
    if split and (
        not query_text.endswith(expected_check + "\n")
        or not re.search(
            rf"^\(declare-fun {re.escape(f'{api}!{equal}.?')}\s", query_text, re.MULTILINE,
        )
    ):
        raise ValueError(f"The mutable split baseline is not the original target query: {query}")
    invocations = native["invocations"]
    if len(invocations) != 1:
        raise ValueError(f"Expected one mutable native invocation: {report_path}")
    invocation = invocations[0]
    process = invocation["process"]
    if (
        invocation["function"] != function or invocation["module"]
        or invocation["role"] != "determinism" or invocation["status"] != "verified"
        or invocation["verified_goals"] != 1 or process["returncode"] != 0
        or process["timed_out"] or process["command"] != [
            str(ROOT / VERUS), entrypoint, "--crate-type", "lib", "--log-all",
            "--log-dir", native["logs"], "--num-threads", "1",
            "--verify-root", "--verify-function", function,
        ]
        or process["stdout"].strip() !=
        "verification results:: 1 verified, 0 errors (partial verification with `--verify-*`)"
        or process["stderr"].strip() != "note: verifying root module (selected functions)"
    ):
        raise ValueError(f"Unexpected mutable native proof result: {report_path}")
    if split:
        baseline = json.loads((attempt / "query/baseline.json").read_text())["payload"]
        if (
            baseline["evidence"] != result["baseline"] or baseline["query_role"] != "originalC"
            or baseline["source_transcript"] != str(Path(native["logs"]) / "root.smt2")
            or baseline["guard_assignments"] != dict.fromkeys(guards, False)
            or json.loads((attempt / "verifier/process.json").read_text())["payload"] != process
            or (attempt / "verifier/stdout.txt").read_text() != process["stdout"]
            or (attempt / "verifier/stderr.txt").read_text() != process["stderr"]
        ):
            raise ValueError(f"Mutable split baseline or native execution differs from its artifacts: {report_path}")
        checked_mutable_split_queries(Path(native["logs"]), {"root": [f"{api}::{function}"]})
    return report, result, native, command


def checked_mutable_state():
    logs = ROOT / "logs/mutable-endpoints-proposal/value-state/state"
    command = [
        VERUS, MUTABLE_STATE, "--crate-type", "lib", "--crate-name", "mutable_state_state",
        "--compile", "--no-cheating", "--num-threads", "1", "--log-all",
        "--log-dir", relative(logs / "queries"), "-o", relative(logs / "libstate.rlib"),
    ]
    if (
        json.loads((logs / "command.json").read_text()) != {"command": command, "returncode": 0}
        or (logs / "verus.log").read_text().strip() != "verification results:: 7 verified, 0 errors"
        or (logs / "libstate.rlib").stat().st_size == 0
    ):
        raise ValueError("Missing compiled mutable state correspondence")
    functions = [
        "first_candidate_correspondence", "last_candidate_correspondence", "caller_domain",
        "all_caller_writes", "full_first_frame", "full_last_frame", "value_state_comparison",
    ]
    query = (logs / "queries/root.smt2").read_text()
    transcript = (logs / "queries/root.smt_transcript").read_text()
    if (
        re.findall(r"^;; Function-Def (.+)$", query, re.MULTILINE)
        != [f"mutable_state_state::{name}" for name in functions]
        or len(re.findall(r"^\s*\(check-sat\)\s*$", query, re.MULTILINE)) != len(functions)
        or re.findall(r"^(?:unsat|sat|unknown)$", transcript, re.MULTILINE) != ["unsat"] * len(functions)
    ):
        raise ValueError("Missing mutable state proof obligations")
    for path in (MUTABLE_STATE, MUTABLE_POST):
        if (
            ROOT / "logs/mutable-endpoints/adoption-before" / path
        ).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Mutable state changed after the independently reviewed proofs: {path}")


def checked_mutable_split_queries(logs, modules):
    for module, functions in modules.items():
        query = (logs / f"{module}.smt2").read_text()
        transcript = (logs / f"{module}.smt_transcript").read_text()
        if (
            not query.strip()
            or re.findall(r"^;; Function-Def (.+)$", query, re.MULTILINE) != functions
            or len(re.findall(r"^\s*\(check-sat\)\s*$", query, re.MULTILINE)) != len(functions)
            or len(re.findall(r"^\(check-sat\)$", transcript, re.MULTILINE)) != len(functions)
            or re.findall(r"^(?:unsat|sat|unknown)$", transcript, re.MULTILINE)
            != ["unsat"] * len(functions)
        ):
            raise ValueError(f"Missing successful mutable split obligations: {logs}/{module}")


def checked_mutable_split_compile(
    logs, source, crate, modules, dependencies=(), *, source_run=False, no_cheating=True,
):
    output = logs / f"lib{crate}.rlib"
    command = [
        str(ROOT / VERUS), str(source), "--crate-type", "lib", "--crate-name", crate,
        "--compile", *(["--no-cheating"] if no_cheating else []), "--num-threads", "1",
        "--log-all", "--log-dir", str(logs / "queries"), "-o", str(output),
    ]
    receipt, exit_field = ("command.json", "returncode") if source_run else ("result.json", "exit_code")
    count = sum(len(functions) for functions in modules.values())
    summary = f"verification results:: {count} verified, 0 errors"
    if (
        json.loads((logs / receipt).read_text()) != {"command": command, exit_field: 0}
        or (logs / "verus.log").read_text().strip() != summary
        or output.stat().st_size == 0
    ):
        raise ValueError(f"No successful compiled mutable split proof: {logs}")
    if source_run and (
        (logs / "verus.stdout").read_bytes() != (logs / "verus.log").read_bytes()
        or (logs / "verus.stderr").read_text().strip()
        or (logs / "verus.exit-code.txt").read_text().strip() != "0"
    ):
        raise ValueError(f"Unsuccessful mutable split source execution: {logs}")
    for path in dependencies:
        if (logs / "inputs" / path).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Mutable split compiled input is stale: {path}")
    checked_mutable_split_queries(logs / "queries", modules)
    return shlex.join(command)


def checked_mutable_split_source(api):
    source = f"proofs/correctness/slice/{api}.rs"
    logs = ROOT / f"logs/mutable-splits/correctness/{api}"
    command = checked_mutable_split_compile(
        logs, source, f"slice_{api}", {"root": [f"slice_{api}::{api}"], "contracts": []},
        (source, MUTABLE_SPLIT_POST), source_run=True,
    )
    original = (ROOT / MUTABLE_SPLIT_BEFORE / source).read_text()
    before, after = (
        (
            "    if let [first, tail @ ..] = slice { Some((first, tail)) } else { None }",
            "    if slice.len() == 0 {\n        None\n    } else {\n"
            "        let (head, tail) = slice.split_at_mut(1);\n"
            "        proof {\n            vstd::slice::mut_ref_slice_len_eq(&tail);\n        }\n"
            "        Some((&mut head[0], tail))\n    }",
        ) if api == "split_first_mut" else (
            "    if let [init @ .., last] = slice { Some((last, init)) } else { None }",
            "    if slice.len() == 0 {\n        None\n    } else {\n"
            "        let i = slice.len() - 1;\n        let (init, last) = slice.split_at_mut(i);\n"
            "        proof {\n            vstd::slice::mut_ref_slice_len_eq(&init);\n        }\n"
            "        Some((&mut last[0], init))\n    }",
        )
    )
    if original.count(before) != 1 or (ROOT / source).read_text() != original.replace(before, after, 1):
        raise ValueError(f"Mutable split source is not the exact permitted body replacement: {api}")
    if api == "split_last_mut":
        contract = original.split("    ensures\n", 1)[1].split("\n{\n", 1)[0]
        expected_binding = (
            "use vstd::prelude::*;\n\n"
            '#[path = "mutable_splits_post.rs"]\npub mod post;\n\nverus! {\n\n'
            "// split_first_mut is already registered by the selected vstd.\n"
            "// Rust 1.96 slice/mod.rs:244-264.\n"
            "pub assume_specification<T>[ <[T]>::split_last_mut ](\n"
            "    slice: &mut [T],\n) -> (result: Option<(&mut T, &mut [T])>)\n"
            "    ensures\n" + contract.replace("contracts::", "post::")
            + "\n    no_unwind\n;\n\n}\n"
        )
        if (
            (ROOT / MUTABLE_SPLIT_BINDING).read_text() != expected_binding
            or (ROOT / MUTABLE_SPLIT_BINDING).read_bytes()
            != (ROOT / MUTABLE_SPLIT_BEFORE / MUTABLE_SPLIT_BINDING).read_bytes()
        ):
            raise ValueError("Expected only the unchanged split_last_mut public binding")
    return {
        "correctness_proof": source,
        "correctness_command": command,
        "correctness_log": relative(logs / "verus.stdout"),
        "correctness_result": (
            "verified and compiled with --no-cheating; 1 target + 0 imported proof functions; "
            "independently permitted mutable pattern-to-length/index/split_at_mut conversion "
            "with borrow-length ghost facts; trusts upstream slice length/index-update/"
            "split_at_mut contracts and Seq view, not metadata, indexing or split_at_mut "
            "implementation verification; final implementation review pending"
        ),
        "correctness_target_functions": "1",
    }


def checked_mutable_split_state():
    for path in (MUTABLE_SPLIT_STATE, MUTABLE_SPLIT_POST):
        if (ROOT / path).read_bytes() != (ROOT / MUTABLE_SPLIT_BEFORE / path).read_bytes():
            raise ValueError(f"Mutable split state changed after the independently reviewed proofs: {path}")
    checked_mutable_split_compile(
        ROOT / MUTABLE_SPLIT_STATE_LOGS / "state", MUTABLE_SPLIT_STATE, "state",
        {"root": [f"state::{name}" for name in MUTABLE_SPLIT_STATE_FUNCTIONS], "post": []},
        (MUTABLE_SPLIT_STATE, MUTABLE_SPLIT_POST),
    )


def checked_mutable_split_comparison(api, native):
    source = f"proofs/completeness/slice/inputs/{api}.rs"
    if (ROOT / source).read_bytes() != (ROOT / MUTABLE_SPLIT_BEFORE / source).read_bytes():
        raise ValueError(f"Mutable split observation changed after independent review: {source}")
    checked_mutable_split_compile(
        ROOT / MUTABLE_SPLIT_STATE_LOGS / api, source, api,
        {
            "root": [f"{api}::{api}_observation"],
            "state": [f"{api}::state::{name}" for name in MUTABLE_SPLIT_STATE_FUNCTIONS],
            "state__post": [],
        },
        (source, MUTABLE_SPLIT_STATE, MUTABLE_SPLIT_POST),
    )
    crate = f"{api}_comparison"
    checked_mutable_split_compile(
        ROOT / "logs/mutable-splits-proposal/compiled-comparisons" / api, native["source"], crate,
        {
            "root": [f"{crate}::{api}_observation", f"{crate}::{native['fn_det']}"],
            "state": [f"{crate}::state::{name}" for name in MUTABLE_SPLIT_STATE_FUNCTIONS],
            "state__post": [],
        },
        no_cheating=False,
    )


def export_mutable_observations(apis, *, split=False):
    choices = MUTABLE_SPLITS if split else MUTABLE_ENDPOINTS
    label = "split" if split else "endpoint"
    if not apis or len(set(apis)) != len(apis) or not set(apis) <= set(choices):
        raise ValueError(f"Select distinct mutable {label}s from {', '.join(choices)}")
    state = MUTABLE_SPLIT_STATE if split else MUTABLE_STATE
    post = MUTABLE_SPLIT_POST if split else MUTABLE_POST
    checker_logs = MUTABLE_SPLIT_CHECKER_LOGS if split else MUTABLE_CHECKER_LOGS
    fields, rows, _ = pattern_coverage()
    if split:
        checked_mutable_split_state()
    else:
        checked_mutable_state()
    evidence, exports = {}, {}
    for api in apis:
        identity = f"<[T]>::{api}"
        if identity not in rows or rows[identity]["independent_review"] not in (
            "not_evaluated_in_this_mission", "pending",
        ):
            raise ValueError(f"Missing mutable identity or unexpected review state: {api}")
        correctness = checked_mutable_split_source(api) if split else checked_mutable_source(api)
        analyzed, result, native, analyze_command = checked_mutable_run(api, "analyze")
        replay, replay_result, replay_native, replay_command = checked_mutable_run(
            api, "replay", Path(analyzed["run_dir"]),
        )
        text = Path(native["harness"]).read_text()
        if (
            text != Path(replay_native["harness"]).read_text()
            or Path(result["baseline"]["artifact"]).read_bytes()
            != Path(replay_result["baseline"]["artifact"]).read_bytes()
        ):
            raise ValueError(f"Mutable replay changed the comparison or original query: {api}")
        if split:
            checked_mutable_split_comparison(api, native)
        before, after = (
            f'#[path = "../{Path(state).name}"]',
            f'#[path = "{Path(state).name}"]',
        )
        if text.count(before) != 1:
            raise ValueError(f"Unexpected mutable state import: {api}")
        exported = ROOT / f"proofs/completeness/slice/{api}.rs"
        contents = (
            "// Generated by specdet; only the relative state import is relocated.\n"
            f"// Native original: {relative(native['harness'])}\n"
            f"// Reexecuted run: {relative(replay['run_dir'])}\n"
            + text.replace(before, after, 1)
        )
        if exported.exists() and exported.read_text() != contents:
            raise ValueError(f"Refusing to overwrite a different mutable completeness proof: {exported}")
        exports[exported] = contents
        logs = ROOT / checker_logs / api
        evidence[identity] = {
            **{key: value for key, value in rows[identity].items() if key not in fields[:4]},
            **correctness,
            "specification": f"{post}::{api}_post",
            "view": f"specs/shared/SLICE_VIEW.md;toolchain/upstream/source/vstd/slice.rs:13-17;{state}",
            "completeness_input": f"proofs/completeness/slice/inputs/{api}.rs",
            "completeness_proof": relative(exported),
            "completeness_command": " && ".join(
                "RUSTUP_HOME=/home/chentianyu/.rustup " + shlex.join(command)
                for command in (analyze_command, replay_command)
            ),
            "completeness_result": (
                "deterministic; initial Option variant/full element and entire initial remainder "
                "Seq<T>, plus entire final owner Seq<T> for the same initial Seq<T> and legal "
                "caller-final Option<(T, Seq<T>)>; caller element/remainder contents independent; "
                "1 generated goal; 7 state lemmas and adapter separately compiled; "
                "9 compiled comparison functions are not source targets; all 19 search guards off; "
                "unchanged analysis/reexecution retained after source adoption"
                if split else
                "deterministic; initial Option variant/full element and entire final Seq<T> "
                "for the same initial Seq<T> and legal caller-final Option<T>; "
                "1 generated goal; 7 state lemmas separately compiled; all 13 search guards off; "
                "unchanged analysis/reexecution retained after source adoption"
            ),
            "completeness_checked_goals": "1",
            "native_query": relative(result["baseline"]["artifact"]),
            "checker_report": ";".join(relative(logs / f"{phase}.json") for phase in ("analyze", "replay")),
            "issues": "issues/V-SLICE-PATTERN.md;issues/S-MUT-RETURN.md",
            "independent_review": "pending",
            "mission_scope": f"slice_mutable_{label}s",
        }
    contents, count = updated_coverage(evidence, fields[4:])
    for path, text in exports.items():
        path.write_text(text)
    (ROOT / "inventory/coverage.tsv").write_bytes(contents)
    print(f"Exported {len(exports)} checked mutable {label} proofs; preserved unselected records and proofs; indexed {count} stable source-owned APIs.")


def export_mutable_endpoints(apis):
    export_mutable_observations(apis)


def export_mutable_splits(apis):
    export_mutable_observations(apis, split=True)


def checked_split_off_compile(
    logs, source, crate, modules, output, dependencies=(), *,
    text_receipt=False, no_cheating=True,
):
    command = [
        VERUS, str(source), "--crate-type", "lib", "--crate-name", crate,
        "--compile", *(["--no-cheating"] if no_cheating else []), "--num-threads", "1",
        "--log-all", "--log-dir", relative(logs / "queries"), "-o", output,
    ]
    if text_receipt:
        valid = (
            shlex.split((logs / "command.txt").read_text()) == command
            and (logs / "exit-code.txt").read_text().strip() == "0"
        )
    else:
        valid = json.loads((logs / "command.json").read_text()) == {
            "command": command, "returncode": 0,
        }
    count = sum(map(len, modules.values()))
    if (
        not valid or (ROOT / output).stat().st_size == 0
        or (logs / "verus.log").read_text().strip()
        != f"verification results:: {count} verified, 0 errors"
    ):
        raise ValueError(f"No successful compiled split-off proof: {logs}")
    for path in dependencies:
        if (logs / "source" / path).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Stale compiled split-off input: {path}")
    checked_mutable_split_queries(logs / "queries", modules)
    return shlex.join(command)


def checked_split_off_source(api):
    source = f"proofs/correctness/slice/{api}.rs"
    before = (ROOT / SPLIT_OFF_BEFORE / source).read_text()
    expected = before
    modules = {"root": [f"{api}::{api}"], "contracts": []}
    dependencies = [source, SPLIT_OFF_POST]
    logs = ROOT / SPLIT_OFF_SOURCE_LOGS[api]
    output = f"target/split-off-endpoints/lib{api}.rlib"
    if api == "split_off_last":
        if before.count("slice.split_last()") != 1 or before.count("mod contracts;\n") != 1:
            raise ValueError("The pre-adoption last source is not the reviewed original")
        expected = before.replace(
            "mod contracts;\n",
            'mod contracts;\n#[path = "split_last.rs"]\nmod split_dependency;\n', 1,
        ).replace("slice.split_last()", "split_dependency::split_last(*slice)", 1)
        dependencies += ["proofs/correctness/slice/split_last.rs", "specs/slice/mod.rs"]
        modules.update({
            "split_dependency": [f"{api}::split_dependency::split_last"],
            "split_dependency__contracts": [
                f"{api}::split_dependency::contracts::{name}"
                for name in ("scalar_domain", "empty_results")
            ],
        })
        output = relative(logs / f"lib{api}.rlib")
        for path in dependencies[2:]:
            if (ROOT / path).read_bytes() != (ROOT / SPLIT_OFF_BEFORE / path).read_bytes():
                raise ValueError(f"The reviewed shared split dependency changed: {path}")
    if (ROOT / source).read_text() != expected:
        raise ValueError(f"The current split-off source differs from the permitted source: {api}")
    command = checked_split_off_compile(
        logs, source, api, modules, output, dependencies, text_receipt=True,
    )
    return {
        "correctness_proof": source,
        "correctness_command": command,
        "correctness_log": relative(logs / "verus.log"),
        "correctness_result": (
            "verified and compiled with --no-cheating; "
            + (
                "1 target + 1 shared split dependency + 2 imported consistency lemmas; "
                "independently permitted last-call rebinding; "
                "trusts upstream length/index/split_at value contracts, not their implementations; "
                if api == "split_off_last" else
                "1 target + 0 imported project proof functions; original first body; "
                "trusts the existing upstream shared split_first value contract; "
            )
            + "full call-return reference-slot contents; final implementation review pending"
        ),
        "correctness_target_functions": "1",
    }


def checked_split_off_state():
    for path in (SPLIT_OFF_POST, SPLIT_OFF_BINDING, SPLIT_OFF_STATE):
        if (ROOT / path).read_bytes() != (ROOT / SPLIT_OFF_BEFORE / path).read_bytes():
            raise ValueError(f"The independently reviewed split-off candidate or state changed: {path}")
    checked_split_off_compile(
        ROOT / "logs/split-off-endpoints/value-state/state", SPLIT_OFF_STATE, "state",
        {"root": [f"state::{name}" for name in SPLIT_OFF_STATE_FUNCTIONS], "post": []},
        "target/split-off-endpoints/libstate.rlib", (SPLIT_OFF_STATE, SPLIT_OFF_POST),
    )


def checked_split_off_run(api, phase, analyzed_run=None):
    logs = ROOT / SPLIT_OFF_CHECKER_LOGS / api
    report = json.loads((logs / f"{phase}.json").read_text())
    source = f"proofs/completeness/slice/inputs/{api}.rs"
    text = (ROOT / source).read_text()
    selector = f"{source}:{api}@15"
    if (
        phase not in ("analyze", "replay") or report["schema_version"] != 1
        or report["status"] != "completed" or report["exit_code"] != 0
        or report["counts"] != {"deterministic": 1} or report["diagnostics"]
        or len(report["targets"]) != 1 or len(report["results"]) != 1
        or text != (ROOT / SPLIT_OFF_BEFORE / source).read_text()
        or f"pub assume_specification<'a, T>[source::{api}::<T>]" not in text.splitlines()[14]
    ):
        raise ValueError(f"Missing successful current split-off target: {logs}/{phase}")
    result = report["results"][0]
    target = result["target"]
    expected_target = {
        "language": "verus", "file": source, "name": api, "line": 15,
        "qualified_name": f"{source}::source::{api}::<T>",
        "kind": "contract_declaration", "module": "",
    }
    if (
        {key: value for key, value in target.items() if key != "source_digest"} != expected_target
        or report["targets"] != [target] or result["status"] != "completed"
        or result["verdict"] != "deterministic" or result["baseline"] is None
        or result["baseline"]["status"] != "unsat"
        or result["baseline"]["role"] != "baseline"
        or result["baseline"]["constraints"] or result["baseline"]["reason"]
        or result["search"] is not None or len(result["proofs"]) != 1
        or result["analysis_kind"] != "concrete_determinism"
        or result["assistance"]["accepted_proposals"]
        or result["coverage"]["ignored_dimensions"]
        or result["coverage"]["mutable_parameter_poststates"] != "modeled"
        or result["coverage"]["return"] != "modeled"
        or result["diagnostics"] != [{
            "stage": "extract", "code": "contract_declaration", "severity": "info", "details": {},
            "message": "This analysis concerns the declared contract, not a proof that an implementation satisfies it",
        }]
    ):
        raise ValueError(f"Incomplete or unsuccessful split-off analysis: {logs}/{phase}")
    run = Path(report["run_dir"])
    command = (
        [CHECKER, "analyze", "--config", "specdet.toml", "--target", selector,
         "--out", relative(logs / phase), "--json"]
        if phase == "analyze" else
        [CHECKER, "replay", "--run", str(analyzed_run), "--reexecute",
         "--out", relative(logs / phase), "--json"]
    )
    if (
        run.parent != logs / phase or run.name != report["run_id"]
        or result["run_id"] != report["run_id"]
        or (phase == "replay" and (analyzed_run is None or run == analyzed_run))
        or json.loads((logs / f"{phase}-command.json").read_text())
        != {"command": command, "returncode": 0}
        or (logs / f"{phase}.stderr").read_text().strip()
        or json.loads((run / "manifest.json").read_text())["payload"] != {
            "run_id": report["run_id"], "status": "completed", "exit_code": 0,
            "parent_run": "" if phase == "analyze" else str(analyzed_run),
        }
    ):
        raise ValueError(f"Split-off replay must execute its exact analyzed selection: {logs}/{phase}")
    config = json.loads((run / "effective-config.json").read_text())["payload"]
    if (
        config["selectors"] != [selector]
        or config["project_root"] != str(ROOT if phase == "analyze" else Path(analyzed_run) / "workspace")
        or config["output_dir"] != str(logs / phase) or config["language"] != "verus"
        or config["type_sources"] != ["specs/slice/mod.rs"]
        or config["build"]["adapter"] != "verus.single_file"
        or config["build"]["extra_args"] != ["--crate-type", "lib"]
        or config["toolchain"]["executable"] != str(ROOT / VERUS)
        or config["toolchain"]["rust_toolchain"] != "1.98.1-x86_64-unknown-linux-gnu"
        or config["toolchain"]["extra_args"] != ["--num-threads", "1"]
        or config["toolchain"]["environment"] or not config["offline"]
        or config["assistance"] != {"mode": "off"}
        or config["analysis_kind"] != "concrete_determinism"
        or config["observation_policy"] != "verus-observable-v1"
    ):
        raise ValueError(f"Unexpected split-off checker configuration: {logs}/{phase}")
    for path in (source, *SPLIT_OFF_DEPENDENCIES):
        if (run / "workspace" / path).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Stale split-off analyzed input: {path}")
    proof = result["proofs"][0]
    native = proof["native"]
    if (
        proof["status"] != "verified" or proof["verified_goals"] != 1
        or proof["diagnostics"] or native["baseline"] is not True
    ):
        raise ValueError(f"Expected exactly one proved split-off comparison: {logs}/{phase}")
    comparison = native["det_spec"]
    equal_name = native["fn_det"] + "_equal"
    equal = (
        "// Generated equal-fn for determinism check.\n"
        "// Policy: errs_equivalent=True, opaque_ok=False\n"
        f"spec fn {equal_name}<'a, T>(r1: Option<&'a T>, r2: Option<&'a T>, "
        "post1_slice: &[T], post2_slice: &[T]) -> bool {\n"
        "    (((r1 is Some) == (r2 is Some)) && ((r1 is Some) ==> (r1->Some_0 == r2->Some_0)))\n"
        "    && (post1_slice =~= post2_slice)\n}"
    )
    parameters = "pre_slice: &[T], post1_slice: &[T], r1: Option<&'a T>, post2_slice: &[T], r2: Option<&'a T>"
    clause = text.split("    ensures\n", 1)[1].split("\n;", 1)[0].strip().removesuffix(",")
    clauses = [
        clause.replace("old(slice)", "pre_slice").replace("final(slice)", f"post{index}_slice")
        .replace("match result {", f"match r{index} {{")
        for index in (1, 2)
    ]
    template = (
        f"proof fn {native['fn_det']}<'a, T>({parameters})\n"
        "    ensures\n        ({\n"
        f"            &&& ({clauses[0]})\n            &&& ({clauses[1]})\n"
        f"        }}) ==> {equal_name}::<T>(r1, r2, post1_slice, post2_slice),\n"
        "{\n{ASSUMES}}"
    )
    if (
        comparison["equal_fn_def"] != equal or comparison["det_check_template"] != template
        or comparison["equal_arg_pairs"] != [
            {"lhs": "r1", "rhs": "r2"}, {"lhs": "post1_slice", "rhs": "post2_slice"},
        ]
        or comparison["equal_fn_name"] != equal_name
        or comparison["check_fn_name"] != native["fn_det"]
        or comparison["function"] != f"source::{api}::<T>"
        or comparison["generics_decl"] != "<'a, T>" or comparison["where_decl"]
        or comparison["equal_policy"] != {
            "compare_raw_pointers": False, "custom_body": None, "errs_equivalent": True,
            "ignore_fields": [], "opaque_ok": False, "opaque_types": [], "rationale": None,
            "source": "verus-observable-v1",
        }
    ):
        raise ValueError(f"Split-off comparison must retain Option, full value and both remaining slices: {logs}/{phase}")
    guards, guard_parameters, assumptions = [], [], []
    for value in ("pre_slice", "r1", "r2", "post1_slice", "post2_slice"):
        if value in ("r1", "r2"):
            for variant in ("Some", "None"):
                guard = f"g_{value}_is_{variant}"
                guards.append(guard)
                guard_parameters.append(f"{guard}: bool")
                assumptions.append(f"    if {guard} {{ assume({value} is {variant}); }}\n")
        else:
            guards += [f"g_{value}_leneq", f"g_{value}_lenrng"]
            guard_parameters += [
                f"g_{value}_leneq: bool", f"k_{value}_leneq: nat",
                f"g_{value}_lenrng: bool", f"k_{value}_lenrng_lo: nat", f"k_{value}_lenrng_hi: nat",
            ]
            assumptions += [
                f"    if g_{value}_leneq {{ assume({value}.len() == k_{value}_leneq); }}\n",
                f"    if g_{value}_lenrng {{ assume({value}.len() >= k_{value}_lenrng_lo "
                f"&& {value}.len() <= k_{value}_lenrng_hi); }}\n",
            ]
    guards.append("g_neq_tuple")
    guard_parameters.append("g_neq_tuple: bool")
    assumptions.append(
        f"    if g_neq_tuple {{ assume(!{equal_name}::<T>(r1, r2, post1_slice, post2_slice)); }}\n"
    )
    guarded = template.replace(
        f"({parameters})", f"({', '.join(guard_parameters)}, {parameters})", 1,
    ).replace("{ASSUMES}", "".join(assumptions))
    attempt = Path(proof["artifact"])
    worktree = attempt / "worktree"
    entrypoint = str(worktree / source)
    query = Path(result["baseline"]["artifact"])
    if (
        not attempt.is_relative_to(run / "targets")
        or native["harness"] != str(attempt / "harness.rs")
        or native["source"] != entrypoint or native["entrypoint"] != entrypoint
        or native["crate_entrypoint"] != entrypoint or native["worktree"] != str(worktree)
        or native["logs"] != str(attempt / "verifier/logs")
        or native["module"] or native["crate"] != api
        or query != attempt / "query/originalC.smt2" or not text.endswith(";\n}\n")
        or Path(native["harness"]).read_text() != text[:-2] + f"\n{equal}\n\n{guarded}\n\n}}\n"
        or Path(native["harness"]).read_bytes() != Path(entrypoint).read_bytes()
    ):
        raise ValueError(f"Unexpected actual split-off generated comparison: {logs}/{phase}")
    for path in SPLIT_OFF_DEPENDENCIES:
        if (worktree / path).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Stale split-off generated dependency: {path}")
    query_text = query.read_text()
    checks = [line.strip() for line in query_text.splitlines() if line.lstrip().startswith("(check-sat")]
    expected_check = "(check-sat-assuming (" + " ".join(f"(not {guard}!)" for guard in guards) + "))"
    baseline = json.loads((attempt / "query/baseline.json").read_text())["payload"]
    if (
        checks != [expected_check]
        or sorted(re.findall(r"^\(declare-fun (g_\S+)! \(\) Bool\)$", query_text, re.MULTILINE))
        != sorted(guards)
        or baseline["evidence"] != result["baseline"] or baseline["query_role"] != "originalC"
        or baseline["guard_assignments"] != dict.fromkeys(guards, False)
        or baseline["source_transcript"] != str(attempt / "verifier/logs/root.smt2")
    ):
        raise ValueError(f"Every actual split-off search guard must be off: {query}")
    if len(native["invocations"]) != 1:
        raise ValueError(f"Expected one actual split-off verifier invocation: {logs}/{phase}")
    invocation = native["invocations"][0]
    process = invocation["process"]
    if (
        invocation["function"] != native["fn_det"] or invocation["module"]
        or invocation["role"] != "determinism" or invocation["status"] != "verified"
        or invocation["verified_goals"] != 1 or process["returncode"] != 0 or process["timed_out"]
        or process["command"] != [
            str(ROOT / VERUS), entrypoint, "--crate-type", "lib", "--log-all",
            "--log-dir", native["logs"], "--num-threads", "1",
            "--verify-root", "--verify-function", native["fn_det"],
        ]
        or process["stdout"].strip()
        != "verification results:: 1 verified, 0 errors (partial verification with `--verify-*`)"
        or process["stderr"].strip() != "note: verifying root module (selected functions)"
        or json.loads((attempt / "verifier/process.json").read_text())["payload"] != process
        or (attempt / "verifier/stdout.txt").read_text() != process["stdout"]
        or (attempt / "verifier/stderr.txt").read_text() != process["stderr"]
    ):
        raise ValueError(f"Unsuccessful split-off generated proof execution: {logs}/{phase}")
    checked_mutable_split_queries(
        Path(native["logs"]), {"root": [f"{api}::{native['fn_det']}"]},
    )
    return report, result, native, command


def export_split_off_endpoints(apis):
    if not apis or len(set(apis)) != len(apis) or not set(apis) <= set(SPLIT_OFF_ENDPOINTS):
        raise ValueError("Select distinct split_off_first and split_off_last methods")
    fields, rows, _ = pattern_coverage()
    checked_split_off_state()
    evidence, exports = {}, {}
    for api in apis:
        identity = f"<[T]>::{api}"
        if identity not in rows or rows[identity]["independent_review"] not in (
            "not_evaluated_in_this_mission", "pending",
        ):
            raise ValueError(f"Missing split-off identity or unexpected review state: {api}")
        correctness = checked_split_off_source(api)
        analyzed, result, native, analyze_command = checked_split_off_run(api, "analyze")
        replay, replay_result, replay_native, replay_command = checked_split_off_run(
            api, "replay", Path(analyzed["run_dir"]),
        )
        text = Path(native["harness"]).read_text()
        if (
            text != Path(replay_native["harness"]).read_text()
            or Path(result["baseline"]["artifact"]).read_bytes()
            != Path(replay_result["baseline"]["artifact"]).read_bytes()
        ):
            raise ValueError(f"Split-off replay changed the comparison or original query: {api}")
        checked_split_off_compile(
            ROOT / "logs/split-off-endpoints/compiled-comparisons" / api, native["source"], api,
            {"root": [f"{api}::{native['fn_det']}"], "contracts": []},
            f"target/split-off-endpoints/lib{api}_comparison.rlib", no_cheating=False,
        )
        before = '#[path = "../../../../specs/slice/split_off_post.rs"]'
        after = '#[path = "../../../specs/slice/split_off_post.rs"]'
        if text.count(before) != 1:
            raise ValueError(f"Unexpected split-off candidate import: {api}")
        contents = (
            "// Generated by specdet; only the relative pure-candidate import is relocated.\n"
            f"// Native original: {relative(native['harness'])}\n"
            f"// Reexecuted run: {relative(replay['run_dir'])}\n"
            + text.replace(before, after, 1)
        )
        exported = ROOT / f"proofs/completeness/slice/{api}.rs"
        if exported.exists() and exported.read_text() != contents:
            raise ValueError(f"Refusing to overwrite a different split-off comparison: {exported}")
        exports[exported] = contents
        evidence[identity] = {
            **{key: value for key, value in rows[identity].items() if key not in fields[:4]},
            **correctness,
            "specification": f"{SPLIT_OFF_POST}::{api}_post",
            "view": f"specs/shared/SLICE_VIEW.md;toolchain/upstream/source/vstd/slice.rs:13-17;{SPLIT_OFF_STATE}",
            "completeness_input": f"proofs/completeness/slice/inputs/{api}.rs",
            "completeness_proof": relative(exported),
            "completeness_command": " && ".join(
                "RUSTUP_HOME=/home/chentianyu/.rustup " + shlex.join(command)
                for command in (analyze_command, replay_command)
            ),
            "completeness_result": (
                "deterministic; Option variant/full element and entire call-return remaining Seq<T>; "
                "same initial slice, two independent post-slot observations, no caller-final input; "
                "1 generated goal; 6 state lemmas separately compiled; all 11 search guards off; "
                "unchanged analysis/reexecution retained after source adoption"
            ),
            "completeness_checked_goals": "1",
            "native_query": relative(result["baseline"]["artifact"]),
            "checker_report": ";".join(
                f"{SPLIT_OFF_CHECKER_LOGS}/{api}/{phase}.json" for phase in ("analyze", "replay")
            ),
            "issues": "issues/V-ASCII-CALL-BINDING.md" if api == "split_off_last" else "",
            "independent_review": "pending",
            "mission_scope": "slice_shared_split_off_endpoints",
        }
    contents, count = updated_coverage(evidence, fields[4:])
    for path, text in exports.items():
        path.write_text(text)
    (ROOT / "inventory/coverage.tsv").write_bytes(contents)
    print(
        f"Exported {len(exports)} checked split-off proofs; preserved unselected records "
        f"and proofs; indexed {count} stable source-owned APIs."
    )


def readonly_evidence():
    patterns = pattern_evidence(PATTERNS)
    evidence = {}
    import_before = '#[path = "../../../../specs/slice/mod.rs"]'
    import_after = '#[path = "../../../specs/slice/mod.rs"]'
    for api in APIS:
        if api in PATTERNS:
            evidence[f"<[T]>::{api}"] = patterns[f"<[T]>::{api}"]
            continue
        report_path = ROOT / f"logs/foundation/completeness/{api}.json"
        report = json.loads(report_path.read_text())
        if report["schema_version"] != 1 or len(report["results"]) != 1:
            raise ValueError(f"Unexpected native checker report for {api}")
        result = report["results"][0]
        if (
            result["target"]["name"] != api
            or result["target"]["kind"] != "contract_declaration"
            or result["status"] != "completed"
            or result["verdict"] != "deterministic"
            or result["baseline"]["status"] != "unsat"
        ):
            raise ValueError(f"No successful original completeness result for {api}")
        proofs = [
            proof for proof in result["proofs"]
            if proof["status"] == "verified" and proof["verified_goals"] > 0
        ]
        if len(proofs) != 1 or not proofs[0]["native"]["baseline"]:
            raise ValueError(f"Expected one checked native baseline proof for {api}")
        proof = proofs[0]
        native = proof["native"]
        snapshot = Path(report["run_dir"]) / "workspace"
        for source in (
            "specs/slice/mod.rs",
            f"proofs/completeness/slice/inputs/{api}.rs",
            "specdet.toml",
        ):
            if (snapshot / source).read_bytes() != (ROOT / source).read_bytes():
                raise ValueError(f"Current candidate differs from checked snapshot: {source}")
        harness = Path(native["harness"])
        text = harness.read_text()
        if text.count(import_before) != 1:
            raise ValueError(f"Unexpected predicate import in native harness for {api}")
        query = Path(result["baseline"]["artifact"])
        if query.stat().st_size == 0:
            raise ValueError(f"Missing native query for {api}")
        exported = ROOT / f"proofs/completeness/slice/{api}.rs"
        exported.write_text(
            "// Generated by specdet; only the relative predicate import is relocated.\n"
            f"// Native original: {relative(harness)}\n"
            + text.replace(import_before, import_after, 1)
        )
        line = result["target"]["line"]
        correctness_log = ROOT / f"logs/foundation/correctness/{api}/verus.log"
        diagnostic = correctness_log.read_text()
        if api == "is_empty":
            if "verification results:: 3 verified, 0 errors" not in diagnostic:
                raise ValueError("The source is_empty proof is not the expected checked result")
            outcome = "verified; 1 target function + 2 imported consistency lemmas"
            obligations = "1"
            issue = "issues/V-METADATA.md (len dependency; target body verified)"
        else:
            expected = "dereferencing a pointer" if api == "len" else "slice patterns"
            if expected not in diagnostic:
                raise ValueError(f"Expected source limitation diagnostic is absent for {api}")
            outcome = f"frontend_rejected: {expected}"
            obligations = "0"
            issue = "issues/V-METADATA.md" if api == "len" else "issues/V-SLICE-PATTERN.md"
        evidence[f"<[T]>::{api}"] = {
            "specification": f"specs/slice/mod.rs::{api}_post",
            "view": "specs/shared/SLICE_VIEW.md;toolchain/upstream/source/vstd/slice.rs:13-17",
            "correctness_proof": f"proofs/correctness/slice/{api}.rs",
            "correctness_command": (
                f"{VERUS} proofs/correctness/slice/{api}.rs --crate-type lib "
                f"--crate-name slice_{api}_source --compile --no-cheating --num-threads 1 "
                f"--log-all --log-dir logs/foundation/correctness/{api}/queries "
                f"-o target/foundation/libslice_{api}_source.rlib"
            ),
            "correctness_log": relative(correctness_log),
            "correctness_result": outcome,
            "correctness_target_functions": obligations,
            "completeness_input": f"proofs/completeness/slice/inputs/{api}.rs",
            "completeness_proof": relative(exported),
            "completeness_command": (
                f"{CHECKER} analyze --config specdet.toml "
                f"--target proofs/completeness/slice/inputs/{api}.rs:{api}@{line} "
                f"--out proofs/completeness/slice/runs/{api} --json"
            ),
            "completeness_result": result["verdict"],
            "completeness_checked_goals": str(proof["verified_goals"]),
            "native_query": relative(query),
            "checker_report": relative(report_path),
            "issues": issue,
            "independent_review": "pending",
            "mission_scope": "current_six",
        }
    return evidence


def checked_default_run(api, phase):
    report_path = ROOT / DEFAULT_CHECKER_LOGS[api] / f"{phase}.json"
    report = json.loads(report_path.read_text())
    if report["schema_version"] != 1 or len(report["results"]) != 1:
        raise ValueError(f"Unexpected checker report: {report_path}")
    result = report["results"][0]
    name = "default" if api == "default_shared" else "default_mut_observation"
    kind = "contract_declaration" if api == "default_shared" else "function"
    if (
        result["target"]["name"] != name or result["target"]["kind"] != kind
        or result["status"] != "completed" or result["verdict"] != "deterministic"
        or result["baseline"] is None or result["baseline"]["status"] != "unsat"
        or len(result["proofs"]) != 1
    ):
        raise ValueError(f"No successful original completeness result: {report_path}")
    proof = result["proofs"][0]
    native = proof["native"]
    if proof["status"] != "verified" or proof["verified_goals"] != 1 or not native["baseline"]:
        raise ValueError(f"Expected one verified baseline goal: {report_path}")
    comparison = native["det_spec"]
    policy = comparison["equal_policy"]
    if (
        comparison["equal_arg_pairs"] != [{"lhs": "r1", "rhs": "r2"}]
        or not comparison["equal_fn_def"].endswith("    (r1 =~= r2)\n}")
        or policy["source"] != "verus-observable-v1"
        or policy["custom_body"] is not None or policy["ignore_fields"]
        or policy["opaque_ok"] or result["coverage"]["ignored_dimensions"]
    ):
        raise ValueError(f"The complete returned slice is not compared: {report_path}")
    expected_template = (
        f"proof fn {native['fn_det']}<T>(r1: &[T], r2: &[T])\n"
        "    ensures\n"
        "        ({\n"
        "            &&& (contracts::default_post(r1))\n"
        "            &&& (contracts::default_post(r2))\n"
        f"        }}) ==> {comparison['equal_fn_name']}::<T>(r1, r2),\n"
        "{\n{ASSUMES}}"
    )
    if comparison["det_check_template"] != expected_template:
        raise ValueError(f"Unexpected premises in the determinism obligation: {report_path}")
    query = Path(result["baseline"]["artifact"])
    checks = [line for line in query.read_text().splitlines() if line.startswith("(check-sat")]
    if checks != [
        "(check-sat-assuming ((not g_r1_leneq!) (not g_r1_lenrng!) "
        "(not g_r2_leneq!) (not g_r2_lenrng!) (not g_neq_tuple!)))"
    ]:
        raise ValueError(f"The original query did not disable every search guard: {query}")
    snapshot = Path(report["run_dir"]) / "workspace"
    sources = [
        "specs/slice/default_post.rs",
        f"proofs/completeness/slice/inputs/{api}.rs",
        "specdet.toml" if api == "default_shared" else "proofs/completeness/slice/defaults.toml",
    ]
    if api == "default_mut":
        sources.append("proofs/correctness/slice/default_mut.rs")
    for source in sources:
        if (snapshot / source).read_bytes() != (ROOT / source).read_bytes():
            raise ValueError(f"Current input differs from the checked snapshot: {source}")
    invocation = native["invocations"]
    if (
        len(invocation) != 1 or invocation[0]["verified_goals"] != 1
        or invocation[0]["process"]["returncode"] != 0
        or invocation[0]["process"]["command"][0] != str(ROOT / VERUS)
    ):
        raise ValueError(f"Unexpected verifier invocation: {report_path}")
    return report, result, native


def default_evidence(apis=("default_shared", "default_mut")):
    evidence = {}
    for api in apis:
        _, result, native = checked_default_run(api, "analyze")
        replay, _, replay_native = checked_default_run(api, "replay")
        harness = Path(native["harness"])
        text = harness.read_text()
        if harness.read_bytes() != Path(replay_native["harness"]).read_bytes():
            raise ValueError(f"The replay changed the native harness for {api}")
        replacements = {
            '#[path = "../../../../specs/slice/default_post.rs"]':
                '#[path = "../../../specs/slice/default_post.rs"]',
        }
        if api == "default_mut":
            replacements['#[path = "../../../correctness/slice/default_mut.rs"]'] = (
                '#[path = "../../correctness/slice/default_mut.rs"]'
            )
        for before, after in replacements.items():
            if text.count(before) != 1:
                raise ValueError(f"Unexpected relative import in {harness}: {before}")
            text = text.replace(before, after, 1)
        exported = ROOT / f"proofs/completeness/slice/{api}.rs"
        exported.write_text(
            "// Generated by specdet; only relative imports are relocated.\n"
            f"// Native original: {relative(harness)}\n"
            f"// Reexecuted run: {relative(replay['run_dir'])}\n"
            + text
        )
        correctness = ROOT / f"logs/defaults/correctness/{api}"
        log = correctness / "verus.log"
        if "verification results:: 1 verified, 0 errors" not in log.read_text():
            raise ValueError(f"The original {api} body has no successful target proof")
        receiver = "&[T]" if api == "default_shared" else "&mut [T]"
        checker_logs = ROOT / DEFAULT_CHECKER_LOGS[api]
        evidence[f"<{receiver} as core::default::Default>::default"] = {
            "specification": "specs/slice/default.rs;specs/slice/default_post.rs::default_post",
            "view": "specs/shared/SLICE_VIEW.md;toolchain/upstream/source/vstd/slice.rs:13-17",
            "correctness_proof": f"proofs/correctness/slice/{api}.rs",
            "correctness_command": (correctness / "command.txt").read_text().strip(),
            "correctness_log": relative(log),
            "correctness_result": "verified; 1 target function; no imported proof functions",
            "correctness_target_functions": "1",
            "completeness_input": f"proofs/completeness/slice/inputs/{api}.rs",
            "completeness_proof": relative(exported),
            "completeness_command": " && ".join(
                (checker_logs / name).read_text().strip()
                for name in ("command.txt", "replay-command.txt")
            ),
            "completeness_result": "deterministic",
            "completeness_checked_goals": "1",
            "native_query": relative(result["baseline"]["artifact"]),
            "checker_report": ";".join(
                relative(checker_logs / f"{phase}.json") for phase in ("analyze", "replay")
            ),
            "issues": "" if api == "default_shared" else "issues/S-MUT-RETURN.md",
            "independent_review": "pending",
            "mission_scope": "slice_defaults",
        }
    return evidence


def checked_singleton_run(api, phase):
    logs = ROOT / SINGLETON_CHECKER_LOGS[api]
    report_path = logs / f"{phase}.json"
    report = json.loads(report_path.read_text())
    if report["schema_version"] != 1 or len(report["results"]) != 1:
        raise ValueError(f"Unexpected checker report: {report_path}")
    result = report["results"][0]
    source = f"proofs/completeness/slice/inputs/{api}.rs"
    target = result["target"]
    name = "from_ref" if api == "from_ref" else "from_mut_observation"
    kind = "contract_declaration" if api == "from_ref" else "function"
    signature = (
        "[ core::slice::from_ref ]" if api == "from_ref"
        else "pub fn from_mut_observation<T>("
    )
    lines = (ROOT / source).read_text().splitlines()
    if (
        target["file"] != source or target["name"] != name
        or target["kind"] != kind or not 1 <= target["line"] <= len(lines)
        or signature not in lines[target["line"] - 1]
    ):
        raise ValueError(f"Unexpected singleton target: {report_path}")
    snapshot = Path(report["run_dir"]) / "workspace"
    sources = [
        source, "specs/slice/raw.rs", "specs/slice/raw_post.rs",
        "proofs/completeness/slice/singletons.toml",
    ]
    if api == "from_mut":
        sources.append("proofs/completeness/slice/from_mut_state.rs")
    for path in sources:
        if (snapshot / path).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Current input differs from the checked snapshot: {path}")
    exit_code = int((logs / f"{phase}.exit-code.txt").read_text())
    if (
        exit_code != 0 or result["status"] != "completed"
        or result["verdict"] != "deterministic" or result["baseline"] is None
        or result["baseline"]["status"] != "unsat" or result["baseline"]["constraints"]
        or len(result["proofs"]) != 1 or report["exit_code"] != 0
        or report["status"] != "completed" or report["diagnostics"]
        or (api == "from_mut" and result["diagnostics"])
    ):
        raise ValueError(f"No successful original completeness result: {report_path}")
    proof = result["proofs"][0]
    native = proof["native"]
    if proof["status"] != "verified" or proof["verified_goals"] != 1 or not native["baseline"]:
        raise ValueError(f"Expected one verified baseline goal: {report_path}")
    comparison = native["det_spec"]
    policy = comparison["equal_policy"]
    output_type = "&[T]" if api == "from_ref" else "Ghost<(Seq<T>, T)>"
    equality = (
        "(r1 =~= r2)" if api == "from_ref"
        else "(((r1)@.0 =~= (r2)@.0) && ((r1)@.1 == (r2)@.1))"
    )
    expected_equal = (
        "// Generated equal-fn for determinism check.\n"
        "// Policy: errs_equivalent=True, opaque_ok=False\n"
        f"spec fn {comparison['equal_fn_name']}<T>(r1: {output_type}, r2: {output_type}) -> bool {{\n"
        f"    {equality}\n}}"
    )
    ignored = [] if api == "from_ref" else ["return.representation_beyond_view"]
    if (
        comparison["equal_arg_pairs"] != [{"lhs": "r1", "rhs": "r2"}]
        or comparison["equal_fn_def"] != expected_equal
        or policy["source"] != "verus-observable-v1"
        or policy["custom_body"] is not None or policy["ignore_fields"]
        or policy["opaque_ok"] or policy["opaque_types"]
        or result["coverage"]["ignored_dimensions"] != ignored
        or comparison["generics_decl"] != "<T>" or comparison["where_decl"]
    ):
        raise ValueError(f"The complete singleton observations are not compared: {report_path}")
    if api == "from_ref":
        parameters = "s: &T, r1: &[T], r2: &[T]"
        requires = ""
        postconditions = (
            "            &&& (contracts::singleton_post(*s, r1@))\n"
            "            &&& (contracts::singleton_post(*s, r2@))\n"
        )
        guards = ("g_r1_leneq", "g_r1_lenrng", "g_r2_leneq", "g_r2_lenrng", "g_neq_tuple")
    else:
        parameters = (
            "input_initial: Ghost<T>, caller_final: Ghost<Seq<T>>, "
            "r1: Ghost<(Seq<T>, T)>, r2: Ghost<(Seq<T>, T)>"
        )
        requires = "    requires (caller_final@.len() == 1),\n"
        postconditions = (
            "            &&& (state::post::singleton_post(input_initial@, r1@.0))\n"
            "            &&& (r1@.1 == caller_final@[0])\n"
            "            &&& (state::post::singleton_post(input_initial@, r2@.0))\n"
            "            &&& (r2@.1 == caller_final@[0])\n"
        )
        guards = (
            "g__caller_final___leneq", "g__caller_final___lenrng",
            "g__r1___0_leneq", "g__r1___0_lenrng",
            "g__r2___0_leneq", "g__r2___0_lenrng", "g_neq_tuple",
        )
    expected_template = (
        f"proof fn {native['fn_det']}<T>({parameters})\n"
        f"{requires}"
        "    ensures\n"
        "        ({\n"
        f"{postconditions}"
        f"        }}) ==> {comparison['equal_fn_name']}::<T>(r1, r2),\n"
        "{\n{ASSUMES}}"
    )
    if comparison["det_check_template"] != expected_template:
        raise ValueError(f"Unexpected premises in the determinism obligation: {report_path}")
    query = Path(result["baseline"]["artifact"])
    checks = [line for line in query.read_text().splitlines() if line.startswith("(check-sat")]
    expected_check = "(check-sat-assuming (" + " ".join(f"(not {guard}!)" for guard in guards) + "))"
    if checks != [expected_check]:
        raise ValueError(f"The original query did not disable every search guard: {query}")
    invocation = native["invocations"]
    if (
        len(invocation) != 1 or invocation[0]["verified_goals"] != 1
        or invocation[0]["process"]["returncode"] != 0
        or invocation[0]["process"]["command"][0] != str(ROOT / VERUS)
    ):
        raise ValueError(f"Unexpected verifier invocation: {report_path}")
    return report, result, native


def singleton_evidence(apis=("from_ref", "from_mut")):
    if not apis or len(set(apis)) != len(apis) or not set(apis) <= SINGLETON_CHECKER_LOGS.keys():
        raise ValueError("Select distinct singleton APIs from from_ref and from_mut")
    evidence = {}
    for api in apis:
        _, result, native = checked_singleton_run(api, "analyze")
        replay, _, replay_native = checked_singleton_run(api, "replay")
        exported = ROOT / f"proofs/completeness/slice/{api}.rs"
        harness = Path(native["harness"])
        text = harness.read_text()
        if harness.read_bytes() != Path(replay_native["harness"]).read_bytes():
            raise ValueError(f"The replay changed the native harness for {api}")
        if api == "from_ref":
            before = '#[path = "../../../../specs/slice/raw_post.rs"]'
            after = '#[path = "../../../specs/slice/raw_post.rs"]'
            dependency = "predicate"
        else:
            before = '#[path = "../from_mut_state.rs"]'
            after = '#[path = "from_mut_state.rs"]'
            dependency = "state"
        if text.count(before) != 1:
            raise ValueError(f"Unexpected relative import in {harness}")
        exported.write_text(
            f"// Generated by specdet; only the relative {dependency} import is relocated.\n"
            f"// Native original: {relative(harness)}\n"
            f"// Reexecuted run: {relative(replay['run_dir'])}\n"
            + text.replace(before, after, 1)
        )
        correctness = ROOT / f"logs/singletons/correctness/{api}"
        diagnostic = correctness / "stderr.log"
        if (
            int((correctness / "exit-code.txt").read_text()) != 1
            or "dereferencing a pointer (here the dereference is implicit)" not in diagnostic.read_text()
        ):
            raise ValueError(f"Expected the array dependency rejection for {api}")
        logs = ROOT / SINGLETON_CHECKER_LOGS[api]
        evidence[f"core::slice::{api}"] = {
            "specification": "specs/slice/raw.rs;specs/slice/raw_post.rs::singleton_post",
            "view": (
                "specs/shared/SLICE_VIEW.md;toolchain/upstream/source/vstd/slice.rs:13-17;"
                "toolchain/upstream/source/vstd/array.rs:11-21,90-95,115-121,175-183"
                + (";proofs/completeness/slice/from_mut_state.rs" if api == "from_mut" else "")
            ),
            "correctness_proof": f"proofs/correctness/slice/{api}.rs;proofs/correctness/array/singleton.rs",
            "correctness_command": (correctness / "command.txt").read_text().strip(),
            "correctness_log": relative(diagnostic),
            "correctness_result": "frontend_rejected: array reference-to-pointer casts; 0 target and 0 dependency functions verified",
            "correctness_target_functions": "0",
            "completeness_input": f"proofs/completeness/slice/inputs/{api}.rs",
            "completeness_proof": relative(exported),
            "completeness_command": " && ".join(
                (logs / f"{phase}-command.txt").read_text().strip()
                for phase in ("analyze", "replay")
            ),
            "completeness_result": result["verdict"] + (
                "; full initial sequence + full returned T (input writeback) for the same "
                "initial T and arbitrary lawful final caller sequence (length one)"
                if api == "from_mut" else ""
            ),
            "completeness_checked_goals": "1",
            "native_query": relative(result["baseline"]["artifact"]),
            "checker_report": ";".join(relative(logs / f"{phase}.json") for phase in ("analyze", "replay")),
            "issues": "issues/V-METADATA.md" + (";issues/S-MUT-RETURN.md" if api == "from_mut" else ""),
            "independent_review": "pending",
            "mission_scope": "slice_singletons",
        }
    return evidence


def checked_ascii_run(api, phase):
    logs = ROOT / ASCII_CHECKER_LOGS[api]
    report_path = logs / f"{phase}.json"
    report = json.loads(report_path.read_text())
    name = f"{api}_observation"
    expected_names = (
        {name} if phase == "analyze"
        else {f"{selected}_observation" for selected in ASCII_CHECKER_LOGS}
    )
    results = report["results"]
    if (
        report["schema_version"] != 1 or len(results) != len(expected_names)
        or {result["target"]["name"] for result in results} != expected_names
        or report["status"] != "completed" or report["exit_code"] != 0
        or int((logs / f"{phase}.exit-code.txt").read_text()) != 0
        or report["diagnostics"]
    ):
        raise ValueError(f"Unexpected ASCII checker report: {report_path}")
    result = next(result for result in results if result["target"]["name"] == name)
    source = f"proofs/completeness/slice/inputs/{api}.rs"
    target = result["target"]
    lines = (ROOT / source).read_text().splitlines()
    if (
        target["file"] != source or target["kind"] != "function"
        or not 1 <= target["line"] <= len(lines)
        or f"pub fn {name}(initial: Ghost<Seq<u8>>)" not in lines[target["line"] - 1]
    ):
        raise ValueError(f"Unexpected ASCII target: {report_path}")
    snapshot = Path(report["run_dir"]) / "workspace"
    for path in (
        source, "specs/slice/ascii.rs", "specs/slice/ascii_post.rs",
        "proofs/completeness/slice/ascii_state.rs", "proofs/completeness/slice/ascii.toml",
    ):
        if (snapshot / path).read_bytes() != (ROOT / path).read_bytes():
            raise ValueError(f"Current input differs from the checked snapshot: {path}")
    if (
        result["status"] != "completed" or result["verdict"] != "deterministic"
        or result["baseline"] is None or result["baseline"]["status"] != "unsat"
        or result["baseline"]["constraints"] or result["diagnostics"]
        or len(result["proofs"]) != 1
    ):
        raise ValueError(f"No successful original completeness result: {report_path}")
    proof = result["proofs"][0]
    native = proof["native"]
    if proof["status"] != "verified" or proof["verified_goals"] != 1 or not native["baseline"]:
        raise ValueError(f"Expected one verified baseline goal: {report_path}")
    comparison = native["det_spec"]
    policy = comparison["equal_policy"]
    expected_equal = (
        "// Generated equal-fn for determinism check.\n"
        "// Policy: errs_equivalent=True, opaque_ok=False\n"
        f"spec fn {comparison['equal_fn_name']}(r1: Ghost<Seq<u8>>, r2: Ghost<Seq<u8>>) -> bool {{\n"
        "    ((r1)@ =~= (r2)@)\n}"
    )
    if (
        comparison["equal_arg_pairs"] != [{"lhs": "r1", "rhs": "r2"}]
        or comparison["equal_fn_def"] != expected_equal
        or policy["source"] != "verus-observable-v1" or policy["custom_body"] is not None
        or policy["ignore_fields"] or policy["opaque_ok"] or policy["opaque_types"]
        or comparison["generics_decl"] or comparison["where_decl"]
        or result["coverage"]["ignored_dimensions"] != ["return.representation_beyond_view"]
    ):
        raise ValueError(f"The complete final byte sequence is not compared: {report_path}")
    case = api.removeprefix("make_ascii_")
    expected_template = (
        f"proof fn {native['fn_det']}(initial: Ghost<Seq<u8>>, "
        "r1: Ghost<Seq<u8>>, r2: Ghost<Seq<u8>>)\n"
        "    ensures\n"
        "        ({\n"
        f"            &&& (state::post::{case}_post(initial@, r1@))\n"
        f"            &&& (state::post::{case}_post(initial@, r2@))\n"
        f"        }}) ==> {comparison['equal_fn_name']}(r1, r2),\n"
        "{\n{ASSUMES}}"
    )
    if comparison["det_check_template"] != expected_template:
        raise ValueError(f"Unexpected premises in the determinism obligation: {report_path}")
    guards = []
    for value in ("initial", "r1", "r2"):
        guards.extend((f"g__{value}___leneq", f"g__{value}___lenrng"))
        for index in range(8):
            guards.extend((f"g__{value}___{index}__eq", f"g__{value}___{index}__rng"))
    guards.append("g_neq_tuple")
    query = Path(result["baseline"]["artifact"])
    checks = [line for line in query.read_text().splitlines() if line.startswith("(check-sat")]
    expected_check = "(check-sat-assuming (" + " ".join(f"(not {guard}!)" for guard in guards) + "))"
    if checks != [expected_check]:
        raise ValueError(f"The original query did not disable every search guard: {query}")
    invocation = native["invocations"]
    if (
        len(invocation) != 1 or invocation[0]["verified_goals"] != 1
        or invocation[0]["process"]["returncode"] != 0
        or invocation[0]["process"]["command"][0] != str(ROOT / VERUS)
    ):
        raise ValueError(f"Unexpected verifier invocation: {report_path}")
    return report, result, native


def ascii_evidence(apis=("make_ascii_uppercase", "make_ascii_lowercase")):
    if not apis or len(set(apis)) != len(apis) or not set(apis) <= ASCII_CHECKER_LOGS.keys():
        raise ValueError("Select distinct ASCII APIs from make_ascii_uppercase and make_ascii_lowercase")
    evidence = {}
    for api in apis:
        _, result, native = checked_ascii_run(api, "analyze")
        replay, _, replay_native = checked_ascii_run(api, "replay")
        harness = Path(native["harness"])
        text = harness.read_text()
        if harness.read_bytes() != Path(replay_native["harness"]).read_bytes():
            raise ValueError(f"The replay changed the native harness for {api}")
        before = '#[path = "../ascii_state.rs"]'
        after = '#[path = "ascii_state.rs"]'
        if text.count(before) != 1:
            raise ValueError(f"Unexpected relative state import in {harness}")
        correctness = ROOT / ASCII_CORRECTNESS_LOGS[api]
        diagnostic = correctness / "verus.stdout"
        if (
            int((correctness / "exit-code.txt").read_text()) != 0
            or diagnostic.read_text().strip() != "verification results:: 13 verified, 0 errors"
            or (correctness / "verus.stderr").read_text().strip()
        ):
            raise ValueError(f"No successful compiled ASCII source proof for {api}")
        for source in (
            f"proofs/correctness/slice/{api}.rs", *ASCII_CORRECTNESS_DEPENDENCIES,
        ):
            if (correctness / "inputs" / source).read_bytes() != (ROOT / source).read_bytes():
                raise ValueError(f"Current source differs from the checked source proof: {source}")
        exported = ROOT / f"proofs/completeness/slice/{api}.rs"
        exported.write_text(
            "// Generated by specdet; only the relative state import is relocated.\n"
            f"// Native original: {relative(harness)}\n"
            f"// Reexecuted run: {relative(replay['run_dir'])}\n"
            + text.replace(before, after, 1)
        )
        case = api.removeprefix("make_ascii_")
        logs = ROOT / ASCII_CHECKER_LOGS[api]
        evidence[f"<[u8]>::{api}"] = {
            "specification": f"specs/slice/ascii.rs;specs/slice/ascii_post.rs::{case}_post",
            "view": (
                "specs/shared/SLICE_VIEW.md;toolchain/upstream/source/vstd/slice.rs:13-17;"
                "proofs/completeness/slice/ascii_state.rs"
            ),
            "correctness_proof": (
                f"proofs/correctness/slice/{api}.rs;proofs/correctness/num/u8_ascii.rs;"
                "proofs/correctness/num/u8_ascii_classify.rs"
            ),
            "correctness_command": (correctness / "command.txt").read_text().strip(),
            "correctness_log": relative(diagnostic),
            "correctness_result": (
                "verified and compiled with --no-cheating; reviewed source-copy call rebinding; "
                "1 target + 6 scalar source functions; 13 verified obligations including "
                "1 loop, 1 constant and 4 bit-vector assertions"
            ),
            "correctness_target_functions": "1",
            "completeness_input": f"proofs/completeness/slice/inputs/{api}.rs",
            "completeness_proof": relative(exported),
            "completeness_command": " && ".join(
                (logs / f"{phase}-command.txt").read_text().strip()
                for phase in ("analyze", "replay")
            ),
            "completeness_result": "deterministic; full final Seq<u8> for the same initial Seq<u8>",
            "completeness_checked_goals": "1",
            "native_query": relative(result["baseline"]["artifact"]),
            "checker_report": ";".join(relative(logs / f"{phase}.json") for phase in ("analyze", "replay")),
            "issues": "issues/V-ASCII-CALL-BINDING.md",
            "independent_review": "pending",
            "mission_scope": "slice_ascii_case",
        }
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        "--defaults", nargs="*", choices=DEFAULT_CHECKER_LOGS,
        help="export Default results, optionally selecting individual APIs",
    )
    selection.add_argument(
        "--singletons", nargs="*", choices=SINGLETON_CHECKER_LOGS,
        help="export checked singleton observations, optionally selecting individual APIs",
    )
    selection.add_argument(
        "--ascii-case", nargs="*", choices=ASCII_CHECKER_LOGS,
        help="export checked full final ASCII sequences, optionally selecting individual APIs",
    )
    selection.add_argument(
        "--endpoints", nargs="*", choices=ENDPOINTS,
        help="update only checked first/last source results; preserve all completeness exports",
    )
    selection.add_argument(
        "--splits", nargs="*", choices=SPLITS,
        help="update only checked split source results; preserve all completeness exports",
    )
    selection.add_argument(
        "--mutable-endpoints", nargs="*", choices=MUTABLE_ENDPOINTS,
        help="export checked first_mut/last_mut source and complete writeback observations",
    )
    selection.add_argument(
        "--mutable-splits", nargs="*", choices=MUTABLE_SPLITS,
        help="export checked mutable split sources, complete initial returns and final owners",
    )
    selection.add_argument(
        "--split-off-endpoints", nargs="*", choices=SPLIT_OFF_ENDPOINTS,
        help="export checked shared split-off sources, full returned values and remaining slots",
    )
    args = parser.parse_args()
    if args.endpoints is not None:
        if len(set(args.endpoints)) != len(args.endpoints):
            parser.error("--endpoints requires distinct API selections")
        export_pattern_sources(pattern_evidence(args.endpoints or ENDPOINTS))
        return
    elif args.splits is not None:
        if len(set(args.splits)) != len(args.splits):
            parser.error("--splits requires distinct API selections")
        export_pattern_sources(pattern_evidence(args.splits or SPLITS))
        return
    elif args.mutable_endpoints is not None:
        if len(set(args.mutable_endpoints)) != len(args.mutable_endpoints):
            parser.error("--mutable-endpoints requires distinct API selections")
        export_mutable_endpoints(args.mutable_endpoints or MUTABLE_ENDPOINTS)
        return
    elif args.mutable_splits is not None:
        if len(set(args.mutable_splits)) != len(args.mutable_splits):
            parser.error("--mutable-splits requires distinct API selections")
        export_mutable_splits(args.mutable_splits or MUTABLE_SPLITS)
        return
    elif args.split_off_endpoints is not None:
        if len(set(args.split_off_endpoints)) != len(args.split_off_endpoints):
            parser.error("--split-off-endpoints requires distinct API selections")
        export_split_off_endpoints(args.split_off_endpoints or SPLIT_OFF_ENDPOINTS)
        return
    elif args.ascii_case is not None:
        if len(set(args.ascii_case)) != len(args.ascii_case):
            parser.error("--ascii-case requires distinct API selections")
        evidence = ascii_evidence(args.ascii_case or tuple(ASCII_CHECKER_LOGS))
    elif args.singletons is not None:
        if len(set(args.singletons)) != len(args.singletons):
            parser.error("--singletons requires distinct API selections")
        evidence = singleton_evidence(args.singletons or ("from_ref", "from_mut"))
    else:
        evidence = (
            default_evidence(args.defaults or ("default_shared", "default_mut"))
            if args.defaults is not None else readonly_evidence()
        )
    fields = [
        "canonical_id", "source_span", "doc_spans", "existing_vstd_coverage",
        *next(iter(evidence.values())).keys(),
    ]
    with (ROOT / "inventory/apis.tsv").open() as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    if len({row["canonical_id"] for row in source_rows}) != len(source_rows):
        raise ValueError("Duplicate canonical identity in source inventory")
    if not evidence.keys() <= {row["canonical_id"] for row in source_rows}:
        raise ValueError("A checked API is missing from the source inventory")
    previous = {}
    coverage = ROOT / "inventory/coverage.tsv"
    if coverage.exists():
        with coverage.open() as stream:
            previous_rows = list(csv.DictReader(stream, delimiter="\t"))
        previous = {row["canonical_id"]: row for row in previous_rows}
        if len(previous) != len(previous_rows) or previous.keys() != {
            row["canonical_id"] for row in source_rows
        }:
            raise ValueError("Existing coverage and source inventory identities differ")
    with (ROOT / "inventory/coverage.tsv").open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for source in source_rows:
            row = dict(previous[source["canonical_id"]]) if previous else {}
            if (
                source["canonical_id"] in evidence
                and source["canonical_id"] not in PATTERN_IDS
            ) or not previous:
                row.update({key: source[key] for key in fields[:4]})
            if source["canonical_id"] in evidence:
                row.update(evidence[source["canonical_id"]])
            elif not previous:
                row.update({
                    "correctness_result": "not_evaluated_in_this_mission",
                    "completeness_result": "not_evaluated_in_this_mission",
                    "independent_review": "not_evaluated_in_this_mission",
                    "mission_scope": "outside_current_six",
                })
            writer.writerow(row)
    exported_count = sum(
        bool(item["completeness_proof"])
        for identity, item in evidence.items() if identity not in PATTERN_IDS
    )
    print(
        f"Exported {exported_count} "
        "native completeness harnesses; "
        f"indexed {len(source_rows)} stable source-owned APIs."
    )


if __name__ == "__main__":
    main()
