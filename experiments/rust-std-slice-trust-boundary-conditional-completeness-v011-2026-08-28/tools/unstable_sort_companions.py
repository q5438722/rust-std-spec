#!/usr/bin/env python3
"""Shared generators for the Ord-backed unstable-sort companion targets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
BOUNDED_SANITY = "bounded-length-three-sanity"
EXACT_FINAL_SLICE = "exact-final-slice-determinism"
PURPOSES = (PRIMARY, BOUNDED_SANITY, EXACT_FINAL_SLICE)

POSITIVE_EQUIVALENCE_WITNESS = (
    "evidence/equivalence/unstable_sort_equal_keys.positive.smt2"
)
NEGATIVE_EQUIVALENCE_WITNESS = (
    "evidence/equivalence/unstable_sort_equal_keys.negative.smt2"
)


@dataclass(frozen=True)
class TargetConfig:
    target: str
    input_order: str
    artifact_id: str
    active_contract_sha256: str
    active_contract_text: str
    mode: str
    target_source_citation: str
    public_docs_citation: str
    admitted_trust_site_id: str
    excluded_retained_trust_site_ids: tuple[str, ...]
    all_audited_trust_site_ids: tuple[str, ...]
    proof_filename: str
    verus_expected_summary: str


ORD_LAW_CITATIONS = (
    "core/src/cmp.rs:733-761",
    "specs/slice_shared_vocabulary.rs:330-379",
)


def _check_config(config: TargetConfig) -> None:
    if config.mode not in {"ord", "key"}:
        raise ValueError(f"{config.target}: unknown unstable-sort mode")
    if "core::cmp::Ord" not in config.active_contract_text:
        raise ValueError(f"{config.target}: active contract lacks its Ord bound")


def _boundary_declaration(config: TargetConfig, *, bounded: bool) -> str:
    del bounded
    if config.mode == "ord":
        fields = [
            "(b_ord_class_of_identity (Array Int Int))",
            "(b_callback_state_delta Int)",
        ]
    else:
        fields = [
            "(b_key_of_identity (Array Int Int))",
            "(b_ord_class_of_key (Array Int Int))",
            "(b_callback_state_delta Int)",
        ]
    return "\n      ".join(fields)


def _observed_class_definition(config: TargetConfig) -> str:
    if config.mode == "ord":
        body = "(select (b_ord_class_of_identity b) identity)"
    else:
        body = """\
  (select (b_ord_class_of_key b)
          (select (b_key_of_identity b) identity))"""
    return f"""\
