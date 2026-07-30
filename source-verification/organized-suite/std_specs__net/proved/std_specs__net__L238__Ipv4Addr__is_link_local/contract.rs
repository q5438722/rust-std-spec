pub assume_specification[ Ipv4Addr::is_link_local ](address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_link_local(address@),
;
