#!/usr/bin/env python3
"""Re-run typechecking and determinism on final generated contracts."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import re
import sys
from typing import Any

WORKSPACE = Path(__file__).resolve().parent
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

import run_rust_std_spec_feedback as runner
from spec_determinism.view.registry import ViewRegistry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_summary", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--vstd-root",
        type=Path,
        default=WORKSPACE / "verus" / "source" / "vstd",
    )
    parser.add_argument(
        "--verus-bin",
        type=Path,
        default=WORKSPACE
        / "verus"
        / "source"
        / "target-verus"
        / "release"
        / "verus",
    )
    parser.add_argument(
        "--z3-path",
        type=Path,
        default=WORKSPACE / "verus" / "source" / "z3",
    )
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--rlimit", type=float, default=30)
    return parser.parse_args()


def is_rechecked(final: dict[str, Any]) -> bool:
    checker = final.get("checker") or {}
    return bool(final.get("rechecked") and checker.get("typecheck"))


def candidate_from_record(record: dict[str, Any]) -> dict[str, Any]:
    return record.get("candidate") or {}


def is_add_spec_candidate(candidate: dict[str, Any]) -> bool:
    return candidate.get("decision") == "add_spec" and bool(
        candidate.get("contract_code")
    )


def is_forced_source_skip_record(record: dict[str, Any]) -> bool:
    candidate = candidate_from_record(record)
    return (
        record.get("round") == "source_skip"
        and candidate.get("decision") == "skip"
        and record.get("soundness_status") == "source_backed_skip_no_contract"
    )


UNICODE_WHITE_SPACE_HELPER = """pub open spec fn str_unicode_white_space(c: char) -> bool {
    c == '\\u{0009}' || c == '\\u{000a}' || c == '\\u{000b}' ||
    c == '\\u{000c}' || c == '\\u{000d}' || c == '\\u{0020}' ||
    c == '\\u{0085}' || c == '\\u{00a0}' || c == '\\u{1680}' ||
    c == '\\u{2000}' || c == '\\u{2001}' || c == '\\u{2002}' ||
    c == '\\u{2003}' || c == '\\u{2004}' || c == '\\u{2005}' ||
    c == '\\u{2006}' || c == '\\u{2007}' || c == '\\u{2008}' ||
    c == '\\u{2009}' || c == '\\u{200a}' || c == '\\u{2028}' ||
    c == '\\u{2029}' || c == '\\u{202f}' || c == '\\u{205f}' ||
    c == '\\u{3000}'
}"""


def unicode_trim_start_contract(method: str) -> str:
    return f"""{UNICODE_WHITE_SPACE_HELPER}

pub assume_specification[ str::{method} ](s: &str) -> (result: &str)
    ensures
        result@ == ({{
            let start = choose|start: int|
                0 <= start
                && start <= s@.len()
                && (forall|i: int| 0 <= i < start ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (start == s@.len() || !str_unicode_white_space(s@[start]));
            s@.subrange(start, s@.len() as int)
        }}),
;"""


def unicode_trim_end_contract(method: str) -> str:
    return f"""{UNICODE_WHITE_SPACE_HELPER}

pub assume_specification[ str::{method} ](s: &str) -> (result: &str)
    ensures
        result@ == s@.subrange(0, result@.len() as int),
        result@.len() <= s@.len(),
        forall|i: int| result@.len() <= i < s@.len() ==> {{
            let c = #[trigger] s@[i];
            str_unicode_white_space(c)
        }},
        result@.len() > 0 ==> {{
            let c = result@[(result@.len() - 1) as int];
            !str_unicode_white_space(c)
        }},
;"""


def unicode_trim_contract() -> str:
    return f"""{UNICODE_WHITE_SPACE_HELPER}

pub assume_specification[ str::trim ](s: &str) -> (result: &str)
    ensures
        result@ == ({{
            let bounds = choose|bounds: (int, int)|
                0 <= bounds.0
                && bounds.0 <= bounds.1
                && bounds.1 <= s@.len()
                && (forall|i: int| 0 <= i < bounds.0 ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (forall|i: int| bounds.1 <= i < s@.len() ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (bounds.0 == bounds.1 || !str_unicode_white_space(s@[bounds.0]))
                && (bounds.0 == bounds.1 || !str_unicode_white_space(s@[bounds.1 - 1]));
            s@.subrange(bounds.0, bounds.1)
        }}),
;"""


UNICODE_TRIM_RECOVERY_CANDIDATES = {
    "core::str::trim_left": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": unicode_trim_start_contract("trim_left"),
        "requires": [],
        "ensures": [
            "result@ equals the suffix after removing the maximal leading Unicode White_Space run"
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 implements trim_left by delegating to trim_start, whose "
            "source removes leading char::is_whitespace characters. The helper "
            "enumerates the documented Unicode White_Space set and the choose "
            "expression gives one deterministic string view."
        ),
        "risks": [
            "The explicit Unicode White_Space enumeration must stay aligned with Rust's char::is_whitespace.",
            "The contract specifies the returned string view, not pointer identity or slice provenance.",
        ],
    },
    "core::str::trim_start": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": unicode_trim_start_contract("trim_start"),
        "requires": [],
        "ensures": [
            "result@ equals the suffix after removing the maximal leading Unicode White_Space run"
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 trim_start delegates to trim_start_matches(char::is_whitespace). "
            "The helper enumerates the documented Unicode White_Space set and the "
            "choose expression gives one deterministic string view."
        ),
        "risks": [
            "The explicit Unicode White_Space enumeration must stay aligned with Rust's char::is_whitespace.",
            "The contract specifies the returned string view, not pointer identity or slice provenance.",
        ],
    },
    "core::str::trim_end": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": unicode_trim_end_contract("trim_end"),
        "requires": [],
        "ensures": [
            "result@ is the maximal prefix left after removing trailing Unicode White_Space characters"
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 trim_end delegates to trim_end_matches(char::is_whitespace). "
            "The contract uses the accepted trim_ascii_end prefix/suffix shape "
            "with the documented Unicode White_Space set."
        ),
        "risks": [
            "The explicit Unicode White_Space enumeration must stay aligned with Rust's char::is_whitespace.",
            "The contract specifies the returned string view, not pointer identity or slice provenance.",
        ],
    },
    "core::str::trim": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": unicode_trim_contract(),
        "requires": [],
        "ensures": [
            "result@ equals the subrange after removing maximal leading and trailing Unicode White_Space runs"
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 trim removes leading and trailing char::is_whitespace "
            "characters. The helper enumerates the documented Unicode White_Space "
            "set and the choose expression gives one deterministic string view."
        ),
        "risks": [
            "The explicit Unicode White_Space enumeration must stay aligned with Rust's char::is_whitespace.",
            "The contract specifies the returned string view, not pointer identity or slice provenance.",
        ],
    },
}


STR_FROM_UTF8_SOURCE_RECOVERY_CANDIDATES = {
    "core::str::from_utf8": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification[ str::from_utf8 ](
    v: &[u8],
) -> (result: Result<&str, core::str::Utf8Error>)
    ensures
        valid_utf8(v@) ==> (result matches Ok(string) && string@ == decode_utf8(v@)),
        !valid_utf8(v@) ==> result is Err,
;""",
        "requires": [],
        "ensures": [
            (
                "valid_utf8(v@) ==> "
                "(result matches Ok(string) && string@ == decode_utf8(v@))"
            ),
            "!valid_utf8(v@) ==> result is Err",
        ],
        "feature_gates": [],
        "imports": ["vstd::utf8::{decode_utf8, valid_utf8}"],
        "useful": True,
        "rationale": (
            "Promotes the saved round-01 source-backed contract for the inherent "
            "`str::from_utf8` declaration only. Rust 1.96 delegates the inherent "
            "constructor to `converts::from_utf8`, whose body returns `Ok` after "
            "`run_utf8_validation` succeeds and `Err(err)` otherwise; the contract "
            "specifies only the decoded string view and Result branch."
        ),
        "risks": [
            "The contract is trusted and models the returned string view, not reference identity or provenance.",
            "It is accepted only for the single inherent `str::from_utf8` assume_specification, not a duplicate free-function spec.",
        ],
    }
}


SLICE_BINARY_SEARCH_SOURCE_RECOVERY_CANDIDATES = {
    "core::slice::binary_search": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T>[ <[T]>::binary_search ](
    v: &[T],
    x: &T,
) -> (result: Result<usize, usize>)
where
    T: Ord,
    requires
        obeys_cmp::<T>(),
        forall|i: int, j: int| 0 <= i < j < v@.len() ==>
            v@[i].cmp_spec(&v@[j]) != Ordering::Greater,
        forall|i: int, j: int|
            0 <= i < v@.len() && 0 <= j < v@.len()
            && v@[i].cmp_spec(x) == Ordering::Equal
            && v@[j].cmp_spec(x) == Ordering::Equal ==> i == j,
    ensures
        match result {
            Ok(i) => {
                &&& i < v@.len()
                &&& v@[i as int].cmp_spec(x) == Ordering::Equal
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) < j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
            Err(i) => {
                &&& i <= v@.len()
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) <= j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
        },
;""",
        "requires": [
            "obeys_cmp::<T>()",
            (
                "forall|i: int, j: int| 0 <= i < j < v@.len() ==>\n"
                "            v@[i].cmp_spec(&v@[j]) != Ordering::Greater"
            ),
            (
                "forall|i: int, j: int|\n"
                "            0 <= i < v@.len() && 0 <= j < v@.len()\n"
                "            && v@[i].cmp_spec(x) == Ordering::Equal\n"
                "            && v@[j].cmp_spec(x) == Ordering::Equal ==> i == j"
            ),
        ],
        "ensures": [
            """match result {
            Ok(i) => {
                &&& i < v@.len()
                &&& v@[i as int].cmp_spec(x) == Ordering::Equal
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) < j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
            Err(i) => {
                &&& i <= v@.len()
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) <= j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
        }"""
        ],
        "feature_gates": [],
        "imports": [
            "core::cmp::{Ord, Ordering}",
            "core::result::Result",
            "vstd::laws_cmp::obeys_cmp",
            "vstd::prelude::*",
            "vstd::std_specs::cmp::OrdSpec",
        ],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents slice::binary_search as a T: Ord wrapper around "
            "`self.binary_search_by(|p| p.cmp(x))`, returning the matching index "
            "or insertion index for sorted input while allowing any duplicate "
            "match. The uniqueness precondition removes only that documented "
            "duplicate-choice nondeterminism, so the Ok/Err partition is "
            "deterministic under obeys_cmp."
        ),
        "risks": [
            "The contract applies only when at most one slice element compares equal to the searched value.",
            "The runtime Ord implementation must agree with cmp_spec through obeys_cmp.",
            "This trusted external contract depends on the documented standard-library binary-search behavior.",
        ],
    },
}


SAFE_SLICE_CHUNK_SOURCE_RECOVERY_CANDIDATES = {
    "core::slice::as_chunks": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, const N: usize>[ <[T]>::as_chunks::<N> ](
    slice: &[T],
) -> (ret: (&[[T; N]], &[T]))
    requires
        N != 0,
    ensures
        {
            let chunks = choose|candidate: Seq<[T; N]>| {
                &&& candidate.len() == slice@.len() / (N as nat)
                &&& forall|i: int| 0 <= i < candidate.len() ==>
                    (#[trigger] candidate[i])@ == slice@.subrange(
                        i * (N as int),
                        (i + 1) * (N as int),
                    )
            };
            &&& ret.0@ == chunks
            &&& ret.0@.len() == slice@.len() / (N as nat)
            &&& ret.1@.len() == slice@.len() % (N as nat)
            &&& slice@.len() == ret.0@.len() * (N as nat) + ret.1@.len()
            &&& forall|i: int| 0 <= i < ret.0@.len() ==>
                (#[trigger] ret.0@[i])@ == slice@.subrange(
                    i * (N as int),
                    (i + 1) * (N as int),
                )
            &&& ret.1@ == slice@.subrange(
                ((slice@.len() / (N as nat)) * (N as nat)) as int,
                slice@.len() as int,
            )
        },
;""",
        "requires": ["N != 0"],
        "ensures": [
            (
                "{ let chunks = choose|candidate: Seq<[T; N]>| { &&& "
                "candidate.len() == slice@.len() / (N as nat) &&& "
                "forall|i: int| 0 <= i < candidate.len() ==> "
                "(#[trigger] candidate[i])@ == slice@.subrange(i * (N as int), "
                "(i + 1) * (N as int)) }; &&& ret.0@ == chunks &&& "
                "ret.0@.len() == slice@.len() / (N as nat) &&& "
                "ret.1@.len() == slice@.len() % (N as nat) &&& "
                "slice@.len() == ret.0@.len() * (N as nat) + ret.1@.len() &&& "
                "forall|i: int| 0 <= i < ret.0@.len() ==> "
                "(#[trigger] ret.0@[i])@ == slice@.subrange(i * (N as int), "
                "(i + 1) * (N as int)) &&& ret.1@ == slice@.subrange("
                "((slice@.len() / (N as nat)) * (N as nat)) as int, "
                "slice@.len() as int) }"
            )
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents and asserts that the safe API panics for N == 0, "
            "then splits at len / N * N and casts the exact multiple-of-N prefix. "
            "The choose-backed chunk sequence makes the returned views uniquely "
            "deterministic without specifying reference identity."
        ),
        "risks": [
            "The contract is trusted and models slice views, not pointer provenance.",
            "The nonzero precondition is accepted only as the documented normal-return domain.",
        ],
    },
    "core::slice::as_rchunks": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, const N: usize>[ <[T]>::as_rchunks::<N> ](
    slice: &[T],
) -> (ret: (&[T], &[[T; N]]))
    requires
        N != 0,
    ensures
        ret.0@ == slice@.subrange(
            0,
            (slice@.len() % (N as nat)) as int,
        ),
        ret.1@ == Seq::new(
            slice@.len() / (N as nat),
            |i: int| choose|chunk: [T; N]|
                chunk@ == slice@.subrange(
                    (slice@.len() % (N as nat)) as int + i * (N as int),
                    (slice@.len() % (N as nat)) as int + (i + 1) * (N as int),
                ),
        ),
        forall|i: int| i >= 0 && ret.1@.len() > i ==>
            (#[trigger] ret.1@[i])@ == slice@.subrange(
                (slice@.len() % (N as nat)) as int + i * (N as int),
                (slice@.len() % (N as nat)) as int + (i + 1) * (N as int),
            ),
;""",
        "requires": ["N != 0"],
        "ensures": [
            (
                "ret.0@ == slice@.subrange(0, (slice@.len() % (N as nat)) as int)"
            ),
            (
                "ret.1@ == Seq::new(slice@.len() / (N as nat), |i: int| "
                "choose|chunk: [T; N]| chunk@ == slice@.subrange("
                "(slice@.len() % (N as nat)) as int + i * (N as int), "
                "(slice@.len() % (N as nat)) as int + (i + 1) * (N as int)))"
            ),
            (
                "forall|i: int| i >= 0 && ret.1@.len() > i ==> "
                "(#[trigger] ret.1@[i])@ == slice@.subrange("
                "(slice@.len() % (N as nat)) as int + i * (N as int), "
                "(slice@.len() % (N as nat)) as int + (i + 1) * (N as int))"
            ),
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents and asserts that the safe reverse chunk API "
            "panics for N == 0, then splits off the len % N leading remainder and "
            "casts the exact multiple-of-N suffix. The Seq::new chunk view is "
            "deterministic and avoids reference-identity claims."
        ),
        "risks": [
            "The contract is trusted and models slice views, not pointer provenance.",
            "The nonzero precondition is accepted only as the documented normal-return domain.",
        ],
    },
}


MUT_SLICE_CHUNK_SOURCE_RECOVERY_CANDIDATES = {
    "core::slice::as_chunks_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, const N: usize>[ <[T]>::as_chunks_mut::<N> ](
    slice: &mut [T],
) -> (ret: (&mut [[T; N]], &mut [T]))
    requires
        N != 0,
    ensures
        {
            let chunks = choose|candidate: Seq<[T; N]>| {
                &&& candidate.len() == old(slice)@.len() / (N as nat)
                &&& forall|i: int| 0 <= i < candidate.len() ==>
                    (#[trigger] candidate[i])@ == old(slice)@.subrange(
                        i * (N as int),
                        (i + 1) * (N as int),
                    )
            };
            &&& ret.0@ == chunks
            &&& ret.0@.len() == old(slice)@.len() / (N as nat)
            &&& ret.1@ == old(slice)@.subrange(
                ((old(slice)@.len() / (N as nat)) * (N as nat)) as int,
                old(slice)@.len() as int,
            )
            &&& final(ret.0)@ == ret.0@
            &&& final(ret.1)@ == ret.1@
            &&& final(slice)@ == old(slice)@
        },
;""",
        "requires": ["N != 0"],
        "ensures": [
            (
                "{ let chunks = choose|candidate: Seq<[T; N]>| { &&& "
                "candidate.len() == old(slice)@.len() / (N as nat) &&& "
                "forall|i: int| 0 <= i < candidate.len() ==> "
                "(#[trigger] candidate[i])@ == old(slice)@.subrange(i * (N as int), "
                "(i + 1) * (N as int)) }; &&& ret.0@ == chunks &&& "
                "ret.0@.len() == old(slice)@.len() / (N as nat) &&& "
                "ret.1@ == old(slice)@.subrange("
                "((old(slice)@.len() / (N as nat)) * (N as nat)) as int, "
                "old(slice)@.len() as int) &&& final(ret.0)@ == ret.0@ &&& "
                "final(ret.1)@ == ret.1@ &&& final(slice)@ == old(slice)@ }"
            )
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents and asserts that the mutable safe chunk API "
            "panics for N == 0, then splits at len / N * N and casts the "
            "exact multiple-of-N prefix with as_chunks_unchecked_mut. The "
            "contract models the returned chunk/remainder views, preserves "
            "those returned mutable views at function return, and records the "
            "unchanged final input slice without pointer/provenance claims."
        ),
        "risks": [
            "The contract is trusted and models mutable semantic views, not reference identity.",
            "The nonzero precondition is accepted only as the documented normal-return domain.",
        ],
    },
    "core::slice::as_rchunks_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, const N: usize>[ <[T]>::as_rchunks_mut::<N> ](
    slice: &mut [T],
) -> (ret: (&mut [T], &mut [[T; N]]))
    requires
        N != 0,
    ensures
        ret.0@ == old(slice)@.subrange(
            0,
            (old(slice)@.len() % (N as nat)) as int,
        ),
        ret.1@ == Seq::new(
            old(slice)@.len() / (N as nat),
            |i: int| choose|chunk: [T; N]|
                chunk@ == old(slice)@.subrange(
                    (old(slice)@.len() % (N as nat)) as int + i * (N as int),
                    (old(slice)@.len() % (N as nat)) as int + (i + 1) * (N as int),
                ),
        ),
        forall|i: int| i >= 0 && ret.1@.len() > i ==>
            (#[trigger] ret.1@[i])@ == old(slice)@.subrange(
                (old(slice)@.len() % (N as nat)) as int + i * (N as int),
                (old(slice)@.len() % (N as nat)) as int + (i + 1) * (N as int),
            ),
        final(ret.0)@ == ret.0@,
        final(ret.1)@ == ret.1@,
        final(slice)@ == old(slice)@,
