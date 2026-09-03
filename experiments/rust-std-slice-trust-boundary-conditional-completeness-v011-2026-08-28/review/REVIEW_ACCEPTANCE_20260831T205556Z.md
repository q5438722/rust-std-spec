# Independent Reviewer decision: MaybeUninit lifecycle cluster

**VERDICT: ACCEPT**

**Timestamp:** 2026-08-31T20:55:56Z

This decision covers only input orders 025
`core::slice::assume_init_drop`, 026 `core::slice::assume_init_mut`, and
119 `core::slice::write_clone_of_slice`. It does not authorize a Manager
stage transition.

## Contract, source, and boundary review

- Direct readable-content comparisons bind each active contract and generated
  declaration to its canonical Rust item and public documentation, frozen
  implementation-proof harness, transformation manifest, dependency manifest,
  source-body record, and complete target-specific trust-site inventory.
- Target 025 excludes `TS-025-D002` and `TS-025-E001` rather than relabeling
  them. Its replacement derives the nonempty branch, raw slice identity,
  increasing per-element drop order, exact drop count, Destruct-state chain,
  final uninitialized storage, and outside frame. The reachable
  `DropSourceExecution_T` relation uses the per-step index and storage
  transitions.
- Target 026 excludes `TS-026-D002` and `TS-026-E001` rather than relabeling
  them. Its replacement is the lower layout-preserving mutable-slice cast:
  allocation, address, provenance, borrow identity, length, and initial values
  are source-derived, while in-range final values remain free exactly where the
  returned mutable reference permits them to vary.
- Target 119 admits its retained Clone, one-slot write, and Guard-effect sites
  only as lower per-step observations. It derives source order and counts,
  composes the target-026 cast after initialized storage is established, and
  derives normal Guard-forget behavior. Its panic relation reuses the reachable
  successful-prefix clone/write transition and derives initialized-prefix
  cleanup through per-element Destruct transitions.
- Each `Boundary_T` contains only initial storage and initialization,
  memory/layout/address/provenance and borrow/frame identity, plus individual
  Clone or Destruct outcomes and state transitions. Returned references,
  resulting storage, aggregate callback state, operation order/count, answer
  encodings, and complete traces are absent.
- All active contract conjuncts are represented. Both obligations use exact
  equality for their modeled principal observations; no weakened equivalence
  is introduced.

## Fresh Reviewer execution

Python compilation and the target suite were run with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m compileall -q tools tests
PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s tests \
  -p 'test_maybeuninit_lifecycle_cluster.py' -v
```

Compilation completed successfully. The target suite ran 19 tests and reported
`OK`. It exercised all six theorem obligations, all target probes, the fixed
target-026 counterexample, contract replay, boundary guards, reachable
write/drop ordering and panic cleanup, delivered-state reset behavior, and
out-of-scope ledger rejection.

The retained obligations were replayed directly with Z3:

| Target | Full exact equivalence | Exact output |
|---|---|---|
| 025 `assume_init_drop` | `unsat` | `unsat` |
| 026 `assume_init_mut` | `sat` | `unsat` |
| 119 `write_clone_of_slice` | `unsat` | `unsat` |

An independent replay executed all six obligations and 58 positive/negative
solver probes. The target-026 fixed model returned `sat`; its content-level
replay used the same valid input and boundary in both executions, satisfied
all ten checked contract conditions in each execution, returned the same
mutable-slice identity and initial values, and produced unequal final
initialized storage. This supports exact-output conditional completeness and
full exact-state conditional incompleteness for target 026.

All three experiment-local Verus models were separately run with
`--no-verify` and then verified. Type-checking completed with empty output and
empty stderr. Verification reported:

```text
025: verification results:: 2 verified, 0 errors
026: verification results:: 2 verified, 0 errors
119: verification results:: 3 verified, 0 errors
```

None of the three models contains `external_body`.

The standalone cluster runner passed first from the certified 19-target entry
state and again from the delivered 22-target state:

```bash
PYTHONDONTWRITEBYTECODE=1 \
  python3 tools/run_maybeuninit_lifecycle_cluster.py
```

Both runs reported the expected three classifications, a passed independent
replay, three clean Verus models, 19 preserved evidence trees, and a final
22-classified/40-`not-run` ledger.

Finally, the Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

All 28 commands completed successfully. Python compilation succeeded, 233
tests ran and reported `OK`, the local validator passed, and the bounded
cluster completed. Direct before/after content comparisons found the complete
CSV and JSON ledgers and all 19 previously certified evidence trees unchanged
across this acceptance replay.

## Final scope state

The CSV and JSON crosswalks agree on all 62 selected rows. Exactly 22 rows are
classified and 40 remain `not-run`. The bounded rows record:

- 025: exact output `conditional-complete`; full exact state
  `conditional-complete`
- 026: exact output `conditional-complete`; full exact state
  `conditional-incomplete`
- 119: exact output `conditional-complete`; full exact state
  `conditional-complete`

**No stage transition is authorized by this review.**
