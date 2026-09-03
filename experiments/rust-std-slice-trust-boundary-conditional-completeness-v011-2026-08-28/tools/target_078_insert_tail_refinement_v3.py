#!/usr/bin/env python3
"""Mechanical Verus/SMT binding for target-078 insert_tail refinement v3."""

from __future__ import annotations

import re
from hashlib import sha256
from pathlib import Path
from typing import Any

import target_078_exact_smt_v1 as exact_smt
import target_078_operational_smt_v1 as accepted_smt
import target_078_operational_v1 as accepted_model
import target_079_adapter_refinement_v2 as verus_syntax


ROOT = Path(__file__).resolve().parents[1]
TARGET = accepted_model.TARGET
INPUT_ORDER = accepted_model.INPUT_ORDER
MODEL_ID = "target-078-insert-tail-refinement-v3-rust-1.96"
MODEL_VERSION = 3
PROOF_PATH = (
    ROOT
    / "proofs/"
    "078_core_slice_select_nth_unstable_by_insert_tail_refinement_v3.rs"
)
ACCEPTED_SMT_PATH = ROOT / "tools/target_078_exact_smt_v1.py"
ACCEPTED_RESULT_PATH = (
    ROOT / "evidence/target_078_operational_v1/result.json"
)
ACCEPTED_BOUNDARY_PATH = (
    ROOT / "evidence/target_078_operational_v1/boundary_manifest.json"
)
SOURCE_PATH = (
    ROOT / "evidence/target_078_operational_v1/bound_inputs/smallsort.rs"
)
PRESERVATION_V1_PATH = ROOT / "preservation/path_policy_v1.json"

SMT_FIELD_BINDINGS = {
    "ComparatorBoundary": (
        "b_callback_identity",
        "b_initial_state",
        "b_contract_ordering",
        "b_ordering",
        "b_next_state",
        "b_panics",
    ),
    "InsertTailState": (
        "e_sequence",
        "e_callback_state",
        "e_panicked",
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
    "InsertTailState": (
        ("e_sequence", "Seq<int>"),
        ("e_callback_state", "int"),
        ("e_panicked", "bool"),
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
    "ExactState": (
        ("e_sequence", "(Array Int Int)"),
        ("e_callback_state", "Int"),
        ("e_panicked", "Bool"),
    ),
}

ALL_OPEN_SPEC_FUNCTIONS = (
    "boundary_ordering",
    "boundary_next_state",
    "boundary_panics",
    "target_adapter_is_less",
    "comparator_callback",
    "shifted_state",
    "restored_state",
    "restored_sequence",
    "valid_insert_tail_input",
    "valid_insert_tail_loop_input",
    "insert_tail_loop",
    "insert_tail",
    "panic_state_is_boundary_observed",
)
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
    "comparator_callback": (
        (
            ("state", "InsertTailState"),
            ("boundary", "ComparatorBoundary"),
            ("left", "int"),
            ("right", "int"),
        ),
        "InsertTailState",
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
            ("boundary", "ComparatorBoundary"),
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
            ("boundary", "ComparatorBoundary"),
            ("begin", "int"),
            ("tail", "int"),
        ),
        "InsertTailState",
    ),
}
REFINED_FUNCTION_NAMES = {
    name: "Refined" + "".join(part.title() for part in name.split("_"))
    for name in VERUS_SEMANTIC_SIGNATURES
}
RECURSIVE_FUNCTIONS = {"insert_tail_loop"}
REQUIRED_PROOFS = (
    "callback_uses_ordered_operands_and_pre_state",
    "initial_comparison_panic_is_exact",
    "no_shift_path_is_exact",
    "initial_less_enters_loop_with_tail_gap",
    "loop_at_begin_restores_temporary",
    "loop_normal_stop_restores_temporary",
    "loop_panic_restores_gap_and_retains_callback_state",
    "loop_less_advances_sift_and_gap",
    "shift_then_restore_preserves_identity_multiplicity",
    "insert_tail_loop_preserves_restored_sequence_properties",
    "insert_tail_preserves_length_multiplicity_and_frame",
    "insert_tail_loop_retains_callback_state_on_panic",
    "insert_tail_retains_callback_state_on_panic",
)
PINNED_GUARD_FUNCTIONS = (
    "restored_sequence",
    "valid_insert_tail_input",
    "valid_insert_tail_loop_input",
    "panic_state_is_boundary_observed",
)
EXPECTED_GUARD_SHA256 = {
    "restored_sequence": (
        "92c8b141ba87d58ee1a2dad0bb1a7ba2a192ffbd786c35304f773b2a18a1b173"
    ),
    "valid_insert_tail_input": (
        "3a0e939a2a6359f0ef55432ffc76c2f94c394bf69c39e0c4be249914439ba879"
    ),
    "valid_insert_tail_loop_input": (
        "2ea889331ed405727623a6dfcb775d233b943129bd4c66d2500a44d5bf8e34f4"
    ),
    "panic_state_is_boundary_observed": (
        "ab1064811248025840e03ad5b05cbd2dc6c9dea3726ce4d0558e13be61e7b827"
    ),
}
SOURCE_ORDER = (
    "initial comparison before moving the tail identity",
    "move sift into the current gap",
    "advance the guard destination to sift",
    "decrement sift before the next comparison",
    "lookup callback observations at the current pre-call state",
    "commit callback next state before panic propagation",
    "restore the temporary identity at the current gap on stop or panic",
)
MUTATION_KINDS = (
    "operand-order",
    "lookup-state",
    "shift-source",
    "shift-destination",
    "gap-advancement",
    "normal-restoration",
    "base-restoration",
    "panic-restoration",
    "callback-next-state",
    "panic-propagation",
)
WITNESS_KINDS = (
    "no-shift",
    "multi-shift",
    "insert-at-begin",
    "panic-after-shift",
)

