(set-logic ALL)
(declare-datatypes ((Input 0)) (((mkInput (x_value Int)))))
(declare-datatypes ((Boundary 0)) (((mkBoundary (b_callback_value Int)))))
(declare-datatypes ((Output 0)) (((mkOutput (y_value Int)))))
(declare-datatypes ((State 0)) (((mkState (s_value Int)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun CallbackStep ((x Input) (b Boundary)) Int
  (+ (x_value x) (b_callback_value b)))
(define-fun Requires_T ((x Input)) Bool true)
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (>= (b_callback_value b) 0))
(define-fun TargetDefinition_T ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (= (y_value y) (CallbackStep x b))
       (= (s_value s) (x_value x))))
(define-fun Spec_T ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and (= (y_value y1) (y_value y2))
       (= (s_value s1) (s_value s2))))
(assert
  (not
    (=>
      (and (Requires_T x)
           (Boundary_T x b)
           (Spec_T x b y1 s1)
           (Spec_T x b y2 s2))
      (Equivalent_T x b y1 s1 y2 s2))))
(check-sat)
