    pub const unsafe fn assume_init_mut(&mut self) -> &mut [T] {
        // SAFETY: similar to safety notes for `slice_get_ref`, but we have a
        // mutable reference which is also guaranteed to be valid for writes.
        unsafe { &mut *(self as *mut Self as *mut [T]) }
    }
