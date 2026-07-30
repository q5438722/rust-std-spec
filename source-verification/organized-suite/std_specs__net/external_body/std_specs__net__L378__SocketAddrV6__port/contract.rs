pub assume_specification[ SocketAddrV6::port ](address: &SocketAddrV6) -> (result: u16)
    ensures
        result == address@.port,
;
