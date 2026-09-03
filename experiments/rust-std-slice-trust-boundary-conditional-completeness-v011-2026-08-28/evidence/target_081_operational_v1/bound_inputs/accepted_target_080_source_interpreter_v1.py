#!/usr/bin/env python3
"""Independent Rust 1.96 source interpreter used for target-080 correspondence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import target_078_operational_v1 as selection


NORMAL = "modeled-normal"
PANIC = "modeled-panic"
ABORT = "modeled-abort"

MAX_LEN_ALWAYS_INSERTION_SORT = 20
SMALL_FALLBACK = 16
SMALL_GENERAL = 32
GENERAL_SCRATCH = 48
NETWORK_SCRATCH = 32
MAX_STACK = 4096


class _Abort(BaseException):
    pass


@dataclass(frozen=True)
class ReferenceExecution:
    sequence: tuple[int, ...]
    callback_state: int
    terminal_status: str
    panicked: bool
    aborted: bool
    terminal: bool
    unit_returned: bool
    events: tuple[selection.DerivedEvent, ...]


class _BoundaryAdapter:
    def __init__(self, boundary: Any) -> None:
        self.boundary = boundary
        self.initial_state = boundary.initial_state

    def observe(
        self, state: int, left_identity: int, right_identity: int
    ) -> selection.ComparatorObservation:
        observed = self.boundary.observe(
            state, left_identity, right_identity
        )
        return selection.ComparatorObservation(
            ordering=(
                selection.LESS
                if observed.is_less
                else selection.GREATER
            ),
            next_state=observed.next_state,
            panicked=observed.panicked,
        )


def _engine(initial: tuple[int, ...], configuration: Any, boundary: Any):
    source_input = selection.SelectionInput(
        initial_sequence=initial,
        index=0,
        allocation=80,
        borrow=80,
        is_zst=configuration.element_size == 0,
        configuration=selection.SourceConfiguration(
            optimize_for_size=configuration.optimize_for_size,
            element_size=configuration.element_size,
        ),
    )
    return selection._Engine(source_input, _BoundaryAdapter(boundary))


def _threshold(configuration: Any) -> int:
    if not configuration.is_freeze:
        return SMALL_FALLBACK
    general = configuration.element_size * GENERAL_SCRATCH <= MAX_STACK
    if not configuration.is_copy:
        return SMALL_GENERAL if general else SMALL_FALLBACK
    network = (
        configuration.element_size <= 8
        and configuration.element_size * NETWORK_SCRATCH <= MAX_STACK
    )
    return SMALL_GENERAL if network or general else SMALL_FALLBACK


def _kind(configuration: Any) -> str:
    if not configuration.is_freeze:
        return "fallback"
    general = configuration.element_size * GENERAL_SCRATCH <= MAX_STACK
    if not configuration.is_copy:
        return "general" if general else "fallback"
    if (
        configuration.element_size <= 8
        and configuration.element_size * NETWORK_SCRATCH <= MAX_STACK
    ):
        return "network"
    return "general" if general else "fallback"


def _sort4(
    engine: Any, values: list[int], phase: str
) -> list[int]:
    less = engine.is_less
    c1 = less(values[1], values[0], f"{phase}:c1")
    c2 = less(values[3], values[2], f"{phase}:c2")
    a, b = ((1, 0) if c1 else (0, 1))
    c, d = ((3, 2) if c2 else (2, 3))
    c3 = less(values[c], values[a], f"{phase}:c3")
    c4 = less(values[d], values[b], f"{phase}:c4")
    smallest = c if c3 else a
    largest = b if c4 else d
    unknown_left = a if c3 else c if c4 else b
    unknown_right = d if c4 else b if c3 else c
    c5 = less(
        values[unknown_right],
        values[unknown_left],
        f"{phase}:c5",
    )
    return [
        values[smallest],
        values[unknown_right if c5 else unknown_left],
        values[unknown_left if c5 else unknown_right],
        values[largest],
    ]


def _merge(
    engine: Any, values: list[int], split: int, phase: str
) -> list[int]:
    length = len(values)
    output = [0] * length
    left, right = 0, split
    left_back, right_back = split - 1, length - 1
    front, back = 0, length - 1
    for index in range(split):
        from_left = not engine.is_less(
            values[right],
            values[left],
            f"{phase}:merge-up[{index}]",
        )
        output[front] = values[left if from_left else right]
        left += int(from_left)
        right += int(not from_left)
        front += 1

        from_right = not engine.is_less(
            values[right_back],
            values[left_back],
            f"{phase}:merge-down[{index}]",
        )
        output[back] = values[
            right_back if from_right else left_back
        ]
        right_back -= int(from_right)
        left_back -= int(not from_right)
        back -= 1
    left_end, right_end = left_back + 1, right_back + 1
    if length % 2:
        use_left = left < left_end
        output[front] = values[left if use_left else right]
        left += int(use_left)
        right += int(not use_left)
    if left != left_end or right != right_end:
        raise selection._CallbackPanic("reference:ord-violation")
    return output


def _sort8(
    engine: Any, values: list[int], phase: str
) -> list[int]:
    return _merge(
        engine,
        _sort4(engine, values[:4], f"{phase}:left-sort4")
        + _sort4(engine, values[4:], f"{phase}:right-sort4"),
        4,
        f"{phase}:merge",
    )


NETWORK9 = (
    (0, 3), (1, 7), (2, 5), (4, 8), (0, 7), (2, 4), (3, 8),
    (5, 6), (0, 2), (1, 3), (4, 5), (7, 8), (1, 4), (3, 6),
    (5, 7), (0, 1), (2, 4), (3, 5), (6, 8), (2, 3), (4, 5),
    (6, 7), (1, 2), (3, 4), (5, 6),
)

NETWORK13 = (
    (0, 12), (1, 10), (2, 9), (3, 7), (5, 11), (6, 8),
    (1, 6), (2, 3), (4, 11), (7, 9), (8, 10), (0, 4), (1, 2),
    (3, 6), (7, 8), (9, 10), (11, 12), (4, 6), (5, 9), (8, 11),
    (10, 12), (0, 5), (3, 8), (4, 7), (6, 11), (9, 10), (0, 1),
    (2, 5), (6, 9), (7, 8), (10, 11), (1, 3), (2, 4), (5, 6),
    (9, 10), (1, 2), (3, 4), (5, 7), (6, 8), (2, 3), (4, 5),
    (6, 7), (8, 9), (3, 4), (5, 6),
)


def _network_region(
    engine: Any, start: int, end: int
) -> None:
    length = end - start
    pairs = NETWORK13 if length >= 13 else NETWORK9 if length >= 9 else ()
    presorted = 13 if length >= 13 else 9 if length >= 9 else 1
    phase = (
        "small-sort-network:sort13"
        if length >= 13
        else "small-sort-network:sort9"
    )
    for index, (first, second) in enumerate(pairs):
        first += start
        second += start
        if engine.is_less(
            engine.sequence[second],
            engine.sequence[first],
            f"{phase}[{index}]:compare",
        ):
            engine.swap(first, second, f"{phase}[{index}]:swap")
    selection._insertion_sort_shift_left(
        engine, start, end, presorted
    )


def _small_network(
    engine: Any, start: int, end: int
) -> None:
    length = end - start
    if length < 2:
        return
    half = length // 2
    if length < 18:
        _network_region(engine, start, end)
        return
    _network_region(engine, start, start + half)
    _network_region(engine, start + half, end)
    merged = _merge(
        engine,
        list(engine.sequence[start:end]),
        half,
        "small-sort-network:final-merge",
    )
    engine.sequence[start:end] = merged


def _insert_buffer(
    engine: Any,
    values: list[int],
    begin: int,
    tail: int,
    phase: str,
) -> None:
    saved = values[tail]
    if not engine.is_less(
        saved, values[tail - 1], f"{phase}:initial-compare"
    ):
        return
    scan, hole = tail - 1, tail
    try:
        while True:
            values[hole] = values[scan]
            hole = scan
            if scan == begin:
                break
            scan -= 1
            if not engine.is_less(
                saved,
                values[scan],
                f"{phase}:sift-compare",
            ):
                break
    except selection._CallbackPanic:
        values[hole] = saved
        raise
    values[hole] = saved


def _small_general(
    engine: Any, start: int, end: int
) -> None:
    length = end - start
    if length < 2:
        return
    source = list(engine.sequence[start:end])
    half = length // 2
    scratch: list[int | None] = [None] * length
    if engine.selection_input.configuration.element_size <= 16 and length >= 16:
        scratch[:8] = _sort8(
            engine, source[:8], "small-sort-general:left-sort8"
        )
        scratch[half : half + 8] = _sort8(
            engine,
            source[half : half + 8],
            "small-sort-general:right-sort8",
        )
        presorted = 8
    elif length >= 8:
        scratch[:4] = _sort4(
            engine, source[:4], "small-sort-general:left-sort4"
        )
        scratch[half : half + 4] = _sort4(
            engine,
            source[half : half + 4],
            "small-sort-general:right-sort4",
        )
        presorted = 4
    else:
        scratch[0], scratch[half] = source[0], source[half]
        presorted = 1
    for offset, desired in ((0, half), (half, length - half)):
        for index in range(presorted, desired):
            scratch[offset + index] = source[offset + index]
            buffer = [0 if value is None else value for value in scratch]
            _insert_buffer(
                engine,
                buffer,
                offset,
                offset + index,
                (
                    "small-sort-general:"
                    f"insert-tail[{offset}:{offset + desired}:{index}]"
                ),
            )
            scratch[offset : offset + index + 1] = buffer[
                offset : offset + index + 1
            ]
    if any(value is None for value in scratch):
        raise AssertionError("reference scratch incomplete")
    complete = [int(value) for value in scratch]
    try:
        merged = _merge(
            engine, complete, half, "small-sort-general:final-merge"
        )
    except selection._CallbackPanic:
        engine.sequence[start:end] = complete
        raise
    engine.sequence[start:end] = merged


def _small(engine: Any, configuration: Any, start: int, end: int) -> None:
    kind = _kind(configuration)
    if kind == "fallback":
        if end - start >= 2:
            selection._insertion_sort_shift_left(engine, start, end, 1)
    elif kind == "network":
        _small_network(engine, start, end)
    else:
        _small_general(engine, start, end)


def _sift(
    engine: Any,
    start: int,
    end: int,
    node: int,
    phase: str,
) -> None:
    length = end - start
    while True:
        child = 2 * node + 1
        if child >= length:
            return
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
            return
        engine.swap(
            start + node, start + child, f"{phase}:swap"
        )
        node = child


def _heap(
    engine: Any, start: int, end: int, phase: str
) -> None:
    length = end - start
    for index in range(length + length // 2 - 1, -1, -1):
        if index >= length:
            node = index - length
        else:
            engine.swap(start, start + index, f"{phase}:extract")
            node = 0
        _sift(
            engine,
            start,
            start + min(index, length),
            node,
            f"{phase}:sift-down[{index}]",
        )


def _quick(
    engine: Any,
    configuration: Any,
    start: int,
    end: int,
    ancestor: int | None,
    limit: int,
) -> None:
    while True:
        if end - start <= _threshold(configuration):
            _small(engine, configuration, start, end)
            return
        if limit == 0:
            _heap(engine, start, end, "quicksort:imbalance-fallback")
            return
        limit -= 1
        pivot = selection._choose_pivot(engine, start, end)
        if ancestor is not None and not engine.is_less(
            ancestor,
            engine.sequence[start + pivot],
            "quicksort:ancestor-pivot-compare",
        ):
            equal = selection._partition(
                engine, start, end, pivot, reverse=True
            )
            start += equal + 1
            ancestor = None
            continue
        lower = selection._partition(engine, start, end, pivot)
        pivot_index = start + lower
        pivot_identity = engine.sequence[pivot_index]
        _quick(
            engine,
            configuration,
            start,
            pivot_index,
            ancestor,
            limit,
        )
        start = pivot_index + 1
        ancestor = pivot_identity


def execute(
    initial_sequence: tuple[int, ...],
    configuration: Any,
    boundary: Any,
) -> ReferenceExecution:
    engine = _engine(initial_sequence, configuration, boundary)
    status = NORMAL
    try:
        length = len(engine.sequence)
        if configuration.element_size == 0 or length < 2:
            pass
        elif (
            configuration.optimize_for_size
            or configuration.target_pointer_width == 16
        ):
            _heap(engine, 0, length, "sort:configuration-heapsort")
        elif length <= MAX_LEN_ALWAYS_INSERTION_SORT:
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
                _quick(engine, configuration, 0, length, None, limit)
    except selection._CallbackPanic:
        status = PANIC
    except _Abort:
        status = ABORT
    return ReferenceExecution(
        sequence=tuple(engine.sequence),
        callback_state=engine.callback_state,
        terminal_status=status,
        panicked=status == PANIC,
        aborted=status == ABORT,
        terminal=True,
        unit_returned=status == NORMAL,
        events=tuple(engine.events),
    )
