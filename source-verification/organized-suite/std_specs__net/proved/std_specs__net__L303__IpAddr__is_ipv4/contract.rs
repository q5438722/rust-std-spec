pub assume_specification[ IpAddr::is_ipv4 ](address: &IpAddr) -> (result: bool)
    ensures
        result <==> address@ is V4,
;
