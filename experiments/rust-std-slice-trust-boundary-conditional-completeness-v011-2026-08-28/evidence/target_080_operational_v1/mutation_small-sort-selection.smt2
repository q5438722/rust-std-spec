; Target: core::slice::sort_unstable
; Model: target-080-operational-v1-rust-1.96-complete
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


(define-fun ExactLimitExhausted ((limit Int)) Bool
  (= limit 0))

; find_existing_run and descending reversal
(declare-datatypes ((ExactRunResult 0))
  (((mkExactRunResult
      (err_state ExactState)
      (err_length Int)
      (err_descending Bool)))))

(define-fun-rec ExactExistingRunLoop
  ((q ExactState)
   (b Boundary)
   (length Int)
   (run_length Int)
   (descending Bool)) ExactRunResult
  (ite
    (or (e_panicked q) (>= run_length length))
    (mkExactRunResult q run_length descending)
    (let ((left (select (e_sequence q) run_length))
          (right (select (e_sequence q) (- run_length 1))))
      (let ((called (ExactCallback q b left right))
            (less
              (TargetAdapterIsLess
                b (e_callback_state q) left right)))
        (ite
          (e_panicked called)
          (mkExactRunResult called run_length descending)
          (ite
            (ite descending less (not less))
            (ExactExistingRunLoop
              called b length (+ run_length 1) descending)
            (mkExactRunResult called run_length descending)))))))

(define-fun ExactFindExistingRun
  ((q ExactState) (b Boundary) (length Int)) ExactRunResult
  (ite
    (< length 2)
    (mkExactRunResult q length false)
    (let ((left (select (e_sequence q) 1))
          (right (select (e_sequence q) 0)))
      (let ((called (ExactCallback q b left right))
            (descending
              (TargetAdapterIsLess
                b (e_callback_state q) left right)))
        (ite
          (e_panicked called)
          (mkExactRunResult called 2 descending)
          (ExactExistingRunLoop called b length 2 descending))))))

(define-fun-rec ExactReverseLoop
  ((q ExactState) (left Int) (right Int)) ExactState
  (ite
    (or (e_panicked q) (>= left right))
    q
    (ExactReverseLoop
      (ExactSwap q left right) (+ left 1) (- right 1))))

; heapsort and sift_down
(define-funs-rec
  ((ExactSiftDown
      ((q ExactState)
       (b Boundary)
       (start Int)
       (end Int)
       (node Int)) ExactState)
   (ExactSiftDownParent
      ((q ExactState)
       (b Boundary)
       (start Int)
       (end Int)
       (node Int)
       (child Int)) ExactState))
  ((ite
     (e_panicked q)
     q
     (let ((length (- end start))
           (child (+ (* 2 node) 1)))
       (ite
         (>= child length)
         q
         (ite
           (< (+ child 1) length)
           (let ((left (select (e_sequence q) (+ start child)))
                 (right
                   (select (e_sequence q) (+ start child 1))))
             (let ((called (ExactCallback q b left right))
                   (right_greater
                     (TargetAdapterIsLess
                       b (e_callback_state q) left right)))
               (ite
                 (e_panicked called)
                 called
                 (ExactSiftDownParent
                   called
                   b
                   start
                   end
                   node
                   (ite right_greater (+ child 1) child)))))
           (ExactSiftDownParent q b start end node child)))))
   (ite
     (e_panicked q)
     q
     (let ((left (select (e_sequence q) (+ start node)))
           (right (select (e_sequence q) (+ start child))))
       (let ((called (ExactCallback q b left right))
             (parent_less
               (TargetAdapterIsLess
                 b (e_callback_state q) left right)))
         (ite
           (e_panicked called)
           called
           (ite
             parent_less
             (ExactSiftDown
               (ExactSwap q (+ start node) (+ start child))
               b
               start
               end
               child)
             called)))))))

(define-fun-rec ExactHeapSortLoop
  ((q ExactState)
   (b Boundary)
   (start Int)
   (length Int)
   (index Int)) ExactState
  (ite
    (or (e_panicked q) (< index 0))
    q
    (let ((sifted
            (ite
              (>= index length)
              (ExactSiftDown
                q b start (+ start length) (- index length))
              (ExactSiftDown
                (ExactSwap q start (+ start index))
                b
                start
                (+ start index)
                0))))
      (ExactHeapSortLoop sifted b start length (- index 1)))))

(define-fun ExactHeapSort
  ((q ExactState) (b Boundary) (start Int) (end Int)) ExactState
  (let ((length (- end start)))
    (ExactHeapSortLoop
      q b start length (- (+ length (div length 2)) 1))))

