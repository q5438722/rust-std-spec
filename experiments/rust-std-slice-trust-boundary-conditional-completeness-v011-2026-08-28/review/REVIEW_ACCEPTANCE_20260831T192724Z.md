# Independent Reviewer decision: strengthened chunk-contract cluster

**VERDICT: ACCEPT**

**Timestamp:** 2026-08-31T19:27:24Z

This decision covers only input orders 012 `core::slice::as_chunks`, 014
`core::slice::as_chunks_unchecked`, 015
`core::slice::as_chunks_unchecked_mut`, 023 `core::slice::as_rchunks`, and
024 `core::slice::as_rchunks_mut`. It does not authorize a stage transition.

## Contract, source, and boundary review

- The SMT translations retain every active strengthened partition, quotient
  or remainder length, initial subrange, mutable final length, final frame,
  and final subrange conjunct. The weaker retained contracts are not used.
- The implementation order is 014 -> 015 -> 012 -> 023 -> 024. Target 014
  composes the accepted 021 slice-to-pointer semantics, target 015 composes
  the accepted 019 mutable cast semantics, targets 012 and 023 compose 014,
  and target 024 composes 015.
- Target 015 excludes `TS-015-D006` and `TS-015-E002`. Their complete
  postconditions are replaced by explicit pointer-cast, array-pointer-cast,
  raw-slice construction, shared-storage alias, and mutable final-view
  transitions derived from the canonical Rust bodies.
- Target 012 derives front chunks and a rear remainder. Targets 023 and 024
  derive a front remainder and rear chunks. Concrete source-derived probes
  accepted these orientations and rejected their swapped forms.
- `Boundary_T` contains only initial allocation, address, provenance, layout,
  initialization, borrow, mutability, exclusivity, platform-limit, and frame
  observations. No returned reference, range, chunk or remainder value, final
  storage or view, answer encoding, or execution trace is present.
- Both obligations use exact equality for every modeled principal return and
  final-state observation; no weakened equivalence is introduced.

## Fresh Reviewer verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

All 27 commands completed successfully. Python compilation completed with
empty output, and 214 tests ran and reported `OK`.

The Reviewer also replayed the ten theorem files directly with Z3:

| Target | Full reviewed equivalence | Exact output |
|---|---|---|
| 012 `as_chunks` | `unsat` | `unsat` |
| 014 `as_chunks_unchecked` | `unsat` | `unsat` |
| 015 `as_chunks_unchecked_mut` | `sat` | `unsat` |
| 023 `as_rchunks` | `unsat` | `unsat` |
| 024 `as_rchunks_mut` | `sat` | `unsat` |

The target-015 and target-024 SAT results have fixed-input, fixed-boundary
models and independent concrete replays. Both executions return the same
source-derived initial views, satisfy every active conjunct, and differ only
in final values legally written through the returned mutable views. The
immutable and exact-output UNSAT results therefore support the recorded
classifications.

All five experiment-local Verus models separately type-checked and reported
`1 verified, 0 errors`, with empty stderr and no `external_body`.

An additional Reviewer-owned adversarial run completed 205 checks. It removed
each principal equality, each primary active-conjunct call, each mutable
exact-output final-contract bridge, and each upper lower-transition call and
confirmed fail-closed rejection. It also exercised independently derived
front/rear geometry, pointer address and provenance, N=0, null and misaligned
pointers, isize overflow, empty slices, and ZST slices.

## Scope and preservation

A direct recursive content comparison around the fresh acceptance run found no
change in any of the 14 previously certified evidence trees. The CSV and JSON
ledgers agree semantically on 62 rows. Exactly 19 rows are classified and 43
remain `not-run`; only the two result fields of the five bounded rows carry
this increment's classifications.

**No stage transition is authorized by this review.**
