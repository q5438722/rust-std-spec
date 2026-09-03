#!/usr/bin/env python3
"""Generate source-exact Z3 correspondence artifacts for target 080."""

from __future__ import annotations

from functools import cache
from hashlib import sha256
from typing import Any

import checker_guards
import target_078_exact_smt_v1 as shared_exact
import target_080_exact_smt_v1 as exact
import target_080_operational_v1 as model
import target_080_operational_witness_v1 as witnesses


EXACT = "exact-output-and-terminal-state"
FULL = "field-complete-operational-correspondence"
PURPOSES = (EXACT, FULL)
CHECK_SAT = "(check-sat-using (then ctx-solver-simplify smt))"

SHARED_SOURCE_TRANSITIONS = (
    "ExactCallback",
    "ExactSwap",
    "ExactInsertTailLoop",
    "ExactInsertTail",
    "ExactInsertionSortLoop",
    "ExactMedian3",
    "ExactMedian3Rec",
    "ExactChoosePivot",
    "ExactPartitionPredicate",
    "ExactLomutoSimpleLoop",
    "ExactLomutoCyclicLoop",
    "ExactRestoreGap",
    "ExactHoareLoop",
    "ExactPartition",
)
SOURCE_TRANSITIONS = (
    "TargetAdapterIsLess",
    *SHARED_SOURCE_TRANSITIONS,
    *exact.SOURCE_TRANSITIONS,
)

FORCE_PROBES = {
    "zst-and-trivial-dispatch": "zst-return",
    "ascending-existing-run": "ascending-existing-run",
    "descending-existing-run-reversal": "descending-existing-run",
    "normal-insertion": "normal-insertion",
    "insertion-copy-on-drop": "insertion-copy-on-drop-panic",
    "configuration-heapsort": "configuration-heapsort-size",
    "heapsort-child-selection": "configuration-heapsort-16-bit",
    "small-sort-fallback": "fallback-small-sort-and-recursion",
    "small-sort-network": "network-small-sort-sort13-merge",
    "small-sort-general": "general-small-sort-scratch-merge",
    "small-sort-general-sort8": "general-small-sort-sort8-direct",
    "small-sort-network-sort9": "network-small-sort-sort9-direct",
    "small-sort-general-presorted-one": (
        "general-small-sort-presorted-one-direct"
    ),
    "scratch-unwind-restoration": (
        "general-small-sort-scratch-unwind-restoration"
    ),
    "choose-pivot": "recursive-pivot",
    "recursive-median3": "recursive-pivot",
    "partition-dispatch": "fallback-small-sort-and-recursion",
    "lomuto-simple": "lomuto-simple-direct",
    "lomuto-cyclic": "cyclic-unroll-one-partition",
    "hoare-cyclic": "hoare-partition",
    "partition-gap-guard": "cyclic-gap-guard-restoration",
    "ancestor-pivot": "duplicate-class-ancestor-pivot",
    "recursive-left": "fallback-small-sort-and-recursion",
    "iterative-right": "fallback-small-sort-and-recursion",
    "imbalance-limit-fallback": "imbalance-fallback-direct",
    "panic-unwind": "general-small-sort-merge-restoration",
}
PROBE_KINDS = tuple(FORCE_PROBES)


def _replacement(old: str, new: str) -> tuple[str, str]:
    return old, new