; fixed sort4/sort8 and bidirectional merge
(declare-datatypes ((ExactArrayResult 0))
  (((mkExactArrayResult
      (ear_state ExactState)
      (ear_output (Array Int Int))))))

(define-fun ExactSort4
  ((q ExactState) (b Boundary) (start Int)) ExactState
  (let ((v0 (select (e_sequence q) start))
        (v1 (select (e_sequence q) (+ start 1)))
        (v2 (select (e_sequence q) (+ start 2)))
        (v3 (select (e_sequence q) (+ start 3))))
    (let ((first (ExactCallback q b v1 v0))
          (c1
            (TargetAdapterIsLess b (e_callback_state q) v1 v0)))
      (ite
        (e_panicked first)
        first
        (let ((second (ExactCallback first b v3 v2))
              (c2
                (TargetAdapterIsLess
                  b (e_callback_state first) v3 v2)))
          (ite
            (e_panicked second)
            second
            (let ((a (ite c1 (+ start 1) start))
                  (sample_b (ite c1 start (+ start 1)))
                  (c (ite c2 (+ start 3) (+ start 2)))
                  (d (ite c2 (+ start 2) (+ start 3))))
              (let ((third
                      (ExactCallback
                        second
                        b
                        (select (e_sequence q) c)
                        (select (e_sequence q) a)))
                    (c3
                      (TargetAdapterIsLess
                        b
                        (e_callback_state second)
                        (select (e_sequence q) c)
                        (select (e_sequence q) a))))
                (ite
                  (e_panicked third)
                  third
                  (let ((fourth
                          (ExactCallback
                            third
                            b
                            (select (e_sequence q) d)
                            (select (e_sequence q) sample_b)))
                        (c4
                          (TargetAdapterIsLess
                            b
                            (e_callback_state third)
                            (select (e_sequence q) d)
                            (select (e_sequence q) sample_b))))
                    (ite
                      (e_panicked fourth)
                      fourth
                      (let ((minimum (ite c3 c a))
                            (maximum (ite c4 sample_b d))
                            (unknown_left
                              (ite c3 a (ite c4 c sample_b)))
                            (unknown_right
                              (ite c4 d (ite c3 sample_b c))))
                        (let ((fifth
                                (ExactCallback
                                  fourth
                                  b
                                  (select
                                    (e_sequence q)
                                    unknown_right)
                                  (select
                                    (e_sequence q)
                                    unknown_left)))
                              (c5
                                (TargetAdapterIsLess
                                  b
                                  (e_callback_state fourth)
                                  (select
                                    (e_sequence q)
                                    unknown_right)
                                  (select
                                    (e_sequence q)
                                    unknown_left))))
                          (ite
                            (e_panicked fifth)
                            fifth
                            (mkExactState
                              (store
                                (store
                                  (store
                                    (store
                                      (e_sequence q)
                                      start
                                      (select
                                        (e_sequence q)
                                        minimum))
                                    (+ start 1)
                                    (select
                                      (e_sequence q)
                                      (ite c5
                                        unknown_right
                                        unknown_left)))
                                  (+ start 2)
                                  (select
                                    (e_sequence q)
                                    (ite c5
                                      unknown_left
                                      unknown_right)))
                                (+ start 3)
                                (select
                                  (e_sequence q)
                                  maximum))
                              (e_callback_state fifth)
                              false)))))))))))))))

