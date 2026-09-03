; Target: core::slice::select_nth_unstable_by
; Model: target-078-operational-v1-rust-1.96-complete
; Active contract SHA-256: 8d197563a2e9735beef3c52ff46ea5d3dd44da47b48e3b199654cf3c667490d7
; Executable source semantics: tools/target_078_operational_v1.py
; Two independently declared executions are constrained by the same explicit,
; deterministic source-step relation and immutable callback maps.
(set-logic ALL)
(declare-datatypes ((CallKey 0))
  (((mkCallKey
      (call_state Int)
      (call_left_identity Int)
      (call_right_identity Int)))))
(declare-datatypes ((PairKey 0))
  (((mkPairKey
      (pair_left_identity Int)
      (pair_right_identity Int)))))
(declare-datatypes ((Input 0))
  (((mkInput
      (x_length Int)
      (x_index Int)
      (x_allocation Int)
      (x_borrow Int)
      (x_initial_sequence (Array Int Int))
      (x_is_zst Bool)))))
(declare-datatypes ((Configuration 0))
  (((mkConfiguration
      (c_optimize_for_size Bool)
      (c_element_size Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_callback_identity Int)
      (b_initial_state Int)
      (b_contract_ordering (Array PairKey Int))
      (b_ordering (Array CallKey Int))
      (b_next_state (Array CallKey Int))
      (b_panics (Array CallKey Bool))))))
(declare-datatypes ((Reference 0))
  (((mkReference
      (ref_allocation Int)
      (ref_parent_borrow Int)
      (ref_start Int)
      (ref_span Int)
      (ref_projection_kind Int)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_left Reference)
      (y_pivot Reference)
      (y_right Reference)
      (y_pivot_identity Int)))))
(declare-datatypes ((FinalState 0))
  (((mkFinalState
      (s_final_sequence (Array Int Int))
      (s_allocation Int)
      (s_borrow Int)
      (s_length Int)
      (s_callback_state Int)
      (s_panicked Bool)
      (s_terminal Bool)))))
(declare-datatypes ((Machine 0))
  (((mkMachine
      (m_sequence (Array Int Int))
      (m_callback_state Int)
      (m_start Int)
      (m_end Int)
      (m_index Int)
      (m_limit Int)
      (m_phase Int)
      (m_mode Int)
      (m_cursor Int)
      (m_accumulator Int)
      (m_tail Int)
      (m_sift Int)
      (m_gap Int)
      (m_temporary Int)
      (m_panicked Bool)
      (m_terminal Bool)))))

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
    (forall ((left Int) (right Int))
      (let ((ordering (ContractOrdering b left right)))
        (or (= ordering -1) (= ordering 0) (= ordering 1))))
    (forall ((value Int))
      (= (ContractOrdering b value value) 0))
    (forall ((left Int) (right Int))
      (= (ContractOrdering b left right)
         (- (ContractOrdering b right left))))
    (forall ((left Int) (right Int))
      (or
        (<= (ContractOrdering b left right) 0)
        (<= (ContractOrdering b right left) 0)))
    (forall ((left Int) (middle Int) (right Int))
      (=>
        (and
          (<= (ContractOrdering b left middle) 0)
          (<= (ContractOrdering b middle right) 0))
        (<= (ContractOrdering b left right) 0)))))
(define-fun InputWellFormed ((x Input) (c Configuration)) Bool
  (and
    (< 0 (x_length x))
    (<= 0 (x_index x))
    (< (x_index x) (x_length x))
    (<= 0 (c_element_size c))
    (= (x_is_zst x) (= (c_element_size c) 0))))

; 0=ZST, 1=max, 2=min, 3=optimize-for-size, 4=introselect.
(define-fun PartitionAtIndexBranch
  ((x Input) (c Configuration)) Int
  (ite
    (x_is_zst x)
    0
    (ite
      (= (x_index x) (- (x_length x) 1))
      1
      (ite
        (= (x_index x) 0)
        2
        (ite (c_optimize_for_size c) 3 4)))))
; 0=lomuto-simple, 1=lomuto-cyclic/unroll-2,
; 2=lomuto-cyclic/unroll-1, 3=hoare-cyclic.
(define-fun PartitionKernel ((c Configuration)) Int
  (ite
    (<= (c_element_size c) 96)
    (ite
      (c_optimize_for_size c)
      0
      (ite (<= (c_element_size c) 16) 1 2))
    3))
