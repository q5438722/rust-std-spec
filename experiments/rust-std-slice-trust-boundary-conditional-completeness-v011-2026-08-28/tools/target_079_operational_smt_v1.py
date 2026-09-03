#!/usr/bin/env python3
"""Relational SMT obligations for target-079 operational-v1."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

import target_079_exact_smt_v1 as exact_smt
import target_079_operational_v1 as operational


EXACT = "exact-principal-return-determinism"
FULL = "completeness-modulo-exact-principal-return-and-final-state"
PRIMARY = FULL
PURPOSES = (EXACT, FULL)
NONVACUITY = "arbitrary-domain-nonvacuity"
LENGTH_17_CORRESPONDENCE = "length-17-source-correspondence"
EXACT_CLEANUP_REGRESSIONS = (
    "ordinary-copy-on-drop-restoration",
    "abort-copy-on-drop-bypass",
    "ordinary-gap-guard-restoration",
    "abort-gap-guard-bypass",
)

SELECTION_PROBE_KINDS = (
    "zst-dispatch",
    "max-dispatch",
    "min-dispatch",
    "optimize-for-size-dispatch",
    "introselect-dispatch",
    "insertion-copy-on-drop",
    "choose-pivot-recursive",
    "lomuto-simple-kernel",
    "lomuto-cyclic-unroll-two-kernel",
    "lomuto-cyclic-unroll-one-kernel",
    "hoare-cyclic-kernel",
    "ancestor-pivot",
    "left-narrowing",
    "right-narrowing",
    "introselect-limit-sixteen-fallback",
    "median-of-ninthers",
    "returned-reference-layout",
)
SELECTION_MUTATION_PROBES = SELECTION_PROBE_KINDS
SELECTION_PHASE_COVERAGE = {
    operational.selection.SOURCE_PHASES[0]: (
        "max-dispatch",
        "min-dispatch",
        "insertion-copy-on-drop",
    ),
    operational.selection.SOURCE_PHASES[1]: (
        "zst-dispatch",
        "max-dispatch",
        "min-dispatch",
        "optimize-for-size-dispatch",
        "introselect-dispatch",
    ),
    operational.selection.SOURCE_PHASES[2]: (
        "choose-pivot-recursive",
    ),
    operational.selection.SOURCE_PHASES[3]: (
        "lomuto-simple-kernel",
        "lomuto-cyclic-unroll-two-kernel",
        "lomuto-cyclic-unroll-one-kernel",
        "hoare-cyclic-kernel",
    ),
    operational.selection.SOURCE_PHASES[4]: (
        "lomuto-cyclic-unroll-two-kernel",
        "lomuto-cyclic-unroll-one-kernel",
    ),
    operational.selection.SOURCE_PHASES[5]: (
        "lomuto-simple-kernel",
    ),
    operational.selection.SOURCE_PHASES[6]: (
        "hoare-cyclic-kernel",
    ),
    operational.selection.SOURCE_PHASES[7]: (
        "ancestor-pivot",
    ),
    operational.selection.SOURCE_PHASES[8]: (
        "left-narrowing",
        "right-narrowing",
        "introselect-limit-sixteen-fallback",
    ),
    operational.selection.SOURCE_PHASES[9]: (
        "optimize-for-size-dispatch",
        "introselect-limit-sixteen-fallback",
    ),
    operational.selection.SOURCE_PHASES[10]: (
        "median-of-ninthers",
    ),
    operational.selection.SOURCE_PHASES[11]: (
        "insertion-copy-on-drop",
    ),
    operational.selection.SOURCE_PHASES[12]: (
        "returned-reference-layout",
    ),
}
PARTITION_KERNEL_PROBES = {
    "lomuto-simple": "lomuto-simple-kernel",
    "lomuto-cyclic-unroll-two": (
        "lomuto-cyclic-unroll-two-kernel"
    ),
    "lomuto-cyclic-unroll-one": (
        "lomuto-cyclic-unroll-one-kernel"
    ),
    "hoare-cyclic": "hoare-cyclic-kernel",
}
ADAPTER_PROBE_KINDS = (
    "key-left",
    "key-right",
    "ord-lt",
    "drop-right",
    "drop-left",
    "normal",
    "first-key-panic",
    "ord-lt-panic-right-cleanup-left-drop-panic",
    "right-drop-panic-left-cleanup",
)
ADAPTER_MUTATION_PROBES = (
    "key-result",
    "key-next-state",
    "key-panic",
    "ord-lt-result",
    "ord-lt-next-state",
    "ord-lt-panic",
    "drop-next-state",
    "drop-panic",
    "owned-right-slot",
)

SOURCE_TRANSITIONS = (
    "KeyResult",
    "KeyNextState",
    "KeyPanics",
    "OrdLtResult",
    "OrdLtNextState",
    "OrdLtPanics",
    "DropNextState",
    "DropPanics",
    "AdapterKeyLeft",
    "AdapterKeyRight",
    "AdapterOrdLt",
    "AdapterDropRight",
    "AdapterDropLeft",
    "AdapterTransition",
    "BoundaryNextState",
    "BoundaryPanics",
    "BoundaryAborts",
    "TargetAdapterIsLess",
    *exact_smt.SOURCE_TRANSITIONS,
    "FinalReturnedSubsliceTransition",
)


def _prefix() -> str:
    return f"""\
; Target: {operational.TARGET}
; Model: {operational.MODEL_ID}
; Active contract SHA-256: {operational.ACTIVE_CONTRACT_SHA256}
; Executable source semantics: tools/target_079_operational_v1.py
; Exact selection semantics: imported target-078 ExactRunState, with the
; target-079 adapter termination sum threaded through every callback.
(set-logic ALL)
(declare-datatypes ((KeyCall 0))
  (((mkKeyCall
      (key_call_state Int)
      (key_call_value Int)))))
(declare-datatypes ((OwnedKey 0))
  (((mkOwnedKey
      (owned_creation_state Int)
      (owned_slot Int)
      (owned_source_identity Int)
      (owned_key_identity Int)))))
(declare-datatypes ((OrdCall 0))
  (((mkOrdCall
      (ord_call_state Int)
      (ord_call_left OwnedKey)
      (ord_call_right OwnedKey)))))
(declare-datatypes ((DropCall 0))
  (((mkDropCall
      (drop_call_state Int)
      (drop_call_key OwnedKey)))))
(declare-datatypes ((PairKey 0))
  (((mkPairKey
      (pair_left_identity Int)
      (pair_right_identity Int)))))
(declare-datatypes ((Input 0))
  (((mkInput
      (x_length Int)
      (x_index Int)
      (x_allocation Int)
      (x_borrow Int)
      (x_initial_sequence (Array Int Int))
      (x_is_zst Bool)))))
(declare-datatypes ((Configuration 0))
  (((mkConfiguration
      (c_optimize_for_size Bool)
      (c_element_size Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_callback_identity Int)
      (b_key_function_identity Int)
      (b_ord_function_identity Int)
      (b_drop_function_identity Int)
      (b_initial_state Int)
      (b_contract_key (Array Int Int))
      (b_contract_ordering (Array PairKey Int))
      (b_key_result (Array KeyCall Int))
      (b_key_next_state (Array KeyCall Int))
      (b_key_panics (Array KeyCall Bool))
      (b_ord_lt_result (Array OrdCall Bool))
      (b_ord_lt_next_state (Array OrdCall Int))
      (b_ord_lt_panics (Array OrdCall Bool))
      (b_drop_next_state (Array DropCall Int))
      (b_drop_panics (Array DropCall Bool))))))
(declare-datatypes ((AdapterFrame 0))
  (((mkAdapterFrame
      (af_state Int)
      (af_termination Int)
      (af_is_less Bool)
      (af_panic_origin Int)
      (af_left_owned OwnedKey)
      (af_right_owned OwnedKey)
      (af_left_live Bool)
      (af_right_live Bool)))))
(declare-datatypes ((Reference 0))
  (((mkReference
      (ref_allocation Int)
      (ref_parent_borrow Int)
      (ref_start Int)
      (ref_span Int)
      (ref_projection_kind Int)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_left Reference)
      (y_pivot Reference)
      (y_right Reference)
      (y_pivot_identity Int)))))
(declare-datatypes ((FinalState 0))
  (((mkFinalState
      (s_final_sequence (Array Int Int))
      (s_allocation Int)
      (s_borrow Int)
      (s_length Int)
      (s_callback_state Int)
      (s_termination Int)
      (s_panicked Bool)
      (s_aborted Bool)
      (s_terminal Bool)))))
(declare-datatypes ((Machine 0))
  (((mkMachine
      (m_sequence (Array Int Int))
      (m_callback_state Int)
      (m_start Int)
      (m_end Int)
      (m_index Int)
      (m_limit Int)
      (m_phase Int)
      (m_mode Int)
      (m_cursor Int)
      (m_accumulator Int)
      (m_tail Int)
      (m_sift Int)
      (m_gap Int)
      (m_temporary Int)
      (m_panicked Bool)
      (m_terminal Bool)))))

