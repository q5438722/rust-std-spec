#!/usr/bin/env python3
"""Split the immutable collected contracts by their original Rust implementation file."""

import argparse
from collections import defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import runpy
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT.parent
RUNS = ORIGINAL.parent
sys.path.insert(0, str(ORIGINAL / "scripts"))
import audit_collection as collection
from rust_format import formatted

LEX = collection.LEX
MODEL_NAMES = ("ascii", "splits", "chunk_by", "chunks", "arrays", "windows")
BUCKETS = ("slice_mod", "slice_non_mod", "vec_mod", "vec_non_mod")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_owners():
    old_slice = RUNS / "rust-std-slice-specgen-astra-2026-09-22"
    reader = runpy.run_path(str(old_slice / "scripts/generate_inventory.py"))["read_tsv"]
    result = {}
    for item in reader(old_slice / "inventory/apis.tsv"):
        span = "core/src/" + item["source_span"]
        result["slice", item["canonical_id"]] = {
            "rust_source_file": span.split(":", 1)[0],
            "rust_source_span": span,
            "source_kind": item["signature_origin"],
        }
    vec = json.loads((RUNS / "rust-std-vec-specgen-astra-2026-09-22/inventory/source_api.json").read_text())
    for item in vec["apis"]:
        source = item["source"]
        result["vec", item["canonical_id"]] = {
            "rust_source_file": source["path"],
            "rust_source_span": f"{source['path']}:{source['start_line']}-{source['end_line']}",
            "source_kind": item["origin"],
        }
    return result


def parse_files(files):
    with tempfile.TemporaryDirectory(prefix="parse-", dir=ROOT / "work") as directory:
        directory = Path(directory)
        for name, text in files.items():
            (directory / name).write_text(text)
        return LEX["OfficialTree"](directory).assumptions


def named_block(text, expression):
    code = LEX["mask_noncode"](text)
    match = re.search(expression, code)
    assert match, expression
    opening = code.index("{", match.end())
    return text[match.start():LEX["balanced_end"](code, opening)]


def external_type(text, name):
    code = LEX["mask_noncode"](text)
    match = re.search(r"pub struct " + re.escape(name) + r"\b", code)
    assert match, name
    start = code.rfind("#[verifier::external_type_specification]", 0, match.start())
    assert start >= 0
    end = code.index(";", match.end()) + 1
    return text[start:end]


def common_slice_model(text):
    parts = [
        "use core::slice::{EscapeAscii, GetDisjointMutError};",
        "use vstd::prelude::*;",
        "verus! {",
    ]
    for name in ("uppercase_byte", "lowercase_byte", "ascii_whitespace"):
        parts.append(named_block(text, r"pub open spec fn " + name + r"\b"))
    parts += [external_type(text, "ExGetDisjointMutError"), external_type(text, "ExEscapeAscii"), "}"]
    for name in MODEL_NAMES:
        parts.append(named_block(text, r"pub mod " + name + r"_model\b"))
    combined = "\n\n".join(parts) + "\n"
    assert not re.search(r"\bassume_specification\b", LEX["mask_noncode"](combined))
    return combined


def attributes(text, record):
    start = record["source"]["start_byte"]
    before = text.encode()[:start].decode()
    # The collected declarations use cfg attributes; copy them with the item.
    match = re.search(r"((?:#\[[^\]\n]+\]\s*)+)$", before)
    return match[1] if match else ""


def imports(module, family):
    if module == "vec":
        return "\n".join((
            "use core::alloc::Allocator;", "use std::borrow::Cow;", "use std::vec::IntoIter;",
            "use vstd::prelude::*;", "use vstd::std_specs::cmp::PartialEqSpec;",
            "use vstd::std_specs::iter::IteratorSpec;",
            "use vstd::std_specs::vec::into_iter_elts;",
        )) + "\n"
    if family == "base":
        return "\n".join((
            "use core::slice::*;", "use vstd::prelude::*;",
            "use vstd::std_specs::iter::IteratorSpec;",
            "use vstd::std_specs::slice::into_iter_elts;",
            "use super::slice_shared::{ascii_whitespace, lowercase_byte, uppercase_byte};",
        )) + "\n"
    result = (
        "use core::slice::*;\nuse vstd::prelude::*;\n"
        "use vstd::std_specs::iter::IteratorSpec;\n"
        f"use super::super::slice_shared::{family}_model::*;\n"
    )
    if family == "ascii":
        result += "use state::Parts;\n"
    return result


def adapt_checks(text):
    pattern = r'#\[path\s*=\s*"\.\./(?:slice|vec)\.rs"\]\s*pub mod (?:slice_specs|vec_specs);'
    text, count = re.subn(pattern, "", text)
    assert count == 2
    first, rest = text.split("\n", 1)
    assert first.startswith("#![feature")
    header = "\n".join(
        f'#[path = "../{name}.rs"]\npub mod {name};'
        for name in ("slice_shared", *BUCKETS)
    )
    header += "\npub mod slice_specs { pub use super::slice_shared::*; }\n"
    header += "pub mod vec_specs {}\n"
    return first + "\n" + header + rest


