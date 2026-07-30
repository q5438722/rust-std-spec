#![allow(dead_code)]

use core::net::Ipv4Addr;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::net::*;

verus! {

fn source_ipv4_from_octets(octets: [u8; 4]) -> (result: Ipv4Addr)
    ensures
        result@ == octets@,
{
    let result = Ipv4Addr::new(octets[0], octets[1], octets[2], octets[3]);
    proof {
        assert_seqs_equal!(result@, octets@);
    }
    result
}

}

fn main() {}