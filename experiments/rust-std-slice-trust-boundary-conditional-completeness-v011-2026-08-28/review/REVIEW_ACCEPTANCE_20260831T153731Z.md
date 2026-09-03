# Independent Reviewer decision: target 052

**VERDICT: ACCEPT**

This acceptance covers only input order 052,
`core::slice::get_disjoint_unchecked_mut`. It preserves the accepted decisions
for targets 013, 022, 029, 051, 081, 106, and 120 and does not authorize a
Manager stage transition.

## Fresh verification

The Reviewer ran the repository's complete acceptance driver, a standalone
target-052 pipeline with direct byte-content preservation checks, every
target-052 SMT artifact directly through Z3, an independent concrete-witness
probe, the local validator, and direct Verus type-checking and verification:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_target_052.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_authority_design.py
../../verus/source/target-verus/release/verus \
  proofs/052_core_slice_get_disjoint_unchecked_mut.rs --crate-type=lib --no-verify
../../verus/source/target-verus/release/verus \
  proofs/052_core_slice_get_disjoint_unchecked_mut.rs --crate-type=lib
```

The full acceptance sequence completed all 18 commands successfully. Python
compilation completed with status zero, 165 tests ran and reported `OK`, all
eight target pipelines passed, and local validation reported
`validation=PASS`. Direct Verus type-checking completed with status zero and
verification reported `4 verified, 0 errors`.

Direct Z3 execution covered all 11 target-052 SMT artifacts. Both literal
theorem negations, the fixed witness, and the three positive source-transition
probes returned `sat`. The five invalid-reference/storage probes returned
`unsat`. The fixed witness reported cloned indices `[0, 2]`, first-slot-only
initialization after the first write, complete initialization after the second
write, rejected premature `assume_init`, return arrays `[0, 2]` and `[1, 2]`,
and equal final-state observations.

## Review findings

| Check | Decision |
|---|---|
| Authority and source binding | Accepted. Direct content comparisons bind the active catalog contract, retained contract, generated declaration, canonical Rust item and normalized public docs, implementation-proof harness, and all three manifests to the packaged inputs. |
| Boundary adequacy | Accepted. `Boundary_T` contains only initial receiver values, memory/provenance and mutable-borrow identity, layout/platform limits, and the outside-frame token. It excludes validity bits, outputs, final state, MaybeUninit results, alias maps, canonical answers, and traces. |
| Source-backed replacement | Accepted. The bounded model replaces `TS-052-D004` and `TS-052-E001` with explicit `usize` clone identity, in-bounds unchecked index resolution, ordered two-slot writes, prior-slot preservation, complete initialization, and delayed `assume_init`. The replacement is defined in SMT and verified independently in Verus without `external_body`. |
| Contract fidelity | Accepted. `Spec_T` is the generated final-length postcondition plus well-formed, disjoint receiver-reference invariants. It deliberately does not constrain returned references to the canonical source-selected indices and does not inject a final state. |
| Literal theorem and equivalence | Accepted. Both obligations use one shared valid input and one shared boundary, two independent output/state pairs, and exact equality for every modeled return field; the full obligation additionally compares every modeled final-state field. |
| Concrete incompleteness witness | Accepted. For the valid length-three non-ZST input with indices `[0, 2]`, both `[0, 2]` and `[1, 2]` are well-formed disjoint receiver-borrow arrays satisfying the active contract under the same boundary and exact same final state, while exact output and full exact equivalence both fail. |
| Negative probes | Accepted. Executed guards and solver probes reject output- or final-state-bearing boundaries, opaque validity, canonical-answer injection, out-of-bounds and overlapping returns, prior-slot mutation, partial initialization, and premature `assume_init`. |
| Scope and preservation | Accepted. The active manifest/catalog derivation remains 120 generated Slice contracts with exactly 62 selected UNKNOWN rows. Exactly 8 rows are classified and 54 remain `not-run`. Direct recursive byte comparisons found all seven previously accepted evidence trees unchanged by the standalone target-052 pipeline. |

