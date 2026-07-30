pub const fn is_private(&self) -> bool {
        match self.octets() {
            [10, ..] => true,
            [172, b, ..] if b >= 16 && b <= 31 => true,
            [192, 168, ..] => true,
            _ => false,
        }
    }
