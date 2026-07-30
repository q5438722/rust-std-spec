pub fn get_or_insert(&mut self, value: T) -> &mut T {
        self.get_or_insert_with(|| value)
    }
