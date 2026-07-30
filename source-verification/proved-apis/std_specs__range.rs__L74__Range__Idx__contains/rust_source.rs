pub const fn contains<U>(&self, item: &U) -> bool
    where
        Idx: [const] PartialOrd<U>,
        U: ?Sized + [const] PartialOrd<Idx>,
    {
        <Self as RangeBounds<Idx>>::contains(self, item)
    }