; Boundary_T consists only of total functional observations.
(define-fun ContractKey ((b Boundary) (value Int)) Int
  (select (b_contract_key b) value))
(define-fun ContractKeyOrdering
  ((b Boundary) (left_key Int) (right_key Int)) Int
  (select
    (b_contract_ordering b)
    (mkPairKey left_key right_key)))
(define-fun ContractOrdering
  ((b Boundary) (left Int) (right Int)) Int
  (ContractKeyOrdering
    b (ContractKey b left) (ContractKey b right)))
(define-fun KeyResult
  ((b Boundary) (state Int) (value Int)) Int
  (select (b_key_result b) (mkKeyCall state value)))
(define-fun KeyNextState
  ((b Boundary) (state Int) (value Int)) Int
  (select (b_key_next_state b) (mkKeyCall state value)))
(define-fun KeyPanics
  ((b Boundary) (state Int) (value Int)) Bool
  (select (b_key_panics b) (mkKeyCall state value)))
(define-fun OrdLtResult
  ((b Boundary) (state Int) (left OwnedKey) (right OwnedKey)) Bool
  (select (b_ord_lt_result b) (mkOrdCall state left right)))
(define-fun OrdLtNextState
  ((b Boundary) (state Int) (left OwnedKey) (right OwnedKey)) Int
  (select (b_ord_lt_next_state b) (mkOrdCall state left right)))
(define-fun OrdLtPanics
  ((b Boundary) (state Int) (left OwnedKey) (right OwnedKey)) Bool
  (select (b_ord_lt_panics b) (mkOrdCall state left right)))
(define-fun DropNextState
  ((b Boundary) (state Int) (key OwnedKey)) Int
  (select (b_drop_next_state b) (mkDropCall state key)))
(define-fun DropPanics
  ((b Boundary) (state Int) (key OwnedKey)) Bool
  (select (b_drop_panics b) (mkDropCall state key)))

; termination: 0=normal, 1=panic/unwind, 2=non-unwinding abort.
(define-fun AdapterInitial ((state Int)) AdapterFrame
  (mkAdapterFrame
    state 0 false 0
    (mkOwnedKey 0 0 0 0)
    (mkOwnedKey 0 1 0 0)
    false false))
(define-fun AdapterKeyLeft
  ((frame AdapterFrame) (b Boundary) (left Int)) AdapterFrame
  (ite
    (= (af_termination frame) 0)
    (let ((state (af_state frame)))
      (let ((key (KeyResult b state left))
            (next (KeyNextState b state left))
            (panics (KeyPanics b state left)))
        (mkAdapterFrame
          next
          (ite panics 1 0)
          false
          (ite panics 1 0)
          (mkOwnedKey state 0 left key)
          (af_right_owned frame)
          (not panics)
          false)))
    frame))
(define-fun AdapterKeyRight
  ((frame AdapterFrame) (b Boundary) (right Int)) AdapterFrame
  (ite
    (= (af_termination frame) 0)
    (let ((state (af_state frame)))
      (let ((key (KeyResult b state right))
            (next (KeyNextState b state right))
            (panics (KeyPanics b state right)))
        (mkAdapterFrame
          next
          (ite panics 1 0)
          false
          (ite panics 2 0)
          (af_left_owned frame)
          (mkOwnedKey state 1 right key)
          (af_left_live frame)
          (not panics))))
    frame))
(define-fun AdapterOrdLt
  ((frame AdapterFrame) (b Boundary)) AdapterFrame
  (ite
    (= (af_termination frame) 0)
    (let ((state (af_state frame))
          (left (af_left_owned frame))
          (right (af_right_owned frame)))
      (let ((less (OrdLtResult b state left right))
            (next (OrdLtNextState b state left right))
            (panics (OrdLtPanics b state left right)))
        (mkAdapterFrame
          next
          (ite panics 1 0)
          less
          (ite panics 3 0)
          left right
          (af_left_live frame)
          (af_right_live frame))))
    frame))
(define-fun AdapterDropRight
  ((frame AdapterFrame) (b Boundary)) AdapterFrame
  (ite
    (and
      (af_right_live frame)
      (not (= (af_termination frame) 2)))
    (let ((state (af_state frame))
          (key (af_right_owned frame))
          (old_termination (af_termination frame)))
      (let ((next (DropNextState b state key))
            (panics (DropPanics b state key)))
        (mkAdapterFrame
          next
          (ite
            panics
            (ite (= old_termination 1) 2 1)
            old_termination)
          (af_is_less frame)
          (ite panics 4 (af_panic_origin frame))
          (af_left_owned frame)
          key
          (af_left_live frame)
          false)))
    frame))
(define-fun AdapterDropLeft
  ((frame AdapterFrame) (b Boundary)) AdapterFrame
  (ite
    (and
      (af_left_live frame)
      (not (= (af_termination frame) 2)))
    (let ((state (af_state frame))
          (key (af_left_owned frame))
          (old_termination (af_termination frame)))
      (let ((next (DropNextState b state key))
            (panics (DropPanics b state key)))
        (mkAdapterFrame
          next
          (ite
            panics
            (ite (= old_termination 1) 2 1)
            old_termination)
          (af_is_less frame)
          (ite panics 5 (af_panic_origin frame))
          key
          (af_right_owned frame)
          false
          (af_right_live frame))))
    frame))
(define-fun AdapterTransition
  ((b Boundary) (state Int) (left Int) (right Int)) AdapterFrame
  (AdapterDropLeft
    (AdapterDropRight
      (AdapterOrdLt
        (AdapterKeyRight
          (AdapterKeyLeft (AdapterInitial state) b left)
          b
          right)
        b)
      b)
    b))
(define-fun BoundaryNextState
  ((b Boundary) (state Int) (left Int) (right Int)) Int
  (af_state (AdapterTransition b state left right)))
(define-fun BoundaryPanics
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (not
    (= (af_termination (AdapterTransition b state left right)) 0)))
(define-fun BoundaryAborts
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (= (af_termination (AdapterTransition b state left right)) 2))
(define-fun TargetAdapterIsLess
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (af_is_less (AdapterTransition b state left right)))

(define-fun BoundaryWellFormed ((b Boundary)) Bool
  (and
    (forall ((state Int) (value Int))
      (= (KeyResult b state value) (ContractKey b value)))
    (forall ((state Int) (left OwnedKey) (right OwnedKey))
      (=
        (OrdLtResult b state left right)
        (=
          (ContractKeyOrdering
            b
            (owned_key_identity left)
            (owned_key_identity right))
          -1)))
    (forall ((left Int) (right Int))
      (let ((ordering (ContractKeyOrdering b left right)))
        (or (= ordering -1) (= ordering 0) (= ordering 1))))
    (forall ((value Int))
      (= (ContractKeyOrdering b value value) 0))
    (forall ((left Int) (right Int))
      (=
        (ContractKeyOrdering b left right)
        (- (ContractKeyOrdering b right left))))
    (forall ((left Int) (right Int))
      (or
        (<= (ContractKeyOrdering b left right) 0)
        (<= (ContractKeyOrdering b right left) 0)))
    (forall ((left Int) (middle Int) (right Int))
      (=>
        (and
          (<= (ContractKeyOrdering b left middle) 0)
          (<= (ContractKeyOrdering b middle right) 0))
        (<= (ContractKeyOrdering b left right) 0)))))
(define-fun InputWellFormed ((x Input) (c Configuration)) Bool
  (and
    (< 0 (x_length x))
    (<= 0 (x_index x))
    (< (x_index x) (x_length x))
    (<= 0 (c_element_size c))
    (= (x_is_zst x) (= (c_element_size c) 0))
    (=>
      (x_is_zst x)
      (forall ((position Int))
        (=>
          (and (<= 0 position) (< position (x_length x)))
          (=
            (select (x_initial_sequence x) position)
            (select (x_initial_sequence x) 0)))))))

; Accepted source dispatch and primitive mutation helpers.
(define-fun PartitionAtIndexBranch
  ((x Input) (c Configuration)) Int
  (ite
    (x_is_zst x)
    0
    (ite
      (= (x_index x) (- (x_length x) 1))
      1
      (ite
        (= (x_index x) 0)
        2
        (ite (c_optimize_for_size c) 3 4)))))
(define-fun PartitionKernel ((c Configuration)) Int
  (ite
    (<= (c_element_size c) 96)
    (ite
      (c_optimize_for_size c)
      0
      (ite (<= (c_element_size c) 16) 1 2))
    3))
