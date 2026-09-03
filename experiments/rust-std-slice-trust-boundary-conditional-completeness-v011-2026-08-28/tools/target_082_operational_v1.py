#!/usr/bin/env python3
"""Source-operational Rust 1.96 model for sort_unstable_by_key."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from enum import IntEnum
from typing import Any

import target_079_operational_v1 as accepted_key_lifecycle
import target_080_operational_v1 as private_sort


TARGET = "core::slice::sort_unstable_by_key"
INPUT_ORDER = "82"
MODEL_ID = "target-082-key-sort-operational-v1-rust-1.96-complete"
MODEL_VERSION = 1
ACTIVE_CONTRACT_SHA256 = (
    "019252db65344fd8830ffbbd90d127355a93541c6fbfab3fde3e6b3abe16e8ae"
)

ADMITTED_TRUST_SITE_IDS = ("TS-082-D004",)
REPLACED_TRUST_SITE_IDS = (
    "TS-082-D002",
    "TS-082-D003",
    "TS-082-E001",
)
CONTEXT_ONLY_TRUST_SITE_IDS = ("TS-082-D001", "TS-082-C001")
PENDING_REPLACEMENT_TRUST_SITE_IDS: tuple[str, ...] = ()
SOURCE_MODEL_COMPLETE = True
CLASSIFICATION_ELIGIBLE = True

NORMAL = private_sort.NORMAL
PANIC = private_sort.PANIC
ABORT = private_sort.ABORT

INCREMENT_STATE = private_sort.INCREMENT_STATE
IDENTITY_STATE = private_sort.IDENTITY_STATE
AFFINE_STATE = private_sort.AFFINE_STATE

CONTRACT_KEY = "contract-key"
STATE_OFFSET_KEY = "state-offset-key"
INTERIOR_OFFSET_KEY = "interior-offset-key"
KEY_TOTAL_ORDER = "key-total-order"
RANK_TOTAL_ORDER = "rank-total-order"
CONSTANT_EQUAL = "constant-equal"
STATE_PARITY_ORDER = "state-parity-order"
INTERIOR_PARITY_ORDER = "interior-parity-order"

SourceConfiguration = private_sort.SourceConfiguration
SortInput = private_sort.SortInput

COVERED_SOURCE_PHASES = (
    "public adapter evaluates f(left) before f(right)",
    "K::lt is evaluated only after both owned K temporaries exist",
    "Ord::lt panic becomes observable before a Boolean less result",
    "right owned K is destroyed before left owned K",
    "ordinary key/Ord panic enters private-sort unwind restoration",
    "owned-key destructor panic during unwind aborts immediately",
    "owned F is destroyed after normal private-sort return or during unwind",
    "owned F destructor panic during unwind aborts immediately",
    "complete callback and externally observable element state propagation",
    *private_sort.COVERED_SOURCE_PHASES[1:],
)
MISSING_SOURCE_PHASES: tuple[str, ...] = ()


class BoundaryViolation(ValueError):
    pass


class KeySlot(IntEnum):
    LEFT = accepted_key_lifecycle.KeySlot.LEFT.value
    RIGHT = accepted_key_lifecycle.KeySlot.RIGHT.value


@dataclass(frozen=True, order=True)
class OwnedKeyIdentity:
    """One source-created owned K, distinct even when values compare equal."""

    invocation: int
    creation_state: int
    slot: KeySlot
    source_identity: int
    key_identity: int


@dataclass(frozen=True, order=True)
class KeyCallKey:
    state: int
    slot: KeySlot
    source_identity: int


@dataclass(frozen=True, order=True)
class KeyDropKey:
    state: int
    slot: KeySlot


@dataclass(frozen=True)
class KeyObservation:
    key_identity: int
    next_state: int
    next_observable_element_state: tuple[int, ...]
    panicked: bool


@dataclass(frozen=True)
class OrdLtObservation:
    is_less: bool
    next_state: int
    next_observable_element_state: tuple[int, ...]
    panicked: bool


@dataclass(frozen=True)
class DropObservation:
    next_state: int
    next_observable_element_state: tuple[int, ...]
    panicked: bool


@dataclass(frozen=True)
class KeySortBoundary:
    """Total key, Ord, owned-key Drop, and owned-F Drop observations."""

    callback_identity: int = 82
    key_function_identity: int = 8201
    ord_function_identity: int = 8202
    key_drop_function_identity: int = 8203
    f_drop_function_identity: int = 8204
    initial_state: int = 0
    initial_observable_element_state: tuple[int, ...] = ()
    key_mode: str = CONTRACT_KEY
    key_pairs: tuple[tuple[int, int], ...] = ()
    ordering_mode: str = KEY_TOTAL_ORDER
    contract_ordering_mode: str | None = KEY_TOTAL_ORDER
    rank_pairs: tuple[tuple[int, int], ...] = ()
    key_next_state_mode: str = INCREMENT_STATE
    key_state_multiplier: int = 1
    key_state_offset: int = 1
    key_interior_mode: str = IDENTITY_STATE
    key_interior_multiplier: int = 1
    key_interior_offset: int = 0
    ord_next_state_mode: str = INCREMENT_STATE
    ord_state_multiplier: int = 1
    ord_state_offset: int = 1
    ord_interior_mode: str = IDENTITY_STATE
    ord_interior_multiplier: int = 1
    ord_interior_offset: int = 0
    key_drop_next_state_mode: str = INCREMENT_STATE
    key_drop_state_multiplier: int = 1
    key_drop_state_offset: int = 1
    key_drop_interior_mode: str = IDENTITY_STATE
    key_drop_interior_multiplier: int = 1
    key_drop_interior_offset: int = 0
    f_drop_next_state_mode: str = IDENTITY_STATE
    f_drop_state_multiplier: int = 1
    f_drop_state_offset: int = 0
    f_drop_interior_mode: str = IDENTITY_STATE
    f_drop_interior_multiplier: int = 1
    f_drop_interior_offset: int = 0
    key_panic_states: frozenset[int] = frozenset()
    key_panic_calls: frozenset[KeyCallKey] = frozenset()
    ord_panic_states: frozenset[int] = frozenset()
    key_drop_panic_normal: frozenset[KeyDropKey] = frozenset()
    key_drop_panic_unwind: frozenset[KeyDropKey] = frozenset()
    f_drop_panic_normal_states: frozenset[int] = frozenset()
    f_drop_panic_unwind_states: frozenset[int] = frozenset()

    def __post_init__(self) -> None:
        if accepted_key_lifecycle.MODEL_ID != (
            "target-079-key-ord-drop-operational-v1-rust-1.96-complete"
        ):
            raise RuntimeError("accepted target-079 lifecycle identity changed")
        if private_sort.MODEL_ID != (
            "target-080-operational-v1-rust-1.96-complete"
        ):
            raise RuntimeError("accepted target-080 sort identity changed")
        if self.key_mode not in {
            CONTRACT_KEY,
            STATE_OFFSET_KEY,
            INTERIOR_OFFSET_KEY,
        }:
            raise BoundaryViolation("unknown key extraction mode")
        ordering_modes = {
            KEY_TOTAL_ORDER,
            RANK_TOTAL_ORDER,
            CONSTANT_EQUAL,
            STATE_PARITY_ORDER,
            INTERIOR_PARITY_ORDER,
        }
        if self.ordering_mode not in ordering_modes:
            raise BoundaryViolation("unknown Ord::lt mode")
        if self.contract_ordering_mode not in {
            None,
            KEY_TOTAL_ORDER,
            RANK_TOTAL_ORDER,
            CONSTANT_EQUAL,
        }:
            raise BoundaryViolation("contract ordering is not total")
        state_modes = {INCREMENT_STATE, IDENTITY_STATE, AFFINE_STATE}
        for name in (
            "key_next_state_mode",
            "key_interior_mode",
            "ord_next_state_mode",
            "ord_interior_mode",
            "key_drop_next_state_mode",
            "key_drop_interior_mode",
            "f_drop_next_state_mode",
            "f_drop_interior_mode",
        ):
            if getattr(self, name) not in state_modes:
                raise BoundaryViolation(f"unknown transition mode: {name}")
        for pairs, label in (
            (self.key_pairs, "source identities"),
            (self.rank_pairs, "key ranks"),
        ):
            keys = [key for key, _ in pairs]
            if len(keys) != len(set(keys)):
                raise BoundaryViolation(f"{label} must be unique")
        if not isinstance(self.initial_observable_element_state, tuple):
            raise TypeError("observable element state must be a tuple")
        if any(
            not isinstance(value, int)
            for value in self.initial_observable_element_state
        ):
            raise TypeError("observable element state must contain integers")
        for name in (
            "key_panic_states",
            "key_panic_calls",
            "ord_panic_states",
            "key_drop_panic_normal",
            "key_drop_panic_unwind",
            "f_drop_panic_normal_states",
            "f_drop_panic_unwind_states",
        ):
            if not isinstance(getattr(self, name), frozenset):
                raise TypeError(f"{name} must be a frozenset")

    @staticmethod
    def _next_scalar(
        mode: str, state: int, multiplier: int, offset: int
    ) -> int:
        if mode == INCREMENT_STATE:
            return state + 1
        if mode == IDENTITY_STATE:
            return state
        if mode == AFFINE_STATE:
            return multiplier * state + offset
        raise BoundaryViolation(f"unsupported scalar transition: {mode}")

    @classmethod
    def _next_interior(
        cls,
        mode: str,
        state: tuple[int, ...],
        multiplier: int,
        offset: int,
    ) -> tuple[int, ...]:
        return tuple(
            cls._next_scalar(mode, value, multiplier, offset)
            for value in state
        )

    def contract_key(self, source_identity: int) -> int:
        return dict(self.key_pairs).get(source_identity, source_identity)

    def runtime_key(
        self,
        state: int,
        source_identity: int,
        observable_element_state: tuple[int, ...],
    ) -> int:
        base = self.contract_key(source_identity)
        if self.key_mode == CONTRACT_KEY:
            return base
        if self.key_mode == STATE_OFFSET_KEY:
            return base + state
        if self.key_mode == INTERIOR_OFFSET_KEY:
            return base + sum(observable_element_state)
        raise BoundaryViolation("unsupported key extraction mode")

    def _rank(self, key_identity: int) -> tuple[int, int]:
        ranks = dict(self.rank_pairs)
        if key_identity in ranks:
            return (0, ranks[key_identity])
        return (1, key_identity)

    def _is_less(
        self,
        mode: str,
        state: int,
        left: OwnedKeyIdentity,
        right: OwnedKeyIdentity,
        observable_element_state: tuple[int, ...],
    ) -> bool:
        if mode == KEY_TOTAL_ORDER:
            left_key: Any = left.key_identity
            right_key: Any = right.key_identity
        elif mode in {
            RANK_TOTAL_ORDER,
            STATE_PARITY_ORDER,
            INTERIOR_PARITY_ORDER,
        }:
            left_key = self._rank(left.key_identity)
            right_key = self._rank(right.key_identity)
            if mode == STATE_PARITY_ORDER and state % 2:
                left_key, right_key = right_key, left_key
            if (
                mode == INTERIOR_PARITY_ORDER
                and sum(observable_element_state) % 2
            ):
                left_key, right_key = right_key, left_key
        elif mode == CONSTANT_EQUAL:
            return False
        else:
            raise BoundaryViolation(f"unsupported Ord::lt mode: {mode}")
        return left_key < right_key

    def observe_key(
        self,
        state: int,
        slot: KeySlot,
        source_identity: int,
        observable_element_state: tuple[int, ...],
    ) -> KeyObservation:
        call = KeyCallKey(state, slot, source_identity)
        return KeyObservation(
            key_identity=self.runtime_key(
                state, source_identity, observable_element_state
            ),
            next_state=self._next_scalar(
                self.key_next_state_mode,
                state,
                self.key_state_multiplier,
                self.key_state_offset,
            ),
            next_observable_element_state=self._next_interior(
                self.key_interior_mode,
                observable_element_state,
                self.key_interior_multiplier,
                self.key_interior_offset,
            ),
            panicked=(
                state in self.key_panic_states
                or call in self.key_panic_calls
            ),
        )

    def observe_ord_lt(
        self,
        state: int,
        left: OwnedKeyIdentity,
        right: OwnedKeyIdentity,
        observable_element_state: tuple[int, ...],
    ) -> OrdLtObservation:
        return OrdLtObservation(
            is_less=self._is_less(
                self.ordering_mode,
                state,
                left,
                right,
                observable_element_state,
            ),
            next_state=self._next_scalar(
                self.ord_next_state_mode,
                state,
                self.ord_state_multiplier,
                self.ord_state_offset,
            ),
            next_observable_element_state=self._next_interior(
                self.ord_interior_mode,
                observable_element_state,
                self.ord_interior_multiplier,
                self.ord_interior_offset,
            ),
            panicked=state in self.ord_panic_states,
        )

    def observe_key_drop(
        self,
        state: int,
        owned_key: OwnedKeyIdentity,
        observable_element_state: tuple[int, ...],
        *,
        unwinding: bool,
    ) -> DropObservation:
        selector = KeyDropKey(state, owned_key.slot)
        panics = (
            self.key_drop_panic_unwind
            if unwinding
            else self.key_drop_panic_normal
        )
        return DropObservation(
            next_state=self._next_scalar(
                self.key_drop_next_state_mode,
                state,
                self.key_drop_state_multiplier,
                self.key_drop_state_offset,
            ),
            next_observable_element_state=self._next_interior(
                self.key_drop_interior_mode,
                observable_element_state,
                self.key_drop_interior_multiplier,
                self.key_drop_interior_offset,
            ),
            panicked=selector in panics,
        )

    def observe_f_drop(
        self,
        state: int,
        observable_element_state: tuple[int, ...],
        *,
        unwinding: bool,
    ) -> DropObservation:
        panics = (
            self.f_drop_panic_unwind_states
            if unwinding
            else self.f_drop_panic_normal_states
        )
        return DropObservation(
            next_state=self._next_scalar(
                self.f_drop_next_state_mode,
                state,
                self.f_drop_state_multiplier,
                self.f_drop_state_offset,
            ),
            next_observable_element_state=self._next_interior(
                self.f_drop_interior_mode,
                observable_element_state,
                self.f_drop_interior_multiplier,
                self.f_drop_interior_offset,
            ),
            panicked=state in panics,
        )

    def contract_is_less(
        self, left_identity: int, right_identity: int
    ) -> bool:
        if self.contract_ordering_mode is None:
            raise BoundaryViolation("no state-independent contract projection")
        left = OwnedKeyIdentity(
            0, self.initial_state, KeySlot.LEFT, left_identity,
            self.contract_key(left_identity),
        )
        right = OwnedKeyIdentity(
            0, self.initial_state, KeySlot.RIGHT, right_identity,
            self.contract_key(right_identity),
        )
        return self._is_less(
            self.contract_ordering_mode,
            self.initial_state,
            left,
            right,
            self.initial_observable_element_state,
        )

    def contract_admissible(self) -> bool:
        return (
            self.key_mode == CONTRACT_KEY
            and self.contract_ordering_mode is not None
            and self.ordering_mode == self.contract_ordering_mode
            and self.ordering_mode
            not in {STATE_PARITY_ORDER, INTERIOR_PARITY_ORDER}
        )


@dataclass(frozen=True)
class AdapterEvent:
    action: str
    invocation: int
    state_before: int
    state_after: int
    observable_element_state_before: tuple[int, ...]
    observable_element_state_after: tuple[int, ...]
    panicked: bool
    unwinding: bool
    source_identity: int | None = None
    owned_key: OwnedKeyIdentity | None = None
    left_owned_key: OwnedKeyIdentity | None = None
    right_owned_key: OwnedKeyIdentity | None = None
    result_available: bool = False
    is_less: bool | None = None


@dataclass(frozen=True)
class AdapterResult:
    terminal_status: str
    final_state: int
    final_observable_element_state: tuple[int, ...]
    is_less: bool | None
    panic_origin: str | None
    events: tuple[AdapterEvent, ...]


class KeyOrdDropAdapter:
    """Exact source order for `f(a).lt(&f(b))` and its temporaries."""

    def __init__(self, boundary: KeySortBoundary) -> None:
        self.boundary = boundary
        self.initial_state = boundary.initial_state
        self.observable_element_state = (
            boundary.initial_observable_element_state
        )
        self.events: list[AdapterEvent] = []
        self.invocations: list[AdapterResult] = []

    def transition(
        self, state: int, left_identity: int, right_identity: int
    ) -> AdapterResult:
        invocation = len(self.invocations)
        current = state
        interior = self.observable_element_state
        status = NORMAL
        panic_origin: str | None = None
        is_less: bool | None = None
        local_events: list[AdapterEvent] = []
        left_owned: OwnedKeyIdentity | None = None
        right_owned: OwnedKeyIdentity | None = None

        def key_step(
            slot: KeySlot, source_identity: int, action: str
        ) -> OwnedKeyIdentity | None:
            nonlocal current, interior, status, panic_origin
            before_state = current
            before_interior = interior
            observed = self.boundary.observe_key(
                current, slot, source_identity, interior
            )
            current = observed.next_state
            interior = observed.next_observable_element_state
            owned = None
            if observed.panicked:
                status = PANIC
                panic_origin = action
            else:
                owned = OwnedKeyIdentity(
                    invocation,
                    before_state,
                    slot,
                    source_identity,
                    observed.key_identity,
                )
            local_events.append(
                AdapterEvent(
                    action=action,
                    invocation=invocation,
                    state_before=before_state,
                    state_after=current,
                    observable_element_state_before=before_interior,
                    observable_element_state_after=interior,
                    panicked=observed.panicked,
                    unwinding=False,
                    source_identity=source_identity,
                    owned_key=owned,
                    result_available=not observed.panicked,
                )
            )
            return owned

        def ord_step() -> None:
            nonlocal current, interior, status, panic_origin, is_less
            assert left_owned is not None and right_owned is not None
            before_state = current
            before_interior = interior
            observed = self.boundary.observe_ord_lt(
                current, left_owned, right_owned, interior
            )
            current = observed.next_state
            interior = observed.next_observable_element_state
            local_events.append(
                AdapterEvent(
                    action="ord-lt",
                    invocation=invocation,
                    state_before=before_state,
                    state_after=current,
                    observable_element_state_before=before_interior,
                    observable_element_state_after=interior,
                    panicked=observed.panicked,
                    unwinding=False,
                    left_owned_key=left_owned,
                    right_owned_key=right_owned,
                    result_available=not observed.panicked,
                    is_less=(
                        None if observed.panicked else observed.is_less
                    ),
                )
            )
            if observed.panicked:
                status = PANIC
                panic_origin = "ord-lt"
            else:
                is_less = observed.is_less

        def drop_step(owned: OwnedKeyIdentity, action: str) -> None:
            nonlocal current, interior, status, panic_origin
            if status == ABORT:
                return
            before_state = current
            before_interior = interior
            unwinding = status == PANIC
            observed = self.boundary.observe_key_drop(
                current, owned, interior, unwinding=unwinding
            )
            current = observed.next_state
            interior = observed.next_observable_element_state
            local_events.append(
                AdapterEvent(
                    action=action,
                    invocation=invocation,
                    state_before=before_state,
                    state_after=current,
                    observable_element_state_before=before_interior,
                    observable_element_state_after=interior,
                    panicked=observed.panicked,
                    unwinding=unwinding,
                    owned_key=owned,
                )
            )
            if observed.panicked:
                status = ABORT if unwinding else PANIC
                panic_origin = action

        left_owned = key_step(KeySlot.LEFT, left_identity, "key-left")
        if status == NORMAL:
            right_owned = key_step(
                KeySlot.RIGHT, right_identity, "key-right"
            )
        if status == NORMAL:
            ord_step()
        if right_owned is not None:
            drop_step(right_owned, "drop-key-right")
        if left_owned is not None and status != ABORT:
            drop_step(left_owned, "drop-key-left")

        if status != NORMAL:
            is_less = None
        result = AdapterResult(
            terminal_status=status,
            final_state=current,
            final_observable_element_state=interior,
            is_less=is_less,
            panic_origin=panic_origin,
            events=tuple(local_events),
        )
        self.observable_element_state = interior
        self.events.extend(local_events)
        self.invocations.append(result)
        return result

    def contract_admissible(self) -> bool:
        return self.boundary.contract_admissible()

    def contract_is_less(
        self, left_identity: int, right_identity: int
    ) -> bool:
        return self.boundary.contract_is_less(
            left_identity, right_identity
        )


class _KeySortEngine(private_sort._Engine):
    def __init__(
        self, sort_input: SortInput, adapter: KeyOrdDropAdapter
    ) -> None:
        super().__init__(sort_input, adapter)
        self.adapter = adapter

    def is_less(
        self, left_identity: int, right_identity: int, phase: str
    ) -> bool:
        before = self.callback_state
        result = self.adapter.transition(
            before, left_identity, right_identity
        )
        self.callback_state = result.final_state
        self.record(
            "ord-lt",
            phase,
            adapter_terminal_status=result.terminal_status,
            is_less=result.is_less,
            left_identity=left_identity,
            next_state=result.final_state,
            panicked=result.terminal_status != NORMAL,
            right_identity=right_identity,
            state=before,
        )
        if result.terminal_status == ABORT:
            raise private_sort._SourceAbort(
                f"{phase}:{result.panic_origin}"
            )
        if result.terminal_status == PANIC:
            raise private_sort._OrdPanic(phase)
        assert result.is_less is not None
        return result.is_less


def _execute_private(
    sort_input: SortInput, adapter: KeyOrdDropAdapter
) -> private_sort.Execution:
    engine = _KeySortEngine(sort_input, adapter)
    configuration = sort_input.configuration
    length = len(engine.sequence)
    try:
        if configuration.is_zst:
            engine.record("return", "sort:zst")
            return engine.finish(NORMAL)
        if length < 2:
            engine.record("return", "sort:length-less-than-two")
            return engine.finish(NORMAL)
        if configuration.use_configuration_heapsort:
            private_sort._heapsort(
                engine, 0, length, "sort:configuration-heapsort"
            )
            engine.record("return", "sort:configuration-heapsort")
            return engine.finish(NORMAL)
        if length <= private_sort.MAX_LEN_ALWAYS_INSERTION_SORT:
            private_sort._insertion_sort_shift_left(engine, 0, length, 1)
            engine.record("return", "sort:insertion")
            return engine.finish(NORMAL)
        run_length, was_reversed = private_sort._find_existing_run(engine)
        if run_length == length:
            if was_reversed:
                engine.sequence.reverse()
                engine.record("reverse", "ipnsort:full-descending-run")
            engine.record("return", "ipnsort:full-existing-run")
            return engine.finish(NORMAL)
        limit = 2 * ((length | 1).bit_length() - 1)
        engine.record(
            "quicksort-dispatch",
            "ipnsort",
            ancestor_pivot=False,
            imbalance_limit=limit,
            length=length,
        )
        private_sort._quicksort(engine, 0, length, None, limit)
        engine.record("return", "ipnsort:quicksort")
        return engine.finish(NORMAL)
    except private_sort._OrdPanic as panic:
        engine.record("panic", panic.phase)
        return engine.finish(PANIC, panic_phase=panic.phase)
    except private_sort._SourceAbort as abort:
        engine.record("abort", abort.phase)
        return engine.finish(ABORT, abort_phase=abort.phase)


@dataclass(frozen=True)
class FinalState:
    sequence: tuple[int, ...]
    callback_state: int
    observable_element_state: tuple[int, ...]
    panicked: bool
    aborted: bool
    terminal: bool
    f_drop_invoked: bool
    f_drop_completed: bool


@dataclass(frozen=True)
class Execution:
    state: FinalState
    terminal_status: str
    unit_returned: bool
    private_terminal_status: str
    panic_phase: str | None
    panic_origin: str | None
    abort_phase: str | None
    adapter_events: tuple[AdapterEvent, ...]
    private_steps: tuple[private_sort.DerivedStep, ...]


def execute(sort_input: SortInput, boundary: KeySortBoundary) -> Execution:
    adapter = KeyOrdDropAdapter(boundary)
    private = _execute_private(sort_input, adapter)
    status = private.terminal_status
    callback_state = private.state.callback_state
    interior = adapter.observable_element_state
    panic_phase = private.panic_phase
    abort_phase = private.abort_phase
    panic_origin = (
        adapter.invocations[-1].panic_origin
        if adapter.invocations
        and adapter.invocations[-1].terminal_status != NORMAL
        else None
    )
    f_drop_invoked = False
    f_drop_completed = False

    if status != ABORT:
        f_drop_invoked = True
        unwinding = status == PANIC
        observed = boundary.observe_f_drop(
            callback_state, interior, unwinding=unwinding
        )
        adapter.events.append(
            AdapterEvent(
                action="drop-f",
                invocation=len(adapter.invocations),
                state_before=callback_state,
                state_after=observed.next_state,
                observable_element_state_before=interior,
                observable_element_state_after=(
                    observed.next_observable_element_state
                ),
                panicked=observed.panicked,
                unwinding=unwinding,
            )
        )
        callback_state = observed.next_state
        interior = observed.next_observable_element_state
        f_drop_completed = not observed.panicked
        if observed.panicked:
            panic_origin = "drop-f"
            if unwinding:
                status = ABORT
                abort_phase = "drop-f-during-unwind"
            else:
                status = PANIC
                panic_phase = "drop-f-after-normal-sort"

    return Execution(
        state=FinalState(
            sequence=private.state.sequence,
            callback_state=callback_state,
            observable_element_state=interior,
            panicked=status == PANIC,
            aborted=status == ABORT,
            terminal=True,
            f_drop_invoked=f_drop_invoked,
            f_drop_completed=f_drop_completed,
        ),
        terminal_status=status,
        unit_returned=status == NORMAL,
        private_terminal_status=private.terminal_status,
        panic_phase=panic_phase,
        panic_origin=panic_origin,
        abort_phase=abort_phase,
        adapter_events=tuple(adapter.events),
        private_steps=private.derived_steps,
    )


def integer_total_order_boundary(**kwargs: Any) -> KeySortBoundary:
    return KeySortBoundary(**kwargs)


def mapped_key_boundary(
    key_by_identity: Mapping[int, int],
    *,
    rank_by_key: Mapping[int, int] | None = None,
    **kwargs: Any,
) -> KeySortBoundary:
    ordering_mode = (
        RANK_TOTAL_ORDER if rank_by_key is not None else KEY_TOTAL_ORDER
    )
    return KeySortBoundary(
        key_pairs=tuple(sorted(key_by_identity.items())),
        ordering_mode=ordering_mode,
        contract_ordering_mode=ordering_mode,
        rank_pairs=(
            ()
            if rank_by_key is None
            else tuple(sorted(rank_by_key.items()))
        ),
        **kwargs,
    )


def state_dependent_boundary(**kwargs: Any) -> KeySortBoundary:
    return KeySortBoundary(
        ordering_mode=STATE_PARITY_ORDER,
        contract_ordering_mode=None,
        **kwargs,
    )


def interior_state_dependent_boundary(**kwargs: Any) -> KeySortBoundary:
    return KeySortBoundary(
        ordering_mode=INTERIOR_PARITY_ORDER,
        contract_ordering_mode=None,
        **kwargs,
    )


def sequence_is_permutation(
    execution: Execution, before: tuple[int, ...]
) -> bool:
    return Counter(execution.state.sequence) == Counter(before)


def sequence_is_contract_sorted(
    execution: Execution, boundary: KeySortBoundary
) -> bool:
    if not boundary.contract_admissible():
        raise BoundaryViolation("contract projection is unavailable")
    return all(
        not boundary.contract_is_less(right, left)
        for left, right in zip(
            execution.state.sequence, execution.state.sequence[1:]
        )
    )


def exact_equivalent(first: Execution, second: Execution) -> bool:
    return (
        first.state == second.state
        and first.terminal_status == second.terminal_status
        and first.unit_returned == second.unit_returned
        and first.private_terminal_status == second.private_terminal_status
        and first.panic_phase == second.panic_phase
        and first.panic_origin == second.panic_origin
        and first.abort_phase == second.abort_phase
    )


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "model_id": MODEL_ID,
        "admitted_trust_site_ids": list(ADMITTED_TRUST_SITE_IDS),
        "replaced_trust_site_ids": list(REPLACED_TRUST_SITE_IDS),
        "context_only_trust_site_ids": list(CONTEXT_ONLY_TRUST_SITE_IDS),
        "pending_replacement_trust_site_ids": [],
        "boundary_narrower_than_target": True,
        "accepted_immutable_bindings": {
            "private_sort": private_sort.MODEL_ID,
            "key_ord_drop_lifecycle": accepted_key_lifecycle.MODEL_ID,
            "callback_state_semantics": (
                "target-081-operational-v1-rust-1.96-complete"
            ),
        },
        "shared_boundary_observations": [
            "total f(state,slot,element,interior) key/next-state/interior/panic",
            "total K::lt(state,left-owned-key,right-owned-key,interior) result/next-state/interior/panic",
            "total owned-K Drop(state,owned-key,unwinding,interior) next-state/interior/panic",
            "total owned-F Drop(state,unwinding,interior) next-state/interior/panic",
            "state-independent contract key and total Ord projection",
        ],
        "owned_key_identity": [
            "source-derived comparator invocation",
            "creation state",
            "left/right slot",
            "source element identity",
            "abstract key identity",
        ],
        "source_evaluation_order": [
            "f(left)",
            "f(right)",
            "K::lt(left-owned-key,right-owned-key)",
            "drop(right-owned-key)",
            "drop(left-owned-key)",
            "private-sort return or unwind restoration",
            "drop(F)",
        ],
        "externally_observable_state": (
            "complete callback scalar state and complete element-interior "
            "state after every key, Ord, K-Drop, and F-Drop transition"
        ),
        "source_derived_observations": [
            "realized callback schedule and operand order",
            "temporary identities and lifetimes",
            "pivots, partitions, swaps, writes, and restoration",
            "output sequence, terminal status, and final state",
            "execution trace",
        ],
        "prohibited_boundary_observations": [
            "realized schedule or prior calls",
            "temporary lifetime or destruction schedule",
            "pivot, partition, swap, or write choice",
            "selected output or permutation",
            "aggregate final state",
            "target execution trace",
            "precomputed terminal result",
        ],
        "trust_site_dispositions": {
            "TS-082-D001": "context-only-generated-contract-vocabulary",
            "TS-082-D002": "replaced-by-source-key-ord-drop-adapter",
            "TS-082-D003": "replaced-by-accepted-private-source-transitions",
            "TS-082-D004": (
                "admitted-total-key-ord-drop-and-state-observations"
            ),
            "TS-082-C001": "context-only-direct-call-identity",
            "TS-082-E001": "replaced-by-accepted-private-source-transitions",
        },
    }
