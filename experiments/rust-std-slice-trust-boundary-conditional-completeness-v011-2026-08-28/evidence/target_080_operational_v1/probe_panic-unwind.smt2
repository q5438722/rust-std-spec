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

; formal source input case=general-small-sort-merge-restoration
(define-fun boundary_0 () Boundary
  (mkBoundary
    80
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) (or (= (call_state key) 102)))))
(define-fun configuration_0 () SortConfiguration
  (mkSortConfiguration
    false
    64
    24
    true
    true))
(define-fun source_initial_0 () FormalMachine
  (mkFormalMachine (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 14) 1 10) 2 9) 3 18) 4 22) 5 13) 6 2) 7 19) 8 7) 9 24) 10 8) 11 20) 12 3) 13 6) 14 0) 15 25) 16 16) 17 1) 18 15) 19 21) 20 5) 21 12) 22 11) 23 23) 24 17) 25 4) (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 14) 1 10) 2 9) 3 18) 4 22) 5 13) 6 2) 7 19) 8 7) 9 24) 10 8) 11 20) 12 3) 13 6) 14 0) 15 25) 16 16) 17 1) 18 15) 19 21) 20 5) 21 12) 22 11) 23 23) 24 17) 25 4) (b_initial_state boundary_0) false))
(assert (BoundaryWellFormed boundary_0))
; source callback case=general-small-sort-merge-restoration phase=find-existing-run:direction
(assert (not (m_panicked source_initial_0)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) false))
; source callback transition phase=find-existing-run:direction
(define-fun formal_0_1 () FormalMachine (FormalCallback source_initial_0 boundary_0 (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)))
; source callback case=general-small-sort-merge-restoration phase=find-existing-run:descending
(assert (not (m_panicked formal_0_1)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) false))
; source callback transition phase=find-existing-run:descending
(define-fun formal_0_2 () FormalMachine (FormalCallback formal_0_1 boundary_0 (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)))
; source callback case=general-small-sort-merge-restoration phase=find-existing-run:descending
(assert (not (m_panicked formal_0_2)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 3) (select (m_origin formal_0_2) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 3) (select (m_origin formal_0_2) 2)) false))
; source callback transition phase=find-existing-run:descending
(define-fun formal_0_3 () FormalMachine (FormalCallback formal_0_2 boundary_0 (select (m_origin formal_0_2) 3) (select (m_origin formal_0_2) 2)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:left-sort4:c1
(assert (not (m_panicked formal_0_3)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 1) (select (m_origin formal_0_3) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 1) (select (m_origin formal_0_3) 0)) false))
; source callback transition phase=small-sort-general:left-sort4:c1
(define-fun formal_0_4 () FormalMachine (FormalCallback formal_0_3 boundary_0 (select (m_origin formal_0_3) 1) (select (m_origin formal_0_3) 0)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:left-sort4:c2
(assert (not (m_panicked formal_0_4)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 3) (select (m_origin formal_0_4) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 3) (select (m_origin formal_0_4) 2)) false))
; source callback transition phase=small-sort-general:left-sort4:c2
(define-fun formal_0_5 () FormalMachine (FormalCallback formal_0_4 boundary_0 (select (m_origin formal_0_4) 3) (select (m_origin formal_0_4) 2)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:left-sort4:c3
(assert (not (m_panicked formal_0_5)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_5) (select (m_origin formal_0_5) 2) (select (m_origin formal_0_5) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_5) (select (m_origin formal_0_5) 2) (select (m_origin formal_0_5) 1)) false))
; source callback transition phase=small-sort-general:left-sort4:c3
(define-fun formal_0_6 () FormalMachine (FormalCallback formal_0_5 boundary_0 (select (m_origin formal_0_5) 2) (select (m_origin formal_0_5) 1)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:left-sort4:c4
(assert (not (m_panicked formal_0_6)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 3) (select (m_origin formal_0_6) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 3) (select (m_origin formal_0_6) 0)) false))
; source callback transition phase=small-sort-general:left-sort4:c4
(define-fun formal_0_7 () FormalMachine (FormalCallback formal_0_6 boundary_0 (select (m_origin formal_0_6) 3) (select (m_origin formal_0_6) 0)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:left-sort4:c5
(assert (not (m_panicked formal_0_7)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_7) (select (m_origin formal_0_7) 0) (select (m_origin formal_0_7) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_7) (select (m_origin formal_0_7) 0) (select (m_origin formal_0_7) 1)) false))
; source callback transition phase=small-sort-general:left-sort4:c5
(define-fun formal_0_8 () FormalMachine (FormalCallback formal_0_7 boundary_0 (select (m_origin formal_0_7) 0) (select (m_origin formal_0_7) 1)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:right-sort4:c1
(assert (not (m_panicked formal_0_8)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 14) (select (m_origin formal_0_8) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 14) (select (m_origin formal_0_8) 13)) false))
; source callback transition phase=small-sort-general:right-sort4:c1
(define-fun formal_0_9 () FormalMachine (FormalCallback formal_0_8 boundary_0 (select (m_origin formal_0_8) 14) (select (m_origin formal_0_8) 13)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:right-sort4:c2
(assert (not (m_panicked formal_0_9)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_9) (select (m_origin formal_0_9) 16) (select (m_origin formal_0_9) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_9) (select (m_origin formal_0_9) 16) (select (m_origin formal_0_9) 15)) false))
; source callback transition phase=small-sort-general:right-sort4:c2
(define-fun formal_0_10 () FormalMachine (FormalCallback formal_0_9 boundary_0 (select (m_origin formal_0_9) 16) (select (m_origin formal_0_9) 15)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:right-sort4:c3
(assert (not (m_panicked formal_0_10)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_10) (select (m_origin formal_0_10) 16) (select (m_origin formal_0_10) 14)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_10) (select (m_origin formal_0_10) 16) (select (m_origin formal_0_10) 14)) false))
; source callback transition phase=small-sort-general:right-sort4:c3
(define-fun formal_0_11 () FormalMachine (FormalCallback formal_0_10 boundary_0 (select (m_origin formal_0_10) 16) (select (m_origin formal_0_10) 14)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:right-sort4:c4
(assert (not (m_panicked formal_0_11)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_11) (select (m_origin formal_0_11) 15) (select (m_origin formal_0_11) 13)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_11) (select (m_origin formal_0_11) 15) (select (m_origin formal_0_11) 13)) false))
; source callback transition phase=small-sort-general:right-sort4:c4
(define-fun formal_0_12 () FormalMachine (FormalCallback formal_0_11 boundary_0 (select (m_origin formal_0_11) 15) (select (m_origin formal_0_11) 13)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:right-sort4:c5
(assert (not (m_panicked formal_0_12)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_12) (select (m_origin formal_0_12) 16) (select (m_origin formal_0_12) 13)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_12) (select (m_origin formal_0_12) 16) (select (m_origin formal_0_12) 13)) false))
; source callback transition phase=small-sort-general:right-sort4:c5
(define-fun formal_0_13 () FormalMachine (FormalCallback formal_0_12 boundary_0 (select (m_origin formal_0_12) 16) (select (m_origin formal_0_12) 13)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:4]:initial-compare
(assert (not (m_panicked formal_0_13)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_13) (select (m_origin formal_0_13) 4) (select (m_origin formal_0_13) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_13) (select (m_origin formal_0_13) 4) (select (m_origin formal_0_13) 3)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:4]:initial-compare
(define-fun formal_0_14 () FormalMachine (FormalCallback formal_0_13 boundary_0 (select (m_origin formal_0_13) 4) (select (m_origin formal_0_13) 3)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:5]:initial-compare
(assert (not (m_panicked formal_0_14)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_14) (select (m_origin formal_0_14) 5) (select (m_origin formal_0_14) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_14) (select (m_origin formal_0_14) 5) (select (m_origin formal_0_14) 4)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:5]:initial-compare
(define-fun formal_0_15 () FormalMachine (FormalCallback formal_0_14 boundary_0 (select (m_origin formal_0_14) 5) (select (m_origin formal_0_14) 4)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:5]:sift-compare
(assert (not (m_panicked formal_0_15)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_15) (select (m_origin formal_0_15) 5) (select (m_origin formal_0_15) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_15) (select (m_origin formal_0_15) 5) (select (m_origin formal_0_15) 3)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:5]:sift-compare
(define-fun formal_0_16 () FormalMachine (FormalCallback formal_0_15 boundary_0 (select (m_origin formal_0_15) 5) (select (m_origin formal_0_15) 3)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:5]:sift-compare
(assert (not (m_panicked formal_0_16)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_16) (select (m_origin formal_0_16) 5) (select (m_origin formal_0_16) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_16) (select (m_origin formal_0_16) 5) (select (m_origin formal_0_16) 0)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:5]:sift-compare
(define-fun formal_0_17 () FormalMachine (FormalCallback formal_0_16 boundary_0 (select (m_origin formal_0_16) 5) (select (m_origin formal_0_16) 0)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:5]:sift-compare
(assert (not (m_panicked formal_0_17)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_17) (select (m_origin formal_0_17) 5) (select (m_origin formal_0_17) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_17) (select (m_origin formal_0_17) 5) (select (m_origin formal_0_17) 1)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:5]:sift-compare
(define-fun formal_0_18 () FormalMachine (FormalCallback formal_0_17 boundary_0 (select (m_origin formal_0_17) 5) (select (m_origin formal_0_17) 1)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:6]:initial-compare
(assert (not (m_panicked formal_0_18)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_18) (select (m_origin formal_0_18) 6) (select (m_origin formal_0_18) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_18) (select (m_origin formal_0_18) 6) (select (m_origin formal_0_18) 4)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:6]:initial-compare
(define-fun formal_0_19 () FormalMachine (FormalCallback formal_0_18 boundary_0 (select (m_origin formal_0_18) 6) (select (m_origin formal_0_18) 4)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:6]:sift-compare
(assert (not (m_panicked formal_0_19)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_19) (select (m_origin formal_0_19) 6) (select (m_origin formal_0_19) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_19) (select (m_origin formal_0_19) 6) (select (m_origin formal_0_19) 3)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:6]:sift-compare
(define-fun formal_0_20 () FormalMachine (FormalCallback formal_0_19 boundary_0 (select (m_origin formal_0_19) 6) (select (m_origin formal_0_19) 3)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:6]:sift-compare
(assert (not (m_panicked formal_0_20)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 6) (select (m_origin formal_0_20) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 6) (select (m_origin formal_0_20) 0)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:6]:sift-compare
(define-fun formal_0_21 () FormalMachine (FormalCallback formal_0_20 boundary_0 (select (m_origin formal_0_20) 6) (select (m_origin formal_0_20) 0)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:6]:sift-compare
(assert (not (m_panicked formal_0_21)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_21) (select (m_origin formal_0_21) 6) (select (m_origin formal_0_21) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_21) (select (m_origin formal_0_21) 6) (select (m_origin formal_0_21) 5)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:6]:sift-compare
(define-fun formal_0_22 () FormalMachine (FormalCallback formal_0_21 boundary_0 (select (m_origin formal_0_21) 6) (select (m_origin formal_0_21) 5)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:6]:sift-compare
(assert (not (m_panicked formal_0_22)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_22) (select (m_origin formal_0_22) 6) (select (m_origin formal_0_22) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_22) (select (m_origin formal_0_22) 6) (select (m_origin formal_0_22) 1)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:6]:sift-compare
(define-fun formal_0_23 () FormalMachine (FormalCallback formal_0_22 boundary_0 (select (m_origin formal_0_22) 6) (select (m_origin formal_0_22) 1)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:6]:sift-compare
(assert (not (m_panicked formal_0_23)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_23) (select (m_origin formal_0_23) 6) (select (m_origin formal_0_23) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_23) (select (m_origin formal_0_23) 6) (select (m_origin formal_0_23) 2)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:6]:sift-compare
(define-fun formal_0_24 () FormalMachine (FormalCallback formal_0_23 boundary_0 (select (m_origin formal_0_23) 6) (select (m_origin formal_0_23) 2)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:7]:initial-compare
(assert (not (m_panicked formal_0_24)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_24) (select (m_origin formal_0_24) 7) (select (m_origin formal_0_24) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_24) (select (m_origin formal_0_24) 7) (select (m_origin formal_0_24) 4)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:7]:initial-compare
(define-fun formal_0_25 () FormalMachine (FormalCallback formal_0_24 boundary_0 (select (m_origin formal_0_24) 7) (select (m_origin formal_0_24) 4)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:7]:sift-compare
(assert (not (m_panicked formal_0_25)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 7) (select (m_origin formal_0_25) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 7) (select (m_origin formal_0_25) 3)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:7]:sift-compare
(define-fun formal_0_26 () FormalMachine (FormalCallback formal_0_25 boundary_0 (select (m_origin formal_0_25) 7) (select (m_origin formal_0_25) 3)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:8]:initial-compare
(assert (not (m_panicked formal_0_26)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_26) (select (m_origin formal_0_26) 8) (select (m_origin formal_0_26) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_26) (select (m_origin formal_0_26) 8) (select (m_origin formal_0_26) 4)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:8]:initial-compare
(define-fun formal_0_27 () FormalMachine (FormalCallback formal_0_26 boundary_0 (select (m_origin formal_0_26) 8) (select (m_origin formal_0_26) 4)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(assert (not (m_panicked formal_0_27)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_27) (select (m_origin formal_0_27) 8) (select (m_origin formal_0_27) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_27) (select (m_origin formal_0_27) 8) (select (m_origin formal_0_27) 7)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(define-fun formal_0_28 () FormalMachine (FormalCallback formal_0_27 boundary_0 (select (m_origin formal_0_27) 8) (select (m_origin formal_0_27) 7)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(assert (not (m_panicked formal_0_28)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_28) (select (m_origin formal_0_28) 8) (select (m_origin formal_0_28) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_28) (select (m_origin formal_0_28) 8) (select (m_origin formal_0_28) 3)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(define-fun formal_0_29 () FormalMachine (FormalCallback formal_0_28 boundary_0 (select (m_origin formal_0_28) 8) (select (m_origin formal_0_28) 3)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(assert (not (m_panicked formal_0_29)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_29) (select (m_origin formal_0_29) 8) (select (m_origin formal_0_29) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_29) (select (m_origin formal_0_29) 8) (select (m_origin formal_0_29) 0)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(define-fun formal_0_30 () FormalMachine (FormalCallback formal_0_29 boundary_0 (select (m_origin formal_0_29) 8) (select (m_origin formal_0_29) 0)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(assert (not (m_panicked formal_0_30)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_30) (select (m_origin formal_0_30) 8) (select (m_origin formal_0_30) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_30) (select (m_origin formal_0_30) 8) (select (m_origin formal_0_30) 5)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(define-fun formal_0_31 () FormalMachine (FormalCallback formal_0_30 boundary_0 (select (m_origin formal_0_30) 8) (select (m_origin formal_0_30) 5)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(assert (not (m_panicked formal_0_31)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_31) (select (m_origin formal_0_31) 8) (select (m_origin formal_0_31) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_31) (select (m_origin formal_0_31) 8) (select (m_origin formal_0_31) 1)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(define-fun formal_0_32 () FormalMachine (FormalCallback formal_0_31 boundary_0 (select (m_origin formal_0_31) 8) (select (m_origin formal_0_31) 1)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(assert (not (m_panicked formal_0_32)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_32) (select (m_origin formal_0_32) 8) (select (m_origin formal_0_32) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_32) (select (m_origin formal_0_32) 8) (select (m_origin formal_0_32) 2)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(define-fun formal_0_33 () FormalMachine (FormalCallback formal_0_32 boundary_0 (select (m_origin formal_0_32) 8) (select (m_origin formal_0_32) 2)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(assert (not (m_panicked formal_0_33)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_33) (select (m_origin formal_0_33) 8) (select (m_origin formal_0_33) 6)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_33) (select (m_origin formal_0_33) 8) (select (m_origin formal_0_33) 6)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:8]:sift-compare
(define-fun formal_0_34 () FormalMachine (FormalCallback formal_0_33 boundary_0 (select (m_origin formal_0_33) 8) (select (m_origin formal_0_33) 6)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:9]:initial-compare
(assert (not (m_panicked formal_0_34)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_34) (select (m_origin formal_0_34) 9) (select (m_origin formal_0_34) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_34) (select (m_origin formal_0_34) 9) (select (m_origin formal_0_34) 4)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:9]:initial-compare
(define-fun formal_0_35 () FormalMachine (FormalCallback formal_0_34 boundary_0 (select (m_origin formal_0_34) 9) (select (m_origin formal_0_34) 4)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:10]:initial-compare
(assert (not (m_panicked formal_0_35)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_35) (select (m_origin formal_0_35) 10) (select (m_origin formal_0_35) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_35) (select (m_origin formal_0_35) 10) (select (m_origin formal_0_35) 9)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:10]:initial-compare
(define-fun formal_0_36 () FormalMachine (FormalCallback formal_0_35 boundary_0 (select (m_origin formal_0_35) 10) (select (m_origin formal_0_35) 9)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(assert (not (m_panicked formal_0_36)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_36) (select (m_origin formal_0_36) 10) (select (m_origin formal_0_36) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_36) (select (m_origin formal_0_36) 10) (select (m_origin formal_0_36) 4)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(define-fun formal_0_37 () FormalMachine (FormalCallback formal_0_36 boundary_0 (select (m_origin formal_0_36) 10) (select (m_origin formal_0_36) 4)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(assert (not (m_panicked formal_0_37)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_37) (select (m_origin formal_0_37) 10) (select (m_origin formal_0_37) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_37) (select (m_origin formal_0_37) 10) (select (m_origin formal_0_37) 7)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(define-fun formal_0_38 () FormalMachine (FormalCallback formal_0_37 boundary_0 (select (m_origin formal_0_37) 10) (select (m_origin formal_0_37) 7)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(assert (not (m_panicked formal_0_38)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 10) (select (m_origin formal_0_38) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 10) (select (m_origin formal_0_38) 3)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(define-fun formal_0_39 () FormalMachine (FormalCallback formal_0_38 boundary_0 (select (m_origin formal_0_38) 10) (select (m_origin formal_0_38) 3)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(assert (not (m_panicked formal_0_39)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_39) (select (m_origin formal_0_39) 10) (select (m_origin formal_0_39) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_39) (select (m_origin formal_0_39) 10) (select (m_origin formal_0_39) 0)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(define-fun formal_0_40 () FormalMachine (FormalCallback formal_0_39 boundary_0 (select (m_origin formal_0_39) 10) (select (m_origin formal_0_39) 0)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(assert (not (m_panicked formal_0_40)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_40) (select (m_origin formal_0_40) 10) (select (m_origin formal_0_40) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_40) (select (m_origin formal_0_40) 10) (select (m_origin formal_0_40) 5)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(define-fun formal_0_41 () FormalMachine (FormalCallback formal_0_40 boundary_0 (select (m_origin formal_0_40) 10) (select (m_origin formal_0_40) 5)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(assert (not (m_panicked formal_0_41)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 10) (select (m_origin formal_0_41) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 10) (select (m_origin formal_0_41) 1)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(define-fun formal_0_42 () FormalMachine (FormalCallback formal_0_41 boundary_0 (select (m_origin formal_0_41) 10) (select (m_origin formal_0_41) 1)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(assert (not (m_panicked formal_0_42)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_42) (select (m_origin formal_0_42) 10) (select (m_origin formal_0_42) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_42) (select (m_origin formal_0_42) 10) (select (m_origin formal_0_42) 2)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(define-fun formal_0_43 () FormalMachine (FormalCallback formal_0_42 boundary_0 (select (m_origin formal_0_42) 10) (select (m_origin formal_0_42) 2)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(assert (not (m_panicked formal_0_43)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_43) (select (m_origin formal_0_43) 10) (select (m_origin formal_0_43) 8)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_43) (select (m_origin formal_0_43) 10) (select (m_origin formal_0_43) 8)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:10]:sift-compare
(define-fun formal_0_44 () FormalMachine (FormalCallback formal_0_43 boundary_0 (select (m_origin formal_0_43) 10) (select (m_origin formal_0_43) 8)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:11]:initial-compare
(assert (not (m_panicked formal_0_44)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 11) (select (m_origin formal_0_44) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 11) (select (m_origin formal_0_44) 9)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:11]:initial-compare
(define-fun formal_0_45 () FormalMachine (FormalCallback formal_0_44 boundary_0 (select (m_origin formal_0_44) 11) (select (m_origin formal_0_44) 9)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:11]:sift-compare
(assert (not (m_panicked formal_0_45)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_45) (select (m_origin formal_0_45) 11) (select (m_origin formal_0_45) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_45) (select (m_origin formal_0_45) 11) (select (m_origin formal_0_45) 4)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:11]:sift-compare
(define-fun formal_0_46 () FormalMachine (FormalCallback formal_0_45 boundary_0 (select (m_origin formal_0_45) 11) (select (m_origin formal_0_45) 4)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:11]:sift-compare
(assert (not (m_panicked formal_0_46)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_46) (select (m_origin formal_0_46) 11) (select (m_origin formal_0_46) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_46) (select (m_origin formal_0_46) 11) (select (m_origin formal_0_46) 7)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:11]:sift-compare
(define-fun formal_0_47 () FormalMachine (FormalCallback formal_0_46 boundary_0 (select (m_origin formal_0_46) 11) (select (m_origin formal_0_46) 7)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:initial-compare
(assert (not (m_panicked formal_0_47)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_47) (select (m_origin formal_0_47) 12) (select (m_origin formal_0_47) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_47) (select (m_origin formal_0_47) 12) (select (m_origin formal_0_47) 9)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:initial-compare
(define-fun formal_0_48 () FormalMachine (FormalCallback formal_0_47 boundary_0 (select (m_origin formal_0_47) 12) (select (m_origin formal_0_47) 9)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_48)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 12) (select (m_origin formal_0_48) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 12) (select (m_origin formal_0_48) 4)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_49 () FormalMachine (FormalCallback formal_0_48 boundary_0 (select (m_origin formal_0_48) 12) (select (m_origin formal_0_48) 4)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_49)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_49) (select (m_origin formal_0_49) 12) (select (m_origin formal_0_49) 11)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_49) (select (m_origin formal_0_49) 12) (select (m_origin formal_0_49) 11)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_50 () FormalMachine (FormalCallback formal_0_49 boundary_0 (select (m_origin formal_0_49) 12) (select (m_origin formal_0_49) 11)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_50)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_50) (select (m_origin formal_0_50) 12) (select (m_origin formal_0_50) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_50) (select (m_origin formal_0_50) 12) (select (m_origin formal_0_50) 7)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_51 () FormalMachine (FormalCallback formal_0_50 boundary_0 (select (m_origin formal_0_50) 12) (select (m_origin formal_0_50) 7)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_51)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_51) (select (m_origin formal_0_51) 12) (select (m_origin formal_0_51) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_51) (select (m_origin formal_0_51) 12) (select (m_origin formal_0_51) 3)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_52 () FormalMachine (FormalCallback formal_0_51 boundary_0 (select (m_origin formal_0_51) 12) (select (m_origin formal_0_51) 3)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_52)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_52) (select (m_origin formal_0_52) 12) (select (m_origin formal_0_52) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_52) (select (m_origin formal_0_52) 12) (select (m_origin formal_0_52) 0)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_53 () FormalMachine (FormalCallback formal_0_52 boundary_0 (select (m_origin formal_0_52) 12) (select (m_origin formal_0_52) 0)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_53)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_53) (select (m_origin formal_0_53) 12) (select (m_origin formal_0_53) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_53) (select (m_origin formal_0_53) 12) (select (m_origin formal_0_53) 5)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_54 () FormalMachine (FormalCallback formal_0_53 boundary_0 (select (m_origin formal_0_53) 12) (select (m_origin formal_0_53) 5)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_54)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_54) (select (m_origin formal_0_54) 12) (select (m_origin formal_0_54) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_54) (select (m_origin formal_0_54) 12) (select (m_origin formal_0_54) 1)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_55 () FormalMachine (FormalCallback formal_0_54 boundary_0 (select (m_origin formal_0_54) 12) (select (m_origin formal_0_54) 1)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_55)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_55) (select (m_origin formal_0_55) 12) (select (m_origin formal_0_55) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_55) (select (m_origin formal_0_55) 12) (select (m_origin formal_0_55) 2)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_56 () FormalMachine (FormalCallback formal_0_55 boundary_0 (select (m_origin formal_0_55) 12) (select (m_origin formal_0_55) 2)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_56)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_56) (select (m_origin formal_0_56) 12) (select (m_origin formal_0_56) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_56) (select (m_origin formal_0_56) 12) (select (m_origin formal_0_56) 10)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_57 () FormalMachine (FormalCallback formal_0_56 boundary_0 (select (m_origin formal_0_56) 12) (select (m_origin formal_0_56) 10)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_57)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_57) (select (m_origin formal_0_57) 12) (select (m_origin formal_0_57) 8)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_57) (select (m_origin formal_0_57) 12) (select (m_origin formal_0_57) 8)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_58 () FormalMachine (FormalCallback formal_0_57 boundary_0 (select (m_origin formal_0_57) 12) (select (m_origin formal_0_57) 8)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(assert (not (m_panicked formal_0_58)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_58) (select (m_origin formal_0_58) 12) (select (m_origin formal_0_58) 6)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_58) (select (m_origin formal_0_58) 12) (select (m_origin formal_0_58) 6)) false))
; source callback transition phase=small-sort-general:insert-tail[0:13:12]:sift-compare
(define-fun formal_0_59 () FormalMachine (FormalCallback formal_0_58 boundary_0 (select (m_origin formal_0_58) 12) (select (m_origin formal_0_58) 6)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:4]:initial-compare
(assert (not (m_panicked formal_0_59)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_59) (select (m_origin formal_0_59) 17) (select (m_origin formal_0_59) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_59) (select (m_origin formal_0_59) 17) (select (m_origin formal_0_59) 15)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:4]:initial-compare
(define-fun formal_0_60 () FormalMachine (FormalCallback formal_0_59 boundary_0 (select (m_origin formal_0_59) 17) (select (m_origin formal_0_59) 15)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:4]:sift-compare
(assert (not (m_panicked formal_0_60)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_60) (select (m_origin formal_0_60) 17) (select (m_origin formal_0_60) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_60) (select (m_origin formal_0_60) 17) (select (m_origin formal_0_60) 16)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:4]:sift-compare
(define-fun formal_0_61 () FormalMachine (FormalCallback formal_0_60 boundary_0 (select (m_origin formal_0_60) 17) (select (m_origin formal_0_60) 16)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:4]:sift-compare
(assert (not (m_panicked formal_0_61)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_61) (select (m_origin formal_0_61) 17) (select (m_origin formal_0_61) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_61) (select (m_origin formal_0_61) 17) (select (m_origin formal_0_61) 13)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:4]:sift-compare
(define-fun formal_0_62 () FormalMachine (FormalCallback formal_0_61 boundary_0 (select (m_origin formal_0_61) 17) (select (m_origin formal_0_61) 13)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:4]:sift-compare
(assert (not (m_panicked formal_0_62)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_62) (select (m_origin formal_0_62) 17) (select (m_origin formal_0_62) 14)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_62) (select (m_origin formal_0_62) 17) (select (m_origin formal_0_62) 14)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:4]:sift-compare
(define-fun formal_0_63 () FormalMachine (FormalCallback formal_0_62 boundary_0 (select (m_origin formal_0_62) 17) (select (m_origin formal_0_62) 14)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:5]:initial-compare
(assert (not (m_panicked formal_0_63)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_63) (select (m_origin formal_0_63) 18) (select (m_origin formal_0_63) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_63) (select (m_origin formal_0_63) 18) (select (m_origin formal_0_63) 15)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:5]:initial-compare
(define-fun formal_0_64 () FormalMachine (FormalCallback formal_0_63 boundary_0 (select (m_origin formal_0_63) 18) (select (m_origin formal_0_63) 15)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:5]:sift-compare
(assert (not (m_panicked formal_0_64)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_64) (select (m_origin formal_0_64) 18) (select (m_origin formal_0_64) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_64) (select (m_origin formal_0_64) 18) (select (m_origin formal_0_64) 16)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:5]:sift-compare
(define-fun formal_0_65 () FormalMachine (FormalCallback formal_0_64 boundary_0 (select (m_origin formal_0_64) 18) (select (m_origin formal_0_64) 16)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:5]:sift-compare
(assert (not (m_panicked formal_0_65)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_65) (select (m_origin formal_0_65) 18) (select (m_origin formal_0_65) 13)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_65) (select (m_origin formal_0_65) 18) (select (m_origin formal_0_65) 13)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:5]:sift-compare
(define-fun formal_0_66 () FormalMachine (FormalCallback formal_0_65 boundary_0 (select (m_origin formal_0_65) 18) (select (m_origin formal_0_65) 13)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:6]:initial-compare
(assert (not (m_panicked formal_0_66)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_66) (select (m_origin formal_0_66) 19) (select (m_origin formal_0_66) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_66) (select (m_origin formal_0_66) 19) (select (m_origin formal_0_66) 15)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:6]:initial-compare
(define-fun formal_0_67 () FormalMachine (FormalCallback formal_0_66 boundary_0 (select (m_origin formal_0_66) 19) (select (m_origin formal_0_66) 15)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:6]:sift-compare
(assert (not (m_panicked formal_0_67)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_67) (select (m_origin formal_0_67) 19) (select (m_origin formal_0_67) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_67) (select (m_origin formal_0_67) 19) (select (m_origin formal_0_67) 16)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:6]:sift-compare
(define-fun formal_0_68 () FormalMachine (FormalCallback formal_0_67 boundary_0 (select (m_origin formal_0_67) 19) (select (m_origin formal_0_67) 16)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:7]:initial-compare
(assert (not (m_panicked formal_0_68)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_68) (select (m_origin formal_0_68) 20) (select (m_origin formal_0_68) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_68) (select (m_origin formal_0_68) 20) (select (m_origin formal_0_68) 15)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:7]:initial-compare
(define-fun formal_0_69 () FormalMachine (FormalCallback formal_0_68 boundary_0 (select (m_origin formal_0_68) 20) (select (m_origin formal_0_68) 15)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:7]:sift-compare
(assert (not (m_panicked formal_0_69)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 20) (select (m_origin formal_0_69) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 20) (select (m_origin formal_0_69) 19)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:7]:sift-compare
(define-fun formal_0_70 () FormalMachine (FormalCallback formal_0_69 boundary_0 (select (m_origin formal_0_69) 20) (select (m_origin formal_0_69) 19)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:7]:sift-compare
(assert (not (m_panicked formal_0_70)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_70) (select (m_origin formal_0_70) 20) (select (m_origin formal_0_70) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_70) (select (m_origin formal_0_70) 20) (select (m_origin formal_0_70) 16)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:7]:sift-compare
(define-fun formal_0_71 () FormalMachine (FormalCallback formal_0_70 boundary_0 (select (m_origin formal_0_70) 20) (select (m_origin formal_0_70) 16)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:7]:sift-compare
(assert (not (m_panicked formal_0_71)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_71) (select (m_origin formal_0_71) 20) (select (m_origin formal_0_71) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_71) (select (m_origin formal_0_71) 20) (select (m_origin formal_0_71) 18)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:7]:sift-compare
(define-fun formal_0_72 () FormalMachine (FormalCallback formal_0_71 boundary_0 (select (m_origin formal_0_71) 20) (select (m_origin formal_0_71) 18)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:7]:sift-compare
(assert (not (m_panicked formal_0_72)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_72) (select (m_origin formal_0_72) 20) (select (m_origin formal_0_72) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_72) (select (m_origin formal_0_72) 20) (select (m_origin formal_0_72) 13)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:7]:sift-compare
(define-fun formal_0_73 () FormalMachine (FormalCallback formal_0_72 boundary_0 (select (m_origin formal_0_72) 20) (select (m_origin formal_0_72) 13)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:7]:sift-compare
(assert (not (m_panicked formal_0_73)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 20) (select (m_origin formal_0_73) 17)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 20) (select (m_origin formal_0_73) 17)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:7]:sift-compare
(define-fun formal_0_74 () FormalMachine (FormalCallback formal_0_73 boundary_0 (select (m_origin formal_0_73) 20) (select (m_origin formal_0_73) 17)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:8]:initial-compare
(assert (not (m_panicked formal_0_74)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_74) (select (m_origin formal_0_74) 21) (select (m_origin formal_0_74) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_74) (select (m_origin formal_0_74) 21) (select (m_origin formal_0_74) 15)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:8]:initial-compare
(define-fun formal_0_75 () FormalMachine (FormalCallback formal_0_74 boundary_0 (select (m_origin formal_0_74) 21) (select (m_origin formal_0_74) 15)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:8]:sift-compare
(assert (not (m_panicked formal_0_75)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 21) (select (m_origin formal_0_75) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 21) (select (m_origin formal_0_75) 19)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:8]:sift-compare
(define-fun formal_0_76 () FormalMachine (FormalCallback formal_0_75 boundary_0 (select (m_origin formal_0_75) 21) (select (m_origin formal_0_75) 19)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:8]:sift-compare
(assert (not (m_panicked formal_0_76)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_76) (select (m_origin formal_0_76) 21) (select (m_origin formal_0_76) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_76) (select (m_origin formal_0_76) 21) (select (m_origin formal_0_76) 16)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:8]:sift-compare
(define-fun formal_0_77 () FormalMachine (FormalCallback formal_0_76 boundary_0 (select (m_origin formal_0_76) 21) (select (m_origin formal_0_76) 16)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:8]:sift-compare
(assert (not (m_panicked formal_0_77)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_77) (select (m_origin formal_0_77) 21) (select (m_origin formal_0_77) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_77) (select (m_origin formal_0_77) 21) (select (m_origin formal_0_77) 18)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:8]:sift-compare
(define-fun formal_0_78 () FormalMachine (FormalCallback formal_0_77 boundary_0 (select (m_origin formal_0_77) 21) (select (m_origin formal_0_77) 18)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:8]:sift-compare
(assert (not (m_panicked formal_0_78)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 21) (select (m_origin formal_0_78) 13)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 21) (select (m_origin formal_0_78) 13)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:8]:sift-compare
(define-fun formal_0_79 () FormalMachine (FormalCallback formal_0_78 boundary_0 (select (m_origin formal_0_78) 21) (select (m_origin formal_0_78) 13)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:9]:initial-compare
(assert (not (m_panicked formal_0_79)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_79) (select (m_origin formal_0_79) 22) (select (m_origin formal_0_79) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_79) (select (m_origin formal_0_79) 22) (select (m_origin formal_0_79) 15)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:9]:initial-compare
(define-fun formal_0_80 () FormalMachine (FormalCallback formal_0_79 boundary_0 (select (m_origin formal_0_79) 22) (select (m_origin formal_0_79) 15)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:9]:sift-compare
(assert (not (m_panicked formal_0_80)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_80) (select (m_origin formal_0_80) 22) (select (m_origin formal_0_80) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_80) (select (m_origin formal_0_80) 22) (select (m_origin formal_0_80) 19)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:9]:sift-compare
(define-fun formal_0_81 () FormalMachine (FormalCallback formal_0_80 boundary_0 (select (m_origin formal_0_80) 22) (select (m_origin formal_0_80) 19)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:9]:sift-compare
(assert (not (m_panicked formal_0_81)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 22) (select (m_origin formal_0_81) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 22) (select (m_origin formal_0_81) 16)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:9]:sift-compare
(define-fun formal_0_82 () FormalMachine (FormalCallback formal_0_81 boundary_0 (select (m_origin formal_0_81) 22) (select (m_origin formal_0_81) 16)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:9]:sift-compare
(assert (not (m_panicked formal_0_82)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_82) (select (m_origin formal_0_82) 22) (select (m_origin formal_0_82) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_82) (select (m_origin formal_0_82) 22) (select (m_origin formal_0_82) 18)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:9]:sift-compare
(define-fun formal_0_83 () FormalMachine (FormalCallback formal_0_82 boundary_0 (select (m_origin formal_0_82) 22) (select (m_origin formal_0_82) 18)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:9]:sift-compare
(assert (not (m_panicked formal_0_83)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_83) (select (m_origin formal_0_83) 22) (select (m_origin formal_0_83) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_83) (select (m_origin formal_0_83) 22) (select (m_origin formal_0_83) 21)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:9]:sift-compare
(define-fun formal_0_84 () FormalMachine (FormalCallback formal_0_83 boundary_0 (select (m_origin formal_0_83) 22) (select (m_origin formal_0_83) 21)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:9]:sift-compare
(assert (not (m_panicked formal_0_84)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_84) (select (m_origin formal_0_84) 22) (select (m_origin formal_0_84) 13)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_84) (select (m_origin formal_0_84) 22) (select (m_origin formal_0_84) 13)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:9]:sift-compare
(define-fun formal_0_85 () FormalMachine (FormalCallback formal_0_84 boundary_0 (select (m_origin formal_0_84) 22) (select (m_origin formal_0_84) 13)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:10]:initial-compare
(assert (not (m_panicked formal_0_85)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_85) (select (m_origin formal_0_85) 23) (select (m_origin formal_0_85) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_85) (select (m_origin formal_0_85) 23) (select (m_origin formal_0_85) 15)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:10]:initial-compare
(define-fun formal_0_86 () FormalMachine (FormalCallback formal_0_85 boundary_0 (select (m_origin formal_0_85) 23) (select (m_origin formal_0_85) 15)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:10]:sift-compare
(assert (not (m_panicked formal_0_86)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 23) (select (m_origin formal_0_86) 19)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 23) (select (m_origin formal_0_86) 19)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:10]:sift-compare
(define-fun formal_0_87 () FormalMachine (FormalCallback formal_0_86 boundary_0 (select (m_origin formal_0_86) 23) (select (m_origin formal_0_86) 19)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:11]:initial-compare
(assert (not (m_panicked formal_0_87)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_87) (select (m_origin formal_0_87) 24) (select (m_origin formal_0_87) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_87) (select (m_origin formal_0_87) 24) (select (m_origin formal_0_87) 15)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:11]:initial-compare
(define-fun formal_0_88 () FormalMachine (FormalCallback formal_0_87 boundary_0 (select (m_origin formal_0_87) 24) (select (m_origin formal_0_87) 15)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:11]:sift-compare
(assert (not (m_panicked formal_0_88)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_88) (select (m_origin formal_0_88) 24) (select (m_origin formal_0_88) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_88) (select (m_origin formal_0_88) 24) (select (m_origin formal_0_88) 23)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:11]:sift-compare
(define-fun formal_0_89 () FormalMachine (FormalCallback formal_0_88 boundary_0 (select (m_origin formal_0_88) 24) (select (m_origin formal_0_88) 23)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:11]:sift-compare
(assert (not (m_panicked formal_0_89)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_89) (select (m_origin formal_0_89) 24) (select (m_origin formal_0_89) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_89) (select (m_origin formal_0_89) 24) (select (m_origin formal_0_89) 19)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:11]:sift-compare
(define-fun formal_0_90 () FormalMachine (FormalCallback formal_0_89 boundary_0 (select (m_origin formal_0_89) 24) (select (m_origin formal_0_89) 19)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:11]:sift-compare
(assert (not (m_panicked formal_0_90)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_90) (select (m_origin formal_0_90) 24) (select (m_origin formal_0_90) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_90) (select (m_origin formal_0_90) 24) (select (m_origin formal_0_90) 16)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:11]:sift-compare
(define-fun formal_0_91 () FormalMachine (FormalCallback formal_0_90 boundary_0 (select (m_origin formal_0_90) 24) (select (m_origin formal_0_90) 16)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:initial-compare
(assert (not (m_panicked formal_0_91)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_91) (select (m_origin formal_0_91) 25) (select (m_origin formal_0_91) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_91) (select (m_origin formal_0_91) 25) (select (m_origin formal_0_91) 15)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:initial-compare
(define-fun formal_0_92 () FormalMachine (FormalCallback formal_0_91 boundary_0 (select (m_origin formal_0_91) 25) (select (m_origin formal_0_91) 15)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(assert (not (m_panicked formal_0_92)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_92) (select (m_origin formal_0_92) 25) (select (m_origin formal_0_92) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_92) (select (m_origin formal_0_92) 25) (select (m_origin formal_0_92) 23)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(define-fun formal_0_93 () FormalMachine (FormalCallback formal_0_92 boundary_0 (select (m_origin formal_0_92) 25) (select (m_origin formal_0_92) 23)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(assert (not (m_panicked formal_0_93)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_93) (select (m_origin formal_0_93) 25) (select (m_origin formal_0_93) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_93) (select (m_origin formal_0_93) 25) (select (m_origin formal_0_93) 19)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(define-fun formal_0_94 () FormalMachine (FormalCallback formal_0_93 boundary_0 (select (m_origin formal_0_93) 25) (select (m_origin formal_0_93) 19)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(assert (not (m_panicked formal_0_94)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_94) (select (m_origin formal_0_94) 25) (select (m_origin formal_0_94) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_94) (select (m_origin formal_0_94) 25) (select (m_origin formal_0_94) 24)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(define-fun formal_0_95 () FormalMachine (FormalCallback formal_0_94 boundary_0 (select (m_origin formal_0_94) 25) (select (m_origin formal_0_94) 24)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(assert (not (m_panicked formal_0_95)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_95) (select (m_origin formal_0_95) 25) (select (m_origin formal_0_95) 16)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_95) (select (m_origin formal_0_95) 25) (select (m_origin formal_0_95) 16)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(define-fun formal_0_96 () FormalMachine (FormalCallback formal_0_95 boundary_0 (select (m_origin formal_0_95) 25) (select (m_origin formal_0_95) 16)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(assert (not (m_panicked formal_0_96)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_96) (select (m_origin formal_0_96) 25) (select (m_origin formal_0_96) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_96) (select (m_origin formal_0_96) 25) (select (m_origin formal_0_96) 18)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(define-fun formal_0_97 () FormalMachine (FormalCallback formal_0_96 boundary_0 (select (m_origin formal_0_96) 25) (select (m_origin formal_0_96) 18)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(assert (not (m_panicked formal_0_97)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_97) (select (m_origin formal_0_97) 25) (select (m_origin formal_0_97) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_97) (select (m_origin formal_0_97) 25) (select (m_origin formal_0_97) 21)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(define-fun formal_0_98 () FormalMachine (FormalCallback formal_0_97 boundary_0 (select (m_origin formal_0_97) 25) (select (m_origin formal_0_97) 21)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(assert (not (m_panicked formal_0_98)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_98) (select (m_origin formal_0_98) 25) (select (m_origin formal_0_98) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_98) (select (m_origin formal_0_98) 25) (select (m_origin formal_0_98) 22)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(define-fun formal_0_99 () FormalMachine (FormalCallback formal_0_98 boundary_0 (select (m_origin formal_0_98) 25) (select (m_origin formal_0_98) 22)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(assert (not (m_panicked formal_0_99)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 25) (select (m_origin formal_0_99) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 25) (select (m_origin formal_0_99) 13)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(define-fun formal_0_100 () FormalMachine (FormalCallback formal_0_99 boundary_0 (select (m_origin formal_0_99) 25) (select (m_origin formal_0_99) 13)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(assert (not (m_panicked formal_0_100)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_100) (select (m_origin formal_0_100) 25) (select (m_origin formal_0_100) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_100) (select (m_origin formal_0_100) 25) (select (m_origin formal_0_100) 20)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(define-fun formal_0_101 () FormalMachine (FormalCallback formal_0_100 boundary_0 (select (m_origin formal_0_100) 25) (select (m_origin formal_0_100) 20)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(assert (not (m_panicked formal_0_101)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_101) (select (m_origin formal_0_101) 25) (select (m_origin formal_0_101) 17)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_101) (select (m_origin formal_0_101) 25) (select (m_origin formal_0_101) 17)) false))
; source callback transition phase=small-sort-general:insert-tail[13:26:12]:sift-compare
(define-fun formal_0_102 () FormalMachine (FormalCallback formal_0_101 boundary_0 (select (m_origin formal_0_101) 25) (select (m_origin formal_0_101) 17)))
; source callback case=general-small-sort-merge-restoration phase=small-sort-general:final-merge:merge-up[0]
(assert (not (m_panicked formal_0_102)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_102) (select (m_origin formal_0_102) 14) (select (m_origin formal_0_102) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_102) (select (m_origin formal_0_102) 14) (select (m_origin formal_0_102) 6)) true))
; source callback transition phase=small-sort-general:final-merge:merge-up[0]
(define-fun formal_0_103 () FormalMachine (FormalCallback formal_0_102 boundary_0 (select (m_origin formal_0_102) 14) (select (m_origin formal_0_102) 6)))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_104 () FormalMachine (FormalWriteFromOrigin formal_0_103 0 6))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_105 () FormalMachine (FormalWriteFromOrigin formal_0_104 1 12))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_106 () FormalMachine (FormalWriteFromOrigin formal_0_105 2 8))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_107 () FormalMachine (FormalWriteFromOrigin formal_0_106 3 10))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_108 () FormalMachine (FormalWriteFromOrigin formal_0_107 4 2))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_109 () FormalMachine (FormalWriteFromOrigin formal_0_108 5 1))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_110 () FormalMachine (FormalWriteFromOrigin formal_0_109 6 5))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_111 () FormalMachine (FormalWriteFromOrigin formal_0_110 7 0))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_112 () FormalMachine (FormalWriteFromOrigin formal_0_111 8 3))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_113 () FormalMachine (FormalWriteFromOrigin formal_0_112 9 7))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_114 () FormalMachine (FormalWriteFromOrigin formal_0_113 10 11))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_115 () FormalMachine (FormalWriteFromOrigin formal_0_114 11 4))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_116 () FormalMachine (FormalWriteFromOrigin formal_0_115 12 9))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_117 () FormalMachine (FormalWriteFromOrigin formal_0_116 13 14))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_118 () FormalMachine (FormalWriteFromOrigin formal_0_117 14 17))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_119 () FormalMachine (FormalWriteFromOrigin formal_0_118 15 25))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_120 () FormalMachine (FormalWriteFromOrigin formal_0_119 16 20))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_121 () FormalMachine (FormalWriteFromOrigin formal_0_120 17 13))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_122 () FormalMachine (FormalWriteFromOrigin formal_0_121 18 22))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_123 () FormalMachine (FormalWriteFromOrigin formal_0_122 19 21))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_124 () FormalMachine (FormalWriteFromOrigin formal_0_123 20 18))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_125 () FormalMachine (FormalWriteFromOrigin formal_0_124 21 16))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_126 () FormalMachine (FormalWriteFromOrigin formal_0_125 22 24))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_127 () FormalMachine (FormalWriteFromOrigin formal_0_126 23 19))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_128 () FormalMachine (FormalWriteFromOrigin formal_0_127 24 23))
; source write kind=copy-on-drop-restore phase=small-sort-general
(define-fun formal_0_129 () FormalMachine (FormalWriteFromOrigin formal_0_128 25 15))
(define-fun formal_result_0 () Result
  (mkResult
    (m_sequence formal_0_129)
    (m_callback formal_0_129)
    (m_panicked formal_0_129)
    false
    true
    (ite (m_panicked formal_0_129) 1 0)
    (not (m_panicked formal_0_129))
    -1))
(define-fun reference_result_0 () Result (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 2) 1 3) 2 7) 3 8) 4 9) 5 10) 6 13) 7 14) 8 18) 9 19) 10 20) 11 22) 12 24) 13 0) 14 1) 15 4) 16 5) 17 6) 18 11) 19 12) 20 15) 21 16) 22 17) 23 21) 24 23) 25 25) 103 true false true 1 false -1))
; retained source-forcing witness: panic-unwind
(assert (= formal_result_0 (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 2) 1 3) 2 7) 3 8) 4 9) 5 10) 6 13) 7 14) 8 18) 9 19) 10 20) 11 22) 12 24) 13 0) 14 1) 15 4) 16 5) 17 6) 18 11) 19 12) 20 15) 21 16) 22 17) 23 21) 24 23) 25 25) 103 true false true 1 false -1)))
(check-sat-using (then ctx-solver-simplify smt))
