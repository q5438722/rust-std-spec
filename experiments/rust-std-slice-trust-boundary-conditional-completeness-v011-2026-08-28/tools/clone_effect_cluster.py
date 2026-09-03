#!/usr/bin/env python3
"""Source-backed conditional-completeness models for targets 037 and 043."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

CANONICAL_SLICE_PATH = "core/src/slice/mod.rs"
CANONICAL_SLICE_SHA256 = (
    "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
)
SPECIALIZE_PATH = "core/src/slice/specialize.rs"
SPECIALIZE_SHA256 = (
    "261d34c381bd3e2c8f0f8602fd2afe11fc2531d70b4a2a514dd176a69933b0ac"
)
VOCABULARY_RANGE = (277, 290)

TYPE_GENERIC = 0
TYPE_TRIVIAL = 1
TYPE_U8 = 2
TYPE_I8 = 3
TYPE_INTEGER = 4

PATH_CLONE_DEFAULT = 10
PATH_CLONE_TRIVIAL_COPY = 11
PATH_FILL_DEFAULT = 20
PATH_FILL_TRIVIAL_READ = 21
PATH_FILL_U8_BYTES = 22
PATH_FILL_I8_BYTES = 23
PATH_FILL_INTEGER_BYTES = 24
PATH_FILL_INTEGER_LOOP = 25


@dataclass(frozen=True)
class CloneEffectTarget:
    target: str
    input_order: str
    artifact_id: str
    active_contract_sha256: str
    active_contract_text: str
    generated_declaration_sha256: str
    source_start: int
    source_end: int
    docs_start: int
    docs_end: int
    source_item_sha256: str
    harness_sha256: str
    source_body_manifest_sha256: str
    transformation_manifest_sha256: str
    dependency_manifest_sha256: str
    admitted_trust_site_ids: tuple[str, ...]
    context_only_trust_site_ids: tuple[str, ...]
    is_fill: bool

    @property
    def function_name(self) -> str:
        return self.target.rsplit("::", 1)[-1]

    @property
    def source_reference(self) -> str:
        return f"{CANONICAL_SLICE_PATH}:{self.source_start}-{self.source_end}"

    @property
    def docs_reference(self) -> str:
        return f"{CANONICAL_SLICE_PATH}:{self.docs_start}-{self.docs_end}"

    @property
    def helper_reference(self) -> str:
        return (
            f"{SPECIALIZE_PATH}:4-73"
            if self.is_fill
            else f"{CANONICAL_SLICE_PATH}:5556-5628"
        )

    @property
    def all_trust_site_ids(self) -> tuple[str, ...]:
        return (
            *self.admitted_trust_site_ids,
            *self.context_only_trust_site_ids,
        )

    @property
    def output_fields(self) -> tuple[tuple[str, str], ...]:
        return (
            ("y_returned_unit", "Bool"),
            ("y_final_length", "Int"),
            ("y_final_values", "(Array Int Int)"),
        )

    @property
    def state_fields(self) -> tuple[tuple[str, str], ...]:
        common = (
            ("s_destination_values", "(Array Int Int)"),
            ("s_clone_state", "Int"),
            ("s_clone_call_count", "Int"),
            ("s_write_count", "Int"),
            ("s_intrinsic_call_count", "Int"),
            ("s_assignment_count", "Int"),
            ("s_selected_path", "Int"),
            ("s_frame_token", "Int"),
        )
        if self.is_fill:
            return common + (("s_final_slot_moved", "Bool"),)
        return common + (("s_source_values", "(Array Int Int)"),)

    @property
    def boundary_fields(self) -> tuple[tuple[str, str], ...]:
        fields: list[tuple[str, str]] = [
            ("b_destination_values", "(Array Int Int)"),
            ("b_destination_address", "Int"),
            ("b_destination_allocation", "Int"),
            ("b_destination_provenance", "Int"),
            ("b_destination_borrow", "Int"),
            ("b_element_size", "Int"),
            ("b_element_alignment", "Int"),
            ("b_clone_argument", "(Array Int Int)"),
            ("b_clone_result", "(Array Int CloneValue)"),
            ("b_clone_state_before", "(Array Int Int)"),
            ("b_clone_state_after", "(Array Int Int)"),
            ("b_clone_outcome", "(Array Int CallbackOutcome)"),
        ]
        if self.is_fill:
            fields.extend(
                (
                    ("b_fill_value", "Int"),
                    ("b_miri", "Bool"),
                    ("b_static_known", "Bool"),
                )
            )
        else:
            fields.extend(
                (
                    ("b_source_values", "(Array Int Int)"),
                    ("b_source_address", "Int"),
                    ("b_source_allocation", "Int"),
                    ("b_source_provenance", "Int"),
                )
            )
        return tuple(fields)

    @property
    def active_conjuncts(self) -> tuple[str, ...]:
        return (
            "ActiveFinalLengthConjunct",
            (
                "ActiveSliceFilledWithCloneConjunct"
                if self.is_fill
                else "ActiveSliceClonedFromConjunct"
            ),
        )


TARGET_037 = CloneEffectTarget(
    target="core::slice::clone_from_slice",
    input_order="37",
    artifact_id="037_core_slice_clone_from_slice",
    active_contract_sha256=(
        "a0fab9b11562f51ba66aa30d496a750f79f0e0b691e4d3e75051a847547033f5"
    ),
    active_contract_text=(
        "pub assume_specification<T: core::clone::Clone>[ "
        "<[T]>::clone_from_slice ](dst: &mut [T], src: &[T]) requires "
        "old(dst)@.len() == src@.len() ensures "
        "slice_cloned_from(src@, final(dst)@);"
    ),
    generated_declaration_sha256=(
        "5f4c2605d0cd1b2ba2c475a03b200e7570b0f4b008b1354c0c0f149e227c44d6"
    ),
    source_start=4254,
    source_end=4259,
    docs_start=4199,
    docs_end=4250,
    source_item_sha256=(
        "0dfc2e8b8b0a5319d883279e62986e9055b56d6ac6ba773cc4f6b9887423819b"
    ),
    harness_sha256=(
        "f3744b77ac104baaff9937db598e197d8427900e61e2dbfd0c046bf5d1fa8630"
    ),
    source_body_manifest_sha256=(
        "172c58d1e652fedd5ef90927dbacdb1cb312ac10f6f22f1e638413c1c6a2562d"
    ),
    transformation_manifest_sha256=(
        "ffb074f80cbadcac3ebf73164aa42e5aba5ff9968da380219e03e6e329398c99"
    ),
    dependency_manifest_sha256=(
        "b4a0e9c31e5b0097c4bf1db95ebb40870529d205216df3dea1d7c246eef92e1c"
    ),
    admitted_trust_site_ids=(
        "TS-037-D002",
        "TS-037-D003",
        "TS-037-D004",
        "TS-037-E001",
    ),
    context_only_trust_site_ids=(
        "TS-037-D001",
        "TS-037-C001",
        "TS-037-C002",
        "TS-037-C003",
        "TS-037-C004",
        "TS-037-C005",
        "TS-037-C006",
        "TS-037-C007",
        "TS-037-C008",
    ),
    is_fill=False,
)

TARGET_043 = CloneEffectTarget(
    target="core::slice::fill",
    input_order="43",
    artifact_id="043_core_slice_fill",
    active_contract_sha256=(
        "7772c35bc8a2e714a53e79384d43b99e96daae6650124087e508e2542ceb3f38"
    ),
    active_contract_text=(
        "pub assume_specification<T: core::clone::Clone>[ <[T]>::fill ]("
        "slice: &mut [T], value: T) ensures "
        "slice_filled_with_clone(old(slice)@, value, final(slice)@);"
    ),
    generated_declaration_sha256=(
        "4e0eaf1bbf6302f5739006669aaf73e237cda9ea78acb8bfea2eb64d64071618"
    ),
    source_start=4166,
    source_end=4171,
    docs_start=4155,
    docs_end=4163,
    source_item_sha256=(
        "e9949b7e821e39d687514cd4b39f23b69157d7ef6c845f36b8c95f1864a553d8"
    ),
    harness_sha256=(
        "e0b180f6cb52a78b70a62a2750a87bbf8b878e3ab649400b8497c8c9e5e40fd8"
    ),
    source_body_manifest_sha256=(
        "7362df490d3ea30f582cbd306c168fb4d1a99fb7c38fc46fe0492f263f8297a1"
    ),
    transformation_manifest_sha256=(
        "b0790c77c05c76ca07958b0b7b55bf2b248dad9a65b831b9d4a0f770202f49d0"
    ),
    dependency_manifest_sha256=(
        "46c12ff62c16a92ea4aa41f8a1799c00b56225ce4cf1c31e6bae749074ac9faf"
    ),
    admitted_trust_site_ids=(
        "TS-043-D002",
        "TS-043-D003",
        "TS-043-D004",
        "TS-043-D005",
        "TS-043-E001",
    ),
    context_only_trust_site_ids=(
        "TS-043-D001",
        "TS-043-C001",
        "TS-043-C002",
        "TS-043-C003",
    ),
    is_fill=True,
)

TARGETS = (TARGET_037, TARGET_043)
TARGET_BY_ARTIFACT = {target.artifact_id: target for target in TARGETS}
TARGET_BY_KEY = {
    (target.target, target.input_order): target for target in TARGETS
}
TARGET_KEYS = tuple(TARGET_BY_KEY)


@dataclass(frozen=True)
class SourceCase:
    name: str
    length: int
    element_size: int
    type_kind: int
    expected_path: int
    miri: bool = False
    static_known: bool = False
    uniform_bytes: bool = False
    relation_valued: bool = False


SOURCE_CASES: dict[str, tuple[SourceCase, ...]] = {
    TARGET_037.artifact_id: (
        SourceCase(
            "default_empty_non_zst", 0, 8, TYPE_GENERIC, PATH_CLONE_DEFAULT
        ),
        SourceCase(
            "default_empty_zst", 0, 0, TYPE_GENERIC, PATH_CLONE_DEFAULT
        ),
        SourceCase(
            "default_singleton_non_zst",
            1,
            8,
            TYPE_GENERIC,
            PATH_CLONE_DEFAULT,
            relation_valued=True,
        ),
        SourceCase(
            "default_longer_non_zst",
            4,
            8,
            TYPE_GENERIC,
            PATH_CLONE_DEFAULT,
            relation_valued=True,
        ),
        SourceCase(
            "default_longer_zst",
            4,
            0,
            TYPE_GENERIC,
            PATH_CLONE_DEFAULT,
            relation_valued=True,
        ),
        SourceCase(
            "trivial_empty_non_zst",
            0,
            8,
            TYPE_TRIVIAL,
            PATH_CLONE_TRIVIAL_COPY,
        ),
        SourceCase(
            "trivial_singleton_non_zst",
            1,
            8,
            TYPE_TRIVIAL,
            PATH_CLONE_TRIVIAL_COPY,
        ),
        SourceCase(
            "trivial_longer_non_zst",
            4,
            8,
            TYPE_TRIVIAL,
            PATH_CLONE_TRIVIAL_COPY,
        ),
        SourceCase(
            "trivial_longer_zst",
            4,
            0,
            TYPE_TRIVIAL,
            PATH_CLONE_TRIVIAL_COPY,
        ),
    ),
    TARGET_043.artifact_id: (
        SourceCase(
            "default_empty_non_zst", 0, 8, TYPE_GENERIC, PATH_FILL_DEFAULT
        ),
        SourceCase(
            "default_empty_zst", 0, 0, TYPE_GENERIC, PATH_FILL_DEFAULT
        ),
        SourceCase(
            "default_singleton_non_zst",
            1,
            8,
            TYPE_GENERIC,
            PATH_FILL_DEFAULT,
        ),
        SourceCase(
            "default_longer_non_zst",
            4,
            8,
            TYPE_GENERIC,
            PATH_FILL_DEFAULT,
            relation_valued=True,
        ),
        SourceCase(
            "default_longer_zst",
            4,
            0,
            TYPE_GENERIC,
            PATH_FILL_DEFAULT,
            relation_valued=True,
        ),
        SourceCase(
            "trivial_singleton_non_zst",
            1,
            8,
            TYPE_TRIVIAL,
            PATH_FILL_TRIVIAL_READ,
        ),
        SourceCase(
            "trivial_longer_non_zst",
            4,
            8,
            TYPE_TRIVIAL,
            PATH_FILL_TRIVIAL_READ,
        ),
        SourceCase(
            "trivial_longer_zst",
            4,
            0,
            TYPE_TRIVIAL,
            PATH_FILL_TRIVIAL_READ,
        ),
        SourceCase("u8_empty", 0, 1, TYPE_U8, PATH_FILL_U8_BYTES),
        SourceCase("u8_longer", 4, 1, TYPE_U8, PATH_FILL_U8_BYTES),
        SourceCase("i8_singleton", 1, 1, TYPE_I8, PATH_FILL_I8_BYTES),
        SourceCase("i8_longer", 4, 1, TYPE_I8, PATH_FILL_I8_BYTES),
        SourceCase(
            "integer_static_uniform_bytes",
            4,
            4,
            TYPE_INTEGER,
            PATH_FILL_INTEGER_BYTES,
            static_known=True,
            uniform_bytes=True,
        ),
        SourceCase(
            "integer_static_nonuniform_loop",
            4,
            4,
            TYPE_INTEGER,
            PATH_FILL_INTEGER_LOOP,
            static_known=True,
        ),
        SourceCase(
            "integer_dynamic_loop",
            4,
            4,
            TYPE_INTEGER,
            PATH_FILL_INTEGER_LOOP,
        ),
        SourceCase(
            "integer_miri_long_uniform_bytes",
            33,
            4,
            TYPE_INTEGER,
            PATH_FILL_INTEGER_BYTES,
            miri=True,
            uniform_bytes=True,
        ),
        SourceCase(
            "integer_miri_long_nonuniform_loop",
            33,
            4,
            TYPE_INTEGER,
            PATH_FILL_INTEGER_LOOP,
            miri=True,
        ),
        SourceCase(
            "integer_miri_short_loop",
            32,
            4,
            TYPE_INTEGER,
            PATH_FILL_INTEGER_LOOP,
            miri=True,
        ),
    ),
}


def expected_intrinsic_call_count(
    config: CloneEffectTarget,
    case: SourceCase,
) -> int:
    if not config.is_fill:
        return int(case.type_kind == TYPE_TRIVIAL)
    if case.type_kind in {TYPE_U8, TYPE_I8}:
        return 1
    if case.type_kind != TYPE_INTEGER:
        return 0

    miri_long = case.miri and case.length > 32
    static_known_calls = int(not miri_long)
    write_bytes_calls = int(
        (miri_long or case.static_known) and case.uniform_bytes
    )
    return static_known_calls + write_bytes_calls


def _record_fields(fields: tuple[tuple[str, str], ...]) -> str:
    return "\n".join(f"      ({name} {sort})" for name, sort in fields)


INPUT_FIELDS = (
    ("x_destination_length", "Int"),
    ("x_source_length", "Int"),
    ("x_destination_values", "(Array Int Int)"),
    ("x_source_values", "(Array Int Int)"),
    ("x_fill_value", "Int"),
    ("x_type_kind", "Int"),
    ("x_miri", "Bool"),
    ("x_value_uniform_bytes", "Bool"),
    ("x_destination_address", "Int"),
    ("x_destination_allocation", "Int"),
    ("x_destination_provenance", "Int"),
    ("x_destination_borrow", "Int"),
    ("x_source_address", "Int"),
    ("x_source_allocation", "Int"),
    ("x_source_provenance", "Int"),
    ("x_element_size", "Int"),
    ("x_element_alignment", "Int"),
    ("x_frame_token", "Int"),
    ("x_clone_initial_state", "Int"),
)


def _state_declaration(config: CloneEffectTarget, purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    return f"""\
(declare-datatypes ((State 0))
  (((mkState
{_record_fields(config.state_fields)}))))"""


def _input_boundary_observed(config: CloneEffectTarget) -> str:
    clauses = [
        "(= (b_destination_values b) (x_destination_values x))",
        "(= (b_destination_address b) (x_destination_address x))",
        "(= (b_destination_allocation b) (x_destination_allocation x))",
        "(= (b_destination_provenance b) (x_destination_provenance x))",
        "(= (b_destination_borrow b) (x_destination_borrow x))",
        "(= (b_element_size b) (x_element_size x))",
        "(= (b_element_alignment b) (x_element_alignment x))",
    ]
    if config.is_fill:
        clauses.extend(
            (
                "(= (b_fill_value b) (x_fill_value x))",
                "(= (b_miri b) (x_miri x))",
                (
                    "(or (= (x_type_kind x) 4) "
                    "(= (b_static_known b) false))"
                ),
            )
        )
    else:
        clauses.extend(
            (
                "(= (b_source_values b) (x_source_values x))",
                "(= (b_source_address b) (x_source_address x))",
                "(= (b_source_allocation b) (x_source_allocation x))",
                "(= (b_source_provenance b) (x_source_provenance x))",
            )
        )
    return """\
