pub const fn is_unique_local(&self) -> bool {
        (self.segments()[0] & 0xfe00) == 0xfc00
    }
