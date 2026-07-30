#![allow(dead_code)]

use core::net::Ipv6Addr;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_ipv6_from_octets(octets: [u8; 16]) -> (result: Ipv6Addr)
    ensures
        result@ == octets@,
{
    let result = Ipv6Addr::new(
        (octets[0] as u16) * 256 + octets[1] as u16,
        (octets[2] as u16) * 256 + octets[3] as u16,
        (octets[4] as u16) * 256 + octets[5] as u16,
        (octets[6] as u16) * 256 + octets[7] as u16,
        (octets[8] as u16) * 256 + octets[9] as u16,
        (octets[10] as u16) * 256 + octets[11] as u16,
        (octets[12] as u16) * 256 + octets[13] as u16,
        (octets[14] as u16) * 256 + octets[15] as u16,
    );
    proof {
        assert_seqs_equal!(result@, octets@);
    }
    result
}

}

fn main() {}