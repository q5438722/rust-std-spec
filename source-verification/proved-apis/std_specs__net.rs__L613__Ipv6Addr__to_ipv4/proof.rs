#![allow(dead_code)]

use core::net::{Ipv4Addr, Ipv6Addr};
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

proof fn lemma_zero_prefix(bytes: Seq<u8>)
    requires bytes.len() == 16,
    ensures
        bytes.subrange(0, 12) == Seq::new(12, |i: int| 0u8)
            <==> bytes[0] == 0 && bytes[1] == 0 && bytes[2] == 0
                && bytes[3] == 0 && bytes[4] == 0 && bytes[5] == 0
                && bytes[6] == 0 && bytes[7] == 0 && bytes[8] == 0
                && bytes[9] == 0 && bytes[10] == 0 && bytes[11] == 0,
{
    let prefix = Seq::new(12, |i: int| 0u8);
    if bytes[0] == 0 && bytes[1] == 0 && bytes[2] == 0
        && bytes[3] == 0 && bytes[4] == 0 && bytes[5] == 0
        && bytes[6] == 0 && bytes[7] == 0 && bytes[8] == 0
        && bytes[9] == 0 && bytes[10] == 0 && bytes[11] == 0
    {
        assert_seqs_equal!(bytes.subrange(0, 12), prefix);
    } else if bytes.subrange(0, 12) == prefix {
        assert forall|i: int| 0 <= i < 12 implies bytes[i] == prefix[i] by {
            assert(bytes.subrange(0, 12)[i] == bytes[i]);
        }
        assert(prefix[0] == 0); assert(prefix[1] == 0);
        assert(prefix[2] == 0); assert(prefix[3] == 0);
        assert(prefix[4] == 0); assert(prefix[5] == 0);
        assert(prefix[6] == 0); assert(prefix[7] == 0);
        assert(prefix[8] == 0); assert(prefix[9] == 0);
        assert(prefix[10] == 0); assert(prefix[11] == 0);
        assert(bytes[0] == 0); assert(bytes[1] == 0);
        assert(bytes[2] == 0); assert(bytes[3] == 0);
        assert(bytes[4] == 0); assert(bytes[5] == 0);
        assert(bytes[6] == 0); assert(bytes[7] == 0);
        assert(bytes[8] == 0); assert(bytes[9] == 0);
        assert(bytes[10] == 0); assert(bytes[11] == 0);
        assert(false);
    }
}

proof fn lemma_mapped_prefix(bytes: Seq<u8>)
    requires bytes.len() == 16,
    ensures
        bytes.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8]
            <==> bytes[0] == 0 && bytes[1] == 0 && bytes[2] == 0
                && bytes[3] == 0 && bytes[4] == 0 && bytes[5] == 0
                && bytes[6] == 0 && bytes[7] == 0 && bytes[8] == 0
                && bytes[9] == 0 && bytes[10] == 0xff && bytes[11] == 0xff,
{
    let prefix = Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8];
    if bytes[0] == 0 && bytes[1] == 0 && bytes[2] == 0
        && bytes[3] == 0 && bytes[4] == 0 && bytes[5] == 0
        && bytes[6] == 0 && bytes[7] == 0 && bytes[8] == 0
        && bytes[9] == 0 && bytes[10] == 0xff && bytes[11] == 0xff
    {
        assert_seqs_equal!(bytes.subrange(0, 12), prefix);
    } else if bytes.subrange(0, 12) == prefix {
        assert forall|i: int| 0 <= i < 12 implies bytes[i] == prefix[i] by {
            assert(bytes.subrange(0, 12)[i] == bytes[i]);
        }
        assert(prefix[0] == 0); assert(prefix[1] == 0);
        assert(prefix[2] == 0); assert(prefix[3] == 0);
        assert(prefix[4] == 0); assert(prefix[5] == 0);
        assert(prefix[6] == 0); assert(prefix[7] == 0);
        assert(prefix[8] == 0); assert(prefix[9] == 0);
        assert(prefix[10] == 0xff); assert(prefix[11] == 0xff);
        assert(bytes[0] == 0); assert(bytes[1] == 0);
        assert(bytes[2] == 0); assert(bytes[3] == 0);
        assert(bytes[4] == 0); assert(bytes[5] == 0);
        assert(bytes[6] == 0); assert(bytes[7] == 0);
        assert(bytes[8] == 0); assert(bytes[9] == 0);
        assert(bytes[10] == 0xff); assert(bytes[11] == 0xff);
        assert(false);
    }
}

