pub const fn map_err<F, O>(self, op: O) -> Result<T, F>
    where
        O: [const] FnOnce(E) -> F + [const] Destruct,
    {
        match self {
            Ok(t) => Ok(t),
            Err(e) => Err(op(e)),
        }
    }
