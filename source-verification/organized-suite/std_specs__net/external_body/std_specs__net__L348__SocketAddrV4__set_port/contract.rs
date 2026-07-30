pub assume_specification[ SocketAddrV4::set_port ](address: &mut SocketAddrV4, port: u16)
    ensures
        final(address)@ == (SocketAddrV4View { ip: old(address)@.ip, port }),
;
