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
pub fn external_std_specs__net_rs__l587__ipv6addr__to_bits(address: Ipv6Addr) -> (result: u128)
    ensures
        result as int == (address@[0] as int) * 0x100_0000_0000_0000_0000_0000_0000_0000 + (
        address@[1] as int) * 0x1_0000_0000_0000_0000_0000_0000_0000 + (address@[2] as int)
            * 0x100_0000_0000_0000_0000_0000_0000 + (address@[3] as int)
            * 0x1_0000_0000_0000_0000_0000_0000 + (address@[4] as int)
            * 0x100_0000_0000_0000_0000_0000 + (address@[5] as int) * 0x1_0000_0000_0000_0000_0000
            + (address@[6] as int) * 0x100_0000_0000_0000_0000 + (address@[7] as int)
            * 0x1_0000_0000_0000_0000 + (address@[8] as int) * 0x100_0000_0000_0000 + (
        address@[9] as int) * 0x1_0000_0000_0000 + (address@[10] as int) * 0x100_0000_0000 + (
        address@[11] as int) * 0x1_0000_0000 + (address@[12] as int) * 0x100_0000 + (
        address@[13] as int) * 0x1_0000 + (address@[14] as int) * 0x100 + address@[15] as int,
    { loop { } }

}

fn main() {}
