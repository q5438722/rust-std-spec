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

; formal source input case=cyclic-unroll-one-partition
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
    32
    false
    false))
(define-fun source_initial_0 () FormalMachine
  (mkFormalMachine (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 27) 1 14) 2 30) 3 13) 4 0) 5 18) 6 19) 7 7) 8 10) 9 5) 10 43) 11 38) 12 15) 13 11) 14 6) 15 42) 16 39) 17 4) 18 2) 19 29) 20 1) 21 21) 22 37) 23 32) 24 17) 25 35) 26 24) 27 31) 28 16) 29 3) 30 40) 31 12) 32 25) 33 20) 34 23) 35 22) 36 36) 37 34) 38 26) 39 28) 40 41) 41 8) 42 44) 43 9) 44 33) (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 27) 1 14) 2 30) 3 13) 4 0) 5 18) 6 19) 7 7) 8 10) 9 5) 10 43) 11 38) 12 15) 13 11) 14 6) 15 42) 16 39) 17 4) 18 2) 19 29) 20 1) 21 21) 22 37) 23 32) 24 17) 25 35) 26 24) 27 31) 28 16) 29 3) 30 40) 31 12) 32 25) 33 20) 34 23) 35 22) 36 36) 37 34) 38 26) 39 28) 40 41) 41 8) 42 44) 43 9) 44 33) (b_initial_state boundary_0) false))
