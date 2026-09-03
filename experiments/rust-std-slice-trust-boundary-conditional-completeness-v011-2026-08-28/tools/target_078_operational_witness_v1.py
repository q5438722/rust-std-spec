#!/usr/bin/env python3
"""Concrete witnesses for the complete target-078 operational model."""

from __future__ import annotations

import copy
import random
from collections import Counter
from typing import Any

import target_078_operational_v1 as model


def _input(
    sequence: list[int] | tuple[int, ...] | range,
    index: int,
    *,
    optimize_for_size: bool = False,
    element_size: int = 8,
) -> model.SelectionInput:
    return model.SelectionInput(
        tuple(sequence),
        index,
        41,
        51,
        False,
        model.SourceConfiguration(optimize_for_size, element_size),
    )


def _input_payload(item: model.SelectionInput) -> dict[str, Any]:
    return {
        "sequence": list(item.initial_sequence),
        "index": item.index,
        "allocation": item.allocation,
        "borrow": item.borrow,
        "is_zst": item.is_zst,
        "configuration": {
            "optimize_for_size": (
                item.configuration.optimize_for_size
            ),
            "element_size": item.configuration.element_size,
        },
    }


def _reference_payload(reference: model.Reference) -> dict[str, Any]:
    return {
        "allocation": reference.allocation,
        "parent_borrow": reference.parent_borrow,
        "start": reference.start,
        "span": reference.span,
        "projection_kind": reference.projection_kind,
    }


def _execution_payload(execution: model.Execution) -> dict[str, Any]:
    output = execution.output
    event_counts = Counter(
        event.kind for event in execution.derived_events
    )
    event_details = {
        "partition_implementations": sorted(
            {
                str(event.detail("implementation"))
                for event in execution.derived_events
                if event.kind == "partition-implementation"
            }
        ),
        "narrowing_kinds": sorted(
            {
                event.kind
                for event in execution.derived_events
                if "narrow" in event.kind
            }
        ),
        "ninther_branches": sorted(
            {
                str(event.detail("branch"))
                for event in execution.derived_events
                if event.kind == "ninther"
            }
        ),
        "introselect_terminal": [
            str(event.detail("terminal"))
            for event in execution.derived_events
            if event.kind == "introselect-return"
        ],
    }
    return {
        "coverage_status": execution.coverage_status,
        "branch": execution.branch,
        "output": (
            None
            if output is None
            else {
                "left": _reference_payload(output.left),
                "pivot": _reference_payload(output.pivot),
                "right": _reference_payload(output.right),
                "pivot_identity": output.pivot_identity,
            }
        ),
        "final_state": {
            "sequence": list(execution.final_state.sequence),
            "allocation": execution.final_state.allocation,
            "borrow": execution.final_state.borrow,
            "length": execution.final_state.length,
            "callback_state": execution.final_state.callback_state,
            "panicked": execution.final_state.panicked,
            "terminal": execution.final_state.terminal,
        },
        "panic_phase": execution.panic_phase,
        "event_counts": dict(sorted(event_counts.items())),
        "event_details": event_details,
    }


def _normal_determinism() -> dict[str, Any]:
    sequence = list(range(65))
    random.Random(780165).shuffle(sequence)
    item = _input(sequence, 32, element_size=128)
    boundary = model.integer_total_order_boundary(initial_state=9)
    first = model.execute(item, boundary)
    second = model.execute(item, boundary)
    assert model.exact_equivalent(first, second)
    assert model.active_contract_holds(item, boundary, first)
    context = {
        "input": _input_payload(item),
        "boundary": {
            "callback_identity": boundary.callback_identity,
            "initial_state": boundary.initial_state,
            "ordering": "integer-total-order",
            "next_state": "increment",
            "contract_ordering": "integer-total-order",
            "panics": [],
        },
    }
    return {
        "input": context["input"],
        "boundary": context["boundary"],
        "execution1_context": copy.deepcopy(context),
        "execution2_context": copy.deepcopy(context),
        "execution1": _execution_payload(first),
        "execution2": _execution_payload(second),
        "expected": {
            "same_input_and_boundary": True,
            "execution1_satisfies_active_contract": True,
            "execution2_satisfies_active_contract": True,
            "pivot_is_sorted_order_statistic": True,
            "exact_principal_return_and_final_state": True,
        },
    }


