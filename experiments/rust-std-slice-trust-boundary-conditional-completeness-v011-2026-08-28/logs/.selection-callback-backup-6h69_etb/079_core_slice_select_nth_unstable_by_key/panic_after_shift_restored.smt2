; Target: core::slice::select_nth_unstable_by_key
; Active contract SHA-256: 9366859a88badc5f8d8cdfb15fbc544ef81edb756429e14a887b1ce6c73e3e95
; Rust target: core/src/slice/mod.rs:3648-3658
; Public docs: core/src/slice/mod.rs:3592-3645
; Private introselect: core/src/slice/sort/select.rs:17-307
; Lower partition: core/src/slice/sort/unstable/quicksort.rs:93-137
; Purpose: completeness-modulo-reviewed-selection-equivalence
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_length Int)
      (x_index Int)
      (x_allocation Int)
      (x_borrow Int)
      (x_initial_sequence (Array Int Int))
      (x_is_zst Bool)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_callback_identity Int)
      (b_initial_callback_state Int)
      (b_key_result_relation
        (Array Int
          (Array Int Int)))
      (b_key_next_state_relation
        (Array Int
          (Array Int Int)))
      (b_key_panic_relation
        (Array Int
          (Array Int Bool)))
      (b_ord_lt_result_relation
        (Array Int
          (Array Int
            (Array Int
              Bool))))
      (b_ord_lt_next_state_relation
        (Array Int
          (Array Int
            (Array Int
              Int))))
      (b_ord_lt_panic_relation
        (Array Int
          (Array Int
            (Array Int
              Bool))))))))
(declare-datatypes ((Reference 0))
  (((mkReference
      (ref_allocation Int)
      (ref_parent_borrow Int)
      (ref_start Int)
      (ref_span Int)
      (ref_projection_kind Int)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_left_ref Reference)
      (y_pivot_ref Reference)
      (y_right_ref Reference)
      (y_left_len Int)
      (y_pivot_identity Int)
      (y_right_len Int)))))
