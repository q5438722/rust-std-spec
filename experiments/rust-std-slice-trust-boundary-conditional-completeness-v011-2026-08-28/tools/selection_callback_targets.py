#!/usr/bin/env python3
"""Source-backed obligations for callback-driven selection targets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


PRIMARY = "completeness-modulo-reviewed-selection-equivalence"
EXACT = "exact-return-final-slice-and-callback-state"
PURPOSES = (PRIMARY,)

OUTPUT_FIELDS = (
    ("y_left_ref", "Reference"),
    ("y_pivot_ref", "Reference"),
    ("y_right_ref", "Reference"),
    ("y_left_len", "Int"),
    ("y_pivot_identity", "Int"),
    ("y_right_len", "Int"),
)
STATE_FIELDS = (
    ("s_final_sequence", "Array Int Int"),
    ("s_final_allocation", "Int"),
    ("s_final_borrow", "Int"),
    ("s_final_length", "Int"),
    ("s_callback_state", "Int"),
    ("s_panicked", "Bool"),
)
SOURCE_TRANSITIONS = (
    "BoundsTransition",
    "SmallSortTransition",
    "NormalReturnTransition",
    "FinalReturnedSubsliceTransition",
)
ACTIVE_CONJUNCTS = (
    "ActiveFinalConcatConjunct",
    "ActiveLeftLengthConjunct",
    "ActivePivotAtIndexConjunct",
    "ActiveRightLengthConjunct",
    "ActivePermutationConjunct",
    "ActiveCallbackPartitionConjunct",
)


@dataclass(frozen=True)
class TargetConfig:
    target: str
    input_order: str
    artifact_id: str
    active_contract_sha256: str
    active_contract_text: str
    mode: str
    target_source: str
    public_docs: str
    selection_source: str
    partition_source: str
    small_sort_source: str
    vocabulary_source: str
    admitted_trust_site: str
    excluded_trust_sites: tuple[str, ...]
    context_only_trust_sites: tuple[str, ...]
    all_trust_sites: tuple[str, ...]
    replacement_id: str
    proof_filename: str
    verus_expected_summary: str


def _check_config(config: TargetConfig) -> None:
    if config.mode not in {"compare", "key"}:
        raise ValueError(f"{config.target}: unknown callback-selection mode")
    if config.admitted_trust_site not in config.all_trust_sites:
        raise ValueError(f"{config.target}: admitted trust site is not audited")
    dispositions = (
        {config.admitted_trust_site}
        | set(config.excluded_trust_sites)
        | set(config.context_only_trust_sites)
    )
    if dispositions != set(config.all_trust_sites):
        raise ValueError(f"{config.target}: trust dispositions do not partition")


def missing_source_phases(config: TargetConfig) -> tuple[str, ...]:
    phases = (
        "choose_pivot mutation and callback schedule",
        "lower partition intermediate mutation and callback schedule",
        "introselect window narrowing and ancestor-pivot branch",
        "16-step median-of-medians fallback",
        "introselect panic prefixes and unwind mutation",
    )
    if config.mode == "key":
        return (
            *phases,
            "temporary key Drop order, callback-visible state, and panic",
        )
    return phases


def _boundary_relation_fields(config: TargetConfig) -> str:
    if config.mode == "compare":
        return """\
      (b_compare_ordering_relation
        (Array Int
          (Array Int
            (Array Int Int))))
      (b_compare_next_state_relation
        (Array Int
          (Array Int
            (Array Int Int))))
      (b_compare_panic_relation
        (Array Int
          (Array Int
            (Array Int Bool))))"""
    return """\
      (b_key_result_relation
        (Array Int
          (Array Int Int)))
      (b_key_next_state_relation
        (Array Int
          (Array Int Int)))
      (b_key_panic_relation
        (Array Int
          (Array Int Bool)))
      (b_ord_lt_result_relation
        (Array Int
          (Array Int
            (Array Int
              Bool))))
      (b_ord_lt_next_state_relation
        (Array Int
          (Array Int
            (Array Int
              Int))))
      (b_ord_lt_panic_relation
        (Array Int
          (Array Int
            (Array Int
              Bool))))"""


def _callback_definitions(config: TargetConfig) -> str:
    if config.mode == "compare":
        return """\
(define-fun CompareStep
  ((b Boundary)
   (state Int)
   (left Int)
   (right Int)
   (ordering Int)
   (next_state Int)
   (panicked Bool)) Bool
  (and
    (= ordering
       (select
         (select
           (select (b_compare_ordering_relation b) state)
           left)
         right))
    (<= -1 ordering)
    (<= ordering 1)
    (= next_state
       (select
         (select
           (select (b_compare_next_state_relation b) state)
           left)
         right))
    (= panicked
       (select
         (select
           (select (b_compare_panic_relation b) state)
           left)
         right))))
(define-fun CallbackTransitionFunctional ((b Boundary)) Bool
  (forall
    ((state Int)
     (left Int)
     (right Int)
     (ordering1 Int)
     (next_state1 Int)
     (panicked1 Bool)
     (ordering2 Int)
     (next_state2 Int)
     (panicked2 Bool))
    (=>
      (and
        (CompareStep
          b state left right ordering1 next_state1 panicked1)
        (CompareStep
          b state left right ordering2 next_state2 panicked2))
      (and
        (= ordering1 ordering2)
        (= next_state1 next_state2)
        (= panicked1 panicked2)))))
(define-fun AdapterNormal
  ((b Boundary)
   (state Int)
   (left Int)
   (right Int)
   (is_less Bool)
   (next_state Int)) Bool
  (exists ((ordering Int))
    (and
      (<= -1 ordering)
      (<= ordering 1)
      (CompareStep
        b
        state
        left
        right
        ordering
        next_state
        false)
      (= is_less (= ordering -1)))))
(define-fun AdapterPanic
  ((b Boundary)
   (state Int)
   (left Int)
   (right Int)
   (next_state Int)) Bool
  (exists ((ordering Int))
    (and
      (<= -1 ordering)
      (<= ordering 1)
      (CompareStep
        b
        state
        left
        right
        ordering
        next_state
        true))))
(define-fun ContractLeq
  ((b Boundary) (left Int) (right Int)) Bool
  (let
    ((ordering
       (select
         (select
           (select
             (b_compare_ordering_relation b)
             (b_initial_callback_state b))
           left)
         right)))
    (and
      (<= -1 ordering)
      (<= ordering 0)
      (not
        (select
          (select
            (select
              (b_compare_panic_relation b)
              (b_initial_callback_state b))
            left)
          right)))))
(define-fun FastContractLeq
  ((b Boundary) (left Int) (right Int)) Bool
  (ContractLeq b left right))"""
    return """\
(define-fun KeyStep
  ((b Boundary)
   (state Int)
   (value Int)
   (key Int)
   (next_state Int)
   (panicked Bool)) Bool
  (and
    (= key
       (select
         (select (b_key_result_relation b) state)
         value))
    (= next_state
       (select
         (select (b_key_next_state_relation b) state)
         value))
    (= panicked
       (select
         (select (b_key_panic_relation b) state)
         value))))
(define-fun OrdLtStep
  ((b Boundary)
   (state Int)
   (left_key Int)
   (right_key Int)
   (is_less Bool)
   (next_state Int)
   (panicked Bool)) Bool
  (and
    (= is_less
       (select
         (select
           (select (b_ord_lt_result_relation b) state)
           left_key)
         right_key))
    (= next_state
       (select
         (select
           (select (b_ord_lt_next_state_relation b) state)
           left_key)
         right_key))
    (= panicked
       (select
         (select
           (select (b_ord_lt_panic_relation b) state)
           left_key)
         right_key))))
(define-fun CallbackTransitionFunctional ((b Boundary)) Bool
  (and
    (forall
      ((state Int)
       (value Int)
       (key1 Int)
       (next_state1 Int)
       (panicked1 Bool)
       (key2 Int)
       (next_state2 Int)
       (panicked2 Bool))
      (=>
        (and
          (KeyStep b state value key1 next_state1 panicked1)
          (KeyStep b state value key2 next_state2 panicked2))
        (and
          (= key1 key2)
          (= next_state1 next_state2)
          (= panicked1 panicked2))))
    (forall
      ((state Int)
       (left_key Int)
       (right_key Int)
       (is_less1 Bool)
       (next_state1 Int)
       (panicked1 Bool)
       (is_less2 Bool)
       (next_state2 Int)
       (panicked2 Bool))
      (=>
        (and
          (OrdLtStep
            b state left_key right_key
            is_less1 next_state1 panicked1)
          (OrdLtStep
            b state left_key right_key
            is_less2 next_state2 panicked2))
        (and
          (= is_less1 is_less2)
          (= next_state1 next_state2)
          (= panicked1 panicked2))))))
(define-fun AdapterNormal
  ((b Boundary)
   (state Int)
   (left Int)
   (right Int)
   (is_less Bool)
   (next_state Int)) Bool
  (exists
    ((left_key Int)
     (after_left Int)
     (right_key Int)
     (after_right Int))
    (and
      (KeyStep
        b
        state
        left
        left_key
        after_left
        false)
      (KeyStep
        b
        after_left
        right
        right_key
        after_right
        false)
      (OrdLtStep
        b
        after_right
        left_key
        right_key
        is_less
        next_state
        false))))
