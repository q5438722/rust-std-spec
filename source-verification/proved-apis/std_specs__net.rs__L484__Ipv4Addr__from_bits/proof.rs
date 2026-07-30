#![allow(dead_code)]

use core::net::Ipv4Addr;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_ipv4_from_bits(bits: u32) -> (result: Ipv4Addr)
    ensures
        result@ == seq![
            (bits >> 24) as u8,
            ((bits >> 16) & 0xff) as u8,
            ((bits >> 8) & 0xff) as u8,
            (bits & 0xff) as u8,
        ],
{
    Ipv4Addr::from_octets([
        (bits >> 24) as u8,
        ((bits >> 16) & 0xff) as u8,
        ((bits >> 8) & 0xff) as u8,
        (bits & 0xff) as u8,
    ])
}

}

fn main() {}