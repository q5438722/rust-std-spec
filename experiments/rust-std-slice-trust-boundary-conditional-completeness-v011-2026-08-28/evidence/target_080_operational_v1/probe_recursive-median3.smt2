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

; formal source input case=recursive-pivot
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
  (mkFormalMachine (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 74) 1 30) 2 59) 3 32) 4 15) 5 70) 6 78) 7 76) 8 20) 9 28) 10 37) 11 72) 12 41) 13 67) 14 13) 15 31) 16 0) 17 16) 18 54) 19 63) 20 19) 21 17) 22 10) 23 21) 24 49) 25 39) 26 4) 27 2) 28 79) 29 29) 30 57) 31 25) 32 47) 33 3) 34 36) 35 77) 36 34) 37 55) 38 23) 39 5) 40 40) 41 35) 42 66) 43 71) 44 43) 45 68) 46 46) 47 27) 48 52) 49 69) 50 7) 51 8) 52 22) 53 48) 54 51) 55 14) 56 11) 57 12) 58 9) 59 62) 60 45) 61 56) 62 42) 63 18) 64 1) 65 64) 66 24) 67 73) 68 65) 69 38) 70 26) 71 58) 72 75) 73 33) 74 44) 75 50) 76 60) 77 53) 78 61) 79 6) (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 74) 1 30) 2 59) 3 32) 4 15) 5 70) 6 78) 7 76) 8 20) 9 28) 10 37) 11 72) 12 41) 13 67) 14 13) 15 31) 16 0) 17 16) 18 54) 19 63) 20 19) 21 17) 22 10) 23 21) 24 49) 25 39) 26 4) 27 2) 28 79) 29 29) 30 57) 31 25) 32 47) 33 3) 34 36) 35 77) 36 34) 37 55) 38 23) 39 5) 40 40) 41 35) 42 66) 43 71) 44 43) 45 68) 46 46) 47 27) 48 52) 49 69) 50 7) 51 8) 52 22) 53 48) 54 51) 55 14) 56 11) 57 12) 58 9) 59 62) 60 45) 61 56) 62 42) 63 18) 64 1) 65 64) 66 24) 67 73) 68 65) 69 38) 70 26) 71 58) 72 75) 73 33) 74 44) 75 50) 76 60) 77 53) 78 61) 79 6) (b_initial_state boundary_0) false))
