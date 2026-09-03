#!/usr/bin/env python3
"""Constructive Verus/SMT binding for the target-079 adapter lifecycle."""

from __future__ import annotations

import re
from hashlib import sha256
from pathlib import Path
from typing import Any

import target_079_operational_smt_v1 as accepted_smt
import target_079_operational_v1 as accepted_model


ROOT = Path(__file__).resolve().parents[1]
TARGET = accepted_model.TARGET
INPUT_ORDER = accepted_model.INPUT_ORDER
MODEL_ID = "target-079-adapter-refinement-v2-rust-1.96"
MODEL_VERSION = 2
PROOF_PATH = (
    ROOT
    / "proofs/079_core_slice_select_nth_unstable_by_key_adapter_refinement_v2.rs"
)
ACCEPTED_SMT_PATH = ROOT / "tools/target_079_operational_smt_v1.py"
ACCEPTED_RESULT_PATH = (
    ROOT / "evidence/target_079_operational_v1/result.json"
)
ACCEPTED_BOUNDARY_PATH = (
    ROOT / "evidence/target_079_operational_v1/boundary_manifest.json"
)
SOURCE_BODY_PATH = (
    ROOT
    / "provenance/frozen/implproof/"
    "079_core_slice_select_nth_unstable_by_key/source_body.json"
)

