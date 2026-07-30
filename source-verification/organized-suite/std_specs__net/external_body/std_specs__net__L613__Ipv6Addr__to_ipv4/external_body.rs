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
pub fn external_std_specs__net_rs__l613__ipv6addr__to_ipv4(address: &Ipv6Addr) -> (result: Option<Ipv4Addr>)
    ensures
        (result is Some) <==> (address@.subrange(0, 12) == Seq::new(12, |i: int| 0u8)
            || address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8]),
        result is Some ==> result->Some_0@ == address@.subrange(12, 16),
    { loop { } }

}

fn main() {}
