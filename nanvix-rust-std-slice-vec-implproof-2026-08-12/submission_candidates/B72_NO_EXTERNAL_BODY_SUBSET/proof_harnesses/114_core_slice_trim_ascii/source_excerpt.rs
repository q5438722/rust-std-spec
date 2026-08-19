    pub const fn trim_ascii(&self) -> &[u8] {
        self.trim_ascii_start().trim_ascii_end()
    }
