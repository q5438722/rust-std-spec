pub assume_specification[ Ipv6Addr::is_unicast_link_local ](address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_unicast_link_local(address@),
;
