#!/usr/bin/env python3
"""Organize proved and blocked contracts by original vstd source file."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import sys


HERE = Path(__file__).resolve().parent
SOURCE_VERIFICATION = HERE.parent
WORKSPACE = SOURCE_VERIFICATION.parent
PROVED_ROOT = SOURCE_VERIFICATION / "proved-apis"
SUITE_ROOT = SOURCE_VERIFICATION / "organized-suite"
sys.path.insert(0, str(WORKSPACE))

from run_rust_std_spec_feedback import assume_to_synthetic


FEATURES = [
    "allocator_api",
    "box_into_inner",
    "const_trait_impl",
    "exact_size_is_empty",
    "iter_advance_by",
    "layout_for_ptr",
    "maybe_uninit_as_bytes",
    "maybe_uninit_array_assume_init",
    "never_type",
    "nonzero_internals",
    "ptr_metadata",
    "slice_ptr_get",
    "sized_hierarchy",
    "step_trait",
    "trusted_len",
    "unsized_fn_params",
]


def safe(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", value).strip("_")


def identifier(value: str) -> str:
    result = re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_").lower()
    return result if result and not result[0].isdigit() else f"generated_{result}"


def group_name(source_file: str) -> str:
    return safe(str(Path(source_file).with_suffix("")))


def record_directory_name(target_id: str) -> str:
    return safe(re.sub(r"\.rs(?=__|$)", "", target_id, count=1))


def remove_source_function_prefixes(path: Path) -> None:
    text = path.read_text(errors="replace")
    names = set(
        re.findall(
            r"\b(?:pub\s+)?(?:proof\s+|spec\s+|exec\s+|const\s+|unsafe\s+)*"
            r"fn\s+(source_[A-Za-z_][A-Za-z0-9_]*)",
            text,
        )
    )
    if not names:
        return
    all_functions = set(
        re.findall(
            r"\b(?:pub\s+)?(?:proof\s+|spec\s+|exec\s+|const\s+|unsafe\s+)*"
            r"fn\s+([A-Za-z_][A-Za-z0-9_]*)",
            text,
        )
    )
    renames = {
        name: f"{name.removeprefix('source_')}_proof" for name in names
    }
    assert len(set(renames.values())) == len(renames)
    assert not (set(renames.values()) & (all_functions - names))
    for old, new in sorted(renames.items(), key=lambda item: -len(item[0])):
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    path.write_text(text)


def resolve_import(source_file: str, value: str) -> str:
    value = value.strip()
    module = ["vstd", *Path(source_file).with_suffix("").parts]
    relative = False
    while value.startswith("super::"):
        relative = True
        value = value[len("super::") :]
        module.pop()
    if value.startswith("crate::"):
        relative = True
        value = value[len("crate::") :]
        module = ["vstd"]
    if value.startswith("self::"):
        relative = True
        value = value[len("self::") :]
    if not relative and value.startswith(("core::", "alloc::", "std::", "vstd::", "verus")):
        return value
    return "::".join([*module, value])


def original_imports(source_file: str) -> str:
    path = WORKSPACE / "verus" / "source" / "vstd" / source_file
    text = path.read_text(errors="replace")
    marker_positions = [
        position
        for marker in ("verus! {", "verus_! {")
        if (position := text.find(marker)) >= 0
    ]
    prefix = text[: min(marker_positions)] if marker_positions else text[:10000]
    imports = []
    for match in re.finditer(r"(?m)^(?:pub\s+)?use\s+(.+?);", prefix, flags=re.DOTALL):
        value = re.sub(r"\s+", " ", match.group(1)).strip()
        if value.startswith("verus as "):
            continue
        value = value.replace(", TrustedSpecSealed", "").replace(
            "TrustedSpecSealed, ",
            "",
        )
        imports.append(f"use {resolve_import(source_file, value)};")
    return "\n".join(dict.fromkeys(imports))


def external_body_source(target: dict) -> str:
    synthetic = assume_to_synthetic(target["contract_code"])
    name = "external_" + identifier(target["id"])
    synthetic = synthetic.replace(
        "pub exec fn __rust_std_candidate",
        f"#[verifier::external_body]\npub fn {name}",
        1,
    )
    feature_lines = "".join(f"#![feature({feature})]\n" for feature in FEATURES)
    return (
        "#![allow(dead_code, unused_imports, unused_variables)]\n"
        f"{feature_lines}"
        "extern crate alloc;\n"
        "use vstd::prelude::*;\n"
        f"{original_imports(target['contract_source_file'])}\n"
        f"use {target['suggested_vstd_import']};\n"
        "verus! {\n\n"
        f"{synthetic}\n"
        "}\n\n"
        "fn main() {}\n"
    )


def main() -> None:
    manifest = json.loads((HERE / "manifest.json").read_text())
    targets = {target["id"]: target for target in manifest["targets"]}
    overall = json.loads((HERE / "OVERALL.json").read_text())
    results = {result["id"]: result for result in overall["results"]}
    verdict_path = SOURCE_VERIFICATION / "fidelity-verdicts.json"
    verdicts = json.loads(verdict_path.read_text()) if verdict_path.is_file() else {}
    downgraded = set(verdicts.get("downgraded", []))

    if SUITE_ROOT.exists():
        shutil.rmtree(SUITE_ROOT)
    SUITE_ROOT.mkdir(parents=True)
    groups: dict[str, dict] = {}
    directory_paths: set[Path] = set()
    for target_id, target in targets.items():
        result = results[target_id]
        source_file = target["contract_source_file"]
        group = groups.setdefault(
            source_file,
            {
                "source_file": source_file,
                "proved": [],
                "external_body": [],
            },
        )
        group_dir = SUITE_ROOT / group_name(source_file)
        if result["status"] in {"proved", "preproved"} and target_id not in downgraded:
            source_dir = PROVED_ROOT / target_id
            destination = group_dir / "proved" / record_directory_name(target_id)
            assert destination not in directory_paths, destination
            directory_paths.add(destination)
            destination.mkdir(parents=True, exist_ok=True)
            for filename in (
                "proof.rs",
                "contract.rs",
                "rust_source.rs",
                "api.json",
                "metadata.json",
            ):
                path = source_dir / filename
                if path.is_file():
                    shutil.copy2(path, destination / filename)
            remove_source_function_prefixes(destination / "proof.rs")
            group["proved"].append(
                {
                    "id": target_id,
                    "api_path": target["api_path"],
                    "path": str((destination / "proof.rs").relative_to(SUITE_ROOT)),
                }
            )
        else:
            destination = (
                group_dir / "external_body" / record_directory_name(target_id)
            )
            assert destination not in directory_paths, destination
            directory_paths.add(destination)
            destination.mkdir(parents=True, exist_ok=True)
            external_path = destination / "external_body.rs"
            external_path.write_text(external_body_source(target))
            (destination / "contract.rs").write_text(
                target["contract_code"].rstrip() + "\n"
            )
            (destination / "metadata.json").write_text(
                json.dumps(
                    {
                        "id": target_id,
                        "api_path": target["api_path"],
                        "raw_target": target["raw_target"],
                        "contract_source_file": source_file,
                        "contract_source_line": target["contract_source_line"],
                        "status": result["status"],
                        "blocker": (
                            "Not retained by the conservative source-surrogate audit; "
                            "see source-verification/surrogate-audit/records.csv."
                            if target_id in downgraded
                            else result.get("blocker", "")
                        ),
                        "fidelity_downgraded": target_id in downgraded,
                    },
                    indent=2,
                )
                + "\n"
            )
            group["external_body"].append(
                {
                    "id": target_id,
                    "api_path": target["api_path"],
                    "path": str(external_path.relative_to(SUITE_ROOT)),
                }
            )

    for source_file, group in groups.items():
        group_dir = SUITE_ROOT / group_name(source_file)
        (group_dir / "manifest.json").write_text(json.dumps(group, indent=2) + "\n")

    suite = {
        "counts": {
            "groups": len(groups),
            "proved": sum(len(group["proved"]) for group in groups.values()),
            "external_body": sum(
                len(group["external_body"]) for group in groups.values()
            ),
        },
        "groups": [groups[key] for key in sorted(groups)],
    }
    (SUITE_ROOT / "manifest.json").write_text(json.dumps(suite, indent=2) + "\n")
    (SUITE_ROOT / "verify.sh").write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        'SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"\n'
        'WORKSPACE="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"\n\n'
        'exec "${WORKSPACE}/.venv/bin/python" \\\n'
        '  "${WORKSPACE}/source-verification/bulk-proof/verify_organized_suite.py" \\\n'
        '  --suite "${SCRIPT_DIR}" \\\n'
        '  "$@"\n'
    )
    (SUITE_ROOT / "verify.sh").chmod(0o755)
    print(json.dumps(suite["counts"], indent=2))


if __name__ == "__main__":
    main()
