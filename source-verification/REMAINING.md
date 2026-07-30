# Why 117 newly specified stable APIs lack source verification

- Newly covered stable APIs: **211**
- Source-verified intersection: **94**
- Remaining: **117**

| Blocker | Count | Explanation |
|---|---:|---|
| `collection_private_internals` | 28 | Private Vec/node/ring-buffer fields, unsafe pointer algorithms, or guard/reference semantics are hidden by the public collection View. |
| `network_leaf_representation` | 27 | Leaf address structs keep octets/ports private; constructors, accessors, endian conversions, and setters are the trusted roots beneath the verified enum dispatch. |
| `allocator_capacity_state` | 25 | Capacity and reserve behavior depends on RawVec/allocator state; success and final capacity are intentionally not uniquely determined by abstract contents. |
| `ffi_private_buffers_and_errors` | 22 | Raw slices, ownership transfer, NUL/UTF-8 scans, and private error payloads require memory/provenance and representation models not available to a downstream proof. |
| `layout_root_primitives` | 6 | These are the trusted roots for private Alignment and compiler size/align intrinsics; derived Layout methods were verified from them. |
| `duration_root_representation` | 5 | The private secs/Nanoseconds fields are the trusted representation roots beneath the verified Duration arithmetic and conversion methods. |
| `compiler_location_state` | 4 | Location fields and the trailing-NUL filename allocation are compiler-created private state, including raw-pointer reconstruction in file_as_c_str. |

## collection_private_internals (28)

- `alloc::collections::BinaryHeap::append`
- `alloc::collections::BinaryHeap::as_slice`
- `alloc::collections::BinaryHeap::clear`
- `alloc::collections::BinaryHeap::into_sorted_vec`
- `alloc::collections::BinaryHeap::into_vec`
- `alloc::collections::BinaryHeap::len`
- `alloc::collections::BinaryHeap::new`
- `alloc::collections::BinaryHeap::peek`
- `alloc::collections::BinaryHeap::pop`
- `alloc::collections::BinaryHeap::push`
- `alloc::collections::LinkedList::append`
- `alloc::collections::LinkedList::back`
- `alloc::collections::LinkedList::clear`
- `alloc::collections::LinkedList::contains`
- `alloc::collections::LinkedList::front`
- `alloc::collections::LinkedList::len`
- `alloc::collections::LinkedList::new`
- `alloc::collections::LinkedList::pop_back`
- `alloc::collections::LinkedList::pop_front`
- `alloc::collections::LinkedList::push_back`
- `alloc::collections::LinkedList::push_front`
- `alloc::collections::LinkedList::split_off`
- `alloc::collections::VecDeque::as_slices`
- `alloc::collections::VecDeque::contains`
- `alloc::collections::VecDeque::get`
- `alloc::collections::VecDeque::rotate_left`
- `alloc::collections::VecDeque::rotate_right`
- `alloc::collections::VecDeque::swap`

## network_leaf_representation (27)

- `core::net::Ipv4Addr::from_bits`
- `core::net::Ipv4Addr::from_octets`
- `core::net::Ipv4Addr::new`
- `core::net::Ipv4Addr::octets`
- `core::net::Ipv4Addr::to_bits`
- `core::net::Ipv6Addr::from_bits`
- `core::net::Ipv6Addr::from_octets`
- `core::net::Ipv6Addr::from_segments`
- `core::net::Ipv6Addr::new`
- `core::net::Ipv6Addr::octets`
- `core::net::Ipv6Addr::segments`
- `core::net::Ipv6Addr::to_bits`
- `core::net::Ipv6Addr::to_ipv4`
- `core::net::SocketAddrV4::ip`
- `core::net::SocketAddrV4::new`
- `core::net::SocketAddrV4::port`
- `core::net::SocketAddrV4::set_ip`
- `core::net::SocketAddrV4::set_port`
- `core::net::SocketAddrV6::flowinfo`
- `core::net::SocketAddrV6::ip`
- `core::net::SocketAddrV6::new`
- `core::net::SocketAddrV6::port`
- `core::net::SocketAddrV6::scope_id`
- `core::net::SocketAddrV6::set_flowinfo`
- `core::net::SocketAddrV6::set_ip`
- `core::net::SocketAddrV6::set_port`
- `core::net::SocketAddrV6::set_scope_id`

## allocator_capacity_state (25)

- `alloc::collections::BinaryHeap::capacity`
- `alloc::collections::BinaryHeap::reserve`
- `alloc::collections::BinaryHeap::reserve_exact`
- `alloc::collections::BinaryHeap::shrink_to`
- `alloc::collections::BinaryHeap::shrink_to_fit`
- `alloc::collections::BinaryHeap::try_reserve`
- `alloc::collections::BinaryHeap::try_reserve_exact`
- `alloc::collections::VecDeque::capacity`
- `alloc::collections::VecDeque::reserve_exact`
- `alloc::collections::VecDeque::shrink_to`
- `alloc::collections::VecDeque::shrink_to_fit`
- `alloc::collections::VecDeque::try_reserve`
- `alloc::collections::VecDeque::try_reserve_exact`
- `alloc::string::String::capacity`
- `alloc::string::String::reserve`
- `alloc::string::String::reserve_exact`
- `alloc::string::String::shrink_to`
- `alloc::string::String::shrink_to_fit`
- `alloc::string::String::try_reserve`
- `alloc::string::String::try_reserve_exact`
- `alloc::vec::Vec::capacity`
- `alloc::vec::Vec::reserve_exact`
- `alloc::vec::Vec::shrink_to`
- `alloc::vec::Vec::shrink_to_fit`
- `alloc::vec::Vec::try_reserve_exact`

## ffi_private_buffers_and_errors (22)

- `alloc::ffi::CString::as_c_str`
- `alloc::ffi::CString::from_vec_with_nul`
- `alloc::ffi::CString::into_boxed_c_str`
- `alloc::ffi::CString::into_bytes`
- `alloc::ffi::CString::into_bytes_with_nul`
- `alloc::ffi::CString::into_string`
- `alloc::ffi::FromVecWithNulError::as_bytes`
- `alloc::ffi::FromVecWithNulError::into_bytes`
- `alloc::ffi::IntoStringError::into_cstring`
- `alloc::ffi::IntoStringError::utf8_error`
- `alloc::ffi::NulError::into_vec`
- `alloc::ffi::NulError::nul_position`
- `alloc::string::FromUtf8Error::as_bytes`
- `alloc::string::FromUtf8Error::into_bytes`
- `alloc::string::FromUtf8Error::utf8_error`
- `core::ffi::CStr::from_bytes_until_nul`
- `core::ffi::CStr::from_bytes_with_nul`
- `core::ffi::CStr::to_bytes`
- `core::ffi::CStr::to_bytes_with_nul`
- `core::ffi::CStr::to_str`
- `core::str::Utf8Error::error_len`
- `core::str::Utf8Error::valid_up_to`

## layout_root_primitives (6)

- `core::alloc::Layout::align`
- `core::alloc::Layout::for_value`
- `core::alloc::Layout::from_size_align`
- `core::alloc::Layout::from_size_align_unchecked`
- `core::alloc::Layout::new`
- `core::alloc::Layout::size`

## duration_root_representation (5)

- `core::time::Duration::as_secs`
- `core::time::Duration::new`
- `core::time::Duration::subsec_micros`
- `core::time::Duration::subsec_millis`
- `core::time::Duration::subsec_nanos`

## compiler_location_state (4)

- `core::panic::Location::column`
- `core::panic::Location::file`
- `core::panic::Location::file_as_c_str`
- `core::panic::Location::line`
