# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 101
- Add-spec decisions: 0
- Skip decisions: 101
- Static skips: 0
- Raw determinism reward: 0
- Guarded reward: 0
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::collections::BTreeMap::entry` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::extract_if` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::into_keys` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::into_values` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::range` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::range_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::values_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::difference` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::extract_if` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::intersection` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::range` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::symmetric_difference` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::union` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BinaryHeap::drain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BinaryHeap::iter` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BinaryHeap::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::extract_if` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::iter` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::drain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::range` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::range_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::retain_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::string::String::drain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::string::String::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::drain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::extract_if` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::retain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::retain_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::splice` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::next_if` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::next_if_eq` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::next_if_map` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::next_if_map_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::peek` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::chain` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::empty` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::from_fn` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::once` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result, determinism_unsupported_contract_form |
| `core::iter::once_with` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::repeat` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::repeat_n` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::repeat_with` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::successors` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::zip` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::option::Option::iter` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::option::Option::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::result::Result::iter` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::result::Result::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::array_windows` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::chunks` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::chunks_exact` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::chunks_exact_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::chunks_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::escape_ascii` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::iter_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks_exact` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks_exact_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks_mut` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::split` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::split_inclusive` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::splitn` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::utf8_chunks` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::windows` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::bytes` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::char_indices` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::encode_utf16` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::escape_debug` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::escape_default` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::escape_unicode` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::lines` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::lines_any` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::match_indices` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::matches` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_ascii_whitespace` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_inclusive` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_terminator` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_whitespace` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::splitn` | data_structure | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::drain` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::extract_if` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::into_keys` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::into_values` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::iter_mut` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::retain` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::values_mut` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::difference` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::drain` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::extract_if` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::intersection` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::retain` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::symmetric_difference` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::union` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
| `std::path::Path::iter` | other | skip | 0 | 0 | classification:iterator_or_adapter_result |
