#!/usr/bin/env python3
"""SMT obligations for target-082 key lifecycle and sort composition."""

from __future__ import annotations

from functools import cache
from hashlib import sha256
from typing import Any

import target_080_operational_smt_v1 as accepted_private_smt
import target_082_operational_v1 as model


PRIVATE_SOURCE = "accepted-private-sort-source-correspondence"
ADAPTER_SOURCE = "key-ord-drop-adapter-source-correspondence"
FIXED_BOUNDARY = "fixed-boundary-exact-terminal-output-full-state"
PURPOSES = (PRIVATE_SOURCE, ADAPTER_SOURCE, FIXED_BOUNDARY)

PROBE_KINDS = (
    "normal-left-right-ord-right-drop-left-drop",
    "duplicate-owned-key-identities",
    "left-key-panic-prefix",
    "right-key-panic-left-unwind-drop",
    "ord-panic-right-left-unwind-drop",
    "right-drop-panic-left-unwind-drop",
    "left-drop-panic",
    "ord-panic-right-drop-double-panic-abort",
    "right-left-drop-double-panic-abort",
    "callback-and-interior-state",
    "normal-f-drop",
    "f-drop-double-panic-abort",
)
MUTATION_KINDS = (
    "left-right-key-order-swapped",
    "owned-key-identities-collapsed",
    "ord-panic-result-exposed",
    "right-before-left-drop-reversed",
    "callback-next-state-ignored",
    "observable-interior-state-ignored",
    "key-panic-ignored",
    "temporary-drop-panic-ignored",
    "f-drop-skipped",
    "double-panic-collapsed-to-panic",
)
CORRESPONDENCE_MUTATION_KINDS = (
    "source-left-key-observes-right-slot-and-source",
    "source-left-key-panic-event-result-changed",
    "source-public-abort-collapsed-to-panic",
)
COMPOSITION_REGRESSION_EXPECTATIONS = {
    "adapter-abort-preserved": "sat",
    "adapter-abort-to-panic-f-drop": "unsat",
    "adapter-panic-runs-f-drop": "sat",
    "adapter-normal-runs-f-drop": "sat",
}
CHECK_SAT = "(check-sat-using (then ctx-solver-simplify smt))"


