pub const fn from_segments(segments: [u16; 8]) -> Ipv6Addr {
        let [a, b, c, d, e, f, g, h] = segments;
        Ipv6Addr::new(a, b, c, d, e, f, g, h)
    }
