# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 9
- Add-spec decisions: 0
- Skip decisions: 9
- Static skips: 0
- Raw determinism reward: 0
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `core::cell::Cell::set` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::cell::Cell::swap` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::cell::Cell::update` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::cell::RefCell::swap` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::hint::cold_path` | other | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::hint::spin_loop` | other | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::mem::drop` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `core::mem::forget` | data_structure | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
| `std::panic::set_hook` | other | skip | 0 | 0 | classification:no_modeled_observable_output, no_modeled_observable_output |
