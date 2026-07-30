#![allow(dead_code)]

use core::net::Ipv4Addr;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_ipv4_to_bits(address: Ipv4Addr) -> (result: u32)
    ensures
        result == (((address@[0] as u32) << 24)
            | ((address@[1] as u32) << 16)
            | ((address@[2] as u32) << 8)
            | (address@[3] as u32)),
{
    let octets = address.octets();
    proof {
        assert(octets@ == address@);
    }
    ((octets[0] as u32) << 24)
        | ((octets[1] as u32) << 16)
        | ((octets[2] as u32) << 8)
        | (octets[3] as u32)
}

}

fn main() {}