# Independent Reviewer findings: pointer-cast cluster

**VERDICT: CHANGES REQUIRED**

This review covers input orders 019 `core::slice::as_mut_ptr`, 021
`core::slice::as_ptr`, and 020 `core::slice::as_mut_ptr_range`. It does not
authorize a Manager stage transition.

## Fresh verification

The Reviewer ran the complete acceptance driver, the local validator, all six
theorem files directly through Z3, the complete target-local probe matrix, and
direct Verus type-checking and verification:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_authority_design.py
z3 -smt2 evidence/targets/<target>/obligation.smt2
z3 -smt2 evidence/targets/<target>/exact_output_obligation.smt2
../../verus/source/target-verus/release/verus proofs/<target>.rs \
  --crate-type=lib --no-verify
../../verus/source/target-verus/release/verus proofs/<target>.rs \
  --crate-type=lib
```

The complete acceptance sequence passed all 21 commands. Python compilation
passed, 177 tests ran and reported `OK`, the local validator reported
`validation=PASS`, and the crosswalk ended with 11 classified and 51
`not-run` rows. All six theorem replays returned exact clean `unsat`. The
independent probe matrix returned the expected five SAT domain cases per
target and 6, 5, and 13 UNSAT guards for targets 019, 021, and 020
respectively. Each Verus model reported `2 verified, 0 errors` and contains no
`external_body`. Direct recursive content comparison found all eight
previously certified evidence trees unchanged.

## Blocking findings

### 1. Excluded synthetic sites still back target-019 and target-021 boundary fields

`tools/pointer_cast_cluster.py` declares `TS-019-D001` and `TS-021-D001` as
excluded retained sites, but also assigns those same IDs to
`boundary_backing_trust_sites`. Consequently every `boundary_fields` entry in
both obligation metadata files names the excluded synthetic site as its trust
backing, while `boundary_scope.admitted_trust_site_ids` is empty.

This conflicts with the mission requirement to replace rather than relabel the
synthetic sites. The SMT transition itself is source-shaped, but its boundary
provenance remains attributed to the rejected helper. The existing guard does
not catch the conflict: it requires nonempty `trust_site_ids`, while the
target-local test checks only that the boundary manifest's admitted and
excluded sets are disjoint.

Repair the metadata model so each initial memory/provenance/layout observation
is backed by an explicitly source-backed replacement identity rather than an
excluded retained site. Add a fail-closed check that boundary-field backing
cannot intersect excluded retained sites and is covered by the declared
admitted/source-backed set, then regenerate all three evidence trees.

### 2. The requested ordered target replay is not self-contained from the delivered state

Running `python3 tools/run_target_019.py` directly from the delivered final
crosswalk fails because already-classified targets 020 and 021 are treated as
out-of-scope results. Running the authority builder first also does not make
the chain runnable: the builder resets the eight certified predecessor rows
to `not-run`, so target 019 then rejects its expected preserved baseline.

The full acceptance driver passes because it reconstructs all eight
predecessor pipelines before running 019, 021, and 020. Provide a documented,
self-contained ordered cluster runner or make the three runners idempotent
against the delivered state so the separately requested 019 -> 021 -> 020
replay and local validator pass without manually editing result rows.

