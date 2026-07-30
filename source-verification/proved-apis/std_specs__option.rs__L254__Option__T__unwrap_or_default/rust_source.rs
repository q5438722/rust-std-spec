pub const fn unwrap_or_default(self) -> T
    where
        T: [const] Default,
    {
        match self {
            Some(x) => x,
            None => T::default(),
        }
    }
