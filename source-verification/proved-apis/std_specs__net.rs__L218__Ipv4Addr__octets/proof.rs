#![allow(dead_code)]

use core::net::Ipv4Addr;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

proof fn lemma_unpack_ipv4(bits: u32, a: u8, b: u8, c: u8, d: u8)
    requires
        bits == (((a as u32) << 24)
            | ((b as u32) << 16)
            | ((c as u32) << 8)
            | (d as u32)),
    ensures
        (bits >> 24) as u8 == a,
        ((bits >> 16) & 0xff) as u8 == b,
        ((bits >> 8) & 0xff) as u8 == c,
        (bits & 0xff) as u8 == d,
{
    let aa = a as u32;
    let bb = b as u32;
    let cc = c as u32;
    let dd = d as u32;
    assert(
        (bits == ((aa << 24) | (bb << 16) | (cc << 8) | dd)
            && aa < 256 && bb < 256 && cc < 256 && dd < 256) ==>
            aa == bits >> 24
                && bb == ((bits >> 16) & 0xff)
                && cc == ((bits >> 8) & 0xff)
                && dd == (bits & 0xff)
    ) by (bit_vector);
}

fn source_ipv4_octets(address: &Ipv4Addr) -> (result: [u8; 4])
    ensures
        result@ == address@,
{
    let bits = (*address).to_bits();
    let a = (bits >> 24) as u8;
    let b = ((bits >> 16) & 0xff) as u8;
    let c = ((bits >> 8) & 0xff) as u8;
    let d = (bits & 0xff) as u8;
    proof {
        lemma_unpack_ipv4(
            bits,
            address@[0],
            address@[1],
            address@[2],
            address@[3],
        );
    }
    let result = [a, b, c, d];
    proof {
        axiom_ipv4_view_len(address);
        assert_seqs_equal!(result@, address@);
    }
    result
}

}

fn main() {}