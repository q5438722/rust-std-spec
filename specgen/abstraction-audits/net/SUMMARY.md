# Determinism audit: net.rs

- Targets: 44
- R0 results: `{'unsat': 42, 'unknown': 2}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `Ipv4Addr::new` | ok | unsat | complete |
| `Ipv4Addr::from_octets` | ok | unsat | complete |
| `Ipv4Addr::octets` | ok | unsat | complete |
| `Ipv4Addr::is_unspecified` | ok | unsat | complete |
| `Ipv4Addr::is_loopback` | ok | unsat | complete |
| `Ipv4Addr::is_private` | ok | unsat | complete |
| `Ipv4Addr::is_link_local` | ok | unsat | complete |
| `Ipv4Addr::is_multicast` | ok | unsat | complete |
| `Ipv4Addr::is_broadcast` | ok | unsat | complete |
| `Ipv4Addr::is_documentation` | ok | unsat | complete |
| `Ipv4Addr::to_ipv6_compatible` | ok | unsat | complete |
| `Ipv4Addr::to_ipv6_mapped` | ok | unsat | complete |
| `Ipv6Addr::from_octets` | ok | unsat | complete |
| `Ipv6Addr::octets` | ok | unsat | complete |
| `Ipv6Addr::is_unspecified` | ok | unsat | complete |
| `Ipv6Addr::is_loopback` | ok | unsat | complete |
| `Ipv6Addr::is_multicast` | ok | unsat | complete |
| `Ipv6Addr::is_unique_local` | ok | unsat | complete |
| `Ipv6Addr::is_unicast_link_local` | ok | unsat | complete |
| `IpAddr::is_ipv4` | ok | unsat | complete |
| `IpAddr::is_ipv6` | ok | unsat | complete |
| `IpAddr::is_unspecified` | ok | unsat | complete |
| `IpAddr::is_loopback` | ok | unsat | complete |
| `IpAddr::is_multicast` | ok | unsat | complete |
| `SocketAddrV4::new` | ok | unsat | complete |
| `SocketAddrV4::ip` | ok | unknown | ok_inconclusive |
| `SocketAddrV4::set_ip` | ok | unsat | complete |
| `SocketAddrV4::port` | ok | unsat | complete |
| `SocketAddrV4::set_port` | ok | unsat | complete |
| `SocketAddrV6::new` | ok | unsat | complete |
| `SocketAddrV6::ip` | ok | unknown | ok_inconclusive |
| `SocketAddrV6::set_ip` | ok | unsat | complete |
| `SocketAddrV6::port` | ok | unsat | complete |
| `SocketAddrV6::set_port` | ok | unsat | complete |
| `SocketAddrV6::flowinfo` | ok | unsat | complete |
| `SocketAddrV6::set_flowinfo` | ok | unsat | complete |
| `SocketAddrV6::scope_id` | ok | unsat | complete |
| `SocketAddrV6::set_scope_id` | ok | unsat | complete |
| `SocketAddr::new` | ok | unsat | complete |
| `SocketAddr::is_ipv4` | ok | unsat | complete |
| `SocketAddr::is_ipv6` | ok | unsat | complete |
| `SocketAddr::ip` | ok | unsat | complete |
| `SocketAddr::port` | ok | unsat | complete |
| `SocketAddr::set_port` | ok | unsat | complete |
