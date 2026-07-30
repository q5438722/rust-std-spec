pub assume_specification[ SocketAddrV4::new ](ip: Ipv4Addr, port: u16) -> (result: SocketAddrV4)
    ensures
        result@ == (SocketAddrV4View { ip: ip@, port }),
;
