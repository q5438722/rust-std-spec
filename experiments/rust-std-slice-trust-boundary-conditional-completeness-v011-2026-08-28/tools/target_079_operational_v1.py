#!/usr/bin/env python3
"""Operational-v1 key/Ord/Drop adapter semantics for target 079."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

import target_078_operational_v1 as selection


TARGET = "core::slice::select_nth_unstable_by_key"
INPUT_ORDER = "79"
MODEL_ID = "target-079-key-ord-drop-operational-v1-rust-1.96-complete"
MODEL_VERSION = 1
SOURCE_MODEL_COMPLETE = True
ACTIVE_CONTRACT_SHA256 = (
    "9366859a88badc5f8d8cdfb15fbc544ef81edb756429e14a887b1ce6c73e3e95"
)
ACTIVE_CONJUNCTS = (
    "final-concat",
    "left-length",
    "pivot-at-index",
    "right-length",
    "slice-permutation",
    "key-partition",
)
ADMITTED_TRUST_SITE_IDS = ("TS-079-D004",)
ADAPTER_REPLACED_TRUST_SITE_IDS = ("TS-079-D002",)
ALGORITHM_REPLACED_TRUST_SITE_IDS = ("TS-079-D003", "TS-079-E001")
REPLACED_TRUST_SITE_IDS = (
    *ADAPTER_REPLACED_TRUST_SITE_IDS,
    *ALGORITHM_REPLACED_TRUST_SITE_IDS,
)
MISSING_SOURCE_PHASES: tuple[str, ...] = ()
MODELED_ABORT = "modeled-abort"

SelectionInput = selection.SelectionInput
SourceConfiguration = selection.SourceConfiguration
SelectionExecution = selection.Execution


class BoundaryViolation(ValueError):
    """A supplied total observation returned an inadmissible value."""


class AdapterTermination(str, Enum):
    NORMAL = "normal"
    PANIC = "panic"
    ABORT = "abort"


class KeySlot(int, Enum):
    LEFT = 0
    RIGHT = 1


@dataclass(frozen=True, order=True)
class OwnedKeyIdentity:
    """Identity of one owned K temporary, distinct from its abstract K value."""

    creation_state: int
    slot: KeySlot
    source_identity: int
    key_identity: int


@dataclass(frozen=True)
class KeyObservation:
    key_identity: int
    next_state: int
    panicked: bool


@dataclass(frozen=True)
class OrdLtObservation:
    is_less: bool
    next_state: int
    panicked: bool


@dataclass(frozen=True)
class DropObservation:
    next_state: int
    panicked: bool


KeyFunction = Callable[[int, int], KeyObservation]
OrdLtFunction = Callable[
    [int, OwnedKeyIdentity, OwnedKeyIdentity], OrdLtObservation
]
DropFunction = Callable[[int, OwnedKeyIdentity], DropObservation]
ContractKeyFunction = Callable[[int], int]
ContractOrderingFunction = Callable[[int, int], int]


def _integer_ordering(left: int, right: int) -> int:
    if left < right:
        return selection.LESS
    if left > right:
        return selection.GREATER
    return selection.EQUAL


def _default_key(state: int, value_identity: int) -> KeyObservation:
    return KeyObservation(value_identity, state + 1, False)


def _default_ord_lt(
    state: int,
    left: OwnedKeyIdentity,
    right: OwnedKeyIdentity,
) -> OrdLtObservation:
    return OrdLtObservation(
        left.key_identity < right.key_identity,
        state + 1,
        False,
    )


def _default_drop(
    state: int, _owned_key: OwnedKeyIdentity
) -> DropObservation:
    return DropObservation(state + 1, False)


def _identity_contract_key(value_identity: int) -> int:
    return value_identity


@dataclass(frozen=True)
class AdapterEvent:
    action: str
    state_before: int
    state_after: int
    panicked: bool
    unwinding: bool
    value_identity: int | None = None
    owned_key: OwnedKeyIdentity | None = None
    left_owned_key: OwnedKeyIdentity | None = None
    right_owned_key: OwnedKeyIdentity | None = None
    is_less: bool | None = None


@dataclass(frozen=True)
class AdapterResult:
    termination: AdapterTermination
    final_state: int
    is_less: bool | None
    panic_origin: str | None
    events: tuple[AdapterEvent, ...]


@dataclass(frozen=True)
class KeyOrdDropBoundary:
    """Total state-dependent f, Ord::lt, Drop, and contract observations.

    The callables are immutable Boundary_T fields. They are functions over
    every value in their domain rather than realized-call tables. Owned K
    identity is source-derived from the creation state, operand slot, source
    identity, and abstract key identity; it is not a trace observation.
    """

    callback_identity: int = 79
    key_function_identity: int = 7901
    ord_function_identity: int = 7902
    drop_function_identity: int = 7903
    initial_state: int = 0
    key: KeyFunction = _default_key
    ord_lt: OrdLtFunction = _default_ord_lt
    drop: DropFunction = _default_drop
    contract_key: ContractKeyFunction = _identity_contract_key
    contract_ordering_function: ContractOrderingFunction = _integer_ordering
    enforce_contract_projection: bool = True

    def __post_init__(self) -> None:
        for name in (
            "key",
            "ord_lt",
            "drop",
            "contract_key",
            "contract_ordering_function",
        ):
            if not callable(getattr(self, name)):
                raise TypeError(f"{name} must be a total callable")
        if not isinstance(self.enforce_contract_projection, bool):
            raise TypeError("enforce_contract_projection must be bool")

    @staticmethod
    def _validate_key(observation: KeyObservation) -> None:
        if not isinstance(observation, KeyObservation):
            raise BoundaryViolation("key function must return KeyObservation")
        if not isinstance(observation.key_identity, int):
            raise BoundaryViolation("key identity must be an integer")
        if not isinstance(observation.next_state, int):
            raise BoundaryViolation("key next state must be an integer")
        if not isinstance(observation.panicked, bool):
            raise BoundaryViolation("key panic result must be bool")

    @staticmethod
    def _validate_ord(observation: OrdLtObservation) -> None:
        if not isinstance(observation, OrdLtObservation):
            raise BoundaryViolation(
                "Ord::lt function must return OrdLtObservation"
            )
        if not isinstance(observation.is_less, bool):
            raise BoundaryViolation("Ord::lt result must be bool")
        if not isinstance(observation.next_state, int):
            raise BoundaryViolation("Ord::lt next state must be an integer")
        if not isinstance(observation.panicked, bool):
            raise BoundaryViolation("Ord::lt panic result must be bool")

    @staticmethod
    def _validate_drop(observation: DropObservation) -> None:
        if not isinstance(observation, DropObservation):
            raise BoundaryViolation(
                "Drop function must return DropObservation"
            )
        if not isinstance(observation.next_state, int):
            raise BoundaryViolation("Drop next state must be an integer")
        if not isinstance(observation.panicked, bool):
            raise BoundaryViolation("Drop panic result must be bool")

    def contract_ordering(
        self, left_identity: int, right_identity: int
    ) -> int:
        left_key = self.contract_key(left_identity)
        right_key = self.contract_key(right_identity)
        ordering = self.contract_ordering_function(left_key, right_key)
        if ordering not in (
            selection.LESS,
            selection.EQUAL,
            selection.GREATER,
        ):
            raise BoundaryViolation(
                "contract Ordering must be Less, Equal, or Greater"
            )
        return ordering

    def contract_admissible(self) -> bool:
        return self.enforce_contract_projection

    def transition(
        self, state: int, left_identity: int, right_identity: int
    ) -> AdapterResult:
        events: list[AdapterEvent] = []
        left_owned: OwnedKeyIdentity | None = None
        right_owned: OwnedKeyIdentity | None = None
        current = state
        termination = AdapterTermination.NORMAL
        panic_origin: str | None = None
        is_less: bool | None = None

        def key_step(
            value_identity: int, slot: KeySlot, action: str
        ) -> OwnedKeyIdentity | None:
            nonlocal current, termination, panic_origin
            before = current
            observed = self.key(before, value_identity)
            self._validate_key(observed)
            current = observed.next_state
            owned = None
            if not observed.panicked:
                contract_key = self.contract_key(value_identity)
                if (
                    self.enforce_contract_projection
                    and observed.key_identity != contract_key
                ):
                    raise BoundaryViolation(
                        "runtime f result must project to contract f result"
                    )
                owned = OwnedKeyIdentity(
                    before,
                    slot,
                    value_identity,
                    observed.key_identity,
                )
            else:
                termination = AdapterTermination.PANIC
                panic_origin = action
            events.append(
                AdapterEvent(
                    action=action,
                    state_before=before,
                    state_after=current,
                    panicked=observed.panicked,
                    unwinding=False,
                    value_identity=value_identity,
                    owned_key=owned,
                )
            )
            return owned

        def ord_step() -> None:
            nonlocal current, termination, panic_origin, is_less
            assert left_owned is not None
            assert right_owned is not None
            before = current
            observed = self.ord_lt(before, left_owned, right_owned)
            self._validate_ord(observed)
            if self.enforce_contract_projection:
                expected = (
                    self.contract_ordering_function(
                        left_owned.key_identity,
                        right_owned.key_identity,
                    )
                    == selection.LESS
                )
                if observed.is_less != expected:
                    raise BoundaryViolation(
                        "runtime Ord::lt must project to contract Ordering"
                    )
            current = observed.next_state
            events.append(
                AdapterEvent(
                    action="ord-lt",
                    state_before=before,
                    state_after=current,
                    panicked=observed.panicked,
                    unwinding=False,
                    left_owned_key=left_owned,
                    right_owned_key=right_owned,
                    is_less=observed.is_less,
                )
            )
            if observed.panicked:
                termination = AdapterTermination.PANIC
                panic_origin = "ord-lt"
            else:
                is_less = observed.is_less

        def drop_step(
            owned: OwnedKeyIdentity, action: str
        ) -> None:
            nonlocal current, termination, panic_origin
            if termination == AdapterTermination.ABORT:
                return
            before = current
            unwinding = termination == AdapterTermination.PANIC
            observed = self.drop(before, owned)
            self._validate_drop(observed)
            current = observed.next_state
            events.append(
                AdapterEvent(
                    action=action,
                    state_before=before,
                    state_after=current,
                    panicked=observed.panicked,
                    unwinding=unwinding,
                    owned_key=owned,
                )
            )
            if observed.panicked:
                if unwinding:
                    termination = AdapterTermination.ABORT
                else:
                    termination = AdapterTermination.PANIC
                panic_origin = action

        left_owned = key_step(
            left_identity, KeySlot.LEFT, "key-left"
        )
        if termination == AdapterTermination.NORMAL:
            right_owned = key_step(
                right_identity, KeySlot.RIGHT, "key-right"
            )
        if termination == AdapterTermination.NORMAL:
            ord_step()
        if right_owned is not None:
            drop_step(right_owned, "drop-right")
        if left_owned is not None:
            drop_step(left_owned, "drop-left")

        if termination != AdapterTermination.NORMAL:
            is_less = None
        return AdapterResult(
            termination=termination,
            final_state=current,
            is_less=is_less,
            panic_origin=panic_origin,
            events=tuple(events),
        )

    def observe(
        self, state: int, left_identity: int, right_identity: int
    ) -> selection.ComparatorObservation:
        """Compatibility projection for non-aborting direct engine use."""

        result = self.transition(state, left_identity, right_identity)
        if result.termination == AdapterTermination.ABORT:
            raise BoundaryViolation(
                "aborting adapters require target-079 execute()"
            )
        return selection.ComparatorObservation(
            ordering=(
                selection.LESS
                if result.is_less
                else selection.EQUAL
            ),
            next_state=result.final_state,
            panicked=result.termination == AdapterTermination.PANIC,
        )


@dataclass(frozen=True)
class OperationalExecution:
    selection: SelectionExecution
    adapter_invocations: tuple[tuple[str, AdapterResult], ...]
    termination: AdapterTermination
    panic_origin: str | None = None


class _AdapterAbortSignal(BaseException):
    def __init__(self, phase: str, result: AdapterResult) -> None:
        super().__init__(phase)
        self.phase = phase
        self.result = result


class _AdapterEngine(selection._Engine):
    """Read-only reuse of every accepted target-078 selection helper."""

    def __init__(
        self,
        selection_input: SelectionInput,
        boundary: KeyOrdDropBoundary,
    ) -> None:
        super().__init__(selection_input, boundary)
        self.boundary = boundary
        self.adapter_invocations: list[tuple[str, AdapterResult]] = []

    def is_less(
        self, left_identity: int, right_identity: int, phase: str
    ) -> bool:
        state_before = self.callback_state
        result = self.boundary.transition(
            state_before, left_identity, right_identity
        )
        self.callback_state = result.final_state
        self.adapter_invocations.append((phase, result))
        self.record(
            "callback",
            phase,
            adapter_termination=result.termination.value,
            left_identity=left_identity,
            next_state=result.final_state,
            ordering=(
                selection.LESS
                if result.is_less
                else selection.EQUAL
            ),
            panicked=result.termination != AdapterTermination.NORMAL,
            right_identity=right_identity,
            state=state_before,
        )
        if result.termination == AdapterTermination.ABORT:
            raise _AdapterAbortSignal(phase, result)
        if result.termination == AdapterTermination.PANIC:
            raise selection._CallbackPanic(phase)
        assert result.is_less is not None
        return result.is_less


def _execution(
    engine: _AdapterEngine,
    *,
    coverage_status: str,
    branch: str,
    termination: AdapterTermination,
    output: selection.SelectionOutput | None,
    panic_phase: str | None = None,
    panic_origin: str | None = None,
) -> OperationalExecution:
    selected = selection.Execution(
        coverage_status=coverage_status,
        branch=branch,
        output=output,
        final_state=engine.final_state(
            panicked=termination != AdapterTermination.NORMAL
        ),
        derived_events=tuple(engine.events),
        panic_phase=panic_phase,
    )
    return OperationalExecution(
        selection=selected,
        adapter_invocations=tuple(engine.adapter_invocations),
        termination=termination,
        panic_origin=panic_origin,
    )


def execute(
    selection_input: SelectionInput, boundary: KeyOrdDropBoundary
) -> OperationalExecution:
    """Compose the adapter termination sum through accepted selection code.

    Ordinary callback panic is re-raised as target 078's private panic signal,
    so CopyOnDrop and partition gap guards restore exactly as accepted.
    Adapter abort uses a distinct BaseException signal; those handlers do not
    catch it, so execution retains the interrupted sequence and state without
    running any Rust cleanup that process termination would bypass.
    """

    if selection.MODEL_ID != (
        "target-078-operational-v1-rust-1.96-complete"
    ):
        raise RuntimeError("accepted target-078 engine identity changed")

    engine = _AdapterEngine(selection_input, boundary)
    length = len(engine.sequence)
    index = selection_input.index
    branch = "bounds"

    try:
        if not selection.requires_t(selection_input):
            engine.record(
                "branch",
                "partition-at-index",
                branch="bounds-panic",
                index=index,
                length=length,
            )
            return _execution(
                engine,
                coverage_status=selection.MODELED_PANIC,
                branch="bounds-panic",
                termination=AdapterTermination.PANIC,
                output=None,
                panic_phase="bounds",
                panic_origin="bounds",
            )

        if selection_input.is_zst:
            branch = "zst"
            engine.record("branch", "partition-at-index", branch=branch)
        elif index == length - 1:
            branch = "max-scan"
            engine.record("branch", "partition-at-index", branch=branch)
            winner = selection._extreme_scan(
                engine,
                0,
                length,
                find_min=False,
                phase="max-index",
            )
            engine.swap(winner, index, "max-index-final-swap")
        elif index == 0:
            branch = "min-scan"
            engine.record("branch", "partition-at-index", branch=branch)
            winner = selection._extreme_scan(
                engine,
                0,
                length,
                find_min=True,
                phase="min-index",
            )
            engine.swap(winner, index, "min-index-final-swap")
        elif selection_input.configuration.optimize_for_size:
            branch = "optimize-for-size"
            engine.record(
                "branch",
                "partition-at-index",
                branch="median-of-medians",
            )
            selection._median_of_medians(
                engine,
                0,
                length,
                index,
                phase="optimize-for-size",
            )
        else:
            branch = "introselect"
            engine.record(
                "branch",
                "partition-at-index",
                branch="partition-at-index-loop",
            )
            terminal = selection._partition_at_index_loop(engine, index)
            if terminal == "insertion-sort":
                branch = terminal
            engine.record(
                "introselect-return",
                "partition-at-index-loop",
                terminal=terminal,
            )
    except selection._CallbackPanic as panic:
        invocation = (
            engine.adapter_invocations[-1][1]
            if engine.adapter_invocations
            else None
        )
        return _execution(
            engine,
            coverage_status=selection.MODELED_PANIC,
            branch=branch,
            termination=AdapterTermination.PANIC,
            output=None,
            panic_phase=panic.phase,
            panic_origin=(
                invocation.panic_origin if invocation is not None else None
            ),
        )
    except _AdapterAbortSignal as abort:
        return _execution(
            engine,
            coverage_status=MODELED_ABORT,
            branch=branch,
            termination=AdapterTermination.ABORT,
            output=None,
            panic_phase=abort.phase,
            panic_origin=abort.result.panic_origin,
        )

    return _execution(
        engine,
        coverage_status=selection.MODELED_NORMAL,
        branch=branch,
        termination=AdapterTermination.NORMAL,
        output=selection._output(selection_input, engine.sequence),
    )


def active_contract_conjuncts(
    selection_input: SelectionInput,
    boundary: KeyOrdDropBoundary,
    execution: OperationalExecution,
) -> dict[str, bool]:
    accepted = selection.active_contract_conjuncts(
        selection_input, boundary, execution.selection
    )
    return {
        name: accepted[
            "callback-partition"
            if name == "key-partition"
            else name
        ]
        for name in ACTIVE_CONJUNCTS
    }


def active_contract_holds(
    selection_input: SelectionInput,
    boundary: KeyOrdDropBoundary,
    execution: OperationalExecution,
) -> bool:
    return (
        boundary.contract_admissible()
        and execution.termination == AdapterTermination.NORMAL
        and all(
            active_contract_conjuncts(
                selection_input, boundary, execution
            ).values()
        )
    )


def exact_equivalent(
    first: OperationalExecution, second: OperationalExecution
) -> bool:
    return (
        first.termination == second.termination
        and selection.exact_equivalent(
            first.selection, second.selection
        )
    )


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 2,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "source_model_complete": SOURCE_MODEL_COMPLETE,
        "classification_eligible": True,
        "admitted_trust_site_ids": list(ADMITTED_TRUST_SITE_IDS),
        "adapter_replaced_trust_site_ids": list(
            ADAPTER_REPLACED_TRUST_SITE_IDS
        ),
        "algorithm_replaced_trust_site_ids": list(
            ALGORITHM_REPLACED_TRUST_SITE_IDS
        ),
        "unresolved_trust_site_ids": [],
        "selection_engine": {
            "module": "tools/target_078_operational_v1.py",
            "model_id": selection.MODEL_ID,
            "reuse": (
                "read-only source-backed dispatch, insertion, pivot, "
                "partition, narrowing, fallback, restoration, and return"
            ),
            "classification_inherited": False,
        },
        "shared_boundary_observations": [
            "callback, key-function, Ord, and Drop identities",
            "initial callback-visible state",
            (
                "total key(state,value) abstract-key, next-state, and "
                "panic functions"
            ),
            (
                "total Ord::lt(state,left-owned-key,right-owned-key) "
                "result, next-state, and panic functions"
            ),
            (
                "total Drop(state,owned-key) next-state and panic "
                "functions"
            ),
            "state-independent contract key and total Ordering functions",
        ],
        "owned_key_identity": {
            "fields": [
                "creation state",
                "left/right operand slot",
                "source value identity",
                "abstract key identity",
            ],
            "role": (
                "source-derived identity for each live owned K temporary; "
                "equal abstract keys remain separately destructible"
            ),
            "boundary_observation": False,
        },
        "excluded_from_boundary": [
            "realized calls or invocation count",
            "temporary lifetime or drop schedule",
            "selection branches, pivots, swaps, and mutations",
            "returned references, selected answer, or final state",
            "execution trace",
        ],
        "adapter_evaluation_order": [
            "f(left)",
            "f(right)",
            "K::lt(&left_key,&right_key)",
            "drop(right_owned_key)",
            "drop(left_owned_key)",
        ],
        "termination_composition": {
            "normal": "selection consumes Ord::lt and continues",
            "panic": (
                "accepted target-078 CopyOnDrop and gap-guard unwind "
                "restoration runs"
            ),
            "abort": (
                "distinct termination bypasses ordinary unwind and retains "
                "the interrupted full selection state"
            ),
        },
        "classification_boundary_requirement": (
            "runtime key results and Ord::lt observations project exactly "
            "to the state-independent contract key total order"
        ),
        "equivalence": (
            "exact termination, principal return, and full "
            "final/interrupted state; traces and panic origin are internal"
        ),
    }