;""",
        "requires": ["N != 0"],
        "ensures": [
            (
                "ret.0@ == old(slice)@.subrange(0, "
                "(old(slice)@.len() % (N as nat)) as int)"
            ),
            (
                "ret.1@ == Seq::new(old(slice)@.len() / (N as nat), |i: int| "
                "choose|chunk: [T; N]| chunk@ == old(slice)@.subrange("
                "(old(slice)@.len() % (N as nat)) as int + i * (N as int), "
                "(old(slice)@.len() % (N as nat)) as int + (i + 1) * (N as int)))"
            ),
            (
                "forall|i: int| i >= 0 && ret.1@.len() > i ==> "
                "(#[trigger] ret.1@[i])@ == old(slice)@.subrange("
                "(old(slice)@.len() % (N as nat)) as int + i * (N as int), "
                "(old(slice)@.len() % (N as nat)) as int + (i + 1) * (N as int))"
            ),
            "final(ret.0)@ == ret.0@",
            "final(ret.1)@ == ret.1@",
            "final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents and asserts that the mutable reverse chunk API "
            "panics for N == 0, then splits off the len % N leading remainder "
            "and casts the exact multiple-of-N suffix with "
            "as_chunks_unchecked_mut. The contract models those deterministic "
            "returned views, preserves them at function return, and avoids "
            "reference-identity or provenance claims."
        ),
        "risks": [
            "The contract is trusted and models mutable semantic views, not reference identity.",
            "The nonzero precondition is accepted only as the documented normal-return domain.",
        ],
    },
}


BTREESET_SOURCE_RECOVERY_CANDIDATES = {
    "alloc::collections::BTreeSet::last": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<
    'a,
    T: core::cmp::Ord,
    A: alloc::alloc::Allocator + core::clone::Clone,
>[ alloc::collections::BTreeSet::<T, A>::last ](
    m: &'a alloc::collections::BTreeSet<T, A>,
) -> (result: core::option::Option<&'a T>)
    requires
        vstd::laws_cmp::obeys_cmp::<T>(),
    ensures
        match result {
            core::option::Option::Some(value) => {
                &&& !m@.is_empty()
                &&& *value == m@.find_unique_maximal(
                    |x: T, y: T| x.cmp_spec(&y) != core::cmp::Ordering::Greater,
                )
                &&& m@.contains(*value)
                &&& forall|x: T| #[trigger] m@.contains(x) ==>
                    x.cmp_spec(value) != core::cmp::Ordering::Greater
            },
            core::option::Option::None => m@.is_empty(),
        },
;""",
        "requires": ["vstd::laws_cmp::obeys_cmp::<T>()"],
        "ensures": [
            (
                "match result { core::option::Option::Some(value) => { &&& "
                "!m@.is_empty() &&& *value == m@.find_unique_maximal(|x: T, "
                "y: T| x.cmp_spec(&y) != core::cmp::Ordering::Greater,) &&& "
                "m@.contains(*value) &&& forall|x: T| #[trigger] "
                "m@.contains(x) ==> x.cmp_spec(value) != "
                "core::cmp::Ordering::Greater }, core::option::Option::None "
                "=> m@.is_empty(), }"
            )
        ],
        "feature_gates": ["allocator_api"],
        "imports": [
            "vstd::prelude::*",
            "vstd::set_lib::*",
            "vstd::std_specs::cmp::OrdSpec",
        ],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents BTreeSet::last as returning the set maximum "
            "and implements it by projecting the key from last_key_value. The "
            "prior deterministic shape identifies the returned semantic value "
            "with the unique maximal element instead of reference identity."
        ),
        "risks": [
            "The contract models the returned element value, not reference provenance.",
            "The comparator bridge relies on the source T: Ord bound and vstd obeys_cmp law.",
        ],
    },
    "alloc::collections::BTreeSet::pop_first": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T: Ord, A: Allocator + Clone>[ BTreeSet::<T, A>::pop_first ](
    m: &mut BTreeSet<T, A>,
) -> (result: Option<T>)
    requires
        obeys_cmp::<T>(),
    ensures
        if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let first = choose|candidate: T| {
                &&& old(m)@.contains(candidate)
                &&& forall|element: T| old(m)@.contains(element)
                    ==> candidate.cmp_spec(&element) != Ordering::Greater
            };
            &&& result == Some(first)
            &&& old(m)@.contains(first)
            &&& forall|element: T| old(m)@.contains(element)
                ==> first.cmp_spec(&element) != Ordering::Greater
            &&& final(m)@ == old(m)@.remove(first)
        },
