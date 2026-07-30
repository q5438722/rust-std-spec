pub assume_specification[ Ipv4Addr::is_loopback ](address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_loopback(address@),
;
