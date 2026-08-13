    pub fn extend_from_slice(&mut self, other: &[T]) {
        self.spec_extend(other.iter())
    }
