pub assume_specification[ SocketAddr::set_ip ](address: &mut SocketAddr, new_ip: IpAddr)
    ensures
        final(address)@ == match (old(address)@, new_ip@) {
            (SocketAddrView::V4(old_v4), IpAddrView::V4(ip)) => SocketAddrView::V4(
                SocketAddrV4View { ip, port: old_v4.port },
            ),
            (SocketAddrView::V4(old_v4), IpAddrView::V6(ip)) => SocketAddrView::V6(
                SocketAddrV6View { ip, port: old_v4.port, flowinfo: 0, scope_id: 0 },
            ),
            (SocketAddrView::V6(old_v6), IpAddrView::V4(ip)) => SocketAddrView::V4(
                SocketAddrV4View { ip, port: old_v6.port },
            ),
            (SocketAddrView::V6(old_v6), IpAddrView::V6(ip)) => SocketAddrView::V6(
                SocketAddrV6View {
                    ip,
                    port: old_v6.port,
                    flowinfo: old_v6.flowinfo,
                    scope_id: old_v6.scope_id,
                },
            ),
        },
;
