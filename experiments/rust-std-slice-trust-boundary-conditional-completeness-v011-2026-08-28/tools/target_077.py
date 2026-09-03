#!/usr/bin/env python3
"""Source-backed conditional-completeness model for select_nth_unstable."""

from __future__ import annotations

from collections import Counter
from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::select_nth_unstable"
INPUT_ORDER = "77"
ARTIFACT_ID = "077_core_slice_select_nth_unstable"
ACTIVE_CONTRACT_SHA256 = (
    "e570c36bf97546100d3408a95ea9c5f821ba0aed6ebe0e63ef6358d7d713fdaf"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<T: core::cmp::Ord>[ "
    "<[T]>::select_nth_unstable ]( slice: &mut [T], index: usize, ) -> "
    "(ret: (&mut [T], &mut T, &mut [T])) requires index < "
    "old(slice)@.len(), ensures final(slice)@ == final(ret.0)@ + "
    "seq![*final(ret.1)] + final(ret.2)@, final(ret.0)@.len() == index, "
    "*final(ret.1) == final(slice)@[index as int], final(ret.2)@.len() == "
    "old(slice)@.len() - (index as int) - 1, "
    "slice_permutation(old(slice)@, final(slice)@), "
    "slice_select_partition_ord(final(ret.0)@, *final(ret.1), "
    "final(ret.2)@), ;"
)

TARGET_SOURCE = "core/src/slice/mod.rs:3516-3521"
PUBLIC_DOCS = "core/src/slice/mod.rs:3461-3513"
SELECT_SOURCE = "core/src/slice/sort/select.rs:17-307"
PARTITION_SOURCE = "core/src/slice/sort/unstable/quicksort.rs:93-137"
ORD_SOURCE = "core/src/cmp.rs:733-761"
VOCABULARY_SOURCE = "specs/slice_shared_vocabulary.rs:316-379,759-770"

ADMITTED_TRUST_SITES = ("TS-077-D003",)
EXCLUDED_RETAINED_TRUST_SITES = ("TS-077-D002", "TS-077-E001")
CONTEXT_ONLY_TRUST_SITES = ("TS-077-D001", "TS-077-C001")
ALL_AUDITED_TRUST_SITES = (
    "TS-077-D001",
    "TS-077-D002",
    "TS-077-D003",
    "TS-077-C001",
    "TS-077-E001",
)
REPLACEMENT_ID = "RB-077-SOURCE-REACHABLE-INTROSELECT-TRANSITIONS"

PRIMARY = "completeness-modulo-reviewed-selection-equivalence"
EXACT_OUTPUT = "exact-output-and-final-state-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

OUTPUT_FIELDS = (
    ("y_left_ref", "Reference"),
    ("y_pivot_ref", "Reference"),
    ("y_right_ref", "Reference"),
    ("y_left_len", "Int"),
    ("y_pivot_identity", "Int"),
    ("y_pivot_class", "Int"),
    ("y_right_len", "Int"),
)
STATE_FIELDS = (
    ("s_final_sequence", "Array Int Int"),
    ("s_final_identity_multiplicity", "Array Int Int"),
    ("s_left_class_multiplicity", "Array Int Int"),
    ("s_right_class_multiplicity", "Array Int Int"),
    ("s_final_allocation", "Int"),
    ("s_final_borrow", "Int"),
    ("s_final_length", "Int"),
)
SOURCE_TRANSITIONS = (
    "BoundsTransition",
    "OrdObservationTransition",
    "ZstTransition",
    "MinMaxScanTransition",
    "SwapPermutationTransition",
    "PartitionTransition",
    "RecursiveLoopOrFallbackTransition",
    "FinalReturnedSubsliceTransition",
)
ACTIVE_CONJUNCTS = (
    "ActiveFinalConcatConjunct",
    "ActiveLeftLengthConjunct",
    "ActivePivotAtIndexConjunct",
    "ActiveRightLengthConjunct",
    "ActivePermutationConjunct",
    "ActiveOrdPartitionConjunct",
)


def _equivalence_body(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        equalities = [
            f"(= ({selector} y1) ({selector} y2))"
            for selector, _ in OUTPUT_FIELDS
        ]
        equalities.extend(
            f"(= ({selector} s1) ({selector} s2))"
            for selector, _ in STATE_FIELDS
        )
        return "  (and " + "\n       ".join(equalities) + "))"
    return """\
  (ReviewedSelectionEquivalent x b y1 s1 y2 s2))"""


def _model_prefix() -> str:
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Rust target: {TARGET_SOURCE}
; Public docs: {PUBLIC_DOCS}
; Private selection source: {SELECT_SOURCE}
; Partition source: {PARTITION_SOURCE}
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_length Int)
      (x_index Int)
      (x_allocation Int)
      (x_borrow Int)
      (x_initial_sequence (Array Int Int))
      (x_identity_multiplicity (Array Int Int))
      (x_class_multiplicity (Array Int Int))
      (x_less_count (Array Int Int))
      (x_equal_count (Array Int Int))
      (x_greater_count (Array Int Int))
      (x_is_zst Bool)
      (x_ord_identity Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_ord_identity Int)
      (b_ord_class (Array Int Int))))))
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
      (y_pivot_class Int)
      (y_right_len Int)))))
