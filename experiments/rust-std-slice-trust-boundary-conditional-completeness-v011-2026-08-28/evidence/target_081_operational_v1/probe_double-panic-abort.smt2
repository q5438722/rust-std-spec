; Target: core::slice::sort_unstable_by
; Model: target-081-operational-v1-rust-1.96-complete
; Source: compare(a,b) is evaluated once; successful Ordering is then tested
; against Ordering::Less. Comparator results, closure state, externally
; observable element interior state, panic, and Drop effects are the only
; admitted callback observations.
(set-logic ALL)
(set-option :produce-models true)
(declare-datatypes ((CallKey 0))
  (((mkCallKey (call_state Int) (call_left Int) (call_right Int)))))
(declare-datatypes ((DropKey 0))
  (((mkDropKey (drop_state Int) (drop_unwinding Bool)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_ordering (Array CallKey Int))
      (b_next_state (Array CallKey Int))
      (b_next_interior (Array CallKey (Array Int Int)))
      (b_panics (Array CallKey Bool))
      (b_drop_next_state (Array DropKey Int))
      (b_drop_next_interior (Array DropKey (Array Int Int)))
      (b_drop_panics (Array DropKey Bool))))))
(declare-datatypes ((AdapterResult 0))
  (((mkAdapterResult
      (ar_ordering Int)
      (ar_state Int)
      (ar_interior (Array Int Int))
      (ar_panicked Bool)
      (ar_callback_evaluations Int)
      (ar_less_tested Bool)
      (ar_is_less Bool)
      (ar_observation Int)))))
(declare-datatypes ((PrivateResult 0))
  (((mkPrivateResult
      (pr_sequence (Array Int Int))
      (pr_state Int)
      (pr_interior (Array Int Int))
      (pr_status Int)))))
(declare-datatypes ((PublicResult 0))
  (((mkPublicResult
      (r_sequence (Array Int Int))
      (r_state Int)
      (r_interior (Array Int Int))
      (r_panicked Bool)
      (r_aborted Bool)
      (r_terminal Bool)
      (r_status Int)
      (r_unit Bool)
      (r_drop_invoked Bool)
      (r_drop_completed Bool)))))

(define-fun BoundaryOrdering
  ((b Boundary) (state Int) (left Int) (right Int)) Int
  (select (b_ordering b) (mkCallKey state left right)))
(define-fun BoundaryNextState
  ((b Boundary) (state Int) (left Int) (right Int)) Int
  (select (b_next_state b) (mkCallKey state left right)))
(define-fun BoundaryNextInterior
  ((b Boundary) (state Int) (left Int) (right Int)) (Array Int Int)
  (select (b_next_interior b) (mkCallKey state left right)))
(define-fun BoundaryPanics
  ((b Boundary) (state Int) (left Int) (right Int)) Bool
  (select (b_panics b) (mkCallKey state left right)))
(define-fun ComparatorObservation
  ((b Boundary) (state Int) (left Int) (right Int)) Int
  (BoundaryOrdering b state left right))
(define-fun BoundaryWellFormed ((b Boundary)) Bool
  (forall ((state Int) (left Int) (right Int))
    (let ((ordering (BoundaryOrdering b state left right)))
      (or (= ordering -1) (= ordering 0) (= ordering 1)))))

(define-fun SourceOrderingAdapter
  ((b Boundary) (state Int) (left Int) (right Int)) AdapterResult
  (let ((ordering (BoundaryOrdering b state left right))
        (next_state (BoundaryNextState b state left right))
        (next_interior (BoundaryNextInterior b state left right))
        (panics (BoundaryPanics b state left right)))
    (mkAdapterResult
      ordering
      next_state
      next_interior
      panics
      1
      (not panics)
      (and (not panics) (= ordering -1))
      (ComparatorObservation b state left right))))
(define-fun IndependentOrderingAdapter
  ((b Boundary) (state Int) (left Int) (right Int)) AdapterResult
  (let ((observed (select (b_ordering b) (mkCallKey state left right)))
        (transitioned
          (select (b_next_state b) (mkCallKey state left right)))
        (interior_transitioned
          (select (b_next_interior b) (mkCallKey state left right)))
        (raised (select (b_panics b) (mkCallKey state left right))))
    (mkAdapterResult
      observed
      transitioned
      interior_transitioned
      raised
      1
      (not raised)
      (and (not raised) (= observed -1))
      observed)))

(define-fun SourcePublicFinish
  ((b Boundary) (private PrivateResult)) PublicResult
  (ite
    (= (pr_status private) 2)
    (mkPublicResult
      (pr_sequence private) (pr_state private) (pr_interior private)
      false true true 2 false false false)
    (let ((unwinding (= (pr_status private) 1))
          (drop_next
            (select
              (b_drop_next_state b)
              (mkDropKey
                (pr_state private)
                (= (pr_status private) 1))))
          (drop_next_interior
            (select
              (b_drop_next_interior b)
              (mkDropKey
                (pr_state private)
                (= (pr_status private) 1))))
          (drop_panics
            (select
              (b_drop_panics b)
              (mkDropKey
                (pr_state private)
                (= (pr_status private) 1)))))
      (let ((status
              (ite drop_panics
                (ite unwinding 2 1)
                (ite unwinding 1 0))))
        (mkPublicResult
          (pr_sequence private)
          drop_next
          drop_next_interior
          (= status 1)
          (= status 2)
          true
          status
          (= status 0)
          true
          (not drop_panics))))))
(define-fun IndependentPublicFinish
  ((b Boundary) (private PrivateResult)) PublicResult
  (ite
    (= (pr_status private) 2)
    (mkPublicResult
      (pr_sequence private) (pr_state private) (pr_interior private)
      false true true 2 false false false)
    (let ((was_unwinding (= (pr_status private) 1)))
      (let ((after_drop
              (select
                (b_drop_next_state b)
                (mkDropKey (pr_state private) was_unwinding)))
            (interior_after_drop
              (select
                (b_drop_next_interior b)
                (mkDropKey (pr_state private) was_unwinding)))
            (drop_raised
              (select
                (b_drop_panics b)
                (mkDropKey (pr_state private) was_unwinding))))
        (let ((terminal_status
                (ite drop_raised
                  (ite was_unwinding 2 1)
                  (ite was_unwinding 1 0))))
          (mkPublicResult
            (pr_sequence private)
            after_drop
            interior_after_drop
            (= terminal_status 1)
            (= terminal_status 2)
            true
            terminal_status
            (= terminal_status 0)
            true
            (not drop_raised)))))))
(define-fun fixture () Boundary
  (mkBoundary
    ((as const (Array CallKey Int)) -1)
    ((as const (Array CallKey Int)) 8)
    ((as const (Array CallKey (Array Int Int)))
      ((as const (Array Int Int)) 13))
    ((as const (Array CallKey Bool)) true)
    ((as const (Array DropKey Int)) 9)
    ((as const (Array DropKey (Array Int Int)))
      ((as const (Array Int Int)) 17))
    ((as const (Array DropKey Bool)) true)))
(define-fun adapter () AdapterResult
  (SourceOrderingAdapter fixture 7 1 2))
(define-fun private () PrivateResult
  (mkPrivateResult
    ((as const (Array Int Int)) 0)
    8
    ((as const (Array Int Int)) 13)
    1))
(define-fun public () PublicResult
  (SourcePublicFinish fixture private))
(assert (r_aborted public))
(assert (= (r_status public) 2))
(check-sat-using (then ctx-solver-simplify smt))
