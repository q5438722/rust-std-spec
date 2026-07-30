pub const fn to_str(&self) -> Result<&str, str::Utf8Error> {
        // N.B., when `CStr` is changed to perform the length check in `.to_bytes()`
        // instead of in `from_ptr()`, it may be worth considering if this should
        // be rewritten to do the UTF-8 check inline with the length calculation
        // instead of doing it afterwards.
        str::from_utf8(self.to_bytes())
    }