(define-fun-rec ExactMergeLoop
  ((q ExactState)
   (b Boundary)
   (output (Array Int Int))
   (start Int)
   (length Int)
   (split Int)
   (iteration Int)
   (left Int)
   (right Int)
   (left_back Int)
   (right_back Int)
   (front Int)
   (back Int)) ExactArrayResult
  (ite
    (or (e_panicked q) (>= iteration split))
    (ite
      (and
        (not (e_panicked q))
        (= (mod length 2) 1))
      (mkExactArrayResult
        q
        (store
          output
          front
          (select
            (e_sequence q)
            (ite (< left (+ left_back 1)) left right))))
      (mkExactArrayResult q output))
    (let ((up_left (select (e_sequence q) left))
          (up_right (select (e_sequence q) right)))
      (let ((called_up (ExactCallback q b up_right up_left))
            (take_left
              (not
                (TargetAdapterIsLess
                  b
                  (e_callback_state q)
                  up_right
                  up_left))))
        (ite
          (e_panicked called_up)
          (mkExactArrayResult called_up output)
          (let ((output_up
                  (store
                    output
                    front
                    (ite take_left up_left up_right)))
                (down_left
                  (select (e_sequence q) left_back))
                (down_right
                  (select (e_sequence q) right_back)))
            (let ((called_down
                    (ExactCallback
                      called_up b down_right down_left))
                  (take_right
                    (not
                      (TargetAdapterIsLess
                        b
                        (e_callback_state called_up)
                        down_right
                        down_left))))
              (ite
                (e_panicked called_down)
                (mkExactArrayResult called_down output_up)
                (ExactMergeLoop
                  called_down
                  b
                  (store
                    output_up
                    back
                    (ite take_right down_right down_left))
                  start
                  length
                  split
                  (+ iteration 1)
                  (ite take_left (+ left 1) left)
                  (ite take_left right (+ right 1))
                  (ite take_right left_back (- left_back 1))
                  (ite take_right (- right_back 1) right_back)
                  (+ front 1)
                  (- back 1))))))))))

(define-fun ExactMerge
  ((q ExactState)
   (b Boundary)
   (start Int)
   (length Int)
   (split Int)) ExactArrayResult
  (ExactMergeLoop
    q
    b
    (e_sequence q)
    start
    length
    split
    0
    start
    (+ start split)
    (- (+ start split) 1)
    (- (+ start length) 1)
    start
    (- (+ start length) 1)))

(define-fun ExactSort8
  ((q ExactState) (b Boundary) (start Int)) ExactState
  (let ((left (ExactSort4 q b start)))
    (ite
      (e_panicked left)
      left
      (let ((right (ExactSort4 left b (+ start 4))))
        (ite
          (e_panicked right)
          right
          (let ((merged (ExactMerge right b start 8 4)))
            (ite
              (e_panicked (ear_state merged))
              (ear_state merged)
              (mkExactState
                (ear_output merged)
                (e_callback_state (ear_state merged))
                false))))))))

; fixed sorting-network prefixes
(define-fun ExactNetworkFirst ((network Int) (index Int)) Int
  (ite (= network 13) (ite (= index 0) 0 (ite (= index 1) 1 (ite (= index 2) 2 (ite (= index 3) 3 (ite (= index 4) 5 (ite (= index 5) 6 (ite (= index 6) 1 (ite (= index 7) 2 (ite (= index 8) 4 (ite (= index 9) 7 (ite (= index 10) 8 (ite (= index 11) 0 (ite (= index 12) 1 (ite (= index 13) 3 (ite (= index 14) 7 (ite (= index 15) 9 (ite (= index 16) 11 (ite (= index 17) 4 (ite (= index 18) 5 (ite (= index 19) 8 (ite (= index 20) 10 (ite (= index 21) 0 (ite (= index 22) 3 (ite (= index 23) 4 (ite (= index 24) 6 (ite (= index 25) 9 (ite (= index 26) 0 (ite (= index 27) 2 (ite (= index 28) 6 (ite (= index 29) 7 (ite (= index 30) 10 (ite (= index 31) 1 (ite (= index 32) 2 (ite (= index 33) 5 (ite (= index 34) 9 (ite (= index 35) 1 (ite (= index 36) 3 (ite (= index 37) 5 (ite (= index 38) 6 (ite (= index 39) 2 (ite (= index 40) 4 (ite (= index 41) 6 (ite (= index 42) 8 (ite (= index 43) 3 (ite (= index 44) 5 0))))))))))))))))))))))))))))))))))))))))))))) (ite (= index 0) 0 (ite (= index 1) 1 (ite (= index 2) 2 (ite (= index 3) 4 (ite (= index 4) 0 (ite (= index 5) 2 (ite (= index 6) 3 (ite (= index 7) 5 (ite (= index 8) 0 (ite (= index 9) 1 (ite (= index 10) 4 (ite (= index 11) 7 (ite (= index 12) 1 (ite (= index 13) 3 (ite (= index 14) 5 (ite (= index 15) 0 (ite (= index 16) 2 (ite (= index 17) 3 (ite (= index 18) 6 (ite (= index 19) 2 (ite (= index 20) 4 (ite (= index 21) 6 (ite (= index 22) 1 (ite (= index 23) 3 (ite (= index 24) 5 0)))))))))))))))))))))))))))