;""",
        "requires": ["obeys_cmp::<T>()"],
        "ensures": [
            (
                "if old(m)@.is_empty() { &&& result is None &&& final(m)@ == "
                "old(m)@ } else { let first = choose|candidate: T| { &&& "
                "old(m)@.contains(candidate) &&& forall|element: T| "
                "old(m)@.contains(element) ==> candidate.cmp_spec(&element) "
                "!= Ordering::Greater }; &&& result == Some(first) &&& "
                "old(m)@.contains(first) &&& forall|element: T| "
                "old(m)@.contains(element) ==> first.cmp_spec(&element) != "
                "Ordering::Greater &&& final(m)@ == old(m)@.remove(first) }"
            )
        ],
        "feature_gates": ["allocator_api"],
        "imports": [
            "alloc::alloc::Allocator",
            "alloc::collections::BTreeSet",
            "core::cmp::Ordering",
            "vstd::laws_cmp::obeys_cmp",
            "vstd::prelude::*",
            "vstd::std_specs::cmp::OrdSpec",
        ],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents BTreeSet::pop_first as removing and returning "
            "the set minimum and implements it through map.pop_first. The prior "
            "deterministic shape chooses that minimum value and exposes exact "
            "post-state removal."
        ),
        "risks": [
            "Allocator side effects and panic behavior are intentionally outside the modeled postcondition.",
            "The comparator bridge relies on the source T: Ord bound and vstd obeys_cmp law.",
        ],
    },
}

RESULT_SOURCE_RECOVERY_CANDIDATES = {
    "core::result::Result::and": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, E, U>[ core::result::Result::<T, E>::and ](
    result: core::result::Result<T, E>,
    res: core::result::Result<U, E>,
) -> (and_result: core::result::Result<U, E>)
    ensures
        result is Ok ==> and_result == res,
        result is Err ==> and_result is Err && and_result->Err_0 == result->Err_0,
    no_unwind
;""",
        "requires": [],
        "ensures": [
            "result is Ok ==> and_result == res",
            "result is Err ==> and_result is Err && and_result->Err_0 == result->Err_0",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 implements Result::and by returning `res` in the Ok branch "
            "and returning the original Err payload in the Err branch. This uses "
            "the accepted Result::or-style direct variant postconditions and avoids "
            "a local when_used_as_spec helper."
        ),
        "risks": [
            "The contract specifies branch-visible Result values, not drop order or other unmodeled ownership effects.",
        ],
    },
}

HASHMAP_SOURCE_RECOVERY_CANDIDATES = {
    "std::collections::HashMap::get_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<
    'a,
    Key: std::borrow::Borrow<Q> + std::hash::Hash + Eq,
    Value,
    S: std::hash::BuildHasher,
    A: std::alloc::Allocator,
    Q: std::hash::Hash + Eq + ?Sized,
>[ std::collections::HashMap::<Key, Value, S, A>::get_mut::<Q> ](
    m: &'a mut std::collections::HashMap<Key, Value, S, A>,
    k: &Q,
) -> (result: Option<&'a mut Value>)
    requires
        obeys_key_model::<Key>(),
        builds_valid_hashers::<S>(),
    ensures
        {
            let old_map = old(m)@;
            let selected_key = choose|key: Key|
                sets_borrowed_key_to_key(old_map.dom(), k, &key);
            &&& contains_borrowed_key(old_map, k) ==>
                sets_borrowed_key_to_key(old_map.dom(), k, &selected_key)
            &&& result is Some == contains_borrowed_key(old_map, k)
            &&& match result {
                Some(v) => {
                    &&& *v == old_map[selected_key]
                    &&& *final(v) == *v
                    &&& final(m)@ == old_map
                },
                None => {
                    &&& !contains_borrowed_key(old_map, k)
                    &&& final(m)@ == old_map
                },
            }
        },
;""",
        "requires": [
            "obeys_key_model::<Key>()",
            "builds_valid_hashers::<S>()",
        ],
        "ensures": [
            (
                "{ let old_map = old(m)@; let selected_key = choose|key: Key| "
                "sets_borrowed_key_to_key(old_map.dom(), k, &key); &&& "
                "contains_borrowed_key(old_map, k) ==> "
                "sets_borrowed_key_to_key(old_map.dom(), k, &selected_key) &&& "
                "result is Some == contains_borrowed_key(old_map, k) &&& "
                "match result { Some(v) => { &&& *v == old_map[selected_key] "
                "&&& *final(v) == *v &&& final(m)@ == old_map }, "
                "None => { &&& !contains_borrowed_key(old_map, k) "
                "&&& final(m)@ == old_map } } }"
            )
        ],
        "feature_gates": ["allocator_api"],
        "imports": [
            (
                "vstd::std_specs::hash::{builds_valid_hashers, "
                "contains_borrowed_key, obeys_key_model, "
                "sets_borrowed_key_to_key}"
            )
        ],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents HashMap::get_mut as returning a mutable "
            "reference to the value for the borrowed key, requires borrowed-form "
            "Hash/Eq compatibility, and delegates to self.base.get_mut(k). The "
            "contract chooses the stored key selected by the borrowed-key model, "
            "returns the old value through the mutable reference when present, "
            "and records that the lookup itself does not mutate the map."
        ),
        "risks": [
            "The contract models the returned value and map view, not reference identity or provenance.",
            "The borrowed-key relation relies on the source Hash/Eq compatibility and BuildHasher bridge.",
        ],
    },
    "std::collections::HashMap::remove_entry": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<
    Key: std::borrow::Borrow<Q> + std::hash::Hash + Eq,
    Value,
    S: std::hash::BuildHasher,
    A: std::alloc::Allocator,
    Q: std::hash::Hash + Eq + ?Sized,
>[ std::collections::HashMap::<Key, Value, S, A>::remove_entry::<Q> ](
    m: &mut std::collections::HashMap<Key, Value, S, A>,
    k: &Q,
) -> (result: Option<(Key, Value)>)
    requires
        obeys_key_model::<Key>(),
        builds_valid_hashers::<S>(),
    ensures
        {
            let old_map = old(m)@;
            let removed_key = choose|key: Key|
                sets_borrowed_key_to_key(old_map.dom(), k, &key);
            &&& contains_borrowed_key(old_map, k) ==>
                sets_borrowed_key_to_key(old_map.dom(), k, &removed_key)
            &&& result == if contains_borrowed_key(old_map, k) {
                Some((removed_key, old_map[removed_key]))
            } else {
                None
            }
            &&& final(m)@ == if contains_borrowed_key(old_map, k) {
                old_map.remove(removed_key)
            } else {
                old_map
            }
        },
;""",
        "requires": [
            "obeys_key_model::<Key>()",
            "builds_valid_hashers::<S>()",
        ],
        "ensures": [
            (
                "{ let old_map = old(m)@; let removed_key = choose|key: Key| "
                "sets_borrowed_key_to_key(old_map.dom(), k, &key); &&& "
                "contains_borrowed_key(old_map, k) ==> "
                "sets_borrowed_key_to_key(old_map.dom(), k, &removed_key) &&& "
                "result == if contains_borrowed_key(old_map, k) { "
                "Some((removed_key, old_map[removed_key])) } else { None } &&& "
                "final(m)@ == if contains_borrowed_key(old_map, k) { "
                "old_map.remove(removed_key) } else { old_map } }"
            )
        ],
        "feature_gates": ["allocator_api"],
        "imports": [
            (
                "vstd::std_specs::hash::{builds_valid_hashers, "
                "contains_borrowed_key, obeys_key_model, "
                "sets_borrowed_key_to_key}"
            )
        ],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents HashMap::remove_entry as removing a borrowed "
            "key and returning the stored key-value pair, and the body delegates "
            "to self.base.remove_entry(k). The Hash/Eq/hasher preconditions are "
            "the vstd bridge that makes the borrowed-key model functional enough "
            "to identify the returned stored key and exact final map."
        ),
        "risks": [
            "The contract models the returned stored key/value and map view, not allocator effects.",
            "The borrowed-key relation relies on the source Hash/Eq compatibility and BuildHasher bridge.",
        ],
    },
}


