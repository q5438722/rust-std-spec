pub assume_specification[ SocketAddrV6::set_scope_id ](address: &mut SocketAddrV6, scope_id: u32)
    ensures
        final(address)@ == (SocketAddrV6View {
            ip: old(address)@.ip,
            port: old(address)@.port,
            flowinfo: old(address)@.flowinfo,
            scope_id,
        }),
;
