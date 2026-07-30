#![allow(dead_code)]

use core::net::{Ipv4Addr, Ipv6Addr};
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::net::{
    axiom_ipv4_view_len, axiom_ipv6_view_len, ipv4_is_broadcast, ipv4_is_documentation,
    ipv4_is_link_local, ipv4_is_loopback, ipv4_is_multicast, ipv4_is_private,
    ipv4_is_unspecified, ipv6_is_loopback, ipv6_is_multicast, ipv6_is_unicast_link_local,
    ipv6_is_unique_local, ipv6_is_unspecified,
};

verus! {

proof fn lemma_seq4_eq(bytes: Seq<u8>, a: u8, b: u8, c: u8, d: u8)
    requires
        bytes.len() == 4,
    ensures
        bytes == seq![a, b, c, d]
            <==> bytes[0] == a && bytes[1] == b && bytes[2] == c && bytes[3] == d,
{
    let expected = seq![a, b, c, d];
    if bytes[0] == a && bytes[1] == b && bytes[2] == c && bytes[3] == d {
        assert_seqs_equal!(bytes, expected);
    } else if bytes == expected {
        assert forall|i: int| 0 <= i < 4 implies bytes[i] == expected[i] by {}
        assert(expected[0] == a);
        assert(expected[1] == b);
        assert(expected[2] == c);
        assert(expected[3] == d);
        assert(false);
    }
}

proof fn lemma_ipv4_mapped_prefix(bytes: Seq<u8>)
    requires
        bytes.len() == 16,
    ensures
        bytes.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8]
            <==> bytes[0] == 0
                && bytes[1] == 0
                && bytes[2] == 0
                && bytes[3] == 0
                && bytes[4] == 0
                && bytes[5] == 0
                && bytes[6] == 0
                && bytes[7] == 0
                && bytes[8] == 0
                && bytes[9] == 0
                && bytes[10] == 0xff
                && bytes[11] == 0xff,
{
    let prefix = Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8];
    if bytes[0] == 0
        && bytes[1] == 0
        && bytes[2] == 0
        && bytes[3] == 0
        && bytes[4] == 0
        && bytes[5] == 0
        && bytes[6] == 0
        && bytes[7] == 0
        && bytes[8] == 0
        && bytes[9] == 0
        && bytes[10] == 0xff
        && bytes[11] == 0xff
    {
        assert_seqs_equal!(bytes.subrange(0, 12), prefix);
    } else if bytes.subrange(0, 12) == prefix {
        assert forall|i: int| 0 <= i < 12 implies bytes[i] == prefix[i] by {
            assert(bytes.subrange(0, 12)[i] == bytes[i]);
        }
        assert(prefix[0] == 0);
        assert(prefix[1] == 0);
        assert(prefix[2] == 0);
        assert(prefix[3] == 0);
        assert(prefix[4] == 0);
        assert(prefix[5] == 0);
        assert(prefix[6] == 0);
        assert(prefix[7] == 0);
        assert(prefix[8] == 0);
        assert(prefix[9] == 0);
        assert(prefix[10] == 0xff);
        assert(prefix[11] == 0xff);
        assert(bytes[0] == 0);
        assert(bytes[1] == 0);
        assert(bytes[2] == 0);
        assert(bytes[3] == 0);
        assert(bytes[4] == 0);
        assert(bytes[5] == 0);
        assert(bytes[6] == 0);
        assert(bytes[7] == 0);
        assert(bytes[8] == 0);
        assert(bytes[9] == 0);
        assert(bytes[10] == 0xff);
        assert(bytes[11] == 0xff);
        assert(false);
    }
}

