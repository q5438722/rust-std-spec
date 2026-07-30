pub const fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: [const] FnOnce() -> T + [const] Destruct,
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
