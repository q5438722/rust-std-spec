#!/usr/bin/env python3
"""Relational SMT obligations for the target-078 operational interpreter."""

from __future__ import annotations

from typing import Any

import target_078_exact_smt_v1 as exact_smt
import target_078_operational_v1 as operational


EXACT = "exact-output-and-final-state-determinism"
FULL = "completeness-modulo-exact-principal-return-and-final-state"
PRIMARY = FULL
PURPOSES = (EXACT, FULL)
NONVACUITY = "arbitrary-domain-nonvacuity"
LENGTH_17_CORRESPONDENCE = "length-17-source-correspondence"

PROBE_KINDS = (
    "zst-dispatch",
    "max-dispatch",
    "min-dispatch",
    "optimize-for-size-dispatch",
    "introselect-dispatch",
    "lomuto-simple-kernel",
    "lomuto-cyclic-unroll-two-kernel",
    "lomuto-cyclic-unroll-one-kernel",
    "hoare-cyclic-kernel",
    "choose-pivot-recursive",
    "introselect-limit-sixteen",
    "ninther-frac-small",
    "ninther-frac-medium",
    "ninther-frac-large",
    "median-index-c",
    "median-index-a",
    "median-index-b",
    "left-narrowing-shrinks",
    "right-narrowing-shrinks",
    "ancestor-reverse-predicate",
    "returned-reference-layout",
    "callback-step-consumes-boundary",
    "extreme-swap-mutates-sequence",
    "insertion-shift-mutates-sequence",
)

MUTATION_PROBES = {
    "adapter-ordering": (
        "callback-step-consumes-boundary",
        "(= (BoundaryOrdering b state left right) -1)",
        "(= (BoundaryOrdering b state left right) 1)",
    ),
    "partition-kernel": (
        "lomuto-simple-kernel",
        """(ite
      (c_optimize_for_size c)
      0""",
        """(ite
      (c_optimize_for_size c)
      3""",
    ),
    "ninther-fraction": (
        "ninther-frac-small",
        "(div length 12)",
        "(div length 13)",
    ),
    "median-index": (
        "median-index-c",
        "(ite less_cprime_b cprime",
        "(ite less_cprime_b aprime",
    ),
    "swap-mutation": (
        "extreme-swap-mutates-sequence",
        "(store sequence left (select sequence right))",
        "(store sequence left (select sequence left))",
    ),
    "callback-next-state": (
        "callback-step-consumes-boundary",
        "(select (b_next_state b) (mkCallKey state left right))",
        "state",
    ),
    "returned-layout": (
        "returned-reference-layout",
        "(x_index x) 1 2",
        "(+ (x_index x) 1) 1 2",
    ),
}

SOURCE_TRANSITIONS = (
    "TargetAdapterIsLess",
    "PartitionAtIndexBranch",
    "PartitionKernel",
    "ChoosePivotRecurses",
    "IntroselectLimit",
    "NintherFraction",
    "MedianIndex",
    "SwapArray",
    *exact_smt.SOURCE_TRANSITIONS,
    "FinalReturnedSubsliceTransition",
)


