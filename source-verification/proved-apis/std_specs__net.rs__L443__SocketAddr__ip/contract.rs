pub assume_specification[ SocketAddr::ip ](address: &SocketAddr) -> (result: IpAddr)
    ensures
        result@ == match address@ {
            SocketAddrView::V4(v4) => IpAddrView::V4(v4.ip),
            SocketAddrView::V6(v6) => IpAddrView::V6(v6.ip),
        },
;