(assert (BoundaryWellFormed boundary_0))
; source callback case=recursive-pivot phase=find-existing-run:direction
(assert (not (m_panicked source_initial_0)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) false))
; source callback transition phase=find-existing-run:direction
(define-fun formal_0_1 () FormalMachine (FormalCallback source_initial_0 boundary_0 (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)))
; source callback case=recursive-pivot phase=find-existing-run:descending
(assert (not (m_panicked formal_0_1)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) false))
; source callback transition phase=find-existing-run:descending
(define-fun formal_0_2 () FormalMachine (FormalCallback formal_0_1 boundary_0 (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)))
; source callback case=recursive-pivot phase=choose-pivot:median3-rec:a:median3:a-b
(assert (not (m_panicked formal_0_2)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 0) (select (m_origin formal_0_2) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 0) (select (m_origin formal_0_2) 4)) false))
; source callback transition phase=choose-pivot:median3-rec:a:median3:a-b
(define-fun formal_0_3 () FormalMachine (FormalCallback formal_0_2 boundary_0 (select (m_origin formal_0_2) 0) (select (m_origin formal_0_2) 4)))
; source callback case=recursive-pivot phase=choose-pivot:median3-rec:a:median3:a-c
(assert (not (m_panicked formal_0_3)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 0) (select (m_origin formal_0_3) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 0) (select (m_origin formal_0_3) 7)) false))
; source callback transition phase=choose-pivot:median3-rec:a:median3:a-c
(define-fun formal_0_4 () FormalMachine (FormalCallback formal_0_3 boundary_0 (select (m_origin formal_0_3) 0) (select (m_origin formal_0_3) 7)))
; source callback case=recursive-pivot phase=choose-pivot:median3-rec:b:median3:a-b
(assert (not (m_panicked formal_0_4)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 40) (select (m_origin formal_0_4) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 40) (select (m_origin formal_0_4) 44)) false))
; source callback transition phase=choose-pivot:median3-rec:b:median3:a-b
(define-fun formal_0_5 () FormalMachine (FormalCallback formal_0_4 boundary_0 (select (m_origin formal_0_4) 40) (select (m_origin formal_0_4) 44)))
; source callback case=recursive-pivot phase=choose-pivot:median3-rec:b:median3:a-c
(assert (not (m_panicked formal_0_5)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_5) (select (m_origin formal_0_5) 40) (select (m_origin formal_0_5) 47)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_5) (select (m_origin formal_0_5) 40) (select (m_origin formal_0_5) 47)) false))
; source callback transition phase=choose-pivot:median3-rec:b:median3:a-c
(define-fun formal_0_6 () FormalMachine (FormalCallback formal_0_5 boundary_0 (select (m_origin formal_0_5) 40) (select (m_origin formal_0_5) 47)))
; source callback case=recursive-pivot phase=choose-pivot:median3-rec:c:median3:a-b
(assert (not (m_panicked formal_0_6)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 70) (select (m_origin formal_0_6) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 70) (select (m_origin formal_0_6) 74)) false))
; source callback transition phase=choose-pivot:median3-rec:c:median3:a-b
(define-fun formal_0_7 () FormalMachine (FormalCallback formal_0_6 boundary_0 (select (m_origin formal_0_6) 70) (select (m_origin formal_0_6) 74)))
; source callback case=recursive-pivot phase=choose-pivot:median3-rec:c:median3:a-c
(assert (not (m_panicked formal_0_7)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_7) (select (m_origin formal_0_7) 70) (select (m_origin formal_0_7) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_7) (select (m_origin formal_0_7) 70) (select (m_origin formal_0_7) 77)) false))
; source callback transition phase=choose-pivot:median3-rec:c:median3:a-c
(define-fun formal_0_8 () FormalMachine (FormalCallback formal_0_7 boundary_0 (select (m_origin formal_0_7) 70) (select (m_origin formal_0_7) 77)))
; source callback case=recursive-pivot phase=choose-pivot:median3-rec:c:median3:b-c
(assert (not (m_panicked formal_0_8)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 74) (select (m_origin formal_0_8) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 74) (select (m_origin formal_0_8) 77)) false))
; source callback transition phase=choose-pivot:median3-rec:c:median3:b-c
(define-fun formal_0_9 () FormalMachine (FormalCallback formal_0_8 boundary_0 (select (m_origin formal_0_8) 74) (select (m_origin formal_0_8) 77)))
; source callback case=recursive-pivot phase=choose-pivot:median3-rec:median3:a-b
(assert (not (m_panicked formal_0_9)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_9) (select (m_origin formal_0_9) 0) (select (m_origin formal_0_9) 40)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_9) (select (m_origin formal_0_9) 0) (select (m_origin formal_0_9) 40)) false))
; source callback transition phase=choose-pivot:median3-rec:median3:a-b
(define-fun formal_0_10 () FormalMachine (FormalCallback formal_0_9 boundary_0 (select (m_origin formal_0_9) 0) (select (m_origin formal_0_9) 40)))
; source callback case=recursive-pivot phase=choose-pivot:median3-rec:median3:a-c
(assert (not (m_panicked formal_0_10)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_10) (select (m_origin formal_0_10) 0) (select (m_origin formal_0_10) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_10) (select (m_origin formal_0_10) 0) (select (m_origin formal_0_10) 74)) false))
; source callback transition phase=choose-pivot:median3-rec:median3:a-c
(define-fun formal_0_11 () FormalMachine (FormalCallback formal_0_10 boundary_0 (select (m_origin formal_0_10) 0) (select (m_origin formal_0_10) 74)))
; source callback case=recursive-pivot phase=choose-pivot:median3-rec:median3:b-c
(assert (not (m_panicked formal_0_11)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_11) (select (m_origin formal_0_11) 40) (select (m_origin formal_0_11) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_11) (select (m_origin formal_0_11) 40) (select (m_origin formal_0_11) 74)) false))
; source callback transition phase=choose-pivot:median3-rec:median3:b-c
(define-fun formal_0_12 () FormalMachine (FormalCallback formal_0_11 boundary_0 (select (m_origin formal_0_11) 40) (select (m_origin formal_0_11) 74)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_13 () FormalMachine (FormalSwap formal_0_12 0 74))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_13)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_13) (select (m_origin formal_0_13) 2) (select (m_origin formal_0_13) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_13) (select (m_origin formal_0_13) 2) (select (m_origin formal_0_13) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_14 () FormalMachine (FormalCallback formal_0_13 boundary_0 (select (m_origin formal_0_13) 2) (select (m_origin formal_0_13) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_15 () FormalMachine (FormalWriteFromOrigin formal_0_14 1 2))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_15)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_15) (select (m_origin formal_0_15) 3) (select (m_origin formal_0_15) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_15) (select (m_origin formal_0_15) 3) (select (m_origin formal_0_15) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_16 () FormalMachine (FormalCallback formal_0_15 boundary_0 (select (m_origin formal_0_15) 3) (select (m_origin formal_0_15) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_17 () FormalMachine (FormalWriteFromOrigin formal_0_16 1 3))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_17)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_17) (select (m_origin formal_0_17) 4) (select (m_origin formal_0_17) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_17) (select (m_origin formal_0_17) 4) (select (m_origin formal_0_17) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_18 () FormalMachine (FormalCallback formal_0_17 boundary_0 (select (m_origin formal_0_17) 4) (select (m_origin formal_0_17) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_19 () FormalMachine (FormalWriteFromOrigin formal_0_18 2 4))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_20 () FormalMachine (FormalWriteFromOrigin formal_0_19 3 2))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_20)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 5) (select (m_origin formal_0_20) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 5) (select (m_origin formal_0_20) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_21 () FormalMachine (FormalCallback formal_0_20 boundary_0 (select (m_origin formal_0_20) 5) (select (m_origin formal_0_20) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_22 () FormalMachine (FormalWriteFromOrigin formal_0_21 3 5))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_23 () FormalMachine (FormalWriteFromOrigin formal_0_22 4 2))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_23)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_23) (select (m_origin formal_0_23) 6) (select (m_origin formal_0_23) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_23) (select (m_origin formal_0_23) 6) (select (m_origin formal_0_23) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_24 () FormalMachine (FormalCallback formal_0_23 boundary_0 (select (m_origin formal_0_23) 6) (select (m_origin formal_0_23) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_25 () FormalMachine (FormalWriteFromOrigin formal_0_24 3 6))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_25)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 7) (select (m_origin formal_0_25) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_25) (select (m_origin formal_0_25) 7) (select (m_origin formal_0_25) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_26 () FormalMachine (FormalCallback formal_0_25 boundary_0 (select (m_origin formal_0_25) 7) (select (m_origin formal_0_25) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_27 () FormalMachine (FormalWriteFromOrigin formal_0_26 3 7))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_27)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_27) (select (m_origin formal_0_27) 8) (select (m_origin formal_0_27) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_27) (select (m_origin formal_0_27) 8) (select (m_origin formal_0_27) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_28 () FormalMachine (FormalCallback formal_0_27 boundary_0 (select (m_origin formal_0_27) 8) (select (m_origin formal_0_27) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_29 () FormalMachine (FormalWriteFromOrigin formal_0_28 3 8))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_29)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_29) (select (m_origin formal_0_29) 9) (select (m_origin formal_0_29) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_29) (select (m_origin formal_0_29) 9) (select (m_origin formal_0_29) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_30 () FormalMachine (FormalCallback formal_0_29 boundary_0 (select (m_origin formal_0_29) 9) (select (m_origin formal_0_29) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_31 () FormalMachine (FormalWriteFromOrigin formal_0_30 4 9))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_32 () FormalMachine (FormalWriteFromOrigin formal_0_31 8 2))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_32)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_32) (select (m_origin formal_0_32) 10) (select (m_origin formal_0_32) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_32) (select (m_origin formal_0_32) 10) (select (m_origin formal_0_32) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_33 () FormalMachine (FormalCallback formal_0_32 boundary_0 (select (m_origin formal_0_32) 10) (select (m_origin formal_0_32) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_34 () FormalMachine (FormalWriteFromOrigin formal_0_33 5 10))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_35 () FormalMachine (FormalWriteFromOrigin formal_0_34 9 5))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_35)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_35) (select (m_origin formal_0_35) 11) (select (m_origin formal_0_35) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_35) (select (m_origin formal_0_35) 11) (select (m_origin formal_0_35) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_36 () FormalMachine (FormalCallback formal_0_35 boundary_0 (select (m_origin formal_0_35) 11) (select (m_origin formal_0_35) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_37 () FormalMachine (FormalWriteFromOrigin formal_0_36 6 11))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_38 () FormalMachine (FormalWriteFromOrigin formal_0_37 10 6))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_38)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 12) (select (m_origin formal_0_38) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 12) (select (m_origin formal_0_38) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_39 () FormalMachine (FormalCallback formal_0_38 boundary_0 (select (m_origin formal_0_38) 12) (select (m_origin formal_0_38) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_40 () FormalMachine (FormalWriteFromOrigin formal_0_39 6 12))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_40)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_40) (select (m_origin formal_0_40) 13) (select (m_origin formal_0_40) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_40) (select (m_origin formal_0_40) 13) (select (m_origin formal_0_40) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_41 () FormalMachine (FormalCallback formal_0_40 boundary_0 (select (m_origin formal_0_40) 13) (select (m_origin formal_0_40) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_42 () FormalMachine (FormalWriteFromOrigin formal_0_41 7 13))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_43 () FormalMachine (FormalWriteFromOrigin formal_0_42 12 7))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_43)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_43) (select (m_origin formal_0_43) 14) (select (m_origin formal_0_43) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_43) (select (m_origin formal_0_43) 14) (select (m_origin formal_0_43) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_44 () FormalMachine (FormalCallback formal_0_43 boundary_0 (select (m_origin formal_0_43) 14) (select (m_origin formal_0_43) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_45 () FormalMachine (FormalWriteFromOrigin formal_0_44 7 14))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_45)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_45) (select (m_origin formal_0_45) 15) (select (m_origin formal_0_45) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_45) (select (m_origin formal_0_45) 15) (select (m_origin formal_0_45) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_46 () FormalMachine (FormalCallback formal_0_45 boundary_0 (select (m_origin formal_0_45) 15) (select (m_origin formal_0_45) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_47 () FormalMachine (FormalWriteFromOrigin formal_0_46 8 15))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_48 () FormalMachine (FormalWriteFromOrigin formal_0_47 14 2))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_48)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 16) (select (m_origin formal_0_48) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 16) (select (m_origin formal_0_48) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_49 () FormalMachine (FormalCallback formal_0_48 boundary_0 (select (m_origin formal_0_48) 16) (select (m_origin formal_0_48) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_50 () FormalMachine (FormalWriteFromOrigin formal_0_49 9 16))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_51 () FormalMachine (FormalWriteFromOrigin formal_0_50 15 5))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_51)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_51) (select (m_origin formal_0_51) 17) (select (m_origin formal_0_51) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_51) (select (m_origin formal_0_51) 17) (select (m_origin formal_0_51) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_52 () FormalMachine (FormalCallback formal_0_51 boundary_0 (select (m_origin formal_0_51) 17) (select (m_origin formal_0_51) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_53 () FormalMachine (FormalWriteFromOrigin formal_0_52 10 17))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_54 () FormalMachine (FormalWriteFromOrigin formal_0_53 16 6))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_54)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_54) (select (m_origin formal_0_54) 18) (select (m_origin formal_0_54) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_54) (select (m_origin formal_0_54) 18) (select (m_origin formal_0_54) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_55 () FormalMachine (FormalCallback formal_0_54 boundary_0 (select (m_origin formal_0_54) 18) (select (m_origin formal_0_54) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_56 () FormalMachine (FormalWriteFromOrigin formal_0_55 11 18))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_57 () FormalMachine (FormalWriteFromOrigin formal_0_56 17 11))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_57)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_57) (select (m_origin formal_0_57) 19) (select (m_origin formal_0_57) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_57) (select (m_origin formal_0_57) 19) (select (m_origin formal_0_57) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_58 () FormalMachine (FormalCallback formal_0_57 boundary_0 (select (m_origin formal_0_57) 19) (select (m_origin formal_0_57) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_59 () FormalMachine (FormalWriteFromOrigin formal_0_58 11 19))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_59)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_59) (select (m_origin formal_0_59) 20) (select (m_origin formal_0_59) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_59) (select (m_origin formal_0_59) 20) (select (m_origin formal_0_59) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_60 () FormalMachine (FormalCallback formal_0_59 boundary_0 (select (m_origin formal_0_59) 20) (select (m_origin formal_0_59) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_61 () FormalMachine (FormalWriteFromOrigin formal_0_60 11 20))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_61)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_61) (select (m_origin formal_0_61) 21) (select (m_origin formal_0_61) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_61) (select (m_origin formal_0_61) 21) (select (m_origin formal_0_61) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_62 () FormalMachine (FormalCallback formal_0_61 boundary_0 (select (m_origin formal_0_61) 21) (select (m_origin formal_0_61) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_63 () FormalMachine (FormalWriteFromOrigin formal_0_62 12 21))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_64 () FormalMachine (FormalWriteFromOrigin formal_0_63 20 7))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_64)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_64) (select (m_origin formal_0_64) 22) (select (m_origin formal_0_64) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_64) (select (m_origin formal_0_64) 22) (select (m_origin formal_0_64) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_65 () FormalMachine (FormalCallback formal_0_64 boundary_0 (select (m_origin formal_0_64) 22) (select (m_origin formal_0_64) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_66 () FormalMachine (FormalWriteFromOrigin formal_0_65 13 22))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_67 () FormalMachine (FormalWriteFromOrigin formal_0_66 21 13))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_67)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_67) (select (m_origin formal_0_67) 23) (select (m_origin formal_0_67) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_67) (select (m_origin formal_0_67) 23) (select (m_origin formal_0_67) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_68 () FormalMachine (FormalCallback formal_0_67 boundary_0 (select (m_origin formal_0_67) 23) (select (m_origin formal_0_67) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_69 () FormalMachine (FormalWriteFromOrigin formal_0_68 14 23))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_70 () FormalMachine (FormalWriteFromOrigin formal_0_69 22 2))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_70)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_70) (select (m_origin formal_0_70) 24) (select (m_origin formal_0_70) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_70) (select (m_origin formal_0_70) 24) (select (m_origin formal_0_70) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_71 () FormalMachine (FormalCallback formal_0_70 boundary_0 (select (m_origin formal_0_70) 24) (select (m_origin formal_0_70) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_72 () FormalMachine (FormalWriteFromOrigin formal_0_71 15 24))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_73 () FormalMachine (FormalWriteFromOrigin formal_0_72 23 5))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_73)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 25) (select (m_origin formal_0_73) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 25) (select (m_origin formal_0_73) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_74 () FormalMachine (FormalCallback formal_0_73 boundary_0 (select (m_origin formal_0_73) 25) (select (m_origin formal_0_73) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_75 () FormalMachine (FormalWriteFromOrigin formal_0_74 15 25))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_75)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 26) (select (m_origin formal_0_75) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 26) (select (m_origin formal_0_75) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_76 () FormalMachine (FormalCallback formal_0_75 boundary_0 (select (m_origin formal_0_75) 26) (select (m_origin formal_0_75) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_77 () FormalMachine (FormalWriteFromOrigin formal_0_76 16 26))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_78 () FormalMachine (FormalWriteFromOrigin formal_0_77 25 6))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_78)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 27) (select (m_origin formal_0_78) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 27) (select (m_origin formal_0_78) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_79 () FormalMachine (FormalCallback formal_0_78 boundary_0 (select (m_origin formal_0_78) 27) (select (m_origin formal_0_78) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_80 () FormalMachine (FormalWriteFromOrigin formal_0_79 17 27))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_81 () FormalMachine (FormalWriteFromOrigin formal_0_80 26 11))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_81)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 28) (select (m_origin formal_0_81) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_81) (select (m_origin formal_0_81) 28) (select (m_origin formal_0_81) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_82 () FormalMachine (FormalCallback formal_0_81 boundary_0 (select (m_origin formal_0_81) 28) (select (m_origin formal_0_81) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_83 () FormalMachine (FormalWriteFromOrigin formal_0_82 18 28))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_84 () FormalMachine (FormalWriteFromOrigin formal_0_83 27 18))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_84)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_84) (select (m_origin formal_0_84) 29) (select (m_origin formal_0_84) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_84) (select (m_origin formal_0_84) 29) (select (m_origin formal_0_84) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_85 () FormalMachine (FormalCallback formal_0_84 boundary_0 (select (m_origin formal_0_84) 29) (select (m_origin formal_0_84) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_86 () FormalMachine (FormalWriteFromOrigin formal_0_85 18 29))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_86)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 30) (select (m_origin formal_0_86) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 30) (select (m_origin formal_0_86) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_87 () FormalMachine (FormalCallback formal_0_86 boundary_0 (select (m_origin formal_0_86) 30) (select (m_origin formal_0_86) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_88 () FormalMachine (FormalWriteFromOrigin formal_0_87 19 30))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_89 () FormalMachine (FormalWriteFromOrigin formal_0_88 29 19))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_89)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_89) (select (m_origin formal_0_89) 31) (select (m_origin formal_0_89) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_89) (select (m_origin formal_0_89) 31) (select (m_origin formal_0_89) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_90 () FormalMachine (FormalCallback formal_0_89 boundary_0 (select (m_origin formal_0_89) 31) (select (m_origin formal_0_89) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_91 () FormalMachine (FormalWriteFromOrigin formal_0_90 19 31))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_91)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_91) (select (m_origin formal_0_91) 32) (select (m_origin formal_0_91) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_91) (select (m_origin formal_0_91) 32) (select (m_origin formal_0_91) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_92 () FormalMachine (FormalCallback formal_0_91 boundary_0 (select (m_origin formal_0_91) 32) (select (m_origin formal_0_91) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_93 () FormalMachine (FormalWriteFromOrigin formal_0_92 20 32))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_94 () FormalMachine (FormalWriteFromOrigin formal_0_93 31 7))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_94)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_94) (select (m_origin formal_0_94) 33) (select (m_origin formal_0_94) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_94) (select (m_origin formal_0_94) 33) (select (m_origin formal_0_94) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_95 () FormalMachine (FormalCallback formal_0_94 boundary_0 (select (m_origin formal_0_94) 33) (select (m_origin formal_0_94) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_96 () FormalMachine (FormalWriteFromOrigin formal_0_95 20 33))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_96)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_96) (select (m_origin formal_0_96) 34) (select (m_origin formal_0_96) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_96) (select (m_origin formal_0_96) 34) (select (m_origin formal_0_96) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_97 () FormalMachine (FormalCallback formal_0_96 boundary_0 (select (m_origin formal_0_96) 34) (select (m_origin formal_0_96) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_98 () FormalMachine (FormalWriteFromOrigin formal_0_97 21 34))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_99 () FormalMachine (FormalWriteFromOrigin formal_0_98 33 13))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_99)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 35) (select (m_origin formal_0_99) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 35) (select (m_origin formal_0_99) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_100 () FormalMachine (FormalCallback formal_0_99 boundary_0 (select (m_origin formal_0_99) 35) (select (m_origin formal_0_99) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_101 () FormalMachine (FormalWriteFromOrigin formal_0_100 22 35))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_102 () FormalMachine (FormalWriteFromOrigin formal_0_101 34 2))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_102)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_102) (select (m_origin formal_0_102) 36) (select (m_origin formal_0_102) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_102) (select (m_origin formal_0_102) 36) (select (m_origin formal_0_102) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_103 () FormalMachine (FormalCallback formal_0_102 boundary_0 (select (m_origin formal_0_102) 36) (select (m_origin formal_0_102) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_104 () FormalMachine (FormalWriteFromOrigin formal_0_103 22 36))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_104)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_104) (select (m_origin formal_0_104) 37) (select (m_origin formal_0_104) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_104) (select (m_origin formal_0_104) 37) (select (m_origin formal_0_104) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_105 () FormalMachine (FormalCallback formal_0_104 boundary_0 (select (m_origin formal_0_104) 37) (select (m_origin formal_0_104) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_106 () FormalMachine (FormalWriteFromOrigin formal_0_105 23 37))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_107 () FormalMachine (FormalWriteFromOrigin formal_0_106 36 5))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_107)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_107) (select (m_origin formal_0_107) 38) (select (m_origin formal_0_107) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_107) (select (m_origin formal_0_107) 38) (select (m_origin formal_0_107) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_108 () FormalMachine (FormalCallback formal_0_107 boundary_0 (select (m_origin formal_0_107) 38) (select (m_origin formal_0_107) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_109 () FormalMachine (FormalWriteFromOrigin formal_0_108 23 38))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_109)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_109) (select (m_origin formal_0_109) 39) (select (m_origin formal_0_109) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_109) (select (m_origin formal_0_109) 39) (select (m_origin formal_0_109) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_110 () FormalMachine (FormalCallback formal_0_109 boundary_0 (select (m_origin formal_0_109) 39) (select (m_origin formal_0_109) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_111 () FormalMachine (FormalWriteFromOrigin formal_0_110 24 39))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_112 () FormalMachine (FormalWriteFromOrigin formal_0_111 38 24))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_112)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_112) (select (m_origin formal_0_112) 40) (select (m_origin formal_0_112) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_112) (select (m_origin formal_0_112) 40) (select (m_origin formal_0_112) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_113 () FormalMachine (FormalCallback formal_0_112 boundary_0 (select (m_origin formal_0_112) 40) (select (m_origin formal_0_112) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_114 () FormalMachine (FormalWriteFromOrigin formal_0_113 25 40))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_115 () FormalMachine (FormalWriteFromOrigin formal_0_114 39 6))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_115)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_115) (select (m_origin formal_0_115) 41) (select (m_origin formal_0_115) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_115) (select (m_origin formal_0_115) 41) (select (m_origin formal_0_115) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_116 () FormalMachine (FormalCallback formal_0_115 boundary_0 (select (m_origin formal_0_115) 41) (select (m_origin formal_0_115) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_117 () FormalMachine (FormalWriteFromOrigin formal_0_116 26 41))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_118 () FormalMachine (FormalWriteFromOrigin formal_0_117 40 11))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_118)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_118) (select (m_origin formal_0_118) 42) (select (m_origin formal_0_118) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_118) (select (m_origin formal_0_118) 42) (select (m_origin formal_0_118) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_119 () FormalMachine (FormalCallback formal_0_118 boundary_0 (select (m_origin formal_0_118) 42) (select (m_origin formal_0_118) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_120 () FormalMachine (FormalWriteFromOrigin formal_0_119 27 42))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_121 () FormalMachine (FormalWriteFromOrigin formal_0_120 41 18))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_121)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_121) (select (m_origin formal_0_121) 43) (select (m_origin formal_0_121) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_121) (select (m_origin formal_0_121) 43) (select (m_origin formal_0_121) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_122 () FormalMachine (FormalCallback formal_0_121 boundary_0 (select (m_origin formal_0_121) 43) (select (m_origin formal_0_121) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_123 () FormalMachine (FormalWriteFromOrigin formal_0_122 27 43))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_123)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_123) (select (m_origin formal_0_123) 44) (select (m_origin formal_0_123) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_123) (select (m_origin formal_0_123) 44) (select (m_origin formal_0_123) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_124 () FormalMachine (FormalCallback formal_0_123 boundary_0 (select (m_origin formal_0_123) 44) (select (m_origin formal_0_123) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_125 () FormalMachine (FormalWriteFromOrigin formal_0_124 27 44))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_125)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_125) (select (m_origin formal_0_125) 45) (select (m_origin formal_0_125) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_125) (select (m_origin formal_0_125) 45) (select (m_origin formal_0_125) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_126 () FormalMachine (FormalCallback formal_0_125 boundary_0 (select (m_origin formal_0_125) 45) (select (m_origin formal_0_125) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_127 () FormalMachine (FormalWriteFromOrigin formal_0_126 28 45))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_128 () FormalMachine (FormalWriteFromOrigin formal_0_127 44 28))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_128)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 46) (select (m_origin formal_0_128) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 46) (select (m_origin formal_0_128) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_129 () FormalMachine (FormalCallback formal_0_128 boundary_0 (select (m_origin formal_0_128) 46) (select (m_origin formal_0_128) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_130 () FormalMachine (FormalWriteFromOrigin formal_0_129 28 46))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_130)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_130) (select (m_origin formal_0_130) 47) (select (m_origin formal_0_130) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_130) (select (m_origin formal_0_130) 47) (select (m_origin formal_0_130) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_131 () FormalMachine (FormalCallback formal_0_130 boundary_0 (select (m_origin formal_0_130) 47) (select (m_origin formal_0_130) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_132 () FormalMachine (FormalWriteFromOrigin formal_0_131 28 47))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_132)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_132) (select (m_origin formal_0_132) 48) (select (m_origin formal_0_132) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_132) (select (m_origin formal_0_132) 48) (select (m_origin formal_0_132) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_133 () FormalMachine (FormalCallback formal_0_132 boundary_0 (select (m_origin formal_0_132) 48) (select (m_origin formal_0_132) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_134 () FormalMachine (FormalWriteFromOrigin formal_0_133 29 48))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_135 () FormalMachine (FormalWriteFromOrigin formal_0_134 47 19))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_135)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_135) (select (m_origin formal_0_135) 49) (select (m_origin formal_0_135) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_135) (select (m_origin formal_0_135) 49) (select (m_origin formal_0_135) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_136 () FormalMachine (FormalCallback formal_0_135 boundary_0 (select (m_origin formal_0_135) 49) (select (m_origin formal_0_135) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_137 () FormalMachine (FormalWriteFromOrigin formal_0_136 29 49))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_137)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_137) (select (m_origin formal_0_137) 50) (select (m_origin formal_0_137) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_137) (select (m_origin formal_0_137) 50) (select (m_origin formal_0_137) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_138 () FormalMachine (FormalCallback formal_0_137 boundary_0 (select (m_origin formal_0_137) 50) (select (m_origin formal_0_137) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_139 () FormalMachine (FormalWriteFromOrigin formal_0_138 29 50))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_139)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_139) (select (m_origin formal_0_139) 51) (select (m_origin formal_0_139) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_139) (select (m_origin formal_0_139) 51) (select (m_origin formal_0_139) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_140 () FormalMachine (FormalCallback formal_0_139 boundary_0 (select (m_origin formal_0_139) 51) (select (m_origin formal_0_139) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_141 () FormalMachine (FormalWriteFromOrigin formal_0_140 30 51))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_142 () FormalMachine (FormalWriteFromOrigin formal_0_141 50 30))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_142)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_142) (select (m_origin formal_0_142) 52) (select (m_origin formal_0_142) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_142) (select (m_origin formal_0_142) 52) (select (m_origin formal_0_142) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_143 () FormalMachine (FormalCallback formal_0_142 boundary_0 (select (m_origin formal_0_142) 52) (select (m_origin formal_0_142) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_144 () FormalMachine (FormalWriteFromOrigin formal_0_143 31 52))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_145 () FormalMachine (FormalWriteFromOrigin formal_0_144 51 7))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_145)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_145) (select (m_origin formal_0_145) 53) (select (m_origin formal_0_145) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_145) (select (m_origin formal_0_145) 53) (select (m_origin formal_0_145) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_146 () FormalMachine (FormalCallback formal_0_145 boundary_0 (select (m_origin formal_0_145) 53) (select (m_origin formal_0_145) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_147 () FormalMachine (FormalWriteFromOrigin formal_0_146 32 53))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_148 () FormalMachine (FormalWriteFromOrigin formal_0_147 52 32))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_148)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_148) (select (m_origin formal_0_148) 54) (select (m_origin formal_0_148) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_148) (select (m_origin formal_0_148) 54) (select (m_origin formal_0_148) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_149 () FormalMachine (FormalCallback formal_0_148 boundary_0 (select (m_origin formal_0_148) 54) (select (m_origin formal_0_148) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_150 () FormalMachine (FormalWriteFromOrigin formal_0_149 32 54))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_150)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_150) (select (m_origin formal_0_150) 55) (select (m_origin formal_0_150) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_150) (select (m_origin formal_0_150) 55) (select (m_origin formal_0_150) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_151 () FormalMachine (FormalCallback formal_0_150 boundary_0 (select (m_origin formal_0_150) 55) (select (m_origin formal_0_150) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_152 () FormalMachine (FormalWriteFromOrigin formal_0_151 32 55))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_152)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_152) (select (m_origin formal_0_152) 56) (select (m_origin formal_0_152) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_152) (select (m_origin formal_0_152) 56) (select (m_origin formal_0_152) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_153 () FormalMachine (FormalCallback formal_0_152 boundary_0 (select (m_origin formal_0_152) 56) (select (m_origin formal_0_152) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_154 () FormalMachine (FormalWriteFromOrigin formal_0_153 33 56))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_155 () FormalMachine (FormalWriteFromOrigin formal_0_154 55 13))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_155)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 57) (select (m_origin formal_0_155) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 57) (select (m_origin formal_0_155) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_156 () FormalMachine (FormalCallback formal_0_155 boundary_0 (select (m_origin formal_0_155) 57) (select (m_origin formal_0_155) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_157 () FormalMachine (FormalWriteFromOrigin formal_0_156 34 57))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_158 () FormalMachine (FormalWriteFromOrigin formal_0_157 56 2))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_158)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_158) (select (m_origin formal_0_158) 58) (select (m_origin formal_0_158) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_158) (select (m_origin formal_0_158) 58) (select (m_origin formal_0_158) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_159 () FormalMachine (FormalCallback formal_0_158 boundary_0 (select (m_origin formal_0_158) 58) (select (m_origin formal_0_158) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_160 () FormalMachine (FormalWriteFromOrigin formal_0_159 35 58))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_161 () FormalMachine (FormalWriteFromOrigin formal_0_160 57 35))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_161)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_161) (select (m_origin formal_0_161) 59) (select (m_origin formal_0_161) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_161) (select (m_origin formal_0_161) 59) (select (m_origin formal_0_161) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_162 () FormalMachine (FormalCallback formal_0_161 boundary_0 (select (m_origin formal_0_161) 59) (select (m_origin formal_0_161) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_163 () FormalMachine (FormalWriteFromOrigin formal_0_162 36 59))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_164 () FormalMachine (FormalWriteFromOrigin formal_0_163 58 5))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_164)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_164) (select (m_origin formal_0_164) 60) (select (m_origin formal_0_164) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_164) (select (m_origin formal_0_164) 60) (select (m_origin formal_0_164) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_165 () FormalMachine (FormalCallback formal_0_164 boundary_0 (select (m_origin formal_0_164) 60) (select (m_origin formal_0_164) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_166 () FormalMachine (FormalWriteFromOrigin formal_0_165 36 60))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_166)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_166) (select (m_origin formal_0_166) 61) (select (m_origin formal_0_166) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_166) (select (m_origin formal_0_166) 61) (select (m_origin formal_0_166) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_167 () FormalMachine (FormalCallback formal_0_166 boundary_0 (select (m_origin formal_0_166) 61) (select (m_origin formal_0_166) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_168 () FormalMachine (FormalWriteFromOrigin formal_0_167 36 61))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_168)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_168) (select (m_origin formal_0_168) 62) (select (m_origin formal_0_168) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_168) (select (m_origin formal_0_168) 62) (select (m_origin formal_0_168) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_169 () FormalMachine (FormalCallback formal_0_168 boundary_0 (select (m_origin formal_0_168) 62) (select (m_origin formal_0_168) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_170 () FormalMachine (FormalWriteFromOrigin formal_0_169 36 62))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_170)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_170) (select (m_origin formal_0_170) 63) (select (m_origin formal_0_170) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_170) (select (m_origin formal_0_170) 63) (select (m_origin formal_0_170) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_171 () FormalMachine (FormalCallback formal_0_170 boundary_0 (select (m_origin formal_0_170) 63) (select (m_origin formal_0_170) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_172 () FormalMachine (FormalWriteFromOrigin formal_0_171 37 63))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_173 () FormalMachine (FormalWriteFromOrigin formal_0_172 62 37))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_173)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_173) (select (m_origin formal_0_173) 64) (select (m_origin formal_0_173) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_173) (select (m_origin formal_0_173) 64) (select (m_origin formal_0_173) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_174 () FormalMachine (FormalCallback formal_0_173 boundary_0 (select (m_origin formal_0_173) 64) (select (m_origin formal_0_173) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_175 () FormalMachine (FormalWriteFromOrigin formal_0_174 38 64))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_176 () FormalMachine (FormalWriteFromOrigin formal_0_175 63 24))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_176)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 65) (select (m_origin formal_0_176) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 65) (select (m_origin formal_0_176) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_177 () FormalMachine (FormalCallback formal_0_176 boundary_0 (select (m_origin formal_0_176) 65) (select (m_origin formal_0_176) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_178 () FormalMachine (FormalWriteFromOrigin formal_0_177 39 65))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_179 () FormalMachine (FormalWriteFromOrigin formal_0_178 64 6))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_179)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_179) (select (m_origin formal_0_179) 66) (select (m_origin formal_0_179) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_179) (select (m_origin formal_0_179) 66) (select (m_origin formal_0_179) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_180 () FormalMachine (FormalCallback formal_0_179 boundary_0 (select (m_origin formal_0_179) 66) (select (m_origin formal_0_179) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_181 () FormalMachine (FormalWriteFromOrigin formal_0_180 39 66))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_181)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_181) (select (m_origin formal_0_181) 67) (select (m_origin formal_0_181) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_181) (select (m_origin formal_0_181) 67) (select (m_origin formal_0_181) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_182 () FormalMachine (FormalCallback formal_0_181 boundary_0 (select (m_origin formal_0_181) 67) (select (m_origin formal_0_181) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_183 () FormalMachine (FormalWriteFromOrigin formal_0_182 40 67))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_184 () FormalMachine (FormalWriteFromOrigin formal_0_183 66 11))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_184)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_184) (select (m_origin formal_0_184) 68) (select (m_origin formal_0_184) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_184) (select (m_origin formal_0_184) 68) (select (m_origin formal_0_184) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_185 () FormalMachine (FormalCallback formal_0_184 boundary_0 (select (m_origin formal_0_184) 68) (select (m_origin formal_0_184) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_186 () FormalMachine (FormalWriteFromOrigin formal_0_185 40 68))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_186)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_186) (select (m_origin formal_0_186) 69) (select (m_origin formal_0_186) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_186) (select (m_origin formal_0_186) 69) (select (m_origin formal_0_186) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_187 () FormalMachine (FormalCallback formal_0_186 boundary_0 (select (m_origin formal_0_186) 69) (select (m_origin formal_0_186) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_188 () FormalMachine (FormalWriteFromOrigin formal_0_187 40 69))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_188)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_188) (select (m_origin formal_0_188) 70) (select (m_origin formal_0_188) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_188) (select (m_origin formal_0_188) 70) (select (m_origin formal_0_188) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_189 () FormalMachine (FormalCallback formal_0_188 boundary_0 (select (m_origin formal_0_188) 70) (select (m_origin formal_0_188) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_190 () FormalMachine (FormalWriteFromOrigin formal_0_189 41 70))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_191 () FormalMachine (FormalWriteFromOrigin formal_0_190 69 18))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_191)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_191) (select (m_origin formal_0_191) 71) (select (m_origin formal_0_191) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_191) (select (m_origin formal_0_191) 71) (select (m_origin formal_0_191) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_192 () FormalMachine (FormalCallback formal_0_191 boundary_0 (select (m_origin formal_0_191) 71) (select (m_origin formal_0_191) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_193 () FormalMachine (FormalWriteFromOrigin formal_0_192 42 71))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_194 () FormalMachine (FormalWriteFromOrigin formal_0_193 70 42))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_194)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_194) (select (m_origin formal_0_194) 72) (select (m_origin formal_0_194) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_194) (select (m_origin formal_0_194) 72) (select (m_origin formal_0_194) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_195 () FormalMachine (FormalCallback formal_0_194 boundary_0 (select (m_origin formal_0_194) 72) (select (m_origin formal_0_194) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_196 () FormalMachine (FormalWriteFromOrigin formal_0_195 42 72))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_196)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_196) (select (m_origin formal_0_196) 73) (select (m_origin formal_0_196) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_196) (select (m_origin formal_0_196) 73) (select (m_origin formal_0_196) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_197 () FormalMachine (FormalCallback formal_0_196 boundary_0 (select (m_origin formal_0_196) 73) (select (m_origin formal_0_196) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_198 () FormalMachine (FormalWriteFromOrigin formal_0_197 42 73))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_198)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_198) (select (m_origin formal_0_198) 0) (select (m_origin formal_0_198) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_198) (select (m_origin formal_0_198) 0) (select (m_origin formal_0_198) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_199 () FormalMachine (FormalCallback formal_0_198 boundary_0 (select (m_origin formal_0_198) 0) (select (m_origin formal_0_198) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_200 () FormalMachine (FormalWriteFromOrigin formal_0_199 43 0))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_201 () FormalMachine (FormalWriteFromOrigin formal_0_200 73 43))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_201)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_201) (select (m_origin formal_0_201) 75) (select (m_origin formal_0_201) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_201) (select (m_origin formal_0_201) 75) (select (m_origin formal_0_201) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_202 () FormalMachine (FormalCallback formal_0_201 boundary_0 (select (m_origin formal_0_201) 75) (select (m_origin formal_0_201) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_203 () FormalMachine (FormalWriteFromOrigin formal_0_202 43 75))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_203)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_203) (select (m_origin formal_0_203) 76) (select (m_origin formal_0_203) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_203) (select (m_origin formal_0_203) 76) (select (m_origin formal_0_203) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_204 () FormalMachine (FormalCallback formal_0_203 boundary_0 (select (m_origin formal_0_203) 76) (select (m_origin formal_0_203) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_205 () FormalMachine (FormalWriteFromOrigin formal_0_204 43 76))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_205)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_205) (select (m_origin formal_0_205) 77) (select (m_origin formal_0_205) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_205) (select (m_origin formal_0_205) 77) (select (m_origin formal_0_205) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_206 () FormalMachine (FormalCallback formal_0_205 boundary_0 (select (m_origin formal_0_205) 77) (select (m_origin formal_0_205) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_207 () FormalMachine (FormalWriteFromOrigin formal_0_206 43 77))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_207)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_207) (select (m_origin formal_0_207) 78) (select (m_origin formal_0_207) 74)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_207) (select (m_origin formal_0_207) 78) (select (m_origin formal_0_207) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_208 () FormalMachine (FormalCallback formal_0_207 boundary_0 (select (m_origin formal_0_207) 78) (select (m_origin formal_0_207) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_209 () FormalMachine (FormalWriteFromOrigin formal_0_208 43 78))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_209)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_209) (select (m_origin formal_0_209) 79) (select (m_origin formal_0_209) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_209) (select (m_origin formal_0_209) 79) (select (m_origin formal_0_209) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_210 () FormalMachine (FormalCallback formal_0_209 boundary_0 (select (m_origin formal_0_209) 79) (select (m_origin formal_0_209) 74)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_211 () FormalMachine (FormalWriteFromOrigin formal_0_210 43 79))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_211)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_211) (select (m_origin formal_0_211) 1) (select (m_origin formal_0_211) 74)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_211) (select (m_origin formal_0_211) 1) (select (m_origin formal_0_211) 74)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_212 () FormalMachine (FormalCallback formal_0_211 boundary_0 (select (m_origin formal_0_211) 1) (select (m_origin formal_0_211) 74)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_213 () FormalMachine (FormalWriteFromOrigin formal_0_212 44 1))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_214 () FormalMachine (FormalWriteFromOrigin formal_0_213 79 28))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_215 () FormalMachine (FormalSwap formal_0_214 0 44))
; source callback case=recursive-pivot phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_215)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_215) (select (m_origin formal_0_215) 1) (select (m_origin formal_0_215) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_215) (select (m_origin formal_0_215) 1) (select (m_origin formal_0_215) 33)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_216 () FormalMachine (FormalCallback formal_0_215 boundary_0 (select (m_origin formal_0_215) 1) (select (m_origin formal_0_215) 33)))
; source callback case=recursive-pivot phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_216)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_216) (select (m_origin formal_0_216) 1) (select (m_origin formal_0_216) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_216) (select (m_origin formal_0_216) 1) (select (m_origin formal_0_216) 58)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_217 () FormalMachine (FormalCallback formal_0_216 boundary_0 (select (m_origin formal_0_216) 1) (select (m_origin formal_0_216) 58)))
; source callback case=recursive-pivot phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_217)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_217) (select (m_origin formal_0_217) 33) (select (m_origin formal_0_217) 58)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_217) (select (m_origin formal_0_217) 33) (select (m_origin formal_0_217) 58)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_218 () FormalMachine (FormalCallback formal_0_217 boundary_0 (select (m_origin formal_0_217) 33) (select (m_origin formal_0_217) 58)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_219 () FormalMachine (FormalSwap formal_0_218 0 35))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_219)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_219) (select (m_origin formal_0_219) 4) (select (m_origin formal_0_219) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_219) (select (m_origin formal_0_219) 4) (select (m_origin formal_0_219) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_220 () FormalMachine (FormalCallback formal_0_219 boundary_0 (select (m_origin formal_0_219) 4) (select (m_origin formal_0_219) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_221 () FormalMachine (FormalWriteFromOrigin formal_0_220 1 4))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_221)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_221) (select (m_origin formal_0_221) 8) (select (m_origin formal_0_221) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_221) (select (m_origin formal_0_221) 8) (select (m_origin formal_0_221) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_222 () FormalMachine (FormalCallback formal_0_221 boundary_0 (select (m_origin formal_0_221) 8) (select (m_origin formal_0_221) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_223 () FormalMachine (FormalWriteFromOrigin formal_0_222 1 8))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_223)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_223) (select (m_origin formal_0_223) 9) (select (m_origin formal_0_223) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_223) (select (m_origin formal_0_223) 9) (select (m_origin formal_0_223) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_224 () FormalMachine (FormalCallback formal_0_223 boundary_0 (select (m_origin formal_0_223) 9) (select (m_origin formal_0_223) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_225 () FormalMachine (FormalWriteFromOrigin formal_0_224 1 9))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_225)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_225) (select (m_origin formal_0_225) 10) (select (m_origin formal_0_225) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_225) (select (m_origin formal_0_225) 10) (select (m_origin formal_0_225) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_226 () FormalMachine (FormalCallback formal_0_225 boundary_0 (select (m_origin formal_0_225) 10) (select (m_origin formal_0_225) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_227 () FormalMachine (FormalWriteFromOrigin formal_0_226 1 10))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_227)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_227) (select (m_origin formal_0_227) 12) (select (m_origin formal_0_227) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_227) (select (m_origin formal_0_227) 12) (select (m_origin formal_0_227) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_228 () FormalMachine (FormalCallback formal_0_227 boundary_0 (select (m_origin formal_0_227) 12) (select (m_origin formal_0_227) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_229 () FormalMachine (FormalWriteFromOrigin formal_0_228 1 12))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_229)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_229) (select (m_origin formal_0_229) 14) (select (m_origin formal_0_229) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_229) (select (m_origin formal_0_229) 14) (select (m_origin formal_0_229) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_230 () FormalMachine (FormalCallback formal_0_229 boundary_0 (select (m_origin formal_0_229) 14) (select (m_origin formal_0_229) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_231 () FormalMachine (FormalWriteFromOrigin formal_0_230 1 14))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_231)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_231) (select (m_origin formal_0_231) 15) (select (m_origin formal_0_231) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_231) (select (m_origin formal_0_231) 15) (select (m_origin formal_0_231) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_232 () FormalMachine (FormalCallback formal_0_231 boundary_0 (select (m_origin formal_0_231) 15) (select (m_origin formal_0_231) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_233 () FormalMachine (FormalWriteFromOrigin formal_0_232 1 15))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_233)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_233) (select (m_origin formal_0_233) 16) (select (m_origin formal_0_233) 58)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_233) (select (m_origin formal_0_233) 16) (select (m_origin formal_0_233) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_234 () FormalMachine (FormalCallback formal_0_233 boundary_0 (select (m_origin formal_0_233) 16) (select (m_origin formal_0_233) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_235 () FormalMachine (FormalWriteFromOrigin formal_0_234 1 16))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_235)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_235) (select (m_origin formal_0_235) 17) (select (m_origin formal_0_235) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_235) (select (m_origin formal_0_235) 17) (select (m_origin formal_0_235) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_236 () FormalMachine (FormalCallback formal_0_235 boundary_0 (select (m_origin formal_0_235) 17) (select (m_origin formal_0_235) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_237 () FormalMachine (FormalWriteFromOrigin formal_0_236 2 17))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_238 () FormalMachine (FormalWriteFromOrigin formal_0_237 9 4))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_238)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_238) (select (m_origin formal_0_238) 20) (select (m_origin formal_0_238) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_238) (select (m_origin formal_0_238) 20) (select (m_origin formal_0_238) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_239 () FormalMachine (FormalCallback formal_0_238 boundary_0 (select (m_origin formal_0_238) 20) (select (m_origin formal_0_238) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_240 () FormalMachine (FormalWriteFromOrigin formal_0_239 2 20))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_240)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_240) (select (m_origin formal_0_240) 21) (select (m_origin formal_0_240) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_240) (select (m_origin formal_0_240) 21) (select (m_origin formal_0_240) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_241 () FormalMachine (FormalCallback formal_0_240 boundary_0 (select (m_origin formal_0_240) 21) (select (m_origin formal_0_240) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_242 () FormalMachine (FormalWriteFromOrigin formal_0_241 2 21))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_242)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_242) (select (m_origin formal_0_242) 22) (select (m_origin formal_0_242) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_242) (select (m_origin formal_0_242) 22) (select (m_origin formal_0_242) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_243 () FormalMachine (FormalCallback formal_0_242 boundary_0 (select (m_origin formal_0_242) 22) (select (m_origin formal_0_242) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_244 () FormalMachine (FormalWriteFromOrigin formal_0_243 2 22))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_244)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_244) (select (m_origin formal_0_244) 23) (select (m_origin formal_0_244) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_244) (select (m_origin formal_0_244) 23) (select (m_origin formal_0_244) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_245 () FormalMachine (FormalCallback formal_0_244 boundary_0 (select (m_origin formal_0_244) 23) (select (m_origin formal_0_244) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_246 () FormalMachine (FormalWriteFromOrigin formal_0_245 2 23))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_246)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_246) (select (m_origin formal_0_246) 25) (select (m_origin formal_0_246) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_246) (select (m_origin formal_0_246) 25) (select (m_origin formal_0_246) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_247 () FormalMachine (FormalCallback formal_0_246 boundary_0 (select (m_origin formal_0_246) 25) (select (m_origin formal_0_246) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_248 () FormalMachine (FormalWriteFromOrigin formal_0_247 2 25))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_248)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_248) (select (m_origin formal_0_248) 26) (select (m_origin formal_0_248) 58)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_248) (select (m_origin formal_0_248) 26) (select (m_origin formal_0_248) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_249 () FormalMachine (FormalCallback formal_0_248 boundary_0 (select (m_origin formal_0_248) 26) (select (m_origin formal_0_248) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_250 () FormalMachine (FormalWriteFromOrigin formal_0_249 2 26))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_250)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_250) (select (m_origin formal_0_250) 27) (select (m_origin formal_0_250) 58)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_250) (select (m_origin formal_0_250) 27) (select (m_origin formal_0_250) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_251 () FormalMachine (FormalCallback formal_0_250 boundary_0 (select (m_origin formal_0_250) 27) (select (m_origin formal_0_250) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_252 () FormalMachine (FormalWriteFromOrigin formal_0_251 3 27))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_253 () FormalMachine (FormalWriteFromOrigin formal_0_252 16 8))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_253)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_253) (select (m_origin formal_0_253) 29) (select (m_origin formal_0_253) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_253) (select (m_origin formal_0_253) 29) (select (m_origin formal_0_253) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_254 () FormalMachine (FormalCallback formal_0_253 boundary_0 (select (m_origin formal_0_253) 29) (select (m_origin formal_0_253) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_255 () FormalMachine (FormalWriteFromOrigin formal_0_254 4 29))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_256 () FormalMachine (FormalWriteFromOrigin formal_0_255 17 9))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_256)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_256) (select (m_origin formal_0_256) 31) (select (m_origin formal_0_256) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_256) (select (m_origin formal_0_256) 31) (select (m_origin formal_0_256) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_257 () FormalMachine (FormalCallback formal_0_256 boundary_0 (select (m_origin formal_0_256) 31) (select (m_origin formal_0_256) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_258 () FormalMachine (FormalWriteFromOrigin formal_0_257 4 31))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_258)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_258) (select (m_origin formal_0_258) 33) (select (m_origin formal_0_258) 58)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_258) (select (m_origin formal_0_258) 33) (select (m_origin formal_0_258) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_259 () FormalMachine (FormalCallback formal_0_258 boundary_0 (select (m_origin formal_0_258) 33) (select (m_origin formal_0_258) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_260 () FormalMachine (FormalWriteFromOrigin formal_0_259 4 33))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_260)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_260) (select (m_origin formal_0_260) 34) (select (m_origin formal_0_260) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_260) (select (m_origin formal_0_260) 34) (select (m_origin formal_0_260) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_261 () FormalMachine (FormalCallback formal_0_260 boundary_0 (select (m_origin formal_0_260) 34) (select (m_origin formal_0_260) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_262 () FormalMachine (FormalWriteFromOrigin formal_0_261 5 34))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_263 () FormalMachine (FormalWriteFromOrigin formal_0_262 20 10))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_263)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_263) (select (m_origin formal_0_263) 36) (select (m_origin formal_0_263) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_263) (select (m_origin formal_0_263) 36) (select (m_origin formal_0_263) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_264 () FormalMachine (FormalCallback formal_0_263 boundary_0 (select (m_origin formal_0_263) 36) (select (m_origin formal_0_263) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_265 () FormalMachine (FormalWriteFromOrigin formal_0_264 5 36))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_265)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_265) (select (m_origin formal_0_265) 38) (select (m_origin formal_0_265) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_265) (select (m_origin formal_0_265) 38) (select (m_origin formal_0_265) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_266 () FormalMachine (FormalCallback formal_0_265 boundary_0 (select (m_origin formal_0_265) 38) (select (m_origin formal_0_265) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_267 () FormalMachine (FormalWriteFromOrigin formal_0_266 5 38))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_267)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_267) (select (m_origin formal_0_267) 39) (select (m_origin formal_0_267) 58)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_267) (select (m_origin formal_0_267) 39) (select (m_origin formal_0_267) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_268 () FormalMachine (FormalCallback formal_0_267 boundary_0 (select (m_origin formal_0_267) 39) (select (m_origin formal_0_267) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_269 () FormalMachine (FormalWriteFromOrigin formal_0_268 5 39))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_269)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_269) (select (m_origin formal_0_269) 40) (select (m_origin formal_0_269) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_269) (select (m_origin formal_0_269) 40) (select (m_origin formal_0_269) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_270 () FormalMachine (FormalCallback formal_0_269 boundary_0 (select (m_origin formal_0_269) 40) (select (m_origin formal_0_269) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_271 () FormalMachine (FormalWriteFromOrigin formal_0_270 6 40))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_272 () FormalMachine (FormalWriteFromOrigin formal_0_271 24 12))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_272)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_272) (select (m_origin formal_0_272) 41) (select (m_origin formal_0_272) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_272) (select (m_origin formal_0_272) 41) (select (m_origin formal_0_272) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_273 () FormalMachine (FormalCallback formal_0_272 boundary_0 (select (m_origin formal_0_272) 41) (select (m_origin formal_0_272) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_274 () FormalMachine (FormalWriteFromOrigin formal_0_273 6 41))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_274)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_274) (select (m_origin formal_0_274) 44) (select (m_origin formal_0_274) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_274) (select (m_origin formal_0_274) 44) (select (m_origin formal_0_274) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_275 () FormalMachine (FormalCallback formal_0_274 boundary_0 (select (m_origin formal_0_274) 44) (select (m_origin formal_0_274) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_276 () FormalMachine (FormalWriteFromOrigin formal_0_275 6 44))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_276)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_276) (select (m_origin formal_0_276) 47) (select (m_origin formal_0_276) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_276) (select (m_origin formal_0_276) 47) (select (m_origin formal_0_276) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_277 () FormalMachine (FormalCallback formal_0_276 boundary_0 (select (m_origin formal_0_276) 47) (select (m_origin formal_0_276) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_278 () FormalMachine (FormalWriteFromOrigin formal_0_277 6 47))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_278)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_278) (select (m_origin formal_0_278) 50) (select (m_origin formal_0_278) 58)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_278) (select (m_origin formal_0_278) 50) (select (m_origin formal_0_278) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_279 () FormalMachine (FormalCallback formal_0_278 boundary_0 (select (m_origin formal_0_278) 50) (select (m_origin formal_0_278) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_280 () FormalMachine (FormalWriteFromOrigin formal_0_279 6 50))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_280)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_280) (select (m_origin formal_0_280) 51) (select (m_origin formal_0_280) 58)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_280) (select (m_origin formal_0_280) 51) (select (m_origin formal_0_280) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_281 () FormalMachine (FormalCallback formal_0_280 boundary_0 (select (m_origin formal_0_280) 51) (select (m_origin formal_0_280) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_282 () FormalMachine (FormalWriteFromOrigin formal_0_281 7 51))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_283 () FormalMachine (FormalWriteFromOrigin formal_0_282 29 14))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_283)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_283) (select (m_origin formal_0_283) 52) (select (m_origin formal_0_283) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_283) (select (m_origin formal_0_283) 52) (select (m_origin formal_0_283) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_284 () FormalMachine (FormalCallback formal_0_283 boundary_0 (select (m_origin formal_0_283) 52) (select (m_origin formal_0_283) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_285 () FormalMachine (FormalWriteFromOrigin formal_0_284 8 52))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_286 () FormalMachine (FormalWriteFromOrigin formal_0_285 30 15))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_286)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 55) (select (m_origin formal_0_286) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 55) (select (m_origin formal_0_286) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_287 () FormalMachine (FormalCallback formal_0_286 boundary_0 (select (m_origin formal_0_286) 55) (select (m_origin formal_0_286) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_288 () FormalMachine (FormalWriteFromOrigin formal_0_287 8 55))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_288)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 56) (select (m_origin formal_0_288) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 56) (select (m_origin formal_0_288) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_289 () FormalMachine (FormalCallback formal_0_288 boundary_0 (select (m_origin formal_0_288) 56) (select (m_origin formal_0_288) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_290 () FormalMachine (FormalWriteFromOrigin formal_0_289 8 56))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_290)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_290) (select (m_origin formal_0_290) 57) (select (m_origin formal_0_290) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_290) (select (m_origin formal_0_290) 57) (select (m_origin formal_0_290) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_291 () FormalMachine (FormalCallback formal_0_290 boundary_0 (select (m_origin formal_0_290) 57) (select (m_origin formal_0_290) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_292 () FormalMachine (FormalWriteFromOrigin formal_0_291 8 57))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_292)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 1) (select (m_origin formal_0_292) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 1) (select (m_origin formal_0_292) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_293 () FormalMachine (FormalCallback formal_0_292 boundary_0 (select (m_origin formal_0_292) 1) (select (m_origin formal_0_292) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_294 () FormalMachine (FormalWriteFromOrigin formal_0_293 8 1))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_294)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_294) (select (m_origin formal_0_294) 62) (select (m_origin formal_0_294) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_294) (select (m_origin formal_0_294) 62) (select (m_origin formal_0_294) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_295 () FormalMachine (FormalCallback formal_0_294 boundary_0 (select (m_origin formal_0_294) 62) (select (m_origin formal_0_294) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_296 () FormalMachine (FormalWriteFromOrigin formal_0_295 8 62))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_296)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_296) (select (m_origin formal_0_296) 63) (select (m_origin formal_0_296) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_296) (select (m_origin formal_0_296) 63) (select (m_origin formal_0_296) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_297 () FormalMachine (FormalCallback formal_0_296 boundary_0 (select (m_origin formal_0_296) 63) (select (m_origin formal_0_296) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_298 () FormalMachine (FormalWriteFromOrigin formal_0_297 8 63))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_298)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_298) (select (m_origin formal_0_298) 64) (select (m_origin formal_0_298) 58)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_298) (select (m_origin formal_0_298) 64) (select (m_origin formal_0_298) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_299 () FormalMachine (FormalCallback formal_0_298 boundary_0 (select (m_origin formal_0_298) 64) (select (m_origin formal_0_298) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_300 () FormalMachine (FormalWriteFromOrigin formal_0_299 8 64))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_300)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_300) (select (m_origin formal_0_300) 66) (select (m_origin formal_0_300) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_300) (select (m_origin formal_0_300) 66) (select (m_origin formal_0_300) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_301 () FormalMachine (FormalCallback formal_0_300 boundary_0 (select (m_origin formal_0_300) 66) (select (m_origin formal_0_300) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_302 () FormalMachine (FormalWriteFromOrigin formal_0_301 9 66))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_303 () FormalMachine (FormalWriteFromOrigin formal_0_302 38 4))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_303)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_303) (select (m_origin formal_0_303) 69) (select (m_origin formal_0_303) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_303) (select (m_origin formal_0_303) 69) (select (m_origin formal_0_303) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_304 () FormalMachine (FormalCallback formal_0_303 boundary_0 (select (m_origin formal_0_303) 69) (select (m_origin formal_0_303) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_305 () FormalMachine (FormalWriteFromOrigin formal_0_304 9 69))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_305)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_305) (select (m_origin formal_0_305) 70) (select (m_origin formal_0_305) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_305) (select (m_origin formal_0_305) 70) (select (m_origin formal_0_305) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_306 () FormalMachine (FormalCallback formal_0_305 boundary_0 (select (m_origin formal_0_305) 70) (select (m_origin formal_0_305) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_307 () FormalMachine (FormalWriteFromOrigin formal_0_306 9 70))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_307)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_307) (select (m_origin formal_0_307) 73) (select (m_origin formal_0_307) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_307) (select (m_origin formal_0_307) 73) (select (m_origin formal_0_307) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_308 () FormalMachine (FormalCallback formal_0_307 boundary_0 (select (m_origin formal_0_307) 73) (select (m_origin formal_0_307) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_309 () FormalMachine (FormalWriteFromOrigin formal_0_308 9 73))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_309)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_309) (select (m_origin formal_0_309) 79) (select (m_origin formal_0_309) 58)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_309) (select (m_origin formal_0_309) 79) (select (m_origin formal_0_309) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_310 () FormalMachine (FormalCallback formal_0_309 boundary_0 (select (m_origin formal_0_309) 79) (select (m_origin formal_0_309) 58)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_311 () FormalMachine (FormalWriteFromOrigin formal_0_310 9 79))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_311)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_311) (select (m_origin formal_0_311) 3) (select (m_origin formal_0_311) 58)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_311) (select (m_origin formal_0_311) 3) (select (m_origin formal_0_311) 58)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_312 () FormalMachine (FormalCallback formal_0_311 boundary_0 (select (m_origin formal_0_311) 3) (select (m_origin formal_0_311) 58)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_313 () FormalMachine (FormalWriteFromOrigin formal_0_312 10 3))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_314 () FormalMachine (FormalWriteFromOrigin formal_0_313 43 17))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_315 () FormalMachine (FormalSwap formal_0_314 0 9))
; source callback case=recursive-pivot phase=insert-tail[0:9:1]:initial-compare
(assert (not (m_panicked formal_0_315)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_315) (select (m_origin formal_0_315) 16) (select (m_origin formal_0_315) 79)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_315) (select (m_origin formal_0_315) 16) (select (m_origin formal_0_315) 79)) false))
; source callback transition phase=insert-tail[0:9:1]:initial-compare
(define-fun formal_0_316 () FormalMachine (FormalCallback formal_0_315 boundary_0 (select (m_origin formal_0_315) 16) (select (m_origin formal_0_315) 79)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:1]
(define-fun formal_0_317 () FormalMachine (FormalWriteFromOrigin formal_0_316 1 79))
; source write kind=copy-on-drop-restore phase=insert-tail[0:9:1]
(define-fun formal_0_318 () FormalMachine (FormalWriteFromOrigin formal_0_317 0 16))
; source callback case=recursive-pivot phase=insert-tail[0:9:2]:initial-compare
(assert (not (m_panicked formal_0_318)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_318) (select (m_origin formal_0_318) 26) (select (m_origin formal_0_318) 79)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_318) (select (m_origin formal_0_318) 26) (select (m_origin formal_0_318) 79)) false))
; source callback transition phase=insert-tail[0:9:2]:initial-compare
(define-fun formal_0_319 () FormalMachine (FormalCallback formal_0_318 boundary_0 (select (m_origin formal_0_318) 26) (select (m_origin formal_0_318) 79)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:2]
(define-fun formal_0_320 () FormalMachine (FormalWriteFromOrigin formal_0_319 2 79))
; source callback case=recursive-pivot phase=insert-tail[0:9:2]:sift-compare
(assert (not (m_panicked formal_0_320)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_320) (select (m_origin formal_0_320) 26) (select (m_origin formal_0_320) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_320) (select (m_origin formal_0_320) 26) (select (m_origin formal_0_320) 16)) false))
; source callback transition phase=insert-tail[0:9:2]:sift-compare
(define-fun formal_0_321 () FormalMachine (FormalCallback formal_0_320 boundary_0 (select (m_origin formal_0_320) 26) (select (m_origin formal_0_320) 16)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:9:2]
(define-fun formal_0_322 () FormalMachine (FormalWriteFromOrigin formal_0_321 1 26))
; source callback case=recursive-pivot phase=insert-tail[0:9:3]:initial-compare
(assert (not (m_panicked formal_0_322)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 27) (select (m_origin formal_0_322) 79)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 27) (select (m_origin formal_0_322) 79)) false))
; source callback transition phase=insert-tail[0:9:3]:initial-compare
(define-fun formal_0_323 () FormalMachine (FormalCallback formal_0_322 boundary_0 (select (m_origin formal_0_322) 27) (select (m_origin formal_0_322) 79)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:3]
(define-fun formal_0_324 () FormalMachine (FormalWriteFromOrigin formal_0_323 3 79))
; source callback case=recursive-pivot phase=insert-tail[0:9:3]:sift-compare
(assert (not (m_panicked formal_0_324)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_324) (select (m_origin formal_0_324) 27) (select (m_origin formal_0_324) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_324) (select (m_origin formal_0_324) 27) (select (m_origin formal_0_324) 26)) false))
; source callback transition phase=insert-tail[0:9:3]:sift-compare
(define-fun formal_0_325 () FormalMachine (FormalCallback formal_0_324 boundary_0 (select (m_origin formal_0_324) 27) (select (m_origin formal_0_324) 26)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:3]
(define-fun formal_0_326 () FormalMachine (FormalWriteFromOrigin formal_0_325 2 26))
; source callback case=recursive-pivot phase=insert-tail[0:9:3]:sift-compare
(assert (not (m_panicked formal_0_326)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_326) (select (m_origin formal_0_326) 27) (select (m_origin formal_0_326) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_326) (select (m_origin formal_0_326) 27) (select (m_origin formal_0_326) 16)) false))
; source callback transition phase=insert-tail[0:9:3]:sift-compare
(define-fun formal_0_327 () FormalMachine (FormalCallback formal_0_326 boundary_0 (select (m_origin formal_0_326) 27) (select (m_origin formal_0_326) 16)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:9:3]
(define-fun formal_0_328 () FormalMachine (FormalWriteFromOrigin formal_0_327 1 27))
; source callback case=recursive-pivot phase=insert-tail[0:9:4]:initial-compare
(assert (not (m_panicked formal_0_328)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_328) (select (m_origin formal_0_328) 33) (select (m_origin formal_0_328) 79)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_328) (select (m_origin formal_0_328) 33) (select (m_origin formal_0_328) 79)) false))
; source callback transition phase=insert-tail[0:9:4]:initial-compare
(define-fun formal_0_329 () FormalMachine (FormalCallback formal_0_328 boundary_0 (select (m_origin formal_0_328) 33) (select (m_origin formal_0_328) 79)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:4]
(define-fun formal_0_330 () FormalMachine (FormalWriteFromOrigin formal_0_329 4 79))
; source callback case=recursive-pivot phase=insert-tail[0:9:4]:sift-compare
(assert (not (m_panicked formal_0_330)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_330) (select (m_origin formal_0_330) 33) (select (m_origin formal_0_330) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_330) (select (m_origin formal_0_330) 33) (select (m_origin formal_0_330) 26)) false))
; source callback transition phase=insert-tail[0:9:4]:sift-compare
(define-fun formal_0_331 () FormalMachine (FormalCallback formal_0_330 boundary_0 (select (m_origin formal_0_330) 33) (select (m_origin formal_0_330) 26)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:4]
(define-fun formal_0_332 () FormalMachine (FormalWriteFromOrigin formal_0_331 3 26))
; source callback case=recursive-pivot phase=insert-tail[0:9:4]:sift-compare
(assert (not (m_panicked formal_0_332)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_332) (select (m_origin formal_0_332) 33) (select (m_origin formal_0_332) 27)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_332) (select (m_origin formal_0_332) 33) (select (m_origin formal_0_332) 27)) false))
; source callback transition phase=insert-tail[0:9:4]:sift-compare
(define-fun formal_0_333 () FormalMachine (FormalCallback formal_0_332 boundary_0 (select (m_origin formal_0_332) 33) (select (m_origin formal_0_332) 27)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:9:4]
(define-fun formal_0_334 () FormalMachine (FormalWriteFromOrigin formal_0_333 2 33))
; source callback case=recursive-pivot phase=insert-tail[0:9:5]:initial-compare
(assert (not (m_panicked formal_0_334)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_334) (select (m_origin formal_0_334) 39) (select (m_origin formal_0_334) 79)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_334) (select (m_origin formal_0_334) 39) (select (m_origin formal_0_334) 79)) false))
; source callback transition phase=insert-tail[0:9:5]:initial-compare
(define-fun formal_0_335 () FormalMachine (FormalCallback formal_0_334 boundary_0 (select (m_origin formal_0_334) 39) (select (m_origin formal_0_334) 79)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:5]
(define-fun formal_0_336 () FormalMachine (FormalWriteFromOrigin formal_0_335 5 79))
; source callback case=recursive-pivot phase=insert-tail[0:9:5]:sift-compare
(assert (not (m_panicked formal_0_336)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_336) (select (m_origin formal_0_336) 39) (select (m_origin formal_0_336) 26)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_336) (select (m_origin formal_0_336) 39) (select (m_origin formal_0_336) 26)) false))
; source callback transition phase=insert-tail[0:9:5]:sift-compare
(define-fun formal_0_337 () FormalMachine (FormalCallback formal_0_336 boundary_0 (select (m_origin formal_0_336) 39) (select (m_origin formal_0_336) 26)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:9:5]
(define-fun formal_0_338 () FormalMachine (FormalWriteFromOrigin formal_0_337 4 39))
; source callback case=recursive-pivot phase=insert-tail[0:9:6]:initial-compare
(assert (not (m_panicked formal_0_338)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_338) (select (m_origin formal_0_338) 50) (select (m_origin formal_0_338) 79)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_338) (select (m_origin formal_0_338) 50) (select (m_origin formal_0_338) 79)) false))
; source callback transition phase=insert-tail[0:9:6]:initial-compare
(define-fun formal_0_339 () FormalMachine (FormalCallback formal_0_338 boundary_0 (select (m_origin formal_0_338) 50) (select (m_origin formal_0_338) 79)))
; source callback case=recursive-pivot phase=insert-tail[0:9:7]:initial-compare
(assert (not (m_panicked formal_0_339)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_339) (select (m_origin formal_0_339) 51) (select (m_origin formal_0_339) 50)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_339) (select (m_origin formal_0_339) 51) (select (m_origin formal_0_339) 50)) false))
; source callback transition phase=insert-tail[0:9:7]:initial-compare
(define-fun formal_0_340 () FormalMachine (FormalCallback formal_0_339 boundary_0 (select (m_origin formal_0_339) 51) (select (m_origin formal_0_339) 50)))
; source callback case=recursive-pivot phase=insert-tail[0:9:8]:initial-compare
(assert (not (m_panicked formal_0_340)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_340) (select (m_origin formal_0_340) 64) (select (m_origin formal_0_340) 51)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_340) (select (m_origin formal_0_340) 64) (select (m_origin formal_0_340) 51)) false))
; source callback transition phase=insert-tail[0:9:8]:initial-compare
(define-fun formal_0_341 () FormalMachine (FormalCallback formal_0_340 boundary_0 (select (m_origin formal_0_340) 64) (select (m_origin formal_0_340) 51)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:8]
(define-fun formal_0_342 () FormalMachine (FormalWriteFromOrigin formal_0_341 8 51))
; source callback case=recursive-pivot phase=insert-tail[0:9:8]:sift-compare
(assert (not (m_panicked formal_0_342)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_342) (select (m_origin formal_0_342) 64) (select (m_origin formal_0_342) 50)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_342) (select (m_origin formal_0_342) 64) (select (m_origin formal_0_342) 50)) false))
; source callback transition phase=insert-tail[0:9:8]:sift-compare
(define-fun formal_0_343 () FormalMachine (FormalCallback formal_0_342 boundary_0 (select (m_origin formal_0_342) 64) (select (m_origin formal_0_342) 50)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:8]
(define-fun formal_0_344 () FormalMachine (FormalWriteFromOrigin formal_0_343 7 50))
; source callback case=recursive-pivot phase=insert-tail[0:9:8]:sift-compare
(assert (not (m_panicked formal_0_344)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_344) (select (m_origin formal_0_344) 64) (select (m_origin formal_0_344) 79)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_344) (select (m_origin formal_0_344) 64) (select (m_origin formal_0_344) 79)) false))
; source callback transition phase=insert-tail[0:9:8]:sift-compare
(define-fun formal_0_345 () FormalMachine (FormalCallback formal_0_344 boundary_0 (select (m_origin formal_0_344) 64) (select (m_origin formal_0_344) 79)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:8]
(define-fun formal_0_346 () FormalMachine (FormalWriteFromOrigin formal_0_345 6 79))
; source callback case=recursive-pivot phase=insert-tail[0:9:8]:sift-compare
(assert (not (m_panicked formal_0_346)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_346) (select (m_origin formal_0_346) 64) (select (m_origin formal_0_346) 39)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_346) (select (m_origin formal_0_346) 64) (select (m_origin formal_0_346) 39)) false))
; source callback transition phase=insert-tail[0:9:8]:sift-compare
(define-fun formal_0_347 () FormalMachine (FormalCallback formal_0_346 boundary_0 (select (m_origin formal_0_346) 64) (select (m_origin formal_0_346) 39)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:8]
(define-fun formal_0_348 () FormalMachine (FormalWriteFromOrigin formal_0_347 5 39))
; source callback case=recursive-pivot phase=insert-tail[0:9:8]:sift-compare
(assert (not (m_panicked formal_0_348)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_348) (select (m_origin formal_0_348) 64) (select (m_origin formal_0_348) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_348) (select (m_origin formal_0_348) 64) (select (m_origin formal_0_348) 26)) false))
; source callback transition phase=insert-tail[0:9:8]:sift-compare
(define-fun formal_0_349 () FormalMachine (FormalCallback formal_0_348 boundary_0 (select (m_origin formal_0_348) 64) (select (m_origin formal_0_348) 26)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:8]
(define-fun formal_0_350 () FormalMachine (FormalWriteFromOrigin formal_0_349 4 26))
; source callback case=recursive-pivot phase=insert-tail[0:9:8]:sift-compare
(assert (not (m_panicked formal_0_350)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_350) (select (m_origin formal_0_350) 64) (select (m_origin formal_0_350) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_350) (select (m_origin formal_0_350) 64) (select (m_origin formal_0_350) 33)) false))
; source callback transition phase=insert-tail[0:9:8]:sift-compare
(define-fun formal_0_351 () FormalMachine (FormalCallback formal_0_350 boundary_0 (select (m_origin formal_0_350) 64) (select (m_origin formal_0_350) 33)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:8]
(define-fun formal_0_352 () FormalMachine (FormalWriteFromOrigin formal_0_351 3 33))
; source callback case=recursive-pivot phase=insert-tail[0:9:8]:sift-compare
(assert (not (m_panicked formal_0_352)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_352) (select (m_origin formal_0_352) 64) (select (m_origin formal_0_352) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_352) (select (m_origin formal_0_352) 64) (select (m_origin formal_0_352) 27)) false))
; source callback transition phase=insert-tail[0:9:8]:sift-compare
(define-fun formal_0_353 () FormalMachine (FormalCallback formal_0_352 boundary_0 (select (m_origin formal_0_352) 64) (select (m_origin formal_0_352) 27)))
; source write kind=insert-tail-shift phase=insert-tail[0:9:8]
(define-fun formal_0_354 () FormalMachine (FormalWriteFromOrigin formal_0_353 2 27))
; source callback case=recursive-pivot phase=insert-tail[0:9:8]:sift-compare
(assert (not (m_panicked formal_0_354)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_354) (select (m_origin formal_0_354) 64) (select (m_origin formal_0_354) 16)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_354) (select (m_origin formal_0_354) 64) (select (m_origin formal_0_354) 16)) false))
; source callback transition phase=insert-tail[0:9:8]:sift-compare
(define-fun formal_0_355 () FormalMachine (FormalCallback formal_0_354 boundary_0 (select (m_origin formal_0_354) 64) (select (m_origin formal_0_354) 16)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:9:8]
(define-fun formal_0_356 () FormalMachine (FormalWriteFromOrigin formal_0_355 1 64))
; source callback case=recursive-pivot phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_356)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_356) (select (m_origin formal_0_356) 3) (select (m_origin formal_0_356) 41)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_356) (select (m_origin formal_0_356) 3) (select (m_origin formal_0_356) 41)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_357 () FormalMachine (FormalCallback formal_0_356 boundary_0 (select (m_origin formal_0_356) 3) (select (m_origin formal_0_356) 41)))
; source callback case=recursive-pivot phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_357)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 3) (select (m_origin formal_0_357) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 3) (select (m_origin formal_0_357) 4)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_358 () FormalMachine (FormalCallback formal_0_357 boundary_0 (select (m_origin formal_0_357) 3) (select (m_origin formal_0_357) 4)))
; source callback case=recursive-pivot phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_358)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_358) (select (m_origin formal_0_358) 58) (select (m_origin formal_0_358) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_358) (select (m_origin formal_0_358) 58) (select (m_origin formal_0_358) 3)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_359 () FormalMachine (FormalCallback formal_0_358 boundary_0 (select (m_origin formal_0_358) 58) (select (m_origin formal_0_358) 3)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_360 () FormalMachine (FormalSwap formal_0_359 10 10))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_360)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_360) (select (m_origin formal_0_360) 21) (select (m_origin formal_0_360) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_360) (select (m_origin formal_0_360) 21) (select (m_origin formal_0_360) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_361 () FormalMachine (FormalCallback formal_0_360 boundary_0 (select (m_origin formal_0_360) 21) (select (m_origin formal_0_360) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_362 () FormalMachine (FormalWriteFromOrigin formal_0_361 11 21))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_362)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_362) (select (m_origin formal_0_362) 22) (select (m_origin formal_0_362) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_362) (select (m_origin formal_0_362) 22) (select (m_origin formal_0_362) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_363 () FormalMachine (FormalCallback formal_0_362 boundary_0 (select (m_origin formal_0_362) 22) (select (m_origin formal_0_362) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_364 () FormalMachine (FormalWriteFromOrigin formal_0_363 12 22))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_364)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_364) (select (m_origin formal_0_364) 23) (select (m_origin formal_0_364) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_364) (select (m_origin formal_0_364) 23) (select (m_origin formal_0_364) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_365 () FormalMachine (FormalCallback formal_0_364 boundary_0 (select (m_origin formal_0_364) 23) (select (m_origin formal_0_364) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_366 () FormalMachine (FormalWriteFromOrigin formal_0_365 13 23))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_366)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_366) (select (m_origin formal_0_366) 25) (select (m_origin formal_0_366) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_366) (select (m_origin formal_0_366) 25) (select (m_origin formal_0_366) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_367 () FormalMachine (FormalCallback formal_0_366 boundary_0 (select (m_origin formal_0_366) 25) (select (m_origin formal_0_366) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_368 () FormalMachine (FormalWriteFromOrigin formal_0_367 14 25))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_368)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_368) (select (m_origin formal_0_368) 8) (select (m_origin formal_0_368) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_368) (select (m_origin formal_0_368) 8) (select (m_origin formal_0_368) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_369 () FormalMachine (FormalCallback formal_0_368 boundary_0 (select (m_origin formal_0_368) 8) (select (m_origin formal_0_368) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_370 () FormalMachine (FormalWriteFromOrigin formal_0_369 14 8))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_370)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_370) (select (m_origin formal_0_370) 9) (select (m_origin formal_0_370) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_370) (select (m_origin formal_0_370) 9) (select (m_origin formal_0_370) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_371 () FormalMachine (FormalCallback formal_0_370 boundary_0 (select (m_origin formal_0_370) 9) (select (m_origin formal_0_370) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_372 () FormalMachine (FormalWriteFromOrigin formal_0_371 15 9))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_373 () FormalMachine (FormalWriteFromOrigin formal_0_372 16 25))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_373)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_373) (select (m_origin formal_0_373) 29) (select (m_origin formal_0_373) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_373) (select (m_origin formal_0_373) 29) (select (m_origin formal_0_373) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_374 () FormalMachine (FormalCallback formal_0_373 boundary_0 (select (m_origin formal_0_373) 29) (select (m_origin formal_0_373) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_375 () FormalMachine (FormalWriteFromOrigin formal_0_374 16 29))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_376 () FormalMachine (FormalWriteFromOrigin formal_0_375 17 25))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_376)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_376) (select (m_origin formal_0_376) 31) (select (m_origin formal_0_376) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_376) (select (m_origin formal_0_376) 31) (select (m_origin formal_0_376) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_377 () FormalMachine (FormalCallback formal_0_376 boundary_0 (select (m_origin formal_0_376) 31) (select (m_origin formal_0_376) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_378 () FormalMachine (FormalWriteFromOrigin formal_0_377 17 31))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_379 () FormalMachine (FormalWriteFromOrigin formal_0_378 18 25))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_379)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_379) (select (m_origin formal_0_379) 10) (select (m_origin formal_0_379) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_379) (select (m_origin formal_0_379) 10) (select (m_origin formal_0_379) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_380 () FormalMachine (FormalCallback formal_0_379 boundary_0 (select (m_origin formal_0_379) 10) (select (m_origin formal_0_379) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_381 () FormalMachine (FormalWriteFromOrigin formal_0_380 18 10))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_382 () FormalMachine (FormalWriteFromOrigin formal_0_381 19 25))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_382)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_382) (select (m_origin formal_0_382) 34) (select (m_origin formal_0_382) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_382) (select (m_origin formal_0_382) 34) (select (m_origin formal_0_382) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_383 () FormalMachine (FormalCallback formal_0_382 boundary_0 (select (m_origin formal_0_382) 34) (select (m_origin formal_0_382) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_384 () FormalMachine (FormalWriteFromOrigin formal_0_383 18 34))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_384)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_384) (select (m_origin formal_0_384) 36) (select (m_origin formal_0_384) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_384) (select (m_origin formal_0_384) 36) (select (m_origin formal_0_384) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_385 () FormalMachine (FormalCallback formal_0_384 boundary_0 (select (m_origin formal_0_384) 36) (select (m_origin formal_0_384) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_386 () FormalMachine (FormalWriteFromOrigin formal_0_385 18 36))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_386)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_386) (select (m_origin formal_0_386) 38) (select (m_origin formal_0_386) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_386) (select (m_origin formal_0_386) 38) (select (m_origin formal_0_386) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_387 () FormalMachine (FormalCallback formal_0_386 boundary_0 (select (m_origin formal_0_386) 38) (select (m_origin formal_0_386) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_388 () FormalMachine (FormalWriteFromOrigin formal_0_387 18 38))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_388)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_388) (select (m_origin formal_0_388) 12) (select (m_origin formal_0_388) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_388) (select (m_origin formal_0_388) 12) (select (m_origin formal_0_388) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_389 () FormalMachine (FormalCallback formal_0_388 boundary_0 (select (m_origin formal_0_388) 12) (select (m_origin formal_0_388) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_390 () FormalMachine (FormalWriteFromOrigin formal_0_389 19 12))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_391 () FormalMachine (FormalWriteFromOrigin formal_0_390 23 25))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_391)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_391) (select (m_origin formal_0_391) 40) (select (m_origin formal_0_391) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_391) (select (m_origin formal_0_391) 40) (select (m_origin formal_0_391) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_392 () FormalMachine (FormalCallback formal_0_391 boundary_0 (select (m_origin formal_0_391) 40) (select (m_origin formal_0_391) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_393 () FormalMachine (FormalWriteFromOrigin formal_0_392 19 40))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_393)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_393) (select (m_origin formal_0_393) 41) (select (m_origin formal_0_393) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_393) (select (m_origin formal_0_393) 41) (select (m_origin formal_0_393) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_394 () FormalMachine (FormalCallback formal_0_393 boundary_0 (select (m_origin formal_0_393) 41) (select (m_origin formal_0_393) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_395 () FormalMachine (FormalWriteFromOrigin formal_0_394 19 41))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_395)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_395) (select (m_origin formal_0_395) 44) (select (m_origin formal_0_395) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_395) (select (m_origin formal_0_395) 44) (select (m_origin formal_0_395) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_396 () FormalMachine (FormalCallback formal_0_395 boundary_0 (select (m_origin formal_0_395) 44) (select (m_origin formal_0_395) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_397 () FormalMachine (FormalWriteFromOrigin formal_0_396 19 44))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_397)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_397) (select (m_origin formal_0_397) 47) (select (m_origin formal_0_397) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_397) (select (m_origin formal_0_397) 47) (select (m_origin formal_0_397) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_398 () FormalMachine (FormalCallback formal_0_397 boundary_0 (select (m_origin formal_0_397) 47) (select (m_origin formal_0_397) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_399 () FormalMachine (FormalWriteFromOrigin formal_0_398 19 47))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_399)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_399) (select (m_origin formal_0_399) 14) (select (m_origin formal_0_399) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_399) (select (m_origin formal_0_399) 14) (select (m_origin formal_0_399) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_400 () FormalMachine (FormalCallback formal_0_399 boundary_0 (select (m_origin formal_0_399) 14) (select (m_origin formal_0_399) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_401 () FormalMachine (FormalWriteFromOrigin formal_0_400 20 14))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_402 () FormalMachine (FormalWriteFromOrigin formal_0_401 28 10))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_402)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_402) (select (m_origin formal_0_402) 15) (select (m_origin formal_0_402) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_402) (select (m_origin formal_0_402) 15) (select (m_origin formal_0_402) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_403 () FormalMachine (FormalCallback formal_0_402 boundary_0 (select (m_origin formal_0_402) 15) (select (m_origin formal_0_402) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_404 () FormalMachine (FormalWriteFromOrigin formal_0_403 21 15))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_405 () FormalMachine (FormalWriteFromOrigin formal_0_404 29 34))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_405)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_405) (select (m_origin formal_0_405) 52) (select (m_origin formal_0_405) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_405) (select (m_origin formal_0_405) 52) (select (m_origin formal_0_405) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_406 () FormalMachine (FormalCallback formal_0_405 boundary_0 (select (m_origin formal_0_405) 52) (select (m_origin formal_0_405) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_407 () FormalMachine (FormalWriteFromOrigin formal_0_406 22 52))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_408 () FormalMachine (FormalWriteFromOrigin formal_0_407 30 36))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_408)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_408) (select (m_origin formal_0_408) 55) (select (m_origin formal_0_408) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_408) (select (m_origin formal_0_408) 55) (select (m_origin formal_0_408) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_409 () FormalMachine (FormalCallback formal_0_408 boundary_0 (select (m_origin formal_0_408) 55) (select (m_origin formal_0_408) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_410 () FormalMachine (FormalWriteFromOrigin formal_0_409 23 55))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_411 () FormalMachine (FormalWriteFromOrigin formal_0_410 31 25))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_411)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_411) (select (m_origin formal_0_411) 56) (select (m_origin formal_0_411) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_411) (select (m_origin formal_0_411) 56) (select (m_origin formal_0_411) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_412 () FormalMachine (FormalCallback formal_0_411 boundary_0 (select (m_origin formal_0_411) 56) (select (m_origin formal_0_411) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_413 () FormalMachine (FormalWriteFromOrigin formal_0_412 24 56))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_414 () FormalMachine (FormalWriteFromOrigin formal_0_413 32 12))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_414)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_414) (select (m_origin formal_0_414) 57) (select (m_origin formal_0_414) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_414) (select (m_origin formal_0_414) 57) (select (m_origin formal_0_414) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_415 () FormalMachine (FormalCallback formal_0_414 boundary_0 (select (m_origin formal_0_414) 57) (select (m_origin formal_0_414) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_416 () FormalMachine (FormalWriteFromOrigin formal_0_415 25 57))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_417 () FormalMachine (FormalWriteFromOrigin formal_0_416 33 40))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_417)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_417) (select (m_origin formal_0_417) 1) (select (m_origin formal_0_417) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_417) (select (m_origin formal_0_417) 1) (select (m_origin formal_0_417) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_418 () FormalMachine (FormalCallback formal_0_417 boundary_0 (select (m_origin formal_0_417) 1) (select (m_origin formal_0_417) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_419 () FormalMachine (FormalWriteFromOrigin formal_0_418 26 1))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_420 () FormalMachine (FormalWriteFromOrigin formal_0_419 34 41))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_420)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_420) (select (m_origin formal_0_420) 62) (select (m_origin formal_0_420) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_420) (select (m_origin formal_0_420) 62) (select (m_origin formal_0_420) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_421 () FormalMachine (FormalCallback formal_0_420 boundary_0 (select (m_origin formal_0_420) 62) (select (m_origin formal_0_420) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_422 () FormalMachine (FormalWriteFromOrigin formal_0_421 27 62))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_423 () FormalMachine (FormalWriteFromOrigin formal_0_422 35 44))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_423)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_423) (select (m_origin formal_0_423) 63) (select (m_origin formal_0_423) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_423) (select (m_origin formal_0_423) 63) (select (m_origin formal_0_423) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_424 () FormalMachine (FormalCallback formal_0_423 boundary_0 (select (m_origin formal_0_423) 63) (select (m_origin formal_0_423) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_425 () FormalMachine (FormalWriteFromOrigin formal_0_424 27 63))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_425)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_425) (select (m_origin formal_0_425) 4) (select (m_origin formal_0_425) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_425) (select (m_origin formal_0_425) 4) (select (m_origin formal_0_425) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_426 () FormalMachine (FormalCallback formal_0_425 boundary_0 (select (m_origin formal_0_425) 4) (select (m_origin formal_0_425) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_427 () FormalMachine (FormalWriteFromOrigin formal_0_426 28 4))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_428 () FormalMachine (FormalWriteFromOrigin formal_0_427 37 10))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_428)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_428) (select (m_origin formal_0_428) 66) (select (m_origin formal_0_428) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_428) (select (m_origin formal_0_428) 66) (select (m_origin formal_0_428) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_429 () FormalMachine (FormalCallback formal_0_428 boundary_0 (select (m_origin formal_0_428) 66) (select (m_origin formal_0_428) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_430 () FormalMachine (FormalWriteFromOrigin formal_0_429 29 66))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_431 () FormalMachine (FormalWriteFromOrigin formal_0_430 38 34))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_431)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_431) (select (m_origin formal_0_431) 69) (select (m_origin formal_0_431) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_431) (select (m_origin formal_0_431) 69) (select (m_origin formal_0_431) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_432 () FormalMachine (FormalCallback formal_0_431 boundary_0 (select (m_origin formal_0_431) 69) (select (m_origin formal_0_431) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_433 () FormalMachine (FormalWriteFromOrigin formal_0_432 30 69))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_434 () FormalMachine (FormalWriteFromOrigin formal_0_433 39 36))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_434)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_434) (select (m_origin formal_0_434) 70) (select (m_origin formal_0_434) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_434) (select (m_origin formal_0_434) 70) (select (m_origin formal_0_434) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_435 () FormalMachine (FormalCallback formal_0_434 boundary_0 (select (m_origin formal_0_434) 70) (select (m_origin formal_0_434) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_436 () FormalMachine (FormalWriteFromOrigin formal_0_435 30 70))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_436)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_436) (select (m_origin formal_0_436) 73) (select (m_origin formal_0_436) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_436) (select (m_origin formal_0_436) 73) (select (m_origin formal_0_436) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_437 () FormalMachine (FormalCallback formal_0_436 boundary_0 (select (m_origin formal_0_436) 73) (select (m_origin formal_0_436) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_438 () FormalMachine (FormalWriteFromOrigin formal_0_437 31 73))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_439 () FormalMachine (FormalWriteFromOrigin formal_0_438 41 25))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_439)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_439) (select (m_origin formal_0_439) 17) (select (m_origin formal_0_439) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_439) (select (m_origin formal_0_439) 17) (select (m_origin formal_0_439) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_440 () FormalMachine (FormalCallback formal_0_439 boundary_0 (select (m_origin formal_0_439) 17) (select (m_origin formal_0_439) 3)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_441 () FormalMachine (FormalWriteFromOrigin formal_0_440 31 17))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_441)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_441) (select (m_origin formal_0_441) 20) (select (m_origin formal_0_441) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_441) (select (m_origin formal_0_441) 20) (select (m_origin formal_0_441) 3)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_442 () FormalMachine (FormalCallback formal_0_441 boundary_0 (select (m_origin formal_0_441) 20) (select (m_origin formal_0_441) 3)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_443 () FormalMachine (FormalWriteFromOrigin formal_0_442 32 20))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_444 () FormalMachine (FormalWriteFromOrigin formal_0_443 43 12))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_445 () FormalMachine (FormalSwap formal_0_444 10 32))
; source callback case=recursive-pivot phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_445)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_445) (select (m_origin formal_0_445) 20) (select (m_origin formal_0_445) 38)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_445) (select (m_origin formal_0_445) 20) (select (m_origin formal_0_445) 38)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_446 () FormalMachine (FormalCallback formal_0_445 boundary_0 (select (m_origin formal_0_445) 20) (select (m_origin formal_0_445) 38)))
; source callback case=recursive-pivot phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_446)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_446) (select (m_origin formal_0_446) 20) (select (m_origin formal_0_446) 56)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_446) (select (m_origin formal_0_446) 20) (select (m_origin formal_0_446) 56)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_447 () FormalMachine (FormalCallback formal_0_446 boundary_0 (select (m_origin formal_0_446) 20) (select (m_origin formal_0_446) 56)))
; source callback case=recursive-pivot phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_447)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_447) (select (m_origin formal_0_447) 58) (select (m_origin formal_0_447) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_447) (select (m_origin formal_0_447) 58) (select (m_origin formal_0_447) 20)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_448 () FormalMachine (FormalCallback formal_0_447 boundary_0 (select (m_origin formal_0_447) 58) (select (m_origin formal_0_447) 20)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_449 () FormalMachine (FormalSwap formal_0_448 10 10))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_449)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_449) (select (m_origin formal_0_449) 22) (select (m_origin formal_0_449) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_449) (select (m_origin formal_0_449) 22) (select (m_origin formal_0_449) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_450 () FormalMachine (FormalCallback formal_0_449 boundary_0 (select (m_origin formal_0_449) 22) (select (m_origin formal_0_449) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_451 () FormalMachine (FormalWriteFromOrigin formal_0_450 11 22))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_451)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_451) (select (m_origin formal_0_451) 23) (select (m_origin formal_0_451) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_451) (select (m_origin formal_0_451) 23) (select (m_origin formal_0_451) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_452 () FormalMachine (FormalCallback formal_0_451 boundary_0 (select (m_origin formal_0_451) 23) (select (m_origin formal_0_451) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_453 () FormalMachine (FormalWriteFromOrigin formal_0_452 12 23))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_453)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_453) (select (m_origin formal_0_453) 8) (select (m_origin formal_0_453) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_453) (select (m_origin formal_0_453) 8) (select (m_origin formal_0_453) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_454 () FormalMachine (FormalCallback formal_0_453 boundary_0 (select (m_origin formal_0_453) 8) (select (m_origin formal_0_453) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_455 () FormalMachine (FormalWriteFromOrigin formal_0_454 12 8))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_455)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_455) (select (m_origin formal_0_455) 9) (select (m_origin formal_0_455) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_455) (select (m_origin formal_0_455) 9) (select (m_origin formal_0_455) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_456 () FormalMachine (FormalCallback formal_0_455 boundary_0 (select (m_origin formal_0_455) 9) (select (m_origin formal_0_455) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_457 () FormalMachine (FormalWriteFromOrigin formal_0_456 12 9))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_457)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_457) (select (m_origin formal_0_457) 29) (select (m_origin formal_0_457) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_457) (select (m_origin formal_0_457) 29) (select (m_origin formal_0_457) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_458 () FormalMachine (FormalCallback formal_0_457 boundary_0 (select (m_origin formal_0_457) 29) (select (m_origin formal_0_457) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_459 () FormalMachine (FormalWriteFromOrigin formal_0_458 12 29))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_459)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_459) (select (m_origin formal_0_459) 31) (select (m_origin formal_0_459) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_459) (select (m_origin formal_0_459) 31) (select (m_origin formal_0_459) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_460 () FormalMachine (FormalCallback formal_0_459 boundary_0 (select (m_origin formal_0_459) 31) (select (m_origin formal_0_459) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_461 () FormalMachine (FormalWriteFromOrigin formal_0_460 12 31))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_461)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_461) (select (m_origin formal_0_461) 38) (select (m_origin formal_0_461) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_461) (select (m_origin formal_0_461) 38) (select (m_origin formal_0_461) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_462 () FormalMachine (FormalCallback formal_0_461 boundary_0 (select (m_origin formal_0_461) 38) (select (m_origin formal_0_461) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_463 () FormalMachine (FormalWriteFromOrigin formal_0_462 12 38))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_463)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_463) (select (m_origin formal_0_463) 47) (select (m_origin formal_0_463) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_463) (select (m_origin formal_0_463) 47) (select (m_origin formal_0_463) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_464 () FormalMachine (FormalCallback formal_0_463 boundary_0 (select (m_origin formal_0_463) 47) (select (m_origin formal_0_463) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_465 () FormalMachine (FormalWriteFromOrigin formal_0_464 12 47))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_465)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_465) (select (m_origin formal_0_465) 14) (select (m_origin formal_0_465) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_465) (select (m_origin formal_0_465) 14) (select (m_origin formal_0_465) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_466 () FormalMachine (FormalCallback formal_0_465 boundary_0 (select (m_origin formal_0_465) 14) (select (m_origin formal_0_465) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_467 () FormalMachine (FormalWriteFromOrigin formal_0_466 12 14))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_467)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_467) (select (m_origin formal_0_467) 15) (select (m_origin formal_0_467) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_467) (select (m_origin formal_0_467) 15) (select (m_origin formal_0_467) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_468 () FormalMachine (FormalCallback formal_0_467 boundary_0 (select (m_origin formal_0_467) 15) (select (m_origin formal_0_467) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_469 () FormalMachine (FormalWriteFromOrigin formal_0_468 13 15))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_470 () FormalMachine (FormalWriteFromOrigin formal_0_469 20 23))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_470)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_470) (select (m_origin formal_0_470) 52) (select (m_origin formal_0_470) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_470) (select (m_origin formal_0_470) 52) (select (m_origin formal_0_470) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_471 () FormalMachine (FormalCallback formal_0_470 boundary_0 (select (m_origin formal_0_470) 52) (select (m_origin formal_0_470) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_472 () FormalMachine (FormalWriteFromOrigin formal_0_471 13 52))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_472)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_472) (select (m_origin formal_0_472) 55) (select (m_origin formal_0_472) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_472) (select (m_origin formal_0_472) 55) (select (m_origin formal_0_472) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_473 () FormalMachine (FormalCallback formal_0_472 boundary_0 (select (m_origin formal_0_472) 55) (select (m_origin formal_0_472) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_474 () FormalMachine (FormalWriteFromOrigin formal_0_473 13 55))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_474)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_474) (select (m_origin formal_0_474) 56) (select (m_origin formal_0_474) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_474) (select (m_origin formal_0_474) 56) (select (m_origin formal_0_474) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_475 () FormalMachine (FormalCallback formal_0_474 boundary_0 (select (m_origin formal_0_474) 56) (select (m_origin formal_0_474) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_476 () FormalMachine (FormalWriteFromOrigin formal_0_475 14 56))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_477 () FormalMachine (FormalWriteFromOrigin formal_0_476 23 8))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_477)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_477) (select (m_origin formal_0_477) 57) (select (m_origin formal_0_477) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_477) (select (m_origin formal_0_477) 57) (select (m_origin formal_0_477) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_478 () FormalMachine (FormalCallback formal_0_477 boundary_0 (select (m_origin formal_0_477) 57) (select (m_origin formal_0_477) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_479 () FormalMachine (FormalWriteFromOrigin formal_0_478 15 57))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_480 () FormalMachine (FormalWriteFromOrigin formal_0_479 24 9))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_480)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_480) (select (m_origin formal_0_480) 1) (select (m_origin formal_0_480) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_480) (select (m_origin formal_0_480) 1) (select (m_origin formal_0_480) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_481 () FormalMachine (FormalCallback formal_0_480 boundary_0 (select (m_origin formal_0_480) 1) (select (m_origin formal_0_480) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_482 () FormalMachine (FormalWriteFromOrigin formal_0_481 16 1))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_483 () FormalMachine (FormalWriteFromOrigin formal_0_482 25 29))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_483)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_483) (select (m_origin formal_0_483) 63) (select (m_origin formal_0_483) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_483) (select (m_origin formal_0_483) 63) (select (m_origin formal_0_483) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_484 () FormalMachine (FormalCallback formal_0_483 boundary_0 (select (m_origin formal_0_483) 63) (select (m_origin formal_0_483) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_485 () FormalMachine (FormalWriteFromOrigin formal_0_484 16 63))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_485)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_485) (select (m_origin formal_0_485) 4) (select (m_origin formal_0_485) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_485) (select (m_origin formal_0_485) 4) (select (m_origin formal_0_485) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_486 () FormalMachine (FormalCallback formal_0_485 boundary_0 (select (m_origin formal_0_485) 4) (select (m_origin formal_0_485) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_487 () FormalMachine (FormalWriteFromOrigin formal_0_486 17 4))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_488 () FormalMachine (FormalWriteFromOrigin formal_0_487 27 31))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_488)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_488) (select (m_origin formal_0_488) 66) (select (m_origin formal_0_488) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_488) (select (m_origin formal_0_488) 66) (select (m_origin formal_0_488) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_489 () FormalMachine (FormalCallback formal_0_488 boundary_0 (select (m_origin formal_0_488) 66) (select (m_origin formal_0_488) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_490 () FormalMachine (FormalWriteFromOrigin formal_0_489 18 66))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_491 () FormalMachine (FormalWriteFromOrigin formal_0_490 28 38))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_491)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_491) (select (m_origin formal_0_491) 70) (select (m_origin formal_0_491) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_491) (select (m_origin formal_0_491) 70) (select (m_origin formal_0_491) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_492 () FormalMachine (FormalCallback formal_0_491 boundary_0 (select (m_origin formal_0_491) 70) (select (m_origin formal_0_491) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_493 () FormalMachine (FormalWriteFromOrigin formal_0_492 18 70))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_493)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_493) (select (m_origin formal_0_493) 17) (select (m_origin formal_0_493) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_493) (select (m_origin formal_0_493) 17) (select (m_origin formal_0_493) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_494 () FormalMachine (FormalCallback formal_0_493 boundary_0 (select (m_origin formal_0_493) 17) (select (m_origin formal_0_493) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_495 () FormalMachine (FormalWriteFromOrigin formal_0_494 18 17))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_495)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_495) (select (m_origin formal_0_495) 21) (select (m_origin formal_0_495) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_495) (select (m_origin formal_0_495) 21) (select (m_origin formal_0_495) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_496 () FormalMachine (FormalCallback formal_0_495 boundary_0 (select (m_origin formal_0_495) 21) (select (m_origin formal_0_495) 20)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_497 () FormalMachine (FormalWriteFromOrigin formal_0_496 19 21))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_498 () FormalMachine (FormalWriteFromOrigin formal_0_497 31 47))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_499 () FormalMachine (FormalSwap formal_0_498 10 19))
; source callback case=recursive-pivot phase=insert-tail[10:19:1]:initial-compare
(assert (not (m_panicked formal_0_499)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_499) (select (m_origin formal_0_499) 22) (select (m_origin formal_0_499) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_499) (select (m_origin formal_0_499) 22) (select (m_origin formal_0_499) 21)) false))
; source callback transition phase=insert-tail[10:19:1]:initial-compare
(define-fun formal_0_500 () FormalMachine (FormalCallback formal_0_499 boundary_0 (select (m_origin formal_0_499) 22) (select (m_origin formal_0_499) 21)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:1]
(define-fun formal_0_501 () FormalMachine (FormalWriteFromOrigin formal_0_500 11 21))
; source write kind=copy-on-drop-restore phase=insert-tail[10:19:1]
(define-fun formal_0_502 () FormalMachine (FormalWriteFromOrigin formal_0_501 10 22))
; source callback case=recursive-pivot phase=insert-tail[10:19:2]:initial-compare
(assert (not (m_panicked formal_0_502)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_502) (select (m_origin formal_0_502) 14) (select (m_origin formal_0_502) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_502) (select (m_origin formal_0_502) 14) (select (m_origin formal_0_502) 21)) false))
; source callback transition phase=insert-tail[10:19:2]:initial-compare
(define-fun formal_0_503 () FormalMachine (FormalCallback formal_0_502 boundary_0 (select (m_origin formal_0_502) 14) (select (m_origin formal_0_502) 21)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:2]
(define-fun formal_0_504 () FormalMachine (FormalWriteFromOrigin formal_0_503 12 21))
; source callback case=recursive-pivot phase=insert-tail[10:19:2]:sift-compare
(assert (not (m_panicked formal_0_504)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_504) (select (m_origin formal_0_504) 14) (select (m_origin formal_0_504) 22)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_504) (select (m_origin formal_0_504) 14) (select (m_origin formal_0_504) 22)) false))
; source callback transition phase=insert-tail[10:19:2]:sift-compare
(define-fun formal_0_505 () FormalMachine (FormalCallback formal_0_504 boundary_0 (select (m_origin formal_0_504) 14) (select (m_origin formal_0_504) 22)))
; source write kind=copy-on-drop-restore phase=insert-tail[10:19:2]
(define-fun formal_0_506 () FormalMachine (FormalWriteFromOrigin formal_0_505 11 14))
; source callback case=recursive-pivot phase=insert-tail[10:19:3]:initial-compare
(assert (not (m_panicked formal_0_506)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_506) (select (m_origin formal_0_506) 55) (select (m_origin formal_0_506) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_506) (select (m_origin formal_0_506) 55) (select (m_origin formal_0_506) 21)) false))
; source callback transition phase=insert-tail[10:19:3]:initial-compare
(define-fun formal_0_507 () FormalMachine (FormalCallback formal_0_506 boundary_0 (select (m_origin formal_0_506) 55) (select (m_origin formal_0_506) 21)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:3]
(define-fun formal_0_508 () FormalMachine (FormalWriteFromOrigin formal_0_507 13 21))
; source callback case=recursive-pivot phase=insert-tail[10:19:3]:sift-compare
(assert (not (m_panicked formal_0_508)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_508) (select (m_origin formal_0_508) 55) (select (m_origin formal_0_508) 14)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_508) (select (m_origin formal_0_508) 55) (select (m_origin formal_0_508) 14)) false))
; source callback transition phase=insert-tail[10:19:3]:sift-compare
(define-fun formal_0_509 () FormalMachine (FormalCallback formal_0_508 boundary_0 (select (m_origin formal_0_508) 55) (select (m_origin formal_0_508) 14)))
; source write kind=copy-on-drop-restore phase=insert-tail[10:19:3]
(define-fun formal_0_510 () FormalMachine (FormalWriteFromOrigin formal_0_509 12 55))
; source callback case=recursive-pivot phase=insert-tail[10:19:4]:initial-compare
(assert (not (m_panicked formal_0_510)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_510) (select (m_origin formal_0_510) 56) (select (m_origin formal_0_510) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_510) (select (m_origin formal_0_510) 56) (select (m_origin formal_0_510) 21)) false))
; source callback transition phase=insert-tail[10:19:4]:initial-compare
(define-fun formal_0_511 () FormalMachine (FormalCallback formal_0_510 boundary_0 (select (m_origin formal_0_510) 56) (select (m_origin formal_0_510) 21)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:4]
(define-fun formal_0_512 () FormalMachine (FormalWriteFromOrigin formal_0_511 14 21))
; source callback case=recursive-pivot phase=insert-tail[10:19:4]:sift-compare
(assert (not (m_panicked formal_0_512)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_512) (select (m_origin formal_0_512) 56) (select (m_origin formal_0_512) 55)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_512) (select (m_origin formal_0_512) 56) (select (m_origin formal_0_512) 55)) false))
; source callback transition phase=insert-tail[10:19:4]:sift-compare
(define-fun formal_0_513 () FormalMachine (FormalCallback formal_0_512 boundary_0 (select (m_origin formal_0_512) 56) (select (m_origin formal_0_512) 55)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:4]
(define-fun formal_0_514 () FormalMachine (FormalWriteFromOrigin formal_0_513 13 55))
; source callback case=recursive-pivot phase=insert-tail[10:19:4]:sift-compare
(assert (not (m_panicked formal_0_514)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_514) (select (m_origin formal_0_514) 56) (select (m_origin formal_0_514) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_514) (select (m_origin formal_0_514) 56) (select (m_origin formal_0_514) 14)) false))
; source callback transition phase=insert-tail[10:19:4]:sift-compare
(define-fun formal_0_515 () FormalMachine (FormalCallback formal_0_514 boundary_0 (select (m_origin formal_0_514) 56) (select (m_origin formal_0_514) 14)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:4]
(define-fun formal_0_516 () FormalMachine (FormalWriteFromOrigin formal_0_515 12 14))
; source callback case=recursive-pivot phase=insert-tail[10:19:4]:sift-compare
(assert (not (m_panicked formal_0_516)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_516) (select (m_origin formal_0_516) 56) (select (m_origin formal_0_516) 22)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_516) (select (m_origin formal_0_516) 56) (select (m_origin formal_0_516) 22)) false))
; source callback transition phase=insert-tail[10:19:4]:sift-compare
(define-fun formal_0_517 () FormalMachine (FormalCallback formal_0_516 boundary_0 (select (m_origin formal_0_516) 56) (select (m_origin formal_0_516) 22)))
; source write kind=copy-on-drop-restore phase=insert-tail[10:19:4]
(define-fun formal_0_518 () FormalMachine (FormalWriteFromOrigin formal_0_517 11 56))
; source callback case=recursive-pivot phase=insert-tail[10:19:5]:initial-compare
(assert (not (m_panicked formal_0_518)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_518) (select (m_origin formal_0_518) 57) (select (m_origin formal_0_518) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_518) (select (m_origin formal_0_518) 57) (select (m_origin formal_0_518) 21)) false))
; source callback transition phase=insert-tail[10:19:5]:initial-compare
(define-fun formal_0_519 () FormalMachine (FormalCallback formal_0_518 boundary_0 (select (m_origin formal_0_518) 57) (select (m_origin formal_0_518) 21)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:5]
(define-fun formal_0_520 () FormalMachine (FormalWriteFromOrigin formal_0_519 15 21))
; source callback case=recursive-pivot phase=insert-tail[10:19:5]:sift-compare
(assert (not (m_panicked formal_0_520)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_520) (select (m_origin formal_0_520) 57) (select (m_origin formal_0_520) 55)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_520) (select (m_origin formal_0_520) 57) (select (m_origin formal_0_520) 55)) false))
; source callback transition phase=insert-tail[10:19:5]:sift-compare
(define-fun formal_0_521 () FormalMachine (FormalCallback formal_0_520 boundary_0 (select (m_origin formal_0_520) 57) (select (m_origin formal_0_520) 55)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:5]
(define-fun formal_0_522 () FormalMachine (FormalWriteFromOrigin formal_0_521 14 55))
; source callback case=recursive-pivot phase=insert-tail[10:19:5]:sift-compare
(assert (not (m_panicked formal_0_522)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_522) (select (m_origin formal_0_522) 57) (select (m_origin formal_0_522) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_522) (select (m_origin formal_0_522) 57) (select (m_origin formal_0_522) 14)) false))
; source callback transition phase=insert-tail[10:19:5]:sift-compare
(define-fun formal_0_523 () FormalMachine (FormalCallback formal_0_522 boundary_0 (select (m_origin formal_0_522) 57) (select (m_origin formal_0_522) 14)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:5]
(define-fun formal_0_524 () FormalMachine (FormalWriteFromOrigin formal_0_523 13 14))
; source callback case=recursive-pivot phase=insert-tail[10:19:5]:sift-compare
(assert (not (m_panicked formal_0_524)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_524) (select (m_origin formal_0_524) 57) (select (m_origin formal_0_524) 56)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_524) (select (m_origin formal_0_524) 57) (select (m_origin formal_0_524) 56)) false))
; source callback transition phase=insert-tail[10:19:5]:sift-compare
(define-fun formal_0_525 () FormalMachine (FormalCallback formal_0_524 boundary_0 (select (m_origin formal_0_524) 57) (select (m_origin formal_0_524) 56)))
; source write kind=copy-on-drop-restore phase=insert-tail[10:19:5]
(define-fun formal_0_526 () FormalMachine (FormalWriteFromOrigin formal_0_525 12 57))
; source callback case=recursive-pivot phase=insert-tail[10:19:6]:initial-compare
(assert (not (m_panicked formal_0_526)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_526) (select (m_origin formal_0_526) 63) (select (m_origin formal_0_526) 21)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_526) (select (m_origin formal_0_526) 63) (select (m_origin formal_0_526) 21)) false))
; source callback transition phase=insert-tail[10:19:6]:initial-compare
(define-fun formal_0_527 () FormalMachine (FormalCallback formal_0_526 boundary_0 (select (m_origin formal_0_526) 63) (select (m_origin formal_0_526) 21)))
; source callback case=recursive-pivot phase=insert-tail[10:19:7]:initial-compare
(assert (not (m_panicked formal_0_527)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_527) (select (m_origin formal_0_527) 4) (select (m_origin formal_0_527) 63)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_527) (select (m_origin formal_0_527) 4) (select (m_origin formal_0_527) 63)) false))
; source callback transition phase=insert-tail[10:19:7]:initial-compare
(define-fun formal_0_528 () FormalMachine (FormalCallback formal_0_527 boundary_0 (select (m_origin formal_0_527) 4) (select (m_origin formal_0_527) 63)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:7]
(define-fun formal_0_529 () FormalMachine (FormalWriteFromOrigin formal_0_528 17 63))
; source callback case=recursive-pivot phase=insert-tail[10:19:7]:sift-compare
(assert (not (m_panicked formal_0_529)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_529) (select (m_origin formal_0_529) 4) (select (m_origin formal_0_529) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_529) (select (m_origin formal_0_529) 4) (select (m_origin formal_0_529) 21)) false))
; source callback transition phase=insert-tail[10:19:7]:sift-compare
(define-fun formal_0_530 () FormalMachine (FormalCallback formal_0_529 boundary_0 (select (m_origin formal_0_529) 4) (select (m_origin formal_0_529) 21)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:7]
(define-fun formal_0_531 () FormalMachine (FormalWriteFromOrigin formal_0_530 16 21))
; source callback case=recursive-pivot phase=insert-tail[10:19:7]:sift-compare
(assert (not (m_panicked formal_0_531)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_531) (select (m_origin formal_0_531) 4) (select (m_origin formal_0_531) 55)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_531) (select (m_origin formal_0_531) 4) (select (m_origin formal_0_531) 55)) false))
; source callback transition phase=insert-tail[10:19:7]:sift-compare
(define-fun formal_0_532 () FormalMachine (FormalCallback formal_0_531 boundary_0 (select (m_origin formal_0_531) 4) (select (m_origin formal_0_531) 55)))
; source write kind=copy-on-drop-restore phase=insert-tail[10:19:7]
(define-fun formal_0_533 () FormalMachine (FormalWriteFromOrigin formal_0_532 15 4))
; source callback case=recursive-pivot phase=insert-tail[10:19:8]:initial-compare
(assert (not (m_panicked formal_0_533)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_533) (select (m_origin formal_0_533) 17) (select (m_origin formal_0_533) 63)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_533) (select (m_origin formal_0_533) 17) (select (m_origin formal_0_533) 63)) false))
; source callback transition phase=insert-tail[10:19:8]:initial-compare
(define-fun formal_0_534 () FormalMachine (FormalCallback formal_0_533 boundary_0 (select (m_origin formal_0_533) 17) (select (m_origin formal_0_533) 63)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:8]
(define-fun formal_0_535 () FormalMachine (FormalWriteFromOrigin formal_0_534 18 63))
; source callback case=recursive-pivot phase=insert-tail[10:19:8]:sift-compare
(assert (not (m_panicked formal_0_535)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_535) (select (m_origin formal_0_535) 17) (select (m_origin formal_0_535) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_535) (select (m_origin formal_0_535) 17) (select (m_origin formal_0_535) 21)) false))
; source callback transition phase=insert-tail[10:19:8]:sift-compare
(define-fun formal_0_536 () FormalMachine (FormalCallback formal_0_535 boundary_0 (select (m_origin formal_0_535) 17) (select (m_origin formal_0_535) 21)))
; source write kind=insert-tail-shift phase=insert-tail[10:19:8]
(define-fun formal_0_537 () FormalMachine (FormalWriteFromOrigin formal_0_536 17 21))
; source callback case=recursive-pivot phase=insert-tail[10:19:8]:sift-compare
(assert (not (m_panicked formal_0_537)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_537) (select (m_origin formal_0_537) 17) (select (m_origin formal_0_537) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_537) (select (m_origin formal_0_537) 17) (select (m_origin formal_0_537) 4)) false))
; source callback transition phase=insert-tail[10:19:8]:sift-compare
(define-fun formal_0_538 () FormalMachine (FormalCallback formal_0_537 boundary_0 (select (m_origin formal_0_537) 17) (select (m_origin formal_0_537) 4)))
; source write kind=copy-on-drop-restore phase=insert-tail[10:19:8]
(define-fun formal_0_539 () FormalMachine (FormalWriteFromOrigin formal_0_538 16 17))
; source callback case=recursive-pivot phase=insert-tail[20:32:1]:initial-compare
(assert (not (m_panicked formal_0_539)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_539) (select (m_origin formal_0_539) 15) (select (m_origin formal_0_539) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_539) (select (m_origin formal_0_539) 15) (select (m_origin formal_0_539) 23)) false))
; source callback transition phase=insert-tail[20:32:1]:initial-compare
(define-fun formal_0_540 () FormalMachine (FormalCallback formal_0_539 boundary_0 (select (m_origin formal_0_539) 15) (select (m_origin formal_0_539) 23)))
; source callback case=recursive-pivot phase=insert-tail[20:32:2]:initial-compare
(assert (not (m_panicked formal_0_540)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_540) (select (m_origin formal_0_540) 52) (select (m_origin formal_0_540) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_540) (select (m_origin formal_0_540) 52) (select (m_origin formal_0_540) 15)) false))
; source callback transition phase=insert-tail[20:32:2]:initial-compare
(define-fun formal_0_541 () FormalMachine (FormalCallback formal_0_540 boundary_0 (select (m_origin formal_0_540) 52) (select (m_origin formal_0_540) 15)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:2]
(define-fun formal_0_542 () FormalMachine (FormalWriteFromOrigin formal_0_541 22 15))
; source callback case=recursive-pivot phase=insert-tail[20:32:2]:sift-compare
(assert (not (m_panicked formal_0_542)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_542) (select (m_origin formal_0_542) 52) (select (m_origin formal_0_542) 23)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_542) (select (m_origin formal_0_542) 52) (select (m_origin formal_0_542) 23)) false))
; source callback transition phase=insert-tail[20:32:2]:sift-compare
(define-fun formal_0_543 () FormalMachine (FormalCallback formal_0_542 boundary_0 (select (m_origin formal_0_542) 52) (select (m_origin formal_0_542) 23)))
; source write kind=copy-on-drop-restore phase=insert-tail[20:32:2]
(define-fun formal_0_544 () FormalMachine (FormalWriteFromOrigin formal_0_543 21 52))
; source callback case=recursive-pivot phase=insert-tail[20:32:3]:initial-compare
(assert (not (m_panicked formal_0_544)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_544) (select (m_origin formal_0_544) 8) (select (m_origin formal_0_544) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_544) (select (m_origin formal_0_544) 8) (select (m_origin formal_0_544) 15)) false))
; source callback transition phase=insert-tail[20:32:3]:initial-compare
(define-fun formal_0_545 () FormalMachine (FormalCallback formal_0_544 boundary_0 (select (m_origin formal_0_544) 8) (select (m_origin formal_0_544) 15)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:3]
(define-fun formal_0_546 () FormalMachine (FormalWriteFromOrigin formal_0_545 23 15))
; source callback case=recursive-pivot phase=insert-tail[20:32:3]:sift-compare
(assert (not (m_panicked formal_0_546)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_546) (select (m_origin formal_0_546) 8) (select (m_origin formal_0_546) 52)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_546) (select (m_origin formal_0_546) 8) (select (m_origin formal_0_546) 52)) false))
; source callback transition phase=insert-tail[20:32:3]:sift-compare
(define-fun formal_0_547 () FormalMachine (FormalCallback formal_0_546 boundary_0 (select (m_origin formal_0_546) 8) (select (m_origin formal_0_546) 52)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:3]
(define-fun formal_0_548 () FormalMachine (FormalWriteFromOrigin formal_0_547 22 52))
; source callback case=recursive-pivot phase=insert-tail[20:32:3]:sift-compare
(assert (not (m_panicked formal_0_548)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_548) (select (m_origin formal_0_548) 8) (select (m_origin formal_0_548) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_548) (select (m_origin formal_0_548) 8) (select (m_origin formal_0_548) 23)) false))
; source callback transition phase=insert-tail[20:32:3]:sift-compare
(define-fun formal_0_549 () FormalMachine (FormalCallback formal_0_548 boundary_0 (select (m_origin formal_0_548) 8) (select (m_origin formal_0_548) 23)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:3]
(define-fun formal_0_550 () FormalMachine (FormalWriteFromOrigin formal_0_549 21 23))
; source write kind=copy-on-drop-restore phase=insert-tail[20:32:3]
(define-fun formal_0_551 () FormalMachine (FormalWriteFromOrigin formal_0_550 20 8))
; source callback case=recursive-pivot phase=insert-tail[20:32:4]:initial-compare
(assert (not (m_panicked formal_0_551)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_551) (select (m_origin formal_0_551) 9) (select (m_origin formal_0_551) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_551) (select (m_origin formal_0_551) 9) (select (m_origin formal_0_551) 15)) false))
; source callback transition phase=insert-tail[20:32:4]:initial-compare
(define-fun formal_0_552 () FormalMachine (FormalCallback formal_0_551 boundary_0 (select (m_origin formal_0_551) 9) (select (m_origin formal_0_551) 15)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:4]
(define-fun formal_0_553 () FormalMachine (FormalWriteFromOrigin formal_0_552 24 15))
; source callback case=recursive-pivot phase=insert-tail[20:32:4]:sift-compare
(assert (not (m_panicked formal_0_553)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_553) (select (m_origin formal_0_553) 9) (select (m_origin formal_0_553) 52)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_553) (select (m_origin formal_0_553) 9) (select (m_origin formal_0_553) 52)) false))
; source callback transition phase=insert-tail[20:32:4]:sift-compare
(define-fun formal_0_554 () FormalMachine (FormalCallback formal_0_553 boundary_0 (select (m_origin formal_0_553) 9) (select (m_origin formal_0_553) 52)))
; source write kind=copy-on-drop-restore phase=insert-tail[20:32:4]
(define-fun formal_0_555 () FormalMachine (FormalWriteFromOrigin formal_0_554 23 9))
; source callback case=recursive-pivot phase=insert-tail[20:32:5]:initial-compare
(assert (not (m_panicked formal_0_555)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_555) (select (m_origin formal_0_555) 29) (select (m_origin formal_0_555) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_555) (select (m_origin formal_0_555) 29) (select (m_origin formal_0_555) 15)) false))
; source callback transition phase=insert-tail[20:32:5]:initial-compare
(define-fun formal_0_556 () FormalMachine (FormalCallback formal_0_555 boundary_0 (select (m_origin formal_0_555) 29) (select (m_origin formal_0_555) 15)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:5]
(define-fun formal_0_557 () FormalMachine (FormalWriteFromOrigin formal_0_556 25 15))
; source callback case=recursive-pivot phase=insert-tail[20:32:5]:sift-compare
(assert (not (m_panicked formal_0_557)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_557) (select (m_origin formal_0_557) 29) (select (m_origin formal_0_557) 9)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_557) (select (m_origin formal_0_557) 29) (select (m_origin formal_0_557) 9)) false))
; source callback transition phase=insert-tail[20:32:5]:sift-compare
(define-fun formal_0_558 () FormalMachine (FormalCallback formal_0_557 boundary_0 (select (m_origin formal_0_557) 29) (select (m_origin formal_0_557) 9)))
; source write kind=copy-on-drop-restore phase=insert-tail[20:32:5]
(define-fun formal_0_559 () FormalMachine (FormalWriteFromOrigin formal_0_558 24 29))
; source callback case=recursive-pivot phase=insert-tail[20:32:6]:initial-compare
(assert (not (m_panicked formal_0_559)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_559) (select (m_origin formal_0_559) 1) (select (m_origin formal_0_559) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_559) (select (m_origin formal_0_559) 1) (select (m_origin formal_0_559) 15)) false))
; source callback transition phase=insert-tail[20:32:6]:initial-compare
(define-fun formal_0_560 () FormalMachine (FormalCallback formal_0_559 boundary_0 (select (m_origin formal_0_559) 1) (select (m_origin formal_0_559) 15)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:6]
(define-fun formal_0_561 () FormalMachine (FormalWriteFromOrigin formal_0_560 26 15))
; source callback case=recursive-pivot phase=insert-tail[20:32:6]:sift-compare
(assert (not (m_panicked formal_0_561)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_561) (select (m_origin formal_0_561) 1) (select (m_origin formal_0_561) 29)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_561) (select (m_origin formal_0_561) 1) (select (m_origin formal_0_561) 29)) false))
; source callback transition phase=insert-tail[20:32:6]:sift-compare
(define-fun formal_0_562 () FormalMachine (FormalCallback formal_0_561 boundary_0 (select (m_origin formal_0_561) 1) (select (m_origin formal_0_561) 29)))
; source write kind=copy-on-drop-restore phase=insert-tail[20:32:6]
(define-fun formal_0_563 () FormalMachine (FormalWriteFromOrigin formal_0_562 25 1))
; source callback case=recursive-pivot phase=insert-tail[20:32:7]:initial-compare
(assert (not (m_panicked formal_0_563)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_563) (select (m_origin formal_0_563) 31) (select (m_origin formal_0_563) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_563) (select (m_origin formal_0_563) 31) (select (m_origin formal_0_563) 15)) false))
; source callback transition phase=insert-tail[20:32:7]:initial-compare
(define-fun formal_0_564 () FormalMachine (FormalCallback formal_0_563 boundary_0 (select (m_origin formal_0_563) 31) (select (m_origin formal_0_563) 15)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:7]
(define-fun formal_0_565 () FormalMachine (FormalWriteFromOrigin formal_0_564 27 15))
; source callback case=recursive-pivot phase=insert-tail[20:32:7]:sift-compare
(assert (not (m_panicked formal_0_565)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_565) (select (m_origin formal_0_565) 31) (select (m_origin formal_0_565) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_565) (select (m_origin formal_0_565) 31) (select (m_origin formal_0_565) 1)) false))
; source callback transition phase=insert-tail[20:32:7]:sift-compare
(define-fun formal_0_566 () FormalMachine (FormalCallback formal_0_565 boundary_0 (select (m_origin formal_0_565) 31) (select (m_origin formal_0_565) 1)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:7]
(define-fun formal_0_567 () FormalMachine (FormalWriteFromOrigin formal_0_566 26 1))
; source callback case=recursive-pivot phase=insert-tail[20:32:7]:sift-compare
(assert (not (m_panicked formal_0_567)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_567) (select (m_origin formal_0_567) 31) (select (m_origin formal_0_567) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_567) (select (m_origin formal_0_567) 31) (select (m_origin formal_0_567) 29)) false))
; source callback transition phase=insert-tail[20:32:7]:sift-compare
(define-fun formal_0_568 () FormalMachine (FormalCallback formal_0_567 boundary_0 (select (m_origin formal_0_567) 31) (select (m_origin formal_0_567) 29)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:7]
(define-fun formal_0_569 () FormalMachine (FormalWriteFromOrigin formal_0_568 25 29))
; source callback case=recursive-pivot phase=insert-tail[20:32:7]:sift-compare
(assert (not (m_panicked formal_0_569)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_569) (select (m_origin formal_0_569) 31) (select (m_origin formal_0_569) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_569) (select (m_origin formal_0_569) 31) (select (m_origin formal_0_569) 9)) false))
; source callback transition phase=insert-tail[20:32:7]:sift-compare
(define-fun formal_0_570 () FormalMachine (FormalCallback formal_0_569 boundary_0 (select (m_origin formal_0_569) 31) (select (m_origin formal_0_569) 9)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:7]
(define-fun formal_0_571 () FormalMachine (FormalWriteFromOrigin formal_0_570 24 9))
; source callback case=recursive-pivot phase=insert-tail[20:32:7]:sift-compare
(assert (not (m_panicked formal_0_571)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_571) (select (m_origin formal_0_571) 31) (select (m_origin formal_0_571) 52)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_571) (select (m_origin formal_0_571) 31) (select (m_origin formal_0_571) 52)) false))
; source callback transition phase=insert-tail[20:32:7]:sift-compare
(define-fun formal_0_572 () FormalMachine (FormalCallback formal_0_571 boundary_0 (select (m_origin formal_0_571) 31) (select (m_origin formal_0_571) 52)))
; source write kind=copy-on-drop-restore phase=insert-tail[20:32:7]
(define-fun formal_0_573 () FormalMachine (FormalWriteFromOrigin formal_0_572 23 31))
; source callback case=recursive-pivot phase=insert-tail[20:32:8]:initial-compare
(assert (not (m_panicked formal_0_573)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_573) (select (m_origin formal_0_573) 38) (select (m_origin formal_0_573) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_573) (select (m_origin formal_0_573) 38) (select (m_origin formal_0_573) 15)) false))
; source callback transition phase=insert-tail[20:32:8]:initial-compare
(define-fun formal_0_574 () FormalMachine (FormalCallback formal_0_573 boundary_0 (select (m_origin formal_0_573) 38) (select (m_origin formal_0_573) 15)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:8]
(define-fun formal_0_575 () FormalMachine (FormalWriteFromOrigin formal_0_574 28 15))
; source callback case=recursive-pivot phase=insert-tail[20:32:8]:sift-compare
(assert (not (m_panicked formal_0_575)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_575) (select (m_origin formal_0_575) 38) (select (m_origin formal_0_575) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_575) (select (m_origin formal_0_575) 38) (select (m_origin formal_0_575) 1)) false))
; source callback transition phase=insert-tail[20:32:8]:sift-compare
(define-fun formal_0_576 () FormalMachine (FormalCallback formal_0_575 boundary_0 (select (m_origin formal_0_575) 38) (select (m_origin formal_0_575) 1)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:8]
(define-fun formal_0_577 () FormalMachine (FormalWriteFromOrigin formal_0_576 27 1))
; source callback case=recursive-pivot phase=insert-tail[20:32:8]:sift-compare
(assert (not (m_panicked formal_0_577)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_577) (select (m_origin formal_0_577) 38) (select (m_origin formal_0_577) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_577) (select (m_origin formal_0_577) 38) (select (m_origin formal_0_577) 29)) false))
; source callback transition phase=insert-tail[20:32:8]:sift-compare
(define-fun formal_0_578 () FormalMachine (FormalCallback formal_0_577 boundary_0 (select (m_origin formal_0_577) 38) (select (m_origin formal_0_577) 29)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:8]
(define-fun formal_0_579 () FormalMachine (FormalWriteFromOrigin formal_0_578 26 29))
; source callback case=recursive-pivot phase=insert-tail[20:32:8]:sift-compare
(assert (not (m_panicked formal_0_579)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_579) (select (m_origin formal_0_579) 38) (select (m_origin formal_0_579) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_579) (select (m_origin formal_0_579) 38) (select (m_origin formal_0_579) 9)) false))
; source callback transition phase=insert-tail[20:32:8]:sift-compare
(define-fun formal_0_580 () FormalMachine (FormalCallback formal_0_579 boundary_0 (select (m_origin formal_0_579) 38) (select (m_origin formal_0_579) 9)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:8]
(define-fun formal_0_581 () FormalMachine (FormalWriteFromOrigin formal_0_580 25 9))
; source callback case=recursive-pivot phase=insert-tail[20:32:8]:sift-compare
(assert (not (m_panicked formal_0_581)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_581) (select (m_origin formal_0_581) 38) (select (m_origin formal_0_581) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_581) (select (m_origin formal_0_581) 38) (select (m_origin formal_0_581) 31)) false))
; source callback transition phase=insert-tail[20:32:8]:sift-compare
(define-fun formal_0_582 () FormalMachine (FormalCallback formal_0_581 boundary_0 (select (m_origin formal_0_581) 38) (select (m_origin formal_0_581) 31)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:8]
(define-fun formal_0_583 () FormalMachine (FormalWriteFromOrigin formal_0_582 24 31))
; source callback case=recursive-pivot phase=insert-tail[20:32:8]:sift-compare
(assert (not (m_panicked formal_0_583)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_583) (select (m_origin formal_0_583) 38) (select (m_origin formal_0_583) 52)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_583) (select (m_origin formal_0_583) 38) (select (m_origin formal_0_583) 52)) false))
; source callback transition phase=insert-tail[20:32:8]:sift-compare
(define-fun formal_0_584 () FormalMachine (FormalCallback formal_0_583 boundary_0 (select (m_origin formal_0_583) 38) (select (m_origin formal_0_583) 52)))
; source write kind=copy-on-drop-restore phase=insert-tail[20:32:8]
(define-fun formal_0_585 () FormalMachine (FormalWriteFromOrigin formal_0_584 23 38))
; source callback case=recursive-pivot phase=insert-tail[20:32:9]:initial-compare
(assert (not (m_panicked formal_0_585)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_585) (select (m_origin formal_0_585) 66) (select (m_origin formal_0_585) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_585) (select (m_origin formal_0_585) 66) (select (m_origin formal_0_585) 15)) false))
; source callback transition phase=insert-tail[20:32:9]:initial-compare
(define-fun formal_0_586 () FormalMachine (FormalCallback formal_0_585 boundary_0 (select (m_origin formal_0_585) 66) (select (m_origin formal_0_585) 15)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:9]
(define-fun formal_0_587 () FormalMachine (FormalWriteFromOrigin formal_0_586 29 15))
; source callback case=recursive-pivot phase=insert-tail[20:32:9]:sift-compare
(assert (not (m_panicked formal_0_587)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_587) (select (m_origin formal_0_587) 66) (select (m_origin formal_0_587) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_587) (select (m_origin formal_0_587) 66) (select (m_origin formal_0_587) 1)) false))
; source callback transition phase=insert-tail[20:32:9]:sift-compare
(define-fun formal_0_588 () FormalMachine (FormalCallback formal_0_587 boundary_0 (select (m_origin formal_0_587) 66) (select (m_origin formal_0_587) 1)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:9]
(define-fun formal_0_589 () FormalMachine (FormalWriteFromOrigin formal_0_588 28 1))
; source callback case=recursive-pivot phase=insert-tail[20:32:9]:sift-compare
(assert (not (m_panicked formal_0_589)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_589) (select (m_origin formal_0_589) 66) (select (m_origin formal_0_589) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_589) (select (m_origin formal_0_589) 66) (select (m_origin formal_0_589) 29)) false))
; source callback transition phase=insert-tail[20:32:9]:sift-compare
(define-fun formal_0_590 () FormalMachine (FormalCallback formal_0_589 boundary_0 (select (m_origin formal_0_589) 66) (select (m_origin formal_0_589) 29)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:9]
(define-fun formal_0_591 () FormalMachine (FormalWriteFromOrigin formal_0_590 27 29))
; source callback case=recursive-pivot phase=insert-tail[20:32:9]:sift-compare
(assert (not (m_panicked formal_0_591)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_591) (select (m_origin formal_0_591) 66) (select (m_origin formal_0_591) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_591) (select (m_origin formal_0_591) 66) (select (m_origin formal_0_591) 9)) false))
; source callback transition phase=insert-tail[20:32:9]:sift-compare
(define-fun formal_0_592 () FormalMachine (FormalCallback formal_0_591 boundary_0 (select (m_origin formal_0_591) 66) (select (m_origin formal_0_591) 9)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:9]
(define-fun formal_0_593 () FormalMachine (FormalWriteFromOrigin formal_0_592 26 9))
; source callback case=recursive-pivot phase=insert-tail[20:32:9]:sift-compare
(assert (not (m_panicked formal_0_593)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_593) (select (m_origin formal_0_593) 66) (select (m_origin formal_0_593) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_593) (select (m_origin formal_0_593) 66) (select (m_origin formal_0_593) 31)) false))
; source callback transition phase=insert-tail[20:32:9]:sift-compare
(define-fun formal_0_594 () FormalMachine (FormalCallback formal_0_593 boundary_0 (select (m_origin formal_0_593) 66) (select (m_origin formal_0_593) 31)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:9]
(define-fun formal_0_595 () FormalMachine (FormalWriteFromOrigin formal_0_594 25 31))
; source callback case=recursive-pivot phase=insert-tail[20:32:9]:sift-compare
(assert (not (m_panicked formal_0_595)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_595) (select (m_origin formal_0_595) 66) (select (m_origin formal_0_595) 38)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_595) (select (m_origin formal_0_595) 66) (select (m_origin formal_0_595) 38)) false))
; source callback transition phase=insert-tail[20:32:9]:sift-compare
(define-fun formal_0_596 () FormalMachine (FormalCallback formal_0_595 boundary_0 (select (m_origin formal_0_595) 66) (select (m_origin formal_0_595) 38)))
; source write kind=copy-on-drop-restore phase=insert-tail[20:32:9]
(define-fun formal_0_597 () FormalMachine (FormalWriteFromOrigin formal_0_596 24 66))
; source callback case=recursive-pivot phase=insert-tail[20:32:10]:initial-compare
(assert (not (m_panicked formal_0_597)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_597) (select (m_origin formal_0_597) 70) (select (m_origin formal_0_597) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_597) (select (m_origin formal_0_597) 70) (select (m_origin formal_0_597) 15)) false))
; source callback transition phase=insert-tail[20:32:10]:initial-compare
(define-fun formal_0_598 () FormalMachine (FormalCallback formal_0_597 boundary_0 (select (m_origin formal_0_597) 70) (select (m_origin formal_0_597) 15)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:10]
(define-fun formal_0_599 () FormalMachine (FormalWriteFromOrigin formal_0_598 30 15))
; source callback case=recursive-pivot phase=insert-tail[20:32:10]:sift-compare
(assert (not (m_panicked formal_0_599)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_599) (select (m_origin formal_0_599) 70) (select (m_origin formal_0_599) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_599) (select (m_origin formal_0_599) 70) (select (m_origin formal_0_599) 1)) false))
; source callback transition phase=insert-tail[20:32:10]:sift-compare
(define-fun formal_0_600 () FormalMachine (FormalCallback formal_0_599 boundary_0 (select (m_origin formal_0_599) 70) (select (m_origin formal_0_599) 1)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:10]
(define-fun formal_0_601 () FormalMachine (FormalWriteFromOrigin formal_0_600 29 1))
; source callback case=recursive-pivot phase=insert-tail[20:32:10]:sift-compare
(assert (not (m_panicked formal_0_601)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_601) (select (m_origin formal_0_601) 70) (select (m_origin formal_0_601) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_601) (select (m_origin formal_0_601) 70) (select (m_origin formal_0_601) 29)) false))
; source callback transition phase=insert-tail[20:32:10]:sift-compare
(define-fun formal_0_602 () FormalMachine (FormalCallback formal_0_601 boundary_0 (select (m_origin formal_0_601) 70) (select (m_origin formal_0_601) 29)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:10]
(define-fun formal_0_603 () FormalMachine (FormalWriteFromOrigin formal_0_602 28 29))
; source callback case=recursive-pivot phase=insert-tail[20:32:10]:sift-compare
(assert (not (m_panicked formal_0_603)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_603) (select (m_origin formal_0_603) 70) (select (m_origin formal_0_603) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_603) (select (m_origin formal_0_603) 70) (select (m_origin formal_0_603) 9)) false))
; source callback transition phase=insert-tail[20:32:10]:sift-compare
(define-fun formal_0_604 () FormalMachine (FormalCallback formal_0_603 boundary_0 (select (m_origin formal_0_603) 70) (select (m_origin formal_0_603) 9)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:10]
(define-fun formal_0_605 () FormalMachine (FormalWriteFromOrigin formal_0_604 27 9))
; source callback case=recursive-pivot phase=insert-tail[20:32:10]:sift-compare
(assert (not (m_panicked formal_0_605)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_605) (select (m_origin formal_0_605) 70) (select (m_origin formal_0_605) 31)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_605) (select (m_origin formal_0_605) 70) (select (m_origin formal_0_605) 31)) false))
; source callback transition phase=insert-tail[20:32:10]:sift-compare
(define-fun formal_0_606 () FormalMachine (FormalCallback formal_0_605 boundary_0 (select (m_origin formal_0_605) 70) (select (m_origin formal_0_605) 31)))
; source write kind=copy-on-drop-restore phase=insert-tail[20:32:10]
(define-fun formal_0_607 () FormalMachine (FormalWriteFromOrigin formal_0_606 26 70))
; source callback case=recursive-pivot phase=insert-tail[20:32:11]:initial-compare
(assert (not (m_panicked formal_0_607)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_607) (select (m_origin formal_0_607) 47) (select (m_origin formal_0_607) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_607) (select (m_origin formal_0_607) 47) (select (m_origin formal_0_607) 15)) false))
; source callback transition phase=insert-tail[20:32:11]:initial-compare
(define-fun formal_0_608 () FormalMachine (FormalCallback formal_0_607 boundary_0 (select (m_origin formal_0_607) 47) (select (m_origin formal_0_607) 15)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:11]
(define-fun formal_0_609 () FormalMachine (FormalWriteFromOrigin formal_0_608 31 15))
; source callback case=recursive-pivot phase=insert-tail[20:32:11]:sift-compare
(assert (not (m_panicked formal_0_609)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_609) (select (m_origin formal_0_609) 47) (select (m_origin formal_0_609) 1)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_609) (select (m_origin formal_0_609) 47) (select (m_origin formal_0_609) 1)) false))
; source callback transition phase=insert-tail[20:32:11]:sift-compare
(define-fun formal_0_610 () FormalMachine (FormalCallback formal_0_609 boundary_0 (select (m_origin formal_0_609) 47) (select (m_origin formal_0_609) 1)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:11]
(define-fun formal_0_611 () FormalMachine (FormalWriteFromOrigin formal_0_610 30 1))
; source callback case=recursive-pivot phase=insert-tail[20:32:11]:sift-compare
(assert (not (m_panicked formal_0_611)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_611) (select (m_origin formal_0_611) 47) (select (m_origin formal_0_611) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_611) (select (m_origin formal_0_611) 47) (select (m_origin formal_0_611) 29)) false))
; source callback transition phase=insert-tail[20:32:11]:sift-compare
(define-fun formal_0_612 () FormalMachine (FormalCallback formal_0_611 boundary_0 (select (m_origin formal_0_611) 47) (select (m_origin formal_0_611) 29)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:11]
(define-fun formal_0_613 () FormalMachine (FormalWriteFromOrigin formal_0_612 29 29))
; source callback case=recursive-pivot phase=insert-tail[20:32:11]:sift-compare
(assert (not (m_panicked formal_0_613)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_613) (select (m_origin formal_0_613) 47) (select (m_origin formal_0_613) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_613) (select (m_origin formal_0_613) 47) (select (m_origin formal_0_613) 9)) false))
; source callback transition phase=insert-tail[20:32:11]:sift-compare
(define-fun formal_0_614 () FormalMachine (FormalCallback formal_0_613 boundary_0 (select (m_origin formal_0_613) 47) (select (m_origin formal_0_613) 9)))
; source write kind=insert-tail-shift phase=insert-tail[20:32:11]
(define-fun formal_0_615 () FormalMachine (FormalWriteFromOrigin formal_0_614 28 9))
; source callback case=recursive-pivot phase=insert-tail[20:32:11]:sift-compare
(assert (not (m_panicked formal_0_615)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_615) (select (m_origin formal_0_615) 47) (select (m_origin formal_0_615) 70)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_615) (select (m_origin formal_0_615) 47) (select (m_origin formal_0_615) 70)) false))
; source callback transition phase=insert-tail[20:32:11]:sift-compare
(define-fun formal_0_616 () FormalMachine (FormalCallback formal_0_615 boundary_0 (select (m_origin formal_0_615) 47) (select (m_origin formal_0_615) 70)))
; source write kind=copy-on-drop-restore phase=insert-tail[20:32:11]
(define-fun formal_0_617 () FormalMachine (FormalWriteFromOrigin formal_0_616 27 47))
; source callback case=recursive-pivot phase=insert-tail[33:44:1]:initial-compare
(assert (not (m_panicked formal_0_617)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_617) (select (m_origin formal_0_617) 41) (select (m_origin formal_0_617) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_617) (select (m_origin formal_0_617) 41) (select (m_origin formal_0_617) 40)) false))
; source callback transition phase=insert-tail[33:44:1]:initial-compare
(define-fun formal_0_618 () FormalMachine (FormalCallback formal_0_617 boundary_0 (select (m_origin formal_0_617) 41) (select (m_origin formal_0_617) 40)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:1]
(define-fun formal_0_619 () FormalMachine (FormalWriteFromOrigin formal_0_618 34 40))
; source write kind=copy-on-drop-restore phase=insert-tail[33:44:1]
(define-fun formal_0_620 () FormalMachine (FormalWriteFromOrigin formal_0_619 33 41))
; source callback case=recursive-pivot phase=insert-tail[33:44:2]:initial-compare
(assert (not (m_panicked formal_0_620)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_620) (select (m_origin formal_0_620) 44) (select (m_origin formal_0_620) 40)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_620) (select (m_origin formal_0_620) 44) (select (m_origin formal_0_620) 40)) false))
; source callback transition phase=insert-tail[33:44:2]:initial-compare
(define-fun formal_0_621 () FormalMachine (FormalCallback formal_0_620 boundary_0 (select (m_origin formal_0_620) 44) (select (m_origin formal_0_620) 40)))
; source callback case=recursive-pivot phase=insert-tail[33:44:3]:initial-compare
(assert (not (m_panicked formal_0_621)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_621) (select (m_origin formal_0_621) 62) (select (m_origin formal_0_621) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_621) (select (m_origin formal_0_621) 62) (select (m_origin formal_0_621) 44)) false))
; source callback transition phase=insert-tail[33:44:3]:initial-compare
(define-fun formal_0_622 () FormalMachine (FormalCallback formal_0_621 boundary_0 (select (m_origin formal_0_621) 62) (select (m_origin formal_0_621) 44)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:3]
(define-fun formal_0_623 () FormalMachine (FormalWriteFromOrigin formal_0_622 36 44))
; source callback case=recursive-pivot phase=insert-tail[33:44:3]:sift-compare
(assert (not (m_panicked formal_0_623)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_623) (select (m_origin formal_0_623) 62) (select (m_origin formal_0_623) 40)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_623) (select (m_origin formal_0_623) 62) (select (m_origin formal_0_623) 40)) false))
; source callback transition phase=insert-tail[33:44:3]:sift-compare
(define-fun formal_0_624 () FormalMachine (FormalCallback formal_0_623 boundary_0 (select (m_origin formal_0_623) 62) (select (m_origin formal_0_623) 40)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:44:3]
(define-fun formal_0_625 () FormalMachine (FormalWriteFromOrigin formal_0_624 35 62))
; source callback case=recursive-pivot phase=insert-tail[33:44:4]:initial-compare
(assert (not (m_panicked formal_0_625)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_625) (select (m_origin formal_0_625) 10) (select (m_origin formal_0_625) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_625) (select (m_origin formal_0_625) 10) (select (m_origin formal_0_625) 44)) false))
; source callback transition phase=insert-tail[33:44:4]:initial-compare
(define-fun formal_0_626 () FormalMachine (FormalCallback formal_0_625 boundary_0 (select (m_origin formal_0_625) 10) (select (m_origin formal_0_625) 44)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:4]
(define-fun formal_0_627 () FormalMachine (FormalWriteFromOrigin formal_0_626 37 44))
; source callback case=recursive-pivot phase=insert-tail[33:44:4]:sift-compare
(assert (not (m_panicked formal_0_627)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_627) (select (m_origin formal_0_627) 10) (select (m_origin formal_0_627) 62)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_627) (select (m_origin formal_0_627) 10) (select (m_origin formal_0_627) 62)) false))
; source callback transition phase=insert-tail[33:44:4]:sift-compare
(define-fun formal_0_628 () FormalMachine (FormalCallback formal_0_627 boundary_0 (select (m_origin formal_0_627) 10) (select (m_origin formal_0_627) 62)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:4]
(define-fun formal_0_629 () FormalMachine (FormalWriteFromOrigin formal_0_628 36 62))
; source callback case=recursive-pivot phase=insert-tail[33:44:4]:sift-compare
(assert (not (m_panicked formal_0_629)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_629) (select (m_origin formal_0_629) 10) (select (m_origin formal_0_629) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_629) (select (m_origin formal_0_629) 10) (select (m_origin formal_0_629) 40)) false))
; source callback transition phase=insert-tail[33:44:4]:sift-compare
(define-fun formal_0_630 () FormalMachine (FormalCallback formal_0_629 boundary_0 (select (m_origin formal_0_629) 10) (select (m_origin formal_0_629) 40)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:4]
(define-fun formal_0_631 () FormalMachine (FormalWriteFromOrigin formal_0_630 35 40))
; source callback case=recursive-pivot phase=insert-tail[33:44:4]:sift-compare
(assert (not (m_panicked formal_0_631)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_631) (select (m_origin formal_0_631) 10) (select (m_origin formal_0_631) 41)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_631) (select (m_origin formal_0_631) 10) (select (m_origin formal_0_631) 41)) false))
; source callback transition phase=insert-tail[33:44:4]:sift-compare
(define-fun formal_0_632 () FormalMachine (FormalCallback formal_0_631 boundary_0 (select (m_origin formal_0_631) 10) (select (m_origin formal_0_631) 41)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:44:4]
(define-fun formal_0_633 () FormalMachine (FormalWriteFromOrigin formal_0_632 34 10))
; source callback case=recursive-pivot phase=insert-tail[33:44:5]:initial-compare
(assert (not (m_panicked formal_0_633)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_633) (select (m_origin formal_0_633) 34) (select (m_origin formal_0_633) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_633) (select (m_origin formal_0_633) 34) (select (m_origin formal_0_633) 44)) false))
; source callback transition phase=insert-tail[33:44:5]:initial-compare
(define-fun formal_0_634 () FormalMachine (FormalCallback formal_0_633 boundary_0 (select (m_origin formal_0_633) 34) (select (m_origin formal_0_633) 44)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:5]
(define-fun formal_0_635 () FormalMachine (FormalWriteFromOrigin formal_0_634 38 44))
; source callback case=recursive-pivot phase=insert-tail[33:44:5]:sift-compare
(assert (not (m_panicked formal_0_635)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_635) (select (m_origin formal_0_635) 34) (select (m_origin formal_0_635) 62)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_635) (select (m_origin formal_0_635) 34) (select (m_origin formal_0_635) 62)) false))
; source callback transition phase=insert-tail[33:44:5]:sift-compare
(define-fun formal_0_636 () FormalMachine (FormalCallback formal_0_635 boundary_0 (select (m_origin formal_0_635) 34) (select (m_origin formal_0_635) 62)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:5]
(define-fun formal_0_637 () FormalMachine (FormalWriteFromOrigin formal_0_636 37 62))
; source callback case=recursive-pivot phase=insert-tail[33:44:5]:sift-compare
(assert (not (m_panicked formal_0_637)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_637) (select (m_origin formal_0_637) 34) (select (m_origin formal_0_637) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_637) (select (m_origin formal_0_637) 34) (select (m_origin formal_0_637) 40)) false))
; source callback transition phase=insert-tail[33:44:5]:sift-compare
(define-fun formal_0_638 () FormalMachine (FormalCallback formal_0_637 boundary_0 (select (m_origin formal_0_637) 34) (select (m_origin formal_0_637) 40)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:5]
(define-fun formal_0_639 () FormalMachine (FormalWriteFromOrigin formal_0_638 36 40))
; source callback case=recursive-pivot phase=insert-tail[33:44:5]:sift-compare
(assert (not (m_panicked formal_0_639)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_639) (select (m_origin formal_0_639) 34) (select (m_origin formal_0_639) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_639) (select (m_origin formal_0_639) 34) (select (m_origin formal_0_639) 10)) false))
; source callback transition phase=insert-tail[33:44:5]:sift-compare
(define-fun formal_0_640 () FormalMachine (FormalCallback formal_0_639 boundary_0 (select (m_origin formal_0_639) 34) (select (m_origin formal_0_639) 10)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:5]
(define-fun formal_0_641 () FormalMachine (FormalWriteFromOrigin formal_0_640 35 10))
; source callback case=recursive-pivot phase=insert-tail[33:44:5]:sift-compare
(assert (not (m_panicked formal_0_641)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_641) (select (m_origin formal_0_641) 34) (select (m_origin formal_0_641) 41)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_641) (select (m_origin formal_0_641) 34) (select (m_origin formal_0_641) 41)) false))
; source callback transition phase=insert-tail[33:44:5]:sift-compare
(define-fun formal_0_642 () FormalMachine (FormalCallback formal_0_641 boundary_0 (select (m_origin formal_0_641) 34) (select (m_origin formal_0_641) 41)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:44:5]
(define-fun formal_0_643 () FormalMachine (FormalWriteFromOrigin formal_0_642 34 34))
; source callback case=recursive-pivot phase=insert-tail[33:44:6]:initial-compare
(assert (not (m_panicked formal_0_643)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_643) (select (m_origin formal_0_643) 36) (select (m_origin formal_0_643) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_643) (select (m_origin formal_0_643) 36) (select (m_origin formal_0_643) 44)) false))
; source callback transition phase=insert-tail[33:44:6]:initial-compare
(define-fun formal_0_644 () FormalMachine (FormalCallback formal_0_643 boundary_0 (select (m_origin formal_0_643) 36) (select (m_origin formal_0_643) 44)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:6]
(define-fun formal_0_645 () FormalMachine (FormalWriteFromOrigin formal_0_644 39 44))
; source callback case=recursive-pivot phase=insert-tail[33:44:6]:sift-compare
(assert (not (m_panicked formal_0_645)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_645) (select (m_origin formal_0_645) 36) (select (m_origin formal_0_645) 62)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_645) (select (m_origin formal_0_645) 36) (select (m_origin formal_0_645) 62)) false))
; source callback transition phase=insert-tail[33:44:6]:sift-compare
(define-fun formal_0_646 () FormalMachine (FormalCallback formal_0_645 boundary_0 (select (m_origin formal_0_645) 36) (select (m_origin formal_0_645) 62)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:6]
(define-fun formal_0_647 () FormalMachine (FormalWriteFromOrigin formal_0_646 38 62))
; source callback case=recursive-pivot phase=insert-tail[33:44:6]:sift-compare
(assert (not (m_panicked formal_0_647)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_647) (select (m_origin formal_0_647) 36) (select (m_origin formal_0_647) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_647) (select (m_origin formal_0_647) 36) (select (m_origin formal_0_647) 40)) false))
; source callback transition phase=insert-tail[33:44:6]:sift-compare
(define-fun formal_0_648 () FormalMachine (FormalCallback formal_0_647 boundary_0 (select (m_origin formal_0_647) 36) (select (m_origin formal_0_647) 40)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:6]
(define-fun formal_0_649 () FormalMachine (FormalWriteFromOrigin formal_0_648 37 40))
; source callback case=recursive-pivot phase=insert-tail[33:44:6]:sift-compare
(assert (not (m_panicked formal_0_649)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_649) (select (m_origin formal_0_649) 36) (select (m_origin formal_0_649) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_649) (select (m_origin formal_0_649) 36) (select (m_origin formal_0_649) 10)) false))
; source callback transition phase=insert-tail[33:44:6]:sift-compare
(define-fun formal_0_650 () FormalMachine (FormalCallback formal_0_649 boundary_0 (select (m_origin formal_0_649) 36) (select (m_origin formal_0_649) 10)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:6]
(define-fun formal_0_651 () FormalMachine (FormalWriteFromOrigin formal_0_650 36 10))
; source callback case=recursive-pivot phase=insert-tail[33:44:6]:sift-compare
(assert (not (m_panicked formal_0_651)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_651) (select (m_origin formal_0_651) 36) (select (m_origin formal_0_651) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_651) (select (m_origin formal_0_651) 36) (select (m_origin formal_0_651) 34)) false))
; source callback transition phase=insert-tail[33:44:6]:sift-compare
(define-fun formal_0_652 () FormalMachine (FormalCallback formal_0_651 boundary_0 (select (m_origin formal_0_651) 36) (select (m_origin formal_0_651) 34)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:6]
(define-fun formal_0_653 () FormalMachine (FormalWriteFromOrigin formal_0_652 35 34))
; source callback case=recursive-pivot phase=insert-tail[33:44:6]:sift-compare
(assert (not (m_panicked formal_0_653)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_653) (select (m_origin formal_0_653) 36) (select (m_origin formal_0_653) 41)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_653) (select (m_origin formal_0_653) 36) (select (m_origin formal_0_653) 41)) false))
; source callback transition phase=insert-tail[33:44:6]:sift-compare
(define-fun formal_0_654 () FormalMachine (FormalCallback formal_0_653 boundary_0 (select (m_origin formal_0_653) 36) (select (m_origin formal_0_653) 41)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:6]
(define-fun formal_0_655 () FormalMachine (FormalWriteFromOrigin formal_0_654 34 41))
; source write kind=copy-on-drop-restore phase=insert-tail[33:44:6]
(define-fun formal_0_656 () FormalMachine (FormalWriteFromOrigin formal_0_655 33 36))
; source callback case=recursive-pivot phase=insert-tail[33:44:7]:initial-compare
(assert (not (m_panicked formal_0_656)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_656) (select (m_origin formal_0_656) 69) (select (m_origin formal_0_656) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_656) (select (m_origin formal_0_656) 69) (select (m_origin formal_0_656) 44)) false))
; source callback transition phase=insert-tail[33:44:7]:initial-compare
(define-fun formal_0_657 () FormalMachine (FormalCallback formal_0_656 boundary_0 (select (m_origin formal_0_656) 69) (select (m_origin formal_0_656) 44)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:7]
(define-fun formal_0_658 () FormalMachine (FormalWriteFromOrigin formal_0_657 40 44))
; source callback case=recursive-pivot phase=insert-tail[33:44:7]:sift-compare
(assert (not (m_panicked formal_0_658)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_658) (select (m_origin formal_0_658) 69) (select (m_origin formal_0_658) 62)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_658) (select (m_origin formal_0_658) 69) (select (m_origin formal_0_658) 62)) false))
; source callback transition phase=insert-tail[33:44:7]:sift-compare
(define-fun formal_0_659 () FormalMachine (FormalCallback formal_0_658 boundary_0 (select (m_origin formal_0_658) 69) (select (m_origin formal_0_658) 62)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:7]
(define-fun formal_0_660 () FormalMachine (FormalWriteFromOrigin formal_0_659 39 62))
; source callback case=recursive-pivot phase=insert-tail[33:44:7]:sift-compare
(assert (not (m_panicked formal_0_660)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_660) (select (m_origin formal_0_660) 69) (select (m_origin formal_0_660) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_660) (select (m_origin formal_0_660) 69) (select (m_origin formal_0_660) 40)) false))
; source callback transition phase=insert-tail[33:44:7]:sift-compare
(define-fun formal_0_661 () FormalMachine (FormalCallback formal_0_660 boundary_0 (select (m_origin formal_0_660) 69) (select (m_origin formal_0_660) 40)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:7]
(define-fun formal_0_662 () FormalMachine (FormalWriteFromOrigin formal_0_661 38 40))
; source callback case=recursive-pivot phase=insert-tail[33:44:7]:sift-compare
(assert (not (m_panicked formal_0_662)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_662) (select (m_origin formal_0_662) 69) (select (m_origin formal_0_662) 10)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_662) (select (m_origin formal_0_662) 69) (select (m_origin formal_0_662) 10)) false))
; source callback transition phase=insert-tail[33:44:7]:sift-compare
(define-fun formal_0_663 () FormalMachine (FormalCallback formal_0_662 boundary_0 (select (m_origin formal_0_662) 69) (select (m_origin formal_0_662) 10)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:44:7]
(define-fun formal_0_664 () FormalMachine (FormalWriteFromOrigin formal_0_663 37 69))
; source callback case=recursive-pivot phase=insert-tail[33:44:8]:initial-compare
(assert (not (m_panicked formal_0_664)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_664) (select (m_origin formal_0_664) 25) (select (m_origin formal_0_664) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_664) (select (m_origin formal_0_664) 25) (select (m_origin formal_0_664) 44)) false))
; source callback transition phase=insert-tail[33:44:8]:initial-compare
(define-fun formal_0_665 () FormalMachine (FormalCallback formal_0_664 boundary_0 (select (m_origin formal_0_664) 25) (select (m_origin formal_0_664) 44)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:8]
(define-fun formal_0_666 () FormalMachine (FormalWriteFromOrigin formal_0_665 41 44))
; source callback case=recursive-pivot phase=insert-tail[33:44:8]:sift-compare
(assert (not (m_panicked formal_0_666)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_666) (select (m_origin formal_0_666) 25) (select (m_origin formal_0_666) 62)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_666) (select (m_origin formal_0_666) 25) (select (m_origin formal_0_666) 62)) false))
; source callback transition phase=insert-tail[33:44:8]:sift-compare
(define-fun formal_0_667 () FormalMachine (FormalCallback formal_0_666 boundary_0 (select (m_origin formal_0_666) 25) (select (m_origin formal_0_666) 62)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:8]
(define-fun formal_0_668 () FormalMachine (FormalWriteFromOrigin formal_0_667 40 62))
; source callback case=recursive-pivot phase=insert-tail[33:44:8]:sift-compare
(assert (not (m_panicked formal_0_668)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_668) (select (m_origin formal_0_668) 25) (select (m_origin formal_0_668) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_668) (select (m_origin formal_0_668) 25) (select (m_origin formal_0_668) 40)) false))
; source callback transition phase=insert-tail[33:44:8]:sift-compare
(define-fun formal_0_669 () FormalMachine (FormalCallback formal_0_668 boundary_0 (select (m_origin formal_0_668) 25) (select (m_origin formal_0_668) 40)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:8]
(define-fun formal_0_670 () FormalMachine (FormalWriteFromOrigin formal_0_669 39 40))
; source callback case=recursive-pivot phase=insert-tail[33:44:8]:sift-compare
(assert (not (m_panicked formal_0_670)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_670) (select (m_origin formal_0_670) 25) (select (m_origin formal_0_670) 69)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_670) (select (m_origin formal_0_670) 25) (select (m_origin formal_0_670) 69)) false))
; source callback transition phase=insert-tail[33:44:8]:sift-compare
(define-fun formal_0_671 () FormalMachine (FormalCallback formal_0_670 boundary_0 (select (m_origin formal_0_670) 25) (select (m_origin formal_0_670) 69)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:44:8]
(define-fun formal_0_672 () FormalMachine (FormalWriteFromOrigin formal_0_671 38 25))
; source callback case=recursive-pivot phase=insert-tail[33:44:9]:initial-compare
(assert (not (m_panicked formal_0_672)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_672) (select (m_origin formal_0_672) 73) (select (m_origin formal_0_672) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_672) (select (m_origin formal_0_672) 73) (select (m_origin formal_0_672) 44)) false))
; source callback transition phase=insert-tail[33:44:9]:initial-compare
(define-fun formal_0_673 () FormalMachine (FormalCallback formal_0_672 boundary_0 (select (m_origin formal_0_672) 73) (select (m_origin formal_0_672) 44)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:9]
(define-fun formal_0_674 () FormalMachine (FormalWriteFromOrigin formal_0_673 42 44))
; source callback case=recursive-pivot phase=insert-tail[33:44:9]:sift-compare
(assert (not (m_panicked formal_0_674)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_674) (select (m_origin formal_0_674) 73) (select (m_origin formal_0_674) 62)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_674) (select (m_origin formal_0_674) 73) (select (m_origin formal_0_674) 62)) false))
; source callback transition phase=insert-tail[33:44:9]:sift-compare
(define-fun formal_0_675 () FormalMachine (FormalCallback formal_0_674 boundary_0 (select (m_origin formal_0_674) 73) (select (m_origin formal_0_674) 62)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:9]
(define-fun formal_0_676 () FormalMachine (FormalWriteFromOrigin formal_0_675 41 62))
; source callback case=recursive-pivot phase=insert-tail[33:44:9]:sift-compare
(assert (not (m_panicked formal_0_676)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_676) (select (m_origin formal_0_676) 73) (select (m_origin formal_0_676) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_676) (select (m_origin formal_0_676) 73) (select (m_origin formal_0_676) 40)) false))
; source callback transition phase=insert-tail[33:44:9]:sift-compare
(define-fun formal_0_677 () FormalMachine (FormalCallback formal_0_676 boundary_0 (select (m_origin formal_0_676) 73) (select (m_origin formal_0_676) 40)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:9]
(define-fun formal_0_678 () FormalMachine (FormalWriteFromOrigin formal_0_677 40 40))
; source callback case=recursive-pivot phase=insert-tail[33:44:9]:sift-compare
(assert (not (m_panicked formal_0_678)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_678) (select (m_origin formal_0_678) 73) (select (m_origin formal_0_678) 25)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_678) (select (m_origin formal_0_678) 73) (select (m_origin formal_0_678) 25)) false))
; source callback transition phase=insert-tail[33:44:9]:sift-compare
(define-fun formal_0_679 () FormalMachine (FormalCallback formal_0_678 boundary_0 (select (m_origin formal_0_678) 73) (select (m_origin formal_0_678) 25)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:9]
(define-fun formal_0_680 () FormalMachine (FormalWriteFromOrigin formal_0_679 39 25))
; source callback case=recursive-pivot phase=insert-tail[33:44:9]:sift-compare
(assert (not (m_panicked formal_0_680)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_680) (select (m_origin formal_0_680) 73) (select (m_origin formal_0_680) 69)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_680) (select (m_origin formal_0_680) 73) (select (m_origin formal_0_680) 69)) false))
; source callback transition phase=insert-tail[33:44:9]:sift-compare
(define-fun formal_0_681 () FormalMachine (FormalCallback formal_0_680 boundary_0 (select (m_origin formal_0_680) 73) (select (m_origin formal_0_680) 69)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:9]
(define-fun formal_0_682 () FormalMachine (FormalWriteFromOrigin formal_0_681 38 69))
; source callback case=recursive-pivot phase=insert-tail[33:44:9]:sift-compare
(assert (not (m_panicked formal_0_682)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_682) (select (m_origin formal_0_682) 73) (select (m_origin formal_0_682) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_682) (select (m_origin formal_0_682) 73) (select (m_origin formal_0_682) 10)) false))
; source callback transition phase=insert-tail[33:44:9]:sift-compare
(define-fun formal_0_683 () FormalMachine (FormalCallback formal_0_682 boundary_0 (select (m_origin formal_0_682) 73) (select (m_origin formal_0_682) 10)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:9]
(define-fun formal_0_684 () FormalMachine (FormalWriteFromOrigin formal_0_683 37 10))
; source callback case=recursive-pivot phase=insert-tail[33:44:9]:sift-compare
(assert (not (m_panicked formal_0_684)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_684) (select (m_origin formal_0_684) 73) (select (m_origin formal_0_684) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_684) (select (m_origin formal_0_684) 73) (select (m_origin formal_0_684) 34)) false))
; source callback transition phase=insert-tail[33:44:9]:sift-compare
(define-fun formal_0_685 () FormalMachine (FormalCallback formal_0_684 boundary_0 (select (m_origin formal_0_684) 73) (select (m_origin formal_0_684) 34)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:9]
(define-fun formal_0_686 () FormalMachine (FormalWriteFromOrigin formal_0_685 36 34))
; source callback case=recursive-pivot phase=insert-tail[33:44:9]:sift-compare
(assert (not (m_panicked formal_0_686)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_686) (select (m_origin formal_0_686) 73) (select (m_origin formal_0_686) 41)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_686) (select (m_origin formal_0_686) 73) (select (m_origin formal_0_686) 41)) false))
; source callback transition phase=insert-tail[33:44:9]:sift-compare
(define-fun formal_0_687 () FormalMachine (FormalCallback formal_0_686 boundary_0 (select (m_origin formal_0_686) 73) (select (m_origin formal_0_686) 41)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:9]
(define-fun formal_0_688 () FormalMachine (FormalWriteFromOrigin formal_0_687 35 41))
; source callback case=recursive-pivot phase=insert-tail[33:44:9]:sift-compare
(assert (not (m_panicked formal_0_688)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_688) (select (m_origin formal_0_688) 73) (select (m_origin formal_0_688) 36)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_688) (select (m_origin formal_0_688) 73) (select (m_origin formal_0_688) 36)) false))
; source callback transition phase=insert-tail[33:44:9]:sift-compare
(define-fun formal_0_689 () FormalMachine (FormalCallback formal_0_688 boundary_0 (select (m_origin formal_0_688) 73) (select (m_origin formal_0_688) 36)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:9]
(define-fun formal_0_690 () FormalMachine (FormalWriteFromOrigin formal_0_689 34 36))
; source write kind=copy-on-drop-restore phase=insert-tail[33:44:9]
(define-fun formal_0_691 () FormalMachine (FormalWriteFromOrigin formal_0_690 33 73))
; source callback case=recursive-pivot phase=insert-tail[33:44:10]:initial-compare
(assert (not (m_panicked formal_0_691)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_691) (select (m_origin formal_0_691) 12) (select (m_origin formal_0_691) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_691) (select (m_origin formal_0_691) 12) (select (m_origin formal_0_691) 44)) false))
; source callback transition phase=insert-tail[33:44:10]:initial-compare
(define-fun formal_0_692 () FormalMachine (FormalCallback formal_0_691 boundary_0 (select (m_origin formal_0_691) 12) (select (m_origin formal_0_691) 44)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:10]
(define-fun formal_0_693 () FormalMachine (FormalWriteFromOrigin formal_0_692 43 44))
; source callback case=recursive-pivot phase=insert-tail[33:44:10]:sift-compare
(assert (not (m_panicked formal_0_693)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_693) (select (m_origin formal_0_693) 12) (select (m_origin formal_0_693) 62)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_693) (select (m_origin formal_0_693) 12) (select (m_origin formal_0_693) 62)) false))
; source callback transition phase=insert-tail[33:44:10]:sift-compare
(define-fun formal_0_694 () FormalMachine (FormalCallback formal_0_693 boundary_0 (select (m_origin formal_0_693) 12) (select (m_origin formal_0_693) 62)))
; source write kind=insert-tail-shift phase=insert-tail[33:44:10]
(define-fun formal_0_695 () FormalMachine (FormalWriteFromOrigin formal_0_694 42 62))
; source callback case=recursive-pivot phase=insert-tail[33:44:10]:sift-compare
(assert (not (m_panicked formal_0_695)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_695) (select (m_origin formal_0_695) 12) (select (m_origin formal_0_695) 40)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_695) (select (m_origin formal_0_695) 12) (select (m_origin formal_0_695) 40)) false))
; source callback transition phase=insert-tail[33:44:10]:sift-compare
(define-fun formal_0_696 () FormalMachine (FormalCallback formal_0_695 boundary_0 (select (m_origin formal_0_695) 12) (select (m_origin formal_0_695) 40)))
; source write kind=copy-on-drop-restore phase=insert-tail[33:44:10]
(define-fun formal_0_697 () FormalMachine (FormalWriteFromOrigin formal_0_696 41 12))
; source callback case=recursive-pivot phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_697)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_697) (select (m_origin formal_0_697) 45) (select (m_origin formal_0_697) 61)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_697) (select (m_origin formal_0_697) 45) (select (m_origin formal_0_697) 61)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_698 () FormalMachine (FormalCallback formal_0_697 boundary_0 (select (m_origin formal_0_697) 45) (select (m_origin formal_0_697) 61)))
; source callback case=recursive-pivot phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_698)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_698) (select (m_origin formal_0_698) 45) (select (m_origin formal_0_698) 43)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_698) (select (m_origin formal_0_698) 45) (select (m_origin formal_0_698) 43)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_699 () FormalMachine (FormalCallback formal_0_698 boundary_0 (select (m_origin formal_0_698) 45) (select (m_origin formal_0_698) 43)))
; source callback case=recursive-pivot phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_699)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_699) (select (m_origin formal_0_699) 74) (select (m_origin formal_0_699) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_699) (select (m_origin formal_0_699) 74) (select (m_origin formal_0_699) 45)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_700 () FormalMachine (FormalCallback formal_0_699 boundary_0 (select (m_origin formal_0_699) 74) (select (m_origin formal_0_699) 45)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_701 () FormalMachine (FormalSwap formal_0_700 45 45))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_701)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_701) (select (m_origin formal_0_701) 19) (select (m_origin formal_0_701) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_701) (select (m_origin formal_0_701) 19) (select (m_origin formal_0_701) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_702 () FormalMachine (FormalCallback formal_0_701 boundary_0 (select (m_origin formal_0_701) 19) (select (m_origin formal_0_701) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_703 () FormalMachine (FormalWriteFromOrigin formal_0_702 46 19))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_703)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_703) (select (m_origin formal_0_703) 48) (select (m_origin formal_0_703) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_703) (select (m_origin formal_0_703) 48) (select (m_origin formal_0_703) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_704 () FormalMachine (FormalCallback formal_0_703 boundary_0 (select (m_origin formal_0_703) 48) (select (m_origin formal_0_703) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_705 () FormalMachine (FormalWriteFromOrigin formal_0_704 47 48))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_705)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_705) (select (m_origin formal_0_705) 49) (select (m_origin formal_0_705) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_705) (select (m_origin formal_0_705) 49) (select (m_origin formal_0_705) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_706 () FormalMachine (FormalCallback formal_0_705 boundary_0 (select (m_origin formal_0_705) 49) (select (m_origin formal_0_705) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_707 () FormalMachine (FormalWriteFromOrigin formal_0_706 48 49))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_707)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_707) (select (m_origin formal_0_707) 30) (select (m_origin formal_0_707) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_707) (select (m_origin formal_0_707) 30) (select (m_origin formal_0_707) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_708 () FormalMachine (FormalCallback formal_0_707 boundary_0 (select (m_origin formal_0_707) 30) (select (m_origin formal_0_707) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_709 () FormalMachine (FormalWriteFromOrigin formal_0_708 48 30))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_709)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_709) (select (m_origin formal_0_709) 7) (select (m_origin formal_0_709) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_709) (select (m_origin formal_0_709) 7) (select (m_origin formal_0_709) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_710 () FormalMachine (FormalCallback formal_0_709 boundary_0 (select (m_origin formal_0_709) 7) (select (m_origin formal_0_709) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_711 () FormalMachine (FormalWriteFromOrigin formal_0_710 49 7))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_712 () FormalMachine (FormalWriteFromOrigin formal_0_711 50 49))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_712)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_712) (select (m_origin formal_0_712) 32) (select (m_origin formal_0_712) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_712) (select (m_origin formal_0_712) 32) (select (m_origin formal_0_712) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_713 () FormalMachine (FormalCallback formal_0_712 boundary_0 (select (m_origin formal_0_712) 32) (select (m_origin formal_0_712) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_714 () FormalMachine (FormalWriteFromOrigin formal_0_713 49 32))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_714)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_714) (select (m_origin formal_0_714) 53) (select (m_origin formal_0_714) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_714) (select (m_origin formal_0_714) 53) (select (m_origin formal_0_714) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_715 () FormalMachine (FormalCallback formal_0_714 boundary_0 (select (m_origin formal_0_714) 53) (select (m_origin formal_0_714) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_716 () FormalMachine (FormalWriteFromOrigin formal_0_715 50 53))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_717 () FormalMachine (FormalWriteFromOrigin formal_0_716 52 49))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_717)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_717) (select (m_origin formal_0_717) 54) (select (m_origin formal_0_717) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_717) (select (m_origin formal_0_717) 54) (select (m_origin formal_0_717) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_718 () FormalMachine (FormalCallback formal_0_717 boundary_0 (select (m_origin formal_0_717) 54) (select (m_origin formal_0_717) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_719 () FormalMachine (FormalWriteFromOrigin formal_0_718 51 54))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_720 () FormalMachine (FormalWriteFromOrigin formal_0_719 53 7))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_720)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_720) (select (m_origin formal_0_720) 13) (select (m_origin formal_0_720) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_720) (select (m_origin formal_0_720) 13) (select (m_origin formal_0_720) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_721 () FormalMachine (FormalCallback formal_0_720 boundary_0 (select (m_origin formal_0_720) 13) (select (m_origin formal_0_720) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_722 () FormalMachine (FormalWriteFromOrigin formal_0_721 52 13))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_723 () FormalMachine (FormalWriteFromOrigin formal_0_722 54 49))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_723)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_723) (select (m_origin formal_0_723) 2) (select (m_origin formal_0_723) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_723) (select (m_origin formal_0_723) 2) (select (m_origin formal_0_723) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_724 () FormalMachine (FormalCallback formal_0_723 boundary_0 (select (m_origin formal_0_723) 2) (select (m_origin formal_0_723) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_725 () FormalMachine (FormalWriteFromOrigin formal_0_724 53 2))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_726 () FormalMachine (FormalWriteFromOrigin formal_0_725 55 7))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_726)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_726) (select (m_origin formal_0_726) 35) (select (m_origin formal_0_726) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_726) (select (m_origin formal_0_726) 35) (select (m_origin formal_0_726) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_727 () FormalMachine (FormalCallback formal_0_726 boundary_0 (select (m_origin formal_0_726) 35) (select (m_origin formal_0_726) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_728 () FormalMachine (FormalWriteFromOrigin formal_0_727 54 35))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_729 () FormalMachine (FormalWriteFromOrigin formal_0_728 56 49))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_729)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_729) (select (m_origin formal_0_729) 5) (select (m_origin formal_0_729) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_729) (select (m_origin formal_0_729) 5) (select (m_origin formal_0_729) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_730 () FormalMachine (FormalCallback formal_0_729 boundary_0 (select (m_origin formal_0_729) 5) (select (m_origin formal_0_729) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_731 () FormalMachine (FormalWriteFromOrigin formal_0_730 54 5))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_731)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_731) (select (m_origin formal_0_731) 59) (select (m_origin formal_0_731) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_731) (select (m_origin formal_0_731) 59) (select (m_origin formal_0_731) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_732 () FormalMachine (FormalCallback formal_0_731 boundary_0 (select (m_origin formal_0_731) 59) (select (m_origin formal_0_731) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_733 () FormalMachine (FormalWriteFromOrigin formal_0_732 54 59))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_733)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_733) (select (m_origin formal_0_733) 60) (select (m_origin formal_0_733) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_733) (select (m_origin formal_0_733) 60) (select (m_origin formal_0_733) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_734 () FormalMachine (FormalCallback formal_0_733 boundary_0 (select (m_origin formal_0_733) 60) (select (m_origin formal_0_733) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_735 () FormalMachine (FormalWriteFromOrigin formal_0_734 55 60))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_736 () FormalMachine (FormalWriteFromOrigin formal_0_735 59 7))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_736)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_736) (select (m_origin formal_0_736) 61) (select (m_origin formal_0_736) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_736) (select (m_origin formal_0_736) 61) (select (m_origin formal_0_736) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_737 () FormalMachine (FormalCallback formal_0_736 boundary_0 (select (m_origin formal_0_736) 61) (select (m_origin formal_0_736) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_738 () FormalMachine (FormalWriteFromOrigin formal_0_737 56 61))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_739 () FormalMachine (FormalWriteFromOrigin formal_0_738 60 49))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_739)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_739) (select (m_origin formal_0_739) 37) (select (m_origin formal_0_739) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_739) (select (m_origin formal_0_739) 37) (select (m_origin formal_0_739) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_740 () FormalMachine (FormalCallback formal_0_739 boundary_0 (select (m_origin formal_0_739) 37) (select (m_origin formal_0_739) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_741 () FormalMachine (FormalWriteFromOrigin formal_0_740 57 37))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_742 () FormalMachine (FormalWriteFromOrigin formal_0_741 61 35))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_742)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_742) (select (m_origin formal_0_742) 24) (select (m_origin formal_0_742) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_742) (select (m_origin formal_0_742) 24) (select (m_origin formal_0_742) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_743 () FormalMachine (FormalCallback formal_0_742 boundary_0 (select (m_origin formal_0_742) 24) (select (m_origin formal_0_742) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_744 () FormalMachine (FormalWriteFromOrigin formal_0_743 58 24))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_745 () FormalMachine (FormalWriteFromOrigin formal_0_744 62 5))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_745)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_745) (select (m_origin formal_0_745) 6) (select (m_origin formal_0_745) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_745) (select (m_origin formal_0_745) 6) (select (m_origin formal_0_745) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_746 () FormalMachine (FormalCallback formal_0_745 boundary_0 (select (m_origin formal_0_745) 6) (select (m_origin formal_0_745) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_747 () FormalMachine (FormalWriteFromOrigin formal_0_746 59 6))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_748 () FormalMachine (FormalWriteFromOrigin formal_0_747 63 7))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_748)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_748) (select (m_origin formal_0_748) 65) (select (m_origin formal_0_748) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_748) (select (m_origin formal_0_748) 65) (select (m_origin formal_0_748) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_749 () FormalMachine (FormalCallback formal_0_748 boundary_0 (select (m_origin formal_0_748) 65) (select (m_origin formal_0_748) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_750 () FormalMachine (FormalWriteFromOrigin formal_0_749 59 65))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_750)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_750) (select (m_origin formal_0_750) 11) (select (m_origin formal_0_750) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_750) (select (m_origin formal_0_750) 11) (select (m_origin formal_0_750) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_751 () FormalMachine (FormalCallback formal_0_750 boundary_0 (select (m_origin formal_0_750) 11) (select (m_origin formal_0_750) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_752 () FormalMachine (FormalWriteFromOrigin formal_0_751 60 11))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_753 () FormalMachine (FormalWriteFromOrigin formal_0_752 65 49))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_753)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_753) (select (m_origin formal_0_753) 67) (select (m_origin formal_0_753) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_753) (select (m_origin formal_0_753) 67) (select (m_origin formal_0_753) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_754 () FormalMachine (FormalCallback formal_0_753 boundary_0 (select (m_origin formal_0_753) 67) (select (m_origin formal_0_753) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_755 () FormalMachine (FormalWriteFromOrigin formal_0_754 60 67))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_755)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_755) (select (m_origin formal_0_755) 68) (select (m_origin formal_0_755) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_755) (select (m_origin formal_0_755) 68) (select (m_origin formal_0_755) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_756 () FormalMachine (FormalCallback formal_0_755 boundary_0 (select (m_origin formal_0_755) 68) (select (m_origin formal_0_755) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_757 () FormalMachine (FormalWriteFromOrigin formal_0_756 60 68))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_757)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_757) (select (m_origin formal_0_757) 18) (select (m_origin formal_0_757) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_757) (select (m_origin formal_0_757) 18) (select (m_origin formal_0_757) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_758 () FormalMachine (FormalCallback formal_0_757 boundary_0 (select (m_origin formal_0_757) 18) (select (m_origin formal_0_757) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_759 () FormalMachine (FormalWriteFromOrigin formal_0_758 61 18))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_760 () FormalMachine (FormalWriteFromOrigin formal_0_759 68 35))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_760)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_760) (select (m_origin formal_0_760) 42) (select (m_origin formal_0_760) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_760) (select (m_origin formal_0_760) 42) (select (m_origin formal_0_760) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_761 () FormalMachine (FormalCallback formal_0_760 boundary_0 (select (m_origin formal_0_760) 42) (select (m_origin formal_0_760) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_762 () FormalMachine (FormalWriteFromOrigin formal_0_761 62 42))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_763 () FormalMachine (FormalWriteFromOrigin formal_0_762 69 5))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_763)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_763) (select (m_origin formal_0_763) 71) (select (m_origin formal_0_763) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_763) (select (m_origin formal_0_763) 71) (select (m_origin formal_0_763) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_764 () FormalMachine (FormalCallback formal_0_763 boundary_0 (select (m_origin formal_0_763) 71) (select (m_origin formal_0_763) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_765 () FormalMachine (FormalWriteFromOrigin formal_0_764 63 71))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_766 () FormalMachine (FormalWriteFromOrigin formal_0_765 70 7))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_766)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_766) (select (m_origin formal_0_766) 72) (select (m_origin formal_0_766) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_766) (select (m_origin formal_0_766) 72) (select (m_origin formal_0_766) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_767 () FormalMachine (FormalCallback formal_0_766 boundary_0 (select (m_origin formal_0_766) 72) (select (m_origin formal_0_766) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_768 () FormalMachine (FormalWriteFromOrigin formal_0_767 64 72))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_769 () FormalMachine (FormalWriteFromOrigin formal_0_768 71 6))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_769)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_769) (select (m_origin formal_0_769) 43) (select (m_origin formal_0_769) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_769) (select (m_origin formal_0_769) 43) (select (m_origin formal_0_769) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_770 () FormalMachine (FormalCallback formal_0_769 boundary_0 (select (m_origin formal_0_769) 43) (select (m_origin formal_0_769) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_771 () FormalMachine (FormalWriteFromOrigin formal_0_770 64 43))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_771)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_771) (select (m_origin formal_0_771) 0) (select (m_origin formal_0_771) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_771) (select (m_origin formal_0_771) 0) (select (m_origin formal_0_771) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_772 () FormalMachine (FormalCallback formal_0_771 boundary_0 (select (m_origin formal_0_771) 0) (select (m_origin formal_0_771) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_773 () FormalMachine (FormalWriteFromOrigin formal_0_772 64 0))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_773)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_773) (select (m_origin formal_0_773) 75) (select (m_origin formal_0_773) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_773) (select (m_origin formal_0_773) 75) (select (m_origin formal_0_773) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_774 () FormalMachine (FormalCallback formal_0_773 boundary_0 (select (m_origin formal_0_773) 75) (select (m_origin formal_0_773) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_775 () FormalMachine (FormalWriteFromOrigin formal_0_774 64 75))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_775)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_775) (select (m_origin formal_0_775) 76) (select (m_origin formal_0_775) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_775) (select (m_origin formal_0_775) 76) (select (m_origin formal_0_775) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_776 () FormalMachine (FormalCallback formal_0_775 boundary_0 (select (m_origin formal_0_775) 76) (select (m_origin formal_0_775) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_777 () FormalMachine (FormalWriteFromOrigin formal_0_776 65 76))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_778 () FormalMachine (FormalWriteFromOrigin formal_0_777 75 49))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_778)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_778) (select (m_origin formal_0_778) 77) (select (m_origin formal_0_778) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_778) (select (m_origin formal_0_778) 77) (select (m_origin formal_0_778) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_779 () FormalMachine (FormalCallback formal_0_778 boundary_0 (select (m_origin formal_0_778) 77) (select (m_origin formal_0_778) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_780 () FormalMachine (FormalWriteFromOrigin formal_0_779 66 77))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_781 () FormalMachine (FormalWriteFromOrigin formal_0_780 76 11))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_781)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_781) (select (m_origin formal_0_781) 78) (select (m_origin formal_0_781) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_781) (select (m_origin formal_0_781) 78) (select (m_origin formal_0_781) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_782 () FormalMachine (FormalCallback formal_0_781 boundary_0 (select (m_origin formal_0_781) 78) (select (m_origin formal_0_781) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_783 () FormalMachine (FormalWriteFromOrigin formal_0_782 67 78))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_784 () FormalMachine (FormalWriteFromOrigin formal_0_783 77 67))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_784)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_784) (select (m_origin formal_0_784) 28) (select (m_origin formal_0_784) 45)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_784) (select (m_origin formal_0_784) 28) (select (m_origin formal_0_784) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_785 () FormalMachine (FormalCallback formal_0_784 boundary_0 (select (m_origin formal_0_784) 28) (select (m_origin formal_0_784) 45)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_786 () FormalMachine (FormalWriteFromOrigin formal_0_785 68 28))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_787 () FormalMachine (FormalWriteFromOrigin formal_0_786 78 35))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_787)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_787) (select (m_origin formal_0_787) 46) (select (m_origin formal_0_787) 45)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_787) (select (m_origin formal_0_787) 46) (select (m_origin formal_0_787) 45)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_788 () FormalMachine (FormalCallback formal_0_787 boundary_0 (select (m_origin formal_0_787) 46) (select (m_origin formal_0_787) 45)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_789 () FormalMachine (FormalWriteFromOrigin formal_0_788 68 46))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_790 () FormalMachine (FormalSwap formal_0_789 45 68))
; source callback case=recursive-pivot phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_790)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_790) (select (m_origin formal_0_790) 46) (select (m_origin formal_0_790) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_790) (select (m_origin formal_0_790) 46) (select (m_origin formal_0_790) 2)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_791 () FormalMachine (FormalCallback formal_0_790 boundary_0 (select (m_origin formal_0_790) 46) (select (m_origin formal_0_790) 2)))
; source callback case=recursive-pivot phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_791)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_791) (select (m_origin formal_0_791) 46) (select (m_origin formal_0_791) 65)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_791) (select (m_origin formal_0_791) 46) (select (m_origin formal_0_791) 65)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_792 () FormalMachine (FormalCallback formal_0_791 boundary_0 (select (m_origin formal_0_791) 46) (select (m_origin formal_0_791) 65)))
; source callback case=recursive-pivot phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_792)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_792) (select (m_origin formal_0_792) 2) (select (m_origin formal_0_792) 65)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_792) (select (m_origin formal_0_792) 2) (select (m_origin formal_0_792) 65)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_793 () FormalMachine (FormalCallback formal_0_792 boundary_0 (select (m_origin formal_0_792) 2) (select (m_origin formal_0_792) 65)))
; source callback case=recursive-pivot phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_793)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_793) (select (m_origin formal_0_793) 74) (select (m_origin formal_0_793) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_793) (select (m_origin formal_0_793) 74) (select (m_origin formal_0_793) 2)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_794 () FormalMachine (FormalCallback formal_0_793 boundary_0 (select (m_origin formal_0_793) 74) (select (m_origin formal_0_793) 2)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_795 () FormalMachine (FormalSwap formal_0_794 45 53))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_795)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_795) (select (m_origin formal_0_795) 48) (select (m_origin formal_0_795) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_795) (select (m_origin formal_0_795) 48) (select (m_origin formal_0_795) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_796 () FormalMachine (FormalCallback formal_0_795 boundary_0 (select (m_origin formal_0_795) 48) (select (m_origin formal_0_795) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_797 () FormalMachine (FormalWriteFromOrigin formal_0_796 46 48))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_797)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_797) (select (m_origin formal_0_797) 30) (select (m_origin formal_0_797) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_797) (select (m_origin formal_0_797) 30) (select (m_origin formal_0_797) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_798 () FormalMachine (FormalCallback formal_0_797 boundary_0 (select (m_origin formal_0_797) 30) (select (m_origin formal_0_797) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_799 () FormalMachine (FormalWriteFromOrigin formal_0_798 47 30))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_799)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_799) (select (m_origin formal_0_799) 32) (select (m_origin formal_0_799) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_799) (select (m_origin formal_0_799) 32) (select (m_origin formal_0_799) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_800 () FormalMachine (FormalCallback formal_0_799 boundary_0 (select (m_origin formal_0_799) 32) (select (m_origin formal_0_799) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_801 () FormalMachine (FormalWriteFromOrigin formal_0_800 48 32))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_801)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_801) (select (m_origin formal_0_801) 53) (select (m_origin formal_0_801) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_801) (select (m_origin formal_0_801) 53) (select (m_origin formal_0_801) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_802 () FormalMachine (FormalCallback formal_0_801 boundary_0 (select (m_origin formal_0_801) 53) (select (m_origin formal_0_801) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_803 () FormalMachine (FormalWriteFromOrigin formal_0_802 49 53))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_803)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_803) (select (m_origin formal_0_803) 54) (select (m_origin formal_0_803) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_803) (select (m_origin formal_0_803) 54) (select (m_origin formal_0_803) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_804 () FormalMachine (FormalCallback formal_0_803 boundary_0 (select (m_origin formal_0_803) 54) (select (m_origin formal_0_803) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_805 () FormalMachine (FormalWriteFromOrigin formal_0_804 50 54))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_805)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_805) (select (m_origin formal_0_805) 13) (select (m_origin formal_0_805) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_805) (select (m_origin formal_0_805) 13) (select (m_origin formal_0_805) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_806 () FormalMachine (FormalCallback formal_0_805 boundary_0 (select (m_origin formal_0_805) 13) (select (m_origin formal_0_805) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_807 () FormalMachine (FormalWriteFromOrigin formal_0_806 51 13))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_807)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_807) (select (m_origin formal_0_807) 46) (select (m_origin formal_0_807) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_807) (select (m_origin formal_0_807) 46) (select (m_origin formal_0_807) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_808 () FormalMachine (FormalCallback formal_0_807 boundary_0 (select (m_origin formal_0_807) 46) (select (m_origin formal_0_807) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_809 () FormalMachine (FormalWriteFromOrigin formal_0_808 51 46))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_809)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_809) (select (m_origin formal_0_809) 59) (select (m_origin formal_0_809) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_809) (select (m_origin formal_0_809) 59) (select (m_origin formal_0_809) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_810 () FormalMachine (FormalCallback formal_0_809 boundary_0 (select (m_origin formal_0_809) 59) (select (m_origin formal_0_809) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_811 () FormalMachine (FormalWriteFromOrigin formal_0_810 52 59))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_812 () FormalMachine (FormalWriteFromOrigin formal_0_811 53 13))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_812)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_812) (select (m_origin formal_0_812) 60) (select (m_origin formal_0_812) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_812) (select (m_origin formal_0_812) 60) (select (m_origin formal_0_812) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_813 () FormalMachine (FormalCallback formal_0_812 boundary_0 (select (m_origin formal_0_812) 60) (select (m_origin formal_0_812) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_814 () FormalMachine (FormalWriteFromOrigin formal_0_813 52 60))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_814)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_814) (select (m_origin formal_0_814) 61) (select (m_origin formal_0_814) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_814) (select (m_origin formal_0_814) 61) (select (m_origin formal_0_814) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_815 () FormalMachine (FormalCallback formal_0_814 boundary_0 (select (m_origin formal_0_814) 61) (select (m_origin formal_0_814) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_816 () FormalMachine (FormalWriteFromOrigin formal_0_815 53 61))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_817 () FormalMachine (FormalWriteFromOrigin formal_0_816 55 13))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_817)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_817) (select (m_origin formal_0_817) 37) (select (m_origin formal_0_817) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_817) (select (m_origin formal_0_817) 37) (select (m_origin formal_0_817) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_818 () FormalMachine (FormalCallback formal_0_817 boundary_0 (select (m_origin formal_0_817) 37) (select (m_origin formal_0_817) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_819 () FormalMachine (FormalWriteFromOrigin formal_0_818 54 37))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_820 () FormalMachine (FormalWriteFromOrigin formal_0_819 56 59))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_820)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_820) (select (m_origin formal_0_820) 24) (select (m_origin formal_0_820) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_820) (select (m_origin formal_0_820) 24) (select (m_origin formal_0_820) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_821 () FormalMachine (FormalCallback formal_0_820 boundary_0 (select (m_origin formal_0_820) 24) (select (m_origin formal_0_820) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_822 () FormalMachine (FormalWriteFromOrigin formal_0_821 55 24))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_823 () FormalMachine (FormalWriteFromOrigin formal_0_822 57 13))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_823)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_823) (select (m_origin formal_0_823) 65) (select (m_origin formal_0_823) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_823) (select (m_origin formal_0_823) 65) (select (m_origin formal_0_823) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_824 () FormalMachine (FormalCallback formal_0_823 boundary_0 (select (m_origin formal_0_823) 65) (select (m_origin formal_0_823) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_825 () FormalMachine (FormalWriteFromOrigin formal_0_824 56 65))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_826 () FormalMachine (FormalWriteFromOrigin formal_0_825 58 59))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_826)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_826) (select (m_origin formal_0_826) 68) (select (m_origin formal_0_826) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_826) (select (m_origin formal_0_826) 68) (select (m_origin formal_0_826) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_827 () FormalMachine (FormalCallback formal_0_826 boundary_0 (select (m_origin formal_0_826) 68) (select (m_origin formal_0_826) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_828 () FormalMachine (FormalWriteFromOrigin formal_0_827 56 68))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_828)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_828) (select (m_origin formal_0_828) 18) (select (m_origin formal_0_828) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_828) (select (m_origin formal_0_828) 18) (select (m_origin formal_0_828) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_829 () FormalMachine (FormalCallback formal_0_828 boundary_0 (select (m_origin formal_0_828) 18) (select (m_origin formal_0_828) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_830 () FormalMachine (FormalWriteFromOrigin formal_0_829 56 18))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_830)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_830) (select (m_origin formal_0_830) 42) (select (m_origin formal_0_830) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_830) (select (m_origin formal_0_830) 42) (select (m_origin formal_0_830) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_831 () FormalMachine (FormalCallback formal_0_830 boundary_0 (select (m_origin formal_0_830) 42) (select (m_origin formal_0_830) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_832 () FormalMachine (FormalWriteFromOrigin formal_0_831 57 42))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_833 () FormalMachine (FormalWriteFromOrigin formal_0_832 61 13))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_833)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_833) (select (m_origin formal_0_833) 71) (select (m_origin formal_0_833) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_833) (select (m_origin formal_0_833) 71) (select (m_origin formal_0_833) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_834 () FormalMachine (FormalCallback formal_0_833 boundary_0 (select (m_origin formal_0_833) 71) (select (m_origin formal_0_833) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_835 () FormalMachine (FormalWriteFromOrigin formal_0_834 57 71))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_835)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_835) (select (m_origin formal_0_835) 75) (select (m_origin formal_0_835) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_835) (select (m_origin formal_0_835) 75) (select (m_origin formal_0_835) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_836 () FormalMachine (FormalCallback formal_0_835 boundary_0 (select (m_origin formal_0_835) 75) (select (m_origin formal_0_835) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_837 () FormalMachine (FormalWriteFromOrigin formal_0_836 58 75))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_838 () FormalMachine (FormalWriteFromOrigin formal_0_837 63 59))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_838)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_838) (select (m_origin formal_0_838) 76) (select (m_origin formal_0_838) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_838) (select (m_origin formal_0_838) 76) (select (m_origin formal_0_838) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_839 () FormalMachine (FormalCallback formal_0_838 boundary_0 (select (m_origin formal_0_838) 76) (select (m_origin formal_0_838) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_840 () FormalMachine (FormalWriteFromOrigin formal_0_839 59 76))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_841 () FormalMachine (FormalWriteFromOrigin formal_0_840 64 65))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_841)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_841) (select (m_origin formal_0_841) 77) (select (m_origin formal_0_841) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_841) (select (m_origin formal_0_841) 77) (select (m_origin formal_0_841) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_842 () FormalMachine (FormalCallback formal_0_841 boundary_0 (select (m_origin formal_0_841) 77) (select (m_origin formal_0_841) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_843 () FormalMachine (FormalWriteFromOrigin formal_0_842 59 77))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_843)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_843) (select (m_origin formal_0_843) 78) (select (m_origin formal_0_843) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_843) (select (m_origin formal_0_843) 78) (select (m_origin formal_0_843) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_844 () FormalMachine (FormalCallback formal_0_843 boundary_0 (select (m_origin formal_0_843) 78) (select (m_origin formal_0_843) 2)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_845 () FormalMachine (FormalWriteFromOrigin formal_0_844 60 78))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_846 () FormalMachine (FormalWriteFromOrigin formal_0_845 66 68))
; source callback case=recursive-pivot phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_846)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_846) (select (m_origin formal_0_846) 19) (select (m_origin formal_0_846) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_846) (select (m_origin formal_0_846) 19) (select (m_origin formal_0_846) 2)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_847 () FormalMachine (FormalCallback formal_0_846 boundary_0 (select (m_origin formal_0_846) 19) (select (m_origin formal_0_846) 2)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_848 () FormalMachine (FormalWriteFromOrigin formal_0_847 60 19))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_849 () FormalMachine (FormalSwap formal_0_848 45 59))
; source callback case=recursive-pivot phase=insert-tail[45:59:1]:initial-compare
(assert (not (m_panicked formal_0_849)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_849) (select (m_origin formal_0_849) 48) (select (m_origin formal_0_849) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_849) (select (m_origin formal_0_849) 48) (select (m_origin formal_0_849) 77)) false))
; source callback transition phase=insert-tail[45:59:1]:initial-compare
(define-fun formal_0_850 () FormalMachine (FormalCallback formal_0_849 boundary_0 (select (m_origin formal_0_849) 48) (select (m_origin formal_0_849) 77)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:1]
(define-fun formal_0_851 () FormalMachine (FormalWriteFromOrigin formal_0_850 46 77))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:1]
(define-fun formal_0_852 () FormalMachine (FormalWriteFromOrigin formal_0_851 45 48))
; source callback case=recursive-pivot phase=insert-tail[45:59:2]:initial-compare
(assert (not (m_panicked formal_0_852)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_852) (select (m_origin formal_0_852) 30) (select (m_origin formal_0_852) 77)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_852) (select (m_origin formal_0_852) 30) (select (m_origin formal_0_852) 77)) false))
; source callback transition phase=insert-tail[45:59:2]:initial-compare
(define-fun formal_0_853 () FormalMachine (FormalCallback formal_0_852 boundary_0 (select (m_origin formal_0_852) 30) (select (m_origin formal_0_852) 77)))
; source callback case=recursive-pivot phase=insert-tail[45:59:3]:initial-compare
(assert (not (m_panicked formal_0_853)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_853) (select (m_origin formal_0_853) 32) (select (m_origin formal_0_853) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_853) (select (m_origin formal_0_853) 32) (select (m_origin formal_0_853) 30)) false))
; source callback transition phase=insert-tail[45:59:3]:initial-compare
(define-fun formal_0_854 () FormalMachine (FormalCallback formal_0_853 boundary_0 (select (m_origin formal_0_853) 32) (select (m_origin formal_0_853) 30)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:3]
(define-fun formal_0_855 () FormalMachine (FormalWriteFromOrigin formal_0_854 48 30))
; source callback case=recursive-pivot phase=insert-tail[45:59:3]:sift-compare
(assert (not (m_panicked formal_0_855)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_855) (select (m_origin formal_0_855) 32) (select (m_origin formal_0_855) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_855) (select (m_origin formal_0_855) 32) (select (m_origin formal_0_855) 77)) false))
; source callback transition phase=insert-tail[45:59:3]:sift-compare
(define-fun formal_0_856 () FormalMachine (FormalCallback formal_0_855 boundary_0 (select (m_origin formal_0_855) 32) (select (m_origin formal_0_855) 77)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:3]
(define-fun formal_0_857 () FormalMachine (FormalWriteFromOrigin formal_0_856 47 77))
; source callback case=recursive-pivot phase=insert-tail[45:59:3]:sift-compare
(assert (not (m_panicked formal_0_857)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_857) (select (m_origin formal_0_857) 32) (select (m_origin formal_0_857) 48)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_857) (select (m_origin formal_0_857) 32) (select (m_origin formal_0_857) 48)) false))
; source callback transition phase=insert-tail[45:59:3]:sift-compare
(define-fun formal_0_858 () FormalMachine (FormalCallback formal_0_857 boundary_0 (select (m_origin formal_0_857) 32) (select (m_origin formal_0_857) 48)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:3]
(define-fun formal_0_859 () FormalMachine (FormalWriteFromOrigin formal_0_858 46 48))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:3]
(define-fun formal_0_860 () FormalMachine (FormalWriteFromOrigin formal_0_859 45 32))
; source callback case=recursive-pivot phase=insert-tail[45:59:4]:initial-compare
(assert (not (m_panicked formal_0_860)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_860) (select (m_origin formal_0_860) 53) (select (m_origin formal_0_860) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_860) (select (m_origin formal_0_860) 53) (select (m_origin formal_0_860) 30)) false))
; source callback transition phase=insert-tail[45:59:4]:initial-compare
(define-fun formal_0_861 () FormalMachine (FormalCallback formal_0_860 boundary_0 (select (m_origin formal_0_860) 53) (select (m_origin formal_0_860) 30)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:4]
(define-fun formal_0_862 () FormalMachine (FormalWriteFromOrigin formal_0_861 49 30))
; source callback case=recursive-pivot phase=insert-tail[45:59:4]:sift-compare
(assert (not (m_panicked formal_0_862)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_862) (select (m_origin formal_0_862) 53) (select (m_origin formal_0_862) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_862) (select (m_origin formal_0_862) 53) (select (m_origin formal_0_862) 77)) false))
; source callback transition phase=insert-tail[45:59:4]:sift-compare
(define-fun formal_0_863 () FormalMachine (FormalCallback formal_0_862 boundary_0 (select (m_origin formal_0_862) 53) (select (m_origin formal_0_862) 77)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:4]
(define-fun formal_0_864 () FormalMachine (FormalWriteFromOrigin formal_0_863 48 77))
; source callback case=recursive-pivot phase=insert-tail[45:59:4]:sift-compare
(assert (not (m_panicked formal_0_864)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_864) (select (m_origin formal_0_864) 53) (select (m_origin formal_0_864) 48)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_864) (select (m_origin formal_0_864) 53) (select (m_origin formal_0_864) 48)) false))
; source callback transition phase=insert-tail[45:59:4]:sift-compare
(define-fun formal_0_865 () FormalMachine (FormalCallback formal_0_864 boundary_0 (select (m_origin formal_0_864) 53) (select (m_origin formal_0_864) 48)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:4]
(define-fun formal_0_866 () FormalMachine (FormalWriteFromOrigin formal_0_865 47 48))
; source callback case=recursive-pivot phase=insert-tail[45:59:4]:sift-compare
(assert (not (m_panicked formal_0_866)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_866) (select (m_origin formal_0_866) 53) (select (m_origin formal_0_866) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_866) (select (m_origin formal_0_866) 53) (select (m_origin formal_0_866) 32)) false))
; source callback transition phase=insert-tail[45:59:4]:sift-compare
(define-fun formal_0_867 () FormalMachine (FormalCallback formal_0_866 boundary_0 (select (m_origin formal_0_866) 53) (select (m_origin formal_0_866) 32)))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:4]
(define-fun formal_0_868 () FormalMachine (FormalWriteFromOrigin formal_0_867 46 53))
; source callback case=recursive-pivot phase=insert-tail[45:59:5]:initial-compare
(assert (not (m_panicked formal_0_868)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_868) (select (m_origin formal_0_868) 54) (select (m_origin formal_0_868) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_868) (select (m_origin formal_0_868) 54) (select (m_origin formal_0_868) 30)) false))
; source callback transition phase=insert-tail[45:59:5]:initial-compare
(define-fun formal_0_869 () FormalMachine (FormalCallback formal_0_868 boundary_0 (select (m_origin formal_0_868) 54) (select (m_origin formal_0_868) 30)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:5]
(define-fun formal_0_870 () FormalMachine (FormalWriteFromOrigin formal_0_869 50 30))
; source callback case=recursive-pivot phase=insert-tail[45:59:5]:sift-compare
(assert (not (m_panicked formal_0_870)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_870) (select (m_origin formal_0_870) 54) (select (m_origin formal_0_870) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_870) (select (m_origin formal_0_870) 54) (select (m_origin formal_0_870) 77)) false))
; source callback transition phase=insert-tail[45:59:5]:sift-compare
(define-fun formal_0_871 () FormalMachine (FormalCallback formal_0_870 boundary_0 (select (m_origin formal_0_870) 54) (select (m_origin formal_0_870) 77)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:5]
(define-fun formal_0_872 () FormalMachine (FormalWriteFromOrigin formal_0_871 49 77))
; source callback case=recursive-pivot phase=insert-tail[45:59:5]:sift-compare
(assert (not (m_panicked formal_0_872)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_872) (select (m_origin formal_0_872) 54) (select (m_origin formal_0_872) 48)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_872) (select (m_origin formal_0_872) 54) (select (m_origin formal_0_872) 48)) false))
; source callback transition phase=insert-tail[45:59:5]:sift-compare
(define-fun formal_0_873 () FormalMachine (FormalCallback formal_0_872 boundary_0 (select (m_origin formal_0_872) 54) (select (m_origin formal_0_872) 48)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:5]
(define-fun formal_0_874 () FormalMachine (FormalWriteFromOrigin formal_0_873 48 48))
; source callback case=recursive-pivot phase=insert-tail[45:59:5]:sift-compare
(assert (not (m_panicked formal_0_874)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_874) (select (m_origin formal_0_874) 54) (select (m_origin formal_0_874) 53)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_874) (select (m_origin formal_0_874) 54) (select (m_origin formal_0_874) 53)) false))
; source callback transition phase=insert-tail[45:59:5]:sift-compare
(define-fun formal_0_875 () FormalMachine (FormalCallback formal_0_874 boundary_0 (select (m_origin formal_0_874) 54) (select (m_origin formal_0_874) 53)))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:5]
(define-fun formal_0_876 () FormalMachine (FormalWriteFromOrigin formal_0_875 47 54))
; source callback case=recursive-pivot phase=insert-tail[45:59:6]:initial-compare
(assert (not (m_panicked formal_0_876)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_876) (select (m_origin formal_0_876) 46) (select (m_origin formal_0_876) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_876) (select (m_origin formal_0_876) 46) (select (m_origin formal_0_876) 30)) false))
; source callback transition phase=insert-tail[45:59:6]:initial-compare
(define-fun formal_0_877 () FormalMachine (FormalCallback formal_0_876 boundary_0 (select (m_origin formal_0_876) 46) (select (m_origin formal_0_876) 30)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:6]
(define-fun formal_0_878 () FormalMachine (FormalWriteFromOrigin formal_0_877 51 30))
; source callback case=recursive-pivot phase=insert-tail[45:59:6]:sift-compare
(assert (not (m_panicked formal_0_878)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_878) (select (m_origin formal_0_878) 46) (select (m_origin formal_0_878) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_878) (select (m_origin formal_0_878) 46) (select (m_origin formal_0_878) 77)) false))
; source callback transition phase=insert-tail[45:59:6]:sift-compare
(define-fun formal_0_879 () FormalMachine (FormalCallback formal_0_878 boundary_0 (select (m_origin formal_0_878) 46) (select (m_origin formal_0_878) 77)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:6]
(define-fun formal_0_880 () FormalMachine (FormalWriteFromOrigin formal_0_879 50 77))
; source callback case=recursive-pivot phase=insert-tail[45:59:6]:sift-compare
(assert (not (m_panicked formal_0_880)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_880) (select (m_origin formal_0_880) 46) (select (m_origin formal_0_880) 48)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_880) (select (m_origin formal_0_880) 46) (select (m_origin formal_0_880) 48)) false))
; source callback transition phase=insert-tail[45:59:6]:sift-compare
(define-fun formal_0_881 () FormalMachine (FormalCallback formal_0_880 boundary_0 (select (m_origin formal_0_880) 46) (select (m_origin formal_0_880) 48)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:6]
(define-fun formal_0_882 () FormalMachine (FormalWriteFromOrigin formal_0_881 49 48))
; source callback case=recursive-pivot phase=insert-tail[45:59:6]:sift-compare
(assert (not (m_panicked formal_0_882)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_882) (select (m_origin formal_0_882) 46) (select (m_origin formal_0_882) 54)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_882) (select (m_origin formal_0_882) 46) (select (m_origin formal_0_882) 54)) false))
; source callback transition phase=insert-tail[45:59:6]:sift-compare
(define-fun formal_0_883 () FormalMachine (FormalCallback formal_0_882 boundary_0 (select (m_origin formal_0_882) 46) (select (m_origin formal_0_882) 54)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:6]
(define-fun formal_0_884 () FormalMachine (FormalWriteFromOrigin formal_0_883 48 54))
; source callback case=recursive-pivot phase=insert-tail[45:59:6]:sift-compare
(assert (not (m_panicked formal_0_884)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_884) (select (m_origin formal_0_884) 46) (select (m_origin formal_0_884) 53)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_884) (select (m_origin formal_0_884) 46) (select (m_origin formal_0_884) 53)) false))
; source callback transition phase=insert-tail[45:59:6]:sift-compare
(define-fun formal_0_885 () FormalMachine (FormalCallback formal_0_884 boundary_0 (select (m_origin formal_0_884) 46) (select (m_origin formal_0_884) 53)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:6]
(define-fun formal_0_886 () FormalMachine (FormalWriteFromOrigin formal_0_885 47 53))
; source callback case=recursive-pivot phase=insert-tail[45:59:6]:sift-compare
(assert (not (m_panicked formal_0_886)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_886) (select (m_origin formal_0_886) 46) (select (m_origin formal_0_886) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_886) (select (m_origin formal_0_886) 46) (select (m_origin formal_0_886) 32)) false))
; source callback transition phase=insert-tail[45:59:6]:sift-compare
(define-fun formal_0_887 () FormalMachine (FormalCallback formal_0_886 boundary_0 (select (m_origin formal_0_886) 46) (select (m_origin formal_0_886) 32)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:6]
(define-fun formal_0_888 () FormalMachine (FormalWriteFromOrigin formal_0_887 46 32))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:6]
(define-fun formal_0_889 () FormalMachine (FormalWriteFromOrigin formal_0_888 45 46))
; source callback case=recursive-pivot phase=insert-tail[45:59:7]:initial-compare
(assert (not (m_panicked formal_0_889)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_889) (select (m_origin formal_0_889) 60) (select (m_origin formal_0_889) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_889) (select (m_origin formal_0_889) 60) (select (m_origin formal_0_889) 30)) false))
; source callback transition phase=insert-tail[45:59:7]:initial-compare
(define-fun formal_0_890 () FormalMachine (FormalCallback formal_0_889 boundary_0 (select (m_origin formal_0_889) 60) (select (m_origin formal_0_889) 30)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:7]
(define-fun formal_0_891 () FormalMachine (FormalWriteFromOrigin formal_0_890 52 30))
; source callback case=recursive-pivot phase=insert-tail[45:59:7]:sift-compare
(assert (not (m_panicked formal_0_891)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_891) (select (m_origin formal_0_891) 60) (select (m_origin formal_0_891) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_891) (select (m_origin formal_0_891) 60) (select (m_origin formal_0_891) 77)) false))
; source callback transition phase=insert-tail[45:59:7]:sift-compare
(define-fun formal_0_892 () FormalMachine (FormalCallback formal_0_891 boundary_0 (select (m_origin formal_0_891) 60) (select (m_origin formal_0_891) 77)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:7]
(define-fun formal_0_893 () FormalMachine (FormalWriteFromOrigin formal_0_892 51 77))
; source callback case=recursive-pivot phase=insert-tail[45:59:7]:sift-compare
(assert (not (m_panicked formal_0_893)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_893) (select (m_origin formal_0_893) 60) (select (m_origin formal_0_893) 48)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_893) (select (m_origin formal_0_893) 60) (select (m_origin formal_0_893) 48)) false))
; source callback transition phase=insert-tail[45:59:7]:sift-compare
(define-fun formal_0_894 () FormalMachine (FormalCallback formal_0_893 boundary_0 (select (m_origin formal_0_893) 60) (select (m_origin formal_0_893) 48)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:7]
(define-fun formal_0_895 () FormalMachine (FormalWriteFromOrigin formal_0_894 50 48))
; source callback case=recursive-pivot phase=insert-tail[45:59:7]:sift-compare
(assert (not (m_panicked formal_0_895)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_895) (select (m_origin formal_0_895) 60) (select (m_origin formal_0_895) 54)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_895) (select (m_origin formal_0_895) 60) (select (m_origin formal_0_895) 54)) false))
; source callback transition phase=insert-tail[45:59:7]:sift-compare
(define-fun formal_0_896 () FormalMachine (FormalCallback formal_0_895 boundary_0 (select (m_origin formal_0_895) 60) (select (m_origin formal_0_895) 54)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:7]
(define-fun formal_0_897 () FormalMachine (FormalWriteFromOrigin formal_0_896 49 54))
; source callback case=recursive-pivot phase=insert-tail[45:59:7]:sift-compare
(assert (not (m_panicked formal_0_897)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_897) (select (m_origin formal_0_897) 60) (select (m_origin formal_0_897) 53)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_897) (select (m_origin formal_0_897) 60) (select (m_origin formal_0_897) 53)) false))
; source callback transition phase=insert-tail[45:59:7]:sift-compare
(define-fun formal_0_898 () FormalMachine (FormalCallback formal_0_897 boundary_0 (select (m_origin formal_0_897) 60) (select (m_origin formal_0_897) 53)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:7]
(define-fun formal_0_899 () FormalMachine (FormalWriteFromOrigin formal_0_898 48 53))
; source callback case=recursive-pivot phase=insert-tail[45:59:7]:sift-compare
(assert (not (m_panicked formal_0_899)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_899) (select (m_origin formal_0_899) 60) (select (m_origin formal_0_899) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_899) (select (m_origin formal_0_899) 60) (select (m_origin formal_0_899) 32)) false))
; source callback transition phase=insert-tail[45:59:7]:sift-compare
(define-fun formal_0_900 () FormalMachine (FormalCallback formal_0_899 boundary_0 (select (m_origin formal_0_899) 60) (select (m_origin formal_0_899) 32)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:7]
(define-fun formal_0_901 () FormalMachine (FormalWriteFromOrigin formal_0_900 47 32))
; source callback case=recursive-pivot phase=insert-tail[45:59:7]:sift-compare
(assert (not (m_panicked formal_0_901)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_901) (select (m_origin formal_0_901) 60) (select (m_origin formal_0_901) 46)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_901) (select (m_origin formal_0_901) 60) (select (m_origin formal_0_901) 46)) false))
; source callback transition phase=insert-tail[45:59:7]:sift-compare
(define-fun formal_0_902 () FormalMachine (FormalCallback formal_0_901 boundary_0 (select (m_origin formal_0_901) 60) (select (m_origin formal_0_901) 46)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:7]
(define-fun formal_0_903 () FormalMachine (FormalWriteFromOrigin formal_0_902 46 46))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:7]
(define-fun formal_0_904 () FormalMachine (FormalWriteFromOrigin formal_0_903 45 60))
; source callback case=recursive-pivot phase=insert-tail[45:59:8]:initial-compare
(assert (not (m_panicked formal_0_904)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_904) (select (m_origin formal_0_904) 61) (select (m_origin formal_0_904) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_904) (select (m_origin formal_0_904) 61) (select (m_origin formal_0_904) 30)) false))
; source callback transition phase=insert-tail[45:59:8]:initial-compare
(define-fun formal_0_905 () FormalMachine (FormalCallback formal_0_904 boundary_0 (select (m_origin formal_0_904) 61) (select (m_origin formal_0_904) 30)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:8]
(define-fun formal_0_906 () FormalMachine (FormalWriteFromOrigin formal_0_905 53 30))
; source callback case=recursive-pivot phase=insert-tail[45:59:8]:sift-compare
(assert (not (m_panicked formal_0_906)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_906) (select (m_origin formal_0_906) 61) (select (m_origin formal_0_906) 77)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_906) (select (m_origin formal_0_906) 61) (select (m_origin formal_0_906) 77)) false))
; source callback transition phase=insert-tail[45:59:8]:sift-compare
(define-fun formal_0_907 () FormalMachine (FormalCallback formal_0_906 boundary_0 (select (m_origin formal_0_906) 61) (select (m_origin formal_0_906) 77)))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:8]
(define-fun formal_0_908 () FormalMachine (FormalWriteFromOrigin formal_0_907 52 61))
; source callback case=recursive-pivot phase=insert-tail[45:59:9]:initial-compare
(assert (not (m_panicked formal_0_908)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_908) (select (m_origin formal_0_908) 37) (select (m_origin formal_0_908) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_908) (select (m_origin formal_0_908) 37) (select (m_origin formal_0_908) 30)) false))
; source callback transition phase=insert-tail[45:59:9]:initial-compare
(define-fun formal_0_909 () FormalMachine (FormalCallback formal_0_908 boundary_0 (select (m_origin formal_0_908) 37) (select (m_origin formal_0_908) 30)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:9]
(define-fun formal_0_910 () FormalMachine (FormalWriteFromOrigin formal_0_909 54 30))
; source callback case=recursive-pivot phase=insert-tail[45:59:9]:sift-compare
(assert (not (m_panicked formal_0_910)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_910) (select (m_origin formal_0_910) 37) (select (m_origin formal_0_910) 61)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_910) (select (m_origin formal_0_910) 37) (select (m_origin formal_0_910) 61)) false))
; source callback transition phase=insert-tail[45:59:9]:sift-compare
(define-fun formal_0_911 () FormalMachine (FormalCallback formal_0_910 boundary_0 (select (m_origin formal_0_910) 37) (select (m_origin formal_0_910) 61)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:9]
(define-fun formal_0_912 () FormalMachine (FormalWriteFromOrigin formal_0_911 53 61))
; source callback case=recursive-pivot phase=insert-tail[45:59:9]:sift-compare
(assert (not (m_panicked formal_0_912)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_912) (select (m_origin formal_0_912) 37) (select (m_origin formal_0_912) 77)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_912) (select (m_origin formal_0_912) 37) (select (m_origin formal_0_912) 77)) false))
; source callback transition phase=insert-tail[45:59:9]:sift-compare
(define-fun formal_0_913 () FormalMachine (FormalCallback formal_0_912 boundary_0 (select (m_origin formal_0_912) 37) (select (m_origin formal_0_912) 77)))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:9]
(define-fun formal_0_914 () FormalMachine (FormalWriteFromOrigin formal_0_913 52 37))
; source callback case=recursive-pivot phase=insert-tail[45:59:10]:initial-compare
(assert (not (m_panicked formal_0_914)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_914) (select (m_origin formal_0_914) 24) (select (m_origin formal_0_914) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_914) (select (m_origin formal_0_914) 24) (select (m_origin formal_0_914) 30)) false))
; source callback transition phase=insert-tail[45:59:10]:initial-compare
(define-fun formal_0_915 () FormalMachine (FormalCallback formal_0_914 boundary_0 (select (m_origin formal_0_914) 24) (select (m_origin formal_0_914) 30)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:10]
(define-fun formal_0_916 () FormalMachine (FormalWriteFromOrigin formal_0_915 55 30))
; source callback case=recursive-pivot phase=insert-tail[45:59:10]:sift-compare
(assert (not (m_panicked formal_0_916)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_916) (select (m_origin formal_0_916) 24) (select (m_origin formal_0_916) 61)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_916) (select (m_origin formal_0_916) 24) (select (m_origin formal_0_916) 61)) false))
; source callback transition phase=insert-tail[45:59:10]:sift-compare
(define-fun formal_0_917 () FormalMachine (FormalCallback formal_0_916 boundary_0 (select (m_origin formal_0_916) 24) (select (m_origin formal_0_916) 61)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:10]
(define-fun formal_0_918 () FormalMachine (FormalWriteFromOrigin formal_0_917 54 61))
; source callback case=recursive-pivot phase=insert-tail[45:59:10]:sift-compare
(assert (not (m_panicked formal_0_918)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_918) (select (m_origin formal_0_918) 24) (select (m_origin formal_0_918) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_918) (select (m_origin formal_0_918) 24) (select (m_origin formal_0_918) 37)) false))
; source callback transition phase=insert-tail[45:59:10]:sift-compare
(define-fun formal_0_919 () FormalMachine (FormalCallback formal_0_918 boundary_0 (select (m_origin formal_0_918) 24) (select (m_origin formal_0_918) 37)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:10]
(define-fun formal_0_920 () FormalMachine (FormalWriteFromOrigin formal_0_919 53 37))
; source callback case=recursive-pivot phase=insert-tail[45:59:10]:sift-compare
(assert (not (m_panicked formal_0_920)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_920) (select (m_origin formal_0_920) 24) (select (m_origin formal_0_920) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_920) (select (m_origin formal_0_920) 24) (select (m_origin formal_0_920) 77)) false))
; source callback transition phase=insert-tail[45:59:10]:sift-compare
(define-fun formal_0_921 () FormalMachine (FormalCallback formal_0_920 boundary_0 (select (m_origin formal_0_920) 24) (select (m_origin formal_0_920) 77)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:10]
(define-fun formal_0_922 () FormalMachine (FormalWriteFromOrigin formal_0_921 52 77))
; source callback case=recursive-pivot phase=insert-tail[45:59:10]:sift-compare
(assert (not (m_panicked formal_0_922)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_922) (select (m_origin formal_0_922) 24) (select (m_origin formal_0_922) 48)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_922) (select (m_origin formal_0_922) 24) (select (m_origin formal_0_922) 48)) false))
; source callback transition phase=insert-tail[45:59:10]:sift-compare
(define-fun formal_0_923 () FormalMachine (FormalCallback formal_0_922 boundary_0 (select (m_origin formal_0_922) 24) (select (m_origin formal_0_922) 48)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:10]
(define-fun formal_0_924 () FormalMachine (FormalWriteFromOrigin formal_0_923 51 48))
; source callback case=recursive-pivot phase=insert-tail[45:59:10]:sift-compare
(assert (not (m_panicked formal_0_924)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_924) (select (m_origin formal_0_924) 24) (select (m_origin formal_0_924) 54)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_924) (select (m_origin formal_0_924) 24) (select (m_origin formal_0_924) 54)) false))
; source callback transition phase=insert-tail[45:59:10]:sift-compare
(define-fun formal_0_925 () FormalMachine (FormalCallback formal_0_924 boundary_0 (select (m_origin formal_0_924) 24) (select (m_origin formal_0_924) 54)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:10]
(define-fun formal_0_926 () FormalMachine (FormalWriteFromOrigin formal_0_925 50 54))
; source callback case=recursive-pivot phase=insert-tail[45:59:10]:sift-compare
(assert (not (m_panicked formal_0_926)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_926) (select (m_origin formal_0_926) 24) (select (m_origin formal_0_926) 53)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_926) (select (m_origin formal_0_926) 24) (select (m_origin formal_0_926) 53)) false))
; source callback transition phase=insert-tail[45:59:10]:sift-compare
(define-fun formal_0_927 () FormalMachine (FormalCallback formal_0_926 boundary_0 (select (m_origin formal_0_926) 24) (select (m_origin formal_0_926) 53)))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:10]
(define-fun formal_0_928 () FormalMachine (FormalWriteFromOrigin formal_0_927 49 24))
; source callback case=recursive-pivot phase=insert-tail[45:59:11]:initial-compare
(assert (not (m_panicked formal_0_928)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_928) (select (m_origin formal_0_928) 18) (select (m_origin formal_0_928) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_928) (select (m_origin formal_0_928) 18) (select (m_origin formal_0_928) 30)) false))
; source callback transition phase=insert-tail[45:59:11]:initial-compare
(define-fun formal_0_929 () FormalMachine (FormalCallback formal_0_928 boundary_0 (select (m_origin formal_0_928) 18) (select (m_origin formal_0_928) 30)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:11]
(define-fun formal_0_930 () FormalMachine (FormalWriteFromOrigin formal_0_929 56 30))
; source callback case=recursive-pivot phase=insert-tail[45:59:11]:sift-compare
(assert (not (m_panicked formal_0_930)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_930) (select (m_origin formal_0_930) 18) (select (m_origin formal_0_930) 61)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_930) (select (m_origin formal_0_930) 18) (select (m_origin formal_0_930) 61)) false))
; source callback transition phase=insert-tail[45:59:11]:sift-compare
(define-fun formal_0_931 () FormalMachine (FormalCallback formal_0_930 boundary_0 (select (m_origin formal_0_930) 18) (select (m_origin formal_0_930) 61)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:11]
(define-fun formal_0_932 () FormalMachine (FormalWriteFromOrigin formal_0_931 55 61))
; source callback case=recursive-pivot phase=insert-tail[45:59:11]:sift-compare
(assert (not (m_panicked formal_0_932)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_932) (select (m_origin formal_0_932) 18) (select (m_origin formal_0_932) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_932) (select (m_origin formal_0_932) 18) (select (m_origin formal_0_932) 37)) false))
; source callback transition phase=insert-tail[45:59:11]:sift-compare
(define-fun formal_0_933 () FormalMachine (FormalCallback formal_0_932 boundary_0 (select (m_origin formal_0_932) 18) (select (m_origin formal_0_932) 37)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:11]
(define-fun formal_0_934 () FormalMachine (FormalWriteFromOrigin formal_0_933 54 37))
; source callback case=recursive-pivot phase=insert-tail[45:59:11]:sift-compare
(assert (not (m_panicked formal_0_934)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_934) (select (m_origin formal_0_934) 18) (select (m_origin formal_0_934) 77)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_934) (select (m_origin formal_0_934) 18) (select (m_origin formal_0_934) 77)) false))
; source callback transition phase=insert-tail[45:59:11]:sift-compare
(define-fun formal_0_935 () FormalMachine (FormalCallback formal_0_934 boundary_0 (select (m_origin formal_0_934) 18) (select (m_origin formal_0_934) 77)))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:11]
(define-fun formal_0_936 () FormalMachine (FormalWriteFromOrigin formal_0_935 53 18))
; source callback case=recursive-pivot phase=insert-tail[45:59:12]:initial-compare
(assert (not (m_panicked formal_0_936)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_936) (select (m_origin formal_0_936) 71) (select (m_origin formal_0_936) 30)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_936) (select (m_origin formal_0_936) 71) (select (m_origin formal_0_936) 30)) false))
; source callback transition phase=insert-tail[45:59:12]:initial-compare
(define-fun formal_0_937 () FormalMachine (FormalCallback formal_0_936 boundary_0 (select (m_origin formal_0_936) 71) (select (m_origin formal_0_936) 30)))
; source callback case=recursive-pivot phase=insert-tail[45:59:13]:initial-compare
(assert (not (m_panicked formal_0_937)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_937) (select (m_origin formal_0_937) 75) (select (m_origin formal_0_937) 71)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_937) (select (m_origin formal_0_937) 75) (select (m_origin formal_0_937) 71)) false))
; source callback transition phase=insert-tail[45:59:13]:initial-compare
(define-fun formal_0_938 () FormalMachine (FormalCallback formal_0_937 boundary_0 (select (m_origin formal_0_937) 75) (select (m_origin formal_0_937) 71)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:13]
(define-fun formal_0_939 () FormalMachine (FormalWriteFromOrigin formal_0_938 58 71))
; source callback case=recursive-pivot phase=insert-tail[45:59:13]:sift-compare
(assert (not (m_panicked formal_0_939)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_939) (select (m_origin formal_0_939) 75) (select (m_origin formal_0_939) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_939) (select (m_origin formal_0_939) 75) (select (m_origin formal_0_939) 30)) false))
; source callback transition phase=insert-tail[45:59:13]:sift-compare
(define-fun formal_0_940 () FormalMachine (FormalCallback formal_0_939 boundary_0 (select (m_origin formal_0_939) 75) (select (m_origin formal_0_939) 30)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:13]
(define-fun formal_0_941 () FormalMachine (FormalWriteFromOrigin formal_0_940 57 30))
; source callback case=recursive-pivot phase=insert-tail[45:59:13]:sift-compare
(assert (not (m_panicked formal_0_941)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_941) (select (m_origin formal_0_941) 75) (select (m_origin formal_0_941) 61)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_941) (select (m_origin formal_0_941) 75) (select (m_origin formal_0_941) 61)) false))
; source callback transition phase=insert-tail[45:59:13]:sift-compare
(define-fun formal_0_942 () FormalMachine (FormalCallback formal_0_941 boundary_0 (select (m_origin formal_0_941) 75) (select (m_origin formal_0_941) 61)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:13]
(define-fun formal_0_943 () FormalMachine (FormalWriteFromOrigin formal_0_942 56 61))
; source callback case=recursive-pivot phase=insert-tail[45:59:13]:sift-compare
(assert (not (m_panicked formal_0_943)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_943) (select (m_origin formal_0_943) 75) (select (m_origin formal_0_943) 37)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_943) (select (m_origin formal_0_943) 75) (select (m_origin formal_0_943) 37)) false))
; source callback transition phase=insert-tail[45:59:13]:sift-compare
(define-fun formal_0_944 () FormalMachine (FormalCallback formal_0_943 boundary_0 (select (m_origin formal_0_943) 75) (select (m_origin formal_0_943) 37)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:13]
(define-fun formal_0_945 () FormalMachine (FormalWriteFromOrigin formal_0_944 55 37))
; source callback case=recursive-pivot phase=insert-tail[45:59:13]:sift-compare
(assert (not (m_panicked formal_0_945)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_945) (select (m_origin formal_0_945) 75) (select (m_origin formal_0_945) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_945) (select (m_origin formal_0_945) 75) (select (m_origin formal_0_945) 18)) false))
; source callback transition phase=insert-tail[45:59:13]:sift-compare
(define-fun formal_0_946 () FormalMachine (FormalCallback formal_0_945 boundary_0 (select (m_origin formal_0_945) 75) (select (m_origin formal_0_945) 18)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:13]
(define-fun formal_0_947 () FormalMachine (FormalWriteFromOrigin formal_0_946 54 18))
; source callback case=recursive-pivot phase=insert-tail[45:59:13]:sift-compare
(assert (not (m_panicked formal_0_947)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_947) (select (m_origin formal_0_947) 75) (select (m_origin formal_0_947) 77)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_947) (select (m_origin formal_0_947) 75) (select (m_origin formal_0_947) 77)) false))
; source callback transition phase=insert-tail[45:59:13]:sift-compare
(define-fun formal_0_948 () FormalMachine (FormalCallback formal_0_947 boundary_0 (select (m_origin formal_0_947) 75) (select (m_origin formal_0_947) 77)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:13]
(define-fun formal_0_949 () FormalMachine (FormalWriteFromOrigin formal_0_948 53 77))
; source callback case=recursive-pivot phase=insert-tail[45:59:13]:sift-compare
(assert (not (m_panicked formal_0_949)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_949) (select (m_origin formal_0_949) 75) (select (m_origin formal_0_949) 48)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_949) (select (m_origin formal_0_949) 75) (select (m_origin formal_0_949) 48)) false))
; source callback transition phase=insert-tail[45:59:13]:sift-compare
(define-fun formal_0_950 () FormalMachine (FormalCallback formal_0_949 boundary_0 (select (m_origin formal_0_949) 75) (select (m_origin formal_0_949) 48)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:13]
(define-fun formal_0_951 () FormalMachine (FormalWriteFromOrigin formal_0_950 52 48))
; source callback case=recursive-pivot phase=insert-tail[45:59:13]:sift-compare
(assert (not (m_panicked formal_0_951)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_951) (select (m_origin formal_0_951) 75) (select (m_origin formal_0_951) 54)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_951) (select (m_origin formal_0_951) 75) (select (m_origin formal_0_951) 54)) false))
; source callback transition phase=insert-tail[45:59:13]:sift-compare
(define-fun formal_0_952 () FormalMachine (FormalCallback formal_0_951 boundary_0 (select (m_origin formal_0_951) 75) (select (m_origin formal_0_951) 54)))
; source write kind=insert-tail-shift phase=insert-tail[45:59:13]
(define-fun formal_0_953 () FormalMachine (FormalWriteFromOrigin formal_0_952 51 54))
; source callback case=recursive-pivot phase=insert-tail[45:59:13]:sift-compare
(assert (not (m_panicked formal_0_953)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_953) (select (m_origin formal_0_953) 75) (select (m_origin formal_0_953) 24)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_953) (select (m_origin formal_0_953) 75) (select (m_origin formal_0_953) 24)) false))
; source callback transition phase=insert-tail[45:59:13]:sift-compare
(define-fun formal_0_954 () FormalMachine (FormalCallback formal_0_953 boundary_0 (select (m_origin formal_0_953) 75) (select (m_origin formal_0_953) 24)))
; source write kind=copy-on-drop-restore phase=insert-tail[45:59:13]
(define-fun formal_0_955 () FormalMachine (FormalWriteFromOrigin formal_0_954 50 75))
; source callback case=recursive-pivot phase=insert-tail[60:68:1]:initial-compare
(assert (not (m_panicked formal_0_955)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_955) (select (m_origin formal_0_955) 13) (select (m_origin formal_0_955) 19)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_955) (select (m_origin formal_0_955) 13) (select (m_origin formal_0_955) 19)) false))
; source callback transition phase=insert-tail[60:68:1]:initial-compare
(define-fun formal_0_956 () FormalMachine (FormalCallback formal_0_955 boundary_0 (select (m_origin formal_0_955) 13) (select (m_origin formal_0_955) 19)))
; source callback case=recursive-pivot phase=insert-tail[60:68:2]:initial-compare
(assert (not (m_panicked formal_0_956)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_956) (select (m_origin formal_0_956) 42) (select (m_origin formal_0_956) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_956) (select (m_origin formal_0_956) 42) (select (m_origin formal_0_956) 13)) false))
; source callback transition phase=insert-tail[60:68:2]:initial-compare
(define-fun formal_0_957 () FormalMachine (FormalCallback formal_0_956 boundary_0 (select (m_origin formal_0_956) 42) (select (m_origin formal_0_956) 13)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:2]
(define-fun formal_0_958 () FormalMachine (FormalWriteFromOrigin formal_0_957 62 13))
; source callback case=recursive-pivot phase=insert-tail[60:68:2]:sift-compare
(assert (not (m_panicked formal_0_958)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_958) (select (m_origin formal_0_958) 42) (select (m_origin formal_0_958) 19)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_958) (select (m_origin formal_0_958) 42) (select (m_origin formal_0_958) 19)) false))
; source callback transition phase=insert-tail[60:68:2]:sift-compare
(define-fun formal_0_959 () FormalMachine (FormalCallback formal_0_958 boundary_0 (select (m_origin formal_0_958) 42) (select (m_origin formal_0_958) 19)))
; source write kind=copy-on-drop-restore phase=insert-tail[60:68:2]
(define-fun formal_0_960 () FormalMachine (FormalWriteFromOrigin formal_0_959 61 42))
; source callback case=recursive-pivot phase=insert-tail[60:68:3]:initial-compare
(assert (not (m_panicked formal_0_960)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_960) (select (m_origin formal_0_960) 59) (select (m_origin formal_0_960) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_960) (select (m_origin formal_0_960) 59) (select (m_origin formal_0_960) 13)) false))
; source callback transition phase=insert-tail[60:68:3]:initial-compare
(define-fun formal_0_961 () FormalMachine (FormalCallback formal_0_960 boundary_0 (select (m_origin formal_0_960) 59) (select (m_origin formal_0_960) 13)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:3]
(define-fun formal_0_962 () FormalMachine (FormalWriteFromOrigin formal_0_961 63 13))
; source callback case=recursive-pivot phase=insert-tail[60:68:3]:sift-compare
(assert (not (m_panicked formal_0_962)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_962) (select (m_origin formal_0_962) 59) (select (m_origin formal_0_962) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_962) (select (m_origin formal_0_962) 59) (select (m_origin formal_0_962) 42)) false))
; source callback transition phase=insert-tail[60:68:3]:sift-compare
(define-fun formal_0_963 () FormalMachine (FormalCallback formal_0_962 boundary_0 (select (m_origin formal_0_962) 59) (select (m_origin formal_0_962) 42)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:3]
(define-fun formal_0_964 () FormalMachine (FormalWriteFromOrigin formal_0_963 62 42))
; source callback case=recursive-pivot phase=insert-tail[60:68:3]:sift-compare
(assert (not (m_panicked formal_0_964)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_964) (select (m_origin formal_0_964) 59) (select (m_origin formal_0_964) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_964) (select (m_origin formal_0_964) 59) (select (m_origin formal_0_964) 19)) false))
; source callback transition phase=insert-tail[60:68:3]:sift-compare
(define-fun formal_0_965 () FormalMachine (FormalCallback formal_0_964 boundary_0 (select (m_origin formal_0_964) 59) (select (m_origin formal_0_964) 19)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:3]
(define-fun formal_0_966 () FormalMachine (FormalWriteFromOrigin formal_0_965 61 19))
; source write kind=copy-on-drop-restore phase=insert-tail[60:68:3]
(define-fun formal_0_967 () FormalMachine (FormalWriteFromOrigin formal_0_966 60 59))
; source callback case=recursive-pivot phase=insert-tail[60:68:4]:initial-compare
(assert (not (m_panicked formal_0_967)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_967) (select (m_origin formal_0_967) 65) (select (m_origin formal_0_967) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_967) (select (m_origin formal_0_967) 65) (select (m_origin formal_0_967) 13)) false))
; source callback transition phase=insert-tail[60:68:4]:initial-compare
(define-fun formal_0_968 () FormalMachine (FormalCallback formal_0_967 boundary_0 (select (m_origin formal_0_967) 65) (select (m_origin formal_0_967) 13)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:4]
(define-fun formal_0_969 () FormalMachine (FormalWriteFromOrigin formal_0_968 64 13))
; source callback case=recursive-pivot phase=insert-tail[60:68:4]:sift-compare
(assert (not (m_panicked formal_0_969)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_969) (select (m_origin formal_0_969) 65) (select (m_origin formal_0_969) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_969) (select (m_origin formal_0_969) 65) (select (m_origin formal_0_969) 42)) false))
; source callback transition phase=insert-tail[60:68:4]:sift-compare
(define-fun formal_0_970 () FormalMachine (FormalCallback formal_0_969 boundary_0 (select (m_origin formal_0_969) 65) (select (m_origin formal_0_969) 42)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:4]
(define-fun formal_0_971 () FormalMachine (FormalWriteFromOrigin formal_0_970 63 42))
; source callback case=recursive-pivot phase=insert-tail[60:68:4]:sift-compare
(assert (not (m_panicked formal_0_971)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_971) (select (m_origin formal_0_971) 65) (select (m_origin formal_0_971) 19)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_971) (select (m_origin formal_0_971) 65) (select (m_origin formal_0_971) 19)) false))
; source callback transition phase=insert-tail[60:68:4]:sift-compare
(define-fun formal_0_972 () FormalMachine (FormalCallback formal_0_971 boundary_0 (select (m_origin formal_0_971) 65) (select (m_origin formal_0_971) 19)))
; source write kind=copy-on-drop-restore phase=insert-tail[60:68:4]
(define-fun formal_0_973 () FormalMachine (FormalWriteFromOrigin formal_0_972 62 65))
; source callback case=recursive-pivot phase=insert-tail[60:68:5]:initial-compare
(assert (not (m_panicked formal_0_973)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_973) (select (m_origin formal_0_973) 76) (select (m_origin formal_0_973) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_973) (select (m_origin formal_0_973) 76) (select (m_origin formal_0_973) 13)) false))
; source callback transition phase=insert-tail[60:68:5]:initial-compare
(define-fun formal_0_974 () FormalMachine (FormalCallback formal_0_973 boundary_0 (select (m_origin formal_0_973) 76) (select (m_origin formal_0_973) 13)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:5]
(define-fun formal_0_975 () FormalMachine (FormalWriteFromOrigin formal_0_974 65 13))
; source callback case=recursive-pivot phase=insert-tail[60:68:5]:sift-compare
(assert (not (m_panicked formal_0_975)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_975) (select (m_origin formal_0_975) 76) (select (m_origin formal_0_975) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_975) (select (m_origin formal_0_975) 76) (select (m_origin formal_0_975) 42)) false))
; source callback transition phase=insert-tail[60:68:5]:sift-compare
(define-fun formal_0_976 () FormalMachine (FormalCallback formal_0_975 boundary_0 (select (m_origin formal_0_975) 76) (select (m_origin formal_0_975) 42)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:5]
(define-fun formal_0_977 () FormalMachine (FormalWriteFromOrigin formal_0_976 64 42))
; source callback case=recursive-pivot phase=insert-tail[60:68:5]:sift-compare
(assert (not (m_panicked formal_0_977)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_977) (select (m_origin formal_0_977) 76) (select (m_origin formal_0_977) 65)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_977) (select (m_origin formal_0_977) 76) (select (m_origin formal_0_977) 65)) false))
; source callback transition phase=insert-tail[60:68:5]:sift-compare
(define-fun formal_0_978 () FormalMachine (FormalCallback formal_0_977 boundary_0 (select (m_origin formal_0_977) 76) (select (m_origin formal_0_977) 65)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:5]
(define-fun formal_0_979 () FormalMachine (FormalWriteFromOrigin formal_0_978 63 65))
; source callback case=recursive-pivot phase=insert-tail[60:68:5]:sift-compare
(assert (not (m_panicked formal_0_979)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_979) (select (m_origin formal_0_979) 76) (select (m_origin formal_0_979) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_979) (select (m_origin formal_0_979) 76) (select (m_origin formal_0_979) 19)) false))
; source callback transition phase=insert-tail[60:68:5]:sift-compare
(define-fun formal_0_980 () FormalMachine (FormalCallback formal_0_979 boundary_0 (select (m_origin formal_0_979) 76) (select (m_origin formal_0_979) 19)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:5]
(define-fun formal_0_981 () FormalMachine (FormalWriteFromOrigin formal_0_980 62 19))
; source callback case=recursive-pivot phase=insert-tail[60:68:5]:sift-compare
(assert (not (m_panicked formal_0_981)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_981) (select (m_origin formal_0_981) 76) (select (m_origin formal_0_981) 59)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_981) (select (m_origin formal_0_981) 76) (select (m_origin formal_0_981) 59)) false))
; source callback transition phase=insert-tail[60:68:5]:sift-compare
(define-fun formal_0_982 () FormalMachine (FormalCallback formal_0_981 boundary_0 (select (m_origin formal_0_981) 76) (select (m_origin formal_0_981) 59)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:5]
(define-fun formal_0_983 () FormalMachine (FormalWriteFromOrigin formal_0_982 61 59))
; source write kind=copy-on-drop-restore phase=insert-tail[60:68:5]
(define-fun formal_0_984 () FormalMachine (FormalWriteFromOrigin formal_0_983 60 76))
; source callback case=recursive-pivot phase=insert-tail[60:68:6]:initial-compare
(assert (not (m_panicked formal_0_984)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_984) (select (m_origin formal_0_984) 68) (select (m_origin formal_0_984) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_984) (select (m_origin formal_0_984) 68) (select (m_origin formal_0_984) 13)) false))
; source callback transition phase=insert-tail[60:68:6]:initial-compare
(define-fun formal_0_985 () FormalMachine (FormalCallback formal_0_984 boundary_0 (select (m_origin formal_0_984) 68) (select (m_origin formal_0_984) 13)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:6]
(define-fun formal_0_986 () FormalMachine (FormalWriteFromOrigin formal_0_985 66 13))
; source callback case=recursive-pivot phase=insert-tail[60:68:6]:sift-compare
(assert (not (m_panicked formal_0_986)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_986) (select (m_origin formal_0_986) 68) (select (m_origin formal_0_986) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_986) (select (m_origin formal_0_986) 68) (select (m_origin formal_0_986) 42)) false))
; source callback transition phase=insert-tail[60:68:6]:sift-compare
(define-fun formal_0_987 () FormalMachine (FormalCallback formal_0_986 boundary_0 (select (m_origin formal_0_986) 68) (select (m_origin formal_0_986) 42)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:6]
(define-fun formal_0_988 () FormalMachine (FormalWriteFromOrigin formal_0_987 65 42))
; source callback case=recursive-pivot phase=insert-tail[60:68:6]:sift-compare
(assert (not (m_panicked formal_0_988)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_988) (select (m_origin formal_0_988) 68) (select (m_origin formal_0_988) 65)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_988) (select (m_origin formal_0_988) 68) (select (m_origin formal_0_988) 65)) false))
; source callback transition phase=insert-tail[60:68:6]:sift-compare
(define-fun formal_0_989 () FormalMachine (FormalCallback formal_0_988 boundary_0 (select (m_origin formal_0_988) 68) (select (m_origin formal_0_988) 65)))
; source write kind=copy-on-drop-restore phase=insert-tail[60:68:6]
(define-fun formal_0_990 () FormalMachine (FormalWriteFromOrigin formal_0_989 64 68))
; source callback case=recursive-pivot phase=insert-tail[60:68:7]:initial-compare
(assert (not (m_panicked formal_0_990)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_990) (select (m_origin formal_0_990) 78) (select (m_origin formal_0_990) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_990) (select (m_origin formal_0_990) 78) (select (m_origin formal_0_990) 13)) false))
; source callback transition phase=insert-tail[60:68:7]:initial-compare
(define-fun formal_0_991 () FormalMachine (FormalCallback formal_0_990 boundary_0 (select (m_origin formal_0_990) 78) (select (m_origin formal_0_990) 13)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:7]
(define-fun formal_0_992 () FormalMachine (FormalWriteFromOrigin formal_0_991 67 13))
; source callback case=recursive-pivot phase=insert-tail[60:68:7]:sift-compare
(assert (not (m_panicked formal_0_992)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_992) (select (m_origin formal_0_992) 78) (select (m_origin formal_0_992) 42)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_992) (select (m_origin formal_0_992) 78) (select (m_origin formal_0_992) 42)) false))
; source callback transition phase=insert-tail[60:68:7]:sift-compare
(define-fun formal_0_993 () FormalMachine (FormalCallback formal_0_992 boundary_0 (select (m_origin formal_0_992) 78) (select (m_origin formal_0_992) 42)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:7]
(define-fun formal_0_994 () FormalMachine (FormalWriteFromOrigin formal_0_993 66 42))
; source callback case=recursive-pivot phase=insert-tail[60:68:7]:sift-compare
(assert (not (m_panicked formal_0_994)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_994) (select (m_origin formal_0_994) 78) (select (m_origin formal_0_994) 68)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_994) (select (m_origin formal_0_994) 78) (select (m_origin formal_0_994) 68)) false))
; source callback transition phase=insert-tail[60:68:7]:sift-compare
(define-fun formal_0_995 () FormalMachine (FormalCallback formal_0_994 boundary_0 (select (m_origin formal_0_994) 78) (select (m_origin formal_0_994) 68)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:7]
(define-fun formal_0_996 () FormalMachine (FormalWriteFromOrigin formal_0_995 65 68))
; source callback case=recursive-pivot phase=insert-tail[60:68:7]:sift-compare
(assert (not (m_panicked formal_0_996)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_996) (select (m_origin formal_0_996) 78) (select (m_origin formal_0_996) 65)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_996) (select (m_origin formal_0_996) 78) (select (m_origin formal_0_996) 65)) false))
; source callback transition phase=insert-tail[60:68:7]:sift-compare
(define-fun formal_0_997 () FormalMachine (FormalCallback formal_0_996 boundary_0 (select (m_origin formal_0_996) 78) (select (m_origin formal_0_996) 65)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:7]
(define-fun formal_0_998 () FormalMachine (FormalWriteFromOrigin formal_0_997 64 65))
; source callback case=recursive-pivot phase=insert-tail[60:68:7]:sift-compare
(assert (not (m_panicked formal_0_998)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_998) (select (m_origin formal_0_998) 78) (select (m_origin formal_0_998) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_998) (select (m_origin formal_0_998) 78) (select (m_origin formal_0_998) 19)) false))
; source callback transition phase=insert-tail[60:68:7]:sift-compare
(define-fun formal_0_999 () FormalMachine (FormalCallback formal_0_998 boundary_0 (select (m_origin formal_0_998) 78) (select (m_origin formal_0_998) 19)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:7]
(define-fun formal_0_1000 () FormalMachine (FormalWriteFromOrigin formal_0_999 63 19))
; source callback case=recursive-pivot phase=insert-tail[60:68:7]:sift-compare
(assert (not (m_panicked formal_0_1000)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1000) (select (m_origin formal_0_1000) 78) (select (m_origin formal_0_1000) 59)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1000) (select (m_origin formal_0_1000) 78) (select (m_origin formal_0_1000) 59)) false))
; source callback transition phase=insert-tail[60:68:7]:sift-compare
(define-fun formal_0_1001 () FormalMachine (FormalCallback formal_0_1000 boundary_0 (select (m_origin formal_0_1000) 78) (select (m_origin formal_0_1000) 59)))
; source write kind=insert-tail-shift phase=insert-tail[60:68:7]
(define-fun formal_0_1002 () FormalMachine (FormalWriteFromOrigin formal_0_1001 62 59))
; source callback case=recursive-pivot phase=insert-tail[60:68:7]:sift-compare
(assert (not (m_panicked formal_0_1002)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1002) (select (m_origin formal_0_1002) 78) (select (m_origin formal_0_1002) 76)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1002) (select (m_origin formal_0_1002) 78) (select (m_origin formal_0_1002) 76)) false))
; source callback transition phase=insert-tail[60:68:7]:sift-compare
(define-fun formal_0_1003 () FormalMachine (FormalCallback formal_0_1002 boundary_0 (select (m_origin formal_0_1002) 78) (select (m_origin formal_0_1002) 76)))
; source write kind=copy-on-drop-restore phase=insert-tail[60:68:7]
(define-fun formal_0_1004 () FormalMachine (FormalWriteFromOrigin formal_0_1003 61 78))
; source callback case=recursive-pivot phase=insert-tail[69:80:1]:initial-compare
(assert (not (m_panicked formal_0_1004)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1004) (select (m_origin formal_0_1004) 7) (select (m_origin formal_0_1004) 5)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1004) (select (m_origin formal_0_1004) 7) (select (m_origin formal_0_1004) 5)) false))
; source callback transition phase=insert-tail[69:80:1]:initial-compare
(define-fun formal_0_1005 () FormalMachine (FormalCallback formal_0_1004 boundary_0 (select (m_origin formal_0_1004) 7) (select (m_origin formal_0_1004) 5)))
; source callback case=recursive-pivot phase=insert-tail[69:80:2]:initial-compare
(assert (not (m_panicked formal_0_1005)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1005) (select (m_origin formal_0_1005) 6) (select (m_origin formal_0_1005) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1005) (select (m_origin formal_0_1005) 6) (select (m_origin formal_0_1005) 7)) false))
; source callback transition phase=insert-tail[69:80:2]:initial-compare
(define-fun formal_0_1006 () FormalMachine (FormalCallback formal_0_1005 boundary_0 (select (m_origin formal_0_1005) 6) (select (m_origin formal_0_1005) 7)))
; source callback case=recursive-pivot phase=insert-tail[69:80:3]:initial-compare
(assert (not (m_panicked formal_0_1006)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1006) (select (m_origin formal_0_1006) 72) (select (m_origin formal_0_1006) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1006) (select (m_origin formal_0_1006) 72) (select (m_origin formal_0_1006) 6)) false))
; source callback transition phase=insert-tail[69:80:3]:initial-compare
(define-fun formal_0_1007 () FormalMachine (FormalCallback formal_0_1006 boundary_0 (select (m_origin formal_0_1006) 72) (select (m_origin formal_0_1006) 6)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:3]
(define-fun formal_0_1008 () FormalMachine (FormalWriteFromOrigin formal_0_1007 72 6))
; source callback case=recursive-pivot phase=insert-tail[69:80:3]:sift-compare
(assert (not (m_panicked formal_0_1008)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1008) (select (m_origin formal_0_1008) 72) (select (m_origin formal_0_1008) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1008) (select (m_origin formal_0_1008) 72) (select (m_origin formal_0_1008) 7)) false))
; source callback transition phase=insert-tail[69:80:3]:sift-compare
(define-fun formal_0_1009 () FormalMachine (FormalCallback formal_0_1008 boundary_0 (select (m_origin formal_0_1008) 72) (select (m_origin formal_0_1008) 7)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:3]
(define-fun formal_0_1010 () FormalMachine (FormalWriteFromOrigin formal_0_1009 71 7))
; source callback case=recursive-pivot phase=insert-tail[69:80:3]:sift-compare
(assert (not (m_panicked formal_0_1010)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1010) (select (m_origin formal_0_1010) 72) (select (m_origin formal_0_1010) 5)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1010) (select (m_origin formal_0_1010) 72) (select (m_origin formal_0_1010) 5)) false))
; source callback transition phase=insert-tail[69:80:3]:sift-compare
(define-fun formal_0_1011 () FormalMachine (FormalCallback formal_0_1010 boundary_0 (select (m_origin formal_0_1010) 72) (select (m_origin formal_0_1010) 5)))
; source write kind=copy-on-drop-restore phase=insert-tail[69:80:3]
(define-fun formal_0_1012 () FormalMachine (FormalWriteFromOrigin formal_0_1011 70 72))
; source callback case=recursive-pivot phase=insert-tail[69:80:4]:initial-compare
(assert (not (m_panicked formal_0_1012)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1012) (select (m_origin formal_0_1012) 43) (select (m_origin formal_0_1012) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1012) (select (m_origin formal_0_1012) 43) (select (m_origin formal_0_1012) 6)) false))
; source callback transition phase=insert-tail[69:80:4]:initial-compare
(define-fun formal_0_1013 () FormalMachine (FormalCallback formal_0_1012 boundary_0 (select (m_origin formal_0_1012) 43) (select (m_origin formal_0_1012) 6)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:4]
(define-fun formal_0_1014 () FormalMachine (FormalWriteFromOrigin formal_0_1013 73 6))
; source callback case=recursive-pivot phase=insert-tail[69:80:4]:sift-compare
(assert (not (m_panicked formal_0_1014)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1014) (select (m_origin formal_0_1014) 43) (select (m_origin formal_0_1014) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1014) (select (m_origin formal_0_1014) 43) (select (m_origin formal_0_1014) 7)) false))
; source callback transition phase=insert-tail[69:80:4]:sift-compare
(define-fun formal_0_1015 () FormalMachine (FormalCallback formal_0_1014 boundary_0 (select (m_origin formal_0_1014) 43) (select (m_origin formal_0_1014) 7)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:4]
(define-fun formal_0_1016 () FormalMachine (FormalWriteFromOrigin formal_0_1015 72 7))
; source callback case=recursive-pivot phase=insert-tail[69:80:4]:sift-compare
(assert (not (m_panicked formal_0_1016)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1016) (select (m_origin formal_0_1016) 43) (select (m_origin formal_0_1016) 72)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1016) (select (m_origin formal_0_1016) 43) (select (m_origin formal_0_1016) 72)) false))
; source callback transition phase=insert-tail[69:80:4]:sift-compare
(define-fun formal_0_1017 () FormalMachine (FormalCallback formal_0_1016 boundary_0 (select (m_origin formal_0_1016) 43) (select (m_origin formal_0_1016) 72)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:4]
(define-fun formal_0_1018 () FormalMachine (FormalWriteFromOrigin formal_0_1017 71 72))
; source callback case=recursive-pivot phase=insert-tail[69:80:4]:sift-compare
(assert (not (m_panicked formal_0_1018)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1018) (select (m_origin formal_0_1018) 43) (select (m_origin formal_0_1018) 5)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1018) (select (m_origin formal_0_1018) 43) (select (m_origin formal_0_1018) 5)) false))
; source callback transition phase=insert-tail[69:80:4]:sift-compare
(define-fun formal_0_1019 () FormalMachine (FormalCallback formal_0_1018 boundary_0 (select (m_origin formal_0_1018) 43) (select (m_origin formal_0_1018) 5)))
; source write kind=copy-on-drop-restore phase=insert-tail[69:80:4]
(define-fun formal_0_1020 () FormalMachine (FormalWriteFromOrigin formal_0_1019 70 43))
; source callback case=recursive-pivot phase=insert-tail[69:80:5]:initial-compare
(assert (not (m_panicked formal_0_1020)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1020) (select (m_origin formal_0_1020) 0) (select (m_origin formal_0_1020) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1020) (select (m_origin formal_0_1020) 0) (select (m_origin formal_0_1020) 6)) false))
; source callback transition phase=insert-tail[69:80:5]:initial-compare
(define-fun formal_0_1021 () FormalMachine (FormalCallback formal_0_1020 boundary_0 (select (m_origin formal_0_1020) 0) (select (m_origin formal_0_1020) 6)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:5]
(define-fun formal_0_1022 () FormalMachine (FormalWriteFromOrigin formal_0_1021 74 6))
; source callback case=recursive-pivot phase=insert-tail[69:80:5]:sift-compare
(assert (not (m_panicked formal_0_1022)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1022) (select (m_origin formal_0_1022) 0) (select (m_origin formal_0_1022) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1022) (select (m_origin formal_0_1022) 0) (select (m_origin formal_0_1022) 7)) false))
; source callback transition phase=insert-tail[69:80:5]:sift-compare
(define-fun formal_0_1023 () FormalMachine (FormalCallback formal_0_1022 boundary_0 (select (m_origin formal_0_1022) 0) (select (m_origin formal_0_1022) 7)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:5]
(define-fun formal_0_1024 () FormalMachine (FormalWriteFromOrigin formal_0_1023 73 7))
; source callback case=recursive-pivot phase=insert-tail[69:80:5]:sift-compare
(assert (not (m_panicked formal_0_1024)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1024) (select (m_origin formal_0_1024) 0) (select (m_origin formal_0_1024) 72)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1024) (select (m_origin formal_0_1024) 0) (select (m_origin formal_0_1024) 72)) false))
; source callback transition phase=insert-tail[69:80:5]:sift-compare
(define-fun formal_0_1025 () FormalMachine (FormalCallback formal_0_1024 boundary_0 (select (m_origin formal_0_1024) 0) (select (m_origin formal_0_1024) 72)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:5]
(define-fun formal_0_1026 () FormalMachine (FormalWriteFromOrigin formal_0_1025 72 72))
; source callback case=recursive-pivot phase=insert-tail[69:80:5]:sift-compare
(assert (not (m_panicked formal_0_1026)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1026) (select (m_origin formal_0_1026) 0) (select (m_origin formal_0_1026) 43)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1026) (select (m_origin formal_0_1026) 0) (select (m_origin formal_0_1026) 43)) false))
; source callback transition phase=insert-tail[69:80:5]:sift-compare
(define-fun formal_0_1027 () FormalMachine (FormalCallback formal_0_1026 boundary_0 (select (m_origin formal_0_1026) 0) (select (m_origin formal_0_1026) 43)))
; source write kind=copy-on-drop-restore phase=insert-tail[69:80:5]
(define-fun formal_0_1028 () FormalMachine (FormalWriteFromOrigin formal_0_1027 71 0))
; source callback case=recursive-pivot phase=insert-tail[69:80:6]:initial-compare
(assert (not (m_panicked formal_0_1028)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1028) (select (m_origin formal_0_1028) 49) (select (m_origin formal_0_1028) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1028) (select (m_origin formal_0_1028) 49) (select (m_origin formal_0_1028) 6)) false))
; source callback transition phase=insert-tail[69:80:6]:initial-compare
(define-fun formal_0_1029 () FormalMachine (FormalCallback formal_0_1028 boundary_0 (select (m_origin formal_0_1028) 49) (select (m_origin formal_0_1028) 6)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:6]
(define-fun formal_0_1030 () FormalMachine (FormalWriteFromOrigin formal_0_1029 75 6))
; source callback case=recursive-pivot phase=insert-tail[69:80:6]:sift-compare
(assert (not (m_panicked formal_0_1030)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1030) (select (m_origin formal_0_1030) 49) (select (m_origin formal_0_1030) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1030) (select (m_origin formal_0_1030) 49) (select (m_origin formal_0_1030) 7)) false))
; source callback transition phase=insert-tail[69:80:6]:sift-compare
(define-fun formal_0_1031 () FormalMachine (FormalCallback formal_0_1030 boundary_0 (select (m_origin formal_0_1030) 49) (select (m_origin formal_0_1030) 7)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:6]
(define-fun formal_0_1032 () FormalMachine (FormalWriteFromOrigin formal_0_1031 74 7))
; source callback case=recursive-pivot phase=insert-tail[69:80:6]:sift-compare
(assert (not (m_panicked formal_0_1032)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1032) (select (m_origin formal_0_1032) 49) (select (m_origin formal_0_1032) 72)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1032) (select (m_origin formal_0_1032) 49) (select (m_origin formal_0_1032) 72)) false))
; source callback transition phase=insert-tail[69:80:6]:sift-compare
(define-fun formal_0_1033 () FormalMachine (FormalCallback formal_0_1032 boundary_0 (select (m_origin formal_0_1032) 49) (select (m_origin formal_0_1032) 72)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:6]
(define-fun formal_0_1034 () FormalMachine (FormalWriteFromOrigin formal_0_1033 73 72))
; source callback case=recursive-pivot phase=insert-tail[69:80:6]:sift-compare
(assert (not (m_panicked formal_0_1034)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1034) (select (m_origin formal_0_1034) 49) (select (m_origin formal_0_1034) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1034) (select (m_origin formal_0_1034) 49) (select (m_origin formal_0_1034) 0)) false))
; source callback transition phase=insert-tail[69:80:6]:sift-compare
(define-fun formal_0_1035 () FormalMachine (FormalCallback formal_0_1034 boundary_0 (select (m_origin formal_0_1034) 49) (select (m_origin formal_0_1034) 0)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:6]
(define-fun formal_0_1036 () FormalMachine (FormalWriteFromOrigin formal_0_1035 72 0))
; source callback case=recursive-pivot phase=insert-tail[69:80:6]:sift-compare
(assert (not (m_panicked formal_0_1036)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1036) (select (m_origin formal_0_1036) 49) (select (m_origin formal_0_1036) 43)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1036) (select (m_origin formal_0_1036) 49) (select (m_origin formal_0_1036) 43)) false))
; source callback transition phase=insert-tail[69:80:6]:sift-compare
(define-fun formal_0_1037 () FormalMachine (FormalCallback formal_0_1036 boundary_0 (select (m_origin formal_0_1036) 49) (select (m_origin formal_0_1036) 43)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:6]
(define-fun formal_0_1038 () FormalMachine (FormalWriteFromOrigin formal_0_1037 71 43))
; source callback case=recursive-pivot phase=insert-tail[69:80:6]:sift-compare
(assert (not (m_panicked formal_0_1038)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1038) (select (m_origin formal_0_1038) 49) (select (m_origin formal_0_1038) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1038) (select (m_origin formal_0_1038) 49) (select (m_origin formal_0_1038) 5)) false))
; source callback transition phase=insert-tail[69:80:6]:sift-compare
(define-fun formal_0_1039 () FormalMachine (FormalCallback formal_0_1038 boundary_0 (select (m_origin formal_0_1038) 49) (select (m_origin formal_0_1038) 5)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:6]
(define-fun formal_0_1040 () FormalMachine (FormalWriteFromOrigin formal_0_1039 70 5))
; source write kind=copy-on-drop-restore phase=insert-tail[69:80:6]
(define-fun formal_0_1041 () FormalMachine (FormalWriteFromOrigin formal_0_1040 69 49))
; source callback case=recursive-pivot phase=insert-tail[69:80:7]:initial-compare
(assert (not (m_panicked formal_0_1041)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1041) (select (m_origin formal_0_1041) 11) (select (m_origin formal_0_1041) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1041) (select (m_origin formal_0_1041) 11) (select (m_origin formal_0_1041) 6)) false))
; source callback transition phase=insert-tail[69:80:7]:initial-compare
(define-fun formal_0_1042 () FormalMachine (FormalCallback formal_0_1041 boundary_0 (select (m_origin formal_0_1041) 11) (select (m_origin formal_0_1041) 6)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:7]
(define-fun formal_0_1043 () FormalMachine (FormalWriteFromOrigin formal_0_1042 76 6))
; source callback case=recursive-pivot phase=insert-tail[69:80:7]:sift-compare
(assert (not (m_panicked formal_0_1043)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1043) (select (m_origin formal_0_1043) 11) (select (m_origin formal_0_1043) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1043) (select (m_origin formal_0_1043) 11) (select (m_origin formal_0_1043) 7)) false))
; source callback transition phase=insert-tail[69:80:7]:sift-compare
(define-fun formal_0_1044 () FormalMachine (FormalCallback formal_0_1043 boundary_0 (select (m_origin formal_0_1043) 11) (select (m_origin formal_0_1043) 7)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:7]
(define-fun formal_0_1045 () FormalMachine (FormalWriteFromOrigin formal_0_1044 75 7))
; source callback case=recursive-pivot phase=insert-tail[69:80:7]:sift-compare
(assert (not (m_panicked formal_0_1045)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1045) (select (m_origin formal_0_1045) 11) (select (m_origin formal_0_1045) 72)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1045) (select (m_origin formal_0_1045) 11) (select (m_origin formal_0_1045) 72)) false))
; source callback transition phase=insert-tail[69:80:7]:sift-compare
(define-fun formal_0_1046 () FormalMachine (FormalCallback formal_0_1045 boundary_0 (select (m_origin formal_0_1045) 11) (select (m_origin formal_0_1045) 72)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:7]
(define-fun formal_0_1047 () FormalMachine (FormalWriteFromOrigin formal_0_1046 74 72))
; source callback case=recursive-pivot phase=insert-tail[69:80:7]:sift-compare
(assert (not (m_panicked formal_0_1047)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1047) (select (m_origin formal_0_1047) 11) (select (m_origin formal_0_1047) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1047) (select (m_origin formal_0_1047) 11) (select (m_origin formal_0_1047) 0)) false))
; source callback transition phase=insert-tail[69:80:7]:sift-compare
(define-fun formal_0_1048 () FormalMachine (FormalCallback formal_0_1047 boundary_0 (select (m_origin formal_0_1047) 11) (select (m_origin formal_0_1047) 0)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:7]
(define-fun formal_0_1049 () FormalMachine (FormalWriteFromOrigin formal_0_1048 73 0))
; source callback case=recursive-pivot phase=insert-tail[69:80:7]:sift-compare
(assert (not (m_panicked formal_0_1049)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1049) (select (m_origin formal_0_1049) 11) (select (m_origin formal_0_1049) 43)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1049) (select (m_origin formal_0_1049) 11) (select (m_origin formal_0_1049) 43)) false))
; source callback transition phase=insert-tail[69:80:7]:sift-compare
(define-fun formal_0_1050 () FormalMachine (FormalCallback formal_0_1049 boundary_0 (select (m_origin formal_0_1049) 11) (select (m_origin formal_0_1049) 43)))
; source write kind=copy-on-drop-restore phase=insert-tail[69:80:7]
(define-fun formal_0_1051 () FormalMachine (FormalWriteFromOrigin formal_0_1050 72 11))
; source callback case=recursive-pivot phase=insert-tail[69:80:8]:initial-compare
(assert (not (m_panicked formal_0_1051)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1051) (select (m_origin formal_0_1051) 67) (select (m_origin formal_0_1051) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1051) (select (m_origin formal_0_1051) 67) (select (m_origin formal_0_1051) 6)) false))
; source callback transition phase=insert-tail[69:80:8]:initial-compare
(define-fun formal_0_1052 () FormalMachine (FormalCallback formal_0_1051 boundary_0 (select (m_origin formal_0_1051) 67) (select (m_origin formal_0_1051) 6)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:8]
(define-fun formal_0_1053 () FormalMachine (FormalWriteFromOrigin formal_0_1052 77 6))
; source callback case=recursive-pivot phase=insert-tail[69:80:8]:sift-compare
(assert (not (m_panicked formal_0_1053)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1053) (select (m_origin formal_0_1053) 67) (select (m_origin formal_0_1053) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1053) (select (m_origin formal_0_1053) 67) (select (m_origin formal_0_1053) 7)) false))
; source callback transition phase=insert-tail[69:80:8]:sift-compare
(define-fun formal_0_1054 () FormalMachine (FormalCallback formal_0_1053 boundary_0 (select (m_origin formal_0_1053) 67) (select (m_origin formal_0_1053) 7)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:8]
(define-fun formal_0_1055 () FormalMachine (FormalWriteFromOrigin formal_0_1054 76 7))
; source callback case=recursive-pivot phase=insert-tail[69:80:8]:sift-compare
(assert (not (m_panicked formal_0_1055)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1055) (select (m_origin formal_0_1055) 67) (select (m_origin formal_0_1055) 72)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1055) (select (m_origin formal_0_1055) 67) (select (m_origin formal_0_1055) 72)) false))
; source callback transition phase=insert-tail[69:80:8]:sift-compare
(define-fun formal_0_1056 () FormalMachine (FormalCallback formal_0_1055 boundary_0 (select (m_origin formal_0_1055) 67) (select (m_origin formal_0_1055) 72)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:8]
(define-fun formal_0_1057 () FormalMachine (FormalWriteFromOrigin formal_0_1056 75 72))
; source callback case=recursive-pivot phase=insert-tail[69:80:8]:sift-compare
(assert (not (m_panicked formal_0_1057)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1057) (select (m_origin formal_0_1057) 67) (select (m_origin formal_0_1057) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1057) (select (m_origin formal_0_1057) 67) (select (m_origin formal_0_1057) 0)) false))
; source callback transition phase=insert-tail[69:80:8]:sift-compare
(define-fun formal_0_1058 () FormalMachine (FormalCallback formal_0_1057 boundary_0 (select (m_origin formal_0_1057) 67) (select (m_origin formal_0_1057) 0)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:8]
(define-fun formal_0_1059 () FormalMachine (FormalWriteFromOrigin formal_0_1058 74 0))
; source callback case=recursive-pivot phase=insert-tail[69:80:8]:sift-compare
(assert (not (m_panicked formal_0_1059)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1059) (select (m_origin formal_0_1059) 67) (select (m_origin formal_0_1059) 11)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1059) (select (m_origin formal_0_1059) 67) (select (m_origin formal_0_1059) 11)) false))
; source callback transition phase=insert-tail[69:80:8]:sift-compare
(define-fun formal_0_1060 () FormalMachine (FormalCallback formal_0_1059 boundary_0 (select (m_origin formal_0_1059) 67) (select (m_origin formal_0_1059) 11)))
; source write kind=copy-on-drop-restore phase=insert-tail[69:80:8]
(define-fun formal_0_1061 () FormalMachine (FormalWriteFromOrigin formal_0_1060 73 67))
; source callback case=recursive-pivot phase=insert-tail[69:80:9]:initial-compare
(assert (not (m_panicked formal_0_1061)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1061) (select (m_origin formal_0_1061) 35) (select (m_origin formal_0_1061) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1061) (select (m_origin formal_0_1061) 35) (select (m_origin formal_0_1061) 6)) false))
; source callback transition phase=insert-tail[69:80:9]:initial-compare
(define-fun formal_0_1062 () FormalMachine (FormalCallback formal_0_1061 boundary_0 (select (m_origin formal_0_1061) 35) (select (m_origin formal_0_1061) 6)))
; source write kind=insert-tail-shift phase=insert-tail[69:80:9]
(define-fun formal_0_1063 () FormalMachine (FormalWriteFromOrigin formal_0_1062 78 6))
; source callback case=recursive-pivot phase=insert-tail[69:80:9]:sift-compare
(assert (not (m_panicked formal_0_1063)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1063) (select (m_origin formal_0_1063) 35) (select (m_origin formal_0_1063) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1063) (select (m_origin formal_0_1063) 35) (select (m_origin formal_0_1063) 7)) false))
; source callback transition phase=insert-tail[69:80:9]:sift-compare
(define-fun formal_0_1064 () FormalMachine (FormalCallback formal_0_1063 boundary_0 (select (m_origin formal_0_1063) 35) (select (m_origin formal_0_1063) 7)))
; source write kind=copy-on-drop-restore phase=insert-tail[69:80:9]
(define-fun formal_0_1065 () FormalMachine (FormalWriteFromOrigin formal_0_1064 77 35))
; source callback case=recursive-pivot phase=insert-tail[69:80:10]:initial-compare
(assert (not (m_panicked formal_0_1065)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1065) (select (m_origin formal_0_1065) 28) (select (m_origin formal_0_1065) 6)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1065) (select (m_origin formal_0_1065) 28) (select (m_origin formal_0_1065) 6)) false))
; source callback transition phase=insert-tail[69:80:10]:initial-compare
(define-fun formal_0_1066 () FormalMachine (FormalCallback formal_0_1065 boundary_0 (select (m_origin formal_0_1065) 28) (select (m_origin formal_0_1065) 6)))
(define-fun formal_result_0 () Result
  (mkResult
    (m_sequence formal_0_1066)
    (m_callback formal_0_1066)
    (m_panicked formal_0_1066)
    false
    true
    (ite (m_panicked formal_0_1066) 1 0)
    (not (m_panicked formal_0_1066))
    -1))