(define-fun ExactNetworkSecond ((network Int) (index Int)) Int
  (ite (= network 13) (ite (= index 0) 12 (ite (= index 1) 10 (ite (= index 2) 9 (ite (= index 3) 7 (ite (= index 4) 11 (ite (= index 5) 8 (ite (= index 6) 6 (ite (= index 7) 3 (ite (= index 8) 11 (ite (= index 9) 9 (ite (= index 10) 10 (ite (= index 11) 4 (ite (= index 12) 2 (ite (= index 13) 6 (ite (= index 14) 8 (ite (= index 15) 10 (ite (= index 16) 12 (ite (= index 17) 6 (ite (= index 18) 9 (ite (= index 19) 11 (ite (= index 20) 12 (ite (= index 21) 5 (ite (= index 22) 8 (ite (= index 23) 7 (ite (= index 24) 11 (ite (= index 25) 10 (ite (= index 26) 1 (ite (= index 27) 5 (ite (= index 28) 9 (ite (= index 29) 8 (ite (= index 30) 11 (ite (= index 31) 3 (ite (= index 32) 4 (ite (= index 33) 6 (ite (= index 34) 10 (ite (= index 35) 2 (ite (= index 36) 4 (ite (= index 37) 7 (ite (= index 38) 8 (ite (= index 39) 3 (ite (= index 40) 5 (ite (= index 41) 7 (ite (= index 42) 9 (ite (= index 43) 4 (ite (= index 44) 6 0))))))))))))))))))))))))))))))))))))))))))))) (ite (= index 0) 3 (ite (= index 1) 7 (ite (= index 2) 5 (ite (= index 3) 8 (ite (= index 4) 7 (ite (= index 5) 4 (ite (= index 6) 8 (ite (= index 7) 6 (ite (= index 8) 2 (ite (= index 9) 3 (ite (= index 10) 5 (ite (= index 11) 8 (ite (= index 12) 4 (ite (= index 13) 6 (ite (= index 14) 7 (ite (= index 15) 1 (ite (= index 16) 4 (ite (= index 17) 5 (ite (= index 18) 8 (ite (= index 19) 3 (ite (= index 20) 5 (ite (= index 21) 7 (ite (= index 22) 2 (ite (= index 23) 4 (ite (= index 24) 6 0)))))))))))))))))))))))))))
(define-fun ExactNetworkCount ((network Int)) Int
  (ite (= network 13) 45
    (ite (= network 9) 25 0)))

(define-fun-rec ExactNetworkLoop
  ((q ExactState)
   (b Boundary)
   (start Int)
   (network Int)
   (index Int)) ExactState
  (ite
    (or
      (e_panicked q)
      (>= index (ExactNetworkCount network)))
    q
    (let ((first (+ start (ExactNetworkFirst network index)))
          (second (+ start (ExactNetworkSecond network index))))
      (let ((left (select (e_sequence q) first))
            (right (select (e_sequence q) second)))
        (let ((called (ExactCallback q b right left))
              (should_swap
                (TargetAdapterIsLess
                  b (e_callback_state q) right left)))
          (ite
            (e_panicked called)
            called
            (ExactNetworkLoop
              (ite should_swap
                (ExactSwap called first second)
                called)
              b
              start
              network
              (+ index 1))))))))

(define-fun ExactNetworkRegion
  ((q ExactState) (b Boundary) (start Int) (end Int)) ExactState
  (let ((length (- end start)))
    (let ((network
            (ite (>= length 13) 13
              (ite (>= length 9) 9 0))))
      (let ((networked (ExactNetworkLoop q b start network 0)))
        (ite
          (e_panicked networked)
          networked
          (ExactInsertionSortLoop
            networked
            b
            start
            end
            (+ start (ite (= network 0) 1 network))))))))

(define-fun ExactSmallNetwork
  ((q ExactState) (b Boundary) (start Int) (end Int)) ExactState
  (let ((length (- end start)))
    (ite
      (< length 2)
      q
      (ite
        (< length 18)
        (ExactNetworkRegion q b start end)
        (let ((half (div length 2)))
          (let ((left
                  (ExactNetworkRegion q b start (+ start half))))
            (ite
              (e_panicked left)
              left
              (let ((right
                      (ExactNetworkRegion
                        left b (+ start half) end)))
                (ite
                  (e_panicked right)
                  right
                  (let ((merged
                          (ExactMerge right b start length half)))
                    (ite
                      (e_panicked (ear_state merged))
                      (ear_state merged)
                      (mkExactState
                        (ear_output merged)
                        (e_callback_state (ear_state merged))
                        false))))))))))))

