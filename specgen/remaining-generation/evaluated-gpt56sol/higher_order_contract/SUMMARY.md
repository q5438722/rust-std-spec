# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 71
- Add-spec decisions: 37
- Skip decisions: 34
- Static skips: 0
- Raw determinism reward: 17
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::collections::VecDeque::binary_search_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `alloc::collections::VecDeque::binary_search_by_key` | data_structure | add_spec | 0 | 0 | checker_status:verus_error, classification:higher_order_contract |
| `alloc::collections::VecDeque::partition_point` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `alloc::collections::VecDeque::pop_back_if` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown, structured_contract_mismatch |
| `alloc::collections::VecDeque::pop_front_if` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `alloc::collections::VecDeque::resize_with` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `alloc::collections::btree_map::Entry::and_modify` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::dedup_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::dedup_by_key` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::pop_if` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::resize_with` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::array::from_fn` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::array::map` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::LazyCell::force` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::LazyCell::new` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::OnceCell::get_or_init` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::filter_map` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::map` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::map_split` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefCell::replace_with` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::filter_map` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::map` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::map_split` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::cmp::Ordering::then_with` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown, structured_contract_mismatch |
| `core::cmp::max_by` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::cmp::max_by_key` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::cmp::min_by` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::cmp::min_by_key` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::future::poll_fn` | other | skip | 0 | 0 | classification:higher_order_contract |
| `core::ops::Bound::map` | other | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::ops::ControlFlow::map_break` | other | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `core::ops::ControlFlow::map_continue` | other | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `core::option::Option::filter` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::option::Option::inspect` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::option::Option::is_none_or` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::option::Option::is_some_and` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `core::option::Option::map_or` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::option::Option::map_or_default` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::option::Option::map_or_else` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::option::Option::or_else` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::option::Option::take_if` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `core::ptr::NonNull::map_addr` | memory_pointer | skip | 0 | 0 | classification:higher_order_contract |
| `core::result::Result::and_then` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `core::result::Result::inspect` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::inspect_err` | data_structure | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `core::result::Result::is_err_and` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `core::result::Result::is_ok_and` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `core::result::Result::map_or` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `core::result::Result::map_or_default` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::result::Result::map_or_else` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::result::Result::or_else` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::result::Result::unwrap_or_else` | data_structure | add_spec | 0 | 0 | classification:higher_order_contract, determinism_not_proved:unknown |
| `core::slice::binary_search_by` | data_structure | add_spec | 0 | 0 | checker_status:verus_error, classification:higher_order_contract |
| `core::slice::binary_search_by_key` | data_structure | add_spec | 0 | 0 | checker_status:verus_error, classification:higher_order_contract, structured_contract_mismatch |
| `core::slice::chunk_by` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::chunk_by_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::fill_with` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::is_sorted_by` | data_structure | add_spec | 0 | 0 | checker_status:verus_error, classification:higher_order_contract |
| `core::slice::is_sorted_by_key` | data_structure | add_spec | 0 | 0 | checker_status:verus_error, classification:higher_order_contract, structured_contract_mismatch |
| `core::slice::partition_point` | data_structure | add_spec | 1 | 0 | classification:higher_order_contract |
| `core::slice::rsplit` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplit_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplitn` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplitn_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::sort_unstable_by` | data_structure | add_spec | 0 | 0 | checker_status:verus_error, classification:higher_order_contract |
| `core::slice::sort_unstable_by_key` | data_structure | add_spec | 0 | 0 | checker_status:verus_error, classification:higher_order_contract |
| `core::slice::split_inclusive_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::split_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `core::slice::splitn_mut` | data_structure | skip | 0 | 0 | classification:higher_order_contract |
| `std::panic::catch_unwind` | other | skip | 0 | 0 | classification:higher_order_contract, determinism_unsupported_contract_form |
| `std::panic::take_hook` | other | skip | 0 | 0 | classification:higher_order_contract |
