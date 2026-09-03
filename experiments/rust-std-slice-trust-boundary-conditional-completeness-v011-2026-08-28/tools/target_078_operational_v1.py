#!/usr/bin/env python3
"""Versioned source operational model for target 078."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any


TARGET = "core::slice::select_nth_unstable_by"
INPUT_ORDER = "78"
MODEL_ID = "target-078-operational-v1-rust-1.96-complete"
MODEL_VERSION = 1
SOURCE_MODEL_COMPLETE = True
ACTIVE_CONTRACT_SHA256 = (
    "8d197563a2e9735beef3c52ff46ea5d3dd44da47b48e3b199654cf3c667490d7"
)
ADMITTED_TRUST_SITE_IDS = ("TS-078-D004",)
ADAPTER_REPLACED_TRUST_SITE_IDS = ("TS-078-D002",)
ALGORITHM_REPLACED_TRUST_SITE_IDS = ("TS-078-D003", "TS-078-E001")
REPLACED_TRUST_SITE_IDS = (
    *ADAPTER_REPLACED_TRUST_SITE_IDS,
    *ALGORITHM_REPLACED_TRUST_SITE_IDS,
)
UNRESOLVED_TRUST_SITE_IDS: tuple[str, ...] = ()
CONTEXT_ONLY_TRUST_SITE_IDS = ("TS-078-D001", "TS-078-C001")

LESS = -1
EQUAL = 0
GREATER = 1
INSERTION_SORT_THRESHOLD = 16
INTROSELECT_LIMIT = 16
PSEUDO_MEDIAN_REC_THRESHOLD = 64
MAX_BRANCHLESS_PARTITION_SIZE = 96

MODELED_NORMAL = "modeled-normal"
MODELED_PANIC = "modeled-panic"

INTEGER_TOTAL_ORDER = "integer-total-order"
CONSTANT_LESS = "constant-less"
CONSTANT_EQUAL = "constant-equal"
CONSTANT_GREATER = "constant-greater"
STATE_PREFIX_LESS_THEN_GREATER = "state-prefix-less-then-greater"
INCREMENT_STATE = "increment"
IDENTITY_STATE = "identity"

ACTIVE_CONJUNCTS = (
    "final-concat",
    "left-length",
    "pivot-at-index",
    "right-length",
    "slice-permutation",
    "callback-partition",
)
SOURCE_PHASES = (
    "target comparator-to-Less adapter",
    "partition_at_index bounds, ZST, min, max, and cfg_select dispatch",
    "choose_pivot, median3_rec, and median3",
    "partition wrapper and all inst_partition branches",
    "partition_lomuto_branchless_cyclic and GapGuardRaw unwind",
    "partition_lomuto_branchless_simple",
    "partition_hoare_branchy_cyclic and GapGuard unwind",
    "ancestor-pivot reverse partition",
    "strictly shrinking introselect windows and sixteen-step limit",
    "median_of_medians fallback",
    "median_of_ninthers, ninther, and median_idx",
    "insertion_sort_shift_left, insert_tail, and CopyOnDrop unwind",
    "returned subslice construction",
)
MISSING_SOURCE_PHASES: tuple[str, ...] = ()


class BoundaryViolation(ValueError):
    """The supplied callback relation is not a valid total function."""


@dataclass(frozen=True, order=True)
class ObservationKey:
    state: int
    left_identity: int
    right_identity: int


@dataclass(frozen=True)
class ComparatorObservation:
    ordering: int
    next_state: int
    panicked: bool


@dataclass(frozen=True)
class ComparatorBoundary:
    """Total TS-078-D004 callback relations shared by all executions."""

    callback_identity: int
    initial_state: int
    ordering_mode: str
    next_state_mode: str
    contract_ordering_mode: str | None
    ordering_cutoff: int | None = None
    panic_states: frozenset[int] = frozenset()
    panic_keys: frozenset[ObservationKey] = frozenset()

    def __post_init__(self) -> None:
        if not isinstance(self.panic_states, frozenset):
            raise TypeError("panic_states must be a frozenset")
        if not isinstance(self.panic_keys, frozenset):
            raise TypeError("panic_keys must be a frozenset")
        if self.ordering_mode not in (
            INTEGER_TOTAL_ORDER,
            CONSTANT_LESS,
            CONSTANT_EQUAL,
            CONSTANT_GREATER,
            STATE_PREFIX_LESS_THEN_GREATER,
        ):
            raise ValueError("unknown immutable ordering mode")
        if self.next_state_mode not in (
            INCREMENT_STATE,
            IDENTITY_STATE,
        ):
            raise ValueError("unknown immutable next-state mode")
        if self.contract_ordering_mode not in (
            None,
            INTEGER_TOTAL_ORDER,
            CONSTANT_EQUAL,
        ):
            raise ValueError(
                "contract ordering must be a state-independent total preorder"
            )
        exact_contract_mode = {
            INTEGER_TOTAL_ORDER: INTEGER_TOTAL_ORDER,
            CONSTANT_EQUAL: CONSTANT_EQUAL,
        }.get(self.ordering_mode)
        if (
            self.contract_ordering_mode is not None
            and self.contract_ordering_mode != exact_contract_mode
        ):
            raise BoundaryViolation(
                "contract Ordering must exactly project implementation "
                "Ordering at every callback state"
            )
        if (
            self.ordering_mode == STATE_PREFIX_LESS_THEN_GREATER
        ) != (self.ordering_cutoff is not None):
            raise ValueError(
                "state-prefix ordering requires exactly one cutoff"
            )
        if self.ordering_cutoff is not None and not isinstance(
            self.ordering_cutoff, int
        ):
            raise TypeError("ordering cutoff must be an integer")

    @staticmethod
    def _validate_observation(
        observation: ComparatorObservation,
    ) -> None:
        if observation.ordering not in (LESS, EQUAL, GREATER):
            raise BoundaryViolation(
                "callback ordering must be Less, Equal, or Greater"
            )
        if not isinstance(observation.panicked, bool):
            raise BoundaryViolation("callback panic observation must be bool")

    @staticmethod
    def _mode_ordering(
        mode: str, left_identity: int, right_identity: int
    ) -> int:
        if mode == INTEGER_TOTAL_ORDER:
            return (
                LESS
                if left_identity < right_identity
                else GREATER
                if left_identity > right_identity
                else EQUAL
            )
        if mode == CONSTANT_LESS:
            return LESS
        if mode == CONSTANT_EQUAL:
            return EQUAL
        if mode == CONSTANT_GREATER:
            return GREATER
        raise BoundaryViolation(f"ordering mode is not pair-based: {mode}")

    def observe(
        self, state: int, left_identity: int, right_identity: int
    ) -> ComparatorObservation:
        key = ObservationKey(state, left_identity, right_identity)
        if self.ordering_mode == STATE_PREFIX_LESS_THEN_GREATER:
            assert self.ordering_cutoff is not None
            ordering = LESS if state < self.ordering_cutoff else GREATER
        else:
            ordering = self._mode_ordering(
                self.ordering_mode, left_identity, right_identity
            )
        next_state = (
            state + 1
            if self.next_state_mode == INCREMENT_STATE
            else state
        )
        observation = ComparatorObservation(
            ordering=ordering,
            next_state=next_state,
            panicked=state in self.panic_states or key in self.panic_keys,
        )
        self._validate_observation(observation)
        return observation

    def contract_ordering(
        self, left_identity: int, right_identity: int
    ) -> int:
        """Project the exact state-independent active-contract Ordering."""

        if self.contract_ordering_mode is None:
            raise BoundaryViolation(
                "callback relation has no admissible contract Ordering"
            )
        return self._mode_ordering(
            self.contract_ordering_mode,
            left_identity,
            right_identity,
        )

    def contract_admissible(self) -> bool:
        return self.contract_ordering_mode is not None


@dataclass(frozen=True)
class SourceConfiguration:
    optimize_for_size: bool = False
    element_size: int = 8

    def __post_init__(self) -> None:
        if self.element_size < 0:
            raise ValueError("element_size must be nonnegative")


@dataclass(frozen=True)
class SelectionInput:
    initial_sequence: tuple[int, ...]
    index: int
    allocation: int
    borrow: int
    is_zst: bool
    configuration: SourceConfiguration = SourceConfiguration()


@dataclass(frozen=True)
class Reference:
    allocation: int
    parent_borrow: int
    start: int
    span: int
    projection_kind: str


@dataclass(frozen=True)
class SelectionOutput:
    left: Reference
    pivot: Reference
    right: Reference
    pivot_identity: int


@dataclass(frozen=True)
class FinalState:
    sequence: tuple[int, ...]
    allocation: int
    borrow: int
    length: int
    callback_state: int
    panicked: bool
    terminal: bool


@dataclass(frozen=True)
class DerivedEvent:
    """A source-derived event; it is evidence, never part of Boundary_T."""

    kind: str
    phase: str
    details: tuple[tuple[str, Any], ...]

    def detail(self, name: str) -> Any:
        return dict(self.details)[name]


@dataclass(frozen=True)
class Execution:
    coverage_status: str
    branch: str
    output: SelectionOutput | None
    final_state: FinalState
    derived_events: tuple[DerivedEvent, ...]
    panic_phase: str | None = None
    model_gap_phase: str | None = None


class _CallbackPanic(RuntimeError):
    def __init__(self, phase: str) -> None:
        super().__init__(phase)
        self.phase = phase


class _Engine:
    def __init__(
        self, selection_input: SelectionInput, boundary: ComparatorBoundary
    ) -> None:
        self.selection_input = selection_input
        self.boundary = boundary
        self.sequence = list(selection_input.initial_sequence)
        self.callback_state = boundary.initial_state
        self.events: list[DerivedEvent] = []

    def record(self, kind: str, phase: str, **details: Any) -> None:
        self.events.append(
            DerivedEvent(kind, phase, tuple(sorted(details.items())))
        )

    def is_less(
        self, left_identity: int, right_identity: int, phase: str
    ) -> bool:
        state_before = self.callback_state
        observation = self.boundary.observe(
            state_before, left_identity, right_identity
        )
        self.callback_state = observation.next_state
        self.record(
            "callback",
            phase,
            left_identity=left_identity,
            next_state=observation.next_state,
            ordering=observation.ordering,
            panicked=observation.panicked,
            right_identity=right_identity,
            state=state_before,
        )
        if observation.panicked:
            raise _CallbackPanic(phase)
        return observation.ordering == LESS

    def swap(self, left: int, right: int, phase: str) -> None:
        self.sequence[left], self.sequence[right] = (
            self.sequence[right],
            self.sequence[left],
        )
        self.record(
            "swap",
            phase,
            left_position=left,
            right_position=right,
        )

    def final_state(self, *, panicked: bool) -> FinalState:
        selection_input = self.selection_input
        return FinalState(
            sequence=tuple(self.sequence),
            allocation=selection_input.allocation,
            borrow=selection_input.borrow,
            length=len(self.sequence),
            callback_state=self.callback_state,
            panicked=panicked,
            terminal=True,
        )


def integer_total_order_boundary(
    *,
    callback_identity: int = 61,
    initial_state: int = 0,
    panic_states: frozenset[int] = frozenset(),
    panic_keys: frozenset[ObservationKey] = frozenset(),
) -> ComparatorBoundary:
    """Construct an immutable integer comparator relation."""

    return ComparatorBoundary(
        callback_identity=callback_identity,
        initial_state=initial_state,
        ordering_mode=INTEGER_TOTAL_ORDER,
        next_state_mode=INCREMENT_STATE,
        contract_ordering_mode=INTEGER_TOTAL_ORDER,
        panic_states=panic_states,
        panic_keys=panic_keys,
    )


def constant_order_boundary(
    ordering: int,
    *,
    callback_identity: int = 61,
    initial_state: int = 0,
    panic_states: frozenset[int] = frozenset(),
) -> ComparatorBoundary:
    modes = {
        LESS: CONSTANT_LESS,
        EQUAL: CONSTANT_EQUAL,
        GREATER: CONSTANT_GREATER,
    }
    if ordering not in modes:
        raise BoundaryViolation("constant ordering must be valid")
    return ComparatorBoundary(
        callback_identity=callback_identity,
        initial_state=initial_state,
        ordering_mode=modes[ordering],
        next_state_mode=INCREMENT_STATE,
        contract_ordering_mode=(
            CONSTANT_EQUAL if ordering == EQUAL else None
        ),
        panic_states=panic_states,
    )


def state_prefix_order_boundary(
    *,
    ordering_cutoff: int,
    callback_identity: int = 61,
    initial_state: int = 0,
    panic_states: frozenset[int] = frozenset(),
) -> ComparatorBoundary:
    """Construct a total state-indexed relation for replay regressions."""

    return ComparatorBoundary(
        callback_identity=callback_identity,
        initial_state=initial_state,
        ordering_mode=STATE_PREFIX_LESS_THEN_GREATER,
        next_state_mode=INCREMENT_STATE,
        contract_ordering_mode=None,
        ordering_cutoff=ordering_cutoff,
        panic_states=panic_states,
    )


def requires_t(selection_input: SelectionInput) -> bool:
    return (
        0 <= selection_input.index < len(selection_input.initial_sequence)
    )


def _insert_tail(
    engine: _Engine, begin: int, tail: int, phase: str
) -> None:
    temporary = engine.sequence[tail]
    if not engine.is_less(
        temporary,
        engine.sequence[tail - 1],
        f"{phase}:initial-compare",
    ):
        engine.record("insert-tail-no-shift", phase, tail=tail)
        return

    sift = tail - 1
    gap = tail
    try:
        while True:
            engine.sequence[gap] = engine.sequence[sift]
            engine.record(
                "insert-tail-shift",
                phase,
                destination=gap,
                source=sift,
                tail=tail,
            )
            gap = sift
            if sift == begin:
                break
            sift -= 1
            if not engine.is_less(
                temporary,
                engine.sequence[sift],
                f"{phase}:sift-compare",
            ):
                break
    except _CallbackPanic:
        engine.sequence[gap] = temporary
        engine.record(
            "copy-on-drop-restore",
            phase,
            destination=gap,
            panicked=True,
            tail=tail,
        )
        raise

    engine.sequence[gap] = temporary
    engine.record(
        "copy-on-drop-restore",
        phase,
        destination=gap,
        panicked=False,
        tail=tail,
    )


def _insertion_sort_shift_left(
    engine: _Engine, start: int, end: int, offset: int
) -> None:
    length = end - start
    if offset == 0 or offset > length:
        raise AssertionError("source insertion-sort precondition violated")
    for tail in range(start + offset, end):
        engine.record(
            "insertion-tail",
            "insertion-sort-shift-left",
            relative_tail=tail - start,
            tail=tail,
            window_end=end,
            window_start=start,
        )
        _insert_tail(
            engine,
            start,
            tail,
            f"insert-tail[{start}:{end}:{tail - start}]",
        )


def _extreme_scan(
    engine: _Engine,
    start: int,
    end: int,
    *,
    find_min: bool,
    phase: str,
) -> int:
    accumulator = start
    for candidate in range(start + 1, end):
        left = (
            engine.sequence[candidate]
            if find_min
            else engine.sequence[accumulator]
        )
        right = (
            engine.sequence[accumulator]
            if find_min
            else engine.sequence[candidate]
        )
        if engine.is_less(left, right, phase):
            accumulator = candidate
        engine.record(
            "extreme-scan-step",
            phase,
            accumulator=accumulator,
            candidate=candidate,
            window_end=end,
            window_start=start,
        )
    return accumulator


def _median3(
    engine: _Engine, a: int, b: int, c: int, phase: str
) -> int:
    x = engine.is_less(
        engine.sequence[a], engine.sequence[b], f"{phase}:a-b"
    )
    y = engine.is_less(
        engine.sequence[a], engine.sequence[c], f"{phase}:a-c"
    )
    if x == y:
        z = engine.is_less(
            engine.sequence[b], engine.sequence[c], f"{phase}:b-c"
        )
        result = c if z ^ x else b
        branch = "outer"
    else:
        result = a
        branch = "a"
    engine.record(
        "median3",
        phase,
        a=a,
        b=b,
        branch=branch,
        c=c,
        result=result,
    )
    return result


def _median3_rec(
    engine: _Engine,
    a: int,
    b: int,
    c: int,
    n: int,
    phase: str,
) -> int:
    engine.record(
        "median3-rec-enter", phase, a=a, b=b, c=c, region_length=n
    )
    if n * 8 >= PSEUDO_MEDIAN_REC_THRESHOLD:
        n8 = n // 8
        a = _median3_rec(
            engine,
            a,
            a + n8 * 4,
            a + n8 * 7,
            n8,
            f"{phase}:a",
        )
        b = _median3_rec(
            engine,
            b,
            b + n8 * 4,
            b + n8 * 7,
            n8,
            f"{phase}:b",
        )
        c = _median3_rec(
            engine,
            c,
            c + n8 * 4,
            c + n8 * 7,
            n8,
            f"{phase}:c",
        )
    return _median3(engine, a, b, c, f"{phase}:median3")


def _choose_pivot(engine: _Engine, start: int, end: int) -> int:
    length = end - start
    if length < 8:
        raise AssertionError("choose_pivot source precondition violated")
    len_div_8 = length // 8
    a = start
    b = start + len_div_8 * 4
    c = start + len_div_8 * 7
    if length < PSEUDO_MEDIAN_REC_THRESHOLD:
        result = _median3(engine, a, b, c, "choose-pivot:median3")
        branch = "median3"
    else:
        result = _median3_rec(
            engine,
            a,
            b,
            c,
            len_div_8,
            "choose-pivot:median3-rec",
        )
        branch = "median3-rec"
    engine.record(
        "choose-pivot",
        "choose-pivot",
        branch=branch,
        pivot_position=result,
        window_end=end,
        window_start=start,
    )
    return result - start


def _partition_predicate(
    engine: _Engine,
    left_identity: int,
    right_identity: int,
    phase: str,
    *,
    reverse: bool,
) -> bool:
    if reverse:
        result = not engine.is_less(
            right_identity, left_identity, f"{phase}:reverse-less"
        )
    else:
        result = engine.is_less(left_identity, right_identity, phase)
    engine.record(
        "partition-predicate",
        phase,
        left_identity=left_identity,
        result=result,
        reverse=reverse,
        right_identity=right_identity,
    )
    return result


def _partition_lomuto_branchless_simple(
    engine: _Engine,
    start: int,
    end: int,
    pivot_identity: int,
    *,
    reverse: bool,
) -> int:
    left = start
    engine.record(
        "partition-implementation",
        "partition-lomuto-branchless-simple",
        implementation="lomuto-simple",
        window_end=end,
        window_start=start,
    )
    for right in range(start, end):
        right_is_lt = _partition_predicate(
            engine,
            engine.sequence[right],
            pivot_identity,
            "partition-lomuto-simple:compare",
            reverse=reverse,
        )
        engine.swap(left, right, "partition-lomuto-simple:swap")
        engine.record(
            "partition-step",
            "partition-lomuto-branchless-simple",
            left=left,
            right=right,
            right_is_lt=right_is_lt,
        )
        left += int(right_is_lt)
    return left - start


def _partition_lomuto_branchless_cyclic(
    engine: _Engine,
    start: int,
    end: int,
    pivot_identity: int,
    *,
    reverse: bool,
) -> int:
    length = end - start
    if length == 0:
        return 0
    unroll_len = (
        2
        if engine.selection_input.configuration.element_size <= 16
        else 1
    )
    engine.record(
        "partition-implementation",
        "partition-lomuto-branchless-cyclic",
        implementation="lomuto-cyclic",
        unroll_len=unroll_len,
        window_end=end,
        window_start=start,
    )
    gap_value = engine.sequence[start]
    gap_position = start
    num_lt = 0
    try:
        for right in range(start + 1, end):
            right_value = engine.sequence[right]
            right_is_lt = _partition_predicate(
                engine,
                right_value,
                pivot_identity,
                "partition-lomuto-cyclic:compare",
                reverse=reverse,
            )
            left = start + num_lt
            engine.sequence[gap_position] = engine.sequence[left]
            engine.sequence[left] = right_value
            engine.record(
                "partition-cycle",
                "partition-lomuto-branchless-cyclic",
                gap_destination=gap_position,
                left=left,
                right=right,
                right_is_lt=right_is_lt,
            )
            gap_position = right
            num_lt += int(right_is_lt)

        right_is_lt = _partition_predicate(
            engine,
            gap_value,
            pivot_identity,
            "partition-lomuto-cyclic:cleanup-compare",
            reverse=reverse,
        )
        left = start + num_lt
        engine.sequence[gap_position] = engine.sequence[left]
        engine.sequence[left] = gap_value
        num_lt += int(right_is_lt)
        engine.record(
            "partition-cycle-cleanup",
            "partition-lomuto-branchless-cyclic",
            consumed_guard=True,
            gap_destination=gap_position,
            left=left,
            right_is_lt=right_is_lt,
        )
        return num_lt
    except _CallbackPanic:
        engine.sequence[gap_position] = gap_value
        engine.record(
            "gap-guard-restore",
            "partition-lomuto-branchless-cyclic",
            destination=gap_position,
            panicked=True,
        )
        raise


def _partition_hoare_branchy_cyclic(
    engine: _Engine,
    start: int,
    end: int,
    pivot_identity: int,
    *,
    reverse: bool,
) -> int:
    if start == end:
        return 0
    engine.record(
        "partition-implementation",
        "partition-hoare-branchy-cyclic",
        implementation="hoare-cyclic",
        window_end=end,
        window_start=start,
    )
    left = start
    right = end
    gap_value: int | None = None
    gap_position: int | None = None
    try:
        while True:
            while left < right and _partition_predicate(
                engine,
                engine.sequence[left],
                pivot_identity,
                "partition-hoare:left-scan",
                reverse=reverse,
            ):
                left += 1

            while True:
                right -= 1
                if left >= right or _partition_predicate(
                    engine,
                    engine.sequence[right],
                    pivot_identity,
                    "partition-hoare:right-scan",
                    reverse=reverse,
                ):
                    break

            if left >= right:
                break

            first_pair = gap_value is None
            if first_pair:
                gap_value = engine.sequence[left]
            else:
                assert gap_position is not None
                engine.sequence[gap_position] = engine.sequence[left]
            gap_position = right
            engine.sequence[left] = engine.sequence[right]
            engine.record(
                "partition-cycle",
                "partition-hoare-branchy-cyclic",
                first_pair=first_pair,
                gap_destination=gap_position,
                left=left,
                right=right,
            )
            left += 1
    except _CallbackPanic:
        if gap_value is not None:
            assert gap_position is not None
            engine.sequence[gap_position] = gap_value
            engine.record(
                "gap-guard-restore",
                "partition-hoare-branchy-cyclic",
                destination=gap_position,
                panicked=True,
            )
        raise

    if gap_value is not None:
        assert gap_position is not None
        engine.sequence[gap_position] = gap_value
        engine.record(
            "gap-guard-restore",
            "partition-hoare-branchy-cyclic",
            destination=gap_position,
            panicked=False,
        )
    return left - start


def _partition(
    engine: _Engine,
    start: int,
    end: int,
    pivot_position: int,
    *,
    reverse: bool = False,
) -> int:
    length = end - start
    if length == 0 or not 0 <= pivot_position < length:
        raise AssertionError("partition source precondition violated")
    pivot_global = start + pivot_position
    engine.swap(start, pivot_global, "partition:pivot-to-front")
    pivot_identity = engine.sequence[start]
    lower_start = start + 1
    configuration = engine.selection_input.configuration
    if configuration.element_size <= MAX_BRANCHLESS_PARTITION_SIZE:
        if configuration.optimize_for_size:
            num_lt = _partition_lomuto_branchless_simple(
                engine,
                lower_start,
                end,
                pivot_identity,
                reverse=reverse,
            )
        else:
            num_lt = _partition_lomuto_branchless_cyclic(
                engine,
                lower_start,
                end,
                pivot_identity,
                reverse=reverse,
            )
    else:
        num_lt = _partition_hoare_branchy_cyclic(
            engine,
            lower_start,
            end,
            pivot_identity,
            reverse=reverse,
        )
    engine.swap(start, start + num_lt, "partition:pivot-to-middle")
    engine.record(
        "partition-result",
        "partition",
        mid=num_lt,
        reverse=reverse,
        window_end=end,
        window_start=start,
    )
    return num_lt


def _median_idx(
    engine: _Engine, a: int, b: int, c: int, phase: str
) -> int:
    if engine.is_less(
        engine.sequence[c], engine.sequence[a], f"{phase}:c-a"
    ):
        a, c = c, a
    if engine.is_less(
        engine.sequence[c], engine.sequence[b], f"{phase}:c-b"
    ):
        result = c
    elif engine.is_less(
        engine.sequence[b], engine.sequence[a], f"{phase}:b-a"
    ):
        result = a
    else:
        result = b
    engine.record(
        "median-idx",
        phase,
        a=a,
        b=b,
        c=c,
        result=result,
    )
    return result


def _ninther(
    engine: _Engine,
    a: int,
    b: int,
    c: int,
    d: int,
    e: int,
    f: int,
    g: int,
    h: int,
    i: int,
    phase: str,
) -> None:
    b = _median_idx(engine, a, b, c, f"{phase}:left-median")
    h = _median_idx(engine, g, h, i, f"{phase}:right-median")
    if engine.is_less(
        engine.sequence[h], engine.sequence[b], f"{phase}:h-b"
    ):
        b, h = h, b
    if engine.is_less(
        engine.sequence[f], engine.sequence[d], f"{phase}:f-d"
    ):
        d, f = f, d
    if engine.is_less(
        engine.sequence[e], engine.sequence[d], f"{phase}:e-d"
    ):
        branch = "e-less-d"
    elif engine.is_less(
        engine.sequence[f], engine.sequence[e], f"{phase}:f-e"
    ):
        d = f
        branch = "f-less-e"
    else:
        if engine.is_less(
            engine.sequence[e], engine.sequence[b], f"{phase}:e-b"
        ):
            engine.swap(e, b, f"{phase}:swap-e-b")
            branch = "swap-e-b"
        elif engine.is_less(
            engine.sequence[h], engine.sequence[e], f"{phase}:h-e"
        ):
            engine.swap(e, h, f"{phase}:swap-e-h")
            branch = "swap-e-h"
        else:
            branch = "already-median"
        engine.record("ninther", phase, branch=branch, destination=e)
        return

    if engine.is_less(
        engine.sequence[d], engine.sequence[b], f"{phase}:d-b"
    ):
        d = b
    elif engine.is_less(
        engine.sequence[h], engine.sequence[d], f"{phase}:h-d"
    ):
        d = h
    engine.swap(d, e, f"{phase}:swap-d-e")
    engine.record("ninther", phase, branch=branch, destination=e)


def median_of_ninthers_geometry(
    length: int,
) -> tuple[int, int, int, int, str]:
    """Return the source's frac, pivot, lo, gap, and selected size branch."""

    if length <= INSERTION_SORT_THRESHOLD:
        raise ValueError("median_of_ninthers requires a length above 16")
    if length <= 1024:
        frac = length // 12
        frac_branch = "len/12"
    elif length <= 128 * 1024:
        frac = length // 64
        frac_branch = "len/64"
    else:
        frac = length // 1024
        frac_branch = "len/1024"
    pivot = frac // 2
    lo = length // 2 - pivot
    gap = (length - 9 * frac) // 4
    return frac, pivot, lo, gap, frac_branch