(define-fun ChoosePivotRecurses ((length Int)) Bool (<= 64 length))
(define-fun IntroselectLimit () Int 16)
(define-fun NintherFraction ((length Int)) Int
  (ite
    (<= length 1024)
    (div length 12)
    (ite
      (<= length (* 128 1024))
      (div length 64)
      (div length 1024))))
(define-fun MedianIndex
  ((less_c_a Bool)
   (less_cprime_b Bool)
   (less_b_aprime Bool)
   (a Int)
   (b Int)
   (c Int)) Int
  (let ((aprime (ite less_c_a c a))
        (cprime (ite less_c_a a c)))
    (ite less_cprime_b cprime
      (ite less_b_aprime aprime b))))
(define-fun SwapArray
  ((sequence (Array Int Int)) (left Int) (right Int)) (Array Int Int)
  (store
    (store sequence left (select sequence right))
    right
    (select sequence left)))

{exact_smt.definitions_text()}

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
(define-fun FinalReturnedSubsliceTransition
  ((x Input) (y Output)) Bool
  (and
    (= (y_left y) (LeftReference x))
    (= (y_pivot y) (PivotReference x))
    (= (y_right y) (RightReference x))))

(define-fun-rec IdentityCountThrough
  ((sequence (Array Int Int)) (count Int) (identity Int)) Int
  (ite
    (<= count 0)
    0
    (let ((position (- count 1)))
      (+ (IdentityCountThrough sequence position identity)
         (ite (= (select sequence position) identity) 1 0)))))
(define-fun ActiveFinalConcatConjunct
  ((x Input) (y Output) (s FinalState)) Bool
  (and
    (= (ref_start (y_left y)) 0)
    (= (ref_span (y_left y)) (x_index x))
    (= (ref_start (y_pivot y)) (x_index x))
    (= (ref_span (y_pivot y)) 1)
    (= (ref_start (y_right y)) (+ (x_index x) 1))
    (= (+ (ref_span (y_left y))
          (ref_span (y_pivot y))
          (ref_span (y_right y)))
       (s_length s))))
(define-fun ActiveLeftLengthConjunct
  ((x Input) (y Output)) Bool
  (= (ref_span (y_left y)) (x_index x)))
(define-fun ActivePivotAtIndexConjunct
  ((x Input) (y Output) (s FinalState)) Bool
  (= (y_pivot_identity y)
     (select (s_final_sequence s) (x_index x))))
(define-fun ActiveRightLengthConjunct
  ((x Input) (y Output)) Bool
  (= (ref_span (y_right y))
     (- (x_length x) (x_index x) 1)))
(define-fun ActivePermutationConjunct
  ((x Input) (s FinalState)) Bool
  (forall ((identity Int))
    (= (IdentityCountThrough
         (x_initial_sequence x) (x_length x) identity)
       (IdentityCountThrough
         (s_final_sequence s) (s_length s) identity))))
(define-fun ActiveKeyPartitionConjunct
  ((x Input) (b Boundary) (y Output) (s FinalState)) Bool
  (and
    (forall ((position Int))
      (=>
        (and (<= 0 position) (< position (x_index x)))
        (<=
          (ContractOrdering
            b
            (select (s_final_sequence s) position)
            (y_pivot_identity y))
          0)))
    (forall ((position Int))
      (=>
        (and (< (x_index x) position) (< position (x_length x)))
        (<=
          (ContractOrdering
            b
            (y_pivot_identity y)
            (select (s_final_sequence s) position))
          0)))))

; Literal active contract: exactly these six generated conjuncts.
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s FinalState)) Bool
  (and
    (ActiveFinalConcatConjunct x y s)
    (ActiveLeftLengthConjunct x y)
    (ActivePivotAtIndexConjunct x y s)
    (ActiveRightLengthConjunct x y)
    (ActivePermutationConjunct x s)
    (ActiveKeyPartitionConjunct x b y s)))
(define-fun TargetDefinition_T
  ((x Input)
   (b Boundary)
   (c Configuration)
   (y Output)
   (s FinalState)) Bool
  (let ((run (ExactRunState x b c)))
    (let ((termination
            (ite (e_aborted run) 2 (ite (e_panicked run) 1 0))))
      (and
        (= (y_left y) (LeftReference x))
        (= (y_pivot y) (PivotReference x))
        (= (y_right y) (RightReference x))
        (= (y_pivot_identity y)
           (select (e_sequence run) (x_index x)))
        (= (s_final_sequence s) (e_sequence run))
        (= (s_allocation s) (x_allocation x))
        (= (s_borrow s) (x_borrow x))
        (= (s_length s) (x_length x))
        (= (s_callback_state s) (e_callback_state run))
        (= (s_termination s) termination)
        (= (s_panicked s) (e_panicked run))
        (= (s_aborted s) (e_aborted run))
        (s_terminal s)
        (FinalReturnedSubsliceTransition x y)
        (=> (= termination 0) (Spec_T x b y s))))))
(define-fun ExactPrincipalReturn
  ((y1 Output) (y2 Output)) Bool
  (and
    (= (y_left y1) (y_left y2))
    (= (y_pivot y1) (y_pivot y2))
    (= (y_right y1) (y_right y2))
    (= (y_pivot_identity y1) (y_pivot_identity y2))))
(define-fun ExactFinalState
  ((s1 FinalState) (s2 FinalState)) Bool
  (and
    (= (s_final_sequence s1) (s_final_sequence s2))
    (= (s_allocation s1) (s_allocation s2))
    (= (s_borrow s1) (s_borrow s2))
    (= (s_length s1) (s_length s2))
    (= (s_callback_state s1) (s_callback_state s2))
    (= (s_termination s1) (s_termination s2))
    (= (s_panicked s1) (s_panicked s2))
    (= (s_aborted s1) (s_aborted s2))
    (= (s_terminal s1) (s_terminal s2))))
(define-fun ExactPrincipalReturnAndFinalState
  ((y1 Output)
   (s1 FinalState)
   (y2 Output)
   (s2 FinalState)) Bool
  (and
    (ExactPrincipalReturn y1 y2)
    (ExactFinalState s1 s2)))
"""


def obligation_text(purpose: str = EXACT) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-079 purpose: {purpose}")
    equivalence = (
        "(ExactPrincipalReturn y1 y2)"
        if purpose == EXACT
        else "(ExactPrincipalReturnAndFinalState y1 s1 y2 s2)"
    )
    return (
        _prefix()
        + f"; Obligation purpose: {purpose}\n"
        + f"""\
(declare-const x Input)
(declare-const b Boundary)
(declare-const c Configuration)
(declare-const y1 Output)
(declare-const s1 FinalState)
(declare-const y2 Output)
(declare-const s2 FinalState)
(assert (InputWellFormed x c))
(assert (BoundaryWellFormed b))
(assert (TargetDefinition_T x b c y1 s1))
(assert (TargetDefinition_T x b c y2 s2))
(assert (not {equivalence}))
(check-sat)
"""
    )


def obligation_metadata(purpose: str = EXACT) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-079 purpose: {purpose}")
    return {
        "schema_version": 2,
        "target": operational.TARGET,
        "input_order": operational.INPUT_ORDER,
        "model_id": operational.MODEL_ID,
        "active_contract_sha256": operational.ACTIVE_CONTRACT_SHA256,
        "active_contract_conjuncts": list(
            operational.ACTIVE_CONJUNCTS
        ),
        "literal_conjunct_count": 6,
        "obligation_purpose": purpose,
        "expected_solver_result": "unsat",
        "domain": {
            "bounded": False,
            "slice_length": "arbitrary positive integer",
            "index": "arbitrary integer in [0, length)",
            "configuration": (
                "both optimize_for_size arms and every size_of::<T> "
                "partition specialization"
            ),
            "executions": (
                "two independent principal returns and full states under "
                "one total key/Ord/Drop boundary"
            ),
            "termination": "normal | panic | abort",
        },
        "equivalence_kind": (
            "exact-principal-return"
            if purpose == EXACT
            else "exact-principal-return-and-final-state"
        ),
        "boundary_fields": [
            "b_callback_identity",
            "b_key_function_identity",
            "b_ord_function_identity",
            "b_drop_function_identity",
            "b_initial_state",
            "b_contract_key",
            "b_contract_ordering",
            "b_key_result",
            "b_key_next_state",
            "b_key_panics",
            "b_ord_lt_result",
            "b_ord_lt_next_state",
            "b_ord_lt_panics",
            "b_drop_next_state",
            "b_drop_panics",
        ],
        "owned_key_identity": [
            "creation_state",
            "operand_slot",
            "source_identity",
            "abstract_key_identity",
        ],
        "boundary_admitted_trust_site_ids": ["TS-079-D004"],
        "source_backed_replacements": {
            "TS-079-D002": "AdapterTransition",
            "TS-079-D003": (
                "imported target-078 ExactRunState plus abort composition"
            ),
            "TS-079-E001": (
                "imported target-078 ExactRunState plus abort composition"
            ),
        },
        "source_transition_definitions": list(SOURCE_TRANSITIONS),
        "selection_semantic_force_probes": list(SELECTION_PROBE_KINDS),
        "adapter_semantic_force_probes": list(ADAPTER_PROBE_KINDS),
        "selection_semantic_mutation_probes": list(
            SELECTION_MUTATION_PROBES
        ),
        "selection_source_phase_coverage": {
            phase: list(probes)
            for phase, probes in SELECTION_PHASE_COVERAGE.items()
        },
        "partition_kernel_probes": dict(PARTITION_KERNEL_PROBES),
        "adapter_semantic_mutation_probes": list(
            ADAPTER_MUTATION_PROBES
        ),
        "executable_source_model": (
            "tools/target_079_operational_v1.py"
        ),
        "selection_model_reuse": (
            "tools/target_078_exact_smt_v1.py::ExactRunState"
        ),
        "accepted_exact_definitions_sha256": (
            exact_smt.ACCEPTED_DEFINITIONS_SHA256
        ),
        "source_binding_manifest": (
            "evidence/target_079_operational_v1/source_bindings.json"
        ),
        "classification_eligible": True,
    }


def _normal_boundary(name: str = "normal_b") -> str:
    return f"""\
