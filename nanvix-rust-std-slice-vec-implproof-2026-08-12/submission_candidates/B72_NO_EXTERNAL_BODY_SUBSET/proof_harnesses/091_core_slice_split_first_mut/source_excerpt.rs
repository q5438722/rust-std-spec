    pub const fn split_first_mut(&mut self) -> Option<(&mut T, &mut [T])> {
        if let [first, tail @ ..] = self { Some((first, tail)) } else { None }
    }
