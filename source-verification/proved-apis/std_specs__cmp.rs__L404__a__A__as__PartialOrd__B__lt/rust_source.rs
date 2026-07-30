fn lt(&self, other: &Rhs) -> bool {
        self.partial_cmp(other).is_some_and(Ordering::is_lt)
    }
