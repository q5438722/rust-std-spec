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
pub fn external_std_specs__net_rs__l484__ipv4addr__from_bits(bits: u32) -> (result: Ipv4Addr)
    ensures
        result@ == seq![
            (bits >> 24) as u8,
            ((bits >> 16) & 0xff) as u8,
            ((bits >> 8) & 0xff) as u8,
            (bits & 0xff) as u8,
        ],
    { loop { } }

}

fn main() {}
