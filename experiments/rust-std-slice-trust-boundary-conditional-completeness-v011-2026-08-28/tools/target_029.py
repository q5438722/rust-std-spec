#!/usr/bin/env python3
"""Bounded contract translation for input order 29, binary_search_by."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::binary_search_by"
INPUT_ORDER = "29"
ARTIFACT_ID = "029_core_slice_binary_search_by"
ACTIVE_CONTRACT_SHA256 = (
    "bbea7d2146da8d9116c68e9603460103ed4f7322c785180266a17b23b06c0f6b"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<'a, T, F: core::ops::FnMut(&'a T) -> "
    "core::cmp::Ordering>[ <[T]>::binary_search_by::<F> ](slice: &'a [T], "
    "f: F) -> (result: core::result::Result<usize, usize>) ensures "
    "slice_binary_search_by_result(slice@, f, result);"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
SORTED_SANITY = "sorted-domain-sanity"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, SORTED_SANITY, EXACT_OUTPUT)

SOURCE_CITATIONS = [
    "core/src/slice/mod.rs:2926-2967",
    "core/src/slice/mod.rs:2970-3022",
]
POSITIVE_EQUIVALENCE_WITNESS = (
    "evidence/equivalence/binary_search_duplicate.positive.smt2"
)
NEGATIVE_EQUIVALENCE_WITNESS = (
    "evidence/equivalence/binary_search_duplicate.negative.smt2"
)


def _boundary_body(purpose: str) -> str:
    profile = {
        PRIMARY: """\
       (ComparatorObservation (b_cmp0 b))
       (ComparatorObservation (b_cmp1 b))""",
        SORTED_SANITY: """\
       (ComparatorObservation (b_cmp0 b))
       (ComparatorObservation (b_cmp1 b))
       (OrderedProfile x b)""",
        EXACT_OUTPUT: """\
       (= (b_cmp0 b) Equal)
       (= (b_cmp1 b) Equal)""",
    }[purpose]
    return f"""\
  (and (ElementReadsMatch x b)
{profile}
       (= (b_state_delta0 b) 0)
       (= (b_state_delta1 b) 0)))"""


def _equivalence_body(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return """\
  (and (= (y_is_ok y1) (y_is_ok y2))
       (= (y_index y1) (y_index y2))
       (= (s_callback_state s1) (s_callback_state s2))))"""
    return """\
  (and (= (s_callback_state s1) (s_callback_state s2))
       (= (y_is_ok y1) (y_is_ok y2))
       (ite (y_is_ok y1)
            (and (EqualAt x b (y_index y1))
                 (EqualAt x b (y_index y2)))
            (= (y_index y1) (y_index y2)))))"""


def obligation_text(purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-029 obligation purpose: {purpose}")
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Purpose: {purpose}
; Bounded domain: exactly two input elements. Requires_T adds no sortedness.
(set-logic ALL)
(declare-datatypes ((Ordering 0)) (((Less) (Equal) (Greater))))
(declare-datatypes ((Input 0))
  (((mkInput
      (x_length Int)
      (x_element0 Int)
      (x_element1 Int)
      (x_callback_initial_state Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_read0 Int)
      (b_read1 Int)
      (b_cmp0 Ordering)
      (b_cmp1 Ordering)
      (b_state_delta0 Int)
      (b_state_delta1 Int)))))
(declare-datatypes ((Output 0))
  (((mkOutput (y_is_ok Bool) (y_index Int)))))
(declare-datatypes ((State 0))
  (((mkState (s_callback_state Int)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun OrderingRank ((ordering Ordering)) Int
  (ite (= ordering Less) (- 1) (ite (= ordering Equal) 0 1)))
(define-fun ComparatorObservation ((ordering Ordering)) Bool
  (or (= ordering Less) (= ordering Equal) (= ordering Greater)))
(define-fun LengthTwo ((x Input)) Bool
  (= (x_length x) 2))
(define-fun ElementReadsMatch ((x Input) (b Boundary)) Bool
  (and (= (b_read0 b) (x_element0 x))
       (= (b_read1 b) (x_element1 x))))
(define-fun ObservedOrdering ((b Boundary) (index Int)) Ordering
  (ite (= index 0) (b_cmp0 b) (b_cmp1 b)))
(define-fun OrderedProfile ((x Input) (b Boundary)) Bool
  (and (LengthTwo x)
       (<= (OrderingRank (ObservedOrdering b 0))
           (OrderingRank (ObservedOrdering b 1)))))
(define-fun OutputInBounds ((x Input) (y Output)) Bool
  (and (>= (y_index y) 0)
       (ite (y_is_ok y)
            (< (y_index y) (x_length x))
            (<= (y_index y) (x_length x)))))
(define-fun EqualAt
  ((x Input) (b Boundary) (index Int)) Bool
  (and (>= index 0)
       (< index (x_length x))
       (= (ObservedOrdering b index) Equal)))
(define-fun InsertionPoint
  ((x Input) (b Boundary) (index Int)) Bool
  (and (>= index 0)
       (<= index (x_length x))
       (=> (> index 0) (= (ObservedOrdering b 0) Less))
       (=> (> index 1) (= (ObservedOrdering b 1) Less))
       (=> (<= index 0) (= (ObservedOrdering b 0) Greater))
       (=> (<= index 1) (= (ObservedOrdering b 1) Greater))))
(define-fun GeneratedBinarySearchByResult
  ((x Input) (b Boundary) (y Output)) Bool
  (and (OutputInBounds x y)
       (=>
         (OrderedProfile x b)
         (ite (y_is_ok y)
              (EqualAt x b (y_index y))
              (InsertionPoint x b (y_index y))))))
(define-fun CallbackStateAfterTwo
  ((x Input) (b Boundary)) Int
  (+ (x_callback_initial_state x)
     (b_state_delta0 b)
     (b_state_delta1 b)))
(define-fun Requires_T ((x Input)) Bool
  (LengthTwo x))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
{_boundary_body(purpose)}
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (ElementReadsMatch x b)
       (GeneratedBinarySearchByResult x b y)
       (= (s_callback_state s) (CallbackStateAfterTwo x b))))
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


def obligation_metadata(purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-029 obligation purpose: {purpose}")
    metadata: dict[str, Any] = {
        "schema_version": 2,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "bounded_domain": {
            "length": 2,
            "requires_adds_sortedness": False,
            "boundary_profile": {
                PRIMARY: "all three-valued comparator profiles",
                SORTED_SANITY: "all nondecreasing comparator profiles",
                EXACT_OUTPUT: "[Equal, Equal]",
            }[purpose],
            "callback_transition_profile": "state-preserving",
            "contract_translation": (
                "Output is always bounded; only an ordered comparator profile "
                "implies Equal-at-Ok or the exact Less/Greater insertion point."
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                "source element reads",
                "per-element comparator results",
                "callback state-transition deltas",
            ],
            "deterministic_source_semantics": [
                "select_unpredictable returns the condition-selected operand",
                "assert_unchecked contributes only its proved domain condition",
            ],
            "excluded_observations": [
                "selected index",
                "returned Result",
                "aggregate final state",
                "selected execution trace",
                "answer-equivalent encoding",
            ],
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
                "selector": "b_read0",
                "role": "input_memory",
                "source_citations": [
                    "core/src/slice/mod.rs:2995,3014",
                    "core/src/slice/mod.rs:639-647",
                ],
                "trust_site_ids": ["TS-029-D002", "TS-029-E001"],
            },
            {
                "selector": "b_read1",
                "role": "input_memory",
                "source_citations": [
                    "core/src/slice/mod.rs:2995,3014",
                    "core/src/slice/mod.rs:639-647",
                ],
                "trust_site_ids": ["TS-029-D002", "TS-029-E001"],
            },
            {
                "selector": "b_cmp0",
                "role": "callback_result",
                "source_citations": ["core/src/slice/mod.rs:2995,3014"],
                "trust_site_ids": ["TS-029-D003", "TS-029-E002"],
            },
            {
                "selector": "b_cmp1",
                "role": "callback_result",
                "source_citations": ["core/src/slice/mod.rs:2995,3014"],
                "trust_site_ids": ["TS-029-D003", "TS-029-E002"],
            },
            {
                "selector": "b_state_delta0",
                "role": "callback_state_transition",
                "source_citations": ["core/src/slice/mod.rs:2995,3014"],
                "trust_site_ids": ["TS-029-D003", "TS-029-E002"],
            },
            {
                "selector": "b_state_delta1",
                "role": "callback_state_transition",
                "source_citations": ["core/src/slice/mod.rs:2995,3014"],
                "trust_site_ids": ["TS-029-D003", "TS-029-E002"],
            },
        ],
        "declared_functions": [],
        "source_transition_definitions": ["CallbackStateAfterTwo"],
        "equivalence_kind": (
            "exact" if purpose == EXACT_OUTPUT else "matching-index-equivalence"
        ),
        "principal_observations": [
            {
                "selector": "y_is_ok",
                "left": "output1",
                "right": "output2",
                "sort": "Bool",
            },
            {
                "selector": "y_index",
                "left": "output1",
                "right": "output2",
                "sort": "Int",
            },
            {
                "selector": "s_callback_state",
                "left": "state1",
                "right": "state2",
                "sort": "Int",
            },
        ],
        "expected_solver_result": "unsat" if purpose == SORTED_SANITY else "sat",
    }
    if purpose != EXACT_OUTPUT:
        metadata["weak_equivalence_review"] = {
            "source_citations": SOURCE_CITATIONS,
            "positive_witness": POSITIVE_EQUIVALENCE_WITNESS,
            "negative_witness": NEGATIVE_EQUIVALENCE_WITNESS,
            "policy": (
                "Result tags and callback state are exact. Err indices are exact. "
                "Distinct Ok indices are equivalent only when both observations "
                "are Equal at their selected elements."
            ),
        }
    return metadata


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return obligation_text(purpose), obligation_metadata(purpose)


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "boundary_narrower_than_target": True,
        "all_audited_trust_site_ids": [
            "TS-029-D001",
            "TS-029-D002",
            "TS-029-D003",
            "TS-029-D004",
            "TS-029-D005",
            "TS-029-C001",
            "TS-029-E001",
            "TS-029-E002",
        ],
        "retained_implementation_proof_boundary": {
            "context_only_trust_site_ids": [
                "TS-029-D001",
                "TS-029-C001",
            ],
            "executable_lower_boundary_trust_site_ids": [
                "TS-029-D002",
                "TS-029-D003",
                "TS-029-D004",
                "TS-029-D005",
                "TS-029-E001",
                "TS-029-E002",
            ],
            "assumption": (
                "The retained Verus implementation proof trusts source-linked "
                "get_unchecked element resolution, arbitrary FnMut Ordering "
                "observations, the select_unpredictable/assert_unchecked hint "
                "semantics, and verified source-shaped loop-result support."
            ),
        },
        "conditional_obligation_boundary": {
            "used_boundary_trust_site_ids": [
                "TS-029-D002",
                "TS-029-D003",
                "TS-029-E001",
                "TS-029-E002",
            ],
            "source_transition_only_trust_site_ids": [
                "TS-029-D004",
                "TS-029-D005",
            ],
            "context_only_trust_site_ids": [
                "TS-029-D001",
                "TS-029-C001",
            ],
            "distinction": (
                "The new two-execution obligation does not import the retained "
                "implementation proof as a functionality oracle. Only source "
                "element reads and callback observations enter Boundary_T; hint "
                "and loop-result support remain outside b."
            ),
        },
        "shared_boundary_observations": [
            {
                "fields": ["b_read0", "b_read1"],
                "kind": "source element reads at the two get_unchecked sites",
                "trust_site_ids": ["TS-029-D002", "TS-029-E001"],
                "source_citations": [
                    "core/src/slice/mod.rs:2995,3014",
                    "core/src/slice/mod.rs:639-647",
                ],
            },
            {
                "fields": ["b_cmp0", "b_cmp1"],
                "kind": "per-element FnMut Ordering results",
                "trust_site_ids": ["TS-029-D003", "TS-029-E002"],
                "source_citations": ["core/src/slice/mod.rs:2995,3014"],
            },
            {
                "fields": ["b_state_delta0", "b_state_delta1"],
                "kind": "per-call callback state transitions",
                "trust_site_ids": ["TS-029-D003", "TS-029-E002"],
                "source_citations": ["core/src/slice/mod.rs:2995,3014"],
            },
        ],
        "deterministic_source_transitions": [
            {
                "operation": "hint::select_unpredictable",
                "semantics": (
                    "returns the condition-selected base or midpoint operand; "
                    "the choice is derived and is not a boundary field"
                ),
                "source_citations": ["core/src/slice/mod.rs:3000"],
                "trust_site_ids": ["TS-029-D004"],
            },
            {
                "operation": "hint::assert_unchecked",
                "semantics": (
                    "contributes only the source-proved Ok or Err index bound "
                    "and supplies no result observation"
                ),
                "source_citations": [
                    "core/src/slice/mod.rs:3017,3022",
                ],
                "trust_site_ids": ["TS-029-D004"],
            },
            {
                "operation": "length-two callback state composition",
                "semantics": (
                    "threads the initial callback state through the two source "
                    "invocations by adding the two shared transition deltas"
                ),
                "source_citations": [
                    "core/src/slice/mod.rs:2980-3022",
                ],
                "trust_site_ids": ["TS-029-D003", "TS-029-D005"],
            },
        ],
        "excluded_retained_trust_site_ids": [],
        "source_backed_replacements": [],
        "excluded_from_boundary": [
            "selected index or insertion point",
            "returned Result tag or payload",
            "aggregate callback final state",
            "select_unpredictable branch choice",
            "loop base, size, midpoint, or complete execution trace",
            "active-contract truth or an answer-equivalent encoding",
        ],
        "proof_scope": {
            "domain": "exactly two input elements",
            "requires_adds_sortedness": False,
            "target_relation": (
                "literal active generated contract plus source-backed callback "
                "state composition"
            ),
            "limitation": (
                "This is a bounded active-contract conditional-completeness "
                "obligation, not a recursive verification of the public target "
                "implementation for arbitrary lengths."
            ),
        },
    }


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError("target-029 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-029 metadata differs from the reviewed bounded translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-029 SMT differs from the reviewed bounded contract translation"
        )


def witness_payload() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "general_counterexample": {
            "input": {
                "length": 2,
                "elements": [10, 20],
                "callback_initial_state": 7,
            },
            "boundary": {
                "element_reads": [10, 20],
                "comparator_results": ["Greater", "Less"],
                "callback_state_deltas": [0, 0],
            },
            "execution1": {
                "result": {"tag": "Ok", "index": 0},
                "callback_final_state": 7,
            },
            "execution2": {
                "result": {"tag": "Err", "index": 0},
                "callback_final_state": 7,
            },
            "expected": {
                "ordered": False,
                "execution1_satisfies_contract": True,
                "execution2_satisfies_contract": True,
                "equivalent": False,
            },
        },
        "exact_output_counterexample": {
            "input": {
                "length": 2,
                "elements": [10, 10],
                "callback_initial_state": 7,
            },
            "boundary": {
                "element_reads": [10, 10],
                "comparator_results": ["Equal", "Equal"],
                "callback_state_deltas": [0, 0],
            },
            "execution1": {
                "result": {"tag": "Ok", "index": 0},
                "callback_final_state": 7,
            },
            "execution2": {
                "result": {"tag": "Ok", "index": 1},
                "callback_final_state": 7,
            },
            "expected": {
                "ordered": True,
                "execution1_satisfies_contract": True,
                "execution2_satisfies_contract": True,
                "matching_index_equivalent": True,
                "exactly_equal": False,
            },
        },
    }


def fixed_model_text(purpose: str) -> str:
    if purpose not in {PRIMARY, EXACT_OUTPUT}:
        raise ValueError("fixed models exist only for SAT obligations")
    text = obligation_text(purpose)
    terminal = "(check-sat)\n"
    if not text.endswith(terminal):
        raise ValueError("target obligation lacks the expected terminal check-sat")
    if purpose == PRIMARY:
        boundary = "(mkBoundary 10 20 Greater Less 0 0)"
        output1 = "(mkOutput true 0)"
        output2 = "(mkOutput false 0)"
    else:
        boundary = "(mkBoundary 10 10 Equal Equal 0 0)"
        output1 = "(mkOutput true 0)"
        output2 = "(mkOutput true 1)"
    input_value = (
        "(mkInput 2 10 20 7)"
        if purpose == PRIMARY
        else "(mkInput 2 10 10 7)"
    )
    return (
        text[: -len(terminal)]
        + f"""\
(assert (= x {input_value}))
(assert (= b {boundary}))
(assert (= y1 {output1}))
(assert (= s1 (mkState 7)))
(assert (= y2 {output2}))
(assert (= s2 (mkState 7)))
(check-sat)
(get-value (
  (x_length x)
  (b_cmp0 b)
  (b_cmp1 b)
  (y_is_ok y1)
  (y_index y1)
  (s_callback_state s1)
  (y_is_ok y2)
  (y_index y2)
  (s_callback_state s2)))
"""
    )
