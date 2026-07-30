#![allow(dead_code)]

use core::net::Ipv6Addr;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn ipv6_is_unicast_link_local_proof(address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_unicast_link_local(address@),
{
    let segment = address.segments()[0];
    proof {
        axiom_ipv6_view_len(address);
        let first_octet = address@[0];
        let second_octet = address@[1];
        assert(
            segment as int
                == (first_octet as int) * 256 + second_octet as int
        );
        assert(
            (segment & 0xffc0) == 0xfe80
                <==> segment >= 0xfe80 && segment <= 0xfebf
        ) by (bit_vector);
        assert(
            second_octet / 64 == 2
                <==> second_octet >= 128 && second_octet <= 191
        ) by (bit_vector);
        assert(0 <= first_octet as int && first_octet as int <= 255);
        assert(0 <= second_octet as int && second_octet as int <= 255);
        assert(
            ((segment as int) >= 0xfe80 && (segment as int) <= 0xfebf)
                <==> (first_octet as int) == 254
                    && (second_octet as int) >= 128
                    && (second_octet as int) <= 191
        );
    }
    (segment & 0xffc0) == 0xfe80
}

} // verus!

fn main() {}