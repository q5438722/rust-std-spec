# Determinism audit: duration.rs

- Targets: 36
- R0 results: `{'unsat': 34, 'unknown': 2}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `Duration::new` | ok | unsat | complete |
| `Duration::from_secs` | ok | unsat | complete |
| `Duration::from_millis` | ok | unsat | complete |
| `Duration::from_micros` | ok | unsat | complete |
| `Duration::from_nanos` | ok | unsat | complete |
| `Duration::from_nanos_u128` | ok | unsat | complete |
| `Duration::from_hours` | ok | unsat | complete |
| `Duration::from_mins` | ok | unsat | complete |
| `Duration::is_zero` | ok | unsat | complete |
| `Duration::as_secs` | ok | unsat | complete |
| `Duration::as_secs_f32` | ok | unsat | complete |
| `Duration::as_secs_f64` | ok | unsat | complete |
| `Duration::subsec_millis` | ok | unsat | complete |
| `Duration::subsec_micros` | ok | unsat | complete |
| `Duration::subsec_nanos` | ok | unsat | complete |
| `Duration::as_millis` | ok | unsat | complete |
| `Duration::as_micros` | ok | unsat | complete |
| `Duration::as_nanos` | ok | unsat | complete |
| `Duration::abs_diff` | ok | unsat | complete |
| `Duration::checked_add` | ok | unsat | complete |
| `Duration::saturating_add` | ok | unsat | complete |
| `Duration::checked_sub` | ok | unsat | complete |
| `Duration::saturating_sub` | ok | unsat | complete |
| `Duration::checked_mul` | ok | unsat | complete |
| `Duration::saturating_mul` | ok | unsat | complete |
| `Duration::checked_div` | ok | unsat | complete |
| `Duration::mul_f64` | ok | unsat | complete |
| `Duration::mul_f32` | ok | unsat | complete |
| `Duration::div_f64` | ok | unsat | complete |
| `Duration::div_f32` | ok | unsat | complete |
| `Duration::from_secs_f32` | ok | unsat | complete |
| `Duration::from_secs_f64` | ok | unsat | complete |
| `Duration::try_from_secs_f32` | ok | unsat | complete |
| `Duration::try_from_secs_f64` | ok | unsat | complete |
| `Duration::div_duration_f32` | ok | unknown | ok_inconclusive |
| `Duration::div_duration_f64` | ok | unknown | ok_inconclusive |