(define-fun ObservedClass ((b Boundary) (identity Int)) Int
  {body})"""


def _general_obligation_text(config: TargetConfig) -> str:
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {PRIMARY}
; General domain: arbitrary nonnegative slice length, arbitrary identity
; multiplicities, and an arbitrary valid observation position when nonempty.
; The input count summaries are the order-statistic consequences of exact
; permutation plus Ord/key sortedness; they are input facts, not boundary data.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_len Int)
      (x_position Int)
      (x_identity_multiplicity (Array Int Int))
      (x_count_strictly_before_class (Array Int Int))
      (x_count_at_or_before_class (Array Int Int))
      (x_callback_initial_state Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      {_boundary_declaration(config, bounded=False)}))))
(declare-datatypes ((Output 0))
  (((mkOutput (y_return_unit Bool)))))
(declare-datatypes ((State 0))
  (((mkState
      (s_identity_at_position Int)
      (s_identity_multiplicity (Array Int Int))
      (s_callback_state Int)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
{_observed_class_definition(config)}
(define-fun UnitReturnAfterSort ((x Input)) Bool
  (= (x_len x) (x_len x)))
(define-fun CallbackStateAfterSort ((x Input) (b Boundary)) Int
  (+ (x_callback_initial_state x) (b_callback_state_delta b)))
(define-fun IdentityMultisetAfterSort
  ((x Input)) (Array Int Int)
  (x_identity_multiplicity x))
(define-fun Requires_T ((x Input)) Bool
  (and
    (>= (x_len x) 0)
    (=>
      (> (x_len x) 0)
      (and
        (<= 0 (x_position x))
        (< (x_position x) (x_len x))))
    (forall ((identity Int))
      (and
        (>= (select (x_identity_multiplicity x) identity) 0)
        (<= (select (x_identity_multiplicity x) identity) (x_len x))))
    (forall ((class Int))
      (=>
        (and (<= 0 class) (< class (x_len x)))
        (and
          (<= 0 (select (x_count_strictly_before_class x) class))
          (<= (select (x_count_strictly_before_class x) class)
              (select (x_count_at_or_before_class x) class))
          (<= (select (x_count_at_or_before_class x) class)
              (x_len x)))))
    (forall ((left_class Int) (right_class Int))
      (=>
        (and
          (<= 0 left_class)
          (< left_class right_class)
          (< right_class (x_len x)))
        (<= (select (x_count_at_or_before_class x) left_class)
            (select (x_count_strictly_before_class x) right_class))))))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and
    (>= (b_callback_state_delta b) 0)
    (forall ((identity Int))
      (=>
        (> (select (x_identity_multiplicity x) identity) 0)
        (let ((class (ObservedClass b identity)))
          (and
            (<= 0 class)
            (< class (x_len x))
            (< (select (x_count_strictly_before_class x) class)
               (select (x_count_at_or_before_class x) class))))))))
(define-fun GeneratedPermutation ((x Input) (s State)) Bool
  (and
    (= (s_identity_multiplicity s) (IdentityMultisetAfterSort x))
    (=>
      (> (x_len x) 0)
      (> (select (s_identity_multiplicity s)
                 (s_identity_at_position s))
         0))))
(define-fun GeneratedSortednessAtPosition
  ((x Input) (b Boundary) (s State)) Bool
  (let ((class (ObservedClass b (s_identity_at_position s))))
    (=>
      (> (x_len x) 0)
      (and
        (<= (select (x_count_strictly_before_class x) class)
            (x_position x))
        (< (x_position x)
           (select (x_count_at_or_before_class x) class))))))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (GeneratedPermutation x s)
    (GeneratedSortednessAtPosition x b s)
    (= (y_return_unit y) (UnitReturnAfterSort x))
    (= (s_callback_state s) (CallbackStateAfterSort x b))))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and
    (= (y_return_unit y1) (y_return_unit y2))
    (= (s_identity_multiplicity s1) (s_identity_multiplicity s2))
    (= (s_callback_state s1) (s_callback_state s2))
    (or
      (= (x_len x) 0)
      (= (ObservedClass b (s_identity_at_position s1))
         (ObservedClass b (s_identity_at_position s2))))))
(assert
  (not
    (=>
      (and
        (Requires_T x)
        (Boundary_T x b)
        (Spec_T x b y1 s1)
        (Spec_T x b y2 s2))
      (Equivalent_T x b y1 s1 y2 s2))))
(check-sat)
"""


def _multiplicity(sequence: str, identity: str) -> str:
    return (
        f"(+ (ite (= (s_final0 {sequence}) {identity}) 1 0)"
        f" (ite (= (s_final1 {sequence}) {identity}) 1 0)"
        f" (ite (= (s_final2 {sequence}) {identity}) 1 0))"
    )


def _bounded_equivalence_body(purpose: str) -> str:
    if purpose == EXACT_FINAL_SLICE:
        return """\
  (and
    (= (y_return_unit y1) (y_return_unit y2))
    (= (s_final0 s1) (s_final0 s2))
    (= (s_final1 s1) (s_final1 s2))
    (= (s_final2 s1) (s_final2 s2))
    (= (s_callback_state s1) (s_callback_state s2))))"""
    return """\
  (and
    (= (y_return_unit y1) (y_return_unit y2))
    (= (s_callback_state s1) (s_callback_state s2))
    (SameElementMultiset s1 s2)
    (= (ObservedClass b (s_final0 s1))
       (ObservedClass b (s_final0 s2)))
    (= (ObservedClass b (s_final1 s1))
       (ObservedClass b (s_final1 s2)))
    (= (ObservedClass b (s_final2 s1))
       (ObservedClass b (s_final2 s2)))))"""


