# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 21
- Add-spec decisions: 1
- Skip decisions: 20
- Static skips: 0
- Raw determinism reward: 0
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::collections::BTreeMap::first_entry` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::collections::BTreeMap::last_entry` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16_lossy` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16be` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16be_lossy` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16le` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16le_lossy` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf8` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf8_lossy` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::into_boxed_str` | data_structure | add_spec | 0 | 0 | classification:complex_result_or_pattern_model, determinism_not_proved:unknown |
| `core::option::Option::as_pin_ref` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::slice::sort_unstable` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::contains` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::find` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::split_once` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::starts_with` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::strip_prefix` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::strip_suffix` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::trim_left_matches` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::trim_start_matches` | data_structure | skip | 0 | 0 | classification:complex_result_or_pattern_model |