(declare-datatypes ((State 0))
  (((mkState
      (s_final_sequence (Array Int Int))
      (s_final_identity_multiplicity (Array Int Int))
      (s_left_class_multiplicity (Array Int Int))
      (s_right_class_multiplicity (Array Int Int))
      (s_final_allocation Int)
      (s_final_borrow Int)
      (s_final_length Int)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun InClassDomain ((x Input) (class Int)) Bool
  (and (<= 0 class) (< class (x_length x))))
(define-fun ObservedClass
  ((b Boundary) (identity Int)) Int
  (select (b_ord_class b) identity))
(define-fun PositionInRange
  ((position Int) (start Int) (end Int)) Bool
  (and (<= start position) (< position end)))
(define-fun-rec IdentityCountThrough
  ((sequence (Array Int Int)) (count Int) (identity Int)) Int
  (ite
    (<= count 0)
    0
    (let ((position (- count 1)))
      (+ (IdentityCountThrough sequence position identity)
         (ite (= (select sequence position) identity) 1 0)))))
(define-fun-rec ClassCountThrough
  ((sequence (Array Int Int))
   (classes (Array Int Int))
   (count Int)
   (class Int)) Int
  (ite
    (<= count 0)
    0
    (let ((position (- count 1)))
      (+ (ClassCountThrough sequence classes position class)
         (ite
           (= (select classes (select sequence position)) class)
           1
           0)))))
(define-fun-rec LessCountThrough
  ((sequence (Array Int Int))
   (classes (Array Int Int))
   (count Int)
   (class Int)) Int
  (ite
    (<= count 0)
    0
    (let ((position (- count 1)))
      (+ (LessCountThrough sequence classes position class)
         (ite
           (< (select classes (select sequence position)) class)
           1
           0)))))
(define-fun-rec GreaterCountThrough
  ((sequence (Array Int Int))
   (classes (Array Int Int))
   (count Int)
   (class Int)) Int
  (ite
    (<= count 0)
    0
    (let ((position (- count 1)))
      (+ (GreaterCountThrough sequence classes position class)
         (ite
           (> (select classes (select sequence position)) class)
           1
           0)))))
(define-fun SequenceIdentityMultiplicity
  ((sequence (Array Int Int)) (length Int)) (Array Int Int)
  (lambda ((identity Int))
    (IdentityCountThrough sequence length identity)))
(define-fun SequenceClassMultiplicity
  ((sequence (Array Int Int))
   (classes (Array Int Int))
   (length Int)) (Array Int Int)
  (lambda ((class Int))
    (ClassCountThrough sequence classes length class)))
(define-fun SequenceLessCounts
  ((sequence (Array Int Int))
   (classes (Array Int Int))
   (length Int)) (Array Int Int)
  (lambda ((class Int))
    (LessCountThrough sequence classes length class)))
(define-fun SequenceGreaterCounts
  ((sequence (Array Int Int))
   (classes (Array Int Int))
   (length Int)) (Array Int Int)
  (lambda ((class Int))
    (GreaterCountThrough sequence classes length class)))
(define-fun InputIdentityMultiplicity
  ((x Input)) (Array Int Int)
  (SequenceIdentityMultiplicity
    (x_initial_sequence x)
    (x_length x)))
(define-fun InputClassMultiplicity
  ((x Input) (b Boundary)) (Array Int Int)
  (SequenceClassMultiplicity
    (x_initial_sequence x)
    (b_ord_class b)
    (x_length x)))
(define-fun InputLessCounts
  ((x Input) (b Boundary)) (Array Int Int)
  (SequenceLessCounts
    (x_initial_sequence x)
    (b_ord_class b)
    (x_length x)))
(define-fun InputGreaterCounts
  ((x Input) (b Boundary)) (Array Int Int)
  (SequenceGreaterCounts
    (x_initial_sequence x)
    (b_ord_class b)
    (x_length x)))
(define-fun FinalIdentityMultiplicity
  ((x Input) (s State)) (Array Int Int)
  (SequenceIdentityMultiplicity
    (s_final_sequence s)
    (x_length x)))
(define-fun FinalLeftClassMultiplicity
  ((x Input) (b Boundary) (s State)) (Array Int Int)
  (SequenceClassMultiplicity
    (s_final_sequence s)
    (b_ord_class b)
    (x_index x)))
(define-fun FinalRightClassMultiplicity
  ((x Input) (b Boundary) (s State)) (Array Int Int)
  (lambda ((class Int))
    (- (ClassCountThrough
         (s_final_sequence s)
         (b_ord_class b)
         (x_length x)
         class)
       (ClassCountThrough
         (s_final_sequence s)
         (b_ord_class b)
         (+ (x_index x) 1)
         class))))
(define-fun InputShapeValid ((x Input)) Bool
  (and
    (> (x_length x) 0)
    (<= 0 (x_index x))
    (< (x_index x) (x_length x))
    (>= (x_allocation x) 0)
    (>= (x_borrow x) 0)
    (>= (x_ord_identity x) 0)))
(define-fun RankSelected
  ((x Input) (class Int)) Bool
  (and
    (InClassDomain x class)
    (<= (select (x_less_count x) class) (x_index x))
    (< (x_index x)
       (+ (select (x_less_count x) class)
          (select (x_equal_count x) class)))))
(define-fun RankSummaryUnique ((x Input)) Bool
  (forall ((first_class Int) (second_class Int))
    (=>
      (and
        (RankSelected x first_class)
        (RankSelected x second_class))
      (= first_class second_class))))
(define-fun InputSummaryValid
  ((x Input) (b Boundary)) Bool
  (and
    (= (x_identity_multiplicity x)
       (InputIdentityMultiplicity x))
    (= (x_class_multiplicity x)
       (InputClassMultiplicity x b))
    (= (x_less_count x)
       (InputLessCounts x b))
    (= (x_equal_count x)
       (InputClassMultiplicity x b))
    (= (x_greater_count x)
       (InputGreaterCounts x b))
    (forall ((position Int))
      (=>
        (PositionInRange position 0 (x_length x))
        (InClassDomain
          x
          (ObservedClass
            b
            (select (x_initial_sequence x) position)))))
    (RankSummaryUnique x)))
(define-fun StateSummaryValid
  ((x Input) (b Boundary) (s State)) Bool
  (and
    (= (s_final_identity_multiplicity s)
       (FinalIdentityMultiplicity x s))
    (= (s_left_class_multiplicity s)
       (FinalLeftClassMultiplicity x b s))
    (= (s_right_class_multiplicity s)
       (FinalRightClassMultiplicity x b s))))
(define-fun ExpectedLeftClassCount
  ((x Input) (pivot_class Int) (class Int)) Int
  (ite
    (< class pivot_class)
    (select (x_class_multiplicity x) class)
    (ite
      (= class pivot_class)
      (- (x_index x) (select (x_less_count x) pivot_class))
      0)))
(define-fun ExpectedRightClassCount
  ((x Input) (pivot_class Int) (class Int)) Int
  (ite
    (> class pivot_class)
    (select (x_class_multiplicity x) class)
    (ite
      (= class pivot_class)
      (- (select (x_equal_count x) pivot_class)
         (- (x_index x) (select (x_less_count x) pivot_class))
         1)
      0)))
(define-fun ExpectedLeftClassMultiplicity
  ((x Input) (pivot_class Int)) (Array Int Int)
  (lambda ((class Int))
    (ExpectedLeftClassCount x pivot_class class)))
(define-fun ExpectedRightClassMultiplicity
  ((x Input) (pivot_class Int)) (Array Int Int)
  (lambda ((class Int))
    (ExpectedRightClassCount x pivot_class class)))
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
(define-fun WindowValid
  ((x Input) (start Int) (end Int)) Bool
  (and
    (<= 0 start)
    (< start end)
    (<= end (x_length x))
    (PositionInRange (x_index x) start end)))
(define-fun PartitionedWindow
  ((b Boundary)
   (sequence (Array Int Int))
   (start Int)
   (pivot Int)
   (end Int)) Bool
  (and
    (PositionInRange pivot start end)
    (forall ((position Int))
      (=>
        (PositionInRange position start pivot)
        (<=
          (ObservedClass b (select sequence position))
          (ObservedClass b (select sequence pivot)))))
    (forall ((position Int))
      (=>
        (PositionInRange position (+ pivot 1) end)
        (>=
          (ObservedClass b (select sequence position))
          (ObservedClass b (select sequence pivot)))))))
(define-fun SortedWindow
  ((b Boundary)
   (sequence (Array Int Int))
   (start Int)
   (end Int)) Bool
  (forall ((lower Int) (upper Int))
    (=>
      (and
        (PositionInRange lower start end)
        (PositionInRange upper start end)
        (< lower upper))
      (<=
        (ObservedClass b (select sequence lower))
        (ObservedClass b (select sequence upper))))))
(define-fun MainNarrowingStep
  ((x Input)
   (b Boundary)
   (s State)
   (starts (Array Int Int))
   (ends (Array Int Int))
   (pivots (Array Int Int))
   (step Int)) Bool
  (let ((start (select starts step))
        (end (select ends step))
        (pivot (select pivots step))
        (next_start (select starts (+ step 1)))
        (next_end (select ends (+ step 1))))
    (and
      (WindowValid x start end)
      (> (- end start) 16)
      (PositionInRange pivot start end)
      (not (= pivot (x_index x)))
      (PartitionedWindow b (s_final_sequence s) start pivot end)
      (= next_start
         (ite (< pivot (x_index x)) (+ pivot 1) start))
      (= next_end
         (ite (< pivot (x_index x)) end pivot))
      (WindowValid x next_start next_end)
      (< (- next_end next_start) (- end start)))))
(define-fun-rec MainNarrowingSteps
  ((x Input)
   (b Boundary)
   (s State)
   (initial_start Int)
   (initial_end Int)
   (starts (Array Int Int))
   (ends (Array Int Int))
   (pivots (Array Int Int))
   (count Int)) Bool
  (ite
    (<= count 0)
    (and
      (= (select starts 0) initial_start)
      (= (select ends 0) initial_end)
      (WindowValid x initial_start initial_end))
    (let ((step (- count 1)))
      (and
        (MainNarrowingSteps
          x b s initial_start initial_end starts ends pivots step)
        (MainNarrowingStep x b s starts ends pivots step)))))
(define-fun FallbackNarrowingStep
  ((x Input)
   (b Boundary)
   (s State)
   (starts (Array Int Int))
   (ends (Array Int Int))
   (pivots (Array Int Int))
   (step Int)) Bool
  (and
    (MainNarrowingStep x b s starts ends pivots step)
    (< (select starts step) (x_index x))
    (< (x_index x) (- (select ends step) 1))))
(define-fun-rec FallbackNarrowingSteps
  ((x Input)
   (b Boundary)
   (s State)
   (initial_start Int)
   (initial_end Int)
   (starts (Array Int Int))
   (ends (Array Int Int))
   (pivots (Array Int Int))
   (count Int)) Bool
  (ite
    (<= count 0)
    (and
      (= (select starts 0) initial_start)
      (= (select ends 0) initial_end)
      (WindowValid x initial_start initial_end))
    (let ((step (- count 1)))
      (and
        (FallbackNarrowingSteps
          x b s initial_start initial_end starts ends pivots step)
        (FallbackNarrowingStep x b s starts ends pivots step)))))
(define-fun SelectionTerminalAtWindow
  ((x Input)
   (b Boundary)
   (y Output)
   (s State)
   (start Int)
   (end Int)) Bool
  (and
    (WindowValid x start end)
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (= (y_pivot_class y)
       (ObservedClass b (y_pivot_identity y)))
    (or
      (and
        (<= (- end start) 16)
        (SortedWindow b (s_final_sequence s) start end))
      (and
        (> (- end start) 16)
        (PartitionedWindow
          b
          (s_final_sequence s)
          start
          (x_index x)
          end)))))
(define-fun FallbackTerminalAtWindow
  ((x Input)
   (b Boundary)
   (y Output)
   (s State)
   (start Int)
   (end Int)) Bool
  (and
    (WindowValid x start end)
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (= (y_pivot_class y)
       (ObservedClass b (y_pivot_identity y)))
    (or
      (and
        (<= (- end start) 16)
        (SortedWindow b (s_final_sequence s) start end))
      (and
        (> (- end start) 16)
        (= (x_index x) start)
        (PartitionedWindow
          b (s_final_sequence s) start (x_index x) end))
      (and
        (> (- end start) 16)
        (= (x_index x) (- end 1))
        (PartitionedWindow
          b (s_final_sequence s) start (x_index x) end))
      (and
        (> (- end start) 16)
        (< start (x_index x))
        (< (x_index x) (- end 1))
        (PartitionedWindow
          b (s_final_sequence s) start (x_index x) end)))))
(define-fun FallbackReachable
  ((x Input)
   (b Boundary)
   (y Output)
   (s State)
   (initial_start Int)
   (initial_end Int)) Bool
  (exists
    ((narrowings Int)
     (starts (Array Int Int))
     (ends (Array Int Int))
     (pivots (Array Int Int)))
    (and
      (<= 0 narrowings)
      (< narrowings (- initial_end initial_start))
      (FallbackNarrowingSteps
        x
        b
        s
        initial_start
        initial_end
        starts
        ends
        pivots
        narrowings)
      (FallbackTerminalAtWindow
        x
        b
        y
        s
        (select starts narrowings)
        (select ends narrowings)))))
(define-fun BoundsTransition
  ((x Input) (y Output)) Bool
  (and
    (= (y_left_len y) (x_index x))
    (= (y_right_len y) (- (x_length x) (x_index x) 1))))
(define-fun OrdObservationTransition
  ((x Input) (b Boundary) (y Output)) Bool
  (and
    (= (b_ord_identity b) (x_ord_identity x))
    (> (select (x_identity_multiplicity x) (y_pivot_identity y)) 0)
    (= (y_pivot_class y)
       (ObservedClass b (y_pivot_identity y)))))
(define-fun ZstTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (=>
    (x_is_zst x)
    (and
      (forall ((position Int))
        (=>
          (PositionInRange position 0 (x_length x))
          (= (select (s_final_sequence s) position)
             (select (x_initial_sequence x) position))))
      (forall ((position Int))
        (=>
          (PositionInRange position 0 (x_length x))
          (= (ObservedClass
               b
               (select (x_initial_sequence x) position))
             (ObservedClass
               b
               (select (x_initial_sequence x) 0)))))
      (= (y_pivot_class y)
         (ObservedClass b (select (x_initial_sequence x) 0)))
      (= (select (x_less_count x) (y_pivot_class y)) 0)
      (= (select (x_equal_count x) (y_pivot_class y)) (x_length x))
      (= (select (x_greater_count x) (y_pivot_class y)) 0))))
(define-fun MinMaxScanTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (=>
      (and (not (x_is_zst x))
           (= (x_index x) (- (x_length x) 1)))
      (and
        (= (select (x_greater_count x) (y_pivot_class y)) 0)
        (PartitionedWindow
          b
          (s_final_sequence s)
          0
          (x_index x)
          (x_length x))))
    (=>
      (and (not (x_is_zst x))
           (not (= (x_index x) (- (x_length x) 1)))
           (= (x_index x) 0))
      (and
        (= (select (x_less_count x) (y_pivot_class y)) 0)
        (PartitionedWindow
          b
          (s_final_sequence s)
          0
          (x_index x)
          (x_length x))))))
(define-fun SwapPermutationTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (StateSummaryValid x b s)
    (> (select (x_identity_multiplicity x) (y_pivot_identity y)) 0)
    (= (s_final_identity_multiplicity s)
       (x_identity_multiplicity x))))
(define-fun PartitionTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (RankSelected x (y_pivot_class y))
    (PartitionedWindow
      b
      (s_final_sequence s)
      0
      (x_index x)
      (x_length x))
    (= (s_left_class_multiplicity s)
       (ExpectedLeftClassMultiplicity x (y_pivot_class y)))
    (= (s_right_class_multiplicity s)
       (ExpectedRightClassMultiplicity x (y_pivot_class y)))))
(define-fun RecursiveLoopOrFallbackTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (= (y_pivot_class y)
       (ObservedClass b (y_pivot_identity y)))
    (=>
      (and
        (not (x_is_zst x))
        (< 0 (x_index x))
        (< (x_index x) (- (x_length x) 1)))
      (exists
        ((main_narrowings Int)
         (starts (Array Int Int))
         (ends (Array Int Int))
         (pivots (Array Int Int)))
        (and
          (<= 0 main_narrowings)
          (<= main_narrowings 16)
          (MainNarrowingSteps
            x
            b
            s
            0
            (x_length x)
            starts
            ends
            pivots
            main_narrowings)
          (let
            ((current_start (select starts main_narrowings))
             (current_end (select ends main_narrowings)))
            (or
              (and
                (< main_narrowings 16)
                (SelectionTerminalAtWindow
                  x b y s current_start current_end))
              (and
                (= main_narrowings 16)
                (or
                  (and
                    (<= (- current_end current_start) 16)
                    (SelectionTerminalAtWindow
                      x b y s current_start current_end))
                  (and
                    (> (- current_end current_start) 16)
                    (FallbackReachable
                      x
                      b
                      y
                      s
                      current_start
                      current_end)))))))))))
(define-fun FinalReturnedSubsliceTransition
  ((x Input) (y Output) (s State)) Bool
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
    (= (s_final_length s) (x_length x))))
(define-fun ActiveFinalConcatConjunct
  ((x Input)
   (left_ref Reference)
   (pivot_ref Reference)
   (right_ref Reference)
   (final_allocation Int)
   (final_borrow Int)
   (final_length Int)) Bool
  (and
    (= left_ref (LeftReference x))
    (= pivot_ref (PivotReference x))
    (= right_ref (RightReference x))
    (= final_allocation (x_allocation x))
    (= final_borrow (x_borrow x))
    (= final_length
       (+ (ref_span left_ref) (ref_span pivot_ref) (ref_span right_ref)))))
(define-fun ActiveLeftLengthConjunct
  ((x Input) (left_len Int) (left_ref Reference)) Bool
  (and (= left_len (x_index x)) (= (ref_span left_ref) left_len)))
(define-fun ActivePivotAtIndexConjunct
  ((x Input)
   (pivot_identity Int)
   (pivot_ref Reference)
   (final_sequence (Array Int Int))) Bool
  (and
    (= (ref_start pivot_ref) (x_index x))
    (= (ref_span pivot_ref) 1)
    (= pivot_identity (select final_sequence (x_index x)))))
(define-fun ActiveRightLengthConjunct
  ((x Input) (right_len Int) (right_ref Reference)) Bool
  (and
    (= right_len (- (x_length x) (x_index x) 1))
    (= (ref_span right_ref) right_len)))
(define-fun ActivePermutationConjunct
  ((x Input)
   (final_sequence (Array Int Int))
   (final_identity_multiplicity (Array Int Int))) Bool
  (and
    (= final_identity_multiplicity
       (SequenceIdentityMultiplicity final_sequence (x_length x)))
    (= final_identity_multiplicity (x_identity_multiplicity x))))
(define-fun ActiveOrdPartitionConjunct
  ((x Input)
   (b Boundary)
   (pivot_identity Int)
   (pivot_class Int)
   (final_sequence (Array Int Int))
   (left_class_multiplicity (Array Int Int))
   (right_class_multiplicity (Array Int Int))) Bool
  (and
    (= pivot_class (ObservedClass b pivot_identity))
    (= pivot_identity (select final_sequence (x_index x)))
    (RankSelected x pivot_class)
    (PartitionedWindow
      b final_sequence 0 (x_index x) (x_length x))
    (= left_class_multiplicity
       (SequenceClassMultiplicity
         final_sequence
         (b_ord_class b)
         (x_index x)))
    (= right_class_multiplicity
       (lambda ((class Int))
         (- (ClassCountThrough
              final_sequence
              (b_ord_class b)
              (x_length x)
              class)
            (ClassCountThrough
              final_sequence
              (b_ord_class b)
              (+ (x_index x) 1)
              class))))
    (= left_class_multiplicity
       (ExpectedLeftClassMultiplicity x pivot_class))
    (= right_class_multiplicity
       (ExpectedRightClassMultiplicity x pivot_class))))