; scratch small sort. Scratch operations thread callback state but only copy
; back to the source sequence after both halves are initialized.
(define-fun ExactSmallGeneral
  ((q ExactState)
   (b Boundary)
   (c SortConfiguration)
   (start Int)
   (end Int)) ExactState
  (let ((length (- end start))
        (half (div (- end start) 2)))
    (ite
      (< length 2)
      q
      (let ((scratch
              (mkExactState
                (e_sequence q)
                (e_callback_state q)
                false)))
        (let ((presorted
                (ite
                  (and (<= (sc_element_size c) 16) (>= length 16))
                  8
                  (ite (>= length 8) 4 1)))
              (left_fixed
                (ite
                  (and (<= (sc_element_size c) 16) (>= length 16))
                  (ExactSort8 scratch b start)
                  (ite
                    (>= length 8)
                    (ExactSort4 scratch b start)
                    scratch))))
          (ite
            (e_panicked left_fixed)
            (mkExactState
              (e_sequence q)
              (e_callback_state left_fixed)
              true)
            (let ((right_fixed
                    (ite
                      (= presorted 8)
                      (ExactSort8 left_fixed b (+ start half))
                      (ite
                        (= presorted 4)
                        (ExactSort4 left_fixed b (+ start half))
                        left_fixed))))
              (ite
                (e_panicked right_fixed)
                (mkExactState
                  (e_sequence q)
                  (e_callback_state right_fixed)
                  true)
                (let ((left_sorted
                        (ExactInsertionSortLoop
                          right_fixed
                          b
                          start
                          (+ start half)
                          (+ start presorted))))
                  (ite
                    (e_panicked left_sorted)
                    (mkExactState
                      (e_sequence q)
                      (e_callback_state left_sorted)
                      true)
                    (let ((right_sorted
                            (ExactInsertionSortLoop
                              left_sorted
                              b
                              (+ start half)
                              end
                              (+ start half presorted))))
                      (ite
                        (e_panicked right_sorted)
                        (mkExactState
                          (e_sequence q)
                          (e_callback_state right_sorted)
                          true)
                        (let ((merged
                                (ExactMerge
                                  right_sorted
                                  b
                                  start
                                  length
                                  half)))
                          (ite
                            (e_panicked (ear_state merged))
                            (mkExactState
                              (e_sequence right_sorted)
                              (e_callback_state (ear_state merged))
                              true)
                            (mkExactState
                              (ear_output merged)
                              (e_callback_state (ear_state merged))
                              false)))))))))))))))

; 0=fallback insertion, 1=general scratch, 2=network.
(define-fun ExactSmallSortKind ((c SortConfiguration)) Int
  (let ((general_fits
          (<= (* (sc_element_size c) 48) 4096))
        (network_fits
          (and
            (<= (sc_element_size c) 8)
            (<= (* (sc_element_size c) 32) 4096))))
    (ite
      (not (sc_is_freeze c))
      0
      (ite
        (not (sc_is_copy c))
        (ite general_fits 1 0)
        (ite network_fits 2 (ite general_fits 1 0))))))

(define-fun ExactSmallSortThreshold ((c SortConfiguration)) Int
  (ite (= (ExactSmallSortKind c) 0) 16 32))

(define-fun ExactSmallSort
  ((q ExactState)
   (b Boundary)
   (c SortConfiguration)
   (start Int)
   (end Int)) ExactState
  (let ((kind (ExactSmallSortKind c)))
    (ite
      (= kind 0)
      (ite
        (>= (- end start) 2)
        (ExactInsertionSortLoop q b start end (+ start 1))
        q)
      (ite
        (= kind 1)
        (ExactSmallNetwork q b start end)
        (ExactSmallNetwork q b start end)))))

