#!/usr/bin/env python3
"""Source-operational Rust 1.96 model for target 081."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import target_080_operational_v1 as private_sort


TARGET = "core::slice::sort_unstable_by"
INPUT_ORDER = "81"
MODEL_ID = "target-081-operational-v1-rust-1.96-complete"
MODEL_VERSION = 1
ACTIVE_CONTRACT_SHA256 = (
    "420e250d3b0ae471b64eb3d6474588eaec8acfc7644b5c1dd4420e4c1b2c0597"
)

ADMITTED_TRUST_SITE_IDS = ("TS-081-D004",)
REPLACED_TRUST_SITE_IDS = (
    "TS-081-D002",
    "TS-081-D003",
    "TS-081-E001",
)
CONTEXT_ONLY_TRUST_SITE_IDS = ("TS-081-D001", "TS-081-C001")
PENDING_REPLACEMENT_TRUST_SITE_IDS: tuple[str, ...] = ()
SOURCE_MODEL_COMPLETE = True
CLASSIFICATION_ELIGIBLE = True

LESS = -1
EQUAL = 0
GREATER = 1
ORDERINGS = (LESS, EQUAL, GREATER)

IDENTITY_TOTAL_ORDER = "identity-total-order"
RANK_TOTAL_ORDER = "rank-total-order"
CONSTANT_EQUAL = "constant-equal"
EXPLICIT_ORDERING = "explicit-ordering"
STATE_PARITY_ORDER = "state-parity-order"
INTERIOR_PARITY_ORDER = "interior-parity-order"

INCREMENT_STATE = private_sort.INCREMENT_STATE
IDENTITY_STATE = private_sort.IDENTITY_STATE
AFFINE_STATE = private_sort.AFFINE_STATE

NORMAL = private_sort.NORMAL
PANIC = private_sort.PANIC
ABORT = private_sort.ABORT

SourceConfiguration = private_sort.SourceConfiguration
SortInput = private_sort.SortInput

COVERED_SOURCE_PHASES = (
    "public sort_unstable_by adapter evaluates compare(a,b) exactly once",
    "Ordering::Less projection after successful callback evaluation",
    "callback state and panic propagation into private is_less",
    "externally observable element interior-mutation state on return and panic",
    "callback-value destruction after normal private-sort return",
    "callback-value destruction during comparator-panic unwind",
    "normal drop panic and double-panic abort distinction",
    *private_sort.COVERED_SOURCE_PHASES[1:],
)
MISSING_SOURCE_PHASES: tuple[str, ...] = ()


class BoundaryViolation(ValueError):
    pass


@dataclass(frozen=True, order=True)
class ObservationKey:
    state: int
    left_identity: int
    right_identity: int


@dataclass(frozen=True)
class ComparatorObservation:
    ordering: int
    next_state: int
    next_observable_element_state: tuple[int, ...]
    panicked: bool


@dataclass(frozen=True)
class DropObservation:
    next_state: int
    next_observable_element_state: tuple[int, ...]
    panicked: bool


@dataclass(frozen=True)
class ComparatorBoundary:
    """Total callback and callback-destruction observations."""

    callback_identity: int
    initial_state: int
    ordering_mode: str
    next_state_mode: str
    contract_ordering_mode: str | None
    initial_observable_element_state: tuple[int, ...] = ()
    interior_next_state_mode: str = IDENTITY_STATE
    interior_affine_multiplier: int = 1
    interior_affine_offset: int = 0
    rank_pairs: tuple[tuple[int, int], ...] = ()
    explicit_orderings: tuple[tuple[int, int, int], ...] = ()
    affine_multiplier: int = 1
    affine_offset: int = 1
    panic_states: frozenset[int] = frozenset()
    panic_keys: frozenset[ObservationKey] = frozenset()
    drop_next_state_mode: str = IDENTITY_STATE
    drop_affine_multiplier: int = 1
    drop_affine_offset: int = 0
    drop_interior_next_state_mode: str = IDENTITY_STATE
    drop_interior_affine_multiplier: int = 1
    drop_interior_affine_offset: int = 0
    drop_panic_normal_states: frozenset[int] = frozenset()
    drop_panic_unwind_states: frozenset[int] = frozenset()

    def __post_init__(self) -> None:
        modes = {
            IDENTITY_TOTAL_ORDER,
            RANK_TOTAL_ORDER,
            CONSTANT_EQUAL,
            EXPLICIT_ORDERING,
            STATE_PARITY_ORDER,
            INTERIOR_PARITY_ORDER,
        }
        if self.ordering_mode not in modes:
            raise BoundaryViolation("unknown comparator Ordering mode")
        if (
            self.contract_ordering_mode is not None
            and self.contract_ordering_mode
            not in modes - {STATE_PARITY_ORDER, INTERIOR_PARITY_ORDER}
        ):
            raise BoundaryViolation("invalid comparator_observation projection")
        state_modes = {INCREMENT_STATE, IDENTITY_STATE, AFFINE_STATE}
        if self.next_state_mode not in state_modes:
            raise BoundaryViolation("unknown callback-state mode")
        if self.drop_next_state_mode not in state_modes:
            raise BoundaryViolation("unknown callback-drop state mode")
        if self.interior_next_state_mode not in state_modes:
            raise BoundaryViolation("unknown element-interior state mode")
        if self.drop_interior_next_state_mode not in state_modes:
            raise BoundaryViolation(
                "unknown callback-drop element-interior state mode"
            )
        if not isinstance(self.initial_observable_element_state, tuple):
            raise TypeError(
                "initial_observable_element_state must be a tuple"
            )
        if any(
            not isinstance(value, int)
            for value in self.initial_observable_element_state
        ):
            raise TypeError(
                "observable element-interior state values must be integers"
            )
        identities = [identity for identity, _ in self.rank_pairs]
        if len(identities) != len(set(identities)):
            raise BoundaryViolation("rank identities must be unique")
        explicit_keys = [
            (left, right) for left, right, _ in self.explicit_orderings
        ]
        if len(explicit_keys) != len(set(explicit_keys)):
            raise BoundaryViolation("explicit comparator keys must be unique")
        if any(
            ordering not in ORDERINGS
            for _, _, ordering in self.explicit_orderings
        ):
            raise BoundaryViolation("invalid explicit Ordering result")
        if not isinstance(self.panic_states, frozenset):
            raise TypeError("panic_states must be a frozenset")
        if not isinstance(self.panic_keys, frozenset):
            raise TypeError("panic_keys must be a frozenset")
        if not isinstance(self.drop_panic_normal_states, frozenset):
            raise TypeError("drop_panic_normal_states must be a frozenset")
        if not isinstance(self.drop_panic_unwind_states, frozenset):
            raise TypeError("drop_panic_unwind_states must be a frozenset")

    def _rank(self, identity: int) -> tuple[int, int]:
        ranks = dict(self.rank_pairs)
        if identity in ranks:
            return (0, ranks[identity])
        return (1, identity)

    def _ordering(
        self,
        mode: str,
        state: int,
        left_identity: int,
        right_identity: int,
        observable_element_state: tuple[int, ...],
    ) -> int:
        if mode == IDENTITY_TOTAL_ORDER:
            left_key = left_identity
            right_key = right_identity
        elif mode in (
            RANK_TOTAL_ORDER,
            STATE_PARITY_ORDER,
            INTERIOR_PARITY_ORDER,
        ):
            left_key = self._rank(left_identity)
            right_key = self._rank(right_identity)
            if mode == STATE_PARITY_ORDER and state % 2:
                left_key, right_key = right_key, left_key
            if (
                mode == INTERIOR_PARITY_ORDER
                and sum(observable_element_state) % 2
            ):
                left_key, right_key = right_key, left_key
        elif mode == CONSTANT_EQUAL:
            return EQUAL
        elif mode == EXPLICIT_ORDERING:
            explicit = {
                (left, right): ordering
                for left, right, ordering in self.explicit_orderings
            }
            if (left_identity, right_identity) in explicit:
                return explicit[(left_identity, right_identity)]
            left_key = left_identity
            right_key = right_identity
        else:
            raise BoundaryViolation(f"unsupported Ordering mode: {mode}")
        if left_key < right_key:
            return LESS
        if left_key > right_key:
            return GREATER
        return EQUAL

    @staticmethod
    def _next_state(
        mode: str,
        state: int,
        multiplier: int,
        offset: int,
    ) -> int:
        if mode == INCREMENT_STATE:
            return state + 1
        if mode == IDENTITY_STATE:
            return state
        if mode == AFFINE_STATE:
            return multiplier * state + offset
        raise BoundaryViolation(f"unsupported state mode: {mode}")

    @classmethod
    def _next_observable_element_state(
        cls,
        mode: str,
        state: tuple[int, ...],
        multiplier: int,
        offset: int,
    ) -> tuple[int, ...]:
        return tuple(
            cls._next_state(mode, value, multiplier, offset)
            for value in state
        )

    def observe(
        self,
        state: int,
        left_identity: int,
        right_identity: int,
        observable_element_state: tuple[int, ...] | None = None,
    ) -> ComparatorObservation:
        if observable_element_state is None:
            observable_element_state = (
                self.initial_observable_element_state
            )
        key = ObservationKey(state, left_identity, right_identity)
        observation = ComparatorObservation(
            ordering=self._ordering(
                self.ordering_mode,
                state,
                left_identity,
                right_identity,
                observable_element_state,
            ),
            next_state=self._next_state(
                self.next_state_mode,
                state,
                self.affine_multiplier,
                self.affine_offset,
            ),
            next_observable_element_state=(
                self._next_observable_element_state(
                    self.interior_next_state_mode,
                    observable_element_state,
                    self.interior_affine_multiplier,
                    self.interior_affine_offset,
                )
            ),
            panicked=state in self.panic_states or key in self.panic_keys,
        )
        if observation.ordering not in ORDERINGS:
            raise BoundaryViolation("callback returned an invalid Ordering")
        return observation

    def observe_drop(
        self,
        state: int,
        observable_element_state: tuple[int, ...],
        *,
        unwinding: bool,
    ) -> DropObservation:
        panic_states = (
            self.drop_panic_unwind_states
            if unwinding
            else self.drop_panic_normal_states
        )
        return DropObservation(
            next_state=self._next_state(
                self.drop_next_state_mode,
                state,
                self.drop_affine_multiplier,
                self.drop_affine_offset,
            ),
            next_observable_element_state=(
                self._next_observable_element_state(
                    self.drop_interior_next_state_mode,
                    observable_element_state,
                    self.drop_interior_affine_multiplier,
                    self.drop_interior_affine_offset,
                )
            ),
            panicked=state in panic_states,
        )

    def contract_ordering(
        self, left_identity: int, right_identity: int
    ) -> int:
        if self.contract_ordering_mode is None:
            raise BoundaryViolation(
                "boundary has no comparator_observation projection"
            )
        return self._ordering(
            self.contract_ordering_mode,
            self.initial_state,
            left_identity,
            right_identity,
            self.initial_observable_element_state,
        )

    def contract_admissible(self) -> bool:
        return (
            self.contract_ordering_mode is not None
            and self.contract_ordering_mode == self.ordering_mode
            and self.ordering_mode
            not in {STATE_PARITY_ORDER, INTERIOR_PARITY_ORDER}
        )


@dataclass(frozen=True)
class AdapterEvent:
    state: int
    observable_element_state_before: tuple[int, ...]
    left_identity: int
    right_identity: int
    ordering: int
    next_state: int
    observable_element_state_after: tuple[int, ...]
    panicked: bool
    callback_evaluations: int
    less_tested: bool
    is_less: bool


class OrderingToLessAdapter:
    """The exact `compare(a, b) == Ordering::Less` source adapter."""

    def __init__(self, boundary: ComparatorBoundary) -> None:
        self.boundary = boundary
        self.callback_identity = boundary.callback_identity
        self.initial_state = boundary.initial_state
        self.observable_element_state = (
            boundary.initial_observable_element_state
        )
        self.events: list[AdapterEvent] = []

    def observe(
        self, state: int, left_identity: int, right_identity: int
    ) -> private_sort.OrdObservation:
        before = self.observable_element_state
        observation = self.boundary.observe(
            state,
            left_identity,
            right_identity,
            before,
        )
        self.observable_element_state = (
            observation.next_observable_element_state
        )
        is_less = (
            not observation.panicked and observation.ordering == LESS
        )
        self.events.append(
            AdapterEvent(
                state=state,
                observable_element_state_before=before,
                left_identity=left_identity,
                right_identity=right_identity,
                ordering=observation.ordering,
                next_state=observation.next_state,
                observable_element_state_after=(
                    observation.next_observable_element_state
                ),
                panicked=observation.panicked,
                callback_evaluations=1,
                less_tested=not observation.panicked,
                is_less=is_less,
            )
        )
        return private_sort.OrdObservation(
            is_less=is_less,
            next_state=observation.next_state,
            panicked=observation.panicked,
        )

    def contract_admissible(self) -> bool:
        return self.boundary.contract_admissible()

    def contract_is_less(
        self, left_identity: int, right_identity: int
    ) -> bool:
        return (
            self.boundary.contract_ordering(left_identity, right_identity)
            == LESS
        )


@dataclass(frozen=True)
class FinalState:
    sequence: tuple[int, ...]
    callback_state: int
    observable_element_state: tuple[int, ...]
    panicked: bool
    aborted: bool
    terminal: bool
    callback_drop_invoked: bool
    callback_drop_completed: bool


@dataclass(frozen=True)
class Execution:
    state: FinalState
    terminal_status: str
    unit_returned: bool
    private_terminal_status: str
    panic_phase: str | None
    abort_phase: str | None
    adapter_events: tuple[AdapterEvent, ...]
    comparator_observation: tuple[tuple[int, int, int, int], ...]
    private_steps: tuple[private_sort.DerivedStep, ...]


def _project_comparator_observation(
    events: tuple[AdapterEvent, ...],
) -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        (
            event.state,
            event.left_identity,
            event.right_identity,
            event.ordering,
        )
        for event in events
    )


def _finish_public_execution(
    private: private_sort.Execution,
    adapter: OrderingToLessAdapter,
    boundary: ComparatorBoundary,
) -> Execution:
    status = private.terminal_status
    callback_state = private.state.callback_state
    observable_element_state = adapter.observable_element_state
    panic_phase = private.panic_phase
    abort_phase = private.abort_phase
    drop_invoked = False
    drop_completed = False

    if status != ABORT:
        drop_invoked = True
        unwinding = status == PANIC
        drop = boundary.observe_drop(
            callback_state,
            observable_element_state,
            unwinding=unwinding,
        )
        callback_state = drop.next_state
        observable_element_state = (
            drop.next_observable_element_state
        )
        drop_completed = not drop.panicked
        if drop.panicked:
            if unwinding:
                status = ABORT
                abort_phase = "callback-drop-during-unwind"
            else:
                status = PANIC
                panic_phase = "callback-drop-after-normal-sort"

    events = tuple(adapter.events)
    if any(event.callback_evaluations != 1 for event in events):
        raise RuntimeError("source adapter evaluated compare more than once")
    private_callbacks = sum(
        step.kind == "ord-lt" for step in private.derived_steps
    )
    if private_callbacks != len(events):
        raise RuntimeError("adapter/private callback count diverged")

    return Execution(
        state=FinalState(
            sequence=private.state.sequence,
            callback_state=callback_state,
            observable_element_state=observable_element_state,
            panicked=status == PANIC,
            aborted=status == ABORT,
            terminal=True,
            callback_drop_invoked=drop_invoked,
            callback_drop_completed=drop_completed,
        ),
        terminal_status=status,
        unit_returned=status == NORMAL,
        private_terminal_status=private.terminal_status,
        panic_phase=panic_phase,
        abort_phase=abort_phase,
        adapter_events=events,
        comparator_observation=_project_comparator_observation(events),
        private_steps=private.derived_steps,
    )


def execute(
    sort_input: SortInput, boundary: ComparatorBoundary
) -> Execution:
    adapter = OrderingToLessAdapter(boundary)
    private = private_sort.execute(sort_input, adapter)
    return _finish_public_execution(private, adapter, boundary)


def integer_total_order_boundary(
    *,
    initial_state: int = 0,
    initial_observable_element_state: tuple[int, ...] = (),
    next_state_mode: str = INCREMENT_STATE,
    affine_multiplier: int = 1,
    affine_offset: int = 1,
    interior_next_state_mode: str = IDENTITY_STATE,
    interior_affine_multiplier: int = 1,
    interior_affine_offset: int = 0,
    panic_states: frozenset[int] = frozenset(),
    panic_keys: frozenset[ObservationKey] = frozenset(),
    drop_next_state_mode: str = IDENTITY_STATE,
    drop_affine_multiplier: int = 1,
    drop_affine_offset: int = 0,
    drop_interior_next_state_mode: str = IDENTITY_STATE,
    drop_interior_affine_multiplier: int = 1,
    drop_interior_affine_offset: int = 0,
    drop_panic_normal_states: frozenset[int] = frozenset(),
    drop_panic_unwind_states: frozenset[int] = frozenset(),
) -> ComparatorBoundary:
    return ComparatorBoundary(
        callback_identity=81,
        initial_state=initial_state,
        ordering_mode=IDENTITY_TOTAL_ORDER,
        next_state_mode=next_state_mode,
        contract_ordering_mode=IDENTITY_TOTAL_ORDER,
        initial_observable_element_state=(
            initial_observable_element_state
        ),
        interior_next_state_mode=interior_next_state_mode,
        interior_affine_multiplier=interior_affine_multiplier,
        interior_affine_offset=interior_affine_offset,
        affine_multiplier=affine_multiplier,
        affine_offset=affine_offset,
        panic_states=panic_states,
        panic_keys=panic_keys,
        drop_next_state_mode=drop_next_state_mode,
        drop_affine_multiplier=drop_affine_multiplier,
        drop_affine_offset=drop_affine_offset,
        drop_interior_next_state_mode=drop_interior_next_state_mode,
        drop_interior_affine_multiplier=(
            drop_interior_affine_multiplier
        ),
        drop_interior_affine_offset=drop_interior_affine_offset,
        drop_panic_normal_states=drop_panic_normal_states,
        drop_panic_unwind_states=drop_panic_unwind_states,
    )


def rank_total_order_boundary(
    class_ranks: Mapping[int, int],
    **kwargs: Any,
) -> ComparatorBoundary:
    boundary = integer_total_order_boundary(**kwargs)
    return ComparatorBoundary(
        **{
            **boundary.__dict__,
            "ordering_mode": RANK_TOTAL_ORDER,
            "contract_ordering_mode": RANK_TOTAL_ORDER,
            "rank_pairs": tuple(sorted(class_ranks.items())),
        }
    )


def explicit_ordering_boundary(
    orderings: Mapping[tuple[int, int], int],
    *,
    initial_state: int = 0,
    initial_observable_element_state: tuple[int, ...] = (),
    next_state_mode: str = INCREMENT_STATE,
    affine_multiplier: int = 1,
    affine_offset: int = 1,
    interior_next_state_mode: str = IDENTITY_STATE,
    interior_affine_multiplier: int = 1,
    interior_affine_offset: int = 0,
    panic_states: frozenset[int] = frozenset(),
    panic_keys: frozenset[ObservationKey] = frozenset(),
    drop_next_state_mode: str = IDENTITY_STATE,
    drop_affine_multiplier: int = 1,
    drop_affine_offset: int = 0,
    drop_interior_next_state_mode: str = IDENTITY_STATE,
    drop_interior_affine_multiplier: int = 1,
    drop_interior_affine_offset: int = 0,
    drop_panic_normal_states: frozenset[int] = frozenset(),
    drop_panic_unwind_states: frozenset[int] = frozenset(),
) -> ComparatorBoundary:
    return ComparatorBoundary(
        callback_identity=81,
        initial_state=initial_state,
        ordering_mode=EXPLICIT_ORDERING,
        next_state_mode=next_state_mode,
        contract_ordering_mode=EXPLICIT_ORDERING,
        initial_observable_element_state=(
            initial_observable_element_state
        ),
        interior_next_state_mode=interior_next_state_mode,
        interior_affine_multiplier=interior_affine_multiplier,
        interior_affine_offset=interior_affine_offset,
        explicit_orderings=tuple(
            sorted(
                (left, right, ordering)
                for (left, right), ordering in orderings.items()
            )
        ),
        affine_multiplier=affine_multiplier,
        affine_offset=affine_offset,
        panic_states=panic_states,
        panic_keys=panic_keys,
        drop_next_state_mode=drop_next_state_mode,
        drop_affine_multiplier=drop_affine_multiplier,
        drop_affine_offset=drop_affine_offset,
        drop_interior_next_state_mode=drop_interior_next_state_mode,
        drop_interior_affine_multiplier=(
            drop_interior_affine_multiplier
        ),
        drop_interior_affine_offset=drop_interior_affine_offset,
        drop_panic_normal_states=drop_panic_normal_states,
        drop_panic_unwind_states=drop_panic_unwind_states,
    )


def state_dependent_boundary(
    class_ranks: Mapping[int, int],
    **kwargs: Any,
) -> ComparatorBoundary:
    boundary = integer_total_order_boundary(**kwargs)
    return ComparatorBoundary(
        **{
            **boundary.__dict__,
            "ordering_mode": STATE_PARITY_ORDER,
            "contract_ordering_mode": None,
            "rank_pairs": tuple(sorted(class_ranks.items())),
        }
    )


def interior_state_dependent_boundary(
    class_ranks: Mapping[int, int],
    **kwargs: Any,
) -> ComparatorBoundary:
    boundary = integer_total_order_boundary(**kwargs)
    return ComparatorBoundary(
        **{
            **boundary.__dict__,
            "ordering_mode": INTERIOR_PARITY_ORDER,
            "contract_ordering_mode": None,
            "rank_pairs": tuple(sorted(class_ranks.items())),
        }
    )


def sequence_is_permutation(
    execution: Execution, before: tuple[int, ...]
) -> bool:
    return Counter(execution.state.sequence) == Counter(before)


def sequence_is_contract_sorted(
    execution: Execution, boundary: ComparatorBoundary
) -> bool:
    if not boundary.contract_admissible():
        raise BoundaryViolation(
            "contract sortedness needs a comparator_observation projection"
        )
    sequence = execution.state.sequence
    return all(
        boundary.contract_ordering(right, left) != LESS
        for left, right in zip(sequence, sequence[1:])
    )


def exact_equivalent(first: Execution, second: Execution) -> bool:
    return (
        first.state == second.state
        and first.terminal_status == second.terminal_status
        and first.unit_returned == second.unit_returned
        and first.private_terminal_status == second.private_terminal_status
        and first.panic_phase == second.panic_phase
        and first.abort_phase == second.abort_phase
        and first.comparator_observation == second.comparator_observation
    )


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "model_id": MODEL_ID,
        "admitted_trust_site_ids": list(ADMITTED_TRUST_SITE_IDS),
        "replaced_trust_site_ids": list(REPLACED_TRUST_SITE_IDS),
        "context_only_trust_site_ids": list(CONTEXT_ONLY_TRUST_SITE_IDS),
        "pending_replacement_trust_site_ids": [],
        "boundary_narrower_than_target": True,
        "source_adapter": (
            "one compare(a,b) evaluation; on success test Ordering::Less"
        ),
        "comparator_observation_projection": (
            "each source-derived callback event projects its state, operands, "
            "and exact Ordering to comparator_observation"
        ),
        "callback_lifecycle": (
            "compare is dropped once after normal return or during unwind; "
            "drop panic during unwind is modeled as abort"
        ),
        "externally_observable_state": (
            "observable_element_state is distinct from callback_state and "
            "contains the complete element interior-mutation state, indexed "
            "by stable observable-cell identity; callback and Drop "
            "transitions update it before either normal return or panic "
            "becomes observable"
        ),
        "shared_boundary_observations": [
            "total compare Ordering(state,left_identity,right_identity)",
            "total compare next_state(state,left_identity,right_identity)",
            (
                "total compare next observable element interior state"
                "(state,left_identity,right_identity,current interior state)"
            ),
            "total compare panic(state,left_identity,right_identity)",
            "total callback Drop next_state(state,unwinding)",
            (
                "total callback Drop next observable element interior state"
                "(state,unwinding,current interior state)"
            ),
            "total callback Drop panic(state,unwinding)",
        ],
        "source_derived_observations": [
            "callback evaluation count and operand order",
            "Ordering::Less branch result",
            "comparison schedule",
            "callback destruction point and unwind mode",
            "private-sort pivots, partitions, swaps, writes, and restoration",
            "terminal status, output sequence, and final callback state",
            "final externally observable element interior-mutation state",
        ],
        "prohibited_boundary_observations": [
            "realized comparison schedule or prior comparisons",
            "pivot, partition, swap, or write choice",
            "selected output or permutation",
            "aggregate final state",
            "target execution trace",
            "precomputed terminal result",
        ],
        "trust_site_dispositions": {
            "TS-081-D001": "context-only-generated-contract-vocabulary",
            "TS-081-D002": "replaced-by-source-ordering-to-less-adapter",
            "TS-081-D003": "replaced-by-accepted-private-source-transitions",
            "TS-081-D004": "admitted-total-callback-and-drop-observations",
            "TS-081-C001": "context-only-direct-call-identity",
            "TS-081-E001": "replaced-by-accepted-private-source-transitions",
        },
    }
