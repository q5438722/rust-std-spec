pub assume_specification[ IpAddr::is_ipv6 ](address: &IpAddr) -> (result: bool)
    ensures
        result <==> address@ is V6,
;
