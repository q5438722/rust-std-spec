#!/usr/bin/env python3
"""Source-backed constructor model for input order 106, splitn_mut."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::splitn_mut"
INPUT_ORDER = "106"
ARTIFACT_ID = "106_core_slice_splitn_mut"
ACTIVE_CONTRACT_SHA256 = (
    "8fb38da00d00aea693a93e948863b8ab7bf6d6d2e6e4662345ad50d9a923d3db"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ "
    "<[T]>::splitn_mut::<F> ]( slice: &'a mut [T], n: usize, pred: F, ) -> "
    "(iter: core::slice::SplitNMut<'a, T, F>) ensures "
    "slice_predicate_split_view::<core::slice::SplitNMut<'a, T, F>, F, T>( "
    "iter, old(slice)@, pred, false, false, n as int, ), ;"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

ACTIVE_CONJUNCT_SYMBOLS = (
    "ActiveWellFormedConjunct",
    "ActiveSourceConjunct",
    "ActiveRemainingConjunct",
    "ActiveYieldedEmptyConjunct",
    "ActiveRemainderEmptyConjunct",
    "ActiveReverseConjunct",
    "ActiveLimitConjunct",
    "ActiveLimitNonnegativeConjunct",
    "ActiveForwardCompositionConjunct",
    "ActivePredicateTotalityConjunct",
)
OUTPUT_FIELDS = (
    ("y_source_sequence", "Int"),
    ("y_source_start", "Int"),
    ("y_source_length", "Int"),
    ("y_remaining_sequence", "Int"),
    ("y_remaining_start", "Int"),
    ("y_remaining_length", "Int"),
    ("y_yielded_sequence", "Int"),
    ("y_yielded_start", "Int"),
    ("y_yielded_length", "Int"),
    ("y_remainder_sequence", "Int"),
    ("y_remainder_start", "Int"),
    ("y_remainder_length", "Int"),
    ("y_allocation", "Int"),
    ("y_borrow", "Int"),
    ("y_predicate_identity", "Int"),
    ("y_predicate_state", "Int"),
    ("y_finished", "Bool"),
    ("y_count", "Int"),
    ("y_reverse", "Bool"),
    ("y_inclusive", "Bool"),
    ("y_callback_calls", "Int"),
)
STATE_FIELDS = (
    ("s_final_slice_sequence", "Int"),
    ("s_final_slice_start", "Int"),
    ("s_final_slice_length", "Int"),
    ("s_final_allocation", "Int"),
    ("s_final_borrow", "Int"),
    ("s_callback_identity", "Int"),
    ("s_callback_state", "Int"),
    ("s_callback_calls", "Int"),
)
SOURCE_TRANSITIONS = (
    "SplitMutNewSourceSequence",
    "SplitMutNewSourceStart",
    "SplitMutNewSourceLength",
    "SplitMutNewAllocation",
    "SplitMutNewBorrow",
    "SplitMutNewPredicateIdentity",
    "SplitMutNewPredicateState",
    "SplitMutNewFinished",
    "SplitMutNewCallbackCalls",
    "SplitNMutNewCount",
    "SplitNMutNewReverse",
    "SplitNMutNewInclusive",
    "ConstructorFinalSliceSequence",
    "ConstructorFinalSliceStart",
    "ConstructorFinalSliceLength",
    "ConstructorFinalAllocation",
    "ConstructorFinalBorrow",
    "ConstructorFinalCallbackIdentity",
    "ConstructorFinalCallbackState",
    "ConstructorFinalCallbackCalls",
)
OUTPUT_SOURCE_TRANSITIONS = SOURCE_TRANSITIONS[:12]


def _state_declaration(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    return """\
(declare-datatypes ((State 0))
  (((mkState
      (s_final_slice_sequence Int)
      (s_final_slice_start Int)
      (s_final_slice_length Int)
      (s_final_allocation Int)
      (s_final_borrow Int)
      (s_callback_identity Int)
      (s_callback_state Int)
      (s_callback_calls Int)))))"""


def _final_state_arguments(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "       (ConstructorFinalStateExists x)"
    return """\
       (= (s_final_slice_sequence s) (ConstructorFinalSliceSequence x))
       (= (s_final_slice_start s) (ConstructorFinalSliceStart x))
       (= (s_final_slice_length s) (ConstructorFinalSliceLength x))
       (= (s_final_allocation s) (ConstructorFinalAllocation x))
       (= (s_final_borrow s) (ConstructorFinalBorrow x))
       (= (s_callback_identity s) (ConstructorFinalCallbackIdentity x))
       (= (s_callback_state s) (ConstructorFinalCallbackState x))
       (= (s_callback_calls s) (ConstructorFinalCallbackCalls x))"""


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


def obligation_text(purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-106 obligation purpose: {purpose}")
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Purpose: {purpose}
; The boundary contains input identities only; every returned field is derived.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_source_sequence Int)
      (x_source_start Int)
      (x_length Int)
      (x_allocation Int)
      (x_borrow Int)
      (x_predicate_identity Int)
      (x_predicate_state Int)
      (x_n Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_input_allocation Int)
      (b_input_borrow Int)
      (b_predicate_identity Int)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_source_sequence Int)
      (y_source_start Int)
      (y_source_length Int)
      (y_remaining_sequence Int)
      (y_remaining_start Int)
      (y_remaining_length Int)
      (y_yielded_sequence Int)
      (y_yielded_start Int)
      (y_yielded_length Int)
      (y_remainder_sequence Int)
      (y_remainder_start Int)
      (y_remainder_length Int)
      (y_allocation Int)
      (y_borrow Int)
      (y_predicate_identity Int)
      (y_predicate_state Int)
      (y_finished Bool)
      (y_count Int)
      (y_reverse Bool)
      (y_inclusive Bool)
      (y_callback_calls Int)))))
{_state_declaration(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun InputIdentityObserved ((x Input) (b Boundary)) Bool
  (and (= (b_input_allocation b) (x_allocation x))
       (= (b_input_borrow b) (x_borrow x))
       (= (b_predicate_identity b) (x_predicate_identity x))))
(define-fun SplitMutNewSourceSequence ((x Input)) Int
  (x_source_sequence x))
(define-fun SplitMutNewSourceStart ((x Input)) Int
  (x_source_start x))
(define-fun SplitMutNewSourceLength ((x Input)) Int
  (x_length x))
(define-fun SplitMutNewAllocation ((x Input)) Int
  (x_allocation x))
(define-fun SplitMutNewBorrow ((x Input)) Int
  (x_borrow x))
(define-fun SplitMutNewPredicateIdentity ((x Input)) Int
  (x_predicate_identity x))
(define-fun SplitMutNewPredicateState ((x Input)) Int
  (x_predicate_state x))
(define-fun SplitMutNewFinished ((x Input)) Bool
  false)
(define-fun SplitMutNewCallbackCalls ((x Input)) Int
  0)
(define-fun SplitNMutNewCount ((x Input)) Int
  (x_n x))
(define-fun SplitNMutNewReverse ((x Input)) Bool
  false)
(define-fun SplitNMutNewInclusive ((x Input)) Bool
  false)
(define-fun ConstructorFinalSliceSequence ((x Input)) Int
  (x_source_sequence x))
(define-fun ConstructorFinalSliceStart ((x Input)) Int
  (x_source_start x))
(define-fun ConstructorFinalSliceLength ((x Input)) Int
  (x_length x))
(define-fun ConstructorFinalAllocation ((x Input)) Int
  (x_allocation x))
(define-fun ConstructorFinalBorrow ((x Input)) Int
  (x_borrow x))
(define-fun ConstructorFinalCallbackIdentity ((x Input)) Int
  (x_predicate_identity x))
(define-fun ConstructorFinalCallbackState ((x Input)) Int
  (x_predicate_state x))
(define-fun ConstructorFinalCallbackCalls ((x Input)) Int
  0)
(define-fun ConstructorFinalStateExists ((x Input)) Bool
  (exists
    ((final_slice_sequence Int)
     (final_slice_start Int)
     (final_slice_length Int)
     (final_allocation Int)
     (final_borrow Int)
     (callback_identity Int)
     (callback_state Int)
     (callback_calls Int))
    (and (= final_slice_sequence (ConstructorFinalSliceSequence x))
         (= final_slice_start (ConstructorFinalSliceStart x))
         (= final_slice_length (ConstructorFinalSliceLength x))
         (= final_allocation (ConstructorFinalAllocation x))
         (= final_borrow (ConstructorFinalBorrow x))
         (= callback_identity (ConstructorFinalCallbackIdentity x))
         (= callback_state (ConstructorFinalCallbackState x))
         (= callback_calls (ConstructorFinalCallbackCalls x)))))
(define-fun ActiveWellFormedConjunct ((y Output)) Bool
  (and (>= (y_count y) 0)
       (>= (y_remainder_length y) 0)
       (<= (y_remainder_length y) (y_source_length y))))
(define-fun ActiveSourceConjunct ((x Input) (y Output)) Bool
  (and (= (y_source_sequence y) (x_source_sequence x))
       (= (y_source_start y) (x_source_start x))
       (= (y_source_length y) (x_length x))))
(define-fun ActiveRemainingConjunct ((y Output)) Bool
  (and (= (y_remaining_sequence y) (y_source_sequence y))
       (= (y_remaining_start y) (y_source_start y))
       (= (y_remaining_length y) (y_source_length y))))
(define-fun ActiveYieldedEmptyConjunct ((y Output)) Bool
  (and (= (y_yielded_sequence y) 0)
       (= (y_yielded_start y) 0)
       (= (y_yielded_length y) 0)))
(define-fun ActiveRemainderEmptyConjunct ((y Output)) Bool
  (and (= (y_remainder_sequence y) 0)
       (= (y_remainder_start y) 0)
       (= (y_remainder_length y) 0)))
(define-fun ActiveReverseConjunct ((y Output)) Bool
  (not (y_reverse y)))
(define-fun ActiveLimitConjunct ((x Input) (y Output)) Bool
  (= (y_count y) (x_n x)))
(define-fun ActiveLimitNonnegativeConjunct ((y Output)) Bool
  (>= (y_count y) 0))
(define-fun ActiveForwardCompositionConjunct ((y Output)) Bool
  (and (= (y_yielded_length y) 0)
       (= (y_remaining_sequence y) (y_source_sequence y))
       (= (y_remaining_start y) (y_source_start y))
       (= (y_remaining_length y) (y_source_length y))))
(define-fun ActivePredicateTotalityConjunct ((x Input)) Bool
  (forall ((i Int))
    (=>
      (and (>= i 0) (< i (x_length x)))
      (or (= i i) (not (= i i))))))
(define-fun Requires_T ((x Input)) Bool
  (and (>= (x_source_start x) 0)
       (>= (x_length x) 0)
       (>= (x_allocation x) 0)
       (>= (x_borrow x) 0)
       (>= (x_predicate_identity x) 0)
       (>= (x_n x) 0)))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (>= (b_input_allocation b) 0)
       (>= (b_input_borrow b) 0)
       (>= (b_predicate_identity b) 0)
       (InputIdentityObserved x b)))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (InputIdentityObserved x b)
       (= (y_source_sequence y) (SplitMutNewSourceSequence x))
       (= (y_source_start y) (SplitMutNewSourceStart x))
       (= (y_source_length y) (SplitMutNewSourceLength x))
       (= (y_remaining_sequence y) (SplitMutNewSourceSequence x))
       (= (y_remaining_start y) (SplitMutNewSourceStart x))
       (= (y_remaining_length y) (SplitMutNewSourceLength x))
       (= (y_yielded_sequence y) 0)
       (= (y_yielded_start y) 0)
       (= (y_yielded_length y) 0)
       (= (y_remainder_sequence y) 0)
       (= (y_remainder_start y) 0)
       (= (y_remainder_length y) 0)
       (= (y_allocation y) (SplitMutNewAllocation x))
       (= (y_borrow y) (SplitMutNewBorrow x))
       (= (y_predicate_identity y) (SplitMutNewPredicateIdentity x))
       (= (y_predicate_state y) (SplitMutNewPredicateState x))
       (= (y_finished y) (SplitMutNewFinished x))
       (= (y_count y) (SplitNMutNewCount x))
       (= (y_reverse y) (SplitNMutNewReverse x))
       (= (y_inclusive y) (SplitNMutNewInclusive x))
       (= (y_callback_calls y) (SplitMutNewCallbackCalls x))
{_final_state_arguments(purpose)}
       (ActiveWellFormedConjunct y)
       (ActiveSourceConjunct x y)
       (ActiveRemainingConjunct y)
       (ActiveYieldedEmptyConjunct y)
       (ActiveRemainderEmptyConjunct y)
       (ActiveReverseConjunct y)
       (ActiveLimitConjunct x y)
       (ActiveLimitNonnegativeConjunct y)
       (ActiveForwardCompositionConjunct y)
       (ActivePredicateTotalityConjunct x)))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
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


def _principal_observations(purpose: str) -> list[dict[str, str]]:
    observations = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort,
        }
        for selector, sort in OUTPUT_FIELDS
    ]
    if purpose == PRIMARY:
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
        raise ValueError(f"unknown target-106 obligation purpose: {purpose}")
    return {
        "schema_version": 2,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "domain": {
            "slice": "arbitrary source identity, nonnegative start, and length",
            "n": "arbitrary nonnegative integer representing usize",
            "predicate": "arbitrary identity and initial state",
            "reference_identity": (
                "structural allocation and parent mutable-borrow identity"
            ),
        },
        "contract_translation": {
            "active_conjuncts": list(ACTIVE_CONJUNCT_SYMBOLS),
            "predicate_totality": (
                "The generated forall P(i) or not P(i) clause is classical "
                "totality only. It is retained as ActivePredicateTotalityConjunct "
                "without introducing a constructor-time callback observation."
            ),
            "source_flow": [
                "split_mut(slice, pred)",
                "SplitMut::new stores the full mutable slice and predicate",
                "SplitMut::new sets finished=false and invokes no callback",
                "SplitNMut::new stores that SplitMut and count=n",
            ],
        },
        "boundary_scope": {
            "shared_observations": [
                "input allocation identity",
                "input mutable-borrow identity",
                "input predicate identity",
            ],
            "excluded_observations": [
                "returned SplitNMut or iterator view",
                "source, remaining, yielded, or remainder ranges",
                "predicate results or constructor-time callback transitions",
                "private finished/count/reverse state",
                "aggregate final state",
                "answer-equivalent encodings",
                "selected or complete execution traces",
            ],
            "narrower_than_target": True,
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
        "boundary_fields": [
            {
                "selector": "b_input_allocation",
                "role": "input_provenance",
                "source_citations": [
                    "core/src/slice/mod.rs:2442-2447",
                    "core/src/slice/iter.rs:678-690",
                ],
                "trust_site_ids": ["TS-106-D001", "TS-106-D002"],
            },
            {
                "selector": "b_input_borrow",
                "role": "input_provenance",
                "source_citations": [
                    "core/src/slice/mod.rs:2442-2447",
                    "core/src/slice/iter.rs:678-690",
                ],
                "trust_site_ids": ["TS-106-D001", "TS-106-D004"],
            },
            {
                "selector": "b_predicate_identity",
                "role": "callback_argument",
                "source_citations": [
                    "core/src/slice/mod.rs:2442-2447",
                    "core/src/slice/iter.rs:678-690",
                ],
                "trust_site_ids": ["TS-106-D003"],
            },
        ],
        "declared_functions": [],
        "source_transition_definitions": list(
            SOURCE_TRANSITIONS if purpose == PRIMARY else OUTPUT_SOURCE_TRANSITIONS
        ),
        "source_transition_bindings": {
            "split_mut": {
                "symbols": [
                    "SplitMutNewSourceSequence",
                    "SplitMutNewSourceStart",
                    "SplitMutNewSourceLength",
                    "SplitMutNewAllocation",
                    "SplitMutNewBorrow",
                    "SplitMutNewPredicateIdentity",
                    "SplitMutNewPredicateState",
                    "SplitMutNewFinished",
                    "SplitMutNewCallbackCalls",
                ],
                "trust_site_ids": [
                    "TS-106-D001",
                    "TS-106-D002",
                    "TS-106-D003",
                    "TS-106-C001",
                ],
                "source_citations": [
                    "core/src/slice/mod.rs:2445-2447",
                    "core/src/slice/iter.rs:678-690",
                ],
            },
            "split_n_mut_new": {
                "symbols": [
                    "SplitNMutNewCount",
                    "SplitNMutNewReverse",
                    "SplitNMutNewInclusive",
                ],
                "trust_site_ids": [
                    "TS-106-D001",
                    "TS-106-D004",
                    "TS-106-C002",
                ],
                "source_citations": [
                    "core/src/slice/iter.rs:1105-1108",
                    "core/src/slice/iter.rs:1241-1252",
                ],
            },
            "constructor_final_state": {
                "symbols": [
                    "ConstructorFinalSliceSequence",
                    "ConstructorFinalSliceStart",
                    "ConstructorFinalSliceLength",
                    "ConstructorFinalAllocation",
                    "ConstructorFinalBorrow",
                    "ConstructorFinalCallbackIdentity",
                    "ConstructorFinalCallbackState",
                    "ConstructorFinalCallbackCalls",
                ],
                "trust_site_ids": [
                    "TS-106-D002",
                    "TS-106-D003",
                    "TS-106-D004",
                ],
                "source_citations": [
                    "core/src/slice/mod.rs:2442-2447",
                    "core/src/slice/iter.rs:678-690,1241-1252",
                ],
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "principal return, private iterator state, reference identity, "
            "callback state, and final state"
            if purpose == PRIMARY
            else "principal return, private iterator state, and reference identity"
        ),
        "principal_observations": _principal_observations(purpose),
        "expected_solver_result": "unsat",
    }


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return obligation_text(purpose), obligation_metadata(purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError("target-106 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-106 metadata differs from the reviewed constructor translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-106 SMT differs from the reviewed constructor translation"
        )


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": [
            {
                "field": "b_input_allocation",
                "meaning": "identity of the allocation backing the input slice",
                "trust_site_ids": ["TS-106-D001", "TS-106-D002"],
            },
            {
                "field": "b_input_borrow",
                "meaning": "identity of the input mutable borrow",
                "trust_site_ids": ["TS-106-D001", "TS-106-D004"],
            },
            {
                "field": "b_predicate_identity",
                "meaning": "identity of the predicate value moved into SplitMut",
                "trust_site_ids": ["TS-106-D003"],
            },
        ],
        "deterministic_source_transitions": [
            {
                "operation": "split_mut -> SplitMut::new",
                "semantics": (
                    "stores the complete input slice reference and predicate, "
                    "sets finished=false, and performs zero predicate calls"
                ),
                "trust_site_ids": [
                    "TS-106-D001",
                    "TS-106-D002",
                    "TS-106-D003",
                    "TS-106-C001",
                ],
            },
            {
                "operation": "SplitNMut::new",
                "semantics": (
                    "stores the SplitMut unchanged in GenericSplitN and sets count=n"
                ),
                "trust_site_ids": [
                    "TS-106-D001",
                    "TS-106-D004",
                    "TS-106-C002",
                ],
            },
            {
                "operation": "slice_predicate_split_view",
                "semantics": (
                    "projects full source and remaining ranges, empty yielded "
                    "and remainder sequences, reverse=false, and limit=n"
                ),
                "trust_site_ids": ["TS-106-D001", "TS-106-D002", "TS-106-D004"],
            },
        ],
        "constructor_callback_invocations": 0,
        "executable_boundary_trust_site_ids": [
            "TS-106-D001",
            "TS-106-D002",
            "TS-106-D003",
            "TS-106-D004",
        ],
        "context_only_trust_sites": ["TS-106-C001", "TS-106-C002"],
        "all_audited_trust_site_ids": [
            "TS-106-D001",
            "TS-106-D002",
            "TS-106-D003",
            "TS-106-D004",
            "TS-106-C001",
            "TS-106-C002",
        ],
        "excluded_from_boundary": [
            "returned SplitNMut or iterator view",
            "selected source, remaining, yielded, or remainder ranges",
            "predicate results and callback state transitions",
            "finished, count, reverse, or inclusive state",
            "final slice or callback state",
            "answer-equivalent encodings",
            "selected or complete execution traces",
        ],
    }
