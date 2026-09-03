#!/usr/bin/env python3
"""Source-exact big-step SMT transition for target 078."""

from __future__ import annotations


SOURCE_TRANSITIONS = (
    "ExactCallback",
    "ExactSwap",
    "ExactInsertTailLoop",
    "ExactInsertTail",
    "ExactInsertionSortLoop",
    "ExactExtremeScanLoop",
    "ExactMedian3",
    "ExactMedian3Rec",
    "ExactChoosePivot",
    "ExactPartitionPredicate",
    "ExactLomutoSimpleLoop",
    "ExactLomutoCyclicLoop",
    "ExactRestoreGap",
    "ExactHoareLoop",
    "ExactPartition",
    "ExactMedianIdx",
    "ExactNintherFinishLow",
    "ExactNinther",
    "ExactMedianOfNinthers",
    "ExactMedianOfNinthersLoop",
    "ExactMedianOfMedians",
    "ExactIntroselect",
    "ExactIntroselectPartition",
    "ExactRunState",
    "RunMachine",
)


def definitions_text() -> str:
    return r"""
; Source-exact big-step state. Every callback updates this state before panic
; propagation, and every active gap guard restores its saved identity.
(declare-datatypes ((ExactState 0))
  (((mkExactState
      (e_sequence (Array Int Int))
      (e_callback_state Int)
      (e_panicked Bool)))))
(declare-datatypes ((ExactIndexResult 0))
  (((mkExactIndexResult
      (eir_state ExactState)
      (eir_value Int)))))
(declare-datatypes ((ExactBoolResult 0))
  (((mkExactBoolResult
      (ebr_state ExactState)
      (ebr_value Bool)))))

(define-fun ExactCallback
  ((q ExactState) (b Boundary) (left Int) (right Int)) ExactState
  (mkExactState
    (e_sequence q)
    (BoundaryNextState b (e_callback_state q) left right)
    (BoundaryPanics b (e_callback_state q) left right)))
(define-fun ExactSwap
  ((q ExactState) (left Int) (right Int)) ExactState
  (mkExactState
    (SwapArray (e_sequence q) left right)
    (e_callback_state q)
    (e_panicked q)))

; insertion_sort_shift_left / insert_tail / CopyOnDrop
(define-fun-rec ExactInsertTailLoop
  ((q ExactState)
   (b Boundary)
   (begin Int)
   (sift Int)
   (gap Int)
   (temporary Int)) ExactState
  (ite
    (e_panicked q)
    q
    (let ((shifted
            (mkExactState
              (store
                (e_sequence q)
                gap
                (select (e_sequence q) sift))
              (e_callback_state q)
              false)))
      (ite
        (= sift begin)
        (mkExactState
          (store (e_sequence shifted) sift temporary)
          (e_callback_state shifted)
          false)
        (let ((next_sift (- sift 1)))
          (let ((right (select (e_sequence shifted) next_sift)))
            (let ((called
                    (ExactCallback shifted b temporary right))
                  (less
                    (TargetAdapterIsLess
                      b
                      (e_callback_state shifted)
                      temporary
                      right)))
              (ite
                (e_panicked called)
                (mkExactState
                  (store (e_sequence called) sift temporary)
                  (e_callback_state called)
                  true)
                (ite
                  less
                  (ExactInsertTailLoop
                    called b begin next_sift sift temporary)
                  (mkExactState
                    (store (e_sequence called) sift temporary)
                    (e_callback_state called)
                    false))))))))))

(define-fun ExactInsertTail
  ((q ExactState) (b Boundary) (begin Int) (tail Int)) ExactState
  (ite
    (e_panicked q)
    q
    (let ((temporary (select (e_sequence q) tail))
          (right (select (e_sequence q) (- tail 1))))
      (let ((called (ExactCallback q b temporary right))
            (less
              (TargetAdapterIsLess
                b (e_callback_state q) temporary right)))
        (ite
          (e_panicked called)
          called
          (ite
            less
            (ExactInsertTailLoop
              called b begin (- tail 1) tail temporary)
            called))))))

(define-fun-rec ExactInsertionSortLoop
  ((q ExactState)
   (b Boundary)
   (start Int)
   (end Int)
   (tail Int)) ExactState
  (ite
    (or (e_panicked q) (>= tail end))
    q
    (let ((next (ExactInsertTail q b start tail)))
      (ite
        (e_panicked next)
        next
        (ExactInsertionSortLoop next b start end (+ tail 1))))))

; min/max source scans
(define-fun-rec ExactExtremeScanLoop
  ((q ExactState)
   (b Boundary)
   (end Int)
   (candidate Int)
   (accumulator Int)
   (find_min Bool)) ExactIndexResult
  (ite
    (or (e_panicked q) (>= candidate end))
    (mkExactIndexResult q accumulator)
    (let ((left
            (ite
              find_min
              (select (e_sequence q) candidate)
              (select (e_sequence q) accumulator)))
          (right
            (ite
              find_min
              (select (e_sequence q) accumulator)
              (select (e_sequence q) candidate))))
      (let ((called (ExactCallback q b left right))
            (less
              (TargetAdapterIsLess
                b (e_callback_state q) left right)))
        (ite
          (e_panicked called)
          (mkExactIndexResult called accumulator)
          (ExactExtremeScanLoop
            called
            b
            end
            (+ candidate 1)
            (ite less candidate accumulator)
            find_min))))))

; choose_pivot / median3_rec / median3
(define-fun ExactMedian3
  ((q ExactState)
   (b Boundary)
   (a Int)
   (sample_b Int)
   (c Int)) ExactIndexResult
  (let ((value_a (select (e_sequence q) a))
        (value_b (select (e_sequence q) sample_b)))
    (let ((first (ExactCallback q b value_a value_b))
          (less_a_b
            (TargetAdapterIsLess
              b (e_callback_state q) value_a value_b)))
      (ite
        (e_panicked first)
        (mkExactIndexResult first a)
        (let ((value_c (select (e_sequence first) c)))
          (let ((second
                  (ExactCallback first b value_a value_c))
                (less_a_c
                  (TargetAdapterIsLess
                    b (e_callback_state first) value_a value_c)))
            (ite
              (e_panicked second)
              (mkExactIndexResult second a)
              (ite
                (= less_a_b less_a_c)
                (let ((third
                        (ExactCallback second b value_b value_c))
                      (less_b_c
                        (TargetAdapterIsLess
                          b
                          (e_callback_state second)
                          value_b
                          value_c)))
                  (mkExactIndexResult
                    third
                    (ite (xor less_b_c less_a_b) c sample_b)))
                (mkExactIndexResult second a)))))))))

(define-fun-rec ExactMedian3Rec
  ((q ExactState)
   (b Boundary)
   (a Int)
   (sample_b Int)
   (c Int)
   (n Int)) ExactIndexResult
  (ite
    (e_panicked q)
    (mkExactIndexResult q a)
    (ite
      (>= (* n 8) 64)
      (let ((n8 (div n 8)))
        (let ((first
                (ExactMedian3Rec
                  q b a (+ a (* n8 4)) (+ a (* n8 7)) n8)))
          (ite
            (e_panicked (eir_state first))
            first
            (let ((second
                    (ExactMedian3Rec
                      (eir_state first)
                      b
                      sample_b
                      (+ sample_b (* n8 4))
                      (+ sample_b (* n8 7))
                      n8)))
              (ite
                (e_panicked (eir_state second))
                second
                (let ((third
                        (ExactMedian3Rec
                          (eir_state second)
                          b
                          c
                          (+ c (* n8 4))
                          (+ c (* n8 7))
                          n8)))
                  (ite
                    (e_panicked (eir_state third))
                    third
                    (ExactMedian3
                      (eir_state third)
                      b
                      (eir_value first)
                      (eir_value second)
                      (eir_value third)))))))))
      (ExactMedian3 q b a sample_b c))))

(define-fun ExactChoosePivot
  ((q ExactState) (b Boundary) (start Int) (end Int)) ExactIndexResult
  (let ((length (- end start)))
    (let ((eighth (div length 8)))
      (let ((a start)
            (sample_b (+ start (* eighth 4)))
            (c (+ start (* eighth 7))))
        (let ((chosen
                (ite
                  (< length 64)
                  (ExactMedian3 q b a sample_b c)
                  (ExactMedian3Rec q b a sample_b c eighth))))
          (mkExactIndexResult
            (eir_state chosen)
            (- (eir_value chosen) start)))))))

; Partition predicate adapter, including ancestor-pivot reverse partition.
(define-fun ExactPartitionPredicate
  ((q ExactState)
   (b Boundary)
   (value Int)
   (pivot Int)
   (reverse Bool)) ExactBoolResult
  (ite
    reverse
    (let ((called (ExactCallback q b pivot value)))
      (mkExactBoolResult
        called
        (not
          (TargetAdapterIsLess
            b (e_callback_state q) pivot value))))
    (let ((called (ExactCallback q b value pivot)))
      (mkExactBoolResult
        called
        (TargetAdapterIsLess
          b (e_callback_state q) value pivot)))))

(define-fun-rec ExactLomutoSimpleLoop
  ((q ExactState)
   (b Boundary)
   (start Int)
   (end Int)
   (left Int)
   (right Int)
   (pivot Int)
   (reverse Bool)) ExactIndexResult
  (ite
    (or (e_panicked q) (>= right end))
    (mkExactIndexResult q (- left start))
    (let ((predicate
            (ExactPartitionPredicate
              q b (select (e_sequence q) right) pivot reverse)))
      (ite
        (e_panicked (ebr_state predicate))
        (mkExactIndexResult (ebr_state predicate) (- left start))
        (let ((swapped
                (ExactSwap (ebr_state predicate) left right)))
          (ExactLomutoSimpleLoop
            swapped
            b
            start
            end
            (ite (ebr_value predicate) (+ left 1) left)
            (+ right 1)
            pivot
            reverse))))))

(define-fun-rec ExactLomutoCyclicLoop
  ((q ExactState)
   (b Boundary)
   (start Int)
   (end Int)
   (right Int)
   (num_lt Int)
   (gap_value Int)
   (gap_position Int)
   (pivot Int)
   (reverse Bool)) ExactIndexResult
  (ite
    (e_panicked q)
    (mkExactIndexResult
      (mkExactState
        (store (e_sequence q) gap_position gap_value)
        (e_callback_state q)
        true)
      num_lt)
    (ite
      (< right end)
      (let ((right_value (select (e_sequence q) right)))
        (let ((predicate
                (ExactPartitionPredicate
                  q b right_value pivot reverse)))
          (ite
            (e_panicked (ebr_state predicate))
            (mkExactIndexResult
              (mkExactState
                (store
                  (e_sequence (ebr_state predicate))
                  gap_position
                  gap_value)
                (e_callback_state (ebr_state predicate))
                true)
              num_lt)
            (let ((left (+ start num_lt)))
              (let ((cycled
                      (mkExactState
                        (store
                          (store
                            (e_sequence (ebr_state predicate))
                            gap_position
                            (select
                              (e_sequence (ebr_state predicate))
                              left))
                          left
                          right_value)
                        (e_callback_state (ebr_state predicate))
                        false)))
                (ExactLomutoCyclicLoop
                  cycled
                  b
                  start
                  end
                  (+ right 1)
                  (ite (ebr_value predicate) (+ num_lt 1) num_lt)
                  gap_value
                  right
                  pivot
                  reverse))))))
      (let ((predicate
              (ExactPartitionPredicate q b gap_value pivot reverse)))
        (ite
          (e_panicked (ebr_state predicate))
          (mkExactIndexResult
            (mkExactState
              (store
                (e_sequence (ebr_state predicate))
                gap_position
                gap_value)
              (e_callback_state (ebr_state predicate))
              true)
            num_lt)
          (let ((left (+ start num_lt)))
            (let ((cycled
                    (mkExactState
                      (store
                        (store
                          (e_sequence (ebr_state predicate))
                          gap_position
                          (select
                            (e_sequence (ebr_state predicate))
                            left))
                        left
                        gap_value)
                      (e_callback_state (ebr_state predicate))
                      false)))
              (mkExactIndexResult
                cycled
                (ite (ebr_value predicate) (+ num_lt 1) num_lt)))))))))

(define-fun ExactRestoreGap
  ((q ExactState)
   (gap_present Bool)
   (gap_value Int)
   (gap_position Int)) ExactState
  (ite
    gap_present
    (mkExactState
      (store (e_sequence q) gap_position gap_value)
      (e_callback_state q)
      (e_panicked q))
    q))

(define-fun-rec ExactHoareLoop
  ((q ExactState)
   (b Boundary)
   (start Int)
   (pivot Int)
   (reverse Bool)
   (left Int)
   (right Int)
   (gap_present Bool)
   (gap_value Int)
   (gap_position Int)
   (scan_right Bool)) ExactIndexResult
  (ite
    (e_panicked q)
    (mkExactIndexResult
      (ExactRestoreGap q gap_present gap_value gap_position)
      (- left start))
    (ite
      scan_right
      (let ((next_right (- right 1)))
        (ite
          (>= left next_right)
          (mkExactIndexResult
            (ExactRestoreGap q gap_present gap_value gap_position)
            (- left start))
          (let ((predicate
                  (ExactPartitionPredicate
                    q
                    b
                    (select (e_sequence q) next_right)
                    pivot
                    reverse)))
            (ite
              (e_panicked (ebr_state predicate))
              (mkExactIndexResult
                (ExactRestoreGap
                  (ebr_state predicate)
                  gap_present
                  gap_value
                  gap_position)
                (- left start))
              (ite
                (ebr_value predicate)
                (let ((saved
                        (ite
                          gap_present
                          gap_value
                          (select
                            (e_sequence (ebr_state predicate))
                            left)))
                      (filled
                        (ite
                          gap_present
                          (store
                            (e_sequence (ebr_state predicate))
                            gap_position
                            (select
                              (e_sequence (ebr_state predicate))
                              left))
                          (e_sequence (ebr_state predicate)))))
                  (let ((cycled
                          (mkExactState
                            (store
                              filled
                              left
                              (select
                                (e_sequence (ebr_state predicate))
                                next_right))
                            (e_callback_state (ebr_state predicate))
                            false)))
                    (ExactHoareLoop
                      cycled b start pivot reverse
                      (+ left 1) next_right true saved next_right false)))
                (ExactHoareLoop
                  (ebr_state predicate)
                  b
                  start
                  pivot
                  reverse
                  left
                  next_right
                  gap_present
                  gap_value
                  gap_position
                  true))))))
      (ite
        (>= left right)
        (mkExactIndexResult
          (ExactRestoreGap q gap_present gap_value gap_position)
          (- left start))
        (let ((predicate
                (ExactPartitionPredicate
                  q b (select (e_sequence q) left) pivot reverse)))
          (ite
            (e_panicked (ebr_state predicate))
            (mkExactIndexResult
              (ExactRestoreGap
                (ebr_state predicate)
                gap_present
                gap_value
                gap_position)
              (- left start))
            (ite
              (ebr_value predicate)
              (ExactHoareLoop
                (ebr_state predicate)
                b
                start
                pivot
                reverse
                (+ left 1)
                right
                gap_present
                gap_value
                gap_position
                false)
              (ExactHoareLoop
                (ebr_state predicate)
                b
                start
                pivot
                reverse
                left
                right
                gap_present
                gap_value
                gap_position
                true))))))))

(define-fun ExactPartition
  ((q ExactState)
   (b Boundary)
   (c Configuration)
   (start Int)
   (end Int)
   (pivot_position Int)
   (reverse Bool)) ExactIndexResult
  (let ((pivot_global (+ start pivot_position)))
    (let ((pivoted (ExactSwap q start pivot_global)))
      (let ((pivot (select (e_sequence pivoted) start))
            (lower_start (+ start 1)))
        (let ((partitioned
                (ite
                  (> (c_element_size c) 96)
                  (ExactHoareLoop
                    pivoted
                    b
                    lower_start
                    pivot
                    reverse
                    lower_start
                    end
                    false
                    0
                    0
                    false)
                  (ite
                    (c_optimize_for_size c)
                    (ExactLomutoSimpleLoop
                      pivoted
                      b
                      lower_start
                      end
                      lower_start
                      lower_start
                      pivot
                      reverse)
                    (ExactLomutoCyclicLoop
                      pivoted
                      b
                      lower_start
                      end
                      (+ lower_start 1)
                      0
                      (select (e_sequence pivoted) lower_start)
                      lower_start
                      pivot
                      reverse)))))
          (ite
            (e_panicked (eir_state partitioned))
            partitioned
            (mkExactIndexResult
              (ExactSwap
                (eir_state partitioned)
                start
                (+ start (eir_value partitioned)))
              (eir_value partitioned))))))))

; median_idx and ninther helpers used by the deterministic fallback.
(define-fun ExactMedianIdx
  ((q ExactState)
   (b Boundary)
   (a Int)
   (sample_b Int)
   (c Int)) ExactIndexResult
  (let ((first
          (ExactCallback
            q b
            (select (e_sequence q) c)
            (select (e_sequence q) a)))
        (less_c_a
          (TargetAdapterIsLess
            b
            (e_callback_state q)
            (select (e_sequence q) c)
            (select (e_sequence q) a))))
    (ite
      (e_panicked first)
      (mkExactIndexResult first a)
      (let ((aprime (ite less_c_a c a))
            (cprime (ite less_c_a a c)))
        (let ((second
                (ExactCallback
                  first b
                  (select (e_sequence first) cprime)
                  (select (e_sequence first) sample_b)))
              (less_cprime_b
                (TargetAdapterIsLess
                  b
                  (e_callback_state first)
                  (select (e_sequence first) cprime)
                  (select (e_sequence first) sample_b))))
          (ite
            (e_panicked second)
            (mkExactIndexResult second cprime)
            (ite
              less_cprime_b
              (mkExactIndexResult second cprime)
              (let ((third
                      (ExactCallback
                        second b
                        (select (e_sequence second) sample_b)
                        (select (e_sequence second) aprime)))
                    (less_b_aprime
                      (TargetAdapterIsLess
                        b
                        (e_callback_state second)
                        (select (e_sequence second) sample_b)
                        (select (e_sequence second) aprime))))
                (mkExactIndexResult
                  third
                  (ite less_b_aprime aprime sample_b))))))))))

(define-fun ExactNintherFinishLow
  ((q ExactState)
   (b Boundary)
   (sample_b Int)
   (h Int)
   (d Int)
   (e Int)) ExactState
  (let ((first
          (ExactCallback
            q b
            (select (e_sequence q) d)
            (select (e_sequence q) sample_b)))
        (less_d_b
          (TargetAdapterIsLess
            b
            (e_callback_state q)
            (select (e_sequence q) d)
            (select (e_sequence q) sample_b))))
    (ite
      (e_panicked first)
      first
      (ite
        less_d_b
        (ExactSwap first sample_b e)
        (let ((second
                (ExactCallback
                  first b
                  (select (e_sequence first) h)
                  (select (e_sequence first) d)))
              (less_h_d
                (TargetAdapterIsLess
                  b
                  (e_callback_state first)
                  (select (e_sequence first) h)
                  (select (e_sequence first) d))))
          (ite
            (e_panicked second)
            second
            (ExactSwap second (ite less_h_d h d) e)))))))

(define-fun ExactNinther
  ((q ExactState)
   (b Boundary)
   (a Int)
   (sample_b Int)
   (c Int)
   (d Int)
   (e Int)
   (f Int)
   (g Int)
   (h Int)
   (i Int)) ExactState
  (let ((left_median (ExactMedianIdx q b a sample_b c)))
    (ite
      (e_panicked (eir_state left_median))
      (eir_state left_median)
      (let ((right_median
              (ExactMedianIdx
                (eir_state left_median) b g h i)))
        (ite
          (e_panicked (eir_state right_median))
          (eir_state right_median)
          (let ((bprime (eir_value left_median))
                (hprime (eir_value right_median)))
            (let ((hb
                    (ExactCallback
                      (eir_state right_median)
                      b
                      (select
                        (e_sequence (eir_state right_median))
                        hprime)
                      (select
                        (e_sequence (eir_state right_median))
                        bprime)))
                  (less_h_b
                    (TargetAdapterIsLess
                      b
                      (e_callback_state (eir_state right_median))
                      (select
                        (e_sequence (eir_state right_median))
                        hprime)
                      (select
                        (e_sequence (eir_state right_median))
                        bprime))))
              (ite
                (e_panicked hb)
                hb
                (let ((bfinal (ite less_h_b hprime bprime))
                      (hfinal (ite less_h_b bprime hprime)))
                  (let ((fd
                          (ExactCallback
                            hb b
                            (select (e_sequence hb) f)
                            (select (e_sequence hb) d)))
                        (less_f_d
                          (TargetAdapterIsLess
                            b
                            (e_callback_state hb)
                            (select (e_sequence hb) f)
                            (select (e_sequence hb) d))))
                    (ite
                      (e_panicked fd)
                      fd
                      (let ((dfinal (ite less_f_d f d))
                            (ffinal (ite less_f_d d f)))
                        (let ((ed
                                (ExactCallback
                                  fd b
                                  (select (e_sequence fd) e)
                                  (select (e_sequence fd) dfinal)))
                              (less_e_d
                                (TargetAdapterIsLess
                                  b
                                  (e_callback_state fd)
                                  (select (e_sequence fd) e)
                                  (select (e_sequence fd) dfinal))))
                          (ite
                            (e_panicked ed)
                            ed
                            (ite
                              less_e_d
                              (ExactNintherFinishLow
                                ed b bfinal hfinal dfinal e)
                              (let ((fe
                                      (ExactCallback
                                        ed b
                                        (select (e_sequence ed) ffinal)
                                        (select (e_sequence ed) e)))
                                    (less_f_e
                                      (TargetAdapterIsLess
                                        b
                                        (e_callback_state ed)
                                        (select (e_sequence ed) ffinal)
                                        (select (e_sequence ed) e))))
                                (ite
                                  (e_panicked fe)
                                  fe
                                  (ite
                                    less_f_e
                                    (ExactNintherFinishLow
                                      fe b bfinal hfinal ffinal e)
                                    (let ((eb
                                            (ExactCallback
                                              fe b
                                              (select (e_sequence fe) e)
                                              (select
                                                (e_sequence fe)
                                                bfinal)))
                                          (less_e_b
                                            (TargetAdapterIsLess
                                              b
                                              (e_callback_state fe)
                                              (select (e_sequence fe) e)
                                              (select
                                                (e_sequence fe)
                                                bfinal))))
                                      (ite
                                        (e_panicked eb)
                                        eb
                                        (ite
                                          less_e_b
                                          (ExactSwap eb e bfinal)
                                          (let ((he
                                                  (ExactCallback
                                                    eb b
                                                    (select
                                                      (e_sequence eb)
                                                      hfinal)
                                                    (select
                                                      (e_sequence eb)
                                                      e)))
                                                (less_h_e
                                                  (TargetAdapterIsLess
                                                    b
                                                    (e_callback_state eb)
                                                    (select
                                                      (e_sequence eb)
                                                      hfinal)
                                                    (select
                                                      (e_sequence eb)
                                                      e))))
                                            (ite
                                              (e_panicked he)
                                              he
                                              (ite
                                                less_h_e
                                                (ExactSwap he e hfinal)
                                                he))))))))))))))))))))))))

; The three fallback functions are mutually recursive exactly as
; median_of_ninthers invokes median_of_medians on its sample and
; median_of_medians invokes median_of_ninthers on each large window.
(define-funs-rec
  ((ExactMedianOfNinthers
      ((q ExactState)
       (b Boundary)
       (c Configuration)
       (start Int)
       (end Int))
      ExactIndexResult)
   (ExactMedianOfNinthersLoop
      ((q ExactState)
       (b Boundary)
       (c Configuration)
       (start Int)
       (end Int)
       (frac Int)
       (pivot Int)
       (lo Int)
       (hi Int)
       (a Int)
       (sample_b Int)
       (local_i Int))
      ExactIndexResult)
   (ExactMedianOfMedians
      ((q ExactState)
       (b Boundary)
       (c Configuration)
       (start Int)
       (end Int)
       (k Int))
      ExactState))
  ((let ((length (- end start)))
     (let ((frac
             (ite
               (<= length 1024)
               (div length 12)
               (ite
                 (<= length (* 128 1024))
                 (div length 64)
                 (div length 1024)))))
       (let ((pivot (div frac 2))
             (lo (- (div length 2) (div frac 2)))
             (gap (div (- length (* 9 frac)) 4)))
         (let ((hi (+ frac lo)))
           (ExactMedianOfNinthersLoop
             q
             b
             c
             start
             end
             frac
             pivot
             lo
             hi
             (- lo (* 4 frac) gap)
             (+ hi gap)
             lo)))))
   (ite
     (e_panicked q)
     (mkExactIndexResult q 0)
     (ite
       (< local_i hi)
       (let ((next
               (ExactNinther
                 q
                 b
                 (+ start a)
                 (+ start local_i (- frac))
                 (+ start sample_b)
                 (+ start a 1)
                 (+ start local_i)
                 (+ start sample_b 1)
                 (+ start a 2)
                 (+ start local_i frac)
                 (+ start sample_b 2))))
         (ite
           (e_panicked next)
           (mkExactIndexResult next 0)
           (ExactMedianOfNinthersLoop
             next
             b
             c
             start
             end
             frac
             pivot
             lo
             hi
             (+ a 3)
             (+ sample_b 3)
             (+ local_i 1))))
       (let ((sampled
               (ExactMedianOfMedians
                 q
                 b
                 c
                 (+ start lo)
                 (+ start lo frac)
                 pivot)))
         (ite
           (e_panicked sampled)
           (mkExactIndexResult sampled 0)
           (ExactPartition
             sampled b c start end (+ lo pivot) false)))))
   (ite
     (e_panicked q)
     q
     (let ((length (- end start)))
       (ite
         (<= length 16)
         (ite
           (>= length 2)
           (ExactInsertionSortLoop q b start end (+ start 1))
           q)
         (ite
           (= k (- length 1))
           (let ((extreme
                   (ExactExtremeScanLoop
                     q b end (+ start 1) start false)))
             (ite
               (e_panicked (eir_state extreme))
               (eir_state extreme)
               (ExactSwap
                 (eir_state extreme)
                 (eir_value extreme)
                 (+ start k))))
           (ite
             (= k 0)
             (let ((extreme
                     (ExactExtremeScanLoop
                       q b end (+ start 1) start true)))
               (ite
                 (e_panicked (eir_state extreme))
                 (eir_state extreme)
                 (ExactSwap
                   (eir_state extreme)
                   (eir_value extreme)
                   start)))
             (let ((partitioned
                     (ExactMedianOfNinthers q b c start end)))
               (ite
                 (e_panicked (eir_state partitioned))
                 (eir_state partitioned)
                 (ite
                   (= (eir_value partitioned) k)
                   (eir_state partitioned)
                   (ite
                     (> (eir_value partitioned) k)
                     (ExactMedianOfMedians
                       (eir_state partitioned)
                       b
                       c
                       start
                       (+ start (eir_value partitioned))
                       k)
                     (ExactMedianOfMedians
                       (eir_state partitioned)
                       b
                       c
                       (+ start (eir_value partitioned) 1)
                       end
                       (- k (eir_value partitioned) 1)))))))))))))

; Exact introselect loop. The helper performs the ordinary partition after
; choose_pivot and preserves or replaces the ancestor exactly on narrowing.
(define-funs-rec
  ((ExactIntroselect
      ((q ExactState)
       (b Boundary)
       (c Configuration)
       (start Int)
       (end Int)
       (index Int)
       (ancestor_present Bool)
       (ancestor Int)
       (limit Int))
      ExactState)
   (ExactIntroselectPartition
      ((q ExactState)
       (b Boundary)
       (c Configuration)
       (start Int)
       (end Int)
       (index Int)
       (ancestor_present Bool)
       (ancestor Int)
       (limit Int)
       (pivot_position Int))
      ExactState))
  ((ite
     (e_panicked q)
     q
     (let ((length (- end start)))
       (ite
         (<= length 16)
         (ite
           (>= length 2)
           (ExactInsertionSortLoop q b start end (+ start 1))
           q)
         (ite
           (<= limit 0)
           (ExactMedianOfMedians q b c start end index)
           (let ((chosen (ExactChoosePivot q b start end)))
             (ite
               (e_panicked (eir_state chosen))
               (eir_state chosen)
               (ite
                 ancestor_present
                 (let ((pivot_identity
                         (select
                           (e_sequence (eir_state chosen))
                           (+ start (eir_value chosen)))))
                   (let ((compared
                           (ExactCallback
                             (eir_state chosen)
                             b
                             ancestor
                             pivot_identity))
                         (ancestor_less
                           (TargetAdapterIsLess
                             b
                             (e_callback_state (eir_state chosen))
                             ancestor
                             pivot_identity)))
                     (ite
                       (e_panicked compared)
                       compared
                       (ite
                         ancestor_less
                         (ExactIntroselectPartition
                           compared
                           b
                           c
                           start
                           end
                           index
                           true
                           ancestor
                           (- limit 1)
                           (eir_value chosen))
                         (let ((partitioned
                                 (ExactPartition
                                   compared
                                   b
                                   c
                                   start
                                   end
                                   (eir_value chosen)
                                   true)))
                           (ite
                             (e_panicked (eir_state partitioned))
                             (eir_state partitioned)
                             (let ((mid (+ (eir_value partitioned) 1)))
                               (ite
                                 (> mid index)
                                 (eir_state partitioned)
                                 (ExactIntroselect
                                   (eir_state partitioned)
                                   b
                                   c
                                   (+ start mid)
                                   end
                                   (- index mid)
                                   false
                                   0
                                   (- limit 1))))))))))
                 (ExactIntroselectPartition
                   (eir_state chosen)
                   b
                   c
                   start
                   end
                   index
                   false
                   0
                   (- limit 1)
                   (eir_value chosen)))))))))
   (let ((partitioned
           (ExactPartition q b c start end pivot_position false)))
     (ite
       (e_panicked (eir_state partitioned))
       (eir_state partitioned)
       (ite
         (< (eir_value partitioned) index)
         (ExactIntroselect
           (eir_state partitioned)
           b
           c
           (+ start (eir_value partitioned) 1)
           end
           (- index (eir_value partitioned) 1)
           true
           (select
             (e_sequence (eir_state partitioned))
             (+ start (eir_value partitioned)))
           limit)
         (ite
           (> (eir_value partitioned) index)
           (ExactIntroselect
             (eir_state partitioned)
             b
             c
             start
             (+ start (eir_value partitioned))
             index
             ancestor_present
             ancestor
             limit)
           (eir_state partitioned)))))))

(define-fun ExactRunState
  ((x Input) (b Boundary) (c Configuration)) ExactState
  (let ((initial
          (mkExactState
            (x_initial_sequence x)
            (b_initial_state b)
            false)))
    (ite
      (x_is_zst x)
      initial
      (ite
        (= (x_index x) (- (x_length x) 1))
        (let ((extreme
                (ExactExtremeScanLoop
                  initial b (x_length x) 1 0 false)))
          (ite
            (e_panicked (eir_state extreme))
            (eir_state extreme)
            (ExactSwap
              (eir_state extreme)
              (eir_value extreme)
              (x_index x))))
        (ite
          (= (x_index x) 0)
          (let ((extreme
                  (ExactExtremeScanLoop
                    initial b (x_length x) 1 0 true)))
            (ite
              (e_panicked (eir_state extreme))
              (eir_state extreme)
              (ExactSwap
                (eir_state extreme)
                (eir_value extreme)
                0)))
          (ite
            (c_optimize_for_size c)
            (ExactMedianOfMedians
              initial b c 0 (x_length x) (x_index x))
            (ExactIntroselect
              initial
              b
              c
              0
              (x_length x)
              (x_index x)
              false
              0
              16)))))))

(define-fun RunMachine
  ((x Input) (b Boundary) (c Configuration)) Machine
  (let ((run (ExactRunState x b c)))
    (mkMachine
      (e_sequence run)
      (e_callback_state run)
      0
      (x_length x)
      (x_index x)
      0
      11
      (PartitionKernel c)
      0
      0
      0
      0
      0
      0
      (e_panicked run)
      true)))
"""
