#!/usr/bin/env python3
"""Mechanical adapter/insert_tail binding for target-079 refinement v3."""

from __future__ import annotations

import copy
import re
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterator

import target_078_insert_tail_refinement_v3 as insert_analogue
import target_079_adapter_refinement_v2 as adapter_model
import target_079_exact_smt_v1 as exact_smt
import target_079_operational_smt_v1 as accepted_smt
import target_079_operational_v1 as accepted_model


ROOT = Path(__file__).resolve().parents[1]
TARGET = accepted_model.TARGET
INPUT_ORDER = accepted_model.INPUT_ORDER
MODEL_ID = "target-079-insert-tail-refinement-v3-rust-1.96"
MODEL_VERSION = 3
PROOF_PATH = (
    ROOT
    / "proofs/"
    "079_core_slice_select_nth_unstable_by_key_insert_tail_refinement_v3.rs"
)
ACCEPTED_ADAPTER_PROOF_PATH = adapter_model.PROOF_PATH
ACCEPTED_SMT_PATH = ROOT / "tools/target_079_exact_smt_v1.py"
ACCEPTED_RESULT_PATH = (
    ROOT / "evidence/target_079_operational_v1/result.json"
)
ACCEPTED_BOUNDARY_PATH = (
    ROOT / "evidence/target_079_operational_v1/boundary_manifest.json"
)
ACCEPTED_ADAPTER_RESULT_PATH = (
    ROOT / "evidence/target_079_adapter_refinement_v2/result.json"
)
SOURCE_PATH = (
    ROOT / "evidence/target_079_operational_v1/bound_inputs/smallsort.rs"
)
PRESERVATION_V2_PATH = ROOT / "preservation/path_policy_v2.json"

ADAPTER_CORE_FUNCTIONS = (
    "key_result",
    "key_next_state",
    "key_panics",
    "ord_lt_result",
    "ord_lt_next_state",
    "ord_lt_panics",
    "drop_next_state",
    "drop_panics",
    "owned_key",
    "adapter_initial",
    "adapter_key_left",
    "adapter_key_right",
    "adapter_ord_lt",
    "adapter_drop_right",
    "adapter_drop_left",
    "adapter_transition",
)
ADAPTER_SIGNATURES = {
    name: adapter_model.VERUS_SEMANTIC_SIGNATURES[name]
    for name in ADAPTER_CORE_FUNCTIONS
}
INSERT_SIGNATURES = {
    "callback_frame": (
        (
            ("state", "InsertTailState"),
            ("boundary", "KeyOrdDropBoundary"),
            ("left", "int"),
            ("right", "int"),
        ),
        "AdapterFrame",
    ),
    "adapter_callback": (
        (
            ("state", "InsertTailState"),
            ("boundary", "KeyOrdDropBoundary"),
            ("left", "int"),
            ("right", "int"),
        ),
        "InsertTailState",
    ),
    "target_adapter_is_less": (
        (
            ("state", "InsertTailState"),
            ("boundary", "KeyOrdDropBoundary"),
            ("left", "int"),
            ("right", "int"),
        ),
        "bool",
    ),
    "shifted_state": (
        (
            ("state", "InsertTailState"),
            ("sift", "int"),
            ("gap", "int"),
        ),
        "InsertTailState",
    ),
    "restored_state": (
        (
            ("state", "InsertTailState"),
            ("destination", "int"),
            ("temporary", "int"),
            ("panicked", "bool"),
        ),
        "InsertTailState",
    ),
    "insert_tail_loop": (
        (
            ("state", "InsertTailState"),
            ("boundary", "KeyOrdDropBoundary"),
            ("begin", "int"),
            ("sift", "int"),
            ("gap", "int"),
            ("temporary", "int"),
        ),
        "InsertTailState",
    ),
    "insert_tail": (
        (
            ("state", "InsertTailState"),
            ("boundary", "KeyOrdDropBoundary"),
            ("begin", "int"),
            ("tail", "int"),
        ),
        "InsertTailState",
    ),
}
ADAPTER_REFINED_FUNCTION_NAMES = {
    name: adapter_model.REFINED_FUNCTION_NAMES[name]
    for name in ADAPTER_CORE_FUNCTIONS
}
INSERT_REFINED_FUNCTION_NAMES = {
    name: "Refined" + "".join(part.title() for part in name.split("_"))
    for name in INSERT_SIGNATURES
}
REFINED_FUNCTION_NAMES = {
    **ADAPTER_REFINED_FUNCTION_NAMES,
    **INSERT_REFINED_FUNCTION_NAMES,
}
RECURSIVE_FUNCTIONS = {"insert_tail_loop"}

