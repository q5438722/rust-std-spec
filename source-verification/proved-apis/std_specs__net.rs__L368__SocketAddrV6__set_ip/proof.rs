#![allow(dead_code)]

use core::net::{Ipv6Addr, SocketAddrV6};
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_socket_addr_v6_set_ip(address: &mut SocketAddrV6, new_ip: Ipv6Addr)
    ensures
        final(address)@ == (SocketAddrV6View {
            ip: new_ip@,
            port: old(address)@.port,
            flowinfo: old(address)@.flowinfo,
            scope_id: old(address)@.scope_id,
        }),
{
    let port = address.port();
    let flowinfo = address.flowinfo();
    let scope_id = address.scope_id();
    *address = SocketAddrV6::new(new_ip, port, flowinfo, scope_id);
}

}

fn main() {}