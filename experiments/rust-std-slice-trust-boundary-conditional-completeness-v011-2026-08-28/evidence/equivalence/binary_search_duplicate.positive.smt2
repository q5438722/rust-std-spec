; Reviewed input: [0, 1a, 1b, 2], searched key: 1.
; Rust 1.96 docs permit either matching duplicate index.
(set-logic QF_LIA)
(declare-const first Int)
(declare-const second Int)
(define-fun Matches ((index Int)) Bool (or (= index 1) (= index 2)))
(define-fun MatchingIndexEquivalent ((left Int) (right Int)) Bool
  (and (Matches left) (Matches right)))
(assert (= first 1))
(assert (= second 2))
(assert (not (= first second)))
(assert (and (Matches first) (Matches second)))
(check-sat)
(get-model)