(define-fun ReviewedSelectionEquivalent
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and
    (= (y_left_ref y1) (y_left_ref y2))
    (= (y_pivot_ref y1) (y_pivot_ref y2))
    (= (y_right_ref y1) (y_right_ref y2))
    (= (y_left_len y1) (y_left_len y2))
    (= (y_pivot_class y1) (y_pivot_class y2))
    (= (y_right_len y1) (y_right_len y2))
    (= (s_final_identity_multiplicity s1)
       (s_final_identity_multiplicity s2))
    (= (FinalIdentityMultiplicity x s1)
       (FinalIdentityMultiplicity x s2))
    (= (s_left_class_multiplicity s1)
       (s_left_class_multiplicity s2))
    (= (FinalLeftClassMultiplicity x b s1)
       (FinalLeftClassMultiplicity x b s2))
    (= (s_right_class_multiplicity s1)
       (s_right_class_multiplicity s2))
    (= (FinalRightClassMultiplicity x b s1)
       (FinalRightClassMultiplicity x b s2))
    (= (s_final_allocation s1) (s_final_allocation s2))
    (= (s_final_borrow s1) (s_final_borrow s2))
    (= (s_final_length s1) (s_final_length s2))))
(define-fun RequiresDefinition_T ((x Input)) Bool
  (InputShapeValid x))
(define-fun BoundaryDefinition_T ((x Input) (b Boundary)) Bool
  (and
    (= (b_ord_identity b) (x_ord_identity x))
    (InputSummaryValid x b)
    (=>
      (x_is_zst x)
      (= (select
           (x_equal_count x)
           (ObservedClass b (select (x_initial_sequence x) 0)))
         (x_length x)))))
(define-fun Requires_T ((x Input)) Bool
  (RequiresDefinition_T x))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (BoundaryDefinition_T x b))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (BoundsTransition x y)
    (OrdObservationTransition x b y)
    (ZstTransition x b y s)
    (MinMaxScanTransition x b y s)
    (SwapPermutationTransition x b y s)
    (PartitionTransition x b y s)
    (RecursiveLoopOrFallbackTransition x b y s)
    (FinalReturnedSubsliceTransition x y s)
    (ActiveFinalConcatConjunct
      x
      (y_left_ref y)
      (y_pivot_ref y)
      (y_right_ref y)
      (s_final_allocation s)
      (s_final_borrow s)
      (s_final_length s))
    (ActiveLeftLengthConjunct x (y_left_len y) (y_left_ref y))
    (ActivePivotAtIndexConjunct
      x
      (y_pivot_identity y)
      (y_pivot_ref y)
      (s_final_sequence s))
    (ActiveRightLengthConjunct x (y_right_len y) (y_right_ref y))
    (ActivePermutationConjunct
      x
      (s_final_sequence s)
      (s_final_identity_multiplicity s))
    (ActiveOrdPartitionConjunct
      x
      b
      (y_pivot_identity y)
      (y_pivot_class y)
      (s_final_sequence s)
      (s_left_class_multiplicity s)
      (s_right_class_multiplicity s))))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
"""


def _replace_definition(text: str, symbol: str, replacement: str) -> str:
    markers = (
        f"(define-fun {symbol}",
        f"(define-fun-rec {symbol}",
    )
    starts = [text.find(marker) for marker in markers]
    start = min(position for position in starts if position >= 0)
    end = text.index("\n(define-fun", start + 1)
    return text[:start] + replacement.rstrip() + text[end:]


def _bounded_count_definition(
    symbol: str,
    arguments: str,
    condition: str,
) -> str:
    terms = [
        f"(ite (and (< {position} count) "
        f"{condition.replace('POSITION', str(position))}) 1 0)"
        for position in range(5)
    ]
    return (
        f"(define-fun {symbol}\n"
        f"  ({arguments}) Int\n"
        f"  (+ {' '.join(terms)}))"
    )


def _bounded_rank_summary_unique_definition() -> str:
    implications = [
        "(=> (and "
        f"(RankSelected x {first}) "
        f"(RankSelected x {second})) "
        f"(= {first} {second}))"
        for first in range(5)
        for second in range(5)
    ]
    return """\
(define-fun RankSummaryUnique ((x Input)) Bool
  (and
    BOUNDED_RANK_IMPLICATIONS))""".replace(
        "BOUNDED_RANK_IMPLICATIONS",
        "\n    ".join(implications),
    )


def _bounded_sum(terms: list[str]) -> str:
    return f"(+ {' '.join(terms)})"


def _bounded_identity_count(
    sequence: str,
    length: str,
    identity: int,
) -> str:
    return _bounded_sum(
        [
            "(ite "
            f"(and (< {position} {length}) "
            f"(= (select {sequence} {position}) {identity})) "
            "1 0)"
            for position in range(5)
        ]
    )


def _bounded_class_count(
    sequence: str,
    classes: str,
    *,
    start: str,
    end: str,
    class_value: int,
) -> str:
    return _bounded_sum(
        [
            "(ite "
            f"(and (<= {start} {position}) (< {position} {end}) "
            f"(= (select {classes} (select {sequence} {position})) "
            f"{class_value})) "
            "1 0)"
            for position in range(5)
        ]
    )


def _bounded_rank_count(
    sequence: str,
    classes: str,
    length: str,
    class_value: int,
    operator: str,
) -> str:
    return _bounded_sum(
        [
            "(ite "
            f"(and (< {position} {length}) "
            f"({operator} "
            f"(select {classes} (select {sequence} {position})) "
            f"{class_value})) "
            "1 0)"
            for position in range(5)
        ]
    )


def _bounded_input_summary_definition() -> str:
    summary_checks = []
    for identity in (10, 11, 20, 21, 30, 31, 99):
        summary_checks.append(
            f"(= (select (x_identity_multiplicity x) {identity}) "
            f"{_bounded_identity_count('(x_initial_sequence x)', '(x_length x)', identity)})"
        )
    for class_value in range(5):
        class_count = _bounded_class_count(
            "(x_initial_sequence x)",
            "(b_ord_class b)",
            start="0",
            end="(x_length x)",
            class_value=class_value,
        )
        less_count = _bounded_rank_count(
            "(x_initial_sequence x)",
            "(b_ord_class b)",
            "(x_length x)",
            class_value,
            "<",
        )
        greater_count = _bounded_rank_count(
            "(x_initial_sequence x)",
            "(b_ord_class b)",
            "(x_length x)",
            class_value,
            ">",
        )
        summary_checks.extend(
            (
                f"(= (select (x_class_multiplicity x) {class_value}) "
                f"{class_count})",
                f"(= (select (x_less_count x) {class_value}) "
                f"{less_count})",
                f"(= (select (x_equal_count x) {class_value}) "
                f"{class_count})",
                f"(= (select (x_greater_count x) {class_value}) "
                f"{greater_count})",
            )
        )
    domain_checks = [
        "(=> "
        f"(< {position} (x_length x)) "
        "(InClassDomain x "
        "(ObservedClass b "
        f"(select (x_initial_sequence x) {position}))))"
        for position in range(5)
    ]
    return """\
(define-fun InputSummaryValid
  ((x Input) (b Boundary)) Bool
  (and
    BOUNDED_SUMMARY_CHECKS
    BOUNDED_DOMAIN_CHECKS
    (RankSummaryUnique x)))""".replace(
        "BOUNDED_SUMMARY_CHECKS",
        "\n    ".join(summary_checks),
    ).replace(
        "BOUNDED_DOMAIN_CHECKS",
        "\n    ".join(domain_checks),
    )


def _bounded_state_summary_definition() -> str:
    checks = []
    for identity in (10, 11, 20, 21, 30, 31, 99):
        checks.append(
            f"(= (select (s_final_identity_multiplicity s) {identity}) "
            f"{_bounded_identity_count('(s_final_sequence s)', '(x_length x)', identity)})"
        )
    for class_value in range(5):
        left_count = _bounded_class_count(
            "(s_final_sequence s)",
            "(b_ord_class b)",
            start="0",
            end="(x_index x)",
            class_value=class_value,
        )
        right_count = _bounded_class_count(
            "(s_final_sequence s)",
            "(b_ord_class b)",
            start="(+ (x_index x) 1)",
            end="(x_length x)",
            class_value=class_value,
        )
        checks.extend(
            (
                f"(= (select (s_left_class_multiplicity s) {class_value}) "
                f"{left_count})",
                f"(= (select (s_right_class_multiplicity s) {class_value}) "
                f"{right_count})",
            )
        )
    return """\
(define-fun StateSummaryValid
  ((x Input) (b Boundary) (s State)) Bool
  (and
    BOUNDED_STATE_SUMMARY_CHECKS))""".replace(
        "BOUNDED_STATE_SUMMARY_CHECKS",
        "\n    ".join(checks),
    )


def _bounded_partitioned_window_definition() -> str:
    left = [
        "(=> "
        f"(PositionInRange {position} start pivot) "
        "(<= "
        f"(ObservedClass b (select sequence {position})) "
        "(ObservedClass b (select sequence pivot))))"
        for position in range(5)
    ]
    right = [
        "(=> "
        f"(PositionInRange {position} (+ pivot 1) end) "
        "(>= "
        f"(ObservedClass b (select sequence {position})) "
        "(ObservedClass b (select sequence pivot))))"
        for position in range(5)
    ]
    return """\
