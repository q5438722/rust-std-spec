pub assume_specification[ Ipv4Addr::is_private ](address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_private(address@),
;