BTREEMAP_SOURCE_RECOVERY_CANDIDATES = {
    "alloc::collections::BTreeMap::get_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<
    'a,
    Key: core::borrow::Borrow<Q> + core::cmp::Ord,
    Value,
    A: core::alloc::Allocator + core::clone::Clone,
    Q: core::cmp::Ord + ?Sized,
>[ alloc::collections::BTreeMap::<Key, Value, A>::get_mut::<Q> ](
    m: &'a mut alloc::collections::BTreeMap<Key, Value, A>,
    k: &Q,
) -> (result: core::option::Option<&'a mut Value>)
    requires
        obeys_cmp::<Key>(),
    ensures
        {
            let old_map = old(m)@;
            let selected_key = choose|key: Key|
                sets_borrowed_key_to_key(old_map.dom(), k, &key);
            &&& contains_borrowed_key(old_map, k) ==>
                sets_borrowed_key_to_key(old_map.dom(), k, &selected_key)
            &&& result is Some == contains_borrowed_key(old_map, k)
            &&& match result {
                Some(v) => {
                    &&& *v == old_map[selected_key]
                    &&& *final(v) == *v
                    &&& final(m)@ == old_map
                },
                None => {
                    &&& !contains_borrowed_key(old_map, k)
                    &&& final(m)@ == old_map
                },
            }
        },
;""",
        "requires": ["obeys_cmp::<Key>()"],
        "ensures": [
            (
                "{ let old_map = old(m)@; let selected_key = choose|key: Key| "
                "sets_borrowed_key_to_key(old_map.dom(), k, &key); &&& "
                "contains_borrowed_key(old_map, k) ==> "
                "sets_borrowed_key_to_key(old_map.dom(), k, &selected_key) &&& "
                "result is Some == contains_borrowed_key(old_map, k) &&& "
                "match result { Some(v) => { &&& *v == old_map[selected_key] "
                "&&& *final(v) == *v &&& final(m)@ == old_map }, "
                "None => { &&& !contains_borrowed_key(old_map, k) "
                "&&& final(m)@ == old_map } } }"
            )
        ],
        "feature_gates": ["allocator_api"],
        "imports": [
            "vstd::laws_cmp::obeys_cmp",
            (
                "vstd::std_specs::btree::{contains_borrowed_key, "
                "sets_borrowed_key_to_key}"
            ),
        ],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents BTreeMap::get_mut as returning a mutable "
            "reference to the value for the borrowed key, requires borrowed-form "
            "ordering to match the key ordering, and implements the lookup by "
            "search_tree(key) with Found(handle) returning handle.into_val_mut(). "
            "The contract chooses the stored key selected by the borrowed-key "
            "model, returns the old value through that mutable reference, and "
            "records that the lookup itself does not mutate the map."
        ),
        "risks": [
            "The contract models the returned value and map view, not reference identity or provenance.",
            "The borrowed-key relation relies on the source Ord compatibility and obeys_cmp bridge.",
        ],
    },
}


SLICE_SPLIT_AT_MUT_UNCHECKED_SOURCE_RECOVERY_CANDIDATES = {
    "core::slice::split_at_mut_unchecked": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T>[ <[T]>::split_at_mut_unchecked ](
    slice: &mut [T],
    mid: usize,
) -> (ret: (&mut [T], &mut [T]))
    requires
        mid as int <= old(slice)@.len(),
    ensures
        ret.0@ == old(slice)@.subrange(0, mid as int),
        ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int),
        final(ret.0)@ == ret.0@,
        final(ret.1)@ == ret.1@,
        final(slice)@ == final(ret.0)@ + final(ret.1)@,
;""",
        "requires": ["mid as int <= old(slice)@.len()"],
        "ensures": [
            "ret.0@ == old(slice)@.subrange(0, mid as int)",
            "ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int)",
            "final(ret.0)@ == ret.0@",
            "final(ret.1)@ == ret.1@",
            "final(slice)@ == final(ret.0)@ + final(ret.1)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents the unsafe precondition `0 <= mid <= self.len()`, "
            "checks `mid <= len`, then returns the prefix and suffix with "
            "`from_raw_parts_mut(ptr, mid)` and "
            "`from_raw_parts_mut(ptr.add(mid), unchecked_sub(len, mid))`. The "
            "contract models those prefix/suffix slice views, preserves the "
            "returned sub-slice contents at function return, and exposes the "
            "final concatenated input state without specifying reference provenance."
        ),
        "risks": [
            "The contract is trusted and models observable slice views, not pointer identity or aliasing provenance.",
            "It is accepted only for this exact source-backed unsafe precondition and prefix/suffix construction.",
        ],
    },
}

SLICE_SPLIT_AT_MUT_CHECKED_SOURCE_RECOVERY_CANDIDATES = {
    "core::slice::split_at_mut_checked": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T>[ <[T]>::split_at_mut_checked ](
    slice: &mut [T],
    mid: usize,
) -> (ret: Option<(&mut [T], &mut [T])>)
    ensures
        ret is Some == (mid <= old(slice)@.len()),
        ret matches Some((left, right)) ==> {
            &&& left@ == old(slice)@.subrange(0, mid as int)
            &&& right@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int)
            &&& final(left)@ == left@
            &&& final(right)@ == right@
            &&& final(slice)@ == final(left)@ + final(right)@
        },
        ret is None ==> final(slice)@ == old(slice)@,
;""",
        "requires": [],
        "ensures": [
            "ret is Some == (mid <= old(slice)@.len())",
            (
                "ret matches Some((left, right)) ==> { "
                "&&& left@ == old(slice)@.subrange(0, mid as int) "
                "&&& right@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int) "
                "&&& final(left)@ == left@ "
                "&&& final(right)@ == right@ "
                "&&& final(slice)@ == final(left)@ + final(right)@ }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 returns Some exactly when `mid <= self.len()`, delegates "
            "that branch to `self.split_at_mut_unchecked(mid)`, and otherwise "
            "returns None. The contract reuses the accepted split_at_checked "
            "Option shape, the accepted mutable split post-state preservation, "
            "and the unchanged input state on the None branch."
        ),
        "risks": [
            "The contract is trusted and models observable slice views, not pointer identity or aliasing provenance.",
            "It is accepted only for this exact source-backed checked split and Option branch shape.",
        ],
    },
}


STR_SPLIT_AT_CHECKED_SOURCE_RECOVERY_CANDIDATES = {
    "core::str::split_at_checked": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification[ str::split_at_checked ](
    s: &str,
    mid: usize,
) -> (ret: Option<(&str, &str)>)
    ensures
        ret.is_some() == is_char_boundary(s.spec_bytes(), mid as int),
        ret.is_some() ==> ret.unwrap().0.spec_bytes() == s.spec_bytes().subrange(0, mid as int),
        ret.is_some() ==> ret.unwrap().1.spec_bytes() == s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int),
;""",
        "requires": [],
        "ensures": [
            "ret.is_some() == is_char_boundary(s.spec_bytes(), mid as int)",
            (
                "ret.is_some() ==> ret.unwrap().0.spec_bytes() == "
                "s.spec_bytes().subrange(0, mid as int)"
            ),
            (
                "ret.is_some() ==> ret.unwrap().1.spec_bytes() == "
                "s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int)"
            ),
        ],
        "feature_gates": [],
        "imports": [
            "vstd::string::StringSliceAdditionalSpecFns",
            "vstd::utf8::is_char_boundary",
        ],
        "useful": True,
        "rationale": (
            "Rust 1.96 returns Some exactly when `self.is_char_boundary(mid)`, "
            "delegates that branch to `self.split_at_unchecked(mid)`, and "
            "otherwise returns None. The contract models only the returned "
            "immutable string slices' byte views as the source prefix and suffix, "
            "without claiming reference identity or provenance."
        ),
        "risks": [
            "The contract is trusted and models observable str bytes, not reference identity or provenance.",
            "It is accepted only for this exact source-backed checked split and byte-subrange shape.",
        ],
    },
}


STR_SPLIT_AT_MUT_CHECKED_SOURCE_RECOVERY_CANDIDATES = {
    "core::str::split_at_mut_checked": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification[ str::split_at_mut_checked ](
    s: &mut str,
    mid: usize,
) -> (ret: Option<(&mut str, &mut str)>)
    ensures
        ret is Some <==> is_char_boundary(old(s).spec_bytes(), mid as int),
        ret matches Some((left, right)) ==> {
            &&& left.spec_bytes() =~= old(s).spec_bytes().subrange(0, mid as int)
            &&& right.spec_bytes() =~= old(s).spec_bytes().subrange(mid as int, old(s).spec_bytes().len() as int)
            &&& final(left).spec_bytes() == left.spec_bytes()
            &&& final(right).spec_bytes() == right.spec_bytes()
            &&& final(s).spec_bytes() == final(left).spec_bytes() + final(right).spec_bytes()
        },
        ret is None ==> final(s).spec_bytes() == old(s).spec_bytes(),
;""",
        "requires": [],
        "ensures": [
            "ret is Some <==> is_char_boundary(old(s).spec_bytes(), mid as int)",
            (
                "ret matches Some((left, right)) ==> { "
                "&&& left.spec_bytes() =~= old(s).spec_bytes().subrange(0, mid as int) "
                "&&& right.spec_bytes() =~= old(s).spec_bytes().subrange(mid as int, old(s).spec_bytes().len() as int) "
                "&&& final(left).spec_bytes() == left.spec_bytes() "
                "&&& final(right).spec_bytes() == right.spec_bytes() "
                "&&& final(s).spec_bytes() == final(left).spec_bytes() + final(right).spec_bytes() }"
            ),
            "ret is None ==> final(s).spec_bytes() == old(s).spec_bytes()",
        ],
        "feature_gates": [],
        "imports": [
            "vstd::string::StringSliceAdditionalSpecFns",
            "vstd::utf8::is_char_boundary",
        ],
        "useful": True,
        "rationale": (
            "Rust 1.96 returns Some exactly when `self.is_char_boundary(mid)`, "
            "delegates that branch to `self.split_at_mut_unchecked(mid)`, and "
            "otherwise returns None. The contract models the returned mutable str "
            "slices extensionally by their byte subranges and preserves the input "
            "byte state on the None branch without claiming pointer provenance."
        ),
        "risks": [
            "The contract is trusted and models observable str bytes, not pointer identity or aliasing provenance.",
            "It is accepted only for this exact source-backed checked split and byte-subrange shape.",
        ],
    },
}


STRING_REPLACE_RANGE_SOURCE_RECOVERY_CANDIDATES = {
    "alloc::string::String::replace_range": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub open spec fn string_replace_range_snapshot<R: RangeBoundsSpec<usize>>(
    range: &R,
    len: nat,
) -> (int, int) {
    let start = match range.spec_start_bound() {
        SpecBound::Included(i) => *i as int,
        SpecBound::Excluded(i) => (*i as int) + 1,
        SpecBound::Unbounded => 0,
    };
    let end = match range.spec_end_bound() {
        SpecBound::Included(i) => (*i as int) + 1,
        SpecBound::Excluded(i) => *i as int,
        SpecBound::Unbounded => len as int,
    };
    (start, end)
}

pub open spec fn string_replace_range_valid<R: RangeBoundsSpec<usize>>(
    range: &R,
    old_bytes: Seq<u8>,
) -> bool {
    let snapshot = string_replace_range_snapshot(range, old_bytes.len());
    snapshot.0 <= snapshot.1
        && snapshot.1 <= old_bytes.len()
        && is_char_boundary(old_bytes, snapshot.0)
        && is_char_boundary(old_bytes, snapshot.1)
}

pub open spec fn string_replace_range_result<R: RangeBoundsSpec<usize>>(
    range: &R,
    old_bytes: Seq<u8>,
    replace_with: Seq<char>,
) -> Seq<char> {
    let snapshot = string_replace_range_snapshot(range, old_bytes.len());
    decode_utf8(
        old_bytes.subrange(0, snapshot.0)
            + encode_utf8(replace_with)
            + old_bytes.subrange(snapshot.1, old_bytes.len() as int),
    )
}

pub assume_specification<R>[ alloc::string::String::replace_range ](
    s: &mut alloc::string::String,
    range: R,
    replace_with: &str,
)
where
    R: core::ops::RangeBounds<usize>,
    requires
        string_replace_range_valid(&range, encode_utf8(old(s)@)),
    ensures
        final(s)@ == string_replace_range_result(&range, encode_utf8(old(s)@), replace_with@),
;""",
        "requires": [
            "string_replace_range_valid(&range, encode_utf8(old(s)@))",
        ],
        "ensures": [
            (
                "final(s)@ == string_replace_range_result(&range, "
                "encode_utf8(old(s)@), replace_with@)"
            ),
        ],
        "feature_gates": [],
        "imports": [
            "vstd::std_specs::range::{RangeBoundsSpec, SpecBound}",
            "vstd::utf8::{decode_utf8, encode_utf8, is_char_boundary}",
        ],
        "useful": True,
        "rationale": (
            "Rust 1.96 normalizes the generic RangeBounds value exactly once with "
            "`slice::range(range, ..self.len())`, checks both resulting byte "
            "endpoints with `is_char_boundary`, and splices `replace_with.bytes()` "
            "into that checked byte range. The helper snapshots those normalized "
            "byte endpoints once and the postcondition decodes the resulting UTF-8 "
            "bytes into the observable String view."
        ),
        "risks": [
            "The trusted contract relies on vstd's RangeBoundsSpec model for the single normalized range snapshot.",
            "The contract specifies the resulting string view and does not claim allocation, capacity, or pointer/provenance identity.",
        ],
    },
}