def _median_of_ninthers(
    engine: _Engine, start: int, end: int
) -> int:
    length = end - start
    frac, pivot, lo, gap, frac_branch = median_of_ninthers_geometry(
        length
    )
    hi = frac + lo
    a = lo - 4 * frac - gap
    b = hi + gap
    engine.record(
        "median-of-ninthers",
        "median-of-ninthers",
        frac=frac,
        frac_branch=frac_branch,
        gap=gap,
        hi=start + hi,
        lo=start + lo,
        pivot=pivot,
        window_end=end,
        window_start=start,
    )
    for local_i in range(lo, hi):
        _ninther(
            engine,
            start + a,
            start + local_i - frac,
            start + b,
            start + a + 1,
            start + local_i,
            start + b + 1,
            start + a + 2,
            start + local_i + frac,
            start + b + 2,
            f"ninther[{start}:{end}:{local_i - lo}]",
        )
        a += 3
        b += 3

    _median_of_medians(
        engine,
        start + lo,
        start + lo + frac,
        pivot,
        phase="median-of-ninthers:recursive-median",
    )
    return _partition(engine, start, end, lo + pivot)


def _median_of_medians(
    engine: _Engine,
    start: int,
    end: int,
    k: int,
    *,
    phase: str,
) -> str:
    if not 0 <= k < end - start:
        raise AssertionError("median_of_medians source precondition violated")
    while True:
        length = end - start
        engine.record(
            "fallback-window",
            phase,
            index=k,
            window_end=end,
            window_start=start,
        )
        if length <= INSERTION_SORT_THRESHOLD:
            if length >= 2:
                _insertion_sort_shift_left(engine, start, end, 1)
            return "fallback-small-sort"
        if k == length - 1:
            winner = _extreme_scan(
                engine,
                start,
                end,
                find_min=False,
                phase="fallback-max-index",
            )
            engine.swap(winner, start + k, "fallback-max-final-swap")
            return "fallback-max"
        if k == 0:
            winner = _extreme_scan(
                engine,
                start,
                end,
                find_min=True,
                phase="fallback-min-index",
            )
            engine.swap(winner, start, "fallback-min-final-swap")
            return "fallback-min"

        pivot = _median_of_ninthers(engine, start, end)
        if pivot == k:
            return "fallback-hit"
        if pivot > k:
            previous_end = end
            end = start + pivot
            engine.record(
                "fallback-narrow-left",
                phase,
                new_end=end,
                previous_end=previous_end,
                window_start=start,
            )
        else:
            previous_start = start
            start += pivot + 1
            k -= pivot + 1
            engine.record(
                "fallback-narrow-right",
                phase,
                new_index=k,
                new_start=start,
                previous_start=previous_start,
                window_end=end,
            )


