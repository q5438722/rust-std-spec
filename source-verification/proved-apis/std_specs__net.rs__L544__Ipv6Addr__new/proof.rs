#![allow(dead_code)]

use core::net::Ipv6Addr;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_ipv6_new(
    a: u16,
    b: u16,
    c: u16,
    d: u16,
    e: u16,
    f: u16,
    g: u16,
    h: u16,
) -> (result: Ipv6Addr)
    ensures
        result@ == seq![
            (a / 256) as u8,
            (a % 256) as u8,
            (b / 256) as u8,
            (b % 256) as u8,
            (c / 256) as u8,
            (c % 256) as u8,
            (d / 256) as u8,
            (d % 256) as u8,
            (e / 256) as u8,
            (e % 256) as u8,
            (f / 256) as u8,
            (f % 256) as u8,
            (g / 256) as u8,
            (g % 256) as u8,
            (h / 256) as u8,
            (h % 256) as u8,
        ],
{
    // Fuse `to_be` with the bytewise transmute, then use the public form of
    // the source's private `octets` field construction.
    let addr16 = [a, b, c, d, e, f, g, h];
    let octets = [
        (addr16[0] / 256) as u8,
        (addr16[0] % 256) as u8,
        (addr16[1] / 256) as u8,
        (addr16[1] % 256) as u8,
        (addr16[2] / 256) as u8,
        (addr16[2] % 256) as u8,
        (addr16[3] / 256) as u8,
        (addr16[3] % 256) as u8,
        (addr16[4] / 256) as u8,
        (addr16[4] % 256) as u8,
        (addr16[5] / 256) as u8,
        (addr16[5] % 256) as u8,
        (addr16[6] / 256) as u8,
        (addr16[6] % 256) as u8,
        (addr16[7] / 256) as u8,
        (addr16[7] % 256) as u8,
    ];
    Ipv6Addr::from_octets(octets)
}

}

fn main() {}