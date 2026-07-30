# Determinism audit: ordering.rs

- Targets: 8
- R0 results: `{'unsat': 8}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `Ordering::is_eq` | ok | unsat | complete |
| `Ordering::is_ne` | ok | unsat | complete |
| `Ordering::is_lt` | ok | unsat | complete |
| `Ordering::is_gt` | ok | unsat | complete |
| `Ordering::is_le` | ok | unsat | complete |
| `Ordering::is_ge` | ok | unsat | complete |
| `Ordering::reverse` | ok | unsat | complete |
| `Ordering::then` | ok | unsat | complete |