def _partition_at_index_loop(
    engine: _Engine, target_index: int
) -> str:
    start = 0
    end = len(engine.sequence)
    index = target_index
    ancestor_pivot: int | None = None
    limit = INTROSELECT_LIMIT
    while True:
        length = end - start
        engine.record(
            "introselect-window",
            "partition-at-index-loop",
            ancestor_present=ancestor_pivot is not None,
            index=index,
            limit=limit,
            window_end=end,
            window_start=start,
        )
        if start + index != target_index:
            raise AssertionError("introselect index/window invariant failed")
        if length <= INSERTION_SORT_THRESHOLD:
            if length >= 2:
                _insertion_sort_shift_left(engine, start, end, 1)
            return "insertion-sort"
        if limit == 0:
            _median_of_medians(
                engine,
                start,
                end,
                index,
                phase="introselect-fallback",
            )
            return "introselect-fallback"
        limit -= 1

        pivot_position = _choose_pivot(engine, start, end)
        if ancestor_pivot is not None:
            pivot_identity = engine.sequence[start + pivot_position]
            if not engine.is_less(
                ancestor_pivot,
                pivot_identity,
                "ancestor-pivot:compare",
            ):
                num_lt = _partition(
                    engine,
                    start,
                    end,
                    pivot_position,
                    reverse=True,
                )
                mid = num_lt + 1
                engine.record(
                    "ancestor-pivot-partition",
                    "partition-at-index-loop",
                    index=index,
                    mid=mid,
                    window_end=end,
                    window_start=start,
                )
                if mid > index:
                    return "ancestor-pivot-return"
                previous_start = start
                start += mid
                index -= mid
                ancestor_pivot = None
                engine.record(
                    "ancestor-narrow-right",
                    "partition-at-index-loop",
                    new_index=index,
                    new_start=start,
                    previous_start=previous_start,
                    window_end=end,
                )
                continue

        mid = _partition(
            engine, start, end, pivot_position, reverse=False
        )
        if mid < index:
            pivot_global = start + mid
            ancestor_pivot = engine.sequence[pivot_global]
            previous_start = start
            start = pivot_global + 1
            index -= mid + 1
            engine.record(
                "introselect-narrow-right",
                "partition-at-index-loop",
                new_index=index,
                new_start=start,
                previous_start=previous_start,
                window_end=end,
            )
        elif mid > index:
            previous_end = end
            end = start + mid
            engine.record(
                "introselect-narrow-left",
                "partition-at-index-loop",
                new_end=end,
                previous_end=previous_end,
                window_start=start,
            )
        else:
            return "introselect-pivot-hit"


