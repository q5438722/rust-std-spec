# Independent Reviewer decision: targets 080 and 082

**VERDICT: ACCEPT**

**Timestamp:** 2026-08-31T21:36:48Z

This decision covers only input order 080 `core::slice::sort_unstable` and
input order 082 `core::slice::sort_unstable_by_key`. It does not import target
081's classification, modify selection targets 077-079, or authorize a
Manager stage transition.

## Contract, source, equivalence, and boundary review

- Direct readable-content comparisons bind each active generated declaration
  to its crosswalk contract, canonical Rust item and stripped public rustdoc,
  frozen harness, transformation manifest, dependency manifest, source-body
  record, and complete trust-site inventory.
- The Rust items call the private unstable sorter through `T::lt` or through
  key extraction followed by `K::lt`. The `Ord` documentation and generated
  vocabulary supply the target-specific reflexive, dual, total, and transitive
  ordering laws. No target-081 result is used.
- Target 080 admits only lower Ord observations from `TS-080-D003`; target 082
  admits only lower key-extraction and key-Ord observations from
  `TS-082-D004`. `TS-080-D002`, `TS-080-E001`, `TS-082-D002`,
  `TS-082-D003`, and `TS-082-E001` remain explicitly excluded.
- `Boundary_T` contains only extensional Ord/key observations and a callback
  state transition. It contains no result slice, permutation, selected order,
  aggregate final state, pivot or swap choice, answer encoding, or execution
  trace.
- The reviewed equivalence keeps unit return, exact identity multiplicities,
  callback final state, and the class at every position exact. It permits only
  source-documented reordering within an equal Ord or equal-key class.

## Solver and witness review

The general obligations quantify arbitrary nonnegative length, arbitrary
identity multiplicities, and an arbitrary valid position when nonempty. Their
order-statistic summaries are answer-independent consequences of input
multiplicity plus the shared Ord/key boundary. Exact permutation and
sortedness place each result identity in the interval for its class; total
order separates different class intervals.

Direct Z3 replay returned `unsat` for both general reviewed-equivalence
theorems. Both separate length-three sanity obligations also returned
`unsat`, but are labeled sanity-only. Both exact-final-slice obligations and
both fixed equal-class models returned `sat`.

The fixed models use one valid input and one boundary for both executions.
Each execution satisfies the exact permutation and sortedness conjuncts,
returns unit, preserves identity multiplicities and callback final state, and
has the same class at every position. The final identity sequences differ only
inside the equal class. Positive equal-class witnesses and negative
foreign-identity, unequal-class, callback-state, and key-state witnesses all
replayed with the required polarity.

## Fresh Reviewer execution

The Reviewer ran Python compilation and the targeted suite:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m compileall -q tools tests
PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s tests \
  -p 'test_unstable_sort_companions.py' -v
```

Compilation completed successfully. The targeted suite ran 18 tests and
reported `OK`.

Both experiment-local Verus models were type-checked with `--no-verify` and
then verified normally. Each reported:

```text
verification results:: 3 verified, 0 errors
```

Their type-check and verification stderr captures are empty, and neither model
contains `external_body`.

The standalone campaign, local validator, full suite, and acceptance driver
were then run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_unstable_sort_companions.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_authority_design.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

The campaign and validator reported `PASS`. The full suite ran 251 tests and
reported `OK`. The acceptance driver completed all 29 commands and reported
`acceptance=PASS`.

An independent 58-case probe additionally confirmed that deleting permutation,
sortedness, unit return, or callback-state constraints makes the bounded
negated theorem satisfiable; zero- and one-length general cases remain
unsatisfiable; invalid return types, lengths, identities, orderings, callback
states, and boundaries are rejected; all principal and boundary fields are
mapped; and solver/Verus argument ordering is retained.

## Scope and preservation

Direct before/after byte comparisons, rather than integrity identifiers,
confirmed that all 22 certified target evidence trees, both crosswalk formats,
and every frozen row-077/078/079 selection artifact were unchanged by the
fresh campaign and full acceptance replay. The two ledger rows record:

- 080: exact output `conditional-incomplete`; reviewed equal-Ord equivalence
  `conditional-complete`
- 082: exact output `conditional-incomplete`; reviewed equal-key equivalence
  `conditional-complete`

The selected ledger now contains exactly 24 classified rows and 38 `not-run`
rows. No stage transition is authorized by this review.
