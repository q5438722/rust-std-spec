; Reviewed input identities 10 and 11 have key 1; identity 20 has key 2.
; Rust 1.96 unstable-sort docs permit reordering equal-key identities only.
; Identity 12 is foreign but deliberately has key 1, so key equality alone
; cannot establish equivalence.
(set-logic QF_AUFLIA)
(declare-const base (Array Int Int))
(define-fun Key ((identity Int)) Int (ite (= identity 20) 2 1))
(define-fun output1 () (Array Int Int)
  (store (store (store base 0 10) 1 11) 2 20))
(define-fun output2 () (Array Int Int)
  (store (store (store base 0 11) 1 10) 2 20))
(define-fun ElementMultiplicity
  ((output (Array Int Int)) (identity Int)) Int
  (+ (ite (= (select output 0) identity) 1 0)
     (ite (= (select output 1) identity) 1 0)
     (ite (= (select output 2) identity) 1 0)))
(define-fun SameElementMultiset
  ((left (Array Int Int)) (right (Array Int Int))) Bool
  (and
    (= (ElementMultiplicity left (select left 0))
       (ElementMultiplicity right (select left 0)))
    (= (ElementMultiplicity left (select left 1))
       (ElementMultiplicity right (select left 1)))
    (= (ElementMultiplicity left (select left 2))
       (ElementMultiplicity right (select left 2)))
    (= (ElementMultiplicity left (select right 0))
       (ElementMultiplicity right (select right 0)))
    (= (ElementMultiplicity left (select right 1))
       (ElementMultiplicity right (select right 1)))
    (= (ElementMultiplicity left (select right 2))
       (ElementMultiplicity right (select right 2)))))
(define-fun EqualKeyEquivalent
  ((left (Array Int Int)) (right (Array Int Int))) Bool
  (and (SameElementMultiset left right)
       (= (Key (select left 0)) (Key (select right 0)))
       (= (Key (select left 1)) (Key (select right 1)))
       (= (Key (select left 2)) (Key (select right 2)))))
(assert (not (= output1 output2)))
(assert (EqualKeyEquivalent output1 output2))
(check-sat)
(get-model)
