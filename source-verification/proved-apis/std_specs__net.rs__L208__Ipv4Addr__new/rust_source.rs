pub const fn new(a: u8, b: u8, c: u8, d: u8) -> Ipv4Addr {
        Ipv4Addr { octets: [a, b, c, d] }
    }
