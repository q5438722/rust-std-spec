pub const fn file(&self) -> &'a str {
        // SAFETY: The filename is valid.
        unsafe { self.filename.as_ref() }
    }