def _prefix() -> str:
    return f"""\
; Target: {operational.TARGET}
; Model: {operational.MODEL_ID}
; Active contract SHA-256: {operational.ACTIVE_CONTRACT_SHA256}
; Executable source semantics: tools/target_078_operational_v1.py
; Two independently declared executions are constrained by the same explicit,
; deterministic source-step relation and immutable callback maps.
(set-logic ALL)
(declare-datatypes ((CallKey 0))
  (((mkCallKey
      (call_state Int)
      (call_left_identity Int)
      (call_right_identity Int)))))
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
      (b_initial_state Int)
      (b_contract_ordering (Array PairKey Int))
      (b_ordering (Array CallKey Int))
      (b_next_state (Array CallKey Int))
      (b_panics (Array CallKey Bool))))))
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
      (s_panicked Bool)
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
    (forall ((left Int) (right Int))
      (let ((ordering (ContractOrdering b left right)))
        (or (= ordering -1) (= ordering 0) (= ordering 1))))
    (forall ((value Int))
      (= (ContractOrdering b value value) 0))
    (forall ((left Int) (right Int))
      (= (ContractOrdering b left right)
         (- (ContractOrdering b right left))))
    (forall ((left Int) (right Int))
      (or
        (<= (ContractOrdering b left right) 0)
        (<= (ContractOrdering b right left) 0)))
    (forall ((left Int) (middle Int) (right Int))
      (=>
        (and
          (<= (ContractOrdering b left middle) 0)
          (<= (ContractOrdering b middle right) 0))
        (<= (ContractOrdering b left right) 0)))))
(define-fun InputWellFormed ((x Input) (c Configuration)) Bool
  (and
    (< 0 (x_length x))
    (<= 0 (x_index x))
    (< (x_index x) (x_length x))
    (<= 0 (c_element_size c))
    (= (x_is_zst x) (= (c_element_size c) 0))))

; 0=ZST, 1=max, 2=min, 3=optimize-for-size, 4=introselect.
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
; 0=lomuto-simple, 1=lomuto-cyclic/unroll-2,
; 2=lomuto-cyclic/unroll-1, 3=hoare-cyclic.
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
(define-fun WindowShrinks
  ((old_start Int) (old_end Int) (new_start Int) (new_end Int)) Bool
  (and
    (<= old_start new_start)
    (<= new_start new_end)
    (<= new_end old_end)
    (< (- new_end new_start) (- old_end old_start))))
(define-fun NarrowLeft
  ((m Machine)) Machine
  (mkMachine
    (m_sequence m) (m_callback_state m)
    (m_start m) (m_accumulator m) (m_index m)
    (ite (> (m_limit m) 0) (- (m_limit m) 1) 0)
    0 (m_mode m) 0 0 (+ (m_start m) 1) 0 0 0
    (m_panicked m) false))
(define-fun NarrowRight
  ((m Machine)) Machine
  (let ((new_start (+ (m_accumulator m) 1))
        (target (+ (m_start m) (m_index m))))
    (mkMachine
      (m_sequence m) (m_callback_state m)
      new_start (m_end m) (- target new_start)
      (ite (> (m_limit m) 0) (- (m_limit m) 1) 0)
      8 (m_mode m) 0 0 (+ new_start 1) 0 0
      (select (m_sequence m) (m_accumulator m))
      (m_panicked m) false)))
(define-fun AncestorReversePredicate
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (not (TargetAdapterIsLess b state right left)))

(define-fun InitialMachine
  ((x Input) (b Boundary)) Machine
  (mkMachine
    (x_initial_sequence x) (b_initial_state b)
    0 (x_length x) (x_index x) 16
    0 0 0 0 1 0 0 0 false false))

; Phase 0: source dispatch.
(define-fun DispatchStep
  ((m Machine) (x Input) (c Configuration)) Machine
  (let ((branch (PartitionAtIndexBranch x c)))
    (ite
      (= branch 0)
      (mkMachine
        (m_sequence m) (m_callback_state m)
        (m_start m) (m_end m) (m_index m) (m_limit m)
        11 branch 0 0 0 0 0 0 false true)
      (ite
        (or (= branch 1) (= branch 2))
        (mkMachine
          (m_sequence m) (m_callback_state m)
          (m_start m) (m_end m) (m_index m) (m_limit m)
          1 branch (+ (m_start m) 1) (m_start m)
          0 0 0 0 false false)
        (ite
          (<= (- (m_end m) (m_start m)) 16)
          (mkMachine
            (m_sequence m) (m_callback_state m)
            (m_start m) (m_end m) (m_index m) (m_limit m)
            3 branch 0 0 (+ (m_start m) 1) 0 0 0 false false)
          (ite
            (= branch 3)
            (mkMachine
              (m_sequence m) (m_callback_state m)
              (m_start m) (m_end m) (m_index m) (m_limit m)
              9 branch 0 0 0 0 0 0 false false)
            (mkMachine
              (m_sequence m) (m_callback_state m)
              (m_start m) (m_end m) (m_index m) (m_limit m)
              5 branch 0 0 0 0 0 0 false false)))))))

; Phase 1: exact min/max scan callback and accumulator update.
(define-fun ExtremeScanStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (>= (m_cursor m) (m_end m))
    (mkMachine
      (m_sequence m) (m_callback_state m)
      (m_start m) (m_end m) (m_index m) (m_limit m)
      2 (m_mode m) (m_cursor m) (m_accumulator m)
      0 0 0 0 false false)
    (let ((left
            (ite
              (= (m_mode m) 2)
              (select (m_sequence m) (m_cursor m))
              (select (m_sequence m) (m_accumulator m))))
          (right
            (ite
              (= (m_mode m) 2)
              (select (m_sequence m) (m_accumulator m))
              (select (m_sequence m) (m_cursor m)))))
      (let ((panics
              (BoundaryPanics b (m_callback_state m) left right))
            (less
              (TargetAdapterIsLess
                b (m_callback_state m) left right)))
        (mkMachine
          (m_sequence m)
          (BoundaryNextState b (m_callback_state m) left right)
          (m_start m) (m_end m) (m_index m) (m_limit m)
          (ite panics 11 1) (m_mode m) (+ (m_cursor m) 1)
          (ite less (m_cursor m) (m_accumulator m))
          0 0 0 0 panics panics)))))

; Phase 2: exact extreme final swap.
(define-fun ExtremeSwapStep
  ((m Machine) (x Input)) Machine
  (mkMachine
    (SwapArray (m_sequence m) (m_accumulator m) (x_index x))
    (m_callback_state m)
    (m_start m) (m_end m) (m_index m) (m_limit m)
    11 (m_mode m) (m_cursor m) (m_accumulator m)
    0 0 0 0 false true))

; Phase 3: exact insert_tail initial comparison.
(define-fun InsertionCompareStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (>= (m_tail m) (m_end m))
    (mkMachine
      (m_sequence m) (m_callback_state m)
      (m_start m) (m_end m) (m_index m) (m_limit m)
      11 (m_mode m) 0 0 (m_tail m) 0 0 0 false true)
    (let ((temporary (select (m_sequence m) (m_tail m)))
          (right (select (m_sequence m) (- (m_tail m) 1))))
      (let ((panics
              (BoundaryPanics
                b (m_callback_state m) temporary right))
            (less
              (TargetAdapterIsLess
                b (m_callback_state m) temporary right)))
        (mkMachine
          (m_sequence m)
          (BoundaryNextState
            b (m_callback_state m) temporary right)
          (m_start m) (m_end m) (m_index m) (m_limit m)
          (ite panics 11 (ite less 4 3))
          (m_mode m) 0 0
          (ite less (m_tail m) (+ (m_tail m) 1))
          (ite less (- (m_tail m) 1) 0)
          (ite less (m_tail m) 0)
          (ite less temporary 0)
          panics panics)))))

; Phase 4: exact shift, callback, and CopyOnDrop restoration.
(define-fun InsertionShiftStep
  ((m Machine) (b Boundary)) Machine
  (let ((shifted
          (store
            (m_sequence m)
            (m_gap m)
            (select (m_sequence m) (m_sift m)))))
    (ite
      (= (m_sift m) (m_start m))
      (mkMachine
        (store shifted (m_sift m) (m_temporary m))
        (m_callback_state m)
        (m_start m) (m_end m) (m_index m) (m_limit m)
        3 (m_mode m) 0 0 (+ (m_tail m) 1)
        0 0 0 false false)
      (let ((next_sift (- (m_sift m) 1)))
        (let ((right (select shifted next_sift))
              (left (m_temporary m)))
          (let ((panics
                  (BoundaryPanics
                    b (m_callback_state m) left right))
                (less
                  (TargetAdapterIsLess
                    b (m_callback_state m) left right)))
            (mkMachine
              (ite
                (or panics (not less))
                (store shifted (m_sift m) (m_temporary m))
                shifted)
              (BoundaryNextState
                b (m_callback_state m) left right)
              (m_start m) (m_end m) (m_index m) (m_limit m)
              (ite panics 11 (ite less 4 3))
              (m_mode m) 0 0
              (ite less (m_tail m) (+ (m_tail m) 1))
              (ite less next_sift 0)
              (ite less (m_sift m) 0)
              (ite less (m_temporary m) 0)
              panics panics)))))))

; Phase 5: exact nonrecursive median3 and pivot-to-front mutation. The
; callback state advances only through comparisons reached by source control.
(define-fun ChoosePivotStep
  ((m Machine) (b Boundary) (c Configuration)) Machine
  (let ((length (- (m_end m) (m_start m))))
    (let ((a (m_start m))
          (sample_b (+ (m_start m) (* 4 (div length 8))))
          (sample_c (+ (m_start m) (* 7 (div length 8)))))
      (let ((state0 (m_callback_state m))
            (value_a (select (m_sequence m) a))
            (value_b (select (m_sequence m) sample_b))
            (value_c (select (m_sequence m) sample_c)))
        (let ((panic1
                (BoundaryPanics b state0 value_a value_b))
              (less_a_b
                (TargetAdapterIsLess b state0 value_a value_b))
              (state1
                (BoundaryNextState b state0 value_a value_b)))
          (let ((panic2
                  (BoundaryPanics b state1 value_a value_c))
                (less_a_c
                  (TargetAdapterIsLess b state1 value_a value_c))
                (state2
                  (BoundaryNextState b state1 value_a value_c)))
            (let ((needs_third (= less_a_b less_a_c)))
              (let ((panic3
                      (BoundaryPanics b state2 value_b value_c))
                    (less_b_c
                      (TargetAdapterIsLess b state2 value_b value_c))
                    (state3
                      (BoundaryNextState b state2 value_b value_c)))
                (let ((panics
                        (or
                          panic1
                          (and (not panic1) panic2)
                          (and
                            (not panic1)
                            (not panic2)
                            needs_third
                            panic3)))
                      (chosen
                        (ite
                          needs_third
                          (ite (xor less_b_c less_a_b) sample_c sample_b)
                          a))
                      (final_state
                        (ite
                          panic1 state1
                          (ite
                            panic2 state2
                            (ite needs_third state3 state2)))))
                  (let ((pivoted
                          (SwapArray
                            (m_sequence m) (m_start m) chosen))
                        (kernel (PartitionKernel c)))
                    (let ((lower_start (+ (m_start m) 1)))
                      (mkMachine
                        (ite panics (m_sequence m) pivoted)
                        final_state
                        (m_start m) (m_end m)
                        (m_index m) (m_limit m)
                        (ite panics 11 6)
                        kernel
                        (ite
                          (or (= kernel 1) (= kernel 2))
                          (+ lower_start 1)
                          lower_start)
                        (m_start m)
                        (ite (= kernel 3) (m_end m) 0)
                        (ite
                          (or (= kernel 1) (= kernel 2))
                          (select pivoted lower_start)
                          0)
                        (ite (= kernel 3) -1 lower_start)
                        (select (m_sequence m) chosen)
                        panics panics))))))))))))

(define-fun MachinePartitionKernel ((m Machine)) Int
  (ite (>= (m_mode m) 4) (- (m_mode m) 4) (m_mode m)))
(define-fun PartitionReverseMode ((m Machine)) Bool
  (>= (m_mode m) 4))
(define-fun PartitionPredicate
  ((m Machine) (b Boundary) (value Int)) Bool
  (ite
    (PartitionReverseMode m)
    (not
      (TargetAdapterIsLess
        b (m_callback_state m) (m_temporary m) value))
    (TargetAdapterIsLess
      b (m_callback_state m) value (m_temporary m))))
(define-fun PartitionPanic
  ((m Machine) (b Boundary) (value Int)) Bool
  (ite
    (PartitionReverseMode m)
    (BoundaryPanics
      b (m_callback_state m) (m_temporary m) value)
    (BoundaryPanics
      b (m_callback_state m) value (m_temporary m))))
(define-fun PartitionNextState
  ((m Machine) (b Boundary) (value Int)) Int
  (ite
    (PartitionReverseMode m)
    (BoundaryNextState
      b (m_callback_state m) (m_temporary m) value)
    (BoundaryNextState
      b (m_callback_state m) value (m_temporary m))))
(define-fun FinishPartition
  ((m Machine) (sequence (Array Int Int)) (pivot_position Int)) Machine
  (mkMachine
    (SwapArray sequence (m_start m) pivot_position)
    (m_callback_state m)
    (m_start m) (m_end m) (m_index m) (m_limit m)
    7 (m_mode m) (m_cursor m) pivot_position
    (m_tail m) (m_sift m) (m_gap m) (m_temporary m)
    false false))

; Source lomuto-simple always swaps the current left/right locations, then
; advances left by the predicate result.
(define-fun SimplePartitionStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (>= (m_cursor m) (m_end m))
    (FinishPartition m (m_sequence m) (m_accumulator m))
    (let ((value (select (m_sequence m) (m_cursor m))))
      (let ((panics (PartitionPanic m b value))
            (goes_left (PartitionPredicate m b value))
            (next_state (PartitionNextState m b value)))
        (mkMachine
          (ite
            panics
            (m_sequence m)
            (SwapArray
              (m_sequence m)
              (+ (m_accumulator m) 1)
              (m_cursor m)))
          next_state
          (m_start m) (m_end m) (m_index m) (m_limit m)
          (ite panics 11 6) (m_mode m)
          (+ (m_cursor m) 1)
          (ite
            (and (not panics) goes_left)
            (+ (m_accumulator m) 1)
            (m_accumulator m))
          (m_tail m) (m_sift m) (m_gap m) (m_temporary m)
          panics panics)))))

; Source lomuto-cyclic preserves the first lower element in GapGuardRaw,
; performs a two-copy cycle for each reached right element, and consumes the
; guard in one final cleanup comparison.
(define-fun CyclicPartitionStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (< (m_cursor m) (m_end m))
    (let ((value (select (m_sequence m) (m_cursor m))))
      (let ((panics (PartitionPanic m b value))
            (goes_left (PartitionPredicate m b value))
            (next_state (PartitionNextState m b value))
            (left (+ (m_accumulator m) 1)))
        (let ((cycled
                (store
                  (store
                    (m_sequence m)
                    (m_gap m)
                    (select (m_sequence m) left))
                  left
                  value)))
          (mkMachine
            (ite
              panics
              (store (m_sequence m) (m_gap m) (m_sift m))
              cycled)
            next_state
            (m_start m) (m_end m) (m_index m) (m_limit m)
            (ite panics 11 6) (m_mode m)
            (+ (m_cursor m) 1)
            (ite
              (and (not panics) goes_left)
              (+ (m_accumulator m) 1)
              (m_accumulator m))
            (m_tail m) (m_sift m) (m_cursor m) (m_temporary m)
            panics panics))))
    (let ((value (m_sift m)))
      (let ((panics (PartitionPanic m b value))
            (goes_left (PartitionPredicate m b value))
            (next_state (PartitionNextState m b value))
            (left (+ (m_accumulator m) 1)))
        (let ((cycled
                (store
                  (store
                    (m_sequence m)
                    (m_gap m)
                    (select (m_sequence m) left))
                  left
                  value))
              (next_acc
                (ite goes_left
                  (+ (m_accumulator m) 1)
                  (m_accumulator m))))
          (ite
            panics
            (mkMachine
              (store (m_sequence m) (m_gap m) value)
              next_state
              (m_start m) (m_end m) (m_index m) (m_limit m)
              11 (m_mode m) (m_cursor m) (m_accumulator m)
              (m_tail m) (m_sift m) (m_gap m) (m_temporary m)
              true true)
            (FinishPartition
              (mkMachine
                cycled next_state
                (m_start m) (m_end m) (m_index m) (m_limit m)
                6 (m_mode m) (m_cursor m) next_acc
                (m_tail m) (m_sift m) (m_gap m) (m_temporary m)
                false false)
              cycled
              next_acc)))))))

(define-fun FinishHoarePartition ((m Machine)) Machine
  (let ((restored
          (ite
            (>= (m_gap m) 0)
            (store (m_sequence m) (m_gap m) (m_sift m))
            (m_sequence m)))
        (pivot_position (- (m_cursor m) 1)))
    (FinishPartition m restored pivot_position)))

; Hoare phase 6 scans from the left. Phase 12 scans from the right and phase
; 13 performs the source gap-copy cycle.
(define-fun HoareLeftStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (>= (m_cursor m) (m_tail m))
    (FinishHoarePartition m)
    (let ((value (select (m_sequence m) (m_cursor m))))
      (let ((panics (PartitionPanic m b value))
            (goes_left (PartitionPredicate m b value))
            (next_state (PartitionNextState m b value)))
        (mkMachine
          (ite
            (and panics (>= (m_gap m) 0))
            (store (m_sequence m) (m_gap m) (m_sift m))
            (m_sequence m))
          next_state
          (m_start m) (m_end m) (m_index m) (m_limit m)
          (ite panics 11 (ite goes_left 6 12))
          (m_mode m)
          (ite goes_left (+ (m_cursor m) 1) (m_cursor m))
          (m_accumulator m) (m_tail m) (m_sift m) (m_gap m)
          (m_temporary m) panics panics)))))

(define-fun HoareRightStep
  ((m Machine) (b Boundary)) Machine
  (let ((right (- (m_tail m) 1)))
    (ite
      (>= (m_cursor m) right)
      (FinishHoarePartition
        (mkMachine
          (m_sequence m) (m_callback_state m)
          (m_start m) (m_end m) (m_index m) (m_limit m)
          12 (m_mode m) (m_cursor m) (m_accumulator m)
          right (m_sift m) (m_gap m) (m_temporary m)
          false false))
      (let ((value (select (m_sequence m) right)))
        (let ((panics (PartitionPanic m b value))
              (goes_left (PartitionPredicate m b value))
              (next_state (PartitionNextState m b value)))
          (mkMachine
            (ite
              (and panics (>= (m_gap m) 0))
              (store (m_sequence m) (m_gap m) (m_sift m))
              (m_sequence m))
            next_state
            (m_start m) (m_end m) (m_index m) (m_limit m)
            (ite panics 11 (ite goes_left 13 12))
            (m_mode m) (m_cursor m) (m_accumulator m)
            right (m_sift m) (m_gap m) (m_temporary m)
            panics panics))))))

(define-fun HoareCycleStep ((m Machine)) Machine
  (let ((first_pair (< (m_gap m) 0)))
    (let ((saved
            (ite first_pair
              (select (m_sequence m) (m_cursor m))
              (m_sift m)))
          (filled
            (ite first_pair
              (m_sequence m)
              (store
                (m_sequence m)
                (m_gap m)
                (select (m_sequence m) (m_cursor m))))))
      (mkMachine
        (store
          filled
          (m_cursor m)
          (select (m_sequence m) (m_tail m)))
        (m_callback_state m)
        (m_start m) (m_end m) (m_index m) (m_limit m)
        6 (m_mode m) (+ (m_cursor m) 1) (m_accumulator m)
        (m_tail m) saved (m_tail m) (m_temporary m)
        false false))))

(define-fun PartitionStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (= (MachinePartitionKernel m) 0)
    (SimplePartitionStep m b)
    (ite
      (or
        (= (MachinePartitionKernel m) 1)
        (= (MachinePartitionKernel m) 2))
      (CyclicPartitionStep m b)
      (HoareLeftStep m b))))

; Phase 7: exact left/right window arithmetic around the realized pivot.
(define-fun NarrowStep
  ((m Machine)) Machine
  (let ((target (+ (m_start m) (m_index m))))
    (ite
      (= (m_accumulator m) target)
      (mkMachine
        (m_sequence m) (m_callback_state m)
        (m_start m) (m_end m) (m_index m) (m_limit m)
        11 (m_mode m) 0 (m_accumulator m) 0 0 0 0 false true)
      (ite
        (< (m_accumulator m) target)
        (NarrowRight m)
        (NarrowLeft m)))))

; Phase 8: source ancestor-pivot comparison and reverse-partition selection.
(define-fun AncestorPivotStep
  ((m Machine) (b Boundary) (c Configuration)) Machine
  (let ((ancestor (m_temporary m))
        (pivot (select (m_sequence m) (m_start m))))
    (let ((panics
            (BoundaryPanics
              b (m_callback_state m) ancestor pivot))
          (less
            (TargetAdapterIsLess
              b (m_callback_state m) ancestor pivot)))
      (let ((kernel (PartitionKernel c))
            (lower_start (+ (m_start m) 1)))
        (mkMachine
          (m_sequence m)
          (BoundaryNextState
            b (m_callback_state m) ancestor pivot)
          (m_start m) (m_end m) (m_index m) (m_limit m)
          (ite panics 11 (ite less 5 6))
          (ite less (m_mode m) (+ 4 kernel))
          (ite
            (or (= kernel 1) (= kernel 2))
            (+ lower_start 1)
            lower_start)
          (m_start m)
          (ite (= kernel 3) (m_end m) 0)
          (ite
            (or (= kernel 1) (= kernel 2))
            (select (m_sequence m) lower_start)
            0)
          (ite (= kernel 3) -1 lower_start)
          pivot
          panics panics)))))

; Phase 9: the fixed sixteen-step fallback dispatch.
(define-fun FallbackStep
  ((m Machine)) Machine
  (ite
    (<= (- (m_end m) (m_start m)) 16)
    (mkMachine
      (m_sequence m) (m_callback_state m)
      (m_start m) (m_end m) (m_index m) 0
      3 (m_mode m) 0 0 (+ (m_start m) 1) 0 0 0 false false)
    (mkMachine
      (m_sequence m) (m_callback_state m)
      (m_start m) (m_end m) (m_index m) 0
      10 (m_mode m) 0 0 0 0 0 0 false false)))

; Phase 10: a ninther comparison/mutation before deterministic partition.
(define-fun NintherStep
  ((m Machine) (b Boundary) (c Configuration)) Machine
  (let ((length (- (m_end m) (m_start m))))
    (let ((frac (NintherFraction length))
          (middle (+ (m_start m) (div length 2))))
      (let ((left_pos (- middle (div frac 2)))
            (right_pos (+ middle (div frac 2))))
        (let ((left (select (m_sequence m) left_pos))
              (right (select (m_sequence m) right_pos)))
          (let ((panics
                  (BoundaryPanics
                    b (m_callback_state m) left right))
                (less
                  (TargetAdapterIsLess
                    b (m_callback_state m) left right)))
            (mkMachine
              (ite
                (and (not panics) less)
                (SwapArray (m_sequence m) left_pos right_pos)
                (m_sequence m))
              (BoundaryNextState
                b (m_callback_state m) left right)
              (m_start m) (m_end m) (m_index m) 0
              (ite panics 11 5)
              (PartitionKernel c) 0 0 0 0 0 0
              panics panics)))))))

(define-fun SourceStep
  ((m Machine) (x Input) (b Boundary) (c Configuration)) Machine
  (ite
    (m_terminal m)
    m
    (ite (= (m_phase m) 0) (DispatchStep m x c)
    (ite (= (m_phase m) 1) (ExtremeScanStep m b)
    (ite (= (m_phase m) 2) (ExtremeSwapStep m x)
    (ite (= (m_phase m) 3) (InsertionCompareStep m b)
    (ite (= (m_phase m) 4) (InsertionShiftStep m b)
    (ite (= (m_phase m) 5) (ChoosePivotStep m b c)
    (ite (= (m_phase m) 6) (PartitionStep m b)
    (ite (= (m_phase m) 7) (NarrowStep m)
    (ite (= (m_phase m) 8) (AncestorPivotStep m b c)
    (ite (= (m_phase m) 9) (FallbackStep m)
    (ite (= (m_phase m) 10) (NintherStep m b c)
    (ite (= (m_phase m) 12) (HoareRightStep m b)
    (ite (= (m_phase m) 13) (HoareCycleStep m)
      (mkMachine
        (m_sequence m) (m_callback_state m)
        (m_start m) (m_end m) (m_index m) (m_limit m)
        11 (m_mode m) (m_cursor m) (m_accumulator m)
        (m_tail m) (m_sift m) (m_gap m) (m_temporary m)
        (m_panicked m) true))))))))))))))))

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
(define-fun ActiveCallbackPartitionConjunct
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
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s FinalState)) Bool
  (and
    (ActiveFinalConcatConjunct x y s)
    (ActiveLeftLengthConjunct x y)
    (ActivePivotAtIndexConjunct x y s)
    (ActiveRightLengthConjunct x y)
    (ActivePermutationConjunct x s)
    (ActiveCallbackPartitionConjunct x b y s)))
(define-fun TargetDefinition_T
  ((x Input)
   (b Boundary)
   (c Configuration)
   (y Output)
   (s FinalState)) Bool
  (let ((run (RunMachine x b c)))
    (and
      (= (y_left y) (LeftReference x))
      (= (y_pivot y) (PivotReference x))
      (= (y_right y) (RightReference x))
      (= (y_pivot_identity y)
         (select (m_sequence run) (x_index x)))
      (= (s_final_sequence s) (m_sequence run))
      (= (s_allocation s) (x_allocation x))
      (= (s_borrow s) (x_borrow x))
      (= (s_length s) (x_length x))
      (= (s_callback_state s) (m_callback_state run))
      (= (s_panicked s) (m_panicked run))
      (= (s_terminal s) (m_terminal run))
      (m_terminal run)
      (FinalReturnedSubsliceTransition x y)
      (=> (not (s_panicked s)) (Spec_T x b y s)))))
(define-fun ExactPrincipalReturnAndFinalState
  ((y1 Output)
   (s1 FinalState)
   (y2 Output)
   (s2 FinalState)) Bool
  (and
    (= (y_left y1) (y_left y2))
    (= (y_pivot y1) (y_pivot y2))
    (= (y_right y1) (y_right y2))
    (= (y_pivot_identity y1) (y_pivot_identity y2))
    (= (s_final_sequence s1) (s_final_sequence s2))
    (= (s_allocation s1) (s_allocation s2))
    (= (s_borrow s1) (s_borrow s2))
    (= (s_length s1) (s_length s2))
    (= (s_callback_state s1) (s_callback_state s2))
    (= (s_panicked s1) (s_panicked s2))
    (= (s_terminal s1) (s_terminal s2))))
"""


