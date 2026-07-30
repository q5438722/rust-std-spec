pub const fn as_str(&self) -> &str {
        // SAFETY: String contents are stipulated to be valid UTF-8, invalid contents are an error
        // at construction.
        unsafe { str::from_utf8_unchecked(self.vec.as_slice()) }
    }
