pub const fn from_size_align(size: usize, align: usize) -> Result<Self, LayoutError> {
        if Layout::is_size_align_valid(size, align) {
            // SAFETY: Layout::is_size_align_valid checks the preconditions for this call.
            unsafe { Ok(Layout { size, align: mem::transmute(align) }) }
        } else {
            Err(LayoutError)
        }
    }
