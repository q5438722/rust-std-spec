#![allow(dead_code)]

use core::net::{IpAddr, SocketAddr};
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_socket_addr_set_ip(address: &mut SocketAddr, new_ip: IpAddr)
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
{
    match (address, new_ip) {
        (SocketAddr::V4(a), IpAddr::V4(new_ip)) => a.set_ip(new_ip),
        (SocketAddr::V6(a), IpAddr::V6(new_ip)) => a.set_ip(new_ip),
        (self_, new_ip) => *self_ = SocketAddr::new(new_ip, self_.port()),
    }
}

} // verus!

fn main() {}