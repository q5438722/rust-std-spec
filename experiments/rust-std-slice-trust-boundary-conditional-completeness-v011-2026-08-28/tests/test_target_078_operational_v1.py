#!/usr/bin/env python3
from __future__ import annotations

import json
import random
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import target_078_operational_v1 as model


def selection_input(
    sequence: tuple[int, ...] | list[int] | range,
    index: int,
    *,
    is_zst: bool = False,
    optimize_for_size: bool = False,
    element_size: int = 8,
) -> model.SelectionInput:
    if is_zst:
        element_size = 0
    return model.SelectionInput(
        initial_sequence=tuple(sequence),
        index=index,
        allocation=41,
        borrow=51,
        is_zst=is_zst,
        configuration=model.SourceConfiguration(
            optimize_for_size=optimize_for_size,
            element_size=element_size,
        ),
    )


def events_of(
    execution: model.Execution, kind: str
) -> list[model.DerivedEvent]:
    return [
        event
        for event in execution.derived_events
        if event.kind == kind
    ]


def first_callback_state_after(
    execution: model.Execution,
    *,
    prior_kind: str,
    phase_prefix: str,
) -> int:
    reached_prior = False
    for event in execution.derived_events:
        if event.kind == prior_kind:
            reached_prior = True
        elif (
            reached_prior
            and event.kind == "callback"
            and event.phase.startswith(phase_prefix)
        ):
            return int(event.detail("state"))
    raise AssertionError(
        f"no {phase_prefix!r} callback followed {prior_kind!r}"
    )


