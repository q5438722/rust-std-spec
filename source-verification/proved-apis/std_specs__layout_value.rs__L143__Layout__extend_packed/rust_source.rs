pub const fn extend_packed(&self, next: Self) -> Result<Self, LayoutError> {
        // SAFETY: each `size` is at most `isize::MAX == usize::MAX/2`, so the
        // sum is at most `usize::MAX/2*2 == usize::MAX - 1`, and cannot overflow.
        let new_size = unsafe { unchecked_add(self.size, next.size) };
        // The safe constructor enforces that the new size isn't too big for the alignment
        Layout::from_size_alignment(new_size, self.align)
    }
