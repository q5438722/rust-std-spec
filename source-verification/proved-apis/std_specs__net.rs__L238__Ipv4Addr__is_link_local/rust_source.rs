pub const fn is_link_local(&self) -> bool {
        matches!(self.octets(), [169, 254, ..])
    }
