pub assume_specification[ Ipv4Addr::is_unspecified ](address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_unspecified(address@),
;