(define-fun ChoosePivotRecurses ((length Int)) Bool (<= 64 length))
(define-fun IntroselectLimit () Int 16)
(define-fun NintherFraction ((length Int)) Int
  (ite
    (<= length 1024)
    (div length 12)
    (ite
      (<= length (* 128 1024))
      (div length 64)
      (div length 1024))))
(define-fun MedianIndex
  ((less_c_a Bool)
   (less_cprime_b Bool)
   (less_b_aprime Bool)
   (a Int)
   (b Int)
   (c Int)) Int
  (let ((aprime (ite less_c_a c a))
        (cprime (ite less_c_a a c)))
    (ite less_cprime_b cprime
      (ite less_b_aprime aprime b))))
(define-fun SwapArray
  ((sequence (Array Int Int)) (left Int) (right Int)) (Array Int Int)
  (store
    (store sequence left (select sequence right))
    right
    (select sequence left)))
(define-fun WindowShrinks
  ((old_start Int) (old_end Int) (new_start Int) (new_end Int)) Bool
  (and
    (<= old_start new_start)
    (<= new_start new_end)
    (<= new_end old_end)
    (< (- new_end new_start) (- old_end old_start))))
(define-fun NarrowLeft
  ((m Machine)) Machine
  (mkMachine
    (m_sequence m) (m_callback_state m)
    (m_start m) (m_accumulator m) (m_index m)
    (ite (> (m_limit m) 0) (- (m_limit m) 1) 0)
    0 (m_mode m) 0 0 (+ (m_start m) 1) 0 0 0
    (m_panicked m) false))
(define-fun NarrowRight
  ((m Machine)) Machine
  (let ((new_start (+ (m_accumulator m) 1))
        (target (+ (m_start m) (m_index m))))
    (mkMachine
      (m_sequence m) (m_callback_state m)
      new_start (m_end m) (- target new_start)
      (ite (> (m_limit m) 0) (- (m_limit m) 1) 0)
      8 (m_mode m) 0 0 (+ new_start 1) 0 0
      (select (m_sequence m) (m_accumulator m))
      (m_panicked m) false)))
(define-fun AncestorReversePredicate
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (not (TargetAdapterIsLess b state right left)))

(define-fun InitialMachine
  ((x Input) (b Boundary)) Machine
  (mkMachine
    (x_initial_sequence x) (b_initial_state b)
    0 (x_length x) (x_index x) 16
    0 0 0 0 1 0 0 0 false false))

; Phase 0: source dispatch.
(define-fun DispatchStep
  ((m Machine) (x Input) (c Configuration)) Machine
  (let ((branch (PartitionAtIndexBranch x c)))
    (ite
      (= branch 0)
      (mkMachine
        (m_sequence m) (m_callback_state m)
        (m_start m) (m_end m) (m_index m) (m_limit m)
        11 branch 0 0 0 0 0 0 false true)
      (ite
        (or (= branch 1) (= branch 2))
        (mkMachine
          (m_sequence m) (m_callback_state m)
          (m_start m) (m_end m) (m_index m) (m_limit m)
          1 branch (+ (m_start m) 1) (m_start m)
          0 0 0 0 false false)
        (ite
          (<= (- (m_end m) (m_start m)) 16)
          (mkMachine
            (m_sequence m) (m_callback_state m)
            (m_start m) (m_end m) (m_index m) (m_limit m)
            3 branch 0 0 (+ (m_start m) 1) 0 0 0 false false)
          (ite
            (= branch 3)
            (mkMachine
              (m_sequence m) (m_callback_state m)
              (m_start m) (m_end m) (m_index m) (m_limit m)
              9 branch 0 0 0 0 0 0 false false)
            (mkMachine
              (m_sequence m) (m_callback_state m)
              (m_start m) (m_end m) (m_index m) (m_limit m)
              5 branch 0 0 0 0 0 0 false false)))))))

