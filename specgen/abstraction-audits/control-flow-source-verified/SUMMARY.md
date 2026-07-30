# Determinism audit: control_flow.rs

- Targets: 10
- R0 results: `{'': 3, 'unsat': 7}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `Result::<T, E>::branch` | verus_error |  |  |
| `Option::<T>::branch` | verus_error |  |  |
| `Option::<T>::from_residual` | ok | unsat | complete |
| `ControlFlow::<B, C>::is_break` | ok | unsat | complete |
| `ControlFlow::<B, C>::is_continue` | ok | unsat | complete |
| `ControlFlow::<B, C>::break_value` | ok | unsat | complete |
| `ControlFlow::<B, C>::continue_value` | ok | unsat | complete |
| `ControlFlow::<B, C>::break_ok` | ok | unsat | complete |
| `ControlFlow::<B, C>::continue_ok` | ok | unsat | complete |
| `Result::<T, F>::from_residual` | verus_error |  |  |