def obligation_text(purpose: str = EXACT) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-078 purpose: {purpose}")
    return (
        _prefix()
        + f"; Obligation purpose: {purpose}\n"
        + """\
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
(assert (not (ExactPrincipalReturnAndFinalState y1 s1 y2 s2)))
(check-sat)
"""
    )


def obligation_metadata(purpose: str = EXACT) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-078 purpose: {purpose}")
    return {
        "schema_version": 2,
        "target": operational.TARGET,
        "input_order": operational.INPUT_ORDER,
        "model_id": operational.MODEL_ID,
        "active_contract_sha256": operational.ACTIVE_CONTRACT_SHA256,
        "active_contract_conjuncts": list(operational.ACTIVE_CONJUNCTS),
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
                "two independently declared outputs/final states constrained "
                "by TargetDefinition_T"
            ),
        },
        "equivalence_kind": "exact-principal-return-and-final-state",
        "boundary_fields": [
            "b_callback_identity",
            "b_initial_state",
            "b_contract_ordering",
            "b_ordering",
            "b_next_state",
            "b_panics",
        ],
        "boundary_admitted_trust_site_ids": ["TS-078-D004"],
        "source_backed_replacements": {
            "TS-078-D002": "TargetAdapterIsLess",
            "TS-078-D003": (
                "ExactRunState and tools/target_078_operational_v1.py"
            ),
            "TS-078-E001": (
                "ExactRunState and tools/target_078_operational_v1.py"
            ),
        },
        "source_transition_definitions": list(SOURCE_TRANSITIONS),
        "semantic_force_probes": list(PROBE_KINDS),
        "semantic_mutation_probes": list(MUTATION_PROBES),
        "executable_source_model": "tools/target_078_operational_v1.py",
        "source_binding_manifest": (
            "evidence/target_078_operational_v1/source_bindings.json"
        ),
        "classification_eligible": True,
    }