def _bounded_obligation_text(config: TargetConfig, purpose: str) -> str:
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; Bounded domain: exactly three distinct element identities. This obligation
; supplies an exact-output witness or sanity evidence, never the general
; conditional-completeness classification.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_id0 Int)
      (x_id1 Int)
      (x_id2 Int)
      (x_callback_initial_state Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      {_boundary_declaration(config, bounded=True)}))))
(declare-datatypes ((Output 0))
  (((mkOutput (y_return_unit Bool)))))
(declare-datatypes ((State 0))
  (((mkState
      (s_final0 Int)
      (s_final1 Int)
      (s_final2 Int)
      (s_callback_state Int)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
{_observed_class_definition(config)}
(define-fun DistinctInput ((x Input)) Bool
  (distinct (x_id0 x) (x_id1 x) (x_id2 x)))
(define-fun UnitReturnAfterSort ((x Input)) Bool
  (= (x_id0 x) (x_id0 x)))
(define-fun CallbackStateAfterSort ((x Input) (b Boundary)) Int
  (+ (x_callback_initial_state x) (b_callback_state_delta b)))
(define-fun InputMultiplicity ((x Input) (identity Int)) Int
  (+ (ite (= (x_id0 x) identity) 1 0)
     (ite (= (x_id1 x) identity) 1 0)
     (ite (= (x_id2 x) identity) 1 0)))
(define-fun FinalMultiplicity ((s State) (identity Int)) Int
  {_multiplicity("s", "identity")})
(define-fun ExactMultiplicities ((x Input) (s State)) Bool
  (and
    (= (InputMultiplicity x (x_id0 x))
       (FinalMultiplicity s (x_id0 x)))
    (= (InputMultiplicity x (x_id1 x))
       (FinalMultiplicity s (x_id1 x)))
    (= (InputMultiplicity x (x_id2 x))
       (FinalMultiplicity s (x_id2 x)))
    (= (InputMultiplicity x (s_final0 s))
       (FinalMultiplicity s (s_final0 s)))
    (= (InputMultiplicity x (s_final1 s))
       (FinalMultiplicity s (s_final1 s)))
    (= (InputMultiplicity x (s_final2 s))
       (FinalMultiplicity s (s_final2 s)))))
(define-fun OneOfSixPermutations ((x Input) (s State)) Bool
  (or
    (and (= (s_final0 s) (x_id0 x))
         (= (s_final1 s) (x_id1 x))
         (= (s_final2 s) (x_id2 x)))
    (and (= (s_final0 s) (x_id0 x))
         (= (s_final1 s) (x_id2 x))
         (= (s_final2 s) (x_id1 x)))
    (and (= (s_final0 s) (x_id1 x))
         (= (s_final1 s) (x_id0 x))
         (= (s_final2 s) (x_id2 x)))
    (and (= (s_final0 s) (x_id1 x))
         (= (s_final1 s) (x_id2 x))
         (= (s_final2 s) (x_id0 x)))
    (and (= (s_final0 s) (x_id2 x))
         (= (s_final1 s) (x_id0 x))
         (= (s_final2 s) (x_id1 x)))
    (and (= (s_final0 s) (x_id2 x))
         (= (s_final1 s) (x_id1 x))
         (= (s_final2 s) (x_id0 x)))))
(define-fun GeneratedPermutation ((x Input) (s State)) Bool
  (and (ExactMultiplicities x s) (OneOfSixPermutations x s)))
(define-fun GeneratedSortedness
  ((b Boundary) (s State)) Bool
  (and
    (<= (ObservedClass b (s_final0 s))
        (ObservedClass b (s_final0 s)))
    (<= (ObservedClass b (s_final0 s))
        (ObservedClass b (s_final1 s)))
    (<= (ObservedClass b (s_final0 s))
        (ObservedClass b (s_final2 s)))
    (<= (ObservedClass b (s_final1 s))
        (ObservedClass b (s_final1 s)))
    (<= (ObservedClass b (s_final1 s))
        (ObservedClass b (s_final2 s)))
    (<= (ObservedClass b (s_final2 s))
        (ObservedClass b (s_final2 s)))))
(define-fun SameElementMultiset ((left State) (right State)) Bool
  (and
    (= {_multiplicity("left", "(s_final0 left)")}
       {_multiplicity("right", "(s_final0 left)")})
    (= {_multiplicity("left", "(s_final1 left)")}
       {_multiplicity("right", "(s_final1 left)")})
    (= {_multiplicity("left", "(s_final2 left)")}
       {_multiplicity("right", "(s_final2 left)")})
    (= {_multiplicity("left", "(s_final0 right)")}
       {_multiplicity("right", "(s_final0 right)")})
    (= {_multiplicity("left", "(s_final1 right)")}
       {_multiplicity("right", "(s_final1 right)")})
    (= {_multiplicity("left", "(s_final2 right)")}
       {_multiplicity("right", "(s_final2 right)")})))
(define-fun Requires_T ((x Input)) Bool
  (DistinctInput x))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and
    (>= (b_callback_state_delta b) 0)
    (<= 0 (ObservedClass b (x_id0 x)))
    (< (ObservedClass b (x_id0 x)) 3)
    (<= 0 (ObservedClass b (x_id1 x)))
    (< (ObservedClass b (x_id1 x)) 3)
    (<= 0 (ObservedClass b (x_id2 x)))
    (< (ObservedClass b (x_id2 x)) 3)))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (GeneratedPermutation x s)
    (GeneratedSortedness b s)
    (= (y_return_unit y) (UnitReturnAfterSort x))
    (= (s_callback_state s) (CallbackStateAfterSort x b))))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_bounded_equivalence_body(purpose)}
