# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 179
- Add-spec decisions: 0
- Skip decisions: 179
- Static skips: 0
- Raw determinism reward: 0
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `core::sync::atomic::Atomic::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::compare_exchange` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::Atomic::compare_exchange_weak` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_add` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_and` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_byte_add` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_byte_sub` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_max` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_min` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_nand` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_not` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_or` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_ptr_add` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_ptr_sub` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_sub` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_xor` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::load` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::new` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::store` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, no_modeled_observable_output |
| `core::sync::atomic::Atomic::swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicBool::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::fetch_not` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::compare_exchange` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::compare_exchange_weak` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_and` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_byte_add` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_byte_sub` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_or` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_ptr_add` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_ptr_sub` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_xor` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::load` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::new` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::store` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, no_modeled_observable_output |
| `core::sync::atomic::AtomicPtr::swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::as_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::compare_and_swap` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::fetch_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::from_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::from_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::from_ptr` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::get_mut` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::get_mut_slice` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::into_inner` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::try_update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::update` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::compiler_fence` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, no_modeled_observable_output |
| `core::sync::atomic::fence` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, no_modeled_observable_output |
| `core::sync::atomic::spin_loop_hint` | atomic | skip | 0 | 0 | classification:concurrency_or_hidden_state, no_modeled_observable_output |
