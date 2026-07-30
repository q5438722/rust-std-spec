pub const fn first_mut(&mut self) -> Option<&mut T> {
        if let [first, ..] = self { Some(first) } else { None }
    }
