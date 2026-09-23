#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export RUSTUP_HOME="$PWD/toolchains/rustup"
export CARGO_HOME="$PWD/toolchains/cargo"
export TMPDIR="$PWD/toolchains/tmp"
mkdir -p "$TMPDIR" toolchains/downloads toolchains/upstream toolchains/readiness

curl --fail --location --silent --show-error \
  'https://github.com/verus-lang/verus/releases/download/release/0.2026.09.20.aef82ed/verus-0.2026.09.20.aef82ed-x86-linux.zip' \
  --output toolchains/downloads/verus-0.2026.09.20.aef82ed-x86-linux.zip
printf '%s\n' \
  '7b870fa12bc589015c2fab60a8b3d9f07c7b1adb3444eb0fadffcbf7f0447b33  toolchains/downloads/verus-0.2026.09.20.aef82ed-x86-linux.zip' \
  | sha256sum --check
unzip -q toolchains/downloads/verus-0.2026.09.20.aef82ed-x86-linux.zip -d toolchains

curl --fail --location --silent --show-error \
  'https://codeload.github.com/verus-lang/verus/tar.gz/aef82eda71838deef4a8cd0260fda6c9504be9b9' \
  --output toolchains/downloads/verus-aef82eda71838deef4a8cd0260fda6c9504be9b9.tar.gz
tar -xzf toolchains/downloads/verus-aef82eda71838deef4a8cd0260fda6c9504be9b9.tar.gz \
  --directory toolchains/upstream --strip-components=1

rustup toolchain install 1.98.1 --profile minimal --no-self-update \
  --component rustfmt --component rustc-dev --component llvm-tools
rustup run 1.98.1 rustc --version --verbose
toolchains/verus-x86-linux/verus --version