(define-fun AdapterNormalFast
  ((b Boundary)
   (state Int)
   (left Int)
   (right Int)
   (is_less Bool)
   (next_state Int)) Bool
  (and
    (KeyStep
      b
      state
      left
      (select (select (b_key_result_relation b) state) left)
      (select (select (b_key_next_state_relation b) state) left)
      false)
    (let
      ((after_left
         (select (select (b_key_next_state_relation b) state) left)))
      (exists ((right_key Int) (after_right Int))
        (and
          (KeyStep b after_left right right_key after_right false)
          (OrdLtStep
            b
            after_right
            (select (select (b_key_result_relation b) state) left)
            right_key
            is_less
            next_state
            false))))
    ))
(define-fun AdapterPanic
  ((b Boundary)
   (state Int)
   (left Int)
   (right Int)
   (next_state Int)) Bool
  (or
    (exists ((left_key Int))
      (KeyStep
        b
        state
        left
        left_key
        next_state
        true))
    (exists ((left_key Int) (after_left Int) (right_key Int))
      (and
        (KeyStep
          b
          state
          left
          left_key
          after_left
          false)
        (KeyStep
          b
          after_left
          right
          right_key
          next_state
          true)))
    (exists
      ((left_key Int)
       (after_left Int)
       (right_key Int)
       (after_right Int)
       (is_less Bool))
      (and
        (KeyStep
          b
          state
          left
          left_key
          after_left
          false)
        (KeyStep
          b
          after_left
          right
          right_key
          after_right
          false)
        (OrdLtStep
          b
          after_right
          left_key
          right_key
          is_less
          next_state
          true)))))
(define-fun MayCompareLess
  ((b Boundary) (left Int) (right Int)) Bool
  (exists ((next_state Int))
    (AdapterNormal
      b
      (b_initial_callback_state b)
      left
      right
      true
      next_state)))
(define-fun ContractLeq
  ((b Boundary) (left Int) (right Int)) Bool
  (not (MayCompareLess b right left)))
