# Determinism audit: location.rs

- Targets: 4
- R0 results: `{'unsat': 4}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `Location::file` | ok | unsat | complete |
| `Location::file_as_c_str` | ok | unsat | complete |
| `Location::line` | ok | unsat | complete |
| `Location::column` | ok | unsat | complete |
