import argparse
import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def write_config(directory):
    directory = directory.resolve()
    text = (ROOT / "specdet.toml").read_text()
    expected = tomllib.loads(text)
    changes = [
        (expected["project"], "root", ROOT / expected["project"]["root"]),
        (expected["adapters"]["verus"], "executable",
         ROOT / expected["adapters"]["verus"]["executable"]),
        (expected["adapters"]["verus"]["environment"], "TMPDIR", directory / "tmp"),
        (expected["artifacts"], "output_dir", directory / "analysis-runs"),
    ]
    for table, key, path in changes:
        original = f"{key} = {json.dumps(table[key])}"
        if text.count(original) != 1:
            raise ValueError(f"Expected one original {key} assignment in specdet.toml")
        table[key] = str(path.resolve())
        text = text.replace(original, f"{key} = {json.dumps(table[key])}", 1)
    if tomllib.loads(text) != expected:
        raise ValueError("Scratch configuration changed more than the four path settings")
    (directory / "tmp").mkdir(parents=True, exist_ok=True)
    destination = directory / "specdet.toml"
    with destination.open("x") as stream:
        stream.write(text)
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(write_config(args.directory))