SMT_FUNCTION_BINDINGS = {
    "adapter_initial": "AdapterInitial",
    "adapter_key_left": "AdapterKeyLeft",
    "adapter_key_right": "AdapterKeyRight",
    "adapter_ord_lt": "AdapterOrdLt",
    "adapter_drop_right": "AdapterDropRight",
    "adapter_drop_left": "AdapterDropLeft",
    "adapter_transition": "AdapterTransition",
}
VERUS_SEMANTIC_SIGNATURES = {
    "key_result": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("value", "int"),
        ),
        "int",
    ),
    "key_next_state": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("value", "int"),
        ),
        "int",
    ),
    "key_panics": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("value", "int"),
        ),
        "bool",
    ),
    "ord_lt_result": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "OwnedKey"),
            ("right", "OwnedKey"),
        ),
        "bool",
    ),
    "ord_lt_next_state": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "OwnedKey"),
            ("right", "OwnedKey"),
        ),
        "int",
    ),
    "ord_lt_panics": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "OwnedKey"),
            ("right", "OwnedKey"),
        ),
        "bool",
    ),
    "drop_next_state": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("key", "OwnedKey"),
        ),
        "int",
    ),
    "drop_panics": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("key", "OwnedKey"),
        ),
        "bool",
    ),
    "owned_key": (
        (
            ("creation_state", "int"),
            ("slot", "int"),
            ("source_identity", "int"),
            ("key_identity", "int"),
        ),
        "OwnedKey",
    ),
    "adapter_initial": ((("state", "int"),), "AdapterFrame"),
    "adapter_key_left": (
        (
            ("frame", "AdapterFrame"),
            ("boundary", "KeyOrdDropBoundary"),
            ("left", "int"),
        ),
        "AdapterFrame",
    ),
    "adapter_key_right": (
        (
            ("frame", "AdapterFrame"),
            ("boundary", "KeyOrdDropBoundary"),
            ("right", "int"),
        ),
        "AdapterFrame",
    ),
    "adapter_ord_lt": (
        (
            ("frame", "AdapterFrame"),
            ("boundary", "KeyOrdDropBoundary"),
        ),
        "AdapterFrame",
    ),
    "adapter_drop_right": (
        (
            ("frame", "AdapterFrame"),
            ("boundary", "KeyOrdDropBoundary"),
        ),
        "AdapterFrame",
    ),
    "adapter_drop_left": (
        (
            ("frame", "AdapterFrame"),
            ("boundary", "KeyOrdDropBoundary"),
        ),
        "AdapterFrame",
    ),
    "frame_after_key_left": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
        ),
        "AdapterFrame",
    ),
    "frame_after_key_right": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "AdapterFrame",
    ),
    "frame_after_ord_lt": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "AdapterFrame",
    ),
    "frame_after_drop_right": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "AdapterFrame",
    ),
    "adapter_transition": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "AdapterFrame",
    ),
    "left_state": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
        ),
        "int",
    ),
    "left_owned": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
        ),
        "OwnedKey",
    ),
    "right_state": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "int",
    ),
    "right_owned": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "OwnedKey",
    ),
    "ord_state": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "int",
    ),
    "right_drop_state": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "int",
    ),
    "left_drop_state": (
        (
            ("boundary", "KeyOrdDropBoundary"),
            ("state", "int"),
            ("left", "int"),
            ("right", "int"),
        ),
        "int",
    ),
}
REFINED_FUNCTION_NAMES = {
    name: "Refined" + "".join(part.title() for part in name.split("_"))
    for name in VERUS_SEMANTIC_SIGNATURES
}
SMT_FIELD_BINDINGS = {
    "OwnedKey": (
        "owned_creation_state",
        "owned_slot",
        "owned_source_identity",
        "owned_key_identity",
    ),
    "AdapterFrame": (
        "af_state",
        "af_termination",
        "af_is_less",
        "af_panic_origin",
        "af_left_owned",
        "af_right_owned",
        "af_left_live",
        "af_right_live",
    ),
    "Boundary": (
        "b_callback_identity",
        "b_key_function_identity",
        "b_ord_function_identity",
        "b_drop_function_identity",
        "b_initial_state",
        "b_contract_key",
        "b_contract_ordering",
        "b_key_result",
        "b_key_next_state",
        "b_key_panics",
        "b_ord_lt_result",
        "b_ord_lt_next_state",
        "b_ord_lt_panics",
        "b_drop_next_state",
        "b_drop_panics",
    ),
}
VERUS_STRUCT_FIELD_TYPES = {
    "OwnedKey": (
        ("owned_creation_state", "int"),
        ("owned_slot", "int"),
        ("owned_source_identity", "int"),
        ("owned_key_identity", "int"),
    ),
    "AdapterFrame": (
        ("af_state", "int"),
        ("af_termination", "int"),
        ("af_is_less", "bool"),
        ("af_panic_origin", "int"),
        ("af_left_owned", "OwnedKey"),
        ("af_right_owned", "OwnedKey"),
        ("af_left_live", "bool"),
        ("af_right_live", "bool"),
    ),
    "KeyOrdDropBoundary": (
        ("b_callback_identity", "int"),
        ("b_key_function_identity", "int"),
        ("b_ord_function_identity", "int"),
        ("b_drop_function_identity", "int"),
        ("b_initial_state", "int"),
        ("b_contract_key", "Map<int, int>"),
        ("b_contract_ordering", "Map<int, Map<int, int>>"),
        ("b_key_result", "Map<int, Map<int, int>>"),
        ("b_key_next_state", "Map<int, Map<int, int>>"),
        ("b_key_panics", "Map<int, Map<int, bool>>"),
        (
            "b_ord_lt_result",
            "Map<int, Map<OwnedKey, Map<OwnedKey, bool>>>",
        ),
        (
            "b_ord_lt_next_state",
            "Map<int, Map<OwnedKey, Map<OwnedKey, int>>>",
        ),
        (
            "b_ord_lt_panics",
            "Map<int, Map<OwnedKey, Map<OwnedKey, bool>>>",
        ),
        ("b_drop_next_state", "Map<int, Map<OwnedKey, int>>"),
        ("b_drop_panics", "Map<int, Map<OwnedKey, bool>>"),
    ),
}
SMT_FIELD_SORTS = {
    "OwnedKey": (
        ("owned_creation_state", "Int"),
        ("owned_slot", "Int"),
        ("owned_source_identity", "Int"),
        ("owned_key_identity", "Int"),
    ),
    "AdapterFrame": (
        ("af_state", "Int"),
        ("af_termination", "Int"),
        ("af_is_less", "Bool"),
        ("af_panic_origin", "Int"),
        ("af_left_owned", "OwnedKey"),
        ("af_right_owned", "OwnedKey"),
        ("af_left_live", "Bool"),
        ("af_right_live", "Bool"),
    ),
    "Boundary": (
        ("b_callback_identity", "Int"),
        ("b_key_function_identity", "Int"),
        ("b_ord_function_identity", "Int"),
        ("b_drop_function_identity", "Int"),
        ("b_initial_state", "Int"),
        ("b_contract_key", "(Array Int Int)"),
        ("b_contract_ordering", "(Array PairKey Int)"),
        ("b_key_result", "(Array KeyCall Int)"),
        ("b_key_next_state", "(Array KeyCall Int)"),
        ("b_key_panics", "(Array KeyCall Bool)"),
        ("b_ord_lt_result", "(Array OrdCall Bool)"),
        ("b_ord_lt_next_state", "(Array OrdCall Int)"),
        ("b_ord_lt_panics", "(Array OrdCall Bool)"),
        ("b_drop_next_state", "(Array DropCall Int)"),
        ("b_drop_panics", "(Array DropCall Bool)"),
    ),
}
VERUS_STRUCT_BINDINGS = {
    "OwnedKey": SMT_FIELD_BINDINGS["OwnedKey"],
    "AdapterFrame": SMT_FIELD_BINDINGS["AdapterFrame"],
    "KeyOrdDropBoundary": SMT_FIELD_BINDINGS["Boundary"],
}
STEP_ORDER = (
    "adapter_key_left",
    "adapter_key_right",
    "adapter_ord_lt",
    "adapter_drop_right",
    "adapter_drop_left",
)
REQUIRED_PROOFS = (
    "transition_is_the_smt_constructor_chain",
    "owned_key_identity_tracks_creation_slot_and_source",
    "normal_execution_threads_all_callback_states",
    "first_key_panic_stops_before_owned_cleanup",
    "second_key_panic_cleans_up_only_left",
    "second_key_panic_and_left_destructor_panic_aborts",
    "ord_panic_cleans_right_then_left",
    "ord_panic_and_right_destructor_panic_aborts_before_left",
    "ord_panic_and_left_destructor_panic_after_right_cleanup_aborts",
    "normal_right_destructor_panic_unwinds_left",
    "normal_right_and_unwind_left_destructor_panics_abort",
    "normal_left_destructor_panic_is_single_panic",
    "initial_callback_state_is_the_transition_entry",
)
MUTATION_KINDS = (
    "step-order",
    "ownership-slot",
    "next-state",
    "panic-propagation",
    "cleanup-order",
    "panic-abort-distinction",
)
CORRESPONDENCE_MUTATION_KINDS = (
    "right-owned-field",
    "initial-default-field",
    "boundary-helper-field",
)

