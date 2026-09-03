; Target: core::slice::sort_unstable_by_key
; Model: target-082-key-sort-operational-v1-rust-1.96-complete
; Source: f(left), f(right), K::lt, drop(right K), drop(left K), then
; private-sort completion/unwind and drop(F). All schedules are derived.
(set-logic ALL)
(set-option :produce-models true)

(declare-datatypes ((KOwned 0))
  (((mkKOwned
      (ko_invocation Int)
      (ko_creation_state Int)
      (ko_slot Int)
      (ko_source Int)
      (ko_key Int)))))
(declare-datatypes ((KCallKey 0))
  (((mkKCallKey
      (kc_state Int)
      (kc_slot Int)
      (kc_source Int)
      (kc_interior (Array Int Int))))))
(declare-datatypes ((KOrdKey 0))
  (((mkKOrdKey
      (kord_state Int)
      (kord_left KOwned)
      (kord_right KOwned)
      (kord_interior (Array Int Int))))))
(declare-datatypes ((KDropKey 0))
  (((mkKDropKey
      (kd_state Int)
      (kd_owned KOwned)
      (kd_unwinding Bool)
      (kd_interior (Array Int Int))))))
(declare-datatypes ((KFDropKey 0))
  (((mkKFDropKey
      (kfd_state Int)
      (kfd_unwinding Bool)
      (kfd_interior (Array Int Int))))))
(declare-datatypes ((KPairKey 0))
  (((mkKPairKey (kp_left Int) (kp_right Int)))))
(declare-datatypes ((KBoundary 0))
  (((mkKBoundary
      (kb_initial_state Int)
      (kb_contract_key (Array Int Int))
      (kb_contract_ordering (Array KPairKey Int))
      (kb_key_value (Array KCallKey Int))
      (kb_key_next_state (Array KCallKey Int))
      (kb_key_next_interior (Array KCallKey (Array Int Int)))
      (kb_key_panics (Array KCallKey Bool))
      (kb_ord_is_less (Array KOrdKey Bool))
      (kb_ord_next_state (Array KOrdKey Int))
      (kb_ord_next_interior (Array KOrdKey (Array Int Int)))
      (kb_ord_panics (Array KOrdKey Bool))
      (kb_drop_next_state (Array KDropKey Int))
      (kb_drop_next_interior (Array KDropKey (Array Int Int)))
      (kb_drop_panics (Array KDropKey Bool))
      (kb_f_drop_next_state (Array KFDropKey Int))
      (kb_f_drop_next_interior
        (Array KFDropKey (Array Int Int)))
      (kb_f_drop_panics (Array KFDropKey Bool))
      (kb_interior_at_state (Array Int (Array Int Int)))))))
(declare-datatypes ((KKeyResult 0))
  (((mkKKeyResult
      (kkr_key Int)
      (kkr_state Int)
      (kkr_interior (Array Int Int))
      (kkr_panicked Bool)))))
(declare-datatypes ((KOrdResult 0))
  (((mkKOrdResult
      (kor_less Bool)
      (kor_state Int)
      (kor_interior (Array Int Int))
      (kor_panicked Bool)))))
(declare-datatypes ((KDropResult 0))
  (((mkKDropResult
      (kdr_state Int)
      (kdr_interior (Array Int Int))
      (kdr_panicked Bool)))))
(declare-datatypes ((KAdapterResult 0))
  (((mkKAdapterResult
      (kar_status Int)
      (kar_state Int)
      (kar_interior (Array Int Int))
      (kar_is_less Bool)
      (kar_result_available Bool)
      (kar_key_evaluations Int)
      (kar_ord_evaluations Int)
      (kar_right_drops Int)
      (kar_left_drops Int)
      (kar_event_code Int)
      (kar_has_left Bool)
      (kar_has_right Bool)
      (kar_left_owned KOwned)
      (kar_right_owned KOwned)))))
(declare-datatypes ((KPrivateResult 0))
  (((mkKPrivateResult
      (kpr_sequence (Array Int Int))
      (kpr_state Int)
      (kpr_status Int)))))
(declare-datatypes ((KPublicResult 0))
  (((mkKPublicResult
      (kpub_sequence (Array Int Int))
      (kpub_state Int)
      (kpub_interior (Array Int Int))
      (kpub_status Int)
      (kpub_unit Bool)
      (kpub_panicked Bool)
      (kpub_aborted Bool)
      (kpub_f_drop_invoked Bool)
      (kpub_f_drop_completed Bool)))))

(define-fun KObserveKey
  ((b KBoundary) (state Int) (slot Int) (source Int)
   (interior (Array Int Int))) KKeyResult
  (let ((call (mkKCallKey state slot source interior)))
    (mkKKeyResult
      (select (kb_key_value b) call)
      (select (kb_key_next_state b) call)
      (select (kb_key_next_interior b) call)
      (select (kb_key_panics b) call))))
