pub assume_specification[ Ipv6Addr::is_unspecified ](address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_unspecified(address@),
;