(declare-datatypes ((State 0))
  (((mkState
      (s_final_sequence (Array Int Int))
      (s_final_allocation Int)
      (s_final_borrow Int)
      (s_final_length Int)
      (s_callback_state Int)
      (s_panicked Bool)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun PositionInRange
  ((position Int) (start Int) (end Int)) Bool
  (and (<= start position) (< position end)))
(define-fun KeyStep
  ((b Boundary)
   (state Int)
   (value Int)
   (key Int)
   (next_state Int)
   (panicked Bool)) Bool
  (and
    (= key
       (select
         (select (b_key_result_relation b) state)
         value))
    (= next_state
       (select
         (select (b_key_next_state_relation b) state)
         value))
    (= panicked
       (select
         (select (b_key_panic_relation b) state)
         value))))
(define-fun OrdLtStep
  ((b Boundary)
   (state Int)
   (left_key Int)
   (right_key Int)
   (is_less Bool)
   (next_state Int)
   (panicked Bool)) Bool
  (and
    (= is_less
       (select
         (select
           (select (b_ord_lt_result_relation b) state)
           left_key)
         right_key))
    (= next_state
       (select
         (select
           (select (b_ord_lt_next_state_relation b) state)
           left_key)
         right_key))
    (= panicked
       (select
         (select
           (select (b_ord_lt_panic_relation b) state)
           left_key)
         right_key))))
(define-fun CallbackTransitionFunctional ((b Boundary)) Bool
  (and
    (forall
      ((state Int)
       (value Int)
       (key1 Int)
       (next_state1 Int)
       (panicked1 Bool)
       (key2 Int)
       (next_state2 Int)
       (panicked2 Bool))
      (=>
        (and
          (KeyStep b state value key1 next_state1 panicked1)
          (KeyStep b state value key2 next_state2 panicked2))
        (and
          (= key1 key2)
          (= next_state1 next_state2)
          (= panicked1 panicked2))))
    (forall
      ((state Int)
       (left_key Int)
       (right_key Int)
       (is_less1 Bool)
       (next_state1 Int)
       (panicked1 Bool)
       (is_less2 Bool)
       (next_state2 Int)
       (panicked2 Bool))
      (=>
        (and
          (OrdLtStep
            b state left_key right_key
            is_less1 next_state1 panicked1)
          (OrdLtStep
            b state left_key right_key
            is_less2 next_state2 panicked2))
        (and
          (= is_less1 is_less2)
          (= next_state1 next_state2)
          (= panicked1 panicked2))))))
(define-fun AdapterNormal
  ((b Boundary)
   (state Int)
   (left Int)
   (right Int)
   (is_less Bool)
   (next_state Int)) Bool
  (exists
    ((left_key Int)
     (after_left Int)
     (right_key Int)
     (after_right Int))
    (and
      (KeyStep
        b
        state
        left
        left_key
        after_left
        false)
      (KeyStep
        b
        after_left
        right
        right_key
        after_right
        false)
      (OrdLtStep
        b
        after_right
        left_key
        right_key
        is_less
        next_state
        false))))
(define-fun AdapterPanic
  ((b Boundary)
   (state Int)
   (left Int)
   (right Int)
   (next_state Int)) Bool
  (or
    (exists ((left_key Int))
      (KeyStep
        b
        state
        left
        left_key
        next_state
        true))
    (exists ((left_key Int) (after_left Int) (right_key Int))
      (and
        (KeyStep
          b
          state
          left
          left_key
          after_left
          false)
        (KeyStep
          b
          after_left
          right
          right_key
          next_state
          true)))
    (exists
      ((left_key Int)
       (after_left Int)
       (right_key Int)
       (after_right Int)
       (is_less Bool))
      (and
        (KeyStep
          b
          state
          left
          left_key
          after_left
          false)
        (KeyStep
          b
          after_left
          right
          right_key
          after_right
          false)
        (OrdLtStep
          b
          after_right
          left_key
          right_key
          is_less
          next_state
          true)))))
(define-fun MayCompareLess
  ((b Boundary) (left Int) (right Int)) Bool
  (exists ((next_state Int))
    (AdapterNormal
      b
      (b_initial_callback_state b)
      left
      right
      true
      next_state)))
(define-fun ContractLeq
  ((b Boundary) (left Int) (right Int)) Bool
  (not (MayCompareLess b right left)))
(define-fun IdentityInInput ((x Input) (identity Int)) Bool
  (or
    (= (select (x_initial_sequence x) 0) identity)
    (= (select (x_initial_sequence x) 1) identity)
    (= (select (x_initial_sequence x) 2) identity)
    (= (select (x_initial_sequence x) 3) identity)))
(define-fun PermutationFromInput
  ((x Input) (s State)) Bool
  (exists ((o0 Int) (o1 Int) (o2 Int) (o3 Int))
    (and
      (PositionInRange o0 0 4)
      (PositionInRange o1 0 4)
      (PositionInRange o2 0 4)
      (PositionInRange o3 0 4)
      (distinct o0 o1 o2 o3)
      (= (select (s_final_sequence s) 0)
         (select (x_initial_sequence x) o0))
      (= (select (s_final_sequence s) 1)
         (select (x_initial_sequence x) o1))
      (= (select (s_final_sequence s) 2)
         (select (x_initial_sequence x) o2))
      (= (select (s_final_sequence s) 3)
         (select (x_initial_sequence x) o3)))))
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
(define-fun InputShapeValid ((x Input)) Bool
  (and
    (> (x_length x) 0)
    (<= 0 (x_index x))
    (< (x_index x) (x_length x))
    (>= (x_allocation x) 0)
    (>= (x_borrow x) 0)))
(define-fun CallbackBoundaryWellFormed
  ((x Input) (b Boundary)) Bool
  (and
    (>= (b_callback_identity b) 0)
    (>= (b_initial_callback_state b) 0)
    (CallbackTransitionFunctional b)
  (exists ((key Int) (key_state Int) (key_panicked Bool))
    (KeyStep
      b
      (b_initial_callback_state b)
      (select (x_initial_sequence x) 0)
      key
      key_state
      key_panicked))
  (exists
    ((left_key Int)
     (right_key Int)
     (is_less Bool)
     (next_state Int)
     (panicked Bool))
    (OrdLtStep
      b
      (b_initial_callback_state b)
      left_key
      right_key
      is_less
      next_state
      panicked))))
(define-fun SequenceAfterInsert
  ((sequence (Array Int Int)) (tail Int) (insertion Int))
  (Array Int Int)
  (ite
    (= tail 1)
    (ite
      (= insertion 0)
      (store
        (store sequence 1 (select sequence 0))
        0
        (select sequence 1))
      sequence)
    (ite
      (= tail 2)
      (ite
        (= insertion 0)
        (store
          (store
            (store sequence 2 (select sequence 1))
            1
            (select sequence 0))
          0
          (select sequence 2))
        (ite
          (= insertion 1)
          (store
            (store sequence 2 (select sequence 1))
            1
            (select sequence 2))
          sequence))
      (ite
        (= insertion 0)
        (store
          (store
            (store
              (store sequence 3 (select sequence 2))
              2
              (select sequence 1))
            1
            (select sequence 0))
          0
          (select sequence 3))
        (ite
          (= insertion 1)
          (store
            (store
              (store sequence 3 (select sequence 2))
              2
              (select sequence 1))
            1
            (select sequence 3))
          (ite
            (= insertion 2)
            (store
              (store sequence 3 (select sequence 2))
              2
              (select sequence 3))
            sequence))))))
(define-fun InsertTailNormal
  ((b Boundary)
   (sequence (Array Int Int))
   (tail Int)
   (state Int)
   (next_sequence (Array Int Int))
   (next_state Int)) Bool
  (or
    (and
      (= tail 1)
      (or
        (and
          (AdapterNormal
            b state (select sequence 1) (select sequence 0)
            false next_state)
          (= next_sequence sequence))
        (and
          (AdapterNormal
            b state (select sequence 1) (select sequence 0)
            true next_state)
          (= next_sequence (SequenceAfterInsert sequence 1 0)))))
    (and
      (= tail 2)
      (or
        (and
          (AdapterNormal
            b state (select sequence 2) (select sequence 1)
            false next_state)
          (= next_sequence sequence))
        (exists ((after_first Int))
          (and
            (AdapterNormal
              b state (select sequence 2) (select sequence 1)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 2) (select sequence 0)
              false next_state)
            (= next_sequence
               (SequenceAfterInsert sequence 2 1))))
        (exists ((after_first Int))
          (and
            (AdapterNormal
              b state (select sequence 2) (select sequence 1)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 2) (select sequence 0)
              true next_state)
            (= next_sequence
               (SequenceAfterInsert sequence 2 0))))))
    (and
      (= tail 3)
      (or
        (and
          (AdapterNormal
            b state (select sequence 3) (select sequence 2)
            false next_state)
          (= next_sequence sequence))
        (exists ((after_first Int))
          (and
            (AdapterNormal
              b state (select sequence 3) (select sequence 2)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 3) (select sequence 1)
              false next_state)
            (= next_sequence
               (SequenceAfterInsert sequence 3 2))))
        (exists ((after_first Int) (after_second Int))
          (and
            (AdapterNormal
              b state (select sequence 3) (select sequence 2)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 3) (select sequence 1)
              true after_second)
            (AdapterNormal
              b after_second (select sequence 3) (select sequence 0)
              false next_state)
            (= next_sequence
               (SequenceAfterInsert sequence 3 1))))
        (exists ((after_first Int) (after_second Int))
          (and
            (AdapterNormal
              b state (select sequence 3) (select sequence 2)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 3) (select sequence 1)
              true after_second)
            (AdapterNormal
              b after_second (select sequence 3) (select sequence 0)
              true next_state)
            (= next_sequence
               (SequenceAfterInsert sequence 3 0))))))))