def _adapter_preamble() -> str:
    return f"""\
; Target: {model.TARGET}
; Model: {model.MODEL_ID}
; Source: f(left), f(right), K::lt, drop(right K), drop(left K), then
; private-sort completion/unwind and drop(F). All schedules are derived.
(set-logic ALL)
(set-option :produce-models true)

(declare-datatypes ((KOwned 0))
  (((mkKOwned
      (ko_invocation Int)
      (ko_creation_state Int)
      (ko_slot Int)
      (ko_source Int)
      (ko_key Int)))))
(declare-datatypes ((KCallKey 0))
  (((mkKCallKey
      (kc_state Int)
      (kc_slot Int)
      (kc_source Int)
      (kc_interior (Array Int Int))))))
(declare-datatypes ((KOrdKey 0))
  (((mkKOrdKey
      (kord_state Int)
      (kord_left KOwned)
      (kord_right KOwned)
      (kord_interior (Array Int Int))))))
(declare-datatypes ((KDropKey 0))
  (((mkKDropKey
      (kd_state Int)
      (kd_owned KOwned)
      (kd_unwinding Bool)
      (kd_interior (Array Int Int))))))
(declare-datatypes ((KFDropKey 0))
  (((mkKFDropKey
      (kfd_state Int)
      (kfd_unwinding Bool)
      (kfd_interior (Array Int Int))))))
(declare-datatypes ((KPairKey 0))
  (((mkKPairKey (kp_left Int) (kp_right Int)))))
(declare-datatypes ((KBoundary 0))
  (((mkKBoundary
      (kb_initial_state Int)
      (kb_contract_key (Array Int Int))
      (kb_contract_ordering (Array KPairKey Int))
      (kb_key_value (Array KCallKey Int))
      (kb_key_next_state (Array KCallKey Int))
      (kb_key_next_interior (Array KCallKey (Array Int Int)))
      (kb_key_panics (Array KCallKey Bool))
      (kb_ord_is_less (Array KOrdKey Bool))
      (kb_ord_next_state (Array KOrdKey Int))
      (kb_ord_next_interior (Array KOrdKey (Array Int Int)))
      (kb_ord_panics (Array KOrdKey Bool))
      (kb_drop_next_state (Array KDropKey Int))
      (kb_drop_next_interior (Array KDropKey (Array Int Int)))
      (kb_drop_panics (Array KDropKey Bool))
      (kb_f_drop_next_state (Array KFDropKey Int))
      (kb_f_drop_next_interior
        (Array KFDropKey (Array Int Int)))
      (kb_f_drop_panics (Array KFDropKey Bool))
      (kb_interior_at_state (Array Int (Array Int Int)))))))
(declare-datatypes ((KKeyResult 0))
  (((mkKKeyResult
      (kkr_key Int)
      (kkr_state Int)
      (kkr_interior (Array Int Int))
      (kkr_panicked Bool)))))
(declare-datatypes ((KOrdResult 0))
  (((mkKOrdResult
      (kor_less Bool)
      (kor_state Int)
      (kor_interior (Array Int Int))
      (kor_panicked Bool)))))
(declare-datatypes ((KDropResult 0))
  (((mkKDropResult
      (kdr_state Int)
      (kdr_interior (Array Int Int))
      (kdr_panicked Bool)))))
(declare-datatypes ((KAdapterResult 0))
  (((mkKAdapterResult
      (kar_status Int)
      (kar_state Int)
      (kar_interior (Array Int Int))
      (kar_is_less Bool)
      (kar_result_available Bool)
      (kar_key_evaluations Int)
      (kar_ord_evaluations Int)
      (kar_right_drops Int)
      (kar_left_drops Int)
      (kar_event_code Int)
      (kar_has_left Bool)
      (kar_has_right Bool)
      (kar_left_owned KOwned)
      (kar_right_owned KOwned)))))
(declare-datatypes ((KPrivateResult 0))
  (((mkKPrivateResult
      (kpr_sequence (Array Int Int))
      (kpr_state Int)
      (kpr_status Int)))))
(declare-datatypes ((KPublicResult 0))
  (((mkKPublicResult
      (kpub_sequence (Array Int Int))
      (kpub_state Int)
      (kpub_interior (Array Int Int))
      (kpub_status Int)
      (kpub_unit Bool)
      (kpub_panicked Bool)
      (kpub_aborted Bool)
      (kpub_f_drop_invoked Bool)
      (kpub_f_drop_completed Bool)))))

(define-fun KObserveKey
  ((b KBoundary) (state Int) (slot Int) (source Int)
   (interior (Array Int Int))) KKeyResult
  (let ((call (mkKCallKey state slot source interior)))
    (mkKKeyResult
      (select (kb_key_value b) call)
      (select (kb_key_next_state b) call)
      (select (kb_key_next_interior b) call)
      (select (kb_key_panics b) call))))
(define-fun KObserveOrd
  ((b KBoundary) (state Int) (left KOwned) (right KOwned)
   (interior (Array Int Int))) KOrdResult
  (let ((call (mkKOrdKey state left right interior)))
    (mkKOrdResult
      (select (kb_ord_is_less b) call)
      (select (kb_ord_next_state b) call)
      (select (kb_ord_next_interior b) call)
      (select (kb_ord_panics b) call))))
(define-fun KObserveDrop
  ((b KBoundary) (state Int) (owned KOwned) (unwinding Bool)
   (interior (Array Int Int))) KDropResult
  (let ((call (mkKDropKey state owned unwinding interior)))
    (mkKDropResult
      (select (kb_drop_next_state b) call)
      (select (kb_drop_next_interior b) call)
      (select (kb_drop_panics b) call))))
(define-fun KObserveFDrop
  ((b KBoundary) (state Int) (unwinding Bool)
   (interior (Array Int Int))) KDropResult
  (let ((call (mkKFDropKey state unwinding interior)))
    (mkKDropResult
      (select (kb_f_drop_next_state b) call)
      (select (kb_f_drop_next_interior b) call)
      (select (kb_f_drop_panics b) call))))

(define-fun KCleanupLeftAfterRightKeyPanic
  ((b KBoundary) (left KOwned) (state Int)
   (interior (Array Int Int))) KAdapterResult
  (let ((left_drop (KObserveDrop b state left true interior)))
    (mkKAdapterResult
      (ite (kdr_panicked left_drop) 2 1)
      (kdr_state left_drop)
      (kdr_interior left_drop)
      false false 2 0 0 1
      (ite (kdr_panicked left_drop) 1219 1215)
      true false left left)))

(define-fun KCleanupTwo
  ((b KBoundary) (left KOwned) (right KOwned) (state Int)
   (interior (Array Int Int)) (already_unwinding Bool)
   (resolved_less Bool)) KAdapterResult
  (let ((right_drop
          (KObserveDrop b state right already_unwinding interior)))
    (ite
      (and already_unwinding (kdr_panicked right_drop))
      (mkKAdapterResult
        2 (kdr_state right_drop) (kdr_interior right_drop)
        false false 2 1 1 0 12349 true true left right)
      (let ((unwinding
              (or already_unwinding (kdr_panicked right_drop))))
        (let ((left_drop
                (KObserveDrop
                  b
                  (kdr_state right_drop)
                  left
                  unwinding
                  (kdr_interior right_drop))))
          (let ((status
                  (ite
                    (kdr_panicked left_drop)
                    (ite unwinding 2 1)
                    (ite unwinding 1 0))))
            (mkKAdapterResult
              status
              (kdr_state left_drop)
              (kdr_interior left_drop)
              (and (= status 0) resolved_less)
              (= status 0)
              2 1 1 1
              (ite (= status 0) 12345
                (ite (= status 1) 12347 12349))
              true true left right)))))))

(define-fun SourceKeyAdapter
  ((b KBoundary) (state Int) (left_source Int) (right_source Int)
   (interior (Array Int Int)) (invocation Int)) KAdapterResult
  (let ((left_key (KObserveKey b state 0 left_source interior)))
    (let ((left_owned
            (mkKOwned
              invocation state 0 left_source (kkr_key left_key))))
      (ite
        (kkr_panicked left_key)
        (mkKAdapterResult
          1 (kkr_state left_key) (kkr_interior left_key)
          false false 1 0 0 0 19 false false
          left_owned left_owned)
        (let ((right_key
                (KObserveKey
                  b
                  (kkr_state left_key)
                  1
                  right_source
                  (kkr_interior left_key))))
          (let ((right_owned
                  (mkKOwned
                    invocation
                    (kkr_state left_key)
                    1
                    right_source
                    (kkr_key right_key))))
            (ite
              (kkr_panicked right_key)
              (KCleanupLeftAfterRightKeyPanic
                b left_owned (kkr_state right_key)
                (kkr_interior right_key))
              (let ((ord
                      (KObserveOrd
                        b
                        (kkr_state right_key)
                        left_owned
                        right_owned
                        (kkr_interior right_key))))
                (KCleanupTwo
                  b left_owned right_owned
                  (kor_state ord)
                  (kor_interior ord)
                  (kor_panicked ord)
                  (kor_less ord))))))))))

(define-fun IndependentCleanupLeftAfterRightKeyPanic
  ((b KBoundary) (left KOwned) (state Int)
   (interior (Array Int Int))) KAdapterResult
  (let ((left_drop (KObserveDrop b state left true interior)))
    (mkKAdapterResult
      (ite (kdr_panicked left_drop) 2 1)
      (kdr_state left_drop)
      (kdr_interior left_drop)
      false false 2 0 0 1
      (ite (kdr_panicked left_drop) 1219 1215)
      true false left left)))

(define-fun IndependentCleanupTwo
  ((b KBoundary) (left KOwned) (right KOwned) (state Int)
   (interior (Array Int Int)) (already_unwinding Bool)
   (resolved_less Bool)) KAdapterResult
  (let ((right_drop
          (KObserveDrop b state right already_unwinding interior)))
    (ite
      (and already_unwinding (kdr_panicked right_drop))
      (mkKAdapterResult
        2 (kdr_state right_drop) (kdr_interior right_drop)
        false false 2 1 1 0 12349 true true left right)
      (let ((unwinding
              (or already_unwinding (kdr_panicked right_drop))))
        (let ((left_drop
                (KObserveDrop
                  b
                  (kdr_state right_drop)
                  left
                  unwinding
                  (kdr_interior right_drop))))
          (let ((status
                  (ite
                    (kdr_panicked left_drop)
                    (ite unwinding 2 1)
                    (ite unwinding 1 0))))
            (mkKAdapterResult
              status
              (kdr_state left_drop)
              (kdr_interior left_drop)
              (and (= status 0) resolved_less)
              (= status 0)
              2 1 1 1
              (ite (= status 0) 12345
                (ite (= status 1) 12347 12349))
              true true left right)))))))

(define-fun IndependentKeyAdapter
  ((b KBoundary) (state Int) (left_source Int) (right_source Int)
   (interior (Array Int Int)) (invocation Int)) KAdapterResult
  (let ((left_key (KObserveKey b state 0 left_source interior)))
    (let ((left_owned
            (mkKOwned
              invocation state 0 left_source (kkr_key left_key))))
      (ite
        (kkr_panicked left_key)
        (mkKAdapterResult
          1 (kkr_state left_key) (kkr_interior left_key)
          false false 1 0 0 0 19 false false
          left_owned left_owned)
        (let ((right_key
                (KObserveKey
                  b
                  (kkr_state left_key)
                  1
                  right_source
                  (kkr_interior left_key))))
          (let ((right_owned
                  (mkKOwned
                    invocation
                    (kkr_state left_key)
                    1
                    right_source
                    (kkr_key right_key))))
            (ite
              (kkr_panicked right_key)
              (IndependentCleanupLeftAfterRightKeyPanic
                b left_owned (kkr_state right_key)
                (kkr_interior right_key))
              (let ((ord
                      (KObserveOrd
                        b
                        (kkr_state right_key)
                        left_owned
                        right_owned
                        (kkr_interior right_key))))
                (IndependentCleanupTwo
                  b left_owned right_owned
                  (kor_state ord)
                  (kor_interior ord)
                  (kor_panicked ord)
                  (kor_less ord))))))))))

(define-fun SourcePublicFinish082
  ((b KBoundary) (private KPrivateResult)
   (interior (Array Int Int))) KPublicResult
  (ite
    (= (kpr_status private) 2)
    (mkKPublicResult
      (kpr_sequence private) (kpr_state private) interior
      2 false false true false false)
    (let ((unwinding (= (kpr_status private) 1)))
      (let ((d
              (KObserveFDrop
                b (kpr_state private) unwinding interior)))
        (let ((status
                (ite
                  (kdr_panicked d)
                  (ite unwinding 2 1)
                  (ite unwinding 1 0))))
          (mkKPublicResult
            (kpr_sequence private)
            (kdr_state d)
            (kdr_interior d)
            status
            (= status 0)
            (= status 1)
            (= status 2)
            true
            (not (kdr_panicked d))))))))

(define-fun IndependentPublicFinish082
  ((b KBoundary) (private KPrivateResult)
   (interior (Array Int Int))) KPublicResult
  (ite
    (= (kpr_status private) 2)
    (mkKPublicResult
      (kpr_sequence private) (kpr_state private) interior
      2 false false true false false)
    (let ((unwinding (= (kpr_status private) 1)))
      (let ((d
              (KObserveFDrop
                b (kpr_state private) unwinding interior)))
        (let ((status
                (ite
                  (kdr_panicked d)
                  (ite unwinding 2 1)
                  (ite unwinding 1 0))))
          (mkKPublicResult
            (kpr_sequence private)
            (kdr_state d)
            (kdr_interior d)
            status
            (= status 0)
            (= status 1)
            (= status 2)
            true
            (not (kdr_panicked d))))))))
"""