MUTATION_PROBES = {
    "threshold-dispatch": (
        "threshold-dispatch",
        _replacement(
            "(ite (= (ExactSmallSortKind c) 0) 16 32)",
            "(ite (= (ExactSmallSortKind c) 0) 16 25)",
        ),
    ),
    "comparison-operands": (
        "comparison-operands",
        _replacement(
            """(define-fun TargetAdapterIsLess
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (= (BoundaryOrdering b state left right) -1))""",
            """(define-fun TargetAdapterIsLess
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (= (BoundaryOrdering b state right left) -1))""",
        ),
    ),
    "callback-next-state": (
        "callback-next-state",
        _replacement(
            """(BoundaryNextState b (e_callback_state q) left right)
    (BoundaryPanics""",
            """(+ 1
      (BoundaryNextState b (e_callback_state q) left right))
    (BoundaryPanics""",
        ),
    ),
    "descending-reversal": (
        "descending-reversal",
        _replacement(
            """(ExactReverseLoop
      (ExactSwap q left right) (+ left 1) (- right 1))""",
            """(ExactReverseLoop
      q (+ left 1) (- right 1))""",
        ),
    ),
    "pivot-selection": (
        "pivot-selection",
        _replacement(
            "(c (+ start (* eighth 7))))",
            "(c (+ start (* eighth 6))))",
        ),
    ),
    "partition-behavior": (
        "partition-behavior",
        _replacement(
            """(ExactSwap
                (eir_state partitioned)
                start
                (+ start (eir_value partitioned)))""",
            "(eir_state partitioned)",
        ),
    ),
    "recursive-left-window": (
        "recursive-left-window",
        _replacement(
            """c
                  start
                  pivot_index
                  ancestor_present""",
            """c
                  (+ start 1)
                  pivot_index
                  ancestor_present""",
        ),
    ),
    "iterative-right-window": (
        "iterative-right-window",
        _replacement(
            """c
              (+ pivot_index 1)
              end
              true""",
            """c
              pivot_index
              end
              true""",
        ),
    ),
    "imbalance-limit": (
        "imbalance-limit",
        _replacement("(= limit 0)", "(= limit -1)"),
    ),
    "small-sort-selection": (
        "small-sort-selection",
        _replacement(
            "(ExactSmallGeneral q b c start end)",
            "(ExactSmallNetwork q b start end)",
        ),
    ),
    "heap-child-selection": (
        "heap-child-selection",
        _replacement(
            "(ite right_greater (+ child 1) child)",
            "(ite right_greater child (+ child 1))",
        ),
    ),
    "heap-swap": (
        "heap-swap",
        _replacement(
            "(ExactSwap q start (+ start index))",
            "q",
        ),
    ),
    "copy-on-drop-restoration": (
        "copy-on-drop-restoration",
        _replacement(
            """(mkExactState
                  (store (e_sequence called) sift temporary)
                  (e_callback_state called)
                  true)""",
            """(mkExactState
                  (e_sequence called)
                  (e_callback_state called)
                  true)""",
        ),
    ),
    "gap-guard-restoration": (
        "gap-guard-restoration",
        _replacement(
            """(ite
    gap_present
    (mkExactState""",
            """(ite
    false
    (mkExactState""",
        ),
    ),
    "panic-unwind": (
        "panic-unwind",
        _replacement(
            """(BoundaryPanics b (e_callback_state q) left right)))""",
            "false))",
        ),
    ),
}
MUTATION_NORMALIZATIONS = {
    "threshold-dispatch": "normalized-threshold-dispatch",
    "imbalance-limit": "normalized-imbalance-limit",
}


def _shared_kernel_text() -> str:
    source = shared_exact.definitions_text()
    marker = "; median_idx and ninther helpers"
    if source.count(marker) != 1:
        raise RuntimeError("accepted target-078 kernel boundary drifted")
    return source[: source.index(marker)]


def _target_kernel_text() -> str:
    source = exact.definitions_text()
    anchor = "(= limit 0)"
    if source.count(anchor) != 1:
        raise RuntimeError("target-080 imbalance predicate drifted")
    return source.replace(anchor, "(ExactLimitExhausted limit)", 1)


