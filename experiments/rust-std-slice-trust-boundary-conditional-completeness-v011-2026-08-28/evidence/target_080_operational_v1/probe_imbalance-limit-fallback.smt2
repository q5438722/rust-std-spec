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

; formal source input case=imbalance-fallback-direct
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
    8
    false
    false))
(define-fun source_initial_0 () FormalMachine
  (mkFormalMachine (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 34) 1 3) 2 11) 3 7) 4 33) 5 1) 6 10) 7 9) 8 24) 9 19) 10 30) 11 29) 12 16) 13 36) 14 35) 15 26) 16 31) 17 23) 18 25) 19 32) 20 5) 21 28) 22 22) 23 0) 24 21) 25 14) 26 4) 27 20) 28 27) 29 18) 30 38) 31 12) 32 39) 33 2) 34 17) 35 13) 36 37) 37 8) 38 6) 39 15) (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 34) 1 3) 2 11) 3 7) 4 33) 5 1) 6 10) 7 9) 8 24) 9 19) 10 30) 11 29) 12 16) 13 36) 14 35) 15 26) 16 31) 17 23) 18 25) 19 32) 20 5) 21 28) 22 22) 23 0) 24 21) 25 14) 26 4) 27 20) 28 27) 29 18) 30 38) 31 12) 32 39) 33 2) 34 17) 35 13) 36 37) 37 8) 38 6) 39 15) (b_initial_state boundary_0) false))
