#!/usr/bin/env python3
"""Constructive Verus/SMT binding for the target-078 comparator adapter."""

from __future__ import annotations

import re
from hashlib import sha256
from pathlib import Path
from typing import Any

import target_078_exact_smt_v1 as exact_smt
import target_078_operational_smt_v1 as accepted_smt
import target_078_operational_v1 as accepted_model
import target_079_adapter_refinement_v2 as verus_ast


ROOT = Path(__file__).resolve().parents[1]
TARGET = accepted_model.TARGET
INPUT_ORDER = accepted_model.INPUT_ORDER
MODEL_ID = "target-078-adapter-refinement-v2-rust-1.96"
MODEL_VERSION = 2
PROOF_PATH = (
    ROOT
    / "proofs/078_core_slice_select_nth_unstable_by_adapter_refinement_v2.rs"
)
ACCEPTED_SMT_PATH = ROOT / "tools/target_078_operational_smt_v1.py"
ACCEPTED_EXACT_SMT_PATH = ROOT / "tools/target_078_exact_smt_v1.py"
ACCEPTED_RESULT_PATH = (
    ROOT / "evidence/target_078_operational_v1/result.json"
)
ACCEPTED_BOUNDARY_PATH = (
    ROOT / "evidence/target_078_operational_v1/boundary_manifest.json"
)
SOURCE_BODY_PATH = (
    ROOT
    / "provenance/frozen/implproof/"
    "078_core_slice_select_nth_unstable_by/source_body.json"
)
CANONICAL_SOURCE_PATH = (
    ROOT / "provenance/frozen/rust-1.96/library/core/src/slice/mod.rs"
)

