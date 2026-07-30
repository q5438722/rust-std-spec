pub assume_specification[ SocketAddrV6::ip ](address: &SocketAddrV6) -> (result: &Ipv6Addr)
    ensures
        result@ == address@.ip,
;
