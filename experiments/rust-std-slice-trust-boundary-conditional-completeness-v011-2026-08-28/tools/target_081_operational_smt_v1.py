#!/usr/bin/env python3
"""SMT obligations for target-081 source adapter and operational composition."""

from __future__ import annotations

from functools import cache
from hashlib import sha256
from typing import Any

import target_080_operational_smt_v1 as accepted_private_smt
import target_081_operational_v1 as model
import target_081_operational_witness_v1 as witnesses


PRIVATE_SOURCE = "accepted-private-source-correspondence"
ADAPTER_SOURCE = "ordering-adapter-source-correspondence"
FIXED_BOUNDARY = "fixed-boundary-operational-determinism"
PURPOSES = (PRIVATE_SOURCE, ADAPTER_SOURCE, FIXED_BOUNDARY)

PROBE_KINDS = (
    "ordering-less",
    "ordering-equal",
    "ordering-greater",
    "compare-panic-before-less-test",
    "callback-state-transition",
    "interior-mutation-before-panic",
    "normal-drop",
    "drop-interior-mutation",
    "normal-drop-panic",
    "double-panic-abort",
)
MUTATION_KINDS = (
    "adapter-evaluates-twice",
    "equal-treated-as-less",
    "callback-next-state-ignored",
    "callback-interior-state-ignored",
    "callback-panic-ignored",
    "callback-drop-skipped",
    "callback-drop-interior-state-ignored",
    "normal-drop-panic-ignored",
    "double-panic-collapsed-to-panic",
)
CHECK_SAT = "(check-sat-using (then ctx-solver-simplify smt))"


