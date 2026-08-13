    pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {
        self.buf.try_reserve(self.len, additional)
    }
