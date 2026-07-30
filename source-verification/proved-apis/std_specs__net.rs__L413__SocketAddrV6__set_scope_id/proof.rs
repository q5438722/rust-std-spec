#![allow(dead_code)]

use core::net::SocketAddrV6;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_socket_addr_v6_set_scope_id(address: &mut SocketAddrV6, new_scope_id: u32)
    ensures
        final(address)@ == (SocketAddrV6View {
            ip: old(address)@.ip,
            port: old(address)@.port,
            flowinfo: old(address)@.flowinfo,
            scope_id: new_scope_id,
        }),
{
    let ip = *address.ip();
    let port = address.port();
    let flowinfo = address.flowinfo();
    *address = SocketAddrV6::new(ip, port, flowinfo, new_scope_id);
}

}

fn main() {}