def _integer_boundary(name: str = "b") -> str:
    return f"""\
(define-fun {name} () Boundary
  (mkBoundary
    61
    0
    (lambda ((key PairKey))
      (ite
        (< (pair_left_identity key) (pair_right_identity key))
        -1
        (ite
          (= (pair_left_identity key) (pair_right_identity key))
          0
          1)))
    (lambda ((key CallKey))
      (ite
        (< (call_left_identity key) (call_right_identity key))
        -1
        (ite
          (= (call_left_identity key) (call_right_identity key))
          0
          1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    ((as const (Array CallKey Bool)) false)))
"""


def _integer_array(values: tuple[int, ...]) -> str:
    expression = "((as const (Array Int Int)) 0)"
    for index, value in enumerate(values):
        expression = f"(store {expression} {index} {value})"
    return expression


def _concrete_boundary(
    boundary: operational.ComparatorBoundary, name: str = "b"
) -> str:
    def pair_ordering(mode: str | None, key_sort: str) -> str:
        left = (
            "pair_left_identity key"
            if key_sort == "PairKey"
            else "call_left_identity key"
        )
        right = (
            "pair_right_identity key"
            if key_sort == "PairKey"
            else "call_right_identity key"
        )
        if mode == operational.INTEGER_TOTAL_ORDER:
            return (
                f"(ite (< ({left}) ({right})) -1 "
                f"(ite (= ({left}) ({right})) 0 1))"
            )
        if mode == operational.CONSTANT_LESS:
            return "-1"
        if mode in (None, operational.CONSTANT_EQUAL):
            return "0"
        if mode == operational.CONSTANT_GREATER:
            return "1"
        if mode == operational.STATE_PREFIX_LESS_THEN_GREATER:
            assert boundary.ordering_cutoff is not None
            return (
                f"(ite (< (call_state key) "
                f"{boundary.ordering_cutoff}) -1 1)"
            )
        raise ValueError(f"unsupported concrete ordering mode: {mode}")

    panic_terms = [
        f"(= (call_state key) {state})"
        for state in sorted(boundary.panic_states)
    ]
    panic_terms.extend(
        (
            "(and "
            f"(= (call_state key) {key.state}) "
            f"(= (call_left_identity key) {key.left_identity}) "
            f"(= (call_right_identity key) {key.right_identity}))"
        )
        for key in sorted(boundary.panic_keys)
    )
    panics = (
        "false"
        if not panic_terms
        else panic_terms[0]
        if len(panic_terms) == 1
        else f"(or {' '.join(panic_terms)})"
    )
    next_state = (
        "(+ (call_state key) 1)"
        if boundary.next_state_mode == operational.INCREMENT_STATE
        else "(call_state key)"
    )
    return f"""\
(define-fun {name} () Boundary
  (mkBoundary
    {boundary.callback_identity}
    {boundary.initial_state}
    (lambda ((key PairKey))
      {pair_ordering(boundary.contract_ordering_mode, "PairKey")})
    (lambda ((key CallKey))
      {pair_ordering(boundary.ordering_mode, "CallKey")})
    (lambda ((key CallKey)) {next_state})
    (lambda ((key CallKey)) {panics})))
"""


