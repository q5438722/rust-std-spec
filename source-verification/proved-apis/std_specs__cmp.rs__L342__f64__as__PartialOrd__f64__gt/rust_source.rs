fn gt(&self, other: &Rhs) -> bool {
        self.partial_cmp(other).is_some_and(Ordering::is_gt)
    }