(define-fun InputBoundaryObserved ((x Input) (b Boundary)) Bool
  (and %s))""" % "\n       ".join(clauses)


def _type_requirement(config: CloneEffectTarget) -> str:
    if config.is_fill:
        return "(and (>= (x_type_kind x) 0) (<= (x_type_kind x) 4))"
    return "(or (= (x_type_kind x) 0) (= (x_type_kind x) 1))"


def _selected_path(config: CloneEffectTarget) -> str:
    if not config.is_fill:
        body = (
            f"(ite (= (x_type_kind x) {TYPE_GENERIC}) "
            f"{PATH_CLONE_DEFAULT} {PATH_CLONE_TRIVIAL_COPY})"
        )
    else:
        body = f"""\
(ite (= (x_type_kind x) {TYPE_GENERIC}) {PATH_FILL_DEFAULT}
  (ite (= (x_type_kind x) {TYPE_TRIVIAL}) {PATH_FILL_TRIVIAL_READ}
    (ite (= (x_type_kind x) {TYPE_U8}) {PATH_FILL_U8_BYTES}
      (ite (= (x_type_kind x) {TYPE_I8}) {PATH_FILL_I8_BYTES}
        (ite
          (and
            (or
              (and (x_miri x) (> (x_destination_length x) 32))
              (b_static_known b))
            (x_value_uniform_bytes x))
          {PATH_FILL_INTEGER_BYTES}
          {PATH_FILL_INTEGER_LOOP})))))"""
    return f"""\
(define-fun SelectedSpecializationPath ((x Input) (b Boundary)) Int
  {body})"""


def _intrinsic_call_count_definition(
    config: CloneEffectTarget,
) -> str:
    if not config.is_fill:
        return f"""\
(define-fun IntrinsicCallCount ((x Input) (b Boundary)) Int
  (ite
    (or
      (= (SelectedSpecializationPath x b) {PATH_CLONE_TRIVIAL_COPY})
      (= (SelectedSpecializationPath x b) {PATH_FILL_U8_BYTES})
      (= (SelectedSpecializationPath x b) {PATH_FILL_I8_BYTES})
      (= (SelectedSpecializationPath x b) {PATH_FILL_INTEGER_BYTES}))
    1
    0))"""
    return f"""\
(define-fun IntrinsicCallCount ((x Input) (b Boundary)) Int
  (ite
    (or
      (= (x_type_kind x) {TYPE_U8})
      (= (x_type_kind x) {TYPE_I8}))
    1
    (ite
      (= (x_type_kind x) {TYPE_INTEGER})
      (+
        (ite
          (and (x_miri x) (> (x_destination_length x) 32))
          0
          1)
        (ite
          (= (SelectedSpecializationPath x b) {PATH_FILL_INTEGER_BYTES})
          1
          0))
      0)))"""


def _callback_count(config: CloneEffectTarget) -> str:
    if config.is_fill:
        body = """\
(ite (= (x_type_kind x) 0)
     (ite (> (x_destination_length x) 0)
          (- (x_destination_length x) 1)
          0)
     0)"""
    else:
        body = """\
(ite (= (x_type_kind x) 0)
     (x_destination_length x)
     0)"""
    return f"""\
(define-fun CallbackOperationCount ((x Input)) Int
  {body})"""


def _expected_argument(config: CloneEffectTarget) -> str:
    value = (
        "(x_fill_value x)"
        if config.is_fill
        else "(select (x_source_values x) index)"
    )
    return f"""\
