pub fn back(&self) -> Option<&T> {
        self.get(self.len.wrapping_sub(1))
    }
