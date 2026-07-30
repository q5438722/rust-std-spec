# Determinism-feedback comparison

Both columns use the same **2,121 targets**. `With feedback` means using spec determinism as feedback.

## Pure determinism-feedback status table

| Status | No feedback | With feedback | Delta |
|---|---:|---:|---:|
| `complete` | 150 | 225 | +75 |
| `unknown` | 68 | 40 | -28 |
| `trivial_equality` | 19 | 3 | -16 |
| `incomplete (sat reported by Z3)` | 0 | 0 | +0 |
| `no_spec` | 1884 | 1853 | -31 |

## Completeness summary

| Metric | No feedback | With feedback |
|---|---:|---:|
| Add-spec proposals | 462 (21.78%) | 280 (13.20%) |
| Checker-valid contracts | 237 (11.17%) | 268 (12.64%) |
| Complete contracts | 150 (7.07%) | 225 (10.61%) |
| Not complete / no spec | 1971 (92.93%) | 1896 (89.39%) |
| Complete among checker-valid | 150/237 (63.29%) | 225/268 (83.96%) |

## Raw saved-final transitions

The transition table below shows the literal saved final decisions
before moving the 66 suitability-filtered complete contracts back into
the pure determinism `complete` count.

| No-feedback status | With-feedback status | Targets |
|---|---|---:|
| `skip_no_spec` | `skip_no_spec` | 1658 |
| `typecheck_or_checker_failure` | `skip_no_spec` | 133 |
| `complete` | `complete` | 84 |
| `complete` | `skip_no_spec` | 66 |
| `typecheck_or_checker_failure` | `complete` | 50 |
| `unknown` | `skip_no_spec` | 33 |
| `typecheck_or_checker_failure` | `unknown` | 30 |
| `unknown` | `complete` | 24 |
| `trivial_equality` | `skip_no_spec` | 17 |
| `typecheck_or_checker_failure` | `typecheck_or_checker_failure` | 11 |
| `unknown` | `unknown` | 10 |
| `trivial_equality` | `trivial_equality` | 2 |
| `skip_no_spec` | `complete` | 1 |
| `unknown` | `typecheck_or_checker_failure` | 1 |
| `typecheck_or_checker_failure` | `trivial_equality` | 1 |

### Why the no-spec count increased

- Newly changed to skip: **249**.
- Previously skipped but recovered: **1**.
- Net increase: **248**.

| Round-0 status of newly skipped target | Count |
|---|---:|
| `typecheck_or_checker_failure` | 133 |
| `complete` | 66 |
| `unknown` | 33 |
| `trivial_equality` | 17 |

## Source-proof status for saved final contracts

Proof campaign state: `complete`.

| Proof status | No feedback | With feedback |
|---|---:|---:|
| `known_mismatch_or_inadmissible` | 36 | 24 |
| `no_valid_spec` | 1884 | 1919 |
| `not_proved` | 112 | 79 |
| `strict_faithful_admissible` | 89 | 99 |

### Provability summary

| Metric | No feedback | With feedback |
|---|---:|---:|
| Checker-valid contracts attempted | 237 | 202 |
| Verus pass before fidelity rejection | 125 | 123 |
| Strict-faithful admissible proofs | **89** | **99** |
| Strict proof rate among checker-valid | 89/237 (37.55%) | 99/202 (49.01%) |
| Strict proof rate among complete contracts | 64/150 (42.67%) | 79/159 (49.69%) |

## Completeness crossed with proof status

| Feedback phase | Completeness group | Proof status | Targets |
|---|---|---|---:|
| `no_feedback` | `complete` | `known_mismatch_or_inadmissible` | 28 |
| `no_feedback` | `complete` | `not_proved` | 58 |
| `no_feedback` | `complete` | `strict_faithful_admissible` | 64 |
| `no_feedback` | `checker_valid_noncomplete` | `known_mismatch_or_inadmissible` | 8 |
| `no_feedback` | `checker_valid_noncomplete` | `not_proved` | 54 |
| `no_feedback` | `checker_valid_noncomplete` | `strict_faithful_admissible` | 25 |
| `no_feedback` | `invalid_or_no_spec` | `no_valid_spec` | 1884 |
| `with_feedback` | `complete` | `known_mismatch_or_inadmissible` | 12 |
| `with_feedback` | `complete` | `not_proved` | 68 |
| `with_feedback` | `complete` | `strict_faithful_admissible` | 79 |
| `with_feedback` | `checker_valid_noncomplete` | `known_mismatch_or_inadmissible` | 12 |
| `with_feedback` | `checker_valid_noncomplete` | `not_proved` | 11 |
| `with_feedback` | `checker_valid_noncomplete` | `strict_faithful_admissible` | 20 |
| `with_feedback` | `invalid_or_no_spec` | `no_valid_spec` | 1919 |

## Why no specification was produced

| Reason | Meaning | No feedback | With feedback | With-feedback share |
|---|---|---:|---:|---:|
| `runtime_or_hidden_state` | Result depends on OS/runtime/process state not exposed by a stable pure view. | 463 | 456 | 24.61% |
| `needs_new_vstd_abstraction` | Required semantic vocabulary or owner/module model is absent from vstd. | 360 | 346 | 18.67% |
| `trait_contract_integration` | Requires editing or composing an external trait specification. | 201 | 201 | 10.85% |
| `concurrency_or_hidden_state` | Atomic/concurrent state is not represented by an ordinary deterministic view. | 175 | 179 | 9.66% |
| `unsafe_or_representation_sensitive` | Raw pointer, provenance, unsafe, or representation-sensitive behavior. | 134 | 150 | 8.09% |
| `determinism_checker_unsupported` | Current checker cannot encode the exact output or mutable post-state. | 110 | 124 | 6.69% |
| `iterator_or_adapter_result` | Iterator/guard/adapter result needs a prophetic or state-transition model. | 101 | 101 | 5.45% |
| `toolchain_unavailable` | API is unavailable in the Verus Rust 1.96 toolchain. | 70 | 70 | 3.78% |
| `formatting_effect` | Formatting state and emitted effects are not modeled. | 68 | 67 | 3.62% |
| `representation_or_allocator` | Allocator or private representation state is absent from the public view. | 36 | 40 | 2.16% |
| `higher_order_contract` | Closure/callback semantics require call-ensures or a higher-order model. | 64 | 39 | 2.10% |
| `ownership_or_uninitialized_model` | Linear ownership, initialization, or MaybeUninit state is not modeled. | 22 | 25 | 1.35% |
| `complex_result_or_pattern_model` | Result discriminant/pattern semantics need an additional model. | 20 | 20 | 1.08% |
| `associated_type_or_projection` | Associated-type/projection signature requires manual integration. | 16 | 17 | 0.92% |
| `no_modeled_observable_output` | No return value or mutable output is represented by the checker. | 9 | 9 | 0.49% |
| `needs_borrowed_key_or_ordering_model` | Borrow<Q> functionality or cross-type ordering is missing. | 0 | 4 | 0.22% |
| `needs_pointer_identity_or_provenance_model` | Semantic views erase location, identity, address, or provenance. | 30 | 3 | 0.16% |
| `needs_functional_trait_semantics` | Clone/Default is only relational and does not uniquely determine output. | 5 | 2 | 0.11% |

Detailed paired rows are in `records.csv`; machine-readable totals
and the full transition matrix are in `summary.json`.
