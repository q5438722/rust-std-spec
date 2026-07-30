# Rust std missing-contract generation with determinism feedback

- Model: `gpt-5.6-sol`
- Targets: 27
- Add-spec decisions: 18
- Skip decisions: 9
- Static skips: 0
- Raw determinism reward: 18
- Guarded reward: 18
- LLM errors: 0
- Soundness: external contracts remain unverified; no candidate is automatically eligible for upstream application.

| Target | Category | Decision | Raw | Guarded | Issues |
|---|---|---|---:|---:|---|
| `alloc::collections::BinaryHeap::peek_mut` | data_structure | skip | 0 | 0 |  |
| `alloc::collections::LinkedList::contains` | data_structure | add_spec | 1 | 1 |  |
| `alloc::ffi::CString::new` | other | skip | 0 | 0 |  |
| `core::net::IpAddr::to_canonical` | other | add_spec | 1 | 1 |  |
| `core::net::Ipv4Addr::from_bits` | other | add_spec | 1 | 1 |  |
| `core::net::Ipv4Addr::to_bits` | other | add_spec | 1 | 1 |  |
| `core::net::Ipv6Addr::from_bits` | other | add_spec | 1 | 1 |  |
| `core::net::Ipv6Addr::from_segments` | other | add_spec | 1 | 1 |  |
| `core::net::Ipv6Addr::new` | other | add_spec | 1 | 1 |  |
| `core::net::Ipv6Addr::segments` | other | add_spec | 1 | 1 |  |
| `core::net::Ipv6Addr::to_bits` | other | add_spec | 1 | 1 |  |
| `core::net::Ipv6Addr::to_canonical` | other | add_spec | 1 | 1 |  |
| `core::net::Ipv6Addr::to_ipv4` | other | add_spec | 1 | 1 |  |
| `core::net::Ipv6Addr::to_ipv4_mapped` | other | add_spec | 1 | 1 |  |
| `core::net::SocketAddr::set_ip` | other | add_spec | 1 | 1 |  |
| `core::time::Duration::as_secs_f32` | other | add_spec | 1 | 1 |  |
| `core::time::Duration::as_secs_f64` | other | add_spec | 1 | 1 |  |
| `core::time::Duration::div_duration_f32` | other | skip | 0 | 0 |  |
| `core::time::Duration::div_duration_f64` | other | skip | 0 | 0 |  |
| `core::time::Duration::div_f32` | other | skip | 0 | 0 |  |
| `core::time::Duration::div_f64` | other | skip | 0 | 0 |  |
| `core::time::Duration::from_secs_f32` | other | add_spec | 1 | 1 |  |
| `core::time::Duration::from_secs_f64` | other | add_spec | 1 | 1 |  |
| `core::time::Duration::mul_f32` | other | skip | 0 | 0 |  |
| `core::time::Duration::mul_f64` | other | add_spec | 1 | 1 |  |
| `core::time::Duration::try_from_secs_f32` | other | skip | 0 | 0 |  |
| `core::time::Duration::try_from_secs_f64` | other | skip | 0 | 0 | determinism_unsupported_contract_form |
