pub const fn segments(&self) -> [u16; 8] {
        // All elements in `self.octets` must be big endian.
        // SAFETY: `[u8; 16]` is always safe to transmute to `[u16; 8]`.
        let [a, b, c, d, e, f, g, h] = unsafe { transmute::<_, [u16; 8]>(self.octets) };
        // We want native endian u16
        [
            u16::from_be(a),
            u16::from_be(b),
            u16::from_be(c),
            u16::from_be(d),
            u16::from_be(e),
            u16::from_be(f),
            u16::from_be(g),
            u16::from_be(h),
        ]
    }