(define-fun PartitionedWindow
  ((b Boundary)
   (sequence (Array Int Int))
   (start Int)
   (pivot Int)
   (end Int)) Bool
  (and
    (PositionInRange pivot start end)
    BOUNDED_PARTITION_CHECKS))""".replace(
        "BOUNDED_PARTITION_CHECKS",
        "\n    ".join([*left, *right]),
    )


def _bounded_sorted_window_definition() -> str:
    checks = [
        "(=> "
        f"(and (PositionInRange {lower} start end) "
        f"(PositionInRange {upper} start end)) "
        "(<= "
        f"(ObservedClass b (select sequence {lower})) "
        f"(ObservedClass b (select sequence {upper}))))"
        for lower in range(5)
        for upper in range(lower + 1, 5)
    ]
    return """\
(define-fun SortedWindow
  ((b Boundary)
   (sequence (Array Int Int))
   (start Int)
   (end Int)) Bool
  (and
    BOUNDED_SORT_CHECKS))""".replace(
        "BOUNDED_SORT_CHECKS",
        "\n    ".join(checks),
    )


def _bounded_zst_transition_definition() -> str:
    sequence_checks = [
        "(=> "
        f"(< {position} (x_length x)) "
        f"(= (select (s_final_sequence s) {position}) "
        f"(select (x_initial_sequence x) {position})))"
        for position in range(5)
    ]
    class_checks = [
        "(=> "
        f"(< {position} (x_length x)) "
        "(= "
        "(ObservedClass b "
        f"(select (x_initial_sequence x) {position})) "
        "(ObservedClass b (select (x_initial_sequence x) 0))))"
        for position in range(5)
    ]
    return """\
(define-fun ZstTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (=>
    (x_is_zst x)
    (and
      BOUNDED_ZST_CHECKS
      (= (y_pivot_class y)
         (ObservedClass b (select (x_initial_sequence x) 0)))
      (= (select (x_less_count x) (y_pivot_class y)) 0)
      (= (select (x_equal_count x) (y_pivot_class y)) (x_length x))
      (= (select (x_greater_count x) (y_pivot_class y)) 0))))""".replace(
        "BOUNDED_ZST_CHECKS",
        "\n      ".join([*sequence_checks, *class_checks]),
    )


def _bounded_partition_transition_definition() -> str:
    checks = [
        f"(= (select (s_left_class_multiplicity s) {class_value}) "
        f"(ExpectedLeftClassCount x (y_pivot_class y) {class_value}))"
        for class_value in range(5)
    ]
    checks.extend(
        f"(= (select (s_right_class_multiplicity s) {class_value}) "
        f"(ExpectedRightClassCount x (y_pivot_class y) {class_value}))"
        for class_value in range(5)
    )
    return """\
(define-fun PartitionTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (RankSelected x (y_pivot_class y))
    (PartitionedWindow
      b
      (s_final_sequence s)
      0
      (x_index x)
      (x_length x))
    BOUNDED_EXPECTED_SIDE_CHECKS))""".replace(
        "BOUNDED_EXPECTED_SIDE_CHECKS",
        "\n    ".join(checks),
    )


def _bounded_active_permutation_definition() -> str:
    checks = [
        f"(= (select final_identity_multiplicity {identity}) "
        f"{_bounded_identity_count('final_sequence', '(x_length x)', identity)})"
        for identity in (10, 11, 20, 21, 30, 31, 99)
    ]
    return """\
(define-fun ActivePermutationConjunct
  ((x Input)
   (final_sequence (Array Int Int))
   (final_identity_multiplicity (Array Int Int))) Bool
  (and
    BOUNDED_FINAL_IDENTITY_CHECKS
    (= final_identity_multiplicity (x_identity_multiplicity x))))""".replace(
        "BOUNDED_FINAL_IDENTITY_CHECKS",
        "\n    ".join(checks),
    )


def _bounded_active_partition_definition() -> str:
    checks = []
    for class_value in range(5):
        left_count = _bounded_class_count(
            "final_sequence",
            "(b_ord_class b)",
            start="0",
            end="(x_index x)",
            class_value=class_value,
        )
        right_count = _bounded_class_count(
            "final_sequence",
            "(b_ord_class b)",
            start="(+ (x_index x) 1)",
            end="(x_length x)",
            class_value=class_value,
        )
        checks.extend(
            (
                f"(= (select left_class_multiplicity {class_value}) "
                f"{left_count})",
                f"(= (select right_class_multiplicity {class_value}) "
                f"{right_count})",
                f"(= (select left_class_multiplicity {class_value}) "
                f"(ExpectedLeftClassCount x pivot_class {class_value}))",
                f"(= (select right_class_multiplicity {class_value}) "
                f"(ExpectedRightClassCount x pivot_class {class_value}))",
            )
        )
    return """\
(define-fun ActiveOrdPartitionConjunct
  ((x Input)
   (b Boundary)
   (pivot_identity Int)
   (pivot_class Int)
   (final_sequence (Array Int Int))
   (left_class_multiplicity (Array Int Int))
   (right_class_multiplicity (Array Int Int))) Bool
  (and
    (= pivot_class (ObservedClass b pivot_identity))
    (= pivot_identity (select final_sequence (x_index x)))
    (RankSelected x pivot_class)
    (PartitionedWindow
      b final_sequence 0 (x_index x) (x_length x))
    BOUNDED_ACTIVE_SIDE_CHECKS))""".replace(
        "BOUNDED_ACTIVE_SIDE_CHECKS",
        "\n    ".join(checks),
    )


def _bounded_reviewed_equivalence_definition() -> str:
    return """\
(define-fun ReviewedSelectionEquivalent
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and
    (= (y_left_ref y1) (y_left_ref y2))
    (= (y_pivot_ref y1) (y_pivot_ref y2))
    (= (y_right_ref y1) (y_right_ref y2))
    (= (y_left_len y1) (y_left_len y2))
    (= (y_pivot_class y1) (y_pivot_class y2))
    (= (y_right_len y1) (y_right_len y2))
    (= (s_final_identity_multiplicity s1)
       (s_final_identity_multiplicity s2))
    (= (s_left_class_multiplicity s1)
       (s_left_class_multiplicity s2))
    (= (s_right_class_multiplicity s1)
       (s_right_class_multiplicity s2))
    (= (s_final_allocation s1) (s_final_allocation s2))
    (= (s_final_borrow s1) (s_final_borrow s2))
    (= (s_final_length s1) (s_final_length s2))))"""


def _bounded_model_prefix(terms: dict[str, str]) -> str:
    prefix = _model_prefix()
    for symbol, arguments, condition in (
        (
            "IdentityCountThrough",
            "(sequence (Array Int Int)) (count Int) (identity Int)",
            "(= (select sequence POSITION) identity)",
        ),
        (
            "ClassCountThrough",
            (
                "(sequence (Array Int Int)) "
                "(classes (Array Int Int)) "
                "(count Int) (class Int)"
            ),
            "(= (select classes (select sequence POSITION)) class)",
        ),
        (
            "LessCountThrough",
            (
                "(sequence (Array Int Int)) "
                "(classes (Array Int Int)) "
                "(count Int) (class Int)"
            ),
            "(< (select classes (select sequence POSITION)) class)",
        ),
        (
            "GreaterCountThrough",
            (
                "(sequence (Array Int Int)) "
                "(classes (Array Int Int)) "
                "(count Int) (class Int)"
            ),
            "(> (select classes (select sequence POSITION)) class)",
        ),
    ):
        prefix = _replace_definition(
            prefix,
            symbol,
            _bounded_count_definition(symbol, arguments, condition),
        )
    for symbol, replacement in (
        ("RankSummaryUnique", _bounded_rank_summary_unique_definition()),
        ("InputSummaryValid", _bounded_input_summary_definition()),
        ("StateSummaryValid", _bounded_state_summary_definition()),
        ("PartitionedWindow", _bounded_partitioned_window_definition()),
        ("SortedWindow", _bounded_sorted_window_definition()),
        ("ZstTransition", _bounded_zst_transition_definition()),
        ("PartitionTransition", _bounded_partition_transition_definition()),
        (
            "ActivePermutationConjunct",
            _bounded_active_permutation_definition(),
        ),
        (
            "ActiveOrdPartitionConjunct",
            _bounded_active_partition_definition(),
        ),
        (
            "ReviewedSelectionEquivalent",
            _bounded_reviewed_equivalence_definition(),
        ),
    ):
        prefix = _replace_definition(prefix, symbol, replacement)
    for symbol in ("MainNarrowingSteps", "FallbackNarrowingSteps"):
        prefix = _replace_definition(
            prefix,
            symbol,
            f"""\