def _adapter_preamble() -> str:
    return f"""\
; Target: {model.TARGET}
; Model: {model.MODEL_ID}
; Source: compare(a,b) is evaluated once; successful Ordering is then tested
; against Ordering::Less. Comparator results, closure state, externally
; observable element interior state, panic, and Drop effects are the only
; admitted callback observations.
(set-logic ALL)
(set-option :produce-models true)
(declare-datatypes ((CallKey 0))
  (((mkCallKey (call_state Int) (call_left Int) (call_right Int)))))
(declare-datatypes ((DropKey 0))
  (((mkDropKey (drop_state Int) (drop_unwinding Bool)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_ordering (Array CallKey Int))
      (b_next_state (Array CallKey Int))
      (b_next_interior (Array CallKey (Array Int Int)))
      (b_panics (Array CallKey Bool))
      (b_drop_next_state (Array DropKey Int))
      (b_drop_next_interior (Array DropKey (Array Int Int)))
      (b_drop_panics (Array DropKey Bool))))))
(declare-datatypes ((AdapterResult 0))
  (((mkAdapterResult
      (ar_ordering Int)
      (ar_state Int)
      (ar_interior (Array Int Int))
      (ar_panicked Bool)
      (ar_callback_evaluations Int)
      (ar_less_tested Bool)
      (ar_is_less Bool)
      (ar_observation Int)))))
(declare-datatypes ((PrivateResult 0))
  (((mkPrivateResult
      (pr_sequence (Array Int Int))
      (pr_state Int)
      (pr_interior (Array Int Int))
      (pr_status Int)))))
(declare-datatypes ((PublicResult 0))
  (((mkPublicResult
      (r_sequence (Array Int Int))
      (r_state Int)
      (r_interior (Array Int Int))
      (r_panicked Bool)
      (r_aborted Bool)
      (r_terminal Bool)
      (r_status Int)
      (r_unit Bool)
      (r_drop_invoked Bool)
      (r_drop_completed Bool)))))

(define-fun BoundaryOrdering
  ((b Boundary) (state Int) (left Int) (right Int)) Int
  (select (b_ordering b) (mkCallKey state left right)))
(define-fun BoundaryNextState
  ((b Boundary) (state Int) (left Int) (right Int)) Int
  (select (b_next_state b) (mkCallKey state left right)))
(define-fun BoundaryNextInterior
  ((b Boundary) (state Int) (left Int) (right Int)) (Array Int Int)
  (select (b_next_interior b) (mkCallKey state left right)))
(define-fun BoundaryPanics
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (select (b_panics b) (mkCallKey state left right)))
(define-fun ComparatorObservation
  ((b Boundary) (state Int) (left Int) (right Int)) Int
  (BoundaryOrdering b state left right))
(define-fun BoundaryWellFormed ((b Boundary)) Bool
  (forall ((state Int) (left Int) (right Int))
    (let ((ordering (BoundaryOrdering b state left right)))
      (or (= ordering -1) (= ordering 0) (= ordering 1)))))

(define-fun SourceOrderingAdapter
  ((b Boundary) (state Int) (left Int) (right Int)) AdapterResult
  (let ((ordering (BoundaryOrdering b state left right))
        (next_state (BoundaryNextState b state left right))
        (next_interior (BoundaryNextInterior b state left right))
        (panics (BoundaryPanics b state left right)))
    (mkAdapterResult
      ordering
      next_state
      next_interior
      panics
      1
      (not panics)
      (and (not panics) (= ordering -1))
      (ComparatorObservation b state left right))))
(define-fun IndependentOrderingAdapter
  ((b Boundary) (state Int) (left Int) (right Int)) AdapterResult
  (let ((observed (select (b_ordering b) (mkCallKey state left right)))
        (transitioned
          (select (b_next_state b) (mkCallKey state left right)))
        (interior_transitioned
          (select (b_next_interior b) (mkCallKey state left right)))
        (raised (select (b_panics b) (mkCallKey state left right))))
    (mkAdapterResult
      observed
      transitioned
      interior_transitioned
      raised
      1
      (not raised)
      (and (not raised) (= observed -1))
      observed)))

(define-fun SourcePublicFinish
  ((b Boundary) (private PrivateResult)) PublicResult
  (ite
    (= (pr_status private) 2)
    (mkPublicResult
      (pr_sequence private) (pr_state private) (pr_interior private)
      false true true 2 false false false)
    (let ((unwinding (= (pr_status private) 1))
          (drop_next
            (select
              (b_drop_next_state b)
              (mkDropKey
                (pr_state private)
                (= (pr_status private) 1))))
          (drop_next_interior
            (select
              (b_drop_next_interior b)
              (mkDropKey
                (pr_state private)
                (= (pr_status private) 1))))
          (drop_panics
            (select
              (b_drop_panics b)
              (mkDropKey
                (pr_state private)
                (= (pr_status private) 1)))))
      (let ((status
              (ite drop_panics
                (ite unwinding 2 1)
                (ite unwinding 1 0))))
        (mkPublicResult
          (pr_sequence private)
          drop_next
          drop_next_interior
          (= status 1)
          (= status 2)
          true
          status
          (= status 0)
          true
          (not drop_panics))))))
(define-fun IndependentPublicFinish
  ((b Boundary) (private PrivateResult)) PublicResult
  (ite
    (= (pr_status private) 2)
    (mkPublicResult
      (pr_sequence private) (pr_state private) (pr_interior private)
      false true true 2 false false false)
    (let ((was_unwinding (= (pr_status private) 1)))
      (let ((after_drop
              (select
                (b_drop_next_state b)
                (mkDropKey (pr_state private) was_unwinding)))
            (interior_after_drop
              (select
                (b_drop_next_interior b)
                (mkDropKey (pr_state private) was_unwinding)))
            (drop_raised
              (select
                (b_drop_panics b)
                (mkDropKey (pr_state private) was_unwinding))))
        (let ((terminal_status
                (ite drop_raised
                  (ite was_unwinding 2 1)
                  (ite was_unwinding 1 0))))
          (mkPublicResult
            (pr_sequence private)
            after_drop
            interior_after_drop
            (= terminal_status 1)
            (= terminal_status 2)
            true
            terminal_status
            (= terminal_status 0)
            true
            (not drop_raised)))))))
"""


def adapter_source_correspondence_text() -> str:
    return (
        _adapter_preamble()
        + """\
(declare-const boundary Boundary)
(declare-const state Int)
(declare-const left Int)
(declare-const right Int)
(declare-const private PrivateResult)
(assert
  (or
    (not
      (=
        (SourceOrderingAdapter boundary state left right)
        (IndependentOrderingAdapter boundary state left right)))
    (not
      (=
        (SourcePublicFinish boundary private)
        (IndependentPublicFinish boundary private)))))
"""
        + CHECK_SAT
        + "\n"
    )


def private_source_correspondence_text() -> str:
    return accepted_private_smt.obligation_text(
        accepted_private_smt.FULL
    )


