pub const fn from_bits(bits: u32) -> Ipv4Addr {
        Ipv4Addr { octets: bits.to_be_bytes() }
    }
