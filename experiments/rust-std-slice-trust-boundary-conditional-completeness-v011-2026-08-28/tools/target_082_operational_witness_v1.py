#!/usr/bin/env python3
"""Paired source-path witnesses for target 082 operational v1."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from functools import cache
from typing import Any

import target_080_operational_v1 as accepted_private
import target_080_operational_witness_v1 as accepted_witnesses
import target_082_operational_v1 as model
import target_082_source_interpreter_v1 as reference


def configuration_record(
    configuration: model.SourceConfiguration,
) -> dict[str, Any]:
    return asdict(configuration)


def boundary_record(boundary: model.KeySortBoundary) -> dict[str, Any]:
    record = asdict(boundary)
    for name in (
        "key_panic_states",
        "ord_panic_states",
        "f_drop_panic_normal_states",
        "f_drop_panic_unwind_states",
    ):
        record[name] = sorted(getattr(boundary, name))
    record["key_panic_calls"] = [
        {
            "state": item.state,
            "slot": int(item.slot),
            "source_identity": item.source_identity,
        }
        for item in sorted(boundary.key_panic_calls)
    ]
    for name in (
        "key_drop_panic_normal",
        "key_drop_panic_unwind",
    ):
        record[name] = [
            {"state": item.state, "slot": int(item.slot)}
            for item in sorted(getattr(boundary, name))
        ]
    record["key_pairs"] = [list(pair) for pair in boundary.key_pairs]
    record["rank_pairs"] = [list(pair) for pair in boundary.rank_pairs]
    record["initial_observable_element_state"] = list(
        boundary.initial_observable_element_state
    )
    return record


def boundary_from_record(
    record: dict[str, Any],
) -> model.KeySortBoundary:
    scalar_sets = {
        name: frozenset(record[name])
        for name in (
            "key_panic_states",
            "ord_panic_states",
            "f_drop_panic_normal_states",
            "f_drop_panic_unwind_states",
        )
    }
    return model.KeySortBoundary(
        **{
            **record,
            "initial_observable_element_state": tuple(
                record["initial_observable_element_state"]
            ),
            "key_pairs": tuple(
                tuple(pair) for pair in record["key_pairs"]
            ),
            "rank_pairs": tuple(
                tuple(pair) for pair in record["rank_pairs"]
            ),
            "key_panic_calls": frozenset(
                model.KeyCallKey(
                    item["state"],
                    model.KeySlot(item["slot"]),
                    item["source_identity"],
                )
                for item in record["key_panic_calls"]
            ),
            "key_drop_panic_normal": frozenset(
                model.KeyDropKey(
                    item["state"], model.KeySlot(item["slot"])
                )
                for item in record["key_drop_panic_normal"]
            ),
            "key_drop_panic_unwind": frozenset(
                model.KeyDropKey(
                    item["state"], model.KeySlot(item["slot"])
                )
                for item in record["key_drop_panic_unwind"]
            ),
            **scalar_sets,
        }
    )


def _spec(
    name: str,
    sequence: tuple[int, ...],
    configuration: model.SourceConfiguration,
    boundary: model.KeySortBoundary,
    *,
    source_case: str,
) -> dict[str, Any]:
    return {
        "name": name,
        "sequence": list(sequence),
        "configuration": configuration_record(configuration),
        "boundary": boundary_record(boundary),
        "source_case": source_case,
    }


def _accepted_boundary(
    record: dict[str, Any],
) -> model.KeySortBoundary | None:
    mode = record["result_mode"]
    if mode == accepted_private.IDENTITY_TOTAL_ORDER:
        ordering = model.KEY_TOTAL_ORDER
    elif mode == accepted_private.RANK_TOTAL_ORDER:
        ordering = model.RANK_TOTAL_ORDER
    elif mode == accepted_private.CONSTANT_EQUAL:
        ordering = model.CONSTANT_EQUAL
    else:
        return None
    return model.KeySortBoundary(
        initial_state=record["initial_state"],
        ordering_mode=ordering,
        contract_ordering_mode=ordering,
        rank_pairs=tuple(
            tuple(pair) for pair in record["rank_pairs"]
        ),
    )


def _inherited_private_specs() -> list[dict[str, Any]]:
    inherited = []
    for accepted in accepted_witnesses.witness_specs():
        if accepted["action"] != "sort":
            continue
        boundary_record_080 = accepted["boundary"]
        if (
            boundary_record_080["panic_states"]
            or boundary_record_080["panic_keys"]
        ):
            continue
        boundary = _accepted_boundary(boundary_record_080)
        if boundary is None:
            continue
        inherited.append(
            _spec(
                f"inherited-{accepted['name']}",
                tuple(accepted["sequence"]),
                model.SourceConfiguration(**accepted["configuration"]),
                boundary,
                source_case=accepted["name"],
            )
        )
    return inherited


@cache
def witness_specs() -> tuple[dict[str, Any], ...]:
    insertion = (2, 1)
    extras = [
        _spec(
            "empty-trivial-f-drop",
            (),
            model.SourceConfiguration(),
            model.KeySortBoundary(
                initial_state=7,
                f_drop_next_state_mode=model.INCREMENT_STATE,
            ),
            source_case="target-082-lifecycle",
        ),
        _spec(
            "zst-trivial-f-drop",
            (2, 1, 0),
            model.SourceConfiguration(element_size=0),
            model.KeySortBoundary(
                initial_observable_element_state=(4, 8),
                f_drop_interior_mode=model.INCREMENT_STATE,
            ),
            source_case="target-082-lifecycle",
        ),
        _spec(
            "duplicate-equal-owned-keys",
            (20, 11, 10, 21),
            model.SourceConfiguration(),
            model.mapped_key_boundary(
                {10: 0, 11: 0, 20: 1, 21: 1}
            ),
            source_case="target-082-duplicate",
        ),
        _spec(
            "all-equal-owned-key-identities",
            (4, 3, 2, 1, 0),
            model.SourceConfiguration(),
            model.KeySortBoundary(
                ordering_mode=model.CONSTANT_EQUAL,
                contract_ordering_mode=model.CONSTANT_EQUAL,
            ),
            source_case="target-082-duplicate",
        ),
        _spec(
            "key-left-panic-prefix",
            insertion,
            model.SourceConfiguration(),
            model.KeySortBoundary(
                key_panic_calls=frozenset(
                    {model.KeyCallKey(0, model.KeySlot.LEFT, 1)}
                )
            ),
            source_case="target-082-panic",
        ),
        _spec(
            "key-right-panic-left-unwind-drop",
            insertion,
            model.SourceConfiguration(),
            model.KeySortBoundary(
                key_panic_calls=frozenset(
                    {model.KeyCallKey(1, model.KeySlot.RIGHT, 2)}
                )
            ),
            source_case="target-082-panic",
        ),
        _spec(
            "ord-lt-panic-right-then-left-unwind-drop",
            insertion,
            model.SourceConfiguration(),
            model.KeySortBoundary(ord_panic_states=frozenset({2})),
            source_case="target-082-panic",
        ),
        _spec(
            "right-key-drop-panic-left-unwind-drop",
            insertion,
            model.SourceConfiguration(),
            model.KeySortBoundary(
                key_drop_panic_normal=frozenset(
                    {model.KeyDropKey(3, model.KeySlot.RIGHT)}
                )
            ),
            source_case="target-082-drop",
        ),
        _spec(
            "left-key-drop-panic",
            insertion,
            model.SourceConfiguration(),
            model.KeySortBoundary(
                key_drop_panic_normal=frozenset(
                    {model.KeyDropKey(4, model.KeySlot.LEFT)}
                )
            ),
            source_case="target-082-drop",
        ),
        _spec(
            "ord-panic-right-drop-double-panic-abort",
            insertion,
            model.SourceConfiguration(),
            model.KeySortBoundary(
                ord_panic_states=frozenset({2}),
                key_drop_panic_unwind=frozenset(
                    {model.KeyDropKey(3, model.KeySlot.RIGHT)}
                ),
            ),
            source_case="target-082-abort",
        ),
        _spec(
            "right-drop-panic-left-drop-double-panic-abort",
            insertion,
            model.SourceConfiguration(),
            model.KeySortBoundary(
                key_drop_panic_normal=frozenset(
                    {model.KeyDropKey(3, model.KeySlot.RIGHT)}
                ),
                key_drop_panic_unwind=frozenset(
                    {model.KeyDropKey(4, model.KeySlot.LEFT)}
                ),
            ),
            source_case="target-082-abort",
        ),
        _spec(
            "normal-f-drop-panic",
            (),
            model.SourceConfiguration(),
            model.KeySortBoundary(
                f_drop_panic_normal_states=frozenset({0})
            ),
            source_case="target-082-f-drop",
        ),
        _spec(
            "key-panic-f-drop-double-panic-abort",
            insertion,
            model.SourceConfiguration(),
            model.KeySortBoundary(
                key_panic_calls=frozenset(
                    {model.KeyCallKey(0, model.KeySlot.LEFT, 1)}
                ),
                f_drop_panic_unwind_states=frozenset({1}),
            ),
            source_case="target-082-f-drop",
        ),
        _spec(
            "callback-and-element-interior-mutation",
            (5, 3, 4, 1, 2, 0),
            model.SourceConfiguration(),
            model.KeySortBoundary(
                initial_state=2,
                initial_observable_element_state=(1, 2, 3),
                key_next_state_mode=model.AFFINE_STATE,
                key_state_multiplier=2,
                key_state_offset=1,
                key_interior_mode=model.INCREMENT_STATE,
                ord_next_state_mode=model.AFFINE_STATE,
                ord_state_multiplier=2,
                ord_state_offset=1,
                ord_interior_mode=model.AFFINE_STATE,
                ord_interior_multiplier=2,
                ord_interior_offset=1,
                key_drop_interior_mode=model.INCREMENT_STATE,
                f_drop_next_state_mode=model.INCREMENT_STATE,
                f_drop_interior_mode=model.INCREMENT_STATE,
            ),
            source_case="target-082-state",
        ),
        _spec(
            "interior-state-dependent-nonclassifying",
            (4, 3, 2, 1, 0),
            model.SourceConfiguration(),
            model.interior_state_dependent_boundary(
                initial_observable_element_state=(0,),
                key_interior_mode=model.INCREMENT_STATE,
            ),
            source_case="target-082-state",
        ),
    ]
    return tuple(_inherited_private_specs() + extras)


def _record(execution: Any) -> dict[str, Any]:
    return {
        "sequence": list(execution.state.sequence),
        "callback_state": execution.state.callback_state,
        "observable_element_state": list(
            execution.state.observable_element_state
        ),
        "terminal_status": execution.terminal_status,
        "private_terminal_status": execution.private_terminal_status,
        "unit_returned": execution.unit_returned,
        "panicked": execution.state.panicked,
        "aborted": execution.state.aborted,
        "terminal": execution.state.terminal,
        "f_drop_invoked": execution.state.f_drop_invoked,
        "f_drop_completed": execution.state.f_drop_completed,
        "panic_phase": execution.panic_phase,
        "panic_origin": execution.panic_origin,
        "abort_phase": execution.abort_phase,
        "adapter_event_count": len(execution.adapter_events),
    }


def _event_record(event: model.AdapterEvent) -> dict[str, Any]:
    record = asdict(event)
    for name in ("owned_key", "left_owned_key", "right_owned_key"):
        owned = getattr(event, name)
        if owned is not None:
            record[name]["slot"] = int(owned.slot)
    return record


def execute_spec(
    spec: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    sequence = tuple(spec["sequence"])
    configuration = model.SourceConfiguration(**spec["configuration"])
    boundary = boundary_from_record(spec["boundary"])
    primary = model.execute(model.SortInput(sequence, configuration), boundary)
    independent = reference.execute(sequence, configuration, boundary)
    primary_record = _record(primary)
    independent_record = _record(independent)
    primary_events = [
        _event_record(event) for event in primary.adapter_events
    ]
    independent_events = [
        _event_record(event) for event in independent.adapter_events
    ]
    correspondence = {
        "field_complete": primary_record == independent_record,
        "adapter_events_equal": primary_events == independent_events,
        "normal_panic_abort_equal": (
            primary.terminal_status == independent.terminal_status
        ),
        "full_observable_state_equal": (
            primary.state.callback_state
            == independent.state.callback_state
            and primary.state.observable_element_state
            == independent.state.observable_element_state
        ),
        "source_ordered_temporaries": all(
            _invocation_order_is_source_ordered(primary_events, invocation)
            for invocation in {
                event["invocation"]
                for event in primary_events
                if event["action"] != "drop-f"
            }
        ),
        "permutation_retained": (
            Counter(primary.state.sequence) == Counter(sequence)
            and Counter(independent.state.sequence) == Counter(sequence)
        ),
        "private_primary_step_count": len(primary.private_steps),
        "private_independent_event_count": len(
            independent.private_events
        ),
    }
    return primary_record, independent_record, correspondence


def _invocation_order_is_source_ordered(
    events: list[dict[str, Any]], invocation: int
) -> bool:
    actions = [
        event["action"]
        for event in events
        if event["invocation"] == invocation
        and event["action"] != "drop-f"
    ]
    canonical = [
        "key-left",
        "key-right",
        "ord-lt",
        "drop-key-right",
        "drop-key-left",
    ]
    positions = [canonical.index(action) for action in actions]
    return positions == sorted(positions) and len(actions) == len(set(actions))


@cache
def witness_payload() -> dict[str, Any]:
    cases: dict[str, Any] = {}
    statuses: set[str] = set()
    for spec in witness_specs():
        primary, independent, correspondence = execute_spec(spec)
        if not correspondence["field_complete"]:
            raise RuntimeError(f"{spec['name']}: field correspondence failed")
        if not correspondence["adapter_events_equal"]:
            raise RuntimeError(f"{spec['name']}: adapter events diverged")
        if not correspondence["source_ordered_temporaries"]:
            raise RuntimeError(f"{spec['name']}: temporary order diverged")
        if not correspondence["permutation_retained"]:
            raise RuntimeError(f"{spec['name']}: permutation was not retained")
        statuses.add(primary["terminal_status"])
        cases[spec["name"]] = {
            "spec": spec,
            "primary": primary,
            "independent": independent,
            "correspondence": correspondence,
        }
    if statuses != {model.NORMAL, model.PANIC, model.ABORT}:
        raise RuntimeError("witnesses do not cover normal, panic, and abort")
    return {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "private_source_model": accepted_private.MODEL_ID,
        "key_lifecycle_model": (
            "target-079-key-ord-drop-operational-v1-rust-1.96-complete"
        ),
        "case_count": len(cases),
        "terminal_statuses": sorted(statuses),
        "cases": cases,
    }


def operational_specs() -> tuple[dict[str, Any], ...]:
    return witness_specs()