SMT_FIELD_BINDINGS = {
    "OwnedKey": adapter_model.SMT_FIELD_BINDINGS["OwnedKey"],
    "AdapterFrame": adapter_model.SMT_FIELD_BINDINGS["AdapterFrame"],
    "KeyOrdDropBoundary": adapter_model.SMT_FIELD_BINDINGS["Boundary"],
    "InsertTailState": (
        "e_sequence",
        "e_callback_state",
        "e_panicked",
        "e_aborted",
    ),
}
VERUS_STRUCT_FIELD_TYPES = {
    "OwnedKey": adapter_model.VERUS_STRUCT_FIELD_TYPES["OwnedKey"],
    "AdapterFrame": adapter_model.VERUS_STRUCT_FIELD_TYPES["AdapterFrame"],
    "KeyOrdDropBoundary": (
        adapter_model.VERUS_STRUCT_FIELD_TYPES["KeyOrdDropBoundary"]
    ),
    "InsertTailState": (
        ("e_sequence", "Seq<int>"),
        ("e_callback_state", "int"),
        ("e_panicked", "bool"),
        ("e_aborted", "bool"),
    ),
}
SMT_FIELD_SORTS = {
    "Boundary": adapter_model.SMT_FIELD_SORTS["Boundary"],
    "ExactState": (
        ("e_sequence", "(Array Int Int)"),
        ("e_callback_state", "Int"),
        ("e_panicked", "Bool"),
        ("e_aborted", "Bool"),
    ),
}
ALL_OPEN_SPEC_FUNCTIONS = (
    *ADAPTER_CORE_FUNCTIONS,
    "callback_frame",
    "adapter_callback",
    "target_adapter_is_less",
    "shifted_state",
    "restored_state",
    "restored_sequence",
    "valid_insert_tail_input",
    "valid_insert_tail_loop_input",
    "insert_tail_loop",
    "insert_tail",
)
REQUIRED_PROOFS = (
    "callback_is_derived_from_adapter_transition",
    "initial_adapter_panic_precedes_gap_creation",
    "initial_adapter_abort_precedes_gap_creation",
    "no_shift_path_is_exact",
    "initial_less_enters_loop_with_tail_gap",
    "loop_at_begin_restores_temporary",
    "loop_normal_stop_restores_temporary",
    "loop_ordinary_panic_restores_active_gap",
    "loop_abort_bypasses_copy_on_drop",
    "loop_less_advances_sift_and_gap",
    "shift_then_restore_preserves_identity_multiplicity",
    "insert_tail_loop_preserves_length_and_outside_frame",
    "insert_tail_loop_nonabort_preserves_identity_multiplicity",
    "insert_tail_preserves_length_frame_and_nonabort_multiplicity",
)
PINNED_GUARD_FUNCTIONS = (
    "restored_sequence",
    "valid_insert_tail_input",
    "valid_insert_tail_loop_input",
)
EXPECTED_GUARD_SHA256 = {
    "restored_sequence": (
        "92c8b141ba87d58ee1a2dad0bb1a7ba2a192ffbd786c35304f773b2a18a1b173"
    ),
    "valid_insert_tail_input": (
        "2a9d3734039bf4c888bde0d6ae56e92bd585136bb825b96a435a8f3e82403821"
    ),
    "valid_insert_tail_loop_input": (
        "896e6ed27fc03472e806f1c6b41493d1870e0a1c4875489e3e9a193e598845d6"
    ),
}
SOURCE_ORDER = (
    "derive every callback frame from accepted adapter_transition",
    "perform the initial adapter call before creating an insertion gap",
    "move sift into the current gap only after a normal Less result",
    "advance the guard destination from gap to sift",
    "commit callback state before ordinary panic or abort propagation",
    "restore the active gap on normal return and ordinary panic",
    "bypass CopyOnDrop restoration after double-panic abort",
)
MUTATION_KINDS = (
    "adapter-operands",
    "lookup-state",
    "less-gating",
    "shift-source",
    "shift-destination",
    "gap-advancement",
    "callback-state",
    "panic-restoration",
    "abort-discrimination",
    "cleanup-bypass",
)
WITNESS_KINDS = (
    "no-shift",
    "multi-shift",
    "ordinary-panic-after-shift",
    "abort-after-shift",
)
VERUS_INSENSITIVE_MUTATIONS = {
    "adapter-operands",
    "less-gating",
}
VERUS_INSENSITIVITY_REASON = (
    "the proof obligations consume adapter_transition and "
    "target_adapter_is_less through their own definitions, so these two "
    "definition-consistent mutations are rejected by AST correspondence "
    "rather than by the Verus lemmas"
)
LOOP_DOMAIN = (
    "(and (not (e_panicked loop_state)) "
    "(not (e_aborted loop_state)) "
    "(<= 0 loop_begin) "
    "(<= loop_begin loop_sift) "
    "(= loop_gap (+ loop_sift 1)) "
    "(< loop_gap loop_sequence_len))"
)
ENTRY_DOMAIN = (
    "(and (not (e_panicked entry_state)) "
    "(not (e_aborted entry_state)) "
    "(<= 0 entry_begin) "
    "(< entry_begin entry_tail) "
    "(< entry_tail entry_sequence_len))"
)
EXPECTED_DOMAIN_SHA256 = {
    "loop": (
        "e72153dfcc72dcd45edb8ff97de962c56e7f42999ff582798c792bd069d10a5f"
    ),
    "entry": (
        "d18b4863c8734912efbcf96251532401a11acf2b84a632de34993e05df3fc0be"
    ),
}

_MUTATIONS = {
    "adapter-operands": (
        "adapter_transition",
        (
            (
                "boundary,\n                        left,",
                "boundary,\n                        right,",
                1,
            ),
        ),
    ),
    "lookup-state": (
        "callback_frame",
        (("state.e_callback_state,", "boundary.b_initial_state,", 1),),
    ),
    "less-gating": (
        "target_adapter_is_less",
        ((").af_is_less", ").af_left_live", 1),),
    ),
    "shift-source": (
        "shifted_state",
        (("state.e_sequence[sift],", "state.e_sequence[gap],", 1),),
    ),
    "shift-destination": (
        "shifted_state",
        (
            (
                "state.e_sequence.update(\n"
                "            gap,\n"
                "            state.e_sequence[sift],",
                "state.e_sequence.update(\n"
                "            sift,\n"
                "            state.e_sequence[sift],",
                1,
            ),
        ),
    ),
    "gap-advancement": (
        "insert_tail_loop",
        (
            (
                "next_sift,\n"
                "                    sift,\n"
                "                    temporary,",
                "next_sift,\n"
                "                    gap,\n"
                "                    temporary,",
                1,
            ),
        ),
    ),
    "callback-state": (
        "adapter_callback",
        (
            (
                "e_callback_state: frame.af_state,",
                "e_callback_state: state.e_callback_state,",
                1,
            ),
        ),
    ),
    "panic-restoration": (
        "insert_tail_loop",
        (
            (
                "restored_state(called, sift, temporary, true)",
                "restored_state(called, gap, temporary, true)",
                1,
            ),
        ),
    ),
    "abort-discrimination": (
        "adapter_callback",
        (
            (
                "e_aborted: frame.af_termination == 2,",
                "e_aborted: frame.af_termination == 1,",
                1,
            ),
        ),
    ),
    "cleanup-bypass": (
        "restored_state",
        (("if state.e_aborted {", "if false {", 1),),
    ),
}


def digest_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def digest_path(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"required target-079 v3 artifact is missing: {path}")
    return digest_bytes(path.read_bytes())


def _adapter_source(
    text: str,
    functions: tuple[str, ...] = ADAPTER_CORE_FUNCTIONS,
) -> str:
    return "\n\n".join(
        adapter_model._extract_verus_item(text, "open spec fn", name)
        for name in functions
    )


@contextmanager
def _adapter_translation_configuration(
    signatures: dict[
        str,
        tuple[tuple[tuple[str, str], ...], str],
    ],
) -> Iterator[None]:
    previous_signatures = adapter_model.VERUS_SEMANTIC_SIGNATURES
    previous_refined = adapter_model.REFINED_FUNCTION_NAMES
    adapter_model.VERUS_SEMANTIC_SIGNATURES = signatures
    adapter_model.REFINED_FUNCTION_NAMES = ADAPTER_REFINED_FUNCTION_NAMES
    try:
        yield
    finally:
        adapter_model.VERUS_SEMANTIC_SIGNATURES = previous_signatures
        adapter_model.REFINED_FUNCTION_NAMES = previous_refined


def _derive_adapter_smt(
    text: str,
    functions: tuple[str, ...] = ADAPTER_CORE_FUNCTIONS,
) -> dict[str, Any]:
    source = _adapter_source(text, functions)
    signatures = {
        name: ADAPTER_SIGNATURES[name] for name in functions
    }
    with _adapter_translation_configuration(signatures):
        derived = adapter_model._derive_verus_smt(source)
    derived["full_source_sha256"] = digest_bytes(text.encode())
    return derived


