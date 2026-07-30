pub const fn is_unspecified(&self) -> bool {
        u32::from_be_bytes(self.octets) == 0
    }
