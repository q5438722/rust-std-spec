#![allow(dead_code)]

use core::net::Ipv6Addr;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_ipv6_from_bits(bits: u128) -> (result: Ipv6Addr)
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
{
    Ipv6Addr::from_octets([
        ((bits >> 120) & 0xffu128) as u8,
        ((bits >> 112) & 0xffu128) as u8,
        ((bits >> 104) & 0xffu128) as u8,
        ((bits >> 96) & 0xffu128) as u8,
        ((bits >> 88) & 0xffu128) as u8,
        ((bits >> 80) & 0xffu128) as u8,
        ((bits >> 72) & 0xffu128) as u8,
        ((bits >> 64) & 0xffu128) as u8,
        ((bits >> 56) & 0xffu128) as u8,
        ((bits >> 48) & 0xffu128) as u8,
        ((bits >> 40) & 0xffu128) as u8,
        ((bits >> 32) & 0xffu128) as u8,
        ((bits >> 24) & 0xffu128) as u8,
        ((bits >> 16) & 0xffu128) as u8,
        ((bits >> 8) & 0xffu128) as u8,
        (bits & 0xffu128) as u8,
    ])
}

}

fn main() {}