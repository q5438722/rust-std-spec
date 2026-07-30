pub const fn ok_or_else<E, F>(self, err: F) -> Result<T, E>
    where
        F: [const] FnOnce() -> E + [const] Destruct,
    {
        match self {
            Some(v) => Ok(v),
            None => Err(err()),
        }
    }
