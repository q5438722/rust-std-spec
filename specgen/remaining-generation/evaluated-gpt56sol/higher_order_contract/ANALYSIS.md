# Rust std contract generation with determinism feedback

## Aggregate result

| Metric | Count |
|---|---:|
| `targets` | 71 |
| `initial_add_spec` | 44 |
| `initial_skip` | 27 |
| `final_add_spec` | 37 |
| `final_skip` | 34 |
| `typecheck_passed` | 37 |
| `det_unsat` | 17 |
| `det_sat` | 0 |
| `det_unknown` | 13 |
| `raw_reward` | 17 |
| `guarded_reward` | 0 |
| `semantic_guarded_reward` | 0 |
| `llm_errors` | 0 |
| `static_skips` | 0 |

External `assume_specification` declarations are trusted. A guarded determinism reward means only that the candidate typechecked, avoided the configured vacuity gates, and uniquely determined the modeled outputs. It does not prove the contract sound.

## Feedback transitions

| Transition | Count |
|---|---:|
| `add_spec->add_spec` | 37 |
| `add_spec->skip` | 7 |
| `skip->skip` | 27 |

## Frequent issues

| Issue | Count |
|---|---:|
| `classification:higher_order_contract` | 71 |
| `determinism_not_proved:unknown` | 13 |
| `checker_status:verus_error` | 7 |
| `structured_contract_mismatch` | 4 |
| `determinism_unsupported_contract_form` | 3 |

## Guarded-deterministic candidates

| Target | Ensures |
|---|---|

## Semantic-gated candidates

0 of 0 guarded-deterministic candidates pass the pilot-derived semantic postprocessing gates.

| Target | Ensures |
|---|---|

## Per-target result

| Target | Initial | Final | Typecheck | R0 | Guarded | Semantic | Issues |
|---|---|---|---:|---|---:|---:|---|
| `alloc::collections::VecDeque::binary_search_by` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::collections::VecDeque::binary_search_by_key` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract |
| `alloc::collections::VecDeque::partition_point` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `alloc::collections::VecDeque::pop_back_if` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown;structured_contract_mismatch |
| `alloc::collections::VecDeque::pop_front_if` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `alloc::collections::VecDeque::resize_with` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::collections::btree_map::Entry::and_modify` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::dedup_by` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::dedup_by_key` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::pop_if` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::resize_with` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::array::from_fn` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::array::map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::LazyCell::force` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::LazyCell::new` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::OnceCell::get_or_init` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::filter_map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::map_split` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefCell::replace_with` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::filter_map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::map_split` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cmp::Ordering::then_with` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown;structured_contract_mismatch |
| `core::cmp::max_by` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::cmp::max_by_key` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::cmp::min_by` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::cmp::min_by_key` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::future::poll_fn` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::ops::Bound::map` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::ops::ControlFlow::map_break` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::ops::ControlFlow::map_continue` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::option::Option::filter` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::inspect` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::is_none_or` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::is_some_and` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::option::Option::map_or` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::map_or_default` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::map_or_else` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::or_else` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::take_if` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::ptr::NonNull::map_addr` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::result::Result::and_then` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::result::Result::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::inspect_err` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::is_err_and` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::result::Result::is_ok_and` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::result::Result::map_or` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::result::Result::map_or_default` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::result::Result::map_or_else` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::result::Result::or_else` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::result::Result::unwrap_or_else` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::slice::chunk_by` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::chunk_by_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::fill_with` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::is_sorted_by` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract |
| `core::slice::partition_point` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplit` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplit_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplitn` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplitn_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::sort_unstable_by` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract |
| `core::slice::sort_unstable_by_key` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract |
| `core::slice::split_inclusive_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::split_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::splitn_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `std::panic::catch_unwind` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `std::panic::take_hook` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::binary_search_by` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract;borrowed_key_uniqueness_precondition |
| `core::slice::binary_search_by_key` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract;structured_contract_mismatch |
| `core::slice::is_sorted_by_key` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract;structured_contract_mismatch |
