pub const fn new(a: u16, b: u16, c: u16, d: u16, e: u16, f: u16, g: u16, h: u16) -> Ipv6Addr {
        let addr16 = [
            a.to_be(),
            b.to_be(),
            c.to_be(),
            d.to_be(),
            e.to_be(),
            f.to_be(),
            g.to_be(),
            h.to_be(),
        ];
        Ipv6Addr {
            // All elements in `addr16` are big endian.
            // SAFETY: `[u16; 8]` is always safe to transmute to `[u8; 16]`.
            octets: unsafe { transmute::<_, [u8; 16]>(addr16) },
        }
    }
