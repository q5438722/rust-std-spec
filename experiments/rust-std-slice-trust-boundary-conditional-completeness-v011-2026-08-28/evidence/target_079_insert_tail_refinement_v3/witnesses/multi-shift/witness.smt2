; Target: core::slice::select_nth_unstable_by_key
; Model: target-079-key-ord-drop-operational-v1-rust-1.96-complete
; Active contract SHA-256: 9366859a88badc5f8d8cdfb15fbc544ef81edb756429e14a887b1ce6c73e3e95
; Executable source semantics: tools/target_079_operational_v1.py
; Exact selection semantics: imported target-078 ExactRunState, with the
; target-079 adapter termination sum threaded through every callback.
(set-logic ALL)
(declare-datatypes ((KeyCall 0))
  (((mkKeyCall
      (key_call_state Int)
      (key_call_value Int)))))
(declare-datatypes ((OwnedKey 0))
  (((mkOwnedKey
      (owned_creation_state Int)
      (owned_slot Int)
      (owned_source_identity Int)
      (owned_key_identity Int)))))
(declare-datatypes ((OrdCall 0))
  (((mkOrdCall
      (ord_call_state Int)
      (ord_call_left OwnedKey)
      (ord_call_right OwnedKey)))))
(declare-datatypes ((DropCall 0))
  (((mkDropCall
      (drop_call_state Int)
      (drop_call_key OwnedKey)))))
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
      (b_key_function_identity Int)
      (b_ord_function_identity Int)
      (b_drop_function_identity Int)
      (b_initial_state Int)
      (b_contract_key (Array Int Int))
      (b_contract_ordering (Array PairKey Int))
      (b_key_result (Array KeyCall Int))
      (b_key_next_state (Array KeyCall Int))
      (b_key_panics (Array KeyCall Bool))
      (b_ord_lt_result (Array OrdCall Bool))
      (b_ord_lt_next_state (Array OrdCall Int))
      (b_ord_lt_panics (Array OrdCall Bool))
      (b_drop_next_state (Array DropCall Int))
      (b_drop_panics (Array DropCall Bool))))))
(declare-datatypes ((AdapterFrame 0))
  (((mkAdapterFrame
      (af_state Int)
      (af_termination Int)
      (af_is_less Bool)
      (af_panic_origin Int)
      (af_left_owned OwnedKey)
      (af_right_owned OwnedKey)
      (af_left_live Bool)
      (af_right_live Bool)))))
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
      (s_termination Int)
      (s_panicked Bool)
      (s_aborted Bool)
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

; Boundary_T consists only of total functional observations.
(define-fun ContractKey ((b Boundary) (value Int)) Int
  (select (b_contract_key b) value))
(define-fun ContractKeyOrdering
  ((b Boundary) (left_key Int) (right_key Int)) Int
  (select
    (b_contract_ordering b)
    (mkPairKey left_key right_key)))
(define-fun ContractOrdering
  ((b Boundary) (left Int) (right Int)) Int
  (ContractKeyOrdering
    b (ContractKey b left) (ContractKey b right)))
(define-fun KeyResult
  ((b Boundary) (state Int) (value Int)) Int
  (select (b_key_result b) (mkKeyCall state value)))
(define-fun KeyNextState
  ((b Boundary) (state Int) (value Int)) Int
  (select (b_key_next_state b) (mkKeyCall state value)))
(define-fun KeyPanics
  ((b Boundary) (state Int) (value Int)) Bool
  (select (b_key_panics b) (mkKeyCall state value)))
(define-fun OrdLtResult
  ((b Boundary) (state Int) (left OwnedKey) (right OwnedKey)) Bool
  (select (b_ord_lt_result b) (mkOrdCall state left right)))
(define-fun OrdLtNextState
  ((b Boundary) (state Int) (left OwnedKey) (right OwnedKey)) Int
  (select (b_ord_lt_next_state b) (mkOrdCall state left right)))
(define-fun OrdLtPanics
  ((b Boundary) (state Int) (left OwnedKey) (right OwnedKey)) Bool
  (select (b_ord_lt_panics b) (mkOrdCall state left right)))
(define-fun DropNextState
  ((b Boundary) (state Int) (key OwnedKey)) Int
  (select (b_drop_next_state b) (mkDropCall state key)))
(define-fun DropPanics
  ((b Boundary) (state Int) (key OwnedKey)) Bool
  (select (b_drop_panics b) (mkDropCall state key)))

