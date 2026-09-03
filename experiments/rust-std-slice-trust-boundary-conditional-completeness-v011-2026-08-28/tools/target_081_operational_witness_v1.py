#!/usr/bin/env python3
"""Paired source-path witnesses for target 081 operational v1."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from functools import cache
from typing import Any

import target_080_operational_witness_v1 as accepted_witnesses
import target_081_operational_v1 as model
import target_081_source_interpreter_v1 as reference


def configuration_record(
    configuration: model.SourceConfiguration,
) -> dict[str, Any]:
    return asdict(configuration)


def boundary_record(
    boundary: model.ComparatorBoundary,
) -> dict[str, Any]:
    record = asdict(boundary)
    record["panic_states"] = sorted(boundary.panic_states)
    record["panic_keys"] = [
        asdict(key) for key in sorted(boundary.panic_keys)
    ]
    record["drop_panic_normal_states"] = sorted(
        boundary.drop_panic_normal_states
    )
    record["drop_panic_unwind_states"] = sorted(
        boundary.drop_panic_unwind_states
    )
    record["rank_pairs"] = [list(pair) for pair in boundary.rank_pairs]
    record["explicit_orderings"] = [
        list(item) for item in boundary.explicit_orderings
    ]
    record["initial_observable_element_state"] = list(
        boundary.initial_observable_element_state
    )
    return record


def boundary_from_record(
    record: dict[str, Any],
) -> model.ComparatorBoundary:
    return model.ComparatorBoundary(
        callback_identity=record["callback_identity"],
        initial_state=record["initial_state"],
        ordering_mode=record["ordering_mode"],
        next_state_mode=record["next_state_mode"],
        contract_ordering_mode=record["contract_ordering_mode"],
        initial_observable_element_state=tuple(
            record["initial_observable_element_state"]
        ),
        interior_next_state_mode=record["interior_next_state_mode"],
        interior_affine_multiplier=record[
            "interior_affine_multiplier"
        ],
        interior_affine_offset=record["interior_affine_offset"],
        rank_pairs=tuple(tuple(pair) for pair in record["rank_pairs"]),
        explicit_orderings=tuple(
            tuple(item) for item in record["explicit_orderings"]
        ),
        affine_multiplier=record["affine_multiplier"],
        affine_offset=record["affine_offset"],
        panic_states=frozenset(record["panic_states"]),
        panic_keys=frozenset(
            model.ObservationKey(**item) for item in record["panic_keys"]
        ),
        drop_next_state_mode=record["drop_next_state_mode"],
        drop_affine_multiplier=record["drop_affine_multiplier"],
        drop_affine_offset=record["drop_affine_offset"],
        drop_interior_next_state_mode=record[
            "drop_interior_next_state_mode"
        ],
        drop_interior_affine_multiplier=record[
            "drop_interior_affine_multiplier"
        ],
        drop_interior_affine_offset=record[
            "drop_interior_affine_offset"
        ],
        drop_panic_normal_states=frozenset(
            record["drop_panic_normal_states"]
        ),
        drop_panic_unwind_states=frozenset(
            record["drop_panic_unwind_states"]
        ),
    )


def _accepted_boundary(record: dict[str, Any]) -> model.ComparatorBoundary:
    common = {
        "initial_state": record["initial_state"],
        "next_state_mode": record["next_state_mode"],
        "affine_multiplier": record["affine_multiplier"],
        "affine_offset": record["affine_offset"],
        "panic_states": frozenset(record["panic_states"]),
        "panic_keys": frozenset(
            model.ObservationKey(**item) for item in record["panic_keys"]
        ),
    }
    if record["result_mode"] == model.IDENTITY_TOTAL_ORDER:
        return model.integer_total_order_boundary(**common)
    if record["result_mode"] == model.RANK_TOTAL_ORDER:
        return model.rank_total_order_boundary(
            dict(record["rank_pairs"]), **common
        )
    if record["result_mode"] == model.CONSTANT_EQUAL:
        boundary = model.integer_total_order_boundary(**common)
        return model.ComparatorBoundary(
            **{
                **boundary.__dict__,
                "ordering_mode": model.CONSTANT_EQUAL,
                "contract_ordering_mode": model.CONSTANT_EQUAL,
            }
        )
    raise ValueError(
        f"unsupported accepted boundary mode: {record['result_mode']}"
    )


def _spec(
    name: str,
    sequence: tuple[int, ...],
    configuration: model.SourceConfiguration,
    boundary: model.ComparatorBoundary,
    *,
    source_case: str,
) -> dict[str, Any]:
    return {
        "name": name,
        "action": "sort",
        "sequence": list(sequence),
        "configuration": configuration_record(configuration),
        "boundary": boundary_record(boundary),
        "source_case": source_case,
    }


def _inherited_public_specs() -> list[dict[str, Any]]:
    payload = accepted_witnesses.witness_payload()
    specs = []
    for name, case in payload["cases"].items():
        accepted = case["spec"]
        if accepted["action"] != "sort":
            continue
        specs.append(
            _spec(
                f"inherited-{name}",
                tuple(accepted["sequence"]),
                model.SourceConfiguration(**accepted["configuration"]),
                _accepted_boundary(accepted["boundary"]),
                source_case=name,
            )
        )
    return specs


def _explicit(
    values: dict[tuple[int, int], int],
    **kwargs: Any,
) -> model.ComparatorBoundary:
    return model.explicit_ordering_boundary(values, **kwargs)


@cache
def witness_specs() -> tuple[dict[str, Any], ...]:
    cycle = {
        (0, 0): model.EQUAL,
        (1, 1): model.EQUAL,
        (2, 2): model.EQUAL,
        (0, 1): model.LESS,
        (1, 0): model.GREATER,
        (1, 2): model.LESS,
        (2, 1): model.GREATER,
        (2, 0): model.LESS,
        (0, 2): model.GREATER,
    }
    both_less = {
        (0, 0): model.EQUAL,
        (1, 1): model.EQUAL,
        (2, 2): model.EQUAL,
        (0, 1): model.LESS,
        (1, 0): model.LESS,
    }
    extras = [
        _spec(
            "duplicate-equal-key-total-order",
            (4, 1, 3, 2, 0),
            model.SourceConfiguration(),
            model.rank_total_order_boundary(
                {0: 0, 1: 0, 2: 1, 3: 1, 4: 2}
            ),
            source_case="target-081-extra",
        ),
        _spec(
            "documented-non-total-cycle",
            (2, 1, 0, 2, 1, 0),
            model.SourceConfiguration(),
            _explicit(cycle),
            source_case="target-081-extra",
        ),
        _spec(
            "non-total-both-less",
            (2, 1, 0),
            model.SourceConfiguration(),
            _explicit(both_less),
            source_case="target-081-extra",
        ),
        _spec(
            "callback-state-affine",
            (5, 3, 4, 1, 2, 0),
            model.SourceConfiguration(),
            model.integer_total_order_boundary(
                initial_state=2,
                next_state_mode=model.AFFINE_STATE,
                affine_multiplier=2,
                affine_offset=1,
                drop_next_state_mode=model.AFFINE_STATE,
                drop_affine_multiplier=3,
                drop_affine_offset=2,
            ),
            source_case="target-081-extra",
        ),
        _spec(
            "state-dependent-callback-result",
            (4, 3, 2, 1, 0),
            model.SourceConfiguration(),
            model.state_dependent_boundary({value: value for value in range(5)}),
            source_case="target-081-extra",
        ),
        _spec(
            "observable-interior-mutation-normal",
            (5, 3, 4, 1, 2, 0),
            model.SourceConfiguration(),
            model.integer_total_order_boundary(
                initial_observable_element_state=(2, 4, 6, 8, 10, 12),
                interior_next_state_mode=model.AFFINE_STATE,
                interior_affine_multiplier=2,
                interior_affine_offset=1,
                drop_interior_next_state_mode=model.INCREMENT_STATE,
            ),
            source_case="target-081-extra",
        ),
        _spec(
            "observable-interior-mutation-before-panic",
            (3, 2, 1, 0),
            model.SourceConfiguration(),
            model.interior_state_dependent_boundary(
                {value: value for value in range(4)},
                initial_observable_element_state=(1, 3, 5, 7),
                interior_next_state_mode=model.INCREMENT_STATE,
                panic_states=frozenset({0}),
                drop_interior_next_state_mode=model.AFFINE_STATE,
                drop_interior_affine_multiplier=3,
                drop_interior_affine_offset=2,
            ),
            source_case="target-081-extra",
        ),
        _spec(
            "normal-callback-drop-panic",
            (),
            model.SourceConfiguration(),
            model.integer_total_order_boundary(
                initial_state=7,
                drop_panic_normal_states=frozenset({7}),
            ),
            source_case="target-081-extra",
        ),
        _spec(
            "comparator-panic-drop-completes",
            (3, 2, 1, 0),
            model.SourceConfiguration(),
            model.integer_total_order_boundary(
                panic_states=frozenset({0}),
                drop_next_state_mode=model.INCREMENT_STATE,
            ),
            source_case="target-081-extra",
        ),
        _spec(
            "comparator-panic-drop-double-panic-abort",
            (3, 2, 1, 0),
            model.SourceConfiguration(),
            model.integer_total_order_boundary(
                panic_states=frozenset({0}),
                drop_next_state_mode=model.INCREMENT_STATE,
                drop_panic_unwind_states=frozenset({1}),
            ),
            source_case="target-081-extra",
        ),
    ]
    return tuple(_inherited_public_specs() + extras)


def _record(execution: Any) -> dict[str, Any]:
    return {
        "sequence": list(execution.state.sequence),
        "callback_state": execution.state.callback_state,
        "observable_element_state": list(
            execution.state.observable_element_state
        ),
        "terminal_status": execution.terminal_status,
        "panicked": execution.state.panicked,
        "aborted": execution.state.aborted,
        "terminal": execution.state.terminal,
        "unit_returned": execution.unit_returned,
        "private_terminal_status": execution.private_terminal_status,
        "panic_phase": execution.panic_phase,
        "abort_phase": execution.abort_phase,
        "callback_drop_invoked": execution.state.callback_drop_invoked,
        "callback_drop_completed": execution.state.callback_drop_completed,
        "adapter_evaluation_count": len(execution.adapter_events),
        "comparator_observation": [
            list(item) for item in execution.comparator_observation
        ],
    }


def execute_spec(
    spec: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    sequence = tuple(spec["sequence"])
    configuration = model.SourceConfiguration(**spec["configuration"])
    boundary = boundary_from_record(spec["boundary"])
    primary = model.execute(model.SortInput(sequence, configuration), boundary)
    secondary = reference.execute(sequence, configuration, boundary)
    primary_record = _record(primary)
    secondary_record = _record(secondary)
    primary_schedule = [asdict(event) for event in primary.adapter_events]
    secondary_schedule = [asdict(event) for event in secondary.adapter_events]
    correspondence = {
        "field_complete": primary_record == secondary_record,
        "adapter_schedule_equal": primary_schedule == secondary_schedule,
        "observable_interior_state_equal": (
            primary.state.observable_element_state
            == secondary.state.observable_element_state
        ),
        "adapter_evaluations_are_single": all(
            event["callback_evaluations"] == 1
            for event in primary_schedule + secondary_schedule
        ),
        "comparison_count": len(primary_schedule),
        "private_primary_step_count": len(primary.private_steps),
        "private_reference_event_count": len(secondary.private_events),
        "permutation_retained": (
            Counter(primary.state.sequence) == Counter(sequence)
            and Counter(secondary.state.sequence) == Counter(sequence)
        ),
    }
    return primary_record, secondary_record, correspondence


def _is_total_order(
    boundary: model.ComparatorBoundary, sequence: tuple[int, ...]
) -> bool:
    domain = tuple(sorted(set(sequence)))
    if not boundary.contract_admissible():
        return False
    ordering = boundary.contract_ordering
    if any(ordering(value, value) != model.EQUAL for value in domain):
        return False
    for left in domain:
        for right in domain:
            if ordering(left, right) != -ordering(right, left):
                return False
    for left in domain:
        for middle in domain:
            for right in domain:
                if (
                    ordering(left, middle) <= model.EQUAL
                    and ordering(middle, right) <= model.EQUAL
                    and ordering(left, right) > model.EQUAL
                ):
                    return False
    return True


@cache
def witness_payload() -> dict[str, Any]:
    cases: dict[str, Any] = {}
    for spec in witness_specs():
        primary, secondary, correspondence = execute_spec(spec)
        if not correspondence["field_complete"]:
            raise RuntimeError(f"{spec['name']}: result correspondence failed")
        if not correspondence["adapter_schedule_equal"]:
            raise RuntimeError(f"{spec['name']}: callback schedule diverged")
        if not correspondence["adapter_evaluations_are_single"]:
            raise RuntimeError(f"{spec['name']}: callback was evaluated twice")
        if not correspondence["observable_interior_state_equal"]:
            raise RuntimeError(
                f"{spec['name']}: observable interior state diverged"
            )
        if not correspondence["permutation_retained"]:
            raise RuntimeError(f"{spec['name']}: source restoration failed")
        boundary = boundary_from_record(spec["boundary"])
        sequence = tuple(spec["sequence"])
        cases[spec["name"]] = {
            "spec": spec,
            "primary": primary,
            "independent": secondary,
            "correspondence": correspondence,
            "boundary_total_order": _is_total_order(boundary, sequence),
            "contract_projection_available": boundary.contract_admissible(),
        }
    return {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "private_source_model": (
            "accepted target-080 Rust 1.96 private-sort transition"
        ),
        "independent_private_interpreter": (
            "accepted target-080 Rust 1.96 independent interpreter"
        ),
        "case_count": len(cases),
        "cases": cases,
    }


def operational_specs() -> tuple[dict[str, Any], ...]:
    return witness_specs()
