pub const fn ok_or<E: [const] Destruct>(self, err: E) -> Result<T, E> {
        match self {
            Some(v) => Ok(v),
            None => Err(err),
        }
    }