(define-fun KObserveOrd
  ((b KBoundary) (state Int) (left KOwned) (right KOwned)
   (interior (Array Int Int))) KOrdResult
  (let ((call (mkKOrdKey state left right interior)))
    (mkKOrdResult
      (select (kb_ord_is_less b) call)
      (select (kb_ord_next_state b) call)
      (select (kb_ord_next_interior b) call)
      (select (kb_ord_panics b) call))))
(define-fun KObserveDrop
  ((b KBoundary) (state Int) (owned KOwned) (unwinding Bool)
   (interior (Array Int Int))) KDropResult
  (let ((call (mkKDropKey state owned unwinding interior)))
    (mkKDropResult
      (select (kb_drop_next_state b) call)
      (select (kb_drop_next_interior b) call)
      (select (kb_drop_panics b) call))))
(define-fun KObserveFDrop
  ((b KBoundary) (state Int) (unwinding Bool)
   (interior (Array Int Int))) KDropResult
  (let ((call (mkKFDropKey state unwinding interior)))
    (mkKDropResult
      (select (kb_f_drop_next_state b) call)
      (select (kb_f_drop_next_interior b) call)
      (select (kb_f_drop_panics b) call))))

(define-fun KCleanupLeftAfterRightKeyPanic
  ((b KBoundary) (left KOwned) (state Int)
   (interior (Array Int Int))) KAdapterResult
  (let ((left_drop (KObserveDrop b state left true interior)))
    (mkKAdapterResult
      (ite (kdr_panicked left_drop) 2 1)
      (kdr_state left_drop)
      (kdr_interior left_drop)
      false false 2 0 0 1
      (ite (kdr_panicked left_drop) 1219 1215)
      true false left left)))

(define-fun KCleanupTwo
  ((b KBoundary) (left KOwned) (right KOwned) (state Int)
   (interior (Array Int Int)) (already_unwinding Bool)
   (resolved_less Bool)) KAdapterResult
  (let ((right_drop
          (KObserveDrop b state right already_unwinding interior)))
    (ite
      (and already_unwinding (kdr_panicked right_drop))
      (mkKAdapterResult
        2 (kdr_state right_drop) (kdr_interior right_drop)
        false false 2 1 1 0 12349 true true left right)
      (let ((unwinding
              (or already_unwinding (kdr_panicked right_drop))))
        (let ((left_drop
                (KObserveDrop
                  b
                  (kdr_state right_drop)
                  left
                  unwinding
                  (kdr_interior right_drop))))
          (let ((status
                  (ite
                    (kdr_panicked left_drop)
                    (ite unwinding 2 1)
                    (ite unwinding 1 0))))
            (mkKAdapterResult
              status
              (kdr_state left_drop)
              (kdr_interior left_drop)
              (and (= status 0) resolved_less)
              (= status 0)
              2 1 1 1
              (ite (= status 0) 12345
                (ite (= status 1) 12347 12349))
              true true left right)))))))

(define-fun SourceKeyAdapter
  ((b KBoundary) (state Int) (left_source Int) (right_source Int)
   (interior (Array Int Int)) (invocation Int)) KAdapterResult
  (let ((left_key (KObserveKey b state 0 left_source interior)))
    (let ((left_owned
            (mkKOwned
              invocation state 0 left_source (kkr_key left_key))))
      (ite
        (kkr_panicked left_key)
        (mkKAdapterResult
          1 (kkr_state left_key) (kkr_interior left_key)
          false false 1 0 0 0 19 false false
          left_owned left_owned)
        (let ((right_key
                (KObserveKey
                  b
                  (kkr_state left_key)
                  1
                  right_source
                  (kkr_interior left_key))))
          (let ((right_owned
                  (mkKOwned
                    invocation
                    (kkr_state left_key)
                    1
                    right_source
                    (kkr_key right_key))))
            (ite
              (kkr_panicked right_key)
              (KCleanupLeftAfterRightKeyPanic
                b left_owned (kkr_state right_key)
                (kkr_interior right_key))
              (let ((ord
                      (KObserveOrd
                        b
                        (kkr_state right_key)
                        left_owned
                        right_owned
                        (kkr_interior right_key))))
                (KCleanupTwo
                  b left_owned right_owned
                  (kor_state ord)
                  (kor_interior ord)
                  (kor_panicked ord)
                  (kor_less ord))))))))))

(define-fun IndependentCleanupLeftAfterRightKeyPanic
  ((b KBoundary) (left KOwned) (state Int)
   (interior (Array Int Int))) KAdapterResult
  (let ((left_drop (KObserveDrop b state left true interior)))
    (mkKAdapterResult
      (ite (kdr_panicked left_drop) 2 1)
      (kdr_state left_drop)
      (kdr_interior left_drop)
      false false 2 0 0 1
      (ite (kdr_panicked left_drop) 1219 1215)
      true false left left)))