def concrete_correspondence_text(
    item: operational.SelectionInput,
    boundary: operational.ComparatorBoundary,
) -> str:
    if not operational.requires_t(item):
        raise ValueError("correspondence requires a valid source input")
    source = operational.execute(item, boundary)
    expected_sequence = source.final_state.sequence
    initial_array = _integer_array(item.initial_sequence)
    final_array = _integer_array(expected_sequence)
    normal_fields = ""
    if source.output is not None:
        normal_fields = f"""\
      (= (y_left formal_y)
         (mkReference {item.allocation} {item.borrow} 0 {item.index} 1))
      (= (y_pivot formal_y)
         (mkReference {item.allocation} {item.borrow} {item.index} 1 2))
      (= (y_right formal_y)
         (mkReference
           {item.allocation}
           {item.borrow}
           {item.index + 1}
           {len(item.initial_sequence) - item.index - 1}
           3))
      (= (y_pivot_identity formal_y) {source.output.pivot_identity})
"""
    contract_assertion = (
        "(assert (BoundaryWellFormed b))\n"
        if boundary.contract_ordering_mode is not None
        else ""
    )
    return (
        _prefix()
        + _concrete_boundary(boundary)
        + f"""\
(define-fun concrete_initial_sequence () (Array Int Int)
  {initial_array})
(define-fun concrete_expected_sequence () (Array Int Int)
  {final_array})
(define-fun concrete_x () Input
  (mkInput
    {len(item.initial_sequence)}
    {item.index}
    {item.allocation}
    {item.borrow}
    concrete_initial_sequence
    {'true' if item.is_zst else 'false'}))
(define-fun concrete_c () Configuration
  (mkConfiguration
    {'true' if item.configuration.optimize_for_size else 'false'}
    {item.configuration.element_size}))
(define-fun concrete_run () Machine
  (RunMachine concrete_x b concrete_c))
(define-fun formal_y () Output
  (mkOutput
    (LeftReference concrete_x)
    (PivotReference concrete_x)
    (RightReference concrete_x)
    (select (m_sequence concrete_run) {item.index})))
(assert (InputWellFormed concrete_x concrete_c))
{contract_assertion}(assert
  (not
    (and
      (= (m_sequence concrete_run) concrete_expected_sequence)
      (= (m_callback_state concrete_run)
         {source.final_state.callback_state})
      (= (m_panicked concrete_run)
         {'true' if source.final_state.panicked else 'false'})
      (m_terminal concrete_run)
{normal_fields}    )))
(check-sat)
"""
    )


