    pub const fn get<I>(&self, index: I) -> Option<&I::Output>
    where
        I: [const] SliceIndex<Self>,
    {
        index.get(self)
    }