_MUTATIONS = {
    "step-order": (
        "frame_after_key_right",
        """\
    adapter_key_right(
        frame_after_key_left(boundary, state, left),
        boundary,
        right,
    )""",
        """\
    adapter_key_left(
        adapter_key_right(adapter_initial(state), boundary, right),
        boundary,
        left,
    )""",
    ),
    "ownership-slot": (
        "adapter_key_right",
        "af_right_owned: owned_key(state, 1, right, key),",
        "af_right_owned: owned_key(state, 0, right, key),",
    ),
    "next-state": (
        "adapter_key_left",
        "af_state: next,",
        "af_state: state,",
    ),
    "panic-propagation": (
        "adapter_key_right",
        "af_termination: if panics { 1 } else { 0 },",
        "af_termination: 0,",
    ),
    "cleanup-order": (
        "adapter_transition",
        """\
    adapter_drop_left(
        frame_after_drop_right(boundary, state, left, right),
        boundary,
    )""",
        """\
    adapter_drop_right(
        adapter_drop_left(
            frame_after_ord_lt(boundary, state, left, right),
            boundary,
        ),
        boundary,
    )""",
    ),
    "panic-abort-distinction": (
        "adapter_drop_right",
        "if old_termination == 1 { 2 } else { 1 }",
        "1",
    ),
}
_CORRESPONDENCE_MUTATIONS = {
    "right-owned-field": (
        "adapter_drop_right",
        "af_right_owned: key,",
        "af_right_owned: frame.af_left_owned,",
    ),
    "initial-default-field": (
        "adapter_initial",
        "af_right_owned: owned_key(0, 1, 0, 0),",
        "af_right_owned: owned_key(0, 0, 0, 0),",
    ),
    "boundary-helper-field": (
        "key_result",
        "boundary.b_key_result[state][value]",
        "boundary.b_key_next_state[state][value]",
    ),
}


def digest_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def digest_path(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"required binding input is missing: {path}")
    return digest_bytes(path.read_bytes())


def _matching_delimiter(
    text: str,
    start: int,
    opening: str,
    closing: str,
) -> int:
    depth = 0
    for position in range(start, len(text)):
        character = text[position]
        if character == opening:
            depth += 1
        elif character == closing:
            depth -= 1
            if depth == 0:
                return position
    raise ValueError(f"unterminated {opening}{closing} form")


def _extract_smt_form(text: str, marker: str) -> str:
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"SMT form is missing: {marker}")
    end = _matching_delimiter(text, start, "(", ")")
    return text[start : end + 1]


def _extract_smt_definition(text: str, name: str) -> str:
    return _extract_smt_form(text, f"(define-fun {name}")


def _extract_verus_item(text: str, kind: str, name: str) -> str:
    marker = f"pub {kind} {name}"
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"Verus item is missing: {marker}")
    body_start = text.find("{", start)
    if body_start < 0:
        raise ValueError(f"Verus item has no body: {marker}")
    end = _matching_delimiter(text, body_start, "{", "}")
    return text[start : end + 1]


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _smt_datatype_fields(text: str, datatype: str) -> tuple[str, ...]:
    form = _extract_smt_form(
        text, f"(declare-datatypes (({datatype} 0))"
    )
    fields = tuple(
        match.group(1)
        for match in re.finditer(r"\(([a-z][a-z0-9_]*)\s", form)
    )
    if not fields:
        raise ValueError(f"SMT datatype has no selectors: {datatype}")
    return fields


def _smt_datatype_field_sorts(
    text: str,
    datatype: str,
) -> tuple[tuple[str, str], ...]:
    form = _extract_smt_form(
        text, f"(declare-datatypes (({datatype} 0))"
    )
    fields = _smt_datatype_fields(text, datatype)
    result: list[tuple[str, str]] = []
    for field in fields:
        match = re.search(
            rf"\({re.escape(field)}\s+"
            r"(\([^()]+\)|[A-Za-z][A-Za-z0-9_]*)\)",
            form,
        )
        if match is None:
            raise ValueError(
                f"SMT selector sort is missing: {datatype}.{field}"
            )
        result.append((field, _normalize(match.group(1))))
    return tuple(result)