def adapter_source_correspondence_text() -> str:
    return (
        _adapter_preamble()
        + """\
(declare-const boundary KBoundary)
(declare-const state Int)
(declare-const left Int)
(declare-const right Int)
(declare-const interior (Array Int Int))
(declare-const invocation Int)
(declare-const private KPrivateResult)
(assert
  (or
    (not
      (=
        (SourceKeyAdapter
          boundary state left right interior invocation)
        (IndependentKeyAdapter
          boundary state left right interior invocation)))
    (not
      (=
        (SourcePublicFinish082 boundary private interior)
        (IndependentPublicFinish082 boundary private interior)))))
"""
        + CHECK_SAT
        + "\n"
    )


def correspondence_mutation_text(kind: str) -> str:
    mutations = {
        "source-left-key-observes-right-slot-and-source": (
            "(define-fun SourceKeyAdapter",
            "(define-fun IndependentCleanupLeftAfterRightKeyPanic",
            "(KObserveKey b state 0 left_source interior)",
            "(KObserveKey b state 1 right_source interior)",
        ),
        "source-left-key-panic-event-result-changed": (
            "(define-fun SourceKeyAdapter",
            "(define-fun IndependentCleanupLeftAfterRightKeyPanic",
            "false false 1 0 0 0 19 false false",
            "false false 1 0 0 0 29 false false",
        ),
        "source-public-abort-collapsed-to-panic": (
            "(define-fun SourcePublicFinish082",
            "(define-fun IndependentPublicFinish082",
            "2 false false true false false)",
            "1 false true false false false)",
        ),
    }
    if kind not in CORRESPONDENCE_MUTATION_KINDS:
        raise ValueError(
            f"unknown target-082 correspondence mutation: {kind}"
        )
    text = adapter_source_correspondence_text()
    start_marker, end_marker, old, new = mutations[kind]
    source_start = text.index(start_marker)
    source_end = text.index(end_marker, source_start)
    source = text[source_start:source_end]
    if source.count(old) != 1:
        raise ValueError(
            f"{kind}: source-only mutation anchor is not unique"
        )
    mutated_source = source.replace(old, new, 1)
    return (
        f"; Source-only correspondence mutation: {kind}\n"
        + text[:source_start]
        + mutated_source
        + text[source_end:]
    )


