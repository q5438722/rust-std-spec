#!/usr/bin/env python3
"""Independent Rust 1.96 interpreter for target 082."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import target_078_operational_v1 as selection
import target_080_source_interpreter_v1 as private_reference
import target_082_operational_v1 as model


def _next(mode: str, value: int, multiplier: int, offset: int) -> int:
    if mode == model.INCREMENT_STATE:
        return value + 1
    if mode == model.IDENTITY_STATE:
        return value
    if mode == model.AFFINE_STATE:
        return multiplier * value + offset
    raise ValueError(f"unsupported independent transition mode: {mode}")


def _next_interior(
    mode: str,
    values: tuple[int, ...],
    multiplier: int,
    offset: int,
) -> tuple[int, ...]:
    return tuple(_next(mode, value, multiplier, offset) for value in values)


def _contract_key(boundary: Any, identity: int) -> int:
    return dict(boundary.key_pairs).get(identity, identity)


def _runtime_key(
    boundary: Any,
    state: int,
    identity: int,
    interior: tuple[int, ...],
) -> int:
    base = _contract_key(boundary, identity)
    if boundary.key_mode == model.CONTRACT_KEY:
        return base
    if boundary.key_mode == model.STATE_OFFSET_KEY:
        return base + state
    if boundary.key_mode == model.INTERIOR_OFFSET_KEY:
        return base + sum(interior)
    raise ValueError("unsupported independent key mode")


def _rank(boundary: Any, key: int) -> tuple[int, int]:
    ranks = dict(boundary.rank_pairs)
    return (0, ranks[key]) if key in ranks else (1, key)


def _is_less(
    boundary: Any,
    state: int,
    left: model.OwnedKeyIdentity,
    right: model.OwnedKeyIdentity,
    interior: tuple[int, ...],
) -> bool:
    mode = boundary.ordering_mode
    if mode == model.KEY_TOTAL_ORDER:
        left_key: Any = left.key_identity
        right_key: Any = right.key_identity
    elif mode in {
        model.RANK_TOTAL_ORDER,
        model.STATE_PARITY_ORDER,
        model.INTERIOR_PARITY_ORDER,
    }:
        left_key = _rank(boundary, left.key_identity)
        right_key = _rank(boundary, right.key_identity)
        if mode == model.STATE_PARITY_ORDER and state % 2:
            left_key, right_key = right_key, left_key
        if mode == model.INTERIOR_PARITY_ORDER and sum(interior) % 2:
            left_key, right_key = right_key, left_key
    elif mode == model.CONSTANT_EQUAL:
        return False
    else:
        raise ValueError("unsupported independent ordering mode")
    return left_key < right_key


class _IndependentAdapter:
    def __init__(self, boundary: Any) -> None:
        self.boundary = boundary
        self.initial_state = boundary.initial_state
        self.interior = boundary.initial_observable_element_state
        self.events: list[model.AdapterEvent] = []
        self.invocations: list[model.AdapterResult] = []

    def transition(
        self, state: int, left_identity: int, right_identity: int
    ) -> model.AdapterResult:
        invocation = len(self.invocations)
        current = state
        interior = self.interior
        status = model.NORMAL
        panic_origin: str | None = None
        is_less: bool | None = None
        events: list[model.AdapterEvent] = []
        left_owned: model.OwnedKeyIdentity | None = None
        right_owned: model.OwnedKeyIdentity | None = None

        def key_step(
            slot: model.KeySlot, source: int, action: str
        ) -> model.OwnedKeyIdentity | None:
            nonlocal current, interior, status, panic_origin
            before_state = current
            before_interior = interior
            key_identity = _runtime_key(
                self.boundary, current, source, interior
            )
            next_state = _next(
                self.boundary.key_next_state_mode,
                current,
                self.boundary.key_state_multiplier,
                self.boundary.key_state_offset,
            )
            next_interior = _next_interior(
                self.boundary.key_interior_mode,
                interior,
                self.boundary.key_interior_multiplier,
                self.boundary.key_interior_offset,
            )
            panicked = (
                current in self.boundary.key_panic_states
                or model.KeyCallKey(current, slot, source)
                in self.boundary.key_panic_calls
            )
            current = next_state
            interior = next_interior
            owned = None
            if panicked:
                status = model.PANIC
                panic_origin = action
            else:
                owned = model.OwnedKeyIdentity(
                    invocation,
                    before_state,
                    slot,
                    source,
                    key_identity,
                )
            events.append(
                model.AdapterEvent(
                    action,
                    invocation,
                    before_state,
                    current,
                    before_interior,
                    interior,
                    panicked,
                    False,
                    source_identity=source,
                    owned_key=owned,
                    result_available=not panicked,
                )
            )
            return owned

        def ord_step() -> None:
            nonlocal current, interior, status, panic_origin, is_less
            assert left_owned is not None and right_owned is not None
            before_state = current
            before_interior = interior
            less = _is_less(
                self.boundary,
                current,
                left_owned,
                right_owned,
                interior,
            )
            panicked = current in self.boundary.ord_panic_states
            current = _next(
                self.boundary.ord_next_state_mode,
                current,
                self.boundary.ord_state_multiplier,
                self.boundary.ord_state_offset,
            )
            interior = _next_interior(
                self.boundary.ord_interior_mode,
                interior,
                self.boundary.ord_interior_multiplier,
                self.boundary.ord_interior_offset,
            )
            events.append(
                model.AdapterEvent(
                    "ord-lt",
                    invocation,
                    before_state,
                    current,
                    before_interior,
                    interior,
                    panicked,
                    False,
                    left_owned_key=left_owned,
                    right_owned_key=right_owned,
                    result_available=not panicked,
                    is_less=None if panicked else less,
                )
            )
            if panicked:
                status = model.PANIC
                panic_origin = "ord-lt"
            else:
                is_less = less

        def drop_step(
            owned: model.OwnedKeyIdentity, action: str
        ) -> None:
            nonlocal current, interior, status, panic_origin
            if status == model.ABORT:
                return
            before_state = current
            before_interior = interior
            unwinding = status == model.PANIC
            selector = model.KeyDropKey(current, owned.slot)
            panic_set = (
                self.boundary.key_drop_panic_unwind
                if unwinding
                else self.boundary.key_drop_panic_normal
            )
            panicked = selector in panic_set
            current = _next(
                self.boundary.key_drop_next_state_mode,
                current,
                self.boundary.key_drop_state_multiplier,
                self.boundary.key_drop_state_offset,
            )
            interior = _next_interior(
                self.boundary.key_drop_interior_mode,
                interior,
                self.boundary.key_drop_interior_multiplier,
                self.boundary.key_drop_interior_offset,
            )
            events.append(
                model.AdapterEvent(
                    action,
                    invocation,
                    before_state,
                    current,
                    before_interior,
                    interior,
                    panicked,
                    unwinding,
                    owned_key=owned,
                )
            )
            if panicked:
                status = model.ABORT if unwinding else model.PANIC
                panic_origin = action

        left_owned = key_step(
            model.KeySlot.LEFT, left_identity, "key-left"
        )
        if status == model.NORMAL:
            right_owned = key_step(
                model.KeySlot.RIGHT, right_identity, "key-right"
            )
        if status == model.NORMAL:
            ord_step()
        if right_owned is not None:
            drop_step(right_owned, "drop-key-right")
        if left_owned is not None and status != model.ABORT:
            drop_step(left_owned, "drop-key-left")
        if status != model.NORMAL:
            is_less = None
        result = model.AdapterResult(
            status,
            current,
            interior,
            is_less,
            panic_origin,
            tuple(events),
        )
        self.interior = interior
        self.events.extend(events)
        self.invocations.append(result)
        return result


class _AdapterAbort(BaseException):
    def __init__(self, phase: str) -> None:
        super().__init__(phase)
        self.phase = phase


class _ReferenceEngine(selection._Engine):
    def __init__(
        self,
        initial: tuple[int, ...],
        configuration: Any,
        adapter: _IndependentAdapter,
    ) -> None:
        source_input = selection.SelectionInput(
            initial_sequence=initial,
            index=0,
            allocation=82,
            borrow=82,
            is_zst=configuration.element_size == 0,
            configuration=selection.SourceConfiguration(
                optimize_for_size=configuration.optimize_for_size,
                element_size=configuration.element_size,
            ),
        )
        super().__init__(source_input, adapter)
        self.adapter = adapter
        self.abort_phase: str | None = None

    def is_less(
        self, left_identity: int, right_identity: int, phase: str
    ) -> bool:
        before = self.callback_state
        result = self.adapter.transition(
            before, left_identity, right_identity
        )
        self.callback_state = result.final_state
        self.record(
            "callback",
            phase,
            adapter_terminal_status=result.terminal_status,
            left_identity=left_identity,
            next_state=result.final_state,
            ordering=(
                selection.LESS if result.is_less else selection.GREATER
            ),
            panicked=result.terminal_status != model.NORMAL,
            right_identity=right_identity,
            state=before,
        )
        if result.terminal_status == model.ABORT:
            self.abort_phase = f"{phase}:{result.panic_origin}"
            raise _AdapterAbort(self.abort_phase)
        if result.terminal_status == model.PANIC:
            raise selection._CallbackPanic(phase)
        assert result.is_less is not None
        return result.is_less


@dataclass(frozen=True)
class ReferenceExecution:
    state: model.FinalState
    terminal_status: str
    unit_returned: bool
    private_terminal_status: str
    panic_phase: str | None
    panic_origin: str | None
    abort_phase: str | None
    adapter_events: tuple[model.AdapterEvent, ...]
    private_events: tuple[Any, ...]


def _execute_private(
    initial: tuple[int, ...],
    configuration: Any,
    adapter: _IndependentAdapter,
) -> tuple[_ReferenceEngine, str]:
    engine = _ReferenceEngine(initial, configuration, adapter)
    status = model.NORMAL
    try:
        length = len(engine.sequence)
        if configuration.element_size == 0 or length < 2:
            pass
        elif (
            configuration.optimize_for_size
            or configuration.target_pointer_width == 16
        ):
            private_reference._heap(
                engine, 0, length, "sort:configuration-heapsort"
            )
        elif length <= private_reference.MAX_LEN_ALWAYS_INSERTION_SORT:
            selection._insertion_sort_shift_left(engine, 0, length, 1)
        else:
            run = 2
            descending = engine.is_less(
                engine.sequence[1],
                engine.sequence[0],
                "find-existing-run:direction",
            )
            if descending:
                while run < length and engine.is_less(
                    engine.sequence[run],
                    engine.sequence[run - 1],
                    "find-existing-run:descending",
                ):
                    run += 1
            else:
                while run < length and not engine.is_less(
                    engine.sequence[run],
                    engine.sequence[run - 1],
                    "find-existing-run:ascending",
                ):
                    run += 1
            if run == length:
                if descending:
                    engine.sequence.reverse()
            else:
                limit = 2 * ((length | 1).bit_length() - 1)
                private_reference._quick(
                    engine,
                    configuration,
                    0,
                    length,
                    None,
                    limit,
                )
    except selection._CallbackPanic:
        status = model.PANIC
    except _AdapterAbort:
        status = model.ABORT
    except private_reference._Abort:
        status = model.ABORT
    return engine, status


def execute(
    initial_sequence: tuple[int, ...],
    configuration: Any,
    boundary: Any,
) -> ReferenceExecution:
    adapter = _IndependentAdapter(boundary)
    engine, private_status = _execute_private(
        initial_sequence, configuration, adapter
    )
    status = private_status
    callback_state = engine.callback_state
    interior = adapter.interior
    panic_origin = (
        adapter.invocations[-1].panic_origin
        if adapter.invocations
        and adapter.invocations[-1].terminal_status != model.NORMAL
        else None
    )
    panic_phase = None
    abort_phase = engine.abort_phase
    callback_events = [
        event for event in engine.events if event.kind == "callback"
    ]
    if callback_events and callback_events[-1].detail("panicked"):
        if private_status == model.PANIC:
            panic_phase = callback_events[-1].phase
        elif abort_phase is None:
            abort_phase = callback_events[-1].phase
    f_drop_invoked = False
    f_drop_completed = False

    if status != model.ABORT:
        f_drop_invoked = True
        unwinding = status == model.PANIC
        before_state = callback_state
        before_interior = interior
        callback_state = _next(
            boundary.f_drop_next_state_mode,
            callback_state,
            boundary.f_drop_state_multiplier,
            boundary.f_drop_state_offset,
        )
        interior = _next_interior(
            boundary.f_drop_interior_mode,
            interior,
            boundary.f_drop_interior_multiplier,
            boundary.f_drop_interior_offset,
        )
        panic_states = (
            boundary.f_drop_panic_unwind_states
            if unwinding
            else boundary.f_drop_panic_normal_states
        )
        panicked = before_state in panic_states
        adapter.events.append(
            model.AdapterEvent(
                "drop-f",
                len(adapter.invocations),
                before_state,
                callback_state,
                before_interior,
                interior,
                panicked,
                unwinding,
            )
        )
        f_drop_completed = not panicked
        if panicked:
            panic_origin = "drop-f"
            if unwinding:
                status = model.ABORT
                abort_phase = "drop-f-during-unwind"
            else:
                status = model.PANIC
                panic_phase = "drop-f-after-normal-sort"

    return ReferenceExecution(
        state=model.FinalState(
            tuple(engine.sequence),
            callback_state,
            interior,
            status == model.PANIC,
            status == model.ABORT,
            True,
            f_drop_invoked,
            f_drop_completed,
        ),
        terminal_status=status,
        unit_returned=status == model.NORMAL,
        private_terminal_status=private_status,
        panic_phase=panic_phase,
        panic_origin=panic_origin,
        abort_phase=abort_phase,
        adapter_events=tuple(adapter.events),
        private_events=tuple(engine.events),
    )
