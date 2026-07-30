# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 19
- Add-spec decisions: 2
- Skip decisions: 17
- Static skips: 0
- Raw determinism reward: 1
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::borrow::Cow::into_owned` | data_structure | add_spec | 0 | 0 | classification:associated_type_or_projection, determinism_not_proved:unknown |
| `core::option::Option::as_deref` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::pin::Pin::as_ref` | other | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::pin::Pin::set` | other | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::result::Result::as_deref` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::ends_with` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::get` | data_structure | add_spec | 1 | 0 | classification:associated_type_or_projection |
| `core::str::parse` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rfind` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rmatch_indices` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rmatches` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplit` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplit_once` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplit_terminator` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplitn` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::strip_circumfix` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::trim_end_matches` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::trim_matches` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
| `core::str::trim_right_matches` | data_structure | skip | 0 | 0 | classification:associated_type_or_projection |