; Phase 1: exact min/max scan callback and accumulator update.
(define-fun ExtremeScanStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (>= (m_cursor m) (m_end m))
    (mkMachine
      (m_sequence m) (m_callback_state m)
      (m_start m) (m_end m) (m_index m) (m_limit m)
      2 (m_mode m) (m_cursor m) (m_accumulator m)
      0 0 0 0 false false)
    (let ((left
            (ite
              (= (m_mode m) 2)
              (select (m_sequence m) (m_cursor m))
              (select (m_sequence m) (m_accumulator m))))
          (right
            (ite
              (= (m_mode m) 2)
              (select (m_sequence m) (m_accumulator m))
              (select (m_sequence m) (m_cursor m)))))
      (let ((panics
              (BoundaryPanics b (m_callback_state m) left right))
            (less
              (TargetAdapterIsLess
                b (m_callback_state m) left right)))
        (mkMachine
          (m_sequence m)
          (BoundaryNextState b (m_callback_state m) left right)
          (m_start m) (m_end m) (m_index m) (m_limit m)
          (ite panics 11 1) (m_mode m) (+ (m_cursor m) 1)
          (ite less (m_cursor m) (m_accumulator m))
          0 0 0 0 panics panics)))))

; Phase 2: exact extreme final swap.
(define-fun ExtremeSwapStep
  ((m Machine) (x Input)) Machine
  (mkMachine
    (SwapArray (m_sequence m) (m_accumulator m) (x_index x))
    (m_callback_state m)
    (m_start m) (m_end m) (m_index m) (m_limit m)
    11 (m_mode m) (m_cursor m) (m_accumulator m)
    0 0 0 0 false true))

; Phase 3: exact insert_tail initial comparison.
(define-fun InsertionCompareStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (>= (m_tail m) (m_end m))
    (mkMachine
      (m_sequence m) (m_callback_state m)
      (m_start m) (m_end m) (m_index m) (m_limit m)
      11 (m_mode m) 0 0 (m_tail m) 0 0 0 false true)
    (let ((temporary (select (m_sequence m) (m_tail m)))
          (right (select (m_sequence m) (- (m_tail m) 1))))
      (let ((panics
              (BoundaryPanics
                b (m_callback_state m) temporary right))
            (less
              (TargetAdapterIsLess
                b (m_callback_state m) temporary right)))
        (mkMachine
          (m_sequence m)
          (BoundaryNextState
            b (m_callback_state m) temporary right)
          (m_start m) (m_end m) (m_index m) (m_limit m)
          (ite panics 11 (ite less 4 3))
          (m_mode m) 0 0
          (ite less (m_tail m) (+ (m_tail m) 1))
          (ite less (- (m_tail m) 1) 0)
          (ite less (m_tail m) 0)
          (ite less temporary 0)
          panics panics)))))

; Phase 4: exact shift, callback, and CopyOnDrop restoration.
(define-fun InsertionShiftStep
  ((m Machine) (b Boundary)) Machine
  (let ((shifted
          (store
            (m_sequence m)
            (m_gap m)
            (select (m_sequence m) (m_sift m)))))
    (ite
      (= (m_sift m) (m_start m))
      (mkMachine
        (store shifted (m_sift m) (m_temporary m))
        (m_callback_state m)
        (m_start m) (m_end m) (m_index m) (m_limit m)
        3 (m_mode m) 0 0 (+ (m_tail m) 1)
        0 0 0 false false)
      (let ((next_sift (- (m_sift m) 1)))
        (let ((right (select shifted next_sift))
              (left (m_temporary m)))
          (let ((panics
                  (BoundaryPanics
                    b (m_callback_state m) left right))
                (less
                  (TargetAdapterIsLess
                    b (m_callback_state m) left right)))
            (mkMachine
              (ite
                (or panics (not less))
                (store shifted (m_sift m) (m_temporary m))
                shifted)
              (BoundaryNextState
                b (m_callback_state m) left right)
              (m_start m) (m_end m) (m_index m) (m_limit m)
              (ite panics 11 (ite less 4 3))
              (m_mode m) 0 0
              (ite less (m_tail m) (+ (m_tail m) 1))
              (ite less next_sift 0)
              (ite less (m_sift m) 0)
              (ite less (m_temporary m) 0)
              panics panics)))))))