; termination: 0=normal, 1=panic/unwind, 2=non-unwinding abort.
(define-fun AdapterInitial ((state Int)) AdapterFrame
  (mkAdapterFrame
    state 0 false 0
    (mkOwnedKey 0 0 0 0)
    (mkOwnedKey 0 1 0 0)
    false false))
(define-fun AdapterKeyLeft
  ((frame AdapterFrame) (b Boundary) (left Int)) AdapterFrame
  (ite
    (= (af_termination frame) 0)
    (let ((state (af_state frame)))
      (let ((key (KeyResult b state left))
            (next (KeyNextState b state left))
            (panics (KeyPanics b state left)))
        (mkAdapterFrame
          next
          (ite panics 1 0)
          false
          (ite panics 1 0)
          (mkOwnedKey state 0 left key)
          (af_right_owned frame)
          (not panics)
          false)))
    frame))
(define-fun AdapterKeyRight
  ((frame AdapterFrame) (b Boundary) (right Int)) AdapterFrame
  (ite
    (= (af_termination frame) 0)
    (let ((state (af_state frame)))
      (let ((key (KeyResult b state right))
            (next (KeyNextState b state right))
            (panics (KeyPanics b state right)))
        (mkAdapterFrame
          next
          (ite panics 1 0)
          false
          (ite panics 2 0)
          (af_left_owned frame)
          (mkOwnedKey state 1 right key)
          (af_left_live frame)
          (not panics))))
    frame))
(define-fun AdapterOrdLt
  ((frame AdapterFrame) (b Boundary)) AdapterFrame
  (ite
    (= (af_termination frame) 0)
    (let ((state (af_state frame))
          (left (af_left_owned frame))
          (right (af_right_owned frame)))
      (let ((less (OrdLtResult b state left right))
            (next (OrdLtNextState b state left right))
            (panics (OrdLtPanics b state left right)))
        (mkAdapterFrame
          next
          (ite panics 1 0)
          less
          (ite panics 3 0)
          left right
          (af_left_live frame)
          (af_right_live frame))))
    frame))
(define-fun AdapterDropRight
  ((frame AdapterFrame) (b Boundary)) AdapterFrame
  (ite
    (and
      (af_right_live frame)
      (not (= (af_termination frame) 2)))
    (let ((state (af_state frame))
          (key (af_right_owned frame))
          (old_termination (af_termination frame)))
      (let ((next (DropNextState b state key))
            (panics (DropPanics b state key)))
        (mkAdapterFrame
          next
          (ite
            panics
            (ite (= old_termination 1) 2 1)
            old_termination)
          (af_is_less frame)
          (ite panics 4 (af_panic_origin frame))
          (af_left_owned frame)
          key
          (af_left_live frame)
          false)))
    frame))
(define-fun AdapterDropLeft
  ((frame AdapterFrame) (b Boundary)) AdapterFrame
  (ite
    (and
      (af_left_live frame)
      (not (= (af_termination frame) 2)))
    (let ((state (af_state frame))
          (key (af_left_owned frame))
          (old_termination (af_termination frame)))
      (let ((next (DropNextState b state key))
            (panics (DropPanics b state key)))
        (mkAdapterFrame
          next
          (ite
            panics
            (ite (= old_termination 1) 2 1)
            old_termination)
          (af_is_less frame)
          (ite panics 5 (af_panic_origin frame))
          key
          (af_right_owned frame)
          false
          (af_right_live frame))))
    frame))
(define-fun AdapterTransition
  ((b Boundary) (state Int) (left Int) (right Int)) AdapterFrame
  (AdapterDropLeft
    (AdapterDropRight
      (AdapterOrdLt
        (AdapterKeyRight
          (AdapterKeyLeft (AdapterInitial state) b left)
          b
          right)
        b)
      b)
    b))
(define-fun BoundaryNextState
  ((b Boundary) (state Int) (left Int) (right Int)) Int
  (af_state (AdapterTransition b state left right)))
(define-fun BoundaryPanics
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (not
    (= (af_termination (AdapterTransition b state left right)) 0)))
(define-fun BoundaryAborts
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (= (af_termination (AdapterTransition b state left right)) 2))
(define-fun TargetAdapterIsLess
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (af_is_less (AdapterTransition b state left right)))

