# Independent Reviewer decision: mutable Slice view construction

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T13:50:04Z

This decision covers only input orders 017
`core::slice::as_flattened_mut`, 018 `core::slice::as_mut_array`, 046
`core::slice::first_chunk_mut`, and 047 `core::slice::from_mut` against the
independently accepted 56-target baseline. It does not authorize a
Manager-owned stage transition.

## Readable semantic review

The Reviewer inspected all four literal active declarations, their generated
view vocabulary, the Rust 1.96 implementations and public docs, the canonical
pointer and array helper bodies, all four frozen implementation-proof
harnesses, all 16 bound proof manifests, all 34 trust records, both generated
obligations per target, the fixed witnesses, the target-local Verus models,
and the retained command and solver captures. Integrity identifiers were not
used as evidence; authority and preservation were judged from readable
content, direct execution, and byte-content comparisons.

The active contracts remain unchanged. Retained sites
`TS-017-D006`/`TS-017-E004`, `TS-018-D004`/`TS-018-E002`,
`TS-046-D004`/`TS-046-E002`, and `TS-047-D001`/`TS-047-E001` remain
inadmissible complete-result or complete-branch bridges. The new obligations
exclude those sites and replace them with defined source transitions rather
than relabeling them as boundary observations.

The replacement follows the canonical source order: checked multiplication
and the ZST overflow panic, valid non-ZST unchecked multiplication, exact
`len == N` or `N <= len` branch selection, mutable pointer extraction,
pointer casts, raw-slice or mutable array-reference construction, exact
returned ranges, and preservation of allocation, provenance, and live
exclusive root-borrow identity. Target 047 additionally derives the
singleton array reference and array-to-slice unsizing from a project-local
excerpt of canonical Rust 1.96 `core/src/array/mod.rs:174-177`; that excerpt
is outside the frozen authority tree.

Every theorem uses one shared valid input `x` and one shared boundary
observation `b`. `Boundary_T` contains only initial and outside-frame memory,
addresses, allocation extents, provenance, root-borrow identity and
liveness, exclusivity, element layout, and usize/isize platform limits. It
contains no multiplication result, branch choice, returned value, range,
pointer or borrow result, projection, final state, answer encoding, or trace.
All branch, return, identity, and frame observations are derived after the
boundary.

Exact-output equivalence compares the complete panic or option outcome,
values, range, address, allocation, provenance, root borrow, layout,
projection, and uniqueness. Full-state equivalence additionally compares
receiver, returned-view, outside-memory, and backing-identity frames.
`BorrowLifetimeFinalFrameTransition` fixes successful returned lengths and
receiver/return reconstruction while leaving returned mutable contents free;
target 046 also retains the old suffix. Panic and `None` paths preserve the
input and create no returned frame. This matches the active `final(...)`
relations without the rejected strengthening that fixed successful contents
to their initial values.

The retained source cases cover empty and nonempty receivers, ZST and
non-ZST elements, `N = 0`, `N < len`, `N = len`, `N > len`, checked
multiplication overflow, valid unchecked multiplication, and singleton
unsizing. The negative set rejects null, misaligned, allocation-invalid,
out-of-range, provenance-free, nonexclusive, dead-borrow, wrong-branch,
wrong-range, wrong-identity, wrong-projection, wrong-frame, and
answer-laundering alternatives.

## Independent execution

- Forced Python compilation of `tools` and `tests` completed successfully.
- All 13 focused mutable-view tests and all 455 repository tests passed.
- Each of the four trusted-free Verus models type-checked, then verified two
  obligations with zero errors and no `external_body`.
- Direct Z3 replay produced four exact-output `unsat` results, four
  full-state `sat` results, four fixed-input/fixed-boundary witness `sat`
  results, 22 source-instance `sat` results with models, and 82
  semantic/domain-probe `unsat` results.
- A separate source-derived 17-case probe checked complete output, default,
  identity, range, and frame mappings. Every correct mapping was `sat`; a
  disjunction allowing any wrong mapped field was `unsat`.
- The bounded runner, focused evidence validator, integrated authority
  validator, and complete 42-command acceptance driver passed.

## Preservation and decision

A direct byte-content comparison found all 6,376 files in the complete
target-evidence tree unchanged across the full acceptance replay, including
all 56 certified predecessor evidence trees. All 320 frozen input files and
both crosswalk serializations were also unchanged. The row-update test
confirms that only the two result fields on rows 017, 018, 046, and 047 are
changed by this bounded increment.

All four targets are accepted as exact-output `conditional-complete` and
full-state `conditional-incomplete`. The selected ledger contains exactly 60
classified rows and 2 `not-run` rows, which are the out-of-scope `align_to`
pair. Stage transition remains disabled.