def length_17_correspondence_text() -> str:
    item = operational.SelectionInput(
        initial_sequence=tuple(range(16, -1, -1)),
        index=8,
        allocation=41,
        borrow=51,
        is_zst=False,
        configuration=operational.SourceConfiguration(
            optimize_for_size=False,
            element_size=8,
        ),
    )
    source = operational.execute(
        item, operational.integer_total_order_boundary()
    )
    expected_sequence = (
        0,
        7,
        6,
        5,
        4,
        3,
        2,
        1,
        8,
        15,
        13,
        12,
        11,
        10,
        9,
        16,
        14,
    )
    if (
        source.output is None
        or source.output.pivot_identity != 8
        or source.final_state.sequence != expected_sequence
        or source.final_state.callback_state != 19
        or source.final_state.panicked
        or not source.final_state.terminal
    ):
        raise ValueError("length-17 source correspondence fixture drifted")
    return concrete_correspondence_text(
        item, operational.integer_total_order_boundary()
    )


def nonvacuity_text() -> str:
    return (
        _prefix()
        + _integer_boundary()
        + """\
(define-fun zst_sequence () (Array Int Int)
  (store ((as const (Array Int Int)) 0) 0 0))
(define-fun zst_x () Input (mkInput 1 0 41 51 zst_sequence true))
(define-fun zst_c () Configuration (mkConfiguration false 0))
(define-fun zst_run () Machine
  (DispatchStep (InitialMachine zst_x b) zst_x zst_c))
(define-fun zst_y () Output
  (mkOutput
    (LeftReference zst_x)
    (PivotReference zst_x)
    (RightReference zst_x)
    0))
(define-fun zst_s () FinalState
  (mkFinalState
    (m_sequence zst_run) 41 51 1
    (m_callback_state zst_run) false (m_terminal zst_run)))
(assert (InputWellFormed zst_x zst_c))
(assert (m_terminal zst_run))
(assert (not (s_panicked zst_s)))
(assert (Spec_T zst_x b zst_y zst_s))

(define-fun small_sequence () (Array Int Int)
  (store
    (store
      (store ((as const (Array Int Int)) 0) 0 0)
      1 1)
    2 2))
(define-fun small_x () Input
  (mkInput 3 1 41 51 small_sequence false))
(define-fun small_c () Configuration (mkConfiguration false 8))
(define-fun small_m0 () Machine (InitialMachine small_x b))
(define-fun small_m1 () Machine
  (SourceStep small_m0 small_x b small_c))
(define-fun small_m2 () Machine
  (SourceStep small_m1 small_x b small_c))
(define-fun small_m3 () Machine
  (SourceStep small_m2 small_x b small_c))
(define-fun small_m4 () Machine
  (SourceStep small_m3 small_x b small_c))
(define-fun small_y () Output
  (mkOutput
    (LeftReference small_x)
    (PivotReference small_x)
    (RightReference small_x)
    (select (m_sequence small_m4) 1)))
(define-fun small_s () FinalState
  (mkFinalState
    (m_sequence small_m4) 41 51 3
    (m_callback_state small_m4) (m_panicked small_m4)
    (m_terminal small_m4)))
(assert (InputWellFormed small_x small_c))
(assert (m_terminal small_m4))
(assert (not (s_panicked small_s)))
(assert (Spec_T small_x b small_y small_s))
(check-sat)
"""
    )


