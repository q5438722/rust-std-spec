# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 33
- Add-spec decisions: 8
- Skip decisions: 25
- Static skips: 0
- Raw determinism reward: 1
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::boxed::Box::into_pin` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::boxed::Box::new_uninit_slice` | data_structure | add_spec | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_not_proved:unknown |
| `alloc::boxed::Box::new_zeroed` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::boxed::Box::new_zeroed_slice` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::boxed::Box::pin` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::boxed::Box::write` | data_structure | add_spec | 1 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::downcast` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::downgrade` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_cyclic` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_uninit` | data_structure | add_spec | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_not_proved:unknown |
| `alloc::rc::Rc::new_uninit_slice` | data_structure | add_spec | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_not_proved:unknown |
| `alloc::rc::Rc::new_zeroed` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_zeroed_slice` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::pin` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::ptr_eq` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::strong_count` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::unwrap_or_clone` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::rc::Rc::weak_count` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::downcast` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::downgrade` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::into_inner` | data_structure | add_spec | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_not_proved:unknown |
| `alloc::sync::Arc::new_cyclic` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::new_uninit` | data_structure | add_spec | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_not_proved:unknown |
| `alloc::sync::Arc::new_uninit_slice` | data_structure | add_spec | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_not_proved:unknown |
| `alloc::sync::Arc::new_zeroed` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::new_zeroed_slice` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::pin` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::ptr_eq` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::strong_count` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::try_unwrap` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_unsupported_contract_form |
| `alloc::sync::Arc::unwrap_or_clone` | data_structure | add_spec | 0 | 0 | classification:ownership_or_uninitialized_model, determinism_not_proved:unknown |
| `alloc::sync::Arc::weak_count` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
| `core::mem::MaybeUninit::zeroed` | data_structure | skip | 0 | 0 | classification:ownership_or_uninitialized_model |
