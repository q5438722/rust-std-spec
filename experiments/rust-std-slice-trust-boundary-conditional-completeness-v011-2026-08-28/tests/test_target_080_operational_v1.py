#!/usr/bin/env python3
from __future__ import annotations

import random
import sys
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import target_078_operational_v1 as accepted_078
import target_080_operational_v1 as model
import target_080_operational_witness_v1 as witnesses
import target_080_source_interpreter_v1 as reference


def permutation(length: int, seed: int) -> tuple[int, ...]:
    values = list(range(length))
    random.Random(seed).shuffle(values)
    return tuple(values)


class Target080OperationalV1Tests(unittest.TestCase):
    def test_model_is_source_complete_and_replaces_excluded_sites(self) -> None:
        self.assertTrue(model.SOURCE_MODEL_COMPLETE)
        self.assertTrue(model.CLASSIFICATION_ELIGIBLE)
        self.assertEqual(model.MISSING_SOURCE_PHASES, ())
        self.assertEqual(model.PENDING_REPLACEMENT_TRUST_SITE_IDS, ())
        self.assertEqual(
            model.REPLACED_TRUST_SITE_IDS,
            ("TS-080-D002", "TS-080-E001"),
        )
        self.assertGreaterEqual(len(model.COVERED_SOURCE_PHASES), 14)

    def test_general_total_boundary_supports_duplicate_classes(self) -> None:
        boundary = model.rank_total_order_boundary(
            {10: 0, 11: 0, 20: 1, 21: 2},
            initial_state=3,
            next_state_mode=model.AFFINE_STATE,
            affine_multiplier=2,
            affine_offset=1,
            panic_keys=frozenset(
                {model.ObservationKey(7, 20, 21)}
            ),
        )
        self.assertTrue(boundary.contract_admissible())
        self.assertFalse(boundary.observe(3, 10, 11).is_less)
        self.assertFalse(boundary.observe(3, 11, 10).is_less)
        self.assertTrue(boundary.observe(3, 10, 20).is_less)
        self.assertEqual(boundary.observe(3, 10, 20).next_state, 7)
        self.assertTrue(boundary.observe(7, 20, 21).panicked)
        for state in (-100, 0, 100):
            for left in (-4, 10, 11, 20, 99):
                for right in (-4, 10, 11, 20, 99):
                    observation = boundary.observe(state, left, right)
                    self.assertIsInstance(observation.is_less, bool)
                    self.assertIsInstance(observation.next_state, int)
                    self.assertIsInstance(observation.panicked, bool)

    def test_state_indexed_fixture_is_total_but_not_classifying(self) -> None:
        boundary = model.symbolic_state_boundary({0: 0, 1: 1})
        self.assertFalse(boundary.contract_admissible())
        self.assertTrue(boundary.observe(0, 0, 1).is_less)
        self.assertTrue(boundary.observe(1, 1, 0).is_less)
        with self.assertRaises(model.BoundaryViolation):
            boundary.contract_is_less(0, 1)

    def test_boundary_contains_no_answer_or_trace_fields(self) -> None:
        fields = set(model.OrdBoundary.__dataclass_fields__)
        for forbidden in (
            "schedule",
            "pivot",
            "swap",
            "output",
            "final_sequence",
            "permutation",
            "aggregate_state",
            "trace",
        ):
            self.assertNotIn(forbidden, fields)
        manifest = model.boundary_manifest()
        self.assertEqual(
            manifest["admitted_trust_site_ids"], ["TS-080-D003"]
        )
        self.assertEqual(
            manifest["replaced_trust_site_ids"],
            ["TS-080-D002", "TS-080-E001"],
        )
        self.assertEqual(manifest["pending_replacement_trust_site_ids"], [])

    def test_zst_trivial_and_configuration_heapsort_dispatch(self) -> None:
        boundary = model.integer_total_order_boundary()
        zst = model.execute(
            model.SortInput(
                (3, 2, 1),
                model.SourceConfiguration(element_size=0),
            ),
            boundary,
        )
        self.assertEqual(zst.terminal_status, model.NORMAL)
        self.assertEqual(zst.state.sequence, (3, 2, 1))
        self.assertEqual(zst.state.callback_state, 0)
        for sequence in ((), (4,)):
            run = model.execute(model.SortInput(sequence), boundary)
            self.assertEqual(run.terminal_status, model.NORMAL)
            self.assertEqual(run.state.callback_state, 0)

        for configuration in (
            model.SourceConfiguration(optimize_for_size=True),
            model.SourceConfiguration(target_pointer_width=16),
        ):
            sequence = permutation(25, configuration.target_pointer_width)
            run = model.execute(
                model.SortInput(sequence, configuration), boundary
            )
            self.assertEqual(run.terminal_status, model.NORMAL)
            self.assertEqual(run.state.sequence, tuple(sorted(sequence)))
            self.assertTrue(
                any(
                    step.kind == "heapsort-enter"
                    and step.phase == "sort:configuration-heapsort"
                    for step in run.derived_steps
                )
            )

    def test_insertion_and_copy_on_drop_restoration(self) -> None:
        sequence = (4, 1, 3, 2)
        normal = model.execute(
            model.SortInput(sequence),
            model.integer_total_order_boundary(),
        )
        self.assertEqual(normal.state.sequence, (1, 2, 3, 4))
        for panic_state in (0, 2, 4):
            with self.subTest(panic_state=panic_state):
                run = model.execute(
                    model.SortInput(sequence),
                    model.integer_total_order_boundary(
                        panic_states=frozenset({panic_state})
                    ),
                )
                self.assertEqual(run.terminal_status, model.PANIC)
                self.assertEqual(
                    Counter(run.state.sequence), Counter(sequence)
                )
        sift_panic = model.execute(
            model.SortInput(sequence),
            model.integer_total_order_boundary(
                panic_states=frozenset({2})
            ),
        )
        restores = [
            step
            for step in sift_panic.derived_steps
            if step.kind == "copy-on-drop-restore"
        ]
        self.assertTrue(restores[-1].detail("panicked"))

    def test_existing_runs_and_reversal_are_source_ordered(self) -> None:
        boundary = model.integer_total_order_boundary()
        ascending = model.execute(
            model.SortInput(tuple(range(21))), boundary
        )
        descending = model.execute(
            model.SortInput(tuple(range(20, -1, -1))), boundary
        )
        self.assertEqual(ascending.state.callback_state, 20)
        self.assertEqual(descending.state.callback_state, 20)
        self.assertEqual(descending.state.sequence, tuple(range(21)))
        self.assertTrue(
            any(step.kind == "reverse" for step in descending.derived_steps)
        )

    def test_small_sort_specialization_thresholds(self) -> None:
        cases = (
            (model.SourceConfiguration(), 16, "fallback"),
            (
                model.SourceConfiguration(is_freeze=True),
                32,
                "general",
            ),
            (
                model.SourceConfiguration(is_freeze=True, is_copy=True),
                32,
                "network",
            ),
            (
                model.SourceConfiguration(
                    element_size=24,
                    is_freeze=True,
                    is_copy=True,
                    has_efficient_in_place_swap=False,
                ),
                32,
                "general",
            ),
            (
                model.SourceConfiguration(
                    element_size=256, is_freeze=True
                ),
                16,
                "fallback",
            ),
        )
        for configuration, threshold, kind in cases:
            with self.subTest(configuration=configuration):
                self.assertEqual(
                    model._small_sort_threshold(configuration), threshold
                )
                self.assertEqual(model._small_sort_kind(configuration), kind)

    def test_all_small_sort_implementations_execute(self) -> None:
        cases = (
            (
                model.SourceConfiguration(),
                permutation(45, 8101),
                "fallback",
            ),
            (
                model.SourceConfiguration(is_freeze=True, is_copy=True),
                permutation(26, 8102),
                "network",
            ),
            (
                model.SourceConfiguration(
                    element_size=24,
                    is_freeze=True,
                    is_copy=True,
                    has_efficient_in_place_swap=False,
                ),
                permutation(26, 8103),
                "general",
            ),
        )
        for configuration, sequence, expected_kind in cases:
            with self.subTest(expected_kind=expected_kind):
                run = model.execute(
                    model.SortInput(sequence, configuration),
                    model.integer_total_order_boundary(),
                )
                self.assertEqual(run.terminal_status, model.NORMAL)
                self.assertEqual(run.state.sequence, tuple(sorted(sequence)))
                implementations = {
                    step.detail("implementation")
                    for step in run.derived_steps
                    if step.kind == "small-sort-dispatch"
                }
                self.assertIn(expected_kind, implementations)

    def test_small_sort_and_partition_panics_restore_permutations(self) -> None:
        payload = witnesses.witness_payload()
        for name in (
            "general-small-sort-merge-restoration",
            "general-small-sort-scratch-unwind-restoration",
            "network-small-sort-merge-panic",
            "cyclic-gap-guard-restoration",
            "hoare-gap-guard-restoration",
        ):
            with self.subTest(name=name):
                case = payload["cases"][name]
                self.assertEqual(
                    case["expected"]["terminal_status"], model.PANIC
                )
                self.assertEqual(
                    Counter(case["expected"]["sequence"]),
                    Counter(case["spec"]["sequence"]),
                )
        self.assertIn(
            "gap-guard-restore",
            payload["cases"]["cyclic-gap-guard-restoration"][
                "source_step_kinds"
            ],
        )
        self.assertIn(
            "copy-on-drop-restore",
            payload["cases"]["general-small-sort-merge-restoration"][
                "source_step_kinds"
            ],
        )
        self.assertIn(
            "scratch-copy-on-drop-restore",
            payload["cases"][
                "general-small-sort-scratch-unwind-restoration"
            ]["source_step_kinds"],
        )

    def test_uncovered_small_sort_branches_have_retained_witnesses(
        self,
    ) -> None:
        payload = witnesses.witness_payload()
        cases = {
            "general-small-sort-sort8-direct": (
                "small-sort-general-presorted",
                "sort8",
                8,
            ),
            "network-small-sort-sort9-direct": (
                "small-sort-network-presorted",
                "sort9",
                9,
            ),
            "general-small-sort-presorted-one-direct": (
                "small-sort-general-presorted",
                "singleton",
                1,
            ),
        }
        for name, (kind, implementation, length) in cases.items():
            with self.subTest(name=name):
                _, _, steps, _ = witnesses.execute_spec(
                    payload["cases"][name]["spec"]
                )
                branch = next(step for step in steps if step.kind == kind)
                self.assertEqual(
                    branch.detail("implementation"), implementation
                )
                self.assertEqual(
                    branch.detail("presorted_length"), length
                )

    def test_empty_partition_helper_returns_zero(self) -> None:
        spec = witnesses._spec(
            "empty-partition",
            (),
            model.SourceConfiguration(),
            model.integer_total_order_boundary(),
            action="partition",
            parameters={"pivot": 0},
        )
        primary, secondary, _, correspondence = witnesses.execute_spec(spec)
        self.assertEqual(primary, secondary)
        self.assertEqual(primary["returned_index"], 0)
        self.assertEqual(primary["terminal_status"], model.NORMAL)
        self.assertEqual(correspondence["callback_count"], 0)

    def test_shared_pivot_and_partition_match_accepted_target_078(self) -> None:
        sequence = permutation(40, 8200)
        configuration = model.SourceConfiguration(element_size=32)
        actual_engine = model._Engine(
            model.SortInput(sequence, configuration),
            model.integer_total_order_boundary(),
        )
        expected_engine = accepted_078._Engine(
            accepted_078.SelectionInput(
                initial_sequence=sequence,
                index=0,
                allocation=1,
                borrow=1,
                is_zst=False,
                configuration=accepted_078.SourceConfiguration(
                    element_size=32
                ),
            ),
            accepted_078.integer_total_order_boundary(),
        )
        actual_pivot = model._choose_pivot(
            actual_engine, 0, len(sequence)
        )
        expected_pivot = accepted_078._choose_pivot(
            expected_engine, 0, len(sequence)
        )
        self.assertEqual(actual_pivot, expected_pivot)
        self.assertEqual(
            actual_engine.callback_state, expected_engine.callback_state
        )
        actual_mid = model._partition(
            actual_engine, 0, len(sequence), actual_pivot
        )
        expected_mid = accepted_078._partition(
            expected_engine, 0, len(sequence), expected_pivot
        )
        self.assertEqual(actual_mid, expected_mid)
        self.assertEqual(
            actual_engine.sequence, expected_engine.sequence
        )
        self.assertEqual(
            actual_engine.callback_state, expected_engine.callback_state
        )

    def test_every_partition_kernel_is_reachable_in_bound_evidence(self) -> None:
        payload = witnesses.witness_payload()
        expected = {
            "lomuto-simple-direct": "lomuto-simple",
            "cyclic-unroll-one-partition": "lomuto-cyclic",
            "hoare-partition": "hoare-cyclic",
        }
        for name, implementation in expected.items():
            with self.subTest(name=name):
                primary, _, steps, _ = witnesses.execute_spec(
                    payload["cases"][name]["spec"]
                )
                self.assertEqual(primary["terminal_status"], model.NORMAL)
                self.assertTrue(
                    any(
                        step.kind == "partition-implementation"
                        and step.detail("implementation") == implementation
                        for step in steps
                    )
                )

    def test_duplicate_ancestor_recursion_and_limit_fallback(self) -> None:
        payload = witnesses.witness_payload()
        ancestor = payload["cases"]["duplicate-class-ancestor-pivot"]
        self.assertIn(
            "ancestor-pivot-partition", ancestor["source_step_kinds"]
        )
        recursive = payload["cases"]["fallback-small-sort-and-recursion"]
        self.assertIn("quicksort-partition", recursive["source_step_kinds"])
        self.assertIn(
            "quicksort-iterate-right", recursive["source_step_kinds"]
        )
        fallback = payload["cases"]["imbalance-fallback-direct"]
        self.assertIn("heapsort-enter", fallback["source_step_kinds"])
        self.assertEqual(fallback["expected"]["terminal_status"], model.NORMAL)

    def test_arbitrary_duplicate_classes_sort_by_contract_order(self) -> None:
        sequence = permutation(80, 0)
        boundary = model.rank_total_order_boundary(
            {identity: identity % 6 for identity in sequence}
        )
        run = model.execute(model.SortInput(sequence), boundary)
        self.assertEqual(run.terminal_status, model.NORMAL)
        self.assertTrue(model.sequence_is_permutation(run, sequence))
        self.assertTrue(model.sequence_is_contract_sorted(run, boundary))
        ranks = [identity % 6 for identity in run.state.sequence]
        self.assertEqual(ranks, sorted(ranks))

    def test_independent_interpreter_corresponds_for_normal_and_panic(self) -> None:
        configurations = (
            model.SourceConfiguration(),
            model.SourceConfiguration(optimize_for_size=True),
            model.SourceConfiguration(is_freeze=True, is_copy=True),
            model.SourceConfiguration(
                element_size=24,
                is_freeze=True,
                is_copy=True,
                has_efficient_in_place_swap=False,
            ),
            model.SourceConfiguration(element_size=128),
        )
        for index, configuration in enumerate(configurations):
            sequence = permutation(45, 8300 + index)
            normal_boundary = model.integer_total_order_boundary()
            normal = model.execute(
                model.SortInput(sequence, configuration), normal_boundary
            )
            states = (0, max(0, normal.state.callback_state // 2))
            for panic_state in (None, *states):
                with self.subTest(
                    configuration=configuration,
                    panic_state=panic_state,
                ):
                    boundary = (
                        normal_boundary
                        if panic_state is None
                        else model.integer_total_order_boundary(
                            panic_states=frozenset({panic_state})
                        )
                    )
                    actual = model.execute(
                        model.SortInput(sequence, configuration), boundary
                    )
                    expected = reference.execute(
                        sequence, configuration, boundary
                    )
                    self.assertEqual(
                        (
                            actual.state.sequence,
                            actual.state.callback_state,
                            actual.terminal_status,
                            actual.state.panicked,
                            actual.state.aborted,
                            actual.unit_returned,
                        ),
                        (
                            expected.sequence,
                            expected.callback_state,
                            expected.terminal_status,
                            expected.panicked,
                            expected.aborted,
                            expected.unit_returned,
                        ),
                    )

    def test_independent_configuration_predicates_use_shared_fields(
        self,
    ) -> None:
        configuration = model.SourceConfiguration(
            element_size=8,
            is_freeze=True,
            is_copy=True,
        )
        forbidden = (
            "is_zst",
            "efficient_swap",
            "use_configuration_heapsort",
        )
        source = (
            ROOT / "tools/target_080_source_interpreter_v1.py"
        ).read_text()
        for name in forbidden:
            self.assertNotIn(f"configuration.{name}", source)
        run = reference.execute(
            permutation(26, 8306),
            configuration,
            model.integer_total_order_boundary(),
        )
        self.assertEqual(run.terminal_status, model.NORMAL)
        self.assertEqual(run.sequence, tuple(range(26)))

    def test_retained_witnesses_are_field_complete(self) -> None:
        payload = witnesses.witness_payload()
        self.assertEqual(len(payload["cases"]), 28)
        for name, case in payload["cases"].items():
            with self.subTest(name=name):
                primary, secondary, _, correspondence = (
                    witnesses.execute_spec(case["spec"])
                )
                self.assertEqual(primary, secondary)
                self.assertEqual(primary, case["expected"])
                self.assertTrue(
                    correspondence["callback_schedule_equal"]
                )
                self.assertEqual(
                    correspondence, case["callback_correspondence"]
                )

    def test_threshold_mutation_changes_reachable_dispatch(self) -> None:
        sequence = (1, 0, *range(2, 21))
        baseline = model.execute(
            model.SortInput(sequence),
            model.integer_total_order_boundary(),
        )
        self.assertTrue(
            any(
                step.kind == "quicksort-dispatch"
                for step in baseline.derived_steps
            )
        )
        with mock.patch.object(
            model, "MAX_LEN_ALWAYS_INSERTION_SORT", 21
        ):
            mutated = model.execute(
                model.SortInput(sequence),
                model.integer_total_order_boundary(),
            )
        self.assertTrue(
            any(
                step.phase == "sort:insertion"
                for step in mutated.derived_steps
            )
        )
        self.assertNotEqual(
            baseline.state.callback_state, mutated.state.callback_state
        )


if __name__ == "__main__":
    unittest.main()
