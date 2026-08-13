    pub fn dedup(&mut self) {
        self.dedup_by(|a, b| a == b)
    }