(define-fun ExpectedCloneArgument ((x Input) (index Int)) Int
  {value})"""


def _state_equalities(config: CloneEffectTarget, purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return ""
    common = """\
       (= (s_destination_values s) (SourceFinalStorage x b))
       (= (s_clone_state s) (FinalCloneState x b))
       (= (s_clone_call_count s) (CallbackOperationCount x))
       (= (s_write_count s) (x_destination_length x))
       (= (s_intrinsic_call_count s) (IntrinsicCallCount x b))
       (= (s_assignment_count s) (AssignmentOperationCount x b))
       (= (s_selected_path s) (SelectedSpecializationPath x b))
       (= (s_frame_token s) (x_frame_token x))"""
    if config.is_fill:
        target = """\
       (= (s_final_slot_moved s)
          (and (= (x_type_kind x) 0)
               (> (x_destination_length x) 0)))"""
    else:
        target = """\
       (= (s_source_values s) (x_source_values x))"""
    return common + "\n" + target


def _active_relation(config: CloneEffectTarget) -> str:
    name = (
        "ActiveSliceFilledWithCloneConjunct"
        if config.is_fill
        else "ActiveSliceClonedFromConjunct"
    )
    source = (
        "(x_fill_value x)"
        if config.is_fill
        else "(select (x_source_values x) index)"
    )
    return f"""\
(define-fun {name}
  ((x Input) (b Boundary) (y Output)) Bool
  (forall ((index Int))
    (=>
      (and (>= index 0) (< index (x_destination_length x)))
      (Cloned_T
        x b index {source} (select (y_final_values y) index)))))"""


def _model_text(
    config: CloneEffectTarget,
    purpose: str,
    *,
    include_theorem: bool,
) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown obligation purpose {purpose}")
    state_equalities = _state_equalities(config, purpose)
    active_name = config.active_conjuncts[1]
    equivalence = [
        f"(= ({selector} y1) ({selector} y2))"
        for selector, _ in config.output_fields
    ]
    if purpose == PRIMARY:
        equivalence.extend(
            f"(= ({selector} s1) ({selector} s2))"
            for selector, _ in config.state_fields
        )
    theorem = ""
    if include_theorem:
        theorem = """\
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
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; Cloned_T is relation-valued. Only individual source-used Clone observations
; enter Boundary_T; order, count, dispatch, final storage, and final state are
; derived by the Rust 1.96 source transition.
(set-logic ALL)
(declare-datatypes ((CallbackOutcome 0))
  (((Completed) (Panicked) (NotCalled))))
(declare-datatypes ((CloneValue 0))
  (((Cloned (cloned_value Int)))))
(declare-datatypes ((Input 0))
  (((mkInput
{_record_fields(INPUT_FIELDS)}))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
{_record_fields(config.boundary_fields)}))))
(declare-datatypes ((Output 0))
  (((mkOutput
{_record_fields(config.output_fields)}))))
{_state_declaration(config, purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
{_input_boundary_observed(config)}
{_selected_path(config)}
{_intrinsic_call_count_definition(config)}
(define-fun AssignmentOperationCount ((x Input) (b Boundary)) Int
  (ite
    (= (SelectedSpecializationPath x b) {PATH_FILL_DEFAULT})
    (ite (> (x_destination_length x) 0) 1 0)
    (ite
      (or
        (= (SelectedSpecializationPath x b) {PATH_FILL_TRIVIAL_READ})
        (= (SelectedSpecializationPath x b) {PATH_FILL_INTEGER_LOOP}))
      (x_destination_length x)
      0)))
{_callback_count(config)}
{_expected_argument(config)}
(define-fun CloneIndexAtStep ((x Input) (step Int)) Int
  step)
(define-fun IndexUsesCloneCallback ((x Input) (index Int)) Bool
  (and (>= index 0) (< index (CallbackOperationCount x))))
(define-fun Cloned_T
  ((x Input) (b Boundary) (index Int) (source Int) (result Int)) Bool
  (ite
    (IndexUsesCloneCallback x index)
    (and
      (= (select (b_clone_argument b) index) source)
      (= (cloned_value (select (b_clone_result b) index)) result)
      (= (select (b_clone_outcome b) index) Completed))
    (= result source)))
(define-fun-rec CallbackCompletedThrough
  ((x Input) (b Boundary) (count Int)) Bool
  (ite
    (<= count 0)
    true
    (let ((step (- count 1)))
      (let ((index (CloneIndexAtStep x step)))
        (and
          (CallbackCompletedThrough x b step)
          (= index step)
          (= (select (b_clone_argument b) index)
             (ExpectedCloneArgument x index))
          ((_ is Cloned) (select (b_clone_result b) index))
          (= (select (b_clone_outcome b) index) Completed)
          (= (select (b_clone_state_before b) index)
             (ite
               (= step 0)
               (x_clone_initial_state x)
               (select
                 (b_clone_state_after b)
                 (CloneIndexAtStep x (- step 1))))))))))
(define-fun NoUnexpectedCallbacks ((x Input) (b Boundary)) Bool
  (forall ((index Int))
    (=>
      (and
        (>= index (CallbackOperationCount x))
        (< index (x_destination_length x)))
      (= (select (b_clone_outcome b) index) NotCalled))))
(define-fun NormalCallbackExecution ((x Input) (b Boundary)) Bool
  (and
    (CallbackCompletedThrough x b (CallbackOperationCount x))
    (NoUnexpectedCallbacks x b)))
(define-fun FinalCloneState ((x Input) (b Boundary)) Int
  (ite
    (= (CallbackOperationCount x) 0)
    (x_clone_initial_state x)
    (select
      (b_clone_state_after b)
      (CloneIndexAtStep x (- (CallbackOperationCount x) 1)))))
(define-fun SourceValueAt ((x Input) (index Int)) Int
  {"(x_fill_value x)" if config.is_fill else "(select (x_source_values x) index)"})
(define-fun ResultValueAt
  ((x Input) (b Boundary) (index Int)) Int
  (ite
    (IndexUsesCloneCallback x index)
    (cloned_value (select (b_clone_result b) index))
    (SourceValueAt x index)))
(define-fun WriteIndexAtStep ((x Input) (step Int)) Int
  step)
(define-fun-rec WriteStorageAfterSteps
  ((x Input) (b Boundary) (count Int)) (Array Int Int)
  (ite
    (<= count 0)
    (x_destination_values x)
    (let ((step (- count 1)))
      (store
        (WriteStorageAfterSteps x b step)
        (WriteIndexAtStep x step)
        (ResultValueAt x b step)))))
(define-fun SourceFinalStorage
  ((x Input) (b Boundary)) (Array Int Int)
  (lambda ((index Int))
    (ite
      (and (>= index 0) (< index (x_destination_length x)))
      (ResultValueAt x b index)
      (select (x_destination_values x) index))))
(define-fun WritesCompletedThrough
  ((x Input) (b Boundary) (count Int)) Bool
  (and
    (>= count 0)
    (<= count (x_destination_length x))
    (forall ((step Int))
      (=>
        (and (>= step 0) (< step count))
        (and
          (= (WriteIndexAtStep x step) step)
          (Cloned_T
            x
            b
            step
            (SourceValueAt x step)
            (ResultValueAt x b step))
          (= (select (SourceFinalStorage x b) step)
             (ResultValueAt x b step)))))))
(define-fun NormalSourceExecution
  ((x Input) (b Boundary)) Bool
  (and
    (NormalCallbackExecution x b)
    (WritesCompletedThrough x b (x_destination_length x))
    (>= (SelectedSpecializationPath x b) 0)))
(define-fun ActiveFinalLengthConjunct
  ((x Input) (y Output)) Bool
  (= (y_final_length y) (x_destination_length x)))
{_active_relation(config)}
(define-fun Requires_T ((x Input)) Bool
  (and
    (>= (x_destination_length x) 0)
    (>= (x_source_length x) 0)
    {("(= (x_destination_length x) (x_source_length x))" if not config.is_fill else "true")}
    {_type_requirement(config)}
    (> (x_destination_address x) 0)
    (> (x_destination_borrow x) 0)
    (> (x_element_alignment x) 0)
    (>= (x_element_size x) 0)
    (= (mod (x_destination_address x) (x_element_alignment x)) 0)
    {("(and (> (x_source_address x) 0) (= (mod (x_source_address x) (x_element_alignment x)) 0))" if not config.is_fill else "true")}
    (or
      (= (x_element_size x) 0)
      (and
        (> (x_destination_allocation x) 0)
        (> (x_destination_provenance x) 0)
        {("(and (> (x_source_allocation x) 0) (> (x_source_provenance x) 0))" if not config.is_fill else "true")}))))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and
    (InputBoundaryObserved x b)
    (NormalCallbackExecution x b)))