DIRECT_MUT_VIEW_ADAPTER_SOURCE_RECOVERY_CANDIDATES = {
    "core::array::from_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T>[ core::array::from_mut::<T> ](
    s: &mut T,
) -> (out: &mut [T; 1])
    ensures
        out@[0] == *old(s),
        final(out)@ == out@,
        *final(s) == final(out)@[0],
;""",
        "requires": [],
        "ensures": [
            "out@[0] == *old(s)",
            "final(out)@ == out@",
            "*final(s) == final(out)@[0]",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents array::from_mut as converting `&mut T` to "
            "`&mut [T; 1]` without copying, and its body performs exactly the "
            "`(s as *mut T).cast::<[T; 1]>()` reinterpretation. The contract "
            "models only the observable singleton array view and the final "
            "mutation correspondence to the input reference."
        ),
        "risks": [
            "The contract is trusted and intentionally avoids pointer identity or provenance claims.",
            "It is accepted only for this exact source-backed singleton mutable-array adapter.",
        ],
    },
    "core::slice::from_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T>[ core::slice::from_mut ](
    s: &mut T,
) -> (ret: &mut [T])
    ensures
        ret@ == seq![*old(s)],
        final(ret)@ == ret@,
        final(ret)@ == seq![*final(s)],
        *final(s) == *old(s),
;""",
        "requires": [],
        "ensures": [
            "ret@ == seq![*old(s)]",
            "final(ret)@ == ret@",
            "final(ret)@ == seq![*final(s)]",
            "*final(s) == *old(s)",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents slice::from_mut as producing a length-one "
            "slice without copying and implements it by delegating directly to "
            "`array::from_mut(s)`. The contract models the singleton slice "
            "contents before and after mutation through the returned view."
        ),
        "risks": [
            "The contract is trusted and models semantic slice contents, not reference identity.",
            "It is accepted only for this exact source-backed delegation to array::from_mut.",
        ],
    },
    "core::array::as_mut_slice": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, const N: usize>[ <[T; N]>::as_mut_slice ](
    ar: &mut [T; N],
) -> (out: &mut [T])
    ensures
        out@ == old(ar)@,
        final(out)@ == out@,
        final(out)@ == final(ar)@,
;""",
        "requires": [],
        "ensures": [
            "out@ == old(ar)@",
            "final(out)@ == out@",
            "final(out)@ == final(ar)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents [T; N]::as_mut_slice as returning a mutable "
            "slice over the entire array, equivalent to `&mut s[..]`, and the "
            "body returns `self`. The contract keeps exactly that whole-array "
            "view relation and final mutation correspondence."
        ),
        "risks": [
            "The contract is trusted and models semantic views, not pointer identity.",
            "It is accepted only for this exact whole-array mutable slice adapter.",
        ],
    },
    "core::slice::as_mut_array": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, const N: usize>[ <[T]>::as_mut_array::<N> ](
    slice: &mut [T],
) -> (ret: Option<&mut [T; N]>)
    ensures
        ret is Some == (old(slice)@.len() == N),
        ret matches Some(out) ==> {
            &&& out@ == old(slice)@
            &&& final(out)@ == out@
            &&& final(slice)@ == final(out)@
        },
        ret is None ==> final(slice)@ == old(slice)@,
;""",
        "requires": [],
        "ensures": [
            "ret is Some == (old(slice)@.len() == N)",
            (
                "ret matches Some(out) ==> { "
                "&&& out@ == old(slice)@ "
                "&&& final(out)@ == out@ "
                "&&& final(slice)@ == final(out)@ }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents slice::as_mut_array as returning Some exactly "
            "when the slice length equals N, then reinterprets the same mutable "
            "storage as `[T; N]`. The contract models only that observable whole "
            "slice/array view, returned-view preservation, and unchanged None "
            "branch without pointer or provenance claims."
        ),
        "risks": [
            "The contract is trusted and models semantic array/slice views, not reference identity.",
            "It is accepted only for this exact source-backed Option mutable-array adapter.",
        ],
    },
    "core::slice::first_chunk_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, const N: usize>[ <[T]>::first_chunk_mut::<N> ](
    slice: &mut [T],
) -> (ret: Option<&mut [T; N]>)
    ensures
        ret is Some == (N as int <= old(slice)@.len()),
        ret matches Some(out) ==> {
            &&& out@ == old(slice)@.subrange(0, N as int)
            &&& final(out)@ == out@
            &&& final(slice)@ == final(out)@ + old(slice)@.subrange(N as int, old(slice)@.len() as int)
        },
        ret is None ==> final(slice)@ == old(slice)@,
;""",
        "requires": [],
        "ensures": [
            "ret is Some == (N as int <= old(slice)@.len())",
            (
                "ret matches Some(out) ==> { "
                "&&& out@ == old(slice)@.subrange(0, N as int) "
                "&&& final(out)@ == out@ "
                "&&& final(slice)@ == final(out)@ + "
                "old(slice)@.subrange(N as int, old(slice)@.len() as int) }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents first_chunk_mut as returning None when the slice "
            "is shorter than N and otherwise returning a mutable array reference "
            "to the first N items. The source casts the slice's mutable pointer "
            "after the length check, so the contract models the prefix view, "
            "returned-view preservation, and the untouched suffix."
        ),
        "risks": [
            "The contract is trusted and models semantic array/slice views, not reference identity.",
            "It is accepted only for this exact source-backed first-chunk mutable-array adapter.",
        ],
    },
    "core::slice::last_chunk_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, const N: usize>[ <[T]>::last_chunk_mut::<N> ](
    slice: &mut [T],
) -> (ret: Option<&mut [T; N]>)
    ensures
        ret is Some == (N as int <= old(slice)@.len()),
        ret matches Some(out) ==> {
            &&& out@ == old(slice)@.subrange(old(slice)@.len() - N as int, old(slice)@.len() as int)
            &&& final(out)@ == out@
            &&& final(slice)@ == old(slice)@.subrange(0, old(slice)@.len() - N as int) + final(out)@
        },
        ret is None ==> final(slice)@ == old(slice)@,
;""",
        "requires": [],
        "ensures": [
            "ret is Some == (N as int <= old(slice)@.len())",
            (
                "ret matches Some(out) ==> { "
                "&&& out@ == old(slice)@.subrange("
                "old(slice)@.len() - N as int, old(slice)@.len() as int) "
                "&&& final(out)@ == out@ "
                "&&& final(slice)@ == old(slice)@.subrange("
                "0, old(slice)@.len() - N as int) + final(out)@ }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 documents last_chunk_mut as returning None when the slice "
            "is shorter than N and otherwise returning a mutable array reference "
            "to the last N items. The body computes the suffix index with "
            "checked_sub, splits at that index, and casts the last slice to "
            "`[T; N]`, so the contract models the unchanged prefix and returned "
            "suffix view without provenance claims."
        ),
        "risks": [
            "The contract is trusted and models semantic array/slice views, not reference identity.",
            "It is accepted only for this exact source-backed last-chunk mutable-array adapter.",
        ],
    },
}


SPLIT_CHUNK_MUT_TUPLE_SOURCE_RECOVERY_CANDIDATES = {
    "core::slice::split_first_chunk_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, const N: usize>[ <[T]>::split_first_chunk_mut::<N> ](
    slice: &mut [T],
) -> (ret: Option<(&mut [T; N], &mut [T])>)
    ensures
        ret is Some == (N as int <= old(slice)@.len()),
        ret matches Some((first, tail)) ==> {
            &&& first@ == old(slice)@.subrange(0, N as int)
            &&& tail@ == old(slice)@.subrange(N as int, old(slice)@.len() as int)
            &&& final(first)@ == first@
            &&& final(tail)@ == tail@
            &&& final(slice)@ == final(first)@ + final(tail)@
        },
        ret is None ==> final(slice)@ == old(slice)@,
;""",
        "requires": [],
        "ensures": [
            "ret is Some == (N as int <= old(slice)@.len())",
            (
                "ret matches Some((first, tail)) ==> { "
                "&&& first@ == old(slice)@.subrange(0, N as int) "
                "&&& tail@ == old(slice)@.subrange(N as int, old(slice)@.len() as int) "
                "&&& final(first)@ == first@ "
                "&&& final(tail)@ == tail@ "
                "&&& final(slice)@ == final(first)@ + final(tail)@ }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 returns Some exactly when `split_at_mut_checked(N)` "
            "succeeds, casts the checked first slice to `[T; N]`, and returns "
            "the remaining tail. The contract models those returned mutable "
            "views by their old slice/array contents, preserves each returned "
            "view at function return, and relates the final input slice to the "
            "final first-chunk and tail views without claiming pointer identity."
        ),
        "risks": [
            "The contract is trusted and models semantic array/slice views, not reference identity.",
            "It is accepted only for this exact source-backed mutable split-first chunk tuple shape.",
        ],
    },
    "core::slice::split_last_chunk_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, const N: usize>[ <[T]>::split_last_chunk_mut::<N> ](
    slice: &mut [T],
) -> (ret: Option<(&mut [T], &mut [T; N])>)
    ensures
        ret is Some == (N as int <= old(slice)@.len()),
        ret matches Some((init, last)) ==> {
            &&& init@ == old(slice)@.subrange(0, old(slice)@.len() - N as int)
            &&& last@ == old(slice)@.subrange(old(slice)@.len() - N as int, old(slice)@.len() as int)
            &&& final(init)@ == init@
            &&& final(last)@ == last@
            &&& final(slice)@ == final(init)@ + final(last)@
        },
        ret is None ==> final(slice)@ == old(slice)@,
;""",
        "requires": [],
        "ensures": [
            "ret is Some == (N as int <= old(slice)@.len())",
            (
                "ret matches Some((init, last)) ==> { "
                "&&& init@ == old(slice)@.subrange(0, old(slice)@.len() - N as int) "
                "&&& last@ == old(slice)@.subrange(old(slice)@.len() - N as int, old(slice)@.len() as int) "
                "&&& final(init)@ == init@ "
                "&&& final(last)@ == last@ "
                "&&& final(slice)@ == final(init)@ + final(last)@ }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 returns None when `self.len().checked_sub(N)` fails; "
            "otherwise it splits at the checked index, returns the init slice "
            "and casts the last slice to `[T; N]`. The contract models that "
            "branch shape with old init/last views, preserves both returned "
            "views at function return, and reconstructs the final input slice "
            "from their final semantic views."
        ),
        "risks": [
            "The contract is trusted and models semantic slice/array views, not reference identity.",
            "It is accepted only for this exact source-backed mutable split-last chunk tuple shape.",
        ],
    },
}


