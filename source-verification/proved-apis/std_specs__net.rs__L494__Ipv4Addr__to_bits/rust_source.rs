pub const fn to_bits(self) -> u32 {
        u32::from_be_bytes(self.octets)
    }