(define-fun {symbol}
  ((x Input)
   (b Boundary)
   (s State)
   (initial_start Int)
   (initial_end Int)
   (starts (Array Int Int))
   (ends (Array Int Int))
   (pivots (Array Int Int))
   (count Int)) Bool
  (and
    (= count 0)
    (= (select starts 0) initial_start)
    (= (select ends 0) initial_end)
    (WindowValid x initial_start initial_end)))""",
        )
    prefix = _replace_definition(
        prefix,
        "RecursiveLoopOrFallbackTransition",
        """\
(define-fun RecursiveLoopOrFallbackTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (= (y_pivot_identity y)
       (select (s_final_sequence s) (x_index x)))
    (= (y_pivot_class y)
       (ObservedClass b (y_pivot_identity y)))
    (=>
      (and
        (not (x_is_zst x))
        (< 0 (x_index x))
        (< (x_index x) (- (x_length x) 1)))
      (and
        (<= (x_length x) 16)
        (SortedWindow
          b
          (s_final_sequence s)
          0
          (x_length x))))))""",
    )
    prefix = _replace_definition(
        prefix,
        "Requires_T",
        "(define-fun Requires_T ((x Input)) Bool\n"
        "  (and\n"
        f"    (= x {terms['x']})\n"
        "    (RequiresDefinition_T x)))",
    )
    prefix = _replace_definition(
        prefix,
        "Boundary_T",
        "(define-fun Boundary_T ((x Input) (b Boundary)) Bool\n"
        "  (and\n"
        f"    (= b {terms['b']})\n"
        "    (BoundaryDefinition_T x b)))",
    )
    return prefix


def obligation_text(purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-077 obligation purpose: {purpose}")
    prefix = (
        _bounded_model_prefix(_case_terms())
        if purpose == EXACT_OUTPUT
        else _model_prefix()
    )
    return (
        prefix
        + f"""\
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_equivalence_body(purpose)}
(assert
  (not
    (=>
      (and (Requires_T x)
           (Boundary_T x b)
           (Spec_T x b y1 s1)
           (Spec_T x b y2 s2))
      (Equivalent_T x b y1 s1 y2 s2))))