def render():
    original_manifest = json.loads((ORIGINAL / "manifest.json").read_text())
    texts = {f"{module}.rs": (ORIGINAL / f"{module}.rs").read_text() for module in ("slice", "vec")}
    for name in texts:
        assert sha(ORIGINAL / name) == original_manifest["files"][name]["sha256"], name
    evidence = json.loads((ORIGINAL / "provenance/api_evidence.json").read_text())
    selected = {(e["module"], collection.normalize(e["canonical_api"])): e for e in evidence}
    owners = source_owners()
    records = parse_files(texts)
    grouped = defaultdict(lambda: defaultdict(list))
    rows = []
    seen = set()
    originals = {}
    for record in records:
        module = Path(record["source"]["path"]).stem
        key = module, collection.normalize(record["literal_target"])
        assert key not in seen
        seen.add(key)
        item = selected[key]
        source = owners[module, item["canonical_api"]]
        root_source = "core/src/slice/mod.rs" if module == "slice" else "alloc/src/vec/mod.rs"
        bucket = module + ("_mod" if source["rust_source_file"] == root_source else "_non_mod")
        item_text = attributes(texts[f"{module}.rs"], record) + record["literal"]
        grouped[bucket][item["family"]].append(item_text)
        originals[item["canonical_api"]] = {
            "source_group": bucket, **source,
            "original_file": f"{module}.rs", "original_line": record["source"]["start_line"],
            "original_item_sha256": hashlib.sha256(item_text.encode()).hexdigest(),
        }
    assert len(seen) == 98
    outputs = {
        "lib.rs": "#![feature(allocator_api)]\n\n" + "\n".join(
            f"pub mod {name};" for name in ("slice_shared", *BUCKETS)
        ) + "\n",
        "slice_shared.rs": common_slice_model(texts["slice.rs"]),
    }
    for bucket in BUCKETS:
        module = bucket.split("_", 1)[0]
        parts = []
        for family, declarations in grouped[bucket].items():
            body = imports(module, family) + "\nverus! {\n\n" + "\n\n".join(declarations) + "\n}\n"
            parts.append(body if family == "base" else f"pub mod {family} {{\n{body}\n}}\n")
        outputs[f"{bucket}.rs"] = "\n".join(parts)
    for name in ("api_clients.rs", "examples.rs", "reject_vacuity.rs"):
        outputs[f"checks/{name}"] = adapt_checks((ORIGINAL / "checks" / name).read_text())
    outputs = formatted(ROOT, outputs)

    output_records = parse_files({f"{b}.rs": outputs[f"{b}.rs"] for b in BUCKETS})
    locations = {}
    for record in output_records:
        bucket = Path(record["source"]["path"]).stem
        module = bucket.split("_", 1)[0]
        key = module, collection.normalize(record["literal_target"])
        assert key not in locations and key in seen
        item = selected[key]
        assert originals[item["canonical_api"]]["source_group"] == bucket
        locations[key] = f"{bucket}.rs:{record['source']['start_line']}"
    assert set(locations) == seen
    for item in evidence:
        key = item["module"], collection.normalize(item["canonical_api"])
        owner = owners[item["module"], item["canonical_api"]]
        root_source = "core/src/slice/mod.rs" if item["module"] == "slice" else "alloc/src/vec/mod.rs"
        bucket = item["module"] + ("_mod" if owner["rust_source_file"] == root_source else "_non_mod")
        rows.append({
            "module": item["module"], "canonical_api": item["canonical_api"],
            **owner, "source_group": bucket, "status": item["status"],
            "location": locations.get(key, "existing pinned vstd; no duplicate declaration"),
            "historical_proof_baseline": item["proof_baseline"],
            "historical_scope": item["historical_scope"],
            "new_original_source_proof_claimed": "no",
        })
    rows.sort(key=lambda r: (r["source_group"], r["canonical_api"]))
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    outputs["api_index.tsv"] = buffer.getvalue()
    counts = {bucket: sum(len(items) for items in grouped[bucket].values()) for bucket in BUCKETS}
    assert counts == {"slice_mod": 23, "slice_non_mod": 39, "vec_mod": 7, "vec_non_mod": 29}, counts
    outputs["source_mapping.json"] = json.dumps({
        "schema_version": 1, "original_collection": str(ORIGINAL),
        "original_manifest_sha256": sha(ORIGINAL / "manifest.json"),
        "classification": "Rust1.96 implementation/origin source file, not Self type or trait declaration.",
        "counts": counts, "declarations": originals,
        "contracts_changed": False, "proof_scopes_changed": False,
    }, ensure_ascii=False, indent=2) + "\n"
    return outputs, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    (ROOT / "work").mkdir(parents=True, exist_ok=True)
    outputs, counts = render()
    for name, text in outputs.items():
        path = ROOT / name
        if args.check:
            assert path.read_text() == text, name
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    print(json.dumps({"counts": counts, "checked": args.check}))


if __name__ == "__main__":
    main()