def private_source_correspondence_text() -> str:
    return accepted_private_smt.obligation_text(
        accepted_private_smt.FULL
    )


def _without_header(text: str) -> str:
    return "\n".join(
        line
        for line in text.splitlines()
        if not line.startswith("(set-logic")
        and not line.startswith("(set-option")
    ) + "\n"


@cache
def _composition_preamble() -> str:
    return (
        accepted_private_smt._base_preamble()
        + _without_header(_adapter_preamble())
        + """\
(define-fun KEncodePrivateState082
  ((callback_state Int) (status Int)) Int
  (+ (* 3 callback_state) status))

(define-fun KPrivateCallbackState082 ((encoded Int)) Int
  (div encoded 3))

(define-fun KPrivateTerminalStatus082 ((encoded Int)) Int
  (mod encoded 3))

(define-fun AdapterAtPrivateCall082
  ((b KBoundary) (call CallKey)) KAdapterResult
  (SourceKeyAdapter
    b
    (KPrivateCallbackState082 (call_state call))
    (call_left_identity call)
    (call_right_identity call)
    (select
      (kb_interior_at_state b)
      (KPrivateCallbackState082 (call_state call)))
    (call_state call)))

(define-fun ProjectBoundary082 ((b KBoundary)) Boundary
  (mkBoundary
    82
    (KEncodePrivateState082 (kb_initial_state b) 0)
    (lambda ((pair PairKey))
      (select
        (kb_contract_ordering b)
        (mkKPairKey
          (select
            (kb_contract_key b)
            (pair_left_identity pair))
          (select
            (kb_contract_key b)
            (pair_right_identity pair)))))
    (lambda ((call CallKey))
      (ite
        (kar_is_less (AdapterAtPrivateCall082 b call))
        -1
        1))
    (lambda ((call CallKey))
      (KEncodePrivateState082
        (kar_state (AdapterAtPrivateCall082 b call))
        (kar_status (AdapterAtPrivateCall082 b call))))
    (lambda ((call CallKey))
      (not
        (=
          (kar_status (AdapterAtPrivateCall082 b call))
          0)))))

(define-fun PrivateResult082 ((private ExactState)) KPrivateResult
  (mkKPrivateResult
    (e_sequence private)
    (KPrivateCallbackState082 (e_callback_state private))
    (KPrivateTerminalStatus082 (e_callback_state private))))

(define-fun FinishExact082
  ((b KBoundary) (private ExactState)) KPublicResult
  (let ((private082 (PrivateResult082 private)))
    (SourcePublicFinish082
      b
      private082
      (select (kb_interior_at_state b) (kpr_state private082)))))
"""
    )


