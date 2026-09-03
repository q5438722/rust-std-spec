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

; formal source input case=hoare-partition
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
    128
    false
    false))
(define-fun source_initial_0 () FormalMachine
  (mkFormalMachine (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 40) 1 18) 2 16) 3 13) 4 32) 5 29) 6 42) 7 37) 8 4) 9 11) 10 2) 11 44) 12 6) 13 31) 14 34) 15 38) 16 39) 17 22) 18 20) 19 41) 20 10) 21 30) 22 15) 23 21) 24 17) 25 8) 26 19) 27 24) 28 43) 29 23) 30 14) 31 33) 32 27) 33 35) 34 0) 35 3) 36 1) 37 7) 38 25) 39 12) 40 36) 41 26) 42 9) 43 5) 44 28) (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 40) 1 18) 2 16) 3 13) 4 32) 5 29) 6 42) 7 37) 8 4) 9 11) 10 2) 11 44) 12 6) 13 31) 14 34) 15 38) 16 39) 17 22) 18 20) 19 41) 20 10) 21 30) 22 15) 23 21) 24 17) 25 8) 26 19) 27 24) 28 43) 29 23) 30 14) 31 33) 32 27) 33 35) 34 0) 35 3) 36 1) 37 7) 38 25) 39 12) 40 36) 41 26) 42 9) 43 5) 44 28) (b_initial_state boundary_0) false))