(define-fun BoundaryWellFormed ((b Boundary)) Bool
  (and
    (forall ((state Int) (value Int))
      (= (KeyResult b state value) (ContractKey b value)))
    (forall ((state Int) (left OwnedKey) (right OwnedKey))
      (=
        (OrdLtResult b state left right)
        (=
          (ContractKeyOrdering
            b
            (owned_key_identity left)
            (owned_key_identity right))
          -1)))
    (forall ((left Int) (right Int))
      (let ((ordering (ContractKeyOrdering b left right)))
        (or (= ordering -1) (= ordering 0) (= ordering 1))))
    (forall ((value Int))
      (= (ContractKeyOrdering b value value) 0))
    (forall ((left Int) (right Int))
      (=
        (ContractKeyOrdering b left right)
        (- (ContractKeyOrdering b right left))))
    (forall ((left Int) (right Int))
      (or
        (<= (ContractKeyOrdering b left right) 0)
        (<= (ContractKeyOrdering b right left) 0)))
    (forall ((left Int) (middle Int) (right Int))
      (=>
        (and
          (<= (ContractKeyOrdering b left middle) 0)
          (<= (ContractKeyOrdering b middle right) 0))
        (<= (ContractKeyOrdering b left right) 0)))))
(define-fun InputWellFormed ((x Input) (c Configuration)) Bool
  (and
    (< 0 (x_length x))
    (<= 0 (x_index x))
    (< (x_index x) (x_length x))
    (<= 0 (c_element_size c))
    (= (x_is_zst x) (= (c_element_size c) 0))
    (=>
      (x_is_zst x)
      (forall ((position Int))
        (=>
          (and (<= 0 position) (< position (x_length x)))
          (=
            (select (x_initial_sequence x) position)
            (select (x_initial_sequence x) 0)))))))

; Accepted source dispatch and primitive mutation helpers.
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


; Source-exact target-078 big-step state, imported byte-for-byte before
; adding target-079 adapter abort. Ordinary panic restores active guards;
; abort preserves the interrupted sequence and bypasses cleanup.
(declare-datatypes ((ExactState 0))
  (((mkExactState
      (e_sequence (Array Int Int))
      (e_callback_state Int)
      (e_panicked Bool)
      (e_aborted Bool)))))
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
      (BoundaryPanics b (e_callback_state q) left right)
      (BoundaryAborts b (e_callback_state q) left right)))
(define-fun ExactSwap
  ((q ExactState) (left Int) (right Int)) ExactState
  (mkExactState
      (SwapArray (e_sequence q) left right)
      (e_callback_state q)
      (e_panicked q)
      (e_aborted q)))

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
      false
      (e_aborted q))))
      (ite
        (= sift begin)
        (mkExactState
      (ite (e_aborted shifted) (e_sequence shifted) (store (e_sequence shifted) sift temporary))
      (e_callback_state shifted)
      false
      (e_aborted shifted))
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
      (ite (e_aborted called) (e_sequence called) (store (e_sequence called) sift temporary))
      (e_callback_state called)
      true
      (e_aborted called))
                (ite
                  less
                  (ExactInsertTailLoop
                    called b begin next_sift sift temporary)
                  (mkExactState
      (ite (e_aborted called) (e_sequence called) (store (e_sequence called) sift temporary))
      (e_callback_state called)
      false
      (e_aborted called)))))))))))

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
      (ite (e_aborted q) (e_sequence q) (store (e_sequence q) gap_position gap_value))
      (e_callback_state q)
      true
      (e_aborted q))
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
      (ite (e_aborted (ebr_state predicate)) (e_sequence (ebr_state predicate)) (store
                  (e_sequence (ebr_state predicate))
                  gap_position
                  gap_value))
      (e_callback_state (ebr_state predicate))
      true
      (e_aborted (ebr_state predicate)))
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
      false
      (e_aborted (ebr_state predicate)))))
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
      (ite (e_aborted (ebr_state predicate)) (e_sequence (ebr_state predicate)) (store
                (e_sequence (ebr_state predicate))
                gap_position
                gap_value))
      (e_callback_state (ebr_state predicate))
      true
      (e_aborted (ebr_state predicate)))
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
      false
      (e_aborted (ebr_state predicate)))))
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
      (ite (e_aborted q) (e_sequence q) (store (e_sequence q) gap_position gap_value))
      (e_callback_state q)
      (e_panicked q)
      (e_aborted q))
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
      false
      (e_aborted (ebr_state predicate)))))
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
      false
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
(define-fun ActiveKeyPartitionConjunct
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

; Literal active contract: exactly these six generated conjuncts.
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s FinalState)) Bool
  (and
    (ActiveFinalConcatConjunct x y s)
    (ActiveLeftLengthConjunct x y)
    (ActivePivotAtIndexConjunct x y s)
    (ActiveRightLengthConjunct x y)
    (ActivePermutationConjunct x s)
    (ActiveKeyPartitionConjunct x b y s)))
