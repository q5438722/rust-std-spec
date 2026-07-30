pub assume_specification[ Ipv6Addr::is_unique_local ](address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_unique_local(address@),
;
