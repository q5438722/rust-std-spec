#!/usr/bin/env python3
"""Replayable source-path and correspondence witnesses for target 080."""

from __future__ import annotations

import random
from dataclasses import asdict
from functools import cache
from typing import Any

import target_078_operational_v1 as accepted_selection
import target_080_operational_v1 as model
import target_080_source_interpreter_v1 as reference


def _permutation(length: int, seed: int) -> tuple[int, ...]:
    values = list(range(length))
    random.Random(seed).shuffle(values)
    return tuple(values)


def _configuration(**overrides: Any) -> model.SourceConfiguration:
    return model.SourceConfiguration(**overrides)


def _configuration_record(
    configuration: model.SourceConfiguration,
) -> dict[str, Any]:
    return asdict(configuration)


def _boundary_record(boundary: model.OrdBoundary) -> dict[str, Any]:
    return {
        "callback_identity": boundary.callback_identity,
        "initial_state": boundary.initial_state,
        "result_mode": boundary.result_mode,
        "next_state_mode": boundary.next_state_mode,
        "contract_result_mode": boundary.contract_result_mode,
        "rank_pairs": [list(pair) for pair in boundary.rank_pairs],
        "affine_multiplier": boundary.affine_multiplier,
        "affine_offset": boundary.affine_offset,
        "panic_states": sorted(boundary.panic_states),
        "panic_keys": [
            asdict(key) for key in sorted(boundary.panic_keys)
        ],
    }


def boundary_from_record(record: dict[str, Any]) -> model.OrdBoundary:
    return model.OrdBoundary(
        callback_identity=record["callback_identity"],
        initial_state=record["initial_state"],
        result_mode=record["result_mode"],
        next_state_mode=record["next_state_mode"],
        contract_result_mode=record["contract_result_mode"],
        rank_pairs=tuple(tuple(pair) for pair in record["rank_pairs"]),
        affine_multiplier=record["affine_multiplier"],
        affine_offset=record["affine_offset"],
        panic_states=frozenset(record["panic_states"]),
        panic_keys=frozenset(
            model.ObservationKey(**key) for key in record["panic_keys"]
        ),
    )


def configuration_from_record(
    record: dict[str, Any],
) -> model.SourceConfiguration:
    return model.SourceConfiguration(**record)


def _primary_callback_schedule(
    steps: tuple[model.DerivedStep, ...],
) -> list[dict[str, Any]]:
    return [
        {
            "phase": step.phase,
            "state": step.detail("state"),
            "left_identity": step.detail("left_identity"),
            "right_identity": step.detail("right_identity"),
            "is_less": step.detail("is_less"),
            "next_state": step.detail("next_state"),
            "panicked": step.detail("panicked"),
        }
        for step in steps
        if step.kind == "ord-lt"
    ]


def _reference_callback_schedule(
    events: tuple[accepted_selection.DerivedEvent, ...],
) -> list[dict[str, Any]]:
    return [
        {
            "phase": event.phase,
            "state": event.detail("state"),
            "left_identity": event.detail("left_identity"),
            "right_identity": event.detail("right_identity"),
            "is_less": event.detail("ordering")
            == accepted_selection.LESS,
            "next_state": event.detail("next_state"),
            "panicked": event.detail("panicked"),
        }
        for event in events
        if event.kind == "callback"
    ]


