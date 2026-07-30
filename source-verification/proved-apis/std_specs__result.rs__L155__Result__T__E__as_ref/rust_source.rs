pub const fn as_ref(&self) -> Result<&T, &E> {
        match *self {
            Ok(ref x) => Ok(x),
            Err(ref x) => Err(x),
        }
    }