(define-fun TargetSourceTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (NormalSourceExecution x b)
    (= (y_returned_unit y) true)
    (= (y_final_length y) (x_destination_length x))
    (= (y_final_values y) (SourceFinalStorage x b))
{state_equalities}))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and
    (InputBoundaryObserved x b)
    (TargetSourceTransition x b y s)
    (ActiveFinalLengthConjunct x y)
    ({active_name} x b y)))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and {" ".join(equivalence)}))
{theorem}"""


def obligation_text(config: CloneEffectTarget, purpose: str) -> str:
    return _model_text(config, purpose, include_theorem=True)


def _principal_observations(
    config: CloneEffectTarget, purpose: str
) -> list[dict[str, str]]:
    result = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort.strip("()"),
        }
        for selector, sort in config.output_fields
    ]
    if purpose == PRIMARY:
        result.extend(
            {
                "selector": selector,
                "left": "state1",
                "right": "state2",
                "sort": sort.strip("()"),
            }
            for selector, sort in config.state_fields
        )
    return result


def _boundary_metadata(config: CloneEffectTarget) -> list[dict[str, Any]]:
    clone_fields = {
        "b_clone_argument",
        "b_clone_result",
        "b_clone_state_before",
        "b_clone_state_after",
        "b_clone_outcome",
    }
    provenance_fields = {
        "b_destination_allocation",
        "b_destination_provenance",
        "b_destination_borrow",
        "b_source_allocation",
        "b_source_provenance",
    }
    layout_fields = {"b_element_size", "b_element_alignment"}
    roles = {
        "b_clone_argument": "callback_argument",
        "b_clone_result": "callback_result",
        "b_clone_state_before": "callback_state_transition",
        "b_clone_state_after": "callback_state_transition",
        "b_clone_outcome": "callback_panic",
        "b_destination_values": "input_initialization",
        "b_source_values": "input_memory",
        "b_fill_value": "callback_argument",
        "b_miri": "source_helper_observation",
        "b_static_known": "source_helper_observation",
    }
    records: list[dict[str, Any]] = []
    for selector, _ in config.boundary_fields:
        role = roles.get(selector)
        if role is None:
            if selector in provenance_fields:
                role = "input_provenance"
            elif selector in layout_fields:
                role = "input_layout"
            else:
                role = "input_memory"
        if selector in clone_fields:
            trust = [
                site
                for site in config.admitted_trust_site_ids
                if site.endswith(("D002", "D003", "D005", "E001"))
            ]
        elif selector in {"b_miri", "b_static_known"}:
            trust = [
                site
                for site in config.admitted_trust_site_ids
                if site.endswith("D004")
            ]
        else:
            trust = list(config.admitted_trust_site_ids)
        records.append(
            {
                "selector": selector,
                "role": role,
                "meaning": (
                    "one source-used Clone observation"
                    if selector in clone_fields
                    else "initial source/platform input observation"
                ),
                "source_citations": [
                    config.source_reference,
                    config.helper_reference,
                    (
                        "vstd::std_specs::clone::cloned<T>"
                        if selector in clone_fields
                        else config.docs_reference
                    ),
                ],
                "trust_site_ids": trust,
                "source_backed_replacement_ids": [],
            }
        )
    return records


def obligation_metadata(
    config: CloneEffectTarget, purpose: str
) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown obligation purpose {purpose}")
    return {
        "schema_version": 3,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "model_status": "source-backed-complete",
        "domain": {
            "length": (
                "arbitrary equal nonnegative source/destination lengths"
                if not config.is_fill
                else "arbitrary nonnegative destination length"
            ),
            "layout": "zero-sized and non-zero-sized elements",
            "clone": (
                "relation-valued per-call results, state transitions, and "
                "panic outcomes"
            ),
            "specialization": (
                "generic/default and TrivialClone copy"
                if not config.is_fill
                else (
                    "default, TrivialClone, u8, i8, and integer "
                    "write_bytes-or-loop paths"
                )
            ),
            "source_model_complete": True,
        },
        "active_contract_conjuncts": list(config.active_conjuncts),
        "boundary_scope": {
            "shared_observations": [
                field["selector"] for field in _boundary_metadata(config)
            ],
            "admitted_trust_site_ids": list(
                config.admitted_trust_site_ids
            ),
            "excluded_retained_trust_site_ids": [],
            "context_only_trust_site_ids": list(
                config.context_only_trust_site_ids
            ),
            "all_audited_trust_site_ids": list(
                config.all_trust_site_ids
            ),
            "source_backed_replacement_ids": [],
            "excluded_observations": [
                "aggregate destination storage",
                "aggregate final callback state",
                "operation order or count",
                "selected specialization result",
                "complete execution trace",
                "answer-equivalent output",
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
        "boundary_fields": _boundary_metadata(config),
        "declared_functions": [],
        "source_backed_replacements": [],
        "unresolved_source_model_trust_site_ids": [],
        "source_transition_definitions": ["TargetSourceTransition"],
        "source_transition_bindings": {
            "public_target": config.source_reference,
            "private_paths": config.helper_reference,
            "active_relation": (
                "slice_filled_with_clone"
                if config.is_fill
                else "slice_cloned_from"
            ),
            "relation_vocabulary": "vstd::std_specs::clone::cloned<T>",
            "ordered_operations": [
                "CloneIndexAtStep",
                "CallbackCompletedThrough",
                "WriteIndexAtStep",
                "WriteStorageAfterSteps",
                "SourceFinalStorage",
            ],
            "specialization_selector": "SelectedSpecializationPath",
            "final_slot_move": config.is_fill,
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "unit return, relation-valued final destination, source frame, "
            "callback state/count, write count, and selected source path"
            if purpose == PRIMARY
            else "unit return and relation-valued final destination"
        ),
        "principal_observations": _principal_observations(config, purpose),
        "expected_solver_result": "unsat",
    }


def obligation(
    config: CloneEffectTarget, purpose: str
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: CloneEffectTarget,
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
            f"{config.target}: metadata differs from the reviewed clone model"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.target}: SMT differs from the reviewed clone model"
        )


def _int_array(values: dict[int, int], default: int = 0) -> str:
    expression = f"((as const (Array Int Int)) {default})"
    for index, value in sorted(values.items()):
        expression = f"(store {expression} {index} {value})"
    return expression


def _replace_definition(text: str, symbol: str, replacement: str) -> str:
    marker = f"(define-fun {symbol}"
    recursive_marker = f"(define-fun-rec {symbol}"
    if marker in text:
        start = text.index(marker)
    else:
        start = text.index(recursive_marker)
    balance = 0
    for end in range(start, len(text)):
        if text[end] == "(":
            balance += 1
        elif text[end] == ")":
            balance -= 1
            if balance == 0:
                return text[:start] + replacement + text[end + 1 :]
    raise RuntimeError(f"unterminated SMT definition: {symbol}")


def _bounded_model_text(
    config: CloneEffectTarget,
    purpose: str,
    case: SourceCase,
) -> str:
    length = case.length
    if length < 0:
        raise ValueError("bounded model length must be nonnegative")
    text = _model_text(config, purpose, include_theorem=False)
    callback_count = (
        length
        if not config.is_fill and case.type_kind == TYPE_GENERIC
        else max(length - 1, 0)
        if config.is_fill and case.type_kind == TYPE_GENERIC
        else 0
    )

    callback_steps = [
        f"""(and
        (= (CloneIndexAtStep x {index}) {index})
        (= (select (b_clone_argument b) {index})
           (ExpectedCloneArgument x {index}))
        ((_ is Cloned) (select (b_clone_result b) {index}))
        (= (select (b_clone_outcome b) {index}) Completed)
        (= (select (b_clone_state_before b) {index})
           {"(x_clone_initial_state x)" if index == 0 else f"(select (b_clone_state_after b) {index - 1})"}))"""
        for index in range(callback_count)
    ]
    text = _replace_definition(
        text,
        "CallbackCompletedThrough",
        f"""(define-fun CallbackCompletedThrough
  ((x Input) (b Boundary) (count Int)) Bool
  (and
    (= count {callback_count})
    {" ".join(callback_steps) or "true"}))""",
    )

    text = _replace_definition(
        text,
        "WriteStorageAfterSteps",
        """(define-fun WriteStorageAfterSteps
  ((x Input) (b Boundary) (count Int)) (Array Int Int)
  (x_destination_values x))""",
    )

    if config.is_fill and case.type_kind != TYPE_GENERIC:
        storage = "((as const (Array Int Int)) (x_fill_value x))"
    else:
        storage = "(x_destination_values x)"
        for index in range(length):
            storage = (
                f"(store {storage} {index} "
                f"(ResultValueAt x b {index}))"
            )
    text = _replace_definition(
        text,
        "SourceFinalStorage",
        """(define-fun SourceFinalStorage
  ((x Input) (b Boundary)) (Array Int Int)
  %s)""" % storage,
    )

    unexpected = [
        f"(= (select (b_clone_outcome b) {index}) NotCalled)"
        for index in range(callback_count, length)
    ]
    text = _replace_definition(
        text,
        "NoUnexpectedCallbacks",
        (
            """(define-fun NoUnexpectedCallbacks
  ((x Input) (b Boundary)) Bool
  (= (b_clone_outcome b)
     ((as const (Array Int CallbackOutcome)) NotCalled)))"""
            if config.is_fill and case.type_kind != TYPE_GENERIC
            else """(define-fun NoUnexpectedCallbacks
  ((x Input) (b Boundary)) Bool
  (and %s))""" % (" ".join(unexpected) or "true")
        ),
    )

    writes = (
        []
        if config.is_fill and case.type_kind != TYPE_GENERIC
        else [
            f"""(=>
      (< {index} count)
      (and
        (= (WriteIndexAtStep x {index}) {index})
        (Cloned_T
          x b {index} (SourceValueAt x {index})
          (ResultValueAt x b {index}))
        (= (select (SourceFinalStorage x b) {index})
           (ResultValueAt x b {index}))))"""
            for index in range(length)
        ]
    )
    text = _replace_definition(
        text,
        "WritesCompletedThrough",
        """(define-fun WritesCompletedThrough
  ((x Input) (b Boundary) (count Int)) Bool
  (and
    (>= count 0)
    (<= count (x_destination_length x))
    %s))""" % ("\n    ".join(writes) or "true"),
    )

    active_name = config.active_conjuncts[1]
    relations = (
        [
            "(= (y_final_values y) "
            "((as const (Array Int Int)) (x_fill_value x)))"
        ]
        if config.is_fill and case.type_kind != TYPE_GENERIC
        else [
            (
                f"(Cloned_T x b {index} (SourceValueAt x {index}) "
                f"(select (y_final_values y) {index}))"
            )
            for index in range(length)
        ]
    )
    text = _replace_definition(
        text,
        active_name,
        f"""(define-fun {active_name}
  ((x Input) (b Boundary) (y Output)) Bool
  (and {" ".join(relations) or "true"}))""",
    )
    return text


def _outcome_array(
    *,
    completed: tuple[int, ...] = (),
    panicked: tuple[int, ...] = (),
) -> str:
    expression = "((as const (Array Int CallbackOutcome)) NotCalled)"
    for index in completed:
        expression = f"(store {expression} {index} Completed)"
    for index in panicked:
        expression = f"(store {expression} {index} Panicked)"
    return expression


def _clone_array(values: dict[int, int], default: int = 0) -> str:
    expression = (
        f"((as const (Array Int CloneValue)) (Cloned {default}))"
    )
    for index, value in sorted(values.items()):
        expression = f"(store {expression} {index} (Cloned {value}))"
    return expression


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _case_values(
    config: CloneEffectTarget,
    case: SourceCase,
    *,
    panic_index: int | None = None,
    mismatch_source_length: int | None = None,
    broken_state_chain: bool = False,
) -> dict[str, Any]:
    length = case.length
    source_length = (
        length
        if mismatch_source_length is None
        else mismatch_source_length
    )
    source = (
        {}
        if config.is_fill
        else {
            index: 10 + index
            for index in range(max(source_length, length))
        }
    )
    destination = (
        {}
        if length == 0
        else {0: 500, length - 1: 500 + length - 1}
    )
    callback_count = (
        length
        if not config.is_fill and case.type_kind == TYPE_GENERIC
        else max(length - 1, 0)
        if config.is_fill and case.type_kind == TYPE_GENERIC
        else 0
    )
    completed_count = (
        callback_count if panic_index is None else panic_index
    )
    clone_argument = {
        index: (
            77 if config.is_fill else source[index]
        )
        for index in range(callback_count)
    }
    clone_result = {
        index: (
            1000 + index
            if case.relation_valued or panic_index is not None
            else clone_argument[index]
        )
        for index in range(callback_count)
    }
    before = {index: 100 + index for index in range(callback_count)}
    after = {index: 101 + index for index in range(callback_count)}
    if broken_state_chain and callback_count > 1:
        before[1] = 999
    return {
        "length": length,
        "source_length": source_length,
        "source": source,
        "destination": destination,
        "fill_value": 77,
        "type_kind": case.type_kind,
        "miri": case.miri,
        "uniform": case.uniform_bytes,
        "static_known": case.static_known,
        "element_size": case.element_size,
        "element_alignment": 1 if case.element_size in (0, 1) else 4,
        "destination_address": 4096,
        "destination_allocation": 61,
        "destination_provenance": 161,
        "destination_borrow": 261,
        "source_address": 8192,
        "source_allocation": 62,
        "source_provenance": 162,
        "frame_token": 999,
        "clone_initial_state": 100,
        "callback_count": callback_count,
        "completed_count": completed_count,
        "clone_argument": clone_argument,
        "clone_result": clone_result,
        "clone_before": before,
        "clone_after": after,
        "panic_index": panic_index,
    }


def _input_assertions(values: dict[str, Any]) -> list[str]:
    pairs = (
        ("x_destination_length", values["length"]),
        ("x_source_length", values["source_length"]),
        ("x_destination_values", _int_array(values["destination"])),
        ("x_source_values", _int_array(values["source"])),
        ("x_fill_value", values["fill_value"]),
        ("x_type_kind", values["type_kind"]),
        ("x_miri", _bool(values["miri"])),
        ("x_value_uniform_bytes", _bool(values["uniform"])),
        ("x_destination_address", values["destination_address"]),
        ("x_destination_allocation", values["destination_allocation"]),
        ("x_destination_provenance", values["destination_provenance"]),
        ("x_destination_borrow", values["destination_borrow"]),
        ("x_source_address", values["source_address"]),
        ("x_source_allocation", values["source_allocation"]),
        ("x_source_provenance", values["source_provenance"]),
        ("x_element_size", values["element_size"]),
        ("x_element_alignment", values["element_alignment"]),
        ("x_frame_token", values["frame_token"]),
        ("x_clone_initial_state", values["clone_initial_state"]),
    )
    return [f"(assert (= ({selector} x) {value}))" for selector, value in pairs]


def _boundary_assertions(
    config: CloneEffectTarget,
    values: dict[str, Any],
) -> list[str]:
    panic_index = values["panic_index"]
    outcomes = _outcome_array(
        completed=tuple(range(values["completed_count"])),
        panicked=(() if panic_index is None else (panic_index,)),
    )
    pairs: list[tuple[str, Any]] = [
        ("b_destination_values", _int_array(values["destination"])),
        ("b_destination_address", values["destination_address"]),
        ("b_destination_allocation", values["destination_allocation"]),
        ("b_destination_provenance", values["destination_provenance"]),
        ("b_destination_borrow", values["destination_borrow"]),
        ("b_element_size", values["element_size"]),
        ("b_element_alignment", values["element_alignment"]),
        ("b_clone_argument", _int_array(values["clone_argument"])),
        ("b_clone_result", _clone_array(values["clone_result"])),
        ("b_clone_state_before", _int_array(values["clone_before"], 100)),
        ("b_clone_state_after", _int_array(values["clone_after"], 100)),
        ("b_clone_outcome", outcomes),
    ]
    if config.is_fill:
        pairs.extend(
            (
                ("b_fill_value", values["fill_value"]),
                ("b_miri", _bool(values["miri"])),
                ("b_static_known", _bool(values["static_known"])),
            )
        )
    else:
        pairs.extend(
            (
                ("b_source_values", _int_array(values["source"])),
                ("b_source_address", values["source_address"]),
                ("b_source_allocation", values["source_allocation"]),
                ("b_source_provenance", values["source_provenance"]),
            )
        )
    return [f"(assert (= ({selector} b) {value}))" for selector, value in pairs]


def _instance_assertions(
    config: CloneEffectTarget,
    case: SourceCase,
    *,
    broken_state_chain: bool = False,
) -> list[str]:
    values = _case_values(
        config,
        case,
        broken_state_chain=broken_state_chain,
    )
    intrinsic_count = expected_intrinsic_call_count(config, case)
    assignment_count = (
        1
        if case.expected_path == PATH_FILL_DEFAULT and case.length > 0
        else case.length
        if case.expected_path
        in {PATH_FILL_TRIVIAL_READ, PATH_FILL_INTEGER_LOOP}
        else 0
    )
    assertions = [
        *_input_assertions(values),
        *_boundary_assertions(config, values),
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
        "(assert (Spec_T x b y1 s1))",
        (
            "(assert (= (s_selected_path s1) "
            f"{case.expected_path}))"
        ),
        (
            "(assert (= (s_clone_call_count s1) "
            f"{values['callback_count']}))"
        ),
        f"(assert (= (s_write_count s1) {case.length}))",
        (
            "(assert (= (s_intrinsic_call_count s1) "
            f"{intrinsic_count}))"
        ),
        (
            "(assert (= (s_assignment_count s1) "
            f"{assignment_count}))"
        ),
    ]
    if config.is_fill:
        assertions.append(
            "(assert (= (s_final_slot_moved s1) "
            + _bool(case.type_kind == TYPE_GENERIC and case.length > 0)
            + "))"
        )
    if case.relation_valued and case.length > 0:
        assertions.extend(
            (
                (
                    "(assert (distinct "
                    "(select (y_final_values y1) 0) "
                    "(SourceValueAt x 0)))"
                ),
                "(assert (Cloned_T x b 0 (SourceValueAt x 0) "
                "(select (y_final_values y1) 0)))",
            )
        )
    return assertions


def _compact_specialized_fill_instance_text(case: SourceCase) -> str:
    intrinsic_count = expected_intrinsic_call_count(TARGET_043, case)
    assignment_count = (
        case.length
        if case.expected_path
        in {PATH_FILL_TRIVIAL_READ, PATH_FILL_INTEGER_LOOP}
        else 0
    )
    return f"""\