def _private_boundary_record(
    record: dict[str, Any],
) -> dict[str, Any]:
    return {
        "callback_identity": record["callback_identity"],
        "initial_state": record["initial_state"],
        "result_mode": record["ordering_mode"],
        "next_state_mode": record["next_state_mode"],
        "contract_result_mode": record["contract_ordering_mode"],
        "rank_pairs": record["rank_pairs"],
        "affine_multiplier": record["affine_multiplier"],
        "affine_offset": record["affine_offset"],
        "panic_states": record["panic_states"],
        "panic_keys": record["panic_keys"],
    }


def _drop_next_expression(record: dict[str, Any]) -> str:
    mode = record["drop_next_state_mode"]
    if mode == model.INCREMENT_STATE:
        return "(+ (drop_state key) 1)"
    if mode == model.IDENTITY_STATE:
        return "(drop_state key)"
    if mode == model.AFFINE_STATE:
        return (
            f"(+ (* {record['drop_affine_multiplier']} (drop_state key)) "
            f"{record['drop_affine_offset']})"
        )
    raise ValueError(f"unsupported drop state mode: {mode}")


def _drop_panic_expression(record: dict[str, Any]) -> str:
    normal = record["drop_panic_normal_states"]
    unwind = record["drop_panic_unwind_states"]

    def states(values: list[int]) -> str:
        if not values:
            return "false"
        return "(or " + " ".join(
            f"(= (drop_state key) {state})" for state in values
        ) + ")"

    return (
        f"(ite (drop_unwinding key) {states(unwind)} {states(normal)})"
    )


def _source_public_suffix() -> str:
    return """\
(declare-datatypes ((DropKey 0))
  (((mkDropKey (drop_state Int) (drop_unwinding Bool)))))
(declare-datatypes ((DropBoundary 0))
  (((mkDropBoundary
      (db_next_state (Array DropKey Int))
      (db_panics (Array DropKey Bool))))))
(declare-datatypes ((PublicResult081 0))
  (((mkPublicResult081
      (p_sequence (Array Int Int))
      (p_callback Int)
      (p_panicked Bool)
      (p_aborted Bool)
      (p_terminal Bool)
      (p_status Int)
      (p_unit Bool)
      (p_drop_invoked Bool)
      (p_drop_completed Bool)))))
(define-fun FinishPublic081
  ((private ExactState) (drop_boundary DropBoundary)) PublicResult081
  (let ((unwinding (e_panicked private)))
    (let ((next_state
            (select
              (db_next_state drop_boundary)
              (mkDropKey (e_callback_state private) unwinding)))
          (drop_panics
            (select
              (db_panics drop_boundary)
              (mkDropKey (e_callback_state private) unwinding))))
      (let ((status
              (ite drop_panics
                (ite unwinding 2 1)
                (ite unwinding 1 0))))
        (mkPublicResult081
          (e_sequence private)
          next_state
          (= status 1)
          (= status 2)
          true
          status
          (= status 0)
          true
          (not drop_panics))))))
"""


@cache
def fixed_boundary_determinism_text() -> str:
    blocks = [
        accepted_private_smt._base_preamble(),
        _source_public_suffix(),
    ]
    case_id = 0
    for spec in witnesses.operational_specs():
        boundary = spec["boundary"]
        if (
            boundary["ordering_mode"]
            not in {
                model.IDENTITY_TOTAL_ORDER,
                model.RANK_TOTAL_ORDER,
                model.CONSTANT_EQUAL,
            }
            or boundary["contract_ordering_mode"] is None
        ):
            continue
        name = spec["name"]
        private_record = _private_boundary_record(boundary)
        blocks.extend(
            (
                f"; fixed Boundary_T source case={name}\n",
                accepted_private_smt._boundary(
                    f"boundary081_{case_id}", private_record
                ),
                accepted_private_smt._configuration(
                    f"configuration081_{case_id}", spec["configuration"]
                ),
                (
                    f"(define-fun initial081_{case_id} () ExactState\n"
                    f"  (mkExactState "
                    f"{accepted_private_smt._array(spec['sequence'])} "
                    f"{boundary['initial_state']} false))\n"
                ),
                (
                    f"(define-fun drop081_{case_id} () DropBoundary\n"
                    "  (mkDropBoundary\n"
                    f"    (lambda ((key DropKey)) "
                    f"{_drop_next_expression(boundary)})\n"
                    f"    (lambda ((key DropKey)) "
                    f"{_drop_panic_expression(boundary)})))\n"
                ),
                (
                    f"(define-fun private_left081_{case_id} () ExactState\n"
                    f"  (ExactSort initial081_{case_id} "
                    f"boundary081_{case_id} configuration081_{case_id} "
                    f"{len(spec['sequence'])}))\n"
                ),
                (
                    f"(define-fun private_right081_{case_id} () ExactState\n"
                    f"  (ExactSort initial081_{case_id} "
                    f"boundary081_{case_id} configuration081_{case_id} "
                    f"{len(spec['sequence'])}))\n"
                ),
                (
                    f"(define-fun public_left081_{case_id} () "
                    f"PublicResult081\n"
                    f"  (FinishPublic081 private_left081_{case_id} "
                    f"drop081_{case_id}))\n"
                ),
                (
                    f"(define-fun public_right081_{case_id} () "
                    f"PublicResult081\n"
                    f"  (FinishPublic081 private_right081_{case_id} "
                    f"drop081_{case_id}))\n"
                ),
                (
                    f"(assert (not (= public_left081_{case_id} "
                    f"public_right081_{case_id})))\n"
                ),
            )
        )
        case_id += 1
    if case_id < 20:
        raise RuntimeError("fixed-boundary source cases are incomplete")
    blocks.append(CHECK_SAT + "\n")
    return "".join(blocks)