(define-fun TargetDefinition_T
  ((x Input)
   (b Boundary)
   (c Configuration)
   (y Output)
   (s FinalState)) Bool
  (let ((run (ExactRunState x b c)))
    (let ((termination
            (ite (e_aborted run) 2 (ite (e_panicked run) 1 0))))
      (and
        (= (y_left y) (LeftReference x))
        (= (y_pivot y) (PivotReference x))
        (= (y_right y) (RightReference x))
        (= (y_pivot_identity y)
           (select (e_sequence run) (x_index x)))
        (= (s_final_sequence s) (e_sequence run))
        (= (s_allocation s) (x_allocation x))
        (= (s_borrow s) (x_borrow x))
        (= (s_length s) (x_length x))
        (= (s_callback_state s) (e_callback_state run))
        (= (s_termination s) termination)
        (= (s_panicked s) (e_panicked run))
        (= (s_aborted s) (e_aborted run))
        (s_terminal s)
        (FinalReturnedSubsliceTransition x y)
        (=> (= termination 0) (Spec_T x b y s))))))
(define-fun ExactPrincipalReturn
  ((y1 Output) (y2 Output)) Bool
  (and
    (= (y_left y1) (y_left y2))
    (= (y_pivot y1) (y_pivot y2))
    (= (y_right y1) (y_right y2))
    (= (y_pivot_identity y1) (y_pivot_identity y2))))
(define-fun ExactFinalState
  ((s1 FinalState) (s2 FinalState)) Bool
  (and
    (= (s_final_sequence s1) (s_final_sequence s2))
    (= (s_allocation s1) (s_allocation s2))
    (= (s_borrow s1) (s_borrow s2))
    (= (s_length s1) (s_length s2))
    (= (s_callback_state s1) (s_callback_state s2))
    (= (s_termination s1) (s_termination s2))
    (= (s_panicked s1) (s_panicked s2))
    (= (s_aborted s1) (s_aborted s2))
    (= (s_terminal s1) (s_terminal s2))))
(define-fun ExactPrincipalReturnAndFinalState
  ((y1 Output)
   (s1 FinalState)
   (y2 Output)
   (s2 FinalState)) Bool
  (and
    (ExactPrincipalReturn y1 y2)
    (ExactFinalState s1 s2)))

; Refined definitions mechanically translated from Verus AST.
(define-fun RefinedKeyResult ((boundary Boundary) (state Int) (value Int)) Int
  (select (b_key_result boundary) (mkKeyCall state value)))
(define-fun RefinedKeyNextState ((boundary Boundary) (state Int) (value Int)) Int
  (select (b_key_next_state boundary) (mkKeyCall state value)))
(define-fun RefinedKeyPanics ((boundary Boundary) (state Int) (value Int)) Bool
  (select (b_key_panics boundary) (mkKeyCall state value)))
(define-fun RefinedOrdLtResult ((boundary Boundary) (state Int) (left OwnedKey) (right OwnedKey)) Bool
  (select (b_ord_lt_result boundary) (mkOrdCall state left right)))
(define-fun RefinedOrdLtNextState ((boundary Boundary) (state Int) (left OwnedKey) (right OwnedKey)) Int
  (select (b_ord_lt_next_state boundary) (mkOrdCall state left right)))
(define-fun RefinedOrdLtPanics ((boundary Boundary) (state Int) (left OwnedKey) (right OwnedKey)) Bool
  (select (b_ord_lt_panics boundary) (mkOrdCall state left right)))
(define-fun RefinedDropNextState ((boundary Boundary) (state Int) (key OwnedKey)) Int
  (select (b_drop_next_state boundary) (mkDropCall state key)))
(define-fun RefinedDropPanics ((boundary Boundary) (state Int) (key OwnedKey)) Bool
  (select (b_drop_panics boundary) (mkDropCall state key)))
