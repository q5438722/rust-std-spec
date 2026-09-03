#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import target_078_operational_v1 as accepted_selection
import target_079_operational_v1 as model


LEFT = 10
RIGHT = 20


def actions(result: model.AdapterResult) -> list[str]:
    return [event.action for event in result.events]


def fixture_boundary(
    *,
    key_panics: frozenset[tuple[int, int]] = frozenset(),
    ord_panics: frozenset[tuple[int, int, int]] = frozenset(),
    drop_panics: Callable[
        [int, model.OwnedKeyIdentity], bool
    ] = lambda _state, _owned: False,
) -> model.KeyOrdDropBoundary:
    def key(state: int, value: int) -> model.KeyObservation:
        return model.KeyObservation(
            value,
            state + 1,
            (state, value) in key_panics,
        )

    def ord_lt(
        state: int,
        left: model.OwnedKeyIdentity,
        right: model.OwnedKeyIdentity,
    ) -> model.OrdLtObservation:
        return model.OrdLtObservation(
            left.key_identity < right.key_identity,
            state + 1,
            (
                state,
                left.key_identity,
                right.key_identity,
            )
            in ord_panics,
        )

    def drop(
        state: int, owned: model.OwnedKeyIdentity
    ) -> model.DropObservation:
        return model.DropObservation(
            state + 1,
            drop_panics(state, owned),
        )

    return model.KeyOrdDropBoundary(key=key, ord_lt=ord_lt, drop=drop)


