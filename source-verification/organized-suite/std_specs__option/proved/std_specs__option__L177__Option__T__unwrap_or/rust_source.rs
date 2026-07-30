pub const fn unwrap_or(self, default: T) -> T
    where
        T: [const] Destruct,
    {
        match self {
            Some(x) => x,
            None => default,
        }
    }
