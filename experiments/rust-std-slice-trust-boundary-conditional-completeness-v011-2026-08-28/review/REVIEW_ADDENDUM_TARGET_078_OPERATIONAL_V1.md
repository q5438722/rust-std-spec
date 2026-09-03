# Independent Reviewer addendum: target 078 operational v1

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T18:30:03Z

This decision covers only the additive operational-v1 evidence for input order
078, `core::slice::select_nth_unstable_by`. It does not alter the certified
campaign result, classify target 079, or authorize a Manager-owned stage
transition.

## Decisive repair

The classification transition is now the fuel-free `ExactRunState` big-step
interpreter in `tools/target_078_exact_smt_v1.py`. It follows the source
callback and mutation order for insertion and CopyOnDrop, extrema, recursive
pivot selection, all three partition families and their gap restoration,
ancestor-pivot handling, both narrowing directions, the sixteen-step
introselect limit, median-of-ninthers fallback, panic propagation, and normal
return. `RunMachine` projects only a completed exact state; the former compact
finite control machine remains local force-probe scaffolding and is not the
classification transition.

The fixed descending length-17, index-8 cyclic case now compares the exact
formal `RunMachine` directly with the Python source interpreter. It requires
terminal status and equality of the full final slice, callback state, panic
status, and every principal-return field. The regression is clean UNSAT with
the source final slice:

```text
(0, 7, 6, 5, 4, 3, 2, 1, 8, 15, 13, 12, 11, 10, 9, 16, 14)
```

The Python callback boundary no longer has finite observation tables or a
`freeze()` path. Its declarative implementation relations are total for every
state and identity pair. Contract Ordering is a separate state-independent
projection. Classification-admissible boundaries require exact equality
between implementation and contract Ordering at every state and enforce the
frozen reflexive, dual, total, and transitive laws; state-dependent operational
fixtures are explicitly rejected as contract observations.

The Verus artifact no longer contains the rejected compressed source
transition. It is a trusted-free, parameterized checked refinement from a
terminal exact interpreter result to the formal result representation. The
projection copies and proves equality of return presence, all three ranges,
allocation and borrow identities, pivot identity, final sequence, final
allocation, final borrow, final length, callback state, panic status, and
terminal status. Dropping the sequence projection makes verification fail.

## Fresh focused evidence

Fresh checks completed Python compilation of the exact generators, both
arbitrary-domain SMT obligations, the length-17 formal/source correspondence,
normal and panic correspondence probes, 20 operational tests with 241
subtests, artifact force and mutation probes, Verus verification with
`5 verified, 0 errors`, and the negative Verus projection mutation. No
high-confidence source-transition or retained-field mismatch remains.

The complete supervised gate
`target-078-operational-v1-acceptance-r2-1788287486470306433` then completed
with 30 focused tests and 314 subtests, five verified Verus obligations, the
target runner, all 505 unit tests, and all 45 acceptance commands. It preserved
target 079, certified target-078 evidence, both frozen trees, final campaign
artifacts, the certified ledgers, and `research/PIPELINE_STATE.json`.
