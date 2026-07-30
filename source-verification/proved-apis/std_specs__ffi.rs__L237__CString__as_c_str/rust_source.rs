pub fn as_c_str(&self) -> &CStr {
        unsafe { CStr::from_bytes_with_nul_unchecked(self.as_bytes_with_nul()) }
    }
