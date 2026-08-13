    pub fn reserve(&mut self, additional: usize) {
        self.buf.reserve(self.len, additional);
    }