(define-fun LengthFourInsertionSortNormal
  ((x Input) (b Boundary) (s State)) Bool
  (exists
    ((after_first_sequence (Array Int Int))
     (after_first_state Int)
     (after_second_sequence (Array Int Int))
     (after_second_state Int))
    (and
      (InsertTailNormal
        b
        (x_initial_sequence x)
        1
        (b_initial_callback_state b)
        after_first_sequence
        after_first_state)
      (InsertTailNormal
        b
        after_first_sequence
        2
        after_first_state
        after_second_sequence
        after_second_state)
      (InsertTailNormal
        b
        after_second_sequence
        3
        after_second_state
        (s_final_sequence s)
        (s_callback_state s)))))
(define-fun InsertTailPanic
  ((b Boundary)
   (sequence (Array Int Int))
   (tail Int)
   (state Int)
   (panic_sequence (Array Int Int))
   (panic_state Int)) Bool
  (and
    (<= 1 tail)
    (<= tail 3)
    (or
      (and
        (= panic_sequence sequence)
        (AdapterPanic
          b
          state
          (select sequence tail)
          (select sequence (- tail 1))
          panic_state))
      (and
        (= tail 2)
        (exists ((after_first Int))
          (and
            (AdapterNormal
              b state (select sequence 2) (select sequence 1)
              true after_first)
            (AdapterPanic
              b after_first (select sequence 2) (select sequence 0)
              panic_state)
            (= panic_sequence
               (SequenceAfterInsert sequence 2 1)))))
      (and
        (= tail 3)
        (exists ((after_first Int))
          (and
            (AdapterNormal
              b state (select sequence 3) (select sequence 2)
              true after_first)
            (AdapterPanic
              b after_first (select sequence 3) (select sequence 1)
              panic_state)
            (= panic_sequence
               (SequenceAfterInsert sequence 3 2)))))
      (and
        (= tail 3)
        (exists ((after_first Int) (after_second Int))
          (and
            (AdapterNormal
              b state (select sequence 3) (select sequence 2)
              true after_first)
            (AdapterNormal
              b after_first (select sequence 3) (select sequence 1)
              true after_second)
            (AdapterPanic
              b after_second (select sequence 3) (select sequence 0)
              panic_state)
            (= panic_sequence
               (SequenceAfterInsert sequence 3 1))))))))
