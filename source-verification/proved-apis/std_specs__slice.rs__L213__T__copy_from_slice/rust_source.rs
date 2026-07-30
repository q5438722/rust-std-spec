pub const fn copy_from_slice(&mut self, src: &[T])
    where
        T: Copy,
    {
        // SAFETY: `T` implements `Copy`.
        unsafe { copy_from_slice_impl(self, src) }
    }
