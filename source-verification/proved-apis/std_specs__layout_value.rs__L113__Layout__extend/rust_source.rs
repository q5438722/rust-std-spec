pub const fn extend(&self, next: Self) -> Result<(Self, usize), LayoutError> {
        let new_alignment = Alignment::max(self.align, next.align);
        let offset = self.size_rounded_up_to_custom_alignment(next.align);

        // SAFETY: `offset` is at most `isize::MAX + 1` (such as from aligning
        // to `Alignment::MAX`) and `next.size` is at most `isize::MAX` (from the
        // `Layout` type invariant).  Thus the largest possible `new_size` is
        // `isize::MAX + 1 + isize::MAX`, which is `usize::MAX`, and cannot overflow.
        let new_size = unsafe { unchecked_add(offset, next.size) };

        if let Ok(layout) = Layout::from_size_alignment(new_size, new_alignment) {
            Ok((layout, offset))
        } else {
            Err(LayoutError)
        }
    }
