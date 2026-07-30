# Determinism audit: control_flow.rs

- Targets: 10
- R0 results: `{'': 4, 'unsat': 6}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `Result::<T, E>::branch` | verus_error |  |  |
| `Option::<T>::branch` | verus_error |  |  |
| `Option::<T>::from_residual` | verus_error |  |  |
| `ControlFlow::<B, C>::is_break` | ok | unsat | complete |
| `ControlFlow::<B, C>::is_continue` | ok | unsat | complete |
| `ControlFlow::<B, C>::break_value` | ok | unsat | complete |
| `ControlFlow::<B, C>::continue_value` | ok | unsat | complete |
| `ControlFlow::<B, C>::break_ok` | ok | unsat | complete |
| `ControlFlow::<B, C>::continue_ok` | ok | unsat | complete |
| `Result::<T, F>::from_residual` | verus_error |  |  |