@contextmanager
def _insert_translation_configuration() -> Iterator[None]:
    replacements = {
        "SMT_FIELD_BINDINGS": {
            "OwnedKey": SMT_FIELD_BINDINGS["OwnedKey"],
            "AdapterFrame": SMT_FIELD_BINDINGS["AdapterFrame"],
            "InsertTailState": SMT_FIELD_BINDINGS["InsertTailState"],
        },
        "VERUS_SEMANTIC_SIGNATURES": INSERT_SIGNATURES,
        "REFINED_FUNCTION_NAMES": REFINED_FUNCTION_NAMES,
        "RECURSIVE_FUNCTIONS": RECURSIVE_FUNCTIONS,
        "_STRUCT_CONSTRUCTORS": {
            "OwnedKey": "mkOwnedKey",
            "AdapterFrame": "mkAdapterFrame",
            "InsertTailState": "mkExactState",
        },
        "_BOUNDARY_INDEX_ENCODINGS": (
            adapter_model._BOUNDARY_INDEX_ENCODINGS
        ),
        "_VERUS_TYPE_TO_SMT": {
            "int": "Int",
            "bool": "Bool",
            "OwnedKey": "OwnedKey",
            "AdapterFrame": "AdapterFrame",
            "KeyOrdDropBoundary": "Boundary",
            "InsertTailState": "ExactState",
        },
    }
    previous = {
        name: getattr(insert_analogue, name) for name in replacements
    }
    for name, value in replacements.items():
        setattr(insert_analogue, name, value)
    try:
        yield
    finally:
        for name, value in previous.items():
            setattr(insert_analogue, name, value)


def _derive_insert_smt(text: str) -> dict[str, Any]:
    with _insert_translation_configuration():
        return insert_analogue._derive_verus_smt(text)


def _derive_all_smt(text: str) -> dict[str, Any]:
    adapter = _derive_adapter_smt(text)
    insertion = _derive_insert_smt(text)
    return {
        "definitions": [
            *adapter["definitions"],
            *insertion["definitions"],
        ],
        "adapter": adapter,
        "insertion": insertion,
        "source_sha256": digest_bytes(text.encode()),
    }


def _adapter_components() -> tuple[str, list[str], list[str]]:
    arguments = adapter_model._correspondence_arguments()
    accepted = adapter_model._accepted_correspondence_expressions()
    declarations = r"""
(declare-const correspondence_boundary Boundary)
(declare-const correspondence_state Int)
(declare-const correspondence_left Int)
(declare-const correspondence_right Int)
(declare-const correspondence_slot Int)
(declare-const correspondence_key Int)
(declare-const correspondence_input_frame AdapterFrame)
(declare-const correspondence_owned_left OwnedKey)
(declare-const correspondence_owned_right OwnedKey)
"""
    aliases: list[str] = []
    equalities: list[str] = []
    for name, (_parameters, return_type) in ADAPTER_SIGNATURES.items():
        smt_return = adapter_model._VERUS_TYPE_TO_SMT[return_type]
        if name == "adapter_transition":
            accepted_alias = "accepted_frame"
            refined_alias = "refined_frame"
        else:
            accepted_alias = f"accepted_{name}"
            refined_alias = f"refined_{name}"
        aliases.extend(
            (
                f"(define-fun {accepted_alias} () {smt_return}\n"
                f"  {accepted[name]})",
                f"(define-fun {refined_alias} () {smt_return}\n"
                f"  ({ADAPTER_REFINED_FUNCTION_NAMES[name]} "
                f"{' '.join(arguments[name])}))",
            )
        )
        if return_type == "AdapterFrame":
            fields = SMT_FIELD_BINDINGS["AdapterFrame"]
        elif return_type == "OwnedKey":
            fields = SMT_FIELD_BINDINGS["OwnedKey"]
        else:
            fields = ()
        if fields:
            equalities.extend(
                f"(= ({field} {accepted_alias}) "
                f"({field} {refined_alias}))"
                for field in fields
            )
        else:
            equalities.append(f"(= {accepted_alias} {refined_alias})")
    return declarations, aliases, equalities


def adapter_correspondence_coverage() -> dict[str, Any]:
    _declarations, _aliases, equalities = _adapter_components()
    return {
        "semantic_functions": list(ADAPTER_CORE_FUNCTIONS),
        "adapter_fields": list(SMT_FIELD_BINDINGS["AdapterFrame"]),
        "owned_key_fields": list(SMT_FIELD_BINDINGS["OwnedKey"]),
        "boundary_fields": list(
            SMT_FIELD_BINDINGS["KeyOrdDropBoundary"]
        ),
        "comparison_count": len(equalities),
    }


def adapter_correspondence_query_text(
    proof_text: str | None = None,
) -> str:
    if proof_text is None:
        proof_text = PROOF_PATH.read_text()
    derived = _derive_adapter_smt(proof_text)
    declarations, aliases, equalities = _adapter_components()
    equality_text = "\n      ".join(equalities)
    return (
        accepted_smt._prefix()
        + "\n"
        + (
            "; Refined adapter definitions below are mechanically translated\n"
            "; from the parsed Verus expression AST, not copied from SMT.\n"
            f"; Verus source SHA-256: {derived['full_source_sha256']}\n"
        )
        + "\n".join(derived["definitions"])
        + declarations
        + "\n".join(aliases)
        + """
(assert
  (not
    (and
      """
        + equality_text
        + """)))
(check-sat)
"""
    )


def validate_adapter_correspondence_query(text: str) -> None:
    _declarations, _aliases, equalities = _adapter_components()
    for equality in equalities:
        if text.count(equality) != 1:
            raise ValueError(
                "adapter correspondence does not compare exactly once: "
                f"{equality}"
            )
    for refined in ADAPTER_REFINED_FUNCTION_NAMES.values():
        if text.count(f"(define-fun {refined} ") != 1:
            raise ValueError(
                f"adapter correspondence does not derive {refined} once"
            )
    if text.count("(assert") != 1 or text.count("(check-sat)") != 1:
        raise ValueError("adapter correspondence query shape changed")
    if "(get-model)" in text:
        raise ValueError("UNSAT adapter correspondence requests a model")
    if "mechanically translated" not in text:
        raise ValueError("adapter correspondence lacks AST marker")


def _state_equalities(left: str, right: str) -> list[str]:
    return [
        f"(= ({field} {left}) ({field} {right}))"
        for field in SMT_FIELD_BINDINGS["InsertTailState"]
    ]


def _state_difference(left: str, right: str) -> str:
    comparisons = " ".join(
        f"(not (= ({field} {left}) ({field} {right})))"
        for field in SMT_FIELD_BINDINGS["InsertTailState"]
    )
    return f"(or {comparisons})"


def _helper_correspondence() -> tuple[str, list[str]]:
    declarations = r"""
(declare-const helper_boundary Boundary)
(declare-const helper_state ExactState)
(declare-const helper_left Int)
(declare-const helper_right Int)
(declare-const helper_sift Int)
(declare-const helper_gap Int)
(declare-const helper_destination Int)
(declare-const helper_temporary Int)
(declare-const helper_panicked Bool)

(define-fun accepted_callback () ExactState
  (ExactCallback helper_state helper_boundary helper_left helper_right))
(define-fun refined_callback () ExactState
  (RefinedAdapterCallback
    helper_state helper_boundary helper_left helper_right))
(define-fun accepted_target_less () Bool
  (TargetAdapterIsLess
    helper_boundary
    (e_callback_state helper_state)
    helper_left
    helper_right))
(define-fun refined_target_less () Bool
  (RefinedTargetAdapterIsLess
    helper_state helper_boundary helper_left helper_right))
(define-fun accepted_shifted () ExactState
  (mkExactState
    (store
      (e_sequence helper_state)
      helper_gap
      (select (e_sequence helper_state) helper_sift))
    (e_callback_state helper_state)
    false
    false))
(define-fun refined_shifted () ExactState
  (RefinedShiftedState helper_state helper_sift helper_gap))
(define-fun accepted_restored () ExactState
  (ite
    (e_aborted helper_state)
    helper_state
    (mkExactState
      (store
        (e_sequence helper_state)
        helper_destination
        helper_temporary)
      (e_callback_state helper_state)
      helper_panicked
      false)))
(define-fun refined_restored () ExactState
  (RefinedRestoredState
    helper_state helper_destination helper_temporary helper_panicked))
"""
    equalities = [
        *_state_equalities("accepted_callback", "refined_callback"),
        "(= accepted_target_less refined_target_less)",
        *_state_equalities("accepted_shifted", "refined_shifted"),
        *_state_equalities("accepted_restored", "refined_restored"),
    ]
    return declarations, equalities


