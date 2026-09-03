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

(declare-datatypes ((DropKey 0))
  (((mkDropKey (drop_state Int) (drop_unwinding Bool)))))
(declare-datatypes ((DropBoundary 0))
  (((mkDropBoundary
      (db_next_state (Array DropKey Int))
      (db_panics (Array DropKey Bool))))))
(declare-datatypes ((PublicResult081 0))
  (((mkPublicResult081
      (p_sequence (Array Int Int))
      (p_callback Int)
      (p_panicked Bool)
      (p_aborted Bool)
      (p_terminal Bool)
      (p_status Int)
      (p_unit Bool)
      (p_drop_invoked Bool)
      (p_drop_completed Bool)))))
(define-fun FinishPublic081
  ((private ExactState) (drop_boundary DropBoundary)) PublicResult081
  (let ((unwinding (e_panicked private)))
    (let ((next_state
            (select
              (db_next_state drop_boundary)
              (mkDropKey (e_callback_state private) unwinding)))
          (drop_panics
            (select
              (db_panics drop_boundary)
              (mkDropKey (e_callback_state private) unwinding))))
      (let ((status
              (ite drop_panics
                (ite unwinding 2 1)
                (ite unwinding 1 0))))
        (mkPublicResult081
          (e_sequence private)
          next_state
          (= status 1)
          (= status 2)
          true
          status
          (= status 0)
          true
          (not drop_panics))))))
; fixed Boundary_T source case=inherited-zst-return
(define-fun boundary081_0 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_0 () SortConfiguration
  (mkSortConfiguration
    false
    64
    0
    false
    false))
(define-fun initial081_0 () ExactState
  (mkExactState (store (store (store ((as const (Array Int Int)) 0) 0 3) 1 2) 2 1) 0 false))
(define-fun drop081_0 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_0 () ExactState
  (ExactSort initial081_0 boundary081_0 configuration081_0 3))
(define-fun private_right081_0 () ExactState
  (ExactSort initial081_0 boundary081_0 configuration081_0 3))
(define-fun public_left081_0 () PublicResult081
  (FinishPublic081 private_left081_0 drop081_0))
(define-fun public_right081_0 () PublicResult081
  (FinishPublic081 private_right081_0 drop081_0))
(assert (not (= public_left081_0 public_right081_0)))
; fixed Boundary_T source case=inherited-trivial-return
(define-fun boundary081_1 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_1 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_1 () ExactState
  (mkExactState (store ((as const (Array Int Int)) 0) 0 7) 0 false))
(define-fun drop081_1 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_1 () ExactState
  (ExactSort initial081_1 boundary081_1 configuration081_1 1))
(define-fun private_right081_1 () ExactState
  (ExactSort initial081_1 boundary081_1 configuration081_1 1))
(define-fun public_left081_1 () PublicResult081
  (FinishPublic081 private_left081_1 drop081_1))
(define-fun public_right081_1 () PublicResult081
  (FinishPublic081 private_right081_1 drop081_1))
(assert (not (= public_left081_1 public_right081_1)))
; fixed Boundary_T source case=inherited-normal-insertion
(define-fun boundary081_2 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_2 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_2 () ExactState
  (mkExactState (store (store (store (store ((as const (Array Int Int)) 0) 0 4) 1 1) 2 3) 3 2) 0 false))
(define-fun drop081_2 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_2 () ExactState
  (ExactSort initial081_2 boundary081_2 configuration081_2 4))
(define-fun private_right081_2 () ExactState
  (ExactSort initial081_2 boundary081_2 configuration081_2 4))
(define-fun public_left081_2 () PublicResult081
  (FinishPublic081 private_left081_2 drop081_2))
(define-fun public_right081_2 () PublicResult081
  (FinishPublic081 private_right081_2 drop081_2))
(assert (not (= public_left081_2 public_right081_2)))
; fixed Boundary_T source case=inherited-ascending-existing-run
(define-fun boundary081_3 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_3 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_3 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 0) 1 1) 2 2) 3 3) 4 4) 5 5) 6 6) 7 7) 8 8) 9 9) 10 10) 11 11) 12 12) 13 13) 14 14) 15 15) 16 16) 17 17) 18 18) 19 19) 20 20) 0 false))
(define-fun drop081_3 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_3 () ExactState
  (ExactSort initial081_3 boundary081_3 configuration081_3 21))
(define-fun private_right081_3 () ExactState
  (ExactSort initial081_3 boundary081_3 configuration081_3 21))
(define-fun public_left081_3 () PublicResult081
  (FinishPublic081 private_left081_3 drop081_3))
(define-fun public_right081_3 () PublicResult081
  (FinishPublic081 private_right081_3 drop081_3))
(assert (not (= public_left081_3 public_right081_3)))
; fixed Boundary_T source case=inherited-descending-existing-run
(define-fun boundary081_4 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_4 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_4 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 20) 1 19) 2 18) 3 17) 4 16) 5 15) 6 14) 7 13) 8 12) 9 11) 10 10) 11 9) 12 8) 13 7) 14 6) 15 5) 16 4) 17 3) 18 2) 19 1) 20 0) 0 false))
(define-fun drop081_4 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_4 () ExactState
  (ExactSort initial081_4 boundary081_4 configuration081_4 21))
(define-fun private_right081_4 () ExactState
  (ExactSort initial081_4 boundary081_4 configuration081_4 21))
(define-fun public_left081_4 () PublicResult081
  (FinishPublic081 private_left081_4 drop081_4))
(define-fun public_right081_4 () PublicResult081
  (FinishPublic081 private_right081_4 drop081_4))
(assert (not (= public_left081_4 public_right081_4)))
; fixed Boundary_T source case=inherited-configuration-heapsort-size
(define-fun boundary081_5 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_5 () SortConfiguration
  (mkSortConfiguration
    true
    64
    8
    false
    false))
(define-fun initial081_5 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 5) 1 3) 2 23) 3 8) 4 7) 5 12) 6 16) 7 4) 8 17) 9 1) 10 10) 11 20) 12 11) 13 2) 14 15) 15 0) 16 22) 17 21) 18 14) 19 13) 20 24) 21 6) 22 9) 23 19) 24 18) 0 false))
(define-fun drop081_5 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_5 () ExactState
  (ExactSort initial081_5 boundary081_5 configuration081_5 25))
(define-fun private_right081_5 () ExactState
  (ExactSort initial081_5 boundary081_5 configuration081_5 25))
(define-fun public_left081_5 () PublicResult081
  (FinishPublic081 private_left081_5 drop081_5))
(define-fun public_right081_5 () PublicResult081
  (FinishPublic081 private_right081_5 drop081_5))
(assert (not (= public_left081_5 public_right081_5)))
; fixed Boundary_T source case=inherited-configuration-heapsort-16-bit
(define-fun boundary081_6 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_6 () SortConfiguration
  (mkSortConfiguration
    false
    16
    8
    false
    false))
(define-fun initial081_6 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 20) 1 6) 2 13) 3 5) 4 1) 5 21) 6 9) 7 8) 8 0) 9 22) 10 10) 11 16) 12 19) 13 3) 14 2) 15 14) 16 24) 17 11) 18 23) 19 4) 20 15) 21 18) 22 12) 23 7) 24 17) 0 false))
(define-fun drop081_6 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_6 () ExactState
  (ExactSort initial081_6 boundary081_6 configuration081_6 25))
(define-fun private_right081_6 () ExactState
  (ExactSort initial081_6 boundary081_6 configuration081_6 25))
(define-fun public_left081_6 () PublicResult081
  (FinishPublic081 private_left081_6 drop081_6))
(define-fun public_right081_6 () PublicResult081
  (FinishPublic081 private_right081_6 drop081_6))
(assert (not (= public_left081_6 public_right081_6)))
; fixed Boundary_T source case=inherited-fallback-small-sort-and-recursion
(define-fun boundary081_7 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_7 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_7 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 5) 1 24) 2 38) 3 39) 4 28) 5 27) 6 26) 7 42) 8 36) 9 20) 10 19) 11 12) 12 1) 13 3) 14 44) 15 4) 16 0) 17 34) 18 21) 19 13) 20 11) 21 40) 22 10) 23 43) 24 9) 25 14) 26 33) 27 32) 28 35) 29 30) 30 41) 31 7) 32 29) 33 23) 34 37) 35 18) 36 2) 37 6) 38 22) 39 17) 40 8) 41 16) 42 25) 43 31) 44 15) 0 false))
(define-fun drop081_7 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_7 () ExactState
  (ExactSort initial081_7 boundary081_7 configuration081_7 45))
(define-fun private_right081_7 () ExactState
  (ExactSort initial081_7 boundary081_7 configuration081_7 45))
(define-fun public_left081_7 () PublicResult081
  (FinishPublic081 private_left081_7 drop081_7))
(define-fun public_right081_7 () PublicResult081
  (FinishPublic081 private_right081_7 drop081_7))
(assert (not (= public_left081_7 public_right081_7)))
; fixed Boundary_T source case=inherited-network-small-sort-sort13-merge
(define-fun boundary081_8 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_8 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    true
    true))
(define-fun initial081_8 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 22) 1 12) 2 14) 3 10) 4 4) 5 1) 6 11) 7 21) 8 19) 9 0) 10 20) 11 8) 12 3) 13 13) 14 25) 15 17) 16 7) 17 9) 18 2) 19 24) 20 18) 21 6) 22 5) 23 23) 24 16) 25 15) 0 false))
(define-fun drop081_8 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_8 () ExactState
  (ExactSort initial081_8 boundary081_8 configuration081_8 26))
(define-fun private_right081_8 () ExactState
  (ExactSort initial081_8 boundary081_8 configuration081_8 26))
(define-fun public_left081_8 () PublicResult081
  (FinishPublic081 private_left081_8 drop081_8))
(define-fun public_right081_8 () PublicResult081
  (FinishPublic081 private_right081_8 drop081_8))
(assert (not (= public_left081_8 public_right081_8)))
; fixed Boundary_T source case=inherited-general-small-sort-scratch-merge
(define-fun boundary081_9 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_9 () SortConfiguration
  (mkSortConfiguration
    false
    64
    24
    true
    true))
(define-fun initial081_9 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 14) 1 10) 2 9) 3 18) 4 22) 5 13) 6 2) 7 19) 8 7) 9 24) 10 8) 11 20) 12 3) 13 6) 14 0) 15 25) 16 16) 17 1) 18 15) 19 21) 20 5) 21 12) 22 11) 23 23) 24 17) 25 4) 0 false))
(define-fun drop081_9 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_9 () ExactState
  (ExactSort initial081_9 boundary081_9 configuration081_9 26))
(define-fun private_right081_9 () ExactState
  (ExactSort initial081_9 boundary081_9 configuration081_9 26))
(define-fun public_left081_9 () PublicResult081
  (FinishPublic081 private_left081_9 drop081_9))
(define-fun public_right081_9 () PublicResult081
  (FinishPublic081 private_right081_9 drop081_9))
(assert (not (= public_left081_9 public_right081_9)))
; fixed Boundary_T source case=inherited-recursive-pivot
(define-fun boundary081_10 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_10 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_10 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 74) 1 30) 2 59) 3 32) 4 15) 5 70) 6 78) 7 76) 8 20) 9 28) 10 37) 11 72) 12 41) 13 67) 14 13) 15 31) 16 0) 17 16) 18 54) 19 63) 20 19) 21 17) 22 10) 23 21) 24 49) 25 39) 26 4) 27 2) 28 79) 29 29) 30 57) 31 25) 32 47) 33 3) 34 36) 35 77) 36 34) 37 55) 38 23) 39 5) 40 40) 41 35) 42 66) 43 71) 44 43) 45 68) 46 46) 47 27) 48 52) 49 69) 50 7) 51 8) 52 22) 53 48) 54 51) 55 14) 56 11) 57 12) 58 9) 59 62) 60 45) 61 56) 62 42) 63 18) 64 1) 65 64) 66 24) 67 73) 68 65) 69 38) 70 26) 71 58) 72 75) 73 33) 74 44) 75 50) 76 60) 77 53) 78 61) 79 6) 0 false))
(define-fun drop081_10 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_10 () ExactState
  (ExactSort initial081_10 boundary081_10 configuration081_10 80))
(define-fun private_right081_10 () ExactState
  (ExactSort initial081_10 boundary081_10 configuration081_10 80))
(define-fun public_left081_10 () PublicResult081
  (FinishPublic081 private_left081_10 drop081_10))
(define-fun public_right081_10 () PublicResult081
  (FinishPublic081 private_right081_10 drop081_10))
(assert (not (= public_left081_10 public_right081_10)))
; fixed Boundary_T source case=inherited-hoare-partition
(define-fun boundary081_11 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_11 () SortConfiguration
  (mkSortConfiguration
    false
    64
    128
    false
    false))
(define-fun initial081_11 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 40) 1 18) 2 16) 3 13) 4 32) 5 29) 6 42) 7 37) 8 4) 9 11) 10 2) 11 44) 12 6) 13 31) 14 34) 15 38) 16 39) 17 22) 18 20) 19 41) 20 10) 21 30) 22 15) 23 21) 24 17) 25 8) 26 19) 27 24) 28 43) 29 23) 30 14) 31 33) 32 27) 33 35) 34 0) 35 3) 36 1) 37 7) 38 25) 39 12) 40 36) 41 26) 42 9) 43 5) 44 28) 0 false))
(define-fun drop081_11 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_11 () ExactState
  (ExactSort initial081_11 boundary081_11 configuration081_11 45))
(define-fun private_right081_11 () ExactState
  (ExactSort initial081_11 boundary081_11 configuration081_11 45))
(define-fun public_left081_11 () PublicResult081
  (FinishPublic081 private_left081_11 drop081_11))
(define-fun public_right081_11 () PublicResult081
  (FinishPublic081 private_right081_11 drop081_11))
(assert (not (= public_left081_11 public_right081_11)))
; fixed Boundary_T source case=inherited-cyclic-unroll-one-partition
(define-fun boundary081_12 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_12 () SortConfiguration
  (mkSortConfiguration
    false
    64
    32
    false
    false))
(define-fun initial081_12 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 27) 1 14) 2 30) 3 13) 4 0) 5 18) 6 19) 7 7) 8 10) 9 5) 10 43) 11 38) 12 15) 13 11) 14 6) 15 42) 16 39) 17 4) 18 2) 19 29) 20 1) 21 21) 22 37) 23 32) 24 17) 25 35) 26 24) 27 31) 28 16) 29 3) 30 40) 31 12) 32 25) 33 20) 34 23) 35 22) 36 36) 37 34) 38 26) 39 28) 40 41) 41 8) 42 44) 43 9) 44 33) 0 false))
(define-fun drop081_12 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_12 () ExactState
  (ExactSort initial081_12 boundary081_12 configuration081_12 45))
(define-fun private_right081_12 () ExactState
  (ExactSort initial081_12 boundary081_12 configuration081_12 45))
(define-fun public_left081_12 () PublicResult081
  (FinishPublic081 private_left081_12 drop081_12))
(define-fun public_right081_12 () PublicResult081
  (FinishPublic081 private_right081_12 drop081_12))
