pub fn reserve_exact(&mut self, additional: usize) {
        self.buf.reserve_exact(self.len, additional);
    }
