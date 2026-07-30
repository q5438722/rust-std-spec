pub assume_specification[ SocketAddrV4::ip ](address: &SocketAddrV4) -> (result: &Ipv4Addr)
    ensures
        result@ == address@.ip,
;