; Phase 5: exact nonrecursive median3 and pivot-to-front mutation. The
; callback state advances only through comparisons reached by source control.
(define-fun ChoosePivotStep
  ((m Machine) (b Boundary) (c Configuration)) Machine
  (let ((length (- (m_end m) (m_start m))))
    (let ((a (m_start m))
          (sample_b (+ (m_start m) (* 4 (div length 8))))
          (sample_c (+ (m_start m) (* 7 (div length 8)))))
      (let ((state0 (m_callback_state m))
            (value_a (select (m_sequence m) a))
            (value_b (select (m_sequence m) sample_b))
            (value_c (select (m_sequence m) sample_c)))
        (let ((panic1
                (BoundaryPanics b state0 value_a value_b))
              (less_a_b
                (TargetAdapterIsLess b state0 value_a value_b))
              (state1
                (BoundaryNextState b state0 value_a value_b)))
          (let ((panic2
                  (BoundaryPanics b state1 value_a value_c))
                (less_a_c
                  (TargetAdapterIsLess b state1 value_a value_c))
                (state2
                  (BoundaryNextState b state1 value_a value_c)))
            (let ((needs_third (= less_a_b less_a_c)))
              (let ((panic3
                      (BoundaryPanics b state2 value_b value_c))
                    (less_b_c
                      (TargetAdapterIsLess b state2 value_b value_c))
                    (state3
                      (BoundaryNextState b state2 value_b value_c)))
                (let ((panics
                        (or
                          panic1
                          (and (not panic1) panic2)
                          (and
                            (not panic1)
                            (not panic2)
                            needs_third
                            panic3)))
                      (chosen
                        (ite
                          needs_third
                          (ite (xor less_b_c less_a_b) sample_c sample_b)
                          a))
                      (final_state
                        (ite
                          panic1 state1
                          (ite
                            panic2 state2
                            (ite needs_third state3 state2)))))
                  (let ((pivoted
                          (SwapArray
                            (m_sequence m) (m_start m) chosen))
                        (kernel (PartitionKernel c)))
                    (let ((lower_start (+ (m_start m) 1)))
                      (mkMachine
                        (ite panics (m_sequence m) pivoted)
                        final_state
                        (m_start m) (m_end m)
                        (m_index m) (m_limit m)
                        (ite panics 11 6)
                        kernel
                        (ite
                          (or (= kernel 1) (= kernel 2))
                          (+ lower_start 1)
                          lower_start)
                        (m_start m)
                        (ite (= kernel 3) (m_end m) 0)
                        (ite
                          (or (= kernel 1) (= kernel 2))
                          (select pivoted lower_start)
                          0)
                        (ite (= kernel 3) -1 lower_start)
                        (select (m_sequence m) chosen)
                        panics panics))))))))))))

(define-fun MachinePartitionKernel ((m Machine)) Int
  (ite (>= (m_mode m) 4) (- (m_mode m) 4) (m_mode m)))
(define-fun PartitionReverseMode ((m Machine)) Bool
  (>= (m_mode m) 4))
(define-fun PartitionPredicate
  ((m Machine) (b Boundary) (value Int)) Bool
  (ite
    (PartitionReverseMode m)
    (not
      (TargetAdapterIsLess
        b (m_callback_state m) (m_temporary m) value))
    (TargetAdapterIsLess
      b (m_callback_state m) value (m_temporary m))))
(define-fun PartitionPanic
  ((m Machine) (b Boundary) (value Int)) Bool
  (ite
    (PartitionReverseMode m)
    (BoundaryPanics
      b (m_callback_state m) (m_temporary m) value)
    (BoundaryPanics
      b (m_callback_state m) value (m_temporary m))))
(define-fun PartitionNextState
  ((m Machine) (b Boundary) (value Int)) Int
  (ite
    (PartitionReverseMode m)
    (BoundaryNextState
      b (m_callback_state m) (m_temporary m) value)
    (BoundaryNextState
      b (m_callback_state m) value (m_temporary m))))
(define-fun FinishPartition
  ((m Machine) (sequence (Array Int Int)) (pivot_position Int)) Machine
  (mkMachine
    (SwapArray sequence (m_start m) pivot_position)
    (m_callback_state m)
    (m_start m) (m_end m) (m_index m) (m_limit m)
    7 (m_mode m) (m_cursor m) pivot_position
    (m_tail m) (m_sift m) (m_gap m) (m_temporary m)
    false false))