(define-fun LengthFourInsertionSortPanic
  ((x Input) (b Boundary) (s State)) Bool
  (or
    (InsertTailPanic
      b
      (x_initial_sequence x)
      1
      (b_initial_callback_state b)
      (s_final_sequence s)
      (s_callback_state s))
    (exists
      ((after_first_sequence (Array Int Int))
       (after_first_state Int))
      (and
        (InsertTailNormal
          b
          (x_initial_sequence x)
          1
          (b_initial_callback_state b)
          after_first_sequence
          after_first_state)
        (InsertTailPanic
          b
          after_first_sequence
          2
          after_first_state
          (s_final_sequence s)
          (s_callback_state s))))
    (exists
      ((after_first_sequence (Array Int Int))
       (after_first_state Int)
       (after_second_sequence (Array Int Int))
       (after_second_state Int))
      (and
        (InsertTailNormal
          b
          (x_initial_sequence x)
          1
          (b_initial_callback_state b)
          after_first_sequence
          after_first_state)
        (InsertTailNormal
          b
          after_first_sequence
          2
          after_first_state
          after_second_sequence
          after_second_state)
        (InsertTailPanic
          b
          after_second_sequence
          3
          after_second_state
          (s_final_sequence s)
          (s_callback_state s))))))
(define-fun NormalReturnTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (not (s_panicked s))
    (>= (b_callback_identity b) 0)
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))))
(define-fun PanicPrefixReachable
  ((x Input) (b Boundary) (s State)) Bool
  (and
    (= (x_length x) 4)
    (= (x_index x) 1)
    (not (x_is_zst x))
    (= (s_final_allocation s) (x_allocation x))
    (= (s_final_borrow s) (x_borrow x))
    (= (s_final_length s) (x_length x))
    (s_panicked s)
    (LengthFourInsertionSortPanic x b s)))
(define-fun PartitionedWindow
  ((b Boundary)
   (sequence (Array Int Int))
   (start Int)
   (pivot Int)
   (end Int)) Bool
  (and
    (= start 0)
    (= pivot 1)
    (= end 4)
    (ContractLeq b (select sequence 0) (select sequence 1))
    (ContractLeq b (select sequence 1) (select sequence 2))
    (ContractLeq b (select sequence 1) (select sequence 3))))
(define-fun BoundsTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (<= 0 (x_index x))
    (< (x_index x) (x_length x))
    (= (y_left_len y) (x_index x))
    (= (y_right_len y) (- (x_length x) (x_index x) 1))
    (not (s_panicked s))
    (>= (b_callback_identity b) 0)))
(define-fun SmallSortTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (x_length x) 4)
    (= (x_index x) 1)
    (not (x_is_zst x))
    (LengthFourInsertionSortNormal x b s)
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))))
(define-fun FinalReturnedSubsliceTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_left_ref y) (LeftReference x))
    (= (y_pivot_ref y) (PivotReference x))
    (= (y_right_ref y) (RightReference x))
    (= (y_left_len y) (x_index x))
    (= (y_right_len y) (- (x_length x) (x_index x) 1))
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (= (s_final_allocation s) (x_allocation x))
    (= (s_final_borrow s) (x_borrow x))
    (= (s_final_length s) (x_length x))
    (>= (s_callback_state s) (b_initial_callback_state b))))
