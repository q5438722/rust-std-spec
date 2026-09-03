#!/usr/bin/env python3
"""Structural and data-flow guards for future conditional SMT obligations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


SExpr = str | list["SExpr"]

ALLOWED_BOUNDARY_ROLES = {
    "callback_argument",
    "callback_result",
    "callback_state_transition",
    "callback_panic",
    "iterator_private_state",
    "input_memory",
    "input_provenance",
    "input_layout",
    "input_initialization",
    "source_helper_observation",
    "allocator_outcome",
}
PROHIBITED_BOUNDARY_ROLES = {
    "selected_output",
    "selected_index",
    "answer_encoding",
    "aggregate_final_state",
    "implementation_trace",
    "full_execution_trace",
    "final_permutation",
    "pivot_trace",
    "swap_trace",
}
ALLOWED_DECLARED_FUNCTION_ROLES = {
    "callback_observation",
    "memory_observation",
    "source_transition",
    "allocator_observation",
}
AGGREGATE_TARGET_SORTS = {"Input", "Output", "State"}
THEOREM_VARIABLE_SORTS = {
    "input": "Input",
    "boundary": "Boundary",
    "output1": "Output",
    "state1": "State",
    "output2": "Output",
    "state2": "State",
}


class GuardError(ValueError):
    """Raised when an obligation violates a structural checker invariant."""


def _tokens(text: str) -> list[str]:
    tokens: list[str] = []
    index = 0
    while index < len(text):
        char = text[index]
        if char.isspace():
            index += 1
            continue
        if char == ";":
            while index < len(text) and text[index] != "\n":
                index += 1
            continue
        if char in "()":
            tokens.append(char)
            index += 1
            continue
        if char == '"':
            start = index
            index += 1
            escaped = False
            while index < len(text):
                if text[index] == '"' and not escaped:
                    index += 1
                    break
                escaped = text[index] == "\\" and not escaped
                if text[index] != "\\":
                    escaped = False
                index += 1
            tokens.append(text[start:index])
            continue
        start = index
        while index < len(text) and not text[index].isspace() and text[index] not in "();":
            index += 1
        tokens.append(text[start:index])
    return tokens


def parse_smt(text: str) -> list[SExpr]:
    tokens = _tokens(text)
    cursor = 0

    def parse_one() -> SExpr:
        nonlocal cursor
        if cursor >= len(tokens):
            raise GuardError("unexpected end of SMT input")
        token = tokens[cursor]
        cursor += 1
        if token != "(":
            if token == ")":
                raise GuardError("unexpected closing parenthesis")
            return token
        result: list[SExpr] = []
        while cursor < len(tokens) and tokens[cursor] != ")":
            result.append(parse_one())
        if cursor >= len(tokens):
            raise GuardError("unterminated SMT expression")
        cursor += 1
        return result

    forms: list[SExpr] = []
    while cursor < len(tokens):
        forms.append(parse_one())
    return forms


def _walk(expr: SExpr) -> Iterable[list[SExpr]]:
    if not isinstance(expr, list):
        return
    yield expr
    for child in expr:
        yield from _walk(child)


def _head(expr: SExpr) -> str:
    if isinstance(expr, list) and expr and isinstance(expr[0], str):
        return expr[0]
    return ""


def _definitions(forms: list[SExpr]) -> dict[str, list[SExpr]]:
    result: dict[str, list[SExpr]] = {}

    def add(name: str, definition: list[SExpr]) -> None:
        if name in result:
            raise GuardError(f"duplicate SMT function definition: {name}")
        result[name] = definition

    for form in forms:
        if (
            _head(form) in {"define-fun", "define-fun-rec"}
            and len(form) >= 5
            and isinstance(form[1], str)
        ):
            add(form[1], form)
            continue
        if _head(form) != "define-funs-rec":
            continue
        if (
            len(form) != 3
            or not isinstance(form[1], list)
            or not isinstance(form[2], list)
            or len(form[1]) != len(form[2])
        ):
            raise GuardError("malformed define-funs-rec declaration")
        for signature, body in zip(form[1], form[2]):
            if (
                not isinstance(signature, list)
                or len(signature) != 3
                or not isinstance(signature[0], str)
                or not isinstance(signature[1], list)
            ):
                raise GuardError("malformed define-funs-rec signature")
            name = signature[0]
            add(
                name,
                [
                    "define-fun-rec",
                    name,
                    signature[1],
                    signature[2],
                    body,
                ],
            )
    return result


def defined_function_names(text: str) -> frozenset[str]:
    """Return every function defined by singular or mutual declarations."""
    return frozenset(_definitions(parse_smt(text)))


def _datatype_fields(forms: list[SExpr], datatype: str) -> dict[str, str]:
    declarations: list[list[SExpr]] = []
    for form in forms:
        if _head(form) == "declare-datatype" and len(form) == 3:
            if form[1] == datatype and isinstance(form[2], list):
                declarations.append(form[2])
            continue
        if _head(form) != "declare-datatypes" or len(form) != 3:
            continue
        sorts, bodies = form[1], form[2]
        if not isinstance(sorts, list) or not isinstance(bodies, list):
            continue
        for sort, body in zip(sorts, bodies):
            if (
                isinstance(sort, list)
                and sort
                and sort[0] == datatype
                and isinstance(body, list)
            ):
                declarations.append(body)
    if len(declarations) != 1:
        raise GuardError(
            f"obligation must declare exactly one {datatype} datatype"
        )
    if len(declarations[0]) != 1:
        raise GuardError(f"{datatype} must be a single-constructor record")
    fields: dict[str, str] = {}
    for constructor in declarations[0]:
        if not isinstance(constructor, list) or not constructor:
            raise GuardError(f"{datatype} has a malformed constructor")
        for field in constructor[1:]:
            if (
                not isinstance(field, list)
                or len(field) != 2
                or not isinstance(field[0], str)
            ):
                raise GuardError(f"{datatype} has a malformed field")
            selector = field[0]
            if selector in fields:
                raise GuardError(f"{datatype} declares a duplicate field selector")
            fields[selector] = _sort_name(field[1])
    return fields


def _datatype_selectors(forms: list[SExpr], datatype: str) -> set[str]:
    return set(_datatype_fields(forms, datatype))


def _calls(expr: SExpr) -> set[str]:
    return {
        node[0]
        for node in _walk(expr)
        if node and isinstance(node[0], str)
    }


def _reachable_definitions(
    definitions: dict[str, list[SExpr]], root: str
) -> set[str]:
    pending = [root]
    reached: set[str] = set()
    while pending:
        name = pending.pop()
        if name in reached or name not in definitions:
            continue
        reached.add(name)
        for called in _calls(definitions[name][4]):
            if called in definitions and called not in reached:
                pending.append(called)
    return reached


def _sort_name(sort: SExpr) -> str:
    if isinstance(sort, str):
        return sort
    return " ".join(str(item) for item in sort)


def _constant_bool(expr: SExpr) -> bool | None:
    if expr == "true":
        return True
    if expr == "false":
        return False
    head = _head(expr)
    if head == "not" and len(expr) == 2:
        value = _constant_bool(expr[1])
        return None if value is None else not value
    if head == "=" and len(expr) == 3 and expr[1] == expr[2]:
        return True
    if head in {"<=", ">="} and len(expr) == 3 and expr[1] == expr[2]:
        return True
    if head in {"<", ">", "distinct"} and len(expr) == 3 and expr[1] == expr[2]:
        return False
    if head == "and":
        values = [_constant_bool(child) for child in expr[1:]]
        if False in values:
            return False
        if values and all(value is True for value in values):
            return True
    if head == "or":
        values = [_constant_bool(child) for child in expr[1:]]
        if True in values:
            return True
        if values and all(value is False for value in values):
            return False
    if head == "=>" and len(expr) == 3:
        antecedent = _constant_bool(expr[1])
        consequent = _constant_bool(expr[2])
        if antecedent is False or consequent is True:
            return True
        if antecedent is True and consequent is not None:
            return consequent
    if head == "ite" and len(expr) == 4:
        condition = _constant_bool(expr[1])
        if condition is not None:
            return _constant_bool(expr[2] if condition else expr[3])
        if expr[2] == expr[3]:
            return _constant_bool(expr[2])
    return None


def _meaningful_symbols(
    expr: SExpr,
    definitions: dict[str, list[SExpr]],
    environment: dict[str, set[str]] | None = None,
    call_stack: tuple[str, ...] = (),
) -> set[str]:
    environment = environment or {}
    if isinstance(expr, str):
        if expr in environment:
            return set(environment[expr])
        if expr in definitions and expr not in call_stack:
            definition = definitions[expr]
            if definition[2] == []:
                return {expr} | _meaningful_symbols(
                    definition[4],
                    definitions,
                    environment,
                    (*call_stack, expr),
                )
        return set()
    if not expr or _constant_bool(expr) is not None:
        return set()
    head = _head(expr)
    if head == "let" and len(expr) == 3 and isinstance(expr[1], list):
        local = dict(environment)
        for binding in expr[1]:
            if (
                isinstance(binding, list)
                and len(binding) == 2
                and isinstance(binding[0], str)
            ):
                local[binding[0]] = _meaningful_symbols(
                    binding[1], definitions, environment, call_stack
                )
        return _meaningful_symbols(expr[2], definitions, local, call_stack)
    if head == "and":
        if any(_constant_bool(child) is False for child in expr[1:]):
            return set()
        children = [
            child for child in expr[1:] if _constant_bool(child) is not True
        ]
    elif head == "or":
        if any(_constant_bool(child) is True for child in expr[1:]):
            return set()
        children = [
            child for child in expr[1:] if _constant_bool(child) is not False
        ]
    elif head == "=>" and len(expr) == 3:
        antecedent = _constant_bool(expr[1])
        consequent = _constant_bool(expr[2])
        if antecedent is False or consequent is True:
            return set()
        if antecedent is True:
            children = [expr[2]]
        elif consequent is False:
            children = [expr[1]]
        else:
            children = expr[1:]
    elif head == "ite" and len(expr) == 4:
        condition = _constant_bool(expr[1])
        if condition is not None:
            children = [expr[2] if condition else expr[3]]
        elif expr[2] == expr[3]:
            children = [expr[2]]
        else:
            children = expr[1:]
    elif head == "*" and "0" in expr[1:]:
        return set()
    else:
        children = expr[1:]
    if head in definitions and head not in call_stack:
        definition = definitions[head]
        arguments = definition[2]
        if isinstance(arguments, list) and len(arguments) == len(expr) - 1:
            local = dict(environment)
            for formal, actual in zip(arguments, expr[1:]):
                if (
                    isinstance(formal, list)
                    and len(formal) == 2
                    and isinstance(formal[0], str)
                ):
                    local[formal[0]] = _meaningful_symbols(
                        actual, definitions, environment, call_stack
                    )
            return {head} | _meaningful_symbols(
                definition[4],
                definitions,
                local,
                (*call_stack, head),
            )
    result = {head} if head else set()
    for child in children:
        result.update(
            _meaningful_symbols(child, definitions, environment, call_stack)
        )
    return result


@dataclass(frozen=True)
class Dependencies:
    kinds: frozenset[str]
    semantic: bool = False

    def union(self, other: "Dependencies") -> "Dependencies":
        return Dependencies(self.kinds | other.kinds, self.semantic or other.semantic)


@dataclass
class _DependencyValue:
    constant: int
    terms: dict[tuple[Any, ...], tuple[int, Dependencies]]

    @classmethod
    def integer(cls, value: int) -> "_DependencyValue":
        return cls(value, {})

    @classmethod
    def atom(
        cls, key: tuple[Any, ...], dependencies: Dependencies
    ) -> "_DependencyValue":
        return cls(0, {key: (1, dependencies)})

    def dependencies(self) -> Dependencies:
        result = Dependencies(frozenset())
        for _, dependencies in self.terms.values():
            result = result.union(dependencies)
        return result

    def canonical(self) -> tuple[Any, ...]:
        terms = tuple(
            sorted(
                ((key, coefficient) for key, (coefficient, _) in self.terms.items()),
                key=lambda item: repr(item[0]),
            )
        )
        return ("affine", self.constant, terms)

    def plus(self, other: "_DependencyValue") -> "_DependencyValue":
        terms = dict(self.terms)
        for key, (coefficient, dependencies) in other.terms.items():
            old_coefficient, old_dependencies = terms.get(
                key, (0, Dependencies(frozenset()))
            )
            new_coefficient = old_coefficient + coefficient
            if new_coefficient == 0:
                terms.pop(key, None)
            else:
                terms[key] = (
                    new_coefficient,
                    old_dependencies.union(dependencies),
                )
        return _DependencyValue(self.constant + other.constant, terms)

    def scaled(self, coefficient: int) -> "_DependencyValue":
        if coefficient == 0:
            return _DependencyValue.integer(0)
        return _DependencyValue(
            self.constant * coefficient,
            {
                key: (term_coefficient * coefficient, dependencies)
                for key, (term_coefficient, dependencies) in self.terms.items()
            },
        )


def _integer_literal(expr: str) -> int | None:
    try:
        return int(expr, 10)
    except ValueError:
        return None


def _dependency_value(
    expr: SExpr,
    environment: dict[str, _DependencyValue],
    global_environment: dict[str, _DependencyValue],
    boundary_selectors: set[str],
    output_selectors: set[str],
    definitions: dict[str, list[SExpr]],
    semantic_definitions: set[str],
    call_stack: tuple[str, ...] = (),
) -> _DependencyValue:
    if isinstance(expr, str):
        if expr in environment:
            return environment[expr]
        if expr in definitions and expr not in call_stack:
            definition = definitions[expr]
            if definition[2] == []:
                return _dependency_value(
                    definition[4],
                    dict(global_environment),
                    global_environment,
                    boundary_selectors,
                    output_selectors,
                    definitions,
                    semantic_definitions,
                    (*call_stack, expr),
                )
        integer = _integer_literal(expr)
        if integer is not None:
            return _DependencyValue.integer(integer)
        return _DependencyValue.atom(
            ("symbol", expr), Dependencies(frozenset())
        )
    if not expr:
        return _DependencyValue.integer(0)
    constant_bool = _constant_bool(expr)
    if constant_bool is not None:
        return _DependencyValue.integer(int(constant_bool))
    if _head(expr) == "let" and len(expr) == 3 and isinstance(expr[1], list):
        local = dict(environment)
        for binding in expr[1]:
            if (
                isinstance(binding, list)
                and len(binding) == 2
                and isinstance(binding[0], str)
            ):
                local[binding[0]] = _dependency_value(
                    binding[1],
                    environment,
                    global_environment,
                    boundary_selectors,
                    output_selectors,
                    definitions,
                    semantic_definitions,
                    call_stack,
                )
        return _dependency_value(
            expr[2],
            local,
            global_environment,
            boundary_selectors,
            output_selectors,
            definitions,
            semantic_definitions,
            call_stack,
        )
    head = _head(expr)
    if head in definitions and head not in call_stack:
        definition = definitions[head]
        arguments = definition[2]
        if isinstance(arguments, list) and len(arguments) == len(expr) - 1:
            local = dict(global_environment)
            for formal, actual in zip(arguments, expr[1:]):
                if (
                    isinstance(formal, list)
                    and len(formal) == 2
                    and isinstance(formal[0], str)
                ):
                    local[formal[0]] = _dependency_value(
                        actual,
                        environment,
                        global_environment,
                        boundary_selectors,
                        output_selectors,
                        definitions,
                        semantic_definitions,
                        call_stack,
                    )
            return _dependency_value(
                definition[4],
                local,
                global_environment,
                boundary_selectors,
                output_selectors,
                definitions,
                semantic_definitions,
                (*call_stack, head),
            )
    children = [
        _dependency_value(
            child,
            environment,
            global_environment,
            boundary_selectors,
            output_selectors,
            definitions,
            semantic_definitions,
            call_stack,
        )
        for child in expr[1:]
    ]
    if head == "+":
        result = _DependencyValue.integer(0)
        for child in children:
            result = result.plus(child)
        return result
    if head == "-" and children:
        if len(children) == 1:
            return children[0].scaled(-1)
        result = children[0]
        for child in children[1:]:
            result = result.plus(child.scaled(-1))
        return result
    if head == "*":
        if any(not child.terms and child.constant == 0 for child in children):
            return _DependencyValue.integer(0)
        constant_factor = 1
        nonconstant: list[_DependencyValue] = []
        for child in children:
            if child.terms:
                nonconstant.append(child)
            else:
                constant_factor *= child.constant
        if not nonconstant:
            return _DependencyValue.integer(constant_factor)
        if len(nonconstant) == 1:
            return nonconstant[0].scaled(constant_factor)

    dependencies = Dependencies(frozenset(), head in semantic_definitions)
    for child in children:
        dependencies = dependencies.union(child.dependencies())
    if head in boundary_selectors:
        dependencies = dependencies.union(Dependencies(frozenset({"boundary"})))
    if head in output_selectors:
        dependencies = dependencies.union(Dependencies(frozenset({"output"})))
    child_keys = [child.canonical() for child in children]
    if head == "*":
        child_keys.sort(key=repr)
    return _DependencyValue.atom(
        ("call", head, tuple(child_keys)),
        dependencies,
    )


def _dependencies(
    expr: SExpr,
    environment: dict[str, Dependencies],
    global_environment: dict[str, Dependencies],
    boundary_selectors: set[str],
    output_selectors: set[str],
    definitions: dict[str, list[SExpr]],
    semantic_definitions: set[str],
    call_stack: tuple[str, ...] = (),
) -> Dependencies:
    symbolic_global = {
        name: _DependencyValue.atom(("symbol", name), dependencies)
        for name, dependencies in global_environment.items()
    }
    symbolic_environment = dict(symbolic_global)
    symbolic_environment.update(
        {
            name: _DependencyValue.atom(("symbol", name), dependencies)
            for name, dependencies in environment.items()
        }
    )
    return _dependency_value(
        expr,
        symbolic_environment,
        symbolic_global,
        boundary_selectors,
        output_selectors,
        definitions,
        semantic_definitions,
        call_stack,
    ).dependencies()


def _sort_dependencies(sort: SExpr) -> Dependencies:
    name = _sort_name(sort)
    if name == "Input":
        return Dependencies(frozenset({"input"}))
    if name == "Boundary":
        return Dependencies(frozenset({"boundary"}))
    if name in {"Output", "State"}:
        return Dependencies(frozenset({"output"}))
    return Dependencies(frozenset())


def _global_environment(forms: list[SExpr]) -> dict[str, Dependencies]:
    environment: dict[str, Dependencies] = {}
    for form in forms:
        if (
            _head(form) == "declare-const"
            and len(form) == 3
            and isinstance(form[1], str)
        ):
            environment[form[1]] = _sort_dependencies(form[2])
    return environment


def _definition_environment(
    definition: list[SExpr],
    global_environment: dict[str, Dependencies],
) -> dict[str, Dependencies]:
    environment = dict(global_environment)
    arguments = definition[2]
    if not isinstance(arguments, list):
        return environment
    for argument in arguments:
        if (
            not isinstance(argument, list)
            or len(argument) != 2
            or not isinstance(argument[0], str)
        ):
            continue
        environment[argument[0]] = _sort_dependencies(argument[1])
    return environment


def _validate_definition_signature(
    definition: list[SExpr],
    symbol: str,
    expected_argument_sorts: tuple[str, ...],
) -> list[str]:
    if len(definition) != 5 or _sort_name(definition[3]) != "Bool":
        raise GuardError(f"{symbol}: definition must return Bool")
    arguments = definition[2]
    if not isinstance(arguments, list) or len(arguments) != len(
        expected_argument_sorts
    ):
        raise GuardError(f"{symbol}: definition has the wrong arity")
    names: list[str] = []
    sorts: list[str] = []
    for argument in arguments:
        if (
            not isinstance(argument, list)
            or len(argument) != 2
            or not isinstance(argument[0], str)
        ):
            raise GuardError(f"{symbol}: definition has malformed arguments")
        names.append(argument[0])
        sorts.append(_sort_name(argument[1]))
    if len(names) != len(set(names)):
        raise GuardError(f"{symbol}: definition has duplicate arguments")
    if tuple(sorts) != expected_argument_sorts:
        raise GuardError(
            f"{symbol}: definition argument sorts {tuple(sorts)} do not match "
            f"{expected_argument_sorts}"
        )
    return names


def _free_symbols(expr: SExpr, bound: set[str]) -> set[str]:
    if isinstance(expr, str):
        return set() if expr in bound else {expr}
    if not expr:
        return set()
    head = _head(expr)
    if head == "let" and len(expr) == 3 and isinstance(expr[1], list):
        result: set[str] = set()
        local = set(bound)
        for binding in expr[1]:
            if (
                isinstance(binding, list)
                and len(binding) == 2
                and isinstance(binding[0], str)
            ):
                result.update(_free_symbols(binding[1], bound))
                local.add(binding[0])
        result.update(_free_symbols(expr[2], local))
        return result
    if head in {"forall", "exists"} and len(expr) >= 3 and isinstance(expr[1], list):
        local = set(bound)
        for binder in expr[1]:
            if (
                isinstance(binder, list)
                and len(binder) == 2
                and isinstance(binder[0], str)
            ):
                local.add(binder[0])
        result: set[str] = set()
        for child in expr[2:]:
            result.update(_free_symbols(child, local))
        return result
    result: set[str] = set()
    for child in expr[1:]:
        result.update(_free_symbols(child, bound))
    return result


def _declared_call_dependencies(
    expr: SExpr,
    environment: dict[str, Dependencies],
    global_environment: dict[str, Dependencies],
    boundary_selectors: set[str],
    output_selectors: set[str],
    definitions: dict[str, list[SExpr]],
    semantic_definitions: set[str],
    declared_functions: set[str],
    call_stack: tuple[str, ...] = (),
) -> list[tuple[str, Dependencies]]:
    if isinstance(expr, str):
        if expr in definitions and expr not in call_stack:
            definition = definitions[expr]
            if definition[2] == []:
                return _declared_call_dependencies(
                    definition[4],
                    dict(global_environment),
                    global_environment,
                    boundary_selectors,
                    output_selectors,
                    definitions,
                    semantic_definitions,
                    declared_functions,
                    (*call_stack, expr),
                )
        return []
    if not expr:
        return []
    head = _head(expr)
    if head == "let" and len(expr) == 3 and isinstance(expr[1], list):
        local = dict(environment)
        calls: list[tuple[str, Dependencies]] = []
        for binding in expr[1]:
            if (
                isinstance(binding, list)
                and len(binding) == 2
                and isinstance(binding[0], str)
            ):
                calls.extend(
                    _declared_call_dependencies(
                        binding[1],
                        environment,
                        global_environment,
                        boundary_selectors,
                        output_selectors,
                        definitions,
                        semantic_definitions,
                        declared_functions,
                        call_stack,
                    )
                )
                local[binding[0]] = _dependencies(
                    binding[1],
                    environment,
                    global_environment,
                    boundary_selectors,
                    output_selectors,
                    definitions,
                    semantic_definitions,
                    call_stack,
                )
        calls.extend(
            _declared_call_dependencies(
                expr[2],
                local,
                global_environment,
                boundary_selectors,
                output_selectors,
                definitions,
                semantic_definitions,
                declared_functions,
                call_stack,
            )
        )
        return calls
    if head in definitions and head not in call_stack:
        definition = definitions[head]
        arguments = definition[2]
        if isinstance(arguments, list) and len(arguments) == len(expr) - 1:
            local = dict(global_environment)
            calls = []
            for formal, actual in zip(arguments, expr[1:]):
                calls.extend(
                    _declared_call_dependencies(
                        actual,
                        environment,
                        global_environment,
                        boundary_selectors,
                        output_selectors,
                        definitions,
                        semantic_definitions,
                        declared_functions,
                        call_stack,
                    )
                )
                if (
                    isinstance(formal, list)
                    and len(formal) == 2
                    and isinstance(formal[0], str)
                ):
                    local[formal[0]] = _dependencies(
                        actual,
                        environment,
                        global_environment,
                        boundary_selectors,
                        output_selectors,
                        definitions,
                        semantic_definitions,
                        call_stack,
                    )
            calls.extend(
                _declared_call_dependencies(
                    definition[4],
                    local,
                    global_environment,
                    boundary_selectors,
                    output_selectors,
                    definitions,
                    semantic_definitions,
                    declared_functions,
                    (*call_stack, head),
                )
            )
            return calls
    calls = []
    if head in declared_functions:
        dependencies = Dependencies(frozenset())
        for argument in expr[1:]:
            dependencies = dependencies.union(
                _dependencies(
                    argument,
                    environment,
                    global_environment,
                    boundary_selectors,
                    output_selectors,
                    definitions,
                    semantic_definitions,
                    call_stack,
                )
            )
        calls.append((head, dependencies))
    for child in expr[1:]:
        calls.extend(
            _declared_call_dependencies(
                child,
                environment,
                global_environment,
                boundary_selectors,
                output_selectors,
                definitions,
                semantic_definitions,
                declared_functions,
                call_stack,
            )
        )
    return calls


def _has_exact_call(expr: SExpr, name: str, arguments: list[str]) -> bool:
    return any(
        node == [name, *arguments]
        for node in _walk(expr)
    )


def _selector_equality_pairs(expr: SExpr) -> set[tuple[str, str, str]]:
    pairs: set[tuple[str, str, str]] = set()
    if _head(expr) != "=" or len(expr) != 3:
        return pairs
    left, right = expr[1], expr[2]
    for first, second in ((left, right), (right, left)):
        if (
            isinstance(first, list)
            and len(first) == 2
            and isinstance(first[0], str)
            and isinstance(first[1], str)
            and isinstance(second, list)
            and len(second) == 2
            and second[0] == first[0]
            and isinstance(second[1], str)
        ):
            pairs.add((first[0], first[1], second[1]))
    return pairs


def _guaranteed_equality_pairs(expr: SExpr) -> set[tuple[str, str, str]]:
    """Return selector equalities that must hold whenever expr is true."""
    if isinstance(expr, str) or not expr or _constant_bool(expr) is not None:
        return set()
    direct = _selector_equality_pairs(expr)
    if direct:
        return direct
    head = _head(expr)
    if head == "and":
        required: set[tuple[str, str, str]] = set()
        for child in expr[1:]:
            required.update(_guaranteed_equality_pairs(child))
        return required
    if head == "or":
        branches = [
            child for child in expr[1:]
            if _constant_bool(child) is not False
        ]
        if not branches or any(
            _constant_bool(child) is True for child in branches
        ):
            return set()
        required = _guaranteed_equality_pairs(branches[0])
        for branch in branches[1:]:
            required.intersection_update(_guaranteed_equality_pairs(branch))
        return required
    if head == "=>" and len(expr) == 3:
        if _constant_bool(expr[1]) is True:
            return _guaranteed_equality_pairs(expr[2])
        return set()
    if head == "ite" and len(expr) == 4:
        condition = _constant_bool(expr[1])
        if condition is not None:
            return _guaranteed_equality_pairs(
                expr[2] if condition else expr[3]
            )
        required = _guaranteed_equality_pairs(expr[2])
        required.intersection_update(_guaranteed_equality_pairs(expr[3]))
        return required
    return set()


def _direct_principal_transitions(
    expr: SExpr,
    principal_formals: dict[str, str],
    source_transitions: set[str],
    definitions: dict[str, list[SExpr]],
) -> set[str]:
    head = _head(expr)
    if head in source_transitions and head in definitions:
        definition = definitions[head]
        arguments = definition[2]
        if isinstance(arguments, list) and len(arguments) == len(expr) - 1:
            meaningful = _meaningful_symbols(definition[4], definitions)
            for selector, principal_formal in principal_formals.items():
                for formal, actual in zip(arguments, expr[1:]):
                    if (
                        actual == principal_formal
                        and isinstance(formal, list)
                        and len(formal) == 2
                        and isinstance(formal[0], str)
                        and selector in meaningful
                        and any(
                            isinstance(node, list)
                            and len(node) == 2
                            and _head(node) == selector
                            and node[1] == formal[0]
                            for node in _walk(definition[4])
                        )
                    ):
                        return {head}
    if head != "=" or len(expr) != 3:
        return set()
    result: set[str] = set()
    for principal, value in ((expr[1], expr[2]), (expr[2], expr[1])):
        if (
            isinstance(principal, list)
            and len(principal) == 2
            and isinstance(principal[0], str)
            and principal[1] == principal_formals.get(principal[0])
            and _head(value) in source_transitions
        ):
            result.add(_head(value))
    return result


def _guaranteed_principal_transitions(
    expr: SExpr,
    principal_formals: dict[str, str],
    source_transitions: set[str],
    definitions: dict[str, list[SExpr]],
) -> set[str]:
    if isinstance(expr, str) or not expr or _constant_bool(expr) is not None:
        return set()
    direct = _direct_principal_transitions(
        expr, principal_formals, source_transitions, definitions
    )
    if direct:
        return direct
    head = _head(expr)
    if head == "and":
        required: set[str] = set()
        for child in expr[1:]:
            required.update(
                _guaranteed_principal_transitions(
                    child,
                    principal_formals,
                    source_transitions,
                    definitions,
                )
            )
        return required
    if head == "or":
        branches = [
            child for child in expr[1:]
            if _constant_bool(child) is not False
        ]
        if not branches or any(
            _constant_bool(child) is True for child in branches
        ):
            return set()
        required = _guaranteed_principal_transitions(
            branches[0],
            principal_formals,
            source_transitions,
            definitions,
        )
        for branch in branches[1:]:
            required.intersection_update(
                _guaranteed_principal_transitions(
                    branch,
                    principal_formals,
                    source_transitions,
                    definitions,
                )
            )
        return required
    if head == "=>" and len(expr) == 3:
        if _constant_bool(expr[1]) is True:
            return _guaranteed_principal_transitions(
                expr[2],
                principal_formals,
                source_transitions,
                definitions,
            )
        return set()
    if head == "ite" and len(expr) == 4:
        condition = _constant_bool(expr[1])
        if condition is not None:
            return _guaranteed_principal_transitions(
                expr[2] if condition else expr[3],
                principal_formals,
                source_transitions,
                definitions,
            )
        required = _guaranteed_principal_transitions(
            expr[2],
            principal_formals,
            source_transitions,
            definitions,
        )
        required.intersection_update(
            _guaranteed_principal_transitions(
                expr[3],
                principal_formals,
                source_transitions,
                definitions,
            )
        )
        return required
    return set()


def _validate_theorem_variables(
    forms: list[SExpr], metadata: dict[str, Any]
) -> dict[str, str]:
    variables = metadata.get("theorem_variables")
    if (
        not isinstance(variables, dict)
        or set(variables) != set(THEOREM_VARIABLE_SORTS)
        or any(
            not isinstance(name, str) or not name
            for name in variables.values()
        )
    ):
        raise GuardError("theorem-variable metadata is malformed")
    if len(set(variables.values())) != len(THEOREM_VARIABLE_SORTS):
        raise GuardError("theorem variables must be six distinct symbols")

    declarations: dict[str, str] = {}
    for form in forms:
        if _head(form) != "declare-const":
            continue
        if len(form) != 3 or not isinstance(form[1], str):
            raise GuardError("malformed theorem constant declaration")
        symbol = form[1]
        if symbol in declarations:
            raise GuardError(f"duplicate constant declaration: {symbol}")
        declarations[symbol] = _sort_name(form[2])

    for role, expected_sort in THEOREM_VARIABLE_SORTS.items():
        symbol = variables[role]
        actual_sort = declarations.get(symbol)
        if actual_sort is None:
            raise GuardError(
                f"{role}: theorem variable {symbol} is not declared"
            )
        if actual_sort != expected_sort:
            raise GuardError(
                f"{role}: theorem variable {symbol} has sort {actual_sort}, "
                f"expected {expected_sort}"
            )
    unexpected = set(declarations) - set(variables.values())
    if unexpected:
        raise GuardError(
            "obligation declares global constants outside the six "
            f"source-audited theorem variables: {sorted(unexpected)}"
        )
    return variables


def _validate_principal_observations(
    forms: list[SExpr], metadata: dict[str, Any]
) -> list[dict[str, str]]:
    expected: dict[str, tuple[str, str, str]] = {}
    for datatype, left, right in (
        ("Output", "output1", "output2"),
        ("State", "state1", "state2"),
    ):
        for selector, sort in _datatype_fields(forms, datatype).items():
            if selector in expected:
                raise GuardError(
                    f"principal selector is ambiguous across datatypes: {selector}"
                )
            expected[selector] = (left, right, sort)
    if not expected:
        raise GuardError("principal observation schema must not be empty")

    observations = metadata.get("principal_observations")
    if not isinstance(observations, list) or any(
        not isinstance(item, dict)
        or not isinstance(item.get("selector"), str)
        or not isinstance(item.get("left"), str)
        or not isinstance(item.get("right"), str)
        or not isinstance(item.get("sort"), str)
        for item in observations
    ):
        raise GuardError("principal-observation metadata is malformed")
    selectors = [item["selector"] for item in observations]
    if len(selectors) != len(set(selectors)):
        raise GuardError("principal-observation metadata contains duplicates")
    actual = {
        item["selector"]: (item["left"], item["right"], item["sort"])
        for item in observations
    }
    if actual != expected:
        raise GuardError(
            "principal-observation metadata does not exactly match the "
            "Output/State selector-and-sort schema"
        )
    return [
        {
            "selector": selector,
            "left": left,
            "right": right,
            "sort": sort,
        }
        for selector, (left, right, sort) in expected.items()
    ]


def _check_theorem_shape(
    forms: list[SExpr], metadata: dict[str, Any]
) -> dict[str, str]:
    variables = _validate_theorem_variables(forms, metadata)
    logic_forms = [form for form in forms if _head(form) == "set-logic"]
    if logic_forms != [["set-logic", "ALL"]]:
        raise GuardError(
            "obligation must select datatype-compatible SMT logic ALL exactly once"
        )
    allowed_commands = {
        "set-logic",
        "declare-datatype",
        "declare-datatypes",
        "declare-const",
        "declare-fun",
        "define-fun",
        "define-fun-rec",
        "assert",
        "check-sat",
    }
    unsupported = [
        _head(form) or "<atom>"
        for form in forms
        if _head(form) not in allowed_commands
    ]
    if unsupported:
        raise GuardError(
            f"obligation contains unsupported top-level commands: {unsupported}"
        )
    check_sat_forms = [form for form in forms if _head(form) == "check-sat"]
    if check_sat_forms != [["check-sat"]] or forms[-1] != ["check-sat"]:
        raise GuardError(
            "obligation must end with exactly one argument-free check-sat"
        )
    x = variables["input"]
    b = variables["boundary"]
    y1 = variables["output1"]
    s1 = variables["state1"]
    y2 = variables["output2"]
    s2 = variables["state2"]
    assertion_forms = [form for form in forms if _head(form) == "assert"]
    if len(assertion_forms) != 1:
        raise GuardError(
            "obligation must contain exactly one assertion: "
            "the negated theorem implication"
        )
    assertion = assertion_forms[0]
    if (
        len(assertion) != 2
        or _head(assertion[1]) != "not"
        or len(assertion[1]) != 2
        or _head(assertion[1][1]) != "=>"
    ):
        raise GuardError("the sole assertion must be the negated theorem implication")
    implication = assertion[1][1]
    if len(implication) != 3 or _head(implication[1]) != "and":
        raise GuardError("theorem antecedent must be a single conjunction")
    antecedent = implication[1]
    expected = [
        ["Requires_T", x],
        ["Boundary_T", x, b],
        ["Spec_T", x, b, y1, s1],
        ["Spec_T", x, b, y2, s2],
    ]
    actual = antecedent[1:]
    if actual != expected:
        raise GuardError(
            "theorem must use one shared input and one shared boundary in literal order"
        )
    if implication[2] != ["Equivalent_T", x, b, y1, s1, y2, s2]:
        raise GuardError("theorem consequent is not the required Equivalent_T call")
    return variables


def validate_obligation(text: str, metadata: dict[str, Any]) -> None:
    schema_version = metadata.get("schema_version")
    if type(schema_version) is not int or schema_version < 2:
        raise GuardError("metadata schema version must be an integer >= 2")
    forms = parse_smt(text)
    definitions = _definitions(forms)
    variables = _check_theorem_shape(forms, metadata)
    target_definition = metadata.get("target_definition")
    if (
        not isinstance(target_definition, str)
        or not target_definition
        or target_definition
        in {"Requires_T", "Boundary_T", "Spec_T", "Equivalent_T"}
    ):
        raise GuardError("target definition metadata is malformed")
    required = {
        "Requires_T",
        "Boundary_T",
        "Spec_T",
        "Equivalent_T",
        target_definition,
    }
    missing = required - definitions.keys()
    if missing:
        raise GuardError(f"missing defined obligation symbols: {sorted(missing)}")
    signature_arguments = {
        "Requires_T": _validate_definition_signature(
            definitions["Requires_T"], "Requires_T", ("Input",)
        ),
        "Boundary_T": _validate_definition_signature(
            definitions["Boundary_T"],
            "Boundary_T",
            ("Input", "Boundary"),
        ),
        "Spec_T": _validate_definition_signature(
            definitions["Spec_T"],
            "Spec_T",
            ("Input", "Boundary", "Output", "State"),
        ),
        "Equivalent_T": _validate_definition_signature(
            definitions["Equivalent_T"],
            "Equivalent_T",
            ("Input", "Boundary", "Output", "State", "Output", "State"),
        ),
        target_definition: _validate_definition_signature(
            definitions[target_definition],
            target_definition,
            ("Input", "Boundary", "Output", "State"),
        ),
    }
    theorem_constants = set(variables.values())
    for symbol, definition in definitions.items():
        arguments = definition[2]
        formal_names = {
            argument[0]
            for argument in arguments
            if (
                isinstance(arguments, list)
                and isinstance(argument, list)
                and len(argument) == 2
                and isinstance(argument[0], str)
            )
        }
        captured = _free_symbols(definition[4], formal_names) & theorem_constants
        if captured:
            raise GuardError(
                f"{symbol}: definition closes over theorem constants "
                f"{sorted(captured)}"
            )

    boundary_fields = metadata.get("boundary_fields", [])
    if not isinstance(boundary_fields, list):
        raise GuardError("boundary field metadata must be a list")
    metadata_selectors = [
        field.get("selector", "") for field in boundary_fields
        if isinstance(field, dict)
    ]
    if len(metadata_selectors) != len(boundary_fields):
        raise GuardError("boundary field metadata contains a malformed entry")
    if len(metadata_selectors) != len(set(metadata_selectors)):
        raise GuardError("boundary field metadata contains duplicate selectors")
    declared_boundary_selectors = _datatype_selectors(forms, "Boundary")
    if set(metadata_selectors) != declared_boundary_selectors:
        missing_metadata = declared_boundary_selectors - set(metadata_selectors)
        missing_datatype = set(metadata_selectors) - declared_boundary_selectors
        raise GuardError(
            "Boundary datatype and metadata selectors differ: "
            f"missing_metadata={sorted(missing_metadata)}, "
            f"missing_datatype={sorted(missing_datatype)}"
        )
    boundary_scope = metadata.get("boundary_scope")
    strict_boundary_backing = schema_version >= 3
    if boundary_scope is None:
        boundary_scope = {}
    if not isinstance(boundary_scope, dict):
        raise GuardError("boundary-scope metadata must be an object")

    def metadata_ids(value: Any, label: str) -> set[str]:
        if (
            not isinstance(value, list)
            or any(not isinstance(item, str) or not item for item in value)
            or len(value) != len(set(value))
        ):
            raise GuardError(f"{label} must be a duplicate-free string list")
        return set(value)

    admitted_trust_sites = metadata_ids(
        boundary_scope.get("admitted_trust_site_ids", []),
        "admitted boundary trust-site IDs",
    )
    excluded_trust_sites = metadata_ids(
        boundary_scope.get("excluded_retained_trust_site_ids", []),
        "excluded retained trust-site IDs",
    )
    context_only_trust_sites = metadata_ids(
        boundary_scope.get("context_only_trust_site_ids", []),
        "context-only trust-site IDs",
    )
    if (
        admitted_trust_sites & excluded_trust_sites
        or admitted_trust_sites & context_only_trust_sites
        or excluded_trust_sites & context_only_trust_sites
    ):
        raise GuardError("boundary trust-site dispositions overlap")
    audited_trust_sites = metadata_ids(
        boundary_scope.get("all_audited_trust_site_ids", []),
        "all audited trust-site IDs",
    )
    if strict_boundary_backing and (
        not audited_trust_sites
        or (
            admitted_trust_sites
            | excluded_trust_sites
            | context_only_trust_sites
        )
        != audited_trust_sites
    ):
        raise GuardError(
            "boundary trust-site dispositions do not partition the audited set"
        )

    boundary_replacement_ids: set[str] = set()
    replacement_metadata = metadata.get("source_backed_replacements", [])
    if strict_boundary_backing or replacement_metadata:
        if not isinstance(replacement_metadata, list):
            raise GuardError("source-backed replacement metadata must be a list")
        replacement_records: dict[str, dict[str, Any]] = {}
        source_transition_symbols = metadata_ids(
            metadata.get("source_transition_definitions", []),
            "source-transition definitions",
        )
        replaced_trust_sites: set[str] = set()
        for replacement in replacement_metadata:
            if not isinstance(replacement, dict):
                raise GuardError("source-backed replacement metadata is malformed")
            replacement_id = replacement.get("replacement_id")
            if (
                not isinstance(replacement_id, str)
                or not replacement_id
                or replacement_id in replacement_records
            ):
                raise GuardError(
                    "source-backed replacement IDs are missing or duplicated"
                )
            citations = metadata_ids(
                replacement.get("source_citations"),
                f"{replacement_id}: source citations",
            )
            symbols = metadata_ids(
                replacement.get("symbols"),
                f"{replacement_id}: source-transition symbols",
            )
            replaced_sites = metadata_ids(
                replacement.get("replaces_trust_site_ids"),
                f"{replacement_id}: replaced trust-site IDs",
            )
            if not citations or not symbols or not replaced_sites:
                raise GuardError(
                    f"{replacement_id}: source-backed replacement is incomplete"
                )
            if not symbols <= source_transition_symbols:
                raise GuardError(
                    f"{replacement_id}: replacement names undeclared source transitions"
                )
            if not replaced_sites <= excluded_trust_sites:
                raise GuardError(
                    f"{replacement_id}: replacement does not target excluded sites"
                )
            if replaced_sites & replaced_trust_sites:
                raise GuardError("excluded trust site has multiple replacements")
            replaced_trust_sites.update(replaced_sites)
            replacement_records[replacement_id] = replacement
        boundary_replacement_ids = metadata_ids(
            boundary_scope.get("source_backed_replacement_ids", []),
            "declared source-backed replacement IDs",
        )
        if not boundary_replacement_ids <= set(replacement_records):
            raise GuardError(
                "boundary scope names an undeclared source-backed replacement"
            )
        unresolved_trust_sites = metadata_ids(
            metadata.get("unresolved_source_model_trust_site_ids", []),
            "unresolved source-model trust-site IDs",
        )
        source_model_incomplete = (
            metadata.get("model_status") == "missing-source-backed-model"
            and metadata.get("domain", {}).get("source_model_complete") is False
        )
        if strict_boundary_backing and source_model_incomplete:
            if (
                not unresolved_trust_sites
                or unresolved_trust_sites & replaced_trust_sites
                or unresolved_trust_sites | replaced_trust_sites
                != excluded_trust_sites
            ):
                raise GuardError(
                    "incomplete source model does not partition replaced and "
                    "unresolved retained trust sites"
                )
        elif strict_boundary_backing and (
            replaced_trust_sites != excluded_trust_sites
            or unresolved_trust_sites
        ):
            raise GuardError(
                "excluded retained trust sites lack exact source replacements"
            )
        if set(replacement_records) & audited_trust_sites:
            raise GuardError(
                "source-backed replacement identity reuses a retained trust-site ID"
            )

    boundary_selectors: set[str] = set()
    used_replacement_ids: set[str] = set()
    for field in boundary_fields:
        selector = field.get("selector", "")
        role = field.get("role", "")
        if not selector:
            raise GuardError("boundary field lacks a selector")
        if role in PROHIBITED_BOUNDARY_ROLES or role not in ALLOWED_BOUNDARY_ROLES:
            raise GuardError(f"{selector}: prohibited or unknown boundary role {role}")
        citations = metadata_ids(
            field.get("source_citations"),
            f"{selector}: source citations",
        )
        trust_sites = metadata_ids(
            field.get("trust_site_ids", []),
            f"{selector}: trust-site IDs",
        )
        replacement_ids = metadata_ids(
            field.get("source_backed_replacement_ids", []),
            f"{selector}: source-backed replacement IDs",
        )
        if not citations or not (trust_sites or replacement_ids):
            raise GuardError(f"{selector}: boundary field lacks source/trust backing")
        if trust_sites & excluded_trust_sites:
            raise GuardError(f"{selector}: excluded trust site backs a boundary field")
        if strict_boundary_backing:
            if not trust_sites <= admitted_trust_sites:
                raise GuardError(
                    f"{selector}: boundary trust backing is not declared admitted"
                )
            if not replacement_ids <= boundary_replacement_ids:
                raise GuardError(
                    f"{selector}: source replacement backing is not declared"
                )
            for replacement_id in replacement_ids:
                replacement_citations = set(
                    replacement_records[replacement_id]["source_citations"]
                )
                if not replacement_citations <= citations:
                    raise GuardError(
                        f"{selector}: replacement citation is absent from field backing"
                    )
        elif replacement_ids:
            raise GuardError(
                f"{selector}: source replacement backing requires schema-v3 metadata"
            )
        used_replacement_ids.update(replacement_ids)
        boundary_selectors.add(selector)
    if strict_boundary_backing and not used_replacement_ids <= boundary_replacement_ids:
        raise GuardError("boundary fields use undeclared source replacements")
    if strict_boundary_backing and boundary_replacement_ids - used_replacement_ids:
        raise GuardError("declared source-backed replacement is unused")

    declared_function_metadata = metadata.get("declared_functions", [])
    if not isinstance(declared_function_metadata, list) or any(
        not isinstance(item, dict) or not item.get("symbol")
        for item in declared_function_metadata
    ):
        raise GuardError("declared-function metadata is malformed")
    declared_metadata = {
        item["symbol"]: item for item in declared_function_metadata
    }
    if len(declared_metadata) != len(declared_function_metadata):
        raise GuardError("declared-function metadata contains duplicate symbols")
    declared_forms: dict[str, list[SExpr]] = {}
    for form in forms:
        if _head(form) != "declare-fun":
            continue
        if (
            len(form) != 4
            or not isinstance(form[1], str)
            or not isinstance(form[2], list)
        ):
            raise GuardError("malformed uninterpreted function declaration")
        symbol = form[1]
        if not symbol or symbol in declared_forms:
            raise GuardError("malformed or duplicate uninterpreted function declaration")
        if not form[2]:
            raise GuardError(
                f"{symbol}: nullary uninterpreted functions are unaudited "
                "global constants"
            )
        declared_forms[symbol] = form
        declaration = declared_metadata.get(symbol)
        if declaration is None:
            raise GuardError(f"{symbol}: unclassified uninterpreted function")
        if declaration.get("role") not in ALLOWED_DECLARED_FUNCTION_ROLES:
            raise GuardError(f"{symbol}: functionality-like uninterpreted function")
        if not declaration.get("source_citations"):
            raise GuardError(f"{symbol}: uninterpreted function lacks source citations")
        argument_sorts = {
            _sort_name(item) for item in form[2]
        } if len(form) > 2 and isinstance(form[2], list) else set()
        return_sort = _sort_name(form[3]) if len(form) > 3 else ""
        if argument_sorts & AGGREGATE_TARGET_SORTS:
            raise GuardError(
                f"{symbol}: opaque function consumes an aggregate target sort"
            )
        if return_sort in {"Output", "State"}:
            raise GuardError(f"{symbol}: uninterpreted function returns a principal result")
        if (
            return_sort == "Bool"
            and ({"Output", "State"} & argument_sorts)
        ):
            raise GuardError(f"{symbol}: opaque whole-target functionality relation")
    if set(declared_metadata) != set(declared_forms):
        stale = set(declared_metadata) - set(declared_forms)
        raise GuardError(
            f"declared-function metadata names undeclared symbols: {sorted(stale)}"
        )

    spec_argument_names = signature_arguments["Spec_T"]
    if definitions["Spec_T"][4] != [target_definition, *spec_argument_names]:
        raise GuardError(
            "Spec_T must be an exact forwarding call to the target definition"
        )

    boundary_calls = _meaningful_symbols(
        definitions["Boundary_T"][4], definitions
    )
    target_calls = _meaningful_symbols(
        definitions[target_definition][4], definitions
    )
    for selector in boundary_selectors:
        if selector not in boundary_calls:
            raise GuardError(
                f"{selector}: boundary field is not meaningfully constrained by Boundary_T"
            )
        if selector not in target_calls:
            raise GuardError(
                f"{selector}: boundary field is not meaningfully used by the target definition"
            )

    principal_observations = _validate_principal_observations(forms, metadata)
    output_selectors = {
        item["selector"] for item in principal_observations
    }
    source_transition_definitions = metadata.get("source_transition_definitions")
    if (
        not isinstance(source_transition_definitions, list)
        or not source_transition_definitions
        or any(
            not isinstance(symbol, str) or not symbol
            for symbol in source_transition_definitions
        )
        or len(source_transition_definitions)
        != len(set(source_transition_definitions))
    ):
        raise GuardError("source-transition metadata is malformed or empty")
    semantic_definitions = set(source_transition_definitions)
    if not semantic_definitions <= definitions.keys():
        raise GuardError("source transition metadata names an undefined helper")
    if target_definition in semantic_definitions:
        raise GuardError(
            "source-transition metadata must name a proper target helper"
        )
    unreachable_transitions = semantic_definitions - target_calls
    if unreachable_transitions:
        raise GuardError(
            "source-transition definitions are not meaningfully reachable "
            f"from the target definition: {sorted(unreachable_transitions)}"
        )
    target_arguments = signature_arguments[target_definition]
    principal_formals = {
        item["selector"]: target_arguments[
            2 if item["left"] == "output1" else 3
        ]
        for item in principal_observations
    }
    determining_transitions = _guaranteed_principal_transitions(
        definitions[target_definition][4],
        principal_formals,
        semantic_definitions,
        definitions,
    )
    non_determining_transitions = semantic_definitions - determining_transitions
    if non_determining_transitions:
        raise GuardError(
            "source transitions must directly and conjunctively determine a "
            "principal observation: "
            f"{sorted(non_determining_transitions)}"
        )

    global_environment = _global_environment(forms)
    target_environment = _definition_environment(
        definitions[target_definition], global_environment
    )
    for symbol, dependencies in _declared_call_dependencies(
        definitions[target_definition][4],
        target_environment,
        global_environment,
        boundary_selectors,
        output_selectors,
        definitions,
        semantic_definitions,
        set(declared_forms),
    ):
        if "output" in dependencies.kinds:
            raise GuardError(
                f"{symbol}: opaque whole-target relation consumes principal "
                "observations at its call site"
            )
    for definition in definitions.values():
        environment = _definition_environment(definition, global_environment)
        for node in _walk(definition[4]):
            if _head(node) != "=" or len(node) != 3:
                continue
            left = _dependencies(
                node[1],
                environment,
                global_environment,
                boundary_selectors,
                output_selectors,
                definitions,
                semantic_definitions,
            )
            right = _dependencies(
                node[2],
                environment,
                global_environment,
                boundary_selectors,
                output_selectors,
                definitions,
                semantic_definitions,
            )
            for output_side, other_side in ((left, right), (right, left)):
                if "output" not in output_side.kinds:
                    continue
                other_symbols = _meaningful_symbols(
                    node[2] if output_side is left else node[1],
                    definitions,
                    environment={
                        name: {name} for name in environment
                    },
                )
                opaque = set(declared_forms) & other_symbols
                if opaque:
                    raise GuardError(
                        "principal observation depends on uninterpreted "
                        f"functionality: {sorted(opaque)}"
                    )
                if (
                    other_side.kinds
                    and other_side.kinds <= {"boundary"}
                ):
                    raise GuardError(
                        "principal observation is equated to boundary-only data"
                    )
    if metadata.get("equivalence_kind") == "exact":
        pairs = _guaranteed_equality_pairs(definitions["Equivalent_T"][4])
        equivalent_arguments = signature_arguments["Equivalent_T"]
        equivalent_formals = {
            "output1": equivalent_arguments[2],
            "state1": equivalent_arguments[3],
            "output2": equivalent_arguments[4],
            "state2": equivalent_arguments[5],
        }
        expected_pairs = {
            (
                item["selector"],
                equivalent_formals[item["left"]],
                equivalent_formals[item["right"]],
            )
            for item in principal_observations
        }
        if not expected_pairs <= pairs:
            raise GuardError("exact equivalence omits a principal observation")
    else:
        review = metadata.get("weak_equivalence_review", {})
        if not (
            review.get("source_citations")
            and review.get("positive_witness")
            and review.get("negative_witness")
        ):
            raise GuardError("weak equivalence lacks citations and both witnesses")


def example_obligation() -> tuple[str, dict[str, Any]]:
    text = """\
