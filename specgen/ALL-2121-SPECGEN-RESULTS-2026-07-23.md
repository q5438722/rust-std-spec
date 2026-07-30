# Full Rust std spec-generation results for all 2,121 APIs

## 1. Scope

This report extends the first 133-target suitable run to every stable Rust API
used by Nanvix that was not covered by the current Verus vstd inventory.

Model and checker:

- model: `gpt-5.6-sol`;
- Verus/vstd: `1beb0fad337b8f8a224cf8684162cb02d0c2fc01`;
- Verus Rust toolchain: `1.96.0`;
- determinism result: `R0 = unsat` means the candidate uniquely determines the
  modeled outputs;
- external contracts remain trusted and are not proved sound.

## 2. Full result

| Metric | Count |
|---|---:|
| Total APIs | 2,121 |
| Initial `add_spec` decisions | 437 |
| Initial `skip` decisions | 1,684 |
| Final `add_spec` decisions | 214 |
| Final `skip` decisions | 1,907 |
| Typechecked final contracts | 212 |
| `R0 = unsat` | 162 |
| `R0 = unknown` | 40 |
| `R0 = sat` | 0 |
| Raw determinism reward | 162 |
| Guarded determinism reward | 104 |
| Semantic-gated reward | 94 |
| LLM errors after retries/recovery | 0 |

The final 214 add-spec decisions are generated candidates, not upstream-ready
specifications.

## 3. Contribution of the remaining 2,018 APIs

The original suitable run had already generated 103 contracts. The remaining
run covered the other 2,018 APIs, including the 30 suitable-run skips.

| Metric | Remaining run |
|---|---:|
| Targets | 2,018 |
| Batch first-pass `add_spec` | 334 |
| Batch first-pass `skip` | 1,684 |
| Final `add_spec` | 111 |
| Final `skip` | 1,907 |
| Typechecked contracts | 109 |
| `R0 = unsat` | 59 |
| `R0 = unknown` | 40 |
| Guarded determinism reward | 1 |
| Semantic-gated reward | 0 |

Thus the remaining run produced many syntactically meaningful candidates, but
none added a new semantically accepted candidate beyond the original 94.

## 4. Why the remaining groups mostly stayed skipped

| Classification | Original count | Typical outcome |
|---|---:|---|
| Runtime, OS, I/O, or hidden state | 495 | Hidden state cannot be represented by ordinary result postconditions |
| Needs a new vstd abstraction | 361 | Some contracts typechecked, but existing views were insufficient |
| Trait-contract integration | 201 | Requires editing or extending external trait specifications |
| Unsafe or representation-sensitive | 181 | Pointer provenance and ownership effects were not modeled |
| Atomic/concurrent hidden state | 179 | First pass almost always selected skip |
| Mutable-reference return unsupported | 109 | Current determinism checker cannot compare these results |
| Iterator/adapter result | 101 | Requires prophetic iterator models |
| Formatting effect | 79 | Formatting state is not part of an ordinary logical view |
| Higher-order contract | 71 | Closure laws and call relations are required |
| Toolchain unavailable | 70 | API is absent from Verus's Rust 1.96 toolchain |

## 5. Final add-spec candidates by broad category

| Category | Add spec | Skip |
|---|---:|---:|
| Data structures | 158 | 487 |
| Other pure/core APIs | 21 | 369 |
| Runtime/OS/I/O | 17 | 478 |
| Memory/pointer APIs | 15 | 113 |
| Formatting | 2 | 77 |
| Trait methods | 1 | 204 |
| Atomic APIs | 0 | 179 |

Most runtime, formatting, pointer, and trait candidates that survived the batch
first pass were changed to skip after typechecking or semantic feedback.

## 6. The sole additional guarded-deterministic candidate

The remaining run found one candidate with guarded determinism:

```text
alloc::string::String::replace_range
```

Its contract normalized the generic range through repeated
`slice_range_start`/`slice_range_end` spec calls. A targeted semantic audit found
this likely unsound for arbitrary stateful `RangeBounds` implementations:
Rust normalizes the range once and reuses that snapshot.

