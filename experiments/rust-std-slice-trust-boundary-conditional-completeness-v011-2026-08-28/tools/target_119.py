#!/usr/bin/env python3
"""Source-backed conditional-completeness model for write_clone_of_slice."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::write_clone_of_slice"
INPUT_ORDER = "119"
ARTIFACT_ID = "119_core_slice_write_clone_of_slice"
ACTIVE_CONTRACT_SHA256 = (
    "0e3746ad6530835f74de584a989ea1c6126fdb297454de35509cbdb05fd8c54b"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<'a, 'b, T: core::clone::Clone>[ "
    "<[core::mem::MaybeUninit<T>]>::write_clone_of_slice ]( slice: &'a "
    "mut [core::mem::MaybeUninit<T>], src: &'b [T], ) -> (ret: &'a mut "
    "[T]) requires old(slice)@.len() == src@.len(), ensures ret@ == "
    "src@, ret@.len() == src@.len(), final(slice)@.len() == "
    "old(slice)@.len(), maybe_uninit_relation_well_formed( "
    "maybe_uninit_seq_relation(old(slice)@), old(slice)@.len() as int, ), "
    "maybe_uninit_relation_well_formed( maybe_uninit_seq_relation("
    "final(slice)@), final(slice)@.len() as int, ), "
    "maybe_uninit_written_from( maybe_uninit_seq_relation(old(slice)@), "
    "maybe_uninit_seq_relation(final(slice)@), src@, ), "
    "maybe_uninit_all_initialized(maybe_uninit_seq_relation("
    "final(slice)@)), final(ret)@.len() == src@.len(), "
    "maybe_uninit_seq_relation(final(slice)@).values == final(ret)@, ;"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

TARGET_SOURCE_REFERENCE = "core/src/mem/maybe_uninit.rs:1175-1249"
GUARD_SOURCE_REFERENCE = "core/src/mem/maybe_uninit.rs:1623-1635"
CLONE_SOURCE_REFERENCE = "core/src/clone.rs:39-58,129-153,192-233"
ASSUME_INIT_MUT_REFERENCE = "core/src/mem/maybe_uninit.rs:1516-1531"

ADMITTED_TRUST_SITES = (
    "TS-119-D002",
    "TS-119-D003",
    "TS-119-D004",
    "TS-119-E001",
    "TS-119-E002",
    "TS-119-E003",
)
CONTEXT_ONLY_TRUST_SITES = (
    "TS-119-D001",
    "TS-119-C001",
    "TS-119-C002",
    "TS-119-C003",
    "TS-119-C004",
)
ALL_AUDITED_TRUST_SITES = (
    "TS-119-D001",
    "TS-119-D002",
    "TS-119-D003",
    "TS-119-D004",
    "TS-119-C001",
    "TS-119-C002",
    "TS-119-C003",
    "TS-119-C004",
    "TS-119-E001",
    "TS-119-E002",
    "TS-119-E003",
)

ACTIVE_CONJUNCT_SYMBOLS = (
    "ActiveReturnEqualsSourceConjunct",
    "ActiveReturnLengthConjunct",
    "ActiveFinalDestinationLengthConjunct",
    "ActiveInitialRelationWellFormedConjunct",
    "ActiveFinalRelationWellFormedConjunct",
    "ActiveWrittenFromConjunct",
    "ActiveAllInitializedConjunct",
    "ActiveFinalReturnLengthConjunct",
    "ActiveFinalStorageEqualsReturnConjunct",
)

OUTPUT_FIELDS = (
    ("y_return_allocation", "Int"),
    ("y_return_address", "Int"),
    ("y_return_provenance", "Int"),
    ("y_return_borrow", "Int"),
    ("y_return_length", "Int"),
    ("y_return_values", "Array Int Int"),
)

STATE_FIELDS = (
    ("s_destination_length", "Int"),
    ("s_relation_initialized_length", "Int"),
    ("s_relation_values_length", "Int"),
    ("s_destination_storage", "Array Int Cell"),
    ("s_destination_allocation", "Int"),
    ("s_destination_address", "Int"),
    ("s_destination_provenance", "Int"),
    ("s_destination_borrow", "Int"),
    ("s_destination_allocation_base", "Int"),
    ("s_destination_allocation_bytes", "Int"),
    ("s_source_length", "Int"),
    ("s_source_values", "Array Int Int"),
    ("s_source_allocation", "Int"),
    ("s_source_address", "Int"),
    ("s_source_provenance", "Int"),
    ("s_source_allocation_base", "Int"),
    ("s_source_allocation_bytes", "Int"),
    ("s_return_length", "Int"),
    ("s_return_values", "Array Int Int"),
    ("s_return_allocation", "Int"),
    ("s_return_address", "Int"),
    ("s_return_provenance", "Int"),
    ("s_return_borrow", "Int"),
    ("s_clone_state", "Int"),
    ("s_destruct_state", "Int"),
    ("s_element_size", "Int"),
    ("s_element_alignment", "Int"),
    ("s_isize_max", "Int"),
    ("s_address_space_limit", "Int"),
    ("s_frame_token", "Int"),
)

OUTPUT_SOURCE_TRANSITIONS = (
    "AssumeInitMutReturnAllocation",
    "AssumeInitMutReturnAddress",
    "AssumeInitMutReturnProvenance",
    "AssumeInitMutReturnBorrow",
    "AssumeInitMutReturnLength",
    "AssumeInitMutReturnValues",
)


def _state_declaration(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    fields = "\n".join(
        f"      ({selector} ({sort}))"
        if sort.startswith("Array ")
        else f"      ({selector} {sort})"
        for selector, sort in STATE_FIELDS
    )
    return (
        "(declare-datatypes ((State 0))\n"
        "  (((mkState\n"
        f"{fields}))))"
    )


def _state_equalities(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "       (DeterministicFinalContract x b y)"
    return """\
       (= (s_destination_length s) (x_destination_length x))
       (= (s_relation_initialized_length s) (x_destination_length x))
       (= (s_relation_values_length s) (x_destination_length x))
       (= (s_destination_storage s) (WriteCloneFinalStorage x))
       (= (s_destination_allocation s) (x_destination_allocation x))
       (= (s_destination_address s) (x_destination_address x))
       (= (s_destination_provenance s) (x_destination_provenance x))
       (= (s_destination_borrow s) (x_destination_borrow x))
       (= (s_destination_allocation_base s)
          (x_destination_allocation_base x))
       (= (s_destination_allocation_bytes s)
          (x_destination_allocation_bytes x))
       (= (s_source_length s) (x_source_length x))
       (= (s_source_values s) (x_source_values x))
       (= (s_source_allocation s) (x_source_allocation x))
       (= (s_source_address s) (x_source_address x))
       (= (s_source_provenance s) (x_source_provenance x))
       (= (s_source_allocation_base s) (x_source_allocation_base x))
       (= (s_source_allocation_bytes s) (x_source_allocation_bytes x))
       (= (s_return_length s) (AssumeInitMutReturnLength x))
       (= (s_return_values s) (AssumeInitMutReturnValues x))
       (= (s_return_allocation s) (AssumeInitMutReturnAllocation x))
       (= (s_return_address s) (AssumeInitMutReturnAddress x))
       (= (s_return_provenance s) (AssumeInitMutReturnProvenance x))
       (= (s_return_borrow s) (AssumeInitMutReturnBorrow x))
       (= (s_clone_state s) (CloneFinalState x b))
       (= (s_destruct_state s) (x_destruct_initial_state x))
       (= (s_element_size s) (x_element_size x))
       (= (s_element_alignment s) (x_element_alignment x))
       (= (s_isize_max s) (x_isize_max x))
       (= (s_address_space_limit s) (x_address_space_limit x))
       (= (s_frame_token s) (x_frame_token x))
       (ActiveFinalDestinationLengthConjunct
         x (s_destination_length s))
       (ActiveInitialRelationWellFormedConjunct x)
       (ActiveFinalRelationWellFormedConjunct
         (s_destination_length s)
         (s_relation_initialized_length s)
         (s_relation_values_length s))
       (ActiveWrittenFromConjunct
         x
         (s_destination_length s)
         (s_relation_initialized_length s)
         (s_relation_values_length s)
         (s_destination_storage s))
       (ActiveAllInitializedConjunct
         (s_destination_storage s) (s_return_values s))
       (ActiveFinalReturnLengthConjunct x (s_return_length s))
       (ActiveFinalStorageEqualsReturnConjunct
         (s_destination_storage s) (s_return_values s))"""


def _equivalence_body(purpose: str) -> str:
    equalities = [
        f"(= ({selector} y1) ({selector} y2))"
        for selector, _ in OUTPUT_FIELDS
    ]
    if purpose == PRIMARY:
        equalities.extend(
            f"(= ({selector} s1) ({selector} s2))"
            for selector, _ in STATE_FIELDS
        )
    return "  (and " + "\n       ".join(equalities) + "))"


def _source_transitions(purpose: str) -> tuple[str, ...]:
    if purpose == EXACT_OUTPUT:
        return OUTPUT_SOURCE_TRANSITIONS
    return (
        *OUTPUT_SOURCE_TRANSITIONS,
        "WriteCloneFinalStorage",
        "CloneFinalState",
    )


def _model_text(purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-119 obligation purpose: {purpose}")
    output_equalities = "\n".join(
        f"       (= ({selector} y) ({transition} x))"
        for (selector, _), transition in zip(
            OUTPUT_FIELDS, OUTPUT_SOURCE_TRANSITIONS, strict=True
        )
    )
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Purpose: {purpose}
; Clone values and state transitions are genuine per-call observations.
; Source order, call/write counts, initialized-prefix behavior, storage, and
; the final assume_init_mut return are derived below the public target.
(set-logic ALL)
(declare-datatypes ((Cell 0))
  (((Uninitialized)
    (Initialized (initialized_value Int)))))
(declare-datatypes ((CloneValue 0))
  (((Cloned (cloned_value Int)))))
(declare-datatypes ((CallbackOutcome 0))
  (((Completed) (Panicked) (NotCalled))))
(declare-datatypes ((Input 0))
  (((mkInput
      (x_destination_length Int)
      (x_relation_initialized_length Int)
      (x_relation_values_length Int)
      (x_destination_storage (Array Int Cell))
      (x_source_length Int)
      (x_source_values (Array Int Int))
      (x_destination_allocation Int)
      (x_destination_address Int)
      (x_destination_provenance Int)
      (x_destination_borrow Int)
      (x_destination_allocation_base Int)
      (x_destination_allocation_bytes Int)
      (x_source_allocation Int)
      (x_source_address Int)
      (x_source_provenance Int)
      (x_source_allocation_base Int)
      (x_source_allocation_bytes Int)
      (x_element_size Int)
      (x_element_alignment Int)
      (x_isize_max Int)
      (x_address_space_limit Int)
      (x_frame_token Int)
      (x_clone_initial_state Int)
      (x_destruct_initial_state Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_destination_length Int)
      (b_relation_initialized_length Int)
      (b_relation_values_length Int)
      (b_destination_storage (Array Int Cell))
      (b_source_length Int)
      (b_source_values (Array Int Int))
      (b_destination_allocation Int)
      (b_destination_address Int)
      (b_destination_provenance Int)
      (b_destination_borrow Int)
      (b_destination_allocation_base Int)
      (b_destination_allocation_bytes Int)
      (b_source_allocation Int)
      (b_source_address Int)
      (b_source_provenance Int)
      (b_source_allocation_base Int)
      (b_source_allocation_bytes Int)
      (b_element_size Int)
      (b_element_alignment Int)
      (b_isize_max Int)
      (b_address_space_limit Int)
      (b_frame_token Int)
      (b_clone_initial_state Int)
      (b_destruct_initial_state Int)
      (b_clone_result (Array Int CloneValue))
      (b_clone_state_before (Array Int Int))
      (b_clone_state_after (Array Int Int))
      (b_clone_outcome (Array Int CallbackOutcome))
      (b_destruct_state_before (Array Int Int))
      (b_destruct_state_after (Array Int Int))
      (b_destruct_outcome (Array Int CallbackOutcome))))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_return_allocation Int)
      (y_return_address Int)
      (y_return_provenance Int)
      (y_return_borrow Int)
      (y_return_length Int)
      (y_return_values (Array Int Int))))))
{_state_declaration(purpose)}
(declare-datatypes ((PanicState 0))
  (((mkPanicState
      (p_final_storage (Array Int Cell))
      (p_clone_call_count Int)
      (p_write_count Int)
      (p_guard_initialized Int)
      (p_cleanup_drop_count Int)
      (p_clone_state_before_panic Int)
      (p_destruct_state Int)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun CopyByteCount ((x Input)) Int
  (* (x_destination_length x) (x_element_size x)))
(define-fun BoundaryInputsObserved ((x Input) (b Boundary)) Bool
  (and (= (b_destination_length b) (x_destination_length x))
       (= (b_relation_initialized_length b)
          (x_relation_initialized_length x))
       (= (b_relation_values_length b) (x_relation_values_length x))
       (= (b_destination_storage b) (x_destination_storage x))
       (= (b_source_length b) (x_source_length x))
       (= (b_source_values b) (x_source_values x))
       (= (b_destination_allocation b) (x_destination_allocation x))
       (= (b_destination_address b) (x_destination_address x))
       (= (b_destination_provenance b) (x_destination_provenance x))
       (= (b_destination_borrow b) (x_destination_borrow x))
       (= (b_destination_allocation_base b)
          (x_destination_allocation_base x))
       (= (b_destination_allocation_bytes b)
          (x_destination_allocation_bytes x))
       (= (b_source_allocation b) (x_source_allocation x))
       (= (b_source_address b) (x_source_address x))
       (= (b_source_provenance b) (x_source_provenance x))
       (= (b_source_allocation_base b) (x_source_allocation_base x))
       (= (b_source_allocation_bytes b) (x_source_allocation_bytes x))
       (= (b_element_size b) (x_element_size x))
       (= (b_element_alignment b) (x_element_alignment x))
       (= (b_isize_max b) (x_isize_max x))
       (= (b_address_space_limit b) (x_address_space_limit x))
       (= (b_frame_token b) (x_frame_token x))
       (= (b_clone_initial_state b) (x_clone_initial_state x))
       (= (b_destruct_initial_state b) (x_destruct_initial_state x))))
(define-fun ValidCloneMemory ((x Input)) Bool
  (and (> (x_destination_address x) 0)
       (> (x_source_address x) 0)
       (> (x_destination_borrow x) 0)
       (>= (x_destination_allocation x) 0)
       (>= (x_destination_provenance x) 0)
       (>= (x_destination_allocation_base x) 0)
       (>= (x_destination_allocation_bytes x) 0)
       (>= (x_source_allocation x) 0)
       (>= (x_source_provenance x) 0)
       (>= (x_source_allocation_base x) 0)
       (>= (x_source_allocation_bytes x) 0)
       (>= (x_element_size x) 0)
       (> (x_element_alignment x) 0)
       (> (x_isize_max x) 0)
       (> (x_address_space_limit x) 0)
       (= (mod (x_destination_address x) (x_element_alignment x)) 0)
       (= (mod (x_source_address x) (x_element_alignment x)) 0)
       (or (= (x_element_size x) 0)
           (and (>= (x_element_size x) (x_element_alignment x))
                (= (mod (x_element_size x) (x_element_alignment x)) 0)))
       (<= (CopyByteCount x) (x_isize_max x))
       (<= (+ (x_destination_address x) (CopyByteCount x))
           (x_address_space_limit x))
       (<= (+ (x_source_address x) (CopyByteCount x))
           (x_address_space_limit x))
       (or (= (CopyByteCount x) 0)
           (and (> (x_destination_allocation x) 0)
                (> (x_destination_provenance x) 0)
                (> (x_source_allocation x) 0)
                (> (x_source_provenance x) 0)
                (<= (x_destination_allocation_base x)
                    (x_destination_address x))
                (<= (+ (x_destination_address x) (CopyByteCount x))
                    (+ (x_destination_allocation_base x)
                       (x_destination_allocation_bytes x)))
                (<= (x_source_allocation_base x) (x_source_address x))
                (<= (+ (x_source_address x) (CopyByteCount x))
                    (+ (x_source_allocation_base x)
                       (x_source_allocation_bytes x)))
                (or (not (= (x_destination_allocation x)
                            (x_source_allocation x)))
                    (<= (+ (x_destination_address x) (CopyByteCount x))
                        (x_source_address x))
                    (<= (+ (x_source_address x) (CopyByteCount x))
                        (x_destination_address x)))))))
(define-fun CloneIndexAtStep ((x Input) (step Int)) Int step)
(define-fun WriteIndexAtStep ((x Input) (step Int)) Int step)
(define-fun CloneOperationCount ((x Input)) Int (x_source_length x))
(define-fun WriteOperationCount ((x Input)) Int (x_destination_length x))
(define-fun WriteCloneFinalStorage
  ((x Input)) (Array Int Cell)
  ((_ map Initialized) (x_source_values x)))
(define-fun WriteStorageAfterStep
  ((storage (Array Int Cell)) (index Int) (value Int))
  (Array Int Cell)
  (store storage index (Initialized value)))
(define-fun-rec WriteStorageAfterSteps
  ((x Input) (b Boundary) (count Int)) (Array Int Cell)
  (ite (<= count 0)
       (x_destination_storage x)
       (let ((step (- count 1)))
         (WriteStorageAfterStep
           (WriteStorageAfterSteps x b step)
           (WriteIndexAtStep x step)
           (cloned_value
             (select (b_clone_result b) (CloneIndexAtStep x step)))))))
(define-fun-rec CloneCompletedThrough
  ((x Input) (b Boundary) (count Int)) Bool
  (ite (<= count 0)
       true
       (let ((step (- count 1)))
         (let ((index (CloneIndexAtStep x step)))
           (and
             (CloneCompletedThrough x b step)
             (= index step)
             ((_ is Cloned) (select (b_clone_result b) index))
             (= (select (b_clone_outcome b) index) Completed)
             (= (select (b_clone_state_before b) index)
                (ite (= step 0)
                     (x_clone_initial_state x)
                     (select
                       (b_clone_state_after b)
                       (CloneIndexAtStep x (- step 1))))))))))
(define-fun-rec WriteCompletedThrough
  ((x Input) (b Boundary) (final_storage (Array Int Cell)) (count Int))
  Bool
  (ite (<= count 0)
       true
       (let ((step (- count 1)))
         (let ((clone_index (CloneIndexAtStep x step))
               (write_index (WriteIndexAtStep x step)))
           (and
             (WriteCompletedThrough x b final_storage step)
             (= clone_index step)
             (= write_index step)
             (= (select final_storage write_index)
                (select
                  (WriteStorageAfterSteps x b count)
                  write_index)))))))
(define-fun-rec NoCleanupThrough
  ((x Input) (b Boundary) (count Int)) Bool
  (ite (<= count 0)
       true
       (let ((index (- count 1)))
         (and
           (NoCleanupThrough x b index)
           (= (select (b_destruct_outcome b) index) NotCalled)
           (= (select (b_destruct_state_before b) index)
              (x_destruct_initial_state x))
           (= (select (b_destruct_state_after b) index)
              (x_destruct_initial_state x))))))
(define-fun CloneResultValues ((b Boundary)) (Array Int Int)
  ((_ map cloned_value) (b_clone_result b)))
(define-fun CloneResultsMatchSource ((x Input) (b Boundary)) Bool
  (= (CloneResultValues b) (x_source_values x)))
(define-fun CloneFinalState ((x Input) (b Boundary)) Int
  (ite (= (CloneOperationCount x) 0)
       (x_clone_initial_state x)
       (select
         (b_clone_state_after b)
         (CloneIndexAtStep x (- (CloneOperationCount x) 1)))))
(define-fun CloneWriteSourceExecution_T ((x Input) (b Boundary)) Bool
  (and (= (CloneOperationCount x) (x_source_length x))
       (= (WriteOperationCount x) (x_destination_length x))
       (= (CloneOperationCount x) (WriteOperationCount x))
       (CloneCompletedThrough x b (CloneOperationCount x))
       (WriteCompletedThrough
         x b (WriteCloneFinalStorage x) (WriteOperationCount x))
       (NoCleanupThrough x b (WriteOperationCount x))))
(define-fun CleanupDropIndexAtStep
  ((panic_index Int) (step Int)) Int
  step)
(define-fun PanicCloneCallCount ((panic_index Int)) Int
  (+ panic_index 1))
(define-fun PanicWriteOperationCount ((panic_index Int)) Int
  panic_index)
(define-fun GuardInitializedAtPanic ((panic_index Int)) Int
  panic_index)
(define-fun CleanupDropOperationCount ((panic_index Int)) Int
  panic_index)
(define-fun PanicWriteStorageAfterSteps
  ((x Input) (b Boundary) (count Int)) (Array Int Cell)
  (WriteStorageAfterSteps x b count))
(define-fun-rec PanicCleanupStorageAfterSteps
  ((x Input) (b Boundary) (panic_index Int) (count Int))
  (Array Int Cell)
  (ite (<= count 0)
       (PanicWriteStorageAfterSteps x b panic_index)
       (let ((step (- count 1)))
         (store
           (PanicCleanupStorageAfterSteps x b panic_index step)
           (CleanupDropIndexAtStep panic_index step)
           Uninitialized))))
(define-fun ClonePanicsAtStep
  ((x Input) (b Boundary) (panic_index Int)) Bool
  (let ((index (CloneIndexAtStep x panic_index)))
    (and (= index panic_index)
         (= (select (b_clone_outcome b) index) Panicked)
         (= (select (b_clone_state_before b) index)
            (ite (= panic_index 0)
                 (x_clone_initial_state x)
                 (select
                   (b_clone_state_after b)
                   (CloneIndexAtStep x (- panic_index 1))))))))
(define-fun-rec CleanupDestructCompletedThrough
  ((x Input) (b Boundary) (panic_index Int) (count Int)) Bool
  (ite (<= count 0)
       true
       (let ((step (- count 1)))
         (let ((index (CleanupDropIndexAtStep panic_index step)))
           (and
             (CleanupDestructCompletedThrough x b panic_index step)
             (= index step)
             (= (select (b_destruct_outcome b) index) Completed)
             (= (select (b_destruct_state_before b) index)
                (ite (= step 0)
                     (x_destruct_initial_state x)
                     (select
                       (b_destruct_state_after b)
                       (CleanupDropIndexAtStep panic_index (- step 1))))))))))
(define-fun PanicFinalDestructState
  ((x Input) (b Boundary) (panic_index Int)) Int
  (ite (= (CleanupDropOperationCount panic_index) 0)
       (x_destruct_initial_state x)
       (select
         (b_destruct_state_after b)
         (CleanupDropIndexAtStep
           panic_index
           (- (CleanupDropOperationCount panic_index) 1)))))
(define-fun PanicBoundary_T
  ((x Input) (b Boundary) (panic_index Int)) Bool
  (and (BoundaryInputsObserved x b)
       (>= panic_index 0)
       (< panic_index (x_source_length x))
       (CloneCompletedThrough x b panic_index)
       (ClonePanicsAtStep x b panic_index)
       (CleanupDestructCompletedThrough
         x b panic_index (CleanupDropOperationCount panic_index))))
(define-fun PanicTargetDefinition_T
  ((x Input) (b Boundary) (panic_index Int) (p PanicState)) Bool
  (and (BoundaryInputsObserved x b)
       (= (PanicCloneCallCount panic_index) (+ panic_index 1))
       (= (PanicWriteOperationCount panic_index) panic_index)
       (= (GuardInitializedAtPanic panic_index) panic_index)
       (= (CleanupDropOperationCount panic_index) panic_index)
       (CloneCompletedThrough x b (PanicWriteOperationCount panic_index))
       (ClonePanicsAtStep x b panic_index)
       (WriteCompletedThrough
         x
         b
         (PanicWriteStorageAfterSteps
           x b (PanicWriteOperationCount panic_index))
         (PanicWriteOperationCount panic_index))
       (CleanupDestructCompletedThrough
         x b panic_index (CleanupDropOperationCount panic_index))
       (= (p_final_storage p)
          (PanicCleanupStorageAfterSteps
            x b panic_index (CleanupDropOperationCount panic_index)))
       (= (p_clone_call_count p) (PanicCloneCallCount panic_index))
       (= (p_write_count p) (PanicWriteOperationCount panic_index))
       (= (p_guard_initialized p) (GuardInitializedAtPanic panic_index))
       (= (p_cleanup_drop_count p)
          (CleanupDropOperationCount panic_index))
       (= (p_clone_state_before_panic p)
          (select
            (b_clone_state_before b)
            (CloneIndexAtStep x panic_index)))
       (= (p_destruct_state p)
          (PanicFinalDestructState x b panic_index))))
(define-fun PanicSpec_T
  ((x Input) (b Boundary) (panic_index Int) (p PanicState)) Bool
  (PanicTargetDefinition_T x b panic_index p))
; Lower target 026 composition: the final initialized storage is reborrowed
; without changing allocation, address, provenance, borrow, length, or values.
(define-fun AssumeInitMutReturnAllocation ((x Input)) Int
  (x_destination_allocation x))
(define-fun AssumeInitMutReturnAddress ((x Input)) Int
  (x_destination_address x))
(define-fun AssumeInitMutReturnProvenance ((x Input)) Int
  (x_destination_provenance x))
(define-fun AssumeInitMutReturnBorrow ((x Input)) Int
  (x_destination_borrow x))
(define-fun AssumeInitMutReturnLength ((x Input)) Int
  (x_destination_length x))
(define-fun AssumeInitMutReturnValues
  ((x Input)) (Array Int Int)
  (x_source_values x))
(define-fun ActiveReturnEqualsSourceConjunct
  ((x Input) (y Output)) Bool
  (= (y_return_values y) (x_source_values x)))
(define-fun ActiveReturnLengthConjunct ((x Input) (y Output)) Bool
  (= (y_return_length y) (x_source_length x)))
(define-fun ActiveFinalDestinationLengthConjunct
  ((x Input) (final_length Int)) Bool
  (= final_length (x_destination_length x)))
(define-fun ActiveInitialRelationWellFormedConjunct ((x Input)) Bool
  (and (>= (x_destination_length x) 0)
       (= (x_relation_initialized_length x) (x_destination_length x))
       (= (x_relation_values_length x) (x_destination_length x))))
(define-fun ActiveFinalRelationWellFormedConjunct
  ((final_length Int)
   (final_initialized_length Int)
   (final_values_length Int)) Bool
  (and (>= final_length 0)
       (= final_initialized_length final_length)
       (= final_values_length final_length)))
(define-fun ActiveWrittenFromConjunct
  ((x Input)
   (final_length Int)
   (final_initialized_length Int)
   (final_values_length Int)
   (final_storage (Array Int Cell))) Bool
  (and (= (x_relation_initialized_length x) (x_source_length x))
       (= (x_relation_values_length x) (x_source_length x))
       (= final_length (x_source_length x))
       (= final_initialized_length (x_source_length x))
       (= final_values_length (x_source_length x))
       (= final_storage ((_ map Initialized) (x_source_values x)))))
(define-fun ActiveAllInitializedConjunct
  ((final_storage (Array Int Cell))
   (final_values (Array Int Int))) Bool
  (= final_storage ((_ map Initialized) final_values)))
(define-fun ActiveFinalReturnLengthConjunct
  ((x Input) (final_return_length Int)) Bool
  (= final_return_length (x_source_length x)))
(define-fun ActiveFinalStorageEqualsReturnConjunct
  ((final_storage (Array Int Cell))
   (final_return_values (Array Int Int))) Bool
  (= final_storage ((_ map Initialized) final_return_values)))
(define-fun DeterministicFinalContract
  ((x Input) (b Boundary) (y Output)) Bool
  (and (ActiveFinalDestinationLengthConjunct
         x (x_destination_length x))
       (ActiveInitialRelationWellFormedConjunct x)
       (ActiveFinalRelationWellFormedConjunct
         (x_destination_length x)
         (x_destination_length x)
         (x_destination_length x))
       (ActiveWrittenFromConjunct
         x
         (x_destination_length x)
         (x_destination_length x)
         (x_destination_length x)
         (WriteCloneFinalStorage x))
       (ActiveAllInitializedConjunct
         (WriteCloneFinalStorage x)
         (AssumeInitMutReturnValues x))
       (ActiveFinalReturnLengthConjunct x (AssumeInitMutReturnLength x))
       (ActiveFinalStorageEqualsReturnConjunct
         (WriteCloneFinalStorage x)
         (AssumeInitMutReturnValues x))
       (= (y_return_values y) (AssumeInitMutReturnValues x))))
(define-fun Requires_T ((x Input)) Bool
  (and (>= (x_destination_length x) 0)
       (= (x_destination_length x) (x_source_length x))
       (= (x_relation_initialized_length x) (x_destination_length x))
       (= (x_relation_values_length x) (x_destination_length x))
       (ValidCloneMemory x)))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (BoundaryInputsObserved x b)
       (>= (b_destination_length b) 0)
       (>= (b_source_length b) 0)
       (> (b_destination_address b) 0)
       (> (b_source_address b) 0)
       (> (b_destination_borrow b) 0)
       (> (b_element_alignment b) 0)
       (> (b_isize_max b) 0)
       (> (b_address_space_limit b) 0)
       (CloneCompletedThrough x b (CloneOperationCount x))
       (NoCleanupThrough x b (WriteOperationCount x))))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (BoundaryInputsObserved x b)
       (CloneWriteSourceExecution_T x b)
       (CloneResultsMatchSource x b)
{output_equalities}
       (ActiveReturnEqualsSourceConjunct x y)
       (ActiveReturnLengthConjunct x y)
{_state_equalities(purpose)}))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_equivalence_body(purpose)}
"""


