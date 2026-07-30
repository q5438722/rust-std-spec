pub fn swap_remove_back(&mut self, index: usize) -> Option<T> {
        let length = self.len;
        if length > 0 && index < length - 1 {
            self.swap(index, length - 1);
        } else if index >= length {
            return None;
        }
        self.pop_back()
    }
