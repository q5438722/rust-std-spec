pub assume_specification[ Ipv6Addr::is_multicast ](address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_multicast(address@),
;