(define-fun {name} () Boundary
  (mkBoundary
    79 7901 7902 7903 0
    (lambda ((value Int)) value)
    (lambda ((pair PairKey))
      (ite
        (< (pair_left_identity pair) (pair_right_identity pair))
        -1
        (ite
          (> (pair_left_identity pair) (pair_right_identity pair))
          1
          0)))
    (lambda ((call KeyCall)) (key_call_value call))
    (lambda ((call KeyCall)) (+ (key_call_state call) 1))
    ((as const (Array KeyCall Bool)) false)
    (lambda ((call OrdCall))
      (<
        (owned_key_identity (ord_call_left call))
        (owned_key_identity (ord_call_right call))))
    (lambda ((call OrdCall)) (+ (ord_call_state call) 1))
    ((as const (Array OrdCall Bool)) false)
    (lambda ((call DropCall)) (+ (drop_call_state call) 1))
    ((as const (Array DropCall Bool)) false)))
"""


def _ord_panic_left_drop_panic_boundary(
    name: str = "abort_b",
) -> str:
    return (
        _normal_boundary("base_abort_b")
        + f"""\
(define-fun {name} () Boundary
  (let ((base base_abort_b)
        (left (mkOwnedKey 0 0 10 10))
        (right (mkOwnedKey 1 1 20 20)))
    (mkBoundary
      (b_callback_identity base)
      (b_key_function_identity base)
      (b_ord_function_identity base)
      (b_drop_function_identity base)
      (b_initial_state base)
      (b_contract_key base)
      (b_contract_ordering base)
      (b_key_result base)
      (b_key_next_state base)
      (b_key_panics base)
      (b_ord_lt_result base)
      (b_ord_lt_next_state base)
      (store
        (b_ord_lt_panics base)
        (mkOrdCall 2 left right)
        true)
      (b_drop_next_state base)
      (store
        (b_drop_panics base)
        (mkDropCall 4 left)
        true))))
"""
    )


def _ord_panic_boundary(
    left: int,
    right: int,
    name: str = "panic_b",
) -> str:
    return (
        _normal_boundary("base_panic_b")
        + f"""\
(define-fun {name} () Boundary
  (let ((base base_panic_b)
        (left (mkOwnedKey 0 0 {left} {left}))
        (right (mkOwnedKey 1 1 {right} {right})))
    (mkBoundary
      (b_callback_identity base)
      (b_key_function_identity base)
      (b_ord_function_identity base)
      (b_drop_function_identity base)
      (b_initial_state base)
      (b_contract_key base)
      (b_contract_ordering base)
      (b_key_result base)
      (b_key_next_state base)
      (b_key_panics base)
      (b_ord_lt_result base)
      (b_ord_lt_next_state base)
      (store
        (b_ord_lt_panics base)
        (mkOrdCall 2 left right)
        true)
      (b_drop_next_state base)
      (b_drop_panics base))))
"""
    )


def nonvacuity_text() -> str:
    text = selection_probe_text("returned-reference-layout")
    witness = """\
(define-fun y () Output
  (mkOutput
    (LeftReference x)
    (PivotReference x)
    (RightReference x)
    (select (e_sequence run) (x_index x))))
(define-fun s () FinalState
  (mkFinalState
    (e_sequence run)
    (x_allocation x)
    (x_borrow x)
    (x_length x)
    (e_callback_state run)
    (ite (e_aborted run) 2 (ite (e_panicked run) 1 0))
    (e_panicked run)
    (e_aborted run)
    true))
(assert (not (e_panicked run)))
(assert (not (e_aborted run)))
(assert (TargetDefinition_T x normal_b c y s))
(assert (Spec_T x normal_b y s))
(check-sat-using (then ctx-solver-simplify smt))
"""
    anchor = "(check-sat-using (then ctx-solver-simplify smt))\n"
    if text.count(anchor) != 1:
        raise ValueError("selection probe solver anchor changed")
    return text.replace(anchor, witness, 1)


def _adapter_probe_assertion(kind: str) -> tuple[str, str]:
    normal_frame = """\
(define-fun f0 () AdapterFrame (AdapterInitial 0))
(define-fun f1 () AdapterFrame (AdapterKeyLeft f0 normal_b 10))
(define-fun f2 () AdapterFrame (AdapterKeyRight f1 normal_b 20))
(define-fun f3 () AdapterFrame (AdapterOrdLt f2 normal_b))
(define-fun f4 () AdapterFrame (AdapterDropRight f3 normal_b))
(define-fun f5 () AdapterFrame (AdapterDropLeft f4 normal_b))
"""
    cases = {
        "key-left": (
            _normal_boundary() + normal_frame,
            """\
(assert (= (af_state f1) 1))
(assert (af_left_live f1))
(assert (= (owned_slot (af_left_owned f1)) 0))
(assert (= (owned_key_identity (af_left_owned f1)) 10))""",
        ),
        "key-right": (
            _normal_boundary() + normal_frame,
            """\
(assert (= (af_state f2) 2))
(assert (af_right_live f2))
(assert (= (owned_slot (af_right_owned f2)) 1))
(assert (not (= (af_left_owned f2) (af_right_owned f2))))""",
        ),
        "ord-lt": (
            _normal_boundary() + normal_frame,
            """\
(assert (= (af_state f3) 3))
(assert (af_is_less f3))
(assert (= (af_termination f3) 0))""",
        ),
        "drop-right": (
            _normal_boundary() + normal_frame,
            """\
(assert (= (af_state f4) 4))
(assert (not (af_right_live f4)))
(assert (af_left_live f4))""",
        ),
        "drop-left": (
            _normal_boundary() + normal_frame,
            """\
(assert (= (af_state f5) 5))
(assert (not (af_left_live f5)))
(assert (= (af_termination f5) 0))""",
        ),
        "normal": (
            _normal_boundary(),
            """\
(define-fun frame () AdapterFrame
  (AdapterTransition normal_b 0 10 20))
(assert (= (af_termination frame) 0))
(assert (= (af_state frame) 5))
(assert (af_is_less frame))""",
        ),
        "first-key-panic": (
            _normal_boundary("base_key_panic_b")
            + """\
(define-fun key_panic_b () Boundary
  (let ((base base_key_panic_b))
    (mkBoundary
      (b_callback_identity base)
      (b_key_function_identity base)
      (b_ord_function_identity base)
      (b_drop_function_identity base)
      (b_initial_state base)
      (b_contract_key base)
      (b_contract_ordering base)
      (b_key_result base)
      (b_key_next_state base)
      (store (b_key_panics base) (mkKeyCall 0 10) true)
      (b_ord_lt_result base)
      (b_ord_lt_next_state base)
      (b_ord_lt_panics base)
      (b_drop_next_state base)
      (b_drop_panics base))))
""",
            """\
(define-fun frame () AdapterFrame
  (AdapterTransition key_panic_b 0 10 20))
(assert (= (af_termination frame) 1))
(assert (= (af_state frame) 1))
(assert (not (af_left_live frame)))""",
        ),
        "ord-lt-panic-right-cleanup-left-drop-panic": (
            _ord_panic_left_drop_panic_boundary(),
            """\
(define-fun frame () AdapterFrame
  (AdapterTransition abort_b 0 10 20))
(assert (= (af_termination frame) 2))
(assert (= (af_state frame) 5))
(assert (= (af_panic_origin frame) 5))
(assert (not (af_left_live frame)))
(assert (not (af_right_live frame)))""",
        ),
        "right-drop-panic-left-cleanup": (
            _normal_boundary("base_drop_panic_b")
            + """\
