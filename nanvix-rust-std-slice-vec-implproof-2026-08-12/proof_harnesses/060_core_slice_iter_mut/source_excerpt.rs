    pub const fn iter_mut(&mut self) -> IterMut<'_, T> {
        IterMut::new(self)
    }
