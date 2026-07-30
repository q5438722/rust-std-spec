#![allow(dead_code)]

use core::net::Ipv6Addr;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

proof fn lemma_segment_bytes(segment: u16)
    ensures
        (segment / 256) as u8 == ((segment >> 8) & 0xff) as u8,
        (segment % 256) as u8 == (segment & 0xff) as u8,
{
    assert(segment >> 8 == segment / 256) by (bit_vector);
    assert((segment >> 8) & 0xff == segment >> 8) by (bit_vector);
    assert(segment & 0xff == segment % 256) by (bit_vector);
}

fn ipv6_from_segments_proof(segments: [u16; 8]) -> (result: Ipv6Addr)
    ensures
        result@ == seq![
            ((segments@[0] >> 8) & 0xff) as u8,
            (segments@[0] & 0xff) as u8,
            ((segments@[1] >> 8) & 0xff) as u8,
            (segments@[1] & 0xff) as u8,
            ((segments@[2] >> 8) & 0xff) as u8,
            (segments@[2] & 0xff) as u8,
            ((segments@[3] >> 8) & 0xff) as u8,
            (segments@[3] & 0xff) as u8,
            ((segments@[4] >> 8) & 0xff) as u8,
            (segments@[4] & 0xff) as u8,
            ((segments@[5] >> 8) & 0xff) as u8,
            (segments@[5] & 0xff) as u8,
            ((segments@[6] >> 8) & 0xff) as u8,
            (segments@[6] & 0xff) as u8,
            ((segments@[7] >> 8) & 0xff) as u8,
            (segments@[7] & 0xff) as u8,
        ],
{
    let a = segments[0];
    let b = segments[1];
    let c = segments[2];
    let d = segments[3];
    let e = segments[4];
    let f = segments[5];
    let g = segments[6];
    let h = segments[7];
    proof {
        lemma_segment_bytes(a);
        lemma_segment_bytes(b);
        lemma_segment_bytes(c);
        lemma_segment_bytes(d);
        lemma_segment_bytes(e);
        lemma_segment_bytes(f);
        lemma_segment_bytes(g);
        lemma_segment_bytes(h);
    }
    Ipv6Addr::new(a, b, c, d, e, f, g, h)
}

}

fn main() {}