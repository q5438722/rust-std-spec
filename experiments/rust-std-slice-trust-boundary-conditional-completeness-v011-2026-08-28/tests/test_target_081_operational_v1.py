#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import target_081_operational_smt_v1 as smt
import target_081_operational_v1 as model
import target_081_operational_witness_v1 as witnesses
import target_081_source_interpreter_v1 as reference


class Target081OperationalV1Tests(unittest.TestCase):
    def test_model_is_source_complete_and_replaces_opaque_sites(self) -> None:
        self.assertTrue(model.SOURCE_MODEL_COMPLETE)
        self.assertTrue(model.CLASSIFICATION_ELIGIBLE)
        self.assertEqual(model.MISSING_SOURCE_PHASES, ())
        self.assertEqual(model.PENDING_REPLACEMENT_TRUST_SITE_IDS, ())
        self.assertEqual(
            model.REPLACED_TRUST_SITE_IDS,
            ("TS-081-D002", "TS-081-D003", "TS-081-E001"),
        )
        self.assertEqual(model.ADMITTED_TRUST_SITE_IDS, ("TS-081-D004",))

    def test_adapter_evaluates_once_and_projects_exact_ordering(self) -> None:
        boundaries = (
            model.integer_total_order_boundary(),
            model.rank_total_order_boundary({1: 0, 2: 0}),
            model.explicit_ordering_boundary(
                {(1, 2): model.LESS, (2, 1): model.LESS}
            ),
        )
        for boundary in boundaries:
            with self.subTest(mode=boundary.ordering_mode):
                adapter = model.OrderingToLessAdapter(boundary)
                observed = boundary.observe(0, 1, 2)
                lowered = adapter.observe(0, 1, 2)
                event = adapter.events[0]
                self.assertEqual(len(adapter.events), 1)
                self.assertEqual(event.callback_evaluations, 1)
                self.assertEqual(event.ordering, observed.ordering)
                self.assertEqual(
                    event.is_less, observed.ordering == model.LESS
                )
                self.assertEqual(lowered.is_less, event.is_less)
                self.assertEqual(lowered.next_state, observed.next_state)
                self.assertEqual(lowered.panicked, observed.panicked)
                self.assertEqual(
                    event.observable_element_state_after,
                    observed.next_observable_element_state,
                )

    def test_callback_panic_precedes_less_test(self) -> None:
        boundary = model.integer_total_order_boundary(
            initial_observable_element_state=(4, 9),
            interior_next_state_mode=model.INCREMENT_STATE,
            panic_states=frozenset({0}),
            drop_interior_next_state_mode=model.AFFINE_STATE,
            drop_interior_affine_multiplier=2,
            drop_interior_affine_offset=1,
        )
        primary = model.execute(model.SortInput((3, 2, 1)), boundary)
        independent = reference.execute(
            (3, 2, 1), model.SourceConfiguration(), boundary
        )
        self.assertEqual(primary.adapter_events, independent.adapter_events)
        self.assertEqual(primary.state, independent.state)
        for run in (primary, independent):
            with self.subTest(adapter=type(run).__name__):
                self.assertEqual(run.terminal_status, model.PANIC)
                self.assertEqual(len(run.adapter_events), 1)
                event = run.adapter_events[0]
                self.assertEqual(event.ordering, model.LESS)
                self.assertEqual(event.callback_evaluations, 1)
                self.assertTrue(event.panicked)
                self.assertFalse(event.less_tested)
                self.assertFalse(event.is_less)
                self.assertEqual(
                    event.observable_element_state_before,
                    (4, 9),
                )
                self.assertEqual(
                    event.observable_element_state_after,
                    (5, 10),
                )
                self.assertEqual(
                    run.state.observable_element_state,
                    (11, 21),
                )
                self.assertTrue(run.state.callback_drop_invoked)
                self.assertTrue(run.state.callback_drop_completed)

    def test_normal_drop_panic_and_double_panic_are_distinct(self) -> None:
        normal_drop_panic = model.execute(
            model.SortInput(()),
            model.integer_total_order_boundary(
                initial_state=4,
                drop_panic_normal_states=frozenset({4}),
            ),
        )
        self.assertEqual(normal_drop_panic.terminal_status, model.PANIC)
        self.assertFalse(normal_drop_panic.state.aborted)
        self.assertEqual(
            normal_drop_panic.panic_phase,
            "callback-drop-after-normal-sort",
        )

        double_panic = model.execute(
            model.SortInput((2, 1, 0)),
            model.integer_total_order_boundary(
                panic_states=frozenset({0}),
                drop_panic_unwind_states=frozenset({1}),
            ),
        )
        self.assertEqual(double_panic.terminal_status, model.ABORT)
        self.assertTrue(double_panic.state.aborted)
        self.assertFalse(double_panic.state.panicked)
        self.assertEqual(
            double_panic.abort_phase, "callback-drop-during-unwind"
        )

    def test_callback_and_drop_state_are_observable(self) -> None:
        boundary = model.integer_total_order_boundary(
            initial_state=2,
            initial_observable_element_state=(1, 2),
            next_state_mode=model.AFFINE_STATE,
            affine_multiplier=2,
            affine_offset=1,
            interior_next_state_mode=model.AFFINE_STATE,
            interior_affine_multiplier=2,
            interior_affine_offset=1,
            drop_next_state_mode=model.AFFINE_STATE,
            drop_affine_multiplier=3,
            drop_affine_offset=2,
            drop_interior_next_state_mode=model.AFFINE_STATE,
            drop_interior_affine_multiplier=3,
            drop_interior_affine_offset=2,
        )
        run = model.execute(model.SortInput((1, 0)), boundary)
        self.assertEqual(run.adapter_events[0].next_state, 5)
        self.assertEqual(run.state.callback_state, 17)
        self.assertEqual(
            run.state.observable_element_state,
            (11, 17),
        )
        self.assertTrue(run.state.callback_drop_completed)

    def test_interior_state_can_drive_later_callback_results(self) -> None:
        boundary = model.interior_state_dependent_boundary(
            {0: 0, 1: 1, 2: 2},
            initial_observable_element_state=(0,),
            interior_next_state_mode=model.INCREMENT_STATE,
        )
        primary = model.execute(model.SortInput((2, 1, 0)), boundary)
        secondary = reference.execute(
            (2, 1, 0), model.SourceConfiguration(), boundary
        )
        self.assertEqual(primary.state, secondary.state)
        self.assertEqual(
            tuple(
                event.observable_element_state_before
                for event in primary.adapter_events
            ),
            tuple(
                event.observable_element_state_before
                for event in secondary.adapter_events
            ),
        )
        self.assertGreater(len(primary.adapter_events), 1)
        self.assertEqual(
            primary.adapter_events[0].observable_element_state_before,
            (0,),
        )
        self.assertEqual(
            primary.adapter_events[1].observable_element_state_before,
            (1,),
        )

    def test_non_total_comparator_is_operationally_deterministic(self) -> None:
        boundary = model.explicit_ordering_boundary(
            {
                (0, 0): model.EQUAL,
                (1, 1): model.EQUAL,
                (2, 2): model.EQUAL,
                (0, 1): model.LESS,
                (1, 2): model.LESS,
                (2, 0): model.LESS,
                (1, 0): model.GREATER,
                (2, 1): model.GREATER,
                (0, 2): model.GREATER,
            }
        )
        primary = model.execute(model.SortInput((2, 1, 0)), boundary)
        secondary = reference.execute(
            (2, 1, 0), model.SourceConfiguration(), boundary
        )
        self.assertEqual(primary.state, secondary.state)
        self.assertEqual(
            primary.comparator_observation,
            secondary.comparator_observation,
        )

    def test_all_witnesses_replay_field_for_field(self) -> None:
        payload = witnesses.witness_payload()
        self.assertGreaterEqual(payload["case_count"], 31)
        names = set(payload["cases"])
        for required in (
            "duplicate-equal-key-total-order",
            "documented-non-total-cycle",
            "callback-state-affine",
            "observable-interior-mutation-normal",
            "observable-interior-mutation-before-panic",
            "normal-callback-drop-panic",
            "comparator-panic-drop-double-panic-abort",
            "inherited-configuration-heapsort-size",
            "inherited-general-small-sort-merge-restoration",
        ):
            self.assertIn(required, names)
        for name, case in payload["cases"].items():
            with self.subTest(name=name):
                self.assertEqual(case["primary"], case["independent"])
                self.assertTrue(case["correspondence"]["field_complete"])
                self.assertTrue(
                    case["correspondence"][
                        "adapter_evaluations_are_single"
                    ]
                )
                self.assertTrue(
                    case["correspondence"][
                        "observable_interior_state_equal"
                    ]
                )
                self.assertEqual(
                    Counter(case["spec"]["sequence"]),
                    Counter(case["primary"]["sequence"]),
                )

    def test_boundary_has_no_answer_or_trace_fields(self) -> None:
        fields = set(model.ComparatorBoundary.__dataclass_fields__)
        for forbidden in (
            "schedule",
            "comparison_trace",
            "pivot",
            "swap",
            "output",
            "permutation",
            "final_state",
            "terminal_result",
        ):
            self.assertNotIn(forbidden, fields)
        manifest = model.boundary_manifest()
        self.assertTrue(manifest["boundary_narrower_than_target"])
        self.assertEqual(
            manifest["admitted_trust_site_ids"], ["TS-081-D004"]
        )
        self.assertIn(
            "complete element interior-mutation state",
            manifest["externally_observable_state"],
        )

    def test_small_smt_obligations_and_probes_replay(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        obligations = (
            (smt.adapter_source_correspondence_text(), "unsat\n"),
            (smt.nonvacuity_text(), "sat\n"),
            *((
                smt.probe_text(kind),
                "sat\n",
            ) for kind in smt.PROBE_KINDS),
            *((
                smt.mutation_text(kind),
                "sat\n",
            ) for kind in smt.MUTATION_KINDS),
        )
        for text, expected in obligations:
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


class Target081WitnessSerializationTests(unittest.TestCase):
    def test_boundary_round_trip_is_exact(self) -> None:
        boundary = model.explicit_ordering_boundary(
            {(1, 2): model.LESS, (2, 1): model.LESS},
            initial_state=-3,
            initial_observable_element_state=(7, 11),
            next_state_mode=model.AFFINE_STATE,
            affine_multiplier=-2,
            affine_offset=5,
            interior_next_state_mode=model.AFFINE_STATE,
            interior_affine_multiplier=3,
            interior_affine_offset=-4,
            panic_keys=frozenset({model.ObservationKey(-3, 1, 2)}),
            drop_next_state_mode=model.INCREMENT_STATE,
            drop_interior_next_state_mode=model.INCREMENT_STATE,
            drop_panic_unwind_states=frozenset({11}),
        )
        record = witnesses.boundary_record(boundary)
        self.assertEqual(witnesses.boundary_from_record(record), boundary)
        json.dumps(record)


if __name__ == "__main__":
    unittest.main()