(define-fun FastContractLeq
  ((b Boundary) (left Int) (right Int)) Bool
  (and
    (KeyStep
      b
      (b_initial_callback_state b)
      right
      right
      (+ (b_initial_callback_state b) 1)
      false)
    (KeyStep
      b
      (+ (b_initial_callback_state b) 1)
      left
      left
      (+ (b_initial_callback_state b) 2)
      false)
    (not
      (or
        (OrdLtStep
          b
          (+ (b_initial_callback_state b) 2)
          right
          left
          true
          (+ (b_initial_callback_state b) 3)
          false)
        (OrdLtStep
          b
          (+ (b_initial_callback_state b) 2)
          right
          left
          true
          (+ (b_initial_callback_state b) 4)
          false)))))"""


def _relation_available(config: TargetConfig) -> str:
    if config.mode == "compare":
        return """\
  (exists ((ordering Int) (next_state Int) (panicked Bool))
    (and
      (<= -1 ordering)
      (<= ordering 1)
      (CompareStep
        b
        (b_initial_callback_state b)
        (select (x_initial_sequence x) 0)
        (select (x_initial_sequence x) 0)
        ordering
        next_state
        panicked)))"""
    return """\
  (exists ((key Int) (key_state Int) (key_panicked Bool))
    (KeyStep
      b
      (b_initial_callback_state b)
      (select (x_initial_sequence x) 0)
      key
      key_state
      key_panicked))
  (exists
    ((left_key Int)
     (right_key Int)
     (is_less Bool)
     (next_state Int)
     (panicked Bool))
    (OrdLtStep
      b
      (b_initial_callback_state b)
      left_key
      right_key
      is_less
      next_state
      panicked))"""


def _equivalence_body(config: TargetConfig, purpose: str) -> str:
    equalities = [
        f"(= ({selector} y1) ({selector} y2))"
        for selector, _ in OUTPUT_FIELDS
    ]
    equalities.extend(
        f"(= ({selector} s1) ({selector} s2))"
        for selector, _ in STATE_FIELDS
    )
    return "  (and " + "\n       ".join(equalities) + "))"


def _drop_smt_definition(text: str, symbol: str) -> str:
    starts = [
        position
        for marker in (
            f"(define-fun {symbol}",
            f"(define-fun-rec {symbol}",
        )
        if (position := text.find(marker)) >= 0
    ]
    if len(starts) != 1:
        raise ValueError(f"{symbol}: expected exactly one SMT definition")
    start = starts[0]
    depth = 0
    for end in range(start, len(text)):
        if text[end] == "(":
            depth += 1
        elif text[end] == ")":
            depth -= 1
            if depth == 0:
                if end + 1 < len(text) and text[end + 1] == "\n":
                    end += 1
                return text[:start] + text[end + 1 :]
    raise ValueError(f"{symbol}: unterminated SMT definition")


def obligation_text(config: TargetConfig, purpose: str) -> str:
    _check_config(config)
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown obligation purpose {purpose}")
    fast_adapter = "AdapterNormal"
    text = f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Rust target: {config.target_source}
; Public docs: {config.public_docs}
; Private introselect: {config.selection_source}
; Lower partition: {config.partition_source}
; Purpose: {purpose}
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_length Int)
      (x_index Int)
      (x_allocation Int)
      (x_borrow Int)
      (x_initial_sequence (Array Int Int))
      (x_is_zst Bool)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_callback_identity Int)
      (b_initial_callback_state Int)
{_boundary_relation_fields(config)}))))
(declare-datatypes ((Reference 0))
  (((mkReference
      (ref_allocation Int)
      (ref_parent_borrow Int)
      (ref_start Int)
      (ref_span Int)
      (ref_projection_kind Int)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_left_ref Reference)
      (y_pivot_ref Reference)
      (y_right_ref Reference)
      (y_left_len Int)
      (y_pivot_identity Int)
      (y_right_len Int)))))
(declare-datatypes ((State 0))
  (((mkState
      (s_final_sequence (Array Int Int))
      (s_final_allocation Int)
      (s_final_borrow Int)
      (s_final_length Int)
      (s_callback_state Int)
      (s_panicked Bool)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun PositionInRange
  ((position Int) (start Int) (end Int)) Bool
  (and (<= start position) (< position end)))
{_callback_definitions(config)}
(define-fun IdentityInInput ((x Input) (identity Int)) Bool
  (or
    (= (select (x_initial_sequence x) 0) identity)
    (= (select (x_initial_sequence x) 1) identity)
    (= (select (x_initial_sequence x) 2) identity)
    (= (select (x_initial_sequence x) 3) identity)))
(define-fun ProfileCode
  ((b Boundary) (identity Int) (pivot Int)) Int
  (+ (ite (ContractLeq b identity pivot) 1 0)
     (ite (ContractLeq b pivot identity) 2 0)))
(define-fun SwapPositions
  ((sequence (Array Int Int)) (left Int) (right Int))
  (Array Int Int)
  (store
    (store sequence left (select sequence right))
    right
    (select sequence left)))
(define-fun SameProfileAt
  ((b Boundary)
   (sequence (Array Int Int))
   (pivot Int)
   (left Int)
   (right Int)) Bool
  (= (ProfileCode b (select sequence left) pivot)
     (ProfileCode b (select sequence right) pivot)))
(define-fun ReviewedFinalSequenceEquivalent
  ((x Input)
   (b Boundary)
   (y Output)
   (left State)
   (right State)) Bool
  (let
    ((sequence (s_final_sequence left))
     (candidate (s_final_sequence right))
     (pivot (y_pivot_identity y))
     (right_start (+ (x_index x) 1))
     (right_next (+ (x_index x) 2)))
    (ite
      (= candidate sequence)
      true
      (or
        (and
          (<= 2 (x_index x))
          (SameProfileAt b sequence pivot 0 1)
          (= candidate (SwapPositions sequence 0 1)))
        (and
          (< right_next (x_length x))
          (SameProfileAt b sequence pivot right_start right_next)
          (= candidate
             (SwapPositions sequence right_start right_next)))
        (and
          (<= 2 (x_index x))
          (< right_next (x_length x))
          (SameProfileAt b sequence pivot 0 1)
          (SameProfileAt b sequence pivot right_start right_next)
          (= candidate
             (SwapPositions
               (SwapPositions sequence 0 1)
               right_start
               right_next)))))))
(define-fun PermutationFromInput
  ((x Input) (s State)) Bool
  (exists ((o0 Int) (o1 Int) (o2 Int) (o3 Int))
    (and
      (PositionInRange o0 0 4)
      (PositionInRange o1 0 4)
      (PositionInRange o2 0 4)
      (PositionInRange o3 0 4)
      (distinct o0 o1 o2 o3)
      (= (select (s_final_sequence s) 0)
         (select (x_initial_sequence x) o0))
      (= (select (s_final_sequence s) 1)
         (select (x_initial_sequence x) o1))
      (= (select (s_final_sequence s) 2)
         (select (x_initial_sequence x) o2))
      (= (select (s_final_sequence s) 3)
         (select (x_initial_sequence x) o3)))))
(define-fun SameIdentityMultiplicity
  ((x Input) (left State) (right State)) Bool
  (ite
    (= (x_length x) 2)
    (or
      (and
        (= (select (s_final_sequence left) 0)
           (select (s_final_sequence right) 0))
        (= (select (s_final_sequence left) 1)
           (select (s_final_sequence right) 1)))
      (and
        (= (select (s_final_sequence left) 0)
           (select (s_final_sequence right) 1))
        (= (select (s_final_sequence left) 1)
           (select (s_final_sequence right) 0))))
    (exists ((matching (Array Int Int)))
      (and
        (forall ((position Int))
          (=>
            (PositionInRange position 0 (x_length x))
            (and
              (PositionInRange
                (select matching position) 0 (x_length x))
              (= (select (s_final_sequence left) position)
                 (select
                   (s_final_sequence right)
                   (select matching position))))))
        (forall ((first Int) (second Int))
          (=>
            (and
              (PositionInRange first 0 (x_length x))
              (PositionInRange second 0 (x_length x))
              (not (= first second)))
            (not
              (= (select matching first) (select matching second)))))))))
(define-fun PivotProfilesEqual
  ((x Input) (b Boundary) (left_pivot Int) (right_pivot Int)) Bool
  (ite
    (= (x_length x) 2)
    (and
      (= (ProfileCode
           b (select (x_initial_sequence x) 0) left_pivot)
         (ProfileCode
           b (select (x_initial_sequence x) 0) right_pivot))
      (= (ProfileCode
           b (select (x_initial_sequence x) 1) left_pivot)
         (ProfileCode
           b (select (x_initial_sequence x) 1) right_pivot)))
    (forall ((position Int))
      (=>
        (PositionInRange position 0 (x_length x))
        (= (ProfileCode
             b
             (select (x_initial_sequence x) position)
             left_pivot)
           (ProfileCode
             b
             (select (x_initial_sequence x) position)
             right_pivot))))))
(define-fun SideProfileMultiplicitiesEqual
  ((x Input)
   (b Boundary)
   (left_output Output)
   (left_state State)
   (right_output Output)
   (right_state State)
   (start Int)
   (end Int)) Bool
  (ite
    (and (= (x_length x) 2) (= (x_index x) 0))
    (or
      (= start end)
      (and
        (= start 1)
        (= end 2)
        (= (ProfileCode
             b
             (select (s_final_sequence left_state) 1)
             (y_pivot_identity left_output))
           (ProfileCode
             b
             (select (s_final_sequence right_state) 1)
             (y_pivot_identity right_output)))))
    (exists ((matching (Array Int Int)))
      (and
        (forall ((position Int))
          (=>
            (PositionInRange position start end)
            (and
              (PositionInRange (select matching position) start end)
              (= (ProfileCode
                   b
                   (select (s_final_sequence left_state) position)
                   (y_pivot_identity left_output))
                 (ProfileCode
                   b
                   (select
                     (s_final_sequence right_state)
                     (select matching position))
                   (y_pivot_identity right_output))))))
        (forall ((first Int) (second Int))
          (=>
            (and
              (PositionInRange first start end)
              (PositionInRange second start end)
              (not (= first second)))
            (not
              (= (select matching first) (select matching second)))))))))
(define-fun LeftReference ((x Input)) Reference
  (mkReference
    (x_allocation x) (x_borrow x) 0 (x_index x) 1))
(define-fun PivotReference ((x Input)) Reference
  (mkReference
    (x_allocation x) (x_borrow x) (x_index x) 1 2))
(define-fun RightReference ((x Input)) Reference
  (mkReference
    (x_allocation x)
    (x_borrow x)
    (+ (x_index x) 1)
    (- (x_length x) (x_index x) 1)
    3))
(define-fun NoCallCallbackState ((x Input) (b Boundary)) Int
  (+ (b_initial_callback_state b)
     (ite (x_is_zst x) 0 (- (x_length x) 1))))
(define-fun InputShapeValid ((x Input)) Bool
  (and
    (> (x_length x) 0)
    (<= 0 (x_index x))
    (< (x_index x) (x_length x))
    (>= (x_allocation x) 0)
    (>= (x_borrow x) 0)))
(define-fun CallbackBoundaryWellFormed
  ((x Input) (b Boundary)) Bool
  (and
    (>= (b_callback_identity b) 0)
    (>= (b_initial_callback_state b) 0)
    (CallbackTransitionFunctional b)
{_relation_available(config)}))
(define-fun SequenceSwapMatches
  ((x Input) (s State) (winner Int) (target Int)) Bool
  (and
    (PositionInRange winner 0 (x_length x))
    (PositionInRange target 0 (x_length x))
    (ite
      (= (x_length x) 2)
      (and
        (= (select (s_final_sequence s) 0)
           (ite
             (= target 0)
             (select (x_initial_sequence x) winner)
             (ite
               (= winner 0)
               (select (x_initial_sequence x) target)
               (select (x_initial_sequence x) 0))))
        (= (select (s_final_sequence s) 1)
           (ite
             (= target 1)
             (select (x_initial_sequence x) winner)
             (ite
               (= winner 1)
               (select (x_initial_sequence x) target)
               (select (x_initial_sequence x) 1)))))
      (forall ((position Int))
        (=>
          (PositionInRange position 0 (x_length x))
          (= (select (s_final_sequence s) position)
             (ite
               (= position target)
               (select (x_initial_sequence x) winner)
               (ite
                 (= position winner)
                 (select (x_initial_sequence x) target)
                 (select (x_initial_sequence x) position)))))))))
(define-fun ExtremeScanNormal
  ((x Input)
   (b Boundary)
   (s State)
   (find_min Bool)) Bool
  (ite
    (= (x_length x) 2)
    (or
      (and
        ({fast_adapter}
          b
          (b_initial_callback_state b)
          (select
            (x_initial_sequence x)
            (ite find_min 1 0))
          (select
            (x_initial_sequence x)
            (ite find_min 0 1))
          true
          (s_callback_state s))
        (SequenceSwapMatches x s 1 (x_index x)))
      (and
        ({fast_adapter}
          b
          (b_initial_callback_state b)
          (select
            (x_initial_sequence x)
            (ite find_min 1 0))
          (select
            (x_initial_sequence x)
            (ite find_min 0 1))
          false
          (s_callback_state s))
        (SequenceSwapMatches x s 0 (x_index x))))
    (exists
    ((accumulators (Array Int Int))
     (states (Array Int Int))
     (less_results (Array Int Bool)))
    (and
      (= (select accumulators 0) 0)
      (= (select states 0) (b_initial_callback_state b))
      (forall ((position Int))
        (=>
          (and (<= 1 position) (< position (x_length x)))
          (let
            ((accumulator (select accumulators (- position 1)))
             (candidate position)
             (state (select states (- position 1)))
             (next_state (select states position))
             (is_less (select less_results position)))
            (and
              (AdapterNormal
                b
                state
                (select
                  (x_initial_sequence x)
                  (ite find_min candidate accumulator))
                (select
                  (x_initial_sequence x)
                  (ite find_min accumulator candidate))
                is_less
                next_state)
              (= (select accumulators position)
                 (ite is_less candidate accumulator))))))
      (= (s_callback_state s)
         (select states (- (x_length x) 1)))
      (SequenceSwapMatches
        x
        s
        (select accumulators (- (x_length x) 1))
        (x_index x))))))
(define-fun SequenceAfterInsert
  ((sequence (Array Int Int)) (tail Int) (insertion Int))
  (Array Int Int)
  (ite
    (= tail 1)
    (ite
      (= insertion 0)
      (store
        (store sequence 1 (select sequence 0))
        0
        (select sequence 1))
      sequence)
    (ite
      (= tail 2)
      (ite
        (= insertion 0)
        (store
          (store
            (store sequence 2 (select sequence 1))
            1
            (select sequence 0))
          0
          (select sequence 2))
        (ite
          (= insertion 1)
          (store
            (store sequence 2 (select sequence 1))
            1
            (select sequence 2))
          sequence))
      (ite
        (= insertion 0)
        (store
          (store
            (store
              (store sequence 3 (select sequence 2))
              2
              (select sequence 1))
            1
            (select sequence 0))
          0
          (select sequence 3))
        (ite
          (= insertion 1)
          (store
            (store
              (store sequence 3 (select sequence 2))
              2
              (select sequence 1))
            1
            (select sequence 3))
          (ite
            (= insertion 2)
            (store
              (store sequence 3 (select sequence 2))
              2
              (select sequence 3))
            sequence))))))
(define-fun InsertTailNormal
  ((b Boundary)
   (sequence (Array Int Int))
   (tail Int)
   (state Int)
   (next_sequence (Array Int Int))
   (next_state Int)) Bool
  (or
    (and
      (= tail 1)
      (or
        (and
          (AdapterNormal
            b state (select sequence 1) (select sequence 0)
            false next_state)
          (= next_sequence sequence))
        (and
          (AdapterNormal
            b state (select sequence 1) (select sequence 0)
            true next_state)
          (= next_sequence (SequenceAfterInsert sequence 1 0)))))
    (and
      (= tail 2)
      (or
        (and
          (AdapterNormal
            b state (select sequence 2) (select sequence 1)
            false next_state)
          (= next_sequence sequence))
        (exists ((after_first Int))
          (and
            (AdapterNormal
              b state (select sequence 2) (select sequence 1)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 2) (select sequence 0)
              false next_state)
            (= next_sequence
               (SequenceAfterInsert sequence 2 1))))
        (exists ((after_first Int))
          (and
            (AdapterNormal
              b state (select sequence 2) (select sequence 1)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 2) (select sequence 0)
              true next_state)
            (= next_sequence
               (SequenceAfterInsert sequence 2 0))))))
    (and
      (= tail 3)
      (or
        (and
          (AdapterNormal
            b state (select sequence 3) (select sequence 2)
            false next_state)
          (= next_sequence sequence))
        (exists ((after_first Int))
          (and
            (AdapterNormal
              b state (select sequence 3) (select sequence 2)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 3) (select sequence 1)
              false next_state)
            (= next_sequence
               (SequenceAfterInsert sequence 3 2))))
        (exists ((after_first Int) (after_second Int))
          (and
            (AdapterNormal
              b state (select sequence 3) (select sequence 2)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 3) (select sequence 1)
              true after_second)
            (AdapterNormal
              b after_second (select sequence 3) (select sequence 0)
              false next_state)
            (= next_sequence
               (SequenceAfterInsert sequence 3 1))))
        (exists ((after_first Int) (after_second Int))
          (and
            (AdapterNormal
              b state (select sequence 3) (select sequence 2)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 3) (select sequence 1)
              true after_second)
            (AdapterNormal
              b after_second (select sequence 3) (select sequence 0)
              true next_state)
            (= next_sequence
               (SequenceAfterInsert sequence 3 0))))))))
(define-fun LengthFourInsertionSortNormal
  ((x Input) (b Boundary) (s State)) Bool
  (exists
    ((after_first_sequence (Array Int Int))
     (after_first_state Int)
     (after_second_sequence (Array Int Int))
     (after_second_state Int))
    (and
      (InsertTailNormal
        b
        (x_initial_sequence x)
        1
        (b_initial_callback_state b)
        after_first_sequence
        after_first_state)
      (InsertTailNormal
        b
        after_first_sequence
        2
        after_first_state
        after_second_sequence
        after_second_state)
      (InsertTailNormal
        b
        after_second_sequence
        3
        after_second_state
        (s_final_sequence s)
        (s_callback_state s)))))
(define-fun InsertTailPanic
  ((b Boundary)
   (sequence (Array Int Int))
   (tail Int)
   (state Int)
   (panic_sequence (Array Int Int))
   (panic_state Int)) Bool
  (and
    (<= 1 tail)
    (<= tail 3)
    (or
      (and
        (= panic_sequence sequence)
        (AdapterPanic
          b
          state
          (select sequence tail)
          (select sequence (- tail 1))
          panic_state))
      (and
        (= tail 2)
        (exists ((after_first Int))
          (and
            (AdapterNormal
              b state (select sequence 2) (select sequence 1)
              true after_first)
            (AdapterPanic
              b after_first (select sequence 2) (select sequence 0)
              panic_state)
            (= panic_sequence
               (SequenceAfterInsert sequence 2 1)))))
      (and
        (= tail 3)
        (exists ((after_first Int))
          (and
            (AdapterNormal
              b state (select sequence 3) (select sequence 2)
              true after_first)
            (AdapterPanic
              b after_first (select sequence 3) (select sequence 1)
              panic_state)
            (= panic_sequence
               (SequenceAfterInsert sequence 3 2)))))
      (and
        (= tail 3)
        (exists ((after_first Int) (after_second Int))
          (and
            (AdapterNormal
              b state (select sequence 3) (select sequence 2)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 3) (select sequence 1)
              true after_second)
            (AdapterPanic
              b after_second (select sequence 3) (select sequence 0)
              panic_state)
            (= panic_sequence
               (SequenceAfterInsert sequence 3 1))))))))
(define-fun LengthFourInsertionSortPanic
  ((x Input) (b Boundary) (s State)) Bool
  (or
    (InsertTailPanic
      b
      (x_initial_sequence x)
      1
      (b_initial_callback_state b)
      (s_final_sequence s)
      (s_callback_state s))
    (exists
      ((after_first_sequence (Array Int Int))
       (after_first_state Int))
      (and
        (InsertTailNormal
          b
          (x_initial_sequence x)
          1
          (b_initial_callback_state b)
          after_first_sequence
          after_first_state)
        (InsertTailPanic
          b
          after_first_sequence
          2
          after_first_state
          (s_final_sequence s)
          (s_callback_state s))))
    (exists
      ((after_first_sequence (Array Int Int))
       (after_first_state Int)
       (after_second_sequence (Array Int Int))
       (after_second_state Int))
      (and
        (InsertTailNormal
          b
          (x_initial_sequence x)
          1
          (b_initial_callback_state b)
          after_first_sequence
          after_first_state)
        (InsertTailNormal
          b
          after_first_sequence
          2
          after_first_state
          after_second_sequence
          after_second_state)
        (InsertTailPanic
          b
          after_second_sequence
          3
          after_second_state
          (s_final_sequence s)
          (s_callback_state s))))))
(define-fun NormalReturnTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (not (s_panicked s))
    (>= (b_callback_identity b) 0)
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))))
(define-fun PanicPrefixReachable
  ((x Input) (b Boundary) (s State)) Bool
  (and
    (= (x_length x) 4)
    (= (x_index x) 1)
    (not (x_is_zst x))
    (= (s_final_allocation s) (x_allocation x))
    (= (s_final_borrow s) (x_borrow x))
    (= (s_final_length s) (x_length x))
    (s_panicked s)
    (LengthFourInsertionSortPanic x b s)))
(define-fun WindowValid
  ((x Input) (start Int) (end Int)) Bool
  (and
    (<= 0 start)
    (< start end)
    (<= end (x_length x))
    (PositionInRange (x_index x) start end)))
(define-fun PartitionedWindow
  ((b Boundary)
   (sequence (Array Int Int))
   (start Int)
   (pivot Int)
   (end Int)) Bool
  (and
    (= start 0)
    (= pivot 1)
    (= end 4)
    (ContractLeq b (select sequence 0) (select sequence 1))
    (ContractLeq b (select sequence 1) (select sequence 2))
    (ContractLeq b (select sequence 1) (select sequence 3))))
(define-fun SortedWindow
  ((b Boundary)
   (sequence (Array Int Int))
   (start Int)
   (end Int)) Bool
  (forall ((lower Int) (upper Int))
    (=>
      (and
        (PositionInRange lower start end)
        (PositionInRange upper start end)
        (< lower upper))
      (ContractLeq
        b (select sequence lower) (select sequence upper)))))
(define-fun MainNarrowingSteps
  ((x Input)
   (b Boundary)
   (s State)
   (starts (Array Int Int))
   (ends (Array Int Int))
   (pivots (Array Int Int))
   (count Int)) Bool
  (and
    (<= 0 count)
    (<= count 16)
    (= (select starts 0) 0)
    (= (select ends 0) (x_length x))
    (forall ((step Int))
      (=>
        (and (<= 0 step) (< step count))
        (let
          ((start (select starts step))
           (end (select ends step))
           (pivot (select pivots step))
           (next_start (select starts (+ step 1)))
           (next_end (select ends (+ step 1))))
          (and
            (WindowValid x start end)
            (> (- end start) 16)
            (PositionInRange pivot start end)
            (not (= pivot (x_index x)))
            (PartitionedWindow
              b (s_final_sequence s) start pivot end)
            (= next_start
               (ite (< pivot (x_index x)) (+ pivot 1) start))
            (= next_end
               (ite (< pivot (x_index x)) end pivot))
            (WindowValid x next_start next_end)
            (< (- next_end next_start) (- end start))))))))
(define-fun FallbackReachable
  ((x Input)
   (b Boundary)
   (s State)
   (initial_start Int)
   (initial_end Int)) Bool
  (exists ((start Int) (end Int) (narrowings Int))
    (and
      (<= 0 narrowings)
      (< narrowings (- initial_end initial_start))
      (<= initial_start start)
      (<= start (x_index x))
      (< (x_index x) end)
      (<= end initial_end)
      (=>
        (> narrowings 0)
        (< (- end start) (- initial_end initial_start)))
      (or
        (and
          (<= (- end start) 16)
          (SortedWindow b (s_final_sequence s) start end))
        (and
          (> (- end start) 16)
          (PartitionedWindow
            b
            (s_final_sequence s)
            start
            (x_index x)
            end))))))
(define-fun BoundsTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (<= 0 (x_index x))
    (< (x_index x) (x_length x))
    (= (y_left_len y) (x_index x))
    (= (y_right_len y) (- (x_length x) (x_index x) 1))
    (not (s_panicked s))
    (>= (b_callback_identity b) 0)))
(define-fun ZstTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (=>
    (x_is_zst x)
    (and
      (forall ((position Int))
        (=>
          (PositionInRange position 0 (x_length x))
          (= (select (s_final_sequence s) position)
             (select (x_initial_sequence x) position))))
      (= (s_callback_state s) (NoCallCallbackState x b))
      (= (y_pivot_identity y)
         (select (x_initial_sequence x) (x_index x))))))
(define-fun MinMaxScanTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (=>
      (and
        (not (x_is_zst x))
        (> (x_length x) 1)
        (= (x_index x) 0))
      (ExtremeScanNormal x b s true))
    (=>
      (and
        (not (x_is_zst x))
        (> (x_length x) 1)
        (= (x_index x) (- (x_length x) 1)))
      (ExtremeScanNormal x b s false))
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))))
(define-fun SmallSortTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (x_length x) 4)
    (= (x_index x) 1)
    (not (x_is_zst x))
    (LengthFourInsertionSortNormal x b s)
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))))
(define-fun SwapPermutationTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (PermutationFromInput x s)
    (IdentityInInput x (y_pivot_identity y))
    (>= (b_callback_identity b) 0)))
(define-fun PartitionTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (PartitionedWindow
      b
      (s_final_sequence s)
      0
      (x_index x)
      (x_length x))
    (IdentityInInput x (y_pivot_identity y))
    (>= (s_callback_state s) (b_initial_callback_state b))))
(define-fun RecursiveLoopOrFallbackTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (=>
      (and
        (not (x_is_zst x))
        (< 0 (x_index x))
        (< (x_index x) (- (x_length x) 1)))
      (exists
        ((count Int)
         (starts (Array Int Int))
         (ends (Array Int Int))
         (pivots (Array Int Int)))
        (and
          (MainNarrowingSteps x b s starts ends pivots count)
          (let
            ((start (select starts count))
             (end (select ends count)))
            (and
              (WindowValid x start end)
              (or
                (and
                  (<= (- end start) 16)
                  (SortedWindow b (s_final_sequence s) start end))
                (and
                  (< count 16)
                  (> (- end start) 16)
                  (PartitionedWindow
                    b
                    (s_final_sequence s)
                    start
                    (x_index x)
                    end))
                (and
                  (= count 16)
                  (FallbackReachable x b s start end))))))))))
(define-fun FinalReturnedSubsliceTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_left_ref y) (LeftReference x))
    (= (y_pivot_ref y) (PivotReference x))
    (= (y_right_ref y) (RightReference x))
    (= (y_left_len y) (x_index x))
    (= (y_right_len y) (- (x_length x) (x_index x) 1))
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (= (s_final_allocation s) (x_allocation x))
    (= (s_final_borrow s) (x_borrow x))
    (= (s_final_length s) (x_length x))
    (>= (s_callback_state s) (b_initial_callback_state b))))
(define-fun ActiveFinalConcatConjunct
  ((x Input)
   (b Boundary)
   (y Output)
   (s State)) Bool
  (and
    (= (y_left_ref y) (LeftReference x))
    (= (y_pivot_ref y) (PivotReference x))
    (= (y_right_ref y) (RightReference x))
    (= (s_final_allocation s) (x_allocation x))
    (= (s_final_borrow s) (x_borrow x))
    (= (s_final_length s)
       (+ (ref_span (y_left_ref y))
          (ref_span (y_pivot_ref y))
          (ref_span (y_right_ref y))))
    (>= (b_callback_identity b) 0)))
(define-fun ActiveLeftLengthConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_left_len y) (x_index x))
    (= (ref_span (y_left_ref y)) (y_left_len y))
    (not (s_panicked s))
    (>= (b_initial_callback_state b) 0)))
(define-fun ActivePivotAtIndexConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (ref_start (y_pivot_ref y)) (x_index x))
    (= (ref_span (y_pivot_ref y)) 1)
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (>= (b_callback_identity b) 0)))
(define-fun ActiveRightLengthConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_right_len y) (- (x_length x) (x_index x) 1))
    (= (ref_span (y_right_ref y)) (y_right_len y))
    (not (s_panicked s))
    (>= (b_initial_callback_state b) 0)))
(define-fun ActivePermutationConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (PermutationFromInput x s)
    (IdentityInInput x (y_pivot_identity y))
    (>= (b_callback_identity b) 0)))
(define-fun ActiveCallbackPartitionConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (PartitionedWindow
      b
      (s_final_sequence s)
      0
      (x_index x)
      (x_length x))
    (IdentityInInput x (y_pivot_identity y))
    (>= (s_callback_state s) (b_initial_callback_state b))))
(define-fun Requires_T ((x Input)) Bool
  (and
    (InputShapeValid x)
    (= (x_length x) 4)
    (= (x_index x) 1)
    (not (x_is_zst x))))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (CallbackBoundaryWellFormed x b))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (BoundsTransition x b y s)
    (SmallSortTransition x b y s)
    (NormalReturnTransition x b y s)
    (FinalReturnedSubsliceTransition x b y s)
    (ActiveFinalConcatConjunct x b y s)
    (ActiveLeftLengthConjunct x b y s)
    (ActivePivotAtIndexConjunct x b y s)
    (ActiveRightLengthConjunct x b y s)
    (ActivePermutationConjunct x b y s)
    (ActiveCallbackPartitionConjunct x b y s)))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_equivalence_body(config, purpose)}
(assert
  (not
    (=>
      (and
        (Requires_T x)
        (Boundary_T x b)
        (Spec_T x b y1 s1)
        (Spec_T x b y2 s2))
      (Equivalent_T x b y1 s1 y2 s2))))
(check-sat)
"""
    for symbol in (
        "ProfileCode",
        "SwapPositions",
        "SameProfileAt",
        "ReviewedFinalSequenceEquivalent",
        "SameIdentityMultiplicity",
        "PivotProfilesEqual",
        "SideProfileMultiplicitiesEqual",
        "FastContractLeq",
        "NoCallCallbackState",
        "SequenceSwapMatches",
        "ExtremeScanNormal",
        "WindowValid",
        "SortedWindow",
        "MainNarrowingSteps",
        "FallbackReachable",
        "ZstTransition",
        "MinMaxScanTransition",
        "SwapPermutationTransition",
        "PartitionTransition",
        "RecursiveLoopOrFallbackTransition",
    ):
        text = _drop_smt_definition(text, symbol)
    if config.mode == "key":
        text = _drop_smt_definition(text, "AdapterNormalFast")
    return text


