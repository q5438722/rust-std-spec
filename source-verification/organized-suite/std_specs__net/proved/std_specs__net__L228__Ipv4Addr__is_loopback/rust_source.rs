pub const fn is_loopback(&self) -> bool {
        self.octets()[0] == 127
    }