_MUTATIONS = {
    "operand-order": (
        "comparator_callback",
        (
            (
                "state.e_callback_state,\n"
                "            left,\n"
                "            right,",
                "state.e_callback_state,\n"
                "            right,\n"
                "            left,",
                2,
            ),
        ),
    ),
    "lookup-state": (
        "comparator_callback",
        (
            (
                "state.e_callback_state,\n"
                "            left,\n"
                "            right,",
                "boundary.b_initial_state,\n"
                "            left,\n"
                "            right,",
                2,
            ),
        ),
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
    "normal-restoration": (
        "insert_tail_loop",
        (
            (
                "} else {\n"
                "                restored_state(called, sift, temporary, false)",
                "} else {\n"
                "                restored_state(called, gap, temporary, false)",
                1,
            ),
        ),
    ),
    "base-restoration": (
        "insert_tail_loop",
        (
            (
                "restored_state(shifted, sift, temporary, false)",
                "restored_state(shifted, gap, temporary, false)",
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
    "callback-next-state": (
        "comparator_callback",
        (
            (
                "e_callback_state: boundary_next_state(\n"
                "            boundary,\n"
                "            state.e_callback_state,\n"
                "            left,\n"
                "            right,\n"
                "        ),",
                "e_callback_state: state.e_callback_state,",
                1,
            ),
        ),
    ),
    "panic-propagation": (
        "comparator_callback",
        (
            (
                "e_panicked: boundary_panics(\n"
                "            boundary,\n"
                "            state.e_callback_state,\n"
                "            left,\n"
                "            right,\n"
                "        ),",
                "e_panicked: false,",
                1,
            ),
        ),
    ),
}

_STRUCT_CONSTRUCTORS = {
    "InsertTailState": "mkExactState",
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
    "InsertTailState": "ExactState",
}
_TOKEN = re.compile(
    r"\s*(?:"
    r"(?P<integer>[0-9]+)|"
    r"(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)|"
    r"(?P<operator>==|!=|<=|>=|&&|\|\||"
    r"[!<>\-+={}\(\)\[\],\.:;])"
    r")"
)
_BINARY_PRECEDENCE = {
    "||": 1,
    "&&": 2,
    "==": 3,
    "!=": 3,
    "<": 4,
    "<=": 4,
    ">": 4,
    ">=": 4,
    "+": 5,
    "-": 5,
}


def digest_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def digest_path(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"required target-078 v3 artifact is missing: {path}")
    return digest_bytes(path.read_bytes())


def _extract_spec_item(text: str, name: str) -> str:
    marker = f"pub open spec fn {name}("
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"Verus item is missing: {marker}")
    body_start = text.find("{", start)
    end = verus_syntax._matching_delimiter(
        text, body_start, "{", "}"
    )
    return text[start : end + 1]


class _InsertTailExpressionParser:
    def __init__(self, text: str, function: str) -> None:
        self.function = function
        self.tokens: list[str] = []
        position = 0
        while position < len(text):
            match = _TOKEN.match(text, position)
            if match is None:
                if text[position:].strip() == "":
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
        if self._peek() in {"!", "-"}:
            operator = self._take()
            return ("unary", operator, self._parse_unary())
        return self._parse_postfix()

    def _parse_postfix(self) -> tuple[Any, ...]:
        expression = self._parse_primary()
        while True:
            if self._peek() == ".":
                self._take()
                name = self._take()
                if self._peek() == "(":
                    arguments = self._parse_arguments()
                    expression = (
                        "method",
                        expression,
                        name,
                        arguments,
                    )
                else:
                    expression = ("field", expression, name)
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
            return ("call", token, self._parse_arguments())
        return ("variable", token)

    def _parse_arguments(self) -> tuple[tuple[Any, ...], ...]:
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
        return tuple(arguments)

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
    header = verus_syntax._normalize(item[:body_start])
    marker = f"pub open spec fn {name}"
    if not header.startswith(marker):
        raise ValueError(f"{name}: unsupported Verus signature {header!r}")
    open_paren = header.find("(", len(marker))
    close_paren = verus_syntax._matching_delimiter(
        header, open_paren, "(", ")"
    )
    parameters: list[tuple[str, str]] = []
    for parameter in header[open_paren + 1 : close_paren].split(","):
        if not parameter.strip():
            continue
        pieces = parameter.strip().split(":", 1)
        if len(pieces) != 2:
            raise ValueError(f"{name}: malformed parameter {parameter!r}")
        parameters.append(
            (pieces[0].strip(), verus_syntax._normalize(pieces[1]))
        )
    suffix = header[close_paren + 1 :].strip()
    match = re.fullmatch(
        r"-> ([A-Za-z][A-Za-z0-9_]*)(?: decreases .*,)?",
        suffix,
    )
    if match is None:
        raise ValueError(f"{name}: unsupported return clause {suffix!r}")
    return tuple(parameters), match.group(1)


def _flatten_index(
    expression: tuple[Any, ...],
) -> tuple[tuple[Any, ...], tuple[tuple[Any, ...], ...]]:
    indices: list[tuple[Any, ...]] = []
    while expression[0] == "index":
        indices.append(expression[2])
        expression = expression[1]
    indices.reverse()
    return expression, tuple(indices)


def _translate_expression(expression: tuple[Any, ...]) -> str:
    kind = expression[0]
    if kind in {"integer", "boolean", "variable"}:
        return str(expression[1])
    if kind == "unary":
        value = _translate_expression(expression[2])
        if expression[1] == "!":
            return f"(not {value})"
        if expression[1] == "-":
            return f"(- {value})"
        raise ValueError(f"unsupported unary expression: {expression}")
    if kind == "binary":
        operator = expression[1]
        left = _translate_expression(expression[2])
        right = _translate_expression(expression[3])
        smt_operator = {
            "==": "=",
            "!=": "distinct",
            "&&": "and",
            "||": "or",
            "<": "<",
            "<=": "<=",
            ">": ">",
            ">=": ">=",
            "+": "+",
            "-": "-",
        }.get(operator)
        if smt_operator is None:
            raise ValueError(f"unsupported binary expression: {expression}")
        return f"({smt_operator} {left} {right})"
    if kind == "if":
        return (
            f"(ite {_translate_expression(expression[1])} "
            f"{_translate_expression(expression[2])} "
            f"{_translate_expression(expression[3])})"
        )
    if kind == "block":
        result = _translate_expression(expression[2])
        for name, value in reversed(expression[1]):
            result = (
                f"(let (({name} {_translate_expression(value)})) {result})"
            )
        return result
    if kind == "call":
        name = expression[1]
        if name not in REFINED_FUNCTION_NAMES:
            raise ValueError(f"unbound Verus helper call: {name}")
        arguments = " ".join(
            _translate_expression(argument) for argument in expression[2]
        )
        return f"({REFINED_FUNCTION_NAMES[name]} {arguments})"
    if kind == "field":
        return (
            f"({expression[2]} {_translate_expression(expression[1])})"
        )
    if kind == "index":
        base, indices = _flatten_index(expression)
        if (
            base[0] == "field"
            and base[2] in _BOUNDARY_INDEX_ENCODINGS
        ):
            field = base[2]
            constructor, arity = _BOUNDARY_INDEX_ENCODINGS[field]
            if len(indices) != arity:
                raise ValueError(
                    f"{field}: expected {arity} indices, got {len(indices)}"
                )
            owner = _translate_expression(base[1])
            values = " ".join(
                _translate_expression(index) for index in indices
            )
            return f"(select ({field} {owner}) ({constructor} {values}))"
        if len(indices) != 1:
            raise ValueError(f"unsupported sequence indexing: {expression}")
        return (
            f"(select {_translate_expression(base)} "
            f"{_translate_expression(indices[0])})"
        )
    if kind == "method":
        owner = _translate_expression(expression[1])
        method = expression[2]
        arguments = expression[3]
        if method != "update" or len(arguments) != 2:
            raise ValueError(f"unsupported Verus method: {expression}")
        return (
            f"(store {owner} {_translate_expression(arguments[0])} "
            f"{_translate_expression(arguments[1])})"
        )
    if kind == "struct":
        struct = expression[1]
        actual = dict(expression[2])
        fields = SMT_FIELD_BINDINGS[struct]
        if len(actual) != len(expression[2]) or set(actual) != set(fields):
            raise ValueError(
                f"{struct}: constructor fields changed: "
                f"{tuple(name for name, _ in expression[2])!r}"
            )
        values = " ".join(
            _translate_expression(actual[field]) for field in fields
        )
        return f"({_STRUCT_CONSTRUCTORS[struct]} {values})"
    raise ValueError(f"unsupported Verus expression: {expression}")


def _derive_verus_smt(text: str) -> dict[str, Any]:
    definitions: list[str] = []
    functions: dict[str, Any] = {}
    for name, expected_signature in VERUS_SEMANTIC_SIGNATURES.items():
        item = _extract_spec_item(text, name)
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
        body = item[item.find("{") :]
        expression = _InsertTailExpressionParser(body, name).parse()
        translated = _translate_expression(expression)
        parameter_text = " ".join(
            f"({parameter} {smt_type})"
            for parameter, smt_type in smt_parameters
        )
        refined = REFINED_FUNCTION_NAMES[name]
        form = "define-fun-rec" if name in RECURSIVE_FUNCTIONS else "define-fun"
        definition = (
            f"({form} {refined} ({parameter_text}) {smt_return}\n"
            f"  {translated})"
        )
        definitions.append(definition)
        functions[name] = {
            "refined_smt_function": refined,
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
            "recursive": name in RECURSIVE_FUNCTIONS,
        }
    return {
        "definitions": definitions,
        "functions": functions,
        "source_sha256": digest_bytes(text.encode()),
    }


def accepted_smt_binding() -> dict[str, Any]:
    text = accepted_smt._prefix()
    boundary_fields = verus_syntax._smt_datatype_fields(text, "Boundary")
    exact_state_fields = verus_syntax._smt_datatype_fields(
        text, "ExactState"
    )
    if boundary_fields != SMT_FIELD_BINDINGS["ComparatorBoundary"]:
        raise ValueError("accepted Boundary fields changed")
    if exact_state_fields != SMT_FIELD_BINDINGS["InsertTailState"]:
        raise ValueError("accepted ExactState fields changed")
    boundary_sorts = verus_syntax._smt_datatype_field_sorts(
        text, "Boundary"
    )
    exact_state_sorts = verus_syntax._smt_datatype_field_sorts(
        text, "ExactState"
    )
    if boundary_sorts != SMT_FIELD_SORTS["Boundary"]:
        raise ValueError("accepted Boundary field sorts changed")
    if exact_state_sorts != SMT_FIELD_SORTS["ExactState"]:
        raise ValueError("accepted ExactState field sorts changed")
    exact_loop = verus_syntax._extract_smt_form(
        text, "(define-fun-rec ExactInsertTailLoop"
    )
    exact_entry = verus_syntax._extract_smt_definition(
        text, "ExactInsertTail"
    )
    loop_fragments = (
        "(store (e_sequence q) gap (select (e_sequence q) sift))",
        "(= sift begin)",
        "(ExactCallback shifted b temporary right)",
        "(store (e_sequence called) sift temporary)",
        "(ExactInsertTailLoop called b begin next_sift sift temporary)",
    )
    entry_fragments = (
        "(select (e_sequence q) tail)",
        "(select (e_sequence q) (- tail 1))",
        "(ExactCallback q b temporary right)",
        "(ExactInsertTailLoop called b begin (- tail 1) tail temporary)",
    )
    for definition, fragments, label in (
        (exact_loop, loop_fragments, "ExactInsertTailLoop"),
        (exact_entry, entry_fragments, "ExactInsertTail"),
    ):
        normalized = verus_syntax._normalize(definition)
        for fragment in fragments:
            if verus_syntax._normalize(fragment) not in normalized:
                raise ValueError(f"{label}: retained source semantics changed")
    return {
        "exact_source_sha256": digest_path(ACCEPTED_SMT_PATH),
        "prefix_sha256": digest_bytes(text.encode()),
        "datatype_fields": {
            "Boundary": list(boundary_fields),
            "ExactState": list(exact_state_fields),
        },
        "datatype_sorts": {
            "Boundary": [
                {"field": field, "sort": sort}
                for field, sort in boundary_sorts
            ],
            "ExactState": [
                {"field": field, "sort": sort}
                for field, sort in exact_state_sorts
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
        name: verus_syntax._verus_struct_fields(text, name)
        for name in SMT_FIELD_BINDINGS
    }
    if struct_fields != SMT_FIELD_BINDINGS:
        raise ValueError(f"Verus state fields changed: {struct_fields!r}")
    field_types = {
        name: verus_syntax._verus_struct_field_types(text, name)
        for name in VERUS_STRUCT_FIELD_TYPES
    }
    if field_types != VERUS_STRUCT_FIELD_TYPES:
        raise ValueError(f"Verus state field types changed: {field_types!r}")
    required_fragments = {
        "comparator_callback": (
            "e_sequence: state.e_sequence,",
            "state.e_callback_state,\n            left,\n            right,",
        ),
        "shifted_state": (
            "state.e_sequence.update(\n"
            "            gap,\n"
            "            state.e_sequence[sift],",
        ),
        "restored_state": (
            "state.e_sequence.update(destination, temporary)",
            "e_callback_state: state.e_callback_state,",
            "e_panicked: panicked,",
        ),
        "restored_sequence": (
            "state.e_sequence.update(gap, temporary)",
        ),
        "valid_insert_tail_input": (
            "!state.e_panicked\n"
            "        && 0 <= begin\n"
            "        && begin < tail\n"
            "        && tail < state.e_sequence.len()",
        ),
        "valid_insert_tail_loop_input": (
            "!state.e_panicked\n"
            "        && 0 <= begin\n"
            "        && begin <= sift\n"
            "        && gap == sift + 1\n"
            "        && gap < state.e_sequence.len()",
        ),
        "insert_tail_loop": (
            "let shifted = shifted_state(state, sift, gap);",
            "let next_sift = sift - 1;",
            "restored_state(called, sift, temporary, true)",
            "next_sift,\n                    sift,\n                    temporary,",
            "restored_state(called, sift, temporary, false)",
        ),
        "insert_tail": (
            "let temporary = state.e_sequence[tail];",
            "let right = state.e_sequence[tail - 1];",
            "begin,\n                tail - 1,\n                tail,\n                temporary,",
        ),
        "panic_state_is_boundary_observed": (
            "exists|lookup_state: int, left: int, right: int|",
            "boundary_panics(boundary, lookup_state, left, right)",
            "boundary_next_state(\n"
            "                    boundary,\n"
            "                    lookup_state,\n"
            "                    left,\n"
            "                    right,",
        ),
    }
    for name, fragments in required_fragments.items():
        item = _extract_spec_item(text, name)
        for fragment in fragments:
            if fragment not in item:
                raise ValueError(
                    f"{name}: source-sensitive fragment changed: {fragment}"
                )
    guard_sha256 = {
        name: digest_bytes(_extract_spec_item(text, name).encode())
        for name in PINNED_GUARD_FUNCTIONS
    }
    if guard_sha256 != EXPECTED_GUARD_SHA256:
        raise ValueError("fail-closed guard function body changed")
    derived = _derive_verus_smt(text)
    proof_items = {
        name: verus_syntax._extract_verus_item(text, "proof fn", name)
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
            "accepted ComparatorBoundary",
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
        "semantic_bridge": {
            "derivation": "parsed-verus-expression-ast-to-smt",
            "source_sha256": derived["source_sha256"],
            "functions": derived["functions"],
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
        raise ValueError(f"unknown target-078 v3 mutation: {kind}")
    if text is None:
        text = PROOF_PATH.read_text()
    function, replacements = _MUTATIONS[kind]
    marker = f"pub open spec fn {function}("
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"{kind}: mutation function is missing")
    body_start = text.find("{", start)
    end = verus_syntax._matching_delimiter(
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
(declare-const helper_lookup_state Int)
(declare-const helper_left Int)
(declare-const helper_right Int)
(declare-const helper_sift Int)
(declare-const helper_gap Int)
(declare-const helper_destination Int)
(declare-const helper_temporary Int)
(declare-const helper_panicked Bool)

(define-fun accepted_boundary_ordering () Int
  (BoundaryOrdering helper_boundary helper_lookup_state helper_left helper_right))
(define-fun refined_boundary_ordering () Int
  (RefinedBoundaryOrdering helper_boundary helper_lookup_state helper_left helper_right))
(define-fun accepted_boundary_next_state () Int
  (BoundaryNextState helper_boundary helper_lookup_state helper_left helper_right))
(define-fun refined_boundary_next_state () Int
  (RefinedBoundaryNextState helper_boundary helper_lookup_state helper_left helper_right))
(define-fun accepted_boundary_panics () Bool
  (BoundaryPanics helper_boundary helper_lookup_state helper_left helper_right))
(define-fun refined_boundary_panics () Bool
  (RefinedBoundaryPanics helper_boundary helper_lookup_state helper_left helper_right))
(define-fun accepted_target_less () Bool
  (TargetAdapterIsLess helper_boundary helper_lookup_state helper_left helper_right))
(define-fun refined_target_less () Bool
  (RefinedTargetAdapterIsLess helper_boundary helper_lookup_state helper_left helper_right))
(define-fun accepted_callback () ExactState
  (ExactCallback helper_state helper_boundary helper_left helper_right))
(define-fun refined_callback () ExactState
  (RefinedComparatorCallback helper_state helper_boundary helper_left helper_right))
(define-fun accepted_shifted () ExactState
  (mkExactState
    (store
      (e_sequence helper_state)
      helper_gap
      (select (e_sequence helper_state) helper_sift))
    (e_callback_state helper_state)
    false))
(define-fun refined_shifted () ExactState
  (RefinedShiftedState helper_state helper_sift helper_gap))
(define-fun accepted_restored () ExactState
  (mkExactState
    (store
      (e_sequence helper_state)
      helper_destination
      helper_temporary)
    (e_callback_state helper_state)
    helper_panicked))
(define-fun refined_restored () ExactState
  (RefinedRestoredState
    helper_state helper_destination helper_temporary helper_panicked))
"""
    equalities = [
        "(= accepted_boundary_ordering refined_boundary_ordering)",
        "(= accepted_boundary_next_state refined_boundary_next_state)",
        "(= accepted_boundary_panics refined_boundary_panics)",
        "(= accepted_target_less refined_target_less)",
        *_state_equalities("accepted_callback", "refined_callback"),
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
    false))
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
  (RefinedComparatorCallback
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
    domain = (
        "(and (not (e_panicked loop_state)) "
        "(<= 0 loop_begin) "
        "(<= loop_begin loop_sift) "
        "(= loop_gap (+ loop_sift 1)) "
        "(< loop_gap loop_sequence_len))"
    )
    induction_hypothesis = _state_equalities(
        "exact_loop_child", "refined_loop_child"
    )
    difference = _state_difference(
        "exact_loop_parent", "refined_loop_parent"
    )
    return declarations, domain, induction_hypothesis, difference


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
  (RefinedComparatorCallback
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
    domain = (
        "(and (not (e_panicked entry_state)) "
        "(<= 0 entry_begin) "
        "(< entry_begin entry_tail) "
        "(< entry_tail entry_sequence_len))"
    )
    loop_hypothesis = _state_equalities(
        "exact_entry_loop", "refined_entry_loop"
    )
    difference = _state_difference(
        "exact_entry_parent", "refined_entry_parent"
    )
    return declarations, domain, loop_hypothesis, difference


def correspondence_coverage() -> dict[str, Any]:
    _helper_text, helper_equalities = _helper_correspondence()
    _loop_text, _loop_domain, loop_hypothesis, _loop_difference = (
        _loop_step_correspondence()
    )
    _entry_text, _entry_domain, entry_hypothesis, _entry_difference = (
        _entry_correspondence()
    )
    return {
        "semantic_functions": list(VERUS_SEMANTIC_SIGNATURES),
        "state_fields": list(SMT_FIELD_BINDINGS["InsertTailState"]),
        "boundary_fields": list(SMT_FIELD_BINDINGS["ComparatorBoundary"]),
        "helper_comparison_count": len(helper_equalities),
        "loop_result_comparison_count": 3,
        "entry_result_comparison_count": 3,
        "induction_hypothesis_comparison_count": (
            len(loop_hypothesis) + len(entry_hypothesis)
        ),
        "comparison_count": (
            len(helper_equalities)
            + 3
            + 3
            + len(loop_hypothesis)
            + len(entry_hypothesis)
        ),
        "valid_domains": [
            "0 <= begin <= sift; gap == sift + 1; gap < sequence_len",
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
    derived = _derive_verus_smt(proof_text)
    helper_text, helper_equalities = _helper_correspondence()
    loop_text, loop_domain, loop_hypothesis, loop_difference = (
        _loop_step_correspondence()
    )
    entry_text, entry_domain, entry_hypothesis, entry_difference = (
        _entry_correspondence()
    )
    helper_conjunction = "\n      ".join(helper_equalities)
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
        + "\n"
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
        "ExactCallback",
        "ExactInsertTailLoop",
        "ExactInsertTail",
    ):
        if accepted not in text:
            raise ValueError(
                f"correspondence query omits accepted semantic {accepted}"
            )
    for marker in (
        "(<= loop_begin loop_sift)",
        "(= loop_gap (+ loop_sift 1))",
        "(< loop_gap loop_sequence_len)",
        "(=> (> loop_sift loop_begin)",
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


def _witness_header(proof_text: str) -> str:
    derived = _derive_verus_smt(proof_text)
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


def witness_query_text(
    kind: str,
    proof_text: str | None = None,
) -> str:
    if kind not in WITNESS_KINDS:
        raise ValueError(f"unknown target-078 v3 witness: {kind}")
    if proof_text is None:
        proof_text = PROOF_PATH.read_text()
    header = _witness_header(proof_text)
    equality = _witness_state_equalities()
    if kind == "no-shift":
        body = f"""
(declare-const witness_boundary Boundary)
(declare-const witness_sequence (Array Int Int))
(define-fun witness_state () ExactState
  (mkExactState witness_sequence 0 false))
(assert (= (select witness_sequence 0) 10))
(assert (= (select witness_sequence 1) 20))
(assert (= (BoundaryOrdering witness_boundary 0 20 10) 0))
(assert (= (BoundaryNextState witness_boundary 0 20 10) 1))
(assert (not (BoundaryPanics witness_boundary 0 20 10)))
(define-fun witness_exact_run () ExactState
  (ExactInsertTail witness_state witness_boundary 0 1))
(define-fun witness_refined_run () ExactState
  (RefinedInsertTail witness_state witness_boundary 0 1))
(assert (and
  {equality}
  (= (e_sequence witness_exact_run) witness_sequence)
  (= (e_callback_state witness_exact_run) 1)
  (not (e_panicked witness_exact_run))))
(check-sat)
(get-model)
"""
    elif kind == "multi-shift":
        body = f"""
(declare-const witness_boundary Boundary)
(declare-const witness_sequence (Array Int Int))
(define-fun witness_state () ExactState
  (mkExactState witness_sequence 0 false))
(assert (= (select witness_sequence 0) 10))
(assert (= (select witness_sequence 1) 20))
(assert (= (select witness_sequence 2) 30))
(assert (= (select witness_sequence 3) 5))
(assert (= (BoundaryOrdering witness_boundary 0 5 30) (- 1)))
(assert (= (BoundaryNextState witness_boundary 0 5 30) 1))
(assert (not (BoundaryPanics witness_boundary 0 5 30)))
(assert (= (BoundaryOrdering witness_boundary 1 5 20) (- 1)))
(assert (= (BoundaryNextState witness_boundary 1 5 20) 2))
(assert (not (BoundaryPanics witness_boundary 1 5 20)))
(assert (= (BoundaryOrdering witness_boundary 2 5 10) 0))
(assert (= (BoundaryNextState witness_boundary 2 5 10) 3))
(assert (not (BoundaryPanics witness_boundary 2 5 10)))
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
  (not (e_panicked witness_exact_run))))
(check-sat)
(get-model)
"""
    elif kind == "panic-after-shift":
        body = f"""
(declare-const witness_boundary Boundary)
(declare-const witness_sequence (Array Int Int))
(define-fun witness_state () ExactState
  (mkExactState witness_sequence 0 false))
(assert (= (select witness_sequence 0) 10))
(assert (= (select witness_sequence 1) 20))
(assert (= (select witness_sequence 2) 5))
(assert (= (BoundaryOrdering witness_boundary 0 5 20) (- 1)))
(assert (= (BoundaryNextState witness_boundary 0 5 20) 1))
(assert (not (BoundaryPanics witness_boundary 0 5 20)))
(assert (= (BoundaryOrdering witness_boundary 1 5 10) 0))
(assert (= (BoundaryNextState witness_boundary 1 5 10) 7))
(assert (BoundaryPanics witness_boundary 1 5 10))
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
  (e_panicked witness_exact_run)))
(check-sat)
(get-model)
"""
    else:
        body = f"""
(declare-const witness_boundary Boundary)
(declare-const witness_sequence (Array Int Int))
(define-fun witness_state () ExactState
  (mkExactState witness_sequence 0 false))
(assert (= (select witness_sequence 0) 20))
(assert (= (select witness_sequence 1) 30))
(assert (= (select witness_sequence 2) 5))
(assert (= (BoundaryOrdering witness_boundary 0 5 30) (- 1)))
(assert (= (BoundaryNextState witness_boundary 0 5 30) 1))
(assert (not (BoundaryPanics witness_boundary 0 5 30)))
(assert (= (BoundaryOrdering witness_boundary 1 5 20) (- 1)))
(assert (= (BoundaryNextState witness_boundary 1 5 20) 2))
(assert (not (BoundaryPanics witness_boundary 1 5 20)))
(define-fun witness_exact_run () ExactState
  (ExactInsertTail witness_state witness_boundary 0 2))
(define-fun witness_refined_run () ExactState
  (RefinedInsertTail witness_state witness_boundary 0 2))
(assert (and
  {equality}
  (= (select (e_sequence witness_exact_run) 0) 5)
  (= (select (e_sequence witness_exact_run) 1) 20)
  (= (select (e_sequence witness_exact_run) 2) 30)
  (= (e_callback_state witness_exact_run) 2)
  (not (e_panicked witness_exact_run))))
(check-sat)
(get-model)
"""
    return header + body


def validate_witness_query(kind: str, text: str) -> None:
    if kind not in WITNESS_KINDS:
        raise ValueError(f"unknown target-078 v3 witness: {kind}")
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
        ),
        "multi-shift": (
            "(ExactInsertTail witness_state witness_boundary 0 3)",
            "(= (select (e_sequence witness_exact_run) 1) 5)",
            "(= (select (e_sequence witness_exact_run) 3) 30)",
        ),
        "insert-at-begin": (
            "(ExactInsertTail witness_state witness_boundary 0 2)",
            "(= (select (e_sequence witness_exact_run) 0) 5)",
            "(= (select (e_sequence witness_exact_run) 2) 30)",
            "(= (e_callback_state witness_exact_run) 2)",
        ),
        "panic-after-shift": (
            "(ExactInsertTail witness_state witness_boundary 0 2)",
            "(BoundaryPanics witness_boundary 1 5 10)",
            "(= (e_callback_state witness_exact_run) 7)",
            "(e_panicked witness_exact_run)",
        ),
    }
    for marker in required[kind]:
        if marker not in text:
            raise ValueError(f"{kind}: witness marker missing: {marker}")


def binding_manifest() -> dict[str, Any]:
    proof = validate_proof()
    accepted = accepted_smt_binding()
    coverage = correspondence_coverage()
    return {
        "schema_version": 1,
        "artifact_id": "target_078_insert_tail_refinement_v3",
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
            "accepted_exact_smt": {
                "path": ACCEPTED_SMT_PATH.relative_to(ROOT).as_posix(),
                "sha256": digest_path(ACCEPTED_SMT_PATH),
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
        "field_bindings": {
            "ComparatorBoundary_to_Boundary": {
                field: field
                for field in SMT_FIELD_BINDINGS["ComparatorBoundary"]
            },
            "InsertTailState_to_ExactState": {
                field: field
                for field in SMT_FIELD_BINDINGS["InsertTailState"]
            },
        },
        "function_bindings": {
            "insert_tail_loop": "ExactInsertTailLoop",
            "insert_tail": "ExactInsertTail",
            "comparator_callback": "ExactCallback",
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
            "source_sensitive_mutations": list(MUTATION_KINDS),
        },
        "verus": proof,
        "accepted_smt": accepted,
        "classification_effect": (
            "none; this additive package refines insert_tail and CopyOnDrop "
            "without replacing accepted operational-v1"
        ),
        "stage_transition": "disabled",
    }


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_id": "target_078_insert_tail_refinement_v3",
        "target": TARGET,
        "boundary_source": (
            "accepted target_078_operational_v1 ComparatorBoundary"
        ),
        "transition_inputs": [
            "shared ComparatorBoundary",
            "pre-call sequence of source identities",
            "pre-call callback state",
            "valid begin and tail indices",
        ],
        "consumed_boundary_maps": [
            "ordering at each current pre-call callback state and operand pair",
            "callback next state at the same lookup key",
            "callback panic at the same lookup key",
        ],
        "source_derived_not_boundary": [
            "initial comparison before moving the tail",
            "shift source and destination",
            "gap movement",
            "normal guard restoration",
            "panic-time guard restoration",
            "callback-state update before panic propagation",
            "final sequence, panic status, and callback state",
        ],
        "excluded": [
            "precomputed callback result",
            "precomputed loop result or terminal result",
            "selected output or final state",
            "answer encoding",
            "execution trace",
        ],
        "narrower_than_target": True,
        "arbitrary_valid_range": True,
        "reason": (
            "only genuine comparator observations are trusted; every "
            "insert_tail and CopyOnDrop transition remains source-derived"
        ),
        "accepted_boundary_sha256": digest_path(ACCEPTED_BOUNDARY_PATH),
    }