The `generic_range_snapshot_mismatch` semantic gate therefore rejects it.

## 7. Overall interpretation

The classification step was useful:

- the 133 selected targets produced 103 deterministic contracts and 94
  semantic-gated candidates;
- the other 2,018 APIs produced 111 final add-spec texts, but no additional
  semantic-gated candidate;
- no target produced an SMT-confirmed incomplete (`sat`) candidate after final
  feedback;
- determinism is effective for checking completeness, but it cannot validate
  the soundness of trusted Rust external contracts.

The practical candidate set remains the 94 contracts from the original
suitable run, with four additional review flags for intentionally
underspecified APIs and model-heavy replacement operations.

## 8. Artifacts

- `all-2121-gpt56sol/ANALYSIS.md`: complete per-target combined result.
- `all-2121-gpt56sol/final_candidates.csv`: one final row per API.
- `remaining-generation/firstpass-gpt56sol/`: batched first-pass prompts and
  candidates for the remaining 2,018 APIs.
- `remaining-generation/evaluated-gpt56sol/`: per-classification checker and
  feedback artifacts.
- `remaining-generation/evaluated-gpt56sol/all-combined/`: combined remaining
  analysis.
- `SPECGEN-DETERMINISM-RESULTS-2026-07-22.md`: detailed report for the selected
  133-target run.

## 9. Why 1,907 final decisions are skip

The 1,907 skips have two different origins:

| Skip stage | Count | Share of skips |
|---|---:|---:|
| Model selected `skip` immediately | 1,684 | 88.3% |
| Initial `add_spec` changed to `skip` after feedback | 223 | 11.7% |

Final skips by original classification:

| Classification | Final skip |
|---|---:|
| Runtime, OS, I/O, or hidden state | 478 |
| Needs a new vstd abstraction | 356 |
| Trait-contract integration | 200 |
| Atomic/concurrent hidden state | 179 |
| Unsafe or representation-sensitive | 149 |
| Mutable-reference/checker unsupported | 109 |
| Iterator or adapter result | 101 |
| Formatting effect | 77 |
| Toolchain unavailable | 70 |
| Representation or allocator state | 54 |
| Higher-order contract | 34 |
| Suitable-first-run targets still skipped | 29 |
| Ownership or uninitialized-memory model | 25 |
| Complex result or pattern model | 20 |
| Associated type or projection | 17 |
| No modeled observable output | 9 |

The largest causes are semantic rather than syntactic:

- runtime and I/O APIs depend on filesystem, process, network, clock, lock, or
  other hidden state absent from the logical model;
- many data types have no existing `View`, so a useful result relation cannot be
  expressed without first adding a new vstd abstraction;
- trait and iterator APIs require associated-type, closure-state, or prophetic
  integration rather than a standalone `assume_specification`;
- pointer, allocation, and ownership APIs require tracked permissions and
  provenance that are not present in their ordinary Rust signatures;
- atomic operations may legitimately return different observations under
  interference, so ordinary functional determinism is the wrong specification
  shape.

For the 223 initial add-spec proposals that feedback changed to skip:

- 99 failed exact Verus contract typechecking;
- 26 remained solver-`unknown`;
- 51 required an unsupported external-trait contract form;
- 47 were runtime/hidden-state candidates;
- 32 were unsafe or representation-sensitive.

These counts overlap because one candidate can have several blockers.
Notably, 83 first-round candidates already had `R0 = unsat` but were still
changed to skip: determinism alone did not make the trusted contract useful or
semantically justified.

## 10. Abstraction continuation on 2026-07-29

The follow-up added value-level abstractions and source-audited contracts for
`Duration`, `Layout`, network addresses, C strings, panic locations,
`BinaryHeap`, `LinkedList`, capacity, ordering, control flow, and `VecDeque`.

The final newly-unlocked batch had 20 targets:

| Outcome | Count |
|---|---:|
| LLM guarded candidates | 10 |
| LLM skips | 10 |
| LLM errors after retry | 0 |
| Guarded candidates integrated after source audit | 10 |
| Additional contracts unlocked manually | 6 |
| Remaining unsupported targets | 4 |