(define-fun drop_panic_b () Boundary
  (let ((base base_drop_panic_b)
        (right (mkOwnedKey 1 1 20 20)))
    (mkBoundary
      (b_callback_identity base)
      (b_key_function_identity base)
      (b_ord_function_identity base)
      (b_drop_function_identity base)
      (b_initial_state base)
      (b_contract_key base)
      (b_contract_ordering base)
      (b_key_result base)
      (b_key_next_state base)
      (b_key_panics base)
      (b_ord_lt_result base)
      (b_ord_lt_next_state base)
      (b_ord_lt_panics base)
      (b_drop_next_state base)
      (store
        (b_drop_panics base)
        (mkDropCall 3 right)
        true))))
""",
            """\
(define-fun frame () AdapterFrame
  (AdapterTransition drop_panic_b 0 10 20))
(assert (= (af_termination frame) 1))
(assert (= (af_state frame) 5))
(assert (= (af_panic_origin frame) 4))
(assert (not (af_left_live frame)))""",
        ),
    }
    if kind in cases:
        return cases[kind]

    copy_sequence = """\
(define-fun sequence () (Array Int Int)
  (store
    (store
      (store ((as const (Array Int Int)) 0) 0 3)
      1 4)
    2 1))
"""
    if kind in {
        "ordinary-panic-restores-copy-on-drop",
        "abort-bypasses-copy-on-drop",
    }:
        if kind.startswith("ordinary"):
            boundary = _ord_panic_boundary(1, 3)
        else:
            boundary = (
                _ord_panic_boundary(1, 3, "base_abort_copy_b")
                + """\
(define-fun abort_copy_b () Boundary
  (let ((base base_abort_copy_b)
        (left (mkOwnedKey 0 0 1 1)))
    (mkBoundary
      (b_callback_identity base)
      (b_key_function_identity base)
      (b_ord_function_identity base)
      (b_drop_function_identity base)
      (b_initial_state base)
      (b_contract_key base)
      (b_contract_ordering base)
      (b_key_result base)
      (b_key_next_state base)
      (b_key_panics base)
      (b_ord_lt_result base)
      (b_ord_lt_next_state base)
      (b_ord_lt_panics base)
      (b_drop_next_state base)
      (store
        (b_drop_panics base)
        (mkDropCall 4 left)
        true))))
"""
            )
        return boundary + copy_sequence, ""

    gap_sequence = """\
(define-fun sequence () (Array Int Int)
  (store
    (store ((as const (Array Int Int)) 0) 0 99)
    1 2))
"""
    if kind in {
        "ordinary-panic-restores-gap-guard",
        "abort-bypasses-gap-guard",
    }:
        if kind.startswith("ordinary"):
            boundary = _ord_panic_boundary(2, 5)
        else:
            boundary = (
                _ord_panic_boundary(2, 5, "base_abort_gap_b")
                + """\
(define-fun abort_gap_b () Boundary
  (let ((base base_abort_gap_b)
        (left (mkOwnedKey 0 0 2 2)))
    (mkBoundary
      (b_callback_identity base)
      (b_key_function_identity base)
      (b_ord_function_identity base)
      (b_drop_function_identity base)
      (b_initial_state base)
      (b_contract_key base)
      (b_contract_ordering base)
      (b_key_result base)
      (b_key_next_state base)
      (b_key_panics base)
      (b_ord_lt_result base)
      (b_ord_lt_next_state base)
      (b_ord_lt_panics base)
      (b_drop_next_state base)
      (store
        (b_drop_panics base)
        (mkDropCall 4 left)
        true))))