; Bounded source witness for core::slice::fill specialization {case.name}.
; The arbitrary-length theorem carries the quantified cloned<T> relation.
; This fixed branch has no Clone callback: TrivialClone/primitive cloning is
; reflexive and the source writes the input value to every destination slot.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_length Int)
      (x_fill_value Int)
      (x_type_kind Int)
      (x_miri Bool)
      (x_uniform_bytes Bool)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_static_known Bool)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_final_values (Array Int Int))
      (y_selected_path Int)
      (y_clone_call_count Int)
      (y_write_count Int)
      (y_intrinsic_call_count Int)
      (y_assignment_count Int)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y Output)
(define-fun SelectedSpecializationPath ((x Input) (b Boundary)) Int
  (ite (= (x_type_kind x) {TYPE_TRIVIAL}) {PATH_FILL_TRIVIAL_READ}
    (ite (= (x_type_kind x) {TYPE_U8}) {PATH_FILL_U8_BYTES}
      (ite (= (x_type_kind x) {TYPE_I8}) {PATH_FILL_I8_BYTES}
        (ite
          (and
            (or
              (and (x_miri x) (> (x_length x) 32))
              (b_static_known b))
            (x_uniform_bytes x))
          {PATH_FILL_INTEGER_BYTES}
          {PATH_FILL_INTEGER_LOOP})))))
(define-fun Cloned_T ((source Int) (result Int)) Bool
  (= result source))
(define-fun WriteIndexAtStep ((step Int)) Int
  step)
(define-fun SpecializedSourceExecution
  ((x Input) (b Boundary) (y Output)) Bool
  (and
    (= (y_final_values y)
       ((as const (Array Int Int)) (x_fill_value x)))
    (= (y_selected_path y) (SelectedSpecializationPath x b))
    (= (y_clone_call_count y) 0)
    (= (y_write_count y) (x_length x))
    (= (y_intrinsic_call_count y) {intrinsic_count})
    (= (y_assignment_count y) {assignment_count})
    (= (WriteIndexAtStep 0) 0)
    (= (WriteIndexAtStep (ite (> (x_length x) 0)
                             (- (x_length x) 1)
                             0))
       (ite (> (x_length x) 0) (- (x_length x) 1) 0))
    (=> (> (x_length x) 0)
        (Cloned_T
          (x_fill_value x)
          (select (y_final_values y) (- (x_length x) 1))))))
(assert (= (x_length x) {case.length}))
(assert (= (x_fill_value x) 77))
(assert (= (x_type_kind x) {case.type_kind}))
(assert (= (x_miri x) {_bool(case.miri)}))
(assert (= (x_uniform_bytes x) {_bool(case.uniform_bytes)}))
(assert (= (b_static_known b) {_bool(case.static_known)}))
(assert (SpecializedSourceExecution x b y))
(assert (= (y_selected_path y) {case.expected_path}))
(check-sat)
(get-model)
"""


def _compact_zero_callback_instance_text(
    config: CloneEffectTarget,
    case: SourceCase,
) -> str:
    values = _case_values(config, case)
    final_values = _int_array(values["destination"])
    for index in range(case.length):
        source_value = 77 if config.is_fill else values["source"][index]
        final_values = f"(store {final_values} {index} {source_value})"
    if config.is_fill:
        path_body = f"""\
(ite (= (x_type_kind x) {TYPE_GENERIC}) {PATH_FILL_DEFAULT}
  (ite (= (x_type_kind x) {TYPE_TRIVIAL}) {PATH_FILL_TRIVIAL_READ}
    (ite (= (x_type_kind x) {TYPE_U8}) {PATH_FILL_U8_BYTES}
      (ite (= (x_type_kind x) {TYPE_I8}) {PATH_FILL_I8_BYTES}
        (ite
          (and
            (or
              (and (x_miri x) (> (x_length x) 32))
              (b_static_known b))
            (x_uniform_bytes x))
          {PATH_FILL_INTEGER_BYTES}
          {PATH_FILL_INTEGER_LOOP})))))"""
    else:
        path_body = (
            f"(ite (= (x_type_kind x) {TYPE_GENERIC}) "
            f"{PATH_CLONE_DEFAULT} {PATH_CLONE_TRIVIAL_COPY})"
        )
    intrinsic_count = expected_intrinsic_call_count(config, case)
    assignment_count = (
        1
        if case.expected_path == PATH_FILL_DEFAULT and case.length > 0
        else case.length
        if case.expected_path
        in {PATH_FILL_TRIVIAL_READ, PATH_FILL_INTEGER_LOOP}
        else 0
    )
    source_relations = [
        (
            f"(Cloned_T {77 if config.is_fill else values['source'][index]} "
            f"(select (y_final_values y) {index}))"
        )
        for index in range(case.length)
    ]
    return f"""\
