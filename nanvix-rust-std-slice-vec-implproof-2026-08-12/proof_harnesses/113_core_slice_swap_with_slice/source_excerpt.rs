    pub const fn swap_with_slice(&mut self, other: &mut [T]) {
        assert!(self.len() == other.len(), "destination and source slices have different lengths");
        // SAFETY: `self` is valid for `self.len()` elements by definition, and `src` was
        // checked to have the same length. The slices cannot overlap because
        // mutable references are exclusive.
        unsafe {
            ptr::swap_nonoverlapping(self.as_mut_ptr(), other.as_mut_ptr(), self.len());
        }
    }
