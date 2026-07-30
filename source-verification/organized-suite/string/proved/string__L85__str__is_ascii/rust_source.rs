pub const fn is_ascii(&self) -> bool {
        // We can treat each byte as character here: all multibyte characters
        // start with a byte that is not in the ASCII range, so we will stop
        // there already.
        self.as_bytes().is_ascii()
    }
