pub const fn is_unspecified(&self) -> bool {
        u128::from_be_bytes(self.octets()) == u128::from_be_bytes(Ipv6Addr::UNSPECIFIED.octets())
    }
