pub assume_specification[ SocketAddrV6::set_flowinfo ](address: &mut SocketAddrV6, flowinfo: u32)
    ensures
        final(address)@ == (SocketAddrV6View {
            ip: old(address)@.ip,
            port: old(address)@.port,
            flowinfo,
            scope_id: old(address)@.scope_id,
        }),
;