(assert (BoundaryWellFormed boundary_0))
; source callback case=cyclic-unroll-one-partition phase=find-existing-run:direction
(assert (not (m_panicked source_initial_0)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) false))
; source callback transition phase=find-existing-run:direction
(define-fun formal_0_1 () FormalMachine (FormalCallback source_initial_0 boundary_0 (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)))
; source callback case=cyclic-unroll-one-partition phase=find-existing-run:descending
(assert (not (m_panicked formal_0_1)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) false))
; source callback transition phase=find-existing-run:descending
(define-fun formal_0_2 () FormalMachine (FormalCallback formal_0_1 boundary_0 (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)))
; source callback case=cyclic-unroll-one-partition phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_2)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 0) (select (m_origin formal_0_2) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 0) (select (m_origin formal_0_2) 20)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_3 () FormalMachine (FormalCallback formal_0_2 boundary_0 (select (m_origin formal_0_2) 0) (select (m_origin formal_0_2) 20)))
; source callback case=cyclic-unroll-one-partition phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_3)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 0) (select (m_origin formal_0_3) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 0) (select (m_origin formal_0_3) 35)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_4 () FormalMachine (FormalCallback formal_0_3 boundary_0 (select (m_origin formal_0_3) 0) (select (m_origin formal_0_3) 35)))
; source callback case=cyclic-unroll-one-partition phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_4)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 20) (select (m_origin formal_0_4) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 20) (select (m_origin formal_0_4) 35)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_5 () FormalMachine (FormalCallback formal_0_4 boundary_0 (select (m_origin formal_0_4) 20) (select (m_origin formal_0_4) 35)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_6 () FormalMachine (FormalSwap formal_0_5 0 35))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_6)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 2) (select (m_origin formal_0_6) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 2) (select (m_origin formal_0_6) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_7 () FormalMachine (FormalCallback formal_0_6 boundary_0 (select (m_origin formal_0_6) 2) (select (m_origin formal_0_6) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_8 () FormalMachine (FormalWriteFromOrigin formal_0_7 1 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_8)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 3) (select (m_origin formal_0_8) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 3) (select (m_origin formal_0_8) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_9 () FormalMachine (FormalCallback formal_0_8 boundary_0 (select (m_origin formal_0_8) 3) (select (m_origin formal_0_8) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_10 () FormalMachine (FormalWriteFromOrigin formal_0_9 1 3))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_10)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_10) (select (m_origin formal_0_10) 4) (select (m_origin formal_0_10) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_10) (select (m_origin formal_0_10) 4) (select (m_origin formal_0_10) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_11 () FormalMachine (FormalCallback formal_0_10 boundary_0 (select (m_origin formal_0_10) 4) (select (m_origin formal_0_10) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_12 () FormalMachine (FormalWriteFromOrigin formal_0_11 2 4))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_13 () FormalMachine (FormalWriteFromOrigin formal_0_12 3 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_13)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_13) (select (m_origin formal_0_13) 5) (select (m_origin formal_0_13) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_13) (select (m_origin formal_0_13) 5) (select (m_origin formal_0_13) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_14 () FormalMachine (FormalCallback formal_0_13 boundary_0 (select (m_origin formal_0_13) 5) (select (m_origin formal_0_13) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_15 () FormalMachine (FormalWriteFromOrigin formal_0_14 3 5))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_16 () FormalMachine (FormalWriteFromOrigin formal_0_15 4 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_16)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_16) (select (m_origin formal_0_16) 6) (select (m_origin formal_0_16) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_16) (select (m_origin formal_0_16) 6) (select (m_origin formal_0_16) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_17 () FormalMachine (FormalCallback formal_0_16 boundary_0 (select (m_origin formal_0_16) 6) (select (m_origin formal_0_16) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_18 () FormalMachine (FormalWriteFromOrigin formal_0_17 4 6))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_19 () FormalMachine (FormalWriteFromOrigin formal_0_18 5 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_19)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_19) (select (m_origin formal_0_19) 7) (select (m_origin formal_0_19) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_19) (select (m_origin formal_0_19) 7) (select (m_origin formal_0_19) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_20 () FormalMachine (FormalCallback formal_0_19 boundary_0 (select (m_origin formal_0_19) 7) (select (m_origin formal_0_19) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_21 () FormalMachine (FormalWriteFromOrigin formal_0_20 5 7))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_22 () FormalMachine (FormalWriteFromOrigin formal_0_21 6 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_22)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_22) (select (m_origin formal_0_22) 8) (select (m_origin formal_0_22) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_22) (select (m_origin formal_0_22) 8) (select (m_origin formal_0_22) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_23 () FormalMachine (FormalCallback formal_0_22 boundary_0 (select (m_origin formal_0_22) 8) (select (m_origin formal_0_22) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_24 () FormalMachine (FormalWriteFromOrigin formal_0_23 6 8))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_25 () FormalMachine (FormalWriteFromOrigin formal_0_24 7 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_25)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 9) (select (m_origin formal_0_25) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 9) (select (m_origin formal_0_25) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_26 () FormalMachine (FormalCallback formal_0_25 boundary_0 (select (m_origin formal_0_25) 9) (select (m_origin formal_0_25) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_27 () FormalMachine (FormalWriteFromOrigin formal_0_26 7 9))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_28 () FormalMachine (FormalWriteFromOrigin formal_0_27 8 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_28)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_28) (select (m_origin formal_0_28) 10) (select (m_origin formal_0_28) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_28) (select (m_origin formal_0_28) 10) (select (m_origin formal_0_28) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_29 () FormalMachine (FormalCallback formal_0_28 boundary_0 (select (m_origin formal_0_28) 10) (select (m_origin formal_0_28) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_30 () FormalMachine (FormalWriteFromOrigin formal_0_29 8 10))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_31 () FormalMachine (FormalWriteFromOrigin formal_0_30 9 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_31)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_31) (select (m_origin formal_0_31) 11) (select (m_origin formal_0_31) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_31) (select (m_origin formal_0_31) 11) (select (m_origin formal_0_31) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_32 () FormalMachine (FormalCallback formal_0_31 boundary_0 (select (m_origin formal_0_31) 11) (select (m_origin formal_0_31) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_33 () FormalMachine (FormalWriteFromOrigin formal_0_32 8 11))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_33)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_33) (select (m_origin formal_0_33) 12) (select (m_origin formal_0_33) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_33) (select (m_origin formal_0_33) 12) (select (m_origin formal_0_33) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_34 () FormalMachine (FormalCallback formal_0_33 boundary_0 (select (m_origin formal_0_33) 12) (select (m_origin formal_0_33) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_35 () FormalMachine (FormalWriteFromOrigin formal_0_34 8 12))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_35)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_35) (select (m_origin formal_0_35) 13) (select (m_origin formal_0_35) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_35) (select (m_origin formal_0_35) 13) (select (m_origin formal_0_35) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_36 () FormalMachine (FormalCallback formal_0_35 boundary_0 (select (m_origin formal_0_35) 13) (select (m_origin formal_0_35) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_37 () FormalMachine (FormalWriteFromOrigin formal_0_36 9 13))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_38 () FormalMachine (FormalWriteFromOrigin formal_0_37 12 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_38)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 14) (select (m_origin formal_0_38) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 14) (select (m_origin formal_0_38) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_39 () FormalMachine (FormalCallback formal_0_38 boundary_0 (select (m_origin formal_0_38) 14) (select (m_origin formal_0_38) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_40 () FormalMachine (FormalWriteFromOrigin formal_0_39 10 14))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_41 () FormalMachine (FormalWriteFromOrigin formal_0_40 13 10))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_41)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 15) (select (m_origin formal_0_41) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 15) (select (m_origin formal_0_41) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_42 () FormalMachine (FormalCallback formal_0_41 boundary_0 (select (m_origin formal_0_41) 15) (select (m_origin formal_0_41) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_43 () FormalMachine (FormalWriteFromOrigin formal_0_42 11 15))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_44 () FormalMachine (FormalWriteFromOrigin formal_0_43 14 11))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_44)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 16) (select (m_origin formal_0_44) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 16) (select (m_origin formal_0_44) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_45 () FormalMachine (FormalCallback formal_0_44 boundary_0 (select (m_origin formal_0_44) 16) (select (m_origin formal_0_44) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_46 () FormalMachine (FormalWriteFromOrigin formal_0_45 11 16))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_46)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_46) (select (m_origin formal_0_46) 17) (select (m_origin formal_0_46) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_46) (select (m_origin formal_0_46) 17) (select (m_origin formal_0_46) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_47 () FormalMachine (FormalCallback formal_0_46 boundary_0 (select (m_origin formal_0_46) 17) (select (m_origin formal_0_46) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_48 () FormalMachine (FormalWriteFromOrigin formal_0_47 11 17))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_48)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 18) (select (m_origin formal_0_48) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 18) (select (m_origin formal_0_48) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_49 () FormalMachine (FormalCallback formal_0_48 boundary_0 (select (m_origin formal_0_48) 18) (select (m_origin formal_0_48) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_50 () FormalMachine (FormalWriteFromOrigin formal_0_49 12 18))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_51 () FormalMachine (FormalWriteFromOrigin formal_0_50 17 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_51)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_51) (select (m_origin formal_0_51) 19) (select (m_origin formal_0_51) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_51) (select (m_origin formal_0_51) 19) (select (m_origin formal_0_51) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_52 () FormalMachine (FormalCallback formal_0_51 boundary_0 (select (m_origin formal_0_51) 19) (select (m_origin formal_0_51) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_53 () FormalMachine (FormalWriteFromOrigin formal_0_52 13 19))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_54 () FormalMachine (FormalWriteFromOrigin formal_0_53 18 10))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_54)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_54) (select (m_origin formal_0_54) 20) (select (m_origin formal_0_54) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_54) (select (m_origin formal_0_54) 20) (select (m_origin formal_0_54) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_55 () FormalMachine (FormalCallback formal_0_54 boundary_0 (select (m_origin formal_0_54) 20) (select (m_origin formal_0_54) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_56 () FormalMachine (FormalWriteFromOrigin formal_0_55 13 20))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_56)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_56) (select (m_origin formal_0_56) 21) (select (m_origin formal_0_56) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_56) (select (m_origin formal_0_56) 21) (select (m_origin formal_0_56) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_57 () FormalMachine (FormalCallback formal_0_56 boundary_0 (select (m_origin formal_0_56) 21) (select (m_origin formal_0_56) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_58 () FormalMachine (FormalWriteFromOrigin formal_0_57 14 21))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_59 () FormalMachine (FormalWriteFromOrigin formal_0_58 20 11))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_59)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_59) (select (m_origin formal_0_59) 22) (select (m_origin formal_0_59) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_59) (select (m_origin formal_0_59) 22) (select (m_origin formal_0_59) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_60 () FormalMachine (FormalCallback formal_0_59 boundary_0 (select (m_origin formal_0_59) 22) (select (m_origin formal_0_59) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_61 () FormalMachine (FormalWriteFromOrigin formal_0_60 15 22))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_62 () FormalMachine (FormalWriteFromOrigin formal_0_61 21 15))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_62)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_62) (select (m_origin formal_0_62) 23) (select (m_origin formal_0_62) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_62) (select (m_origin formal_0_62) 23) (select (m_origin formal_0_62) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_63 () FormalMachine (FormalCallback formal_0_62 boundary_0 (select (m_origin formal_0_62) 23) (select (m_origin formal_0_62) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_64 () FormalMachine (FormalWriteFromOrigin formal_0_63 15 23))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_64)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_64) (select (m_origin formal_0_64) 24) (select (m_origin formal_0_64) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_64) (select (m_origin formal_0_64) 24) (select (m_origin formal_0_64) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_65 () FormalMachine (FormalCallback formal_0_64 boundary_0 (select (m_origin formal_0_64) 24) (select (m_origin formal_0_64) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_66 () FormalMachine (FormalWriteFromOrigin formal_0_65 15 24))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_66)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_66) (select (m_origin formal_0_66) 25) (select (m_origin formal_0_66) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_66) (select (m_origin formal_0_66) 25) (select (m_origin formal_0_66) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_67 () FormalMachine (FormalCallback formal_0_66 boundary_0 (select (m_origin formal_0_66) 25) (select (m_origin formal_0_66) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_68 () FormalMachine (FormalWriteFromOrigin formal_0_67 16 25))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_69 () FormalMachine (FormalWriteFromOrigin formal_0_68 24 16))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_69)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 26) (select (m_origin formal_0_69) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 26) (select (m_origin formal_0_69) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_70 () FormalMachine (FormalCallback formal_0_69 boundary_0 (select (m_origin formal_0_69) 26) (select (m_origin formal_0_69) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_71 () FormalMachine (FormalWriteFromOrigin formal_0_70 16 26))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_71)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_71) (select (m_origin formal_0_71) 27) (select (m_origin formal_0_71) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_71) (select (m_origin formal_0_71) 27) (select (m_origin formal_0_71) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_72 () FormalMachine (FormalCallback formal_0_71 boundary_0 (select (m_origin formal_0_71) 27) (select (m_origin formal_0_71) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_73 () FormalMachine (FormalWriteFromOrigin formal_0_72 16 27))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_73)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 28) (select (m_origin formal_0_73) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 28) (select (m_origin formal_0_73) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_74 () FormalMachine (FormalCallback formal_0_73 boundary_0 (select (m_origin formal_0_73) 28) (select (m_origin formal_0_73) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_75 () FormalMachine (FormalWriteFromOrigin formal_0_74 16 28))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_75)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 29) (select (m_origin formal_0_75) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 29) (select (m_origin formal_0_75) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_76 () FormalMachine (FormalCallback formal_0_75 boundary_0 (select (m_origin formal_0_75) 29) (select (m_origin formal_0_75) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_77 () FormalMachine (FormalWriteFromOrigin formal_0_76 17 29))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_78 () FormalMachine (FormalWriteFromOrigin formal_0_77 28 2))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_78)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 30) (select (m_origin formal_0_78) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 30) (select (m_origin formal_0_78) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_79 () FormalMachine (FormalCallback formal_0_78 boundary_0 (select (m_origin formal_0_78) 30) (select (m_origin formal_0_78) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_80 () FormalMachine (FormalWriteFromOrigin formal_0_79 18 30))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_81 () FormalMachine (FormalWriteFromOrigin formal_0_80 29 10))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_81)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 31) (select (m_origin formal_0_81) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 31) (select (m_origin formal_0_81) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_82 () FormalMachine (FormalCallback formal_0_81 boundary_0 (select (m_origin formal_0_81) 31) (select (m_origin formal_0_81) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_83 () FormalMachine (FormalWriteFromOrigin formal_0_82 18 31))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_83)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_83) (select (m_origin formal_0_83) 32) (select (m_origin formal_0_83) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_83) (select (m_origin formal_0_83) 32) (select (m_origin formal_0_83) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_84 () FormalMachine (FormalCallback formal_0_83 boundary_0 (select (m_origin formal_0_83) 32) (select (m_origin formal_0_83) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_85 () FormalMachine (FormalWriteFromOrigin formal_0_84 19 32))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_86 () FormalMachine (FormalWriteFromOrigin formal_0_85 31 19))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_86)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 33) (select (m_origin formal_0_86) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 33) (select (m_origin formal_0_86) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_87 () FormalMachine (FormalCallback formal_0_86 boundary_0 (select (m_origin formal_0_86) 33) (select (m_origin formal_0_86) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_88 () FormalMachine (FormalWriteFromOrigin formal_0_87 19 33))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_88)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_88) (select (m_origin formal_0_88) 34) (select (m_origin formal_0_88) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_88) (select (m_origin formal_0_88) 34) (select (m_origin formal_0_88) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_89 () FormalMachine (FormalCallback formal_0_88 boundary_0 (select (m_origin formal_0_88) 34) (select (m_origin formal_0_88) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_90 () FormalMachine (FormalWriteFromOrigin formal_0_89 20 34))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_91 () FormalMachine (FormalWriteFromOrigin formal_0_90 33 11))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_91)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_91) (select (m_origin formal_0_91) 0) (select (m_origin formal_0_91) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_91) (select (m_origin formal_0_91) 0) (select (m_origin formal_0_91) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_92 () FormalMachine (FormalCallback formal_0_91 boundary_0 (select (m_origin formal_0_91) 0) (select (m_origin formal_0_91) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_93 () FormalMachine (FormalWriteFromOrigin formal_0_92 20 0))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_93)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_93) (select (m_origin formal_0_93) 36) (select (m_origin formal_0_93) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_93) (select (m_origin formal_0_93) 36) (select (m_origin formal_0_93) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_94 () FormalMachine (FormalCallback formal_0_93 boundary_0 (select (m_origin formal_0_93) 36) (select (m_origin formal_0_93) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_95 () FormalMachine (FormalWriteFromOrigin formal_0_94 20 36))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_95)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_95) (select (m_origin formal_0_95) 37) (select (m_origin formal_0_95) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_95) (select (m_origin formal_0_95) 37) (select (m_origin formal_0_95) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_96 () FormalMachine (FormalCallback formal_0_95 boundary_0 (select (m_origin formal_0_95) 37) (select (m_origin formal_0_95) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_97 () FormalMachine (FormalWriteFromOrigin formal_0_96 20 37))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_97)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_97) (select (m_origin formal_0_97) 38) (select (m_origin formal_0_97) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_97) (select (m_origin formal_0_97) 38) (select (m_origin formal_0_97) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_98 () FormalMachine (FormalCallback formal_0_97 boundary_0 (select (m_origin formal_0_97) 38) (select (m_origin formal_0_97) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_99 () FormalMachine (FormalWriteFromOrigin formal_0_98 20 38))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_99)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 39) (select (m_origin formal_0_99) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 39) (select (m_origin formal_0_99) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_100 () FormalMachine (FormalCallback formal_0_99 boundary_0 (select (m_origin formal_0_99) 39) (select (m_origin formal_0_99) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_101 () FormalMachine (FormalWriteFromOrigin formal_0_100 20 39))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_101)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_101) (select (m_origin formal_0_101) 40) (select (m_origin formal_0_101) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_101) (select (m_origin formal_0_101) 40) (select (m_origin formal_0_101) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_102 () FormalMachine (FormalCallback formal_0_101 boundary_0 (select (m_origin formal_0_101) 40) (select (m_origin formal_0_101) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_103 () FormalMachine (FormalWriteFromOrigin formal_0_102 20 40))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_103)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_103) (select (m_origin formal_0_103) 41) (select (m_origin formal_0_103) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_103) (select (m_origin formal_0_103) 41) (select (m_origin formal_0_103) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_104 () FormalMachine (FormalCallback formal_0_103 boundary_0 (select (m_origin formal_0_103) 41) (select (m_origin formal_0_103) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_105 () FormalMachine (FormalWriteFromOrigin formal_0_104 20 41))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_105)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_105) (select (m_origin formal_0_105) 42) (select (m_origin formal_0_105) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_105) (select (m_origin formal_0_105) 42) (select (m_origin formal_0_105) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_106 () FormalMachine (FormalCallback formal_0_105 boundary_0 (select (m_origin formal_0_105) 42) (select (m_origin formal_0_105) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_107 () FormalMachine (FormalWriteFromOrigin formal_0_106 21 42))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_108 () FormalMachine (FormalWriteFromOrigin formal_0_107 41 15))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_108)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_108) (select (m_origin formal_0_108) 43) (select (m_origin formal_0_108) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_108) (select (m_origin formal_0_108) 43) (select (m_origin formal_0_108) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_109 () FormalMachine (FormalCallback formal_0_108 boundary_0 (select (m_origin formal_0_108) 43) (select (m_origin formal_0_108) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_110 () FormalMachine (FormalWriteFromOrigin formal_0_109 21 43))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_110)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_110) (select (m_origin formal_0_110) 44) (select (m_origin formal_0_110) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_110) (select (m_origin formal_0_110) 44) (select (m_origin formal_0_110) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_111 () FormalMachine (FormalCallback formal_0_110 boundary_0 (select (m_origin formal_0_110) 44) (select (m_origin formal_0_110) 35)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_112 () FormalMachine (FormalWriteFromOrigin formal_0_111 22 44))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_113 () FormalMachine (FormalWriteFromOrigin formal_0_112 43 22))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_113)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_113) (select (m_origin formal_0_113) 1) (select (m_origin formal_0_113) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_113) (select (m_origin formal_0_113) 1) (select (m_origin formal_0_113) 35)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_114 () FormalMachine (FormalCallback formal_0_113 boundary_0 (select (m_origin formal_0_113) 1) (select (m_origin formal_0_113) 35)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_115 () FormalMachine (FormalWriteFromOrigin formal_0_114 22 1))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_116 () FormalMachine (FormalSwap formal_0_115 0 22))
; source callback case=cyclic-unroll-one-partition phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_116)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_116) (select (m_origin formal_0_116) 1) (select (m_origin formal_0_116) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_116) (select (m_origin formal_0_116) 1) (select (m_origin formal_0_116) 12)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_117 () FormalMachine (FormalCallback formal_0_116 boundary_0 (select (m_origin formal_0_116) 1) (select (m_origin formal_0_116) 12)))
; source callback case=cyclic-unroll-one-partition phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_117)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_117) (select (m_origin formal_0_117) 1) (select (m_origin formal_0_117) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_117) (select (m_origin formal_0_117) 1) (select (m_origin formal_0_117) 21)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_118 () FormalMachine (FormalCallback formal_0_117 boundary_0 (select (m_origin formal_0_117) 1) (select (m_origin formal_0_117) 21)))
; source callback case=cyclic-unroll-one-partition phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_118)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_118) (select (m_origin formal_0_118) 12) (select (m_origin formal_0_118) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_118) (select (m_origin formal_0_118) 12) (select (m_origin formal_0_118) 21)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_119 () FormalMachine (FormalCallback formal_0_118 boundary_0 (select (m_origin formal_0_118) 12) (select (m_origin formal_0_118) 21)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_120 () FormalMachine (FormalSwap formal_0_119 0 8))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_120)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_120) (select (m_origin formal_0_120) 4) (select (m_origin formal_0_120) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_120) (select (m_origin formal_0_120) 4) (select (m_origin formal_0_120) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_121 () FormalMachine (FormalCallback formal_0_120 boundary_0 (select (m_origin formal_0_120) 4) (select (m_origin formal_0_120) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_122 () FormalMachine (FormalWriteFromOrigin formal_0_121 1 4))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_122)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_122) (select (m_origin formal_0_122) 5) (select (m_origin formal_0_122) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_122) (select (m_origin formal_0_122) 5) (select (m_origin formal_0_122) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_123 () FormalMachine (FormalCallback formal_0_122 boundary_0 (select (m_origin formal_0_122) 5) (select (m_origin formal_0_122) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_124 () FormalMachine (FormalWriteFromOrigin formal_0_123 2 5))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_124)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_124) (select (m_origin formal_0_124) 6) (select (m_origin formal_0_124) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_124) (select (m_origin formal_0_124) 6) (select (m_origin formal_0_124) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_125 () FormalMachine (FormalCallback formal_0_124 boundary_0 (select (m_origin formal_0_124) 6) (select (m_origin formal_0_124) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_126 () FormalMachine (FormalWriteFromOrigin formal_0_125 2 6))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_126)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_126) (select (m_origin formal_0_126) 7) (select (m_origin formal_0_126) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_126) (select (m_origin formal_0_126) 7) (select (m_origin formal_0_126) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_127 () FormalMachine (FormalCallback formal_0_126 boundary_0 (select (m_origin formal_0_126) 7) (select (m_origin formal_0_126) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_128 () FormalMachine (FormalWriteFromOrigin formal_0_127 2 7))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_128)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 8) (select (m_origin formal_0_128) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 8) (select (m_origin formal_0_128) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_129 () FormalMachine (FormalCallback formal_0_128 boundary_0 (select (m_origin formal_0_128) 8) (select (m_origin formal_0_128) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_130 () FormalMachine (FormalWriteFromOrigin formal_0_129 3 8))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_131 () FormalMachine (FormalWriteFromOrigin formal_0_130 5 5))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_131)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_131) (select (m_origin formal_0_131) 9) (select (m_origin formal_0_131) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_131) (select (m_origin formal_0_131) 9) (select (m_origin formal_0_131) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_132 () FormalMachine (FormalCallback formal_0_131 boundary_0 (select (m_origin formal_0_131) 9) (select (m_origin formal_0_131) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_133 () FormalMachine (FormalWriteFromOrigin formal_0_132 4 9))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_134 () FormalMachine (FormalWriteFromOrigin formal_0_133 6 6))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_134)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_134) (select (m_origin formal_0_134) 1) (select (m_origin formal_0_134) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_134) (select (m_origin formal_0_134) 1) (select (m_origin formal_0_134) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_135 () FormalMachine (FormalCallback formal_0_134 boundary_0 (select (m_origin formal_0_134) 1) (select (m_origin formal_0_134) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_136 () FormalMachine (FormalWriteFromOrigin formal_0_135 5 1))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_137 () FormalMachine (FormalWriteFromOrigin formal_0_136 7 5))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_137)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_137) (select (m_origin formal_0_137) 13) (select (m_origin formal_0_137) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_137) (select (m_origin formal_0_137) 13) (select (m_origin formal_0_137) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_138 () FormalMachine (FormalCallback formal_0_137 boundary_0 (select (m_origin formal_0_137) 13) (select (m_origin formal_0_137) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_139 () FormalMachine (FormalWriteFromOrigin formal_0_138 6 13))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_140 () FormalMachine (FormalWriteFromOrigin formal_0_139 8 6))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_140)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_140) (select (m_origin formal_0_140) 14) (select (m_origin formal_0_140) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_140) (select (m_origin formal_0_140) 14) (select (m_origin formal_0_140) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_141 () FormalMachine (FormalCallback formal_0_140 boundary_0 (select (m_origin formal_0_140) 14) (select (m_origin formal_0_140) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_142 () FormalMachine (FormalWriteFromOrigin formal_0_141 7 14))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_143 () FormalMachine (FormalWriteFromOrigin formal_0_142 9 5))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_143)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_143) (select (m_origin formal_0_143) 17) (select (m_origin formal_0_143) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_143) (select (m_origin formal_0_143) 17) (select (m_origin formal_0_143) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_144 () FormalMachine (FormalCallback formal_0_143 boundary_0 (select (m_origin formal_0_143) 17) (select (m_origin formal_0_143) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_145 () FormalMachine (FormalWriteFromOrigin formal_0_144 8 17))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_146 () FormalMachine (FormalWriteFromOrigin formal_0_145 10 6))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_146)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_146) (select (m_origin formal_0_146) 18) (select (m_origin formal_0_146) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_146) (select (m_origin formal_0_146) 18) (select (m_origin formal_0_146) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_147 () FormalMachine (FormalCallback formal_0_146 boundary_0 (select (m_origin formal_0_146) 18) (select (m_origin formal_0_146) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_148 () FormalMachine (FormalWriteFromOrigin formal_0_147 9 18))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_149 () FormalMachine (FormalWriteFromOrigin formal_0_148 11 5))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_149)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_149) (select (m_origin formal_0_149) 20) (select (m_origin formal_0_149) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_149) (select (m_origin formal_0_149) 20) (select (m_origin formal_0_149) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_150 () FormalMachine (FormalCallback formal_0_149 boundary_0 (select (m_origin formal_0_149) 20) (select (m_origin formal_0_149) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_151 () FormalMachine (FormalWriteFromOrigin formal_0_150 10 20))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_152 () FormalMachine (FormalWriteFromOrigin formal_0_151 12 6))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_152)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_152) (select (m_origin formal_0_152) 21) (select (m_origin formal_0_152) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_152) (select (m_origin formal_0_152) 21) (select (m_origin formal_0_152) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_153 () FormalMachine (FormalCallback formal_0_152 boundary_0 (select (m_origin formal_0_152) 21) (select (m_origin formal_0_152) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_154 () FormalMachine (FormalWriteFromOrigin formal_0_153 11 21))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_155 () FormalMachine (FormalWriteFromOrigin formal_0_154 13 5))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_155)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 24) (select (m_origin formal_0_155) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 24) (select (m_origin formal_0_155) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_156 () FormalMachine (FormalCallback formal_0_155 boundary_0 (select (m_origin formal_0_155) 24) (select (m_origin formal_0_155) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_157 () FormalMachine (FormalWriteFromOrigin formal_0_156 11 24))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_157)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_157) (select (m_origin formal_0_157) 28) (select (m_origin formal_0_157) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_157) (select (m_origin formal_0_157) 28) (select (m_origin formal_0_157) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_158 () FormalMachine (FormalCallback formal_0_157 boundary_0 (select (m_origin formal_0_157) 28) (select (m_origin formal_0_157) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_159 () FormalMachine (FormalWriteFromOrigin formal_0_158 11 28))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_159)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_159) (select (m_origin formal_0_159) 29) (select (m_origin formal_0_159) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_159) (select (m_origin formal_0_159) 29) (select (m_origin formal_0_159) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_160 () FormalMachine (FormalCallback formal_0_159 boundary_0 (select (m_origin formal_0_159) 29) (select (m_origin formal_0_159) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_161 () FormalMachine (FormalWriteFromOrigin formal_0_160 11 29))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_161)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_161) (select (m_origin formal_0_161) 31) (select (m_origin formal_0_161) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_161) (select (m_origin formal_0_161) 31) (select (m_origin formal_0_161) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_162 () FormalMachine (FormalCallback formal_0_161 boundary_0 (select (m_origin formal_0_161) 31) (select (m_origin formal_0_161) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_163 () FormalMachine (FormalWriteFromOrigin formal_0_162 12 31))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_164 () FormalMachine (FormalWriteFromOrigin formal_0_163 17 6))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_164)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_164) (select (m_origin formal_0_164) 33) (select (m_origin formal_0_164) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_164) (select (m_origin formal_0_164) 33) (select (m_origin formal_0_164) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_165 () FormalMachine (FormalCallback formal_0_164 boundary_0 (select (m_origin formal_0_164) 33) (select (m_origin formal_0_164) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_166 () FormalMachine (FormalWriteFromOrigin formal_0_165 13 33))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_167 () FormalMachine (FormalWriteFromOrigin formal_0_166 18 5))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_167)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_167) (select (m_origin formal_0_167) 41) (select (m_origin formal_0_167) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_167) (select (m_origin formal_0_167) 41) (select (m_origin formal_0_167) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_168 () FormalMachine (FormalCallback formal_0_167 boundary_0 (select (m_origin formal_0_167) 41) (select (m_origin formal_0_167) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_169 () FormalMachine (FormalWriteFromOrigin formal_0_168 13 41))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_169)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_169) (select (m_origin formal_0_169) 43) (select (m_origin formal_0_169) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_169) (select (m_origin formal_0_169) 43) (select (m_origin formal_0_169) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_170 () FormalMachine (FormalCallback formal_0_169 boundary_0 (select (m_origin formal_0_169) 43) (select (m_origin formal_0_169) 12)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_171 () FormalMachine (FormalWriteFromOrigin formal_0_170 14 43))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_172 () FormalMachine (FormalWriteFromOrigin formal_0_171 20 21))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_172)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_172) (select (m_origin formal_0_172) 3) (select (m_origin formal_0_172) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_172) (select (m_origin formal_0_172) 3) (select (m_origin formal_0_172) 12)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_173 () FormalMachine (FormalCallback formal_0_172 boundary_0 (select (m_origin formal_0_172) 3) (select (m_origin formal_0_172) 12)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_174 () FormalMachine (FormalWriteFromOrigin formal_0_173 15 3))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_175 () FormalMachine (FormalWriteFromOrigin formal_0_174 21 24))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_176 () FormalMachine (FormalSwap formal_0_175 0 15))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:1]:initial-compare
(assert (not (m_panicked formal_0_176)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 4) (select (m_origin formal_0_176) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 4) (select (m_origin formal_0_176) 3)) false))
; source callback transition phase=insert-tail[0:15:1]:initial-compare
(define-fun formal_0_177 () FormalMachine (FormalCallback formal_0_176 boundary_0 (select (m_origin formal_0_176) 4) (select (m_origin formal_0_176) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:1]
(define-fun formal_0_178 () FormalMachine (FormalWriteFromOrigin formal_0_177 1 3))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:1]
(define-fun formal_0_179 () FormalMachine (FormalWriteFromOrigin formal_0_178 0 4))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:2]:initial-compare
(assert (not (m_panicked formal_0_179)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_179) (select (m_origin formal_0_179) 7) (select (m_origin formal_0_179) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_179) (select (m_origin formal_0_179) 7) (select (m_origin formal_0_179) 3)) false))
; source callback transition phase=insert-tail[0:15:2]:initial-compare
(define-fun formal_0_180 () FormalMachine (FormalCallback formal_0_179 boundary_0 (select (m_origin formal_0_179) 7) (select (m_origin formal_0_179) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:2]
(define-fun formal_0_181 () FormalMachine (FormalWriteFromOrigin formal_0_180 2 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:2]:sift-compare
(assert (not (m_panicked formal_0_181)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_181) (select (m_origin formal_0_181) 7) (select (m_origin formal_0_181) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_181) (select (m_origin formal_0_181) 7) (select (m_origin formal_0_181) 4)) false))
; source callback transition phase=insert-tail[0:15:2]:sift-compare
(define-fun formal_0_182 () FormalMachine (FormalCallback formal_0_181 boundary_0 (select (m_origin formal_0_181) 7) (select (m_origin formal_0_181) 4)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:2]
(define-fun formal_0_183 () FormalMachine (FormalWriteFromOrigin formal_0_182 1 7))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:3]:initial-compare
(assert (not (m_panicked formal_0_183)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_183) (select (m_origin formal_0_183) 8) (select (m_origin formal_0_183) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_183) (select (m_origin formal_0_183) 8) (select (m_origin formal_0_183) 3)) false))
; source callback transition phase=insert-tail[0:15:3]:initial-compare
(define-fun formal_0_184 () FormalMachine (FormalCallback formal_0_183 boundary_0 (select (m_origin formal_0_183) 8) (select (m_origin formal_0_183) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:3]
(define-fun formal_0_185 () FormalMachine (FormalWriteFromOrigin formal_0_184 3 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:3]:sift-compare
(assert (not (m_panicked formal_0_185)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_185) (select (m_origin formal_0_185) 8) (select (m_origin formal_0_185) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_185) (select (m_origin formal_0_185) 8) (select (m_origin formal_0_185) 7)) false))
; source callback transition phase=insert-tail[0:15:3]:sift-compare
(define-fun formal_0_186 () FormalMachine (FormalCallback formal_0_185 boundary_0 (select (m_origin formal_0_185) 8) (select (m_origin formal_0_185) 7)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:3]
(define-fun formal_0_187 () FormalMachine (FormalWriteFromOrigin formal_0_186 2 8))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:4]:initial-compare
(assert (not (m_panicked formal_0_187)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_187) (select (m_origin formal_0_187) 9) (select (m_origin formal_0_187) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_187) (select (m_origin formal_0_187) 9) (select (m_origin formal_0_187) 3)) false))
; source callback transition phase=insert-tail[0:15:4]:initial-compare
(define-fun formal_0_188 () FormalMachine (FormalCallback formal_0_187 boundary_0 (select (m_origin formal_0_187) 9) (select (m_origin formal_0_187) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:4]
(define-fun formal_0_189 () FormalMachine (FormalWriteFromOrigin formal_0_188 4 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:4]:sift-compare
(assert (not (m_panicked formal_0_189)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_189) (select (m_origin formal_0_189) 9) (select (m_origin formal_0_189) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_189) (select (m_origin formal_0_189) 9) (select (m_origin formal_0_189) 8)) false))
; source callback transition phase=insert-tail[0:15:4]:sift-compare
(define-fun formal_0_190 () FormalMachine (FormalCallback formal_0_189 boundary_0 (select (m_origin formal_0_189) 9) (select (m_origin formal_0_189) 8)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:4]
(define-fun formal_0_191 () FormalMachine (FormalWriteFromOrigin formal_0_190 3 8))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:4]:sift-compare
(assert (not (m_panicked formal_0_191)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_191) (select (m_origin formal_0_191) 9) (select (m_origin formal_0_191) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_191) (select (m_origin formal_0_191) 9) (select (m_origin formal_0_191) 7)) false))
; source callback transition phase=insert-tail[0:15:4]:sift-compare
(define-fun formal_0_192 () FormalMachine (FormalCallback formal_0_191 boundary_0 (select (m_origin formal_0_191) 9) (select (m_origin formal_0_191) 7)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:4]
(define-fun formal_0_193 () FormalMachine (FormalWriteFromOrigin formal_0_192 2 7))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:4]:sift-compare
(assert (not (m_panicked formal_0_193)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_193) (select (m_origin formal_0_193) 9) (select (m_origin formal_0_193) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_193) (select (m_origin formal_0_193) 9) (select (m_origin formal_0_193) 4)) false))
; source callback transition phase=insert-tail[0:15:4]:sift-compare
(define-fun formal_0_194 () FormalMachine (FormalCallback formal_0_193 boundary_0 (select (m_origin formal_0_193) 9) (select (m_origin formal_0_193) 4)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:4]
(define-fun formal_0_195 () FormalMachine (FormalWriteFromOrigin formal_0_194 1 9))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:5]:initial-compare
(assert (not (m_panicked formal_0_195)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_195) (select (m_origin formal_0_195) 1) (select (m_origin formal_0_195) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_195) (select (m_origin formal_0_195) 1) (select (m_origin formal_0_195) 3)) false))
; source callback transition phase=insert-tail[0:15:5]:initial-compare
(define-fun formal_0_196 () FormalMachine (FormalCallback formal_0_195 boundary_0 (select (m_origin formal_0_195) 1) (select (m_origin formal_0_195) 3)))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:6]:initial-compare
(assert (not (m_panicked formal_0_196)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_196) (select (m_origin formal_0_196) 13) (select (m_origin formal_0_196) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_196) (select (m_origin formal_0_196) 13) (select (m_origin formal_0_196) 1)) false))
; source callback transition phase=insert-tail[0:15:6]:initial-compare
(define-fun formal_0_197 () FormalMachine (FormalCallback formal_0_196 boundary_0 (select (m_origin formal_0_196) 13) (select (m_origin formal_0_196) 1)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:6]
(define-fun formal_0_198 () FormalMachine (FormalWriteFromOrigin formal_0_197 6 1))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:6]:sift-compare
(assert (not (m_panicked formal_0_198)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_198) (select (m_origin formal_0_198) 13) (select (m_origin formal_0_198) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_198) (select (m_origin formal_0_198) 13) (select (m_origin formal_0_198) 3)) false))
; source callback transition phase=insert-tail[0:15:6]:sift-compare
(define-fun formal_0_199 () FormalMachine (FormalCallback formal_0_198 boundary_0 (select (m_origin formal_0_198) 13) (select (m_origin formal_0_198) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:6]
(define-fun formal_0_200 () FormalMachine (FormalWriteFromOrigin formal_0_199 5 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:6]:sift-compare
(assert (not (m_panicked formal_0_200)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_200) (select (m_origin formal_0_200) 13) (select (m_origin formal_0_200) 8)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_200) (select (m_origin formal_0_200) 13) (select (m_origin formal_0_200) 8)) false))
; source callback transition phase=insert-tail[0:15:6]:sift-compare
(define-fun formal_0_201 () FormalMachine (FormalCallback formal_0_200 boundary_0 (select (m_origin formal_0_200) 13) (select (m_origin formal_0_200) 8)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:6]
(define-fun formal_0_202 () FormalMachine (FormalWriteFromOrigin formal_0_201 4 13))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:7]:initial-compare
(assert (not (m_panicked formal_0_202)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_202) (select (m_origin formal_0_202) 14) (select (m_origin formal_0_202) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_202) (select (m_origin formal_0_202) 14) (select (m_origin formal_0_202) 1)) false))
; source callback transition phase=insert-tail[0:15:7]:initial-compare
(define-fun formal_0_203 () FormalMachine (FormalCallback formal_0_202 boundary_0 (select (m_origin formal_0_202) 14) (select (m_origin formal_0_202) 1)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:7]
(define-fun formal_0_204 () FormalMachine (FormalWriteFromOrigin formal_0_203 7 1))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:7]:sift-compare
(assert (not (m_panicked formal_0_204)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_204) (select (m_origin formal_0_204) 14) (select (m_origin formal_0_204) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_204) (select (m_origin formal_0_204) 14) (select (m_origin formal_0_204) 3)) false))
; source callback transition phase=insert-tail[0:15:7]:sift-compare
(define-fun formal_0_205 () FormalMachine (FormalCallback formal_0_204 boundary_0 (select (m_origin formal_0_204) 14) (select (m_origin formal_0_204) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:7]
(define-fun formal_0_206 () FormalMachine (FormalWriteFromOrigin formal_0_205 6 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:7]:sift-compare
(assert (not (m_panicked formal_0_206)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_206) (select (m_origin formal_0_206) 14) (select (m_origin formal_0_206) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_206) (select (m_origin formal_0_206) 14) (select (m_origin formal_0_206) 13)) false))
; source callback transition phase=insert-tail[0:15:7]:sift-compare
(define-fun formal_0_207 () FormalMachine (FormalCallback formal_0_206 boundary_0 (select (m_origin formal_0_206) 14) (select (m_origin formal_0_206) 13)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:7]
(define-fun formal_0_208 () FormalMachine (FormalWriteFromOrigin formal_0_207 5 13))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:7]:sift-compare
(assert (not (m_panicked formal_0_208)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_208) (select (m_origin formal_0_208) 14) (select (m_origin formal_0_208) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_208) (select (m_origin formal_0_208) 14) (select (m_origin formal_0_208) 8)) false))
; source callback transition phase=insert-tail[0:15:7]:sift-compare
(define-fun formal_0_209 () FormalMachine (FormalCallback formal_0_208 boundary_0 (select (m_origin formal_0_208) 14) (select (m_origin formal_0_208) 8)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:7]
(define-fun formal_0_210 () FormalMachine (FormalWriteFromOrigin formal_0_209 4 8))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:7]:sift-compare
(assert (not (m_panicked formal_0_210)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_210) (select (m_origin formal_0_210) 14) (select (m_origin formal_0_210) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_210) (select (m_origin formal_0_210) 14) (select (m_origin formal_0_210) 7)) false))
; source callback transition phase=insert-tail[0:15:7]:sift-compare
(define-fun formal_0_211 () FormalMachine (FormalCallback formal_0_210 boundary_0 (select (m_origin formal_0_210) 14) (select (m_origin formal_0_210) 7)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:7]
(define-fun formal_0_212 () FormalMachine (FormalWriteFromOrigin formal_0_211 3 7))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:7]:sift-compare
(assert (not (m_panicked formal_0_212)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_212) (select (m_origin formal_0_212) 14) (select (m_origin formal_0_212) 9)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_212) (select (m_origin formal_0_212) 14) (select (m_origin formal_0_212) 9)) false))
; source callback transition phase=insert-tail[0:15:7]:sift-compare
(define-fun formal_0_213 () FormalMachine (FormalCallback formal_0_212 boundary_0 (select (m_origin formal_0_212) 14) (select (m_origin formal_0_212) 9)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:7]
(define-fun formal_0_214 () FormalMachine (FormalWriteFromOrigin formal_0_213 2 14))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:8]:initial-compare
(assert (not (m_panicked formal_0_214)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_214) (select (m_origin formal_0_214) 17) (select (m_origin formal_0_214) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_214) (select (m_origin formal_0_214) 17) (select (m_origin formal_0_214) 1)) false))
; source callback transition phase=insert-tail[0:15:8]:initial-compare
(define-fun formal_0_215 () FormalMachine (FormalCallback formal_0_214 boundary_0 (select (m_origin formal_0_214) 17) (select (m_origin formal_0_214) 1)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:8]
(define-fun formal_0_216 () FormalMachine (FormalWriteFromOrigin formal_0_215 8 1))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:8]:sift-compare
(assert (not (m_panicked formal_0_216)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_216) (select (m_origin formal_0_216) 17) (select (m_origin formal_0_216) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_216) (select (m_origin formal_0_216) 17) (select (m_origin formal_0_216) 3)) false))
; source callback transition phase=insert-tail[0:15:8]:sift-compare
(define-fun formal_0_217 () FormalMachine (FormalCallback formal_0_216 boundary_0 (select (m_origin formal_0_216) 17) (select (m_origin formal_0_216) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:8]
(define-fun formal_0_218 () FormalMachine (FormalWriteFromOrigin formal_0_217 7 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:8]:sift-compare
(assert (not (m_panicked formal_0_218)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_218) (select (m_origin formal_0_218) 17) (select (m_origin formal_0_218) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_218) (select (m_origin formal_0_218) 17) (select (m_origin formal_0_218) 13)) false))
; source callback transition phase=insert-tail[0:15:8]:sift-compare
(define-fun formal_0_219 () FormalMachine (FormalCallback formal_0_218 boundary_0 (select (m_origin formal_0_218) 17) (select (m_origin formal_0_218) 13)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:8]
(define-fun formal_0_220 () FormalMachine (FormalWriteFromOrigin formal_0_219 6 13))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:8]:sift-compare
(assert (not (m_panicked formal_0_220)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_220) (select (m_origin formal_0_220) 17) (select (m_origin formal_0_220) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_220) (select (m_origin formal_0_220) 17) (select (m_origin formal_0_220) 8)) false))
; source callback transition phase=insert-tail[0:15:8]:sift-compare
(define-fun formal_0_221 () FormalMachine (FormalCallback formal_0_220 boundary_0 (select (m_origin formal_0_220) 17) (select (m_origin formal_0_220) 8)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:8]
(define-fun formal_0_222 () FormalMachine (FormalWriteFromOrigin formal_0_221 5 8))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:8]:sift-compare
(assert (not (m_panicked formal_0_222)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_222) (select (m_origin formal_0_222) 17) (select (m_origin formal_0_222) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_222) (select (m_origin formal_0_222) 17) (select (m_origin formal_0_222) 7)) false))
; source callback transition phase=insert-tail[0:15:8]:sift-compare
(define-fun formal_0_223 () FormalMachine (FormalCallback formal_0_222 boundary_0 (select (m_origin formal_0_222) 17) (select (m_origin formal_0_222) 7)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:8]
(define-fun formal_0_224 () FormalMachine (FormalWriteFromOrigin formal_0_223 4 7))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:8]:sift-compare
(assert (not (m_panicked formal_0_224)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_224) (select (m_origin formal_0_224) 17) (select (m_origin formal_0_224) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_224) (select (m_origin formal_0_224) 17) (select (m_origin formal_0_224) 14)) false))
; source callback transition phase=insert-tail[0:15:8]:sift-compare
(define-fun formal_0_225 () FormalMachine (FormalCallback formal_0_224 boundary_0 (select (m_origin formal_0_224) 17) (select (m_origin formal_0_224) 14)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:8]
(define-fun formal_0_226 () FormalMachine (FormalWriteFromOrigin formal_0_225 3 14))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:8]:sift-compare
(assert (not (m_panicked formal_0_226)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_226) (select (m_origin formal_0_226) 17) (select (m_origin formal_0_226) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_226) (select (m_origin formal_0_226) 17) (select (m_origin formal_0_226) 9)) false))
; source callback transition phase=insert-tail[0:15:8]:sift-compare
(define-fun formal_0_227 () FormalMachine (FormalCallback formal_0_226 boundary_0 (select (m_origin formal_0_226) 17) (select (m_origin formal_0_226) 9)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:8]
(define-fun formal_0_228 () FormalMachine (FormalWriteFromOrigin formal_0_227 2 9))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:8]:sift-compare
(assert (not (m_panicked formal_0_228)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_228) (select (m_origin formal_0_228) 17) (select (m_origin formal_0_228) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_228) (select (m_origin formal_0_228) 17) (select (m_origin formal_0_228) 4)) false))
; source callback transition phase=insert-tail[0:15:8]:sift-compare
(define-fun formal_0_229 () FormalMachine (FormalCallback formal_0_228 boundary_0 (select (m_origin formal_0_228) 17) (select (m_origin formal_0_228) 4)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:8]
(define-fun formal_0_230 () FormalMachine (FormalWriteFromOrigin formal_0_229 1 17))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:9]:initial-compare
(assert (not (m_panicked formal_0_230)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_230) (select (m_origin formal_0_230) 18) (select (m_origin formal_0_230) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_230) (select (m_origin formal_0_230) 18) (select (m_origin formal_0_230) 1)) false))
; source callback transition phase=insert-tail[0:15:9]:initial-compare
(define-fun formal_0_231 () FormalMachine (FormalCallback formal_0_230 boundary_0 (select (m_origin formal_0_230) 18) (select (m_origin formal_0_230) 1)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:9]
(define-fun formal_0_232 () FormalMachine (FormalWriteFromOrigin formal_0_231 9 1))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:9]:sift-compare
(assert (not (m_panicked formal_0_232)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_232) (select (m_origin formal_0_232) 18) (select (m_origin formal_0_232) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_232) (select (m_origin formal_0_232) 18) (select (m_origin formal_0_232) 3)) false))
; source callback transition phase=insert-tail[0:15:9]:sift-compare
(define-fun formal_0_233 () FormalMachine (FormalCallback formal_0_232 boundary_0 (select (m_origin formal_0_232) 18) (select (m_origin formal_0_232) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:9]
(define-fun formal_0_234 () FormalMachine (FormalWriteFromOrigin formal_0_233 8 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:9]:sift-compare
(assert (not (m_panicked formal_0_234)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_234) (select (m_origin formal_0_234) 18) (select (m_origin formal_0_234) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_234) (select (m_origin formal_0_234) 18) (select (m_origin formal_0_234) 13)) false))
; source callback transition phase=insert-tail[0:15:9]:sift-compare
(define-fun formal_0_235 () FormalMachine (FormalCallback formal_0_234 boundary_0 (select (m_origin formal_0_234) 18) (select (m_origin formal_0_234) 13)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:9]
(define-fun formal_0_236 () FormalMachine (FormalWriteFromOrigin formal_0_235 7 13))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:9]:sift-compare
(assert (not (m_panicked formal_0_236)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_236) (select (m_origin formal_0_236) 18) (select (m_origin formal_0_236) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_236) (select (m_origin formal_0_236) 18) (select (m_origin formal_0_236) 8)) false))
; source callback transition phase=insert-tail[0:15:9]:sift-compare
(define-fun formal_0_237 () FormalMachine (FormalCallback formal_0_236 boundary_0 (select (m_origin formal_0_236) 18) (select (m_origin formal_0_236) 8)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:9]
(define-fun formal_0_238 () FormalMachine (FormalWriteFromOrigin formal_0_237 6 8))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:9]:sift-compare
(assert (not (m_panicked formal_0_238)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_238) (select (m_origin formal_0_238) 18) (select (m_origin formal_0_238) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_238) (select (m_origin formal_0_238) 18) (select (m_origin formal_0_238) 7)) false))
; source callback transition phase=insert-tail[0:15:9]:sift-compare
(define-fun formal_0_239 () FormalMachine (FormalCallback formal_0_238 boundary_0 (select (m_origin formal_0_238) 18) (select (m_origin formal_0_238) 7)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:9]
(define-fun formal_0_240 () FormalMachine (FormalWriteFromOrigin formal_0_239 5 7))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:9]:sift-compare
(assert (not (m_panicked formal_0_240)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_240) (select (m_origin formal_0_240) 18) (select (m_origin formal_0_240) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_240) (select (m_origin formal_0_240) 18) (select (m_origin formal_0_240) 14)) false))
; source callback transition phase=insert-tail[0:15:9]:sift-compare
(define-fun formal_0_241 () FormalMachine (FormalCallback formal_0_240 boundary_0 (select (m_origin formal_0_240) 18) (select (m_origin formal_0_240) 14)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:9]
(define-fun formal_0_242 () FormalMachine (FormalWriteFromOrigin formal_0_241 4 14))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:9]:sift-compare
(assert (not (m_panicked formal_0_242)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_242) (select (m_origin formal_0_242) 18) (select (m_origin formal_0_242) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_242) (select (m_origin formal_0_242) 18) (select (m_origin formal_0_242) 9)) false))
; source callback transition phase=insert-tail[0:15:9]:sift-compare
(define-fun formal_0_243 () FormalMachine (FormalCallback formal_0_242 boundary_0 (select (m_origin formal_0_242) 18) (select (m_origin formal_0_242) 9)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:9]
(define-fun formal_0_244 () FormalMachine (FormalWriteFromOrigin formal_0_243 3 9))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:9]:sift-compare
(assert (not (m_panicked formal_0_244)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_244) (select (m_origin formal_0_244) 18) (select (m_origin formal_0_244) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_244) (select (m_origin formal_0_244) 18) (select (m_origin formal_0_244) 17)) false))
; source callback transition phase=insert-tail[0:15:9]:sift-compare
(define-fun formal_0_245 () FormalMachine (FormalCallback formal_0_244 boundary_0 (select (m_origin formal_0_244) 18) (select (m_origin formal_0_244) 17)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:9]
(define-fun formal_0_246 () FormalMachine (FormalWriteFromOrigin formal_0_245 2 17))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:9]:sift-compare
(assert (not (m_panicked formal_0_246)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_246) (select (m_origin formal_0_246) 18) (select (m_origin formal_0_246) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_246) (select (m_origin formal_0_246) 18) (select (m_origin formal_0_246) 4)) false))
; source callback transition phase=insert-tail[0:15:9]:sift-compare
(define-fun formal_0_247 () FormalMachine (FormalCallback formal_0_246 boundary_0 (select (m_origin formal_0_246) 18) (select (m_origin formal_0_246) 4)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:9]
(define-fun formal_0_248 () FormalMachine (FormalWriteFromOrigin formal_0_247 1 18))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:10]:initial-compare
(assert (not (m_panicked formal_0_248)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_248) (select (m_origin formal_0_248) 20) (select (m_origin formal_0_248) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_248) (select (m_origin formal_0_248) 20) (select (m_origin formal_0_248) 1)) false))
; source callback transition phase=insert-tail[0:15:10]:initial-compare
(define-fun formal_0_249 () FormalMachine (FormalCallback formal_0_248 boundary_0 (select (m_origin formal_0_248) 20) (select (m_origin formal_0_248) 1)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:10]
(define-fun formal_0_250 () FormalMachine (FormalWriteFromOrigin formal_0_249 10 1))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:10]:sift-compare
(assert (not (m_panicked formal_0_250)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_250) (select (m_origin formal_0_250) 20) (select (m_origin formal_0_250) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_250) (select (m_origin formal_0_250) 20) (select (m_origin formal_0_250) 3)) false))
; source callback transition phase=insert-tail[0:15:10]:sift-compare
(define-fun formal_0_251 () FormalMachine (FormalCallback formal_0_250 boundary_0 (select (m_origin formal_0_250) 20) (select (m_origin formal_0_250) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:10]
(define-fun formal_0_252 () FormalMachine (FormalWriteFromOrigin formal_0_251 9 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:10]:sift-compare
(assert (not (m_panicked formal_0_252)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_252) (select (m_origin formal_0_252) 20) (select (m_origin formal_0_252) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_252) (select (m_origin formal_0_252) 20) (select (m_origin formal_0_252) 13)) false))
; source callback transition phase=insert-tail[0:15:10]:sift-compare
(define-fun formal_0_253 () FormalMachine (FormalCallback formal_0_252 boundary_0 (select (m_origin formal_0_252) 20) (select (m_origin formal_0_252) 13)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:10]
(define-fun formal_0_254 () FormalMachine (FormalWriteFromOrigin formal_0_253 8 13))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:10]:sift-compare
(assert (not (m_panicked formal_0_254)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_254) (select (m_origin formal_0_254) 20) (select (m_origin formal_0_254) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_254) (select (m_origin formal_0_254) 20) (select (m_origin formal_0_254) 8)) false))
; source callback transition phase=insert-tail[0:15:10]:sift-compare
(define-fun formal_0_255 () FormalMachine (FormalCallback formal_0_254 boundary_0 (select (m_origin formal_0_254) 20) (select (m_origin formal_0_254) 8)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:10]
(define-fun formal_0_256 () FormalMachine (FormalWriteFromOrigin formal_0_255 7 8))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:10]:sift-compare
(assert (not (m_panicked formal_0_256)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_256) (select (m_origin formal_0_256) 20) (select (m_origin formal_0_256) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_256) (select (m_origin formal_0_256) 20) (select (m_origin formal_0_256) 7)) false))
; source callback transition phase=insert-tail[0:15:10]:sift-compare
(define-fun formal_0_257 () FormalMachine (FormalCallback formal_0_256 boundary_0 (select (m_origin formal_0_256) 20) (select (m_origin formal_0_256) 7)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:10]
(define-fun formal_0_258 () FormalMachine (FormalWriteFromOrigin formal_0_257 6 7))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:10]:sift-compare
(assert (not (m_panicked formal_0_258)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_258) (select (m_origin formal_0_258) 20) (select (m_origin formal_0_258) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_258) (select (m_origin formal_0_258) 20) (select (m_origin formal_0_258) 14)) false))
; source callback transition phase=insert-tail[0:15:10]:sift-compare
(define-fun formal_0_259 () FormalMachine (FormalCallback formal_0_258 boundary_0 (select (m_origin formal_0_258) 20) (select (m_origin formal_0_258) 14)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:10]
(define-fun formal_0_260 () FormalMachine (FormalWriteFromOrigin formal_0_259 5 14))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:10]:sift-compare
(assert (not (m_panicked formal_0_260)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_260) (select (m_origin formal_0_260) 20) (select (m_origin formal_0_260) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_260) (select (m_origin formal_0_260) 20) (select (m_origin formal_0_260) 9)) false))
; source callback transition phase=insert-tail[0:15:10]:sift-compare
(define-fun formal_0_261 () FormalMachine (FormalCallback formal_0_260 boundary_0 (select (m_origin formal_0_260) 20) (select (m_origin formal_0_260) 9)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:10]
(define-fun formal_0_262 () FormalMachine (FormalWriteFromOrigin formal_0_261 4 9))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:10]:sift-compare
(assert (not (m_panicked formal_0_262)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_262) (select (m_origin formal_0_262) 20) (select (m_origin formal_0_262) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_262) (select (m_origin formal_0_262) 20) (select (m_origin formal_0_262) 17)) false))
; source callback transition phase=insert-tail[0:15:10]:sift-compare
(define-fun formal_0_263 () FormalMachine (FormalCallback formal_0_262 boundary_0 (select (m_origin formal_0_262) 20) (select (m_origin formal_0_262) 17)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:10]
(define-fun formal_0_264 () FormalMachine (FormalWriteFromOrigin formal_0_263 3 17))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:10]:sift-compare
(assert (not (m_panicked formal_0_264)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_264) (select (m_origin formal_0_264) 20) (select (m_origin formal_0_264) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_264) (select (m_origin formal_0_264) 20) (select (m_origin formal_0_264) 18)) false))
; source callback transition phase=insert-tail[0:15:10]:sift-compare
(define-fun formal_0_265 () FormalMachine (FormalCallback formal_0_264 boundary_0 (select (m_origin formal_0_264) 20) (select (m_origin formal_0_264) 18)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:10]
(define-fun formal_0_266 () FormalMachine (FormalWriteFromOrigin formal_0_265 2 18))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:10]:sift-compare
(assert (not (m_panicked formal_0_266)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_266) (select (m_origin formal_0_266) 20) (select (m_origin formal_0_266) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_266) (select (m_origin formal_0_266) 20) (select (m_origin formal_0_266) 4)) false))
; source callback transition phase=insert-tail[0:15:10]:sift-compare
(define-fun formal_0_267 () FormalMachine (FormalCallback formal_0_266 boundary_0 (select (m_origin formal_0_266) 20) (select (m_origin formal_0_266) 4)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:10]
(define-fun formal_0_268 () FormalMachine (FormalWriteFromOrigin formal_0_267 1 20))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:11]:initial-compare
(assert (not (m_panicked formal_0_268)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_268) (select (m_origin formal_0_268) 29) (select (m_origin formal_0_268) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_268) (select (m_origin formal_0_268) 29) (select (m_origin formal_0_268) 1)) false))
; source callback transition phase=insert-tail[0:15:11]:initial-compare
(define-fun formal_0_269 () FormalMachine (FormalCallback formal_0_268 boundary_0 (select (m_origin formal_0_268) 29) (select (m_origin formal_0_268) 1)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:11]
(define-fun formal_0_270 () FormalMachine (FormalWriteFromOrigin formal_0_269 11 1))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:11]:sift-compare
(assert (not (m_panicked formal_0_270)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_270) (select (m_origin formal_0_270) 29) (select (m_origin formal_0_270) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_270) (select (m_origin formal_0_270) 29) (select (m_origin formal_0_270) 3)) false))
; source callback transition phase=insert-tail[0:15:11]:sift-compare
(define-fun formal_0_271 () FormalMachine (FormalCallback formal_0_270 boundary_0 (select (m_origin formal_0_270) 29) (select (m_origin formal_0_270) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:11]
(define-fun formal_0_272 () FormalMachine (FormalWriteFromOrigin formal_0_271 10 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:11]:sift-compare
(assert (not (m_panicked formal_0_272)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_272) (select (m_origin formal_0_272) 29) (select (m_origin formal_0_272) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_272) (select (m_origin formal_0_272) 29) (select (m_origin formal_0_272) 13)) false))
; source callback transition phase=insert-tail[0:15:11]:sift-compare
(define-fun formal_0_273 () FormalMachine (FormalCallback formal_0_272 boundary_0 (select (m_origin formal_0_272) 29) (select (m_origin formal_0_272) 13)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:11]
(define-fun formal_0_274 () FormalMachine (FormalWriteFromOrigin formal_0_273 9 13))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:11]:sift-compare
(assert (not (m_panicked formal_0_274)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_274) (select (m_origin formal_0_274) 29) (select (m_origin formal_0_274) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_274) (select (m_origin formal_0_274) 29) (select (m_origin formal_0_274) 8)) false))
; source callback transition phase=insert-tail[0:15:11]:sift-compare
(define-fun formal_0_275 () FormalMachine (FormalCallback formal_0_274 boundary_0 (select (m_origin formal_0_274) 29) (select (m_origin formal_0_274) 8)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:11]
(define-fun formal_0_276 () FormalMachine (FormalWriteFromOrigin formal_0_275 8 8))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:11]:sift-compare
(assert (not (m_panicked formal_0_276)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_276) (select (m_origin formal_0_276) 29) (select (m_origin formal_0_276) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_276) (select (m_origin formal_0_276) 29) (select (m_origin formal_0_276) 7)) false))
; source callback transition phase=insert-tail[0:15:11]:sift-compare
(define-fun formal_0_277 () FormalMachine (FormalCallback formal_0_276 boundary_0 (select (m_origin formal_0_276) 29) (select (m_origin formal_0_276) 7)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:11]
(define-fun formal_0_278 () FormalMachine (FormalWriteFromOrigin formal_0_277 7 7))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:11]:sift-compare
(assert (not (m_panicked formal_0_278)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_278) (select (m_origin formal_0_278) 29) (select (m_origin formal_0_278) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_278) (select (m_origin formal_0_278) 29) (select (m_origin formal_0_278) 14)) false))
; source callback transition phase=insert-tail[0:15:11]:sift-compare
(define-fun formal_0_279 () FormalMachine (FormalCallback formal_0_278 boundary_0 (select (m_origin formal_0_278) 29) (select (m_origin formal_0_278) 14)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:11]
(define-fun formal_0_280 () FormalMachine (FormalWriteFromOrigin formal_0_279 6 14))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:11]:sift-compare
(assert (not (m_panicked formal_0_280)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_280) (select (m_origin formal_0_280) 29) (select (m_origin formal_0_280) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_280) (select (m_origin formal_0_280) 29) (select (m_origin formal_0_280) 9)) false))
; source callback transition phase=insert-tail[0:15:11]:sift-compare
(define-fun formal_0_281 () FormalMachine (FormalCallback formal_0_280 boundary_0 (select (m_origin formal_0_280) 29) (select (m_origin formal_0_280) 9)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:11]
(define-fun formal_0_282 () FormalMachine (FormalWriteFromOrigin formal_0_281 5 9))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:11]:sift-compare
(assert (not (m_panicked formal_0_282)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_282) (select (m_origin formal_0_282) 29) (select (m_origin formal_0_282) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_282) (select (m_origin formal_0_282) 29) (select (m_origin formal_0_282) 17)) false))
; source callback transition phase=insert-tail[0:15:11]:sift-compare
(define-fun formal_0_283 () FormalMachine (FormalCallback formal_0_282 boundary_0 (select (m_origin formal_0_282) 29) (select (m_origin formal_0_282) 17)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:11]
(define-fun formal_0_284 () FormalMachine (FormalWriteFromOrigin formal_0_283 4 17))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:11]:sift-compare
(assert (not (m_panicked formal_0_284)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_284) (select (m_origin formal_0_284) 29) (select (m_origin formal_0_284) 18)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_284) (select (m_origin formal_0_284) 29) (select (m_origin formal_0_284) 18)) false))
; source callback transition phase=insert-tail[0:15:11]:sift-compare
(define-fun formal_0_285 () FormalMachine (FormalCallback formal_0_284 boundary_0 (select (m_origin formal_0_284) 29) (select (m_origin formal_0_284) 18)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:11]
(define-fun formal_0_286 () FormalMachine (FormalWriteFromOrigin formal_0_285 3 29))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:12]:initial-compare
(assert (not (m_panicked formal_0_286)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 31) (select (m_origin formal_0_286) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 31) (select (m_origin formal_0_286) 1)) false))
; source callback transition phase=insert-tail[0:15:12]:initial-compare
(define-fun formal_0_287 () FormalMachine (FormalCallback formal_0_286 boundary_0 (select (m_origin formal_0_286) 31) (select (m_origin formal_0_286) 1)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:12]
(define-fun formal_0_288 () FormalMachine (FormalWriteFromOrigin formal_0_287 12 1))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:12]:sift-compare
(assert (not (m_panicked formal_0_288)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 31) (select (m_origin formal_0_288) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 31) (select (m_origin formal_0_288) 3)) false))
; source callback transition phase=insert-tail[0:15:12]:sift-compare
(define-fun formal_0_289 () FormalMachine (FormalCallback formal_0_288 boundary_0 (select (m_origin formal_0_288) 31) (select (m_origin formal_0_288) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:12]
(define-fun formal_0_290 () FormalMachine (FormalWriteFromOrigin formal_0_289 11 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:12]:sift-compare
(assert (not (m_panicked formal_0_290)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_290) (select (m_origin formal_0_290) 31) (select (m_origin formal_0_290) 13)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_290) (select (m_origin formal_0_290) 31) (select (m_origin formal_0_290) 13)) false))
; source callback transition phase=insert-tail[0:15:12]:sift-compare
(define-fun formal_0_291 () FormalMachine (FormalCallback formal_0_290 boundary_0 (select (m_origin formal_0_290) 31) (select (m_origin formal_0_290) 13)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:12]
(define-fun formal_0_292 () FormalMachine (FormalWriteFromOrigin formal_0_291 10 31))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:13]:initial-compare
(assert (not (m_panicked formal_0_292)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 41) (select (m_origin formal_0_292) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 41) (select (m_origin formal_0_292) 1)) false))
; source callback transition phase=insert-tail[0:15:13]:initial-compare
(define-fun formal_0_293 () FormalMachine (FormalCallback formal_0_292 boundary_0 (select (m_origin formal_0_292) 41) (select (m_origin formal_0_292) 1)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:13]
(define-fun formal_0_294 () FormalMachine (FormalWriteFromOrigin formal_0_293 13 1))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:13]:sift-compare
(assert (not (m_panicked formal_0_294)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_294) (select (m_origin formal_0_294) 41) (select (m_origin formal_0_294) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_294) (select (m_origin formal_0_294) 41) (select (m_origin formal_0_294) 3)) false))
; source callback transition phase=insert-tail[0:15:13]:sift-compare
(define-fun formal_0_295 () FormalMachine (FormalCallback formal_0_294 boundary_0 (select (m_origin formal_0_294) 41) (select (m_origin formal_0_294) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:13]
(define-fun formal_0_296 () FormalMachine (FormalWriteFromOrigin formal_0_295 12 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:13]:sift-compare
(assert (not (m_panicked formal_0_296)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_296) (select (m_origin formal_0_296) 41) (select (m_origin formal_0_296) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_296) (select (m_origin formal_0_296) 41) (select (m_origin formal_0_296) 31)) false))
; source callback transition phase=insert-tail[0:15:13]:sift-compare
(define-fun formal_0_297 () FormalMachine (FormalCallback formal_0_296 boundary_0 (select (m_origin formal_0_296) 41) (select (m_origin formal_0_296) 31)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:13]
(define-fun formal_0_298 () FormalMachine (FormalWriteFromOrigin formal_0_297 11 31))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:13]:sift-compare
(assert (not (m_panicked formal_0_298)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_298) (select (m_origin formal_0_298) 41) (select (m_origin formal_0_298) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_298) (select (m_origin formal_0_298) 41) (select (m_origin formal_0_298) 13)) false))
; source callback transition phase=insert-tail[0:15:13]:sift-compare
(define-fun formal_0_299 () FormalMachine (FormalCallback formal_0_298 boundary_0 (select (m_origin formal_0_298) 41) (select (m_origin formal_0_298) 13)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:13]
(define-fun formal_0_300 () FormalMachine (FormalWriteFromOrigin formal_0_299 10 13))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:13]:sift-compare
(assert (not (m_panicked formal_0_300)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_300) (select (m_origin formal_0_300) 41) (select (m_origin formal_0_300) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_300) (select (m_origin formal_0_300) 41) (select (m_origin formal_0_300) 8)) false))
; source callback transition phase=insert-tail[0:15:13]:sift-compare
(define-fun formal_0_301 () FormalMachine (FormalCallback formal_0_300 boundary_0 (select (m_origin formal_0_300) 41) (select (m_origin formal_0_300) 8)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:13]
(define-fun formal_0_302 () FormalMachine (FormalWriteFromOrigin formal_0_301 9 8))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:13]:sift-compare
(assert (not (m_panicked formal_0_302)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_302) (select (m_origin formal_0_302) 41) (select (m_origin formal_0_302) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_302) (select (m_origin formal_0_302) 41) (select (m_origin formal_0_302) 7)) false))
; source callback transition phase=insert-tail[0:15:13]:sift-compare
(define-fun formal_0_303 () FormalMachine (FormalCallback formal_0_302 boundary_0 (select (m_origin formal_0_302) 41) (select (m_origin formal_0_302) 7)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:13]
(define-fun formal_0_304 () FormalMachine (FormalWriteFromOrigin formal_0_303 8 41))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:14]:initial-compare
(assert (not (m_panicked formal_0_304)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_304) (select (m_origin formal_0_304) 43) (select (m_origin formal_0_304) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_304) (select (m_origin formal_0_304) 43) (select (m_origin formal_0_304) 1)) false))
; source callback transition phase=insert-tail[0:15:14]:initial-compare
(define-fun formal_0_305 () FormalMachine (FormalCallback formal_0_304 boundary_0 (select (m_origin formal_0_304) 43) (select (m_origin formal_0_304) 1)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:14]
(define-fun formal_0_306 () FormalMachine (FormalWriteFromOrigin formal_0_305 14 1))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:14]:sift-compare
(assert (not (m_panicked formal_0_306)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_306) (select (m_origin formal_0_306) 43) (select (m_origin formal_0_306) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_306) (select (m_origin formal_0_306) 43) (select (m_origin formal_0_306) 3)) false))
; source callback transition phase=insert-tail[0:15:14]:sift-compare
(define-fun formal_0_307 () FormalMachine (FormalCallback formal_0_306 boundary_0 (select (m_origin formal_0_306) 43) (select (m_origin formal_0_306) 3)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:14]
(define-fun formal_0_308 () FormalMachine (FormalWriteFromOrigin formal_0_307 13 3))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:14]:sift-compare
(assert (not (m_panicked formal_0_308)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_308) (select (m_origin formal_0_308) 43) (select (m_origin formal_0_308) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_308) (select (m_origin formal_0_308) 43) (select (m_origin formal_0_308) 31)) false))
; source callback transition phase=insert-tail[0:15:14]:sift-compare
(define-fun formal_0_309 () FormalMachine (FormalCallback formal_0_308 boundary_0 (select (m_origin formal_0_308) 43) (select (m_origin formal_0_308) 31)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:14]
(define-fun formal_0_310 () FormalMachine (FormalWriteFromOrigin formal_0_309 12 31))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:14]:sift-compare
(assert (not (m_panicked formal_0_310)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_310) (select (m_origin formal_0_310) 43) (select (m_origin formal_0_310) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_310) (select (m_origin formal_0_310) 43) (select (m_origin formal_0_310) 13)) false))
; source callback transition phase=insert-tail[0:15:14]:sift-compare
(define-fun formal_0_311 () FormalMachine (FormalCallback formal_0_310 boundary_0 (select (m_origin formal_0_310) 43) (select (m_origin formal_0_310) 13)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:14]
(define-fun formal_0_312 () FormalMachine (FormalWriteFromOrigin formal_0_311 11 13))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:14]:sift-compare
(assert (not (m_panicked formal_0_312)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_312) (select (m_origin formal_0_312) 43) (select (m_origin formal_0_312) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_312) (select (m_origin formal_0_312) 43) (select (m_origin formal_0_312) 8)) false))
; source callback transition phase=insert-tail[0:15:14]:sift-compare
(define-fun formal_0_313 () FormalMachine (FormalCallback formal_0_312 boundary_0 (select (m_origin formal_0_312) 43) (select (m_origin formal_0_312) 8)))
; source write kind=insert-tail-shift phase=insert-tail[0:15:14]
(define-fun formal_0_314 () FormalMachine (FormalWriteFromOrigin formal_0_313 10 8))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[0:15:14]:sift-compare
(assert (not (m_panicked formal_0_314)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_314) (select (m_origin formal_0_314) 43) (select (m_origin formal_0_314) 41)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_314) (select (m_origin formal_0_314) 43) (select (m_origin formal_0_314) 41)) false))
; source callback transition phase=insert-tail[0:15:14]:sift-compare
(define-fun formal_0_315 () FormalMachine (FormalCallback formal_0_314 boundary_0 (select (m_origin formal_0_314) 43) (select (m_origin formal_0_314) 41)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:15:14]
(define-fun formal_0_316 () FormalMachine (FormalWriteFromOrigin formal_0_315 9 43))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[16:22:1]:initial-compare
(assert (not (m_panicked formal_0_316)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_316) (select (m_origin formal_0_316) 6) (select (m_origin formal_0_316) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_316) (select (m_origin formal_0_316) 6) (select (m_origin formal_0_316) 28)) false))
; source callback transition phase=insert-tail[16:22:1]:initial-compare
(define-fun formal_0_317 () FormalMachine (FormalCallback formal_0_316 boundary_0 (select (m_origin formal_0_316) 6) (select (m_origin formal_0_316) 28)))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[16:22:2]:initial-compare
(assert (not (m_panicked formal_0_317)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_317) (select (m_origin formal_0_317) 5) (select (m_origin formal_0_317) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_317) (select (m_origin formal_0_317) 5) (select (m_origin formal_0_317) 6)) false))
; source callback transition phase=insert-tail[16:22:2]:initial-compare
(define-fun formal_0_318 () FormalMachine (FormalCallback formal_0_317 boundary_0 (select (m_origin formal_0_317) 5) (select (m_origin formal_0_317) 6)))
; source write kind=insert-tail-shift phase=insert-tail[16:22:2]
(define-fun formal_0_319 () FormalMachine (FormalWriteFromOrigin formal_0_318 18 6))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[16:22:2]:sift-compare
(assert (not (m_panicked formal_0_319)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_319) (select (m_origin formal_0_319) 5) (select (m_origin formal_0_319) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_319) (select (m_origin formal_0_319) 5) (select (m_origin formal_0_319) 28)) false))
; source callback transition phase=insert-tail[16:22:2]:sift-compare
(define-fun formal_0_320 () FormalMachine (FormalCallback formal_0_319 boundary_0 (select (m_origin formal_0_319) 5) (select (m_origin formal_0_319) 28)))
; source write kind=copy-on-drop-restore phase=insert-tail[16:22:2]
(define-fun formal_0_321 () FormalMachine (FormalWriteFromOrigin formal_0_320 17 5))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[16:22:3]:initial-compare
(assert (not (m_panicked formal_0_321)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_321) (select (m_origin formal_0_321) 33) (select (m_origin formal_0_321) 6)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_321) (select (m_origin formal_0_321) 33) (select (m_origin formal_0_321) 6)) false))
; source callback transition phase=insert-tail[16:22:3]:initial-compare
(define-fun formal_0_322 () FormalMachine (FormalCallback formal_0_321 boundary_0 (select (m_origin formal_0_321) 33) (select (m_origin formal_0_321) 6)))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[16:22:4]:initial-compare
(assert (not (m_panicked formal_0_322)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 21) (select (m_origin formal_0_322) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 21) (select (m_origin formal_0_322) 33)) false))
; source callback transition phase=insert-tail[16:22:4]:initial-compare
(define-fun formal_0_323 () FormalMachine (FormalCallback formal_0_322 boundary_0 (select (m_origin formal_0_322) 21) (select (m_origin formal_0_322) 33)))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[16:22:5]:initial-compare
(assert (not (m_panicked formal_0_323)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_323) (select (m_origin formal_0_323) 24) (select (m_origin formal_0_323) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_323) (select (m_origin formal_0_323) 24) (select (m_origin formal_0_323) 21)) false))
; source callback transition phase=insert-tail[16:22:5]:initial-compare
(define-fun formal_0_324 () FormalMachine (FormalCallback formal_0_323 boundary_0 (select (m_origin formal_0_323) 24) (select (m_origin formal_0_323) 21)))
; source write kind=insert-tail-shift phase=insert-tail[16:22:5]
(define-fun formal_0_325 () FormalMachine (FormalWriteFromOrigin formal_0_324 21 21))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[16:22:5]:sift-compare
(assert (not (m_panicked formal_0_325)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_325) (select (m_origin formal_0_325) 24) (select (m_origin formal_0_325) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_325) (select (m_origin formal_0_325) 24) (select (m_origin formal_0_325) 33)) false))
; source callback transition phase=insert-tail[16:22:5]:sift-compare
(define-fun formal_0_326 () FormalMachine (FormalCallback formal_0_325 boundary_0 (select (m_origin formal_0_325) 24) (select (m_origin formal_0_325) 33)))
; source write kind=insert-tail-shift phase=insert-tail[16:22:5]
(define-fun formal_0_327 () FormalMachine (FormalWriteFromOrigin formal_0_326 20 33))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[16:22:5]:sift-compare
(assert (not (m_panicked formal_0_327)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_327) (select (m_origin formal_0_327) 24) (select (m_origin formal_0_327) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_327) (select (m_origin formal_0_327) 24) (select (m_origin formal_0_327) 6)) false))
; source callback transition phase=insert-tail[16:22:5]:sift-compare
(define-fun formal_0_328 () FormalMachine (FormalCallback formal_0_327 boundary_0 (select (m_origin formal_0_327) 24) (select (m_origin formal_0_327) 6)))
; source write kind=insert-tail-shift phase=insert-tail[16:22:5]
(define-fun formal_0_329 () FormalMachine (FormalWriteFromOrigin formal_0_328 19 6))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[16:22:5]:sift-compare
(assert (not (m_panicked formal_0_329)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_329) (select (m_origin formal_0_329) 24) (select (m_origin formal_0_329) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_329) (select (m_origin formal_0_329) 24) (select (m_origin formal_0_329) 5)) false))
; source callback transition phase=insert-tail[16:22:5]:sift-compare
(define-fun formal_0_330 () FormalMachine (FormalCallback formal_0_329 boundary_0 (select (m_origin formal_0_329) 24) (select (m_origin formal_0_329) 5)))
; source write kind=insert-tail-shift phase=insert-tail[16:22:5]
(define-fun formal_0_331 () FormalMachine (FormalWriteFromOrigin formal_0_330 18 5))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[16:22:5]:sift-compare
(assert (not (m_panicked formal_0_331)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_331) (select (m_origin formal_0_331) 24) (select (m_origin formal_0_331) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_331) (select (m_origin formal_0_331) 24) (select (m_origin formal_0_331) 28)) false))
; source callback transition phase=insert-tail[16:22:5]:sift-compare
(define-fun formal_0_332 () FormalMachine (FormalCallback formal_0_331 boundary_0 (select (m_origin formal_0_331) 24) (select (m_origin formal_0_331) 28)))
; source write kind=copy-on-drop-restore phase=insert-tail[16:22:5]
(define-fun formal_0_333 () FormalMachine (FormalWriteFromOrigin formal_0_332 17 24))
; source callback case=cyclic-unroll-one-partition phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_333)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_333) (select (m_origin formal_0_333) 23) (select (m_origin formal_0_333) 19)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_333) (select (m_origin formal_0_333) 23) (select (m_origin formal_0_333) 19)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_334 () FormalMachine (FormalCallback formal_0_333 boundary_0 (select (m_origin formal_0_333) 23) (select (m_origin formal_0_333) 19)))
; source callback case=cyclic-unroll-one-partition phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_334)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_334) (select (m_origin formal_0_334) 23) (select (m_origin formal_0_334) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_334) (select (m_origin formal_0_334) 23) (select (m_origin formal_0_334) 37)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_335 () FormalMachine (FormalCallback formal_0_334 boundary_0 (select (m_origin formal_0_334) 23) (select (m_origin formal_0_334) 37)))
; source callback case=cyclic-unroll-one-partition phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_335)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_335) (select (m_origin formal_0_335) 35) (select (m_origin formal_0_335) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_335) (select (m_origin formal_0_335) 35) (select (m_origin formal_0_335) 23)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_336 () FormalMachine (FormalCallback formal_0_335 boundary_0 (select (m_origin formal_0_335) 35) (select (m_origin formal_0_335) 23)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_337 () FormalMachine (FormalSwap formal_0_336 23 23))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_337)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_337) (select (m_origin formal_0_337) 25) (select (m_origin formal_0_337) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_337) (select (m_origin formal_0_337) 25) (select (m_origin formal_0_337) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_338 () FormalMachine (FormalCallback formal_0_337 boundary_0 (select (m_origin formal_0_337) 25) (select (m_origin formal_0_337) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_339 () FormalMachine (FormalWriteFromOrigin formal_0_338 24 25))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_339)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_339) (select (m_origin formal_0_339) 26) (select (m_origin formal_0_339) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_339) (select (m_origin formal_0_339) 26) (select (m_origin formal_0_339) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_340 () FormalMachine (FormalCallback formal_0_339 boundary_0 (select (m_origin formal_0_339) 26) (select (m_origin formal_0_339) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_341 () FormalMachine (FormalWriteFromOrigin formal_0_340 24 26))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_341)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_341) (select (m_origin formal_0_341) 27) (select (m_origin formal_0_341) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_341) (select (m_origin formal_0_341) 27) (select (m_origin formal_0_341) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_342 () FormalMachine (FormalCallback formal_0_341 boundary_0 (select (m_origin formal_0_341) 27) (select (m_origin formal_0_341) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_343 () FormalMachine (FormalWriteFromOrigin formal_0_342 25 27))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_344 () FormalMachine (FormalWriteFromOrigin formal_0_343 26 25))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_344)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_344) (select (m_origin formal_0_344) 2) (select (m_origin formal_0_344) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_344) (select (m_origin formal_0_344) 2) (select (m_origin formal_0_344) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_345 () FormalMachine (FormalCallback formal_0_344 boundary_0 (select (m_origin formal_0_344) 2) (select (m_origin formal_0_344) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_346 () FormalMachine (FormalWriteFromOrigin formal_0_345 26 2))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_347 () FormalMachine (FormalWriteFromOrigin formal_0_346 27 25))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_347)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_347) (select (m_origin formal_0_347) 10) (select (m_origin formal_0_347) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_347) (select (m_origin formal_0_347) 10) (select (m_origin formal_0_347) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_348 () FormalMachine (FormalCallback formal_0_347 boundary_0 (select (m_origin formal_0_347) 10) (select (m_origin formal_0_347) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_349 () FormalMachine (FormalWriteFromOrigin formal_0_348 27 10))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_350 () FormalMachine (FormalWriteFromOrigin formal_0_349 28 25))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_350)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_350) (select (m_origin formal_0_350) 30) (select (m_origin formal_0_350) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_350) (select (m_origin formal_0_350) 30) (select (m_origin formal_0_350) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_351 () FormalMachine (FormalCallback formal_0_350 boundary_0 (select (m_origin formal_0_350) 30) (select (m_origin formal_0_350) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_352 () FormalMachine (FormalWriteFromOrigin formal_0_351 27 30))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_352)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_352) (select (m_origin formal_0_352) 19) (select (m_origin formal_0_352) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_352) (select (m_origin formal_0_352) 19) (select (m_origin formal_0_352) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_353 () FormalMachine (FormalCallback formal_0_352 boundary_0 (select (m_origin formal_0_352) 19) (select (m_origin formal_0_352) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_354 () FormalMachine (FormalWriteFromOrigin formal_0_353 27 19))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_354)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_354) (select (m_origin formal_0_354) 32) (select (m_origin formal_0_354) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_354) (select (m_origin formal_0_354) 32) (select (m_origin formal_0_354) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_355 () FormalMachine (FormalCallback formal_0_354 boundary_0 (select (m_origin formal_0_354) 32) (select (m_origin formal_0_354) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_356 () FormalMachine (FormalWriteFromOrigin formal_0_355 28 32))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_357 () FormalMachine (FormalWriteFromOrigin formal_0_356 31 25))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_357)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 11) (select (m_origin formal_0_357) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 11) (select (m_origin formal_0_357) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_358 () FormalMachine (FormalCallback formal_0_357 boundary_0 (select (m_origin formal_0_357) 11) (select (m_origin formal_0_357) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_359 () FormalMachine (FormalWriteFromOrigin formal_0_358 29 11))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_360 () FormalMachine (FormalWriteFromOrigin formal_0_359 32 10))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_360)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_360) (select (m_origin formal_0_360) 34) (select (m_origin formal_0_360) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_360) (select (m_origin formal_0_360) 34) (select (m_origin formal_0_360) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_361 () FormalMachine (FormalCallback formal_0_360 boundary_0 (select (m_origin formal_0_360) 34) (select (m_origin formal_0_360) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_362 () FormalMachine (FormalWriteFromOrigin formal_0_361 29 34))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_362)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_362) (select (m_origin formal_0_362) 0) (select (m_origin formal_0_362) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_362) (select (m_origin formal_0_362) 0) (select (m_origin formal_0_362) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_363 () FormalMachine (FormalCallback formal_0_362 boundary_0 (select (m_origin formal_0_362) 0) (select (m_origin formal_0_362) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_364 () FormalMachine (FormalWriteFromOrigin formal_0_363 30 0))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_365 () FormalMachine (FormalWriteFromOrigin formal_0_364 34 30))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_365)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_365) (select (m_origin formal_0_365) 36) (select (m_origin formal_0_365) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_365) (select (m_origin formal_0_365) 36) (select (m_origin formal_0_365) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_366 () FormalMachine (FormalCallback formal_0_365 boundary_0 (select (m_origin formal_0_365) 36) (select (m_origin formal_0_365) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_367 () FormalMachine (FormalWriteFromOrigin formal_0_366 31 36))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_368 () FormalMachine (FormalWriteFromOrigin formal_0_367 35 25))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_368)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_368) (select (m_origin formal_0_368) 37) (select (m_origin formal_0_368) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_368) (select (m_origin formal_0_368) 37) (select (m_origin formal_0_368) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_369 () FormalMachine (FormalCallback formal_0_368 boundary_0 (select (m_origin formal_0_368) 37) (select (m_origin formal_0_368) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_370 () FormalMachine (FormalWriteFromOrigin formal_0_369 31 37))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_370)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_370) (select (m_origin formal_0_370) 38) (select (m_origin formal_0_370) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_370) (select (m_origin formal_0_370) 38) (select (m_origin formal_0_370) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_371 () FormalMachine (FormalCallback formal_0_370 boundary_0 (select (m_origin formal_0_370) 38) (select (m_origin formal_0_370) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_372 () FormalMachine (FormalWriteFromOrigin formal_0_371 31 38))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_372)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_372) (select (m_origin formal_0_372) 39) (select (m_origin formal_0_372) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_372) (select (m_origin formal_0_372) 39) (select (m_origin formal_0_372) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_373 () FormalMachine (FormalCallback formal_0_372 boundary_0 (select (m_origin formal_0_372) 39) (select (m_origin formal_0_372) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_374 () FormalMachine (FormalWriteFromOrigin formal_0_373 32 39))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_375 () FormalMachine (FormalWriteFromOrigin formal_0_374 38 10))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_375)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_375) (select (m_origin formal_0_375) 40) (select (m_origin formal_0_375) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_375) (select (m_origin formal_0_375) 40) (select (m_origin formal_0_375) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_376 () FormalMachine (FormalCallback formal_0_375 boundary_0 (select (m_origin formal_0_375) 40) (select (m_origin formal_0_375) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_377 () FormalMachine (FormalWriteFromOrigin formal_0_376 33 40))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_378 () FormalMachine (FormalWriteFromOrigin formal_0_377 39 11))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_378)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_378) (select (m_origin formal_0_378) 15) (select (m_origin formal_0_378) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_378) (select (m_origin formal_0_378) 15) (select (m_origin formal_0_378) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_379 () FormalMachine (FormalCallback formal_0_378 boundary_0 (select (m_origin formal_0_378) 15) (select (m_origin formal_0_378) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_380 () FormalMachine (FormalWriteFromOrigin formal_0_379 33 15))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_380)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_380) (select (m_origin formal_0_380) 42) (select (m_origin formal_0_380) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_380) (select (m_origin formal_0_380) 42) (select (m_origin formal_0_380) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_381 () FormalMachine (FormalCallback formal_0_380 boundary_0 (select (m_origin formal_0_380) 42) (select (m_origin formal_0_380) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_382 () FormalMachine (FormalWriteFromOrigin formal_0_381 33 42))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_382)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_382) (select (m_origin formal_0_382) 22) (select (m_origin formal_0_382) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_382) (select (m_origin formal_0_382) 22) (select (m_origin formal_0_382) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_383 () FormalMachine (FormalCallback formal_0_382 boundary_0 (select (m_origin formal_0_382) 22) (select (m_origin formal_0_382) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_384 () FormalMachine (FormalWriteFromOrigin formal_0_383 33 22))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_384)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_384) (select (m_origin formal_0_384) 44) (select (m_origin formal_0_384) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_384) (select (m_origin formal_0_384) 44) (select (m_origin formal_0_384) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_385 () FormalMachine (FormalCallback formal_0_384 boundary_0 (select (m_origin formal_0_384) 44) (select (m_origin formal_0_384) 23)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_386 () FormalMachine (FormalWriteFromOrigin formal_0_385 33 44))
; source callback case=cyclic-unroll-one-partition phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_386)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_386) (select (m_origin formal_0_386) 16) (select (m_origin formal_0_386) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_386) (select (m_origin formal_0_386) 16) (select (m_origin formal_0_386) 23)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_387 () FormalMachine (FormalCallback formal_0_386 boundary_0 (select (m_origin formal_0_386) 16) (select (m_origin formal_0_386) 23)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_388 () FormalMachine (FormalWriteFromOrigin formal_0_387 33 16))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_389 () FormalMachine (FormalSwap formal_0_388 23 32))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:1]:initial-compare
(assert (not (m_panicked formal_0_389)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_389) (select (m_origin formal_0_389) 26) (select (m_origin formal_0_389) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_389) (select (m_origin formal_0_389) 26) (select (m_origin formal_0_389) 39)) false))
; source callback transition phase=insert-tail[23:32:1]:initial-compare
(define-fun formal_0_390 () FormalMachine (FormalCallback formal_0_389 boundary_0 (select (m_origin formal_0_389) 26) (select (m_origin formal_0_389) 39)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:1]
(define-fun formal_0_391 () FormalMachine (FormalWriteFromOrigin formal_0_390 24 39))
; source write kind=copy-on-drop-restore phase=insert-tail[23:32:1]
(define-fun formal_0_392 () FormalMachine (FormalWriteFromOrigin formal_0_391 23 26))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:2]:initial-compare
(assert (not (m_panicked formal_0_392)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_392) (select (m_origin formal_0_392) 27) (select (m_origin formal_0_392) 39)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_392) (select (m_origin formal_0_392) 27) (select (m_origin formal_0_392) 39)) false))
; source callback transition phase=insert-tail[23:32:2]:initial-compare
(define-fun formal_0_393 () FormalMachine (FormalCallback formal_0_392 boundary_0 (select (m_origin formal_0_392) 27) (select (m_origin formal_0_392) 39)))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:3]:initial-compare
(assert (not (m_panicked formal_0_393)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_393) (select (m_origin formal_0_393) 2) (select (m_origin formal_0_393) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_393) (select (m_origin formal_0_393) 2) (select (m_origin formal_0_393) 27)) false))
; source callback transition phase=insert-tail[23:32:3]:initial-compare
(define-fun formal_0_394 () FormalMachine (FormalCallback formal_0_393 boundary_0 (select (m_origin formal_0_393) 2) (select (m_origin formal_0_393) 27)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:3]
(define-fun formal_0_395 () FormalMachine (FormalWriteFromOrigin formal_0_394 26 27))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:3]:sift-compare
(assert (not (m_panicked formal_0_395)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_395) (select (m_origin formal_0_395) 2) (select (m_origin formal_0_395) 39)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_395) (select (m_origin formal_0_395) 2) (select (m_origin formal_0_395) 39)) false))
; source callback transition phase=insert-tail[23:32:3]:sift-compare
(define-fun formal_0_396 () FormalMachine (FormalCallback formal_0_395 boundary_0 (select (m_origin formal_0_395) 2) (select (m_origin formal_0_395) 39)))
; source write kind=copy-on-drop-restore phase=insert-tail[23:32:3]
(define-fun formal_0_397 () FormalMachine (FormalWriteFromOrigin formal_0_396 25 2))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:4]:initial-compare
(assert (not (m_panicked formal_0_397)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_397) (select (m_origin formal_0_397) 19) (select (m_origin formal_0_397) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_397) (select (m_origin formal_0_397) 19) (select (m_origin formal_0_397) 27)) false))
; source callback transition phase=insert-tail[23:32:4]:initial-compare
(define-fun formal_0_398 () FormalMachine (FormalCallback formal_0_397 boundary_0 (select (m_origin formal_0_397) 19) (select (m_origin formal_0_397) 27)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:4]
(define-fun formal_0_399 () FormalMachine (FormalWriteFromOrigin formal_0_398 27 27))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:4]:sift-compare
(assert (not (m_panicked formal_0_399)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_399) (select (m_origin formal_0_399) 19) (select (m_origin formal_0_399) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_399) (select (m_origin formal_0_399) 19) (select (m_origin formal_0_399) 2)) false))
; source callback transition phase=insert-tail[23:32:4]:sift-compare
(define-fun formal_0_400 () FormalMachine (FormalCallback formal_0_399 boundary_0 (select (m_origin formal_0_399) 19) (select (m_origin formal_0_399) 2)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:4]
(define-fun formal_0_401 () FormalMachine (FormalWriteFromOrigin formal_0_400 26 2))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:4]:sift-compare
(assert (not (m_panicked formal_0_401)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_401) (select (m_origin formal_0_401) 19) (select (m_origin formal_0_401) 39)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_401) (select (m_origin formal_0_401) 19) (select (m_origin formal_0_401) 39)) false))
; source callback transition phase=insert-tail[23:32:4]:sift-compare
(define-fun formal_0_402 () FormalMachine (FormalCallback formal_0_401 boundary_0 (select (m_origin formal_0_401) 19) (select (m_origin formal_0_401) 39)))
; source write kind=copy-on-drop-restore phase=insert-tail[23:32:4]
(define-fun formal_0_403 () FormalMachine (FormalWriteFromOrigin formal_0_402 25 19))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:5]:initial-compare
(assert (not (m_panicked formal_0_403)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_403) (select (m_origin formal_0_403) 32) (select (m_origin formal_0_403) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_403) (select (m_origin formal_0_403) 32) (select (m_origin formal_0_403) 27)) false))
; source callback transition phase=insert-tail[23:32:5]:initial-compare
(define-fun formal_0_404 () FormalMachine (FormalCallback formal_0_403 boundary_0 (select (m_origin formal_0_403) 32) (select (m_origin formal_0_403) 27)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:5]
(define-fun formal_0_405 () FormalMachine (FormalWriteFromOrigin formal_0_404 28 27))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:5]:sift-compare
(assert (not (m_panicked formal_0_405)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_405) (select (m_origin formal_0_405) 32) (select (m_origin formal_0_405) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_405) (select (m_origin formal_0_405) 32) (select (m_origin formal_0_405) 2)) false))
; source callback transition phase=insert-tail[23:32:5]:sift-compare
(define-fun formal_0_406 () FormalMachine (FormalCallback formal_0_405 boundary_0 (select (m_origin formal_0_405) 32) (select (m_origin formal_0_405) 2)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:5]
(define-fun formal_0_407 () FormalMachine (FormalWriteFromOrigin formal_0_406 27 2))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:5]:sift-compare
(assert (not (m_panicked formal_0_407)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_407) (select (m_origin formal_0_407) 32) (select (m_origin formal_0_407) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_407) (select (m_origin formal_0_407) 32) (select (m_origin formal_0_407) 19)) false))
; source callback transition phase=insert-tail[23:32:5]:sift-compare
(define-fun formal_0_408 () FormalMachine (FormalCallback formal_0_407 boundary_0 (select (m_origin formal_0_407) 32) (select (m_origin formal_0_407) 19)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:5]
(define-fun formal_0_409 () FormalMachine (FormalWriteFromOrigin formal_0_408 26 19))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:5]:sift-compare
(assert (not (m_panicked formal_0_409)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_409) (select (m_origin formal_0_409) 32) (select (m_origin formal_0_409) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_409) (select (m_origin formal_0_409) 32) (select (m_origin formal_0_409) 39)) false))
; source callback transition phase=insert-tail[23:32:5]:sift-compare
(define-fun formal_0_410 () FormalMachine (FormalCallback formal_0_409 boundary_0 (select (m_origin formal_0_409) 32) (select (m_origin formal_0_409) 39)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:5]
(define-fun formal_0_411 () FormalMachine (FormalWriteFromOrigin formal_0_410 25 39))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:5]:sift-compare
(assert (not (m_panicked formal_0_411)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_411) (select (m_origin formal_0_411) 32) (select (m_origin formal_0_411) 26)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_411) (select (m_origin formal_0_411) 32) (select (m_origin formal_0_411) 26)) false))
; source callback transition phase=insert-tail[23:32:5]:sift-compare
(define-fun formal_0_412 () FormalMachine (FormalCallback formal_0_411 boundary_0 (select (m_origin formal_0_411) 32) (select (m_origin formal_0_411) 26)))
; source write kind=copy-on-drop-restore phase=insert-tail[23:32:5]
(define-fun formal_0_413 () FormalMachine (FormalWriteFromOrigin formal_0_412 24 32))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:6]:initial-compare
(assert (not (m_panicked formal_0_413)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_413) (select (m_origin formal_0_413) 34) (select (m_origin formal_0_413) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_413) (select (m_origin formal_0_413) 34) (select (m_origin formal_0_413) 27)) false))
; source callback transition phase=insert-tail[23:32:6]:initial-compare
(define-fun formal_0_414 () FormalMachine (FormalCallback formal_0_413 boundary_0 (select (m_origin formal_0_413) 34) (select (m_origin formal_0_413) 27)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:6]
(define-fun formal_0_415 () FormalMachine (FormalWriteFromOrigin formal_0_414 29 27))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:6]:sift-compare
(assert (not (m_panicked formal_0_415)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_415) (select (m_origin formal_0_415) 34) (select (m_origin formal_0_415) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_415) (select (m_origin formal_0_415) 34) (select (m_origin formal_0_415) 2)) false))
; source callback transition phase=insert-tail[23:32:6]:sift-compare
(define-fun formal_0_416 () FormalMachine (FormalCallback formal_0_415 boundary_0 (select (m_origin formal_0_415) 34) (select (m_origin formal_0_415) 2)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:6]
(define-fun formal_0_417 () FormalMachine (FormalWriteFromOrigin formal_0_416 28 2))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:6]:sift-compare
(assert (not (m_panicked formal_0_417)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_417) (select (m_origin formal_0_417) 34) (select (m_origin formal_0_417) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_417) (select (m_origin formal_0_417) 34) (select (m_origin formal_0_417) 19)) false))
; source callback transition phase=insert-tail[23:32:6]:sift-compare
(define-fun formal_0_418 () FormalMachine (FormalCallback formal_0_417 boundary_0 (select (m_origin formal_0_417) 34) (select (m_origin formal_0_417) 19)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:6]
(define-fun formal_0_419 () FormalMachine (FormalWriteFromOrigin formal_0_418 27 19))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:6]:sift-compare
(assert (not (m_panicked formal_0_419)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_419) (select (m_origin formal_0_419) 34) (select (m_origin formal_0_419) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_419) (select (m_origin formal_0_419) 34) (select (m_origin formal_0_419) 39)) false))
; source callback transition phase=insert-tail[23:32:6]:sift-compare
(define-fun formal_0_420 () FormalMachine (FormalCallback formal_0_419 boundary_0 (select (m_origin formal_0_419) 34) (select (m_origin formal_0_419) 39)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:6]
(define-fun formal_0_421 () FormalMachine (FormalWriteFromOrigin formal_0_420 26 39))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:6]:sift-compare
(assert (not (m_panicked formal_0_421)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_421) (select (m_origin formal_0_421) 34) (select (m_origin formal_0_421) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_421) (select (m_origin formal_0_421) 34) (select (m_origin formal_0_421) 32)) false))
; source callback transition phase=insert-tail[23:32:6]:sift-compare
(define-fun formal_0_422 () FormalMachine (FormalCallback formal_0_421 boundary_0 (select (m_origin formal_0_421) 34) (select (m_origin formal_0_421) 32)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:6]
(define-fun formal_0_423 () FormalMachine (FormalWriteFromOrigin formal_0_422 25 32))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:6]:sift-compare
(assert (not (m_panicked formal_0_423)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_423) (select (m_origin formal_0_423) 34) (select (m_origin formal_0_423) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_423) (select (m_origin formal_0_423) 34) (select (m_origin formal_0_423) 26)) false))
; source callback transition phase=insert-tail[23:32:6]:sift-compare
(define-fun formal_0_424 () FormalMachine (FormalCallback formal_0_423 boundary_0 (select (m_origin formal_0_423) 34) (select (m_origin formal_0_423) 26)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:6]
(define-fun formal_0_425 () FormalMachine (FormalWriteFromOrigin formal_0_424 24 26))
; source write kind=copy-on-drop-restore phase=insert-tail[23:32:6]
(define-fun formal_0_426 () FormalMachine (FormalWriteFromOrigin formal_0_425 23 34))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:7]:initial-compare
(assert (not (m_panicked formal_0_426)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_426) (select (m_origin formal_0_426) 0) (select (m_origin formal_0_426) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_426) (select (m_origin formal_0_426) 0) (select (m_origin formal_0_426) 27)) false))
; source callback transition phase=insert-tail[23:32:7]:initial-compare
(define-fun formal_0_427 () FormalMachine (FormalCallback formal_0_426 boundary_0 (select (m_origin formal_0_426) 0) (select (m_origin formal_0_426) 27)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:7]
(define-fun formal_0_428 () FormalMachine (FormalWriteFromOrigin formal_0_427 30 27))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:7]:sift-compare
(assert (not (m_panicked formal_0_428)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_428) (select (m_origin formal_0_428) 0) (select (m_origin formal_0_428) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_428) (select (m_origin formal_0_428) 0) (select (m_origin formal_0_428) 2)) false))
; source callback transition phase=insert-tail[23:32:7]:sift-compare
(define-fun formal_0_429 () FormalMachine (FormalCallback formal_0_428 boundary_0 (select (m_origin formal_0_428) 0) (select (m_origin formal_0_428) 2)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:7]
(define-fun formal_0_430 () FormalMachine (FormalWriteFromOrigin formal_0_429 29 2))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:7]:sift-compare
(assert (not (m_panicked formal_0_430)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_430) (select (m_origin formal_0_430) 0) (select (m_origin formal_0_430) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_430) (select (m_origin formal_0_430) 0) (select (m_origin formal_0_430) 19)) false))
; source callback transition phase=insert-tail[23:32:7]:sift-compare
(define-fun formal_0_431 () FormalMachine (FormalCallback formal_0_430 boundary_0 (select (m_origin formal_0_430) 0) (select (m_origin formal_0_430) 19)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:7]
(define-fun formal_0_432 () FormalMachine (FormalWriteFromOrigin formal_0_431 28 19))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:7]:sift-compare
(assert (not (m_panicked formal_0_432)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_432) (select (m_origin formal_0_432) 0) (select (m_origin formal_0_432) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_432) (select (m_origin formal_0_432) 0) (select (m_origin formal_0_432) 39)) false))
; source callback transition phase=insert-tail[23:32:7]:sift-compare
(define-fun formal_0_433 () FormalMachine (FormalCallback formal_0_432 boundary_0 (select (m_origin formal_0_432) 0) (select (m_origin formal_0_432) 39)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:7]
(define-fun formal_0_434 () FormalMachine (FormalWriteFromOrigin formal_0_433 27 39))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:7]:sift-compare
(assert (not (m_panicked formal_0_434)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_434) (select (m_origin formal_0_434) 0) (select (m_origin formal_0_434) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_434) (select (m_origin formal_0_434) 0) (select (m_origin formal_0_434) 32)) false))
; source callback transition phase=insert-tail[23:32:7]:sift-compare
(define-fun formal_0_435 () FormalMachine (FormalCallback formal_0_434 boundary_0 (select (m_origin formal_0_434) 0) (select (m_origin formal_0_434) 32)))
; source write kind=copy-on-drop-restore phase=insert-tail[23:32:7]
(define-fun formal_0_436 () FormalMachine (FormalWriteFromOrigin formal_0_435 26 0))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:8]:initial-compare
(assert (not (m_panicked formal_0_436)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_436) (select (m_origin formal_0_436) 38) (select (m_origin formal_0_436) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_436) (select (m_origin formal_0_436) 38) (select (m_origin formal_0_436) 27)) false))
; source callback transition phase=insert-tail[23:32:8]:initial-compare
(define-fun formal_0_437 () FormalMachine (FormalCallback formal_0_436 boundary_0 (select (m_origin formal_0_436) 38) (select (m_origin formal_0_436) 27)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:8]
(define-fun formal_0_438 () FormalMachine (FormalWriteFromOrigin formal_0_437 31 27))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:8]:sift-compare
(assert (not (m_panicked formal_0_438)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_438) (select (m_origin formal_0_438) 38) (select (m_origin formal_0_438) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_438) (select (m_origin formal_0_438) 38) (select (m_origin formal_0_438) 2)) false))
; source callback transition phase=insert-tail[23:32:8]:sift-compare
(define-fun formal_0_439 () FormalMachine (FormalCallback formal_0_438 boundary_0 (select (m_origin formal_0_438) 38) (select (m_origin formal_0_438) 2)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:8]
(define-fun formal_0_440 () FormalMachine (FormalWriteFromOrigin formal_0_439 30 2))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:8]:sift-compare
(assert (not (m_panicked formal_0_440)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_440) (select (m_origin formal_0_440) 38) (select (m_origin formal_0_440) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_440) (select (m_origin formal_0_440) 38) (select (m_origin formal_0_440) 19)) false))
; source callback transition phase=insert-tail[23:32:8]:sift-compare
(define-fun formal_0_441 () FormalMachine (FormalCallback formal_0_440 boundary_0 (select (m_origin formal_0_440) 38) (select (m_origin formal_0_440) 19)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:8]
(define-fun formal_0_442 () FormalMachine (FormalWriteFromOrigin formal_0_441 29 19))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:8]:sift-compare
(assert (not (m_panicked formal_0_442)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_442) (select (m_origin formal_0_442) 38) (select (m_origin formal_0_442) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_442) (select (m_origin formal_0_442) 38) (select (m_origin formal_0_442) 39)) false))
; source callback transition phase=insert-tail[23:32:8]:sift-compare
(define-fun formal_0_443 () FormalMachine (FormalCallback formal_0_442 boundary_0 (select (m_origin formal_0_442) 38) (select (m_origin formal_0_442) 39)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:8]
(define-fun formal_0_444 () FormalMachine (FormalWriteFromOrigin formal_0_443 28 39))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:8]:sift-compare
(assert (not (m_panicked formal_0_444)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_444) (select (m_origin formal_0_444) 38) (select (m_origin formal_0_444) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_444) (select (m_origin formal_0_444) 38) (select (m_origin formal_0_444) 0)) false))
; source callback transition phase=insert-tail[23:32:8]:sift-compare
(define-fun formal_0_445 () FormalMachine (FormalCallback formal_0_444 boundary_0 (select (m_origin formal_0_444) 38) (select (m_origin formal_0_444) 0)))
; source write kind=insert-tail-shift phase=insert-tail[23:32:8]
(define-fun formal_0_446 () FormalMachine (FormalWriteFromOrigin formal_0_445 27 0))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[23:32:8]:sift-compare
(assert (not (m_panicked formal_0_446)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_446) (select (m_origin formal_0_446) 38) (select (m_origin formal_0_446) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_446) (select (m_origin formal_0_446) 38) (select (m_origin formal_0_446) 32)) false))
; source callback transition phase=insert-tail[23:32:8]:sift-compare
(define-fun formal_0_447 () FormalMachine (FormalCallback formal_0_446 boundary_0 (select (m_origin formal_0_446) 38) (select (m_origin formal_0_446) 32)))
; source write kind=copy-on-drop-restore phase=insert-tail[23:32:8]
(define-fun formal_0_448 () FormalMachine (FormalWriteFromOrigin formal_0_447 26 38))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:1]:initial-compare
(assert (not (m_panicked formal_0_448)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_448) (select (m_origin formal_0_448) 30) (select (m_origin formal_0_448) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_448) (select (m_origin formal_0_448) 30) (select (m_origin formal_0_448) 16)) false))
; source callback transition phase=insert-tail[33:45:1]:initial-compare
(define-fun formal_0_449 () FormalMachine (FormalCallback formal_0_448 boundary_0 (select (m_origin formal_0_448) 30) (select (m_origin formal_0_448) 16)))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:2]:initial-compare
(assert (not (m_panicked formal_0_449)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_449) (select (m_origin formal_0_449) 25) (select (m_origin formal_0_449) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_449) (select (m_origin formal_0_449) 25) (select (m_origin formal_0_449) 30)) false))
; source callback transition phase=insert-tail[33:45:2]:initial-compare
(define-fun formal_0_450 () FormalMachine (FormalCallback formal_0_449 boundary_0 (select (m_origin formal_0_449) 25) (select (m_origin formal_0_449) 30)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:2]
(define-fun formal_0_451 () FormalMachine (FormalWriteFromOrigin formal_0_450 35 30))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:2]:sift-compare
(assert (not (m_panicked formal_0_451)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_451) (select (m_origin formal_0_451) 25) (select (m_origin formal_0_451) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_451) (select (m_origin formal_0_451) 25) (select (m_origin formal_0_451) 16)) false))
; source callback transition phase=insert-tail[33:45:2]:sift-compare
(define-fun formal_0_452 () FormalMachine (FormalCallback formal_0_451 boundary_0 (select (m_origin formal_0_451) 25) (select (m_origin formal_0_451) 16)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:2]
(define-fun formal_0_453 () FormalMachine (FormalWriteFromOrigin formal_0_452 34 16))
; source write kind=copy-on-drop-restore phase=insert-tail[33:45:2]
(define-fun formal_0_454 () FormalMachine (FormalWriteFromOrigin formal_0_453 33 25))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:3]:initial-compare
(assert (not (m_panicked formal_0_454)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_454) (select (m_origin formal_0_454) 36) (select (m_origin formal_0_454) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_454) (select (m_origin formal_0_454) 36) (select (m_origin formal_0_454) 30)) false))
; source callback transition phase=insert-tail[33:45:3]:initial-compare
(define-fun formal_0_455 () FormalMachine (FormalCallback formal_0_454 boundary_0 (select (m_origin formal_0_454) 36) (select (m_origin formal_0_454) 30)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:3]
(define-fun formal_0_456 () FormalMachine (FormalWriteFromOrigin formal_0_455 36 30))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:3]:sift-compare
(assert (not (m_panicked formal_0_456)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_456) (select (m_origin formal_0_456) 36) (select (m_origin formal_0_456) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_456) (select (m_origin formal_0_456) 36) (select (m_origin formal_0_456) 16)) false))
; source callback transition phase=insert-tail[33:45:3]:sift-compare
(define-fun formal_0_457 () FormalMachine (FormalCallback formal_0_456 boundary_0 (select (m_origin formal_0_456) 36) (select (m_origin formal_0_456) 16)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:3]
(define-fun formal_0_458 () FormalMachine (FormalWriteFromOrigin formal_0_457 35 16))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:3]:sift-compare
(assert (not (m_panicked formal_0_458)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_458) (select (m_origin formal_0_458) 36) (select (m_origin formal_0_458) 25)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_458) (select (m_origin formal_0_458) 36) (select (m_origin formal_0_458) 25)) false))
; source callback transition phase=insert-tail[33:45:3]:sift-compare
(define-fun formal_0_459 () FormalMachine (FormalCallback formal_0_458 boundary_0 (select (m_origin formal_0_458) 36) (select (m_origin formal_0_458) 25)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:45:3]
(define-fun formal_0_460 () FormalMachine (FormalWriteFromOrigin formal_0_459 34 36))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:4]:initial-compare
(assert (not (m_panicked formal_0_460)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_460) (select (m_origin formal_0_460) 37) (select (m_origin formal_0_460) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_460) (select (m_origin formal_0_460) 37) (select (m_origin formal_0_460) 30)) false))
; source callback transition phase=insert-tail[33:45:4]:initial-compare
(define-fun formal_0_461 () FormalMachine (FormalCallback formal_0_460 boundary_0 (select (m_origin formal_0_460) 37) (select (m_origin formal_0_460) 30)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:4]
(define-fun formal_0_462 () FormalMachine (FormalWriteFromOrigin formal_0_461 37 30))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:4]:sift-compare
(assert (not (m_panicked formal_0_462)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_462) (select (m_origin formal_0_462) 37) (select (m_origin formal_0_462) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_462) (select (m_origin formal_0_462) 37) (select (m_origin formal_0_462) 16)) false))
; source callback transition phase=insert-tail[33:45:4]:sift-compare
(define-fun formal_0_463 () FormalMachine (FormalCallback formal_0_462 boundary_0 (select (m_origin formal_0_462) 37) (select (m_origin formal_0_462) 16)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:4]
(define-fun formal_0_464 () FormalMachine (FormalWriteFromOrigin formal_0_463 36 16))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:4]:sift-compare
(assert (not (m_panicked formal_0_464)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_464) (select (m_origin formal_0_464) 37) (select (m_origin formal_0_464) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_464) (select (m_origin formal_0_464) 37) (select (m_origin formal_0_464) 36)) false))
; source callback transition phase=insert-tail[33:45:4]:sift-compare
(define-fun formal_0_465 () FormalMachine (FormalCallback formal_0_464 boundary_0 (select (m_origin formal_0_464) 37) (select (m_origin formal_0_464) 36)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:4]
(define-fun formal_0_466 () FormalMachine (FormalWriteFromOrigin formal_0_465 35 36))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:4]:sift-compare
(assert (not (m_panicked formal_0_466)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_466) (select (m_origin formal_0_466) 37) (select (m_origin formal_0_466) 25)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_466) (select (m_origin formal_0_466) 37) (select (m_origin formal_0_466) 25)) false))
; source callback transition phase=insert-tail[33:45:4]:sift-compare
(define-fun formal_0_467 () FormalMachine (FormalCallback formal_0_466 boundary_0 (select (m_origin formal_0_466) 37) (select (m_origin formal_0_466) 25)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:4]
(define-fun formal_0_468 () FormalMachine (FormalWriteFromOrigin formal_0_467 34 25))
; source write kind=copy-on-drop-restore phase=insert-tail[33:45:4]
(define-fun formal_0_469 () FormalMachine (FormalWriteFromOrigin formal_0_468 33 37))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:5]:initial-compare
(assert (not (m_panicked formal_0_469)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_469) (select (m_origin formal_0_469) 10) (select (m_origin formal_0_469) 30)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_469) (select (m_origin formal_0_469) 10) (select (m_origin formal_0_469) 30)) false))
; source callback transition phase=insert-tail[33:45:5]:initial-compare
(define-fun formal_0_470 () FormalMachine (FormalCallback formal_0_469 boundary_0 (select (m_origin formal_0_469) 10) (select (m_origin formal_0_469) 30)))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:6]:initial-compare
(assert (not (m_panicked formal_0_470)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_470) (select (m_origin formal_0_470) 11) (select (m_origin formal_0_470) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_470) (select (m_origin formal_0_470) 11) (select (m_origin formal_0_470) 10)) false))
; source callback transition phase=insert-tail[33:45:6]:initial-compare
(define-fun formal_0_471 () FormalMachine (FormalCallback formal_0_470 boundary_0 (select (m_origin formal_0_470) 11) (select (m_origin formal_0_470) 10)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:6]
(define-fun formal_0_472 () FormalMachine (FormalWriteFromOrigin formal_0_471 39 10))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:6]:sift-compare
(assert (not (m_panicked formal_0_472)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_472) (select (m_origin formal_0_472) 11) (select (m_origin formal_0_472) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_472) (select (m_origin formal_0_472) 11) (select (m_origin formal_0_472) 30)) false))
; source callback transition phase=insert-tail[33:45:6]:sift-compare
(define-fun formal_0_473 () FormalMachine (FormalCallback formal_0_472 boundary_0 (select (m_origin formal_0_472) 11) (select (m_origin formal_0_472) 30)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:6]
(define-fun formal_0_474 () FormalMachine (FormalWriteFromOrigin formal_0_473 38 30))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:6]:sift-compare
(assert (not (m_panicked formal_0_474)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_474) (select (m_origin formal_0_474) 11) (select (m_origin formal_0_474) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_474) (select (m_origin formal_0_474) 11) (select (m_origin formal_0_474) 16)) false))
; source callback transition phase=insert-tail[33:45:6]:sift-compare
(define-fun formal_0_475 () FormalMachine (FormalCallback formal_0_474 boundary_0 (select (m_origin formal_0_474) 11) (select (m_origin formal_0_474) 16)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:6]
(define-fun formal_0_476 () FormalMachine (FormalWriteFromOrigin formal_0_475 37 16))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:6]:sift-compare
(assert (not (m_panicked formal_0_476)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_476) (select (m_origin formal_0_476) 11) (select (m_origin formal_0_476) 36)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_476) (select (m_origin formal_0_476) 11) (select (m_origin formal_0_476) 36)) false))
; source callback transition phase=insert-tail[33:45:6]:sift-compare
(define-fun formal_0_477 () FormalMachine (FormalCallback formal_0_476 boundary_0 (select (m_origin formal_0_476) 11) (select (m_origin formal_0_476) 36)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:45:6]
(define-fun formal_0_478 () FormalMachine (FormalWriteFromOrigin formal_0_477 36 11))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:7]:initial-compare
(assert (not (m_panicked formal_0_478)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_478) (select (m_origin formal_0_478) 40) (select (m_origin formal_0_478) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_478) (select (m_origin formal_0_478) 40) (select (m_origin formal_0_478) 10)) false))
; source callback transition phase=insert-tail[33:45:7]:initial-compare
(define-fun formal_0_479 () FormalMachine (FormalCallback formal_0_478 boundary_0 (select (m_origin formal_0_478) 40) (select (m_origin formal_0_478) 10)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:7]
(define-fun formal_0_480 () FormalMachine (FormalWriteFromOrigin formal_0_479 40 10))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:7]:sift-compare
(assert (not (m_panicked formal_0_480)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_480) (select (m_origin formal_0_480) 40) (select (m_origin formal_0_480) 30)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_480) (select (m_origin formal_0_480) 40) (select (m_origin formal_0_480) 30)) false))
; source callback transition phase=insert-tail[33:45:7]:sift-compare
(define-fun formal_0_481 () FormalMachine (FormalCallback formal_0_480 boundary_0 (select (m_origin formal_0_480) 40) (select (m_origin formal_0_480) 30)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:45:7]
(define-fun formal_0_482 () FormalMachine (FormalWriteFromOrigin formal_0_481 39 40))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:8]:initial-compare
(assert (not (m_panicked formal_0_482)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_482) (select (m_origin formal_0_482) 15) (select (m_origin formal_0_482) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_482) (select (m_origin formal_0_482) 15) (select (m_origin formal_0_482) 10)) false))
; source callback transition phase=insert-tail[33:45:8]:initial-compare
(define-fun formal_0_483 () FormalMachine (FormalCallback formal_0_482 boundary_0 (select (m_origin formal_0_482) 15) (select (m_origin formal_0_482) 10)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:8]
(define-fun formal_0_484 () FormalMachine (FormalWriteFromOrigin formal_0_483 41 10))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:8]:sift-compare
(assert (not (m_panicked formal_0_484)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_484) (select (m_origin formal_0_484) 15) (select (m_origin formal_0_484) 40)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_484) (select (m_origin formal_0_484) 15) (select (m_origin formal_0_484) 40)) false))
; source callback transition phase=insert-tail[33:45:8]:sift-compare
(define-fun formal_0_485 () FormalMachine (FormalCallback formal_0_484 boundary_0 (select (m_origin formal_0_484) 15) (select (m_origin formal_0_484) 40)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:45:8]
(define-fun formal_0_486 () FormalMachine (FormalWriteFromOrigin formal_0_485 40 15))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:9]:initial-compare
(assert (not (m_panicked formal_0_486)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_486) (select (m_origin formal_0_486) 42) (select (m_origin formal_0_486) 10)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_486) (select (m_origin formal_0_486) 42) (select (m_origin formal_0_486) 10)) false))
; source callback transition phase=insert-tail[33:45:9]:initial-compare
(define-fun formal_0_487 () FormalMachine (FormalCallback formal_0_486 boundary_0 (select (m_origin formal_0_486) 42) (select (m_origin formal_0_486) 10)))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:10]:initial-compare
(assert (not (m_panicked formal_0_487)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_487) (select (m_origin formal_0_487) 22) (select (m_origin formal_0_487) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_487) (select (m_origin formal_0_487) 22) (select (m_origin formal_0_487) 42)) false))
; source callback transition phase=insert-tail[33:45:10]:initial-compare
(define-fun formal_0_488 () FormalMachine (FormalCallback formal_0_487 boundary_0 (select (m_origin formal_0_487) 22) (select (m_origin formal_0_487) 42)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:10]
(define-fun formal_0_489 () FormalMachine (FormalWriteFromOrigin formal_0_488 43 42))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:10]:sift-compare
(assert (not (m_panicked formal_0_489)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_489) (select (m_origin formal_0_489) 22) (select (m_origin formal_0_489) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_489) (select (m_origin formal_0_489) 22) (select (m_origin formal_0_489) 10)) false))
; source callback transition phase=insert-tail[33:45:10]:sift-compare
(define-fun formal_0_490 () FormalMachine (FormalCallback formal_0_489 boundary_0 (select (m_origin formal_0_489) 22) (select (m_origin formal_0_489) 10)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:10]
(define-fun formal_0_491 () FormalMachine (FormalWriteFromOrigin formal_0_490 42 10))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:10]:sift-compare
(assert (not (m_panicked formal_0_491)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_491) (select (m_origin formal_0_491) 22) (select (m_origin formal_0_491) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_491) (select (m_origin formal_0_491) 22) (select (m_origin formal_0_491) 15)) false))
; source callback transition phase=insert-tail[33:45:10]:sift-compare
(define-fun formal_0_492 () FormalMachine (FormalCallback formal_0_491 boundary_0 (select (m_origin formal_0_491) 22) (select (m_origin formal_0_491) 15)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:10]
(define-fun formal_0_493 () FormalMachine (FormalWriteFromOrigin formal_0_492 41 15))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:10]:sift-compare
(assert (not (m_panicked formal_0_493)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_493) (select (m_origin formal_0_493) 22) (select (m_origin formal_0_493) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_493) (select (m_origin formal_0_493) 22) (select (m_origin formal_0_493) 40)) false))
; source callback transition phase=insert-tail[33:45:10]:sift-compare
(define-fun formal_0_494 () FormalMachine (FormalCallback formal_0_493 boundary_0 (select (m_origin formal_0_493) 22) (select (m_origin formal_0_493) 40)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:10]
(define-fun formal_0_495 () FormalMachine (FormalWriteFromOrigin formal_0_494 40 40))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:10]:sift-compare
(assert (not (m_panicked formal_0_495)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_495) (select (m_origin formal_0_495) 22) (select (m_origin formal_0_495) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_495) (select (m_origin formal_0_495) 22) (select (m_origin formal_0_495) 30)) false))
; source callback transition phase=insert-tail[33:45:10]:sift-compare
(define-fun formal_0_496 () FormalMachine (FormalCallback formal_0_495 boundary_0 (select (m_origin formal_0_495) 22) (select (m_origin formal_0_495) 30)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:10]
(define-fun formal_0_497 () FormalMachine (FormalWriteFromOrigin formal_0_496 39 30))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:10]:sift-compare
(assert (not (m_panicked formal_0_497)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_497) (select (m_origin formal_0_497) 22) (select (m_origin formal_0_497) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_497) (select (m_origin formal_0_497) 22) (select (m_origin formal_0_497) 16)) false))
; source callback transition phase=insert-tail[33:45:10]:sift-compare
(define-fun formal_0_498 () FormalMachine (FormalCallback formal_0_497 boundary_0 (select (m_origin formal_0_497) 22) (select (m_origin formal_0_497) 16)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:10]
(define-fun formal_0_499 () FormalMachine (FormalWriteFromOrigin formal_0_498 38 16))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:10]:sift-compare
(assert (not (m_panicked formal_0_499)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_499) (select (m_origin formal_0_499) 22) (select (m_origin formal_0_499) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_499) (select (m_origin formal_0_499) 22) (select (m_origin formal_0_499) 11)) false))
; source callback transition phase=insert-tail[33:45:10]:sift-compare
(define-fun formal_0_500 () FormalMachine (FormalCallback formal_0_499 boundary_0 (select (m_origin formal_0_499) 22) (select (m_origin formal_0_499) 11)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:10]
(define-fun formal_0_501 () FormalMachine (FormalWriteFromOrigin formal_0_500 37 11))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:10]:sift-compare
(assert (not (m_panicked formal_0_501)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_501) (select (m_origin formal_0_501) 22) (select (m_origin formal_0_501) 36)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_501) (select (m_origin formal_0_501) 22) (select (m_origin formal_0_501) 36)) false))
; source callback transition phase=insert-tail[33:45:10]:sift-compare
(define-fun formal_0_502 () FormalMachine (FormalCallback formal_0_501 boundary_0 (select (m_origin formal_0_501) 22) (select (m_origin formal_0_501) 36)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:45:10]
(define-fun formal_0_503 () FormalMachine (FormalWriteFromOrigin formal_0_502 36 22))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:initial-compare
(assert (not (m_panicked formal_0_503)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_503) (select (m_origin formal_0_503) 44) (select (m_origin formal_0_503) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_503) (select (m_origin formal_0_503) 44) (select (m_origin formal_0_503) 42)) false))
; source callback transition phase=insert-tail[33:45:11]:initial-compare
(define-fun formal_0_504 () FormalMachine (FormalCallback formal_0_503 boundary_0 (select (m_origin formal_0_503) 44) (select (m_origin formal_0_503) 42)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_505 () FormalMachine (FormalWriteFromOrigin formal_0_504 44 42))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:sift-compare
(assert (not (m_panicked formal_0_505)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_505) (select (m_origin formal_0_505) 44) (select (m_origin formal_0_505) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_505) (select (m_origin formal_0_505) 44) (select (m_origin formal_0_505) 10)) false))
; source callback transition phase=insert-tail[33:45:11]:sift-compare
(define-fun formal_0_506 () FormalMachine (FormalCallback formal_0_505 boundary_0 (select (m_origin formal_0_505) 44) (select (m_origin formal_0_505) 10)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_507 () FormalMachine (FormalWriteFromOrigin formal_0_506 43 10))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:sift-compare
(assert (not (m_panicked formal_0_507)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_507) (select (m_origin formal_0_507) 44) (select (m_origin formal_0_507) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_507) (select (m_origin formal_0_507) 44) (select (m_origin formal_0_507) 15)) false))
; source callback transition phase=insert-tail[33:45:11]:sift-compare
(define-fun formal_0_508 () FormalMachine (FormalCallback formal_0_507 boundary_0 (select (m_origin formal_0_507) 44) (select (m_origin formal_0_507) 15)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_509 () FormalMachine (FormalWriteFromOrigin formal_0_508 42 15))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:sift-compare
(assert (not (m_panicked formal_0_509)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_509) (select (m_origin formal_0_509) 44) (select (m_origin formal_0_509) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_509) (select (m_origin formal_0_509) 44) (select (m_origin formal_0_509) 40)) false))
; source callback transition phase=insert-tail[33:45:11]:sift-compare
(define-fun formal_0_510 () FormalMachine (FormalCallback formal_0_509 boundary_0 (select (m_origin formal_0_509) 44) (select (m_origin formal_0_509) 40)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_511 () FormalMachine (FormalWriteFromOrigin formal_0_510 41 40))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:sift-compare
(assert (not (m_panicked formal_0_511)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_511) (select (m_origin formal_0_511) 44) (select (m_origin formal_0_511) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_511) (select (m_origin formal_0_511) 44) (select (m_origin formal_0_511) 30)) false))
; source callback transition phase=insert-tail[33:45:11]:sift-compare
(define-fun formal_0_512 () FormalMachine (FormalCallback formal_0_511 boundary_0 (select (m_origin formal_0_511) 44) (select (m_origin formal_0_511) 30)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_513 () FormalMachine (FormalWriteFromOrigin formal_0_512 40 30))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:sift-compare
(assert (not (m_panicked formal_0_513)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_513) (select (m_origin formal_0_513) 44) (select (m_origin formal_0_513) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_513) (select (m_origin formal_0_513) 44) (select (m_origin formal_0_513) 16)) false))
; source callback transition phase=insert-tail[33:45:11]:sift-compare
(define-fun formal_0_514 () FormalMachine (FormalCallback formal_0_513 boundary_0 (select (m_origin formal_0_513) 44) (select (m_origin formal_0_513) 16)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_515 () FormalMachine (FormalWriteFromOrigin formal_0_514 39 16))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:sift-compare
(assert (not (m_panicked formal_0_515)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_515) (select (m_origin formal_0_515) 44) (select (m_origin formal_0_515) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_515) (select (m_origin formal_0_515) 44) (select (m_origin formal_0_515) 11)) false))
; source callback transition phase=insert-tail[33:45:11]:sift-compare
(define-fun formal_0_516 () FormalMachine (FormalCallback formal_0_515 boundary_0 (select (m_origin formal_0_515) 44) (select (m_origin formal_0_515) 11)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_517 () FormalMachine (FormalWriteFromOrigin formal_0_516 38 11))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:sift-compare
(assert (not (m_panicked formal_0_517)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_517) (select (m_origin formal_0_517) 44) (select (m_origin formal_0_517) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_517) (select (m_origin formal_0_517) 44) (select (m_origin formal_0_517) 22)) false))
; source callback transition phase=insert-tail[33:45:11]:sift-compare
(define-fun formal_0_518 () FormalMachine (FormalCallback formal_0_517 boundary_0 (select (m_origin formal_0_517) 44) (select (m_origin formal_0_517) 22)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_519 () FormalMachine (FormalWriteFromOrigin formal_0_518 37 22))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:sift-compare
(assert (not (m_panicked formal_0_519)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_519) (select (m_origin formal_0_519) 44) (select (m_origin formal_0_519) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_519) (select (m_origin formal_0_519) 44) (select (m_origin formal_0_519) 36)) false))
; source callback transition phase=insert-tail[33:45:11]:sift-compare
(define-fun formal_0_520 () FormalMachine (FormalCallback formal_0_519 boundary_0 (select (m_origin formal_0_519) 44) (select (m_origin formal_0_519) 36)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_521 () FormalMachine (FormalWriteFromOrigin formal_0_520 36 36))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:sift-compare
(assert (not (m_panicked formal_0_521)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_521) (select (m_origin formal_0_521) 44) (select (m_origin formal_0_521) 25)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_521) (select (m_origin formal_0_521) 44) (select (m_origin formal_0_521) 25)) false))
; source callback transition phase=insert-tail[33:45:11]:sift-compare
(define-fun formal_0_522 () FormalMachine (FormalCallback formal_0_521 boundary_0 (select (m_origin formal_0_521) 44) (select (m_origin formal_0_521) 25)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_523 () FormalMachine (FormalWriteFromOrigin formal_0_522 35 25))
; source callback case=cyclic-unroll-one-partition phase=insert-tail[33:45:11]:sift-compare
(assert (not (m_panicked formal_0_523)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_523) (select (m_origin formal_0_523) 44) (select (m_origin formal_0_523) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_523) (select (m_origin formal_0_523) 44) (select (m_origin formal_0_523) 37)) false))
; source callback transition phase=insert-tail[33:45:11]:sift-compare
(define-fun formal_0_524 () FormalMachine (FormalCallback formal_0_523 boundary_0 (select (m_origin formal_0_523) 44) (select (m_origin formal_0_523) 37)))
; source write kind=insert-tail-shift phase=insert-tail[33:45:11]
(define-fun formal_0_525 () FormalMachine (FormalWriteFromOrigin formal_0_524 34 37))
; source write kind=copy-on-drop-restore phase=insert-tail[33:45:11]
(define-fun formal_0_526 () FormalMachine (FormalWriteFromOrigin formal_0_525 33 44))
(define-fun formal_result_0 () Result
  (mkResult
    (m_sequence formal_0_526)
    (m_callback formal_0_526)
    (m_panicked formal_0_526)
    false
    true
    (ite (m_panicked formal_0_526) 1 0)
    (not (m_panicked formal_0_526))
    -1))
(define-fun reference_result_0 () Result (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 21 21) 22 22) 23 23) 24 24) 25 25) 26 26) 27 27) 28 28) 29 29) 30 30) 31 31) 32 32) 33 33) 34 34) 35 35) 36 36) 37 37) 38 38) 39 39) 40 40) 41 41) 42 42) 43 43) 44 44) 245 false false true 0 true -1))
; retained source-forcing witness: lomuto-cyclic
(assert (= formal_result_0 (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 21 21) 22 22) 23 23) 24 24) 25 25) 26 26) 27 27) 28 28) 29 29) 30 30) 31 31) 32 32) 33 33) 34 34) 35 35) 36 36) 37 37) 38 38) 39 39) 40 40) 41 41) 42 42) 43 43) 44 44) 245 false false true 0 true -1)))
(check-sat-using (then ctx-solver-simplify smt))