def _principal_observations() -> list[dict[str, str]]:
    result = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort,
        }
        for selector, sort in OUTPUT_FIELDS
    ]
    result.extend(
        {
            "selector": selector,
            "left": "state1",
            "right": "state2",
            "sort": sort,
        }
        for selector, sort in STATE_FIELDS
    )
    return result


def obligation_metadata(config: TargetConfig, purpose: str) -> dict[str, Any]:
    _check_config(config)
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown obligation purpose {purpose}")
    adapter_site = next(
        trust_site
        for trust_site in config.excluded_trust_sites
        if trust_site.endswith("D002")
    )
    unresolved_sites = [
        trust_site
        for trust_site in config.excluded_trust_sites
        if trust_site != adapter_site
    ]
    adapter_semantics = (
        "one CompareStep call followed by an exact Ordering::Less test"
        if config.mode == "compare"
        else (
            "left KeyStep, then right KeyStep, then OrdLtStep with explicit "
            "state threading and no key-stability assumption"
        )
    )
    return {
        "schema_version": 5,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "model_status": "missing-source-backed-model",
        "domain": {
            "bounded": True,
            "slice_length": "exactly four",
            "index": "exactly one",
            "zst": "excluded from this bounded source model",
            "callback": (
                "functional source-step observations over arguments, result, "
                "next state, and panic"
            ),
            "source_model_complete": False,
            "missing_source_phases": list(missing_source_phases(config)),
            "classification_use": (
                "bounded source-faithfulness regression only; target "
                "classification is missing-source-backed-model"
            ),
        },
        "active_contract_conjuncts": list(ACTIVE_CONJUNCTS),
        "boundary_scope": {
            "admitted_trust_site_ids": [config.admitted_trust_site],
            "excluded_retained_trust_site_ids": list(
                config.excluded_trust_sites
            ),
            "context_only_trust_site_ids": list(
                config.context_only_trust_sites
            ),
            "all_audited_trust_site_ids": list(config.all_trust_sites),
            "source_backed_replacement_ids": [],
            "shared_observations": [
                "callback implementation identity",
                "initial callback-visible state",
                "source-step relation selected by callback identity",
            ],
            "excluded_observations": [
                "realized callback invocation trace or invocation count",
                "pivot or selected permutation",
                "returned ranges or selected output",
                "final callback state or final slice",
                "answer encoding or complete target execution trace",
            ],
            "narrower_than_target": True,
        },
        "boundary_fields": [
            {
                "selector": "b_callback_identity",
                "role": "callback_argument",
                "source_citations": [
                    config.target_source,
                    config.selection_source,
                ],
                "trust_site_ids": [config.admitted_trust_site],
                "source_backed_replacement_ids": [],
            },
            {
                "selector": "b_initial_callback_state",
                "role": "callback_state_transition",
                "source_citations": [
                    config.target_source,
                    config.selection_source,
                ],
                "trust_site_ids": [config.admitted_trust_site],
                "source_backed_replacement_ids": [],
            },
            *(
                [
                    {
                        "selector": "b_compare_ordering_relation",
                        "role": "callback_state_transition",
                        "source_citations": [
                            config.target_source,
                            config.selection_source,
                        ],
                        "trust_site_ids": [config.admitted_trust_site],
                        "source_backed_replacement_ids": [],
                    },
                    {
                        "selector": "b_compare_next_state_relation",
                        "role": "callback_state_transition",
                        "source_citations": [
                            config.target_source,
                            config.selection_source,
                        ],
                        "trust_site_ids": [config.admitted_trust_site],
                        "source_backed_replacement_ids": [],
                    },
                    {
                        "selector": "b_compare_panic_relation",
                        "role": "callback_panic",
                        "source_citations": [
                            config.target_source,
                            config.selection_source,
                        ],
                        "trust_site_ids": [config.admitted_trust_site],
                        "source_backed_replacement_ids": [],
                    },
                ]
                if config.mode == "compare"
                else [
                    {
                        "selector": "b_key_result_relation",
                        "role": "callback_result",
                        "source_citations": [
                            config.target_source,
                            config.selection_source,
                        ],
                        "trust_site_ids": [config.admitted_trust_site],
                        "source_backed_replacement_ids": [],
                    },
                    {
                        "selector": "b_key_next_state_relation",
                        "role": "callback_state_transition",
                        "source_citations": [
                            config.target_source,
                            config.selection_source,
                        ],
                        "trust_site_ids": [config.admitted_trust_site],
                        "source_backed_replacement_ids": [],
                    },
                    {
                        "selector": "b_key_panic_relation",
                        "role": "callback_panic",
                        "source_citations": [
                            config.target_source,
                            config.selection_source,
                        ],
                        "trust_site_ids": [config.admitted_trust_site],
                        "source_backed_replacement_ids": [],
                    },
                    {
                        "selector": "b_ord_lt_result_relation",
                        "role": "callback_result",
                        "source_citations": [
                            config.target_source,
                            config.selection_source,
                        ],
                        "trust_site_ids": [config.admitted_trust_site],
                        "source_backed_replacement_ids": [],
                    },
                    {
                        "selector": "b_ord_lt_next_state_relation",
                        "role": "callback_state_transition",
                        "source_citations": [
                            config.target_source,
                            config.selection_source,
                        ],
                        "trust_site_ids": [config.admitted_trust_site],
                        "source_backed_replacement_ids": [],
                    },
                    {
                        "selector": "b_ord_lt_panic_relation",
                        "role": "callback_panic",
                        "source_citations": [
                            config.target_source,
                            config.selection_source,
                        ],
                        "trust_site_ids": [config.admitted_trust_site],
                        "source_backed_replacement_ids": [],
                    },
                ]
            ),
        ],
        "source_backed_replacements": [
            {
                "replacement_id": config.replacement_id,
                "replaces_trust_site_ids": list(
                    [adapter_site]
                ),
                "symbols": ["SmallSortTransition"],
                "source_citations": [
                    config.target_source,
                    config.selection_source,
                    config.small_sort_source,
                ],
                "semantics": (
                    f"{adapter_semantics}; the exact length-four "
                    "insertion_sort_shift_left loop threads all three tail "
                    "iterations, per-comparison state, sequence rotations, "
                    "normal return, panic prefixes, and final subslices."
                ),
            }
        ],
        "unresolved_source_model_trust_site_ids": unresolved_sites,
        "declared_functions": [],
        "source_transition_definitions": list(SOURCE_TRANSITIONS),
        "source_transition_bindings": {
            "bounds": {
                "symbol": "BoundsTransition",
                "source_citations": [
                    config.target_source,
                    config.selection_source,
                ],
            },
            "small_sort": {
                "symbol": "SmallSortTransition",
                "replacement_id": config.replacement_id,
                "trust_site_ids": [config.admitted_trust_site],
                "source_citations": [
                    config.selection_source,
                    config.small_sort_source,
                ],
                "semantics": (
                    "The exact length-four insertion-sort path executes tails "
                    "one, two, and three. InsertTailNormal derives every "
                    "comparison argument and result, per-call callback state, "
                    "and the source rotation of the intermediate sequence."
                ),
            },
            "normal_return": {
                "symbol": "NormalReturnTransition",
                "replacement_id": config.replacement_id,
                "source_citations": [
                    config.target_source,
                    config.selection_source,
                ],
                "semantics": (
                    "Normal-return obligations exclude panicked states. "
                    "PanicPrefixReachable separately uses the same "
                    "InsertTailNormal and AdapterPanic definitions."
                ),
            },
            "returned_subslices": {
                "symbol": "FinalReturnedSubsliceTransition",
                "replacement_id": config.replacement_id,
                "source_citations": [
                    config.target_source,
                    config.selection_source,
                ],
            },
        },
        "target_definition": "TargetDefinition_T",
        "theorem_variables": {
            "input": "x",
            "boundary": "b",
            "output1": "y1",
            "state1": "s1",
            "output2": "y2",
            "state2": "s2",
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "exact returned references, pivot identity, final slice, all "
            "derived profiles, allocation/borrow identity, panic status, and "
            "callback-visible final state"
        ),
        "weak_equivalence_review": {},
        "principal_observations": _principal_observations(),
        "expected_solver_result": "unsat",
        "solver_result_role": (
            "bounded length-four source-faithfulness regression only; it "
            "cannot classify the arbitrary-length target"
        ),
    }