def _primary_direct(
    action: str,
    sequence: tuple[int, ...],
    configuration: model.SourceConfiguration,
    boundary: model.OrdBoundary,
    parameters: dict[str, Any],
) -> tuple[model.Execution, int | None]:
    engine = model._Engine(model.SortInput(sequence, configuration), boundary)
    returned_index: int | None = None
    try:
        if action == "choose-pivot":
            returned_index = model._choose_pivot(
                engine,
                parameters.get("start", 0),
                parameters.get("end", len(sequence)),
            )
        elif action == "partition":
            returned_index = model._partition(
                engine,
                parameters.get("start", 0),
                parameters.get("end", len(sequence)),
                parameters["pivot"],
                reverse=parameters.get("reverse", False),
            )
        elif action == "quicksort":
            model._quicksort(
                engine,
                parameters.get("start", 0),
                parameters.get("end", len(sequence)),
                parameters.get("ancestor"),
                parameters["limit"],
            )
        elif action == "quicksort-partition":
            start = parameters.get("start", 0)
            end = parameters.get("end", len(sequence))
            ancestor = parameters.get("ancestor")
            limit = parameters["limit"]
            count_less = model._partition(
                engine,
                start,
                end,
                parameters["pivot_position"],
            )
            pivot_index = start + count_less
            pivot_identity = engine.sequence[pivot_index]
            model._quicksort(
                engine,
                start,
                pivot_index,
                ancestor,
                limit,
            )
            model._quicksort(
                engine,
                pivot_index + 1,
                end,
                pivot_identity,
                limit,
            )
        elif action == "small-sort":
            model._small_sort(
                engine,
                parameters.get("start", 0),
                parameters.get("end", len(sequence)),
            )
        elif action == "heapsort":
            model._heapsort(
                engine,
                parameters.get("start", 0),
                parameters.get("end", len(sequence)),
                "witness:direct-heapsort",
            )
        else:
            raise ValueError(f"unsupported direct action: {action}")
        return engine.finish(model.NORMAL), returned_index
    except model._OrdPanic as panic:
        return (
            engine.finish(model.PANIC, panic_phase=panic.phase),
            returned_index,
        )
    except model._SourceAbort as abort:
        return (
            engine.finish(model.ABORT, abort_phase=abort.phase),
            returned_index,
        )


def _reference_direct(
    action: str,
    sequence: tuple[int, ...],
    configuration: model.SourceConfiguration,
    boundary: model.OrdBoundary,
    parameters: dict[str, Any],
) -> tuple[reference.ReferenceExecution, int | None]:
    engine = reference._engine(sequence, configuration, boundary)
    returned_index: int | None = None
    status = model.NORMAL
    try:
        if action == "choose-pivot":
            returned_index = accepted_selection._choose_pivot(
                engine,
                parameters.get("start", 0),
                parameters.get("end", len(sequence)),
            )
        elif action == "partition":
            returned_index = accepted_selection._partition(
                engine,
                parameters.get("start", 0),
                parameters.get("end", len(sequence)),
                parameters["pivot"],
                reverse=parameters.get("reverse", False),
            ) if sequence else 0
        elif action == "quicksort":
            reference._quick(
                engine,
                configuration,
                parameters.get("start", 0),
                parameters.get("end", len(sequence)),
                parameters.get("ancestor"),
                parameters["limit"],
            )
        elif action == "quicksort-partition":
            start = parameters.get("start", 0)
            end = parameters.get("end", len(sequence))
            ancestor = parameters.get("ancestor")
            limit = parameters["limit"]
            count_less = accepted_selection._partition(
                engine,
                start,
                end,
                parameters["pivot_position"],
            )
            pivot_index = start + count_less
            pivot_identity = engine.sequence[pivot_index]
            reference._quick(
                engine,
                configuration,
                start,
                pivot_index,
                ancestor,
                limit,
            )
            reference._quick(
                engine,
                configuration,
                pivot_index + 1,
                end,
                pivot_identity,
                limit,
            )
        elif action == "small-sort":
            reference._small(
                engine,
                configuration,
                parameters.get("start", 0),
                parameters.get("end", len(sequence)),
            )
        elif action == "heapsort":
            reference._heap(
                engine,
                parameters.get("start", 0),
                parameters.get("end", len(sequence)),
                "witness:direct-heapsort",
            )
        else:
            raise ValueError(f"unsupported direct action: {action}")
    except accepted_selection._CallbackPanic:
        status = model.PANIC
    except reference._Abort:
        status = model.ABORT
    return (
        reference.ReferenceExecution(
            sequence=tuple(engine.sequence),
            callback_state=engine.callback_state,
            terminal_status=status,
            panicked=status == model.PANIC,
            aborted=status == model.ABORT,
            terminal=True,
            unit_returned=status == model.NORMAL,
            events=tuple(engine.events),
        ),
        returned_index,
    )