def _output(
    selection_input: SelectionInput, sequence: list[int]
) -> SelectionOutput:
    index = selection_input.index
    length = len(sequence)
    return SelectionOutput(
        left=Reference(
            selection_input.allocation,
            selection_input.borrow,
            0,
            index,
            "left-subslice",
        ),
        pivot=Reference(
            selection_input.allocation,
            selection_input.borrow,
            index,
            1,
            "pivot-element",
        ),
        right=Reference(
            selection_input.allocation,
            selection_input.borrow,
            index + 1,
            length - index - 1,
            "right-subslice",
        ),
        pivot_identity=sequence[index],
    )


def execute(
    selection_input: SelectionInput, boundary: ComparatorBoundary
) -> Execution:
    """Execute all reachable Rust 1.96 source and configuration branches."""

    engine = _Engine(selection_input, boundary)
    length = len(engine.sequence)
    index = selection_input.index
    branch = "bounds"

    try:
        if not requires_t(selection_input):
            engine.record(
                "branch",
                "partition-at-index",
                branch="bounds-panic",
                index=index,
                length=length,
            )
            return Execution(
                coverage_status=MODELED_PANIC,
                branch="bounds-panic",
                output=None,
                final_state=engine.final_state(panicked=True),
                derived_events=tuple(engine.events),
                panic_phase="bounds",
            )

        if selection_input.is_zst:
            branch = "zst"
            engine.record("branch", "partition-at-index", branch=branch)
        elif index == length - 1:
            branch = "max-scan"
            engine.record("branch", "partition-at-index", branch=branch)
            winner = _extreme_scan(
                engine,
                0,
                length,
                find_min=False,
                phase="max-index",
            )
            engine.swap(winner, index, "max-index-final-swap")
        elif index == 0:
            branch = "min-scan"
            engine.record("branch", "partition-at-index", branch=branch)
            winner = _extreme_scan(
                engine,
                0,
                length,
                find_min=True,
                phase="min-index",
            )
            engine.swap(winner, index, "min-index-final-swap")
        elif selection_input.configuration.optimize_for_size:
            branch = "optimize-for-size"
            engine.record(
                "branch",
                "partition-at-index",
                branch="median-of-medians",
            )
            _median_of_medians(
                engine,
                0,
                length,
                index,
                phase="optimize-for-size",
            )
        else:
            branch = "introselect"
            engine.record(
                "branch",
                "partition-at-index",
                branch="partition-at-index-loop",
            )
            terminal = _partition_at_index_loop(engine, index)
            if terminal == "insertion-sort":
                branch = terminal
            engine.record(
                "introselect-return",
                "partition-at-index-loop",
                terminal=terminal,
            )
    except _CallbackPanic as panic:
        return Execution(
            coverage_status=MODELED_PANIC,
            branch=branch,
            output=None,
            final_state=engine.final_state(panicked=True),
            derived_events=tuple(engine.events),
            panic_phase=panic.phase,
        )

    return Execution(
        coverage_status=MODELED_NORMAL,
        branch=branch,
        output=_output(selection_input, engine.sequence),
        final_state=engine.final_state(panicked=False),
        derived_events=tuple(engine.events),
    )


