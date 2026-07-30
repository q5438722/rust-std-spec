pub const fn from_bits(bits: u128) -> Ipv6Addr {
        Ipv6Addr { octets: bits.to_be_bytes() }
    }
