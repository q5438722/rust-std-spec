pub assume_specification[ SocketAddr::is_ipv6 ](address: &SocketAddr) -> (result: bool)
    ensures
        result <==> address@ is V6,
;
