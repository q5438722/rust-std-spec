    pub const fn as_mut_ptr_range(&mut self) -> Range<*mut T> {
        let start = self.as_mut_ptr();
        // SAFETY: See as_ptr_range() above for why `add` here is safe.
        let end = unsafe { start.add(self.len()) };
        start..end
    }
