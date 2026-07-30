#![allow(dead_code)]

use core::net::Ipv6Addr;
use vstd::arithmetic::div_mod::lemma_fundamental_div_mod_converse;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn ipv6_is_unique_local_proof(address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_unique_local(address@),
{
    let segment = address.segments()[0];
    proof {
        let first_octet = address@[0];
        let second_octet = address@[1];
        assert(
            segment as int
                == (first_octet as int) * 256 + second_octet as int
        );
        lemma_fundamental_div_mod_converse(
            segment as int,
            256,
            first_octet as int,
            second_octet as int,
        );
        assert(segment / 256 == first_octet as u16);
        assert(
            segment / 256 == first_octet as u16
                ==> (
                    (segment & 0xfe00) == 0xfc00
                        <==> first_octet / 2 == 0x7e
                )
        ) by (bit_vector);
        assert(
            (segment & 0xfe00) == 0xfc00
                <==> first_octet / 2 == 0x7e
        );
    }
    (segment & 0xfe00) == 0xfc00
}

} // verus!

fn main() {}