(set-logic ALL)
(declare-datatypes ((Input 0)) (((mkInput (x_value Int)))))
(declare-datatypes ((Boundary 0)) (((mkBoundary (b_callback_value Int)))))
(declare-datatypes ((Output 0)) (((mkOutput (y_value Int)))))
(declare-datatypes ((State 0)) (((mkState (s_value Int)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun CallbackStep ((x Input) (b Boundary)) Int
  (+ (x_value x) (b_callback_value b)))
(define-fun Requires_T ((x Input)) Bool true)
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (>= (b_callback_value b) 0))
(define-fun TargetDefinition_T ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (= (y_value y) (CallbackStep x b))
       (= (s_value s) (x_value x))))
(define-fun Spec_T ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and (= (y_value y1) (y_value y2))
       (= (s_value s1) (s_value s2))))
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
    metadata = {
        "schema_version": 2,
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
                "selector": "b_callback_value",
                "role": "callback_result",
                "source_citations": ["design/example.rs:10"],
                "trust_site_ids": ["DESIGN-TS-001"],
            }
        ],
        "declared_functions": [],
        "source_transition_definitions": ["CallbackStep"],
        "equivalence_kind": "exact",
        "principal_observations": [
            {
                "selector": "y_value",
                "left": "output1",
                "right": "output2",
                "sort": "Int",
            },
            {
                "selector": "s_value",
                "left": "state1",
                "right": "state2",
                "sort": "Int",
            },
        ],
    }
    return text, metadata
