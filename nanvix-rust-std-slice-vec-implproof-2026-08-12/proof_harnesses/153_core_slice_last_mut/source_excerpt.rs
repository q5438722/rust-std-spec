    pub const fn last_mut(&mut self) -> Option<&mut T> {
        if let [.., last] = self { Some(last) } else { None }
    }