def _verus_struct_fields(text: str, struct: str) -> tuple[str, ...]:
    item = _extract_verus_item(text, "ghost struct", struct)
    fields = tuple(
        match.group(1)
        for match in re.finditer(r"pub\s+([a-z][a-z0-9_]*):", item)
    )
    if not fields:
        raise ValueError(f"Verus struct has no fields: {struct}")
    return fields


def _verus_struct_field_types(
    text: str,
    struct: str,
) -> tuple[tuple[str, str], ...]:
    item = _extract_verus_item(text, "ghost struct", struct)
    fields: list[tuple[str, str]] = []
    for line in item.splitlines():
        match = re.fullmatch(
            r"\s*pub\s+([a-z][a-z0-9_]*):\s*(.+),\s*",
            line,
        )
        if match is not None:
            fields.append((match.group(1), _normalize(match.group(2))))
    if not fields:
        raise ValueError(f"Verus struct has no typed fields: {struct}")
    return tuple(fields)


_VERUS_TOKEN = re.compile(
    r"\s*(?:"
    r"(?P<integer>[0-9]+)|"
    r"(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)|"
    r"(?P<operator>==|!=|&&|\|\||[!={}\(\)\[\],\.:;])"
    r")"
)
_BINARY_PRECEDENCE = {
    "||": 1,
    "&&": 2,
    "==": 3,
    "!=": 3,
}
_STRUCT_CONSTRUCTORS = {
    "OwnedKey": "mkOwnedKey",
    "AdapterFrame": "mkAdapterFrame",
}
_BOUNDARY_INDEX_ENCODINGS = {
    "b_contract_key": (None, 1),
    "b_contract_ordering": ("mkPairKey", 2),
    "b_key_result": ("mkKeyCall", 2),
    "b_key_next_state": ("mkKeyCall", 2),
    "b_key_panics": ("mkKeyCall", 2),
    "b_ord_lt_result": ("mkOrdCall", 3),
    "b_ord_lt_next_state": ("mkOrdCall", 3),
    "b_ord_lt_panics": ("mkOrdCall", 3),
    "b_drop_next_state": ("mkDropCall", 2),
    "b_drop_panics": ("mkDropCall", 2),
}
_VERUS_TYPE_TO_SMT = {
    "int": "Int",
    "bool": "Bool",
    "OwnedKey": "OwnedKey",
    "AdapterFrame": "AdapterFrame",
    "KeyOrdDropBoundary": "Boundary",
}


class _VerusExpressionParser:
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

    def parse(self) -> tuple[Any, ...]:
        expression = self._parse_block()
        if self.position != len(self.tokens):
            raise ValueError(
                f"{self.function}: trailing token {self._peek()!r}"
            )
        return expression

    def _peek(self) -> str | None:
        if self.position == len(self.tokens):
            return None
        return self.tokens[self.position]

    def _take(self) -> str:
        token = self._peek()
        if token is None:
            raise ValueError(f"{self.function}: unexpected end of body")
        self.position += 1
        return token

    def _expect(self, expected: str) -> None:
        actual = self._take()
        if actual != expected:
            raise ValueError(
                f"{self.function}: expected {expected!r}, got {actual!r}"
            )

    def _parse_block(self) -> tuple[Any, ...]:
        self._expect("{")
        bindings: list[tuple[str, tuple[Any, ...]]] = []
        while self._peek() == "let":
            self._take()
            name = self._take()
            if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
                raise ValueError(
                    f"{self.function}: invalid let binding {name!r}"
                )
            self._expect("=")
            value = self._parse_expression()
            self._expect(";")
            bindings.append((name, value))
        result = self._parse_expression()
        self._expect("}")
        return ("block", tuple(bindings), result)

    def _parse_expression(self, minimum: int = 0) -> tuple[Any, ...]:
        if self._peek() == "if":
            left = self._parse_if()
        else:
            left = self._parse_unary()
        while True:
            operator = self._peek()
            precedence = _BINARY_PRECEDENCE.get(operator or "", -1)
            if precedence < minimum:
                break
            self._take()
            right = self._parse_expression(precedence + 1)
            left = ("binary", operator, left, right)
        return left

    def _parse_if(self) -> tuple[Any, ...]:
        self._expect("if")
        condition = self._parse_expression()
        when_true = self._parse_block()
        self._expect("else")
        when_false = (
            self._parse_if()
            if self._peek() == "if"
            else self._parse_block()
        )
        return ("if", condition, when_true, when_false)

    def _parse_unary(self) -> tuple[Any, ...]:
        if self._peek() == "!":
            self._take()
            return ("unary", "!", self._parse_unary())
        return self._parse_postfix()

    def _parse_postfix(self) -> tuple[Any, ...]:
        expression = self._parse_primary()
        while True:
            if self._peek() == ".":
                self._take()
                expression = ("field", expression, self._take())
            elif self._peek() == "[":
                self._take()
                index = self._parse_expression()
                self._expect("]")
                expression = ("index", expression, index)
            else:
                return expression

    def _parse_primary(self) -> tuple[Any, ...]:
        token = self._take()
        if token.isdigit():
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

    def _parse_call(self, name: str) -> tuple[Any, ...]:
        self._expect("(")
        arguments: list[tuple[Any, ...]] = []
        while self._peek() != ")":
            arguments.append(self._parse_expression())
            if self._peek() != ",":
                break
            self._take()
            if self._peek() == ")":
                break
        self._expect(")")
        return ("call", name, tuple(arguments))

    def _parse_struct(self, name: str) -> tuple[Any, ...]:
        self._expect("{")
        fields: list[tuple[str, tuple[Any, ...]]] = []
        while self._peek() != "}":
            field = self._take()
            self._expect(":")
            fields.append((field, self._parse_expression()))
            if self._peek() != ",":
                break
            self._take()
        self._expect("}")
        return ("struct", name, tuple(fields))


