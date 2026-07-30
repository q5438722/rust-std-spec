pub fn clear(&mut self) {
        self.truncate(0);
        // Not strictly necessary, but leaves things in a more consistent/predictable state.
        self.head = 0;
    }