def obligation_text(purpose: str) -> str:
    return _model_text(purpose) + """\
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


def _principal_observations(purpose: str) -> list[dict[str, str]]:
    result = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort,
        }
        for selector, sort in OUTPUT_FIELDS
    ]
    if purpose == PRIMARY:
        result.extend(
            {
                "selector": selector,
                "left": "state1",
                "right": "state2",
                "sort": sort,
            }
            for selector, sort in STATE_FIELDS
        )
    return result


def _boundary_fields() -> list[dict[str, Any]]:
    roles = {
        "b_destination_length": "input_initialization",
        "b_relation_initialized_length": "input_initialization",
        "b_relation_values_length": "input_initialization",
        "b_destination_storage": "input_initialization",
        "b_source_length": "input_memory",
        "b_source_values": "input_memory",
        "b_destination_allocation": "input_memory",
        "b_destination_address": "input_memory",
        "b_destination_provenance": "input_provenance",
        "b_destination_borrow": "input_provenance",
        "b_destination_allocation_base": "input_memory",
        "b_destination_allocation_bytes": "input_memory",
        "b_source_allocation": "input_memory",
        "b_source_address": "input_memory",
        "b_source_provenance": "input_provenance",
        "b_source_allocation_base": "input_memory",
        "b_source_allocation_bytes": "input_memory",
        "b_element_size": "input_layout",
        "b_element_alignment": "input_layout",
        "b_isize_max": "input_layout",
        "b_address_space_limit": "input_layout",
        "b_frame_token": "input_memory",
        "b_clone_initial_state": "callback_argument",
        "b_destruct_initial_state": "callback_argument",
        "b_clone_result": "callback_result",
        "b_clone_state_before": "callback_state_transition",
        "b_clone_state_after": "callback_state_transition",
        "b_clone_outcome": "callback_panic",
        "b_destruct_state_before": "callback_state_transition",
        "b_destruct_state_after": "callback_state_transition",
        "b_destruct_outcome": "callback_panic",
    }
    callback_fields = {
        "b_clone_initial_state",
        "b_clone_result",
        "b_clone_state_before",
        "b_clone_state_after",
        "b_clone_outcome",
        "b_destruct_initial_state",
        "b_destruct_state_before",
        "b_destruct_state_after",
        "b_destruct_outcome",
    }
    return [
        {
            "selector": selector,
            "role": role,
            "source_citations": [
                TARGET_SOURCE_REFERENCE,
                GUARD_SOURCE_REFERENCE,
                CLONE_SOURCE_REFERENCE,
                ASSUME_INIT_MUT_REFERENCE,
            ],
            "trust_site_ids": (
                ["TS-119-D003", "TS-119-D004", "TS-119-E001", "TS-119-E002"]
                if selector in callback_fields
                else ["TS-119-D002", "TS-119-D003", "TS-119-E001", "TS-119-E003"]
            ),
        }
        for selector, role in roles.items()
    ]


def obligation_metadata(purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-119 obligation purpose: {purpose}")
    source_transitions = _source_transitions(purpose)
    return {
        "schema_version": 3,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "domain": {
            "length": "arbitrary equal nonnegative destination/source lengths",
            "initialization": "arbitrary initial destination cells",
            "clone": (
                "one successful Clone result/outcome/state transition per index "
                "on the normal-return path; arbitrary Clone implementations remain observable"
            ),
            "memory": (
                "nonnull aligned nonoverlapping source/destination ranges for "
                "nonzero byte counts, with empty and ZST behavior represented"
            ),
            "panic": (
                "normal theorem requires completed Clone observations and no "
                "Guard cleanup; panic probes reuse the same successful-prefix "
                "transition before source-derived initialized-prefix cleanup"
            ),
        },
        "contract_translation": {
            "active_conjuncts": list(ACTIVE_CONJUNCT_SYMBOLS),
            "source_flow": [
                "equal-length assertion and full source prefix",
                "Guard initialized count starts at zero",
                "source-ordered Clone then one MaybeUninit write per index",
                "Guard count increments only after each successful write",
                "forget Guard after all writes",
                "compose target 026 layout-preserving assume_init_mut cast",
            ],
            "final_state_projection": (
                "explicit exact theorem state"
                if purpose == PRIMARY
                else "source-derived final contract retained while comparing exact return"
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                "initial source and destination storage/memory identity",
                "initial layout, provenance, mutable borrow, and frame",
                "individual Clone results, outcomes, and state transitions keyed by index",
                "individual Destruct outcomes and state transitions used by Guard cleanup",
            ],
            "excluded_observations": [
                "returned reference",
                "resulting destination storage",
                "aggregate final Clone or Destruct state",
                "clone/write/drop order or count",
                "answer encoding",
                "complete target execution trace",
            ],
            "admitted_trust_site_ids": list(ADMITTED_TRUST_SITES),
            "excluded_retained_trust_site_ids": [],
            "context_only_trust_site_ids": list(CONTEXT_ONLY_TRUST_SITES),
            "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
            "source_backed_replacement_ids": [],
            "narrower_than_target": True,
        },
        "source_backed_replacements": [],
        "target_definition": "TargetDefinition_T",
        "theorem_variables": {
            "input": "x",
            "boundary": "b",
            "output1": "y1",
            "state1": "s1",
            "output2": "y2",
            "state2": "s2",
        },
        "boundary_fields": _boundary_fields(),
        "declared_functions": [],
        "source_transition_definitions": list(source_transitions),
        "source_transition_bindings": {
            "clone_observations": {
                "symbols": [
                    "CloneCompletedThrough",
                    "NoCleanupThrough",
                    "CloneResultValues",
                    "CloneFinalState",
                ],
                "trust_site_ids": [
                    "TS-119-D003",
                    "TS-119-D004",
                    "TS-119-E001",
                    "TS-119-E002",
                ],
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    CLONE_SOURCE_REFERENCE,
                ],
            },
            "one_step_writes": {
                "symbols": [
                    "CloneIndexAtStep",
                    "WriteIndexAtStep",
                    "CloneOperationCount",
                    "WriteOperationCount",
                    "WriteStorageAfterStep",
                    "WriteStorageAfterSteps",
                    "WriteCompletedThrough",
                    "WriteCloneFinalStorage",
                    "CloneWriteSourceExecution_T",
                ],
                "trust_site_ids": [
                    "TS-119-D003",
                    "TS-119-D004",
                    "TS-119-E001",
                    "TS-119-E002",
                ],
                "source_citations": [TARGET_SOURCE_REFERENCE],
                "restriction": (
                    "retained sites supply only one Clone/write step; the "
                    "source loop derives aggregate order, count, and storage"
                ),
            },
            "assume_init_mut_composition": {
                "symbols": list(OUTPUT_SOURCE_TRANSITIONS),
                "trust_site_ids": [
                    "TS-119-D002",
                    "TS-119-E003",
                ],
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    ASSUME_INIT_MUT_REFERENCE,
                ],
                "lower_target": "core::slice::assume_init_mut",
                "lower_active_contract_sha256": (
                    "8d0e90b87ee12383ef38b353ff71f43a4136f565d0ae0f63651ee295c06f649a"
                ),
            },
            "panic_cleanup": {
                "symbols": [
                    "PanicWriteStorageAfterSteps",
                    "PanicCleanupStorageAfterSteps",
                    "CleanupDropIndexAtStep",
                    "CleanupDestructCompletedThrough",
                    "PanicBoundary_T",
                    "PanicTargetDefinition_T",
                    "PanicSpec_T",
                ],
                "trust_site_ids": [
                    "TS-119-D003",
                    "TS-119-D004",
                    "TS-119-E001",
                    "TS-119-E002",
                ],
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    GUARD_SOURCE_REFERENCE,
                ],
                "evidence": (
                    "target-specific clone-panic probes invoke the reviewed "
                    "panic boundary and target definition"
                ),
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "returned reference and all destination/source/callback/layout/frame state"
            if purpose == PRIMARY
            else "returned reference identity, length, and values"
        ),
        "principal_observations": _principal_observations(purpose),
    }


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return obligation_text(purpose), obligation_metadata(purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError("target-119 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-119 metadata differs from the reviewed clone/write translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-119 SMT differs from the reviewed clone/write translation"
        )


def _cell_array(
    values: dict[int, int],
    initialized: tuple[int, ...] = (),
) -> str:
    expression = "((as const (Array Int Cell)) Uninitialized)"
    for index in initialized:
        expression = (
            f"(store {expression} {index} (Initialized {values[index]}))"
        )
    return expression


def _int_array(values: dict[int, int], default: int = 0) -> str:
    expression = f"((as const (Array Int Int)) {default})"
    for index, value in sorted(values.items()):
        expression = f"(store {expression} {index} {value})"
    return expression


def _clone_array(values: dict[int, int]) -> str:
    expression = "((as const (Array Int CloneValue)) (Cloned 0))"
    for index, value in sorted(values.items()):
        expression = f"(store {expression} {index} (Cloned {value}))"
    return expression


def _outcome_array(completed: tuple[int, ...]) -> str:
    expression = "((as const (Array Int CallbackOutcome)) Panicked)"
    for index in completed:
        expression = f"(store {expression} {index} Completed)"
    return expression


def _destruct_outcome_array(completed: tuple[int, ...]) -> str:
    expression = "((as const (Array Int CallbackOutcome)) NotCalled)"
    for index in completed:
        expression = f"(store {expression} {index} Completed)"
    return expression


def _case(
    *,
    destination_length: int = 3,
    source_length: int | None = None,
    source_values: dict[int, int] | None = None,
    initial_values: dict[int, int] | None = None,
    initially_initialized: tuple[int, ...] = (),
) -> dict[str, Any]:
    source_length = (
        destination_length if source_length is None else source_length
    )
    source_values = source_values or {
        index: 11 * (index + 1) for index in range(source_length)
    }
    before = {index: 100 + index for index in range(destination_length)}
    after = {index: 101 + index for index in range(destination_length)}
    destruct_unchanged = {
        index: 200 for index in range(destination_length)
    }
    return {
        "destination_length": destination_length,
        "relation_initialized_length": destination_length,
        "relation_values_length": destination_length,
        "destination_storage_values": initial_values or {},
        "initially_initialized": initially_initialized,
        "source_length": source_length,
        "source_values": source_values,
        "destination_allocation": 61,
        "destination_address": 4096,
        "destination_provenance": 161,
        "destination_borrow": 261,
        "destination_allocation_base": 4096,
        "destination_allocation_bytes": 128,
        "source_allocation": 62,
        "source_address": 8192,
        "source_provenance": 162,
        "source_allocation_base": 8192,
        "source_allocation_bytes": 128,
        "element_size": 4,
        "element_alignment": 4,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "frame_token": 999,
        "clone_initial_state": 100,
        "destruct_initial_state": 200,
        "clone_result": source_values,
        "clone_before": before,
        "clone_after": after,
        "completed": tuple(range(destination_length)),
        "destruct_before": destruct_unchanged,
        "destruct_after": destruct_unchanged,
        "destruct_completed": (),
    }


PROBE_CASES: dict[str, dict[str, Any]] = {
    "valid_empty": {
        **_case(destination_length=0),
        "kind": "valid",
        "expected": "sat",
    },
    "valid_uninitialized_destination": {
        **_case(),
        "kind": "valid",
        "expected": "sat",
    },
    "valid_mixed_destination": {
        **_case(
            initial_values={0: 90, 2: 92},
            initially_initialized=(0, 2),
        ),
        "kind": "valid",
        "expected": "sat",
    },
    "valid_zst_nonempty": {
        **_case(),
        "element_size": 0,
        "destination_allocation": 0,
        "destination_provenance": 0,
        "source_allocation": 0,
        "source_provenance": 0,
        "kind": "valid",
        "expected": "sat",
    },
    "invalid_unequal_lengths": {
        **_case(destination_length=3, source_length=2),
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_clone_result": {
        **_case(),
        "clone_result": {0: 11, 1: 999, 2: 33},
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_clone_callback_order": {
        **_case(),
        "clone_before": {0: 100, 1: 999, 2: 102},
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_no_op_write": {
        **_case(
            initial_values={0: 90, 1: 91, 2: 92},
            initially_initialized=(0, 1, 2),
        ),
        "kind": "no_op_write",
        "expected": "unsat",
    },
    "invalid_partial_write": {
        **_case(),
        "kind": "partial_write",
        "expected": "unsat",
    },
    "invalid_omitted_initialization": {
        **_case(),
        "kind": "omitted_initialization",
        "expected": "unsat",
    },
    "invalid_duplicate_write": {
        **_case(),
        "kind": "duplicate_write",
        "expected": "unsat",
    },
    "invalid_out_of_order_write": {
        **_case(),
        "kind": "out_of_order_write",
        "expected": "unsat",
    },
    "invalid_clone_count": {
        **_case(),
        "kind": "clone_count",
        "expected": "unsat",
    },
    "invalid_write_count": {
        **_case(),
        "kind": "write_count",
        "expected": "unsat",
    },
    "invalid_callback_state": {
        **_case(),
        "kind": "callback_state",
        "expected": "unsat",
    },
    "invalid_wrong_return_identity": {
        **_case(),
        "kind": "return_identity",
        "expected": "unsat",
    },
    "invalid_changed_source": {
        **_case(),
        "kind": "changed_source",
        "expected": "unsat",
    },
    "invalid_changed_frame": {
        **_case(),
        "kind": "changed_frame",
        "expected": "unsat",
    },
    "invalid_null_pointer": {
        **_case(),
        "destination_address": 0,
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_missing_provenance": {
        **_case(),
        "source_provenance": 0,
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_misaligned_pointer": {
        **_case(),
        "source_address": 8194,
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "valid_clone_panic_at_0": {
        "kind": "panic_lifecycle",
        "panic_index": 0,
        "expected": "sat",
    },
    "valid_clone_panic_at_1": {
        "kind": "panic_lifecycle",
        "panic_index": 1,
        "expected": "sat",
    },
    "valid_clone_panic_at_2": {
        "kind": "panic_lifecycle",
        "panic_index": 2,
        "expected": "sat",
    },
    "invalid_panic_partial_cleanup": {
        "kind": "panic_lifecycle_invalid",
        "panic_index": 2,
        "fault": "partial_cleanup",
        "expected": "unsat",
    },
    "invalid_panic_duplicate_cleanup": {
        "kind": "panic_lifecycle_invalid",
        "panic_index": 2,
        "fault": "duplicate_cleanup",
        "expected": "unsat",
    },
    "invalid_panic_out_of_order_cleanup": {
        "kind": "panic_lifecycle_invalid",
        "panic_index": 2,
        "fault": "out_of_order_cleanup",
        "expected": "unsat",
    },
    "invalid_panic_wrong_guard_count": {
        "kind": "panic_lifecycle_invalid",
        "panic_index": 1,
        "fault": "wrong_guard_count",
        "expected": "unsat",
    },
    "invalid_clone_after_panic": {
        "kind": "panic_lifecycle_invalid",
        "panic_index": 1,
        "fault": "clone_after_panic",
        "expected": "unsat",
    },
}

PROBE_EXPECTED_RESULTS = {
    name: str(case["expected"]) for name, case in PROBE_CASES.items()
}


def _input_expression(case: dict[str, Any]) -> str:
    values = (
        case["destination_length"],
        case["relation_initialized_length"],
        case["relation_values_length"],
        _cell_array(
            case["destination_storage_values"],
            case["initially_initialized"],
        ),
        case["source_length"],
        _int_array(case["source_values"]),
        case["destination_allocation"],
        case["destination_address"],
        case["destination_provenance"],
        case["destination_borrow"],
        case["destination_allocation_base"],
        case["destination_allocation_bytes"],
        case["source_allocation"],
        case["source_address"],
        case["source_provenance"],
        case["source_allocation_base"],
        case["source_allocation_bytes"],
        case["element_size"],
        case["element_alignment"],
        case["isize_max"],
        case["address_space_limit"],
        case["frame_token"],
        case["clone_initial_state"],
        case["destruct_initial_state"],
    )
    return "(mkInput " + " ".join(map(str, values)) + ")"


def _boundary_expression(case: dict[str, Any]) -> str:
    values = (
        case["destination_length"],
        case["relation_initialized_length"],
        case["relation_values_length"],
        _cell_array(
            case["destination_storage_values"],
            case["initially_initialized"],
        ),
        case["source_length"],
        _int_array(case["source_values"]),
        case["destination_allocation"],
        case["destination_address"],
        case["destination_provenance"],
        case["destination_borrow"],
        case["destination_allocation_base"],
        case["destination_allocation_bytes"],
        case["source_allocation"],
        case["source_address"],
        case["source_provenance"],
        case["source_allocation_base"],
        case["source_allocation_bytes"],
        case["element_size"],
        case["element_alignment"],
        case["isize_max"],
        case["address_space_limit"],
        case["frame_token"],
        case["clone_initial_state"],
        case["destruct_initial_state"],
        _clone_array(case["clone_result"]),
        _int_array(case["clone_before"]),
        _int_array(case["clone_after"]),
        _outcome_array(case["completed"]),
        _int_array(case["destruct_before"], case["destruct_initial_state"]),
        _int_array(case["destruct_after"], case["destruct_initial_state"]),
        _destruct_outcome_array(case["destruct_completed"]),
    )
    return "(mkBoundary " + " ".join(map(str, values)) + ")"


def _model_with_source_mutation(kind: str) -> str:
    text = _model_text(PRIMARY)
    mutations = {
        "duplicate_write": (
            "(define-fun WriteIndexAtStep ((x Input) (step Int)) Int step)",
            "(define-fun WriteIndexAtStep ((x Input) (step Int)) Int\n"
            "  (ite (= step 1) 0 step))",
        ),
        "out_of_order_write": (
            "(define-fun WriteIndexAtStep ((x Input) (step Int)) Int step)",
            "(define-fun WriteIndexAtStep ((x Input) (step Int)) Int\n"
            "  (- (x_destination_length x) step 1))",
        ),
        "clone_count": (
            "(define-fun CloneOperationCount ((x Input)) Int "
            "(x_source_length x))",
            "(define-fun CloneOperationCount ((x Input)) Int\n"
            "  (- (x_source_length x) 1))",
        ),
        "write_count": (
            "(define-fun WriteOperationCount ((x Input)) Int "
            "(x_destination_length x))",
            "(define-fun WriteOperationCount ((x Input)) Int\n"
            "  (- (x_destination_length x) 1))",
        ),
    }
    try:
        old, new = mutations[kind]
    except KeyError as exc:
        raise ValueError(f"unknown target-119 source mutation: {kind}") from exc
    if text.count(old) != 1:
        raise RuntimeError(f"target-119 mutation anchor changed: {kind}")
    return text.replace(old, new, 1)


def _panic_model_with_source_mutation(fault: str | None) -> str:
    text = _model_text(PRIMARY)
    if fault is None:
        return text
    mutations = {
        "partial_cleanup": (
            "(define-fun CleanupDropOperationCount ((panic_index Int)) Int\n"
            "  panic_index)",
            "(define-fun CleanupDropOperationCount ((panic_index Int)) Int\n"
            "  (- panic_index 1))",
        ),
        "duplicate_cleanup": (
            "(define-fun CleanupDropIndexAtStep\n"
            "  ((panic_index Int) (step Int)) Int\n"
            "  step)",
            "(define-fun CleanupDropIndexAtStep\n"
            "  ((panic_index Int) (step Int)) Int\n"
            "  (ite (= step 1) 0 step))",
        ),
        "out_of_order_cleanup": (
            "(define-fun CleanupDropIndexAtStep\n"
            "  ((panic_index Int) (step Int)) Int\n"
            "  step)",
            "(define-fun CleanupDropIndexAtStep\n"
            "  ((panic_index Int) (step Int)) Int\n"
            "  (- panic_index step 1))",
        ),
        "wrong_guard_count": (
            "(define-fun GuardInitializedAtPanic ((panic_index Int)) Int\n"
            "  panic_index)",
            "(define-fun GuardInitializedAtPanic ((panic_index Int)) Int\n"
            "  (+ panic_index 1))",
        ),
        "clone_after_panic": (
            "(define-fun PanicCloneCallCount ((panic_index Int)) Int\n"
            "  (+ panic_index 1))",
            "(define-fun PanicCloneCallCount ((panic_index Int)) Int\n"
            "  (+ panic_index 2))",
        ),
    }
    try:
        old, new = mutations[fault]
    except KeyError as exc:
        raise ValueError(f"unknown target-119 panic mutation: {fault}") from exc
    if text.count(old) != 1:
        raise RuntimeError(f"target-119 panic mutation anchor changed: {fault}")
    return text.replace(old, new, 1)


def _panic_case(panic: int) -> dict[str, Any]:
    case = _case()
    case["completed"] = tuple(range(panic))
    case["destruct_before"] = {
        index: 200 + index for index in range(panic)
    }
    case["destruct_after"] = {
        index: 201 + index for index in range(panic)
    }
    case["destruct_completed"] = tuple(range(panic))
    return case


def _panic_probe_text(case: dict[str, Any]) -> str:
    panic = int(case["panic_index"])
    model = _panic_model_with_source_mutation(case.get("fault"))
    probe_case = _panic_case(panic)
    assertions = [
        f"(= x {_input_expression(probe_case)})",
        f"(= b {_boundary_expression(probe_case)})",
        "(Requires_T x)",
        f"(PanicBoundary_T x b {panic})",
        f"(PanicSpec_T x b {panic} p1)",
        f"(= (p_clone_call_count p1) {panic + 1})",
        f"(= (p_write_count p1) {panic})",
        f"(= (p_guard_initialized p1) {panic})",
        f"(= (p_cleanup_drop_count p1) {panic})",
        "(= (p_final_storage p1) (x_destination_storage x))",
        f"(= (p_clone_state_before_panic p1) {100 + panic})",
        f"(= (p_destruct_state p1) {200 + panic})",
    ]
    body = "\n       ".join(assertions)
    return model + f"""\