The six additional contracts cover:

- `Duration::{mul_f32, div_f32}`;
- `Duration::{try_from_secs_f32, try_from_secs_f64}` using a new
  `TryFromFloatSecsErrorView`;
- `Duration::{div_duration_f32, div_duration_f64}` with an explicit NaN branch
  for `0 / 0`.

The four remaining targets require a different specification shape:

- `BinaryHeap::peek_mut`: guard/drop semantics and a `PeekMut` abstraction;
- `VecDeque::binary_search`: the returned equal-element index depends on the
  hidden ring-buffer split;
- `CString::new`: needs a contract for generic `Into<Vec<u8>>`;
- `Location::caller`: depends on implicit `#[track_caller]` state.

Two source-level soundness issues were also repaired:

- `Layout::align_to` now rejects zero and non-power-of-two requested
  alignments even when the existing layout has a larger alignment;
- `Result::from_residual` no longer claims `no_unwind` for an arbitrary
  `From<E> for F` conversion and now uses the existing `FromSpec` relation.

Validation:

| Module | Targets | `R0 = unsat` | `R0 = unknown` |
|---|---:|---:|---:|
| `duration.rs` | 36 | 34 | 2 |
| `layout_value.rs` | 13 | 13 | 0 |
| `location.rs` | 4 | 4 | 0 |
| `vecdeque.rs` | 32 | 28 | 4 |

The two new Duration unknowns are the intentional `0 / 0 -> NaN` branches.
The four VecDeque unknowns predate this continuation; both new
`swap_remove_*` contracts are `R0 = unsat`.

The complete modified vstd verifies successfully:

```text
verification results:: 2056 verified, 0 errors
```

After refreshing the survey, stable production coverage increased from
**538 / 2,464 (21.83%)** to **554 / 2,464 (22.48%)**. The original pre-
abstraction baseline was 343 covered stable APIs, so the experimental vstd now
adds 211 covered stable API paths in total. `core::time` is now fully covered
under this module-wide metric: **36 / 36 stable APIs**.

Eight of the Duration float contracts are conditional on
`duration_float_ieee_semantics()`. Nanvix's effective `x86-user` cfg contains
`target_feature="x87"` but not SSE2, so RFC 3514's finite-result guarantee is
not established for that target. Excluding these conditional contracts gives
conservative stable coverage of **546 / 2,464 (22.16%)**.

## 11. Source-level Verus verification

The external contracts were then copied or source-faithfully desugared into
ordinary Verus functions. This verifies the implementation body against the
postcondition instead of assuming the target method's contract.

| Level | Meaning | Contracts |
|---|---|---:|
| A | Self-contained body proof | 16 |
| B | Derived from smaller trusted std contracts | 47 |
| C | Also needs a representation/type invariant | 28 |
| D | Also needs a target floating-point semantics axiom | 8 |
| E | Source control flow copied, but central model equivalence remains trusted | 2 |
| **Total** |  | **101** |

All source-verification harnesses pass. The suite reports **93 contracts**
that do not use `duration_float_ieee_semantics()` and **8 conditional float
contracts**. This does not mean all 88 are free of other axioms: the two
`try_from_secs_f32/f64` mirrors remain Level E.

Representative verified bodies include:

- `VecDeque::{swap_remove_front, swap_remove_back}`;
- `Layout::{align_to, pad_to_align, extend, extend_packed, repeat,
  repeat_packed, array}`;
- all eight `Ordering` convenience methods;
- `ControlFlow` conversions and `Result`/`Option` branching;
- `IpAddr` and `SocketAddr` enum dispatch, including both setters;
- integer `Duration` constructors, accessors, checked and saturating
  arithmetic;
- source-faithful bit-level desugarings of
  `Duration::try_from_secs_f32/f64`;
- Duration float bodies under the explicit RFC/target predicate.

Artifacts and the reproducible runner are in:

```text
/home/chentianyu/nanvix-rust-std-spec-survey/source-verification/
```

## 12. All-vstd proof campaign

The scope was expanded from the 211 newly covered stable APIs to every direct
vstd `assume_specification` record:

| Metric | Count |
|---|---:|
| Direct contracts | 539 |
| Previously proved/exported | 101 |
| Remaining contracts attempted | 438 |
| Newly proved | 305 |
| Mechanically passing proof harnesses | **406** |
| Strict-faithful admissible local surrogates | **168** |
| Passing artifacts not retained | **238** |
| Original blocked records | **133** |

All 406 accepting harnesses were independently rerun. None directly proves an
original Rust std symbol: 405 map to local `source_*` surrogate functions and
one has an incorrect target mapping. After resolving all trait and macro
implementations, 168 records are conservatively retained across 141 unique
proof artifacts. A strict retry of all 204 alternate-implementation records
produced 20 Verus passes; independent review accepted 19 and rejected one.

Strict retained proof levels:

| Level | Count |
|---|---:|
| A | 54 |
| B | 112 |
| C | 2 |

Each passing contract has its own directory containing the proof, original
contract, Rust 1.96 source, and metadata:

```text
/home/chentianyu/nanvix-rust-std-spec-survey/source-verification/proved-apis/
```

The final 371 fallbacks consist of the original 133 blockers plus 238 passing
artifacts that changed the implementation, used inadmissible proof assumptions,
had a wrong target mapping, or could not be linked to a Rust source body. Full
details:

```text
/home/chentianyu/nanvix-rust-std-spec-survey/source-verification/surrogate-audit/SUMMARY.md
```

For one-click use, all contracts are grouped by original vstd source file:

```text
/home/chentianyu/nanvix-rust-std-spec-survey/source-verification/organized-suite/
```

- 168 entries use strict-faithful local-surrogate proofs;
- 371 entries use same-signature `#[verifier::external_body]`
  fallbacks retaining the original contracts.

Running `./verify.sh` verifies the complete suite: **539 passed, 0 failed**.

## 13. Determinism of every direct contract

All 539 direct contracts were checked with the same two-output R0 obligation.

The 539 records collapse to 447 canonical API paths. The 92 extra records come
from concrete trait implementations, bound/cfg variants, and separate source
contracts that intentionally share one canonical path; 33 paths have more than
one record.

| Record result | Current direct contracts |
|---|---:|
| Total contracts | 539 |
| Complete, nontrivial (`R0 = unsat`) | **382** |
| Solver `unknown` | 120 |
| Trivial/opaque equality | 4 |
| Checker unsupported | 17 |
| No local postcondition | 16 |
| SMT-confirmed incomplete (`R0 = sat`) | **0** |

At unique API-path level, **339 / 447** paths have every direct contract record
complete. Three paths have a mix of complete and non-complete records.

Within the 168 strict-faithful admissible local-surrogate proofs:

- 125 records are complete;
- 20 are solver-unknown;
- 23 are trivial, checker-unsupported, or have no local postcondition.

Detailed per-record and per-API results:

```text
/home/chentianyu/nanvix-rust-std-spec-survey/source-verification/determinism-report/
```

## 14. Paired determinism-feedback and proof comparison

Both columns use the same 2,121 generation targets. The no-feedback result is
the saved round-0 result; the with-feedback result is the saved final result.

| Status | No feedback | With feedback |
|---|---:|---:|
| Complete | **150** | **225** |
| Solver `unknown` | 68 | 40 |
| Trivial equality | 19 | 3 |
| No specification or checker failure | 1,884 | 1,853 |
| Confirmed incomplete (`sat`) | 0 | 0 |
| Complete among checker-valid contracts | **63.29%** | **83.96%** |

| Source-proof status | No feedback | With feedback |
|---|---:|---:|
| Strict-faithful admissible proof | **89** | **99** |
| Verus pass rejected by fidelity review | 36 | 24 |
| No passing proof | 112 | 79 |
| No checker-valid specification | 1,884 | 1,919 |
| Strict proof rate among checker-valid contracts | **37.55%** | **49.01%** |

Full paired tables and the no-spec reason taxonomy:

```text
/home/chentianyu/nanvix-rust-std-spec-survey/source-verification/feedback-comparison/
```
