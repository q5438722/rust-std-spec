pub const fn is_broadcast(&self) -> bool {
        u32::from_be_bytes(self.octets()) == u32::from_be_bytes(Self::BROADCAST.octets())
    }
