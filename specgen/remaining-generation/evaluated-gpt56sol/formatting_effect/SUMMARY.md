# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 79
- Add-spec decisions: 2
- Skip decisions: 77
- Static skips: 0
- Raw determinism reward: 0
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::fmt::format` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Arguments::as_str` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugList::entries` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugList::entry` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugList::finish` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugList::finish_non_exhaustive` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::entries` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::entry` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::finish` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::finish_non_exhaustive` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::key` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::value` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::entries` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::entry` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::finish` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::finish_non_exhaustive` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugStruct::field` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugStruct::finish` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugStruct::finish_non_exhaustive` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugTuple::field` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugTuple::finish` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugTuple::finish_non_exhaustive` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::align` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::alternate` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_list` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_map` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_set` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_struct` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_tuple` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::fill` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::flags` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Formatter::pad` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::pad_integral` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::precision` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::sign_aware_zero_pad` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::sign_minus` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::sign_plus` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::width` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::write_fmt` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::write_str` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::NumBuffer::new` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::and` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::and_then` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_deref` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_deref_mut` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_mut` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_ref` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::cloned` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::copied` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::err` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::expect` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::expect_err` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::flatten` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::inspect` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::inspect_err` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::is_err` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::is_err_and` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::is_ok` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::is_ok_and` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::iter` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::iter_mut` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map_err` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map_or` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map_or_default` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map_or_else` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::ok` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::or` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::or_else` | formatting | add_spec | 0 | 0 | classification:formatting_effect, determinism_not_proved:unknown |
| `core::fmt::Result::transpose` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_err` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_err_unchecked` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_or` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_or_default` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_or_else` | formatting | add_spec | 0 | 0 | classification:formatting_effect, determinism_not_proved:unknown |
| `core::fmt::Result::unwrap_unchecked` | formatting | skip | 0 | 0 | classification:formatting_effect, determinism_unsupported_contract_form |
| `core::fmt::from_fn` | formatting | skip | 0 | 0 | classification:formatting_effect |
| `core::fmt::write` | formatting | skip | 0 | 0 | classification:formatting_effect |