def _contract_leq(
    boundary: ComparatorBoundary, left_identity: int, right_identity: int
) -> bool:
    return (
        boundary.contract_ordering(left_identity, right_identity) <= EQUAL
    )


def active_contract_conjuncts(
    selection_input: SelectionInput,
    boundary: ComparatorBoundary,
    execution: Execution,
) -> dict[str, bool]:
    """Evaluate the exact six generated normal-return conjuncts."""

    output = execution.output
    state = execution.final_state
    if (
        execution.coverage_status != MODELED_NORMAL
        or output is None
        or state.panicked
    ):
        return {name: False for name in ACTIVE_CONJUNCTS}

    final = state.sequence
    index = selection_input.index
    left = final[output.left.start : output.left.start + output.left.span]
    pivot_values = final[
        output.pivot.start : output.pivot.start + output.pivot.span
    ]
    right = final[
        output.right.start : output.right.start + output.right.span
    ]
    pivot_identity = output.pivot_identity
    return {
        "final-concat": left + pivot_values + right == final,
        "left-length": output.left.span == index,
        "pivot-at-index": (
            len(pivot_values) == 1
            and pivot_values[0] == pivot_identity
            and pivot_identity == final[index]
        ),
        "right-length": (
            output.right.span
            == len(selection_input.initial_sequence) - index - 1
        ),
        "slice-permutation": (
            Counter(selection_input.initial_sequence) == Counter(final)
        ),
        "callback-partition": (
            all(
                _contract_leq(boundary, identity, pivot_identity)
                for identity in left
            )
            and all(
                _contract_leq(boundary, pivot_identity, identity)
                for identity in right
            )
        ),
    }


