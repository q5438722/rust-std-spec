#!/usr/bin/env python3
"""Compatibility runner that preserves the independently accepted v6 bytes."""

from __future__ import annotations

from pathlib import Path


_ROOT = Path(__file__).resolve().parents[1]
_ARCHIVED = (
    _ROOT
    / "preservation/archive_v2/tools/run_target_081_operational_v1.py"
)
_MODULE_NAME = __name__
__name__ = "_run_target_081_operational_v1_accepted"
exec(compile(_ARCHIVED.read_bytes(), str(Path(__file__)), "exec"), globals())
__name__ = _MODULE_NAME

_accepted_write_path_policy_v6 = _write_path_policy_v6


def _write_path_policy_v6() -> dict[str, Any]:
    """Never regenerate v6 after its independently accepted v7 successor."""

    if not REVIEW_POLICY_V7.is_file():
        return _accepted_write_path_policy_v6()

    import preservation_policy_v8

    v5_payload = json.loads(PATH_POLICY_V5.read_text())
    v6_payload = json.loads(PATH_POLICY_V6.read_text())
    preservation_policy_v8.validate_target_081_v6(
        v6_payload, v5_payload, root=ROOT
    )
    v6_record = _artifact(PATH_POLICY_V6)
    v7_payload = json.loads(REVIEW_POLICY_V7.read_text())
    preservation._validate_target_081_v7(
        v7_payload,
        root=ROOT,
        expected_parent=v6_record,
    )
    return v6_record


if __name__ == "__main__":
    raise SystemExit(main())