class Target079AdapterLifecycleTests(unittest.TestCase):
    def test_normal_order_and_reverse_destruction(self) -> None:
        result = model.KeyOrdDropBoundary().transition(0, LEFT, RIGHT)
        self.assertEqual(result.termination, model.AdapterTermination.NORMAL)
        self.assertTrue(result.is_less)
        self.assertEqual(
            actions(result),
            [
                "key-left",
                "key-right",
                "ord-lt",
                "drop-right",
                "drop-left",
            ],
        )
        self.assertEqual(result.final_state, 5)
        self.assertFalse(any(event.unwinding for event in result.events))
        left = result.events[0].owned_key
        right = result.events[1].owned_key
        self.assertIsNotNone(left)
        self.assertIsNotNone(right)
        self.assertNotEqual(left, right)

    def test_first_key_panic_owns_no_key_temporary(self) -> None:
        boundary = fixture_boundary(
            key_panics=frozenset({(0, LEFT)})
        )
        result = boundary.transition(0, LEFT, RIGHT)
        self.assertEqual(result.termination, model.AdapterTermination.PANIC)
        self.assertEqual(actions(result), ["key-left"])
        self.assertIsNone(result.events[0].owned_key)

    def test_second_key_panic_drops_only_left_during_unwind(self) -> None:
        boundary = fixture_boundary(
            key_panics=frozenset({(1, RIGHT)})
        )
        result = boundary.transition(0, LEFT, RIGHT)
        self.assertEqual(result.termination, model.AdapterTermination.PANIC)
        self.assertEqual(
            actions(result), ["key-left", "key-right", "drop-left"]
        )
        self.assertTrue(result.events[-1].unwinding)
        self.assertEqual(
            result.events[-1].owned_key.slot,
            model.KeySlot.LEFT,
        )

    def test_ord_panic_drops_right_then_left_during_unwind(self) -> None:
        boundary = fixture_boundary(
            ord_panics=frozenset({(2, LEFT, RIGHT)})
        )
        result = boundary.transition(0, LEFT, RIGHT)
        self.assertEqual(result.termination, model.AdapterTermination.PANIC)
        self.assertEqual(
            actions(result),
            [
                "key-left",
                "key-right",
                "ord-lt",
                "drop-right",
                "drop-left",
            ],
        )
        self.assertTrue(result.events[-2].unwinding)
        self.assertTrue(result.events[-1].unwinding)

    def test_lt_panic_right_cleanup_then_left_drop_panic_aborts(
        self,
    ) -> None:
        boundary = fixture_boundary(
            ord_panics=frozenset({(2, LEFT, RIGHT)}),
            drop_panics=lambda state, owned: (
                state == 4 and owned.slot == model.KeySlot.LEFT
            ),
        )
        result = boundary.transition(0, LEFT, RIGHT)
        self.assertEqual(result.termination, model.AdapterTermination.ABORT)
        self.assertEqual(
            actions(result)[-2:], ["drop-right", "drop-left"]
        )
        self.assertFalse(result.events[-2].panicked)
        self.assertTrue(result.events[-1].panicked)
        self.assertTrue(result.events[-1].unwinding)
        self.assertEqual(result.panic_origin, "drop-left")

    def test_destructor_panic_paths(self) -> None:
        cases = {
            "right": (
                lambda state, owned: (
                    state == 3 and owned.slot == model.KeySlot.RIGHT
                ),
                model.AdapterTermination.PANIC,
                [False, True],
            ),
            "left": (
                lambda state, owned: (
                    state == 4 and owned.slot == model.KeySlot.LEFT
                ),
                model.AdapterTermination.PANIC,
                [False, False],
            ),
            "double": (
                lambda state, _owned: state in {3, 4},
                model.AdapterTermination.ABORT,
                [False, True],
            ),
        }
        for label, (drop_panics, termination, unwind_flags) in cases.items():
            with self.subTest(label=label):
                result = fixture_boundary(
                    drop_panics=drop_panics
                ).transition(0, LEFT, RIGHT)
                self.assertEqual(result.termination, termination)
                self.assertEqual(
                    [
                        event.unwinding
                        for event in result.events
                        if event.action.startswith("drop-")
                    ],
                    unwind_flags,
                )

    def test_double_panic_stops_cleanup_immediately(self) -> None:
        boundary = fixture_boundary(
            ord_panics=frozenset({(2, LEFT, RIGHT)}),
            drop_panics=lambda state, owned: (
                state == 3 and owned.slot == model.KeySlot.RIGHT
            ),
        )
        result = boundary.transition(0, LEFT, RIGHT)
        self.assertEqual(result.termination, model.AdapterTermination.ABORT)
        self.assertEqual(actions(result)[-1], "drop-right")
        self.assertNotIn("drop-left", actions(result))

    def test_second_key_panic_plus_left_drop_panic_aborts(self) -> None:
        boundary = fixture_boundary(
            key_panics=frozenset({(1, RIGHT)}),
            drop_panics=lambda state, owned: (
                state == 2 and owned.slot == model.KeySlot.LEFT
            ),
        )
        result = boundary.transition(0, LEFT, RIGHT)
        self.assertEqual(result.termination, model.AdapterTermination.ABORT)
        self.assertEqual(actions(result)[-1], "drop-left")

    def test_arbitrary_state_dependent_total_functions(self) -> None:
        def contract_key(value: int) -> int:
            return abs(value)

        def key(state: int, value: int) -> model.KeyObservation:
            return model.KeyObservation(
                abs(value),
                state * 3 + abs(value) + 1,
                False,
            )

        def ord_lt(
            state: int,
            left: model.OwnedKeyIdentity,
            right: model.OwnedKeyIdentity,
        ) -> model.OrdLtObservation:
            return model.OrdLtObservation(
                left.key_identity < right.key_identity,
                state * 2 + left.key_identity + right.key_identity,
                False,
            )

        def drop(
            state: int, owned: model.OwnedKeyIdentity
        ) -> model.DropObservation:
            return model.DropObservation(
                state + 11 + int(owned.slot),
                False,
            )

        boundary = model.KeyOrdDropBoundary(
            initial_state=7,
            key=key,
            ord_lt=ord_lt,
            drop=drop,
            contract_key=contract_key,
        )
        result = boundary.transition(7, -3, 5)
        self.assertEqual(result.termination, model.AdapterTermination.NORMAL)
        self.assertTrue(result.is_less)
        self.assertEqual(result.final_state, 193)

    def test_equal_abstract_keys_still_have_two_owned_identities(self) -> None:
        dropped: list[model.OwnedKeyIdentity] = []

        def drop(
            state: int, owned: model.OwnedKeyIdentity
        ) -> model.DropObservation:
            dropped.append(owned)
            return model.DropObservation(state + 1, False)

        boundary = model.KeyOrdDropBoundary(
            key=lambda state, _value: model.KeyObservation(
                0, state + 1, False
            ),
            ord_lt=lambda state, _left, _right: model.OrdLtObservation(
                False, state + 1, False
            ),
            drop=drop,
            contract_key=lambda _value: 0,
            contract_ordering_function=lambda _left, _right: (
                accepted_selection.EQUAL
            ),
        )
        result = boundary.transition(0, LEFT, LEFT)
        self.assertEqual(result.termination, model.AdapterTermination.NORMAL)
        self.assertEqual(len(dropped), 2)
        self.assertNotEqual(dropped[0], dropped[1])
        self.assertEqual(
            [owned.slot for owned in dropped],
            [model.KeySlot.RIGHT, model.KeySlot.LEFT],
        )

    def test_inadmissible_runtime_contract_projection_is_rejected(
        self,
    ) -> None:
        boundary = model.KeyOrdDropBoundary(
            key=lambda state, value: model.KeyObservation(
                value + 1, state, False
            )
        )
        with self.assertRaises(model.BoundaryViolation):
            boundary.transition(0, LEFT, RIGHT)


