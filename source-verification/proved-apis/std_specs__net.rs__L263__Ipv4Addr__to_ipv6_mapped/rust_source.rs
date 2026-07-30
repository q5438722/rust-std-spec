pub const fn to_ipv6_mapped(&self) -> Ipv6Addr {
        let [a, b, c, d] = self.octets();
        Ipv6Addr { octets: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xFF, 0xFF, a, b, c, d] }
    }
