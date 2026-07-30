pub assume_specification[ SocketAddr::port ](address: &SocketAddr) -> (result: u16)
    ensures
        result == match address@ {
            SocketAddrView::V4(v4) => v4.port,
            SocketAddrView::V6(v6) => v6.port,
        },
;
