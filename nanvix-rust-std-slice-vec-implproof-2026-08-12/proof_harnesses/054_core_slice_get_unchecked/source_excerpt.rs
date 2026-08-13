    pub const unsafe fn get_unchecked<I>(&self, index: I) -> &I::Output
    where
        I: [const] SliceIndex<Self>,
    {
        // SAFETY: the caller must uphold most of the safety requirements for `get_unchecked`;
        // the slice is dereferenceable because `self` is a safe reference.
        // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.
        unsafe { &*index.get_unchecked(self) }
    }
