#!/usr/bin/env python3
"""Independent public adapter around the accepted Rust 1.96 sort interpreter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import target_080_source_interpreter_v1 as private_reference
import target_081_operational_v1 as model


@dataclass(frozen=True)
class _PrivateObservation:
    is_less: bool
    next_state: int
    panicked: bool


def _rank(boundary: Any, identity: int) -> tuple[int, int]:
    ranks = dict(boundary.rank_pairs)
    if identity in ranks:
        return (0, ranks[identity])
    return (1, identity)


def _ordering(
    boundary: Any,
    state: int,
    left_identity: int,
    right_identity: int,
    observable_element_state: tuple[int, ...],
) -> int:
    mode = boundary.ordering_mode
    if mode == model.IDENTITY_TOTAL_ORDER:
        left_key: Any = left_identity
        right_key: Any = right_identity
    elif mode in (
        model.RANK_TOTAL_ORDER,
        model.STATE_PARITY_ORDER,
        model.INTERIOR_PARITY_ORDER,
    ):
        left_key = _rank(boundary, left_identity)
        right_key = _rank(boundary, right_identity)
        if mode == model.STATE_PARITY_ORDER and state % 2:
            left_key, right_key = right_key, left_key
        if (
            mode == model.INTERIOR_PARITY_ORDER
            and sum(observable_element_state) % 2
        ):
            left_key, right_key = right_key, left_key
    elif mode == model.CONSTANT_EQUAL:
        return model.EQUAL
    elif mode == model.EXPLICIT_ORDERING:
        table = {
            (left, right): ordering
            for left, right, ordering in boundary.explicit_orderings
        }
        if (left_identity, right_identity) in table:
            return table[(left_identity, right_identity)]
        left_key = left_identity
        right_key = right_identity
    else:
        raise ValueError(f"unsupported independent Ordering mode: {mode}")
    if left_key < right_key:
        return model.LESS
    if left_key > right_key:
        return model.GREATER
    return model.EQUAL


def _next_state(
    mode: str, state: int, multiplier: int, offset: int
) -> int:
    if mode == model.INCREMENT_STATE:
        return state + 1
    if mode == model.IDENTITY_STATE:
        return state
    if mode == model.AFFINE_STATE:
        return multiplier * state + offset
    raise ValueError(f"unsupported independent state mode: {mode}")


def _next_observable_element_state(
    mode: str,
    state: tuple[int, ...],
    multiplier: int,
    offset: int,
) -> tuple[int, ...]:
    return tuple(
        _next_state(mode, value, multiplier, offset)
        for value in state
    )


class _OrderingToLessAdapter:
    def __init__(self, boundary: Any) -> None:
        self.boundary = boundary
        self.initial_state = boundary.initial_state
        self.observable_element_state = (
            boundary.initial_observable_element_state
        )
        self.events: list[model.AdapterEvent] = []

    def observe(
        self, state: int, left_identity: int, right_identity: int
    ) -> _PrivateObservation:
        before = self.observable_element_state
        ordering = _ordering(
            self.boundary,
            state,
            left_identity,
            right_identity,
            before,
        )
        next_state = _next_state(
            self.boundary.next_state_mode,
            state,
            self.boundary.affine_multiplier,
            self.boundary.affine_offset,
        )
        panicked = (
            state in self.boundary.panic_states
            or model.ObservationKey(
                state, left_identity, right_identity
            )
            in self.boundary.panic_keys
        )
        after = _next_observable_element_state(
            self.boundary.interior_next_state_mode,
            before,
            self.boundary.interior_affine_multiplier,
            self.boundary.interior_affine_offset,
        )
        self.observable_element_state = after
        is_less = not panicked and ordering == model.LESS
        self.events.append(
            model.AdapterEvent(
                state=state,
                observable_element_state_before=before,
                left_identity=left_identity,
                right_identity=right_identity,
                ordering=ordering,
                next_state=next_state,
                observable_element_state_after=after,
                panicked=panicked,
                callback_evaluations=1,
                less_tested=not panicked,
                is_less=is_less,
            )
        )
        return _PrivateObservation(is_less, next_state, panicked)


@dataclass(frozen=True)
class ReferenceExecution:
    state: model.FinalState
    terminal_status: str
    unit_returned: bool
    private_terminal_status: str
    panic_phase: str | None
    abort_phase: str | None
    adapter_events: tuple[model.AdapterEvent, ...]
    comparator_observation: tuple[tuple[int, int, int, int], ...]
    private_events: tuple[Any, ...]


def execute(
    initial_sequence: tuple[int, ...],
    configuration: Any,
    boundary: Any,
) -> ReferenceExecution:
    adapter = _OrderingToLessAdapter(boundary)
    private = private_reference.execute(
        initial_sequence, configuration, adapter
    )
    status = private.terminal_status
    callback_state = private.callback_state
    observable_element_state = adapter.observable_element_state
    panic_phase: str | None = None
    abort_phase: str | None = None
    drop_invoked = False
    drop_completed = False

    callback_events = [
        event for event in private.events if event.kind == "callback"
    ]
    if callback_events and callback_events[-1].detail("panicked"):
        panic_phase = callback_events[-1].phase

    if status != model.ABORT:
        drop_invoked = True
        unwinding = status == model.PANIC
        callback_state = _next_state(
            boundary.drop_next_state_mode,
            callback_state,
            boundary.drop_affine_multiplier,
            boundary.drop_affine_offset,
        )
        observable_element_state = _next_observable_element_state(
            boundary.drop_interior_next_state_mode,
            observable_element_state,
            boundary.drop_interior_affine_multiplier,
            boundary.drop_interior_affine_offset,
        )
        panic_states = (
            boundary.drop_panic_unwind_states
            if unwinding
            else boundary.drop_panic_normal_states
        )
        drop_panicked = private.callback_state in panic_states
        drop_completed = not drop_panicked
        if drop_panicked:
            if unwinding:
                status = model.ABORT
                abort_phase = "callback-drop-during-unwind"
            else:
                status = model.PANIC
                panic_phase = "callback-drop-after-normal-sort"

    events = tuple(adapter.events)
    if len(callback_events) != len(events):
        raise RuntimeError("independent adapter/private callback count diverged")
    observation = tuple(
        (
            event.state,
            event.left_identity,
            event.right_identity,
            event.ordering,
        )
        for event in events
    )
    return ReferenceExecution(
        state=model.FinalState(
            sequence=private.sequence,
            callback_state=callback_state,
            observable_element_state=observable_element_state,
            panicked=status == model.PANIC,
            aborted=status == model.ABORT,
            terminal=True,
            callback_drop_invoked=drop_invoked,
            callback_drop_completed=drop_completed,
        ),
        terminal_status=status,
        unit_returned=status == model.NORMAL,
        private_terminal_status=private.terminal_status,
        panic_phase=panic_phase,
        abort_phase=abort_phase,
        adapter_events=events,
        comparator_observation=observation,
        private_events=private.events,
    )
