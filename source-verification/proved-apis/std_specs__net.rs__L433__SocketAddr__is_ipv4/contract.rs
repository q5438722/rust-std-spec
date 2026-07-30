pub assume_specification[ SocketAddr::is_ipv4 ](address: &SocketAddr) -> (result: bool)
    ensures
        result <==> address@ is V4,
;
