pub const fn unwrap(self) -> T {
        match self {
            Some(val) => val,
            None => unwrap_failed(),
        }
    }
