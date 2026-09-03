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

; formal source input case=fallback-small-sort-and-recursion
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
  (mkFormalMachine (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 5) 1 24) 2 38) 3 39) 4 28) 5 27) 6 26) 7 42) 8 36) 9 20) 10 19) 11 12) 12 1) 13 3) 14 44) 15 4) 16 0) 17 34) 18 21) 19 13) 20 11) 21 40) 22 10) 23 43) 24 9) 25 14) 26 33) 27 32) 28 35) 29 30) 30 41) 31 7) 32 29) 33 23) 34 37) 35 18) 36 2) 37 6) 38 22) 39 17) 40 8) 41 16) 42 25) 43 31) 44 15) (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 5) 1 24) 2 38) 3 39) 4 28) 5 27) 6 26) 7 42) 8 36) 9 20) 10 19) 11 12) 12 1) 13 3) 14 44) 15 4) 16 0) 17 34) 18 21) 19 13) 20 11) 21 40) 22 10) 23 43) 24 9) 25 14) 26 33) 27 32) 28 35) 29 30) 30 41) 31 7) 32 29) 33 23) 34 37) 35 18) 36 2) 37 6) 38 22) 39 17) 40 8) 41 16) 42 25) 43 31) 44 15) (b_initial_state boundary_0) false))