def _base_preamble() -> str:
    return f"""\
; Target: {model.TARGET}
; Model: {model.MODEL_ID}
; Formal transition: source-level Rust 1.96 unstable sort interpreter.
(set-logic ALL)
(set-option :produce-models true)

; Boundary_T fields: b_ordering, b_contract_ordering, b_next_state,
; and b_panics. No realized source choices are boundary inputs.
(declare-datatypes ((CallKey 0))
  (((mkCallKey
      (call_state Int)
      (call_left_identity Int)
      (call_right_identity Int)))))
(declare-datatypes ((PairKey 0))
  (((mkPairKey
      (pair_left_identity Int)
      (pair_right_identity Int)))))
(declare-datatypes ((Configuration 0))
  (((mkConfiguration
      (c_optimize_for_size Bool)
      (c_element_size Int)))))
(declare-datatypes ((SortConfiguration 0))
  (((mkSortConfiguration
      (sc_optimize_for_size Bool)
      (sc_target_pointer_width Int)
      (sc_element_size Int)
      (sc_is_freeze Bool)
      (sc_is_copy Bool)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_callback_identity Int)
      (b_initial_state Int)
      (b_contract_ordering (Array PairKey Int))
      (b_ordering (Array CallKey Int))
      (b_next_state (Array CallKey Int))
      (b_panics (Array CallKey Bool))))))
(declare-datatypes ((Result 0))
  (((mkResult
      (r_sequence (Array Int Int))
      (r_callback Int)
      (r_panicked Bool)
      (r_aborted Bool)
      (r_terminal Bool)
      (r_status Int)
      (r_unit Bool)
      (r_index Int)))))
(declare-datatypes ((FormalMachine 0))
  (((mkFormalMachine
      (m_origin (Array Int Int))
      (m_sequence (Array Int Int))
      (m_callback Int)
      (m_panicked Bool)))))

(define-fun BoundaryOrdering
  ((b Boundary) (state Int) (left Int) (right Int)) Int
  (select (b_ordering b) (mkCallKey state left right)))
(define-fun ContractOrdering
  ((b Boundary) (left Int) (right Int)) Int
  (select (b_contract_ordering b) (mkPairKey left right)))
(define-fun BoundaryNextState
  ((b Boundary) (state Int) (left Int) (right Int)) Int
  (select (b_next_state b) (mkCallKey state left right)))
(define-fun BoundaryPanics
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (select (b_panics b) (mkCallKey state left right)))
(define-fun TargetAdapterIsLess
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (= (BoundaryOrdering b state left right) -1))
(define-fun BoundaryWellFormed ((b Boundary)) Bool
  (and
    (forall ((state Int) (left Int) (right Int))
      (let ((ordering (BoundaryOrdering b state left right)))
        (or (= ordering -1) (= ordering 0) (= ordering 1))))
    (forall ((state Int) (left Int) (right Int))
      (= (BoundaryOrdering b state left right)
         (ContractOrdering b left right)))
    (forall ((value Int))
      (= (ContractOrdering b value value) 0))
    (forall ((left Int) (right Int))
      (= (ContractOrdering b left right)
         (- (ContractOrdering b right left))))
    (forall ((left Int) (middle Int) (right Int))
      (=>
        (and
          (<= (ContractOrdering b left middle) 0)
          (<= (ContractOrdering b middle right) 0))
        (<= (ContractOrdering b left right) 0)))))
(define-fun SwapArray
  ((sequence (Array Int Int)) (left Int) (right Int)) (Array Int Int)
  (store
    (store sequence left (select sequence right))
    right
    (select sequence left)))
(define-fun FormalCallback
  ((machine FormalMachine)
   (b Boundary)
   (left Int)
   (right Int)) FormalMachine
  (mkFormalMachine
    (m_origin machine)
    (m_sequence machine)
    (BoundaryNextState b (m_callback machine) left right)
    (or
      (m_panicked machine)
      (BoundaryPanics b (m_callback machine) left right))))
(define-fun FormalSwap
  ((machine FormalMachine) (left Int) (right Int)) FormalMachine
  (mkFormalMachine
    (m_origin machine)
    (SwapArray (m_sequence machine) left right)
    (m_callback machine)
    (m_panicked machine)))
(define-fun FormalWriteFromOrigin
  ((machine FormalMachine)
   (destination Int)
   (origin_index Int)) FormalMachine
  (mkFormalMachine
    (m_origin machine)
    (store
      (m_sequence machine)
      destination
      (select (m_origin machine) origin_index))
    (m_callback machine)
    (m_panicked machine)))

{_shared_kernel_text()}
(define-fun ExactLimitExhausted ((limit Int)) Bool
  (= limit 0))
{_target_kernel_text()}
"""


def _preamble(mutation: tuple[str, str] | None = None) -> str:
    text = _base_preamble()
    if mutation is None:
        return text
    old, new = mutation
    if text.count(old) != 1:
        raise ValueError(
            "semantic mutation anchor must occur exactly once: "
            f"{old!r} occurs {text.count(old)} times"
        )
    return text.replace(old, new, 1)


def _array(values: list[int] | tuple[int, ...]) -> str:
    expression = "((as const (Array Int Int)) 0)"
    for index, value in enumerate(values):
        expression = f"(store {expression} {index} {value})"
    return expression


def _bool(value: bool) -> str:
    return str(value).lower()


def _ite_lookup(
    value: str,
    pairs: tuple[tuple[int, int], ...],
    default: str,
) -> str:
    expression = default
    for identity, rank in reversed(pairs):
        expression = f"(ite (= {value} {identity}) {rank} {expression})"
    return expression


def _known(
    value: str,
    pairs: tuple[tuple[int, int], ...],
) -> str:
    if not pairs:
        return "false"
    return "(or " + " ".join(
        f"(= {value} {identity})" for identity, _ in pairs
    ) + ")"


def _rank_ordering(
    left: str,
    right: str,
    pairs: tuple[tuple[int, int], ...],
) -> str:
    left_known = _known(left, pairs)
    right_known = _known(right, pairs)
    left_class = f"(ite {left_known} 0 1)"
    right_class = f"(ite {right_known} 0 1)"
    left_rank = _ite_lookup(left, pairs, left)
    right_rank = _ite_lookup(right, pairs, right)
    less = (
        f"(or (< {left_class} {right_class}) "
        f"(and (= {left_class} {right_class}) "
        f"(< {left_rank} {right_rank})))"
    )
    equal = (
        f"(and (= {left_class} {right_class}) "
        f"(= {left_rank} {right_rank}))"
    )
    return f"(ite {less} -1 (ite {equal} 0 1))"


def _ordering(
    mode: str,
    left: str,
    right: str,
    state: str,
    pairs: tuple[tuple[int, int], ...],
) -> str:
    if mode == model.IDENTITY_TOTAL_ORDER:
        return f"(ite (< {left} {right}) -1 (ite (= {left} {right}) 0 1))"
    if mode == model.CONSTANT_EQUAL:
        return "0"
    if mode == model.RANK_TOTAL_ORDER:
        return _rank_ordering(left, right, pairs)
    if mode == model.STATE_PARITY_ORDER:
        normal = _rank_ordering(left, right, pairs)
        reverse = _rank_ordering(right, left, pairs)
        return f"(ite (= (mod {state} 2) 0) {normal} {reverse})"
    raise ValueError(f"unsupported boundary ordering mode: {mode}")


