    pub const fn as_mut_array<const N: usize>(&mut self) -> Option<&mut [T; N]> {
        if self.len() == N {
            let ptr = self.as_mut_ptr().cast_array();

            // SAFETY: The underlying array of a slice can be reinterpreted as an actual array `[T; N]` if `N` is not greater than the slice's length.
            let me = unsafe { &mut *ptr };
            Some(me)
        } else {
            None
        }
    }