(define-fun RefinedOwnedKey ((creation_state Int) (slot Int) (source_identity Int) (key_identity Int)) OwnedKey
  (mkOwnedKey creation_state slot source_identity key_identity))
(define-fun RefinedAdapterInitial ((state Int)) AdapterFrame
  (mkAdapterFrame state 0 false 0 (RefinedOwnedKey 0 0 0 0) (RefinedOwnedKey 0 1 0 0) false false))
(define-fun RefinedAdapterKeyLeft ((frame AdapterFrame) (boundary Boundary) (left Int)) AdapterFrame
  (ite (= (af_termination frame) 0) (let ((state (af_state frame))) (let ((key (RefinedKeyResult boundary state left))) (let ((next (RefinedKeyNextState boundary state left))) (let ((panics (RefinedKeyPanics boundary state left))) (mkAdapterFrame next (ite panics 1 0) false (ite panics 1 0) (RefinedOwnedKey state 0 left key) (af_right_owned frame) (not panics) false))))) frame))
(define-fun RefinedAdapterKeyRight ((frame AdapterFrame) (boundary Boundary) (right Int)) AdapterFrame
  (ite (= (af_termination frame) 0) (let ((state (af_state frame))) (let ((key (RefinedKeyResult boundary state right))) (let ((next (RefinedKeyNextState boundary state right))) (let ((panics (RefinedKeyPanics boundary state right))) (mkAdapterFrame next (ite panics 1 0) false (ite panics 2 0) (af_left_owned frame) (RefinedOwnedKey state 1 right key) (af_left_live frame) (not panics)))))) frame))
(define-fun RefinedAdapterOrdLt ((frame AdapterFrame) (boundary Boundary)) AdapterFrame
  (ite (= (af_termination frame) 0) (let ((state (af_state frame))) (let ((left (af_left_owned frame))) (let ((right (af_right_owned frame))) (let ((less (RefinedOrdLtResult boundary state left right))) (let ((next (RefinedOrdLtNextState boundary state left right))) (let ((panics (RefinedOrdLtPanics boundary state left right))) (mkAdapterFrame next (ite panics 1 0) less (ite panics 3 0) left right (af_left_live frame) (af_right_live frame)))))))) frame))
(define-fun RefinedAdapterDropRight ((frame AdapterFrame) (boundary Boundary)) AdapterFrame
  (ite (and (af_right_live frame) (not (= (af_termination frame) 2))) (let ((state (af_state frame))) (let ((key (af_right_owned frame))) (let ((old_termination (af_termination frame))) (let ((next (RefinedDropNextState boundary state key))) (let ((panics (RefinedDropPanics boundary state key))) (mkAdapterFrame next (ite panics (ite (= old_termination 1) 2 1) old_termination) (af_is_less frame) (ite panics 4 (af_panic_origin frame)) (af_left_owned frame) key (af_left_live frame) false)))))) frame))
(define-fun RefinedAdapterDropLeft ((frame AdapterFrame) (boundary Boundary)) AdapterFrame
  (ite (and (af_left_live frame) (not (= (af_termination frame) 2))) (let ((state (af_state frame))) (let ((key (af_left_owned frame))) (let ((old_termination (af_termination frame))) (let ((next (RefinedDropNextState boundary state key))) (let ((panics (RefinedDropPanics boundary state key))) (mkAdapterFrame next (ite panics (ite (= old_termination 1) 2 1) old_termination) (af_is_less frame) (ite panics 5 (af_panic_origin frame)) key (af_right_owned frame) false (af_right_live frame))))))) frame))
(define-fun RefinedAdapterTransition ((boundary Boundary) (state Int) (left Int) (right Int)) AdapterFrame
  (RefinedAdapterDropLeft (RefinedAdapterDropRight (RefinedAdapterOrdLt (RefinedAdapterKeyRight (RefinedAdapterKeyLeft (RefinedAdapterInitial state) boundary left) boundary right) boundary) boundary) boundary))
(define-fun RefinedCallbackFrame ((state ExactState) (boundary Boundary) (left Int) (right Int)) AdapterFrame
  (RefinedAdapterTransition boundary (e_callback_state state) left right))
(define-fun RefinedAdapterCallback ((state ExactState) (boundary Boundary) (left Int) (right Int)) ExactState
  (let ((frame (RefinedCallbackFrame state boundary left right))) (mkExactState (e_sequence state) (af_state frame) (distinct (af_termination frame) 0) (= (af_termination frame) 2))))