(assert
  (not
    (=>
      (and
        (Requires_T x)
        (Boundary_T x b)
        (Spec_T x b y1 s1)
        (Spec_T x b y2 s2))
      (Equivalent_T x b y1 s1 y2 s2))))
(check-sat)
"""


def obligation_text(config: TargetConfig, purpose: str) -> str:
    _check_config(config)
    if purpose == PRIMARY:
        return _general_obligation_text(config)
    if purpose in {BOUNDED_SANITY, EXACT_FINAL_SLICE}:
        return _bounded_obligation_text(config, purpose)
    raise ValueError(f"{config.target}: unknown obligation purpose {purpose}")


def _boundary_fields(config: TargetConfig) -> list[dict[str, Any]]:
    if config.mode == "ord":
        result = [
            {
                "selector": "b_ord_class_of_identity",
                "role": "callback_result",
                "source_citations": [
                    config.target_source_citation,
                    *ORD_LAW_CITATIONS,
                ],
                "trust_site_ids": [config.admitted_trust_site_id],
            }
        ]
    else:
        result = [
            {
                "selector": "b_key_of_identity",
                "role": "callback_result",
                "source_citations": [config.target_source_citation],
                "trust_site_ids": [config.admitted_trust_site_id],
            },
            {
                "selector": "b_ord_class_of_key",
                "role": "callback_result",
                "source_citations": [
                    config.target_source_citation,
                    *ORD_LAW_CITATIONS,
                ],
                "trust_site_ids": [config.admitted_trust_site_id],
            },
        ]
    result.append(
        {
            "selector": "b_callback_state_delta",
            "role": "callback_state_transition",
            "source_citations": [config.target_source_citation],
            "trust_site_ids": [config.admitted_trust_site_id],
        }
    )
    return result


def obligation_metadata(config: TargetConfig, purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown obligation purpose {purpose}")
    general = purpose == PRIMARY
    exact = purpose == EXACT_FINAL_SLICE
    state_fields = (
        [
            ("s_identity_at_position", "Int"),
            ("s_identity_multiplicity", "Array Int Int"),
            ("s_callback_state", "Int"),
        ]
        if general
        else [
            ("s_final0", "Int"),
            ("s_final1", "Int"),
            ("s_final2", "Int"),
            ("s_callback_state", "Int"),
        ]
    )
    metadata: dict[str, Any] = {
        "schema_version": 2,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "domain": (
            {
                "slice_length": "arbitrary nonnegative integer",
                "identity_domain": "unbounded integer identities",
                "position": "arbitrary valid index when nonempty",
                "bounded": False,
                "abstraction": (
                    "order-statistic consequence of exact permutation and "
                    "Ord/key sortedness"
                ),
            }
            if general
            else {
                "slice_length": 3,
                "distinct_element_identities": True,
                "bounded": True,
                "classification_use": (
                    "exact SAT witness"
                    if exact
                    else "sanity evidence only"
                ),
            }
        ),
        "contract_translation": {
            "active_conjuncts": [
                "GeneratedPermutation",
                (
                    "GeneratedSortednessAtPosition"
                    if general
                    else "GeneratedSortedness"
                ),
            ],
            "permutation": (
                "exact identity multiplicity array"
                if general
                else "exact multiplicities plus all six permutations"
            ),
            "sortedness": (
                "arbitrary-position order-statistic interval"
                if general
                else "all six i <= j Ord-class comparisons"
            ),
        },
        "ord_totality_basis": {
            "type_bound": (
                "T: core::cmp::Ord"
                if config.mode == "ord"
                else "K: core::cmp::Ord"
            ),
            "source_citations": list(ORD_LAW_CITATIONS),
            "not_inherited_from_target_081": True,
        },
        "boundary_scope": {
            "shared_observations": (
                [
                    "finite extensional Ord comparison classes",
                    "callback observation-count state transition",
                ]
                if config.mode == "ord"
                else [
                    "finite extensional key extraction results",
                    "finite extensional Ord classes for extracted keys",
                    "callback observation-count state transition",
                ]
            ),
            "admitted_trust_site_ids": [config.admitted_trust_site_id],
            "excluded_retained_trust_site_ids": list(
                config.excluded_retained_trust_site_ids
            ),
            "excluded_observations": [
                "returned unit value",
                "final sequence or permutation",
                "selected ordering",
                "aggregate final state",
                "answer-equivalent encoding",
                "pivot or swap decisions",
                "comparison or key-extraction call trace",
                "complete target execution trace",
            ],
        },
        "active_contract_conjuncts": [
            "GeneratedPermutation",
            (
                "GeneratedSortednessAtPosition"
                if general
                else "GeneratedSortedness"
            ),
        ],
        "target_definition": "TargetDefinition_T",
        "theorem_variables": {
            "input": "x",
            "boundary": "b",
            "output1": "y1",
            "state1": "s1",
            "output2": "y2",
            "state2": "s2",
        },
        "boundary_fields": _boundary_fields(config),
        "declared_functions": [],
        "source_transition_definitions": (
            [
                "UnitReturnAfterSort",
                "CallbackStateAfterSort",
            ]
            if general
            else ["UnitReturnAfterSort", "CallbackStateAfterSort"]
        ),
        "equivalence_kind": (
            "exact" if exact else "equal-key-reordering-equivalence"
        ),
        "principal_observations": [
            {
                "selector": "y_return_unit",
                "left": "output1",
                "right": "output2",
                "sort": "Bool",
            },
            *[
                {
                    "selector": selector,
                    "left": "state1",
                    "right": "state2",
                    "sort": sort,
                }
                for selector, sort in state_fields
            ],
        ],
        "expected_solver_result": (
            "sat" if purpose == EXACT_FINAL_SLICE else "unsat"
        ),
    }
    if not exact:
        metadata["weak_equivalence_review"] = {
            "source_citations": [
                config.public_docs_citation,
                config.target_source_citation,
                *ORD_LAW_CITATIONS,
            ],
            "positive_witness": POSITIVE_EQUIVALENCE_WITNESS,
            "negative_witness": NEGATIVE_EQUIVALENCE_WITNESS,
            "target_specific_witness": (
                f"evidence/targets/{config.artifact_id}/witness.json"
            ),
            "policy": (
                "Unit return, exact identity multiplicities, callback state, "
                "and the class at every position remain exact. Only identities "
                "whose observed Ord/key classes are equal may reorder."
            ),
        }
    return metadata


def obligation(
    config: TargetConfig, purpose: str
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: TargetConfig,
    text: str,
    metadata: dict[str, Any],
) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.target}: unknown obligation purpose")
    expected_text, expected_metadata = obligation(config, str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            f"{config.target}: metadata differs from the reviewed translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.target}: SMT differs from the reviewed translation"
        )


def _const_array(default: int, updates: list[tuple[int, int]]) -> str:
    result = f"((as const (Array Int Int)) {default})"
    for index, value in updates:
        result = f"(store {result} {index} {value})"
    return result


def _fixed_boundary(config: TargetConfig) -> str:
    if config.mode == "ord":
        ranks = _const_array(0, [(10, 0), (11, 0), (20, 1)])
        return f"(mkBoundary {ranks} 0)"
    keys = _const_array(0, [(10, 100), (11, 100), (20, 200)])
    ranks = _const_array(0, [(100, 0), (200, 1)])
    return f"(mkBoundary {keys} {ranks} 0)"


def _bounded_prefix(config: TargetConfig, purpose: str) -> str:
    text = _bounded_obligation_text(config, purpose)
    marker = "(assert\n  (not\n    (=>"
    index = text.index(marker)
    return text[:index]


def fixed_exact_model_text(config: TargetConfig) -> str:
    return (
        _bounded_prefix(config, EXACT_FINAL_SLICE)
        + f"""\
