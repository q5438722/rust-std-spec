pub const fn repeat_packed(&self, n: usize) -> Result<Self, LayoutError> {
        if let Some(size) = self.size.checked_mul(n) {
            // The safe constructor is called here to enforce the isize size limit.
            Layout::from_size_alignment(size, self.align)
        } else {
            Err(LayoutError)
        }
    }