@cache
def fixed_boundary_determinism_text() -> str:
    return (
        _composition_preamble()
        + """\

(declare-const boundary082 KBoundary)
(declare-const sequence082 (Array Int Int))
(declare-const configuration082 SortConfiguration)
(declare-const length082 Int)
(define-fun initial082 () ExactState
  (mkExactState
    sequence082
    (KEncodePrivateState082 (kb_initial_state boundary082) 0)
    false))
(define-fun execution_left082 () KPublicResult
  (FinishExact082
    boundary082
    (ExactSort
      initial082
      (ProjectBoundary082 boundary082)
      configuration082
      length082)))
(define-fun execution_right082 () KPublicResult
  (FinishExact082
    boundary082
    (ExactSort
      initial082
      (ProjectBoundary082 boundary082)
      configuration082
      length082)))
(assert (>= length082 0))
(assert (not (= execution_left082 execution_right082)))
"""
        + CHECK_SAT
        + "\n"
    )


def composition_regression_text(kind: str) -> str:
    if kind not in COMPOSITION_REGRESSION_EXPECTATIONS:
        raise ValueError(
            f"unknown target-082 composition regression: {kind}"
        )
    adapter_status = {
        "adapter-abort-preserved": 2,
        "adapter-abort-to-panic-f-drop": 2,
        "adapter-panic-runs-f-drop": 1,
        "adapter-normal-runs-f-drop": 0,
    }[kind]
    assertions = {
        "adapter-abort-preserved": """\
(assert
  (and
    (= (kpub_status regressionPublic082) 2)
    (not (kpub_unit regressionPublic082))
    (not (kpub_panicked regressionPublic082))
    (kpub_aborted regressionPublic082)
    (not (kpub_f_drop_invoked regressionPublic082))
    (not (kpub_f_drop_completed regressionPublic082))
    (= (kpub_sequence regressionPublic082) regressionSequence082)
    (= (kpub_state regressionPublic082)
       (kar_state regressionAdapter082))
    (= (kpub_interior regressionPublic082)
       (kar_interior regressionAdapter082))))
""",
        "adapter-abort-to-panic-f-drop": """\
(assert
  (and
    (= (kpub_status regressionPublic082) 1)
    (kpub_panicked regressionPublic082)
    (not (kpub_aborted regressionPublic082))
    (kpub_f_drop_invoked regressionPublic082)))
""",
        "adapter-panic-runs-f-drop": """\
(assert (not (kdr_panicked regressionFDrop082)))
(assert
  (and
    (= (kpub_status regressionPublic082) 1)
    (not (kpub_unit regressionPublic082))
    (kpub_panicked regressionPublic082)
    (not (kpub_aborted regressionPublic082))
    (kpub_f_drop_invoked regressionPublic082)
    (kpub_f_drop_completed regressionPublic082)
    (= (kpub_sequence regressionPublic082) regressionSequence082)
    (= (kpub_state regressionPublic082)
       (kdr_state regressionFDrop082))
    (= (kpub_interior regressionPublic082)
       (kdr_interior regressionFDrop082))))
""",
        "adapter-normal-runs-f-drop": """\
(assert (not (kdr_panicked regressionFDrop082)))
(assert
  (and
    (= (kpub_status regressionPublic082) 0)
    (kpub_unit regressionPublic082)
    (not (kpub_panicked regressionPublic082))
    (not (kpub_aborted regressionPublic082))
    (kpub_f_drop_invoked regressionPublic082)
    (kpub_f_drop_completed regressionPublic082)
    (= (kpub_state regressionPublic082)
       (kdr_state regressionFDrop082))
    (= (kpub_interior regressionPublic082)
       (kdr_interior regressionFDrop082))))
""",
    }[kind]
    return (
        _composition_preamble()
        + f"""\
(declare-const regressionBoundary082 KBoundary)
(define-fun regressionSequence082 () (Array Int Int)
  (store
    (store ((as const (Array Int Int)) 0) 0 10)
    1
    20))
(define-fun regressionInitial082 () ExactState
  (mkExactState
    regressionSequence082
    (KEncodePrivateState082
      (kb_initial_state regressionBoundary082)
      0)
    false))
(define-fun regressionCall082 () CallKey
  (mkCallKey
    (KEncodePrivateState082
      (kb_initial_state regressionBoundary082)
      0)
    20
    10))
(define-fun regressionAdapter082 () KAdapterResult
  (AdapterAtPrivateCall082
    regressionBoundary082
    regressionCall082))
; This is the first exact source callback in ExactSort's length-two
; insertion path, before any sequence write can occur.
(define-fun regressionPrivate082 () ExactState
  (ExactCallback
    regressionInitial082
    (ProjectBoundary082 regressionBoundary082)
    20
    10))
(define-fun regressionPrivateResult082 () KPrivateResult
  (PrivateResult082 regressionPrivate082))
(define-fun regressionPrivateInterior082 () (Array Int Int)
  (select
    (kb_interior_at_state regressionBoundary082)
    (kpr_state regressionPrivateResult082)))
(define-fun regressionFDrop082 () KDropResult
  (KObserveFDrop
    regressionBoundary082
    (kpr_state regressionPrivateResult082)
    (= (kpr_status regressionPrivateResult082) 1)
    regressionPrivateInterior082))
(define-fun regressionPublic082 () KPublicResult
  (FinishExact082 regressionBoundary082 regressionPrivate082))
(assert (= (kar_status regressionAdapter082) {adapter_status}))
(assert
  (=
    (select
      (kb_interior_at_state regressionBoundary082)
      (kar_state regressionAdapter082))
    (kar_interior regressionAdapter082)))
"""
        + assertions
        + CHECK_SAT
        + "\n"
    )


