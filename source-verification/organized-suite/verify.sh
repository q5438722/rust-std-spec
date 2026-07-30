#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"

exec "${WORKSPACE}/.venv/bin/python" \
  "${WORKSPACE}/source-verification/bulk-proof/verify_organized_suite.py" \
  --suite "${SCRIPT_DIR}" \
  "$@"
