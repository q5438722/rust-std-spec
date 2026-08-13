    pub const unsafe fn get_unchecked_mut<I>(&mut self, index: I) -> &mut I::Output
    where
        I: [const] SliceIndex<Self>,
    {
        // SAFETY: the caller must uphold the safety requirements for `get_unchecked_mut`;
        // the slice is dereferenceable because `self` is a safe reference.
        // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.
        unsafe { &mut *index.get_unchecked_mut(self) }
    }
