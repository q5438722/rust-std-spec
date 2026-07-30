pub const fn map<U, F>(self, f: F) -> Option<U>
    where
        F: [const] FnOnce(T) -> U + [const] Destruct,
    {
        match self {
            Some(x) => Some(f(x)),
            None => None,
        }
    }
