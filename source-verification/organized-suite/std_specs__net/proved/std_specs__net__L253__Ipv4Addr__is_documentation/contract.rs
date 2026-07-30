pub assume_specification[ Ipv4Addr::is_documentation ](address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_documentation(address@),
;