def obligation(
    config: TargetConfig, purpose: str
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: TargetConfig, text: str, metadata: dict[str, Any]
) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.target}: unknown obligation purpose")
    expected_text, expected_metadata = obligation(config, str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            f"{config.target}: metadata differs from source translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.target}: SMT differs from source translation"
        )


def boundary_manifest(config: TargetConfig) -> dict[str, Any]:
    _check_config(config)
    adapter = (
        "one compare(a,b) call followed by exact equality with Ordering::Less"
        if config.mode == "compare"
        else (
            "left-to-right f(a), f(b), then Ord::lt transitions with distinct "
            "intermediate states and no pure/stable-key assumption"
        )
    )
    excluded = []
    for trust_site in config.excluded_trust_sites:
        if trust_site.endswith("D002"):
            reason = (
                "The retained closure-lowering boundary is answer-bearing; "
                "the exact callback adapter is modeled in the bounded "
                "length-four source obligation."
            )
            disposition = "excluded-and-bounded-source-modeled"
        elif trust_site.endswith("D003"):
            reason = (
                "The retained private helper supplies the whole selection "
                "answer. It remains excluded, but exact introselect, pivot, "
                "partition, narrowing, fallback, and panic semantics are not "
                "yet modeled."
            )
            disposition = "excluded-unresolved-source-model"
        else:
            reason = (
                "The external_body supplies the complete selection result and "
                "is excluded rather than relabeled; its arbitrary-length "
                "source replacement remains incomplete."
            )
            disposition = "excluded-unresolved-source-model"
        excluded.append(
            {
                "trust_site_id": trust_site,
                "disposition": disposition,
                "reason": reason,
            }
        )
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "boundary_narrower_than_target": True,
        "admitted_trust_site_ids": [config.admitted_trust_site],
        "context_only_trust_site_ids": list(
            config.context_only_trust_sites
        ),
        "excluded_retained_sites": excluded,
        "shared_boundary_observations": [
            {
                "field": "b_callback_identity",
                "meaning": (
                    "identity selecting the genuine callback source-step "
                    "relation"
                ),
                "trust_site_ids": [config.admitted_trust_site],
            },
            {
                "field": "b_initial_callback_state",
                "meaning": "callback-visible state before the first source call",
                "trust_site_ids": [config.admitted_trust_site],
            },
            *(
                [
                    {
                        "field": "b_compare_ordering_relation",
                        "meaning": (
                            "source-call Ordering result indexed by callback "
                            "state and both arguments, without totality axioms"
                        ),
                        "trust_site_ids": [config.admitted_trust_site],
                    },
                    {
                        "field": "b_compare_next_state_relation",
                        "meaning": (
                            "unique next callback state indexed by current "
                            "state and both arguments"
                        ),
                        "trust_site_ids": [config.admitted_trust_site],
                    },
                    {
                        "field": "b_compare_panic_relation",
                        "meaning": (
                            "panic observation indexed by callback state and "
                            "both arguments"
                        ),
                        "trust_site_ids": [config.admitted_trust_site],
                    },
                ]
                if config.mode == "compare"
                else [
                    {
                        "field": "b_key_result_relation",
                        "meaning": (
                            "unique f(value) result indexed by callback state "
                            "and argument"
                        ),
                        "trust_site_ids": [config.admitted_trust_site],
                    },
                    {
                        "field": "b_key_next_state_relation",
                        "meaning": (
                            "unique state after f(value), indexed by callback "
                            "state and argument"
                        ),
                        "trust_site_ids": [config.admitted_trust_site],
                    },
                    {
                        "field": "b_key_panic_relation",
                        "meaning": (
                            "f(value) panic outcome indexed by callback state "
                            "and argument"
                        ),
                        "trust_site_ids": [config.admitted_trust_site],
                    },
                    {
                        "field": "b_ord_lt_result_relation",
                        "meaning": (
                            "unique Ord::lt result indexed by callback state "
                            "and both key arguments"
                        ),
                        "trust_site_ids": [config.admitted_trust_site],
                    },
                    {
                        "field": "b_ord_lt_next_state_relation",
                        "meaning": (
                            "unique state after Ord::lt, indexed by callback "
                            "state and both key arguments"
                        ),
                        "trust_site_ids": [config.admitted_trust_site],
                    },
                    {
                        "field": "b_ord_lt_panic_relation",
                        "meaning": (
                            "Ord::lt panic outcome indexed by callback state "
                            "and both key arguments"
                        ),
                        "trust_site_ids": [config.admitted_trust_site],
                    },
                ]
            ),
        ],
        "callback_adapter_semantics": adapter,
        "bounded_source_model": {
            "replacement_id": config.replacement_id,
            "models_trust_site_ids": [
                trust_site
                for trust_site in config.excluded_trust_sites
                if trust_site.endswith("D002")
            ],
            "source_citations": [
                config.target_source,
                config.selection_source,
                config.small_sort_source,
            ],
            "transitions": [
                "fixed length-four index-one valid bounds",
                "exact callback/key/Ord adapter state threading",
                "three source-derived insertion-sort tail iterations",
                "per-comparison intermediate sequence rotations",
                "gap-guard-restored callback panic prefixes",
                "final left/pivot/right subslice construction",
            ],
        },
        "missing_source_backed_model": {
            "classification": "missing-source-backed-model",
            "unresolved_trust_site_ids": [
                trust_site
                for trust_site in config.excluded_trust_sites
                if not trust_site.endswith("D002")
            ],
            "missing_transitions": list(missing_source_phases(config)),
            "source_citations": [
                config.selection_source,
                config.partition_source,
            ],
        },
        "reviewed_equivalence": {
            "kind": "exact-principal-return-and-final-state",
            "source_citations": [
                config.public_docs,
                config.selection_source,
            ],
            "preserved": [
                "all returned references and lengths",
                "pivot identity",
                "entire in-range final slice",
                "allocation, mutable-borrow, and callback state",
                "panic status",
            ],
            "relaxed_only": [],
        },
        "excluded_from_boundary": [
            "realized invocation trace or count",
            "pivot or selected permutation",
            "returned ranges",
            "final callback state or final slice",
            "answer encoding",
            "complete target execution trace",
        ],
        "classification_limit": (
            "The bounded source model proves only the canonical length-four "
            "insertion-sort execution. No source-backed operational relation "
            "currently derives arbitrary-length pivot, partition, narrowing, "
            "fallback, mutation, callback-state, and panic behavior, so both "
            "target results are missing-source-backed-model."
        ),
        "all_audited_trust_site_ids": list(config.all_trust_sites),
    }


