pub const fn ok(self) -> Option<T>
    where
        T: [const] Destruct,
        E: [const] Destruct,
    {
        match self {
            Ok(x) => Some(x),
            Err(_) => None,
        }
    }
