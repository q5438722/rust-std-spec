#![allow(dead_code)]

use core::net::SocketAddrV6;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_socket_addr_v6_set_flowinfo(address: &mut SocketAddrV6, new_flowinfo: u32)
    ensures
        final(address)@ == (SocketAddrV6View {
            ip: old(address)@.ip,
            port: old(address)@.port,
            flowinfo: new_flowinfo,
            scope_id: old(address)@.scope_id,
        }),
{
    let ip = *address.ip();
    let port = address.port();
    let scope_id = address.scope_id();
    *address = SocketAddrV6::new(ip, port, new_flowinfo, scope_id);
}

}

fn main() {}