(check-sat)
"""
    )


def _principal_observations() -> list[dict[str, str]]:
    observations = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort,
        }
        for selector, sort in OUTPUT_FIELDS
    ]
    observations.extend(
        {
            "selector": selector,
            "left": "state1",
            "right": "state2",
            "sort": sort,
        }
        for selector, sort in STATE_FIELDS
    )
    return observations


def obligation_metadata(purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-077 obligation purpose: {purpose}")
    exact = purpose == EXACT_OUTPUT
    return {
        "schema_version": 4,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "domain": {
            "bounded": exact,
            "slice_length": (
                "fixed length five classification witness"
                if exact
                else "arbitrary positive integer"
            ),
            "index": (
                "fixed index two classification witness"
                if exact
                else "arbitrary integer in [0, length)"
            ),
            "identity_multiplicity": (
                "exact integer-indexed multiset recursively derived from the "
                "modeled input and final sequences"
            ),
            "ord_classes": (
                "arbitrary source-observed total-order classes whose class, "
                "less, equal, greater, and side counts are recursively "
                "derived from the modeled sequences"
            ),
            "source_branches": [
                "bounds/panic exclusion",
                "zero-sized type",
                "last-index maximum scan and swap",
                "first-index minimum scan and swap",
                "partition-at-index recursive loop",
                "16-iteration median-of-medians fallback",
                "final split_at_mut returned subslices",
            ],
            "classification_use": (
                "fixed-input exact SAT witness"
                if exact
                else "general reviewed-equivalence proof"
            ),
        },
        "active_contract_conjuncts": list(ACTIVE_CONJUNCTS),
        "boundary_scope": {
            "admitted_trust_site_ids": list(ADMITTED_TRUST_SITES),
            "excluded_retained_trust_site_ids": list(
                EXCLUDED_RETAINED_TRUST_SITES
            ),
            "context_only_trust_site_ids": list(CONTEXT_ONLY_TRUST_SITES),
            "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
            "source_backed_replacement_ids": [],
            "shared_observations": [
                "Ord implementation identity",
                "extensional Ord equivalence class for each input identity",
            ],
            "excluded_observations": [
                "pivot identity or class selected by the algorithm",
                "side ordering or selected permutation",
                "returned references",
                "aggregate final state",
                "answer encodings",
                "pivot/swap choices",
                "complete comparison or execution traces",
            ],
            "narrower_than_target": True,
        },
        "boundary_fields": [
            {
                "selector": "b_ord_identity",
                "role": "callback_argument",
                "source_citations": [TARGET_SOURCE, ORD_SOURCE],
                "trust_site_ids": list(ADMITTED_TRUST_SITES),
                "source_backed_replacement_ids": [],
            },
            {
                "selector": "b_ord_class",
                "role": "callback_result",
                "source_citations": [
                    TARGET_SOURCE,
                    SELECT_SOURCE,
                    PARTITION_SOURCE,
                    ORD_SOURCE,
                    VOCABULARY_SOURCE,
                ],
                "trust_site_ids": list(ADMITTED_TRUST_SITES),
                "source_backed_replacement_ids": [],
            },
        ],
        "source_backed_replacements": [
            {
                "replacement_id": REPLACEMENT_ID,
                "replaces_trust_site_ids": list(
                    EXCLUDED_RETAINED_TRUST_SITES
                ),
                "symbols": [
                    symbol
                    for symbol in SOURCE_TRANSITIONS
                    if symbol != "OrdObservationTransition"
                ],
                "source_citations": [
                    TARGET_SOURCE,
                    SELECT_SOURCE,
                    PARTITION_SOURCE,
                ],
                "semantics": (
                    "Explicit bounds, ZST, min/max, sequence-derived "
                    "swap-permutation and partition/rank transitions, "
                    "strictly shrinking introselect windows, a well-founded "
                    "fallback path, and final returned ranges replace the "
                    "opaque retained whole partition_at_index relation."
                ),
            }
        ],
        "declared_functions": [],
        "source_transition_definitions": list(SOURCE_TRANSITIONS),
        "source_transition_bindings": {
            "bounds": {
                "symbol": "BoundsTransition",
                "source_citations": [TARGET_SOURCE, SELECT_SOURCE],
            },
            "ord": {
                "symbol": "OrdObservationTransition",
                "trust_site_ids": list(ADMITTED_TRUST_SITES),
                "source_citations": [TARGET_SOURCE, ORD_SOURCE],
            },
            "zst": {
                "symbol": "ZstTransition",
                "replacement_id": REPLACEMENT_ID,
                "source_citations": [SELECT_SOURCE],
            },
            "min_max": {
                "symbol": "MinMaxScanTransition",
                "replacement_id": REPLACEMENT_ID,
                "source_citations": [SELECT_SOURCE],
            },
            "swap": {
                "symbol": "SwapPermutationTransition",
                "replacement_id": REPLACEMENT_ID,
                "source_citations": [SELECT_SOURCE],
            },
            "partition": {
                "symbol": "PartitionTransition",
                "replacement_id": REPLACEMENT_ID,
                "source_citations": [SELECT_SOURCE, PARTITION_SOURCE],
            },
            "recursive_loop_fallback": {
                "symbol": "RecursiveLoopOrFallbackTransition",
                "replacement_id": REPLACEMENT_ID,
                "source_citations": [SELECT_SOURCE],
            },
            "returned_subslices": {
                "symbol": "FinalReturnedSubsliceTransition",
                "replacement_id": REPLACEMENT_ID,
                "source_citations": [TARGET_SOURCE, SELECT_SOURCE],
            },
        },
        "target_definition": "TargetDefinition_T",
        "theorem_variables": {
            "input": "x",
            "boundary": "b",
            "output1": "y1",
            "state1": "s1",
            "output2": "y2",
            "state2": "s2",
        },
        "equivalence_kind": "exact" if exact else "reviewed-selection",
        "equivalence_scope": (
            "exact returned references, pivot identity, side order, and final state"
            if exact
            else (
                "exact returned range identities and lengths, exact whole-input "
                "identity multiplicity, pivot rank and Ord class, side-class "
                "multiplicity, allocation, borrow, and final length; only side "
                "ordering and equal-class pivot identity are relaxed"
            )
        ),
        "weak_equivalence_review": (
            {}
            if exact
            else {
                "source_citations": [PUBLIC_DOCS, SELECT_SOURCE],
                "positive_witness": (
                    "side-order permutations and equal-class pivot identities "
                    "remain equivalent"
                ),
                "negative_witness": (
                    "foreign identity, wrong rank/class, partition crossing, "
                    "malformed range, and state drift are rejected; stale "
                    "identity and side-class summaries over malformed final "
                    "sequences are independently UNSAT"
                ),
            }
        ),
        "principal_observations": _principal_observations(),
        "expected_solver_result": "sat" if exact else "unsat",
    }


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return obligation_text(purpose), obligation_metadata(purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError("target-077 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-077 metadata differs from the reviewed source translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-077 SMT differs from the reviewed source translation"
        )


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "boundary_narrower_than_target": True,
        "admitted_trust_site_ids": list(ADMITTED_TRUST_SITES),
        "context_only_trust_site_ids": list(CONTEXT_ONLY_TRUST_SITES),
        "excluded_retained_sites": [
            {
                "trust_site_id": "TS-077-D002",
                "disposition": "excluded-inadmissible-answer-bearing-support",
                "reason": (
                    "The retained dependency states the complete permutation, "
                    "pivot, lengths, and partition result."
                ),
            },
            {
                "trust_site_id": "TS-077-E001",
                "disposition": "excluded-inadmissible-opaque-whole-algorithm",
                "reason": (
                    "The external_body supplies the complete target result and "
                    "is not admitted under a new label."
                ),
            },
        ],
        "shared_boundary_observations": [
            {
                "field": "b_ord_identity",
                "meaning": "identity of the Ord implementation invoked as T::lt",
                "trust_site_ids": list(ADMITTED_TRUST_SITES),
            },
            {
                "field": "b_ord_class",
                "meaning": (
                    "extensional total-order equivalence class observed for "
                    "each input element identity"
                ),
                "trust_site_ids": list(ADMITTED_TRUST_SITES),
            },
        ],
        "source_backed_replacement": {
            "replacement_id": REPLACEMENT_ID,
            "replaces_trust_site_ids": list(EXCLUDED_RETAINED_TRUST_SITES),
            "source_citations": [
                TARGET_SOURCE,
                SELECT_SOURCE,
                PARTITION_SOURCE,
            ],
            "transitions": [
                "valid-index bounds and panic exclusion",
                "zero-sized-type no-op branch",
                "minimum/maximum scans and swaps",
                (
                    "sequence-derived identity multiplicity, rank, "
                    "partition, and side-class transitions"
                ),
                (
                    "strictly shrinking recursive introselect windows and "
                    "well-founded iteration-limit fallback windows"
                ),
                "final left/pivot/right returned-subslice construction",
            ],
        },
        "reviewed_equivalence": {
            "kind": "selection-side-order-and-equal-pivot-equivalence",
            "source_citations": [PUBLIC_DOCS, SELECT_SOURCE],
            "preserved": [
                "returned range identities and lengths",
                "whole-input identity multiplicities",
                "pivot rank and Ord class",
                "left and right Ord-class multiplicities",
                "allocation identity, mutable-borrow identity, and final length",
            ],
            "relaxed_only": [
                "ordering within each unsorted side",
                "identity of the pivot among equal-Ord-class elements",
            ],
        },
        "excluded_from_boundary": [
            "pivot identity or pivot class",
            "selected side permutation",
            "returned subslices",
            "aggregate final state",
            "answer encodings",
            "pivot/swap choices",
            "complete comparison or execution traces",
        ],
        "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
    }


def _int_array(values: dict[int, int], default: int = 0) -> str:
    expression = f"((as const (Array Int Int)) {default})"
    for index, value in sorted(values.items()):
        expression = f"(store {expression} {index} {value})"
    return expression


def _reference(allocation: int, borrow: int, start: int, span: int, kind: int) -> str:
    return f"(mkReference {allocation} {borrow} {start} {span} {kind})"


def _case_terms(
    *,
    equal_pivot: bool = False,
    mutation: str | None = None,
    stale_summaries: bool = False,
) -> dict[str, str]:
    if mutation == "small_sort_unreachable":
        length = 5
        index = 2
        initial = [10, 11, 20, 30, 31]
        classes = {10: 0, 11: 1, 20: 1, 30: 2, 31: 2, 99: 2}
        first = [10, 11, 20, 30, 31]
        second = [11, 10, 20, 30, 31]
    elif equal_pivot:
        length = 4
        index = 1
        initial = [10, 20, 21, 30]
        classes = {10: 0, 20: 1, 21: 1, 30: 2}
        first = [10, 20, 21, 30]
        second = [10, 21, 20, 30]
    else:
        length = 5
        index = 2
        initial = [10, 11, 20, 30, 31]
        classes = {10: 0, 11: 0, 20: 1, 30: 2, 31: 2, 99: 2}
        first = [10, 11, 20, 30, 31]
        second = [11, 10, 20, 31, 30]

    allocation = 41
    borrow = 51
    ord_identity = 61
    left_start = 0
    final_allocation = allocation

    if mutation == "foreign_identity":
        second[-1] = 99
    elif mutation == "wrong_rank_class":
        second = [11, 20, 10, 30, 31]
    elif mutation == "partition_crossing":
        second = [30, 11, 20, 10, 31]
    elif mutation == "malformed_range":
        left_start = 1
    elif mutation == "state_drift":
        final_allocation = 99

    pivot1 = first[index]
    pivot2 = second[index]
    identity_counts = dict(Counter(initial))
    class_counts = dict(Counter(classes[identity] for identity in initial))
    less_counts = {
        class_value: sum(
            classes[identity] < class_value for identity in initial
        )
        for class_value in range(5)
    }
    greater_counts = {
        class_value: sum(
            classes[identity] > class_value for identity in initial
        )
        for class_value in range(5)
    }
    first_identity_counts = dict(Counter(first))
    first_left_classes = dict(
        Counter(classes[identity] for identity in first[:index])
    )
    first_right_classes = dict(
        Counter(classes[identity] for identity in first[index + 1 :])
    )
    summary_sequence = first if stale_summaries else second
    second_identity_counts = dict(Counter(summary_sequence))
    second_left_classes = dict(
        Counter(classes[identity] for identity in summary_sequence[:index])
    )
    second_right_classes = dict(
        Counter(
            classes[identity] for identity in summary_sequence[index + 1 :]
        )
    )
    initial_sequence = _int_array(
        {position: identity for position, identity in enumerate(initial)}
    )
    identity_multiplicity = _int_array(identity_counts)
    class_multiplicity = _int_array(class_counts)
    less = _int_array(less_counts)
    equal = _int_array(class_counts)
    greater = _int_array(greater_counts)
    class_by_identity = _int_array(classes)
    first_sequence = _int_array(
        {position: identity for position, identity in enumerate(first)}
    )
    second_sequence = _int_array(
        {position: identity for position, identity in enumerate(second)}
    )
    first_multiplicity = _int_array(first_identity_counts)
    second_multiplicity = _int_array(second_identity_counts)
    first_left_class_array = _int_array(first_left_classes)
    first_right_class_array = _int_array(first_right_classes)
    second_left_class_array = _int_array(second_left_classes)
    second_right_class_array = _int_array(second_right_classes)
    right_len = length - index - 1
    left_ref1 = _reference(allocation, borrow, 0, index, 1)
    left_ref2 = _reference(allocation, borrow, left_start, index, 1)
    pivot_ref = _reference(allocation, borrow, index, 1, 2)
    right_ref = _reference(allocation, borrow, index + 1, right_len, 3)

    return {
        "x": (
            f"(mkInput {length} {index} {allocation} {borrow} "
            f"{initial_sequence} {identity_multiplicity} "
            f"{class_multiplicity} {less} {equal} {greater} false "
            f"{ord_identity})"
        ),
        "b": f"(mkBoundary {ord_identity} {class_by_identity})",
        "y1": (
            f"(mkOutput {left_ref1} {pivot_ref} {right_ref} {index} "
            f"{pivot1} {classes[pivot1]} {right_len})"
        ),
        "s1": (
            f"(mkState {first_sequence} {first_multiplicity} "
            f"{first_left_class_array} {first_right_class_array} "
            f"{allocation} {borrow} {length})"
        ),
        "y2": (
            f"(mkOutput {left_ref2} {pivot_ref} {right_ref} {index} "
            f"{pivot2} {classes[pivot2]} {right_len})"
        ),
        "s2": (
            f"(mkState {second_sequence} {second_multiplicity} "
            f"{second_left_class_array} {second_right_class_array} "
            f"{final_allocation} {borrow} {length})"
        ),
    }


def _fixed_assertions(terms: dict[str, str]) -> str:
    return "\n".join(
        f"(assert (= {name} {terms[name]}))"
        for name in ("x", "b", "y1", "s1", "y2", "s2")
    )


def fixed_exact_model_text() -> str:
    text = obligation_text(EXACT_OUTPUT)
    terminal = "(check-sat)\n"
    if not text.endswith(terminal):
        raise ValueError("target-077 exact obligation lacks terminal check-sat")
    terms = _case_terms()
    return (
        text[: -len(terminal)]
        + _fixed_assertions(terms)
        + "\n(assert (ReviewedSelectionEquivalent x b y1 s1 y2 s2))\n"
        + """\
