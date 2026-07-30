#![allow(dead_code)]

use core::net::{IpAddr, Ipv4Addr, Ipv6Addr};
use vstd::prelude::*;
use vstd::std_specs::net::{
    axiom_ipv6_view_len, ip_is_loopback, ip_is_multicast, ip_is_unspecified, IpAddrView,
};

verus! {

fn ip_addr_is_ipv4_proof(address: &IpAddr) -> (result: bool)
    ensures
        result <==> address@ is V4,
{
    match *address {
        IpAddr::V4(_) => true,
        IpAddr::V6(_) => false,
    }
}

fn ip_addr_is_ipv6_proof(address: &IpAddr) -> (result: bool)
    ensures
        result <==> address@ is V6,
{
    match *address {
        IpAddr::V4(_) => false,
        IpAddr::V6(_) => true,
    }
}

fn ip_addr_is_unspecified_proof(address: &IpAddr) -> (result: bool)
    ensures
        result == ip_is_unspecified(address@),
{
    match *address {
        IpAddr::V4(ip) => ip.is_unspecified(),
        IpAddr::V6(ip) => ip.is_unspecified(),
    }
}

fn ip_addr_is_loopback_proof(address: &IpAddr) -> (result: bool)
    ensures
        result == ip_is_loopback(address@),
{
    match *address {
        IpAddr::V4(ip) => ip.is_loopback(),
        IpAddr::V6(ip) => ip.is_loopback(),
    }
}

fn ip_addr_is_multicast_proof(address: &IpAddr) -> (result: bool)
    ensures
        result == ip_is_multicast(address@),
{
    match *address {
        IpAddr::V4(ip) => ip.is_multicast(),
        IpAddr::V6(ip) => ip.is_multicast(),
    }
}

fn ipv6_to_canonical_proof(address: &Ipv6Addr) -> (result: IpAddr)
    ensures
        result@ == if address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8)
            + seq![0xffu8, 0xffu8]
        {
            IpAddrView::V4(address@.subrange(12, 16))
        } else {
            IpAddrView::V6(address@)
        },
{
    match address.to_ipv4_mapped() {
        Some(ip) => IpAddr::V4(ip),
        None => IpAddr::V6(*address),
    }
}

fn ip_addr_to_canonical_proof(address: &IpAddr) -> (result: IpAddr)
    ensures
        result@ == match address@ {
            IpAddrView::V4(bytes) => IpAddrView::V4(bytes),
            IpAddrView::V6(bytes) => if bytes.len() == 16
                && bytes.subrange(0, 12) == Seq::new(10, |i: int| 0u8)
                    + seq![0xffu8, 0xffu8]
            {
                IpAddrView::V4(bytes.subrange(12, 16))
            } else {
                IpAddrView::V6(bytes)
            },
        },
{
    match *address {
        IpAddr::V4(ip) => {
            let result = IpAddr::V4(ip);
            proof {
                assert(address@ == IpAddrView::V4(ip@));
                assert(result@ == IpAddrView::V4(ip@));
            }
            result
        },
        IpAddr::V6(ip) => {
            proof {
                axiom_ipv6_view_len(&ip);
                assert(address@ == IpAddrView::V6(ip@));
            }
            ipv6_to_canonical_proof(&ip)
        },
    }
}

} // verus!

fn main() {}