(assert (BoundaryWellFormed boundary_0))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[59]:parent-child
(assert (not (m_panicked source_initial_0)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 19) (select (m_origin source_initial_0) 39)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 19) (select (m_origin source_initial_0) 39)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[59]:parent-child
(define-fun formal_0_1 () FormalMachine (FormalCallback source_initial_0 boundary_0 (select (m_origin source_initial_0) 19) (select (m_origin source_initial_0) 39)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[58]:choose-greater-child
(assert (not (m_panicked formal_0_1)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 37) (select (m_origin formal_0_1) 38)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 37) (select (m_origin formal_0_1) 38)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[58]:choose-greater-child
(define-fun formal_0_2 () FormalMachine (FormalCallback formal_0_1 boundary_0 (select (m_origin formal_0_1) 37) (select (m_origin formal_0_1) 38)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[58]:parent-child
(assert (not (m_panicked formal_0_2)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 18) (select (m_origin formal_0_2) 37)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 18) (select (m_origin formal_0_2) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[58]:parent-child
(define-fun formal_0_3 () FormalMachine (FormalCallback formal_0_2 boundary_0 (select (m_origin formal_0_2) 18) (select (m_origin formal_0_2) 37)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[57]:choose-greater-child
(assert (not (m_panicked formal_0_3)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 35) (select (m_origin formal_0_3) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 35) (select (m_origin formal_0_3) 36)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[57]:choose-greater-child
(define-fun formal_0_4 () FormalMachine (FormalCallback formal_0_3 boundary_0 (select (m_origin formal_0_3) 35) (select (m_origin formal_0_3) 36)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[57]:parent-child
(assert (not (m_panicked formal_0_4)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 17) (select (m_origin formal_0_4) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 17) (select (m_origin formal_0_4) 36)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[57]:parent-child
(define-fun formal_0_5 () FormalMachine (FormalCallback formal_0_4 boundary_0 (select (m_origin formal_0_4) 17) (select (m_origin formal_0_4) 36)))
; source swap phase=quicksort:imbalance-fallback:sift-down[57]:swap
(define-fun formal_0_6 () FormalMachine (FormalSwap formal_0_5 17 36))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[56]:choose-greater-child
(assert (not (m_panicked formal_0_6)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 33) (select (m_origin formal_0_6) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 33) (select (m_origin formal_0_6) 34)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[56]:choose-greater-child
(define-fun formal_0_7 () FormalMachine (FormalCallback formal_0_6 boundary_0 (select (m_origin formal_0_6) 33) (select (m_origin formal_0_6) 34)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[56]:parent-child
(assert (not (m_panicked formal_0_7)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_7) (select (m_origin formal_0_7) 16) (select (m_origin formal_0_7) 34)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_7) (select (m_origin formal_0_7) 16) (select (m_origin formal_0_7) 34)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[56]:parent-child
(define-fun formal_0_8 () FormalMachine (FormalCallback formal_0_7 boundary_0 (select (m_origin formal_0_7) 16) (select (m_origin formal_0_7) 34)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[55]:choose-greater-child
(assert (not (m_panicked formal_0_8)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 31) (select (m_origin formal_0_8) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 31) (select (m_origin formal_0_8) 32)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[55]:choose-greater-child
(define-fun formal_0_9 () FormalMachine (FormalCallback formal_0_8 boundary_0 (select (m_origin formal_0_8) 31) (select (m_origin formal_0_8) 32)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[55]:parent-child
(assert (not (m_panicked formal_0_9)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_9) (select (m_origin formal_0_9) 15) (select (m_origin formal_0_9) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_9) (select (m_origin formal_0_9) 15) (select (m_origin formal_0_9) 32)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[55]:parent-child
(define-fun formal_0_10 () FormalMachine (FormalCallback formal_0_9 boundary_0 (select (m_origin formal_0_9) 15) (select (m_origin formal_0_9) 32)))
; source swap phase=quicksort:imbalance-fallback:sift-down[55]:swap
(define-fun formal_0_11 () FormalMachine (FormalSwap formal_0_10 15 32))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[54]:choose-greater-child
(assert (not (m_panicked formal_0_11)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_11) (select (m_origin formal_0_11) 29) (select (m_origin formal_0_11) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_11) (select (m_origin formal_0_11) 29) (select (m_origin formal_0_11) 30)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[54]:choose-greater-child
(define-fun formal_0_12 () FormalMachine (FormalCallback formal_0_11 boundary_0 (select (m_origin formal_0_11) 29) (select (m_origin formal_0_11) 30)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[54]:parent-child
(assert (not (m_panicked formal_0_12)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_12) (select (m_origin formal_0_12) 14) (select (m_origin formal_0_12) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_12) (select (m_origin formal_0_12) 14) (select (m_origin formal_0_12) 30)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[54]:parent-child
(define-fun formal_0_13 () FormalMachine (FormalCallback formal_0_12 boundary_0 (select (m_origin formal_0_12) 14) (select (m_origin formal_0_12) 30)))
; source swap phase=quicksort:imbalance-fallback:sift-down[54]:swap
(define-fun formal_0_14 () FormalMachine (FormalSwap formal_0_13 14 30))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[53]:choose-greater-child
(assert (not (m_panicked formal_0_14)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_14) (select (m_origin formal_0_14) 27) (select (m_origin formal_0_14) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_14) (select (m_origin formal_0_14) 27) (select (m_origin formal_0_14) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[53]:choose-greater-child
(define-fun formal_0_15 () FormalMachine (FormalCallback formal_0_14 boundary_0 (select (m_origin formal_0_14) 27) (select (m_origin formal_0_14) 28)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[53]:parent-child
(assert (not (m_panicked formal_0_15)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_15) (select (m_origin formal_0_15) 13) (select (m_origin formal_0_15) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_15) (select (m_origin formal_0_15) 13) (select (m_origin formal_0_15) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[53]:parent-child
(define-fun formal_0_16 () FormalMachine (FormalCallback formal_0_15 boundary_0 (select (m_origin formal_0_15) 13) (select (m_origin formal_0_15) 28)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[52]:choose-greater-child
(assert (not (m_panicked formal_0_16)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_16) (select (m_origin formal_0_16) 25) (select (m_origin formal_0_16) 26)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_16) (select (m_origin formal_0_16) 25) (select (m_origin formal_0_16) 26)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[52]:choose-greater-child
(define-fun formal_0_17 () FormalMachine (FormalCallback formal_0_16 boundary_0 (select (m_origin formal_0_16) 25) (select (m_origin formal_0_16) 26)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[52]:parent-child
(assert (not (m_panicked formal_0_17)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_17) (select (m_origin formal_0_17) 12) (select (m_origin formal_0_17) 25)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_17) (select (m_origin formal_0_17) 12) (select (m_origin formal_0_17) 25)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[52]:parent-child
(define-fun formal_0_18 () FormalMachine (FormalCallback formal_0_17 boundary_0 (select (m_origin formal_0_17) 12) (select (m_origin formal_0_17) 25)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[51]:choose-greater-child
(assert (not (m_panicked formal_0_18)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_18) (select (m_origin formal_0_18) 23) (select (m_origin formal_0_18) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_18) (select (m_origin formal_0_18) 23) (select (m_origin formal_0_18) 24)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[51]:choose-greater-child
(define-fun formal_0_19 () FormalMachine (FormalCallback formal_0_18 boundary_0 (select (m_origin formal_0_18) 23) (select (m_origin formal_0_18) 24)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[51]:parent-child
(assert (not (m_panicked formal_0_19)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_19) (select (m_origin formal_0_19) 11) (select (m_origin formal_0_19) 24)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_19) (select (m_origin formal_0_19) 11) (select (m_origin formal_0_19) 24)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[51]:parent-child
(define-fun formal_0_20 () FormalMachine (FormalCallback formal_0_19 boundary_0 (select (m_origin formal_0_19) 11) (select (m_origin formal_0_19) 24)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[50]:choose-greater-child
(assert (not (m_panicked formal_0_20)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 21) (select (m_origin formal_0_20) 22)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 21) (select (m_origin formal_0_20) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[50]:choose-greater-child
(define-fun formal_0_21 () FormalMachine (FormalCallback formal_0_20 boundary_0 (select (m_origin formal_0_20) 21) (select (m_origin formal_0_20) 22)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[50]:parent-child
(assert (not (m_panicked formal_0_21)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_21) (select (m_origin formal_0_21) 10) (select (m_origin formal_0_21) 21)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_21) (select (m_origin formal_0_21) 10) (select (m_origin formal_0_21) 21)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[50]:parent-child
(define-fun formal_0_22 () FormalMachine (FormalCallback formal_0_21 boundary_0 (select (m_origin formal_0_21) 10) (select (m_origin formal_0_21) 21)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[49]:choose-greater-child
(assert (not (m_panicked formal_0_22)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_22) (select (m_origin formal_0_22) 19) (select (m_origin formal_0_22) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_22) (select (m_origin formal_0_22) 19) (select (m_origin formal_0_22) 20)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[49]:choose-greater-child
(define-fun formal_0_23 () FormalMachine (FormalCallback formal_0_22 boundary_0 (select (m_origin formal_0_22) 19) (select (m_origin formal_0_22) 20)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[49]:parent-child
(assert (not (m_panicked formal_0_23)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_23) (select (m_origin formal_0_23) 9) (select (m_origin formal_0_23) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_23) (select (m_origin formal_0_23) 9) (select (m_origin formal_0_23) 19)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[49]:parent-child
(define-fun formal_0_24 () FormalMachine (FormalCallback formal_0_23 boundary_0 (select (m_origin formal_0_23) 9) (select (m_origin formal_0_23) 19)))
; source swap phase=quicksort:imbalance-fallback:sift-down[49]:swap
(define-fun formal_0_25 () FormalMachine (FormalSwap formal_0_24 9 19))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[49]:parent-child
(assert (not (m_panicked formal_0_25)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 9) (select (m_origin formal_0_25) 39)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 9) (select (m_origin formal_0_25) 39)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[49]:parent-child
(define-fun formal_0_26 () FormalMachine (FormalCallback formal_0_25 boundary_0 (select (m_origin formal_0_25) 9) (select (m_origin formal_0_25) 39)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[48]:choose-greater-child
(assert (not (m_panicked formal_0_26)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_26) (select (m_origin formal_0_26) 36) (select (m_origin formal_0_26) 18)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_26) (select (m_origin formal_0_26) 36) (select (m_origin formal_0_26) 18)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[48]:choose-greater-child
(define-fun formal_0_27 () FormalMachine (FormalCallback formal_0_26 boundary_0 (select (m_origin formal_0_26) 36) (select (m_origin formal_0_26) 18)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[48]:parent-child
(assert (not (m_panicked formal_0_27)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_27) (select (m_origin formal_0_27) 8) (select (m_origin formal_0_27) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_27) (select (m_origin formal_0_27) 8) (select (m_origin formal_0_27) 36)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[48]:parent-child
(define-fun formal_0_28 () FormalMachine (FormalCallback formal_0_27 boundary_0 (select (m_origin formal_0_27) 8) (select (m_origin formal_0_27) 36)))
; source swap phase=quicksort:imbalance-fallback:sift-down[48]:swap
(define-fun formal_0_29 () FormalMachine (FormalSwap formal_0_28 8 17))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[48]:choose-greater-child
(assert (not (m_panicked formal_0_29)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_29) (select (m_origin formal_0_29) 35) (select (m_origin formal_0_29) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_29) (select (m_origin formal_0_29) 35) (select (m_origin formal_0_29) 17)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[48]:choose-greater-child
(define-fun formal_0_30 () FormalMachine (FormalCallback formal_0_29 boundary_0 (select (m_origin formal_0_29) 35) (select (m_origin formal_0_29) 17)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[48]:parent-child
(assert (not (m_panicked formal_0_30)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_30) (select (m_origin formal_0_30) 8) (select (m_origin formal_0_30) 17)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_30) (select (m_origin formal_0_30) 8) (select (m_origin formal_0_30) 17)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[48]:parent-child
(define-fun formal_0_31 () FormalMachine (FormalCallback formal_0_30 boundary_0 (select (m_origin formal_0_30) 8) (select (m_origin formal_0_30) 17)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[47]:choose-greater-child
(assert (not (m_panicked formal_0_31)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_31) (select (m_origin formal_0_31) 32) (select (m_origin formal_0_31) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_31) (select (m_origin formal_0_31) 32) (select (m_origin formal_0_31) 16)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[47]:choose-greater-child
(define-fun formal_0_32 () FormalMachine (FormalCallback formal_0_31 boundary_0 (select (m_origin formal_0_31) 32) (select (m_origin formal_0_31) 16)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[47]:parent-child
(assert (not (m_panicked formal_0_32)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_32) (select (m_origin formal_0_32) 7) (select (m_origin formal_0_32) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_32) (select (m_origin formal_0_32) 7) (select (m_origin formal_0_32) 32)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[47]:parent-child
(define-fun formal_0_33 () FormalMachine (FormalCallback formal_0_32 boundary_0 (select (m_origin formal_0_32) 7) (select (m_origin formal_0_32) 32)))
; source swap phase=quicksort:imbalance-fallback:sift-down[47]:swap
(define-fun formal_0_34 () FormalMachine (FormalSwap formal_0_33 7 15))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[47]:choose-greater-child
(assert (not (m_panicked formal_0_34)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_34) (select (m_origin formal_0_34) 31) (select (m_origin formal_0_34) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_34) (select (m_origin formal_0_34) 31) (select (m_origin formal_0_34) 15)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[47]:choose-greater-child
(define-fun formal_0_35 () FormalMachine (FormalCallback formal_0_34 boundary_0 (select (m_origin formal_0_34) 31) (select (m_origin formal_0_34) 15)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[47]:parent-child
(assert (not (m_panicked formal_0_35)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_35) (select (m_origin formal_0_35) 7) (select (m_origin formal_0_35) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_35) (select (m_origin formal_0_35) 7) (select (m_origin formal_0_35) 15)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[47]:parent-child
(define-fun formal_0_36 () FormalMachine (FormalCallback formal_0_35 boundary_0 (select (m_origin formal_0_35) 7) (select (m_origin formal_0_35) 15)))
; source swap phase=quicksort:imbalance-fallback:sift-down[47]:swap
(define-fun formal_0_37 () FormalMachine (FormalSwap formal_0_36 15 32))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[46]:choose-greater-child
(assert (not (m_panicked formal_0_37)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_37) (select (m_origin formal_0_37) 13) (select (m_origin formal_0_37) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_37) (select (m_origin formal_0_37) 13) (select (m_origin formal_0_37) 30)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[46]:choose-greater-child
(define-fun formal_0_38 () FormalMachine (FormalCallback formal_0_37 boundary_0 (select (m_origin formal_0_37) 13) (select (m_origin formal_0_37) 30)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[46]:parent-child
(assert (not (m_panicked formal_0_38)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 6) (select (m_origin formal_0_38) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 6) (select (m_origin formal_0_38) 30)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[46]:parent-child
(define-fun formal_0_39 () FormalMachine (FormalCallback formal_0_38 boundary_0 (select (m_origin formal_0_38) 6) (select (m_origin formal_0_38) 30)))
; source swap phase=quicksort:imbalance-fallback:sift-down[46]:swap
(define-fun formal_0_40 () FormalMachine (FormalSwap formal_0_39 6 14))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[46]:choose-greater-child
(assert (not (m_panicked formal_0_40)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_40) (select (m_origin formal_0_40) 29) (select (m_origin formal_0_40) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_40) (select (m_origin formal_0_40) 29) (select (m_origin formal_0_40) 14)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[46]:choose-greater-child
(define-fun formal_0_41 () FormalMachine (FormalCallback formal_0_40 boundary_0 (select (m_origin formal_0_40) 29) (select (m_origin formal_0_40) 14)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[46]:parent-child
(assert (not (m_panicked formal_0_41)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 6) (select (m_origin formal_0_41) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 6) (select (m_origin formal_0_41) 14)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[46]:parent-child
(define-fun formal_0_42 () FormalMachine (FormalCallback formal_0_41 boundary_0 (select (m_origin formal_0_41) 6) (select (m_origin formal_0_41) 14)))
; source swap phase=quicksort:imbalance-fallback:sift-down[46]:swap
(define-fun formal_0_43 () FormalMachine (FormalSwap formal_0_42 14 30))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[45]:choose-greater-child
(assert (not (m_panicked formal_0_43)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_43) (select (m_origin formal_0_43) 11) (select (m_origin formal_0_43) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_43) (select (m_origin formal_0_43) 11) (select (m_origin formal_0_43) 12)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[45]:choose-greater-child
(define-fun formal_0_44 () FormalMachine (FormalCallback formal_0_43 boundary_0 (select (m_origin formal_0_43) 11) (select (m_origin formal_0_43) 12)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[45]:parent-child
(assert (not (m_panicked formal_0_44)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 5) (select (m_origin formal_0_44) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 5) (select (m_origin formal_0_44) 11)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[45]:parent-child
(define-fun formal_0_45 () FormalMachine (FormalCallback formal_0_44 boundary_0 (select (m_origin formal_0_44) 5) (select (m_origin formal_0_44) 11)))
; source swap phase=quicksort:imbalance-fallback:sift-down[45]:swap
(define-fun formal_0_46 () FormalMachine (FormalSwap formal_0_45 5 11))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[45]:choose-greater-child
(assert (not (m_panicked formal_0_46)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_46) (select (m_origin formal_0_46) 23) (select (m_origin formal_0_46) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_46) (select (m_origin formal_0_46) 23) (select (m_origin formal_0_46) 24)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[45]:choose-greater-child
(define-fun formal_0_47 () FormalMachine (FormalCallback formal_0_46 boundary_0 (select (m_origin formal_0_46) 23) (select (m_origin formal_0_46) 24)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[45]:parent-child
(assert (not (m_panicked formal_0_47)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_47) (select (m_origin formal_0_47) 5) (select (m_origin formal_0_47) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_47) (select (m_origin formal_0_47) 5) (select (m_origin formal_0_47) 24)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[45]:parent-child
(define-fun formal_0_48 () FormalMachine (FormalCallback formal_0_47 boundary_0 (select (m_origin formal_0_47) 5) (select (m_origin formal_0_47) 24)))
; source swap phase=quicksort:imbalance-fallback:sift-down[45]:swap
(define-fun formal_0_49 () FormalMachine (FormalSwap formal_0_48 11 24))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[44]:choose-greater-child
(assert (not (m_panicked formal_0_49)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_49) (select (m_origin formal_0_49) 19) (select (m_origin formal_0_49) 10)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_49) (select (m_origin formal_0_49) 19) (select (m_origin formal_0_49) 10)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[44]:choose-greater-child
(define-fun formal_0_50 () FormalMachine (FormalCallback formal_0_49 boundary_0 (select (m_origin formal_0_49) 19) (select (m_origin formal_0_49) 10)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[44]:parent-child
(assert (not (m_panicked formal_0_50)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_50) (select (m_origin formal_0_50) 4) (select (m_origin formal_0_50) 19)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_50) (select (m_origin formal_0_50) 4) (select (m_origin formal_0_50) 19)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[44]:parent-child
(define-fun formal_0_51 () FormalMachine (FormalCallback formal_0_50 boundary_0 (select (m_origin formal_0_50) 4) (select (m_origin formal_0_50) 19)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[43]:choose-greater-child
(assert (not (m_panicked formal_0_51)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_51) (select (m_origin formal_0_51) 32) (select (m_origin formal_0_51) 36)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_51) (select (m_origin formal_0_51) 32) (select (m_origin formal_0_51) 36)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[43]:choose-greater-child
(define-fun formal_0_52 () FormalMachine (FormalCallback formal_0_51 boundary_0 (select (m_origin formal_0_51) 32) (select (m_origin formal_0_51) 36)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[43]:parent-child
(assert (not (m_panicked formal_0_52)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_52) (select (m_origin formal_0_52) 3) (select (m_origin formal_0_52) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_52) (select (m_origin formal_0_52) 3) (select (m_origin formal_0_52) 32)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[43]:parent-child
(define-fun formal_0_53 () FormalMachine (FormalCallback formal_0_52 boundary_0 (select (m_origin formal_0_52) 3) (select (m_origin formal_0_52) 32)))
; source swap phase=quicksort:imbalance-fallback:sift-down[43]:swap
(define-fun formal_0_54 () FormalMachine (FormalSwap formal_0_53 3 7))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[43]:choose-greater-child
(assert (not (m_panicked formal_0_54)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_54) (select (m_origin formal_0_54) 15) (select (m_origin formal_0_54) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_54) (select (m_origin formal_0_54) 15) (select (m_origin formal_0_54) 16)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[43]:choose-greater-child
(define-fun formal_0_55 () FormalMachine (FormalCallback formal_0_54 boundary_0 (select (m_origin formal_0_54) 15) (select (m_origin formal_0_54) 16)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[43]:parent-child
(assert (not (m_panicked formal_0_55)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_55) (select (m_origin formal_0_55) 3) (select (m_origin formal_0_55) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_55) (select (m_origin formal_0_55) 3) (select (m_origin formal_0_55) 16)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[43]:parent-child
(define-fun formal_0_56 () FormalMachine (FormalCallback formal_0_55 boundary_0 (select (m_origin formal_0_55) 3) (select (m_origin formal_0_55) 16)))
; source swap phase=quicksort:imbalance-fallback:sift-down[43]:swap
(define-fun formal_0_57 () FormalMachine (FormalSwap formal_0_56 7 16))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[43]:choose-greater-child
(assert (not (m_panicked formal_0_57)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_57) (select (m_origin formal_0_57) 33) (select (m_origin formal_0_57) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_57) (select (m_origin formal_0_57) 33) (select (m_origin formal_0_57) 34)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[43]:choose-greater-child
(define-fun formal_0_58 () FormalMachine (FormalCallback formal_0_57 boundary_0 (select (m_origin formal_0_57) 33) (select (m_origin formal_0_57) 34)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[43]:parent-child
(assert (not (m_panicked formal_0_58)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_58) (select (m_origin formal_0_58) 3) (select (m_origin formal_0_58) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_58) (select (m_origin formal_0_58) 3) (select (m_origin formal_0_58) 34)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[43]:parent-child
(define-fun formal_0_59 () FormalMachine (FormalCallback formal_0_58 boundary_0 (select (m_origin formal_0_58) 3) (select (m_origin formal_0_58) 34)))
; source swap phase=quicksort:imbalance-fallback:sift-down[43]:swap
(define-fun formal_0_60 () FormalMachine (FormalSwap formal_0_59 16 34))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[42]:choose-greater-child
(assert (not (m_panicked formal_0_60)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_60) (select (m_origin formal_0_60) 11) (select (m_origin formal_0_60) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_60) (select (m_origin formal_0_60) 11) (select (m_origin formal_0_60) 30)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[42]:choose-greater-child
(define-fun formal_0_61 () FormalMachine (FormalCallback formal_0_60 boundary_0 (select (m_origin formal_0_60) 11) (select (m_origin formal_0_60) 30)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[42]:parent-child
(assert (not (m_panicked formal_0_61)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_61) (select (m_origin formal_0_61) 2) (select (m_origin formal_0_61) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_61) (select (m_origin formal_0_61) 2) (select (m_origin formal_0_61) 30)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[42]:parent-child
(define-fun formal_0_62 () FormalMachine (FormalCallback formal_0_61 boundary_0 (select (m_origin formal_0_61) 2) (select (m_origin formal_0_61) 30)))
; source swap phase=quicksort:imbalance-fallback:sift-down[42]:swap
(define-fun formal_0_63 () FormalMachine (FormalSwap formal_0_62 2 6))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[42]:choose-greater-child
(assert (not (m_panicked formal_0_63)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_63) (select (m_origin formal_0_63) 13) (select (m_origin formal_0_63) 14)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_63) (select (m_origin formal_0_63) 13) (select (m_origin formal_0_63) 14)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[42]:choose-greater-child
(define-fun formal_0_64 () FormalMachine (FormalCallback formal_0_63 boundary_0 (select (m_origin formal_0_63) 13) (select (m_origin formal_0_63) 14)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[42]:parent-child
(assert (not (m_panicked formal_0_64)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_64) (select (m_origin formal_0_64) 2) (select (m_origin formal_0_64) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_64) (select (m_origin formal_0_64) 2) (select (m_origin formal_0_64) 13)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[42]:parent-child
(define-fun formal_0_65 () FormalMachine (FormalCallback formal_0_64 boundary_0 (select (m_origin formal_0_64) 2) (select (m_origin formal_0_64) 13)))
; source swap phase=quicksort:imbalance-fallback:sift-down[42]:swap
(define-fun formal_0_66 () FormalMachine (FormalSwap formal_0_65 6 13))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[42]:choose-greater-child
(assert (not (m_panicked formal_0_66)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_66) (select (m_origin formal_0_66) 27) (select (m_origin formal_0_66) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_66) (select (m_origin formal_0_66) 27) (select (m_origin formal_0_66) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[42]:choose-greater-child
(define-fun formal_0_67 () FormalMachine (FormalCallback formal_0_66 boundary_0 (select (m_origin formal_0_66) 27) (select (m_origin formal_0_66) 28)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[42]:parent-child
(assert (not (m_panicked formal_0_67)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_67) (select (m_origin formal_0_67) 2) (select (m_origin formal_0_67) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_67) (select (m_origin formal_0_67) 2) (select (m_origin formal_0_67) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[42]:parent-child
(define-fun formal_0_68 () FormalMachine (FormalCallback formal_0_67 boundary_0 (select (m_origin formal_0_67) 2) (select (m_origin formal_0_67) 28)))
; source swap phase=quicksort:imbalance-fallback:sift-down[42]:swap
(define-fun formal_0_69 () FormalMachine (FormalSwap formal_0_68 13 28))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[41]:choose-greater-child
(assert (not (m_panicked formal_0_69)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 32) (select (m_origin formal_0_69) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 32) (select (m_origin formal_0_69) 4)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[41]:choose-greater-child
(define-fun formal_0_70 () FormalMachine (FormalCallback formal_0_69 boundary_0 (select (m_origin formal_0_69) 32) (select (m_origin formal_0_69) 4)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[41]:parent-child
(assert (not (m_panicked formal_0_70)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_70) (select (m_origin formal_0_70) 1) (select (m_origin formal_0_70) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_70) (select (m_origin formal_0_70) 1) (select (m_origin formal_0_70) 32)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[41]:parent-child
(define-fun formal_0_71 () FormalMachine (FormalCallback formal_0_70 boundary_0 (select (m_origin formal_0_70) 1) (select (m_origin formal_0_70) 32)))
; source swap phase=quicksort:imbalance-fallback:sift-down[41]:swap
(define-fun formal_0_72 () FormalMachine (FormalSwap formal_0_71 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[41]:choose-greater-child
(assert (not (m_panicked formal_0_72)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_72) (select (m_origin formal_0_72) 16) (select (m_origin formal_0_72) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_72) (select (m_origin formal_0_72) 16) (select (m_origin formal_0_72) 36)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[41]:choose-greater-child
(define-fun formal_0_73 () FormalMachine (FormalCallback formal_0_72 boundary_0 (select (m_origin formal_0_72) 16) (select (m_origin formal_0_72) 36)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[41]:parent-child
(assert (not (m_panicked formal_0_73)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 1) (select (m_origin formal_0_73) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 1) (select (m_origin formal_0_73) 36)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[41]:parent-child
(define-fun formal_0_74 () FormalMachine (FormalCallback formal_0_73 boundary_0 (select (m_origin formal_0_73) 1) (select (m_origin formal_0_73) 36)))
; source swap phase=quicksort:imbalance-fallback:sift-down[41]:swap
(define-fun formal_0_75 () FormalMachine (FormalSwap formal_0_74 3 8))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[41]:choose-greater-child
(assert (not (m_panicked formal_0_75)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 8) (select (m_origin formal_0_75) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 8) (select (m_origin formal_0_75) 18)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[41]:choose-greater-child
(define-fun formal_0_76 () FormalMachine (FormalCallback formal_0_75 boundary_0 (select (m_origin formal_0_75) 8) (select (m_origin formal_0_75) 18)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[41]:parent-child
(assert (not (m_panicked formal_0_76)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_76) (select (m_origin formal_0_76) 1) (select (m_origin formal_0_76) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_76) (select (m_origin formal_0_76) 1) (select (m_origin formal_0_76) 18)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[41]:parent-child
(define-fun formal_0_77 () FormalMachine (FormalCallback formal_0_76 boundary_0 (select (m_origin formal_0_76) 1) (select (m_origin formal_0_76) 18)))
; source swap phase=quicksort:imbalance-fallback:sift-down[41]:swap
(define-fun formal_0_78 () FormalMachine (FormalSwap formal_0_77 8 18))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[41]:choose-greater-child
(assert (not (m_panicked formal_0_78)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 37) (select (m_origin formal_0_78) 38)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 37) (select (m_origin formal_0_78) 38)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[41]:choose-greater-child
(define-fun formal_0_79 () FormalMachine (FormalCallback formal_0_78 boundary_0 (select (m_origin formal_0_78) 37) (select (m_origin formal_0_78) 38)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[41]:parent-child
(assert (not (m_panicked formal_0_79)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_79) (select (m_origin formal_0_79) 1) (select (m_origin formal_0_79) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_79) (select (m_origin formal_0_79) 1) (select (m_origin formal_0_79) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[41]:parent-child
(define-fun formal_0_80 () FormalMachine (FormalCallback formal_0_79 boundary_0 (select (m_origin formal_0_79) 1) (select (m_origin formal_0_79) 37)))
; source swap phase=quicksort:imbalance-fallback:sift-down[41]:swap
(define-fun formal_0_81 () FormalMachine (FormalSwap formal_0_80 18 37))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[40]:choose-greater-child
(assert (not (m_panicked formal_0_81)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 32) (select (m_origin formal_0_81) 30)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 32) (select (m_origin formal_0_81) 30)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[40]:choose-greater-child
(define-fun formal_0_82 () FormalMachine (FormalCallback formal_0_81 boundary_0 (select (m_origin formal_0_81) 32) (select (m_origin formal_0_81) 30)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[40]:parent-child
(assert (not (m_panicked formal_0_82)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_82) (select (m_origin formal_0_82) 0) (select (m_origin formal_0_82) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_82) (select (m_origin formal_0_82) 0) (select (m_origin formal_0_82) 32)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[40]:parent-child
(define-fun formal_0_83 () FormalMachine (FormalCallback formal_0_82 boundary_0 (select (m_origin formal_0_82) 0) (select (m_origin formal_0_82) 32)))
; source swap phase=quicksort:imbalance-fallback:sift-down[40]:swap
(define-fun formal_0_84 () FormalMachine (FormalSwap formal_0_83 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[40]:choose-greater-child
(assert (not (m_panicked formal_0_84)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_84) (select (m_origin formal_0_84) 36) (select (m_origin formal_0_84) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_84) (select (m_origin formal_0_84) 36) (select (m_origin formal_0_84) 4)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[40]:choose-greater-child
(define-fun formal_0_85 () FormalMachine (FormalCallback formal_0_84 boundary_0 (select (m_origin formal_0_84) 36) (select (m_origin formal_0_84) 4)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[40]:parent-child
(assert (not (m_panicked formal_0_85)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_85) (select (m_origin formal_0_85) 0) (select (m_origin formal_0_85) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_85) (select (m_origin formal_0_85) 0) (select (m_origin formal_0_85) 36)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[40]:parent-child
(define-fun formal_0_86 () FormalMachine (FormalCallback formal_0_85 boundary_0 (select (m_origin formal_0_85) 0) (select (m_origin formal_0_85) 36)))
; source swap phase=quicksort:imbalance-fallback:sift-down[40]:swap
(define-fun formal_0_87 () FormalMachine (FormalSwap formal_0_86 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[40]:choose-greater-child
(assert (not (m_panicked formal_0_87)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_87) (select (m_origin formal_0_87) 16) (select (m_origin formal_0_87) 18)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_87) (select (m_origin formal_0_87) 16) (select (m_origin formal_0_87) 18)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[40]:choose-greater-child
(define-fun formal_0_88 () FormalMachine (FormalCallback formal_0_87 boundary_0 (select (m_origin formal_0_87) 16) (select (m_origin formal_0_87) 18)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[40]:parent-child
(assert (not (m_panicked formal_0_88)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_88) (select (m_origin formal_0_88) 0) (select (m_origin formal_0_88) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_88) (select (m_origin formal_0_88) 0) (select (m_origin formal_0_88) 16)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[40]:parent-child
(define-fun formal_0_89 () FormalMachine (FormalCallback formal_0_88 boundary_0 (select (m_origin formal_0_88) 0) (select (m_origin formal_0_88) 16)))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_90 () FormalMachine (FormalSwap formal_0_89 0 39))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[39]:choose-greater-child
(assert (not (m_panicked formal_0_90)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_90) (select (m_origin formal_0_90) 36) (select (m_origin formal_0_90) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_90) (select (m_origin formal_0_90) 36) (select (m_origin formal_0_90) 30)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[39]:choose-greater-child
(define-fun formal_0_91 () FormalMachine (FormalCallback formal_0_90 boundary_0 (select (m_origin formal_0_90) 36) (select (m_origin formal_0_90) 30)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[39]:parent-child
(assert (not (m_panicked formal_0_91)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_91) (select (m_origin formal_0_91) 39) (select (m_origin formal_0_91) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_91) (select (m_origin formal_0_91) 39) (select (m_origin formal_0_91) 30)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[39]:parent-child
(define-fun formal_0_92 () FormalMachine (FormalCallback formal_0_91 boundary_0 (select (m_origin formal_0_91) 39) (select (m_origin formal_0_91) 30)))
; source swap phase=quicksort:imbalance-fallback:sift-down[39]:swap
(define-fun formal_0_93 () FormalMachine (FormalSwap formal_0_92 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[39]:choose-greater-child
(assert (not (m_panicked formal_0_93)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_93) (select (m_origin formal_0_93) 11) (select (m_origin formal_0_93) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_93) (select (m_origin formal_0_93) 11) (select (m_origin formal_0_93) 13)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[39]:choose-greater-child
(define-fun formal_0_94 () FormalMachine (FormalCallback formal_0_93 boundary_0 (select (m_origin formal_0_93) 11) (select (m_origin formal_0_93) 13)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[39]:parent-child
(assert (not (m_panicked formal_0_94)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_94) (select (m_origin formal_0_94) 39) (select (m_origin formal_0_94) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_94) (select (m_origin formal_0_94) 39) (select (m_origin formal_0_94) 13)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[39]:parent-child
(define-fun formal_0_95 () FormalMachine (FormalCallback formal_0_94 boundary_0 (select (m_origin formal_0_94) 39) (select (m_origin formal_0_94) 13)))
; source swap phase=quicksort:imbalance-fallback:sift-down[39]:swap
(define-fun formal_0_96 () FormalMachine (FormalSwap formal_0_95 2 6))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[39]:choose-greater-child
(assert (not (m_panicked formal_0_96)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_96) (select (m_origin formal_0_96) 28) (select (m_origin formal_0_96) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_96) (select (m_origin formal_0_96) 28) (select (m_origin formal_0_96) 14)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[39]:choose-greater-child
(define-fun formal_0_97 () FormalMachine (FormalCallback formal_0_96 boundary_0 (select (m_origin formal_0_96) 28) (select (m_origin formal_0_96) 14)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[39]:parent-child
(assert (not (m_panicked formal_0_97)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_97) (select (m_origin formal_0_97) 39) (select (m_origin formal_0_97) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_97) (select (m_origin formal_0_97) 39) (select (m_origin formal_0_97) 14)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[39]:parent-child
(define-fun formal_0_98 () FormalMachine (FormalCallback formal_0_97 boundary_0 (select (m_origin formal_0_97) 39) (select (m_origin formal_0_97) 14)))
; source swap phase=quicksort:imbalance-fallback:sift-down[39]:swap
(define-fun formal_0_99 () FormalMachine (FormalSwap formal_0_98 6 14))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[39]:choose-greater-child
(assert (not (m_panicked formal_0_99)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 29) (select (m_origin formal_0_99) 6)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 29) (select (m_origin formal_0_99) 6)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[39]:choose-greater-child
(define-fun formal_0_100 () FormalMachine (FormalCallback formal_0_99 boundary_0 (select (m_origin formal_0_99) 29) (select (m_origin formal_0_99) 6)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[39]:parent-child
(assert (not (m_panicked formal_0_100)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_100) (select (m_origin formal_0_100) 39) (select (m_origin formal_0_100) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_100) (select (m_origin formal_0_100) 39) (select (m_origin formal_0_100) 29)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[39]:parent-child
(define-fun formal_0_101 () FormalMachine (FormalCallback formal_0_100 boundary_0 (select (m_origin formal_0_100) 39) (select (m_origin formal_0_100) 29)))
; source swap phase=quicksort:imbalance-fallback:sift-down[39]:swap
(define-fun formal_0_102 () FormalMachine (FormalSwap formal_0_101 14 29))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_103 () FormalMachine (FormalSwap formal_0_102 0 38))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[38]:choose-greater-child
(assert (not (m_panicked formal_0_103)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_103) (select (m_origin formal_0_103) 36) (select (m_origin formal_0_103) 13)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_103) (select (m_origin formal_0_103) 36) (select (m_origin formal_0_103) 13)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[38]:choose-greater-child
(define-fun formal_0_104 () FormalMachine (FormalCallback formal_0_103 boundary_0 (select (m_origin formal_0_103) 36) (select (m_origin formal_0_103) 13)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[38]:parent-child
(assert (not (m_panicked formal_0_104)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_104) (select (m_origin formal_0_104) 38) (select (m_origin formal_0_104) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_104) (select (m_origin formal_0_104) 38) (select (m_origin formal_0_104) 36)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[38]:parent-child
(define-fun formal_0_105 () FormalMachine (FormalCallback formal_0_104 boundary_0 (select (m_origin formal_0_104) 38) (select (m_origin formal_0_104) 36)))
; source swap phase=quicksort:imbalance-fallback:sift-down[38]:swap
(define-fun formal_0_106 () FormalMachine (FormalSwap formal_0_105 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[38]:choose-greater-child
(assert (not (m_panicked formal_0_106)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_106) (select (m_origin formal_0_106) 0) (select (m_origin formal_0_106) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_106) (select (m_origin formal_0_106) 0) (select (m_origin formal_0_106) 4)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[38]:choose-greater-child
(define-fun formal_0_107 () FormalMachine (FormalCallback formal_0_106 boundary_0 (select (m_origin formal_0_106) 0) (select (m_origin formal_0_106) 4)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[38]:parent-child
(assert (not (m_panicked formal_0_107)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_107) (select (m_origin formal_0_107) 38) (select (m_origin formal_0_107) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_107) (select (m_origin formal_0_107) 38) (select (m_origin formal_0_107) 0)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[38]:parent-child
(define-fun formal_0_108 () FormalMachine (FormalCallback formal_0_107 boundary_0 (select (m_origin formal_0_107) 38) (select (m_origin formal_0_107) 0)))
; source swap phase=quicksort:imbalance-fallback:sift-down[38]:swap
(define-fun formal_0_109 () FormalMachine (FormalSwap formal_0_108 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[38]:choose-greater-child
(assert (not (m_panicked formal_0_109)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_109) (select (m_origin formal_0_109) 16) (select (m_origin formal_0_109) 18)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_109) (select (m_origin formal_0_109) 16) (select (m_origin formal_0_109) 18)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[38]:choose-greater-child
(define-fun formal_0_110 () FormalMachine (FormalCallback formal_0_109 boundary_0 (select (m_origin formal_0_109) 16) (select (m_origin formal_0_109) 18)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[38]:parent-child
(assert (not (m_panicked formal_0_110)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_110) (select (m_origin formal_0_110) 38) (select (m_origin formal_0_110) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_110) (select (m_origin formal_0_110) 38) (select (m_origin formal_0_110) 16)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[38]:parent-child
(define-fun formal_0_111 () FormalMachine (FormalCallback formal_0_110 boundary_0 (select (m_origin formal_0_110) 38) (select (m_origin formal_0_110) 16)))
; source swap phase=quicksort:imbalance-fallback:sift-down[38]:swap
(define-fun formal_0_112 () FormalMachine (FormalSwap formal_0_111 3 7))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[38]:choose-greater-child
(assert (not (m_panicked formal_0_112)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_112) (select (m_origin formal_0_112) 15) (select (m_origin formal_0_112) 34)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_112) (select (m_origin formal_0_112) 15) (select (m_origin formal_0_112) 34)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[38]:choose-greater-child
(define-fun formal_0_113 () FormalMachine (FormalCallback formal_0_112 boundary_0 (select (m_origin formal_0_112) 15) (select (m_origin formal_0_112) 34)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[38]:parent-child
(assert (not (m_panicked formal_0_113)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_113) (select (m_origin formal_0_113) 38) (select (m_origin formal_0_113) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_113) (select (m_origin formal_0_113) 38) (select (m_origin formal_0_113) 15)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[38]:parent-child
(define-fun formal_0_114 () FormalMachine (FormalCallback formal_0_113 boundary_0 (select (m_origin formal_0_113) 38) (select (m_origin formal_0_113) 15)))
; source swap phase=quicksort:imbalance-fallback:sift-down[38]:swap
(define-fun formal_0_115 () FormalMachine (FormalSwap formal_0_114 7 15))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[38]:choose-greater-child
(assert (not (m_panicked formal_0_115)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_115) (select (m_origin formal_0_115) 31) (select (m_origin formal_0_115) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_115) (select (m_origin formal_0_115) 31) (select (m_origin formal_0_115) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[38]:choose-greater-child
(define-fun formal_0_116 () FormalMachine (FormalCallback formal_0_115 boundary_0 (select (m_origin formal_0_115) 31) (select (m_origin formal_0_115) 7)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[38]:parent-child
(assert (not (m_panicked formal_0_116)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_116) (select (m_origin formal_0_116) 38) (select (m_origin formal_0_116) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_116) (select (m_origin formal_0_116) 38) (select (m_origin formal_0_116) 31)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[38]:parent-child
(define-fun formal_0_117 () FormalMachine (FormalCallback formal_0_116 boundary_0 (select (m_origin formal_0_116) 38) (select (m_origin formal_0_116) 31)))
; source swap phase=quicksort:imbalance-fallback:sift-down[38]:swap
(define-fun formal_0_118 () FormalMachine (FormalSwap formal_0_117 15 31))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_119 () FormalMachine (FormalSwap formal_0_118 0 37))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[37]:choose-greater-child
(assert (not (m_panicked formal_0_119)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_119) (select (m_origin formal_0_119) 0) (select (m_origin formal_0_119) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_119) (select (m_origin formal_0_119) 0) (select (m_origin formal_0_119) 13)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[37]:choose-greater-child
(define-fun formal_0_120 () FormalMachine (FormalCallback formal_0_119 boundary_0 (select (m_origin formal_0_119) 0) (select (m_origin formal_0_119) 13)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[37]:parent-child
(assert (not (m_panicked formal_0_120)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_120) (select (m_origin formal_0_120) 1) (select (m_origin formal_0_120) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_120) (select (m_origin formal_0_120) 1) (select (m_origin formal_0_120) 13)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[37]:parent-child
(define-fun formal_0_121 () FormalMachine (FormalCallback formal_0_120 boundary_0 (select (m_origin formal_0_120) 1) (select (m_origin formal_0_120) 13)))
; source swap phase=quicksort:imbalance-fallback:sift-down[37]:swap
(define-fun formal_0_122 () FormalMachine (FormalSwap formal_0_121 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[37]:choose-greater-child
(assert (not (m_panicked formal_0_122)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_122) (select (m_origin formal_0_122) 11) (select (m_origin formal_0_122) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_122) (select (m_origin formal_0_122) 11) (select (m_origin formal_0_122) 14)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[37]:choose-greater-child
(define-fun formal_0_123 () FormalMachine (FormalCallback formal_0_122 boundary_0 (select (m_origin formal_0_122) 11) (select (m_origin formal_0_122) 14)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[37]:parent-child
(assert (not (m_panicked formal_0_123)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_123) (select (m_origin formal_0_123) 1) (select (m_origin formal_0_123) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_123) (select (m_origin formal_0_123) 1) (select (m_origin formal_0_123) 14)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[37]:parent-child
(define-fun formal_0_124 () FormalMachine (FormalCallback formal_0_123 boundary_0 (select (m_origin formal_0_123) 1) (select (m_origin formal_0_123) 14)))
; source swap phase=quicksort:imbalance-fallback:sift-down[37]:swap
(define-fun formal_0_125 () FormalMachine (FormalSwap formal_0_124 2 6))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[37]:choose-greater-child
(assert (not (m_panicked formal_0_125)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_125) (select (m_origin formal_0_125) 28) (select (m_origin formal_0_125) 29)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_125) (select (m_origin formal_0_125) 28) (select (m_origin formal_0_125) 29)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[37]:choose-greater-child
(define-fun formal_0_126 () FormalMachine (FormalCallback formal_0_125 boundary_0 (select (m_origin formal_0_125) 28) (select (m_origin formal_0_125) 29)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[37]:parent-child
(assert (not (m_panicked formal_0_126)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_126) (select (m_origin formal_0_126) 1) (select (m_origin formal_0_126) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_126) (select (m_origin formal_0_126) 1) (select (m_origin formal_0_126) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[37]:parent-child
(define-fun formal_0_127 () FormalMachine (FormalCallback formal_0_126 boundary_0 (select (m_origin formal_0_126) 1) (select (m_origin formal_0_126) 28)))
; source swap phase=quicksort:imbalance-fallback:sift-down[37]:swap
(define-fun formal_0_128 () FormalMachine (FormalSwap formal_0_127 6 13))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[37]:choose-greater-child
(assert (not (m_panicked formal_0_128)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 27) (select (m_origin formal_0_128) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 27) (select (m_origin formal_0_128) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[37]:choose-greater-child
(define-fun formal_0_129 () FormalMachine (FormalCallback formal_0_128 boundary_0 (select (m_origin formal_0_128) 27) (select (m_origin formal_0_128) 2)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[37]:parent-child
(assert (not (m_panicked formal_0_129)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_129) (select (m_origin formal_0_129) 1) (select (m_origin formal_0_129) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_129) (select (m_origin formal_0_129) 1) (select (m_origin formal_0_129) 27)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[37]:parent-child
(define-fun formal_0_130 () FormalMachine (FormalCallback formal_0_129 boundary_0 (select (m_origin formal_0_129) 1) (select (m_origin formal_0_129) 27)))
; source swap phase=quicksort:imbalance-fallback:sift-down[37]:swap
(define-fun formal_0_131 () FormalMachine (FormalSwap formal_0_130 13 27))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_132 () FormalMachine (FormalSwap formal_0_131 0 36))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[36]:choose-greater-child
(assert (not (m_panicked formal_0_132)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_132) (select (m_origin formal_0_132) 0) (select (m_origin formal_0_132) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_132) (select (m_origin formal_0_132) 0) (select (m_origin formal_0_132) 14)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[36]:choose-greater-child
(define-fun formal_0_133 () FormalMachine (FormalCallback formal_0_132 boundary_0 (select (m_origin formal_0_132) 0) (select (m_origin formal_0_132) 14)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[36]:parent-child
(assert (not (m_panicked formal_0_133)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_133) (select (m_origin formal_0_133) 17) (select (m_origin formal_0_133) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_133) (select (m_origin formal_0_133) 17) (select (m_origin formal_0_133) 14)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[36]:parent-child
(define-fun formal_0_134 () FormalMachine (FormalCallback formal_0_133 boundary_0 (select (m_origin formal_0_133) 17) (select (m_origin formal_0_133) 14)))
; source swap phase=quicksort:imbalance-fallback:sift-down[36]:swap
(define-fun formal_0_135 () FormalMachine (FormalSwap formal_0_134 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[36]:choose-greater-child
(assert (not (m_panicked formal_0_135)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_135) (select (m_origin formal_0_135) 11) (select (m_origin formal_0_135) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_135) (select (m_origin formal_0_135) 11) (select (m_origin formal_0_135) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[36]:choose-greater-child
(define-fun formal_0_136 () FormalMachine (FormalCallback formal_0_135 boundary_0 (select (m_origin formal_0_135) 11) (select (m_origin formal_0_135) 28)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[36]:parent-child
(assert (not (m_panicked formal_0_136)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_136) (select (m_origin formal_0_136) 17) (select (m_origin formal_0_136) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_136) (select (m_origin formal_0_136) 17) (select (m_origin formal_0_136) 11)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[36]:parent-child
(define-fun formal_0_137 () FormalMachine (FormalCallback formal_0_136 boundary_0 (select (m_origin formal_0_136) 17) (select (m_origin formal_0_136) 11)))
; source swap phase=quicksort:imbalance-fallback:sift-down[36]:swap
(define-fun formal_0_138 () FormalMachine (FormalSwap formal_0_137 2 5))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[36]:choose-greater-child
(assert (not (m_panicked formal_0_138)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_138) (select (m_origin formal_0_138) 24) (select (m_origin formal_0_138) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_138) (select (m_origin formal_0_138) 24) (select (m_origin formal_0_138) 12)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[36]:choose-greater-child
(define-fun formal_0_139 () FormalMachine (FormalCallback formal_0_138 boundary_0 (select (m_origin formal_0_138) 24) (select (m_origin formal_0_138) 12)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[36]:parent-child
(assert (not (m_panicked formal_0_139)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_139) (select (m_origin formal_0_139) 17) (select (m_origin formal_0_139) 24)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_139) (select (m_origin formal_0_139) 17) (select (m_origin formal_0_139) 24)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[36]:parent-child
(define-fun formal_0_140 () FormalMachine (FormalCallback formal_0_139 boundary_0 (select (m_origin formal_0_139) 17) (select (m_origin formal_0_139) 24)))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_141 () FormalMachine (FormalSwap formal_0_140 0 35))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[35]:choose-greater-child
(assert (not (m_panicked formal_0_141)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_141) (select (m_origin formal_0_141) 0) (select (m_origin formal_0_141) 11)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_141) (select (m_origin formal_0_141) 0) (select (m_origin formal_0_141) 11)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[35]:choose-greater-child
(define-fun formal_0_142 () FormalMachine (FormalCallback formal_0_141 boundary_0 (select (m_origin formal_0_141) 0) (select (m_origin formal_0_141) 11)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[35]:parent-child
(assert (not (m_panicked formal_0_142)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_142) (select (m_origin formal_0_142) 35) (select (m_origin formal_0_142) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_142) (select (m_origin formal_0_142) 35) (select (m_origin formal_0_142) 0)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[35]:parent-child
(define-fun formal_0_143 () FormalMachine (FormalCallback formal_0_142 boundary_0 (select (m_origin formal_0_142) 35) (select (m_origin formal_0_142) 0)))
; source swap phase=quicksort:imbalance-fallback:sift-down[35]:swap
(define-fun formal_0_144 () FormalMachine (FormalSwap formal_0_143 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[35]:choose-greater-child
(assert (not (m_panicked formal_0_144)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_144) (select (m_origin formal_0_144) 16) (select (m_origin formal_0_144) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_144) (select (m_origin formal_0_144) 16) (select (m_origin formal_0_144) 4)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[35]:choose-greater-child
(define-fun formal_0_145 () FormalMachine (FormalCallback formal_0_144 boundary_0 (select (m_origin formal_0_144) 16) (select (m_origin formal_0_144) 4)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[35]:parent-child
(assert (not (m_panicked formal_0_145)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_145) (select (m_origin formal_0_145) 35) (select (m_origin formal_0_145) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_145) (select (m_origin formal_0_145) 35) (select (m_origin formal_0_145) 4)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[35]:parent-child
(define-fun formal_0_146 () FormalMachine (FormalCallback formal_0_145 boundary_0 (select (m_origin formal_0_145) 35) (select (m_origin formal_0_145) 4)))
; source swap phase=quicksort:imbalance-fallback:sift-down[35]:swap
(define-fun formal_0_147 () FormalMachine (FormalSwap formal_0_146 1 4))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[35]:choose-greater-child
(assert (not (m_panicked formal_0_147)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_147) (select (m_origin formal_0_147) 19) (select (m_origin formal_0_147) 10)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_147) (select (m_origin formal_0_147) 19) (select (m_origin formal_0_147) 10)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[35]:choose-greater-child
(define-fun formal_0_148 () FormalMachine (FormalCallback formal_0_147 boundary_0 (select (m_origin formal_0_147) 19) (select (m_origin formal_0_147) 10)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[35]:parent-child
(assert (not (m_panicked formal_0_148)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_148) (select (m_origin formal_0_148) 35) (select (m_origin formal_0_148) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_148) (select (m_origin formal_0_148) 35) (select (m_origin formal_0_148) 19)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[35]:parent-child
(define-fun formal_0_149 () FormalMachine (FormalCallback formal_0_148 boundary_0 (select (m_origin formal_0_148) 35) (select (m_origin formal_0_148) 19)))
; source swap phase=quicksort:imbalance-fallback:sift-down[35]:swap
(define-fun formal_0_150 () FormalMachine (FormalSwap formal_0_149 4 9))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[35]:choose-greater-child
(assert (not (m_panicked formal_0_150)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_150) (select (m_origin formal_0_150) 9) (select (m_origin formal_0_150) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_150) (select (m_origin formal_0_150) 9) (select (m_origin formal_0_150) 20)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[35]:choose-greater-child
(define-fun formal_0_151 () FormalMachine (FormalCallback formal_0_150 boundary_0 (select (m_origin formal_0_150) 9) (select (m_origin formal_0_150) 20)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[35]:parent-child
(assert (not (m_panicked formal_0_151)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_151) (select (m_origin formal_0_151) 35) (select (m_origin formal_0_151) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_151) (select (m_origin formal_0_151) 35) (select (m_origin formal_0_151) 9)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[35]:parent-child
(define-fun formal_0_152 () FormalMachine (FormalCallback formal_0_151 boundary_0 (select (m_origin formal_0_151) 35) (select (m_origin formal_0_151) 9)))
; source swap phase=quicksort:imbalance-fallback:sift-down[35]:swap
(define-fun formal_0_153 () FormalMachine (FormalSwap formal_0_152 9 19))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_154 () FormalMachine (FormalSwap formal_0_153 0 34))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[34]:choose-greater-child
(assert (not (m_panicked formal_0_154)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_154) (select (m_origin formal_0_154) 4) (select (m_origin formal_0_154) 11)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_154) (select (m_origin formal_0_154) 4) (select (m_origin formal_0_154) 11)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[34]:choose-greater-child
(define-fun formal_0_155 () FormalMachine (FormalCallback formal_0_154 boundary_0 (select (m_origin formal_0_154) 4) (select (m_origin formal_0_154) 11)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[34]:parent-child
(assert (not (m_panicked formal_0_155)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 3) (select (m_origin formal_0_155) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 3) (select (m_origin formal_0_155) 4)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[34]:parent-child
(define-fun formal_0_156 () FormalMachine (FormalCallback formal_0_155 boundary_0 (select (m_origin formal_0_155) 3) (select (m_origin formal_0_155) 4)))
; source swap phase=quicksort:imbalance-fallback:sift-down[34]:swap
(define-fun formal_0_157 () FormalMachine (FormalSwap formal_0_156 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[34]:choose-greater-child
(assert (not (m_panicked formal_0_157)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_157) (select (m_origin formal_0_157) 16) (select (m_origin formal_0_157) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_157) (select (m_origin formal_0_157) 16) (select (m_origin formal_0_157) 19)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[34]:choose-greater-child
(define-fun formal_0_158 () FormalMachine (FormalCallback formal_0_157 boundary_0 (select (m_origin formal_0_157) 16) (select (m_origin formal_0_157) 19)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[34]:parent-child
(assert (not (m_panicked formal_0_158)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_158) (select (m_origin formal_0_158) 3) (select (m_origin formal_0_158) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_158) (select (m_origin formal_0_158) 3) (select (m_origin formal_0_158) 19)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[34]:parent-child
(define-fun formal_0_159 () FormalMachine (FormalCallback formal_0_158 boundary_0 (select (m_origin formal_0_158) 3) (select (m_origin formal_0_158) 19)))
; source swap phase=quicksort:imbalance-fallback:sift-down[34]:swap
(define-fun formal_0_160 () FormalMachine (FormalSwap formal_0_159 1 4))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[34]:choose-greater-child
(assert (not (m_panicked formal_0_160)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_160) (select (m_origin formal_0_160) 9) (select (m_origin formal_0_160) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_160) (select (m_origin formal_0_160) 9) (select (m_origin formal_0_160) 10)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[34]:choose-greater-child
(define-fun formal_0_161 () FormalMachine (FormalCallback formal_0_160 boundary_0 (select (m_origin formal_0_160) 9) (select (m_origin formal_0_160) 10)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[34]:parent-child
(assert (not (m_panicked formal_0_161)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_161) (select (m_origin formal_0_161) 3) (select (m_origin formal_0_161) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_161) (select (m_origin formal_0_161) 3) (select (m_origin formal_0_161) 10)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[34]:parent-child
(define-fun formal_0_162 () FormalMachine (FormalCallback formal_0_161 boundary_0 (select (m_origin formal_0_161) 3) (select (m_origin formal_0_161) 10)))
; source swap phase=quicksort:imbalance-fallback:sift-down[34]:swap
(define-fun formal_0_163 () FormalMachine (FormalSwap formal_0_162 4 10))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[34]:choose-greater-child
(assert (not (m_panicked formal_0_163)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_163) (select (m_origin formal_0_163) 21) (select (m_origin formal_0_163) 22)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_163) (select (m_origin formal_0_163) 21) (select (m_origin formal_0_163) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[34]:choose-greater-child
(define-fun formal_0_164 () FormalMachine (FormalCallback formal_0_163 boundary_0 (select (m_origin formal_0_163) 21) (select (m_origin formal_0_163) 22)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[34]:parent-child
(assert (not (m_panicked formal_0_164)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_164) (select (m_origin formal_0_164) 3) (select (m_origin formal_0_164) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_164) (select (m_origin formal_0_164) 3) (select (m_origin formal_0_164) 21)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[34]:parent-child
(define-fun formal_0_165 () FormalMachine (FormalCallback formal_0_164 boundary_0 (select (m_origin formal_0_164) 3) (select (m_origin formal_0_164) 21)))
; source swap phase=quicksort:imbalance-fallback:sift-down[34]:swap
(define-fun formal_0_166 () FormalMachine (FormalSwap formal_0_165 10 21))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_167 () FormalMachine (FormalSwap formal_0_166 0 33))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[33]:choose-greater-child
(assert (not (m_panicked formal_0_167)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_167) (select (m_origin formal_0_167) 19) (select (m_origin formal_0_167) 11)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_167) (select (m_origin formal_0_167) 19) (select (m_origin formal_0_167) 11)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[33]:choose-greater-child
(define-fun formal_0_168 () FormalMachine (FormalCallback formal_0_167 boundary_0 (select (m_origin formal_0_167) 19) (select (m_origin formal_0_167) 11)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[33]:parent-child
(assert (not (m_panicked formal_0_168)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_168) (select (m_origin formal_0_168) 33) (select (m_origin formal_0_168) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_168) (select (m_origin formal_0_168) 33) (select (m_origin formal_0_168) 19)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[33]:parent-child
(define-fun formal_0_169 () FormalMachine (FormalCallback formal_0_168 boundary_0 (select (m_origin formal_0_168) 33) (select (m_origin formal_0_168) 19)))
; source swap phase=quicksort:imbalance-fallback:sift-down[33]:swap
(define-fun formal_0_170 () FormalMachine (FormalSwap formal_0_169 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[33]:choose-greater-child
(assert (not (m_panicked formal_0_170)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_170) (select (m_origin formal_0_170) 16) (select (m_origin formal_0_170) 10)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_170) (select (m_origin formal_0_170) 16) (select (m_origin formal_0_170) 10)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[33]:choose-greater-child
(define-fun formal_0_171 () FormalMachine (FormalCallback formal_0_170 boundary_0 (select (m_origin formal_0_170) 16) (select (m_origin formal_0_170) 10)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[33]:parent-child
(assert (not (m_panicked formal_0_171)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_171) (select (m_origin formal_0_171) 33) (select (m_origin formal_0_171) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_171) (select (m_origin formal_0_171) 33) (select (m_origin formal_0_171) 16)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[33]:parent-child
(define-fun formal_0_172 () FormalMachine (FormalCallback formal_0_171 boundary_0 (select (m_origin formal_0_171) 33) (select (m_origin formal_0_171) 16)))
; source swap phase=quicksort:imbalance-fallback:sift-down[33]:swap
(define-fun formal_0_173 () FormalMachine (FormalSwap formal_0_172 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[33]:choose-greater-child
(assert (not (m_panicked formal_0_173)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_173) (select (m_origin formal_0_173) 15) (select (m_origin formal_0_173) 18)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_173) (select (m_origin formal_0_173) 15) (select (m_origin formal_0_173) 18)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[33]:choose-greater-child
(define-fun formal_0_174 () FormalMachine (FormalCallback formal_0_173 boundary_0 (select (m_origin formal_0_173) 15) (select (m_origin formal_0_173) 18)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[33]:parent-child
(assert (not (m_panicked formal_0_174)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_174) (select (m_origin formal_0_174) 33) (select (m_origin formal_0_174) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_174) (select (m_origin formal_0_174) 33) (select (m_origin formal_0_174) 15)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[33]:parent-child
(define-fun formal_0_175 () FormalMachine (FormalCallback formal_0_174 boundary_0 (select (m_origin formal_0_174) 33) (select (m_origin formal_0_174) 15)))
; source swap phase=quicksort:imbalance-fallback:sift-down[33]:swap
(define-fun formal_0_176 () FormalMachine (FormalSwap formal_0_175 3 7))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[33]:choose-greater-child
(assert (not (m_panicked formal_0_176)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 31) (select (m_origin formal_0_176) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 31) (select (m_origin formal_0_176) 34)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[33]:choose-greater-child
(define-fun formal_0_177 () FormalMachine (FormalCallback formal_0_176 boundary_0 (select (m_origin formal_0_176) 31) (select (m_origin formal_0_176) 34)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[33]:parent-child
(assert (not (m_panicked formal_0_177)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_177) (select (m_origin formal_0_177) 33) (select (m_origin formal_0_177) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_177) (select (m_origin formal_0_177) 33) (select (m_origin formal_0_177) 34)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[33]:parent-child
(define-fun formal_0_178 () FormalMachine (FormalCallback formal_0_177 boundary_0 (select (m_origin formal_0_177) 33) (select (m_origin formal_0_177) 34)))
; source swap phase=quicksort:imbalance-fallback:sift-down[33]:swap
(define-fun formal_0_179 () FormalMachine (FormalSwap formal_0_178 7 16))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_180 () FormalMachine (FormalSwap formal_0_179 0 32))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[32]:choose-greater-child
(assert (not (m_panicked formal_0_180)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_180) (select (m_origin formal_0_180) 16) (select (m_origin formal_0_180) 11)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_180) (select (m_origin formal_0_180) 16) (select (m_origin formal_0_180) 11)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[32]:choose-greater-child
(define-fun formal_0_181 () FormalMachine (FormalCallback formal_0_180 boundary_0 (select (m_origin formal_0_180) 16) (select (m_origin formal_0_180) 11)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[32]:parent-child
(assert (not (m_panicked formal_0_181)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_181) (select (m_origin formal_0_181) 7) (select (m_origin formal_0_181) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_181) (select (m_origin formal_0_181) 7) (select (m_origin formal_0_181) 16)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[32]:parent-child
(define-fun formal_0_182 () FormalMachine (FormalCallback formal_0_181 boundary_0 (select (m_origin formal_0_181) 7) (select (m_origin formal_0_181) 16)))
; source swap phase=quicksort:imbalance-fallback:sift-down[32]:swap
(define-fun formal_0_183 () FormalMachine (FormalSwap formal_0_182 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[32]:choose-greater-child
(assert (not (m_panicked formal_0_183)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_183) (select (m_origin formal_0_183) 15) (select (m_origin formal_0_183) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_183) (select (m_origin formal_0_183) 15) (select (m_origin formal_0_183) 10)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[32]:choose-greater-child
(define-fun formal_0_184 () FormalMachine (FormalCallback formal_0_183 boundary_0 (select (m_origin formal_0_183) 15) (select (m_origin formal_0_183) 10)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[32]:parent-child
(assert (not (m_panicked formal_0_184)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_184) (select (m_origin formal_0_184) 7) (select (m_origin formal_0_184) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_184) (select (m_origin formal_0_184) 7) (select (m_origin formal_0_184) 10)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[32]:parent-child
(define-fun formal_0_185 () FormalMachine (FormalCallback formal_0_184 boundary_0 (select (m_origin formal_0_184) 7) (select (m_origin formal_0_184) 10)))
; source swap phase=quicksort:imbalance-fallback:sift-down[32]:swap
(define-fun formal_0_186 () FormalMachine (FormalSwap formal_0_185 1 4))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[32]:choose-greater-child
(assert (not (m_panicked formal_0_186)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_186) (select (m_origin formal_0_186) 9) (select (m_origin formal_0_186) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_186) (select (m_origin formal_0_186) 9) (select (m_origin formal_0_186) 21)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[32]:choose-greater-child
(define-fun formal_0_187 () FormalMachine (FormalCallback formal_0_186 boundary_0 (select (m_origin formal_0_186) 9) (select (m_origin formal_0_186) 21)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[32]:parent-child
(assert (not (m_panicked formal_0_187)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_187) (select (m_origin formal_0_187) 7) (select (m_origin formal_0_187) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_187) (select (m_origin formal_0_187) 7) (select (m_origin formal_0_187) 21)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[32]:parent-child
(define-fun formal_0_188 () FormalMachine (FormalCallback formal_0_187 boundary_0 (select (m_origin formal_0_187) 7) (select (m_origin formal_0_187) 21)))
; source swap phase=quicksort:imbalance-fallback:sift-down[32]:swap
(define-fun formal_0_189 () FormalMachine (FormalSwap formal_0_188 4 10))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[32]:choose-greater-child
(assert (not (m_panicked formal_0_189)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_189) (select (m_origin formal_0_189) 3) (select (m_origin formal_0_189) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_189) (select (m_origin formal_0_189) 3) (select (m_origin formal_0_189) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[32]:choose-greater-child
(define-fun formal_0_190 () FormalMachine (FormalCallback formal_0_189 boundary_0 (select (m_origin formal_0_189) 3) (select (m_origin formal_0_189) 22)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[32]:parent-child
(assert (not (m_panicked formal_0_190)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_190) (select (m_origin formal_0_190) 7) (select (m_origin formal_0_190) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_190) (select (m_origin formal_0_190) 7) (select (m_origin formal_0_190) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[32]:parent-child
(define-fun formal_0_191 () FormalMachine (FormalCallback formal_0_190 boundary_0 (select (m_origin formal_0_190) 7) (select (m_origin formal_0_190) 22)))
; source swap phase=quicksort:imbalance-fallback:sift-down[32]:swap
(define-fun formal_0_192 () FormalMachine (FormalSwap formal_0_191 10 22))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_193 () FormalMachine (FormalSwap formal_0_192 0 31))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[31]:choose-greater-child
(assert (not (m_panicked formal_0_193)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_193) (select (m_origin formal_0_193) 10) (select (m_origin formal_0_193) 11)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_193) (select (m_origin formal_0_193) 10) (select (m_origin formal_0_193) 11)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[31]:choose-greater-child
(define-fun formal_0_194 () FormalMachine (FormalCallback formal_0_193 boundary_0 (select (m_origin formal_0_193) 10) (select (m_origin formal_0_193) 11)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[31]:parent-child
(assert (not (m_panicked formal_0_194)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_194) (select (m_origin formal_0_194) 38) (select (m_origin formal_0_194) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_194) (select (m_origin formal_0_194) 38) (select (m_origin formal_0_194) 10)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[31]:parent-child
(define-fun formal_0_195 () FormalMachine (FormalCallback formal_0_194 boundary_0 (select (m_origin formal_0_194) 38) (select (m_origin formal_0_194) 10)))
; source swap phase=quicksort:imbalance-fallback:sift-down[31]:swap
(define-fun formal_0_196 () FormalMachine (FormalSwap formal_0_195 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[31]:choose-greater-child
(assert (not (m_panicked formal_0_196)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_196) (select (m_origin formal_0_196) 15) (select (m_origin formal_0_196) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_196) (select (m_origin formal_0_196) 15) (select (m_origin formal_0_196) 21)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[31]:choose-greater-child
(define-fun formal_0_197 () FormalMachine (FormalCallback formal_0_196 boundary_0 (select (m_origin formal_0_196) 15) (select (m_origin formal_0_196) 21)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[31]:parent-child
(assert (not (m_panicked formal_0_197)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_197) (select (m_origin formal_0_197) 38) (select (m_origin formal_0_197) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_197) (select (m_origin formal_0_197) 38) (select (m_origin formal_0_197) 21)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[31]:parent-child
(define-fun formal_0_198 () FormalMachine (FormalCallback formal_0_197 boundary_0 (select (m_origin formal_0_197) 38) (select (m_origin formal_0_197) 21)))
; source swap phase=quicksort:imbalance-fallback:sift-down[31]:swap
(define-fun formal_0_199 () FormalMachine (FormalSwap formal_0_198 1 4))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[31]:choose-greater-child
(assert (not (m_panicked formal_0_199)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_199) (select (m_origin formal_0_199) 9) (select (m_origin formal_0_199) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_199) (select (m_origin formal_0_199) 9) (select (m_origin formal_0_199) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[31]:choose-greater-child
(define-fun formal_0_200 () FormalMachine (FormalCallback formal_0_199 boundary_0 (select (m_origin formal_0_199) 9) (select (m_origin formal_0_199) 22)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[31]:parent-child
(assert (not (m_panicked formal_0_200)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_200) (select (m_origin formal_0_200) 38) (select (m_origin formal_0_200) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_200) (select (m_origin formal_0_200) 38) (select (m_origin formal_0_200) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[31]:parent-child
(define-fun formal_0_201 () FormalMachine (FormalCallback formal_0_200 boundary_0 (select (m_origin formal_0_200) 38) (select (m_origin formal_0_200) 22)))
; source swap phase=quicksort:imbalance-fallback:sift-down[31]:swap
(define-fun formal_0_202 () FormalMachine (FormalSwap formal_0_201 4 10))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[31]:choose-greater-child
(assert (not (m_panicked formal_0_202)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_202) (select (m_origin formal_0_202) 3) (select (m_origin formal_0_202) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_202) (select (m_origin formal_0_202) 3) (select (m_origin formal_0_202) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[31]:choose-greater-child
(define-fun formal_0_203 () FormalMachine (FormalCallback formal_0_202 boundary_0 (select (m_origin formal_0_202) 3) (select (m_origin formal_0_202) 7)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[31]:parent-child
(assert (not (m_panicked formal_0_203)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_203) (select (m_origin formal_0_203) 38) (select (m_origin formal_0_203) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_203) (select (m_origin formal_0_203) 38) (select (m_origin formal_0_203) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[31]:parent-child
(define-fun formal_0_204 () FormalMachine (FormalCallback formal_0_203 boundary_0 (select (m_origin formal_0_203) 38) (select (m_origin formal_0_203) 7)))
; source swap phase=quicksort:imbalance-fallback:sift-down[31]:swap
(define-fun formal_0_205 () FormalMachine (FormalSwap formal_0_204 10 22))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_206 () FormalMachine (FormalSwap formal_0_205 0 30))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[30]:choose-greater-child
(assert (not (m_panicked formal_0_206)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_206) (select (m_origin formal_0_206) 21) (select (m_origin formal_0_206) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_206) (select (m_origin formal_0_206) 21) (select (m_origin formal_0_206) 11)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[30]:choose-greater-child
(define-fun formal_0_207 () FormalMachine (FormalCallback formal_0_206 boundary_0 (select (m_origin formal_0_206) 21) (select (m_origin formal_0_206) 11)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[30]:parent-child
(assert (not (m_panicked formal_0_207)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_207) (select (m_origin formal_0_207) 6) (select (m_origin formal_0_207) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_207) (select (m_origin formal_0_207) 6) (select (m_origin formal_0_207) 11)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[30]:parent-child
(define-fun formal_0_208 () FormalMachine (FormalCallback formal_0_207 boundary_0 (select (m_origin formal_0_207) 6) (select (m_origin formal_0_207) 11)))
; source swap phase=quicksort:imbalance-fallback:sift-down[30]:swap
(define-fun formal_0_209 () FormalMachine (FormalSwap formal_0_208 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[30]:choose-greater-child
(assert (not (m_panicked formal_0_209)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_209) (select (m_origin formal_0_209) 17) (select (m_origin formal_0_209) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_209) (select (m_origin formal_0_209) 17) (select (m_origin formal_0_209) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[30]:choose-greater-child
(define-fun formal_0_210 () FormalMachine (FormalCallback formal_0_209 boundary_0 (select (m_origin formal_0_209) 17) (select (m_origin formal_0_209) 28)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[30]:parent-child
(assert (not (m_panicked formal_0_210)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_210) (select (m_origin formal_0_210) 6) (select (m_origin formal_0_210) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_210) (select (m_origin formal_0_210) 6) (select (m_origin formal_0_210) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[30]:parent-child
(define-fun formal_0_211 () FormalMachine (FormalCallback formal_0_210 boundary_0 (select (m_origin formal_0_210) 6) (select (m_origin formal_0_210) 28)))
; source swap phase=quicksort:imbalance-fallback:sift-down[30]:swap
(define-fun formal_0_212 () FormalMachine (FormalSwap formal_0_211 2 6))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[30]:choose-greater-child
(assert (not (m_panicked formal_0_212)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_212) (select (m_origin formal_0_212) 27) (select (m_origin formal_0_212) 29)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_212) (select (m_origin formal_0_212) 27) (select (m_origin formal_0_212) 29)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[30]:choose-greater-child
(define-fun formal_0_213 () FormalMachine (FormalCallback formal_0_212 boundary_0 (select (m_origin formal_0_212) 27) (select (m_origin formal_0_212) 29)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[30]:parent-child
(assert (not (m_panicked formal_0_213)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_213) (select (m_origin formal_0_213) 6) (select (m_origin formal_0_213) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_213) (select (m_origin formal_0_213) 6) (select (m_origin formal_0_213) 27)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[30]:parent-child
(define-fun formal_0_214 () FormalMachine (FormalCallback formal_0_213 boundary_0 (select (m_origin formal_0_213) 6) (select (m_origin formal_0_213) 27)))
; source swap phase=quicksort:imbalance-fallback:sift-down[30]:swap
(define-fun formal_0_215 () FormalMachine (FormalSwap formal_0_214 6 13))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[30]:choose-greater-child
(assert (not (m_panicked formal_0_215)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_215) (select (m_origin formal_0_215) 1) (select (m_origin formal_0_215) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_215) (select (m_origin formal_0_215) 1) (select (m_origin formal_0_215) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[30]:choose-greater-child
(define-fun formal_0_216 () FormalMachine (FormalCallback formal_0_215 boundary_0 (select (m_origin formal_0_215) 1) (select (m_origin formal_0_215) 2)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[30]:parent-child
(assert (not (m_panicked formal_0_216)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_216) (select (m_origin formal_0_216) 6) (select (m_origin formal_0_216) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_216) (select (m_origin formal_0_216) 6) (select (m_origin formal_0_216) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[30]:parent-child
(define-fun formal_0_217 () FormalMachine (FormalCallback formal_0_216 boundary_0 (select (m_origin formal_0_216) 6) (select (m_origin formal_0_216) 2)))
; source swap phase=quicksort:imbalance-fallback:sift-down[30]:swap
(define-fun formal_0_218 () FormalMachine (FormalSwap formal_0_217 13 28))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_219 () FormalMachine (FormalSwap formal_0_218 0 29))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[29]:choose-greater-child
(assert (not (m_panicked formal_0_219)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_219) (select (m_origin formal_0_219) 21) (select (m_origin formal_0_219) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_219) (select (m_origin formal_0_219) 21) (select (m_origin formal_0_219) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[29]:choose-greater-child
(define-fun formal_0_220 () FormalMachine (FormalCallback formal_0_219 boundary_0 (select (m_origin formal_0_219) 21) (select (m_origin formal_0_219) 28)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[29]:parent-child
(assert (not (m_panicked formal_0_220)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_220) (select (m_origin formal_0_220) 39) (select (m_origin formal_0_220) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_220) (select (m_origin formal_0_220) 39) (select (m_origin formal_0_220) 21)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[29]:parent-child
(define-fun formal_0_221 () FormalMachine (FormalCallback formal_0_220 boundary_0 (select (m_origin formal_0_220) 39) (select (m_origin formal_0_220) 21)))
; source swap phase=quicksort:imbalance-fallback:sift-down[29]:swap
(define-fun formal_0_222 () FormalMachine (FormalSwap formal_0_221 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[29]:choose-greater-child
(assert (not (m_panicked formal_0_222)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_222) (select (m_origin formal_0_222) 15) (select (m_origin formal_0_222) 22)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_222) (select (m_origin formal_0_222) 15) (select (m_origin formal_0_222) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[29]:choose-greater-child
(define-fun formal_0_223 () FormalMachine (FormalCallback formal_0_222 boundary_0 (select (m_origin formal_0_222) 15) (select (m_origin formal_0_222) 22)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[29]:parent-child
(assert (not (m_panicked formal_0_223)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_223) (select (m_origin formal_0_223) 39) (select (m_origin formal_0_223) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_223) (select (m_origin formal_0_223) 39) (select (m_origin formal_0_223) 15)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[29]:parent-child
(define-fun formal_0_224 () FormalMachine (FormalCallback formal_0_223 boundary_0 (select (m_origin formal_0_223) 39) (select (m_origin formal_0_223) 15)))
; source swap phase=quicksort:imbalance-fallback:sift-down[29]:swap
(define-fun formal_0_225 () FormalMachine (FormalSwap formal_0_224 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[29]:choose-greater-child
(assert (not (m_panicked formal_0_225)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_225) (select (m_origin formal_0_225) 34) (select (m_origin formal_0_225) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_225) (select (m_origin formal_0_225) 34) (select (m_origin formal_0_225) 18)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[29]:choose-greater-child
(define-fun formal_0_226 () FormalMachine (FormalCallback formal_0_225 boundary_0 (select (m_origin formal_0_225) 34) (select (m_origin formal_0_225) 18)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[29]:parent-child
(assert (not (m_panicked formal_0_226)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_226) (select (m_origin formal_0_226) 39) (select (m_origin formal_0_226) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_226) (select (m_origin formal_0_226) 39) (select (m_origin formal_0_226) 18)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[29]:parent-child
(define-fun formal_0_227 () FormalMachine (FormalCallback formal_0_226 boundary_0 (select (m_origin formal_0_226) 39) (select (m_origin formal_0_226) 18)))
; source swap phase=quicksort:imbalance-fallback:sift-down[29]:swap
(define-fun formal_0_228 () FormalMachine (FormalSwap formal_0_227 3 8))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[29]:choose-greater-child
(assert (not (m_panicked formal_0_228)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_228) (select (m_origin formal_0_228) 8) (select (m_origin formal_0_228) 37)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_228) (select (m_origin formal_0_228) 8) (select (m_origin formal_0_228) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[29]:choose-greater-child
(define-fun formal_0_229 () FormalMachine (FormalCallback formal_0_228 boundary_0 (select (m_origin formal_0_228) 8) (select (m_origin formal_0_228) 37)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[29]:parent-child
(assert (not (m_panicked formal_0_229)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_229) (select (m_origin formal_0_229) 39) (select (m_origin formal_0_229) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_229) (select (m_origin formal_0_229) 39) (select (m_origin formal_0_229) 8)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[29]:parent-child
(define-fun formal_0_230 () FormalMachine (FormalCallback formal_0_229 boundary_0 (select (m_origin formal_0_229) 39) (select (m_origin formal_0_229) 8)))
; source swap phase=quicksort:imbalance-fallback:sift-down[29]:swap
(define-fun formal_0_231 () FormalMachine (FormalSwap formal_0_230 8 17))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_232 () FormalMachine (FormalSwap formal_0_231 0 28))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[28]:choose-greater-child
(assert (not (m_panicked formal_0_232)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_232) (select (m_origin formal_0_232) 15) (select (m_origin formal_0_232) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_232) (select (m_origin formal_0_232) 15) (select (m_origin formal_0_232) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[28]:choose-greater-child
(define-fun formal_0_233 () FormalMachine (FormalCallback formal_0_232 boundary_0 (select (m_origin formal_0_232) 15) (select (m_origin formal_0_232) 28)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[28]:parent-child
(assert (not (m_panicked formal_0_233)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_233) (select (m_origin formal_0_233) 6) (select (m_origin formal_0_233) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_233) (select (m_origin formal_0_233) 6) (select (m_origin formal_0_233) 28)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[28]:parent-child
(define-fun formal_0_234 () FormalMachine (FormalCallback formal_0_233 boundary_0 (select (m_origin formal_0_233) 6) (select (m_origin formal_0_233) 28)))
; source swap phase=quicksort:imbalance-fallback:sift-down[28]:swap
(define-fun formal_0_235 () FormalMachine (FormalSwap formal_0_234 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[28]:choose-greater-child
(assert (not (m_panicked formal_0_235)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_235) (select (m_origin formal_0_235) 17) (select (m_origin formal_0_235) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_235) (select (m_origin formal_0_235) 17) (select (m_origin formal_0_235) 27)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[28]:choose-greater-child
(define-fun formal_0_236 () FormalMachine (FormalCallback formal_0_235 boundary_0 (select (m_origin formal_0_235) 17) (select (m_origin formal_0_235) 27)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[28]:parent-child
(assert (not (m_panicked formal_0_236)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_236) (select (m_origin formal_0_236) 6) (select (m_origin formal_0_236) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_236) (select (m_origin formal_0_236) 6) (select (m_origin formal_0_236) 17)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[28]:parent-child
(define-fun formal_0_237 () FormalMachine (FormalCallback formal_0_236 boundary_0 (select (m_origin formal_0_236) 6) (select (m_origin formal_0_236) 17)))
; source swap phase=quicksort:imbalance-fallback:sift-down[28]:swap
(define-fun formal_0_238 () FormalMachine (FormalSwap formal_0_237 2 5))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[28]:choose-greater-child
(assert (not (m_panicked formal_0_238)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_238) (select (m_origin formal_0_238) 24) (select (m_origin formal_0_238) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_238) (select (m_origin formal_0_238) 24) (select (m_origin formal_0_238) 12)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[28]:choose-greater-child
(define-fun formal_0_239 () FormalMachine (FormalCallback formal_0_238 boundary_0 (select (m_origin formal_0_238) 24) (select (m_origin formal_0_238) 12)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[28]:parent-child
(assert (not (m_panicked formal_0_239)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_239) (select (m_origin formal_0_239) 6) (select (m_origin formal_0_239) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_239) (select (m_origin formal_0_239) 6) (select (m_origin formal_0_239) 24)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[28]:parent-child
(define-fun formal_0_240 () FormalMachine (FormalCallback formal_0_239 boundary_0 (select (m_origin formal_0_239) 6) (select (m_origin formal_0_239) 24)))
; source swap phase=quicksort:imbalance-fallback:sift-down[28]:swap
(define-fun formal_0_241 () FormalMachine (FormalSwap formal_0_240 5 11))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[28]:choose-greater-child
(assert (not (m_panicked formal_0_241)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_241) (select (m_origin formal_0_241) 23) (select (m_origin formal_0_241) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_241) (select (m_origin formal_0_241) 23) (select (m_origin formal_0_241) 5)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[28]:choose-greater-child
(define-fun formal_0_242 () FormalMachine (FormalCallback formal_0_241 boundary_0 (select (m_origin formal_0_241) 23) (select (m_origin formal_0_241) 5)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[28]:parent-child
(assert (not (m_panicked formal_0_242)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_242) (select (m_origin formal_0_242) 6) (select (m_origin formal_0_242) 5)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_242) (select (m_origin formal_0_242) 6) (select (m_origin formal_0_242) 5)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[28]:parent-child
(define-fun formal_0_243 () FormalMachine (FormalCallback formal_0_242 boundary_0 (select (m_origin formal_0_242) 6) (select (m_origin formal_0_242) 5)))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_244 () FormalMachine (FormalSwap formal_0_243 0 27))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[27]:choose-greater-child
(assert (not (m_panicked formal_0_244)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_244) (select (m_origin formal_0_244) 15) (select (m_origin formal_0_244) 17)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_244) (select (m_origin formal_0_244) 15) (select (m_origin formal_0_244) 17)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[27]:choose-greater-child
(define-fun formal_0_245 () FormalMachine (FormalCallback formal_0_244 boundary_0 (select (m_origin formal_0_244) 15) (select (m_origin formal_0_244) 17)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[27]:parent-child
(assert (not (m_panicked formal_0_245)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_245) (select (m_origin formal_0_245) 1) (select (m_origin formal_0_245) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_245) (select (m_origin formal_0_245) 1) (select (m_origin formal_0_245) 15)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[27]:parent-child
(define-fun formal_0_246 () FormalMachine (FormalCallback formal_0_245 boundary_0 (select (m_origin formal_0_245) 1) (select (m_origin formal_0_245) 15)))
; source swap phase=quicksort:imbalance-fallback:sift-down[27]:swap
(define-fun formal_0_247 () FormalMachine (FormalSwap formal_0_246 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[27]:choose-greater-child
(assert (not (m_panicked formal_0_247)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_247) (select (m_origin formal_0_247) 18) (select (m_origin formal_0_247) 22)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_247) (select (m_origin formal_0_247) 18) (select (m_origin formal_0_247) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[27]:choose-greater-child
(define-fun formal_0_248 () FormalMachine (FormalCallback formal_0_247 boundary_0 (select (m_origin formal_0_247) 18) (select (m_origin formal_0_247) 22)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[27]:parent-child
(assert (not (m_panicked formal_0_248)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_248) (select (m_origin formal_0_248) 1) (select (m_origin formal_0_248) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_248) (select (m_origin formal_0_248) 1) (select (m_origin formal_0_248) 18)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[27]:parent-child
(define-fun formal_0_249 () FormalMachine (FormalCallback formal_0_248 boundary_0 (select (m_origin formal_0_248) 1) (select (m_origin formal_0_248) 18)))
; source swap phase=quicksort:imbalance-fallback:sift-down[27]:swap
(define-fun formal_0_250 () FormalMachine (FormalSwap formal_0_249 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[27]:choose-greater-child
(assert (not (m_panicked formal_0_250)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_250) (select (m_origin formal_0_250) 34) (select (m_origin formal_0_250) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_250) (select (m_origin formal_0_250) 34) (select (m_origin formal_0_250) 8)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[27]:choose-greater-child
(define-fun formal_0_251 () FormalMachine (FormalCallback formal_0_250 boundary_0 (select (m_origin formal_0_250) 34) (select (m_origin formal_0_250) 8)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[27]:parent-child
(assert (not (m_panicked formal_0_251)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_251) (select (m_origin formal_0_251) 1) (select (m_origin formal_0_251) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_251) (select (m_origin formal_0_251) 1) (select (m_origin formal_0_251) 8)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[27]:parent-child
(define-fun formal_0_252 () FormalMachine (FormalCallback formal_0_251 boundary_0 (select (m_origin formal_0_251) 1) (select (m_origin formal_0_251) 8)))
; source swap phase=quicksort:imbalance-fallback:sift-down[27]:swap
(define-fun formal_0_253 () FormalMachine (FormalSwap formal_0_252 3 8))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[27]:choose-greater-child
(assert (not (m_panicked formal_0_253)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_253) (select (m_origin formal_0_253) 39) (select (m_origin formal_0_253) 37)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_253) (select (m_origin formal_0_253) 39) (select (m_origin formal_0_253) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[27]:choose-greater-child
(define-fun formal_0_254 () FormalMachine (FormalCallback formal_0_253 boundary_0 (select (m_origin formal_0_253) 39) (select (m_origin formal_0_253) 37)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[27]:parent-child
(assert (not (m_panicked formal_0_254)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_254) (select (m_origin formal_0_254) 1) (select (m_origin formal_0_254) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_254) (select (m_origin formal_0_254) 1) (select (m_origin formal_0_254) 39)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[27]:parent-child
(define-fun formal_0_255 () FormalMachine (FormalCallback formal_0_254 boundary_0 (select (m_origin formal_0_254) 1) (select (m_origin formal_0_254) 39)))
; source swap phase=quicksort:imbalance-fallback:sift-down[27]:swap
(define-fun formal_0_256 () FormalMachine (FormalSwap formal_0_255 8 17))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_257 () FormalMachine (FormalSwap formal_0_256 0 26))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[26]:choose-greater-child
(assert (not (m_panicked formal_0_257)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_257) (select (m_origin formal_0_257) 18) (select (m_origin formal_0_257) 17)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_257) (select (m_origin formal_0_257) 18) (select (m_origin formal_0_257) 17)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[26]:choose-greater-child
(define-fun formal_0_258 () FormalMachine (FormalCallback formal_0_257 boundary_0 (select (m_origin formal_0_257) 18) (select (m_origin formal_0_257) 17)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[26]:parent-child
(assert (not (m_panicked formal_0_258)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_258) (select (m_origin formal_0_258) 26) (select (m_origin formal_0_258) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_258) (select (m_origin formal_0_258) 26) (select (m_origin formal_0_258) 18)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[26]:parent-child
(define-fun formal_0_259 () FormalMachine (FormalCallback formal_0_258 boundary_0 (select (m_origin formal_0_258) 26) (select (m_origin formal_0_258) 18)))
; source swap phase=quicksort:imbalance-fallback:sift-down[26]:swap
(define-fun formal_0_260 () FormalMachine (FormalSwap formal_0_259 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[26]:choose-greater-child
(assert (not (m_panicked formal_0_260)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_260) (select (m_origin formal_0_260) 8) (select (m_origin formal_0_260) 22)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_260) (select (m_origin formal_0_260) 8) (select (m_origin formal_0_260) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[26]:choose-greater-child
(define-fun formal_0_261 () FormalMachine (FormalCallback formal_0_260 boundary_0 (select (m_origin formal_0_260) 8) (select (m_origin formal_0_260) 22)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[26]:parent-child
(assert (not (m_panicked formal_0_261)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_261) (select (m_origin formal_0_261) 26) (select (m_origin formal_0_261) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_261) (select (m_origin formal_0_261) 26) (select (m_origin formal_0_261) 8)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[26]:parent-child
(define-fun formal_0_262 () FormalMachine (FormalCallback formal_0_261 boundary_0 (select (m_origin formal_0_261) 26) (select (m_origin formal_0_261) 8)))
; source swap phase=quicksort:imbalance-fallback:sift-down[26]:swap
(define-fun formal_0_263 () FormalMachine (FormalSwap formal_0_262 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[26]:choose-greater-child
(assert (not (m_panicked formal_0_263)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_263) (select (m_origin formal_0_263) 34) (select (m_origin formal_0_263) 39)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_263) (select (m_origin formal_0_263) 34) (select (m_origin formal_0_263) 39)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[26]:choose-greater-child
(define-fun formal_0_264 () FormalMachine (FormalCallback formal_0_263 boundary_0 (select (m_origin formal_0_263) 34) (select (m_origin formal_0_263) 39)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[26]:parent-child
(assert (not (m_panicked formal_0_264)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_264) (select (m_origin formal_0_264) 26) (select (m_origin formal_0_264) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_264) (select (m_origin formal_0_264) 26) (select (m_origin formal_0_264) 34)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[26]:parent-child
(define-fun formal_0_265 () FormalMachine (FormalCallback formal_0_264 boundary_0 (select (m_origin formal_0_264) 26) (select (m_origin formal_0_264) 34)))
; source swap phase=quicksort:imbalance-fallback:sift-down[26]:swap
(define-fun formal_0_266 () FormalMachine (FormalSwap formal_0_265 3 7))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[26]:choose-greater-child
(assert (not (m_panicked formal_0_266)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_266) (select (m_origin formal_0_266) 31) (select (m_origin formal_0_266) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_266) (select (m_origin formal_0_266) 31) (select (m_origin formal_0_266) 33)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[26]:choose-greater-child
(define-fun formal_0_267 () FormalMachine (FormalCallback formal_0_266 boundary_0 (select (m_origin formal_0_266) 31) (select (m_origin formal_0_266) 33)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[26]:parent-child
(assert (not (m_panicked formal_0_267)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_267) (select (m_origin formal_0_267) 26) (select (m_origin formal_0_267) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_267) (select (m_origin formal_0_267) 26) (select (m_origin formal_0_267) 31)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[26]:parent-child
(define-fun formal_0_268 () FormalMachine (FormalCallback formal_0_267 boundary_0 (select (m_origin formal_0_267) 26) (select (m_origin formal_0_267) 31)))
; source swap phase=quicksort:imbalance-fallback:sift-down[26]:swap
(define-fun formal_0_269 () FormalMachine (FormalSwap formal_0_268 7 15))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_270 () FormalMachine (FormalSwap formal_0_269 0 25))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[25]:choose-greater-child
(assert (not (m_panicked formal_0_270)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_270) (select (m_origin formal_0_270) 8) (select (m_origin formal_0_270) 17)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_270) (select (m_origin formal_0_270) 8) (select (m_origin formal_0_270) 17)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[25]:choose-greater-child
(define-fun formal_0_271 () FormalMachine (FormalCallback formal_0_270 boundary_0 (select (m_origin formal_0_270) 8) (select (m_origin formal_0_270) 17)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[25]:parent-child
(assert (not (m_panicked formal_0_271)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_271) (select (m_origin formal_0_271) 25) (select (m_origin formal_0_271) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_271) (select (m_origin formal_0_271) 25) (select (m_origin formal_0_271) 8)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[25]:parent-child
(define-fun formal_0_272 () FormalMachine (FormalCallback formal_0_271 boundary_0 (select (m_origin formal_0_271) 25) (select (m_origin formal_0_271) 8)))
; source swap phase=quicksort:imbalance-fallback:sift-down[25]:swap
(define-fun formal_0_273 () FormalMachine (FormalSwap formal_0_272 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[25]:choose-greater-child
(assert (not (m_panicked formal_0_273)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_273) (select (m_origin formal_0_273) 34) (select (m_origin formal_0_273) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_273) (select (m_origin formal_0_273) 34) (select (m_origin formal_0_273) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[25]:choose-greater-child
(define-fun formal_0_274 () FormalMachine (FormalCallback formal_0_273 boundary_0 (select (m_origin formal_0_273) 34) (select (m_origin formal_0_273) 22)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[25]:parent-child
(assert (not (m_panicked formal_0_274)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_274) (select (m_origin formal_0_274) 25) (select (m_origin formal_0_274) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_274) (select (m_origin formal_0_274) 25) (select (m_origin formal_0_274) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[25]:parent-child
(define-fun formal_0_275 () FormalMachine (FormalCallback formal_0_274 boundary_0 (select (m_origin formal_0_274) 25) (select (m_origin formal_0_274) 22)))
; source swap phase=quicksort:imbalance-fallback:sift-down[25]:swap
(define-fun formal_0_276 () FormalMachine (FormalSwap formal_0_275 1 4))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[25]:choose-greater-child
(assert (not (m_panicked formal_0_276)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_276) (select (m_origin formal_0_276) 9) (select (m_origin formal_0_276) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_276) (select (m_origin formal_0_276) 9) (select (m_origin formal_0_276) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[25]:choose-greater-child
(define-fun formal_0_277 () FormalMachine (FormalCallback formal_0_276 boundary_0 (select (m_origin formal_0_276) 9) (select (m_origin formal_0_276) 7)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[25]:parent-child
(assert (not (m_panicked formal_0_277)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_277) (select (m_origin formal_0_277) 25) (select (m_origin formal_0_277) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_277) (select (m_origin formal_0_277) 25) (select (m_origin formal_0_277) 9)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[25]:parent-child
(define-fun formal_0_278 () FormalMachine (FormalCallback formal_0_277 boundary_0 (select (m_origin formal_0_277) 25) (select (m_origin formal_0_277) 9)))
; source swap phase=quicksort:imbalance-fallback:sift-down[25]:swap
(define-fun formal_0_279 () FormalMachine (FormalSwap formal_0_278 4 9))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[25]:choose-greater-child
(assert (not (m_panicked formal_0_279)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_279) (select (m_origin formal_0_279) 35) (select (m_origin formal_0_279) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_279) (select (m_origin formal_0_279) 35) (select (m_origin formal_0_279) 20)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[25]:choose-greater-child
(define-fun formal_0_280 () FormalMachine (FormalCallback formal_0_279 boundary_0 (select (m_origin formal_0_279) 35) (select (m_origin formal_0_279) 20)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[25]:parent-child
(assert (not (m_panicked formal_0_280)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_280) (select (m_origin formal_0_280) 25) (select (m_origin formal_0_280) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_280) (select (m_origin formal_0_280) 25) (select (m_origin formal_0_280) 35)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[25]:parent-child
(define-fun formal_0_281 () FormalMachine (FormalCallback formal_0_280 boundary_0 (select (m_origin formal_0_280) 25) (select (m_origin formal_0_280) 35)))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_282 () FormalMachine (FormalSwap formal_0_281 0 24))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[24]:choose-greater-child
(assert (not (m_panicked formal_0_282)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_282) (select (m_origin formal_0_282) 22) (select (m_origin formal_0_282) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_282) (select (m_origin formal_0_282) 22) (select (m_origin formal_0_282) 17)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[24]:choose-greater-child
(define-fun formal_0_283 () FormalMachine (FormalCallback formal_0_282 boundary_0 (select (m_origin formal_0_282) 22) (select (m_origin formal_0_282) 17)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[24]:parent-child
(assert (not (m_panicked formal_0_283)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_283) (select (m_origin formal_0_283) 5) (select (m_origin formal_0_283) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_283) (select (m_origin formal_0_283) 5) (select (m_origin formal_0_283) 17)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[24]:parent-child
(define-fun formal_0_284 () FormalMachine (FormalCallback formal_0_283 boundary_0 (select (m_origin formal_0_283) 5) (select (m_origin formal_0_283) 17)))
; source swap phase=quicksort:imbalance-fallback:sift-down[24]:swap
(define-fun formal_0_285 () FormalMachine (FormalSwap formal_0_284 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[24]:choose-greater-child
(assert (not (m_panicked formal_0_285)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_285) (select (m_origin formal_0_285) 24) (select (m_origin formal_0_285) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_285) (select (m_origin formal_0_285) 24) (select (m_origin formal_0_285) 27)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[24]:choose-greater-child
(define-fun formal_0_286 () FormalMachine (FormalCallback formal_0_285 boundary_0 (select (m_origin formal_0_285) 24) (select (m_origin formal_0_285) 27)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[24]:parent-child
(assert (not (m_panicked formal_0_286)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 5) (select (m_origin formal_0_286) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 5) (select (m_origin formal_0_286) 24)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[24]:parent-child
(define-fun formal_0_287 () FormalMachine (FormalCallback formal_0_286 boundary_0 (select (m_origin formal_0_286) 5) (select (m_origin formal_0_286) 24)))
; source swap phase=quicksort:imbalance-fallback:sift-down[24]:swap
(define-fun formal_0_288 () FormalMachine (FormalSwap formal_0_287 2 5))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[24]:choose-greater-child
(assert (not (m_panicked formal_0_288)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 6) (select (m_origin formal_0_288) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 6) (select (m_origin formal_0_288) 12)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[24]:choose-greater-child
(define-fun formal_0_289 () FormalMachine (FormalCallback formal_0_288 boundary_0 (select (m_origin formal_0_288) 6) (select (m_origin formal_0_288) 12)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[24]:parent-child
(assert (not (m_panicked formal_0_289)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_289) (select (m_origin formal_0_289) 5) (select (m_origin formal_0_289) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_289) (select (m_origin formal_0_289) 5) (select (m_origin formal_0_289) 12)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[24]:parent-child
(define-fun formal_0_290 () FormalMachine (FormalCallback formal_0_289 boundary_0 (select (m_origin formal_0_289) 5) (select (m_origin formal_0_289) 12)))
; source swap phase=quicksort:imbalance-fallback:sift-down[24]:swap
(define-fun formal_0_291 () FormalMachine (FormalSwap formal_0_290 5 12))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_292 () FormalMachine (FormalSwap formal_0_291 0 23))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[23]:choose-greater-child
(assert (not (m_panicked formal_0_292)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 22) (select (m_origin formal_0_292) 24)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 22) (select (m_origin formal_0_292) 24)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[23]:choose-greater-child
(define-fun formal_0_293 () FormalMachine (FormalCallback formal_0_292 boundary_0 (select (m_origin formal_0_292) 22) (select (m_origin formal_0_292) 24)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[23]:parent-child
(assert (not (m_panicked formal_0_293)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_293) (select (m_origin formal_0_293) 23) (select (m_origin formal_0_293) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_293) (select (m_origin formal_0_293) 23) (select (m_origin formal_0_293) 22)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[23]:parent-child
(define-fun formal_0_294 () FormalMachine (FormalCallback formal_0_293 boundary_0 (select (m_origin formal_0_293) 23) (select (m_origin formal_0_293) 22)))
; source swap phase=quicksort:imbalance-fallback:sift-down[23]:swap
(define-fun formal_0_295 () FormalMachine (FormalSwap formal_0_294 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[23]:choose-greater-child
(assert (not (m_panicked formal_0_295)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_295) (select (m_origin formal_0_295) 34) (select (m_origin formal_0_295) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_295) (select (m_origin formal_0_295) 34) (select (m_origin formal_0_295) 9)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[23]:choose-greater-child
(define-fun formal_0_296 () FormalMachine (FormalCallback formal_0_295 boundary_0 (select (m_origin formal_0_295) 34) (select (m_origin formal_0_295) 9)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[23]:parent-child
(assert (not (m_panicked formal_0_296)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_296) (select (m_origin formal_0_296) 23) (select (m_origin formal_0_296) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_296) (select (m_origin formal_0_296) 23) (select (m_origin formal_0_296) 9)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[23]:parent-child
(define-fun formal_0_297 () FormalMachine (FormalCallback formal_0_296 boundary_0 (select (m_origin formal_0_296) 23) (select (m_origin formal_0_296) 9)))
; source swap phase=quicksort:imbalance-fallback:sift-down[23]:swap
(define-fun formal_0_298 () FormalMachine (FormalSwap formal_0_297 1 4))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[23]:choose-greater-child
(assert (not (m_panicked formal_0_298)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_298) (select (m_origin formal_0_298) 25) (select (m_origin formal_0_298) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_298) (select (m_origin formal_0_298) 25) (select (m_origin formal_0_298) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[23]:choose-greater-child
(define-fun formal_0_299 () FormalMachine (FormalCallback formal_0_298 boundary_0 (select (m_origin formal_0_298) 25) (select (m_origin formal_0_298) 7)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[23]:parent-child
(assert (not (m_panicked formal_0_299)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_299) (select (m_origin formal_0_299) 23) (select (m_origin formal_0_299) 25)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_299) (select (m_origin formal_0_299) 23) (select (m_origin formal_0_299) 25)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[23]:parent-child
(define-fun formal_0_300 () FormalMachine (FormalCallback formal_0_299 boundary_0 (select (m_origin formal_0_299) 23) (select (m_origin formal_0_299) 25)))
; source swap phase=quicksort:imbalance-fallback:sift-down[23]:swap
(define-fun formal_0_301 () FormalMachine (FormalSwap formal_0_300 4 9))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[23]:choose-greater-child
(assert (not (m_panicked formal_0_301)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_301) (select (m_origin formal_0_301) 35) (select (m_origin formal_0_301) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_301) (select (m_origin formal_0_301) 35) (select (m_origin formal_0_301) 20)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[23]:choose-greater-child
(define-fun formal_0_302 () FormalMachine (FormalCallback formal_0_301 boundary_0 (select (m_origin formal_0_301) 35) (select (m_origin formal_0_301) 20)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[23]:parent-child
(assert (not (m_panicked formal_0_302)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_302) (select (m_origin formal_0_302) 23) (select (m_origin formal_0_302) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_302) (select (m_origin formal_0_302) 23) (select (m_origin formal_0_302) 35)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[23]:parent-child
(define-fun formal_0_303 () FormalMachine (FormalCallback formal_0_302 boundary_0 (select (m_origin formal_0_302) 23) (select (m_origin formal_0_302) 35)))
; source swap phase=quicksort:imbalance-fallback:sift-down[23]:swap
(define-fun formal_0_304 () FormalMachine (FormalSwap formal_0_303 9 19))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_305 () FormalMachine (FormalSwap formal_0_304 0 22))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[22]:choose-greater-child
(assert (not (m_panicked formal_0_305)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_305) (select (m_origin formal_0_305) 9) (select (m_origin formal_0_305) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_305) (select (m_origin formal_0_305) 9) (select (m_origin formal_0_305) 24)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[22]:choose-greater-child
(define-fun formal_0_306 () FormalMachine (FormalCallback formal_0_305 boundary_0 (select (m_origin formal_0_305) 9) (select (m_origin formal_0_305) 24)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[22]:parent-child
(assert (not (m_panicked formal_0_306)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_306) (select (m_origin formal_0_306) 38) (select (m_origin formal_0_306) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_306) (select (m_origin formal_0_306) 38) (select (m_origin formal_0_306) 24)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[22]:parent-child
(define-fun formal_0_307 () FormalMachine (FormalCallback formal_0_306 boundary_0 (select (m_origin formal_0_306) 38) (select (m_origin formal_0_306) 24)))
; source swap phase=quicksort:imbalance-fallback:sift-down[22]:swap
(define-fun formal_0_308 () FormalMachine (FormalSwap formal_0_307 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[22]:choose-greater-child
(assert (not (m_panicked formal_0_308)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_308) (select (m_origin formal_0_308) 12) (select (m_origin formal_0_308) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_308) (select (m_origin formal_0_308) 12) (select (m_origin formal_0_308) 27)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[22]:choose-greater-child
(define-fun formal_0_309 () FormalMachine (FormalCallback formal_0_308 boundary_0 (select (m_origin formal_0_308) 12) (select (m_origin formal_0_308) 27)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[22]:parent-child
(assert (not (m_panicked formal_0_309)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_309) (select (m_origin formal_0_309) 38) (select (m_origin formal_0_309) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_309) (select (m_origin formal_0_309) 38) (select (m_origin formal_0_309) 27)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[22]:parent-child
(define-fun formal_0_310 () FormalMachine (FormalCallback formal_0_309 boundary_0 (select (m_origin formal_0_309) 38) (select (m_origin formal_0_309) 27)))
; source swap phase=quicksort:imbalance-fallback:sift-down[22]:swap
(define-fun formal_0_311 () FormalMachine (FormalSwap formal_0_310 2 6))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[22]:choose-greater-child
(assert (not (m_panicked formal_0_311)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_311) (select (m_origin formal_0_311) 2) (select (m_origin formal_0_311) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_311) (select (m_origin formal_0_311) 2) (select (m_origin formal_0_311) 29)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[22]:choose-greater-child
(define-fun formal_0_312 () FormalMachine (FormalCallback formal_0_311 boundary_0 (select (m_origin formal_0_311) 2) (select (m_origin formal_0_311) 29)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[22]:parent-child
(assert (not (m_panicked formal_0_312)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_312) (select (m_origin formal_0_312) 38) (select (m_origin formal_0_312) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_312) (select (m_origin formal_0_312) 38) (select (m_origin formal_0_312) 29)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[22]:parent-child
(define-fun formal_0_313 () FormalMachine (FormalCallback formal_0_312 boundary_0 (select (m_origin formal_0_312) 38) (select (m_origin formal_0_312) 29)))
; source swap phase=quicksort:imbalance-fallback:sift-down[22]:swap
(define-fun formal_0_314 () FormalMachine (FormalSwap formal_0_313 6 14))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_315 () FormalMachine (FormalSwap formal_0_314 0 21))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[21]:choose-greater-child
(assert (not (m_panicked formal_0_315)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_315) (select (m_origin formal_0_315) 9) (select (m_origin formal_0_315) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_315) (select (m_origin formal_0_315) 9) (select (m_origin formal_0_315) 27)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[21]:choose-greater-child
(define-fun formal_0_316 () FormalMachine (FormalCallback formal_0_315 boundary_0 (select (m_origin formal_0_315) 9) (select (m_origin formal_0_315) 27)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[21]:parent-child
(assert (not (m_panicked formal_0_316)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_316) (select (m_origin formal_0_316) 3) (select (m_origin formal_0_316) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_316) (select (m_origin formal_0_316) 3) (select (m_origin formal_0_316) 27)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[21]:parent-child
(define-fun formal_0_317 () FormalMachine (FormalCallback formal_0_316 boundary_0 (select (m_origin formal_0_316) 3) (select (m_origin formal_0_316) 27)))
; source swap phase=quicksort:imbalance-fallback:sift-down[21]:swap
(define-fun formal_0_318 () FormalMachine (FormalSwap formal_0_317 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[21]:choose-greater-child
(assert (not (m_panicked formal_0_318)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_318) (select (m_origin formal_0_318) 12) (select (m_origin formal_0_318) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_318) (select (m_origin formal_0_318) 12) (select (m_origin formal_0_318) 29)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[21]:choose-greater-child
(define-fun formal_0_319 () FormalMachine (FormalCallback formal_0_318 boundary_0 (select (m_origin formal_0_318) 12) (select (m_origin formal_0_318) 29)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[21]:parent-child
(assert (not (m_panicked formal_0_319)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_319) (select (m_origin formal_0_319) 3) (select (m_origin formal_0_319) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_319) (select (m_origin formal_0_319) 3) (select (m_origin formal_0_319) 29)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[21]:parent-child
(define-fun formal_0_320 () FormalMachine (FormalCallback formal_0_319 boundary_0 (select (m_origin formal_0_319) 3) (select (m_origin formal_0_319) 29)))
; source swap phase=quicksort:imbalance-fallback:sift-down[21]:swap
(define-fun formal_0_321 () FormalMachine (FormalSwap formal_0_320 2 6))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[21]:choose-greater-child
(assert (not (m_panicked formal_0_321)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_321) (select (m_origin formal_0_321) 2) (select (m_origin formal_0_321) 38)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_321) (select (m_origin formal_0_321) 2) (select (m_origin formal_0_321) 38)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[21]:choose-greater-child
(define-fun formal_0_322 () FormalMachine (FormalCallback formal_0_321 boundary_0 (select (m_origin formal_0_321) 2) (select (m_origin formal_0_321) 38)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[21]:parent-child
(assert (not (m_panicked formal_0_322)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 3) (select (m_origin formal_0_322) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 3) (select (m_origin formal_0_322) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[21]:parent-child
(define-fun formal_0_323 () FormalMachine (FormalCallback formal_0_322 boundary_0 (select (m_origin formal_0_322) 3) (select (m_origin formal_0_322) 2)))
; source swap phase=quicksort:imbalance-fallback:sift-down[21]:swap
(define-fun formal_0_324 () FormalMachine (FormalSwap formal_0_323 6 13))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_325 () FormalMachine (FormalSwap formal_0_324 0 20))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[20]:choose-greater-child
(assert (not (m_panicked formal_0_325)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_325) (select (m_origin formal_0_325) 9) (select (m_origin formal_0_325) 29)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_325) (select (m_origin formal_0_325) 9) (select (m_origin formal_0_325) 29)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[20]:choose-greater-child
(define-fun formal_0_326 () FormalMachine (FormalCallback formal_0_325 boundary_0 (select (m_origin formal_0_325) 9) (select (m_origin formal_0_325) 29)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[20]:parent-child
(assert (not (m_panicked formal_0_326)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_326) (select (m_origin formal_0_326) 20) (select (m_origin formal_0_326) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_326) (select (m_origin formal_0_326) 20) (select (m_origin formal_0_326) 9)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[20]:parent-child
(define-fun formal_0_327 () FormalMachine (FormalCallback formal_0_326 boundary_0 (select (m_origin formal_0_326) 20) (select (m_origin formal_0_326) 9)))
; source swap phase=quicksort:imbalance-fallback:sift-down[20]:swap
(define-fun formal_0_328 () FormalMachine (FormalSwap formal_0_327 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[20]:choose-greater-child
(assert (not (m_panicked formal_0_328)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_328) (select (m_origin formal_0_328) 34) (select (m_origin formal_0_328) 25)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_328) (select (m_origin formal_0_328) 34) (select (m_origin formal_0_328) 25)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[20]:choose-greater-child
(define-fun formal_0_329 () FormalMachine (FormalCallback formal_0_328 boundary_0 (select (m_origin formal_0_328) 34) (select (m_origin formal_0_328) 25)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[20]:parent-child
(assert (not (m_panicked formal_0_329)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_329) (select (m_origin formal_0_329) 20) (select (m_origin formal_0_329) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_329) (select (m_origin formal_0_329) 20) (select (m_origin formal_0_329) 34)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[20]:parent-child
(define-fun formal_0_330 () FormalMachine (FormalCallback formal_0_329 boundary_0 (select (m_origin formal_0_329) 20) (select (m_origin formal_0_329) 34)))
; source swap phase=quicksort:imbalance-fallback:sift-down[20]:swap
(define-fun formal_0_331 () FormalMachine (FormalSwap formal_0_330 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[20]:choose-greater-child
(assert (not (m_panicked formal_0_331)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_331) (select (m_origin formal_0_331) 31) (select (m_origin formal_0_331) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_331) (select (m_origin formal_0_331) 31) (select (m_origin formal_0_331) 39)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[20]:choose-greater-child
(define-fun formal_0_332 () FormalMachine (FormalCallback formal_0_331 boundary_0 (select (m_origin formal_0_331) 31) (select (m_origin formal_0_331) 39)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[20]:parent-child
(assert (not (m_panicked formal_0_332)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_332) (select (m_origin formal_0_332) 20) (select (m_origin formal_0_332) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_332) (select (m_origin formal_0_332) 20) (select (m_origin formal_0_332) 39)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[20]:parent-child
(define-fun formal_0_333 () FormalMachine (FormalCallback formal_0_332 boundary_0 (select (m_origin formal_0_332) 20) (select (m_origin formal_0_332) 39)))
; source swap phase=quicksort:imbalance-fallback:sift-down[20]:swap
(define-fun formal_0_334 () FormalMachine (FormalSwap formal_0_333 3 8))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[20]:choose-greater-child
(assert (not (m_panicked formal_0_334)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_334) (select (m_origin formal_0_334) 1) (select (m_origin formal_0_334) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_334) (select (m_origin formal_0_334) 1) (select (m_origin formal_0_334) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[20]:choose-greater-child
(define-fun formal_0_335 () FormalMachine (FormalCallback formal_0_334 boundary_0 (select (m_origin formal_0_334) 1) (select (m_origin formal_0_334) 37)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[20]:parent-child
(assert (not (m_panicked formal_0_335)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_335) (select (m_origin formal_0_335) 20) (select (m_origin formal_0_335) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_335) (select (m_origin formal_0_335) 20) (select (m_origin formal_0_335) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[20]:parent-child
(define-fun formal_0_336 () FormalMachine (FormalCallback formal_0_335 boundary_0 (select (m_origin formal_0_335) 20) (select (m_origin formal_0_335) 37)))
; source swap phase=quicksort:imbalance-fallback:sift-down[20]:swap
(define-fun formal_0_337 () FormalMachine (FormalSwap formal_0_336 8 18))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_338 () FormalMachine (FormalSwap formal_0_337 0 19))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[19]:choose-greater-child
(assert (not (m_panicked formal_0_338)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_338) (select (m_origin formal_0_338) 34) (select (m_origin formal_0_338) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_338) (select (m_origin formal_0_338) 34) (select (m_origin formal_0_338) 29)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[19]:choose-greater-child
(define-fun formal_0_339 () FormalMachine (FormalCallback formal_0_338 boundary_0 (select (m_origin formal_0_338) 34) (select (m_origin formal_0_338) 29)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[19]:parent-child
(assert (not (m_panicked formal_0_339)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_339) (select (m_origin formal_0_339) 23) (select (m_origin formal_0_339) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_339) (select (m_origin formal_0_339) 23) (select (m_origin formal_0_339) 29)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[19]:parent-child
(define-fun formal_0_340 () FormalMachine (FormalCallback formal_0_339 boundary_0 (select (m_origin formal_0_339) 23) (select (m_origin formal_0_339) 29)))
; source swap phase=quicksort:imbalance-fallback:sift-down[19]:swap
(define-fun formal_0_341 () FormalMachine (FormalSwap formal_0_340 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[19]:choose-greater-child
(assert (not (m_panicked formal_0_341)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_341) (select (m_origin formal_0_341) 12) (select (m_origin formal_0_341) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_341) (select (m_origin formal_0_341) 12) (select (m_origin formal_0_341) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[19]:choose-greater-child
(define-fun formal_0_342 () FormalMachine (FormalCallback formal_0_341 boundary_0 (select (m_origin formal_0_341) 12) (select (m_origin formal_0_341) 2)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[19]:parent-child
(assert (not (m_panicked formal_0_342)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_342) (select (m_origin formal_0_342) 23) (select (m_origin formal_0_342) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_342) (select (m_origin formal_0_342) 23) (select (m_origin formal_0_342) 12)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[19]:parent-child
(define-fun formal_0_343 () FormalMachine (FormalCallback formal_0_342 boundary_0 (select (m_origin formal_0_342) 23) (select (m_origin formal_0_342) 12)))
; source swap phase=quicksort:imbalance-fallback:sift-down[19]:swap
(define-fun formal_0_344 () FormalMachine (FormalSwap formal_0_343 2 5))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[19]:choose-greater-child
(assert (not (m_panicked formal_0_344)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_344) (select (m_origin formal_0_344) 6) (select (m_origin formal_0_344) 5)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_344) (select (m_origin formal_0_344) 6) (select (m_origin formal_0_344) 5)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[19]:choose-greater-child
(define-fun formal_0_345 () FormalMachine (FormalCallback formal_0_344 boundary_0 (select (m_origin formal_0_344) 6) (select (m_origin formal_0_344) 5)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[19]:parent-child
(assert (not (m_panicked formal_0_345)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_345) (select (m_origin formal_0_345) 23) (select (m_origin formal_0_345) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_345) (select (m_origin formal_0_345) 23) (select (m_origin formal_0_345) 6)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[19]:parent-child
(define-fun formal_0_346 () FormalMachine (FormalCallback formal_0_345 boundary_0 (select (m_origin formal_0_345) 23) (select (m_origin formal_0_345) 6)))
; source swap phase=quicksort:imbalance-fallback:sift-down[19]:swap
(define-fun formal_0_347 () FormalMachine (FormalSwap formal_0_346 5 11))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_348 () FormalMachine (FormalSwap formal_0_347 0 18))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[18]:choose-greater-child
(assert (not (m_panicked formal_0_348)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_348) (select (m_origin formal_0_348) 34) (select (m_origin formal_0_348) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_348) (select (m_origin formal_0_348) 34) (select (m_origin formal_0_348) 12)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[18]:choose-greater-child
(define-fun formal_0_349 () FormalMachine (FormalCallback formal_0_348 boundary_0 (select (m_origin formal_0_348) 34) (select (m_origin formal_0_348) 12)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[18]:parent-child
(assert (not (m_panicked formal_0_349)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_349) (select (m_origin formal_0_349) 20) (select (m_origin formal_0_349) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_349) (select (m_origin formal_0_349) 20) (select (m_origin formal_0_349) 34)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[18]:parent-child
(define-fun formal_0_350 () FormalMachine (FormalCallback formal_0_349 boundary_0 (select (m_origin formal_0_349) 20) (select (m_origin formal_0_349) 34)))
; source swap phase=quicksort:imbalance-fallback:sift-down[18]:swap
(define-fun formal_0_351 () FormalMachine (FormalSwap formal_0_350 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[18]:choose-greater-child
(assert (not (m_panicked formal_0_351)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_351) (select (m_origin formal_0_351) 39) (select (m_origin formal_0_351) 25)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_351) (select (m_origin formal_0_351) 39) (select (m_origin formal_0_351) 25)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[18]:choose-greater-child
(define-fun formal_0_352 () FormalMachine (FormalCallback formal_0_351 boundary_0 (select (m_origin formal_0_351) 39) (select (m_origin formal_0_351) 25)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[18]:parent-child
(assert (not (m_panicked formal_0_352)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_352) (select (m_origin formal_0_352) 20) (select (m_origin formal_0_352) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_352) (select (m_origin formal_0_352) 20) (select (m_origin formal_0_352) 39)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[18]:parent-child
(define-fun formal_0_353 () FormalMachine (FormalCallback formal_0_352 boundary_0 (select (m_origin formal_0_352) 20) (select (m_origin formal_0_352) 39)))
; source swap phase=quicksort:imbalance-fallback:sift-down[18]:swap
(define-fun formal_0_354 () FormalMachine (FormalSwap formal_0_353 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[18]:choose-greater-child
(assert (not (m_panicked formal_0_354)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_354) (select (m_origin formal_0_354) 31) (select (m_origin formal_0_354) 37)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_354) (select (m_origin formal_0_354) 31) (select (m_origin formal_0_354) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[18]:choose-greater-child
(define-fun formal_0_355 () FormalMachine (FormalCallback formal_0_354 boundary_0 (select (m_origin formal_0_354) 31) (select (m_origin formal_0_354) 37)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[18]:parent-child
(assert (not (m_panicked formal_0_355)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_355) (select (m_origin formal_0_355) 20) (select (m_origin formal_0_355) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_355) (select (m_origin formal_0_355) 20) (select (m_origin formal_0_355) 31)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[18]:parent-child
(define-fun formal_0_356 () FormalMachine (FormalCallback formal_0_355 boundary_0 (select (m_origin formal_0_355) 20) (select (m_origin formal_0_355) 31)))
; source swap phase=quicksort:imbalance-fallback:sift-down[18]:swap
(define-fun formal_0_357 () FormalMachine (FormalSwap formal_0_356 3 7))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[18]:choose-greater-child
(assert (not (m_panicked formal_0_357)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 26) (select (m_origin formal_0_357) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 26) (select (m_origin formal_0_357) 33)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[18]:choose-greater-child
(define-fun formal_0_358 () FormalMachine (FormalCallback formal_0_357 boundary_0 (select (m_origin formal_0_357) 26) (select (m_origin formal_0_357) 33)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[18]:parent-child
(assert (not (m_panicked formal_0_358)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_358) (select (m_origin formal_0_358) 20) (select (m_origin formal_0_358) 26)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_358) (select (m_origin formal_0_358) 20) (select (m_origin formal_0_358) 26)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[18]:parent-child
(define-fun formal_0_359 () FormalMachine (FormalCallback formal_0_358 boundary_0 (select (m_origin formal_0_358) 20) (select (m_origin formal_0_358) 26)))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_360 () FormalMachine (FormalSwap formal_0_359 0 17))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[17]:choose-greater-child
(assert (not (m_panicked formal_0_360)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_360) (select (m_origin formal_0_360) 39) (select (m_origin formal_0_360) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_360) (select (m_origin formal_0_360) 39) (select (m_origin formal_0_360) 12)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[17]:choose-greater-child
(define-fun formal_0_361 () FormalMachine (FormalCallback formal_0_360 boundary_0 (select (m_origin formal_0_360) 39) (select (m_origin formal_0_360) 12)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[17]:parent-child
(assert (not (m_panicked formal_0_361)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_361) (select (m_origin formal_0_361) 1) (select (m_origin formal_0_361) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_361) (select (m_origin formal_0_361) 1) (select (m_origin formal_0_361) 12)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[17]:parent-child
(define-fun formal_0_362 () FormalMachine (FormalCallback formal_0_361 boundary_0 (select (m_origin formal_0_361) 1) (select (m_origin formal_0_361) 12)))
; source swap phase=quicksort:imbalance-fallback:sift-down[17]:swap
(define-fun formal_0_363 () FormalMachine (FormalSwap formal_0_362 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[17]:choose-greater-child
(assert (not (m_panicked formal_0_363)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_363) (select (m_origin formal_0_363) 6) (select (m_origin formal_0_363) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_363) (select (m_origin formal_0_363) 6) (select (m_origin formal_0_363) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[17]:choose-greater-child
(define-fun formal_0_364 () FormalMachine (FormalCallback formal_0_363 boundary_0 (select (m_origin formal_0_363) 6) (select (m_origin formal_0_363) 2)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[17]:parent-child
(assert (not (m_panicked formal_0_364)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_364) (select (m_origin formal_0_364) 1) (select (m_origin formal_0_364) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_364) (select (m_origin formal_0_364) 1) (select (m_origin formal_0_364) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[17]:parent-child
(define-fun formal_0_365 () FormalMachine (FormalCallback formal_0_364 boundary_0 (select (m_origin formal_0_364) 1) (select (m_origin formal_0_364) 2)))
; source swap phase=quicksort:imbalance-fallback:sift-down[17]:swap
(define-fun formal_0_366 () FormalMachine (FormalSwap formal_0_365 2 6))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[17]:choose-greater-child
(assert (not (m_panicked formal_0_366)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_366) (select (m_origin formal_0_366) 3) (select (m_origin formal_0_366) 38)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_366) (select (m_origin formal_0_366) 3) (select (m_origin formal_0_366) 38)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[17]:choose-greater-child
(define-fun formal_0_367 () FormalMachine (FormalCallback formal_0_366 boundary_0 (select (m_origin formal_0_366) 3) (select (m_origin formal_0_366) 38)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[17]:parent-child
(assert (not (m_panicked formal_0_367)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_367) (select (m_origin formal_0_367) 1) (select (m_origin formal_0_367) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_367) (select (m_origin formal_0_367) 1) (select (m_origin formal_0_367) 3)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[17]:parent-child
(define-fun formal_0_368 () FormalMachine (FormalCallback formal_0_367 boundary_0 (select (m_origin formal_0_367) 1) (select (m_origin formal_0_367) 3)))
; source swap phase=quicksort:imbalance-fallback:sift-down[17]:swap
(define-fun formal_0_369 () FormalMachine (FormalSwap formal_0_368 6 13))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_370 () FormalMachine (FormalSwap formal_0_369 0 16))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[16]:choose-greater-child
(assert (not (m_panicked formal_0_370)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_370) (select (m_origin formal_0_370) 39) (select (m_origin formal_0_370) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_370) (select (m_origin formal_0_370) 39) (select (m_origin formal_0_370) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[16]:choose-greater-child
(define-fun formal_0_371 () FormalMachine (FormalCallback formal_0_370 boundary_0 (select (m_origin formal_0_370) 39) (select (m_origin formal_0_370) 2)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[16]:parent-child
(assert (not (m_panicked formal_0_371)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_371) (select (m_origin formal_0_371) 33) (select (m_origin formal_0_371) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_371) (select (m_origin formal_0_371) 33) (select (m_origin formal_0_371) 39)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[16]:parent-child
(define-fun formal_0_372 () FormalMachine (FormalCallback formal_0_371 boundary_0 (select (m_origin formal_0_371) 33) (select (m_origin formal_0_371) 39)))
; source swap phase=quicksort:imbalance-fallback:sift-down[16]:swap
(define-fun formal_0_373 () FormalMachine (FormalSwap formal_0_372 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[16]:choose-greater-child
(assert (not (m_panicked formal_0_373)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_373) (select (m_origin formal_0_373) 31) (select (m_origin formal_0_373) 25)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_373) (select (m_origin formal_0_373) 31) (select (m_origin formal_0_373) 25)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[16]:choose-greater-child
(define-fun formal_0_374 () FormalMachine (FormalCallback formal_0_373 boundary_0 (select (m_origin formal_0_373) 31) (select (m_origin formal_0_373) 25)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[16]:parent-child
(assert (not (m_panicked formal_0_374)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_374) (select (m_origin formal_0_374) 33) (select (m_origin formal_0_374) 25)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_374) (select (m_origin formal_0_374) 33) (select (m_origin formal_0_374) 25)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[16]:parent-child
(define-fun formal_0_375 () FormalMachine (FormalCallback formal_0_374 boundary_0 (select (m_origin formal_0_374) 33) (select (m_origin formal_0_374) 25)))
; source swap phase=quicksort:imbalance-fallback:sift-down[16]:swap
(define-fun formal_0_376 () FormalMachine (FormalSwap formal_0_375 1 4))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[16]:choose-greater-child
(assert (not (m_panicked formal_0_376)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_376) (select (m_origin formal_0_376) 35) (select (m_origin formal_0_376) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_376) (select (m_origin formal_0_376) 35) (select (m_origin formal_0_376) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[16]:choose-greater-child
(define-fun formal_0_377 () FormalMachine (FormalCallback formal_0_376 boundary_0 (select (m_origin formal_0_376) 35) (select (m_origin formal_0_376) 7)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[16]:parent-child
(assert (not (m_panicked formal_0_377)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_377) (select (m_origin formal_0_377) 33) (select (m_origin formal_0_377) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_377) (select (m_origin formal_0_377) 33) (select (m_origin formal_0_377) 35)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[16]:parent-child
(define-fun formal_0_378 () FormalMachine (FormalCallback formal_0_377 boundary_0 (select (m_origin formal_0_377) 33) (select (m_origin formal_0_377) 35)))
; source swap phase=quicksort:imbalance-fallback:sift-down[16]:swap
(define-fun formal_0_379 () FormalMachine (FormalSwap formal_0_378 4 9))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_380 () FormalMachine (FormalSwap formal_0_379 0 15))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[15]:choose-greater-child
(assert (not (m_panicked formal_0_380)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_380) (select (m_origin formal_0_380) 25) (select (m_origin formal_0_380) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_380) (select (m_origin formal_0_380) 25) (select (m_origin formal_0_380) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[15]:choose-greater-child
(define-fun formal_0_381 () FormalMachine (FormalCallback formal_0_380 boundary_0 (select (m_origin formal_0_380) 25) (select (m_origin formal_0_380) 2)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[15]:parent-child
(assert (not (m_panicked formal_0_381)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_381) (select (m_origin formal_0_381) 26) (select (m_origin formal_0_381) 25)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_381) (select (m_origin formal_0_381) 26) (select (m_origin formal_0_381) 25)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[15]:parent-child
(define-fun formal_0_382 () FormalMachine (FormalCallback formal_0_381 boundary_0 (select (m_origin formal_0_381) 26) (select (m_origin formal_0_381) 25)))
; source swap phase=quicksort:imbalance-fallback:sift-down[15]:swap
(define-fun formal_0_383 () FormalMachine (FormalSwap formal_0_382 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[15]:choose-greater-child
(assert (not (m_panicked formal_0_383)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_383) (select (m_origin formal_0_383) 31) (select (m_origin formal_0_383) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_383) (select (m_origin formal_0_383) 31) (select (m_origin formal_0_383) 35)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[15]:choose-greater-child
(define-fun formal_0_384 () FormalMachine (FormalCallback formal_0_383 boundary_0 (select (m_origin formal_0_383) 31) (select (m_origin formal_0_383) 35)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[15]:parent-child
(assert (not (m_panicked formal_0_384)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_384) (select (m_origin formal_0_384) 26) (select (m_origin formal_0_384) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_384) (select (m_origin formal_0_384) 26) (select (m_origin formal_0_384) 35)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[15]:parent-child
(define-fun formal_0_385 () FormalMachine (FormalCallback formal_0_384 boundary_0 (select (m_origin formal_0_384) 26) (select (m_origin formal_0_384) 35)))
; source swap phase=quicksort:imbalance-fallback:sift-down[15]:swap
(define-fun formal_0_386 () FormalMachine (FormalSwap formal_0_385 1 4))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[15]:choose-greater-child
(assert (not (m_panicked formal_0_386)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_386) (select (m_origin formal_0_386) 33) (select (m_origin formal_0_386) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_386) (select (m_origin formal_0_386) 33) (select (m_origin formal_0_386) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[15]:choose-greater-child
(define-fun formal_0_387 () FormalMachine (FormalCallback formal_0_386 boundary_0 (select (m_origin formal_0_386) 33) (select (m_origin formal_0_386) 7)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[15]:parent-child
(assert (not (m_panicked formal_0_387)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_387) (select (m_origin formal_0_387) 26) (select (m_origin formal_0_387) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_387) (select (m_origin formal_0_387) 26) (select (m_origin formal_0_387) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[15]:parent-child
(define-fun formal_0_388 () FormalMachine (FormalCallback formal_0_387 boundary_0 (select (m_origin formal_0_387) 26) (select (m_origin formal_0_387) 7)))
; source swap phase=quicksort:imbalance-fallback:sift-down[15]:swap
(define-fun formal_0_389 () FormalMachine (FormalSwap formal_0_388 4 10))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_390 () FormalMachine (FormalSwap formal_0_389 0 14))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[14]:choose-greater-child
(assert (not (m_panicked formal_0_390)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_390) (select (m_origin formal_0_390) 35) (select (m_origin formal_0_390) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_390) (select (m_origin formal_0_390) 35) (select (m_origin formal_0_390) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[14]:choose-greater-child
(define-fun formal_0_391 () FormalMachine (FormalCallback formal_0_390 boundary_0 (select (m_origin formal_0_390) 35) (select (m_origin formal_0_390) 2)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[14]:parent-child
(assert (not (m_panicked formal_0_391)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_391) (select (m_origin formal_0_391) 38) (select (m_origin formal_0_391) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_391) (select (m_origin formal_0_391) 38) (select (m_origin formal_0_391) 35)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[14]:parent-child
(define-fun formal_0_392 () FormalMachine (FormalCallback formal_0_391 boundary_0 (select (m_origin formal_0_391) 38) (select (m_origin formal_0_391) 35)))
; source swap phase=quicksort:imbalance-fallback:sift-down[14]:swap
(define-fun formal_0_393 () FormalMachine (FormalSwap formal_0_392 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[14]:choose-greater-child
(assert (not (m_panicked formal_0_393)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_393) (select (m_origin formal_0_393) 31) (select (m_origin formal_0_393) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_393) (select (m_origin formal_0_393) 31) (select (m_origin formal_0_393) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[14]:choose-greater-child
(define-fun formal_0_394 () FormalMachine (FormalCallback formal_0_393 boundary_0 (select (m_origin formal_0_393) 31) (select (m_origin formal_0_393) 7)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[14]:parent-child
(assert (not (m_panicked formal_0_394)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_394) (select (m_origin formal_0_394) 38) (select (m_origin formal_0_394) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_394) (select (m_origin formal_0_394) 38) (select (m_origin formal_0_394) 31)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[14]:parent-child
(define-fun formal_0_395 () FormalMachine (FormalCallback formal_0_394 boundary_0 (select (m_origin formal_0_394) 38) (select (m_origin formal_0_394) 31)))
; source swap phase=quicksort:imbalance-fallback:sift-down[14]:swap
(define-fun formal_0_396 () FormalMachine (FormalSwap formal_0_395 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[14]:choose-greater-child
(assert (not (m_panicked formal_0_396)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_396) (select (m_origin formal_0_396) 20) (select (m_origin formal_0_396) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_396) (select (m_origin formal_0_396) 20) (select (m_origin formal_0_396) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[14]:choose-greater-child
(define-fun formal_0_397 () FormalMachine (FormalCallback formal_0_396 boundary_0 (select (m_origin formal_0_396) 20) (select (m_origin formal_0_396) 37)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[14]:parent-child
(assert (not (m_panicked formal_0_397)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_397) (select (m_origin formal_0_397) 38) (select (m_origin formal_0_397) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_397) (select (m_origin formal_0_397) 38) (select (m_origin formal_0_397) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[14]:parent-child
(define-fun formal_0_398 () FormalMachine (FormalCallback formal_0_397 boundary_0 (select (m_origin formal_0_397) 38) (select (m_origin formal_0_397) 37)))
; source swap phase=quicksort:imbalance-fallback:sift-down[14]:swap
(define-fun formal_0_399 () FormalMachine (FormalSwap formal_0_398 3 8))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_400 () FormalMachine (FormalSwap formal_0_399 0 13))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[13]:choose-greater-child
(assert (not (m_panicked formal_0_400)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_400) (select (m_origin formal_0_400) 31) (select (m_origin formal_0_400) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_400) (select (m_origin formal_0_400) 31) (select (m_origin formal_0_400) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[13]:choose-greater-child
(define-fun formal_0_401 () FormalMachine (FormalCallback formal_0_400 boundary_0 (select (m_origin formal_0_400) 31) (select (m_origin formal_0_400) 2)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[13]:parent-child
(assert (not (m_panicked formal_0_401)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_401) (select (m_origin formal_0_401) 1) (select (m_origin formal_0_401) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_401) (select (m_origin formal_0_401) 1) (select (m_origin formal_0_401) 31)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[13]:parent-child
(define-fun formal_0_402 () FormalMachine (FormalCallback formal_0_401 boundary_0 (select (m_origin formal_0_401) 1) (select (m_origin formal_0_401) 31)))
; source swap phase=quicksort:imbalance-fallback:sift-down[13]:swap
(define-fun formal_0_403 () FormalMachine (FormalSwap formal_0_402 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[13]:choose-greater-child
(assert (not (m_panicked formal_0_403)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_403) (select (m_origin formal_0_403) 37) (select (m_origin formal_0_403) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_403) (select (m_origin formal_0_403) 37) (select (m_origin formal_0_403) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[13]:choose-greater-child
(define-fun formal_0_404 () FormalMachine (FormalCallback formal_0_403 boundary_0 (select (m_origin formal_0_403) 37) (select (m_origin formal_0_403) 7)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[13]:parent-child
(assert (not (m_panicked formal_0_404)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_404) (select (m_origin formal_0_404) 1) (select (m_origin formal_0_404) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_404) (select (m_origin formal_0_404) 1) (select (m_origin formal_0_404) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[13]:parent-child
(define-fun formal_0_405 () FormalMachine (FormalCallback formal_0_404 boundary_0 (select (m_origin formal_0_404) 1) (select (m_origin formal_0_404) 7)))
; source swap phase=quicksort:imbalance-fallback:sift-down[13]:swap
(define-fun formal_0_406 () FormalMachine (FormalSwap formal_0_405 1 4))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[13]:choose-greater-child
(assert (not (m_panicked formal_0_406)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_406) (select (m_origin formal_0_406) 33) (select (m_origin formal_0_406) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_406) (select (m_origin formal_0_406) 33) (select (m_origin formal_0_406) 26)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[13]:choose-greater-child
(define-fun formal_0_407 () FormalMachine (FormalCallback formal_0_406 boundary_0 (select (m_origin formal_0_406) 33) (select (m_origin formal_0_406) 26)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[13]:parent-child
(assert (not (m_panicked formal_0_407)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_407) (select (m_origin formal_0_407) 1) (select (m_origin formal_0_407) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_407) (select (m_origin formal_0_407) 1) (select (m_origin formal_0_407) 26)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[13]:parent-child
(define-fun formal_0_408 () FormalMachine (FormalCallback formal_0_407 boundary_0 (select (m_origin formal_0_407) 1) (select (m_origin formal_0_407) 26)))
; source swap phase=quicksort:imbalance-fallback:sift-down[13]:swap
(define-fun formal_0_409 () FormalMachine (FormalSwap formal_0_408 4 10))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_410 () FormalMachine (FormalSwap formal_0_409 0 12))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[12]:choose-greater-child
(assert (not (m_panicked formal_0_410)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_410) (select (m_origin formal_0_410) 7) (select (m_origin formal_0_410) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_410) (select (m_origin formal_0_410) 7) (select (m_origin formal_0_410) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[12]:choose-greater-child
(define-fun formal_0_411 () FormalMachine (FormalCallback formal_0_410 boundary_0 (select (m_origin formal_0_410) 7) (select (m_origin formal_0_410) 2)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[12]:parent-child
(assert (not (m_panicked formal_0_411)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_411) (select (m_origin formal_0_411) 5) (select (m_origin formal_0_411) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_411) (select (m_origin formal_0_411) 5) (select (m_origin formal_0_411) 2)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[12]:parent-child
(define-fun formal_0_412 () FormalMachine (FormalCallback formal_0_411 boundary_0 (select (m_origin formal_0_411) 5) (select (m_origin formal_0_411) 2)))
; source swap phase=quicksort:imbalance-fallback:sift-down[12]:swap
(define-fun formal_0_413 () FormalMachine (FormalSwap formal_0_412 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[12]:choose-greater-child
(assert (not (m_panicked formal_0_413)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_413) (select (m_origin formal_0_413) 6) (select (m_origin formal_0_413) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_413) (select (m_origin formal_0_413) 6) (select (m_origin formal_0_413) 3)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[12]:choose-greater-child
(define-fun formal_0_414 () FormalMachine (FormalCallback formal_0_413 boundary_0 (select (m_origin formal_0_413) 6) (select (m_origin formal_0_413) 3)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[12]:parent-child
(assert (not (m_panicked formal_0_414)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_414) (select (m_origin formal_0_414) 5) (select (m_origin formal_0_414) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_414) (select (m_origin formal_0_414) 5) (select (m_origin formal_0_414) 6)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[12]:parent-child
(define-fun formal_0_415 () FormalMachine (FormalCallback formal_0_414 boundary_0 (select (m_origin formal_0_414) 5) (select (m_origin formal_0_414) 6)))
; source swap phase=quicksort:imbalance-fallback:sift-down[12]:swap
(define-fun formal_0_416 () FormalMachine (FormalSwap formal_0_415 2 5))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[12]:parent-child
(assert (not (m_panicked formal_0_416)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_416) (select (m_origin formal_0_416) 5) (select (m_origin formal_0_416) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_416) (select (m_origin formal_0_416) 5) (select (m_origin formal_0_416) 23)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[12]:parent-child
(define-fun formal_0_417 () FormalMachine (FormalCallback formal_0_416 boundary_0 (select (m_origin formal_0_416) 5) (select (m_origin formal_0_416) 23)))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_418 () FormalMachine (FormalSwap formal_0_417 0 11))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[11]:choose-greater-child
(assert (not (m_panicked formal_0_418)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_418) (select (m_origin formal_0_418) 7) (select (m_origin formal_0_418) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_418) (select (m_origin formal_0_418) 7) (select (m_origin formal_0_418) 6)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[11]:choose-greater-child
(define-fun formal_0_419 () FormalMachine (FormalCallback formal_0_418 boundary_0 (select (m_origin formal_0_418) 7) (select (m_origin formal_0_418) 6)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[11]:parent-child
(assert (not (m_panicked formal_0_419)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_419) (select (m_origin formal_0_419) 23) (select (m_origin formal_0_419) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_419) (select (m_origin formal_0_419) 23) (select (m_origin formal_0_419) 6)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[11]:parent-child
(define-fun formal_0_420 () FormalMachine (FormalCallback formal_0_419 boundary_0 (select (m_origin formal_0_419) 23) (select (m_origin formal_0_419) 6)))
; source swap phase=quicksort:imbalance-fallback:sift-down[11]:swap
(define-fun formal_0_421 () FormalMachine (FormalSwap formal_0_420 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[11]:choose-greater-child
(assert (not (m_panicked formal_0_421)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_421) (select (m_origin formal_0_421) 5) (select (m_origin formal_0_421) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_421) (select (m_origin formal_0_421) 5) (select (m_origin formal_0_421) 3)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[11]:choose-greater-child
(define-fun formal_0_422 () FormalMachine (FormalCallback formal_0_421 boundary_0 (select (m_origin formal_0_421) 5) (select (m_origin formal_0_421) 3)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[11]:parent-child
(assert (not (m_panicked formal_0_422)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_422) (select (m_origin formal_0_422) 23) (select (m_origin formal_0_422) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_422) (select (m_origin formal_0_422) 23) (select (m_origin formal_0_422) 3)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[11]:parent-child
(define-fun formal_0_423 () FormalMachine (FormalCallback formal_0_422 boundary_0 (select (m_origin formal_0_422) 23) (select (m_origin formal_0_422) 3)))
; source swap phase=quicksort:imbalance-fallback:sift-down[11]:swap
(define-fun formal_0_424 () FormalMachine (FormalSwap formal_0_423 2 6))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_425 () FormalMachine (FormalSwap formal_0_424 0 10))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[10]:choose-greater-child
(assert (not (m_panicked formal_0_425)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_425) (select (m_origin formal_0_425) 7) (select (m_origin formal_0_425) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_425) (select (m_origin formal_0_425) 7) (select (m_origin formal_0_425) 3)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[10]:choose-greater-child
(define-fun formal_0_426 () FormalMachine (FormalCallback formal_0_425 boundary_0 (select (m_origin formal_0_425) 7) (select (m_origin formal_0_425) 3)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[10]:parent-child
(assert (not (m_panicked formal_0_426)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_426) (select (m_origin formal_0_426) 1) (select (m_origin formal_0_426) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_426) (select (m_origin formal_0_426) 1) (select (m_origin formal_0_426) 7)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[10]:parent-child
(define-fun formal_0_427 () FormalMachine (FormalCallback formal_0_426 boundary_0 (select (m_origin formal_0_426) 1) (select (m_origin formal_0_426) 7)))
; source swap phase=quicksort:imbalance-fallback:sift-down[10]:swap
(define-fun formal_0_428 () FormalMachine (FormalSwap formal_0_427 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[10]:choose-greater-child
(assert (not (m_panicked formal_0_428)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_428) (select (m_origin formal_0_428) 37) (select (m_origin formal_0_428) 26)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_428) (select (m_origin formal_0_428) 37) (select (m_origin formal_0_428) 26)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[10]:choose-greater-child
(define-fun formal_0_429 () FormalMachine (FormalCallback formal_0_428 boundary_0 (select (m_origin formal_0_428) 37) (select (m_origin formal_0_428) 26)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[10]:parent-child
(assert (not (m_panicked formal_0_429)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_429) (select (m_origin formal_0_429) 1) (select (m_origin formal_0_429) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_429) (select (m_origin formal_0_429) 1) (select (m_origin formal_0_429) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[10]:parent-child
(define-fun formal_0_430 () FormalMachine (FormalCallback formal_0_429 boundary_0 (select (m_origin formal_0_429) 1) (select (m_origin formal_0_429) 37)))
; source swap phase=quicksort:imbalance-fallback:sift-down[10]:swap
(define-fun formal_0_431 () FormalMachine (FormalSwap formal_0_430 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[10]:choose-greater-child
(assert (not (m_panicked formal_0_431)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_431) (select (m_origin formal_0_431) 20) (select (m_origin formal_0_431) 38)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_431) (select (m_origin formal_0_431) 20) (select (m_origin formal_0_431) 38)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[10]:choose-greater-child
(define-fun formal_0_432 () FormalMachine (FormalCallback formal_0_431 boundary_0 (select (m_origin formal_0_431) 20) (select (m_origin formal_0_431) 38)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[10]:parent-child
(assert (not (m_panicked formal_0_432)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_432) (select (m_origin formal_0_432) 1) (select (m_origin formal_0_432) 38)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_432) (select (m_origin formal_0_432) 1) (select (m_origin formal_0_432) 38)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[10]:parent-child
(define-fun formal_0_433 () FormalMachine (FormalCallback formal_0_432 boundary_0 (select (m_origin formal_0_432) 1) (select (m_origin formal_0_432) 38)))
; source swap phase=quicksort:imbalance-fallback:sift-down[10]:swap
(define-fun formal_0_434 () FormalMachine (FormalSwap formal_0_433 3 8))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_435 () FormalMachine (FormalSwap formal_0_434 0 9))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[9]:choose-greater-child
(assert (not (m_panicked formal_0_435)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_435) (select (m_origin formal_0_435) 37) (select (m_origin formal_0_435) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_435) (select (m_origin formal_0_435) 37) (select (m_origin formal_0_435) 3)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[9]:choose-greater-child
(define-fun formal_0_436 () FormalMachine (FormalCallback formal_0_435 boundary_0 (select (m_origin formal_0_435) 37) (select (m_origin formal_0_435) 3)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[9]:parent-child
(assert (not (m_panicked formal_0_436)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_436) (select (m_origin formal_0_436) 33) (select (m_origin formal_0_436) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_436) (select (m_origin formal_0_436) 33) (select (m_origin formal_0_436) 37)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[9]:parent-child
(define-fun formal_0_437 () FormalMachine (FormalCallback formal_0_436 boundary_0 (select (m_origin formal_0_436) 33) (select (m_origin formal_0_436) 37)))
; source swap phase=quicksort:imbalance-fallback:sift-down[9]:swap
(define-fun formal_0_438 () FormalMachine (FormalSwap formal_0_437 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[9]:choose-greater-child
(assert (not (m_panicked formal_0_438)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_438) (select (m_origin formal_0_438) 38) (select (m_origin formal_0_438) 26)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_438) (select (m_origin formal_0_438) 38) (select (m_origin formal_0_438) 26)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[9]:choose-greater-child
(define-fun formal_0_439 () FormalMachine (FormalCallback formal_0_438 boundary_0 (select (m_origin formal_0_438) 38) (select (m_origin formal_0_438) 26)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[9]:parent-child
(assert (not (m_panicked formal_0_439)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_439) (select (m_origin formal_0_439) 33) (select (m_origin formal_0_439) 38)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_439) (select (m_origin formal_0_439) 33) (select (m_origin formal_0_439) 38)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[9]:parent-child
(define-fun formal_0_440 () FormalMachine (FormalCallback formal_0_439 boundary_0 (select (m_origin formal_0_439) 33) (select (m_origin formal_0_439) 38)))
; source swap phase=quicksort:imbalance-fallback:sift-down[9]:swap
(define-fun formal_0_441 () FormalMachine (FormalSwap formal_0_440 1 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[9]:choose-greater-child
(assert (not (m_panicked formal_0_441)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_441) (select (m_origin formal_0_441) 20) (select (m_origin formal_0_441) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_441) (select (m_origin formal_0_441) 20) (select (m_origin formal_0_441) 1)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[9]:choose-greater-child
(define-fun formal_0_442 () FormalMachine (FormalCallback formal_0_441 boundary_0 (select (m_origin formal_0_441) 20) (select (m_origin formal_0_441) 1)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[9]:parent-child
(assert (not (m_panicked formal_0_442)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_442) (select (m_origin formal_0_442) 33) (select (m_origin formal_0_442) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_442) (select (m_origin formal_0_442) 33) (select (m_origin formal_0_442) 20)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[9]:parent-child
(define-fun formal_0_443 () FormalMachine (FormalCallback formal_0_442 boundary_0 (select (m_origin formal_0_442) 33) (select (m_origin formal_0_442) 20)))
; source swap phase=quicksort:imbalance-fallback:sift-down[9]:swap
(define-fun formal_0_444 () FormalMachine (FormalSwap formal_0_443 3 7))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_445 () FormalMachine (FormalSwap formal_0_444 0 8))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[8]:choose-greater-child
(assert (not (m_panicked formal_0_445)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_445) (select (m_origin formal_0_445) 38) (select (m_origin formal_0_445) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_445) (select (m_origin formal_0_445) 38) (select (m_origin formal_0_445) 3)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[8]:choose-greater-child
(define-fun formal_0_446 () FormalMachine (FormalCallback formal_0_445 boundary_0 (select (m_origin formal_0_445) 38) (select (m_origin formal_0_445) 3)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[8]:parent-child
(assert (not (m_panicked formal_0_446)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_446) (select (m_origin formal_0_446) 1) (select (m_origin formal_0_446) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_446) (select (m_origin formal_0_446) 1) (select (m_origin formal_0_446) 3)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[8]:parent-child
(define-fun formal_0_447 () FormalMachine (FormalCallback formal_0_446 boundary_0 (select (m_origin formal_0_446) 1) (select (m_origin formal_0_446) 3)))
; source swap phase=quicksort:imbalance-fallback:sift-down[8]:swap
(define-fun formal_0_448 () FormalMachine (FormalSwap formal_0_447 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[8]:choose-greater-child
(assert (not (m_panicked formal_0_448)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_448) (select (m_origin formal_0_448) 5) (select (m_origin formal_0_448) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_448) (select (m_origin formal_0_448) 5) (select (m_origin formal_0_448) 23)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[8]:choose-greater-child
(define-fun formal_0_449 () FormalMachine (FormalCallback formal_0_448 boundary_0 (select (m_origin formal_0_448) 5) (select (m_origin formal_0_448) 23)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[8]:parent-child
(assert (not (m_panicked formal_0_449)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_449) (select (m_origin formal_0_449) 1) (select (m_origin formal_0_449) 5)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_449) (select (m_origin formal_0_449) 1) (select (m_origin formal_0_449) 5)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[8]:parent-child
(define-fun formal_0_450 () FormalMachine (FormalCallback formal_0_449 boundary_0 (select (m_origin formal_0_449) 1) (select (m_origin formal_0_449) 5)))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_451 () FormalMachine (FormalSwap formal_0_450 0 7))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[7]:choose-greater-child
(assert (not (m_panicked formal_0_451)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_451) (select (m_origin formal_0_451) 38) (select (m_origin formal_0_451) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_451) (select (m_origin formal_0_451) 38) (select (m_origin formal_0_451) 1)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[7]:choose-greater-child
(define-fun formal_0_452 () FormalMachine (FormalCallback formal_0_451 boundary_0 (select (m_origin formal_0_451) 38) (select (m_origin formal_0_451) 1)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[7]:parent-child
(assert (not (m_panicked formal_0_452)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_452) (select (m_origin formal_0_452) 33) (select (m_origin formal_0_452) 38)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_452) (select (m_origin formal_0_452) 33) (select (m_origin formal_0_452) 38)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[7]:parent-child
(define-fun formal_0_453 () FormalMachine (FormalCallback formal_0_452 boundary_0 (select (m_origin formal_0_452) 33) (select (m_origin formal_0_452) 38)))
; source swap phase=quicksort:imbalance-fallback:sift-down[7]:swap
(define-fun formal_0_454 () FormalMachine (FormalSwap formal_0_453 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[7]:choose-greater-child
(assert (not (m_panicked formal_0_454)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_454) (select (m_origin formal_0_454) 20) (select (m_origin formal_0_454) 26)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_454) (select (m_origin formal_0_454) 20) (select (m_origin formal_0_454) 26)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[7]:choose-greater-child
(define-fun formal_0_455 () FormalMachine (FormalCallback formal_0_454 boundary_0 (select (m_origin formal_0_454) 20) (select (m_origin formal_0_454) 26)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[7]:parent-child
(assert (not (m_panicked formal_0_455)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_455) (select (m_origin formal_0_455) 33) (select (m_origin formal_0_455) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_455) (select (m_origin formal_0_455) 33) (select (m_origin formal_0_455) 20)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[7]:parent-child
(define-fun formal_0_456 () FormalMachine (FormalCallback formal_0_455 boundary_0 (select (m_origin formal_0_455) 33) (select (m_origin formal_0_455) 20)))
; source swap phase=quicksort:imbalance-fallback:sift-down[7]:swap
(define-fun formal_0_457 () FormalMachine (FormalSwap formal_0_456 1 3))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_458 () FormalMachine (FormalSwap formal_0_457 0 6))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[6]:choose-greater-child
(assert (not (m_panicked formal_0_458)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_458) (select (m_origin formal_0_458) 20) (select (m_origin formal_0_458) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_458) (select (m_origin formal_0_458) 20) (select (m_origin formal_0_458) 1)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[6]:choose-greater-child
(define-fun formal_0_459 () FormalMachine (FormalCallback formal_0_458 boundary_0 (select (m_origin formal_0_458) 20) (select (m_origin formal_0_458) 1)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[6]:parent-child
(assert (not (m_panicked formal_0_459)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_459) (select (m_origin formal_0_459) 23) (select (m_origin formal_0_459) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_459) (select (m_origin formal_0_459) 23) (select (m_origin formal_0_459) 20)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[6]:parent-child
(define-fun formal_0_460 () FormalMachine (FormalCallback formal_0_459 boundary_0 (select (m_origin formal_0_459) 23) (select (m_origin formal_0_459) 20)))
; source swap phase=quicksort:imbalance-fallback:sift-down[6]:swap
(define-fun formal_0_461 () FormalMachine (FormalSwap formal_0_460 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[6]:choose-greater-child
(assert (not (m_panicked formal_0_461)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_461) (select (m_origin formal_0_461) 33) (select (m_origin formal_0_461) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_461) (select (m_origin formal_0_461) 33) (select (m_origin formal_0_461) 26)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[6]:choose-greater-child
(define-fun formal_0_462 () FormalMachine (FormalCallback formal_0_461 boundary_0 (select (m_origin formal_0_461) 33) (select (m_origin formal_0_461) 26)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[6]:parent-child
(assert (not (m_panicked formal_0_462)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_462) (select (m_origin formal_0_462) 23) (select (m_origin formal_0_462) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_462) (select (m_origin formal_0_462) 23) (select (m_origin formal_0_462) 26)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[6]:parent-child
(define-fun formal_0_463 () FormalMachine (FormalCallback formal_0_462 boundary_0 (select (m_origin formal_0_462) 23) (select (m_origin formal_0_462) 26)))
; source swap phase=quicksort:imbalance-fallback:sift-down[6]:swap
(define-fun formal_0_464 () FormalMachine (FormalSwap formal_0_463 1 4))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_465 () FormalMachine (FormalSwap formal_0_464 0 5))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[5]:choose-greater-child
(assert (not (m_panicked formal_0_465)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_465) (select (m_origin formal_0_465) 26) (select (m_origin formal_0_465) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_465) (select (m_origin formal_0_465) 26) (select (m_origin formal_0_465) 1)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[5]:choose-greater-child
(define-fun formal_0_466 () FormalMachine (FormalCallback formal_0_465 boundary_0 (select (m_origin formal_0_465) 26) (select (m_origin formal_0_465) 1)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[5]:parent-child
(assert (not (m_panicked formal_0_466)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_466) (select (m_origin formal_0_466) 5) (select (m_origin formal_0_466) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_466) (select (m_origin formal_0_466) 5) (select (m_origin formal_0_466) 26)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[5]:parent-child
(define-fun formal_0_467 () FormalMachine (FormalCallback formal_0_466 boundary_0 (select (m_origin formal_0_466) 5) (select (m_origin formal_0_466) 26)))
; source swap phase=quicksort:imbalance-fallback:sift-down[5]:swap
(define-fun formal_0_468 () FormalMachine (FormalSwap formal_0_467 0 1))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[5]:choose-greater-child
(assert (not (m_panicked formal_0_468)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_468) (select (m_origin formal_0_468) 33) (select (m_origin formal_0_468) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_468) (select (m_origin formal_0_468) 33) (select (m_origin formal_0_468) 23)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[5]:choose-greater-child
(define-fun formal_0_469 () FormalMachine (FormalCallback formal_0_468 boundary_0 (select (m_origin formal_0_468) 33) (select (m_origin formal_0_468) 23)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[5]:parent-child
(assert (not (m_panicked formal_0_469)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_469) (select (m_origin formal_0_469) 5) (select (m_origin formal_0_469) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_469) (select (m_origin formal_0_469) 5) (select (m_origin formal_0_469) 33)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[5]:parent-child
(define-fun formal_0_470 () FormalMachine (FormalCallback formal_0_469 boundary_0 (select (m_origin formal_0_469) 5) (select (m_origin formal_0_469) 33)))
; source swap phase=quicksort:imbalance-fallback:sift-down[5]:swap
(define-fun formal_0_471 () FormalMachine (FormalSwap formal_0_470 1 3))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_472 () FormalMachine (FormalSwap formal_0_471 0 4))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[4]:choose-greater-child
(assert (not (m_panicked formal_0_472)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_472) (select (m_origin formal_0_472) 33) (select (m_origin formal_0_472) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_472) (select (m_origin formal_0_472) 33) (select (m_origin formal_0_472) 1)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[4]:choose-greater-child
(define-fun formal_0_473 () FormalMachine (FormalCallback formal_0_472 boundary_0 (select (m_origin formal_0_472) 33) (select (m_origin formal_0_472) 1)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[4]:parent-child
(assert (not (m_panicked formal_0_473)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_473) (select (m_origin formal_0_473) 23) (select (m_origin formal_0_473) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_473) (select (m_origin formal_0_473) 23) (select (m_origin formal_0_473) 1)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[4]:parent-child
(define-fun formal_0_474 () FormalMachine (FormalCallback formal_0_473 boundary_0 (select (m_origin formal_0_473) 23) (select (m_origin formal_0_473) 1)))
; source swap phase=quicksort:imbalance-fallback:sift-down[4]:swap
(define-fun formal_0_475 () FormalMachine (FormalSwap formal_0_474 0 2))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_476 () FormalMachine (FormalSwap formal_0_475 0 3))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[3]:choose-greater-child
(assert (not (m_panicked formal_0_476)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_476) (select (m_origin formal_0_476) 33) (select (m_origin formal_0_476) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_476) (select (m_origin formal_0_476) 33) (select (m_origin formal_0_476) 23)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[3]:choose-greater-child
(define-fun formal_0_477 () FormalMachine (FormalCallback formal_0_476 boundary_0 (select (m_origin formal_0_476) 33) (select (m_origin formal_0_476) 23)))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[3]:parent-child
(assert (not (m_panicked formal_0_477)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_477) (select (m_origin formal_0_477) 5) (select (m_origin formal_0_477) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_477) (select (m_origin formal_0_477) 5) (select (m_origin formal_0_477) 33)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[3]:parent-child
(define-fun formal_0_478 () FormalMachine (FormalCallback formal_0_477 boundary_0 (select (m_origin formal_0_477) 5) (select (m_origin formal_0_477) 33)))
; source swap phase=quicksort:imbalance-fallback:sift-down[3]:swap
(define-fun formal_0_479 () FormalMachine (FormalSwap formal_0_478 0 1))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_480 () FormalMachine (FormalSwap formal_0_479 0 2))
; source callback case=imbalance-fallback-direct phase=quicksort:imbalance-fallback:sift-down[2]:parent-child
(assert (not (m_panicked formal_0_480)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_480) (select (m_origin formal_0_480) 23) (select (m_origin formal_0_480) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_480) (select (m_origin formal_0_480) 23) (select (m_origin formal_0_480) 5)) false))
; source callback transition phase=quicksort:imbalance-fallback:sift-down[2]:parent-child
(define-fun formal_0_481 () FormalMachine (FormalCallback formal_0_480 boundary_0 (select (m_origin formal_0_480) 23) (select (m_origin formal_0_480) 5)))
; source swap phase=quicksort:imbalance-fallback:sift-down[2]:swap
(define-fun formal_0_482 () FormalMachine (FormalSwap formal_0_481 0 1))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_483 () FormalMachine (FormalSwap formal_0_482 0 1))
; source swap phase=quicksort:imbalance-fallback:extract
(define-fun formal_0_484 () FormalMachine (FormalSwap formal_0_483 0 0))
(define-fun formal_result_0 () Result
  (mkResult
    (m_sequence formal_0_484)
    (m_callback formal_0_484)
    (m_panicked formal_0_484)
    false
    true
    (ite (m_panicked formal_0_484) 1 0)
    (not (m_panicked formal_0_484))
    -1))
(define-fun reference_result_0 () Result (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 21 21) 22 22) 23 23) 24 24) 25 25) 26 26) 27 27) 28 28) 29 29) 30 30) 31 31) 32 32) 33 33) 34 34) 35 35) 36 36) 37 37) 38 38) 39 39) 306 false false true 0 true -1))
; retained source-forcing witness: imbalance-limit-fallback
(assert (= formal_result_0 (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 21 21) 22 22) 23 23) 24 24) 25 25) 26 26) 27 27) 28 28) 29 29) 30 30) 31 31) 32 32) 33 33) 34 34) 35 35) 36 36) 37 37) 38 38) 39 39) 306 false false true 0 true -1)))
(check-sat-using (then ctx-solver-simplify smt))