(assert (BoundaryWellFormed boundary_0))
; source callback case=hoare-partition phase=find-existing-run:direction
(assert (not (m_panicked source_initial_0)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) false))
; source callback transition phase=find-existing-run:direction
(define-fun formal_0_1 () FormalMachine (FormalCallback source_initial_0 boundary_0 (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)))
; source callback case=hoare-partition phase=find-existing-run:descending
(assert (not (m_panicked formal_0_1)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) false))
; source callback transition phase=find-existing-run:descending
(define-fun formal_0_2 () FormalMachine (FormalCallback formal_0_1 boundary_0 (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)))
; source callback case=hoare-partition phase=find-existing-run:descending
(assert (not (m_panicked formal_0_2)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 3) (select (m_origin formal_0_2) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 3) (select (m_origin formal_0_2) 2)) false))
; source callback transition phase=find-existing-run:descending
(define-fun formal_0_3 () FormalMachine (FormalCallback formal_0_2 boundary_0 (select (m_origin formal_0_2) 3) (select (m_origin formal_0_2) 2)))
; source callback case=hoare-partition phase=find-existing-run:descending
(assert (not (m_panicked formal_0_3)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 4) (select (m_origin formal_0_3) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 4) (select (m_origin formal_0_3) 3)) false))
; source callback transition phase=find-existing-run:descending
(define-fun formal_0_4 () FormalMachine (FormalCallback formal_0_3 boundary_0 (select (m_origin formal_0_3) 4) (select (m_origin formal_0_3) 3)))
; source callback case=hoare-partition phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_4)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 0) (select (m_origin formal_0_4) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 0) (select (m_origin formal_0_4) 20)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_5 () FormalMachine (FormalCallback formal_0_4 boundary_0 (select (m_origin formal_0_4) 0) (select (m_origin formal_0_4) 20)))
; source callback case=hoare-partition phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_5)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_5) (select (m_origin formal_0_5) 0) (select (m_origin formal_0_5) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_5) (select (m_origin formal_0_5) 0) (select (m_origin formal_0_5) 35)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_6 () FormalMachine (FormalCallback formal_0_5 boundary_0 (select (m_origin formal_0_5) 0) (select (m_origin formal_0_5) 35)))
; source callback case=hoare-partition phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_6)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 20) (select (m_origin formal_0_6) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 20) (select (m_origin formal_0_6) 35)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_7 () FormalMachine (FormalCallback formal_0_6 boundary_0 (select (m_origin formal_0_6) 20) (select (m_origin formal_0_6) 35)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_8 () FormalMachine (FormalSwap formal_0_7 0 20))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_8)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 1) (select (m_origin formal_0_8) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 1) (select (m_origin formal_0_8) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_9 () FormalMachine (FormalCallback formal_0_8 boundary_0 (select (m_origin formal_0_8) 1) (select (m_origin formal_0_8) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_9)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_9) (select (m_origin formal_0_9) 44) (select (m_origin formal_0_9) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_9) (select (m_origin formal_0_9) 44) (select (m_origin formal_0_9) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_10 () FormalMachine (FormalCallback formal_0_9 boundary_0 (select (m_origin formal_0_9) 44) (select (m_origin formal_0_9) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_10)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_10) (select (m_origin formal_0_10) 43) (select (m_origin formal_0_10) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_10) (select (m_origin formal_0_10) 43) (select (m_origin formal_0_10) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_11 () FormalMachine (FormalCallback formal_0_10 boundary_0 (select (m_origin formal_0_10) 43) (select (m_origin formal_0_10) 20)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_12 () FormalMachine (FormalWriteFromOrigin formal_0_11 1 43))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_12)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_12) (select (m_origin formal_0_12) 2) (select (m_origin formal_0_12) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_12) (select (m_origin formal_0_12) 2) (select (m_origin formal_0_12) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_13 () FormalMachine (FormalCallback formal_0_12 boundary_0 (select (m_origin formal_0_12) 2) (select (m_origin formal_0_12) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_13)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_13) (select (m_origin formal_0_13) 42) (select (m_origin formal_0_13) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_13) (select (m_origin formal_0_13) 42) (select (m_origin formal_0_13) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_14 () FormalMachine (FormalCallback formal_0_13 boundary_0 (select (m_origin formal_0_13) 42) (select (m_origin formal_0_13) 20)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_15 () FormalMachine (FormalWriteFromOrigin formal_0_14 2 42))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_16 () FormalMachine (FormalWriteFromOrigin formal_0_15 43 2))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_16)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_16) (select (m_origin formal_0_16) 3) (select (m_origin formal_0_16) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_16) (select (m_origin formal_0_16) 3) (select (m_origin formal_0_16) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_17 () FormalMachine (FormalCallback formal_0_16 boundary_0 (select (m_origin formal_0_16) 3) (select (m_origin formal_0_16) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_17)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_17) (select (m_origin formal_0_17) 41) (select (m_origin formal_0_17) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_17) (select (m_origin formal_0_17) 41) (select (m_origin formal_0_17) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_18 () FormalMachine (FormalCallback formal_0_17 boundary_0 (select (m_origin formal_0_17) 41) (select (m_origin formal_0_17) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_18)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_18) (select (m_origin formal_0_18) 40) (select (m_origin formal_0_18) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_18) (select (m_origin formal_0_18) 40) (select (m_origin formal_0_18) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_19 () FormalMachine (FormalCallback formal_0_18 boundary_0 (select (m_origin formal_0_18) 40) (select (m_origin formal_0_18) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_19)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_19) (select (m_origin formal_0_19) 39) (select (m_origin formal_0_19) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_19) (select (m_origin formal_0_19) 39) (select (m_origin formal_0_19) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_20 () FormalMachine (FormalCallback formal_0_19 boundary_0 (select (m_origin formal_0_19) 39) (select (m_origin formal_0_19) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_20)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 38) (select (m_origin formal_0_20) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 38) (select (m_origin formal_0_20) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_21 () FormalMachine (FormalCallback formal_0_20 boundary_0 (select (m_origin formal_0_20) 38) (select (m_origin formal_0_20) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_21)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_21) (select (m_origin formal_0_21) 37) (select (m_origin formal_0_21) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_21) (select (m_origin formal_0_21) 37) (select (m_origin formal_0_21) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_22 () FormalMachine (FormalCallback formal_0_21 boundary_0 (select (m_origin formal_0_21) 37) (select (m_origin formal_0_21) 20)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_23 () FormalMachine (FormalWriteFromOrigin formal_0_22 3 37))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_24 () FormalMachine (FormalWriteFromOrigin formal_0_23 42 3))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_24)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_24) (select (m_origin formal_0_24) 4) (select (m_origin formal_0_24) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_24) (select (m_origin formal_0_24) 4) (select (m_origin formal_0_24) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_25 () FormalMachine (FormalCallback formal_0_24 boundary_0 (select (m_origin formal_0_24) 4) (select (m_origin formal_0_24) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_25)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 36) (select (m_origin formal_0_25) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 36) (select (m_origin formal_0_25) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_26 () FormalMachine (FormalCallback formal_0_25 boundary_0 (select (m_origin formal_0_25) 36) (select (m_origin formal_0_25) 20)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_27 () FormalMachine (FormalWriteFromOrigin formal_0_26 4 36))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_28 () FormalMachine (FormalWriteFromOrigin formal_0_27 37 4))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_28)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_28) (select (m_origin formal_0_28) 5) (select (m_origin formal_0_28) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_28) (select (m_origin formal_0_28) 5) (select (m_origin formal_0_28) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_29 () FormalMachine (FormalCallback formal_0_28 boundary_0 (select (m_origin formal_0_28) 5) (select (m_origin formal_0_28) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_29)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_29) (select (m_origin formal_0_29) 35) (select (m_origin formal_0_29) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_29) (select (m_origin formal_0_29) 35) (select (m_origin formal_0_29) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_30 () FormalMachine (FormalCallback formal_0_29 boundary_0 (select (m_origin formal_0_29) 35) (select (m_origin formal_0_29) 20)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_31 () FormalMachine (FormalWriteFromOrigin formal_0_30 5 35))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_32 () FormalMachine (FormalWriteFromOrigin formal_0_31 36 5))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_32)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_32) (select (m_origin formal_0_32) 6) (select (m_origin formal_0_32) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_32) (select (m_origin formal_0_32) 6) (select (m_origin formal_0_32) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_33 () FormalMachine (FormalCallback formal_0_32 boundary_0 (select (m_origin formal_0_32) 6) (select (m_origin formal_0_32) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_33)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_33) (select (m_origin formal_0_33) 34) (select (m_origin formal_0_33) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_33) (select (m_origin formal_0_33) 34) (select (m_origin formal_0_33) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_34 () FormalMachine (FormalCallback formal_0_33 boundary_0 (select (m_origin formal_0_33) 34) (select (m_origin formal_0_33) 20)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_35 () FormalMachine (FormalWriteFromOrigin formal_0_34 6 34))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_36 () FormalMachine (FormalWriteFromOrigin formal_0_35 35 6))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_36)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_36) (select (m_origin formal_0_36) 7) (select (m_origin formal_0_36) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_36) (select (m_origin formal_0_36) 7) (select (m_origin formal_0_36) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_37 () FormalMachine (FormalCallback formal_0_36 boundary_0 (select (m_origin formal_0_36) 7) (select (m_origin formal_0_36) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_37)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_37) (select (m_origin formal_0_37) 33) (select (m_origin formal_0_37) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_37) (select (m_origin formal_0_37) 33) (select (m_origin formal_0_37) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_38 () FormalMachine (FormalCallback formal_0_37 boundary_0 (select (m_origin formal_0_37) 33) (select (m_origin formal_0_37) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_38)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 32) (select (m_origin formal_0_38) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 32) (select (m_origin formal_0_38) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_39 () FormalMachine (FormalCallback formal_0_38 boundary_0 (select (m_origin formal_0_38) 32) (select (m_origin formal_0_38) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_39)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_39) (select (m_origin formal_0_39) 31) (select (m_origin formal_0_39) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_39) (select (m_origin formal_0_39) 31) (select (m_origin formal_0_39) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_40 () FormalMachine (FormalCallback formal_0_39 boundary_0 (select (m_origin formal_0_39) 31) (select (m_origin formal_0_39) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_40)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_40) (select (m_origin formal_0_40) 30) (select (m_origin formal_0_40) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_40) (select (m_origin formal_0_40) 30) (select (m_origin formal_0_40) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_41 () FormalMachine (FormalCallback formal_0_40 boundary_0 (select (m_origin formal_0_40) 30) (select (m_origin formal_0_40) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_41)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 29) (select (m_origin formal_0_41) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 29) (select (m_origin formal_0_41) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_42 () FormalMachine (FormalCallback formal_0_41 boundary_0 (select (m_origin formal_0_41) 29) (select (m_origin formal_0_41) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_42)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_42) (select (m_origin formal_0_42) 28) (select (m_origin formal_0_42) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_42) (select (m_origin formal_0_42) 28) (select (m_origin formal_0_42) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_43 () FormalMachine (FormalCallback formal_0_42 boundary_0 (select (m_origin formal_0_42) 28) (select (m_origin formal_0_42) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_43)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_43) (select (m_origin formal_0_43) 27) (select (m_origin formal_0_43) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_43) (select (m_origin formal_0_43) 27) (select (m_origin formal_0_43) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_44 () FormalMachine (FormalCallback formal_0_43 boundary_0 (select (m_origin formal_0_43) 27) (select (m_origin formal_0_43) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_44)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 26) (select (m_origin formal_0_44) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 26) (select (m_origin formal_0_44) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_45 () FormalMachine (FormalCallback formal_0_44 boundary_0 (select (m_origin formal_0_44) 26) (select (m_origin formal_0_44) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_45)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_45) (select (m_origin formal_0_45) 25) (select (m_origin formal_0_45) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_45) (select (m_origin formal_0_45) 25) (select (m_origin formal_0_45) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_46 () FormalMachine (FormalCallback formal_0_45 boundary_0 (select (m_origin formal_0_45) 25) (select (m_origin formal_0_45) 20)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_47 () FormalMachine (FormalWriteFromOrigin formal_0_46 7 25))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_48 () FormalMachine (FormalWriteFromOrigin formal_0_47 34 7))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_48)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 8) (select (m_origin formal_0_48) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 8) (select (m_origin formal_0_48) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_49 () FormalMachine (FormalCallback formal_0_48 boundary_0 (select (m_origin formal_0_48) 8) (select (m_origin formal_0_48) 20)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_49)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_49) (select (m_origin formal_0_49) 9) (select (m_origin formal_0_49) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_49) (select (m_origin formal_0_49) 9) (select (m_origin formal_0_49) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_50 () FormalMachine (FormalCallback formal_0_49 boundary_0 (select (m_origin formal_0_49) 9) (select (m_origin formal_0_49) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_50)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_50) (select (m_origin formal_0_50) 24) (select (m_origin formal_0_50) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_50) (select (m_origin formal_0_50) 24) (select (m_origin formal_0_50) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_51 () FormalMachine (FormalCallback formal_0_50 boundary_0 (select (m_origin formal_0_50) 24) (select (m_origin formal_0_50) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_51)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_51) (select (m_origin formal_0_51) 23) (select (m_origin formal_0_51) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_51) (select (m_origin formal_0_51) 23) (select (m_origin formal_0_51) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_52 () FormalMachine (FormalCallback formal_0_51 boundary_0 (select (m_origin formal_0_51) 23) (select (m_origin formal_0_51) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_52)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_52) (select (m_origin formal_0_52) 22) (select (m_origin formal_0_52) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_52) (select (m_origin formal_0_52) 22) (select (m_origin formal_0_52) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_53 () FormalMachine (FormalCallback formal_0_52 boundary_0 (select (m_origin formal_0_52) 22) (select (m_origin formal_0_52) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_53)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_53) (select (m_origin formal_0_53) 21) (select (m_origin formal_0_53) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_53) (select (m_origin formal_0_53) 21) (select (m_origin formal_0_53) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_54 () FormalMachine (FormalCallback formal_0_53 boundary_0 (select (m_origin formal_0_53) 21) (select (m_origin formal_0_53) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_54)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_54) (select (m_origin formal_0_54) 0) (select (m_origin formal_0_54) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_54) (select (m_origin formal_0_54) 0) (select (m_origin formal_0_54) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_55 () FormalMachine (FormalCallback formal_0_54 boundary_0 (select (m_origin formal_0_54) 0) (select (m_origin formal_0_54) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_55)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_55) (select (m_origin formal_0_55) 19) (select (m_origin formal_0_55) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_55) (select (m_origin formal_0_55) 19) (select (m_origin formal_0_55) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_56 () FormalMachine (FormalCallback formal_0_55 boundary_0 (select (m_origin formal_0_55) 19) (select (m_origin formal_0_55) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_56)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_56) (select (m_origin formal_0_56) 18) (select (m_origin formal_0_56) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_56) (select (m_origin formal_0_56) 18) (select (m_origin formal_0_56) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_57 () FormalMachine (FormalCallback formal_0_56 boundary_0 (select (m_origin formal_0_56) 18) (select (m_origin formal_0_56) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_57)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_57) (select (m_origin formal_0_57) 17) (select (m_origin formal_0_57) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_57) (select (m_origin formal_0_57) 17) (select (m_origin formal_0_57) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_58 () FormalMachine (FormalCallback formal_0_57 boundary_0 (select (m_origin formal_0_57) 17) (select (m_origin formal_0_57) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_58)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_58) (select (m_origin formal_0_58) 16) (select (m_origin formal_0_58) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_58) (select (m_origin formal_0_58) 16) (select (m_origin formal_0_58) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_59 () FormalMachine (FormalCallback formal_0_58 boundary_0 (select (m_origin formal_0_58) 16) (select (m_origin formal_0_58) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_59)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_59) (select (m_origin formal_0_59) 15) (select (m_origin formal_0_59) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_59) (select (m_origin formal_0_59) 15) (select (m_origin formal_0_59) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_60 () FormalMachine (FormalCallback formal_0_59 boundary_0 (select (m_origin formal_0_59) 15) (select (m_origin formal_0_59) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_60)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_60) (select (m_origin formal_0_60) 14) (select (m_origin formal_0_60) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_60) (select (m_origin formal_0_60) 14) (select (m_origin formal_0_60) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_61 () FormalMachine (FormalCallback formal_0_60 boundary_0 (select (m_origin formal_0_60) 14) (select (m_origin formal_0_60) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_61)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_61) (select (m_origin formal_0_61) 13) (select (m_origin formal_0_61) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_61) (select (m_origin formal_0_61) 13) (select (m_origin formal_0_61) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_62 () FormalMachine (FormalCallback formal_0_61 boundary_0 (select (m_origin formal_0_61) 13) (select (m_origin formal_0_61) 20)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_62)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_62) (select (m_origin formal_0_62) 12) (select (m_origin formal_0_62) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_62) (select (m_origin formal_0_62) 12) (select (m_origin formal_0_62) 20)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_63 () FormalMachine (FormalCallback formal_0_62 boundary_0 (select (m_origin formal_0_62) 12) (select (m_origin formal_0_62) 20)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_64 () FormalMachine (FormalWriteFromOrigin formal_0_63 9 12))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_65 () FormalMachine (FormalWriteFromOrigin formal_0_64 25 9))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_65)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_65) (select (m_origin formal_0_65) 10) (select (m_origin formal_0_65) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_65) (select (m_origin formal_0_65) 10) (select (m_origin formal_0_65) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_66 () FormalMachine (FormalCallback formal_0_65 boundary_0 (select (m_origin formal_0_65) 10) (select (m_origin formal_0_65) 20)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_66)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_66) (select (m_origin formal_0_66) 11) (select (m_origin formal_0_66) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_66) (select (m_origin formal_0_66) 11) (select (m_origin formal_0_66) 20)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_67 () FormalMachine (FormalCallback formal_0_66 boundary_0 (select (m_origin formal_0_66) 11) (select (m_origin formal_0_66) 20)))
; source write kind=gap-guard-restore phase=partition-hoare-branchy-cyclic
(define-fun formal_0_68 () FormalMachine (FormalWriteFromOrigin formal_0_67 12 1))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_69 () FormalMachine (FormalSwap formal_0_68 0 10))
; source callback case=hoare-partition phase=insert-tail[0:10:1]:initial-compare
(assert (not (m_panicked formal_0_69)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 43) (select (m_origin formal_0_69) 10)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 43) (select (m_origin formal_0_69) 10)) false))
; source callback transition phase=insert-tail[0:10:1]:initial-compare
(define-fun formal_0_70 () FormalMachine (FormalCallback formal_0_69 boundary_0 (select (m_origin formal_0_69) 43) (select (m_origin formal_0_69) 10)))
; source callback case=hoare-partition phase=insert-tail[0:10:2]:initial-compare
(assert (not (m_panicked formal_0_70)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_70) (select (m_origin formal_0_70) 42) (select (m_origin formal_0_70) 43)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_70) (select (m_origin formal_0_70) 42) (select (m_origin formal_0_70) 43)) false))
; source callback transition phase=insert-tail[0:10:2]:initial-compare
(define-fun formal_0_71 () FormalMachine (FormalCallback formal_0_70 boundary_0 (select (m_origin formal_0_70) 42) (select (m_origin formal_0_70) 43)))
; source callback case=hoare-partition phase=insert-tail[0:10:3]:initial-compare
(assert (not (m_panicked formal_0_71)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_71) (select (m_origin formal_0_71) 37) (select (m_origin formal_0_71) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_71) (select (m_origin formal_0_71) 37) (select (m_origin formal_0_71) 42)) false))
; source callback transition phase=insert-tail[0:10:3]:initial-compare
(define-fun formal_0_72 () FormalMachine (FormalCallback formal_0_71 boundary_0 (select (m_origin formal_0_71) 37) (select (m_origin formal_0_71) 42)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:3]
(define-fun formal_0_73 () FormalMachine (FormalWriteFromOrigin formal_0_72 3 42))
; source callback case=hoare-partition phase=insert-tail[0:10:3]:sift-compare
(assert (not (m_panicked formal_0_73)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 37) (select (m_origin formal_0_73) 43)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 37) (select (m_origin formal_0_73) 43)) false))
; source callback transition phase=insert-tail[0:10:3]:sift-compare
(define-fun formal_0_74 () FormalMachine (FormalCallback formal_0_73 boundary_0 (select (m_origin formal_0_73) 37) (select (m_origin formal_0_73) 43)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:10:3]
(define-fun formal_0_75 () FormalMachine (FormalWriteFromOrigin formal_0_74 2 37))
; source callback case=hoare-partition phase=insert-tail[0:10:4]:initial-compare
(assert (not (m_panicked formal_0_75)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 36) (select (m_origin formal_0_75) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 36) (select (m_origin formal_0_75) 42)) false))
; source callback transition phase=insert-tail[0:10:4]:initial-compare
(define-fun formal_0_76 () FormalMachine (FormalCallback formal_0_75 boundary_0 (select (m_origin formal_0_75) 36) (select (m_origin formal_0_75) 42)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:4]
(define-fun formal_0_77 () FormalMachine (FormalWriteFromOrigin formal_0_76 4 42))
; source callback case=hoare-partition phase=insert-tail[0:10:4]:sift-compare
(assert (not (m_panicked formal_0_77)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_77) (select (m_origin formal_0_77) 36) (select (m_origin formal_0_77) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_77) (select (m_origin formal_0_77) 36) (select (m_origin formal_0_77) 37)) false))
; source callback transition phase=insert-tail[0:10:4]:sift-compare
(define-fun formal_0_78 () FormalMachine (FormalCallback formal_0_77 boundary_0 (select (m_origin formal_0_77) 36) (select (m_origin formal_0_77) 37)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:4]
(define-fun formal_0_79 () FormalMachine (FormalWriteFromOrigin formal_0_78 3 37))
; source callback case=hoare-partition phase=insert-tail[0:10:4]:sift-compare
(assert (not (m_panicked formal_0_79)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_79) (select (m_origin formal_0_79) 36) (select (m_origin formal_0_79) 43)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_79) (select (m_origin formal_0_79) 36) (select (m_origin formal_0_79) 43)) false))
; source callback transition phase=insert-tail[0:10:4]:sift-compare
(define-fun formal_0_80 () FormalMachine (FormalCallback formal_0_79 boundary_0 (select (m_origin formal_0_79) 36) (select (m_origin formal_0_79) 43)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:4]
(define-fun formal_0_81 () FormalMachine (FormalWriteFromOrigin formal_0_80 2 43))
; source callback case=hoare-partition phase=insert-tail[0:10:4]:sift-compare
(assert (not (m_panicked formal_0_81)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 36) (select (m_origin formal_0_81) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 36) (select (m_origin formal_0_81) 10)) false))
; source callback transition phase=insert-tail[0:10:4]:sift-compare
(define-fun formal_0_82 () FormalMachine (FormalCallback formal_0_81 boundary_0 (select (m_origin formal_0_81) 36) (select (m_origin formal_0_81) 10)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:4]
(define-fun formal_0_83 () FormalMachine (FormalWriteFromOrigin formal_0_82 1 10))
; source write kind=copy-on-drop-restore phase=insert-tail[0:10:4]
(define-fun formal_0_84 () FormalMachine (FormalWriteFromOrigin formal_0_83 0 36))
; source callback case=hoare-partition phase=insert-tail[0:10:5]:initial-compare
(assert (not (m_panicked formal_0_84)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_84) (select (m_origin formal_0_84) 35) (select (m_origin formal_0_84) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_84) (select (m_origin formal_0_84) 35) (select (m_origin formal_0_84) 42)) false))
; source callback transition phase=insert-tail[0:10:5]:initial-compare
(define-fun formal_0_85 () FormalMachine (FormalCallback formal_0_84 boundary_0 (select (m_origin formal_0_84) 35) (select (m_origin formal_0_84) 42)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:5]
(define-fun formal_0_86 () FormalMachine (FormalWriteFromOrigin formal_0_85 5 42))
; source callback case=hoare-partition phase=insert-tail[0:10:5]:sift-compare
(assert (not (m_panicked formal_0_86)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 35) (select (m_origin formal_0_86) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 35) (select (m_origin formal_0_86) 37)) false))
; source callback transition phase=insert-tail[0:10:5]:sift-compare
(define-fun formal_0_87 () FormalMachine (FormalCallback formal_0_86 boundary_0 (select (m_origin formal_0_86) 35) (select (m_origin formal_0_86) 37)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:5]
(define-fun formal_0_88 () FormalMachine (FormalWriteFromOrigin formal_0_87 4 37))
; source callback case=hoare-partition phase=insert-tail[0:10:5]:sift-compare
(assert (not (m_panicked formal_0_88)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_88) (select (m_origin formal_0_88) 35) (select (m_origin formal_0_88) 43)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_88) (select (m_origin formal_0_88) 35) (select (m_origin formal_0_88) 43)) false))
; source callback transition phase=insert-tail[0:10:5]:sift-compare
(define-fun formal_0_89 () FormalMachine (FormalCallback formal_0_88 boundary_0 (select (m_origin formal_0_88) 35) (select (m_origin formal_0_88) 43)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:5]
(define-fun formal_0_90 () FormalMachine (FormalWriteFromOrigin formal_0_89 3 43))
; source callback case=hoare-partition phase=insert-tail[0:10:5]:sift-compare
(assert (not (m_panicked formal_0_90)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_90) (select (m_origin formal_0_90) 35) (select (m_origin formal_0_90) 10)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_90) (select (m_origin formal_0_90) 35) (select (m_origin formal_0_90) 10)) false))
; source callback transition phase=insert-tail[0:10:5]:sift-compare
(define-fun formal_0_91 () FormalMachine (FormalCallback formal_0_90 boundary_0 (select (m_origin formal_0_90) 35) (select (m_origin formal_0_90) 10)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:10:5]
(define-fun formal_0_92 () FormalMachine (FormalWriteFromOrigin formal_0_91 2 35))
; source callback case=hoare-partition phase=insert-tail[0:10:6]:initial-compare
(assert (not (m_panicked formal_0_92)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_92) (select (m_origin formal_0_92) 34) (select (m_origin formal_0_92) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_92) (select (m_origin formal_0_92) 34) (select (m_origin formal_0_92) 42)) false))
; source callback transition phase=insert-tail[0:10:6]:initial-compare
(define-fun formal_0_93 () FormalMachine (FormalCallback formal_0_92 boundary_0 (select (m_origin formal_0_92) 34) (select (m_origin formal_0_92) 42)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:6]
(define-fun formal_0_94 () FormalMachine (FormalWriteFromOrigin formal_0_93 6 42))
; source callback case=hoare-partition phase=insert-tail[0:10:6]:sift-compare
(assert (not (m_panicked formal_0_94)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_94) (select (m_origin formal_0_94) 34) (select (m_origin formal_0_94) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_94) (select (m_origin formal_0_94) 34) (select (m_origin formal_0_94) 37)) false))
; source callback transition phase=insert-tail[0:10:6]:sift-compare
(define-fun formal_0_95 () FormalMachine (FormalCallback formal_0_94 boundary_0 (select (m_origin formal_0_94) 34) (select (m_origin formal_0_94) 37)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:6]
(define-fun formal_0_96 () FormalMachine (FormalWriteFromOrigin formal_0_95 5 37))
; source callback case=hoare-partition phase=insert-tail[0:10:6]:sift-compare
(assert (not (m_panicked formal_0_96)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_96) (select (m_origin formal_0_96) 34) (select (m_origin formal_0_96) 43)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_96) (select (m_origin formal_0_96) 34) (select (m_origin formal_0_96) 43)) false))
; source callback transition phase=insert-tail[0:10:6]:sift-compare
(define-fun formal_0_97 () FormalMachine (FormalCallback formal_0_96 boundary_0 (select (m_origin formal_0_96) 34) (select (m_origin formal_0_96) 43)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:6]
(define-fun formal_0_98 () FormalMachine (FormalWriteFromOrigin formal_0_97 4 43))
; source callback case=hoare-partition phase=insert-tail[0:10:6]:sift-compare
(assert (not (m_panicked formal_0_98)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_98) (select (m_origin formal_0_98) 34) (select (m_origin formal_0_98) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_98) (select (m_origin formal_0_98) 34) (select (m_origin formal_0_98) 35)) false))
; source callback transition phase=insert-tail[0:10:6]:sift-compare
(define-fun formal_0_99 () FormalMachine (FormalCallback formal_0_98 boundary_0 (select (m_origin formal_0_98) 34) (select (m_origin formal_0_98) 35)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:6]
(define-fun formal_0_100 () FormalMachine (FormalWriteFromOrigin formal_0_99 3 35))
; source callback case=hoare-partition phase=insert-tail[0:10:6]:sift-compare
(assert (not (m_panicked formal_0_100)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_100) (select (m_origin formal_0_100) 34) (select (m_origin formal_0_100) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_100) (select (m_origin formal_0_100) 34) (select (m_origin formal_0_100) 10)) false))
; source callback transition phase=insert-tail[0:10:6]:sift-compare
(define-fun formal_0_101 () FormalMachine (FormalCallback formal_0_100 boundary_0 (select (m_origin formal_0_100) 34) (select (m_origin formal_0_100) 10)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:6]
(define-fun formal_0_102 () FormalMachine (FormalWriteFromOrigin formal_0_101 2 10))
; source callback case=hoare-partition phase=insert-tail[0:10:6]:sift-compare
(assert (not (m_panicked formal_0_102)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_102) (select (m_origin formal_0_102) 34) (select (m_origin formal_0_102) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_102) (select (m_origin formal_0_102) 34) (select (m_origin formal_0_102) 36)) false))
; source callback transition phase=insert-tail[0:10:6]:sift-compare
(define-fun formal_0_103 () FormalMachine (FormalCallback formal_0_102 boundary_0 (select (m_origin formal_0_102) 34) (select (m_origin formal_0_102) 36)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:6]
(define-fun formal_0_104 () FormalMachine (FormalWriteFromOrigin formal_0_103 1 36))
; source write kind=copy-on-drop-restore phase=insert-tail[0:10:6]
(define-fun formal_0_105 () FormalMachine (FormalWriteFromOrigin formal_0_104 0 34))
; source callback case=hoare-partition phase=insert-tail[0:10:7]:initial-compare
(assert (not (m_panicked formal_0_105)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_105) (select (m_origin formal_0_105) 25) (select (m_origin formal_0_105) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_105) (select (m_origin formal_0_105) 25) (select (m_origin formal_0_105) 42)) false))
; source callback transition phase=insert-tail[0:10:7]:initial-compare
(define-fun formal_0_106 () FormalMachine (FormalCallback formal_0_105 boundary_0 (select (m_origin formal_0_105) 25) (select (m_origin formal_0_105) 42)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:7]
(define-fun formal_0_107 () FormalMachine (FormalWriteFromOrigin formal_0_106 7 42))
; source callback case=hoare-partition phase=insert-tail[0:10:7]:sift-compare
(assert (not (m_panicked formal_0_107)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_107) (select (m_origin formal_0_107) 25) (select (m_origin formal_0_107) 37)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_107) (select (m_origin formal_0_107) 25) (select (m_origin formal_0_107) 37)) false))
; source callback transition phase=insert-tail[0:10:7]:sift-compare
(define-fun formal_0_108 () FormalMachine (FormalCallback formal_0_107 boundary_0 (select (m_origin formal_0_107) 25) (select (m_origin formal_0_107) 37)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:10:7]
(define-fun formal_0_109 () FormalMachine (FormalWriteFromOrigin formal_0_108 6 25))
; source callback case=hoare-partition phase=insert-tail[0:10:8]:initial-compare
(assert (not (m_panicked formal_0_109)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_109) (select (m_origin formal_0_109) 8) (select (m_origin formal_0_109) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_109) (select (m_origin formal_0_109) 8) (select (m_origin formal_0_109) 42)) false))
; source callback transition phase=insert-tail[0:10:8]:initial-compare
(define-fun formal_0_110 () FormalMachine (FormalCallback formal_0_109 boundary_0 (select (m_origin formal_0_109) 8) (select (m_origin formal_0_109) 42)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:8]
(define-fun formal_0_111 () FormalMachine (FormalWriteFromOrigin formal_0_110 8 42))
; source callback case=hoare-partition phase=insert-tail[0:10:8]:sift-compare
(assert (not (m_panicked formal_0_111)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_111) (select (m_origin formal_0_111) 8) (select (m_origin formal_0_111) 25)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_111) (select (m_origin formal_0_111) 8) (select (m_origin formal_0_111) 25)) false))
; source callback transition phase=insert-tail[0:10:8]:sift-compare
(define-fun formal_0_112 () FormalMachine (FormalCallback formal_0_111 boundary_0 (select (m_origin formal_0_111) 8) (select (m_origin formal_0_111) 25)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:8]
(define-fun formal_0_113 () FormalMachine (FormalWriteFromOrigin formal_0_112 7 25))
; source callback case=hoare-partition phase=insert-tail[0:10:8]:sift-compare
(assert (not (m_panicked formal_0_113)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_113) (select (m_origin formal_0_113) 8) (select (m_origin formal_0_113) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_113) (select (m_origin formal_0_113) 8) (select (m_origin formal_0_113) 37)) false))
; source callback transition phase=insert-tail[0:10:8]:sift-compare
(define-fun formal_0_114 () FormalMachine (FormalCallback formal_0_113 boundary_0 (select (m_origin formal_0_113) 8) (select (m_origin formal_0_113) 37)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:8]
(define-fun formal_0_115 () FormalMachine (FormalWriteFromOrigin formal_0_114 6 37))
; source callback case=hoare-partition phase=insert-tail[0:10:8]:sift-compare
(assert (not (m_panicked formal_0_115)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_115) (select (m_origin formal_0_115) 8) (select (m_origin formal_0_115) 43)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_115) (select (m_origin formal_0_115) 8) (select (m_origin formal_0_115) 43)) false))
; source callback transition phase=insert-tail[0:10:8]:sift-compare
(define-fun formal_0_116 () FormalMachine (FormalCallback formal_0_115 boundary_0 (select (m_origin formal_0_115) 8) (select (m_origin formal_0_115) 43)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:8]
(define-fun formal_0_117 () FormalMachine (FormalWriteFromOrigin formal_0_116 5 43))
; source callback case=hoare-partition phase=insert-tail[0:10:8]:sift-compare
(assert (not (m_panicked formal_0_117)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_117) (select (m_origin formal_0_117) 8) (select (m_origin formal_0_117) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_117) (select (m_origin formal_0_117) 8) (select (m_origin formal_0_117) 35)) false))
; source callback transition phase=insert-tail[0:10:8]:sift-compare
(define-fun formal_0_118 () FormalMachine (FormalCallback formal_0_117 boundary_0 (select (m_origin formal_0_117) 8) (select (m_origin formal_0_117) 35)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:10:8]
(define-fun formal_0_119 () FormalMachine (FormalWriteFromOrigin formal_0_118 4 8))
; source callback case=hoare-partition phase=insert-tail[0:10:9]:initial-compare
(assert (not (m_panicked formal_0_119)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_119) (select (m_origin formal_0_119) 12) (select (m_origin formal_0_119) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_119) (select (m_origin formal_0_119) 12) (select (m_origin formal_0_119) 42)) false))
; source callback transition phase=insert-tail[0:10:9]:initial-compare
(define-fun formal_0_120 () FormalMachine (FormalCallback formal_0_119 boundary_0 (select (m_origin formal_0_119) 12) (select (m_origin formal_0_119) 42)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:9]
(define-fun formal_0_121 () FormalMachine (FormalWriteFromOrigin formal_0_120 9 42))
; source callback case=hoare-partition phase=insert-tail[0:10:9]:sift-compare
(assert (not (m_panicked formal_0_121)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_121) (select (m_origin formal_0_121) 12) (select (m_origin formal_0_121) 25)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_121) (select (m_origin formal_0_121) 12) (select (m_origin formal_0_121) 25)) false))
; source callback transition phase=insert-tail[0:10:9]:sift-compare
(define-fun formal_0_122 () FormalMachine (FormalCallback formal_0_121 boundary_0 (select (m_origin formal_0_121) 12) (select (m_origin formal_0_121) 25)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:9]
(define-fun formal_0_123 () FormalMachine (FormalWriteFromOrigin formal_0_122 8 25))
; source callback case=hoare-partition phase=insert-tail[0:10:9]:sift-compare
(assert (not (m_panicked formal_0_123)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_123) (select (m_origin formal_0_123) 12) (select (m_origin formal_0_123) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_123) (select (m_origin formal_0_123) 12) (select (m_origin formal_0_123) 37)) false))
; source callback transition phase=insert-tail[0:10:9]:sift-compare
(define-fun formal_0_124 () FormalMachine (FormalCallback formal_0_123 boundary_0 (select (m_origin formal_0_123) 12) (select (m_origin formal_0_123) 37)))
; source write kind=insert-tail-shift phase=insert-tail[0:10:9]
(define-fun formal_0_125 () FormalMachine (FormalWriteFromOrigin formal_0_124 7 37))
; source callback case=hoare-partition phase=insert-tail[0:10:9]:sift-compare
(assert (not (m_panicked formal_0_125)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_125) (select (m_origin formal_0_125) 12) (select (m_origin formal_0_125) 43)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_125) (select (m_origin formal_0_125) 12) (select (m_origin formal_0_125) 43)) false))
; source callback transition phase=insert-tail[0:10:9]:sift-compare
(define-fun formal_0_126 () FormalMachine (FormalCallback formal_0_125 boundary_0 (select (m_origin formal_0_125) 12) (select (m_origin formal_0_125) 43)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:10:9]
(define-fun formal_0_127 () FormalMachine (FormalWriteFromOrigin formal_0_126 6 12))
; source callback case=hoare-partition phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_127)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_127) (select (m_origin formal_0_127) 11) (select (m_origin formal_0_127) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_127) (select (m_origin formal_0_127) 11) (select (m_origin formal_0_127) 27)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_128 () FormalMachine (FormalCallback formal_0_127 boundary_0 (select (m_origin formal_0_127) 11) (select (m_origin formal_0_127) 27)))
; source callback case=hoare-partition phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_128)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 11) (select (m_origin formal_0_128) 39)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 11) (select (m_origin formal_0_128) 39)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_129 () FormalMachine (FormalCallback formal_0_128 boundary_0 (select (m_origin formal_0_128) 11) (select (m_origin formal_0_128) 39)))
; source callback case=hoare-partition phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_129)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_129) (select (m_origin formal_0_129) 27) (select (m_origin formal_0_129) 39)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_129) (select (m_origin formal_0_129) 27) (select (m_origin formal_0_129) 39)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_130 () FormalMachine (FormalCallback formal_0_129 boundary_0 (select (m_origin formal_0_129) 27) (select (m_origin formal_0_129) 39)))
; source callback case=hoare-partition phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_130)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_130) (select (m_origin formal_0_130) 20) (select (m_origin formal_0_130) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_130) (select (m_origin formal_0_130) 20) (select (m_origin formal_0_130) 27)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_131 () FormalMachine (FormalCallback formal_0_130 boundary_0 (select (m_origin formal_0_130) 20) (select (m_origin formal_0_130) 27)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_132 () FormalMachine (FormalSwap formal_0_131 11 27))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_132)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_132) (select (m_origin formal_0_132) 1) (select (m_origin formal_0_132) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_132) (select (m_origin formal_0_132) 1) (select (m_origin formal_0_132) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_133 () FormalMachine (FormalCallback formal_0_132 boundary_0 (select (m_origin formal_0_132) 1) (select (m_origin formal_0_132) 27)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_133)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_133) (select (m_origin formal_0_133) 13) (select (m_origin formal_0_133) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_133) (select (m_origin formal_0_133) 13) (select (m_origin formal_0_133) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_134 () FormalMachine (FormalCallback formal_0_133 boundary_0 (select (m_origin formal_0_133) 13) (select (m_origin formal_0_133) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_134)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_134) (select (m_origin formal_0_134) 44) (select (m_origin formal_0_134) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_134) (select (m_origin formal_0_134) 44) (select (m_origin formal_0_134) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_135 () FormalMachine (FormalCallback formal_0_134 boundary_0 (select (m_origin formal_0_134) 44) (select (m_origin formal_0_134) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_135)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_135) (select (m_origin formal_0_135) 2) (select (m_origin formal_0_135) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_135) (select (m_origin formal_0_135) 2) (select (m_origin formal_0_135) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_136 () FormalMachine (FormalCallback formal_0_135 boundary_0 (select (m_origin formal_0_135) 2) (select (m_origin formal_0_135) 27)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_137 () FormalMachine (FormalWriteFromOrigin formal_0_136 13 2))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_137)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_137) (select (m_origin formal_0_137) 14) (select (m_origin formal_0_137) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_137) (select (m_origin formal_0_137) 14) (select (m_origin formal_0_137) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_138 () FormalMachine (FormalCallback formal_0_137 boundary_0 (select (m_origin formal_0_137) 14) (select (m_origin formal_0_137) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_138)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_138) (select (m_origin formal_0_138) 3) (select (m_origin formal_0_138) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_138) (select (m_origin formal_0_138) 3) (select (m_origin formal_0_138) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_139 () FormalMachine (FormalCallback formal_0_138 boundary_0 (select (m_origin formal_0_138) 3) (select (m_origin formal_0_138) 27)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_140 () FormalMachine (FormalWriteFromOrigin formal_0_139 14 3))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_141 () FormalMachine (FormalWriteFromOrigin formal_0_140 43 14))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_141)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_141) (select (m_origin formal_0_141) 15) (select (m_origin formal_0_141) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_141) (select (m_origin formal_0_141) 15) (select (m_origin formal_0_141) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_142 () FormalMachine (FormalCallback formal_0_141 boundary_0 (select (m_origin formal_0_141) 15) (select (m_origin formal_0_141) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_142)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_142) (select (m_origin formal_0_142) 41) (select (m_origin formal_0_142) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_142) (select (m_origin formal_0_142) 41) (select (m_origin formal_0_142) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_143 () FormalMachine (FormalCallback formal_0_142 boundary_0 (select (m_origin formal_0_142) 41) (select (m_origin formal_0_142) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_143)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_143) (select (m_origin formal_0_143) 40) (select (m_origin formal_0_143) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_143) (select (m_origin formal_0_143) 40) (select (m_origin formal_0_143) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_144 () FormalMachine (FormalCallback formal_0_143 boundary_0 (select (m_origin formal_0_143) 40) (select (m_origin formal_0_143) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_144)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_144) (select (m_origin formal_0_144) 39) (select (m_origin formal_0_144) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_144) (select (m_origin formal_0_144) 39) (select (m_origin formal_0_144) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_145 () FormalMachine (FormalCallback formal_0_144 boundary_0 (select (m_origin formal_0_144) 39) (select (m_origin formal_0_144) 27)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_146 () FormalMachine (FormalWriteFromOrigin formal_0_145 15 39))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_147 () FormalMachine (FormalWriteFromOrigin formal_0_146 42 15))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_147)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_147) (select (m_origin formal_0_147) 16) (select (m_origin formal_0_147) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_147) (select (m_origin formal_0_147) 16) (select (m_origin formal_0_147) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_148 () FormalMachine (FormalCallback formal_0_147 boundary_0 (select (m_origin formal_0_147) 16) (select (m_origin formal_0_147) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_148)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_148) (select (m_origin formal_0_148) 38) (select (m_origin formal_0_148) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_148) (select (m_origin formal_0_148) 38) (select (m_origin formal_0_148) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_149 () FormalMachine (FormalCallback formal_0_148 boundary_0 (select (m_origin formal_0_148) 38) (select (m_origin formal_0_148) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_149)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_149) (select (m_origin formal_0_149) 4) (select (m_origin formal_0_149) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_149) (select (m_origin formal_0_149) 4) (select (m_origin formal_0_149) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_150 () FormalMachine (FormalCallback formal_0_149 boundary_0 (select (m_origin formal_0_149) 4) (select (m_origin formal_0_149) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_150)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_150) (select (m_origin formal_0_150) 5) (select (m_origin formal_0_150) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_150) (select (m_origin formal_0_150) 5) (select (m_origin formal_0_150) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_151 () FormalMachine (FormalCallback formal_0_150 boundary_0 (select (m_origin formal_0_150) 5) (select (m_origin formal_0_150) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_151)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_151) (select (m_origin formal_0_151) 6) (select (m_origin formal_0_151) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_151) (select (m_origin formal_0_151) 6) (select (m_origin formal_0_151) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_152 () FormalMachine (FormalCallback formal_0_151 boundary_0 (select (m_origin formal_0_151) 6) (select (m_origin formal_0_151) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_152)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_152) (select (m_origin formal_0_152) 7) (select (m_origin formal_0_152) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_152) (select (m_origin formal_0_152) 7) (select (m_origin formal_0_152) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_153 () FormalMachine (FormalCallback formal_0_152 boundary_0 (select (m_origin formal_0_152) 7) (select (m_origin formal_0_152) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_153)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_153) (select (m_origin formal_0_153) 33) (select (m_origin formal_0_153) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_153) (select (m_origin formal_0_153) 33) (select (m_origin formal_0_153) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_154 () FormalMachine (FormalCallback formal_0_153 boundary_0 (select (m_origin formal_0_153) 33) (select (m_origin formal_0_153) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_154)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_154) (select (m_origin formal_0_154) 32) (select (m_origin formal_0_154) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_154) (select (m_origin formal_0_154) 32) (select (m_origin formal_0_154) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_155 () FormalMachine (FormalCallback formal_0_154 boundary_0 (select (m_origin formal_0_154) 32) (select (m_origin formal_0_154) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_155)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 31) (select (m_origin formal_0_155) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 31) (select (m_origin formal_0_155) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_156 () FormalMachine (FormalCallback formal_0_155 boundary_0 (select (m_origin formal_0_155) 31) (select (m_origin formal_0_155) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_156)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_156) (select (m_origin formal_0_156) 30) (select (m_origin formal_0_156) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_156) (select (m_origin formal_0_156) 30) (select (m_origin formal_0_156) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_157 () FormalMachine (FormalCallback formal_0_156 boundary_0 (select (m_origin formal_0_156) 30) (select (m_origin formal_0_156) 27)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_158 () FormalMachine (FormalWriteFromOrigin formal_0_157 16 30))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_159 () FormalMachine (FormalWriteFromOrigin formal_0_158 39 16))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_159)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_159) (select (m_origin formal_0_159) 17) (select (m_origin formal_0_159) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_159) (select (m_origin formal_0_159) 17) (select (m_origin formal_0_159) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_160 () FormalMachine (FormalCallback formal_0_159 boundary_0 (select (m_origin formal_0_159) 17) (select (m_origin formal_0_159) 27)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_160)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_160) (select (m_origin formal_0_160) 18) (select (m_origin formal_0_160) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_160) (select (m_origin formal_0_160) 18) (select (m_origin formal_0_160) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_161 () FormalMachine (FormalCallback formal_0_160 boundary_0 (select (m_origin formal_0_160) 18) (select (m_origin formal_0_160) 27)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_161)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_161) (select (m_origin formal_0_161) 19) (select (m_origin formal_0_161) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_161) (select (m_origin formal_0_161) 19) (select (m_origin formal_0_161) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_162 () FormalMachine (FormalCallback formal_0_161 boundary_0 (select (m_origin formal_0_161) 19) (select (m_origin formal_0_161) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_162)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_162) (select (m_origin formal_0_162) 29) (select (m_origin formal_0_162) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_162) (select (m_origin formal_0_162) 29) (select (m_origin formal_0_162) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_163 () FormalMachine (FormalCallback formal_0_162 boundary_0 (select (m_origin formal_0_162) 29) (select (m_origin formal_0_162) 27)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_164 () FormalMachine (FormalWriteFromOrigin formal_0_163 19 29))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_165 () FormalMachine (FormalWriteFromOrigin formal_0_164 30 19))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_165)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_165) (select (m_origin formal_0_165) 0) (select (m_origin formal_0_165) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_165) (select (m_origin formal_0_165) 0) (select (m_origin formal_0_165) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_166 () FormalMachine (FormalCallback formal_0_165 boundary_0 (select (m_origin formal_0_165) 0) (select (m_origin formal_0_165) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_166)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_166) (select (m_origin formal_0_166) 28) (select (m_origin formal_0_166) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_166) (select (m_origin formal_0_166) 28) (select (m_origin formal_0_166) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_167 () FormalMachine (FormalCallback formal_0_166 boundary_0 (select (m_origin formal_0_166) 28) (select (m_origin formal_0_166) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_167)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_167) (select (m_origin formal_0_167) 11) (select (m_origin formal_0_167) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_167) (select (m_origin formal_0_167) 11) (select (m_origin formal_0_167) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_168 () FormalMachine (FormalCallback formal_0_167 boundary_0 (select (m_origin formal_0_167) 11) (select (m_origin formal_0_167) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_168)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_168) (select (m_origin formal_0_168) 26) (select (m_origin formal_0_168) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_168) (select (m_origin formal_0_168) 26) (select (m_origin formal_0_168) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_169 () FormalMachine (FormalCallback formal_0_168 boundary_0 (select (m_origin formal_0_168) 26) (select (m_origin formal_0_168) 27)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_170 () FormalMachine (FormalWriteFromOrigin formal_0_169 20 26))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_171 () FormalMachine (FormalWriteFromOrigin formal_0_170 29 0))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_171)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_171) (select (m_origin formal_0_171) 21) (select (m_origin formal_0_171) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_171) (select (m_origin formal_0_171) 21) (select (m_origin formal_0_171) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_172 () FormalMachine (FormalCallback formal_0_171 boundary_0 (select (m_origin formal_0_171) 21) (select (m_origin formal_0_171) 27)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_172)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_172) (select (m_origin formal_0_172) 9) (select (m_origin formal_0_172) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_172) (select (m_origin formal_0_172) 9) (select (m_origin formal_0_172) 27)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_173 () FormalMachine (FormalCallback formal_0_172 boundary_0 (select (m_origin formal_0_172) 9) (select (m_origin formal_0_172) 27)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_174 () FormalMachine (FormalWriteFromOrigin formal_0_173 21 9))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_175 () FormalMachine (FormalWriteFromOrigin formal_0_174 26 21))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_175)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_175) (select (m_origin formal_0_175) 22) (select (m_origin formal_0_175) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_175) (select (m_origin formal_0_175) 22) (select (m_origin formal_0_175) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_176 () FormalMachine (FormalCallback formal_0_175 boundary_0 (select (m_origin formal_0_175) 22) (select (m_origin formal_0_175) 27)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_176)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 23) (select (m_origin formal_0_176) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 23) (select (m_origin formal_0_176) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_177 () FormalMachine (FormalCallback formal_0_176 boundary_0 (select (m_origin formal_0_176) 23) (select (m_origin formal_0_176) 27)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_177)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_177) (select (m_origin formal_0_177) 24) (select (m_origin formal_0_177) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_177) (select (m_origin formal_0_177) 24) (select (m_origin formal_0_177) 27)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_178 () FormalMachine (FormalCallback formal_0_177 boundary_0 (select (m_origin formal_0_177) 24) (select (m_origin formal_0_177) 27)))
; source write kind=gap-guard-restore phase=partition-hoare-branchy-cyclic
(define-fun formal_0_179 () FormalMachine (FormalWriteFromOrigin formal_0_178 25 13))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_180 () FormalMachine (FormalSwap formal_0_179 11 24))
; source callback case=hoare-partition phase=insert-tail[11:24:1]:initial-compare
(assert (not (m_panicked formal_0_180)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_180) (select (m_origin formal_0_180) 1) (select (m_origin formal_0_180) 24)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_180) (select (m_origin formal_0_180) 1) (select (m_origin formal_0_180) 24)) false))
; source callback transition phase=insert-tail[11:24:1]:initial-compare
(define-fun formal_0_181 () FormalMachine (FormalCallback formal_0_180 boundary_0 (select (m_origin formal_0_180) 1) (select (m_origin formal_0_180) 24)))
; source callback case=hoare-partition phase=insert-tail[11:24:2]:initial-compare
(assert (not (m_panicked formal_0_181)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_181) (select (m_origin formal_0_181) 2) (select (m_origin formal_0_181) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_181) (select (m_origin formal_0_181) 2) (select (m_origin formal_0_181) 1)) false))
; source callback transition phase=insert-tail[11:24:2]:initial-compare
(define-fun formal_0_182 () FormalMachine (FormalCallback formal_0_181 boundary_0 (select (m_origin formal_0_181) 2) (select (m_origin formal_0_181) 1)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:2]
(define-fun formal_0_183 () FormalMachine (FormalWriteFromOrigin formal_0_182 13 1))
; source callback case=hoare-partition phase=insert-tail[11:24:2]:sift-compare
(assert (not (m_panicked formal_0_183)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_183) (select (m_origin formal_0_183) 2) (select (m_origin formal_0_183) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_183) (select (m_origin formal_0_183) 2) (select (m_origin formal_0_183) 24)) false))
; source callback transition phase=insert-tail[11:24:2]:sift-compare
(define-fun formal_0_184 () FormalMachine (FormalCallback formal_0_183 boundary_0 (select (m_origin formal_0_183) 2) (select (m_origin formal_0_183) 24)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:2]
(define-fun formal_0_185 () FormalMachine (FormalWriteFromOrigin formal_0_184 12 24))
; source write kind=copy-on-drop-restore phase=insert-tail[11:24:2]
(define-fun formal_0_186 () FormalMachine (FormalWriteFromOrigin formal_0_185 11 2))
; source callback case=hoare-partition phase=insert-tail[11:24:3]:initial-compare
(assert (not (m_panicked formal_0_186)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_186) (select (m_origin formal_0_186) 3) (select (m_origin formal_0_186) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_186) (select (m_origin formal_0_186) 3) (select (m_origin formal_0_186) 1)) false))
; source callback transition phase=insert-tail[11:24:3]:initial-compare
(define-fun formal_0_187 () FormalMachine (FormalCallback formal_0_186 boundary_0 (select (m_origin formal_0_186) 3) (select (m_origin formal_0_186) 1)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:3]
(define-fun formal_0_188 () FormalMachine (FormalWriteFromOrigin formal_0_187 14 1))
; source callback case=hoare-partition phase=insert-tail[11:24:3]:sift-compare
(assert (not (m_panicked formal_0_188)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_188) (select (m_origin formal_0_188) 3) (select (m_origin formal_0_188) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_188) (select (m_origin formal_0_188) 3) (select (m_origin formal_0_188) 24)) false))
; source callback transition phase=insert-tail[11:24:3]:sift-compare
(define-fun formal_0_189 () FormalMachine (FormalCallback formal_0_188 boundary_0 (select (m_origin formal_0_188) 3) (select (m_origin formal_0_188) 24)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:3]
(define-fun formal_0_190 () FormalMachine (FormalWriteFromOrigin formal_0_189 13 24))
; source callback case=hoare-partition phase=insert-tail[11:24:3]:sift-compare
(assert (not (m_panicked formal_0_190)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_190) (select (m_origin formal_0_190) 3) (select (m_origin formal_0_190) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_190) (select (m_origin formal_0_190) 3) (select (m_origin formal_0_190) 2)) false))
; source callback transition phase=insert-tail[11:24:3]:sift-compare
(define-fun formal_0_191 () FormalMachine (FormalCallback formal_0_190 boundary_0 (select (m_origin formal_0_190) 3) (select (m_origin formal_0_190) 2)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:3]
(define-fun formal_0_192 () FormalMachine (FormalWriteFromOrigin formal_0_191 12 2))
; source write kind=copy-on-drop-restore phase=insert-tail[11:24:3]
(define-fun formal_0_193 () FormalMachine (FormalWriteFromOrigin formal_0_192 11 3))
; source callback case=hoare-partition phase=insert-tail[11:24:4]:initial-compare
(assert (not (m_panicked formal_0_193)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_193) (select (m_origin formal_0_193) 39) (select (m_origin formal_0_193) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_193) (select (m_origin formal_0_193) 39) (select (m_origin formal_0_193) 1)) false))
; source callback transition phase=insert-tail[11:24:4]:initial-compare
(define-fun formal_0_194 () FormalMachine (FormalCallback formal_0_193 boundary_0 (select (m_origin formal_0_193) 39) (select (m_origin formal_0_193) 1)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:4]
(define-fun formal_0_195 () FormalMachine (FormalWriteFromOrigin formal_0_194 15 1))
; source callback case=hoare-partition phase=insert-tail[11:24:4]:sift-compare
(assert (not (m_panicked formal_0_195)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_195) (select (m_origin formal_0_195) 39) (select (m_origin formal_0_195) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_195) (select (m_origin formal_0_195) 39) (select (m_origin formal_0_195) 24)) false))
; source callback transition phase=insert-tail[11:24:4]:sift-compare
(define-fun formal_0_196 () FormalMachine (FormalCallback formal_0_195 boundary_0 (select (m_origin formal_0_195) 39) (select (m_origin formal_0_195) 24)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:4]
(define-fun formal_0_197 () FormalMachine (FormalWriteFromOrigin formal_0_196 14 24))
; source callback case=hoare-partition phase=insert-tail[11:24:4]:sift-compare
(assert (not (m_panicked formal_0_197)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_197) (select (m_origin formal_0_197) 39) (select (m_origin formal_0_197) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_197) (select (m_origin formal_0_197) 39) (select (m_origin formal_0_197) 2)) false))
; source callback transition phase=insert-tail[11:24:4]:sift-compare
(define-fun formal_0_198 () FormalMachine (FormalCallback formal_0_197 boundary_0 (select (m_origin formal_0_197) 39) (select (m_origin formal_0_197) 2)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:4]
(define-fun formal_0_199 () FormalMachine (FormalWriteFromOrigin formal_0_198 13 2))
; source callback case=hoare-partition phase=insert-tail[11:24:4]:sift-compare
(assert (not (m_panicked formal_0_199)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_199) (select (m_origin formal_0_199) 39) (select (m_origin formal_0_199) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_199) (select (m_origin formal_0_199) 39) (select (m_origin formal_0_199) 3)) false))
; source callback transition phase=insert-tail[11:24:4]:sift-compare
(define-fun formal_0_200 () FormalMachine (FormalCallback formal_0_199 boundary_0 (select (m_origin formal_0_199) 39) (select (m_origin formal_0_199) 3)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:4]
(define-fun formal_0_201 () FormalMachine (FormalWriteFromOrigin formal_0_200 12 3))
; source write kind=copy-on-drop-restore phase=insert-tail[11:24:4]
(define-fun formal_0_202 () FormalMachine (FormalWriteFromOrigin formal_0_201 11 39))
; source callback case=hoare-partition phase=insert-tail[11:24:5]:initial-compare
(assert (not (m_panicked formal_0_202)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_202) (select (m_origin formal_0_202) 30) (select (m_origin formal_0_202) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_202) (select (m_origin formal_0_202) 30) (select (m_origin formal_0_202) 1)) false))
; source callback transition phase=insert-tail[11:24:5]:initial-compare
(define-fun formal_0_203 () FormalMachine (FormalCallback formal_0_202 boundary_0 (select (m_origin formal_0_202) 30) (select (m_origin formal_0_202) 1)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:5]
(define-fun formal_0_204 () FormalMachine (FormalWriteFromOrigin formal_0_203 16 1))
; source callback case=hoare-partition phase=insert-tail[11:24:5]:sift-compare
(assert (not (m_panicked formal_0_204)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_204) (select (m_origin formal_0_204) 30) (select (m_origin formal_0_204) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_204) (select (m_origin formal_0_204) 30) (select (m_origin formal_0_204) 24)) false))
; source callback transition phase=insert-tail[11:24:5]:sift-compare
(define-fun formal_0_205 () FormalMachine (FormalCallback formal_0_204 boundary_0 (select (m_origin formal_0_204) 30) (select (m_origin formal_0_204) 24)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:5]
(define-fun formal_0_206 () FormalMachine (FormalWriteFromOrigin formal_0_205 15 24))
; source callback case=hoare-partition phase=insert-tail[11:24:5]:sift-compare
(assert (not (m_panicked formal_0_206)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_206) (select (m_origin formal_0_206) 30) (select (m_origin formal_0_206) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_206) (select (m_origin formal_0_206) 30) (select (m_origin formal_0_206) 2)) false))
; source callback transition phase=insert-tail[11:24:5]:sift-compare
(define-fun formal_0_207 () FormalMachine (FormalCallback formal_0_206 boundary_0 (select (m_origin formal_0_206) 30) (select (m_origin formal_0_206) 2)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:5]
(define-fun formal_0_208 () FormalMachine (FormalWriteFromOrigin formal_0_207 14 2))
; source callback case=hoare-partition phase=insert-tail[11:24:5]:sift-compare
(assert (not (m_panicked formal_0_208)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_208) (select (m_origin formal_0_208) 30) (select (m_origin formal_0_208) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_208) (select (m_origin formal_0_208) 30) (select (m_origin formal_0_208) 3)) false))
; source callback transition phase=insert-tail[11:24:5]:sift-compare
(define-fun formal_0_209 () FormalMachine (FormalCallback formal_0_208 boundary_0 (select (m_origin formal_0_208) 30) (select (m_origin formal_0_208) 3)))
; source write kind=copy-on-drop-restore phase=insert-tail[11:24:5]
(define-fun formal_0_210 () FormalMachine (FormalWriteFromOrigin formal_0_209 13 30))
; source callback case=hoare-partition phase=insert-tail[11:24:6]:initial-compare
(assert (not (m_panicked formal_0_210)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_210) (select (m_origin formal_0_210) 17) (select (m_origin formal_0_210) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_210) (select (m_origin formal_0_210) 17) (select (m_origin formal_0_210) 1)) false))
; source callback transition phase=insert-tail[11:24:6]:initial-compare
(define-fun formal_0_211 () FormalMachine (FormalCallback formal_0_210 boundary_0 (select (m_origin formal_0_210) 17) (select (m_origin formal_0_210) 1)))
; source callback case=hoare-partition phase=insert-tail[11:24:7]:initial-compare
(assert (not (m_panicked formal_0_211)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_211) (select (m_origin formal_0_211) 18) (select (m_origin formal_0_211) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_211) (select (m_origin formal_0_211) 18) (select (m_origin formal_0_211) 17)) false))
; source callback transition phase=insert-tail[11:24:7]:initial-compare
(define-fun formal_0_212 () FormalMachine (FormalCallback formal_0_211 boundary_0 (select (m_origin formal_0_211) 18) (select (m_origin formal_0_211) 17)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:7]
(define-fun formal_0_213 () FormalMachine (FormalWriteFromOrigin formal_0_212 18 17))
; source callback case=hoare-partition phase=insert-tail[11:24:7]:sift-compare
(assert (not (m_panicked formal_0_213)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_213) (select (m_origin formal_0_213) 18) (select (m_origin formal_0_213) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_213) (select (m_origin formal_0_213) 18) (select (m_origin formal_0_213) 1)) false))
; source callback transition phase=insert-tail[11:24:7]:sift-compare
(define-fun formal_0_214 () FormalMachine (FormalCallback formal_0_213 boundary_0 (select (m_origin formal_0_213) 18) (select (m_origin formal_0_213) 1)))
; source write kind=copy-on-drop-restore phase=insert-tail[11:24:7]
(define-fun formal_0_215 () FormalMachine (FormalWriteFromOrigin formal_0_214 17 18))
; source callback case=hoare-partition phase=insert-tail[11:24:8]:initial-compare
(assert (not (m_panicked formal_0_215)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_215) (select (m_origin formal_0_215) 29) (select (m_origin formal_0_215) 17)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_215) (select (m_origin formal_0_215) 29) (select (m_origin formal_0_215) 17)) false))
; source callback transition phase=insert-tail[11:24:8]:initial-compare
(define-fun formal_0_216 () FormalMachine (FormalCallback formal_0_215 boundary_0 (select (m_origin formal_0_215) 29) (select (m_origin formal_0_215) 17)))
; source callback case=hoare-partition phase=insert-tail[11:24:9]:initial-compare
(assert (not (m_panicked formal_0_216)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_216) (select (m_origin formal_0_216) 26) (select (m_origin formal_0_216) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_216) (select (m_origin formal_0_216) 26) (select (m_origin formal_0_216) 29)) false))
; source callback transition phase=insert-tail[11:24:9]:initial-compare
(define-fun formal_0_217 () FormalMachine (FormalCallback formal_0_216 boundary_0 (select (m_origin formal_0_216) 26) (select (m_origin formal_0_216) 29)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:9]
(define-fun formal_0_218 () FormalMachine (FormalWriteFromOrigin formal_0_217 20 29))
; source callback case=hoare-partition phase=insert-tail[11:24:9]:sift-compare
(assert (not (m_panicked formal_0_218)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_218) (select (m_origin formal_0_218) 26) (select (m_origin formal_0_218) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_218) (select (m_origin formal_0_218) 26) (select (m_origin formal_0_218) 17)) false))
; source callback transition phase=insert-tail[11:24:9]:sift-compare
(define-fun formal_0_219 () FormalMachine (FormalCallback formal_0_218 boundary_0 (select (m_origin formal_0_218) 26) (select (m_origin formal_0_218) 17)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:9]
(define-fun formal_0_220 () FormalMachine (FormalWriteFromOrigin formal_0_219 19 17))
; source callback case=hoare-partition phase=insert-tail[11:24:9]:sift-compare
(assert (not (m_panicked formal_0_220)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_220) (select (m_origin formal_0_220) 26) (select (m_origin formal_0_220) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_220) (select (m_origin formal_0_220) 26) (select (m_origin formal_0_220) 18)) false))
; source callback transition phase=insert-tail[11:24:9]:sift-compare
(define-fun formal_0_221 () FormalMachine (FormalCallback formal_0_220 boundary_0 (select (m_origin formal_0_220) 26) (select (m_origin formal_0_220) 18)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:9]
(define-fun formal_0_222 () FormalMachine (FormalWriteFromOrigin formal_0_221 18 18))
; source callback case=hoare-partition phase=insert-tail[11:24:9]:sift-compare
(assert (not (m_panicked formal_0_222)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_222) (select (m_origin formal_0_222) 26) (select (m_origin formal_0_222) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_222) (select (m_origin formal_0_222) 26) (select (m_origin formal_0_222) 1)) false))
; source callback transition phase=insert-tail[11:24:9]:sift-compare
(define-fun formal_0_223 () FormalMachine (FormalCallback formal_0_222 boundary_0 (select (m_origin formal_0_222) 26) (select (m_origin formal_0_222) 1)))
; source write kind=copy-on-drop-restore phase=insert-tail[11:24:9]
(define-fun formal_0_224 () FormalMachine (FormalWriteFromOrigin formal_0_223 17 26))
; source callback case=hoare-partition phase=insert-tail[11:24:10]:initial-compare
(assert (not (m_panicked formal_0_224)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_224) (select (m_origin formal_0_224) 9) (select (m_origin formal_0_224) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_224) (select (m_origin formal_0_224) 9) (select (m_origin formal_0_224) 29)) false))
; source callback transition phase=insert-tail[11:24:10]:initial-compare
(define-fun formal_0_225 () FormalMachine (FormalCallback formal_0_224 boundary_0 (select (m_origin formal_0_224) 9) (select (m_origin formal_0_224) 29)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:10]
(define-fun formal_0_226 () FormalMachine (FormalWriteFromOrigin formal_0_225 21 29))
; source callback case=hoare-partition phase=insert-tail[11:24:10]:sift-compare
(assert (not (m_panicked formal_0_226)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_226) (select (m_origin formal_0_226) 9) (select (m_origin formal_0_226) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_226) (select (m_origin formal_0_226) 9) (select (m_origin formal_0_226) 17)) false))
; source callback transition phase=insert-tail[11:24:10]:sift-compare
(define-fun formal_0_227 () FormalMachine (FormalCallback formal_0_226 boundary_0 (select (m_origin formal_0_226) 9) (select (m_origin formal_0_226) 17)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:10]
(define-fun formal_0_228 () FormalMachine (FormalWriteFromOrigin formal_0_227 20 17))
; source callback case=hoare-partition phase=insert-tail[11:24:10]:sift-compare
(assert (not (m_panicked formal_0_228)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_228) (select (m_origin formal_0_228) 9) (select (m_origin formal_0_228) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_228) (select (m_origin formal_0_228) 9) (select (m_origin formal_0_228) 18)) false))
; source callback transition phase=insert-tail[11:24:10]:sift-compare
(define-fun formal_0_229 () FormalMachine (FormalCallback formal_0_228 boundary_0 (select (m_origin formal_0_228) 9) (select (m_origin formal_0_228) 18)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:10]
(define-fun formal_0_230 () FormalMachine (FormalWriteFromOrigin formal_0_229 19 18))
; source callback case=hoare-partition phase=insert-tail[11:24:10]:sift-compare
(assert (not (m_panicked formal_0_230)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_230) (select (m_origin formal_0_230) 9) (select (m_origin formal_0_230) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_230) (select (m_origin formal_0_230) 9) (select (m_origin formal_0_230) 26)) false))
; source callback transition phase=insert-tail[11:24:10]:sift-compare
(define-fun formal_0_231 () FormalMachine (FormalCallback formal_0_230 boundary_0 (select (m_origin formal_0_230) 9) (select (m_origin formal_0_230) 26)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:10]
(define-fun formal_0_232 () FormalMachine (FormalWriteFromOrigin formal_0_231 18 26))
; source callback case=hoare-partition phase=insert-tail[11:24:10]:sift-compare
(assert (not (m_panicked formal_0_232)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_232) (select (m_origin formal_0_232) 9) (select (m_origin formal_0_232) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_232) (select (m_origin formal_0_232) 9) (select (m_origin formal_0_232) 1)) false))
; source callback transition phase=insert-tail[11:24:10]:sift-compare
(define-fun formal_0_233 () FormalMachine (FormalCallback formal_0_232 boundary_0 (select (m_origin formal_0_232) 9) (select (m_origin formal_0_232) 1)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:10]
(define-fun formal_0_234 () FormalMachine (FormalWriteFromOrigin formal_0_233 17 1))
; source callback case=hoare-partition phase=insert-tail[11:24:10]:sift-compare
(assert (not (m_panicked formal_0_234)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_234) (select (m_origin formal_0_234) 9) (select (m_origin formal_0_234) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_234) (select (m_origin formal_0_234) 9) (select (m_origin formal_0_234) 24)) false))
; source callback transition phase=insert-tail[11:24:10]:sift-compare
(define-fun formal_0_235 () FormalMachine (FormalCallback formal_0_234 boundary_0 (select (m_origin formal_0_234) 9) (select (m_origin formal_0_234) 24)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:10]
(define-fun formal_0_236 () FormalMachine (FormalWriteFromOrigin formal_0_235 16 24))
; source callback case=hoare-partition phase=insert-tail[11:24:10]:sift-compare
(assert (not (m_panicked formal_0_236)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_236) (select (m_origin formal_0_236) 9) (select (m_origin formal_0_236) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_236) (select (m_origin formal_0_236) 9) (select (m_origin formal_0_236) 2)) false))
; source callback transition phase=insert-tail[11:24:10]:sift-compare
(define-fun formal_0_237 () FormalMachine (FormalCallback formal_0_236 boundary_0 (select (m_origin formal_0_236) 9) (select (m_origin formal_0_236) 2)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:10]
(define-fun formal_0_238 () FormalMachine (FormalWriteFromOrigin formal_0_237 15 2))
; source callback case=hoare-partition phase=insert-tail[11:24:10]:sift-compare
(assert (not (m_panicked formal_0_238)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_238) (select (m_origin formal_0_238) 9) (select (m_origin formal_0_238) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_238) (select (m_origin formal_0_238) 9) (select (m_origin formal_0_238) 30)) false))
; source callback transition phase=insert-tail[11:24:10]:sift-compare
(define-fun formal_0_239 () FormalMachine (FormalCallback formal_0_238 boundary_0 (select (m_origin formal_0_238) 9) (select (m_origin formal_0_238) 30)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:10]
(define-fun formal_0_240 () FormalMachine (FormalWriteFromOrigin formal_0_239 14 30))
; source callback case=hoare-partition phase=insert-tail[11:24:10]:sift-compare
(assert (not (m_panicked formal_0_240)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_240) (select (m_origin formal_0_240) 9) (select (m_origin formal_0_240) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_240) (select (m_origin formal_0_240) 9) (select (m_origin formal_0_240) 3)) false))
; source callback transition phase=insert-tail[11:24:10]:sift-compare
(define-fun formal_0_241 () FormalMachine (FormalCallback formal_0_240 boundary_0 (select (m_origin formal_0_240) 9) (select (m_origin formal_0_240) 3)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:10]
(define-fun formal_0_242 () FormalMachine (FormalWriteFromOrigin formal_0_241 13 3))
; source callback case=hoare-partition phase=insert-tail[11:24:10]:sift-compare
(assert (not (m_panicked formal_0_242)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_242) (select (m_origin formal_0_242) 9) (select (m_origin formal_0_242) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_242) (select (m_origin formal_0_242) 9) (select (m_origin formal_0_242) 39)) false))
; source callback transition phase=insert-tail[11:24:10]:sift-compare
(define-fun formal_0_243 () FormalMachine (FormalCallback formal_0_242 boundary_0 (select (m_origin formal_0_242) 9) (select (m_origin formal_0_242) 39)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:10]
(define-fun formal_0_244 () FormalMachine (FormalWriteFromOrigin formal_0_243 12 39))
; source write kind=copy-on-drop-restore phase=insert-tail[11:24:10]
(define-fun formal_0_245 () FormalMachine (FormalWriteFromOrigin formal_0_244 11 9))
; source callback case=hoare-partition phase=insert-tail[11:24:11]:initial-compare
(assert (not (m_panicked formal_0_245)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_245) (select (m_origin formal_0_245) 22) (select (m_origin formal_0_245) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_245) (select (m_origin formal_0_245) 22) (select (m_origin formal_0_245) 29)) false))
; source callback transition phase=insert-tail[11:24:11]:initial-compare
(define-fun formal_0_246 () FormalMachine (FormalCallback formal_0_245 boundary_0 (select (m_origin formal_0_245) 22) (select (m_origin formal_0_245) 29)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:11]
(define-fun formal_0_247 () FormalMachine (FormalWriteFromOrigin formal_0_246 22 29))
; source callback case=hoare-partition phase=insert-tail[11:24:11]:sift-compare
(assert (not (m_panicked formal_0_247)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_247) (select (m_origin formal_0_247) 22) (select (m_origin formal_0_247) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_247) (select (m_origin formal_0_247) 22) (select (m_origin formal_0_247) 17)) false))
; source callback transition phase=insert-tail[11:24:11]:sift-compare
(define-fun formal_0_248 () FormalMachine (FormalCallback formal_0_247 boundary_0 (select (m_origin formal_0_247) 22) (select (m_origin formal_0_247) 17)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:11]
(define-fun formal_0_249 () FormalMachine (FormalWriteFromOrigin formal_0_248 21 17))
; source callback case=hoare-partition phase=insert-tail[11:24:11]:sift-compare
(assert (not (m_panicked formal_0_249)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_249) (select (m_origin formal_0_249) 22) (select (m_origin formal_0_249) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_249) (select (m_origin formal_0_249) 22) (select (m_origin formal_0_249) 18)) false))
; source callback transition phase=insert-tail[11:24:11]:sift-compare
(define-fun formal_0_250 () FormalMachine (FormalCallback formal_0_249 boundary_0 (select (m_origin formal_0_249) 22) (select (m_origin formal_0_249) 18)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:11]
(define-fun formal_0_251 () FormalMachine (FormalWriteFromOrigin formal_0_250 20 18))
; source callback case=hoare-partition phase=insert-tail[11:24:11]:sift-compare
(assert (not (m_panicked formal_0_251)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_251) (select (m_origin formal_0_251) 22) (select (m_origin formal_0_251) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_251) (select (m_origin formal_0_251) 22) (select (m_origin formal_0_251) 26)) false))
; source callback transition phase=insert-tail[11:24:11]:sift-compare
(define-fun formal_0_252 () FormalMachine (FormalCallback formal_0_251 boundary_0 (select (m_origin formal_0_251) 22) (select (m_origin formal_0_251) 26)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:11]
(define-fun formal_0_253 () FormalMachine (FormalWriteFromOrigin formal_0_252 19 26))
; source callback case=hoare-partition phase=insert-tail[11:24:11]:sift-compare
(assert (not (m_panicked formal_0_253)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_253) (select (m_origin formal_0_253) 22) (select (m_origin formal_0_253) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_253) (select (m_origin formal_0_253) 22) (select (m_origin formal_0_253) 1)) false))
; source callback transition phase=insert-tail[11:24:11]:sift-compare
(define-fun formal_0_254 () FormalMachine (FormalCallback formal_0_253 boundary_0 (select (m_origin formal_0_253) 22) (select (m_origin formal_0_253) 1)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:11]
(define-fun formal_0_255 () FormalMachine (FormalWriteFromOrigin formal_0_254 18 1))
; source callback case=hoare-partition phase=insert-tail[11:24:11]:sift-compare
(assert (not (m_panicked formal_0_255)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_255) (select (m_origin formal_0_255) 22) (select (m_origin formal_0_255) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_255) (select (m_origin formal_0_255) 22) (select (m_origin formal_0_255) 24)) false))
; source callback transition phase=insert-tail[11:24:11]:sift-compare
(define-fun formal_0_256 () FormalMachine (FormalCallback formal_0_255 boundary_0 (select (m_origin formal_0_255) 22) (select (m_origin formal_0_255) 24)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:11]
(define-fun formal_0_257 () FormalMachine (FormalWriteFromOrigin formal_0_256 17 24))
; source callback case=hoare-partition phase=insert-tail[11:24:11]:sift-compare
(assert (not (m_panicked formal_0_257)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_257) (select (m_origin formal_0_257) 22) (select (m_origin formal_0_257) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_257) (select (m_origin formal_0_257) 22) (select (m_origin formal_0_257) 2)) false))
; source callback transition phase=insert-tail[11:24:11]:sift-compare
(define-fun formal_0_258 () FormalMachine (FormalCallback formal_0_257 boundary_0 (select (m_origin formal_0_257) 22) (select (m_origin formal_0_257) 2)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:11]
(define-fun formal_0_259 () FormalMachine (FormalWriteFromOrigin formal_0_258 16 2))
; source callback case=hoare-partition phase=insert-tail[11:24:11]:sift-compare
(assert (not (m_panicked formal_0_259)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_259) (select (m_origin formal_0_259) 22) (select (m_origin formal_0_259) 30)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_259) (select (m_origin formal_0_259) 22) (select (m_origin formal_0_259) 30)) false))
; source callback transition phase=insert-tail[11:24:11]:sift-compare
(define-fun formal_0_260 () FormalMachine (FormalCallback formal_0_259 boundary_0 (select (m_origin formal_0_259) 22) (select (m_origin formal_0_259) 30)))
; source write kind=copy-on-drop-restore phase=insert-tail[11:24:11]
(define-fun formal_0_261 () FormalMachine (FormalWriteFromOrigin formal_0_260 15 22))
; source callback case=hoare-partition phase=insert-tail[11:24:12]:initial-compare
(assert (not (m_panicked formal_0_261)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_261) (select (m_origin formal_0_261) 23) (select (m_origin formal_0_261) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_261) (select (m_origin formal_0_261) 23) (select (m_origin formal_0_261) 29)) false))
; source callback transition phase=insert-tail[11:24:12]:initial-compare
(define-fun formal_0_262 () FormalMachine (FormalCallback formal_0_261 boundary_0 (select (m_origin formal_0_261) 23) (select (m_origin formal_0_261) 29)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:12]
(define-fun formal_0_263 () FormalMachine (FormalWriteFromOrigin formal_0_262 23 29))
; source callback case=hoare-partition phase=insert-tail[11:24:12]:sift-compare
(assert (not (m_panicked formal_0_263)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_263) (select (m_origin formal_0_263) 23) (select (m_origin formal_0_263) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_263) (select (m_origin formal_0_263) 23) (select (m_origin formal_0_263) 17)) false))
; source callback transition phase=insert-tail[11:24:12]:sift-compare
(define-fun formal_0_264 () FormalMachine (FormalCallback formal_0_263 boundary_0 (select (m_origin formal_0_263) 23) (select (m_origin formal_0_263) 17)))
; source write kind=insert-tail-shift phase=insert-tail[11:24:12]
(define-fun formal_0_265 () FormalMachine (FormalWriteFromOrigin formal_0_264 22 17))
; source callback case=hoare-partition phase=insert-tail[11:24:12]:sift-compare
(assert (not (m_panicked formal_0_265)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_265) (select (m_origin formal_0_265) 23) (select (m_origin formal_0_265) 18)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_265) (select (m_origin formal_0_265) 23) (select (m_origin formal_0_265) 18)) false))
; source callback transition phase=insert-tail[11:24:12]:sift-compare
(define-fun formal_0_266 () FormalMachine (FormalCallback formal_0_265 boundary_0 (select (m_origin formal_0_265) 23) (select (m_origin formal_0_265) 18)))
; source write kind=copy-on-drop-restore phase=insert-tail[11:24:12]
(define-fun formal_0_267 () FormalMachine (FormalWriteFromOrigin formal_0_266 21 23))
; source callback case=hoare-partition phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_267)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_267) (select (m_origin formal_0_267) 13) (select (m_origin formal_0_267) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_267) (select (m_origin formal_0_267) 13) (select (m_origin formal_0_267) 33)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_268 () FormalMachine (FormalCallback formal_0_267 boundary_0 (select (m_origin formal_0_267) 13) (select (m_origin formal_0_267) 33)))
; source callback case=hoare-partition phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_268)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_268) (select (m_origin formal_0_268) 13) (select (m_origin formal_0_268) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_268) (select (m_origin formal_0_268) 13) (select (m_origin formal_0_268) 16)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_269 () FormalMachine (FormalCallback formal_0_268 boundary_0 (select (m_origin formal_0_268) 13) (select (m_origin formal_0_268) 16)))
; source callback case=hoare-partition phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_269)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_269) (select (m_origin formal_0_269) 33) (select (m_origin formal_0_269) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_269) (select (m_origin formal_0_269) 33) (select (m_origin formal_0_269) 16)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_270 () FormalMachine (FormalCallback formal_0_269 boundary_0 (select (m_origin formal_0_269) 33) (select (m_origin formal_0_269) 16)))
; source callback case=hoare-partition phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_270)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_270) (select (m_origin formal_0_270) 27) (select (m_origin formal_0_270) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_270) (select (m_origin formal_0_270) 27) (select (m_origin formal_0_270) 33)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_271 () FormalMachine (FormalCallback formal_0_270 boundary_0 (select (m_origin formal_0_270) 27) (select (m_origin formal_0_270) 33)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_272 () FormalMachine (FormalSwap formal_0_271 25 33))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_272)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_272) (select (m_origin formal_0_272) 21) (select (m_origin formal_0_272) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_272) (select (m_origin formal_0_272) 21) (select (m_origin formal_0_272) 33)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_273 () FormalMachine (FormalCallback formal_0_272 boundary_0 (select (m_origin formal_0_272) 21) (select (m_origin formal_0_272) 33)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_273)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_273) (select (m_origin formal_0_273) 11) (select (m_origin formal_0_273) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_273) (select (m_origin formal_0_273) 11) (select (m_origin formal_0_273) 33)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_274 () FormalMachine (FormalCallback formal_0_273 boundary_0 (select (m_origin formal_0_273) 11) (select (m_origin formal_0_273) 33)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_274)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_274) (select (m_origin formal_0_274) 44) (select (m_origin formal_0_274) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_274) (select (m_origin formal_0_274) 44) (select (m_origin formal_0_274) 33)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_275 () FormalMachine (FormalCallback formal_0_274 boundary_0 (select (m_origin formal_0_274) 44) (select (m_origin formal_0_274) 33)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_276 () FormalMachine (FormalWriteFromOrigin formal_0_275 27 44))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_276)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_276) (select (m_origin formal_0_276) 28) (select (m_origin formal_0_276) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_276) (select (m_origin formal_0_276) 28) (select (m_origin formal_0_276) 33)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_277 () FormalMachine (FormalCallback formal_0_276 boundary_0 (select (m_origin formal_0_276) 28) (select (m_origin formal_0_276) 33)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_277)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_277) (select (m_origin formal_0_277) 14) (select (m_origin formal_0_277) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_277) (select (m_origin formal_0_277) 14) (select (m_origin formal_0_277) 33)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_278 () FormalMachine (FormalCallback formal_0_277 boundary_0 (select (m_origin formal_0_277) 14) (select (m_origin formal_0_277) 33)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_279 () FormalMachine (FormalWriteFromOrigin formal_0_278 28 14))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_280 () FormalMachine (FormalWriteFromOrigin formal_0_279 44 28))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_280)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_280) (select (m_origin formal_0_280) 0) (select (m_origin formal_0_280) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_280) (select (m_origin formal_0_280) 0) (select (m_origin formal_0_280) 33)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_281 () FormalMachine (FormalCallback formal_0_280 boundary_0 (select (m_origin formal_0_280) 0) (select (m_origin formal_0_280) 33)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_281)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_281) (select (m_origin formal_0_281) 15) (select (m_origin formal_0_281) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_281) (select (m_origin formal_0_281) 15) (select (m_origin formal_0_281) 33)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_282 () FormalMachine (FormalCallback formal_0_281 boundary_0 (select (m_origin formal_0_281) 15) (select (m_origin formal_0_281) 33)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_282)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_282) (select (m_origin formal_0_282) 41) (select (m_origin formal_0_282) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_282) (select (m_origin formal_0_282) 41) (select (m_origin formal_0_282) 33)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_283 () FormalMachine (FormalCallback formal_0_282 boundary_0 (select (m_origin formal_0_282) 41) (select (m_origin formal_0_282) 33)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_284 () FormalMachine (FormalWriteFromOrigin formal_0_283 29 41))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_285 () FormalMachine (FormalWriteFromOrigin formal_0_284 43 0))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_285)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_285) (select (m_origin formal_0_285) 19) (select (m_origin formal_0_285) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_285) (select (m_origin formal_0_285) 19) (select (m_origin formal_0_285) 33)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_286 () FormalMachine (FormalCallback formal_0_285 boundary_0 (select (m_origin formal_0_285) 19) (select (m_origin formal_0_285) 33)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_286)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 40) (select (m_origin formal_0_286) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 40) (select (m_origin formal_0_286) 33)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_287 () FormalMachine (FormalCallback formal_0_286 boundary_0 (select (m_origin formal_0_286) 40) (select (m_origin formal_0_286) 33)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_287)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_287) (select (m_origin formal_0_287) 16) (select (m_origin formal_0_287) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_287) (select (m_origin formal_0_287) 16) (select (m_origin formal_0_287) 33)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_288 () FormalMachine (FormalCallback formal_0_287 boundary_0 (select (m_origin formal_0_287) 16) (select (m_origin formal_0_287) 33)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_288)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 38) (select (m_origin formal_0_288) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 38) (select (m_origin formal_0_288) 33)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_289 () FormalMachine (FormalCallback formal_0_288 boundary_0 (select (m_origin formal_0_288) 38) (select (m_origin formal_0_288) 33)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_290 () FormalMachine (FormalWriteFromOrigin formal_0_289 30 38))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_291 () FormalMachine (FormalWriteFromOrigin formal_0_290 41 19))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_291)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_291) (select (m_origin formal_0_291) 31) (select (m_origin formal_0_291) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_291) (select (m_origin formal_0_291) 31) (select (m_origin formal_0_291) 33)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_292 () FormalMachine (FormalCallback formal_0_291 boundary_0 (select (m_origin formal_0_291) 31) (select (m_origin formal_0_291) 33)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_292)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 32) (select (m_origin formal_0_292) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 32) (select (m_origin formal_0_292) 33)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_293 () FormalMachine (FormalCallback formal_0_292 boundary_0 (select (m_origin formal_0_292) 32) (select (m_origin formal_0_292) 33)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_293)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_293) (select (m_origin formal_0_293) 13) (select (m_origin formal_0_293) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_293) (select (m_origin formal_0_293) 13) (select (m_origin formal_0_293) 33)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_294 () FormalMachine (FormalCallback formal_0_293 boundary_0 (select (m_origin formal_0_293) 13) (select (m_origin formal_0_293) 33)))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_294)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_294) (select (m_origin formal_0_294) 7) (select (m_origin formal_0_294) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_294) (select (m_origin formal_0_294) 7) (select (m_origin formal_0_294) 33)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_295 () FormalMachine (FormalCallback formal_0_294 boundary_0 (select (m_origin formal_0_294) 7) (select (m_origin formal_0_294) 33)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_295)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_295) (select (m_origin formal_0_295) 4) (select (m_origin formal_0_295) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_295) (select (m_origin formal_0_295) 4) (select (m_origin formal_0_295) 33)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_296 () FormalMachine (FormalCallback formal_0_295 boundary_0 (select (m_origin formal_0_295) 4) (select (m_origin formal_0_295) 33)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_297 () FormalMachine (FormalWriteFromOrigin formal_0_296 34 4))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_298 () FormalMachine (FormalWriteFromOrigin formal_0_297 38 7))
; source callback case=hoare-partition phase=partition-hoare:left-scan
(assert (not (m_panicked formal_0_298)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_298) (select (m_origin formal_0_298) 6) (select (m_origin formal_0_298) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_298) (select (m_origin formal_0_298) 6) (select (m_origin formal_0_298) 33)) false))
; source callback transition phase=partition-hoare:left-scan
(define-fun formal_0_299 () FormalMachine (FormalCallback formal_0_298 boundary_0 (select (m_origin formal_0_298) 6) (select (m_origin formal_0_298) 33)))
; source callback case=hoare-partition phase=partition-hoare:right-scan
(assert (not (m_panicked formal_0_299)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_299) (select (m_origin formal_0_299) 5) (select (m_origin formal_0_299) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_299) (select (m_origin formal_0_299) 5) (select (m_origin formal_0_299) 33)) false))
; source callback transition phase=partition-hoare:right-scan
(define-fun formal_0_300 () FormalMachine (FormalCallback formal_0_299 boundary_0 (select (m_origin formal_0_299) 5) (select (m_origin formal_0_299) 33)))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_301 () FormalMachine (FormalWriteFromOrigin formal_0_300 35 5))
; source write kind=partition-cycle phase=partition-hoare-branchy-cyclic
(define-fun formal_0_302 () FormalMachine (FormalWriteFromOrigin formal_0_301 37 6))
; source write kind=gap-guard-restore phase=partition-hoare-branchy-cyclic
(define-fun formal_0_303 () FormalMachine (FormalWriteFromOrigin formal_0_302 36 11))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_304 () FormalMachine (FormalSwap formal_0_303 25 35))
; source callback case=hoare-partition phase=insert-tail[25:35:1]:initial-compare
(assert (not (m_panicked formal_0_304)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_304) (select (m_origin formal_0_304) 21) (select (m_origin formal_0_304) 5)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_304) (select (m_origin formal_0_304) 21) (select (m_origin formal_0_304) 5)) false))
; source callback transition phase=insert-tail[25:35:1]:initial-compare
(define-fun formal_0_305 () FormalMachine (FormalCallback formal_0_304 boundary_0 (select (m_origin formal_0_304) 21) (select (m_origin formal_0_304) 5)))
; source callback case=hoare-partition phase=insert-tail[25:35:2]:initial-compare
(assert (not (m_panicked formal_0_305)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_305) (select (m_origin formal_0_305) 44) (select (m_origin formal_0_305) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_305) (select (m_origin formal_0_305) 44) (select (m_origin formal_0_305) 21)) false))
; source callback transition phase=insert-tail[25:35:2]:initial-compare
(define-fun formal_0_306 () FormalMachine (FormalCallback formal_0_305 boundary_0 (select (m_origin formal_0_305) 44) (select (m_origin formal_0_305) 21)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:2]
(define-fun formal_0_307 () FormalMachine (FormalWriteFromOrigin formal_0_306 27 21))
; source callback case=hoare-partition phase=insert-tail[25:35:2]:sift-compare
(assert (not (m_panicked formal_0_307)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_307) (select (m_origin formal_0_307) 44) (select (m_origin formal_0_307) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_307) (select (m_origin formal_0_307) 44) (select (m_origin formal_0_307) 5)) false))
; source callback transition phase=insert-tail[25:35:2]:sift-compare
(define-fun formal_0_308 () FormalMachine (FormalCallback formal_0_307 boundary_0 (select (m_origin formal_0_307) 44) (select (m_origin formal_0_307) 5)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:2]
(define-fun formal_0_309 () FormalMachine (FormalWriteFromOrigin formal_0_308 26 5))
; source write kind=copy-on-drop-restore phase=insert-tail[25:35:2]
(define-fun formal_0_310 () FormalMachine (FormalWriteFromOrigin formal_0_309 25 44))
; source callback case=hoare-partition phase=insert-tail[25:35:3]:initial-compare
(assert (not (m_panicked formal_0_310)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_310) (select (m_origin formal_0_310) 14) (select (m_origin formal_0_310) 21)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_310) (select (m_origin formal_0_310) 14) (select (m_origin formal_0_310) 21)) false))
; source callback transition phase=insert-tail[25:35:3]:initial-compare
(define-fun formal_0_311 () FormalMachine (FormalCallback formal_0_310 boundary_0 (select (m_origin formal_0_310) 14) (select (m_origin formal_0_310) 21)))
; source callback case=hoare-partition phase=insert-tail[25:35:4]:initial-compare
(assert (not (m_panicked formal_0_311)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_311) (select (m_origin formal_0_311) 41) (select (m_origin formal_0_311) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_311) (select (m_origin formal_0_311) 41) (select (m_origin formal_0_311) 14)) false))
; source callback transition phase=insert-tail[25:35:4]:initial-compare
(define-fun formal_0_312 () FormalMachine (FormalCallback formal_0_311 boundary_0 (select (m_origin formal_0_311) 41) (select (m_origin formal_0_311) 14)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:4]
(define-fun formal_0_313 () FormalMachine (FormalWriteFromOrigin formal_0_312 29 14))
; source callback case=hoare-partition phase=insert-tail[25:35:4]:sift-compare
(assert (not (m_panicked formal_0_313)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_313) (select (m_origin formal_0_313) 41) (select (m_origin formal_0_313) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_313) (select (m_origin formal_0_313) 41) (select (m_origin formal_0_313) 21)) false))
; source callback transition phase=insert-tail[25:35:4]:sift-compare
(define-fun formal_0_314 () FormalMachine (FormalCallback formal_0_313 boundary_0 (select (m_origin formal_0_313) 41) (select (m_origin formal_0_313) 21)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:4]
(define-fun formal_0_315 () FormalMachine (FormalWriteFromOrigin formal_0_314 28 21))
; source callback case=hoare-partition phase=insert-tail[25:35:4]:sift-compare
(assert (not (m_panicked formal_0_315)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_315) (select (m_origin formal_0_315) 41) (select (m_origin formal_0_315) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_315) (select (m_origin formal_0_315) 41) (select (m_origin formal_0_315) 5)) false))
; source callback transition phase=insert-tail[25:35:4]:sift-compare
(define-fun formal_0_316 () FormalMachine (FormalCallback formal_0_315 boundary_0 (select (m_origin formal_0_315) 41) (select (m_origin formal_0_315) 5)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:4]
(define-fun formal_0_317 () FormalMachine (FormalWriteFromOrigin formal_0_316 27 5))
; source callback case=hoare-partition phase=insert-tail[25:35:4]:sift-compare
(assert (not (m_panicked formal_0_317)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_317) (select (m_origin formal_0_317) 41) (select (m_origin formal_0_317) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_317) (select (m_origin formal_0_317) 41) (select (m_origin formal_0_317) 44)) false))
; source callback transition phase=insert-tail[25:35:4]:sift-compare
(define-fun formal_0_318 () FormalMachine (FormalCallback formal_0_317 boundary_0 (select (m_origin formal_0_317) 41) (select (m_origin formal_0_317) 44)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:4]
(define-fun formal_0_319 () FormalMachine (FormalWriteFromOrigin formal_0_318 26 44))
; source write kind=copy-on-drop-restore phase=insert-tail[25:35:4]
(define-fun formal_0_320 () FormalMachine (FormalWriteFromOrigin formal_0_319 25 41))
; source callback case=hoare-partition phase=insert-tail[25:35:5]:initial-compare
(assert (not (m_panicked formal_0_320)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_320) (select (m_origin formal_0_320) 38) (select (m_origin formal_0_320) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_320) (select (m_origin formal_0_320) 38) (select (m_origin formal_0_320) 14)) false))
; source callback transition phase=insert-tail[25:35:5]:initial-compare
(define-fun formal_0_321 () FormalMachine (FormalCallback formal_0_320 boundary_0 (select (m_origin formal_0_320) 38) (select (m_origin formal_0_320) 14)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:5]
(define-fun formal_0_322 () FormalMachine (FormalWriteFromOrigin formal_0_321 30 14))
; source callback case=hoare-partition phase=insert-tail[25:35:5]:sift-compare
(assert (not (m_panicked formal_0_322)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 38) (select (m_origin formal_0_322) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 38) (select (m_origin formal_0_322) 21)) false))
; source callback transition phase=insert-tail[25:35:5]:sift-compare
(define-fun formal_0_323 () FormalMachine (FormalCallback formal_0_322 boundary_0 (select (m_origin formal_0_322) 38) (select (m_origin formal_0_322) 21)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:5]
(define-fun formal_0_324 () FormalMachine (FormalWriteFromOrigin formal_0_323 29 21))
; source callback case=hoare-partition phase=insert-tail[25:35:5]:sift-compare
(assert (not (m_panicked formal_0_324)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_324) (select (m_origin formal_0_324) 38) (select (m_origin formal_0_324) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_324) (select (m_origin formal_0_324) 38) (select (m_origin formal_0_324) 5)) false))
; source callback transition phase=insert-tail[25:35:5]:sift-compare
(define-fun formal_0_325 () FormalMachine (FormalCallback formal_0_324 boundary_0 (select (m_origin formal_0_324) 38) (select (m_origin formal_0_324) 5)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:5]
(define-fun formal_0_326 () FormalMachine (FormalWriteFromOrigin formal_0_325 28 5))
; source callback case=hoare-partition phase=insert-tail[25:35:5]:sift-compare
(assert (not (m_panicked formal_0_326)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_326) (select (m_origin formal_0_326) 38) (select (m_origin formal_0_326) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_326) (select (m_origin formal_0_326) 38) (select (m_origin formal_0_326) 44)) false))
; source callback transition phase=insert-tail[25:35:5]:sift-compare
(define-fun formal_0_327 () FormalMachine (FormalCallback formal_0_326 boundary_0 (select (m_origin formal_0_326) 38) (select (m_origin formal_0_326) 44)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:5]
(define-fun formal_0_328 () FormalMachine (FormalWriteFromOrigin formal_0_327 27 44))
; source callback case=hoare-partition phase=insert-tail[25:35:5]:sift-compare
(assert (not (m_panicked formal_0_328)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_328) (select (m_origin formal_0_328) 38) (select (m_origin formal_0_328) 41)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_328) (select (m_origin formal_0_328) 38) (select (m_origin formal_0_328) 41)) false))
; source callback transition phase=insert-tail[25:35:5]:sift-compare
(define-fun formal_0_329 () FormalMachine (FormalCallback formal_0_328 boundary_0 (select (m_origin formal_0_328) 38) (select (m_origin formal_0_328) 41)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:5]
(define-fun formal_0_330 () FormalMachine (FormalWriteFromOrigin formal_0_329 26 41))
; source write kind=copy-on-drop-restore phase=insert-tail[25:35:5]
(define-fun formal_0_331 () FormalMachine (FormalWriteFromOrigin formal_0_330 25 38))
; source callback case=hoare-partition phase=insert-tail[25:35:6]:initial-compare
(assert (not (m_panicked formal_0_331)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_331) (select (m_origin formal_0_331) 31) (select (m_origin formal_0_331) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_331) (select (m_origin formal_0_331) 31) (select (m_origin formal_0_331) 14)) false))
; source callback transition phase=insert-tail[25:35:6]:initial-compare
(define-fun formal_0_332 () FormalMachine (FormalCallback formal_0_331 boundary_0 (select (m_origin formal_0_331) 31) (select (m_origin formal_0_331) 14)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:6]
(define-fun formal_0_333 () FormalMachine (FormalWriteFromOrigin formal_0_332 31 14))
; source callback case=hoare-partition phase=insert-tail[25:35:6]:sift-compare
(assert (not (m_panicked formal_0_333)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_333) (select (m_origin formal_0_333) 31) (select (m_origin formal_0_333) 21)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_333) (select (m_origin formal_0_333) 31) (select (m_origin formal_0_333) 21)) false))
; source callback transition phase=insert-tail[25:35:6]:sift-compare
(define-fun formal_0_334 () FormalMachine (FormalCallback formal_0_333 boundary_0 (select (m_origin formal_0_333) 31) (select (m_origin formal_0_333) 21)))
; source write kind=copy-on-drop-restore phase=insert-tail[25:35:6]
(define-fun formal_0_335 () FormalMachine (FormalWriteFromOrigin formal_0_334 30 31))
; source callback case=hoare-partition phase=insert-tail[25:35:7]:initial-compare
(assert (not (m_panicked formal_0_335)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_335) (select (m_origin formal_0_335) 32) (select (m_origin formal_0_335) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_335) (select (m_origin formal_0_335) 32) (select (m_origin formal_0_335) 14)) false))
; source callback transition phase=insert-tail[25:35:7]:initial-compare
(define-fun formal_0_336 () FormalMachine (FormalCallback formal_0_335 boundary_0 (select (m_origin formal_0_335) 32) (select (m_origin formal_0_335) 14)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:7]
(define-fun formal_0_337 () FormalMachine (FormalWriteFromOrigin formal_0_336 32 14))
; source callback case=hoare-partition phase=insert-tail[25:35:7]:sift-compare
(assert (not (m_panicked formal_0_337)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_337) (select (m_origin formal_0_337) 32) (select (m_origin formal_0_337) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_337) (select (m_origin formal_0_337) 32) (select (m_origin formal_0_337) 31)) false))
; source callback transition phase=insert-tail[25:35:7]:sift-compare
(define-fun formal_0_338 () FormalMachine (FormalCallback formal_0_337 boundary_0 (select (m_origin formal_0_337) 32) (select (m_origin formal_0_337) 31)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:7]
(define-fun formal_0_339 () FormalMachine (FormalWriteFromOrigin formal_0_338 31 31))
; source callback case=hoare-partition phase=insert-tail[25:35:7]:sift-compare
(assert (not (m_panicked formal_0_339)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_339) (select (m_origin formal_0_339) 32) (select (m_origin formal_0_339) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_339) (select (m_origin formal_0_339) 32) (select (m_origin formal_0_339) 21)) false))
; source callback transition phase=insert-tail[25:35:7]:sift-compare
(define-fun formal_0_340 () FormalMachine (FormalCallback formal_0_339 boundary_0 (select (m_origin formal_0_339) 32) (select (m_origin formal_0_339) 21)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:7]
(define-fun formal_0_341 () FormalMachine (FormalWriteFromOrigin formal_0_340 30 21))
; source callback case=hoare-partition phase=insert-tail[25:35:7]:sift-compare
(assert (not (m_panicked formal_0_341)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_341) (select (m_origin formal_0_341) 32) (select (m_origin formal_0_341) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_341) (select (m_origin formal_0_341) 32) (select (m_origin formal_0_341) 5)) false))
; source callback transition phase=insert-tail[25:35:7]:sift-compare
(define-fun formal_0_342 () FormalMachine (FormalCallback formal_0_341 boundary_0 (select (m_origin formal_0_341) 32) (select (m_origin formal_0_341) 5)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:7]
(define-fun formal_0_343 () FormalMachine (FormalWriteFromOrigin formal_0_342 29 5))
; source callback case=hoare-partition phase=insert-tail[25:35:7]:sift-compare
(assert (not (m_panicked formal_0_343)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_343) (select (m_origin formal_0_343) 32) (select (m_origin formal_0_343) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_343) (select (m_origin formal_0_343) 32) (select (m_origin formal_0_343) 44)) false))
; source callback transition phase=insert-tail[25:35:7]:sift-compare
(define-fun formal_0_344 () FormalMachine (FormalCallback formal_0_343 boundary_0 (select (m_origin formal_0_343) 32) (select (m_origin formal_0_343) 44)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:7]
(define-fun formal_0_345 () FormalMachine (FormalWriteFromOrigin formal_0_344 28 44))
; source callback case=hoare-partition phase=insert-tail[25:35:7]:sift-compare
(assert (not (m_panicked formal_0_345)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_345) (select (m_origin formal_0_345) 32) (select (m_origin formal_0_345) 41)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_345) (select (m_origin formal_0_345) 32) (select (m_origin formal_0_345) 41)) false))
; source callback transition phase=insert-tail[25:35:7]:sift-compare
(define-fun formal_0_346 () FormalMachine (FormalCallback formal_0_345 boundary_0 (select (m_origin formal_0_345) 32) (select (m_origin formal_0_345) 41)))
; source write kind=copy-on-drop-restore phase=insert-tail[25:35:7]
(define-fun formal_0_347 () FormalMachine (FormalWriteFromOrigin formal_0_346 27 32))
; source callback case=hoare-partition phase=insert-tail[25:35:8]:initial-compare
(assert (not (m_panicked formal_0_347)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_347) (select (m_origin formal_0_347) 13) (select (m_origin formal_0_347) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_347) (select (m_origin formal_0_347) 13) (select (m_origin formal_0_347) 14)) false))
; source callback transition phase=insert-tail[25:35:8]:initial-compare
(define-fun formal_0_348 () FormalMachine (FormalCallback formal_0_347 boundary_0 (select (m_origin formal_0_347) 13) (select (m_origin formal_0_347) 14)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:8]
(define-fun formal_0_349 () FormalMachine (FormalWriteFromOrigin formal_0_348 33 14))
; source callback case=hoare-partition phase=insert-tail[25:35:8]:sift-compare
(assert (not (m_panicked formal_0_349)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_349) (select (m_origin formal_0_349) 13) (select (m_origin formal_0_349) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_349) (select (m_origin formal_0_349) 13) (select (m_origin formal_0_349) 31)) false))
; source callback transition phase=insert-tail[25:35:8]:sift-compare
(define-fun formal_0_350 () FormalMachine (FormalCallback formal_0_349 boundary_0 (select (m_origin formal_0_349) 13) (select (m_origin formal_0_349) 31)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:8]
(define-fun formal_0_351 () FormalMachine (FormalWriteFromOrigin formal_0_350 32 31))
; source callback case=hoare-partition phase=insert-tail[25:35:8]:sift-compare
(assert (not (m_panicked formal_0_351)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_351) (select (m_origin formal_0_351) 13) (select (m_origin formal_0_351) 21)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_351) (select (m_origin formal_0_351) 13) (select (m_origin formal_0_351) 21)) false))
; source callback transition phase=insert-tail[25:35:8]:sift-compare
(define-fun formal_0_352 () FormalMachine (FormalCallback formal_0_351 boundary_0 (select (m_origin formal_0_351) 13) (select (m_origin formal_0_351) 21)))
; source write kind=copy-on-drop-restore phase=insert-tail[25:35:8]
(define-fun formal_0_353 () FormalMachine (FormalWriteFromOrigin formal_0_352 31 13))
; source callback case=hoare-partition phase=insert-tail[25:35:9]:initial-compare
(assert (not (m_panicked formal_0_353)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_353) (select (m_origin formal_0_353) 4) (select (m_origin formal_0_353) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_353) (select (m_origin formal_0_353) 4) (select (m_origin formal_0_353) 14)) false))
; source callback transition phase=insert-tail[25:35:9]:initial-compare
(define-fun formal_0_354 () FormalMachine (FormalCallback formal_0_353 boundary_0 (select (m_origin formal_0_353) 4) (select (m_origin formal_0_353) 14)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:9]
(define-fun formal_0_355 () FormalMachine (FormalWriteFromOrigin formal_0_354 34 14))
; source callback case=hoare-partition phase=insert-tail[25:35:9]:sift-compare
(assert (not (m_panicked formal_0_355)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_355) (select (m_origin formal_0_355) 4) (select (m_origin formal_0_355) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_355) (select (m_origin formal_0_355) 4) (select (m_origin formal_0_355) 31)) false))
; source callback transition phase=insert-tail[25:35:9]:sift-compare
(define-fun formal_0_356 () FormalMachine (FormalCallback formal_0_355 boundary_0 (select (m_origin formal_0_355) 4) (select (m_origin formal_0_355) 31)))
; source write kind=insert-tail-shift phase=insert-tail[25:35:9]
(define-fun formal_0_357 () FormalMachine (FormalWriteFromOrigin formal_0_356 33 31))
; source callback case=hoare-partition phase=insert-tail[25:35:9]:sift-compare
(assert (not (m_panicked formal_0_357)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 4) (select (m_origin formal_0_357) 13)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 4) (select (m_origin formal_0_357) 13)) false))
; source callback transition phase=insert-tail[25:35:9]:sift-compare
(define-fun formal_0_358 () FormalMachine (FormalCallback formal_0_357 boundary_0 (select (m_origin formal_0_357) 4) (select (m_origin formal_0_357) 13)))
; source write kind=copy-on-drop-restore phase=insert-tail[25:35:9]
(define-fun formal_0_359 () FormalMachine (FormalWriteFromOrigin formal_0_358 32 4))
; source callback case=hoare-partition phase=insert-tail[36:45:1]:initial-compare
(assert (not (m_panicked formal_0_359)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_359) (select (m_origin formal_0_359) 6) (select (m_origin formal_0_359) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_359) (select (m_origin formal_0_359) 6) (select (m_origin formal_0_359) 11)) false))
; source callback transition phase=insert-tail[36:45:1]:initial-compare
(define-fun formal_0_360 () FormalMachine (FormalCallback formal_0_359 boundary_0 (select (m_origin formal_0_359) 6) (select (m_origin formal_0_359) 11)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:1]
(define-fun formal_0_361 () FormalMachine (FormalWriteFromOrigin formal_0_360 37 11))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:1]
(define-fun formal_0_362 () FormalMachine (FormalWriteFromOrigin formal_0_361 36 6))
; source callback case=hoare-partition phase=insert-tail[36:45:2]:initial-compare
(assert (not (m_panicked formal_0_362)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_362) (select (m_origin formal_0_362) 7) (select (m_origin formal_0_362) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_362) (select (m_origin formal_0_362) 7) (select (m_origin formal_0_362) 11)) false))
; source callback transition phase=insert-tail[36:45:2]:initial-compare
(define-fun formal_0_363 () FormalMachine (FormalCallback formal_0_362 boundary_0 (select (m_origin formal_0_362) 7) (select (m_origin formal_0_362) 11)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:2]
(define-fun formal_0_364 () FormalMachine (FormalWriteFromOrigin formal_0_363 38 11))
; source callback case=hoare-partition phase=insert-tail[36:45:2]:sift-compare
(assert (not (m_panicked formal_0_364)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_364) (select (m_origin formal_0_364) 7) (select (m_origin formal_0_364) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_364) (select (m_origin formal_0_364) 7) (select (m_origin formal_0_364) 6)) false))
; source callback transition phase=insert-tail[36:45:2]:sift-compare
(define-fun formal_0_365 () FormalMachine (FormalCallback formal_0_364 boundary_0 (select (m_origin formal_0_364) 7) (select (m_origin formal_0_364) 6)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:2]
(define-fun formal_0_366 () FormalMachine (FormalWriteFromOrigin formal_0_365 37 6))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:2]
(define-fun formal_0_367 () FormalMachine (FormalWriteFromOrigin formal_0_366 36 7))
; source callback case=hoare-partition phase=insert-tail[36:45:3]:initial-compare
(assert (not (m_panicked formal_0_367)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_367) (select (m_origin formal_0_367) 16) (select (m_origin formal_0_367) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_367) (select (m_origin formal_0_367) 16) (select (m_origin formal_0_367) 11)) false))
; source callback transition phase=insert-tail[36:45:3]:initial-compare
(define-fun formal_0_368 () FormalMachine (FormalCallback formal_0_367 boundary_0 (select (m_origin formal_0_367) 16) (select (m_origin formal_0_367) 11)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:3]
(define-fun formal_0_369 () FormalMachine (FormalWriteFromOrigin formal_0_368 39 11))
; source callback case=hoare-partition phase=insert-tail[36:45:3]:sift-compare
(assert (not (m_panicked formal_0_369)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_369) (select (m_origin formal_0_369) 16) (select (m_origin formal_0_369) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_369) (select (m_origin formal_0_369) 16) (select (m_origin formal_0_369) 6)) false))
; source callback transition phase=insert-tail[36:45:3]:sift-compare
(define-fun formal_0_370 () FormalMachine (FormalCallback formal_0_369 boundary_0 (select (m_origin formal_0_369) 16) (select (m_origin formal_0_369) 6)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:3]
(define-fun formal_0_371 () FormalMachine (FormalWriteFromOrigin formal_0_370 38 6))
; source callback case=hoare-partition phase=insert-tail[36:45:3]:sift-compare
(assert (not (m_panicked formal_0_371)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_371) (select (m_origin formal_0_371) 16) (select (m_origin formal_0_371) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_371) (select (m_origin formal_0_371) 16) (select (m_origin formal_0_371) 7)) false))
; source callback transition phase=insert-tail[36:45:3]:sift-compare
(define-fun formal_0_372 () FormalMachine (FormalCallback formal_0_371 boundary_0 (select (m_origin formal_0_371) 16) (select (m_origin formal_0_371) 7)))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:3]
(define-fun formal_0_373 () FormalMachine (FormalWriteFromOrigin formal_0_372 37 16))
; source callback case=hoare-partition phase=insert-tail[36:45:4]:initial-compare
(assert (not (m_panicked formal_0_373)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_373) (select (m_origin formal_0_373) 40) (select (m_origin formal_0_373) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_373) (select (m_origin formal_0_373) 40) (select (m_origin formal_0_373) 11)) false))
; source callback transition phase=insert-tail[36:45:4]:initial-compare
(define-fun formal_0_374 () FormalMachine (FormalCallback formal_0_373 boundary_0 (select (m_origin formal_0_373) 40) (select (m_origin formal_0_373) 11)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:4]
(define-fun formal_0_375 () FormalMachine (FormalWriteFromOrigin formal_0_374 40 11))
; source callback case=hoare-partition phase=insert-tail[36:45:4]:sift-compare
(assert (not (m_panicked formal_0_375)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_375) (select (m_origin formal_0_375) 40) (select (m_origin formal_0_375) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_375) (select (m_origin formal_0_375) 40) (select (m_origin formal_0_375) 6)) false))
; source callback transition phase=insert-tail[36:45:4]:sift-compare
(define-fun formal_0_376 () FormalMachine (FormalCallback formal_0_375 boundary_0 (select (m_origin formal_0_375) 40) (select (m_origin formal_0_375) 6)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:4]
(define-fun formal_0_377 () FormalMachine (FormalWriteFromOrigin formal_0_376 39 6))
; source callback case=hoare-partition phase=insert-tail[36:45:4]:sift-compare
(assert (not (m_panicked formal_0_377)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_377) (select (m_origin formal_0_377) 40) (select (m_origin formal_0_377) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_377) (select (m_origin formal_0_377) 40) (select (m_origin formal_0_377) 16)) false))
; source callback transition phase=insert-tail[36:45:4]:sift-compare
(define-fun formal_0_378 () FormalMachine (FormalCallback formal_0_377 boundary_0 (select (m_origin formal_0_377) 40) (select (m_origin formal_0_377) 16)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:4]
(define-fun formal_0_379 () FormalMachine (FormalWriteFromOrigin formal_0_378 38 16))
; source callback case=hoare-partition phase=insert-tail[36:45:4]:sift-compare
(assert (not (m_panicked formal_0_379)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_379) (select (m_origin formal_0_379) 40) (select (m_origin formal_0_379) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_379) (select (m_origin formal_0_379) 40) (select (m_origin formal_0_379) 7)) false))
; source callback transition phase=insert-tail[36:45:4]:sift-compare
(define-fun formal_0_380 () FormalMachine (FormalCallback formal_0_379 boundary_0 (select (m_origin formal_0_379) 40) (select (m_origin formal_0_379) 7)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:4]
(define-fun formal_0_381 () FormalMachine (FormalWriteFromOrigin formal_0_380 37 7))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:4]
(define-fun formal_0_382 () FormalMachine (FormalWriteFromOrigin formal_0_381 36 40))
; source callback case=hoare-partition phase=insert-tail[36:45:5]:initial-compare
(assert (not (m_panicked formal_0_382)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_382) (select (m_origin formal_0_382) 19) (select (m_origin formal_0_382) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_382) (select (m_origin formal_0_382) 19) (select (m_origin formal_0_382) 11)) false))
; source callback transition phase=insert-tail[36:45:5]:initial-compare
(define-fun formal_0_383 () FormalMachine (FormalCallback formal_0_382 boundary_0 (select (m_origin formal_0_382) 19) (select (m_origin formal_0_382) 11)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:5]
(define-fun formal_0_384 () FormalMachine (FormalWriteFromOrigin formal_0_383 41 11))
; source callback case=hoare-partition phase=insert-tail[36:45:5]:sift-compare
(assert (not (m_panicked formal_0_384)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_384) (select (m_origin formal_0_384) 19) (select (m_origin formal_0_384) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_384) (select (m_origin formal_0_384) 19) (select (m_origin formal_0_384) 6)) false))
; source callback transition phase=insert-tail[36:45:5]:sift-compare
(define-fun formal_0_385 () FormalMachine (FormalCallback formal_0_384 boundary_0 (select (m_origin formal_0_384) 19) (select (m_origin formal_0_384) 6)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:5]
(define-fun formal_0_386 () FormalMachine (FormalWriteFromOrigin formal_0_385 40 6))
; source callback case=hoare-partition phase=insert-tail[36:45:5]:sift-compare
(assert (not (m_panicked formal_0_386)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_386) (select (m_origin formal_0_386) 19) (select (m_origin formal_0_386) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_386) (select (m_origin formal_0_386) 19) (select (m_origin formal_0_386) 16)) false))
; source callback transition phase=insert-tail[36:45:5]:sift-compare
(define-fun formal_0_387 () FormalMachine (FormalCallback formal_0_386 boundary_0 (select (m_origin formal_0_386) 19) (select (m_origin formal_0_386) 16)))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:5]
(define-fun formal_0_388 () FormalMachine (FormalWriteFromOrigin formal_0_387 39 19))
; source callback case=hoare-partition phase=insert-tail[36:45:6]:initial-compare
(assert (not (m_panicked formal_0_388)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_388) (select (m_origin formal_0_388) 15) (select (m_origin formal_0_388) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_388) (select (m_origin formal_0_388) 15) (select (m_origin formal_0_388) 11)) false))
; source callback transition phase=insert-tail[36:45:6]:initial-compare
(define-fun formal_0_389 () FormalMachine (FormalCallback formal_0_388 boundary_0 (select (m_origin formal_0_388) 15) (select (m_origin formal_0_388) 11)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:6]
(define-fun formal_0_390 () FormalMachine (FormalWriteFromOrigin formal_0_389 42 11))
; source callback case=hoare-partition phase=insert-tail[36:45:6]:sift-compare
(assert (not (m_panicked formal_0_390)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_390) (select (m_origin formal_0_390) 15) (select (m_origin formal_0_390) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_390) (select (m_origin formal_0_390) 15) (select (m_origin formal_0_390) 6)) false))
; source callback transition phase=insert-tail[36:45:6]:sift-compare
(define-fun formal_0_391 () FormalMachine (FormalCallback formal_0_390 boundary_0 (select (m_origin formal_0_390) 15) (select (m_origin formal_0_390) 6)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:6]
(define-fun formal_0_392 () FormalMachine (FormalWriteFromOrigin formal_0_391 41 6))
; source callback case=hoare-partition phase=insert-tail[36:45:6]:sift-compare
(assert (not (m_panicked formal_0_392)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_392) (select (m_origin formal_0_392) 15) (select (m_origin formal_0_392) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_392) (select (m_origin formal_0_392) 15) (select (m_origin formal_0_392) 19)) false))
; source callback transition phase=insert-tail[36:45:6]:sift-compare
(define-fun formal_0_393 () FormalMachine (FormalCallback formal_0_392 boundary_0 (select (m_origin formal_0_392) 15) (select (m_origin formal_0_392) 19)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:6]
(define-fun formal_0_394 () FormalMachine (FormalWriteFromOrigin formal_0_393 40 19))
; source callback case=hoare-partition phase=insert-tail[36:45:6]:sift-compare
(assert (not (m_panicked formal_0_394)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_394) (select (m_origin formal_0_394) 15) (select (m_origin formal_0_394) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_394) (select (m_origin formal_0_394) 15) (select (m_origin formal_0_394) 16)) false))
; source callback transition phase=insert-tail[36:45:6]:sift-compare
(define-fun formal_0_395 () FormalMachine (FormalCallback formal_0_394 boundary_0 (select (m_origin formal_0_394) 15) (select (m_origin formal_0_394) 16)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:6]
(define-fun formal_0_396 () FormalMachine (FormalWriteFromOrigin formal_0_395 39 16))
; source callback case=hoare-partition phase=insert-tail[36:45:6]:sift-compare
(assert (not (m_panicked formal_0_396)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_396) (select (m_origin formal_0_396) 15) (select (m_origin formal_0_396) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_396) (select (m_origin formal_0_396) 15) (select (m_origin formal_0_396) 7)) false))
; source callback transition phase=insert-tail[36:45:6]:sift-compare
(define-fun formal_0_397 () FormalMachine (FormalCallback formal_0_396 boundary_0 (select (m_origin formal_0_396) 15) (select (m_origin formal_0_396) 7)))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:6]
(define-fun formal_0_398 () FormalMachine (FormalWriteFromOrigin formal_0_397 38 15))
; source callback case=hoare-partition phase=insert-tail[36:45:7]:initial-compare
(assert (not (m_panicked formal_0_398)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_398) (select (m_origin formal_0_398) 0) (select (m_origin formal_0_398) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_398) (select (m_origin formal_0_398) 0) (select (m_origin formal_0_398) 11)) false))
; source callback transition phase=insert-tail[36:45:7]:initial-compare
(define-fun formal_0_399 () FormalMachine (FormalCallback formal_0_398 boundary_0 (select (m_origin formal_0_398) 0) (select (m_origin formal_0_398) 11)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:7]
(define-fun formal_0_400 () FormalMachine (FormalWriteFromOrigin formal_0_399 43 11))
; source callback case=hoare-partition phase=insert-tail[36:45:7]:sift-compare
(assert (not (m_panicked formal_0_400)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_400) (select (m_origin formal_0_400) 0) (select (m_origin formal_0_400) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_400) (select (m_origin formal_0_400) 0) (select (m_origin formal_0_400) 6)) false))
; source callback transition phase=insert-tail[36:45:7]:sift-compare
(define-fun formal_0_401 () FormalMachine (FormalCallback formal_0_400 boundary_0 (select (m_origin formal_0_400) 0) (select (m_origin formal_0_400) 6)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:7]
(define-fun formal_0_402 () FormalMachine (FormalWriteFromOrigin formal_0_401 42 6))
; source callback case=hoare-partition phase=insert-tail[36:45:7]:sift-compare
(assert (not (m_panicked formal_0_402)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_402) (select (m_origin formal_0_402) 0) (select (m_origin formal_0_402) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_402) (select (m_origin formal_0_402) 0) (select (m_origin formal_0_402) 19)) false))
; source callback transition phase=insert-tail[36:45:7]:sift-compare
(define-fun formal_0_403 () FormalMachine (FormalCallback formal_0_402 boundary_0 (select (m_origin formal_0_402) 0) (select (m_origin formal_0_402) 19)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:7]
(define-fun formal_0_404 () FormalMachine (FormalWriteFromOrigin formal_0_403 41 19))
; source callback case=hoare-partition phase=insert-tail[36:45:7]:sift-compare
(assert (not (m_panicked formal_0_404)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_404) (select (m_origin formal_0_404) 0) (select (m_origin formal_0_404) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_404) (select (m_origin formal_0_404) 0) (select (m_origin formal_0_404) 16)) false))
; source callback transition phase=insert-tail[36:45:7]:sift-compare
(define-fun formal_0_405 () FormalMachine (FormalCallback formal_0_404 boundary_0 (select (m_origin formal_0_404) 0) (select (m_origin formal_0_404) 16)))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:7]
(define-fun formal_0_406 () FormalMachine (FormalWriteFromOrigin formal_0_405 40 0))
; source callback case=hoare-partition phase=insert-tail[36:45:8]:initial-compare
(assert (not (m_panicked formal_0_406)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_406) (select (m_origin formal_0_406) 28) (select (m_origin formal_0_406) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_406) (select (m_origin formal_0_406) 28) (select (m_origin formal_0_406) 11)) false))
; source callback transition phase=insert-tail[36:45:8]:initial-compare
(define-fun formal_0_407 () FormalMachine (FormalCallback formal_0_406 boundary_0 (select (m_origin formal_0_406) 28) (select (m_origin formal_0_406) 11)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:8]
(define-fun formal_0_408 () FormalMachine (FormalWriteFromOrigin formal_0_407 44 11))
; source callback case=hoare-partition phase=insert-tail[36:45:8]:sift-compare
(assert (not (m_panicked formal_0_408)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_408) (select (m_origin formal_0_408) 28) (select (m_origin formal_0_408) 6)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_408) (select (m_origin formal_0_408) 28) (select (m_origin formal_0_408) 6)) false))
; source callback transition phase=insert-tail[36:45:8]:sift-compare
(define-fun formal_0_409 () FormalMachine (FormalCallback formal_0_408 boundary_0 (select (m_origin formal_0_408) 28) (select (m_origin formal_0_408) 6)))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:8]
(define-fun formal_0_410 () FormalMachine (FormalWriteFromOrigin formal_0_409 43 28))
(define-fun formal_result_0 () Result
  (mkResult
    (m_sequence formal_0_410)
    (m_callback formal_0_410)
    (m_panicked formal_0_410)
    false
    true
    (ite (m_panicked formal_0_410) 1 0)
    (not (m_panicked formal_0_410))
    -1))
(define-fun reference_result_0 () Result (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 21 21) 22 22) 23 23) 24 24) 25 25) 26 26) 27 27) 28 28) 29 29) 30 30) 31 31) 32 32) 33 33) 34 34) 35 35) 36 36) 37 37) 38 38) 39 39) 40 40) 41 41) 42 42) 43 43) 44 44) 234 false false true 0 true -1))
; retained source-forcing witness: hoare-cyclic
(assert (= formal_result_0 (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 21 21) 22 22) 23 23) 24 24) 25 25) 26 26) 27 27) 28 28) 29 29) 30 30) 31 31) 32 32) 33 33) 34 34) 35 35) 36 36) 37 37) 38 38) 39 39) 40 40) 41 41) 42 42) 43 43) 44 44) 234 false false true 0 true -1)))
(check-sat-using (then ctx-solver-simplify smt))