(declare-const p1 PanicState)
(assert
  (and {body}))
(check-sat)
"""


def probe_text(name: str) -> str:
    try:
        case = PROBE_CASES[name]
    except KeyError as exc:
        raise ValueError(f"unknown target-119 probe: {name}") from exc
    if case["kind"].startswith("panic_lifecycle"):
        return _panic_probe_text(case)
    kind = case["kind"]
    model = (
        _model_with_source_mutation(kind)
        if kind
        in {
            "duplicate_write",
            "out_of_order_write",
            "clone_count",
            "write_count",
        }
        else _model_text(PRIMARY)
    )
    assertions = [
        f"(= x {_input_expression(case)})",
        f"(= b {_boundary_expression(case)})",
        "(Requires_T x)",
        "(Boundary_T x b)",
        "(Spec_T x b y1 s1)",
    ]
    if kind == "valid":
        assertions.extend(
            [
                (
                    f"(= (y_return_allocation y1) "
                    f"{case['destination_allocation']})"
                ),
                f"(= (y_return_address y1) {case['destination_address']})",
                (
                    f"(= (y_return_provenance y1) "
                    f"{case['destination_provenance']})"
                ),
                f"(= (y_return_borrow y1) {case['destination_borrow']})",
                f"(= (y_return_length y1) {case['source_length']})",
            ]
        )
    elif kind == "no_op_write":
        assertions.append(
            "(= (s_destination_storage s1) (x_destination_storage x))"
        )
    elif kind == "partial_write":
        assertions.append(
            "(= (select (s_destination_storage s1) 2) (Initialized 0))"
        )
    elif kind == "omitted_initialization":
        assertions.append(
            "(= (select (s_destination_storage s1) 1) Uninitialized)"
        )
    elif kind in {
        "duplicate_write",
        "out_of_order_write",
        "clone_count",
        "write_count",
    }:
        pass
    elif kind == "callback_state":
        assertions.append(
            f"(= (s_clone_state s1) {case['clone_after'][2] + 1})"
        )
    elif kind == "return_identity":
        assertions.append(
            f"(= (y_return_allocation y1) {case['source_allocation']})"
        )
    elif kind == "changed_source":
        assertions.append(
            "(= (select (s_source_values s1) 1) 999)"
        )
    elif kind == "changed_frame":
        assertions.append(
            f"(= (s_frame_token s1) {case['frame_token'] + 1})"
        )
    elif kind != "invalid_domain":
        raise ValueError(f"unknown target-119 probe kind: {kind}")
    body = "\n       ".join(assertions)
    return model + f"""\
