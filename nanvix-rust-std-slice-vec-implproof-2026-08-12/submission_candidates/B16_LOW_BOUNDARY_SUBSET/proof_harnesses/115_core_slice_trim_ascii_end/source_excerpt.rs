    pub const fn trim_ascii_end(&self) -> &[u8] {
        let mut bytes = self;
        // Note: A pattern matching based approach (instead of indexing) allows
        // making the function const.
        while let [rest @ .., last] = bytes {
            if last.is_ascii_whitespace() {
                bytes = rest;
            } else {
                break;
            }
        }
        bytes
    }
