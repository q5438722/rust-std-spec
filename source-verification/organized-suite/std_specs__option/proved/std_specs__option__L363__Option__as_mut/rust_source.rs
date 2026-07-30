pub const fn as_mut(&mut self) -> Option<&mut T> {
        match *self {
            Some(ref mut x) => Some(x),
            None => None,
        }
    }