class Target079SelectionCompositionTests(unittest.TestCase):
    @staticmethod
    def selection_input(
        sequence: tuple[int, ...] = (4, 3, 2, 1),
        index: int = 1,
        *,
        element_size: int = 8,
        optimize_for_size: bool = False,
        is_zst: bool = False,
    ) -> model.SelectionInput:
        return model.SelectionInput(
            initial_sequence=sequence,
            index=index,
            allocation=790,
            borrow=791,
            is_zst=is_zst,
            configuration=model.SourceConfiguration(
                element_size=element_size,
                optimize_for_size=optimize_for_size,
            ),
        )

    def test_arbitrary_length_normal_run_reuses_accepted_engine(self) -> None:
        selection_input = self.selection_input(
            tuple(range(39, 0, -1)),
            19,
        )
        boundary = model.KeyOrdDropBoundary()
        execution = model.execute(selection_input, boundary)
        self.assertEqual(
            execution.termination, model.AdapterTermination.NORMAL
        )
        self.assertTrue(
            model.active_contract_holds(
                selection_input, boundary, execution
            )
        )
        self.assertGreater(len(execution.adapter_invocations), 0)
        for _, invocation in execution.adapter_invocations:
            self.assertEqual(
                actions(invocation),
                [
                    "key-left",
                    "key-right",
                    "ord-lt",
                    "drop-right",
                    "drop-left",
                ],
            )

    def test_zst_path_performs_no_adapter_call(self) -> None:
        selection_input = self.selection_input(
            (4, 3, 2, 1),
            2,
            element_size=0,
            is_zst=True,
        )
        execution = model.execute(
            selection_input, model.KeyOrdDropBoundary()
        )
        self.assertEqual(execution.selection.branch, "zst")
        self.assertEqual(execution.adapter_invocations, ())

    def test_single_panic_uses_selection_unwind_restoration(self) -> None:
        selection_input = self.selection_input()
        boundary = fixture_boundary(
            ord_panics=frozenset({(2, 3, 4)})
        )
        execution = model.execute(selection_input, boundary)
        self.assertEqual(
            execution.termination, model.AdapterTermination.PANIC
        )
        self.assertCountEqual(
            execution.selection.final_state.sequence,
            selection_input.initial_sequence,
        )

    def test_abort_retains_full_interrupted_state_without_cleanup(
        self,
    ) -> None:
        selection_input = self.selection_input()
        boundary = fixture_boundary(
            ord_panics=frozenset({(12, 2, 3)}),
            drop_panics=lambda state, owned: (
                state == 14 and owned.slot == model.KeySlot.LEFT
            ),
        )
        execution = model.execute(selection_input, boundary)
        self.assertEqual(
            execution.termination, model.AdapterTermination.ABORT
        )
        self.assertEqual(
            execution.selection.coverage_status, model.MODELED_ABORT
        )
        self.assertIsNone(execution.selection.output)
        self.assertEqual(
            execution.selection.final_state.sequence,
            (3, 4, 4, 1),
        )
        self.assertEqual(
            execution.selection.final_state.callback_state,
            15,
        )
        self.assertNotEqual(
            Counter(execution.selection.final_state.sequence),
            Counter(selection_input.initial_sequence),
        )

    def test_same_ord_panic_without_double_panic_restores_copy_guard(
        self,
    ) -> None:
        selection_input = self.selection_input()
        boundary = fixture_boundary(
            ord_panics=frozenset({(12, 2, 3)})
        )
        execution = model.execute(selection_input, boundary)
        self.assertEqual(
            execution.termination, model.AdapterTermination.PANIC
        )
        self.assertEqual(
            execution.selection.final_state.sequence,
            (3, 2, 4, 1),
        )
        self.assertCountEqual(
            execution.selection.final_state.sequence,
            selection_input.initial_sequence,
        )

    def test_all_partition_kernel_configurations_execute(self) -> None:
        cases = (
            (True, 8, "partition-lomuto-branchless-simple"),
            (False, 8, "partition-lomuto-branchless-cyclic"),
            (False, 32, "partition-lomuto-branchless-cyclic"),
            (False, 128, "partition-hoare-branchy-cyclic"),
        )
        sequence = tuple(range(33, 0, -1))
        for optimize, size, phase in cases:
            with self.subTest(optimize=optimize, size=size):
                execution = model.execute(
                    self.selection_input(
                        sequence,
                        16,
                        element_size=size,
                        optimize_for_size=optimize,
                    ),
                    model.KeyOrdDropBoundary(),
                )
                self.assertEqual(
                    execution.termination,
                    model.AdapterTermination.NORMAL,
                )
                phases = {
                    event.phase
                    for event in execution.selection.derived_events
                }
                self.assertIn(phase, phases)

    def test_selection_engine_module_is_unchanged_dependency(self) -> None:
        manifest = model.boundary_manifest()
        self.assertEqual(
            manifest["selection_engine"]["model_id"],
            accepted_selection.MODEL_ID,
        )
        self.assertFalse(
            manifest["selection_engine"]["classification_inherited"]
        )
        self.assertTrue(manifest["source_model_complete"])


if __name__ == "__main__":
    unittest.main()