(define-fun RefinedTargetAdapterIsLess ((state ExactState) (boundary Boundary) (left Int) (right Int)) Bool
  (af_is_less (RefinedCallbackFrame state boundary left right)))
(define-fun RefinedShiftedState ((state ExactState) (sift Int) (gap Int)) ExactState
  (mkExactState (store (e_sequence state) gap (select (e_sequence state) sift)) (e_callback_state state) false false))
(define-fun RefinedRestoredState ((state ExactState) (destination Int) (temporary Int) (panicked Bool)) ExactState
  (ite (e_aborted state) state (mkExactState (store (e_sequence state) destination temporary) (e_callback_state state) panicked false)))
(define-fun-rec RefinedInsertTailLoop ((state ExactState) (boundary Boundary) (begin Int) (sift Int) (gap Int) (temporary Int)) ExactState
  (ite (or (e_panicked state) (e_aborted state)) state (let ((shifted (RefinedShiftedState state sift gap))) (ite (<= sift begin) (RefinedRestoredState shifted sift temporary false) (let ((next_sift (- sift 1))) (let ((right (select (e_sequence shifted) next_sift))) (let ((called (RefinedAdapterCallback shifted boundary temporary right))) (let ((less (RefinedTargetAdapterIsLess shifted boundary temporary right))) (ite (e_panicked called) (RefinedRestoredState called sift temporary true) (ite less (RefinedInsertTailLoop called boundary begin next_sift sift temporary) (RefinedRestoredState called sift temporary false)))))))))))
(define-fun RefinedInsertTail ((state ExactState) (boundary Boundary) (begin Int) (tail Int)) ExactState
  (ite (or (e_panicked state) (e_aborted state)) state (let ((temporary (select (e_sequence state) tail))) (let ((right (select (e_sequence state) (- tail 1)))) (let ((called (RefinedAdapterCallback state boundary temporary right))) (let ((less (RefinedTargetAdapterIsLess state boundary temporary right))) (ite (e_panicked called) called (ite less (RefinedInsertTailLoop called boundary begin (- tail 1) tail temporary) called))))))))

(declare-const witness_boundary Boundary)
(declare-const witness_sequence (Array Int Int))
(define-fun witness_state () ExactState
  (mkExactState witness_sequence 0 false false))
(assert (= (select witness_sequence 0) 10))
(assert (= (select witness_sequence 1) 20))
(assert (= (select witness_sequence 2) 30))
(assert (= (select witness_sequence 3) 5))
(assert (= (af_state (AdapterTransition witness_boundary 0 5 30)) 1))
(assert (= (af_termination (AdapterTransition witness_boundary 0 5 30)) 0))
(assert (= (af_is_less (AdapterTransition witness_boundary 0 5 30)) true))
(assert (= (af_state (AdapterTransition witness_boundary 1 5 20)) 2))
(assert (= (af_termination (AdapterTransition witness_boundary 1 5 20)) 0))
(assert (= (af_is_less (AdapterTransition witness_boundary 1 5 20)) true))
(assert (= (af_state (AdapterTransition witness_boundary 2 5 10)) 3))
(assert (= (af_termination (AdapterTransition witness_boundary 2 5 10)) 0))
(assert (= (af_is_less (AdapterTransition witness_boundary 2 5 10)) false))
(define-fun witness_exact_run () ExactState
  (ExactInsertTail witness_state witness_boundary 0 3))
(define-fun witness_refined_run () ExactState
  (RefinedInsertTail witness_state witness_boundary 0 3))
(assert (and
  (= (e_sequence witness_exact_run) (e_sequence witness_refined_run))
  (= (e_callback_state witness_exact_run) (e_callback_state witness_refined_run))
  (= (e_panicked witness_exact_run) (e_panicked witness_refined_run))
  (= (e_aborted witness_exact_run) (e_aborted witness_refined_run))
  (= (select (e_sequence witness_exact_run) 0) 10)
  (= (select (e_sequence witness_exact_run) 1) 5)
  (= (select (e_sequence witness_exact_run) 2) 20)
  (= (select (e_sequence witness_exact_run) 3) 30)
  (= (e_callback_state witness_exact_run) 3)
  (not (e_panicked witness_exact_run))
  (not (e_aborted witness_exact_run))))
(check-sat)
(get-model)