def _adapter_fixture(
    *,
    ordering: int = model.LESS,
    next_state: int = 8,
    next_interior: int = 13,
    panics: bool = False,
    drop_next: int = 9,
    drop_next_interior: int = 17,
    drop_panics: bool = False,
) -> str:
    return f"""\
(define-fun fixture () Boundary
  (mkBoundary
    ((as const (Array CallKey Int)) {ordering})
    ((as const (Array CallKey Int)) {next_state})
    ((as const (Array CallKey (Array Int Int)))
      ((as const (Array Int Int)) {next_interior}))
    ((as const (Array CallKey Bool)) {str(panics).lower()})
    ((as const (Array DropKey Int)) {drop_next})
    ((as const (Array DropKey (Array Int Int)))
      ((as const (Array Int Int)) {drop_next_interior}))
    ((as const (Array DropKey Bool)) {str(drop_panics).lower()})))
"""


def nonvacuity_text() -> str:
    return (
        _adapter_preamble()
        + _adapter_fixture()
        + """\
(define-fun private () PrivateResult
  (mkPrivateResult
    ((as const (Array Int Int)) 0)
    8
    ((as const (Array Int Int)) 13)
    0))
(assert (= (ar_ordering (SourceOrderingAdapter fixture 7 1 2)) -1))
(assert
  (= (select (ar_interior (SourceOrderingAdapter fixture 7 1 2)) 0) 13))
(assert (= (r_status (SourcePublicFinish fixture private)) 0))
(assert (= (select (r_interior (SourcePublicFinish fixture private)) 0) 17))
"""
        + CHECK_SAT
        + "\n"
    )