def execute_spec(
    spec: dict[str, Any],
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    tuple[model.DerivedStep, ...],
    dict[str, Any],
]:
    sequence = tuple(spec["sequence"])
    configuration = configuration_from_record(spec["configuration"])
    boundary = boundary_from_record(spec["boundary"])
    action = spec["action"]
    parameters = dict(spec.get("parameters", {}))
    if action == "sort":
        primary = model.execute(
            model.SortInput(sequence, configuration), boundary
        )
        secondary = reference.execute(sequence, configuration, boundary)
        primary_index = secondary_index = None
    else:
        primary, primary_index = _primary_direct(
            action, sequence, configuration, boundary, parameters
        )
        secondary, secondary_index = _reference_direct(
            action, sequence, configuration, boundary, parameters
        )
    primary_record = {
        "sequence": list(primary.state.sequence),
        "callback_state": primary.state.callback_state,
        "terminal_status": primary.terminal_status,
        "panicked": primary.state.panicked,
        "aborted": primary.state.aborted,
        "terminal": primary.state.terminal,
        "unit_returned": primary.unit_returned,
        "returned_index": primary_index,
    }
    secondary_record = {
        "sequence": list(secondary.sequence),
        "callback_state": secondary.callback_state,
        "terminal_status": secondary.terminal_status,
        "panicked": secondary.panicked,
        "aborted": secondary.aborted,
        "terminal": secondary.terminal,
        "unit_returned": secondary.unit_returned,
        "returned_index": secondary_index,
    }
    primary_schedule = _primary_callback_schedule(primary.derived_steps)
    reference_schedule = _reference_callback_schedule(secondary.events)
    correspondence = {
        "callback_schedule_equal": primary_schedule == reference_schedule,
        "callback_count": len(primary_schedule),
        "callback_schedule": primary_schedule,
        "phase_sequence": [
            observation["phase"] for observation in primary_schedule
        ],
    }
    return (
        primary_record,
        secondary_record,
        primary.derived_steps,
        correspondence,
    )


def _spec(
    name: str,
    sequence: tuple[int, ...],
    configuration: model.SourceConfiguration,
    boundary: model.OrdBoundary,
    *,
    action: str = "sort",
    parameters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "name": name,
        "action": action,
        "sequence": list(sequence),
        "configuration": _configuration_record(configuration),
        "boundary": _boundary_record(boundary),
        "parameters": parameters or {},
    }


def _panic_state_after(
    spec: dict[str, Any],
    *,
    phase_contains: str | None = None,
    event_before: str | None = None,
    occurrence: int = 0,
) -> int:
    _, _, steps, _ = execute_spec(spec)
    seen_event = event_before is None
    matches: list[int] = []
    for step in steps:
        if step.kind == event_before:
            seen_event = True
            continue
        if (
            seen_event
            and step.kind == "ord-lt"
            and (
                phase_contains is None
                or phase_contains in step.phase
            )
        ):
            matches.append(step.detail("state"))
    if occurrence >= len(matches):
        raise RuntimeError(
            f"{spec['name']}: no callback state for {phase_contains!r}"
        )
    return matches[occurrence]


def _with_panic(
    spec: dict[str, Any], name: str, state: int
) -> dict[str, Any]:
    changed = {
        key: value
        for key, value in spec.items()
        if key != "boundary"
    }
    boundary = dict(spec["boundary"])
    boundary["panic_states"] = [state]
    changed["boundary"] = boundary
    changed["name"] = name
    return changed