MUTATING_SLICE_SOURCE_RECOVERY_CANDIDATES = {
    "core::slice::reverse": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T>[ <[T]>::reverse ](slice: &mut [T])
    ensures
        final(slice)@ == old(slice)@.reverse(),
;""",
        "requires": [],
        "ensures": ["final(slice)@ == old(slice)@.reverse()"],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 reverses the slice in place by splitting the front and "
            "back halves and swapping mirrored elements. The contract records "
            "only the observable final sequence view, avoiding pointer or "
            "provenance claims while preserving the operation's full semantics."
        ),
        "risks": [
            "The contract is trusted and models the final semantic slice view, not element addresses or provenance.",
            "It is accepted only for the source-backed in-place reversal body.",
        ],
    },
}


SINGLE_ELEMENT_MUT_SPLIT_SOURCE_RECOVERY_CANDIDATES = {
    "core::slice::split_first_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T>[ <[T]>::split_first_mut ](
    slice: &mut [T],
) -> (ret: Option<(&mut T, &mut [T])>)
    ensures
        ret is Some == (old(slice)@.len() != 0),
        ret matches Some((first, tail)) ==> {
            &&& *first == old(slice)@[0]
            &&& tail@ == old(slice)@.subrange(1, old(slice)@.len() as int)
            &&& *final(first) == *first
            &&& final(tail)@ == tail@
            &&& final(slice)@ == seq![*final(first)] + final(tail)@
        },
        ret is None ==> final(slice)@ == old(slice)@,
;""",
        "requires": [],
        "ensures": [
            "ret is Some == (old(slice)@.len() != 0)",
            (
                "ret matches Some((first, tail)) ==> { "
                "&&& *first == old(slice)@[0] "
                "&&& tail@ == old(slice)@.subrange(1, old(slice)@.len() as int) "
                "&&& *final(first) == *first "
                "&&& final(tail)@ == tail@ "
                "&&& final(slice)@ == seq![*final(first)] + final(tail)@ }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 pattern-matches `[first, tail @ ..]` and returns "
            "`Some((first, tail))` exactly for nonempty slices. The contract "
            "models the returned element by its dereferenced value, the returned "
            "tail by its semantic view, preserves both returned mutable views at "
            "function return, and reconstructs the final input slice from those "
            "views without pointer/provenance claims."
        ),
        "risks": [
            "The contract is trusted and models semantic values/views, not reference identity.",
            "It is accepted only for this exact source-backed single-element mutable split shape.",
        ],
    },
    "core::slice::split_last_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T>[ <[T]>::split_last_mut ](
    slice: &mut [T],
) -> (ret: Option<(&mut T, &mut [T])>)
    ensures
        ret is Some == (old(slice)@.len() != 0),
        ret matches Some((last, init)) ==> {
            &&& *last == old(slice)@[(old(slice)@.len() - 1) as int]
            &&& init@ == old(slice)@.subrange(0, old(slice)@.len() - 1)
            &&& *final(last) == *last
            &&& final(init)@ == init@
            &&& final(slice)@ == final(init)@ + seq![*final(last)]
        },
        ret is None ==> final(slice)@ == old(slice)@,
;""",
        "requires": [],
        "ensures": [
            "ret is Some == (old(slice)@.len() != 0)",
            (
                "ret matches Some((last, init)) ==> { "
                "&&& *last == old(slice)@[(old(slice)@.len() - 1) as int] "
                "&&& init@ == old(slice)@.subrange(0, old(slice)@.len() - 1) "
                "&&& *final(last) == *last "
                "&&& final(init)@ == init@ "
                "&&& final(slice)@ == final(init)@ + seq![*final(last)] }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 pattern-matches `[init @ .., last]` and returns "
            "`Some((last, init))` exactly for nonempty slices. The contract "
            "models the returned element by its dereferenced value, the returned "
            "init slice by its semantic view, preserves both returned mutable "
            "views, and reconstructs the final input slice from those views."
        ),
        "risks": [
            "The contract is trusted and models semantic values/views, not reference identity.",
            "It is accepted only for this exact source-backed single-element mutable split shape.",
        ],
    },
    "core::slice::split_off_first_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<'a, T>[ <[T]>::split_off_first_mut ](
    slice: &mut &'a mut [T],
) -> (ret: Option<&'a mut T>)
    ensures
        ret is Some == (old(slice)@.len() != 0),
        ret matches Some(first) ==> {
            &&& *first == old(slice)@[0]
            &&& *final(first) == *first
            &&& final(slice)@ == old(slice)@.subrange(1, old(slice)@.len() as int)
            &&& old(slice)@ == seq![*final(first)] + final(slice)@
        },
        ret is None ==> final(slice)@ == old(slice)@,
;""",
        "requires": [],
        "ensures": [
            "ret is Some == (old(slice)@.len() != 0)",
            (
                "ret matches Some(first) ==> { "
                "&&& *first == old(slice)@[0] "
                "&&& *final(first) == *first "
                "&&& final(slice)@ == old(slice)@.subrange(1, old(slice)@.len() as int) "
                "&&& old(slice)@ == seq![*final(first)] + final(slice)@ }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 replaces `self` with an empty mutable slice, delegates to "
            "`split_first_mut`, assigns `*self = rem`, and returns `Some(first)` "
            "only for nonempty slices. The contract models the returned element by "
            "dereferenced value and reconstructs the final slice reference as the "
            "remaining tail, without pointer/provenance claims."
        ),
        "risks": [
            "The contract is trusted and models semantic values/views, not reference identity.",
            "It is accepted only for this exact source-backed split-off-first mutable shape.",
        ],
    },
    "core::slice::split_off_last_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<'a, T>[ <[T]>::split_off_last_mut ](
    slice: &mut &'a mut [T],
) -> (ret: Option<&'a mut T>)
    ensures
        ret is Some == (old(slice)@.len() != 0),
        ret matches Some(last) ==> {
            &&& *last == old(slice)@[(old(slice)@.len() - 1) as int]
            &&& *final(last) == *last
            &&& final(slice)@ == old(slice)@.subrange(0, old(slice)@.len() - 1)
            &&& old(slice)@ == final(slice)@ + seq![*final(last)]
        },
        ret is None ==> final(slice)@ == old(slice)@,
;""",
        "requires": [],
        "ensures": [
            "ret is Some == (old(slice)@.len() != 0)",
            (
                "ret matches Some(last) ==> { "
                "&&& *last == old(slice)@[(old(slice)@.len() - 1) as int] "
                "&&& *final(last) == *last "
                "&&& final(slice)@ == old(slice)@.subrange(0, old(slice)@.len() - 1) "
                "&&& old(slice)@ == final(slice)@ + seq![*final(last)] }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        "feature_gates": [],
        "imports": [],
        "useful": True,
        "rationale": (
            "Rust 1.96 replaces `self` with an empty mutable slice, delegates to "
            "`split_last_mut`, assigns `*self = rem`, and returns `Some(last)` "
            "only for nonempty slices. The contract models the returned element by "
            "dereferenced value and reconstructs the final slice reference as the "
            "remaining init slice, without pointer/provenance claims."
        ),
        "risks": [
            "The contract is trusted and models semantic values/views, not reference identity.",
            "It is accepted only for this exact source-backed split-off-last mutable shape.",
        ],
    },
}


LINKEDLIST_BACK_MUT_SOURCE_RECOVERY_CANDIDATES = {
    "alloc::collections::LinkedList::back_mut": {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "contract_code": """pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::back_mut ](
    list: &mut LinkedList<T, A>,
) -> (result: Option<&mut T>)
    ensures
        result is Some == (old(list)@.len() != 0),
        result is None == (old(list)@.len() == 0),
        result matches Some(value) ==> {
            &&& *value == old(list)@.last()
            &&& *final(value) == *value
            &&& final(list)@ == old(list)@
        },
        result is None ==> final(list)@ == old(list)@,
