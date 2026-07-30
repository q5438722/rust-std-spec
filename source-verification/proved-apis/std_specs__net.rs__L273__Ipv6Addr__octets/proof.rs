#![allow(dead_code)]

use core::net::Ipv6Addr;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

proof fn lemma_unpack_segment(segment: u16, hi: u8, lo: u8)
    requires
        segment as int == (hi as int) * 256 + lo as int,
    ensures
        (segment >> 8) as u8 == hi,
        (segment & 0xff) as u8 == lo,
{
    let hi16 = hi as u16;
    let lo16 = lo as u16;
    assert(segment == hi16 * 256 + lo16);
    assert(
        segment == hi16 * 256 + lo16 && hi16 < 256 && lo16 < 256 ==>
            segment == (hi16 << 8) | lo16
    ) by (bit_vector);
    assert(
        segment == (hi16 << 8) | lo16 && hi16 < 256 && lo16 < 256 ==>
            segment >> 8 == hi16
    ) by (bit_vector);
    assert(
        segment == (hi16 << 8) | lo16 && hi16 < 256 && lo16 < 256 ==>
            segment & 0xff == lo16
    ) by (bit_vector);
}

fn source_ipv6_octets(address: &Ipv6Addr) -> (result: [u8; 16])
    ensures
        result@ == address@,
{
    let segments = address.segments();
    proof {
        lemma_unpack_segment(segments[0], address@[0], address@[1]);
        lemma_unpack_segment(segments[1], address@[2], address@[3]);
        lemma_unpack_segment(segments[2], address@[4], address@[5]);
        lemma_unpack_segment(segments[3], address@[6], address@[7]);
        lemma_unpack_segment(segments[4], address@[8], address@[9]);
        lemma_unpack_segment(segments[5], address@[10], address@[11]);
        lemma_unpack_segment(segments[6], address@[12], address@[13]);
        lemma_unpack_segment(segments[7], address@[14], address@[15]);
    }
    let result = [
        (segments[0] >> 8) as u8,
        (segments[0] & 0xff) as u8,
        (segments[1] >> 8) as u8,
        (segments[1] & 0xff) as u8,
        (segments[2] >> 8) as u8,
        (segments[2] & 0xff) as u8,
        (segments[3] >> 8) as u8,
        (segments[3] & 0xff) as u8,
        (segments[4] >> 8) as u8,
        (segments[4] & 0xff) as u8,
        (segments[5] >> 8) as u8,
        (segments[5] & 0xff) as u8,
        (segments[6] >> 8) as u8,
        (segments[6] & 0xff) as u8,
        (segments[7] >> 8) as u8,
        (segments[7] & 0xff) as u8,
    ];
    proof {
        axiom_ipv6_view_len(address);
        assert_seqs_equal!(result@, address@);
    }
    result
}

}

fn main() {}