(assert
  (and {body}))
(check-sat)
"""


def panic_probe_semantics(name: str) -> dict[str, Any]:
    case = PROBE_CASES[name]
    if not case["kind"].startswith("panic_lifecycle"):
        raise ValueError(f"{name} is not a panic lifecycle probe")
    panic = int(case["panic_index"])
    probe_case = _panic_case(panic)
    successful = list(range(panic))
    storage: list[int | None] = [None] * probe_case["destination_length"]
    for step in successful:
        storage[step] = probe_case["clone_result"][step]
    for step in successful:
        storage[step] = None
    clone_chain_valid = all(
        probe_case["clone_before"][step]
        == (
            probe_case["clone_initial_state"]
            if step == 0
            else probe_case["clone_after"][step - 1]
        )
        for step in [*successful, panic]
    )
    destruct_chain_valid = all(
        probe_case["destruct_before"][step]
        == (
            probe_case["destruct_initial_state"]
            if step == 0
            else probe_case["destruct_after"][step - 1]
        )
        for step in successful
    )
    valid = (
        clone_chain_valid
        and destruct_chain_valid
        and probe_case["completed"] == tuple(successful)
        and probe_case["destruct_completed"] == tuple(successful)
        and storage == [None] * probe_case["destination_length"]
    )
    return {
        "valid": valid,
        "panic_index": panic,
        "clone_call_indices": [*successful, panic],
        "write_indices": successful,
        "guard_initialized": panic,
        "cleanup_drop_indices": successful,
        "final_initialized_prefix": [],
        "untouched_suffix_indices": list(range(panic, 3)),
        "clone_call_count": panic + 1,
        "write_count": panic,
        "cleanup_drop_count": panic,
        "clone_state_chain_valid": clone_chain_valid,
        "destruct_state_chain_valid": destruct_chain_valid,
        "final_storage": [
            "Uninitialized" if value is None else f"Initialized({value})"
            for value in storage
        ],
        "fault": case.get("fault"),
    }


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": [
            {
                "fields": [
                    "b_destination_length",
                    "b_relation_initialized_length",
                    "b_relation_values_length",
                    "b_destination_storage",
                    "b_source_length",
                    "b_source_values",
                ],
                "kind": "initial source and destination storage only",
                "trust_site_ids": [
                    "TS-119-D002",
                    "TS-119-D003",
                    "TS-119-E001",
                    "TS-119-E003",
                ],
            },
            {
                "fields": [
                    "b_destination_allocation",
                    "b_destination_address",
                    "b_destination_provenance",
                    "b_destination_borrow",
                    "b_destination_allocation_base",
                    "b_destination_allocation_bytes",
                    "b_source_allocation",
                    "b_source_address",
                    "b_source_provenance",
                    "b_source_allocation_base",
                    "b_source_allocation_bytes",
                    "b_element_size",
                    "b_element_alignment",
                    "b_isize_max",
                    "b_address_space_limit",
                    "b_frame_token",
                ],
                "kind": "initial memory, provenance, layout, borrow, and frame",
                "trust_site_ids": [
                    "TS-119-D002",
                    "TS-119-D003",
                    "TS-119-E001",
                    "TS-119-E003",
                ],
            },
            {
                "fields": [
                    "b_clone_initial_state",
                    "b_clone_result",
                    "b_clone_state_before",
                    "b_clone_state_after",
                    "b_clone_outcome",
                ],
                "kind": (
                    "individual Clone results/outcomes/state transitions keyed "
                    "by source index; source derives order, count, and final state"
                ),
                "trust_site_ids": [
                    "TS-119-D003",
                    "TS-119-D004",
                    "TS-119-E001",
                    "TS-119-E002",
                ],
            },
            {
                "fields": [
                    "b_destruct_initial_state",
                    "b_destruct_state_before",
                    "b_destruct_state_after",
                    "b_destruct_outcome",
                ],
                "kind": (
                    "individual Destruct outcomes/state transitions keyed by "
                    "cleanup index; normal return derives no calls and panic "
                    "paths derive initialized-prefix cleanup order and count"
                ),
                "trust_site_ids": [
                    "TS-119-D003",
                    "TS-119-D004",
                    "TS-119-E001",
                    "TS-119-E002",
                ],
            },
        ],
        "admitted_retained_trust_site_ids": list(ADMITTED_TRUST_SITES),
        "excluded_retained_trust_site_ids": [],
        "context_only_trust_site_ids": list(CONTEXT_ONLY_TRUST_SITES),
        "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
        "retained_site_restriction": (
            "TS-119-D003/D004 and TS-119-E001/E002 contribute only one "
            "Clone/write observation at a time. No aggregate prefix or final "
            "storage postcondition is admitted."
        ),
        "lower_composition": {
            "target": "core::slice::assume_init_mut",
            "active_contract_sha256": (
                "8d0e90b87ee12383ef38b353ff71f43a4136f565d0ae0f63651ee295c06f649a"
            ),
            "trust_site_ids": ["TS-119-D002", "TS-119-E003"],
            "derived": (
                "same destination allocation/address/provenance/borrow/length "
                "and the values of source-derived initialized storage"
            ),
        },
        "excluded_from_boundary": [
            "returned mutable reference",
            "resulting destination storage",
            "aggregate final Clone or Destruct state",
            "clone/write/drop order or count",
            "answer encoding",
            "selected or complete target execution trace",
        ],
        "boundary_statement": (
            "The boundary fixes initial memory and individual Clone/Destruct "
            "observations. The source derives equal-length control flow, "
            "increasing callback/write order, exact counts, initialized storage, "
            "normal-path Guard forget behavior, and the target-026 returned "
            "mutable-slice cast. Panic probes invoke the same successful-prefix "
            "transition and derive initialized-prefix cleanup from Guard::drop."
        ),
    }
