# Independent Reviewer decision: target 120

**VERDICT: ACCEPT**

This acceptance covers only input order 120,
`core::slice::write_copy_of_slice`. It preserves the accepted decisions for
targets 013, 022, 029, 081, and 106 and does not authorize a Manager stage
transition.

## Fresh verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

All 16 commands completed successfully. Python compilation completed with
status zero, 140 tests ran and reported `OK`, all six target pipelines passed,
and local validation reported `validation=PASS`.

The Reviewer then directly ran Z3 on both retained target-120 theorem
obligations and all 12 domain/rejection probes. The full exact-state and exact
output theorem negations each returned clean `unsat`. Empty, wholly
uninitialized, mixed-initialization, and fully initialized valid destinations
returned `sat`. Unequal lengths, a no-op copy, a partial copy, omitted
initialization, wrong destination identity, wrong returned-reference identity,
changed source, and changed outside frame each returned `unsat`.

Direct Verus type-checking completed with status zero. Direct verification
reported `3 verified, 0 errors`, and the target-local model contains no
`external_body`.

## Review findings

| Check | Decision |
|---|---|
| Authority and source binding | Accepted. Direct content comparisons bind the active and retained contract text, generated declaration, public docs, canonical Rust target item, transmute, `copy_from_slice`, `copy_nonoverlapping`, `assume_init_mut`, retained harness, and three proof manifests to the packaged inputs. |
| Contract interpretation | Accepted. `TargetDefinition_T` expands every active return, length, initialization, written-from, and final-view conjunct. It admits arbitrary equal nonnegative lengths and uses exact output and final-state equality. |
| Per-slot storage semantics | Accepted. A datatype distinguishes `Uninitialized` from `Initialized(value)`. The raw-copy transition maps each source value to an initialized destination cell without projecting a value from an uninitialized destination cell; the source and outside frame remain unchanged. |
| Memory and identity semantics | Accepted. The model includes source and destination allocation, address, provenance and bounds, element layout, platform limits, non-overlap for nonzero copies, destination mutable-borrow identity, and exact returned-reference identity. Empty and zero-byte behavior remains in the valid domain. |
| Boundary adequacy | Accepted. The shared boundary contains only initial source/destination storage, initialization, memory/provenance, destination borrow, layout, platform limits, and the pre-existing frame token. It contains no resulting storage, returned reference, answer encoding, or execution trace. `TS-120-D004` and `TS-120-E005` are excluded rather than renamed or reused. |
| Literal theorem | Accepted. Both executions share the same `x` and `b`; `Spec_T` forwards to the explicit source transition; every principal output and state field is covered; and both negated implications replay as clean `unsat`. |
| Negative guards | Accepted. Executed tests reject aggregate final-storage boundaries, retained-site reuse, reads from uninitialized cells, no-op or partial copies, omitted initialization or value updates, unequal lengths, wrong destination/return identity, source/frame mutation, and out-of-scope crosswalk result changes. |
| Scope and preservation | Accepted. CSV and JSON contain the same 62 selected rows. Exactly targets 013, 022, 029, 081, 106, and 120 are classified, target 120 has both result fields set to `conditional-complete`, and 56 rows remain `not-run`. Direct before/after comparisons found the complete crosswalk and all five previously accepted evidence trees byte-for-byte unchanged. |
