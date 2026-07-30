#![allow(dead_code)]

use core::net::Ipv6Addr;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

proof fn lemma_multicast_segment(segment: u16, hi: u8, lo: u8)
    requires
        segment as int == (hi as int) * 256 + lo as int,
    ensures
        ((segment & 0xff00) == 0xff00) == (hi == 0xff),
{
    let hi16 = hi as u16;
    let lo16 = lo as u16;
    assert(segment == hi16 * 256 + lo16);
    assert(hi16 < 256);
    assert(lo16 < 256);
    assert(
        segment == hi16 * 256 + lo16 && hi16 < 256 && lo16 < 256 ==>
            (((segment & 0xff00) == 0xff00) == (hi16 == 0xff))
    ) by (bit_vector);
}

fn source_ipv6_is_multicast(address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_multicast(address@),
{
    let segments = address.segments();
    proof {
        axiom_ipv6_view_len(address);
        lemma_multicast_segment(segments[0], address@[0], address@[1]);
    }
    (segments[0] & 0xff00) == 0xff00
}

} // verus!

fn main() {}