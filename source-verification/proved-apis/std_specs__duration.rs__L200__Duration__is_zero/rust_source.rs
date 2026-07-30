pub const fn is_zero(&self) -> bool {
        self.secs == 0 && self.nanos.as_inner() == 0
    }
