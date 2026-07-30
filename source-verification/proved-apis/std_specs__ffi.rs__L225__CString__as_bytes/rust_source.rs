pub fn as_bytes(&self) -> &[u8] {
        // SAFETY: CString has a length at least 1
        unsafe { self.inner.get_unchecked(..self.inner.len() - 1) }
    }