def active_contract_holds(
    selection_input: SelectionInput,
    boundary: ComparatorBoundary,
    execution: Execution,
) -> bool:
    return all(
        active_contract_conjuncts(
            selection_input, boundary, execution
        ).values()
    )


def exact_equivalent(first: Execution, second: Execution) -> bool:
    """Exact principal-return and final-state equality; traces are internal."""

    return (
        first.coverage_status == second.coverage_status
        and first.output == second.output
        and first.final_state == second.final_state
    )


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 2,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "source_model_complete": SOURCE_MODEL_COMPLETE,
        "admitted_trust_site_ids": list(ADMITTED_TRUST_SITE_IDS),
        "adapter_replaced_trust_site_ids": list(
            ADAPTER_REPLACED_TRUST_SITE_IDS
        ),
        "algorithm_replaced_trust_site_ids": list(
            ALGORITHM_REPLACED_TRUST_SITE_IDS
        ),
        "unresolved_trust_site_ids": list(UNRESOLVED_TRUST_SITE_IDS),
        "shared_boundary_observations": [
            {
                "name": "callback_identity",
                "role": "FnMut object identity",
            },
            {
                "name": "initial_callback_state",
                "role": "callback-visible state before target entry",
            },
            {
                "name": "immutable_ordering(state,left_identity,right_identity)",
                "role": "total functional implementation Ordering observation",
            },
            {
                "name": "immutable_next_state(state,left_identity,right_identity)",
                "role": "total functional callback-state transition",
            },
            {
                "name": "immutable_panic(state,left_identity,right_identity)",
                "role": "total functional callback panic observation",
            },
            {
                "name": "contract_ordering(left_identity,right_identity)",
                "role": (
                    "state-independent total-preorder Ordering projection "
                    "equal to implementation Ordering at every state, with "
                    "reflexive, dual, total, and transitive laws"
                ),
            },
        ],
        "immutability_enforcement": (
            "Executions retain only total declarative immutable relations; "
            "finite trace-shaped callback tables and live callables are "
            "not representable."
        ),
        "internally_derived": [
            "callback invocations",
            "branch choices",
            "element shifts and swaps",
            "guard restoration",
            "references and post-sequence",
            "post-callback-visible state",
        ],
        "covered_source_phases": list(SOURCE_PHASES),
        "missing_source_phases": [],
        "classification_boundary_requirement": (
            "contract_admissible() rejects state-dependent or otherwise "
            "inadmissible implementation Ordering relations"
        ),
        "classification_eligible": True,
        "equivalence": "exact-principal-return-and-final-state",
    }
