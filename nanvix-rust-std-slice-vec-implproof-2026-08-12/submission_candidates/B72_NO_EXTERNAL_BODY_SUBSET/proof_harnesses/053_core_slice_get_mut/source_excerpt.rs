    pub const fn get_mut<I>(&mut self, index: I) -> Option<&mut I::Output>
    where
        I: [const] SliceIndex<Self>,
    {
        index.get_mut(self)
    }
