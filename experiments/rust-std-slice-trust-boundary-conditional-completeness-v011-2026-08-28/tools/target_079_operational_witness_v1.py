#!/usr/bin/env python3
"""Concrete replay witnesses for target-079 operational-v1."""

from __future__ import annotations

import copy
from dataclasses import asdict
from typing import Any

import target_079_operational_v1 as model


def _input(
    sequence: tuple[int, ...], index: int
) -> model.SelectionInput:
    return model.SelectionInput(
        initial_sequence=sequence,
        index=index,
        allocation=79,
        borrow=179,
        is_zst=False,
    )


def _panic_boundary(*, abort: bool) -> model.KeyOrdDropBoundary:
    def ord_lt(
        state: int,
        left: model.OwnedKeyIdentity,
        right: model.OwnedKeyIdentity,
    ) -> model.OrdLtObservation:
        return model.OrdLtObservation(
            left.key_identity < right.key_identity,
            state + 1,
            (
                state == 12
                and left.key_identity == 2
                and right.key_identity == 3
            ),
        )

    def drop(
        state: int, owned: model.OwnedKeyIdentity
    ) -> model.DropObservation:
        return model.DropObservation(
            state + 1,
            (
                abort
                and state == 14
                and owned.slot == model.KeySlot.LEFT
            ),
        )

    return model.KeyOrdDropBoundary(ord_lt=ord_lt, drop=drop)


def _missing_path_boundary() -> model.KeyOrdDropBoundary:
    def ord_lt(
        state: int,
        left: model.OwnedKeyIdentity,
        right: model.OwnedKeyIdentity,
    ) -> model.OrdLtObservation:
        return model.OrdLtObservation(
            left.key_identity < right.key_identity,
            state + 1,
            state == 2,
        )

    def drop(
        state: int, owned: model.OwnedKeyIdentity
    ) -> model.DropObservation:
        return model.DropObservation(
            state + 1,
            state == 4 and owned.slot == model.KeySlot.LEFT,
        )

    return model.KeyOrdDropBoundary(ord_lt=ord_lt, drop=drop)


def _reference(reference: model.selection.Reference) -> dict[str, Any]:
    return asdict(reference)


def _execution(
    execution: model.OperationalExecution,
) -> dict[str, Any]:
    output = execution.selection.output
    return {
        "termination": execution.termination.value,
        "panic_origin": execution.panic_origin,
        "coverage_status": execution.selection.coverage_status,
        "branch": execution.selection.branch,
        "output": (
            None
            if output is None
            else {
                "left": _reference(output.left),
                "pivot": _reference(output.pivot),
                "right": _reference(output.right),
                "pivot_identity": output.pivot_identity,
            }
        ),
        "final_state": asdict(execution.selection.final_state),
        "adapter_invocation_count": len(
            execution.adapter_invocations
        ),
    }


def _adapter(result: model.AdapterResult) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    for event in result.events:
        record = asdict(event)
        for field in (
            "owned_key",
            "left_owned_key",
            "right_owned_key",
        ):
            owned = getattr(event, field)
            record[field] = None if owned is None else asdict(owned)
        events.append(record)
    return {
        "termination": result.termination.value,
        "final_state": result.final_state,
        "is_less": result.is_less,
        "panic_origin": result.panic_origin,
        "events": events,
    }


def witness_payload() -> dict[str, Any]:
    normal_input = _input(tuple(range(39, 0, -1)), 19)
    normal_boundary = model.KeyOrdDropBoundary()
    normal_first = model.execute(normal_input, normal_boundary)
    normal_second = model.execute(normal_input, normal_boundary)
    assert model.exact_equivalent(normal_first, normal_second)
    assert model.active_contract_holds(
        normal_input, normal_boundary, normal_first
    )

    interrupted_input = _input((4, 3, 2, 1), 1)
    ordinary = model.execute(
        interrupted_input, _panic_boundary(abort=False)
    )
    aborted = model.execute(
        interrupted_input, _panic_boundary(abort=True)
    )
    missing_path = _missing_path_boundary().transition(0, 10, 20)

    normal_record = _execution(normal_first)
    negative_state = copy.deepcopy(normal_record)
    negative_state["final_state"]["callback_state"] += 1
    negative_termination = copy.deepcopy(normal_record)
    negative_termination["termination"] = "abort"

    return {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "normal": {
            "input": {
                "sequence": list(normal_input.initial_sequence),
                "index": normal_input.index,
                "allocation": normal_input.allocation,
                "borrow": normal_input.borrow,
            },
            "execution1": normal_record,
            "execution2": _execution(normal_second),
        },
        "ordinary_panic": _execution(ordinary),
        "abort": _execution(aborted),
        "lt_panic_right_cleanup_left_drop_panic": _adapter(
            missing_path
        ),
        "negative_exact_equivalence": {
            "callback_state": negative_state,
            "termination": negative_termination,
        },
    }