class Target078OperationalV1Tests(unittest.TestCase):
    def test_source_binding_manifest_closes_every_used_excerpt(self) -> None:
        manifest_path = (
            ROOT
            / "evidence/target_078_operational_v1/source_bindings.json"
        )
        manifest = json.loads(manifest_path.read_text())
        self.assertEqual(manifest["model_id"], model.MODEL_ID)
        self.assertEqual(manifest["model_version"], model.MODEL_VERSION)
        self.assertTrue(manifest["source_model_complete"])
        self.assertTrue(manifest["classification_eligible"])
        self.assertEqual(manifest["missing_source_phases"], [])
        self.assertEqual(
            set(manifest["configuration_coverage"]),
            {
                "optimize_for_size=true",
                "optimize_for_size=false",
                "size_of_T<=16",
                "16<size_of_T<=96",
                "size_of_T>96",
            },
        )
        self.assertEqual(
            len(manifest["active_contract"]["conjuncts"]),
            len(model.ACTIVE_CONJUNCTS),
        )
        roles = {binding["role"] for binding in manifest["covered_source"]}
        self.assertEqual(
            roles,
            {
                "public-target-adapter",
                "selection-and-fallback",
                "pivot-selection",
                "frozen-partition-entry",
                "partition-and-unwind",
                "small-sort-and-unwind",
                "cfg-select-semantics",
                "zst-type-property",
                "callback-contract-vocabulary",
            },
        )
        for binding in manifest["covered_source"]:
            path = ROOT / binding["path"]
            self.assertTrue(path.is_file(), path)
            source = path.read_text()
            for anchor in binding["semantic_anchors"]:
                self.assertIn(anchor, source)

    def test_boundary_is_immutable_complete_and_answer_free(self) -> None:
        self.assertEqual(model.TARGET, "core::slice::select_nth_unstable_by")
        self.assertEqual(model.INPUT_ORDER, "78")
        self.assertTrue(model.SOURCE_MODEL_COMPLETE)
        self.assertEqual(model.MISSING_SOURCE_PHASES, ())
        manifest = model.boundary_manifest()
        self.assertTrue(manifest["source_model_complete"])
        self.assertTrue(manifest["classification_eligible"])
        self.assertEqual(
            set(manifest["admitted_trust_site_ids"]), {"TS-078-D004"}
        )
        self.assertEqual(
            set(manifest["adapter_replaced_trust_site_ids"]),
            {"TS-078-D002"},
        )
        self.assertEqual(
            set(manifest["algorithm_replaced_trust_site_ids"]),
            {"TS-078-D003", "TS-078-E001"},
        )
        self.assertEqual(manifest["unresolved_trust_site_ids"], [])
        observed = json.dumps(
            manifest["shared_boundary_observations"]
        ).lower()
        for forbidden in (
            "realized",
            "count",
            "pivot",
            "permutation",
            "returned",
            "final slice",
            "final callback",
            "trace",
        ):
            self.assertNotIn(forbidden, observed)

    def test_prior_falsifier_uses_total_trace_independent_relation(
        self,
    ) -> None:
        boundary = model.state_prefix_order_boundary(
            ordering_cutoff=3,
        )
        item = selection_input((3, 2, 1), 1)
        first = model.execute(item, boundary)
        second = model.execute(item, boundary)
        self.assertEqual(first.final_state.sequence, (1, 2, 3))
        self.assertTrue(model.exact_equivalent(first, second))
        self.assertEqual(
            boundary.observe(10_000, -50, 700),
            model.ComparatorObservation(
                ordering=model.GREATER,
                next_state=10_001,
                panicked=False,
            ),
        )
        self.assertFalse(
            any(callable(value) for value in vars(boundary).values())
        )
        self.assertFalse(hasattr(model.ComparatorBoundary, "freeze"))

    def test_invalid_or_inadmissible_relations_fail_closed(self) -> None:
        with self.assertRaises(TypeError):
            model.ComparatorBoundary(
                callback_identity=1,
                initial_state=0,
                ordering_mode=model.INTEGER_TOTAL_ORDER,
                next_state_mode=model.INCREMENT_STATE,
                contract_ordering_mode=model.INTEGER_TOTAL_ORDER,
                panic_states=set(),  # type: ignore[arg-type]
            )
        with self.assertRaises(model.BoundaryViolation):
            model.constant_order_boundary(model.LESS).contract_ordering(1, 2)
        with self.assertRaises(model.BoundaryViolation):
            model.ComparatorBoundary(
                callback_identity=1,
                initial_state=0,
                ordering_mode=model.STATE_PREFIX_LESS_THEN_GREATER,
                next_state_mode=model.INCREMENT_STATE,
                contract_ordering_mode=model.INTEGER_TOTAL_ORDER,
                ordering_cutoff=3,
            )

    def test_contract_ordering_is_state_independent_and_axiomatized(
        self,
    ) -> None:
        boundary = model.integer_total_order_boundary(initial_state=27)
        values = (-3, 0, 4)
        for left in values:
            self.assertEqual(
                boundary.contract_ordering(left, left), model.EQUAL
            )
            for right in values:
                observed = boundary.contract_ordering(left, right)
                reverse = boundary.contract_ordering(right, left)
                self.assertEqual(observed, -reverse)
                self.assertTrue(
                    observed <= model.EQUAL or reverse <= model.EQUAL
                )
                self.assertEqual(
                    observed,
                    boundary.contract_ordering(left, right),
                )
                for third in values:
                    if (
                        observed <= model.EQUAL
                        and boundary.contract_ordering(right, third)
                        <= model.EQUAL
                    ):
                        self.assertLessEqual(
                            boundary.contract_ordering(left, third),
                            model.EQUAL,
                        )

    def test_zst_and_bounds_paths_make_no_callback_observation(self) -> None:
        boundary = model.integer_total_order_boundary(initial_state=7)
        zst = model.execute(
            selection_input(tuple(range(257)), 128, is_zst=True),
            boundary,
        )
        self.assertEqual(zst.coverage_status, model.MODELED_NORMAL)
        self.assertEqual(zst.branch, "zst")
        self.assertEqual(zst.final_state.sequence, tuple(range(257)))
        self.assertEqual(zst.final_state.callback_state, 7)
        self.assertEqual(events_of(zst, "callback"), [])

        for index in (-1, 0, 1):
            with self.subTest(empty_index=index):
                bounded = model.execute(
                    selection_input((), index),
                    boundary,
                )
                self.assertEqual(
                    bounded.coverage_status, model.MODELED_PANIC
                )
                self.assertEqual(bounded.branch, "bounds-panic")
                self.assertEqual(bounded.final_state.callback_state, 7)
                self.assertEqual(bounded.panic_phase, "bounds")

    def test_arbitrary_length_min_and_max_scans_follow_source_order(self) -> None:
        sequence = tuple(range(96, 0, -1))
        boundary = model.integer_total_order_boundary()
        minimum_input = selection_input(sequence, 0)
        maximum_input = selection_input(sequence, len(sequence) - 1)
        minimum = model.execute(minimum_input, boundary)
        maximum = model.execute(maximum_input, boundary)
        for item, execution, branch, pivot in (
            (minimum_input, minimum, "min-scan", 1),
            (maximum_input, maximum, "max-scan", 96),
        ):
            with self.subTest(branch=branch):
                self.assertEqual(execution.coverage_status, model.MODELED_NORMAL)
                self.assertEqual(execution.branch, branch)
                self.assertIsNotNone(execution.output)
                self.assertEqual(execution.output.pivot_identity, pivot)
                self.assertEqual(
                    execution.final_state.callback_state,
                    len(sequence) - 1,
                )
                self.assertTrue(
                    model.active_contract_holds(item, boundary, execution)
                )
        self.assertEqual(
            [
                (event.detail("left_identity"), event.detail("right_identity"))
                for event in events_of(minimum, "callback")[:3]
            ],
            [(95, 96), (94, 95), (93, 94)],
        )
        self.assertEqual(
            [
                (event.detail("left_identity"), event.detail("right_identity"))
                for event in events_of(maximum, "callback")[:3]
            ],
            [(96, 95), (96, 94), (96, 93)],
        )

    def test_every_small_sort_length_and_index_is_source_reachable(self) -> None:
        boundary = model.integer_total_order_boundary()
        for length in range(3, model.INSERTION_SORT_THRESHOLD + 1):
            initial = tuple(range(length, 0, -1))
            for index in range(1, length - 1):
                with self.subTest(length=length, index=index):
                    item = selection_input(initial, index)
                    execution = model.execute(item, boundary)
                    self.assertEqual(
                        execution.coverage_status, model.MODELED_NORMAL
                    )
                    self.assertEqual(execution.branch, "insertion-sort")
                    self.assertEqual(
                        execution.final_state.sequence,
                        tuple(range(1, length + 1)),
                    )
                    self.assertEqual(
                        execution.final_state.callback_state,
                        length * (length - 1) // 2,
                    )
                    self.assertEqual(
                        {
                            event.detail("relative_tail")
                            for event in events_of(
                                execution, "insertion-tail"
                            )
                        },
                        set(range(1, length)),
                    )
                    conjuncts = model.active_contract_conjuncts(
                        item, boundary, execution
                    )
                    self.assertEqual(
                        set(conjuncts), set(model.ACTIVE_CONJUNCTS)
                    )
                    self.assertTrue(all(conjuncts.values()))

    def test_small_sort_no_shift_partial_shift_and_unwind(self) -> None:
        boundary = model.integer_total_order_boundary()
        ascending = model.execute(
            selection_input((10, 20, 30, 40), 1), boundary
        )
        self.assertEqual(ascending.final_state.callback_state, 3)
        self.assertEqual(
            len(events_of(ascending, "insert-tail-no-shift")), 3
        )

        partial = model.execute(
            selection_input((10, 30, 20, 40), 1), boundary
        )
        self.assertEqual(partial.final_state.sequence, (10, 20, 30, 40))
        self.assertEqual(partial.final_state.callback_state, 4)
        self.assertTrue(events_of(partial, "insert-tail-shift"))
        self.assertTrue(
            any(
                not event.detail("panicked")
                for event in events_of(partial, "copy-on-drop-restore")
            )
        )

        panic = model.execute(
            selection_input((10, 30, 20, 40), 1),
            model.integer_total_order_boundary(
                panic_states=frozenset({2})
            ),
        )
        self.assertEqual(panic.coverage_status, model.MODELED_PANIC)
        self.assertEqual(panic.final_state.sequence, (10, 20, 30, 40))
        self.assertEqual(panic.final_state.callback_state, 3)
        self.assertEqual(
            Counter(panic.final_state.sequence),
            Counter((10, 30, 20, 40)),
        )
        self.assertTrue(
            events_of(panic, "copy-on-drop-restore")[-1].detail(
                "panicked"
            )
        )

    def test_choose_pivot_recursion_is_executed(self) -> None:
        sequence = list(range(65))
        random.Random(6501).shuffle(sequence)
        item = selection_input(sequence, 32)
        execution = model.execute(
            item, model.integer_total_order_boundary()
        )
        self.assertEqual(execution.coverage_status, model.MODELED_NORMAL)
        choices = events_of(execution, "choose-pivot")
        self.assertTrue(choices)
        self.assertEqual(choices[0].detail("branch"), "median3-rec")
        self.assertTrue(events_of(execution, "median3-rec-enter"))
        self.assertTrue(
            model.active_contract_holds(
                item, model.integer_total_order_boundary(), execution
            )
        )

    def test_all_partition_implementations_have_source_exact_mutations(
        self,
    ) -> None:
        fixtures = (
            (
                False,
                8,
                "lomuto-cyclic",
                2,
                (1, 2, 0, 3, 4, 5),
                [(5, 3), (2, 3), (4, 3), (0, 3), (1, 3)],
            ),
            (
                False,
                32,
                "lomuto-cyclic",
                1,
                (1, 2, 0, 3, 4, 5),
                [(5, 3), (2, 3), (4, 3), (0, 3), (1, 3)],
            ),
            (
                False,
                128,
                "hoare-cyclic",
                None,
                (2, 1, 0, 3, 4, 5),
                [(1, 3), (5, 3), (0, 3), (2, 3), (4, 3)],
            ),
            (
                True,
                8,
                "lomuto-simple",
                None,
                (0, 1, 2, 3, 5, 4),
                [(1, 3), (5, 3), (2, 3), (4, 3), (0, 3)],
            ),
            (
                True,
                128,
                "hoare-cyclic",
                None,
                (2, 1, 0, 3, 4, 5),
                [(1, 3), (5, 3), (0, 3), (2, 3), (4, 3)],
            ),
        )
        for (
            optimize,
            size,
            implementation,
            unroll,
            expected,
            expected_calls,
        ) in fixtures:
            with self.subTest(optimize=optimize, size=size):
                item = selection_input(
                    (5, 1, 3, 2, 4, 0),
                    2,
                    optimize_for_size=optimize,
                    element_size=size,
                )
                engine = model._Engine(
                    item, model.integer_total_order_boundary()
                )
                mid = model._partition(engine, 0, 6, 2)
                self.assertEqual(mid, 3)
                self.assertEqual(tuple(engine.sequence), expected)
                implementation_event = events_of(
                    model.Execution(
                        model.MODELED_NORMAL,
                        "probe",
                        None,
                        engine.final_state(panicked=False),
                        tuple(engine.events),
                    ),
                    "partition-implementation",
                )[0]
                self.assertEqual(
                    implementation_event.detail("implementation"),
                    implementation,
                )
                if unroll is not None:
                    self.assertEqual(
                        implementation_event.detail("unroll_len"), unroll
                    )
                self.assertEqual(
                    [
                        (
                            event.detail("left_identity"),
                            event.detail("right_identity"),
                        )
                        for event in engine.events
                        if event.kind == "callback"
                    ],
                    expected_calls,
                )

    def test_both_introselect_narrowing_directions_are_forced(self) -> None:
        sequence = list(range(33))
        random.Random(49).shuffle(sequence)
        item = selection_input(sequence, 16)
        execution = model.execute(
            item, model.integer_total_order_boundary()
        )
        kinds = {event.kind for event in execution.derived_events}
        self.assertIn("introselect-narrow-left", kinds)
        self.assertIn("introselect-narrow-right", kinds)
        for event in events_of(execution, "introselect-window"):
            self.assertEqual(
                event.detail("window_start") + event.detail("index"), 16
            )
        self.assertTrue(
            model.active_contract_holds(
                item, model.integer_total_order_boundary(), execution
            )
        )

    def test_length_17_cyclic_partition_correspondence_fixture(
        self,
    ) -> None:
        item = selection_input(tuple(range(16, -1, -1)), 8)
        execution = model.execute(
            item, model.integer_total_order_boundary()
        )
        self.assertEqual(
            execution.final_state.sequence,
            (0, 7, 6, 5, 4, 3, 2, 1, 8, 15, 13, 12, 11, 10, 9, 16, 14),
        )
        self.assertEqual(execution.final_state.callback_state, 19)
        self.assertFalse(execution.final_state.panicked)
        self.assertTrue(execution.final_state.terminal)
        self.assertEqual(execution.output.pivot_identity, 8)
        self.assertTrue(
            model.active_contract_holds(
                item, model.integer_total_order_boundary(), execution
            )
        )

    def test_ancestor_pivot_reverse_partition_is_forced(self) -> None:
        item = selection_input((7,) * 40, 20)
        boundary = model.integer_total_order_boundary()
        execution = model.execute(item, boundary)
        self.assertEqual(execution.coverage_status, model.MODELED_NORMAL)
        ancestors = events_of(execution, "ancestor-pivot-partition")
        self.assertTrue(ancestors)
        self.assertTrue(
            any(
                event.detail("reverse")
                for event in events_of(execution, "partition-result")
            )
        )
        terminal = events_of(execution, "introselect-return")[-1]
        self.assertEqual(
            terminal.detail("terminal"), "ancestor-pivot-return"
        )
        self.assertTrue(model.active_contract_holds(item, boundary, execution))

    def test_sixteen_step_fallback_and_all_ninther_branches_are_forced(
        self,
    ) -> None:
        item = selection_input(range(50), 1)
        execution = model.execute(
            item, model.constant_order_boundary(model.LESS)
        )
        self.assertEqual(execution.coverage_status, model.MODELED_NORMAL)
        self.assertEqual(len(events_of(execution, "choose-pivot")), 16)
        self.assertTrue(events_of(execution, "median-of-ninthers"))
        self.assertEqual(
            events_of(execution, "introselect-return")[-1].detail(
                "terminal"
            ),
            "introselect-fallback",
        )
        self.assertEqual(
            Counter(execution.final_state.sequence),
            Counter(item.initial_sequence),
        )

        branches: set[str] = set()
        for seed in (0, 1, 4, 7, 10):
            sequence = list(range(17))
            random.Random(seed).shuffle(sequence)
            candidate = model.execute(
                selection_input(
                    sequence, 8, optimize_for_size=True
                ),
                model.integer_total_order_boundary(),
            )
            branches.update(
                str(event.detail("branch"))
                for event in events_of(candidate, "ninther")
            )
        self.assertEqual(
            branches,
            {
                "e-less-d",
                "f-less-e",
                "swap-e-b",
                "swap-e-h",
                "already-median",
            },
        )

    def test_every_ninther_fraction_configuration_is_bound(self) -> None:
        self.assertEqual(
            model.median_of_ninthers_geometry(17)[-1], "len/12"
        )
        self.assertEqual(
            model.median_of_ninthers_geometry(1025)[-1], "len/64"
        )
        self.assertEqual(
            model.median_of_ninthers_geometry(128 * 1024 + 1)[-1],
            "len/1024",
        )
        for length in (17, 1024, 1025, 128 * 1024, 128 * 1024 + 1):
            frac, pivot, lo, gap, _branch = (
                model.median_of_ninthers_geometry(length)
            )
            self.assertGreater(frac, 0)
            self.assertGreaterEqual(pivot, 0)
            self.assertGreaterEqual(lo - 4 * frac - gap, 0)
            self.assertLess(lo + frac + gap + 3 * frac, length)

    def test_callback_panic_prefixes_preserve_permutation(self) -> None:
        fixtures = (
            (
                selection_input(
                    random.Random(17).sample(range(40), 40), 20
                ),
                "median3",
                "choose-pivot",
                False,
            ),
            (
                selection_input(
                    random.Random(908).sample(range(40), 40),
                    20,
                    element_size=8,
                ),
                "partition-cycle",
                "partition-lomuto-cyclic",
                True,
            ),
            (
                selection_input(
                    random.Random(1028).sample(range(40), 40),
                    20,
                    element_size=128,
                ),
                "partition-cycle",
                "partition-hoare",
                True,
            ),
            (
                selection_input(
                    random.Random(19).sample(range(40), 40),
                    20,
                    optimize_for_size=True,
                    element_size=8,
                ),
                "swap",
                "partition-lomuto-simple",
                False,
            ),
        )
        for item, prior_kind, prefix, expects_guard in fixtures:
            with self.subTest(prefix=prefix):
                normal = model.execute(
                    item, model.integer_total_order_boundary()
                )
                state = first_callback_state_after(
                    normal,
                    prior_kind=prior_kind,
                    phase_prefix=prefix,
                )
                panic = model.execute(
                    item,
                    model.integer_total_order_boundary(
                        panic_states=frozenset({state})
                    ),
                )
                self.assertEqual(
                    panic.coverage_status, model.MODELED_PANIC
                )
                self.assertTrue(panic.panic_phase.startswith(prefix))
                self.assertEqual(
                    Counter(panic.final_state.sequence),
                    Counter(item.initial_sequence),
                )
                self.assertIsNone(panic.output)
                self.assertEqual(
                    bool(events_of(panic, "gap-guard-restore")),
                    expects_guard,
                )

    def test_ancestor_and_ninther_callback_panic_prefixes_are_reached(
        self,
    ) -> None:
        fixtures = (
            (selection_input((7,) * 40, 20), "ancestor-pivot"),
            (
                selection_input(
                    random.Random(0).sample(range(17), 17),
                    8,
                    optimize_for_size=True,
                ),
                "ninther",
            ),
        )
        for item, prefix in fixtures:
            with self.subTest(prefix=prefix):
                normal = model.execute(
                    item, model.integer_total_order_boundary()
                )
                event = next(
                    event
                    for event in events_of(normal, "callback")
                    if event.phase.startswith(prefix)
                )
                panic = model.execute(
                    item,
                    model.integer_total_order_boundary(
                        panic_states=frozenset(
                            {int(event.detail("state"))}
                        )
                    ),
                )
                self.assertEqual(
                    panic.coverage_status, model.MODELED_PANIC
                )
                self.assertTrue(panic.panic_phase.startswith(prefix))
                self.assertEqual(
                    Counter(panic.final_state.sequence),
                    Counter(item.initial_sequence),
                )

    def test_arbitrary_lengths_and_configurations_satisfy_contract(self) -> None:
        boundary = model.integer_total_order_boundary()
        configurations = (
            (False, 8),
            (False, 32),
            (False, 128),
            (True, 8),
            (True, 128),
        )
        for length in (1, 2, 3, 16, 17, 33, 64, 65, 97):
            sequence = list(range(length))
            random.Random(length * 101).shuffle(sequence)
            for index in sorted({0, length // 2, length - 1}):
                for optimize, size in configurations:
                    with self.subTest(
                        length=length,
                        index=index,
                        optimize=optimize,
                        size=size,
                    ):
                        item = selection_input(
                            sequence,
                            index,
                            optimize_for_size=optimize,
                            element_size=size,
                        )
                        execution = model.execute(item, boundary)
                        self.assertEqual(
                            execution.coverage_status,
                            model.MODELED_NORMAL,
                        )
                        self.assertTrue(
                            model.active_contract_holds(
                                item, boundary, execution
                            )
                        )
                        self.assertEqual(
                            execution.output.left.span, index
                        )
                        self.assertEqual(
                            execution.output.right.span,
                            length - index - 1,
                        )

    def test_same_input_and_boundary_are_exactly_deterministic(self) -> None:
        sequence = list(range(97))
        random.Random(7801).shuffle(sequence)
        item = selection_input(sequence, 48, element_size=128)
        boundary = model.integer_total_order_boundary(initial_state=11)
        first = model.execute(item, boundary)
        second = model.execute(item, boundary)
        self.assertTrue(model.exact_equivalent(first, second))
        self.assertEqual(first.output, second.output)
        self.assertEqual(first.final_state, second.final_state)
        self.assertIsNone(first.model_gap_phase)


if __name__ == "__main__":
    unittest.main()