; Source lomuto-simple always swaps the current left/right locations, then
; advances left by the predicate result.
(define-fun SimplePartitionStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (>= (m_cursor m) (m_end m))
    (FinishPartition m (m_sequence m) (m_accumulator m))
    (let ((value (select (m_sequence m) (m_cursor m))))
      (let ((panics (PartitionPanic m b value))
            (goes_left (PartitionPredicate m b value))
            (next_state (PartitionNextState m b value)))
        (mkMachine
          (ite
            panics
            (m_sequence m)
            (SwapArray
              (m_sequence m)
              (+ (m_accumulator m) 1)
              (m_cursor m)))
          next_state
          (m_start m) (m_end m) (m_index m) (m_limit m)
          (ite panics 11 6) (m_mode m)
          (+ (m_cursor m) 1)
          (ite
            (and (not panics) goes_left)
            (+ (m_accumulator m) 1)
            (m_accumulator m))
          (m_tail m) (m_sift m) (m_gap m) (m_temporary m)
          panics panics)))))

; Source lomuto-cyclic preserves the first lower element in GapGuardRaw,
; performs a two-copy cycle for each reached right element, and consumes the
; guard in one final cleanup comparison.
(define-fun CyclicPartitionStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (< (m_cursor m) (m_end m))
    (let ((value (select (m_sequence m) (m_cursor m))))
      (let ((panics (PartitionPanic m b value))
            (goes_left (PartitionPredicate m b value))
            (next_state (PartitionNextState m b value))
            (left (+ (m_accumulator m) 1)))
        (let ((cycled
                (store
                  (store
                    (m_sequence m)
                    (m_gap m)
                    (select (m_sequence m) left))
                  left
                  value)))
          (mkMachine
            (ite
              panics
              (store (m_sequence m) (m_gap m) (m_sift m))
              cycled)
            next_state
            (m_start m) (m_end m) (m_index m) (m_limit m)
            (ite panics 11 6) (m_mode m)
            (+ (m_cursor m) 1)
            (ite
              (and (not panics) goes_left)
              (+ (m_accumulator m) 1)
              (m_accumulator m))
            (m_tail m) (m_sift m) (m_cursor m) (m_temporary m)
            panics panics))))
    (let ((value (m_sift m)))
      (let ((panics (PartitionPanic m b value))
            (goes_left (PartitionPredicate m b value))
            (next_state (PartitionNextState m b value))
            (left (+ (m_accumulator m) 1)))
        (let ((cycled
                (store
                  (store
                    (m_sequence m)
                    (m_gap m)
                    (select (m_sequence m) left))
                  left
                  value))
              (next_acc
                (ite goes_left
                  (+ (m_accumulator m) 1)
                  (m_accumulator m))))
          (ite
            panics
            (mkMachine
              (store (m_sequence m) (m_gap m) value)
              next_state
              (m_start m) (m_end m) (m_index m) (m_limit m)
              11 (m_mode m) (m_cursor m) (m_accumulator m)
              (m_tail m) (m_sift m) (m_gap m) (m_temporary m)
              true true)
            (FinishPartition
              (mkMachine
                cycled next_state
                (m_start m) (m_end m) (m_index m) (m_limit m)
                6 (m_mode m) (m_cursor m) next_acc
                (m_tail m) (m_sift m) (m_gap m) (m_temporary m)
                false false)
              cycled
              next_acc)))))))

(define-fun FinishHoarePartition ((m Machine)) Machine
  (let ((restored
          (ite
            (>= (m_gap m) 0)
            (store (m_sequence m) (m_gap m) (m_sift m))
            (m_sequence m)))
        (pivot_position (- (m_cursor m) 1)))
    (FinishPartition m restored pivot_position)))

; Hoare phase 6 scans from the left. Phase 12 scans from the right and phase
; 13 performs the source gap-copy cycle.
(define-fun HoareLeftStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (>= (m_cursor m) (m_tail m))
    (FinishHoarePartition m)
    (let ((value (select (m_sequence m) (m_cursor m))))
      (let ((panics (PartitionPanic m b value))
            (goes_left (PartitionPredicate m b value))
            (next_state (PartitionNextState m b value)))
        (mkMachine
          (ite
            (and panics (>= (m_gap m) 0))
            (store (m_sequence m) (m_gap m) (m_sift m))
            (m_sequence m))
          next_state
          (m_start m) (m_end m) (m_index m) (m_limit m)
          (ite panics 11 (ite goes_left 6 12))
          (m_mode m)
          (ite goes_left (+ (m_cursor m) 1) (m_cursor m))
          (m_accumulator m) (m_tail m) (m_sift m) (m_gap m)
          (m_temporary m) panics panics)))))