fn ipv4_is_loopback_proof(address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_loopback(address@),
{
    address.octets()[0] == 127
}

fn ipv4_is_unspecified_proof(address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_unspecified(address@),
{
    let octets = address.octets();
    proof {
        axiom_ipv4_view_len(address);
        lemma_seq4_eq(address@, 0, 0, 0, 0);
    }
    octets[0] == 0 && octets[1] == 0 && octets[2] == 0 && octets[3] == 0
}

fn ipv4_is_private_proof(address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_private(address@),
{
    let octets = address.octets();
    octets[0] == 10
        || (octets[0] == 172 && octets[1] >= 16 && octets[1] <= 31)
        || (octets[0] == 192 && octets[1] == 168)
}

fn ipv4_is_link_local_proof(address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_link_local(address@),
{
    let octets = address.octets();
    octets[0] == 169 && octets[1] == 254
}

fn ipv4_is_multicast_proof(address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_multicast(address@),
{
    address.octets()[0] >= 224 && address.octets()[0] <= 239
}

fn ipv4_is_documentation_proof(address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_documentation(address@),
{
    let octets = address.octets();
    (octets[0] == 192 && octets[1] == 0 && octets[2] == 2)
        || (octets[0] == 198 && octets[1] == 51 && octets[2] == 100)
        || (octets[0] == 203 && octets[1] == 0 && octets[2] == 113)
}

fn ipv4_is_broadcast_proof(address: &Ipv4Addr) -> (result: bool)
    ensures
        result == ipv4_is_broadcast(address@),
{
    let octets = address.octets();
    proof {
        axiom_ipv4_view_len(address);
        lemma_seq4_eq(address@, 0xff, 0xff, 0xff, 0xff);
    }
    octets[0] == 0xff
        && octets[1] == 0xff
        && octets[2] == 0xff
        && octets[3] == 0xff
}

fn ipv4_to_ipv6_compatible_proof(address: &Ipv4Addr) -> (result: Ipv6Addr)
    ensures
        result@ == Seq::new(12, |i: int| 0u8) + address@,
{
    let octets = address.octets();
    Ipv6Addr::from_octets([
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        octets[0],
        octets[1],
        octets[2],
        octets[3],
    ])
}

fn ipv4_to_ipv6_mapped_proof(address: &Ipv4Addr) -> (result: Ipv6Addr)
    ensures
        result@ == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8] + address@,
{
    let octets = address.octets();
    Ipv6Addr::from_octets([
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0xff,
        0xff,
        octets[0],
        octets[1],
        octets[2],
        octets[3],
    ])
}

fn ipv6_to_ipv4_mapped_proof(address: &Ipv6Addr) -> (result: Option<Ipv4Addr>)
    ensures
        (result is Some) <==> address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8)
            + seq![0xffu8, 0xffu8],
        result is Some ==> result->Some_0@ == address@.subrange(12, 16),
{
    let octets = address.octets();
    proof {
        lemma_ipv4_mapped_prefix(address@);
    }
    if octets[0] == 0
        && octets[1] == 0
        && octets[2] == 0
        && octets[3] == 0
        && octets[4] == 0
        && octets[5] == 0
        && octets[6] == 0
        && octets[7] == 0
        && octets[8] == 0
        && octets[9] == 0
        && octets[10] == 0xff
        && octets[11] == 0xff
    {
        Some(Ipv4Addr::new(octets[12], octets[13], octets[14], octets[15]))
    } else {
        None
    }
}

fn ipv6_is_unspecified_proof(address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_unspecified(address@),
{
    let octets = address.octets();
    proof {
        axiom_ipv6_view_len(address);
        assert(octets@ == address@);
    }
    let mut index: usize = 0;
    while index < 16
        invariant
            index <= 16,
            octets@ == address@,
            forall|i: int| 0 <= i < index ==> octets@[i] == 0,
        decreases 16 - index,
    {
        if octets[index] != 0 {
            proof {
                reveal(ipv6_is_unspecified);
                assert(octets@[index as int] == address@[index as int]);
                assert(address@[index as int] != 0);
                assert(address@ != Seq::new(16, |i: int| 0u8));
            }
            return false;
        }
        index += 1;
    }
    proof {
        reveal(ipv6_is_unspecified);
        assert_seqs_equal!(address@, Seq::new(16, |i: int| 0u8));
    }
    true
}

fn ipv6_is_loopback_proof(address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_loopback(address@),
{
    let octets = address.octets();
    proof {
        axiom_ipv6_view_len(address);
        assert(octets@ == address@);
    }
    let mut index: usize = 0;
    while index < 15
        invariant
            index <= 15,
            octets@ == address@,
            forall|i: int| 0 <= i < index ==> octets@[i] == 0,
        decreases 15 - index,
    {
        if octets[index] != 0 {
            proof {
                reveal(ipv6_is_loopback);
                assert(octets@[index as int] == address@[index as int]);
                assert(address@[index as int] != 0);
                if address@.subrange(0, 15) == Seq::new(15, |i: int| 0u8) {
                    assert(address@.subrange(0, 15)[index as int] == address@[index as int]);
                    assert(Seq::new(15, |i: int| 0u8)[index as int] == 0);
                    assert(false);
                }
                assert(address@.subrange(0, 15) != Seq::new(15, |i: int| 0u8));
            }
            return false;
        }
        index += 1;
    }
    if octets[15] != 1 {
        return false;
    }
    proof {
        reveal(ipv6_is_loopback);
        assert_seqs_equal!(address@.subrange(0, 15), Seq::new(15, |i: int| 0u8));
    }
    true
}

fn ipv6_is_multicast_proof(address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_multicast(address@),
{
    let octets = address.octets();
    proof {
        axiom_ipv6_view_len(address);
        assert(octets@ == address@);
    }
    octets[0] == 0xff
}

fn ipv6_is_unique_local_proof(address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_unique_local(address@),
{
    let octets = address.octets();
    proof {
        axiom_ipv6_view_len(address);
        assert(octets@ == address@);
    }
    octets[0] / 2 == 0x7e
}

fn ipv6_is_unicast_link_local_proof(address: &Ipv6Addr) -> (result: bool)
    ensures
        result == ipv6_is_unicast_link_local(address@),
{
    let octets = address.octets();
    proof {
        axiom_ipv6_view_len(address);
        assert(octets@ == address@);
    }
    octets[0] == 0xfe && octets[1] / 64 == 2
}

} // verus!

fn main() {}
