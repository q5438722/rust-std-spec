pub const fn to_ipv6_compatible(&self) -> Ipv6Addr {
        let [a, b, c, d] = self.octets();
        Ipv6Addr { octets: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a, b, c, d] }
    }
