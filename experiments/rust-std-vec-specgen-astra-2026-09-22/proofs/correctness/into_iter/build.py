import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests"))
from test_with_capacity_isolation import run


def main():
    output = Path(sys.argv[1]).resolve()
    names = sys.argv[2:] or ["bindings", "count", "last"]
    if not names or set(names) - {"bindings", "count", "last"}:
        raise ValueError("select bindings, count, or last")
    output.mkdir(parents=True, exist_ok=False)
    (output / "tmp").mkdir()
    (output / "build").mkdir()
    shutil.copyfile(
        ROOT / "proofs/correctness/into_iter/source.rs", output / "source.rs",
    )
    shutil.copyfile(
        ROOT / "proofs/correctness/into_iter/source_last.rs", output / "source_last.rs",
    )
    shutil.copyfile(
        ROOT / "proofs/correctness/into_iter/isolated/consumers.rs",
        output / "consumers.source.rs",
    )
    shutil.copyfile(
        ROOT / "proofs/correctness/into_iter/isolated/iterator_methods.rs",
        output / "iterator_methods.source.rs",
    )
    for name in names:
        entry = ROOT / (
            "proofs/correctness/into_iter/isolated/lib.rs" if name == "bindings"
            else f"proofs/correctness/into_iter/{name}.rs"
        )
        shutil.copyfile(entry, output / f"{name}.source.rs")
        crate = f"into_iter_{name}"
        library = output / "build" / f"lib{crate}.rlib"
        command = [
            str(ROOT / "toolchains/verus-x86-linux/verus"), str(entry),
            "--edition=2021", "--crate-type=lib", "--crate-name", crate,
            "--compile", "--num-threads=1", "--trace", "--log-all",
            "--log-dir", str(output / name), "-o", str(library),
        ]
        if name != "bindings":
            command += [
                "--verify-only-module", "source", "--verify-function", f"IntoIter::{name}",
            ]
        result = run(output, name, command)
        result.check_returncode()
        text = (output / f"{name}.stdout").read_text()
        expected = 0 if name == "bindings" else 1
        if f"verification results:: {expected} verified, 0 errors" not in text:
            raise AssertionError(f"{name}: expected {expected} source obligations\n{text}")
        receipt = json.loads((output / f"{name}.result.json").read_text())
        if not receipt["started_ns"] <= library.stat().st_mtime_ns <= receipt["finished_ns"]:
            raise AssertionError(f"{name}: library is not from this build")
        print(f"{name}: {expected} verified; compiled {library.name}", flush=True)


if __name__ == "__main__":
    main()
