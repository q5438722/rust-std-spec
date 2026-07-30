pub assume_specification[ SocketAddrV6::new ](
    ip: Ipv6Addr,
    port: u16,
    flowinfo: u32,
    scope_id: u32,
) -> (result: SocketAddrV6)
    ensures
        result@ == (SocketAddrV6View { ip: ip@, port, flowinfo, scope_id }),
;
