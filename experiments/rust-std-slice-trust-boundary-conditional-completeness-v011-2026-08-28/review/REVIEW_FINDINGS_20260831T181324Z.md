# Independent Reviewer findings: search-wrapper cluster

**VERDICT: CHANGES REQUIRED**

This review covers only input orders 028 `core::slice::binary_search`, 030
`core::slice::binary_search_by_key`, and 065 `core::slice::partition_point`.
It does not authorize a stage transition.

## Material finding

### F1: Targets 028 and 030 conditionally drop the accepted lower transition

The canonical wrappers delegate to `binary_search_by` unconditionally:

- `core/src/slice/mod.rs:2922-2924`
- `core/src/slice/mod.rs:3075-3077`

The SMT wrapper transitions instead require
`ReviewedBinarySearchByLowerResult` only when the upper target's sortedness
predicate holds:

- `tools/search_family.py:399-405`
- `tools/search_family.py:489-496`

The Verus source-transition models repeat the same conditional composition:

- `proofs/028_core_slice_binary_search.rs:123-133`
- `proofs/030_core_slice_binary_search_by_key.rs:123-133`

Upper sortedness and lower comparator-profile orderedness are not equivalent.
Fresh Z3 probes demonstrated both missing branches:

- For 028, elements `[2, 1]` searched for `3` produce the fixed comparator
  profile `[Less, Less]`. `SliceSortedByOrd` is false,
  `ComparatorProfileOrdered` is true, the chosen `Ok(0)` violates the reviewed
  lower relation, yet `Spec_T` is true.
- For 030, extracted keys `[KHigh, KMid]` searched against `KLow` produce
  `[Greater, Greater]`. `ExtractedKeysOrdered` is false,
  `ComparatorProfileOrdered` is true, the chosen `Ok(0)` violates the reviewed
  lower relation, yet `Spec_T` is true.

Thus the replacement transition omits a real source delegation branch and is
not yet a faithful source-backed replacement for the retained answer-bearing
sites. The existing SAT witnesses use genuinely unordered lower profiles, so
this finding does not by itself determine different final classifications.
The obligations and evidence must nevertheless be regenerated from a model
that composes the accepted lower relation unconditionally.

Add fail-closed regressions asserting that, for 028 and 030,
`SourceBacked...` implies `ReviewedBinarySearchByLowerResult` even when the
upper sortedness predicate is false. Mirror the correction in both Verus
models, replay all target evidence, and rerun the independent Reviewer gate.

## Fresh verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

It reported `acceptance=PASS` for all 26 commands. Python compilation
succeeded, 198 tests passed, the local validator passed, and each of the three
Verus models separately type-checked and reported
`verification results:: 3 verified, 0 errors`.

Direct Z3 replay returned SAT for each general and exact-output obligation and
UNSAT for each ordered/partitioned sanity obligation. All six fixed SAT
models and independent contract-witness replays also passed. A direct
file-content comparison around the acceptance run found no changes in any of
the 11 certified evidence trees. The crosswalk remains at 14 classified and
48 `not-run` rows.

These successful mechanical checks do not cover F1, so independent acceptance
is withheld.
