pub assume_specification[ Ipv4Addr::is_multicast ](address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_multicast(address@),
;