; Exact zero-callback source witness for {config.target}: {case.name}.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_length Int)
      (x_source_length Int)
      (x_type_kind Int)
      (x_miri Bool)
      (x_uniform_bytes Bool)
      (x_element_size Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_static_known Bool)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_final_values (Array Int Int))
      (y_selected_path Int)
      (y_clone_call_count Int)
      (y_write_count Int)
      (y_intrinsic_call_count Int)
      (y_assignment_count Int)
      (y_final_slot_moved Bool)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y Output)
(define-fun SelectedSpecializationPath ((x Input) (b Boundary)) Int
  {path_body})
(define-fun Cloned_T ((source Int) (result Int)) Bool
  (= result source))
(define-fun ZeroCallbackSourceExecution
  ((x Input) (b Boundary) (y Output)) Bool
  (and
    (= (y_final_values y) {final_values})
    (= (y_selected_path y) (SelectedSpecializationPath x b))
    (= (y_clone_call_count y) 0)
    (= (y_write_count y) (x_length x))
    (= (y_intrinsic_call_count y) {intrinsic_count})
    (= (y_assignment_count y) {assignment_count})
    (= (y_final_slot_moved y)
       {_bool(config.is_fill and case.type_kind == TYPE_GENERIC and case.length > 0)})
    {" ".join(source_relations) or "true"}))
(assert (= (x_length x) {case.length}))
(assert (= (x_source_length x) {case.length}))
(assert (= (x_type_kind x) {case.type_kind}))
(assert (= (x_miri x) {_bool(case.miri)}))
(assert (= (x_uniform_bytes x) {_bool(case.uniform_bytes)}))
(assert (= (x_element_size x) {case.element_size}))
(assert (= (b_static_known b) {_bool(case.static_known)}))
(assert (ZeroCallbackSourceExecution x b y))
(assert (= (y_selected_path y) {case.expected_path}))
(check-sat)
(get-model)
"""


def source_instance_text(
    config: CloneEffectTarget,
    case: SourceCase,
) -> str:
    if config.is_fill and case.type_kind != TYPE_GENERIC:
        return _compact_specialized_fill_instance_text(case)
    values = _case_values(config, case)
    if values["callback_count"] == 0:
        return _compact_zero_callback_instance_text(config, case)
    return (
        _bounded_model_text(config, PRIMARY, case)
        + "\n"
        + "\n".join(_instance_assertions(config, case))
        + "\n(check-sat)\n(get-model)\n"
    )


def negative_probe_names(config: CloneEffectTarget) -> tuple[str, ...]:
    common = (
        "mismatched_boundary",
        "wrong_callback_count",
        "broken_state_chain",
        "wrong_specialization_path",
    )
    if config.is_fill:
        return common + (
            "wrong_final_slot",
            "callback_on_specialized_path",
        )
    return common


def negative_probe_text(
    config: CloneEffectTarget,
    name: str,
) -> str:
    if name not in negative_probe_names(config):
        raise ValueError(f"{config.target}: unknown negative probe {name}")
    generic = next(
        case
        for case in SOURCE_CASES[config.artifact_id]
        if case.type_kind == TYPE_GENERIC and case.length >= 4
    )
    case = generic
    broken = name == "broken_state_chain"
    assertions = _instance_assertions(
        config,
        case,
        broken_state_chain=broken,
    )
    if name == "mismatched_boundary":
        assertions.append(
            "(assert (distinct (b_destination_address b) "
            "(x_destination_address x)))"
        )
    elif name == "wrong_callback_count":
        assertions.append(
            "(assert (distinct (s_clone_call_count s1) "
            "(CallbackOperationCount x)))"
        )
    elif name == "wrong_specialization_path":
        assertions.append(
            "(assert (distinct (s_selected_path s1) "
            f"{case.expected_path}))"
        )
    elif name == "wrong_final_slot":
        assertions.append(
            "(assert (distinct "
            "(select (y_final_values y1) "
            "(- (x_destination_length x) 1)) "
            "(x_fill_value x)))"
        )
    elif name == "callback_on_specialized_path":
        case = next(
            item
            for item in SOURCE_CASES[config.artifact_id]
            if item.type_kind == TYPE_U8 and item.length > 0
        )
        assertions = _instance_assertions(config, case)
        assertions.append(
            "(assert (= (select (b_clone_outcome b) 0) Completed))"
        )
    elif name != "broken_state_chain":
        raise AssertionError(name)
    return (
        _bounded_model_text(config, PRIMARY, case)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n"
    )


def _panic_definitions(config: CloneEffectTarget) -> str:
    return f"""\
(declare-datatypes ((PanicState 0))
  (((mkPanicState
      (p_destination_values (Array Int Int))
      (p_clone_state Int)
      (p_clone_call_count Int)
      (p_write_count Int)
      (p_panic_index Int)
      (p_selected_path Int)))))
(declare-const panic_index Int)
(declare-const p1 PanicState)
(declare-const p2 PanicState)
(define-fun ClonePanicsAt
  ((x Input) (b Boundary) (index Int)) Bool
  (and
    (= (CloneIndexAtStep x index) index)
    (= (select (b_clone_argument b) index)
       (ExpectedCloneArgument x index))
    (= (select (b_clone_outcome b) index) Panicked)
    (= (select (b_clone_state_before b) index)
       (ite
         (= index 0)
         (x_clone_initial_state x)
         (select (b_clone_state_after b) (- index 1))))))
(define-fun PanicBoundary_T
  ((x Input) (b Boundary) (index Int)) Bool
  (and
    (InputBoundaryObserved x b)
    (= (x_type_kind x) {TYPE_GENERIC})
    (>= index 0)
    (< index (CallbackOperationCount x))
    (CallbackCompletedThrough x b index)
    (ClonePanicsAt x b index)))
(define-fun PanicStorage
  ((x Input) (b Boundary) (index Int)) (Array Int Int)
  (store
    (WriteStorageAfterSteps x b index)
    index
    (cloned_value (select (b_clone_result b) index))))
(define-fun PanicTargetTransition
  ((x Input) (b Boundary) (index Int) (p PanicState)) Bool
  (and
    (PanicBoundary_T x b index)
    (= (p_destination_values p) (PanicStorage x b index))
    (= (p_clone_state p) (select (b_clone_state_after b) index))
    (= (p_clone_call_count p) (+ index 1))
    (= (p_write_count p) (+ index 1))
    (= (p_panic_index p) index)
    (= (p_selected_path p) (SelectedSpecializationPath x b))))
(define-fun PanicSpec_T
  ((x Input) (b Boundary) (index Int) (p PanicState)) Bool
  (PanicTargetTransition x b index p))
(define-fun PanicEquivalent_T
  ((left PanicState) (right PanicState)) Bool
  (and
    (= (p_destination_values left) (p_destination_values right))
    (= (p_clone_state left) (p_clone_state right))
    (= (p_clone_call_count left) (p_clone_call_count right))
    (= (p_write_count left) (p_write_count right))
    (= (p_panic_index left) (p_panic_index right))
    (= (p_selected_path left) (p_selected_path right))))"""


def panic_obligation_text(config: CloneEffectTarget) -> str:
    return (
        _model_text(config, PRIMARY, include_theorem=False)
        + "\n"
        + _panic_definitions(config)
        + """\

(assert
  (not
    (=>
      (and
        (Requires_T x)
        (PanicBoundary_T x b panic_index)
        (PanicSpec_T x b panic_index p1)
        (PanicSpec_T x b panic_index p2))
      (PanicEquivalent_T p1 p2))))
(check-sat)
"""
    )


def validate_panic_obligation(
    config: CloneEffectTarget,
    text: str,
) -> None:
    if parse_smt(text) != parse_smt(panic_obligation_text(config)):
        raise GuardError(f"{config.target}: panic-prefix obligation changed")


def panic_probe_text(
    config: CloneEffectTarget,
    panic_index: int,
) -> str:
    if panic_index < 0:
        raise ValueError("panic index must be nonnegative")
    length = max(4, panic_index + (2 if config.is_fill else 1))
    case = SourceCase(
        name=f"panic_at_{panic_index}",
        length=length,
        element_size=8,
        type_kind=TYPE_GENERIC,
        expected_path=(
            PATH_FILL_DEFAULT if config.is_fill else PATH_CLONE_DEFAULT
        ),
        relation_valued=True,
    )
    values = _case_values(config, case, panic_index=panic_index)
    assertions = [
        *_input_assertions(values),
        *_boundary_assertions(config, values),
        "(assert (Requires_T x))",
        f"(assert (PanicBoundary_T x b {panic_index}))",
        f"(assert (PanicSpec_T x b {panic_index} p1))",
        f"(assert (= (p_panic_index p1) {panic_index}))",
        f"(assert (= (p_clone_call_count p1) {panic_index + 1}))",
        f"(assert (= (p_write_count p1) {panic_index + 1}))",
        (
            "(assert (= (select (p_destination_values p1) "
            f"{panic_index}) "
            f"{values['clone_result'][panic_index]}))"
        ),
    ]
    return (
        _model_text(config, PRIMARY, include_theorem=False)
        + "\n"
        + _panic_definitions(config)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n(get-model)\n"
    )


def mismatch_obligation_text(config: CloneEffectTarget) -> str:
    if config.is_fill:
        raise ValueError("fill has no length-mismatch precondition panic")
    return (
        _model_text(config, PRIMARY, include_theorem=False)
        + """\

(declare-datatypes ((MismatchState 0))
  (((mkMismatchState
      (m_destination_values (Array Int Int))
      (m_clone_state Int)
      (m_clone_call_count Int)
      (m_write_count Int)
      (m_selected_path Int)))))
(declare-const m1 MismatchState)
(declare-const m2 MismatchState)
(define-fun MismatchRequires ((x Input)) Bool
  (and
    (>= (x_destination_length x) 0)
    (>= (x_source_length x) 0)
    (distinct (x_destination_length x) (x_source_length x))
    (or (= (x_type_kind x) 0) (= (x_type_kind x) 1))))
(define-fun MismatchPanicTransition
  ((x Input) (b Boundary) (m MismatchState)) Bool
  (and
    (InputBoundaryObserved x b)
    (= (m_destination_values m) (x_destination_values x))
    (= (m_clone_state m) (x_clone_initial_state x))
    (= (m_clone_call_count m) 0)
    (= (m_write_count m) 0)
    (= (m_selected_path m) (SelectedSpecializationPath x b))))
