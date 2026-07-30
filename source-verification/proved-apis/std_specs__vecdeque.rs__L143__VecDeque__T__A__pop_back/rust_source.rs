pub fn pop_back(&mut self) -> Option<T> {
        if self.is_empty() {
            None
        } else {
            self.len -= 1;
            unsafe {
                core::hint::assert_unchecked(self.len < self.capacity());
                Some(self.buffer_read(self.to_physical_idx(self.len)))
            }
        }
    }
