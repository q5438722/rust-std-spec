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
        (ExactSmallGeneral q b c start end)
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

; formal source input case=duplicate-class-ancestor-pivot
(define-fun boundary_0 () Boundary
  (mkBoundary
    80
    0
    (lambda ((key PairKey)) (ite (or (< (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4) (= (pair_left_identity key) 5) (= (pair_left_identity key) 6) (= (pair_left_identity key) 7) (= (pair_left_identity key) 8) (= (pair_left_identity key) 9) (= (pair_left_identity key) 10) (= (pair_left_identity key) 11) (= (pair_left_identity key) 12) (= (pair_left_identity key) 13) (= (pair_left_identity key) 14) (= (pair_left_identity key) 15) (= (pair_left_identity key) 16) (= (pair_left_identity key) 17) (= (pair_left_identity key) 18) (= (pair_left_identity key) 19) (= (pair_left_identity key) 20) (= (pair_left_identity key) 21) (= (pair_left_identity key) 22) (= (pair_left_identity key) 23) (= (pair_left_identity key) 24) (= (pair_left_identity key) 25) (= (pair_left_identity key) 26) (= (pair_left_identity key) 27) (= (pair_left_identity key) 28) (= (pair_left_identity key) 29) (= (pair_left_identity key) 30) (= (pair_left_identity key) 31) (= (pair_left_identity key) 32) (= (pair_left_identity key) 33) (= (pair_left_identity key) 34) (= (pair_left_identity key) 35) (= (pair_left_identity key) 36) (= (pair_left_identity key) 37) (= (pair_left_identity key) 38) (= (pair_left_identity key) 39) (= (pair_left_identity key) 40) (= (pair_left_identity key) 41) (= (pair_left_identity key) 42) (= (pair_left_identity key) 43) (= (pair_left_identity key) 44) (= (pair_left_identity key) 45) (= (pair_left_identity key) 46) (= (pair_left_identity key) 47) (= (pair_left_identity key) 48) (= (pair_left_identity key) 49) (= (pair_left_identity key) 50) (= (pair_left_identity key) 51) (= (pair_left_identity key) 52) (= (pair_left_identity key) 53) (= (pair_left_identity key) 54) (= (pair_left_identity key) 55) (= (pair_left_identity key) 56) (= (pair_left_identity key) 57) (= (pair_left_identity key) 58) (= (pair_left_identity key) 59) (= (pair_left_identity key) 60) (= (pair_left_identity key) 61) (= (pair_left_identity key) 62) (= (pair_left_identity key) 63) (= (pair_left_identity key) 64) (= (pair_left_identity key) 65) (= (pair_left_identity key) 66) (= (pair_left_identity key) 67) (= (pair_left_identity key) 68) (= (pair_left_identity key) 69) (= (pair_left_identity key) 70) (= (pair_left_identity key) 71) (= (pair_left_identity key) 72) (= (pair_left_identity key) 73) (= (pair_left_identity key) 74) (= (pair_left_identity key) 75) (= (pair_left_identity key) 76) (= (pair_left_identity key) 77) (= (pair_left_identity key) 78) (= (pair_left_identity key) 79)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4) (= (pair_right_identity key) 5) (= (pair_right_identity key) 6) (= (pair_right_identity key) 7) (= (pair_right_identity key) 8) (= (pair_right_identity key) 9) (= (pair_right_identity key) 10) (= (pair_right_identity key) 11) (= (pair_right_identity key) 12) (= (pair_right_identity key) 13) (= (pair_right_identity key) 14) (= (pair_right_identity key) 15) (= (pair_right_identity key) 16) (= (pair_right_identity key) 17) (= (pair_right_identity key) 18) (= (pair_right_identity key) 19) (= (pair_right_identity key) 20) (= (pair_right_identity key) 21) (= (pair_right_identity key) 22) (= (pair_right_identity key) 23) (= (pair_right_identity key) 24) (= (pair_right_identity key) 25) (= (pair_right_identity key) 26) (= (pair_right_identity key) 27) (= (pair_right_identity key) 28) (= (pair_right_identity key) 29) (= (pair_right_identity key) 30) (= (pair_right_identity key) 31) (= (pair_right_identity key) 32) (= (pair_right_identity key) 33) (= (pair_right_identity key) 34) (= (pair_right_identity key) 35) (= (pair_right_identity key) 36) (= (pair_right_identity key) 37) (= (pair_right_identity key) 38) (= (pair_right_identity key) 39) (= (pair_right_identity key) 40) (= (pair_right_identity key) 41) (= (pair_right_identity key) 42) (= (pair_right_identity key) 43) (= (pair_right_identity key) 44) (= (pair_right_identity key) 45) (= (pair_right_identity key) 46) (= (pair_right_identity key) 47) (= (pair_right_identity key) 48) (= (pair_right_identity key) 49) (= (pair_right_identity key) 50) (= (pair_right_identity key) 51) (= (pair_right_identity key) 52) (= (pair_right_identity key) 53) (= (pair_right_identity key) 54) (= (pair_right_identity key) 55) (= (pair_right_identity key) 56) (= (pair_right_identity key) 57) (= (pair_right_identity key) 58) (= (pair_right_identity key) 59) (= (pair_right_identity key) 60) (= (pair_right_identity key) 61) (= (pair_right_identity key) 62) (= (pair_right_identity key) 63) (= (pair_right_identity key) 64) (= (pair_right_identity key) 65) (= (pair_right_identity key) 66) (= (pair_right_identity key) 67) (= (pair_right_identity key) 68) (= (pair_right_identity key) 69) (= (pair_right_identity key) 70) (= (pair_right_identity key) 71) (= (pair_right_identity key) 72) (= (pair_right_identity key) 73) (= (pair_right_identity key) 74) (= (pair_right_identity key) 75) (= (pair_right_identity key) 76) (= (pair_right_identity key) 77) (= (pair_right_identity key) 78) (= (pair_right_identity key) 79)) 0 1)) (and (= (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4) (= (pair_left_identity key) 5) (= (pair_left_identity key) 6) (= (pair_left_identity key) 7) (= (pair_left_identity key) 8) (= (pair_left_identity key) 9) (= (pair_left_identity key) 10) (= (pair_left_identity key) 11) (= (pair_left_identity key) 12) (= (pair_left_identity key) 13) (= (pair_left_identity key) 14) (= (pair_left_identity key) 15) (= (pair_left_identity key) 16) (= (pair_left_identity key) 17) (= (pair_left_identity key) 18) (= (pair_left_identity key) 19) (= (pair_left_identity key) 20) (= (pair_left_identity key) 21) (= (pair_left_identity key) 22) (= (pair_left_identity key) 23) (= (pair_left_identity key) 24) (= (pair_left_identity key) 25) (= (pair_left_identity key) 26) (= (pair_left_identity key) 27) (= (pair_left_identity key) 28) (= (pair_left_identity key) 29) (= (pair_left_identity key) 30) (= (pair_left_identity key) 31) (= (pair_left_identity key) 32) (= (pair_left_identity key) 33) (= (pair_left_identity key) 34) (= (pair_left_identity key) 35) (= (pair_left_identity key) 36) (= (pair_left_identity key) 37) (= (pair_left_identity key) 38) (= (pair_left_identity key) 39) (= (pair_left_identity key) 40) (= (pair_left_identity key) 41) (= (pair_left_identity key) 42) (= (pair_left_identity key) 43) (= (pair_left_identity key) 44) (= (pair_left_identity key) 45) (= (pair_left_identity key) 46) (= (pair_left_identity key) 47) (= (pair_left_identity key) 48) (= (pair_left_identity key) 49) (= (pair_left_identity key) 50) (= (pair_left_identity key) 51) (= (pair_left_identity key) 52) (= (pair_left_identity key) 53) (= (pair_left_identity key) 54) (= (pair_left_identity key) 55) (= (pair_left_identity key) 56) (= (pair_left_identity key) 57) (= (pair_left_identity key) 58) (= (pair_left_identity key) 59) (= (pair_left_identity key) 60) (= (pair_left_identity key) 61) (= (pair_left_identity key) 62) (= (pair_left_identity key) 63) (= (pair_left_identity key) 64) (= (pair_left_identity key) 65) (= (pair_left_identity key) 66) (= (pair_left_identity key) 67) (= (pair_left_identity key) 68) (= (pair_left_identity key) 69) (= (pair_left_identity key) 70) (= (pair_left_identity key) 71) (= (pair_left_identity key) 72) (= (pair_left_identity key) 73) (= (pair_left_identity key) 74) (= (pair_left_identity key) 75) (= (pair_left_identity key) 76) (= (pair_left_identity key) 77) (= (pair_left_identity key) 78) (= (pair_left_identity key) 79)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4) (= (pair_right_identity key) 5) (= (pair_right_identity key) 6) (= (pair_right_identity key) 7) (= (pair_right_identity key) 8) (= (pair_right_identity key) 9) (= (pair_right_identity key) 10) (= (pair_right_identity key) 11) (= (pair_right_identity key) 12) (= (pair_right_identity key) 13) (= (pair_right_identity key) 14) (= (pair_right_identity key) 15) (= (pair_right_identity key) 16) (= (pair_right_identity key) 17) (= (pair_right_identity key) 18) (= (pair_right_identity key) 19) (= (pair_right_identity key) 20) (= (pair_right_identity key) 21) (= (pair_right_identity key) 22) (= (pair_right_identity key) 23) (= (pair_right_identity key) 24) (= (pair_right_identity key) 25) (= (pair_right_identity key) 26) (= (pair_right_identity key) 27) (= (pair_right_identity key) 28) (= (pair_right_identity key) 29) (= (pair_right_identity key) 30) (= (pair_right_identity key) 31) (= (pair_right_identity key) 32) (= (pair_right_identity key) 33) (= (pair_right_identity key) 34) (= (pair_right_identity key) 35) (= (pair_right_identity key) 36) (= (pair_right_identity key) 37) (= (pair_right_identity key) 38) (= (pair_right_identity key) 39) (= (pair_right_identity key) 40) (= (pair_right_identity key) 41) (= (pair_right_identity key) 42) (= (pair_right_identity key) 43) (= (pair_right_identity key) 44) (= (pair_right_identity key) 45) (= (pair_right_identity key) 46) (= (pair_right_identity key) 47) (= (pair_right_identity key) 48) (= (pair_right_identity key) 49) (= (pair_right_identity key) 50) (= (pair_right_identity key) 51) (= (pair_right_identity key) 52) (= (pair_right_identity key) 53) (= (pair_right_identity key) 54) (= (pair_right_identity key) 55) (= (pair_right_identity key) 56) (= (pair_right_identity key) 57) (= (pair_right_identity key) 58) (= (pair_right_identity key) 59) (= (pair_right_identity key) 60) (= (pair_right_identity key) 61) (= (pair_right_identity key) 62) (= (pair_right_identity key) 63) (= (pair_right_identity key) 64) (= (pair_right_identity key) 65) (= (pair_right_identity key) 66) (= (pair_right_identity key) 67) (= (pair_right_identity key) 68) (= (pair_right_identity key) 69) (= (pair_right_identity key) 70) (= (pair_right_identity key) 71) (= (pair_right_identity key) 72) (= (pair_right_identity key) 73) (= (pair_right_identity key) 74) (= (pair_right_identity key) 75) (= (pair_right_identity key) 76) (= (pair_right_identity key) 77) (= (pair_right_identity key) 78) (= (pair_right_identity key) 79)) 0 1)) (< (ite (= (pair_left_identity key) 0) 0 (ite (= (pair_left_identity key) 1) 1 (ite (= (pair_left_identity key) 2) 2 (ite (= (pair_left_identity key) 3) 3 (ite (= (pair_left_identity key) 4) 4 (ite (= (pair_left_identity key) 5) 5 (ite (= (pair_left_identity key) 6) 0 (ite (= (pair_left_identity key) 7) 1 (ite (= (pair_left_identity key) 8) 2 (ite (= (pair_left_identity key) 9) 3 (ite (= (pair_left_identity key) 10) 4 (ite (= (pair_left_identity key) 11) 5 (ite (= (pair_left_identity key) 12) 0 (ite (= (pair_left_identity key) 13) 1 (ite (= (pair_left_identity key) 14) 2 (ite (= (pair_left_identity key) 15) 3 (ite (= (pair_left_identity key) 16) 4 (ite (= (pair_left_identity key) 17) 5 (ite (= (pair_left_identity key) 18) 0 (ite (= (pair_left_identity key) 19) 1 (ite (= (pair_left_identity key) 20) 2 (ite (= (pair_left_identity key) 21) 3 (ite (= (pair_left_identity key) 22) 4 (ite (= (pair_left_identity key) 23) 5 (ite (= (pair_left_identity key) 24) 0 (ite (= (pair_left_identity key) 25) 1 (ite (= (pair_left_identity key) 26) 2 (ite (= (pair_left_identity key) 27) 3 (ite (= (pair_left_identity key) 28) 4 (ite (= (pair_left_identity key) 29) 5 (ite (= (pair_left_identity key) 30) 0 (ite (= (pair_left_identity key) 31) 1 (ite (= (pair_left_identity key) 32) 2 (ite (= (pair_left_identity key) 33) 3 (ite (= (pair_left_identity key) 34) 4 (ite (= (pair_left_identity key) 35) 5 (ite (= (pair_left_identity key) 36) 0 (ite (= (pair_left_identity key) 37) 1 (ite (= (pair_left_identity key) 38) 2 (ite (= (pair_left_identity key) 39) 3 (ite (= (pair_left_identity key) 40) 4 (ite (= (pair_left_identity key) 41) 5 (ite (= (pair_left_identity key) 42) 0 (ite (= (pair_left_identity key) 43) 1 (ite (= (pair_left_identity key) 44) 2 (ite (= (pair_left_identity key) 45) 3 (ite (= (pair_left_identity key) 46) 4 (ite (= (pair_left_identity key) 47) 5 (ite (= (pair_left_identity key) 48) 0 (ite (= (pair_left_identity key) 49) 1 (ite (= (pair_left_identity key) 50) 2 (ite (= (pair_left_identity key) 51) 3 (ite (= (pair_left_identity key) 52) 4 (ite (= (pair_left_identity key) 53) 5 (ite (= (pair_left_identity key) 54) 0 (ite (= (pair_left_identity key) 55) 1 (ite (= (pair_left_identity key) 56) 2 (ite (= (pair_left_identity key) 57) 3 (ite (= (pair_left_identity key) 58) 4 (ite (= (pair_left_identity key) 59) 5 (ite (= (pair_left_identity key) 60) 0 (ite (= (pair_left_identity key) 61) 1 (ite (= (pair_left_identity key) 62) 2 (ite (= (pair_left_identity key) 63) 3 (ite (= (pair_left_identity key) 64) 4 (ite (= (pair_left_identity key) 65) 5 (ite (= (pair_left_identity key) 66) 0 (ite (= (pair_left_identity key) 67) 1 (ite (= (pair_left_identity key) 68) 2 (ite (= (pair_left_identity key) 69) 3 (ite (= (pair_left_identity key) 70) 4 (ite (= (pair_left_identity key) 71) 5 (ite (= (pair_left_identity key) 72) 0 (ite (= (pair_left_identity key) 73) 1 (ite (= (pair_left_identity key) 74) 2 (ite (= (pair_left_identity key) 75) 3 (ite (= (pair_left_identity key) 76) 4 (ite (= (pair_left_identity key) 77) 5 (ite (= (pair_left_identity key) 78) 0 (ite (= (pair_left_identity key) 79) 1 (pair_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (pair_right_identity key) 0) 0 (ite (= (pair_right_identity key) 1) 1 (ite (= (pair_right_identity key) 2) 2 (ite (= (pair_right_identity key) 3) 3 (ite (= (pair_right_identity key) 4) 4 (ite (= (pair_right_identity key) 5) 5 (ite (= (pair_right_identity key) 6) 0 (ite (= (pair_right_identity key) 7) 1 (ite (= (pair_right_identity key) 8) 2 (ite (= (pair_right_identity key) 9) 3 (ite (= (pair_right_identity key) 10) 4 (ite (= (pair_right_identity key) 11) 5 (ite (= (pair_right_identity key) 12) 0 (ite (= (pair_right_identity key) 13) 1 (ite (= (pair_right_identity key) 14) 2 (ite (= (pair_right_identity key) 15) 3 (ite (= (pair_right_identity key) 16) 4 (ite (= (pair_right_identity key) 17) 5 (ite (= (pair_right_identity key) 18) 0 (ite (= (pair_right_identity key) 19) 1 (ite (= (pair_right_identity key) 20) 2 (ite (= (pair_right_identity key) 21) 3 (ite (= (pair_right_identity key) 22) 4 (ite (= (pair_right_identity key) 23) 5 (ite (= (pair_right_identity key) 24) 0 (ite (= (pair_right_identity key) 25) 1 (ite (= (pair_right_identity key) 26) 2 (ite (= (pair_right_identity key) 27) 3 (ite (= (pair_right_identity key) 28) 4 (ite (= (pair_right_identity key) 29) 5 (ite (= (pair_right_identity key) 30) 0 (ite (= (pair_right_identity key) 31) 1 (ite (= (pair_right_identity key) 32) 2 (ite (= (pair_right_identity key) 33) 3 (ite (= (pair_right_identity key) 34) 4 (ite (= (pair_right_identity key) 35) 5 (ite (= (pair_right_identity key) 36) 0 (ite (= (pair_right_identity key) 37) 1 (ite (= (pair_right_identity key) 38) 2 (ite (= (pair_right_identity key) 39) 3 (ite (= (pair_right_identity key) 40) 4 (ite (= (pair_right_identity key) 41) 5 (ite (= (pair_right_identity key) 42) 0 (ite (= (pair_right_identity key) 43) 1 (ite (= (pair_right_identity key) 44) 2 (ite (= (pair_right_identity key) 45) 3 (ite (= (pair_right_identity key) 46) 4 (ite (= (pair_right_identity key) 47) 5 (ite (= (pair_right_identity key) 48) 0 (ite (= (pair_right_identity key) 49) 1 (ite (= (pair_right_identity key) 50) 2 (ite (= (pair_right_identity key) 51) 3 (ite (= (pair_right_identity key) 52) 4 (ite (= (pair_right_identity key) 53) 5 (ite (= (pair_right_identity key) 54) 0 (ite (= (pair_right_identity key) 55) 1 (ite (= (pair_right_identity key) 56) 2 (ite (= (pair_right_identity key) 57) 3 (ite (= (pair_right_identity key) 58) 4 (ite (= (pair_right_identity key) 59) 5 (ite (= (pair_right_identity key) 60) 0 (ite (= (pair_right_identity key) 61) 1 (ite (= (pair_right_identity key) 62) 2 (ite (= (pair_right_identity key) 63) 3 (ite (= (pair_right_identity key) 64) 4 (ite (= (pair_right_identity key) 65) 5 (ite (= (pair_right_identity key) 66) 0 (ite (= (pair_right_identity key) 67) 1 (ite (= (pair_right_identity key) 68) 2 (ite (= (pair_right_identity key) 69) 3 (ite (= (pair_right_identity key) 70) 4 (ite (= (pair_right_identity key) 71) 5 (ite (= (pair_right_identity key) 72) 0 (ite (= (pair_right_identity key) 73) 1 (ite (= (pair_right_identity key) 74) 2 (ite (= (pair_right_identity key) 75) 3 (ite (= (pair_right_identity key) 76) 4 (ite (= (pair_right_identity key) 77) 5 (ite (= (pair_right_identity key) 78) 0 (ite (= (pair_right_identity key) 79) 1 (pair_right_identity key)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) -1 (ite (and (= (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4) (= (pair_left_identity key) 5) (= (pair_left_identity key) 6) (= (pair_left_identity key) 7) (= (pair_left_identity key) 8) (= (pair_left_identity key) 9) (= (pair_left_identity key) 10) (= (pair_left_identity key) 11) (= (pair_left_identity key) 12) (= (pair_left_identity key) 13) (= (pair_left_identity key) 14) (= (pair_left_identity key) 15) (= (pair_left_identity key) 16) (= (pair_left_identity key) 17) (= (pair_left_identity key) 18) (= (pair_left_identity key) 19) (= (pair_left_identity key) 20) (= (pair_left_identity key) 21) (= (pair_left_identity key) 22) (= (pair_left_identity key) 23) (= (pair_left_identity key) 24) (= (pair_left_identity key) 25) (= (pair_left_identity key) 26) (= (pair_left_identity key) 27) (= (pair_left_identity key) 28) (= (pair_left_identity key) 29) (= (pair_left_identity key) 30) (= (pair_left_identity key) 31) (= (pair_left_identity key) 32) (= (pair_left_identity key) 33) (= (pair_left_identity key) 34) (= (pair_left_identity key) 35) (= (pair_left_identity key) 36) (= (pair_left_identity key) 37) (= (pair_left_identity key) 38) (= (pair_left_identity key) 39) (= (pair_left_identity key) 40) (= (pair_left_identity key) 41) (= (pair_left_identity key) 42) (= (pair_left_identity key) 43) (= (pair_left_identity key) 44) (= (pair_left_identity key) 45) (= (pair_left_identity key) 46) (= (pair_left_identity key) 47) (= (pair_left_identity key) 48) (= (pair_left_identity key) 49) (= (pair_left_identity key) 50) (= (pair_left_identity key) 51) (= (pair_left_identity key) 52) (= (pair_left_identity key) 53) (= (pair_left_identity key) 54) (= (pair_left_identity key) 55) (= (pair_left_identity key) 56) (= (pair_left_identity key) 57) (= (pair_left_identity key) 58) (= (pair_left_identity key) 59) (= (pair_left_identity key) 60) (= (pair_left_identity key) 61) (= (pair_left_identity key) 62) (= (pair_left_identity key) 63) (= (pair_left_identity key) 64) (= (pair_left_identity key) 65) (= (pair_left_identity key) 66) (= (pair_left_identity key) 67) (= (pair_left_identity key) 68) (= (pair_left_identity key) 69) (= (pair_left_identity key) 70) (= (pair_left_identity key) 71) (= (pair_left_identity key) 72) (= (pair_left_identity key) 73) (= (pair_left_identity key) 74) (= (pair_left_identity key) 75) (= (pair_left_identity key) 76) (= (pair_left_identity key) 77) (= (pair_left_identity key) 78) (= (pair_left_identity key) 79)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4) (= (pair_right_identity key) 5) (= (pair_right_identity key) 6) (= (pair_right_identity key) 7) (= (pair_right_identity key) 8) (= (pair_right_identity key) 9) (= (pair_right_identity key) 10) (= (pair_right_identity key) 11) (= (pair_right_identity key) 12) (= (pair_right_identity key) 13) (= (pair_right_identity key) 14) (= (pair_right_identity key) 15) (= (pair_right_identity key) 16) (= (pair_right_identity key) 17) (= (pair_right_identity key) 18) (= (pair_right_identity key) 19) (= (pair_right_identity key) 20) (= (pair_right_identity key) 21) (= (pair_right_identity key) 22) (= (pair_right_identity key) 23) (= (pair_right_identity key) 24) (= (pair_right_identity key) 25) (= (pair_right_identity key) 26) (= (pair_right_identity key) 27) (= (pair_right_identity key) 28) (= (pair_right_identity key) 29) (= (pair_right_identity key) 30) (= (pair_right_identity key) 31) (= (pair_right_identity key) 32) (= (pair_right_identity key) 33) (= (pair_right_identity key) 34) (= (pair_right_identity key) 35) (= (pair_right_identity key) 36) (= (pair_right_identity key) 37) (= (pair_right_identity key) 38) (= (pair_right_identity key) 39) (= (pair_right_identity key) 40) (= (pair_right_identity key) 41) (= (pair_right_identity key) 42) (= (pair_right_identity key) 43) (= (pair_right_identity key) 44) (= (pair_right_identity key) 45) (= (pair_right_identity key) 46) (= (pair_right_identity key) 47) (= (pair_right_identity key) 48) (= (pair_right_identity key) 49) (= (pair_right_identity key) 50) (= (pair_right_identity key) 51) (= (pair_right_identity key) 52) (= (pair_right_identity key) 53) (= (pair_right_identity key) 54) (= (pair_right_identity key) 55) (= (pair_right_identity key) 56) (= (pair_right_identity key) 57) (= (pair_right_identity key) 58) (= (pair_right_identity key) 59) (= (pair_right_identity key) 60) (= (pair_right_identity key) 61) (= (pair_right_identity key) 62) (= (pair_right_identity key) 63) (= (pair_right_identity key) 64) (= (pair_right_identity key) 65) (= (pair_right_identity key) 66) (= (pair_right_identity key) 67) (= (pair_right_identity key) 68) (= (pair_right_identity key) 69) (= (pair_right_identity key) 70) (= (pair_right_identity key) 71) (= (pair_right_identity key) 72) (= (pair_right_identity key) 73) (= (pair_right_identity key) 74) (= (pair_right_identity key) 75) (= (pair_right_identity key) 76) (= (pair_right_identity key) 77) (= (pair_right_identity key) 78) (= (pair_right_identity key) 79)) 0 1)) (= (ite (= (pair_left_identity key) 0) 0 (ite (= (pair_left_identity key) 1) 1 (ite (= (pair_left_identity key) 2) 2 (ite (= (pair_left_identity key) 3) 3 (ite (= (pair_left_identity key) 4) 4 (ite (= (pair_left_identity key) 5) 5 (ite (= (pair_left_identity key) 6) 0 (ite (= (pair_left_identity key) 7) 1 (ite (= (pair_left_identity key) 8) 2 (ite (= (pair_left_identity key) 9) 3 (ite (= (pair_left_identity key) 10) 4 (ite (= (pair_left_identity key) 11) 5 (ite (= (pair_left_identity key) 12) 0 (ite (= (pair_left_identity key) 13) 1 (ite (= (pair_left_identity key) 14) 2 (ite (= (pair_left_identity key) 15) 3 (ite (= (pair_left_identity key) 16) 4 (ite (= (pair_left_identity key) 17) 5 (ite (= (pair_left_identity key) 18) 0 (ite (= (pair_left_identity key) 19) 1 (ite (= (pair_left_identity key) 20) 2 (ite (= (pair_left_identity key) 21) 3 (ite (= (pair_left_identity key) 22) 4 (ite (= (pair_left_identity key) 23) 5 (ite (= (pair_left_identity key) 24) 0 (ite (= (pair_left_identity key) 25) 1 (ite (= (pair_left_identity key) 26) 2 (ite (= (pair_left_identity key) 27) 3 (ite (= (pair_left_identity key) 28) 4 (ite (= (pair_left_identity key) 29) 5 (ite (= (pair_left_identity key) 30) 0 (ite (= (pair_left_identity key) 31) 1 (ite (= (pair_left_identity key) 32) 2 (ite (= (pair_left_identity key) 33) 3 (ite (= (pair_left_identity key) 34) 4 (ite (= (pair_left_identity key) 35) 5 (ite (= (pair_left_identity key) 36) 0 (ite (= (pair_left_identity key) 37) 1 (ite (= (pair_left_identity key) 38) 2 (ite (= (pair_left_identity key) 39) 3 (ite (= (pair_left_identity key) 40) 4 (ite (= (pair_left_identity key) 41) 5 (ite (= (pair_left_identity key) 42) 0 (ite (= (pair_left_identity key) 43) 1 (ite (= (pair_left_identity key) 44) 2 (ite (= (pair_left_identity key) 45) 3 (ite (= (pair_left_identity key) 46) 4 (ite (= (pair_left_identity key) 47) 5 (ite (= (pair_left_identity key) 48) 0 (ite (= (pair_left_identity key) 49) 1 (ite (= (pair_left_identity key) 50) 2 (ite (= (pair_left_identity key) 51) 3 (ite (= (pair_left_identity key) 52) 4 (ite (= (pair_left_identity key) 53) 5 (ite (= (pair_left_identity key) 54) 0 (ite (= (pair_left_identity key) 55) 1 (ite (= (pair_left_identity key) 56) 2 (ite (= (pair_left_identity key) 57) 3 (ite (= (pair_left_identity key) 58) 4 (ite (= (pair_left_identity key) 59) 5 (ite (= (pair_left_identity key) 60) 0 (ite (= (pair_left_identity key) 61) 1 (ite (= (pair_left_identity key) 62) 2 (ite (= (pair_left_identity key) 63) 3 (ite (= (pair_left_identity key) 64) 4 (ite (= (pair_left_identity key) 65) 5 (ite (= (pair_left_identity key) 66) 0 (ite (= (pair_left_identity key) 67) 1 (ite (= (pair_left_identity key) 68) 2 (ite (= (pair_left_identity key) 69) 3 (ite (= (pair_left_identity key) 70) 4 (ite (= (pair_left_identity key) 71) 5 (ite (= (pair_left_identity key) 72) 0 (ite (= (pair_left_identity key) 73) 1 (ite (= (pair_left_identity key) 74) 2 (ite (= (pair_left_identity key) 75) 3 (ite (= (pair_left_identity key) 76) 4 (ite (= (pair_left_identity key) 77) 5 (ite (= (pair_left_identity key) 78) 0 (ite (= (pair_left_identity key) 79) 1 (pair_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (pair_right_identity key) 0) 0 (ite (= (pair_right_identity key) 1) 1 (ite (= (pair_right_identity key) 2) 2 (ite (= (pair_right_identity key) 3) 3 (ite (= (pair_right_identity key) 4) 4 (ite (= (pair_right_identity key) 5) 5 (ite (= (pair_right_identity key) 6) 0 (ite (= (pair_right_identity key) 7) 1 (ite (= (pair_right_identity key) 8) 2 (ite (= (pair_right_identity key) 9) 3 (ite (= (pair_right_identity key) 10) 4 (ite (= (pair_right_identity key) 11) 5 (ite (= (pair_right_identity key) 12) 0 (ite (= (pair_right_identity key) 13) 1 (ite (= (pair_right_identity key) 14) 2 (ite (= (pair_right_identity key) 15) 3 (ite (= (pair_right_identity key) 16) 4 (ite (= (pair_right_identity key) 17) 5 (ite (= (pair_right_identity key) 18) 0 (ite (= (pair_right_identity key) 19) 1 (ite (= (pair_right_identity key) 20) 2 (ite (= (pair_right_identity key) 21) 3 (ite (= (pair_right_identity key) 22) 4 (ite (= (pair_right_identity key) 23) 5 (ite (= (pair_right_identity key) 24) 0 (ite (= (pair_right_identity key) 25) 1 (ite (= (pair_right_identity key) 26) 2 (ite (= (pair_right_identity key) 27) 3 (ite (= (pair_right_identity key) 28) 4 (ite (= (pair_right_identity key) 29) 5 (ite (= (pair_right_identity key) 30) 0 (ite (= (pair_right_identity key) 31) 1 (ite (= (pair_right_identity key) 32) 2 (ite (= (pair_right_identity key) 33) 3 (ite (= (pair_right_identity key) 34) 4 (ite (= (pair_right_identity key) 35) 5 (ite (= (pair_right_identity key) 36) 0 (ite (= (pair_right_identity key) 37) 1 (ite (= (pair_right_identity key) 38) 2 (ite (= (pair_right_identity key) 39) 3 (ite (= (pair_right_identity key) 40) 4 (ite (= (pair_right_identity key) 41) 5 (ite (= (pair_right_identity key) 42) 0 (ite (= (pair_right_identity key) 43) 1 (ite (= (pair_right_identity key) 44) 2 (ite (= (pair_right_identity key) 45) 3 (ite (= (pair_right_identity key) 46) 4 (ite (= (pair_right_identity key) 47) 5 (ite (= (pair_right_identity key) 48) 0 (ite (= (pair_right_identity key) 49) 1 (ite (= (pair_right_identity key) 50) 2 (ite (= (pair_right_identity key) 51) 3 (ite (= (pair_right_identity key) 52) 4 (ite (= (pair_right_identity key) 53) 5 (ite (= (pair_right_identity key) 54) 0 (ite (= (pair_right_identity key) 55) 1 (ite (= (pair_right_identity key) 56) 2 (ite (= (pair_right_identity key) 57) 3 (ite (= (pair_right_identity key) 58) 4 (ite (= (pair_right_identity key) 59) 5 (ite (= (pair_right_identity key) 60) 0 (ite (= (pair_right_identity key) 61) 1 (ite (= (pair_right_identity key) 62) 2 (ite (= (pair_right_identity key) 63) 3 (ite (= (pair_right_identity key) 64) 4 (ite (= (pair_right_identity key) 65) 5 (ite (= (pair_right_identity key) 66) 0 (ite (= (pair_right_identity key) 67) 1 (ite (= (pair_right_identity key) 68) 2 (ite (= (pair_right_identity key) 69) 3 (ite (= (pair_right_identity key) 70) 4 (ite (= (pair_right_identity key) 71) 5 (ite (= (pair_right_identity key) 72) 0 (ite (= (pair_right_identity key) 73) 1 (ite (= (pair_right_identity key) 74) 2 (ite (= (pair_right_identity key) 75) 3 (ite (= (pair_right_identity key) 76) 4 (ite (= (pair_right_identity key) 77) 5 (ite (= (pair_right_identity key) 78) 0 (ite (= (pair_right_identity key) 79) 1 (pair_right_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 0 1)))
    (lambda ((key CallKey)) (ite (or (< (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4) (= (call_left_identity key) 5) (= (call_left_identity key) 6) (= (call_left_identity key) 7) (= (call_left_identity key) 8) (= (call_left_identity key) 9) (= (call_left_identity key) 10) (= (call_left_identity key) 11) (= (call_left_identity key) 12) (= (call_left_identity key) 13) (= (call_left_identity key) 14) (= (call_left_identity key) 15) (= (call_left_identity key) 16) (= (call_left_identity key) 17) (= (call_left_identity key) 18) (= (call_left_identity key) 19) (= (call_left_identity key) 20) (= (call_left_identity key) 21) (= (call_left_identity key) 22) (= (call_left_identity key) 23) (= (call_left_identity key) 24) (= (call_left_identity key) 25) (= (call_left_identity key) 26) (= (call_left_identity key) 27) (= (call_left_identity key) 28) (= (call_left_identity key) 29) (= (call_left_identity key) 30) (= (call_left_identity key) 31) (= (call_left_identity key) 32) (= (call_left_identity key) 33) (= (call_left_identity key) 34) (= (call_left_identity key) 35) (= (call_left_identity key) 36) (= (call_left_identity key) 37) (= (call_left_identity key) 38) (= (call_left_identity key) 39) (= (call_left_identity key) 40) (= (call_left_identity key) 41) (= (call_left_identity key) 42) (= (call_left_identity key) 43) (= (call_left_identity key) 44) (= (call_left_identity key) 45) (= (call_left_identity key) 46) (= (call_left_identity key) 47) (= (call_left_identity key) 48) (= (call_left_identity key) 49) (= (call_left_identity key) 50) (= (call_left_identity key) 51) (= (call_left_identity key) 52) (= (call_left_identity key) 53) (= (call_left_identity key) 54) (= (call_left_identity key) 55) (= (call_left_identity key) 56) (= (call_left_identity key) 57) (= (call_left_identity key) 58) (= (call_left_identity key) 59) (= (call_left_identity key) 60) (= (call_left_identity key) 61) (= (call_left_identity key) 62) (= (call_left_identity key) 63) (= (call_left_identity key) 64) (= (call_left_identity key) 65) (= (call_left_identity key) 66) (= (call_left_identity key) 67) (= (call_left_identity key) 68) (= (call_left_identity key) 69) (= (call_left_identity key) 70) (= (call_left_identity key) 71) (= (call_left_identity key) 72) (= (call_left_identity key) 73) (= (call_left_identity key) 74) (= (call_left_identity key) 75) (= (call_left_identity key) 76) (= (call_left_identity key) 77) (= (call_left_identity key) 78) (= (call_left_identity key) 79)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4) (= (call_right_identity key) 5) (= (call_right_identity key) 6) (= (call_right_identity key) 7) (= (call_right_identity key) 8) (= (call_right_identity key) 9) (= (call_right_identity key) 10) (= (call_right_identity key) 11) (= (call_right_identity key) 12) (= (call_right_identity key) 13) (= (call_right_identity key) 14) (= (call_right_identity key) 15) (= (call_right_identity key) 16) (= (call_right_identity key) 17) (= (call_right_identity key) 18) (= (call_right_identity key) 19) (= (call_right_identity key) 20) (= (call_right_identity key) 21) (= (call_right_identity key) 22) (= (call_right_identity key) 23) (= (call_right_identity key) 24) (= (call_right_identity key) 25) (= (call_right_identity key) 26) (= (call_right_identity key) 27) (= (call_right_identity key) 28) (= (call_right_identity key) 29) (= (call_right_identity key) 30) (= (call_right_identity key) 31) (= (call_right_identity key) 32) (= (call_right_identity key) 33) (= (call_right_identity key) 34) (= (call_right_identity key) 35) (= (call_right_identity key) 36) (= (call_right_identity key) 37) (= (call_right_identity key) 38) (= (call_right_identity key) 39) (= (call_right_identity key) 40) (= (call_right_identity key) 41) (= (call_right_identity key) 42) (= (call_right_identity key) 43) (= (call_right_identity key) 44) (= (call_right_identity key) 45) (= (call_right_identity key) 46) (= (call_right_identity key) 47) (= (call_right_identity key) 48) (= (call_right_identity key) 49) (= (call_right_identity key) 50) (= (call_right_identity key) 51) (= (call_right_identity key) 52) (= (call_right_identity key) 53) (= (call_right_identity key) 54) (= (call_right_identity key) 55) (= (call_right_identity key) 56) (= (call_right_identity key) 57) (= (call_right_identity key) 58) (= (call_right_identity key) 59) (= (call_right_identity key) 60) (= (call_right_identity key) 61) (= (call_right_identity key) 62) (= (call_right_identity key) 63) (= (call_right_identity key) 64) (= (call_right_identity key) 65) (= (call_right_identity key) 66) (= (call_right_identity key) 67) (= (call_right_identity key) 68) (= (call_right_identity key) 69) (= (call_right_identity key) 70) (= (call_right_identity key) 71) (= (call_right_identity key) 72) (= (call_right_identity key) 73) (= (call_right_identity key) 74) (= (call_right_identity key) 75) (= (call_right_identity key) 76) (= (call_right_identity key) 77) (= (call_right_identity key) 78) (= (call_right_identity key) 79)) 0 1)) (and (= (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4) (= (call_left_identity key) 5) (= (call_left_identity key) 6) (= (call_left_identity key) 7) (= (call_left_identity key) 8) (= (call_left_identity key) 9) (= (call_left_identity key) 10) (= (call_left_identity key) 11) (= (call_left_identity key) 12) (= (call_left_identity key) 13) (= (call_left_identity key) 14) (= (call_left_identity key) 15) (= (call_left_identity key) 16) (= (call_left_identity key) 17) (= (call_left_identity key) 18) (= (call_left_identity key) 19) (= (call_left_identity key) 20) (= (call_left_identity key) 21) (= (call_left_identity key) 22) (= (call_left_identity key) 23) (= (call_left_identity key) 24) (= (call_left_identity key) 25) (= (call_left_identity key) 26) (= (call_left_identity key) 27) (= (call_left_identity key) 28) (= (call_left_identity key) 29) (= (call_left_identity key) 30) (= (call_left_identity key) 31) (= (call_left_identity key) 32) (= (call_left_identity key) 33) (= (call_left_identity key) 34) (= (call_left_identity key) 35) (= (call_left_identity key) 36) (= (call_left_identity key) 37) (= (call_left_identity key) 38) (= (call_left_identity key) 39) (= (call_left_identity key) 40) (= (call_left_identity key) 41) (= (call_left_identity key) 42) (= (call_left_identity key) 43) (= (call_left_identity key) 44) (= (call_left_identity key) 45) (= (call_left_identity key) 46) (= (call_left_identity key) 47) (= (call_left_identity key) 48) (= (call_left_identity key) 49) (= (call_left_identity key) 50) (= (call_left_identity key) 51) (= (call_left_identity key) 52) (= (call_left_identity key) 53) (= (call_left_identity key) 54) (= (call_left_identity key) 55) (= (call_left_identity key) 56) (= (call_left_identity key) 57) (= (call_left_identity key) 58) (= (call_left_identity key) 59) (= (call_left_identity key) 60) (= (call_left_identity key) 61) (= (call_left_identity key) 62) (= (call_left_identity key) 63) (= (call_left_identity key) 64) (= (call_left_identity key) 65) (= (call_left_identity key) 66) (= (call_left_identity key) 67) (= (call_left_identity key) 68) (= (call_left_identity key) 69) (= (call_left_identity key) 70) (= (call_left_identity key) 71) (= (call_left_identity key) 72) (= (call_left_identity key) 73) (= (call_left_identity key) 74) (= (call_left_identity key) 75) (= (call_left_identity key) 76) (= (call_left_identity key) 77) (= (call_left_identity key) 78) (= (call_left_identity key) 79)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4) (= (call_right_identity key) 5) (= (call_right_identity key) 6) (= (call_right_identity key) 7) (= (call_right_identity key) 8) (= (call_right_identity key) 9) (= (call_right_identity key) 10) (= (call_right_identity key) 11) (= (call_right_identity key) 12) (= (call_right_identity key) 13) (= (call_right_identity key) 14) (= (call_right_identity key) 15) (= (call_right_identity key) 16) (= (call_right_identity key) 17) (= (call_right_identity key) 18) (= (call_right_identity key) 19) (= (call_right_identity key) 20) (= (call_right_identity key) 21) (= (call_right_identity key) 22) (= (call_right_identity key) 23) (= (call_right_identity key) 24) (= (call_right_identity key) 25) (= (call_right_identity key) 26) (= (call_right_identity key) 27) (= (call_right_identity key) 28) (= (call_right_identity key) 29) (= (call_right_identity key) 30) (= (call_right_identity key) 31) (= (call_right_identity key) 32) (= (call_right_identity key) 33) (= (call_right_identity key) 34) (= (call_right_identity key) 35) (= (call_right_identity key) 36) (= (call_right_identity key) 37) (= (call_right_identity key) 38) (= (call_right_identity key) 39) (= (call_right_identity key) 40) (= (call_right_identity key) 41) (= (call_right_identity key) 42) (= (call_right_identity key) 43) (= (call_right_identity key) 44) (= (call_right_identity key) 45) (= (call_right_identity key) 46) (= (call_right_identity key) 47) (= (call_right_identity key) 48) (= (call_right_identity key) 49) (= (call_right_identity key) 50) (= (call_right_identity key) 51) (= (call_right_identity key) 52) (= (call_right_identity key) 53) (= (call_right_identity key) 54) (= (call_right_identity key) 55) (= (call_right_identity key) 56) (= (call_right_identity key) 57) (= (call_right_identity key) 58) (= (call_right_identity key) 59) (= (call_right_identity key) 60) (= (call_right_identity key) 61) (= (call_right_identity key) 62) (= (call_right_identity key) 63) (= (call_right_identity key) 64) (= (call_right_identity key) 65) (= (call_right_identity key) 66) (= (call_right_identity key) 67) (= (call_right_identity key) 68) (= (call_right_identity key) 69) (= (call_right_identity key) 70) (= (call_right_identity key) 71) (= (call_right_identity key) 72) (= (call_right_identity key) 73) (= (call_right_identity key) 74) (= (call_right_identity key) 75) (= (call_right_identity key) 76) (= (call_right_identity key) 77) (= (call_right_identity key) 78) (= (call_right_identity key) 79)) 0 1)) (< (ite (= (call_left_identity key) 0) 0 (ite (= (call_left_identity key) 1) 1 (ite (= (call_left_identity key) 2) 2 (ite (= (call_left_identity key) 3) 3 (ite (= (call_left_identity key) 4) 4 (ite (= (call_left_identity key) 5) 5 (ite (= (call_left_identity key) 6) 0 (ite (= (call_left_identity key) 7) 1 (ite (= (call_left_identity key) 8) 2 (ite (= (call_left_identity key) 9) 3 (ite (= (call_left_identity key) 10) 4 (ite (= (call_left_identity key) 11) 5 (ite (= (call_left_identity key) 12) 0 (ite (= (call_left_identity key) 13) 1 (ite (= (call_left_identity key) 14) 2 (ite (= (call_left_identity key) 15) 3 (ite (= (call_left_identity key) 16) 4 (ite (= (call_left_identity key) 17) 5 (ite (= (call_left_identity key) 18) 0 (ite (= (call_left_identity key) 19) 1 (ite (= (call_left_identity key) 20) 2 (ite (= (call_left_identity key) 21) 3 (ite (= (call_left_identity key) 22) 4 (ite (= (call_left_identity key) 23) 5 (ite (= (call_left_identity key) 24) 0 (ite (= (call_left_identity key) 25) 1 (ite (= (call_left_identity key) 26) 2 (ite (= (call_left_identity key) 27) 3 (ite (= (call_left_identity key) 28) 4 (ite (= (call_left_identity key) 29) 5 (ite (= (call_left_identity key) 30) 0 (ite (= (call_left_identity key) 31) 1 (ite (= (call_left_identity key) 32) 2 (ite (= (call_left_identity key) 33) 3 (ite (= (call_left_identity key) 34) 4 (ite (= (call_left_identity key) 35) 5 (ite (= (call_left_identity key) 36) 0 (ite (= (call_left_identity key) 37) 1 (ite (= (call_left_identity key) 38) 2 (ite (= (call_left_identity key) 39) 3 (ite (= (call_left_identity key) 40) 4 (ite (= (call_left_identity key) 41) 5 (ite (= (call_left_identity key) 42) 0 (ite (= (call_left_identity key) 43) 1 (ite (= (call_left_identity key) 44) 2 (ite (= (call_left_identity key) 45) 3 (ite (= (call_left_identity key) 46) 4 (ite (= (call_left_identity key) 47) 5 (ite (= (call_left_identity key) 48) 0 (ite (= (call_left_identity key) 49) 1 (ite (= (call_left_identity key) 50) 2 (ite (= (call_left_identity key) 51) 3 (ite (= (call_left_identity key) 52) 4 (ite (= (call_left_identity key) 53) 5 (ite (= (call_left_identity key) 54) 0 (ite (= (call_left_identity key) 55) 1 (ite (= (call_left_identity key) 56) 2 (ite (= (call_left_identity key) 57) 3 (ite (= (call_left_identity key) 58) 4 (ite (= (call_left_identity key) 59) 5 (ite (= (call_left_identity key) 60) 0 (ite (= (call_left_identity key) 61) 1 (ite (= (call_left_identity key) 62) 2 (ite (= (call_left_identity key) 63) 3 (ite (= (call_left_identity key) 64) 4 (ite (= (call_left_identity key) 65) 5 (ite (= (call_left_identity key) 66) 0 (ite (= (call_left_identity key) 67) 1 (ite (= (call_left_identity key) 68) 2 (ite (= (call_left_identity key) 69) 3 (ite (= (call_left_identity key) 70) 4 (ite (= (call_left_identity key) 71) 5 (ite (= (call_left_identity key) 72) 0 (ite (= (call_left_identity key) 73) 1 (ite (= (call_left_identity key) 74) 2 (ite (= (call_left_identity key) 75) 3 (ite (= (call_left_identity key) 76) 4 (ite (= (call_left_identity key) 77) 5 (ite (= (call_left_identity key) 78) 0 (ite (= (call_left_identity key) 79) 1 (call_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (call_right_identity key) 0) 0 (ite (= (call_right_identity key) 1) 1 (ite (= (call_right_identity key) 2) 2 (ite (= (call_right_identity key) 3) 3 (ite (= (call_right_identity key) 4) 4 (ite (= (call_right_identity key) 5) 5 (ite (= (call_right_identity key) 6) 0 (ite (= (call_right_identity key) 7) 1 (ite (= (call_right_identity key) 8) 2 (ite (= (call_right_identity key) 9) 3 (ite (= (call_right_identity key) 10) 4 (ite (= (call_right_identity key) 11) 5 (ite (= (call_right_identity key) 12) 0 (ite (= (call_right_identity key) 13) 1 (ite (= (call_right_identity key) 14) 2 (ite (= (call_right_identity key) 15) 3 (ite (= (call_right_identity key) 16) 4 (ite (= (call_right_identity key) 17) 5 (ite (= (call_right_identity key) 18) 0 (ite (= (call_right_identity key) 19) 1 (ite (= (call_right_identity key) 20) 2 (ite (= (call_right_identity key) 21) 3 (ite (= (call_right_identity key) 22) 4 (ite (= (call_right_identity key) 23) 5 (ite (= (call_right_identity key) 24) 0 (ite (= (call_right_identity key) 25) 1 (ite (= (call_right_identity key) 26) 2 (ite (= (call_right_identity key) 27) 3 (ite (= (call_right_identity key) 28) 4 (ite (= (call_right_identity key) 29) 5 (ite (= (call_right_identity key) 30) 0 (ite (= (call_right_identity key) 31) 1 (ite (= (call_right_identity key) 32) 2 (ite (= (call_right_identity key) 33) 3 (ite (= (call_right_identity key) 34) 4 (ite (= (call_right_identity key) 35) 5 (ite (= (call_right_identity key) 36) 0 (ite (= (call_right_identity key) 37) 1 (ite (= (call_right_identity key) 38) 2 (ite (= (call_right_identity key) 39) 3 (ite (= (call_right_identity key) 40) 4 (ite (= (call_right_identity key) 41) 5 (ite (= (call_right_identity key) 42) 0 (ite (= (call_right_identity key) 43) 1 (ite (= (call_right_identity key) 44) 2 (ite (= (call_right_identity key) 45) 3 (ite (= (call_right_identity key) 46) 4 (ite (= (call_right_identity key) 47) 5 (ite (= (call_right_identity key) 48) 0 (ite (= (call_right_identity key) 49) 1 (ite (= (call_right_identity key) 50) 2 (ite (= (call_right_identity key) 51) 3 (ite (= (call_right_identity key) 52) 4 (ite (= (call_right_identity key) 53) 5 (ite (= (call_right_identity key) 54) 0 (ite (= (call_right_identity key) 55) 1 (ite (= (call_right_identity key) 56) 2 (ite (= (call_right_identity key) 57) 3 (ite (= (call_right_identity key) 58) 4 (ite (= (call_right_identity key) 59) 5 (ite (= (call_right_identity key) 60) 0 (ite (= (call_right_identity key) 61) 1 (ite (= (call_right_identity key) 62) 2 (ite (= (call_right_identity key) 63) 3 (ite (= (call_right_identity key) 64) 4 (ite (= (call_right_identity key) 65) 5 (ite (= (call_right_identity key) 66) 0 (ite (= (call_right_identity key) 67) 1 (ite (= (call_right_identity key) 68) 2 (ite (= (call_right_identity key) 69) 3 (ite (= (call_right_identity key) 70) 4 (ite (= (call_right_identity key) 71) 5 (ite (= (call_right_identity key) 72) 0 (ite (= (call_right_identity key) 73) 1 (ite (= (call_right_identity key) 74) 2 (ite (= (call_right_identity key) 75) 3 (ite (= (call_right_identity key) 76) 4 (ite (= (call_right_identity key) 77) 5 (ite (= (call_right_identity key) 78) 0 (ite (= (call_right_identity key) 79) 1 (call_right_identity key)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) -1 (ite (and (= (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4) (= (call_left_identity key) 5) (= (call_left_identity key) 6) (= (call_left_identity key) 7) (= (call_left_identity key) 8) (= (call_left_identity key) 9) (= (call_left_identity key) 10) (= (call_left_identity key) 11) (= (call_left_identity key) 12) (= (call_left_identity key) 13) (= (call_left_identity key) 14) (= (call_left_identity key) 15) (= (call_left_identity key) 16) (= (call_left_identity key) 17) (= (call_left_identity key) 18) (= (call_left_identity key) 19) (= (call_left_identity key) 20) (= (call_left_identity key) 21) (= (call_left_identity key) 22) (= (call_left_identity key) 23) (= (call_left_identity key) 24) (= (call_left_identity key) 25) (= (call_left_identity key) 26) (= (call_left_identity key) 27) (= (call_left_identity key) 28) (= (call_left_identity key) 29) (= (call_left_identity key) 30) (= (call_left_identity key) 31) (= (call_left_identity key) 32) (= (call_left_identity key) 33) (= (call_left_identity key) 34) (= (call_left_identity key) 35) (= (call_left_identity key) 36) (= (call_left_identity key) 37) (= (call_left_identity key) 38) (= (call_left_identity key) 39) (= (call_left_identity key) 40) (= (call_left_identity key) 41) (= (call_left_identity key) 42) (= (call_left_identity key) 43) (= (call_left_identity key) 44) (= (call_left_identity key) 45) (= (call_left_identity key) 46) (= (call_left_identity key) 47) (= (call_left_identity key) 48) (= (call_left_identity key) 49) (= (call_left_identity key) 50) (= (call_left_identity key) 51) (= (call_left_identity key) 52) (= (call_left_identity key) 53) (= (call_left_identity key) 54) (= (call_left_identity key) 55) (= (call_left_identity key) 56) (= (call_left_identity key) 57) (= (call_left_identity key) 58) (= (call_left_identity key) 59) (= (call_left_identity key) 60) (= (call_left_identity key) 61) (= (call_left_identity key) 62) (= (call_left_identity key) 63) (= (call_left_identity key) 64) (= (call_left_identity key) 65) (= (call_left_identity key) 66) (= (call_left_identity key) 67) (= (call_left_identity key) 68) (= (call_left_identity key) 69) (= (call_left_identity key) 70) (= (call_left_identity key) 71) (= (call_left_identity key) 72) (= (call_left_identity key) 73) (= (call_left_identity key) 74) (= (call_left_identity key) 75) (= (call_left_identity key) 76) (= (call_left_identity key) 77) (= (call_left_identity key) 78) (= (call_left_identity key) 79)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4) (= (call_right_identity key) 5) (= (call_right_identity key) 6) (= (call_right_identity key) 7) (= (call_right_identity key) 8) (= (call_right_identity key) 9) (= (call_right_identity key) 10) (= (call_right_identity key) 11) (= (call_right_identity key) 12) (= (call_right_identity key) 13) (= (call_right_identity key) 14) (= (call_right_identity key) 15) (= (call_right_identity key) 16) (= (call_right_identity key) 17) (= (call_right_identity key) 18) (= (call_right_identity key) 19) (= (call_right_identity key) 20) (= (call_right_identity key) 21) (= (call_right_identity key) 22) (= (call_right_identity key) 23) (= (call_right_identity key) 24) (= (call_right_identity key) 25) (= (call_right_identity key) 26) (= (call_right_identity key) 27) (= (call_right_identity key) 28) (= (call_right_identity key) 29) (= (call_right_identity key) 30) (= (call_right_identity key) 31) (= (call_right_identity key) 32) (= (call_right_identity key) 33) (= (call_right_identity key) 34) (= (call_right_identity key) 35) (= (call_right_identity key) 36) (= (call_right_identity key) 37) (= (call_right_identity key) 38) (= (call_right_identity key) 39) (= (call_right_identity key) 40) (= (call_right_identity key) 41) (= (call_right_identity key) 42) (= (call_right_identity key) 43) (= (call_right_identity key) 44) (= (call_right_identity key) 45) (= (call_right_identity key) 46) (= (call_right_identity key) 47) (= (call_right_identity key) 48) (= (call_right_identity key) 49) (= (call_right_identity key) 50) (= (call_right_identity key) 51) (= (call_right_identity key) 52) (= (call_right_identity key) 53) (= (call_right_identity key) 54) (= (call_right_identity key) 55) (= (call_right_identity key) 56) (= (call_right_identity key) 57) (= (call_right_identity key) 58) (= (call_right_identity key) 59) (= (call_right_identity key) 60) (= (call_right_identity key) 61) (= (call_right_identity key) 62) (= (call_right_identity key) 63) (= (call_right_identity key) 64) (= (call_right_identity key) 65) (= (call_right_identity key) 66) (= (call_right_identity key) 67) (= (call_right_identity key) 68) (= (call_right_identity key) 69) (= (call_right_identity key) 70) (= (call_right_identity key) 71) (= (call_right_identity key) 72) (= (call_right_identity key) 73) (= (call_right_identity key) 74) (= (call_right_identity key) 75) (= (call_right_identity key) 76) (= (call_right_identity key) 77) (= (call_right_identity key) 78) (= (call_right_identity key) 79)) 0 1)) (= (ite (= (call_left_identity key) 0) 0 (ite (= (call_left_identity key) 1) 1 (ite (= (call_left_identity key) 2) 2 (ite (= (call_left_identity key) 3) 3 (ite (= (call_left_identity key) 4) 4 (ite (= (call_left_identity key) 5) 5 (ite (= (call_left_identity key) 6) 0 (ite (= (call_left_identity key) 7) 1 (ite (= (call_left_identity key) 8) 2 (ite (= (call_left_identity key) 9) 3 (ite (= (call_left_identity key) 10) 4 (ite (= (call_left_identity key) 11) 5 (ite (= (call_left_identity key) 12) 0 (ite (= (call_left_identity key) 13) 1 (ite (= (call_left_identity key) 14) 2 (ite (= (call_left_identity key) 15) 3 (ite (= (call_left_identity key) 16) 4 (ite (= (call_left_identity key) 17) 5 (ite (= (call_left_identity key) 18) 0 (ite (= (call_left_identity key) 19) 1 (ite (= (call_left_identity key) 20) 2 (ite (= (call_left_identity key) 21) 3 (ite (= (call_left_identity key) 22) 4 (ite (= (call_left_identity key) 23) 5 (ite (= (call_left_identity key) 24) 0 (ite (= (call_left_identity key) 25) 1 (ite (= (call_left_identity key) 26) 2 (ite (= (call_left_identity key) 27) 3 (ite (= (call_left_identity key) 28) 4 (ite (= (call_left_identity key) 29) 5 (ite (= (call_left_identity key) 30) 0 (ite (= (call_left_identity key) 31) 1 (ite (= (call_left_identity key) 32) 2 (ite (= (call_left_identity key) 33) 3 (ite (= (call_left_identity key) 34) 4 (ite (= (call_left_identity key) 35) 5 (ite (= (call_left_identity key) 36) 0 (ite (= (call_left_identity key) 37) 1 (ite (= (call_left_identity key) 38) 2 (ite (= (call_left_identity key) 39) 3 (ite (= (call_left_identity key) 40) 4 (ite (= (call_left_identity key) 41) 5 (ite (= (call_left_identity key) 42) 0 (ite (= (call_left_identity key) 43) 1 (ite (= (call_left_identity key) 44) 2 (ite (= (call_left_identity key) 45) 3 (ite (= (call_left_identity key) 46) 4 (ite (= (call_left_identity key) 47) 5 (ite (= (call_left_identity key) 48) 0 (ite (= (call_left_identity key) 49) 1 (ite (= (call_left_identity key) 50) 2 (ite (= (call_left_identity key) 51) 3 (ite (= (call_left_identity key) 52) 4 (ite (= (call_left_identity key) 53) 5 (ite (= (call_left_identity key) 54) 0 (ite (= (call_left_identity key) 55) 1 (ite (= (call_left_identity key) 56) 2 (ite (= (call_left_identity key) 57) 3 (ite (= (call_left_identity key) 58) 4 (ite (= (call_left_identity key) 59) 5 (ite (= (call_left_identity key) 60) 0 (ite (= (call_left_identity key) 61) 1 (ite (= (call_left_identity key) 62) 2 (ite (= (call_left_identity key) 63) 3 (ite (= (call_left_identity key) 64) 4 (ite (= (call_left_identity key) 65) 5 (ite (= (call_left_identity key) 66) 0 (ite (= (call_left_identity key) 67) 1 (ite (= (call_left_identity key) 68) 2 (ite (= (call_left_identity key) 69) 3 (ite (= (call_left_identity key) 70) 4 (ite (= (call_left_identity key) 71) 5 (ite (= (call_left_identity key) 72) 0 (ite (= (call_left_identity key) 73) 1 (ite (= (call_left_identity key) 74) 2 (ite (= (call_left_identity key) 75) 3 (ite (= (call_left_identity key) 76) 4 (ite (= (call_left_identity key) 77) 5 (ite (= (call_left_identity key) 78) 0 (ite (= (call_left_identity key) 79) 1 (call_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (call_right_identity key) 0) 0 (ite (= (call_right_identity key) 1) 1 (ite (= (call_right_identity key) 2) 2 (ite (= (call_right_identity key) 3) 3 (ite (= (call_right_identity key) 4) 4 (ite (= (call_right_identity key) 5) 5 (ite (= (call_right_identity key) 6) 0 (ite (= (call_right_identity key) 7) 1 (ite (= (call_right_identity key) 8) 2 (ite (= (call_right_identity key) 9) 3 (ite (= (call_right_identity key) 10) 4 (ite (= (call_right_identity key) 11) 5 (ite (= (call_right_identity key) 12) 0 (ite (= (call_right_identity key) 13) 1 (ite (= (call_right_identity key) 14) 2 (ite (= (call_right_identity key) 15) 3 (ite (= (call_right_identity key) 16) 4 (ite (= (call_right_identity key) 17) 5 (ite (= (call_right_identity key) 18) 0 (ite (= (call_right_identity key) 19) 1 (ite (= (call_right_identity key) 20) 2 (ite (= (call_right_identity key) 21) 3 (ite (= (call_right_identity key) 22) 4 (ite (= (call_right_identity key) 23) 5 (ite (= (call_right_identity key) 24) 0 (ite (= (call_right_identity key) 25) 1 (ite (= (call_right_identity key) 26) 2 (ite (= (call_right_identity key) 27) 3 (ite (= (call_right_identity key) 28) 4 (ite (= (call_right_identity key) 29) 5 (ite (= (call_right_identity key) 30) 0 (ite (= (call_right_identity key) 31) 1 (ite (= (call_right_identity key) 32) 2 (ite (= (call_right_identity key) 33) 3 (ite (= (call_right_identity key) 34) 4 (ite (= (call_right_identity key) 35) 5 (ite (= (call_right_identity key) 36) 0 (ite (= (call_right_identity key) 37) 1 (ite (= (call_right_identity key) 38) 2 (ite (= (call_right_identity key) 39) 3 (ite (= (call_right_identity key) 40) 4 (ite (= (call_right_identity key) 41) 5 (ite (= (call_right_identity key) 42) 0 (ite (= (call_right_identity key) 43) 1 (ite (= (call_right_identity key) 44) 2 (ite (= (call_right_identity key) 45) 3 (ite (= (call_right_identity key) 46) 4 (ite (= (call_right_identity key) 47) 5 (ite (= (call_right_identity key) 48) 0 (ite (= (call_right_identity key) 49) 1 (ite (= (call_right_identity key) 50) 2 (ite (= (call_right_identity key) 51) 3 (ite (= (call_right_identity key) 52) 4 (ite (= (call_right_identity key) 53) 5 (ite (= (call_right_identity key) 54) 0 (ite (= (call_right_identity key) 55) 1 (ite (= (call_right_identity key) 56) 2 (ite (= (call_right_identity key) 57) 3 (ite (= (call_right_identity key) 58) 4 (ite (= (call_right_identity key) 59) 5 (ite (= (call_right_identity key) 60) 0 (ite (= (call_right_identity key) 61) 1 (ite (= (call_right_identity key) 62) 2 (ite (= (call_right_identity key) 63) 3 (ite (= (call_right_identity key) 64) 4 (ite (= (call_right_identity key) 65) 5 (ite (= (call_right_identity key) 66) 0 (ite (= (call_right_identity key) 67) 1 (ite (= (call_right_identity key) 68) 2 (ite (= (call_right_identity key) 69) 3 (ite (= (call_right_identity key) 70) 4 (ite (= (call_right_identity key) 71) 5 (ite (= (call_right_identity key) 72) 0 (ite (= (call_right_identity key) 73) 1 (ite (= (call_right_identity key) 74) 2 (ite (= (call_right_identity key) 75) 3 (ite (= (call_right_identity key) 76) 4 (ite (= (call_right_identity key) 77) 5 (ite (= (call_right_identity key) 78) 0 (ite (= (call_right_identity key) 79) 1 (call_right_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration_0 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun source_initial_0 () FormalMachine
  (mkFormalMachine (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 56) 1 44) 2 42) 3 50) 4 24) 5 31) 6 68) 7 11) 8 66) 9 41) 10 75) 11 8) 12 37) 13 29) 14 1) 15 14) 16 52) 17 59) 18 63) 19 18) 20 47) 21 2) 22 78) 23 74) 24 23) 25 7) 26 10) 27 60) 28 26) 29 15) 30 55) 31 71) 32 25) 33 77) 34 0) 35 3) 36 16) 37 76) 38 28) 39 79) 40 48) 41 13) 42 40) 43 39) 44 20) 45 69) 46 22) 47 54) 48 35) 49 30) 50 21) 51 43) 52 4) 53 46) 54 6) 55 19) 56 9) 57 57) 58 72) 59 73) 60 70) 61 34) 62 58) 63 32) 64 12) 65 67) 66 36) 67 17) 68 64) 69 27) 70 45) 71 61) 72 38) 73 51) 74 62) 75 65) 76 33) 77 5) 78 53) 79 49) (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 56) 1 44) 2 42) 3 50) 4 24) 5 31) 6 68) 7 11) 8 66) 9 41) 10 75) 11 8) 12 37) 13 29) 14 1) 15 14) 16 52) 17 59) 18 63) 19 18) 20 47) 21 2) 22 78) 23 74) 24 23) 25 7) 26 10) 27 60) 28 26) 29 15) 30 55) 31 71) 32 25) 33 77) 34 0) 35 3) 36 16) 37 76) 38 28) 39 79) 40 48) 41 13) 42 40) 43 39) 44 20) 45 69) 46 22) 47 54) 48 35) 49 30) 50 21) 51 43) 52 4) 53 46) 54 6) 55 19) 56 9) 57 57) 58 72) 59 73) 60 70) 61 34) 62 58) 63 32) 64 12) 65 67) 66 36) 67 17) 68 64) 69 27) 70 45) 71 61) 72 38) 73 51) 74 62) 75 65) 76 33) 77 5) 78 53) 79 49) (b_initial_state boundary_0) false))
(assert (BoundaryWellFormed boundary_0))
; source callback case=duplicate-class-ancestor-pivot phase=find-existing-run:direction
(assert (not (m_panicked source_initial_0)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) false))
; source callback transition phase=find-existing-run:direction
(define-fun formal_0_1 () FormalMachine (FormalCallback source_initial_0 boundary_0 (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)))
; source callback case=duplicate-class-ancestor-pivot phase=find-existing-run:ascending
(assert (not (m_panicked formal_0_1)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) false))
; source callback transition phase=find-existing-run:ascending
(define-fun formal_0_2 () FormalMachine (FormalCallback formal_0_1 boundary_0 (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3-rec:a:median3:a-b
(assert (not (m_panicked formal_0_2)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 0) (select (m_origin formal_0_2) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 0) (select (m_origin formal_0_2) 4)) false))
; source callback transition phase=choose-pivot:median3-rec:a:median3:a-b
(define-fun formal_0_3 () FormalMachine (FormalCallback formal_0_2 boundary_0 (select (m_origin formal_0_2) 0) (select (m_origin formal_0_2) 4)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3-rec:a:median3:a-c
(assert (not (m_panicked formal_0_3)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 0) (select (m_origin formal_0_3) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 0) (select (m_origin formal_0_3) 7)) false))
; source callback transition phase=choose-pivot:median3-rec:a:median3:a-c
(define-fun formal_0_4 () FormalMachine (FormalCallback formal_0_3 boundary_0 (select (m_origin formal_0_3) 0) (select (m_origin formal_0_3) 7)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3-rec:b:median3:a-b
(assert (not (m_panicked formal_0_4)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 40) (select (m_origin formal_0_4) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 40) (select (m_origin formal_0_4) 44)) false))
; source callback transition phase=choose-pivot:median3-rec:b:median3:a-b
(define-fun formal_0_5 () FormalMachine (FormalCallback formal_0_4 boundary_0 (select (m_origin formal_0_4) 40) (select (m_origin formal_0_4) 44)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3-rec:b:median3:a-c
(assert (not (m_panicked formal_0_5)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_5) (select (m_origin formal_0_5) 40) (select (m_origin formal_0_5) 47)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_5) (select (m_origin formal_0_5) 40) (select (m_origin formal_0_5) 47)) false))
; source callback transition phase=choose-pivot:median3-rec:b:median3:a-c
(define-fun formal_0_6 () FormalMachine (FormalCallback formal_0_5 boundary_0 (select (m_origin formal_0_5) 40) (select (m_origin formal_0_5) 47)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3-rec:c:median3:a-b
(assert (not (m_panicked formal_0_6)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 70) (select (m_origin formal_0_6) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 70) (select (m_origin formal_0_6) 74)) false))
; source callback transition phase=choose-pivot:median3-rec:c:median3:a-b
(define-fun formal_0_7 () FormalMachine (FormalCallback formal_0_6 boundary_0 (select (m_origin formal_0_6) 70) (select (m_origin formal_0_6) 74)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3-rec:c:median3:a-c
(assert (not (m_panicked formal_0_7)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_7) (select (m_origin formal_0_7) 70) (select (m_origin formal_0_7) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_7) (select (m_origin formal_0_7) 70) (select (m_origin formal_0_7) 77)) false))
; source callback transition phase=choose-pivot:median3-rec:c:median3:a-c
(define-fun formal_0_8 () FormalMachine (FormalCallback formal_0_7 boundary_0 (select (m_origin formal_0_7) 70) (select (m_origin formal_0_7) 77)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3-rec:median3:a-b
(assert (not (m_panicked formal_0_8)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 0) (select (m_origin formal_0_8) 40)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 0) (select (m_origin formal_0_8) 40)) false))
; source callback transition phase=choose-pivot:median3-rec:median3:a-b
(define-fun formal_0_9 () FormalMachine (FormalCallback formal_0_8 boundary_0 (select (m_origin formal_0_8) 0) (select (m_origin formal_0_8) 40)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3-rec:median3:a-c
(assert (not (m_panicked formal_0_9)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_9) (select (m_origin formal_0_9) 0) (select (m_origin formal_0_9) 70)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_9) (select (m_origin formal_0_9) 0) (select (m_origin formal_0_9) 70)) false))
; source callback transition phase=choose-pivot:median3-rec:median3:a-c
(define-fun formal_0_10 () FormalMachine (FormalCallback formal_0_9 boundary_0 (select (m_origin formal_0_9) 0) (select (m_origin formal_0_9) 70)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_11 () FormalMachine (FormalSwap formal_0_10 0 0))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_11)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_11) (select (m_origin formal_0_11) 2) (select (m_origin formal_0_11) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_11) (select (m_origin formal_0_11) 2) (select (m_origin formal_0_11) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_12 () FormalMachine (FormalCallback formal_0_11 boundary_0 (select (m_origin formal_0_11) 2) (select (m_origin formal_0_11) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_13 () FormalMachine (FormalWriteFromOrigin formal_0_12 1 2))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_13)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_13) (select (m_origin formal_0_13) 3) (select (m_origin formal_0_13) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_13) (select (m_origin formal_0_13) 3) (select (m_origin formal_0_13) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_14 () FormalMachine (FormalCallback formal_0_13 boundary_0 (select (m_origin formal_0_13) 3) (select (m_origin formal_0_13) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_15 () FormalMachine (FormalWriteFromOrigin formal_0_14 2 3))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_15)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_15) (select (m_origin formal_0_15) 4) (select (m_origin formal_0_15) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_15) (select (m_origin formal_0_15) 4) (select (m_origin formal_0_15) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_16 () FormalMachine (FormalCallback formal_0_15 boundary_0 (select (m_origin formal_0_15) 4) (select (m_origin formal_0_15) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_17 () FormalMachine (FormalWriteFromOrigin formal_0_16 2 4))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_17)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_17) (select (m_origin formal_0_17) 5) (select (m_origin formal_0_17) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_17) (select (m_origin formal_0_17) 5) (select (m_origin formal_0_17) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_18 () FormalMachine (FormalCallback formal_0_17 boundary_0 (select (m_origin formal_0_17) 5) (select (m_origin formal_0_17) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_19 () FormalMachine (FormalWriteFromOrigin formal_0_18 3 5))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_20 () FormalMachine (FormalWriteFromOrigin formal_0_19 4 3))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_20)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 6) (select (m_origin formal_0_20) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 6) (select (m_origin formal_0_20) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_21 () FormalMachine (FormalCallback formal_0_20 boundary_0 (select (m_origin formal_0_20) 6) (select (m_origin formal_0_20) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_22 () FormalMachine (FormalWriteFromOrigin formal_0_21 4 6))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_23 () FormalMachine (FormalWriteFromOrigin formal_0_22 5 3))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_23)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_23) (select (m_origin formal_0_23) 7) (select (m_origin formal_0_23) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_23) (select (m_origin formal_0_23) 7) (select (m_origin formal_0_23) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_24 () FormalMachine (FormalCallback formal_0_23 boundary_0 (select (m_origin formal_0_23) 7) (select (m_origin formal_0_23) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_25 () FormalMachine (FormalWriteFromOrigin formal_0_24 4 7))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_25)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 8) (select (m_origin formal_0_25) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 8) (select (m_origin formal_0_25) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_26 () FormalMachine (FormalCallback formal_0_25 boundary_0 (select (m_origin formal_0_25) 8) (select (m_origin formal_0_25) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_27 () FormalMachine (FormalWriteFromOrigin formal_0_26 4 8))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_27)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_27) (select (m_origin formal_0_27) 9) (select (m_origin formal_0_27) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_27) (select (m_origin formal_0_27) 9) (select (m_origin formal_0_27) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_28 () FormalMachine (FormalCallback formal_0_27 boundary_0 (select (m_origin formal_0_27) 9) (select (m_origin formal_0_27) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_29 () FormalMachine (FormalWriteFromOrigin formal_0_28 5 9))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_30 () FormalMachine (FormalWriteFromOrigin formal_0_29 8 3))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_30)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_30) (select (m_origin formal_0_30) 10) (select (m_origin formal_0_30) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_30) (select (m_origin formal_0_30) 10) (select (m_origin formal_0_30) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_31 () FormalMachine (FormalCallback formal_0_30 boundary_0 (select (m_origin formal_0_30) 10) (select (m_origin formal_0_30) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_32 () FormalMachine (FormalWriteFromOrigin formal_0_31 5 10))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_32)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_32) (select (m_origin formal_0_32) 11) (select (m_origin formal_0_32) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_32) (select (m_origin formal_0_32) 11) (select (m_origin formal_0_32) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_33 () FormalMachine (FormalCallback formal_0_32 boundary_0 (select (m_origin formal_0_32) 11) (select (m_origin formal_0_32) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_34 () FormalMachine (FormalWriteFromOrigin formal_0_33 5 11))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_34)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_34) (select (m_origin formal_0_34) 12) (select (m_origin formal_0_34) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_34) (select (m_origin formal_0_34) 12) (select (m_origin formal_0_34) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_35 () FormalMachine (FormalCallback formal_0_34 boundary_0 (select (m_origin formal_0_34) 12) (select (m_origin formal_0_34) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_36 () FormalMachine (FormalWriteFromOrigin formal_0_35 5 12))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_36)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_36) (select (m_origin formal_0_36) 13) (select (m_origin formal_0_36) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_36) (select (m_origin formal_0_36) 13) (select (m_origin formal_0_36) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_37 () FormalMachine (FormalCallback formal_0_36 boundary_0 (select (m_origin formal_0_36) 13) (select (m_origin formal_0_36) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_38 () FormalMachine (FormalWriteFromOrigin formal_0_37 6 13))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_39 () FormalMachine (FormalWriteFromOrigin formal_0_38 12 6))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_39)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_39) (select (m_origin formal_0_39) 14) (select (m_origin formal_0_39) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_39) (select (m_origin formal_0_39) 14) (select (m_origin formal_0_39) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_40 () FormalMachine (FormalCallback formal_0_39 boundary_0 (select (m_origin formal_0_39) 14) (select (m_origin formal_0_39) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_41 () FormalMachine (FormalWriteFromOrigin formal_0_40 6 14))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_41)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 15) (select (m_origin formal_0_41) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 15) (select (m_origin formal_0_41) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_42 () FormalMachine (FormalCallback formal_0_41 boundary_0 (select (m_origin formal_0_41) 15) (select (m_origin formal_0_41) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_43 () FormalMachine (FormalWriteFromOrigin formal_0_42 7 15))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_44 () FormalMachine (FormalWriteFromOrigin formal_0_43 14 7))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_44)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 16) (select (m_origin formal_0_44) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 16) (select (m_origin formal_0_44) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_45 () FormalMachine (FormalCallback formal_0_44 boundary_0 (select (m_origin formal_0_44) 16) (select (m_origin formal_0_44) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_46 () FormalMachine (FormalWriteFromOrigin formal_0_45 7 16))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_46)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_46) (select (m_origin formal_0_46) 17) (select (m_origin formal_0_46) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_46) (select (m_origin formal_0_46) 17) (select (m_origin formal_0_46) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_47 () FormalMachine (FormalCallback formal_0_46 boundary_0 (select (m_origin formal_0_46) 17) (select (m_origin formal_0_46) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_48 () FormalMachine (FormalWriteFromOrigin formal_0_47 7 17))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_48)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 18) (select (m_origin formal_0_48) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 18) (select (m_origin formal_0_48) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_49 () FormalMachine (FormalCallback formal_0_48 boundary_0 (select (m_origin formal_0_48) 18) (select (m_origin formal_0_48) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_50 () FormalMachine (FormalWriteFromOrigin formal_0_49 7 18))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_50)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_50) (select (m_origin formal_0_50) 19) (select (m_origin formal_0_50) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_50) (select (m_origin formal_0_50) 19) (select (m_origin formal_0_50) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_51 () FormalMachine (FormalCallback formal_0_50 boundary_0 (select (m_origin formal_0_50) 19) (select (m_origin formal_0_50) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_52 () FormalMachine (FormalWriteFromOrigin formal_0_51 7 19))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_52)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_52) (select (m_origin formal_0_52) 20) (select (m_origin formal_0_52) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_52) (select (m_origin formal_0_52) 20) (select (m_origin formal_0_52) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_53 () FormalMachine (FormalCallback formal_0_52 boundary_0 (select (m_origin formal_0_52) 20) (select (m_origin formal_0_52) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_54 () FormalMachine (FormalWriteFromOrigin formal_0_53 8 20))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_55 () FormalMachine (FormalWriteFromOrigin formal_0_54 19 3))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_55)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_55) (select (m_origin formal_0_55) 21) (select (m_origin formal_0_55) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_55) (select (m_origin formal_0_55) 21) (select (m_origin formal_0_55) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_56 () FormalMachine (FormalCallback formal_0_55 boundary_0 (select (m_origin formal_0_55) 21) (select (m_origin formal_0_55) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_57 () FormalMachine (FormalWriteFromOrigin formal_0_56 8 21))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_57)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_57) (select (m_origin formal_0_57) 22) (select (m_origin formal_0_57) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_57) (select (m_origin formal_0_57) 22) (select (m_origin formal_0_57) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_58 () FormalMachine (FormalCallback formal_0_57 boundary_0 (select (m_origin formal_0_57) 22) (select (m_origin formal_0_57) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_59 () FormalMachine (FormalWriteFromOrigin formal_0_58 8 22))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_59)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_59) (select (m_origin formal_0_59) 23) (select (m_origin formal_0_59) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_59) (select (m_origin formal_0_59) 23) (select (m_origin formal_0_59) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_60 () FormalMachine (FormalCallback formal_0_59 boundary_0 (select (m_origin formal_0_59) 23) (select (m_origin formal_0_59) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_61 () FormalMachine (FormalWriteFromOrigin formal_0_60 9 23))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_62 () FormalMachine (FormalWriteFromOrigin formal_0_61 22 9))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_62)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_62) (select (m_origin formal_0_62) 24) (select (m_origin formal_0_62) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_62) (select (m_origin formal_0_62) 24) (select (m_origin formal_0_62) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_63 () FormalMachine (FormalCallback formal_0_62 boundary_0 (select (m_origin formal_0_62) 24) (select (m_origin formal_0_62) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_64 () FormalMachine (FormalWriteFromOrigin formal_0_63 9 24))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_64)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_64) (select (m_origin formal_0_64) 25) (select (m_origin formal_0_64) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_64) (select (m_origin formal_0_64) 25) (select (m_origin formal_0_64) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_65 () FormalMachine (FormalCallback formal_0_64 boundary_0 (select (m_origin formal_0_64) 25) (select (m_origin formal_0_64) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_66 () FormalMachine (FormalWriteFromOrigin formal_0_65 9 25))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_66)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_66) (select (m_origin formal_0_66) 26) (select (m_origin formal_0_66) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_66) (select (m_origin formal_0_66) 26) (select (m_origin formal_0_66) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_67 () FormalMachine (FormalCallback formal_0_66 boundary_0 (select (m_origin formal_0_66) 26) (select (m_origin formal_0_66) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_68 () FormalMachine (FormalWriteFromOrigin formal_0_67 10 26))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_69 () FormalMachine (FormalWriteFromOrigin formal_0_68 25 10))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_69)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 27) (select (m_origin formal_0_69) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 27) (select (m_origin formal_0_69) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_70 () FormalMachine (FormalCallback formal_0_69 boundary_0 (select (m_origin formal_0_69) 27) (select (m_origin formal_0_69) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_71 () FormalMachine (FormalWriteFromOrigin formal_0_70 10 27))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_71)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_71) (select (m_origin formal_0_71) 28) (select (m_origin formal_0_71) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_71) (select (m_origin formal_0_71) 28) (select (m_origin formal_0_71) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_72 () FormalMachine (FormalCallback formal_0_71 boundary_0 (select (m_origin formal_0_71) 28) (select (m_origin formal_0_71) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_73 () FormalMachine (FormalWriteFromOrigin formal_0_72 11 28))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_74 () FormalMachine (FormalWriteFromOrigin formal_0_73 27 11))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_74)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_74) (select (m_origin formal_0_74) 29) (select (m_origin formal_0_74) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_74) (select (m_origin formal_0_74) 29) (select (m_origin formal_0_74) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_75 () FormalMachine (FormalCallback formal_0_74 boundary_0 (select (m_origin formal_0_74) 29) (select (m_origin formal_0_74) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_76 () FormalMachine (FormalWriteFromOrigin formal_0_75 11 29))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_76)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_76) (select (m_origin formal_0_76) 30) (select (m_origin formal_0_76) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_76) (select (m_origin formal_0_76) 30) (select (m_origin formal_0_76) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_77 () FormalMachine (FormalCallback formal_0_76 boundary_0 (select (m_origin formal_0_76) 30) (select (m_origin formal_0_76) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_78 () FormalMachine (FormalWriteFromOrigin formal_0_77 11 30))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_78)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 31) (select (m_origin formal_0_78) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 31) (select (m_origin formal_0_78) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_79 () FormalMachine (FormalCallback formal_0_78 boundary_0 (select (m_origin formal_0_78) 31) (select (m_origin formal_0_78) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_80 () FormalMachine (FormalWriteFromOrigin formal_0_79 12 31))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_81 () FormalMachine (FormalWriteFromOrigin formal_0_80 30 6))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_81)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 32) (select (m_origin formal_0_81) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 32) (select (m_origin formal_0_81) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_82 () FormalMachine (FormalCallback formal_0_81 boundary_0 (select (m_origin formal_0_81) 32) (select (m_origin formal_0_81) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_83 () FormalMachine (FormalWriteFromOrigin formal_0_82 12 32))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_83)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_83) (select (m_origin formal_0_83) 33) (select (m_origin formal_0_83) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_83) (select (m_origin formal_0_83) 33) (select (m_origin formal_0_83) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_84 () FormalMachine (FormalCallback formal_0_83 boundary_0 (select (m_origin formal_0_83) 33) (select (m_origin formal_0_83) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_85 () FormalMachine (FormalWriteFromOrigin formal_0_84 13 33))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_86 () FormalMachine (FormalWriteFromOrigin formal_0_85 32 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_86)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 34) (select (m_origin formal_0_86) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 34) (select (m_origin formal_0_86) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_87 () FormalMachine (FormalCallback formal_0_86 boundary_0 (select (m_origin formal_0_86) 34) (select (m_origin formal_0_86) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_88 () FormalMachine (FormalWriteFromOrigin formal_0_87 13 34))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_88)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_88) (select (m_origin formal_0_88) 35) (select (m_origin formal_0_88) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_88) (select (m_origin formal_0_88) 35) (select (m_origin formal_0_88) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_89 () FormalMachine (FormalCallback formal_0_88 boundary_0 (select (m_origin formal_0_88) 35) (select (m_origin formal_0_88) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_90 () FormalMachine (FormalWriteFromOrigin formal_0_89 14 35))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_91 () FormalMachine (FormalWriteFromOrigin formal_0_90 34 7))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_91)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_91) (select (m_origin formal_0_91) 36) (select (m_origin formal_0_91) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_91) (select (m_origin formal_0_91) 36) (select (m_origin formal_0_91) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_92 () FormalMachine (FormalCallback formal_0_91 boundary_0 (select (m_origin formal_0_91) 36) (select (m_origin formal_0_91) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_93 () FormalMachine (FormalWriteFromOrigin formal_0_92 14 36))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_93)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_93) (select (m_origin formal_0_93) 37) (select (m_origin formal_0_93) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_93) (select (m_origin formal_0_93) 37) (select (m_origin formal_0_93) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_94 () FormalMachine (FormalCallback formal_0_93 boundary_0 (select (m_origin formal_0_93) 37) (select (m_origin formal_0_93) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_95 () FormalMachine (FormalWriteFromOrigin formal_0_94 14 37))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_95)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_95) (select (m_origin formal_0_95) 38) (select (m_origin formal_0_95) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_95) (select (m_origin formal_0_95) 38) (select (m_origin formal_0_95) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_96 () FormalMachine (FormalCallback formal_0_95 boundary_0 (select (m_origin formal_0_95) 38) (select (m_origin formal_0_95) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_97 () FormalMachine (FormalWriteFromOrigin formal_0_96 14 38))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_97)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_97) (select (m_origin formal_0_97) 39) (select (m_origin formal_0_97) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_97) (select (m_origin formal_0_97) 39) (select (m_origin formal_0_97) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_98 () FormalMachine (FormalCallback formal_0_97 boundary_0 (select (m_origin formal_0_97) 39) (select (m_origin formal_0_97) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_99 () FormalMachine (FormalWriteFromOrigin formal_0_98 14 39))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_99)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 40) (select (m_origin formal_0_99) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 40) (select (m_origin formal_0_99) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_100 () FormalMachine (FormalCallback formal_0_99 boundary_0 (select (m_origin formal_0_99) 40) (select (m_origin formal_0_99) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_101 () FormalMachine (FormalWriteFromOrigin formal_0_100 15 40))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_102 () FormalMachine (FormalWriteFromOrigin formal_0_101 39 15))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_102)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_102) (select (m_origin formal_0_102) 41) (select (m_origin formal_0_102) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_102) (select (m_origin formal_0_102) 41) (select (m_origin formal_0_102) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_103 () FormalMachine (FormalCallback formal_0_102 boundary_0 (select (m_origin formal_0_102) 41) (select (m_origin formal_0_102) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_104 () FormalMachine (FormalWriteFromOrigin formal_0_103 16 41))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_105 () FormalMachine (FormalWriteFromOrigin formal_0_104 40 16))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_105)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_105) (select (m_origin formal_0_105) 42) (select (m_origin formal_0_105) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_105) (select (m_origin formal_0_105) 42) (select (m_origin formal_0_105) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_106 () FormalMachine (FormalCallback formal_0_105 boundary_0 (select (m_origin formal_0_105) 42) (select (m_origin formal_0_105) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_107 () FormalMachine (FormalWriteFromOrigin formal_0_106 17 42))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_108 () FormalMachine (FormalWriteFromOrigin formal_0_107 41 17))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_108)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_108) (select (m_origin formal_0_108) 43) (select (m_origin formal_0_108) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_108) (select (m_origin formal_0_108) 43) (select (m_origin formal_0_108) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_109 () FormalMachine (FormalCallback formal_0_108 boundary_0 (select (m_origin formal_0_108) 43) (select (m_origin formal_0_108) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_110 () FormalMachine (FormalWriteFromOrigin formal_0_109 17 43))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_110)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_110) (select (m_origin formal_0_110) 44) (select (m_origin formal_0_110) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_110) (select (m_origin formal_0_110) 44) (select (m_origin formal_0_110) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_111 () FormalMachine (FormalCallback formal_0_110 boundary_0 (select (m_origin formal_0_110) 44) (select (m_origin formal_0_110) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_112 () FormalMachine (FormalWriteFromOrigin formal_0_111 17 44))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_112)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_112) (select (m_origin formal_0_112) 45) (select (m_origin formal_0_112) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_112) (select (m_origin formal_0_112) 45) (select (m_origin formal_0_112) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_113 () FormalMachine (FormalCallback formal_0_112 boundary_0 (select (m_origin formal_0_112) 45) (select (m_origin formal_0_112) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_114 () FormalMachine (FormalWriteFromOrigin formal_0_113 17 45))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_114)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_114) (select (m_origin formal_0_114) 46) (select (m_origin formal_0_114) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_114) (select (m_origin formal_0_114) 46) (select (m_origin formal_0_114) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_115 () FormalMachine (FormalCallback formal_0_114 boundary_0 (select (m_origin formal_0_114) 46) (select (m_origin formal_0_114) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_116 () FormalMachine (FormalWriteFromOrigin formal_0_115 17 46))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_116)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_116) (select (m_origin formal_0_116) 47) (select (m_origin formal_0_116) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_116) (select (m_origin formal_0_116) 47) (select (m_origin formal_0_116) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_117 () FormalMachine (FormalCallback formal_0_116 boundary_0 (select (m_origin formal_0_116) 47) (select (m_origin formal_0_116) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_118 () FormalMachine (FormalWriteFromOrigin formal_0_117 17 47))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_118)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_118) (select (m_origin formal_0_118) 48) (select (m_origin formal_0_118) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_118) (select (m_origin formal_0_118) 48) (select (m_origin formal_0_118) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_119 () FormalMachine (FormalCallback formal_0_118 boundary_0 (select (m_origin formal_0_118) 48) (select (m_origin formal_0_118) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_120 () FormalMachine (FormalWriteFromOrigin formal_0_119 18 48))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_121 () FormalMachine (FormalWriteFromOrigin formal_0_120 47 18))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_121)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_121) (select (m_origin formal_0_121) 49) (select (m_origin formal_0_121) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_121) (select (m_origin formal_0_121) 49) (select (m_origin formal_0_121) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_122 () FormalMachine (FormalCallback formal_0_121 boundary_0 (select (m_origin formal_0_121) 49) (select (m_origin formal_0_121) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_123 () FormalMachine (FormalWriteFromOrigin formal_0_122 18 49))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_123)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_123) (select (m_origin formal_0_123) 50) (select (m_origin formal_0_123) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_123) (select (m_origin formal_0_123) 50) (select (m_origin formal_0_123) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_124 () FormalMachine (FormalCallback formal_0_123 boundary_0 (select (m_origin formal_0_123) 50) (select (m_origin formal_0_123) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_125 () FormalMachine (FormalWriteFromOrigin formal_0_124 19 50))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_126 () FormalMachine (FormalWriteFromOrigin formal_0_125 49 3))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_126)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_126) (select (m_origin formal_0_126) 51) (select (m_origin formal_0_126) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_126) (select (m_origin formal_0_126) 51) (select (m_origin formal_0_126) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_127 () FormalMachine (FormalCallback formal_0_126 boundary_0 (select (m_origin formal_0_126) 51) (select (m_origin formal_0_126) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_128 () FormalMachine (FormalWriteFromOrigin formal_0_127 19 51))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_128)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 52) (select (m_origin formal_0_128) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 52) (select (m_origin formal_0_128) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_129 () FormalMachine (FormalCallback formal_0_128 boundary_0 (select (m_origin formal_0_128) 52) (select (m_origin formal_0_128) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_130 () FormalMachine (FormalWriteFromOrigin formal_0_129 20 52))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_131 () FormalMachine (FormalWriteFromOrigin formal_0_130 51 20))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_131)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_131) (select (m_origin formal_0_131) 53) (select (m_origin formal_0_131) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_131) (select (m_origin formal_0_131) 53) (select (m_origin formal_0_131) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_132 () FormalMachine (FormalCallback formal_0_131 boundary_0 (select (m_origin formal_0_131) 53) (select (m_origin formal_0_131) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_133 () FormalMachine (FormalWriteFromOrigin formal_0_132 20 53))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_133)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_133) (select (m_origin formal_0_133) 54) (select (m_origin formal_0_133) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_133) (select (m_origin formal_0_133) 54) (select (m_origin formal_0_133) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_134 () FormalMachine (FormalCallback formal_0_133 boundary_0 (select (m_origin formal_0_133) 54) (select (m_origin formal_0_133) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_135 () FormalMachine (FormalWriteFromOrigin formal_0_134 20 54))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_135)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_135) (select (m_origin formal_0_135) 55) (select (m_origin formal_0_135) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_135) (select (m_origin formal_0_135) 55) (select (m_origin formal_0_135) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_136 () FormalMachine (FormalCallback formal_0_135 boundary_0 (select (m_origin formal_0_135) 55) (select (m_origin formal_0_135) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_137 () FormalMachine (FormalWriteFromOrigin formal_0_136 21 55))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_138 () FormalMachine (FormalWriteFromOrigin formal_0_137 54 21))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_138)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_138) (select (m_origin formal_0_138) 56) (select (m_origin formal_0_138) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_138) (select (m_origin formal_0_138) 56) (select (m_origin formal_0_138) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_139 () FormalMachine (FormalCallback formal_0_138 boundary_0 (select (m_origin formal_0_138) 56) (select (m_origin formal_0_138) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_140 () FormalMachine (FormalWriteFromOrigin formal_0_139 22 56))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_141 () FormalMachine (FormalWriteFromOrigin formal_0_140 55 9))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_141)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_141) (select (m_origin formal_0_141) 57) (select (m_origin formal_0_141) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_141) (select (m_origin formal_0_141) 57) (select (m_origin formal_0_141) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_142 () FormalMachine (FormalCallback formal_0_141 boundary_0 (select (m_origin formal_0_141) 57) (select (m_origin formal_0_141) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_143 () FormalMachine (FormalWriteFromOrigin formal_0_142 22 57))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_143)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_143) (select (m_origin formal_0_143) 58) (select (m_origin formal_0_143) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_143) (select (m_origin formal_0_143) 58) (select (m_origin formal_0_143) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_144 () FormalMachine (FormalCallback formal_0_143 boundary_0 (select (m_origin formal_0_143) 58) (select (m_origin formal_0_143) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_145 () FormalMachine (FormalWriteFromOrigin formal_0_144 22 58))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_145)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_145) (select (m_origin formal_0_145) 59) (select (m_origin formal_0_145) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_145) (select (m_origin formal_0_145) 59) (select (m_origin formal_0_145) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_146 () FormalMachine (FormalCallback formal_0_145 boundary_0 (select (m_origin formal_0_145) 59) (select (m_origin formal_0_145) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_147 () FormalMachine (FormalWriteFromOrigin formal_0_146 23 59))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_148 () FormalMachine (FormalWriteFromOrigin formal_0_147 58 23))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_148)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_148) (select (m_origin formal_0_148) 60) (select (m_origin formal_0_148) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_148) (select (m_origin formal_0_148) 60) (select (m_origin formal_0_148) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_149 () FormalMachine (FormalCallback formal_0_148 boundary_0 (select (m_origin formal_0_148) 60) (select (m_origin formal_0_148) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_150 () FormalMachine (FormalWriteFromOrigin formal_0_149 24 60))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_151 () FormalMachine (FormalWriteFromOrigin formal_0_150 59 24))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_151)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_151) (select (m_origin formal_0_151) 61) (select (m_origin formal_0_151) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_151) (select (m_origin formal_0_151) 61) (select (m_origin formal_0_151) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_152 () FormalMachine (FormalCallback formal_0_151 boundary_0 (select (m_origin formal_0_151) 61) (select (m_origin formal_0_151) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_153 () FormalMachine (FormalWriteFromOrigin formal_0_152 24 61))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_153)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_153) (select (m_origin formal_0_153) 62) (select (m_origin formal_0_153) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_153) (select (m_origin formal_0_153) 62) (select (m_origin formal_0_153) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_154 () FormalMachine (FormalCallback formal_0_153 boundary_0 (select (m_origin formal_0_153) 62) (select (m_origin formal_0_153) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_155 () FormalMachine (FormalWriteFromOrigin formal_0_154 24 62))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_155)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 63) (select (m_origin formal_0_155) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 63) (select (m_origin formal_0_155) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_156 () FormalMachine (FormalCallback formal_0_155 boundary_0 (select (m_origin formal_0_155) 63) (select (m_origin formal_0_155) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_157 () FormalMachine (FormalWriteFromOrigin formal_0_156 24 63))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_157)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_157) (select (m_origin formal_0_157) 64) (select (m_origin formal_0_157) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_157) (select (m_origin formal_0_157) 64) (select (m_origin formal_0_157) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_158 () FormalMachine (FormalCallback formal_0_157 boundary_0 (select (m_origin formal_0_157) 64) (select (m_origin formal_0_157) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_159 () FormalMachine (FormalWriteFromOrigin formal_0_158 24 64))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_159)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_159) (select (m_origin formal_0_159) 65) (select (m_origin formal_0_159) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_159) (select (m_origin formal_0_159) 65) (select (m_origin formal_0_159) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_160 () FormalMachine (FormalCallback formal_0_159 boundary_0 (select (m_origin formal_0_159) 65) (select (m_origin formal_0_159) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_161 () FormalMachine (FormalWriteFromOrigin formal_0_160 25 65))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_162 () FormalMachine (FormalWriteFromOrigin formal_0_161 64 10))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_162)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_162) (select (m_origin formal_0_162) 66) (select (m_origin formal_0_162) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_162) (select (m_origin formal_0_162) 66) (select (m_origin formal_0_162) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_163 () FormalMachine (FormalCallback formal_0_162 boundary_0 (select (m_origin formal_0_162) 66) (select (m_origin formal_0_162) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_164 () FormalMachine (FormalWriteFromOrigin formal_0_163 26 66))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_165 () FormalMachine (FormalWriteFromOrigin formal_0_164 65 26))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_165)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_165) (select (m_origin formal_0_165) 67) (select (m_origin formal_0_165) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_165) (select (m_origin formal_0_165) 67) (select (m_origin formal_0_165) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_166 () FormalMachine (FormalCallback formal_0_165 boundary_0 (select (m_origin formal_0_165) 67) (select (m_origin formal_0_165) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_167 () FormalMachine (FormalWriteFromOrigin formal_0_166 27 67))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_168 () FormalMachine (FormalWriteFromOrigin formal_0_167 66 11))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_168)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_168) (select (m_origin formal_0_168) 68) (select (m_origin formal_0_168) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_168) (select (m_origin formal_0_168) 68) (select (m_origin formal_0_168) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_169 () FormalMachine (FormalCallback formal_0_168 boundary_0 (select (m_origin formal_0_168) 68) (select (m_origin formal_0_168) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_170 () FormalMachine (FormalWriteFromOrigin formal_0_169 27 68))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_170)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_170) (select (m_origin formal_0_170) 69) (select (m_origin formal_0_170) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_170) (select (m_origin formal_0_170) 69) (select (m_origin formal_0_170) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_171 () FormalMachine (FormalCallback formal_0_170 boundary_0 (select (m_origin formal_0_170) 69) (select (m_origin formal_0_170) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_172 () FormalMachine (FormalWriteFromOrigin formal_0_171 27 69))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_172)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_172) (select (m_origin formal_0_172) 70) (select (m_origin formal_0_172) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_172) (select (m_origin formal_0_172) 70) (select (m_origin formal_0_172) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_173 () FormalMachine (FormalCallback formal_0_172 boundary_0 (select (m_origin formal_0_172) 70) (select (m_origin formal_0_172) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_174 () FormalMachine (FormalWriteFromOrigin formal_0_173 27 70))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_174)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_174) (select (m_origin formal_0_174) 71) (select (m_origin formal_0_174) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_174) (select (m_origin formal_0_174) 71) (select (m_origin formal_0_174) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_175 () FormalMachine (FormalCallback formal_0_174 boundary_0 (select (m_origin formal_0_174) 71) (select (m_origin formal_0_174) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_176 () FormalMachine (FormalWriteFromOrigin formal_0_175 27 71))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_176)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 72) (select (m_origin formal_0_176) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 72) (select (m_origin formal_0_176) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_177 () FormalMachine (FormalCallback formal_0_176 boundary_0 (select (m_origin formal_0_176) 72) (select (m_origin formal_0_176) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_178 () FormalMachine (FormalWriteFromOrigin formal_0_177 28 72))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_179 () FormalMachine (FormalWriteFromOrigin formal_0_178 71 28))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_179)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_179) (select (m_origin formal_0_179) 73) (select (m_origin formal_0_179) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_179) (select (m_origin formal_0_179) 73) (select (m_origin formal_0_179) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_180 () FormalMachine (FormalCallback formal_0_179 boundary_0 (select (m_origin formal_0_179) 73) (select (m_origin formal_0_179) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_181 () FormalMachine (FormalWriteFromOrigin formal_0_180 28 73))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_181)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_181) (select (m_origin formal_0_181) 74) (select (m_origin formal_0_181) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_181) (select (m_origin formal_0_181) 74) (select (m_origin formal_0_181) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_182 () FormalMachine (FormalCallback formal_0_181 boundary_0 (select (m_origin formal_0_181) 74) (select (m_origin formal_0_181) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_183 () FormalMachine (FormalWriteFromOrigin formal_0_182 28 74))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_183)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_183) (select (m_origin formal_0_183) 75) (select (m_origin formal_0_183) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_183) (select (m_origin formal_0_183) 75) (select (m_origin formal_0_183) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_184 () FormalMachine (FormalCallback formal_0_183 boundary_0 (select (m_origin formal_0_183) 75) (select (m_origin formal_0_183) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_185 () FormalMachine (FormalWriteFromOrigin formal_0_184 28 75))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_185)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_185) (select (m_origin formal_0_185) 76) (select (m_origin formal_0_185) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_185) (select (m_origin formal_0_185) 76) (select (m_origin formal_0_185) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_186 () FormalMachine (FormalCallback formal_0_185 boundary_0 (select (m_origin formal_0_185) 76) (select (m_origin formal_0_185) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_187 () FormalMachine (FormalWriteFromOrigin formal_0_186 28 76))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_187)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_187) (select (m_origin formal_0_187) 77) (select (m_origin formal_0_187) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_187) (select (m_origin formal_0_187) 77) (select (m_origin formal_0_187) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_188 () FormalMachine (FormalCallback formal_0_187 boundary_0 (select (m_origin formal_0_187) 77) (select (m_origin formal_0_187) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_189 () FormalMachine (FormalWriteFromOrigin formal_0_188 28 77))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_189)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_189) (select (m_origin formal_0_189) 78) (select (m_origin formal_0_189) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_189) (select (m_origin formal_0_189) 78) (select (m_origin formal_0_189) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_190 () FormalMachine (FormalCallback formal_0_189 boundary_0 (select (m_origin formal_0_189) 78) (select (m_origin formal_0_189) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_191 () FormalMachine (FormalWriteFromOrigin formal_0_190 28 78))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_191)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_191) (select (m_origin formal_0_191) 79) (select (m_origin formal_0_191) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_191) (select (m_origin formal_0_191) 79) (select (m_origin formal_0_191) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_192 () FormalMachine (FormalCallback formal_0_191 boundary_0 (select (m_origin formal_0_191) 79) (select (m_origin formal_0_191) 0)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_193 () FormalMachine (FormalWriteFromOrigin formal_0_192 28 79))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_193)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_193) (select (m_origin formal_0_193) 1) (select (m_origin formal_0_193) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_193) (select (m_origin formal_0_193) 1) (select (m_origin formal_0_193) 0)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_194 () FormalMachine (FormalCallback formal_0_193 boundary_0 (select (m_origin formal_0_193) 1) (select (m_origin formal_0_193) 0)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_195 () FormalMachine (FormalWriteFromOrigin formal_0_194 29 1))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_196 () FormalMachine (FormalWriteFromOrigin formal_0_195 79 29))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_197 () FormalMachine (FormalSwap formal_0_196 0 28))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_197)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_197) (select (m_origin formal_0_197) 79) (select (m_origin formal_0_197) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_197) (select (m_origin formal_0_197) 79) (select (m_origin formal_0_197) 32)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_198 () FormalMachine (FormalCallback formal_0_197 boundary_0 (select (m_origin formal_0_197) 79) (select (m_origin formal_0_197) 32)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_198)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_198) (select (m_origin formal_0_198) 79) (select (m_origin formal_0_198) 55)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_198) (select (m_origin formal_0_198) 79) (select (m_origin formal_0_198) 55)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_199 () FormalMachine (FormalCallback formal_0_198 boundary_0 (select (m_origin formal_0_198) 79) (select (m_origin formal_0_198) 55)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_199)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_199) (select (m_origin formal_0_199) 32) (select (m_origin formal_0_199) 55)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_199) (select (m_origin formal_0_199) 32) (select (m_origin formal_0_199) 55)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_200 () FormalMachine (FormalCallback formal_0_199 boundary_0 (select (m_origin formal_0_199) 32) (select (m_origin formal_0_199) 55)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_201 () FormalMachine (FormalSwap formal_0_200 0 12))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_201)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_201) (select (m_origin formal_0_201) 4) (select (m_origin formal_0_201) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_201) (select (m_origin formal_0_201) 4) (select (m_origin formal_0_201) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_202 () FormalMachine (FormalCallback formal_0_201 boundary_0 (select (m_origin formal_0_201) 4) (select (m_origin formal_0_201) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_203 () FormalMachine (FormalWriteFromOrigin formal_0_202 1 4))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_203)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_203) (select (m_origin formal_0_203) 5) (select (m_origin formal_0_203) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_203) (select (m_origin formal_0_203) 5) (select (m_origin formal_0_203) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_204 () FormalMachine (FormalCallback formal_0_203 boundary_0 (select (m_origin formal_0_203) 5) (select (m_origin formal_0_203) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_205 () FormalMachine (FormalWriteFromOrigin formal_0_204 2 5))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_205)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_205) (select (m_origin formal_0_205) 8) (select (m_origin formal_0_205) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_205) (select (m_origin formal_0_205) 8) (select (m_origin formal_0_205) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_206 () FormalMachine (FormalCallback formal_0_205 boundary_0 (select (m_origin formal_0_205) 8) (select (m_origin formal_0_205) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_207 () FormalMachine (FormalWriteFromOrigin formal_0_206 2 8))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_207)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_207) (select (m_origin formal_0_207) 12) (select (m_origin formal_0_207) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_207) (select (m_origin formal_0_207) 12) (select (m_origin formal_0_207) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_208 () FormalMachine (FormalCallback formal_0_207 boundary_0 (select (m_origin formal_0_207) 12) (select (m_origin formal_0_207) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_209 () FormalMachine (FormalWriteFromOrigin formal_0_208 3 12))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_210 () FormalMachine (FormalWriteFromOrigin formal_0_209 4 5))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_210)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_210) (select (m_origin formal_0_210) 14) (select (m_origin formal_0_210) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_210) (select (m_origin formal_0_210) 14) (select (m_origin formal_0_210) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_211 () FormalMachine (FormalCallback formal_0_210 boundary_0 (select (m_origin formal_0_210) 14) (select (m_origin formal_0_210) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_212 () FormalMachine (FormalWriteFromOrigin formal_0_211 3 14))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_212)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_212) (select (m_origin formal_0_212) 19) (select (m_origin formal_0_212) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_212) (select (m_origin formal_0_212) 19) (select (m_origin formal_0_212) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_213 () FormalMachine (FormalCallback formal_0_212 boundary_0 (select (m_origin formal_0_212) 19) (select (m_origin formal_0_212) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_214 () FormalMachine (FormalWriteFromOrigin formal_0_213 3 19))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_214)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_214) (select (m_origin formal_0_214) 22) (select (m_origin formal_0_214) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_214) (select (m_origin formal_0_214) 22) (select (m_origin formal_0_214) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_215 () FormalMachine (FormalCallback formal_0_214 boundary_0 (select (m_origin formal_0_214) 22) (select (m_origin formal_0_214) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_216 () FormalMachine (FormalWriteFromOrigin formal_0_215 4 22))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_217 () FormalMachine (FormalWriteFromOrigin formal_0_216 7 5))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_217)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_217) (select (m_origin formal_0_217) 25) (select (m_origin formal_0_217) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_217) (select (m_origin formal_0_217) 25) (select (m_origin formal_0_217) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_218 () FormalMachine (FormalCallback formal_0_217 boundary_0 (select (m_origin formal_0_217) 25) (select (m_origin formal_0_217) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_219 () FormalMachine (FormalWriteFromOrigin formal_0_218 5 25))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_220 () FormalMachine (FormalWriteFromOrigin formal_0_219 8 12))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_220)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_220) (select (m_origin formal_0_220) 27) (select (m_origin formal_0_220) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_220) (select (m_origin formal_0_220) 27) (select (m_origin formal_0_220) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_221 () FormalMachine (FormalCallback formal_0_220 boundary_0 (select (m_origin formal_0_220) 27) (select (m_origin formal_0_220) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_222 () FormalMachine (FormalWriteFromOrigin formal_0_221 5 27))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_222)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_222) (select (m_origin formal_0_222) 30) (select (m_origin formal_0_222) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_222) (select (m_origin formal_0_222) 30) (select (m_origin formal_0_222) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_223 () FormalMachine (FormalCallback formal_0_222 boundary_0 (select (m_origin formal_0_222) 30) (select (m_origin formal_0_222) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_224 () FormalMachine (FormalWriteFromOrigin formal_0_223 6 30))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_225 () FormalMachine (FormalWriteFromOrigin formal_0_224 10 14))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_225)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_225) (select (m_origin formal_0_225) 79) (select (m_origin formal_0_225) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_225) (select (m_origin formal_0_225) 79) (select (m_origin formal_0_225) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_226 () FormalMachine (FormalCallback formal_0_225 boundary_0 (select (m_origin formal_0_225) 79) (select (m_origin formal_0_225) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_227 () FormalMachine (FormalWriteFromOrigin formal_0_226 6 79))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_227)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_227) (select (m_origin formal_0_227) 34) (select (m_origin formal_0_227) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_227) (select (m_origin formal_0_227) 34) (select (m_origin formal_0_227) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_228 () FormalMachine (FormalCallback formal_0_227 boundary_0 (select (m_origin formal_0_227) 34) (select (m_origin formal_0_227) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_229 () FormalMachine (FormalWriteFromOrigin formal_0_228 6 34))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_229)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_229) (select (m_origin formal_0_229) 39) (select (m_origin formal_0_229) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_229) (select (m_origin formal_0_229) 39) (select (m_origin formal_0_229) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_230 () FormalMachine (FormalCallback formal_0_229 boundary_0 (select (m_origin formal_0_229) 39) (select (m_origin formal_0_229) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_231 () FormalMachine (FormalWriteFromOrigin formal_0_230 7 39))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_232 () FormalMachine (FormalWriteFromOrigin formal_0_231 13 5))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_232)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_232) (select (m_origin formal_0_232) 40) (select (m_origin formal_0_232) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_232) (select (m_origin formal_0_232) 40) (select (m_origin formal_0_232) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_233 () FormalMachine (FormalCallback formal_0_232 boundary_0 (select (m_origin formal_0_232) 40) (select (m_origin formal_0_232) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_234 () FormalMachine (FormalWriteFromOrigin formal_0_233 7 40))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_234)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_234) (select (m_origin formal_0_234) 41) (select (m_origin formal_0_234) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_234) (select (m_origin formal_0_234) 41) (select (m_origin formal_0_234) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_235 () FormalMachine (FormalCallback formal_0_234 boundary_0 (select (m_origin formal_0_234) 41) (select (m_origin formal_0_234) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_236 () FormalMachine (FormalWriteFromOrigin formal_0_235 8 41))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_237 () FormalMachine (FormalWriteFromOrigin formal_0_236 15 12))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_237)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_237) (select (m_origin formal_0_237) 47) (select (m_origin formal_0_237) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_237) (select (m_origin formal_0_237) 47) (select (m_origin formal_0_237) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_238 () FormalMachine (FormalCallback formal_0_237 boundary_0 (select (m_origin formal_0_237) 47) (select (m_origin formal_0_237) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_239 () FormalMachine (FormalWriteFromOrigin formal_0_238 8 47))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_239)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_239) (select (m_origin formal_0_239) 49) (select (m_origin formal_0_239) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_239) (select (m_origin formal_0_239) 49) (select (m_origin formal_0_239) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_240 () FormalMachine (FormalCallback formal_0_239 boundary_0 (select (m_origin formal_0_239) 49) (select (m_origin formal_0_239) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_241 () FormalMachine (FormalWriteFromOrigin formal_0_240 9 49))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_242 () FormalMachine (FormalWriteFromOrigin formal_0_241 17 25))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_242)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_242) (select (m_origin formal_0_242) 51) (select (m_origin formal_0_242) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_242) (select (m_origin formal_0_242) 51) (select (m_origin formal_0_242) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_243 () FormalMachine (FormalCallback formal_0_242 boundary_0 (select (m_origin formal_0_242) 51) (select (m_origin formal_0_242) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_244 () FormalMachine (FormalWriteFromOrigin formal_0_243 10 51))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_245 () FormalMachine (FormalWriteFromOrigin formal_0_244 18 14))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_245)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_245) (select (m_origin formal_0_245) 54) (select (m_origin formal_0_245) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_245) (select (m_origin formal_0_245) 54) (select (m_origin formal_0_245) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_246 () FormalMachine (FormalCallback formal_0_245 boundary_0 (select (m_origin formal_0_245) 54) (select (m_origin formal_0_245) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_247 () FormalMachine (FormalWriteFromOrigin formal_0_246 10 54))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_247)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_247) (select (m_origin formal_0_247) 55) (select (m_origin formal_0_247) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_247) (select (m_origin formal_0_247) 55) (select (m_origin formal_0_247) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_248 () FormalMachine (FormalCallback formal_0_247 boundary_0 (select (m_origin formal_0_247) 55) (select (m_origin formal_0_247) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_249 () FormalMachine (FormalWriteFromOrigin formal_0_248 11 55))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_250 () FormalMachine (FormalWriteFromOrigin formal_0_249 20 30))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_250)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_250) (select (m_origin formal_0_250) 58) (select (m_origin formal_0_250) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_250) (select (m_origin formal_0_250) 58) (select (m_origin formal_0_250) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_251 () FormalMachine (FormalCallback formal_0_250 boundary_0 (select (m_origin formal_0_250) 58) (select (m_origin formal_0_250) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_252 () FormalMachine (FormalWriteFromOrigin formal_0_251 11 58))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_252)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_252) (select (m_origin formal_0_252) 59) (select (m_origin formal_0_252) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_252) (select (m_origin formal_0_252) 59) (select (m_origin formal_0_252) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_253 () FormalMachine (FormalCallback formal_0_252 boundary_0 (select (m_origin formal_0_252) 59) (select (m_origin formal_0_252) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_254 () FormalMachine (FormalWriteFromOrigin formal_0_253 12 59))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_255 () FormalMachine (FormalWriteFromOrigin formal_0_254 22 79))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_255)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_255) (select (m_origin formal_0_255) 64) (select (m_origin formal_0_255) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_255) (select (m_origin formal_0_255) 64) (select (m_origin formal_0_255) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_256 () FormalMachine (FormalCallback formal_0_255 boundary_0 (select (m_origin formal_0_255) 64) (select (m_origin formal_0_255) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_257 () FormalMachine (FormalWriteFromOrigin formal_0_256 12 64))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_257)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_257) (select (m_origin formal_0_257) 65) (select (m_origin formal_0_257) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_257) (select (m_origin formal_0_257) 65) (select (m_origin formal_0_257) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_258 () FormalMachine (FormalCallback formal_0_257 boundary_0 (select (m_origin formal_0_257) 65) (select (m_origin formal_0_257) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_259 () FormalMachine (FormalWriteFromOrigin formal_0_258 13 65))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_260 () FormalMachine (FormalWriteFromOrigin formal_0_259 24 5))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_260)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_260) (select (m_origin formal_0_260) 66) (select (m_origin formal_0_260) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_260) (select (m_origin formal_0_260) 66) (select (m_origin formal_0_260) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_261 () FormalMachine (FormalCallback formal_0_260 boundary_0 (select (m_origin formal_0_260) 66) (select (m_origin formal_0_260) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_262 () FormalMachine (FormalWriteFromOrigin formal_0_261 13 66))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_262)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_262) (select (m_origin formal_0_262) 71) (select (m_origin formal_0_262) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_262) (select (m_origin formal_0_262) 71) (select (m_origin formal_0_262) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_263 () FormalMachine (FormalCallback formal_0_262 boundary_0 (select (m_origin formal_0_262) 71) (select (m_origin formal_0_262) 32)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_264 () FormalMachine (FormalWriteFromOrigin formal_0_263 14 71))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_265 () FormalMachine (FormalWriteFromOrigin formal_0_264 26 39))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_265)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_265) (select (m_origin formal_0_265) 2) (select (m_origin formal_0_265) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_265) (select (m_origin formal_0_265) 2) (select (m_origin formal_0_265) 32)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_266 () FormalMachine (FormalCallback formal_0_265 boundary_0 (select (m_origin formal_0_265) 2) (select (m_origin formal_0_265) 32)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_267 () FormalMachine (FormalWriteFromOrigin formal_0_266 14 2))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_268 () FormalMachine (FormalSwap formal_0_267 0 14))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:1]:initial-compare
(assert (not (m_panicked formal_0_268)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_268) (select (m_origin formal_0_268) 4) (select (m_origin formal_0_268) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_268) (select (m_origin formal_0_268) 4) (select (m_origin formal_0_268) 2)) false))
; source callback transition phase=insert-tail[0:14:1]:initial-compare
(define-fun formal_0_269 () FormalMachine (FormalCallback formal_0_268 boundary_0 (select (m_origin formal_0_268) 4) (select (m_origin formal_0_268) 2)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:2]:initial-compare
(assert (not (m_panicked formal_0_269)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_269) (select (m_origin formal_0_269) 8) (select (m_origin formal_0_269) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_269) (select (m_origin formal_0_269) 8) (select (m_origin formal_0_269) 4)) false))
; source callback transition phase=insert-tail[0:14:2]:initial-compare
(define-fun formal_0_270 () FormalMachine (FormalCallback formal_0_269 boundary_0 (select (m_origin formal_0_269) 8) (select (m_origin formal_0_269) 4)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:3]:initial-compare
(assert (not (m_panicked formal_0_270)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_270) (select (m_origin formal_0_270) 19) (select (m_origin formal_0_270) 8)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_270) (select (m_origin formal_0_270) 19) (select (m_origin formal_0_270) 8)) false))
; source callback transition phase=insert-tail[0:14:3]:initial-compare
(define-fun formal_0_271 () FormalMachine (FormalCallback formal_0_270 boundary_0 (select (m_origin formal_0_270) 19) (select (m_origin formal_0_270) 8)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:4]:initial-compare
(assert (not (m_panicked formal_0_271)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_271) (select (m_origin formal_0_271) 22) (select (m_origin formal_0_271) 19)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_271) (select (m_origin formal_0_271) 22) (select (m_origin formal_0_271) 19)) false))
; source callback transition phase=insert-tail[0:14:4]:initial-compare
(define-fun formal_0_272 () FormalMachine (FormalCallback formal_0_271 boundary_0 (select (m_origin formal_0_271) 22) (select (m_origin formal_0_271) 19)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:5]:initial-compare
(assert (not (m_panicked formal_0_272)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_272) (select (m_origin formal_0_272) 27) (select (m_origin formal_0_272) 22)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_272) (select (m_origin formal_0_272) 27) (select (m_origin formal_0_272) 22)) false))
; source callback transition phase=insert-tail[0:14:5]:initial-compare
(define-fun formal_0_273 () FormalMachine (FormalCallback formal_0_272 boundary_0 (select (m_origin formal_0_272) 27) (select (m_origin formal_0_272) 22)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:6]:initial-compare
(assert (not (m_panicked formal_0_273)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_273) (select (m_origin formal_0_273) 34) (select (m_origin formal_0_273) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_273) (select (m_origin formal_0_273) 34) (select (m_origin formal_0_273) 27)) false))
; source callback transition phase=insert-tail[0:14:6]:initial-compare
(define-fun formal_0_274 () FormalMachine (FormalCallback formal_0_273 boundary_0 (select (m_origin formal_0_273) 34) (select (m_origin formal_0_273) 27)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:7]:initial-compare
(assert (not (m_panicked formal_0_274)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_274) (select (m_origin formal_0_274) 40) (select (m_origin formal_0_274) 34)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_274) (select (m_origin formal_0_274) 40) (select (m_origin formal_0_274) 34)) false))
; source callback transition phase=insert-tail[0:14:7]:initial-compare
(define-fun formal_0_275 () FormalMachine (FormalCallback formal_0_274 boundary_0 (select (m_origin formal_0_274) 40) (select (m_origin formal_0_274) 34)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:8]:initial-compare
(assert (not (m_panicked formal_0_275)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_275) (select (m_origin formal_0_275) 47) (select (m_origin formal_0_275) 40)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_275) (select (m_origin formal_0_275) 47) (select (m_origin formal_0_275) 40)) false))
; source callback transition phase=insert-tail[0:14:8]:initial-compare
(define-fun formal_0_276 () FormalMachine (FormalCallback formal_0_275 boundary_0 (select (m_origin formal_0_275) 47) (select (m_origin formal_0_275) 40)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:9]:initial-compare
(assert (not (m_panicked formal_0_276)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_276) (select (m_origin formal_0_276) 49) (select (m_origin formal_0_276) 47)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_276) (select (m_origin formal_0_276) 49) (select (m_origin formal_0_276) 47)) false))
; source callback transition phase=insert-tail[0:14:9]:initial-compare
(define-fun formal_0_277 () FormalMachine (FormalCallback formal_0_276 boundary_0 (select (m_origin formal_0_276) 49) (select (m_origin formal_0_276) 47)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:10]:initial-compare
(assert (not (m_panicked formal_0_277)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_277) (select (m_origin formal_0_277) 54) (select (m_origin formal_0_277) 49)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_277) (select (m_origin formal_0_277) 54) (select (m_origin formal_0_277) 49)) false))
; source callback transition phase=insert-tail[0:14:10]:initial-compare
(define-fun formal_0_278 () FormalMachine (FormalCallback formal_0_277 boundary_0 (select (m_origin formal_0_277) 54) (select (m_origin formal_0_277) 49)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:11]:initial-compare
(assert (not (m_panicked formal_0_278)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_278) (select (m_origin formal_0_278) 58) (select (m_origin formal_0_278) 54)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_278) (select (m_origin formal_0_278) 58) (select (m_origin formal_0_278) 54)) false))
; source callback transition phase=insert-tail[0:14:11]:initial-compare
(define-fun formal_0_279 () FormalMachine (FormalCallback formal_0_278 boundary_0 (select (m_origin formal_0_278) 58) (select (m_origin formal_0_278) 54)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:12]:initial-compare
(assert (not (m_panicked formal_0_279)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_279) (select (m_origin formal_0_279) 64) (select (m_origin formal_0_279) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_279) (select (m_origin formal_0_279) 64) (select (m_origin formal_0_279) 58)) false))
; source callback transition phase=insert-tail[0:14:12]:initial-compare
(define-fun formal_0_280 () FormalMachine (FormalCallback formal_0_279 boundary_0 (select (m_origin formal_0_279) 64) (select (m_origin formal_0_279) 58)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[0:14:13]:initial-compare
(assert (not (m_panicked formal_0_280)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_280) (select (m_origin formal_0_280) 66) (select (m_origin formal_0_280) 64)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_280) (select (m_origin formal_0_280) 66) (select (m_origin formal_0_280) 64)) false))
; source callback transition phase=insert-tail[0:14:13]:initial-compare
(define-fun formal_0_281 () FormalMachine (FormalCallback formal_0_280 boundary_0 (select (m_origin formal_0_280) 66) (select (m_origin formal_0_280) 64)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:1]:initial-compare
(assert (not (m_panicked formal_0_281)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_281) (select (m_origin formal_0_281) 41) (select (m_origin formal_0_281) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_281) (select (m_origin formal_0_281) 41) (select (m_origin formal_0_281) 12)) false))
; source callback transition phase=insert-tail[15:28:1]:initial-compare
(define-fun formal_0_282 () FormalMachine (FormalCallback formal_0_281 boundary_0 (select (m_origin formal_0_281) 41) (select (m_origin formal_0_281) 12)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:2]:initial-compare
(assert (not (m_panicked formal_0_282)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_282) (select (m_origin formal_0_282) 25) (select (m_origin formal_0_282) 41)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_282) (select (m_origin formal_0_282) 25) (select (m_origin formal_0_282) 41)) false))
; source callback transition phase=insert-tail[15:28:2]:initial-compare
(define-fun formal_0_283 () FormalMachine (FormalCallback formal_0_282 boundary_0 (select (m_origin formal_0_282) 25) (select (m_origin formal_0_282) 41)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:3]:initial-compare
(assert (not (m_panicked formal_0_283)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_283) (select (m_origin formal_0_283) 14) (select (m_origin formal_0_283) 25)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_283) (select (m_origin formal_0_283) 14) (select (m_origin formal_0_283) 25)) false))
; source callback transition phase=insert-tail[15:28:3]:initial-compare
(define-fun formal_0_284 () FormalMachine (FormalCallback formal_0_283 boundary_0 (select (m_origin formal_0_283) 14) (select (m_origin formal_0_283) 25)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:4]:initial-compare
(assert (not (m_panicked formal_0_284)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_284) (select (m_origin formal_0_284) 51) (select (m_origin formal_0_284) 14)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_284) (select (m_origin formal_0_284) 51) (select (m_origin formal_0_284) 14)) false))
; source callback transition phase=insert-tail[15:28:4]:initial-compare
(define-fun formal_0_285 () FormalMachine (FormalCallback formal_0_284 boundary_0 (select (m_origin formal_0_284) 51) (select (m_origin formal_0_284) 14)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:5]:initial-compare
(assert (not (m_panicked formal_0_285)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_285) (select (m_origin formal_0_285) 30) (select (m_origin formal_0_285) 51)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_285) (select (m_origin formal_0_285) 30) (select (m_origin formal_0_285) 51)) false))
; source callback transition phase=insert-tail[15:28:5]:initial-compare
(define-fun formal_0_286 () FormalMachine (FormalCallback formal_0_285 boundary_0 (select (m_origin formal_0_285) 30) (select (m_origin formal_0_285) 51)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:6]:initial-compare
(assert (not (m_panicked formal_0_286)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 55) (select (m_origin formal_0_286) 30)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 55) (select (m_origin formal_0_286) 30)) false))
; source callback transition phase=insert-tail[15:28:6]:initial-compare
(define-fun formal_0_287 () FormalMachine (FormalCallback formal_0_286 boundary_0 (select (m_origin formal_0_286) 55) (select (m_origin formal_0_286) 30)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:7]:initial-compare
(assert (not (m_panicked formal_0_287)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_287) (select (m_origin formal_0_287) 79) (select (m_origin formal_0_287) 55)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_287) (select (m_origin formal_0_287) 79) (select (m_origin formal_0_287) 55)) false))
; source callback transition phase=insert-tail[15:28:7]:initial-compare
(define-fun formal_0_288 () FormalMachine (FormalCallback formal_0_287 boundary_0 (select (m_origin formal_0_287) 79) (select (m_origin formal_0_287) 55)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:8]:initial-compare
(assert (not (m_panicked formal_0_288)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 59) (select (m_origin formal_0_288) 79)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 59) (select (m_origin formal_0_288) 79)) false))
; source callback transition phase=insert-tail[15:28:8]:initial-compare
(define-fun formal_0_289 () FormalMachine (FormalCallback formal_0_288 boundary_0 (select (m_origin formal_0_288) 59) (select (m_origin formal_0_288) 79)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:9]:initial-compare
(assert (not (m_panicked formal_0_289)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_289) (select (m_origin formal_0_289) 5) (select (m_origin formal_0_289) 59)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_289) (select (m_origin formal_0_289) 5) (select (m_origin formal_0_289) 59)) false))
; source callback transition phase=insert-tail[15:28:9]:initial-compare
(define-fun formal_0_290 () FormalMachine (FormalCallback formal_0_289 boundary_0 (select (m_origin formal_0_289) 5) (select (m_origin formal_0_289) 59)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:10]:initial-compare
(assert (not (m_panicked formal_0_290)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_290) (select (m_origin formal_0_290) 65) (select (m_origin formal_0_290) 5)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_290) (select (m_origin formal_0_290) 65) (select (m_origin formal_0_290) 5)) false))
; source callback transition phase=insert-tail[15:28:10]:initial-compare
(define-fun formal_0_291 () FormalMachine (FormalCallback formal_0_290 boundary_0 (select (m_origin formal_0_290) 65) (select (m_origin formal_0_290) 5)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:11]:initial-compare
(assert (not (m_panicked formal_0_291)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_291) (select (m_origin formal_0_291) 39) (select (m_origin formal_0_291) 65)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_291) (select (m_origin formal_0_291) 39) (select (m_origin formal_0_291) 65)) false))
; source callback transition phase=insert-tail[15:28:11]:initial-compare
(define-fun formal_0_292 () FormalMachine (FormalCallback formal_0_291 boundary_0 (select (m_origin formal_0_291) 39) (select (m_origin formal_0_291) 65)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[15:28:12]:initial-compare
(assert (not (m_panicked formal_0_292)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 71) (select (m_origin formal_0_292) 39)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 71) (select (m_origin formal_0_292) 39)) false))
; source callback transition phase=insert-tail[15:28:12]:initial-compare
(define-fun formal_0_293 () FormalMachine (FormalCallback formal_0_292 boundary_0 (select (m_origin formal_0_292) 71) (select (m_origin formal_0_292) 39)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_293)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_293) (select (m_origin formal_0_293) 1) (select (m_origin formal_0_293) 53)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_293) (select (m_origin formal_0_293) 1) (select (m_origin formal_0_293) 53)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_294 () FormalMachine (FormalCallback formal_0_293 boundary_0 (select (m_origin formal_0_293) 1) (select (m_origin formal_0_293) 53)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_294)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_294) (select (m_origin formal_0_294) 1) (select (m_origin formal_0_294) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_294) (select (m_origin formal_0_294) 1) (select (m_origin formal_0_294) 28)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_295 () FormalMachine (FormalCallback formal_0_294 boundary_0 (select (m_origin formal_0_294) 1) (select (m_origin formal_0_294) 28)))
; source callback case=duplicate-class-ancestor-pivot phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_295)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_295) (select (m_origin formal_0_295) 0) (select (m_origin formal_0_295) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_295) (select (m_origin formal_0_295) 0) (select (m_origin formal_0_295) 1)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_296 () FormalMachine (FormalCallback formal_0_295 boundary_0 (select (m_origin formal_0_295) 0) (select (m_origin formal_0_295) 1)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_297 () FormalMachine (FormalSwap formal_0_296 29 29))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_297)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_297) (select (m_origin formal_0_297) 1) (select (m_origin formal_0_297) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_297) (select (m_origin formal_0_297) 1) (select (m_origin formal_0_297) 31)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_298 () FormalMachine (FormalCallback formal_0_297 boundary_0 (select (m_origin formal_0_297) 1) (select (m_origin formal_0_297) 31)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_299 () FormalMachine (FormalWriteFromOrigin formal_0_298 30 31))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_299)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_299) (select (m_origin formal_0_299) 1) (select (m_origin formal_0_299) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_299) (select (m_origin formal_0_299) 1) (select (m_origin formal_0_299) 13)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_300 () FormalMachine (FormalCallback formal_0_299 boundary_0 (select (m_origin formal_0_299) 1) (select (m_origin formal_0_299) 13)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_301 () FormalMachine (FormalWriteFromOrigin formal_0_300 30 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_301)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_301) (select (m_origin formal_0_301) 1) (select (m_origin formal_0_301) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_301) (select (m_origin formal_0_301) 1) (select (m_origin formal_0_301) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_302 () FormalMachine (FormalCallback formal_0_301 boundary_0 (select (m_origin formal_0_301) 1) (select (m_origin formal_0_301) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_303 () FormalMachine (FormalWriteFromOrigin formal_0_302 30 33))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_303)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_303) (select (m_origin formal_0_303) 1) (select (m_origin formal_0_303) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_303) (select (m_origin formal_0_303) 1) (select (m_origin formal_0_303) 7)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_304 () FormalMachine (FormalCallback formal_0_303 boundary_0 (select (m_origin formal_0_303) 1) (select (m_origin formal_0_303) 7)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_305 () FormalMachine (FormalWriteFromOrigin formal_0_304 30 7))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_305)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_305) (select (m_origin formal_0_305) 1) (select (m_origin formal_0_305) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_305) (select (m_origin formal_0_305) 1) (select (m_origin formal_0_305) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_306 () FormalMachine (FormalCallback formal_0_305 boundary_0 (select (m_origin formal_0_305) 1) (select (m_origin formal_0_305) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_307 () FormalMachine (FormalWriteFromOrigin formal_0_306 30 35))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_307)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_307) (select (m_origin formal_0_307) 1) (select (m_origin formal_0_307) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_307) (select (m_origin formal_0_307) 1) (select (m_origin formal_0_307) 36)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_308 () FormalMachine (FormalCallback formal_0_307 boundary_0 (select (m_origin formal_0_307) 1) (select (m_origin formal_0_307) 36)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_309 () FormalMachine (FormalWriteFromOrigin formal_0_308 30 36))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_309)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_309) (select (m_origin formal_0_309) 1) (select (m_origin formal_0_309) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_309) (select (m_origin formal_0_309) 1) (select (m_origin formal_0_309) 37)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_310 () FormalMachine (FormalCallback formal_0_309 boundary_0 (select (m_origin formal_0_309) 1) (select (m_origin formal_0_309) 37)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_311 () FormalMachine (FormalWriteFromOrigin formal_0_310 30 37))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_311)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_311) (select (m_origin formal_0_311) 1) (select (m_origin formal_0_311) 38)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_311) (select (m_origin formal_0_311) 1) (select (m_origin formal_0_311) 38)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_312 () FormalMachine (FormalCallback formal_0_311 boundary_0 (select (m_origin formal_0_311) 1) (select (m_origin formal_0_311) 38)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_313 () FormalMachine (FormalWriteFromOrigin formal_0_312 30 38))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_313)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_313) (select (m_origin formal_0_313) 1) (select (m_origin formal_0_313) 15)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_313) (select (m_origin formal_0_313) 1) (select (m_origin formal_0_313) 15)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_314 () FormalMachine (FormalCallback formal_0_313 boundary_0 (select (m_origin formal_0_313) 1) (select (m_origin formal_0_313) 15)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_315 () FormalMachine (FormalWriteFromOrigin formal_0_314 30 15))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_315)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_315) (select (m_origin formal_0_315) 1) (select (m_origin formal_0_315) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_315) (select (m_origin formal_0_315) 1) (select (m_origin formal_0_315) 16)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_316 () FormalMachine (FormalCallback formal_0_315 boundary_0 (select (m_origin formal_0_315) 1) (select (m_origin formal_0_315) 16)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_317 () FormalMachine (FormalWriteFromOrigin formal_0_316 31 16))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_318 () FormalMachine (FormalWriteFromOrigin formal_0_317 39 31))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_318)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_318) (select (m_origin formal_0_318) 1) (select (m_origin formal_0_318) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_318) (select (m_origin formal_0_318) 1) (select (m_origin formal_0_318) 17)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_319 () FormalMachine (FormalCallback formal_0_318 boundary_0 (select (m_origin formal_0_318) 1) (select (m_origin formal_0_318) 17)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_320 () FormalMachine (FormalWriteFromOrigin formal_0_319 31 17))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_320)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_320) (select (m_origin formal_0_320) 1) (select (m_origin formal_0_320) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_320) (select (m_origin formal_0_320) 1) (select (m_origin formal_0_320) 42)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_321 () FormalMachine (FormalCallback formal_0_320 boundary_0 (select (m_origin formal_0_320) 1) (select (m_origin formal_0_320) 42)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_322 () FormalMachine (FormalWriteFromOrigin formal_0_321 31 42))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_322)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 1) (select (m_origin formal_0_322) 43)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 1) (select (m_origin formal_0_322) 43)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_323 () FormalMachine (FormalCallback formal_0_322 boundary_0 (select (m_origin formal_0_322) 1) (select (m_origin formal_0_322) 43)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_324 () FormalMachine (FormalWriteFromOrigin formal_0_323 31 43))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_324)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_324) (select (m_origin formal_0_324) 1) (select (m_origin formal_0_324) 44)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_324) (select (m_origin formal_0_324) 1) (select (m_origin formal_0_324) 44)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_325 () FormalMachine (FormalCallback formal_0_324 boundary_0 (select (m_origin formal_0_324) 1) (select (m_origin formal_0_324) 44)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_326 () FormalMachine (FormalWriteFromOrigin formal_0_325 31 44))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_326)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_326) (select (m_origin formal_0_326) 1) (select (m_origin formal_0_326) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_326) (select (m_origin formal_0_326) 1) (select (m_origin formal_0_326) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_327 () FormalMachine (FormalCallback formal_0_326 boundary_0 (select (m_origin formal_0_326) 1) (select (m_origin formal_0_326) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_328 () FormalMachine (FormalWriteFromOrigin formal_0_327 32 45))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_329 () FormalMachine (FormalWriteFromOrigin formal_0_328 44 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_329)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_329) (select (m_origin formal_0_329) 1) (select (m_origin formal_0_329) 46)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_329) (select (m_origin formal_0_329) 1) (select (m_origin formal_0_329) 46)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_330 () FormalMachine (FormalCallback formal_0_329 boundary_0 (select (m_origin formal_0_329) 1) (select (m_origin formal_0_329) 46)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_331 () FormalMachine (FormalWriteFromOrigin formal_0_330 32 46))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_331)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_331) (select (m_origin formal_0_331) 1) (select (m_origin formal_0_331) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_331) (select (m_origin formal_0_331) 1) (select (m_origin formal_0_331) 18)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_332 () FormalMachine (FormalCallback formal_0_331 boundary_0 (select (m_origin formal_0_331) 1) (select (m_origin formal_0_331) 18)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_333 () FormalMachine (FormalWriteFromOrigin formal_0_332 32 18))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_333)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_333) (select (m_origin formal_0_333) 1) (select (m_origin formal_0_333) 48)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_333) (select (m_origin formal_0_333) 1) (select (m_origin formal_0_333) 48)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_334 () FormalMachine (FormalCallback formal_0_333 boundary_0 (select (m_origin formal_0_333) 1) (select (m_origin formal_0_333) 48)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_335 () FormalMachine (FormalWriteFromOrigin formal_0_334 32 48))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_335)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_335) (select (m_origin formal_0_335) 1) (select (m_origin formal_0_335) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_335) (select (m_origin formal_0_335) 1) (select (m_origin formal_0_335) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_336 () FormalMachine (FormalCallback formal_0_335 boundary_0 (select (m_origin formal_0_335) 1) (select (m_origin formal_0_335) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_337 () FormalMachine (FormalWriteFromOrigin formal_0_336 32 3))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_337)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_337) (select (m_origin formal_0_337) 1) (select (m_origin formal_0_337) 50)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_337) (select (m_origin formal_0_337) 1) (select (m_origin formal_0_337) 50)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_338 () FormalMachine (FormalCallback formal_0_337 boundary_0 (select (m_origin formal_0_337) 1) (select (m_origin formal_0_337) 50)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_339 () FormalMachine (FormalWriteFromOrigin formal_0_338 33 50))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_340 () FormalMachine (FormalWriteFromOrigin formal_0_339 49 33))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_340)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_340) (select (m_origin formal_0_340) 1) (select (m_origin formal_0_340) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_340) (select (m_origin formal_0_340) 1) (select (m_origin formal_0_340) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_341 () FormalMachine (FormalCallback formal_0_340 boundary_0 (select (m_origin formal_0_340) 1) (select (m_origin formal_0_340) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_342 () FormalMachine (FormalWriteFromOrigin formal_0_341 33 20))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_342)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_342) (select (m_origin formal_0_342) 1) (select (m_origin formal_0_342) 52)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_342) (select (m_origin formal_0_342) 1) (select (m_origin formal_0_342) 52)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_343 () FormalMachine (FormalCallback formal_0_342 boundary_0 (select (m_origin formal_0_342) 1) (select (m_origin formal_0_342) 52)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_344 () FormalMachine (FormalWriteFromOrigin formal_0_343 33 52))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_344)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_344) (select (m_origin formal_0_344) 1) (select (m_origin formal_0_344) 53)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_344) (select (m_origin formal_0_344) 1) (select (m_origin formal_0_344) 53)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_345 () FormalMachine (FormalCallback formal_0_344 boundary_0 (select (m_origin formal_0_344) 1) (select (m_origin formal_0_344) 53)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_346 () FormalMachine (FormalWriteFromOrigin formal_0_345 33 53))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_346)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_346) (select (m_origin formal_0_346) 1) (select (m_origin formal_0_346) 21)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_346) (select (m_origin formal_0_346) 1) (select (m_origin formal_0_346) 21)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_347 () FormalMachine (FormalCallback formal_0_346 boundary_0 (select (m_origin formal_0_346) 1) (select (m_origin formal_0_346) 21)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_348 () FormalMachine (FormalWriteFromOrigin formal_0_347 33 21))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_348)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_348) (select (m_origin formal_0_348) 1) (select (m_origin formal_0_348) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_348) (select (m_origin formal_0_348) 1) (select (m_origin formal_0_348) 9)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_349 () FormalMachine (FormalCallback formal_0_348 boundary_0 (select (m_origin formal_0_348) 1) (select (m_origin formal_0_348) 9)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_350 () FormalMachine (FormalWriteFromOrigin formal_0_349 34 9))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_351 () FormalMachine (FormalWriteFromOrigin formal_0_350 54 7))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_351)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_351) (select (m_origin formal_0_351) 1) (select (m_origin formal_0_351) 56)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_351) (select (m_origin formal_0_351) 1) (select (m_origin formal_0_351) 56)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_352 () FormalMachine (FormalCallback formal_0_351 boundary_0 (select (m_origin formal_0_351) 1) (select (m_origin formal_0_351) 56)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_353 () FormalMachine (FormalWriteFromOrigin formal_0_352 34 56))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_353)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_353) (select (m_origin formal_0_353) 1) (select (m_origin formal_0_353) 57)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_353) (select (m_origin formal_0_353) 1) (select (m_origin formal_0_353) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_354 () FormalMachine (FormalCallback formal_0_353 boundary_0 (select (m_origin formal_0_353) 1) (select (m_origin formal_0_353) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_355 () FormalMachine (FormalWriteFromOrigin formal_0_354 34 57))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_355)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_355) (select (m_origin formal_0_355) 1) (select (m_origin formal_0_355) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_355) (select (m_origin formal_0_355) 1) (select (m_origin formal_0_355) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_356 () FormalMachine (FormalCallback formal_0_355 boundary_0 (select (m_origin formal_0_355) 1) (select (m_origin formal_0_355) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_357 () FormalMachine (FormalWriteFromOrigin formal_0_356 34 23))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_357)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 1) (select (m_origin formal_0_357) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 1) (select (m_origin formal_0_357) 24)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_358 () FormalMachine (FormalCallback formal_0_357 boundary_0 (select (m_origin formal_0_357) 1) (select (m_origin formal_0_357) 24)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_359 () FormalMachine (FormalWriteFromOrigin formal_0_358 35 24))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_360 () FormalMachine (FormalWriteFromOrigin formal_0_359 58 35))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_360)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_360) (select (m_origin formal_0_360) 1) (select (m_origin formal_0_360) 60)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_360) (select (m_origin formal_0_360) 1) (select (m_origin formal_0_360) 60)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_361 () FormalMachine (FormalCallback formal_0_360 boundary_0 (select (m_origin formal_0_360) 1) (select (m_origin formal_0_360) 60)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_362 () FormalMachine (FormalWriteFromOrigin formal_0_361 35 60))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_362)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_362) (select (m_origin formal_0_362) 1) (select (m_origin formal_0_362) 61)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_362) (select (m_origin formal_0_362) 1) (select (m_origin formal_0_362) 61)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_363 () FormalMachine (FormalCallback formal_0_362 boundary_0 (select (m_origin formal_0_362) 1) (select (m_origin formal_0_362) 61)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_364 () FormalMachine (FormalWriteFromOrigin formal_0_363 35 61))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_364)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_364) (select (m_origin formal_0_364) 1) (select (m_origin formal_0_364) 62)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_364) (select (m_origin formal_0_364) 1) (select (m_origin formal_0_364) 62)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_365 () FormalMachine (FormalCallback formal_0_364 boundary_0 (select (m_origin formal_0_364) 1) (select (m_origin formal_0_364) 62)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_366 () FormalMachine (FormalWriteFromOrigin formal_0_365 35 62))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_366)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_366) (select (m_origin formal_0_366) 1) (select (m_origin formal_0_366) 63)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_366) (select (m_origin formal_0_366) 1) (select (m_origin formal_0_366) 63)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_367 () FormalMachine (FormalCallback formal_0_366 boundary_0 (select (m_origin formal_0_366) 1) (select (m_origin formal_0_366) 63)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_368 () FormalMachine (FormalWriteFromOrigin formal_0_367 35 63))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_368)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_368) (select (m_origin formal_0_368) 1) (select (m_origin formal_0_368) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_368) (select (m_origin formal_0_368) 1) (select (m_origin formal_0_368) 10)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_369 () FormalMachine (FormalCallback formal_0_368 boundary_0 (select (m_origin formal_0_368) 1) (select (m_origin formal_0_368) 10)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_370 () FormalMachine (FormalWriteFromOrigin formal_0_369 36 10))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_371 () FormalMachine (FormalWriteFromOrigin formal_0_370 63 36))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_371)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_371) (select (m_origin formal_0_371) 1) (select (m_origin formal_0_371) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_371) (select (m_origin formal_0_371) 1) (select (m_origin formal_0_371) 26)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_372 () FormalMachine (FormalCallback formal_0_371 boundary_0 (select (m_origin formal_0_371) 1) (select (m_origin formal_0_371) 26)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_373 () FormalMachine (FormalWriteFromOrigin formal_0_372 36 26))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_373)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_373) (select (m_origin formal_0_373) 1) (select (m_origin formal_0_373) 11)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_373) (select (m_origin formal_0_373) 1) (select (m_origin formal_0_373) 11)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_374 () FormalMachine (FormalCallback formal_0_373 boundary_0 (select (m_origin formal_0_373) 1) (select (m_origin formal_0_373) 11)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_375 () FormalMachine (FormalWriteFromOrigin formal_0_374 36 11))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_375)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_375) (select (m_origin formal_0_375) 1) (select (m_origin formal_0_375) 67)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_375) (select (m_origin formal_0_375) 1) (select (m_origin formal_0_375) 67)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_376 () FormalMachine (FormalCallback formal_0_375 boundary_0 (select (m_origin formal_0_375) 1) (select (m_origin formal_0_375) 67)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_377 () FormalMachine (FormalWriteFromOrigin formal_0_376 37 67))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_378 () FormalMachine (FormalWriteFromOrigin formal_0_377 66 37))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_378)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_378) (select (m_origin formal_0_378) 1) (select (m_origin formal_0_378) 68)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_378) (select (m_origin formal_0_378) 1) (select (m_origin formal_0_378) 68)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_379 () FormalMachine (FormalCallback formal_0_378 boundary_0 (select (m_origin formal_0_378) 1) (select (m_origin formal_0_378) 68)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_380 () FormalMachine (FormalWriteFromOrigin formal_0_379 37 68))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_380)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_380) (select (m_origin formal_0_380) 1) (select (m_origin formal_0_380) 69)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_380) (select (m_origin formal_0_380) 1) (select (m_origin formal_0_380) 69)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_381 () FormalMachine (FormalCallback formal_0_380 boundary_0 (select (m_origin formal_0_380) 1) (select (m_origin formal_0_380) 69)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_382 () FormalMachine (FormalWriteFromOrigin formal_0_381 37 69))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_382)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_382) (select (m_origin formal_0_382) 1) (select (m_origin formal_0_382) 70)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_382) (select (m_origin formal_0_382) 1) (select (m_origin formal_0_382) 70)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_383 () FormalMachine (FormalCallback formal_0_382 boundary_0 (select (m_origin formal_0_382) 1) (select (m_origin formal_0_382) 70)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_384 () FormalMachine (FormalWriteFromOrigin formal_0_383 37 70))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_384)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_384) (select (m_origin formal_0_384) 1) (select (m_origin formal_0_384) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_384) (select (m_origin formal_0_384) 1) (select (m_origin formal_0_384) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_385 () FormalMachine (FormalCallback formal_0_384 boundary_0 (select (m_origin formal_0_384) 1) (select (m_origin formal_0_384) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_386 () FormalMachine (FormalWriteFromOrigin formal_0_385 37 28))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_386)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_386) (select (m_origin formal_0_386) 1) (select (m_origin formal_0_386) 72)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_386) (select (m_origin formal_0_386) 1) (select (m_origin formal_0_386) 72)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_387 () FormalMachine (FormalCallback formal_0_386 boundary_0 (select (m_origin formal_0_386) 1) (select (m_origin formal_0_386) 72)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_388 () FormalMachine (FormalWriteFromOrigin formal_0_387 38 72))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_389 () FormalMachine (FormalWriteFromOrigin formal_0_388 71 38))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_389)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_389) (select (m_origin formal_0_389) 1) (select (m_origin formal_0_389) 73)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_389) (select (m_origin formal_0_389) 1) (select (m_origin formal_0_389) 73)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_390 () FormalMachine (FormalCallback formal_0_389 boundary_0 (select (m_origin formal_0_389) 1) (select (m_origin formal_0_389) 73)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_391 () FormalMachine (FormalWriteFromOrigin formal_0_390 39 73))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_392 () FormalMachine (FormalWriteFromOrigin formal_0_391 72 31))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_392)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_392) (select (m_origin formal_0_392) 1) (select (m_origin formal_0_392) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_392) (select (m_origin formal_0_392) 1) (select (m_origin formal_0_392) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_393 () FormalMachine (FormalCallback formal_0_392 boundary_0 (select (m_origin formal_0_392) 1) (select (m_origin formal_0_392) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_394 () FormalMachine (FormalWriteFromOrigin formal_0_393 39 74))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_394)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_394) (select (m_origin formal_0_394) 1) (select (m_origin formal_0_394) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_394) (select (m_origin formal_0_394) 1) (select (m_origin formal_0_394) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_395 () FormalMachine (FormalCallback formal_0_394 boundary_0 (select (m_origin formal_0_394) 1) (select (m_origin formal_0_394) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_396 () FormalMachine (FormalWriteFromOrigin formal_0_395 40 75))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_397 () FormalMachine (FormalWriteFromOrigin formal_0_396 74 16))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_397)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_397) (select (m_origin formal_0_397) 1) (select (m_origin formal_0_397) 76)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_397) (select (m_origin formal_0_397) 1) (select (m_origin formal_0_397) 76)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_398 () FormalMachine (FormalCallback formal_0_397 boundary_0 (select (m_origin formal_0_397) 1) (select (m_origin formal_0_397) 76)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_399 () FormalMachine (FormalWriteFromOrigin formal_0_398 40 76))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_399)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_399) (select (m_origin formal_0_399) 1) (select (m_origin formal_0_399) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_399) (select (m_origin formal_0_399) 1) (select (m_origin formal_0_399) 77)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_400 () FormalMachine (FormalCallback formal_0_399 boundary_0 (select (m_origin formal_0_399) 1) (select (m_origin formal_0_399) 77)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_401 () FormalMachine (FormalWriteFromOrigin formal_0_400 40 77))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_401)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_401) (select (m_origin formal_0_401) 1) (select (m_origin formal_0_401) 78)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_401) (select (m_origin formal_0_401) 1) (select (m_origin formal_0_401) 78)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_402 () FormalMachine (FormalCallback formal_0_401 boundary_0 (select (m_origin formal_0_401) 1) (select (m_origin formal_0_401) 78)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_403 () FormalMachine (FormalWriteFromOrigin formal_0_402 40 78))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_403)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_403) (select (m_origin formal_0_403) 1) (select (m_origin formal_0_403) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_403) (select (m_origin formal_0_403) 1) (select (m_origin formal_0_403) 29)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_404 () FormalMachine (FormalCallback formal_0_403 boundary_0 (select (m_origin formal_0_403) 1) (select (m_origin formal_0_403) 29)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_405 () FormalMachine (FormalWriteFromOrigin formal_0_404 40 29))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:cleanup-compare:reverse-less
(assert (not (m_panicked formal_0_405)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_405) (select (m_origin formal_0_405) 1) (select (m_origin formal_0_405) 6)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_405) (select (m_origin formal_0_405) 1) (select (m_origin formal_0_405) 6)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare:reverse-less
(define-fun formal_0_406 () FormalMachine (FormalCallback formal_0_405 boundary_0 (select (m_origin formal_0_405) 1) (select (m_origin formal_0_405) 6)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_407 () FormalMachine (FormalWriteFromOrigin formal_0_406 40 6))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_408 () FormalMachine (FormalSwap formal_0_407 29 40))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_408)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_408) (select (m_origin formal_0_408) 17) (select (m_origin formal_0_408) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_408) (select (m_origin formal_0_408) 17) (select (m_origin formal_0_408) 57)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_409 () FormalMachine (FormalCallback formal_0_408 boundary_0 (select (m_origin formal_0_408) 17) (select (m_origin formal_0_408) 57)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_409)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_409) (select (m_origin formal_0_409) 17) (select (m_origin formal_0_409) 69)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_409) (select (m_origin formal_0_409) 17) (select (m_origin formal_0_409) 69)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_410 () FormalMachine (FormalCallback formal_0_409 boundary_0 (select (m_origin formal_0_409) 17) (select (m_origin formal_0_409) 69)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_410)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_410) (select (m_origin formal_0_410) 57) (select (m_origin formal_0_410) 69)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_410) (select (m_origin formal_0_410) 57) (select (m_origin formal_0_410) 69)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_411 () FormalMachine (FormalCallback formal_0_410 boundary_0 (select (m_origin formal_0_410) 57) (select (m_origin formal_0_410) 69)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_412 () FormalMachine (FormalSwap formal_0_411 41 57))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_412)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_412) (select (m_origin formal_0_412) 43) (select (m_origin formal_0_412) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_412) (select (m_origin formal_0_412) 43) (select (m_origin formal_0_412) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_413 () FormalMachine (FormalCallback formal_0_412 boundary_0 (select (m_origin formal_0_412) 43) (select (m_origin formal_0_412) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_414 () FormalMachine (FormalWriteFromOrigin formal_0_413 42 43))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_414)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_414) (select (m_origin formal_0_414) 13) (select (m_origin formal_0_414) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_414) (select (m_origin formal_0_414) 13) (select (m_origin formal_0_414) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_415 () FormalMachine (FormalCallback formal_0_414 boundary_0 (select (m_origin formal_0_414) 13) (select (m_origin formal_0_414) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_416 () FormalMachine (FormalWriteFromOrigin formal_0_415 42 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_416)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_416) (select (m_origin formal_0_416) 45) (select (m_origin formal_0_416) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_416) (select (m_origin formal_0_416) 45) (select (m_origin formal_0_416) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_417 () FormalMachine (FormalCallback formal_0_416 boundary_0 (select (m_origin formal_0_416) 45) (select (m_origin formal_0_416) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_418 () FormalMachine (FormalWriteFromOrigin formal_0_417 42 45))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_418)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_418) (select (m_origin formal_0_418) 46) (select (m_origin formal_0_418) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_418) (select (m_origin formal_0_418) 46) (select (m_origin formal_0_418) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_419 () FormalMachine (FormalCallback formal_0_418 boundary_0 (select (m_origin formal_0_418) 46) (select (m_origin formal_0_418) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_420 () FormalMachine (FormalWriteFromOrigin formal_0_419 42 46))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_420)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_420) (select (m_origin formal_0_420) 18) (select (m_origin formal_0_420) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_420) (select (m_origin formal_0_420) 18) (select (m_origin formal_0_420) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_421 () FormalMachine (FormalCallback formal_0_420 boundary_0 (select (m_origin formal_0_420) 18) (select (m_origin formal_0_420) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_422 () FormalMachine (FormalWriteFromOrigin formal_0_421 42 18))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_422)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_422) (select (m_origin formal_0_422) 48) (select (m_origin formal_0_422) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_422) (select (m_origin formal_0_422) 48) (select (m_origin formal_0_422) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_423 () FormalMachine (FormalCallback formal_0_422 boundary_0 (select (m_origin formal_0_422) 48) (select (m_origin formal_0_422) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_424 () FormalMachine (FormalWriteFromOrigin formal_0_423 42 48))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_424)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_424) (select (m_origin formal_0_424) 33) (select (m_origin formal_0_424) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_424) (select (m_origin formal_0_424) 33) (select (m_origin formal_0_424) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_425 () FormalMachine (FormalCallback formal_0_424 boundary_0 (select (m_origin formal_0_424) 33) (select (m_origin formal_0_424) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_426 () FormalMachine (FormalWriteFromOrigin formal_0_425 42 33))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_426)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_426) (select (m_origin formal_0_426) 50) (select (m_origin formal_0_426) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_426) (select (m_origin formal_0_426) 50) (select (m_origin formal_0_426) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_427 () FormalMachine (FormalCallback formal_0_426 boundary_0 (select (m_origin formal_0_426) 50) (select (m_origin formal_0_426) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_428 () FormalMachine (FormalWriteFromOrigin formal_0_427 42 50))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_428)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_428) (select (m_origin formal_0_428) 20) (select (m_origin formal_0_428) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_428) (select (m_origin formal_0_428) 20) (select (m_origin formal_0_428) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_429 () FormalMachine (FormalCallback formal_0_428 boundary_0 (select (m_origin formal_0_428) 20) (select (m_origin formal_0_428) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_430 () FormalMachine (FormalWriteFromOrigin formal_0_429 42 20))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_430)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_430) (select (m_origin formal_0_430) 52) (select (m_origin formal_0_430) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_430) (select (m_origin formal_0_430) 52) (select (m_origin formal_0_430) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_431 () FormalMachine (FormalCallback formal_0_430 boundary_0 (select (m_origin formal_0_430) 52) (select (m_origin formal_0_430) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_432 () FormalMachine (FormalWriteFromOrigin formal_0_431 42 52))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_432)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_432) (select (m_origin formal_0_432) 53) (select (m_origin formal_0_432) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_432) (select (m_origin formal_0_432) 53) (select (m_origin formal_0_432) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_433 () FormalMachine (FormalCallback formal_0_432 boundary_0 (select (m_origin formal_0_432) 53) (select (m_origin formal_0_432) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_434 () FormalMachine (FormalWriteFromOrigin formal_0_433 42 53))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_434)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_434) (select (m_origin formal_0_434) 7) (select (m_origin formal_0_434) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_434) (select (m_origin formal_0_434) 7) (select (m_origin formal_0_434) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_435 () FormalMachine (FormalCallback formal_0_434 boundary_0 (select (m_origin formal_0_434) 7) (select (m_origin formal_0_434) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_436 () FormalMachine (FormalWriteFromOrigin formal_0_435 42 7))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_436)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_436) (select (m_origin formal_0_436) 9) (select (m_origin formal_0_436) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_436) (select (m_origin formal_0_436) 9) (select (m_origin formal_0_436) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_437 () FormalMachine (FormalCallback formal_0_436 boundary_0 (select (m_origin formal_0_436) 9) (select (m_origin formal_0_436) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_438 () FormalMachine (FormalWriteFromOrigin formal_0_437 42 9))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_438)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_438) (select (m_origin formal_0_438) 56) (select (m_origin formal_0_438) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_438) (select (m_origin formal_0_438) 56) (select (m_origin formal_0_438) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_439 () FormalMachine (FormalCallback formal_0_438 boundary_0 (select (m_origin formal_0_438) 56) (select (m_origin formal_0_438) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_440 () FormalMachine (FormalWriteFromOrigin formal_0_439 42 56))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_440)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_440) (select (m_origin formal_0_440) 17) (select (m_origin formal_0_440) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_440) (select (m_origin formal_0_440) 17) (select (m_origin formal_0_440) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_441 () FormalMachine (FormalCallback formal_0_440 boundary_0 (select (m_origin formal_0_440) 17) (select (m_origin formal_0_440) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_442 () FormalMachine (FormalWriteFromOrigin formal_0_441 42 17))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_442)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_442) (select (m_origin formal_0_442) 35) (select (m_origin formal_0_442) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_442) (select (m_origin formal_0_442) 35) (select (m_origin formal_0_442) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_443 () FormalMachine (FormalCallback formal_0_442 boundary_0 (select (m_origin formal_0_442) 35) (select (m_origin formal_0_442) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_444 () FormalMachine (FormalWriteFromOrigin formal_0_443 42 35))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_444)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_444) (select (m_origin formal_0_444) 24) (select (m_origin formal_0_444) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_444) (select (m_origin formal_0_444) 24) (select (m_origin formal_0_444) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_445 () FormalMachine (FormalCallback formal_0_444 boundary_0 (select (m_origin formal_0_444) 24) (select (m_origin formal_0_444) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_446 () FormalMachine (FormalWriteFromOrigin formal_0_445 42 24))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_446)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_446) (select (m_origin formal_0_446) 60) (select (m_origin formal_0_446) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_446) (select (m_origin formal_0_446) 60) (select (m_origin formal_0_446) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_447 () FormalMachine (FormalCallback formal_0_446 boundary_0 (select (m_origin formal_0_446) 60) (select (m_origin formal_0_446) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_448 () FormalMachine (FormalWriteFromOrigin formal_0_447 42 60))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_448)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_448) (select (m_origin formal_0_448) 61) (select (m_origin formal_0_448) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_448) (select (m_origin formal_0_448) 61) (select (m_origin formal_0_448) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_449 () FormalMachine (FormalCallback formal_0_448 boundary_0 (select (m_origin formal_0_448) 61) (select (m_origin formal_0_448) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_450 () FormalMachine (FormalWriteFromOrigin formal_0_449 42 61))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_450)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_450) (select (m_origin formal_0_450) 62) (select (m_origin formal_0_450) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_450) (select (m_origin formal_0_450) 62) (select (m_origin formal_0_450) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_451 () FormalMachine (FormalCallback formal_0_450 boundary_0 (select (m_origin formal_0_450) 62) (select (m_origin formal_0_450) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_452 () FormalMachine (FormalWriteFromOrigin formal_0_451 42 62))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_452)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_452) (select (m_origin formal_0_452) 36) (select (m_origin formal_0_452) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_452) (select (m_origin formal_0_452) 36) (select (m_origin formal_0_452) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_453 () FormalMachine (FormalCallback formal_0_452 boundary_0 (select (m_origin formal_0_452) 36) (select (m_origin formal_0_452) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_454 () FormalMachine (FormalWriteFromOrigin formal_0_453 42 36))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_454)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_454) (select (m_origin formal_0_454) 10) (select (m_origin formal_0_454) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_454) (select (m_origin formal_0_454) 10) (select (m_origin formal_0_454) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_455 () FormalMachine (FormalCallback formal_0_454 boundary_0 (select (m_origin formal_0_454) 10) (select (m_origin formal_0_454) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_456 () FormalMachine (FormalWriteFromOrigin formal_0_455 42 10))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_456)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_456) (select (m_origin formal_0_456) 26) (select (m_origin formal_0_456) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_456) (select (m_origin formal_0_456) 26) (select (m_origin formal_0_456) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_457 () FormalMachine (FormalCallback formal_0_456 boundary_0 (select (m_origin formal_0_456) 26) (select (m_origin formal_0_456) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_458 () FormalMachine (FormalWriteFromOrigin formal_0_457 42 26))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_458)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_458) (select (m_origin formal_0_458) 37) (select (m_origin formal_0_458) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_458) (select (m_origin formal_0_458) 37) (select (m_origin formal_0_458) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_459 () FormalMachine (FormalCallback formal_0_458 boundary_0 (select (m_origin formal_0_458) 37) (select (m_origin formal_0_458) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_460 () FormalMachine (FormalWriteFromOrigin formal_0_459 42 37))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_460)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_460) (select (m_origin formal_0_460) 67) (select (m_origin formal_0_460) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_460) (select (m_origin formal_0_460) 67) (select (m_origin formal_0_460) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_461 () FormalMachine (FormalCallback formal_0_460 boundary_0 (select (m_origin formal_0_460) 67) (select (m_origin formal_0_460) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_462 () FormalMachine (FormalWriteFromOrigin formal_0_461 42 67))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_462)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_462) (select (m_origin formal_0_462) 68) (select (m_origin formal_0_462) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_462) (select (m_origin formal_0_462) 68) (select (m_origin formal_0_462) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_463 () FormalMachine (FormalCallback formal_0_462 boundary_0 (select (m_origin formal_0_462) 68) (select (m_origin formal_0_462) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_464 () FormalMachine (FormalWriteFromOrigin formal_0_463 42 68))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_464)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_464) (select (m_origin formal_0_464) 69) (select (m_origin formal_0_464) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_464) (select (m_origin formal_0_464) 69) (select (m_origin formal_0_464) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_465 () FormalMachine (FormalCallback formal_0_464 boundary_0 (select (m_origin formal_0_464) 69) (select (m_origin formal_0_464) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_466 () FormalMachine (FormalWriteFromOrigin formal_0_465 42 69))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_466)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_466) (select (m_origin formal_0_466) 70) (select (m_origin formal_0_466) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_466) (select (m_origin formal_0_466) 70) (select (m_origin formal_0_466) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_467 () FormalMachine (FormalCallback formal_0_466 boundary_0 (select (m_origin formal_0_466) 70) (select (m_origin formal_0_466) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_468 () FormalMachine (FormalWriteFromOrigin formal_0_467 42 70))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_468)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_468) (select (m_origin formal_0_468) 38) (select (m_origin formal_0_468) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_468) (select (m_origin formal_0_468) 38) (select (m_origin formal_0_468) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_469 () FormalMachine (FormalCallback formal_0_468 boundary_0 (select (m_origin formal_0_468) 38) (select (m_origin formal_0_468) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_470 () FormalMachine (FormalWriteFromOrigin formal_0_469 42 38))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_470)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_470) (select (m_origin formal_0_470) 31) (select (m_origin formal_0_470) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_470) (select (m_origin formal_0_470) 31) (select (m_origin formal_0_470) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_471 () FormalMachine (FormalCallback formal_0_470 boundary_0 (select (m_origin formal_0_470) 31) (select (m_origin formal_0_470) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_472 () FormalMachine (FormalWriteFromOrigin formal_0_471 42 31))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_472)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_472) (select (m_origin formal_0_472) 73) (select (m_origin formal_0_472) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_472) (select (m_origin formal_0_472) 73) (select (m_origin formal_0_472) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_473 () FormalMachine (FormalCallback formal_0_472 boundary_0 (select (m_origin formal_0_472) 73) (select (m_origin formal_0_472) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_474 () FormalMachine (FormalWriteFromOrigin formal_0_473 42 73))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_474)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_474) (select (m_origin formal_0_474) 16) (select (m_origin formal_0_474) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_474) (select (m_origin formal_0_474) 16) (select (m_origin formal_0_474) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_475 () FormalMachine (FormalCallback formal_0_474 boundary_0 (select (m_origin formal_0_474) 16) (select (m_origin formal_0_474) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_476 () FormalMachine (FormalWriteFromOrigin formal_0_475 42 16))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_476)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_476) (select (m_origin formal_0_476) 75) (select (m_origin formal_0_476) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_476) (select (m_origin formal_0_476) 75) (select (m_origin formal_0_476) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_477 () FormalMachine (FormalCallback formal_0_476 boundary_0 (select (m_origin formal_0_476) 75) (select (m_origin formal_0_476) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_478 () FormalMachine (FormalWriteFromOrigin formal_0_477 42 75))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_478)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_478) (select (m_origin formal_0_478) 76) (select (m_origin formal_0_478) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_478) (select (m_origin formal_0_478) 76) (select (m_origin formal_0_478) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_479 () FormalMachine (FormalCallback formal_0_478 boundary_0 (select (m_origin formal_0_478) 76) (select (m_origin formal_0_478) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_480 () FormalMachine (FormalWriteFromOrigin formal_0_479 42 76))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_480)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_480) (select (m_origin formal_0_480) 77) (select (m_origin formal_0_480) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_480) (select (m_origin formal_0_480) 77) (select (m_origin formal_0_480) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_481 () FormalMachine (FormalCallback formal_0_480 boundary_0 (select (m_origin formal_0_480) 77) (select (m_origin formal_0_480) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_482 () FormalMachine (FormalWriteFromOrigin formal_0_481 42 77))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_482)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_482) (select (m_origin formal_0_482) 78) (select (m_origin formal_0_482) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_482) (select (m_origin formal_0_482) 78) (select (m_origin formal_0_482) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_483 () FormalMachine (FormalCallback formal_0_482 boundary_0 (select (m_origin formal_0_482) 78) (select (m_origin formal_0_482) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_484 () FormalMachine (FormalWriteFromOrigin formal_0_483 42 78))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_484)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_484) (select (m_origin formal_0_484) 29) (select (m_origin formal_0_484) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_484) (select (m_origin formal_0_484) 29) (select (m_origin formal_0_484) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_485 () FormalMachine (FormalCallback formal_0_484 boundary_0 (select (m_origin formal_0_484) 29) (select (m_origin formal_0_484) 57)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_486 () FormalMachine (FormalWriteFromOrigin formal_0_485 42 29))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_486)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_486) (select (m_origin formal_0_486) 42) (select (m_origin formal_0_486) 57)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_486) (select (m_origin formal_0_486) 42) (select (m_origin formal_0_486) 57)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_487 () FormalMachine (FormalCallback formal_0_486 boundary_0 (select (m_origin formal_0_486) 42) (select (m_origin formal_0_486) 57)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_488 () FormalMachine (FormalWriteFromOrigin formal_0_487 42 42))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_489 () FormalMachine (FormalSwap formal_0_488 41 41))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_489)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_489) (select (m_origin formal_0_489) 42) (select (m_origin formal_0_489) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_489) (select (m_origin formal_0_489) 42) (select (m_origin formal_0_489) 35)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_490 () FormalMachine (FormalCallback formal_0_489 boundary_0 (select (m_origin formal_0_489) 42) (select (m_origin formal_0_489) 35)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_490)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_490) (select (m_origin formal_0_490) 42) (select (m_origin formal_0_490) 70)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_490) (select (m_origin formal_0_490) 42) (select (m_origin formal_0_490) 70)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_491 () FormalMachine (FormalCallback formal_0_490 boundary_0 (select (m_origin formal_0_490) 42) (select (m_origin formal_0_490) 70)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_491)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_491) (select (m_origin formal_0_491) 35) (select (m_origin formal_0_491) 70)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_491) (select (m_origin formal_0_491) 35) (select (m_origin formal_0_491) 70)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_492 () FormalMachine (FormalCallback formal_0_491 boundary_0 (select (m_origin formal_0_491) 35) (select (m_origin formal_0_491) 70)))
; source callback case=duplicate-class-ancestor-pivot phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_492)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_492) (select (m_origin formal_0_492) 57) (select (m_origin formal_0_492) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_492) (select (m_origin formal_0_492) 57) (select (m_origin formal_0_492) 35)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_493 () FormalMachine (FormalCallback formal_0_492 boundary_0 (select (m_origin formal_0_492) 57) (select (m_origin formal_0_492) 35)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_494 () FormalMachine (FormalSwap formal_0_493 42 58))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_494)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_494) (select (m_origin formal_0_494) 35) (select (m_origin formal_0_494) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_494) (select (m_origin formal_0_494) 35) (select (m_origin formal_0_494) 13)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_495 () FormalMachine (FormalCallback formal_0_494 boundary_0 (select (m_origin formal_0_494) 35) (select (m_origin formal_0_494) 13)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_496 () FormalMachine (FormalWriteFromOrigin formal_0_495 43 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_496)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_496) (select (m_origin formal_0_496) 35) (select (m_origin formal_0_496) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_496) (select (m_origin formal_0_496) 35) (select (m_origin formal_0_496) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_497 () FormalMachine (FormalCallback formal_0_496 boundary_0 (select (m_origin formal_0_496) 35) (select (m_origin formal_0_496) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_498 () FormalMachine (FormalWriteFromOrigin formal_0_497 43 45))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_498)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_498) (select (m_origin formal_0_498) 35) (select (m_origin formal_0_498) 46)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_498) (select (m_origin formal_0_498) 35) (select (m_origin formal_0_498) 46)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_499 () FormalMachine (FormalCallback formal_0_498 boundary_0 (select (m_origin formal_0_498) 35) (select (m_origin formal_0_498) 46)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_500 () FormalMachine (FormalWriteFromOrigin formal_0_499 44 46))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_501 () FormalMachine (FormalWriteFromOrigin formal_0_500 45 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_501)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_501) (select (m_origin formal_0_501) 35) (select (m_origin formal_0_501) 18)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_501) (select (m_origin formal_0_501) 35) (select (m_origin formal_0_501) 18)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_502 () FormalMachine (FormalCallback formal_0_501 boundary_0 (select (m_origin formal_0_501) 35) (select (m_origin formal_0_501) 18)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_503 () FormalMachine (FormalWriteFromOrigin formal_0_502 44 18))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_503)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_503) (select (m_origin formal_0_503) 35) (select (m_origin formal_0_503) 48)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_503) (select (m_origin formal_0_503) 35) (select (m_origin formal_0_503) 48)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_504 () FormalMachine (FormalCallback formal_0_503 boundary_0 (select (m_origin formal_0_503) 35) (select (m_origin formal_0_503) 48)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_505 () FormalMachine (FormalWriteFromOrigin formal_0_504 45 48))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_506 () FormalMachine (FormalWriteFromOrigin formal_0_505 47 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_506)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_506) (select (m_origin formal_0_506) 35) (select (m_origin formal_0_506) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_506) (select (m_origin formal_0_506) 35) (select (m_origin formal_0_506) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_507 () FormalMachine (FormalCallback formal_0_506 boundary_0 (select (m_origin formal_0_506) 35) (select (m_origin formal_0_506) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_508 () FormalMachine (FormalWriteFromOrigin formal_0_507 45 33))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_508)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_508) (select (m_origin formal_0_508) 35) (select (m_origin formal_0_508) 50)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_508) (select (m_origin formal_0_508) 35) (select (m_origin formal_0_508) 50)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_509 () FormalMachine (FormalCallback formal_0_508 boundary_0 (select (m_origin formal_0_508) 35) (select (m_origin formal_0_508) 50)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_510 () FormalMachine (FormalWriteFromOrigin formal_0_509 45 50))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_510)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_510) (select (m_origin formal_0_510) 35) (select (m_origin formal_0_510) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_510) (select (m_origin formal_0_510) 35) (select (m_origin formal_0_510) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_511 () FormalMachine (FormalCallback formal_0_510 boundary_0 (select (m_origin formal_0_510) 35) (select (m_origin formal_0_510) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_512 () FormalMachine (FormalWriteFromOrigin formal_0_511 46 20))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_513 () FormalMachine (FormalWriteFromOrigin formal_0_512 50 46))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_513)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_513) (select (m_origin formal_0_513) 35) (select (m_origin formal_0_513) 52)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_513) (select (m_origin formal_0_513) 35) (select (m_origin formal_0_513) 52)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_514 () FormalMachine (FormalCallback formal_0_513 boundary_0 (select (m_origin formal_0_513) 35) (select (m_origin formal_0_513) 52)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_515 () FormalMachine (FormalWriteFromOrigin formal_0_514 46 52))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_515)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_515) (select (m_origin formal_0_515) 35) (select (m_origin formal_0_515) 53)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_515) (select (m_origin formal_0_515) 35) (select (m_origin formal_0_515) 53)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_516 () FormalMachine (FormalCallback formal_0_515 boundary_0 (select (m_origin formal_0_515) 35) (select (m_origin formal_0_515) 53)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_517 () FormalMachine (FormalWriteFromOrigin formal_0_516 46 53))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_517)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_517) (select (m_origin formal_0_517) 35) (select (m_origin formal_0_517) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_517) (select (m_origin formal_0_517) 35) (select (m_origin formal_0_517) 7)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_518 () FormalMachine (FormalCallback formal_0_517 boundary_0 (select (m_origin formal_0_517) 35) (select (m_origin formal_0_517) 7)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_519 () FormalMachine (FormalWriteFromOrigin formal_0_518 46 7))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_519)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_519) (select (m_origin formal_0_519) 35) (select (m_origin formal_0_519) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_519) (select (m_origin formal_0_519) 35) (select (m_origin formal_0_519) 9)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_520 () FormalMachine (FormalCallback formal_0_519 boundary_0 (select (m_origin formal_0_519) 35) (select (m_origin formal_0_519) 9)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_521 () FormalMachine (FormalWriteFromOrigin formal_0_520 46 9))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_521)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_521) (select (m_origin formal_0_521) 35) (select (m_origin formal_0_521) 56)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_521) (select (m_origin formal_0_521) 35) (select (m_origin formal_0_521) 56)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_522 () FormalMachine (FormalCallback formal_0_521 boundary_0 (select (m_origin formal_0_521) 35) (select (m_origin formal_0_521) 56)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_523 () FormalMachine (FormalWriteFromOrigin formal_0_522 46 56))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_523)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_523) (select (m_origin formal_0_523) 35) (select (m_origin formal_0_523) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_523) (select (m_origin formal_0_523) 35) (select (m_origin formal_0_523) 17)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_524 () FormalMachine (FormalCallback formal_0_523 boundary_0 (select (m_origin formal_0_523) 35) (select (m_origin formal_0_523) 17)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_525 () FormalMachine (FormalWriteFromOrigin formal_0_524 47 17))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_526 () FormalMachine (FormalWriteFromOrigin formal_0_525 56 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_526)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_526) (select (m_origin formal_0_526) 35) (select (m_origin formal_0_526) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_526) (select (m_origin formal_0_526) 35) (select (m_origin formal_0_526) 42)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_527 () FormalMachine (FormalCallback formal_0_526 boundary_0 (select (m_origin formal_0_526) 35) (select (m_origin formal_0_526) 42)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_528 () FormalMachine (FormalWriteFromOrigin formal_0_527 47 42))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_528)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_528) (select (m_origin formal_0_528) 35) (select (m_origin formal_0_528) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_528) (select (m_origin formal_0_528) 35) (select (m_origin formal_0_528) 24)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_529 () FormalMachine (FormalCallback formal_0_528 boundary_0 (select (m_origin formal_0_528) 35) (select (m_origin formal_0_528) 24)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_530 () FormalMachine (FormalWriteFromOrigin formal_0_529 47 24))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_530)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_530) (select (m_origin formal_0_530) 35) (select (m_origin formal_0_530) 60)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_530) (select (m_origin formal_0_530) 35) (select (m_origin formal_0_530) 60)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_531 () FormalMachine (FormalCallback formal_0_530 boundary_0 (select (m_origin formal_0_530) 35) (select (m_origin formal_0_530) 60)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_532 () FormalMachine (FormalWriteFromOrigin formal_0_531 47 60))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_532)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_532) (select (m_origin formal_0_532) 35) (select (m_origin formal_0_532) 61)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_532) (select (m_origin formal_0_532) 35) (select (m_origin formal_0_532) 61)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_533 () FormalMachine (FormalCallback formal_0_532 boundary_0 (select (m_origin formal_0_532) 35) (select (m_origin formal_0_532) 61)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_534 () FormalMachine (FormalWriteFromOrigin formal_0_533 47 61))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_534)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_534) (select (m_origin formal_0_534) 35) (select (m_origin formal_0_534) 62)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_534) (select (m_origin formal_0_534) 35) (select (m_origin formal_0_534) 62)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_535 () FormalMachine (FormalCallback formal_0_534 boundary_0 (select (m_origin formal_0_534) 35) (select (m_origin formal_0_534) 62)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_536 () FormalMachine (FormalWriteFromOrigin formal_0_535 47 62))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_536)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_536) (select (m_origin formal_0_536) 35) (select (m_origin formal_0_536) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_536) (select (m_origin formal_0_536) 35) (select (m_origin formal_0_536) 36)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_537 () FormalMachine (FormalCallback formal_0_536 boundary_0 (select (m_origin formal_0_536) 35) (select (m_origin formal_0_536) 36)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_538 () FormalMachine (FormalWriteFromOrigin formal_0_537 47 36))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_538)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_538) (select (m_origin formal_0_538) 35) (select (m_origin formal_0_538) 10)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_538) (select (m_origin formal_0_538) 35) (select (m_origin formal_0_538) 10)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_539 () FormalMachine (FormalCallback formal_0_538 boundary_0 (select (m_origin formal_0_538) 35) (select (m_origin formal_0_538) 10)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_540 () FormalMachine (FormalWriteFromOrigin formal_0_539 47 10))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_540)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_540) (select (m_origin formal_0_540) 35) (select (m_origin formal_0_540) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_540) (select (m_origin formal_0_540) 35) (select (m_origin formal_0_540) 26)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_541 () FormalMachine (FormalCallback formal_0_540 boundary_0 (select (m_origin formal_0_540) 35) (select (m_origin formal_0_540) 26)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_542 () FormalMachine (FormalWriteFromOrigin formal_0_541 48 26))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_543 () FormalMachine (FormalWriteFromOrigin formal_0_542 64 48))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_543)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_543) (select (m_origin formal_0_543) 35) (select (m_origin formal_0_543) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_543) (select (m_origin formal_0_543) 35) (select (m_origin formal_0_543) 37)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_544 () FormalMachine (FormalCallback formal_0_543 boundary_0 (select (m_origin formal_0_543) 35) (select (m_origin formal_0_543) 37)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_545 () FormalMachine (FormalWriteFromOrigin formal_0_544 48 37))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_545)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_545) (select (m_origin formal_0_545) 35) (select (m_origin formal_0_545) 67)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_545) (select (m_origin formal_0_545) 35) (select (m_origin formal_0_545) 67)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_546 () FormalMachine (FormalCallback formal_0_545 boundary_0 (select (m_origin formal_0_545) 35) (select (m_origin formal_0_545) 67)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_547 () FormalMachine (FormalWriteFromOrigin formal_0_546 48 67))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_547)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_547) (select (m_origin formal_0_547) 35) (select (m_origin formal_0_547) 68)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_547) (select (m_origin formal_0_547) 35) (select (m_origin formal_0_547) 68)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_548 () FormalMachine (FormalCallback formal_0_547 boundary_0 (select (m_origin formal_0_547) 35) (select (m_origin formal_0_547) 68)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_549 () FormalMachine (FormalWriteFromOrigin formal_0_548 48 68))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_549)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_549) (select (m_origin formal_0_549) 35) (select (m_origin formal_0_549) 69)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_549) (select (m_origin formal_0_549) 35) (select (m_origin formal_0_549) 69)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_550 () FormalMachine (FormalCallback formal_0_549 boundary_0 (select (m_origin formal_0_549) 35) (select (m_origin formal_0_549) 69)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_551 () FormalMachine (FormalWriteFromOrigin formal_0_550 48 69))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_551)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_551) (select (m_origin formal_0_551) 35) (select (m_origin formal_0_551) 70)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_551) (select (m_origin formal_0_551) 35) (select (m_origin formal_0_551) 70)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_552 () FormalMachine (FormalCallback formal_0_551 boundary_0 (select (m_origin formal_0_551) 35) (select (m_origin formal_0_551) 70)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_553 () FormalMachine (FormalWriteFromOrigin formal_0_552 49 70))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_554 () FormalMachine (FormalWriteFromOrigin formal_0_553 69 33))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_554)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_554) (select (m_origin formal_0_554) 35) (select (m_origin formal_0_554) 38)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_554) (select (m_origin formal_0_554) 35) (select (m_origin formal_0_554) 38)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_555 () FormalMachine (FormalCallback formal_0_554 boundary_0 (select (m_origin formal_0_554) 35) (select (m_origin formal_0_554) 38)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_556 () FormalMachine (FormalWriteFromOrigin formal_0_555 50 38))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_557 () FormalMachine (FormalWriteFromOrigin formal_0_556 70 46))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_557)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_557) (select (m_origin formal_0_557) 35) (select (m_origin formal_0_557) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_557) (select (m_origin formal_0_557) 35) (select (m_origin formal_0_557) 31)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_558 () FormalMachine (FormalCallback formal_0_557 boundary_0 (select (m_origin formal_0_557) 35) (select (m_origin formal_0_557) 31)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_559 () FormalMachine (FormalWriteFromOrigin formal_0_558 50 31))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_559)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_559) (select (m_origin formal_0_559) 35) (select (m_origin formal_0_559) 73)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_559) (select (m_origin formal_0_559) 35) (select (m_origin formal_0_559) 73)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_560 () FormalMachine (FormalCallback formal_0_559 boundary_0 (select (m_origin formal_0_559) 35) (select (m_origin formal_0_559) 73)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_561 () FormalMachine (FormalWriteFromOrigin formal_0_560 50 73))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_561)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_561) (select (m_origin formal_0_561) 35) (select (m_origin formal_0_561) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_561) (select (m_origin formal_0_561) 35) (select (m_origin formal_0_561) 16)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_562 () FormalMachine (FormalCallback formal_0_561 boundary_0 (select (m_origin formal_0_561) 35) (select (m_origin formal_0_561) 16)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_563 () FormalMachine (FormalWriteFromOrigin formal_0_562 51 16))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_564 () FormalMachine (FormalWriteFromOrigin formal_0_563 73 20))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_564)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_564) (select (m_origin formal_0_564) 35) (select (m_origin formal_0_564) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_564) (select (m_origin formal_0_564) 35) (select (m_origin formal_0_564) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_565 () FormalMachine (FormalCallback formal_0_564 boundary_0 (select (m_origin formal_0_564) 35) (select (m_origin formal_0_564) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_566 () FormalMachine (FormalWriteFromOrigin formal_0_565 51 75))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_566)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_566) (select (m_origin formal_0_566) 35) (select (m_origin formal_0_566) 76)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_566) (select (m_origin formal_0_566) 35) (select (m_origin formal_0_566) 76)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_567 () FormalMachine (FormalCallback formal_0_566 boundary_0 (select (m_origin formal_0_566) 35) (select (m_origin formal_0_566) 76)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_568 () FormalMachine (FormalWriteFromOrigin formal_0_567 51 76))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_568)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_568) (select (m_origin formal_0_568) 35) (select (m_origin formal_0_568) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_568) (select (m_origin formal_0_568) 35) (select (m_origin formal_0_568) 77)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_569 () FormalMachine (FormalCallback formal_0_568 boundary_0 (select (m_origin formal_0_568) 35) (select (m_origin formal_0_568) 77)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_570 () FormalMachine (FormalWriteFromOrigin formal_0_569 52 77))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_571 () FormalMachine (FormalWriteFromOrigin formal_0_570 76 52))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_571)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_571) (select (m_origin formal_0_571) 35) (select (m_origin formal_0_571) 78)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_571) (select (m_origin formal_0_571) 35) (select (m_origin formal_0_571) 78)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_572 () FormalMachine (FormalCallback formal_0_571 boundary_0 (select (m_origin formal_0_571) 35) (select (m_origin formal_0_571) 78)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_573 () FormalMachine (FormalWriteFromOrigin formal_0_572 52 78))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare:reverse-less
(assert (not (m_panicked formal_0_573)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_573) (select (m_origin formal_0_573) 35) (select (m_origin formal_0_573) 29)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_573) (select (m_origin formal_0_573) 35) (select (m_origin formal_0_573) 29)) false))
; source callback transition phase=partition-lomuto-cyclic:compare:reverse-less
(define-fun formal_0_574 () FormalMachine (FormalCallback formal_0_573 boundary_0 (select (m_origin formal_0_573) 35) (select (m_origin formal_0_573) 29)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_575 () FormalMachine (FormalWriteFromOrigin formal_0_574 52 29))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:cleanup-compare:reverse-less
(assert (not (m_panicked formal_0_575)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_575) (select (m_origin formal_0_575) 35) (select (m_origin formal_0_575) 43)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_575) (select (m_origin formal_0_575) 35) (select (m_origin formal_0_575) 43)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare:reverse-less
(define-fun formal_0_576 () FormalMachine (FormalCallback formal_0_575 boundary_0 (select (m_origin formal_0_575) 35) (select (m_origin formal_0_575) 43)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_577 () FormalMachine (FormalWriteFromOrigin formal_0_576 53 43))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_578 () FormalMachine (FormalWriteFromOrigin formal_0_577 79 53))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_579 () FormalMachine (FormalSwap formal_0_578 42 53))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_579)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_579) (select (m_origin formal_0_579) 7) (select (m_origin formal_0_579) 37)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_579) (select (m_origin formal_0_579) 7) (select (m_origin formal_0_579) 37)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_580 () FormalMachine (FormalCallback formal_0_579 boundary_0 (select (m_origin formal_0_579) 7) (select (m_origin formal_0_579) 37)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_580)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_580) (select (m_origin formal_0_580) 7) (select (m_origin formal_0_580) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_580) (select (m_origin formal_0_580) 7) (select (m_origin formal_0_580) 75)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_581 () FormalMachine (FormalCallback formal_0_580 boundary_0 (select (m_origin formal_0_580) 7) (select (m_origin formal_0_580) 75)))
; source callback case=duplicate-class-ancestor-pivot phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_581)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_581) (select (m_origin formal_0_581) 37) (select (m_origin formal_0_581) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_581) (select (m_origin formal_0_581) 37) (select (m_origin formal_0_581) 75)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_582 () FormalMachine (FormalCallback formal_0_581 boundary_0 (select (m_origin formal_0_581) 37) (select (m_origin formal_0_581) 75)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_583 () FormalMachine (FormalSwap formal_0_582 54 75))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_583)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_583) (select (m_origin formal_0_583) 13) (select (m_origin formal_0_583) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_583) (select (m_origin formal_0_583) 13) (select (m_origin formal_0_583) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_584 () FormalMachine (FormalCallback formal_0_583 boundary_0 (select (m_origin formal_0_583) 13) (select (m_origin formal_0_583) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_585 () FormalMachine (FormalWriteFromOrigin formal_0_584 55 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_585)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_585) (select (m_origin formal_0_585) 17) (select (m_origin formal_0_585) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_585) (select (m_origin formal_0_585) 17) (select (m_origin formal_0_585) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_586 () FormalMachine (FormalCallback formal_0_585 boundary_0 (select (m_origin formal_0_585) 17) (select (m_origin formal_0_585) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_587 () FormalMachine (FormalWriteFromOrigin formal_0_586 55 17))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_587)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_587) (select (m_origin formal_0_587) 42) (select (m_origin formal_0_587) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_587) (select (m_origin formal_0_587) 42) (select (m_origin formal_0_587) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_588 () FormalMachine (FormalCallback formal_0_587 boundary_0 (select (m_origin formal_0_587) 42) (select (m_origin formal_0_587) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_589 () FormalMachine (FormalWriteFromOrigin formal_0_588 55 42))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_589)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_589) (select (m_origin formal_0_589) 24) (select (m_origin formal_0_589) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_589) (select (m_origin formal_0_589) 24) (select (m_origin formal_0_589) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_590 () FormalMachine (FormalCallback formal_0_589 boundary_0 (select (m_origin formal_0_589) 24) (select (m_origin formal_0_589) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_591 () FormalMachine (FormalWriteFromOrigin formal_0_590 56 24))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_592 () FormalMachine (FormalWriteFromOrigin formal_0_591 58 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_592)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_592) (select (m_origin formal_0_592) 60) (select (m_origin formal_0_592) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_592) (select (m_origin formal_0_592) 60) (select (m_origin formal_0_592) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_593 () FormalMachine (FormalCallback formal_0_592 boundary_0 (select (m_origin formal_0_592) 60) (select (m_origin formal_0_592) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_594 () FormalMachine (FormalWriteFromOrigin formal_0_593 56 60))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_594)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_594) (select (m_origin formal_0_594) 61) (select (m_origin formal_0_594) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_594) (select (m_origin formal_0_594) 61) (select (m_origin formal_0_594) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_595 () FormalMachine (FormalCallback formal_0_594 boundary_0 (select (m_origin formal_0_594) 61) (select (m_origin formal_0_594) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_596 () FormalMachine (FormalWriteFromOrigin formal_0_595 57 61))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_597 () FormalMachine (FormalWriteFromOrigin formal_0_596 60 17))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_597)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_597) (select (m_origin formal_0_597) 62) (select (m_origin formal_0_597) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_597) (select (m_origin formal_0_597) 62) (select (m_origin formal_0_597) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_598 () FormalMachine (FormalCallback formal_0_597 boundary_0 (select (m_origin formal_0_597) 62) (select (m_origin formal_0_597) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_599 () FormalMachine (FormalWriteFromOrigin formal_0_598 58 62))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_600 () FormalMachine (FormalWriteFromOrigin formal_0_599 61 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_600)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_600) (select (m_origin formal_0_600) 36) (select (m_origin formal_0_600) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_600) (select (m_origin formal_0_600) 36) (select (m_origin formal_0_600) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_601 () FormalMachine (FormalCallback formal_0_600 boundary_0 (select (m_origin formal_0_600) 36) (select (m_origin formal_0_600) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_602 () FormalMachine (FormalWriteFromOrigin formal_0_601 59 36))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_603 () FormalMachine (FormalWriteFromOrigin formal_0_602 62 24))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_603)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_603) (select (m_origin formal_0_603) 48) (select (m_origin formal_0_603) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_603) (select (m_origin formal_0_603) 48) (select (m_origin formal_0_603) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_604 () FormalMachine (FormalCallback formal_0_603 boundary_0 (select (m_origin formal_0_603) 48) (select (m_origin formal_0_603) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_605 () FormalMachine (FormalWriteFromOrigin formal_0_604 60 48))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_606 () FormalMachine (FormalWriteFromOrigin formal_0_605 63 17))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_606)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_606) (select (m_origin formal_0_606) 26) (select (m_origin formal_0_606) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_606) (select (m_origin formal_0_606) 26) (select (m_origin formal_0_606) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_607 () FormalMachine (FormalCallback formal_0_606 boundary_0 (select (m_origin formal_0_606) 26) (select (m_origin formal_0_606) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_608 () FormalMachine (FormalWriteFromOrigin formal_0_607 60 26))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_608)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_608) (select (m_origin formal_0_608) 37) (select (m_origin formal_0_608) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_608) (select (m_origin formal_0_608) 37) (select (m_origin formal_0_608) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_609 () FormalMachine (FormalCallback formal_0_608 boundary_0 (select (m_origin formal_0_608) 37) (select (m_origin formal_0_608) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_610 () FormalMachine (FormalWriteFromOrigin formal_0_609 61 37))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_611 () FormalMachine (FormalWriteFromOrigin formal_0_610 65 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_611)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_611) (select (m_origin formal_0_611) 67) (select (m_origin formal_0_611) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_611) (select (m_origin formal_0_611) 67) (select (m_origin formal_0_611) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_612 () FormalMachine (FormalCallback formal_0_611 boundary_0 (select (m_origin formal_0_611) 67) (select (m_origin formal_0_611) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_613 () FormalMachine (FormalWriteFromOrigin formal_0_612 62 67))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_614 () FormalMachine (FormalWriteFromOrigin formal_0_613 66 24))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_614)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_614) (select (m_origin formal_0_614) 68) (select (m_origin formal_0_614) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_614) (select (m_origin formal_0_614) 68) (select (m_origin formal_0_614) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_615 () FormalMachine (FormalCallback formal_0_614 boundary_0 (select (m_origin formal_0_614) 68) (select (m_origin formal_0_614) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_616 () FormalMachine (FormalWriteFromOrigin formal_0_615 62 68))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_616)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_616) (select (m_origin formal_0_616) 33) (select (m_origin formal_0_616) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_616) (select (m_origin formal_0_616) 33) (select (m_origin formal_0_616) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_617 () FormalMachine (FormalCallback formal_0_616 boundary_0 (select (m_origin formal_0_616) 33) (select (m_origin formal_0_616) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_618 () FormalMachine (FormalWriteFromOrigin formal_0_617 63 33))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_619 () FormalMachine (FormalWriteFromOrigin formal_0_618 68 17))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_619)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_619) (select (m_origin formal_0_619) 46) (select (m_origin formal_0_619) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_619) (select (m_origin formal_0_619) 46) (select (m_origin formal_0_619) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_620 () FormalMachine (FormalCallback formal_0_619 boundary_0 (select (m_origin formal_0_619) 46) (select (m_origin formal_0_619) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_621 () FormalMachine (FormalWriteFromOrigin formal_0_620 63 46))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_621)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_621) (select (m_origin formal_0_621) 38) (select (m_origin formal_0_621) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_621) (select (m_origin formal_0_621) 38) (select (m_origin formal_0_621) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_622 () FormalMachine (FormalCallback formal_0_621 boundary_0 (select (m_origin formal_0_621) 38) (select (m_origin formal_0_621) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_623 () FormalMachine (FormalWriteFromOrigin formal_0_622 64 38))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_624 () FormalMachine (FormalWriteFromOrigin formal_0_623 70 48))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_624)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_624) (select (m_origin formal_0_624) 31) (select (m_origin formal_0_624) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_624) (select (m_origin formal_0_624) 31) (select (m_origin formal_0_624) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_625 () FormalMachine (FormalCallback formal_0_624 boundary_0 (select (m_origin formal_0_624) 31) (select (m_origin formal_0_624) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_626 () FormalMachine (FormalWriteFromOrigin formal_0_625 65 31))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_627 () FormalMachine (FormalWriteFromOrigin formal_0_626 71 13))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_627)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_627) (select (m_origin formal_0_627) 20) (select (m_origin formal_0_627) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_627) (select (m_origin formal_0_627) 20) (select (m_origin formal_0_627) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_628 () FormalMachine (FormalCallback formal_0_627 boundary_0 (select (m_origin formal_0_627) 20) (select (m_origin formal_0_627) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_629 () FormalMachine (FormalWriteFromOrigin formal_0_628 65 20))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_629)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_629) (select (m_origin formal_0_629) 16) (select (m_origin formal_0_629) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_629) (select (m_origin formal_0_629) 16) (select (m_origin formal_0_629) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_630 () FormalMachine (FormalCallback formal_0_629 boundary_0 (select (m_origin formal_0_629) 16) (select (m_origin formal_0_629) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_631 () FormalMachine (FormalWriteFromOrigin formal_0_630 65 16))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_631)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_631) (select (m_origin formal_0_631) 7) (select (m_origin formal_0_631) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_631) (select (m_origin formal_0_631) 7) (select (m_origin formal_0_631) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_632 () FormalMachine (FormalCallback formal_0_631 boundary_0 (select (m_origin formal_0_631) 7) (select (m_origin formal_0_631) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_633 () FormalMachine (FormalWriteFromOrigin formal_0_632 66 7))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_634 () FormalMachine (FormalWriteFromOrigin formal_0_633 74 24))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_634)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_634) (select (m_origin formal_0_634) 52) (select (m_origin formal_0_634) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_634) (select (m_origin formal_0_634) 52) (select (m_origin formal_0_634) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_635 () FormalMachine (FormalCallback formal_0_634 boundary_0 (select (m_origin formal_0_634) 52) (select (m_origin formal_0_634) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_636 () FormalMachine (FormalWriteFromOrigin formal_0_635 66 52))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_636)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_636) (select (m_origin formal_0_636) 77) (select (m_origin formal_0_636) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_636) (select (m_origin formal_0_636) 77) (select (m_origin formal_0_636) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_637 () FormalMachine (FormalCallback formal_0_636 boundary_0 (select (m_origin formal_0_636) 77) (select (m_origin formal_0_636) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_638 () FormalMachine (FormalWriteFromOrigin formal_0_637 67 77))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_639 () FormalMachine (FormalWriteFromOrigin formal_0_638 76 67))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_639)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_639) (select (m_origin formal_0_639) 78) (select (m_origin formal_0_639) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_639) (select (m_origin formal_0_639) 78) (select (m_origin formal_0_639) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_640 () FormalMachine (FormalCallback formal_0_639 boundary_0 (select (m_origin formal_0_639) 78) (select (m_origin formal_0_639) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_641 () FormalMachine (FormalWriteFromOrigin formal_0_640 67 78))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_641)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_641) (select (m_origin formal_0_641) 53) (select (m_origin formal_0_641) 75)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_641) (select (m_origin formal_0_641) 53) (select (m_origin formal_0_641) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_642 () FormalMachine (FormalCallback formal_0_641 boundary_0 (select (m_origin formal_0_641) 53) (select (m_origin formal_0_641) 75)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_643 () FormalMachine (FormalWriteFromOrigin formal_0_642 67 53))
; source callback case=duplicate-class-ancestor-pivot phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_643)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_643) (select (m_origin formal_0_643) 9) (select (m_origin formal_0_643) 75)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_643) (select (m_origin formal_0_643) 9) (select (m_origin formal_0_643) 75)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_644 () FormalMachine (FormalCallback formal_0_643 boundary_0 (select (m_origin formal_0_643) 9) (select (m_origin formal_0_643) 75)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_645 () FormalMachine (FormalWriteFromOrigin formal_0_644 68 9))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_646 () FormalMachine (FormalWriteFromOrigin formal_0_645 79 17))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_647 () FormalMachine (FormalSwap formal_0_646 54 67))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:1]:initial-compare
(assert (not (m_panicked formal_0_647)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_647) (select (m_origin formal_0_647) 42) (select (m_origin formal_0_647) 53)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_647) (select (m_origin formal_0_647) 42) (select (m_origin formal_0_647) 53)) false))
; source callback transition phase=insert-tail[54:67:1]:initial-compare
(define-fun formal_0_648 () FormalMachine (FormalCallback formal_0_647 boundary_0 (select (m_origin formal_0_647) 42) (select (m_origin formal_0_647) 53)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:2]:initial-compare
(assert (not (m_panicked formal_0_648)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_648) (select (m_origin formal_0_648) 60) (select (m_origin formal_0_648) 42)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_648) (select (m_origin formal_0_648) 60) (select (m_origin formal_0_648) 42)) false))
; source callback transition phase=insert-tail[54:67:2]:initial-compare
(define-fun formal_0_649 () FormalMachine (FormalCallback formal_0_648 boundary_0 (select (m_origin formal_0_648) 60) (select (m_origin formal_0_648) 42)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:3]:initial-compare
(assert (not (m_panicked formal_0_649)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_649) (select (m_origin formal_0_649) 61) (select (m_origin formal_0_649) 60)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_649) (select (m_origin formal_0_649) 61) (select (m_origin formal_0_649) 60)) false))
; source callback transition phase=insert-tail[54:67:3]:initial-compare
(define-fun formal_0_650 () FormalMachine (FormalCallback formal_0_649 boundary_0 (select (m_origin formal_0_649) 61) (select (m_origin formal_0_649) 60)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:4]:initial-compare
(assert (not (m_panicked formal_0_650)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_650) (select (m_origin formal_0_650) 62) (select (m_origin formal_0_650) 61)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_650) (select (m_origin formal_0_650) 62) (select (m_origin formal_0_650) 61)) false))
; source callback transition phase=insert-tail[54:67:4]:initial-compare
(define-fun formal_0_651 () FormalMachine (FormalCallback formal_0_650 boundary_0 (select (m_origin formal_0_650) 62) (select (m_origin formal_0_650) 61)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:5]:initial-compare
(assert (not (m_panicked formal_0_651)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_651) (select (m_origin formal_0_651) 36) (select (m_origin formal_0_651) 62)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_651) (select (m_origin formal_0_651) 36) (select (m_origin formal_0_651) 62)) false))
; source callback transition phase=insert-tail[54:67:5]:initial-compare
(define-fun formal_0_652 () FormalMachine (FormalCallback formal_0_651 boundary_0 (select (m_origin formal_0_651) 36) (select (m_origin formal_0_651) 62)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:6]:initial-compare
(assert (not (m_panicked formal_0_652)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_652) (select (m_origin formal_0_652) 26) (select (m_origin formal_0_652) 36)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_652) (select (m_origin formal_0_652) 26) (select (m_origin formal_0_652) 36)) false))
; source callback transition phase=insert-tail[54:67:6]:initial-compare
(define-fun formal_0_653 () FormalMachine (FormalCallback formal_0_652 boundary_0 (select (m_origin formal_0_652) 26) (select (m_origin formal_0_652) 36)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:7]:initial-compare
(assert (not (m_panicked formal_0_653)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_653) (select (m_origin formal_0_653) 37) (select (m_origin formal_0_653) 26)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_653) (select (m_origin formal_0_653) 37) (select (m_origin formal_0_653) 26)) false))
; source callback transition phase=insert-tail[54:67:7]:initial-compare
(define-fun formal_0_654 () FormalMachine (FormalCallback formal_0_653 boundary_0 (select (m_origin formal_0_653) 37) (select (m_origin formal_0_653) 26)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:8]:initial-compare
(assert (not (m_panicked formal_0_654)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_654) (select (m_origin formal_0_654) 68) (select (m_origin formal_0_654) 37)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_654) (select (m_origin formal_0_654) 68) (select (m_origin formal_0_654) 37)) false))
; source callback transition phase=insert-tail[54:67:8]:initial-compare
(define-fun formal_0_655 () FormalMachine (FormalCallback formal_0_654 boundary_0 (select (m_origin formal_0_654) 68) (select (m_origin formal_0_654) 37)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:9]:initial-compare
(assert (not (m_panicked formal_0_655)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_655) (select (m_origin formal_0_655) 46) (select (m_origin formal_0_655) 68)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_655) (select (m_origin formal_0_655) 46) (select (m_origin formal_0_655) 68)) false))
; source callback transition phase=insert-tail[54:67:9]:initial-compare
(define-fun formal_0_656 () FormalMachine (FormalCallback formal_0_655 boundary_0 (select (m_origin formal_0_655) 46) (select (m_origin formal_0_655) 68)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:10]:initial-compare
(assert (not (m_panicked formal_0_656)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_656) (select (m_origin formal_0_656) 38) (select (m_origin formal_0_656) 46)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_656) (select (m_origin formal_0_656) 38) (select (m_origin formal_0_656) 46)) false))
; source callback transition phase=insert-tail[54:67:10]:initial-compare
(define-fun formal_0_657 () FormalMachine (FormalCallback formal_0_656 boundary_0 (select (m_origin formal_0_656) 38) (select (m_origin formal_0_656) 46)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:11]:initial-compare
(assert (not (m_panicked formal_0_657)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_657) (select (m_origin formal_0_657) 16) (select (m_origin formal_0_657) 38)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_657) (select (m_origin formal_0_657) 16) (select (m_origin formal_0_657) 38)) false))
; source callback transition phase=insert-tail[54:67:11]:initial-compare
(define-fun formal_0_658 () FormalMachine (FormalCallback formal_0_657 boundary_0 (select (m_origin formal_0_657) 16) (select (m_origin formal_0_657) 38)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[54:67:12]:initial-compare
(assert (not (m_panicked formal_0_658)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_658) (select (m_origin formal_0_658) 52) (select (m_origin formal_0_658) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_658) (select (m_origin formal_0_658) 52) (select (m_origin formal_0_658) 16)) false))
; source callback transition phase=insert-tail[54:67:12]:initial-compare
(define-fun formal_0_659 () FormalMachine (FormalCallback formal_0_658 boundary_0 (select (m_origin formal_0_658) 52) (select (m_origin formal_0_658) 16)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:1]:initial-compare
(assert (not (m_panicked formal_0_659)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_659) (select (m_origin formal_0_659) 33) (select (m_origin formal_0_659) 9)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_659) (select (m_origin formal_0_659) 33) (select (m_origin formal_0_659) 9)) false))
; source callback transition phase=insert-tail[68:80:1]:initial-compare
(define-fun formal_0_660 () FormalMachine (FormalCallback formal_0_659 boundary_0 (select (m_origin formal_0_659) 33) (select (m_origin formal_0_659) 9)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:2]:initial-compare
(assert (not (m_panicked formal_0_660)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_660) (select (m_origin formal_0_660) 48) (select (m_origin formal_0_660) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_660) (select (m_origin formal_0_660) 48) (select (m_origin formal_0_660) 33)) false))
; source callback transition phase=insert-tail[68:80:2]:initial-compare
(define-fun formal_0_661 () FormalMachine (FormalCallback formal_0_660 boundary_0 (select (m_origin formal_0_660) 48) (select (m_origin formal_0_660) 33)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:3]:initial-compare
(assert (not (m_panicked formal_0_661)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_661) (select (m_origin formal_0_661) 13) (select (m_origin formal_0_661) 48)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_661) (select (m_origin formal_0_661) 13) (select (m_origin formal_0_661) 48)) false))
; source callback transition phase=insert-tail[68:80:3]:initial-compare
(define-fun formal_0_662 () FormalMachine (FormalCallback formal_0_661 boundary_0 (select (m_origin formal_0_661) 13) (select (m_origin formal_0_661) 48)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:4]:initial-compare
(assert (not (m_panicked formal_0_662)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_662) (select (m_origin formal_0_662) 31) (select (m_origin formal_0_662) 13)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_662) (select (m_origin formal_0_662) 31) (select (m_origin formal_0_662) 13)) false))
; source callback transition phase=insert-tail[68:80:4]:initial-compare
(define-fun formal_0_663 () FormalMachine (FormalCallback formal_0_662 boundary_0 (select (m_origin formal_0_662) 31) (select (m_origin formal_0_662) 13)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:5]:initial-compare
(assert (not (m_panicked formal_0_663)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_663) (select (m_origin formal_0_663) 20) (select (m_origin formal_0_663) 31)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_663) (select (m_origin formal_0_663) 20) (select (m_origin formal_0_663) 31)) false))
; source callback transition phase=insert-tail[68:80:5]:initial-compare
(define-fun formal_0_664 () FormalMachine (FormalCallback formal_0_663 boundary_0 (select (m_origin formal_0_663) 20) (select (m_origin formal_0_663) 31)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:6]:initial-compare
(assert (not (m_panicked formal_0_664)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_664) (select (m_origin formal_0_664) 24) (select (m_origin formal_0_664) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_664) (select (m_origin formal_0_664) 24) (select (m_origin formal_0_664) 20)) false))
; source callback transition phase=insert-tail[68:80:6]:initial-compare
(define-fun formal_0_665 () FormalMachine (FormalCallback formal_0_664 boundary_0 (select (m_origin formal_0_664) 24) (select (m_origin formal_0_664) 20)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:7]:initial-compare
(assert (not (m_panicked formal_0_665)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_665) (select (m_origin formal_0_665) 7) (select (m_origin formal_0_665) 24)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_665) (select (m_origin formal_0_665) 7) (select (m_origin formal_0_665) 24)) false))
; source callback transition phase=insert-tail[68:80:7]:initial-compare
(define-fun formal_0_666 () FormalMachine (FormalCallback formal_0_665 boundary_0 (select (m_origin formal_0_665) 7) (select (m_origin formal_0_665) 24)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:8]:initial-compare
(assert (not (m_panicked formal_0_666)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_666) (select (m_origin formal_0_666) 67) (select (m_origin formal_0_666) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_666) (select (m_origin formal_0_666) 67) (select (m_origin formal_0_666) 7)) false))
; source callback transition phase=insert-tail[68:80:8]:initial-compare
(define-fun formal_0_667 () FormalMachine (FormalCallback formal_0_666 boundary_0 (select (m_origin formal_0_666) 67) (select (m_origin formal_0_666) 7)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:9]:initial-compare
(assert (not (m_panicked formal_0_667)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_667) (select (m_origin formal_0_667) 77) (select (m_origin formal_0_667) 67)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_667) (select (m_origin formal_0_667) 77) (select (m_origin formal_0_667) 67)) false))
; source callback transition phase=insert-tail[68:80:9]:initial-compare
(define-fun formal_0_668 () FormalMachine (FormalCallback formal_0_667 boundary_0 (select (m_origin formal_0_667) 77) (select (m_origin formal_0_667) 67)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:10]:initial-compare
(assert (not (m_panicked formal_0_668)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_668) (select (m_origin formal_0_668) 78) (select (m_origin formal_0_668) 77)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_668) (select (m_origin formal_0_668) 78) (select (m_origin formal_0_668) 77)) false))
; source callback transition phase=insert-tail[68:80:10]:initial-compare
(define-fun formal_0_669 () FormalMachine (FormalCallback formal_0_668 boundary_0 (select (m_origin formal_0_668) 78) (select (m_origin formal_0_668) 77)))
; source callback case=duplicate-class-ancestor-pivot phase=insert-tail[68:80:11]:initial-compare
(assert (not (m_panicked formal_0_669)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_669) (select (m_origin formal_0_669) 17) (select (m_origin formal_0_669) 78)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_669) (select (m_origin formal_0_669) 17) (select (m_origin formal_0_669) 78)) false))
; source callback transition phase=insert-tail[68:80:11]:initial-compare
(define-fun formal_0_670 () FormalMachine (FormalCallback formal_0_669 boundary_0 (select (m_origin formal_0_669) 17) (select (m_origin formal_0_669) 78)))
(define-fun formal_result_0 () Result
  (mkResult
    (m_sequence formal_0_670)
    (m_callback formal_0_670)
    (m_panicked formal_0_670)
    false
    true
    (ite (m_panicked formal_0_670) 1 0)
    (not (m_panicked formal_0_670))
    -1))
(define-fun reference_result_0 () Result (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 42) 1 24) 2 66) 3 18) 4 78) 5 60) 6 0) 7 48) 8 54) 9 30) 10 6) 11 72) 12 12) 13 36) 14 25) 15 37) 16 13) 17 7) 18 1) 19 43) 20 55) 21 19) 22 49) 23 73) 24 31) 25 67) 26 79) 27 61) 28 56) 29 68) 30 14) 31 20) 32 50) 33 2) 34 74) 35 32) 36 8) 37 26) 38 38) 39 62) 40 44) 41 57) 42 39) 43 69) 44 63) 45 21) 46 9) 47 75) 48 27) 49 45) 50 51) 51 33) 52 15) 53 3) 54 46) 55 40) 56 70) 57 34) 58 58) 59 16) 60 10) 61 76) 62 64) 63 22) 64 28) 65 52) 66 4) 67 65) 68 41) 69 77) 70 35) 71 29) 72 71) 73 47) 74 23) 75 11) 76 17) 77 5) 78 53) 79 59) 330 false false true 0 true -1))
; retained source-forcing witness: ancestor-pivot
(assert (= formal_result_0 (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 42) 1 24) 2 66) 3 18) 4 78) 5 60) 6 0) 7 48) 8 54) 9 30) 10 6) 11 72) 12 12) 13 36) 14 25) 15 37) 16 13) 17 7) 18 1) 19 43) 20 55) 21 19) 22 49) 23 73) 24 31) 25 67) 26 79) 27 61) 28 56) 29 68) 30 14) 31 20) 32 50) 33 2) 34 74) 35 32) 36 8) 37 26) 38 38) 39 62) 40 44) 41 57) 42 39) 43 69) 44 63) 45 21) 46 9) 47 75) 48 27) 49 45) 50 51) 51 33) 52 15) 53 3) 54 46) 55 40) 56 70) 57 34) 58 58) 59 16) 60 10) 61 76) 62 64) 63 22) 64 28) 65 52) 66 4) 67 65) 68 41) 69 77) 70 35) 71 29) 72 71) 73 47) 74 23) 75 11) 76 17) 77 5) 78 53) 79 59) 330 false false true 0 true -1)))
(check-sat-using (then ctx-solver-simplify smt))