(assert (= x (mkInput 10 11 20 7)))
(assert (= b {_fixed_boundary(config)}))
(assert (= y1 (mkOutput true)))
(assert (= s1 (mkState 10 11 20 7)))
(assert (= y2 (mkOutput true)))
(assert (= s2 (mkState 11 10 20 7)))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
(assert (not (Equivalent_T x b y1 s1 y2 s2)))
(check-sat)
(get-value (
  (s_final0 s1)
  (s_final1 s1)
  (s_final2 s1)
  (s_callback_state s1)
  (s_final0 s2)
  (s_final1 s2)
  (s_final2 s2)
  (s_callback_state s2)
  (ObservedClass b (s_final0 s1))
  (ObservedClass b (s_final0 s2))))
"""
    )


def equivalence_probe_text(config: TargetConfig, *, positive: bool) -> str:
    right = "11 10 20" if positive else "20 11 10"
    assertion = (
        "(assert (Equivalent_T x b y1 s1 y2 s2))"
        if positive
        else """\
(assert (SameElementMultiset s1 s2))
(assert (not (Equivalent_T x b y1 s1 y2 s2)))"""
    )
    spec_assertions = (
        """\
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
"""
        if positive
        else ""
    )
    return (
        _bounded_prefix(config, BOUNDED_SANITY)
        + f"""\
