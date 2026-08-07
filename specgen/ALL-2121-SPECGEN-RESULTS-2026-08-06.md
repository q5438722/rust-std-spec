# Fresh Rust std exec-spec generation results for all 2,121 APIs

## 1. Scope

This report publishes the fresh source-backed rerun of all 2,121 executable
Rust `core`/`alloc`/`std` API targets used by Nanvix.

The canonical tracked aggregate artifact tree is:

```text
specgen/all-2121-gpt56sol-fresh-20260806-0453/
```

Raw per-target generation directories are reproducible and intentionally
excluded by the repository-wide `**/targets/` ignore rule.

Configuration:

- model: `gpt-5.6-sol`;
- feedback rounds: 2;
- Verus: `0.2026.07.21.1beb0fa.dirty`;
- Rust toolchain: `1.96.0`;
- contract form: Verus `assume_specification`;
- trusted external contracts are source-fidelity audited but are not proofs of
  the Rust standard-library implementation.

## 2. Final result

| Metric | Count |
|---|---:|
| Manifest targets | 2,121 |
| Result rows | 2,121 |
| Final candidate rows | 2,121 |
| Missing / extra / duplicate targets | 0 / 0 / 0 |
| Final `add_spec` decisions | **127** |
| Accepted semantic candidates | **127** |
| Final `skip` decisions | **1,994** |
| Empty skip rationales | 0 |
| Unclassified / unjustified skips | 0 / 0 |

The accepted set is:

```text
accepted_semantic_candidates.csv
accepted_semantic_candidates.json
```

It contains 114 data-structure contracts, 12 other pure/core contracts, and
one I/O/runtime contract.

## 3. Acceptance gates

Every accepted row satisfies:

```text
final_decision == add_spec
typecheck_passed == true
guarded_reward == 1
semantic_guarded_reward == 1
issues == ""
semantic_gate_issues == ""
semantic_review_issues == ""
```

For the 47 accepted contracts with non-empty `requires`, all 47 preconditions
are classified `source_justified`. All 127 accepted `ensures` clauses have
source-context evidence and are classified `source_justified`.

Additional audits cover all 127 accepted contracts:

- target owner/name/module binding: zero missing, multiple, parse-failed, or
  mismatched rows;
- ordered input arity, reference/mutability shape, and output shape: zero
  mismatches;
- type/const generics, trait bounds, and `where` predicates: zero mismatches;
- contract text safety: no empty ensures, literal `true`/`false` ensures,
  `requires false`, arbitrary values, or standalone assumptions.

## 4. Skip taxonomy

All 1,994 skip rows have a non-empty source-backed rationale and a classified
taxonomy. The largest groups are:

| Taxonomy | Count |
|---|---:|
| Runtime or hidden state | 599 |
| Unsafe or representation-sensitive | 267 |
| Duplicate existing vstd specification | 226 |
| Higher-order behavior unmodeled | 210 |
| Needs a new vstd abstraction | 155 |
| Trait-contract integration gap | 146 |
| Determinism-unsupported contract form | 85 |
| Formatting effect unmodeled | 68 |
| Iterator or adapter result gap | 65 |

The 226 duplicate-vstd rows are retained as inventory skips rather than
generating duplicate trusted contracts.

## 5. Prior-versus-fresh delta

The fresh run is compared by target name and final decision against the prior
tracked `specgen/all-2121-gpt56sol/` tree.

| Delta | Count |
|---|---:|
| Changed final decisions | 147 |
| Prior `add_spec` → fresh `skip` | 117 |
| Prior `skip` → fresh `add_spec` | 30 |

The semantic taxonomy audit classifies every changed row, with zero
unclassified or unjustified upgrades/downgrades.

The fresh result is intentionally more conservative: determinism alone is not
enough for acceptance; source fidelity, semantic usefulness, abstraction
support, target binding, and signature/generic compatibility must also pass.

## 6. Representative accepted recoveries

Representative source-backed contracts include:

- `core::slice::reverse`: exact final sequence reversal;
- `core::slice::binary_search`: sorted, unique-match deterministic
  `Ok`/`Err` partition contract;
- `alloc::string::String::replace_range`: one-snapshot `RangeBounds`
  normalization with UTF-8 character-boundary checks;
- `alloc::collections::LinkedList::back_mut`: mutable tail lookup modeled by
  dereferenced values and list view, not pointer identity;
- `core::array::each_mut`: per-index array-of-mutable-reference semantics,
  avoiding pointer/provenance claims;
- `core::str::from_utf8`: valid-byte decoding and `Ok`/`Err` branch behavior.

## 7. Verification artifacts

Primary files:

```text
batch_summary.json
recheck_summary.json
analysis.json
ANALYSIS.md
SUMMARY.md
final_candidates.csv
accepted_semantic_candidates.csv
accepted_semantic_candidates.json
final_verification.json
```

Additional tracked artifacts include:

```text
accepted_*_audit.{csv,json}
final_candidate_payload_consistency_audit.{csv,json}
final_skip_rationale_audit.csv
final_skip_rationale_audit_summary.json
FINAL_SKIP_RATIONALE_AUDIT.md
prior_fresh_delta/
```

`final_verification.json` is the machine-readable acceptance authority for the
published snapshot.