def _loop_step_correspondence() -> tuple[str, str, list[str], str]:
    declarations = r"""
(declare-const loop_boundary Boundary)
(declare-const loop_state ExactState)
(declare-const loop_begin Int)
(declare-const loop_sift Int)
(declare-const loop_gap Int)
(declare-const loop_temporary Int)
(declare-const loop_sequence_len Int)

(define-fun exact_loop_shifted () ExactState
  (mkExactState
    (store
      (e_sequence loop_state)
      loop_gap
      (select (e_sequence loop_state) loop_sift))
    (e_callback_state loop_state)
    false
    (e_aborted loop_state)))
(define-fun refined_loop_shifted () ExactState
  (RefinedShiftedState loop_state loop_sift loop_gap))
(define-fun exact_loop_right () Int
  (select (e_sequence exact_loop_shifted) (- loop_sift 1)))
(define-fun refined_loop_right () Int
  (select (e_sequence refined_loop_shifted) (- loop_sift 1)))
(define-fun exact_loop_called () ExactState
  (ExactCallback
    exact_loop_shifted
    loop_boundary
    loop_temporary
    exact_loop_right))
(define-fun refined_loop_called () ExactState
  (RefinedAdapterCallback
    refined_loop_shifted
    loop_boundary
    loop_temporary
    refined_loop_right))
(define-fun exact_loop_child () ExactState
  (ExactInsertTailLoop
    exact_loop_called
    loop_boundary
    loop_begin
    (- loop_sift 1)
    loop_sift
    loop_temporary))
(define-fun refined_loop_child () ExactState
  (RefinedInsertTailLoop
    refined_loop_called
    loop_boundary
    loop_begin
    (- loop_sift 1)
    loop_sift
    loop_temporary))
(define-fun exact_loop_parent () ExactState
  (ExactInsertTailLoop
    loop_state
    loop_boundary
    loop_begin
    loop_sift
    loop_gap
    loop_temporary))
(define-fun refined_loop_parent () ExactState
  (RefinedInsertTailLoop
    loop_state
    loop_boundary
    loop_begin
    loop_sift
    loop_gap
    loop_temporary))
"""
    return (
        declarations,
        LOOP_DOMAIN,
        _state_equalities("exact_loop_child", "refined_loop_child"),
        _state_difference("exact_loop_parent", "refined_loop_parent"),
    )


def _entry_correspondence() -> tuple[str, str, list[str], str]:
    declarations = r"""
(declare-const entry_boundary Boundary)
(declare-const entry_state ExactState)
(declare-const entry_begin Int)
(declare-const entry_tail Int)
(declare-const entry_sequence_len Int)

(define-fun exact_entry_temporary () Int
  (select (e_sequence entry_state) entry_tail))
(define-fun refined_entry_temporary () Int
  (select (e_sequence entry_state) entry_tail))
(define-fun exact_entry_right () Int
  (select (e_sequence entry_state) (- entry_tail 1)))
(define-fun refined_entry_right () Int
  (select (e_sequence entry_state) (- entry_tail 1)))
(define-fun exact_entry_called () ExactState
  (ExactCallback
    entry_state
    entry_boundary
    exact_entry_temporary
    exact_entry_right))
(define-fun refined_entry_called () ExactState
  (RefinedAdapterCallback
    entry_state
    entry_boundary
    refined_entry_temporary
    refined_entry_right))
(define-fun exact_entry_loop () ExactState
  (ExactInsertTailLoop
    exact_entry_called
    entry_boundary
    entry_begin
    (- entry_tail 1)
    entry_tail
    exact_entry_temporary))
(define-fun refined_entry_loop () ExactState
  (RefinedInsertTailLoop
    refined_entry_called
    entry_boundary
    entry_begin
    (- entry_tail 1)
    entry_tail
    refined_entry_temporary))
(define-fun exact_entry_parent () ExactState
  (ExactInsertTail
    entry_state entry_boundary entry_begin entry_tail))
(define-fun refined_entry_parent () ExactState
  (RefinedInsertTail
    entry_state entry_boundary entry_begin entry_tail))
"""
    return (
        declarations,
        ENTRY_DOMAIN,
        _state_equalities("exact_entry_loop", "refined_entry_loop"),
        _state_difference("exact_entry_parent", "refined_entry_parent"),
    )


def correspondence_coverage() -> dict[str, Any]:
    _adapter_text, _adapter_aliases, adapter_equalities = (
        _adapter_components()
    )
    _helper_text, helper_equalities = _helper_correspondence()
    _loop_text, _loop_domain, loop_hypothesis, _loop_difference = (
        _loop_step_correspondence()
    )
    _entry_text, _entry_domain, entry_hypothesis, _entry_difference = (
        _entry_correspondence()
    )
    return {
        "semantic_functions": [
            *ADAPTER_CORE_FUNCTIONS,
            *INSERT_SIGNATURES,
        ],
        "state_fields": list(SMT_FIELD_BINDINGS["InsertTailState"]),
        "boundary_fields": list(
            SMT_FIELD_BINDINGS["KeyOrdDropBoundary"]
        ),
        "adapter_comparison_count": len(adapter_equalities),
        "helper_comparison_count": len(helper_equalities),
        "loop_result_comparison_count": 4,
        "entry_result_comparison_count": 4,
        "induction_hypothesis_comparison_count": (
            len(loop_hypothesis) + len(entry_hypothesis)
        ),
        "comparison_count": (
            len(adapter_equalities)
            + len(helper_equalities)
            + 4
            + 4
            + len(loop_hypothesis)
            + len(entry_hypothesis)
        ),
        "valid_domains": [
            "non-panicked, non-aborted; 0 <= begin <= sift; "
            "gap == sift + 1; gap < sequence_len",
            "non-panicked, non-aborted; "
            "0 <= begin < tail < sequence_len",
        ],
        "proof_rule": (
            "field-complete well-founded induction on sift - begin, "
            "followed by entry-point lifting"
        ),
    }