def nonvacuity_text() -> str:
    return (
        _adapter_preamble()
        + """\
(declare-const boundary KBoundary)
(declare-const interior (Array Int Int))
(define-fun adapter () KAdapterResult
  (SourceKeyAdapter boundary 0 10 20 interior 0))
(define-fun private () KPrivateResult
  (mkKPrivateResult ((as const (Array Int Int)) 0)
    (kar_state adapter) (kar_status adapter)))
(define-fun public () KPublicResult
  (SourcePublicFinish082 boundary private (kar_interior adapter)))
(assert (= (kar_status adapter) 0))
(assert (kar_result_available adapter))
(assert (= (kar_key_evaluations adapter) 2))
(assert (= (kar_ord_evaluations adapter) 1))
(assert (= (kar_right_drops adapter) 1))
(assert (= (kar_left_drops adapter) 1))
(assert (= (kpub_status public) 0))
"""
        + CHECK_SAT
        + "\n"
    )


def probe_text(kind: str) -> str:
    if kind not in PROBE_KINDS:
        raise ValueError(f"unknown target-082 probe: {kind}")
    assertions = {
        "normal-left-right-ord-right-drop-left-drop": (
            "(assert (and (= (kar_status adapter) 0) "
            "(= (kar_event_code adapter) 12345) "
            "(= (kar_key_evaluations adapter) 2) "
            "(= (kar_ord_evaluations adapter) 1) "
            "(= (kar_right_drops adapter) 1) "
            "(= (kar_left_drops adapter) 1)))"
        ),
        "duplicate-owned-key-identities": (
            "(assert (and (= (kar_status adapter) 0) "
            "(= (ko_key (kar_left_owned adapter)) "
            "(ko_key (kar_right_owned adapter))) "
            "(not (= (kar_left_owned adapter) "
            "(kar_right_owned adapter)))))"
        ),
        "left-key-panic-prefix": (
            "(assert (and (= (kar_status adapter) 1) "
            "(= (kar_key_evaluations adapter) 1) "
            "(= (kar_left_drops adapter) 0)))"
        ),
        "right-key-panic-left-unwind-drop": (
            "(assert (and (= (kar_status adapter) 1) "
            "(= (kar_key_evaluations adapter) 2) "
            "(= (kar_ord_evaluations adapter) 0) "
            "(= (kar_left_drops adapter) 1)))"
        ),
        "ord-panic-right-left-unwind-drop": (
            "(assert (and (= (kar_status adapter) 1) "
            "(= (kar_ord_evaluations adapter) 1) "
            "(= (kar_right_drops adapter) 1) "
            "(= (kar_left_drops adapter) 1) "
            "(not (kar_result_available adapter))))"
        ),
        "right-drop-panic-left-unwind-drop": (
            "(assert (and (= (kar_status adapter) 1) "
            "(= (kar_right_drops adapter) 1) "
            "(= (kar_left_drops adapter) 1)))"
        ),
        "left-drop-panic": (
            "(assert (and (= (kar_status adapter) 1) "
            "(= (kar_right_drops adapter) 1) "
            "(= (kar_left_drops adapter) 1)))"
        ),
        "ord-panic-right-drop-double-panic-abort": (
            "(assert (and (= (kar_status adapter) 2) "
            "(= (kar_right_drops adapter) 1) "
            "(= (kar_left_drops adapter) 0)))"
        ),
        "right-left-drop-double-panic-abort": (
            "(assert (and (= (kar_status adapter) 2) "
            "(= (kar_right_drops adapter) 1) "
            "(= (kar_left_drops adapter) 1)))"
        ),
        "callback-and-interior-state": (
            "(assert (and (not (= (kar_state adapter) 0)) "
            "(not (= (kar_interior adapter) interior))))"
        ),
        "normal-f-drop": (
            "(assert (and (= (kar_status adapter) 0) "
            "(kpub_f_drop_invoked public) "
            "(kpub_f_drop_completed public)))"
        ),
        "f-drop-double-panic-abort": (
            "(assert (and (= (kar_status adapter) 1) "
            "(= (kpub_status public) 2) "
            "(kpub_aborted public)))"
        ),
    }[kind]
    return (
        _adapter_preamble()
        + """\
(declare-const boundary KBoundary)
(declare-const interior (Array Int Int))
(define-fun adapter () KAdapterResult
  (SourceKeyAdapter boundary 0 10 20 interior 0))
(define-fun private () KPrivateResult
  (mkKPrivateResult
    ((as const (Array Int Int)) 0)
    (kar_state adapter)
    (kar_status adapter)))
(define-fun public () KPublicResult
  (SourcePublicFinish082 boundary private (kar_interior adapter)))
"""
        + assertions
        + "\n"
        + CHECK_SAT
        + "\n"
    )


