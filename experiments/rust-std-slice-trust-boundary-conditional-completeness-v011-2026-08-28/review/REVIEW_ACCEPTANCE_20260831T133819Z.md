# Independent Reviewer decision: target 022

**VERDICT: ACCEPT**

This acceptance covers only input order 22,
`core::slice::as_ptr_range`. It preserves the accepted decisions for targets
013, 029, 081, and 106 and does not authorize a Manager stage transition.

## Fresh verification

The Reviewer ran:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py
```

All 15 commands completed successfully. Python compilation completed with
status zero and no diagnostics, 123 tests ran and reported `OK`, all five
target pipelines passed, and local validation reported `validation=PASS`.

The Reviewer also replayed both target obligations directly with Z3. The full
exact-equivalence and exact-output theorem negations each returned clean
`unsat`. All eight retained domain probes returned their expected results:
five valid allocated or dangling cases were `sat`, while null-address and
nonzero-offset-without-allocation/provenance cases were `unsat`.

An independent in-memory probe matrix used fresh values derived from the Rust
source and pointer-add safety text. It confirmed `sat` for a dangling empty
non-ZST slice, a nonempty non-ZST slice ending exactly one past its allocation,
and a dangling nonempty ZST slice. It confirmed `unsat` for a null data
pointer, misalignment, address wrap, a wrong end address, changed end
provenance, and mutated final state.

Direct Verus type-checking succeeded, and direct verification reported
`2 verified, 0 errors`. The experiment-local source-transition model contains
no `external_body`.

## Review findings

| Check | Decision |
|---|---|
| Authority and source binding | Accepted. Direct content comparisons bind the active generated declaration, public docs, Rust source item, retained harness and manifests, and target-local pointer-add source and safety documentation to their designated frozen or canonical inputs. |
| Contract interpretation | Accepted. `TargetDefinition_T` expands both active pointer-range conjuncts through explicit slice-to-thin-pointer and pointer-add definitions. It contains no uninterpreted whole-target or pointer-add relation. |
| Pointer semantics | Accepted. The start pointer retains the input allocation, address, and provenance. The end address is exactly `start + len * element_size`; allocation and provenance are retained; isize fit and mathematical no-wrap are required; and nonzero offsets additionally require an allocation-backed in-bounds range permitting the one-past endpoint. |
| Zero-byte domain | Accepted. Empty non-ZST and nonempty ZST slices require a non-null aligned pointer but may use dangling pointers without allocation provenance. Nonzero byte offsets require positive allocation/provenance and valid allocation bounds. |
| Boundary adequacy | Accepted. The shared boundary contains only pre-existing input allocation, address, provenance, pointee layout, and platform-limit observations. The synthetic start-pointer helper and both answer-bearing range-end sites are excluded rather than relabeled. No returned endpoint, range, final state, target truth, answer encoding, or trace is present. |
| Literal theorem and equivalence | Accepted. Both executions share the exact `x` and `b`; `Spec_T` forwards to the explicit target definition; exact-output equality covers every start/end allocation, address, and provenance field; and full equivalence additionally covers every modeled final-state field. |
| Negative guards | Accepted. Executed tests reject null-provenance synthesis, address-equals-length substitution, endpoint-bearing boundaries, changed provenance, wrong byte offsets, omitted no-wrap or allocation constraints, opaque pointer-add relations, omitted endpoint equality, mutations of all four accepted result rows, and mutation of an unclassified row. |
| Scope and preservation | Accepted. CSV and JSON agree on the 62 selected rows. Only targets 013, 022, 029, 081, and 106 are classified, target 022 has both result fields `conditional-complete`, and exactly 57 rows remain `not-run`. Direct before/after comparisons found every file in the four previously accepted evidence trees unchanged, and the crosswalk remained unchanged across the final acceptance run. |