def immutable_replay_text() -> str:
    return obligation_text(EXACT)


def swap_regression_text() -> str:
    return mutation_probe_text("swap-mutation")


def _probe_assertion(kind: str) -> str:
    assertions = {
        "zst-dispatch": (
            "(assert (= (PartitionAtIndexBranch "
            "(mkInput 9 4 1 2 ((as const (Array Int Int)) 0) true) "
            "(mkConfiguration false 0)) 0))"
        ),
        "max-dispatch": (
            "(assert (= (PartitionAtIndexBranch "
            "(mkInput 9 8 1 2 ((as const (Array Int Int)) 0) false) "
            "(mkConfiguration false 8)) 1))"
        ),
        "min-dispatch": (
            "(assert (= (PartitionAtIndexBranch "
            "(mkInput 9 0 1 2 ((as const (Array Int Int)) 0) false) "
            "(mkConfiguration false 8)) 2))"
        ),
        "optimize-for-size-dispatch": (
            "(assert (= (PartitionAtIndexBranch "
            "(mkInput 17 8 1 2 ((as const (Array Int Int)) 0) false) "
            "(mkConfiguration true 8)) 3))"
        ),
        "introselect-dispatch": (
            "(assert (= (PartitionAtIndexBranch "
            "(mkInput 17 8 1 2 ((as const (Array Int Int)) 0) false) "
            "(mkConfiguration false 8)) 4))"
        ),
        "lomuto-simple-kernel": (
            "(assert (= (PartitionKernel (mkConfiguration true 8)) 0))"
        ),
        "lomuto-cyclic-unroll-two-kernel": (
            "(assert (= (PartitionKernel (mkConfiguration false 8)) 1))"
        ),
        "lomuto-cyclic-unroll-one-kernel": (
            "(assert (= (PartitionKernel (mkConfiguration false 32)) 2))"
        ),
        "hoare-cyclic-kernel": (
            "(assert (= (PartitionKernel (mkConfiguration false 128)) 3))"
        ),
        "choose-pivot-recursive": (
            "(assert (ChoosePivotRecurses 64))"
        ),
        "introselect-limit-sixteen": (
            "(assert (= IntroselectLimit 16))"
        ),
        "ninther-frac-small": (
            "(assert (= (NintherFraction 24) 2))"
        ),
        "ninther-frac-medium": (
            "(assert (= (NintherFraction 1025) 16))"
        ),
        "ninther-frac-large": (
            "(assert (= (NintherFraction 131073) 128))"
        ),
        "median-index-c": (
            "(assert (= (MedianIndex true true false 0 1 2) 0))"
        ),
        "median-index-a": (
            "(assert (= (MedianIndex false false true 0 1 2) 0))"
        ),
        "median-index-b": (
            "(assert (= (MedianIndex false false false 0 1 2) 1))"
        ),
        "left-narrowing-shrinks": """\
(define-fun m () Machine
  (mkMachine
    ((as const (Array Int Int)) 0) 0 0 40 10 16
    7 0 0 20 0 0 0 0 false false))
(assert
  (WindowShrinks
    (m_start m) (m_end m)
    (m_start (NarrowLeft m)) (m_end (NarrowLeft m))))""",
        "right-narrowing-shrinks": """\
(define-fun m () Machine
  (mkMachine
    ((as const (Array Int Int)) 0) 0 0 40 30 16
    7 0 0 20 0 0 0 0 false false))
(assert
  (WindowShrinks
    (m_start m) (m_end m)
    (m_start (NarrowRight m)) (m_end (NarrowRight m))))""",
        "ancestor-reverse-predicate": """\
(declare-const b Boundary)
(assert
  (= (AncestorReversePredicate b 0 7 9)
     (not (TargetAdapterIsLess b 0 9 7))))""",
        "returned-reference-layout": """\
(define-fun x () Input
  (mkInput 17 8 41 51 ((as const (Array Int Int)) 0) false))
(assert (= (ref_span (LeftReference x)) 8))
(assert (= (ref_start (PivotReference x)) 8))
(assert (= (ref_start (RightReference x)) 9))
(assert (= (ref_span (RightReference x)) 8))""",
        "callback-step-consumes-boundary": (
            _integer_boundary()
            + """\
(define-fun sequence () (Array Int Int)
  (store
    (store ((as const (Array Int Int)) 0) 0 1)
    1 2))
(define-fun m () Machine
  (mkMachine sequence 0 0 2 1 16 1 1 1 0 0 0 0 0 false false))
(define-fun next () Machine (ExtremeScanStep m b))
(assert (= (m_callback_state next) 1))
(assert (= (m_accumulator next) 1))
(assert (= (m_cursor next) 2))
(assert (not (m_panicked next)))"""
        ),
        "extreme-swap-mutates-sequence": """\
(define-fun sequence () (Array Int Int)
  (store
    (store ((as const (Array Int Int)) 0) 0 11)
    1 22))
(define-fun x () Input (mkInput 2 1 41 51 sequence false))
(define-fun m () Machine
  (mkMachine sequence 0 0 2 1 16 2 1 2 0 0 0 0 0 false false))
(define-fun next () Machine (ExtremeSwapStep m x))
(assert (= (select (m_sequence next) 0) 22))
(assert (= (select (m_sequence next) 1) 11))
(assert (m_terminal next))""",
        "insertion-shift-mutates-sequence": (
            _integer_boundary()
            + """\
(define-fun sequence () (Array Int Int)
  (store
    (store
      (store ((as const (Array Int Int)) 0) 0 3)
      1 2)
    2 1))
(define-fun m () Machine
  (mkMachine sequence 0 0 3 1 16 4 4 0 0 2 1 2 1 false false))
(define-fun next () Machine (InsertionShiftStep m b))
(assert (= (select (m_sequence next) 2) 2))
(assert (= (m_gap next) 1))
(assert (= (m_sift next) 0))
(assert (= (m_callback_state next) 1))
(assert (= (m_phase next) 4))"""
        ),
    }
    return assertions[kind]


