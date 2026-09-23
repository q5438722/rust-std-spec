import json
import tarfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "toolchains"
COMMIT = "aef82eda71838deef4a8cd0260fda6c9504be9b9"


def main():
    release = TOOLS / "downloads/verus-0.2026.09.20.aef82ed-x86-linux.zip"
    files = 0
    with zipfile.ZipFile(release) as archive:
        for entry in archive.infolist():
            if entry.is_dir():
                continue
            actual = TOOLS / entry.filename
            assert actual.is_file(), f"Missing release file: {actual}"
            assert actual.read_bytes() == archive.read(entry), f"Changed release file: {actual}"
            files += 1
    source_files = 0
    source_archive = TOOLS / f"downloads/verus-{COMMIT}.tar.gz"
    with tarfile.open(source_archive) as archive:
        for entry in archive.getmembers():
            if not entry.isfile():
                continue
            relative = Path(*Path(entry.name).parts[1:])
            if relative.parts[:2] != ("source", "vstd"):
                continue
            original = archive.extractfile(entry)
            assert original is not None
            assert (TOOLS / "upstream" / relative).read_bytes() == original.read(), relative
            source_files += 1
    version = json.loads((TOOLS / "verus-x86-linux/version.json").read_text())
    assert COMMIT in json.dumps(version), version
    toolchain = (TOOLS / "upstream/rust-toolchain.toml").read_text()
    assert 'channel = "1.98.1"' in toolchain
    print(json.dumps({
        "release": "release/0.2026.09.20.aef82ed",
        "upstream_commit": COMMIT,
        "release_files_byte_equal": files,
        "vstd_source_files_byte_equal": source_files,
        "compiled_vstd": ["toolchains/verus-x86-linux/libvstd.rlib",
                          "toolchains/verus-x86-linux/vstd.vir"],
        "rust_toolchain": "1.98.1-x86_64-unknown-linux-gnu",
        "version": version,
    }, indent=2))


if __name__ == "__main__":
    main()
