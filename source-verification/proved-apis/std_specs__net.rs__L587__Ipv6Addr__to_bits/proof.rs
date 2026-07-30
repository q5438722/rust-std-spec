#![allow(dead_code)]

use core::net::Ipv6Addr;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_ipv6_to_bits(address: Ipv6Addr) -> (result: u128)
    ensures
        result as int == (address@[0] as int) * 0x100_0000_0000_0000_0000_0000_0000_0000
            + (address@[1] as int) * 0x1_0000_0000_0000_0000_0000_0000_0000
            + (address@[2] as int) * 0x100_0000_0000_0000_0000_0000_0000
            + (address@[3] as int) * 0x1_0000_0000_0000_0000_0000_0000
            + (address@[4] as int) * 0x100_0000_0000_0000_0000_0000
            + (address@[5] as int) * 0x1_0000_0000_0000_0000_0000
            + (address@[6] as int) * 0x100_0000_0000_0000_0000
            + (address@[7] as int) * 0x1_0000_0000_0000_0000
            + (address@[8] as int) * 0x100_0000_0000_0000
            + (address@[9] as int) * 0x1_0000_0000_0000
            + (address@[10] as int) * 0x100_0000_0000
            + (address@[11] as int) * 0x1_0000_0000
            + (address@[12] as int) * 0x100_0000
            + (address@[13] as int) * 0x1_0000
            + (address@[14] as int) * 0x100
            + address@[15] as int,
{
    let octets = address.octets();
    proof {
        assert(octets@ == address@);
    }
    let b0 = octets[0];
    let b1 = octets[1];
    let b2 = octets[2];
    let b3 = octets[3];
    let b4 = octets[4];
    let b5 = octets[5];
    let b6 = octets[6];
    let b7 = octets[7];
    let b8 = octets[8];
    let b9 = octets[9];
    let b10 = octets[10];
    let b11 = octets[11];
    let b12 = octets[12];
    let b13 = octets[13];
    let b14 = octets[14];
    let b15 = octets[15];
    (b0 as u128) * 0x100_0000_0000_0000_0000_0000_0000_0000u128
        + (b1 as u128) * 0x1_0000_0000_0000_0000_0000_0000_0000u128
        + (b2 as u128) * 0x100_0000_0000_0000_0000_0000_0000u128
        + (b3 as u128) * 0x1_0000_0000_0000_0000_0000_0000u128
        + (b4 as u128) * 0x100_0000_0000_0000_0000_0000u128
        + (b5 as u128) * 0x1_0000_0000_0000_0000_0000u128
        + (b6 as u128) * 0x100_0000_0000_0000_0000u128
        + (b7 as u128) * 0x1_0000_0000_0000_0000u128
        + (b8 as u128) * 0x100_0000_0000_0000u128
        + (b9 as u128) * 0x1_0000_0000_0000u128
        + (b10 as u128) * 0x100_0000_0000u128
        + (b11 as u128) * 0x1_0000_0000u128
        + (b12 as u128) * 0x100_0000u128
        + (b13 as u128) * 0x1_0000u128
        + (b14 as u128) * 0x100u128
        + b15 as u128
}

}

fn main() {}