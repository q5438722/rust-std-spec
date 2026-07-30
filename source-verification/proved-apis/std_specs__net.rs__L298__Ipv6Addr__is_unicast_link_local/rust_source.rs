pub const fn is_unicast_link_local(&self) -> bool {
        (self.segments()[0] & 0xffc0) == 0xfe80
    }