def _parse_verus_signature(
    item: str,
    name: str,
) -> tuple[tuple[tuple[str, str], ...], str]:
    body_start = item.find("{")
    header = _normalize(item[:body_start])
    match = re.fullmatch(
        rf"pub open spec fn {re.escape(name)}\((.*)\) -> "
        r"([A-Za-z][A-Za-z0-9_]*)",
        header,
    )
    if match is None:
        raise ValueError(f"{name}: unsupported Verus signature {header!r}")
    parameters: list[tuple[str, str]] = []
    parameter_text = match.group(1).strip()
    if parameter_text:
        for parameter in parameter_text.split(","):
            if parameter.strip() == "":
                continue
            pieces = parameter.strip().split(":", 1)
            if len(pieces) != 2:
                raise ValueError(
                    f"{name}: malformed Verus parameter {parameter!r}"
                )
            parameters.append(
                (pieces[0].strip(), _normalize(pieces[1]))
            )
    return tuple(parameters), match.group(2)


def _flatten_index(
    expression: tuple[Any, ...],
) -> tuple[tuple[Any, ...], tuple[tuple[Any, ...], ...]]:
    indices: list[tuple[Any, ...]] = []
    while expression[0] == "index":
        indices.append(expression[2])
        expression = expression[1]
    indices.reverse()
    return expression, tuple(indices)


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
        base, indices = _flatten_index(expression)
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
        key = (
            translated_indices
            if constructor is None
            else f"({constructor} {translated_indices})"
        )
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
        item = _extract_verus_item(text, "open spec fn", name)
        signature = _parse_verus_signature(item, name)
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

        body_start = item.find("{")
        body = item[body_start:]
        expression = _VerusExpressionParser(body, name).parse()
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
    datatype_fields = {
        name: _smt_datatype_fields(text, name)
        for name in SMT_FIELD_BINDINGS
    }
    if datatype_fields != SMT_FIELD_BINDINGS:
        raise ValueError(
            "accepted SMT constructor/selectors changed: "
            f"{datatype_fields!r}"
        )
    datatype_sorts = {
        name: _smt_datatype_field_sorts(text, name)
        for name in SMT_FIELD_SORTS
    }
    if datatype_sorts != SMT_FIELD_SORTS:
        raise ValueError(
            "accepted SMT selector sorts changed: "
            f"{datatype_sorts!r}"
        )

    definitions = {
        name: _extract_smt_definition(text, name)
        for name in SMT_FUNCTION_BINDINGS.values()
    }
    transition = _normalize(definitions["AdapterTransition"])
    expected_transition = _normalize(
        """\
(define-fun AdapterTransition
  ((b Boundary) (state Int) (left Int) (right Int)) AdapterFrame
  (AdapterDropLeft
    (AdapterDropRight
      (AdapterOrdLt
        (AdapterKeyRight
          (AdapterKeyLeft (AdapterInitial state) b left)
          b
          right)
        b)
      b)
    b))"""
    )
    if transition != expected_transition:
        raise ValueError("accepted SMT AdapterTransition order changed")

    for name, origin in (
        ("AdapterKeyLeft", "1"),
        ("AdapterKeyRight", "2"),
        ("AdapterOrdLt", "3"),
        ("AdapterDropRight", "4"),
        ("AdapterDropLeft", "5"),
    ):
        definition = definitions[name]
        if f"(ite panics {origin} 0)" not in definition and name not in {
            "AdapterDropRight",
            "AdapterDropLeft",
        }:
            raise ValueError(f"{name}: panic-origin constructor changed")
    for name in ("AdapterDropRight", "AdapterDropLeft"):
        definition = definitions[name]
        if "(ite (= old_termination 1) 2 1)" not in _normalize(
            definition
        ):
            raise ValueError(f"{name}: double-panic transition changed")

    return {
        "source_sha256": digest_path(ACCEPTED_SMT_PATH),
        "prefix_sha256": digest_bytes(text.encode()),
        "datatype_fields": {
            name: list(fields)
            for name, fields in datatype_fields.items()
        },
        "datatype_sorts": {
            name: [
                {"field": field, "sort": sort}
                for field, sort in fields
            ]
            for name, fields in datatype_sorts.items()
        },
        "definitions": {
            name: {
                "sha256": digest_bytes(definition.encode()),
                "verus_function": next(
                    verus
                    for verus, smt in SMT_FUNCTION_BINDINGS.items()
                    if smt == name
                ),
            }
            for name, definition in definitions.items()
        },
        "step_order": list(STEP_ORDER),
    }