(define-fun reference_result_0 () Result (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 21 21) 22 22) 23 23) 24 24) 25 25) 26 26) 27 27) 28 28) 29 29) 30 30) 31 31) 32 32) 33 33) 34 34) 35 35) 36 36) 37 37) 38 38) 39 39) 40 40) 41 41) 42 42) 43 43) 44 44) 45 45) 46 46) 47 47) 48 48) 49 49) 50 50) 51 51) 52 52) 53 53) 54 54) 55 55) 56 56) 57 57) 58 58) 59 59) 60 60) 61 61) 62 62) 63 63) 64 64) 65 65) 66 66) 67 67) 68 68) 69 69) 70 70) 71 71) 72 72) 73 73) 74 74) 75 75) 76 76) 77 77) 78 78) 79 79) 487 false false true 0 true -1))
; retained source-forcing witness: recursive-median3
(assert (= formal_result_0 (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 21 21) 22 22) 23 23) 24 24) 25 25) 26 26) 27 27) 28 28) 29 29) 30 30) 31 31) 32 32) 33 33) 34 34) 35 35) 36 36) 37 37) 38 38) 39 39) 40 40) 41 41) 42 42) 43 43) 44 44) 45 45) 46 46) 47 47) 48 48) 49 49) 50 50) 51 51) 52 52) 53 53) 54 54) 55 55) 56 56) 57 57) 58 58) 59 59) 60 60) 61 61) 62 62) 63 63) 64 64) 65 65) 66 66) 67 67) 68 68) 69 69) 70 70) 71 71) 72 72) 73 73) 74 74) 75 75) 76 76) 77 77) 78 78) 79 79) 487 false false true 0 true -1)))
(check-sat-using (then ctx-solver-simplify smt))
