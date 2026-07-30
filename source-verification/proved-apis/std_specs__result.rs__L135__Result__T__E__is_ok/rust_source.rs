pub const fn is_ok(&self) -> bool {
        matches!(*self, Ok(_))
    }
