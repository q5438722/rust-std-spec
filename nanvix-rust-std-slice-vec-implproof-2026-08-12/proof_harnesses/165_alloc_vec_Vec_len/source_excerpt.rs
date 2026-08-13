    pub const fn len(&self) -> usize {
        let len = self.len;

        // SAFETY: The maximum capacity of `Vec<T>` is `isize::MAX` bytes, so the maximum value can
        // be returned is `usize::checked_div(size_of::<T>()).unwrap_or(usize::MAX)`, which
        // matches the definition of `T::MAX_SLICE_LEN`.
        unsafe { intrinsics::assume(len <= T::MAX_SLICE_LEN) };

        len
    }