SMT_FUNCTION_BINDINGS = {
    "boundary_ordering": "BoundaryOrdering",
    "boundary_next_state": "BoundaryNextState",
    "boundary_panics": "BoundaryPanics",
    "target_adapter_is_less": "TargetAdapterIsLess",
    "comparator_adapter_transition": (
        "AcceptedComparatorAdapterTransition"
    ),
}
VERUS_SEMANTIC_SIGNATURES = {
    "boundary_ordering": (
        (
            ("boundary", "ComparatorBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "int",
    ),
    "boundary_next_state": (
        (
            ("boundary", "ComparatorBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "int",
    ),
    "boundary_panics": (
        (
            ("boundary", "ComparatorBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "bool",
    ),
    "target_adapter_is_less": (
        (
            ("boundary", "ComparatorBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "bool",
    ),
    "comparator_adapter_transition": (
        (
            ("boundary", "ComparatorBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "ComparatorAdapterFrame",
    ),
}
REFINED_FUNCTION_NAMES = {
    name: "Refined" + "".join(part.title() for part in name.split("_"))
    for name in VERUS_SEMANTIC_SIGNATURES
}
SMT_FIELD_BINDINGS = {
    "ComparatorAdapterFrame": (
        "caf_callback_identity",
        "caf_lookup_state",
        "caf_left_identity",
        "caf_right_identity",
        "caf_ordering",
        "caf_next_state",
        "caf_panicked",
        "caf_returned",
        "caf_is_less",
    ),
    "Boundary": (
        "b_callback_identity",
        "b_initial_state",
        "b_contract_ordering",
        "b_ordering",
        "b_next_state",
        "b_panics",
    ),
}
VERUS_STRUCT_FIELD_TYPES = {
    "ComparatorBoundary": (
        ("b_callback_identity", "int"),
        ("b_initial_state", "int"),
        ("b_contract_ordering", "Map<int, Map<int, int>>"),
        ("b_ordering", "Map<int, Map<int, Map<int, int>>>"),
        ("b_next_state", "Map<int, Map<int, Map<int, int>>>"),
        ("b_panics", "Map<int, Map<int, Map<int, bool>>>"),
    ),
    "ComparatorAdapterFrame": (
        ("caf_callback_identity", "int"),
        ("caf_lookup_state", "int"),
        ("caf_left_identity", "int"),
        ("caf_right_identity", "int"),
        ("caf_ordering", "int"),
        ("caf_next_state", "int"),
        ("caf_panicked", "bool"),
        ("caf_returned", "bool"),
        ("caf_is_less", "bool"),
    ),
}
SMT_FIELD_SORTS = {
    "Boundary": (
        ("b_callback_identity", "Int"),
        ("b_initial_state", "Int"),
        ("b_contract_ordering", "(Array PairKey Int)"),
        ("b_ordering", "(Array CallKey Int)"),
        ("b_next_state", "(Array CallKey Int)"),
        ("b_panics", "(Array CallKey Bool)"),
    ),
}
VERUS_STRUCT_BINDINGS = {
    "ComparatorBoundary": SMT_FIELD_BINDINGS["Boundary"],
    "ComparatorAdapterFrame": SMT_FIELD_BINDINGS[
        "ComparatorAdapterFrame"
    ],
}
REQUIRED_PROOFS = (
    "transition_records_ordered_operands_and_pre_state",
    "callback_next_state_threads_on_normal_return",
    "callback_next_state_threads_before_panic_propagation",
    "panic_flag_matches_boundary_observation",
    "normal_less_returns_true",
    "normal_equal_returns_false",
    "normal_greater_returns_false",
    "panic_suppresses_returned_boolean",
    "normal_boolean_equals_target_adapter_is_less",
    "callback_state_update_is_retained_on_panic",
    "boundary_initial_state_selects_entry_lookup",
)
STEP_ORDER = (
    "lookup ordering at pre-call state and ordered operands",
    "derive callback next state at the same lookup key",
    "derive callback panic at the same lookup key",
    "commit callback next state before panic propagation",
    "expose Ordering::Less only after normal return",
)
MUTATION_KINDS = (
    "operand-reversal",
    "pre-state-lookup",
    "next-state",
    "panic-propagation",
    "normal-path-gating",
    "less-encoding",
)
CORRESPONDENCE_MUTATION_KINDS = (
    "callback-identity-field",
    "ordering-boundary-selector",
    "next-state-boundary-selector",
    "panic-boundary-index",
)

_MUTATIONS = {
    "operand-reversal": (
        "comparator_adapter_transition",
        (
            (
                "boundary, state, left, right",
                "boundary, state, right, left",
                4,
            ),
        ),
    ),
    "pre-state-lookup": (
        "comparator_adapter_transition",
        (
            (
                "boundary, state, left, right",
                "boundary, boundary.b_initial_state, left, right",
                4,
            ),
        ),
    ),
    "next-state": (
        "comparator_adapter_transition",
        (("caf_next_state: next,", "caf_next_state: state,", 1),),
    ),
    "panic-propagation": (
        "comparator_adapter_transition",
        (("caf_panicked: panics,", "caf_panicked: false,", 1),),
    ),
    "normal-path-gating": (
        "comparator_adapter_transition",
        (
            (
                "caf_is_less: returned\n"
                "            && target_adapter_is_less("
                "boundary, state, left, right),",
                "caf_is_less: target_adapter_is_less("
                "boundary, state, left, right),",
                1,
            ),
        ),
    ),
    "less-encoding": (
        "target_adapter_is_less",
        (
            (
                "boundary_ordering(boundary, state, left, right) == -1",
                "boundary_ordering(boundary, state, left, right) == 0",
                1,
            ),
        ),
    ),
}
_CORRESPONDENCE_MUTATIONS = {
    "callback-identity-field": (
        "comparator_adapter_transition",
        (
            (
                "caf_callback_identity: boundary.b_callback_identity,",
                "caf_callback_identity: state,",
                1,
            ),
        ),
    ),
    "ordering-boundary-selector": (
        "boundary_ordering",
        (
            (
                "boundary.b_ordering[state][left][right]",
                "boundary.b_next_state[state][left][right]",
                1,
            ),
        ),
    ),
    "next-state-boundary-selector": (
        "boundary_next_state",
        (
            (
                "boundary.b_next_state[state][left][right]",
                "boundary.b_ordering[state][left][right]",
                1,
            ),
        ),
    ),
    "panic-boundary-index": (
        "boundary_panics",
        (
            (
                "boundary.b_panics[state][left][right]",
                "boundary.b_panics[boundary.b_initial_state][left][right]",
                1,
            ),
        ),
    ),
}

_FRAME_DATATYPE = """\
(declare-datatypes ((ComparatorAdapterFrame 0))
  (((mkComparatorAdapterFrame
      (caf_callback_identity Int)
      (caf_lookup_state Int)
      (caf_left_identity Int)
      (caf_right_identity Int)
      (caf_ordering Int)
      (caf_next_state Int)
      (caf_panicked Bool)
      (caf_returned Bool)
      (caf_is_less Bool)))))"""
_STRUCT_CONSTRUCTORS = {
    "ComparatorAdapterFrame": "mkComparatorAdapterFrame",
}
_BOUNDARY_INDEX_ENCODINGS = {
    "b_contract_ordering": ("mkPairKey", 2),
    "b_ordering": ("mkCallKey", 3),
    "b_next_state": ("mkCallKey", 3),
    "b_panics": ("mkCallKey", 3),
}
_VERUS_TYPE_TO_SMT = {
    "int": "Int",
    "bool": "Bool",
    "ComparatorBoundary": "Boundary",
    "ComparatorAdapterFrame": "ComparatorAdapterFrame",
}
_VERUS_TOKEN = re.compile(
    r"\s*(?:"
    r"(?P<integer>-?[0-9]+)|"
    r"(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)|"
    r"(?P<operator>==|!=|&&|\|\||[!={}\(\)\[\],\.:;])"
    r")"
)


def digest_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def digest_path(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"required target-078 artifact is missing: {path}")
    return digest_bytes(path.read_bytes())


class _ComparatorExpressionParser(verus_ast._VerusExpressionParser):
    def __init__(self, text: str, function: str) -> None:
        self.function = function
        self.tokens: list[str] = []
        position = 0
        while position < len(text):
            match = _VERUS_TOKEN.match(text, position)
            if match is None:
                if text[position:].strip() == "":
                    position = len(text)
                    break
                excerpt = text[position : position + 40]
                raise ValueError(
                    f"{function}: unsupported Verus syntax near {excerpt!r}"
                )
            self.tokens.append(match.group(0).strip())
            position = match.end()
        self.position = 0

    def _parse_primary(self) -> tuple[Any, ...]:
        token = self._take()
        if re.fullmatch(r"-?[0-9]+", token):
            return ("integer", token)
        if token in {"true", "false"}:
            return ("boolean", token)
        if token == "(":
            expression = self._parse_expression()
            self._expect(")")
            return expression
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            raise ValueError(
                f"{self.function}: expected expression, got {token!r}"
            )
        if token in _STRUCT_CONSTRUCTORS and self._peek() == "{":
            return self._parse_struct(token)
        if self._peek() == "(":
            return self._parse_call(token)
        return ("variable", token)


def _translate_verus_expression(expression: tuple[Any, ...]) -> str:
    kind = expression[0]
    if kind in {"integer", "boolean", "variable"}:
        return str(expression[1])
    if kind == "unary":
        if expression[1] != "!":
            raise ValueError(f"unsupported Verus unary operator: {expression}")
        return f"(not {_translate_verus_expression(expression[2])})"
    if kind == "binary":
        operator = expression[1]
        left = _translate_verus_expression(expression[2])
        right = _translate_verus_expression(expression[3])
        if operator == "==":
            return f"(= {left} {right})"
        if operator == "!=":
            return f"(not (= {left} {right}))"
        if operator == "&&":
            return f"(and {left} {right})"
        if operator == "||":
            return f"(or {left} {right})"
        raise ValueError(f"unsupported Verus binary operator: {operator}")
    if kind == "if":
        condition = _translate_verus_expression(expression[1])
        when_true = _translate_verus_expression(expression[2])
        when_false = _translate_verus_expression(expression[3])
        return f"(ite {condition} {when_true} {when_false})"
    if kind == "block":
        result = _translate_verus_expression(expression[2])
        for name, value in reversed(expression[1]):
            translated = _translate_verus_expression(value)
            result = f"(let (({name} {translated})) {result})"
        return result
    if kind == "call":
        name = expression[1]
        if name not in REFINED_FUNCTION_NAMES:
            raise ValueError(f"unbound Verus helper call: {name}")
        arguments = " ".join(
            _translate_verus_expression(argument)
            for argument in expression[2]
        )
        return f"({REFINED_FUNCTION_NAMES[name]} {arguments})"
    if kind == "field":
        base = _translate_verus_expression(expression[1])
        return f"({expression[2]} {base})"
    if kind == "index":
        base, indices = verus_ast._flatten_index(expression)
        if base[0] != "field":
            raise ValueError(f"unsupported Verus map base: {base}")
        field = base[2]
        if field not in _BOUNDARY_INDEX_ENCODINGS:
            raise ValueError(f"unbound Verus map field: {field}")
        constructor, arity = _BOUNDARY_INDEX_ENCODINGS[field]
        if len(indices) != arity:
            raise ValueError(
                f"{field}: expected {arity} map indices, got {len(indices)}"
            )
        owner = _translate_verus_expression(base[1])
        translated_indices = " ".join(
            _translate_verus_expression(index) for index in indices
        )
        key = f"({constructor} {translated_indices})"
        return f"(select ({field} {owner}) {key})"
    if kind == "struct":
        struct = expression[1]
        if struct not in _STRUCT_CONSTRUCTORS:
            raise ValueError(f"unbound Verus struct literal: {struct}")
        actual = dict(expression[2])
        fields = SMT_FIELD_BINDINGS[struct]
        if len(actual) != len(expression[2]) or set(actual) != set(fields):
            raise ValueError(
                f"{struct}: constructor fields changed: "
                f"{tuple(name for name, _ in expression[2])!r}"
            )
        values = " ".join(
            _translate_verus_expression(actual[field])
            for field in fields
        )
        return f"({_STRUCT_CONSTRUCTORS[struct]} {values})"
    raise ValueError(f"unsupported Verus expression: {expression}")


def _derive_verus_smt(text: str) -> dict[str, Any]:
    actual_functions = tuple(
        re.findall(r"pub open spec fn ([a-z][a-z0-9_]*)\s*\(", text)
    )
    expected_functions = tuple(VERUS_SEMANTIC_SIGNATURES)
    if actual_functions != expected_functions:
        raise ValueError(
            "Verus semantic helper set changed: "
            f"{actual_functions!r}"
        )

    definitions: list[str] = []
    functions: dict[str, Any] = {}
    for name, expected_signature in VERUS_SEMANTIC_SIGNATURES.items():
        item = verus_ast._extract_verus_item(
            text, "open spec fn", name
        )
        signature = verus_ast._parse_verus_signature(item, name)
        if signature != expected_signature:
            raise ValueError(
                f"{name}: Verus signature changed: {signature!r}"
            )
        parameters, return_type = signature
        try:
            smt_parameters = tuple(
                (parameter, _VERUS_TYPE_TO_SMT[verus_type])
                for parameter, verus_type in parameters
            )
            smt_return = _VERUS_TYPE_TO_SMT[return_type]
        except KeyError as error:
            raise ValueError(
                f"{name}: unbound Verus type {error.args[0]!r}"
            ) from error

        body = item[item.find("{") :]
        expression = _ComparatorExpressionParser(body, name).parse()
        translated = _translate_verus_expression(expression)
        parameter_text = " ".join(
            f"({parameter} {smt_type})"
            for parameter, smt_type in smt_parameters
        )
        refined_name = REFINED_FUNCTION_NAMES[name]
        definition = (
            f"(define-fun {refined_name} "
            f"({parameter_text}) {smt_return}\n  {translated})"
        )
        definitions.append(definition)
        functions[name] = {
            "refined_smt_function": refined_name,
            "verus_sha256": digest_bytes(item.encode()),
            "derived_smt_sha256": digest_bytes(definition.encode()),
            "parameters": [
                {
                    "name": parameter,
                    "verus_type": verus_type,
                    "smt_sort": smt_type,
                }
                for (parameter, verus_type), (_, smt_type) in zip(
                    parameters, smt_parameters, strict=True
                )
            ],
            "verus_return_type": return_type,
            "smt_return_sort": smt_return,
        }
    return {
        "definitions": definitions,
        "functions": functions,
        "source_sha256": digest_bytes(text.encode()),
    }


def accepted_smt_binding() -> dict[str, Any]:
    text = accepted_smt._prefix()
    boundary_fields = verus_ast._smt_datatype_fields(text, "Boundary")
    if boundary_fields != SMT_FIELD_BINDINGS["Boundary"]:
        raise ValueError(
            "accepted target-078 Boundary fields changed: "
            f"{boundary_fields!r}"
        )
    boundary_sorts = verus_ast._smt_datatype_field_sorts(
        text, "Boundary"
    )
    if boundary_sorts != SMT_FIELD_SORTS["Boundary"]:
        raise ValueError(
            "accepted target-078 Boundary sorts changed: "
            f"{boundary_sorts!r}"
        )
    helper_definitions = {
        smt_name: verus_ast._extract_smt_definition(text, smt_name)
        for smt_name in tuple(SMT_FUNCTION_BINDINGS.values())[:-1]
    }
    exact_callback = verus_ast._extract_smt_definition(
        text, "ExactCallback"
    )
    required_exact_fragments = (
        "(e_sequence q)",
        "(BoundaryNextState b (e_callback_state q) left right)",
        "(BoundaryPanics b (e_callback_state q) left right)",
    )
    normalized_exact = verus_ast._normalize(exact_callback)
    for fragment in required_exact_fragments:
        if verus_ast._normalize(fragment) not in normalized_exact:
            raise ValueError(
                "accepted ExactCallback selector semantics changed"
            )
    return {
        "operational_source_sha256": digest_path(ACCEPTED_SMT_PATH),
        "exact_source_sha256": digest_path(ACCEPTED_EXACT_SMT_PATH),
        "prefix_sha256": digest_bytes(text.encode()),
        "datatype_fields": {
            "Boundary": list(boundary_fields),
            "ComparatorAdapterFrame": list(
                SMT_FIELD_BINDINGS["ComparatorAdapterFrame"]
            ),
        },
        "datatype_sorts": {
            "Boundary": [
                {"field": field, "sort": sort}
                for field, sort in boundary_sorts
            ],
        },
        "definitions": {
            name: {
                "sha256": digest_bytes(definition.encode()),
                "verus_function": next(
                    verus_name
                    for verus_name, smt_name in (
                        SMT_FUNCTION_BINDINGS.items()
                    )
                    if smt_name == name
                ),
            }
            for name, definition in helper_definitions.items()
        },
        "exact_callback": {
            "sha256": digest_bytes(exact_callback.encode()),
            "compared_selectors": ["e_callback_state", "e_panicked"],
        },
    }


def validate_proof(text: str | None = None) -> dict[str, Any]:
    if text is None:
        text = PROOF_PATH.read_text()
    for token in ("external_body", "assume(", "admit(", "axiom"):
        if token in text:
            raise ValueError(f"Verus proof contains forbidden token {token!r}")
    for token in (
        "ExactCallback",
        "ExactState",
        "ExactOperationalResult",
        "PrincipalReturn",
        "FinalState",
        "selected_output",
        "final_state",
        "trace_input",
    ):
        if token in text:
            raise ValueError(
                f"Verus proof accepts or names forbidden input {token!r}"
            )

    struct_fields = {
        name: verus_ast._verus_struct_fields(text, name)
        for name in VERUS_STRUCT_BINDINGS
    }
    if struct_fields != VERUS_STRUCT_BINDINGS:
        raise ValueError(
            "Verus constructor/field mapping changed: "
            f"{struct_fields!r}"
        )
    struct_field_types = {
        name: verus_ast._verus_struct_field_types(text, name)
        for name in VERUS_STRUCT_FIELD_TYPES
    }
    if struct_field_types != VERUS_STRUCT_FIELD_TYPES:
        raise ValueError(
            "Verus constructor field types changed: "
            f"{struct_field_types!r}"
        )
    derived_smt = _derive_verus_smt(text)

    items = {
        name: verus_ast._extract_verus_item(
            text, "open spec fn", name
        )
        for name in VERUS_SEMANTIC_SIGNATURES
    }
    transition_header = verus_ast._normalize(
        items["comparator_adapter_transition"]
    ).split("-> ComparatorAdapterFrame", 1)[0].strip()
    expected_header = verus_ast._normalize(
        """\
pub open spec fn comparator_adapter_transition(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)"""
    )
    if transition_header != expected_header:
        raise ValueError(
            "adapter transition must take only boundary, state, left, right"
        )

    required_transition_fragments = (
        "let ordering = boundary_ordering("
        "boundary, state, left, right);",
        "let next = boundary_next_state("
        "boundary, state, left, right);",
        "let panics = boundary_panics("
        "boundary, state, left, right);",
        "let returned = !panics;",
        "caf_lookup_state: state,",
        "caf_left_identity: left,",
        "caf_right_identity: right,",
        "caf_next_state: next,",
        "caf_panicked: panics,",
        "caf_returned: returned,",
        "caf_is_less: returned && target_adapter_is_less("
        "boundary, state, left, right),",
    )
    normalized_transition = verus_ast._normalize(
        items["comparator_adapter_transition"]
    )
    for fragment in required_transition_fragments:
        if verus_ast._normalize(fragment) not in normalized_transition:
            raise ValueError(
                "adapter transition source semantics changed: "
                f"{fragment}"
            )

    proof_items = {
        name: verus_ast._extract_verus_item(text, "proof fn", name)
        for name in REQUIRED_PROOFS
    }
    actual_proofs = tuple(
        re.findall(r"pub proof fn ([a-z][a-z0-9_]*)\s*\(", text)
    )
    if actual_proofs != REQUIRED_PROOFS:
        raise ValueError(
            "Verus proof obligation set changed: "
            f"{actual_proofs!r}"
        )
    return {
        "proof_sha256": digest_bytes(text.encode()),
        "trusted_free": True,
        "precomputed_terminal_input": False,
        "top_level_inputs": [
            "boundary",
            "pre_call_callback_state",
            "left_identity",
            "right_identity",
        ],
        "struct_fields": {
            name: list(fields) for name, fields in struct_fields.items()
        },
        "struct_field_types": {
            name: [
                {"field": field, "type": field_type}
                for field, field_type in fields
            ]
            for name, fields in struct_field_types.items()
        },
        "proof_obligations": {
            name: digest_bytes(item.encode())
            for name, item in proof_items.items()
        },
        "proof_count": len(proof_items),
        "step_order": list(STEP_ORDER),
        "semantic_bridge": {
            "derivation": "parsed-verus-expression-ast-to-smt",
            "source_sha256": derived_smt["source_sha256"],
            "functions": derived_smt["functions"],
        },
    }


def mutate_proof(kind: str, text: str | None = None) -> str:
    mutations = {**_MUTATIONS, **_CORRESPONDENCE_MUTATIONS}
    if kind not in mutations:
        raise ValueError(f"unknown target-078 v2 mutation: {kind}")
    if text is None:
        text = PROOF_PATH.read_text()
    function, replacements = mutations[kind]
    marker = f"pub open spec fn {function}"
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"{kind}: mutation function is missing")
    body_start = text.find("{", start)
    end = verus_ast._matching_delimiter(
        text, body_start, "{", "}"
    ) + 1
    item = text[start:end]
    for old, new, expected_count in replacements:
        actual_count = item.count(old)
        if actual_count != expected_count:
            raise ValueError(
                f"{kind}: expected {expected_count} mutation anchors, "
                f"found {actual_count}"
            )
        item = item.replace(old, new)
    return text[:start] + item + text[end:]


def _correspondence_arguments() -> dict[str, tuple[str, ...]]:
    boundary = "correspondence_boundary"
    state = "(e_callback_state correspondence_exact_state)"
    left = "correspondence_left"
    right = "correspondence_right"
    return {
        name: (boundary, state, left, right)
        for name in VERUS_SEMANTIC_SIGNATURES
    }


def _accepted_correspondence_expressions() -> dict[str, str]:
    boundary = "correspondence_boundary"
    exact_state = "correspondence_exact_state"
    state = f"(e_callback_state {exact_state})"
    left = "correspondence_left"
    right = "correspondence_right"
    exact_callback = (
        f"(ExactCallback {exact_state} {boundary} {left} {right})"
    )
    ordering = f"(BoundaryOrdering {boundary} {state} {left} {right})"
    panics = f"(BoundaryPanics {boundary} {state} {left} {right})"
    target_less = (
        f"(TargetAdapterIsLess {boundary} {state} {left} {right})"
    )
    frame = (
        f"(mkComparatorAdapterFrame "
        f"(b_callback_identity {boundary}) "
        f"{state} {left} {right} {ordering} "
        f"(e_callback_state {exact_callback}) "
        f"(e_panicked {exact_callback}) "
        f"(not {panics}) "
        f"(and (not {panics}) {target_less}))"
    )
    return {
        "boundary_ordering": ordering,
        "boundary_next_state": (
            f"(BoundaryNextState {boundary} {state} {left} {right})"
        ),
        "boundary_panics": panics,
        "target_adapter_is_less": target_less,
        "comparator_adapter_transition": frame,
    }


def _correspondence_alias(name: str, side: str) -> str:
    if name == "comparator_adapter_transition":
        return (
            "accepted_frame" if side == "accepted" else "refined_frame"
        )
    return f"{side}_{name}"


def _correspondence_equalities() -> list[str]:
    equalities: list[str] = []
    for name, (_parameters, return_type) in (
        VERUS_SEMANTIC_SIGNATURES.items()
    ):
        accepted = _correspondence_alias(name, "accepted")
        refined = _correspondence_alias(name, "refined")
        if return_type == "ComparatorAdapterFrame":
            equalities.extend(
                f"(= ({field} {accepted}) ({field} {refined}))"
                for field in SMT_FIELD_BINDINGS[
                    "ComparatorAdapterFrame"
                ]
            )
        else:
            equalities.append(f"(= {accepted} {refined})")
    return equalities


def _exact_callback_equalities() -> list[str]:
    state = "(e_callback_state correspondence_exact_state)"
    callback = (
        "(ExactCallback correspondence_exact_state "
        "correspondence_boundary correspondence_left "
        "correspondence_right)"
    )
    target_less = (
        "(TargetAdapterIsLess correspondence_boundary "
        f"{state} correspondence_left correspondence_right)"
    )
    return [
        "(= (caf_next_state refined_frame) "
        f"(e_callback_state {callback}))",
        "(= (caf_panicked refined_frame) "
        f"(e_panicked {callback}))",
        "(=> (not (caf_panicked refined_frame)) "
        f"(= (caf_is_less refined_frame) {target_less}))",
        "(=> (caf_panicked refined_frame) "
        "(and (not (caf_returned refined_frame)) "
        "(not (caf_is_less refined_frame))))",
    ]


def correspondence_coverage() -> dict[str, Any]:
    frame_fields = list(SMT_FIELD_BINDINGS["ComparatorAdapterFrame"])
    return {
        "semantic_functions": list(VERUS_SEMANTIC_SIGNATURES),
        "constructor_field_comparisons": {
            "ComparatorAdapterFrame": frame_fields,
        },
        "helper_and_field_comparison_count": len(
            _correspondence_equalities()
        ),
        "exact_callback_comparison_count": len(
            _exact_callback_equalities()
        ),
        "comparison_count": (
            len(_correspondence_equalities())
            + len(_exact_callback_equalities())
        ),
    }


def correspondence_query_text(proof_text: str | None = None) -> str:
    if proof_text is None:
        proof_text = PROOF_PATH.read_text()
    derived = _derive_verus_smt(proof_text)
    arguments = _correspondence_arguments()
    accepted_expressions = _accepted_correspondence_expressions()
    aliases: list[str] = []
    for name, (_parameters, return_type) in (
        VERUS_SEMANTIC_SIGNATURES.items()
    ):
        smt_return = _VERUS_TYPE_TO_SMT[return_type]
        accepted_alias = _correspondence_alias(name, "accepted")
        refined_alias = _correspondence_alias(name, "refined")
        refined_arguments = " ".join(arguments[name])
        aliases.extend(
            (
                f"(define-fun {accepted_alias} () {smt_return}\n"
                f"  {accepted_expressions[name]})",
                f"(define-fun {refined_alias} () {smt_return}\n"
                f"  ({REFINED_FUNCTION_NAMES[name]} "
                f"{refined_arguments}))",
            )
        )
    equalities = "\n      ".join(
        [*_correspondence_equalities(), *_exact_callback_equalities()]
    )
    return (
        accepted_smt._prefix()
        + "\n"
        + _FRAME_DATATYPE
        + "\n\n"
        + (
            "; Refined definitions below are mechanically translated from\n"
            "; the parsed Verus expression AST, not copied from accepted SMT.\n"
            f"; Verus source SHA-256: {derived['source_sha256']}\n"
        )
        + "\n".join(derived["definitions"])
        + """\

(declare-const correspondence_boundary Boundary)
(declare-const correspondence_exact_state ExactState)
(declare-const correspondence_left Int)
(declare-const correspondence_right Int)
"""
        + "\n".join(aliases)
        + """
(assert
  (not
    (and
      """
        + equalities
        + """)))
(check-sat)
"""
    )


def validate_correspondence_query(text: str) -> None:
    for equality in [
        *_correspondence_equalities(),
        *_exact_callback_equalities(),
    ]:
        if text.count(equality) != 1:
            raise ValueError(
                "correspondence query does not compare exactly once: "
                f"{equality}"
            )
    for refined in REFINED_FUNCTION_NAMES.values():
        if text.count(f"(define-fun {refined} ") != 1:
            raise ValueError(
                f"correspondence query does not derive {refined} once"
            )
    for accepted in (
        "BoundaryOrdering",
        "BoundaryNextState",
        "BoundaryPanics",
        "TargetAdapterIsLess",
        "ExactCallback",
    ):
        if accepted not in text:
            raise ValueError(
                f"correspondence query omits accepted semantic {accepted}"
            )
    if text.count("(assert") != 1 or text.count("(check-sat)") != 1:
        raise ValueError("correspondence query shape changed")
    if "(get-model)" in text:
        raise ValueError("UNSAT correspondence query requests a model")
    if "mechanically translated" not in text:
        raise ValueError("correspondence query lacks Verus derivation marker")


def binding_manifest() -> dict[str, Any]:
    proof = validate_proof()
    smt = accepted_smt_binding()
    coverage = correspondence_coverage()
    return {
        "schema_version": 1,
        "artifact_id": "target_078_adapter_refinement_v2",
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "source_adapter": (
            "|a: &T, b: &T| compare(a, b) == Ordering::Less"
        ),
        "source_order": list(STEP_ORDER),
        "field_bindings": {
            "ComparatorAdapterFrame": {
                name: name
                for name in SMT_FIELD_BINDINGS[
                    "ComparatorAdapterFrame"
                ]
            },
            "ComparatorBoundary_to_Boundary": {
                name: name for name in SMT_FIELD_BINDINGS["Boundary"]
            },
        },
        "function_bindings": SMT_FUNCTION_BINDINGS,
        "mechanical_correspondence": {
            "derivation": "parsed-verus-expression-ast-to-smt",
            "semantic_functions": coverage["semantic_functions"],
            "refined_functions": REFINED_FUNCTION_NAMES,
            "comparison_count": coverage["comparison_count"],
            "constructor_field_comparisons": coverage[
                "constructor_field_comparisons"
            ],
            "exact_callback_selectors": [
                "e_callback_state",
                "e_panicked",
            ],
            "source_sensitive_mutations": list(
                CORRESPONDENCE_MUTATION_KINDS
            ),
        },
        "verus": proof,
        "accepted_smt": smt,
        "source_binding": {
            "source_body": {
                "path": SOURCE_BODY_PATH.relative_to(ROOT).as_posix(),
                "sha256": digest_path(SOURCE_BODY_PATH),
                "source_reference": "core/src/slice/mod.rs:3581-3590",
            },
            "canonical_source": {
                "path": CANONICAL_SOURCE_PATH.relative_to(ROOT).as_posix(),
                "sha256": digest_path(CANONICAL_SOURCE_PATH),
                "adapter_span": "3581-3590",
            },
            "accepted_operational_result": {
                "path": ACCEPTED_RESULT_PATH.relative_to(ROOT).as_posix(),
                "sha256": digest_path(ACCEPTED_RESULT_PATH),
            },
            "accepted_boundary_manifest": {
                "path": ACCEPTED_BOUNDARY_PATH.relative_to(ROOT).as_posix(),
                "sha256": digest_path(ACCEPTED_BOUNDARY_PATH),
            },
        },
        "classification_effect": (
            "none; this package closes the constructive comparator-adapter "
            "refinement and replays, but does not replace, operational-v1"
        ),
        "stage_transition": "disabled",
    }


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_id": "target_078_adapter_refinement_v2",
        "target": TARGET,
        "boundary_source": (
            "accepted target_078_operational_v1 ComparatorBoundary"
        ),
        "transition_inputs": [
            "shared ComparatorBoundary",
            "pre-call callback-visible state",
            "ordered left source identity",
            "ordered right source identity",
        ],
        "consumed_boundary_maps": [
            "Ordering result at pre-call state and ordered operands",
            "callback next-state at the same lookup key",
            "callback panic at the same lookup key",
        ],
        "source_derived_not_boundary": [
            "operand order",
            "boundary lookup key",
            "callback-state update before panic propagation",
            "normal versus panic completion",
            "Ordering::Less conversion",
            "suppression of the returned boolean on panic",
        ],
        "excluded": [
            "realized calls or invocation count",
            "precomputed adapter transition or callback result",
            "selection branch, pivot, mutation, or execution trace",
            "principal return or final selection state",
            "selected output, final state, or trace input",
        ],
        "narrower_than_target": True,
        "reason": (
            "the boundary fixes only genuine comparator result/state/panic "
            "observations; the adapter transition and all target outcomes "
            "remain source-derived"
        ),
        "accepted_boundary_sha256": digest_path(ACCEPTED_BOUNDARY_PATH),
    }
