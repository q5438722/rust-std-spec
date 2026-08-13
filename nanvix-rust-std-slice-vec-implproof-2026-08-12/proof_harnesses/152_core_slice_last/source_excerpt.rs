    pub const fn last(&self) -> Option<&T> {
        if let [.., last] = self { Some(last) } else { None }
    }