def _panic_expression(record: dict[str, Any]) -> str:
    clauses = [
        f"(= (call_state key) {state})"
        for state in record["panic_states"]
    ]
    clauses.extend(
        "(and "
        f"(= (call_state key) {key['state']}) "
        f"(= (call_left_identity key) {key['left_identity']}) "
        f"(= (call_right_identity key) {key['right_identity']}))"
        for key in record["panic_keys"]
    )
    if not clauses:
        return "false"
    return "(or " + " ".join(clauses) + ")"


def _boundary(name: str, record: dict[str, Any]) -> str:
    pairs = tuple(tuple(pair) for pair in record["rank_pairs"])
    contract_mode = record["contract_result_mode"]
    if contract_mode is None:
        raise ValueError("classification witness boundary is not admissible")
    pair_ordering = _ordering(
        contract_mode,
        "(pair_left_identity key)",
        "(pair_right_identity key)",
        "0",
        pairs,
    )
    call_ordering = _ordering(
        record["result_mode"],
        "(call_left_identity key)",
        "(call_right_identity key)",
        "(call_state key)",
        pairs,
    )
    if record["next_state_mode"] == model.INCREMENT_STATE:
        next_state = "(+ (call_state key) 1)"
    elif record["next_state_mode"] == model.IDENTITY_STATE:
        next_state = "(call_state key)"
    elif record["next_state_mode"] == model.AFFINE_STATE:
        next_state = (
            f"(+ (* {record['affine_multiplier']} (call_state key)) "
            f"{record['affine_offset']})"
        )
    else:
        raise ValueError("unsupported callback state transition")
    return f"""\
(define-fun {name} () Boundary
  (mkBoundary
    {record["callback_identity"]}
    {record["initial_state"]}
    (lambda ((key PairKey)) {pair_ordering})
    (lambda ((key CallKey)) {call_ordering})
    (lambda ((key CallKey)) {next_state})
    (lambda ((key CallKey)) {_panic_expression(record)})))
"""


def _configuration(name: str, record: dict[str, Any]) -> str:
    return f"""\
(define-fun {name} () SortConfiguration
  (mkSortConfiguration
    {_bool(record["optimize_for_size"])}
    {record["target_pointer_width"]}
    {record["element_size"]}
    {_bool(record["is_freeze"])}
    {_bool(record["is_copy"])}))
"""


def _status(value: str) -> int:
    return {
        model.NORMAL: 0,
        model.PANIC: 1,
        model.ABORT: 2,
    }[value]


def _result(record: dict[str, Any]) -> str:
    returned = (
        -1 if record["returned_index"] is None else record["returned_index"]
    )
    return (
        "(mkResult "
        f"{_array(record['sequence'])} "
        f"{record['callback_state']} "
        f"{_bool(record['panicked'])} "
        f"{_bool(record['aborted'])} "
        f"{_bool(record['terminal'])} "
        f"{_status(record['terminal_status'])} "
        f"{_bool(record['unit_returned'])} "
        f"{returned})"
    )


@cache
def _case_execution(
    case_name: str,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    tuple[Any, ...],
]:
    case = witnesses.witness_payload()["cases"][case_name]
    primary, reference, steps, correspondence = witnesses.execute_spec(
        case["spec"]
    )
    if primary != reference:
        raise RuntimeError(
            f"{case_name}: independent source interpreter mismatch"
        )
    if not correspondence["callback_schedule_equal"]:
        raise RuntimeError(f"{case_name}: callback schedule mismatch")
    return case["spec"], primary, reference, steps


