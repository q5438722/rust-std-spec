pub assume_specification[ IpAddr::is_loopback ](address: &IpAddr) -> (result: bool)
    ensures
        result == ip_is_loopback(address@),
;