(define-fun MismatchSpec_T
  ((x Input) (b Boundary) (m MismatchState)) Bool
  (MismatchPanicTransition x b m))
(define-fun MismatchEquivalent_T
  ((left MismatchState) (right MismatchState)) Bool
  (and
    (= (m_destination_values left) (m_destination_values right))
    (= (m_clone_state left) (m_clone_state right))
    (= (m_clone_call_count left) (m_clone_call_count right))
    (= (m_write_count left) (m_write_count right))
    (= (m_selected_path left) (m_selected_path right))))
(assert
  (not
    (=>
      (and
        (MismatchRequires x)
        (InputBoundaryObserved x b)
        (MismatchSpec_T x b m1)
        (MismatchSpec_T x b m2))
      (MismatchEquivalent_T m1 m2))))
(check-sat)
"""
    )


def validate_mismatch_obligation(
    config: CloneEffectTarget,
    text: str,
) -> None:
    if parse_smt(text) != parse_smt(mismatch_obligation_text(config)):
        raise GuardError(f"{config.target}: mismatch-panic obligation changed")


def mismatch_probe_text(
    config: CloneEffectTarget,
    *,
    trivial: bool,
) -> str:
    if config.is_fill:
        raise ValueError("fill has no length-mismatch precondition panic")
    type_kind = TYPE_TRIVIAL if trivial else TYPE_GENERIC
    selected_path = (
        PATH_CLONE_TRIVIAL_COPY if trivial else PATH_CLONE_DEFAULT
    )
    return f"""\
; Length-mismatch panic witness for clone_from_slice.
; Both CloneFromSpec paths check lengths before callbacks or writes.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_destination_length Int)
      (x_source_length Int)
      (x_destination_values (Array Int Int))
      (x_type_kind Int)
      (x_clone_initial_state Int)))))
(declare-datatypes ((PanicState 0))
  (((mkPanicState
      (p_destination_values (Array Int Int))
      (p_clone_state Int)
      (p_clone_call_count Int)
      (p_write_count Int)
      (p_selected_path Int)))))
(declare-const x Input)
(declare-const p PanicState)
(define-fun MismatchPanicTransition
  ((x Input) (p PanicState)) Bool
  (and
    (distinct (x_destination_length x) (x_source_length x))
    (= (p_destination_values p) (x_destination_values x))
    (= (p_clone_state p) (x_clone_initial_state x))
    (= (p_clone_call_count p) 0)
    (= (p_write_count p) 0)
    (= (p_selected_path p)
       (ite (= (x_type_kind x) {TYPE_GENERIC})
            {PATH_CLONE_DEFAULT}
            {PATH_CLONE_TRIVIAL_COPY}))))
(assert (= (x_destination_length x) 3))
(assert (= (x_source_length x) 2))
(assert (= (x_destination_values x)
           (store
             (store ((as const (Array Int Int)) 0) 0 500)
             2
             502)))
(assert (= (x_type_kind x) {type_kind}))
(assert (= (x_clone_initial_state x) 100))
(assert (MismatchPanicTransition x p))
(assert (= (p_selected_path p) {selected_path}))
(assert (= (p_clone_call_count p) 0))
(assert (= (p_write_count p) 0))
(assert (= (p_destination_values p) (x_destination_values x)))
(check-sat)
(get-model)
"""


def validate_source_anchors(
    config: CloneEffectTarget,
    source_item: str,
    helper_source: str,
    vocabulary: str,
) -> None:
    normalized_item = " ".join(source_item.split())
    normalized_helper = " ".join(helper_source.split())
    normalized_vocabulary = " ".join(vocabulary.split())
    if config.is_fill:
        required_item = "specialize::SpecFill::spec_fill(self, value);"
        helper_fragments = (
            "if let Some((last, elems)) = self.split_last_mut()",
            "el.clone_from(&value);",
            "*last = value",
            "*item = unsafe { ptr::read(&value) };",
            "impl SpecFill<u8> for [u8]",
            "impl SpecFill<i8> for [i8]",
            "crate::intrinsics::write_bytes",
            "cfg!(miri) && self.len() > 32",
            "crate::intrinsics::is_val_statically_known(value)",
            "for item in self.iter_mut()",
        )
        vocabulary_fragment = (
            "slice_filled_with_clone<T: core::clone::Clone>"
        )
    else:
        required_item = "self.spec_clone_from(src);"
        helper_fragments = (
            "assert!(self.len() == src.len()",
            "let src = &src[..len];",
            "while idx < self.len()",
            "self[idx].clone_from(&src[idx]);",
            "T: [const] TrivialClone + [const] Destruct",
            "copy_from_slice_impl(self, src);",
        )
        vocabulary_fragment = "slice_cloned_from<T: core::clone::Clone>"
    if required_item not in normalized_item:
        raise GuardError(f"{config.target}: public source body changed")
    for fragment in helper_fragments:
        if " ".join(fragment.split()) not in normalized_helper:
            raise GuardError(
                f"{config.target}: helper/specialization path changed: {fragment}"
            )
    if (
        vocabulary_fragment not in normalized_vocabulary
        or "cloned::<T>" not in normalized_vocabulary
    ):
        raise GuardError(f"{config.target}: relation-valued vocabulary changed")


def boundary_manifest(config: CloneEffectTarget) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": _boundary_metadata(config),
        "admitted_retained_trust_site_ids": list(
            config.admitted_trust_site_ids
        ),
        "context_only_trust_site_ids": list(
            config.context_only_trust_site_ids
        ),
        "all_audited_trust_site_ids": list(config.all_trust_site_ids),
        "source_paths": [
            config.source_reference,
            config.helper_reference,
        ],
        "relation_vocabulary": {
            "name": (
                "slice_filled_with_clone"
                if config.is_fill
                else "slice_cloned_from"
            ),
            "element_relation": "cloned<T>",
            "replacement_with_equality": "forbidden",
        },
        "specialization_selection": (
            "fixed by input type; Miri is platform input and static-known is "
            "the only hidden intrinsic observation"
            if config.is_fill
            else "fixed by whether the input type selects default Clone or TrivialClone"
        ),
        "excluded_from_boundary": [
            "aggregate destination storage",
            "final callback state",
            "operation order or count",
            "selected specialization result",
            "answer-bearing relation",
            "complete execution trace",
        ],
        "panic_prefix": (
            "The successful prefix is folded in increasing index order. The "
            "panicking clone's b_clone_result cell records only that lower "
            "element's unwind-visible partial destination value."
        ),
    }


def verus_text(config: CloneEffectTarget) -> str:
    if config.is_fill:
        return _fill_verus_text(config)
    return _clone_from_verus_text(config)


def _clone_from_verus_text(config: CloneEffectTarget) -> str:
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free source-transition model for {config.target}.

use vstd::prelude::*;
use vstd::seq::*;

verus! {{

pub ghost enum TypeKind {{
    GenericClone,
    TrivialClone,
}}

pub ghost struct Input {{
    pub destination: Seq<int>,
    pub source: Seq<int>,
    pub kind: TypeKind,
    pub clone_initial_state: int,
}}

pub ghost struct Boundary {{
    pub clone_argument: Seq<int>,
    pub clone_result: Seq<int>,
    pub clone_state_before: Seq<int>,
    pub clone_state_after: Seq<int>,
    pub clone_completed: Seq<bool>,
    pub clone_panicked: Seq<bool>,
    pub clone_panic_value: Seq<int>,
}}

pub ghost struct Output {{
    pub final_values: Seq<int>,
}}

pub ghost struct FinalState {{
    pub destination: Seq<int>,
    pub source: Seq<int>,
    pub clone_state: int,
    pub clone_call_count: nat,
    pub write_count: nat,
    pub intrinsic_call_count: nat,
    pub assignment_count: nat,
    pub selected_path: int,
}}

pub open spec fn callback_count(input: Input) -> nat {{
    match input.kind {{
        TypeKind::GenericClone => input.source.len(),
        TypeKind::TrivialClone => 0nat,
    }}
}}

pub open spec fn intrinsic_call_count(input: Input) -> nat {{
    match input.kind {{
        TypeKind::GenericClone => 0nat,
        TypeKind::TrivialClone => 1nat,
    }}
}}

pub open spec fn assignment_count(input: Input) -> nat {{
    0nat
}}

pub open spec fn cloned_relation_at(
    input: Input,
    boundary: Boundary,
    index: int,
    source: int,
    result: int,
) -> bool {{
    match input.kind {{
        TypeKind::GenericClone =>
            boundary.clone_argument[index] == source
                && boundary.clone_result[index] == result,
        TypeKind::TrivialClone => result == source,
    }}
}}

pub open spec fn source_result_at(
    input: Input,
    boundary: Boundary,
    index: int,
) -> int {{
    match input.kind {{
        TypeKind::GenericClone => boundary.clone_result[index],
        TypeKind::TrivialClone => input.source[index],
    }}
}}

pub open spec fn source_values(
    input: Input,
    boundary: Boundary,
) -> Seq<int> {{
    Seq::new(input.source.len(), |index: int|
        source_result_at(input, boundary, index))
}}

pub open spec fn callback_chain(input: Input, boundary: Boundary) -> bool {{
    boundary.clone_argument.len() >= callback_count(input)
        && boundary.clone_result.len() >= callback_count(input)
        && boundary.clone_state_before.len() >= callback_count(input)
        && boundary.clone_state_after.len() >= callback_count(input)
        && boundary.clone_completed.len() >= callback_count(input)
        && boundary.clone_panicked.len() >= callback_count(input)
        && forall|index: int| #![auto] 0 <= index < callback_count(input) ==>
            boundary.clone_argument[index] == input.source[index]
            && boundary.clone_completed[index]
            && !boundary.clone_panicked[index]
            && boundary.clone_state_before[index]
                == if index == 0 {{
                    input.clone_initial_state
                }} else {{
                    boundary.clone_state_after[index - 1]
                }}
}}

pub open spec fn active_slice_cloned_from(
    input: Input,
    boundary: Boundary,
    output: Output,
) -> bool {{
    output.final_values.len() == input.source.len()
        && forall|index: int| #![auto] 0 <= index < input.source.len() ==>
            cloned_relation_at(
                input,
                boundary,
                index,
                input.source[index],
                output.final_values[index],
            )
}}

pub open spec fn source_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    input.destination.len() == input.source.len()
        && callback_chain(input, boundary)
        && output.final_values == source_values(input, boundary)
        && state.destination == source_values(input, boundary)
        && state.source == input.source
        && state.clone_state
            == if callback_count(input) == 0 {{
                input.clone_initial_state
            }} else {{
                boundary.clone_state_after[callback_count(input) - 1]
            }}
        && state.clone_call_count == callback_count(input)
        && state.write_count == input.destination.len()
        && state.intrinsic_call_count == intrinsic_call_count(input)
        && state.assignment_count == assignment_count(input)
        && state.selected_path
            == match input.kind {{
                TypeKind::GenericClone => {PATH_CLONE_DEFAULT}int,
                TypeKind::TrivialClone => {PATH_CLONE_TRIVIAL_COPY}int,
            }}
}}

pub open spec fn panic_prefix(
    input: Input,
    boundary: Boundary,
    panic_index: int,
) -> bool {{
    matches!(input.kind, TypeKind::GenericClone)
        && 0 <= panic_index < callback_count(input)
        && boundary.clone_panicked.len() > panic_index
        && boundary.clone_panic_value.len() > panic_index
        && boundary.clone_panicked[panic_index]
        && forall|index: int| #![auto] 0 <= index < panic_index ==>
            boundary.clone_completed[index]
            && !boundary.clone_panicked[index]
            &&
            cloned_relation_at(
                input,
                boundary,
                index,
                input.source[index],
                boundary.clone_result[index],
            )
}}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    source_transition(input, boundary, output, state)
        && active_slice_cloned_from(input, boundary, output)
}}

pub open spec fn exact_equivalent(
    left: Output,
    left_state: FinalState,
    right: Output,
    right_state: FinalState,
) -> bool {{
    left.final_values == right.final_values
        && left_state.destination == right_state.destination
        && left_state.source == right_state.source
        && left_state.clone_state == right_state.clone_state
        && left_state.clone_call_count == right_state.clone_call_count
        && left_state.write_count == right_state.write_count
        && left_state.intrinsic_call_count == right_state.intrinsic_call_count
        && left_state.assignment_count == right_state.assignment_count
        && left_state.selected_path == right_state.selected_path
}}

pub proof fn conditional_complete_clone_from_slice(
    input: Input,
    boundary: Boundary,
    output1: Output,
    state1: FinalState,
    output2: Output,
    state2: FinalState,
)
    requires
        target_transition(input, boundary, output1, state1),
        target_transition(input, boundary, output2, state2),
    ensures
        exact_equivalent(output1, state1, output2, state2),
{{
    reveal(target_transition);
    reveal(source_transition);
    reveal(exact_equivalent);
}}

}} // verus!
"""


