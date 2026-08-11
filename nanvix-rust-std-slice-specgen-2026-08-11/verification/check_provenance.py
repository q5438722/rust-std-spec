#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path


RUST_SLICE_SOURCE = Path(
    "/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src/slice"
)
VSTD_SOURCE = Path("/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/vstd")
VSTD_RELATIVE_FILES = ("slice.rs", "std_specs/slice.rs")
MANIFEST_CSV = Path("provenance/source_manifest.csv")
MANIFEST_JSON = Path("provenance/source_manifest.json")
FIELDS = ("component", "relative_path", "source_path", "dest_path", "sha256", "bytes")


def fail(message: str) -> None:
    print(f"provenance check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_set(root: Path) -> set[str]:
    if not root.is_dir():
        fail(f"missing directory {root}")
    return {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}


def expected_rows(root: Path, rust_copy: Path, vstd_copy: Path) -> list[dict[str, str]]:
    if not RUST_SLICE_SOURCE.is_dir():
        fail(f"missing Rust source {RUST_SLICE_SOURCE}")
    if not VSTD_SOURCE.is_dir():
        fail(f"missing vstd source {VSTD_SOURCE}")

    rows: list[dict[str, str]] = []
    for source in sorted(path for path in RUST_SLICE_SOURCE.rglob("*") if path.is_file()):
        rel = source.relative_to(RUST_SLICE_SOURCE).as_posix()
        rows.append(
            {
                "component": "rust-core-slice",
                "relative_path": rel,
                "source_path": str(source),
                "dest_path": (rust_copy / rel).relative_to(root).as_posix(),
                "sha256": sha256(source),
                "bytes": str(source.stat().st_size),
            }
        )

    for rel in VSTD_RELATIVE_FILES:
        source = VSTD_SOURCE / rel
        if not source.is_file():
            fail(f"missing vstd source file {source}")
        rows.append(
            {
                "component": "vstd-baseline",
                "relative_path": rel,
                "source_path": str(source),
                "dest_path": (vstd_copy / rel).relative_to(root).as_posix(),
                "sha256": sha256(source),
                "bytes": str(source.stat().st_size),
            }
        )
    return rows


def read_manifest_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing manifest {path}")
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            fail(f"{path} has fields {reader.fieldnames}, expected {list(FIELDS)}")
        rows = list(reader)
    seen: set[tuple[str, str]] = set()
    for row in rows:
        key = (row["component"], row["relative_path"])
        if key in seen:
            fail(f"duplicate manifest row {key}")
        seen.add(key)
    return rows


def read_manifest_json(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing manifest {path}")
    with path.open() as stream:
        payload = json.load(stream)
    if not isinstance(payload, dict) or "rows" not in payload:
        fail(f"{path} must contain an object with a rows array")
    rows = payload["rows"]
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        fail(f"{path} rows must be a list of objects")
    return rows


def validate_manifest_rows(root: Path, rows: list[dict[str, str]], expected: list[dict[str, str]]) -> None:
    if rows != expected:
        actual_keys = {(row.get("component"), row.get("relative_path")) for row in rows}
        expected_keys = {(row["component"], row["relative_path"]) for row in expected}
        missing = sorted(expected_keys - actual_keys)
        extra = sorted(actual_keys - expected_keys)
        details = []
        if missing:
            details.append(f"missing rows={missing[:10]}")
        if extra:
            details.append(f"extra rows={extra[:10]}")
        if not details:
            details.append("row metadata differs from source hashes/paths")
        fail("; ".join(details))

    for row in rows:
        dest = root / row["dest_path"]
        source = Path(row["source_path"])
        if not dest.is_file():
            fail(f"missing copied file {dest}")
        if dest.stat().st_size != source.stat().st_size:
            fail(f"byte size mismatch for {dest}")
        if sha256(dest) != row["sha256"]:
            fail(f"copied file hash mismatch for {dest}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate isolated core::slice source provenance.")
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--rust-copy", required=True, type=Path)
    parser.add_argument("--vstd-copy", required=True, type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    rust_copy = (root / args.rust_copy).resolve()
    vstd_copy = (root / args.vstd_copy).resolve()

    if not root.is_dir():
        fail(f"missing experiment root {root}")
    if not rust_copy.is_relative_to(root) or not vstd_copy.is_relative_to(root):
        fail("copy paths must resolve inside the experiment root")

    expected = expected_rows(root, rust_copy, vstd_copy)
    expected_rust = {
        row["relative_path"] for row in expected if row["component"] == "rust-core-slice"
    }
    expected_vstd = {
        row["relative_path"] for row in expected if row["component"] == "vstd-baseline"
    }

    copied_rust = file_set(rust_copy)
    copied_vstd = file_set(vstd_copy)
    if copied_rust != expected_rust:
        fail(
            "rust-core-slice copy differs from source: "
            f"missing={sorted(expected_rust - copied_rust)[:10]} "
            f"extra={sorted(copied_rust - expected_rust)[:10]}"
        )
    if copied_vstd != expected_vstd:
        fail(
            "vstd-baseline copy differs from required files: "
            f"missing={sorted(expected_vstd - copied_vstd)[:10]} "
            f"extra={sorted(copied_vstd - expected_vstd)[:10]}"
        )

    csv_rows = read_manifest_csv(root / MANIFEST_CSV)
    json_rows = read_manifest_json(root / MANIFEST_JSON)
    validate_manifest_rows(root, csv_rows, expected)
    if json_rows != csv_rows:
        fail("JSON provenance manifest does not match CSV manifest")

    print(
        "provenance ok: "
        f"rust-core-slice files={len(expected_rust)}, "
        f"vstd-baseline files={len(expected_vstd)}, "
        f"manifest rows={len(csv_rows)}"
    )


if __name__ == "__main__":
    main()
