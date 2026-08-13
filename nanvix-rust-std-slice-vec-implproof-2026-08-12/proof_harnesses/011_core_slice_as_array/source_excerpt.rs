    pub const fn as_array<const N: usize>(&self) -> Option<&[T; N]> {
        if self.len() == N {
            let ptr = self.as_ptr().cast_array();

            // SAFETY: The underlying array of a slice can be reinterpreted as an actual array `[T; N]` if `N` is not greater than the slice's length.
            let me = unsafe { &*ptr };
            Some(me)
        } else {
            None
        }
    }