proof fn lemma_segment_zero(segment: u16, hi: u8, lo: u8)
    requires segment as int == (hi as int) * 256 + lo as int,
    ensures segment == 0 <==> hi == 0 && lo == 0,
{
    if segment == 0 { assert(hi == 0); assert(lo == 0); }
    if hi == 0 && lo == 0 { assert(segment == 0); }
}

proof fn lemma_segment_ffff(segment: u16, hi: u8, lo: u8)
    requires segment as int == (hi as int) * 256 + lo as int,
    ensures segment == 0xffff <==> hi == 0xff && lo == 0xff,
{
    if segment == 0xffff { assert(hi == 0xff); assert(lo == 0xff); }
    if hi == 0xff && lo == 0xff { assert(segment == 0xffff); }
}

proof fn lemma_unpack_segment(segment: u16, hi: u8, lo: u8)
    requires segment as int == (hi as int) * 256 + lo as int,
    ensures
        (segment >> 8) as u8 == hi,
        (segment & 0xff) as u8 == lo,
{
    let hi16 = hi as u16;
    let lo16 = lo as u16;
    assert(segment == hi16 * 256 + lo16);
    assert(segment == hi16 * 256 + lo16 && hi16 < 256 && lo16 < 256
        ==> segment == (hi16 << 8) | lo16) by (bit_vector);
    assert(segment == (hi16 << 8) | lo16 && hi16 < 256 && lo16 < 256
        ==> segment >> 8 == hi16) by (bit_vector);
    assert(segment == (hi16 << 8) | lo16 && hi16 < 256 && lo16 < 256
        ==> segment & 0xff == lo16) by (bit_vector);
}

proof fn lemma_tail(bytes: Seq<u8>)
    requires bytes.len() == 16,
    ensures bytes.subrange(12, 16) == seq![bytes[12], bytes[13], bytes[14], bytes[15]],
{
    assert_seqs_equal!(
        bytes.subrange(12, 16),
        seq![bytes[12], bytes[13], bytes[14], bytes[15]]
    );
}

fn source_ipv6_to_ipv4(address: &Ipv6Addr) -> (result: Option<Ipv4Addr>)
    ensures
        (result is Some) <==> (address@.subrange(0, 12) == Seq::new(12, |i: int| 0u8)
            || address@.subrange(0, 12)
                == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8]),
        result is Some ==> result->Some_0@ == address@.subrange(12, 16),
{
    let segments = address.segments();
    proof {
        axiom_ipv6_view_len(address);
        lemma_zero_prefix(address@);
        lemma_mapped_prefix(address@);
        lemma_segment_zero(segments[0], address@[0], address@[1]);
        lemma_segment_zero(segments[1], address@[2], address@[3]);
        lemma_segment_zero(segments[2], address@[4], address@[5]);
        lemma_segment_zero(segments[3], address@[6], address@[7]);
        lemma_segment_zero(segments[4], address@[8], address@[9]);
        lemma_segment_zero(segments[5], address@[10], address@[11]);
        lemma_segment_ffff(segments[5], address@[10], address@[11]);
    }
    if segments[0] == 0
        && segments[1] == 0
        && segments[2] == 0
        && segments[3] == 0
        && segments[4] == 0
        && (segments[5] == 0 || segments[5] == 0xffff)
    {
        let ab = segments[6];
        let cd = segments[7];
        let a = (ab >> 8) as u8;
        let b = (ab & 0xff) as u8;
        let c = (cd >> 8) as u8;
        let d = (cd & 0xff) as u8;
        proof {
            lemma_unpack_segment(ab, address@[12], address@[13]);
            lemma_unpack_segment(cd, address@[14], address@[15]);
            lemma_tail(address@);
        }
        Some(Ipv4Addr::new(a, b, c, d))
    } else {
        None
    }
}

}

fn main() {}