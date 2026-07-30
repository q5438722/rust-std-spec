pub assume_specification[ SocketAddrV6::set_port ](address: &mut SocketAddrV6, port: u16)
    ensures
        final(address)@ == (SocketAddrV6View {
            ip: old(address)@.ip,
            port,
            flowinfo: old(address)@.flowinfo,
            scope_id: old(address)@.scope_id,
        }),
;
