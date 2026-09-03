#!/usr/bin/env python3
"""Source-exact Rust 1.96 operational model for target 080."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


TARGET = "core::slice::sort_unstable"
INPUT_ORDER = "80"
MODEL_ID = "target-080-operational-v1-rust-1.96-complete"
MODEL_VERSION = 1
ACTIVE_CONTRACT_SHA256 = (
    "877e37bea31dc31a92b85282f1d2f633c20aeb5391a5f1f02821cbfa0a09dd4b"
)

ADMITTED_TRUST_SITE_IDS = ("TS-080-D003",)
REPLACED_TRUST_SITE_IDS = ("TS-080-D002", "TS-080-E001")
PENDING_REPLACEMENT_TRUST_SITE_IDS: tuple[str, ...] = ()
SOURCE_MODEL_COMPLETE = True
CLASSIFICATION_ELIGIBLE = True

MAX_LEN_ALWAYS_INSERTION_SORT = 20
SMALL_SORT_FALLBACK_THRESHOLD = 16
SMALL_SORT_GENERAL_THRESHOLD = 32
SMALL_SORT_GENERAL_SCRATCH_LEN = 48
SMALL_SORT_NETWORK_THRESHOLD = 32
SMALL_SORT_NETWORK_SCRATCH_LEN = 32
MAX_STACK_ARRAY_SIZE = 4096
PSEUDO_MEDIAN_REC_THRESHOLD = 64
MAX_BRANCHLESS_PARTITION_SIZE = 96

NORMAL = "modeled-normal"
PANIC = "modeled-panic"
ABORT = "modeled-abort"

IDENTITY_TOTAL_ORDER = "identity-total-order"
RANK_TOTAL_ORDER = "rank-total-order"
CONSTANT_EQUAL = "constant-equal"
STATE_PARITY_ORDER = "state-parity-order"
INCREMENT_STATE = "increment-state"
IDENTITY_STATE = "identity-state"
AFFINE_STATE = "affine-state"

COVERED_SOURCE_PHASES = (
    "public sort_unstable adapter to sort::unstable::sort and T::lt",
    "SizedTypeProperties zero-sized-type and trivial-length returns",
    "cfg_select optimize-for-size and 16-bit heapsort dispatch",
    "configuration and imbalance-fallback heapsort with sift_down",
    "length-at-most-20 insertion_sort_shift_left and CopyOnDrop",
    "find_existing_run ascending and strict-descending reversal",
    "UnstableSmallSortTypeImpl specialization and thresholds",
    "small-sort fallback, sort8/sort9, presorted-length-one, scratch merge, and restoration",
    "choose_pivot, median3, and recursive median3",
    "partition wrapper and all three configuration-selected kernels",
    "GapGuard and GapGuardRaw restoration on comparator panic",
    "duplicate-heavy ancestor-pivot reverse partition",
    "recursive-left and iterative-right quicksort",
    "imbalance-limit decrement and heapsort fallback",
    "normal unit return and comparator panic propagation",
)
MISSING_SOURCE_PHASES: tuple[str, ...] = ()

TARGET_078_KERNEL_CORRESPONDENCE = (
    {
        "target_080_phase": "insert_tail",
        "target_078_symbol": (
            "tools/target_078_operational_v1.py::_insert_tail"
        ),
        "shared_rust_source": (
            "core/src/slice/sort/shared/smallsort.rs:542-577"
        ),
        "compared_fields": (
            "full sequence",
            "callback-visible state",
            "panic status",
        ),
    },
    {
        "target_080_phase": "insertion_sort_shift_left",
        "target_078_symbol": (
            "tools/target_078_operational_v1.py::"
            "_insertion_sort_shift_left"
        ),
        "shared_rust_source": (
            "core/src/slice/sort/shared/smallsort.rs:579-608"
        ),
        "compared_fields": (
            "full sequence",
            "callback-visible state",
            "panic status",
        ),
    },
    {
        "target_080_phase": "choose_pivot",
        "target_078_symbol": (
            "tools/target_078_operational_v1.py::_choose_pivot"
        ),
        "shared_rust_source": "core/src/slice/sort/shared/pivot.rs:10-94",
        "compared_fields": (
            "pivot position",
            "callback-visible state",
            "panic status",
        ),
    },
    {
        "target_080_phase": "partition",
        "target_078_symbol": "tools/target_078_operational_v1.py::_partition",
        "shared_rust_source": (
            "core/src/slice/sort/unstable/quicksort.rs:82-393"
        ),
        "compared_fields": (
            "full sequence",
            "partition index",
            "callback-visible state",
            "panic status",
        ),
    },
)


class BoundaryViolation(ValueError):
    """A supplied per-call Ord relation is not total or contract-admissible."""


class _OrdPanic(RuntimeError):
    def __init__(self, phase: str) -> None:
        super().__init__(phase)
        self.phase = phase


class _SourceAbort(BaseException):
    def __init__(self, phase: str) -> None:
        super().__init__(phase)
        self.phase = phase


@dataclass(frozen=True, order=True)
class ObservationKey:
    state: int
    left_identity: int
    right_identity: int


@dataclass(frozen=True)
class OrdObservation:
    is_less: bool
    next_state: int
    panicked: bool


@dataclass(frozen=True)
class OrdBoundary:
    """Total per-call Ord::lt, next-state, and panic functions."""

    callback_identity: int
    initial_state: int
    result_mode: str
    next_state_mode: str
    contract_result_mode: str | None
    rank_pairs: tuple[tuple[int, int], ...] = ()
    affine_multiplier: int = 1
    affine_offset: int = 1
    panic_states: frozenset[int] = frozenset()
    panic_keys: frozenset[ObservationKey] = frozenset()

    def __post_init__(self) -> None:
        if self.result_mode not in (
            IDENTITY_TOTAL_ORDER,
            RANK_TOTAL_ORDER,
            CONSTANT_EQUAL,
            STATE_PARITY_ORDER,
        ):
            raise BoundaryViolation("unknown total Ord::lt result mode")
        if self.next_state_mode not in (
            INCREMENT_STATE,
            IDENTITY_STATE,
            AFFINE_STATE,
        ):
            raise BoundaryViolation("unknown total callback-state mode")
        if self.contract_result_mode not in (
            None,
            IDENTITY_TOTAL_ORDER,
            RANK_TOTAL_ORDER,
            CONSTANT_EQUAL,
        ):
            raise BoundaryViolation(
                "contract ordering must be state-independent"
            )
        exact_contract = {
            IDENTITY_TOTAL_ORDER: IDENTITY_TOTAL_ORDER,
            RANK_TOTAL_ORDER: RANK_TOTAL_ORDER,
            CONSTANT_EQUAL: CONSTANT_EQUAL,
        }.get(self.result_mode)
        if (
            self.contract_result_mode is not None
            and self.contract_result_mode != exact_contract
        ):
            raise BoundaryViolation(
                "implementation Ord::lt must exactly project to contract Ord"
            )
        identities = [identity for identity, _ in self.rank_pairs]
        if len(identities) != len(set(identities)):
            raise BoundaryViolation("rank identities must be unique")
        if (
            self.result_mode == RANK_TOTAL_ORDER
            or self.contract_result_mode == RANK_TOTAL_ORDER
        ) and not self.rank_pairs:
            raise BoundaryViolation("rank ordering requires rank pairs")
        if not isinstance(self.panic_states, frozenset):
            raise TypeError("panic_states must be a frozenset")
        if not isinstance(self.panic_keys, frozenset):
            raise TypeError("panic_keys must be a frozenset")

    def _rank(self, identity: int) -> tuple[int, int]:
        ranks = dict(self.rank_pairs)
        if identity in ranks:
            return (0, ranks[identity])
        return (1, identity)

    def _result(
        self,
        mode: str,
        state: int,
        left_identity: int,
        right_identity: int,
    ) -> bool:
        if mode == IDENTITY_TOTAL_ORDER:
            return left_identity < right_identity
        if mode == RANK_TOTAL_ORDER:
            return self._rank(left_identity) < self._rank(right_identity)
        if mode == CONSTANT_EQUAL:
            return False
        if mode == STATE_PARITY_ORDER:
            if state % 2 == 0:
                return self._rank(left_identity) < self._rank(right_identity)
            return self._rank(right_identity) < self._rank(left_identity)
        raise BoundaryViolation(f"unsupported Ord::lt mode: {mode}")

    def observe(
        self, state: int, left_identity: int, right_identity: int
    ) -> OrdObservation:
        key = ObservationKey(state, left_identity, right_identity)
        if self.next_state_mode == INCREMENT_STATE:
            next_state = state + 1
        elif self.next_state_mode == IDENTITY_STATE:
            next_state = state
        else:
            next_state = (
                self.affine_multiplier * state + self.affine_offset
            )
        observation = OrdObservation(
            is_less=self._result(
                self.result_mode,
                state,
                left_identity,
                right_identity,
            ),
            next_state=next_state,
            panicked=state in self.panic_states or key in self.panic_keys,
        )
        if not isinstance(observation.is_less, bool):
            raise BoundaryViolation("Ord::lt result must be boolean")
        if not isinstance(observation.next_state, int):
            raise BoundaryViolation("callback next-state must be an integer")
        if not isinstance(observation.panicked, bool):
            raise BoundaryViolation("callback panic must be boolean")
        return observation

    def contract_is_less(
        self, left_identity: int, right_identity: int
    ) -> bool:
        if self.contract_result_mode is None:
            raise BoundaryViolation(
                "boundary has no state-independent contract Ord projection"
            )
        return self._result(
            self.contract_result_mode,
            self.initial_state,
            left_identity,
            right_identity,
        )

    def contract_admissible(self) -> bool:
        return self.contract_result_mode is not None


@dataclass(frozen=True)
class SourceConfiguration:
    optimize_for_size: bool = False
    target_pointer_width: int = 64
    element_size: int = 8
    is_freeze: bool = False
    is_copy: bool = False
    has_efficient_in_place_swap: bool | None = None

    def __post_init__(self) -> None:
        if self.target_pointer_width <= 0:
            raise ValueError("target_pointer_width must be positive")
        if self.element_size < 0:
            raise ValueError("element_size must be nonnegative")
        if self.is_copy and not self.is_freeze:
            raise ValueError("Copy specialization requires Freeze")
        source_efficient_swap = self.element_size <= 8
        if (
            self.has_efficient_in_place_swap is not None
            and self.has_efficient_in_place_swap != source_efficient_swap
        ):
            raise ValueError(
                "efficient-swap property must equal size_of::<T>() <= 8"
            )

    @property
    def is_zst(self) -> bool:
        return self.element_size == 0

    @property
    def use_configuration_heapsort(self) -> bool:
        return self.optimize_for_size or self.target_pointer_width == 16

    @property
    def efficient_swap(self) -> bool:
        return self.element_size <= 8


@dataclass(frozen=True)
class SortInput:
    initial_sequence: tuple[int, ...]
    configuration: SourceConfiguration = SourceConfiguration()


@dataclass(frozen=True)
class FinalState:
    sequence: tuple[int, ...]
    callback_state: int
    panicked: bool
    aborted: bool
    terminal: bool


@dataclass(frozen=True)
class DerivedStep:
    """A source-derived event; it is evidence and never boundary input."""

    kind: str
    phase: str
    details: tuple[tuple[str, Any], ...] = ()
    sequence_after: tuple[int, ...] = ()
    callback_state_after: int = 0

    def detail(self, name: str) -> Any:
        return dict(self.details)[name]


@dataclass(frozen=True)
class Execution:
    state: FinalState
    terminal_status: str
    unit_returned: bool
    missing_source_phase: str | None
    derived_steps: tuple[DerivedStep, ...]
    panic_phase: str | None = None
    abort_phase: str | None = None


class _Engine:
    def __init__(
        self, sort_input: SortInput, boundary: OrdBoundary
    ) -> None:
        self.sort_input = sort_input
        self.boundary = boundary
        self.sequence = list(sort_input.initial_sequence)
        self.callback_state = boundary.initial_state
        self.steps: list[DerivedStep] = []

    def record(self, kind: str, phase: str, **details: Any) -> None:
        self.steps.append(
            DerivedStep(
                kind,
                phase,
                tuple(sorted(details.items())),
                tuple(self.sequence),
                self.callback_state,
            )
        )

    def is_less(
        self, left_identity: int, right_identity: int, phase: str
    ) -> bool:
        state = self.callback_state
        observation = self.boundary.observe(
            state, left_identity, right_identity
        )
        self.callback_state = observation.next_state
        self.record(
            "ord-lt",
            phase,
            is_less=observation.is_less,
            left_identity=left_identity,
            next_state=observation.next_state,
            panicked=observation.panicked,
            right_identity=right_identity,
            state=state,
        )
        if observation.panicked:
            raise _OrdPanic(phase)
        return observation.is_less

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

    def finish(
        self,
        status: str,
        *,
        panic_phase: str | None = None,
        abort_phase: str | None = None,
    ) -> Execution:
        return Execution(
            state=FinalState(
                sequence=tuple(self.sequence),
                callback_state=self.callback_state,
                panicked=status == PANIC,
                aborted=status == ABORT,
                terminal=True,
            ),
            terminal_status=status,
            unit_returned=status == NORMAL,
            missing_source_phase=None,
            derived_steps=tuple(self.steps),
            panic_phase=panic_phase,
            abort_phase=abort_phase,
        )


def integer_total_order_boundary(
    *,
    callback_identity: int = 80,
    initial_state: int = 0,
    panic_states: frozenset[int] = frozenset(),
    panic_keys: frozenset[ObservationKey] = frozenset(),
) -> OrdBoundary:
    return OrdBoundary(
        callback_identity=callback_identity,
        initial_state=initial_state,
        result_mode=IDENTITY_TOTAL_ORDER,
        next_state_mode=INCREMENT_STATE,
        contract_result_mode=IDENTITY_TOTAL_ORDER,
        panic_states=panic_states,
        panic_keys=panic_keys,
    )


def rank_total_order_boundary(
    class_ranks: Mapping[int, int],
    *,
    callback_identity: int = 80,
    initial_state: int = 0,
    next_state_mode: str = INCREMENT_STATE,
    affine_multiplier: int = 1,
    affine_offset: int = 1,
    panic_states: frozenset[int] = frozenset(),
    panic_keys: frozenset[ObservationKey] = frozenset(),
) -> OrdBoundary:
    return OrdBoundary(
        callback_identity=callback_identity,
        initial_state=initial_state,
        result_mode=RANK_TOTAL_ORDER,
        next_state_mode=next_state_mode,
        contract_result_mode=RANK_TOTAL_ORDER,
        rank_pairs=tuple(sorted(class_ranks.items())),
        affine_multiplier=affine_multiplier,
        affine_offset=affine_offset,
        panic_states=panic_states,
        panic_keys=panic_keys,
    )


def all_equal_boundary(
    *,
    callback_identity: int = 80,
    initial_state: int = 0,
    panic_states: frozenset[int] = frozenset(),
) -> OrdBoundary:
    return OrdBoundary(
        callback_identity=callback_identity,
        initial_state=initial_state,
        result_mode=CONSTANT_EQUAL,
        next_state_mode=INCREMENT_STATE,
        contract_result_mode=CONSTANT_EQUAL,
        panic_states=panic_states,
    )


def symbolic_state_boundary(
    class_ranks: Mapping[int, int],
    *,
    initial_state: int = 0,
    next_state_mode: str = AFFINE_STATE,
    affine_multiplier: int = 1,
    affine_offset: int = 1,
    panic_states: frozenset[int] = frozenset(),
    panic_keys: frozenset[ObservationKey] = frozenset(),
) -> OrdBoundary:
    """Construct a total state-indexed operational fixture.

    It intentionally has no contract projection and is therefore useful only
    for panic/restoration and mutation replays, never classification.
    """

    return OrdBoundary(
        callback_identity=80,
        initial_state=initial_state,
        result_mode=STATE_PARITY_ORDER,
        next_state_mode=next_state_mode,
        contract_result_mode=None,
        rank_pairs=tuple(sorted(class_ranks.items())),
        affine_multiplier=affine_multiplier,
        affine_offset=affine_offset,
        panic_states=panic_states,
        panic_keys=panic_keys,
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
    except _OrdPanic:
        engine.sequence[gap] = temporary
        engine.record(
            "copy-on-drop-restore",
            phase,
            destination=gap,
            panicked=True,
            tail=tail,
            value=temporary,
        )
        raise

    engine.sequence[gap] = temporary
    engine.record(
        "copy-on-drop-restore",
        phase,
        destination=gap,
        panicked=False,
        tail=tail,
        value=temporary,
    )


def _insertion_sort_shift_left(
    engine: _Engine, start: int, end: int, offset: int
) -> None:
    length = end - start
    if offset == 0 or offset > length:
        raise _SourceAbort("insertion-sort-precondition")
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


def _insert_tail_buffer(
    engine: _Engine,
    values: list[int],
    begin: int,
    tail: int,
    phase: str,
) -> None:
    temporary = values[tail]
    if not engine.is_less(
        temporary, values[tail - 1], f"{phase}:initial-compare"
    ):
        return
    sift = tail - 1
    gap = tail
    try:
        while True:
            values[gap] = values[sift]
            gap = sift
            if sift == begin:
                break
            sift -= 1
            if not engine.is_less(
                temporary, values[sift], f"{phase}:sift-compare"
            ):
                break
    except _OrdPanic:
        values[gap] = temporary
        engine.record(
            "scratch-copy-on-drop-restore",
            phase,
            destination=gap,
            panicked=True,
        )
        raise
    values[gap] = temporary


def _sort4_values(
    engine: _Engine, values: list[int], phase: str
) -> list[int]:
    if len(values) != 4:
        raise _SourceAbort("sort4-precondition")
    c1 = engine.is_less(values[1], values[0], f"{phase}:c1")
    c2 = engine.is_less(values[3], values[2], f"{phase}:c2")
    a = 1 if c1 else 0
    b = 0 if c1 else 1
    c = 3 if c2 else 2
    d = 2 if c2 else 3
    c3 = engine.is_less(values[c], values[a], f"{phase}:c3")
    c4 = engine.is_less(values[d], values[b], f"{phase}:c4")
    minimum = c if c3 else a
    maximum = b if c4 else d
    unknown_left = a if c3 else c if c4 else b
    unknown_right = d if c4 else b if c3 else c
    c5 = engine.is_less(
        values[unknown_right],
        values[unknown_left],
        f"{phase}:c5",
    )
    low = unknown_right if c5 else unknown_left
    high = unknown_left if c5 else unknown_right
    result = [
        values[minimum],
        values[low],
        values[high],
        values[maximum],
    ]
    engine.record("sort4-stable", phase, result=tuple(result))
    return result


def _bidirectional_merge_values(
    engine: _Engine,
    values: list[int],
    split: int,
    phase: str,
) -> list[int]:
    length = len(values)
    if length < 2 or split != length // 2:
        raise _SourceAbort("bidirectional-merge-precondition")
    output: list[int | None] = [None] * length
    left = 0
    right = split
    left_reverse = split - 1
    right_reverse = length - 1
    destination = 0
    destination_reverse = length - 1

    for iteration in range(split):
        take_left = not engine.is_less(
            values[right],
            values[left],
            f"{phase}:merge-up[{iteration}]",
        )
        output[destination] = values[left if take_left else right]
        left += int(take_left)
        right += int(not take_left)
        destination += 1

        take_right = not engine.is_less(
            values[right_reverse],
            values[left_reverse],
            f"{phase}:merge-down[{iteration}]",
        )
        output[destination_reverse] = values[
            right_reverse if take_right else left_reverse
        ]
        right_reverse -= int(take_right)
        left_reverse -= int(not take_right)
        destination_reverse -= 1

    left_end = left_reverse + 1
    right_end = right_reverse + 1
    if length % 2:
        left_nonempty = left < left_end
        output[destination] = values[left if left_nonempty else right]
        left += int(left_nonempty)
        right += int(not left_nonempty)

    if left != left_end or right != right_end:
        engine.record("ord-violation-panic", phase)
        raise _OrdPanic(f"{phase}:ord-violation")
    if any(value is None for value in output):
        raise AssertionError("merge did not initialize every destination")
    result = [int(value) for value in output]
    engine.record(
        "bidirectional-merge",
        phase,
        result=tuple(result),
        split=split,
    )
    return result


def _sort8_values(
    engine: _Engine, values: list[int], phase: str
) -> list[int]:
    if len(values) != 8:
        raise _SourceAbort("sort8-precondition")
    scratch = _sort4_values(engine, values[:4], f"{phase}:left-sort4")
    scratch.extend(
        _sort4_values(engine, values[4:], f"{phase}:right-sort4")
    )
    return _bidirectional_merge_values(
        engine, scratch, 4, f"{phase}:merge"
    )


SORT9_NETWORK = (
    (0, 3),
    (1, 7),
    (2, 5),
    (4, 8),
    (0, 7),
    (2, 4),
    (3, 8),
    (5, 6),
    (0, 2),
    (1, 3),
    (4, 5),
    (7, 8),
    (1, 4),
    (3, 6),
    (5, 7),
    (0, 1),
    (2, 4),
    (3, 5),
    (6, 8),
    (2, 3),
    (4, 5),
    (6, 7),
    (1, 2),
    (3, 4),
    (5, 6),
)

SORT13_NETWORK = (
    (0, 12),
    (1, 10),
    (2, 9),
    (3, 7),
    (5, 11),
    (6, 8),
    (1, 6),
    (2, 3),
    (4, 11),
    (7, 9),
    (8, 10),
    (0, 4),
    (1, 2),
    (3, 6),
    (7, 8),
    (9, 10),
    (11, 12),
    (4, 6),
    (5, 9),
    (8, 11),
    (10, 12),
    (0, 5),
    (3, 8),
    (4, 7),
    (6, 11),
    (9, 10),
    (0, 1),
    (2, 5),
    (6, 9),
    (7, 8),
    (10, 11),
    (1, 3),
    (2, 4),
    (5, 6),
    (9, 10),
    (1, 2),
    (3, 4),
    (5, 7),
    (6, 8),
    (2, 3),
    (4, 5),
    (6, 7),
    (8, 9),
    (3, 4),
    (5, 6),
)


def _swap_if_less(
    engine: _Engine,
    first: int,
    second: int,
    phase: str,
) -> None:
    should_swap = engine.is_less(
        engine.sequence[second],
        engine.sequence[first],
        f"{phase}:compare",
    )
    engine.record(
        "network-comparator",
        phase,
        first=first,
        second=second,
        should_swap=should_swap,
    )
    if should_swap:
        engine.swap(first, second, f"{phase}:swap")


def _sort_network_prefix(
    engine: _Engine,
    start: int,
    pairs: tuple[tuple[int, int], ...],
    phase: str,
) -> None:
    for index, (first, second) in enumerate(pairs):
        _swap_if_less(
            engine,
            start + first,
            start + second,
            f"{phase}[{index}]",
        )


def _small_sort_threshold(configuration: SourceConfiguration) -> int:
    if not configuration.is_freeze:
        return SMALL_SORT_FALLBACK_THRESHOLD
    general_fits = (
        configuration.element_size * SMALL_SORT_GENERAL_SCRATCH_LEN
        <= MAX_STACK_ARRAY_SIZE
    )
    if not configuration.is_copy:
        return (
            SMALL_SORT_GENERAL_THRESHOLD
            if general_fits
            else SMALL_SORT_FALLBACK_THRESHOLD
        )
    network_fits = (
        configuration.efficient_swap
        and configuration.element_size * SMALL_SORT_NETWORK_SCRATCH_LEN
        <= MAX_STACK_ARRAY_SIZE
    )
    if network_fits:
        return SMALL_SORT_NETWORK_THRESHOLD
    if general_fits:
        return SMALL_SORT_GENERAL_THRESHOLD
    return SMALL_SORT_FALLBACK_THRESHOLD


def _small_sort_kind(configuration: SourceConfiguration) -> str:
    if not configuration.is_freeze:
        return "fallback"
    general_fits = (
        configuration.element_size * SMALL_SORT_GENERAL_SCRATCH_LEN
        <= MAX_STACK_ARRAY_SIZE
    )
    if not configuration.is_copy:
        return "general" if general_fits else "fallback"
    network_fits = (
        configuration.efficient_swap
        and configuration.element_size * SMALL_SORT_NETWORK_SCRATCH_LEN
        <= MAX_STACK_ARRAY_SIZE
    )
    if network_fits:
        return "network"
    return "general" if general_fits else "fallback"


def _small_sort_fallback(
    engine: _Engine, start: int, end: int
) -> None:
    if end - start >= 2:
        _insertion_sort_shift_left(engine, start, end, 1)


def _small_sort_general(
    engine: _Engine, start: int, end: int
) -> None:
    length = end - start
    if length < 2:
        return
    if length + 16 > SMALL_SORT_GENERAL_SCRATCH_LEN:
        raise _SourceAbort("small-sort-general-scratch")

    source = list(engine.sequence[start:end])
    scratch: list[int | None] = [None] * length
    half = length // 2
    if engine.sort_input.configuration.element_size <= 16 and length >= 16:
        scratch[:8] = _sort8_values(
            engine, source[:8], "small-sort-general:left-sort8"
        )
        scratch[half : half + 8] = _sort8_values(
            engine,
            source[half : half + 8],
            "small-sort-general:right-sort8",
        )
        presorted_length = 8
        presorted_implementation = "sort8"
    elif length >= 8:
        scratch[:4] = _sort4_values(
            engine, source[:4], "small-sort-general:left-sort4"
        )
        scratch[half : half + 4] = _sort4_values(
            engine,
            source[half : half + 4],
            "small-sort-general:right-sort4",
        )
        presorted_length = 4
        presorted_implementation = "sort4"
    else:
        scratch[0] = source[0]
        scratch[half] = source[half]
        presorted_length = 1
        presorted_implementation = "singleton"
    engine.record(
        "small-sort-general-presorted",
        "small-sort-general",
        implementation=presorted_implementation,
        presorted_length=presorted_length,
    )

    for offset, desired_length in (
        (0, half),
        (half, length - half),
    ):
        for index in range(presorted_length, desired_length):
            scratch[offset + index] = source[offset + index]
            initialized = [
                int(value)
                for value in scratch
                if value is not None
            ]
            del initialized
            values = [
                int(value) if value is not None else 0
                for value in scratch
            ]
            _insert_tail_buffer(
                engine,
                values,
                offset,
                offset + index,
                (
                    "small-sort-general:"
                    f"insert-tail[{offset}:{offset + desired_length}:"
                    f"{index}]"
                ),
            )
            scratch[offset : offset + index + 1] = values[
                offset : offset + index + 1
            ]

    if any(value is None for value in scratch):
        raise AssertionError("small-sort scratch was not fully initialized")
    initialized_scratch = [int(value) for value in scratch]
    try:
        merged = _bidirectional_merge_values(
            engine,
            initialized_scratch,
            half,
            "small-sort-general:final-merge",
        )
    except _OrdPanic:
        engine.sequence[start:end] = initialized_scratch
        engine.record(
            "copy-on-drop-restore",
            "small-sort-general",
            destination=start,
            length=length,
            panicked=True,
            result=tuple(initialized_scratch),
        )
        raise
    engine.sequence[start:end] = merged
    engine.record(
        "small-sort-general-copy-back",
        "small-sort-general",
        length=length,
        result=tuple(merged),
        window_end=end,
        window_start=start,
    )


def _small_sort_network(
    engine: _Engine, start: int, end: int
) -> None:
    length = end - start
    if length < 2:
        return
    if length > SMALL_SORT_NETWORK_SCRATCH_LEN:
        raise _SourceAbort("small-sort-network-scratch")
    half = length // 2
    no_merge = length < 18
    regions = (
        ((start, end),)
        if no_merge
        else ((start, start + half), (start + half, end))
    )
    for region_start, region_end in regions:
        region_length = region_end - region_start
        if region_length >= 13:
            _sort_network_prefix(
                engine,
                region_start,
                SORT13_NETWORK,
                "small-sort-network:sort13",
            )
            presorted_length = 13
            presorted_implementation = "sort13"
        elif region_length >= 9:
            _sort_network_prefix(
                engine,
                region_start,
                SORT9_NETWORK,
                "small-sort-network:sort9",
            )
            presorted_length = 9
            presorted_implementation = "sort9"
        else:
            presorted_length = 1
            presorted_implementation = "insertion"
        engine.record(
            "small-sort-network-presorted",
            "small-sort-network",
            implementation=presorted_implementation,
            presorted_length=presorted_length,
            window_end=region_end,
            window_start=region_start,
        )
        _insertion_sort_shift_left(
            engine,
            region_start,
            region_end,
            presorted_length,
        )
    if no_merge:
        return

    source = list(engine.sequence[start:end])
    merged = _bidirectional_merge_values(
        engine, source, half, "small-sort-network:final-merge"
    )
    engine.sequence[start:end] = merged
    engine.record(
        "small-sort-network-copy-back",
        "small-sort-network",
        length=length,
        result=tuple(merged),
        window_end=end,
        window_start=start,
    )


def _small_sort(engine: _Engine, start: int, end: int) -> None:
    configuration = engine.sort_input.configuration
    kind = _small_sort_kind(configuration)
    threshold = _small_sort_threshold(configuration)
    if end - start > threshold:
        raise _SourceAbort("small-sort-threshold")
    engine.record(
        "small-sort-dispatch",
        "quicksort",
        implementation=kind,
        threshold=threshold,
        window_end=end,
        window_start=start,
    )
    if kind == "fallback":
        _small_sort_fallback(engine, start, end)
    elif kind == "general":
        _small_sort_general(engine, start, end)
    else:
        _small_sort_network(engine, start, end)


def _find_existing_run(engine: _Engine) -> tuple[int, bool]:
    length = len(engine.sequence)
    if length < 2:
        return length, False
    run_length = 2
    strictly_descending = engine.is_less(
        engine.sequence[1],
        engine.sequence[0],
        "find-existing-run:direction",
    )
    if strictly_descending:
        while run_length < length and engine.is_less(
            engine.sequence[run_length],
            engine.sequence[run_length - 1],
            "find-existing-run:descending",
        ):
            run_length += 1
    else:
        while run_length < length and not engine.is_less(
            engine.sequence[run_length],
            engine.sequence[run_length - 1],
            "find-existing-run:ascending",
        ):
            run_length += 1
    engine.record(
        "existing-run",
        "ipnsort",
        run_length=run_length,
        strictly_descending=strictly_descending,
    )
    return run_length, strictly_descending


def _sift_down(
    engine: _Engine,
    start: int,
    end: int,
    node: int,
    phase: str,
) -> None:
    length = end - start
    if node > length:
        raise _SourceAbort("sift-down-precondition")
    while True:
        child = 2 * node + 1
        if child >= length:
            break
        if child + 1 < length and engine.is_less(
            engine.sequence[start + child],
            engine.sequence[start + child + 1],
            f"{phase}:choose-greater-child",
        ):
            child += 1
        if not engine.is_less(
            engine.sequence[start + node],
            engine.sequence[start + child],
            f"{phase}:parent-child",
        ):
            break
        engine.swap(
            start + node,
            start + child,
            f"{phase}:swap",
        )
        node = child


def _heapsort(
    engine: _Engine, start: int, end: int, phase: str
) -> None:
    length = end - start
    engine.record(
        "heapsort-enter",
        phase,
        window_end=end,
        window_start=start,
    )
    for index in range(length + length // 2 - 1, -1, -1):
        if index >= length:
            sift_index = index - length
        else:
            engine.swap(start, start + index, f"{phase}:extract")
            sift_index = 0
        _sift_down(
            engine,
            start,
            start + min(index, length),
            sift_index,
            f"{phase}:sift-down[{index}]",
        )
    engine.record(
        "heapsort-return",
        phase,
        window_end=end,
        window_start=start,
    )


def _median3(
    engine: _Engine, first: int, second: int, third: int, phase: str
) -> int:
    first_less_second = engine.is_less(
        engine.sequence[first],
        engine.sequence[second],
        f"{phase}:a-b",
    )
    first_less_third = engine.is_less(
        engine.sequence[first],
        engine.sequence[third],
        f"{phase}:a-c",
    )
    if first_less_second == first_less_third:
        second_less_third = engine.is_less(
            engine.sequence[second],
            engine.sequence[third],
            f"{phase}:b-c",
        )
        result = (
            third
            if second_less_third ^ first_less_second
            else second
        )
        branch = "outer"
    else:
        result = first
        branch = "first"
    engine.record(
        "median3",
        phase,
        first=first,
        second=second,
        third=third,
        branch=branch,
        result=result,
    )
    return result


def _median3_rec(
    engine: _Engine,
    first: int,
    second: int,
    third: int,
    region_length: int,
    phase: str,
) -> int:
    engine.record(
        "median3-rec-enter",
        phase,
        first=first,
        second=second,
        third=third,
        region_length=region_length,
    )
    if region_length * 8 >= PSEUDO_MEDIAN_REC_THRESHOLD:
        eighth = region_length // 8
        first = _median3_rec(
            engine,
            first,
            first + eighth * 4,
            first + eighth * 7,
            eighth,
            f"{phase}:a",
        )
        second = _median3_rec(
            engine,
            second,
            second + eighth * 4,
            second + eighth * 7,
            eighth,
            f"{phase}:b",
        )
        third = _median3_rec(
            engine,
            third,
            third + eighth * 4,
            third + eighth * 7,
            eighth,
            f"{phase}:c",
        )
    return _median3(
        engine,
        first,
        second,
        third,
        f"{phase}:median3",
    )


def _choose_pivot(engine: _Engine, start: int, end: int) -> int:
    length = end - start
    if length < 8:
        raise _SourceAbort("choose-pivot-precondition")
    eighth = length // 8
    first = start
    second = start + eighth * 4
    third = start + eighth * 7
    if length < PSEUDO_MEDIAN_REC_THRESHOLD:
        result = _median3(
            engine,
            first,
            second,
            third,
            "choose-pivot:median3",
        )
        branch = "median3"
    else:
        result = _median3_rec(
            engine,
            first,
            second,
            third,
            eighth,
            "choose-pivot:median3-rec",
        )
        branch = "median3-rec"
    engine.record(
        "choose-pivot",
        "choose-pivot",
        branch=branch,
        pivot_position=result - start,
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
            right_identity,
            left_identity,
            f"{phase}:reverse-less",
        )
    else:
        result = engine.is_less(
            left_identity,
            right_identity,
            phase,
        )
    engine.record(
        "partition-predicate",
        phase,
        left_identity=left_identity,
        right_identity=right_identity,
        result=result,
        reverse=reverse,
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
        right_is_less = _partition_predicate(
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
            right_is_less=right_is_less,
        )
        left += int(right_is_less)
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
    unroll_length = (
        2
        if engine.sort_input.configuration.element_size <= 16
        else 1
    )
    engine.record(
        "partition-implementation",
        "partition-lomuto-branchless-cyclic",
        implementation="lomuto-cyclic",
        unroll_length=unroll_length,
        window_end=end,
        window_start=start,
    )
    gap_value = engine.sequence[start]
    gap_position = start
    count_less = 0
    try:
        for right in range(start + 1, end):
            right_value = engine.sequence[right]
            right_is_less = _partition_predicate(
                engine,
                right_value,
                pivot_identity,
                "partition-lomuto-cyclic:compare",
                reverse=reverse,
            )
            left = start + count_less
            engine.sequence[gap_position] = engine.sequence[left]
            engine.sequence[left] = right_value
            engine.record(
                "partition-cycle",
                "partition-lomuto-branchless-cyclic",
                gap_destination=gap_position,
                left=left,
                right=right,
                right_is_less=right_is_less,
            )
            gap_position = right
            count_less += int(right_is_less)

        right_is_less = _partition_predicate(
            engine,
            gap_value,
            pivot_identity,
            "partition-lomuto-cyclic:cleanup-compare",
            reverse=reverse,
        )
        left = start + count_less
        engine.sequence[gap_position] = engine.sequence[left]
        engine.sequence[left] = gap_value
        count_less += int(right_is_less)
        engine.record(
            "partition-cycle-cleanup",
            "partition-lomuto-branchless-cyclic",
            consumed_guard=True,
            gap_destination=gap_position,
            gap_value=gap_value,
            left=left,
            right_is_less=right_is_less,
        )
        return count_less
    except _OrdPanic:
        engine.sequence[gap_position] = gap_value
        engine.record(
            "gap-guard-restore",
            "partition-lomuto-branchless-cyclic",
            destination=gap_position,
            panicked=True,
            value=gap_value,
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
    except _OrdPanic:
        if gap_value is not None:
            assert gap_position is not None
            engine.sequence[gap_position] = gap_value
            engine.record(
                "gap-guard-restore",
                "partition-hoare-branchy-cyclic",
                destination=gap_position,
                panicked=True,
                value=gap_value,
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
            value=gap_value,
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
    if length == 0:
        engine.record(
            "partition-empty",
            "partition",
            mid=0,
            reverse=reverse,
            window_end=end,
            window_start=start,
        )
        return 0
    if not 0 <= pivot_position < length:
        raise _SourceAbort("partition-precondition")
    pivot_global = start + pivot_position
    engine.swap(start, pivot_global, "partition:pivot-to-front")
    pivot_identity = engine.sequence[start]
    lower_start = start + 1
    configuration = engine.sort_input.configuration
    if configuration.element_size <= MAX_BRANCHLESS_PARTITION_SIZE:
        if configuration.optimize_for_size:
            count_less = _partition_lomuto_branchless_simple(
                engine,
                lower_start,
                end,
                pivot_identity,
                reverse=reverse,
            )
        else:
            count_less = _partition_lomuto_branchless_cyclic(
                engine,
                lower_start,
                end,
                pivot_identity,
                reverse=reverse,
            )
    else:
        count_less = _partition_hoare_branchy_cyclic(
            engine,
            lower_start,
            end,
            pivot_identity,
            reverse=reverse,
        )
    if count_less >= length:
        raise _SourceAbort("partition-result")
    engine.swap(
        start,
        start + count_less,
        "partition:pivot-to-middle",
    )
    engine.record(
        "partition-result",
        "partition",
        mid=count_less,
        reverse=reverse,
        window_end=end,
        window_start=start,
    )
    return count_less


def _quicksort(
    engine: _Engine,
    start: int,
    end: int,
    ancestor_pivot: int | None,
    limit: int,
    *,
    depth: int = 0,
) -> None:
    while True:
        length = end - start
        threshold = _small_sort_threshold(
            engine.sort_input.configuration
        )
        engine.record(
            "quicksort-loop",
            "quicksort",
            ancestor_present=ancestor_pivot is not None,
            depth=depth,
            limit=limit,
            threshold=threshold,
            window_end=end,
            window_start=start,
        )
        if length <= threshold:
            _small_sort(engine, start, end)
            engine.record(
                "quicksort-return",
                "quicksort:small-sort",
                depth=depth,
                window_end=end,
                window_start=start,
            )
            return
        if limit == 0:
            _heapsort(
                engine,
                start,
                end,
                "quicksort:imbalance-fallback",
            )
            engine.record(
                "quicksort-return",
                "quicksort:heapsort",
                depth=depth,
                window_end=end,
                window_start=start,
            )
            return
        limit -= 1
        pivot_position = _choose_pivot(engine, start, end)

        if ancestor_pivot is not None:
            pivot_identity = engine.sequence[start + pivot_position]
            if not engine.is_less(
                ancestor_pivot,
                pivot_identity,
                "quicksort:ancestor-pivot-compare",
            ):
                count_less = _partition(
                    engine,
                    start,
                    end,
                    pivot_position,
                    reverse=True,
                )
                engine.record(
                    "ancestor-pivot-partition",
                    "quicksort",
                    count_equal=count_less + 1,
                    depth=depth,
                    window_end=end,
                    window_start=start,
                )
                start += count_less + 1
                ancestor_pivot = None
                continue

        count_less = _partition(
            engine,
            start,
            end,
            pivot_position,
        )
        pivot_index = start + count_less
        pivot_identity = engine.sequence[pivot_index]
        engine.record(
            "quicksort-partition",
            "quicksort",
            depth=depth,
            left_end=pivot_index,
            pivot_index=pivot_index,
            right_start=pivot_index + 1,
            window_end=end,
            window_start=start,
        )

        _quicksort(
            engine,
            start,
            pivot_index,
            ancestor_pivot,
            limit,
            depth=depth + 1,
        )
        start = pivot_index + 1
        ancestor_pivot = pivot_identity
        engine.record(
            "quicksort-iterate-right",
            "quicksort",
            ancestor_identity=pivot_identity,
            depth=depth,
            limit=limit,
            window_end=end,
            window_start=start,
        )


def execute(sort_input: SortInput, boundary: OrdBoundary) -> Execution:
    """Execute the complete bound Rust 1.96 `sort_unstable` transition."""

    engine = _Engine(sort_input, boundary)
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
            _heapsort(engine, 0, length, "sort:configuration-heapsort")
            engine.record("return", "sort:configuration-heapsort")
            return engine.finish(NORMAL)
        if length <= MAX_LEN_ALWAYS_INSERTION_SORT:
            _insertion_sort_shift_left(engine, 0, length, 1)
            engine.record("return", "sort:insertion")
            return engine.finish(NORMAL)

        run_length, was_reversed = _find_existing_run(engine)
        if run_length == length:
            if was_reversed:
                engine.sequence.reverse()
                engine.record(
                    "reverse",
                    "ipnsort:full-descending-run",
                )
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
        _quicksort(engine, 0, length, None, limit)
        engine.record("return", "ipnsort:quicksort")
        return engine.finish(NORMAL)
    except _OrdPanic as panic:
        engine.record("panic", panic.phase)
        return engine.finish(PANIC, panic_phase=panic.phase)
    except _SourceAbort as abort:
        engine.record("abort", abort.phase)
        return engine.finish(ABORT, abort_phase=abort.phase)


def sequence_is_permutation(
    execution: Execution, before: tuple[int, ...]
) -> bool:
    return Counter(execution.state.sequence) == Counter(before)


def sequence_is_contract_sorted(
    execution: Execution, boundary: OrdBoundary
) -> bool:
    if not boundary.contract_admissible():
        raise BoundaryViolation(
            "contract sorting requires an admissible Ord projection"
        )
    sequence = execution.state.sequence
    return all(
        not boundary.contract_is_less(right, left)
        for left, right in zip(sequence, sequence[1:])
    )


def exact_equivalent(first: Execution, second: Execution) -> bool:
    return (
        first.state == second.state
        and first.terminal_status == second.terminal_status
        and first.unit_returned == second.unit_returned
        and first.missing_source_phase == second.missing_source_phase
        and first.panic_phase == second.panic_phase
        and first.abort_phase == second.abort_phase
    )


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 2,
        "target": TARGET,
        "model_id": MODEL_ID,
        "admitted_trust_site_ids": list(ADMITTED_TRUST_SITE_IDS),
        "replaced_trust_site_ids": list(REPLACED_TRUST_SITE_IDS),
        "pending_replacement_trust_site_ids": [],
        "boundary_narrower_than_target": True,
        "implementation_relation": (
            "total functions over every callback state and identity pair"
        ),
        "classification_admissibility": (
            "implementation is_less exactly equals one state-independent "
            "contract total preorder for every call"
        ),
        "supported_total_relations": [
            "integer identity order",
            "arbitrary finite duplicate-class ranks with total fallback",
            "all-equal order",
            "state-indexed symbolic replay relation (nonclassifying)",
            "increment, identity, or affine callback next-state",
            "state/key predicate callback panic",
        ],
        "shared_input_properties": [
            "optimize_for_size",
            "target_pointer_width",
            "element_size and derived IS_ZST",
            "Freeze specialization",
            "Copy specialization",
            "efficient in-place swap property",
        ],
        "shared_boundary_observations": [
            "total Ord::lt(state,left_identity,right_identity) result",
            "total callback next_state(state,left_identity,right_identity)",
            "total callback panic(state,left_identity,right_identity)",
        ],
        "prohibited_boundary_observations": [
            "realized comparison schedule",
            "pivot or partition choice",
            "swap choice",
            "selected output",
            "final sequence or permutation",
            "aggregate final state",
            "target execution trace",
            "precomputed terminal state",
        ],
    }
