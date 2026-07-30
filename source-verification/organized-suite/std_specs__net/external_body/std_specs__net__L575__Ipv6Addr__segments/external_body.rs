#![allow(dead_code, unused_imports, unused_variables)]
#![feature(allocator_api)]
#![feature(box_into_inner)]
#![feature(const_trait_impl)]
#![feature(exact_size_is_empty)]
#![feature(iter_advance_by)]
#![feature(layout_for_ptr)]
#![feature(maybe_uninit_as_bytes)]
#![feature(maybe_uninit_array_assume_init)]
#![feature(never_type)]
#![feature(nonzero_internals)]
#![feature(ptr_metadata)]
#![feature(slice_ptr_get)]
#![feature(sized_hierarchy)]
#![feature(step_trait)]
#![feature(trusted_len)]
#![feature(unsized_fn_params)]
extern crate alloc;
use vstd::prelude::*;
use vstd::prelude::*;
use core::net::{IpAddr, Ipv4Addr, Ipv6Addr, SocketAddr, SocketAddrV4, SocketAddrV6};
use vstd::std_specs::net::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__net_rs__l575__ipv6addr__segments(address: &Ipv6Addr) -> (result: [u16; 8])
    ensures
        (result@[0] as int) == (address@[0] as int) * 256 + address@[1] as int,
        (result@[1] as int) == (address@[2] as int) * 256 + address@[3] as int,
        (result@[2] as int) == (address@[4] as int) * 256 + address@[5] as int,
        (result@[3] as int) == (address@[6] as int) * 256 + address@[7] as int,
        (result@[4] as int) == (address@[8] as int) * 256 + address@[9] as int,
        (result@[5] as int) == (address@[10] as int) * 256 + address@[11] as int,
        (result@[6] as int) == (address@[12] as int) * 256 + address@[13] as int,
        (result@[7] as int) == (address@[14] as int) * 256 + address@[15] as int,
    { loop { } }

}

fn main() {}