(assert (BoundaryWellFormed boundary_0))
; source callback case=fallback-small-sort-and-recursion phase=find-existing-run:direction
(assert (not (m_panicked source_initial_0)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback source_initial_0) (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)) false))
; source callback transition phase=find-existing-run:direction
(define-fun formal_0_1 () FormalMachine (FormalCallback source_initial_0 boundary_0 (select (m_origin source_initial_0) 1) (select (m_origin source_initial_0) 0)))
; source callback case=fallback-small-sort-and-recursion phase=find-existing-run:ascending
(assert (not (m_panicked formal_0_1)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_1) (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)) false))
; source callback transition phase=find-existing-run:ascending
(define-fun formal_0_2 () FormalMachine (FormalCallback formal_0_1 boundary_0 (select (m_origin formal_0_1) 2) (select (m_origin formal_0_1) 1)))
; source callback case=fallback-small-sort-and-recursion phase=find-existing-run:ascending
(assert (not (m_panicked formal_0_2)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 3) (select (m_origin formal_0_2) 2)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_2) (select (m_origin formal_0_2) 3) (select (m_origin formal_0_2) 2)) false))
; source callback transition phase=find-existing-run:ascending
(define-fun formal_0_3 () FormalMachine (FormalCallback formal_0_2 boundary_0 (select (m_origin formal_0_2) 3) (select (m_origin formal_0_2) 2)))
; source callback case=fallback-small-sort-and-recursion phase=find-existing-run:ascending
(assert (not (m_panicked formal_0_3)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 4) (select (m_origin formal_0_3) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_3) (select (m_origin formal_0_3) 4) (select (m_origin formal_0_3) 3)) false))
; source callback transition phase=find-existing-run:ascending
(define-fun formal_0_4 () FormalMachine (FormalCallback formal_0_3 boundary_0 (select (m_origin formal_0_3) 4) (select (m_origin formal_0_3) 3)))
; source callback case=fallback-small-sort-and-recursion phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_4)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 0) (select (m_origin formal_0_4) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_4) (select (m_origin formal_0_4) 0) (select (m_origin formal_0_4) 20)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_5 () FormalMachine (FormalCallback formal_0_4 boundary_0 (select (m_origin formal_0_4) 0) (select (m_origin formal_0_4) 20)))
; source callback case=fallback-small-sort-and-recursion phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_5)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_5) (select (m_origin formal_0_5) 0) (select (m_origin formal_0_5) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_5) (select (m_origin formal_0_5) 0) (select (m_origin formal_0_5) 35)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_6 () FormalMachine (FormalCallback formal_0_5 boundary_0 (select (m_origin formal_0_5) 0) (select (m_origin formal_0_5) 35)))
; source callback case=fallback-small-sort-and-recursion phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_6)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 20) (select (m_origin formal_0_6) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_6) (select (m_origin formal_0_6) 20) (select (m_origin formal_0_6) 35)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_7 () FormalMachine (FormalCallback formal_0_6 boundary_0 (select (m_origin formal_0_6) 20) (select (m_origin formal_0_6) 35)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_8 () FormalMachine (FormalSwap formal_0_7 0 20))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_8)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 2) (select (m_origin formal_0_8) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_8) (select (m_origin formal_0_8) 2) (select (m_origin formal_0_8) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_9 () FormalMachine (FormalCallback formal_0_8 boundary_0 (select (m_origin formal_0_8) 2) (select (m_origin formal_0_8) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_10 () FormalMachine (FormalWriteFromOrigin formal_0_9 1 2))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_10)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_10) (select (m_origin formal_0_10) 3) (select (m_origin formal_0_10) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_10) (select (m_origin formal_0_10) 3) (select (m_origin formal_0_10) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_11 () FormalMachine (FormalCallback formal_0_10 boundary_0 (select (m_origin formal_0_10) 3) (select (m_origin formal_0_10) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_12 () FormalMachine (FormalWriteFromOrigin formal_0_11 1 3))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_12)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_12) (select (m_origin formal_0_12) 4) (select (m_origin formal_0_12) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_12) (select (m_origin formal_0_12) 4) (select (m_origin formal_0_12) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_13 () FormalMachine (FormalCallback formal_0_12 boundary_0 (select (m_origin formal_0_12) 4) (select (m_origin formal_0_12) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_14 () FormalMachine (FormalWriteFromOrigin formal_0_13 1 4))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_14)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_14) (select (m_origin formal_0_14) 5) (select (m_origin formal_0_14) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_14) (select (m_origin formal_0_14) 5) (select (m_origin formal_0_14) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_15 () FormalMachine (FormalCallback formal_0_14 boundary_0 (select (m_origin formal_0_14) 5) (select (m_origin formal_0_14) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_16 () FormalMachine (FormalWriteFromOrigin formal_0_15 1 5))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_16)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_16) (select (m_origin formal_0_16) 6) (select (m_origin formal_0_16) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_16) (select (m_origin formal_0_16) 6) (select (m_origin formal_0_16) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_17 () FormalMachine (FormalCallback formal_0_16 boundary_0 (select (m_origin formal_0_16) 6) (select (m_origin formal_0_16) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_18 () FormalMachine (FormalWriteFromOrigin formal_0_17 1 6))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_18)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_18) (select (m_origin formal_0_18) 7) (select (m_origin formal_0_18) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_18) (select (m_origin formal_0_18) 7) (select (m_origin formal_0_18) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_19 () FormalMachine (FormalCallback formal_0_18 boundary_0 (select (m_origin formal_0_18) 7) (select (m_origin formal_0_18) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_20 () FormalMachine (FormalWriteFromOrigin formal_0_19 1 7))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_20)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 8) (select (m_origin formal_0_20) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_20) (select (m_origin formal_0_20) 8) (select (m_origin formal_0_20) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_21 () FormalMachine (FormalCallback formal_0_20 boundary_0 (select (m_origin formal_0_20) 8) (select (m_origin formal_0_20) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_22 () FormalMachine (FormalWriteFromOrigin formal_0_21 1 8))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_22)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_22) (select (m_origin formal_0_22) 9) (select (m_origin formal_0_22) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_22) (select (m_origin formal_0_22) 9) (select (m_origin formal_0_22) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_23 () FormalMachine (FormalCallback formal_0_22 boundary_0 (select (m_origin formal_0_22) 9) (select (m_origin formal_0_22) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_24 () FormalMachine (FormalWriteFromOrigin formal_0_23 1 9))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_24)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_24) (select (m_origin formal_0_24) 10) (select (m_origin formal_0_24) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_24) (select (m_origin formal_0_24) 10) (select (m_origin formal_0_24) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_25 () FormalMachine (FormalCallback formal_0_24 boundary_0 (select (m_origin formal_0_24) 10) (select (m_origin formal_0_24) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_26 () FormalMachine (FormalWriteFromOrigin formal_0_25 1 10))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_26)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_26) (select (m_origin formal_0_26) 11) (select (m_origin formal_0_26) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_26) (select (m_origin formal_0_26) 11) (select (m_origin formal_0_26) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_27 () FormalMachine (FormalCallback formal_0_26 boundary_0 (select (m_origin formal_0_26) 11) (select (m_origin formal_0_26) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_28 () FormalMachine (FormalWriteFromOrigin formal_0_27 1 11))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_28)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_28) (select (m_origin formal_0_28) 12) (select (m_origin formal_0_28) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_28) (select (m_origin formal_0_28) 12) (select (m_origin formal_0_28) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_29 () FormalMachine (FormalCallback formal_0_28 boundary_0 (select (m_origin formal_0_28) 12) (select (m_origin formal_0_28) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_30 () FormalMachine (FormalWriteFromOrigin formal_0_29 1 12))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_30)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_30) (select (m_origin formal_0_30) 13) (select (m_origin formal_0_30) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_30) (select (m_origin formal_0_30) 13) (select (m_origin formal_0_30) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_31 () FormalMachine (FormalCallback formal_0_30 boundary_0 (select (m_origin formal_0_30) 13) (select (m_origin formal_0_30) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_32 () FormalMachine (FormalWriteFromOrigin formal_0_31 2 13))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_33 () FormalMachine (FormalWriteFromOrigin formal_0_32 12 2))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_33)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_33) (select (m_origin formal_0_33) 14) (select (m_origin formal_0_33) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_33) (select (m_origin formal_0_33) 14) (select (m_origin formal_0_33) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_34 () FormalMachine (FormalCallback formal_0_33 boundary_0 (select (m_origin formal_0_33) 14) (select (m_origin formal_0_33) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_35 () FormalMachine (FormalWriteFromOrigin formal_0_34 3 14))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_36 () FormalMachine (FormalWriteFromOrigin formal_0_35 13 3))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_36)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_36) (select (m_origin formal_0_36) 15) (select (m_origin formal_0_36) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_36) (select (m_origin formal_0_36) 15) (select (m_origin formal_0_36) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_37 () FormalMachine (FormalCallback formal_0_36 boundary_0 (select (m_origin formal_0_36) 15) (select (m_origin formal_0_36) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_38 () FormalMachine (FormalWriteFromOrigin formal_0_37 3 15))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_38)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 16) (select (m_origin formal_0_38) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_38) (select (m_origin formal_0_38) 16) (select (m_origin formal_0_38) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_39 () FormalMachine (FormalCallback formal_0_38 boundary_0 (select (m_origin formal_0_38) 16) (select (m_origin formal_0_38) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_40 () FormalMachine (FormalWriteFromOrigin formal_0_39 4 16))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_41 () FormalMachine (FormalWriteFromOrigin formal_0_40 15 4))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_41)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 17) (select (m_origin formal_0_41) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_41) (select (m_origin formal_0_41) 17) (select (m_origin formal_0_41) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_42 () FormalMachine (FormalCallback formal_0_41 boundary_0 (select (m_origin formal_0_41) 17) (select (m_origin formal_0_41) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_43 () FormalMachine (FormalWriteFromOrigin formal_0_42 5 17))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_44 () FormalMachine (FormalWriteFromOrigin formal_0_43 16 5))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_44)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 18) (select (m_origin formal_0_44) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_44) (select (m_origin formal_0_44) 18) (select (m_origin formal_0_44) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_45 () FormalMachine (FormalCallback formal_0_44 boundary_0 (select (m_origin formal_0_44) 18) (select (m_origin formal_0_44) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_46 () FormalMachine (FormalWriteFromOrigin formal_0_45 5 18))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_46)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_46) (select (m_origin formal_0_46) 19) (select (m_origin formal_0_46) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_46) (select (m_origin formal_0_46) 19) (select (m_origin formal_0_46) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_47 () FormalMachine (FormalCallback formal_0_46 boundary_0 (select (m_origin formal_0_46) 19) (select (m_origin formal_0_46) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_48 () FormalMachine (FormalWriteFromOrigin formal_0_47 5 19))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_48)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 0) (select (m_origin formal_0_48) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_48) (select (m_origin formal_0_48) 0) (select (m_origin formal_0_48) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_49 () FormalMachine (FormalCallback formal_0_48 boundary_0 (select (m_origin formal_0_48) 0) (select (m_origin formal_0_48) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_50 () FormalMachine (FormalWriteFromOrigin formal_0_49 5 0))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_50)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_50) (select (m_origin formal_0_50) 21) (select (m_origin formal_0_50) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_50) (select (m_origin formal_0_50) 21) (select (m_origin formal_0_50) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_51 () FormalMachine (FormalCallback formal_0_50 boundary_0 (select (m_origin formal_0_50) 21) (select (m_origin formal_0_50) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_52 () FormalMachine (FormalWriteFromOrigin formal_0_51 6 21))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_53 () FormalMachine (FormalWriteFromOrigin formal_0_52 20 6))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_53)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_53) (select (m_origin formal_0_53) 22) (select (m_origin formal_0_53) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_53) (select (m_origin formal_0_53) 22) (select (m_origin formal_0_53) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_54 () FormalMachine (FormalCallback formal_0_53 boundary_0 (select (m_origin formal_0_53) 22) (select (m_origin formal_0_53) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_55 () FormalMachine (FormalWriteFromOrigin formal_0_54 6 22))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_55)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_55) (select (m_origin formal_0_55) 23) (select (m_origin formal_0_55) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_55) (select (m_origin formal_0_55) 23) (select (m_origin formal_0_55) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_56 () FormalMachine (FormalCallback formal_0_55 boundary_0 (select (m_origin formal_0_55) 23) (select (m_origin formal_0_55) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_57 () FormalMachine (FormalWriteFromOrigin formal_0_56 7 23))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_58 () FormalMachine (FormalWriteFromOrigin formal_0_57 22 7))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_58)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_58) (select (m_origin formal_0_58) 24) (select (m_origin formal_0_58) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_58) (select (m_origin formal_0_58) 24) (select (m_origin formal_0_58) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_59 () FormalMachine (FormalCallback formal_0_58 boundary_0 (select (m_origin formal_0_58) 24) (select (m_origin formal_0_58) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_60 () FormalMachine (FormalWriteFromOrigin formal_0_59 7 24))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_60)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_60) (select (m_origin formal_0_60) 25) (select (m_origin formal_0_60) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_60) (select (m_origin formal_0_60) 25) (select (m_origin formal_0_60) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_61 () FormalMachine (FormalCallback formal_0_60 boundary_0 (select (m_origin formal_0_60) 25) (select (m_origin formal_0_60) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_62 () FormalMachine (FormalWriteFromOrigin formal_0_61 8 25))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_63 () FormalMachine (FormalWriteFromOrigin formal_0_62 24 8))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_63)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_63) (select (m_origin formal_0_63) 26) (select (m_origin formal_0_63) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_63) (select (m_origin formal_0_63) 26) (select (m_origin formal_0_63) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_64 () FormalMachine (FormalCallback formal_0_63 boundary_0 (select (m_origin formal_0_63) 26) (select (m_origin formal_0_63) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_65 () FormalMachine (FormalWriteFromOrigin formal_0_64 8 26))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_65)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_65) (select (m_origin formal_0_65) 27) (select (m_origin formal_0_65) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_65) (select (m_origin formal_0_65) 27) (select (m_origin formal_0_65) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_66 () FormalMachine (FormalCallback formal_0_65 boundary_0 (select (m_origin formal_0_65) 27) (select (m_origin formal_0_65) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_67 () FormalMachine (FormalWriteFromOrigin formal_0_66 8 27))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_67)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_67) (select (m_origin formal_0_67) 28) (select (m_origin formal_0_67) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_67) (select (m_origin formal_0_67) 28) (select (m_origin formal_0_67) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_68 () FormalMachine (FormalCallback formal_0_67 boundary_0 (select (m_origin formal_0_67) 28) (select (m_origin formal_0_67) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_69 () FormalMachine (FormalWriteFromOrigin formal_0_68 8 28))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_69)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 29) (select (m_origin formal_0_69) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_69) (select (m_origin formal_0_69) 29) (select (m_origin formal_0_69) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_70 () FormalMachine (FormalCallback formal_0_69 boundary_0 (select (m_origin formal_0_69) 29) (select (m_origin formal_0_69) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_71 () FormalMachine (FormalWriteFromOrigin formal_0_70 8 29))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_71)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_71) (select (m_origin formal_0_71) 30) (select (m_origin formal_0_71) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_71) (select (m_origin formal_0_71) 30) (select (m_origin formal_0_71) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_72 () FormalMachine (FormalCallback formal_0_71 boundary_0 (select (m_origin formal_0_71) 30) (select (m_origin formal_0_71) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_73 () FormalMachine (FormalWriteFromOrigin formal_0_72 8 30))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_73)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 31) (select (m_origin formal_0_73) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_73) (select (m_origin formal_0_73) 31) (select (m_origin formal_0_73) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_74 () FormalMachine (FormalCallback formal_0_73 boundary_0 (select (m_origin formal_0_73) 31) (select (m_origin formal_0_73) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_75 () FormalMachine (FormalWriteFromOrigin formal_0_74 8 31))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_75)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 32) (select (m_origin formal_0_75) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_75) (select (m_origin formal_0_75) 32) (select (m_origin formal_0_75) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_76 () FormalMachine (FormalCallback formal_0_75 boundary_0 (select (m_origin formal_0_75) 32) (select (m_origin formal_0_75) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_77 () FormalMachine (FormalWriteFromOrigin formal_0_76 9 32))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_78 () FormalMachine (FormalWriteFromOrigin formal_0_77 31 9))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_78)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 33) (select (m_origin formal_0_78) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_78) (select (m_origin formal_0_78) 33) (select (m_origin formal_0_78) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_79 () FormalMachine (FormalCallback formal_0_78 boundary_0 (select (m_origin formal_0_78) 33) (select (m_origin formal_0_78) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_80 () FormalMachine (FormalWriteFromOrigin formal_0_79 9 33))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_80)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_80) (select (m_origin formal_0_80) 34) (select (m_origin formal_0_80) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_80) (select (m_origin formal_0_80) 34) (select (m_origin formal_0_80) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_81 () FormalMachine (FormalCallback formal_0_80 boundary_0 (select (m_origin formal_0_80) 34) (select (m_origin formal_0_80) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_82 () FormalMachine (FormalWriteFromOrigin formal_0_81 9 34))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_82)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_82) (select (m_origin formal_0_82) 35) (select (m_origin formal_0_82) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_82) (select (m_origin formal_0_82) 35) (select (m_origin formal_0_82) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_83 () FormalMachine (FormalCallback formal_0_82 boundary_0 (select (m_origin formal_0_82) 35) (select (m_origin formal_0_82) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_84 () FormalMachine (FormalWriteFromOrigin formal_0_83 9 35))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_84)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_84) (select (m_origin formal_0_84) 36) (select (m_origin formal_0_84) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_84) (select (m_origin formal_0_84) 36) (select (m_origin formal_0_84) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_85 () FormalMachine (FormalCallback formal_0_84 boundary_0 (select (m_origin formal_0_84) 36) (select (m_origin formal_0_84) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_86 () FormalMachine (FormalWriteFromOrigin formal_0_85 9 36))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_86)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 37) (select (m_origin formal_0_86) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_86) (select (m_origin formal_0_86) 37) (select (m_origin formal_0_86) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_87 () FormalMachine (FormalCallback formal_0_86 boundary_0 (select (m_origin formal_0_86) 37) (select (m_origin formal_0_86) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_88 () FormalMachine (FormalWriteFromOrigin formal_0_87 10 37))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_89 () FormalMachine (FormalWriteFromOrigin formal_0_88 36 10))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_89)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_89) (select (m_origin formal_0_89) 38) (select (m_origin formal_0_89) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_89) (select (m_origin formal_0_89) 38) (select (m_origin formal_0_89) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_90 () FormalMachine (FormalCallback formal_0_89 boundary_0 (select (m_origin formal_0_89) 38) (select (m_origin formal_0_89) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_91 () FormalMachine (FormalWriteFromOrigin formal_0_90 11 38))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_92 () FormalMachine (FormalWriteFromOrigin formal_0_91 37 11))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_92)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_92) (select (m_origin formal_0_92) 39) (select (m_origin formal_0_92) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_92) (select (m_origin formal_0_92) 39) (select (m_origin formal_0_92) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_93 () FormalMachine (FormalCallback formal_0_92 boundary_0 (select (m_origin formal_0_92) 39) (select (m_origin formal_0_92) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_94 () FormalMachine (FormalWriteFromOrigin formal_0_93 11 39))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_94)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_94) (select (m_origin formal_0_94) 40) (select (m_origin formal_0_94) 20)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_94) (select (m_origin formal_0_94) 40) (select (m_origin formal_0_94) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_95 () FormalMachine (FormalCallback formal_0_94 boundary_0 (select (m_origin formal_0_94) 40) (select (m_origin formal_0_94) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_96 () FormalMachine (FormalWriteFromOrigin formal_0_95 11 40))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_96)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_96) (select (m_origin formal_0_96) 41) (select (m_origin formal_0_96) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_96) (select (m_origin formal_0_96) 41) (select (m_origin formal_0_96) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_97 () FormalMachine (FormalCallback formal_0_96 boundary_0 (select (m_origin formal_0_96) 41) (select (m_origin formal_0_96) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_98 () FormalMachine (FormalWriteFromOrigin formal_0_97 12 41))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_99 () FormalMachine (FormalWriteFromOrigin formal_0_98 40 2))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_99)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 42) (select (m_origin formal_0_99) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_99) (select (m_origin formal_0_99) 42) (select (m_origin formal_0_99) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_100 () FormalMachine (FormalCallback formal_0_99 boundary_0 (select (m_origin formal_0_99) 42) (select (m_origin formal_0_99) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_101 () FormalMachine (FormalWriteFromOrigin formal_0_100 12 42))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_101)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_101) (select (m_origin formal_0_101) 43) (select (m_origin formal_0_101) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_101) (select (m_origin formal_0_101) 43) (select (m_origin formal_0_101) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_102 () FormalMachine (FormalCallback formal_0_101 boundary_0 (select (m_origin formal_0_101) 43) (select (m_origin formal_0_101) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_103 () FormalMachine (FormalWriteFromOrigin formal_0_102 12 43))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_103)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_103) (select (m_origin formal_0_103) 44) (select (m_origin formal_0_103) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_103) (select (m_origin formal_0_103) 44) (select (m_origin formal_0_103) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_104 () FormalMachine (FormalCallback formal_0_103 boundary_0 (select (m_origin formal_0_103) 44) (select (m_origin formal_0_103) 20)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_105 () FormalMachine (FormalWriteFromOrigin formal_0_104 12 44))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_105)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_105) (select (m_origin formal_0_105) 1) (select (m_origin formal_0_105) 20)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_105) (select (m_origin formal_0_105) 1) (select (m_origin formal_0_105) 20)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_106 () FormalMachine (FormalCallback formal_0_105 boundary_0 (select (m_origin formal_0_105) 1) (select (m_origin formal_0_105) 20)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_107 () FormalMachine (FormalWriteFromOrigin formal_0_106 12 1))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_108 () FormalMachine (FormalSwap formal_0_107 0 11))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:1]:initial-compare
(assert (not (m_panicked formal_0_108)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_108) (select (m_origin formal_0_108) 12) (select (m_origin formal_0_108) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_108) (select (m_origin formal_0_108) 12) (select (m_origin formal_0_108) 40)) false))
; source callback transition phase=insert-tail[0:11:1]:initial-compare
(define-fun formal_0_109 () FormalMachine (FormalCallback formal_0_108 boundary_0 (select (m_origin formal_0_108) 12) (select (m_origin formal_0_108) 40)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:1]
(define-fun formal_0_110 () FormalMachine (FormalWriteFromOrigin formal_0_109 1 40))
; source write kind=copy-on-drop-restore phase=insert-tail[0:11:1]
(define-fun formal_0_111 () FormalMachine (FormalWriteFromOrigin formal_0_110 0 12))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:2]:initial-compare
(assert (not (m_panicked formal_0_111)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_111) (select (m_origin formal_0_111) 13) (select (m_origin formal_0_111) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_111) (select (m_origin formal_0_111) 13) (select (m_origin formal_0_111) 40)) false))
; source callback transition phase=insert-tail[0:11:2]:initial-compare
(define-fun formal_0_112 () FormalMachine (FormalCallback formal_0_111 boundary_0 (select (m_origin formal_0_111) 13) (select (m_origin formal_0_111) 40)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:2]
(define-fun formal_0_113 () FormalMachine (FormalWriteFromOrigin formal_0_112 2 40))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:2]:sift-compare
(assert (not (m_panicked formal_0_113)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_113) (select (m_origin formal_0_113) 13) (select (m_origin formal_0_113) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_113) (select (m_origin formal_0_113) 13) (select (m_origin formal_0_113) 12)) false))
; source callback transition phase=insert-tail[0:11:2]:sift-compare
(define-fun formal_0_114 () FormalMachine (FormalCallback formal_0_113 boundary_0 (select (m_origin formal_0_113) 13) (select (m_origin formal_0_113) 12)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:11:2]
(define-fun formal_0_115 () FormalMachine (FormalWriteFromOrigin formal_0_114 1 13))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:3]:initial-compare
(assert (not (m_panicked formal_0_115)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_115) (select (m_origin formal_0_115) 15) (select (m_origin formal_0_115) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_115) (select (m_origin formal_0_115) 15) (select (m_origin formal_0_115) 40)) false))
; source callback transition phase=insert-tail[0:11:3]:initial-compare
(define-fun formal_0_116 () FormalMachine (FormalCallback formal_0_115 boundary_0 (select (m_origin formal_0_115) 15) (select (m_origin formal_0_115) 40)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:3]
(define-fun formal_0_117 () FormalMachine (FormalWriteFromOrigin formal_0_116 3 40))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:3]:sift-compare
(assert (not (m_panicked formal_0_117)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_117) (select (m_origin formal_0_117) 15) (select (m_origin formal_0_117) 13)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_117) (select (m_origin formal_0_117) 15) (select (m_origin formal_0_117) 13)) false))
; source callback transition phase=insert-tail[0:11:3]:sift-compare
(define-fun formal_0_118 () FormalMachine (FormalCallback formal_0_117 boundary_0 (select (m_origin formal_0_117) 15) (select (m_origin formal_0_117) 13)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:11:3]
(define-fun formal_0_119 () FormalMachine (FormalWriteFromOrigin formal_0_118 2 15))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:4]:initial-compare
(assert (not (m_panicked formal_0_119)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_119) (select (m_origin formal_0_119) 16) (select (m_origin formal_0_119) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_119) (select (m_origin formal_0_119) 16) (select (m_origin formal_0_119) 40)) false))
; source callback transition phase=insert-tail[0:11:4]:initial-compare
(define-fun formal_0_120 () FormalMachine (FormalCallback formal_0_119 boundary_0 (select (m_origin formal_0_119) 16) (select (m_origin formal_0_119) 40)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:4]
(define-fun formal_0_121 () FormalMachine (FormalWriteFromOrigin formal_0_120 4 40))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:4]:sift-compare
(assert (not (m_panicked formal_0_121)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_121) (select (m_origin formal_0_121) 16) (select (m_origin formal_0_121) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_121) (select (m_origin formal_0_121) 16) (select (m_origin formal_0_121) 15)) false))
; source callback transition phase=insert-tail[0:11:4]:sift-compare
(define-fun formal_0_122 () FormalMachine (FormalCallback formal_0_121 boundary_0 (select (m_origin formal_0_121) 16) (select (m_origin formal_0_121) 15)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:4]
(define-fun formal_0_123 () FormalMachine (FormalWriteFromOrigin formal_0_122 3 15))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:4]:sift-compare
(assert (not (m_panicked formal_0_123)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_123) (select (m_origin formal_0_123) 16) (select (m_origin formal_0_123) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_123) (select (m_origin formal_0_123) 16) (select (m_origin formal_0_123) 13)) false))
; source callback transition phase=insert-tail[0:11:4]:sift-compare
(define-fun formal_0_124 () FormalMachine (FormalCallback formal_0_123 boundary_0 (select (m_origin formal_0_123) 16) (select (m_origin formal_0_123) 13)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:4]
(define-fun formal_0_125 () FormalMachine (FormalWriteFromOrigin formal_0_124 2 13))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:4]:sift-compare
(assert (not (m_panicked formal_0_125)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_125) (select (m_origin formal_0_125) 16) (select (m_origin formal_0_125) 12)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_125) (select (m_origin formal_0_125) 16) (select (m_origin formal_0_125) 12)) false))
; source callback transition phase=insert-tail[0:11:4]:sift-compare
(define-fun formal_0_126 () FormalMachine (FormalCallback formal_0_125 boundary_0 (select (m_origin formal_0_125) 16) (select (m_origin formal_0_125) 12)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:4]
(define-fun formal_0_127 () FormalMachine (FormalWriteFromOrigin formal_0_126 1 12))
; source write kind=copy-on-drop-restore phase=insert-tail[0:11:4]
(define-fun formal_0_128 () FormalMachine (FormalWriteFromOrigin formal_0_127 0 16))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:5]:initial-compare
(assert (not (m_panicked formal_0_128)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 0) (select (m_origin formal_0_128) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_128) (select (m_origin formal_0_128) 0) (select (m_origin formal_0_128) 40)) false))
; source callback transition phase=insert-tail[0:11:5]:initial-compare
(define-fun formal_0_129 () FormalMachine (FormalCallback formal_0_128 boundary_0 (select (m_origin formal_0_128) 0) (select (m_origin formal_0_128) 40)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:5]
(define-fun formal_0_130 () FormalMachine (FormalWriteFromOrigin formal_0_129 5 40))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:5]:sift-compare
(assert (not (m_panicked formal_0_130)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_130) (select (m_origin formal_0_130) 0) (select (m_origin formal_0_130) 15)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_130) (select (m_origin formal_0_130) 0) (select (m_origin formal_0_130) 15)) false))
; source callback transition phase=insert-tail[0:11:5]:sift-compare
(define-fun formal_0_131 () FormalMachine (FormalCallback formal_0_130 boundary_0 (select (m_origin formal_0_130) 0) (select (m_origin formal_0_130) 15)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:11:5]
(define-fun formal_0_132 () FormalMachine (FormalWriteFromOrigin formal_0_131 4 0))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:6]:initial-compare
(assert (not (m_panicked formal_0_132)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_132) (select (m_origin formal_0_132) 22) (select (m_origin formal_0_132) 40)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_132) (select (m_origin formal_0_132) 22) (select (m_origin formal_0_132) 40)) false))
; source callback transition phase=insert-tail[0:11:6]:initial-compare
(define-fun formal_0_133 () FormalMachine (FormalCallback formal_0_132 boundary_0 (select (m_origin formal_0_132) 22) (select (m_origin formal_0_132) 40)))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:7]:initial-compare
(assert (not (m_panicked formal_0_133)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_133) (select (m_origin formal_0_133) 24) (select (m_origin formal_0_133) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_133) (select (m_origin formal_0_133) 24) (select (m_origin formal_0_133) 22)) false))
; source callback transition phase=insert-tail[0:11:7]:initial-compare
(define-fun formal_0_134 () FormalMachine (FormalCallback formal_0_133 boundary_0 (select (m_origin formal_0_133) 24) (select (m_origin formal_0_133) 22)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:7]
(define-fun formal_0_135 () FormalMachine (FormalWriteFromOrigin formal_0_134 7 22))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:7]:sift-compare
(assert (not (m_panicked formal_0_135)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_135) (select (m_origin formal_0_135) 24) (select (m_origin formal_0_135) 40)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_135) (select (m_origin formal_0_135) 24) (select (m_origin formal_0_135) 40)) false))
; source callback transition phase=insert-tail[0:11:7]:sift-compare
(define-fun formal_0_136 () FormalMachine (FormalCallback formal_0_135 boundary_0 (select (m_origin formal_0_135) 24) (select (m_origin formal_0_135) 40)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:11:7]
(define-fun formal_0_137 () FormalMachine (FormalWriteFromOrigin formal_0_136 6 24))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:8]:initial-compare
(assert (not (m_panicked formal_0_137)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_137) (select (m_origin formal_0_137) 31) (select (m_origin formal_0_137) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_137) (select (m_origin formal_0_137) 31) (select (m_origin formal_0_137) 22)) false))
; source callback transition phase=insert-tail[0:11:8]:initial-compare
(define-fun formal_0_138 () FormalMachine (FormalCallback formal_0_137 boundary_0 (select (m_origin formal_0_137) 31) (select (m_origin formal_0_137) 22)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:8]
(define-fun formal_0_139 () FormalMachine (FormalWriteFromOrigin formal_0_138 8 22))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:8]:sift-compare
(assert (not (m_panicked formal_0_139)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_139) (select (m_origin formal_0_139) 31) (select (m_origin formal_0_139) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_139) (select (m_origin formal_0_139) 31) (select (m_origin formal_0_139) 24)) false))
; source callback transition phase=insert-tail[0:11:8]:sift-compare
(define-fun formal_0_140 () FormalMachine (FormalCallback formal_0_139 boundary_0 (select (m_origin formal_0_139) 31) (select (m_origin formal_0_139) 24)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:8]
(define-fun formal_0_141 () FormalMachine (FormalWriteFromOrigin formal_0_140 7 24))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:8]:sift-compare
(assert (not (m_panicked formal_0_141)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_141) (select (m_origin formal_0_141) 31) (select (m_origin formal_0_141) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_141) (select (m_origin formal_0_141) 31) (select (m_origin formal_0_141) 40)) false))
; source callback transition phase=insert-tail[0:11:8]:sift-compare
(define-fun formal_0_142 () FormalMachine (FormalCallback formal_0_141 boundary_0 (select (m_origin formal_0_141) 31) (select (m_origin formal_0_141) 40)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:8]
(define-fun formal_0_143 () FormalMachine (FormalWriteFromOrigin formal_0_142 6 40))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:8]:sift-compare
(assert (not (m_panicked formal_0_143)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_143) (select (m_origin formal_0_143) 31) (select (m_origin formal_0_143) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_143) (select (m_origin formal_0_143) 31) (select (m_origin formal_0_143) 0)) false))
; source callback transition phase=insert-tail[0:11:8]:sift-compare
(define-fun formal_0_144 () FormalMachine (FormalCallback formal_0_143 boundary_0 (select (m_origin formal_0_143) 31) (select (m_origin formal_0_143) 0)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:11:8]
(define-fun formal_0_145 () FormalMachine (FormalWriteFromOrigin formal_0_144 5 31))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:9]:initial-compare
(assert (not (m_panicked formal_0_145)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_145) (select (m_origin formal_0_145) 36) (select (m_origin formal_0_145) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_145) (select (m_origin formal_0_145) 36) (select (m_origin formal_0_145) 22)) false))
; source callback transition phase=insert-tail[0:11:9]:initial-compare
(define-fun formal_0_146 () FormalMachine (FormalCallback formal_0_145 boundary_0 (select (m_origin formal_0_145) 36) (select (m_origin formal_0_145) 22)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:9]
(define-fun formal_0_147 () FormalMachine (FormalWriteFromOrigin formal_0_146 9 22))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:9]:sift-compare
(assert (not (m_panicked formal_0_147)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_147) (select (m_origin formal_0_147) 36) (select (m_origin formal_0_147) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_147) (select (m_origin formal_0_147) 36) (select (m_origin formal_0_147) 24)) false))
; source callback transition phase=insert-tail[0:11:9]:sift-compare
(define-fun formal_0_148 () FormalMachine (FormalCallback formal_0_147 boundary_0 (select (m_origin formal_0_147) 36) (select (m_origin formal_0_147) 24)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:9]
(define-fun formal_0_149 () FormalMachine (FormalWriteFromOrigin formal_0_148 8 24))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:9]:sift-compare
(assert (not (m_panicked formal_0_149)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_149) (select (m_origin formal_0_149) 36) (select (m_origin formal_0_149) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_149) (select (m_origin formal_0_149) 36) (select (m_origin formal_0_149) 40)) false))
; source callback transition phase=insert-tail[0:11:9]:sift-compare
(define-fun formal_0_150 () FormalMachine (FormalCallback formal_0_149 boundary_0 (select (m_origin formal_0_149) 36) (select (m_origin formal_0_149) 40)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:9]
(define-fun formal_0_151 () FormalMachine (FormalWriteFromOrigin formal_0_150 7 40))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:9]:sift-compare
(assert (not (m_panicked formal_0_151)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_151) (select (m_origin formal_0_151) 36) (select (m_origin formal_0_151) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_151) (select (m_origin formal_0_151) 36) (select (m_origin formal_0_151) 31)) false))
; source callback transition phase=insert-tail[0:11:9]:sift-compare
(define-fun formal_0_152 () FormalMachine (FormalCallback formal_0_151 boundary_0 (select (m_origin formal_0_151) 36) (select (m_origin formal_0_151) 31)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:9]
(define-fun formal_0_153 () FormalMachine (FormalWriteFromOrigin formal_0_152 6 31))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:9]:sift-compare
(assert (not (m_panicked formal_0_153)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_153) (select (m_origin formal_0_153) 36) (select (m_origin formal_0_153) 0)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_153) (select (m_origin formal_0_153) 36) (select (m_origin formal_0_153) 0)) false))
; source callback transition phase=insert-tail[0:11:9]:sift-compare
(define-fun formal_0_154 () FormalMachine (FormalCallback formal_0_153 boundary_0 (select (m_origin formal_0_153) 36) (select (m_origin formal_0_153) 0)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:9]
(define-fun formal_0_155 () FormalMachine (FormalWriteFromOrigin formal_0_154 5 0))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:9]:sift-compare
(assert (not (m_panicked formal_0_155)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 36) (select (m_origin formal_0_155) 15)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_155) (select (m_origin formal_0_155) 36) (select (m_origin formal_0_155) 15)) false))
; source callback transition phase=insert-tail[0:11:9]:sift-compare
(define-fun formal_0_156 () FormalMachine (FormalCallback formal_0_155 boundary_0 (select (m_origin formal_0_155) 36) (select (m_origin formal_0_155) 15)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:9]
(define-fun formal_0_157 () FormalMachine (FormalWriteFromOrigin formal_0_156 4 15))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:9]:sift-compare
(assert (not (m_panicked formal_0_157)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_157) (select (m_origin formal_0_157) 36) (select (m_origin formal_0_157) 13)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_157) (select (m_origin formal_0_157) 36) (select (m_origin formal_0_157) 13)) false))
; source callback transition phase=insert-tail[0:11:9]:sift-compare
(define-fun formal_0_158 () FormalMachine (FormalCallback formal_0_157 boundary_0 (select (m_origin formal_0_157) 36) (select (m_origin formal_0_157) 13)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:9]
(define-fun formal_0_159 () FormalMachine (FormalWriteFromOrigin formal_0_158 3 13))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:9]:sift-compare
(assert (not (m_panicked formal_0_159)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_159) (select (m_origin formal_0_159) 36) (select (m_origin formal_0_159) 12)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_159) (select (m_origin formal_0_159) 36) (select (m_origin formal_0_159) 12)) false))
; source callback transition phase=insert-tail[0:11:9]:sift-compare
(define-fun formal_0_160 () FormalMachine (FormalCallback formal_0_159 boundary_0 (select (m_origin formal_0_159) 36) (select (m_origin formal_0_159) 12)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:11:9]
(define-fun formal_0_161 () FormalMachine (FormalWriteFromOrigin formal_0_160 2 36))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:10]:initial-compare
(assert (not (m_panicked formal_0_161)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_161) (select (m_origin formal_0_161) 37) (select (m_origin formal_0_161) 22)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_161) (select (m_origin formal_0_161) 37) (select (m_origin formal_0_161) 22)) false))
; source callback transition phase=insert-tail[0:11:10]:initial-compare
(define-fun formal_0_162 () FormalMachine (FormalCallback formal_0_161 boundary_0 (select (m_origin formal_0_161) 37) (select (m_origin formal_0_161) 22)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:10]
(define-fun formal_0_163 () FormalMachine (FormalWriteFromOrigin formal_0_162 10 22))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:10]:sift-compare
(assert (not (m_panicked formal_0_163)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_163) (select (m_origin formal_0_163) 37) (select (m_origin formal_0_163) 24)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_163) (select (m_origin formal_0_163) 37) (select (m_origin formal_0_163) 24)) false))
; source callback transition phase=insert-tail[0:11:10]:sift-compare
(define-fun formal_0_164 () FormalMachine (FormalCallback formal_0_163 boundary_0 (select (m_origin formal_0_163) 37) (select (m_origin formal_0_163) 24)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:10]
(define-fun formal_0_165 () FormalMachine (FormalWriteFromOrigin formal_0_164 9 24))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:10]:sift-compare
(assert (not (m_panicked formal_0_165)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_165) (select (m_origin formal_0_165) 37) (select (m_origin formal_0_165) 40)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_165) (select (m_origin formal_0_165) 37) (select (m_origin formal_0_165) 40)) false))
; source callback transition phase=insert-tail[0:11:10]:sift-compare
(define-fun formal_0_166 () FormalMachine (FormalCallback formal_0_165 boundary_0 (select (m_origin formal_0_165) 37) (select (m_origin formal_0_165) 40)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:10]
(define-fun formal_0_167 () FormalMachine (FormalWriteFromOrigin formal_0_166 8 40))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:10]:sift-compare
(assert (not (m_panicked formal_0_167)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_167) (select (m_origin formal_0_167) 37) (select (m_origin formal_0_167) 31)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_167) (select (m_origin formal_0_167) 37) (select (m_origin formal_0_167) 31)) false))
; source callback transition phase=insert-tail[0:11:10]:sift-compare
(define-fun formal_0_168 () FormalMachine (FormalCallback formal_0_167 boundary_0 (select (m_origin formal_0_167) 37) (select (m_origin formal_0_167) 31)))
; source write kind=insert-tail-shift phase=insert-tail[0:11:10]
(define-fun formal_0_169 () FormalMachine (FormalWriteFromOrigin formal_0_168 7 31))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[0:11:10]:sift-compare
(assert (not (m_panicked formal_0_169)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_169) (select (m_origin formal_0_169) 37) (select (m_origin formal_0_169) 0)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_169) (select (m_origin formal_0_169) 37) (select (m_origin formal_0_169) 0)) false))
; source callback transition phase=insert-tail[0:11:10]:sift-compare
(define-fun formal_0_170 () FormalMachine (FormalCallback formal_0_169 boundary_0 (select (m_origin formal_0_169) 37) (select (m_origin formal_0_169) 0)))
; source write kind=copy-on-drop-restore phase=insert-tail[0:11:10]
(define-fun formal_0_171 () FormalMachine (FormalWriteFromOrigin formal_0_170 6 37))
; source callback case=fallback-small-sort-and-recursion phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_171)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_171) (select (m_origin formal_0_171) 1) (select (m_origin formal_0_171) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_171) (select (m_origin formal_0_171) 1) (select (m_origin formal_0_171) 28)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_172 () FormalMachine (FormalCallback formal_0_171 boundary_0 (select (m_origin formal_0_171) 1) (select (m_origin formal_0_171) 28)))
; source callback case=fallback-small-sort-and-recursion phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_172)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_172) (select (m_origin formal_0_172) 1) (select (m_origin formal_0_172) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_172) (select (m_origin formal_0_172) 1) (select (m_origin formal_0_172) 2)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_173 () FormalMachine (FormalCallback formal_0_172 boundary_0 (select (m_origin formal_0_172) 1) (select (m_origin formal_0_172) 2)))
; source callback case=fallback-small-sort-and-recursion phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_173)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_173) (select (m_origin formal_0_173) 28) (select (m_origin formal_0_173) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_173) (select (m_origin formal_0_173) 28) (select (m_origin formal_0_173) 2)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_174 () FormalMachine (FormalCallback formal_0_173 boundary_0 (select (m_origin formal_0_173) 28) (select (m_origin formal_0_173) 2)))
; source callback case=fallback-small-sort-and-recursion phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_174)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_174) (select (m_origin formal_0_174) 20) (select (m_origin formal_0_174) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_174) (select (m_origin formal_0_174) 20) (select (m_origin formal_0_174) 28)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_175 () FormalMachine (FormalCallback formal_0_174 boundary_0 (select (m_origin formal_0_174) 20) (select (m_origin formal_0_174) 28)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_176 () FormalMachine (FormalSwap formal_0_175 12 28))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_176)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 14) (select (m_origin formal_0_176) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_176) (select (m_origin formal_0_176) 14) (select (m_origin formal_0_176) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_177 () FormalMachine (FormalCallback formal_0_176 boundary_0 (select (m_origin formal_0_176) 14) (select (m_origin formal_0_176) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_178 () FormalMachine (FormalWriteFromOrigin formal_0_177 13 14))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_178)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_178) (select (m_origin formal_0_178) 4) (select (m_origin formal_0_178) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_178) (select (m_origin formal_0_178) 4) (select (m_origin formal_0_178) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_179 () FormalMachine (FormalCallback formal_0_178 boundary_0 (select (m_origin formal_0_178) 4) (select (m_origin formal_0_178) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_180 () FormalMachine (FormalWriteFromOrigin formal_0_179 13 4))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_180)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_180) (select (m_origin formal_0_180) 5) (select (m_origin formal_0_180) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_180) (select (m_origin formal_0_180) 5) (select (m_origin formal_0_180) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_181 () FormalMachine (FormalCallback formal_0_180 boundary_0 (select (m_origin formal_0_180) 5) (select (m_origin formal_0_180) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_182 () FormalMachine (FormalWriteFromOrigin formal_0_181 14 5))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_183 () FormalMachine (FormalWriteFromOrigin formal_0_182 15 14))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_183)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_183) (select (m_origin formal_0_183) 17) (select (m_origin formal_0_183) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_183) (select (m_origin formal_0_183) 17) (select (m_origin formal_0_183) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_184 () FormalMachine (FormalCallback formal_0_183 boundary_0 (select (m_origin formal_0_183) 17) (select (m_origin formal_0_183) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_185 () FormalMachine (FormalWriteFromOrigin formal_0_184 15 17))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_186 () FormalMachine (FormalWriteFromOrigin formal_0_185 16 14))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_186)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_186) (select (m_origin formal_0_186) 18) (select (m_origin formal_0_186) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_186) (select (m_origin formal_0_186) 18) (select (m_origin formal_0_186) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_187 () FormalMachine (FormalCallback formal_0_186 boundary_0 (select (m_origin formal_0_186) 18) (select (m_origin formal_0_186) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_188 () FormalMachine (FormalWriteFromOrigin formal_0_187 16 18))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_189 () FormalMachine (FormalWriteFromOrigin formal_0_188 17 14))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_189)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_189) (select (m_origin formal_0_189) 19) (select (m_origin formal_0_189) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_189) (select (m_origin formal_0_189) 19) (select (m_origin formal_0_189) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_190 () FormalMachine (FormalCallback formal_0_189 boundary_0 (select (m_origin formal_0_189) 19) (select (m_origin formal_0_189) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_191 () FormalMachine (FormalWriteFromOrigin formal_0_190 17 19))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_192 () FormalMachine (FormalWriteFromOrigin formal_0_191 18 14))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_192)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_192) (select (m_origin formal_0_192) 6) (select (m_origin formal_0_192) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_192) (select (m_origin formal_0_192) 6) (select (m_origin formal_0_192) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_193 () FormalMachine (FormalCallback formal_0_192 boundary_0 (select (m_origin formal_0_192) 6) (select (m_origin formal_0_192) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_194 () FormalMachine (FormalWriteFromOrigin formal_0_193 18 6))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_195 () FormalMachine (FormalWriteFromOrigin formal_0_194 19 14))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_195)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_195) (select (m_origin formal_0_195) 21) (select (m_origin formal_0_195) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_195) (select (m_origin formal_0_195) 21) (select (m_origin formal_0_195) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_196 () FormalMachine (FormalCallback formal_0_195 boundary_0 (select (m_origin formal_0_195) 21) (select (m_origin formal_0_195) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_197 () FormalMachine (FormalWriteFromOrigin formal_0_196 19 21))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_198 () FormalMachine (FormalWriteFromOrigin formal_0_197 20 14))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_198)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_198) (select (m_origin formal_0_198) 7) (select (m_origin formal_0_198) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_198) (select (m_origin formal_0_198) 7) (select (m_origin formal_0_198) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_199 () FormalMachine (FormalCallback formal_0_198 boundary_0 (select (m_origin formal_0_198) 7) (select (m_origin formal_0_198) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_200 () FormalMachine (FormalWriteFromOrigin formal_0_199 19 7))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_200)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_200) (select (m_origin formal_0_200) 23) (select (m_origin formal_0_200) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_200) (select (m_origin formal_0_200) 23) (select (m_origin formal_0_200) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_201 () FormalMachine (FormalCallback formal_0_200 boundary_0 (select (m_origin formal_0_200) 23) (select (m_origin formal_0_200) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_202 () FormalMachine (FormalWriteFromOrigin formal_0_201 19 23))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_202)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_202) (select (m_origin formal_0_202) 8) (select (m_origin formal_0_202) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_202) (select (m_origin formal_0_202) 8) (select (m_origin formal_0_202) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_203 () FormalMachine (FormalCallback formal_0_202 boundary_0 (select (m_origin formal_0_202) 8) (select (m_origin formal_0_202) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_204 () FormalMachine (FormalWriteFromOrigin formal_0_203 19 8))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_204)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_204) (select (m_origin formal_0_204) 25) (select (m_origin formal_0_204) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_204) (select (m_origin formal_0_204) 25) (select (m_origin formal_0_204) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_205 () FormalMachine (FormalCallback formal_0_204 boundary_0 (select (m_origin formal_0_204) 25) (select (m_origin formal_0_204) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_206 () FormalMachine (FormalWriteFromOrigin formal_0_205 19 25))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_206)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_206) (select (m_origin formal_0_206) 26) (select (m_origin formal_0_206) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_206) (select (m_origin formal_0_206) 26) (select (m_origin formal_0_206) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_207 () FormalMachine (FormalCallback formal_0_206 boundary_0 (select (m_origin formal_0_206) 26) (select (m_origin formal_0_206) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_208 () FormalMachine (FormalWriteFromOrigin formal_0_207 20 26))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_209 () FormalMachine (FormalWriteFromOrigin formal_0_208 25 14))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_209)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_209) (select (m_origin formal_0_209) 27) (select (m_origin formal_0_209) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_209) (select (m_origin formal_0_209) 27) (select (m_origin formal_0_209) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_210 () FormalMachine (FormalCallback formal_0_209 boundary_0 (select (m_origin formal_0_209) 27) (select (m_origin formal_0_209) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_211 () FormalMachine (FormalWriteFromOrigin formal_0_210 21 27))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_212 () FormalMachine (FormalWriteFromOrigin formal_0_211 26 21))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_212)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_212) (select (m_origin formal_0_212) 1) (select (m_origin formal_0_212) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_212) (select (m_origin formal_0_212) 1) (select (m_origin formal_0_212) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_213 () FormalMachine (FormalCallback formal_0_212 boundary_0 (select (m_origin formal_0_212) 1) (select (m_origin formal_0_212) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_214 () FormalMachine (FormalWriteFromOrigin formal_0_213 22 1))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_215 () FormalMachine (FormalWriteFromOrigin formal_0_214 27 7))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_215)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_215) (select (m_origin formal_0_215) 29) (select (m_origin formal_0_215) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_215) (select (m_origin formal_0_215) 29) (select (m_origin formal_0_215) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_216 () FormalMachine (FormalCallback formal_0_215 boundary_0 (select (m_origin formal_0_215) 29) (select (m_origin formal_0_215) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_217 () FormalMachine (FormalWriteFromOrigin formal_0_216 23 29))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_218 () FormalMachine (FormalWriteFromOrigin formal_0_217 28 23))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_218)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_218) (select (m_origin formal_0_218) 30) (select (m_origin formal_0_218) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_218) (select (m_origin formal_0_218) 30) (select (m_origin formal_0_218) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_219 () FormalMachine (FormalCallback formal_0_218 boundary_0 (select (m_origin formal_0_218) 30) (select (m_origin formal_0_218) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_220 () FormalMachine (FormalWriteFromOrigin formal_0_219 24 30))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_221 () FormalMachine (FormalWriteFromOrigin formal_0_220 29 8))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_221)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_221) (select (m_origin formal_0_221) 9) (select (m_origin formal_0_221) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_221) (select (m_origin formal_0_221) 9) (select (m_origin formal_0_221) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_222 () FormalMachine (FormalCallback formal_0_221 boundary_0 (select (m_origin formal_0_221) 9) (select (m_origin formal_0_221) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_223 () FormalMachine (FormalWriteFromOrigin formal_0_222 24 9))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_223)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_223) (select (m_origin formal_0_223) 32) (select (m_origin formal_0_223) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_223) (select (m_origin formal_0_223) 32) (select (m_origin formal_0_223) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_224 () FormalMachine (FormalCallback formal_0_223 boundary_0 (select (m_origin formal_0_223) 32) (select (m_origin formal_0_223) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_225 () FormalMachine (FormalWriteFromOrigin formal_0_224 25 32))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_226 () FormalMachine (FormalWriteFromOrigin formal_0_225 31 14))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_226)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_226) (select (m_origin formal_0_226) 33) (select (m_origin formal_0_226) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_226) (select (m_origin formal_0_226) 33) (select (m_origin formal_0_226) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_227 () FormalMachine (FormalCallback formal_0_226 boundary_0 (select (m_origin formal_0_226) 33) (select (m_origin formal_0_226) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_228 () FormalMachine (FormalWriteFromOrigin formal_0_227 26 33))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_229 () FormalMachine (FormalWriteFromOrigin formal_0_228 32 21))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_229)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_229) (select (m_origin formal_0_229) 34) (select (m_origin formal_0_229) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_229) (select (m_origin formal_0_229) 34) (select (m_origin formal_0_229) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_230 () FormalMachine (FormalCallback formal_0_229 boundary_0 (select (m_origin formal_0_229) 34) (select (m_origin formal_0_229) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_231 () FormalMachine (FormalWriteFromOrigin formal_0_230 27 34))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_232 () FormalMachine (FormalWriteFromOrigin formal_0_231 33 7))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_232)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_232) (select (m_origin formal_0_232) 35) (select (m_origin formal_0_232) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_232) (select (m_origin formal_0_232) 35) (select (m_origin formal_0_232) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_233 () FormalMachine (FormalCallback formal_0_232 boundary_0 (select (m_origin formal_0_232) 35) (select (m_origin formal_0_232) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_234 () FormalMachine (FormalWriteFromOrigin formal_0_233 27 35))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_234)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_234) (select (m_origin formal_0_234) 10) (select (m_origin formal_0_234) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_234) (select (m_origin formal_0_234) 10) (select (m_origin formal_0_234) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_235 () FormalMachine (FormalCallback formal_0_234 boundary_0 (select (m_origin formal_0_234) 10) (select (m_origin formal_0_234) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_236 () FormalMachine (FormalWriteFromOrigin formal_0_235 28 10))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_237 () FormalMachine (FormalWriteFromOrigin formal_0_236 35 23))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_237)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_237) (select (m_origin formal_0_237) 11) (select (m_origin formal_0_237) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_237) (select (m_origin formal_0_237) 11) (select (m_origin formal_0_237) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_238 () FormalMachine (FormalCallback formal_0_237 boundary_0 (select (m_origin formal_0_237) 11) (select (m_origin formal_0_237) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_239 () FormalMachine (FormalWriteFromOrigin formal_0_238 29 11))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_240 () FormalMachine (FormalWriteFromOrigin formal_0_239 36 8))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_240)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_240) (select (m_origin formal_0_240) 38) (select (m_origin formal_0_240) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_240) (select (m_origin formal_0_240) 38) (select (m_origin formal_0_240) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_241 () FormalMachine (FormalCallback formal_0_240 boundary_0 (select (m_origin formal_0_240) 38) (select (m_origin formal_0_240) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_242 () FormalMachine (FormalWriteFromOrigin formal_0_241 30 38))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_243 () FormalMachine (FormalWriteFromOrigin formal_0_242 37 30))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_243)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_243) (select (m_origin formal_0_243) 39) (select (m_origin formal_0_243) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_243) (select (m_origin formal_0_243) 39) (select (m_origin formal_0_243) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_244 () FormalMachine (FormalCallback formal_0_243 boundary_0 (select (m_origin formal_0_243) 39) (select (m_origin formal_0_243) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_245 () FormalMachine (FormalWriteFromOrigin formal_0_244 31 39))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_246 () FormalMachine (FormalWriteFromOrigin formal_0_245 38 14))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_246)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_246) (select (m_origin formal_0_246) 2) (select (m_origin formal_0_246) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_246) (select (m_origin formal_0_246) 2) (select (m_origin formal_0_246) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_247 () FormalMachine (FormalCallback formal_0_246 boundary_0 (select (m_origin formal_0_246) 2) (select (m_origin formal_0_246) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_248 () FormalMachine (FormalWriteFromOrigin formal_0_247 32 2))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_249 () FormalMachine (FormalWriteFromOrigin formal_0_248 39 21))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_249)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_249) (select (m_origin formal_0_249) 41) (select (m_origin formal_0_249) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_249) (select (m_origin formal_0_249) 41) (select (m_origin formal_0_249) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_250 () FormalMachine (FormalCallback formal_0_249 boundary_0 (select (m_origin formal_0_249) 41) (select (m_origin formal_0_249) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_251 () FormalMachine (FormalWriteFromOrigin formal_0_250 32 41))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_251)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_251) (select (m_origin formal_0_251) 42) (select (m_origin formal_0_251) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_251) (select (m_origin formal_0_251) 42) (select (m_origin formal_0_251) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_252 () FormalMachine (FormalCallback formal_0_251 boundary_0 (select (m_origin formal_0_251) 42) (select (m_origin formal_0_251) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_253 () FormalMachine (FormalWriteFromOrigin formal_0_252 33 42))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_254 () FormalMachine (FormalWriteFromOrigin formal_0_253 41 7))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_254)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_254) (select (m_origin formal_0_254) 43) (select (m_origin formal_0_254) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_254) (select (m_origin formal_0_254) 43) (select (m_origin formal_0_254) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_255 () FormalMachine (FormalCallback formal_0_254 boundary_0 (select (m_origin formal_0_254) 43) (select (m_origin formal_0_254) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_256 () FormalMachine (FormalWriteFromOrigin formal_0_255 34 43))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_257 () FormalMachine (FormalWriteFromOrigin formal_0_256 42 34))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_257)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_257) (select (m_origin formal_0_257) 44) (select (m_origin formal_0_257) 28)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_257) (select (m_origin formal_0_257) 44) (select (m_origin formal_0_257) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_258 () FormalMachine (FormalCallback formal_0_257 boundary_0 (select (m_origin formal_0_257) 44) (select (m_origin formal_0_257) 28)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_259 () FormalMachine (FormalWriteFromOrigin formal_0_258 35 44))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_260 () FormalMachine (FormalWriteFromOrigin formal_0_259 43 23))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_260)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_260) (select (m_origin formal_0_260) 3) (select (m_origin formal_0_260) 28)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_260) (select (m_origin formal_0_260) 3) (select (m_origin formal_0_260) 28)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_261 () FormalMachine (FormalCallback formal_0_260 boundary_0 (select (m_origin formal_0_260) 3) (select (m_origin formal_0_260) 28)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_262 () FormalMachine (FormalWriteFromOrigin formal_0_261 36 3))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_263 () FormalMachine (FormalWriteFromOrigin formal_0_262 44 8))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_264 () FormalMachine (FormalSwap formal_0_263 12 35))
; source callback case=fallback-small-sort-and-recursion phase=choose-pivot:median3:a-b
(assert (not (m_panicked formal_0_264)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_264) (select (m_origin formal_0_264) 44) (select (m_origin formal_0_264) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_264) (select (m_origin formal_0_264) 44) (select (m_origin formal_0_264) 26)) false))
; source callback transition phase=choose-pivot:median3:a-b
(define-fun formal_0_265 () FormalMachine (FormalCallback formal_0_264 boundary_0 (select (m_origin formal_0_264) 44) (select (m_origin formal_0_264) 26)))
; source callback case=fallback-small-sort-and-recursion phase=choose-pivot:median3:a-c
(assert (not (m_panicked formal_0_265)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_265) (select (m_origin formal_0_265) 44) (select (m_origin formal_0_265) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_265) (select (m_origin formal_0_265) 44) (select (m_origin formal_0_265) 33)) false))
; source callback transition phase=choose-pivot:median3:a-c
(define-fun formal_0_266 () FormalMachine (FormalCallback formal_0_265 boundary_0 (select (m_origin formal_0_265) 44) (select (m_origin formal_0_265) 33)))
; source callback case=fallback-small-sort-and-recursion phase=choose-pivot:median3:b-c
(assert (not (m_panicked formal_0_266)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_266) (select (m_origin formal_0_266) 26) (select (m_origin formal_0_266) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_266) (select (m_origin formal_0_266) 26) (select (m_origin formal_0_266) 33)) false))
; source callback transition phase=choose-pivot:median3:b-c
(define-fun formal_0_267 () FormalMachine (FormalCallback formal_0_266 boundary_0 (select (m_origin formal_0_266) 26) (select (m_origin formal_0_266) 33)))
; source callback case=fallback-small-sort-and-recursion phase=quicksort:ancestor-pivot-compare
(assert (not (m_panicked formal_0_267)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_267) (select (m_origin formal_0_267) 20) (select (m_origin formal_0_267) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_267) (select (m_origin formal_0_267) 20) (select (m_origin formal_0_267) 33)) false))
; source callback transition phase=quicksort:ancestor-pivot-compare
(define-fun formal_0_268 () FormalMachine (FormalCallback formal_0_267 boundary_0 (select (m_origin formal_0_267) 20) (select (m_origin formal_0_267) 33)))
; source swap phase=partition:pivot-to-front
(define-fun formal_0_269 () FormalMachine (FormalSwap formal_0_268 12 26))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_269)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_269) (select (m_origin formal_0_269) 5) (select (m_origin formal_0_269) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_269) (select (m_origin formal_0_269) 5) (select (m_origin formal_0_269) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_270 () FormalMachine (FormalCallback formal_0_269 boundary_0 (select (m_origin formal_0_269) 5) (select (m_origin formal_0_269) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_271 () FormalMachine (FormalWriteFromOrigin formal_0_270 13 5))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_271)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_271) (select (m_origin formal_0_271) 17) (select (m_origin formal_0_271) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_271) (select (m_origin formal_0_271) 17) (select (m_origin formal_0_271) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_272 () FormalMachine (FormalCallback formal_0_271 boundary_0 (select (m_origin formal_0_271) 17) (select (m_origin formal_0_271) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_273 () FormalMachine (FormalWriteFromOrigin formal_0_272 13 17))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_273)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_273) (select (m_origin formal_0_273) 18) (select (m_origin formal_0_273) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_273) (select (m_origin formal_0_273) 18) (select (m_origin formal_0_273) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_274 () FormalMachine (FormalCallback formal_0_273 boundary_0 (select (m_origin formal_0_273) 18) (select (m_origin formal_0_273) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_275 () FormalMachine (FormalWriteFromOrigin formal_0_274 13 18))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_275)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_275) (select (m_origin formal_0_275) 19) (select (m_origin formal_0_275) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_275) (select (m_origin formal_0_275) 19) (select (m_origin formal_0_275) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_276 () FormalMachine (FormalCallback formal_0_275 boundary_0 (select (m_origin formal_0_275) 19) (select (m_origin formal_0_275) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_277 () FormalMachine (FormalWriteFromOrigin formal_0_276 14 19))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_278 () FormalMachine (FormalWriteFromOrigin formal_0_277 16 5))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_278)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_278) (select (m_origin formal_0_278) 6) (select (m_origin formal_0_278) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_278) (select (m_origin formal_0_278) 6) (select (m_origin formal_0_278) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_279 () FormalMachine (FormalCallback formal_0_278 boundary_0 (select (m_origin formal_0_278) 6) (select (m_origin formal_0_278) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_280 () FormalMachine (FormalWriteFromOrigin formal_0_279 15 6))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_281 () FormalMachine (FormalWriteFromOrigin formal_0_280 17 17))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_281)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_281) (select (m_origin formal_0_281) 25) (select (m_origin formal_0_281) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_281) (select (m_origin formal_0_281) 25) (select (m_origin formal_0_281) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_282 () FormalMachine (FormalCallback formal_0_281 boundary_0 (select (m_origin formal_0_281) 25) (select (m_origin formal_0_281) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_283 () FormalMachine (FormalWriteFromOrigin formal_0_282 15 25))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_283)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_283) (select (m_origin formal_0_283) 26) (select (m_origin formal_0_283) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_283) (select (m_origin formal_0_283) 26) (select (m_origin formal_0_283) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_284 () FormalMachine (FormalCallback formal_0_283 boundary_0 (select (m_origin formal_0_283) 26) (select (m_origin formal_0_283) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_285 () FormalMachine (FormalWriteFromOrigin formal_0_284 16 26))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_286 () FormalMachine (FormalWriteFromOrigin formal_0_285 19 5))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_286)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 27) (select (m_origin formal_0_286) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_286) (select (m_origin formal_0_286) 27) (select (m_origin formal_0_286) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_287 () FormalMachine (FormalCallback formal_0_286 boundary_0 (select (m_origin formal_0_286) 27) (select (m_origin formal_0_286) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_288 () FormalMachine (FormalWriteFromOrigin formal_0_287 16 27))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_288)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 1) (select (m_origin formal_0_288) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_288) (select (m_origin formal_0_288) 1) (select (m_origin formal_0_288) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_289 () FormalMachine (FormalCallback formal_0_288 boundary_0 (select (m_origin formal_0_288) 1) (select (m_origin formal_0_288) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_290 () FormalMachine (FormalWriteFromOrigin formal_0_289 16 1))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_290)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_290) (select (m_origin formal_0_290) 29) (select (m_origin formal_0_290) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_290) (select (m_origin formal_0_290) 29) (select (m_origin formal_0_290) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_291 () FormalMachine (FormalCallback formal_0_290 boundary_0 (select (m_origin formal_0_290) 29) (select (m_origin formal_0_290) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_292 () FormalMachine (FormalWriteFromOrigin formal_0_291 16 29))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_292)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 9) (select (m_origin formal_0_292) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_292) (select (m_origin formal_0_292) 9) (select (m_origin formal_0_292) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_293 () FormalMachine (FormalCallback formal_0_292 boundary_0 (select (m_origin formal_0_292) 9) (select (m_origin formal_0_292) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_294 () FormalMachine (FormalWriteFromOrigin formal_0_293 16 9))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_294)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_294) (select (m_origin formal_0_294) 32) (select (m_origin formal_0_294) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_294) (select (m_origin formal_0_294) 32) (select (m_origin formal_0_294) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_295 () FormalMachine (FormalCallback formal_0_294 boundary_0 (select (m_origin formal_0_294) 32) (select (m_origin formal_0_294) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_296 () FormalMachine (FormalWriteFromOrigin formal_0_295 17 32))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_297 () FormalMachine (FormalWriteFromOrigin formal_0_296 24 17))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_297)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_297) (select (m_origin formal_0_297) 44) (select (m_origin formal_0_297) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_297) (select (m_origin formal_0_297) 44) (select (m_origin formal_0_297) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_298 () FormalMachine (FormalCallback formal_0_297 boundary_0 (select (m_origin formal_0_297) 44) (select (m_origin formal_0_297) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_299 () FormalMachine (FormalWriteFromOrigin formal_0_298 17 44))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_299)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_299) (select (m_origin formal_0_299) 35) (select (m_origin formal_0_299) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_299) (select (m_origin formal_0_299) 35) (select (m_origin formal_0_299) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_300 () FormalMachine (FormalCallback formal_0_299 boundary_0 (select (m_origin formal_0_299) 35) (select (m_origin formal_0_299) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_301 () FormalMachine (FormalWriteFromOrigin formal_0_300 18 35))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_302 () FormalMachine (FormalWriteFromOrigin formal_0_301 26 6))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_302)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_302) (select (m_origin formal_0_302) 10) (select (m_origin formal_0_302) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_302) (select (m_origin formal_0_302) 10) (select (m_origin formal_0_302) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_303 () FormalMachine (FormalCallback formal_0_302 boundary_0 (select (m_origin formal_0_302) 10) (select (m_origin formal_0_302) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_304 () FormalMachine (FormalWriteFromOrigin formal_0_303 19 10))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_305 () FormalMachine (FormalWriteFromOrigin formal_0_304 27 5))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_305)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_305) (select (m_origin formal_0_305) 11) (select (m_origin formal_0_305) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_305) (select (m_origin formal_0_305) 11) (select (m_origin formal_0_305) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_306 () FormalMachine (FormalCallback formal_0_305 boundary_0 (select (m_origin formal_0_305) 11) (select (m_origin formal_0_305) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_307 () FormalMachine (FormalWriteFromOrigin formal_0_306 20 11))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_308 () FormalMachine (FormalWriteFromOrigin formal_0_307 28 26))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_308)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_308) (select (m_origin formal_0_308) 38) (select (m_origin formal_0_308) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_308) (select (m_origin formal_0_308) 38) (select (m_origin formal_0_308) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_309 () FormalMachine (FormalCallback formal_0_308 boundary_0 (select (m_origin formal_0_308) 38) (select (m_origin formal_0_308) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_310 () FormalMachine (FormalWriteFromOrigin formal_0_309 21 38))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_311 () FormalMachine (FormalWriteFromOrigin formal_0_310 29 27))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_311)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_311) (select (m_origin formal_0_311) 39) (select (m_origin formal_0_311) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_311) (select (m_origin formal_0_311) 39) (select (m_origin formal_0_311) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_312 () FormalMachine (FormalCallback formal_0_311 boundary_0 (select (m_origin formal_0_311) 39) (select (m_origin formal_0_311) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_313 () FormalMachine (FormalWriteFromOrigin formal_0_312 22 39))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_314 () FormalMachine (FormalWriteFromOrigin formal_0_313 30 1))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_314)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_314) (select (m_origin formal_0_314) 41) (select (m_origin formal_0_314) 33)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_314) (select (m_origin formal_0_314) 41) (select (m_origin formal_0_314) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_315 () FormalMachine (FormalCallback formal_0_314 boundary_0 (select (m_origin formal_0_314) 41) (select (m_origin formal_0_314) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_316 () FormalMachine (FormalWriteFromOrigin formal_0_315 23 41))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_317 () FormalMachine (FormalWriteFromOrigin formal_0_316 31 29))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_317)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_317) (select (m_origin formal_0_317) 42) (select (m_origin formal_0_317) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_317) (select (m_origin formal_0_317) 42) (select (m_origin formal_0_317) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_318 () FormalMachine (FormalCallback formal_0_317 boundary_0 (select (m_origin formal_0_317) 42) (select (m_origin formal_0_317) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_319 () FormalMachine (FormalWriteFromOrigin formal_0_318 24 42))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_320 () FormalMachine (FormalWriteFromOrigin formal_0_319 32 17))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:compare
(assert (not (m_panicked formal_0_320)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_320) (select (m_origin formal_0_320) 43) (select (m_origin formal_0_320) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_320) (select (m_origin formal_0_320) 43) (select (m_origin formal_0_320) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:compare
(define-fun formal_0_321 () FormalMachine (FormalCallback formal_0_320 boundary_0 (select (m_origin formal_0_320) 43) (select (m_origin formal_0_320) 33)))
; source write kind=partition-cycle phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_322 () FormalMachine (FormalWriteFromOrigin formal_0_321 24 43))
; source callback case=fallback-small-sort-and-recursion phase=partition-lomuto-cyclic:cleanup-compare
(assert (not (m_panicked formal_0_322)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 4) (select (m_origin formal_0_322) 33)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_322) (select (m_origin formal_0_322) 4) (select (m_origin formal_0_322) 33)) false))
; source callback transition phase=partition-lomuto-cyclic:cleanup-compare
(define-fun formal_0_323 () FormalMachine (FormalCallback formal_0_322 boundary_0 (select (m_origin formal_0_322) 4) (select (m_origin formal_0_322) 33)))
; source write kind=partition-cycle-cleanup phase=partition-lomuto-branchless-cyclic
(define-fun formal_0_324 () FormalMachine (FormalWriteFromOrigin formal_0_323 24 4))
; source swap phase=partition:pivot-to-middle
(define-fun formal_0_325 () FormalMachine (FormalSwap formal_0_324 12 23))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:1]:initial-compare
(assert (not (m_panicked formal_0_325)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_325) (select (m_origin formal_0_325) 18) (select (m_origin formal_0_325) 41)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_325) (select (m_origin formal_0_325) 18) (select (m_origin formal_0_325) 41)) false))
; source callback transition phase=insert-tail[12:23:1]:initial-compare
(define-fun formal_0_326 () FormalMachine (FormalCallback formal_0_325 boundary_0 (select (m_origin formal_0_325) 18) (select (m_origin formal_0_325) 41)))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:2]:initial-compare
(assert (not (m_panicked formal_0_326)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_326) (select (m_origin formal_0_326) 19) (select (m_origin formal_0_326) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_326) (select (m_origin formal_0_326) 19) (select (m_origin formal_0_326) 18)) false))
; source callback transition phase=insert-tail[12:23:2]:initial-compare
(define-fun formal_0_327 () FormalMachine (FormalCallback formal_0_326 boundary_0 (select (m_origin formal_0_326) 19) (select (m_origin formal_0_326) 18)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:2]
(define-fun formal_0_328 () FormalMachine (FormalWriteFromOrigin formal_0_327 14 18))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:2]:sift-compare
(assert (not (m_panicked formal_0_328)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_328) (select (m_origin formal_0_328) 19) (select (m_origin formal_0_328) 41)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_328) (select (m_origin formal_0_328) 19) (select (m_origin formal_0_328) 41)) false))
; source callback transition phase=insert-tail[12:23:2]:sift-compare
(define-fun formal_0_329 () FormalMachine (FormalCallback formal_0_328 boundary_0 (select (m_origin formal_0_328) 19) (select (m_origin formal_0_328) 41)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:2]
(define-fun formal_0_330 () FormalMachine (FormalWriteFromOrigin formal_0_329 13 41))
; source write kind=copy-on-drop-restore phase=insert-tail[12:23:2]
(define-fun formal_0_331 () FormalMachine (FormalWriteFromOrigin formal_0_330 12 19))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:3]:initial-compare
(assert (not (m_panicked formal_0_331)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_331) (select (m_origin formal_0_331) 25) (select (m_origin formal_0_331) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_331) (select (m_origin formal_0_331) 25) (select (m_origin formal_0_331) 18)) false))
; source callback transition phase=insert-tail[12:23:3]:initial-compare
(define-fun formal_0_332 () FormalMachine (FormalCallback formal_0_331 boundary_0 (select (m_origin formal_0_331) 25) (select (m_origin formal_0_331) 18)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:3]
(define-fun formal_0_333 () FormalMachine (FormalWriteFromOrigin formal_0_332 15 18))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:3]:sift-compare
(assert (not (m_panicked formal_0_333)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_333) (select (m_origin formal_0_333) 25) (select (m_origin formal_0_333) 41)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_333) (select (m_origin formal_0_333) 25) (select (m_origin formal_0_333) 41)) false))
; source callback transition phase=insert-tail[12:23:3]:sift-compare
(define-fun formal_0_334 () FormalMachine (FormalCallback formal_0_333 boundary_0 (select (m_origin formal_0_333) 25) (select (m_origin formal_0_333) 41)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:3]
(define-fun formal_0_335 () FormalMachine (FormalWriteFromOrigin formal_0_334 14 41))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:3]:sift-compare
(assert (not (m_panicked formal_0_335)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_335) (select (m_origin formal_0_335) 25) (select (m_origin formal_0_335) 19)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_335) (select (m_origin formal_0_335) 25) (select (m_origin formal_0_335) 19)) false))
; source callback transition phase=insert-tail[12:23:3]:sift-compare
(define-fun formal_0_336 () FormalMachine (FormalCallback formal_0_335 boundary_0 (select (m_origin formal_0_335) 25) (select (m_origin formal_0_335) 19)))
; source write kind=copy-on-drop-restore phase=insert-tail[12:23:3]
(define-fun formal_0_337 () FormalMachine (FormalWriteFromOrigin formal_0_336 13 25))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:4]:initial-compare
(assert (not (m_panicked formal_0_337)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_337) (select (m_origin formal_0_337) 9) (select (m_origin formal_0_337) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_337) (select (m_origin formal_0_337) 9) (select (m_origin formal_0_337) 18)) false))
; source callback transition phase=insert-tail[12:23:4]:initial-compare
(define-fun formal_0_338 () FormalMachine (FormalCallback formal_0_337 boundary_0 (select (m_origin formal_0_337) 9) (select (m_origin formal_0_337) 18)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:4]
(define-fun formal_0_339 () FormalMachine (FormalWriteFromOrigin formal_0_338 16 18))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:4]:sift-compare
(assert (not (m_panicked formal_0_339)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_339) (select (m_origin formal_0_339) 9) (select (m_origin formal_0_339) 41)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_339) (select (m_origin formal_0_339) 9) (select (m_origin formal_0_339) 41)) false))
; source callback transition phase=insert-tail[12:23:4]:sift-compare
(define-fun formal_0_340 () FormalMachine (FormalCallback formal_0_339 boundary_0 (select (m_origin formal_0_339) 9) (select (m_origin formal_0_339) 41)))
; source write kind=copy-on-drop-restore phase=insert-tail[12:23:4]
(define-fun formal_0_341 () FormalMachine (FormalWriteFromOrigin formal_0_340 15 9))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:5]:initial-compare
(assert (not (m_panicked formal_0_341)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_341) (select (m_origin formal_0_341) 44) (select (m_origin formal_0_341) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_341) (select (m_origin formal_0_341) 44) (select (m_origin formal_0_341) 18)) false))
; source callback transition phase=insert-tail[12:23:5]:initial-compare
(define-fun formal_0_342 () FormalMachine (FormalCallback formal_0_341 boundary_0 (select (m_origin formal_0_341) 44) (select (m_origin formal_0_341) 18)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:5]
(define-fun formal_0_343 () FormalMachine (FormalWriteFromOrigin formal_0_342 17 18))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:5]:sift-compare
(assert (not (m_panicked formal_0_343)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_343) (select (m_origin formal_0_343) 44) (select (m_origin formal_0_343) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_343) (select (m_origin formal_0_343) 44) (select (m_origin formal_0_343) 9)) false))
; source callback transition phase=insert-tail[12:23:5]:sift-compare
(define-fun formal_0_344 () FormalMachine (FormalCallback formal_0_343 boundary_0 (select (m_origin formal_0_343) 44) (select (m_origin formal_0_343) 9)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:5]
(define-fun formal_0_345 () FormalMachine (FormalWriteFromOrigin formal_0_344 16 9))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:5]:sift-compare
(assert (not (m_panicked formal_0_345)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_345) (select (m_origin formal_0_345) 44) (select (m_origin formal_0_345) 41)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_345) (select (m_origin formal_0_345) 44) (select (m_origin formal_0_345) 41)) false))
; source callback transition phase=insert-tail[12:23:5]:sift-compare
(define-fun formal_0_346 () FormalMachine (FormalCallback formal_0_345 boundary_0 (select (m_origin formal_0_345) 44) (select (m_origin formal_0_345) 41)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:5]
(define-fun formal_0_347 () FormalMachine (FormalWriteFromOrigin formal_0_346 15 41))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:5]:sift-compare
(assert (not (m_panicked formal_0_347)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_347) (select (m_origin formal_0_347) 44) (select (m_origin formal_0_347) 25)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_347) (select (m_origin formal_0_347) 44) (select (m_origin formal_0_347) 25)) false))
; source callback transition phase=insert-tail[12:23:5]:sift-compare
(define-fun formal_0_348 () FormalMachine (FormalCallback formal_0_347 boundary_0 (select (m_origin formal_0_347) 44) (select (m_origin formal_0_347) 25)))
; source write kind=copy-on-drop-restore phase=insert-tail[12:23:5]
(define-fun formal_0_349 () FormalMachine (FormalWriteFromOrigin formal_0_348 14 44))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:6]:initial-compare
(assert (not (m_panicked formal_0_349)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_349) (select (m_origin formal_0_349) 35) (select (m_origin formal_0_349) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_349) (select (m_origin formal_0_349) 35) (select (m_origin formal_0_349) 18)) false))
; source callback transition phase=insert-tail[12:23:6]:initial-compare
(define-fun formal_0_350 () FormalMachine (FormalCallback formal_0_349 boundary_0 (select (m_origin formal_0_349) 35) (select (m_origin formal_0_349) 18)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:6]
(define-fun formal_0_351 () FormalMachine (FormalWriteFromOrigin formal_0_350 18 18))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:6]:sift-compare
(assert (not (m_panicked formal_0_351)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_351) (select (m_origin formal_0_351) 35) (select (m_origin formal_0_351) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_351) (select (m_origin formal_0_351) 35) (select (m_origin formal_0_351) 9)) false))
; source callback transition phase=insert-tail[12:23:6]:sift-compare
(define-fun formal_0_352 () FormalMachine (FormalCallback formal_0_351 boundary_0 (select (m_origin formal_0_351) 35) (select (m_origin formal_0_351) 9)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:6]
(define-fun formal_0_353 () FormalMachine (FormalWriteFromOrigin formal_0_352 17 9))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:6]:sift-compare
(assert (not (m_panicked formal_0_353)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_353) (select (m_origin formal_0_353) 35) (select (m_origin formal_0_353) 41)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_353) (select (m_origin formal_0_353) 35) (select (m_origin formal_0_353) 41)) false))
; source callback transition phase=insert-tail[12:23:6]:sift-compare
(define-fun formal_0_354 () FormalMachine (FormalCallback formal_0_353 boundary_0 (select (m_origin formal_0_353) 35) (select (m_origin formal_0_353) 41)))
; source write kind=copy-on-drop-restore phase=insert-tail[12:23:6]
(define-fun formal_0_355 () FormalMachine (FormalWriteFromOrigin formal_0_354 16 35))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:7]:initial-compare
(assert (not (m_panicked formal_0_355)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_355) (select (m_origin formal_0_355) 10) (select (m_origin formal_0_355) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_355) (select (m_origin formal_0_355) 10) (select (m_origin formal_0_355) 18)) false))
; source callback transition phase=insert-tail[12:23:7]:initial-compare
(define-fun formal_0_356 () FormalMachine (FormalCallback formal_0_355 boundary_0 (select (m_origin formal_0_355) 10) (select (m_origin formal_0_355) 18)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:7]
(define-fun formal_0_357 () FormalMachine (FormalWriteFromOrigin formal_0_356 19 18))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:7]:sift-compare
(assert (not (m_panicked formal_0_357)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 10) (select (m_origin formal_0_357) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_357) (select (m_origin formal_0_357) 10) (select (m_origin formal_0_357) 9)) false))
; source callback transition phase=insert-tail[12:23:7]:sift-compare
(define-fun formal_0_358 () FormalMachine (FormalCallback formal_0_357 boundary_0 (select (m_origin formal_0_357) 10) (select (m_origin formal_0_357) 9)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:7]
(define-fun formal_0_359 () FormalMachine (FormalWriteFromOrigin formal_0_358 18 9))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:7]:sift-compare
(assert (not (m_panicked formal_0_359)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_359) (select (m_origin formal_0_359) 10) (select (m_origin formal_0_359) 35)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_359) (select (m_origin formal_0_359) 10) (select (m_origin formal_0_359) 35)) false))
; source callback transition phase=insert-tail[12:23:7]:sift-compare
(define-fun formal_0_360 () FormalMachine (FormalCallback formal_0_359 boundary_0 (select (m_origin formal_0_359) 10) (select (m_origin formal_0_359) 35)))
; source write kind=copy-on-drop-restore phase=insert-tail[12:23:7]
(define-fun formal_0_361 () FormalMachine (FormalWriteFromOrigin formal_0_360 17 10))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:8]:initial-compare
(assert (not (m_panicked formal_0_361)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_361) (select (m_origin formal_0_361) 11) (select (m_origin formal_0_361) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_361) (select (m_origin formal_0_361) 11) (select (m_origin formal_0_361) 18)) false))
; source callback transition phase=insert-tail[12:23:8]:initial-compare
(define-fun formal_0_362 () FormalMachine (FormalCallback formal_0_361 boundary_0 (select (m_origin formal_0_361) 11) (select (m_origin formal_0_361) 18)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:8]
(define-fun formal_0_363 () FormalMachine (FormalWriteFromOrigin formal_0_362 20 18))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:8]:sift-compare
(assert (not (m_panicked formal_0_363)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_363) (select (m_origin formal_0_363) 11) (select (m_origin formal_0_363) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_363) (select (m_origin formal_0_363) 11) (select (m_origin formal_0_363) 9)) false))
; source callback transition phase=insert-tail[12:23:8]:sift-compare
(define-fun formal_0_364 () FormalMachine (FormalCallback formal_0_363 boundary_0 (select (m_origin formal_0_363) 11) (select (m_origin formal_0_363) 9)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:8]
(define-fun formal_0_365 () FormalMachine (FormalWriteFromOrigin formal_0_364 19 9))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:8]:sift-compare
(assert (not (m_panicked formal_0_365)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_365) (select (m_origin formal_0_365) 11) (select (m_origin formal_0_365) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_365) (select (m_origin formal_0_365) 11) (select (m_origin formal_0_365) 10)) false))
; source callback transition phase=insert-tail[12:23:8]:sift-compare
(define-fun formal_0_366 () FormalMachine (FormalCallback formal_0_365 boundary_0 (select (m_origin formal_0_365) 11) (select (m_origin formal_0_365) 10)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:8]
(define-fun formal_0_367 () FormalMachine (FormalWriteFromOrigin formal_0_366 18 10))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:8]:sift-compare
(assert (not (m_panicked formal_0_367)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_367) (select (m_origin formal_0_367) 11) (select (m_origin formal_0_367) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_367) (select (m_origin formal_0_367) 11) (select (m_origin formal_0_367) 35)) false))
; source callback transition phase=insert-tail[12:23:8]:sift-compare
(define-fun formal_0_368 () FormalMachine (FormalCallback formal_0_367 boundary_0 (select (m_origin formal_0_367) 11) (select (m_origin formal_0_367) 35)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:8]
(define-fun formal_0_369 () FormalMachine (FormalWriteFromOrigin formal_0_368 17 35))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:8]:sift-compare
(assert (not (m_panicked formal_0_369)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_369) (select (m_origin formal_0_369) 11) (select (m_origin formal_0_369) 41)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_369) (select (m_origin formal_0_369) 11) (select (m_origin formal_0_369) 41)) false))
; source callback transition phase=insert-tail[12:23:8]:sift-compare
(define-fun formal_0_370 () FormalMachine (FormalCallback formal_0_369 boundary_0 (select (m_origin formal_0_369) 11) (select (m_origin formal_0_369) 41)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:8]
(define-fun formal_0_371 () FormalMachine (FormalWriteFromOrigin formal_0_370 16 41))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:8]:sift-compare
(assert (not (m_panicked formal_0_371)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_371) (select (m_origin formal_0_371) 11) (select (m_origin formal_0_371) 44)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_371) (select (m_origin formal_0_371) 11) (select (m_origin formal_0_371) 44)) false))
; source callback transition phase=insert-tail[12:23:8]:sift-compare
(define-fun formal_0_372 () FormalMachine (FormalCallback formal_0_371 boundary_0 (select (m_origin formal_0_371) 11) (select (m_origin formal_0_371) 44)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:8]
(define-fun formal_0_373 () FormalMachine (FormalWriteFromOrigin formal_0_372 15 44))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:8]:sift-compare
(assert (not (m_panicked formal_0_373)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_373) (select (m_origin formal_0_373) 11) (select (m_origin formal_0_373) 25)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_373) (select (m_origin formal_0_373) 11) (select (m_origin formal_0_373) 25)) false))
; source callback transition phase=insert-tail[12:23:8]:sift-compare
(define-fun formal_0_374 () FormalMachine (FormalCallback formal_0_373 boundary_0 (select (m_origin formal_0_373) 11) (select (m_origin formal_0_373) 25)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:8]
(define-fun formal_0_375 () FormalMachine (FormalWriteFromOrigin formal_0_374 14 25))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:8]:sift-compare
(assert (not (m_panicked formal_0_375)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_375) (select (m_origin formal_0_375) 11) (select (m_origin formal_0_375) 19)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_375) (select (m_origin formal_0_375) 11) (select (m_origin formal_0_375) 19)) false))
; source callback transition phase=insert-tail[12:23:8]:sift-compare
(define-fun formal_0_376 () FormalMachine (FormalCallback formal_0_375 boundary_0 (select (m_origin formal_0_375) 11) (select (m_origin formal_0_375) 19)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:8]
(define-fun formal_0_377 () FormalMachine (FormalWriteFromOrigin formal_0_376 13 19))
; source write kind=copy-on-drop-restore phase=insert-tail[12:23:8]
(define-fun formal_0_378 () FormalMachine (FormalWriteFromOrigin formal_0_377 12 11))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:9]:initial-compare
(assert (not (m_panicked formal_0_378)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_378) (select (m_origin formal_0_378) 38) (select (m_origin formal_0_378) 18)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_378) (select (m_origin formal_0_378) 38) (select (m_origin formal_0_378) 18)) false))
; source callback transition phase=insert-tail[12:23:9]:initial-compare
(define-fun formal_0_379 () FormalMachine (FormalCallback formal_0_378 boundary_0 (select (m_origin formal_0_378) 38) (select (m_origin formal_0_378) 18)))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:10]:initial-compare
(assert (not (m_panicked formal_0_379)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_379) (select (m_origin formal_0_379) 39) (select (m_origin formal_0_379) 38)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_379) (select (m_origin formal_0_379) 39) (select (m_origin formal_0_379) 38)) false))
; source callback transition phase=insert-tail[12:23:10]:initial-compare
(define-fun formal_0_380 () FormalMachine (FormalCallback formal_0_379 boundary_0 (select (m_origin formal_0_379) 39) (select (m_origin formal_0_379) 38)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:10]
(define-fun formal_0_381 () FormalMachine (FormalWriteFromOrigin formal_0_380 22 38))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:10]:sift-compare
(assert (not (m_panicked formal_0_381)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_381) (select (m_origin formal_0_381) 39) (select (m_origin formal_0_381) 18)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_381) (select (m_origin formal_0_381) 39) (select (m_origin formal_0_381) 18)) false))
; source callback transition phase=insert-tail[12:23:10]:sift-compare
(define-fun formal_0_382 () FormalMachine (FormalCallback formal_0_381 boundary_0 (select (m_origin formal_0_381) 39) (select (m_origin formal_0_381) 18)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:10]
(define-fun formal_0_383 () FormalMachine (FormalWriteFromOrigin formal_0_382 21 18))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:10]:sift-compare
(assert (not (m_panicked formal_0_383)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_383) (select (m_origin formal_0_383) 39) (select (m_origin formal_0_383) 9)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_383) (select (m_origin formal_0_383) 39) (select (m_origin formal_0_383) 9)) false))
; source callback transition phase=insert-tail[12:23:10]:sift-compare
(define-fun formal_0_384 () FormalMachine (FormalCallback formal_0_383 boundary_0 (select (m_origin formal_0_383) 39) (select (m_origin formal_0_383) 9)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:10]
(define-fun formal_0_385 () FormalMachine (FormalWriteFromOrigin formal_0_384 20 9))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:10]:sift-compare
(assert (not (m_panicked formal_0_385)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_385) (select (m_origin formal_0_385) 39) (select (m_origin formal_0_385) 10)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_385) (select (m_origin formal_0_385) 39) (select (m_origin formal_0_385) 10)) false))
; source callback transition phase=insert-tail[12:23:10]:sift-compare
(define-fun formal_0_386 () FormalMachine (FormalCallback formal_0_385 boundary_0 (select (m_origin formal_0_385) 39) (select (m_origin formal_0_385) 10)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:10]
(define-fun formal_0_387 () FormalMachine (FormalWriteFromOrigin formal_0_386 19 10))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:10]:sift-compare
(assert (not (m_panicked formal_0_387)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_387) (select (m_origin formal_0_387) 39) (select (m_origin formal_0_387) 35)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_387) (select (m_origin formal_0_387) 39) (select (m_origin formal_0_387) 35)) false))
; source callback transition phase=insert-tail[12:23:10]:sift-compare
(define-fun formal_0_388 () FormalMachine (FormalCallback formal_0_387 boundary_0 (select (m_origin formal_0_387) 39) (select (m_origin formal_0_387) 35)))
; source write kind=insert-tail-shift phase=insert-tail[12:23:10]
(define-fun formal_0_389 () FormalMachine (FormalWriteFromOrigin formal_0_388 18 35))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[12:23:10]:sift-compare
(assert (not (m_panicked formal_0_389)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_389) (select (m_origin formal_0_389) 39) (select (m_origin formal_0_389) 41)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_389) (select (m_origin formal_0_389) 39) (select (m_origin formal_0_389) 41)) false))
; source callback transition phase=insert-tail[12:23:10]:sift-compare
(define-fun formal_0_390 () FormalMachine (FormalCallback formal_0_389 boundary_0 (select (m_origin formal_0_389) 39) (select (m_origin formal_0_389) 41)))
; source write kind=copy-on-drop-restore phase=insert-tail[12:23:10]
(define-fun formal_0_391 () FormalMachine (FormalWriteFromOrigin formal_0_390 17 39))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:1]:initial-compare
(assert (not (m_panicked formal_0_391)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_391) (select (m_origin formal_0_391) 32) (select (m_origin formal_0_391) 4)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_391) (select (m_origin formal_0_391) 32) (select (m_origin formal_0_391) 4)) false))
; source callback transition phase=insert-tail[24:35:1]:initial-compare
(define-fun formal_0_392 () FormalMachine (FormalCallback formal_0_391 boundary_0 (select (m_origin formal_0_391) 32) (select (m_origin formal_0_391) 4)))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:2]:initial-compare
(assert (not (m_panicked formal_0_392)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_392) (select (m_origin formal_0_392) 6) (select (m_origin formal_0_392) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_392) (select (m_origin formal_0_392) 6) (select (m_origin formal_0_392) 32)) false))
; source callback transition phase=insert-tail[24:35:2]:initial-compare
(define-fun formal_0_393 () FormalMachine (FormalCallback formal_0_392 boundary_0 (select (m_origin formal_0_392) 6) (select (m_origin formal_0_392) 32)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:2]
(define-fun formal_0_394 () FormalMachine (FormalWriteFromOrigin formal_0_393 26 32))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:2]:sift-compare
(assert (not (m_panicked formal_0_394)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_394) (select (m_origin formal_0_394) 6) (select (m_origin formal_0_394) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_394) (select (m_origin formal_0_394) 6) (select (m_origin formal_0_394) 4)) false))
; source callback transition phase=insert-tail[24:35:2]:sift-compare
(define-fun formal_0_395 () FormalMachine (FormalCallback formal_0_394 boundary_0 (select (m_origin formal_0_394) 6) (select (m_origin formal_0_394) 4)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:2]
(define-fun formal_0_396 () FormalMachine (FormalWriteFromOrigin formal_0_395 25 4))
; source write kind=copy-on-drop-restore phase=insert-tail[24:35:2]
(define-fun formal_0_397 () FormalMachine (FormalWriteFromOrigin formal_0_396 24 6))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:3]:initial-compare
(assert (not (m_panicked formal_0_397)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_397) (select (m_origin formal_0_397) 5) (select (m_origin formal_0_397) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_397) (select (m_origin formal_0_397) 5) (select (m_origin formal_0_397) 32)) false))
; source callback transition phase=insert-tail[24:35:3]:initial-compare
(define-fun formal_0_398 () FormalMachine (FormalCallback formal_0_397 boundary_0 (select (m_origin formal_0_397) 5) (select (m_origin formal_0_397) 32)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:3]
(define-fun formal_0_399 () FormalMachine (FormalWriteFromOrigin formal_0_398 27 32))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:3]:sift-compare
(assert (not (m_panicked formal_0_399)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_399) (select (m_origin formal_0_399) 5) (select (m_origin formal_0_399) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_399) (select (m_origin formal_0_399) 5) (select (m_origin formal_0_399) 4)) false))
; source callback transition phase=insert-tail[24:35:3]:sift-compare
(define-fun formal_0_400 () FormalMachine (FormalCallback formal_0_399 boundary_0 (select (m_origin formal_0_399) 5) (select (m_origin formal_0_399) 4)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:3]
(define-fun formal_0_401 () FormalMachine (FormalWriteFromOrigin formal_0_400 26 4))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:3]:sift-compare
(assert (not (m_panicked formal_0_401)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_401) (select (m_origin formal_0_401) 5) (select (m_origin formal_0_401) 6)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_401) (select (m_origin formal_0_401) 5) (select (m_origin formal_0_401) 6)) false))
; source callback transition phase=insert-tail[24:35:3]:sift-compare
(define-fun formal_0_402 () FormalMachine (FormalCallback formal_0_401 boundary_0 (select (m_origin formal_0_401) 5) (select (m_origin formal_0_401) 6)))
; source write kind=copy-on-drop-restore phase=insert-tail[24:35:3]
(define-fun formal_0_403 () FormalMachine (FormalWriteFromOrigin formal_0_402 25 5))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:4]:initial-compare
(assert (not (m_panicked formal_0_403)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_403) (select (m_origin formal_0_403) 26) (select (m_origin formal_0_403) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_403) (select (m_origin formal_0_403) 26) (select (m_origin formal_0_403) 32)) false))
; source callback transition phase=insert-tail[24:35:4]:initial-compare
(define-fun formal_0_404 () FormalMachine (FormalCallback formal_0_403 boundary_0 (select (m_origin formal_0_403) 26) (select (m_origin formal_0_403) 32)))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:5]:initial-compare
(assert (not (m_panicked formal_0_404)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_404) (select (m_origin formal_0_404) 27) (select (m_origin formal_0_404) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_404) (select (m_origin formal_0_404) 27) (select (m_origin formal_0_404) 26)) false))
; source callback transition phase=insert-tail[24:35:5]:initial-compare
(define-fun formal_0_405 () FormalMachine (FormalCallback formal_0_404 boundary_0 (select (m_origin formal_0_404) 27) (select (m_origin formal_0_404) 26)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:5]
(define-fun formal_0_406 () FormalMachine (FormalWriteFromOrigin formal_0_405 29 26))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:5]:sift-compare
(assert (not (m_panicked formal_0_406)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_406) (select (m_origin formal_0_406) 27) (select (m_origin formal_0_406) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_406) (select (m_origin formal_0_406) 27) (select (m_origin formal_0_406) 32)) false))
; source callback transition phase=insert-tail[24:35:5]:sift-compare
(define-fun formal_0_407 () FormalMachine (FormalCallback formal_0_406 boundary_0 (select (m_origin formal_0_406) 27) (select (m_origin formal_0_406) 32)))
; source write kind=copy-on-drop-restore phase=insert-tail[24:35:5]
(define-fun formal_0_408 () FormalMachine (FormalWriteFromOrigin formal_0_407 28 27))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:6]:initial-compare
(assert (not (m_panicked formal_0_408)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_408) (select (m_origin formal_0_408) 1) (select (m_origin formal_0_408) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_408) (select (m_origin formal_0_408) 1) (select (m_origin formal_0_408) 26)) false))
; source callback transition phase=insert-tail[24:35:6]:initial-compare
(define-fun formal_0_409 () FormalMachine (FormalCallback formal_0_408 boundary_0 (select (m_origin formal_0_408) 1) (select (m_origin formal_0_408) 26)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:6]
(define-fun formal_0_410 () FormalMachine (FormalWriteFromOrigin formal_0_409 30 26))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:6]:sift-compare
(assert (not (m_panicked formal_0_410)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_410) (select (m_origin formal_0_410) 1) (select (m_origin formal_0_410) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_410) (select (m_origin formal_0_410) 1) (select (m_origin formal_0_410) 27)) false))
; source callback transition phase=insert-tail[24:35:6]:sift-compare
(define-fun formal_0_411 () FormalMachine (FormalCallback formal_0_410 boundary_0 (select (m_origin formal_0_410) 1) (select (m_origin formal_0_410) 27)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:6]
(define-fun formal_0_412 () FormalMachine (FormalWriteFromOrigin formal_0_411 29 27))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:6]:sift-compare
(assert (not (m_panicked formal_0_412)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_412) (select (m_origin formal_0_412) 1) (select (m_origin formal_0_412) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_412) (select (m_origin formal_0_412) 1) (select (m_origin formal_0_412) 32)) false))
; source callback transition phase=insert-tail[24:35:6]:sift-compare
(define-fun formal_0_413 () FormalMachine (FormalCallback formal_0_412 boundary_0 (select (m_origin formal_0_412) 1) (select (m_origin formal_0_412) 32)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:6]
(define-fun formal_0_414 () FormalMachine (FormalWriteFromOrigin formal_0_413 28 32))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:6]:sift-compare
(assert (not (m_panicked formal_0_414)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_414) (select (m_origin formal_0_414) 1) (select (m_origin formal_0_414) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_414) (select (m_origin formal_0_414) 1) (select (m_origin formal_0_414) 4)) false))
; source callback transition phase=insert-tail[24:35:6]:sift-compare
(define-fun formal_0_415 () FormalMachine (FormalCallback formal_0_414 boundary_0 (select (m_origin formal_0_414) 1) (select (m_origin formal_0_414) 4)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:6]
(define-fun formal_0_416 () FormalMachine (FormalWriteFromOrigin formal_0_415 27 4))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:6]:sift-compare
(assert (not (m_panicked formal_0_416)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_416) (select (m_origin formal_0_416) 1) (select (m_origin formal_0_416) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_416) (select (m_origin formal_0_416) 1) (select (m_origin formal_0_416) 5)) false))
; source callback transition phase=insert-tail[24:35:6]:sift-compare
(define-fun formal_0_417 () FormalMachine (FormalCallback formal_0_416 boundary_0 (select (m_origin formal_0_416) 1) (select (m_origin formal_0_416) 5)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:6]
(define-fun formal_0_418 () FormalMachine (FormalWriteFromOrigin formal_0_417 26 5))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:6]:sift-compare
(assert (not (m_panicked formal_0_418)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_418) (select (m_origin formal_0_418) 1) (select (m_origin formal_0_418) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_418) (select (m_origin formal_0_418) 1) (select (m_origin formal_0_418) 6)) false))
; source callback transition phase=insert-tail[24:35:6]:sift-compare
(define-fun formal_0_419 () FormalMachine (FormalCallback formal_0_418 boundary_0 (select (m_origin formal_0_418) 1) (select (m_origin formal_0_418) 6)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:6]
(define-fun formal_0_420 () FormalMachine (FormalWriteFromOrigin formal_0_419 25 6))
; source write kind=copy-on-drop-restore phase=insert-tail[24:35:6]
(define-fun formal_0_421 () FormalMachine (FormalWriteFromOrigin formal_0_420 24 1))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:7]:initial-compare
(assert (not (m_panicked formal_0_421)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_421) (select (m_origin formal_0_421) 29) (select (m_origin formal_0_421) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_421) (select (m_origin formal_0_421) 29) (select (m_origin formal_0_421) 26)) false))
; source callback transition phase=insert-tail[24:35:7]:initial-compare
(define-fun formal_0_422 () FormalMachine (FormalCallback formal_0_421 boundary_0 (select (m_origin formal_0_421) 29) (select (m_origin formal_0_421) 26)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:7]
(define-fun formal_0_423 () FormalMachine (FormalWriteFromOrigin formal_0_422 31 26))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:7]:sift-compare
(assert (not (m_panicked formal_0_423)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_423) (select (m_origin formal_0_423) 29) (select (m_origin formal_0_423) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_423) (select (m_origin formal_0_423) 29) (select (m_origin formal_0_423) 27)) false))
; source callback transition phase=insert-tail[24:35:7]:sift-compare
(define-fun formal_0_424 () FormalMachine (FormalCallback formal_0_423 boundary_0 (select (m_origin formal_0_423) 29) (select (m_origin formal_0_423) 27)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:7]
(define-fun formal_0_425 () FormalMachine (FormalWriteFromOrigin formal_0_424 30 27))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:7]:sift-compare
(assert (not (m_panicked formal_0_425)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_425) (select (m_origin formal_0_425) 29) (select (m_origin formal_0_425) 32)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_425) (select (m_origin formal_0_425) 29) (select (m_origin formal_0_425) 32)) false))
; source callback transition phase=insert-tail[24:35:7]:sift-compare
(define-fun formal_0_426 () FormalMachine (FormalCallback formal_0_425 boundary_0 (select (m_origin formal_0_425) 29) (select (m_origin formal_0_425) 32)))
; source write kind=copy-on-drop-restore phase=insert-tail[24:35:7]
(define-fun formal_0_427 () FormalMachine (FormalWriteFromOrigin formal_0_426 29 29))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:8]:initial-compare
(assert (not (m_panicked formal_0_427)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_427) (select (m_origin formal_0_427) 17) (select (m_origin formal_0_427) 26)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_427) (select (m_origin formal_0_427) 17) (select (m_origin formal_0_427) 26)) false))
; source callback transition phase=insert-tail[24:35:8]:initial-compare
(define-fun formal_0_428 () FormalMachine (FormalCallback formal_0_427 boundary_0 (select (m_origin formal_0_427) 17) (select (m_origin formal_0_427) 26)))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:9]:initial-compare
(assert (not (m_panicked formal_0_428)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_428) (select (m_origin formal_0_428) 42) (select (m_origin formal_0_428) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_428) (select (m_origin formal_0_428) 42) (select (m_origin formal_0_428) 17)) false))
; source callback transition phase=insert-tail[24:35:9]:initial-compare
(define-fun formal_0_429 () FormalMachine (FormalCallback formal_0_428 boundary_0 (select (m_origin formal_0_428) 42) (select (m_origin formal_0_428) 17)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:9]
(define-fun formal_0_430 () FormalMachine (FormalWriteFromOrigin formal_0_429 33 17))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:9]:sift-compare
(assert (not (m_panicked formal_0_430)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_430) (select (m_origin formal_0_430) 42) (select (m_origin formal_0_430) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_430) (select (m_origin formal_0_430) 42) (select (m_origin formal_0_430) 26)) false))
; source callback transition phase=insert-tail[24:35:9]:sift-compare
(define-fun formal_0_431 () FormalMachine (FormalCallback formal_0_430 boundary_0 (select (m_origin formal_0_430) 42) (select (m_origin formal_0_430) 26)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:9]
(define-fun formal_0_432 () FormalMachine (FormalWriteFromOrigin formal_0_431 32 26))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:9]:sift-compare
(assert (not (m_panicked formal_0_432)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_432) (select (m_origin formal_0_432) 42) (select (m_origin formal_0_432) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_432) (select (m_origin formal_0_432) 42) (select (m_origin formal_0_432) 27)) false))
; source callback transition phase=insert-tail[24:35:9]:sift-compare
(define-fun formal_0_433 () FormalMachine (FormalCallback formal_0_432 boundary_0 (select (m_origin formal_0_432) 42) (select (m_origin formal_0_432) 27)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:9]
(define-fun formal_0_434 () FormalMachine (FormalWriteFromOrigin formal_0_433 31 27))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:9]:sift-compare
(assert (not (m_panicked formal_0_434)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_434) (select (m_origin formal_0_434) 42) (select (m_origin formal_0_434) 29)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_434) (select (m_origin formal_0_434) 42) (select (m_origin formal_0_434) 29)) false))
; source callback transition phase=insert-tail[24:35:9]:sift-compare
(define-fun formal_0_435 () FormalMachine (FormalCallback formal_0_434 boundary_0 (select (m_origin formal_0_434) 42) (select (m_origin formal_0_434) 29)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:9]
(define-fun formal_0_436 () FormalMachine (FormalWriteFromOrigin formal_0_435 30 29))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:9]:sift-compare
(assert (not (m_panicked formal_0_436)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_436) (select (m_origin formal_0_436) 42) (select (m_origin formal_0_436) 32)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_436) (select (m_origin formal_0_436) 42) (select (m_origin formal_0_436) 32)) false))
; source callback transition phase=insert-tail[24:35:9]:sift-compare
(define-fun formal_0_437 () FormalMachine (FormalCallback formal_0_436 boundary_0 (select (m_origin formal_0_436) 42) (select (m_origin formal_0_436) 32)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:9]
(define-fun formal_0_438 () FormalMachine (FormalWriteFromOrigin formal_0_437 29 32))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:9]:sift-compare
(assert (not (m_panicked formal_0_438)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_438) (select (m_origin formal_0_438) 42) (select (m_origin formal_0_438) 4)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_438) (select (m_origin formal_0_438) 42) (select (m_origin formal_0_438) 4)) false))
; source callback transition phase=insert-tail[24:35:9]:sift-compare
(define-fun formal_0_439 () FormalMachine (FormalCallback formal_0_438 boundary_0 (select (m_origin formal_0_438) 42) (select (m_origin formal_0_438) 4)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:9]
(define-fun formal_0_440 () FormalMachine (FormalWriteFromOrigin formal_0_439 28 4))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:9]:sift-compare
(assert (not (m_panicked formal_0_440)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_440) (select (m_origin formal_0_440) 42) (select (m_origin formal_0_440) 5)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_440) (select (m_origin formal_0_440) 42) (select (m_origin formal_0_440) 5)) false))
; source callback transition phase=insert-tail[24:35:9]:sift-compare
(define-fun formal_0_441 () FormalMachine (FormalCallback formal_0_440 boundary_0 (select (m_origin formal_0_440) 42) (select (m_origin formal_0_440) 5)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:9]
(define-fun formal_0_442 () FormalMachine (FormalWriteFromOrigin formal_0_441 27 5))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:9]:sift-compare
(assert (not (m_panicked formal_0_442)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_442) (select (m_origin formal_0_442) 42) (select (m_origin formal_0_442) 6)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_442) (select (m_origin formal_0_442) 42) (select (m_origin formal_0_442) 6)) false))
; source callback transition phase=insert-tail[24:35:9]:sift-compare
(define-fun formal_0_443 () FormalMachine (FormalCallback formal_0_442 boundary_0 (select (m_origin formal_0_442) 42) (select (m_origin formal_0_442) 6)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:9]
(define-fun formal_0_444 () FormalMachine (FormalWriteFromOrigin formal_0_443 26 6))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:9]:sift-compare
(assert (not (m_panicked formal_0_444)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_444) (select (m_origin formal_0_444) 42) (select (m_origin formal_0_444) 1)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_444) (select (m_origin formal_0_444) 42) (select (m_origin formal_0_444) 1)) false))
; source callback transition phase=insert-tail[24:35:9]:sift-compare
(define-fun formal_0_445 () FormalMachine (FormalCallback formal_0_444 boundary_0 (select (m_origin formal_0_444) 42) (select (m_origin formal_0_444) 1)))
; source write kind=copy-on-drop-restore phase=insert-tail[24:35:9]
(define-fun formal_0_446 () FormalMachine (FormalWriteFromOrigin formal_0_445 25 42))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:10]:initial-compare
(assert (not (m_panicked formal_0_446)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_446) (select (m_origin formal_0_446) 43) (select (m_origin formal_0_446) 17)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_446) (select (m_origin formal_0_446) 43) (select (m_origin formal_0_446) 17)) false))
; source callback transition phase=insert-tail[24:35:10]:initial-compare
(define-fun formal_0_447 () FormalMachine (FormalCallback formal_0_446 boundary_0 (select (m_origin formal_0_446) 43) (select (m_origin formal_0_446) 17)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:10]
(define-fun formal_0_448 () FormalMachine (FormalWriteFromOrigin formal_0_447 34 17))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:10]:sift-compare
(assert (not (m_panicked formal_0_448)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_448) (select (m_origin formal_0_448) 43) (select (m_origin formal_0_448) 26)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_448) (select (m_origin formal_0_448) 43) (select (m_origin formal_0_448) 26)) false))
; source callback transition phase=insert-tail[24:35:10]:sift-compare
(define-fun formal_0_449 () FormalMachine (FormalCallback formal_0_448 boundary_0 (select (m_origin formal_0_448) 43) (select (m_origin formal_0_448) 26)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:10]
(define-fun formal_0_450 () FormalMachine (FormalWriteFromOrigin formal_0_449 33 26))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:10]:sift-compare
(assert (not (m_panicked formal_0_450)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_450) (select (m_origin formal_0_450) 43) (select (m_origin formal_0_450) 27)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_450) (select (m_origin formal_0_450) 43) (select (m_origin formal_0_450) 27)) false))
; source callback transition phase=insert-tail[24:35:10]:sift-compare
(define-fun formal_0_451 () FormalMachine (FormalCallback formal_0_450 boundary_0 (select (m_origin formal_0_450) 43) (select (m_origin formal_0_450) 27)))
; source write kind=insert-tail-shift phase=insert-tail[24:35:10]
(define-fun formal_0_452 () FormalMachine (FormalWriteFromOrigin formal_0_451 32 27))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[24:35:10]:sift-compare
(assert (not (m_panicked formal_0_452)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_452) (select (m_origin formal_0_452) 43) (select (m_origin formal_0_452) 29)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_452) (select (m_origin formal_0_452) 43) (select (m_origin formal_0_452) 29)) false))
; source callback transition phase=insert-tail[24:35:10]:sift-compare
(define-fun formal_0_453 () FormalMachine (FormalCallback formal_0_452 boundary_0 (select (m_origin formal_0_452) 43) (select (m_origin formal_0_452) 29)))
; source write kind=copy-on-drop-restore phase=insert-tail[24:35:10]
(define-fun formal_0_454 () FormalMachine (FormalWriteFromOrigin formal_0_453 31 43))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:1]:initial-compare
(assert (not (m_panicked formal_0_454)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_454) (select (m_origin formal_0_454) 30) (select (m_origin formal_0_454) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_454) (select (m_origin formal_0_454) 30) (select (m_origin formal_0_454) 3)) false))
; source callback transition phase=insert-tail[36:45:1]:initial-compare
(define-fun formal_0_455 () FormalMachine (FormalCallback formal_0_454 boundary_0 (select (m_origin formal_0_454) 30) (select (m_origin formal_0_454) 3)))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:2]:initial-compare
(assert (not (m_panicked formal_0_455)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_455) (select (m_origin formal_0_455) 14) (select (m_origin formal_0_455) 30)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_455) (select (m_origin formal_0_455) 14) (select (m_origin formal_0_455) 30)) false))
; source callback transition phase=insert-tail[36:45:2]:initial-compare
(define-fun formal_0_456 () FormalMachine (FormalCallback formal_0_455 boundary_0 (select (m_origin formal_0_455) 14) (select (m_origin formal_0_455) 30)))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:3]:initial-compare
(assert (not (m_panicked formal_0_456)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_456) (select (m_origin formal_0_456) 21) (select (m_origin formal_0_456) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_456) (select (m_origin formal_0_456) 21) (select (m_origin formal_0_456) 14)) false))
; source callback transition phase=insert-tail[36:45:3]:initial-compare
(define-fun formal_0_457 () FormalMachine (FormalCallback formal_0_456 boundary_0 (select (m_origin formal_0_456) 21) (select (m_origin formal_0_456) 14)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:3]
(define-fun formal_0_458 () FormalMachine (FormalWriteFromOrigin formal_0_457 39 14))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:3]:sift-compare
(assert (not (m_panicked formal_0_458)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_458) (select (m_origin formal_0_458) 21) (select (m_origin formal_0_458) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_458) (select (m_origin formal_0_458) 21) (select (m_origin formal_0_458) 30)) false))
; source callback transition phase=insert-tail[36:45:3]:sift-compare
(define-fun formal_0_459 () FormalMachine (FormalCallback formal_0_458 boundary_0 (select (m_origin formal_0_458) 21) (select (m_origin formal_0_458) 30)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:3]
(define-fun formal_0_460 () FormalMachine (FormalWriteFromOrigin formal_0_459 38 30))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:3]:sift-compare
(assert (not (m_panicked formal_0_460)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_460) (select (m_origin formal_0_460) 21) (select (m_origin formal_0_460) 3)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_460) (select (m_origin formal_0_460) 21) (select (m_origin formal_0_460) 3)) false))
; source callback transition phase=insert-tail[36:45:3]:sift-compare
(define-fun formal_0_461 () FormalMachine (FormalCallback formal_0_460 boundary_0 (select (m_origin formal_0_460) 21) (select (m_origin formal_0_460) 3)))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:3]
(define-fun formal_0_462 () FormalMachine (FormalWriteFromOrigin formal_0_461 37 21))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:4]:initial-compare
(assert (not (m_panicked formal_0_462)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_462) (select (m_origin formal_0_462) 2) (select (m_origin formal_0_462) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_462) (select (m_origin formal_0_462) 2) (select (m_origin formal_0_462) 14)) false))
; source callback transition phase=insert-tail[36:45:4]:initial-compare
(define-fun formal_0_463 () FormalMachine (FormalCallback formal_0_462 boundary_0 (select (m_origin formal_0_462) 2) (select (m_origin formal_0_462) 14)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:4]
(define-fun formal_0_464 () FormalMachine (FormalWriteFromOrigin formal_0_463 40 14))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:4]:sift-compare
(assert (not (m_panicked formal_0_464)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_464) (select (m_origin formal_0_464) 2) (select (m_origin formal_0_464) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_464) (select (m_origin formal_0_464) 2) (select (m_origin formal_0_464) 30)) false))
; source callback transition phase=insert-tail[36:45:4]:sift-compare
(define-fun formal_0_465 () FormalMachine (FormalCallback formal_0_464 boundary_0 (select (m_origin formal_0_464) 2) (select (m_origin formal_0_464) 30)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:4]
(define-fun formal_0_466 () FormalMachine (FormalWriteFromOrigin formal_0_465 39 30))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:4]:sift-compare
(assert (not (m_panicked formal_0_466)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_466) (select (m_origin formal_0_466) 2) (select (m_origin formal_0_466) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_466) (select (m_origin formal_0_466) 2) (select (m_origin formal_0_466) 21)) false))
; source callback transition phase=insert-tail[36:45:4]:sift-compare
(define-fun formal_0_467 () FormalMachine (FormalCallback formal_0_466 boundary_0 (select (m_origin formal_0_466) 2) (select (m_origin formal_0_466) 21)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:4]
(define-fun formal_0_468 () FormalMachine (FormalWriteFromOrigin formal_0_467 38 21))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:4]:sift-compare
(assert (not (m_panicked formal_0_468)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_468) (select (m_origin formal_0_468) 2) (select (m_origin formal_0_468) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_468) (select (m_origin formal_0_468) 2) (select (m_origin formal_0_468) 3)) false))
; source callback transition phase=insert-tail[36:45:4]:sift-compare
(define-fun formal_0_469 () FormalMachine (FormalCallback formal_0_468 boundary_0 (select (m_origin formal_0_468) 2) (select (m_origin formal_0_468) 3)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:4]
(define-fun formal_0_470 () FormalMachine (FormalWriteFromOrigin formal_0_469 37 3))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:4]
(define-fun formal_0_471 () FormalMachine (FormalWriteFromOrigin formal_0_470 36 2))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:5]:initial-compare
(assert (not (m_panicked formal_0_471)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_471) (select (m_origin formal_0_471) 7) (select (m_origin formal_0_471) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_471) (select (m_origin formal_0_471) 7) (select (m_origin formal_0_471) 14)) false))
; source callback transition phase=insert-tail[36:45:5]:initial-compare
(define-fun formal_0_472 () FormalMachine (FormalCallback formal_0_471 boundary_0 (select (m_origin formal_0_471) 7) (select (m_origin formal_0_471) 14)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:5]
(define-fun formal_0_473 () FormalMachine (FormalWriteFromOrigin formal_0_472 41 14))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:5]:sift-compare
(assert (not (m_panicked formal_0_473)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_473) (select (m_origin formal_0_473) 7) (select (m_origin formal_0_473) 30)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_473) (select (m_origin formal_0_473) 7) (select (m_origin formal_0_473) 30)) false))
; source callback transition phase=insert-tail[36:45:5]:sift-compare
(define-fun formal_0_474 () FormalMachine (FormalCallback formal_0_473 boundary_0 (select (m_origin formal_0_473) 7) (select (m_origin formal_0_473) 30)))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:5]
(define-fun formal_0_475 () FormalMachine (FormalWriteFromOrigin formal_0_474 40 7))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:6]:initial-compare
(assert (not (m_panicked formal_0_475)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_475) (select (m_origin formal_0_475) 34) (select (m_origin formal_0_475) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_475) (select (m_origin formal_0_475) 34) (select (m_origin formal_0_475) 14)) false))
; source callback transition phase=insert-tail[36:45:6]:initial-compare
(define-fun formal_0_476 () FormalMachine (FormalCallback formal_0_475 boundary_0 (select (m_origin formal_0_475) 34) (select (m_origin formal_0_475) 14)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:6]
(define-fun formal_0_477 () FormalMachine (FormalWriteFromOrigin formal_0_476 42 14))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:6]:sift-compare
(assert (not (m_panicked formal_0_477)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_477) (select (m_origin formal_0_477) 34) (select (m_origin formal_0_477) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_477) (select (m_origin formal_0_477) 34) (select (m_origin formal_0_477) 7)) false))
; source callback transition phase=insert-tail[36:45:6]:sift-compare
(define-fun formal_0_478 () FormalMachine (FormalCallback formal_0_477 boundary_0 (select (m_origin formal_0_477) 34) (select (m_origin formal_0_477) 7)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:6]
(define-fun formal_0_479 () FormalMachine (FormalWriteFromOrigin formal_0_478 41 7))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:6]:sift-compare
(assert (not (m_panicked formal_0_479)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_479) (select (m_origin formal_0_479) 34) (select (m_origin formal_0_479) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_479) (select (m_origin formal_0_479) 34) (select (m_origin formal_0_479) 30)) false))
; source callback transition phase=insert-tail[36:45:6]:sift-compare
(define-fun formal_0_480 () FormalMachine (FormalCallback formal_0_479 boundary_0 (select (m_origin formal_0_479) 34) (select (m_origin formal_0_479) 30)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:6]
(define-fun formal_0_481 () FormalMachine (FormalWriteFromOrigin formal_0_480 40 30))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:6]:sift-compare
(assert (not (m_panicked formal_0_481)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_481) (select (m_origin formal_0_481) 34) (select (m_origin formal_0_481) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_481) (select (m_origin formal_0_481) 34) (select (m_origin formal_0_481) 21)) false))
; source callback transition phase=insert-tail[36:45:6]:sift-compare
(define-fun formal_0_482 () FormalMachine (FormalCallback formal_0_481 boundary_0 (select (m_origin formal_0_481) 34) (select (m_origin formal_0_481) 21)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:6]
(define-fun formal_0_483 () FormalMachine (FormalWriteFromOrigin formal_0_482 39 21))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:6]:sift-compare
(assert (not (m_panicked formal_0_483)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_483) (select (m_origin formal_0_483) 34) (select (m_origin formal_0_483) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_483) (select (m_origin formal_0_483) 34) (select (m_origin formal_0_483) 3)) false))
; source callback transition phase=insert-tail[36:45:6]:sift-compare
(define-fun formal_0_484 () FormalMachine (FormalCallback formal_0_483 boundary_0 (select (m_origin formal_0_483) 34) (select (m_origin formal_0_483) 3)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:6]
(define-fun formal_0_485 () FormalMachine (FormalWriteFromOrigin formal_0_484 38 3))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:6]:sift-compare
(assert (not (m_panicked formal_0_485)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_485) (select (m_origin formal_0_485) 34) (select (m_origin formal_0_485) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_485) (select (m_origin formal_0_485) 34) (select (m_origin formal_0_485) 2)) false))
; source callback transition phase=insert-tail[36:45:6]:sift-compare
(define-fun formal_0_486 () FormalMachine (FormalCallback formal_0_485 boundary_0 (select (m_origin formal_0_485) 34) (select (m_origin formal_0_485) 2)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:6]
(define-fun formal_0_487 () FormalMachine (FormalWriteFromOrigin formal_0_486 37 2))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:6]
(define-fun formal_0_488 () FormalMachine (FormalWriteFromOrigin formal_0_487 36 34))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:7]:initial-compare
(assert (not (m_panicked formal_0_488)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_488) (select (m_origin formal_0_488) 23) (select (m_origin formal_0_488) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_488) (select (m_origin formal_0_488) 23) (select (m_origin formal_0_488) 14)) false))
; source callback transition phase=insert-tail[36:45:7]:initial-compare
(define-fun formal_0_489 () FormalMachine (FormalCallback formal_0_488 boundary_0 (select (m_origin formal_0_488) 23) (select (m_origin formal_0_488) 14)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:7]
(define-fun formal_0_490 () FormalMachine (FormalWriteFromOrigin formal_0_489 43 14))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:7]:sift-compare
(assert (not (m_panicked formal_0_490)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_490) (select (m_origin formal_0_490) 23) (select (m_origin formal_0_490) 7)) false))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_490) (select (m_origin formal_0_490) 23) (select (m_origin formal_0_490) 7)) false))
; source callback transition phase=insert-tail[36:45:7]:sift-compare
(define-fun formal_0_491 () FormalMachine (FormalCallback formal_0_490 boundary_0 (select (m_origin formal_0_490) 23) (select (m_origin formal_0_490) 7)))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:7]
(define-fun formal_0_492 () FormalMachine (FormalWriteFromOrigin formal_0_491 42 23))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:8]:initial-compare
(assert (not (m_panicked formal_0_492)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_492) (select (m_origin formal_0_492) 8) (select (m_origin formal_0_492) 14)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_492) (select (m_origin formal_0_492) 8) (select (m_origin formal_0_492) 14)) false))
; source callback transition phase=insert-tail[36:45:8]:initial-compare
(define-fun formal_0_493 () FormalMachine (FormalCallback formal_0_492 boundary_0 (select (m_origin formal_0_492) 8) (select (m_origin formal_0_492) 14)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:8]
(define-fun formal_0_494 () FormalMachine (FormalWriteFromOrigin formal_0_493 44 14))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:8]:sift-compare
(assert (not (m_panicked formal_0_494)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_494) (select (m_origin formal_0_494) 8) (select (m_origin formal_0_494) 23)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_494) (select (m_origin formal_0_494) 8) (select (m_origin formal_0_494) 23)) false))
; source callback transition phase=insert-tail[36:45:8]:sift-compare
(define-fun formal_0_495 () FormalMachine (FormalCallback formal_0_494 boundary_0 (select (m_origin formal_0_494) 8) (select (m_origin formal_0_494) 23)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:8]
(define-fun formal_0_496 () FormalMachine (FormalWriteFromOrigin formal_0_495 43 23))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:8]:sift-compare
(assert (not (m_panicked formal_0_496)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_496) (select (m_origin formal_0_496) 8) (select (m_origin formal_0_496) 7)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_496) (select (m_origin formal_0_496) 8) (select (m_origin formal_0_496) 7)) false))
; source callback transition phase=insert-tail[36:45:8]:sift-compare
(define-fun formal_0_497 () FormalMachine (FormalCallback formal_0_496 boundary_0 (select (m_origin formal_0_496) 8) (select (m_origin formal_0_496) 7)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:8]
(define-fun formal_0_498 () FormalMachine (FormalWriteFromOrigin formal_0_497 42 7))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:8]:sift-compare
(assert (not (m_panicked formal_0_498)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_498) (select (m_origin formal_0_498) 8) (select (m_origin formal_0_498) 30)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_498) (select (m_origin formal_0_498) 8) (select (m_origin formal_0_498) 30)) false))
; source callback transition phase=insert-tail[36:45:8]:sift-compare
(define-fun formal_0_499 () FormalMachine (FormalCallback formal_0_498 boundary_0 (select (m_origin formal_0_498) 8) (select (m_origin formal_0_498) 30)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:8]
(define-fun formal_0_500 () FormalMachine (FormalWriteFromOrigin formal_0_499 41 30))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:8]:sift-compare
(assert (not (m_panicked formal_0_500)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_500) (select (m_origin formal_0_500) 8) (select (m_origin formal_0_500) 21)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_500) (select (m_origin formal_0_500) 8) (select (m_origin formal_0_500) 21)) false))
; source callback transition phase=insert-tail[36:45:8]:sift-compare
(define-fun formal_0_501 () FormalMachine (FormalCallback formal_0_500 boundary_0 (select (m_origin formal_0_500) 8) (select (m_origin formal_0_500) 21)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:8]
(define-fun formal_0_502 () FormalMachine (FormalWriteFromOrigin formal_0_501 40 21))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:8]:sift-compare
(assert (not (m_panicked formal_0_502)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_502) (select (m_origin formal_0_502) 8) (select (m_origin formal_0_502) 3)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_502) (select (m_origin formal_0_502) 8) (select (m_origin formal_0_502) 3)) false))
; source callback transition phase=insert-tail[36:45:8]:sift-compare
(define-fun formal_0_503 () FormalMachine (FormalCallback formal_0_502 boundary_0 (select (m_origin formal_0_502) 8) (select (m_origin formal_0_502) 3)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:8]
(define-fun formal_0_504 () FormalMachine (FormalWriteFromOrigin formal_0_503 39 3))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:8]:sift-compare
(assert (not (m_panicked formal_0_504)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_504) (select (m_origin formal_0_504) 8) (select (m_origin formal_0_504) 2)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_504) (select (m_origin formal_0_504) 8) (select (m_origin formal_0_504) 2)) false))
; source callback transition phase=insert-tail[36:45:8]:sift-compare
(define-fun formal_0_505 () FormalMachine (FormalCallback formal_0_504 boundary_0 (select (m_origin formal_0_504) 8) (select (m_origin formal_0_504) 2)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:8]
(define-fun formal_0_506 () FormalMachine (FormalWriteFromOrigin formal_0_505 38 2))
; source callback case=fallback-small-sort-and-recursion phase=insert-tail[36:45:8]:sift-compare
(assert (not (m_panicked formal_0_506)))
(assert (= (TargetAdapterIsLess boundary_0 (m_callback formal_0_506) (select (m_origin formal_0_506) 8) (select (m_origin formal_0_506) 34)) true))
(assert (= (BoundaryPanics boundary_0 (m_callback formal_0_506) (select (m_origin formal_0_506) 8) (select (m_origin formal_0_506) 34)) false))
; source callback transition phase=insert-tail[36:45:8]:sift-compare
(define-fun formal_0_507 () FormalMachine (FormalCallback formal_0_506 boundary_0 (select (m_origin formal_0_506) 8) (select (m_origin formal_0_506) 34)))
; source write kind=insert-tail-shift phase=insert-tail[36:45:8]
(define-fun formal_0_508 () FormalMachine (FormalWriteFromOrigin formal_0_507 37 34))
; source write kind=copy-on-drop-restore phase=insert-tail[36:45:8]
(define-fun formal_0_509 () FormalMachine (FormalWriteFromOrigin formal_0_508 36 8))
(define-fun formal_result_0 () Result
  (mkResult
    (m_sequence formal_0_509)
    (m_callback formal_0_509)
    (m_panicked formal_0_509)
    false
    true
    (ite (m_panicked formal_0_509) 1 0)
    (not (m_panicked formal_0_509))
    -1))
(define-fun reference_result_0 () Result (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 21 21) 22 22) 23 23) 24 24) 25 25) 26 26) 27 27) 28 28) 29 29) 30 30) 31 31) 32 32) 33 33) 34 34) 35 35) 36 36) 37 37) 38 38) 39 39) 40 40) 41 41) 42 42) 43 43) 44 44) 236 false false true 0 true -1))
; retained source-forcing witness: small-sort-fallback
(assert (= formal_result_0 (mkResult (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 21 21) 22 22) 23 23) 24 24) 25 25) 26 26) 27 27) 28 28) 29 29) 30 30) 31 31) 32 32) 33 33) 34 34) 35 35) 36 36) 37 37) 38 38) 39 39) 40 40) 41 41) 42 42) 43 43) 44 44) 236 false false true 0 true -1)))
(check-sat-using (then ctx-solver-simplify smt))