"""
            )
        return boundary + gap_sequence, ""
    raise ValueError(f"unknown adapter probe: {kind}")


def adapter_probe_text(kind: str) -> str:
    if kind not in ADAPTER_PROBE_KINDS:
        raise ValueError(f"unknown target-079 adapter probe: {kind}")
    fixtures, assertion = _adapter_probe_assertion(kind)
    boundary_name = next(
        name
        for name in (
            "abort_copy_b",
            "abort_gap_b",
            "drop_panic_b",
            "key_panic_b",
            "abort_b",
            "panic_b",
            "normal_b",
        )
        if f"(define-fun {name} " in fixtures
    )
    return (
        _prefix()
        + fixtures
        + f"(assert (BoundaryWellFormed {boundary_name}))\n"
        + assertion
        + "\n(check-sat)\n"
    )


def selection_probe_text(kind: str) -> str:
    if kind not in SELECTION_PROBE_KINDS:
        raise ValueError(f"unknown target-079 selection probe: {kind}")
    if set(SELECTION_PHASE_COVERAGE) != set(
        operational.selection.SOURCE_PHASES
    ):
        raise ValueError("target-079 selection phase coverage changed")
    if set(PARTITION_KERNEL_PROBES.values()) - set(
        SELECTION_PROBE_KINDS
    ):
        raise ValueError("target-079 partition kernel probe is missing")
    if kind == "introselect-limit-sixteen-fallback":
        return _fallback_probe_text()
    if kind in PARTITION_KERNEL_PROBES.values():
        return _partition_kernel_probe_text(kind)
    if kind == "ancestor-pivot":
        return _ancestor_probe_text()
    if kind in {"left-narrowing", "right-narrowing"}:
        return _narrowing_probe_text(kind)
    return _top_level_selection_probe_text(kind)


def adapter_mutation_probe_text(kind: str) -> str:
    if kind not in ADAPTER_MUTATION_PROBES:
        raise ValueError(f"unknown adapter mutation probe: {kind}")
    probe_for = {
        "key-result": "key-left",
        "key-next-state": "key-left",
        "key-panic": "first-key-panic",
        "ord-lt-result": "ord-lt",
        "ord-lt-next-state": "ord-lt",
        "ord-lt-panic": (
            "ord-lt-panic-right-cleanup-left-drop-panic"
        ),
        "drop-next-state": "drop-right",
        "drop-panic": "right-drop-panic-left-cleanup",
        "owned-right-slot": "key-right",
    }[kind]
    text = adapter_probe_text(probe_for)
    replacements = {
        "key-result": (
            "(select (b_key_result b) (mkKeyCall state value))",
            "(+ (select (b_key_result b) (mkKeyCall state value)) 1)",
        ),
        "key-next-state": (
            "(select (b_key_next_state b) (mkKeyCall state value))",
            "state",
        ),
        "key-panic": (
            "(select (b_key_panics b) (mkKeyCall state value))",
            "false",
        ),
        "ord-lt-result": (
            "(select (b_ord_lt_result b) (mkOrdCall state left right))",
            "(not (select "
            "(b_ord_lt_result b) (mkOrdCall state left right)))",
        ),
        "ord-lt-next-state": (
            "(select (b_ord_lt_next_state b) "
            "(mkOrdCall state left right))",
            "state",
        ),
        "ord-lt-panic": (
            "(select (b_ord_lt_panics b) (mkOrdCall state left right))",
            "false",
        ),
        "drop-next-state": (
            "(select (b_drop_next_state b) (mkDropCall state key))",
            "state",
        ),
        "drop-panic": (
            "(select (b_drop_panics b) (mkDropCall state key))",
            "false",
        ),
        "owned-right-slot": (
            "(mkOwnedKey state 1 right key)",
            "(mkOwnedKey state 0 right key)",
        ),
    }
    old, new = replacements[kind]
    if text.count(old) < 1:
        raise ValueError(f"{kind}: mutation anchor is missing")
    return text.replace(old, new, 1)


def selection_mutation_probe_text(kind: str) -> str:
    if kind not in SELECTION_MUTATION_PROBES:
        raise ValueError(f"unknown target-079 selection mutation: {kind}")
    text = selection_probe_text(kind)
    marker = f"; Target-079 selection mutation probe: {kind}\n"
    if kind == "zst-dispatch":
        return marker + _replace_nth(
            text, "(x_is_zst x)", "false", -1
        )
    if kind == "returned-reference-layout":
        return marker + _replace_nth(
            text,
            "(x_index x) 1 2",
            "(+ (x_index x) 1) 1 2",
            0,
        )
    cleanup_mutations = {
        "insertion-copy-on-drop": (
            "(ite (e_aborted called)",
            "(ite false",
            0,
        ),
        "lomuto-cyclic-unroll-two-kernel": (
            "(ite (e_aborted (ebr_state predicate))",
            "(ite false",
            0,
        ),
        "lomuto-cyclic-unroll-one-kernel": (
            "(ite (e_aborted (ebr_state predicate))",
            "(ite false",
            1,
        ),
        "hoare-cyclic-kernel": (
            "(ite (e_aborted q)",
            "(ite false",
            1,
        ),
    }
    if kind in cleanup_mutations:
        old, new, occurrence = cleanup_mutations[kind]
        return marker + _replace_nth(text, old, new, occurrence)
    return marker + _replace_nth(
        text,
        "(BoundaryAborts b (e_callback_state q) left right)",
        "false",
        0,
    )


@dataclass(frozen=True)
class _SelectionProbeFixture:
    sequence: tuple[int, ...]
    index: int
    optimize_for_size: bool = False
    element_size: int = 8
    is_zst: bool = False
    phase_prefix: str | None = None
    after_event_kind: str | None = None
    dispatch_branch: int | None = None
    partition_kernel: int | None = None


def _selection_probe_fixture(kind: str) -> _SelectionProbeFixture:
    reverse_17 = tuple(range(17, 0, -1))
    fixtures = {
        "zst-dispatch": _SelectionProbeFixture(
            (0, 0, 0, 0),
            2,
            element_size=0,
            is_zst=True,
            dispatch_branch=0,
        ),
        "max-dispatch": _SelectionProbeFixture(
            (6, 5, 4, 3, 2, 1),
            5,
            phase_prefix="max-index",
            dispatch_branch=1,
        ),
        "min-dispatch": _SelectionProbeFixture(
            (6, 5, 4, 3, 2, 1),
            0,
            phase_prefix="min-index",
            dispatch_branch=2,
        ),
        "optimize-for-size-dispatch": _SelectionProbeFixture(
            reverse_17,
            8,
            optimize_for_size=True,
            phase_prefix="ninther",
            dispatch_branch=3,
            partition_kernel=0,
        ),
        "introselect-dispatch": _SelectionProbeFixture(
            reverse_17,
            8,
            phase_prefix="choose-pivot",
            dispatch_branch=4,
            partition_kernel=1,
        ),
        "insertion-copy-on-drop": _SelectionProbeFixture(
            (4, 3, 2, 1),
            1,
            phase_prefix="insert-tail[0:4:2]:sift-compare",
            dispatch_branch=4,
            partition_kernel=1,
        ),
        "choose-pivot-recursive": _SelectionProbeFixture(
            tuple(random.Random(6501).sample(range(65), 65)),
            32,
            phase_prefix="choose-pivot:median3-rec",
            dispatch_branch=4,
            partition_kernel=1,
        ),
        "lomuto-simple-kernel": _SelectionProbeFixture(
            (5, 1, 3, 2, 4, 0),
            2,
            optimize_for_size=True,
            phase_prefix="partition-lomuto-simple",
            partition_kernel=0,
        ),
        "lomuto-cyclic-unroll-two-kernel": _SelectionProbeFixture(
            (5, 1, 3, 2, 4, 0),
            2,
            phase_prefix="partition-lomuto-cyclic",
            after_event_kind="partition-cycle",
            partition_kernel=1,
        ),
        "lomuto-cyclic-unroll-one-kernel": _SelectionProbeFixture(
            (5, 1, 3, 2, 4, 0),
            2,
            element_size=32,
            phase_prefix="partition-lomuto-cyclic:cleanup-compare",
            partition_kernel=2,
        ),
        "hoare-cyclic-kernel": _SelectionProbeFixture(
            (5, 1, 3, 2, 4, 0),
            2,
            element_size=128,
            phase_prefix="partition-hoare",
            after_event_kind="partition-cycle",
            partition_kernel=3,
        ),
        "ancestor-pivot": _SelectionProbeFixture(
            (7,) * 40,
            20,
            phase_prefix="ancestor-pivot",
            dispatch_branch=4,
            partition_kernel=1,
        ),
        "left-narrowing": _SelectionProbeFixture(
            (5, 1, 3, 2, 4, 0),
            2,
            optimize_for_size=True,
            partition_kernel=0,
        ),
        "right-narrowing": _SelectionProbeFixture(
            (5, 1, 3, 2, 4, 0),
            4,
            optimize_for_size=True,
            partition_kernel=0,
        ),
        "median-of-ninthers": _SelectionProbeFixture(
            tuple(random.Random(0).sample(range(17), 17)),
            8,
            optimize_for_size=True,
            phase_prefix="ninther",
            dispatch_branch=3,
            partition_kernel=0,
        ),
        "returned-reference-layout": _SelectionProbeFixture(
            (4, 3, 2, 1),
            1,
            dispatch_branch=4,
            partition_kernel=1,
        ),
    }
    try:
        return fixtures[kind]
    except KeyError as error:
        raise ValueError(f"no top-level fixture for {kind}") from error


def _selection_input(
    fixture: _SelectionProbeFixture,
) -> operational.SelectionInput:
    return operational.SelectionInput(
        initial_sequence=fixture.sequence,
        index=fixture.index,
        allocation=79,
        borrow=179,
        is_zst=fixture.is_zst,
        configuration=operational.SourceConfiguration(
            optimize_for_size=fixture.optimize_for_size,
            element_size=fixture.element_size,
        ),
    )


def _target_callback_state(
    execution: operational.OperationalExecution,
    fixture: _SelectionProbeFixture,
) -> tuple[int, str]:
    return _target_callback_state_from_events(
        execution.selection.derived_events,
        fixture,
    )


def _target_callback_state_from_events(
    events: tuple[operational.selection.DerivedEvent, ...]
    | list[operational.selection.DerivedEvent],
    fixture: _SelectionProbeFixture,
) -> tuple[int, str]:
    armed = fixture.after_event_kind is None
    for event in events:
        if event.kind == fixture.after_event_kind:
            armed = True
            continue
        if event.kind != "callback":
            continue
        if not armed:
            continue
        if (
            fixture.phase_prefix is not None
            and not event.phase.startswith(fixture.phase_prefix)
        ):
            continue
        return int(event.detail("state")), event.phase
    raise ValueError(
        "fixture does not reach requested callback: "
        f"{fixture.phase_prefix!r} after {fixture.after_event_kind!r}"
    )


def _python_abort_boundary(
    target_state: int,
) -> operational.KeyOrdDropBoundary:
    def ord_lt(
        state: int,
        left: operational.OwnedKeyIdentity,
        right: operational.OwnedKeyIdentity,
    ) -> operational.OrdLtObservation:
        return operational.OrdLtObservation(
            left.key_identity < right.key_identity,
            state + 1,
            state == target_state + 2,
        )

    def drop(
        state: int, key: operational.OwnedKeyIdentity
    ) -> operational.DropObservation:
        return operational.DropObservation(
            state + 1,
            state == target_state + 4
            and key.slot == operational.KeySlot.LEFT,
        )

    return operational.KeyOrdDropBoundary(ord_lt=ord_lt, drop=drop)


def _phase_abort_boundary_text(target_state: int) -> str:
    return (
        _normal_boundary("base_phase_abort_b")
        + f"""\
(define-fun phase_abort_b () Boundary
  (let ((base base_phase_abort_b))
    (mkBoundary
      (b_callback_identity base)
      (b_key_function_identity base)
      (b_ord_function_identity base)
      (b_drop_function_identity base)
      (b_initial_state base)
      (b_contract_key base)
      (b_contract_ordering base)
      (b_key_result base)
      (b_key_next_state base)
      (b_key_panics base)
      (b_ord_lt_result base)
      (b_ord_lt_next_state base)
      (lambda ((call OrdCall))
        (= (ord_call_state call) {target_state + 2}))
      (b_drop_next_state base)
      (lambda ((call DropCall))
        (and
          (= (drop_call_state call) {target_state + 4})
          (= (owned_slot (drop_call_key call)) 0))))))
"""
    )


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _run_state_assertions(
    execution: operational.OperationalExecution,
    run: str = "run",
) -> str:
    state = execution.selection.final_state
    assertions = [
        f"(assert (= (e_callback_state {run}) {state.callback_state}))",
        f"(assert (= (e_panicked {run}) "
        f"{_bool(state.panicked)}))",
        f"(assert (= (e_aborted {run}) "
        f"{_bool(execution.termination == operational.AdapterTermination.ABORT)}))",
    ]
    assertions.extend(
        f"(assert (= (select (e_sequence {run}) {index}) {value}))"
        for index, value in enumerate(state.sequence)
    )
    return "\n".join(assertions)


def _fixture_definitions(
    fixture: _SelectionProbeFixture,
    boundary: str,
) -> str:
    return f"""\
(define-fun sequence () (Array Int Int)
  {_integer_array(fixture.sequence)})
(define-fun x () Input
  (mkInput
    {len(fixture.sequence)}
    {fixture.index}
    79
    179
    sequence
    {_bool(fixture.is_zst)}))
(define-fun c () Configuration
  (mkConfiguration
    {_bool(fixture.optimize_for_size)}
    {fixture.element_size}))