def _int_array(values: dict[int, int], default: int = 0) -> str:
    expression = f"((as const (Array Int Int)) {default})"
    for index, value in sorted(values.items()):
        expression = f"(store {expression} {index} {value})"
    return expression


def _reference(
    allocation: int, borrow: int, start: int, span: int, kind: int
) -> str:
    return f"(mkReference {allocation} {borrow} {start} {span} {kind})"


def _compare_ordering_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((left Int))
    (lambda ((right Int))
      (ite
        (and (= left 20) (= right 10))
        -1
        (ite (and (= left 10) (= right 20)) 1 0)))))"""


def _compare_panic_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((left Int))
    (lambda ((right Int)) false)))"""


def _compare_next_state_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((left Int))
    (lambda ((right Int)) (+ state 1))))"""


def _key_result_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((value Int)) value))"""


def _key_next_state_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((value Int)) (+ state 1)))"""


def _key_panic_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((value Int)) false))"""


def _ord_result_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((left_key Int))
    (lambda ((right_key Int)) (< left_key right_key))))"""


def _ord_next_state_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((left_key Int))
    (lambda ((right_key Int)) (+ state 1))))"""


def _ord_panic_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((left_key Int))
    (lambda ((right_key Int)) false)))"""


def _equal_ordering_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((left Int))
    (lambda ((right Int)) 0)))"""