def correspondence_query_text(proof_text: str | None = None) -> str:
    if proof_text is None:
        proof_text = PROOF_PATH.read_text()
    derived = _derive_all_smt(proof_text)
    adapter_text, adapter_aliases, adapter_equalities = (
        _adapter_components()
    )
    helper_text, helper_equalities = _helper_correspondence()
    loop_text, loop_domain, loop_hypothesis, loop_difference = (
        _loop_step_correspondence()
    )
    entry_text, entry_domain, entry_hypothesis, entry_difference = (
        _entry_correspondence()
    )
    helper_conjunction = "\n      ".join(
        [*adapter_equalities, *helper_equalities]
    )
    loop_hypothesis_text = "\n          ".join(loop_hypothesis)
    entry_hypothesis_text = "\n      ".join(entry_hypothesis)
    return (
        accepted_smt._prefix()
        + "\n"
        + (
            "; Refined definitions below are mechanically translated from\n"
            "; the parsed Verus expression AST, not copied from accepted SMT.\n"
            f"; Verus source SHA-256: {derived['source_sha256']}\n"
            "; ExactInsertTailLoop correspondence is the arbitrary-valid-domain\n"
            "; induction step; ExactInsertTail is lifted with that hypothesis.\n"
        )
        + "\n".join(derived["definitions"])
        + adapter_text
        + "\n".join(adapter_aliases)
        + helper_text
        + loop_text
        + entry_text
        + """
(assert
  (or
    (not
      (and
      """
        + helper_conjunction
        + """))
    (and
      """
        + loop_domain
        + "\n      (=> (> loop_sift loop_begin)\n"
        + "        (and\n          "
        + loop_hypothesis_text
        + "))"
        + "\n      "
        + loop_difference
        + """)
    (and
      """
        + entry_domain
        + "\n      "
        + entry_hypothesis_text
        + "\n      "
        + entry_difference
        + """)))
(check-sat)
"""
    )


def validate_correspondence_query(text: str) -> None:
    actual_domain_sha256 = {
        "loop": digest_bytes(LOOP_DOMAIN.encode()),
        "entry": digest_bytes(ENTRY_DOMAIN.encode()),
    }
    if actual_domain_sha256 != EXPECTED_DOMAIN_SHA256:
        raise ValueError("correspondence valid-domain predicate changed")
    for label, domain in (
        ("loop", LOOP_DOMAIN),
        ("entry", ENTRY_DOMAIN),
    ):
        if text.count(domain) != 1:
            raise ValueError(
                f"correspondence query does not bind exact {label} domain"
            )
    for name, refined in REFINED_FUNCTION_NAMES.items():
        form = (
            "(define-fun-rec "
            if name in RECURSIVE_FUNCTIONS
            else "(define-fun "
        )
        if text.count(f"{form}{refined} ") != 1:
            raise ValueError(
                f"correspondence query does not derive {refined} once"
            )
    for accepted in (
        "AdapterTransition",
        "ExactCallback",
        "ExactInsertTailLoop",
        "ExactInsertTail",
    ):
        if accepted not in text:
            raise ValueError(
                f"correspondence query omits accepted semantic {accepted}"
            )
    for marker in (
        "(<= 0 loop_begin)",
        "(<= loop_begin loop_sift)",
        "(= loop_gap (+ loop_sift 1))",
        "(< loop_gap loop_sequence_len)",
        "(=> (> loop_sift loop_begin)",
        "(<= 0 entry_begin)",
        "(< entry_begin entry_tail)",
        "(< entry_tail entry_sequence_len)",
        "exact_loop_child",
        "refined_loop_child",
        "exact_entry_loop",
        "refined_entry_loop",
    ):
        if marker not in text:
            raise ValueError(
                f"correspondence query omits induction/domain marker {marker}"
            )
    for field in SMT_FIELD_BINDINGS["InsertTailState"]:
        for left, right in (
            ("exact_loop_parent", "refined_loop_parent"),
            ("exact_entry_parent", "refined_entry_parent"),
        ):
            equality = (
                f"(not (= ({field} {left}) ({field} {right})))"
            )
            if text.count(equality) != 1:
                raise ValueError(
                    f"correspondence query does not compare {field} once"
                )
    if text.count("(assert") != 1 or text.count("(check-sat)") != 1:
        raise ValueError("correspondence query shape changed")
    if "(get-model)" in text:
        raise ValueError("UNSAT correspondence query requests a model")
    if "mechanically translated" not in text:
        raise ValueError("correspondence query lacks AST derivation marker")


def accepted_adapter_binding() -> dict[str, Any]:
    binding = copy.deepcopy(adapter_model.accepted_smt_binding())
    accepted_text = ACCEPTED_ADAPTER_PROOF_PATH.read_text()
    binding.update(
        {
            "accepted_proof_sha256": digest_bytes(
                accepted_text.encode()
            ),
            "verus_struct_fields": {
                name: list(
                    adapter_model._verus_struct_fields(
                        accepted_text, name
                    )
                )
                for name in (
                    "OwnedKey",
                    "AdapterFrame",
                    "KeyOrdDropBoundary",
                )
            },
            "core_semantic_functions": list(ADAPTER_CORE_FUNCTIONS),
        }
    )
    return binding


def accepted_smt_binding() -> dict[str, Any]:
    text = accepted_smt._prefix()
    boundary_fields = adapter_model._smt_datatype_fields(text, "Boundary")
    exact_fields = adapter_model._smt_datatype_fields(text, "ExactState")
    if boundary_fields != SMT_FIELD_BINDINGS["KeyOrdDropBoundary"]:
        raise ValueError("accepted Boundary fields changed")
    if exact_fields != SMT_FIELD_BINDINGS["InsertTailState"]:
        raise ValueError("accepted ExactState fields changed")
    boundary_sorts = adapter_model._smt_datatype_field_sorts(
        text, "Boundary"
    )
    exact_sorts = adapter_model._smt_datatype_field_sorts(
        text, "ExactState"
    )
    if boundary_sorts != SMT_FIELD_SORTS["Boundary"]:
        raise ValueError("accepted Boundary field sorts changed")
    if exact_sorts != SMT_FIELD_SORTS["ExactState"]:
        raise ValueError("accepted ExactState field sorts changed")
    exact_loop = adapter_model._extract_smt_form(
        text, "(define-fun-rec ExactInsertTailLoop"
    )
    exact_entry = adapter_model._extract_smt_definition(
        text, "ExactInsertTail"
    )
    loop_fragments = (
        "(store (e_sequence q) gap (select (e_sequence q) sift))",
        "(ite (e_aborted called) (e_sequence called)",
        "(ExactCallback shifted b temporary right)",
        "(ExactInsertTailLoop called b begin next_sift sift temporary)",
    )
    entry_fragments = (
        "(select (e_sequence q) tail)",
        "(ExactCallback q b temporary right)",
        "(ExactInsertTailLoop called b begin (- tail 1) tail temporary)",
    )
    for definition, fragments, label in (
        (exact_loop, loop_fragments, "ExactInsertTailLoop"),
        (exact_entry, entry_fragments, "ExactInsertTail"),
    ):
        normalized = adapter_model._normalize(definition)
        for fragment in fragments:
            if adapter_model._normalize(fragment) not in normalized:
                raise ValueError(
                    f"{label}: retained abort-aware semantics changed"
                )
    return {
        "exact_source_sha256": digest_path(ACCEPTED_SMT_PATH),
        "exact_definitions_sha256": digest_bytes(
            exact_smt.definitions_text().encode()
        ),
        "prefix_sha256": digest_bytes(text.encode()),
        "datatype_fields": {
            "Boundary": list(boundary_fields),
            "ExactState": list(exact_fields),
        },
        "datatype_sorts": {
            "Boundary": [
                {"field": field, "sort": sort}
                for field, sort in boundary_sorts
            ],
            "ExactState": [
                {"field": field, "sort": sort}
                for field, sort in exact_sorts
            ],
        },
        "definitions": {
            "ExactInsertTailLoop": {
                "sha256": digest_bytes(exact_loop.encode()),
                "kind": "recursive",
            },
            "ExactInsertTail": {
                "sha256": digest_bytes(exact_entry.encode()),
                "kind": "entry",
            },
        },
    }