(define-fun IndependentCleanupTwo
  ((b KBoundary) (left KOwned) (right KOwned) (state Int)
   (interior (Array Int Int)) (already_unwinding Bool)
   (resolved_less Bool)) KAdapterResult
  (let ((right_drop
          (KObserveDrop b state right already_unwinding interior)))
    (ite
      (and already_unwinding (kdr_panicked right_drop))
      (mkKAdapterResult
        2 (kdr_state right_drop) (kdr_interior right_drop)
        false false 2 1 1 0 12349 true true left right)
      (let ((unwinding
              (or already_unwinding (kdr_panicked right_drop))))
        (let ((left_drop
                (KObserveDrop
                  b
                  (kdr_state right_drop)
                  left
                  unwinding
                  (kdr_interior right_drop))))
          (let ((status
                  (ite
                    (kdr_panicked left_drop)
                    (ite unwinding 2 1)
                    (ite unwinding 1 0))))
            (mkKAdapterResult
              status
              (kdr_state left_drop)
              (kdr_interior left_drop)
              (and (= status 0) resolved_less)
              (= status 0)
              2 1 1 1
              (ite (= status 0) 12345
                (ite (= status 1) 12347 12349))
              true true left right)))))))

(define-fun IndependentKeyAdapter
  ((b KBoundary) (state Int) (left_source Int) (right_source Int)
   (interior (Array Int Int)) (invocation Int)) KAdapterResult
  (let ((left_key (KObserveKey b state 0 left_source interior)))
    (let ((left_owned
            (mkKOwned
              invocation state 0 left_source (kkr_key left_key))))
      (ite
        (kkr_panicked left_key)
        (mkKAdapterResult
          1 (kkr_state left_key) (kkr_interior left_key)
          false false 1 0 0 0 19 false false
          left_owned left_owned)
        (let ((right_key
                (KObserveKey
                  b
                  (kkr_state left_key)
                  1
                  right_source
                  (kkr_interior left_key))))
          (let ((right_owned
                  (mkKOwned
                    invocation
                    (kkr_state left_key)
                    1
                    right_source
                    (kkr_key right_key))))
            (ite
              (kkr_panicked right_key)
              (IndependentCleanupLeftAfterRightKeyPanic
                b left_owned (kkr_state right_key)
                (kkr_interior right_key))
              (let ((ord
                      (KObserveOrd
                        b
                        (kkr_state right_key)
                        left_owned
                        right_owned
                        (kkr_interior right_key))))
                (IndependentCleanupTwo
                  b left_owned right_owned
                  (kor_state ord)
                  (kor_interior ord)
                  (kor_panicked ord)
                  (kor_less ord))))))))))

(define-fun SourcePublicFinish082
  ((b KBoundary) (private KPrivateResult)
   (interior (Array Int Int))) KPublicResult
  (ite
    (= (kpr_status private) 2)
    (mkKPublicResult
      (kpr_sequence private) (kpr_state private) interior
      2 false false true false false)
    (let ((unwinding (= (kpr_status private) 1)))
      (let ((d
              (KObserveFDrop
                b (kpr_state private) unwinding interior)))
        (let ((status
                (ite
                  (kdr_panicked d)
                  (ite unwinding 2 1)
                  (ite unwinding 1 0))))
          (mkKPublicResult
            (kpr_sequence private)
            (kdr_state d)
            (kdr_interior d)
            status
            (= status 0)
            (= status 1)
            (= status 2)
            true
            (not (kdr_panicked d))))))))

(define-fun IndependentPublicFinish082
  ((b KBoundary) (private KPrivateResult)
   (interior (Array Int Int))) KPublicResult
  (ite
    (= (kpr_status private) 2)
    (mkKPublicResult
      (kpr_sequence private) (kpr_state private) interior
      2 false false true false false)
    (let ((unwinding (= (kpr_status private) 1)))
      (let ((d
              (KObserveFDrop
                b (kpr_state private) unwinding interior)))
        (let ((status
                (ite
                  (kdr_panicked d)
                  (ite unwinding 2 1)
                  (ite unwinding 1 0))))
          (mkKPublicResult
            (kpr_sequence private)
            (kdr_state d)
            (kdr_interior d)
            status
            (= status 0)
            (= status 1)
            (= status 2)
            true
            (not (kdr_panicked d))))))))
(declare-const boundary KBoundary)
(declare-const interior (Array Int Int))
(define-fun adapter () KAdapterResult
  (SourceKeyAdapter boundary 0 10 20 interior 0))
(define-fun private () KPrivateResult
  (mkKPrivateResult
    ((as const (Array Int Int)) 0)
    (kar_state adapter)
    (kar_status adapter)))
(define-fun public () KPublicResult
  (SourcePublicFinish082 boundary private (kar_interior adapter)))
(assert (and (= (kar_status adapter) 0) (= (kar_event_code adapter) 12345) (= (kar_key_evaluations adapter) 2) (= (kar_ord_evaluations adapter) 1) (= (kar_right_drops adapter) 1) (= (kar_left_drops adapter) 1)))
(check-sat-using (then ctx-solver-simplify smt))
