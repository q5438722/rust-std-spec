pub assume_specification[ SocketAddrV4::set_ip ](address: &mut SocketAddrV4, ip: Ipv4Addr)
    ensures
        final(address)@ == (SocketAddrV4View { ip: ip@, port: old(address)@.port }),
;