def validate_proof(text: str | None = None) -> dict[str, Any]:
    if text is None:
        text = PROOF_PATH.read_text()
    for token in ("external_body", "assume(", "admit("):
        if token in text:
            raise ValueError(f"Verus proof contains forbidden token {token!r}")
    if re.search(r"\baxiom\b", text):
        raise ValueError("Verus proof contains forbidden token 'axiom'")
    for token in (
        "ExactState",
        "ExactInsertTail",
        "selected_output",
        "final_state",
        "answer_encoding",
        "trace_input",
        "terminal_result",
    ):
        if token in text:
            raise ValueError(
                f"Verus proof accepts or names forbidden input {token!r}"
            )
    actual_functions = tuple(
        re.findall(r"pub open spec fn ([a-z][a-z0-9_]*)\s*\(", text)
    )
    if actual_functions != ALL_OPEN_SPEC_FUNCTIONS:
        raise ValueError(
            f"Verus semantic function set changed: {actual_functions!r}"
        )
    struct_fields = {
        name: adapter_model._verus_struct_fields(text, name)
        for name in SMT_FIELD_BINDINGS
    }
    if struct_fields != SMT_FIELD_BINDINGS:
        raise ValueError(f"Verus state fields changed: {struct_fields!r}")
    field_types = {
        name: adapter_model._verus_struct_field_types(text, name)
        for name in VERUS_STRUCT_FIELD_TYPES
    }
    if field_types != VERUS_STRUCT_FIELD_TYPES:
        raise ValueError(f"Verus state field types changed: {field_types!r}")

    required_fragments = {
        "callback_frame": (
            "adapter_transition(\n"
            "        boundary,\n"
            "        state.e_callback_state,\n"
            "        left,\n"
            "        right,",
        ),
        "adapter_callback": (
            "e_callback_state: frame.af_state,",
            "e_panicked: frame.af_termination != 0,",
            "e_aborted: frame.af_termination == 2,",
        ),
        "target_adapter_is_less": (
            "callback_frame(state, boundary, left, right).af_is_less",
        ),
        "shifted_state": (
            "state.e_sequence.update(\n"
            "            gap,\n"
            "            state.e_sequence[sift],",
            "e_aborted: false,",
        ),
        "restored_state": (
            "if state.e_aborted {",
            "state.e_sequence.update(destination, temporary)",
            "e_callback_state: state.e_callback_state,",
            "e_panicked: panicked,",
        ),
        "valid_insert_tail_input": (
            "!state.e_panicked\n"
            "        && !state.e_aborted\n"
            "        && 0 <= begin\n"
            "        && begin < tail\n"
            "        && tail < state.e_sequence.len()",
        ),
        "valid_insert_tail_loop_input": (
            "!state.e_panicked\n"
            "        && !state.e_aborted\n"
            "        && 0 <= begin\n"
            "        && begin <= sift\n"
            "        && gap == sift + 1\n"
            "        && gap < state.e_sequence.len()",
        ),
        "insert_tail_loop": (
            "let shifted = shifted_state(state, sift, gap);",
            "restored_state(shifted, sift, temporary, false)",
            "let called = adapter_callback(",
            "let less = target_adapter_is_less(",
            "restored_state(called, sift, temporary, true)",
            "next_sift,\n"
            "                    sift,\n"
            "                    temporary,",
            "restored_state(called, sift, temporary, false)",
        ),
        "insert_tail": (
            "let temporary = state.e_sequence[tail];",
            "let right = state.e_sequence[tail - 1];",
            "let called = adapter_callback(",
            "let less = target_adapter_is_less(",
            "begin,\n"
            "                tail - 1,\n"
            "                tail,\n"
            "                temporary,",
        ),
    }
    for name, fragments in required_fragments.items():
        item = insert_analogue._extract_spec_item(text, name)
        for fragment in fragments:
            if fragment not in item:
                raise ValueError(
                    f"{name}: source-sensitive fragment changed: {fragment}"
                )
    guard_sha256 = {
        name: digest_bytes(
            insert_analogue._extract_spec_item(text, name).encode()
        )
        for name in PINNED_GUARD_FUNCTIONS
    }
    if guard_sha256 != EXPECTED_GUARD_SHA256:
        raise ValueError("fail-closed guard function body changed")

    adapter_derived = _derive_adapter_smt(text)
    primitive_functions = ADAPTER_CORE_FUNCTIONS[:-1]
    accepted_adapter_derived = _derive_adapter_smt(
        ACCEPTED_ADAPTER_PROOF_PATH.read_text(),
        primitive_functions,
    )
    local_adapter_primitives = _derive_adapter_smt(
        text,
        primitive_functions,
    )
    if (
        local_adapter_primitives["definitions"]
        != accepted_adapter_derived["definitions"]
    ):
        raise ValueError(
            "accepted adapter AST correspondence changed"
        )
    insertion_derived = _derive_insert_smt(text)
    proof_items = {
        name: adapter_model._extract_verus_item(text, "proof fn", name)
        for name in REQUIRED_PROOFS
    }
    actual_proofs = tuple(
        re.findall(r"pub proof fn ([a-z][a-z0-9_]*)\s*\(", text)
    )
    if actual_proofs != REQUIRED_PROOFS:
        raise ValueError(
            f"Verus proof obligation set changed: {actual_proofs!r}"
        )
    return {
        "proof_sha256": digest_bytes(text.encode()),
        "trusted_free": True,
        "precomputed_terminal_or_answer_input": False,
        "top_level_inputs": [
            "accepted KeyOrdDropBoundary",
            "pre-call InsertTailState containing source identities",
            "valid begin index",
            "valid tail index",
        ],
        "struct_fields": {
            name: list(fields) for name, fields in struct_fields.items()
        },
        "struct_field_types": {
            name: [
                {"field": field, "type": field_type}
                for field, field_type in fields
            ]
            for name, fields in field_types.items()
        },
        "adapter_bridge": {
            "derivation": "parsed-verus-expression-ast-to-smt",
            "accepted_proof_sha256": digest_path(
                ACCEPTED_ADAPTER_PROOF_PATH
            ),
            "functions": adapter_derived["functions"],
        },
        "semantic_bridge": {
            "derivation": "parsed-verus-expression-ast-to-smt",
            "source_sha256": insertion_derived["source_sha256"],
            "functions": insertion_derived["functions"],
        },
        "proof_obligations": {
            name: digest_bytes(item.encode())
            for name, item in proof_items.items()
        },
        "proof_count": len(proof_items),
        "source_order": list(SOURCE_ORDER),
        "fail_closed_guard_functions": list(PINNED_GUARD_FUNCTIONS),
        "fail_closed_guard_sha256": guard_sha256,
    }