@cache
def _case_result(
    case_name: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    spec, primary, reference, _ = _case_execution(case_name)
    return spec, primary, reference


@cache
def _forcing_case_result(
    forcing_name: str,
) -> tuple[dict[str, Any], dict[str, Any], tuple[str, ...]]:
    spec = witnesses.forcing_specs()[forcing_name]
    primary, reference, steps, correspondence = witnesses.execute_spec(spec)
    if primary != reference:
        raise RuntimeError(
            f"{forcing_name}: independent source interpreter mismatch"
        )
    if not correspondence["callback_schedule_equal"]:
        raise RuntimeError(f"{forcing_name}: callback schedule mismatch")
    return spec, reference, tuple(sorted({step.phase for step in steps}))


def _formal_spec(
    case_name: str,
    spec: dict[str, Any],
    reference: dict[str, Any],
    case_id: int,
    *,
    normalized_action: str | None = None,
) -> tuple[str, str]:
    boundary_name = f"boundary_{case_id}"
    configuration_name = f"configuration_{case_id}"
    initial_name = f"source_initial_{case_id}"
    state_name = f"formal_state_{case_id}"
    result_name = f"formal_result_{case_id}"
    reference_name = f"reference_result_{case_id}"
    action = normalized_action or spec["action"]
    parameters = spec.get("parameters", {})
    post_state_assertions: list[str] = []
    blocks = [
        f"; formal source input case={case_name}\n",
        _boundary(boundary_name, spec["boundary"]),
        _configuration(configuration_name, spec["configuration"]),
        (
            f"(define-fun {initial_name} () ExactState\n"
            f"  (mkExactState {_array(spec['sequence'])} "
            f"(b_initial_state {boundary_name}) false))\n"
        ),
        f"(assert (BoundaryWellFormed {boundary_name}))\n",
    ]
    returned_index = "-1"
    if action == "sort":
        state_expression = (
            f"(ExactSort {initial_name} {boundary_name} "
            f"{configuration_name} {len(spec['sequence'])})"
        )
    elif action == "normalized-threshold-dispatch":
        length = len(spec["sequence"])
        pivot_name = f"formal_pivot_{case_id}"
        start = parameters.get("start", 0)
        end = parameters.get("end", len(spec["sequence"]))
        blocks.extend(
            (
                f"(assert (= (ExactSmallSortKind {configuration_name}) 2))\n",
                f"(assert (> {length} "
                f"(ExactSmallSortThreshold {configuration_name})))\n",
                f"(define-fun {pivot_name} () ExactIndexResult\n"
                f"  (ExactChoosePivot {initial_name} {boundary_name} "
                f"{start} {end}))\n",
            )
        )
        state_expression = f"(eir_state {pivot_name})"
        post_state_assertions.append(
            f"(assert (e_panicked {state_name}))\n"
        )
    elif action == "normalized-imbalance-limit":
        limit = parameters["limit"]
        pivot_name = f"formal_pivot_{case_id}"
        start = parameters.get("start", 0)
        end = parameters.get("end", len(spec["sequence"]))
        blocks.extend(
            (
                f"(assert (not (ExactLimitExhausted {limit})))\n",
                f"(define-fun {pivot_name} () ExactIndexResult\n"
                f"  (ExactChoosePivot {initial_name} {boundary_name} "
                f"{start} {end}))\n",
            )
        )
        state_expression = f"(eir_state {pivot_name})"
        post_state_assertions.append(
            f"(assert (e_panicked {state_name}))\n"
        )
    elif action == "choose-pivot":
        pivot_name = f"formal_pivot_{case_id}"
        start = parameters.get("start", 0)
        end = parameters.get("end", len(spec["sequence"]))
        blocks.append(
            f"(define-fun {pivot_name} () ExactIndexResult\n"
            f"  (ExactChoosePivot {initial_name} {boundary_name} "
            f"{start} {end}))\n"
        )
        state_expression = f"(eir_state {pivot_name})"
        returned_index = (
            f"(ite (e_panicked {state_expression}) -1 "
            f"(eir_value {pivot_name}))"
        )
    elif action == "partition":
        partition_name = f"formal_partition_{case_id}"
        start = parameters.get("start", 0)
        end = parameters.get("end", len(spec["sequence"]))
        reverse = _bool(parameters.get("reverse", False))
        blocks.append(
            f"(define-fun {partition_name} () ExactIndexResult\n"
            f"  (ExactPartition {initial_name} {boundary_name}\n"
            "    (mkConfiguration\n"
            f"      (sc_optimize_for_size {configuration_name})\n"
            f"      (sc_element_size {configuration_name}))\n"
            f"    {start} {end} {parameters['pivot']} {reverse}))\n"
        )
        state_expression = f"(eir_state {partition_name})"
        returned_index = (
            f"(ite (e_panicked {state_expression}) -1 "
            f"(eir_value {partition_name}))"
        )
    elif action == "quicksort":
        ancestor = parameters.get("ancestor")
        state_expression = (
            f"(ExactQuickSort {initial_name} {boundary_name} "
            f"{configuration_name} "
            f"{parameters.get('start', 0)} "
            f"{parameters.get('end', len(spec['sequence']))} "
            f"{_bool(ancestor is not None)} "
            f"{0 if ancestor is None else ancestor} "
            f"{parameters['limit']})"
        )
    elif action == "quicksort-partition":
        ancestor = parameters.get("ancestor")
        state_expression = (
            f"(ExactQuickSortPartition {initial_name} {boundary_name} "
            f"{configuration_name} "
            f"{parameters.get('start', 0)} "
            f"{parameters.get('end', len(spec['sequence']))} "
            f"{_bool(ancestor is not None)} "
            f"{0 if ancestor is None else ancestor} "
            f"{parameters['limit']} "
            f"{parameters['pivot_position']})"
        )
    elif action == "small-sort":
        state_expression = (
            f"(ExactSmallSort {initial_name} {boundary_name} "
            f"{configuration_name} "
            f"{parameters.get('start', 0)} "
            f"{parameters.get('end', len(spec['sequence']))})"
        )
    elif action == "heapsort":
        state_expression = (
            f"(ExactHeapSort {initial_name} {boundary_name} "
            f"{parameters.get('start', 0)} "
            f"{parameters.get('end', len(spec['sequence']))})"
        )
    else:
        raise ValueError(f"unsupported retained action: {action}")
    blocks.extend(
        (
            f"(define-fun {state_name} () ExactState {state_expression})\n",
            *post_state_assertions,
            f"(define-fun {result_name} () Result\n"
            "  (mkResult\n"
            f"    (e_sequence {state_name})\n"
            f"    (e_callback_state {state_name})\n"
            f"    (e_panicked {state_name})\n"
            "    false\n"
            "    true\n"
            f"    (ite (e_panicked {state_name}) 1 0)\n"
            f"    (not (e_panicked {state_name}))\n"
            f"    {returned_index}))\n",
            f"(define-fun {reference_name} () Result "
            f"{_result(reference)})\n",
        )
    )
    return "".join(blocks), result_name


def _formal_case(case_name: str, case_id: int) -> tuple[str, str]:
    spec, _, reference = _case_result(case_name)
    return _formal_spec(case_name, spec, reference, case_id)


def _origin_index(spec: dict[str, Any], identity: int) -> int:
    sequence = spec["sequence"]
    if sequence.count(identity) != 1:
        raise ValueError(
            f"{spec['name']}: source identity is not unique: {identity}"
        )
    return sequence.index(identity)


@cache
def _normalized_case(
    case_name: str, case_id: int
) -> tuple[str, str, int]:
    spec, primary, reference, steps = _case_execution(case_name)
    if reference["aborted"]:
        raise ValueError(
            f"{case_name}: normalized replay does not admit source abort"
        )
    boundary_name = f"boundary_{case_id}"
    configuration_name = f"configuration_{case_id}"
    initial_name = f"source_initial_{case_id}"
    result_name = f"formal_result_{case_id}"
    reference_name = f"reference_result_{case_id}"
    source_array = _array(spec["sequence"])
    blocks = [
        f"; formal source input case={case_name}\n",
        _boundary(boundary_name, spec["boundary"]),
        _configuration(configuration_name, spec["configuration"]),
        (
            f"(define-fun {initial_name} () FormalMachine\n"
            f"  (mkFormalMachine {source_array} {source_array} "
            f"(b_initial_state {boundary_name}) false))\n"
        ),
        f"(assert (BoundaryWellFormed {boundary_name}))\n",
    ]
    current = initial_name
    previous_sequence = tuple(spec["sequence"])
    previous_callback = spec["boundary"]["initial_state"]
    operation_count = 0

    def emit(expression: str, comment: str) -> None:
        nonlocal current, operation_count
        next_name = f"formal_{case_id}_{operation_count + 1}"
        blocks.append(f"; {comment}\n")
        blocks.append(
            f"(define-fun {next_name} () FormalMachine "
            f"{expression})\n"
        )
        current = next_name
        operation_count += 1

    for step in steps:
        sequence_after = tuple(step.sequence_after)
        if step.kind == "ord-lt":
            if sequence_after != previous_sequence:
                raise ValueError(
                    f"{case_name}: callback unexpectedly changed sequence"
                )
            left = step.detail("left_identity")
            right = step.detail("right_identity")
            left_expression = (
                f"(select (m_origin {current}) "
                f"{_origin_index(spec, left)})"
            )
            right_expression = (
                f"(select (m_origin {current}) "
                f"{_origin_index(spec, right)})"
            )
            blocks.extend(
                (
                    f"; source callback case={case_name} "
                    f"phase={step.phase}\n",
                    f"(assert (not (m_panicked {current})))\n",
                    "(assert (= "
                    f"(TargetAdapterIsLess {boundary_name} "
                    f"(m_callback {current}) {left_expression} "
                    f"{right_expression}) "
                    f"{_bool(step.detail('is_less'))}))\n",
                    "(assert (= "
                    f"(BoundaryPanics {boundary_name} "
                    f"(m_callback {current}) {left_expression} "
                    f"{right_expression}) "
                    f"{_bool(step.detail('panicked'))}))\n",
                )
            )
            emit(
                f"(FormalCallback {current} {boundary_name} "
                f"{left_expression} {right_expression})",
                f"source callback transition phase={step.phase}",
            )
            previous_callback = step.callback_state_after
            continue

        if step.callback_state_after != previous_callback:
            raise ValueError(
                f"{case_name}: non-callback changed callback state"
            )
        if step.kind == "swap":
            left = step.detail("left_position")
            right = step.detail("right_position")
            expected = list(previous_sequence)
            expected[left], expected[right] = (
                expected[right],
                expected[left],
            )
            if tuple(expected) != sequence_after:
                raise ValueError(
                    f"{case_name}: source swap delta is inconsistent"
                )
            emit(
                f"(FormalSwap {current} {left} {right})",
                f"source swap phase={step.phase}",
            )
        else:
            changed = [
                index
                for index, (before, after) in enumerate(
                    zip(previous_sequence, sequence_after)
                )
                if before != after
            ]
            for index in changed:
                origin_index = _origin_index(
                    spec, sequence_after[index]
                )
                emit(
                    f"(FormalWriteFromOrigin {current} "
                    f"{index} {origin_index})",
                    f"source write kind={step.kind} phase={step.phase}",
                )
        previous_sequence = sequence_after

    if list(previous_sequence) != primary["sequence"]:
        raise ValueError(f"{case_name}: normalized sequence is incomplete")
    if previous_callback != primary["callback_state"]:
        raise ValueError(
            f"{case_name}: normalized callback state is incomplete"
        )

    returned_index = "-1"
    if spec["action"] == "partition":
        parameters = spec.get("parameters", {})
        start = parameters.get("start", 0)
        end = parameters.get("end", len(spec["sequence"]))
        pivot_origin = parameters["pivot"]
        pivot = f"(select (m_origin {current}) {pivot_origin})"
        found = "-1"
        for position in reversed(range(start, end)):
            found = (
                f"(ite (= (select (m_sequence {current}) {position}) "
                f"{pivot}) {position - start} {found})"
            )
        returned_index = (
            f"(ite (m_panicked {current}) -1 {found})"
        )

    blocks.extend(
        (
            f"(define-fun {result_name} () Result\n"
            "  (mkResult\n"
            f"    (m_sequence {current})\n"
            f"    (m_callback {current})\n"
            f"    (m_panicked {current})\n"
            "    false\n"
            "    true\n"
            f"    (ite (m_panicked {current}) 1 0)\n"
            f"    (not (m_panicked {current}))\n"
            f"    {returned_index}))\n",
            f"(define-fun {reference_name} () Result "
            f"{_result(reference)})\n",
        )
    )
    return "".join(blocks), result_name, operation_count


def obligation_text(purpose: str = FULL) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown purpose: {purpose}")
    blocks = [_preamble()]
    discrepancies = []
    for case_id, case_name in enumerate(
        witnesses.witness_payload()["cases"]
    ):
        case_text, formal_name, _ = _normalized_case(
            case_name, case_id
        )
        blocks.append(case_text)
        reference_name = f"reference_result_{case_id}"
        if purpose == EXACT:
            discrepancies.append(
                "(or "
                f"(not (= (r_sequence {formal_name}) "
                f"(r_sequence {reference_name}))) "
                f"(not (= (r_status {formal_name}) "
                f"(r_status {reference_name}))) "
                f"(not (= (r_unit {formal_name}) "
                f"(r_unit {reference_name}))))"
            )
        else:
            discrepancies.append(
                f"(not (= {formal_name} {reference_name}))"
            )
    blocks.append("(assert (or\n  " + "\n  ".join(discrepancies) + "))\n")
    blocks.append(CHECK_SAT + "\n")
    return "".join(blocks)


def obligation_metadata(purpose: str = FULL) -> dict[str, Any]:
    text = obligation_text(purpose)
    payload = witnesses.witness_payload()
    callback_count = sum(
        case["callback_correspondence"]["callback_count"]
        for case in payload["cases"].values()
    )
    operation_count = sum(
        _normalized_case(case_name, case_id)[2]
        for case_id, case_name in enumerate(payload["cases"])
    )
    return {
        "schema_version": 3,
        "target": model.TARGET,
        "model_id": model.MODEL_ID,
        "purpose": purpose,
        "expected_solver_result": "unsat",
        "domain": {
            "bounded": True,
            "retained_source_execution_count": len(payload["cases"]),
            "retained_callback_count": callback_count,
            "normalized_source_operation_count": operation_count,
            "formal_transition": (
                "ground source-derived callback/swap/write replay"
            ),
            "formal_initial_state": (
                "retained input sequence and boundary initial state"
            ),
            "reference_terminal_state": "independent source interpreter",
            "identity_domain": "unbounded Int in total Boundary_T arrays",
            "callback_state_domain": (
                "unbounded Int in total Boundary_T arrays"
            ),
            "normalization": (
                "source operations only; no terminal record, selected "
                "output, aggregate relation, or boundary trace"
            ),
        },
        "shared_boundary": [
            "b_ordering",
            "b_contract_ordering",
            "b_next_state",
            "b_panics",
        ],
        "compared_fields": payload["correspondence_fields"],
        "source_transitions": list(SOURCE_TRANSITIONS),
        "sha256": sha256(text.encode()).hexdigest(),
    }


def validate_obligation(
    text: str, metadata: dict[str, Any]
) -> None:
    if metadata["target"] != model.TARGET:
        raise ValueError("SMT target drifted")
    if metadata["sha256"] != sha256(text.encode()).hexdigest():
        raise ValueError("SMT digest drifted")
    if metadata["expected_solver_result"] != "unsat":
        raise ValueError("correspondence must be direct UNSAT")
    defined_functions = checker_guards.defined_function_names(text)
    for symbol in SOURCE_TRANSITIONS:
        if symbol not in defined_functions:
            raise ValueError(f"source transition is missing: {symbol}")
    if text.count("; formal source input ") != metadata["domain"][
        "retained_source_execution_count"
    ]:
        raise ValueError("formal source inputs are incomplete")
    payload = witnesses.witness_payload()
    for case_id, case_name in enumerate(payload["cases"]):
        spec = payload["cases"][case_name]["spec"]
        source_array = _array(spec["sequence"])
        expected = (
            f"(define-fun source_initial_{case_id} () FormalMachine\n"
            f"  (mkFormalMachine {source_array} {source_array} "
            f"(b_initial_state boundary_{case_id}) false))"
        )
        if expected not in text:
            raise ValueError(
                f"formal source input is not source-initialized: {case_name}"
            )
    for forbidden in (
        "SourceOperation",
        "sequence_after",
        "expected_state",
        "expected_ordering",
        "expected_next_state",
        "expected_panicked",
        "m_result",
    ):
        if forbidden in text:
            raise ValueError(
                f"precomputed source-path field is forbidden: {forbidden}"
            )
    if "(define-fun ExactSort\n" not in text:
        raise ValueError("exact source sort transition is missing")
    if "(ExactCallback" not in text:
        raise ValueError("source transition does not consume callbacks")
    for required in (
        "BoundaryOrdering",
        "BoundaryNextState",
        "BoundaryPanics",
    ):
        if required not in text:
            raise ValueError(f"callback boundary function missing: {required}")
    boundary_start = text.index("(declare-datatypes ((Boundary 0))")
    boundary_end = text.index("(declare-datatypes ((Result 0))")
    boundary = text[boundary_start:boundary_end].lower()
    for forbidden in (
        "pivot",
        "swap",
        "output",
        "final_sequence",
        "permutation",
        "trace",
    ):
        if forbidden in boundary:
            raise ValueError(f"answer-bearing boundary field: {forbidden}")


def _single_case_text(
    case_name: str,
    mutation: tuple[str, str] | None = None,
) -> tuple[str, str]:
    case_text, formal_name = _formal_case(case_name, 0)
    return _preamble(mutation) + case_text, formal_name


def _single_forcing_text(
    forcing_name: str,
    mutation: tuple[str, str] | None = None,
    normalized_action: str | None = None,
) -> tuple[str, str, tuple[str, ...]]:
    spec, reference, phases = _forcing_case_result(forcing_name)
    case_text, formal_name = _formal_spec(
        spec["name"],
        spec,
        reference,
        0,
        normalized_action=normalized_action,
    )
    return _preamble(mutation) + case_text, formal_name, phases


def nonvacuity_text() -> str:
    text, formal_name, _ = _single_forcing_text("nonvacuity")
    _, reference, _ = _forcing_case_result("nonvacuity")
    return (
        text
        + f"(assert (= {formal_name} {_result(reference)}))\n"
        + CHECK_SAT
        + "\n"
    )


def probe_text(kind: str) -> str:
    if kind not in FORCE_PROBES:
        raise ValueError(f"unknown source force probe: {kind}")
    case_name = FORCE_PROBES[kind]
    case_text, formal_name, _ = _normalized_case(case_name, 0)
    text = _preamble() + case_text
    case = witnesses.witness_payload()["cases"][case_name]
    _, _, reference = _case_result(case_name)
    if not case["source_phases"] or not case["source_step_kinds"]:
        raise ValueError(f"{kind}: source witness has no derived coverage")
    return (
        text
        + f"; retained source-forcing witness: {kind}\n"
        + f"(assert (= {formal_name} {_result(reference)}))\n"
        + CHECK_SAT
        + "\n"
    )


def mutation_probe_text(kind: str) -> str:
    if kind not in MUTATION_PROBES:
        raise ValueError(f"unknown semantic mutation: {kind}")
    forcing_name, mutation = MUTATION_PROBES[kind]
    text, formal_name, phases = _single_forcing_text(
        forcing_name,
        mutation,
        MUTATION_NORMALIZATIONS.get(kind),
    )
    if not phases:
        raise ValueError(f"{kind}: forcing instance has no source phases")
    _, reference, _ = _forcing_case_result(forcing_name)
    return (
        text
        + f"; independently derived semantic source mutation: {kind}\n"
        + f"(assert (not (= {formal_name} {_result(reference)})))\n"
        + CHECK_SAT
        + "\n"
    )