(assert (= x (mkInput 10 11 20 7)))
(assert (= b {_fixed_boundary(config)}))
(assert (= y1 (mkOutput true)))
(assert (= s1 (mkState 10 11 20 7)))
(assert (= y2 (mkOutput true)))
(assert (= s2 (mkState {right} 7)))
(assert (Requires_T x))
(assert (Boundary_T x b))
{spec_assertions}{assertion}
(check-sat)
"""
    )


def boundary_manifest(config: TargetConfig) -> dict[str, Any]:
    observations = (
        [
            {
                "fields": ["b_ord_class_of_identity"],
                "kind": "finite extensional Ord comparison classes",
                "trust_site_ids": [config.admitted_trust_site_id],
            }
        ]
        if config.mode == "ord"
        else [
            {
                "fields": ["b_key_of_identity"],
                "kind": "finite extensional key extraction results",
                "trust_site_ids": [config.admitted_trust_site_id],
            },
            {
                "fields": ["b_ord_class_of_key"],
                "kind": "finite extensional Ord classes for extracted keys",
                "trust_site_ids": [config.admitted_trust_site_id],
            },
        ]
    )
    observations.append(
        {
            "fields": ["b_callback_state_delta"],
            "kind": "callback observation-count state transition",
            "trust_site_ids": [config.admitted_trust_site_id],
        }
    )
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": observations,
        "admitted_trust_site_ids": [config.admitted_trust_site_id],
        "excluded_retained_sites": [
            {
                "trust_site_id": trust_site,
                "reason": (
                    "The retained site supplies an answer-bearing closure/private-"
                    "sort result and is excluded rather than relabeled."
                ),
            }
            for trust_site in config.excluded_retained_trust_site_ids
        ],
        "context_only_sites": [
            trust_site
            for trust_site in config.all_audited_trust_site_ids
            if trust_site
            not in {
                config.admitted_trust_site_id,
                *config.excluded_retained_trust_site_ids,
            }
        ],
        "all_audited_trust_site_ids": list(
            config.all_audited_trust_site_ids
        ),
        "excluded_observations": [
            "returned unit value",
            "final sequence or permutation",
            "selected ordering",
            "aggregate final state",
            "answer encoding",
            "pivot or swap decisions",
            "comparison or key-extraction call sequence",
            "complete execution trace",
        ],
        "assumption": (
            "Both executions share the same extensional comparison/key "
            "observations and callback state transition. The active permutation "
            "and sortedness conjuncts derive final order statistics; no final "
            "permutation or target trace is placed in b."
        ),
        "general_proof_scope": (
            "The completeness obligation quantifies arbitrary nonnegative "
            "length and identity multiplicities, plus a valid observation "
            "position whenever nonempty. Its "
            "order-statistic summaries are derived input facts and are not "
            "boundary observations."
        ),
    }


def _boundary_payload(config: TargetConfig) -> dict[str, Any]:
    if config.mode == "ord":
        payload: dict[str, Any] = {
            "ord_class_by_identity": {"10": 0, "11": 0, "20": 1}
        }
    else:
        payload = {
            "key_by_identity": {"10": 100, "11": 100, "20": 200},
            "ord_class_by_key": {"100": 0, "200": 1},
        }
    payload["callback_state_delta"] = 0
    return payload


def witness_payload(config: TargetConfig) -> dict[str, Any]:
    common_input = {
        "identities": [10, 11, 20],
        "callback_initial_state": 7,
    }
    common_boundary = _boundary_payload(config)
    first = {
        "return_unit": True,
        "final_slice": [10, 11, 20],
        "callback_final_state": 7,
    }
    second = {
        "return_unit": True,
        "final_slice": [11, 10, 20],
        "callback_final_state": 7,
    }
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "exact_final_slice_counterexample": {
            "input": common_input,
            "boundary": common_boundary,
            "execution1": first,
            "execution2": second,
            "expected": {
                "execution1_satisfies_active_contract": True,
                "execution2_satisfies_active_contract": True,
                "same_fixed_boundary": True,
                "identity_multiplicities_equal": True,
                "callback_final_state_equal": True,
                "reviewed_equal_class_equivalent": True,
                "exact_final_slice_equal": False,
            },
        },
        "unequal_class_negative_witness": {
            "boundary": common_boundary,
            "execution1": first,
            "execution2": {
                "return_unit": True,
                "final_slice": [20, 11, 10],
                "callback_final_state": 7,
            },
            "expected_reviewed_equivalent": False,
        },
        "foreign_identity_negative_witness": {
            "boundary": common_boundary,
            "execution1": first,
            "execution2": {
                "return_unit": True,
                "final_slice": [12, 11, 20],
                "callback_final_state": 7,
            },
            "expected_reviewed_equivalent": False,
        },
        "callback_state_drift_negative_witness": {
            "boundary": common_boundary,
            "execution1": first,
            "execution2": {
                "return_unit": True,
                "final_slice": [11, 10, 20],
                "callback_final_state": 8,
            },
            "expected_reviewed_equivalent": False,
            "expected_execution2_satisfies_active_contract": False,
        },
    }