(define-fun run () ExactState (ExactRunState x {boundary} c))
"""


def _dispatch_assertions(
    fixture: _SelectionProbeFixture,
) -> str:
    assertions = []
    if fixture.dispatch_branch is not None:
        assertions.append(
            "(assert (= (PartitionAtIndexBranch x c) "
            f"{fixture.dispatch_branch}))"
        )
    if fixture.partition_kernel is not None:
        assertions.append(
            "(assert (= (PartitionKernel c) "
            f"{fixture.partition_kernel}))"
        )
    return "\n".join(assertions)


def _top_level_selection_probe_text(kind: str) -> str:
    fixture = _selection_probe_fixture(kind)
    selection_input = _selection_input(fixture)
    if kind == "zst-dispatch":
        execution = operational.execute(
            selection_input, operational.KeyOrdDropBoundary()
        )
        boundary_text = _normal_boundary()
        boundary = "normal_b"
        phase_comment = "ZST return with no adapter invocation"
    elif kind == "returned-reference-layout":
        execution = operational.execute(
            selection_input, operational.KeyOrdDropBoundary()
        )
        boundary_text = _normal_boundary()
        boundary = "normal_b"
        phase_comment = "normal non-ZST return projection"
    else:
        normal = operational.execute(
            selection_input, operational.KeyOrdDropBoundary()
        )
        target_state, phase = _target_callback_state(normal, fixture)
        execution = operational.execute(
            selection_input, _python_abort_boundary(target_state)
        )
        if execution.termination != operational.AdapterTermination.ABORT:
            raise ValueError(f"{kind}: abort fixture did not abort")
        boundary_text = _phase_abort_boundary_text(target_state)
        boundary = "phase_abort_b"
        phase_comment = (
            f"adapter abort at callback state {target_state}: {phase}"
        )

    suffix = ""
    if kind == "zst-dispatch":
        suffix = """\
(define-fun y () Output
  (mkOutput
    (LeftReference x)
    (PivotReference x)
    (RightReference x)
    (select (e_sequence run) (x_index x))))
(define-fun s () FinalState
  (mkFinalState
    (e_sequence run)
    (x_allocation x)
    (x_borrow x)
    (x_length x)
    (e_callback_state run)
    0
    false
    false
    true))
(assert (TargetDefinition_T x normal_b c y s))
(assert (Spec_T x normal_b y s))
"""
    elif kind == "returned-reference-layout":
        suffix = f"""\
(assert (= (ref_span (LeftReference x)) {fixture.index}))
(assert (= (ref_start (PivotReference x)) {fixture.index}))
(assert (= (ref_start (RightReference x)) {fixture.index + 1}))
(assert (= (ref_span (RightReference x))
  {len(fixture.sequence) - fixture.index - 1}))
"""
    return (
        _prefix()
        + f"; Target-079 selection force probe: {kind}\n"
        + "; Probe scope: whole ExactRunState execution.\n"
        + f"; Forced source phase: {phase_comment}\n"
        + boundary_text
        + _fixture_definitions(fixture, boundary)
        + "(assert (InputWellFormed x c))\n"
        + f"(assert (BoundaryWellFormed {boundary}))\n"
        + _dispatch_assertions(fixture)
        + "\n"
        + _run_state_assertions(execution)
        + "\n"
        + suffix
        + "(check-sat-using (then ctx-solver-simplify smt))\n"
    )


def _partition_kernel_probe_text(kind: str) -> str:
    fixture = _selection_probe_fixture(kind)
    selection_input = _selection_input(fixture)
    normal_engine = operational._AdapterEngine(
        selection_input, operational.KeyOrdDropBoundary()
    )
    operational.selection._partition(
        normal_engine,
        0,
        len(fixture.sequence),
        2,
    )
    target_state, phase = _target_callback_state_from_events(
        normal_engine.events,
        fixture,
    )
    abort_engine = operational._AdapterEngine(
        selection_input,
        _python_abort_boundary(target_state),
    )
    try:
        operational.selection._partition(
            abort_engine,
            0,
            len(fixture.sequence),
            2,
        )
    except operational._AdapterAbortSignal as abort:
        execution = operational._execution(
            abort_engine,
            coverage_status=operational.MODELED_ABORT,
            branch=kind,
            termination=operational.AdapterTermination.ABORT,
            output=None,
            panic_phase=abort.phase,
            panic_origin=abort.result.panic_origin,
        )
    else:
        raise ValueError(f"{kind}: direct partition fixture did not abort")

    return (
        _prefix()
        + f"; Target-079 selection force probe: {kind}\n"
        + "; Probe scope: exact partition-kernel entry through "
        "target-079 adapter termination.\n"
        + f"; Forced partition callback at state {target_state}: {phase}\n"
        + _phase_abort_boundary_text(target_state)
        + f"""\
(define-fun sequence () (Array Int Int)
  {_integer_array(fixture.sequence)})
(define-fun c () Configuration
  (mkConfiguration
    {_bool(fixture.optimize_for_size)}
    {fixture.element_size}))
(define-fun q () ExactState
  (mkExactState sequence 0 false false))
(define-fun partitioned () ExactIndexResult
  (ExactPartition
    q
    phase_abort_b
    c
    0
    {len(fixture.sequence)}
    2
    false))
(define-fun run () ExactState (eir_state partitioned))
(assert (BoundaryWellFormed phase_abort_b))
(assert (= (PartitionKernel c) {fixture.partition_kernel}))
"""
        + _run_state_assertions(execution)
        + "\n(check-sat-using (then ctx-solver-simplify smt))\n"
    )


def _ancestor_probe_text() -> str:
    fixture = _SelectionProbeFixture(
        (7,) * 17,
        8,
        phase_prefix="ancestor-pivot",
        partition_kernel=1,
    )
    selection_input = _selection_input(fixture)
    normal_engine = operational._AdapterEngine(
        selection_input, operational.KeyOrdDropBoundary()
    )
    pivot_position = operational.selection._choose_pivot(
        normal_engine, 0, len(fixture.sequence)
    )
    target_state = normal_engine.callback_state
    abort_engine = operational._AdapterEngine(
        selection_input,
        _python_abort_boundary(target_state),
    )
    pivot_position = operational.selection._choose_pivot(
        abort_engine, 0, len(fixture.sequence)
    )
    pivot_identity = abort_engine.sequence[pivot_position]
    try:
        abort_engine.is_less(
            7,
            pivot_identity,
            "ancestor-pivot:compare",
        )
    except operational._AdapterAbortSignal as abort:
        execution = operational._execution(
            abort_engine,
            coverage_status=operational.MODELED_ABORT,
            branch="ancestor-pivot",
            termination=operational.AdapterTermination.ABORT,
            output=None,
            panic_phase=abort.phase,
            panic_origin=abort.result.panic_origin,
        )
    else:
        raise ValueError("ancestor-pivot direct fixture did not abort")

    return (
        _prefix()
        + "; Target-079 selection force probe: ancestor-pivot\n"
        + "; Probe scope: exact ancestor phase entry through target-079 "
        "adapter termination.\n"
        + "; ExactIntroselect reaches the ancestor comparison after "
        "source-exact pivot selection.\n"
        + _phase_abort_boundary_text(target_state)
        + f"""\
(define-fun sequence () (Array Int Int)
  {_integer_array(fixture.sequence)})
(define-fun c () Configuration (mkConfiguration false 8))
(define-fun q () ExactState
  (mkExactState sequence 0 false false))
(define-fun run () ExactState
  (ExactIntroselect
    q
    phase_abort_b
    c
    0
    {len(fixture.sequence)}
    {fixture.index}
    true
    7
    16))
(assert (BoundaryWellFormed phase_abort_b))
(assert (= (PartitionKernel c) 1))
"""
        + _run_state_assertions(execution)
        + "\n(check-sat-using (then ctx-solver-simplify smt))\n"
    )


def _narrowing_probe_text(kind: str) -> str:
    fixture = _selection_probe_fixture(kind)
    selection_input = _selection_input(fixture)
    normal_engine = operational._AdapterEngine(
        selection_input, operational.KeyOrdDropBoundary()
    )
    middle = operational.selection._partition(
        normal_engine,
        0,
        len(fixture.sequence),
        2,
    )
    if middle != 3:
        raise ValueError("narrowing fixture partition result changed")
    target_state = normal_engine.callback_state
    abort_engine = operational._AdapterEngine(
        selection_input,
        _python_abort_boundary(target_state),
    )
    middle = operational.selection._partition(
        abort_engine,
        0,
        len(fixture.sequence),
        2,
    )
    try:
        if kind == "left-narrowing":
            operational.selection._insertion_sort_shift_left(
                abort_engine, 0, middle, 1
            )
        else:
            start = middle + 1
            operational.selection._insertion_sort_shift_left(
                abort_engine,
                start,
                len(fixture.sequence),
                1,
            )
    except operational._AdapterAbortSignal as abort:
        execution = operational._execution(
            abort_engine,
            coverage_status=operational.MODELED_ABORT,
            branch=kind,
            termination=operational.AdapterTermination.ABORT,
            output=None,
            panic_phase=abort.phase,
            panic_origin=abort.result.panic_origin,
        )
    else:
        raise ValueError(f"{kind}: narrowed insertion fixture did not abort")

    return (
        _prefix()
        + f"; Target-079 selection force probe: {kind}\n"
        + "; Probe scope: exact narrowing entry through target-079 "
        "adapter termination.\n"
        + f"; ExactIntroselectPartition forces {kind} after midpoint "
        f"{middle} and aborts in the narrowed window.\n"
        + _phase_abort_boundary_text(target_state)
        + f"""\