def probe_text(kind: str) -> str:
    if kind not in PROBE_KINDS:
        raise ValueError(f"unknown target-081 probe: {kind}")
    fixtures = {
        "ordering-less": (model.LESS, 8, False, 9, False, 0),
        "ordering-equal": (model.EQUAL, 8, False, 9, False, 0),
        "ordering-greater": (model.GREATER, 8, False, 9, False, 0),
        "compare-panic-before-less-test": (
            model.LESS,
            8,
            True,
            9,
            False,
            1,
        ),
        "callback-state-transition": (
            model.GREATER,
            44,
            False,
            45,
            False,
            0,
        ),
        "interior-mutation-before-panic": (
            model.LESS,
            8,
            True,
            9,
            False,
            1,
        ),
        "normal-drop": (model.LESS, 8, False, 9, False, 0),
        "drop-interior-mutation": (
            model.LESS,
            8,
            False,
            9,
            False,
            0,
        ),
        "normal-drop-panic": (model.LESS, 8, False, 9, True, 1),
        "double-panic-abort": (model.LESS, 8, True, 9, True, 2),
    }
    ordering, next_state, panics, drop_next, drop_panics, status = fixtures[
        kind
    ]
    private_status = (
        1
        if kind in {
            "compare-panic-before-less-test",
            "interior-mutation-before-panic",
            "double-panic-abort",
        }
        else 0
    )
    assertions = {
        "ordering-less": "(assert (ar_is_less adapter))",
        "ordering-equal": "(assert (not (ar_is_less adapter)))",
        "ordering-greater": "(assert (not (ar_is_less adapter)))",
        "compare-panic-before-less-test": (
            "(assert (and (ar_panicked adapter) "
            "(not (ar_less_tested adapter))))"
        ),
        "callback-state-transition": "(assert (= (ar_state adapter) 44))",
        "interior-mutation-before-panic": (
            "(assert (and (ar_panicked adapter) "
            "(= (select (ar_interior adapter) 0) 13)))"
        ),
        "normal-drop": "(assert (r_drop_completed public))",
        "drop-interior-mutation": (
            "(assert (= (select (r_interior public) 0) 17))"
        ),
        "normal-drop-panic": "(assert (not (r_drop_completed public)))",
        "double-panic-abort": "(assert (r_aborted public))",
    }
    return (
        _adapter_preamble()
        + _adapter_fixture(
            ordering=ordering,
            next_state=next_state,
            panics=panics,
            drop_next=drop_next,
            drop_panics=drop_panics,
        )
        + f"""\
(define-fun adapter () AdapterResult
  (SourceOrderingAdapter fixture 7 1 2))
(define-fun private () PrivateResult
  (mkPrivateResult
    ((as const (Array Int Int)) 0)
    8
    ((as const (Array Int Int)) 13)
    {private_status}))
(define-fun public () PublicResult
  (SourcePublicFinish fixture private))
{assertions[kind]}
(assert (= (r_status public) {status}))
"""
        + CHECK_SAT
        + "\n"
    )


def mutation_text(kind: str) -> str:
    if kind not in MUTATION_KINDS:
        raise ValueError(f"unknown target-081 mutation: {kind}")
    adapter_bodies = {
        "adapter-evaluates-twice": (
            "(mkAdapterResult ordering next_state next_interior panics 2 "
            "(not panics) (and (not panics) (= ordering -1)) ordering)"
        ),
        "equal-treated-as-less": (
            "(mkAdapterResult ordering next_state next_interior panics 1 "
            "(not panics) (and (not panics) (<= ordering 0)) ordering)"
        ),
        "callback-next-state-ignored": (
            "(mkAdapterResult ordering state next_interior panics 1 "
            "(not panics) (and (not panics) (= ordering -1)) ordering)"
        ),
        "callback-interior-state-ignored": (
            "(mkAdapterResult ordering next_state "
            "((as const (Array Int Int)) 0) panics 1 "
            "(not panics) (and (not panics) (= ordering -1)) ordering)"
        ),
        "callback-panic-ignored": (
            "(mkAdapterResult ordering next_state next_interior false 1 true "
            "(= ordering -1) ordering)"
        ),
    }
    if kind in adapter_bodies:
        return (
            _adapter_preamble()
            + """\
(declare-const boundary Boundary)
(declare-const state Int)
(declare-const left Int)
(declare-const right Int)
(define-fun MutatedAdapter
  ((b Boundary) (state Int) (left Int) (right Int)) AdapterResult
  (let ((ordering (BoundaryOrdering b state left right))
        (next_state (BoundaryNextState b state left right))
        (next_interior (BoundaryNextInterior b state left right))
        (panics (BoundaryPanics b state left right)))
"""
            + "    "
            + adapter_bodies[kind]
            + "))\n"
            + """\
(assert
  (or
    (= (BoundaryOrdering boundary state left right) -1)
    (= (BoundaryOrdering boundary state left right) 0)
    (= (BoundaryOrdering boundary state left right) 1)))
(assert
  (not
    (=
      (SourceOrderingAdapter boundary state left right)
      (MutatedAdapter boundary state left right))))
"""
            + CHECK_SAT
            + "\n"
        )

    mutated_finish = {
        "callback-drop-skipped": """\
  (mkPublicResult
    (pr_sequence private) (pr_state private) (pr_interior private)
    (= (pr_status private) 1) (= (pr_status private) 2) true
    (pr_status private) (= (pr_status private) 0) false false)""",
        "callback-drop-interior-state-ignored": """\
  (mkPublicResult
    (pr_sequence private)
    (select (b_drop_next_state b) (mkDropKey (pr_state private) false))
    (pr_interior private)
    false false true 0 true true true)""",
        "normal-drop-panic-ignored": """\
  (mkPublicResult
    (pr_sequence private)
    (select (b_drop_next_state b) (mkDropKey (pr_state private) false))
    (select (b_drop_next_interior b) (mkDropKey (pr_state private) false))
    false false true 0 true true true)""",
        "double-panic-collapsed-to-panic": """\
  (mkPublicResult
    (pr_sequence private)
    (select (b_drop_next_state b) (mkDropKey (pr_state private) true))
    (select (b_drop_next_interior b) (mkDropKey (pr_state private) true))
    true false true 1 false true false)""",
    }[kind]
    fixture = {
        "callback-drop-skipped": _adapter_fixture(drop_panics=False),
        "callback-drop-interior-state-ignored": _adapter_fixture(
            drop_panics=False
        ),
        "normal-drop-panic-ignored": _adapter_fixture(drop_panics=True),
        "double-panic-collapsed-to-panic": _adapter_fixture(
            panics=True, drop_panics=True
        ),
    }[kind]
    private_status = 1 if kind == "double-panic-collapsed-to-panic" else 0
    return (
        _adapter_preamble()
        + fixture
        + f"""\
(define-fun private () PrivateResult
  (mkPrivateResult
    ((as const (Array Int Int)) 0)
    8
    ((as const (Array Int Int)) 13)
    {private_status}))
(define-fun MutatedFinish
  ((b Boundary) (private PrivateResult)) PublicResult
{mutated_finish})
(assert
  (not
    (=
      (SourcePublicFinish fixture private)
      (MutatedFinish fixture private))))
"""
        + CHECK_SAT
        + "\n"
    )


