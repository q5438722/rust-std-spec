pub assume_specification[ IpAddr::is_multicast ](address: &IpAddr) -> (result: bool)
    ensures
        result == ip_is_multicast(address@),
;
