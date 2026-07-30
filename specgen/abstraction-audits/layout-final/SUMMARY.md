# Determinism audit: layout_value.rs

- Targets: 9
- R0 results: `{'unsat': 9}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `Layout::from_size_align` | ok | unsat | complete |
| `Layout::from_size_align_unchecked` | ok | unsat | complete |
| `Layout::size` | ok | unsat | complete |
| `Layout::align` | ok | unsat | complete |
| `Layout::new::<T>` | ok | unsat | complete |
| `Layout::for_value::<T>` | ok | unsat | complete |
| `Layout::align_to` | ok | unsat | complete |
| `Layout::pad_to_align` | ok | unsat | complete |
| `Layout::array::<T>` | ok | unsat | complete |
