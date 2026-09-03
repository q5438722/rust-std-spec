#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import target_082_operational_smt_v1 as smt
import target_082_operational_v1 as model
import target_082_operational_witness_v1 as witnesses
import target_082_source_interpreter_v1 as reference


class Target082OperationalV1Tests(unittest.TestCase):
    def test_model_is_source_complete_and_replaces_three_opaque_sites(
        self,
    ) -> None:
        self.assertTrue(model.SOURCE_MODEL_COMPLETE)
        self.assertTrue(model.CLASSIFICATION_ELIGIBLE)
        self.assertEqual(model.MISSING_SOURCE_PHASES, ())
        self.assertEqual(
            model.REPLACED_TRUST_SITE_IDS,
            ("TS-082-D002", "TS-082-D003", "TS-082-E001"),
        )
        self.assertEqual(model.ADMITTED_TRUST_SITE_IDS, ("TS-082-D004",))

    def test_normal_adapter_order_and_owned_key_identity(self) -> None:
        adapter = model.KeyOrdDropAdapter(
            model.mapped_key_boundary({1: 0, 2: 0})
        )
        result = adapter.transition(0, 1, 2)
        self.assertEqual(result.terminal_status, model.NORMAL)
        self.assertEqual(
            [event.action for event in result.events],
            [
                "key-left",
                "key-right",
                "ord-lt",
                "drop-key-right",
                "drop-key-left",
            ],
        )
        left = result.events[2].left_owned_key
        right = result.events[2].right_owned_key
        self.assertIsNotNone(left)
        self.assertIsNotNone(right)
        self.assertNotEqual(left, right)
        self.assertEqual(left.key_identity, right.key_identity)
        self.assertEqual(left.slot, model.KeySlot.LEFT)
        self.assertEqual(right.slot, model.KeySlot.RIGHT)

    def test_left_and_right_key_panic_prefixes(self) -> None:
        left = model.KeyOrdDropAdapter(
            model.KeySortBoundary(
                key_panic_calls=frozenset(
                    {model.KeyCallKey(0, model.KeySlot.LEFT, 1)}
                )
            )
        ).transition(0, 1, 2)
        self.assertEqual([event.action for event in left.events], ["key-left"])
        self.assertEqual(left.terminal_status, model.PANIC)

        right = model.KeyOrdDropAdapter(
            model.KeySortBoundary(
                key_panic_calls=frozenset(
                    {model.KeyCallKey(1, model.KeySlot.RIGHT, 2)}
                )
            )
        ).transition(0, 1, 2)
        self.assertEqual(
            [event.action for event in right.events],
            ["key-left", "key-right", "drop-key-left"],
        )
        self.assertTrue(right.events[-1].unwinding)

    def test_ord_panic_precedes_boolean_result_and_drops_right_first(
        self,
    ) -> None:
        result = model.KeyOrdDropAdapter(
            model.KeySortBoundary(ord_panic_states=frozenset({2}))
        ).transition(0, 1, 2)
        self.assertEqual(result.terminal_status, model.PANIC)
        self.assertIsNone(result.is_less)
        ord_event = result.events[2]
        self.assertTrue(ord_event.panicked)
        self.assertFalse(ord_event.result_available)
        self.assertIsNone(ord_event.is_less)
        self.assertEqual(
            [event.action for event in result.events[-2:]],
            ["drop-key-right", "drop-key-left"],
        )
        self.assertTrue(all(event.unwinding for event in result.events[-2:]))

    def test_right_drop_panic_still_unwinds_left(self) -> None:
        result = model.KeyOrdDropAdapter(
            model.KeySortBoundary(
                key_drop_panic_normal=frozenset(
                    {model.KeyDropKey(3, model.KeySlot.RIGHT)}
                )
            )
        ).transition(0, 1, 2)
        self.assertEqual(result.terminal_status, model.PANIC)
        self.assertTrue(result.events[-2].panicked)
        self.assertFalse(result.events[-2].unwinding)
        self.assertEqual(result.events[-1].action, "drop-key-left")
        self.assertTrue(result.events[-1].unwinding)

    def test_double_panic_aborts_without_later_cleanup(self) -> None:
        boundary = model.KeySortBoundary(
            ord_panic_states=frozenset({2}),
            key_drop_panic_unwind=frozenset(
                {model.KeyDropKey(3, model.KeySlot.RIGHT)}
            ),
        )
        adapter = model.KeyOrdDropAdapter(boundary)
        result = adapter.transition(0, 1, 2)
        self.assertEqual(result.terminal_status, model.ABORT)
        self.assertEqual(result.events[-1].action, "drop-key-right")
        self.assertNotIn(
            "drop-key-left", [event.action for event in result.events]
        )
        execution = model.execute(model.SortInput((2, 1)), boundary)
        self.assertEqual(execution.terminal_status, model.ABORT)
        self.assertFalse(execution.state.f_drop_invoked)

    def test_smt_private_composition_preserves_three_way_status(self) -> None:
        fixed = smt.fixed_boundary_determinism_text()
        for required in (
            "KEncodePrivateState082",
            "KPrivateCallbackState082",
            "KPrivateTerminalStatus082",
            "AdapterAtPrivateCall082",
            "PrivateResult082",
        ):
            self.assertIn(required, fixed)
        self.assertNotIn(
            "(ite (e_panicked private) 1 0)",
            fixed,
        )
        valid = smt.composition_regression_text(
            "adapter-abort-preserved"
        )
        invalid = smt.composition_regression_text(
            "adapter-abort-to-panic-f-drop"
        )
        self.assertIn("(= (kar_status regressionAdapter082) 2)", valid)
        self.assertIn("(kpub_aborted regressionPublic082)", valid)
        self.assertIn(
            "(not (kpub_f_drop_invoked regressionPublic082))",
            valid,
        )
        self.assertIn("(kpub_f_drop_invoked regressionPublic082)", invalid)

    def test_f_drop_normal_panic_and_double_panic_are_distinct(self) -> None:
        normal = model.execute(
            model.SortInput(()),
            model.KeySortBoundary(
                initial_state=4,
                f_drop_next_state_mode=model.INCREMENT_STATE,
            ),
        )
        self.assertEqual(normal.terminal_status, model.NORMAL)
        self.assertEqual(normal.state.callback_state, 5)
        self.assertTrue(normal.state.f_drop_completed)

        panic = model.execute(
            model.SortInput(()),
            model.KeySortBoundary(
                f_drop_panic_normal_states=frozenset({0})
            ),
        )
        self.assertEqual(panic.terminal_status, model.PANIC)
        self.assertFalse(panic.state.f_drop_completed)

        abort = model.execute(
            model.SortInput((2, 1)),
            model.KeySortBoundary(
                key_panic_calls=frozenset(
                    {model.KeyCallKey(0, model.KeySlot.LEFT, 1)}
                ),
                f_drop_panic_unwind_states=frozenset({1}),
            ),
        )
        self.assertEqual(abort.terminal_status, model.ABORT)
        self.assertEqual(abort.abort_phase, "drop-f-during-unwind")

    def test_callback_and_complete_interior_state_are_observable(self) -> None:
        boundary = model.KeySortBoundary(
            initial_state=2,
            initial_observable_element_state=(1, 4),
            key_interior_mode=model.INCREMENT_STATE,
            ord_interior_mode=model.INCREMENT_STATE,
            key_drop_interior_mode=model.INCREMENT_STATE,
            f_drop_interior_mode=model.INCREMENT_STATE,
            f_drop_next_state_mode=model.INCREMENT_STATE,
        )
        primary = model.execute(model.SortInput((2, 1)), boundary)
        independent = reference.execute(
            (2, 1), model.SourceConfiguration(), boundary
        )
        self.assertEqual(primary.state, independent.state)
        self.assertEqual(
            primary.state.observable_element_state,
            (7, 10),
        )
        self.assertEqual(primary.state.callback_state, 8)

    def test_all_paired_witnesses_replay_field_for_field(self) -> None:
        payload = witnesses.witness_payload()
        self.assertGreaterEqual(payload["case_count"], 25)
        self.assertEqual(
            set(payload["terminal_statuses"]),
            {model.NORMAL, model.PANIC, model.ABORT},
        )
        names = set(payload["cases"])
        for required in (
            "duplicate-equal-owned-keys",
            "ord-lt-panic-right-then-left-unwind-drop",
            "ord-panic-right-drop-double-panic-abort",
            "callback-and-element-interior-mutation",
            "inherited-configuration-heapsort-size",
            "inherited-fallback-small-sort-and-recursion",
        ):
            self.assertIn(required, names)
        for name, case in payload["cases"].items():
            with self.subTest(name=name):
                self.assertEqual(case["primary"], case["independent"])
                self.assertTrue(case["correspondence"]["field_complete"])
                self.assertTrue(
                    case["correspondence"]["adapter_events_equal"]
                )
                self.assertTrue(
                    case["correspondence"]["source_ordered_temporaries"]
                )

    def test_boundary_contains_no_answer_schedule_or_trace(self) -> None:
        fields = set(model.KeySortBoundary.__dataclass_fields__)
        for forbidden in (
            "schedule",
            "temporary_lifetimes",
            "pivot",
            "writes",
            "output",
            "final_state",
            "trace",
        ):
            self.assertNotIn(forbidden, fields)
        manifest = model.boundary_manifest()
        self.assertTrue(manifest["boundary_narrower_than_target"])
        self.assertEqual(
            manifest["admitted_trust_site_ids"], ["TS-082-D004"]
        )
        shared = json.dumps(manifest["shared_boundary_observations"])
        self.assertIn("K::lt", shared)
        self.assertIn("owned-K Drop", shared)
        self.assertIn("owned-F Drop", shared)

    def test_boundary_serialization_round_trip(self) -> None:
        boundary = model.mapped_key_boundary(
            {1: 0, 2: 0},
            initial_state=-2,
            initial_observable_element_state=(7, 11),
            key_panic_calls=frozenset(
                {model.KeyCallKey(-2, model.KeySlot.LEFT, 1)}
            ),
            key_drop_panic_unwind=frozenset(
                {model.KeyDropKey(-1, model.KeySlot.LEFT)}
            ),
            f_drop_panic_unwind_states=frozenset({4}),
        )
        record = witnesses.boundary_record(boundary)
        self.assertEqual(witnesses.boundary_from_record(record), boundary)
        json.dumps(record)

    def test_all_smt_obligations_probes_and_mutations_replay(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        cases = [
            *(
                (smt.obligation_text(purpose), "unsat\n")
                for purpose in smt.PURPOSES
            ),
            (smt.nonvacuity_text(), "sat\n"),
            *((smt.probe_text(kind), "sat\n") for kind in smt.PROBE_KINDS),
            *(
                (smt.mutation_text(kind), "sat\n")
                for kind in smt.MUTATION_KINDS
            ),
            *(
                (smt.correspondence_mutation_text(kind), "sat\n")
                for kind in smt.CORRESPONDENCE_MUTATION_KINDS
            ),
        ]
        for index, (text, expected) in enumerate(cases):
            with self.subTest(index=index):
                process = subprocess.run(
                    [str(z3), "-in", "-smt2"],
                    input=text,
                    text=True,
                    capture_output=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, expected)
                self.assertEqual(process.stderr, "")

    def test_smt_independent_definitions_do_not_delegate_to_source(
        self,
    ) -> None:
        text = smt.adapter_source_correspondence_text()
        smt.validate_obligation(
            text, smt.obligation_metadata(smt.ADAPTER_SOURCE)
        )
        adapter_start = text.index(
            "(define-fun IndependentCleanupLeftAfterRightKeyPanic"
        )
        adapter_end = text.index(
            "(define-fun SourcePublicFinish082", adapter_start
        )
        independent_adapter = text[adapter_start:adapter_end]
        self.assertNotIn("(SourceKeyAdapter", independent_adapter)
        self.assertNotIn("(KCleanupTwo", independent_adapter)
        finish_start = text.index(
            "(define-fun IndependentPublicFinish082"
        )
        finish_end = text.index(
            "(declare-const boundary KBoundary)", finish_start
        )
        independent_finish = text[finish_start:finish_end]
        self.assertNotIn("(SourcePublicFinish082", independent_finish)
        self.assertIn("(KObserveFDrop", independent_finish)


if __name__ == "__main__":
    unittest.main()
