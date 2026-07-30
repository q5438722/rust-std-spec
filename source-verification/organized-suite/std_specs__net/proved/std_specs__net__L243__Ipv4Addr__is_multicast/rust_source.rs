pub const fn is_multicast(&self) -> bool {
        self.octets()[0] >= 224 && self.octets()[0] <= 239
    }
