pub fn cloned(self) -> Option<T>
    where
        T: Clone,
    {
        self.map(T::clone)
    }