def mutation_text(kind: str) -> str:
    if kind not in MUTATION_KINDS:
        raise ValueError(f"unknown target-082 mutation: {kind}")
    if kind in {
        "f-drop-skipped",
        "double-panic-collapsed-to-panic",
    }:
        status = (
            "(ite (= (kpub_status source) 2) 1 "
            "(kpub_status source))"
            if kind == "double-panic-collapsed-to-panic"
            else "(kpr_status private)"
        )
        invoked = (
            "false" if kind == "f-drop-skipped"
            else "(kpub_f_drop_invoked source)"
        )
        return (
            _adapter_preamble()
            + f"""\
(declare-const boundary KBoundary)
(declare-const private KPrivateResult)
(declare-const interior (Array Int Int))
(define-fun source () KPublicResult
  (SourcePublicFinish082 boundary private interior))
(define-fun mutated () KPublicResult
  (mkKPublicResult
    (kpub_sequence source)
    (kpub_state source)
    (kpub_interior source)
    {status}
    (= {status} 0)
    (= {status} 1)
    (= {status} 2)
    {invoked}
    (kpub_f_drop_completed source)))
(assert (not (= source mutated)))
"""
            + CHECK_SAT
            + "\n"
        )

    fields = {
        "left-right-key-order-swapped": {
            "event": "(+ (kar_event_code source) 1)"
        },
        "owned-key-identities-collapsed": {
            "right_owned": "(kar_left_owned source)"
        },
        "ord-panic-result-exposed": {
            "available": "true",
            "less": "(kor_less (KObserveOrd boundary state "
            "(kar_left_owned source) (kar_right_owned source) "
            "(kar_interior source)))",
        },
        "right-before-left-drop-reversed": {
            "event": "(+ (kar_event_code source) 2)"
        },
        "callback-next-state-ignored": {"state": "state"},
        "observable-interior-state-ignored": {"interior": "interior"},
        "key-panic-ignored": {"status": "0"},
        "temporary-drop-panic-ignored": {"status": "0"},
    }[kind]
    value = {
        "status": "(kar_status source)",
        "state": "(kar_state source)",
        "interior": "(kar_interior source)",
        "less": "(kar_is_less source)",
        "available": "(kar_result_available source)",
        "event": "(kar_event_code source)",
        "right_owned": "(kar_right_owned source)",
    }
    value.update(fields)
    return (
        _adapter_preamble()
        + f"""\
(declare-const boundary KBoundary)
(declare-const state Int)
(declare-const left Int)
(declare-const right Int)
(declare-const interior (Array Int Int))
(declare-const invocation Int)
(define-fun source () KAdapterResult
  (SourceKeyAdapter
    boundary state left right interior invocation))
(define-fun mutated () KAdapterResult
  (mkKAdapterResult
    {value['status']}
    {value['state']}
    {value['interior']}
    {value['less']}
    {value['available']}
    (kar_key_evaluations source)
    (kar_ord_evaluations source)
    (kar_right_drops source)
    (kar_left_drops source)
    {value['event']}
    (kar_has_left source)
    (kar_has_right source)
    (kar_left_owned source)
    {value['right_owned']}))
(assert (not (= source mutated)))
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
    raise ValueError(f"unknown target-082 obligation purpose: {purpose}")


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
        "source_backing": {
            PRIVATE_SOURCE: (
                "accepted target-080 Rust 1.96 private unstable-sort "
                "transition"
            ),
            ADAPTER_SOURCE: (
                "core/src/slice/mod.rs:3240-3246 plus Rust 1.96 MIR "
                "temporary cleanup and Drop glue"
            ),
            FIXED_BOUNDARY: (
                "accepted ExactSort composed with SourceKeyAdapter and "
                "SourcePublicFinish082"
            ),
        }[purpose],
        "boundary_fields": [
            "total f transition",
            "total K::lt transition",
            "total owned-K Drop transition",
            "total owned-F Drop transition",
            "complete callback and element-interior state transitions",
            "state-independent contract key and total order projection",
        ],
        "prohibited_boundary_fields": [
            "realized schedule",
            "temporary lifetime",
            "pivot",
            "swap",
            "write",
            "output",
            "permutation",
            "final state",
            "trace",
            "precomputed terminal result",
        ],
    }


def validate_obligation(text: str, metadata: dict[str, Any]) -> None:
    if metadata["sha256"] != sha256(text.encode()).hexdigest():
        raise ValueError("target-082 operational SMT hash drifted")
    if "(check-sat" not in text:
        raise ValueError("target-082 operational SMT has no solver query")
    purpose = metadata["purpose"]
    required = {
        PRIVATE_SOURCE: {"ExactSort", "TargetAdapterIsLess"},
        ADAPTER_SOURCE: {
            "SourceKeyAdapter",
            "IndependentKeyAdapter",
            "SourcePublicFinish082",
            "IndependentPublicFinish082",
        },
        FIXED_BOUNDARY: {
            "ExactSort",
            "ProjectBoundary082",
            "SourceKeyAdapter",
            "KEncodePrivateState082",
            "KPrivateTerminalStatus082",
            "PrivateResult082",
            "FinishExact082",
        },
    }[purpose]
    for symbol in required:
        if symbol not in text:
            raise ValueError(f"target-082 SMT lacks {symbol}")
    if purpose == ADAPTER_SOURCE:
        adapter_start = text.index(
            "(define-fun IndependentCleanupLeftAfterRightKeyPanic"
        )
        adapter_end = text.index(
            "(define-fun SourcePublicFinish082", adapter_start
        )
        independent_adapter = text[adapter_start:adapter_end]
        for forbidden in (
            "(SourceKeyAdapter",
            "(KCleanupLeftAfterRightKeyPanic",
            "(KCleanupTwo",
        ):
            if forbidden in independent_adapter:
                raise ValueError(
                    "target-082 independent adapter delegates to source"
                )
        for direct_step in (
            "(KObserveKey",
            "(KObserveOrd",
            "(KObserveDrop",
        ):
            if direct_step not in independent_adapter:
                raise ValueError(
                    "target-082 independent adapter is not source-complete"
                )
        finish_start = text.index(
            "(define-fun IndependentPublicFinish082"
        )
        finish_end = text.index(
            "(declare-const boundary KBoundary)", finish_start
        )
        independent_finish = text[finish_start:finish_end]
        if (
            "(SourcePublicFinish082" in independent_finish
            or "(KObserveFDrop" not in independent_finish
        ):
            raise ValueError(
                "target-082 independent public finish delegates to source"
            )
    boundary_start = (
        text.find("(declare-datatypes ((KBoundary 0))")
        if purpose != PRIVATE_SOURCE
        else -1
    )
    if boundary_start >= 0:
        boundary_end = text.find(
            "(declare-datatypes ((KKeyResult 0))", boundary_start
        )
        boundary = text[boundary_start:boundary_end].lower()
        for forbidden in (
            "schedule",
            "pivot",
            "swap",
            "output",
            "final_state",
            "trace",
        ):
            if forbidden in boundary:
                raise ValueError(
                    f"target-082 boundary contains {forbidden}"
                )
