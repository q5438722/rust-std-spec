pub fn reserve_exact(&mut self, additional: usize) {
        self.data.reserve_exact(additional);
    }