(define-fun HoareRightStep
  ((m Machine) (b Boundary)) Machine
  (let ((right (- (m_tail m) 1)))
    (ite
      (>= (m_cursor m) right)
      (FinishHoarePartition
        (mkMachine
          (m_sequence m) (m_callback_state m)
          (m_start m) (m_end m) (m_index m) (m_limit m)
          12 (m_mode m) (m_cursor m) (m_accumulator m)
          right (m_sift m) (m_gap m) (m_temporary m)
          false false))
      (let ((value (select (m_sequence m) right)))
        (let ((panics (PartitionPanic m b value))
              (goes_left (PartitionPredicate m b value))
              (next_state (PartitionNextState m b value)))
          (mkMachine
            (ite
              (and panics (>= (m_gap m) 0))
              (store (m_sequence m) (m_gap m) (m_sift m))
              (m_sequence m))
            next_state
            (m_start m) (m_end m) (m_index m) (m_limit m)
            (ite panics 11 (ite goes_left 13 12))
            (m_mode m) (m_cursor m) (m_accumulator m)
            right (m_sift m) (m_gap m) (m_temporary m)
            panics panics))))))

(define-fun HoareCycleStep ((m Machine)) Machine
  (let ((first_pair (< (m_gap m) 0)))
    (let ((saved
            (ite first_pair
              (select (m_sequence m) (m_cursor m))
              (m_sift m)))
          (filled
            (ite first_pair
              (m_sequence m)
              (store
                (m_sequence m)
                (m_gap m)
                (select (m_sequence m) (m_cursor m))))))
      (mkMachine
        (store
          filled
          (m_cursor m)
          (select (m_sequence m) (m_tail m)))
        (m_callback_state m)
        (m_start m) (m_end m) (m_index m) (m_limit m)
        6 (m_mode m) (+ (m_cursor m) 1) (m_accumulator m)
        (m_tail m) saved (m_tail m) (m_temporary m)
        false false))))

(define-fun PartitionStep
  ((m Machine) (b Boundary)) Machine
  (ite
    (= (MachinePartitionKernel m) 0)
    (SimplePartitionStep m b)
    (ite
      (or
        (= (MachinePartitionKernel m) 1)
        (= (MachinePartitionKernel m) 2))
      (CyclicPartitionStep m b)
      (HoareLeftStep m b))))

; Phase 7: exact left/right window arithmetic around the realized pivot.
(define-fun NarrowStep
  ((m Machine)) Machine
  (let ((target (+ (m_start m) (m_index m))))
    (ite
      (= (m_accumulator m) target)
      (mkMachine
        (m_sequence m) (m_callback_state m)
        (m_start m) (m_end m) (m_index m) (m_limit m)
        11 (m_mode m) 0 (m_accumulator m) 0 0 0 0 false true)
      (ite
        (< (m_accumulator m) target)
        (NarrowRight m)
        (NarrowLeft m)))))

; Phase 8: source ancestor-pivot comparison and reverse-partition selection.
(define-fun AncestorPivotStep
  ((m Machine) (b Boundary) (c Configuration)) Machine
  (let ((ancestor (m_temporary m))
        (pivot (select (m_sequence m) (m_start m))))
    (let ((panics
            (BoundaryPanics
              b (m_callback_state m) ancestor pivot))
          (less
            (TargetAdapterIsLess
              b (m_callback_state m) ancestor pivot)))
      (let ((kernel (PartitionKernel c))
            (lower_start (+ (m_start m) 1)))
        (mkMachine
          (m_sequence m)
          (BoundaryNextState
            b (m_callback_state m) ancestor pivot)
          (m_start m) (m_end m) (m_index m) (m_limit m)
          (ite panics 11 (ite less 5 6))
          (ite less (m_mode m) (+ 4 kernel))
          (ite
            (or (= kernel 1) (= kernel 2))
            (+ lower_start 1)
            lower_start)
          (m_start m)
          (ite (= kernel 3) (m_end m) 0)
          (ite
            (or (= kernel 1) (= kernel 2))
            (select (m_sequence m) lower_start)
            0)
          (ite (= kernel 3) -1 lower_start)
          pivot
          panics panics)))))

