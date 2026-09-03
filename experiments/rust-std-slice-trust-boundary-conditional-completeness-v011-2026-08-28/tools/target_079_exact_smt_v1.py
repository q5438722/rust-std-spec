#!/usr/bin/env python3
"""Abort-aware composition of target 079 with accepted ExactRunState."""

from __future__ import annotations

from hashlib import sha256

import target_078_exact_smt_v1 as accepted


SOURCE_TRANSITIONS = accepted.SOURCE_TRANSITIONS
ACCEPTED_DEFINITIONS_SHA256 = sha256(
    accepted.definitions_text().encode()
).hexdigest()
EXACT_STATE_CONSTRUCTOR_COUNT = 14
ACTIVE_CLEANUP_GUARD_COUNT = 7


def _matching_paren(text: str, start: int) -> int:
    depth = 0
    for position in range(start, len(text)):
        character = text[position]
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return position
    raise ValueError("unterminated SMT expression")


def _list_items(
    text: str, start: int, end: int
) -> list[tuple[int, int]]:
    cursor = start + 1
    items: list[tuple[int, int]] = []
    while cursor < end:
        while cursor < end and text[cursor].isspace():
            cursor += 1
        if cursor >= end:
            break
        item_start = cursor
        if text[cursor] == "(":
            item_end = _matching_paren(text, cursor) + 1
        else:
            while (
                cursor < end
                and not text[cursor].isspace()
                and text[cursor] not in "()"
            ):
                cursor += 1
            item_end = cursor
        items.append((item_start, item_end))
        cursor = item_end
    return items


def _arguments(
    text: str, start: int, end: int
) -> list[tuple[int, int]]:
    items = _list_items(text, start, end)
    if not items or text[slice(*items[0])] != "mkExactState":
        raise ValueError("expected an ExactState constructor")
    return items[1:]


def _expression_items(expression: str) -> list[str]:
    expression = expression.strip()
    if not expression.startswith("("):
        return [expression]
    end = _matching_paren(expression, 0)
    if expression[end + 1 :].strip():
        raise ValueError("trailing text after SMT expression")
    return [
        expression[left:right].strip()
        for left, right in _list_items(expression, 0, end)
    ]


def _abort_source(state: str) -> tuple[str, str | None]:
    items = _expression_items(state)
    head = items[0]
    if head == "BoundaryNextState" and len(items) == 5:
        return (
            state.replace("BoundaryNextState", "BoundaryAborts", 1),
            None,
        )
    if head == "e_callback_state" and len(items) == 2:
        source = items[1]
        return f"(e_aborted {source})", source
    if head == "b_initial_state" and len(items) == 2:
        return "false", None
    raise ValueError(
        "cannot structurally derive abort state from callback state "
        f"expression: {state}"
    )


def _is_cleanup_store(sequence: str, source: str | None) -> bool:
    if source is None:
        return False
    items = _expression_items(sequence)
    if len(items) != 4 or items[0] != "store":
        return False
    if " ".join(items[1].split()) != " ".join(
        f"(e_sequence {source})".split()
    ):
        return False
    value = _expression_items(items[3])
    return value[0] != "select"


def _abort_aware_exact_states(text: str) -> str:
    first_definition = text.index("(define-fun ExactCallback")
    starts: list[int] = []
    cursor = first_definition
    while True:
        start = text.find("(mkExactState", cursor)
        if start < 0:
            break
        starts.append(start)
        cursor = start + 1
    if len(starts) != EXACT_STATE_CONSTRUCTOR_COUNT:
        raise ValueError(
            "accepted ExactRunState constructor count changed: "
            f"{len(starts)}"
        )

    cleanup_guards = 0
    for start in reversed(starts):
        end = _matching_paren(text, start)
        spans = _arguments(text, start, end)
        if len(spans) != 3:
            raise ValueError("accepted ExactState arity changed")
        values = [text[left:right].strip() for left, right in spans]
        sequence, state, panicked = values
        aborted, source = _abort_source(state)
        if _is_cleanup_store(sequence, source):
            assert source is not None
            sequence = (
                f"(ite (e_aborted {source}) (e_sequence {source}) "
                f"{sequence})"
            )
            cleanup_guards += 1

        replacement = (
            "(mkExactState\n"
            f"      {sequence}\n"
            f"      {state}\n"
            f"      {panicked}\n"
            f"      {aborted})"
        )
        text = text[:start] + replacement + text[end + 1 :]
    if cleanup_guards != ACTIVE_CLEANUP_GUARD_COUNT:
        raise ValueError(
            "accepted active cleanup guard count changed: "
            f"{cleanup_guards}"
        )
    return text


def definitions_text() -> str:
    """Return accepted selection semantics with only abort state composed in."""

    text = accepted.definitions_text()
    old_datatype = """\
      (e_sequence (Array Int Int))
      (e_callback_state Int)
      (e_panicked Bool)))))"""
    new_datatype = """\
      (e_sequence (Array Int Int))
      (e_callback_state Int)
      (e_panicked Bool)
      (e_aborted Bool)))))"""
    if text.count(old_datatype) != 1:
        raise ValueError("accepted ExactState datatype changed")
    text = text.replace(old_datatype, new_datatype, 1)
    text = text.replace(
        "; Source-exact big-step state. Every callback updates this state "
        "before panic\n"
        "; propagation, and every active gap guard restores its saved "
        "identity.",
        "; Source-exact target-078 big-step state, imported byte-for-byte "
        "before\n"
        "; adding target-079 adapter abort. Ordinary panic restores active "
        "guards;\n"
        "; abort preserves the interrupted sequence and bypasses cleanup.",
        1,
    )
    text = _abort_aware_exact_states(text)
    if text.count("(e_aborted Bool)") != 1:
        raise ValueError("abort selector was not added exactly once")
    if text.count("(BoundaryAborts b") < 1:
        raise ValueError("ExactCallback does not consume adapter abort")
    if text.count("(ite (e_aborted") != ACTIVE_CLEANUP_GUARD_COUNT:
        raise ValueError("not every active guard bypasses cleanup on abort")
    cursor = text.index("(define-fun ExactCallback")
    constructor_count = 0
    while True:
        start = text.find("(mkExactState", cursor)
        if start < 0:
            break
        end = _matching_paren(text, start)
        if len(_arguments(text, start, end)) != 4:
            raise ValueError("abort was not added to every ExactState")
        constructor_count += 1
        cursor = end + 1
    if constructor_count != EXACT_STATE_CONSTRUCTOR_COUNT:
        raise ValueError("adapted ExactState constructor count changed")
    return text
