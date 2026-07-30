# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 59
- Add-spec decisions: 5
- Skip decisions: 54
- Static skips: 0
- Raw determinism reward: 2
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::collections::BinaryHeap::capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::reserve` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::shrink_to` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::shrink_to_fit` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::try_reserve` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::try_reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::with_capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::VecDeque::capacity` | data_structure | add_spec | 0 | 0 | classification:representation_or_allocator, determinism_not_proved:unknown |
| `alloc::collections::VecDeque::reserve_exact` | data_structure | add_spec | 1 | 0 | classification:representation_or_allocator |
| `alloc::collections::VecDeque::shrink_to` | data_structure | add_spec | 0 | 0 | classification:representation_or_allocator, contract_typecheck_failed |
| `alloc::collections::VecDeque::shrink_to_fit` | data_structure | add_spec | 1 | 0 | classification:representation_or_allocator |
| `alloc::collections::VecDeque::try_reserve` | data_structure | add_spec | 0 | 0 | classification:representation_or_allocator, determinism_not_proved:unknown |
| `alloc::collections::VecDeque::try_reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::string::String::capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::string::String::reserve` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::string::String::reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `alloc::string::String::shrink_to` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `alloc::string::String::shrink_to_fit` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `alloc::string::String::try_reserve` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::string::String::try_reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator |
| `alloc::string::String::with_capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `alloc::vec::Vec::capacity` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `alloc::vec::Vec::reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `alloc::vec::Vec::shrink_to` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `alloc::vec::Vec::shrink_to_fit` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `alloc::vec::Vec::try_reserve_exact` | data_structure | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `core::alloc::Layout::dangling_ptr` | memory_pointer | skip | 0 | 0 | classification:representation_or_allocator |
| `core::ptr::fn_addr_eq` | memory_pointer | skip | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashMap::capacity` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashMap::hasher` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashMap::shrink_to` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashMap::shrink_to_fit` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashMap::try_reserve` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashMap::with_capacity_and_hasher` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashMap::with_hasher` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashSet::capacity` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashSet::hasher` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashSet::shrink_to` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashSet::shrink_to_fit` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashSet::try_reserve` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashSet::with_capacity_and_hasher` | other | skip | 0 | 0 | classification:representation_or_allocator, determinism_unsupported_contract_form |
| `std::collections::HashSet::with_hasher` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::capacity` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::reserve` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::reserve_exact` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::shrink_to` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::shrink_to_fit` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::try_reserve` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::try_reserve_exact` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::with_capacity` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::capacity` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::reserve` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::reserve_exact` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::shrink_to` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::shrink_to_fit` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::try_reserve` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::try_reserve_exact` | other | skip | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::with_capacity` | other | skip | 0 | 0 | classification:representation_or_allocator |