def _frozen_prior_falsifier() -> dict[str, Any]:
    boundary = model.state_prefix_order_boundary(
        ordering_cutoff=3,
    )
    item = _input((3, 2, 1), 1)
    first = model.execute(item, boundary)
    second = model.execute(item, boundary)
    assert model.exact_equivalent(first, second)
    return {
        "input": _input_payload(item),
        "total_relation": {
            "callback_identity": boundary.callback_identity,
            "initial_state": boundary.initial_state,
            "ordering": boundary.ordering_mode,
            "ordering_cutoff": boundary.ordering_cutoff,
            "next_state": boundary.next_state_mode,
            "contract_ordering": boundary.contract_ordering_mode,
            "panic_states": [],
            "panic_keys": [],
        },
        "execution1": _execution_payload(first),
        "execution2": _execution_payload(second),
        "expected": {
            "relation_is_total_and_trace_independent": True,
            "final_sequence": [1, 2, 3],
            "callback_state": 3,
            "exact_principal_return_and_final_state": True,
        },
    }


def _branch_witnesses() -> dict[str, Any]:
    fallback_item = _input(range(50), 1)
    fallback = model.execute(
        fallback_item, model.constant_order_boundary(model.LESS)
    )
    assert len(
        [
            event
            for event in fallback.derived_events
            if event.kind == "choose-pivot"
        ]
    ) == 16

    configurations: dict[str, Any] = {}
    for optimize, size, label in (
        (False, 8, "lomuto-cyclic-unroll-two"),
        (False, 32, "lomuto-cyclic-unroll-one"),
        (False, 128, "hoare-cyclic"),
        (True, 8, "lomuto-simple"),
        (True, 128, "optimize-hoare-cyclic"),
    ):
        sequence = list(range(40))
        random.Random(size + int(optimize)).shuffle(sequence)
        item = _input(
            sequence,
            20,
            optimize_for_size=optimize,
            element_size=size,
        )
        execution = model.execute(
            item, model.integer_total_order_boundary()
        )
        assert model.active_contract_holds(
            item, model.integer_total_order_boundary(), execution
        )
        configurations[label] = {
            "input": _input_payload(item),
            "execution": _execution_payload(execution),
        }
    return {
        "sixteen_step_fallback": {
            "input": _input_payload(fallback_item),
            "execution": _execution_payload(fallback),
            "expected_choose_pivot_count": 16,
            "expected_terminal": "introselect-fallback",
        },
        "partition_configurations": configurations,
    }


def _negative_witnesses(
    baseline_record: dict[str, Any],
) -> dict[str, Any]:
    mutations = {
        "post_sequence_drift": (
            "final_state",
            "sequence",
        ),
        "post_callback_state_drift": (
            "final_state",
            "callback_state",
        ),
        "returned_pivot_reference_drift": (
            "output",
            "pivot",
            "start",
        ),
        "panic_status_drift": (
            "final_state",
            "panicked",
        ),
    }
    result: dict[str, Any] = {}
    for name, path in mutations.items():
        candidate = copy.deepcopy(baseline_record)
        if name == "post_sequence_drift":
            sequence = candidate["final_state"]["sequence"]
            sequence[0], sequence[1] = sequence[1], sequence[0]
        elif name == "post_callback_state_drift":
            candidate["final_state"]["callback_state"] += 1
        elif name == "returned_pivot_reference_drift":
            candidate["output"]["pivot"]["start"] += 1
        else:
            candidate["final_state"]["panicked"] = True
        result[name] = {
            "mutated_path": list(path),
            "candidate": candidate,
            "expected_exact_equivalent": False,
        }
    return result


def witness_payload() -> dict[str, Any]:
    normal = _normal_determinism()
    return {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "model_version": model.MODEL_VERSION,
        "active_contract_sha256": model.ACTIVE_CONTRACT_SHA256,
        "normal_determinism": normal,
        "frozen_prior_falsifier": _frozen_prior_falsifier(),
        "branch_witnesses": _branch_witnesses(),
        "negative_witnesses": _negative_witnesses(
            normal["execution1"]
        ),
    }
