pub assume_specification[ Ipv4Addr::is_broadcast ](address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_broadcast(address@),
;
