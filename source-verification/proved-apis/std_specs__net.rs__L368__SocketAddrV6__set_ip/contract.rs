pub assume_specification[ SocketAddrV6::set_ip ](address: &mut SocketAddrV6, ip: Ipv6Addr)
    ensures
        final(address)@ == (SocketAddrV6View {
            ip: ip@,
            port: old(address)@.port,
            flowinfo: old(address)@.flowinfo,
            scope_id: old(address)@.scope_id,
        }),
;