;""",
        "requires": [],
        "ensures": [
            "result is Some == (old(list)@.len() != 0)",
            "result is None == (old(list)@.len() == 0)",
            (
                "result matches Some(value) ==> { "
                "&&& *value == old(list)@.last() "
                "&&& *final(value) == *value "
                "&&& final(list)@ == old(list)@ }"
            ),
            "result is None ==> final(list)@ == old(list)@",
        ],
        "feature_gates": ["allocator_api"],
        "imports": [
            "alloc::collections::LinkedList",
            "core::alloc::Allocator",
            "vstd::std_specs::collections_extra::*",
        ],
        "useful": True,
        "rationale": (
            "Rust 1.96 implements LinkedList::back_mut as "
            "`self.tail.as_mut().map(|node| &mut node.as_mut().element)`, so it "
            "returns Some exactly for nonempty lists and projects the old tail "
            "element. The contract models only the observable sequence value of "
            "that returned mutable reference and preserves both the returned "
            "value and the list view at function return, without pointer or "
            "private-node identity claims."
        ),
        "risks": [
            "The contract is trusted and models semantic values/views, not reference identity or private node provenance.",
            "It is accepted only for the exact Rust 1.96 tail-projection source body.",
        ],
    }
}


SOURCE_RECOVERY_CANDIDATES = {
    **UNICODE_TRIM_RECOVERY_CANDIDATES,
    **STR_FROM_UTF8_SOURCE_RECOVERY_CANDIDATES,
    **SLICE_BINARY_SEARCH_SOURCE_RECOVERY_CANDIDATES,
    **SAFE_SLICE_CHUNK_SOURCE_RECOVERY_CANDIDATES,
    **MUT_SLICE_CHUNK_SOURCE_RECOVERY_CANDIDATES,
    **MUTATING_SLICE_SOURCE_RECOVERY_CANDIDATES,
    **BTREESET_SOURCE_RECOVERY_CANDIDATES,
    **RESULT_SOURCE_RECOVERY_CANDIDATES,
    **HASHMAP_SOURCE_RECOVERY_CANDIDATES,
    **BTREEMAP_SOURCE_RECOVERY_CANDIDATES,
    **SLICE_SPLIT_AT_MUT_UNCHECKED_SOURCE_RECOVERY_CANDIDATES,
    **SLICE_SPLIT_AT_MUT_CHECKED_SOURCE_RECOVERY_CANDIDATES,
    **STR_SPLIT_AT_CHECKED_SOURCE_RECOVERY_CANDIDATES,
    **STR_SPLIT_AT_MUT_CHECKED_SOURCE_RECOVERY_CANDIDATES,
    **STRING_REPLACE_RANGE_SOURCE_RECOVERY_CANDIDATES,
    **DIRECT_MUT_VIEW_ADAPTER_SOURCE_RECOVERY_CANDIDATES,
    **SPLIT_CHUNK_MUT_TUPLE_SOURCE_RECOVERY_CANDIDATES,
    **SINGLE_ELEMENT_MUT_SPLIT_SOURCE_RECOVERY_CANDIDATES,
    **LINKEDLIST_BACK_MUT_SOURCE_RECOVERY_CANDIDATES,
}


def extracted_checker_clauses(
    checker: dict[str, Any] | None,
) -> tuple[list[str], list[str]] | None:
    if not checker:
        return None
    determinism = checker.get("determinism")
    if not isinstance(determinism, dict):
        determinism = checker
    requires = determinism.get("requires")
    ensures = determinism.get("ensures")
    if not isinstance(requires, list) or not isinstance(ensures, list) or not ensures:
        return None
    return [str(item) for item in requires], [str(item) for item in ensures]


def canonicalize_candidate_clauses(
    candidate: dict[str, Any],
    checker: dict[str, Any] | None,
) -> dict[str, Any]:
    clauses = extracted_checker_clauses(checker)
    if clauses is None:
        return dict(candidate)
    requires, ensures = clauses
    canonical = dict(candidate)
    canonical["requires"] = requires
    canonical["ensures"] = ensures
    return canonical


def recompute_rechecked_final(
    final: dict[str, Any],
    entry: dict[str, Any],
) -> dict[str, Any]:
    checker = final.get("checker") or {}
    typecheck = checker.get("typecheck")
    determinism = checker.get("determinism")
    if not isinstance(typecheck, dict) or not isinstance(determinism, dict):
        return final
    candidate = canonicalize_candidate_clauses(candidate_from_record(final), determinism)
    issues = runner.anti_vacuity_issues(entry, candidate, typecheck, determinism)
    raw_reward = int(
        determinism.get("status") == "ok" and determinism.get("r0_z3") == "unsat"
    )
    guarded_reward = int(
        raw_reward == 1 and typecheck.get("returncode") == 0 and not issues
    )
    updated = dict(final)
    updated.update(
        {
            "candidate": candidate,
            "anti_vacuity_issues": issues,
            "raw_det_reward": raw_reward,
            "guarded_reward": guarded_reward,
        }
    )
    return updated


def recovery_candidate_records(target: str, final: dict[str, Any]) -> list[dict[str, Any]]:
    if int(final.get("guarded_reward", 0)) == 1:
        return []
    candidate = SOURCE_RECOVERY_CANDIDATES.get(target)
    if candidate is None:
        return []
    return [
        {
            "round": "source_recovery",
            "llm_ms": 0,
            "candidate": dict(candidate),
            "checker": {"status": "not_run"},
            "anti_vacuity_issues": [],
            "raw_det_reward": 0,
            "guarded_reward": 0,
            "soundness_status": "unverified_trusted_external_contract",
            "apply_upstream": False,
        }
    ]


def records_to_recheck(
    result: dict[str, Any],
    final: dict[str, Any],
) -> list[dict[str, Any]]:
    records = recovery_candidate_records(result["target"], final)
    records.extend(candidate_records(result, final))
    selected: list[dict[str, Any]] = []
    seen_contracts: set[str] = set()
    for record in records:
        candidate = candidate_from_record(record)
        if not is_add_spec_candidate(candidate):
            continue
        contract_code = str(candidate.get("contract_code") or "")
        if contract_code in seen_contracts:
            continue
        seen_contracts.add(contract_code)
        selected.append(record)
    return selected


def has_stale_cached_recheck(final: dict[str, Any], target_dir: Path) -> bool:
    determinism = ((final.get("checker") or {}).get("determinism") or {})
    stderr_tail = str(determinism.get("stderr_tail") or "")
    if (
        determinism.get("status") == "verus_error"
        and "size for values of type `str`" in stderr_tail
    ):
        return True
    if (
        determinism.get("status") == "verus_error"
        and "size for values of type `[T]`" in stderr_tail
    ):
        return True
    if (
        determinism.get("status") == "verus_error"
        and re.search(r"size for values of type `\[[^`]+\]`", stderr_tail)
    ):
        return True
    if (
        determinism.get("status") == "verus_error"
        and "to dereference a mutable reference parameter in a postcondition" in stderr_tail
    ):
        return True
    if determinism.get("status") == "ok" and determinism.get("r0_z3") == "unknown":
        try:
            det_harness = (target_dir / "recheck_final" / "det_harness.rs").read_text()
        except OSError:
            return False
        return ": &str" in det_harness and (
            ")@ ==" in det_harness or "spec_bytes() == " in det_harness
        )
    return False


def has_current_cached_recheck(
    final: dict[str, Any],
    target_dir: Path,
    registry: ViewRegistry,
) -> bool:
    if not is_rechecked(final):
        return False
    candidate = candidate_from_record(final)
    if not is_add_spec_candidate(candidate):
        return False
    target_dir = target_dir.expanduser().absolute()
    target_dir_resolved = target_dir.resolve(strict=False)
    if target_dir != target_dir_resolved:
        return False
    recheck_dir = target_dir / "recheck_final"
    harness_path = recheck_dir / "contract_harness.rs"
    required_artifacts = [
        harness_path,
        recheck_dir / "typecheck_stdout.txt",
        recheck_dir / "typecheck_stderr.txt",
    ]
    determinism = ((final.get("checker") or {}).get("determinism") or {})
    if isinstance(determinism, dict) and determinism:
        required_artifacts.extend(
            [
                recheck_dir / "synthetic_spec.rs",
                recheck_dir / "det_harness.rs",
                recheck_dir / "det_spec.json",
                recheck_dir / "det_stdout.txt",
                recheck_dir / "det_stderr.txt",
            ]
        )
    for artifact in required_artifacts:
        artifact_absolute = artifact.absolute()
        artifact_resolved = artifact_absolute.resolve(strict=False)
        try:
            artifact_resolved.relative_to(target_dir_resolved)
        except ValueError:
            return False
        if (
            artifact_absolute != artifact_resolved
            or artifact.is_symlink()
            or not artifact.is_file()
        ):
            return False
    try:
        cached_harness = harness_path.read_text()
    except OSError:
        return False
    if cached_harness != runner.build_contract_harness(candidate):
        return False
    if not isinstance(determinism, dict) or not determinism:
        return True

    try:
        prepared = runner.build_determinism_artifacts(candidate, registry)
    except Exception:
        return False
    if prepared.get("status") != "ready":
        return False
    det_spec = prepared["det_spec"]
    expected_artifacts = {
        "synthetic_spec.rs": prepared["synthetic_source"],
        "det_harness.rs": prepared["harness"],
        "det_spec.json": det_spec.to_json(),
    }
    for name, expected in expected_artifacts.items():
        try:
            actual = (recheck_dir / name).read_text()
        except OSError:
            return False
        if actual != expected:
            return False
    spec = prepared["spec"]
    return (
        list(determinism.get("requires") or []) == list(spec.requires)
        and list(determinism.get("ensures") or []) == list(spec.ensures)
    )


def target_artifact_dirs(
    batch_summary: Path,
    metadata: dict[str, Any],
) -> dict[str, Path]:
    nodes = runner.metadata_nodes(metadata)
    candidates: list[Path] = []
    for node in nodes:
        target_artifact_roots = node.get("target_artifact_roots") or []
        if isinstance(target_artifact_roots, (str, Path)):
            target_artifact_roots = [target_artifact_roots]
        candidates.extend(
            Path(str(value)) for value in target_artifact_roots if value
        )

    if not candidates:
        for node in nodes:
            batch_files = node.get("batch_files") or []
            if isinstance(batch_files, (str, Path)):
                batch_files = [batch_files]
            candidates.extend(
                Path(str(value)).parent for value in batch_files if value
            )
    if not candidates:
        candidates.append(batch_summary.parent)

    roots: list[Path] = []
    seen_roots: set[Path] = set()
    for candidate in candidates:
        root_absolute = candidate.expanduser().absolute()
        if root_absolute in seen_roots:
            continue
        seen_roots.add(root_absolute)
        root = root_absolute.resolve(strict=False)
        if (
            root_absolute.is_symlink()
            or root_absolute != root
            or not root_absolute.is_dir()
        ):
            raise ValueError(
                f"target artifact root does not resolve to itself: {root_absolute}"
            )
        targets_dir = root / "targets"
        if not targets_dir.is_dir():
            raise FileNotFoundError(f"target artifact directory is missing: {targets_dir}")
        targets_dir_absolute = targets_dir.absolute()
        targets_dir_resolved = targets_dir_absolute.resolve(strict=False)
        if (
            targets_dir.is_symlink()
            or targets_dir_absolute != targets_dir_resolved
            or targets_dir_resolved.parent != root
        ):
            raise ValueError(
                f"target artifact directory escapes its declared root: {targets_dir}"
            )
        roots.append(root)

    directories: dict[str, Path] = {}
    for root in roots:
        targets_dir = root / "targets"
        for entry in sorted(targets_dir.iterdir(), key=lambda path: path.name):
            if not entry.is_dir():
                continue
            entry_absolute = entry.absolute()
            entry_resolved = entry_absolute.resolve(strict=False)
            if (
                entry.is_symlink()
                or entry_absolute != entry_resolved
                or entry_resolved.parent != targets_dir
            ):
                raise ValueError(
                    f"target artifact directory escapes targets root: {entry}"
                )
            if entry.name in directories:
                raise ValueError(
                    f"duplicate target artifact directory {entry.name!r}: "
                    f"{directories[entry.name]} and {entry}"
                )
            directories[entry.name] = entry
    return directories


def preflight_recheck_results(
    results: Any,
    entries: dict[str, dict[str, Any]],
    artifact_dirs: dict[str, Path],
) -> dict[str, Path]:
    if not isinstance(results, list) or any(
        not isinstance(result, dict) for result in results
    ):
        raise ValueError("batch results must be a list of objects")

    targets = [str(result.get("target") or "") for result in results]
    if any(not target for target in targets):
        raise ValueError("batch results contain an empty target")
    target_counts: dict[str, int] = {}
    for target in targets:
        target_counts[target] = target_counts.get(target, 0) + 1
    duplicate_targets = sorted(
        target for target, count in target_counts.items() if count > 1
    )
    if duplicate_targets:
        raise ValueError(
            "duplicate result targets: " + ", ".join(duplicate_targets)
        )

    unknown_targets = sorted(set(targets) - set(entries))
    if unknown_targets:
        raise ValueError(
            "result targets missing from manifest: " + ", ".join(unknown_targets)
        )

    safe_names: dict[str, str] = {}
    target_dirs: dict[str, Path] = {}
    for target in targets:
        safe = runner.safe_name(target)
        previous_target = safe_names.get(safe)
        if previous_target is not None:
            raise ValueError(
                f"target safe-name collision {safe!r}: "
                f"{previous_target!r} and {target!r}"
            )
        safe_names[safe] = target
        target_dir = artifact_dirs.get(safe)
        if target_dir is None:
            raise FileNotFoundError(
                f"target artifact directory is missing for {target!r}"
            )
        target_json_path = target_dir / "target.json"
        target_json_absolute = target_json_path.absolute()
        target_json_resolved = target_json_absolute.resolve(strict=False)
        if (
            target_json_path.is_symlink()
            or target_json_absolute != target_json_resolved
            or target_json_resolved.parent != target_dir
            or not target_json_path.is_file()
        ):
            raise ValueError(f"invalid target artifact: {target_json_path}")
        target_payload = json.loads(target_json_path.read_text())
        if not isinstance(target_payload, dict):
            raise ValueError(f"target artifact is not an object: {target_json_path}")
        if str(target_payload.get("target") or "") != target:
            raise ValueError(
                f"target artifact mismatch for {target!r}: {target_json_path}"
            )
        target_dirs[target] = target_dir
    return target_dirs


def should_recheck_history(final: dict[str, Any]) -> bool:
    if not is_rechecked(final):
        return False
    if int(final.get("guarded_reward", 0)) == 1:
        return False
    checker = final.get("checker") or {}
    typecheck = checker.get("typecheck") or {}
    determinism = checker.get("determinism") or {}
    return (
        typecheck.get("returncode") != 0
        or determinism.get("status") in {"verus_error", "runner_crash"}
    )


def candidate_records(result: dict[str, Any], final: dict[str, Any]) -> list[dict[str, Any]]:
    if not should_recheck_history(final):
        return [final]
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    final_candidate = candidate_from_record(final)
    if is_add_spec_candidate(final_candidate):
        records.append(final)
        seen.add(str(final_candidate.get("contract_code") or ""))
    for record in reversed(result.get("history") or []):
        candidate = candidate_from_record(record)
        if not is_add_spec_candidate(candidate):
            continue
        key = str(candidate.get("contract_code") or "")
        if key in seen:
            continue
        seen.add(key)
        records.append(record)
    return records or [final]


def recheck_record(
    *,
    record: dict[str, Any],
    result: dict[str, Any],
    entry: dict[str, Any],
    recheck_dir: Path,
    args: argparse.Namespace,
    registry: ViewRegistry,
) -> dict[str, Any]:
    candidate = candidate_from_record(record)
    recheck_dir.mkdir(parents=True, exist_ok=True)
    contract_path = recheck_dir / "contract_harness.rs"
    contract_path.write_text(runner.build_contract_harness(candidate))
    typecheck = runner.run_verus(
        verus_bin=args.verus_bin,
        z3_path=args.z3_path,
        file_path=contract_path,
        timeout=args.timeout,
        rlimit=args.rlimit,
    )
    (recheck_dir / "typecheck_stdout.txt").write_text(typecheck["stdout"])
    (recheck_dir / "typecheck_stderr.txt").write_text(typecheck["stderr"])
    checker = None
    if (
        typecheck["returncode"] == 0
        and candidate.get("contract_form") == "assume_specification"
    ):
        checker = runner.run_determinism(
            candidate=candidate,
            round_dir=recheck_dir,
            view_registry=registry,
            verus_bin=args.verus_bin,
            z3_path=args.z3_path,
            timeout=args.timeout,
            rlimit=args.rlimit,
        )
    candidate = canonicalize_candidate_clauses(candidate, checker)
    issues = runner.anti_vacuity_issues(
        entry,
        candidate,
        typecheck,
        checker,
    )
    raw_reward = int(
        checker is not None
        and checker.get("status") == "ok"
        and checker.get("r0_z3") == "unsat"
    )
    guarded_reward = int(
        raw_reward == 1
        and typecheck["returncode"] == 0
        and not issues
    )
    final = dict(record)
    final.update(
        {
            "candidate": candidate,
            "checker": runner.checker_summary(typecheck, checker),
            "anti_vacuity_issues": issues,
            "raw_det_reward": raw_reward,
            "guarded_reward": guarded_reward,
            "soundness_status": "unverified_trusted_external_contract",
            "apply_upstream": False,
            "rechecked": True,
            "recheck_source_target": result["target"],
        }
    )
    return final


def write_recheck_summary(
    out_dir: Path,
    *,
    batch_summary: Path,
    manifest: Path,
    results: list[dict[str, Any]],
    add_spec_candidates: int,
    cached_rechecks: int,
    rerun_rechecks: int,
) -> None:
    finals = [result.get("final") or {} for result in results]
    add_spec_finals = [
        final
        for final in finals
        if (final.get("candidate") or {}).get("decision") == "add_spec"
    ]
    typecheck_passed = sum(
        ((final.get("checker") or {}).get("typecheck") or {}).get("returncode") == 0
        for final in add_spec_finals
    )
    determinism = [
        ((final.get("checker") or {}).get("determinism") or {})
        for final in add_spec_finals
    ]
    payload = {
        "batch_summary": str(batch_summary.resolve()),
        "manifest": str(manifest.resolve()),
        "targets": len(results),
        "add_spec_candidates": add_spec_candidates,
        "add_spec_rechecked": sum(is_rechecked(final) for final in add_spec_finals),
        "cached_rechecks": cached_rechecks,
        "rerun_rechecks": rerun_rechecks,
        "typecheck_passed": typecheck_passed,
        "det_unsat": sum(item.get("r0_z3") == "unsat" for item in determinism),
        "det_unknown": sum(item.get("r0_z3") == "unknown" for item in determinism),
        "det_sat": sum(item.get("r0_z3") == "sat" for item in determinism),
        "raw_reward": sum(int(final.get("raw_det_reward", 0)) for final in finals),
        "guarded_reward": sum(int(final.get("guarded_reward", 0)) for final in finals),
    }
    (out_dir / "recheck_summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )


def main() -> int:
    args = parse_args()
    payload = json.loads(args.batch_summary.read_text())
    manifest_records = runner.manifest_entries_from_metadata(
        {"manifest": str(args.manifest)}
    )
    if manifest_records is None:
        raise ValueError(f"manifest has no target entries: {args.manifest}")
    entries = {str(entry["target"]): entry for entry in manifest_records}
    metadata = payload.get("metadata") or {}
    metadata_manifest_records = runner.manifest_entries_from_metadata(metadata)
    if metadata_manifest_records is None:
        metadata["manifest"] = str(args.manifest.expanduser().resolve())
        payload["metadata"] = metadata
    else:
        metadata_entries = {
            str(entry["target"]): entry for entry in metadata_manifest_records
        }
        if metadata_entries != entries:
            raise ValueError(
                "the explicit recheck manifest does not match batch metadata manifests"
            )
    logging.getLogger("spec_determinism").setLevel(logging.ERROR)
    artifact_dirs = target_artifact_dirs(args.batch_summary, metadata)
    target_dirs = preflight_recheck_results(
        payload.get("results"),
        entries,
        artifact_dirs,
    )
    registry = ViewRegistry.from_project(args.vstd_root)
    add_spec_candidates = 0
    cached_rechecks = 0
    rerun_rechecks = 0
    for result in payload["results"]:
        entry = entries[result["target"]]
        target_dir = target_dirs[result["target"]]
        normalized_contract_code = runner.normalize_result_contract_codes(result)
        forced_skip_final = runner.source_backed_forced_skip_final(entry)
        if forced_skip_final is not None:
            final = forced_skip_final
            prior_history = result.get("history") or []
            result["history"] = [
                record
                for record in prior_history
                if not is_forced_source_skip_record(record)
            ]
            result["history"].append(final)
            result["final"] = final
            target_dir.mkdir(parents=True, exist_ok=True)
            (target_dir / "summary.json").write_text(
                json.dumps(result, indent=2) + "\n"
            )
            continue
        final = result.get("final") or {}
        candidate = final.get("candidate") or {}
        if not candidate:
            for record in reversed(result.get("history") or []):
                prior = record.get("candidate") or {}
                if prior.get("decision") == "add_spec" and prior.get(
                    "contract_code"
                ):
                    final = dict(record)
                    candidate = prior
                    break
        planned_records = recovery_candidate_records(result["target"], final)
        if planned_records:
            candidate = candidate_from_record(planned_records[0])
        elif not is_add_spec_candidate(candidate):
            if normalized_contract_code:
                target_dir.mkdir(parents=True, exist_ok=True)
                (target_dir / "summary.json").write_text(
                    json.dumps(result, indent=2) + "\n"
                )
            continue
        add_spec_candidates += 1
        fresh_recheck = False
        current_cached_recheck = has_current_cached_recheck(
            final,
            target_dir,
            registry,
        )
        stale_cached_recheck = (
            current_cached_recheck
            and has_stale_cached_recheck(final, target_dir)
        )
        if (
            not planned_records
            and is_rechecked(final)
            and current_cached_recheck
            and not stale_cached_recheck
        ):
            cached_rechecks += 1
            final = recompute_rechecked_final(final, entry)
        else:
            original_final = final
            fresh_finals: list[dict[str, Any]] = []
            fresh_records = planned_records or records_to_recheck(result, final)
            for index, record in enumerate(fresh_records):
                source_round = record.get("round", "final")
                recheck_dir = (
                    target_dir / "recheck_final"
                    if index == 0 and record is final
                    else target_dir / f"recheck_candidate_round_{source_round}"
                )
                fresh = recheck_record(
                    record=record,
                    result=result,
                    entry=entry,
                    recheck_dir=recheck_dir,
                    args=args,
                    registry=registry,
                )
                fresh_finals.append(fresh)
                rerun_rechecks += 1
                if int(fresh.get("guarded_reward", 0)) == 1:
                    break
            final = next(
                (
                    fresh
                    for fresh in fresh_finals
                    if int(fresh.get("guarded_reward", 0)) == 1
                ),
                fresh_finals[0] if fresh_finals else original_final,
            )
            fresh_recheck = True
        if result.get("history") and fresh_recheck:
            if candidate_from_record(final) != candidate_from_record(result["history"][-1]):
                result["history"].append(final)
            else:
                result["history"][-1] = final
        result["final"] = final
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "summary.json").write_text(
            json.dumps(result, indent=2) + "\n"
        )

    runner.write_batch_summary(
        args.batch_summary.parent,
        payload["results"],
        payload["metadata"],
    )
    write_recheck_summary(
        args.batch_summary.parent,
        batch_summary=args.batch_summary,
        manifest=args.manifest,
        results=payload["results"],
        add_spec_candidates=add_spec_candidates,
        cached_rechecks=cached_rechecks,
        rerun_rechecks=rerun_rechecks,
    )
    print(f"rechecked {add_spec_candidates} add-spec candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
