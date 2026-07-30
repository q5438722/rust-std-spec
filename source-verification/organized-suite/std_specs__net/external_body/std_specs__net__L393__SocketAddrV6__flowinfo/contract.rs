pub assume_specification[ SocketAddrV6::flowinfo ](address: &SocketAddrV6) -> (result: u32)
    ensures
        result == address@.flowinfo,
;
