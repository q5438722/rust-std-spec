pub assume_specification[ SocketAddr::new ](ip: IpAddr, port: u16) -> (result: SocketAddr)
    ensures
        result@ == match ip@ {
            IpAddrView::V4(bytes) => SocketAddrView::V4(SocketAddrV4View { ip: bytes, port }),
            IpAddrView::V6(bytes) => SocketAddrView::V6(
                SocketAddrV6View { ip: bytes, port, flowinfo: 0, scope_id: 0 },
            ),
        },
;
