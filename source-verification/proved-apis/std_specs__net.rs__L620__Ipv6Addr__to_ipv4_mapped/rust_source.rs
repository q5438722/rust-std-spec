pub const fn to_ipv4_mapped(&self) -> Option<Ipv4Addr> {
        match self.octets() {
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff, a, b, c, d] => {
                Some(Ipv4Addr::new(a, b, c, d))
            }
            _ => None,
        }
    }
