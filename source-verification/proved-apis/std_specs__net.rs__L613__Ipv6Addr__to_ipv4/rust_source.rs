pub const fn to_ipv4(&self) -> Option<Ipv4Addr> {
        if let [0, 0, 0, 0, 0, 0 | 0xffff, ab, cd] = self.segments() {
            let [a, b] = ab.to_be_bytes();
            let [c, d] = cd.to_be_bytes();
            Some(Ipv4Addr::new(a, b, c, d))
        } else {
            None
        }
    }
