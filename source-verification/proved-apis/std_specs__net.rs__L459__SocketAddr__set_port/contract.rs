pub assume_specification[ SocketAddr::set_port ](address: &mut SocketAddr, port: u16)
    ensures
        final(address)@ == match old(address)@ {
            SocketAddrView::V4(v4) => SocketAddrView::V4(SocketAddrV4View { ip: v4.ip, port }),
            SocketAddrView::V6(v6) => SocketAddrView::V6(
                SocketAddrV6View { ip: v6.ip, port, flowinfo: v6.flowinfo, scope_id: v6.scope_id },
            ),
        },
;
