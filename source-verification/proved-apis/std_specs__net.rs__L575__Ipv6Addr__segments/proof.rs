#![allow(dead_code)]

use core::net::Ipv6Addr;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

proof fn lemma_join_ipv6_segment(hi: u8, lo: u8)
    ensures
        ((((hi as u16) << 8) | (lo as u16)) as int)
            == (hi as int) * 256 + lo as int,
{
    let hi16 = hi as u16;
    let lo16 = lo as u16;
    assert(hi16 < 256);
    assert(lo16 < 256);
    assert(
        hi16 < 256 && lo16 < 256 ==>
            ((hi16 << 8) | lo16) == hi16 * 256 + lo16
    ) by (bit_vector);
}

fn source_ipv6_segments(address: &Ipv6Addr) -> (result: [u16; 8])
    ensures
        (result@[0] as int) == (address@[0] as int) * 256 + address@[1] as int,
        (result@[1] as int) == (address@[2] as int) * 256 + address@[3] as int,
        (result@[2] as int) == (address@[4] as int) * 256 + address@[5] as int,
        (result@[3] as int) == (address@[6] as int) * 256 + address@[7] as int,
        (result@[4] as int) == (address@[8] as int) * 256 + address@[9] as int,
        (result@[5] as int) == (address@[10] as int) * 256 + address@[11] as int,
        (result@[6] as int) == (address@[12] as int) * 256 + address@[13] as int,
        (result@[7] as int) == (address@[14] as int) * 256 + address@[15] as int,
{
    let octets = address.octets();

    // This fuses the transmute followed by `u16::from_be` into its
    // endian-independent operation: decode each adjacent big-endian byte pair.
    let a = ((octets[0] as u16) << 8) | (octets[1] as u16);
    let b = ((octets[2] as u16) << 8) | (octets[3] as u16);
    let c = ((octets[4] as u16) << 8) | (octets[5] as u16);
    let d = ((octets[6] as u16) << 8) | (octets[7] as u16);
    let e = ((octets[8] as u16) << 8) | (octets[9] as u16);
    let f = ((octets[10] as u16) << 8) | (octets[11] as u16);
    let g = ((octets[12] as u16) << 8) | (octets[13] as u16);
    let h = ((octets[14] as u16) << 8) | (octets[15] as u16);

    proof {
        lemma_join_ipv6_segment(octets[0], octets[1]);
        lemma_join_ipv6_segment(octets[2], octets[3]);
        lemma_join_ipv6_segment(octets[4], octets[5]);
        lemma_join_ipv6_segment(octets[6], octets[7]);
        lemma_join_ipv6_segment(octets[8], octets[9]);
        lemma_join_ipv6_segment(octets[10], octets[11]);
        lemma_join_ipv6_segment(octets[12], octets[13]);
        lemma_join_ipv6_segment(octets[14], octets[15]);
    }

    [a, b, c, d, e, f, g, h]
}

}

fn main() {}