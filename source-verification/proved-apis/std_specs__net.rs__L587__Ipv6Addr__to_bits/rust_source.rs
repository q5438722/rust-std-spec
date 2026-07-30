pub const fn to_bits(self) -> u128 {
        u128::from_be_bytes(self.octets)
    }