def validate_proof(text: str | None = None) -> dict[str, Any]:
    if text is None:
        text = PROOF_PATH.read_text()
    for token in ("external_body", "assume(", "admit(", "axiom"):
        if token in text:
            raise ValueError(f"Verus proof contains forbidden token {token!r}")
    if "ExactOperationalResult" in text or "terminal lifecycle" in text:
        raise ValueError("Verus proof accepts a precomputed lifecycle result")

    struct_fields = {
        name: _verus_struct_fields(text, name)
        for name in VERUS_STRUCT_BINDINGS
    }
    if struct_fields != VERUS_STRUCT_BINDINGS:
        raise ValueError(
            "Verus constructor/field mapping changed: "
            f"{struct_fields!r}"
        )
    struct_field_types = {
        name: _verus_struct_field_types(text, name)
        for name in VERUS_STRUCT_FIELD_TYPES
    }
    if struct_field_types != VERUS_STRUCT_FIELD_TYPES:
        raise ValueError(
            "Verus constructor field types changed: "
            f"{struct_field_types!r}"
        )
    derived_smt = _derive_verus_smt(text)

    items = {
        name: _extract_verus_item(text, "open spec fn", name)
        for name in SMT_FUNCTION_BINDINGS
    }
    transition_header = _normalize(items["adapter_transition"]).split(
        "-> AdapterFrame", 1
    )[0].strip()
    expected_arguments = _normalize(
        """\
pub open spec fn adapter_transition(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)"""
    )
    if transition_header != expected_arguments:
        raise ValueError(
            "adapter_transition must take only boundary, state, left, right"
        )

    expected_chain = _normalize(
        """\
adapter_drop_left(
    frame_after_drop_right(boundary, state, left, right),
    boundary,
)"""
    )
    if expected_chain not in _normalize(items["adapter_transition"]):
        raise ValueError("Verus top-level adapter step order changed")

    proof_items = {
        name: _extract_verus_item(text, "proof fn", name)
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

    required_semantics = {
        "adapter_key_left": (
            "owned_key(state, 0, left, key)",
            "af_left_live: !panics",
            "af_right_live: false",
        ),
        "adapter_key_right": (
            "owned_key(state, 1, right, key)",
            "af_left_live: frame.af_left_live",
            "af_right_live: !panics",
        ),
        "adapter_ord_lt": (
            "ord_lt_result(boundary, state, left, right)",
            "ord_lt_next_state(boundary, state, left, right)",
            "ord_lt_panics(boundary, state, left, right)",
        ),
        "adapter_drop_right": (
            "frame.af_right_live && frame.af_termination != 2",
            "if old_termination == 1 { 2 } else { 1 }",
            "af_panic_origin: if panics { 4 }",
        ),
        "adapter_drop_left": (
            "frame.af_left_live && frame.af_termination != 2",
            "if old_termination == 1 { 2 } else { 1 }",
            "af_panic_origin: if panics { 5 }",
        ),
    }
    for name, fragments in required_semantics.items():
        normalized = _normalize(items[name])
        for fragment in fragments:
            if _normalize(fragment) not in normalized:
                raise ValueError(
                    f"{name}: required source semantic is missing: "
                    f"{fragment}"
                )

    return {
        "proof_sha256": digest_bytes(text.encode()),
        "trusted_free": True,
        "precomputed_terminal_input": False,
        "top_level_inputs": [
            "boundary",
            "state",
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
        "functions": {
            name: {
                "smt_function": SMT_FUNCTION_BINDINGS[name],
                "sha256": digest_bytes(item.encode()),
            }
            for name, item in items.items()
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
        raise ValueError(f"unknown target-079 v2 mutation: {kind}")
    if text is None:
        text = PROOF_PATH.read_text()
    function, old, new = mutations[kind]
    marker = f"pub open spec fn {function}"
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"{kind}: mutation function is missing")
    body_start = text.find("{", start)
    end = _matching_delimiter(text, body_start, "{", "}") + 1
    item = text[start:end]
    if item.count(old) != 1:
        raise ValueError(
            f"{kind}: expected one mutation anchor, found "
            f"{item.count(old)}"
        )
    return text[:start] + item.replace(old, new, 1) + text[end:]


def _correspondence_arguments() -> dict[str, tuple[str, ...]]:
    boundary = "correspondence_boundary"
    state = "correspondence_state"
    left = "correspondence_left"
    right = "correspondence_right"
    frame = "correspondence_input_frame"
    owned_left = "correspondence_owned_left"
    owned_right = "correspondence_owned_right"
    slot = "correspondence_slot"
    key = "correspondence_key"
    arguments = {
        "key_result": (boundary, state, left),
        "key_next_state": (boundary, state, left),
        "key_panics": (boundary, state, left),
        "ord_lt_result": (
            boundary,
            state,
            owned_left,
            owned_right,
        ),
        "ord_lt_next_state": (
            boundary,
            state,
            owned_left,
            owned_right,
        ),
        "ord_lt_panics": (
            boundary,
            state,
            owned_left,
            owned_right,
        ),
        "drop_next_state": (boundary, state, owned_right),
        "drop_panics": (boundary, state, owned_right),
        "owned_key": (state, slot, left, key),
        "adapter_initial": (state,),
        "adapter_key_left": (frame, boundary, left),
        "adapter_key_right": (frame, boundary, right),
        "adapter_ord_lt": (frame, boundary),
        "adapter_drop_right": (frame, boundary),
        "adapter_drop_left": (frame, boundary),
        "frame_after_key_left": (boundary, state, left),
        "frame_after_key_right": (boundary, state, left, right),
        "frame_after_ord_lt": (boundary, state, left, right),
        "frame_after_drop_right": (boundary, state, left, right),
        "adapter_transition": (boundary, state, left, right),
        "left_state": (boundary, state, left),
        "left_owned": (boundary, state, left),
        "right_state": (boundary, state, left, right),
        "right_owned": (boundary, state, left, right),
        "ord_state": (boundary, state, left, right),
        "right_drop_state": (boundary, state, left, right),
        "left_drop_state": (boundary, state, left, right),
    }
    if tuple(arguments) != tuple(VERUS_SEMANTIC_SIGNATURES):
        raise ValueError("correspondence arguments do not cover every helper")
    return arguments


def _accepted_correspondence_expressions() -> dict[str, str]:
    boundary = "correspondence_boundary"
    state = "correspondence_state"
    left = "correspondence_left"
    right = "correspondence_right"
    frame = "correspondence_input_frame"
    owned_left = "correspondence_owned_left"
    owned_right = "correspondence_owned_right"
    slot = "correspondence_slot"
    key = "correspondence_key"

    initial = f"(AdapterInitial {state})"
    after_left = f"(AdapterKeyLeft {initial} {boundary} {left})"
    after_right = (
        f"(AdapterKeyRight {after_left} {boundary} {right})"
    )
    after_ord = f"(AdapterOrdLt {after_right} {boundary})"
    after_drop_right = f"(AdapterDropRight {after_ord} {boundary})"

    left_state = f"(KeyNextState {boundary} {state} {left})"
    left_owned = (
        f"(mkOwnedKey {state} 0 {left} "
        f"(KeyResult {boundary} {state} {left}))"
    )
    right_state = (
        f"(KeyNextState {boundary} {left_state} {right})"
    )
    right_owned = (
        f"(mkOwnedKey {left_state} 1 {right} "
        f"(KeyResult {boundary} {left_state} {right}))"
    )
    ord_state = (
        f"(OrdLtNextState {boundary} {right_state} "
        f"{left_owned} {right_owned})"
    )
    right_drop_state = (
        f"(DropNextState {boundary} {ord_state} {right_owned})"
    )
    left_drop_state = (
        f"(DropNextState {boundary} {right_drop_state} {left_owned})"
    )

    expressions = {
        "key_result": f"(KeyResult {boundary} {state} {left})",
        "key_next_state": (
            f"(KeyNextState {boundary} {state} {left})"
        ),
        "key_panics": f"(KeyPanics {boundary} {state} {left})",
        "ord_lt_result": (
            f"(OrdLtResult {boundary} {state} "
            f"{owned_left} {owned_right})"
        ),
        "ord_lt_next_state": (
            f"(OrdLtNextState {boundary} {state} "
            f"{owned_left} {owned_right})"
        ),
        "ord_lt_panics": (
            f"(OrdLtPanics {boundary} {state} "
            f"{owned_left} {owned_right})"
        ),
        "drop_next_state": (
            f"(DropNextState {boundary} {state} {owned_right})"
        ),
        "drop_panics": (
            f"(DropPanics {boundary} {state} {owned_right})"
        ),
        "owned_key": f"(mkOwnedKey {state} {slot} {left} {key})",
        "adapter_initial": initial,
        "adapter_key_left": (
            f"(AdapterKeyLeft {frame} {boundary} {left})"
        ),
        "adapter_key_right": (
            f"(AdapterKeyRight {frame} {boundary} {right})"
        ),
        "adapter_ord_lt": f"(AdapterOrdLt {frame} {boundary})",
        "adapter_drop_right": (
            f"(AdapterDropRight {frame} {boundary})"
        ),
        "adapter_drop_left": (
            f"(AdapterDropLeft {frame} {boundary})"
        ),
        "frame_after_key_left": after_left,
        "frame_after_key_right": after_right,
        "frame_after_ord_lt": after_ord,
        "frame_after_drop_right": after_drop_right,
        "adapter_transition": (
            f"(AdapterTransition {boundary} {state} {left} {right})"
        ),
        "left_state": left_state,
        "left_owned": left_owned,
        "right_state": right_state,
        "right_owned": right_owned,
        "ord_state": ord_state,
        "right_drop_state": right_drop_state,
        "left_drop_state": left_drop_state,
    }
    if tuple(expressions) != tuple(VERUS_SEMANTIC_SIGNATURES):
        raise ValueError("accepted semantics do not cover every Verus helper")
    return expressions


def _correspondence_alias(name: str, side: str) -> str:
    if name == "adapter_transition":
        return "accepted_frame" if side == "accepted" else "refined_frame"
    return f"{side}_{name}"


def _correspondence_equalities() -> list[str]:
    equalities: list[str] = []
    for name, (_, return_type) in VERUS_SEMANTIC_SIGNATURES.items():
        accepted = _correspondence_alias(name, "accepted")
        refined = _correspondence_alias(name, "refined")
        if return_type == "AdapterFrame":
            fields = SMT_FIELD_BINDINGS["AdapterFrame"]
        elif return_type == "OwnedKey":
            fields = SMT_FIELD_BINDINGS["OwnedKey"]
        else:
            fields = ()
        if fields:
            equalities.extend(
                f"(= ({field} {accepted}) ({field} {refined}))"
                for field in fields
            )
        else:
            equalities.append(f"(= {accepted} {refined})")
    return equalities


def correspondence_coverage() -> dict[str, Any]:
    return {
        "semantic_functions": list(VERUS_SEMANTIC_SIGNATURES),
        "comparison_count": len(_correspondence_equalities()),
        "constructor_field_comparisons": {
            "OwnedKey": list(SMT_FIELD_BINDINGS["OwnedKey"]),
            "AdapterFrame": list(SMT_FIELD_BINDINGS["AdapterFrame"]),
        },
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
    equalities = "\n      ".join(_correspondence_equalities())
    return (
        accepted_smt._prefix()
        + "\n"
        + (
            "; Refined definitions below are mechanically translated from\n"
            "; the parsed Verus expression AST, not copied from accepted SMT.\n"
            f"; Verus source SHA-256: {derived['source_sha256']}\n"
        )
        + "\n".join(derived["definitions"])
        + """\

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
    for equality in _correspondence_equalities():
        if text.count(equality) != 1:
            raise ValueError(
                "correspondence query does not compare exactly once: "
                f"{equality}"
            )
    for refined in REFINED_FUNCTION_NAMES.values():
        marker = f"(define-fun {refined} "
        if text.count(marker) != 1:
            raise ValueError(
                f"correspondence query does not derive {refined} once"
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
        "artifact_id": "target_079_adapter_refinement_v2",
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "source_order": [
            "f(left)",
            "f(right)",
            "Ord::lt(&left_key,&right_key)",
            "drop(right_owned_key)",
            "drop(left_owned_key)",
        ],
        "termination_encoding": {
            "0": "normal",
            "1": "panic/unwind",
            "2": "abort",
        },
        "panic_origin_encoding": {
            "0": "none",
            "1": "f(left)",
            "2": "f(right)",
            "3": "Ord::lt",
            "4": "drop(right)",
            "5": "drop(left)",
        },
        "field_bindings": {
            "OwnedKey": {
                name: name for name in SMT_FIELD_BINDINGS["OwnedKey"]
            },
            "AdapterFrame": {
                name: name for name in SMT_FIELD_BINDINGS["AdapterFrame"]
            },
            "KeyOrdDropBoundary_to_Boundary": {
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
            "boundary_map_key_encodings": {
                field: {
                    "key_constructor": constructor,
                    "verus_index_arity": arity,
                }
                for field, (
                    constructor,
                    arity,
                ) in _BOUNDARY_INDEX_ENCODINGS.items()
            },
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
            "none; this proof refines the accepted adapter construction and "
            "replays, but does not replace, the operational-v1 obligations"
        ),
        "stage_transition": "disabled",
    }


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_id": "target_079_adapter_refinement_v2",
        "target": TARGET,
        "boundary_source": (
            "accepted target_079_operational_v1 KeyOrdDropBoundary"
        ),
        "transition_inputs": [
            "shared KeyOrdDropBoundary",
            "current callback-visible state",
            "left source identity",
            "right source identity",
        ],
        "consumed_boundary_maps": [
            "key result, next-state, and panic maps",
            "Ord::lt result, next-state, and panic maps",
            "Drop next-state and panic maps",
        ],
        "source_derived_not_boundary": [
            "five-step evaluation and cleanup order",
            "owned-key creation state and left/right slot",
            "owned-key source and abstract-key identity",
            "temporary liveness",
            "panic origin and unwind status",
            "normal, panic, or abort termination",
            "terminal callback state",
        ],
        "excluded": [
            "realized calls or invocation count",
            "temporary lifetime or drop schedule",
            "selection branch, pivot, mutation, or trace",
            "principal return or final selection state",
            "precomputed adapter result or lifecycle trace",
        ],
        "narrower_than_target": True,
        "reason": (
            "the boundary fixes only total callback/Ord/Drop observations; "
            "the adapter transition and target result remain derived"
        ),
        "accepted_boundary_sha256": digest_path(ACCEPTED_BOUNDARY_PATH),
    }
