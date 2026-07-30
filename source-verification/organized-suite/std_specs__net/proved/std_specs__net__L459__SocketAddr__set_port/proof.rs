#![allow(dead_code)]

use core::net::{
    IpAddr, Ipv4Addr, Ipv6Addr, SocketAddr, SocketAddrV4, SocketAddrV6,
};
use vstd::prelude::*;
use vstd::std_specs::net::{
    IpAddrView, SocketAddrV4View, SocketAddrV6View, SocketAddrView,
};

verus! {

proof fn ip_addr_v4_view(address: Ipv4Addr)
    ensures
        IpAddr::V4(address)@ == IpAddrView::V4(address@)
{}

proof fn ip_addr_v6_view(address: Ipv6Addr)
    ensures
        IpAddr::V6(address)@ == IpAddrView::V6(address@)
{}

proof fn socket_addr_v4_view(address: SocketAddrV4)
    ensures
        SocketAddr::V4(address)@ == SocketAddrView::V4(address@)
{}

proof fn socket_addr_v6_view(address: SocketAddrV6)
    ensures
        SocketAddr::V6(address)@ == SocketAddrView::V6(address@)
{}

fn socket_addr_new_proof(ip: IpAddr, port: u16) -> (result: SocketAddr)
    ensures
        result@ == match ip@ {
            IpAddrView::V4(bytes) => SocketAddrView::V4(SocketAddrV4View { ip: bytes, port }),
            IpAddrView::V6(bytes) => SocketAddrView::V6(
                SocketAddrV6View { ip: bytes, port, flowinfo: 0, scope_id: 0 },
            ),
        },
{
    match ip {
        IpAddr::V4(address) => {
            let inner = SocketAddrV4::new(address, port);
            let result = SocketAddr::V4(inner);
            proof {
                ip_addr_v4_view(address);
                socket_addr_v4_view(inner);
            }
            result
        },
        IpAddr::V6(address) => {
            let inner = SocketAddrV6::new(address, port, 0, 0);
            let result = SocketAddr::V6(inner);
            proof {
                ip_addr_v6_view(address);
                socket_addr_v6_view(inner);
            }
            result
        },
    }
}

fn socket_addr_ip_proof(address: &SocketAddr) -> (result: IpAddr)
    ensures
        result@ == match address@ {
            SocketAddrView::V4(v4) => IpAddrView::V4(v4.ip),
            SocketAddrView::V6(v6) => IpAddrView::V6(v6.ip),
        },
{
    match *address {
        SocketAddr::V4(inner) => {
            let ip = *inner.ip();
            let result = IpAddr::V4(ip);
            proof {
                socket_addr_v4_view(inner);
                ip_addr_v4_view(ip);
            }
            result
        },
        SocketAddr::V6(inner) => {
            let ip = *inner.ip();
            let result = IpAddr::V6(ip);
            proof {
                socket_addr_v6_view(inner);
                ip_addr_v6_view(ip);
            }
            result
        },
    }
}

fn socket_addr_port_proof(address: &SocketAddr) -> (result: u16)
    ensures
        result == match address@ {
            SocketAddrView::V4(v4) => v4.port,
            SocketAddrView::V6(v6) => v6.port,
        },
{
    match *address {
        SocketAddr::V4(inner) => {
            proof {
                socket_addr_v4_view(inner);
            }
            inner.port()
        },
        SocketAddr::V6(inner) => {
            proof {
                socket_addr_v6_view(inner);
            }
            inner.port()
        },
    }
}

fn socket_addr_is_ipv4_proof(address: &SocketAddr) -> (result: bool)
    ensures
        result <==> address@ is V4,
{
    match *address {
        SocketAddr::V4(inner) => {
            proof {
                socket_addr_v4_view(inner);
            }
            true
        },
        SocketAddr::V6(inner) => {
            proof {
                socket_addr_v6_view(inner);
            }
            false
        },
    }
}

fn socket_addr_is_ipv6_proof(address: &SocketAddr) -> (result: bool)
    ensures
        result <==> address@ is V6,
{
    match *address {
        SocketAddr::V4(inner) => {
            proof {
                socket_addr_v4_view(inner);
            }
            false
        },
        SocketAddr::V6(inner) => {
            proof {
                socket_addr_v6_view(inner);
            }
            true
        },
    }
}

fn socket_addr_set_port_proof(address: &mut SocketAddr, port: u16)
    ensures
        final(address)@ == match old(address)@ {
            SocketAddrView::V4(v4) => {
                SocketAddrView::V4(SocketAddrV4View { ip: v4.ip, port })
            },
            SocketAddrView::V6(v6) => SocketAddrView::V6(
                SocketAddrV6View { ip: v6.ip, port, flowinfo: v6.flowinfo, scope_id: v6.scope_id },
            ),
        },
{
    match address {
        SocketAddr::V4(inner) => {
            let old_inner = *inner;
            proof {
                socket_addr_v4_view(old_inner);
            }
            inner.set_port(port);
            proof {
                socket_addr_v4_view(*inner);
            }
        },
        SocketAddr::V6(inner) => {
            let old_inner = *inner;
            proof {
                socket_addr_v6_view(old_inner);
            }
            inner.set_port(port);
            proof {
                socket_addr_v6_view(*inner);
            }
        },
    }
}

fn socket_addr_set_ip_proof(address: &mut SocketAddr, new_ip: IpAddr)
    ensures
        final(address)@ == match (old(address)@, new_ip@) {
            (SocketAddrView::V4(old_v4), IpAddrView::V4(ip)) => {
                SocketAddrView::V4(SocketAddrV4View { ip, port: old_v4.port })
            },
            (SocketAddrView::V4(old_v4), IpAddrView::V6(ip)) => SocketAddrView::V6(
                SocketAddrV6View { ip, port: old_v4.port, flowinfo: 0, scope_id: 0 },
            ),
            (SocketAddrView::V6(old_v6), IpAddrView::V4(ip)) => {
                SocketAddrView::V4(SocketAddrV4View { ip, port: old_v6.port })
            },
            (SocketAddrView::V6(old_v6), IpAddrView::V6(ip)) => SocketAddrView::V6(
                SocketAddrV6View {
                    ip,
                    port: old_v6.port,
                    flowinfo: old_v6.flowinfo,
                    scope_id: old_v6.scope_id,
                },
            ),
        },
{
    match new_ip {
        IpAddr::V4(ip) => match address {
            SocketAddr::V4(inner) => {
                let old_inner = *inner;
                proof {
                    socket_addr_v4_view(old_inner);
                    ip_addr_v4_view(ip);
                    assert(old(address)@ == SocketAddrView::V4(old_inner@));
                    assert(new_ip@ == IpAddrView::V4(ip@));
                }
                inner.set_ip(ip);
                proof {
                    socket_addr_v4_view(*inner);
                    assert(final(address)@ == SocketAddrView::V4(final(inner)@));
                }
            },
            SocketAddr::V6(inner) => {
                let old_inner = *inner;
                proof {
                    socket_addr_v6_view(old_inner);
                    ip_addr_v4_view(ip);
                    assert(old(address)@ == SocketAddrView::V6(old_inner@));
                    assert(new_ip@ == IpAddrView::V4(ip@));
                }
                let port = inner.port();
                let result = SocketAddrV4::new(ip, port);
                *address = SocketAddr::V4(result);
                proof {
                    socket_addr_v4_view(result);
                }
            },
        },
        IpAddr::V6(ip) => match address {
            SocketAddr::V4(inner) => {
                let old_inner = *inner;
                proof {
                    socket_addr_v4_view(old_inner);
                    ip_addr_v6_view(ip);
                    assert(old(address)@ == SocketAddrView::V4(old_inner@));
                    assert(new_ip@ == IpAddrView::V6(ip@));
                }
                let port = inner.port();
                let result = SocketAddrV6::new(ip, port, 0, 0);
                *address = SocketAddr::V6(result);
                proof {
                    socket_addr_v6_view(result);
                }
            },
            SocketAddr::V6(inner) => {
                let old_inner = *inner;
                proof {
                    socket_addr_v6_view(old_inner);
                    ip_addr_v6_view(ip);
                    assert(old(address)@ == SocketAddrView::V6(old_inner@));
                    assert(new_ip@ == IpAddrView::V6(ip@));
                }
                inner.set_ip(ip);
                proof {
                    socket_addr_v6_view(*inner);
                    assert(final(address)@ == SocketAddrView::V6(final(inner)@));
                }
            },
        },
    }
}

} // verus!

fn main() {}