(check-sat)
(get-value (
  (Spec_T x b y1 s1)
  (Spec_T x b y2 s2)
  (ReviewedSelectionEquivalent x b y1 s1 y2 s2)
  (Equivalent_T x b y1 s1 y2 s2)))
"""
    )


PROBE_KINDS = (
    "side_reordering",
    "equal_pivot_identity",
    "foreign_identity",
    "wrong_rank_class",
    "partition_crossing",
    "malformed_range",
    "state_drift",
)

MALFORMED_SEQUENCE_PROBE_KINDS = (
    "foreign_identity_stale_summary",
    "partition_crossing_stale_summary",
)
SEMANTIC_REGRESSION_KINDS = (
    *MALFORMED_SEQUENCE_PROBE_KINDS,
    "input_rank_summary_uniqueness",
    "small_sort_source_reachability",
)


def witness_probe_text(kind: str) -> str:
    if kind not in PROBE_KINDS:
        raise ValueError(f"unknown target-077 witness probe: {kind}")
    equal_pivot = kind == "equal_pivot_identity"
    mutation = None if kind in {"side_reordering", "equal_pivot_identity"} else kind
    terms = _case_terms(equal_pivot=equal_pivot, mutation=mutation)
    text = _bounded_model_prefix(terms)
    text += """\
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (ReviewedSelectionEquivalent x b y1 s1 y2 s2))
"""
    text += _fixed_assertions(terms) + "\n"
    if mutation is None:
        text += """\
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
(assert (ReviewedSelectionEquivalent x b y1 s1 y2 s2))
(assert (not (= (s_final_sequence s1) (s_final_sequence s2))))
"""
        if equal_pivot:
            text += "(assert (not (= (y_pivot_identity y1) (y_pivot_identity y2))))\n"
    else:
        text += """\
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (not (Spec_T x b y2 s2)))
"""
        if kind in {
            "foreign_identity",
            "wrong_rank_class",
            "malformed_range",
            "state_drift",
        }:
            text += (
                "(assert (not "
                "(ReviewedSelectionEquivalent x b y1 s1 y2 s2)))\n"
            )
    return (
        text
        + """\
(check-sat)
(get-value (
  (Spec_T x b y1 s1)
  (Spec_T x b y2 s2)
  (ReviewedSelectionEquivalent x b y1 s1 y2 s2)))
"""
    )


def semantic_regression_probe_text(kind: str) -> str:
    if kind not in SEMANTIC_REGRESSION_KINDS:
        raise ValueError(f"unknown target-077 semantic regression: {kind}")

    if kind in MALFORMED_SEQUENCE_PROBE_KINDS:
        mutation = kind.removesuffix("_stale_summary")
        terms = _case_terms(
            mutation=mutation,
            stale_summaries=True,
        )
        return (
            _bounded_model_prefix(terms)
            + _fixed_assertions(terms)
            + """\
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
(check-sat)
"""
        )

    if kind == "input_rank_summary_uniqueness":
        physical_selectors = (
            "x_length",
            "x_index",
            "x_allocation",
            "x_borrow",
            "x_initial_sequence",
            "x_is_zst",
            "x_ord_identity",
        )
        same_physical_input = "\n".join(
            f"(assert (= ({selector} x) ({selector} x_alt)))"
            for selector in physical_selectors
        )
        return (
            _model_prefix()
            + "(declare-const x_alt Input)\n"
            + """\
(assert (Requires_T x))
(assert (Requires_T x_alt))
(assert (Boundary_T x b))
(assert (Boundary_T x_alt b))
"""
            + same_physical_input
            + """\

(assert
  (or
    (not (= (x_class_multiplicity x)
            (x_class_multiplicity x_alt)))
    (not (= (x_less_count x) (x_less_count x_alt)))
    (not (= (x_equal_count x) (x_equal_count x_alt)))
    (not (= (x_greater_count x) (x_greater_count x_alt)))))
(check-sat)
"""
        )

    terms = _case_terms(mutation="small_sort_unreachable")
    return (
        _bounded_model_prefix(terms)
        + _fixed_assertions(terms)
        + """\
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
(check-sat)
"""
    )


def _reference_payload(
    allocation: int, borrow: int, start: int, span: int, kind: str
) -> dict[str, Any]:
    return {
        "allocation": allocation,
        "parent_borrow": borrow,
        "start": start,
        "span": span,
        "projection_kind": kind,
    }


def _execution_payload(
    sequence: list[int],
    classes: dict[str, int],
    *,
    index: int,
    allocation: int,
    borrow: int,
    pivot_identity: int | None = None,
) -> dict[str, Any]:
    pivot = sequence[index] if pivot_identity is None else pivot_identity
    return {
        "output": {
            "left_reference": _reference_payload(
                allocation, borrow, 0, index, "left-subslice"
            ),
            "pivot_reference": _reference_payload(
                allocation, borrow, index, 1, "pivot-element"
            ),
            "right_reference": _reference_payload(
                allocation,
                borrow,
                index + 1,
                len(sequence) - index - 1,
                "right-subslice",
            ),
            "left_length": index,
            "pivot_identity": pivot,
            "pivot_class": classes[str(pivot)],
            "right_length": len(sequence) - index - 1,
        },
        "final": {
            "sequence": sequence,
            "allocation": allocation,
            "borrow": borrow,
            "length": len(sequence),
        },
    }


def witness_payload() -> dict[str, Any]:
    allocation = 41
    borrow = 51
    classes = {
        "10": 0,
        "11": 0,
        "20": 1,
        "21": 1,
        "30": 2,
        "31": 2,
        "99": 2,
    }
    side_input = {
        "sequence": [10, 11, 20, 30, 31],
        "index": 2,
        "allocation": allocation,
        "borrow": borrow,
        "is_zst": False,
        "ord_identity": 61,
    }
    side_first = _execution_payload(
        [10, 11, 20, 30, 31],
        classes,
        index=2,
        allocation=allocation,
        borrow=borrow,
    )
    side_second = _execution_payload(
        [11, 10, 20, 31, 30],
        classes,
        index=2,
        allocation=allocation,
        borrow=borrow,
    )
    equal_input = {
        "sequence": [10, 20, 21, 30],
        "index": 1,
        "allocation": allocation,
        "borrow": borrow,
        "is_zst": False,
        "ord_identity": 61,
    }
    equal_first = _execution_payload(
        [10, 20, 21, 30],
        classes,
        index=1,
        allocation=allocation,
        borrow=borrow,
    )
    equal_second = _execution_payload(
        [10, 21, 20, 30],
        classes,
        index=1,
        allocation=allocation,
        borrow=borrow,
    )
    negatives = {
        "foreign_identity": _execution_payload(
            [11, 10, 20, 31, 99],
            classes,
            index=2,
            allocation=allocation,
            borrow=borrow,
        ),
        "wrong_rank_class": _execution_payload(
            [11, 20, 10, 30, 31],
            classes,
            index=2,
            allocation=allocation,
            borrow=borrow,
        ),
        "partition_crossing": _execution_payload(
            [30, 11, 20, 10, 31],
            classes,
            index=2,
            allocation=allocation,
            borrow=borrow,
        ),
        "malformed_range": _execution_payload(
            [11, 10, 20, 31, 30],
            classes,
            index=2,
            allocation=allocation,
            borrow=borrow,
        ),
        "state_drift": _execution_payload(
            [11, 10, 20, 31, 30],
            classes,
            index=2,
            allocation=99,
            borrow=borrow,
        ),
    }
    negatives["malformed_range"]["output"]["left_reference"]["start"] = 1
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "boundary": {
            "ord_identity": 61,
            "class_by_identity": classes,
        },
        "exact_side_reordering_counterexample": {
            "input": side_input,
            "execution1": side_first,
            "execution2": side_second,
            "expected": {
                "same_input_and_boundary": True,
                "execution1_satisfies_active_contract": True,
                "execution2_satisfies_active_contract": True,
                "exact_equivalent": False,
                "reviewed_selection_equivalent": True,
            },
        },
        "equal_pivot_positive_witness": {
            "input": equal_input,
            "execution1": equal_first,
            "execution2": equal_second,
            "expected": {
                "same_input_and_boundary": True,
                "execution1_satisfies_active_contract": True,
                "execution2_satisfies_active_contract": True,
                "pivot_identity_equal": False,
                "pivot_class_equal": True,
                "reviewed_selection_equivalent": True,
            },
        },
        "negative_witnesses": {
            name: {
                "input": side_input,
                "baseline": side_first,
                "candidate": candidate,
                "expected_candidate_satisfies_active_contract": False,
            }
            for name, candidate in negatives.items()
        },
    }
