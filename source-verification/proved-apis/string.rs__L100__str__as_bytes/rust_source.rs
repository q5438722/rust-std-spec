pub const fn as_bytes(&self) -> &[u8] {
        // SAFETY: const sound because we transmute two types with the same layout
        unsafe { mem::transmute(self) }
    }
