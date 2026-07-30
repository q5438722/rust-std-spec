pub const fn is_empty(&self) -> bool {
        // SAFETY: We know there is at least one byte; for empty strings it
        // is the NUL terminator.
        // FIXME(const-hack): use get_unchecked
        unsafe { *self.inner.as_ptr() == 0 }
    }