; Phase 9: the fixed sixteen-step fallback dispatch.
(define-fun FallbackStep
  ((m Machine)) Machine
  (ite
    (<= (- (m_end m) (m_start m)) 16)
    (mkMachine
      (m_sequence m) (m_callback_state m)
      (m_start m) (m_end m) (m_index m) 0
      3 (m_mode m) 0 0 (+ (m_start m) 1) 0 0 0 false false)
    (mkMachine
      (m_sequence m) (m_callback_state m)
      (m_start m) (m_end m) (m_index m) 0
      10 (m_mode m) 0 0 0 0 0 0 false false)))

; Phase 10: a ninther comparison/mutation before deterministic partition.
(define-fun NintherStep
  ((m Machine) (b Boundary) (c Configuration)) Machine
  (let ((length (- (m_end m) (m_start m))))
    (let ((frac (NintherFraction length))
          (middle (+ (m_start m) (div length 2))))
      (let ((left_pos (- middle (div frac 2)))
            (right_pos (+ middle (div frac 2))))
        (let ((left (select (m_sequence m) left_pos))
              (right (select (m_sequence m) right_pos)))
          (let ((panics
                  (BoundaryPanics
                    b (m_callback_state m) left right))
                (less
                  (TargetAdapterIsLess
                    b (m_callback_state m) left right)))
            (mkMachine
              (ite
                (and (not panics) less)
                (SwapArray (m_sequence m) left_pos right_pos)
                (m_sequence m))
              (BoundaryNextState
                b (m_callback_state m) left right)
              (m_start m) (m_end m) (m_index m) 0
              (ite panics 11 5)
              (PartitionKernel c) 0 0 0 0 0 0
              panics panics)))))))

(define-fun SourceStep
  ((m Machine) (x Input) (b Boundary) (c Configuration)) Machine
  (ite
    (m_terminal m)
    m
    (ite (= (m_phase m) 0) (DispatchStep m x c)
    (ite (= (m_phase m) 1) (ExtremeScanStep m b)
    (ite (= (m_phase m) 2) (ExtremeSwapStep m x)
    (ite (= (m_phase m) 3) (InsertionCompareStep m b)
    (ite (= (m_phase m) 4) (InsertionShiftStep m b)
    (ite (= (m_phase m) 5) (ChoosePivotStep m b c)
    (ite (= (m_phase m) 6) (PartitionStep m b)
    (ite (= (m_phase m) 7) (NarrowStep m)
    (ite (= (m_phase m) 8) (AncestorPivotStep m b c)
    (ite (= (m_phase m) 9) (FallbackStep m)
    (ite (= (m_phase m) 10) (NintherStep m b c)
    (ite (= (m_phase m) 12) (HoareRightStep m b)
    (ite (= (m_phase m) 13) (HoareCycleStep m)
      (mkMachine
        (m_sequence m) (m_callback_state m)
        (m_start m) (m_end m) (m_index m) (m_limit m)
        11 (m_mode m) (m_cursor m) (m_accumulator m)
        (m_tail m) (m_sift m) (m_gap m) (m_temporary m)
        (m_panicked m) true))))))))))))))))


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


(define-fun LeftReference ((x Input)) Reference
  (mkReference
    (x_allocation x) (x_borrow x) 0 (x_index x) 1))
(define-fun PivotReference ((x Input)) Reference
  (mkReference
    (x_allocation x) (x_borrow x) (x_index x) 1 2))
(define-fun RightReference ((x Input)) Reference
  (mkReference
    (x_allocation x)
    (x_borrow x)
    (+ (x_index x) 1)
    (- (x_length x) (x_index x) 1)
    3))
(define-fun FinalReturnedSubsliceTransition
  ((x Input) (y Output)) Bool
  (and
    (= (y_left y) (LeftReference x))
    (= (y_pivot y) (PivotReference x))
    (= (y_right y) (RightReference x))))

(define-fun-rec IdentityCountThrough
  ((sequence (Array Int Int)) (count Int) (identity Int)) Int
  (ite
    (<= count 0)
    0
    (let ((position (- count 1)))
      (+ (IdentityCountThrough sequence position identity)
         (ite (= (select sequence position) identity) 1 0)))))
