pub const fn to_bytes(&self) -> &[u8] {
        let bytes = self.to_bytes_with_nul();
        // FIXME(const-hack) replace with range index
        // SAFETY: to_bytes_with_nul returns slice with length at least 1
        unsafe { slice::from_raw_parts(bytes.as_ptr(), bytes.len() - 1) }
    }
