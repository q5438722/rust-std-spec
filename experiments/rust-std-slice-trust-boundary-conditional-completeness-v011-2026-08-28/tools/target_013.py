#!/usr/bin/env python3
"""Literal source/range model for input order 13, as_chunks_mut."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::as_chunks_mut"
INPUT_ORDER = "13"
ARTIFACT_ID = "013_core_slice_as_chunks_mut"
ACTIVE_CONTRACT_SHA256 = (
    "669f8bbc7a27aa64da763386dccd397f1d7e81db22ef7b672e71a40b69ff5e7c"
)
RETAINED_CONTRACT_SHA256 = (
    "8c6cc8f88b4de3b1f2c2c1a25965e3744c851cf8ac05d251cc0effd85d0f590e"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<T, const N: usize>[ <[T]>::as_chunks_mut::<N> ]"
    "( slice: &mut [T], ) -> (ret: (&mut [[T; N]], &mut [T])) requires N != 0, "
    "ensures slice_array_chunks_partition::<T, N>(old(slice)@, ret.0@, ret.1@), "
    "ret.0@.len() == old(slice)@.len() / (N as nat), ret.1@.len() == "
    "old(slice)@.len() % (N as nat), forall|chunk: int| 0 <= chunk < "
    "ret.0@.len() ==> array_value_view::<T, N>(ret.0@[chunk]) == "
    "old(slice)@.subrange(chunk * (N as int), (chunk + 1) * (N as int)), "
    "ret.1@ == old(slice)@.subrange((ret.0@.len() * (N as nat)) as int, "
    "old(slice)@.len() as int), final(ret.0)@.len() == ret.0@.len(), "
    "final(ret.1)@.len() == ret.1@.len(), final(slice)@ == "
    "flatten_array_chunks::<T, N>(final(ret.0)@) + final(ret.1)@, "
    "forall|chunk: int| 0 <= chunk < final(ret.0)@.len() ==> "
    "array_value_view::<T, N>(final(ret.0)@[chunk]) == "
    "final(slice)@.subrange(chunk * (N as int), (chunk + 1) * (N as int)), "
    "final(ret.1)@ == final(slice)@.subrange((final(ret.0)@.len() * "
    "(N as nat)) as int, final(slice)@.len() as int), ;"
)
RETAINED_CONTRACT_TEXT = (
    "pub assume_specification<T, const N: usize>[ <[T]>::as_chunks_mut::<N> ]"
    "( slice: &mut [T], ) -> (ret: (&mut [[T; N]], &mut [T])) requires N != 0, "
    "ensures slice_array_chunks_partition::<T, N>(old(slice)@, ret.0@, ret.1@), "
    "final(slice)@ == flatten_array_chunks::<T, N>(final(ret.0)@) + "
    "final(ret.1)@, ;"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)
ACTIVE_CONJUNCT_SYMBOLS = (
    "ActivePartitionConjunct",
    "ActiveChunksLengthConjunct",
    "ActiveRemainderLengthConjunct",
    "ActiveInitialChunkSubrangesConjunct",
    "ActiveInitialRemainderSubrangeConjunct",
    "ActiveFinalChunksLengthConjunct",
    "ActiveFinalRemainderLengthConjunct",
    "ActiveFinalFrameConjunct",
    "ActiveFinalChunkSubrangesConjunct",
    "ActiveFinalRemainderSubrangeConjunct",
)
OUTPUT_FIELDS = (
    ("y_chunks_ref", "Reference"),
    ("y_remainder_ref", "Reference"),
    ("y_chunks_len", "Int"),
    ("y_remainder_len", "Int"),
    ("y_chunks_source", "Int"),
    ("y_chunks_start", "Int"),
    ("y_chunks_width", "Int"),
    ("y_remainder_source", "Int"),
    ("y_remainder_start", "Int"),
)
STATE_FIELDS = (
    ("s_final_slice_len", "Int"),
    ("s_final_sequence", "Int"),
    ("s_final_chunks_len", "Int"),
    ("s_final_remainder_len", "Int"),
    ("s_final_chunks_source", "Int"),
    ("s_final_chunks_start", "Int"),
    ("s_final_chunks_width", "Int"),
    ("s_final_remainder_source", "Int"),
    ("s_final_remainder_start", "Int"),
)
SOURCE_TRANSITIONS = (
    "AsChunksUncheckedMutReference",
    "SplitAtMutUncheckedRightReference",
    "AsChunksUncheckedMutLength",
    "SplitAtMutUncheckedRightLength",
    "AsChunksUncheckedMutSource",
    "AsChunksUncheckedMutStart",
    "AsChunksUncheckedMutWidth",
    "SplitAtMutUncheckedRightSource",
    "SplitAtMutUncheckedRightStart",
)


def _state_declaration(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    return """\
(declare-datatypes ((State 0))
  (((mkState
      (s_final_slice_len Int)
      (s_final_sequence Int)
      (s_final_chunks_len Int)
      (s_final_remainder_len Int)
      (s_final_chunks_source Int)
      (s_final_chunks_start Int)
      (s_final_chunks_width Int)
      (s_final_remainder_source Int)
      (s_final_remainder_start Int)))))"""


def _final_contract_arguments(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "       (FinalContractExists x y)))"
    return """\
       (ActiveFinalChunksLengthConjunct y (s_final_chunks_len s))
       (ActiveFinalRemainderLengthConjunct y (s_final_remainder_len s))
       (ActiveFinalFrameConjunct
         x
         (s_final_slice_len s)
         (s_final_sequence s)
         (s_final_chunks_len s)
         (s_final_remainder_len s)
         (s_final_chunks_source s)
         (s_final_chunks_start s)
         (s_final_chunks_width s)
         (s_final_remainder_source s)
         (s_final_remainder_start s))
       (ActiveFinalChunkSubrangesConjunct
         x
         (s_final_sequence s)
         (s_final_chunks_source s)
         (s_final_chunks_start s)
         (s_final_chunks_width s))
       (ActiveFinalRemainderSubrangeConjunct
         x
         (s_final_chunks_len s)
         (s_final_sequence s)
         (s_final_remainder_source s)
         (s_final_remainder_start s))))"""


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
        raise ValueError(f"unknown target-013 obligation purpose: {purpose}")
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Retained two-conjunct contract SHA-256 (rejected): {RETAINED_CONTRACT_SHA256}
; Purpose: {purpose}
; Sequence values use canonical source/range descriptors.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_length Int)
      (x_chunk_size Int)
      (x_sequence Int)
      (x_allocation Int)
      (x_borrow Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_input_allocation Int)
      (b_input_borrow Int)))))
(declare-datatypes ((Reference 0))
  (((mkReference
      (ref_allocation Int)
      (ref_parent_borrow Int)
      (ref_start Int)
      (ref_span Int)
      (ref_element_width Int)
      (ref_projection_kind Int)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_chunks_ref Reference)
      (y_remainder_ref Reference)
      (y_chunks_len Int)
      (y_remainder_len Int)
      (y_chunks_source Int)
      (y_chunks_start Int)
      (y_chunks_width Int)
      (y_remainder_source Int)
      (y_remainder_start Int)))))
{_state_declaration(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun AssertNonZero ((x Input)) Bool
  (> (x_chunk_size x) 0))
(define-fun InputIdentityObserved ((x Input) (b Boundary)) Bool
  (and (= (b_input_allocation b) (x_allocation x))
       (= (b_input_borrow b) (x_borrow x))))
(define-fun RoundedLength ((x Input)) Int
  (* (div (x_length x) (x_chunk_size x)) (x_chunk_size x)))
(define-fun SplitAtMutUncheckedLeftReference
  ((x Input)) Reference
  (mkReference
    (x_allocation x) (x_borrow x) 0 (RoundedLength x) 1 1))
(define-fun SplitAtMutUncheckedRightReference
  ((x Input)) Reference
  (mkReference
    (x_allocation x)
    (x_borrow x)
    (RoundedLength x)
    (- (x_length x) (RoundedLength x))
    1
    2))
(define-fun AsChunksUncheckedMutReference
  ((x Input)) Reference
  (mkReference
    (ref_allocation (SplitAtMutUncheckedLeftReference x))
    (ref_parent_borrow (SplitAtMutUncheckedLeftReference x))
    (ref_start (SplitAtMutUncheckedLeftReference x))
    (ref_span (SplitAtMutUncheckedLeftReference x))
    (x_chunk_size x)
    3))
(define-fun SplitAtMutUncheckedLeftLength ((x Input)) Int
  (RoundedLength x))
(define-fun SplitAtMutUncheckedRightLength ((x Input)) Int
  (- (x_length x) (RoundedLength x)))
(define-fun AsChunksUncheckedMutLength ((x Input)) Int
  (div (SplitAtMutUncheckedLeftLength x) (x_chunk_size x)))
(define-fun AsChunksUncheckedMutSource ((x Input)) Int
  (x_sequence x))
(define-fun AsChunksUncheckedMutStart ((x Input)) Int
  (- (x_length x) (x_length x)))
(define-fun AsChunksUncheckedMutWidth ((x Input)) Int
  (x_chunk_size x))
(define-fun SplitAtMutUncheckedRightSource ((x Input)) Int
  (x_sequence x))
(define-fun SplitAtMutUncheckedRightStart ((x Input)) Int
  (RoundedLength x))
(define-fun ActivePartitionConjunct ((x Input) (y Output)) Bool
  (and (> (x_chunk_size x) 0)
       (>= (y_remainder_len y) 0)
       (< (y_remainder_len y) (x_chunk_size x))
       (= (x_length x)
          (+ (* (y_chunks_len y) (x_chunk_size x))
             (y_remainder_len y)))
       (= (y_chunks_source y) (x_sequence x))
       (= (y_chunks_start y) 0)
       (= (y_chunks_width y) (x_chunk_size x))
       (= (y_remainder_source y) (x_sequence x))
       (= (y_remainder_start y)
          (* (y_chunks_len y) (x_chunk_size x)))))
(define-fun ActiveChunksLengthConjunct ((x Input) (y Output)) Bool
  (= (y_chunks_len y) (div (x_length x) (x_chunk_size x))))
(define-fun ActiveRemainderLengthConjunct ((x Input) (y Output)) Bool
  (= (y_remainder_len y) (mod (x_length x) (x_chunk_size x))))
(define-fun ActiveInitialChunkSubrangesConjunct
  ((x Input) (y Output)) Bool
  (and (= (y_chunks_source y) (x_sequence x))
       (= (y_chunks_start y) 0)
       (= (y_chunks_width y) (x_chunk_size x))))
(define-fun ActiveInitialRemainderSubrangeConjunct
  ((x Input) (y Output)) Bool
  (and (= (y_remainder_source y) (x_sequence x))
       (= (y_remainder_start y)
          (* (y_chunks_len y) (x_chunk_size x)))))
(define-fun ActiveFinalChunksLengthConjunct
  ((y Output) (final_chunks_len Int)) Bool
  (= final_chunks_len (y_chunks_len y)))
(define-fun ActiveFinalRemainderLengthConjunct
  ((y Output) (final_remainder_len Int)) Bool
  (= final_remainder_len (y_remainder_len y)))
(define-fun ActiveFinalFrameConjunct
  ((x Input)
   (final_slice_len Int)
   (final_sequence Int)
   (final_chunks_len Int)
   (final_remainder_len Int)
   (final_chunks_source Int)
   (final_chunks_start Int)
   (final_chunks_width Int)
   (final_remainder_source Int)
   (final_remainder_start Int)) Bool
  (and (= final_slice_len (x_length x))
       (= final_slice_len
          (+ (* final_chunks_len (x_chunk_size x)) final_remainder_len))
       (= final_chunks_source final_sequence)
       (= final_chunks_start 0)
       (= final_chunks_width (x_chunk_size x))
       (= final_remainder_source final_sequence)
       (= final_remainder_start
          (* final_chunks_len (x_chunk_size x)))))
(define-fun ActiveFinalChunkSubrangesConjunct
  ((x Input)
   (final_sequence Int)
   (final_chunks_source Int)
   (final_chunks_start Int)
   (final_chunks_width Int)) Bool
  (and (= final_chunks_source final_sequence)
       (= final_chunks_start 0)
       (= final_chunks_width (x_chunk_size x))))
(define-fun ActiveFinalRemainderSubrangeConjunct
  ((x Input)
   (final_chunks_len Int)
   (final_sequence Int)
   (final_remainder_source Int)
   (final_remainder_start Int)) Bool
  (and (= final_remainder_source final_sequence)
       (= final_remainder_start
          (* final_chunks_len (x_chunk_size x)))))
(define-fun FinalContractExists ((x Input) (y Output)) Bool
  (exists
    ((final_slice_len Int)
     (final_sequence Int)
     (final_chunks_len Int)
     (final_remainder_len Int)
     (final_chunks_source Int)
     (final_chunks_start Int)
     (final_chunks_width Int)
     (final_remainder_source Int)
     (final_remainder_start Int))
    (and
      (ActiveFinalChunksLengthConjunct y final_chunks_len)
      (ActiveFinalRemainderLengthConjunct y final_remainder_len)
      (ActiveFinalFrameConjunct
        x final_slice_len final_sequence final_chunks_len final_remainder_len
        final_chunks_source final_chunks_start final_chunks_width
        final_remainder_source final_remainder_start)
      (ActiveFinalChunkSubrangesConjunct
        x final_sequence final_chunks_source final_chunks_start final_chunks_width)
      (ActiveFinalRemainderSubrangeConjunct
        x final_chunks_len final_sequence
        final_remainder_source final_remainder_start))))
(define-fun Requires_T ((x Input)) Bool
  (and (>= (x_length x) 0)
       (AssertNonZero x)))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (>= (b_input_allocation b) 0)
       (>= (b_input_borrow b) 0)
       (InputIdentityObserved x b)))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (AssertNonZero x)
       (InputIdentityObserved x b)
       (= (y_chunks_ref y) (AsChunksUncheckedMutReference x))
       (= (y_remainder_ref y) (SplitAtMutUncheckedRightReference x))
       (= (y_chunks_len y) (AsChunksUncheckedMutLength x))
       (= (y_remainder_len y) (SplitAtMutUncheckedRightLength x))
       (= (y_chunks_source y) (AsChunksUncheckedMutSource x))
       (= (y_chunks_start y) (AsChunksUncheckedMutStart x))
       (= (y_chunks_width y) (AsChunksUncheckedMutWidth x))
       (= (y_remainder_source y) (SplitAtMutUncheckedRightSource x))
       (= (y_remainder_start y) (SplitAtMutUncheckedRightStart x))
       (ActivePartitionConjunct x y)
       (ActiveChunksLengthConjunct x y)
       (ActiveRemainderLengthConjunct x y)
       (ActiveInitialChunkSubrangesConjunct x y)
       (ActiveInitialRemainderSubrangeConjunct x y)
{_final_contract_arguments(purpose)}
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
        raise ValueError(f"unknown target-013 obligation purpose: {purpose}")
    return {
        "schema_version": 2,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "rejected_retained_contract_sha256": RETAINED_CONTRACT_SHA256,
        "rejected_retained_contract_text": RETAINED_CONTRACT_TEXT,
        "domain": {
            "input_length": "arbitrary nonnegative integer",
            "chunk_size": "arbitrary positive integer",
            "sequence_representation": (
                "canonical content identity plus source range; this represents "
                "all chunk and remainder values without finite enumeration"
            ),
            "reference_identity": (
                "structural allocation/parent-borrow/subrange/element-width/"
                "projection tuple; no synthetic hash or answer oracle"
            ),
        },
        "contract_translation": {
            "active_conjuncts": list(ACTIVE_CONJUNCT_SYMBOLS),
            "source_flow": [
                "assert N != 0",
                "len_rounded_down = len / N * N",
                "split_at_mut_unchecked(len_rounded_down)",
                "as_chunks_unchecked_mut(multiple_of_n)",
            ],
            "final_state_projection": (
                "explicit theorem state"
                if purpose == PRIMARY
                else "existentially retained while comparing exact return only"
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                "input allocation identity",
                "input mutable-borrow identity",
            ],
            "excluded_observations": [
                "returned references",
                "chunks",
                "remainder",
                "aggregate final state",
                "answer encodings",
                "complete execution traces",
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
                    "core/src/slice/mod.rs:1557-1559",
                    "proof_harnesses/086_core_slice_split_at_mut_unchecked/harness.rs",
                ],
                "trust_site_ids": ["TS-013-D002", "TS-013-E001", "TS-013-E002"],
            },
            {
                "selector": "b_input_borrow",
                "role": "input_provenance",
                "source_citations": [
                    "core/src/slice/mod.rs:1557-1561",
                    "proof_harnesses/015_core_slice_as_chunks_unchecked_mut/harness.rs",
                ],
                "trust_site_ids": ["TS-013-D002", "TS-013-D003", "TS-013-E003"],
            },
        ],
        "declared_functions": [],
        "source_transition_definitions": list(SOURCE_TRANSITIONS),
        "source_transition_bindings": {
            "assert": {
                "symbol": "AssertNonZero",
                "trust_site_ids": ["TS-013-D004"],
                "source_citations": ["core/src/slice/mod.rs:1553"],
            },
            "rounded_length": {
                "symbol": "RoundedLength",
                "trust_site_ids": ["TS-013-D004"],
                "source_citations": ["core/src/slice/mod.rs:1554"],
            },
            "split_at_mut_unchecked": {
                "symbols": [
                    "SplitAtMutUncheckedLeftReference",
                    "SplitAtMutUncheckedRightReference",
                    "SplitAtMutUncheckedLeftLength",
                    "SplitAtMutUncheckedRightLength",
                    "SplitAtMutUncheckedRightSource",
                    "SplitAtMutUncheckedRightStart",
                ],
                "trust_site_ids": ["TS-013-D002", "TS-013-E001", "TS-013-E002"],
                "source_citations": ["core/src/slice/mod.rs:1557-1559"],
            },
            "as_chunks_unchecked_mut": {
                "symbols": [
                    "AsChunksUncheckedMutReference",
                    "AsChunksUncheckedMutLength",
                    "AsChunksUncheckedMutSource",
                    "AsChunksUncheckedMutStart",
                    "AsChunksUncheckedMutWidth",
                ],
                "trust_site_ids": ["TS-013-D003", "TS-013-E003"],
                "source_citations": ["core/src/slice/mod.rs:1560-1561"],
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "principal return, returned-reference identity, and final state"
            if purpose == PRIMARY
            else "principal return and returned-reference identity"
        ),
        "principal_observations": _principal_observations(purpose),
        "expected_solver_result": "sat" if purpose == PRIMARY else "unsat",
    }


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return obligation_text(purpose), obligation_metadata(purpose)


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
                "trust_site_ids": ["TS-013-D002", "TS-013-E001", "TS-013-E002"],
            },
            {
                "field": "b_input_borrow",
                "meaning": "identity of the input mutable borrow",
                "trust_site_ids": ["TS-013-D002", "TS-013-D003", "TS-013-E003"],
            },
        ],
        "deterministic_source_transitions": [
            {
                "operation": "assert N != 0",
                "semantics": "Requires_T fixes N > 0, so the source assertion succeeds",
                "trust_site_ids": ["TS-013-D004"],
            },
            {
                "operation": "rounded-down length",
                "semantics": "len_rounded_down = (len div N) * N",
                "trust_site_ids": ["TS-013-D004"],
            },
            {
                "operation": "split_at_mut_unchecked",
                "semantics": (
                    "produces prefix [0,len_rounded_down) and suffix "
                    "[len_rounded_down,len), with derived borrow identities and "
                    "immutable slice lengths"
                ),
                "trust_site_ids": [
                    "TS-013-D002",
                    "TS-013-E001",
                    "TS-013-E002",
                ],
            },
            {
                "operation": "as_chunks_unchecked_mut",
                "semantics": (
                    "reinterprets the divisible prefix as N-wide arrays without "
                    "changing its source range, with an immutable chunk count"
                ),
                "trust_site_ids": ["TS-013-D003", "TS-013-E003"],
            },
        ],
        "verus_external_bodies": [
            {
                "symbol": "from_raw_parts_mut",
                "trust_site_id": "TS-013-E001",
                "assumes": "intermediate raw-slice length and start-pointer relation",
                "target_postcondition_coverage": "partial lower transition",
            },
            {
                "symbol": "rust_1_96_split_at_mut_unchecked_raw_parts",
                "trust_site_id": "TS-013-E002",
                "assumes": (
                    "intermediate prefix/suffix views, final concatenation frame, "
                    "and immutable child-slice lengths"
                ),
                "target_postcondition_coverage": "partial lower transition",
            },
            {
                "symbol": "as_chunks_unchecked_mut",
                "trust_site_id": "TS-013-E003",
                "assumes": (
                    "divisible-prefix flattening, mutable final frame, and "
                    "immutable returned chunk count"
                ),
                "target_postcondition_coverage": "partial lower transition",
            },
        ],
        "context_only_trust_sites": [
            "TS-013-D001",
            "TS-013-C001",
            "TS-013-C002",
            "TS-013-C003",
        ],
        "all_audited_trust_site_ids": [
            "TS-013-D001",
            "TS-013-D002",
            "TS-013-D003",
            "TS-013-D004",
            "TS-013-C001",
            "TS-013-C002",
            "TS-013-C003",
            "TS-013-E001",
            "TS-013-E002",
            "TS-013-E003",
        ],
        "excluded_from_boundary": [
            "returned reference identities",
            "chunks or remainder values",
            "aggregate final state",
            "equivalent answer encodings",
            "selected or complete execution traces",
        ],
    }


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError("target-013 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-013 metadata differs from the reviewed active-contract translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-013 SMT differs from the reviewed active-contract translation"
        )


def witness_payload() -> dict[str, Any]:
    allocation = 5
    borrow = 7
    rounded = 2
    output = {
        "chunks_reference": {
            "allocation": allocation,
            "parent_borrow": borrow,
            "start": 0,
            "span": rounded,
            "element_width": 2,
            "projection_kind": "array-chunks",
        },
        "remainder_reference": {
            "allocation": allocation,
            "parent_borrow": borrow,
            "start": rounded,
            "span": 1,
            "element_width": 1,
            "projection_kind": "slice-remainder",
        },
        "chunks": [[10, 20]],
        "remainder": [30],
    }
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "input": {
            "chunk_size": 2,
            "slice": [10, 20, 30],
            "allocation": allocation,
            "borrow": borrow,
        },
        "boundary": {
            "input_allocation": allocation,
            "input_borrow": borrow,
        },
        "execution1": {
            "output": output,
            "final": {
                "slice": [1, 2, 3],
                "chunks": [[1, 2]],
                "remainder": [3],
            },
        },
        "execution2": {
            "output": output,
            "final": {
                "slice": [4, 5, 6],
                "chunks": [[4, 5]],
                "remainder": [6],
            },
        },
        "expected": {
            "same_boundary": True,
            "execution1_satisfies_all_active_conjuncts": True,
            "execution2_satisfies_all_active_conjuncts": True,
            "exact_output_equal": True,
            "exact_final_state_equal": False,
            "full_exact_equivalent": False,
        },
    }


def fixed_model_text() -> str:
    text = obligation_text(PRIMARY)
    terminal = "(check-sat)\n"
    if not text.endswith(terminal):
        raise ValueError("target obligation lacks the expected terminal check-sat")
    return (
        text[: -len(terminal)]
        + """\
(assert (= x (mkInput 3 2 99 5 7)))
(assert (= b (mkBoundary 5 7)))
(assert (= y1 (mkOutput
  (mkReference 5 7 0 2 2 3)
  (mkReference 5 7 2 1 1 2)
  1 1 99 0 2 99 2)))
(assert (= s1 (mkState 3 101 1 1 101 0 2 101 2)))
(assert (= y2 (mkOutput
  (mkReference 5 7 0 2 2 3)
  (mkReference 5 7 2 1 1 2)
  1 1 99 0 2 99 2)))
(assert (= s2 (mkState 3 202 1 1 202 0 2 202 2)))
(check-sat)
(get-value (
  (y_chunks_ref y1)
  (y_remainder_ref y1)
  (s_final_sequence s1)
  (s_final_sequence s2)
  (Equivalent_T x b y1 s1 y2 s2)))
"""
    )