def probe_text(kind: str) -> str:
    if kind not in PROBE_KINDS:
        raise ValueError(f"unknown target-078 probe: {kind}")
    return _prefix() + _probe_assertion(kind) + "\n(check-sat)\n"


def mutation_probe_text(kind: str) -> str:
    if kind not in MUTATION_PROBES:
        raise ValueError(f"unknown target-078 mutation probe: {kind}")
    probe, old, new = MUTATION_PROBES[kind]
    text = probe_text(probe)
    if old not in text:
        raise ValueError(
            f"{kind}: mutation anchor is missing"
        )
    return text.replace(old, new, 1)


def validate_obligation(text: str, metadata: dict[str, Any]) -> None:
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES or metadata != obligation_metadata(purpose):
        raise ValueError("target-078 operational metadata changed")
    if f"; Obligation purpose: {purpose}\n" not in text:
        raise ValueError("target-078 purpose is not bound in SMT")
    if "(declare-fun WholeSelection" in text:
        raise ValueError("opaque whole-selection relation is forbidden")
    if exact_smt.definitions_text() not in text:
        raise ValueError("exact source transition block changed")
    for symbol in SOURCE_TRANSITIONS:
        if symbol in exact_smt.SOURCE_TRANSITIONS:
            continue
        if (
            f"(define-fun {symbol}" not in text
            and f"(define-fun-rec {symbol}" not in text
        ):
            raise ValueError(f"missing source transition: {symbol}")
    for symbol in ("y1", "s1", "y2", "s2"):
        if f"(declare-const {symbol} " not in text:
            raise ValueError("obligation lacks independent executions")
    if text.count("(assert (TargetDefinition_T x b c") != 2:
        raise ValueError("both executions must satisfy TargetDefinition_T")
    if "(m_terminal run)" not in text:
        raise ValueError("target definition permits a nonterminal execution")
    if "(b_contract_ordering (Array PairKey Int))" not in text:
        raise ValueError("state-independent contract Ordering is missing")
    for contract_law in (
        "(ContractOrdering b left right)))",
        "(= (ContractOrdering b value value) 0)",
        "(- (ContractOrdering b right left))",
        "(<= (ContractOrdering b left middle) 0)",
        "(<= (ContractOrdering b middle right) 0)",
    ):
        if contract_law not in text:
            raise ValueError("contract Ordering axioms are incomplete")
    boundary_block = text[
        text.index("(declare-datatypes ((Boundary 0))") :
        text.index("(declare-datatypes ((Reference 0))")
    ].lower()
    for forbidden in (
        "pivot",
        "permutation",
        "returned",
        "final_sequence",
        "final_callback",
        "trace",
    ):
        if forbidden in boundary_block:
            raise ValueError(
                f"answer-bearing boundary selector found: {forbidden}"
            )
