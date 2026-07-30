pub assume_specification[ SocketAddrV6::scope_id ](address: &SocketAddrV6) -> (result: u32)
    ensures
        result == address@.scope_id,
;