(define-fun ActiveFinalConcatConjunct
  ((x Input) (y Output) (s FinalState)) Bool
  (and
    (= (ref_start (y_left y)) 0)
    (= (ref_span (y_left y)) (x_index x))
    (= (ref_start (y_pivot y)) (x_index x))
    (= (ref_span (y_pivot y)) 1)
    (= (ref_start (y_right y)) (+ (x_index x) 1))
    (= (+ (ref_span (y_left y))
          (ref_span (y_pivot y))
          (ref_span (y_right y)))
       (s_length s))))
(define-fun ActiveLeftLengthConjunct
  ((x Input) (y Output)) Bool
  (= (ref_span (y_left y)) (x_index x)))
(define-fun ActivePivotAtIndexConjunct
  ((x Input) (y Output) (s FinalState)) Bool
  (= (y_pivot_identity y)
     (select (s_final_sequence s) (x_index x))))
(define-fun ActiveRightLengthConjunct
  ((x Input) (y Output)) Bool
  (= (ref_span (y_right y))
     (- (x_length x) (x_index x) 1)))
(define-fun ActivePermutationConjunct
  ((x Input) (s FinalState)) Bool
  (forall ((identity Int))
    (= (IdentityCountThrough
         (x_initial_sequence x) (x_length x) identity)
       (IdentityCountThrough
         (s_final_sequence s) (s_length s) identity))))
(define-fun ActiveCallbackPartitionConjunct
  ((x Input) (b Boundary) (y Output) (s FinalState)) Bool
  (and
    (forall ((position Int))
      (=>
        (and (<= 0 position) (< position (x_index x)))
        (<=
          (ContractOrdering
            b
            (select (s_final_sequence s) position)
            (y_pivot_identity y))
          0)))
    (forall ((position Int))
      (=>
        (and (< (x_index x) position) (< position (x_length x)))
        (<=
          (ContractOrdering
            b
            (y_pivot_identity y)
            (select (s_final_sequence s) position))
          0)))))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s FinalState)) Bool
  (and
    (ActiveFinalConcatConjunct x y s)
    (ActiveLeftLengthConjunct x y)
    (ActivePivotAtIndexConjunct x y s)
    (ActiveRightLengthConjunct x y)
    (ActivePermutationConjunct x s)
    (ActiveCallbackPartitionConjunct x b y s)))
(define-fun TargetDefinition_T
  ((x Input)
   (b Boundary)
   (c Configuration)
   (y Output)
   (s FinalState)) Bool
  (let ((run (RunMachine x b c)))
    (and
      (= (y_left y) (LeftReference x))
      (= (y_pivot y) (PivotReference x))
      (= (y_right y) (RightReference x))
      (= (y_pivot_identity y)
         (select (m_sequence run) (x_index x)))
      (= (s_final_sequence s) (m_sequence run))
      (= (s_allocation s) (x_allocation x))
      (= (s_borrow s) (x_borrow x))
      (= (s_length s) (x_length x))
      (= (s_callback_state s) (m_callback_state run))
      (= (s_panicked s) (m_panicked run))
      (= (s_terminal s) (m_terminal run))
      (m_terminal run)
      (FinalReturnedSubsliceTransition x y)
      (=> (not (s_panicked s)) (Spec_T x b y s)))))
(define-fun ExactPrincipalReturnAndFinalState
  ((y1 Output)
   (s1 FinalState)
   (y2 Output)
   (s2 FinalState)) Bool
  (and
    (= (y_left y1) (y_left y2))
    (= (y_pivot y1) (y_pivot y2))
    (= (y_right y1) (y_right y2))
    (= (y_pivot_identity y1) (y_pivot_identity y2))
    (= (s_final_sequence s1) (s_final_sequence s2))
    (= (s_allocation s1) (s_allocation s2))
    (= (s_borrow s1) (s_borrow s2))
    (= (s_length s1) (s_length s2))
    (= (s_callback_state s1) (s_callback_state s2))
    (= (s_panicked s1) (s_panicked s2))
    (= (s_terminal s1) (s_terminal s2))))
(define-fun x () Input
  (mkInput 17 8 41 51 ((as const (Array Int Int)) 0) false))
(assert (= (ref_span (LeftReference x)) 8))
(assert (= (ref_start (PivotReference x)) 8))
(assert (= (ref_start (RightReference x)) 9))
(assert (= (ref_span (RightReference x)) 8))
(check-sat)