def _fill_verus_text(config: CloneEffectTarget) -> str:
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free source-transition model for {config.target}.

use vstd::prelude::*;
use vstd::seq::*;

verus! {{

pub ghost enum TypeKind {{
    GenericClone,
    TrivialClone,
    U8,
    I8,
    Integer,
}}

pub ghost struct Input {{
    pub destination: Seq<int>,
    pub value: int,
    pub kind: TypeKind,
    pub miri: bool,
    pub value_has_uniform_bytes: bool,
    pub clone_initial_state: int,
}}

pub ghost struct Boundary {{
    pub clone_argument: Seq<int>,
    pub clone_result: Seq<int>,
    pub clone_state_before: Seq<int>,
    pub clone_state_after: Seq<int>,
    pub clone_completed: Seq<bool>,
    pub clone_panicked: Seq<bool>,
    pub clone_panic_value: Seq<int>,
    pub static_known: bool,
}}

pub ghost struct Output {{
    pub final_values: Seq<int>,
}}

pub ghost struct FinalState {{
    pub destination: Seq<int>,
    pub clone_state: int,
    pub clone_call_count: nat,
    pub write_count: nat,
    pub intrinsic_call_count: nat,
    pub assignment_count: nat,
    pub selected_path: int,
    pub final_slot_moved: bool,
}}

pub open spec fn callback_count(input: Input) -> nat {{
    match input.kind {{
        TypeKind::GenericClone =>
            if input.destination.len() == 0 {{
                0nat
            }} else {{
                (input.destination.len() - 1) as nat
            }},
        _ => 0nat,
    }}
}}

pub open spec fn selected_path(input: Input, boundary: Boundary) -> int {{
    match input.kind {{
        TypeKind::GenericClone => {PATH_FILL_DEFAULT}int,
        TypeKind::TrivialClone => {PATH_FILL_TRIVIAL_READ}int,
        TypeKind::U8 => {PATH_FILL_U8_BYTES}int,
        TypeKind::I8 => {PATH_FILL_I8_BYTES}int,
        TypeKind::Integer =>
            if ((input.miri && input.destination.len() > 32nat)
                    || boundary.static_known)
                && input.value_has_uniform_bytes
            {{
                {PATH_FILL_INTEGER_BYTES}int
            }} else {{
                {PATH_FILL_INTEGER_LOOP}int
            }},
    }}
}}

pub open spec fn intrinsic_call_count(
    input: Input,
    boundary: Boundary,
) -> nat {{
    match input.kind {{
        TypeKind::U8 | TypeKind::I8 => 1nat,
        TypeKind::Integer =>
            (if input.miri && input.destination.len() > 32nat {{
                0nat
            }} else {{
                1nat
            }})
            + (if selected_path(input, boundary)
                    == {PATH_FILL_INTEGER_BYTES}int {{
                1nat
            }} else {{
                0nat
            }}),
        _ => 0nat,
    }}
}}

pub open spec fn assignment_count(
    input: Input,
    boundary: Boundary,
) -> nat {{
    match input.kind {{
        TypeKind::GenericClone =>
            if input.destination.len() == 0 {{ 0nat }} else {{ 1nat }},
        TypeKind::TrivialClone => input.destination.len(),
        TypeKind::Integer =>
            if selected_path(input, boundary) == {PATH_FILL_INTEGER_LOOP}int {{
                input.destination.len()
            }} else {{
                0nat
            }},
        _ => 0nat,
    }}
}}

pub open spec fn index_uses_clone(input: Input, index: int) -> bool {{
    matches!(input.kind, TypeKind::GenericClone)
        && 0 <= index < callback_count(input)
}}

pub open spec fn cloned_relation_at(
    input: Input,
    boundary: Boundary,
    index: int,
    source: int,
    result: int,
) -> bool {{
    if index_uses_clone(input, index) {{
        boundary.clone_argument[index] == source
            && boundary.clone_result[index] == result
    }} else {{
        result == source
    }}
}}

pub open spec fn source_result_at(
    input: Input,
    boundary: Boundary,
    index: int,
) -> int {{
    if index_uses_clone(input, index) {{
        boundary.clone_result[index]
    }} else {{
        input.value
    }}
}}

pub open spec fn source_values(
    input: Input,
    boundary: Boundary,
) -> Seq<int> {{
    Seq::new(input.destination.len(), |index: int|
        source_result_at(input, boundary, index))
}}

pub open spec fn callback_chain(input: Input, boundary: Boundary) -> bool {{
    boundary.clone_argument.len() >= callback_count(input)
        && boundary.clone_result.len() >= callback_count(input)
        && boundary.clone_state_before.len() >= callback_count(input)
        && boundary.clone_state_after.len() >= callback_count(input)
        && boundary.clone_completed.len() >= callback_count(input)
        && boundary.clone_panicked.len() >= callback_count(input)
        && forall|index: int| #![auto] 0 <= index < callback_count(input) ==>
            boundary.clone_argument[index] == input.value
            && boundary.clone_completed[index]
            && !boundary.clone_panicked[index]
            && boundary.clone_state_before[index]
                == if index == 0 {{
                    input.clone_initial_state
                }} else {{
                    boundary.clone_state_after[index - 1]
                }}
}}

pub open spec fn active_slice_filled_with_clone(
    input: Input,
    boundary: Boundary,
    output: Output,
) -> bool {{
    output.final_values.len() == input.destination.len()
        && forall|index: int| #![auto] 0 <= index < input.destination.len() ==>
            cloned_relation_at(
                input,
                boundary,
                index,
                input.value,
                output.final_values[index],
            )
}}

pub open spec fn source_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    callback_chain(input, boundary)
        && output.final_values == source_values(input, boundary)
        && state.destination == source_values(input, boundary)
        && state.clone_state
            == if callback_count(input) == 0 {{
                input.clone_initial_state
            }} else {{
                boundary.clone_state_after[callback_count(input) - 1]
            }}
        && state.clone_call_count == callback_count(input)
        && state.write_count == input.destination.len()
        && state.intrinsic_call_count
            == intrinsic_call_count(input, boundary)
        && state.assignment_count == assignment_count(input, boundary)
        && state.selected_path == selected_path(input, boundary)
        && state.final_slot_moved
            == (matches!(input.kind, TypeKind::GenericClone)
                && input.destination.len() > 0)
}}

pub open spec fn panic_prefix(
    input: Input,
    boundary: Boundary,
    panic_index: int,
) -> bool {{
    matches!(input.kind, TypeKind::GenericClone)
        && 0 <= panic_index < callback_count(input)
        && boundary.clone_panicked.len() > panic_index
        && boundary.clone_panic_value.len() > panic_index
        && boundary.clone_panicked[panic_index]
        && forall|index: int| #![auto] 0 <= index < panic_index ==>
            boundary.clone_completed[index]
            && !boundary.clone_panicked[index]
            &&
            cloned_relation_at(
                input,
                boundary,
                index,
                input.value,
                boundary.clone_result[index],
            )
}}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    source_transition(input, boundary, output, state)
        && active_slice_filled_with_clone(input, boundary, output)
}}

pub open spec fn exact_equivalent(
    left: Output,
    left_state: FinalState,
    right: Output,
    right_state: FinalState,
) -> bool {{
    left.final_values == right.final_values
        && left_state.destination == right_state.destination
        && left_state.clone_state == right_state.clone_state
        && left_state.clone_call_count == right_state.clone_call_count
        && left_state.write_count == right_state.write_count
        && left_state.intrinsic_call_count == right_state.intrinsic_call_count
        && left_state.assignment_count == right_state.assignment_count
        && left_state.selected_path == right_state.selected_path
        && left_state.final_slot_moved == right_state.final_slot_moved
}}

pub proof fn conditional_complete_fill(
    input: Input,
    boundary: Boundary,
    output1: Output,
    state1: FinalState,
    output2: Output,
    state2: FinalState,
)
    requires
        target_transition(input, boundary, output1, state1),
        target_transition(input, boundary, output2, state2),
    ensures
        exact_equivalent(output1, state1, output2, state2),
{{
    reveal(target_transition);
    reveal(source_transition);
    reveal(exact_equivalent);
}}

}} // verus!
"""
