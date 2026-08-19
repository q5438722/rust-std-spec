    pub const fn first(&self) -> Option<&T> {
        if let [first, ..] = self { Some(first) } else { None }
    }
