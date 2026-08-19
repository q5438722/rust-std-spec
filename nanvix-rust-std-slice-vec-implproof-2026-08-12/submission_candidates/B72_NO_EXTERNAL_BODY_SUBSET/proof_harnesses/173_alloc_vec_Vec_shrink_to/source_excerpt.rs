    pub fn shrink_to(&mut self, min_capacity: usize) {
        if self.capacity() > min_capacity {
            self.buf.shrink_to_fit(cmp::max(self.len, min_capacity));
        }
    }