(define-fun sequence () (Array Int Int)
  {_integer_array(fixture.sequence)})
(define-fun c () Configuration (mkConfiguration true 8))
(define-fun q () ExactState
  (mkExactState sequence 0 false false))
(define-fun run () ExactState
  (ExactIntroselectPartition
    q
    phase_abort_b
    c
    0
    {len(fixture.sequence)}
    {fixture.index}
    false
    0
    15
    2))
(assert (BoundaryWellFormed phase_abort_b))
(assert (= (PartitionKernel c) 0))
"""
        + _run_state_assertions(execution)
        + "\n(check-sat-using (then ctx-solver-simplify smt))\n"
    )


def _fallback_probe_text() -> str:
    fixture = _SelectionProbeFixture(
        tuple(range(17, 0, -1)),
        8,
        phase_prefix="ninther",
        partition_kernel=1,
    )
    selection_input = _selection_input(fixture)
    abort_engine = operational._AdapterEngine(
        selection_input,
        _python_abort_boundary(0),
    )
    try:
        operational.selection._median_of_medians(
            abort_engine,
            0,
            len(fixture.sequence),
            fixture.index,
            phase="introselect-fallback",
        )
    except operational._AdapterAbortSignal as abort:
        execution = operational._execution(
            abort_engine,
            coverage_status=operational.MODELED_ABORT,
            branch="introselect-limit-sixteen-fallback",
            termination=operational.AdapterTermination.ABORT,
            output=None,
            panic_phase=abort.phase,
            panic_origin=abort.result.panic_origin,
        )
    else:
        raise ValueError("fallback direct fixture did not abort")
    return (
        _prefix()
        + "; Target-079 selection force probe: "
        "introselect-limit-sixteen-fallback\n"
        + "; Probe scope: exact fallback entry through target-079 adapter "
        "termination.\n"
        + "; ExactIntroselect limit exhaustion enters median-of-medians "
        "with an aborting target-079 adapter.\n"
        + _phase_abort_boundary_text(0)
        + f"""\
(define-fun sequence () (Array Int Int)
  {_integer_array(fixture.sequence)})
(define-fun c () Configuration (mkConfiguration false 8))
(define-fun q () ExactState
  (mkExactState sequence 0 false false))
(define-fun run () ExactState
  (ExactIntroselect q phase_abort_b c 0 17 8 false 0 0))
(assert (BoundaryWellFormed phase_abort_b))
(assert (= IntroselectLimit 16))
"""
        + _run_state_assertions(execution)
        + "\n(check-sat-using (then ctx-solver-simplify smt))\n"
    )


def _replace_nth(
    text: str,
    old: str,
    new: str,
    occurrence: int,
) -> str:
    positions: list[int] = []
    cursor = 0
    while True:
        position = text.find(old, cursor)
        if position < 0:
            break
        positions.append(position)
        cursor = position + len(old)
    try:
        position = positions[occurrence]
    except IndexError as error:
        raise ValueError(
            f"selection mutation anchor {old!r} occurrence "
            f"{occurrence} is missing"
        ) from error
    return text[:position] + new + text[position + len(old) :]


def _integer_array(values: tuple[int, ...]) -> str:
    expression = "((as const (Array Int Int)) 0)"
    for index, value in enumerate(values):
        expression = f"(store {expression} {index} {value})"
    return expression


def length_17_correspondence_text() -> str:
    selection_input = operational.SelectionInput(
        initial_sequence=tuple(range(17, 0, -1)),
        index=8,
        allocation=79,
        borrow=179,
        is_zst=False,
    )
    execution = operational.execute(
        selection_input, operational.KeyOrdDropBoundary()
    )
    if execution.termination != operational.AdapterTermination.NORMAL:
        raise ValueError("length-17 source correspondence did not return")
    state = execution.selection.final_state
    divergent = [
        "(e_panicked run)",
        "(e_aborted run)",
        f"(not (= (e_callback_state run) {state.callback_state}))",
    ]
    divergent.extend(
        f"(not (= (select (e_sequence run) {index}) {value}))"
        for index, value in enumerate(state.sequence)
    )
    return (
        _prefix()
        + _normal_boundary()
        + f"""\
(define-fun sequence () (Array Int Int)
  {_integer_array(selection_input.initial_sequence)})
(define-fun x () Input (mkInput 17 8 79 179 sequence false))
(define-fun c () Configuration (mkConfiguration false 8))
(define-fun run () ExactState (ExactRunState x normal_b c))
(assert (InputWellFormed x c))
(assert (BoundaryWellFormed normal_b))
(assert (or
  {' '.join(divergent)}))
(check-sat)
"""
    )


def exact_cleanup_regression_text(kind: str) -> str:
    if kind not in EXACT_CLEANUP_REGRESSIONS:
        raise ValueError(f"unknown exact cleanup regression: {kind}")
    probe_kind = {
        "ordinary-copy-on-drop-restoration": (
            "ordinary-panic-restores-copy-on-drop"
        ),
        "abort-copy-on-drop-bypass": "abort-bypasses-copy-on-drop",
        "ordinary-gap-guard-restoration": (
            "ordinary-panic-restores-gap-guard"
        ),
        "abort-gap-guard-bypass": "abort-bypasses-gap-guard",
    }[kind]
    fixtures, _ = _adapter_probe_assertion(probe_kind)
    if "copy-on-drop" in probe_kind:
        boundary = (
            "abort_copy_b"
            if probe_kind.startswith("abort")
            else "panic_b"
        )
        expected = 4 if probe_kind.startswith("abort") else 1
        expected_abort = probe_kind.startswith("abort")
        run = f"""\
(define-fun q () ExactState
  (mkExactState sequence 0 false false))
(define-fun run () ExactState
  (ExactInsertTailLoop q {boundary} 0 1 2 1))
"""
        location = 1
    else:
        expected = 99 if probe_kind.startswith("abort") else 7
        expected_abort = probe_kind.startswith("abort")
        run = f"""\
(define-fun q () ExactState
  (mkExactState sequence 5 true {'true' if expected_abort else 'false'}))
(define-fun run () ExactState
  (ExactRestoreGap q true 7 0))
"""
        location = 0
    abort_divergence = (
        "(not (e_aborted run))"
        if expected_abort
        else "(e_aborted run)"
    )
    return (
        _prefix()
        + fixtures
        + run
        + f"""\
(assert
  (or
    {abort_divergence}
    (not (= (select (e_sequence run) {location}) {expected}))))
(check-sat)
"""
    )


def validate_obligation(text: str, metadata: dict[str, Any]) -> None:
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES or metadata != obligation_metadata(purpose):
        raise ValueError("target-079 operational metadata changed")
    if f"; Obligation purpose: {purpose}\n" not in text:
        raise ValueError("target-079 purpose is not bound in SMT")
    expected_equivalence = (
        "(assert (not (ExactPrincipalReturn y1 y2)))"
        if purpose == EXACT
        else (
            "(assert (not (ExactPrincipalReturnAndFinalState "
            "y1 s1 y2 s2)))"
        )
    )
    if expected_equivalence not in text:
        raise ValueError("target-079 obligation projection changed")
    if exact_smt.definitions_text() not in text:
        raise ValueError("abort-aware ExactRunState block changed")
    if "(declare-fun WholeSelection" in text:
        raise ValueError("opaque whole-selection relation is forbidden")
    if text.count("(assert (TargetDefinition_T x b c") != 2:
        raise ValueError("both independent executions must be constrained")
    for symbol in (
        "ActiveFinalConcatConjunct",
        "ActiveLeftLengthConjunct",
        "ActivePivotAtIndexConjunct",
        "ActiveRightLengthConjunct",
        "ActivePermutationConjunct",
        "ActiveKeyPartitionConjunct",
    ):
        if f"({symbol} x" not in text:
            raise ValueError(f"literal contract conjunct missing: {symbol}")
    for selector in (
        "b_key_result",
        "b_key_next_state",
        "b_key_panics",
        "b_ord_lt_result",
        "b_ord_lt_next_state",
        "b_ord_lt_panics",
        "b_drop_next_state",
        "b_drop_panics",
    ):
        if selector not in text:
            raise ValueError(f"total boundary field missing: {selector}")
    for forbidden in (
        "b_realized_calls",
        "b_drop_schedule",
        "b_final_state",
        "b_selected_answer",
        "b_trace",
    ):
        if forbidden in text:
            raise ValueError(f"prohibited boundary field present: {forbidden}")
