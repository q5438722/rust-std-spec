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
pub fn external_std_specs__net_rs__l500__ipv6addr__from_bits(bits: u128) -> (result: Ipv6Addr)
    ensures
        result@ == seq![
            (((bits >> 120) & 0xffu128) as u8),
            (((bits >> 112) & 0xffu128) as u8),
            (((bits >> 104) & 0xffu128) as u8),
            (((bits >> 96) & 0xffu128) as u8),
            (((bits >> 88) & 0xffu128) as u8),
            (((bits >> 80) & 0xffu128) as u8),
            (((bits >> 72) & 0xffu128) as u8),
            (((bits >> 64) & 0xffu128) as u8),
            (((bits >> 56) & 0xffu128) as u8),
            (((bits >> 48) & 0xffu128) as u8),
            (((bits >> 40) & 0xffu128) as u8),
            (((bits >> 32) & 0xffu128) as u8),
            (((bits >> 24) & 0xffu128) as u8),
            (((bits >> 16) & 0xffu128) as u8),
            (((bits >> 8) & 0xffu128) as u8),
            ((bits & 0xffu128) as u8),
        ],
    { loop { } }

}

fn main() {}
