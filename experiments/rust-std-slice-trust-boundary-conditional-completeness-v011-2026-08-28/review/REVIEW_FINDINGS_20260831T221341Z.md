# Independent Reviewer findings: target 077

**VERDICT: CHANGES REQUIRED**

This review covers only input order 077
`core::slice::select_nth_unstable`. It does not classify targets 078-079 or
authorize a Manager stage transition.

## Fresh verification

The active generated declaration, canonical Rust item and public docs, frozen
harness, transformation manifest, dependency manifest, source-body record,
and all five `TS-077` trust records are present and consistently bound.
`TS-077-D002` and `TS-077-E001` remain excluded,
`TS-077-D001` and `TS-077-C001` remain context-only, and only
`TS-077-D003` backs the two Ord boundary fields. Rows 078 and 079 remain
`not-run`; the current ledger has 25 classified and 37 `not-run` rows.

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m compileall -q tools tests
PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s tests -p 'test_target_077.py' -v
../../verus/source/target-verus/release/verus \
  proofs/077_core_slice_select_nth_unstable.rs --crate-type=lib --no-verify
../../verus/source/target-verus/release/verus \
  proofs/077_core_slice_select_nth_unstable.rs --crate-type=lib
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_target_077.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_authority_design.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

Compilation completed successfully. The targeted suite ran 15 tests and the
full suite ran 266 tests; both reported `OK`. The Verus model type-checked and
reported `verification results:: 5 verified, 0 errors`. The target pipeline
and local validation reported `PASS`, and the acceptance driver passed all 30
commands. These mechanical checks do not cover the semantic finding below.

The fixed-input/fixed-boundary exact witness also replays against an
independent concrete active-contract checker: both executions preserve the
input identity multiset and partition around the selected rank while differing
in side order. It supports exact-output/final-state
`conditional-incomplete`.

## Blocking finding

### F1: The general UNSAT theorem is over disconnected summary fields, not the active sequence contract

`tools/target_077.py:113-156` declares the initial/final sequences and their
identity, class, and rank summaries as independent datatype fields.
`InputSummaryValid` at lines 165-195 does not derive the input summaries from
`x_initial_sequence` and `b_ord_class`. `ActivePermutationConjunct` at lines
354-356 compares only the free `s_final_identity_multiplicity` summary, and
`ActiveOrdPartitionConjunct` at lines 357-372 compares only the free side-class
summaries. Neither constrains those summaries to describe
`s_final_sequence`.

Two source-independent Reviewer probes held the same valid input and same Ord
boundary fixed:

1. The final sequence contained foreign identity `99`, while
   `s_final_identity_multiplicity` retained the original input multiset.
2. The final sequence crossed the partition by placing a greater-class
   identity on the left and a lesser-class identity on the right, while the
   side-class summary arrays retained the expected counts.

Z3 returned `sat` for `Requires_T(x)`, `Boundary_T(x,b)`, and
`Spec_T(x,b,y,s)` in both cases. The generated active contract rejects the
first sequence through `slice_permutation` and the second through
`slice_select_partition_ord`. Consequently, the model's general `unsat`
result does not prove completeness modulo the stated equivalence over actual
final sequences.

The named source transitions also do not provide the missing link. Replacing
each individual source-transition call other than `PartitionTransition` with
`true` left the general theorem `unsat`; replacing each individual active
contract conjunct with `true` did the same.
`RecursiveLoopOrFallbackTransition` at lines 297-310 is vacuous on the
interior branch because the existential can choose zero iterations and the
only remaining semantic condition repeats `RankSelected`, already imposed by
`PartitionTransition`. The current deletion tests reject text that differs
from the generator, but do not test that these transitions constrain a
source-reachable execution.

Derive input multiplicity/rank summaries from the physical input sequence and
shared Ord observation, and derive final identity/side-class summaries from
the final sequence. Encode non-vacuous source-path transitions, especially
recursive narrowing and fallback, rather than a fresh existential branch tag.
Add regressions requiring both malformed-sequence probes above to be
unsatisfiable and requiring same-input/same-boundary rank summaries to be
unique. Then regenerate target 077 evidence, rerun the complete acceptance
campaign, and request independent review again.

The present modulo-selection `conditional-complete` ledger value is not
independently accepted.

**No stage transition is authorized by this review.**