def _numeric_ordering_array() -> str:
    return """\
(lambda ((state Int))
  (lambda ((left Int))
    (lambda ((right Int))
      (ite (< left right) -1 (ite (> left right) 1 0)))))"""


def _normal_boundary(config: TargetConfig, *, all_equal: bool) -> str:
    if config.mode == "compare":
        ordering = (
            _equal_ordering_array()
            if all_equal
            else _numeric_ordering_array()
        )
        return (
            f"(mkBoundary 61 0 {ordering} "
            f"{_compare_next_state_array()} {_compare_panic_array()})"
        )
    return (
        f"(mkBoundary 61 0 {_key_result_array()} "
        f"{_key_next_state_array()} {_key_panic_array()} "
        f"{_ord_result_array()} {_ord_next_state_array()} "
        f"{_ord_panic_array()})"
    )


def _length_four_terms(
    config: TargetConfig,
    initial_values: tuple[int, int, int, int],
    final_values: tuple[int, int, int, int],
    callback_state: int,
    *,
    all_equal: bool,
) -> dict[str, str]:
    allocation = 41
    borrow = 51
    initial = _int_array(dict(enumerate(initial_values)))
    final = _int_array(dict(enumerate(final_values)))
    left_ref = _reference(allocation, borrow, 0, 1, 1)
    pivot_ref = _reference(allocation, borrow, 1, 1, 2)
    right_ref = _reference(allocation, borrow, 2, 2, 3)
    return {
        "x": f"(mkInput 4 1 {allocation} {borrow} {initial} false)",
        "b": _normal_boundary(config, all_equal=all_equal),
        "y": (
            f"(mkOutput {left_ref} {pivot_ref} {right_ref} "
            f"1 {final_values[1]} 2)"
        ),
        "s": (
            f"(mkState {final} {allocation} {borrow} 4 "
            f"{callback_state} false)"
        ),
        "final": final,
    }


def _probe_text(config: TargetConfig, assertions: tuple[str, ...]) -> str:
    text = obligation_text(config, PRIMARY)
    theorem_start = text.index("(assert\n  (not\n    (=>")
    return (
        text[:theorem_start]
        + "\n".join(assertions)
        + "\n(check-sat)\n"
    )


def nonvacuity_text(config: TargetConfig) -> str:
    terms = _length_four_terms(
        config,
        (40, 30, 20, 10),
        (10, 20, 30, 40),
        6 if config.mode == "compare" else 18,
        all_equal=False,
    )
    return _probe_text(
        config,
        (
            f"(assert (= x {terms['x']}))",
            f"(assert (= b {terms['b']}))",
            "(assert (Requires_T x))",
            "(assert (Boundary_T x b))",
            "(assert (Spec_T x b y1 s1))",
        ),
    )


def mixed_source_execution_text(config: TargetConfig) -> str:
    terms = _length_four_terms(
        config,
        (10, 30, 20, 40),
        (10, 20, 30, 40),
        4 if config.mode == "compare" else 12,
        all_equal=False,
    )
    return _probe_text(
        config,
        (
            f"(assert (= x {terms['x']}))",
            f"(assert (= b {terms['b']}))",
            f"(assert (= y1 {terms['y']}))",
            f"(assert (= s1 {terms['s']}))",
            "(assert (Requires_T x))",
            "(assert (Boundary_T x b))",
            "(assert (Spec_T x b y1 s1))",
        ),
    )


def length_four_wrong_schedule_text(config: TargetConfig) -> str:
    terms = _length_four_terms(
        config,
        (10, 10, 10, 10),
        (10, 10, 10, 10),
        3 if config.mode == "compare" else 9,
        all_equal=True,
    )
    wrong_states = (1, 2) if config.mode == "compare" else (3, 6)
    return _probe_text(
        config,
        (
            f"(assert (= x {terms['x']}))",
            f"(assert (= b {terms['b']}))",
            "(assert (Requires_T x))",
            "(assert (Boundary_T x b))",
            "(assert (Spec_T x b y1 s1))",
            (
                "(assert (or "
                f"(= (s_callback_state s1) {wrong_states[0]}) "
                f"(= (s_callback_state s1) {wrong_states[1]})))"
            ),
        ),
    )


def length_four_source_execution_text(config: TargetConfig) -> str:
    terms = _length_four_terms(
        config,
        (10, 10, 10, 10),
        (10, 10, 10, 10),
        3 if config.mode == "compare" else 9,
        all_equal=True,
    )
    return _probe_text(
        config,
        (
            f"(assert (= x {terms['x']}))",
            f"(assert (= b {terms['b']}))",
            f"(assert (= y1 {terms['y']}))",
            f"(assert (= s1 {terms['s']}))",
            "(assert (Requires_T x))",
            "(assert (Boundary_T x b))",
            "(assert (Spec_T x b y1 s1))",
        ),
    )


def small_sort_regression_text(config: TargetConfig, case: str) -> str:
    cases = {
        "descending": ((40, 30, 20, 10), 6),
        "mixed": ((10, 30, 20, 40), 4),
        "tail-three-middle": ((10, 20, 40, 30), 4),
        "tail-three-front": ((10, 30, 40, 20), 5),
    }
    if case not in cases:
        raise ValueError(f"{config.target}: unknown small-sort case {case}")
    initial, adapter_count = cases[case]
    expected_state = (
        adapter_count
        if config.mode == "compare"
        else adapter_count * 3
    )
    terms = _length_four_terms(
        config,
        initial,
        (10, 20, 30, 40),
        expected_state,
        all_equal=False,
    )
    return _probe_text(
        config,
        (
            f"(assert (= x {terms['x']}))",
            f"(assert (= b {terms['b']}))",
            "(assert (Requires_T x))",
            "(assert (Boundary_T x b))",
            "(assert (Spec_T x b y1 s1))",
            (
                "(assert (or "
                f"(not (= (s_final_sequence s1) {terms['final']})) "
                f"(not (= (s_callback_state s1) {expected_state}))))"
            ),
        ),
    )


