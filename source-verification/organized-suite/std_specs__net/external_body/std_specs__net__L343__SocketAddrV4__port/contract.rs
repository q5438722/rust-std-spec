pub assume_specification[ SocketAddrV4::port ](address: &SocketAddrV4) -> (result: u16)
    ensures
        result == address@.port,
;
