# Independent Reviewer decision: target 051

**VERDICT: ACCEPT**

This acceptance covers only input order 051,
`core::slice::get_disjoint_mut`. It preserves the accepted decisions for
targets 013, 022, 029, 081, 106, and 120 and does not authorize a Manager
stage transition.

## Fresh verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_target_051.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/replay_target_051.py \
  --evidence-root evidence/targets/051_core_slice_get_disjoint_mut \
  --z3 /home/chentianyu/miniconda3/bin/z3
z3 -smt2 evidence/targets/051_core_slice_get_disjoint_mut/obligation.smt2
z3 -smt2 evidence/targets/051_core_slice_get_disjoint_mut/exact_output_obligation.smt2
z3 -smt2 evidence/targets/051_core_slice_get_disjoint_mut/witnesses/out_of_bounds_error_variants.smt2
z3 -smt2 evidence/targets/051_core_slice_get_disjoint_mut/witnesses/valid_disjoint_distinct_borrows.smt2
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_authority_design.py
../../verus/source/target-verus/release/verus \
  proofs/051_core_slice_get_disjoint_mut.rs --crate-type=lib --no-verify
../../verus/source/target-verus/release/verus \
  proofs/051_core_slice_get_disjoint_mut.rs --crate-type=lib
```

The full acceptance sequence completed all 17 commands successfully. Python
compilation completed with status zero, 152 tests ran and reported `OK`, all
seven target pipelines passed, and local validation reported
`validation=PASS`. Direct Verus type-checking completed with status zero and
verification reported `5 verified, 0 errors`.

Direct Z3 execution returned `sat` for both theorem negations, both fixed
witnesses, the two validation-loop cases, and the canonical construction
case. It returned `unsat` for the out-of-bounds success reference,
overlapping success references, and prior-slot mutation probes. The replay
confirmed that both executions in each fixed witness satisfy the active
contract under one shared boundary and are not exactly equivalent.

## Review findings

| Check | Decision |
|---|---|
| Authority and source binding | Accepted. Direct content comparisons bind the active catalog contract, generated declaration, canonical public item and docs, validation loop, unchecked borrow-construction loop, `usize` index semantics, retained harness, and all three retained manifests to the packaged inputs. |
| Boundary adequacy | Accepted. `Boundary_T` contains only initial slice values, allocation/address/provenance, receiver borrow identity, element layout/platform limits, and the outside-frame token. It excludes validity, error kind, returned borrows, alias maps, resulting state, implementation choice, and traces. |
| Source-backed replacement | Accepted. The validation loop derives the Result tag in source order. The bounded two-slot construction derives in-receiver references and preserves the first initialized slot across the second write. The four answer-bearing retained sites are excluded rather than admitted under new names. |
| Contract fidelity | Accepted. `Spec_T` forwards exactly to `TargetDefinition_T`. It enforces the active Ok/Err implications and Rust reference well-formedness without fixing the implementation-selected error variant or returned borrow indices. |
| Literal theorem and equivalence | Accepted. Both executions share the same `x` and `b`. Exact equivalence covers the Result tag, error variant, all returned-reference observations, and, for the full obligation, every final-state observation. |
| Concrete incompleteness witnesses | Accepted. The fixed out-of-bounds case admits both public error variants with the same final state. The fixed valid-disjoint case admits canonical `[0, 2]` and distinct well-formed `[1, 2]` receiver-borrow arrays with the same final state. Both are contract-satisfying and exact equality fails. |
| Negative and boundary probes | Accepted. Executed checks reject answer-bearing boundaries, opaque validity, deterministic error or borrow-choice injection, invalid and overlapping successful references, prior-slot mutation, negative `usize` encodings, mismatched boundaries, and Result tags inconsistent with validity. |
| Scope and preservation | Accepted. The active manifest/catalog derivation yields 120 generated Slice contracts and exactly 62 selected UNKNOWN rows. Exactly seven rows are classified and 55 remain `not-run`. Direct byte-content comparisons found targets 013, 022, 029, 081, 106, and 120 unchanged. |