def panic_after_shift_text(
    config: TargetConfig, *, restored: bool
) -> str:
    initial = _int_array({0: 10, 1: 30, 2: 20, 3: 40})
    final = (
        _int_array({0: 10, 1: 20, 2: 30, 3: 40})
        if restored
        else initial
    )
    allocation = 41
    borrow = 51
    if config.mode == "compare":
        panic_relation = """\
(lambda ((state Int))
  (lambda ((left Int))
    (lambda ((right Int))
      (and (= state 2) (= left 20) (= right 10)))))"""
        boundary = (
            f"(mkBoundary 61 0 {_numeric_ordering_array()} "
            f"{_compare_next_state_array()} {panic_relation})"
        )
        callback_state = 3
    else:
        ord_panic_relation = """\
(lambda ((state Int))
  (lambda ((left_key Int))
    (lambda ((right_key Int))
      (and (= state 8) (= left_key 20) (= right_key 10)))))"""
        boundary = (
            f"(mkBoundary 61 0 {_key_result_array()} "
            f"{_key_next_state_array()} {_key_panic_array()} "
            f"{_ord_result_array()} {_ord_next_state_array()} "
            f"{ord_panic_relation})"
        )
        callback_state = 9
    state = (
        f"(mkState {final} {allocation} {borrow} 4 "
        f"{callback_state} true)"
    )
    return _probe_text(
        config,
        (
            f"(assert (= x (mkInput 4 1 {allocation} {borrow} "
            f"{initial} false)))",
            f"(assert (= b {boundary}))",
            f"(assert (= s1 {state}))",
            "(assert (Requires_T x))",
            "(assert (Boundary_T x b))",
            "(assert (PanicPrefixReachable x b s1))",
        ),
    )


def panic_probe_kinds(config: TargetConfig) -> tuple[str, ...]:
    if config.mode == "compare":
        return ("compare",)
    return ("first-key", "second-key", "ord-lt")


def panic_probe_text(config: TargetConfig, kind: str) -> str:
    if kind not in panic_probe_kinds(config):
        raise ValueError(f"{config.target}: unknown panic probe {kind}")
    sequence = _int_array({0: 10, 1: 20, 2: 30, 3: 40})
    allocation = 41
    borrow = 51
    if config.mode == "compare":
        panic_relation = """\
(lambda ((state Int))
  (lambda ((left Int))
    (lambda ((right Int))
      (and (= state 0) (= left 20) (= right 10)))))"""
        boundary = (
            f"(mkBoundary 61 0 {_numeric_ordering_array()} "
            f"{_compare_next_state_array()} {panic_relation})"
        )
        expected_state = 1
    else:
        key_state, key_value = {
            "first-key": (0, 20),
            "second-key": (1, 10),
            "ord-lt": (-1, -1),
        }[kind]
        key_panic_relation = f"""\
(lambda ((state Int))
  (lambda ((value Int))
    (and (= state {key_state}) (= value {key_value}))))"""
        ord_panic_relation = (
            """\
(lambda ((state Int))
  (lambda ((left_key Int))
    (lambda ((right_key Int))
      (and (= state 2) (= left_key 20) (= right_key 10)))))"""
            if kind == "ord-lt"
            else _ord_panic_array()
        )
        boundary = (
            f"(mkBoundary 61 0 {_key_result_array()} "
            f"{_key_next_state_array()} {key_panic_relation} "
            f"{_ord_result_array()} {_ord_next_state_array()} "
            f"{ord_panic_relation})"
        )
        expected_state = {"first-key": 1, "second-key": 2, "ord-lt": 3}[kind]
    state = (
        f"(mkState {sequence} {allocation} {borrow} 4 "
        f"{expected_state} true)"
    )
    return _probe_text(
        config,
        (
            f"(assert (= x (mkInput 4 1 {allocation} {borrow} "
            f"{sequence} false)))",
            f"(assert (= b {boundary}))",
            f"(assert (= s1 {state}))",
            "(assert (Requires_T x))",
            "(assert (Boundary_T x b))",
            "(assert (PanicPrefixReachable x b s1))",
        ),
    )


def witness_payload(config: TargetConfig) -> dict[str, Any]:
    first_state = 1 if config.mode == "compare" else 3
    second_state = 2 if config.mode == "compare" else 4
    callback_relation: dict[str, Any]
    if config.mode == "compare":
        callback_relation = {
            "kind": "functional-compare-step-observation",
            "ordering_by_pair": {
                "20,10": "Less",
                "10,20": "Greater",
                "default": "Equal",
            },
            "next_state_delta": 1,
            "panic": False,
        }
    else:
        callback_relation = {
            "kind": "functional-key-then-ord-step-observation",
            "key_by_identity": {},
            "default_key": "identity",
            "ord_lt": "integer-less-than",
            "key_next_state_delta": 1,
            "ord_next_state_delta": 1,
            "panic": False,
            "evaluation_order": ["f(left)", "f(right)", "Ord::lt"],
        }
    reference = {
        "allocation": 41,
        "parent_borrow": 51,
        "start": 0,
        "span": 0,
        "projection_kind": "left-subslice",
    }
    pivot_reference = {
        "allocation": 41,
        "parent_borrow": 51,
        "start": 0,
        "span": 1,
        "projection_kind": "pivot-element",
    }
    right_reference = {
        "allocation": 41,
        "parent_borrow": 51,
        "start": 1,
        "span": 1,
        "projection_kind": "right-subslice",
    }

    def execution(callback_state: int) -> dict[str, Any]:
        final_sequence = (
            [20, 10] if config.mode == "compare" else [10, 20]
        )
        pivot_identity = final_sequence[0]
        return {
            "output": {
                "left_reference": reference,
                "pivot_reference": pivot_reference,
                "right_reference": right_reference,
                "left_length": 0,
                "pivot_identity": pivot_identity,
                "right_length": 1,
            },
            "final": {
                "sequence": final_sequence,
                "allocation": 41,
                "borrow": 51,
                "length": 2,
                "callback_state": callback_state,
                "panicked": False,
            },
        }

    baseline = execution(first_state)
    callback_drift = execution(second_state)
    foreign = execution(first_state)
    foreign["final"] = dict(foreign["final"])
    foreign["final"]["sequence"] = [20, 99]
    malformed = execution(first_state)
    malformed["output"] = dict(malformed["output"])
    malformed["output"]["right_reference"] = dict(
        malformed["output"]["right_reference"]
    )
    malformed["output"]["right_reference"]["start"] = 0
    bounded_relation = (
        {
            "kind": "functional-compare-step-observation",
            "ordering_by_pair": {
                "30,10": "Greater",
                "20,30": "Less",
                "20,10": "Greater",
                "40,30": "Greater",
                "default": "Equal",
            },
            "next_state_delta": 1,
            "panic": False,
        }
        if config.mode == "compare"
        else callback_relation
    )
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "input": {
            "sequence": [10, 20],
            "index": 0,
            "allocation": 41,
            "borrow": 51,
            "is_zst": False,
        },
        "boundary": {
            "callback_identity": 61,
            "initial_callback_state": 0,
            "source_step_relation": callback_relation,
        },
        "functional_boundary_diagnostic": {
            "execution1": baseline,
            "execution2": callback_drift,
            "expected": {
                "same_input_and_boundary": True,
                "execution1_is_source_reachable": True,
                "execution2_is_source_reachable": False,
                "execution1_satisfies_active_contract": True,
                "execution2_satisfies_active_contract": True,
                "exact_equivalent": False,
                "reviewed_selection_equivalent": False,
                "only_difference": "callback-visible-final-state",
            },
            "classification_use": (
                "bounded callback-functionality witness only: the drifted "
                "execution is unreachable under the shared functional "
                "observation and does not classify the missing general model"
            ),
        },
        "bounded_source_execution_witness": {
            "input": {
                "sequence": [10, 30, 20, 40],
                "index": 1,
                "allocation": 41,
                "borrow": 51,
                "is_zst": False,
            },
            "boundary": {
                "callback_identity": 61,
                "initial_callback_state": 0,
                "source_step_relation": bounded_relation,
            },
            "expected": {
                "sequence": [10, 20, 30, 40],
                "callback_state": 4 if config.mode == "compare" else 12,
            },
        },
        "negative_witnesses": {
            "foreign_identity": {
                "baseline": baseline,
                "candidate": foreign,
                "candidate_satisfies_active_contract": False,
            },
            "malformed_returned_range": {
                "baseline": baseline,
                "candidate": malformed,
                "candidate_satisfies_active_contract": False,
            },
            "callback_final_state_drift": {
                "baseline": baseline,
                "candidate": callback_drift,
                "candidate_satisfies_active_contract": True,
                "reviewed_selection_equivalent": False,
            },
        },
    }