(assert (not (= public_left081_12 public_right081_12)))
; fixed Boundary_T source case=inherited-duplicate-class-ancestor-pivot
(define-fun boundary081_13 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (or (< (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4) (= (pair_left_identity key) 5) (= (pair_left_identity key) 6) (= (pair_left_identity key) 7) (= (pair_left_identity key) 8) (= (pair_left_identity key) 9) (= (pair_left_identity key) 10) (= (pair_left_identity key) 11) (= (pair_left_identity key) 12) (= (pair_left_identity key) 13) (= (pair_left_identity key) 14) (= (pair_left_identity key) 15) (= (pair_left_identity key) 16) (= (pair_left_identity key) 17) (= (pair_left_identity key) 18) (= (pair_left_identity key) 19) (= (pair_left_identity key) 20) (= (pair_left_identity key) 21) (= (pair_left_identity key) 22) (= (pair_left_identity key) 23) (= (pair_left_identity key) 24) (= (pair_left_identity key) 25) (= (pair_left_identity key) 26) (= (pair_left_identity key) 27) (= (pair_left_identity key) 28) (= (pair_left_identity key) 29) (= (pair_left_identity key) 30) (= (pair_left_identity key) 31) (= (pair_left_identity key) 32) (= (pair_left_identity key) 33) (= (pair_left_identity key) 34) (= (pair_left_identity key) 35) (= (pair_left_identity key) 36) (= (pair_left_identity key) 37) (= (pair_left_identity key) 38) (= (pair_left_identity key) 39) (= (pair_left_identity key) 40) (= (pair_left_identity key) 41) (= (pair_left_identity key) 42) (= (pair_left_identity key) 43) (= (pair_left_identity key) 44) (= (pair_left_identity key) 45) (= (pair_left_identity key) 46) (= (pair_left_identity key) 47) (= (pair_left_identity key) 48) (= (pair_left_identity key) 49) (= (pair_left_identity key) 50) (= (pair_left_identity key) 51) (= (pair_left_identity key) 52) (= (pair_left_identity key) 53) (= (pair_left_identity key) 54) (= (pair_left_identity key) 55) (= (pair_left_identity key) 56) (= (pair_left_identity key) 57) (= (pair_left_identity key) 58) (= (pair_left_identity key) 59) (= (pair_left_identity key) 60) (= (pair_left_identity key) 61) (= (pair_left_identity key) 62) (= (pair_left_identity key) 63) (= (pair_left_identity key) 64) (= (pair_left_identity key) 65) (= (pair_left_identity key) 66) (= (pair_left_identity key) 67) (= (pair_left_identity key) 68) (= (pair_left_identity key) 69) (= (pair_left_identity key) 70) (= (pair_left_identity key) 71) (= (pair_left_identity key) 72) (= (pair_left_identity key) 73) (= (pair_left_identity key) 74) (= (pair_left_identity key) 75) (= (pair_left_identity key) 76) (= (pair_left_identity key) 77) (= (pair_left_identity key) 78) (= (pair_left_identity key) 79)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4) (= (pair_right_identity key) 5) (= (pair_right_identity key) 6) (= (pair_right_identity key) 7) (= (pair_right_identity key) 8) (= (pair_right_identity key) 9) (= (pair_right_identity key) 10) (= (pair_right_identity key) 11) (= (pair_right_identity key) 12) (= (pair_right_identity key) 13) (= (pair_right_identity key) 14) (= (pair_right_identity key) 15) (= (pair_right_identity key) 16) (= (pair_right_identity key) 17) (= (pair_right_identity key) 18) (= (pair_right_identity key) 19) (= (pair_right_identity key) 20) (= (pair_right_identity key) 21) (= (pair_right_identity key) 22) (= (pair_right_identity key) 23) (= (pair_right_identity key) 24) (= (pair_right_identity key) 25) (= (pair_right_identity key) 26) (= (pair_right_identity key) 27) (= (pair_right_identity key) 28) (= (pair_right_identity key) 29) (= (pair_right_identity key) 30) (= (pair_right_identity key) 31) (= (pair_right_identity key) 32) (= (pair_right_identity key) 33) (= (pair_right_identity key) 34) (= (pair_right_identity key) 35) (= (pair_right_identity key) 36) (= (pair_right_identity key) 37) (= (pair_right_identity key) 38) (= (pair_right_identity key) 39) (= (pair_right_identity key) 40) (= (pair_right_identity key) 41) (= (pair_right_identity key) 42) (= (pair_right_identity key) 43) (= (pair_right_identity key) 44) (= (pair_right_identity key) 45) (= (pair_right_identity key) 46) (= (pair_right_identity key) 47) (= (pair_right_identity key) 48) (= (pair_right_identity key) 49) (= (pair_right_identity key) 50) (= (pair_right_identity key) 51) (= (pair_right_identity key) 52) (= (pair_right_identity key) 53) (= (pair_right_identity key) 54) (= (pair_right_identity key) 55) (= (pair_right_identity key) 56) (= (pair_right_identity key) 57) (= (pair_right_identity key) 58) (= (pair_right_identity key) 59) (= (pair_right_identity key) 60) (= (pair_right_identity key) 61) (= (pair_right_identity key) 62) (= (pair_right_identity key) 63) (= (pair_right_identity key) 64) (= (pair_right_identity key) 65) (= (pair_right_identity key) 66) (= (pair_right_identity key) 67) (= (pair_right_identity key) 68) (= (pair_right_identity key) 69) (= (pair_right_identity key) 70) (= (pair_right_identity key) 71) (= (pair_right_identity key) 72) (= (pair_right_identity key) 73) (= (pair_right_identity key) 74) (= (pair_right_identity key) 75) (= (pair_right_identity key) 76) (= (pair_right_identity key) 77) (= (pair_right_identity key) 78) (= (pair_right_identity key) 79)) 0 1)) (and (= (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4) (= (pair_left_identity key) 5) (= (pair_left_identity key) 6) (= (pair_left_identity key) 7) (= (pair_left_identity key) 8) (= (pair_left_identity key) 9) (= (pair_left_identity key) 10) (= (pair_left_identity key) 11) (= (pair_left_identity key) 12) (= (pair_left_identity key) 13) (= (pair_left_identity key) 14) (= (pair_left_identity key) 15) (= (pair_left_identity key) 16) (= (pair_left_identity key) 17) (= (pair_left_identity key) 18) (= (pair_left_identity key) 19) (= (pair_left_identity key) 20) (= (pair_left_identity key) 21) (= (pair_left_identity key) 22) (= (pair_left_identity key) 23) (= (pair_left_identity key) 24) (= (pair_left_identity key) 25) (= (pair_left_identity key) 26) (= (pair_left_identity key) 27) (= (pair_left_identity key) 28) (= (pair_left_identity key) 29) (= (pair_left_identity key) 30) (= (pair_left_identity key) 31) (= (pair_left_identity key) 32) (= (pair_left_identity key) 33) (= (pair_left_identity key) 34) (= (pair_left_identity key) 35) (= (pair_left_identity key) 36) (= (pair_left_identity key) 37) (= (pair_left_identity key) 38) (= (pair_left_identity key) 39) (= (pair_left_identity key) 40) (= (pair_left_identity key) 41) (= (pair_left_identity key) 42) (= (pair_left_identity key) 43) (= (pair_left_identity key) 44) (= (pair_left_identity key) 45) (= (pair_left_identity key) 46) (= (pair_left_identity key) 47) (= (pair_left_identity key) 48) (= (pair_left_identity key) 49) (= (pair_left_identity key) 50) (= (pair_left_identity key) 51) (= (pair_left_identity key) 52) (= (pair_left_identity key) 53) (= (pair_left_identity key) 54) (= (pair_left_identity key) 55) (= (pair_left_identity key) 56) (= (pair_left_identity key) 57) (= (pair_left_identity key) 58) (= (pair_left_identity key) 59) (= (pair_left_identity key) 60) (= (pair_left_identity key) 61) (= (pair_left_identity key) 62) (= (pair_left_identity key) 63) (= (pair_left_identity key) 64) (= (pair_left_identity key) 65) (= (pair_left_identity key) 66) (= (pair_left_identity key) 67) (= (pair_left_identity key) 68) (= (pair_left_identity key) 69) (= (pair_left_identity key) 70) (= (pair_left_identity key) 71) (= (pair_left_identity key) 72) (= (pair_left_identity key) 73) (= (pair_left_identity key) 74) (= (pair_left_identity key) 75) (= (pair_left_identity key) 76) (= (pair_left_identity key) 77) (= (pair_left_identity key) 78) (= (pair_left_identity key) 79)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4) (= (pair_right_identity key) 5) (= (pair_right_identity key) 6) (= (pair_right_identity key) 7) (= (pair_right_identity key) 8) (= (pair_right_identity key) 9) (= (pair_right_identity key) 10) (= (pair_right_identity key) 11) (= (pair_right_identity key) 12) (= (pair_right_identity key) 13) (= (pair_right_identity key) 14) (= (pair_right_identity key) 15) (= (pair_right_identity key) 16) (= (pair_right_identity key) 17) (= (pair_right_identity key) 18) (= (pair_right_identity key) 19) (= (pair_right_identity key) 20) (= (pair_right_identity key) 21) (= (pair_right_identity key) 22) (= (pair_right_identity key) 23) (= (pair_right_identity key) 24) (= (pair_right_identity key) 25) (= (pair_right_identity key) 26) (= (pair_right_identity key) 27) (= (pair_right_identity key) 28) (= (pair_right_identity key) 29) (= (pair_right_identity key) 30) (= (pair_right_identity key) 31) (= (pair_right_identity key) 32) (= (pair_right_identity key) 33) (= (pair_right_identity key) 34) (= (pair_right_identity key) 35) (= (pair_right_identity key) 36) (= (pair_right_identity key) 37) (= (pair_right_identity key) 38) (= (pair_right_identity key) 39) (= (pair_right_identity key) 40) (= (pair_right_identity key) 41) (= (pair_right_identity key) 42) (= (pair_right_identity key) 43) (= (pair_right_identity key) 44) (= (pair_right_identity key) 45) (= (pair_right_identity key) 46) (= (pair_right_identity key) 47) (= (pair_right_identity key) 48) (= (pair_right_identity key) 49) (= (pair_right_identity key) 50) (= (pair_right_identity key) 51) (= (pair_right_identity key) 52) (= (pair_right_identity key) 53) (= (pair_right_identity key) 54) (= (pair_right_identity key) 55) (= (pair_right_identity key) 56) (= (pair_right_identity key) 57) (= (pair_right_identity key) 58) (= (pair_right_identity key) 59) (= (pair_right_identity key) 60) (= (pair_right_identity key) 61) (= (pair_right_identity key) 62) (= (pair_right_identity key) 63) (= (pair_right_identity key) 64) (= (pair_right_identity key) 65) (= (pair_right_identity key) 66) (= (pair_right_identity key) 67) (= (pair_right_identity key) 68) (= (pair_right_identity key) 69) (= (pair_right_identity key) 70) (= (pair_right_identity key) 71) (= (pair_right_identity key) 72) (= (pair_right_identity key) 73) (= (pair_right_identity key) 74) (= (pair_right_identity key) 75) (= (pair_right_identity key) 76) (= (pair_right_identity key) 77) (= (pair_right_identity key) 78) (= (pair_right_identity key) 79)) 0 1)) (< (ite (= (pair_left_identity key) 0) 0 (ite (= (pair_left_identity key) 1) 1 (ite (= (pair_left_identity key) 2) 2 (ite (= (pair_left_identity key) 3) 3 (ite (= (pair_left_identity key) 4) 4 (ite (= (pair_left_identity key) 5) 5 (ite (= (pair_left_identity key) 6) 0 (ite (= (pair_left_identity key) 7) 1 (ite (= (pair_left_identity key) 8) 2 (ite (= (pair_left_identity key) 9) 3 (ite (= (pair_left_identity key) 10) 4 (ite (= (pair_left_identity key) 11) 5 (ite (= (pair_left_identity key) 12) 0 (ite (= (pair_left_identity key) 13) 1 (ite (= (pair_left_identity key) 14) 2 (ite (= (pair_left_identity key) 15) 3 (ite (= (pair_left_identity key) 16) 4 (ite (= (pair_left_identity key) 17) 5 (ite (= (pair_left_identity key) 18) 0 (ite (= (pair_left_identity key) 19) 1 (ite (= (pair_left_identity key) 20) 2 (ite (= (pair_left_identity key) 21) 3 (ite (= (pair_left_identity key) 22) 4 (ite (= (pair_left_identity key) 23) 5 (ite (= (pair_left_identity key) 24) 0 (ite (= (pair_left_identity key) 25) 1 (ite (= (pair_left_identity key) 26) 2 (ite (= (pair_left_identity key) 27) 3 (ite (= (pair_left_identity key) 28) 4 (ite (= (pair_left_identity key) 29) 5 (ite (= (pair_left_identity key) 30) 0 (ite (= (pair_left_identity key) 31) 1 (ite (= (pair_left_identity key) 32) 2 (ite (= (pair_left_identity key) 33) 3 (ite (= (pair_left_identity key) 34) 4 (ite (= (pair_left_identity key) 35) 5 (ite (= (pair_left_identity key) 36) 0 (ite (= (pair_left_identity key) 37) 1 (ite (= (pair_left_identity key) 38) 2 (ite (= (pair_left_identity key) 39) 3 (ite (= (pair_left_identity key) 40) 4 (ite (= (pair_left_identity key) 41) 5 (ite (= (pair_left_identity key) 42) 0 (ite (= (pair_left_identity key) 43) 1 (ite (= (pair_left_identity key) 44) 2 (ite (= (pair_left_identity key) 45) 3 (ite (= (pair_left_identity key) 46) 4 (ite (= (pair_left_identity key) 47) 5 (ite (= (pair_left_identity key) 48) 0 (ite (= (pair_left_identity key) 49) 1 (ite (= (pair_left_identity key) 50) 2 (ite (= (pair_left_identity key) 51) 3 (ite (= (pair_left_identity key) 52) 4 (ite (= (pair_left_identity key) 53) 5 (ite (= (pair_left_identity key) 54) 0 (ite (= (pair_left_identity key) 55) 1 (ite (= (pair_left_identity key) 56) 2 (ite (= (pair_left_identity key) 57) 3 (ite (= (pair_left_identity key) 58) 4 (ite (= (pair_left_identity key) 59) 5 (ite (= (pair_left_identity key) 60) 0 (ite (= (pair_left_identity key) 61) 1 (ite (= (pair_left_identity key) 62) 2 (ite (= (pair_left_identity key) 63) 3 (ite (= (pair_left_identity key) 64) 4 (ite (= (pair_left_identity key) 65) 5 (ite (= (pair_left_identity key) 66) 0 (ite (= (pair_left_identity key) 67) 1 (ite (= (pair_left_identity key) 68) 2 (ite (= (pair_left_identity key) 69) 3 (ite (= (pair_left_identity key) 70) 4 (ite (= (pair_left_identity key) 71) 5 (ite (= (pair_left_identity key) 72) 0 (ite (= (pair_left_identity key) 73) 1 (ite (= (pair_left_identity key) 74) 2 (ite (= (pair_left_identity key) 75) 3 (ite (= (pair_left_identity key) 76) 4 (ite (= (pair_left_identity key) 77) 5 (ite (= (pair_left_identity key) 78) 0 (ite (= (pair_left_identity key) 79) 1 (pair_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (pair_right_identity key) 0) 0 (ite (= (pair_right_identity key) 1) 1 (ite (= (pair_right_identity key) 2) 2 (ite (= (pair_right_identity key) 3) 3 (ite (= (pair_right_identity key) 4) 4 (ite (= (pair_right_identity key) 5) 5 (ite (= (pair_right_identity key) 6) 0 (ite (= (pair_right_identity key) 7) 1 (ite (= (pair_right_identity key) 8) 2 (ite (= (pair_right_identity key) 9) 3 (ite (= (pair_right_identity key) 10) 4 (ite (= (pair_right_identity key) 11) 5 (ite (= (pair_right_identity key) 12) 0 (ite (= (pair_right_identity key) 13) 1 (ite (= (pair_right_identity key) 14) 2 (ite (= (pair_right_identity key) 15) 3 (ite (= (pair_right_identity key) 16) 4 (ite (= (pair_right_identity key) 17) 5 (ite (= (pair_right_identity key) 18) 0 (ite (= (pair_right_identity key) 19) 1 (ite (= (pair_right_identity key) 20) 2 (ite (= (pair_right_identity key) 21) 3 (ite (= (pair_right_identity key) 22) 4 (ite (= (pair_right_identity key) 23) 5 (ite (= (pair_right_identity key) 24) 0 (ite (= (pair_right_identity key) 25) 1 (ite (= (pair_right_identity key) 26) 2 (ite (= (pair_right_identity key) 27) 3 (ite (= (pair_right_identity key) 28) 4 (ite (= (pair_right_identity key) 29) 5 (ite (= (pair_right_identity key) 30) 0 (ite (= (pair_right_identity key) 31) 1 (ite (= (pair_right_identity key) 32) 2 (ite (= (pair_right_identity key) 33) 3 (ite (= (pair_right_identity key) 34) 4 (ite (= (pair_right_identity key) 35) 5 (ite (= (pair_right_identity key) 36) 0 (ite (= (pair_right_identity key) 37) 1 (ite (= (pair_right_identity key) 38) 2 (ite (= (pair_right_identity key) 39) 3 (ite (= (pair_right_identity key) 40) 4 (ite (= (pair_right_identity key) 41) 5 (ite (= (pair_right_identity key) 42) 0 (ite (= (pair_right_identity key) 43) 1 (ite (= (pair_right_identity key) 44) 2 (ite (= (pair_right_identity key) 45) 3 (ite (= (pair_right_identity key) 46) 4 (ite (= (pair_right_identity key) 47) 5 (ite (= (pair_right_identity key) 48) 0 (ite (= (pair_right_identity key) 49) 1 (ite (= (pair_right_identity key) 50) 2 (ite (= (pair_right_identity key) 51) 3 (ite (= (pair_right_identity key) 52) 4 (ite (= (pair_right_identity key) 53) 5 (ite (= (pair_right_identity key) 54) 0 (ite (= (pair_right_identity key) 55) 1 (ite (= (pair_right_identity key) 56) 2 (ite (= (pair_right_identity key) 57) 3 (ite (= (pair_right_identity key) 58) 4 (ite (= (pair_right_identity key) 59) 5 (ite (= (pair_right_identity key) 60) 0 (ite (= (pair_right_identity key) 61) 1 (ite (= (pair_right_identity key) 62) 2 (ite (= (pair_right_identity key) 63) 3 (ite (= (pair_right_identity key) 64) 4 (ite (= (pair_right_identity key) 65) 5 (ite (= (pair_right_identity key) 66) 0 (ite (= (pair_right_identity key) 67) 1 (ite (= (pair_right_identity key) 68) 2 (ite (= (pair_right_identity key) 69) 3 (ite (= (pair_right_identity key) 70) 4 (ite (= (pair_right_identity key) 71) 5 (ite (= (pair_right_identity key) 72) 0 (ite (= (pair_right_identity key) 73) 1 (ite (= (pair_right_identity key) 74) 2 (ite (= (pair_right_identity key) 75) 3 (ite (= (pair_right_identity key) 76) 4 (ite (= (pair_right_identity key) 77) 5 (ite (= (pair_right_identity key) 78) 0 (ite (= (pair_right_identity key) 79) 1 (pair_right_identity key)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) -1 (ite (and (= (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4) (= (pair_left_identity key) 5) (= (pair_left_identity key) 6) (= (pair_left_identity key) 7) (= (pair_left_identity key) 8) (= (pair_left_identity key) 9) (= (pair_left_identity key) 10) (= (pair_left_identity key) 11) (= (pair_left_identity key) 12) (= (pair_left_identity key) 13) (= (pair_left_identity key) 14) (= (pair_left_identity key) 15) (= (pair_left_identity key) 16) (= (pair_left_identity key) 17) (= (pair_left_identity key) 18) (= (pair_left_identity key) 19) (= (pair_left_identity key) 20) (= (pair_left_identity key) 21) (= (pair_left_identity key) 22) (= (pair_left_identity key) 23) (= (pair_left_identity key) 24) (= (pair_left_identity key) 25) (= (pair_left_identity key) 26) (= (pair_left_identity key) 27) (= (pair_left_identity key) 28) (= (pair_left_identity key) 29) (= (pair_left_identity key) 30) (= (pair_left_identity key) 31) (= (pair_left_identity key) 32) (= (pair_left_identity key) 33) (= (pair_left_identity key) 34) (= (pair_left_identity key) 35) (= (pair_left_identity key) 36) (= (pair_left_identity key) 37) (= (pair_left_identity key) 38) (= (pair_left_identity key) 39) (= (pair_left_identity key) 40) (= (pair_left_identity key) 41) (= (pair_left_identity key) 42) (= (pair_left_identity key) 43) (= (pair_left_identity key) 44) (= (pair_left_identity key) 45) (= (pair_left_identity key) 46) (= (pair_left_identity key) 47) (= (pair_left_identity key) 48) (= (pair_left_identity key) 49) (= (pair_left_identity key) 50) (= (pair_left_identity key) 51) (= (pair_left_identity key) 52) (= (pair_left_identity key) 53) (= (pair_left_identity key) 54) (= (pair_left_identity key) 55) (= (pair_left_identity key) 56) (= (pair_left_identity key) 57) (= (pair_left_identity key) 58) (= (pair_left_identity key) 59) (= (pair_left_identity key) 60) (= (pair_left_identity key) 61) (= (pair_left_identity key) 62) (= (pair_left_identity key) 63) (= (pair_left_identity key) 64) (= (pair_left_identity key) 65) (= (pair_left_identity key) 66) (= (pair_left_identity key) 67) (= (pair_left_identity key) 68) (= (pair_left_identity key) 69) (= (pair_left_identity key) 70) (= (pair_left_identity key) 71) (= (pair_left_identity key) 72) (= (pair_left_identity key) 73) (= (pair_left_identity key) 74) (= (pair_left_identity key) 75) (= (pair_left_identity key) 76) (= (pair_left_identity key) 77) (= (pair_left_identity key) 78) (= (pair_left_identity key) 79)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4) (= (pair_right_identity key) 5) (= (pair_right_identity key) 6) (= (pair_right_identity key) 7) (= (pair_right_identity key) 8) (= (pair_right_identity key) 9) (= (pair_right_identity key) 10) (= (pair_right_identity key) 11) (= (pair_right_identity key) 12) (= (pair_right_identity key) 13) (= (pair_right_identity key) 14) (= (pair_right_identity key) 15) (= (pair_right_identity key) 16) (= (pair_right_identity key) 17) (= (pair_right_identity key) 18) (= (pair_right_identity key) 19) (= (pair_right_identity key) 20) (= (pair_right_identity key) 21) (= (pair_right_identity key) 22) (= (pair_right_identity key) 23) (= (pair_right_identity key) 24) (= (pair_right_identity key) 25) (= (pair_right_identity key) 26) (= (pair_right_identity key) 27) (= (pair_right_identity key) 28) (= (pair_right_identity key) 29) (= (pair_right_identity key) 30) (= (pair_right_identity key) 31) (= (pair_right_identity key) 32) (= (pair_right_identity key) 33) (= (pair_right_identity key) 34) (= (pair_right_identity key) 35) (= (pair_right_identity key) 36) (= (pair_right_identity key) 37) (= (pair_right_identity key) 38) (= (pair_right_identity key) 39) (= (pair_right_identity key) 40) (= (pair_right_identity key) 41) (= (pair_right_identity key) 42) (= (pair_right_identity key) 43) (= (pair_right_identity key) 44) (= (pair_right_identity key) 45) (= (pair_right_identity key) 46) (= (pair_right_identity key) 47) (= (pair_right_identity key) 48) (= (pair_right_identity key) 49) (= (pair_right_identity key) 50) (= (pair_right_identity key) 51) (= (pair_right_identity key) 52) (= (pair_right_identity key) 53) (= (pair_right_identity key) 54) (= (pair_right_identity key) 55) (= (pair_right_identity key) 56) (= (pair_right_identity key) 57) (= (pair_right_identity key) 58) (= (pair_right_identity key) 59) (= (pair_right_identity key) 60) (= (pair_right_identity key) 61) (= (pair_right_identity key) 62) (= (pair_right_identity key) 63) (= (pair_right_identity key) 64) (= (pair_right_identity key) 65) (= (pair_right_identity key) 66) (= (pair_right_identity key) 67) (= (pair_right_identity key) 68) (= (pair_right_identity key) 69) (= (pair_right_identity key) 70) (= (pair_right_identity key) 71) (= (pair_right_identity key) 72) (= (pair_right_identity key) 73) (= (pair_right_identity key) 74) (= (pair_right_identity key) 75) (= (pair_right_identity key) 76) (= (pair_right_identity key) 77) (= (pair_right_identity key) 78) (= (pair_right_identity key) 79)) 0 1)) (= (ite (= (pair_left_identity key) 0) 0 (ite (= (pair_left_identity key) 1) 1 (ite (= (pair_left_identity key) 2) 2 (ite (= (pair_left_identity key) 3) 3 (ite (= (pair_left_identity key) 4) 4 (ite (= (pair_left_identity key) 5) 5 (ite (= (pair_left_identity key) 6) 0 (ite (= (pair_left_identity key) 7) 1 (ite (= (pair_left_identity key) 8) 2 (ite (= (pair_left_identity key) 9) 3 (ite (= (pair_left_identity key) 10) 4 (ite (= (pair_left_identity key) 11) 5 (ite (= (pair_left_identity key) 12) 0 (ite (= (pair_left_identity key) 13) 1 (ite (= (pair_left_identity key) 14) 2 (ite (= (pair_left_identity key) 15) 3 (ite (= (pair_left_identity key) 16) 4 (ite (= (pair_left_identity key) 17) 5 (ite (= (pair_left_identity key) 18) 0 (ite (= (pair_left_identity key) 19) 1 (ite (= (pair_left_identity key) 20) 2 (ite (= (pair_left_identity key) 21) 3 (ite (= (pair_left_identity key) 22) 4 (ite (= (pair_left_identity key) 23) 5 (ite (= (pair_left_identity key) 24) 0 (ite (= (pair_left_identity key) 25) 1 (ite (= (pair_left_identity key) 26) 2 (ite (= (pair_left_identity key) 27) 3 (ite (= (pair_left_identity key) 28) 4 (ite (= (pair_left_identity key) 29) 5 (ite (= (pair_left_identity key) 30) 0 (ite (= (pair_left_identity key) 31) 1 (ite (= (pair_left_identity key) 32) 2 (ite (= (pair_left_identity key) 33) 3 (ite (= (pair_left_identity key) 34) 4 (ite (= (pair_left_identity key) 35) 5 (ite (= (pair_left_identity key) 36) 0 (ite (= (pair_left_identity key) 37) 1 (ite (= (pair_left_identity key) 38) 2 (ite (= (pair_left_identity key) 39) 3 (ite (= (pair_left_identity key) 40) 4 (ite (= (pair_left_identity key) 41) 5 (ite (= (pair_left_identity key) 42) 0 (ite (= (pair_left_identity key) 43) 1 (ite (= (pair_left_identity key) 44) 2 (ite (= (pair_left_identity key) 45) 3 (ite (= (pair_left_identity key) 46) 4 (ite (= (pair_left_identity key) 47) 5 (ite (= (pair_left_identity key) 48) 0 (ite (= (pair_left_identity key) 49) 1 (ite (= (pair_left_identity key) 50) 2 (ite (= (pair_left_identity key) 51) 3 (ite (= (pair_left_identity key) 52) 4 (ite (= (pair_left_identity key) 53) 5 (ite (= (pair_left_identity key) 54) 0 (ite (= (pair_left_identity key) 55) 1 (ite (= (pair_left_identity key) 56) 2 (ite (= (pair_left_identity key) 57) 3 (ite (= (pair_left_identity key) 58) 4 (ite (= (pair_left_identity key) 59) 5 (ite (= (pair_left_identity key) 60) 0 (ite (= (pair_left_identity key) 61) 1 (ite (= (pair_left_identity key) 62) 2 (ite (= (pair_left_identity key) 63) 3 (ite (= (pair_left_identity key) 64) 4 (ite (= (pair_left_identity key) 65) 5 (ite (= (pair_left_identity key) 66) 0 (ite (= (pair_left_identity key) 67) 1 (ite (= (pair_left_identity key) 68) 2 (ite (= (pair_left_identity key) 69) 3 (ite (= (pair_left_identity key) 70) 4 (ite (= (pair_left_identity key) 71) 5 (ite (= (pair_left_identity key) 72) 0 (ite (= (pair_left_identity key) 73) 1 (ite (= (pair_left_identity key) 74) 2 (ite (= (pair_left_identity key) 75) 3 (ite (= (pair_left_identity key) 76) 4 (ite (= (pair_left_identity key) 77) 5 (ite (= (pair_left_identity key) 78) 0 (ite (= (pair_left_identity key) 79) 1 (pair_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (pair_right_identity key) 0) 0 (ite (= (pair_right_identity key) 1) 1 (ite (= (pair_right_identity key) 2) 2 (ite (= (pair_right_identity key) 3) 3 (ite (= (pair_right_identity key) 4) 4 (ite (= (pair_right_identity key) 5) 5 (ite (= (pair_right_identity key) 6) 0 (ite (= (pair_right_identity key) 7) 1 (ite (= (pair_right_identity key) 8) 2 (ite (= (pair_right_identity key) 9) 3 (ite (= (pair_right_identity key) 10) 4 (ite (= (pair_right_identity key) 11) 5 (ite (= (pair_right_identity key) 12) 0 (ite (= (pair_right_identity key) 13) 1 (ite (= (pair_right_identity key) 14) 2 (ite (= (pair_right_identity key) 15) 3 (ite (= (pair_right_identity key) 16) 4 (ite (= (pair_right_identity key) 17) 5 (ite (= (pair_right_identity key) 18) 0 (ite (= (pair_right_identity key) 19) 1 (ite (= (pair_right_identity key) 20) 2 (ite (= (pair_right_identity key) 21) 3 (ite (= (pair_right_identity key) 22) 4 (ite (= (pair_right_identity key) 23) 5 (ite (= (pair_right_identity key) 24) 0 (ite (= (pair_right_identity key) 25) 1 (ite (= (pair_right_identity key) 26) 2 (ite (= (pair_right_identity key) 27) 3 (ite (= (pair_right_identity key) 28) 4 (ite (= (pair_right_identity key) 29) 5 (ite (= (pair_right_identity key) 30) 0 (ite (= (pair_right_identity key) 31) 1 (ite (= (pair_right_identity key) 32) 2 (ite (= (pair_right_identity key) 33) 3 (ite (= (pair_right_identity key) 34) 4 (ite (= (pair_right_identity key) 35) 5 (ite (= (pair_right_identity key) 36) 0 (ite (= (pair_right_identity key) 37) 1 (ite (= (pair_right_identity key) 38) 2 (ite (= (pair_right_identity key) 39) 3 (ite (= (pair_right_identity key) 40) 4 (ite (= (pair_right_identity key) 41) 5 (ite (= (pair_right_identity key) 42) 0 (ite (= (pair_right_identity key) 43) 1 (ite (= (pair_right_identity key) 44) 2 (ite (= (pair_right_identity key) 45) 3 (ite (= (pair_right_identity key) 46) 4 (ite (= (pair_right_identity key) 47) 5 (ite (= (pair_right_identity key) 48) 0 (ite (= (pair_right_identity key) 49) 1 (ite (= (pair_right_identity key) 50) 2 (ite (= (pair_right_identity key) 51) 3 (ite (= (pair_right_identity key) 52) 4 (ite (= (pair_right_identity key) 53) 5 (ite (= (pair_right_identity key) 54) 0 (ite (= (pair_right_identity key) 55) 1 (ite (= (pair_right_identity key) 56) 2 (ite (= (pair_right_identity key) 57) 3 (ite (= (pair_right_identity key) 58) 4 (ite (= (pair_right_identity key) 59) 5 (ite (= (pair_right_identity key) 60) 0 (ite (= (pair_right_identity key) 61) 1 (ite (= (pair_right_identity key) 62) 2 (ite (= (pair_right_identity key) 63) 3 (ite (= (pair_right_identity key) 64) 4 (ite (= (pair_right_identity key) 65) 5 (ite (= (pair_right_identity key) 66) 0 (ite (= (pair_right_identity key) 67) 1 (ite (= (pair_right_identity key) 68) 2 (ite (= (pair_right_identity key) 69) 3 (ite (= (pair_right_identity key) 70) 4 (ite (= (pair_right_identity key) 71) 5 (ite (= (pair_right_identity key) 72) 0 (ite (= (pair_right_identity key) 73) 1 (ite (= (pair_right_identity key) 74) 2 (ite (= (pair_right_identity key) 75) 3 (ite (= (pair_right_identity key) 76) 4 (ite (= (pair_right_identity key) 77) 5 (ite (= (pair_right_identity key) 78) 0 (ite (= (pair_right_identity key) 79) 1 (pair_right_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 0 1)))
    (lambda ((key CallKey)) (ite (or (< (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4) (= (call_left_identity key) 5) (= (call_left_identity key) 6) (= (call_left_identity key) 7) (= (call_left_identity key) 8) (= (call_left_identity key) 9) (= (call_left_identity key) 10) (= (call_left_identity key) 11) (= (call_left_identity key) 12) (= (call_left_identity key) 13) (= (call_left_identity key) 14) (= (call_left_identity key) 15) (= (call_left_identity key) 16) (= (call_left_identity key) 17) (= (call_left_identity key) 18) (= (call_left_identity key) 19) (= (call_left_identity key) 20) (= (call_left_identity key) 21) (= (call_left_identity key) 22) (= (call_left_identity key) 23) (= (call_left_identity key) 24) (= (call_left_identity key) 25) (= (call_left_identity key) 26) (= (call_left_identity key) 27) (= (call_left_identity key) 28) (= (call_left_identity key) 29) (= (call_left_identity key) 30) (= (call_left_identity key) 31) (= (call_left_identity key) 32) (= (call_left_identity key) 33) (= (call_left_identity key) 34) (= (call_left_identity key) 35) (= (call_left_identity key) 36) (= (call_left_identity key) 37) (= (call_left_identity key) 38) (= (call_left_identity key) 39) (= (call_left_identity key) 40) (= (call_left_identity key) 41) (= (call_left_identity key) 42) (= (call_left_identity key) 43) (= (call_left_identity key) 44) (= (call_left_identity key) 45) (= (call_left_identity key) 46) (= (call_left_identity key) 47) (= (call_left_identity key) 48) (= (call_left_identity key) 49) (= (call_left_identity key) 50) (= (call_left_identity key) 51) (= (call_left_identity key) 52) (= (call_left_identity key) 53) (= (call_left_identity key) 54) (= (call_left_identity key) 55) (= (call_left_identity key) 56) (= (call_left_identity key) 57) (= (call_left_identity key) 58) (= (call_left_identity key) 59) (= (call_left_identity key) 60) (= (call_left_identity key) 61) (= (call_left_identity key) 62) (= (call_left_identity key) 63) (= (call_left_identity key) 64) (= (call_left_identity key) 65) (= (call_left_identity key) 66) (= (call_left_identity key) 67) (= (call_left_identity key) 68) (= (call_left_identity key) 69) (= (call_left_identity key) 70) (= (call_left_identity key) 71) (= (call_left_identity key) 72) (= (call_left_identity key) 73) (= (call_left_identity key) 74) (= (call_left_identity key) 75) (= (call_left_identity key) 76) (= (call_left_identity key) 77) (= (call_left_identity key) 78) (= (call_left_identity key) 79)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4) (= (call_right_identity key) 5) (= (call_right_identity key) 6) (= (call_right_identity key) 7) (= (call_right_identity key) 8) (= (call_right_identity key) 9) (= (call_right_identity key) 10) (= (call_right_identity key) 11) (= (call_right_identity key) 12) (= (call_right_identity key) 13) (= (call_right_identity key) 14) (= (call_right_identity key) 15) (= (call_right_identity key) 16) (= (call_right_identity key) 17) (= (call_right_identity key) 18) (= (call_right_identity key) 19) (= (call_right_identity key) 20) (= (call_right_identity key) 21) (= (call_right_identity key) 22) (= (call_right_identity key) 23) (= (call_right_identity key) 24) (= (call_right_identity key) 25) (= (call_right_identity key) 26) (= (call_right_identity key) 27) (= (call_right_identity key) 28) (= (call_right_identity key) 29) (= (call_right_identity key) 30) (= (call_right_identity key) 31) (= (call_right_identity key) 32) (= (call_right_identity key) 33) (= (call_right_identity key) 34) (= (call_right_identity key) 35) (= (call_right_identity key) 36) (= (call_right_identity key) 37) (= (call_right_identity key) 38) (= (call_right_identity key) 39) (= (call_right_identity key) 40) (= (call_right_identity key) 41) (= (call_right_identity key) 42) (= (call_right_identity key) 43) (= (call_right_identity key) 44) (= (call_right_identity key) 45) (= (call_right_identity key) 46) (= (call_right_identity key) 47) (= (call_right_identity key) 48) (= (call_right_identity key) 49) (= (call_right_identity key) 50) (= (call_right_identity key) 51) (= (call_right_identity key) 52) (= (call_right_identity key) 53) (= (call_right_identity key) 54) (= (call_right_identity key) 55) (= (call_right_identity key) 56) (= (call_right_identity key) 57) (= (call_right_identity key) 58) (= (call_right_identity key) 59) (= (call_right_identity key) 60) (= (call_right_identity key) 61) (= (call_right_identity key) 62) (= (call_right_identity key) 63) (= (call_right_identity key) 64) (= (call_right_identity key) 65) (= (call_right_identity key) 66) (= (call_right_identity key) 67) (= (call_right_identity key) 68) (= (call_right_identity key) 69) (= (call_right_identity key) 70) (= (call_right_identity key) 71) (= (call_right_identity key) 72) (= (call_right_identity key) 73) (= (call_right_identity key) 74) (= (call_right_identity key) 75) (= (call_right_identity key) 76) (= (call_right_identity key) 77) (= (call_right_identity key) 78) (= (call_right_identity key) 79)) 0 1)) (and (= (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4) (= (call_left_identity key) 5) (= (call_left_identity key) 6) (= (call_left_identity key) 7) (= (call_left_identity key) 8) (= (call_left_identity key) 9) (= (call_left_identity key) 10) (= (call_left_identity key) 11) (= (call_left_identity key) 12) (= (call_left_identity key) 13) (= (call_left_identity key) 14) (= (call_left_identity key) 15) (= (call_left_identity key) 16) (= (call_left_identity key) 17) (= (call_left_identity key) 18) (= (call_left_identity key) 19) (= (call_left_identity key) 20) (= (call_left_identity key) 21) (= (call_left_identity key) 22) (= (call_left_identity key) 23) (= (call_left_identity key) 24) (= (call_left_identity key) 25) (= (call_left_identity key) 26) (= (call_left_identity key) 27) (= (call_left_identity key) 28) (= (call_left_identity key) 29) (= (call_left_identity key) 30) (= (call_left_identity key) 31) (= (call_left_identity key) 32) (= (call_left_identity key) 33) (= (call_left_identity key) 34) (= (call_left_identity key) 35) (= (call_left_identity key) 36) (= (call_left_identity key) 37) (= (call_left_identity key) 38) (= (call_left_identity key) 39) (= (call_left_identity key) 40) (= (call_left_identity key) 41) (= (call_left_identity key) 42) (= (call_left_identity key) 43) (= (call_left_identity key) 44) (= (call_left_identity key) 45) (= (call_left_identity key) 46) (= (call_left_identity key) 47) (= (call_left_identity key) 48) (= (call_left_identity key) 49) (= (call_left_identity key) 50) (= (call_left_identity key) 51) (= (call_left_identity key) 52) (= (call_left_identity key) 53) (= (call_left_identity key) 54) (= (call_left_identity key) 55) (= (call_left_identity key) 56) (= (call_left_identity key) 57) (= (call_left_identity key) 58) (= (call_left_identity key) 59) (= (call_left_identity key) 60) (= (call_left_identity key) 61) (= (call_left_identity key) 62) (= (call_left_identity key) 63) (= (call_left_identity key) 64) (= (call_left_identity key) 65) (= (call_left_identity key) 66) (= (call_left_identity key) 67) (= (call_left_identity key) 68) (= (call_left_identity key) 69) (= (call_left_identity key) 70) (= (call_left_identity key) 71) (= (call_left_identity key) 72) (= (call_left_identity key) 73) (= (call_left_identity key) 74) (= (call_left_identity key) 75) (= (call_left_identity key) 76) (= (call_left_identity key) 77) (= (call_left_identity key) 78) (= (call_left_identity key) 79)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4) (= (call_right_identity key) 5) (= (call_right_identity key) 6) (= (call_right_identity key) 7) (= (call_right_identity key) 8) (= (call_right_identity key) 9) (= (call_right_identity key) 10) (= (call_right_identity key) 11) (= (call_right_identity key) 12) (= (call_right_identity key) 13) (= (call_right_identity key) 14) (= (call_right_identity key) 15) (= (call_right_identity key) 16) (= (call_right_identity key) 17) (= (call_right_identity key) 18) (= (call_right_identity key) 19) (= (call_right_identity key) 20) (= (call_right_identity key) 21) (= (call_right_identity key) 22) (= (call_right_identity key) 23) (= (call_right_identity key) 24) (= (call_right_identity key) 25) (= (call_right_identity key) 26) (= (call_right_identity key) 27) (= (call_right_identity key) 28) (= (call_right_identity key) 29) (= (call_right_identity key) 30) (= (call_right_identity key) 31) (= (call_right_identity key) 32) (= (call_right_identity key) 33) (= (call_right_identity key) 34) (= (call_right_identity key) 35) (= (call_right_identity key) 36) (= (call_right_identity key) 37) (= (call_right_identity key) 38) (= (call_right_identity key) 39) (= (call_right_identity key) 40) (= (call_right_identity key) 41) (= (call_right_identity key) 42) (= (call_right_identity key) 43) (= (call_right_identity key) 44) (= (call_right_identity key) 45) (= (call_right_identity key) 46) (= (call_right_identity key) 47) (= (call_right_identity key) 48) (= (call_right_identity key) 49) (= (call_right_identity key) 50) (= (call_right_identity key) 51) (= (call_right_identity key) 52) (= (call_right_identity key) 53) (= (call_right_identity key) 54) (= (call_right_identity key) 55) (= (call_right_identity key) 56) (= (call_right_identity key) 57) (= (call_right_identity key) 58) (= (call_right_identity key) 59) (= (call_right_identity key) 60) (= (call_right_identity key) 61) (= (call_right_identity key) 62) (= (call_right_identity key) 63) (= (call_right_identity key) 64) (= (call_right_identity key) 65) (= (call_right_identity key) 66) (= (call_right_identity key) 67) (= (call_right_identity key) 68) (= (call_right_identity key) 69) (= (call_right_identity key) 70) (= (call_right_identity key) 71) (= (call_right_identity key) 72) (= (call_right_identity key) 73) (= (call_right_identity key) 74) (= (call_right_identity key) 75) (= (call_right_identity key) 76) (= (call_right_identity key) 77) (= (call_right_identity key) 78) (= (call_right_identity key) 79)) 0 1)) (< (ite (= (call_left_identity key) 0) 0 (ite (= (call_left_identity key) 1) 1 (ite (= (call_left_identity key) 2) 2 (ite (= (call_left_identity key) 3) 3 (ite (= (call_left_identity key) 4) 4 (ite (= (call_left_identity key) 5) 5 (ite (= (call_left_identity key) 6) 0 (ite (= (call_left_identity key) 7) 1 (ite (= (call_left_identity key) 8) 2 (ite (= (call_left_identity key) 9) 3 (ite (= (call_left_identity key) 10) 4 (ite (= (call_left_identity key) 11) 5 (ite (= (call_left_identity key) 12) 0 (ite (= (call_left_identity key) 13) 1 (ite (= (call_left_identity key) 14) 2 (ite (= (call_left_identity key) 15) 3 (ite (= (call_left_identity key) 16) 4 (ite (= (call_left_identity key) 17) 5 (ite (= (call_left_identity key) 18) 0 (ite (= (call_left_identity key) 19) 1 (ite (= (call_left_identity key) 20) 2 (ite (= (call_left_identity key) 21) 3 (ite (= (call_left_identity key) 22) 4 (ite (= (call_left_identity key) 23) 5 (ite (= (call_left_identity key) 24) 0 (ite (= (call_left_identity key) 25) 1 (ite (= (call_left_identity key) 26) 2 (ite (= (call_left_identity key) 27) 3 (ite (= (call_left_identity key) 28) 4 (ite (= (call_left_identity key) 29) 5 (ite (= (call_left_identity key) 30) 0 (ite (= (call_left_identity key) 31) 1 (ite (= (call_left_identity key) 32) 2 (ite (= (call_left_identity key) 33) 3 (ite (= (call_left_identity key) 34) 4 (ite (= (call_left_identity key) 35) 5 (ite (= (call_left_identity key) 36) 0 (ite (= (call_left_identity key) 37) 1 (ite (= (call_left_identity key) 38) 2 (ite (= (call_left_identity key) 39) 3 (ite (= (call_left_identity key) 40) 4 (ite (= (call_left_identity key) 41) 5 (ite (= (call_left_identity key) 42) 0 (ite (= (call_left_identity key) 43) 1 (ite (= (call_left_identity key) 44) 2 (ite (= (call_left_identity key) 45) 3 (ite (= (call_left_identity key) 46) 4 (ite (= (call_left_identity key) 47) 5 (ite (= (call_left_identity key) 48) 0 (ite (= (call_left_identity key) 49) 1 (ite (= (call_left_identity key) 50) 2 (ite (= (call_left_identity key) 51) 3 (ite (= (call_left_identity key) 52) 4 (ite (= (call_left_identity key) 53) 5 (ite (= (call_left_identity key) 54) 0 (ite (= (call_left_identity key) 55) 1 (ite (= (call_left_identity key) 56) 2 (ite (= (call_left_identity key) 57) 3 (ite (= (call_left_identity key) 58) 4 (ite (= (call_left_identity key) 59) 5 (ite (= (call_left_identity key) 60) 0 (ite (= (call_left_identity key) 61) 1 (ite (= (call_left_identity key) 62) 2 (ite (= (call_left_identity key) 63) 3 (ite (= (call_left_identity key) 64) 4 (ite (= (call_left_identity key) 65) 5 (ite (= (call_left_identity key) 66) 0 (ite (= (call_left_identity key) 67) 1 (ite (= (call_left_identity key) 68) 2 (ite (= (call_left_identity key) 69) 3 (ite (= (call_left_identity key) 70) 4 (ite (= (call_left_identity key) 71) 5 (ite (= (call_left_identity key) 72) 0 (ite (= (call_left_identity key) 73) 1 (ite (= (call_left_identity key) 74) 2 (ite (= (call_left_identity key) 75) 3 (ite (= (call_left_identity key) 76) 4 (ite (= (call_left_identity key) 77) 5 (ite (= (call_left_identity key) 78) 0 (ite (= (call_left_identity key) 79) 1 (call_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (call_right_identity key) 0) 0 (ite (= (call_right_identity key) 1) 1 (ite (= (call_right_identity key) 2) 2 (ite (= (call_right_identity key) 3) 3 (ite (= (call_right_identity key) 4) 4 (ite (= (call_right_identity key) 5) 5 (ite (= (call_right_identity key) 6) 0 (ite (= (call_right_identity key) 7) 1 (ite (= (call_right_identity key) 8) 2 (ite (= (call_right_identity key) 9) 3 (ite (= (call_right_identity key) 10) 4 (ite (= (call_right_identity key) 11) 5 (ite (= (call_right_identity key) 12) 0 (ite (= (call_right_identity key) 13) 1 (ite (= (call_right_identity key) 14) 2 (ite (= (call_right_identity key) 15) 3 (ite (= (call_right_identity key) 16) 4 (ite (= (call_right_identity key) 17) 5 (ite (= (call_right_identity key) 18) 0 (ite (= (call_right_identity key) 19) 1 (ite (= (call_right_identity key) 20) 2 (ite (= (call_right_identity key) 21) 3 (ite (= (call_right_identity key) 22) 4 (ite (= (call_right_identity key) 23) 5 (ite (= (call_right_identity key) 24) 0 (ite (= (call_right_identity key) 25) 1 (ite (= (call_right_identity key) 26) 2 (ite (= (call_right_identity key) 27) 3 (ite (= (call_right_identity key) 28) 4 (ite (= (call_right_identity key) 29) 5 (ite (= (call_right_identity key) 30) 0 (ite (= (call_right_identity key) 31) 1 (ite (= (call_right_identity key) 32) 2 (ite (= (call_right_identity key) 33) 3 (ite (= (call_right_identity key) 34) 4 (ite (= (call_right_identity key) 35) 5 (ite (= (call_right_identity key) 36) 0 (ite (= (call_right_identity key) 37) 1 (ite (= (call_right_identity key) 38) 2 (ite (= (call_right_identity key) 39) 3 (ite (= (call_right_identity key) 40) 4 (ite (= (call_right_identity key) 41) 5 (ite (= (call_right_identity key) 42) 0 (ite (= (call_right_identity key) 43) 1 (ite (= (call_right_identity key) 44) 2 (ite (= (call_right_identity key) 45) 3 (ite (= (call_right_identity key) 46) 4 (ite (= (call_right_identity key) 47) 5 (ite (= (call_right_identity key) 48) 0 (ite (= (call_right_identity key) 49) 1 (ite (= (call_right_identity key) 50) 2 (ite (= (call_right_identity key) 51) 3 (ite (= (call_right_identity key) 52) 4 (ite (= (call_right_identity key) 53) 5 (ite (= (call_right_identity key) 54) 0 (ite (= (call_right_identity key) 55) 1 (ite (= (call_right_identity key) 56) 2 (ite (= (call_right_identity key) 57) 3 (ite (= (call_right_identity key) 58) 4 (ite (= (call_right_identity key) 59) 5 (ite (= (call_right_identity key) 60) 0 (ite (= (call_right_identity key) 61) 1 (ite (= (call_right_identity key) 62) 2 (ite (= (call_right_identity key) 63) 3 (ite (= (call_right_identity key) 64) 4 (ite (= (call_right_identity key) 65) 5 (ite (= (call_right_identity key) 66) 0 (ite (= (call_right_identity key) 67) 1 (ite (= (call_right_identity key) 68) 2 (ite (= (call_right_identity key) 69) 3 (ite (= (call_right_identity key) 70) 4 (ite (= (call_right_identity key) 71) 5 (ite (= (call_right_identity key) 72) 0 (ite (= (call_right_identity key) 73) 1 (ite (= (call_right_identity key) 74) 2 (ite (= (call_right_identity key) 75) 3 (ite (= (call_right_identity key) 76) 4 (ite (= (call_right_identity key) 77) 5 (ite (= (call_right_identity key) 78) 0 (ite (= (call_right_identity key) 79) 1 (call_right_identity key)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) -1 (ite (and (= (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4) (= (call_left_identity key) 5) (= (call_left_identity key) 6) (= (call_left_identity key) 7) (= (call_left_identity key) 8) (= (call_left_identity key) 9) (= (call_left_identity key) 10) (= (call_left_identity key) 11) (= (call_left_identity key) 12) (= (call_left_identity key) 13) (= (call_left_identity key) 14) (= (call_left_identity key) 15) (= (call_left_identity key) 16) (= (call_left_identity key) 17) (= (call_left_identity key) 18) (= (call_left_identity key) 19) (= (call_left_identity key) 20) (= (call_left_identity key) 21) (= (call_left_identity key) 22) (= (call_left_identity key) 23) (= (call_left_identity key) 24) (= (call_left_identity key) 25) (= (call_left_identity key) 26) (= (call_left_identity key) 27) (= (call_left_identity key) 28) (= (call_left_identity key) 29) (= (call_left_identity key) 30) (= (call_left_identity key) 31) (= (call_left_identity key) 32) (= (call_left_identity key) 33) (= (call_left_identity key) 34) (= (call_left_identity key) 35) (= (call_left_identity key) 36) (= (call_left_identity key) 37) (= (call_left_identity key) 38) (= (call_left_identity key) 39) (= (call_left_identity key) 40) (= (call_left_identity key) 41) (= (call_left_identity key) 42) (= (call_left_identity key) 43) (= (call_left_identity key) 44) (= (call_left_identity key) 45) (= (call_left_identity key) 46) (= (call_left_identity key) 47) (= (call_left_identity key) 48) (= (call_left_identity key) 49) (= (call_left_identity key) 50) (= (call_left_identity key) 51) (= (call_left_identity key) 52) (= (call_left_identity key) 53) (= (call_left_identity key) 54) (= (call_left_identity key) 55) (= (call_left_identity key) 56) (= (call_left_identity key) 57) (= (call_left_identity key) 58) (= (call_left_identity key) 59) (= (call_left_identity key) 60) (= (call_left_identity key) 61) (= (call_left_identity key) 62) (= (call_left_identity key) 63) (= (call_left_identity key) 64) (= (call_left_identity key) 65) (= (call_left_identity key) 66) (= (call_left_identity key) 67) (= (call_left_identity key) 68) (= (call_left_identity key) 69) (= (call_left_identity key) 70) (= (call_left_identity key) 71) (= (call_left_identity key) 72) (= (call_left_identity key) 73) (= (call_left_identity key) 74) (= (call_left_identity key) 75) (= (call_left_identity key) 76) (= (call_left_identity key) 77) (= (call_left_identity key) 78) (= (call_left_identity key) 79)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4) (= (call_right_identity key) 5) (= (call_right_identity key) 6) (= (call_right_identity key) 7) (= (call_right_identity key) 8) (= (call_right_identity key) 9) (= (call_right_identity key) 10) (= (call_right_identity key) 11) (= (call_right_identity key) 12) (= (call_right_identity key) 13) (= (call_right_identity key) 14) (= (call_right_identity key) 15) (= (call_right_identity key) 16) (= (call_right_identity key) 17) (= (call_right_identity key) 18) (= (call_right_identity key) 19) (= (call_right_identity key) 20) (= (call_right_identity key) 21) (= (call_right_identity key) 22) (= (call_right_identity key) 23) (= (call_right_identity key) 24) (= (call_right_identity key) 25) (= (call_right_identity key) 26) (= (call_right_identity key) 27) (= (call_right_identity key) 28) (= (call_right_identity key) 29) (= (call_right_identity key) 30) (= (call_right_identity key) 31) (= (call_right_identity key) 32) (= (call_right_identity key) 33) (= (call_right_identity key) 34) (= (call_right_identity key) 35) (= (call_right_identity key) 36) (= (call_right_identity key) 37) (= (call_right_identity key) 38) (= (call_right_identity key) 39) (= (call_right_identity key) 40) (= (call_right_identity key) 41) (= (call_right_identity key) 42) (= (call_right_identity key) 43) (= (call_right_identity key) 44) (= (call_right_identity key) 45) (= (call_right_identity key) 46) (= (call_right_identity key) 47) (= (call_right_identity key) 48) (= (call_right_identity key) 49) (= (call_right_identity key) 50) (= (call_right_identity key) 51) (= (call_right_identity key) 52) (= (call_right_identity key) 53) (= (call_right_identity key) 54) (= (call_right_identity key) 55) (= (call_right_identity key) 56) (= (call_right_identity key) 57) (= (call_right_identity key) 58) (= (call_right_identity key) 59) (= (call_right_identity key) 60) (= (call_right_identity key) 61) (= (call_right_identity key) 62) (= (call_right_identity key) 63) (= (call_right_identity key) 64) (= (call_right_identity key) 65) (= (call_right_identity key) 66) (= (call_right_identity key) 67) (= (call_right_identity key) 68) (= (call_right_identity key) 69) (= (call_right_identity key) 70) (= (call_right_identity key) 71) (= (call_right_identity key) 72) (= (call_right_identity key) 73) (= (call_right_identity key) 74) (= (call_right_identity key) 75) (= (call_right_identity key) 76) (= (call_right_identity key) 77) (= (call_right_identity key) 78) (= (call_right_identity key) 79)) 0 1)) (= (ite (= (call_left_identity key) 0) 0 (ite (= (call_left_identity key) 1) 1 (ite (= (call_left_identity key) 2) 2 (ite (= (call_left_identity key) 3) 3 (ite (= (call_left_identity key) 4) 4 (ite (= (call_left_identity key) 5) 5 (ite (= (call_left_identity key) 6) 0 (ite (= (call_left_identity key) 7) 1 (ite (= (call_left_identity key) 8) 2 (ite (= (call_left_identity key) 9) 3 (ite (= (call_left_identity key) 10) 4 (ite (= (call_left_identity key) 11) 5 (ite (= (call_left_identity key) 12) 0 (ite (= (call_left_identity key) 13) 1 (ite (= (call_left_identity key) 14) 2 (ite (= (call_left_identity key) 15) 3 (ite (= (call_left_identity key) 16) 4 (ite (= (call_left_identity key) 17) 5 (ite (= (call_left_identity key) 18) 0 (ite (= (call_left_identity key) 19) 1 (ite (= (call_left_identity key) 20) 2 (ite (= (call_left_identity key) 21) 3 (ite (= (call_left_identity key) 22) 4 (ite (= (call_left_identity key) 23) 5 (ite (= (call_left_identity key) 24) 0 (ite (= (call_left_identity key) 25) 1 (ite (= (call_left_identity key) 26) 2 (ite (= (call_left_identity key) 27) 3 (ite (= (call_left_identity key) 28) 4 (ite (= (call_left_identity key) 29) 5 (ite (= (call_left_identity key) 30) 0 (ite (= (call_left_identity key) 31) 1 (ite (= (call_left_identity key) 32) 2 (ite (= (call_left_identity key) 33) 3 (ite (= (call_left_identity key) 34) 4 (ite (= (call_left_identity key) 35) 5 (ite (= (call_left_identity key) 36) 0 (ite (= (call_left_identity key) 37) 1 (ite (= (call_left_identity key) 38) 2 (ite (= (call_left_identity key) 39) 3 (ite (= (call_left_identity key) 40) 4 (ite (= (call_left_identity key) 41) 5 (ite (= (call_left_identity key) 42) 0 (ite (= (call_left_identity key) 43) 1 (ite (= (call_left_identity key) 44) 2 (ite (= (call_left_identity key) 45) 3 (ite (= (call_left_identity key) 46) 4 (ite (= (call_left_identity key) 47) 5 (ite (= (call_left_identity key) 48) 0 (ite (= (call_left_identity key) 49) 1 (ite (= (call_left_identity key) 50) 2 (ite (= (call_left_identity key) 51) 3 (ite (= (call_left_identity key) 52) 4 (ite (= (call_left_identity key) 53) 5 (ite (= (call_left_identity key) 54) 0 (ite (= (call_left_identity key) 55) 1 (ite (= (call_left_identity key) 56) 2 (ite (= (call_left_identity key) 57) 3 (ite (= (call_left_identity key) 58) 4 (ite (= (call_left_identity key) 59) 5 (ite (= (call_left_identity key) 60) 0 (ite (= (call_left_identity key) 61) 1 (ite (= (call_left_identity key) 62) 2 (ite (= (call_left_identity key) 63) 3 (ite (= (call_left_identity key) 64) 4 (ite (= (call_left_identity key) 65) 5 (ite (= (call_left_identity key) 66) 0 (ite (= (call_left_identity key) 67) 1 (ite (= (call_left_identity key) 68) 2 (ite (= (call_left_identity key) 69) 3 (ite (= (call_left_identity key) 70) 4 (ite (= (call_left_identity key) 71) 5 (ite (= (call_left_identity key) 72) 0 (ite (= (call_left_identity key) 73) 1 (ite (= (call_left_identity key) 74) 2 (ite (= (call_left_identity key) 75) 3 (ite (= (call_left_identity key) 76) 4 (ite (= (call_left_identity key) 77) 5 (ite (= (call_left_identity key) 78) 0 (ite (= (call_left_identity key) 79) 1 (call_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (call_right_identity key) 0) 0 (ite (= (call_right_identity key) 1) 1 (ite (= (call_right_identity key) 2) 2 (ite (= (call_right_identity key) 3) 3 (ite (= (call_right_identity key) 4) 4 (ite (= (call_right_identity key) 5) 5 (ite (= (call_right_identity key) 6) 0 (ite (= (call_right_identity key) 7) 1 (ite (= (call_right_identity key) 8) 2 (ite (= (call_right_identity key) 9) 3 (ite (= (call_right_identity key) 10) 4 (ite (= (call_right_identity key) 11) 5 (ite (= (call_right_identity key) 12) 0 (ite (= (call_right_identity key) 13) 1 (ite (= (call_right_identity key) 14) 2 (ite (= (call_right_identity key) 15) 3 (ite (= (call_right_identity key) 16) 4 (ite (= (call_right_identity key) 17) 5 (ite (= (call_right_identity key) 18) 0 (ite (= (call_right_identity key) 19) 1 (ite (= (call_right_identity key) 20) 2 (ite (= (call_right_identity key) 21) 3 (ite (= (call_right_identity key) 22) 4 (ite (= (call_right_identity key) 23) 5 (ite (= (call_right_identity key) 24) 0 (ite (= (call_right_identity key) 25) 1 (ite (= (call_right_identity key) 26) 2 (ite (= (call_right_identity key) 27) 3 (ite (= (call_right_identity key) 28) 4 (ite (= (call_right_identity key) 29) 5 (ite (= (call_right_identity key) 30) 0 (ite (= (call_right_identity key) 31) 1 (ite (= (call_right_identity key) 32) 2 (ite (= (call_right_identity key) 33) 3 (ite (= (call_right_identity key) 34) 4 (ite (= (call_right_identity key) 35) 5 (ite (= (call_right_identity key) 36) 0 (ite (= (call_right_identity key) 37) 1 (ite (= (call_right_identity key) 38) 2 (ite (= (call_right_identity key) 39) 3 (ite (= (call_right_identity key) 40) 4 (ite (= (call_right_identity key) 41) 5 (ite (= (call_right_identity key) 42) 0 (ite (= (call_right_identity key) 43) 1 (ite (= (call_right_identity key) 44) 2 (ite (= (call_right_identity key) 45) 3 (ite (= (call_right_identity key) 46) 4 (ite (= (call_right_identity key) 47) 5 (ite (= (call_right_identity key) 48) 0 (ite (= (call_right_identity key) 49) 1 (ite (= (call_right_identity key) 50) 2 (ite (= (call_right_identity key) 51) 3 (ite (= (call_right_identity key) 52) 4 (ite (= (call_right_identity key) 53) 5 (ite (= (call_right_identity key) 54) 0 (ite (= (call_right_identity key) 55) 1 (ite (= (call_right_identity key) 56) 2 (ite (= (call_right_identity key) 57) 3 (ite (= (call_right_identity key) 58) 4 (ite (= (call_right_identity key) 59) 5 (ite (= (call_right_identity key) 60) 0 (ite (= (call_right_identity key) 61) 1 (ite (= (call_right_identity key) 62) 2 (ite (= (call_right_identity key) 63) 3 (ite (= (call_right_identity key) 64) 4 (ite (= (call_right_identity key) 65) 5 (ite (= (call_right_identity key) 66) 0 (ite (= (call_right_identity key) 67) 1 (ite (= (call_right_identity key) 68) 2 (ite (= (call_right_identity key) 69) 3 (ite (= (call_right_identity key) 70) 4 (ite (= (call_right_identity key) 71) 5 (ite (= (call_right_identity key) 72) 0 (ite (= (call_right_identity key) 73) 1 (ite (= (call_right_identity key) 74) 2 (ite (= (call_right_identity key) 75) 3 (ite (= (call_right_identity key) 76) 4 (ite (= (call_right_identity key) 77) 5 (ite (= (call_right_identity key) 78) 0 (ite (= (call_right_identity key) 79) 1 (call_right_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_13 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_13 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 56) 1 44) 2 42) 3 50) 4 24) 5 31) 6 68) 7 11) 8 66) 9 41) 10 75) 11 8) 12 37) 13 29) 14 1) 15 14) 16 52) 17 59) 18 63) 19 18) 20 47) 21 2) 22 78) 23 74) 24 23) 25 7) 26 10) 27 60) 28 26) 29 15) 30 55) 31 71) 32 25) 33 77) 34 0) 35 3) 36 16) 37 76) 38 28) 39 79) 40 48) 41 13) 42 40) 43 39) 44 20) 45 69) 46 22) 47 54) 48 35) 49 30) 50 21) 51 43) 52 4) 53 46) 54 6) 55 19) 56 9) 57 57) 58 72) 59 73) 60 70) 61 34) 62 58) 63 32) 64 12) 65 67) 66 36) 67 17) 68 64) 69 27) 70 45) 71 61) 72 38) 73 51) 74 62) 75 65) 76 33) 77 5) 78 53) 79 49) 0 false))
(define-fun drop081_13 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_13 () ExactState
  (ExactSort initial081_13 boundary081_13 configuration081_13 80))
(define-fun private_right081_13 () ExactState
  (ExactSort initial081_13 boundary081_13 configuration081_13 80))
(define-fun public_left081_13 () PublicResult081
  (FinishPublic081 private_left081_13 drop081_13))
(define-fun public_right081_13 () PublicResult081
  (FinishPublic081 private_right081_13 drop081_13))
(assert (not (= public_left081_13 public_right081_13)))
; fixed Boundary_T source case=inherited-insertion-copy-on-drop-panic
(define-fun boundary081_14 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) (or (= (call_state key) 2)))))
(define-fun configuration081_14 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_14 () ExactState
  (mkExactState (store (store (store (store ((as const (Array Int Int)) 0) 0 4) 1 1) 2 3) 3 2) 0 false))
(define-fun drop081_14 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_14 () ExactState
  (ExactSort initial081_14 boundary081_14 configuration081_14 4))
(define-fun private_right081_14 () ExactState
  (ExactSort initial081_14 boundary081_14 configuration081_14 4))
(define-fun public_left081_14 () PublicResult081
  (FinishPublic081 private_left081_14 drop081_14))
(define-fun public_right081_14 () PublicResult081
  (FinishPublic081 private_right081_14 drop081_14))
(assert (not (= public_left081_14 public_right081_14)))
; fixed Boundary_T source case=inherited-heapsort-child-selection-panic
(define-fun boundary081_15 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) (or (= (call_state key) 0)))))
(define-fun configuration081_15 () SortConfiguration
  (mkSortConfiguration
    true
    64
    8
    false
    false))
(define-fun initial081_15 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 5) 1 3) 2 23) 3 8) 4 7) 5 12) 6 16) 7 4) 8 17) 9 1) 10 10) 11 20) 12 11) 13 2) 14 15) 15 0) 16 22) 17 21) 18 14) 19 13) 20 24) 21 6) 22 9) 23 19) 24 18) 0 false))
(define-fun drop081_15 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_15 () ExactState
  (ExactSort initial081_15 boundary081_15 configuration081_15 25))
(define-fun private_right081_15 () ExactState
  (ExactSort initial081_15 boundary081_15 configuration081_15 25))
(define-fun public_left081_15 () PublicResult081
  (FinishPublic081 private_left081_15 drop081_15))
(define-fun public_right081_15 () PublicResult081
  (FinishPublic081 private_right081_15 drop081_15))
(assert (not (= public_left081_15 public_right081_15)))
; fixed Boundary_T source case=inherited-general-small-sort-merge-restoration
(define-fun boundary081_16 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) (or (= (call_state key) 102)))))
(define-fun configuration081_16 () SortConfiguration
  (mkSortConfiguration
    false
    64
    24
    true
    true))
(define-fun initial081_16 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 14) 1 10) 2 9) 3 18) 4 22) 5 13) 6 2) 7 19) 8 7) 9 24) 10 8) 11 20) 12 3) 13 6) 14 0) 15 25) 16 16) 17 1) 18 15) 19 21) 20 5) 21 12) 22 11) 23 23) 24 17) 25 4) 0 false))
(define-fun drop081_16 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_16 () ExactState
  (ExactSort initial081_16 boundary081_16 configuration081_16 26))
(define-fun private_right081_16 () ExactState
  (ExactSort initial081_16 boundary081_16 configuration081_16 26))
(define-fun public_left081_16 () PublicResult081
  (FinishPublic081 private_left081_16 drop081_16))
(define-fun public_right081_16 () PublicResult081
  (FinishPublic081 private_right081_16 drop081_16))
(assert (not (= public_left081_16 public_right081_16)))
; fixed Boundary_T source case=inherited-general-small-sort-scratch-unwind-restoration
(define-fun boundary081_17 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) (or (= (call_state key) 15)))))
(define-fun configuration081_17 () SortConfiguration
  (mkSortConfiguration
    false
    64
    24
    true
    true))
(define-fun initial081_17 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 14) 1 10) 2 9) 3 18) 4 22) 5 13) 6 2) 7 19) 8 7) 9 24) 10 8) 11 20) 12 3) 13 6) 14 0) 15 25) 16 16) 17 1) 18 15) 19 21) 20 5) 21 12) 22 11) 23 23) 24 17) 25 4) 0 false))
(define-fun drop081_17 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_17 () ExactState
  (ExactSort initial081_17 boundary081_17 configuration081_17 26))
(define-fun private_right081_17 () ExactState
  (ExactSort initial081_17 boundary081_17 configuration081_17 26))
(define-fun public_left081_17 () PublicResult081
  (FinishPublic081 private_left081_17 drop081_17))
(define-fun public_right081_17 () PublicResult081
  (FinishPublic081 private_right081_17 drop081_17))
(assert (not (= public_left081_17 public_right081_17)))
; fixed Boundary_T source case=inherited-network-small-sort-merge-panic
(define-fun boundary081_18 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) (or (= (call_state key) 92)))))
(define-fun configuration081_18 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    true
    true))
(define-fun initial081_18 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 22) 1 12) 2 14) 3 10) 4 4) 5 1) 6 11) 7 21) 8 19) 9 0) 10 20) 11 8) 12 3) 13 13) 14 25) 15 17) 16 7) 17 9) 18 2) 19 24) 20 18) 21 6) 22 5) 23 23) 24 16) 25 15) 0 false))
(define-fun drop081_18 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_18 () ExactState
  (ExactSort initial081_18 boundary081_18 configuration081_18 26))
(define-fun private_right081_18 () ExactState
  (ExactSort initial081_18 boundary081_18 configuration081_18 26))
(define-fun public_left081_18 () PublicResult081
  (FinishPublic081 private_left081_18 drop081_18))
(define-fun public_right081_18 () PublicResult081
  (FinishPublic081 private_right081_18 drop081_18))
(assert (not (= public_left081_18 public_right081_18)))
; fixed Boundary_T source case=inherited-recursive-pivot-panic
(define-fun boundary081_19 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) (or (= (call_state key) 2)))))
(define-fun configuration081_19 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_19 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 74) 1 30) 2 59) 3 32) 4 15) 5 70) 6 78) 7 76) 8 20) 9 28) 10 37) 11 72) 12 41) 13 67) 14 13) 15 31) 16 0) 17 16) 18 54) 19 63) 20 19) 21 17) 22 10) 23 21) 24 49) 25 39) 26 4) 27 2) 28 79) 29 29) 30 57) 31 25) 32 47) 33 3) 34 36) 35 77) 36 34) 37 55) 38 23) 39 5) 40 40) 41 35) 42 66) 43 71) 44 43) 45 68) 46 46) 47 27) 48 52) 49 69) 50 7) 51 8) 52 22) 53 48) 54 51) 55 14) 56 11) 57 12) 58 9) 59 62) 60 45) 61 56) 62 42) 63 18) 64 1) 65 64) 66 24) 67 73) 68 65) 69 38) 70 26) 71 58) 72 75) 73 33) 74 44) 75 50) 76 60) 77 53) 78 61) 79 6) 0 false))
(define-fun drop081_19 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_19 () ExactState
  (ExactSort initial081_19 boundary081_19 configuration081_19 80))
(define-fun private_right081_19 () ExactState
  (ExactSort initial081_19 boundary081_19 configuration081_19 80))
(define-fun public_left081_19 () PublicResult081
  (FinishPublic081 private_left081_19 drop081_19))
(define-fun public_right081_19 () PublicResult081
  (FinishPublic081 private_right081_19 drop081_19))
(assert (not (= public_left081_19 public_right081_19)))
; fixed Boundary_T source case=inherited-ancestor-pivot-panic
(define-fun boundary081_20 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (or (< (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4) (= (pair_left_identity key) 5) (= (pair_left_identity key) 6) (= (pair_left_identity key) 7) (= (pair_left_identity key) 8) (= (pair_left_identity key) 9) (= (pair_left_identity key) 10) (= (pair_left_identity key) 11) (= (pair_left_identity key) 12) (= (pair_left_identity key) 13) (= (pair_left_identity key) 14) (= (pair_left_identity key) 15) (= (pair_left_identity key) 16) (= (pair_left_identity key) 17) (= (pair_left_identity key) 18) (= (pair_left_identity key) 19) (= (pair_left_identity key) 20) (= (pair_left_identity key) 21) (= (pair_left_identity key) 22) (= (pair_left_identity key) 23) (= (pair_left_identity key) 24) (= (pair_left_identity key) 25) (= (pair_left_identity key) 26) (= (pair_left_identity key) 27) (= (pair_left_identity key) 28) (= (pair_left_identity key) 29) (= (pair_left_identity key) 30) (= (pair_left_identity key) 31) (= (pair_left_identity key) 32) (= (pair_left_identity key) 33) (= (pair_left_identity key) 34) (= (pair_left_identity key) 35) (= (pair_left_identity key) 36) (= (pair_left_identity key) 37) (= (pair_left_identity key) 38) (= (pair_left_identity key) 39) (= (pair_left_identity key) 40) (= (pair_left_identity key) 41) (= (pair_left_identity key) 42) (= (pair_left_identity key) 43) (= (pair_left_identity key) 44) (= (pair_left_identity key) 45) (= (pair_left_identity key) 46) (= (pair_left_identity key) 47) (= (pair_left_identity key) 48) (= (pair_left_identity key) 49) (= (pair_left_identity key) 50) (= (pair_left_identity key) 51) (= (pair_left_identity key) 52) (= (pair_left_identity key) 53) (= (pair_left_identity key) 54) (= (pair_left_identity key) 55) (= (pair_left_identity key) 56) (= (pair_left_identity key) 57) (= (pair_left_identity key) 58) (= (pair_left_identity key) 59) (= (pair_left_identity key) 60) (= (pair_left_identity key) 61) (= (pair_left_identity key) 62) (= (pair_left_identity key) 63) (= (pair_left_identity key) 64) (= (pair_left_identity key) 65) (= (pair_left_identity key) 66) (= (pair_left_identity key) 67) (= (pair_left_identity key) 68) (= (pair_left_identity key) 69) (= (pair_left_identity key) 70) (= (pair_left_identity key) 71) (= (pair_left_identity key) 72) (= (pair_left_identity key) 73) (= (pair_left_identity key) 74) (= (pair_left_identity key) 75) (= (pair_left_identity key) 76) (= (pair_left_identity key) 77) (= (pair_left_identity key) 78) (= (pair_left_identity key) 79)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4) (= (pair_right_identity key) 5) (= (pair_right_identity key) 6) (= (pair_right_identity key) 7) (= (pair_right_identity key) 8) (= (pair_right_identity key) 9) (= (pair_right_identity key) 10) (= (pair_right_identity key) 11) (= (pair_right_identity key) 12) (= (pair_right_identity key) 13) (= (pair_right_identity key) 14) (= (pair_right_identity key) 15) (= (pair_right_identity key) 16) (= (pair_right_identity key) 17) (= (pair_right_identity key) 18) (= (pair_right_identity key) 19) (= (pair_right_identity key) 20) (= (pair_right_identity key) 21) (= (pair_right_identity key) 22) (= (pair_right_identity key) 23) (= (pair_right_identity key) 24) (= (pair_right_identity key) 25) (= (pair_right_identity key) 26) (= (pair_right_identity key) 27) (= (pair_right_identity key) 28) (= (pair_right_identity key) 29) (= (pair_right_identity key) 30) (= (pair_right_identity key) 31) (= (pair_right_identity key) 32) (= (pair_right_identity key) 33) (= (pair_right_identity key) 34) (= (pair_right_identity key) 35) (= (pair_right_identity key) 36) (= (pair_right_identity key) 37) (= (pair_right_identity key) 38) (= (pair_right_identity key) 39) (= (pair_right_identity key) 40) (= (pair_right_identity key) 41) (= (pair_right_identity key) 42) (= (pair_right_identity key) 43) (= (pair_right_identity key) 44) (= (pair_right_identity key) 45) (= (pair_right_identity key) 46) (= (pair_right_identity key) 47) (= (pair_right_identity key) 48) (= (pair_right_identity key) 49) (= (pair_right_identity key) 50) (= (pair_right_identity key) 51) (= (pair_right_identity key) 52) (= (pair_right_identity key) 53) (= (pair_right_identity key) 54) (= (pair_right_identity key) 55) (= (pair_right_identity key) 56) (= (pair_right_identity key) 57) (= (pair_right_identity key) 58) (= (pair_right_identity key) 59) (= (pair_right_identity key) 60) (= (pair_right_identity key) 61) (= (pair_right_identity key) 62) (= (pair_right_identity key) 63) (= (pair_right_identity key) 64) (= (pair_right_identity key) 65) (= (pair_right_identity key) 66) (= (pair_right_identity key) 67) (= (pair_right_identity key) 68) (= (pair_right_identity key) 69) (= (pair_right_identity key) 70) (= (pair_right_identity key) 71) (= (pair_right_identity key) 72) (= (pair_right_identity key) 73) (= (pair_right_identity key) 74) (= (pair_right_identity key) 75) (= (pair_right_identity key) 76) (= (pair_right_identity key) 77) (= (pair_right_identity key) 78) (= (pair_right_identity key) 79)) 0 1)) (and (= (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4) (= (pair_left_identity key) 5) (= (pair_left_identity key) 6) (= (pair_left_identity key) 7) (= (pair_left_identity key) 8) (= (pair_left_identity key) 9) (= (pair_left_identity key) 10) (= (pair_left_identity key) 11) (= (pair_left_identity key) 12) (= (pair_left_identity key) 13) (= (pair_left_identity key) 14) (= (pair_left_identity key) 15) (= (pair_left_identity key) 16) (= (pair_left_identity key) 17) (= (pair_left_identity key) 18) (= (pair_left_identity key) 19) (= (pair_left_identity key) 20) (= (pair_left_identity key) 21) (= (pair_left_identity key) 22) (= (pair_left_identity key) 23) (= (pair_left_identity key) 24) (= (pair_left_identity key) 25) (= (pair_left_identity key) 26) (= (pair_left_identity key) 27) (= (pair_left_identity key) 28) (= (pair_left_identity key) 29) (= (pair_left_identity key) 30) (= (pair_left_identity key) 31) (= (pair_left_identity key) 32) (= (pair_left_identity key) 33) (= (pair_left_identity key) 34) (= (pair_left_identity key) 35) (= (pair_left_identity key) 36) (= (pair_left_identity key) 37) (= (pair_left_identity key) 38) (= (pair_left_identity key) 39) (= (pair_left_identity key) 40) (= (pair_left_identity key) 41) (= (pair_left_identity key) 42) (= (pair_left_identity key) 43) (= (pair_left_identity key) 44) (= (pair_left_identity key) 45) (= (pair_left_identity key) 46) (= (pair_left_identity key) 47) (= (pair_left_identity key) 48) (= (pair_left_identity key) 49) (= (pair_left_identity key) 50) (= (pair_left_identity key) 51) (= (pair_left_identity key) 52) (= (pair_left_identity key) 53) (= (pair_left_identity key) 54) (= (pair_left_identity key) 55) (= (pair_left_identity key) 56) (= (pair_left_identity key) 57) (= (pair_left_identity key) 58) (= (pair_left_identity key) 59) (= (pair_left_identity key) 60) (= (pair_left_identity key) 61) (= (pair_left_identity key) 62) (= (pair_left_identity key) 63) (= (pair_left_identity key) 64) (= (pair_left_identity key) 65) (= (pair_left_identity key) 66) (= (pair_left_identity key) 67) (= (pair_left_identity key) 68) (= (pair_left_identity key) 69) (= (pair_left_identity key) 70) (= (pair_left_identity key) 71) (= (pair_left_identity key) 72) (= (pair_left_identity key) 73) (= (pair_left_identity key) 74) (= (pair_left_identity key) 75) (= (pair_left_identity key) 76) (= (pair_left_identity key) 77) (= (pair_left_identity key) 78) (= (pair_left_identity key) 79)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4) (= (pair_right_identity key) 5) (= (pair_right_identity key) 6) (= (pair_right_identity key) 7) (= (pair_right_identity key) 8) (= (pair_right_identity key) 9) (= (pair_right_identity key) 10) (= (pair_right_identity key) 11) (= (pair_right_identity key) 12) (= (pair_right_identity key) 13) (= (pair_right_identity key) 14) (= (pair_right_identity key) 15) (= (pair_right_identity key) 16) (= (pair_right_identity key) 17) (= (pair_right_identity key) 18) (= (pair_right_identity key) 19) (= (pair_right_identity key) 20) (= (pair_right_identity key) 21) (= (pair_right_identity key) 22) (= (pair_right_identity key) 23) (= (pair_right_identity key) 24) (= (pair_right_identity key) 25) (= (pair_right_identity key) 26) (= (pair_right_identity key) 27) (= (pair_right_identity key) 28) (= (pair_right_identity key) 29) (= (pair_right_identity key) 30) (= (pair_right_identity key) 31) (= (pair_right_identity key) 32) (= (pair_right_identity key) 33) (= (pair_right_identity key) 34) (= (pair_right_identity key) 35) (= (pair_right_identity key) 36) (= (pair_right_identity key) 37) (= (pair_right_identity key) 38) (= (pair_right_identity key) 39) (= (pair_right_identity key) 40) (= (pair_right_identity key) 41) (= (pair_right_identity key) 42) (= (pair_right_identity key) 43) (= (pair_right_identity key) 44) (= (pair_right_identity key) 45) (= (pair_right_identity key) 46) (= (pair_right_identity key) 47) (= (pair_right_identity key) 48) (= (pair_right_identity key) 49) (= (pair_right_identity key) 50) (= (pair_right_identity key) 51) (= (pair_right_identity key) 52) (= (pair_right_identity key) 53) (= (pair_right_identity key) 54) (= (pair_right_identity key) 55) (= (pair_right_identity key) 56) (= (pair_right_identity key) 57) (= (pair_right_identity key) 58) (= (pair_right_identity key) 59) (= (pair_right_identity key) 60) (= (pair_right_identity key) 61) (= (pair_right_identity key) 62) (= (pair_right_identity key) 63) (= (pair_right_identity key) 64) (= (pair_right_identity key) 65) (= (pair_right_identity key) 66) (= (pair_right_identity key) 67) (= (pair_right_identity key) 68) (= (pair_right_identity key) 69) (= (pair_right_identity key) 70) (= (pair_right_identity key) 71) (= (pair_right_identity key) 72) (= (pair_right_identity key) 73) (= (pair_right_identity key) 74) (= (pair_right_identity key) 75) (= (pair_right_identity key) 76) (= (pair_right_identity key) 77) (= (pair_right_identity key) 78) (= (pair_right_identity key) 79)) 0 1)) (< (ite (= (pair_left_identity key) 0) 0 (ite (= (pair_left_identity key) 1) 1 (ite (= (pair_left_identity key) 2) 2 (ite (= (pair_left_identity key) 3) 3 (ite (= (pair_left_identity key) 4) 4 (ite (= (pair_left_identity key) 5) 5 (ite (= (pair_left_identity key) 6) 0 (ite (= (pair_left_identity key) 7) 1 (ite (= (pair_left_identity key) 8) 2 (ite (= (pair_left_identity key) 9) 3 (ite (= (pair_left_identity key) 10) 4 (ite (= (pair_left_identity key) 11) 5 (ite (= (pair_left_identity key) 12) 0 (ite (= (pair_left_identity key) 13) 1 (ite (= (pair_left_identity key) 14) 2 (ite (= (pair_left_identity key) 15) 3 (ite (= (pair_left_identity key) 16) 4 (ite (= (pair_left_identity key) 17) 5 (ite (= (pair_left_identity key) 18) 0 (ite (= (pair_left_identity key) 19) 1 (ite (= (pair_left_identity key) 20) 2 (ite (= (pair_left_identity key) 21) 3 (ite (= (pair_left_identity key) 22) 4 (ite (= (pair_left_identity key) 23) 5 (ite (= (pair_left_identity key) 24) 0 (ite (= (pair_left_identity key) 25) 1 (ite (= (pair_left_identity key) 26) 2 (ite (= (pair_left_identity key) 27) 3 (ite (= (pair_left_identity key) 28) 4 (ite (= (pair_left_identity key) 29) 5 (ite (= (pair_left_identity key) 30) 0 (ite (= (pair_left_identity key) 31) 1 (ite (= (pair_left_identity key) 32) 2 (ite (= (pair_left_identity key) 33) 3 (ite (= (pair_left_identity key) 34) 4 (ite (= (pair_left_identity key) 35) 5 (ite (= (pair_left_identity key) 36) 0 (ite (= (pair_left_identity key) 37) 1 (ite (= (pair_left_identity key) 38) 2 (ite (= (pair_left_identity key) 39) 3 (ite (= (pair_left_identity key) 40) 4 (ite (= (pair_left_identity key) 41) 5 (ite (= (pair_left_identity key) 42) 0 (ite (= (pair_left_identity key) 43) 1 (ite (= (pair_left_identity key) 44) 2 (ite (= (pair_left_identity key) 45) 3 (ite (= (pair_left_identity key) 46) 4 (ite (= (pair_left_identity key) 47) 5 (ite (= (pair_left_identity key) 48) 0 (ite (= (pair_left_identity key) 49) 1 (ite (= (pair_left_identity key) 50) 2 (ite (= (pair_left_identity key) 51) 3 (ite (= (pair_left_identity key) 52) 4 (ite (= (pair_left_identity key) 53) 5 (ite (= (pair_left_identity key) 54) 0 (ite (= (pair_left_identity key) 55) 1 (ite (= (pair_left_identity key) 56) 2 (ite (= (pair_left_identity key) 57) 3 (ite (= (pair_left_identity key) 58) 4 (ite (= (pair_left_identity key) 59) 5 (ite (= (pair_left_identity key) 60) 0 (ite (= (pair_left_identity key) 61) 1 (ite (= (pair_left_identity key) 62) 2 (ite (= (pair_left_identity key) 63) 3 (ite (= (pair_left_identity key) 64) 4 (ite (= (pair_left_identity key) 65) 5 (ite (= (pair_left_identity key) 66) 0 (ite (= (pair_left_identity key) 67) 1 (ite (= (pair_left_identity key) 68) 2 (ite (= (pair_left_identity key) 69) 3 (ite (= (pair_left_identity key) 70) 4 (ite (= (pair_left_identity key) 71) 5 (ite (= (pair_left_identity key) 72) 0 (ite (= (pair_left_identity key) 73) 1 (ite (= (pair_left_identity key) 74) 2 (ite (= (pair_left_identity key) 75) 3 (ite (= (pair_left_identity key) 76) 4 (ite (= (pair_left_identity key) 77) 5 (ite (= (pair_left_identity key) 78) 0 (ite (= (pair_left_identity key) 79) 1 (pair_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (pair_right_identity key) 0) 0 (ite (= (pair_right_identity key) 1) 1 (ite (= (pair_right_identity key) 2) 2 (ite (= (pair_right_identity key) 3) 3 (ite (= (pair_right_identity key) 4) 4 (ite (= (pair_right_identity key) 5) 5 (ite (= (pair_right_identity key) 6) 0 (ite (= (pair_right_identity key) 7) 1 (ite (= (pair_right_identity key) 8) 2 (ite (= (pair_right_identity key) 9) 3 (ite (= (pair_right_identity key) 10) 4 (ite (= (pair_right_identity key) 11) 5 (ite (= (pair_right_identity key) 12) 0 (ite (= (pair_right_identity key) 13) 1 (ite (= (pair_right_identity key) 14) 2 (ite (= (pair_right_identity key) 15) 3 (ite (= (pair_right_identity key) 16) 4 (ite (= (pair_right_identity key) 17) 5 (ite (= (pair_right_identity key) 18) 0 (ite (= (pair_right_identity key) 19) 1 (ite (= (pair_right_identity key) 20) 2 (ite (= (pair_right_identity key) 21) 3 (ite (= (pair_right_identity key) 22) 4 (ite (= (pair_right_identity key) 23) 5 (ite (= (pair_right_identity key) 24) 0 (ite (= (pair_right_identity key) 25) 1 (ite (= (pair_right_identity key) 26) 2 (ite (= (pair_right_identity key) 27) 3 (ite (= (pair_right_identity key) 28) 4 (ite (= (pair_right_identity key) 29) 5 (ite (= (pair_right_identity key) 30) 0 (ite (= (pair_right_identity key) 31) 1 (ite (= (pair_right_identity key) 32) 2 (ite (= (pair_right_identity key) 33) 3 (ite (= (pair_right_identity key) 34) 4 (ite (= (pair_right_identity key) 35) 5 (ite (= (pair_right_identity key) 36) 0 (ite (= (pair_right_identity key) 37) 1 (ite (= (pair_right_identity key) 38) 2 (ite (= (pair_right_identity key) 39) 3 (ite (= (pair_right_identity key) 40) 4 (ite (= (pair_right_identity key) 41) 5 (ite (= (pair_right_identity key) 42) 0 (ite (= (pair_right_identity key) 43) 1 (ite (= (pair_right_identity key) 44) 2 (ite (= (pair_right_identity key) 45) 3 (ite (= (pair_right_identity key) 46) 4 (ite (= (pair_right_identity key) 47) 5 (ite (= (pair_right_identity key) 48) 0 (ite (= (pair_right_identity key) 49) 1 (ite (= (pair_right_identity key) 50) 2 (ite (= (pair_right_identity key) 51) 3 (ite (= (pair_right_identity key) 52) 4 (ite (= (pair_right_identity key) 53) 5 (ite (= (pair_right_identity key) 54) 0 (ite (= (pair_right_identity key) 55) 1 (ite (= (pair_right_identity key) 56) 2 (ite (= (pair_right_identity key) 57) 3 (ite (= (pair_right_identity key) 58) 4 (ite (= (pair_right_identity key) 59) 5 (ite (= (pair_right_identity key) 60) 0 (ite (= (pair_right_identity key) 61) 1 (ite (= (pair_right_identity key) 62) 2 (ite (= (pair_right_identity key) 63) 3 (ite (= (pair_right_identity key) 64) 4 (ite (= (pair_right_identity key) 65) 5 (ite (= (pair_right_identity key) 66) 0 (ite (= (pair_right_identity key) 67) 1 (ite (= (pair_right_identity key) 68) 2 (ite (= (pair_right_identity key) 69) 3 (ite (= (pair_right_identity key) 70) 4 (ite (= (pair_right_identity key) 71) 5 (ite (= (pair_right_identity key) 72) 0 (ite (= (pair_right_identity key) 73) 1 (ite (= (pair_right_identity key) 74) 2 (ite (= (pair_right_identity key) 75) 3 (ite (= (pair_right_identity key) 76) 4 (ite (= (pair_right_identity key) 77) 5 (ite (= (pair_right_identity key) 78) 0 (ite (= (pair_right_identity key) 79) 1 (pair_right_identity key)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) -1 (ite (and (= (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4) (= (pair_left_identity key) 5) (= (pair_left_identity key) 6) (= (pair_left_identity key) 7) (= (pair_left_identity key) 8) (= (pair_left_identity key) 9) (= (pair_left_identity key) 10) (= (pair_left_identity key) 11) (= (pair_left_identity key) 12) (= (pair_left_identity key) 13) (= (pair_left_identity key) 14) (= (pair_left_identity key) 15) (= (pair_left_identity key) 16) (= (pair_left_identity key) 17) (= (pair_left_identity key) 18) (= (pair_left_identity key) 19) (= (pair_left_identity key) 20) (= (pair_left_identity key) 21) (= (pair_left_identity key) 22) (= (pair_left_identity key) 23) (= (pair_left_identity key) 24) (= (pair_left_identity key) 25) (= (pair_left_identity key) 26) (= (pair_left_identity key) 27) (= (pair_left_identity key) 28) (= (pair_left_identity key) 29) (= (pair_left_identity key) 30) (= (pair_left_identity key) 31) (= (pair_left_identity key) 32) (= (pair_left_identity key) 33) (= (pair_left_identity key) 34) (= (pair_left_identity key) 35) (= (pair_left_identity key) 36) (= (pair_left_identity key) 37) (= (pair_left_identity key) 38) (= (pair_left_identity key) 39) (= (pair_left_identity key) 40) (= (pair_left_identity key) 41) (= (pair_left_identity key) 42) (= (pair_left_identity key) 43) (= (pair_left_identity key) 44) (= (pair_left_identity key) 45) (= (pair_left_identity key) 46) (= (pair_left_identity key) 47) (= (pair_left_identity key) 48) (= (pair_left_identity key) 49) (= (pair_left_identity key) 50) (= (pair_left_identity key) 51) (= (pair_left_identity key) 52) (= (pair_left_identity key) 53) (= (pair_left_identity key) 54) (= (pair_left_identity key) 55) (= (pair_left_identity key) 56) (= (pair_left_identity key) 57) (= (pair_left_identity key) 58) (= (pair_left_identity key) 59) (= (pair_left_identity key) 60) (= (pair_left_identity key) 61) (= (pair_left_identity key) 62) (= (pair_left_identity key) 63) (= (pair_left_identity key) 64) (= (pair_left_identity key) 65) (= (pair_left_identity key) 66) (= (pair_left_identity key) 67) (= (pair_left_identity key) 68) (= (pair_left_identity key) 69) (= (pair_left_identity key) 70) (= (pair_left_identity key) 71) (= (pair_left_identity key) 72) (= (pair_left_identity key) 73) (= (pair_left_identity key) 74) (= (pair_left_identity key) 75) (= (pair_left_identity key) 76) (= (pair_left_identity key) 77) (= (pair_left_identity key) 78) (= (pair_left_identity key) 79)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4) (= (pair_right_identity key) 5) (= (pair_right_identity key) 6) (= (pair_right_identity key) 7) (= (pair_right_identity key) 8) (= (pair_right_identity key) 9) (= (pair_right_identity key) 10) (= (pair_right_identity key) 11) (= (pair_right_identity key) 12) (= (pair_right_identity key) 13) (= (pair_right_identity key) 14) (= (pair_right_identity key) 15) (= (pair_right_identity key) 16) (= (pair_right_identity key) 17) (= (pair_right_identity key) 18) (= (pair_right_identity key) 19) (= (pair_right_identity key) 20) (= (pair_right_identity key) 21) (= (pair_right_identity key) 22) (= (pair_right_identity key) 23) (= (pair_right_identity key) 24) (= (pair_right_identity key) 25) (= (pair_right_identity key) 26) (= (pair_right_identity key) 27) (= (pair_right_identity key) 28) (= (pair_right_identity key) 29) (= (pair_right_identity key) 30) (= (pair_right_identity key) 31) (= (pair_right_identity key) 32) (= (pair_right_identity key) 33) (= (pair_right_identity key) 34) (= (pair_right_identity key) 35) (= (pair_right_identity key) 36) (= (pair_right_identity key) 37) (= (pair_right_identity key) 38) (= (pair_right_identity key) 39) (= (pair_right_identity key) 40) (= (pair_right_identity key) 41) (= (pair_right_identity key) 42) (= (pair_right_identity key) 43) (= (pair_right_identity key) 44) (= (pair_right_identity key) 45) (= (pair_right_identity key) 46) (= (pair_right_identity key) 47) (= (pair_right_identity key) 48) (= (pair_right_identity key) 49) (= (pair_right_identity key) 50) (= (pair_right_identity key) 51) (= (pair_right_identity key) 52) (= (pair_right_identity key) 53) (= (pair_right_identity key) 54) (= (pair_right_identity key) 55) (= (pair_right_identity key) 56) (= (pair_right_identity key) 57) (= (pair_right_identity key) 58) (= (pair_right_identity key) 59) (= (pair_right_identity key) 60) (= (pair_right_identity key) 61) (= (pair_right_identity key) 62) (= (pair_right_identity key) 63) (= (pair_right_identity key) 64) (= (pair_right_identity key) 65) (= (pair_right_identity key) 66) (= (pair_right_identity key) 67) (= (pair_right_identity key) 68) (= (pair_right_identity key) 69) (= (pair_right_identity key) 70) (= (pair_right_identity key) 71) (= (pair_right_identity key) 72) (= (pair_right_identity key) 73) (= (pair_right_identity key) 74) (= (pair_right_identity key) 75) (= (pair_right_identity key) 76) (= (pair_right_identity key) 77) (= (pair_right_identity key) 78) (= (pair_right_identity key) 79)) 0 1)) (= (ite (= (pair_left_identity key) 0) 0 (ite (= (pair_left_identity key) 1) 1 (ite (= (pair_left_identity key) 2) 2 (ite (= (pair_left_identity key) 3) 3 (ite (= (pair_left_identity key) 4) 4 (ite (= (pair_left_identity key) 5) 5 (ite (= (pair_left_identity key) 6) 0 (ite (= (pair_left_identity key) 7) 1 (ite (= (pair_left_identity key) 8) 2 (ite (= (pair_left_identity key) 9) 3 (ite (= (pair_left_identity key) 10) 4 (ite (= (pair_left_identity key) 11) 5 (ite (= (pair_left_identity key) 12) 0 (ite (= (pair_left_identity key) 13) 1 (ite (= (pair_left_identity key) 14) 2 (ite (= (pair_left_identity key) 15) 3 (ite (= (pair_left_identity key) 16) 4 (ite (= (pair_left_identity key) 17) 5 (ite (= (pair_left_identity key) 18) 0 (ite (= (pair_left_identity key) 19) 1 (ite (= (pair_left_identity key) 20) 2 (ite (= (pair_left_identity key) 21) 3 (ite (= (pair_left_identity key) 22) 4 (ite (= (pair_left_identity key) 23) 5 (ite (= (pair_left_identity key) 24) 0 (ite (= (pair_left_identity key) 25) 1 (ite (= (pair_left_identity key) 26) 2 (ite (= (pair_left_identity key) 27) 3 (ite (= (pair_left_identity key) 28) 4 (ite (= (pair_left_identity key) 29) 5 (ite (= (pair_left_identity key) 30) 0 (ite (= (pair_left_identity key) 31) 1 (ite (= (pair_left_identity key) 32) 2 (ite (= (pair_left_identity key) 33) 3 (ite (= (pair_left_identity key) 34) 4 (ite (= (pair_left_identity key) 35) 5 (ite (= (pair_left_identity key) 36) 0 (ite (= (pair_left_identity key) 37) 1 (ite (= (pair_left_identity key) 38) 2 (ite (= (pair_left_identity key) 39) 3 (ite (= (pair_left_identity key) 40) 4 (ite (= (pair_left_identity key) 41) 5 (ite (= (pair_left_identity key) 42) 0 (ite (= (pair_left_identity key) 43) 1 (ite (= (pair_left_identity key) 44) 2 (ite (= (pair_left_identity key) 45) 3 (ite (= (pair_left_identity key) 46) 4 (ite (= (pair_left_identity key) 47) 5 (ite (= (pair_left_identity key) 48) 0 (ite (= (pair_left_identity key) 49) 1 (ite (= (pair_left_identity key) 50) 2 (ite (= (pair_left_identity key) 51) 3 (ite (= (pair_left_identity key) 52) 4 (ite (= (pair_left_identity key) 53) 5 (ite (= (pair_left_identity key) 54) 0 (ite (= (pair_left_identity key) 55) 1 (ite (= (pair_left_identity key) 56) 2 (ite (= (pair_left_identity key) 57) 3 (ite (= (pair_left_identity key) 58) 4 (ite (= (pair_left_identity key) 59) 5 (ite (= (pair_left_identity key) 60) 0 (ite (= (pair_left_identity key) 61) 1 (ite (= (pair_left_identity key) 62) 2 (ite (= (pair_left_identity key) 63) 3 (ite (= (pair_left_identity key) 64) 4 (ite (= (pair_left_identity key) 65) 5 (ite (= (pair_left_identity key) 66) 0 (ite (= (pair_left_identity key) 67) 1 (ite (= (pair_left_identity key) 68) 2 (ite (= (pair_left_identity key) 69) 3 (ite (= (pair_left_identity key) 70) 4 (ite (= (pair_left_identity key) 71) 5 (ite (= (pair_left_identity key) 72) 0 (ite (= (pair_left_identity key) 73) 1 (ite (= (pair_left_identity key) 74) 2 (ite (= (pair_left_identity key) 75) 3 (ite (= (pair_left_identity key) 76) 4 (ite (= (pair_left_identity key) 77) 5 (ite (= (pair_left_identity key) 78) 0 (ite (= (pair_left_identity key) 79) 1 (pair_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (pair_right_identity key) 0) 0 (ite (= (pair_right_identity key) 1) 1 (ite (= (pair_right_identity key) 2) 2 (ite (= (pair_right_identity key) 3) 3 (ite (= (pair_right_identity key) 4) 4 (ite (= (pair_right_identity key) 5) 5 (ite (= (pair_right_identity key) 6) 0 (ite (= (pair_right_identity key) 7) 1 (ite (= (pair_right_identity key) 8) 2 (ite (= (pair_right_identity key) 9) 3 (ite (= (pair_right_identity key) 10) 4 (ite (= (pair_right_identity key) 11) 5 (ite (= (pair_right_identity key) 12) 0 (ite (= (pair_right_identity key) 13) 1 (ite (= (pair_right_identity key) 14) 2 (ite (= (pair_right_identity key) 15) 3 (ite (= (pair_right_identity key) 16) 4 (ite (= (pair_right_identity key) 17) 5 (ite (= (pair_right_identity key) 18) 0 (ite (= (pair_right_identity key) 19) 1 (ite (= (pair_right_identity key) 20) 2 (ite (= (pair_right_identity key) 21) 3 (ite (= (pair_right_identity key) 22) 4 (ite (= (pair_right_identity key) 23) 5 (ite (= (pair_right_identity key) 24) 0 (ite (= (pair_right_identity key) 25) 1 (ite (= (pair_right_identity key) 26) 2 (ite (= (pair_right_identity key) 27) 3 (ite (= (pair_right_identity key) 28) 4 (ite (= (pair_right_identity key) 29) 5 (ite (= (pair_right_identity key) 30) 0 (ite (= (pair_right_identity key) 31) 1 (ite (= (pair_right_identity key) 32) 2 (ite (= (pair_right_identity key) 33) 3 (ite (= (pair_right_identity key) 34) 4 (ite (= (pair_right_identity key) 35) 5 (ite (= (pair_right_identity key) 36) 0 (ite (= (pair_right_identity key) 37) 1 (ite (= (pair_right_identity key) 38) 2 (ite (= (pair_right_identity key) 39) 3 (ite (= (pair_right_identity key) 40) 4 (ite (= (pair_right_identity key) 41) 5 (ite (= (pair_right_identity key) 42) 0 (ite (= (pair_right_identity key) 43) 1 (ite (= (pair_right_identity key) 44) 2 (ite (= (pair_right_identity key) 45) 3 (ite (= (pair_right_identity key) 46) 4 (ite (= (pair_right_identity key) 47) 5 (ite (= (pair_right_identity key) 48) 0 (ite (= (pair_right_identity key) 49) 1 (ite (= (pair_right_identity key) 50) 2 (ite (= (pair_right_identity key) 51) 3 (ite (= (pair_right_identity key) 52) 4 (ite (= (pair_right_identity key) 53) 5 (ite (= (pair_right_identity key) 54) 0 (ite (= (pair_right_identity key) 55) 1 (ite (= (pair_right_identity key) 56) 2 (ite (= (pair_right_identity key) 57) 3 (ite (= (pair_right_identity key) 58) 4 (ite (= (pair_right_identity key) 59) 5 (ite (= (pair_right_identity key) 60) 0 (ite (= (pair_right_identity key) 61) 1 (ite (= (pair_right_identity key) 62) 2 (ite (= (pair_right_identity key) 63) 3 (ite (= (pair_right_identity key) 64) 4 (ite (= (pair_right_identity key) 65) 5 (ite (= (pair_right_identity key) 66) 0 (ite (= (pair_right_identity key) 67) 1 (ite (= (pair_right_identity key) 68) 2 (ite (= (pair_right_identity key) 69) 3 (ite (= (pair_right_identity key) 70) 4 (ite (= (pair_right_identity key) 71) 5 (ite (= (pair_right_identity key) 72) 0 (ite (= (pair_right_identity key) 73) 1 (ite (= (pair_right_identity key) 74) 2 (ite (= (pair_right_identity key) 75) 3 (ite (= (pair_right_identity key) 76) 4 (ite (= (pair_right_identity key) 77) 5 (ite (= (pair_right_identity key) 78) 0 (ite (= (pair_right_identity key) 79) 1 (pair_right_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 0 1)))
    (lambda ((key CallKey)) (ite (or (< (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4) (= (call_left_identity key) 5) (= (call_left_identity key) 6) (= (call_left_identity key) 7) (= (call_left_identity key) 8) (= (call_left_identity key) 9) (= (call_left_identity key) 10) (= (call_left_identity key) 11) (= (call_left_identity key) 12) (= (call_left_identity key) 13) (= (call_left_identity key) 14) (= (call_left_identity key) 15) (= (call_left_identity key) 16) (= (call_left_identity key) 17) (= (call_left_identity key) 18) (= (call_left_identity key) 19) (= (call_left_identity key) 20) (= (call_left_identity key) 21) (= (call_left_identity key) 22) (= (call_left_identity key) 23) (= (call_left_identity key) 24) (= (call_left_identity key) 25) (= (call_left_identity key) 26) (= (call_left_identity key) 27) (= (call_left_identity key) 28) (= (call_left_identity key) 29) (= (call_left_identity key) 30) (= (call_left_identity key) 31) (= (call_left_identity key) 32) (= (call_left_identity key) 33) (= (call_left_identity key) 34) (= (call_left_identity key) 35) (= (call_left_identity key) 36) (= (call_left_identity key) 37) (= (call_left_identity key) 38) (= (call_left_identity key) 39) (= (call_left_identity key) 40) (= (call_left_identity key) 41) (= (call_left_identity key) 42) (= (call_left_identity key) 43) (= (call_left_identity key) 44) (= (call_left_identity key) 45) (= (call_left_identity key) 46) (= (call_left_identity key) 47) (= (call_left_identity key) 48) (= (call_left_identity key) 49) (= (call_left_identity key) 50) (= (call_left_identity key) 51) (= (call_left_identity key) 52) (= (call_left_identity key) 53) (= (call_left_identity key) 54) (= (call_left_identity key) 55) (= (call_left_identity key) 56) (= (call_left_identity key) 57) (= (call_left_identity key) 58) (= (call_left_identity key) 59) (= (call_left_identity key) 60) (= (call_left_identity key) 61) (= (call_left_identity key) 62) (= (call_left_identity key) 63) (= (call_left_identity key) 64) (= (call_left_identity key) 65) (= (call_left_identity key) 66) (= (call_left_identity key) 67) (= (call_left_identity key) 68) (= (call_left_identity key) 69) (= (call_left_identity key) 70) (= (call_left_identity key) 71) (= (call_left_identity key) 72) (= (call_left_identity key) 73) (= (call_left_identity key) 74) (= (call_left_identity key) 75) (= (call_left_identity key) 76) (= (call_left_identity key) 77) (= (call_left_identity key) 78) (= (call_left_identity key) 79)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4) (= (call_right_identity key) 5) (= (call_right_identity key) 6) (= (call_right_identity key) 7) (= (call_right_identity key) 8) (= (call_right_identity key) 9) (= (call_right_identity key) 10) (= (call_right_identity key) 11) (= (call_right_identity key) 12) (= (call_right_identity key) 13) (= (call_right_identity key) 14) (= (call_right_identity key) 15) (= (call_right_identity key) 16) (= (call_right_identity key) 17) (= (call_right_identity key) 18) (= (call_right_identity key) 19) (= (call_right_identity key) 20) (= (call_right_identity key) 21) (= (call_right_identity key) 22) (= (call_right_identity key) 23) (= (call_right_identity key) 24) (= (call_right_identity key) 25) (= (call_right_identity key) 26) (= (call_right_identity key) 27) (= (call_right_identity key) 28) (= (call_right_identity key) 29) (= (call_right_identity key) 30) (= (call_right_identity key) 31) (= (call_right_identity key) 32) (= (call_right_identity key) 33) (= (call_right_identity key) 34) (= (call_right_identity key) 35) (= (call_right_identity key) 36) (= (call_right_identity key) 37) (= (call_right_identity key) 38) (= (call_right_identity key) 39) (= (call_right_identity key) 40) (= (call_right_identity key) 41) (= (call_right_identity key) 42) (= (call_right_identity key) 43) (= (call_right_identity key) 44) (= (call_right_identity key) 45) (= (call_right_identity key) 46) (= (call_right_identity key) 47) (= (call_right_identity key) 48) (= (call_right_identity key) 49) (= (call_right_identity key) 50) (= (call_right_identity key) 51) (= (call_right_identity key) 52) (= (call_right_identity key) 53) (= (call_right_identity key) 54) (= (call_right_identity key) 55) (= (call_right_identity key) 56) (= (call_right_identity key) 57) (= (call_right_identity key) 58) (= (call_right_identity key) 59) (= (call_right_identity key) 60) (= (call_right_identity key) 61) (= (call_right_identity key) 62) (= (call_right_identity key) 63) (= (call_right_identity key) 64) (= (call_right_identity key) 65) (= (call_right_identity key) 66) (= (call_right_identity key) 67) (= (call_right_identity key) 68) (= (call_right_identity key) 69) (= (call_right_identity key) 70) (= (call_right_identity key) 71) (= (call_right_identity key) 72) (= (call_right_identity key) 73) (= (call_right_identity key) 74) (= (call_right_identity key) 75) (= (call_right_identity key) 76) (= (call_right_identity key) 77) (= (call_right_identity key) 78) (= (call_right_identity key) 79)) 0 1)) (and (= (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4) (= (call_left_identity key) 5) (= (call_left_identity key) 6) (= (call_left_identity key) 7) (= (call_left_identity key) 8) (= (call_left_identity key) 9) (= (call_left_identity key) 10) (= (call_left_identity key) 11) (= (call_left_identity key) 12) (= (call_left_identity key) 13) (= (call_left_identity key) 14) (= (call_left_identity key) 15) (= (call_left_identity key) 16) (= (call_left_identity key) 17) (= (call_left_identity key) 18) (= (call_left_identity key) 19) (= (call_left_identity key) 20) (= (call_left_identity key) 21) (= (call_left_identity key) 22) (= (call_left_identity key) 23) (= (call_left_identity key) 24) (= (call_left_identity key) 25) (= (call_left_identity key) 26) (= (call_left_identity key) 27) (= (call_left_identity key) 28) (= (call_left_identity key) 29) (= (call_left_identity key) 30) (= (call_left_identity key) 31) (= (call_left_identity key) 32) (= (call_left_identity key) 33) (= (call_left_identity key) 34) (= (call_left_identity key) 35) (= (call_left_identity key) 36) (= (call_left_identity key) 37) (= (call_left_identity key) 38) (= (call_left_identity key) 39) (= (call_left_identity key) 40) (= (call_left_identity key) 41) (= (call_left_identity key) 42) (= (call_left_identity key) 43) (= (call_left_identity key) 44) (= (call_left_identity key) 45) (= (call_left_identity key) 46) (= (call_left_identity key) 47) (= (call_left_identity key) 48) (= (call_left_identity key) 49) (= (call_left_identity key) 50) (= (call_left_identity key) 51) (= (call_left_identity key) 52) (= (call_left_identity key) 53) (= (call_left_identity key) 54) (= (call_left_identity key) 55) (= (call_left_identity key) 56) (= (call_left_identity key) 57) (= (call_left_identity key) 58) (= (call_left_identity key) 59) (= (call_left_identity key) 60) (= (call_left_identity key) 61) (= (call_left_identity key) 62) (= (call_left_identity key) 63) (= (call_left_identity key) 64) (= (call_left_identity key) 65) (= (call_left_identity key) 66) (= (call_left_identity key) 67) (= (call_left_identity key) 68) (= (call_left_identity key) 69) (= (call_left_identity key) 70) (= (call_left_identity key) 71) (= (call_left_identity key) 72) (= (call_left_identity key) 73) (= (call_left_identity key) 74) (= (call_left_identity key) 75) (= (call_left_identity key) 76) (= (call_left_identity key) 77) (= (call_left_identity key) 78) (= (call_left_identity key) 79)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4) (= (call_right_identity key) 5) (= (call_right_identity key) 6) (= (call_right_identity key) 7) (= (call_right_identity key) 8) (= (call_right_identity key) 9) (= (call_right_identity key) 10) (= (call_right_identity key) 11) (= (call_right_identity key) 12) (= (call_right_identity key) 13) (= (call_right_identity key) 14) (= (call_right_identity key) 15) (= (call_right_identity key) 16) (= (call_right_identity key) 17) (= (call_right_identity key) 18) (= (call_right_identity key) 19) (= (call_right_identity key) 20) (= (call_right_identity key) 21) (= (call_right_identity key) 22) (= (call_right_identity key) 23) (= (call_right_identity key) 24) (= (call_right_identity key) 25) (= (call_right_identity key) 26) (= (call_right_identity key) 27) (= (call_right_identity key) 28) (= (call_right_identity key) 29) (= (call_right_identity key) 30) (= (call_right_identity key) 31) (= (call_right_identity key) 32) (= (call_right_identity key) 33) (= (call_right_identity key) 34) (= (call_right_identity key) 35) (= (call_right_identity key) 36) (= (call_right_identity key) 37) (= (call_right_identity key) 38) (= (call_right_identity key) 39) (= (call_right_identity key) 40) (= (call_right_identity key) 41) (= (call_right_identity key) 42) (= (call_right_identity key) 43) (= (call_right_identity key) 44) (= (call_right_identity key) 45) (= (call_right_identity key) 46) (= (call_right_identity key) 47) (= (call_right_identity key) 48) (= (call_right_identity key) 49) (= (call_right_identity key) 50) (= (call_right_identity key) 51) (= (call_right_identity key) 52) (= (call_right_identity key) 53) (= (call_right_identity key) 54) (= (call_right_identity key) 55) (= (call_right_identity key) 56) (= (call_right_identity key) 57) (= (call_right_identity key) 58) (= (call_right_identity key) 59) (= (call_right_identity key) 60) (= (call_right_identity key) 61) (= (call_right_identity key) 62) (= (call_right_identity key) 63) (= (call_right_identity key) 64) (= (call_right_identity key) 65) (= (call_right_identity key) 66) (= (call_right_identity key) 67) (= (call_right_identity key) 68) (= (call_right_identity key) 69) (= (call_right_identity key) 70) (= (call_right_identity key) 71) (= (call_right_identity key) 72) (= (call_right_identity key) 73) (= (call_right_identity key) 74) (= (call_right_identity key) 75) (= (call_right_identity key) 76) (= (call_right_identity key) 77) (= (call_right_identity key) 78) (= (call_right_identity key) 79)) 0 1)) (< (ite (= (call_left_identity key) 0) 0 (ite (= (call_left_identity key) 1) 1 (ite (= (call_left_identity key) 2) 2 (ite (= (call_left_identity key) 3) 3 (ite (= (call_left_identity key) 4) 4 (ite (= (call_left_identity key) 5) 5 (ite (= (call_left_identity key) 6) 0 (ite (= (call_left_identity key) 7) 1 (ite (= (call_left_identity key) 8) 2 (ite (= (call_left_identity key) 9) 3 (ite (= (call_left_identity key) 10) 4 (ite (= (call_left_identity key) 11) 5 (ite (= (call_left_identity key) 12) 0 (ite (= (call_left_identity key) 13) 1 (ite (= (call_left_identity key) 14) 2 (ite (= (call_left_identity key) 15) 3 (ite (= (call_left_identity key) 16) 4 (ite (= (call_left_identity key) 17) 5 (ite (= (call_left_identity key) 18) 0 (ite (= (call_left_identity key) 19) 1 (ite (= (call_left_identity key) 20) 2 (ite (= (call_left_identity key) 21) 3 (ite (= (call_left_identity key) 22) 4 (ite (= (call_left_identity key) 23) 5 (ite (= (call_left_identity key) 24) 0 (ite (= (call_left_identity key) 25) 1 (ite (= (call_left_identity key) 26) 2 (ite (= (call_left_identity key) 27) 3 (ite (= (call_left_identity key) 28) 4 (ite (= (call_left_identity key) 29) 5 (ite (= (call_left_identity key) 30) 0 (ite (= (call_left_identity key) 31) 1 (ite (= (call_left_identity key) 32) 2 (ite (= (call_left_identity key) 33) 3 (ite (= (call_left_identity key) 34) 4 (ite (= (call_left_identity key) 35) 5 (ite (= (call_left_identity key) 36) 0 (ite (= (call_left_identity key) 37) 1 (ite (= (call_left_identity key) 38) 2 (ite (= (call_left_identity key) 39) 3 (ite (= (call_left_identity key) 40) 4 (ite (= (call_left_identity key) 41) 5 (ite (= (call_left_identity key) 42) 0 (ite (= (call_left_identity key) 43) 1 (ite (= (call_left_identity key) 44) 2 (ite (= (call_left_identity key) 45) 3 (ite (= (call_left_identity key) 46) 4 (ite (= (call_left_identity key) 47) 5 (ite (= (call_left_identity key) 48) 0 (ite (= (call_left_identity key) 49) 1 (ite (= (call_left_identity key) 50) 2 (ite (= (call_left_identity key) 51) 3 (ite (= (call_left_identity key) 52) 4 (ite (= (call_left_identity key) 53) 5 (ite (= (call_left_identity key) 54) 0 (ite (= (call_left_identity key) 55) 1 (ite (= (call_left_identity key) 56) 2 (ite (= (call_left_identity key) 57) 3 (ite (= (call_left_identity key) 58) 4 (ite (= (call_left_identity key) 59) 5 (ite (= (call_left_identity key) 60) 0 (ite (= (call_left_identity key) 61) 1 (ite (= (call_left_identity key) 62) 2 (ite (= (call_left_identity key) 63) 3 (ite (= (call_left_identity key) 64) 4 (ite (= (call_left_identity key) 65) 5 (ite (= (call_left_identity key) 66) 0 (ite (= (call_left_identity key) 67) 1 (ite (= (call_left_identity key) 68) 2 (ite (= (call_left_identity key) 69) 3 (ite (= (call_left_identity key) 70) 4 (ite (= (call_left_identity key) 71) 5 (ite (= (call_left_identity key) 72) 0 (ite (= (call_left_identity key) 73) 1 (ite (= (call_left_identity key) 74) 2 (ite (= (call_left_identity key) 75) 3 (ite (= (call_left_identity key) 76) 4 (ite (= (call_left_identity key) 77) 5 (ite (= (call_left_identity key) 78) 0 (ite (= (call_left_identity key) 79) 1 (call_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (call_right_identity key) 0) 0 (ite (= (call_right_identity key) 1) 1 (ite (= (call_right_identity key) 2) 2 (ite (= (call_right_identity key) 3) 3 (ite (= (call_right_identity key) 4) 4 (ite (= (call_right_identity key) 5) 5 (ite (= (call_right_identity key) 6) 0 (ite (= (call_right_identity key) 7) 1 (ite (= (call_right_identity key) 8) 2 (ite (= (call_right_identity key) 9) 3 (ite (= (call_right_identity key) 10) 4 (ite (= (call_right_identity key) 11) 5 (ite (= (call_right_identity key) 12) 0 (ite (= (call_right_identity key) 13) 1 (ite (= (call_right_identity key) 14) 2 (ite (= (call_right_identity key) 15) 3 (ite (= (call_right_identity key) 16) 4 (ite (= (call_right_identity key) 17) 5 (ite (= (call_right_identity key) 18) 0 (ite (= (call_right_identity key) 19) 1 (ite (= (call_right_identity key) 20) 2 (ite (= (call_right_identity key) 21) 3 (ite (= (call_right_identity key) 22) 4 (ite (= (call_right_identity key) 23) 5 (ite (= (call_right_identity key) 24) 0 (ite (= (call_right_identity key) 25) 1 (ite (= (call_right_identity key) 26) 2 (ite (= (call_right_identity key) 27) 3 (ite (= (call_right_identity key) 28) 4 (ite (= (call_right_identity key) 29) 5 (ite (= (call_right_identity key) 30) 0 (ite (= (call_right_identity key) 31) 1 (ite (= (call_right_identity key) 32) 2 (ite (= (call_right_identity key) 33) 3 (ite (= (call_right_identity key) 34) 4 (ite (= (call_right_identity key) 35) 5 (ite (= (call_right_identity key) 36) 0 (ite (= (call_right_identity key) 37) 1 (ite (= (call_right_identity key) 38) 2 (ite (= (call_right_identity key) 39) 3 (ite (= (call_right_identity key) 40) 4 (ite (= (call_right_identity key) 41) 5 (ite (= (call_right_identity key) 42) 0 (ite (= (call_right_identity key) 43) 1 (ite (= (call_right_identity key) 44) 2 (ite (= (call_right_identity key) 45) 3 (ite (= (call_right_identity key) 46) 4 (ite (= (call_right_identity key) 47) 5 (ite (= (call_right_identity key) 48) 0 (ite (= (call_right_identity key) 49) 1 (ite (= (call_right_identity key) 50) 2 (ite (= (call_right_identity key) 51) 3 (ite (= (call_right_identity key) 52) 4 (ite (= (call_right_identity key) 53) 5 (ite (= (call_right_identity key) 54) 0 (ite (= (call_right_identity key) 55) 1 (ite (= (call_right_identity key) 56) 2 (ite (= (call_right_identity key) 57) 3 (ite (= (call_right_identity key) 58) 4 (ite (= (call_right_identity key) 59) 5 (ite (= (call_right_identity key) 60) 0 (ite (= (call_right_identity key) 61) 1 (ite (= (call_right_identity key) 62) 2 (ite (= (call_right_identity key) 63) 3 (ite (= (call_right_identity key) 64) 4 (ite (= (call_right_identity key) 65) 5 (ite (= (call_right_identity key) 66) 0 (ite (= (call_right_identity key) 67) 1 (ite (= (call_right_identity key) 68) 2 (ite (= (call_right_identity key) 69) 3 (ite (= (call_right_identity key) 70) 4 (ite (= (call_right_identity key) 71) 5 (ite (= (call_right_identity key) 72) 0 (ite (= (call_right_identity key) 73) 1 (ite (= (call_right_identity key) 74) 2 (ite (= (call_right_identity key) 75) 3 (ite (= (call_right_identity key) 76) 4 (ite (= (call_right_identity key) 77) 5 (ite (= (call_right_identity key) 78) 0 (ite (= (call_right_identity key) 79) 1 (call_right_identity key)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) -1 (ite (and (= (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4) (= (call_left_identity key) 5) (= (call_left_identity key) 6) (= (call_left_identity key) 7) (= (call_left_identity key) 8) (= (call_left_identity key) 9) (= (call_left_identity key) 10) (= (call_left_identity key) 11) (= (call_left_identity key) 12) (= (call_left_identity key) 13) (= (call_left_identity key) 14) (= (call_left_identity key) 15) (= (call_left_identity key) 16) (= (call_left_identity key) 17) (= (call_left_identity key) 18) (= (call_left_identity key) 19) (= (call_left_identity key) 20) (= (call_left_identity key) 21) (= (call_left_identity key) 22) (= (call_left_identity key) 23) (= (call_left_identity key) 24) (= (call_left_identity key) 25) (= (call_left_identity key) 26) (= (call_left_identity key) 27) (= (call_left_identity key) 28) (= (call_left_identity key) 29) (= (call_left_identity key) 30) (= (call_left_identity key) 31) (= (call_left_identity key) 32) (= (call_left_identity key) 33) (= (call_left_identity key) 34) (= (call_left_identity key) 35) (= (call_left_identity key) 36) (= (call_left_identity key) 37) (= (call_left_identity key) 38) (= (call_left_identity key) 39) (= (call_left_identity key) 40) (= (call_left_identity key) 41) (= (call_left_identity key) 42) (= (call_left_identity key) 43) (= (call_left_identity key) 44) (= (call_left_identity key) 45) (= (call_left_identity key) 46) (= (call_left_identity key) 47) (= (call_left_identity key) 48) (= (call_left_identity key) 49) (= (call_left_identity key) 50) (= (call_left_identity key) 51) (= (call_left_identity key) 52) (= (call_left_identity key) 53) (= (call_left_identity key) 54) (= (call_left_identity key) 55) (= (call_left_identity key) 56) (= (call_left_identity key) 57) (= (call_left_identity key) 58) (= (call_left_identity key) 59) (= (call_left_identity key) 60) (= (call_left_identity key) 61) (= (call_left_identity key) 62) (= (call_left_identity key) 63) (= (call_left_identity key) 64) (= (call_left_identity key) 65) (= (call_left_identity key) 66) (= (call_left_identity key) 67) (= (call_left_identity key) 68) (= (call_left_identity key) 69) (= (call_left_identity key) 70) (= (call_left_identity key) 71) (= (call_left_identity key) 72) (= (call_left_identity key) 73) (= (call_left_identity key) 74) (= (call_left_identity key) 75) (= (call_left_identity key) 76) (= (call_left_identity key) 77) (= (call_left_identity key) 78) (= (call_left_identity key) 79)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4) (= (call_right_identity key) 5) (= (call_right_identity key) 6) (= (call_right_identity key) 7) (= (call_right_identity key) 8) (= (call_right_identity key) 9) (= (call_right_identity key) 10) (= (call_right_identity key) 11) (= (call_right_identity key) 12) (= (call_right_identity key) 13) (= (call_right_identity key) 14) (= (call_right_identity key) 15) (= (call_right_identity key) 16) (= (call_right_identity key) 17) (= (call_right_identity key) 18) (= (call_right_identity key) 19) (= (call_right_identity key) 20) (= (call_right_identity key) 21) (= (call_right_identity key) 22) (= (call_right_identity key) 23) (= (call_right_identity key) 24) (= (call_right_identity key) 25) (= (call_right_identity key) 26) (= (call_right_identity key) 27) (= (call_right_identity key) 28) (= (call_right_identity key) 29) (= (call_right_identity key) 30) (= (call_right_identity key) 31) (= (call_right_identity key) 32) (= (call_right_identity key) 33) (= (call_right_identity key) 34) (= (call_right_identity key) 35) (= (call_right_identity key) 36) (= (call_right_identity key) 37) (= (call_right_identity key) 38) (= (call_right_identity key) 39) (= (call_right_identity key) 40) (= (call_right_identity key) 41) (= (call_right_identity key) 42) (= (call_right_identity key) 43) (= (call_right_identity key) 44) (= (call_right_identity key) 45) (= (call_right_identity key) 46) (= (call_right_identity key) 47) (= (call_right_identity key) 48) (= (call_right_identity key) 49) (= (call_right_identity key) 50) (= (call_right_identity key) 51) (= (call_right_identity key) 52) (= (call_right_identity key) 53) (= (call_right_identity key) 54) (= (call_right_identity key) 55) (= (call_right_identity key) 56) (= (call_right_identity key) 57) (= (call_right_identity key) 58) (= (call_right_identity key) 59) (= (call_right_identity key) 60) (= (call_right_identity key) 61) (= (call_right_identity key) 62) (= (call_right_identity key) 63) (= (call_right_identity key) 64) (= (call_right_identity key) 65) (= (call_right_identity key) 66) (= (call_right_identity key) 67) (= (call_right_identity key) 68) (= (call_right_identity key) 69) (= (call_right_identity key) 70) (= (call_right_identity key) 71) (= (call_right_identity key) 72) (= (call_right_identity key) 73) (= (call_right_identity key) 74) (= (call_right_identity key) 75) (= (call_right_identity key) 76) (= (call_right_identity key) 77) (= (call_right_identity key) 78) (= (call_right_identity key) 79)) 0 1)) (= (ite (= (call_left_identity key) 0) 0 (ite (= (call_left_identity key) 1) 1 (ite (= (call_left_identity key) 2) 2 (ite (= (call_left_identity key) 3) 3 (ite (= (call_left_identity key) 4) 4 (ite (= (call_left_identity key) 5) 5 (ite (= (call_left_identity key) 6) 0 (ite (= (call_left_identity key) 7) 1 (ite (= (call_left_identity key) 8) 2 (ite (= (call_left_identity key) 9) 3 (ite (= (call_left_identity key) 10) 4 (ite (= (call_left_identity key) 11) 5 (ite (= (call_left_identity key) 12) 0 (ite (= (call_left_identity key) 13) 1 (ite (= (call_left_identity key) 14) 2 (ite (= (call_left_identity key) 15) 3 (ite (= (call_left_identity key) 16) 4 (ite (= (call_left_identity key) 17) 5 (ite (= (call_left_identity key) 18) 0 (ite (= (call_left_identity key) 19) 1 (ite (= (call_left_identity key) 20) 2 (ite (= (call_left_identity key) 21) 3 (ite (= (call_left_identity key) 22) 4 (ite (= (call_left_identity key) 23) 5 (ite (= (call_left_identity key) 24) 0 (ite (= (call_left_identity key) 25) 1 (ite (= (call_left_identity key) 26) 2 (ite (= (call_left_identity key) 27) 3 (ite (= (call_left_identity key) 28) 4 (ite (= (call_left_identity key) 29) 5 (ite (= (call_left_identity key) 30) 0 (ite (= (call_left_identity key) 31) 1 (ite (= (call_left_identity key) 32) 2 (ite (= (call_left_identity key) 33) 3 (ite (= (call_left_identity key) 34) 4 (ite (= (call_left_identity key) 35) 5 (ite (= (call_left_identity key) 36) 0 (ite (= (call_left_identity key) 37) 1 (ite (= (call_left_identity key) 38) 2 (ite (= (call_left_identity key) 39) 3 (ite (= (call_left_identity key) 40) 4 (ite (= (call_left_identity key) 41) 5 (ite (= (call_left_identity key) 42) 0 (ite (= (call_left_identity key) 43) 1 (ite (= (call_left_identity key) 44) 2 (ite (= (call_left_identity key) 45) 3 (ite (= (call_left_identity key) 46) 4 (ite (= (call_left_identity key) 47) 5 (ite (= (call_left_identity key) 48) 0 (ite (= (call_left_identity key) 49) 1 (ite (= (call_left_identity key) 50) 2 (ite (= (call_left_identity key) 51) 3 (ite (= (call_left_identity key) 52) 4 (ite (= (call_left_identity key) 53) 5 (ite (= (call_left_identity key) 54) 0 (ite (= (call_left_identity key) 55) 1 (ite (= (call_left_identity key) 56) 2 (ite (= (call_left_identity key) 57) 3 (ite (= (call_left_identity key) 58) 4 (ite (= (call_left_identity key) 59) 5 (ite (= (call_left_identity key) 60) 0 (ite (= (call_left_identity key) 61) 1 (ite (= (call_left_identity key) 62) 2 (ite (= (call_left_identity key) 63) 3 (ite (= (call_left_identity key) 64) 4 (ite (= (call_left_identity key) 65) 5 (ite (= (call_left_identity key) 66) 0 (ite (= (call_left_identity key) 67) 1 (ite (= (call_left_identity key) 68) 2 (ite (= (call_left_identity key) 69) 3 (ite (= (call_left_identity key) 70) 4 (ite (= (call_left_identity key) 71) 5 (ite (= (call_left_identity key) 72) 0 (ite (= (call_left_identity key) 73) 1 (ite (= (call_left_identity key) 74) 2 (ite (= (call_left_identity key) 75) 3 (ite (= (call_left_identity key) 76) 4 (ite (= (call_left_identity key) 77) 5 (ite (= (call_left_identity key) 78) 0 (ite (= (call_left_identity key) 79) 1 (call_left_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) (ite (= (call_right_identity key) 0) 0 (ite (= (call_right_identity key) 1) 1 (ite (= (call_right_identity key) 2) 2 (ite (= (call_right_identity key) 3) 3 (ite (= (call_right_identity key) 4) 4 (ite (= (call_right_identity key) 5) 5 (ite (= (call_right_identity key) 6) 0 (ite (= (call_right_identity key) 7) 1 (ite (= (call_right_identity key) 8) 2 (ite (= (call_right_identity key) 9) 3 (ite (= (call_right_identity key) 10) 4 (ite (= (call_right_identity key) 11) 5 (ite (= (call_right_identity key) 12) 0 (ite (= (call_right_identity key) 13) 1 (ite (= (call_right_identity key) 14) 2 (ite (= (call_right_identity key) 15) 3 (ite (= (call_right_identity key) 16) 4 (ite (= (call_right_identity key) 17) 5 (ite (= (call_right_identity key) 18) 0 (ite (= (call_right_identity key) 19) 1 (ite (= (call_right_identity key) 20) 2 (ite (= (call_right_identity key) 21) 3 (ite (= (call_right_identity key) 22) 4 (ite (= (call_right_identity key) 23) 5 (ite (= (call_right_identity key) 24) 0 (ite (= (call_right_identity key) 25) 1 (ite (= (call_right_identity key) 26) 2 (ite (= (call_right_identity key) 27) 3 (ite (= (call_right_identity key) 28) 4 (ite (= (call_right_identity key) 29) 5 (ite (= (call_right_identity key) 30) 0 (ite (= (call_right_identity key) 31) 1 (ite (= (call_right_identity key) 32) 2 (ite (= (call_right_identity key) 33) 3 (ite (= (call_right_identity key) 34) 4 (ite (= (call_right_identity key) 35) 5 (ite (= (call_right_identity key) 36) 0 (ite (= (call_right_identity key) 37) 1 (ite (= (call_right_identity key) 38) 2 (ite (= (call_right_identity key) 39) 3 (ite (= (call_right_identity key) 40) 4 (ite (= (call_right_identity key) 41) 5 (ite (= (call_right_identity key) 42) 0 (ite (= (call_right_identity key) 43) 1 (ite (= (call_right_identity key) 44) 2 (ite (= (call_right_identity key) 45) 3 (ite (= (call_right_identity key) 46) 4 (ite (= (call_right_identity key) 47) 5 (ite (= (call_right_identity key) 48) 0 (ite (= (call_right_identity key) 49) 1 (ite (= (call_right_identity key) 50) 2 (ite (= (call_right_identity key) 51) 3 (ite (= (call_right_identity key) 52) 4 (ite (= (call_right_identity key) 53) 5 (ite (= (call_right_identity key) 54) 0 (ite (= (call_right_identity key) 55) 1 (ite (= (call_right_identity key) 56) 2 (ite (= (call_right_identity key) 57) 3 (ite (= (call_right_identity key) 58) 4 (ite (= (call_right_identity key) 59) 5 (ite (= (call_right_identity key) 60) 0 (ite (= (call_right_identity key) 61) 1 (ite (= (call_right_identity key) 62) 2 (ite (= (call_right_identity key) 63) 3 (ite (= (call_right_identity key) 64) 4 (ite (= (call_right_identity key) 65) 5 (ite (= (call_right_identity key) 66) 0 (ite (= (call_right_identity key) 67) 1 (ite (= (call_right_identity key) 68) 2 (ite (= (call_right_identity key) 69) 3 (ite (= (call_right_identity key) 70) 4 (ite (= (call_right_identity key) 71) 5 (ite (= (call_right_identity key) 72) 0 (ite (= (call_right_identity key) 73) 1 (ite (= (call_right_identity key) 74) 2 (ite (= (call_right_identity key) 75) 3 (ite (= (call_right_identity key) 76) 4 (ite (= (call_right_identity key) 77) 5 (ite (= (call_right_identity key) 78) 0 (ite (= (call_right_identity key) 79) 1 (call_right_identity key))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) (or (= (call_state key) 146)))))
(define-fun configuration081_20 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_20 () ExactState
  (mkExactState (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 56) 1 44) 2 42) 3 50) 4 24) 5 31) 6 68) 7 11) 8 66) 9 41) 10 75) 11 8) 12 37) 13 29) 14 1) 15 14) 16 52) 17 59) 18 63) 19 18) 20 47) 21 2) 22 78) 23 74) 24 23) 25 7) 26 10) 27 60) 28 26) 29 15) 30 55) 31 71) 32 25) 33 77) 34 0) 35 3) 36 16) 37 76) 38 28) 39 79) 40 48) 41 13) 42 40) 43 39) 44 20) 45 69) 46 22) 47 54) 48 35) 49 30) 50 21) 51 43) 52 4) 53 46) 54 6) 55 19) 56 9) 57 57) 58 72) 59 73) 60 70) 61 34) 62 58) 63 32) 64 12) 65 67) 66 36) 67 17) 68 64) 69 27) 70 45) 71 61) 72 38) 73 51) 74 62) 75 65) 76 33) 77 5) 78 53) 79 49) 0 false))
(define-fun drop081_20 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_20 () ExactState
  (ExactSort initial081_20 boundary081_20 configuration081_20 80))
(define-fun private_right081_20 () ExactState
  (ExactSort initial081_20 boundary081_20 configuration081_20 80))
(define-fun public_left081_20 () PublicResult081
  (FinishPublic081 private_left081_20 drop081_20))
(define-fun public_right081_20 () PublicResult081
  (FinishPublic081 private_right081_20 drop081_20))
(assert (not (= public_left081_20 public_right081_20)))
; fixed Boundary_T source case=duplicate-equal-key-total-order
(define-fun boundary081_21 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (or (< (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4)) 0 1)) (and (= (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4)) 0 1)) (< (ite (= (pair_left_identity key) 0) 0 (ite (= (pair_left_identity key) 1) 0 (ite (= (pair_left_identity key) 2) 1 (ite (= (pair_left_identity key) 3) 1 (ite (= (pair_left_identity key) 4) 2 (pair_left_identity key)))))) (ite (= (pair_right_identity key) 0) 0 (ite (= (pair_right_identity key) 1) 0 (ite (= (pair_right_identity key) 2) 1 (ite (= (pair_right_identity key) 3) 1 (ite (= (pair_right_identity key) 4) 2 (pair_right_identity key))))))))) -1 (ite (and (= (ite (or (= (pair_left_identity key) 0) (= (pair_left_identity key) 1) (= (pair_left_identity key) 2) (= (pair_left_identity key) 3) (= (pair_left_identity key) 4)) 0 1) (ite (or (= (pair_right_identity key) 0) (= (pair_right_identity key) 1) (= (pair_right_identity key) 2) (= (pair_right_identity key) 3) (= (pair_right_identity key) 4)) 0 1)) (= (ite (= (pair_left_identity key) 0) 0 (ite (= (pair_left_identity key) 1) 0 (ite (= (pair_left_identity key) 2) 1 (ite (= (pair_left_identity key) 3) 1 (ite (= (pair_left_identity key) 4) 2 (pair_left_identity key)))))) (ite (= (pair_right_identity key) 0) 0 (ite (= (pair_right_identity key) 1) 0 (ite (= (pair_right_identity key) 2) 1 (ite (= (pair_right_identity key) 3) 1 (ite (= (pair_right_identity key) 4) 2 (pair_right_identity key)))))))) 0 1)))
    (lambda ((key CallKey)) (ite (or (< (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4)) 0 1)) (and (= (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4)) 0 1)) (< (ite (= (call_left_identity key) 0) 0 (ite (= (call_left_identity key) 1) 0 (ite (= (call_left_identity key) 2) 1 (ite (= (call_left_identity key) 3) 1 (ite (= (call_left_identity key) 4) 2 (call_left_identity key)))))) (ite (= (call_right_identity key) 0) 0 (ite (= (call_right_identity key) 1) 0 (ite (= (call_right_identity key) 2) 1 (ite (= (call_right_identity key) 3) 1 (ite (= (call_right_identity key) 4) 2 (call_right_identity key))))))))) -1 (ite (and (= (ite (or (= (call_left_identity key) 0) (= (call_left_identity key) 1) (= (call_left_identity key) 2) (= (call_left_identity key) 3) (= (call_left_identity key) 4)) 0 1) (ite (or (= (call_right_identity key) 0) (= (call_right_identity key) 1) (= (call_right_identity key) 2) (= (call_right_identity key) 3) (= (call_right_identity key) 4)) 0 1)) (= (ite (= (call_left_identity key) 0) 0 (ite (= (call_left_identity key) 1) 0 (ite (= (call_left_identity key) 2) 1 (ite (= (call_left_identity key) 3) 1 (ite (= (call_left_identity key) 4) 2 (call_left_identity key)))))) (ite (= (call_right_identity key) 0) 0 (ite (= (call_right_identity key) 1) 0 (ite (= (call_right_identity key) 2) 1 (ite (= (call_right_identity key) 3) 1 (ite (= (call_right_identity key) 4) 2 (call_right_identity key)))))))) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_21 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_21 () ExactState
  (mkExactState (store (store (store (store (store ((as const (Array Int Int)) 0) 0 4) 1 1) 2 3) 3 2) 4 0) 0 false))
(define-fun drop081_21 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_21 () ExactState
  (ExactSort initial081_21 boundary081_21 configuration081_21 5))
(define-fun private_right081_21 () ExactState
  (ExactSort initial081_21 boundary081_21 configuration081_21 5))
(define-fun public_left081_21 () PublicResult081
  (FinishPublic081 private_left081_21 drop081_21))
(define-fun public_right081_21 () PublicResult081
  (FinishPublic081 private_right081_21 drop081_21))
(assert (not (= public_left081_21 public_right081_21)))
; fixed Boundary_T source case=callback-state-affine
(define-fun boundary081_22 () Boundary
  (mkBoundary
    81
    2
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (* 2 (call_state key)) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_22 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_22 () ExactState
  (mkExactState (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 5) 1 3) 2 4) 3 1) 4 2) 5 0) 2 false))
(define-fun drop081_22 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (+ (* 3 (drop_state key)) 2))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_22 () ExactState
  (ExactSort initial081_22 boundary081_22 configuration081_22 6))
(define-fun private_right081_22 () ExactState
  (ExactSort initial081_22 boundary081_22 configuration081_22 6))
(define-fun public_left081_22 () PublicResult081
  (FinishPublic081 private_left081_22 drop081_22))
(define-fun public_right081_22 () PublicResult081
  (FinishPublic081 private_right081_22 drop081_22))
(assert (not (= public_left081_22 public_right081_22)))
; fixed Boundary_T source case=observable-interior-mutation-normal
(define-fun boundary081_23 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_23 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_23 () ExactState
  (mkExactState (store (store (store (store (store (store ((as const (Array Int Int)) 0) 0 5) 1 3) 2 4) 3 1) 4 2) 5 0) 0 false))
(define-fun drop081_23 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_23 () ExactState
  (ExactSort initial081_23 boundary081_23 configuration081_23 6))
(define-fun private_right081_23 () ExactState
  (ExactSort initial081_23 boundary081_23 configuration081_23 6))
(define-fun public_left081_23 () PublicResult081
  (FinishPublic081 private_left081_23 drop081_23))
(define-fun public_right081_23 () PublicResult081
  (FinishPublic081 private_right081_23 drop081_23))
(assert (not (= public_left081_23 public_right081_23)))
; fixed Boundary_T source case=normal-callback-drop-panic
(define-fun boundary081_24 () Boundary
  (mkBoundary
    81
    7
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) false)))
(define-fun configuration081_24 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_24 () ExactState
  (mkExactState ((as const (Array Int Int)) 0) 7 false))
(define-fun drop081_24 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (drop_state key))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false (or (= (drop_state key) 7))))))
(define-fun private_left081_24 () ExactState
  (ExactSort initial081_24 boundary081_24 configuration081_24 0))
(define-fun private_right081_24 () ExactState
  (ExactSort initial081_24 boundary081_24 configuration081_24 0))
(define-fun public_left081_24 () PublicResult081
  (FinishPublic081 private_left081_24 drop081_24))
(define-fun public_right081_24 () PublicResult081
  (FinishPublic081 private_right081_24 drop081_24))
(assert (not (= public_left081_24 public_right081_24)))
; fixed Boundary_T source case=comparator-panic-drop-completes
(define-fun boundary081_25 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) (or (= (call_state key) 0)))))
(define-fun configuration081_25 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_25 () ExactState
  (mkExactState (store (store (store (store ((as const (Array Int Int)) 0) 0 3) 1 2) 2 1) 3 0) 0 false))
(define-fun drop081_25 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (+ (drop_state key) 1))
    (lambda ((key DropKey)) (ite (drop_unwinding key) false false))))
(define-fun private_left081_25 () ExactState
  (ExactSort initial081_25 boundary081_25 configuration081_25 4))
(define-fun private_right081_25 () ExactState
  (ExactSort initial081_25 boundary081_25 configuration081_25 4))
(define-fun public_left081_25 () PublicResult081
  (FinishPublic081 private_left081_25 drop081_25))
(define-fun public_right081_25 () PublicResult081
  (FinishPublic081 private_right081_25 drop081_25))
(assert (not (= public_left081_25 public_right081_25)))
; fixed Boundary_T source case=comparator-panic-drop-double-panic-abort
(define-fun boundary081_26 () Boundary
  (mkBoundary
    81
    0
    (lambda ((key PairKey)) (ite (< (pair_left_identity key) (pair_right_identity key)) -1 (ite (= (pair_left_identity key) (pair_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (ite (< (call_left_identity key) (call_right_identity key)) -1 (ite (= (call_left_identity key) (call_right_identity key)) 0 1)))
    (lambda ((key CallKey)) (+ (call_state key) 1))
    (lambda ((key CallKey)) (or (= (call_state key) 0)))))
(define-fun configuration081_26 () SortConfiguration
  (mkSortConfiguration
    false
    64
    8
    false
    false))
(define-fun initial081_26 () ExactState
  (mkExactState (store (store (store (store ((as const (Array Int Int)) 0) 0 3) 1 2) 2 1) 3 0) 0 false))
(define-fun drop081_26 () DropBoundary
  (mkDropBoundary
    (lambda ((key DropKey)) (+ (drop_state key) 1))
    (lambda ((key DropKey)) (ite (drop_unwinding key) (or (= (drop_state key) 1)) false))))
(define-fun private_left081_26 () ExactState
  (ExactSort initial081_26 boundary081_26 configuration081_26 4))
(define-fun private_right081_26 () ExactState
  (ExactSort initial081_26 boundary081_26 configuration081_26 4))
(define-fun public_left081_26 () PublicResult081
  (FinishPublic081 private_left081_26 drop081_26))
(define-fun public_right081_26 () PublicResult081
  (FinishPublic081 private_right081_26 drop081_26))
(assert (not (= public_left081_26 public_right081_26)))
(check-sat-using (then ctx-solver-simplify smt))