def mutate_proof(kind: str, text: str | None = None) -> str:
    if kind not in _MUTATIONS:
        raise ValueError(f"unknown target-079 v3 mutation: {kind}")
    if text is None:
        text = PROOF_PATH.read_text()
    function, replacements = _MUTATIONS[kind]
    marker = f"pub open spec fn {function}("
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"{kind}: mutation function is missing")
    body_start = text.find("{", start)
    end = adapter_model._matching_delimiter(
        text, body_start, "{", "}"
    ) + 1
    item = text[start:end]
    for old, new, expected_count in replacements:
        actual_count = item.count(old)
        if actual_count != expected_count:
            raise ValueError(
                f"{kind}: expected {expected_count} anchors, "
                f"found {actual_count}"
            )
        item = item.replace(old, new)
    return text[:start] + item + text[end:]


def _witness_header(proof_text: str) -> str:
    derived = _derive_all_smt(proof_text)
    return (
        accepted_smt._prefix()
        + "\n; Refined definitions mechanically translated from Verus AST.\n"
        + "\n".join(derived["definitions"])
        + "\n"
    )


def _witness_state_equalities() -> str:
    return "\n  ".join(
        _state_equalities("witness_exact_run", "witness_refined_run")
    )


def _transition_constraints(
    state: int,
    left: int,
    right: int,
    *,
    next_state: int,
    termination: int,
    less: bool,
) -> str:
    frame = (
        f"(AdapterTransition witness_boundary {state} {left} {right})"
    )
    less_text = "true" if less else "false"
    return "\n".join(
        (
            f"(assert (= (af_state {frame}) {next_state}))",
            f"(assert (= (af_termination {frame}) {termination}))",
            f"(assert (= (af_is_less {frame}) {less_text}))",
        )
    )


def witness_query_text(
    kind: str,
    proof_text: str | None = None,
) -> str:
    if kind not in WITNESS_KINDS:
        raise ValueError(f"unknown target-079 v3 witness: {kind}")
    if proof_text is None:
        proof_text = PROOF_PATH.read_text()
    header = _witness_header(proof_text)
    equality = _witness_state_equalities()
    if kind == "no-shift":
        constraints = _transition_constraints(
            0, 20, 10, next_state=1, termination=0, less=False
        )
        body = f"""
(declare-const witness_boundary Boundary)
(declare-const witness_sequence (Array Int Int))
(define-fun witness_state () ExactState
  (mkExactState witness_sequence 0 false false))
(assert (= (select witness_sequence 0) 10))
(assert (= (select witness_sequence 1) 20))
{constraints}
(define-fun witness_exact_run () ExactState
  (ExactInsertTail witness_state witness_boundary 0 1))
(define-fun witness_refined_run () ExactState
  (RefinedInsertTail witness_state witness_boundary 0 1))
(assert (and
  {equality}
  (= (e_sequence witness_exact_run) witness_sequence)
  (= (e_callback_state witness_exact_run) 1)
  (not (e_panicked witness_exact_run))
  (not (e_aborted witness_exact_run))))
(check-sat)
(get-model)
"""
    elif kind == "multi-shift":
        constraints = "\n".join(
            (
                _transition_constraints(
                    0, 5, 30, next_state=1, termination=0, less=True
                ),
                _transition_constraints(
                    1, 5, 20, next_state=2, termination=0, less=True
                ),
                _transition_constraints(
                    2, 5, 10, next_state=3, termination=0, less=False
                ),
            )
        )
        body = f"""
(declare-const witness_boundary Boundary)
(declare-const witness_sequence (Array Int Int))
(define-fun witness_state () ExactState
  (mkExactState witness_sequence 0 false false))
(assert (= (select witness_sequence 0) 10))
(assert (= (select witness_sequence 1) 20))
(assert (= (select witness_sequence 2) 30))
(assert (= (select witness_sequence 3) 5))
{constraints}
(define-fun witness_exact_run () ExactState
  (ExactInsertTail witness_state witness_boundary 0 3))
(define-fun witness_refined_run () ExactState
  (RefinedInsertTail witness_state witness_boundary 0 3))
(assert (and
  {equality}
  (= (select (e_sequence witness_exact_run) 0) 10)
  (= (select (e_sequence witness_exact_run) 1) 5)
  (= (select (e_sequence witness_exact_run) 2) 20)
  (= (select (e_sequence witness_exact_run) 3) 30)
  (= (e_callback_state witness_exact_run) 3)
  (not (e_panicked witness_exact_run))
  (not (e_aborted witness_exact_run))))
(check-sat)
(get-model)
"""
    elif kind == "ordinary-panic-after-shift":
        constraints = "\n".join(
            (
                _transition_constraints(
                    0, 5, 20, next_state=1, termination=0, less=True
                ),
                _transition_constraints(
                    1, 5, 10, next_state=7, termination=1, less=False
                ),
            )
        )
        body = f"""
(declare-const witness_boundary Boundary)
(declare-const witness_sequence (Array Int Int))
(define-fun witness_state () ExactState
  (mkExactState witness_sequence 0 false false))
(assert (= (select witness_sequence 0) 10))
(assert (= (select witness_sequence 1) 20))
(assert (= (select witness_sequence 2) 5))
{constraints}
(define-fun witness_exact_run () ExactState
  (ExactInsertTail witness_state witness_boundary 0 2))
(define-fun witness_refined_run () ExactState
  (RefinedInsertTail witness_state witness_boundary 0 2))
(assert (and
  {equality}
  (= (select (e_sequence witness_exact_run) 0) 10)
  (= (select (e_sequence witness_exact_run) 1) 5)
  (= (select (e_sequence witness_exact_run) 2) 20)
  (= (e_callback_state witness_exact_run) 7)
  (e_panicked witness_exact_run)
  (not (e_aborted witness_exact_run))))
(check-sat)
(get-model)
"""
    else:
        constraints = "\n".join(
            (
                _transition_constraints(
                    0, 5, 20, next_state=1, termination=0, less=True
                ),
                _transition_constraints(
                    1, 5, 10, next_state=9, termination=2, less=False
                ),
            )
        )
        body = f"""
(declare-const witness_boundary Boundary)
(declare-const witness_sequence (Array Int Int))
(define-fun witness_state () ExactState
  (mkExactState witness_sequence 0 false false))
(assert (= (select witness_sequence 0) 10))
(assert (= (select witness_sequence 1) 20))
(assert (= (select witness_sequence 2) 5))
{constraints}
(define-fun witness_exact_run () ExactState
  (ExactInsertTail witness_state witness_boundary 0 2))
(define-fun witness_refined_run () ExactState
  (RefinedInsertTail witness_state witness_boundary 0 2))
(assert (and
  {equality}
  (= (select (e_sequence witness_exact_run) 0) 10)
  (= (select (e_sequence witness_exact_run) 1) 20)
  (= (select (e_sequence witness_exact_run) 2) 20)
  (= (e_callback_state witness_exact_run) 9)
  (e_panicked witness_exact_run)
  (e_aborted witness_exact_run)))
(check-sat)
(get-model)
"""
    return header + body


