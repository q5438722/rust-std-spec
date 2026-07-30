# Determinism/completeness summary

## Direct contract records

| Category | Count |
|---|---:|
| `complete` | 382 |
| `unknown` | 120 |
| `checker_unsupported` | 17 |
| `no_local_postcondition` | 16 |
| `trivial_equality` | 4 |

## Unique API paths

| Category | Count |
|---|---:|
| `complete_all_records` | 339 |
| `unknown` | 77 |
| `checker_unsupported` | 17 |
| `unclassified_or_error` | 6 |
| `no_local_postcondition` | 3 |
| `mixed_partial` | 3 |
| `trivial_only` | 2 |

## Strict-faithful admissible local-surrogate subset

| Record category | Count |
|---|---:|
| `complete` | 125 |
| `unknown` | 20 |
| `no_local_postcondition` | 14 |
| `checker_unsupported` | 5 |
| `trivial_equality` | 4 |

| Unique API category | Count |
|---|---:|
| `complete_all_records` | 98 |
| `unknown` | 13 |
| `no_local_postcondition` | 9 |
| `checker_unsupported` | 5 |
| `mixed_partial` | 2 |
| `trivial_only` | 2 |

No contract produced `R0 = sat`; there is no SMT-confirmed incomplete
contract in this run. `unknown` remains inconclusive rather than complete.
