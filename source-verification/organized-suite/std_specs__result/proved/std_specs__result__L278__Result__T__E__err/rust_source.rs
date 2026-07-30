pub const fn err(self) -> Option<E>
    where
        T: [const] Destruct,
        E: [const] Destruct,
    {
        match self {
            Ok(_) => None,
            Err(x) => Some(x),
        }
    }
