#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export RUSTUP_HOME="$PWD/toolchains/rustup"
export CARGO_HOME="$PWD/toolchains/cargo"
export TMPDIR="$PWD/toolchains/tmp"
export PYTHONDONTWRITEBYTECODE=1
export RUSTC_BOOTSTRAP=1
exec "$@"