def validate_witness_query(kind: str, text: str) -> None:
    if kind not in WITNESS_KINDS:
        raise ValueError(f"unknown target-079 v3 witness: {kind}")
    if text.count("(check-sat)") != 1 or text.count("(get-model)") != 1:
        raise ValueError(f"{kind}: witness query must retain one model")
    if "ExactInsertTail" not in text or "RefinedInsertTail" not in text:
        raise ValueError(f"{kind}: witness does not exercise both entries")
    for field in SMT_FIELD_BINDINGS["InsertTailState"]:
        equality = (
            f"(= ({field} witness_exact_run) "
            f"({field} witness_refined_run))"
        )
        if equality not in text:
            raise ValueError(f"{kind}: witness omits {field} equality")
    required = {
        "no-shift": (
            "(ExactInsertTail witness_state witness_boundary 0 1)",
            "(= (e_sequence witness_exact_run) witness_sequence)",
            "(not (e_aborted witness_exact_run))",
        ),
        "multi-shift": (
            "(ExactInsertTail witness_state witness_boundary 0 3)",
            "(= (select (e_sequence witness_exact_run) 1) 5)",
            "(= (select (e_sequence witness_exact_run) 3) 30)",
        ),
        "ordinary-panic-after-shift": (
            "(ExactInsertTail witness_state witness_boundary 0 2)",
            "(= (af_termination (AdapterTransition "
            "witness_boundary 1 5 10)) 1)",
            "(= (e_callback_state witness_exact_run) 7)",
            "(not (e_aborted witness_exact_run))",
        ),
        "abort-after-shift": (
            "(ExactInsertTail witness_state witness_boundary 0 2)",
            "(= (af_termination (AdapterTransition "
            "witness_boundary 1 5 10)) 2)",
            "(= (select (e_sequence witness_exact_run) 1) 20)",
            "(= (select (e_sequence witness_exact_run) 2) 20)",
            "(e_aborted witness_exact_run)",
        ),
    }
    for marker in required[kind]:
        if marker not in text:
            raise ValueError(f"{kind}: witness marker missing: {marker}")


def binding_manifest() -> dict[str, Any]:
    proof = validate_proof()
    accepted_exact = accepted_smt_binding()
    accepted_adapter = accepted_adapter_binding()
    adapter_coverage = adapter_correspondence_coverage()
    coverage = correspondence_coverage()
    return {
        "schema_version": 1,
        "artifact_id": "target_079_insert_tail_refinement_v3",
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "source_binding": {
            "insert_tail_and_copy_on_drop": {
                "path": SOURCE_PATH.relative_to(ROOT).as_posix(),
                "sha256": digest_path(SOURCE_PATH),
                "source_reference": (
                    "Rust 1.96 smallsort.rs CopyOnDrop and insert_tail"
                ),
            },
            "accepted_adapter_proof": {
                "path": ACCEPTED_ADAPTER_PROOF_PATH.relative_to(
                    ROOT
                ).as_posix(),
                "sha256": digest_path(ACCEPTED_ADAPTER_PROOF_PATH),
            },
            "accepted_exact_smt": {
                "path": ACCEPTED_SMT_PATH.relative_to(ROOT).as_posix(),
                "sha256": digest_path(ACCEPTED_SMT_PATH),
            },
            "accepted_operational_result": {
                "path": ACCEPTED_RESULT_PATH.relative_to(ROOT).as_posix(),
                "sha256": digest_path(ACCEPTED_RESULT_PATH),
            },
            "accepted_adapter_result": {
                "path": ACCEPTED_ADAPTER_RESULT_PATH.relative_to(
                    ROOT
                ).as_posix(),
                "sha256": digest_path(ACCEPTED_ADAPTER_RESULT_PATH),
            },
            "accepted_boundary_manifest": {
                "path": ACCEPTED_BOUNDARY_PATH.relative_to(ROOT).as_posix(),
                "sha256": digest_path(ACCEPTED_BOUNDARY_PATH),
            },
        },
        "field_bindings": {
            "KeyOrdDropBoundary_to_Boundary": {
                field: field
                for field in SMT_FIELD_BINDINGS["KeyOrdDropBoundary"]
            },
            "InsertTailState_to_ExactState": {
                field: field
                for field in SMT_FIELD_BINDINGS["InsertTailState"]
            },
        },
        "function_bindings": {
            "adapter_transition": "AdapterTransition",
            "adapter_callback": "ExactCallback",
            "insert_tail_loop": "ExactInsertTailLoop",
            "insert_tail": "ExactInsertTail",
        },
        "adapter_correspondence": {
            "derivation": "parsed-verus-expression-ast-to-smt",
            **adapter_coverage,
        },
        "mechanical_correspondence": {
            "derivation": "parsed-verus-expression-ast-to-smt",
            "proof_rule": coverage["proof_rule"],
            "semantic_functions": coverage["semantic_functions"],
            "refined_functions": REFINED_FUNCTION_NAMES,
            "comparison_count": coverage["comparison_count"],
            "state_fields": coverage["state_fields"],
            "boundary_fields": coverage["boundary_fields"],
            "valid_domains": coverage["valid_domains"],
            "valid_domain_sha256": EXPECTED_DOMAIN_SHA256,
            "source_sensitive_mutations": list(MUTATION_KINDS),
            "verus_insensitive_mutations": sorted(
                VERUS_INSENSITIVE_MUTATIONS
            ),
            "verus_insensitivity_reason": (
                VERUS_INSENSITIVITY_REASON
            ),
        },
        "verus": proof,
        "accepted_adapter": accepted_adapter,
        "accepted_smt": accepted_exact,
        "classification_effect": (
            "none; this additive package refines the accepted adapter, "
            "insert_tail, and CopyOnDrop without replacing operational-v1"
        ),
        "stage_transition": "disabled",
    }


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_id": "target_079_insert_tail_refinement_v3",
        "target": TARGET,
        "boundary_source": (
            "accepted target-079 KeyOrdDropBoundary and adapter_transition"
        ),
        "transition_inputs": [
            "accepted KeyOrdDropBoundary",
            "pre-call sequence of source identities",
            "pre-call callback state",
            "valid begin and tail indices",
        ],
        "consumed_boundary_maps": [
            "key results, next states, and panic outcomes",
            "Ord::lt results, next states, and panic outcomes",
            "owned-key Drop next states and panic outcomes",
        ],
        "source_derived_not_boundary": [
            "every adapter lifecycle frame",
            "initial comparison before moving the tail",
            "Less-gated shift source and destination",
            "gap movement",
            "normal and ordinary-panic restoration",
            "callback-state update before panic propagation",
            "abort discrimination from adapter termination",
            "abort-time CopyOnDrop cleanup bypass",
            "final sequence, callback state, panic, and abort fields",
        ],
        "excluded": [
            "precomputed adapter frame",
            "precomputed callback result",
            "precomputed loop result or terminal result",
            "selected output or final state",
            "answer encoding",
            "execution trace",
        ],
        "narrower_than_target": True,
        "arbitrary_valid_range": True,
        "reason": (
            "only genuine key, Ord, and Drop observations are trusted; "
            "the adapter lifecycle and every insert_tail/CopyOnDrop "
            "transition are AST-derived"
        ),
        "accepted_boundary_sha256": digest_path(ACCEPTED_BOUNDARY_PATH),
        "accepted_adapter_sha256": digest_path(
            ACCEPTED_ADAPTER_PROOF_PATH
        ),
    }
