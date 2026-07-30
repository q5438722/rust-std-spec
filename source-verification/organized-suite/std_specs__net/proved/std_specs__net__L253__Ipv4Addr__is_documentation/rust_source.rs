pub const fn is_documentation(&self) -> bool {
        matches!(self.octets(), [192, 0, 2, _] | [198, 51, 100, _] | [203, 0, 113, _])
    }