(define-fun ActiveFinalConcatConjunct
  ((x Input)
   (b Boundary)
   (y Output)
   (s State)) Bool
  (and
    (= (y_left_ref y) (LeftReference x))
    (= (y_pivot_ref y) (PivotReference x))
    (= (y_right_ref y) (RightReference x))
    (= (s_final_allocation s) (x_allocation x))
    (= (s_final_borrow s) (x_borrow x))
    (= (s_final_length s)
       (+ (ref_span (y_left_ref y))
          (ref_span (y_pivot_ref y))
          (ref_span (y_right_ref y))))
    (>= (b_callback_identity b) 0)))
(define-fun ActiveLeftLengthConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_left_len y) (x_index x))
    (= (ref_span (y_left_ref y)) (y_left_len y))
    (not (s_panicked s))
    (>= (b_initial_callback_state b) 0)))
(define-fun ActivePivotAtIndexConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (ref_start (y_pivot_ref y)) (x_index x))
    (= (ref_span (y_pivot_ref y)) 1)
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (>= (b_callback_identity b) 0)))
(define-fun ActiveRightLengthConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_right_len y) (- (x_length x) (x_index x) 1))
    (= (ref_span (y_right_ref y)) (y_right_len y))
    (not (s_panicked s))
    (>= (b_initial_callback_state b) 0)))
(define-fun ActivePermutationConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (PermutationFromInput x s)
    (IdentityInInput x (y_pivot_identity y))
    (>= (b_callback_identity b) 0)))
(define-fun ActiveCallbackPartitionConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (PartitionedWindow
      b
      (s_final_sequence s)
      0
      (x_index x)
      (x_length x))
    (IdentityInInput x (y_pivot_identity y))
    (>= (s_callback_state s) (b_initial_callback_state b))))
(define-fun Requires_T ((x Input)) Bool
  (and
    (InputShapeValid x)
    (= (x_length x) 4)
    (= (x_index x) 1)
    (not (x_is_zst x))))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (CallbackBoundaryWellFormed x b))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (BoundsTransition x b y s)
    (SmallSortTransition x b y s)
    (NormalReturnTransition x b y s)
    (FinalReturnedSubsliceTransition x b y s)
    (ActiveFinalConcatConjunct x b y s)
    (ActiveLeftLengthConjunct x b y s)
    (ActivePivotAtIndexConjunct x b y s)
    (ActiveRightLengthConjunct x b y s)
    (ActivePermutationConjunct x b y s)
    (ActiveCallbackPartitionConjunct x b y s)))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and (= (y_left_ref y1) (y_left_ref y2))
       (= (y_pivot_ref y1) (y_pivot_ref y2))
       (= (y_right_ref y1) (y_right_ref y2))
       (= (y_left_len y1) (y_left_len y2))
       (= (y_pivot_identity y1) (y_pivot_identity y2))
       (= (y_right_len y1) (y_right_len y2))
       (= (s_final_sequence s1) (s_final_sequence s2))
       (= (s_final_allocation s1) (s_final_allocation s2))
       (= (s_final_borrow s1) (s_final_borrow s2))
       (= (s_final_length s1) (s_final_length s2))
       (= (s_callback_state s1) (s_callback_state s2))
       (= (s_panicked s1) (s_panicked s2))))
(assert (= x (mkInput 4 1 41 51 (store (store (store (store ((as const (Array Int Int)) 0) 0 10) 1 30) 2 20) 3 40) false)))
(assert (= b (mkBoundary 61 0 (lambda ((state Int))
  (lambda ((value Int)) value)) (lambda ((state Int))
  (lambda ((value Int)) (+ state 1))) (lambda ((state Int))
  (lambda ((value Int)) false)) (lambda ((state Int))
  (lambda ((left_key Int))
    (lambda ((right_key Int)) (< left_key right_key)))) (lambda ((state Int))
  (lambda ((left_key Int))
    (lambda ((right_key Int)) (+ state 1)))) (lambda ((state Int))
  (lambda ((left_key Int))
    (lambda ((right_key Int))
      (and (= state 8) (= left_key 20) (= right_key 10))))))))
(assert (= s1 (mkState (store (store (store (store ((as const (Array Int Int)) 0) 0 10) 1 20) 2 30) 3 40) 41 51 4 9 true)))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (PanicPrefixReachable x b s1))
(check-sat)
