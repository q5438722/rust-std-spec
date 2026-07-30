#![allow(dead_code)]

use core::net::Ipv4Addr;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_ipv4_addr_new(a: u8, b: u8, c: u8, d: u8) -> (result: Ipv4Addr)
    ensures
        result@ == seq![a, b, c, d],
{
    Ipv4Addr::from_octets([a, b, c, d])
}

}

fn main() {}