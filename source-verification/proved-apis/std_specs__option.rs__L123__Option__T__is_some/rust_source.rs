pub const fn is_some(&self) -> bool {
        matches!(*self, Some(_))
    }