def _with_panic_key(
    spec: dict[str, Any],
    name: str,
    *,
    phase_contains: str,
    derivation_spec: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _, _, steps, _ = execute_spec(derivation_spec or spec)
    key = next(
        (
            {
                "state": step.detail("state"),
                "left_identity": step.detail("left_identity"),
                "right_identity": step.detail("right_identity"),
            }
            for step in steps
            if step.kind == "ord-lt"
            and phase_contains in step.phase
        ),
        None,
    )
    if key is None:
        raise RuntimeError(
            f"{spec['name']}: no callback key for {phase_contains!r}"
        )
    changed = {
        field: value
        for field, value in spec.items()
        if field != "boundary"
    }
    boundary = dict(spec["boundary"])
    boundary["panic_keys"] = [key]
    changed["boundary"] = boundary
    changed["name"] = name
    return changed


@cache
def witness_specs() -> tuple[dict[str, Any], ...]:
    identity = model.integer_total_order_boundary()
    default = _configuration()
    network = _configuration(is_freeze=True, is_copy=True)
    general = _configuration(
        element_size=24,
        is_freeze=True,
        is_copy=True,
        has_efficient_in_place_swap=False,
    )
    hoare = _configuration(element_size=128)
    cyclic_one = _configuration(element_size=32)

    base = [
        _spec(
            "zst-return",
            (3, 2, 1),
            _configuration(element_size=0),
            identity,
        ),
        _spec("trivial-return", (7,), default, identity),
        _spec("normal-insertion", (4, 1, 3, 2), default, identity),
        _spec(
            "ascending-existing-run",
            tuple(range(21)),
            default,
            identity,
        ),
        _spec(
            "descending-existing-run",
            tuple(range(20, -1, -1)),
            default,
            identity,
        ),
        _spec(
            "configuration-heapsort-size",
            _permutation(25, 8001),
            _configuration(optimize_for_size=True),
            identity,
        ),
        _spec(
            "configuration-heapsort-16-bit",
            _permutation(25, 8002),
            _configuration(target_pointer_width=16),
            identity,
        ),
        _spec(
            "fallback-small-sort-and-recursion",
            _permutation(45, 8003),
            default,
            identity,
        ),
        _spec(
            "network-small-sort-sort13-merge",
            _permutation(26, 8004),
            network,
            identity,
        ),
        _spec(
            "general-small-sort-scratch-merge",
            _permutation(26, 8005),
            general,
            identity,
        ),
        _spec(
            "general-small-sort-sort8-direct",
            _permutation(16, 8013),
            _configuration(element_size=8, is_freeze=True),
            identity,
            action="small-sort",
        ),
        _spec(
            "network-small-sort-sort9-direct",
            _permutation(9, 8014),
            network,
            identity,
            action="small-sort",
        ),
        _spec(
            "general-small-sort-presorted-one-direct",
            _permutation(6, 8015),
            general,
            identity,
            action="small-sort",
        ),
        _spec(
            "recursive-pivot",
            _permutation(80, 8006),
            default,
            identity,
        ),
        _spec(
            "hoare-partition",
            _permutation(45, 8007),
            hoare,
            identity,
        ),
        _spec(
            "cyclic-unroll-one-partition",
            _permutation(45, 8008),
            cyclic_one,
            identity,
        ),
        _spec(
            "lomuto-simple-direct",
            _permutation(17, 8009),
            _configuration(optimize_for_size=True),
            identity,
            action="partition",
            parameters={"pivot": 4},
        ),
        _spec(
            "imbalance-fallback-direct",
            _permutation(40, 8010),
            default,
            identity,
            action="quicksort",
            parameters={"limit": 0},
        ),
    ]

    duplicate_sequence = _permutation(80, 0)
    base.append(
        _spec(
            "duplicate-class-ancestor-pivot",
            duplicate_sequence,
            default,
            model.rank_total_order_boundary(
                {identity: identity % 6 for identity in duplicate_sequence}
            ),
        )
    )

    by_name = {spec["name"]: spec for spec in base}
    panic_specs = [
        _with_panic(
            by_name["normal-insertion"],
            "insertion-copy-on-drop-panic",
            2,
        ),
        _with_panic(
            by_name["configuration-heapsort-size"],
            "heapsort-child-selection-panic",
            _panic_state_after(
                by_name["configuration-heapsort-size"],
                phase_contains="choose-greater-child",
            ),
        ),
        _with_panic(
            by_name["general-small-sort-scratch-merge"],
            "general-small-sort-merge-restoration",
            _panic_state_after(
                by_name["general-small-sort-scratch-merge"],
                phase_contains="small-sort-general:final-merge",
            ),
        ),
        _with_panic(
            by_name["general-small-sort-scratch-merge"],
            "general-small-sort-scratch-unwind-restoration",
            _panic_state_after(
                by_name["general-small-sort-scratch-merge"],
                phase_contains="small-sort-general:insert-tail",
                occurrence=2,
            ),
        ),
        _with_panic(
            by_name["network-small-sort-sort13-merge"],
            "network-small-sort-merge-panic",
            _panic_state_after(
                by_name["network-small-sort-sort13-merge"],
                phase_contains="small-sort-network:final-merge",
            ),
        ),
        _with_panic(
            by_name["recursive-pivot"],
            "recursive-pivot-panic",
            _panic_state_after(
                by_name["recursive-pivot"],
                phase_contains="choose-pivot:median3-rec",
            ),
        ),
        _with_panic(
            by_name["duplicate-class-ancestor-pivot"],
            "ancestor-pivot-panic",
            _panic_state_after(
                by_name["duplicate-class-ancestor-pivot"],
                phase_contains="ancestor-pivot-compare",
            ),
        ),
    ]

    cyclic_direct = _spec(
        "cyclic-guard-base",
        _permutation(17, 8011),
        default,
        identity,
        action="partition",
        parameters={"pivot": 4},
    )
    panic_specs.append(
        _with_panic(
            cyclic_direct,
            "cyclic-gap-guard-restoration",
            _panic_state_after(
                cyclic_direct,
                phase_contains="partition-lomuto-cyclic:compare",
                event_before="partition-cycle",
            ),
        )
    )
    hoare_direct = _spec(
        "hoare-guard-base",
        _permutation(17, 8012),
        hoare,
        identity,
        action="partition",
        parameters={"pivot": 4},
    )
    panic_specs.append(
        _with_panic(
            hoare_direct,
            "hoare-gap-guard-restoration",
            _panic_state_after(
                hoare_direct,
                phase_contains="partition-hoare",
                event_before="partition-cycle",
            ),
        )
    )
    return tuple(base + panic_specs)


@cache
def forcing_specs() -> dict[str, dict[str, Any]]:
    """Small source-derived instances used only for bounded SAT checks."""
    identity = model.integer_total_order_boundary()
    default = _configuration()
    general = _configuration(
        element_size=24,
        is_freeze=True,
        is_copy=True,
        has_efficient_in_place_swap=False,
    )
    network = _configuration(is_freeze=True, is_copy=True)
    panic_first = _with_panic(
        _spec(
            "forcing-panic-unwind-base",
            (1, 0),
            default,
            identity,
        ),
        "forcing-panic-unwind",
        0,
    )
    threshold_base = _spec(
        "forcing-threshold-dispatch-base",
        _permutation(26, 9001),
        network,
        identity,
        action="quicksort",
        parameters={"limit": 1},
    )
    threshold_pivot = _spec(
        "forcing-threshold-pivot-derivation",
        tuple(threshold_base["sequence"]),
        network,
        identity,
        action="choose-pivot",
    )
    imbalance_base = _spec(
        "forcing-imbalance-limit-base",
        _permutation(17, 9003),
        default,
        identity,
        action="quicksort",
        parameters={"limit": 0},
    )
    imbalance_pivot = _spec(
        "forcing-imbalance-pivot-derivation",
        tuple(imbalance_base["sequence"]),
        default,
        identity,
        action="choose-pivot",
    )
    return {
        "nonvacuity": _spec(
            "forcing-nonvacuity",
            (1, 0),
            default,
            identity,
        ),
        "threshold-dispatch": _with_panic_key(
            threshold_base,
            "forcing-threshold-dispatch",
            phase_contains="choose-pivot",
            derivation_spec=threshold_pivot,
        ),
        "comparison-operands": _spec(
            "forcing-comparison-operands",
            (1, 0),
            default,
            identity,
        ),
        "callback-next-state": _spec(
            "forcing-callback-next-state",
            (4, 1, 3, 2),
            default,
            identity,
        ),
        "descending-reversal": _spec(
            "forcing-descending-reversal",
            tuple(range(20, -1, -1)),
            default,
            identity,
        ),
        "pivot-selection": _spec(
            "forcing-pivot-selection",
            _permutation(8, 9002),
            default,
            identity,
            action="choose-pivot",
        ),
        "partition-behavior": _spec(
            "forcing-partition-behavior",
            (4, 1, 3, 0, 2),
            default,
            identity,
            action="partition",
            parameters={"pivot": 2},
        ),
        "recursive-left-window": _spec(
            "forcing-recursive-left-window",
            (4, 1, 3, 0, 2),
            default,
            identity,
            action="quicksort-partition",
            parameters={"limit": 1, "pivot_position": 2},
        ),
        "iterative-right-window": _spec(
            "forcing-iterative-right-window",
            (4, 1, 3, 0, 2),
            default,
            identity,
            action="quicksort-partition",
            parameters={"limit": 1, "pivot_position": 2},
        ),
        "imbalance-limit": _with_panic_key(
            imbalance_base,
            "forcing-imbalance-limit",
            phase_contains="choose-pivot",
            derivation_spec=imbalance_pivot,
        ),
        "small-sort-selection": _spec(
            "forcing-small-sort-selection",
            _permutation(9, 9004),
            general,
            identity,
            action="small-sort",
        ),
        "heap-child-selection": _spec(
            "forcing-heap-child-selection",
            (0, 1, 2),
            default,
            identity,
            action="heapsort",
        ),
        "heap-swap": _spec(
            "forcing-heap-swap",
            (1, 0),
            default,
            identity,
            action="heapsort",
        ),
        "copy-on-drop-restoration": _with_panic(
            _spec(
                "forcing-copy-on-drop-base",
                (4, 1, 3, 2),
                default,
                identity,
            ),
            "forcing-copy-on-drop-restoration",
            2,
        ),
        "gap-guard-restoration": _with_panic(
            _spec(
                "forcing-gap-guard-base",
                _permutation(17, 8012),
                _configuration(element_size=128),
                identity,
                action="partition",
                parameters={"pivot": 4},
            ),
            "forcing-gap-guard-restoration",
            _panic_state_after(
                _spec(
                    "forcing-gap-guard-derivation",
                    _permutation(17, 8012),
                    _configuration(element_size=128),
                    identity,
                    action="partition",
                    parameters={"pivot": 4},
                ),
                phase_contains="partition-hoare",
                event_before="partition-cycle",
            ),
        ),
        "panic-unwind": panic_first,
    }


@cache
def witness_payload() -> dict[str, Any]:
    cases: dict[str, Any] = {}
    for spec in witness_specs():
        primary, secondary, steps, correspondence = execute_spec(spec)
        if primary != secondary or not correspondence[
            "callback_schedule_equal"
        ]:
            raise RuntimeError(
                f"{spec['name']}: independent interpreter mismatch"
            )
        cases[spec["name"]] = {
            "spec": spec,
            "expected": primary,
            "source_step_kinds": sorted({step.kind for step in steps}),
            "source_phases": sorted({step.phase for step in steps}),
            "callback_correspondence": correspondence,
        }
    return {
        "schema_version": 1,
        "target": model.TARGET,
        "model_id": model.MODEL_ID,
        "correspondence_fields": [
            "full final sequence",
            "callback-visible state",
            "panic status",
            "abort status",
            "terminal status",
            "unit return",
            "direct helper return index when applicable",
        ],
        "cases": cases,
    }
