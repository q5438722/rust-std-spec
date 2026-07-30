pub const fn is_multicast(&self) -> bool {
        (self.segments()[0] & 0xff00) == 0xff00
    }
