pub assume_specification[ Ipv6Addr::is_loopback ](address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_loopback(address@),
;
