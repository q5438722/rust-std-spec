pub const fn and_then<U, F>(self, f: F) -> Option<U>
    where
        F: [const] FnOnce(T) -> Option<U> + [const] Destruct,
    {
        match self {
            Some(x) => f(x),
            None => None,
        }
    }
