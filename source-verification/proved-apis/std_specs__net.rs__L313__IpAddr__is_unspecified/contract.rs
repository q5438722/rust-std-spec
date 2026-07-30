pub assume_specification[ IpAddr::is_unspecified ](address: &IpAddr) -> (result: bool)
    ensures
        result == ip_is_unspecified(address@),
;