def obligation_text(purpose: str) -> str:
    if purpose == PRIVATE_SOURCE:
        return private_source_correspondence_text()
    if purpose == ADAPTER_SOURCE:
        return adapter_source_correspondence_text()
    if purpose == FIXED_BOUNDARY:
        return fixed_boundary_determinism_text()
    raise ValueError(f"unknown target-081 obligation purpose: {purpose}")


def obligation_metadata(purpose: str) -> dict[str, Any]:
    text = obligation_text(purpose)
    return {
        "schema_version": 1,
        "target": model.TARGET,
        "input_order": model.INPUT_ORDER,
        "model_id": model.MODEL_ID,
        "purpose": purpose,
        "expected_solver_result": "unsat",
        "sha256": sha256(text.encode()).hexdigest(),
        "source_backing": (
            "accepted target-080 Rust 1.96 private source transitions"
            if purpose == PRIVATE_SOURCE
            else "core/src/slice/mod.rs:3188-3193 and callback drop glue"
        ),
        "boundary_fields": [
            "Ordering(state,left,right)",
            "callback next_state(state,left,right)",
            "callback next observable_element_state(state,left,right)",
            "callback panic(state,left,right)",
            "callback Drop next_state(state,unwinding)",
            "callback Drop next observable_element_state(state,unwinding)",
            "callback Drop panic(state,unwinding)",
        ],
        "prohibited_boundary_fields": [
            "schedule",
            "comparison already realized",
            "pivot",
            "swap",
            "output",
            "permutation",
            "final state",
            "final observable element interior state",
            "trace",
        ],
    }


def validate_obligation(text: str, metadata: dict[str, Any]) -> None:
    if metadata["sha256"] != sha256(text.encode()).hexdigest():
        raise ValueError("target-081 SMT hash drifted")
    if "(check-sat" not in text:
        raise ValueError("target-081 SMT has no solver query")
    if metadata["purpose"] == PRIVATE_SOURCE:
        accepted_private_smt.validate_obligation(
            text,
            accepted_private_smt.obligation_metadata(
                accepted_private_smt.FULL
            ),
        )
        return
    required = (
        {
            "SourceOrderingAdapter",
            "ComparatorObservation",
            "SourcePublicFinish",
        }
        if metadata["purpose"] == ADAPTER_SOURCE
        else {"ExactSort", "TargetAdapterIsLess", "FinishPublic081"}
    )
    if not required <= set(
        name
        for name in required
        if f"(define-fun {name}" in text
    ):
        raise ValueError("target-081 source adapter transition is incomplete")
    forbidden = (
        "declare-fun WholeSort",
        "declare-fun PrivateSort",
        "precomputed_terminal",
    )
    if any(item in text for item in forbidden):
        raise ValueError("target-081 SMT contains an opaque result relation")
