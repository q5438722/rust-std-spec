#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import run_acceptance


class AcceptanceTimeoutTests(unittest.TestCase):
    def test_timeout_bytes_are_reported_as_text(self) -> None:
        process = mock.Mock()
        process.communicate.return_value = (
            b"partial stdout",
            b"partial stderr",
        )
        with tempfile.TemporaryDirectory() as directory:
            logs = Path(directory)
            with (
                mock.patch.object(run_acceptance, "LOGS", logs),
                mock.patch.object(
                    run_acceptance.common,
                    "relpath",
                    side_effect=lambda path: str(path),
                ),
                mock.patch.object(
                    run_acceptance.subprocess,
                    "Popen",
                    return_value=process,
                ),
                mock.patch.object(
                    run_acceptance.time,
                    "monotonic",
                    side_effect=(0.0, 2.0),
                ),
            ):
                record = run_acceptance.capture(
                    "timeout",
                    ["slow-command"],
                    cwd=ROOT,
                    timeout=1,
                )

            self.assertEqual(record["exit_code"], 124)
            process.kill.assert_called_once_with()
            self.assertEqual(
                (logs / "timeout.stdout.txt").read_text(),
                "partial stdout",
            )
            self.assertEqual(
                (logs / "timeout.stderr.txt").read_text(),
                "partial stderr\ncommand timed out\n",
            )

    def test_complete_suite_has_acceptance_scale_timeout(self) -> None:
        self.assertEqual(run_acceptance.command_timeout("02_unit_tests"), 900)
        self.assertEqual(
            run_acceptance.command_timeout(
                "44b_target_079_operational_v1"
            ),
            600,
        )
        self.assertEqual(
            run_acceptance.command_timeout(
                "44e_target_078_insert_tail_refinement_v3"
            ),
            600,
        )
        self.assertEqual(
            run_acceptance.command_timeout(
                "44f_target_079_insert_tail_refinement_v3"
            ),
            600,
        )
        self.assertEqual(
            run_acceptance.command_timeout(
                "44h_target_081_operational_v1"
            ),
            600,
        )
        self.assertEqual(run_acceptance.command_timeout("03_builder"), 110)
        self.assertEqual(
            run_acceptance.MINIMUM_TEST_COUNTS["02_unit_tests"],
            777,
        )

    def test_long_command_emits_heartbeat_without_losing_output(self) -> None:
        process = mock.Mock(returncode=0)
        process.communicate.side_effect = (
            subprocess.TimeoutExpired(["slow-command"], 20),
            ("complete stdout\n", ""),
        )
        with tempfile.TemporaryDirectory() as directory:
            logs = Path(directory)
            with (
                mock.patch.object(run_acceptance, "LOGS", logs),
                mock.patch.object(
                    run_acceptance.common,
                    "relpath",
                    side_effect=lambda path: str(path),
                ),
                mock.patch.object(
                    run_acceptance.subprocess,
                    "Popen",
                    return_value=process,
                ),
                mock.patch.object(
                    run_acceptance.time,
                    "monotonic",
                    side_effect=(0.0, 0.0, 20.0, 20.0),
                ),
                mock.patch("builtins.print") as output,
            ):
                record = run_acceptance.capture(
                    "heartbeat",
                    ["slow-command"],
                    cwd=ROOT,
                    timeout=60,
                )

            self.assertEqual(record["exit_code"], 0)
            self.assertEqual(
                (logs / "heartbeat.stdout.txt").read_text(),
                "complete stdout\n",
            )
            self.assertTrue(
                any(
                    call.args
                    and call.args[0].startswith(
                        "acceptance_command_heartbeat=heartbeat"
                    )
                    for call in output.call_args_list
                )
            )

    def test_unittest_count_requires_one_nonzero_summary(self) -> None:
        self.assertEqual(
            run_acceptance.unittest_count("", "Ran 15 tests in 1.000s\n"),
            15,
        )
        self.assertEqual(
            run_acceptance.unittest_count("", "Ran 0 tests in 0.000s\n"),
            0,
        )
        self.assertIsNone(run_acceptance.unittest_count("", "OK\n"))
        self.assertIsNone(
            run_acceptance.unittest_count(
                "Ran 1 test in 0.001s\n",
                "Ran 2 tests in 0.002s\n",
            )
        )

    def test_v3_evidence_is_rebuilt_before_tests(self) -> None:
        source = Path(run_acceptance.__file__).read_text()
        start = source.index("commands = [")
        end = source.index("records: list", start)
        commands = source[start:end]
        target_078_adapter = commands.index(
            '"44d_target_078_adapter_refinement_v2"'
        )
        target_078_producer = commands.index(
            '"44e_target_078_insert_tail_refinement_v3"'
        )
        target_079_producer = commands.index(
            '"44f_target_079_insert_tail_refinement_v3"'
        )
        target_079_adapter = commands.index(
            '"44c_target_079_adapter_refinement_v2"'
        )
        self.assertLess(target_079_adapter, target_078_adapter)
        self.assertLess(target_078_adapter, target_078_producer)
        self.assertLess(target_079_adapter, target_079_producer)
        for producer in (target_078_producer, target_079_producer):
            self.assertLess(
                producer,
                commands.index(
                    '"01b_operational_v2_certification_tests"'
                ),
            )
            self.assertLess(producer, commands.index('"02_unit_tests"'))
            self.assertLess(producer, commands.index('"22_local_validator"'))

    def test_target_078_adapter_uses_reproducible_affinity(self) -> None:
        with mock.patch.object(
            run_acceptance.shutil,
            "which",
            return_value="/usr/bin/taskset",
        ):
            self.assertEqual(
                run_acceptance.target_078_adapter_command("/usr/bin/python3"),
                [
                    "/usr/bin/taskset",
                    "-c",
                    "0-3",
                    "/usr/bin/python3",
                    "tools/run_target_078_adapter_refinement_v2.py",
                ],
            )

    def test_v4_evidence_is_rebuilt_before_policy_consumers(self) -> None:
        source = Path(run_acceptance.__file__).read_text()
        start = source.index("commands = [")
        end = source.index("records: list", start)
        commands = source[start:end]
        builder = commands.index('"03_builder"')
        last_ledger_producer = commands.index('"43_align_to_pair"')
        target_080_producer = commands.index(
            '"44g_target_080_operational_v1"'
        )
        target_079_producer = commands.index(
            '"44b_target_079_operational_v1"'
        )
        final_reconciliation = commands.index(
            '"44_final_reconciliation"'
        )
        operational_v2_reconciliation = commands.index(
            '"45_operational_v2_reconciliation"'
        )
        certification_closure = commands.index(
            '"46_operational_v2_certification_closure"'
        )
        target_079_adapter = commands.index(
            '"44c_target_079_adapter_refinement_v2"'
        )
        target_078_adapter = commands.index(
            '"44d_target_078_adapter_refinement_v2"'
        )
        target_081_producer = commands.index(
            '"44h_target_081_operational_v1"'
        )
        self.assertLess(builder, last_ledger_producer)
        self.assertLess(last_ledger_producer, target_080_producer)
        self.assertLess(target_080_producer, target_081_producer)
        self.assertLess(builder, target_081_producer)
        self.assertLess(target_080_producer, target_079_producer)
        self.assertLess(target_079_producer, final_reconciliation)
        self.assertLess(
            final_reconciliation,
            operational_v2_reconciliation,
        )
        self.assertLess(
            operational_v2_reconciliation,
            certification_closure,
        )
        self.assertLess(certification_closure, target_079_adapter)
        self.assertLess(target_079_adapter, target_078_adapter)
        for consumer in (
            "44e_target_078_insert_tail_refinement_v3",
            "44f_target_079_insert_tail_refinement_v3",
        ):
            self.assertLess(
                certification_closure,
                commands.index(f'"{consumer}"'),
            )
            self.assertLess(
                target_078_adapter,
                commands.index(f'"{consumer}"'),
            )
        self.assertLess(
            target_081_producer,
            commands.index('"02_unit_tests"'),
        )


if __name__ == "__main__":
    unittest.main()