; recursive-left / iterative-right quicksort
(define-funs-rec
  ((ExactQuickSort
      ((q ExactState)
       (b Boundary)
       (c SortConfiguration)
       (start Int)
       (end Int)
       (ancestor_present Bool)
       (ancestor Int)
       (limit Int))
      ExactState)
   (ExactQuickSortPartition
      ((q ExactState)
       (b Boundary)
       (c SortConfiguration)
       (start Int)
       (end Int)
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
        (<= length (ExactSmallSortThreshold c))
        (ExactSmallSort q b c start end)
        (ite
          (ExactLimitExhausted limit)
          (ExactHeapSort q b start end)
          (let ((next_limit (- limit 1))
                (chosen (ExactChoosePivot q b start end)))
            (ite
              (e_panicked (eir_state chosen))
              (eir_state chosen)
              (ite
                ancestor_present
                (let ((pivot
                        (select
                          (e_sequence (eir_state chosen))
                          (+ start (eir_value chosen)))))
                  (let ((compared
                          (ExactCallback
                            (eir_state chosen) b ancestor pivot))
                        (ancestor_less
                          (TargetAdapterIsLess
                            b
                            (e_callback_state (eir_state chosen))
                            ancestor
                            pivot)))
                    (ite
                      (e_panicked compared)
                      compared
                      (ite
                        (not ancestor_less)
                        (let ((equal
                                (ExactPartition
                                  compared
                                  b
                                  (mkConfiguration
                                    (sc_optimize_for_size c)
                                    (sc_element_size c))
                                  start
                                  end
                                  (eir_value chosen)
                                  true)))
                          (ite
                            (e_panicked (eir_state equal))
                            (eir_state equal)
                            (ExactQuickSort
                              (eir_state equal)
                              b
                              c
                              (+ start (eir_value equal) 1)
                              end
                              false
                              0
                              next_limit)))
                        (ExactQuickSortPartition
                          compared
                          b
                          c
                          start
                          end
                          true
                          ancestor
                          next_limit
                          (eir_value chosen))))))
                (ExactQuickSortPartition
                  (eir_state chosen)
                  b
                  c
                  start
                  end
                  false
                  0
                  next_limit
                  (eir_value chosen)))))))))
   (let ((partitioned
          (ExactPartition
            q
            b
            (mkConfiguration
              (sc_optimize_for_size c)
              (sc_element_size c))
            start
            end
            pivot_position
            false)))
    (ite
      (e_panicked (eir_state partitioned))
      (eir_state partitioned)
      (let ((pivot_index (+ start (eir_value partitioned))))
        (let ((pivot
                (select
                  (e_sequence (eir_state partitioned))
                  pivot_index))
              (left
                (ExactQuickSort
                  (eir_state partitioned)
                  b
                  c
                  start
                  pivot_index
                  ancestor_present
                  ancestor
                  limit)))
          (ite
            (e_panicked left)
            left
            (ExactQuickSort
              left
              b
              c
              (+ pivot_index 1)
              end
              true
              pivot
              limit))))))))

(define-fun-rec ExactILog2 ((value Int)) Int
  (ite (< value 2) 0 (+ 1 (ExactILog2 (div value 2)))))

(define-fun ExactSort
  ((q ExactState)
   (b Boundary)
   (c SortConfiguration)
   (length Int)) ExactState
  (ite
    (or (= (sc_element_size c) 0) (< length 2))
    q
    (ite
      (or
        (sc_optimize_for_size c)
        (= (sc_target_pointer_width c) 16))
      (ExactHeapSort q b 0 length)
      (ite
        (<= length 20)
        (ExactInsertionSortLoop q b 0 length 1)
        (let ((run (ExactFindExistingRun q b length)))
          (ite
            (e_panicked (err_state run))
            (err_state run)
            (ite
              (= (err_length run) length)
              (ite
                (err_descending run)
                (ExactReverseLoop
                  (err_state run) 0 (- length 1))
                (err_state run))
              (ExactQuickSort
                (err_state run)
                b
                c
                0
                length
                false
                0
                (* 2
                  (ExactILog2
                    (ite
                      (= (mod length 2) 0)
                      (+ length 1)
                      length)))))))))))

; formal source input case=forcing-small-sort-selection
(define-fun boundary_0 () Boundary
  (mkBoundary
    80
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration_0 () SortConfiguration
  (mkSortConfiguration
    false
    64
    24
    true
    true))
(define-fun source_initial_0 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 1) 1 4) 2 5) 3 6) 4 2) 5 0) 6 3) 7 8) 8 7) (b_initial_state boundary_0) false))
(assert (BoundaryWellFormed boundary_0))
(define-fun formal_state_0 () ExactState (ExactSmallSort source_initial_0 boundary_0 configuration_0 0 9))
(define-fun formal_result_0 () Result
  (mkResult
    (e_sequence formal_state_0)
    (e_callback_state formal_state_0)
    (e_panicked formal_state_0)
    false
    true
    (ite (e_panicked formal_state_0) 1 0)
    (not (e_panicked formal_state_0))
    -1))
(define-fun reference_result_0 () Result (mkResult (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 20 false false true 0 true -1))
; independently derived semantic source mutation: small-sort-selection
(assert (not (= formal_result_0 (mkResult (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 20 false false true 0 true -1))))
(check-sat-using (then ctx-solver-simplify smt))
